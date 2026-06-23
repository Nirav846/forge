# FORGE V2.5 IMPLEMENTATION PLAN

## Delivery: Single working Coach Accelerator

**Last architecture change. No more audits, ontologies, or redesigns.**

---

## 1. SCHEMA CHANGES

### 1.1 Migration Strategy

**Do not delete existing tables.** V1 schema (000001-000025) stays intact. V2.5 adds new tables alongside. All V1 code continues to work until fully replaced.

### 1.2 New Tables Required

#### `exercise_families` — The foundation of V2.5

```sql
CREATE TABLE exercise_families (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL,  -- 'Lower Body', 'Upper Body', 'Core', 'Explosive', 'Field'
    description TEXT,
    display_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Seed 15 families
INSERT INTO exercise_families (name, category, display_order) VALUES
('Double Leg Knee Dominant', 'Lower Body', 1),
('Double Leg Hip Dominant', 'Lower Body', 2),
('Single Leg Knee Dominant', 'Lower Body', 3),
('Single Leg Hip Dominant', 'Lower Body', 4),
('Horizontal Push', 'Upper Body', 5),
('Horizontal Pull', 'Upper Body', 6),
('Vertical Push', 'Upper Body', 7),
('Vertical Pull', 'Upper Body', 8),
('Core', 'Core', 9),
('Carry', 'Core', 10),
('Plyometric', 'Explosive', 11),
('Ballistic', 'Explosive', 12),
('Sprint', 'Field', 13),
('Change of Direction', 'Field', 14),
('Conditioning', 'Field', 15);
```

#### `exercise_family_mapping` — Maps existing exercises to new families

```sql
CREATE TABLE exercise_family_mapping (
    exercise_id BIGINT NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    family_id BIGINT NOT NULL REFERENCES exercise_families(id) ON DELETE CASCADE,
    is_primary BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (exercise_id, family_id)
);
```

Each exercise maps to exactly one primary family. Optionally secondary for cross-category exercises (e.g., Trap Bar Deadlift = Double Leg Hip Dominant primary, Double Leg Knee Dominant secondary).

#### `equipment_categories` — Equipment availability model

```sql
CREATE TABLE equipment_categories (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,  -- 'Full Gym', 'Basic Gym', 'Dumbbells Only', 'Field Only', 'Hotel Gym'
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE equipment_category_mapping (
    equipment_id BIGINT NOT NULL REFERENCES equipment(id) ON DELETE CASCADE,
    category_id BIGINT NOT NULL REFERENCES equipment_categories(id) ON DELETE CASCADE,
    PRIMARY KEY (equipment_id, category_id)
);
```

Seed data:

| Equipment | Full Gym | Basic Gym | Dumbbells Only | Field Only | Hotel Gym |
|-----------|----------|-----------|----------------|------------|-----------|
| Barbell | ✓ | ✓ | | | |
| Dumbbell | ✓ | ✓ | ✓ | | ✓ |
| Kettlebell | ✓ | ✓ | ✓ | | |
| Trap Bar | ✓ | | | | |
| Cable Machine | ✓ | ✓ | | | |
| Resistance Bands | ✓ | ✓ | ✓ | ✓ | ✓ |
| Medicine Ball | ✓ | ✓ | ✓ | | ✓ |
| Bodyweight | ✓ | ✓ | ✓ | ✓ | ✓ |
| Slide Board | ✓ | | | | |
| Foam Roller | ✓ | ✓ | ✓ | ✓ | ✓ |
| Plyo Box | ✓ | ✓ | | | |
| Sled | ✓ | | | ✓ | |
| Agility Cones | ✓ | ✓ | | ✓ | |
| Bike/Rower | ✓ | | | | |
| Pull-up Bar | ✓ | ✓ | | | ✓ |

New equipment items to add: Plyo Box, Sled, Agility Cones, Bike/Rower, Pull-up Bar.

#### `session_intents` — The primary driver of template structure

```sql
CREATE TABLE session_intents (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,  -- 'Strength', 'Power', 'Speed', 'Conditioning', 'Recovery'
    description TEXT,
    display_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO session_intents (name, description, display_order) VALUES
('Strength', 'Maximal force production against external resistance', 1),
('Power', 'High velocity force production for explosive performance', 2),
('Speed', 'Linear and multidirectional velocity development', 3),
('Conditioning', 'Energy system development and work capacity', 4),
('Recovery', 'Regeneration, mobility, and low-intensity restoration', 5);
```

#### `intent_family_priorities` — Which families belong to which session intent

```sql
CREATE TABLE intent_family_priorities (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    intent_id BIGINT NOT NULL REFERENCES session_intents(id) ON DELETE CASCADE,
    family_id BIGINT NOT NULL REFERENCES exercise_families(id) ON DELETE CASCADE,
    priority INT NOT NULL CHECK (priority BETWEEN 1 AND 100),
    UNIQUE (intent_id, family_id)
);
```

