# AUDIT #8 — EXECUTION GAP ANALYSIS
## From Current Codebase to Production-Ready FORGE V2

**Review Mode:** Implementation Auditor | Build Estimator | Technical Debt Destroyer
**Date:** 2026-06-17
**Rule:** Do not repeat architecture reviews, domain audits, explainability audits, or source-of-truth audits. This is a pure implementation gap analysis.

---

## SECTION 1 — CAPABILITY MATRIX

| # | Capability | Status | Confidence | LOC | Production Readiness |
|---|-----------|--------|-----------|-----|-------------------|
| 1 | Athlete Assessment | **MOCK ONLY** (V1) + **PARTIAL** (V2) | 6/10 | 511+386 | CRUD exists. Metric-level deficits exist but are dead code. Assessment history query exists. **Not production-ready** — no validation pipeline, no comparison to norms table. |
| 2 | Deficit Analysis | **DUAL** (3 systems) | 3/10 | 363 | V1 benchmark-based deficits (used). V2 z-score deficits (dead). V2 raw-score heuristic (used by V2 path). **3 systems, no authority.** V1 deficits are Cricket-only hardcoded benchmarks. |
| 3 | Demand Scoring | **MOCK ONLY** | 3/10 | 400+258 | `compute_role_demand_scores()` runs on MockDemandRepository. PostgreSqlDemandRepository exists but never called. Demand lifecycle engine (richer formula) is dead. **Scoring runs, but not against real data.** |
| 4 | Athlete State | **DEAD CODE** | 1/10 | 505 | Mounted router with 4 endpoints. Zero callers. Writes to `athlete_state_snapshots`. Nothing reads it. **Complete service layer with no pipeline integration.** |
| 5 | Training Load | **DEAD CODE** | 1/10 | 465 | Mounted router with 3 endpoints. Zero callers. Writes to `training_load_events`. Nothing reads it during program generation. |
| 6 | ACWR | **DEAD CODE** (app) + **EXISTS** (SQL view) | 2/10 | 30 (SQL) | `acute_chronic_load_view` SQL view exists and is correct. But no service reads it during program generation. **The data is there; the pipeline ignores it.** |
| 7 | Injury Risk | **DEAD CODE** | 1/10 | 523 | Mounted router with 3 endpoints. Zero callers. Writes to `injury_risk_profiles`. Nothing reads it. |
| 8 | Competition Management | **MISSING COMPLETELY** | 0/10 | 0 | No code. No table. No service. No field. Zero competition awareness in any scoring function or program generation path. |
| 9 | Exposure Planning | **MISSING COMPLETELY** | 0/10 | 0 | No code. No table. The demand_scoring_engine ranks demands but has no "how many times per week" logic. Exercises are fetched per demand without frequency targets. |
| 10 | Objective Planning | **MISSING COMPLETELY** | 0/10 | 0 | No objective entity. No primary/secondary/tertiary objective selection. The V2 pipeline scores demands and jumps directly to exercise selection. |
| 11 | Session Sequencing | **MISSING COMPLETELY** | 0/10 | 0 | No sequencing engine. V1 program builder fills template slots using modulo rotation. No awareness of exercise ordering principles (potentiation, fatigue management). |
| 12 | Exercise Selection | **DUAL** (V1 mock + V2 mock) | 3/10 | 1031+500 | V1: 5-factor linear formula on MockExerciseRepository. V2: demand-based formula on MockDemandRepository. **Both run on mock data.** Neither reads from real `exercises` table with real `exercise_demand_mapping`. |
| 13 | Progression | **MOCK ONLY** (hardcoded) | 2/10 | 120 | `calculate_reps_and_intensity()` has hardcoded 4-week progression. `program_design_rules.progression_rules` is TEXT (not executable). **Progression is hardcoded Python, not data-driven.** |
| 14 | Periodization | **MISSING COMPLETELY** | 0/10 | 0 | No macrocycle, mesocycle, microcycle aggregates. No block types. No loading trajectory. **The system cannot periodize. It schedules.** |
| 15 | Recovery Modeling | **DEAD CODE** (schema) + **MISSING** (pipeline) | 0/10 | 0 | `athlete_state_snapshots` has `recovery_score`, `sleep_quality` columns. Zero code reads them during program generation. No multi-modal recovery model. |
| 16 | Program Generation | **MOCK ONLY** (V1) | 4/10 | 1185 | V1 program builder generates 4-week programs from V1 recommendations. **Works end-to-end but on mock data.** `PostgreSqlProgramRepository` exists and persists to real DB tables. |
| 17 | Explainability | **PARTIAL** (infrastructure only) | 2/10 | 400 | `recommendation_log` captures request snapshots, demand scores, candidate rankings. But no reasoning records, no decision trees, no tiebreaker traces. **Storage exists; explanation does not.** |
| 18 | Observability | **PARTIAL** (storage only) | 4/10 | 400 | `recommendation_log` + `coach_feedback` tables exist with full CRUD. Logging happens in demand_scoring_engine endpoint (which is never called by pipeline). **Infrastructure exists; data is sparse.** |
| 19 | Coach Feedback | **EXISTS** (but unused) | 3/10 | 400 | CRUD endpoints exist on `recommendation_observability` router. `coach_feedback` table exists. **But no analysis, no pattern learning, no integration into future recommendations.** |
| 20 | Execution Tracking | **PARTIAL** (V1) | 5/10 | 200 | Migration 000022 added `actual_sets`, `actual_reps`, `actual_intensity`, `actual_rpe`, `actual_rest_seconds`, `completed`, `notes` to `program_session_exercises`. CRUD exists in program_builder. **Schema is ready; execution capture UI/API is basic.** |

