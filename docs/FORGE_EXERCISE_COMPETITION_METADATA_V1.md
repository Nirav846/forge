# FORGE Exercise Competition Metadata — V1.5

## Fields Added

| Field | Type | Range | Purpose |
|-------|------|-------|---------|
| `fatigue_cost` | int | 1-5 | Systemic fatigue from performing the exercise (CNS + muscular) |
| `impact_level` | int | 1-5 | Ground reaction / landing / collision forces |
| `eccentric_cost` | int | 1-5 | Muscle damage risk from eccentric loading |
| `competition_role` | str | enum | Functional role: strength, speed_power, accessory, core, carry |

## Inference Rules

Metadata is inferred at construction time in `data.py` via `_infer_exercise_comp_metadata()`.

### Process:
1. Start with family-level base values
2. Apply difficulty adjustments (diff ≥4 → +1 fatigue, +1 eccentric)
3. Apply explosive adjustment (+1 impact)
4. Apply isometric adjustment (eccentric=1, fatigue-1)
5. Apply named exercise overrides

## Per-Family Distributions

| Family | Fatigue Range | Impact Range | Eccentric Range | Role |
|--------|--------------|--------------|-----------------|------|
| DLKD | 2-5 | 3-4 | 1-4 | strength |
| DLHD | 3-5 | 3-4 | 3-5 | strength |
| SLKD | 3-4 | 3 | 3-4 | strength |
| SLHD | 3-4 | 3 | 3-5 | strength |
| HPush | 2-4 | 3-4 | 3-4 | strength |
| HPull | 3-4 | 3-4 | 3-4 | strength |
| VPush | 3-4 | 3-4 | 2-3 | strength |
| VPull | 3-4 | 3-4 | 3-4 | strength |
| Plyo | 3-4 | 4-5 | 2-4 | speed_power |
| Ball | 3-4 | 4-5 | 1-2 | speed_power |
| Sprint | 3-4 | 3-5 | 1-2 | speed_power |
| Rot | 1-2 | 2 | 1-2 | accessory |
| Carry | 1-3 | 2 | 1-2 | carry |
| Core | 1-2 | 1 | 1-2 | core |
| Acc | 1-2 | 2 | 1-2 | accessory |

## Significant Explicit Overrides

| Exercise | Override | Reason |
|----------|----------|--------|
| Barbell Back Squat | fatigue+1, impact+1 | Heavy bilateral with high load |
| Front Squat | fatigue+1 | Demands significant core/leg work |
| Conventional Deadlift | fatigue+1, impact+1, eccentric+1 | Heavy pull from floor |
| Trap Bar Deadlift | fatigue+1 | Heavy pull (but lower eccentric) |
| RDL | eccentric=5 | High hamstring stretch under load |
| Single-Leg RDL | eccentric=5 | Same as RDL, unilateral variant |
| Nordic Hamstring Curl | eccentric=5, fatigue=4 | Max eccentric, high DOMS |
| Good Morning | eccentric=5 | Spine under load, high eccentric |
| Stiff-Leg Deadlift | eccentric=5 | High hamstring eccentric |
| Depth Jump | impact=5, eccentric=4, fatigue=4 | Max landing forces |
| Full Sprints (Flying, Accel) | impact+2 | Max velocity running |
| Air Squat | fatigue-1, set to 2 | Bodyweight, minimal load |
| Wall Push-Up | fatigue-1, set to 2 | Bodyweight, minimal load |
| Push-Up | fatigue-1, set to 2 | Bodyweight |
| Incline Push-Up | fatigue-1, set to 2 | Bodyweight |
| Farmer/Suitcase Carry | fatigue=3 | Loaded carries, moderate fatigue |

## Low-Risk Exercises (Safe at All Windows)

63 exercises are low-risk (all metrics ≤2): all Core exercises, most Acc (prehab/activation), Pallof press variants, light carries. These pass at all competition windows including PRIMER.

## Why Each Field Matters

- **fatigue_cost**: Determines if an exercise is appropriate 2-3 days before competition (CNS/systemic recovery matters)
- **impact_level**: High impact = higher tissue stress and recovery requirement
- **eccentric_cost**: Directly correlates with DOMS and muscle damage. The most important filter for pre-competition sessions
- **competition_role**: Enables future role-based filtering (e.g., keep speed_power always, trim accessory first)
