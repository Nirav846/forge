# SURVIVABILITY AUDIT: Forge Performance Demand Architecture

**Date:** 2026-06-17
**Scope:** 10-year viability as OS for athlete development
**Scale Target:** 50+ sports, 500+ roles, 5,000+ exercises, 100,000+ athletes
**Methodology:** Apply 10 "death test" scenarios to every proposed entity

---

## EXECUTIVE SUMMARY

**Verdict: The Performance Demand core ontology survives. The application architecture does not.**

The `performance_demands → exercise_demand_mapping` pivot is correct and will survive 10+ years.
But the surrounding application layer (tenancy, identity, events, program structure) has **7 critical gaps** that will force major redesign within 2-3 years.

**Survivability Score (0-100): 42/100**

| Layer | Score | Verdict |
|-------|:-----:|---------|
| Demand Ontology | 90/100 | Solid. 1-quality-1-pattern is correct. |
| Exercise Mapping | 85/100 | Junction table pattern correct. Add metadata_json. |
| Assessment/Metrics | 70/100 | Need assessment_metrics decomposition urgently. |
| Program Structure | 35/100 | Rigid constraints, no execution tracking, no phase calendar. |
| Multi-Tenancy | 0/100 | **Completely missing.** No orgs, teams, coaches, or access control. |
| Event Sourcing | 0/100 | **Completely missing.** AI has no training data. |
| Athlete Model | 30/100 | Single-sport, single-role. Multi-sport athletes unsupported. |
| AI Readiness | 45/100 | No event log, no feedback, no embeddings infrastructure. |

---

## TABLE-BY-TABLE AUDIT

### 1. `movement_patterns`

| Question | Answer |
|----------|--------|
| Should it exist? | **Yes** — fundamental taxonomy |
| Merge with anything? | **No** — distinct domain concept |
| Split? | Current flat list → family hierarchy. Add `family_id` self-reference. |
| Become metadata? | **Too important** — core to constraint solving |
| Become graph? | **Partially** — families as hierarchy in RDBMS, detail in graph (entity_graph_edges) |
| **Survives 10 years?** | **Yes**, with hierarchy addition. Patterns are stable. |

**Death test: A new sport requires a new movement pattern.** What breaks?
If the sport is land-based, zero new patterns. If aquatic (swimming), the existing 10 families suffice (Sprint → freestyle kick, Rotation → flip turn). Pattern ontology is complete.

**Action:** Add `family_id`, `display_order`, `is_active`, `metadata_json JSONB`.

---

### 2. `physical_qualities`

| Question | Answer |
|----------|--------|
| Should it exist? | **Yes** — fundamental biomotor taxonomy |
| Merge? | **No** |
| Split? | Add `category_id` (Force-Velocity, Contraction-Type, Metabolic, Joint-Structural). Add `parent_quality_id` for hierarchy (Mobility → Ankle Mobility, Hip Mobility). |
| Become metadata? | No |
| Become graph? | Hierarchy in RDBMS, detail in graph |
| **Survives 10 years?** | **Yes**, with category decomposition. 22 qualities cover all foreseeable adaptations. |

**Death test: A new training methodology requires a new quality.**
Unlikely. The force-velocity spectrum (Max Strength → Strength-Speed → Speed-Strength → RFD → Reactive Strength → Max Velocity → Acceleration) is biophysically complete.

**Action:** Add `category_id`, `parent_quality_id`, `display_order`, `is_active`, `metadata_json JSONB`.

---

### 3. `performance_demands`

| Question | Answer |
|----------|--------|
| Should it exist? | **Yes** — this is the central pivot of the entire architecture |
| Merge? | **NO** — do NOT merge with quality or pattern. The demand is the SYNTHESIS. |
| Split? | **Single table is correct.** Each demand = 1 PRIMARY quality + 1 PRIMARY pattern. Multiple qualities per demand are expressed through metric_demand_mapping weights. |
| Become metadata? | **No** — this is the CORE ENTITY. Everything routes through it. |
| Become graph? | Both RDBMS (for query) AND graph (for AI traversal). Seed `entity_graph_edges` from this table. |
| **Survives 10 years?** | **YES — this is the most survivable table in the schema.** The 18 demands cover all force-vector × contraction-type combinations for land-based sports. Adding demands for aquatic/extreme sports is additive only. |

**Death test: A new sport requires a demand that doesn't fit quality × pattern.**
Counter-example: Swimming "Aquatic Proprioception" = ??? quality + ??? pattern. This is NOT a biomotor quality + movement pattern combination. It's a sensory-motor skill.

**VERDICT:** The 1-quality × 1-pattern model fails for non-biomotor demands. Solution: Add `demand_type VARCHAR(50) CHECK (IN ('Biomotor', 'Sensory-Motor', 'Metabolic', 'Cognitive'))`. This allows the demand table to hold non-traditional demands without changing schema. Default: 'Biomotor'.