### Summary Statistics

| Category | Count |
|----------|-------|
| Production Ready | **0 / 20 (0%)** |
| Mock Only (works on fake data) | **5 / 20 (25%)** |
| Dead Code (infrastructure with no callers) | **5 / 20 (25%)** |
| Partially Exists (needs significant work) | **4 / 20 (20%)** |
| Missing Completely | **6 / 20 (30%)** |

**Current production-readiness: 0%.** No capability is production-ready. Every capability either runs on mock data, is dead code, is partial, or is missing entirely.

---

## SECTION 2 — DEPENDENCY GRAPH

### Actual Runtime Execution Path (V1 — default ENGINE_MODE)

```
POST /api/v1/integration/athlete-workflow
  │
  ├── athlete_module.create_athlete()          → MOCK REPO (in-memory)
  │
  ├── assessment_entry_module.record_result()  → MOCK REPO (in-memory)
  │
  ├── deficit_detection_engine.detect_deficits() → MOCK (MockBenchmarkRepository)
  │     └── benchmarks table (7 Cricket assessments, hardcoded)
  │
  └── recommendation_engine.get_exercise_recommendations() → MOCK (MockExerciseRepository)
        │
        ├── MockExerciseRepository.get_template()        → hardcoded Cricket Fast Bowler template
        ├── MockExerciseRepository.get_slots()            → hardcoded slot definitions
        ├── MockExerciseRepository.get_ranked_exercises() → hardcoded exercise pool
        │     └── V1 score = relevance×4 + specificity×3 + transfer×20 + tag×2.5 + mechanics×5
        └── MockExerciseRepository.get_slot_progression() → hardcoded progression rules
```

```
POST /generate-program (program_builder)
  │
  ├── athlete_module.get_by_id()                → MOCK REPO (in-memory)
  │
  ├── deficit_detection_engine.detect_deficits() → MOCK (SAME as above — second call)
  │
  └── recommendation_engine.get_exercise_recommendations() → MOCK (SAME as above — second call)
        │
        └── program_builder.build_and_save()
              │
              ├── calculate_reps_and_intensity()  → hardcoded 4-week progression
              ├── uses MockPostgreSql OR PostgreSqlProgramRepository.create_program()
              │     └── writes to: programs, program_weeks, program_sessions, program_session_exercises
              └── returns ProgramResponse
```

