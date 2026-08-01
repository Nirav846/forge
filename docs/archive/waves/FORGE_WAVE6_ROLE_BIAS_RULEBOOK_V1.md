# FORGE Wave 6 — Role Bias Rulebook

## Exercise Selection Bias by Role

`get_role_exercise_bias(role_key, family, sport)` returns -2 to +2 bias score.

### Cricket

| Role | Preferred (+1/+2) | Avoided (-1/-2) |
|---|---|---|
| `fast_bowler` | DLKD, SLKD, SLHD, Sprint, Landing, Core, Acc | DLHD, Rot, VPush |
| `spinner` | Rot, Core, HPush, HPull | Sprint |
| `batter` | Rot, Ball, HPush, HPull, Sprint | — |
| `wicketkeeper` | DLKD, SLKD, Core, Rot, Landing | Sprint, Plyo |

### Rugby

| Role | Preferred (+1/+2) | Avoided (-1/-2) |
|---|---|---|
| `prop` | DLKD(+2), DLHD, HPush(+2), HPull, Core(+2), Carry(+2) | Plyo, Sprint |
| `lock` | DLKD(+2), DLHD, Plyo, Landing, HPush, Core, Carry | — |
| `back_row` | DLKD, DLHD, Sprint, Core, Carry | — |
| `halfback` | Sprint, Ball, SLKD, SLHD, Core | — |
| `backline` | Sprint(+2), Plyo, Ball | DLKD |

### Tennis

| Role | Preferred | Avoided |
|---|---|---|
| `singles` | Sprint, Landing, SLKD, SLHD, Core, Rot | VPush |
| `doubles` | Plyo, Ball, VPush, VPull | Sprint |

### Badminton

| Role | Preferred | Avoided |
|---|---|---|
| `singles` | Sprint, Landing, SLKD(+2), SLHD, Core | — |
| `doubles` | Plyo, Ball, VPush, VPull, SLKD | — |

### Volleyball

| Role | Preferred | Avoided |
|---|---|---|
| `middle` | Plyo(+2), Landing(+2), DLKD, VPush, VPull, Core | — |
| `outside` | Plyo, Landing, HPush, HPull, Rot, Core | — |
| `setter` | SLKD, SLHD, Core | VPush, Sprint |
| `libero` | Landing, SLKD, SLHD, Sprint | VPush, VPull |

### Soccer / Football

| Role | Preferred | Avoided |
|---|---|---|
| `goalkeeper` | Plyo(+2), Landing(+2), Ball, SLKD, SLHD | VPush, VPull, Sprint |
| `defender` | DLKD, DLHD, Sprint, Core, Carry | — |
| `midfielder` | Sprint, SLKD, SLHD, Core | — |
| `forward` | Sprint(+2), Plyo, Ball, Landing | DLKD |

## Role-Based Prescription Modifiers

`get_role_prescription_modifiers(role_key, sport, prescription_role)` returns modifiers applied after athlete profile.

### Cricket

| Role | Prescription Role | Modifier |
|---|---|---|
| `fast_bowler` | MAIN_STRENGTH | `intensity_note_bias: ", lumbar-aware hinge dosing"` |
| `fast_bowler` | SPRINT_MECHANICS | `intensity_note_bias: ", submaximal sprint density"` |
| `fast_bowler` | EXPLOSIVE_POWER | `intensity_note_bias: ", shoulder-friendly loading"` |
| `spinner` | EXPLOSIVE_POWER | `intensity_note_bias: ", rotational power emphasis"` |
| `batter` | EXPLOSIVE_POWER | `intensity_note_bias: ", rotational power emphasis"` |

### Rugby

| Role | Prescription Role | Modifier |
|---|---|---|
| `prop` | MAIN_STRENGTH | `intensity_note_bias: ", maximal force emphasis"` |
| `prop` | SECONDARY_STRENGTH | `set_cap: 3` |
| `prop` | PLYOMETRIC | `set_cap: 3` |
| `lock` | PLYOMETRIC | `intensity_note_bias: ", jump-landing control"` |
| `back_row` | SPRINT_MECHANICS | `intensity_note_bias: ", repeat sprint focus"` |
| `backline` | SPRINT_MECHANICS | `intensity_note_bias: ", max velocity"` |
| `backline` | PLYOMETRIC | `intensity_note_bias: ", reactive emphasis"` |

### Tennis

| Role | Prescription Role | Modifier |
|---|---|---|
| `singles` | SPRINT_MECHANICS | `set_cap: 3` |
| `singles` | CONDITIONING_LIFT | `intensity_note_bias: ", court conditioning density"` |
| `doubles` | EXPLOSIVE_POWER | `intensity_note_bias: ", first-step emphasis"` |

### Volleyball

| Role | Prescription Role | Modifier |
|---|---|---|
| `middle` | PLYOMETRIC | `intensity_note_bias: ", block-jump loading"` |
| `middle` | LANDING_MECHANICS | `intensity_note_bias: ", repeated landing control"` |
| `libero` | LANDING_MECHANICS | `intensity_note_bias: ", lateral coverage"` |
| `libero` | SPRINT_MECHANICS | `set_cap: 3`, `intensity_note_bias: ", short-burst"` |

### Soccer

| Role | Prescription Role | Modifier |
|---|---|---|
| `goalkeeper` | PLYOMETRIC | `intensity_note_bias: ", lateral dive loading"` |
| `goalkeeper` | LANDING_MECHANICS | `intensity_note_bias: ", diving landing control"` |
| `midfielder` | SPRINT_MECHANICS | `intensity_note_bias: ", repeat running"` |
| `midfielder` | CONDITIONING_LIFT | `intensity_note_bias: ", conditioning support"` |
| `forward` | SPRINT_MECHANICS | `intensity_note_bias: ", max acceleration"` |
| `forward` | PLYOMETRIC | `intensity_note_bias: ", finishing power"` |

## Weekly Emphasis Notes

`get_role_weekly_notes(sport, role)` returns human-readable notes for coach output.

Examples:
- `fast_bowler` → "Fast bowler role -> sprint & unilateral emphasis; lumbar-friendly hinge dosing"
- `prop` → "Prop role -> maximal force & collision robustness emphasis"
- `singles` (tennis) → "Singles role -> court conditioning & repeat COD emphasis"
- `libero` (volleyball) → "Libero role -> lateral coverage & low-overhead bias"

## Stacking Rules

When multiple modifiers apply (profile + role + risk):
1. **Set cap**: Most restrictive cap wins (min of all caps)
2. **Intensity note**: All biases concatenated with comma separation
3. **Rep shift**: Only one shift applied (force profile takes precedence)
4. **Loading bias**: Only one loading bias (force/velocity profile takes precedence)
