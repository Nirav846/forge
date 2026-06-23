# Exercise Substitution Engine — Architecture & Design

## 1. Overview

The substitution engine allows coaches to swap exercises within a staged program while preserving movement intent, progression envelope, and athlete safety gates. It supports real-time preview (via `preview-swap`) and coach override persistence.

## 2. Core Components

### 2.1 Exercise Classification (`exercise_classification.py`)

Each exercise is classified into one of:
- **Olympic Lift** — Power Clean, Push Jerk, Split Jerk, Hang Clean, etc.
- **Ballistic** — Loaded jumps (Trap Bar Jump Squat, Barbell Jump Squat)
- **Medicine Ball** — Rotational throws, slams, scoop tosses
- **Plyometric** — Unilateral bounds, hops, pogo jumps
- **Isometric** — Planks, Pallof press variations
- **Sprint Drill** — Acceleration, max velocity, change-of-direction drills
- **Core Stability** — Anti-rotation and anti-extension holds
- **Max Strength** — Heavy compound lifts (Back Squat, RFESS)
- **Accessory** — Isolation exercises (Nordic Hamstring Curl)

Primary adaptation and force vector are derived automatically:
- `determine_primary_adaptation()` — Power, Strength, Rotational Power, Stability, Elastic
- `determine_force_vector()` — Vertical, Horizontal, Rotational

### 2.2 Exercise Equivalencies (`exercise_equivalencies.py`)

Direct 1-to-1 and 1-to-many mappings with sport science rationale:

| Source | Target(s) | Score | Rationale |
|---|---|---|---|
| Trap Bar Jump Squat | Barbell Jump Squat | 8 | Same force-velocity profile |
| Power Clean | Hang Clean, Clean Pull, Mid-Thigh Pull | 7-9 | Shared catch-less pull mechanics |
| Push Jerk | Push Press, Split Jerk | 8 | Same dip-drive mechanics |
| Split Jerk | Push Jerk, Push Press | 7 | Overhead receiving pattern |
| Med Ball Rotational Scoop Toss | Rotational Chest Pass, Overhead Backwards Toss | 7 | Trunk rotational velocity |
| Barbell Back Squat | RFESS, Overhead Squat | 5-6 | Quad-dominant push |
| Trap Bar Deadlift | Kettlebell Swing, Clean Pull | 6-7 | Hip-dominant hinge |
| Barbell Bench Press | Dumbbell Bench, Incline DB Press | 7 | Horizontal press pattern |
| Barbell Row | Dumbbell Row, Cable Row | 7 | Horizontal pull pattern |
| Overhead Squat | Snatch Balance, Front Squat | 6-7 | Overhead stability |

### 2.3 Substitution Engine (`exercise_substitution_engine.py`)

**Flow:**
1. Fetch current exercise metadata from full catalog
2. Fetch all slot-matched candidates via `repo.get_ranked_exercises()` (already filtered by difficulty, equipment, training age)
3. Build `SubstituteExercise` objects with matched reasons
4. Rank by `equivalency_score`, `same_category`, movement pattern, force type, mechanics, `recommendation_score`

**Athlete gates applied by the repository layer:**
- `training_age_months` — minimum experience filter
- `difficulty_cap` — Beginner/Intermediate/Advanced/Elite
- `equipment` — available gear match

**Output format (`SubstituteExercise`):**
```
exercise_id, name, difficulty_level, mechanics_type, force_type,
exercise_class, primary_adaptation, force_vector, movement_pattern,
equivalency_score, recommendation_score, same_category, match_reasons
```

## 3. API Endpoints

### 3.1 `POST /api/v1/programs/preview-swap`

**Request:**
```json
{
  "stage_id": "uuid-string",
  "slot_id": 201,
  "target_exercise_id": 86
}
```

**Response fields:**
- `unchanged` (bool) — True when `exercise_class` and `force_type` match between current and target
- `current_exercise_name` / `new_exercise_name`
- `reason` — classification-based rationale
- `weeks` — 4-week progression for the target exercise using `calculate_reps_and_intensity()`

**Unchanged determination:** Uses `exercise_class + force_type` rather than `movement_pattern` for more stable matching (avoids name-based fragility).

### 3.2 `POST /api/v1/programs/override`

**Request:**
```json
{
  "stage_id": "uuid-string",
  "slot_id": 201,
  "original_exercise_id": 1,
  "selected_exercise_id": 86,
  "override_reason": "Athlete prefers clean variations",
  "overridden_by": "Coach Smith"
}
```