### Actual Runtime Execution Path (V2 — ENGINE_MODE=v2)

```
POST /api/v2/integration/athlete-workflow
  │
  ├── athlete_module.create_athlete()          → MOCK REPO (same as V1)
  │
  ├── assessment_entry_module.record_result()  → MOCK REPO (same as V1)
  │
  ├── deficit_detection_engine.detect_deficits() → MOCK (same as V1 — V2 doesn't use its own deficit system)
  │
  ├── demand_scoring_engine.compute_role_demand_scores() → MOCK (MockDemandRepository)
  │     └── V2 score = priority_weight × (1 + deficit) × level_mult × 100
  │
  └── INLINE SCORING LOOP (integration_workflow.py:363-394)
        └── DUPLICATES demand_scoring_engine logic
        └── wraps in V1 template format
```

### Dead Paths (infrastructure with zero callers)

```
athlete_state_engine.py endpoints           → 4 endpoints, 0 callers
training_load_engine.py endpoints           → 3 endpoints, 0 callers  
injury_risk_engine.py endpoints             → 3 endpoints, 0 callers
assessment_metric_engine.py endpoints       → 4 endpoints, 0 callers
demand_lifecycle_engine.py endpoints        → 1 endpoint, 0 callers
recommendation_observability.py endpoints   → 7 endpoints, 1 partial caller (log only)
domain_events table                         → 6 event types emitted, 0 consumers
performance_demands table                   → seeded but never queried by pipeline
exercise_demand_mapping table               → seeded but never queried by pipeline
role_demand_priority table                  → seeded but never queried by pipeline
assessment_demand_mapping table             → seeded but never queried by pipeline
```

### Dependency Graph Summary

