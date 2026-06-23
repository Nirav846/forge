# FORGE Coach Pilot Protocol V1

**Date:** 2026-06-19
**Status:** Draft — ready for execution
**Target:** 5 S&C coaches, 50 programs, 5 sports

---

## Summary

This protocol defines the final coach-validation phase before FORGE production
release. 50 anonymous programs across 5 sports will be presented to 5 S&C
coaches (10 programs each). Coaches rate credibility, suggest edits, and flag
missing/unnecessary content. Edit distance is tracked per coach, per blueprint,
per family. A release gate scorecard determines production readiness.

### Quick-reference card

| Step | What | Who | When |
|------|------|-----|------|
| 1 | Generate 50 review packets | Engineer | Day 1 |
| 2 | Distribute 10 packets per coach | Engineer | Day 1 |
| 3 | Coaches return surveys (7-day window) | 5 coaches | Days 2–8 |
| 4 | Calculate edit distance on returned surveys | Engineer | Day 9 |
| 5 | Write failure analysis | Engineer | Day 10 |
| 6 | Apply release gate | Engineer + Lead Coach | Day 10 |
| 7 | Gate PASS → release; FAIL → iterate | Both | Day 10 |

---

## Part 1 — Review Packets

### 1.1 Program generation

Generate 50 programs using the existing `generate_program()` pipeline.

Stratify by:

| Sport | Count | Rationale |
|-------|-------|-----------|
| Cricket | 10 | High rotational demand, long-duration field work |
| Rugby | 10 | Contact sport, strength-power emphasis, field-based |
| Tennis | 10 | Asymmetric, multi-directional, high injury-risk |
| Badminton | 10 | Explosive, rotational, indoor court, asymmetry |
| Soccer | 10 | Running-dominant, lower-body heavy, field-based |

For each sport, vary across:

| Variable | Distribution |
|----------|-------------|
| Athlete level | Beginner 4, Intermediate 4, Advanced 2 |
| Training age | 0–2 yr (3), 2–5 yr (4), 5+ yr (3) |
| Season phase | Off-season 3, Pre-season 3, In-season 2, Transition 2 |
| Equipment | Field Only 2, Basic Gym 5, Commercial Gym 3 |
| Goal | strength 3, power 2, speed 2, conditioning 1, mass 1, general 1 |
| Fatigue level | Normal 7, High 3 (per sport) |

10 programs × 5 sports = 50 total.

### 1.2 Anonymisation

Each packet MUST strip all FORGE branding before coach review.

**Remove:**
- "FORGE Generated Program" header
- Credibility scores
- Blueprint IDs and internal names
- Any exercise IDs (e.g. "DLKD-004")

**Render as clean coach output:**

```
Athlete: M, 22, Cricket (Batter)
Level: Intermediate | Training age: 3 yr | Season: Pre-season
Goal: Power | Equipment: Basic Gym | Frequency: 4x/week
Duration: 8 weeks

--- Session 1 ---
  [DLKD] Double Leg Knee Dominant
    - Back Squat (d:3, eq: Barbell, Rack)
    - Front Squat (d:3, eq: Barbell, Rack)
  [Ball] Ballistic
    - Med Ball Chest Pass (d:2, eq: Med Ball)
  [DLHD] Double Leg Hip Dominant
    - Romanian Deadlift (d:3, eq: Barbell)
  [HPush] Horizontal Push
    - Barbell Bench Press (d:3, eq: Barbell, Bench)
  [HPull] Horizontal Pull
    - Barbell Row (d:3, eq: Barbell)
  [Core] Core
    - Dead Bug (d:2, eq: Bodyweight)
  Conditioning: Repeated Sprint Ability (Anaerobic), 3 sets of 6×20m, 1:4 work:rest
  Total estimated time: 62 min
```

### 1.3 Packet distribution

Each coach receives exactly 10 programs — 2 per sport — so every coach sees
the same cross-sport variety. Assign packets labelled Packet-A through
Packet-E.

Track assignment in a spreadsheet:

