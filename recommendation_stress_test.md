# Recommendation Engine Stress Test Report

**Date:** 2026-06-15
**Synthetic Athletes:** 100
**Successful Prescriptions:** 100
**Failed Prescriptions (404/error):** 0

---

## Template Resolution Distribution

| Template | Count |
|----------|-------|
| Cricket Fast Bowler Power | 53 |
| Cricket Batter Strength/Power | 41 |
| Cricket Spinner Rotational Power | 30 |

## Failure Summary: 1814 total failures

| Category | Count | Affected Athletes |
|----------|-------|--------------------|
| 1. Empty Exercise Pools | 748 | 12 |
| 2. Duplicate Exercise Selection | 0 | 0 |
| 3. Same Exercise Multi-Slot | 0 | 0 |
| 4. Unsafe Olympic Lift | 0 | 0 |
| 5. High-Risk Exercise Leakage | 0 | 0 |
| 6. Invalid Progression | 0 | 0 |
| 7. Missing Default Exercises | 748 | 12 |
| 8. Invalid Swap Candidates | 305 | 12 |
| 9. Movement Category Mismatch | 13 | 13 |
| 10. Physical Driver Mismatch | 0 | 0 |

---
## Detailed Root Cause Analysis

### 1. Empty Exercise Pools

**Total occurrences:** 748

#### Sub-type: `GENERAL` (748 occurrences)

**Root cause:** 

- A1 (Batter, Beginner, Bodyweight Only, cap=Beginner, profile=Speed Only Deficit)
  → Slot 'Explosive Hinge/Extension' (Primary) has empty exercise pool
- A1 (Batter, Beginner, Bodyweight Only, cap=Beginner, profile=Speed Only Deficit)
  → Slot 'Unilateral Drive Strength' (Secondary) has empty exercise pool
- A1 (Batter, Beginner, Bodyweight Only, cap=Beginner, profile=Speed Only Deficit)
  → Slot 'Posterior Chain Knee Flexion' (Accessory) has empty exercise pool
- A1 (Batter, Beginner, Bodyweight Only, cap=Beginner, profile=Speed Only Deficit)
  → Slot 'Trunk Stability in Motion' (Core) has empty exercise pool
- A1001 (Batter, Beginner, Bodyweight Only, cap=Beginner, profile=Speed Only Deficit)
  → Slot 'Explosive Hinge/Extension' (Primary) has empty exercise pool
  ... and 743 more occurrences

### 2. Duplicate Exercise Selection

**No failures detected.**

### 3. Same Exercise Multi-Slot

**No failures detected.**

### 4. Unsafe Olympic Lift

**No failures detected.**

### 5. High-Risk Exercise Leakage

**No failures detected.**

### 6. Invalid Progression

**No failures detected.**

### 7. Missing Default Exercises

**Total occurrences:** 748

#### Sub-type: `GENERAL` (748 occurrences)

**Root cause:** 

The mock repo has no `default_exercise_id` concept. Slots either return a pool or None.
When no exercises match equipment + difficulty cap, the pool is empty with no fallback default.

**Root cause:** No `template_slots.default_exercise_id` column exists in current schema.
When filtering eliminates all candidates (e.g., Bodyweight-only for Barbell-required slot 302),
there is no guaranteed backup exercise to return.

- A1 (Batter, Beginner, Bodyweight Only, cap=Beginner, profile=Speed Only Deficit)
  → Slot 'Explosive Hinge/Extension' has no exercises at all (no default)
- A1 (Batter, Beginner, Bodyweight Only, cap=Beginner, profile=Speed Only Deficit)
  → Slot 'Unilateral Drive Strength' has no exercises at all (no default)
- A1 (Batter, Beginner, Bodyweight Only, cap=Beginner, profile=Speed Only Deficit)
  → Slot 'Posterior Chain Knee Flexion' has no exercises at all (no default)
- A1 (Batter, Beginner, Bodyweight Only, cap=Beginner, profile=Speed Only Deficit)
  → Slot 'Trunk Stability in Motion' has no exercises at all (no default)
- A1001 (Batter, Beginner, Bodyweight Only, cap=Beginner, profile=Speed Only Deficit)
  → Slot 'Explosive Hinge/Extension' has no exercises at all (no default)
  ... and 743 more occurrences

### 8. Invalid Swap Candidates

**Total occurrences:** 305

#### Sub-type: `GENERAL` (305 occurrences)

**Root cause:** 

Multiple slots have a pool size of exactly 1.