**THIS IS THE ONLY SCHEMA CHANGE NEEDED ON `performance_demands`.**

**Action:** Add `demand_type VARCHAR(50) DEFAULT 'Biomotor'`, `metadata_json JSONB`.

---

### 4. `role_demand_priority`

| Question | Answer |
|----------|--------|
| Should it exist? | **Yes** — core routing table that replaces movement_templates |
| Merge? | **No** — distinct concept |
| Split? | Add `sport_demand_profiles` for sport-level defaults (before role selected). `role_demand_priority` overrides sport defaults. |
| Become metadata? | **No** — this is the routing engine |
| Become graph? | Both. Priority weights stored in RDBMS for query. Edges seeded to graph for AI. |
| **Survives 10 years?** | **Yes, but needs sport-level default layer.** When a new athlete signs up with only sport known (not role), the system needs default priorities. |

**Death test: A sport has no formal roles (e.g., individual athletics).**
Solution: Create a single "Default" role per sport with generic priorities. This is data, not schema.

**Action:** Add `sport_demand_profiles` table. Add `metadata_json` to role_demand_priority.

---

### 5. `exercise_demand_mapping`

| Question | Answer |
|----------|--------|
| Should it exist? | **Yes** — the core junction that makes the system work |
| Merge? | **No** — do NOT merge into exercises table. M:N junction is correct. |
| Split? | **No** — single junction is correct. |
| Become metadata? | **No** |
| Become graph? | Highly. This is the most important edge type for AI: `exercise --trains--> demand`. |
| **Survives 10 years?** | **YES — cleanest table in the design.** 5K exercises × 18 demands = 90K rows. No scale issue. |

**Death test: An exercise trains a demand through multiple patterns (Depth Jump trains Reactive Strength through BOTH Jump AND Landing).**
The `relevance_score` captures overall effectiveness. The specific pattern contribution is expressed through `exercise_movement_patterns` (which is a separate, parallel taxonomy). This is correct separation of concerns.

**Action:** Add `metadata_json JSONB` for future extensibility.

---

### 6. `assessments`

| Question | Answer |
|----------|--------|
| Should it exist? | **Yes** — defines test protocols |
| Merge? | **No** |
| Split? | **No** — single table is correct. Add `assessment_metrics` for parsed outputs. |
| Become metadata? | Partially. Assessment PROTOCOLS are metadata. Assessment RESULTS are core. |
| **Survives 10 years?** | **Yes, but only with assessment_metrics.** Without metric decomposition, every new test requires schema changes. |

**Death test: Force plate CMJ produces 7 metrics. Current assessment model stores 1 score (height in cm).**
The single `score` column is a legacy bottleneck. Assessment_metrics (new table) solves this.

**Action:** Add `assessment_metrics` table. Add `sport_ids BIGINT[]` to assessments for discoverability. Add `protocol_json JSONB`. Add `metadata_json`.

---

### 7. `deficits`

| Question | Answer |
|----------|--------|
| Should it exist? | **NO — CRITICAL FLAW.** Deficits should be COMPUTED, not stored. |
| Merge with assessment_demand_mapping? | Deficits ARE the output of metric → demand mapping. They should be ephemeral query results. |
| **Survives 10 years?** | **NO — WILL BREAK.** 7 hardcoded deficit names × growing sports = enum explosion. New assessment = new deficit definition needed. |

**Death test: Sport 11 has 7 new assessments. Each maps to demands differently. The deficits table grows to 50+ rows and nobody knows which ones are active.**
Current design: `deficits(assessment_id → name)` — ties a deficit to ONE assessment. But a deficit should be a COMPUTED state across all metrics that map to a demand.

**Action:** DEPRECATE `deficits` table. Replace with `compute_deficits(athlete_id) → TABLE(demand_id, deficit_score, severity)` stored function. Deficits are VIEW-level, not TABLE-level.

---

### 8. `programs`

| Question | Answer |
|----------|--------|
| Should it exist? | **Yes** — core output |
| Merge/Split? | **Program hierarchy (4 levels) is correct.** But remove all CHECK constraints. |
| **Survives 10 years?** | **NO — WILL BREAK.** Three CHECK constraints will fail with non-cricket sports: `sessions_per_week BETWEEN 2 AND 4`, `week_number BETWEEN 1 AND 4`, `session_number BETWEEN 1 AND 4`. |

**Death test: Basketball pre-season requires 6 sessions/week for 8 weeks.**
`programs.sessions_per_week CHECK (BETWEEN 2 AND 4)` → constraint violation → application error.

**Death test: An athlete completes 1 session on Monday, 2 on Tuesday, 1 on Wednesday (variable per day).**
`program_sessions.session_number BETWEEN 1 AND 4` cannot handle >4 sessions.

**Death test: A rehab block runs for 6 weeks.**
`program_weeks.week_number BETWEEN 1 AND 4` → crash.