| Coach | Packet | Programs |
|-------|--------|----------|
| Coach 1 (lead S&C, cricket club) | A | CRI-01–02, TEN-03–04, BAD-05–06, SOC-07–08, RUG-09–10 |
| Coach 2 (rugby S&C) | B | CRI-02–03, TEN-04–05, BAD-06–07, SOC-08–09, RUG-10–01 |
| Coach 3 (tennis academy) | C | CRI-03–04, TEN-05–06, BAD-07–08, SOC-09–10, RUG-01–02 |
| Coach 4 (multi-sport S&C) | D | CRI-04–05, TEN-06–07, BAD-08–09, SOC-10–01, RUG-02–03 |
| Coach 5 (badminton national) | E | CRI-05–06, TEN-07–08, BAD-09–10, SOC-01–02, RUG-03–04 |

Each program appears in exactly 2 packets (2× coverage, 100 reviews total = 50
programs × 2 raters).

---

## Part 2 — Coach Survey

### 2.1 Survey template

For each program, the coach fills out:

```
===========================================================================
PROGRAM: CRI-01
SPORT: Cricket | LEVEL: Intermediate | SEASON: Pre-season | EQUIP: Basic Gym
===========================================================================

Q1. Would you prescribe this athlete this program?
     ☐ Yes, as-is
     ☐ Yes, with minor changes
     ☐ No, with major changes
     ☐ No, would not prescribe

Q2. Credibility score (1-10)
     Score: ___
     (1 = "I would never write this", 10 = "I would write this exactly")

Q3. What would you change?
     _________________________________________________________________
     _________________________________________________________________
     (Free text — list every edit you would make, in order)

Q4. What is missing?
     _________________________________________________________________
     _________________________________________________________________
     (Free text — what exercise families, exercises, or conditioning?)

Q5. What is unnecessary?
     _________________________________________________________________
     _________________________________________________________________
     (Free text — what would you remove?)
```

Five questions per program, 10 programs per coach, ~50 free-text responses
total per coach (estimated 15 min per program, 2.5 hours total per coach).

### 2.2 Survey response envelope

Coaches return surveys in standardised CSV for automated processing OR
free-text for manual extraction. Prefer CSV for edit distance calculation.

---

## Part 3 — Edit Distance Tracking

### 3.1 Response-to-edit pipeline

For each program review, extract structured edits from Q3 free text.

Parse into the five edit types used in the existing edit distance model:

| Symbol | Type | Example |
|--------|------|---------|
| K | Keep | "Keep the squat pattern" → DLKD kept |
| S | Swap | "Replace RDL with barbell hip thrust" → DLHD exercise swap |
| D | Delete | "Drop the plyo, unnecessary for tennis" → Plyo deleted |
| A | Add | "Add single-leg work" → SLKD added |
| R | Reorder | "Move core before accessories" → Core order changed |

Two passes:

**Pass 1 — Family-level edits** (what families changed)

| Program | Family | Edit | Rationale from Q3 |
|---------|--------|------|-------------------|
| CRI-01 | Plyo | D | "Drop plyo — unnecessary pre-season" |
| CRI-01 | SLKD | A | "Missing single-leg knee work" |
| CRI-01 | Core | R | "Core should follow DL work, not end" |
| ... | ... | ... | ... |

**Pass 2 — Exercise-level edits** (what exercises changed within a kept family)

| Program | Family | Exercise | Edit | Rationale |
|---------|--------|----------|------|-----------|
| CRI-01 | DLKD | Back Squat | K | "Squat is fine" |
| CRI-01 | DLKD | Front Squat | S→Bulgarian SS | "Swap for unilateral variation" |
| ... | ... | ... | ... | ... |

### 3.2 Edit distance formula

Uses the same formula as `FORGE_PROGRAM_EDIT_DISTANCE_AUDIT_V1.md`:

```
edit_distance = (S + D + A + R) / (K + S + D + A + R)
```

Where:
- K = kept families + kept exercises
- S = swapped families + swapped exercises
- D = deleted families + deleted exercises
- A = added families + added exercises
- R = reordered families

Family-level edits weight 3× exercise-level edits (changing a family is
higher-impact than swapping within one).

Calculation per program, then averaged per coach, per blueprint, per family.

### 3.3 Aggregation

| Level | Calculation | Purpose |
|-------|-------------|---------|
| Per program | Edit distance on one coach's edits | Individual coach satisfaction |
| Per coach | Avg over 10 programs | Coach-level acceptance |
| Per blueprint | Avg over all programs using that blueprint | Blueprint quality |
| Per family | Avg over all programs containing that family | Family quality |
| Global | Avg over all 100 reviews | Overall readiness |
| Standard deviation | σ across all reviews | Consistency signal |

---

## Part 4 — Failure Analysis

### 4.1 Recurring edits analysis

