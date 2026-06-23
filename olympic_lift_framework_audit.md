# Olympic Lift Framework Audit

**Auditor:** Senior S&C Coach (CSCS, ASCC), Performance Science Lead
**Date:** 2026-06-15
**System:** Forge S&C Recommendation Engine v1

---

## Executive Summary

The system contains **1 of 14 required Olympic lifts** (Power Clean) at **7% completion**. Only Power Clean exists in the database schema (000002). The remaining 13 exercises have zero representation in schema, mock repos, templates, or exercise pools. The single existing lift is misclassified (movement pattern = Hinge only, missing Squat catch priority), has no progression chain, and has the wrong fallback (Kettlebell Swing is not a clean progression).

**Olympic lift readiness: 7%** (1/14 exercises, 0/6 progression families)

---

## 1. Current State Assessment

### 1.1 What exists

| Component | Power Clean Status |
|-----------|-------------------|
| Database entry (exercises table) | Yes - 000002_seed_sample_data.up.sql:86 |
| Equipment mapping | Barbell (required) |
| Movement patterns | Primary: Hinge, Secondary: Squat |
| Physical qualities | RFD (10), Maximal Strength (8) |
| Training methods | Velocity-Based Training |
| Sport mappings | Olympic WL (10/1.00), American Football (9/0.92), Rugby (9/0.90), Sprinting (8/0.88) |
| Tags | Primary Lift, Bilateral, Posterior Chain, Explosive |
| Template slot mapping | Acceleration Development -> Primary -> Explosive Hinge/Extension (004:410) |
| Fallback exercise | Kettlebell Swing (004:412) |
| Mock repo presence | session_generator.py MOCK_EXERCISES (id=86) |
| Mock movement pattern | Hinge (session_generator.py:117) |
| In recommendation engine | **NO** - not in MockExerciseRepository.get_ranked_exercises() |
| In any exercise pool | **NO** - no template slot includes it in mock |
| Difficulty level | Advanced |
| Cricket sport mapping | **NONE** - no row in exercise_sport_mapping for Cricket |

### 1.2 Critical gaps

1. **No cricket-specific mapping** - Power Clean has zero transfer index for Cricket
2. **Not in mock exercise pools** - despite being in the DB, it never appears in recommendations
3. **Misclassified movement pattern** - labeled as 'Hinge' primary in session_generator.py vs 'Hinge' primary AND 'Squat' secondary in DB. The mock ignores the squat catch component.
4. **Wrong fallback** - Kettlebell Swing as fallback for Power Clean. These have different:
   - Load placement (barbell front rack vs kettlebell between legs)
   - Catch mechanics (full squat vs none)
   - Force vector (vertical pull vs hip hinge)

---

## 2. Required Exercise Review

### 2.1 Clean Family (7 exercises)

| Exercise | Current Status | Movement Category | Physical Driver Contribution | Tech Diff (1-10) | Risk (1-5) | Min Training Age | Appropriate Level |
|----------|---------------|-------------------|------------------------------|------------------|------------|-----------------|-------------------|
| Clean Pull | NOT IN SYSTEM | Hinge (Primary) | RFD: 8, Max Strength: 7, Power: 9 | 3 | 2 | 1 year | Intermediate+ |
| Mid-Thigh Pull | NOT IN SYSTEM | Hinge (Primary) | RFD: 10, Max Strength: 8, Power: 10 | 4 | 2 | 2 years | Intermediate+ |
| High Pull | NOT IN SYSTEM | Hinge (Primary), Pull (Vertical) (Secondary) | RFD: 9, Power: 9, Speed Strength: 8 | 5 | 3 | 2 years | Intermediate+ |
| Power Clean | EXISTS (partial) | Hinge (Primary), Squat (Secondary) | RFD: 10, Max Strength: 8, Power: 10 | 7 | 4 | 3 years | Advanced |
| Hang Clean | NOT IN SYSTEM | Hinge (Primary), Squat (Secondary) | RFD: 9, Power: 9, Rate Coding: 8 | 6 | 3 | 2 years | Intermediate+ |
| Squat Clean | NOT IN SYSTEM | Squat (Primary), Hinge (Secondary) | RFD: 10, Max Strength: 9, Power: 10, Mobility: 8 | 9 | 5 | 4 years | Advanced/Elite |
| Clean and Jerk | NOT IN SYSTEM | Squat (Primary), Overhead (Secondary), Hinge (Tertiary) | RFD: 10, Max Strength: 9, Power: 10, Stability: 9 | 10 | 5 | 5 years | Elite |

