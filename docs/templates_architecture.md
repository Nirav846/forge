# Forge Movement Template System Architecture Spec

This specification details the design of the **Movement Template System** for the Forge platform. It bridges high-level physical preparation theory (Strength & Conditioning) with scalable database architecture and future AI capabilities.

---

## 1. Strength & Conditioning Design Philosophy

Movement templates are structured blueprints designed to develop target athletic profiles without locking coaches or athletes into rigid exercise selections.

### A. Slot Structure & Mechanics
Every movement template is broken down into four tactical slots:
- **Primary Slot**: The cornerstone of the workout. Targets multi-joint, compound movements focusing on maximum neural output (e.g. Maximal Strength or peak Rate of Force Development). Typically utilizes heavy external loads (Barbells, Trap Bars).
- **Secondary Slot**: Supports the primary block. Focuses on unilateral strength, directional force development, and stabilizer integration (e.g. Lunges, Single-leg hinge variations).
- **Accessory Slot**: Focuses on muscular hypertrophy, structural balance, and target tissues key to injury prevention (e.g., Nordic Hamstring Curls for hamstring strains).
- **Core Slot**: Targets trunk integration (Rotation, Anti-Rotation, or Anti-Extension) to maximize force transfer through the kinetic chain.

### B. Progression Rules
Progressions govern how loading and intensity adapt over a training block:
- **Linear Load**: Adding a fixed load (e.g., 5 lbs) weekly if reps are completed.
- **Double Progression**: Increasing volume (reps) over weeks within a target zone, then increasing load and resetting reps.
- **Velocity-Based Training (VBT)**: Dynamically altering the load on a barbell to maintain a specific target speed (e.g. 0.80 m/s for explosive power).
- **RPE-Based**: Scaling weights based on Rating of Perceived Exertion (1–10 scale).

---

## 2. Relational Database Schema Explanation

The schema defined in [`000003_create_templates_schema.up.sql`](../migrations/000003_create_templates_schema.up.sql) integrates with our core lookups:

```
[movement_templates] ──(1:N)──> [template_slots]
                                      │
          ┌───────────────────────────┼───────────────────────────┐
          ▼                           ▼                           ▼
[slot_requirements]          [slot_progressions]     [slot_exercise_fallbacks]
  (AND/OR Filters)             (S&C Loading Specs)       (Explicit Alternatives)
```

- **`movement_templates`**: Houses template metadata, associated sport, target athlete roles, and training goals.
- **`template_slots`**: Establishes order and classifications (Primary, Secondary, etc.) for each workout section.
- **`slot_requirements`**: Holds lookup constraints. 
  - *AND Evaluation*: Multiple criteria in a single row must all be true (e.g., Hinge AND Kettlebell).
  - *OR Evaluation*: Multiple rows for the same slot are treated as alternative options.
- **`slot_progressions`**: Maps set, rep, intensity targets, and rules to the slot.
- **`slot_exercise_fallbacks`**: A static routing table allowing coaches to predefine preferred exercises and explicit fallbacks (e.g. Barbell Squat fallback to Trap Bar Deadlift).

---

## 3. Dynamic Exercise Substitution Engine

When compiling a template into a workout, the system resolves exercises dynamically. 

### Algorithmic Resolution Flow

```
   [Select Slot Requirements]
               │
               ▼
   [Query Exercises matching: ] ──> (Movement Pattern, Equipment, Quality)
               │
               ▼
   [Filter by Difficulty Level] ──> (Filter out levels above athlete capability)
               │
               ▼
   [Join Sport specificity rating] ──> (Order by Specificity DESC, Transfer Index DESC)
               │
               ▼
   [Select Top Match / Match Fallbacks]
```

### SQL Resolution Query
To compile exercises that satisfy a specific slot's requirements (e.g., Slot ID 1):
```sql
SELECT e.id, e.name, e.difficulty_level,
       COALESCE(esm.specificity_rating, 0) as sport_spec,
       COALESCE(esm.transfer_index, 0.0) as sport_transfer
FROM exercises e
JOIN exercise_movement_patterns emp ON e.id = emp.exercise_id
JOIN exercise_physical_qualities epq ON e.id = epq.exercise_id
JOIN exercise_equipment eeq ON e.id = eeq.exercise_id
LEFT JOIN exercise_sport_mapping esm ON e.id = esm.exercise_id AND esm.sport_id = (
    SELECT sport_id FROM movement_templates WHERE id = (
        SELECT template_id FROM template_slots WHERE id = 1
    )
)
WHERE emp.movement_pattern_id = (SELECT movement_pattern_id FROM slot_requirements WHERE slot_id = 1 LIMIT 1)
  AND epq.physical_quality_id = (SELECT physical_quality_id FROM slot_requirements WHERE slot_id = 1 LIMIT 1)
  AND eeq.equipment_id = (SELECT equipment_id FROM slot_requirements WHERE slot_id = 1 LIMIT 1)
  AND e.difficulty_level <= (SELECT difficulty_level FROM slot_requirements WHERE slot_id = 1 LIMIT 1)
ORDER BY sport_spec DESC, sport_transfer DESC, e.name ASC;
```

