# FORGE Periodization Rules V1

## Rule Categories

1. **Load Threshold Rules** — adjust based on weekly/acute load
2. **Exposure Rules** — adjust based on exposure bucket counts
3. **ACWR Rules** — adjust based on acute:chronic ratio
4. **Competition Window Rules** — extend V1.5 rules with load awareness
5. **Blueprint-Specific Rules** — per-blueprint defaults and limits
6. **Fatigue Interaction Rules** — combined signal rules

---

## 1. Load Threshold Rules

| ID | Condition | Action | Trigger |
|----|-----------|--------|---------|
| L1 | WeeklyLoad > 125% of blueprint reference | Reduce next week by 1 session if possible, else reduce conditioning | "Overreaching beyond design intent" |
| L2 | WeeklyLoad < 75% of blueprint reference | Add 1 light session or increase conditioning volume by 1 protocol | "Under-training — likely missed session" |
| L3 | SessionLoad > 80 (3 exercises × max 15 + heavy conditioning) | Flag for coach review — likely data error or extreme session | "Session load exceeds typical max by 20%+" |
| L4 | 3 consecutive weeks with WeeklyLoad trending up >10%/week | Force deload week (reduce all loads by 40% or switch to BP13) | "Accumulation phase exceeding 3 weeks — deload indicated" |
| L5 | WeeklyLoad > 120% of any single week in the last 4 weeks | Reduce current week by 20% | "Load spike >20% over chronic baseline" |
| L6 | Last 2 weeks have monotonic load decrease (each week < previous) | Add one strength-maintenance session or increase intensity | "Detraining risk — reverse taper" |

## 2. Exposure Bucket Rules

| ID | Condition | Action | Trigger |
|----|-----------|--------|---------|
| E1 | Weekly sprint count < 1 (in-season, field sport) | Replace one non-sprint session with Sprint Development BP10 | "Insufficient sprint stimulus for field sport athlete" |
| E2 | Weekly sprint count = 0 (off-season, sprint-development blueprint) | Add 2 sprint exposures minimum next week | "Zero sprint volume on sprint-development program" |
| E3 | Weekly sprint count > 4 | Remove sprint exposures from next session | "Sprint overexposure — risk of hamstring strain" |
| E4 | Weekly jump count = 0 (power blueprint) | Replace one non-power session with BP4 variant | "Zero jump volume on power-development program" |
| E5 | Weekly jump count > 3 and any one session has impact ≥5 | Force 48h gap before next high-impact session | "Excessive high-impact loading — tendon health risk" |
| E6 | Weekly eccentric count > 4 and in competition window (-7 to -2 days) | Remove all eccentric ≥4 exercises from this week | "Pre-comp eccentric reduction" |
| E7 | Weekly eccentric count < 2 (strength blueprint, off-season) | Add 1 RDL-variant exercise to next session | "Insufficient eccentric stimulus for strength adaptation" |
| E8 | Weekly decel count = 0 and athlete sport has COD demands | Add one deceleration conditioning protocol next week | "Zero deceleration exposure for COD sport athlete" |
| E9 | Weekly rot count = 0 and athlete sport is rotational-dominant | Add one rotational exercise next session | "Zero rotational exposure for rotational sport athlete" |
| E10 | Weekly rot count > 5 | Reduce rotational exercises by 2 next session | "Rotational overexposure — soft tissue recovery" |

## 3. ACWR Rules

| ID | Condition | Action | Trigger |
|----|-----------|--------|---------|
| A1 | ACWR > 1.5 | Force deload next session (reduce load by 40%) | "Red zone ACWR — mandatory load reduction" |
| A2 | ACWR > 1.3 for 2 consecutive weeks | Reduce current week load by 25% | "Caution zone sustained — intervention needed" |
| A3 | ACWR < 0.8 for 2 consecutive weeks | Add 1 extra session or increase load by 20% | "Under-training zone sustained — ramp up" |
| A4 | ACWR 0.8-1.3 for 4+ consecutive weeks | Allow progression: increase load by 5-10% next week | "Green zone sustained — progression indicated" |

## 4. Competition Window Rules (V1.5 Extensions)

Existing V1.5 rules stand. Additions:

