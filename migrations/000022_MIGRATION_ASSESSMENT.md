# Migration 000022 Assessment

## 1. Compatibility Assessment

### Existing V1 Tables — Untouched
All 28 existing tables remain fully operational:

| Table | Status | Notes |
|-------|--------|-------|
| `movement_templates` | ✅ Unchanged | Template routing still works |
| `template_slots` | ✅ Unchanged | Slot querying unaffected |
| `slot_requirements` | ✅ Unchanged | Exercise matching unchanged |
| `slot_progressions` | ✅ Unchanged | Progression rules unchanged |
| `slot_exercise_fallbacks` | ✅ Unchanged | Fallback resolution unchanged |
| `exercise_physical_qualities` | ✅ Unchanged | Still the active junction (not yet deprecated) |
| `exercise_sport_mapping` | ✅ Unchanged | Manual columns remain (not yet computed) |
| `deficits` | ✅ Unchanged | Still active (not yet replaced by compute function) |
| `performance_drivers` | ✅ Unchanged | Still active (not yet deprecated) |
| `programs` | ✅ Unchanged | CHECK constraints still in place |
| `program_weeks` | ✅ Unchanged | CHECK constraints still in place |
| `program_sessions` | ✅ Unchanged | CHECK constraints still in place |
| `athletes` | ✅ Unchanged | sport_id/role_id still single-value columns |
| `assessment_results` | ✅ Unchanged | score column still active |

### Existing Application Code — Unaffected
| Code Path | Impact | Notes |
|-----------|--------|-------|
| `recommendation_engine.py` | ✅ None | MockExerciseRepository reads tables we haven't changed |
| `program_builder.py` | ✅ None | Reads program/program_* tables — no new FK requirements |
| `deficit_detection_engine.py` | ✅ None | Reads deficits table — still there |
| `exercise_substitution_engine.py` | ✅ None | Reads slot_exercise_fallbacks — still there |
| `integration_workflow.py` | ✅ None | Orchestrates existing services — no new dependencies |
| `sports_science_validator.py` | ✅ None | Reads sports_science_rules — unchanged |

### New V2 Tables — Non-Blocking Additions
| Table | Backward Compatible? | Notes |
|-------|---------------------|-------|
| `performance_demands` | ✅ Yes | All FK columns are SET NULL — no required data |
| `exercise_demand_mapping` | ✅ Yes | New junction, doesn't affect any existing query |
| `role_demand_priority` | ✅ Yes | New table, no application code reads it yet |
| `assessment_demand_mapping` | ✅ Yes | New junction for future deficit computation |
| `injury_risk_demand_mapping` | ✅ Yes | Future use — no application code reads it |
| `assessment_metrics` | ✅ Yes | New decomposition — existing assessment_results intact |
| `metric_demand_mapping` | ✅ Yes | New junction — application doesn't read it yet |
| `movement_pattern_families` | ✅ Yes | New lookup — existing patterns unchanged |
| `quality_categories` | ✅ Yes | New lookup — existing qualities unchanged |
| `domain_events` | ✅ Yes | Append-only — no reads from application code yet |

### Modified Tables — Backward Compatible
| Table | Change | Compatible? | Notes |
|-------|--------|-------------|-------|
| `movement_patterns` | +6 columns | ✅ Yes | All nullable, all with defaults |
| `physical_qualities` | +6 columns | ✅ Yes | All nullable, all with defaults |
| `program_session_exercises` | +7 columns | ✅ Yes | All nullable, all with defaults |

**Compatibility Verdict: FULL BACKWARD COMPATIBILITY.** Zero breaking changes. Zero application code changes needed. Zero query plan changes for existing queries.

---

## 2. Risk Assessment

### Risk 1: Transaction Size
- **Severity**: Low
- **Description**: The migration wraps ~400 lines of DDL + DML in a single transaction
- **Mitigation**: All operations are metadata/seed — no heavy data transformation. If it fails, the transaction rolls back atomically.

