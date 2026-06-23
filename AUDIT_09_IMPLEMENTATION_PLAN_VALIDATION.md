# AUDIT #9 — IMPLEMENTATION PLAN VALIDATION

**Role:** Principal Staff Engineer + Production Systems Architect + Sports Science Platform Reviewer  
**Date:** 2026-06-17  
**Rule:** Do NOT produce another architecture review. Validate proposed fixes. Attack assumptions. Find flaws in the audit recommendations themselves.

---

## SECTION 1 — RECOMMENDATION VALIDATION MATRIX

### 1. Delete 6 Dead Services

**Audit #8 Says:** Delete `athlete_state_engine`, `training_load_engine`, `injury_risk_engine`, `assessment_metric_engine`, `demand_lifecycle_engine` (keep service classes), and 5 router mounts from `demand_scoring_engine.app`.

**Verdict: PARTIALLY AGREE — dangerous oversimplification**

| Dimension | Assessment |
|-----------|-----------|
| Risk if implemented | **MODERATE.** These services ARE dead code (~2,700 LOC). But they contain domain logic that is NOT preserved elsewhere. `assessment_metric_engine.py:250-320` has the only z-score-based deficit computation. `demand_lifecycle_engine.py:148-228` has the only ACWR/recovery/fatigue/injury- risk-aware scoring. Deleting these files before extracting the domain logic destroys the reference implementation. The "keep service classes in archive" recommendation is hand-wavy — archived files rot and are never revived. |
| Risk if not implemented | **LOW.** They're already dead. They don't cause bugs. They add ~2,700 LOC of cognitive load but don't affect production output. The risk is mostly developer confusion and the false impression of integration. |
| Complexity | **TRIVIAL** (1 day) — remove router mounts, delete file references. |
| Alternative approach | **Do NOT delete the files.** Instead: (1) Remove the 5 `app.include_router()` calls from `demand_scoring_engine.py:52-56` (this stops the false advertising). (2) Extract the z-score deficit formula from `assessment_metric_engine.py:250-320` into a standalone function `compute_zscore_deficit()` and move it to a `scoring_utils.py` module. (3) Extract the lifecycle engine's rich scoring formula into `demand_scoring_engine.py` as a `compute_risk_adjusted_score()` function. THEN delete the original files. |
| Final recommendation | **MODIFY.** Don't delete first. Extract first. The audit's order (Delete → Unify → Wire) is wrong for items #2 and #3 because it would destroy the reference implementations before the unification is complete. |

---

### 2. Consolidate to One Deficit Engine

**Audit #8 Says:** "Make `assessment_metric_engine` z-scores the SINGLE authority. Delete raw-score heuristic."

**Verdict: DISAGREE — wrong engine chosen as authority**

| Dimension | Assessment |
|-----------|-----------|
| Risk if implemented | **HIGH.** The z-score system requires `metric_norms` table with population means and standard deviations. Currently this table has mock data (mean=40, std=5 for CMJ). In production, metric norms don't exist generically — they are sport-specific, and often position-specific. A z-score computed against generic norms is WORSE than a raw-score heuristic because it creates a false sense of scientific precision. The z-score formula `severity = max(0, min(1, -z/3))` with hardcoded `/3` denominator is NO LESS arbitrary than `1 - min(raw/50, 1)`. |
| Risk if not implemented | **HIGH.** Currently 3 deficit systems produce different values for the same input (CMJ z=-1.8 → deficit=0.6 in metric_engine, 0.38 in demand_scoring_engine). This WILL destroy coach trust. |
| Complexity | **MEDIUM** (3-5 days) — requires deciding which system is correct, not just which is more scientifically valid-sounding. |
| Alternative approach | **Keep the benchmark-based engine from deficit_detection_engine.py as the SINGLE authority.** Why? (1) It's the only system actually used by the V1 pipeline that works end-to-end. (2) Its logic is backed by the `benchmarks` table with sport-specific thresholds, not hardcoded denominators. (3) It produces categorical deficits (Power Deficit, Acceleration Deficit) that feed directly into template selection. The z-score engine produces continuous severity values that map to demands — a fundamentally different output. These are NOT substitutable. The right architecture is: benchmark engine → categorical deficit → template selection (V1 path), AND benchmark engine → continuous severity → demand scoring (V2 path). One input, two output formats. |
| Final recommendation | **MODIFY.** Keep deficit_detection_engine.py as the single source of truth. Remove the z-score engine's independent deficit computation (it's never been used in production and has no validated norms table). Move the z-score FORMULA into deficit_detection_engine.py as an optional refinement layer, but do NOT make it the authority until metric_norms are populated with real sport-specific data. The audit picked the wrong winner. |

---

### 3. Consolidate to One Demand Scoring Engine

**Audit #8 Says:** "Fold demand_lifecycle_engine's richer formula (ACWR, recovery, fatigue, injury) into demand_scoring_engine. Delete lifecycle engine."

**Verdict: AGREE — but the audit underestimates the difficulty**

