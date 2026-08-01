# FORGE V2 Load Signal Audit

## Current Load Metadata

### Exercise-Level (241 exercises)

| Field | Range | Distribution | Source |
|-------|-------|-------------|--------|
| `fatigue_cost` | 1-5 | 26×1, 49×2, 108×3, 56×4, 2×5 | Family base + difficulty/isometric adjustments + named overrides |
| `impact_level` | 1-5 | 21×1, 54×2, 106×3, 22×4, 38×5 | Family base + explosive adjustment |
| `eccentric_cost` | 1-5 | 64×1, 72×2, 71×3, 27×4, 7×5 | Family base + difficulty adjustment + isometric override |
| `competition_role` | enum | 106 strength, 52 speed_power, 45 accessory, 21 core, 17 carry | Family-based mapping |
| `difficulty` | 1-5 | 38×1, 56×2, 66×3, 51×4, 30×5 | Hand-assigned per exercise |
| `unilateral` | bool | 76 True, 165 False | Hand-assigned |
| `explosive` | bool | 64 True, 177 False | Hand-assigned |
| `isometric` | bool | 36 True, 205 False | Hand-assigned |
| `rotational` | bool | 28 True, 213 False | Hand-assigned |

### Conditioning-Level (105 protocols)

| Field | Range | Distribution | Source |
|-------|-------|-------------|--------|
| `fatigue_cost` | 1-5 | 9×1, 12×2, 28×3, 34×4, 22×5 | From protocol `fatigue_score`, or inference by system |
| `impact_level` | 1-5 | 10×1, 4×2, 28×3, 63×4, 0×5 | Inferred from env_cat + system + fatigue_score |
| `eccentric_cost` | 1-5 | 10×1, 6×2, 83×3, 6×4, 0×5 | Inferred from env_cat + movement_profile |
| `session_role` | enum | 60 main_conditioning, 17 speed_support, 12 top_up, 8 power_maintenance, 8 recovery_flush | Inferred from system + fatigue_score |
| `movement_profile` | string | 12 distinct profiles | Inferred from protocol fields |
| `environment_category` | enum | 74 field, 16 court, 8 recovery, 7 gym | Computed from environment list |

### Missing Metrics

1. **Volume (sets × reps × load)**: No set/rep data on exercises. Blueprint `min_session_composition` has `count` fields (e.g., `count: 1` per family per session) but no rep ranges or percentages. Session duration is estimated at 5 min per exercise block.

2. **Weekly cumulative load**: The main generator (`generate_program`) creates sessions via nested week/day loops but does not accumulate any load value across sessions. Each session is independently generated.

3. **Rolling load (acute:chronic)**: No mechanism to track load across a moving window. The generator runs for `_parse_weeks()` weeks (hardcoded 8) and produces `freq` sessions per week, but no load is carried between weeks.

4. **Exposure frequency**: No tracking of how many times per week an athlete performs sprinting, jumping, eccentric work, decelerations, or rotational work. These are all inferable from the existing data but are not bucketed.

5. **Set count / repetition volume**: `SessionBlock` has `target_intensity` and `rest_period` but no `sets`, `reps`, `rpe`, `percentage`, or `volume` fields.

## What Current Metadata Can Support

| Capability | Support Level | Gap |
|-----------|--------------|-----|
| Per-exercise load score | Ready: fatigue_cost + impact_level + eccentric_cost sum | No set multiplier (we don't know how many sets) |
| Per-session load score | Buildable: sum of exercise loads in blocks + conditioning load | No set volume adjustment |
| Weekly load tracking | Buildable: accumulate session loads across 1 week | Need data structure to hold weekly totals |
| Exposure frequency (sprint/jump/...) | Buildable: tag each exercise/conditioning protocol to exposure buckets | Need bucket definitions + counter |
| Acute:chronic ratio | Buildable if we track rolling 7-day and 28-day windows | Need windowed accumulator |
| Load-driven session adjustment | Requires all of the above + rule engine | Major new subsystem |

## Verdict

The three-variable model (fatigue × impact × eccentric) at the exercise level is a credible foundation. The gap is not in signal quality — it is in **accumulation, bucketing, and response**. We have the sensors; we lack the odometer and the dashboard.

**Available for V2 (no new data needed):**
- Per-exercise load score
- Per-conditioning load score
- Family identification → exposure bucket mapping
- Competition role → intent classification

**Needed for V2 (new code structures):**
- Weekly load accumulator
- Exposure bucket counters
- Acute:chronic windows
- Load-driven rules that modify session generation
