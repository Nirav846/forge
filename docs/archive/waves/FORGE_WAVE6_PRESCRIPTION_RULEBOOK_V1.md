# FORGE Wave 6 — Prescription Rulebook

## Athlete-Profile-Driven Prescription Modifiers

The function `get_athlete_prescription_modifiers(profile, role)` returns a dict applied after blueprint + competition + week modifiers.

### Force / Velocity Profile

| Profile | Role Affected | Modifier |
|---|---|---|
| `force_deficient` | MAIN_STRENGTH | `rep_shift: "lower"` (6-8 → 5-7), `intensity_note_bias: ", heavy bias"`, `loading_bias: "heavier"` |
| `force_deficient` | EXPLOSIVE_POWER | `intensity_note_bias: ", strength-bias power"` |
| `force_deficient` | HYPERTROPHY_ACCESSORY | `set_cap: 3`, `intensity_note_bias: ", controlled"` |
| `velocity_deficient` | MAIN_STRENGTH | `intensity_note_bias: ", velocity-friendly"`, `loading_bias: "velocity"` |
| `velocity_deficient` | EXPLOSIVE_POWER | `intensity_note_bias: ", max intent velocity"`, `rep_shift: "lower"` |
| `velocity_deficient` | PLYOMETRIC | `intensity_note_bias: ", reactive focus"` |

### Landing Competency

| Profile | Role Affected | Modifier |
|---|---|---|
| `poor` | LANDING_MECHANICS | `set_cap: 3`, `intensity_note_bias: ", controlled stick focus"` |
| `poor` | PLYOMETRIC | `set_cap: 3`, `intensity_note_bias: ", low-reactive"` |

### Conditioning Profile

| Profile | Role Affected | Modifier |
|---|---|---|
| `poor` | CONDITIONING_LIFT, SPRINT_MECHANICS | `set_cap: 3`, `intensity_note_bias: ", submaximal density"` |

### Risk Flags

| Risk Flag | Role Affected | Modifier |
|---|---|---|
| `patellar_tendon_risk` | PLYOMETRIC | `set_cap: 2`, `intensity_note_bias: ", low-impact"` |
| `hamstring_risk` | SPRINT_MECHANICS | `set_cap: 3`, `intensity_note_bias: ", controlled exposure"` |
| `shoulder_overhead_risk` | EXPLOSIVE_POWER, SECONDARY_STRENGTH | `intensity_note_bias: ", overhead modified"` |
| `lumbar_risk` | MAIN_STRENGTH, SECONDARY_STRENGTH | `intensity_note_bias: ", lumbar-aware"` |

## Precedence Order (Wave 2 + Wave 6)

The prescription is built in this order — later steps override earlier:

1. **Base prescription table** (role × level × objective)
2. **Blueprint category modifiers** (`BLUEPRINT_PRESCRIPTION_MODIFIERS`)
3. **Competition window modifiers** (`COMP_WINDOW_MODIFIERS`)
4. **Week volume factors** (`WEEK_VOLUME_FACTORS`)
5. **Youth overrides** (cap sets at 3, no low-rep work)
6. **Wave 6: Athlete profile modifiers** ← *new*
7. **Wave 6: Role-based prescription modifiers** ← *new*

This means athlete/role personalization is the **final tuning layer**, respecting all safety and periodization constraints from Waves 1-4.

## Rep Shift Logic

`_shift_reps_lower("6-8")` → `"5-7"` (both ends shifted down by 1, min 1)

Examples:
- `"8-12"` → `"7-11"`
- `"3-5"` → `"3-4"`
- `"4-5"` → `"3-4"`

## Intensity Note Bias

Biases are **appended** to existing intensity note:
- Base: `"RPE 7-9"` + `", heavy bias"` → `"RPE 7-9, heavy bias"`
- Base: `"explosive, RPE 7-8"` + `", max intent velocity"` → `"explosive, RPE 7-8, max intent velocity"`

## Set Cap

Hard cap on maximum sets. Applied after all scaling:
- If base sets = `"4-5"` and `set_cap = 3` → `"3"`
