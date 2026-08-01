# FORGE Wave 5 — Implementation Report

## Files Changed

| File | Change |
|---|---|
| `src/forge/models.py` | Added 14 optional fields to `AthleteProfile` (bodyweight_kg, position_role, force_profile, elastic_profile, conditioning_profile, landing_competency, sprint_mechanics_competency, 6x risk flags, 4x test bands). Added `personalization_notes` to `GeneratedProgram`. |
| `src/forge/athlete_profile_rules.py` | **New module** — 170 lines containing: `get_exercise_personalization_bias()`, `is_exercise_risk_flagged()`, `filter_exercises_for_athlete()`, `score_exercise_for_athlete()`, `personalize_exercise_list()`, `score_conditioning_for_athlete()`, `get_weekly_emphasis_bias()`, `describe_weekly_bias()`. |
| `src/forge/exercise_selector.py` | Added `athlete_profile` parameter to `select_exercise()`. Risk filtering + personalization bias in candidate selection. Added `_recent_score()` helper. |
| `src/forge/substitution_engine.py` | Added `athlete_profile` parameter to `substitute_exercise()`. Risk filtering at all 3 priority levels. |
| `src/forge/progression_engine.py` | Added `athlete_profile` parameter to `select_or_continue()` and `progress_conditioning()`. Passed through to `select_exercise()` and `select_conditioning()`. Added 4 Wave 5 validator checks: `_check_landing_risk()`, `_check_lumbar_risk()`, `_check_shoulder_risk()`, `_check_hamstring_risk()`. |
| `src/forge/conditioning_engine.py` | Added `athlete_profile` parameter to `generate_conditioning()` and `select_conditioning()`. Personalization score added to conditioning protocol ranking. |
| `src/forge/main.py` | Integrated `get_weekly_emphasis_bias()` + `describe_weekly_bias()` into `generate_program()`. Passes `athlete_profile` through all exercise/conditioning calls. Stores `personalization_notes` on `GeneratedProgram`. |
| `src/forge/renderer.py` | Added personalization notes display to `render_coach_program()` and `render_block_summary()`. |
| `tests/test_wave5_personalization.py` | **New test file** — 46 tests in 6 categories. |

## What Each Part Delivered

### Part 1 — Athlete Profile Input Layer
- 14 new optional fields on `AthleteProfile` covering 4 domains: anthropometry, performance profile, risk flags, test bands
- All fields have sensible defaults (None or False) — zero breaking changes to existing code
- `GeneratedProgram.personalization_notes` stores coach-readable explanation of profile-driven decisions

### Part 2 — Exercise Personalization Rules
- Risk filtering: 6 risk flags with deterministic exercise-blocking rules based on family, difficulty, eccentric_cost, impact_level, and exercise name patterns
- Performance bias: force/velocity profile, elastic/landing/sprint competency all produce -1/0/+1 scoring on exercise candidates
- Substitution engine also risk-aware — all 3 priority levels filter before returning
- Backward compatible: `athlete_profile=None` produces identical behavior to pre-Wave-5

### Part 3 — Conditioning Personalization Rules
- Conditioning profile bias: poor-conditioning athletes pushed toward lower-fatigue protocols, strong-conditioning athletes allowed denser work
- Risk-aware conditioning: hamstring risk penalizes RSA/speed endurance; groin risk penalizes COD; lumbar risk penalizes gym env; tendon risk penalizes high-impact protocols
- Optional test band bias: sprint_10m_band and aerobic_band slightly influence protocol preference
- Applied as additive score within existing movement-profile + tier ranking

### Part 4 — Weekly Focus Bias & Program-Level Personalization
- `get_weekly_emphasis_bias()` produces a small dict of Boolean bias flags
- `describe_weekly_bias()` converts to human-readable notes
- Bias flags include: more_lower_strength, more_explosive_emphasis, more_landing_prep, less_plyo_density, less_hinge_rotation, less_overhead, more_sprint_drills, less_sprint_density, less_impact_cond, less_lateral_cod
- Notes stored on program and shown in coach output

