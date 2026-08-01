# FORGE Wave 6 — Prescription Personalization Audit

## Pre-Wave 6 State: What Was Still Generic After Wave 5

After Wave 5, FORGE had athlete-aware **exercise selection** and **conditioning routing**, but the **prescription layer** (sets, reps, intensity, rest, progression) remained completely generic:

| Wave 5 Capability | Wave 5 Gap |
|---|---|
| Exercise selection biased by force/velocity profile | Same prescription for all athletes on same exercise |
| Landing competency filters advanced landings | No adjustment to plyo/landing set-rep-intensity |
| Risk flags filter dangerous exercises | No modification of dosing for risk flags |
| Role-based exercise bias | Role doesn't affect how work is dosed |

**Concrete example of the gap:**
- A force-deficient rugby prop and a velocity-deficient rugby backline both select DLKD-004 (Barbell Back Squat)
- Both get `sets: "4", reps: "6-8", intensity_note: "RPE 7-9"` — identical dosing
- Coach sees different exercise rationale but same dose — not coach-recognizable

## Why Wave 6 Was Needed

Real S&C coaches differentiate **dosing**, not just exercise selection:
- Force-deficient athlete → heavier, lower-rep strength work
- Velocity-deficient athlete → velocity-friendly loading, explosive emphasis  
- Patellar tendon risk → reduced reactive jump density
- Fast bowler → preserved sprint intent but lumbar-friendly hinge dosing
- Singles tennis player → higher court conditioning density than doubles

Wave 6 closes this by making the prescription engine **athlete-aware and role-aware** while preserving the deterministic Wave 2 architecture.
