# Forge Exercise Recommendation Engine Architecture

This document outlines the software architecture, S&C scoring logic, database queries, and caching mechanisms of the **Forge Exercise Recommendation Engine**.

---

## 1. System Pipeline Architecture

The engine accepts athlete properties and compiles them into a structured, highly specific program:

```
[Input Request]
      │
      ▼
 1. [Read Movement Template]  ──> Find template matching (Sport, Role, Goal)
      │
      ▼
 2. [Load Template Slots]     ──> Fetch Slot Types and Progression rules
      │
      ▼
 3. [Filter Exercise Pool]    ──> Validate Equipment & Athlete Difficulty Cap
      │
      ▼
 4. [Score & Rank Pool]       ──> Calculate S&C Specificity & Tag Bonuses
      │
      ▼
[Output Payload]              ──> Return JSON structure (Cached or Hashed key)
```

---

## 2. Dynamic S&C Ranking Algorithm

Each candidate exercise for a template slot is graded using a multi-dimensional sports science scoring formula:

$$Score = (Relevance \times W_{relevance}) + (Specificity \times W_{specificity}) + (Transfer \times W_{transfer}) + (TagMatchCount \times W_{tag}) + (MechanicsBonus)$$

### Scoring Components & Weights

| Component | DB Source | Scale | Weight | Max Value | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Relevance** | `exercise_physical_qualities.relevance_score` | 1 to 10 | 40% (x4.0) | **40.0** | Relevance of exercise to target physical quality (e.g. RFD). |
| **Specificity** | `exercise_sport_mapping.specificity_rating` | 1 to 10 | 30% (x3.0) | **30.0** | Specificity rating of exercise to target sport (e.g. Cricket). |
| **Transfer Index** | `exercise_sport_mapping.transfer_index` | 0.0 to 1.0 | 20% (x20.0) | **20.0** | Bondarchuk transfer index (transfer of training efficiency). |
| **Tag Matches** | `exercise_tags` | Count | +2.0 per tag | **Dynamic** | Bonus points for matching tags required by the slot. |
| **Mechanics** | `exercises.mechanics_type` | Flat | +5.0 points | **5.0** | Bonus if `Compound` lift matches a `Primary` slot. |

---

## 3. Core PostgreSQL Queries

### A. Template Lookup (With Fallback)
Attempts to resolve a highly specific template for a sport role. If none exists, it falls back to a general template matching the goal:
```sql
-- Query 1: Direct Match
SELECT mt.id, mt.name, mt.training_goal, s.name as sport_name
FROM movement_templates mt
JOIN sports s ON mt.sport_id = s.id
WHERE s.name ILIKE :sport 
  AND mt.athlete_role ILIKE :role 
  AND mt.training_goal ILIKE :goal
LIMIT 1;

-- Query 2: Fallback (Goal-Only, Sport-Agnostic)
SELECT mt.id, mt.name, mt.training_goal, s.name as sport_name
FROM movement_templates mt
LEFT JOIN sports s ON mt.sport_id = s.id
WHERE (s.name ILIKE :sport OR s.id IS NULL) 
  AND mt.training_goal ILIKE :goal
ORDER BY s.id DESC NULLS LAST
LIMIT 1;
```

### B. Exercise Filtering and Scoring Query
Runs for each template slot to pull candidates. It filters by athlete level, checks that *all* mandatory equipment is in the available array, and ranks using the S&C scoring formula:
```sql
SELECT 
    e.id, 
    e.name, 
    e.description, 
    e.difficulty_level, 
    e.mechanics_type, 
    e.force_type,
    (
        COALESCE(epq.relevance_score, 0) * 0.40 * 10.0 +  -- relevance (scale 1-10 -> 0-40)
        COALESCE(esm.specificity_rating, 0) * 0.30 * 10.0 + -- specificity (scale 1-10 -> 0-30)
        COALESCE(esm.transfer_index, 0.0) * 20.0 +        -- transfer index (scale 0-1 -> 0-20)
        (CASE WHEN e.mechanics_type = 'Compound' AND ts.slot_type = 'Primary' THEN 5.0 ELSE 0.0 END) + -- mechanics alignment
        (SELECT COUNT(*) * 2.0 FROM exercise_tags et JOIN slot_requirements sr ON et.tag_id = sr.tag_id WHERE et.exercise_id = e.id AND sr.slot_id = ts.id) -- tag match bonus
    )::numeric(5,2) as recommendation_score
FROM exercises e
JOIN exercise_movement_patterns emp ON e.id = emp.exercise_id
JOIN template_slots ts ON ts.id = :slot_id
JOIN slot_requirements sr ON sr.slot_id = ts.id
LEFT JOIN exercise_physical_qualities epq ON e.id = epq.exercise_id AND epq.physical_quality_id = sr.physical_quality_id
LEFT JOIN exercise_sport_mapping esm ON e.id = esm.exercise_id AND esm.sport_id = (SELECT sport_id FROM movement_templates WHERE id = ts.template_id)
WHERE 
    -- 1. Match movement pattern requirement
    (sr.movement_pattern_id IS NULL OR emp.movement_pattern_id = sr.movement_pattern_id)
    -- 2. Validate athlete level cap
    AND (
        CASE e.difficulty_level
            WHEN 'Beginner' THEN 1
            WHEN 'Intermediate' THEN 2
            WHEN 'Advanced' THEN 3
            WHEN 'Elite' THEN 4
        END <= 
        CASE :difficulty_cap
            WHEN 'Beginner' THEN 1
            WHEN 'Intermediate' THEN 2
            WHEN 'Advanced' THEN 3
            WHEN 'Elite' THEN 4
        END
    )
    -- 3. Filter by available equipment (Bodyweight is implicitly allowed)
    -- This enforces that NO mandatory equipment for this exercise lies outside the available list.
    AND NOT EXISTS (
        SELECT 1 
        FROM exercise_equipment ee
        JOIN equipment eq ON ee.equipment_id = eq.id
        WHERE ee.exercise_id = e.id 
          AND ee.is_required = TRUE
          AND eq.name <> 'Bodyweight'
          AND eq.name <> ALL(:available_equipment)
    )
ORDER BY recommendation_score DESC;
```

---

## 4. Caching Strategy

The recommendation engine implements a **dual-layer caching architecture** to deliver sub-millisecond response times:

### A. Cache Key Generation
Input payloads are normalized and hashed using SHA-256 to generate unique cache signatures:
- **Normalized Key Format**: `sport:role:goal:sorted_equipment_array:difficulty_cap`
- **Example Hashed Key**: `a3d6f1...f9a2`

### B. Cache Layers
1. **L1 Local Memory (FastAPI Context)**:
   - Implemented using a thread-safe in-memory cache map with an `asyncio.Lock`.
   - Used for quick serving in single-container microservices.
2. **L2 Shared Cache (Redis)**:
   - For multi-instance deployments, the generated SHA-256 keys are stored in a centralized Redis cluster.
   - TTL is set to **300 seconds (5 minutes)**. This provides high consistency while relieving database workloads under peak request volumes.

### C. Invalidation Policy
- **TTL Expiration**: Automatic eviction after 5 minutes.
- **Event-Driven Flushing**: Triggered by changes to Lookup Tables, Templates, or Exercises. S&C administrators can trigger clear commands via:
  - `POST /api/v1/cache/clear` (flushes the entire cache namespace).