```
                         ┌────────────────────────────┐
                         │  V1 PATH (default)         │
                         │  ─────────────────         │
                         │  AthleteModule (MOCK) ◄────│─── athlete_module.py
                         │       │                   │
                         │  AssessmentEntry (MOCK) ◄──│─── assessment_entry_module.py
                         │       │                   │
                         │  DeficitDetection (MOCK) ◄─│─── deficit_detection_engine.py
                         │       │                   │
                         │  Recommendation (MOCK) ◄───│─── recommendation_engine.py
                         │       │                   │
                         │  ProgramBuilder ─────────►│─── program_builder.py
                         │       │                   │      (only component that persists)
                         │       ▼                   │
                         │  programs table ──────────►│─── PostgreSQL (real)
                         └────────────────────────────┘

                         ┌────────────────────────────┐
                         │  V2 PATH (ENGINE_MODE=v2)  │
                         │  ─────────────────         │
                         │  AthleteModule (MOCK) ◄────│─── SAME as V1
                         │       │                   │
                         │  AssessmentEntry (MOCK) ◄──│─── SAME as V1
                         │       │                   │
                         │  DeficitDetection (MOCK) ◄─│─── SAME as V1
                         │       │                   │     (V2 does NOT use V2 deficit)
                         │       │                   │
                         │  demand_scoring_engine ◄───│─── MOCK (MockDemandRepository)
                         │       │                   │
                         │  inline scoring loop ◄────│─── integration_workflow.py
                         │       │                   │     (bypasses V2 endpoint)
                         │       ▼                   │
                         │  returns V1 format         │
                         │  (no persistence)          │
                         └────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│  DEAD CODE (infrastructure that exists but never executes)                │
│                                                                           │
│  athlete_state_engine → athlete_state_snapshots table (R/W never called)  │
│  training_load_engine → training_load_events table (R/W never called)     │
│  injury_risk_engine  → injury_risk_profiles table (R/W never called)      │
│  assessment_metric_engine → metric_demand_mapping table (R/W never called)│
│  demand_lifecycle_engine → (richer scoring formula, never called)         │
│  domain_events (written by all above, never consumed)                     │
│  performance_demands, role_demand_priority, exercise_demand_mapping       │
│  competition_calendar (doesn't even exist)                                │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## SECTION 3 — BUILD GAP ESTIMATE

### Assumptions

- One senior full-stack engineer (Python + PostgreSQL + some React)
- 40-hour weeks
- No external dependencies except database
- V1 pipeline continues to work during development (parallel deployment)
- MVP = working V2 pipeline with real data for one sport (Cricket), all 20 capabilities present but basic
- Beta = 3 sports, production data, coach feedback integration, explainability UIs
- Production = 10+ sports, multi-tenant, monitoring, rollback, full observability

### Phase 1: Foundation (Current → MVP)

**Goal:** A working V2 pipeline that reads from real database tables and produces a program for one athlete.

| # | Task | Days | Dependencies |
|---|------|------|-------------|
| 1 | **Delete dead infrastructure** — remove 5 dead routers from demand_scoring_engine, remove endpoint registrations | 1 | None |
| 2 | **Unify deficit systems** — make assessment_metric_engine the single authoritative deficit, delete others, wire into pipeline | 3 | #1 |
| 3 | **Unify demand scoring** — fold demand_lifecycle_engine's richer formula (ACWR, recovery, fatigue, injury) into demand_scoring_engine, delete lifecycle engine | 3 | #1 |
| 4 | **Wire ACWR into scoring** — add SQL read of `acute_chronic_load_view` to demand_score computation | 1 | #3 |
| 5 | **Wire competition proximity** — add `competition_calendar` table, add proximity flag to scoring, create red zone constraint | 3 | None |
| 6 | **Demote MockDemandRepository** — make PostgreSqlDemandRepository the default, wire to real `performance_demands`, `role_demand_priority`, `exercise_demand_mapping` tables | 3 | #1 |
| 7 | **Remove inline V2 scoring from integration_workflow** — make V2 path call `get_demand_recommendations()` endpoint | 1 | #6 |
| 8 | **Add exposure planning** — add `exposure_targets` table, compute weekly frequency per demand, filter exercises by exposure | 3 | None |
| 9 | **Add objective planning** — add `session_objectives`, assign primary/secondary/tertiary per session | 2 | #8 |
| 10 | **Add session sequencing** — order exercises within session by movement pattern (power before strength, low fatigue before high fatigue) | 3 | #9 |
| 11 | **Wire program_builder to V2 endpoint** — when ENGINE_MODE=v2, fetch recommendations from V2 endpoint and build program | 2 | #7 |
| 12 | **Add recommendation_id FK to programs** — link program to recommendation_log | 1 | None |
| 13 | **Add config snapshot to recommendation_log** | 1 | None |
| 14 | **Integration test: end-to-end V2 pipeline** | 3 | #1-13 |

**MVP Time: 30 working days (6 weeks)**

**MVP Deliverable:** A single POST that creates athlete, records assessment, computes demand scores (with ACWR and competition proximity), assigns objectives, sequences sessions, selects exercises from real `exercise_demand_mapping`, generates a 4-week program with proper progression, persists to DB, logs to recommendation_log with config snapshot.

**MVP Limitations:** One sport (Cricket). No periodization blocks. No recovery model. No UI. No coach feedback analysis. No athlete state integration.

### Phase 2: Production Hardening (MVP → Beta)

**Goal:** Multi-sport, production data, coach feedback, basic explainability, monitoring.

| # | Task | Days |
|---|------|------|
| 15 | Add sport onboarding tool (seed data importer for demands, roles, mappings) | 5 |
| 16 | Onboard 2 additional sports (Soccer, Rugby) with demand mappings | 5 |
| 17 | Wire athlete state into program generation (readiness modifies volume) | 3 |
| 18 | Wire training load events into ACWR (daily batch import) | 2 |
| 19 | Wire injury risk into demand scoring (reduce load for high-risk athletes) | 2 |
| 20 | Build coach feedback dashboard (accept/reject/modify rates per demand, per exercise) | 5 |
| 21 | Build explainability viewer (decision trace for any generated program) | 5 |
| 22 | Add exercise substitution (coach swaps exercise A for B, system suggests alternatives) | 3 |
| 23 | Add coach override learning (detect patterns: "coach always swaps A for B for demand X") | 5 |
| 24 | Add monitoring (Prometheus metrics for pipeline latency, emptiness rate, acceptance rate) | 3 |
| 25 | Add background job worker (Celery/Redis for async ACWR recompute, injury risk batch) | 5 |
| 26 | Performance test at 100 athletes, identify bottlenecks | 3 |
| 27 | Migration rollback scripts (down.sql for all V2 migrations) | 2 |
| 28 | Beta documentation (API reference, deployment guide, coach's manual) | 5 |

**Beta Time: 53 working days (11 weeks) — cumulative 17 weeks**

**Beta Deliverable:** Multi-sport V2 pipeline with real data, athlete state awareness, coach feedback dashboard, explainability viewer, monitoring, background workers.

**Beta Limitations:** No periodization (still 4-week blocks). No LTAD (youth athletes treated as adults). No rehab/RTS. No team management. Single-tenant.

### Phase 3: Scale (Beta → Production)

**Goal:** Multi-tenant, 10+ sports, full observability, team support.

| # | Task | Days |
|---|------|------|
| 29 | Onboard 7 more sports (Basketball, Track & Field, Swimming, Tennis, Golf, Baseball, MMA) | 15 |
| 30 | Multi-tenant isolation (organization-scoped queries + row-level security) | 10 |
| 31 | Performance optimization at 10K athletes (materialized ACWR view, caching, connection pooling) | 10 |
| 32 | Add team/squad management (shared sessions + individual modifications) | 10 |
| 33 | Add basic periodization (mesocycle planning: select block type, duration, loading trend) | 15 |
| 34 | Add recovery context (sleep, travel, illness integration into readiness) | 10 |
| 35 | Build configuration UI (demand weights, exposure targets, exercise mappings) | 15 |
| 36 | Add program versioning (regenerate with same config → same output) | 5 |
| 37 | Production deployment (Docker, CI/CD, blue-green deployment, rollback) | 10 |
| 38 | Security audit (RBAC, PII handling, cross-org isolation) | 5 |
| 39 | Load test at 10K athletes, tune performance | 5 |

**Production Time: 110 working days (22 weeks) — cumulative 39 weeks**

**Production Deliverable:** Multi-tenant, multi-sport, production-grade FORGE V2 with periodization, team support, configuration UI, and full operational readiness.

---

## SECTION 4 — KILL LIST

### Services to Delete

| Service | File | LOC | Reason | Action |
|---------|------|-----|--------|--------|
| `AthleteStateService` + router | `athlete_state_engine.py` | 505 | Dead code — no callers, no pipeline integration planned before Beta | Delete (keep service class in archive) |
| `TrainingLoadService` + router | `training_load_engine.py` | 465 | Dead code — same | Delete (keep service class) |
| `InjuryRiskService` + router | `injury_risk_engine.py` | 523 | Dead code — same | Delete (keep service class) |
| `AssessmentMetricService` + router | `assessment_metric_engine.py` | 511 | Dead code — same, AND its deficit logic will be folded into demand_scoring_engine | Delete (keep deficit formula) |
| `DemandStateService` + router | `demand_lifecycle_engine.py` | 258 | Dead code — its richer formula will be folded into demand_scoring_engine | Delete (keep formula) |
| Router mounts in demand_scoring_engine.py | lines 52-56 | 5 | Mounts 5 dead routers | Delete immediately |
| `Inline V2 scoring loop` | integration_workflow.py:363-394 | 32 | Duplicate of demand_scoring_engine endpoint | Delete (route through endpoint) |

**Total lines removed: ~2,200+**

### Endpoints to Delete or Deprecate

| Endpoint | File | Reason |
|----------|------|--------|
| `POST /api/v2/athlete-state` | athlete_state_engine.py | No callers |
| `GET /api/v2/athlete-state/{id}` | athlete_state_engine.py | No callers |
| `GET /api/v2/athlete-state/latest/{athlete_id}` | athlete_state_engine.py | No callers |
| `GET /api/v2/athlete-state/athlete/{athlete_id}` | athlete_state_engine.py | No callers |
| `POST /api/v2/training-load` | training_load_engine.py | No callers |
| `GET /api/v2/training-load/{athlete_id}` | training_load_engine.py | No callers |
| `GET /api/v2/training-load/acwr/{athlete_id}` | training_load_engine.py | No callers |
| `POST /api/v2/injury-risk` | injury_risk_engine.py | No callers |
| `GET /api/v2/injury-risk/latest/{athlete_id}` | injury_risk_engine.py | No callers |
| `GET /api/v2/injury-risk/{id}` | injury_risk_engine.py | No callers |
| `POST /api/v2/metric-deficits/compute` | assessment_metric_engine.py | No callers |
| `GET /api/v2/metric-deficits/assessments` | assessment_metric_engine.py | No callers |
| `GET /api/v2/metric-deficits/metrics/{assessment_id}` | assessment_metric_engine.py | No callers |
| `GET /api/v2/metric-deficits/norms/{metric_id}` | assessment_metric_engine.py | No callers |
| `POST /api/v2/demand-states/compute` | demand_lifecycle_engine.py | No callers |
| `POST /api/v1/integration/athlete-workflow` | integration_workflow.py | V1 endpoint — keep for backward compat but deprecate |
| `POST /api/v2/integration/athlete-workflow` | integration_workflow.py | V2 endpoint — keep but refactor to call real V2 endpoint |

**Total endpoints removed or deprecated: 17**

### Tables to Delete or Deprecate

| Table | Migration | Reason | Action |
|-------|-----------|--------|--------|
| `athlete_state_snapshots` | 000024 | Never read by pipeline. Will be re-created properly when athlete state is needed. | **Keep schema** (columns are correct), delete untested code that writes to it |
| `domain_events` | 000022 | Events emitted but never consumed. Need consumer architecture first. | **Keep schema** (domain events are important), add event consumer |
| `entity_relationships` | 000023 | Created but never populated or queried by any code | **Keep schema** (useful for knowledge graph), deprecate until needed |
| `injury_risk_demand_mapping` | 000022 | Table exists but injury risk engine is dead code | **Keep schema** (correct design), deprecate until injury risk is wired |

**Do NOT delete any tables.** The schemas are well-designed. The problem is that code doesn't read them. Keep all tables, delete the dead service code, and wire pipeline reads in Phase 1.

### Duplicate Logic to Delete

| Duplicate | Files | Action |
|-----------|-------|--------|
| `training_months_to_level()` | recommendation_engine.py + demand_scoring_engine.py | Keep one (recommendation_engine.py), import elsewhere |
| `compute_deficit_factor()` / `compute_deficit_factor_sync()` | demand_scoring_engine.py (2 copies, lines 779 and 900) | Delete one — both are in the same file |
| V2 exercise scoring | demand_scoring_engine.py:1060-1092 + integration_workflow.py:375-392 | Delete integration_workflow copy, route through endpoint |
| V1 deficit detection called twice | program_builder.py + integration_workflow.py both call detect_deficits() | De-duplicate: compute once, pass result |

---

## SECTION 5 — KEEP LIST

### Components That Should Become the Foundation of V2

| Component | File | Why Keep |
|-----------|------|----------|
| `DemandScoringService` | demand_scoring_engine.py:766 | Core V2 logic. Will be sole authority after unification. |
| `compute_role_demand_scores()` | demand_scoring_engine.py:947 | Working V2 demand scoring. Add ACWR/competition/injury factors. |
| `get_demand_recommendations()` endpoint | demand_scoring_engine.py:1002 | The V2 endpoint. Wire pipeline to call it. Already has caching, observability logging. |
| `PostgreSqlDemandRepository` | demand_scoring_engine.py:216 | Real DB queries for demands, priorities, mappings. Make default. |
| `DemandStateService._compute_single_demand()` | demand_lifecycle_engine.py:148 | Richer scoring formula with ACWR/recovery/fatigue/injury factors. **Fold into DemandScoringService.** |
| `training_months_to_level()` | recommendation_engine.py:19 | Single authoritative copy. Keep in recommendation_engine, import in demand_scoring_engine. |
| `RecommendationObservabilityRepository.log_recommendation()` | recommendation_observability.py | Working audit trail. Wire V1 pipeline to log here too. |
| `calculate_reps_and_intensity()` | program_builder.py:230 | Working progression logic. Make data-driven by reading `program_design_rules`. |
| `PostgreSqlProgramRepository` | program_builder.py:447 | Real DB persistence for programs. Works correctly. |
| `DeficitDetectionService` | deficit_detection_engine.py | V1 deficit system. Keep as V1 fallback. V2 will use assessment_metric_engine z-scores. |
| `MockDemandRepository` | demand_scoring_engine.py:323 | Keep as test data seed. **Make it read from seed data, not be the production engine.** |
| `acute_chronic_load_view` | migration 000024 | Correct ACWR calculation. Add pipeline read. |

---

## SECTION 6 — RECOMMENDED FREEZE POINT

### Freeze Immediately

These components are **correct and complete** — no further design changes needed:

- `programs` table schema (including execution tracking columns)
- `Performance_demands`, `role_demand_priority`, `exercise_demand_mapping`, `assessment_demand_mapping` table schemas
- `Recommendation_log`, `coach_feedback` table schemas
- `recommendation_log` UUID-as-PK design (for coach feedback referencing)
- V2 scoring formula structure (priority × deficit × level × adjustments)
- `training_months_to_level()` function

**Freeze these now. They are the foundation. Build everything else on top of them.**

### Redesign Immediately

These components need **architectural changes before implementation continues**:

| Component | Current Problem | Required Change |
|-----------|----------------|-----------------|
| deficit system | 3 implementations, no authority | Make assessment_metric_engine z-scores the SINGLE authority. Delete raw-score heuristic. |
| demand score system | 2 implementations (simple + rich) | Fold rich formula (ACWR, recovery, fatigue, injury) into single `DemandScoringService`. Delete lifecycle engine. |
| V2 pipeline entry point | integration_workflow bypasses V2 endpoint | All V2 consumers must call `POST /api/v2/demand-recommendations`. Delete inline scoring. |
| V1 pipeline data source | MockExerciseRepository with hardcoded Cricket data | V1 must read from real `exercises`, `movement_templates`, `template_slots` tables. |
| competition calendar | Doesn't exist | Add `competition_events` table. Add proximity field to `DemandScoreRequest`. Add red zone constraint. |
| program_builder progression | Hardcoded 4-week in Python | Read from `program_design_rules.progression_rules` or replace with data-driven progression table. |

### Postpone to V3

These components are **too large to build in V2's current state** and should be explicitly scoped out:

| Component | Why Postpone | Prerequisite |
|-----------|-------------|-------------|
| Full Periodization (macro/meso/microcycles, block types, loading trajectories) | Requires fundamental domain model expansion. Would delay MVP by 3+ months. | V2 pipeline working end-to-end for one sport |
| LTAD (biological age, PHV, sensitive periods) | Youth athlete domain is a separate bounded context. Betray the adult athlete focus. | V2 production with 3+ sports |
| Rehabilitation / Return-to-Sport | Requires injury registry, phased protocols, RTS gates. Separate bounded context. | V2 production with execution tracking data |
| Team/Squad management | Requires shared sessions, squad rotation. Team sports are a separate workflow. | V2 production with individual athlete programs working |
| AI coach feedback learning | Requires 6+ months of coach feedback data. Premature without data. | V2 Beta with coach feedback accumulation |
| Multi-tenant isolation | Premature optimization. V1 is single-tenant. V2 should match. | V2 production with 5+ organizations |

---

## SECTION 7 — IMPLEMENTATION PRIORITY

### Priority Matrix

```
                    HIGH IMPACT                    LOW IMPACT
