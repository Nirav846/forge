# FORGE Wave 4 — Program-Level Validation

## New Checks (Added in Wave 4)

| Check Key                        | What It Verifies                                                                 | Pass/Fail Example                                                                 |
|----------------------------------|----------------------------------------------------------------------------------|-----------------------------------------------------------------------------------|
| `movement_balance_ok`            | At least 2 of 4 major patterns (squat, hinge, push, pull) have 2+ appearances per week across the block | **Pass**: squat appears 16x, hinge appears 12x across 8 weeks → 2 patterns met<br>**Fail**: only squat appears → only 1 pattern met |
| `sprint_landing_bounded`         | No more than 3 weeks in the block have >3 high-impact exercises                  | **Pass**: 2 weeks exceed threshold<br>**Fail**: 5 weeks exceed threshold |
| `conditioning_not_dominant`      | Conditioning appears in ≤75% of sessions for non-conditioning goals              | **Pass**: strength program has conditioning in 12/32 sessions (37%)<br>**Fail**: strength program has conditioning in 28/32 sessions (87%) |
| `core_rotational_present`        | Core or rotational exercises appear at least once in the entire block            | **Pass**: Plank appears in at least 1 session<br>**Fail**: No core/rotational exercise in any session |
| `test_not_max_loading`           | Test weeks (sessions with `testing_categories`) have ≤8 exercises per session    | **Pass**: test session has 6 exercises<br>**Fail**: test session has 10 exercises |
| `exposure_bounded_across_block`  | No more than 2 weeks in the block trigger high-eccentric warnings                | **Pass**: 1 week triggers eccentric warning<br>**Fail**: 4 weeks trigger eccentric warning |

## Total Check Count

Wave 4 raises the program-level check count from **7** to **14** (7 Wave 3 + 6 Wave 4 + 1 placeholder).

## Score Impact

All 14 checks feed into `calculate_program_credibility_score()`. A perfect program scores 1.0. The credibility score is now visible at both the session level and program level.

## What a Coach Would See

Before Wave 4, `verify_program_credibility()` returned:
```
main_lift_continuity: True,
block_progression_visible: True,
deload_week_actually_reduced: True,
weekly_exposure_safe: True,
...
```

After Wave 4:
```
main_lift_continuity: True,
block_progression_visible: True,
...
movement_balance_ok: True,
sprint_landing_bounded: True,
conditioning_not_dominant: True,
core_rotational_present: True,
test_not_max_loading: True,
exposure_bounded_across_block: True,
```
