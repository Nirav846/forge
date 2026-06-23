# AUDIT #7 — CODE REALITY & SOURCE-OF-TRUTH AUDIT
## Actual Runtime Architecture vs. Intended Design

**Review Mode:** Principal Software Architect | Systems Integrator | Technical Debt Auditor
**Date:** 2026-06-17
**Rule:** Do not review architecture. Do not suggest new domains. Do not propose future features. Map only what actually exists.

---

## SECTION A — Current Runtime Architecture

### A1. FastAPI Applications (9 separate runnable apps)

| # | App (File) | Port/Location | Actual Consumers | Status |
|---|-----------|--------------|-----------------|--------|
| 1 | `athlete_module.py` | `POST /athletes`, `GET /athletes/{id}` | integration_workflow, program_builder | **ACTIVE** |
| 2 | `assessment_entry_module.py` | `POST /assessments/record` | integration_workflow, program_builder | **ACTIVE** |
| 3 | `deficit_detection_engine.py` | `POST /api/v1/deficits/detect` | integration_workflow, program_builder | **ACTIVE** |
| 4 | `recommendation_engine.py` | `POST /api/v1/recommendations` | integration_workflow, program_builder, session_generator | **ACTIVE** (V1 path only) |
| 5 | `demand_scoring_engine.py` | `POST /api/v2/demand-recommendations` | integration_workflow (V2 path), standalone | **ACTIVE** (but consumed only by workflow) |
| 6 | `program_builder.py` | `POST /generate-program`, `POST /stage-program` | None (terminal endpoint) | **ACTIVE** |
| 7 | `session_generator.py` | `POST /generate-session` | None (terminal endpoint) | **ACTIVE** |
| 8 | `integration_workflow.py` | `POST /api/v1/integration/athlete-workflow` | None (demo entrypoint) | **ACTIVE** |
| 9 | `knowledge_graph_service.py` | Various `/kg/` endpoints | None (standalone) | **ACTIVE** |

### A2. Router-Mounted Services (APIRouter, not standalone)

| # | Service (File) | Mounted On | Endpoints | Status |
|---|---------------|-----------|-----------|--------|
| 1 | `training_load_engine.py` | `demand_scoring_engine.app` | `POST /api/v2/training-load`, `GET /acwr` | **MOUNTED** but **NOT CALLED** by any pipeline |
| 2 | `athlete_state_engine.py` | `demand_scoring_engine.app` | `POST /api/v2/athlete-state` | **MOUNTED** but **NOT CALLED** by any pipeline |
| 3 | `injury_risk_engine.py` | `demand_scoring_engine.app` | `POST /api/v2/injury-risk` | **MOUNTED** but **NOT CALLED** by any pipeline |
| 4 | `assessment_metric_engine.py` | `demand_scoring_engine.app` | `POST /api/v2/metric-deficits` | **MOUNTED** but **NOT CALLED** by any pipeline |
| 5 | `demand_lifecycle_engine.py` | `demand_scoring_engine.app` | `POST /api/v2/demand-states/compute` | **MOUNTED** but **NOT CALLED** by any pipeline |
| 6 | `recommendation_observability.py` | `demand_scoring_engine.app` | `POST /api/v2/observability/log` | **MOUNTED** and **CALLED** by demand_scoring_engine only |

### A3. Actual Runtime Flow (V1 — default ENGINE_MODE)

