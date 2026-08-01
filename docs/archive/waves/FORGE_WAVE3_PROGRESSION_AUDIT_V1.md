# FORGE Wave 3 Progression Audit

## How Exercise Rotation Currently Works

**File:** `src/forge/exercise_selector.py:95-109` (`_least_recently_used`)

The entire rotation logic is a single 15-line function. Every call to `select_exercise()` produces a candidate list by filtering `SELECTION_PRIORITIES` (a per-family priority-ordered list of exercise IDs) through difficulty, equipment, injury, and competition gates. The LRU function scores candidates:

- `score = -1` if the exercise has never been used (preferred)
- `score = 0` if recently used (penalised)  
- `score = 1` if recently used AND the `last_used` key contains "week" or "day" (more penalised)

**Key weakness:** This is a stateless per-session pick. There is no concept of "this is the main squat of this block." A coach could see:
- Week 1 Monday: Goblet Squat
- Week 1 Wednesday: Barbell Back Squat  
- Week 2 Monday: Front Squat
- Week 2 Wednesday: Air Squat

No main lift continuity. No mini-block structure. No planned rotation cadence.

| Family Type | Current Rotation | Coach Expectation |
|---|---|---|
| Main strength (DLKD/DLHD) | Can change every session | Stable for 3-4 weeks, progress to harder variant |
| Secondary (HPush/HPull/VPush) | Can change every session | Rotate every 2-3 weeks |
| Accessories (Acc/HYP variants) | Can change every session | Rotate freely |
| Core/Carry/Sprint/Landing | Can change every session | Progression chain should build |

## How Conditioning Progression Currently Works

**File:** `src/forge/conditioning_engine.py:104-181` (`generate_conditioning` / `select_conditioning`)

Conditioning is selected session-by-session with **zero memory of previous selections**. Each call independently picks the best protocol for the current (goal, environment, sport, comp_window, level) context. There is no:

- protocol continuity (same protocol progressed across weeks)
- protocol progression chain (protocol A → progressed A' → protocol B)
- week-type awareness (accumulation vs taper vs deload)

If 8 weeks of sessions include conditioning, weeks 1, 4, and 8 could each get a completely different protocol from a different energy system — even within the same goal.

## What Block-Level Progression Exists from Wave 2

**File:** `src/forge/prescription_rules.py`

Wave 2 added `WEEK_VOLUME_FACTORS`:
```
W1: 0.85  W2: 0.90  W3: 0.95  W4-6: 1.0  W7: 0.85  W8: 0.70
```

This gives a **volume-only** shape (accumulation → peak → taper) but:
- No differentiation in **what** changes week to week (all roles scale the same)
- No deload week logic within a normal block (separate BP13 exists as a full blueprint)
- No competition-window integration with block weeks
- No week-type labels visible in output

## Where the Weakest Coach-Facing Progression Failures Are

| Failure | File | Why It Hurts |
|---|---|---|
| Main lifts bounce randomly | `exercise_selector.py:95-109` | Coach sees no "this is the block squat" |
| Conditioning resets every session | `conditioning_engine.py:104-269` | No intentional progression across 8 weeks |
| Week 1 ≈ week 4 (same sets, same reps, same everything except volume) | `prescription_rules.py` (WEEK_VOLUME_FACTORS only) | Block has no visible training direction |
| No deload/taper week within normal block | `main.py` (no week_type logic) | All weeks look structurally similar |
| No program-level checks | `validator.py` (session-only) | Can't verify block quality |
| Weekly exposure not tracked | nowhere | Can accidentally cluster high-impact/eccentric work |
| No rotation cadence by family role | `exercise_selector.py` | Accessories rotate same as main lifts |

## Minimal Architecture Needed

I need to add coordination logic across the 8-week generation loop in `generate_program()`. Specifically:

1. **Pre-plan exercise continuity** before the week loop, assigning a planned exercise to each (slot, week) pair. Main strength gets 3-4 week mini-blocks; secondary gets 2-week blocks; accessories rotate freely.

2. **Add week-type labels** (ACCUMULATION, INTENSIFICATION, TAPER, DELOAD, COMPETITION_WEEK) that modify prescription and conditioning behavior.

3. **Track conditioning across weeks** with a `prev_conditioning` dict passed through the loop, enabling protocol progression rather than fresh selection.

4. **Add program-level validator** with 6-8 checks.

5. **Add weekly exposure guardrails** for eccentric/impact/sprint/jump clustering.

6. **Add coach-visible week-type labels** to rendered output.

Target: 1 new module (`progression_engine.py`), ~50-100 lines of changes in main.py, ~30-50 lines in validator.py, ~10 lines in renderer.py. Minimal models.py changes.