Seed:

| Intent | Families (ordered by priority) |
|--------|-------------------------------|
| Strength | Double Leg Knee Dominant (10), Double Leg Hip Dominant (9), Horizontal Push (8), Horizontal Pull (7), Single Leg Knee Dominant (6), Vertical Push (6), Vertical Pull (6), Core (5), Single Leg Hip Dominant (5), Carry (4) |
| Power | Ballistic (10), Plyometric (9), Double Leg Knee Dominant (8), Double Leg Hip Dominant (7), Sprint (6), Vertical Push (5), Change of Direction (4) |
| Speed | Sprint (10), Change of Direction (9), Plyometric (8), Single Leg Knee Dominant (4), Single Leg Hip Dominant (4) |
| Conditioning | Conditioning (10), Sprint (5), Carry (4), Core (3) |
| Recovery | Core (8), Carry (6), Conditioning (3) — plus mobility/stretching |

#### `templates_v2` — Simplified template model

```sql
CREATE TABLE templates_v2 (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sport_id BIGINT REFERENCES sports(id) ON DELETE SET NULL,
    role_name VARCHAR(100) NOT NULL DEFAULT 'All',  -- denormalized for simplicity
    age_group VARCHAR(50) NOT NULL DEFAULT 'Adult',  -- 'Junior', 'Adult', 'Masters'
    phase VARCHAR(50) NOT NULL CHECK (phase IN ('Off Season', 'Pre Season', 'In Season', 'Transition')),
    frequency INT NOT NULL CHECK (frequency BETWEEN 1 AND 7),
    session_count INT NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (sport_id, role_name, age_group, phase, frequency)
);

CREATE TABLE template_sessions_v2 (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    template_id BIGINT NOT NULL REFERENCES templates_v2(id) ON DELETE CASCADE,
    session_number INT NOT NULL CHECK (session_number >= 1),
    intent_id BIGINT NOT NULL REFERENCES session_intents(id) ON DELETE RESTRICT,
    location VARCHAR(50) NOT NULL DEFAULT 'Gym' CHECK (location IN ('Gym', 'Field', 'Home', 'Travel')),
    duration_minutes INT DEFAULT 60,
    UNIQUE (template_id, session_number)
);

CREATE TABLE session_family_slots (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    session_id BIGINT NOT NULL REFERENCES template_sessions_v2(id) ON DELETE CASCADE,
    family_id BIGINT NOT NULL REFERENCES exercise_families(id) ON DELETE RESTRICT,
    display_order INT NOT NULL,
    min_exercises INT NOT NULL DEFAULT 1,
    max_exercises INT NOT NULL DEFAULT 1,
    UNIQUE (session_id, display_order)
);
```

### 1.3 Index Strategy

```
idx_templates_v2_lookup ON templates_v2(sport_id, role_name, age_group, phase, frequency)
idx_template_sessions_v2_template ON template_sessions_v2(template_id, session_number)
idx_session_family_slots_session ON session_family_slots(session_id, display_order)
idx_exercise_family_mapping_exercise ON exercise_family_mapping(exercise_id)
idx_exercise_family_mapping_family ON exercise_family_mapping(family_id, exercise_id)
idx_intent_family_priorities_lookup ON intent_family_priorities(intent_id, priority DESC)
```

### 1.4 Migration Files to Create

| File | Purpose |
|------|---------|
| `000026_create_exercise_families.up.sql` + `.down.sql` | exercise_families, exercise_family_mapping, seed 15 families |
| `000027_create_equipment_categories.up.sql` + `.down.sql` | equipment_categories, equipment_category_mapping, seed 5 categories + mappings |
| `000028_create_session_intents.up.sql` + `.down.sql` | session_intents, intent_family_priorities, seed 5 intents + family mappings |
| `000029_create_templates_v2.up.sql` + `.down.sql` | templates_v2, template_sessions_v2, session_family_slots |
| `000030_seed_exercise_family_mappings.up.sql` + `.down.sql` | Map all existing exercises to V2.5 families |
| `000031_seed_equipment_extensions.up.sql` + `.down.sql` | Add new equipment items + category mappings |
| `000032_seed_templates_cricket.up.sql` + `.down.sql` | Cricket Fast Bowler, Batter templates |
| `000033_seed_templates_soccer_rugby.up.sql` + `.down.sql` | Soccer Outfield, Rugby Forward templates |

---

## 2. SEED STRATEGY

### 2.1 Exercise Family Mappings (60-80 exercises)

Map every existing exercise to its V2.5 family. This is the critical data migration.