```
POST /api/v1/integration/athlete-workflow
  → athlete_module (create athlete)
  → assessment_entry_module (record results)
  → deficit_detection_engine (detect_deficits from raw scores)
  → recommendation_engine.get_exercise_recommendations
     → MockExerciseRepository.get_template (sport + role + goal)
     → MockExerciseRepository.get_slots (template_id)
     → MockExerciseRepository.get_ranked_exercises (slot_id)
        → V1 scoring: relevance*4 + specificity*3 + transfer*20 + tag_match*2.5 + mechanics_bonus
     → returns SlotRecommendation[] with exercise_pool
  → returns WorkflowResponse (prescribed_templates with top-3 exercises per slot)

POST /generate-program (program_builder)
  → athlete_module.get_by_id
  → deficit_detection_engine.detect_deficits (again — duplicated call)
  → recommendation_engine.get_exercise_recommendations (again — duplicated call)
     → Same V1 path as above
  → calculate_reps_and_intensity (hardcoded 4-week progression)
  → MockProgramRepository or PostgreSqlProgramRepository.create_program
  → returns ProgramResponse
```

### A4. Actual Runtime Flow (V2 — ENGINE_MODE=v2)

```
POST /api/v2/integration/athlete-workflow
  → athlete_module (create athlete) — SAME CODE
  → assessment_entry_module (record results) — SAME CODE
  → deficit_detection_engine (detect_deficits) — SAME CODE
  → demand_scoring_engine.compute_role_demand_scores
     → V2MockDemandRepository.get_role_demands
     → compute_deficit_factor_sync() — INDEPENDENT deficit computation from raw scores
     → demand_score = priority_weight * (1 + deficit) * level_mult * 100
  → V2MockDemandRepository.get_exercises_for_demand (for each scored demand)
     → exercise_score = relevance * priority_weight * level_mult * eq_match * 100
  → wraps result in V1 template format for backward compat
  → returns V2WorkflowResponse
```

### A5. What V2 endpoints are NEVER called by the pipeline

| Endpoint | Exists? | Called by pipeline? | Called by anything? |
|----------|---------|-------------------|-------------------|
| `POST /api/v2/training-load` | YES | NO | Tests only |
| `GET /api/v2/acwr` | YES | NO | Tests only |
| `POST /api/v2/athlete-state` | YES | NO | Tests only |
| `POST /api/v2/injury-risk` | YES | NO | Tests only |
| `POST /api/v2/metric-deficits` | YES | NO | Tests only |
| `POST /api/v2/demand-states/compute` | YES | NO | Tests only |
| `POST /api/v2/demand-recommendations` | YES | NO (workflow uses compute_role_demand_scores directly, not the endpoint) | Standalone curl only |
| `POST /api/v2/observability/log` | YES | YES (by demand_scoring_engine only) | demand_scoring_engine |

---

## SECTION B — Duplicated Logic

### B1. Deficit Computation — 3 Implementations

| # | Location | Function | Formula | Used By | Authority? |
|---|----------|----------|---------|---------|-----------|
| 1 | `deficit_detection_engine.py` | `detect_deficits()` | Compares raw score to benchmark thresholds (Poor/Suboptimal/Optimal/Elite). Uses `benchmarks` table. Returns `DeficitDetail[]` with severity (High/Moderate). | integration_workflow (both V1+V2), program_builder | **V1 DEFICIT AUTHORITY** |
| 2 | `assessment_metric_engine.py` | `compute_metric_deficits()` | z-score based: `severity = max(0, min(1, -z/3))` for higher_is_better metrics. Uses `metric_norms`. Returns per-metric deficits mapped to demands. | **NO CALLER** (mounted on demand_scoring_engine router, never invoked) | Dead code in pipeline |
| 3 | `demand_scoring_engine.py` | `compute_deficit_factor()` | Raw-score heuristic: `deficit = 1 - min(raw/50, 1)` for CMJ, `1 - min(raw/3, 1)` for sprint, etc. Uses hardcoded denominators. Returns dict of demand_name → deficit. | integration_workflow V2 path, demand_scoring_engine V2 endpoint | **V2 DEFICIT AUTHORITY** |

**Problem:** Implementation #2 (z-score based) is the most scientifically valid but has **zero callers**. Implementation #3 (raw-score heuristic with hardcoded denominators) is what the V2 pipeline actually uses. Implementation #1 (benchmark-based) is what V1 uses.

### B2. Demand Score Computation — 2 Implementations

