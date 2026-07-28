# FORGE Implementation Specification V1

> The single document from which a developer can build FORGE.
> No coaching content. No new rules. No new blueprints. No new exercises. No new conditioning protocols.
> Only consolidation from 8 input documents into implementation-ready form.

---

## SECTION 1: SYSTEM BOUNDARY

### What FORGE Does

FORGE takes an athlete profile and generates a single training session (or a week of sessions) that meets the FORGE standard — a standard reverse-engineered from 58 elite programs across 7 sports.

**Core functions:**
- Select the correct training blueprint for an athlete profile
- Fill each blueprint slot with an exercise matching the athlete's level, equipment, and history
- Apply substitution rules when the first-choice exercise is unavailable
- Select and adjust a conditioning protocol to match the athlete's conditioning goal
- Validate the generated session against 100 non-negotiable laws + 50 conditioning laws + 12-point credibility check
- Render the session as a coach-readable output

### What FORGE Does NOT Do

| Does Not Do | Rationale |
|-------------|-----------|
| No AI / machine learning | Deterministic rules only. Lookup tables + conditional logic. |
| No progression engine | Progression is coach-managed between sessions. FORGE generates individual sessions. |
| No sport-specific engines | All 7 sports are covered by the same 14 blueprints and 15 families. Sport is a selection constraint, not an engine. |
| No 1RM calculation | Load is specified as RPE/RIR bands, not percentages. Coach fills in load. |
| No periodization logic | Block planning is coach input. FORGE generates within a block. |
| No data persistence | Session storage, athlete history, and tracking are outside scope. |
| No auto-regulation | Coach provides current level and injury status each session request. |
| No warm-up generation | Warm-up structure is prescribed by the blueprint; specific exercises are coach-provided. |
| No cool-down generation | Cool-down is a time-bounded block (5 min minimum). Content is coach-choice. |
| No formula-based conditioning generation | Conditioning is selected from curated protocol library only. |
| No injury-specific protocols | Injury modifies substitution within existing families. No separate injury engine. |
| No output beyond a single session | Returns one session at a time. The coach requests the next session. |

### Hard Scope Limits

| Limit | Value |
|-------|-------|
| Max session duration | 90 minutes |
| Max strength exercises per session | 3 |
| Max total family slots per session | 6 (plus warm-up, core, conditioning, cool-down) |
| Max plyometric ground contacts | 30 per session |
| Max conditioning block duration (high-intensity) | 45 minutes |
| Max conditioning block duration (low-intensity) | 60 minutes |
| Min warm-up duration | 10 minutes |
| Min cool-down duration | 5 minutes |
| Athlete levels | 3 (Beginner, Intermediate, Advanced) |
| Exercise difficulty range | L1-L5 (Beginner ≤ L2, Intermediate ≤ L3, Advanced ≤ L5) |
| Equipment profiles | 4 (Field Only, Basic Gym, Commercial Gym, Elite Facility) |
| Blueprints | 14 (exactly as catalogued — no new blueprints) |
| Exercise families | 15 (exactly as catalogued — no new families) |
| Exercise catalog | 191 exercises (exactly as catalogued) |
| Conditioning protocols | 100 (exactly as catalogued) |
| Conditioning energy systems | 10 (exactly as defined) |

### Maximum MVP Scope

The MVP includes:
1. A blueprint selector (decision tree: athlete profile → 1 of 14 blueprints)
2. A slot resolver (blueprint → ordered list of mandatory + optional family slots)
3. An exercise selector (slot + athlete level + equipment → one exercise from the 191-exercise catalog)
4. A substitution engine (when first-choice exercise fails validation)
5. A conditioning selector (decision tree → protocol family → A-tier protocol → level adjustment)
6. A session validator (100 laws + 50 conditioning laws + 12-point credibility check)
7. A session renderer (formatted coach-readable output)

The MVP does NOT include:
- A database or persistence layer
- A web UI or API server
- A progression tracker
- A warm-up/cool-down exercise generator
- A multi-session week builder
- A block planner

---

## SECTION 2: DATASETS

### Dataset 1: Exercise Library

| Property | Value |
|----------|-------|
| **Count** | 191 exercises |
| **Source** | FORGE_COACHING_REFERENCE_DATABASE.md Part 2 |

**Fields:**

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `id` | string | e.g. "DLKD-001" | Unique exercise identifier (family-prefixed sequential) |
| `name` | string | e.g. "Barbell Back Squat" | Exercise name |
| `family` | string | DLKD, DLHD, SLKD, SLHD, HPush, HPull, VPush, VPull, Plyo, Ball, Sprint, Rot, Carry, Core, Acc | Primary family (one of 15) |
| `secondary_family` | string or null | Same as family values, or null | Optional secondary family for cross-listing |
| `objective` | string | STR, POW, HYP, COND, MOB, STAB | Primary training objective |
| `difficulty` | int | 1-5 | L1 (Beginner) through L5 (Elite) |
| `equipment` | string | Bodyweight, Barbell, DB, KB, Band, Cable, Machine, Box, Med Ball, Sled, Cones, Hurdles, Rings, etc. | Key equipment required |
| `unilateral` | boolean | true/false | U (true) or B (false) — unilateral or bilateral |
| `explosive` | boolean | true/false | Explosive intent required |
| `isometric` | boolean | true/false | Has isometric component |
| `rotational` | boolean | true/false | Has rotational component |
| `progression` | string or null | Exercise name | Direct progression (next level within family) |
| `regression` | string or null | Exercise name | Direct regression (previous level within family) |

**Relationships:**
- `family` → `ExerciseFamily.id` (many-to-one)
- `progression` → `Exercise.id` (self-referential, nullable)
- `regression` → `Exercise.id` (self-referential, nullable)

### Dataset 2: Exercise Families

| Property | Value |
|----------|-------|
| **Count** | 15 families |
| **Source** | FORGE_COACHING_REFERENCE_DATABASE.md Part 1 |

**Fields:**

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `id` | string | DLKD, DLHD, SLKD, SLHD, HPush, HPull, VPush, VPull, Plyo, Ball, Sprint, Rot, Carry, Core, Acc | Unique family code |
| `name` | string | e.g. "Double Leg Knee Dominant" | Full family name |
| `definition` | string | Free text | What qualifies for this family |
| `non_negotiable_in` | string | e.g. "90% of programs" | Frequency of appearance in corpus |
| `default_slot` | string | early, mid, late, last | Where this family typically goes in session |
| `selection_priorities` | list[object] | Ordered list of {exercise_id, priority, notes} | Priority-ordered exercise list per Section 2.2 of the Rulebook |

**Relationships:**
- `id` → `Exercise.family` (one-to-many)
- `selection_priorities` → `Exercise.id` (ordered many-to-many)

### Dataset 3: Blueprints

| Property | Value |
|----------|-------|
| **Count** | 14 blueprints |
| **Source** | FORGE_BLUEPRINT_CATALOG_V1.md + FORGE_BLUEPRINT_SELECTION_GUIDE_V1.md |

**Fields:**

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `id` | int | 1-14 | Blueprint number |
| `name` | string | e.g. "Full Body Strength" | Blueprint name |
| `purpose` | string | Free text | What this blueprint accomplishes |
| `typical_athlete` | string | Free text | Who uses this most |
| `best_training_age` | string | e.g. "0-3 years" | Training age range |
| `best_season_phase` | string | e.g. "Off-season" | Season phase best fit |
| `best_frequency` | string | e.g. "3-4 sessions/week" | Sessions per week |
| `contraindications` | string | Free text | When NOT to use |
| `typical_outcomes` | string | Free text | Expected results |
| `progression_path` | string | Blueprint name | What blueprint to progress to |
| `regression_path` | string | Blueprint name | What blueprint to regress from |
| `mandatory_families` | list[string] | Family codes | Must be present every session |
| `optional_families` | list[string] | Family codes | Rotated in as needed |
| `slot_order` | list[string] | Family codes | Priority sequence for exercise families |
| `typical_duration` | string | e.g. "60-75 min" | Session duration |
| `min_session_composition` | list[object] | {family, count, mandatory} | Minimum session composition rules (Section 3.2 of Rulebook) |

**Relationships:**
- `mandatory_families`, `optional_families`, `slot_order`, `min_session_composition` → `ExerciseFamily.id`

### Dataset 4: Conditioning Protocols

| Property | Value |
|----------|-------|
| **Count** | 100 protocols |
| **Source** | FORGE_CONDITIONING_LIBRARY_V1.md |

**Fields:**

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `id` | string | e.g. "AC-001" | Protocol identifier (system-prefixed) |
| `name` | string | e.g. "Long Slow Distance — Base Builder" | Protocol name |
| `objective` | string | Free text | What this protocol accomplishes |
| `system` | string | 1 of 10 energy systems | Primary energy system |
| `level` | string | Beginner, Intermediate, Elite, All levels | Athlete level suitability |
| `environment` | string | Field, Track, Treadmill, Indoor, Limited Space, Gym | Required environment |
| `duration` | string | e.g. "20-30 min" | Session duration |
| `work` | string | Free text | Work interval prescription |
| `rest` | string | Free text | Rest interval prescription (or "None" for continuous) |
| `sets` | string | e.g. "3-4" | Number of sets |
| `total_volume` | string | e.g. "2-5 km" | Total volume |
| `fatigue_score` | int | 1-5 | Fatigue score (1=recovery, 5=lactate tolerance) |
| `progression` | string | Free text | How to progress this protocol |
| `regression` | string | Free text | How to regress this protocol |
| `tier` | string | A, B, C | Ranking tier (from Conditioning Intelligence V2) |