| Exercise (existing) | V2.5 Family | Equipment | Difficulty |
|--------------------|-------------|-----------|------------|
| Barbell Back Squat | Double Leg Knee Dominant | Barbell | Intermediate |
| Front Squat | Double Leg Knee Dominant | Barbell | Intermediate |
| Goblet Squat | Double Leg Knee Dominant | Dumbbell | Beginner |
| Bulgarian Split Squat | Single Leg Knee Dominant | Dumbbell | Intermediate |
| Rear Foot Elevated Split Squat | Single Leg Knee Dominant | Dumbbell | Intermediate |
| Trap Bar Deadlift | Double Leg Hip Dominant | Trap Bar | Intermediate |
| Conventional Deadlift | Double Leg Hip Dominant | Barbell | Advanced |
| Romanian Deadlift | Double Leg Hip Dominant | Barbell | Intermediate |
| Single-Leg RDL | Single Leg Hip Dominant | Dumbbell | Intermediate |
| Kettlebell Swing | Double Leg Hip Dominant | Kettlebell | Beginner |
| Hip Thrust | Double Leg Hip Dominant | Barbell | Intermediate |
| Good Morning | Double Leg Hip Dominant | Barbell | Advanced |
| Nordic Hamstring Curl | Double Leg Hip Dominant | Bodyweight | Intermediate |
| Bench Press | Horizontal Push | Barbell | Intermediate |
| Incline Bench | Horizontal Push | Barbell | Intermediate |
| Dumbbell Bench | Horizontal Push | Dumbbell | Intermediate |
| Push-Up | Horizontal Push | Bodyweight | Beginner |
| Floor Press | Horizontal Push | Barbell | Intermediate |
| Barbell Row | Horizontal Pull | Barbell | Intermediate |
| Dumbbell Row | Horizontal Pull | Dumbbell | Intermediate |
| Cable Row | Horizontal Pull | Cable Machine | Beginner |
| Inverted Row | Horizontal Pull | Bodyweight | Beginner |
| Overhead Press | Vertical Push | Barbell | Intermediate |
| Push Press | Vertical Push | Barbell | Intermediate |
| Push Jerk | Vertical Push | Barbell | Advanced |
| Dumbbell Overhead Press | Vertical Push | Dumbbell | Intermediate |
| Arnold Press | Vertical Push | Dumbbell | Intermediate |
| Pull-Up | Vertical Pull | Bodyweight | Intermediate |
| Chin-Up | Vertical Pull | Bodyweight | Intermediate |
| Lat Pulldown | Vertical Pull | Cable Machine | Beginner |
| Neutral Grip Pulldown | Vertical Pull | Cable Machine | Intermediate |
| Plank | Core | Bodyweight | Beginner |
| Side Plank | Core | Bodyweight | Beginner |
| Pallof Press | Core | Cable Machine | Intermediate |
| Cable Chop | Core | Cable Machine | Intermediate |
| Dead Bug | Core | Bodyweight | Beginner |
| Bird Dog | Core | Bodyweight | Beginner |
| Ab Wheel | Core | Bodyweight | Intermediate |
| Hanging Leg Raise | Core | Bodyweight | Advanced |
| Farmer Walk | Carry | Dumbbell | Beginner |
| Suitcase Carry | Carry | Dumbbell | Intermediate |
| Overhead Carry | Carry | Dumbbell | Intermediate |
| Front Rack Carry | Carry | Kettlebell | Intermediate |
| Depth Jump | Plyometric | Bodyweight | Advanced |
| Box Jump | Plyometric | Bodyweight | Intermediate |
| Broad Jump | Plyometric | Bodyweight | Intermediate |
| Lateral Bound | Plyometric | Bodyweight | Intermediate |
| Pogo Jump | Plyometric | Bodyweight | Intermediate |
| Power Clean | Ballistic | Barbell | Advanced |
| Hang Clean | Ballistic | Barbell | Intermediate |
| Clean Pull | Ballistic | Barbell | Intermediate |
| Medicine Ball Slam | Ballistic | Medicine Ball | Beginner |
| Medicine Ball Chest Pass | Ballistic | Medicine Ball | Beginner |
| MB Rotational Scoop Toss | Ballistic | Medicine Ball | Beginner |
| MB Overhead Backwards Toss | Ballistic | Medicine Ball | Intermediate |
| Trap Bar Jump Squat | Ballistic | Trap Bar | Advanced |
| Barbell Jump Squat | Ballistic | Barbell | Advanced |
| Sled Sprint | Sprint | Sled | Intermediate |
| Resisted Sprint | Sprint | Resistance Bands | Intermediate |
| A-Skip | Sprint | Bodyweight | Beginner |
| B-Skip | Sprint | Bodyweight | Intermediate |
| Acceleration 10m | Sprint | Bodyweight | Intermediate |
| Pro Agility Shuttle | Change of Direction | Bodyweight | Intermediate |
| 5-10-5 Shuttle | Change of Direction | Bodyweight | Intermediate |
| L-Drill | Change of Direction | Bodyweight | Intermediate |
| Tempo Run | Conditioning | Bodyweight | Beginner |
| Interval Run | Conditioning | Bodyweight | Intermediate |
| Bike Intervals | Conditioning | Bike/Rower | Intermediate |
| Rower Intervals | Conditioning | Bike/Rower | Intermediate |
| Sled Push | Conditioning | Sled | Intermediate |
| Sled Pull | Conditioning | Sled | Intermediate |