**Persistence:** Two-tier — in-memory `_coach_overrides` dict during staging, `program_coach_overrides` table on confirm.

## 4. Progression Preservation

`calculate_reps_and_intensity()` in `program_builder.py` uses `exercise_class` metadata (not exercise names):

| Class | Week 1 | Week 2 | Week 3 | Week 4 |
|---|---|---|---|---|
| Olympic Lift | 3x5 @ 75% RPE 7 | 4x5 @ 80% RPE 8 | 4x3 @ 85% RPE 9 | 2x5 @ 60% RPE 6 |
| Ballistic | 4x3 @ 80% 1RM | 4x3 @ 85% 1RM | 3x3 @ 90% 1RM | 2x3 @ 65% 1RM |
| Medicine Ball | 4x5 @ 75% RPE 7 | 4x5 @ 80% RPE 8 | 4x3 @ 85% RPE 9 | 2x5 @ 60% RPE 6 |
| Plyometric | 4x4 BW | 4x4 BW | 4x4 BW | 4x4 BW |
| Isometric | 4x30s | 4x40s | 4x50s | 4x60s |
| Sprint Drill | 6x20m | 6x20m | 6x20m | 6x20m |
| Core Stability | 4x30s | 4x40s | 4x50s | 4x60s |
| Max Strength | 4x3 @ 85% RPE 9 | 4x3 @ 87% RPE 9 | 3x2 @ 90% RPE 10 | 2x2 @ 70% RPE 7 |
| Accessory | 3x8 @ 75% RPE 7 | 4x8 @ 80% RPE 8 | 4x6 @ 85% RPE 9 | 2x8 @ 60% RPE 6 |

Rest seconds: explosive classes (plyometric, sprint drill, medicine ball, accessory, isometric, core stability) get 90s; others get 120s on week 3.

## 5. Data Model (SQL Migration 000016)

### `exercises` columns added
- `exercise_class VARCHAR(50)` — classification for progression
- `primary_adaptation VARCHAR(50)` — training effect
- `force_vector VARCHAR(50)` — direction of force

### `exercise_equivalencies` table
- `id`, `source_exercise_id`, `target_exercise_id`, `equivalency_score DECIMAL(3,1)`, `reason TEXT`
- Unique constraint on `(source_exercise_id, target_exercise_id)`

### `program_coach_overrides` table
- `id`, `program_id`, `stage_id`, `slot_id`, `original_exercise_id`, `selected_exercise_id`, `override_reason`, `overridden_by`, `override_timestamp`
- Unique constraint on `(program_id, slot_id)` for one override per slot per program
- Foreign keys to `programs` and `program_session_exercises`

## 6. Cricket-Specific Examples

| Athlete | Slot | Current Exercise | Target Exercise | Unchanged? | Progression |
|---|---|---|---|---|---|
| Fast Bowler (Power) | 201 | Trap Bar Jump Squat | Power Clean | No (Ballistic→Olympic Lift) | Velocity→RPE-based |
| Fast Bowler (Power) | 201 | Trap Bar Jump Squat | Barbell Jump Squat | Yes (both Ballistic+Push) | Same progression |
| Batter (Power) | 401 | Trap Bar Deadlift | Kettlebell Swing | No (Max Strength→Ballistic) | RPE→Velocity-based |
| Spinner | 301 | Med Ball Rotation Scoop Toss | Overhead Backwards Toss | Yes (both MB+Rotation) | Same progression |
| Fast Bowler | 201 | Power Clean | Hang Clean | Yes (both Olympic Lift+Pull) | Same progression |

## 7. Key Design Decisions

1. **Standalone classification module** — avoids circular imports between recommendation_engine and exercise_substitution_engine
2. **Ballistic class separate from Plyometric** — loaded jumps use velocity-based %1RM progression; unloaded jumps use bodyweight
3. **preview-swap uses exercise_class + force_type** for unchanged detection (not movement_pattern) — more stable
4. **Two-tier override persistence** — in-memory during staging for fast iteration, DB on confirm for audit trail
5. **`_get_full_catalog()` caches** after first call — avoids repeated async calls to repo for the same session
6. **`get_ranked_exercises` outputs include `slots`, `required_equipment`, `minimum_training_age_months`** — enables substitution engine to perform re-filtering without accessing raw exercise definitions
