# FORGE V2 Load Model

## Design Principles

1. **Deterministic** — same inputs always produce same outputs
2. **Transparent** — a coach can verify every calculation by hand
3. **Zero physiology formulas** — no VO2max estimation, no lactate modeling, no HR-based calculations
4. **Composable** — exercise → session → week → mesocycle, each level is sum of the level below

## Load Variables

Every load-capable entity in FORGE produces three raw signals:

```
fatigue_cost  (1-5)  — systemic/CNS fatigue
impact_level  (1-5)  — joint/ground reaction force
eccentric_cost (1-5) — muscle damage / DOMS risk
```

These exist on both `Exercise` and `ConditioningProtocol`.

## Exercise Load Score

```
ExerciseLoad = fatigue_cost + impact_level + eccentric_cost
```

Range: 3–15 per exercise appearance.

**Example:**
- Goblet Squat (F3/I3/E3) → 9
- RDL (F3/I3/E5) → 11
- Nordic Curl (F4/I3/E5) → 12
- Plank (F1/I1/E1) → 3
- Depth Jump (F4/I5/E4) → 13

**Rationale:** Simple sum. No weighting — the three dimensions already encode different risk profiles. A coach reading "RDL = 11" and "Plank = 3" immediately understands the difference.

## Conditioning Load Score

```
ConditioningLoad = fatigue_cost + impact_level + eccentric_cost
```

Range: 3–13 per conditioning protocol.

**Example:**
- AC-001 (F2/I3/E3) → 8
- RSA-003 (F4/I4/E3) → 11
- RC-005 (F1/I1/E1) → 3
- AS-002 (F3/I4/E3) → 10

## Session Load Score

```
SessionLoad = Σ ExerciseLoad(block.exercises) + ConditioningLoad
```

**Example session (Full Body Strength, no comp):**

| Block | Exercise | Fatigue | Impact | Eccentric | Load |
|-------|----------|---------|--------|-----------|------|
| DLKD | Goblet Squat | 3 | 3 | 3 | 9 |
| HPush | Bench Press | 3 | 3 | 3 | 9 |
| DLHD | RDL | 3 | 3 | 5 | 11 |
| HPull | Dumbbell Row | 3 | 3 | 3 | 9 |
| Core | Plank | 1 | 1 | 1 | 3 |
| Acc | Band Pull-Apart | 2 | 2 | 2 | 6 |
| Conditioning | AC-001 | 2 | 3 | 3 | 8 |
| **Total** | | | | | **55** |

## Weekly Load Score

```
WeeklyLoad = Σ SessionLoad(week)
```

For a 3-session/week blueprint:

| Session | Load |
|---------|------|
| Monday | 55 |
| Wednesday | 52 |
| Friday | 48 |
| **Weekly total** | **155** |

## Acute:Chronic Ratio (Rolling Load)

```
AcuteLoad  = Σ SessionLoad(last 7 days)
ChronicLoad = Σ SessionLoad(last 28 days) / 4  (weekly average)

ACWR = AcuteLoad / ChronicLoad
```

**Interpretation (deterministic thresholds):**
- ACWR < 0.8 → under-training risk (program too light)
- ACWR 0.8–1.3 → green zone (appropriate load progression)
- ACWR 1.3–1.5 → caution (possible overreach)
- ACWR > 1.5 → red zone (high injury risk, force deload)

## Family-Level Load Profiles

Pre-computed from current exercise data for reference:

| Family | Avg Fatigue | Avg Impact | Avg Eccentric | Avg ExerciseLoad |
|--------|-------------|------------|---------------|------------------|
| Core | 1.2 | 1.0 | 1.2 | **3.4** |
| Acc | 2.0 | 2.0 | 2.0 | **6.0** |
| Carry | 2.2 | 2.0 | 1.0 | **5.2** |
| Rot | 2.2 | 2.4 | 2.1 | **6.7** |
| HPush | 3.0 | 3.1 | 3.3 | **9.4** |
| SLKD | 3.5 | 3.0 | 3.5 | **10.0** |
| SLHD | 3.2 | 3.0 | 3.4 | **9.6** |
| DLKD | 3.2 | 3.2 | 2.7 | **9.1** |
| HPull | 3.3 | 3.1 | 3.3 | **9.7** |
| VPull | 3.3 | 3.1 | 3.3 | **9.7** |
| VPush | 3.4 | 3.2 | 2.4 | **9.0** |
| Sprint | 3.4 | 4.2 | 1.5 | **9.1** |
| Ball | 3.4 | 5.0 | 1.4 | **9.8** |
| Plyo | 3.2 | 5.0 | 2.4 | **10.6** |
| DLHD | 3.5 | 3.2 | 3.7 | **10.4** |

## Exposure-Specific Load Metrics

In addition to total load, track sub-scores:

```
SprintLoad    = Σ Sprint/Speed exercises + conditioning with sprint movement profile
JumpLoad      = Σ Plyometric exercises + plyometric conditioning
EccentricLoad = Σ exercises/conditioning with eccentric_cost >= 4
DecelLoad     = Σ exercises with "decel" in role/name + conditioning with accel_decel profile
RotLoad       = Σ Rotational exercises + rotational conditioning
```

## Weekly Load Reference Ranges (Suggested)

Based on current blueprint frequencies and typical session loads:

| Blueprint | Sessions/Week | Typical Session Load | Weekly Load Range |
|-----------|---------------|---------------------|-------------------|
| Power Maintenance (BP6) | 1-2 | 25-35 | 25-70 |
| Deload (BP13) | 2-3 | 15-25 | 30-75 |
| Youth Foundation (BP7) | 2-3 | 30-40 | 60-120 |
| Full Body Strength (BP1) | 3-4 | 45-60 | 135-240 |
| Strength+Power (BP2) | 4-5 | 50-70 | 200-350 |
| Rugby Off-Season (BP9) | 4-5 | 55-75 | 220-375 |
| Hypertrophy (BP11) | 4-6 | 55-70 | 220-420 |

## Implementation Notes

- Load scores are integers, not floats (no precision illusion)
- ACWR uses simple averages, not exponentially weighted moving averages
- Weekly load resets every 7 days (Sunday-based or rolling 7-day window, configurable)
- Chronic load is a 28-day simple average of weekly loads (4 rolling weeks)
- All load data is stored alongside the session, not calculated on-the-fly
