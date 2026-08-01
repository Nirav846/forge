# FORGE Wave 5 — Personalization Rulebook

## Athlete Profile Fields

### Anthropometry / Training Background

| Field | Type | Default | Valid Values | What It Changes |
|---|---|---|---|---|
| `bodyweight_kg` | Optional[float] | None | Any positive float | Reserved for future load prescription scaling |
| `position_role` | str | "" | Any string (e.g. "forward", "midfielder") | Sport-specific notes for coach visibility |

### Performance Profile Flags

| Field | Type | Default | Valid Values | What It Changes |
|---|---|---|---|---|
| `force_profile` | Optional[str] | None | "force_deficient", "velocity_deficient", "balanced" | Exercise bias: force-deficient prefers strength families, velocity-deficient prefers explosive families |
| `elastic_profile` | Optional[str] | None | "poor", "average", "strong" | Plyo/ballistic exercise bias: poor avoids advanced plyos, strong allows reactive variants |
| `conditioning_profile` | Optional[str] | None | "poor", "average", "strong" | Conditioning protocol selection: poor prefers low-fatigue protocols, strong allows dense protocols |
| `landing_competency` | Optional[str] | None | "poor", "average", "strong" | Landing/plyo exercise choice: poor caps reactive plyos and prefers basic landing prep |
| `sprint_mechanics_competency` | Optional[str] | None | "poor", "average", "strong" | Sprint exercise choice: poor gets more drill-based work, strong allows max-velocity sprinting |

### Risk / Tolerance Flags

| Field | Type | Default | What It Changes |
|---|---|---|---|
| `lumbar_risk` | bool | False | Reduces high-eccentric hinge selection (RDL, Good Morning, stiff-leg variants); caps heavy rotational loading; avoids heavy spinal compression (back squat, front squat at high difficulty) |
| `patellar_tendon_risk` | bool | False | Caps depth landings (Landing difficulty >= 3), advanced plyos (difficulty >= 4), depth/drop squat variants |
| `hamstring_risk` | bool | False | Reduces high-eccentric hinge selection (RDL, Good Morning, etc.); caps max-velocity sprint exposure (difficulty >= 4) |
| `shoulder_overhead_risk` | bool | False | Modifies overhead press selection (VPush difficulty >= 3 blocked); caps heavy pull-up variants |
| `groin_adductor_risk` | bool | False | Reduces lateral COD sprint exposure (lateral shuffle, crossover); caps lateral single-leg work |
| `ankle_foot_risk` | bool | False | Caps advanced plyos (difficulty >= 4), single-leg landings (difficulty >= 4), max-velocity sprinting |

### Optional Test-Derived Tags

| Field | Type | Default | Valid Values | What It Changes |
|---|---|---|---|---|
| `cmj_band` | Optional[str] | None | "low", "avg", "high" | Reserved for future power emphasis |
| `sprint_10m_band` | Optional[str] | None | "low", "avg", "high" | Conditioning bias: low reduces alactic speed / speed endurance protocol preference |
| `squat_strength_band` | Optional[str] | None | "low", "avg", "high" | Reserved for future loading prescription |
| `aerobic_band` | Optional[str] | None | "low", "avg", "high" | Conditioning bias: low reduces aerobic capacity/power protocol preference |

## Engine Changes by Field

| Field | Exercise Selection | Conditioning Selection | Weekly Bias | Renderer | Validator |
|---|---|---|---|---|---|
| force_profile | +1/-1 bias on strength vs explosive families | — | more_lower_strength | Shown in notes | — |
| elastic_profile | +1/-1 bias on plyo/ballistic | — | — | Shown in notes | — |
| conditioning_profile | — | Fatigue-score bias | — | Shown in notes | — |
| landing_competency | -2 on advanced landings, -1 on high-impact plyos | Impact-level bias | more_landing_prep, less_plyo_density | Shown in notes | landing_risk_respected |
| sprint_mechanics_competency | +1/-1 bias drill vs max-v | — | more_sprint_drills, less_sprint_density | Shown in notes | — |
| lumbar_risk | Risk-filter DLHD/Rot exercises | Gym env penalty | less_hinge_rotation | Shown in notes | lumbar_risk_respected |
| patellar_tendon_risk | Risk-filter landings/plyos | High-impact penalty | less_plyo_density, less_impact_cond | Shown in notes | — |
| hamstring_risk | Risk-filter DLHD/Sprint | RSA/speed-endurance penalty | less_sprint_density | Shown in notes | hamstring_risk_respected |
| shoulder_overhead_risk | Risk-filter VPush/VPull | — | less_overhead | Shown in notes | shoulder_risk_respected |
| groin_adductor_risk | Risk-filter lateral sprint/COD | COD penalty | less_lateral_cod | Shown in notes | — |
| ankle_foot_risk | Risk-filter plyo/landing/sprint | High-impact penalty | less_plyo_density | Shown in notes | — |
| sprint_10m_band | — | Speed-endurance penalty | — | Shown in notes | — |
| aerobic_band | — | Aerobic-penalty | — | Shown in notes | — |

## Key Design Principles

1. **Risk flags are filters, not rehab.** The engine does not build rehab plans. It only avoids exercises that conflict with known risk flags. It does not prescribe corrective exercises.

2. **Performance flags are biases, not hard constraints.** A force-deficient athlete still gets explosive work — just slightly less of it relative to strength work. Bias is applied as a tiebreaker in selection ordering.

3. **All fields are optional.** Old AthleteProfile definitions with none of the new fields set work identically to pre-Wave-5 behavior.

4. **Test bands are reserved for future use.** They exist in the data model but only conditioning selection currently uses them (sprint_10m_band and aerobic_band). They are safe to ignore.