**Total: ~68 exercises. Within the 60-80 target.**

### 2.2 New Exercises to Create

Add these exercises that don't exist yet but are needed for completeness:

| Exercise | Family | Equipment | Difficulty |
|----------|--------|-----------|------------|
| Front Squat | Double Leg Knee Dominant | Barbell | Intermediate |
| Conventional Deadlift | Double Leg Hip Dominant | Barbell | Advanced |
| Romanian Deadlift | Double Leg Hip Dominant | Barbell | Intermediate |
| Single-Leg RDL | Single Leg Hip Dominant | Dumbbell | Intermediate |
| Hip Thrust | Double Leg Hip Dominant | Barbell | Intermediate |
| Good Morning | Double Leg Hip Dominant | Barbell | Advanced |
| Incline Bench Press | Horizontal Push | Barbell | Intermediate |
| Floor Press | Horizontal Push | Barbell | Intermediate |
| Cable Row | Horizontal Pull | Cable Machine | Beginner |
| Inverted Row | Horizontal Pull | Bodyweight | Beginner |
| Chin-Up | Vertical Pull | Bodyweight | Intermediate |
| Lat Pulldown | Vertical Pull | Cable Machine | Beginner |
| Neutral Grip Pulldown | Vertical Pull | Cable Machine | Intermediate |
| Arnold Press | Vertical Push | Dumbbell | Intermediate |
| Dead Bug | Core | Bodyweight | Beginner |
| Bird Dog | Core | Bodyweight | Beginner |
| Ab Wheel | Core | Bodyweight | Intermediate |
| Hanging Leg Raise | Core | Bodyweight | Advanced |
| Farmer Walk | Carry | Dumbbell | Beginner |
| Suitcase Carry | Carry | Dumbbell | Intermediate |
| Overhead Carry | Carry | Dumbbell | Intermediate |
| Front Rack Carry | Carry | Kettlebell | Intermediate |
| Box Jump | Plyometric | Bodyweight | Intermediate |
| Broad Jump | Plyometric | Bodyweight | Intermediate |
| Pogo Jump | Plyometric | Bodyweight | Intermediate |
| Clean Pull | Ballistic | Barbell | Intermediate |
| Medicine Ball Slam | Ballistic | Medicine Ball | Beginner |
| Sled Sprint | Sprint | Sled | Intermediate |
| Resisted Sprint | Sprint | Resistance Bands | Intermediate |
| B-Skip | Sprint | Bodyweight | Intermediate |
| Acceleration 10m | Sprint | Bodyweight | Intermediate |
| Pro Agility Shuttle | Change of Direction | Bodyweight | Intermediate |
| 5-10-5 Shuttle | Change of Direction | Bodyweight | Intermediate |
| L-Drill | Change of Direction | Bodyweight | Intermediate |
| Tempo Run | Conditioning | Bodyweight | Beginner |
| Interval Run | Conditioning | Bodyweight | Intermediate |
| Bike Intervals | Conditioning | Bike/Rower | Intermediate |
| Rower Intervals | Conditioning | Bike/Rower | Intermediate |
| Sled Push | Conditioning | Sled | Intermediate |
| Sled Pull | Conditioning | Sled | Intermediate |

**~40 new exercises. 10 of these replace existing MockExerciseRepository hardcoded entries (ids 1-11, 86-94).**

### 2.3 Template Seed Data

#### Cricket Fast Bowler — Off Season — 3 Day

```
Session 1 (Strength):
  Slots: Double Leg Knee Dominant, Horizontal Push, Horizontal Pull, Core

Session 2 (Power):
  Slots: Ballistic, Plyometric, Core

Session 3 (Conditioning):
  Slots: Sprint, Change of Direction, Conditioning
```

#### Cricket Fast Bowler — Pre Season — 3 Day

```
Session 1 (Strength):
  Slots: Double Leg Knee Dominant, Horizontal Push, Horizontal Pull, Core

Session 2 (Power):
  Slots: Ballistic, Plyometric, Sprint

Session 3 (Speed + Conditioning):
  Slots: Sprint, Change of Direction, Conditioning
```

#### Cricket Fast Bowler — In Season — 2 Day

