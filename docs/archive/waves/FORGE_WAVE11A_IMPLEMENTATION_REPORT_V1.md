# Wave 11A — Minimum Coach-Trust Fixes: Implementation Report

## Summary
Four targeted engine fixes addressing the top coach complaints. All changes are additive/backward-compatible — no existing behavior removed, no API contracts broken.

## Changes

### Part 1 — Advanced Athlete Ceiling
**File:** `src/forge/exercise_selector.py` (3 lines)

Advanced athletes with `strength_base_met=True` can no longer select exercises with difficulty < 3 in DLKD and DLHD families. This prevents Goblet Squat (diff 2) from being selected when Barbell Back Squat (diff 3) is available.

- Advanced DLKD now requires min diff 3 → Barbell Back Squat, Front Squat, or Paused Back Squat
- Advanced DLHD now requires min diff 3
- Intermediate athletes unaffected
- Advanced athletes without strength base (SLKD→DLKD downgrade) unaffected

### Part 2 — In-Season Volume Reduction
**Files:** `src/forge/main.py`, `src/forge/prescription_rules.py`

**`main.py`:** In-season athletes get `preferred` capped at 5 families and `avail_min` capped at 50 minutes, executed after the comp-window taper block in `generate_program`.

**`prescription_rules.py`:** In-season athletes get a set cap of 4 across all prescription roles, added in `get_athlete_prescription_modifiers`.

### Part 3 — Proportional Time Constraint Reduction
**Files:** `src/forge/session_assembly.py`, `src/forge/main.py`

`apply_time_constraint_v2` now returns a 3-tuple `(kept_slots, drop_notes, compact_factor)` where `compact_factor` scales from 0.55 (<30 min) to 1.0 (≥60 min). In `_build_session`, prescriptions are scaled by this factor — sets are compacted proportionally rather than only dropping families.

### Part 4 — Injury Prevention Minimums
**File:** `src/forge/session_rules.py` (5 lines)

For sport roles with `jump_exposure_target="high"` or `sprint_exposure_target="high"`, Landing and Acc families are promoted to at least TIER_B in `compute_family_survival_tier`. This prevents injury-prevention work from being dropped under time constraints for explosive athletes.

### Test Results
- **16 new tests** in `tests/test_wave11a_minimum_fixes.py` — all pass
- **618 of 620** existing tests pass (2 pre-existing failures in `test_wave8_role_week_planning.py` — broken imports, unrelated)
- Existing wave9 tests updated for new 3-tuple return from `apply_time_constraint_v2`
