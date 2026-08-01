# FORGE Wave 6 — Implementation Report

## Files Changed

| File | Change |
|---|---|
| `src/forge/prescription_rules.py` | Added `get_athlete_prescription_modifiers()`, `get_role_prescription_modifiers()`, `describe_prescription_modifiers()`, `_merge_presc_mods()`, `_shift_reps_lower()`. Modified `get_prescription()` to accept `athlete_profile` and apply Wave 6 modifiers. |
| `src/forge/athlete_profile_rules.py` | Added `get_role_exercise_bias()`, `_ROLE_EXERCISE_BIAS` dict (moved from prescription_rules), `get_role_prescription_modifiers()`, `describe_prescription_modifiers()`, `ROLE_WEEKLY_NOTES`, `get_role_weekly_notes()`. |
| `src/forge/main.py` | Updated `get_prescription()` calls to pass `athlete_profile=athlete`. Added role notes and prescription personalization notes to `personalization_notes`. |
| `src/forge/validator.py` | Added `prescription_athlete_aware` and `role_bias_applied` checks to `verify_credibility()`. Fixed `divisor` calculation bug. |
| `src/forge/renderer.py` | Already had personalization notes display (from Wave 5) — works with new notes. |
| `tests/test_wave6_prescription_personalization.py` | **New** — 20 tests in 6 categories. |

## What Each Part Delivered

### Part 1 — Prescription Personalization Layer
- `get_athlete_prescription_modifiers(profile, role)` returns deterministic modifiers
- Applied to sets, reps, intensity_note, loading_bias after all existing modifiers
- Force/velocity profile shifts rep ranges and intensity notes
- Landing competency caps plyo/landing sets
- Conditioning profile adjusts density
- Risk flags modify dosing (patellar, hamstring, shoulder, lumbar)

### Part 2 — Role/Position-Specific Bias Layer
- `_ROLE_EXERCISE_BIAS` dict: 5 sports × 20 roles × 14 families with -2 to +2 bias
- `get_role_exercise_bias()` used by exercise selector for role-aware selection
- `get_role_prescription_modifiers()` applies role-specific prescription tweaks
- `ROLE_WEEKLY_NOTES`: coach-readable weekly emphasis per sport/role

### Part 3 — Prescription Modifier Rules by Role
- Role modifiers stack safely with profile modifiers via `_merge_presc_mods()`
- Precedence: base → blueprint → comp window → week volume → youth → profile → role
- Set caps take most restrictive; intensity notes concatenate

### Part 4 — Weekly Stress Bias & Exposure Controls
- `personalization_notes` on `GeneratedProgram` now includes:
  - Wave 5 profile/risk bias notes
  - Wave 6 role weekly notes
  - Wave 6 prescription personalization notes
- Rendered in `render_coach_program()` and `render_block_summary()`
- Existing Wave 3/4 exposure guards unchanged

### Part 5 — Coach Output + Validation Hardening
- Coach output shows: "Force-deficient profile → lower-rep strength prescriptions; heavier loading bias"
- Coach output shows: "Prop role → maximal force & collision robustness emphasis"
- Validator checks: `prescription_athlete_aware` (force-deficient not getting high-rep strength)
- Validator checks: `role_bias_applied` (role provided = bias applied)

## Test Count

- **422 tests pass** (402 pre-Wave-6 + 20 Wave 6)
- **0 regression** from existing test suite
- **2 pre-existing failures** unchanged (LevelDetermination, IntentCategories)
- **20 Wave 6 tests** across 6 categories:
  - Prescription personalization by athlete profile (7)
  - Role-specific bias (5)
  - Renderer/validator integration (3)
  - Same blueprint divergence (3)
  - Backward compatibility (3)

## Coach-Visible Changes

A coach reading a program after Wave 6 will see:

```
Personalization Notes:
  Force-deficient profile -> lower-rep strength prescriptions; heavier loading bias
  Prop role -> maximal force & collision robustness emphasis
  Lumbar risk -> hinge dosing lumbar-aware; spinal loading moderated
```

And the **same exercise** gets different dosing:
- Force-deficient athlete: DLKD-004 → `sets: "4", reps: "5-7", intensity: "RPE 7-9, heavy bias"`
- Velocity-deficient athlete: DLKD-004 → `sets: "4", reps: "6-8", intensity: "RPE 7-9, velocity-friendly"`

**This is the key difference from Wave 5**: Wave 5 changed *which exercise*; Wave 6 changes *how the exercise is dosed*.

## "Do two athletes on the same blueprint now receive different prescriptions — not just different exercises — for good coaching reasons?"

**Yes.**

| Athlete | Blueprint | MAIN_STRENGTH Dosing |
|---|---|---|
| Force-deficient prop | Strength | `5-7 reps, heavy bias, maximal force emphasis` |
| Velocity-deficient backline | Strength | `6-8 reps, velocity-friendly, max velocity sprint` |
| Poor-landing middle (volleyball) | Court Sport | `plyo set_cap: 3, low-reactive, block-jump loading` |
| Singles tennis player | Court Sport | `sprint set_cap: 3, court conditioning density` |

All programs remain credible, respect blueprint identity, and pass validator checks. The coach sees *why* the dosing differs and can verify it matches their intent.

## Biggest Remaining Gap After Wave 6

### No Mesocycle/Block Autoregulation
Wave 6 personalizes within an 8-week block but doesn't autoregulate **block-to-block** based on prior block performance. A force-deficient athlete who responds well still gets the same progression pattern next block.

**When to close**: When FORGE supports rolling programs with performance feedback loops.

### No Position-Specific Periodization
Role bias affects exercise selection and prescription, but **week structure** (accumulation/intensification/realization) is still blueprint-driven, not role-driven. A prop and a backline player on the same blueprint get the same week types.

**When to close**: When blueprint selection or week planning incorporates role.

### Limited Test Band Integration
`cmj_band`, `sprint_10m_band`, `squat_strength_band`, `aerobic_band` exist on AthleteProfile but only `sprint_10m_band` and `aerobic_band` affect conditioning selection. They don't yet influence prescription dosing.

**When to close**: When objective testing data is available to drive loading zones.

### No Loading Zone Precision
Prescriptions still use RPE ranges (`RPE 7-9`) rather than %1RM. For precision loading, %1RM with velocity-based adjustments would be needed.

**When to close**: When FORGE integrates velocity-based training or 1RM tracking.