---

## 4. API Structure

### REST Endpoints

#### 1. Compile Template to Workout
Generates a concrete workout by resolving constraints against current athlete parameters and equipment availability.
- **Endpoint**: `POST /api/v1/templates/:id/compile`
- **Request Payload**:
  ```json
  {
    "athlete_id": 1024,
    "difficulty_cap": "Intermediate",
    "available_equipment": ["Bodyweight", "Dumbbell", "Kettlebell"],
    "exclude_exercise_ids": [45]
  }
  ```
- **Response Payload**:
  ```json
  {
    "workout_name": "Lower Body Power - Compiled",
    "sport": "American Football",
    "slots": [
      {
        "slot_type": "Primary",
        "slot_name": "Bilateral Power/Strength Lift",
        "assigned_exercise": {
          "id": 4,
          "name": "Trap Bar Deadlift",
          "mechanics_type": "Compound"
        },
        "progression": {
          "progression_type": "Velocity-Based",
          "intensity_target": "0.75-0.85 m/s",
          "volume_target": "4x3",
          "progression_rule": "Monitor velocity of first rep. If velocity > 0.85 m/s, increase load by 5-10 lbs."
        }
      }
    ]
  }
  ```

#### 2. Manage Fallbacks
Adds an explicit substitution route.
- **Endpoint**: `POST /api/v1/slots/:id/fallbacks`
- **Payload**:
  ```json
  {
    "preferred_exercise_id": 1,
    "fallback_exercise_id": 4,
    "preference_rank": 1
  }
  ```

---

### GraphQL Schema

```graphql
type MovementTemplate {
  id: ID!
  name: String!
  sport: Sport
  athleteRole: String
  trainingGoal: String!
  slots: [TemplateSlot!]!
}

type TemplateSlot {
  id: ID!
  slotType: SlotType!
  name: String!
  displayOrder: Int!
  notes: String
  requirements: [SlotRequirement!]!
  progression: SlotProgression
  fallbacks: [ExerciseFallback!]!
}

enum SlotType {
  PRIMARY
  SECONDARY
  ACCESSORY
  CORE
}

type SlotRequirement {
  id: ID!
  movementPattern: MovementPattern
  physicalQuality: PhysicalQuality
  trainingMethod: TrainingMethod
  equipment: Equipment
  difficultyLevel: String
  minRelevanceScore: Int
  minSpecificityRating: Int
  isMandatory: Boolean!
}

type SlotProgression {
  id: ID!
  progressionType: String!
  intensityTarget: String!
  volumeTarget: String!
  progressionRule: String!
  deloadProtocol: String
}

type ExerciseFallback {
  preferredExercise: Exercise!
  fallbackExercise: Exercise!
  preferenceRank: Int!
}

type Query {
  getTemplate(id: ID!): MovementTemplate
  listTemplates(sportId: ID): [MovementTemplate!]!
  resolveSlotExercises(slotId: ID!, difficultyCap: String!, availableEquipment: [ID!]): [Exercise!]!
}

type Mutation {
  createTemplate(name: String!, trainingGoal: String!, sportId: ID): MovementTemplate!
  addSlotFallback(slotId: ID!, preferredId: ID!, fallbackId: ID!, rank: Int!): ExerciseFallback!
}
```

---

## 5. Future AI Compatibility Spec

The schema is built to support immediate integration with Machine Learning (ML) and Large Language Models (LLMs).

### A. Semantic Search & Vector Embeddings
To enable AI to find similar exercises when physical parameters or constraints are too strict for SQL joins, we can extend the `exercises` table to store embeddings (e.g. using PostgreSQL `pgvector` extension):
```sql
-- Enable vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Add embedding column representing 1536-dimensional OpenAI vector of the exercise description & traits
ALTER TABLE exercises ADD COLUMN embedding vector(1536);

-- Index the embeddings for high-speed cosine similarity searches
CREATE INDEX idx_exercises_embedding ON exercises USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```
Using embeddings, the S&C engine can run a cosine similarity query to find semantic substitutions (e.g., "Find an exercise similar to a Barbell Back Squat but targeting stabilizers and using kettlebells").

### B. LLM Context Formatting
The JSON schema developed in `templates.json` can be serialized directly into an LLM context window. By prompting the model with:
1. **System Prompt**: Defining the S&C Scribe agent.
2. **Context**: The Movement Template JSON, available equipment, athlete injury profile (e.g., "Patellar Tendinopathy in left knee"), and current metrics.
3. **Task**: Generate a customized daily program.
Because our templates define *slots* and *constraints* rather than fixed routines, the LLM has strict guards for selecting safe exercises while having the creative freedom to adapt accessory and core blocks.

### C. ML-Driven Progression Adjustments
By tracking actual velocities (VBT) or RPE logs over weeks:
- A regression model can monitor velocity decay or RPE thresholds.
- When an athlete logs an RPE of 10 on a block targeted for RPE 8, the AI engine can intercept the progression rules, query the deload protocol stored in `slot_progressions.deload_protocol`, and dynamically step down volume or suggest an alternative exercise using the fallback engine.