### 2.2 Snatch Family (4 exercises)

| Exercise | Current Status | Movement Category | Physical Driver Contribution | Tech Diff (1-10) | Risk (1-5) | Min Training Age | Appropriate Level |
|----------|---------------|-------------------|------------------------------|------------------|------------|-----------------|-------------------|
| Power Snatch | NOT IN SYSTEM | Hinge (Primary), Overhead Squat (Secondary) | RFD: 10, Power: 10, Mobility: 9, Stability: 8 | 8 | 5 | 4 years | Advanced |
| Hang Snatch | NOT IN SYSTEM | Hinge (Primary), Overhead Squat (Secondary) | RFD: 9, Power: 9, Coordination: 9 | 7 | 4 | 3 years | Advanced |
| Snatch Balance | NOT IN SYSTEM | Overhead Squat (Primary), Drop/Drive (Secondary) | RFD: 7, Stability: 9, Mobility: 9, Coordination: 8 | 8 | 4 | 3 years | Advanced |
| Overhead Squat | NOT IN SYSTEM | Squat (Primary), Overhead (Secondary) | Mobility: 10, Stability: 9, Strength: 6, Core: 8 | 7 | 3 | 2 years | Intermediate+ |

### 2.3 Pressing/Jerk Family (3 exercises)

| Exercise | Current Status | Movement Category | Physical Driver Contribution | Tech Diff (1-10) | Risk (1-5) | Min Training Age | Appropriate Level |
|----------|---------------|-------------------|------------------------------|------------------|------------|-----------------|-------------------|
| Push Press | NOT IN SYSTEM | Push (Vertical) (Primary), Hinge (Secondary) | Power: 9, RFD: 8, Overhead Stability: 8 | 4 | 3 | 1 year | Intermediate |
| Push Jerk | NOT IN SYSTEM | Push (Vertical) (Primary), Squat (Secondary) | Power: 9, RFD: 9, Coordination: 8, Stability: 8 | 6 | 4 | 2 years | Intermediate+ |
| Split Jerk | NOT IN SYSTEM | Push (Vertical) (Primary), Lunge (Secondary) | Power: 10, RFD: 9, Stability: 9, Coordination: 10 | 9 | 5 | 3 years | Advanced/Elite |

---

## 3. Movement Category Analysis

### 3.1 Current Power Clean classification error

The DB correctly assigns Power Clean to:
- **Primary**: Hinge (first pull phase)
- **Secondary**: Squat (catch phase)

The mock repo (session_generator.py) assigns only:
- **Hinge**

**Impact:** The squat catch component is completely lost in the mock system. This means:
- The movement pattern filter cannot distinguish Power Clean from Trap Bar Deadlift or Kettlebell Swing
- The system loses the ability to place Power Clean in slots requiring Squat pattern
- Progression to Squat Clean (where Squat becomes PRIMARY) has no path

**Recommended taxonomy for all Olympic lifts:**

| Exercise | Primary Pattern | Secondary Pattern | Tertiary Pattern |
|----------|----------------|-------------------|------------------|
| Clean Pull | Hinge | Pull (Vertical) | - |
| Mid-Thigh Pull | Hinge | Pull (Vertical) | - |
| High Pull | Hinge | Pull (Vertical) | - |
| Power Clean | Hinge | Squat | - |
| Hang Clean | Hinge | Squat | - |
| Squat Clean | Squat | Hinge | - |
| Power Snatch | Hinge | Overhead Squat | - |
| Hang Snatch | Hinge | Overhead Squat | - |
| Snatch Balance | Overhead Squat | Push (Vertical) | - |
| Overhead Squat | Squat | Push (Vertical) | - |
| Push Press | Push (Vertical) | Hinge | - |
| Push Jerk | Push (Vertical) | Squat | - |
| Split Jerk | Push (Vertical) | Lunge (Single-Leg) | - |
| Clean and Jerk | Squat | Push (Vertical) | Hinge |