**Relationships:**
- `system` → Energy system (1 of 10)
- `tier` is used for default selection (A tier first, B tier if unavailable, C tier niche only)

### Dataset 5: Substitution Matrix

| Property | Value |
|----------|-------|
| **Count** | 15 family ladders + 13 cross-family substitutions |
| **Source** | FORGE_SUBSTITUTION_MATRIX_V1.md |

**Fields:**

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `family` | string | Family code | The family this ladder is for |
| `ladder` | list[object] | {level, double_leg, single_leg, notes} | Ordered difficulty ladder (L1-L5), may have bilateral/unilateral tracks |
| `equipment_fallback` | string | Free text | Instructions when equipment is missing |
| `injury_notes` | list[object] | {injury, modification, avoid, preferred_substitution} | Injury-specific guidance |

**Cross-family substitution fields:**

| Field | Type | Values | Description |
|-------|------|--------|-------------|
| `missing_family` | string | Family code | Family that cannot be trained |
| `best_substitute` | string | Family code | Best replacement family |
| `why` | string | Free text | Justification for substitution |

**Relationships:**
- `family` → `ExerciseFamily.id`
- `missing_family` → `ExerciseFamily.id`
- `best_substitute` → `ExerciseFamily.id`

---

## SECTION 3: GENERATION PIPELINE

All generation follows exactly 8 steps. Deterministic. No branching outside the specified paths.

```
INPUT: athlete_profile { sport, training_age, injury_status, season_phase, goal,
                         equipment_profile, athlete_level, injury_history }
```

### Step 1: Select Blueprint

```
FUNCTION select_blueprint(athlete_profile) → blueprint:

    IF athlete.injury_status == "active" OR athlete.goal == "return_to_sport":
        RETURN blueprint_12  # Return to Sport (Foundation)

    SWITCH athlete.season_phase:
        CASE "off_season":
            IF athlete.training_age < 2:
                blueprint_shortlist = [blueprint_07, blueprint_14]  # Youth Foundation or Mixed Modal
            ELSE IF athlete.goal == "mass":
                blueprint_shortlist = [blueprint_11]  # Hypertrophy
            ELSE IF athlete.sport IN ["rugby", "american_football"]:
                blueprint_shortlist = [blueprint_09]  # Rugby Off-Season
            ELSE IF athlete.sport IN ["tennis", "badminton", "basketball"]:
                blueprint_shortlist = [blueprint_08]  # Court Sport AD
            ELSE IF athlete.goal == "speed":
                blueprint_shortlist = [blueprint_02]  # Strength + Power
            ELSE:
                blueprint_shortlist = [blueprint_01]  # Full Body Strength

        CASE "pre_season":
            IF athlete.goal == "conditioning":
                blueprint_shortlist = [blueprint_03]  # Strength + Conditioning
            ELSE IF athlete.goal == "power_peak":
                blueprint_shortlist = [blueprint_04]  # Power + Speed
            ELSE IF athlete.goal == "speed":
                blueprint_shortlist = [blueprint_10]  # Sprint Development
            ELSE:
                blueprint_shortlist = [blueprint_01]  # Full Body Strength

        CASE "in_season":
            IF athlete.goal == "power_maintenance":
                blueprint_shortlist = [blueprint_06]  # Power Maintenance
            ELSE IF athlete.training_age < 2:
                blueprint_shortlist = [blueprint_07]  # Youth Foundation (2x/week)
            ELSE:
                blueprint_shortlist = [blueprint_01]  # Full Body Strength (2x/week)

        CASE "transition" OR "between_blocks":
            IF athlete.fatigue_level == "high":
                blueprint_shortlist = [blueprint_13]  # Deload / Active Recovery
            ELSE:
                # Re-evaluate by phase
                RETURN select_blueprint(athlete with season_phase from current phase)

        DEFAULT:
            blueprint_shortlist = [blueprint_01]  # Full Body Strength (safest default)

    // If multiple blueprints remain, narrow by sport type
    IF len(blueprint_shortlist) > 1:
        IF athlete.sport IN ["rugby", "american_football"] AND "Rugby Off-Season" IN blueprint_shortlist:
            blueprint_shortlist = ["Rugby Off-Season"]
        ELSE IF athlete.sport IN ["tennis", "badminton", "basketball"] AND "Court Sport AD" IN blueprint_shortlist:
            blueprint_shortlist = ["Court Sport AD"]
        ELSE:
            blueprint_shortlist = [blueprint_shortlist[0]]  # First match wins

    RETURN blueprint_shortlist[0]
```

### Step 2: Determine Athlete Level

```
FUNCTION determine_level(training_age, technique_consistency, strength_base) → level:

    IF training_age < 1 OR technique_consistency < 0.8:
        RETURN "Beginner"
        // Max difficulty: L2. Max load: 60-70% 1RM. RPE 6-7.

    IF training_age >= 1 AND training_age < 3
       AND technique_consistency >= 0.8
       AND no_movement_red_flags:
        RETURN "Intermediate"
        // Max difficulty: L3. Max load: 75-85% 1RM.

    IF training_age >= 3
       AND technique_consistency >= 0.8
       AND strength_base_established:  // ≥1.5x BW squat M, ≥1.2x BW squat F
        RETURN "Advanced"
        // Max difficulty: L5. Max load: 85-95% 1RM.

    // Fallback: safest level
    RETURN "Beginner"

// Special cases:
// - Athlete returning from 4+ week break: regress one level for first 2 weeks
// - Youth U16: never above Intermediate regardless of training age
```

### Step 3: Determine Equipment Profile

```
FUNCTION get_equipment_profile(available_equipment) → profile:

    // Available equipment is a list of equipment items the athlete has access to
    // Returns one of 4 fixed profiles

    IF "barbell" NOT IN available_equipment
       AND "dumbbell" NOT IN available_equipment:
        RETURN "Field Only"
        // Equipment: bodyweight, bands, med balls, cones, field space

    IF "barbell" IN available_equipment
       AND "rack" IN available_equipment
       AND "dumbbell" IN available_equipment
       AND "cable" IN available_equipment
       AND "sled" IN available_equipment
       AND "specialty_bar" IN available_equipment:
        RETURN "Elite Facility"

    IF "barbell" IN available_equipment
       AND "rack" IN available_equipment
       AND "bench" IN available_equipment
       AND "dumbbell" IN available_equipment
       AND "cable" IN available_equipment:
        RETURN "Commercial Gym"

    // Default for anything with basic barbell/dumbbell access
    RETURN "Basic Gym"
    // Equipment: barbell, squat rack, flat bench, dumbbells (up to 40kg), cable station
```

### Step 4: Resolve Blueprint Slot Order

```
FUNCTION resolve_slots(blueprint, athlete_level) → ordered_slots:

    slots = []

    // Start with mandatory families
    FOR EACH family IN blueprint.mandatory_families:
        slots.append(family)

    // Add optional families if total slots < 6
    FOR EACH family IN blueprint.optional_families:
        IF len(slots) >= 6:
            BREAK
        IF family NOT IN slots:
            slots.append(family)

    // Sort slots by the blueprint's slot_order priority
    sorted_slots = sort(slots, by=blueprint.slot_order.index(family))

    // Apply blueprint-specific composition rules (Section 3.2 of Rulebook):
    // - Core is always last slot
    // - Power is always before strength
    // - Conditioning is always last main block
    sorted_slots = enforce_session_flow_rules(sorted_slots)

    RETURN sorted_slots
```

### Step 5: Select Exercise Per Slot

```
FUNCTION select_exercise(slot_family, athlete_level, equipment_profile,
                         recent_exercises, injury_history) → exercise:

    // Get the family's priority-ordered exercise list
    candidates = get_selection_priorities(slot_family)

    FOR EACH exercise IN candidates:

        // Filter 1: Difficulty match
        max_diff = get_max_difficulty(athlete_level)  // Beginner→L2, Intermed→L3, Adv→L5
        IF exercise.difficulty > max_diff:
            CONTINUE

        // Filter 2: Equipment match
        IF NOT equipment_available(exercise.equipment, equipment_profile):
            CONTINUE

        // Filter 3: Injury check
        IF injury_history.conflicts_with(exercise):
            CONTINUE

        // Selection tiebreaker: prefer recently-used exercises first
        // (within last 4 weeks with good technique)
        IF exercise IN recent_exercises AND recent_exercises[exercise].technique_score >= 0.8:
            RETURN exercise  // Prefer known exercise

        // If not recently used, check rotation: prefer least recently used
        IF exercise NOT IN recent_exercises:
            RETURN exercise  // New exercise is acceptable

    // Fallback: substitute within same family at lower difficulty
    candidates_lower = [e FOR e IN candidates WHERE e.difficulty <= max_diff - 1]
    FOR EACH exercise IN candidates_lower:
        IF equipment_available(exercise.equipment, equipment_profile):
            RETURN exercise

    // Ultimate fallback: trigger substitution rules (Step 5b)
    RETURN trigger_substitution(slot_family, athlete_level, equipment_profile)
```

### Step 5b: Substitution

