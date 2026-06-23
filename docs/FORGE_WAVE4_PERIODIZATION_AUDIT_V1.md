# FORGE Wave 4 — Periodization Audit

## What Was Missing Before Wave 4

### 1. Week Intent Was Decorative, Not Structural
Pre-Wave 4, `WEEK_INDEX_TO_TYPE` was a simple dict mapping week index → label (accumulation, intensification, peak, taper, deload). It was used for display only — `_build_session()` received `week_type` but made no behavioral decisions based on it.

**Example of weak behavior:**
- A strength athlete with no competition proximity got `peak` in week 5 and `deload` in week 8, even though peak has no explicit meaning in the code. No session was actually "peaked."
- There was no distinction between "realization" (high output) and "peak" — the terms were interchangeable but neither drove behavior.
- Week 8 was always labeled "deload" regardless of whether the athlete could benefit from an exit test week.

### 2. No Testing / Benchmarking
FORGE generated training sessions only. A real coach inserts deliberate testing weeks (baseline, mid-block checkpoint, exit battery). The absence of testing made programs feel like flat training logs rather than periodized blocks.

**Example of weak behavior:**
- An advanced athlete got 8 identical-looking weeks with different volume prescriptions but no week-1 baseline or week-8 exit test.
- A coach reading the output could not tell whether the athlete was supposed to test their back squat in any given week.

### 3. No Auto-Adjustment Between Weeks
Wave 3 added `review_week()` and `adjust_next_week()` as placeholders. The generate loop never called them.

**Example of weak behavior:**
- Week 1 could generate 6+ high-eccentric exercises, and Week 2 would happily repeat the same volume pattern.
- No mechanism existed to down-regulate the next week when the previous week was clearly dense.
- Consecutive high-impact weeks were possible with no guardrails.

### 4. No Program-Level Balance Guarantees
Wave 3 checked session-level credibility (15 checks) and a small set of program-level checks (continuity, deload reduction). But there was no systematic balance verification.

**Examples of weak behavior:**
- A program could accidentally omit core work for all 8 weeks if the blueprint didn't mandate it.
- Sprint/landing exposure could spike uncontrolled across the block.
- A test week (had one existed) could also be the heaviest loading week.
- Conditioning could dominate a strength program.

## Why Wave 4 Was Needed

The core insight: **a coach manages a block, not a session**. Pre-Wave 4, FORGE assembled sessions independently. Wave 4 makes the 8-week block the atomic unit of periodization.

Without Wave 4:
- Programs looked like 24-32 isolated workouts, not a periodized plan
- A coach reading the output could not explain *why* week 5 was different from week 4
- Testing, tapering, and peaking were cosmetic labels, not structural decisions
- Block-level problems (missing core, excessive eccentric load, conditioning dominance) were invisible to both the generator and the coach

## What Changed

See `FORGE_WAVE4_IMPLEMENTATION_REPORT_V1.md` for full details.