```
Session 1 (Power):
  Slots: Ballistic, Plyometric, Core

Session 2 (Strength):
  Slots: Single Leg Knee Dominant, Horizontal Push, Horizontal Pull
```

#### Cricket Fast Bowler — In Season — 3 Day

```
Session 1 (Power):
  Slots: Ballistic, Plyometric, Core

Session 2 (Strength):
  Slots: Double Leg Knee Dominant, Horizontal Push, Horizontal Pull, Core

Session 3 (Recovery):
  Slots: Core, Carry, Conditioning
```

Repeat pattern for Batter, Soccer Outfield, Rugby Forward with different family slotting (Batter: more rotational work, Soccer: more single leg and plyometric, Rugby: more strength and carries).

---

## 3. SERVICE ARCHITECTURE

### 3.1 Module Structure

```
src/
├── v25/
│   ├── __init__.py
│   ├── app.py                           # FastAPI app for V2.5 endpoints
│   │
│   ├── models/                          # Pydantic models
│   │   ├── __init__.py
│   │   ├── athlete.py                   # AthleteProfile
│   │   ├── context.py                   # TrainingContext (phase, freq, equipment)
│   │   ├── template.py                  # Template, TemplateSession, FamilySlot
│   │   ├── exercise.py                  # Exercise, ExerciseFamily
│   │   └── substitution.py             # SubstitutionRequest, SubstitutionResult
│   │
│   ├── repositories/                    # Data access layer
│   │   ├── __init__.py
│   │   ├── exercise_repository.py       # ExerciseRepositoryV2
│   │   ├── template_repository.py       # TemplateRepositoryV2
│   │   ├── family_repository.py         # ExerciseFamilyRepository
│   │   └── equipment_repository.py      # EquipmentRepositoryV2
│   │
│   ├── services/                        # Business logic
│   │   ├── __init__.py
│   │   ├── template_resolver.py         # Maps 5 inputs → template
│   │   ├── exercise_selector.py         # Maps family + equipment → specific exercise
│   │   ├── substitution_engine.py       # Family-anchored substitution (V2.5 version)
│   │   └── program_populator.py         # Populates template slots with exercises
│   │
│   ├── data/                            # Static seed data
│   │   ├── __init__.py
│   │   ├── exercises.py                 # Full 68-exercise library with metadata
│   │   ├── families.py                  # 15 families
│   │   ├── templates.py                 # Template definitions
│   │   └── equipment_categories.py      # 5 categories + mappings
│   │
│   └── tests/                           # Tests
│       ├── __init__.py
│       ├── test_exercise_families.py
│       ├── test_substitution_engine.py
│       ├── test_template_resolver.py
│       ├── test_exercise_selector.py
│       └── test_e2e_v25.py
```

### 3.2 Key Data Flows

```
Flow 1: Template Resolution

[Sport, Role, Age, Phase, Frequency]
        ↓
TemplateRepository.lookup(sport, role, age, phase, frequency)
        ↓
Template object with N sessions, each with M family slots
        ↓
Return to caller

---

Flow 2: Program Population

Template (with sessions → family slots)
        ↓
For each slot → ExerciseSelector.select(family, equipment, difficulty)
        ↓
ExerciseSelector.exercises_by_family(family_id)
        ↓
Filter by equipment_category match
        ↓
Filter by difficulty ≤ athlete_level
        ↓
Return ranked by: equipment match > difficulty match > coaching_tags
        ↓
Populated program draft

---

Flow 3: Substitution

[Slot with current exercise, new equipment, new difficulty]
        ↓
SubstitutionEngine.substitute(family_id, current_exercise_id, context)
        ↓
Get all exercises in same family
        ↓
Rank by: equipment match > difficulty similarity > tag overlap
        ↓
Return ordered substitution list
```

### 3.3 Dependency Graph

```
No circular dependencies.

template_resolver.py → template_repository.py, sports table
exercise_selector.py → exercise_family_mapping, exercises, equipment_categories
substitution_engine.py → exercise_family_mapping, exercises, equipment_categories
program_populator.py → template_resolver, exercise_selector (both)
```

All services are stateless. Repository layer handles all DB interaction.

---

## 4. FILE-BY-FILE IMPLEMENTATION PLAN

### PHASE A: Foundation Data (Files 1-6)

| # | File | Purpose | Est. Lines |
|---|------|---------|-----------|
| 1 | `migrations/000026_create_exercise_families.up.sql` | exercise_families table + seed 15 families | 40 |
| 2 | `migrations/000027_create_equipment_categories.up.sql` | equipment_categories + equipment_category_mapping + seed | 80 |
| 3 | `migrations/000028_create_session_intents.up.sql` | session_intents + intent_family_priorities + seed | 60 |
| 4 | `migrations/000029_create_templates_v2.up.sql` | templates_v2 + template_sessions_v2 + session_family_slots + indices | 80 |
| 5 | `migrations/000030_seed_exercise_family_mappings.up.sql` | Map all ~68 exercises to V2.5 families | 100 |
| 6 | `migrations/000031_seed_equipment_extensions.up.sql` | Add new equipment (Plyo Box, Sled, etc.) + category mappings | 60 |