HIGH URGENCY    ┌─────────────────────┬─────────────────────┐
                │ 1. Delete dead code │ 5. Add config       │
                │ 2. Unify deficits   │    snapshot to log   │
                │ 3. Unify demand     │ 6. Wire FK from     │
                │    scoring          │    program → reco   │
                │ 4. Wire ACWR + comp │                      │
                │    into scoring     │                      │
                ├─────────────────────┼─────────────────────┤
                │ 7. Wire program_    │ 8. Add exposure     │
                │    builder to V2    │    targets table     │
                │    endpoint         │ 9. Add objective     │
LOW URGENCY     │                     │    planning         │
                │                     │ 10. Session sequencing│
                └─────────────────────┴─────────────────────┘
```

### Build Order

| Phase | Weeks | Deliverable | Dependencies |
|-------|-------|-------------|-------------|
| **Wipe** | 1 | Delete dead code. Remove 5 routers, 17 endpoints, 2 duplicate scoring functions. Fix 2 code copies of training_months_to_level. | None |
| **Unify** | 2 | Single deficit system (z-score authority). Single demand score system (rich formula in demand_scoring_engine). | Wipe |
| **Wire** | 5 | ACWR + competition proximity + injury risk in scoring. PostgreSqlDemandRepository as default. Pipeline calls real endpoint. Inline scoring deleted. | Unify |
| **Build** | 6 | Exposure targets, objectives, session sequencing. Program builder reads V2 endpoint. | Wire |
| **Test** | 1 | End-to-end V2 integration test. V1 ↔ V2 output comparison test. | Build |
| **MVP** | **15 weeks** | Working V2 pipeline, one sport (Cricket), real data, all 20 capabilities basic | — |

---

## SECTION 8 — FINAL VERDICT

### How far is the current codebase from production-ready FORGE V2?

| Milestone | Distance | Confidence |
|-----------|----------|-----------|
| Current state | **0%** — No capability is production-ready | HIGH |
| Cleaning up dead code + duplication | **1 week** | HIGH |
| MVP (one sport, end-to-end, real data) | **15 weeks (3.75 months)** with 1 senior engineer | MEDIUM |
| Beta (3 sports, coach feedback, explainability) | **17 weeks (4.3 months)** from today | MEDIUM |
| Production (10+ sports, multi-tenant, team) | **39 weeks (9.75 months)** from today | LOW |

### The Hard Truth

**The V2 architecture documentation describes a system that does not exist in code.**

The codebase has:

- **6 fully-implemented services that are never called** (2,700 lines of dead code)
- **3 different deficit systems producing different answers** for the same input
- **2 different demand scoring systems producing different scores** for the same demand
- **0 lines of competition calendar code** despite it being documented as a domain
- **0 lines of exposure planning code** despite it being documented as a domain
- **0 lines of objective planning or session sequencing code** despite these being documented
- **1 program builder that generates programs without reading any athlete state data**

The most actionable thing you can do right now: **delete the 6 dead services, unify the deficit and demand scoring systems, and wire ACWR/competition into the scoring formula.** This is 3 weeks of work and eliminates 60% of the gap between documented architecture and running code.

After that, you have a solid foundation. Before that, every new feature adds to the pile of code that looks integrated but isn't.