```
FUNCTION substitute_exercise(family, athlete_level, equipment_profile,
                             injury_info, recent_exercises) → exercise:

    // Priority 1: Same family, next available
    priority_list = get_selection_priorities(family)
    FOR EACH exercise IN priority_list:
        IF equipment_available(exercise.equipment, equipment_profile)
           AND exercise.difficulty <= get_max_difficulty(athlete_level)
           AND NOT injury_info.conflicts_with(exercise):
            RETURN exercise

    // Priority 2: Same intent category, different family
    intent = get_intent_category(family)
    substitute_families = intent_substitution_map[intent]
    FOR EACH sub_family IN substitute_families:
        sub_priority = get_selection_priorities(sub_family)
        FOR EACH exercise IN sub_priority:
            IF equipment_available(exercise.equipment, equipment_profile)
               AND exercise.difficulty <= get_max_difficulty(athlete_level)
               AND NOT injury_info.conflicts_with(exercise):
                RETURN exercise

    // Priority 3: Same equipment, any family
    FOR EACH exercise IN all_exercises:
        IF equipment_available(exercise.equipment, equipment_profile)
           AND exercise.difficulty <= get_max_difficulty(athlete_level)
           AND NOT injury_info.conflicts_with(exercise):
            RETURN exercise

    // Priority 4: Emergency fallback: flag as coaching gap
    RETURN null  // Slot is skipped, flagged as coaching gap
```

### Step 6: Validate Session

```
FUNCTION validate_session(session) → (is_valid, score, failures):

    score = 0
    failures = []

    // Run 12-point credibility check (Section 9.1 of Rulebook)
    checks = [
        check_posterior_chain_present(session),
        check_push_pull_balanced(session),
        check_core_included(session),
        check_appropriate_difficulty(session),
        check_equipment_available(session),
        check_session_flow_correct(session),
        check_power_before_fatigue(session),
        check_recovery_reasonable(session),
        check_knee_hip_balance(session),
        check_no_red_flags(session),
        check_volume_within_limits(session),
        check_rotation_respects_history(session)
    ]

    FOR EACH check IN checks:
        IF check.passed:
            score += 1
        ELSE:
            failures.append(check.name)
            IF check.severity == "critical":
                RETURN (false, score, failures)  // Immediate fail for critical violations

    RETURN (score >= 8, score, failures)
```

### Step 7: Assign Load, Sets, Reps, Rest

```
FUNCTION assign_training_variables(session, blueprint, athlete_level) → session_with_variables:

    FOR EACH block IN session.blocks:

        SWITCH block.type:
            CASE "power":
                block.sets = clamp(2, 5, blueprint.power_sets_default)
                block.reps = "3-6"  // Power rep range
                block.rest = "2-5 min"  // Full recovery
                block.load_intent = "maximal velocity, 30-60% 1RM for loaded, bodyweight for plyos"

            CASE "strength_primary":
                block.sets = clamp(3, 5, blueprint.strength_sets_default)
                block.rep_range = get_family_rep_range(block.family)
                // Family-specific ranges: DLKD/DLHD 3-5, HPush/HPull 4-8, etc.
                block.rest = "2-4 min"  // 3+ min for >85% 1RM
                block.rir = "1-3"  // Reps in reserve

            CASE "strength_secondary":
                block.sets = clamp(2, 4, 3)
                block.rep_range = "6-12"
                block.rest = "2-3 min"
                block.rir = "2-3"

            CASE "accessory":
                block.sets = clamp(2, 3, 3)
                block.rep_range = "10-20"
                block.rest = "60-90s"
                block.rir = "2-3"

            CASE "core":
                block.sets = clamp(2, 4, 3)
                block.rep_range = "8-20"
                block.rest = "60s"
                // Core is time-under-tension based: planks in seconds, not reps

            CASE "conditioning":
                // Conditioning variables are part of the protocol, not calculated here
                block.protocol = select_conditioning(session, athlete_level)

    // Apply athlete level modifiers
    IF athlete_level == "Beginner":
        FOR EACH block IN session.blocks:
            block.sets = max(block.sets - 1, 2)  // Reduce sets
            block.load = "60-70% 1RM or RPE 6-7"

    IF athlete_level == "Advanced":
        // No reduction, may add complexity

    RETURN session
```

### Step 8: Generate Final Session

```
FUNCTION render_session(session) → output:

    output = ""

    output += f"SESSION: {session.blueprint.name}\n"
    output += f"PURPOSE: {session.blueprint.purpose}\n"
    output += f"DURATION: {session.blueprint.typical_duration}\n"
    output += f"ATHLETE: {session.athlete_level}\n\n"

    output += "BLOCK 1: PREPARATION (15-25 min)\n"
    output += "  Warm-up: Movement prep specific to main work\n"
    output += "  Activation: Glute + scapular activation\n\n"

    // Main work blocks
    output += "BLOCK 2: MAIN WORK\n"
    FOR EACH block IN session.main_blocks:
        output += f"  {block.type}: {block.exercise.name}\n"
        output += f"    Sets: {block.sets} | Reps: {block.rep_range} | Rest: {block.rest}\n"
        output += f"    Load: {block.load_intent or f'{block.load}'}\n"

    output += "\nBLOCK 3: CLOSING (10-15 min)\n"
    IF session.conditioning:
        output += f"  Conditioning: {session.conditioning.protocol.name}\n"
        output += f"    {session.conditioning.protocol.work_summary}\n"
    output += "  Cool-down: 5 min minimum\n"

    output += "\nCOACHING NOTES:\n"
    FOR EACH note IN session.coaching_notes:
        output += f"  - {note}\n"

    // Validation score
    output += f"\nCREDIBILITY SCORE: {session.validation_score}/10\n"
    IF session.validation_failures:
        output += "  Warnings:\n"
        FOR EACH f IN session.validation_failures:
            output += f"    - {f}\n"

    RETURN output
```

### Conditioning Selection Pipeline

```
FUNCTION select_conditioning(session, athlete_level, goal, environment, time_available) → protocol:

    // Step 1: Decision tree (Part 1 of Conditioning Intelligence V2)
    protocol_family = conditioning_decision_tree(
        training_age=athlete_level_to_training_age(athlete_level),
        goal=goal,
        environment=environment,
        time_available=time_available
    )

    // Step 2: Select A Tier protocol within family
    candidates = get_protocols_by_family(protocol_family)
    a_tier = [p FOR p IN candidates WHERE p.tier == "A"]
    selected = a_tier[0] IF a_tier ELSE candidates[0]  // Fallback to first candidate

    // Step 3: Level adjustment
    adjusted = apply_level_adjustment(selected, athlete_level)

    // Step 4: Validate against 50 COND-LAWs
    violations = validate_conditioning_laws(adjusted, session, athlete_level)
    IF violations:
        substitute = find_legal_substitute(protocol_family, adjusted, violations)
        selected = substitute IF substitute ELSE adjusted
        // If no substitute, the conditioning block is skipped (flagged)

    RETURN selected
```

---

## SECTION 4: OBJECT MODELS