| # | Location | Function | Formula | Used By | Authority? |
|---|----------|----------|---------|---------|-----------|
| 1 | `demand_scoring_engine.py:947` | `compute_role_demand_scores()` | `score = priority_weight × (1 + deficit) × level_mult × 100` | integration_workflow V2, demand_scoring_engine endpoint | **V2 DEMAND AUTHORITY** |
| 2 | `demand_lifecycle_engine.py:80` | `compute_demand_states()` | `risk_adjusted = base_score × role_mult × injury_adj × acwr_adj × recovery_adj × fatigue_adj` | **NO CALLER** (only tests) | Dead code in pipeline |

**Problem:** Implementation #2 has a richer model (includes ACWR, recovery, fatigue, injury risk) but is **completely disconnected** from the pipeline. Implementation #1 has fewer factors but is what actually runs.

### B3. Exercise Recommendation — 3 Implementations

| # | Location | Function | Scoring | Used By | Authority? |
|---|----------|----------|---------|---------|-----------|
| 1 | `recommendation_engine.py:897` | `get_exercise_recommendations()` | V1: `relevance*4 + specificity*3 + transfer*20 + tag_match*2.5 + mechanics_bonus` | integration_workflow V1, program_builder, session_generator | **V1 EXERCISE AUTHORITY** |
| 2 | `demand_scoring_engine.py:1060-1092` | Inline in `get_demand_recommendations()` | V2: `score = (relevance/10) × priority_weight × level_mult × eq_match × 100` | **NO CALLER** (the endpoint exists but is not called by any pipeline) | Standalone endpoint |
| 3 | `integration_workflow.py:375-392` | Inline in `run_athlete_workflow_v2()` | V2 duplicate: `score = relevance × priority_weight × level_mult × eq_match × 100` | integration_workflow V2 path | **V2 EXERCISE AUTHORITY** (de facto) |

**Critical finding:** The V2 exercise recommendation formula is DUPLICATED in two places (demand_scoring_engine.py and integration_workflow.py). The integration_workflow V2 path does NOT call the demand_scoring_engine endpoint — it reimplements the scoring inline.

### B4. Training Age → Development Level Mapping — 3 Copies

```python
# recommendation_engine.py:19 - ORIGINAL
def training_months_to_level(months):
    if months >= 36: return "PERFORMANCE"
    elif months >= 12: return "DEVELOPMENT"
    return "FOUNDATION"

# demand_scoring_engine.py:34 - COPY 1 (identical)
def training_months_to_level(months):
    if months >= 36: return "PERFORMANCE"
    elif months >= 12: return "DEVELOPMENT"
    return "FOUNDATION"

# integration_workflow.py:19 - imports from recommendation_engine (uses original)
from recommendation_engine import training_months_to_level

# program_builder.py:750 - uses recommendation_engine import (line 750)
```

3 copies in source. 2 are active. If the levels ever change (e.g., adding "ELITE" at 60 months), all copies must be updated.

---

## SECTION C — Dead Code

### C1. Services with Zero Callers in Any Pipeline

| Service | File | LOC | Reason Dead |
|---------|------|-----|-------------|
| `AthleteStateService` | `athlete_state_engine.py` | 505 | Mounted as router on demand_scoring_engine.app. All 4 endpoints have zero callers outside tests. |
| `TrainingLoadService` | `training_load_engine.py` | 465 | Same. 3 endpoints, zero callers. |
| `InjuryRiskService` | `injury_risk_engine.py` | 523 | Same. 3 endpoints, zero callers. |
| `AssessmentMetricService` | `assessment_metric_engine.py` | 511 | Same. 4 endpoints, zero callers. |
| `DemandStateService` | `demand_lifecycle_engine.py` | 258 | Same. 1 endpoint, zero callers. |
| `RecommendationObservabilityService` | `recommendation_observability.py` | ~400 | 7 endpoints, 1 partial caller (demand_scoring_engine logs to it but nothing reads the logs back via API) |