**Phase A Total: ~420 lines SQL. Effort: 1-2 days.**

### PHASE B: Data Layer (Files 7-12)

| # | File | Purpose | Est. Lines |
|---|------|---------|-----------|
| 7 | `src/v25/__init__.py` | Package init | 5 |
| 8 | `src/v25/models/__init__.py` | Models package init | 5 |
| 9 | `src/v25/models/athlete.py` | AthleteProfile pydantic model | 20 |
| 10 | `src/v25/models/context.py` | TrainingContext pydantic model | 30 |
| 11 | `src/v25/models/template.py` | Template, TemplateSession, FamilySlot pydantic models | 50 |
| 12 | `src/v25/models/exercise.py` | Exercise, ExerciseFamily, EquipmentCategory pydantic models | 40 |
| 13 | `src/v25/data/__init__.py` | Data package init | 5 |
| 14 | `src/v25/data/families.py` | 15 families with descriptions | 60 |
| 15 | `src/v25/data/exercises.py` | Full 68-exercise library with family/equip/difficulty/tags | 350 |
| 16 | `src/v25/data/equipment_categories.py` | 5 categories + mapping data | 60 |
| 17 | `src/v25/data/templates.py` | Template definitions (Cricket, Soccer, Rugby) | 300 |

**Phase B Total: ~925 lines Python. Effort: 2-3 days.**

### PHASE C: Repository Layer (Files 18-21)

| # | File | Purpose | Est. Lines |
|---|------|---------|-----------|
| 18 | `src/v25/repositories/__init__.py` | Repositories package init | 5 |
| 19 | `src/v25/repositories/exercise_repository.py` | ExerciseRepositoryV2 (get by family, by equipment, by difficulty) | 120 |
| 20 | `src/v25/repositories/template_repository.py` | TemplateRepositoryV2 (lookup by 5 inputs) | 100 |
| 21 | `src/v25/repositories/family_repository.py` | ExerciseFamilyRepository (list families, get intent mappings) | 60 |
| 22 | `src/v25/repositories/equipment_repository.py` | EquipmentRepositoryV2 (get equipment available in category) | 50 |

**Phase C Total: ~335 lines Python. Effort: 1-2 days.**

### PHASE D: Service Layer (Files 23-26)

| # | File | Purpose | Est. Lines |
|---|------|---------|-----------|
| 23 | `src/v25/services/__init__.py` | Services package init | 5 |
| 24 | `src/v25/services/template_resolver.py` | 5-input → template resolution | 80 |
| 25 | `src/v25/services/exercise_selector.py` | Family + equipment → specific exercise selection | 120 |
| 26 | `src/v25/services/substitution_engine.py` | Family-anchored substitution with ranking | 150 |
| 27 | `src/v25/services/program_populator.py` | Populate template → draft program | 100 |

**Phase D Total: ~455 lines Python. Effort: 2-3 days.**

### PHASE E: API Layer (Files 28-29)

| # | File | Purpose | Est. Lines |
|---|------|---------|-----------|
| 28 | `src/v25/app.py` | FastAPI app with V2.5 endpoints | 200 |
| 29 | `src/v25/tests/` | All tests | 500 |

**Phase E Total: ~700 lines Python. Effort: 2-3 days.**

### PHASE F: Template Seeds (Files 30-33)

| # | File | Purpose | Est. Lines |
|---|------|---------|-----------|
| 30 | `migrations/000032_seed_templates_cricket.up.sql` | Fast Bowler + Batter templates (3 phases × 2-3 frequencies) | 200 |
| 31 | `migrations/000033_seed_templates_soccer_rugby.up.sql` | Soccer Outfield + Rugby Forward templates | 200 |

**Phase F Total: ~400 lines SQL. Effort: 1 day.**

---

## 5. ESTIMATED EFFORT

| Phase | Files | Lines | Days |
|-------|-------|-------|------|
| A: Foundation Data (migrations) | 6 | ~420 SQL | 1-2 |
| B: Data Layer + Models | 11 | ~925 Python | 2-3 |
| C: Repository Layer | 5 | ~335 Python | 1-2 |
| D: Service Layer | 5 | ~455 Python | 2-3 |
| E: API + Tests | 2 | ~700 Python | 2-3 |
| F: Template Seed Data | 2 | ~400 SQL | 1 |
| **Total** | **31** | **~3,235** | **9-14** |