| ID | Condition | Action | Trigger |
|----|-----------|--------|---------|
| C1 | Comp day -7 to -5, WeeklyLoad > 75% of blueprint reference | Reduce to 75% of reference load | "Pre-comp load reduction — 75% week" |
| C2 | Comp day -4 to -2, WeeklyLoad > 50% of blueprint reference | Reduce to 50% of reference load | "Pre-comp load reduction — 50% week" |
| C3 | Comp day -1, SessionLoad > 25 | Reduce to activation-only session (load ≤25) | "Pre-comp activation — no fatigue accumulation" |
| C4 | Comp day -7 to -2, eccentric_exposures > 2 | Remove all eccentric ≥4 exercises | "Pre-comp eccentric protection override" |
| C5 | Comp day -3 to -1, jump_exposures > 1 | Remove all high-impact jumps (impact ≥5) | "Pre-comp jump exposure limit" |
| C6 | Competition day +1 to +2 (post-comp) | Active recovery only — load < 30 total | "Post-comp recovery window" |
| C7 | Competition day +3 to +5 | Gradual re-entry — SessionLoad ≤ 70% of blueprint reference | "Post-comp re-entry window" |

## 5. Blueprint-Specific Rules

| ID | Blueprint | Rule |
|----|-----------|------|
| B1 | BP1 Full Body Strength | Minimum 2 strength-family (DLKD+DLHD) exposures per session |
| B2 | BP2 Strength+Power | Every session must have at least 1 explosive exercise (Ball/Plyo) |
| B3 | BP3 Strength+Conditioning | At least 1 cardio-zone conditioning protocol per session |
| B4 | BP4 Power+Speed | At least 2 sprint/COD exercises per session |
| B5 | BP5 Upper/Lower Split | Upper days: max 3 push exercises; Lower days: max 2 squat-variant exercises |
| B6 | BP6 Power Maintenance | Total session load < 40 (maintenance intent) |
| B7 | BP7 Youth Foundation | All exercises difficulty ≤3; no impact ≥5 |
| B8 | BP8 Court Sport | At least 1 deceleration/modify-direction element per session |
| B9 | BP9 Rugby Off-Season | At least 1 carry or rotational exercise per session |
| B10 | BP10 Sprint Development | At least 1 max-velocity exposure per session (fly zone or ins-n-outs) |
| B11 | BP11 Hypertrophy | Preference for exercises with moderate fatigue (2-3) and high volume potential |
| B12 | BP12 Return to Sport | All exercises difficulty ≤2; no eccentric ≥4; no impact ≥4 |
| B13 | BP13 Deload | Total session load < 30; no eccentric ≥3; no impact ≥4 |

## 6. Fatigue Interaction Rules

| ID | Condition | Action | Trigger |
|----|-----------|--------|---------|
| F1 | SessionLoad > 60 AND athlete has 5+ consecutive training days | Replace next session with deload (BP13) | "Fatigue accumulation beyond recovery capacity" |
| F2 | 3 consecutive sessions with SessionLoad trend > 60 | Reduce next session by 1 exercise (prefer removing Acc/Core) | "Persistent high-session-load pattern" |
| F3 | Eccentric-cost sum over 2 consecutive sessions > 20 | Remove all eccentric ≥4 exercises from next session | "Eccentric load accumulation — DOMS management" |
| F4 | Impact sum over 2 consecutive sessions > 24 (3 exercises × avg 8 impact) | Replace next high-impact session with low-impact alternative | "Impact accumulation — joint protection" |
| F5 | Fatigue sum + Eccentric sum > 30 for any single session | Flag as "High Systemic Load" — mandatory lighter next session | "Combined systemic + muscle damage overload" |
| F6 | Fatigue sum > 20 AND impact sum > 15 (single session) | Replace next session with active recovery | "Double-overload — CNS + joint stress" |

## Quick Reference: Combined Rule Priority

When multiple rules trigger, priority order:

1. Competition window rules (C1-C7) — highest priority
2. ACWR red zone (A1)
3. Fatigue interaction rules (F1-F6)
4. Exposure bucket rules (E1-E10)
5. ACWR caution zone (A2-A3)
6. Load threshold rules (L1-L6)
7. Blueprint-specific rules (B1-B13) — lowest priority

Within same priority, most restrictive rule wins (safest approach).