```python
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class FamilyCode(str, Enum):
    DLKD = "DLKD"
    DLHD = "DLHD"
    SLKD = "SLKD"
    SLHD = "SLHD"
    HPUSH = "HPush"
    HPULL = "HPull"
    VPUSH = "VPush"
    VPULL = "VPull"
    PLYO = "Plyo"
    BALL = "Ball"
    SPRINT = "Sprint"
    ROT = "Rot"
    CARRY = "Carry"
    CORE = "Core"
    ACC = "Acc"


class Objective(str, Enum):
    STRENGTH = "STR"
    POWER = "POW"
    HYPERTROPHY = "HYP"
    CONDITIONING = "COND"
    MOBILITY = "MOB"
    STABILITY = "STAB"


class AthleteLevel(str, Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"


class EquipmentProfile(str, Enum):
    FIELD_ONLY = "Field Only"
    BASIC_GYM = "Basic Gym"
    COMMERCIAL_GYM = "Commercial Gym"
    ELITE_FACILITY = "Elite Facility"


class SeasonPhase(str, Enum):
    OFF_SEASON = "off_season"
    PRE_SEASON = "pre_season"
    IN_SEASON = "in_season"
    TRANSITION = "transition"


class BlueprintName(str, Enum):
    FULL_BODY_STRENGTH = "Full Body Strength"
    STRENGTH_POWER = "Strength + Power"
    STRENGTH_CONDITIONING = "Strength + Conditioning"
    POWER_SPEED = "Power + Speed"
    UPPER_LOWER_SPLIT = "Upper / Lower Split"
    POWER_MAINTENANCE = "Power Maintenance"
    YOUTH_FOUNDATION = "Youth Foundation (U14-U20)"
    COURT_SPORT_AD = "Court Sport Athletic Development"
    RUGBY_OFF_SEASON = "Rugby Off-Season"
    SPRINT_DEVELOPMENT = "Sprint Development"
    HYPERTROPHY = "Hypertrophy / Mass Accrual"
    RETURN_TO_SPORT = "Return to Sport (Foundation)"
    DELOAD = "Deload / Active Recovery"
    MIXED_MODAL = "Mixed Modal (GPP)"


# ─── Exercise ────────────────────────────────────────────────────────

@dataclass
class Exercise:
    id: str                          # e.g. "DLKD-001"
    name: str                        # e.g. "Barbell Back Squat"
    family: FamilyCode
    secondary_family: Optional[FamilyCode]
    objective: Objective
    difficulty: int                  # 1-5
    equipment: list[str]             # e.g. ["Barbell", "Rack"]
    unilateral: bool
    explosive: bool
    isometric: bool
    rotational: bool
    progression: Optional[str]       # Exercise.id
    regression: Optional[str]        # Exercise.id


# ─── Exercise Family ─────────────────────────────────────────────────

@dataclass
class ExerciseFamily:
    id: FamilyCode
    name: str                        # "Double Leg Knee Dominant"
    definition: str
    non_negotiable_in: str           # "90% of programs"
    default_slot: str                # "early", "mid", "late", "last"
    selection_priorities: list[tuple[int, str, str]]
    # [(priority, exercise_id, notes), ...]
    # Source: Rulebook Section 2.2


# ─── Blueprint ───────────────────────────────────────────────────────

@dataclass
class Blueprint:
    id: int                          # 1-14
    name: BlueprintName
    purpose: str
    typical_athlete: str
    best_training_age: str
    best_season_phase: list[SeasonPhase]
    best_frequency: str
    contraindications: str
    typical_outcomes: str
    progression_path: Optional[BlueprintName]
    regression_path: Optional[BlueprintName]
    mandatory_families: list[FamilyCode]
    optional_families: list[FamilyCode]
    slot_order: list[FamilyCode]
    typical_duration: str
    min_session_composition: list[dict]
    # [{family: FamilyCode, mandatory: bool, count: int, notes: str}]


# ─── Conditioning Protocol ───────────────────────────────────────────

@dataclass
class ConditioningProtocol:
    id: str                          # "AC-001"
    name: str                        # "Long Slow Distance — Base Builder"
    objective: str
    system: str                      # 1 of 10 energy systems
    level: str                       # "Beginner", "Intermediate", "Elite", "All levels"
    environment: list[str]           # ["Field", "Track", ...]
    duration: str                    # "20-30 min"
    work_description: str
    rest: str                        # "None", "27s passive", "2 min walk", etc.
    sets: str                        # "3-4", "1", etc.
    total_volume: str                # "2-5 km"
    fatigue_score: int               # 1-5
    progression: str
    regression: str
    tier: str                        # "A", "B", "C"
    work_rest_ratio: Optional[str]   # "1:3", etc.

    # Level-adjusted variants (L1-L5 progression chain)
    level_variants: dict[int, dict] = field(default_factory=dict)
    # {1: {sets: "...", reps: "...", rest: "...", volume: "..."}, ...}


# ─── Session Block ───────────────────────────────────────────────────

@dataclass
class SessionBlock:
    type: str                        # "power", "strength_primary", "strength_secondary",
                                     # "accessory", "core", "conditioning", "warmup", "cooldown"
    family: Optional[FamilyCode]
    exercise: Optional[Exercise]
    sets: int
    rep_range: str                   # e.g. "3-5", "8-12", or "30s" for planks
    rest: str                        # "2-3 min", "60s"
    load: Optional[str]              # "60-70% 1RM", "RPE 7", "maximal intent", or null
    rir: Optional[str]               # "1-3", null for power/conditioning
    coaching_cue: Optional[str]      # "Heel drive", "Brace before descent"


# ─── Session ─────────────────────────────────────────────────────────

@dataclass
class Session:
    blueprint: Blueprint
    athlete_level: AthleteLevel
    blocks: list[SessionBlock]
    conditioning: Optional[ConditioningProtocol]
    warmup_duration: int = 20        # minutes
    cooldown_duration: int = 5       # minutes
    validation_score: int = 0        # 0-10
    validation_failures: list[str] = field(default_factory=list)
    coaching_notes: list[str] = field(default_factory=list)


# ─── Athlete Profile ─────────────────────────────────────────────────

@dataclass
class AthleteProfile:
    sport: str
    training_age_years: float
    season_phase: SeasonPhase
    goal: str                        # "general_strength", "mass", "power_peak",
                                     # "speed", "conditioning", "return_to_sport",
                                     # "power_maintenance", "recovery"
    equipment_profile: EquipmentProfile
    athlete_level: AthleteLevel
    technique_consistency: float     # 0.0-1.0
    injury_status: str               # "active", "cleared", "none"
    injury_history: list[str]        # ["low_back", "acl_left", ...]
    fatigue_level: str               # "normal", "high"
    weeks_since_break: int           # 0 if no break
    recent_exercises: dict[str, dict] = field(default_factory=dict)
    # {exercise_id: {last_used_date, technique_score, sessions_count}}


# ─── Generated Program ───────────────────────────────────────────────

@dataclass
class GeneratedProgram:
    session: Session
    athlete: AthleteProfile
    generation_timestamp: str
    version: str = "FORGE V1"

    def is_valid(self) -> bool:
        return self.session.validation_score >= 8
```

---

## SECTION 5: GENERATOR RULES

All rules from the coaching documents converted to IF/THEN form. Organized by domain.

### Blueprint Selection Rules

```
IF injury_status == "active"                             THEN return Blueprint_12 (Return to Sport)
IF season_phase == "off_season" AND training_age < 2     THEN select from [Youth Foundation, Mixed Modal]
IF season_phase == "off_season" AND goal == "mass"       THEN select Blueprint_11 (Hypertrophy)
IF season_phase == "off_season" AND sport IN contact    THEN select Blueprint_09 (Rugby Off-Season)
IF season_phase == "off_season" AND sport IN court       THEN select Blueprint_08 (Court Sport AD)
IF season_phase == "off_season" AND goal == "speed"      THEN select Blueprint_02 (Strength + Power)
IF season_phase == "pre_season" AND goal == "conditioning" THEN select Blueprint_03 (Strength + Conditioning)
IF season_phase == "pre_season" AND goal == "power_peak" THEN select Blueprint_04 (Power + Speed)
IF season_phase == "in_season" AND goal == "maintenance" THEN select Blueprint_06 (Power Maintenance)
IF season_phase == "in_season" AND training_age < 2      THEN select Blueprint_07 (Youth 2x/week)
IF season_phase == "transition" AND fatigue == "high"    THEN select Blueprint_13 (Deload)
```

### Athlete Level Rules

```
IF training_age < 1                                       THEN level = Beginner
IF training_age >= 1 AND training_age < 3 AND technique >= 0.8 THEN level = Intermediate
IF training_age >= 3 AND technique >= 0.8 AND strength_base_met THEN level = Advanced
IF athlete_returning_after_4_weeks_off                     THEN level = level - 1 (regress one level)
IF age < 16                                                THEN max_level = Intermediate
IF technique_consistency < 0.8                             THEN level = Beginner
```

### Exercise Selection Rules

```
IF exercise.difficulty > athlete_max_difficulty           THEN exclude exercise
IF exercise.equipment NOT IN available_equipment          THEN exclude exercise
IF exercise IN injury_conflicts                           THEN exclude exercise
IF exercise == recently_performed_with_good_technique     THEN prefer exercise (tiebreaker)
IF tie_remains                                            THEN select least_recently_used
IF no_exercise_in_family_matches                          THEN trigger_same_family_substitution
```

### Equipment Profile Rules

```
IF no_barbell AND no_dumbbell                             THEN profile = "Field Only"
IF barbell AND rack AND bench AND dumbbell                THEN profile = "Basic Gym"
IF barbell AND rack AND bench AND dumbbell AND cable     THEN profile = "Commercial Gym"
IF all_equipment_available                                THEN profile = "Elite Facility"
```

### Session Flow Rules

```
IF power_AND_strength_in_session                          THEN power_before_strength
IF core_in_session                                        THEN core_is_last_training_block
IF conditioning_in_session                                THEN conditioning_is_final_element
IF warmup_present                                         THEN warmup_before_any_loaded_work
IF activation_present                                     THEN activation_before_power
IF power_exercise                                         THEN never_superset_power
IF bp_4(Power+Speed) OR bp_10(SprintDev)                  THEN Sprint/COD_may_be_in_activation
```

### Push/Pull Balance Rules

```
IF HPush_in_session                                       THEN HPull_must_also_be_in_session
IF VPush_in_week                                         THEN VPull_in_same_week
total_pull_volume >= total_push_volume                    (across training week)
horizontal_push <= horizontal_pull                        (per session and per week)
```

### Knee/Hip Balance Rules

```
IF full_body_session                                      THEN one_knee_dominant_AND_one_hip_dominant
IF sprint_emphasis_week                                   THEN hip:up_to_2:1_over_knee
IF court_emphasis_week                                    THEN knee:up_to_2:1_over_hip
posterior_chain_volume >= anterior_chain_volume           (across training week)
```

### Core Rules

```
anti-extension                     IN every session
anti-rotation                      >= 2x/week
anti-lateral_flexion               >= 1x/week
flexion_work                       optional_only (crunches not core training)
core                               always_last
```

### Rotation Rules

```
IF exercise_age_4_to_6_weeks                               THEN rotate_1_to_2_exercises
IF athlete_reports_joint_pain                              THEN rotate_immediately
IF athlete_misses_reps_3_consecutive_sessions               THEN rotate
IF no_progress_for_4_weeks                                 THEN rotate
IF exercise_is_progressing                                 THEN keep
IF exercise_is_less_than_2_weeks_old                       THEN keep_minimum_4_weeks
IF exercise_is_primary_compound_and_progressing            THEN keep_up_to_8_weeks
IF tapered_exercise_for_competition                        THEN keep_through_taper
IF progression_scheduled_AND_rotation_scheduled            THEN progression_overrides_rotation
IF exercise_rotated_out                                    THEN minimum_8_weeks_before_return
```

### Substitution Rules

```
IF no_exercise_in_family                                   THEN substitute_same_family_first
IF no_same_family_available                                THEN substitute_same_intent
IF no_same_intent_available                                THEN substitute_same_equipment
IF no_substitution_possible                                THEN skip_slot_and_flag
IF injury_present                                          THEN use_injury_substitution_table
IF equipment_lost                                          THEN use_equipment_fallback
```

