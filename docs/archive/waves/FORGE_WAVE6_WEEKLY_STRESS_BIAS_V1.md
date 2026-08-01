# FORGE Wave 6 — Weekly Stress Bias

## How Weekly Stress Is Modified

Wave 6 adds a lightweight weekly stress bias layer that responds to athlete profile + role + risk. This is **not a new planning engine** — it's a bias layer on top of Wave 4 + Wave 5.

### Inputs

| Source | Fields |
|---|---|
| Athlete profile | force_profile, elastic_profile, conditioning_profile, landing_competency, sprint_mechanics_competency |
| Risk flags | lumbar_risk, patellar_tendon_risk, hamstring_risk, shoulder_overhead_risk, groin_adductor_risk, ankle_foot_risk |
| Role | position_role (sport-specific) |

### Bias Computation

1. **Base bias** from `get_weekly_emphasis_bias(profile)` (Wave 5)
2. **Role notes** from `get_role_weekly_notes(sport, role)` (Wave 6)
3. **Prescription notes** from `describe_prescription_modifiers()` (Wave 6)

All combined into `GeneratedProgram.personalization_notes`.

### Example Outputs

| Athlete | Profile + Role | Weekly Stress Bias |
|---|---|---|
| Force-deficient prop | `force_deficient` + `prop` | More lower-strength emphasis; maximal force emphasis; plyo density reduced |
| Velocity-deficient winger | `velocity_deficient` + `backline` | Velocity-friendly loading; max velocity sprint emphasis; reactive plyo emphasis |
| Fast bowler with lumbar risk | `lumbar_risk=True` + `fast_bowler` | Sprint emphasis preserved; hinge dosing lumbar-aware; shoulder support |
| Poor landing volleyball middle | `landing_competency=poor` + `middle` | Jump work stays; reactive exposure capped; landing prep increased |
| Hamstring-risk forward | `hamstring_risk=True` + `forward` | Sprint exposure remains; density constrained; finishing power emphasis |

### Exposure Cap Logic

No new exposure engine — existing Wave 3/4 weekly exposure guards still run. Wave 6 only affects **what prescriptions are generated**, which indirectly affects exposure counts.

The existing `weekly_exposure_warnings()` in `progression_engine.py` still catches dangerous accumulations regardless of personalization.

### Coach-Visible Summary

In `render_block_summary()`, the personalization notes appear as:

```
Personalization:
  Force-deficient profile -> lower-rep strength prescriptions; heavier loading bias
  Prop role -> maximal force & collision robustness emphasis
  Lumbar risk -> hinge dosing lumbar-aware; spinal loading moderated
```

These notes explain **why** the week looks different from a generic program.
