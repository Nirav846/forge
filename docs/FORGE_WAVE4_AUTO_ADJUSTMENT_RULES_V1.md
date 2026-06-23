# FORGE Wave 4 — Auto-Adjustment Rules

## Architecture

Auto-adjustment runs AFTER each week is generated and BEFORE the next week is built. It consists of two functions:

1. `review_week(sessions, week_type)` → risk flags dict
2. `adjust_next_week(risk_flags, next_intent, blueprint_id, goal)` → adjustment dict

## Thresholds

| Signal                    | Threshold              | Risk Flag             |
|---------------------------|------------------------|-----------------------|
| High-eccentric exercises  | > 3 per week           | `reduce_eccentric`    |
| High-impact exercises     | > 4 per week           | `reduce_impact`       |
| Sprint exposures          | > 4 per week           | `reduce_sprint`       |
| Total exercises           | > 20 per week          | `reduce_volume`       |

## Adjustment Responses

| Risk Flag(s)              | Next Week Adjustment                                                      |
|---------------------------|---------------------------------------------------------------------------|
| `reduce_eccentric`        | -1 slot family (reduce optional families)                                 |
| `reduce_impact`           | -1 slot family                                                           |
| `reduce_sprint`           | Conditioning → `recovery` (light)                                        |
| `reduce_volume`           | -1 slot family                                                           |
| 2+ risks + next intent ∈ {realization, intensification} | Intent overridden to `accumulation`                     |
| Any risk + next intent ∈ {taper, deload, test}         | Conditioning → `recovery` (light)                       |

## Deterministic Rules

1. **Slot reduction is cumulative.** Multiple risks can each trigger -1, but floor is 3 families (minimum viable session).
2. **Intent override is binary.** If 2+ risks exist, the next week's intent is downgraded to accumulation regardless of other factors.
3. **Conditioning modification does not cascade.** Setting conditioning to `recovery` for one week does not force it for subsequent weeks.
4. **Adjustment notes are generated** for coach visibility. All adjustments produce a human-readable note stored on each adjusted session.

## Examples

- Week 1 produces 6 high-eccentric exercises → `reduce_eccentric` → Week 2 gets -1 slot family
- Week 3 produces 5 high-impact + 22 total exercises → `reduce_impact` + `reduce_volume` → Week 4 intent overridden from `intensification` to `accumulation`
- Week 7 (taper) follows a week with any risk → conditioning set to `recovery` (light)
- A clean week with zero risks → no adjustment

## Safety Notes

- Adjustments cannot increase volume or intensity — they only reduce
- Auto-adjustment does not touch Wave 2 prescription logic or Wave 3 continuity
- Week 1 is never adjusted (no previous week to review)
- Competition proximity overrides are handled separately in `plan_weeks()`