### Load Assignment Rules

```
IF block_type == "power"                                   THEN sets=2-5, reps=2-6, rest=2-5min
IF block_type == "strength_primary"                        THEN sets=3-5, reps=3-8, rest=2-4min
IF block_type == "strength_secondary"                      THEN sets=2-4, reps=6-12, rest=2-3min
IF block_type == "accessory"                               THEN sets=2-3, reps=10-20, rest=60-90s
IF block_type == "core"                                    THEN sets=2-4, reps=8-20s/rep, rest=60s
IF athlete_level == "Beginner"                             THEN all_sets--, load=60-70% 1RM
```

### Conditioning Selection Rules

```
IF training_age < 1                                       THEN no_lactate_tolerance
IF training_age < 1                                       THEN RSA_start_at_every_40s
IF goal == "recovery"                                     THEN select_recovery_family
IF goal == "aerobic_capacity"                             THEN select_aerobic_capacity_family
IF goal == "aerobic_power"                                THEN select_aerobic_power_family
IF goal == "extensive_tempo"                              THEN select_extensive_tempo_family
IF goal == "intensive_tempo"                              THEN intensive_tempo_advanced_only
IF goal == "rsa"                                          THEN select_rsa_family
IF goal == "alactic_speed"                                THEN alactic_speed_fresh_CNS
IF goal == "lactate_tolerance"                            THEN lactate_tolerance_advanced_only
IF goal == "power_maintenance"                            THEN power_maintenance_every_block
IF a_tier_available_in_family                             THEN select_a_tier_protocol
IF no_a_tier_available                                    THEN select_b_tier_protocol
IF c_tier                                                  THEN advanced_only_with_specific_goal
```

### Conditioning Session Rules

```
IF session_includes_conditioning                           THEN one_primary_energy_system_targeted
IF conditioning_present                                   THEN after_all_strength_and_power
IF alactic_speed                                          THEN before_any_fatiguing_work
IF rsa_volume_prescribed                                  THEN 95-100%_effort
IF recovery_conditioning                                  THEN RPE <= 3
IF lactate_tolerance_session                              THEN 48h_before_next_speed_session
IF in_season                                              THEN conditioning_volume_50%_off_season
IF high_intensity_conditioning                            THEN max_2_sessions_per_week
IF conditioning_RPE > 9_first_execution                   THEN regress_one_level_next_session
```

### Progression Rules (for coach reference, not engine-generated)

```
IF strength_progression                                   THEN add_reps_first_then_add_load
IF power_progression                                      THEN increase_velocity_first
IF accessory_progression                                  THEN reps->sets->load->exercise_change
IF 4_weeks_completed                                      THEN deload_week
IF primary_lift_RPE > 9_for_2_sessions                    THEN deload
IF velocity_loss > 20%_on_warmup                          THEN deload
```

### Athlete Safety Overrides

```
IF new_pain_reported                                      THEN stop_exercise_substitute
IF 3_consecutive_sessions_missed                          THEN regress_one_level
IF 4_weeks_no_training                                    THEN return_to_sport_protocol
IF rule_conflict                                          THEN safety_over_performance_wins
```

---

## SECTION 6: VALIDATION RULES

### 6.1 100 Program Generation Laws — Machine-Checkable

Each validation has: `validation_id`, `rule_description`, `severity` (critical/warning/info).

| ID | Rule | Severity |
|----|------|----------|
| V001 | Conditioning never precedes power or strength. | critical |
| V002 | Exercise difficulty ≤ athlete max difficulty. | critical |
| V003 | Pulling volume ≥ pushing volume in session. | critical |
| V004 | Core present in session, placed in last block. | critical |
| V005 | Posterior chain exercise present in session. | critical |
| V006 | Power exercises have full recovery (2-5 min between sets). | critical |
| V007 | No more than 3 strength exercises per session. | critical |
| V008 | Session duration ≤ 90 minutes. | critical |
| V009 | Warm-up patterns match session main work. | warning |
| V010 | Session has defined purpose. | critical |
| V011 | No two consecutive sessions identical. | warning |
| V012 | No static stretching before main work. | critical |
| V013 | Prehab exercise present. | critical |
| V014 | Core not before power or strength. | critical |
| V015 | Activation precedes any loaded work. | critical |
| V016 | Exercise difficulty match is primary filter. | critical |
| V017 | Equipment match before variety. | critical |
| V018 | No exercise requiring unavailable equipment. | critical |
| V019 | Tied selection → least recently used. | info |
| V020 | Exercise substitution within family first. | warning |
| V021 | Intent preserved across family substitution. | critical |
| V022 | Olympic lifts are first main work exercise. | warning |
| V023 | Box jumps not conditioning, height ≤ knee height for power. | warning |
| V024 | Depth jumps require 1.5x BW squat. | critical |
| V025 | Single-leg load = 50% bilateral equivalent on first intro. | info |
| V026 | Carries distance/time based, min 20m or 20s per set. | info |
| V027 | Med ball throws require full recovery. | warning |
| V028 | Sprint work measured in meters. | info |
| V029 | Tempo runs specify pace and HR zone. | warning |
| V030 | Plyometric ground contacts ≤ 30 per session. | critical |
| V031 | Beginners no Olympic lifts. | critical |
| V032 | Beginners no depth jumps > 1 foot landing. | critical |
| V033 | Beginners use 60-70% 1RM or RPE 6-7. | warning |
| V034 | Beginners demonstrate competency before load progression. | warning |
| V035 | Intermediates complex training after 4 weeks foundation. | info |
| V036 | Advanced may use velocity-based termination. | info |
| V037 | Athlete level reassessed every 8 weeks. | info |
| V038 | Returning from 4+ weeks off regresses one level for 2 weeks. | critical |
| V039 | Youth U16 no 1RM testing. | critical |
| V040 | Youth U16 no heavy Olympic lifts, depth jumps, spinal loading >50% BW. | critical |
| V041 | Strength progression = reps first, then load. | warning |
| V042 | Load increase based on previous 2-3 sessions. | warning |
| V043 | No progress 3 consecutive sessions → rotate exercise. | warning |
| V044 | No progress 6 consecutive sessions → deload or change family. | warning |
| V045 | Primary compound load increases 2.5-5 kg max. | info |
| V046 | Power progression = velocity → load → complexity. | info |
| V047 | Accessory progression faster than primary. | info |
| V048 | Bodyweight progression = rep thresholds (3x12). | info |
| V049 | Deload every 4-6 weeks. | warning |
| V050 | Deload volume 40-60%, intensity maintained. | warning |
| V051 | Competition week volume -20-30%, intensity maintained. | warning |
| V052 | Off-season: build volume 2-4 weeks before intensity. | info |
| V053 | Pre-season: decrease volume, maintain/increase intensity. | info |
| V054 | In-season: do not progress, maintain. | warning |
| V055 | Progress measured against athlete's own history. | info |
| V056 | Every strength session: knee dominant + hip dominant. | critical |
| V057 | Every power session: explosive lower + upper body. | warning |
| V058 | Every session (except deload/RTS): push + pull. | critical |
| V059 | Every conditioning session: warmup + main block + cooldown. | warning |
| V060 | Full body sessions: lower + push + pull + core. | critical |
| V061 | Upper/lower splits: lower=quad+posterior+core, upper=HPush+HPull+VPull+core. | warning |
| V062 | Court sport: COD + single-leg knee + rotational mandatory. | critical |
| V063 | Contact sport: loaded carries + neck prep every session. | critical |
| V064 | Sprint development: sprint technique before sprint effort. | warning |
| V065 | Return-to-sport: injury prehab before loaded exercise. | critical |
| V066 | Exercises rotate every 4-6 weeks, 1-2 per family. | warning |
| V067 | Primary compounds may stay 8 weeks if progressing. | info |
| V068 | Accessories rotate every 3-4 weeks. | info |
| V069 | Rotated-out exercise not returned for 8 weeks minimum. | info |
| V070 | Progression overrides rotation. | warning |
| V071 | Pain overrides progression. | critical |
| V072 | Rotate to least recently used exercise in family. | info |
| V073 | Rotated-in exercise same difficulty or one level higher. | info |
| V074 | Never rotate >30% of exercises in one session. | warning |
| V075 | Rotation is per-athlete, not per-group. | info |
| V076 | Same-family substitution preferred over cross-family. | warning |
| V077 | When cross-family: match training intent. | critical |
| V078 | When intent can't match: match movement plane. | warning |
| V079 | Equipment loss: next priority in family that matches equipment. | warning |
| V080 | Injury substitution: mechanically different variation in same family. | critical |
| V081 | Cross-family injury substitution: same muscle group, different pattern. | warning |
| V082 | No viable substitution: skip slot, flag it. | warning |
| V083 | Travel: maintain family order, downgrade equipment. | info |
| V084 | Crowded gym: maintain family and intent. | info |
| V085 | Emergency: bodyweight L1 in same family. If not possible, skip. | info |
| V086 | Every session: minimum one measurable data point. | warning |
| V087 | Rest intervals specified for each block. | critical |
| V088 | Conditioning never punishment. | critical |
| V089 | Strength working sets: 1-3 RIR (except competition peaking). | warning |
| V090 | No coaching red flag violations. | critical |
| V091 | Coach must articulate purpose of every exercise. | info |
| V092 | Program accounts for injury history. | critical |
| V093 | S&C program does not conflict with sport practice load. | warning |
| V094 | Individualisation within group template. | info |
| V095 | Every block ends with review. | info |
| V096 | Session score < 8/10: do not deliver. | critical |
| V097 | New pain during session: stop exercise, substitute. | critical |
| V098 | Missed 3+ consecutive sessions: regress one level. | critical |
| V099 | 4+ weeks no training: first 2 weeks return-to-sport protocol. | critical |
| V100 | Rule conflict: safety > performance > volume > technique. | critical |