| Dimension | Assessment |
|-----------|-----------|
| Risk if implemented | **MEDIUM.** The lifecycle engine's formula multiplies 5 adjustment factors (injury × ACWR × recovery × fatigue × role). If ANY of these factors is unavailable or unreliable, the adjusted score becomes garbage. For example: if `fatigue` is not being tracked (which is the current state), the system crashes or produces silent zeros. The audit correctly identifies the need but doesn't specify the fallback strategy for missing factors. |
| Risk if not implemented | **MEDIUM-HIGH.** Two scoring systems = impossible explainability. The 455% discrepancy (138.0 vs 24.87) for the same demand is an auditability nightmare. |
| Complexity | **HIGH** (5-10 days). This isn't copy-paste. The lifecycle engine has different request/response models, different async patterns, and different error handling. The ACWR adjustment logic at `demand_lifecycle_engine.py:180-185` hardcodes zone thresholds (0.8, 1.0, 1.3, 1.5) that need to be configurable. Simply "folding in" without redesigning the configuration model repeats the same hardcoding mistake. |
| Alternative approach | **Create a new `DemandAdjuster` class** with pluggable factor modules: `ACWRAdjuster`, `RecoveryAdjuster`, `FatigueAdjuster`, `InjuryRiskAdjuster`. Each has a `can_compute()` check that returns `(adjustment, confidence, reason)`. If `can_compute()` returns confidence < 0.5, that factor defaults to 1.0 (no adjustment) and logs the gap. This prevents the "missing data → garbage output" failure mode. Only after this, delete the lifecycle engine. |
| Final recommendation | **AGREE WITH MODIFICATION.** The goal is correct. The approach (delete first, fold later) is wrong. Build the `DemandAdjuster` with graceful degradation first, then delete. |

---

### 4. Replace Greedy Allocation with CSP Solver

**Audit #8 Says:** Replace the current exercise selection (greedy, sorted by score, no constraint awareness) with a Constraint Satisfaction Problem solver.

**Verdict: DISAGREE — premature optimization that will delay MVP**

| Dimension | Assessment |
|-----------|-----------|
| Risk if implemented | **HIGH.** A CSP solver is a new runtime dependency (OR-Tools or python-constraint). It introduces: (1) solver timeout risks, (2) non-deterministic output (most CSP solvers use random restarts), (3) cold-start tuning hell (constraint weights, variable ordering, search strategy). For a system that currently has 0 athletes in production, adding a CSP solver before proving the linear scoring model is wrong is architectural over-engineering. The audit's own analysis (Section 2.3 of design review) admits that CSP is only needed at 10K+ athletes and that heuristic approaches work fine for <100 athletes. There are 0 production athletes. |
| Risk if not implemented | **LOW-MEDIUM.** The current greedy allocation has known issues: (1) all three equal-scored exercises rank arbitrarily, (2) no diversity constraint, (3) no fatigue budget. But these can be fixed with simple deterministic tiebreakers and post-hoc filters without a CSP solver. |
| Complexity | **VERY HIGH** (3-4 weeks for first working version, ongoing tuning). |
| Alternative approach | **Phase 1 (MVP):** Keep greedy scoring. Add (a) deterministic tiebreaker: `secondary_score = movement_pattern_variety_score × 0.1 + exercise["name"]` for reproducibility, (b) post-hoc diversity filter: ensure no more than N exercises from same movement pattern per session, (c) equipment availability filter (already partially implemented). **Phase 2 (Beta):** If empty-recommendation rate exceeds 5% or coach override rate exceeds 40%, THEN consider CSP. Otherwise, greedy + rules is good enough for 500 athletes. The audit itself shows greedy is fine up to 100 athletes (Section 2.2 of design review), and the pilot is capped at 500. |
| Final recommendation | **REMOVE.** CSP is a Phase 2 optimization that the audit incorrectly placed in the MVP critical path. It's the single most expensive item on the list with the lowest marginal benefit at current scale. |

---

### 5. Add Competition Calendar Immediately

**Audit #8 Says:** "Add `competition_events` table. Add proximity flag to scoring. Create red zone constraint."

**Verdict: PARTIALLY AGREE — scope is too large**

| Dimension | Assessment |
|-----------|-----------|
| Risk if implemented | **LOW-MEDIUM.** The calendar itself is simple (table + CRUD). The risk is in the RED ZONE LOGIC — what happens when competition is within N days? The audit says "reduce volume by 30% for events within 7 days of competition" but doesn't specify: what about the ACWR interaction? What if the athlete has competition every week (tournament season)? The simple model (competition in 5 days → taper) conflicts with the simple progression model (Week 1-4 Base/Accumulation/Peak/Deload). These two time models interact in complex ways. |
| Risk if not implemented | **CRITICAL.** The program builder currently generates Week 3 (Peak at 85% 1RM) ON competition day. This is a safety issue, not just a quality issue. A coach who sees this will immediately lose trust in the system. |
| Complexity | **MEDIUM** (3-5 days for table + basic proximity flag + simple red zone logic). But could expand to 2+ weeks if the seasonal interaction is addressed. |
| Alternative approach | **Start with just the calendar table and a proximity flag in the response.** Do NOT implement automatic red zone adjustments in MVP. Instead: store competition dates in `competition_events`, show "Competition in N days" in the program output, let the coach manually adjust. The system should flag (not fix) competition proximity. Add auto-adjustment in Beta once the rules are validated by real coaches. This is a case where "build it and they will come" data collection is safer than implementing untested rules. |
| Final recommendation | **MODIFY.** Add the table and CRUD. Storage for future rules is cheap. Implementing unvalidated red zone logic before seeing real usage patterns will produce wrong rules that coaches learn to ignore. Flag, don't fix. |