### Part 5 — Coach-Facing Personalization Summary + Validation
- Renderer: `render_coach_program()` and `render_block_summary()` both show personalization notes
- Validator: 4 new program-level checks for risk-rule compliance:
  - `landing_risk_respected`: poor-landing athlete must not have Plyo/Landing >= d:4
  - `lumbar_risk_respected`: lumbar-risk athlete must not have excessive high-eccentric hinge/rotation
  - `shoulder_risk_respected`: shoulder-risk athlete must not have excessive overhead loading
  - `hamstring_risk_respected`: hamstring-risk athlete must not have reckless sprint density per week

## Test Count

- **402 tests pass** (312 pre-Wave-1 + 44 Wave 4 + 46 Wave 5)
- **0 regression** from existing test suite
- **2 pre-existing failures** unchanged (LevelDetermination, IntentCategories)
- **46 Wave 5 tests** across 6 categories:
  - Profile backward compatibility (4)
  - Exercise personalization (19)
  - Conditioning personalization (8)
  - Weekly bias (7)
  - Renderer/validator (6)
  - Competition interaction (2)

## Coach-Visible Changes

A coach reading a program after Wave 5 will see at the top:

```
Personalization Notes:
  Force-deficient profile -> increased lower-strength emphasis
  Landing competency poor -> advanced reactive plyos capped; landing prep added
  Lumbar risk -> high-eccentric hinges reduced; rotation exposure moderated
```

The block summary shows the same notes. The exercises themselves differ — a force-deficient athlete gets more bilateral squat/hinge exposure relative to explosive work, a poor-landing athlete gets basic landing sticks instead of depth jumps, and a lumbar-risk athlete sees no RDL or Good Morning in the program.

## "Do two athletes on the same blueprint now receive meaningfully different programs for good coaching reasons?"

**Yes.** Two tennis athletes on the Court Sport Athletic Development blueprint will now receive different programs if their profiles differ:

- **Athlete A** (force_deficient, poor landing competency, lumbar_risk):
  - More lower-strength emphasis (more squat/hinge volume relative to plyo)
  - Landing capped to Box Jump Stick low/moderate — no depth jumps
  - No RDL, Good Morning, or heavy rotational throws
  - Conditioning de-prioritizes high-impact field work
  - Personalization notes explain each modification

- **Athlete B** (velocity_deficient, strong elastic profile, healthy):
  - More explosive/power emphasis (more plyo, ballistic, sprint work)
  - Full landing progression available (including reactive SL landings)
  - No exercise restrictions — full DLHD/Rot selection
  - Conditioning can include higher-density court work
  - Personalization notes explain the velocity-deficient emphasis

Both programs remain credible, both respect the same blueprint structure, but the exercise selection, volume distribution, and conditioning routing are athlete-specific in ways a real S&C coach would recognize.

## Biggest Remaining Gap After Wave 5

### No Exercise Progression/Autoregulation Within Blocks
Wave 5 personalizes exercise *selection* but does not autoregulate exercise *prescription* within a block. A force-deficient athlete might get more squat slots, but the sets/reps/loading for those squats do not differ from a velocity-deficient athlete's squat prescription.

**When to close this gap**: When the prescription engine (`prescription_rules.py`) can accept athlete profile inputs to modify loading parameters (more volume for force-deficient, more intensity for velocity-deficient, etc.).

### No Position/Role-Specific Programming
`position_role` exists in the model but is unused. A rugby forward and a rugby back on the same blueprint still get identical programs. Real S&C coaches differentiate by position (more scrum/contact work for forwards, more speed/evasion for backs).

**When to close this gap**: When blueprint selection or slot resolution can be modified by position_role. Small change — modify blueprint selection to favor different optional families based on position.

### Test Bands Not Fully Wired
Four test band fields exist but only `sprint_10m_band` and `aerobic_band` affect conditioning selection. `cmj_band` and `squat_strength_band` are data-model-only. A full implementation would use these to modify explosive exercise selection and strength loading zones.

**When to close this gap**: When an objective testing subsystem exists that can populate these fields.