From the mock data:
- Slot 203 (Fast Bowler Accessory): Only 'Medicine Ball Overhead Backwards Toss'
- Slot 302 (Spinner Secondary): Only 'Barbell Back Squat'
- Slot 303 (Spinner Accessory): Only 'Dumbbell Overhead Press'
- Slot 403 (Batter Accessory): Only 'Dumbbell Row' or 'Nordic Hamstring Curl'
- Slot 401 (Batter Primary): Only 'Trap Bar Deadlift' or 'Kettlebell Swing'

**Root cause:** The mock only seeds 1-2 exercises per slot. A swap/replacement would
return the same exercise, making exercise variation impossible within a program.

- A1001 (Batter, Beginner, Bodyweight Only, cap=Beginner, profile=Speed Only Deficit)
  → Slot 'Trunk Stability in Motion' has only 1 exercise ('Plank with Rotation') - swap would produce no change
- A1001 (Batter, Beginner, Bodyweight Only, cap=Beginner, profile=Speed Only Deficit)
  → Slot 'Trunk Stability in Motion' has only 1 exercise ('Plank with Rotation') - swap would produce no change
- A1002 (Fast Bowler, Elite, Bodyweight Only, cap=Intermediate, profile=All Poor)
  → Slot 'Unilateral Force Production' has only 1 exercise ('Single-Leg Lateral Bound') - swap would produce no change
- A1003 (Batter, Intermediate, Bodyweight Only, cap=Intermediate, profile=Rotational Only Deficit)
  → Slot 'Trunk Stability in Motion' has only 1 exercise ('Plank with Rotation') - swap would produce no change
- A1003 (Batter, Intermediate, Bodyweight Only, cap=Intermediate, profile=Rotational Only Deficit)
  → Slot 'Trunk Stability in Motion' has only 1 exercise ('Plank with Rotation') - swap would produce no change
  ... and 300 more occurrences

### 9. Movement Category Mismatch

**Total occurrences:** 13

#### Sub-type: `PATTERN_DUPLICATE` (13 occurrences)

**Root cause:** 

The mock exercises have force_type values that may not match slot expectations:
- Trap Bar Jump Squat (force_type='Push') used in Primary slots — correct for bilateral power
- Single-Leg Lateral Bound (force_type='Push') used in Secondary — correct for unilateral
- Medicine Ball Overhead Backwards Toss (force_type='Hinge') in Accessory — plausible but atypical

The session generator's pattern duplication check revealed: 
Bodyweight Squat (Squat), A-Skip (Sprint Mechanics), Single-Leg Wall Sit (Static Stability) all have unique patterns.

**Root cause:** force_type taxonomy is inconsistent — 'Push' is used for both vertical jumps AND horizontal bounds.
'Static' force type on Medicine Ball Rotational Scoop Toss is incorrect (should be 'Rotation').

- A6 (session, Fast Bowler, cap=Beginner)
  → Duplicate movement pattern 'Rotation' in session sections
- A8 (session, Spinner, cap=Intermediate)
  → Duplicate movement pattern 'Rotation' in session sections
- A11 (session, Fast Bowler, cap=Beginner)
  → Duplicate movement pattern 'Rotation' in session sections
- A12 (session, Fast Bowler, cap=Intermediate)
  → Duplicate movement pattern 'Rotation' in session sections
- A17 (session, Spinner, cap=Beginner)
  → Duplicate movement pattern 'Rotation' in session sections
  ... and 8 more occurrences

### 10. Physical Driver Mismatch

**No failures detected.**

---
## Overall Assessment

**Total unique source athletes with failures:** 100

### Criticality Ranking

| Rank | Category | Impact | Fix Priority |
|------|----------|--------|-------------|
| 1 | Empty Exercise Pools | Athlete gets NO prescription | P0 - Blocks athlete care |
| 2 | Invalid Swap Candidates | No exercise variety in programs | P0 - Training stagnation |
| 3 | Unsafe Olympic Lift | Injury risk for beginners | P1 - Safety critical |
| 4 | High-Risk Leakage | Eccentric/plyometric injury | P1 - Safety critical |
| 5 | Same Exercise Multi-Slot | Duplicate across template | P2 - Quality of prescription |
| 6 | Missing Default | No fallback for empty pools | P2 - Reliability |
| 7 | Movement Category Mismatch | Wrong exercise in slot | P2 - Quality of prescription |
| 8 | Physical Driver Mismatch | Exercise doesn't target driver | P2 - Quality of prescription |
| 9 | Invalid Progression | Wrong progression type | P3 - S&C science accuracy |
| 10 | Duplicate Exercise Selection | Same exercise in multiple slots | P3 - Nuisance |