---

### 6. Add Exposure Planning Before MVP

**Audit #8 Says:** "Add `exposure_targets` table, compute weekly frequency per demand, filter exercises by exposure."

**Verdict: DISAGREE — scope creep masquerading as critical path**

| Dimension | Assessment |
|-----------|-----------|
| Risk if implemented | **MODERATE.** Exposure planning introduces a new domain entity with its own configuration surface (exposure targets per sport/role/phase/training-age). As the audit's own analysis shows, this can explode to 128K rows at 100 sports. Adding this before the basic pipeline works end-to-end is building infrastructure for a capability we haven't validated. |
| Risk if not implemented | **LOW.** The current system selects exercises per demand without exposure targets. The resulting program is still a valid program — it just may under-emphasize some demands and over-emphasize others. This is a quality issue, not a safety issue. Unlike competition proximity (which can cause injury), suboptimal exposure distribution is a tuning problem. |
| Complexity | **HIGH** (5-10 days). Requires: new table, new CRUD endpoints, integration into demand scoring loop, configuration UI planning. |
| Alternative approach | **Postpone to Beta.** Replace with a simpler heuristic: "top 3-4 demands (by priority × deficit) get exercises selected, remaining demands get 0-1 exercises." This is essentially what the current greedy system does implicitly. Make it explicit with a simple priority cap, then build exposure targets when there's real data on which exposures coaches actually use. |
| Final recommendation | **REMOVE FROM MVP.** Move to Beta (Phase 2 of audit's own timeline). The 6-week MVP estimate should NOT include exposure planning. |

---

### 7. Add Objective Planning Before MVP

**Audit #8 Says:** "Add `session_objectives`, assign primary/secondary/tertiary per session."

**Verdict: DISAGREE — pure scope creep**

| Dimension | Assessment |
|-----------|-----------|
| Risk if implemented | **LOW-MODERATE.** Objectives are useful for explainability ("this session focuses on Vertical Power"). But building objective assignment logic requires: (1) deciding how many objectives per session, (2) whether objectives are per-session or per-microcycle, (3) how objectives cascade from demands, (4) what happens when objectives conflict. Each of these is a design decision with no right answer, and getting it wrong means rework. |
| Risk if not implemented | **LOW.** The system currently goes from demand scores → exercise selection directly and produces a valid program. Objectives are a documentation layer on top of this — they explain the intent without changing the selection. |
| Complexity | **MEDIUM** (3-5 days for basic version, infinite for correct version). |
| Alternative approach | **Do not build objective entities.** Instead, just annotate the demand scores with their priority rank. "Vertical Power (Highest Priority, Score 138)" is effectively an objective without requiring a new aggregate. Add formal objectives only when coaches ask "what's the focus of this session?" and the demand-based answer isn't sufficient. |
| Final recommendation | **REMOVE FROM MVP.** This is a documentation feature, not a pipeline feature. The pipeline works without it. Ship without it, collect coach feedback, add objectives in Beta if coaches request them. |

---

### 8. Add Session Sequencing Before MVP

**Audit #8 Says:** "Order exercises within session by movement pattern (power before strength, low fatigue before high fatigue)."

**Verdict: AGREE — but the audit underestimates the simplicity**

| Dimension | Assessment |
|-----------|-----------|
| Risk if implemented | **LOW.** Exercise ordering is a sorting problem. The current modulo-based rotation in program_builder is demonstrably wrong (it alternates exercises but doesn't follow potentiation principles). Any fixed ordering heuristic is better than the current approach. |
| Risk if not implemented | **MEDIUM.** The current program has exercises in arbitrary order within each session. For the elite fast bowler program, Slot 201 (power) appears first, but the second session puts Slot 204 (core rotation) before power. This violates basic potentiation principles (CNS-intensive work should precede fatigue-inducing work). It's not dangerous, but it's suboptimal and a coach will notice. |
| Complexity | **LOW** (1-2 days). Sort by: (1) movement pattern priority order (Power → Strength → Hypertrophy → Core → Accessory), (2) within same priority, sort by fatigue cost descending. This is a 20-line function, not a "sequencing engine." |
| Alternative approach | **Do exactly what the audit says but keep it simple.** 1 day of work. No new tables. No new aggregates. Just a sort key on exercise classification and a stable sort at program assembly time. |
| Final recommendation | **AGREE.** Keep in MVP. But call it "exercise ordering" not "session sequencing." The latter implies a formal engine. The former is a sorting function. |

---

### 9. Postpone Periodization to V3

**Audit #8 Says:** "Full Periodization (macro/meso/microcycles, block types, loading trajectories) → postpone to V3."

**Verdict: AGREE — this is the right call**

| Dimension | Assessment |
|-----------|-----------|
| Risk if implemented | **CRITICAL.** Building periodization requires rethinking the entire program generation timeline. The current system generates 4-week blocks with hardcoded Base→Accumulation→Peak→Deload. Adding mesocycle aggregates, loading trajectories, and block types would add 3-4 months to MVP and would likely require rewriting program_builder.py from scratch. |
| Risk if not implemented | **LOW-MEDIUM.** The system will generate 4-week blocks that don't adapt to the season calendar. This is a quality limitation, not a safety issue. Elite coaches will want periodization, but for MVP (one sport, basic pipeline), 4-week blocks are acceptable. |
| Complexity | **VERY HIGH** (12-16 weeks). Periodization touches every layer: data model, scoring, exercise selection, progression, competition integration. |
| Final recommendation | **AGREE.** Postpone to V3. But DOCUMENT the decision explicitly in the system architecture so future engineers don't design around an assumption of periodization support. |

---

### 10. Postpone LTAD to V3

**Audit #8 Says:** "LTAD (biological age, PHV, sensitive periods) → postpone to V3."

**Verdict: AGREE — but with a critical caveat**

| Dimension | Assessment |
|-----------|-----------|
| Risk if implemented | **HIGH.** LTAD adds an entirely new domain (biological maturation, PHV windows, sensitive periods) that changes how deficits are interpreted AND how exercises are selected. A 14-year-old in PHV has DIFFERENT exercise selection criteria than a 24-year-old with the same `training_age`. Implementing LTAD without the underlying periodization and adaptation models would produce scientifically wrong recommendations. |
| Risk if not implemented | **LOW-MEDIUM.** If the pilot is restricted to adult athletes (18+), LTAD is irrelevant. If youth athletes enter the system, LTAD becomes CRITICAL. The audit doesn't specify the pilot athlete age range. The risk is that a youth athlete gets an adult-modified program (training_age adjusted but no maturation awareness) and gets injured. |
| Complexity | **VERY HIGH** (8-12 weeks). |
| Alternative approach | **Explicitly restrict MVP to adult athletes (18+)** via system configuration or athlete validation. Document this as a known limitation. Add LTAD as a V3 bounded context with the understanding that any youth athlete data entered during V2 will need to be re-processed when LTAD goes live. |
| Final recommendation | **AGREE WITH CAVEAT.** Postpone LTAD but establish a hard boundary: MVP/Beta supports adult athletes only. Youth athlete support is treated as a new feature, not an iteration. The pilot agreement must explicitly exclude youth athletes. |

---

### 11. Postpone RTS/Rehab to V3

**Audit #8 Says:** "Rehabilitation / Return-to-Sport → postpone to V3."

**Verdict: STRONGLY AGREE**

| Dimension | Assessment |
|-----------|-----------|
| Risk if implemented | **CRITICAL.** Rehab is NOT performance programming with modified weights. It's a different domain with different goals (tissue healing vs. performance adaptation), different progression criteria (pain-free range of motion vs. load progression), and different safety constraints. Combining rehab and performance in the same pipeline without a clear domain boundary will produce programs that are either too aggressive (re-injury) or too conservative (no adaptation). |
| Risk if not implemented | **NONE.** Rehab is a separate product from performance programming. The system should produce programs for HEALTHY athletes. Injured athletes should be in a rehab protocol managed outside the system (or by a separate module). |
| Complexity | EXTREMELY HIGH (16+ weeks for minimum viable rehab module). |
| Final recommendation | **AGREE.** But stronger: do NOT just postpone — explicitly DECLARE that FORGE V2 is for healthy athlete performance programming ONLY. Document this as a product scope boundary, not just a technical postponement. Rehab/RTS is a separate product line. |

---

## SECTION 2 — BUILD SEQUENCE REVIEW

### Audit #8 Proposed Sequence: Wipe → Unify → Wire → Build → Test

**Verdict: THE ORDER IS WRONG.**

The audit's sequence has a fundamental flaw: it deletes the reference implementations (Wipe) BEFORE extracting their domain logic (Unify). This is a recipe for losing institutional knowledge.

### Corrected Sequence:

| Phase | Proposed | Corrected | Why |
|-------|----------|-----------|-----|
| 1 | Wipe | **STOP** | Don't delete anything yet. Assess what the dead services actually contain. |
| 2 | Unify | **EXTRACT** | Copy valuable formulas from dead services into shared modules (`scoring_utils.py`, `demand_adjuster.py`). |
| 3 | Wire | **FIX FAILURES** | Fix the 4 failing tests first. They indicate real bugs, not test issues. |
| 4 | Build | **WIPE** | NOW delete the dead service files (after formulas are extracted). |
| 5 | Test | **WIRE** | Connect the real repositories. Make PostgreSqlDemandRepository the default. |
| 6 | — | **ADD** | Competition calendar table + CRUD. Exercise ordering. Config snapshots. |
| 7 | — | **BUILD** | Only items that survived the cut: competition flag, exercise ordering, ACWR read. |
| 8 | — | **TEST** | End-to-end V2 pipeline test. |

### Why Wipe-First Is Wrong

1. **Cognitive load is not technical debt.** The dead services add 2,700 lines of code but they also contain the ONLY implementations of z-score deficit computation, ACWR-adjusted scoring, and multi-factor demand scoring. Deleting them before extracting these formulas means the formulas are lost unless someone re-reads git history. "Archived" files are never revived.
2. **Context-dependent understanding.** The wipe phase is estimated at 1 day. Realistically, safely deleting 5 services with cross-file dependencies, duplicate functions, and partial references requires 3-5 days of careful analysis. The 1-day estimate reflects the "just delete it" mentality that leads to accidental deletions.
3. **Psychological impact.** Deleting 2,700 lines of tested code creates pressure to "have something to show for it." This leads to rushed unification and wiring. The proper approach is to extract first, which produces visible output (new shared modules) before any deletions.

---

## SECTION 3 — CRITICAL PATH ANALYSIS

### Critical Path (minimum sequence, no parallelism)

```
Extract deficit formulas from dead code (2d)
  → Extract demand adjustment formulas (2d)
  → Fix 4 failing tests (1d)
  → Remove dead router mounts (0.5d)
  → Delete dead service files (0.5d)
  → Unify deficit engine: single authoritative layer (3d)
  → Unify demand scoring: DemandAdjuster with graceful degradation (5d)
  → Add competition calendar table + basic CRUD + proximity flag (3d)
  → Add exercise ordering (1d)
  → Add recommendation_id FK to programs table (0.5d)
  → Add config snapshot to recommendation_log (0.5d)
  → Wire ACVR view query into demand scoring (1d)
  → Demote MockDemandRepository: make PostgreSql default (2d)
  → Remove inline V2 scoring from integration_workflow (1d)
  → Wire program_builder to V2 endpoint (2d)
  → End-to-end V2 integration test (3d)
```

**Total critical path: ~28 working days (5.5 weeks)**

### What's NOT on the Critical Path

- CSP solver (wrong for MVP)
- Exposure targets (scope creep)
- Objective planning (documentation feature)
- Periodization (V3)
- LTAD (V3)
- RTS/Rehab (V3)

### Longest Pole in the Tent

**Demand scoring unification (5 days).** The DemandAdjuster with graceful degradation for missing factors is the single most complex and risk-prone item. It requires:
- Understanding both existing scoring formulas
- Designing the pluggable adjuster interface
- Handling all missing-data edge cases
- Maintaining backward compatibility with existing API responses

This is also the item most likely to encounter hidden complexity. The ACWR adjustment logic alone has 4 hardcoded zone thresholds that need to be extracted to configuration.

**Second longest pole: Deficit engine unification (3 days).** Picking the wrong authority (as the audit does — z-score instead of benchmark) would require rework. If benchmark is chosen as authority, the work involves:
- Adding continuous severity output to benchmark engine
- Removing the independent heuristic from demand_scoring_engine
- Ensuring all pipeline consumers get consistent deficit values
- Tests that prove V1 and V2 produce the same deficit for the same input

### Hidden Dependencies

1. **ACWR view → PostgreSql as default.** The ACWR view (`acute_chronic_load_view`) exists in the database. But it requires `training_load_events` to be populated. If PostgreSqlDemandRepository is made the default before there's real data in `training_load_events`, the ACWR factor will always be NULL → graceful degradation to 1.0 → ACWR is invisible until someone populates load data. The system will appear to work but ACWR will have zero effect. This is a silent failure.

2. **Config snapshots → reproducibility.** Adding config snapshots to `recommendation_log` is 0.5 days of work. But once added, the system must actually USE them for reproducibility, which requires versioning config tables with `valid_from/valid_until`. This cascades to: `role_demand_priority`, `exercise_demand_mapping`, `assessment_demand_mapping`. The audit lists config snapshots as 1 day but the downstream dependency is 5-10 days.

3. **PostgreSqlDemandRepository → seed data quality.** The audit assumes the real data in `performance_demands`, `role_demand_priority`, and `exercise_demand_mapping` tables is correct. Based on the template_inventory_audit and deficit_template_mapping_audit, there are duplicate taxonomies (CMJ vs Force Plate CMJ, Power Deficit vs RFD Deficit) and missing mappings (Power Deficit not mapped to Cricket Fast Bowler Power). Making PostgreSql the default before cleaning up the seed data will produce wrong recommendations from real data — worse than mock data.

### Potential Rework Traps

1. **Trap #1: Delete dead code → lose reference formulas.** Already discussed. Prevention: extract first, delete second.

2. **Trap #2: Make PostgreSqlDemandRepository default → wrong recommendations from bad seed data.** The mock repositories have curated data tuned to produce good-looking programs for Cricket Fast Bowlers. The real database has duplicate taxonomies and missing mappings. Switching to real data without auditing the seed data first will produce worse programs than mock data. Prevention: audit + fix seed data BEFORE switching repositories.

3. **Trap #3: Wire ACWR into scoring → silent null factor (no crash, no warning).** If the ACWR view returns NULL (because `training_load_events` is empty), the demand adjuster returns 1.0 (no adjustment). The system produces programs that LOOK correct but ignore ACWR entirely. A coach sees "ACWR-aware program generation" in the feature list but observes no actual behavior change. Prevention: log a warning when any adjustment factor defaults to 1.0 due to missing data. Make this visible in the API response.

4. **Trap #4: Add competition proximity flag → no actual behavior change.** If the competition flag is added to the response but the scoring formula doesn't use it, coaches see "Competition in 5 days: YES" but the program hasn't changed. This creates the impression of a feature that doesn't work. Prevention: either implement the red zone adjustment OR don't show the flag in coach-facing output. Internal logging only until the adjustment logic exists.

5. **Trap #5: Remove inline V2 scoring → response format drift.** The inline scoring in `integration_workflow.py` produces a V1-format response. The `get_demand_recommendations()` endpoint produces a V2-format response. If the integration_workflow switches to calling the V2 endpoint, the response format changes. Downstream consumers (program_builder, session_generator) may break. Prevention: add a response format adapter in the integration_workflow layer.

---

## SECTION 4 — THE 16-WEEK QUESTION

### "If a single senior engineer had 16 weeks, what is the minimum set of work required to create a production-credible FORGE V2?"

**Answer:** Production-credible means: real data, one sport, end-to-end pipeline, no silent failures, coach can trust the output, system can explain its decisions.

### Minimum Set (16 weeks, 1 senior engineer)

| Week | Work | Risk Level |
|------|------|-----------|
| 1-2 | **Extract phase:** Copy z-score formula, lifecycle formula into `scoring_utils.py`. Design `DemandAdjuster` with graceful degradation. Fix the 4 failing tests. Audit seed data quality. Fix duplicate taxonomies in migration data. | MEDIUM |
| 3 | **Clean phase:** Remove dead router mounts (only). Delete dead service files. Keep the extracted formulas. | LOW |
| 4-5 | **Unify deficit engine:** Single benchmark-based authority with optional z-score refinement. Remove independent heuristic from demand_scoring_engine. Add continuous severity output to benchmark engine. Write regression tests proving V1=V2 deficits for same input. | HIGH |
| 6-7 | **Unify demand scoring:** Build DemandAdjuster with ACWR (reads `acute_chronic_load_view`), recovery, fatigue, injury risk factors. Each factor has `can_compute()` → graceful fallback. Wire into demand_scoring_engine. | HIGH |
| 8 | **Add competition calendar:** `competition_events` table, basic CRUD, proximity flag in response (no auto-adjustment yet). | LOW |
| 9 | **Add exercise ordering:** Sort function in program builder. Power → Strength → Core → Accessory within each session. | LOW |
| 10-11 | **Wire real repositories:** Make PostgreSqlDemandRepository default. Fix seed data. Add missing benchmarks (pull up, rotational med ball throw) to match 7 claimed deficits. Wire ACWR view. | HIGH |
| 12 | **Pipeline integration:** Remove inline V2 scoring. Route integration_workflow V2 through `POST /api/v2/demand-recommendations`. Add response adapter for backward compat. Wire program_builder to V2 endpoint. | MEDIUM |
| 13 | **Observability:** Add config snapshot to recommendation_log. Add recommendation_id FK to programs. Add explainability fields to response (score decomposition, tiebreaker reason, competition proximity flag). | MEDIUM |
| 14-15 | **Testing:** End-to-end V2 integration test. Regression tests: V1 vs V2 output consistency. Determinism test: same input → same output. Competition proximity test. Empty-state tests (no training load, no assessments). | MEDIUM |
| 16 | **Documentation + deployment setup:** API reference, coach's manual, deployment guide, migration rollback scripts, README update. | LOW |

### What's EXCLUDED (explicitly out of scope)

- UI (no dashboard, no coach interface — API only)
- CSP solver (greedy + deterministic tiebreaker is sufficient)
- Exposure planning (postpone to Beta)
- Objective planning (postpone to Beta)
- Periodization (V3)
- LTAD (V3)
- RTS/Rehab (V3)
- Multi-tenant (V3)
- Coach feedback learning (V3)
- Performance optimization beyond basic indexing (done at 10K athlete scale)
- Background jobs (manual triggers for MVP, Celery in Beta)
- Config UI (manual config via API for MVP)
- Auth/RBAC (assume trusted network for pilot)

### What the System Will Do at Week 16

```
POST /api/v2/athlete-workflow
  → Create athlete (real DB)
  → Record assessment (real DB)
  → Detect deficits (benchmark engine → continuous severity)
  → Compute demand scores (with ACWR adjustment, graceful fallback for missing factors)
  → Add competition proximity flag (no auto-adjustment)
  → Select exercises (greedy with deterministic tiebreaker + diversity filter)
  → Order exercises within session (Power → Strength → Core → Accessory)
  → Generate 4-week program with progression (existing V1 logic)
  → Persist to real DB tables
  → Log to recommendation_log with config snapshot
  → Return explainable response (score decomposition, tiebreaker reason, competition flag)
```

### What the System Will NOT Do at Week 16

- Adapt to competition dates automatically
- Plan exposure targets across the microcycle
- Assign session objectives
- Periodize into mesocycles
- Handle youth athletes (LTAD)
- Manage rehab protocols
- Learn from coach feedback
- Support team/squad management
- Provide a coach-facing UI

---

## SECTION 5 — FINAL OUTPUT

### 1. Recommendations to Keep

| # | Recommendation | Keep As-Is |
|---|---------------|-----------|
| 5 | Competition calendar table + CRUD | YES — but flag only, no auto-adjustment |
| 8 | Exercise ordering within session | YES — but scope as sorting, not an engine |
| 9 | Postpone periodization to V3 | YES |
| 10 | Postpone LTAD to V3 | YES — with adult-athlete-only restriction |
| 11 | Postpone RTS/Rehab to V3 | YES — stronger: declare out of product scope |

### 2. Recommendations to Modify

| # | Recommendation | Modified Version |
|---|---------------|-----------------|
| 1 | Delete 6 dead services | **EXTRACT FIRST.** Remove router mounts immediately. Extract formulas into shared modules. THEN delete service files. |
| 2 | Consolidate to one deficit engine | **BENCHMARK-BASED as authority, not z-score.** Z-score is a refinement, not a replacement. Deficit is 2-output: categorical (templates) and continuous (demand scoring). |
| 3 | Consolidate to one demand scoring engine | **Build DemandAdjuster with pluggable factors and graceful degradation.** Delete lifecycle engine only after DemandAdjuster is tested. |
| 5 | Add competition calendar immediately | **Add table + CRUD + proximity flag. No auto-adjustment until Beta.** |

### 3. Recommendations to Remove

| # | Recommendation | Reason for Removal |
|---|---------------|-------------------|
| 4 | Replace greedy allocation with CSP solver | Premature optimization. Greedy + deterministic tiebreaker + diversity filter is sufficient for 500 athletes. CSP adds 3-4 weeks with zero marginal benefit at current scale. The audit's own analysis proves this. |
| 6 | Add exposure planning before MVP | Scope creep. The system works without it. Quality issue, not safety issue. Postpone to Beta. |
| 7 | Add objective planning before MVP | Documentation feature, not pipeline feature. Demand scores already imply priority. Postpone to Beta. |

### 4. Revised Roadmap

| Phase | Weeks | What | Dependencies |
|-------|-------|------|-------------|
| **EXTRACT** | 1-2 | Extract formulas from dead code. Fix 4 failing tests. Audit seed data quality. | None |
| **CLEAN** | 1 | Remove router mounts. Delete dead service files. | Extract |
| **UNIFY** | 3 | Single deficit authority. Single demand scoring with DemandAdjuster. | Clean |
| **WIRE** | 3 | PostgreSql repositories as default. ACWR integration. Competition calendar. | Unify |
| **INTEGRATE** | 2 | Pipeline cleanup. Remove inline V2 scoring. Wire program_builder to V2 endpoint. | Wire |
| **OBSERVE** | 1 | Config snapshots. recommendation_id FK. Explainability fields. | Integrate |
| **TEST** | 2 | End-to-end tests. Regression tests. Determinism tests. Empty-state tests. | Observe |
| **LAUNCH** | 1 | Documentation. Deployment setup. | Test |
| **TOTAL** | **14-16 weeks** | MVP complete | — |

### Revised Sequence: Extract → Clean → Unify → Wire → Integrate → Observe → Test → Launch

The original sequence (Wipe → Unify → Wire → Build → Test) is inverted at the start. Wipe should be Clean and should come AFTER Extract.

### 5. Revised Timeline

| Milestone | Original (Audit #8) | Revised | Delta |
|-----------|-------------------|---------|-------|
| Cleanup | 1 week | 3 weeks (Extract 2 + Clean 1) | +2 weeks |
| Unification | 2 weeks | 3 weeks | +1 week |
| Wiring | 5 weeks | 3 weeks (no CSP, no exposure, no objectives) | -2 weeks |
| Building | 6 weeks | 3 weeks (Integrate 2 + Observe 1) | -3 weeks |
| Testing | 1 week | 2 weeks | +1 week |
| **Total MVP** | **15 weeks** | **14-16 weeks** | **~same** |

**The timeline is similar, but the confidence is higher.** The revised plan cuts 5 weeks of scope (CSP, exposure, objectives) and reinvests them in Extract phase (defusing the "delete before understanding" trap) and testing. The output quality at week 16 is higher because the codebase is cleaner, the data is audited, and the system is actually tested.

### 6. Final Confidence Score

| Criterion | Audit #8 Plan | Revised Plan | Delta |
|-----------|:------------:|:------------:|:-----:|
| Technical correctness | 6/10 | 8/10 | +2 |
| Realism of effort estimates | 5/10 | 7/10 | +2 |
| Risk awareness | 4/10 | 8/10 | +4 |
| Scope discipline | 3/10 | 9/10 | +6 |
| Hidden dependency detection | 5/10 | 8/10 | +3 |
| Rework trap avoidance | 4/10 | 8/10 | +4 |
| **OVERALL** | **4.5/10** | **8/10** | **+3.5** |

**Confidence in Revised Plan: 8/10**

The 2-point gap reflects:
- **Uncertainty about seed data quality** (-0.5): The seed data audit reveals duplicate taxonomies and missing mappings that could take 1-2 weeks to fix. This is now in the critical path (Extract phase) but the effort is uncertain.
- **Single engineer risk** (-0.5): A single senior engineer working alone has no code review, no backup, and significant context-switching. The timeline assumes uninterrupted focus, which is unrealistic.
- **Integration surprises** (-0.5): The V1→V2 pipeline integration has unknown response format drift. The inline scoring in integration_workflow produces different output shape than the V2 endpoint. The adapter layer may reveal incompatibilities.
- **PostgreSql data quality** (-0.5): The existing seed data in `performance_demands`, `role_demand_priority`, `exercise_demand_mapping` tables has never been consumed by the pipeline. There may be structural issues (missing FKs, wrong data types) that only surface when the pipeline actually reads them.

**To reach 9/10:**
1. Audit the seed data quality BEFORE starting the Extract phase (move from week 2 to week 0)
2. Add a second engineer for code review and parallel work (reduces single-person risk)
3. Run the V2 endpoint against the real DB in a staging environment before the Wire phase (surface integration surprises early)

---

## SECTION 6 — DIRECT CHALLENGES TO THE AUDIT

### Challenge 1: The audit over-prioritizes "delete dead code."

~2,700 lines of dead code is alarming. But this code is tested, documented, and represents months of domain modeling work. Deleting it is the EASIEST thing to do but not the MOST VALUABLE. The most valuable work is:
1. Extracting the formulas that ARE valuable (z-score, ACWR adjustment)
2. Understanding why they were never integrated (the domain knowledge gap)
3. Fixing the integration (making the pipeline actually call the V2 endpoint)

Rushing to delete before extracting will leave the system permanently poorer.

### Challenge 2: The audit chooses the wrong deficit authority.

Z-score deficits sound more scientific than benchmark-based deficits. But scientific validity requires valid norms. The `metric_norms` table has mock data (mean=40, std=5 for CMJ — for ALL sports). The benchmarks table has sport-specific, position-specific thresholds. For an MVP with one sport (Cricket) that has validated benchmarks, the benchmark engine is the CORRECT authority.

The audit's bias toward "newer = better" (assessment_metric_engine was built after deficit_detection_engine) leads to the wrong technical decision.

### Challenge 3: The audit's "6 weeks for MVP" is unrealistic.

The audit claims 30 working days (6 weeks) for MVP. But item #4 (CSP solver) alone is 3-4 weeks of that estimate. Removing CSP (as I recommend) leaves ~2 weeks for the remaining 13 items. But items #2-3 (deficit + demand unification) are each 3-5 days, totaling 6-10 days just for those. The math doesn't work.

The revised estimate of 14-16 weeks is more honest. The audit's 6-week MVP either assumes unrealistically fast execution or implicitly relies on the deleted dead code being resurrected (contradicting its own recommendation).

### Challenge 4: The audit sequence has an execution trap.

Wipe → Unify → Wire → Build → Test looks clean on paper. But "Unify" is impossible without the dead code's formulas, and the dead code is scheduled to be deleted in "Wipe." The engineer following this plan would either:
(a) Delete first, then struggle to recreate the formulas from memory/git history, or
(b) Read the code in Wipe, retain it mentally, delete it, then reproduce it in Unify — which is just "extract then delete" with extra steps and higher risk.

The correct sequence is Extract → Clean → Unify. The audit got the first two phases inverted.

### Challenge 5: The audit underestimates the seed data problem.

The audit's data model sections (design review Section 3) correctly identify that 15+ tables exist with no pipeline consumers. But the audit's implementation plan assumes that switching to PostgreSql repositories is simply a matter of changing the default factory return value. This ignores the quality of the existing seed data.

The deficit_template_mapping_audit reveals that:
- "Power Deficit" does NOT map to "Cricket Fast Bowler Power" template (a critical gap)
- Duplicate assessments (CMJ vs Force Plate CMJ) cause divergent template paths
- Missing benchmarks for "pull up" and "rotational med ball throw" cause 2 of the 4 failing tests

These are NOT minor issues — they are fundamental data quality problems that will produce wrong programs if the real database is used as-is. Fixing seed data is table-stakes before any repository switch.

---

## SECTION 7 — SUMMARY

```
Audit #8 was right about:
  ✓ Dead code needs cleanup
  ✓ Deficit unification is critical
  ✓ Demand scoring unification is critical
  ✓ ACWR must be wired into scoring
  ✓ Competition calendar is important
  ✓ Periodization/LTAD/Rehab should wait

Audit #8 was wrong about:
  ✗ Order of operations (Wipe before Extract)
  ✗ Deficit authority choice (z-score vs benchmark)
  ✗ CSP solver in MVP (premature)
  ✗ Exposure planning in MVP (scope creep)
  ✗ Objective planning in MVP (documentation feature)
  ✗ 6-week MVP timeline (underestimated by 2.5x)
  ✗ Seed data quality assumption (ignored entirely)
  ✗ Silent failure of ACWR with empty data (unhandled)
```

**The plan is salvageable. Fix the order (Extract before Clean), fix the authority (benchmark over z-score), remove the scope creep (CSP, exposure, objectives), and audit the seed data. Then the 16-week timeline is credible.**

**Revised confidence: 8/10**