### 3.2 Missing movement patterns needed

The system needs to add:
- **Pull (Vertical)** - for the first pull phase of clean/snatch (currently exists in pattern list but no exercises use it)
- **Overhead Squat** - for snatch balance and overhead squat catch positions (NOT currently in movement_patterns table)

---

## 4. Progression Chain Design

### 4.1 Clean progression chain

```
Training Age 0-1:
  Clean Pull (floor, moderate load, technique focus)
  -> Barbell RDL (warm-up / prep)

Training Age 1-2:
  Mid-Thigh Pull (from blocks or hang above knee, high velocity)
  -> Clean Pull (from floor)

Training Age 2-3:
  High Pull (with catch turn-over, light load)
  -> Hang Clean (from mid-thigh)
  -> Power Clean (from floor)

Training Age 3-4:
  Power Clean (70-85%, velocity based)
  -> Hang Squat Clean (building depth)

Training Age 4-5:
  Squat Clean (85%+)
  -> Clean + Front Squat complex

Training Age 5+:
  Clean and Jerk (full competition lift)
  -> Clean variants + Push Jerk/Split Jerk
```

### 4.2 Snatch progression chain

```
Training Age 2-3:
  Snatch Grip RDL (mobility prep)
  -> Snatch Pull (from floor)
  -> Overhead Squat (bar only -> light load)

Training Age 3-4:
  Power Snatch (from hang)
  -> Power Snatch (from floor)
  -> Snatch Balance (drop under)

Training Age 4-5:
  Snatch Balance (with load)
  -> Hang Snatch (full squat)
  -> Power Snatch + Overhead Squat complex

Training Age 5+:
  Full Snatch (from floor)
  -> Hang Snatch complexes
```

### 4.3 Missing progressions in current system

| Missing Progression | Impact | Priority |
|--------------------|--------|----------|
| Clean Pull (regression from Power Clean) | No regression path for beginners | P0 |
| Mid-Thigh Pull (velocity progression) | No velocity-focused clean variant | P0 |
| Hang Clean (coordination regression) | No entry point for catch mechanics | P0 |
| Squat Clean (depth progression) | No full squat catch variant | P1 |
| Overhead Squat | No snatch catch position training | P0 |
| Power Snatch | No snatch entry point | P1 |
| Push Press | No overhead loading progression | P1 |

---

## 5. Risk Assessment

### 5.1 Risk scores per exercise

| Exercise | Risk Score | Risk Factors |
|----------|-----------|--------------|
| Clean Pull | 2 (Low) | Spinal loading, no catch |
| Mid-Thigh Pull | 2 (Low) | Spinal loading, no catch |
| High Pull | 3 (Moderate) | Spinal loading, elbow turnover |
| Power Clean | 4 (High) | Spinal loading, catch position, wrist stress |
| Hang Clean | 3 (Moderate) | Same as Power Clean but higher velocity from hang |
| Squat Clean | 5 (Very High) | Full squat catch, mobility demand, spinal loading |
| Power Snatch | 5 (Very High) | Wide grip, overhead catch, mobility demand |
| Hang Snatch | 4 (High) | Overhead catch, higher velocity |
| Snatch Balance | 4 (High) | Overhead dropping position |
| Overhead Squat | 3 (Moderate) | Overhead stability, mobility demand |
| Push Press | 3 (Moderate) | Overhead loading, dip mechanics |
| Push Jerk | 4 (High) | Overhead catch, dip-drive timing |
| Split Jerk | 5 (Very High) | Asymmetric catch, overhead load, split position |
| Clean and Jerk | 5 (Very High) | Combination of all risk factors |

### 5.2 Current safety gaps

1. **No risk-based filtering in recommendation engine** - difficulty_level is the only filter. A Power Clean (Advanced) and an Overhead Squat (would be Intermediate+) would pass/fail the same filter despite vastly different risk profiles.

2. **No training age check** - a 12-year-old with training_age=0 and competition_level="Elite" (due to cricket skill) could be recommended Power Clean because difficulty_cap="Elite" allows it. The system has NO mechanism to prevent this.

3. **No mobility prerequisite check** - Overhead Squat requires thoracic extension, shoulder flexion, and ankle dorsiflexion ROM. The system has zero mobility assessments to verify readiness.