After collecting all reviews, identify patterns.

**Table: Recurring Edits**

| Edit | Count | Programs | Coaches | Severity |
|------|-------|----------|---------|----------|
| "Add single-leg work" | 12 | CRI-03, TEN-01, ... | 4/5 | Medium |
| "Remove plyo from cricket" | 8 | CRI-01, CRI-04, ... | 3/5 | Low |
| "Core order wrong" | 7 | ... | 3/5 | Medium |
| "Missing Rot in tennis" | 6 | TEN-02, ... | 3/5 | High |

Severity:
- **High** — edit affects 3+ coaches AND >20% of programs in a sport — must fix
- **Medium** — edit affects 2+ coaches — should fix
- **Low** — edit affects 1 coach — monitor

### 4.2 Recurring blueprint failures

For each blueprint:

| Blueprint | Avg edit distance | Credibility avg | Recurring issues | Grade |
|-----------|-------------------|-----------------|------------------|-------|
| Full Body Strength | 2.1% | 8.9 | None | A |
| Rugby Off-Season | 6.3% | 7.2 | "Too much slow-twitch work" | C |
| Mixed Modal (GPP) | 4.1% | 8.1 | "Session too long" | B |
| ... | ... | ... | ... | ... |

Grade scale:
- **A**: edit ≤ 2%, credibility ≥ 9 → no changes needed
- **B**: edit ≤ 5%, credibility ≥ 8 → minor tweaks
- **C**: edit ≤ 8%, credibility ≥ 7 → moderate revision
- **D**: edit > 8% OR credibility < 7 → redesign blueprint

### 4.3 Recurring family failures

For each family:

| Family | Delete count | Add count | Swap count | Avg credibility impact | Verdict |
|--------|-------------|-----------|------------|----------------------|---------|
| DLKD | 0 | 0 | 1 | -0.1 | ACCEPT |
| SLKD | 0 | 14 | 2 | -0.3 | ADD MORE (shortage) |
| Rot | 1 | 8 | 3 | -0.4 | ADD MORE (rotational) |
| Ball | 7 | 0 | 4 | -0.2 | REDUCE (overused) |
| Sprint | 2 | 6 | 5 | -0.3 | ADD MORE (sport-specific) |

Verdicts:
- **ACCEPT** — family is well-calibrated
- **ADD MORE** — coaches consistently add this family; increase inclusion rate
- **REDUCE** — coaches consistently delete this family; decrease inclusion rate
- **SWAP IMPROPER** — coaches swap to specific variant; adjust selection priorities
- **REASSIGN** — family may belong in different intent category

### 4.4 Critical flaw rules

A flaw is **critical** if it meets ALL three conditions:

1. Mentioned by ≥3 coaches (independently, not coached)
2. Appears in ≥20% of programs for a sport
3. Gets "No, would not prescribe" response AND credibility < 6

Critical flaws block release (see Part 5).

---

## Part 5 — Release Gate

### 5.1 Gate criteria

FORGE is **READY FOR PRODUCTION** if and only if ALL four conditions are met:

| # | Criterion | Threshold | Measurement | Weight |
|---|-----------|-----------|-------------|--------|
| 1 | Average credibility | ≥ 8.5 | Mean of all Q2 scores across all reviews | Gate |
| 2 | Average edit distance | ≤ 5% | Global edit distance across all reviews | Gate |
| 3 | No blueprint below 7/10 | All ≥ 7 | Per-blueprint credibility average | Gate |
| 4 | No recurring critical flaw | Zero | Per Section 4.4 definition | Gate |

**All four must pass.** If any fails, release is blocked.

### 5.2 Graded pass table

| Score | Credibility | Edit distance | Blueprint min | Critical flaws | Verdict |
|-------|-------------|---------------|---------------|----------------|---------|
| Platinum | ≥ 9.0 | ≤ 3% | ≥ 8 | 0 | Full production release |
| Gold | ≥ 8.5 | ≤ 5% | ≥ 7 | 0 | Production release |
| Silver | ≥ 8.0 | ≤ 7% | ≥ 6 | 0 | Conditional — flag below-threshold items |
| Bronze | ≥ 7.0 | ≤ 10% | ≥ 5 | 0 | Iterate — not ready |
| Fail | < 7.0 | > 10% | < 5 | ≥ 1 | Redesign |

### 5.3 Failure response