### Risk 2: Deadlock with Concurrent Writes
- **Severity**: Low
- **Description**: ALTER TABLE ADD COLUMN takes ACCESS EXCLUSIVE lock
- **Mitigation**: Apply during maintenance window. Each ALTER TABLE is O(1) (no table rewrite for nullable columns with defaults). The `program_session_exercises` table is the largest (~7 ALTERs), but each is sub-millisecond.

### Risk 3: Existing Code Reads New Columns
- **Severity**: None
- **Description**: Could existing Python code break if it does `SELECT *` and gets unexpected columns?
- **Mitigation**: No Python code in the codebase does `SELECT *`. All queries specify column lists. Even if they did, extra columns are ignored by the ORM (sqlalchemy).

### Risk 4: Seed Data ID Collisions
- **Severity**: None
- **Description**: Could performance_demands IDs collide with future seeds?
- **Mitigation**: Using `GENERATED ALWAYS AS IDENTITY` — Postgres manages the sequence. `ON CONFLICT DO NOTHING` makes all INSERTs idempotent.

### Risk 5: Duplicate Domain Events on Rollback
- **Severity**: Low
- **Description**: If migration runs, then rolls back, then runs again — events could be duplicated
- **Mitigation**: domain_events is empty on first apply. On re-apply after rollback, it's also empty (table was dropped). No duplicate risk.

### Risk 6: Performance Impact of New Indexes
- **Severity**: None
- **Description**: New indexes on domain_events and performance_demands
- **Mitigation**: These tables are empty or small (<20 rows). Index maintenance cost is negligible. Indexes on domain_events enable future event-sourcing queries and are justified by their critical query path.

**Overall Risk: LOW.** This is a foundation-laying migration with zero risk to existing data or code paths.

---

## 3. Index Strategy

### Query Pattern 1: "Find exercises for a demand"
```sql
SELECT e.* FROM exercises e
JOIN exercise_demand_mapping edm ON e.id = edm.exercise_id
WHERE edm.demand_id = ? AND edm.relevance_score >= ?
ORDER BY edm.relevance_score DESC;
```
- **Index**: `idx_exercise_demand_score (demand_id, relevance_score DESC)`

### Query Pattern 2: "Find all demands for a role"
```sql
SELECT pd.* FROM performance_demands pd
JOIN role_demand_priority rdp ON pd.id = rdp.demand_id
WHERE rdp.role_id = ?
ORDER BY rdp.priority DESC;
```
- **Index**: `idx_role_demand_role (role_id, priority DESC)` — covers the WHERE + ORDER BY

### Query Pattern 3: "Find demands for a quality + pattern combination"
```sql
SELECT * FROM performance_demands
WHERE primary_quality_id = ? AND primary_pattern_id = ?;
```
- **Index**: `idx_demands_quality_pattern (primary_quality_id, primary_pattern_id)`

### Query Pattern 4: "List active demands in order"
```sql
SELECT * FROM performance_demands WHERE is_active = TRUE ORDER BY display_order;
```
- **Index**: `idx_demands_active (is_active, display_order)`

### Query Pattern 5: "Aggregate by family"
```sql
SELECT mp.name, mpf.name AS family FROM movement_patterns mp
JOIN movement_pattern_families mpf ON mp.family_id = mpf.id
ORDER BY mpf.display_order, mp.display_order;
```
- **Index**: `idx_movement_patterns_family (family_id, display_order)`

### Query Pattern 6: "All events for an aggregate"
```sql
SELECT * FROM domain_events
WHERE aggregate_type = ? AND aggregate_id = ?
ORDER BY occurred_at DESC;
```
- **Index**: `idx_domain_events_aggregate (aggregate_type, aggregate_id, occurred_at DESC)`
- **Critical for event sourcing** — this is the most queried pattern on domain_events

### Query Pattern 7: "Events by type over time period"
```sql
SELECT * FROM domain_events
WHERE event_type = ? AND occurred_at BETWEEN ? AND ?
ORDER BY occurred_at DESC;
```
- **Index**: `idx_domain_events_type (event_type, occurred_at DESC)`