4. **No load exposure tracking** - An athlete returning from injury who has never done an Olympic lift could be prescribed Power Clean with velocity-based loading with no ramp protocol.

5. **Single fallback is technically unsafe** - Kettlebell Swing as fallback for Power Clean has a completely different movement pattern. If an athlete fails Power Clean due to:
   - Wrist mobility issue -> Kettlebell Swing doesn't address it
   - Squat catch depth issue -> Kettlebell Swing doesn't train it
   - Spinal loading intolerance -> Kettlebell Swing is LESS load but different pattern

### 5.3 Unsafe recommendation scenarios

| Scenario | Current System Response | Correct Response |
|----------|------------------------|-----------------|
| Beginner, 14yo, Power Clean in pool | Allowed if cap >= Advanced | Block: min training age 3yrs |
| Elite athlete with 0yrs training age | Allowed if cap=Elite | Regress to Clean Pull |
| Athlete with poor ankle mobility + Overhead Squat | No detection possible | Screen: require ankle ROM test |
| Athlete returning from back injury + Clean | No detection possible | Require clearance + regression |
| Athlete with no barbell experience + Snatch | No detection possible | Require overhead squat proficiency |

---

## 6. Template Integration Design

### 6.1 Current slot mapping

Power Clean is mapped to:
- **Acceleration Development** -> Primary -> Explosive Hinge/Extension (slot order 1)
- **Fallback:** Kettlebell Swing

### 6.2 Recommended slot assignments

| Template | Slot Position | Exercise | Rationale |
|----------|--------------|----------|-----------|
| Fast Bowler Power | Primary (Bilateral) | Power Clean, Hang Clean | Triple extension for brace force |
| Fast Bowler Power | Accessory (Triple Ext) | Clean Pull, Mid-Thigh Pull | Velocity-focused pull variants |
| Batter Strength/Power | Primary (Hinge) | Power Clean (alt. to Trap Bar DL) | Hip drive for bat speed |
| Acceleration Development | Primary | Mid-Thigh Pull, Clean Pull | RFD in horizontal/vertical |
| Speed Development | Accessory | Hang Clean, Power Clean | Inter-limb coordination |
| Rotational Power (Spinner) | NOT RECOMMENDED | - | Olympic lifts have low rotational transfer |
| General Strength | Primary | Clean Pull, Power Clean | Foundation for all variants |

### 6.3 Cricket-specific transfer indices

| Exercise | Cricket Transfer Index | Rationale |
|----------|----------------------|-----------|
| Clean Pull | 0.70 | Hip extension power, no catch complexity |
| Mid-Thigh Pull | 0.75 | Highest velocity clean variant, best RFD transfer |
| Power Clean | 0.65 | Full extension + catch, coordination demand limits transfer |
| Hang Clean | 0.60 | Higher velocity, less positional demand |
| Squat Clean | 0.45 | Excessive mobility demand for cricket context |
| Power Snatch | 0.35 | Overhead specificity low for cricket |
| Push Press | 0.55 | Overhead power for throwing, fielding |
| Clean and Jerk | 0.30 | Competition lift, low cricket specificity |

**Recommendation:** For cricket S&C, prioritize the Pull variants (Clean Pull, Mid-Thigh Pull) and Power Clean as the primary Olympic lifts. Squat Clean, Snatch variants, and Split Jerk have low transfer-to-cricket ratios and should be reserved for specialized blocks.

---

## 7. Missing Registry

### 7.1 Missing from exercise database

| Exercise | Should Be In | Priority | Notes |
|----------|-------------|----------|-------|
| Clean Pull | exercises + exercise_equipment + movement_patterns + physical_qualities + tags | P0 | Regression from Power Clean |
| Mid-Thigh Pull | exercises + full mapping | P0 | Highest cricket transfer |
| High Pull | exercises + full mapping | P1 | Intermediate progression |
| Hang Clean | exercises + full mapping | P0 | Catch mechanics development |
| Squat Clean | exercises + full mapping | P1 | Full clean depth variant |
| Push Press | exercises + full mapping | P1 | Entry level overhead loading |
| Push Jerk | exercises + full mapping | P2 | Overhead power development |
| Split Jerk | exercises + full mapping | P2 | Advanced overhead |
| Clean and Jerk | exercises + full mapping | P2 | Full competition lift |
| Power Snatch | exercises + full mapping | P1 | Broader power development |
| Hang Snatch | exercises + full mapping | P2 | Snatch entry point |
| Snatch Balance | exercises + full mapping | P2 | Overhead confidence |
| Overhead Squat | exercises + full mapping | P1 | Mobility + stability assessment |

