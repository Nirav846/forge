# FORGE Wave 4 — Implementation Report

## Files Changed

| File                          | Change                                                                                      |
|-------------------------------|---------------------------------------------------------------------------------------------|
| `src/forge/models.py`         | Added `testing_categories: list[str]` and `adjustment_note: str` to `Session` dataclass    |
| `src/forge/progression_engine.py` | Added `plan_weeks()`, `plan_testing()`, `review_week()`, `adjust_next_week()`, 6 new program-level balance checks |
| `src/forge/main.py`           | Integrated `plan_weeks()`, `plan_testing()`, `review_week()`/`adjust_next_week()` into `generate_program()` |
| `src/forge/renderer.py`       | Added `render_block_summary()`, test `[TEST]` markers, adjustment `[Adj]` markers           |
| `tests/test_wave4_periodization.py` | 44 new Wave 4 tests                                                                    |
| `tests/test_wave3_progression.py` | Updated week-type assertions to include `realization`, `test`, `light`                    |

## What Each Part Delivered

### Part 1 — Explicit Week Structure
- `WEEK_STRUCTURE_DEFAULT` defines the canonical 8-week plan: accumulation x2 → intensification x2 → realization x2 → taper → test
- `plan_weeks()` modifies structure based on: blueprint category (deload=all deload), athlete level (youth/beginner→no test week), goal (RTP→no realization), competition proximity (speed/power→early taper)
- Week types are now behavioral inputs to session building, not just decorative labels

### Part 2 — Testing Integration
- 6 testing categories defined in `TESTING_CATEGORIES` with blocked-for rules
- `plan_testing()` places baseline (W1), mid-block checkpoint (W5/6), and exit battery (W8)
- Testing-aware rendering: `[TEST]` markers in session output
- Blocked by: competition proximity, beginner/youth status, RTP status, deload blueprint

### Part 3 — Auto-Adjustment
- `review_week()` counts eccentric/impact/sprint/exercise totals and produces risk flags
- `adjust_next_week()` translates risks into: slot reduction, conditioning modification, and/or week-intent override
- Applied in `generate_program()` after each week's sessions are generated
- All adjustments produce coach-readable notes stored on adjusted sessions

### Part 4 — Program-Level Balance
- 6 new program-level validation checks added to `verify_program_credibility()`
- Covers: movement balance, sprint/landing bounding, conditioning dominance, core/rotational presence, test-week loading, block-level exposure
- All feed into credibility score

### Part 5 — Coach-Facing Summary
- `render_block_summary()` produces week-by-week table showing: intent, test markers, adjustment flags, exposure summary
- Renderers show `[TEST]` and `[Adj]` markers inline
- Program score visible in both short and long format

## Test Count

- **356 tests pass** (312 existing + 44 new Wave 4)
- **2 pre-existing failures** unchanged (LevelDetermination, IntentCategories)
- **43 Wave 3 tests** updated for compatibility
- **44 Wave 4 tests** across 6 categories: week structure (10), testing (8), auto-adjustment (7), program validation (7), rendering (5), backward compatibility (7)

## Coach-Visible Changes

A coach reading an 8-week program after Wave 4 will see:

1. **Clear week labels**: W1-W2 accumulation, W3-W4 intensification, W5-W6 realization, W7 taper, W8 test
2. **Testing markers**: `[TEST] Movement / Technical Benchmark | Jump / Power Test` on Week 1 sessions
3. **Auto-adjustment notes**: `[Adj] Prev week high impact; reduced families; Downgraded intensification→accumulation`
4. **Block summary**: A table showing every week's intent, tests, adjustments, and exposure
5. **Program score**: Overall credibility score at the top reflecting 14 program-level checks

## Does the Full 8-Week Block Now Look Like It Was Periodized by a Coach?

**Yes.** The most visible change is that week labels are now structural, not cosmetic. A coach reading the output sees:
- Week 1 has a **movement baseline** because it's the first week
- Weeks 3-4 are **intensification** weeks (higher volume, higher difficulty)
- Week 5 has a **jump/sprint checkpoint** because it's the mid-block realization phase
- Week 2 got **auto-adjusted** (fewer families) because Week 1 was too dense
- Week 8 has a **full exit battery** instead of a generic deload

The block summary (`render_block_summary`) gives the coach a one-page view of the entire 8-week arc, with exposure totals and adjustment notes. This is the single biggest improvement — a coach can now see the block as a block, not as 32 separate sessions.

## Biggest Remaining Gap After Wave 4

### Testing Protocols Are Markers, Not Actual Protocols
Wave 4 marks sessions as testing sessions and reduces surrounding training stress, but does not generate actual test protocols (e.g., "3RM Back Squat" or "CMJ x 3 trials"). A coach sees `[TEST] Lower Body Strength Test` but does not get a specific test prescription.

**When to close this gap**: When the data model supports test protocols (sets, reps, loading schemes for assessment) and when the prescription engine can differentiate test prescriptions from training prescriptions.

### Auto-Adjustment is Conservative
The current adjustment rules only reduce — they never increase. A week that was too easy does not get bumped up. This is intentional (safety-first), but means the system cannot auto-correct for under-stimulus.

**When to close this gap**: When FORGE has a load-monitoring or fatigue-management subsystem that can differentiate "too hard" from "too easy."

### No Neuromuscular Readiness Integration
Auto-adjustment looks only at what FORGE generated last week — it does not consider athlete-reported readiness, HRV, or external load data. This keeps it deterministic but limits its ability to respond to real-world training responses.

**When to close this gap**: When FORGE integrates with external monitoring data or when the 8-week block model extends to continuous rolling programs.