### 6.2 50 Conditioning Laws — Machine-Checkable

| ID | Rule | Severity |
|----|------|----------|
| CL001 | One primary energy system per conditioning session. | critical |
| CL002 | Conditioning never precedes power or strength. | critical |
| CL003 | Speed requires fresh CNS. | critical |
| CL004 | Zone 2 on separate days from heavy strength or 6h apart. | warning |
| CL005 | RSA requires 95-100% effort. | warning |
| CL006 | Recovery conditioning RPE ≤ 3. | critical |
| CL007 | Lactate tolerance and alactic speed not same week. 48h min. | critical |
| CL008 | In-season conditioning volume ≤ 50% off-season. | warning |
| CL009 | Conditioning warm-up specific to modality. | warning |
| CL010 | Conditioning cool-down ≥ 5 min at RPE ≤ 3. | warning |
| CL011 | High-intensity conditioning ≤ 45 min. Low-intensity ≤ 60 min. | critical |
| CL012 | Rest intervals specified in every protocol. | critical |
| CL013 | High-intensity conditioning max 2 sessions/week. | warning |
| CL014 | Conditioning volume inversely related to practice volume. | warning |
| CL015 | One day/week zero conditioning. | info |
| CL016 | Conditioning progression: volume before intensity. | info |
| CL017 | Weekly conditioning volume increase ≤ 10%. | warning |
| CL018 | New energy system requires 2 weeks exposure before overload. | info |
| CL019 | Aerobic base (4+ weeks) before high-intensity for <1yr training age. | critical |
| CL020 | MAS pace requires individual test. Generic pace prohibited. | critical |
| CL021 | RSA progression: increase work:rest, then decrease rest, then increase reps. | info |
| CL022 | Deload: conditioning volume -40-60%, intensity ≤ RPE 6. | warning |
| CL023 | Beginners: no lactate tolerance. | critical |
| CL024 | Beginners RSA starts at every 40s. | warning |
| CL025 | Intermediate: 1 high-intensity session/week max. | warning |
| CL026 | Advanced: max 2 high-intensity sessions/week. | warning |
| CL027 | Youth U16: no lactate tolerance, heavy sled, descending ladders. | critical |
| CL028 | Youth U16: high-speed running ≤ 400m/session. | warning |
| CL029 | Return-to-sport: aerobic capacity only for first 2 weeks. | critical |
| CL030 | Conditioning protocol matches available environment. | warning |
| CL031 | Treadmill supplementary. Field athletes need ≥1 over-ground session/week. | warning |
| CL032 | Grass preferred for high-intensity running. Hard surface ≤ 1 session/week. | info |
| CL033 | Limited space (≤20m): shuttle-based protocols only. | warning |
| CL034 | Heat >30°C: high-intensity volume -30%, increase rest. | warning |
| CL035 | Altitude >1500m: MAS -5% per 1000m. | info |
| CL036 | Power maintenance in every conditioning block, ≥1 session/week. | warning |
| CL037 | Power maintenance: maximal intent every rep. | warning |
| CL038 | Power maintenance: 4-6 reps, 3-10s efforts, full recovery. | info |
| CL039 | In-season power maintenance non-negotiable. | critical |
| CL040 | 30m fatigue test default assessment every 4 weeks. | info |
| CL041 | Every conditioning session produces ≥1 data point. | warning |
| CL042 | RSA: record fastest and slowest rep. Decrement >10% flags issue. | info |
| CL043 | Aerobic capacity: HR zone 2 monitoring required. | info |
| CL044 | MAS testing every 4-6 weeks, recalculate pace. | info |
| CL045 | Yo-Yo IR1 pre and post pre-season minimum. | info |
| CL046 | Conditioning substitution: maintain energy system first, then work:rest, then modality. | warning |
| CL047 | Same-system substitution first. Do not switch systems. | warning |
| CL048 | Injury modification: maintain intensity, reduce volume and impact. | warning |
| CL049 | Substitution maintains fatigue score target ±1. | warning |
| CL050 | Session RPE >9 first execution → regress one level. | warning |

### 6.3 12-Point Credibility Check

| # | Check | Pass Condition | Severity |
|---|-------|---------------|----------|
| C01 | Posterior chain present | ≥1 of: DLHD, SLHD, HPull, Ball(KB Swing/Clean) | critical |
| C02 | Push/pull balanced | HPush count ≤ HPull count in session | critical |
| C03 | Core included | ≥1 Core exercise | critical |
| C04 | Appropriate difficulty | All exercises ≤ athlete max difficulty | critical |
| C05 | Equipment available | Every exercise equipment ∈ athlete profile | critical |
| C06 | Session flow correct | Power before strength, Core last, Warm-up first | critical |
| C07 | Power before fatigue | Power precedes strength and conditioning | critical |
| C08 | Rest intervals reasonable | Rest ∈ expected range per block type | warning |
| C09 | Knee/hip balance | ≥1 knee AND ≥1 hip in full body sessions | critical |
| C10 | No red flags | Zero violations of 50 red flags | critical |
| C11 | Volume within limits | Work within Section 3.3 min/max | warning |
| C12 | Rotation respects history | No exercise in same slot without progression | warning |

Scoring: Pass = 1 point. Minimum acceptable: 8/10. Score < 8 → do not deliver.

### 6.4 50 Coach Red Flag Checks

Each red flag from Coaching Bible Section 10 becomes a check. Implementation:
- Checks are grouped by category (session design, exercise selection, load management, coaching behavior, missing standards)
- Any single red flag detected → check C10 fails → session cannot score 10/10
- Example flags that are machine-checkable: no posterior chain (RF-16), push:pull > 1 (RF-17), crunches as primary core (RF-19), no carries (RF-21), no single-leg work (RF-18), no specified rest (RF-06), >3 strength exercises (RF-04), static stretching in warm-up (RF-02), conditioning before strength (RF-03), no power work in field sport program (RF-08)

---

## SECTION 7: API CONTRACTS

### 7.1 generate_program()

```
FUNCTION generate_program(
    athlete: AthleteProfile
) -> GeneratedProgram
```

**Input:**
```python
athlete = AthleteProfile(
    sport="rugby",
    training_age_years=2.5,
    season_phase="off_season",
    goal="general_strength",
    equipment_profile=EquipmentProfile.BASIC_GYM,
    athlete_level=AthleteLevel.INTERMEDIATE,
    technique_consistency=0.9,
    injury_status="cleared",
    injury_history=["acl_left_2023"],
    fatigue_level="normal",
    weeks_since_break=0,
    recent_exercises={
        "DLKD-003": {"last_used": "2_weeks_ago", "technique_score": 0.9, "sessions_count": 6},
        "HPush-003": {"last_used": "1_week_ago", "technique_score": 0.85, "sessions_count": 4}
    }
)
```

**Output:**
```python
program = GeneratedProgram(
    session=Session(...),
    athlete=athlete,
    generation_timestamp="2026-06-19T10:00:00Z",
    version="FORGE V1"
)
```

**Processing steps (internal):**
1. `blueprint = select_blueprint(athlete)` — decision tree based on sport, season, goal, training age
2. `level = determine_level(athlete)` — from training age, technique, strength base
3. `profile = get_equipment_profile(athlete.equipment)` — maps to 1 of 4 profiles
4. `slots = resolve_slots(blueprint, level)` — mandatory + optional families, sort by slot_order, cap at 6
5. `blocks = []`; for each slot: `exercise = select_exercise(slot.family, level, profile, athlete.recent_exercises, athlete.injury_history)`
6. `blocks = assign_training_variables(blocks, blueprint, level)` — sets, reps, rest, load
7. `session.validation_score, session.validation_failures = validate_session(session)`
8. If `session.validation_score < 8`: back to step 5, substitute the violating exercise (max 3 retries)
9. `return GeneratedProgram(session, athlete, timestamp)`

### 7.2 substitute_exercise()

```
FUNCTION substitute_exercise(
    family: FamilyCode,
    athlete_level: AthleteLevel,
    equipment_profile: EquipmentProfile,
    injury_history: list[str],
    recent_exercises: dict,
    current_exercise_id: str
) -> Optional[Exercise]
```

**Input:** The family to substitute in, athlete constraints, and the exercise being replaced (to avoid returning the same one).

**Output:** Either a valid Exercise or `null` (which means skip this slot and flag it).

**Processing:**
1. Priority 1: Same family, next priority exercise that passes all filters
2. Priority 2: Same intent category (e.g., "lower body posterior"), substitute family
3. Priority 3: Same equipment, any family
4. Priority 4: Return null (coaching gap)

### 7.3 generate_conditioning()

```
FUNCTION generate_conditioning(
    session: Session,
    athlete_level: AthleteLevel,
    goal: str,                    # "recovery", "aerobic_capacity", "aerobic_power",
                                  # "extensive_tempo", "intensive_tempo", "rsa",
                                  # "alactic_speed", "lactate_tolerance", "power_maintenance"
    environment: str,             # "field", "track", "treadmill", "indoor", "limited_space"
    time_available: int           # minutes available (10, 20, 30, 45)
) -> Optional[ConditioningProtocol]
```