**Action:** 
- Remove all 3 CHECK constraints (`programs.sessions_per_week`, `program_weeks.week_number`, `program_sessions.session_number`)
- Add `programs.phase_id` → `season_phases`
- Add `programs.athlete_team_id` → `athlete_teams` (multi-sport context)
- Add `metadata_json JSONB`
- Add `training_load_initial` JSONB (baseline load at program start)

---

### 9. `program_session_exercises`

| Question | Answer |
|----------|--------|
| Should it exist? | **Yes** — core output detail |
| **Survives 10 years?** | **NO — INCOMPLETE.** Tracks PRESCRIPTION only. Missing EXECUTION. |

**Death test: "Did the athlete actually complete the prescribed work?"**
Current schema: `sets INT NOT NULL CHECK(sets > 0)`, `reps INT NOT NULL CHECK(reps > 0)`.
What's recorded: what was PLANNED. Not what was DONE.

**Death test: Injury prediction model needs actual training load per session.**
Without execution data, ACWR is computed from PLAN, not REALITY. This is scientifically invalid.

**Action:** Add execution columns alongside prescription:
- `actual_sets INT` (NULL = not yet completed)
- `actual_reps INT`
- `actual_intensity VARCHAR(100)`
- `actual_rpe INT CHECK(1-10)`
- `completed BOOLEAN DEFAULT FALSE`
- `completion_notes TEXT`
- `metadata_json JSONB`

Both prescription and execution coexist in the same row. `sets` = planned, `actual_sets` = completed.

---

## CRITICAL GAPS (Missing Entities)

### GAP 1: No Multi-Tenancy (DEATH IN YEAR 1)

**Scenario:** ECB signs up 200 athletes. BCCI signs up 300 athletes. Both see each other's data.

| Entity | Type | Schema |
|--------|------|--------|
| `organizations` | **NEW CORE** | id, name, type (federation/team/academy), metadata_json |
| `teams` | **NEW CORE** | id, organization_id, sport_id, name, competition_level, metadata_json |
| `athlete_teams` | **NEW CORE** | athlete_id, team_id, sport_id, role_id, start_date, end_date — M:N allows multi-sport |
| `users` | **NEW CORE** | id, email, role_type (admin/coach/sc/athlete), organization_id, metadata_json |
| `team_coaches` | **NEW SUPPORTING** | team_id, user_id, coaching_role, start_date |

Without these, FORGE cannot serve multiple organizations. All future features depend on athlete-team-org context.

### GAP 2: No Event Sourcing (DEATH IN YEAR 2-3)

**Scenario:** "We want to build an injury prediction model. Give us all the data."

Without `domain_events`, there is:
- No sequence of what happened
- No audit trail
- No "before/after" training data for AI
- No ability to reconstruct past states

| Entity | Type | Schema |
|--------|------|--------|
| `domain_events` | **NEW CORE** | id, aggregate_type, aggregate_id, event_type, event_data JSONB, occurred_at, recorded_at, organization_id |

Events are immutable append-only. Every meaningful action writes one:
- `athlete.created`
- `athlete.team_changed`
- `assessment.completed`
- `program.generated`
- `program.coach_modified`
- `session.completed`
- `injury.recorded`

This single table powers: AI training, injury prediction, audit, rollback, analytics, coach feedback loops.

### GAP 3: No Execution Data (DEATH IN YEAR 2)

**Scenario:** "The athlete's ACWR is 1.8. She's at high injury risk."

If ACWR uses PRESCRIBED load (not EXECUTED), the calculation is fiction. The athlete may have completed 50% of prescribed work due to fatigue.

Aliased to `program_session_exercises` missing fields above. The fix is columns, not a new table.

### GAP 4: No Season/Phase Calendar (DEATH IN YEAR 2)

**Scenario:** "Generate an in-season program for Fast Bowler."

Without season phase context:
- Engine doesn't know if it's pre-season (high volume) or in-season (maintenance)
- Difficulty/progression rules are phase-dependent
- Session templates are phase-specific

| Entity | Type | Schema |
|--------|------|--------|
| `season_phases` | **NEW SUPPORTING** | id, organization_id, team_id, name, phase_type (off/pre/in/transition), start_date, end_date, metadata_json |
| `programs.phase_id` | FK ADDITION | Links program to its seasonal context |

### GAP 5: No Coach/Practitioner Identity (DEATH IN YEAR 1)

**Scenario:** "Coach Smith wants to override the AI-generated program for his athlete."

Current: No coach exists in the system. The API accepts a `goal` string. No one knows WHO generated or modified the program.

Without coach identity:
- No personalized preferences can be learned
- No accountability for modifications
- No way to say "Coach Smith prefers single-leg work" → AI adaptation

Aliased to GAP 1 (`users` and `team_coaches` tables).

### GAP 6: No Computed Specificity (DEATH IN YEAR 3-4)

**Scenario:** 50 sports, 5,000 exercises. Each exercise mapped to each sport with specificity_rating and transfer_index. That's 250K rows if each exercise maps to 50 sports. Manual maintenance impossible.