### 7.2 Missing from movement patterns table

| Missing Pattern | Purpose | Priority |
|----------------|---------|----------|
| Overhead Squat | Snatch balance, snatch catch position, OHS exercise | P0 |

### 7.3 Missing from template slots

| Template | Missing Slot | Missing Exercise | Priority |
|----------|-------------|-----------------|----------|
| Fast Bowler Power | Velocity Pull variant | Clean Pull, Mid-Thigh Pull | P0 |
| Batter Strength/Power | Olympic lift alternative | Power Clean | P1 |
| Acceleration Development | Full clean progression chain | Power Clean -> Hang Clean -> Clean Pull | P0 |

### 7.4 Missing from mock repos

| File | Missing |
|------|---------|
| recommendation_engine.py MockExerciseRepository | All 14 Olympic exercises (currently 0 of 14) |
| session_generator.py MOCK_EXERCISES | 13 of 14 (only Power Clean exists) |
| session_generator.py MOCK_PATTERNS | 13 of 14 missing |
| exercise_sport_mapping | No Cricket transfer indices for Power Clean or any Olympic lift |

### 7.5 Missing progression/regression chains

| Current Gap | Priority | Solution |
|------------|----------|----------|
| No regression from Power Clean for beginners | P0 | Add Clean Pull (floor), Clean Pull (blocks) |
| No progression from Power Clean to full clean | P1 | Add Squat Clean, Clean and Jerk |
| No entry to snatch family | P1 | Add Overhead Squat, then Snatch Pull |
| No overhead progression | P1 | Add Push Press -> Push Jerk -> Split Jerk |

---

## 8. Implementation Plan

### 8.1 Migration 024: Schema additions

```
ALTER TABLE exercises ADD COLUMN technical_difficulty INTEGER CHECK (technical_difficulty BETWEEN 1 AND 10);
ALTER TABLE exercises ADD COLUMN risk_score INTEGER CHECK (risk_score BETWEEN 1 AND 5);
ALTER TABLE exercises ADD COLUMN minimum_training_age INTEGER DEFAULT 0;

INSERT INTO movement_patterns (name, description) VALUES
('Overhead Squat', 'Deep squat position maintaining a barbell in a locked-out overhead position.');
```

### 8.2 Migration 025: Exercise seeds

Seed all 14 Olympic lifts with:
- Full equipment mappings (Barbell required for all)
- Full movement pattern assignments (as per Section 3 taxonomy)
- Physical quality scores (as per Section 2 tables)
- Training method assignments (Velocity-Based Training for all)
- Tags: 'Olympic Lift', 'Explosive', 'Primary Lift', 'Bilateral'
- Sport mappings for Cricket (transfer indices 0.30-0.75)
- Technical difficulty scores (1-10)
- Risk scores (1-5)
- Minimum training age
- Appropriate athlete levels

### 8.3 Migration 026: Template slot mapping

Add to existing templates:
- Fast Bowler Power: Clean Pull (slot 3, replacing or alongside MB Overhead Toss)
- Acceleration Development: Expand from Power Clean to full clean chain
- Batter Strength: Power Clean (slot 1, alternative to Trap Bar Deadlift)

Create new slot_exercise_fallbacks:
- Power Clean -> Clean Pull (regression for beginners)
- Power Clean -> Hang Clean (alternative catch variant)
- Squat Clean -> Power Clean (depth progression)
- Push Jerk -> Push Press (regression for overhead)

### 8.4 Code changes