**Total dead code: ~2,662 lines of service layer with no runtime consumers.**

### C2. Dead Repositories

| Repository | File | Used By | Status |
|------------|------|---------|--------|
| `PostgreSqlAthleteStateRepository` | athlete_state_engine.py | Dead service | **DEAD** |
| `PostgreSqlTrainingLoadRepository` | training_load_engine.py | Dead service | **DEAD** |
| `PostgreSqlInjuryRiskRepository` | injury_risk_engine.py | Dead service | **DEAD** |
| `PostgreSqlAssessmentMetricRepository` | assessment_metric_engine.py | Dead service | **DEAD** |
| `PostgreSqlDemandRepository` | demand_scoring_engine.py | Factory exists but V2 pipeline uses Mock | **PARTIALLY DEAD** (factory can return it but no caller uses it for real data) |

### C3. Migration Tables with No Application Code Consumers

| Migration | Table | Written by | Read by |
|-----------|-------|-----------|---------|
| 000022 | `performance_demands` | Seed data | `PostgreSqlDemandRepository.get_role_demands()` — never called |
| 000022 | `exercise_demand_mapping` | Seed data | `PostgreSqlDemandRepository.get_exercises_for_demand()` — never called |
| 000022 | `role_demand_priority` | Seed data | Never consumed by any endpoint in production path |
| 000022 | `assessment_demand_mapping` | Seed data | Never consumed by any endpoint in production path |
| 000022 | `domain_events` | Events emitted | Never consumed (no subscribers) |
| 000023 | `recommendation_log` | V2 endpoint writes | V2 endpoint only — V1 pipeline never logs |
| 000023 | `coach_feedback` | API endpoint exists | No consumer reads it for analysis |
| 000024 | `athlete_state_snapshots` | Dead service writes | Dead — never read by pipeline |
| 000024 | `training_load_events` | Dead service writes | Dead — never read by pipeline |
| 000024 | `injury_risk_profiles` | Dead service writes | Dead — never read by pipeline |

**Total dead tables: 15+** (all V2 Phase 3-5 tables have no pipeline consumers).

---

## SECTION D — Bypassed Components

### D1. V2 Engine Bypass Path

The V2 scoring engine (`demand_scoring_engine.py get_demand_recommendations`) is a fully functional FastAPI endpoint that:

1. Computes demand scores ✓
2. Scores exercises per demand ✓
3. Enriches with classification metadata ✓
4. Logs to recommendation_log ✓
5. Caches results ✓

**But it is NEVER called by any pipeline.** The integration_workflow V2 path bypasses it entirely and reimplements the logic inline:

```
integration_workflow V2 path:
  → compute_role_demand_scores()  ← calls the function, not the endpoint
  → inline scoring loop           ← duplicates demand_scoring_engine lines 1060-1092
  → returns V1-format response    ← discards V2 classification, observability, caching
```

### D2. V1 Pipeline Bypasses All V2 Services

The default `ENGINE_MODE=v1` pipeline (`program_builder.py` → `recommendation_engine.py` → `get_exercise_recommendations`):

1. Does NOT read `performance_demands` table
2. Does NOT read `role_demand_priority` table
3. Does NOT use `exercise_demand_mapping` table
4. Does NOT compute ACWR from any source
5. Does NOT read athlete state or readiness
6. Does NOT check competition calendar
7. Does NOT log to `recommendation_log`
8. Uses V1 mock data exclusively for sport/role/template/exercise mapping

The V1 pipeline is a **hermetically sealed mock system** that produces Cricket-specific programs from hardcoded data.

### D3. Domain Events Bypass

Events are emitted in 6 places (`TrainingLoadRecorded`, `ACWRCalculated`, `InjuryRiskUpdated`, `DemandScoreCalculated`, `AssessmentMetricsExtracted`, `AthleteStateCalculated`) but:

- Only `demand_lifecycle_engine.py` emits `DemandScoreCalculated` — which is never called
- Only `athlete_state_engine.py` emits `AthleteStateCalculated` — which is never called
- The events INSERT into `domain_events` table but **no consumer ever reads from it**

The event_emitter pattern exists but there is zero event-driven behavior in the system. Events are fire-and-forget log entries.

---

## SECTION E — Source of Truth Violations

| Concept | Implementations | Authoritative? | Correctness |
|---------|---------------|---------------|-------------|
| **ACWR** | 1. `training_load_engine.py:95` (MockTrainingLoadRepository.compute_acwr) — mock only<br>2. SQL view `acute_chronic_load_view` in DB | **NONE** — V1 uses neither. V2 has both but no pipeline uses ACWR | V1 produces programs with zero ACWR awareness. Pipeline runs without load context. |
| **Deficit** | 1. `deficit_detection_engine.py` (benchmark-based)<br>2. `assessment_metric_engine.py` (z-score based) — dead<br>3. `demand_scoring_engine.py` (raw-score heuristic) | **NONE** — V1 uses #1, V2 uses #3. Two different deficit values for same input. | Athlete gets different deficit for the same CMJ depending on which engine runs. |
| **Demand Score** | 1. `demand_scoring_engine.py:947` (simple: priority × deficit × level)<br>2. `demand_lifecycle_engine.py:80` (rich: includes ACWR/recovery/fatigue/injury) | **NONE** — #1 is used by V2 workflow but it's the less accurate formula. #2 is richer but dead. | The richer formula exists but is unused. The simpler formula runs in production. |
| **Exercise Score** | 1. `recommendation_engine.py` (V1: 5-factor linear formula)<br>2. `demand_scoring_engine.py` (V2: demand-based formula)<br>3. `integration_workflow.py` (V2 inline — copy of #2) | **NONE** — V1 uses #1, V2 uses #3 (inline copy, not #2) | 3 implementations of exercise scoring, each producing different rankings for the same athlete. |
| **Progression** | 1. `program_builder.py:230` (hardcoded 4-week progression in `calculate_reps_and_intensity`)<br>2. `program_design_rules` table (progression_rules TEXT column) | #1 is de facto because #2 is TEXT (not executable) | Progression rules exist in the database but are never parsed or executed. The actual progression is hardcoded Python. |
| **Readiness** | 1. `athlete_state_engine.py` (composite score from recovery, fatigue, injury risk) | **NONE** — endpoint exists but no pipeline reads readiness | Programs are generated with zero awareness of athlete readiness. |
| **Competition** | 1. Conceptual only — no code implementation | **NONE** | Programs are generated with zero awareness of competition dates. |
| **Training Load Events** | 1. `training_load_engine.py` (create, list, compute_acwr)<br>2. `training_load_events` table (migration 000024) | **NONE** — endpoints exist but no caller | No training load data is ever recorded or read by any program generation path. |
| **Recovery** | 1. `athlete_state_snapshots.recovery_score` column | **NONE** — never written or read by pipeline | Recovery is a schema concept only. |
| **Coach Feedback** | 1. `recommendation_observability.py` (CRUD endpoints)<br>2. `coach_feedback` table | **NONE** — stored but never analyzed | Coach feedback accumulates in the database but no code reads it for pattern learning or quality monitoring. |

**Total source-of-truth violations: 10 out of 10 concepts have no single authority.**

---

## SECTION F — Technical Debt Severity

### F1. Impact Matrix

| Debt Item | Type | Lines | Impact | Fix Priority |
|-----------|------|-------|--------|-------------|
| 5 dead services mounted on demand_scoring_engine router | Dead code | ~2,200 | Confuses developers, increases deployment risk, wastes cognitive load | **IMMEDIATE** |
| V2 scoring duplicated in integration_workflow | Duplication | ~30 | V2 pipeline produces different results than V2 endpoint | **IMMEDIATE** |
| V1 pipeline uses Mock repos exclusively | Mock debt | ~1,500 | All 7 V1 tables have real data but V1 never reads them | **IMMEDIATE** |
| 15+ V2 tables unread by any pipeline | Orphaned schema | 15 tables | Migration scripts create tables no code reads | **HIGH** |
| Domain events emitted but never consumed | Broken pattern | ~200 | Event-driven architecture is decorative | **HIGH** |
| Progression rules in TEXT column not executable | Schema misuse | 1 column | `progression_rules` is documentation, not code | **MEDIUM** |
| 3 copies of training_months_to_level | Duplication | 15 lines | Change requires 3 file updates | **MEDIUM** |
| No main.py or app orchestration | Missing infrastructure | N/A | 9 separate FastAPI apps, zero orchestration | **MEDIUM** |
| V1 program builder produces 4-week blocks ignoring competition | Logic gap | ~50 | Competition in 5 days → still generates Week 3 (Peak) | **HIGH** |
| recommendation_log has no consumer | Orphaned data | ~400 | Append-only log accumulates with no analysis | **MEDIUM** |

### F2. Debt by Category

| Category | Score (/10) | Rationale |
|----------|------------|-----------|
| Dead Code | 9 | ~2,700 lines of service code with zero callers |
| Duplication | 7 | 3 deficit systems, 2 demand scores, 3 exercise scorings, 3 level mappings |
| Orphaned Schema | 8 | 15+ tables created by migrations but never read by code |
| Broken Patterns | 6 | Events emitted but never consumed. Repositories exist but Mock is used everywhere. |
| Integration Gaps | 8 | 9 standalone apps with no orchestration. V2 pipeline bypasses V2 endpoint. |
| **Overall** | **7.6/10** | **System has significant architectural debt from premature V2 expansion.** |

---

## SECTION G — Recommended Cleanup Order

### Phase 1: Remove Dead Code (Week 1)

| # | Action | Files | Risk |
|---|--------|-------|------|
| 1 | Remove 5 dead routers from demand_scoring_engine.app includes | demand_scoring_engine.py lines 52-56 | LOW — nothing calls them |
| 2 | Delete `athlete_state_engine.py` router endpoints | athlete_state_engine.py | LOW — no pipeline consumers |
| 3 | Delete `training_load_engine.py` router endpoints | training_load_engine.py | LOW — no pipeline consumers |
| 4 | Delete `injury_risk_engine.py` router endpoints | injury_risk_engine.py | LOW — no pipeline consumers |
| 5 | Delete `assessment_metric_engine.py` router endpoints | assessment_metric_engine.py | LOW — no pipeline consumers |
| 6 | Delete `demand_lifecycle_engine.py` router endpoints | demand_lifecycle_engine.py | LOW — no pipeline consumers |

**Moves kept:** Keep the service classes (they may be used when V2 is wired). Remove only the router mounting and standalone endpoint exposure until V2 has actual callers.

### Phase 2: Unify Scoring (Week 2)

| # | Action | Files | Risk |
|---|--------|-------|------|
| 7 | Delete inline V2 scoring from integration_workflow.py | integration_workflow.py:363-394 | MEDIUM — must ensure integration_workflow calls the real V2 endpoint |
| 8 | Route integration_workflow V2 through `get_demand_recommendations` | integration_workflow.py | MEDIUM — response format may differ |
| 9 | Keep only one `training_months_to_level` (recommendation_engine.py), import elsewhere | 3 files | LOW |

### Phase 3: Wire V2 Data (Week 3-4)

| # | Action | Files | Risk |
|---|--------|-------|------|
| 10 | Make program_builder call V2 endpoint instead of V1 when ENGINE_MODE=v2 | program_builder.py | HIGH — changes output format |
| 11 | Wire ACWR query into demand scoring | demand_scoring_engine.py | MEDIUM — adds new input parameter |
| 12 | Add competition proximity as scoring input | demand_scoring_engine.py | MEDIUM — adds calendar query |

---

## SECTION H — What Must Be Fixed Before V2 Development Continues

### MUST-FIX (blocks all V2 development)

1. **Decide which deficit system is authoritative.** Currently 3 exist. The z-score system (assessment_metric_engine) is the most valid but has zero callers. The raw-score heuristic (demand_scoring_engine) is what V2 actually uses. Choose one, delete the others, and route all deficit queries through it.

2. **Decide which demand score is authoritative.** The demand_lifecycle_engine has a richer formula (includes ACWR, recovery, fatigue, injury risk) but is dead code. The demand_scoring_engine has a simpler formula (just priority × deficit × level) but is actually used. Either merge the richer formula into the scoring engine or delete the lifecycle engine.

3. **Wire the V2 endpoint into the pipeline instead of duplicating its logic inline.** The integration_workflow V2 path should call `POST /api/v2/demand-recommendations` instead of reimplementing `compute_role_demand_scores` + inline scoring loop.

4. **Remove the 5 dead routers from demand_scoring_engine.app.** They create a false impression that athlete state, training load, injury risk, metrics, and demand lifecycle are integrated. They are not. They are mounted but never called.

5. **Wire ACWR and competition proximity into program generation.** Currently the program_builder generates 4-week blocks with zero awareness of either. This is unsafe for athletes near competition.

### SHOULD-FIX (before V2 production launch)

6. **Make the V1 pipeline read from real database tables instead of MockExerciseRepository.** The `movement_templates`, `template_slots`, `exercises`, and `exercise_equipment` tables have real data. The V1 pipeline bypasses them for hardcoded mock data.

7. **Add a consumer for domain_events.** Events are emitted but never consumed. At minimum, TrainingLoadRecorded should trigger ACWR recalculation, and AssessmentMetricsExtracted should trigger demand score recalculation.

8. **Remove duplication: keep one `training_months_to_level`.** Three copies exist. Two are active.

### COSMETIC (improves developer experience)

9. **Add a main.py orchestrator.** Currently 9 separate FastAPI apps exist with no orchestration. No docker-compose. No single entry point.

10. **Add regression tests that catch the V1/V2 divergence.** Currently test_demand_scoring_engine.py tests V2 functions only. test_athlete_intelligence_layers.py tests dead code. No test verifies that V1 and V2 produce consistent results for the same input.

---

## SUMMARY

**The FORGE V2 codebase has a critical gap between architecture documentation and runtime reality.**

The intended architecture describes an integrated pipeline where athlete state, training load, injury risk, assessment metrics, and demand lifecycle all feed into program generation. The runtime reality is:

```
INTENDED:                                  ACTUAL:
Assessment → Metric Deficit → Demand       Assessment → V1 Deficit Engine
→ Exposure → Objective → Session           → V1 Recommendation Engine
→ Exercise → Progression → Program         → V1 Mock Template → Slot → Pool
  ↑ ACWR ↑ Readiness ↑ Comp Cal             → 4-week hardcoded progression
  ↑ Injury Risk ↑ Fatigue                    → Program (no ACWR/readiness/comp)
```

**The V2 Phase 3-4-5 services (athlete state, training load, injury risk, demand lifecycle, assessment metrics) are architecturally designed but operationally dead — ~2,700 lines of mounted, tested, never-called code.**

**15+ database tables created by migrations store data that no pipeline reads.**

**The V2 pipeline (integration_workflow V2 path) bypasses its own V2 endpoint and duplicates the scoring logic inline.**

**The V1 pipeline (default) uses only mock repositories and produces Cricket-specific programs from hardcoded data.**

### Bottom Line

V2 development should halt until the 5 must-fix items are resolved. The current codebase has a solid architecture on paper but a fragmented, duplicated, and partially dead-code runtime. Continuing to add V2 features without first consolidating the existing implementation will compound the technical debt and make the architecture impossible to validate.