**Input:** Session context + conditioning-specific parameters.

**Output:** Either a level-adjusted ConditioningProtocol or null (conditioning omitted).

**Processing:**
1. `family = decision_tree(athlete_level, goal)` — from Part 1 of Conditioning Intelligence V2
2. `candidates = get_protocols_by_family(family)` — filter to matching environment
3. `selected = select_by_tier(candidates)` — A tier first, B tier fallback
4. `adjusted = apply_level_variant(selected, athlete_level)` — use L1-L5 variants
5. `valid = validate_conditioning_laws(adjusted, session, athlete_level)` — check 50 COND-LAWs
6. If invalid: `substitute_in_family(family, valid_protocols)` or return null

### 7.4 validate_program()

```
FUNCTION validate_program(
    session: Session
) -> tuple[int, list[str]]
```

**Input:** A session object (completed or mid-generation).

**Output:** `(score: int 0-10, failures: list[str])`.

**Processing:**
1. Run all 12 credibility checks
2. Run all applicable 100 laws (Skip laws that are out-of-scope for this session type)
3. Run all applicable 50 conditioning laws (if conditioning present)
4. Score = credibility checks passed (out of 12, min acceptable = 8)
5. Return score + list of failed check descriptions

### 7.5 render_program()

```
FUNCTION render_program(
    program: GeneratedProgram,
    format: str = "text"           # "text" or "structured"
) -> str | dict
```

**Input:** A fully validated GeneratedProgram.

**Output:** Coach-readable session document (text) or structured data (dict).

**Text format structure:**
```
SESSION: Full Body Strength
PURPOSE: General strength accrual across all major movement patterns.
DURATION: 60-75 min
ATHLETE LEVEL: Intermediate

BLOCK 1: PREPARATION (15-25 min)
  Warm-up: Movement prep for squat + hinge + push pattern
  Activation: Glute activation + scapular control

BLOCK 2: MAIN WORK
  POWER: Countermovement Jump
    Sets: 3 | Reps: 4 | Rest: 3 min
    Cue: Maximal intent on every rep. Ground contact < 0.25s.

  STRENGTH PRIMARY: Barbell Back Squat
    Sets: 4 | Reps: 5 | Rest: 3 min | Load: RPE 7-8
    Cue: Heel drive. Brace before descent.

  STRENGTH SECONDARY: Dumbbell Bench Press
    Sets: 3 | Reps: 8 | Rest: 2 min | Load: RPE 7
    Cue: Scapular retraction before press.

  ACCESSORY: Dumbbell Row
    Sets: 3 | Reps: 12 | Rest: 90s | Load: RPE 7

  CORE: Plank
    Sets: 3 | Reps: 45s hold | Rest: 60s

BLOCK 3: CLOSING (10-15 min)
  COOLDOWN: 5 min light stretch

VALIDATION: 10/10
```

---

## SECTION 8: TEST PLAN

### 8.1 Unit Tests

| # | Test | Description | Expected |
|---|------|-------------|----------|
| UT01 | select_blueprint_active_injury | Injury active → Return to Sport | Blueprint 12 |
| UT02 | select_blueprint_off_season_mass | Off-season, goal=mass → Hypertrophy | Blueprint 11 |
| UT03 | select_blueprint_off_season_contact | Off-season, contact sport → Rugby Off-Season | Blueprint 09 |
| UT04 | select_blueprint_off_season_court | Off-season, court sport → Court Sport AD | Blueprint 08 |
| UT05 | select_blueprint_pre_season_conditioning | Pre-season, goal=conditioning → Strength + Conditioning | Blueprint 03 |
| UT06 | select_blueprint_in_season_maintenance | In-season, goal=maintenance → Power Maintenance | Blueprint 06 |
| UT07 | select_blueprint_transition_fatigue | Transition, high fatigue → Deload | Blueprint 13 |
| UT08 | select_blueprint_default | Unknown profile → Full Body Strength | Blueprint 01 |
| UT09 | determine_level_beginner | Training age 0.5 → Beginner | Beginner |
| UT10 | determine_level_intermediate | Training age 2, technique 0.9 → Intermediate | Intermediate |
| UT11 | determine_level_advanced | Training age 4, strength base met → Advanced | Advanced |
| UT12 | determine_level_return_from_break | 5 weeks off, was Advanced → Intermediate | Intermediate |
| UT13 | determine_level_youth_u16 | Age 15, training age 3 → max Intermediate | Intermediate |
| UT14 | equipment_profile_field_only | No barbell, no dumbbell → Field Only | Field Only |
| UT15 | equipment_profile_basic_gym | Barbell + rack + bench + dumbbells → Basic Gym | Basic Gym |
| UT16 | equipment_profile_commercial | Above + cable → Commercial Gym | Commercial Gym |
| UT17 | equipment_profile_elite | Full access + specialty bars + sled → Elite Facility | Elite Facility |
| UT18 | resolve_slots_mandatory_only | Blueprint with 2 mandatory families → 2 slots | 2 slots |
| UT19 | resolve_slots_with_optional | Blueprint with 4 mandatory + 4 optional → 6 slots max | ≤6 slots |
| UT20 | resolve_slots_sort_order | Slots sorted by blueprint.slot_order | Correct order |
| UT21 | select_exercise_difficulty_match | Beginner, difficulty L3 exercise → skip | Next candidate |
| UT22 | select_exercise_equipment_match | Field Only profile, barbell exercise → skip | Next candidate |
| UT23 | select_exercise_injury_conflict | ACL history, deep squat → skip | Next candidate |
| UT24 | select_exercise_prefer_recent | Recently performed with good technique → prefer | Selected |
| UT25 | select_exercise_tie_least_recent | Tie → least recently used | Selected |
| UT26 | select_exercise_fallback_substitution | No match in family → trigger same-family sub | Lower difficulty |
| UT27 | substitute_same_family | DLKD no equipment → next DLKD priority | Valid exercise |
| UT28 | substitute_same_intent | No DLHD available → substitute intent group | Cross-family |
| UT29 | substitute_emergency_fallback | Nothing available → null | null |
| UT30 | validate_session_perfect | Valid session → 10/10 | 10/10 |
| UT31 | validate_session_missing_core | No core → check C03 fails | <10/10 |
| UT32 | validate_session_missing_posterior | No posterior chain → check C01 fails | <10/10 |
| UT33 | validate_session_push_over_pull | HPush > HPull → check C02 fails | <10/10 |
| UT34 | validate_session_below_8 | Multiple failures → score < 8 | Do not deliver |
| UT35 | validate_law_001_conditioning_before_strength | Conditioning before strength → fail | critical |
| UT36 | validate_law_004_no_core | No core → fail | critical |
| UT37 | validate_law_030_excessive_plyos | 35 ground contacts → fail | critical |
| UT38 | validate_law_039_youth_1rm | Youth U16, 1RM test → fail | critical |
| UT39 | validate_law_062_court_mandatory | Court session missing COD → fail | critical |
| UT40 | validate_law_063_contact_carries | Contact session no carries → fail | critical |
| UT41 | validate_conditioning_law_001_two_systems | Two energy systems targeted → fail | critical |
| UT42 | validate_conditioning_law_003_speed_fatigued | Speed after conditioning → fail | critical |
| UT43 | validate_conditioning_law_023_beginner_lactate | Beginner lactate protocol → fail | critical |
| UT44 | validate_cl_029_return_sport_high_intensity | RTS athlete, high-intensity cond → fail | critical |
| UT45 | conditioning_decision_tree_recovery | Goal=recovery → recovery family | Correct family |
| UT46 | conditioning_decision_tree_aerobic_capacity | Goal=aerobic_capacity, 30min field → LSD | AC protocol |
| UT47 | conditioning_decision_tree_rsa | Goal=rsa, intermediate → RSA family | RSA protocol |
| UT48 | conditioning_select_a_tier_first | A tier available → A tier selected | A tier |
| UT49 | conditioning_level_adjustment | Elite protocol → L1 for beginner | Reduced volume |
| UT50 | render_program_text | Valid session → correctly formatted string | Matches spec |

### 8.2 Integration Tests

| # | Test | Description | Expected |
|---|------|-------------|----------|
| IT01 | full_generation_beginner_field_only | Generate session: Beginner, Field Only, off-season | Valid session ≥8/10 |
| IT02 | full_generation_intermediate_basic_gym | Generate session: Intermediate, Basic Gym, off-season | Valid session ≥8/10 |
| IT03 | full_generation_advanced_commercial | Generate session: Advanced, Commercial, pre-season, power goal | Valid session ≥8/10 |
| IT04 | full_generation_court_sport_in_season | Court Sport AD blueprint, in-season | Sessions per week correct |
| IT05 | full_generation_contact_sport_off_season | Rugby blueprint, off-season, elite facility | Mandatory carries present |
| IT06 | full_generation_youth_u16 | Youth blueprint, beginner, field only | No 1RM, no depth jumps, play-based cond |
| IT07 | full_generation_return_to_sport | RTS blueprint, active injury | No explosive, prehab present |
| IT08 | full_generation_deload | Deload blueprint, high fatigue | 50-60% volume, no power, no conditioning |
| IT09 | full_generation_with_substitution | Equipment impossible for first-choice exercise | Substituted correctly, ≥8/10 |
| IT10 | full_generation_with_conditioning | Include conditioning block | Valid protocol selected, all CL laws pass |
| IT11 | generation_fails_validation_then_fixes | First attempt fails credibility | Max 3 retries, then substitution or fail |
| IT12 | all_14_blueprints_generate | Each blueprint produces a valid session | 14/14 pass at ≥8/10 |