Reality check: 9-14 days of focused work. Add 30% for debugging, edge cases, integration testing = **12-18 days to first working version**.

---

## 6. RISKS

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **Family mapping disagreements** | High | Medium | Use consensus patterns. Family assignments can be remapped later. |
| **Missing exercises for a slot** | Medium | High | Ensure each family has 3-5 exercises minimum. Add placeholders if needed. |
| **Equipment category gaps** | Medium | Low | Start with 5 broad categories. Refine as coaches give feedback. |
| **Template structure wrong for coaches** | High | Medium | Templates are data, not code. Easy to change seeded templates in migrations. |
| **V1/V2 conflict in shared DB** | Low | High | V2.5 uses separate tables. V1 code won't touch new tables. No conflict. |
| **36 existing exercises in DB + 40 new = 76** | Medium | Low | 76 is within 60-80 range. If exercises exceed 80, drop lowest-priority ones. |
| **Existing MockExerciseRepository not updated** | Medium | Medium | V2.5 service layer doesn't use MockExerciseRepository. It has its own data source. |
| **Coach finds 5 session intents insufficient** | Medium | Medium | Intents are data, not code. Add mappings. But wait for coach feedback first. |

---

## 7. RECOMMENDED BUILD ORDER

### Week 1: Foundation (Days 1-3)

1. Create 5 migration files (000026-000030)
2. Run migrations against test DB
3. Write data layer: families.py, exercises.py, equipment_categories.py
4. Write model layer: athlete.py, context.py, template.py, exercise.py

**Checkpoint:** Can load all 15 families, 68 exercises, 5 equipment categories into memory.

### Week 2: Core Logic (Days 4-7)

5. Write repository layer (exercise_repo, template_repo, family_repo, equipment_repo)
6. Write template_resolver.py — verify it returns correct template for each of the 5 inputs
7. Write exercise_selector.py — verify it selects correct exercise for family + equipment combo
8. Write substitution_engine.py — verify it returns same-family substitutions ranked by equipment match

**Checkpoint:** Can resolve a template from 5 inputs and populate its first session with exercises.

### Week 3: Integration (Days 8-11)

9. Write program_populator.py — full pipeline: template → sessions → slots → exercises
10. Write app.py — FastAPI endpoints
11. Write all tests
12. Create template seed migrations (000032-000033)

**Checkpoint:** Full E2E flow works. API returns populated draft program.

### Week 4: Polish (Days 12-14)

13. Integration test against full pipeline
14. Fix edge cases (empty slots, missing equipment, unknown sport/role)
15. Test Cricket Fast Bowler, Batter, Soccer Outfield, Rugby Forward all produce valid drafts
16. Verify 3-minute target: measure API response time for template resolution + population

**Checkpoint:** All 4 athlete types produce complete draft programs. E2E tests pass.

---

## 8. TEST STRATEGY

### Unit Tests

| Test | Count | What it covers |
|------|-------|---------------|
| `test_family_lookup` | 5 | Each of 15 families returns correct exercises |
| `test_equipment_filter` | 5 | Equipment category correctly filters exercises |
| `test_difficulty_filter` | 5 | Difficulty cap correctly filters exercises |
| `test_template_resolution` | 12 | 4 sports × 3 phases = 12 template lookups succeed |
| `test_session_intent_families` | 5 | Each intent returns correct family priorities |
| `test_substitution_same_family` | 10 | Substitutions stay within family |
| `test_substitution_ranking` | 5 | Preferred equipment ranked above non-preferred |
| `test_program_population` | 4 | All sessions filled with valid exercises |

### Integration Tests

| Test | What it verifies |
|------|-----------------|
| `test_e2e_v25_fast_bowler` | Fast Bowler Off-Season 3-Day → complete draft |
| `test_e2e_v25_batter` | Batter Pre-Season 4-Day → complete draft |
| `test_e2e_v25_soccer` | Soccer Outfield In-Season 2-Day → complete draft |
| `test_e2e_v25_rugby` | Rugby Forward Off-Season 3-Day → complete draft |
| `test_substitution_chain` | Replace Back Squat → Front Squat → Goblet Squat within family |

### Acceptance Criteria

1. **5 inputs → populated program**: Sport, Role, Age, Phase, Frequency → draft program with exercises in every slot
2. **All substitutions stay in family**: SubstitutionEngine never returns exercises from a different family
3. **Equipment-aware**: Hotel Gym template never selects Barbell-only exercises
4. **Difficulty-aware**: Beginner template never selects Advanced exercises
5. **Session intent correct**: Strength session never defaults to Sprint drills

---

## 9. EXISTING CODE TOUCHPOINTS

### What V2.5 Touches