| File | Change | Priority |
|------|--------|----------|
| recommendation_engine.py | Add all 14 exercises to MockExerciseRepository.get_ranked_exercises() | P0 |
| session_generator.py | Add all 14 exercises to MOCK_EXERCISES and MOCK_PATTERNS | P0 |
| session_generator.py | Fix Power Clean force_type from 'Pull' to 'Pull (Vertical)' | P0 |
| program_builder.py calculate_reps_and_intensity | Add Olympic lift-specific progression rules | P1 |
| recommendation_engine.py | Add technical_difficulty and risk_score to ExerciseModel | P0 |
| recommendation_engine.py | Add minimum_training_age filter to get_ranked_exercises() | P0 |

### 8.5 New safety filters needed

```
class SafetyFilter:
    def check_olympic_lift_eligibility(athlete, exercise) -> tuple[bool, str]:
        checks:
        1. training_age >= exercise.min_training_age
        2. competition_level >= exercise.appropriate_level
        3. mobility_prerequisites_met (if applicable)
        4. no_contraindications (injury history, recent back issues)
        5. load_exposure_appropriate (has done regressions)
        return (passes, reason_if_failed)
```

---

## 9. Summary of P0 Actions

| # | Action | Current State | Target State |
|---|--------|--------------|--------------|
| 1 | Add Clean Pull | Not in system | DB entry + mock + fallback for Power Clean |
| 2 | Add Mid-Thigh Pull | Not in system | Highest cricket transfer Olympic lift |
| 3 | Add Hang Clean | Not in system | Catch mechanics progression |
| 4 | Add Overhead Squat | Not in system | Prerequisite for all snatch variants |
| 5 | Fix Power Clean movement pattern | Hinge only (mock) | Hinge (Primary) + Squat (Secondary) |
| 6 | Add Overhead Squat movement pattern | Not in system | Required for snatch family |
| 7 | Add training_age filter to engine | No filter | Minimum training age enforcement |
| 8 | Add risk_score to ExerciseModel | No risk data | Safety-based filtering |
| 9 | Add cricket transfer indices for all OL | Only 4 sports mapped | Cricket transfer index 0.30-0.75 |
| 10 | Replace Kettlebell Swing fallback | Unsafe/inappropriate | Clean Pull as primary Power Clean fallback |

---

## 10. Olympic Lift Readiness Score

| Dimension | Score (0-100) | Notes |
|-----------|--------------|-------|
| Exercise coverage | 7% | 1/14 exercises |
| Progression chains | 0% | 0/6 chains complete |
| Regression paths | 0% | 0/14 exercises have safe regressions |
| Movement taxonomy | 40% | Power Clean partially correct, 1 missing pattern |
| Safety filtering | 0% | No training age, risk, or mobility checks |
| Mock repo coverage | 7% | 1/14 in session_generator |
| Recommendation support | 0% | 0/14 in recommendation pools |
| Template integration | 10% | 1 template slot, incorrect fallback |
| Cricket-specific mapping | 0% | No cricket transfer indices |
| Progression rules | 0% | No OL-specific progression logic |

**Overall Olympic Lift Framework Readiness: 6.4%**

---

## Appendix A: Full Database Schema Required

### A.1 New columns needed

```sql
ALTER TABLE exercises ADD COLUMN technical_difficulty INTEGER CHECK (technical_difficulty BETWEEN 1 AND 10);
ALTER TABLE exercises ADD COLUMN risk_score INTEGER CHECK (risk_score BETWEEN 1 AND 5);
ALTER TABLE exercises ADD COLUMN minimum_training_age INTEGER DEFAULT 0;
```

### A.2 New movement pattern

```sql
INSERT INTO movement_patterns (name, description) VALUES
('Overhead Squat', 'Deep squat position maintaining a barbell in a locked-out overhead position.');
```

---

## Appendix B: Key References

- Comfort, P. et al. (2011). 'Are the clean pull and mid-thigh pull valid measures of athletic performance?' J Strength Cond Res.
- Suchomel, T.J. et al. (2018). 'The importance of muscular strength in athletic performance.' Sports Med.
- Hori, N. et al. (2008). 'Influence of load on force-time characteristics of the hang high pull.' J Strength Cond Res.
- ECB (2023). 'Fast Bowling Workload Guidelines.' England and Wales Cricket Board.
- Cricket Australia (2022). 'Australian Cricket Pathway: Physical Competencies Framework.'
- Comfort, P. & McMahon, J.J. (2015). 'The relationship between mid-thigh pull variables and sprint performance.' ISBS Proceedings.
