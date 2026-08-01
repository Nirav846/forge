# FORGE Wave 5 — Athlete Profile Audit

## Pre-Wave 5 State: What Gaps Existed

Before Wave 5, `AthleteProfile` contained only:

| Field | Purpose |
|---|---|
| `sport` | Sport selection |
| `training_age_years` | Training experience |
| `season_phase` | Off/pre/in-season/transition |
| `goal` | Strength, power, hypertrophy, etc. |
| `equipment_profile` | Available equipment |
| `athlete_level` | Beginner/Intermediate/Advanced |
| `technique_consistency` | 0-1 gate for difficulty capping |
| `injury_status` / `injury_history` | Injury-aware substitution |
| `fatigue_level` | Normal/elevated/high |
| `age` | Youth safety gates |
| `days_to_match` | Competition proximity |
| `strength_base_met` | Bilateral/unilateral gate |

**What was missing:**

1. **No performance profile** — The engine had no concept of an athlete's force/velocity profile, elastic ability, or conditioning baseline. Two rugby players on the same blueprint received identical programs regardless of being "strong but slow" vs "fast but weak."

2. **No risk flags** — Only injury history (named exercise conflicts) existed. A coach could not flag "this athlete has chronic lumbar issues" or "patellar tendon is a concern" and have the engine adjust loading strategy accordingly.

3. **No landing/sprint competency awareness** — Wave 1 added Landing mechanics as a family, but selection was identical regardless of athlete competency. A poor lander got the same Depth Jump Stick as an elite lander.

4. **No exercise-level personalization** — Exercise selection was driven purely by priority order + LRU rotation. No athlete-specific bias existed.

5. **No conditioning personalization** — Conditioning was sport-aware and competition-aware but not athlete-aware. A poor-conditioning athlete and a well-conditioned athlete on the same sport got the same protocol difficulty tier.

6. **No coach-facing personalization notes** — A coach had no visibility into *why* the engine chose certain exercises or volume patterns for their athlete.

## Why Wave 5 Was Needed

The gap was clear: FORGE could produce a credible program for any sport/blueprint combination, but two athletes on the same blueprint got nearly identical programs. A real S&C coach differentiates programs based on athlete-specific traits: who needs more strength work, who needs more explosive work, who has chronic injury risks that demand modified loading strategies.

Wave 5 closes this gap with a compact, deterministic athlete profile layer.