| Existing File | Change Required |
|--------------|----------------|
| `src/program_builder.py` | None (V1 engine, will be replaced by V2.5 endpoints) |
| `src/recommendation_engine.py` | None (V1 engine, MockExerciseRepository not used by V2.5) |
| `src/exercise_substitution_engine.py` | None (V1 engine, V2.5 has its own substitution) |
| `src/session_generator.py` | None (V1 engine, not used by V2.5) |
| `src/demand_scoring_engine.py` | None (V2 engine, runs alongside V2.5) |

### What V2.5 Does Not Touch

- No V1 tables are altered
- No V1 services are modified
- No existing imports are changed
- No existing tests break (V2.5 uses entirely new endpoints)

### Cleanup after V2.5 Launches

After V2.5 is working and coach-validated:
1. Mark V1 endpoints as deprecated
2. Remove V1 template system after migration period
3. Remove V2 ontology tables if unused
4. Remove MockExerciseRepository hardcoded data

None of this happens in Phase 1.

---

## 10. KEY DESIGN DECISIONS (FROZEN)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Template model | Session Intent → Family Slots | Coaches think in session types first, movement patterns second |
| Substitution anchor | Exercise Family | Hard constraint: never substitute across families |
| Equipment model | 5 categories, not per-item | Simple enough for MVP, extensible later |
| Difficulty model | 4-level (Beginner/Intermediate/Advanced/Elite) | Maps to existing DB schema, matches coach language |
| Session intents | 5 (Strength/Power/Speed/Conditioning/Recovery) | Covers 95% of S&C sessions. No methodology-specific intents. |
| Variants | NOT an entity. Separate exercises. | Keeps library flat. Variants = substitution paths. |
| Progression | NOT an entity. Coach chooses from preset paths. | Avoids complex progression engine. Start simple. |
| V1 compatibility | Parallel tables | No breaking changes. V2.5 runs alongside V1. |

---

## 11. NON-NEGOTIABLE RULES

1. **No AI. No ML.** All selection is deterministic rule-based matching.
2. **No new entities beyond the 7 core** (Athlete, Context, Template, Session, Intent, Family, Exercise).
3. **No variants table.** Different implements = different exercises.
4. **No readiness engine.** No injury engine. No competition calendar. No periodization engine.
5. **Coach can override anything.** Every exercise in the draft is swappable via the substitution engine.
6. **3-minute target or it fails.** If the pipeline takes longer than 180 seconds to produce a draft, it needs optimization.
7. **Family is the hard constraint.** Substitution engine must NEVER return exercises from a different family.
8. **Data before code.** Seed data is more important than algorithm elegance. Templates are data, not code.
9. **Test with real scenarios.** Every test must be based on a real coaching scenario, not abstract theory.
10. **If any implementation requires a concept from the graveyard list: STOP. Document. Do not build.**

---

## 12. IMPLEMENTATION CHECKLIST

### Pre-Flight
- [ ] All architecture decisions in this document agreed
- [ ] No remaining architecture questions
- [ ] Build order accepted
- [ ] 31 files understood

### Phase A Complete
- [ ] 6 migration files written and tested
- [ ] 15 families seeded
- [ ] 5 equipment categories seeded with mappings
- [ ] 5 session intents seeded with family priorities
- [ ] All existing exercises mapped to families
- [ ] V2 template/session/family-slots tables created

### Phase B Complete
- [ ] All Pydantic models written
- [ ] Exercise library data file complete (68 exercises)
- [ ] Family definitions data file complete
- [ ] Equipment categories data file complete
- [ ] Template definitions data file complete

### Phase C Complete
- [ ] ExerciseRepositoryV2 queries working
- [ ] TemplateRepositoryV2 lookups working
- [ ] FamilyRepositoryV2 queries working
- [ ] EquipmentRepositoryV2 queries working

### Phase D Complete
- [ ] TemplateResolver returns correct template for all 5 inputs
- [ ] ExerciseSelector returns correct exercise for family + equipment
- [ ] SubstitutionEngine returns same-family substitutions only
- [ ] ProgramPopulator produces complete draft program

### Phase E Complete
- [ ] FastAPI endpoints responding
- [ ] GET /api/v2/templates?{sport,role,age,phase,frequency}
- [ ] POST /api/v2/programs/populate
- [ ] POST /api/v2/substitutions
- [ ] All unit tests passing
- [ ] All integration tests passing

### Phase F Complete
- [ ] Cricket Fast Bowler templates seeded (3 phases × 2-3 frequencies)
- [ ] Cricket Batter templates seeded
- [ ] Soccer Outfield templates seeded
- [ ] Rugby Forward templates seeded

### Go/No-Go
- [ ] All 4 test pipelines produce valid drafts
- [ ] No V1 tables or code modified
- [ ] 3-minute target verified
- [ ] Coach review scheduled