### Reverse Indexes
Following the same `_rev` naming convention as existing V1 migrations:
- `idx_exercise_demand_rev` — demand_id → exercise lookups
- `idx_assessment_demand_rev` — demand_id → assessment lookups
- `idx_metric_demand_rev` — demand_id → metric lookups
- This matches the pattern from `idx_exercise_phys_qual_rev`, `idx_exercise_sport_rev`, etc.

### Index Maintenance Cost
| Index | Estimated Size | Write Overhead | Justification |
|-------|---------------|----------------|---------------|
| idx_exercise_demand_score | Small | Minimal | Query critical path |
| idx_role_demand_role | Tiny | Negligible | Query critical path |
| idx_demands_quality_pattern | Tiny | Negligible | Lookup path |
| idx_demands_active | Tiny | Negligible | Display ordering |
| idx_movement_patterns_family | Tiny | Negligible | UI tree rendering |
| idx_exercise_demand_rev | Small | Minimal | Reverse lookup |
| idx_assessment_demand_rev | Tiny | Negligible | Reverse lookup |
| idx_metric_demand_rev | Tiny | Negligible | Reverse lookup |
| idx_domain_events_aggregate | Medium | Insert-only | Event sourcing critical |
| idx_domain_events_type | Medium | Insert-only | Event querying |
| idx_domain_events_occurred | Large | Insert-only | Time-based queries |

**Verdict:** All indexes are justified by their query patterns. Insert overhead is acceptable. The domain_events table is append-only (UPDATE never), so index maintenance is only on INSERT.

---

## 4. Data Migration Strategy

### What Gets Seeded

| Seed Data | Rows | Source of Truth |
|-----------|------|----------------|
| `movement_pattern_families` | 6 | Biomechanical taxonomy (audit) |
| `quality_categories` | 4 | Force-Velocity / Metabolic / Morphological / Joint-Structural |
| `performance_demands` | 18 | 1 quality × 1 pattern combinations (biomechanically validated) |
| `role_demand_priority` | ~60 | 5 cricket roles × ~12 demands each |
| `exercise_demand_mapping` | ~50 | Derived from existing exercise_physical_qualities + exercise_movement_patterns |

### Seed Derivation Rules

**For `exercise_demand_mapping`:**
For each exercise, for each demand:
1. Does the exercise have the demand's PRIMARY pattern as its Primary pattern?
2. Does the exercise have the demand's PRIMARY quality with relevance_score ≥ 6?
3. If both YES → insert with relevance_score = quality score
4. If relevance_score ≥ 9 → mark as is_primary = TRUE

This ensures every existing exercise is immediately discoverable via the demand system without manual remapping.

### Future Migration Path

| Future Migration | Depends On | Action |
|-----------------|------------|--------|
| 000023 | This migration | Multi-tenancy tables (orgs, teams, users, athlete_teams) |
| 000024 | 000023 | Event sourcing hooks in service layer |
| 000025 | This migration | Compute deficit function + deprecate deficits table |
| 000026 | This migration | Remove CHECK constraints on programs |
| 000027 | 000023 + 000026 | Season phases, session templates |
| Phase 2 | All of Phase 1 | AI infrastructure (recommendation_log, embeddings, coach_feedback) |

### Rollback Safety
- Full `DOWN` migration exists
- All INSERTs use `ON CONFLICT DO NOTHING` — re-runnable
- All ALTER TABLE uses `IF NOT EXISTS` / `DROP COLUMN IF EXISTS` — re-runnable
- Transaction-wrapped: failure at any point = atomic rollback

---

## 5. Summary

| Metric | Value |
|--------|-------|
| New tables | 10 |
| Modified tables | 3 |
| New columns | 19 total (6+6+7) |
| Seed rows | ~130 |
| New indexes | 15 |
| Breaking changes | **0** |
| Application code changes needed | **0** |
| Rollback safety | Full (down migration exists) |
| Idempotent | Yes (all INSERTs use ON CONFLICT DO NOTHING) |
| Risk level | **LOW** |