Solution: Derive specificity from demand overlap:
```
sport_specificity(exercise, sport) = Σ(exercise.demand_weight × sport.demand_priority) / max_possible
```

**Action:** Remove `exercise_sport_mapping.specificity_rating` and `exercise_sport_mapping.transfer_index`. Replace with computed view. Keep the junction table only for sport-exercise membership (which sports use this exercise).

### GAP 7: No AI/Embedding Infrastructure (DEATH IN YEAR 3)

**Scenario:** "We trained a model. Where do we store the embeddings? Where do we log what it recommended?"

Without embedding storage, coach feedback, and recommendation logging, AI is impossible.

| Entity | Type | Schema |
|--------|------|--------|
| `exercise_embeddings` | AI | exercise_id, model_name, vector(384), created_at |
| `demand_embeddings` | AI | demand_id, model_name, vector(384), created_at |
| `coach_feedback` | AI | id, athlete_id, exercise_id, coach_id, action, reason, created_at |
| `recommendation_log` | AI | id, athlete_id, snapshot JSONB, output JSONB, model_version, latency_ms, created_at |

---

## SURVIVABILITY TEST RESULTS

### Death Test 1: Multi-Organization Day 1
**Scenario:** Two organizations sign up simultaneously.
**Result:** **SYSTEM FAILURE.** No tenant isolation. Athletes, programs, and assessments share the same table space. No way to separate ECB data from BCCI data.
**Fix Required:** `organizations`, `teams`, `users`, `athlete_teams` tables.
**Severity:** **P0 — BLOCKER**

### Death Test 2: Multi-Sport Athlete
**Scenario:** Athlete plays Cricket (Fast Bowler) AND Soccer (Forward).
**Result:** **SYSTEM FAILURE.** `athletes.sport_id` and `athletes.role_id` are single-value columns. Cannot represent multi-sport participation.
**Fix Required:** `athlete_teams` junction table replaces `athletes.sport_id` + `athletes.role_id`.
**Severity:** **P0 — BLOCKER**

### Death Test 3: Non-4-Week Block
**Scenario:** Rugby pre-season requires 8-week block.
**Result:** **APPLICATION ERROR.** `program_weeks.week_number CHECK (1-4)` constraint violation.
**Fix Required:** Remove CHECK constraints from `program_weeks` and `program_sessions`.
**Severity:** **P1 — WILL BREAK**

### Death Test 4: Variable Session Count
**Scenario:** Tennis training: Mon=3 sessions, Tue=2, Wed=1, Thu=3, Fri=2.
**Result:** **APPLICATION ERROR.** `program_sessions.session_number CHECK (1-4)` constraint violation.
**Fix Required:** Remove CHECK constraint. Add `programs.max_sessions_per_week` as metadata.
**Severity:** **P1 — WILL BREAK**

### Death Test 5: Force Plate Integration
**Scenario:** CMJ produces 7 metrics (height, RSI, peak force/BW, impulse, GCT, ecc RFD, con RFD).
**Result:** **DATA LOSS.** Current `assessment_results.score` stores 1 number. 6 metrics discarded.
**Fix Required:** `assessment_metrics` table. This is already in the proposal.
**Severity:** **P0 — SCIENTIFICALLY INVALID**