| Failure mode | Response |
|-------------|----------|
| Credibility < 8.5 | Review offending blueprints & families. Re-run edit audit. Target: reduce edit distance until credibility rises. |
| Edit distance > 5% | Drill into high-edit blueprints. Fix recurring family issues (Section 4.3). Re-run pilot on changed blueprints only. |
| Blueprint < 7/10 | Redesign blueprint: reorder slot_order, adjust mandatory/optional families, add exercises. Re-run single-blueprint pilot (5 coaches × 1 program). |
| Critical flaw present | Fix the root cause, re-run full pilot on all programs touching the flaw, re-assess. |

### 5.4 Scoring template

```
RELEASE GATE SCORECARD
======================
Date: _______________
Evaluator: __________

Criterion 1 — Credibility
  Global avg: ___ / 10
  Pass (≥ 8.5): ☐ YES  ☐ NO

Criterion 2 — Edit distance
  Global avg: ___ %
  Pass (≤ 5%): ☐ YES  ☐ NO

Criterion 3 — Blueprint minimum
  Blueprint with lowest credibility: _____ (___ / 10)
  Pass (all ≥ 7): ☐ YES  ☐ NO

Criterion 4 — Critical flaws
  Critical flaws found: ___
  Pass (zero): ☐ YES  ☐ NO

OVERALL: ☐ PASS  ☐ FAIL
```

### 5.5 Post-gate actions

**If PASS (Gold or Platinum):**
- Freeze exercise library
- Freeze blueprint definitions
- Tag release: `v1.0.0-coach-validated`
- Proceed to production deployment

**If PASS (Silver):**
- Fix flagged blueprints
- Re-run pilot on only those blueprints
- Re-score gate
- If unchanged → freeze and release

**If FAIL (Bronze or below):**
- Root cause analysis document
- Prioritise fixes from recurring edits (Section 4.1)
- Re-run full pilot with corrected system
- Re-score

---

## Appendices

### Appendix A — Program ID scheme

| Prefix | Sport |
|--------|-------|
| CRI | Cricket |
| RUG | Rugby |
| TEN | Tennis |
| BAD | Badminton |
| SOC | Soccer |

Full ID: `{SPORT}-{NN}` (e.g. `CRI-01`, `SOC-10`)

### Appendix B — Coach qualification criteria

Each coach must:
- Hold recognised S&C certification (CSCS, UKSCA, ASCA, or equivalent)
- Minimum 3 years practical coaching experience
- Currently coaching at least one of the 5 target sports
- Not involved in FORGE development (blind review)

### Appendix C — Turnaround timeline

| Day | Activity | Owner |
|-----|----------|-------|
| 1 | Generate 50 programs, anonymise, packet-assign | Engineer |
| 1 | Distribute packets to coaches (email + PDF + CSV) | Engineer |
| 2–8 | Coach review window (7 calendar days) | Coaches |
| 8 | Reminder if not returned (48 hr) | Engineer |
| 9–10 | Output extraction, edit distance calculation | Engineer |
| 10 | Failure analysis, gate scorecard, release decision | Engineer + Lead Coach |

### Appendix D — Budget estimate

| Item | Count | Rate | Total |
|------|-------|------|-------|
| Coach honorarium | 5 | $150 | $750 |
| Data processing | 1 | $200 | $200 |
| Contingency (20%) | — | — | $190 |
| **Total** | | | **$1,140** |

### Appendix E — Risk register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Coach drops out mid-study | Low | High | 2× coverage (every program seen by 2 coaches); N=3 minimum still valid |
| Coach misinterpretation of "credibility" | Medium | Medium | Provide written examples and anchored scale (1 = "never", 10 = "exactly") |
| Programs too similar across sports | Low | Low | Stratify by sport, level, equipment, season phase |
| Edit distance not parseable from free text | Medium | Medium | Provide CSV template; accept manual extraction as fallback |
| All coaches from same sport background | Low | High | Recruit one coach per sport minimum |

---

## References

- `FORGE_HARDENING_PHASE_V1.md` — baseline hardening (0 crashes, 119 tests)
- `FORGE_PROGRAM_EDIT_DISTANCE_AUDIT_V1.md` — edit distance model definition
- `FORGE_SESSION_ARCHITECTURE_AUDIT_V1.md` — architectural baseline
- `FORGE_EXERCISE_LIBRARY_V2.md` — 241 exercises, 15 families

---

*End of protocol. Execute Part 1 when ready to begin pilot.*