### 8.3 Stress Tests

| # | Test | Description | Expected |
|---|------|-------------|----------|
| ST01 | worst_case_athlete | Training age 0, field only, every injury, every contraindication | Generates something valid or explains why not |
| ST02 | equipment_edge_case | Athlete reports both "barbell" and "no rack" | Resolves consistently |
| ST03 | all_field_profiles_consistent | 100 generations with same input produce same output | Determistic: all 100 identical |
| ST04 | injury_combinations | Every injury type paired with every family | Substitution always produces safe exercise |
| ST05 | conditioning_all_goals_all_envs | All 9 conditioning goals × 5 environments × 4 levels × 4 time options | Produces valid protocol or explains gap |

### 8.4 Credibility Tests

| # | Test | Description | Expected |
|---|------|-------------|----------|
| CT01 | cada_verification | All 100 laws applied to each of 14 blueprint types | No law violated by any valid generation |
| CT02 | red_flag_free | No session triggers any of the 50 red flags | Pass all |
| CT03 | posterior_chain_guarantee | Every session checked for posterior chain | Present in 100% of sessions |
| CT04 | push_pull_ratio_guarantee | Every session checked for push:pull ≤ 1:1 | Compliant in 100% |
| CT05 | core_guarantee | Core present in 100% of sessions | Present |

### 8.5 Conditioning Tests

| # | Test | Description | Expected |
|---|------|-------------|----------|
| CNDT01 | all_100_protocols_selected | Every protocol in library can be selected by some input combination | 100/100 reachable |
| CNDT02 | no_c_tier_as_default | C tier protocols never selected when A tier available | Zero C tier in default path |
| CNDT03 | fatigue_score_consistency | Substituted protocol has fatigue score ±1 of original | Consistent |
| CNDT04 | all_10_systems_reachable | Each energy system has at least one valid selection path | 10/10 reachable |
| CNDT05 | law_coverage | Every COND-LAW is triggered by at least one test | 50/50 tested |

### Expected Test Counts

| Type | Count |
|------|-------|
| Unit tests | ≥50 |
| Integration tests | ≥12 |
| Stress tests | ≥5 |
| Credibility tests | ≥5 |
| Conditioning tests | ≥5 |
| **Total** | **≥77** |

---

## SECTION 9: IMPLEMENTATION ORDER

One build path. No alternatives. Do step N before step N+1.

### Step 1: Data Layer — Exercise Library

**What:** Create the 191-exercise catalog as a data structure (list of dicts or JSON file).
**Files:** None generated — this is data, not code. Format: JSON array of Exercise objects.
**Acceptance:** Every exercise from FORGE_COACHING_REFERENCE_DATABASE.md Part 2 is present. All 15 families covered. Fields match Section 4 dataclass.

### Step 2: Data Layer — Blueprint Catalog

**What:** Create the 14-blueprint catalog.
**Acceptance:** Every blueprint from FORGE_BLUEPRINT_CATALOG_V1.md is present with all fields. Slot orders match. Minimum session compositions match Rulebook Section 3.2.

### Step 3: Data Layer — Exercise Family Priorities

**What:** Create the per-family selection priority lists from Rulebook Section 2.2.
**Acceptance:** All 15 families have priority-ordered exercise lists. Each entry references an Exercise.id from Step 1. Difficulty and equipment fields match.

### Step 4: Data Layer — Conditioning Protocol Library

**What:** Create the 100-protocol catalog with tier rankings.
**Acceptance:** Every protocol from FORGE_CONDITIONING_LIBRARY_V1.md is present. A/B/C tier from FORGE_CONDITIONING_INTELLIGENCE_V2.md Part 2 is attached. L1-L5 level variants are defined.

### Step 5: Data Layer — Substitution Matrix

**What:** Create the substitution matrix data structures — per-family ladders, cross-family intent map, equipment loss table, injury modification table.
**Acceptance:** All 15 families have substitution ladders. Cross-family intent map covers all 15 families. Injury table covers all 10 injury types from Rulebook Section 7.4.

### Step 6: Core — Athlete Profile Object

**What:** Implement the AthleteProfile dataclass.
**Acceptance:** All fields present and typed. Equipment profile mapping function from raw equipment list to 1 of 4 profiles.

### Step 7: Core — Blueprint Selector

**What:** Implement `select_blueprint()` as a decision tree (nested if/else or match/case).
**Acceptance:** Passes UT01-UT08. All 14 bluepaths reachable. Default path returns Full Body Strength.

### Step 8: Core — Athlete Level Determiner

**What:** Implement `determine_level()`.
**Acceptance:** Passes UT09-UT13. Special cases handled: return-from-break regression, youth U16 cap.

### Step 9: Core — Slot Resolver

**What:** Implement `resolve_slots()`.
**Acceptance:** Passes UT18-UT20. Never exceeds 6 slots. Core always last. Power always before strength. Conditioning always final.

### Step 10: Core — Exercise Selector

**What:** Implement `select_exercise()` with all five filters:
1. Difficulty match
2. Equipment match
3. Injury conflict check
4. Recent exercise preference
5. Least-recently-used tiebreaker

**Acceptance:** Passes UT21-UT25. Calls substitution when no candidate passes all filters.

### Step 11: Core — Substitution Engine

**What:** Implement `substitute_exercise()` with the four-priority chain.
**Acceptance:** Passes UT26-UT29. Cross-family substitution uses intent map. Emergency fallback returns null.

### Step 12: Core — Training Variable Assigner

**What:** Implement `assign_training_variables()`.
**Acceptance:** Block types get correct sets/reps/rest ranges per Section 3.3 of Rulebook. Beginner modifier applied. Power blocks get full recovery. Core is last.

### Step 13: Core — Session Validator (100 Laws)

**What:** Implement all 100 LAW-xxx checks as boolean functions.
**Acceptance:** Passes UT35-UT40. All 100 laws produce a check result. Severity (critical/warning/info) is attached.

### Step 14: Core — 12-Point Credibility Check

**What:** Implement the 12 credibility checks + scoring.
**Acceptance:** Passes UT30-UT34. Score correctly computed. Score < 8 triggers regeneration.

### Step 15: Core — Conditioning Selector

**What:** Implement the conditioning decision tree + protocol selector + level adjuster.
**Acceptance:** Passes UT45-UT49. Decision tree covers all 9 goals × 5 environments × 4 time options. A tier default. Level adjustment modifies sets/reps/rest.

### Step 16: Core — 50 Conditioning Law Validator

**What:** Implement all 50 COND-LAW-xxx checks.
**Acceptance:** Passes UT41-UT44. Substitution within same energy system family when validation fails.

### Step 17: Core — Session Renderer

**What:** Implement `render_program()`.
**Acceptance:** Passes UT50. Output matches the text format specification. Coaching cues included. Validation score displayed.

### Step 18: Core — Generation Pipeline Orchestrator

**What:** Implement `generate_program()` that calls steps 7-17 in order.
**Acceptance:** Passes all integration tests (IT01-IT12). Retry logic: 3 maximum retries per slot. On 3rd failure, substitute family.

### Step 19: Core — 50 Red Flag Checker

**What:** Implement machine-checkable red flag validators.
**Acceptance:** At minimum: RF-02 (static stretching), RF-03 (conditioning before strength), RF-04 (>3 strength exercises), RF-06 (no rest), RF-16 (no posterior chain), RF-17 (push/pull >1), RF-18 (no single-leg), RF-19 (crunches as core), RF-21 (no carries). Integrated into C10 check.

### Step 20: Final Integration

**What:** Wire everything together. Test end-to-end with all 14 blueprints.
**Acceptance:** All 77+ tests pass. Generation completes in < 3 seconds on consumer hardware. Deterministic: same input → same output every time.

---

## SECTION 10: FINAL MVP DEFINITION

### FORGE MVP is complete when ALL of the following pass:

| # | Criterion | Pass/Fail |
|---|-----------|-----------|
| 1 | `select_blueprint()` produces a correct blueprint for every combination of (sport, season_phase, goal, training_age, injury_status) | ☐ |
| 2 | `resolve_slots()` never produces a session with >6 main work slots | ☐ |
| 3 | `select_exercise()` never selects an exercise above the athlete's max difficulty level | ☐ |
| 4 | `select_exercise()` never selects an exercise requiring unavailable equipment | ☐ |
| 5 | Every generated session scores ≥8/10 on the 12-point credibility check | ☐ |
| 6 | Every generated session passes all 100 program generation laws (critical severity only; warnings may be present) | ☐ |
| 7 | Every generated session with a conditioning block passes all 50 conditioning laws | ☐ |
| 8 | Every generated session has: posterior chain present, push:pull ≤ 1:1, core present, power before strength | ☐ |
| 9 | No generated session triggers any of the 50 coach red flags | ☐ |
| 10 | Substitution engine produces a valid exercise (or null + coaching gap flag) for every substitution scenario | ☐ |
| 11 | Conditioning selector produces a valid A-tier protocol (or B-tier fallback) for every (goal, environment, time, level) combination | ☐ |
| 12 | All 14 blueprints can generate at least one valid session | ☐ |
| 13 | The system is deterministic: identical inputs produce identical outputs across all runs | ☐ |
| 14 | Generation completes in < 3 seconds per session request (consumer hardware, no network) | ☐ |
| 15 | All 77+ tests pass | ☐ |

### When all 15 criteria pass: FORGE MVP is complete.

---