### Death Test 6: Injury Prediction Model
**Scenario:** Data scientist wants to train an injury model from 3 years of training data.
**Result:** **NO DATA.** No `domain_events`, no execution tracking (`program_session_exercises` has no completion data), no load history (`training_load` doesn't exist yet).
**Fix Required:** `domain_events`, `training_load`, execution columns on `program_session_exercises`.
**Severity:** **P0 — AI BLOCKER**

### Death Test 7: Coach Customization
**Scenario:** Coach Smith replaces 30% of AI exercises with his preferred alternatives. Wants AI to learn his preferences.
**Result:** **NO LEARNING.** No `coach_feedback` table. No `users` table to identify who Smith is. No `recommendation_log` to know what was originally recommended.
**Fix Required:** `coach_feedback`, `users`, `recommendation_log`.
**Severity:** **P1 — FEATURE BLOCKER**

### Death Test 8: New Sport = New Deficits
**Scenario:** System adds Swimming with 10 new assessment metrics. Need 10 new deficit definitions.
**Result:** **ENUM EXPLOSION.** `deficits` table grows by 10 rows. Then Combat Sports adds 8 more. Then Athletics adds 15 more. Deficits table becomes unmanageable.
**Fix Required:** Deprecate `deficits` table. Deficits are COMPUTED from metric → demand mapping.
**Severity:** **P1 — MAINTENANCE CRISIS**

### Death Test 9: AI Recommend + Coach Validate
**Scenario:** AI proposes exercises. Coach reviews and accepts/rejects/modifies.
**Result:** **No infrastructure for this workflow.** No `recommendation_log`, no `coach_feedback`, no user identity. The system has no concept of a "review step" between generation and prescription.
**Fix Required:** Recommendation lifecycle: `generated → reviewed → accepted → prescribed → executed`. Each state stored.
**Severity:** **P1 — WORKFLOW BLOCKER**

### Death Test 10: 50,000 Exercise Catalog
**Scenario:** Exercise catalog grows from 31 to 50,000.
**Result:** **exercise_sport_mapping at 2.5M rows.** Manual maintenance collapses. `exercise_physical_qualities` duplicates `exercise_demand_mapping` (both measure exercise → attribute relationships). 50K × 3 qualities = 150K rows in a table that should be deprecated in favor of `exercise_demand_mapping`.
**Fix Required:** Remove `exercise_sport_mapping` manual columns (specificity/transfer). Remove `exercise_physical_qualities` (replaced by `exercise_demand_mapping`). Single source of truth.
**Severity:** **P1 — DATA INCONSISTENCY**

---

## SURVIVAL SCORECARD

| Death Test | Survives? | Fix Scope |
|:----------:|:---------:|-----------|
| 1. Multi-Org | ❌ FAIL | New: organizations, teams, users, athlete_teams (4 tables) |
| 2. Multi-Sport | ❌ FAIL | New: athlete_teams table. Remove sport_id/role_id from athletes. |
| 3. Non-4-Week | ❌ FAIL | Remove CHECK constraint (1 line each) |
| 4. Variable Sessions | ❌ FAIL | Remove CHECK constraint (1 line) |
| 5. Force Plate | ⚠️ Partial | assessment_metrics table (already proposed, NOT yet implemented) |
| 6. Injury Prediction | ❌ FAIL | New: domain_events table. Add execution columns. |
| 7. Coach Custom | ❌ FAIL | New: coach_feedback, users, recommendation_log |
| 8. Deficit Explosion | ❌ FAIL | Deprecate deficits table. Compute at query time. |
| 9. AI Review Loop | ❌ FAIL | Workflow states on recommendation_log |
| 10. 50K Exercises | ⚠️ Partial | Remove exercise_sport_mapping. Deprecate exercise_physical_qualities. |

**PASS RATE: 1/10** (only Death Test 5 has partial fix already proposed)

---

## VERSION 2 — REDESIGNED ARCHITECTURE

### Design Principles
1. **Everything is multi-tenant** — organizations, teams, users, access control
2. **Everything is event-sourced** — every action recorded, AI training data accumulates
3. **Everything is computed** — deficits, specificity, and demand scores are query-time derivations, not stored values
4. **Everything is extensible** — metadata_json on every table
5. **AI is the primary consumer** — schema serves both query AND AI training

### V2 Core Entities

```
ORGANIZATIONAL LAYER
├── organizations (id, name, type, settings_json, metadata_json)
├── teams (id, org_id, sport_id, name, competition_level, metadata_json)
├── users (id, org_id, email, role_type, preferences_json, metadata_json)
├── team_assignments (user_id, team_id, coaching_role, start_date, end_date)

ATHLETE LAYER (redesigned)
├── athletes (id, first_name, last_name, dob, gender, metadata_json)
│   — REMOVED: sport_id, role_id (moved to athlete_teams)
├── athlete_teams (athlete_id, team_id, sport_id, role_id, start_date, end_date, is_primary BOOLEAN)
│   — Replaces: athletes.sport_id + athletes.role_id
│   — Enables: "John = Fast Bowler for Cricket XI + Forward for Soccer Club"

ONTOLOGY LAYER (stable — mostly unchanged)
├── movement_patterns (add: family_id, metadata_json)
├── physical_qualities (add: category_id, parent_id, metadata_json)
├── performance_demands (add: demand_type, metadata_json)
│   — KEPT: 1-quality-1-pattern model
│   — ADDED: demand_type ('Biomotor' | 'Sensory-Motor' | 'Metabolic' | 'Cognitive')
├── demand_prerequisites (demand_id, prereq_id, min_competency)
├── sport_demand_defaults (sport_id, demand_id, default_priority)
├── role_demand_priority (role_id, demand_id, priority, category)

EXERCISE LAYER (simplified)
├── exercises (keep, add: metadata_json)
├── exercise_demand_mapping (exercise_id, demand_id, relevance_score, metadata_json)
│   — PRIMARY exercise attribute table. Replaces exercise_physical_qualities.
├── exercise_contraindications (exercise_id, condition_json, severity)
├── exercise_equivalencies (source_id, target_id, score, reason)
├── exercise_embeddings (exercise_id, model_name, vector(384))
│   — REMOVED: exercise_sport_mapping (specificity/transfer → computed from demand overlap)
│   — DEPRECATED: exercise_physical_qualities (replaced by exercise_demand_mapping)

ASSESSMENT LAYER (redesigned)
├── assessments (add: sport_ids[], protocol_json, metadata_json)
├── assessment_metrics (assessment_id, name, unit, higher_is_better)
│   — NEW: parsed outputs from test protocols
├── metric_demand_mapping (metric_id, demand_id, weight)
│   — CORRECT: maps parsed metrics to demands. Replaces assessment_demand_mapping.
├── assessment_results (athlete_id, assessment_id, test_date, device_info, metadata_json)
│   — KEPT: raw test instance
│   — REMOVED: score column (metrics carry scores now)
├── athlete_metric_history (athlete_id, metric_id, value, result_id, date)
│   — NEW: historical metric values for trending
├── benchmarks (assessment_id, metric_id, classification, min, max)
│   — ADDED: metric_id FK

PROGRAM LAYER (redesigned)
├── season_phases (id, team_id, name, type, start_date, end_date)
├── session_templates (id, name, phase_type, slot_count, slot_structure_json)
├── programs (id, athlete_team_id, phase_id, start_date, end_date, metadata_json)
│   — REMOVED: sessions_per_week CHECK, week_number CHECK
│   — ADDED: athlete_team_id (which sport context), phase_id (seasonal context)
├── program_weeks (id, program_id, week_number, focus, metadata_json)
│   — REMOVED: week_number BETWEEN 1 AND 4 CHECK
├── program_sessions (id, week_id, session_number, metadata_json)
│   — REMOVED: session_number BETWEEN 1 AND 4 CHECK
├── program_session_exercises (id, session_id, display_order, exercise_id,
│       sets, reps, intensity, rest_seconds,
│       actual_sets, actual_reps, actual_intensity, actual_rpe,
│       completed, completion_notes, metadata_json)
│   — ADDED: execution columns (actual_*) alongside prescription columns

INJURY LAYER
├── injury_types (id, name, body_part, category)
├── injury_incidents (athlete_id, injury_type_id, date, severity, mechanism, metadata_json)
├── injury_risk_demand_mapping (injury_type_id, demand_id, relationship, weight)

LOAD LAYER
├── training_load (id, athlete_id, date, source, load_type, value, metadata_json)
│   — REMOVED: load_type CHECK constraint (JSONB for arbitrary load types)

EVENT LAYER (NEW — critical for survival)
├── domain_events (id, aggregate_type, aggregate_id, event_type,
│       event_data JSONB, occurred_at, recorded_at, org_id)
│   — IMMUTABLE: append-only. Never UPDATE, never DELETE.
│   — Fields: aggregate = 'athlete' | 'program' | 'assessment' | 'injury'
│   — Examples: 'athlete.created', 'program.generated', 'session.completed'

AI LEARNING LAYER (NEW — critical for survival)
├── recommendation_log (id, athlete_id, session_context JSONB,
│       demand_scores JSONB, proposed_exercises JSONB, selected_exercises JSONB,
│       model_version, constraint_results JSONB, coach_overridden BOOLEAN,
│       generation_ms, created_at)
│   — FULL SNAPSHOT: every recommendation decision recorded
├── coach_feedback (id, athlete_id, program_id, session_exercise_id,
│       coach_user_id, action,
│       original_exercise_id, replacement_exercise_id, reason, metadata_json)
│   — RL REWARD SIGNAL: what coach accepted, rejected, replaced, why
├── entity_graph_edges (source_type, source_id, target_type, target_id,
│       relationship_type, weight, metadata_json)
│   — KNOWLEDGE GRAPH: seeded from junction tables, enables AI reasoning

VECTOR/EMBEDDING LAYER
├── exercise_embeddings (exercise_id, model_name, vector(384), created_at)
├── demand_embeddings (demand_id, model_name, vector(384), created_at)
├── athlete_snapshot_vectors (athlete_id, snapshot_date, vector float4[], metadata_json)
├── model_metadata (id, name, type, version, active, parameters_json, metrics_json)

METADATA LAYER
├── sports (keep, add: metadata_json)
├── roles (keep, add: metadata_json)
├── equipment (keep, add: metadata_json)
├── tags (keep, add: metadata_json)
├── training_methods (keep, add: metadata_json)
├── muscles (keep, add: metadata_json)
```

---

## V2 KEY DESIGN DECISIONS

### Decision 1: Athlete → Team M:N replaces single sport/role

**Current:** `athletes(sport_id, role_id)` — single value columns
**V2:** `athlete_teams(athlete_id, team_id, sport_id, role_id, start_date, end_date, is_primary)`

**Why:** Athletes play multiple sports and change roles over time. This is the most common edge case in real athlete development (off-season sport = different demands than primary sport).

**Migration:** 
1. Create `athlete_teams` table
2. INSERT from existing athletes: `(athlete.id, default_team, athlete.sport_id, athlete.role_id, athlete.created_at, NULL, TRUE)`
3. Create `athletes` migration: remove `sport_id`, `role_id` FK constraints (keep columns for backward compat, set nullable)

### Decision 2: Deficits are computed, not stored

**Current:** `deficits` table with hardcoded rows
**V2:** `compute_athlete_deficits(athlete_id) → TABLE(demand_id, deficit_score, severity)`

**Why:** The deficit score for a demand changes every time a new assessment is recorded. Storing it means stale data. Computing it means always-current data.

**Performance concern:** Computing deficits for 100K athletes on demand could be expensive.
**Solution:** Materialized view `athlete_current_deficits` refreshed on assessment completion (via domain event trigger).

### Decision 3: Exercise-Sport specificity is computed, not stored

**Current:** `exercise_sport_mapping.specificity_rating` and `transfer_index` — manual columns
**V2:** `sport_specificity = Σ(exercise.demand_weights × sport.demand_priorities) / max_possible`

**Why:** Manual maintenance of 250K+ rows with 50 sports × 5000 exercises is impossible. Computation ensures consistency when new demands are added.

**Implementation:** PostgreSQL function + materialized view, refreshed when `exercise_demand_mapping` or `sport_demand_defaults` changes.

### Decision 4: Events are append-only, never modified

**Current:** No event system
**V2:** `domain_events` — immutable append-only log

**Why:** Injury prediction requires a sequence of events. AI training requires before/after snapshots. Audit requires what happened. All of these need IMMUTABLE history.

**Anti-pattern warning:** Do NOT add "UPDATE domain_events SET..." anywhere. Events are truths. Truths don't change.

### Decision 5: Execution columns alongside prescription columns

**Current:** `program_session_exercises(sets, reps, intensity, rest_seconds)` — all prescription
**V2:** Add `actual_sets, actual_reps, actual_intensity, actual_rpe, completed`

**Why:** ACWR computed from prescribed load ≠ ACWR computed from actual load. Injury research consistently shows actual load predicts injury better than prescribed load.

**Design choice:** Same row, not separate table. This avoids JOIN overhead and makes the prescription→execution gap obvious in a single query.

---

## PERFORMANCE RISKS

| Risk | Impact | Mitigation |
|------|--------|------------|
| `compute_athlete_deficits` per-request | 100K athletes × weekly = 100K function calls | Materialized view + event-driven refresh |
| `domain_events` table growth | 100K athletes × 50 events/year × 10 years = 50M rows | Partition by year. Archive >3 year data to cold storage. |
| `athlete_metric_history` growth | 100K athletes × 50 metrics × 52 weeks = 260M rows in 10 years | Partition by athlete_id hash (16 partitions). 16M/partition — acceptable. |
| Embedding storage | 5K exercises × 384-dim = ~15MB. Negligible. | No action needed. |
| `recommendation_log` growth | 100K athletes × 52 programs = 5.2M rows/year × 10 = 52M | Compress JSONB. Archive >3 years. Partition by year. |
| Graph edge traversal | `entity_graph_edges` could have 500K+ edges | Index on (source_type, source_id) and (target_type, target_id). Graph queries should use WHERE + LIMIT, not full traversal. |
| ACWR calculation over N years | If loading ALL training_load for calculation | Window function with 28-day sliding window. Index on (athlete_id, date DESC). |

**Verdict:** All performance risks are manageable with standard PostgreSQL techniques (indexing, partitioning, materialized views, archiving). No need for specialized infrastructure.

---

## MIGRATION PLAN (12 Weeks)

### Week 1-2: Multi-Tenancy (P0)
```
CREATE TABLE organizations, teams, users, athlete_teams, team_assignments
ALTER TABLE athletes: set sport_id/role_id nullable
Migrate existing data to athlete_teams
Add organization_id FK to all existing tables
```

### Week 3-4: Event Sourcing (P0)
```
CREATE TABLE domain_events
Add event emission to all service endpoints
Backfill: create events for existing data (assessment_results, programs)
```

### Week 5-6: Ontology (P0)
```
CREATE TABLE performance_demands (18 rows)
CREATE TABLE exercise_demand_mapping (migrate from exercise → pattern + quality)
CREATE TABLE demand_prerequisites
ALTER TABLE movement_patterns: add family_id, metadata_json
ALTER TABLE physical_qualities: add category_id, parent_id, metadata_json
```

### Week 7-8: Assessment Redesign (P0)
```
CREATE TABLE assessment_metrics
CREATE TABLE metric_demand_mapping
ALTER TABLE assessment_results: remove score column? (defer — keep for backward compat)
ALTER TABLE benchmarks: add metric_id
CREATE OR REPLACE FUNCTION compute_athlete_deficits()
DEPRECATE TABLE deficits (is_active=FALSE)
```

### Week 9-10: Program Redesign (P1)
```
ALTER TABLE programs: REMOVE CHECK constraints, ADD phase_id, athlete_team_id
ALTER TABLE program_weeks: REMOVE CHECK constraints
ALTER TABLE program_sessions: REMOVE CHECK constraints
ALTER TABLE program_session_exercises: ADD execution columns
CREATE TABLE season_phases
CREATE TABLE session_templates
ADD metadata_json to all program tables
```

### Week 11-12: Exercise Cleanup (P1)
```
CREATE OR REPLACE VIEW exercise_sport_specificity (computed from demand overlap)
DEPRECATE exercise_sport_mapping.specificity_rating (set nullable)
DEPRECATE exercise_sport_mapping.transfer_index (set nullable)
ADD metadata_json to exercises
```

### Phase 2 (Month 3-4): AI Infrastructure
```
CREATE TABLE recommendation_log
CREATE TABLE coach_feedback
CREATE TABLE entity_graph_edges
CREATE TABLE exercise_embeddings
```

### Phase 3 (Month 5-6): Load + Injury
```
CREATE TABLE training_load (with JSONB load_type)
CREATE TABLE injury_types, injury_incidents
CREATE TABLE injury_risk_demand_mapping
```

---

## TECHNICAL DEBT RISKS

| Debt | Severity | Cost to Fix Now | Cost to Fix Later | Decision |
|------|----------|:----------------:|:------------------:|----------|
| NO multi-tenant | **P0** | 1 week (add 4 tables) | 4 weeks (partition ALL existing data) | **Fix now** |
| NO event sourcing | **P0** | 3 days (add 1 table + service hooks) | 3 months (retrospective event reconstruction) | **Fix now** |
| Deficits as table | P1 | 2 days (deprecate + compute function) | 2 weeks (migrate 50+ deficit rows + all dependents) | **Fix now** |
| Rigid program CHECK | P1 | 2 hours (ALTER TABLE DROP CHECK) | 1 week (re-import all programs that violated constraints) | **Fix now** |
| No execution tracking | P1 | 2 days (add 6 columns) | 2 months (parallel execution table + JOIN migration) | **Fix now** |
| exercise_sport_mapping manual | P2 | 3 days (view + deprecation) | 3 weeks (data cleanup + inconsistency resolution) | Fix in Phase 2 |
| No metadata_json | P2 | 1 day per table (ALTER ADD COLUMN) | Every migration adds a real column instead of JSONB | Fix in Phase 1-2 |
| exercise_physical_qualities | P2 | 2 days (deprecate, point to exercise_demand_mapping) | Dual maintenance forever | Fix in Phase 2 |

**The Compounding Debt Rule:** Every table WITHOUT `metadata_json` will require a schema migration in the next 12 months. With the V2 design, 15 core tables need this. That's 15 future migrations avoided.

---

## AI-READINESS SCORE

| Capability | Current | V2 | Delta |
|-----------|:-------:|:--:|:-----:|
| Feature vectors for ML | 20% | 90% | +70% |
| Knowledge graph for inference | 10% | 85% | +75% |
| RL training data (coach feedback) | 0% | 95% | +95% |
| Embedding storage | 0% | 95% | +95% |
| Time-series for prediction | 10% | 80% | +70% |
| Event chain for causal analysis | 0% | 90% | +90% |
| A/B testing infrastructure | 0% | 60% | +60% |
| Model versioning | 0% | 70% | +70% |
| **SCORE** | **5%** | **83%** | **+78%** |

The current architecture scores 5% on AI readiness. V2 scores 83%. The gap is entirely in event sourcing, feedback collection, and embedding storage — all additive infrastructure, not core ontology changes.

---

## FINAL VERDICT

### "Can this architecture survive 10 years of feature additions without major redesign?"

**No. Not in its current form.**

The Performance Demand ontology (qualities → patterns → demands → exercises) is correct and will survive 10+ years. This is the one thing that does not need redesign.

But the APPLICATION ARCHITECTURE surrounding it will fail within 2-3 years because:

1. **No multi-tenancy** → Cannot serve >1 organization (Year 1 death)
2. **No event sourcing** → AI has no training data, audit has no trail (Year 2 death)
3. **Single-sport athlete model** → Multi-sport athletes unsupported (Year 1 death)
4. **Stored deficits** → Enum explosion with new sports (Year 2 death)
5. **No program constraints** → Non-4-week blocks crash (immediate)
6. **No execution tracking** → ACWR is fiction (Year 2 death)
7. **No coach identity** → No personalization, no learning (Year 2 death)

**The V2 redesign fixes all 7 gaps with:**
- +11 new tables (organizations, teams, athlete_teams, users, domain_events)
- +15 ALTER TABLE ADD COLUMN (metadata_json + constraint removals)
- +3 DEPRECATION markers (deficits, exercise_physical_qualities, exercise_sport_mapping manual columns)
- +2 computed functions (deficit computation, sport specificity computation)
- +5 AI infrastructure tables (recommendation_log, coach_feedback, embeddings, entity_graph_edges, model_metadata)

**Total V2 scope:** ~11 new tables + ~15 column additions + ~3 deprecations + ~2 functions + ~5 AI tables = manageable in 12 weeks.

**The core insight:** The ontology is built on ROCK. The application layer is built on SAND. Fix the foundation before adding floors.
