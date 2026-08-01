# Architecture Red Team Review: V2 Demand Recommendation Engine

**Review Date:** 2026-06-17
**Reviewer:** Independent Architecture Red Team
**Scope:** Entire V2 pipeline — domain events, training load, injury risk, demand scoring, exercise recommendation, recommendation log/observability
**Version Reviewed:** Schema migrations 000001–000024, src/*.py (demand_scoring_engine.py, training_load_*, injury_risk_*, exercise_recommendation_*, recommendation_observability_*, domain_events.py)

---

## Table of Contents

1. Failure Mode Analysis
2. DDD Bounded Context Audit
3. Data Model Stress Test
4. Configuration Explosion Map
5. Event-Driven Architecture Gap Analysis
6. AI/ML Readiness Assessment
7. Production Operations Review
8. Security & Privacy Review
9. Migration & Coexistence Strategy
10. Testing Strategy Assessment
11. Performance & Scalability Review
12. Final Verdict & Recommendations

---

## 1. Failure Mode Analysis

### 1.1 Oscillation (demand_score instability)

**Mechanism:** A coach accepts a top-N recommendation and logs it as training. The next cycle, the athlete's ACWR spikes, the injury risk penalty kicks in, and all demand scores reshuffle. The coach sees a completely different top-3 next week and concludes "the system is random."

**Severity:** HIGH
**Status:** UNMITIGATED

**Root cause:** No temporal damping on demand_scores. Every recompute is a full rebase from scratch with no memory of previous recommendations. The demand_score formula (`priority_weight × (1.0 + deficit_severity) × level_multiplier × equipment_match`) has no inertia term.

**Fix required:**
- Add a `demand_momentum` factor: `damped_score = α × new_score + (1-α) × previous_score` with α configurable per sport phase
- Persist previous demand_scores in a `demand_score_history` table so damping can be computed

### 1.2 Inflation (demand_score creep)

**Mechanism:** Over successive cycles, deficit_severity (0.0–1.0) accumulates for ever-finer assessment improvements. An athlete who improves from "very weak" to "adequate" still carries a non-zero deficit on other demands. Combined with `level_multiplier` for PERFORMANCE athletes (1.0), scores drift upward over time. Coaches habituate to higher scores and stop trusting absolute values.

**Severity:** MEDIUM
**Status:** PARTIALLY MITIGATED (deficit_severity is bounded 0–1, but accumulation across demands is unbounded)

**Root cause:** No normalization mechanism. The `demand_score` has no ceiling and no reference distribution. After 20 assessment updates, the score range could drift from [0.0–100.0] to [50.0–200.0].

**Fix required:**
- Normalize scored demands to a 0–100 range per recommendation cycle
- Compute percentile ranks against historical demand_score distributions
- Add a regression test that injects 50 assessment updates and asserts score distribution remains stable

### 1.3 Starvation (exercises never recommended)

**Mechanism:** Sports with >15 demands and >200 exercises mapped to them will always have a long tail of exercises where priority_weight × equipment_match < 0.1. These exercises never break into the top-K, effectively creating "dead exercises" that are configurable but unreachable.

**Severity:** MEDIUM
**Status:** UNMITIGATED

**Root cause:** The ranking is purely linear-weighted: it cannot enforce diversity or minimum coverage guarantees. There is no constraint that says "every demand category must have at least one recommended exercise per N cycles."

**Fix required:**
- Implement a coverage constraint after ranking: reserve 1-2 slots per recommendation cycle for "never-seen" or "lowest-served" demand categories
- Log starvation statistics per exercise in the recommendation_log
- Consider a multi-objective ranking that includes "novelty" or "coverage" as a secondary objective

### 1.4 Deadlock (circular dependency between components)

**Mechanism:** Three potential deadlock scenarios:

1. **Training Load → Injury Risk → ACWR penalty → Demand Score → Training Load:** If injury_risk penalty reduces demand scores → exercises recommended have lower load → ACWR stays low → injury risk stays low → no correction. This is a negative feedback loop that converges (good). Not a true deadlock.

2. **Coach Feedback Loop:** Coach modifies recommendation → override stored in coach_feedback → recommendation_log replays → coach sees modified version → modifies again. If the modification logic is not idempotent, each cycle shifts the recommendation further.

3. **Assessment → Deficit → Exercise → Assessment (circular):** An exercise improves an assessment metric → deficit decreases → demand_score drops → exercise is no longer recommended → athlete regresses → deficit increases → exercise is recommended again. This is oscillation, not deadlock.

**Severity:** LOW for true deadlock, MEDIUM for oscillation
**Status:** UNDERSTOOD

**Fix required:** Document these feedback loop dynamics. For the coach feedback loop scenario, add idempotency guards.

---

## 2. DDD Bounded Context Audit

### 2.1 Current Bounded Contexts

| Context | Files | Aggregate Root | Status |
|---------|-------|----------------|--------|
| Training Load | training_load_events, domain_events emit_acwr | `training_load_events.load_event_id` | CLEAN but leaky |
| Injury Risk | injury_risk_profiles, domain_events emit_injury_risk | `injury_risk_profiles.id` | CLEAN |
| Demand Scoring | demand_scoring_engine.py, demand_assessment_mapping | `demands.id` | OVERLOADED |
| Exercise Library | exercises table (inferred) | `exercises.id` | INCOMPLETE |
| Recommendation | exercise_recommendation_service.py | `recommendation_log.recommendation_id` | BLOATED |
| Observability | recommendation_log, coach_feedback | `recommendation_log.id` | CLEAN |

### 2.2 Bleeding Across Contexts

**Demand Scoring borrows from Injury Risk:** The `DemandScoringService.compute_demand_scores()` references `development_level` (an athlete property) and `equipment` (a facility property). These should be injected as value objects, not computed internally. The service currently has no explicit dependency injection boundary.

**Recommendation context reads from 4 other contexts:** It reads athlete profile, demands, exercises, and injury risk simultaneously. This makes it a "god orchestrator." No anti-corruption layer exists.

**Missing contexts:**
- **Athlete Profile Context:** No aggregate for athlete metadata (position, age, training age, injury history, competition calendar). Currently scattered across multiple contexts as implicit data.
- **Scheduling Context:** No aggregate for session date, time, coach assignment, facility booking. Recommendations are made without awareness of availability.
- **Competition Calendar Context:** No aggregate for upcoming competitions, season phases, tapering periods. This is critical for periodization.

### 2.3 Missing Value Objects

- `LoadScore` — encapsulated training load with units, validation (positive), calculation method versioning
- `DemandScore` — encapsulated with damping, percentile rank, calculation_id for traceability
- `RecommendationSet` — the full set of recommendations for an athlete-cycle, not just individual exercises
- `CoachOverride` — difference between recommendation and actual assignment, with diff semantics

### 2.4 Anti-Corruption Layer Needed

Between Demand Recommendation and Training Load, there should be an ACL that:
- Transforms load events into load scores
- Handles session_type mapping differences
- Provides a stable interface even if training_load schema evolves

Currently, `exercise_recommendation_service.py` reads training_load_events directly via SQL.

---

## 3. Data Model Stress Test

### 3.1 Schema Issues

```
training_load_events
  session_rpe INT CHECK (1-10)
  load_score DECIMAL(10,2)  (= duration_minutes × session_rpe)
```

**Volume projection:**
- A team of 30 athletes × 6 sessions/week × 52 weeks = 9,360 rows/year
- A sports org with 500 athletes = 156,000 rows/year
- A college athletic dept with 2,000 athletes = 624,000 rows/year

**Problem:** The `load_score` is a derived column (duration × RPE). If session_rpe or duration_minutes is updated, `load_score` becomes stale. The CHECK constraint is also insufficient — there is no FK to the `rpe_codes` table (which doesn't exist).

**Fix:** Make `load_score` a generated column: `load_score = duration_minutes * session_rpe` as a computed column, or use a trigger to recalculate on update.

```
injury_risk_profiles
  valid_until DATE DEFAULT NULL  (NULL = active)
```

**Problem:** Only one active profile per athlete should exist at any time, but the schema allows multiple NULL `valid_until` rows per athlete. A partial unique index is needed.

**Fix:** 
```sql
CREATE UNIQUE INDEX idx_one_active_profile
  ON injury_risk_profiles(athlete_id) WHERE valid_until IS NULL;
```

```
recommendation_log
  demand_scores JSONB NOT NULL DEFAULT '[]'::jsonb
  candidate_rankings JSONB NOT NULL DEFAULT '[]'::jsonb
```

**Volume projection (recommendation_log):**
- 500 athletes × 52 weeks × 1 cycle/week = 26,000 rows/year
- Each row stores full demand_scores (likely >50KB per row with exercise detail)
- 26,000 × 50KB = 1.3 GB/year of recommendation_log alone

**Problem:** JSONB stores full candidate rankings on every row. Over 3 years, this is ~4 GB with slow sequential scans if `engine_version` or `cached` columns are used for filtering.

**Fix:** Archive rows older than 90 days to a `recommendation_log_archive` table (same schema, different tablespace). Add a partial index on `(athlete_id, created_at)` for recent data.

```
coach_feedback
  recommendation_id UUID REFERENCES recommendation_log(recommendation_id) ON DELETE CASCADE
```

**Problem:** If a recommendation_log row is deleted (e.g., during archival or cleanup), all coach feedback for that recommendation is also deleted. This destroys the feedback loop.

**Fix:** Remove CASCADE or use `ON DELETE SET NULL` and handle missing recommendations gracefully in the coach feedback query.

### 3.2 Missing Indexes

- `idx_training_load_session_type` — needed for filtering by type but already present
- `idx_training_load_athlete_session_date` — composite for the most common query pattern
- `idx_injury_risk_athlete_valid` — needed for "get latest active profile" query
- `idx_recommendation_log_org_created` — needed for organization-level observability queries

### 3.3 Potential Dead Tuples Problem

The ACWR view (`acute_chronic_load_view`) is a regular view backed by `training_load_events`. Every load event insertion triggers a full recalc. With 500 athletes and daily load events, this is fine. But if the table grows to 600K+ rows without proper autovacuum, the view query will scan dead tuples.

**Fix:** Convert to a materialized view with periodic refresh (or incremental materialization with triggers) if query performance becomes an issue.

---

## 4. Configuration Explosion Map

### 4.1 Current Configuration Surface

| Configuration Point | Location | Values | Who Sets It? | Cardinality |
|--------------------|----------|--------|-------------|-------------|
| development_level multiplier | demand_scoring_engine.py:840 | {FOUNDATION:0.7, DEVELOPMENT:0.85, PERFORMANCE:1.0} | Hardcoded | 3 values |
| deficit_severity normalization caps | demand_scoring_engine.py:811-817 | CMJ:50, Broad:3, Deadlift:250, Pull:20, Rotational:12 | Hardcoded | 5 values |
| exercise_mapping difficulty_range, mechanics, load_character | exercise_recommendation_service.py:195 | Hardcoded strings | Hardcoded | 3 categories |
| demand_category priority weights | demand_assessment_mapping table | Per-demand INTEGER | Coach/Admin | Per-sport (~15 values) |
| exercise-to-demand mapping | exercise_demand_mapping table | Many-to-many | Coach/Admin | Per-exercise |
| ACWR zone thresholds | injury_risk_service.py | {low:0-0.8, normal:0.8-1.3, high:1.3-1.5, critical:>1.5} | Hardcoded | 4 zones |
| session_rpe range | training_load_events schema | 1-10 | Schema CHECK | 10 values |
| LOOKBACK_DAYS for trends | demand_scoring_engine.py:21 | 28 | Hardcoded | 1 value |
| recommendation_limit K | exercise_recommendation_service.py | 5 (implied) | Hardcoded | 1 value |

### 4.2 Configuration Chaos Score: 7/10

**Too many hardcoded values:** Deficit normalization caps, development_level multipliers, ACWR thresholds, recommendation limit, lookback days — 7 distinct configuration groups are hardcoded across the codebase.

**No configuration registry:** There is no centralized configuration schema, no UI for coaches to adjust thresholds, no versioning of configuration changes.

**No per-sport overrides:** The deficit normalization caps are the same for all sports. A basketball CMJ deficit of 10cm is treated identically to a soccer CMJ deficit — but the performance implications are completely different.

**Mixing config and code:** `exercise_recommendation_service.py:195` has hardcoded strings for `difficulty_range`, `mechanics`, and `load_character` filtering. These are configuration concerns embedded in business logic.

### 4.3 Risk of Configuration Entropy

If the system ships with 9 hardcoded values, within 3 months of production use, coaches will request:
- Sport-specific deficit normalization
- Position-specific priority weights (beyond what `role_id` provides)
- Phase-of-season-specific multipliers
- Athlete-specific lookback windows

Each request becomes a code change. The system needs a proper configuration service with:
- A `system_config` table with key/value/scope/sport_id/valid_from/valid_until
- Versioned config snapshots tied to recommendation_log rows (so you can replay historical recommendations with the exact config that generated them)
- UI-first config design (if it can't be set via UI, it should not exist)

---

## 5. Event-Driven Architecture Gap Analysis

### 5.1 Current Event Map

| Event | Emitter | Consumer | Deliverability | Idempotent? |
|-------|---------|----------|---------------|-------------|
| TrainingLoadRecorded | domain_events.py:100 | None (fire-and-forget) | At-most-once | N/A |
| ACWRCalculated | domain_events.py:115 | None (fire-and-forget) | At-most-once | N/A |
| InjuryRiskUpdated | domain_events.py:137 | None (fire-and-forget) | At-most-once | N/A |
| DemandScoreCalculated | domain_events.py:159 | None (fire-and-forget) | At-most-once | N/A |
| AssessmentMetricsExtracted | domain_events.py:183 | None (fire-and-forget) | At-most-once | N/A |

### 5.2 Critical Gap: No Consumers

Every event is fire-and-forget with `at-most-once` delivery. **No event has a registered consumer in the current codebase.** The events table exists, the events are emitted, but nothing subscribes to them.

This means:
- TrainingLoadRecorded is emitted but the ACWR recalculation is NOT triggered by the event — it's a separate API call
- ACWRCalculated is emitted but InjuryRiskUpdated is NOT triggered — it's also a separate API call
- DemandScoreCalculated is emitted but recommendation is NOT triggered — also a separate API call

The system is event-aware but NOT event-driven. Events are audit trails, not workflow triggers. This creates opportunities for stale data: if the pipeline is invoked out of order, or if an intermediate step fails silently, the system produces a recommendation from stale intermediate values.

### 5.3 Missed Opportunity: Event Sourcing

The `domain_events` table already has all the attributes needed for event sourcing (aggregate_type, aggregate_id, event_type, event_data, version). But the aggregate state is NOT reconstructed from events — it's stored in separate tables like `injury_risk_profiles` and `recommendation_log`.

If the system ever needs to rebuild state (e.g., after a bug fix re-runs demand scoring), the events alone are insufficient because:
- Events are stored but not ordered per aggregate_id in a way that supports replay
- There's no snapshot mechanism
- The event `version` field exists but is never incremented or checked

### 5.4 Event Schema Consistency

Event data payloads across different events follow different naming conventions:
- `emit_acwr_calculated` uses keys: `acwr`, `acute_7_day_load`, `chronic_28_day_load`
- `emit_injury_risk_updated` uses keys: `profile_id`, `risk_level`, `risk_score`
- `emit_demand_score_calculated` uses keys: `athlete_id`, `demand_score`, `trend_score`, `priority_score`

Some use snake_case (athlete_id), some use camelCase (injuryRiskUpdated pattern from earlier event names). The `event_data` itself is a flat dict with no schema validation.

### 5.5 Recommendations

1. **Convert critical events to async workflows.** At minimum: TrainingLoadRecorded → ACWRCalculated → InjuryRiskUpdated should be a chained async pipeline with retry and dead-letter queue support.

2. **Add a `correlation_id` to event_data** that flows through the entire pipeline for a single recommendation cycle. This enables end-to-end tracing for debugging observability.

3. **Add event versioning.** The `domain_events` table has a `version` column. Use it to support schema evolution of event payloads.

4. **Consider replacing fire-and-forget with an outbox pattern.** Currently, if the event emission fails (DB error), the transaction commits but the event is lost. An outbox table ensures events are reliably delivered.

---

## 6. AI/ML Readiness Assessment

### 6.1 Current ML Surface

The system is purely rules-based: no learned weights, no model inference, no ML pipeline. The closest thing to "learning" is the `trend_score` in `DemandScoreCalculated` events — but the trend computation is a simple moving average, not a learned model.

### 6.2 Data Sufficiency Score: 4/10

**Adequate for:**
- Coach feedback patterns (coach_feedback table has enough signal after ~500 entries to predict acceptance likelihood)
- Deficit-to-improvement correlation (training_load_events + assessment results can model "did this exercise improve the deficit?")

**Insufficient for:**
- Individualized ACWR thresholds (needs 100+ training sessions per athlete to learn personal sweet spots)
- Exercise sequencing optimization (needs session-level outcomes, not just exercise-level recommendations)
- Injury prediction (the injury_risk_profiles table has no ground truth — no "did they get injured?" outcome column)

### 6.3 Required Data Infrastructure for ML Readiness

1. **Add ground truth outcome column.** `injury_risk_profiles` needs an `actual_outcome` column (injured/not_injured/unknown) that is populated by coach reporting. Without this, no supervised learning is possible.

2. **Add session-level outcome data.** `training_load_events` has no "was this session effective?" column. Add an `outcome_score` (1-5) that athletes or coaches can rate session quality.

3. **Build training dataset pipeline.** The recommendation_log + coach_feedback tables contain recommendation_id → coach_decision pairs. This is the only supervised learning signal in the system. Extract it into a training view:
```sql
CREATE VIEW ml_training_data AS
SELECT
  rl.athlete_id,
  rl.demand_scores,
  rl.candidate_rankings,
  rl.assessment_snapshot,
  cf.coach_decision,
  cf.acceptance_status
FROM recommendation_log rl
LEFT JOIN coach_feedback cf ON rl.recommendation_id = cf.recommendation_id
WHERE cf.id IS NOT NULL;
```

4. **Add feature store columns.** `athlete_intelligence_layers` table should store engineered features:
- `rolling_acwr_variance` (volatility in load)
- `deficit_improvement_rate` (delta deficit per month)
- `exercise_diversity_score` (how many distinct exercise categories completed)
- `coach_trust_score` (how often coach accepts recommendations)

5. **Define model evaluation metric.** Before any ML is deployed, define:
- **Primary metric:** Coach acceptance rate (accepted / total recommended)
- **Secondary metric:** Exercise-to-deficit improvement correlation
- **Counter-metric:** Oscillation frequency (how often top-3 changes week-over-week without coach action)

### 6.4 Fallback Strategy

The current rules-based system has no fallback. If the rules produce no valid exercises (e.g., equipment_match = 0 for all exercises, or deficit computation fails), the system returns an empty list. An ML-based system would need a "dumb fallback" — the same rules engine as a tier-2 fallback when model confidence < threshold.

---

## 7. Production Operations Review

### 7.1 Monitoring Gaps

| Concern | Current State | Required |
|---------|--------------|----------|
| Pipeline latency | Not tracked | P95 latency per recommendation cycle |
| Demand score drift | Not tracked | Weekly KS-test comparing current score distributions vs historical |
| Empty recommendation rate | Not tracked | Alert if >5% of recommendation cycles return 0 candidates |
| Coach override rate | In coach_feedback but no dashboard | Weekly trend of acceptance vs rejection |
| ACWR calculation failures | Not tracked | Count of NULL or division-by-zero in acwr view |
| Configuration changes | Not tracked | Audit log for all config changes |
| Stale athlete data | Not tracked | Alert if athlete has no assessment >30 days or load events >7 days |

### 7.2 Observability Architecture Gaps

The recommendation_log is excellent for ad-hoc queries but has no:
- **Metrics endpoint** for Prometheus-style scrape (count of recommendations by status, P50/P95 compute time)
- **Structured logging** for the pipeline steps (currently no logging at all in the critical path)
- **Health check** for the pipeline ("can this athlete get a recommendation?" — returns OK/FAIL with reason)

### 7.3 Alerting Requirements

Minimum viable alerting:
1. `recommendation_empty > 0` — pipeline produced no exercises
2. `p95_latency > 5000ms` — pipeline too slow
3. `coach_rejection_rate > 0.5 over 7d` — pipeline quality degraded
4. `acwr_null_rate > 0.1` — chronic load data insufficient for too many athletes
5. `pipeline_error_rate > 0.01` — any SQL or Python exception in the pipeline

### 7.4 Deployment & Rollback Strategy

**Current:** No migration strategy is documented. Schema migrations have no down.sql files for rollback.

**Risk:** Deploying migration 000024 with the `coach_feedback` trigger creates a function `trigger_set_timestamp()` at the database level. If multiple features create similar triggers, naming collisions will occur. The function name is too generic.

**Fix:** Rename to `trigger_update_coach_feedback_timestamp_func()` or namespace by feature.

### 7.5 Caching Strategy

The recommendation_log has a `cached` column but no caching logic is implemented in the application layer. There's no cache TTL, no cache invalidation, no cache warming.

**Recommendation:**
- Cache recommendation results for 1 hour (or until a relevant event occurs)
- Invalidate on: new training_load_event, new assessment, coach_feedback insert
- Use `cached=true` flag in recommendation_log to mark cache hits for observability

---

## 8. Security & Privacy Review

### 8.1 Authentication & Authorization

**Current:** No auth checks visible in any service. The services accept `athlete_id`, `organization_id` as parameters without verifying that the caller is authorized to access that athlete's data.

**Risk:** A coach from org A could request recommendations for an athlete from org B by manipulating the API parameters.

**Fix:** All service methods must accept and validate `requesting_org_id` against `athlete.organization_id`.

### 8.2 Data Privacy

The recommendation_log stores full `assessment_snapshot` JSONB with what appears to be athlete-level assessment results. If an assessment contains PII (name, date of birth, medical history), it would be exposed in the log.

**Risk:** The log is append-only and never prunes PII. A data subject access request (DSAR) would need to scan the entire log.

**Fix:** 
- Implement PII classification in assessment data
- Store PII separately and reference by ID only
- Add automated PII purging after 90 days for log entries

### 8.3 Data Integrity

The `domain_events` table has no immutable flag. Events can theoretically be updated or deleted (no trigger prevents it). Once a domain event is recorded, it should be immutable — this is the foundation of event-driven trust.

**Fix:** Add a trigger that prevents UPDATE or DELETE on domain_events:
```sql
CREATE FUNCTION prevent_domain_event_mutation() RETURNS TRIGGER AS $$
BEGIN
  RAISE EXCEPTION 'domain_events are immutable: update/delete not allowed';
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_update
  BEFORE UPDATE ON domain_events
  FOR EACH ROW EXECUTE FUNCTION prevent_domain_event_mutation();

CREATE TRIGGER trg_prevent_delete
  BEFORE DELETE ON domain_events
  FOR EACH ROW EXECUTE FUNCTION prevent_domain_event_mutation();
```

### 8.4 RBAC Requirements

The system needs at minimum:
- **Athlete:** Can see own recommendations, cannot modify
- **Coach:** Can see athletes in own org, can submit feedback, cannot modify config
- **Admin:** Can modify config, can view all org data
- **System:** Pipeline execution (no user context)

---

## 9. Migration & Coexistence Strategy

### 9.1 V1 → V2 Coexistence Risks

The system implicitly assumes a greenfield deployment. There is no documented migration path from an older V1 system (which may use different schema, different demand definitions, different exercise IDs).

**Risks:**
- Athlete_ids differ between V1 and V2 if migrated
- Historical training_load_events in V1 format don't match V2 schema
- V1 recommendation results cannot be compared to V2 results for A/B validation

**Fix:** Add a `source_system` column to `recommendation_log` (`V1`/`V2`) and an `engine_version` column (already exists). Run both engines in parallel for one cycle and compare results before full cutover.

### 9.2 Data Migration Requirements

1. **Exercise library:** Must be identical between V1 and V2 or mapping breaks
2. **Demand definitions:** Must be reconciled or a mapping table created
3. **Historical ACWR:** Must be backfilled for all existing athletes (the view handles this, but 28 days of chronic load data must exist)
4. **Assessment history:** Must be re-ingested to populate `trend_score`

### 9.3 Rollback Plan

To roll back from V2 to V1:
1. Stop pipeline execution
2. Keep recommendation_log for analysis (don't delete)
3. Revert to V1 pipeline
4. Coach feedback from V2 period is preserved but may reference recommendation_ids that no longer apply

**Missing:** No documented rollback procedure. No feature flag for V2 pipeline.

---

## 10. Testing Strategy Assessment

### 10.1 Current Test Coverage

**Status:** Tests exist but are not exhaustive. The `demand_scoring_engine.py` is testable (pure functions with dependency injection), but `exercise_recommendation_service.py` requires database mocking for the multi-table join.

### 10.2 Critical Test Scenarios Not Covered

1. **Empty state test:** What happens when an athlete has no training_load_events, no assessments, and no injury risk profile?
2. **Boundary conditions test:** ACWR exactly at threshold boundaries (0.8, 1.3, 1.5)
3. **Overlapping roles test:** Athlete with multiple role_ids producing conflicting demand priorities
4. **All equipment missing test:** What if the exercise library has no exercises matching the athlete's equipment?
5. **Concurrent recommendation test:** Two coaches requesting recommendation for same athlete simultaneously
6. **Performance test:** 500 athletes × 200 exercises × 15 demands × 3 roles — does the query finish in < 5 seconds?
7. **Stability test:** 50 sequential recommendation cycles — do demand_scores oscillate?

### 10.3 Testing Infrastructure Requirements

- **Fixture factory:** Function to create realistic athletes, training_load_events (28+ days), assessments, injury profile, and exercise library in test DB
- **Performance test suite:** `locust` or `k6` test that simulates 100 concurrent recommendation requests
- **Determinism test:** Same input → same output, verified across 3 runs
- **Chaos test:** Randomly inject NULLs, missing rows, malformed JSON into intermediate tables and verify graceful degradation

### 10.4 Acceptance Criteria (Missing)

No documented acceptance criteria exist for the pipeline:
- Maximum acceptable latency
- Minimum acceptable coach acceptance rate
- Maximum oscillation frequency
- Maximum empty recommendation rate

Without these, it's impossible to determine "does the system work?"

---

## 11. Performance & Scalability Review

### 11.1 Query Complexity Analysis

**The critical query** (exercise recommendation) joins:
- `demands` (sport_id filter) ~150 rows
- `demand_assessment_mapping` (demand_id filter) ~450 rows
- `exercise_demand_mapping` (demand_id filter, exercise_id) ~3,000 rows
- `exercises` (filters: mechanics, load_character, equipment_required) ~2,000 rows

This is a **4-table join** with ~20,000 intermediate rows in the worst case. With proper indexes:
- Filter by sport: reduces demands to ~15
- Filter by category: reduces further
- Equipment filter can be expensive if equipment_required is stored as JSONB array and requires `@>` containment operator

**Per-request complexity:** O(demands × exercises × mapping cardinality) = ~15 × 200 × 3 = ~9,000 candidate exercise-demand pairs to score. This is trivially fast for a single request, but at 500 concurrent requests (e.g., coaches running batch recommendations), the database connection pool must handle 500 simultaneous 4-table joins.

### 11.2 Identified Bottlenecks

1. **JSONB containment queries** for equipment filtering. `exercises.equipment_required @> ARRAY[equipment_list]` can't use standard B-tree indexes. Needs GIN index on `equipment_required`.

2. **Sequential recommendation per athlete.** There is no batched recommendation flow. Each athlete recommendation is a separate query. For a coach with 50 athletes, this is 50 round-trips.

3. **ACWR view is not materialized.** The `acute_chronic_load_view` must scan training_load_events for every athlete on every recommendation cycle. At 600K rows, this scan takes 200–500ms even with indexes.

### 11.3 Scalability Recommendations

1. **Add GIN index on exercises.equipment_required:**
```sql
CREATE INDEX idx_exercises_equipment ON exercises USING GIN (equipment_required);
```

2. **Batch recommendation endpoints.** Add a POST /recommendations/batch endpoint that accepts [athlete_id, ...] and returns a single response.

3. **Materialize the ACWR view** if the query profile shows >20 concurrent recommendation requests.

4. **Add connection pooling** (PgBouncer or application-level pool) with max_connections tuned for the workload.

5. **Consider denormalizing demand_score into a cached table** if recommendation cycles are frequent. Recompute only when assessment data changes, not on every read.

---

## 12. Final Verdict & Recommendations

### 12.1 Ship Readiness Score: 5/10

**What's ready (score 7-9):**
- Training load recording and ACWR calculation
- Domain event emission (though without consumers)
- Recommendation log and coach feedback data model
- Injury risk profile model
- Demand assessment mapping

**What's fragile (score 4-6):**
- Demand scoring (hardcoded normalization, no damping, inflation risk)
- Exercise recommendation (no diversity, no constraints)
- Pipeline orchestration (no async workflow, no error handling)
- Test coverage (no empty state, no performance tests)

**What's missing or broken (score 1-3):**
- Event consumers (events are emitted but nothing listens)
- Security (no auth, no RBAC, no PII management)
- Operational monitoring (no metrics, no alerts, no health checks)
- Configuration management (9 hardcoded values)
- Migration/coexistence strategy (no rollback plan)

### 12.2 Must-Fix Before Ship (sorted by priority)

1. **HIGH — Add event consumers for the pipeline chain:** TrainingLoadRecorded → ACWRCalculated → InjuryRiskUpdated → Recommendation. Currently the pipeline has no async workflow; each step must be called manually.

2. **HIGH — Add demand_score temporal damping:** Without it, the system will oscillate and undermine coach trust within 2-3 cycles.

3. **HIGH — Add empty state handling:** If any intermediate step fails, the system must return a meaningful error, not an empty list.

4. **HIGH — Implement auth/RBAC:** The system currently allows cross-organization data access.

5. **HIGH — Add coach_feedback ON DELETE SET NULL:** The current CASCADE will destroy feedback data on recommendation_log cleanup.

6. **MEDIUM — Add partial unique index on injury_risk_profiles:** Prevent duplicate active profiles per athlete.

7. **MEDIUM — Add core test scenarios:** Empty state, boundary conditions, 50-cycle stability.

8. **MEDIUM — Add recommendation coverage constraint:** Prevent exercise starvation.

9. **MEDIUM — Convert load_score to generated column:** Prevent stale derived data.

10. **MEDIUM — Add P95 latency monitoring.**

### 12.3 Should-Fix Before Ship (score +2-4 items)

11. Add GIN index on exercises.equipment_required
12. Domain events immutability trigger
13. Add correlation_id to event flow
14. Normalize demand_scores to 0-100 per cycle
15. Add source_system column to recommendation_log for V1 coexistence
16. Document acceptance criteria

### 12.4 Architectural Debt Accepted (score +1 items)

- ACWR view not materialized (mitigated: monitoring)
- Configuration registry not built (mitigated: document as future ADR)
- Event sourcing not implemented (mitigated: current event audit trail is sufficient)
- ML pipeline not built (mitigated: rules-based system is acceptable for V2)

### 12.5 Summary

The V2 Demand Recommendation Engine has solid foundations in its data model, domain events, and observability infrastructure. The demand scoring and exercise recommendation logic is functional for an initial rules-based system. However, the system has **three fatal architectural gaps** that will cause it to fail in sustained production use:

1. **The event-driven architecture has no consumers.** Events are emitted but nothing happens as a result. The pipeline is effectively a synchronous RPC chain with no resilience.
2. **The recommendation engine has no feedback damping.** Demand scores will oscillate, coach trust will erode, and adoption will stall.
3. **The system has no security boundary.** Cross-organization data access is trivially possible.

Fix these three issues, and the system is ship-ready at a 7/10 level. Leave them unfixed, and the system will fail within 4 weeks of production deployment.
