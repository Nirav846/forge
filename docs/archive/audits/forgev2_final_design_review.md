# FORGE V2: Final Architecture Validation & Production Readiness Review

**Review Type:** Principal Architect / Domain-Driven Design / Sports Science / Production Readiness
**Date:** 2026-06-17
**Assumptions:** All 11 previously identified fixes are implemented (ACWR centralization, CSP planner, composite objectives, CompetitionCalendarService, SessionSequencingService, configurable pipeline, TrainingAge domain, per-quality fatigue, PreSessionGate, demand-aware progression)
**Scope:** Only risks that survive the revised design — no repetition of prior findings

---

## Executive Summary

Even after all 11 previously identified architectural fixes, **FORGE V2 has 8 remaining critical architectural risks** that span sports science theory, constraint solver scale, data model completeness, operational viability, and AI readiness.

The architecture is **sound for Phase 1 (execution tracking) and Phase 2 (progression)** but **critically incomplete for Phase 3 (intelligent planning)** . The system models deficits and fatigue well but does not model **adaptation**, **periodization**, or **individual response** — the three pillars of evidence-based program design.

**Production Readiness Score: 52/100**
**Verdict: BUILD PILOT ONLY** — cannot ship to full production without addressing periodization modeling, constraint solver architecture, and recovery/readiness completeness.

---

## 1. Sports Science Validation

### 1.1 Periodization Support

**Claim:** The architecture supports periodization through CompetitionCalendarService + SessionSequencingService + CSP planner.

**Reality:** The system supports **session-level planning** but not **block-level periodization**. These are fundamentally different concepts.

#### Gap Analysis

| Periodization Model | Supported? | Why Not |
|--------------------|-----------|---------|
| Linear periodization | NO | No concept of mesocycle blocks with progressive overload across weeks |
| Undulating periodization | PARTIAL | Daily/weekly undulation possible via CSP but no block structure |
| Block periodization | NO | No concept of concentrated loading for specific adaptations |
| Conjugate system | NO | No simultaneous development of opposing qualities with rotation |
| Tactical periodization | NO | No game-model-driven planning with weekly rhythm |

**Root Cause:** The architecture has no `Mesocycle` or `Block` aggregate. The `CompetitionCalendarService` knows about competition dates but doesn't decompose time into preparation phases (general → specific → competition → transition). The `SessionSequencingService` sequences sessions within a microcycle but has no concept of **loading trends across mesocycles**.

**What would need to be designed:**

```
PeriodizationBlock {
  id: UUID
  athlete_id: FK
  block_type: ENUM (GPP, SPP, PreCompetition, Competition, Transition, Deload, Taper)
  start_date: DATE
  end_date: DATE
  primary_adaptation: FK -> physical_qualities
  secondary_adaptations: FK[] -> physical_qualities
  loading_trajectory: JSONB {
    weekly_volume_trend: LINEAR | STEP | UNDULATING | DECAY
    weekly_intensity_trend: LINEAR | STEP | UNDULATING | DECAY
    density_trend: INCREASING | DECREASING | MAINTAIN
  }
  parent_mesocycle_id: FK (self-referential for nesting)
  competition_id: FK (optional, links to competition calendar)
}

Mesocycle {
  id: UUID
  athlete_id: FK
  phase: ENUM (PREPARATORY, COMPETITIVE, TRANSITION)
  sub_phase: ENUM (GENERAL, SPECIFIC, PRE_COMP, COMP, DELOAD, TRANSITION)
  duration_weeks: INT (3-6 typical)
  blocks: PeriodizationBlock[]
  loading_progression: JSONB (week-by-week volume/intensity targets)
}
```

Without these, periodization is reduced to **week-level planning** — every 4-week block looks like Week 1-4 of V1's Base/Accumulation/Peak/Deload regardless of the annual plan context.

### 1.2 Adaptation Modeling

**Critical Finding:** The system models **deficits** but not **adaptation**. These are distinct.

Current flow:
```
Assessment → Deficit Detection → Demand Scoring → Exercise Selection → Program Output
```

What's missing:
```
Program Output → Training Stimulus → [Supercompensation] → Adaptation → New Assessment
```

The architecture has **no model of how training causes adaptation**. It can say "this athlete has a power deficit, prescribe power exercises" but cannot say:
- "This athlete typically needs 3 weeks of power work to see a 5% CMJ improvement"
- "This athlete's power adaptation is slowing down (diminishing returns), time to shift focus"
- "This athlete responded well to high-volume power work but poorly to high-intensity"

**Consequences:**
1. **No individualization of dose-response:** Every athlete with a power deficit gets the same intensity/volume prescription for power demands, adjusted only by training age level
2. **No adaptation rate tracking:** The system doesn't learn how quickly an athlete adapts to different training stimuli
3. **No residual effects modeling:** After a strength block, strength decays over time — the system doesn't model this
4. **No training history accounting:** An athlete who did 8 weeks of power work already has a different response curve than one starting fresh

**Design Required:**

```
AdaptationProfile {
  athlete_id: FK (PK)
  quality_id: FK -> physical_qualities
  adaptation_rate: DECIMAL (weeks per 1% improvement, learned from history)
  responsiveness_class: ENUM (HIGH_RESPONDER, NORMAL, LOW_RESPONDER)
  decay_rate: DECIMAL (weeks per 1% decay after training cessation)
  last_training_block: DATE
  current_adaptation_status: ENUM (ACCUMULATING, INTENSIFYING, REALIZING, DELOADING, DETRAINING)
  training_history: JSONB[] (array of {block_type, dates, volume, intensity, response_metric, response_delta})
}

StimulusResponseFunction {
  quality_id: FK
  athlete_id: FK (NULL for population baseline)
  volume_response_slope: DECIMAL
  intensity_response_slope: DECIMAL
  frequency_response_slope: DECIMAL
  interaction_terms: JSONB (volume × intensity interaction)
  r_squared: DECIMAL (model fit quality)
  last_updated: TIMESTAMPTZ
}
```

Without adaptation modeling, the system is **reactive** (responds to current deficits) rather than **prescriptive** (plans a training trajectory). This is the single biggest sports science gap in the revised architecture.

### 1.3 Recovery Modeling

**Claim:** Per-quality fatigue model exists.

**Reality:** Fatigue is modeled as a single `fatigue_score` across all qualities, not per-quality. Even with per-quality fatigue, recovery is under-modeled.

#### Recovery Modalities Not Modeled

| Modality | Impact | Modeled? |
|----------|--------|----------|
| Sleep quality | ±20-30% training tolerance | NO — `sleep_quality` column exists in athlete_state_snapshots but is not integrated into any planning decision |
| Travel fatigue | ±10-15% performance, increased injury risk | NO |
| Jet lag | ±5-10% per timezone crossed | NO |
| Environmental stress (heat, altitude) | ±10-20% training tolerance | NO |
| Illness/subclinical infection | ±30-50% training tolerance | NO |
| Psychological stress (academic, personal) | ±15-25% training tolerance | NO |
| Menstrual cycle phase | ±5-15% performance, ±20% injury risk | NO |
| Nutrition status (glycogen, hydration) | ±10-30% training capacity | NO |

**Current Integration:** `athlete_state_snapshots.readiness_score` is a weighted combo of recovery, fatigue, and injury risk. But none of the above modalities feed into those components. The `sleep_quality` column exists but nothing reads it.

**Risk:** A coach programs a high-intensity session for an athlete who:
- Flew 6 hours yesterday (travel fatigue)
- Had 4 hours of sleep (recovery deficit)
- Is in a high-stress exam period
- Is at altitude camp

The system will see `readiness_score = 65` (moderate) and proceed, but the combined effect of these stressors makes the session dangerous.

**Design Required:**

```
RecoveryContext {
  id: UUID
  athlete_id: FK
  snapshot_date: DATE
  sleep_quality: INT (1-10)
  sleep_hours: DECIMAL(4,1)
  travel_fatigue_score: INT (0-100) — computed from flight hours × timezones in last 72h
  environmental_stress_score: INT (0-100) — heat/humidity/altitude deviation from baseline
  illness_flag: BOOLEAN
  illness_severity: INT (1-5)
  psychological_stress_score: INT (0-100)
  menstrual_cycle_phase: ENUM (NULL for males)
  nutrition_readiness: INT (0-100) — subjective or app-integrated
  composite_recovery_score: DECIMAL(5,2) — weighted aggregation
  recovery_modifiers: JSONB {
    modality_breakdown: {...},
    z_scores: {...},
    flags: [...]
  }
}
```

This context should be computed daily and fed into the PreSessionGate as a threshold check: if `composite_recovery_score < 40`, automatically suggest a recovery/low-intensity session regardless of the training plan.

### 1.4 Junk Volume and Training Density

**Missing Concept:** The architecture has no guard against **junk volume** — training that contributes to fatigue without stimulating adaptation.

A CSP can fill a session with exercises that satisfy all constraints (demand coverage, equipment, fatigue limits) but produce a session that is:
- Too long (exceeds ideal session duration)
- Too dense (insufficient recovery between sets/exercises)
- Poorly ordered (fatiguing exercise before skill exercise)
- Redundant (3 exercises targeting the same demand with diminishing returns)

**Design Required:**

```
SessionDensityConstraint {
  max_exercises_per_session: INT (per training age level)
  max_volume_per_session: INT (total sets × reps, per athlete level)
  min_rest_between_demand_categories: INT (minutes)
  quality_diversity_minimum: INT (minimum distinct quality categories per session)
  diminishing_returns_threshold: INT (max exercises per demand per session)
}
```

A `SessionQualityGate` should sit after the CSP output and before program finalization, checking:
- Does this session pass the density gate?
- Are exercises optimally ordered (skill/power before strength before conditioning)?
- No redundant exercises for the same demand beyond the diminishing returns threshold?

---

## 2. Constraint Solver Validation

### 2.1 CSP Scope Boundaries

**Claim:** CSP-based objective planner exists.

**Question:** Can CSP alone handle the full problem space?

**Analysis of constraint types:**

| Constraint Type | CSP Suitable? | Notes |
|----------------|--------------|-------|
| Exercise → demand coverage | YES | Binary: this exercise covers this demand |
| Equipment availability | YES | Binary: equipment available or not |
| Fatigue per quality | YES | Finite domain: fatigue budget |
| Movement pattern diversity | YES | Finite domain: patterns per session |
| Competition embargo (pre-competition loading) | YES | Temporal constraint |
| **Objective planning** (which demands to prioritize this cycle) | **PARTIAL** | CSP can select objectives under constraints, but optimization quality depends on objective function |
| **Exercise sequencing** (order within session) | **NO - poor fit** | Sequencing is a scheduling problem, not a constraint satisfaction problem. CSP can enforce ordering constraints but can't optimize rest periods, fatigue accumulation, or potentiating effects |
| **Exposure planning** (distribute demand coverage across microcycle) | **PARTIAL** | CSP can enforce "each demand appears N times per week" but cannot optimize "which day is optimal for which demand" |
| **Progressive overload** (increase over mesocycle) | **NO** | CSP has no concept of temporal trends — it solves for a snapshot, not a trajectory |

**Conclusion:** CSP is appropriate for **single-session exercise selection** but should NOT be the sole solver for:
1. **Microcycle planning** — use CSP for per-session, then a scheduler for distribution across days
2. **Mesocycle progression** — use trend-based rules (separate from CSP)
3. **Exercise sequencing** — use a dedicated sequencing heuristic (potentiation complexes, fatigue management)

### 2.2 Scale Analysis

**Worst-case constraint problem dimension:**

For a single athlete, single microcycle (6 sessions):

```
Variables:
  Exercises per session:   6-10 × 6 sessions = 36-60 exercise slots
  Sets per exercise:       2-5 per exercise = 80-300 set variables
  Intensity per set:       continuous (can discretize to 20 levels)
  Rest per set:            continuous (can discretize to 10 levels)

Constraints (est.):
  Per-session constraints:     10-15 types × 6 sessions = 60-90
  Cross-session constraints:   5-10 types  = 5-10
  Fatigue constraints:         per-quality × 6-8 qualities = 48-64
  Demand coverage:             per-demand × 18 demands = 18
  Diversity constraints:       5-8
  Competition constraints:     2-5 (if in competitive period)

Total variables:        ~100-360
Total constraints:      ~140-200
```

**At scale:**

| Athletes | Variables (total) | Constraints (total) | Est. Solver Time (per cycle) | Notes |
|----------|------------------|--------------------|------------------------------|-------|
| 10 | 1K-3.6K | 1.4K-2K | < 1s | Trivial for any approach |
| 100 | 10K-36K | 14K-20K | 1-5s | CSP fine with pruning |
| 1,000 | 100K-360K | 140K-200K | 30s-5min | CSP starts struggling; need CP-SAT |
| 10,000 | 1M-3.6M | 1.4M-2M | 5min-1hr | CSP infeasible; need decomposed approach |
| 50,000 | 5M-18M | 7M-10M | hours | CSP not viable |

**Key insight:** At 10,000+ athletes, a single CSP solver for the full problem space is **computationally infeasible** for daily regeneration. The architecture must decompose the problem.

### 2.3 Recommended Solver Architecture

**Hybrid approach: Constraint Satisfaction + Optimization + Heuristics**

```
Layer 1: Macro Periodization (heuristic + rules)
  - What phase of the season?
  - Which adaptation blocks?
  - Weekly volume/intensity targets
  - Solver: Rule engine (drools-like or simple if-then)
  - Frequency: Monthly or pre-season

Layer 2: Mesocycle Planning (CP-SAT)
  - Weekly demand exposure targets
  - Quality distribution across weeks
  - Progression trajectory
  - Solver: OR-Tools CP-SAT
  - Frequency: Every 4-6 weeks

Layer 3: Microcycle Planning (CSP + optimizer)
  - Exercise selection per session
  - Within-week fatigue management
  - Movement pattern rotation
  - Solver: Custom CSP with optimization objective
  - Frequency: Weekly

Layer 4: Session Assembly (heuristic)
  - Exercise ordering within session
  - Set/reps/intensity calculation
  - Rest period optimization
  - Solver: Heuristic (no search needed)
  - Frequency: On demand (program generation)
```

**Recommendation:**
- Keep CSP for Layers 3 and 4
- Add CP-SAT (Google OR-Tools) for Layer 2
- Add Rule Engine for Layer 1
- Implement caching at Layers 1 and 2 (they change infrequently)
- Layer 3 and 4 can run per-athlete in parallel (embarrassingly parallel up to 10K workers)

---

## 3. Data Model Validation

### 3.1 Periodization & Block Tables

**Missing tables** (do not exist in any migration):

| Table | Purpose | Example Columns |
|-------|---------|-----------------|
| `periodization_templates` | Pre-built periodization models (linear, block, conjugate) | id, name, model_type, structure JSONB, sport_id, level |
| `mesocycles` | High-level training blocks | id, athlete_id, phase, sub_phase, start_date, end_date, primary_quality, secondary_qualities[], loading_trajectory JSONB |
| `mesocycle_weeks` | Week-by-week targets within mesocycle | id, mesocycle_id, week_number, volume_target, intensity_target, density_target, focus_quality |
| `adaptation_profiles` | Athlete-specific response to training stimuli | id, athlete_id, quality_id, adaptation_rate, decay_rate, responsiveness, last_assessment_id |
| `competition_phases` | Season structure | id, sport_id, phase_name, phase_type (PRE_SEASON, IN_SEASON, OFF_SEASON, TRANSITION), default_duration_weeks, loading_template |
| `recovery_contexts` | Daily multi-modal recovery assessment | id, athlete_id, date, sleep_score, travel_score, environmental_score, illness_flag, stress_score, composite_score, readiness_override |

### 3.2 Configuration Explosion Forecast

**Growth estimation:**

```
Tables at risk of exponential growth:

role_demand_priority
  Current: 5 roles × 18 demands = 90 rows (Cricket only)
  10 sports × 5 roles × 18 demands = 900 rows ✓
  50 sports × 7 roles × 18 demands = 6,300 rows ✓ (manageable)
  100 sports × 10 roles × 18 demands = 18,000 rows ⚠️ (needs UI)

demand_exposure_targets
  Per (sport, role, quality_category, phase, training_age_bracket)
  10 sports × 5 roles × 5 qualities × 4 phases × 3 age brackets = 3,000 rows ✓
  50 sports × 7 roles × 7 qualities × 4 phases × 3 age brackets = 29,400 rows ⚠️
  100 sports × 10 roles × 8 qualities × 4 phases × 4 age brackets = 128,000 rows 🔴

exercise_demand_mapping
  Per (exercise, demand, relevance_score) - grows linearly with exercise library
  500 exercises × 18 demands × 0.3 density = 2,700 rows ✓
  2,000 exercises × 18 demands × 0.3 density = 10,800 rows ✓
  10,000 exercises × 30 demands × 0.3 density = 90,000 rows ⚠️

movement_pattern_diversity_rules
  Per (sport, role, phase, pattern, min_per_week, max_per_week)
  10 sports × 5 roles × 4 phases × 8 patterns = 1,600 ✓
  50 sports × 7 roles × 4 phases × 8 patterns = 11,200 ⚠️
  100 sports × 10 roles × 4 phases × 10 patterns = 40,000 ⚠️
```

**Critical threshold:** At ~50 sports, `demand_exposure_targets` becomes unmaintainable without a configuration UI. At ~100 sports, it requires bulk import/export and versioning.

**Solution required:**
1. **Hierarchical configuration inheritance:** Sport → Role → Phase → Athlete-specific overrides. Not all 128K rows need to be manually entered; 80% can inherit from sport defaults.
2. **Configuration templates:** Pre-built "Soccer General Preparation" template with sensible defaults that coaches tune.
3. **Configuration audit trail:** Every weight change logged with who changed it, when, and why.
4. **Bulk configuration API:** CSV/JSON import for setting up new sports.
5. **Auto-suggestion of defaults:** For new sports, inherit from most similar existing sport based on movement pattern profile.

### 3.3 Reproducibility Strategy

**Can a coach regenerate a program from 6 months ago and get the exact same result?**

**Currently: NO.** Here's why:

| Dependency | Versioned? | Solution |
|-----------|-----------|----------|
| demand_scoring_engine.py | NO — code changes break reproducibility | Add `score_engine_version` to recommendation_log |
| role_demand_priority weights | NO — can be edited anytime | Add `valid_from`/`valid_until` to all config tables |
| exercise_demand_mapping | NO — mapping can change | Same as above |
| CSP solver parameters | NO — solver algorithm can change | Add `solver_config_snapshot` JSONB to recommendation_log |
| Assessment metric conversion formulas | NO — conversion logic can change | Add `conversion_version` to assessment_metrics |
| Progression rules | NO — rules can change | Add `progression_rule_version` to programs |
| Seed / random seed | N/A — current system is deterministic | If CSP uses randomness for tiebreaking, seed must be stored |

**Design Required:**

```sql
-- Config snapshot table for full reproducibility
CREATE TABLE config_snapshots (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  snapshot_type VARCHAR(50) NOT NULL, -- 'full', 'demand_weights', 'solver_params', 'progression'
  snapshot_data JSONB NOT NULL, -- full dump of all config at point in time
  valid_from TIMESTAMPTZ NOT NULL,
  valid_until TIMESTAMPTZ,
  trigger_event_id BIGINT REFERENCES domain_events(id),
  checksum VARCHAR(64), -- SHA-256 of snapshot_data for verification
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Add to recommendation_log
ALTER TABLE recommendation_log ADD COLUMN config_snapshot_id BIGINT REFERENCES config_snapshots(id);
ALTER TABLE recommendation_log ADD COLUMN solver_seed INT;
ALTER TABLE recommendation_log ADD COLUMN recompute_checksum VARCHAR(64); -- run engine with same inputs, verify output matches
```

**Reproducibility Protocol:**
1. Every configuration change creates a new `config_snapshot` with `valid_from` = now
2. Recommendation generation stores the `config_snapshot_id` active at time of generation
3. Repro: load config_snapshot + original assessment data + solver_seed → deterministic output
4. Verification: compare generated output checksum to stored `recompute_checksum`

---

## 4. Domain-Driven Design Review

### 4.1 Bounded Context Audit (Post-Revise)

| Context | Responsibilities | Status |
|---------|-----------------|--------|
| Assessments | Metric extraction, deficit computation, trend analysis | ✓ CLEAN |
| Athlete State | Readiness, fatigue, recovery, ACWR, injury risk aggregation | ⚠️ OVERLOADED — mixes state tracking with readiness computation |
| Training Load | Load recording, ACWR calculation, load type classification | ✓ CLEAN |
| Injury Risk | Risk profiling, factor decomposition, intervention suggestion | ✓ CLEAN |
| Demand Modeling | Demand scoring, deficit mapping, role-weighted prioritization | ⚠️ OVERLOADED — mixes ontology management with scoring |
| Program Generation | CSP planning, exercise selection, session sequencing | ⚠️ BLOATED — handles 4 distinct concerns |
| Progression | Volume/intensity progression, adaptation tracking | ✓ CLEAN (small) |
| Execution Tracking | Session completion, RPE capture, load recording | ✓ CLEAN |

### 4.2 Missing Bounded Contexts

**1. Competition Management Context**
```
Aggregates:
  CompetitionCalendar { id, athlete_id, season_id, events[] }
  Season { id, sport_id, name, start_date, end_date, phases[] }
  CompetitionPhase { id, season_id, phase_type, start, end, loading_strategy }

Services:
  CompetitionCalendarService (assumed exists per prior fixes)
  SeasonPlanner
  PhasePeriodizationService

Events:
  CompetitionPhaseStarted
  CompetitionPhaseEnded
  CompetitionEventLogged
```

**2. Recovery Management Context**
```
Aggregates:
  RecoveryContext { id, athlete_id, date, modalities{} , composite_score }
  SleepLog { id, athlete_id, date, duration, quality, hrv }
  WellnessEntry { id, athlete_id, date, stress, soreness, fatigue, mood }

Services:
  RecoveryComputationService
  SleepAnalysisService
  TravelFatigueEstimator

Events:
  RecoveryContextUpdated
  SleepQualityAlert (when < 6h or poor quality)
  TravelFatigueDetected
```

**3. Coaching Workflow Context**
```
Aggregates:
  CoachingSession { id, coach_id, athlete_id, date, intent, review_notes }
  CoachDecision { id, coaching_session_id, decision_type (APPROVE | MODIFY | REJECT | OVERRIDE), before_snapshot, after_snapshot }

Services:
  CoachingWorkflowService
  CoachFeedbackIngestionService
  CoachIntentCaptureService

Events:
  CoachDecisionLogged
  ProgramModifiedByCoach
  CoachIntentCaptured
```

**4. Rehabilitation Context** (distinct from general programming)
```
Aggregates:
  RehabProtocol { id, athlete_id, injury_type, phase (ACUTE | SUB_ACUTE | STRENGTHENING | RTS), exercises[] }
  RTSGate { id, rehab_protocol_id, criteria[], passed BOOLEAN }

Services:
  RehabProtocolService
  RTSAssessmentService

Events:
  RehabPhaseTransitioned
  RTSCriteriaPassed
  ReturnedToTraining
```

### 4.3 Incorrectly Merged Contexts

**Athlete State** currently merges:
1. Acute readiness (readiness_score)
2. Chronic fatigue (fatigue_score, ACWR_trend)
3. Injury risk (injury_risk_score)
4. Recovery modalities (sleep_quality — field exists but unused)

These should be **separate sub-domains** within a bounded context or split:
- `ReadinessContext` — pre-session go/no-go (reads from Recovery + Fatigue + InjuryRisk)
- `RecoveryContext` — multi-modal recovery tracking (new)
- `FatigueContext` — training-induced fatigue (currently in Athlete State, fine to keep)

**Program Generation** currently merges:
1. Exercise selection (CSP)
2. Session sequencing (order within session)
3. Microcycle planning (distribution across week)
4. Mesocycle planning (progression across weeks)

This should be split into at minimum two contexts:
- `SessionPlanningContext` — exercise selection + session assembly (Layers 3-4)
- `BlockPlanningContext` — microcycle + mesocycle planning (Layers 1-2)

### 4.4 Aggregate Root Map

```
ROOT                    CHILD AGGREGATES
─────────────────────────────────────────────────────
Athlete                 AthleteProfile
                         TrainingAgeMetrics
                         DevelopmentLevel

Assessment              AssessmentMetric[]
                         DeficitRecord[]

TrainingLoad            TrainingLoadEvent[]
                         ACWRRecord

InjuryRisk              InjuryRiskProfile[]
                         RiskFactor[]

Demand                  PerformanceDemand[]
                         RoleDemandPriority[]
                         ExerciseDemandMapping[]

PeriodizationBlock      Mesocycle[]
                         MesocycleWeek[]

Program                 ProgramWeek[]
                         ProgramSession[]
                         SessionExercise[]

RecoveryContext         SleepLog[]
                         WellnessEntry[]
                         TravelFatigueRecord[]

CompetitionCalendar     Season[]
                         CompetitionPhase[]
                         CompetitionEvent[]

CoachingDecision        CoachOverride[]
                         CoachFeedback[]
```

---

## 5. Explainability Review

### 5.1 Current Explainability

The architecture has good **audit trails** (domain_events, recommendation_log, coach_feedback) but poor **decision reasoning**. It answers "what happened?" but not "why this choice over alternatives?"

### 5.2 Five Explainability Questions

**Q1: Why was demand X prioritized over demand Y?**

Current answer: "Because demand_score for X was 84.5 vs 72.3 for Y."

**Missing:** Decomposition of the score into:
- `priority_weight = 0.8 (80th percentile)`
- `deficit_factor = 1.4 (moderate deficit)`
- `level_multiplier = 1.0 (PERFORMANCE)`
- `equipment = 1.0 (all available)`
- `injury_adj = 0.85 (elevated risk)`
- `acwr_adj = 1.0 (in range)`
- `recovery_adj = 0.9 (low recovery)`
- `fatigue_adj = 1.0 (no fatigue)`

**Design Required:**
```sql
CREATE TABLE reasoning_records (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  recommendation_id UUID REFERENCES recommendation_log(recommendation_id),
  reasoning_type VARCHAR(50) NOT NULL, -- 'demand_priority', 'exercise_ranking', 'progression_change', 'session_adaptation'
  subject_type VARCHAR(50) NOT NULL, -- 'demand', 'exercise', 'objective'
  subject_id BIGINT NOT NULL,
  score DECIMAL(10,4),
  score_components JSONB NOT NULL, -- {factor_name: {value, weight, contribution}}
  alternatives_considered JSONB, -- [{id, score, why_rejected}]
  constraint_violations JSONB, -- [{constraint, failed_value, threshold}]
  decision_tree_id BIGINT, -- FK to decision_tree_nodes
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

**Q2: Why was objective A selected over objective B?**

**Missing:** Objective selection trace showing:
- Which demands feed into this objective
- Competition proximity adjustment
- Fatigue budget allocation
- Alternative objectives that were considered and rejected

**Q3: Why did Exercise A rank higher than Exercise B?**

Current answer: "Exercise A had higher demand_score × relevance."

**Missing:** Direct comparison trace:
```
Exercise A (Barbell Back Squat): score=92.4
  demand_score: 85.0 (Vert Jump Power priority)
    × relevance: 9 (strong mapping)
    + tag_bonus: 0.10 (3 matching tags)
    + force_vector_bonus: 0.10 (Vertical matches)
  constraint_check: PASS (equipment, level, fatigue)

Exercise B (Trap Bar Deadlift): score=78.2
  demand_score: 72.0 (Vert Jump Power priority) ← lower demand coverage
    × relevance: 6 (moderate mapping)
    + tag_bonus: 0.05 (1 matching tag)
    + force_vector_bonus: 0 (Vertical not primary)
  constraint_check: PASS

Delta: Exercise A wins on demand_score (+13) and relevance (+3)
```

**Q4: Why did progression change?**

**Missing:** Progression decision trace showing:
- Previous prescription: 4 sets × 8 reps @ 80% 1RM
- New prescription: 4 sets × 6 reps @ 85% 1RM
- Rationale: "Athlete has completed 3 weeks at 80% with no form degradation. Training age = 24mo (DEVELOPMENT). Next progression step per progression_rules for strength exercises: increase intensity by 5%, reduce reps by 2."
- Gate check: "PreSessionGate passed (readiness=72, fatigue=35)"

**Q5: Why was this session adapted (on-the-fly)?**

**Missing:** Real-time adaptation trace showing:
- Original plan: Barbell Back Squat 4×6 @ 85%
- Adapted to: Safety Bar Squat 3×8 @ 75%
- Trigger: "PreSessionGate detected readiness=45 (< 50 threshold). Recovery insufficiency: sleep=4h, stress=8/10, travel=yes. Auto-suggested recovery protocol."
- Coach action: "Coach accepted adaptation. Rationale: 'Athlete had tough travel week, keep it light.'"

### 5.3 Decision Tree Architecture

```sql
CREATE TABLE decision_tree_nodes (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  recommendation_id UUID REFERENCES recommendation_log(recommendation_id),
  parent_node_id BIGINT REFERENCES decision_tree_nodes(id),
  node_type VARCHAR(50) NOT NULL, -- 'branch', 'score_compare', 'constraint_check', 'rejection'
  decision_function VARCHAR(100) NOT NULL, -- 'compare_scores', 'filter_by_equipment', 'apply_fatigue_limit'
  input_snapshot JSONB NOT NULL, -- {entities: [...], scores: {...}, constraints: [...]}
  decision_value VARCHAR(100), -- 'SELECTED', 'REJECTED', 'DEFERRED'
  output_snapshot JSONB, -- {selected: {...}, rejected: {...}, reason: "..."}
  execution_time_ms INT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

This tree captures the full decision path for a recommendation: every comparison, every filter, every constraint check, every rejection. The coach can navigate from "final recommendation" backwards through each decision node to understand why.

---

## 6. Operational Readiness Review

### 6.1 Database Bottlenecks at 10K Athletes

**Critical Path:** Program generation reads:
1. `athlete_state_snapshots` — 10K rows, daily write, weekly read
2. `training_load_events` — 10K × 6/week × 52 = 3.1M rows/year, scanned for ACWR
3. `injury_risk_profiles` — 10K rows, weekly write
4. `assessment_results` — 10K × 7 assessments × quarterly = 280K rows/year
5. `performance_demands` + `role_demand_priority` — < 2K rows (stable)
6. `exercise_demand_mapping` — 10-50K rows
7. `exercises` — 500-2000 rows (stable)
8. `recommendation_log` — 10K × 52 weeks = 520K rows/year (append-only)

**Bottleneck 1: ACWR view scan.** At 3.1M `training_load_events` rows, the `acute_chronic_load_view` (materialized or not) must scan 28 days of history per athlete. Without materialization, this is 3.1M rows scanned × index scan per athlete = 10M-50M row touches per full regeneration cycle.

**Solution:** Convert to **materialized view** with daily refresh:
```sql
CREATE MATERIALIZED VIEW mv_acwr AS
SELECT * FROM acute_chronic_load_view;
CREATE UNIQUE INDEX idx_mv_acwr ON mv_acwr(athlete_id, session_date);
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_acwr; -- daily
```

**Bottleneck 2: CSP solver per athlete.** CSP solving for 10K athletes sequentially at 30s each = 83 hours. Won't finish in a day.

**Solution:** Decompose (see Section 2.3) + parallel worker pool:
- Layer 1 (periodization): once per athlete per month, cache aggressively
- Layer 2 (mesocycle): once per athlete per 4-6 weeks, cache
- Layer 3 (microcycle): once per athlete per week, run in parallel (10K ÷ 100 workers = 100 batches ~ 5-10 min)
- Layer 4 (session assembly): on-demand, fast (< 1s per session)

**Bottleneck 3: recommendation_log writes.** 10K athletes × 52 weeks = 520K rows/year. Each row stores full JSONB snapshots (50-200KB). Total: 26-104 GB/year.

**Solution:**
- Archive to `recommendation_log_archive` after 90 days (same schema, cheaper storage)
- Partial indexes on recent data only
- Consider columnar compression for the JSONB columns (pg_jsonschema or similar)

### 6.2 Caching Strategy

**Current:**
- In-memory dicts with SHA-256 keys
- TTLs of 300-3600s
- No invalidation on relevant events

**Required at 10K scale:**

| Cache | Scope | TTL | Invalidation Trigger | Storage |
|-------|-------|-----|--------------------|---------|
| Sport configuration | Global | 1 hour (or until config change event) | ConfigChange event | Redis |
| ACWR data | Per-athlete | 1 hour (or until new load event) | TrainingLoadRecorded | Redis |
| Injury risk profiles | Per-athlete | 1 hour (or until recompute) | InjuryRiskUpdated | Redis |
| Demand scores | Per-athlete | Until next assessment or config change | AssessmentMetricsExtracted | Redis |
| Exercise pool (per demand) | Global | 1 hour | ExerciseLibraryChange event | Redis |
| CSP solution (microcycle) | Per-athlete | Until next week or event | Sleep cycle boundary | Redis |
| Periodization blocks | Per-athlete | Until season phase change | CompetitionPhaseChanged | Redis |

**Cache Architecture:**
```python
class CacheStrategy:
    # Multi-tier: L1 (local memory) for hot data, L2 (Redis) for warm data
    # L1: sport config, exercise library (rarely changes)
    # L2: athlete-specific computed data
    
    def get_or_compute(self, key, compute_fn, ttl, invalidation_events):
        # Check L1 → L2 → compute
        # On compute: publish cache_loaded event
        # On invalidation event: clear L1+L2 for this key pattern
```

### 6.3 Event-Driven Architecture at Scale

**Current:** DB-based event emission (INSERT INTO domain_events). No message broker.

**At 10K athletes, daily:**
- TrainingLoadRecorded: 10K × 6 = 60K events/day
- ACWRCalculated: 60K events/day (coupled to load events)
- AthleteStateCalculated: 10K events/day
- InjuryRiskUpdated: 10K events/day (weekly batch)
- DemandScoreCalculated: 10K × 18 demands = 180K events/day
- AssessmentMetricsExtracted: 10K × 1 = 10K events/day (quarterly avg)
- **Total: ~320K events/day**

**DB-based event emission at 320K events/day:**
- 320K INSERTs on domain_events table
- Plus consumers that would need to SELECT from domain_events (polling)
- Polling at 1-min intervals: 1440 queries/day × scan of unprocessed events
- This works at low volume but fails at 10K scale due to polling overhead and table bloat

**Recommendation:** Introduce a message broker (Redis Streams or RabbitMQ) for event distribution:
```python
# After successful DB insert, publish to stream
async def emit_with_broker(event_data):
    # 1. INSERT into domain_events (audit trail, immutable record)
    event_id = await insert_domain_event(event_data)
    # 2. Publish to Redis Stream / RabbitMQ (async dispatch)
    await broker.publish("domain_events", {**event_data, "event_id": event_id})
    return event_id
```

This gives:
- Reliable delivery with consumer groups
- Retry + dead-letter queues for failed consumers
- Parallel consumption (ACWR recalculation can run in parallel with injury risk recompute)
- Backpressure (slow consumers don't block producers)
- Replay capability (reprocess from last N hours/days)

### 6.4 Background Jobs

**Required job queue:**

| Job | Frequency | Duration (10K) | Priority |
|-----|-----------|----------------|----------|
| ACWR materialized view refresh | Hourly | 5-30s | HIGH (affects all reads) |
| Injury risk recompute | Daily | 5-30min | MEDIUM |
| Athlete state recompute | Daily | 2-10min | MEDIUM |
| Mesocycle planning | Weekly | 10-60min (parallel) | MEDIUM |
| Microcycle regeneration | Weekly | 5-30min (parallel) | HIGH |
| recommendation_log archival | Daily | < 5min | LOW |
| Config snapshot creation | On config change | < 1s | HIGH |
| Old recommendation purge | Monthly | 5-15min | LOW |

**Architecture:**
```
Worker Pool (Celery / Arq / Hue):
  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
  │ config_worker │  │ load_worker  │  │ csp_worker   │
  │ (1 instance)  │  │ (5 instances)│  │ (100 inst.)   │
  └─────────────┘  └─────────────┘  └─────────────┘
         │                │                 │
         └────────────────┼─────────────────┘
                          ▼
                  ┌──────────────┐
                  │  Redis Queue  │
                  │  + DLQ        │
                  └──────────────┘
                          │
                          ▼
                  ┌──────────────┐
                  │  Priority     │
                  │  Router       │
                  └──────────────┘
                   HIGH │ MEDIUM │ LOW
```

### 6.5 Observability

**Required metrics (Prometheus or similar):**

```
# Pipeline performance
forge_pipeline_duration_seconds{stage="demand_scoring"} …histogram
forge_pipeline_duration_seconds{stage="csp_solving"} …histogram
forge_pipeline_duration_seconds{stage="session_assembly"} …histogram
forge_pipeline_total{status="success|error|empty"} …counter

# Data health
forge_athlete_stale_days{stale_type="no_assessment|no_load|no_readiness"} …gauge
forge_acwr_coverage_ratio …gauge (% of athletes with valid ACWR)

# Quality
forge_coach_acceptance_rate{role="sprint|power|etc"} …gauge
forge_recommendation_empty{reason="no_exercise|constraint_failure"} …counter
forge_oscillation_index{window="3weeks"} …gauge (Jaccard distance between successive top-K)

# Resources
forge_cache_hit_ratio{cache_layer="L1|L2"} …gauge
forge_db_connection_pool_usage …gauge
forge_queue_depth{queue="csp|load|config"} …gauge
forge_worker_pool_usage{pool="csp|load|state"} …gauge
```

### 6.6 Failure Recovery

| Failure Mode | Detection | Recovery |
|-------------|-----------|----------|
| CSP solver failure (timeout) | Duration > 5 min | Fallback to heuristic ranking (no CSP) + log intervention needed |
| DB connection pool exhaustion | Connection wait > 1s | Circuit breaker: shed load for 30s, retry |
| Stale cache (wrong config) | Config version mismatch | Force recompute + alert |
| Event processing backlog > 1h | Queue depth alert | Scale worker pool, skip non-critical recomputes |
| Inconsistent athlete state | State timestamp vs current time gap > 24h | Force full recompute on next request |
| Coach feedback lost | recommendation_id not found | Store feedback in local buffer, retry on recovery |

---

## 7. AI & Future Intelligence Layer

### 7.1 Coach Feedback Learning

**Scenario:** Coach repeatedly swaps Exercise A for Exercise B when recommending for demand X.

**Can the system learn?** Currently: NO. The feedback is stored but never analyzed.

**Architecture Required:**

```sql
-- Pattern detection table
CREATE TABLE coach_behavior_patterns (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  coach_id INT,
  pattern_type VARCHAR(50) NOT NULL, -- 'substitution', 'override_intensity', 'reorder'
  trigger_context JSONB NOT NULL, -- {demand_id, exercise_a_id, exercise_b_id, athlete_level, phase}
  frequency INT NOT NULL DEFAULT 1,
  last_observed TIMESTAMPTZ,
  confidence DECIMAL(5,2), -- statistical confidence in pattern (0-1)
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Learning service
class CoachPatternLearner:
    def detect_substitution_patterns(coach_id, since_date):
        """
        Analyze coach_feedback for repeated substitutions.
        If coach swaps A→B for same demand >3 times:
          - Record pattern with confidence = min(0.5 + 0.1 * count, 0.95)
          - Suggest adjusting exercise_demand_mapping relevance_score for A vs B
          - If confidence > 0.8: auto-apply with coach notification
        """
    
    def detect_intensity_bias(coach_id):
        """
        Detect if coach consistently modifies intensity up/down.
        Build coach calibration curve: recommended vs actual intensity.
        """
```

**Learning Loop:**
```
Coach modifies recommendation
  → stored in coach_feedback
  → CoachPatternLearner analyzes batch (daily)
  → Pattern confidence computed
  → If > threshold: suggest config change to coach
  → If coach accepts: update exercise_demand_mapping / role_demand_priority
  → Next recommendation reflects learned preference
```

### 7.2 Outcome Learning

**Scenario:** Programs with certain exercise combinations consistently lead to CMJ improvement.

**Can the system learn which prescriptions work?** Currently: NO. There is no outcome metric linked to program composition.

**Architecture Required:**

```sql
-- Outcome tracking
CREATE TABLE outcome_measurements (
  id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  athlete_id BIGINT NOT NULL,
  program_id BIGINT REFERENCES programs(id),
  metric_type VARCHAR(50) NOT NULL, -- 'CMJ', 'Broad_Jump', 'Sprint_10m'
  pre_value DECIMAL(10,2),
  post_value DECIMAL(10,2),
  delta DECIMAL(10,2),
  delta_pct DECIMAL(5,2),
  timeframe_days INT,
  assessment_pre_id BIGINT REFERENCES assessment_results(id),
  assessment_post_id BIGINT REFERENCES assessment_results(id),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Prescription-outcome analysis view
CREATE VIEW prescription_effectiveness AS
SELECT
  od.demand_id,
  od.exercise_id,
  AVG(om.delta_pct) AS avg_improvement,
  STDDEV(om.delta_pct) AS variability,
  COUNT(*) AS sample_size,
  CORR(om.delta_pct, ps.weekly_volume) AS volume_correlation,
  CORR(om.delta_pct, ps.weekly_intensity) AS intensity_correlation
FROM program_sessions ps
JOIN program_session_exercises pse ON ps.id = pse.program_session_id
JOIN exercise_demand_mapping od ON pse.exercise_id = od.exercise_id
JOIN outcome_measurements om ON om.program_id = ps.program_id
  AND om.metric_type = od.demand_id  -- demand → metric mapping
WHERE om.delta IS NOT NULL
GROUP BY od.demand_id, od.exercise_id;
```

**Learning Loop:**
```
Program generated → athlete executes → reassessment → outcome_measurement
  → PrescriptionEffectiveness updated
  → CSP solver receives effectiveness data as soft constraint
  → Exercises with high effectiveness for specific demand get boost in scoring
  → Exercises with negative effectiveness get penalty
  → Over time, system converges on evidence-based prescription
```

**Counterfactual Requirement:** To truly learn "what works," the system needs to occasionally recommend non-optimal exercises to build a counterfactual dataset. Without counterfactuals, the system only learns "this exercise is effective when recommended" but not "would a different exercise have been more effective?"

```python
class ExplorationStrategy:
    def __init__(self, epsilon=0.1):
        # Epsilon-greedy: 90% of time recommend optimal, 10% explore
        self.epsilon = epsilon
    
    def should_explore(self, athlete_id, demand_id):
        # Explore more for new athletes (cold start) or demands with low confidence
        return random.random() < self.epsilon
```

### 7.3 Recommendation Engine for Future Intelligence

**Future Goal:** "Suggest better objective," "Suggest alternative exercise," "Suggest different exposure target."

**Can current architecture support this?** PARTIALLY, with significant additions.

**Required changes:**

1. **Alternative generation service:** For any recommendation, generate N alternatives with different trade-offs:
```python
class AlternativeGenerator:
    def generate_alternatives(recommendation_id, count=3):
        """
        For the given recommendation, generate alternatives by:
        - Modifying solver weights (e.g., reduce fatigue penalty → higher intensity session)
        - Substituting exercises with equivalents
        - Reprioritizing demands (e.g., emphasize power over strength)
        Returns ranked alternatives with trade-off analysis.
        """
```

2. **What-if simulation API:**
```python
@router.post("/recommendations/what-if")
async def what_if_simulation(
    recommendation_id: UUID,
    parameter_overrides: Dict[str, Any],
    body: WhatIfRequest
) -> WhatIfResponse:
    """
    Simulate how recommendation changes if:
    - ACWR threshold is tightened
    - A different periodization model is used
    - Equipment availability changes
    Returns alternative recommendation + diff from original.
    """
```

3. **Explanation-driven suggestion engine:**
```python
class SuggestionEngine:
    def suggest_alternative_objective(athlete_id, current_objective):
        """
        Analyze ignored demands (high priority × high deficit but not selected)
        Suggest shifting focus to a different quality category
        """
    
    def suggest_alternative_exercise(current_exercise, demand_id):
        """
        Based on coach feedback patterns + equivalence mapping + outcome data,
        suggest top-3 alternatives for the given exercise.
        """
    
    def suggest_exposure_target_adjustment(athlete_id, demand_id):
        """
        Based on adaptation_rate + current deficit trajectory,
        suggest increasing/decreasing weekly exposure.
        """
```

---

## 8. Technical Debt Forecast

### Year 1: Architectural Failures

**Most likely failure points:**

1. **Configuration Explosion** (Month 3-6)
   - After onboarding sport #10, coaches need sport-specific demand weights, phase targets, and exercise mappings
   - No UI for configuration → engineers become bottleneck for every config change
   - **Impact:** Coach trust erodes when they can't tune the system themselves
   - **Cost:** 2-4 sprint months to build configuration UI + inheritance system

2. **Oscillation Destroys Coach Trust** (Month 1-3)
   - Even with damping, if alpha is not tuned per sport/phase, oscillation occurs
   - Coaches see different top-3 recommendations week-over-week for same athlete
   - **Impact:** Coaches stop accepting recommendations, adoption stalls
   - **Cost:** 1-2 sprint months for oscillation monitoring dashboard + auto-tuning

3. **Empty Recommendation Rate** (Month 2-4)
   - as CSP constraints accumulate (equipment + fatigue + diversity + competition embargo), solvable space shrinks
   - Athletes in competition phase with limited equipment options get empty or near-empty programs
   - **Impact:** Coach override rate spikes, value proposition undermined
   - **Cost:** 2-3 sprint months for constraint relaxation hierarchy + fallback chains

4. **Recovery Model Incompleteness** (Month 4-8)
   - Coaches notice athletes with poor sleep, high travel, or illness are getting full-intensity programs
   - PreSessionGate catches some but not all — athletes report feeling overprescribed
   - **Impact:** Injury spike or burnout in 1-2 athletes → liability concern → system pause
   - **Cost:** 3-4 sprint months for full recovery context integration

### Year 2: Scaling Failures

**Most likely failure points:**

1. **Database Performance Degradation** (12-18 months)
   - training_load_events at 3-6M rows
   - recommendation_log at 500K-1M rows with JSONB blobs
   - ACWR view scans become slow (500ms → 5s)
   - **Impact:** API response times degrade, coaches complain of slowness
   - **Cost:** 2-3 sprint months for materialized view optimization + archival strategy

2. **CSP Solver Timeout** (14-20 months)
   - At 5K+ athletes with weekly regeneration, CSP solver latency grows
   - Constraint complexity increases as new rules are added
   - **Impact:** Overnight batch job misses morning deadline
   - **Cost:** 3-5 sprint months for solver rearchitecture (decomposed approach from Section 2.3)

3. **Coach Feedback Loop Saturation** (16-24 months)
   - coach_feedback at 100K+ rows with diverse override patterns
   - No automated pattern detection → no learning from feedback
   - **Impact:** Coaches feel system ignores their preferences → disengagement
   - **Cost:** 3-4 sprint months for pattern learning implementation

4. **Event Processing Backlog** (18-24 months)
   - 320K+ events/day on DB-only event system
   - No message broker → polling consumers fall behind
   - **Impact:** Stale state → wrong recommendations → coach frustration
   - **Cost:** 2-3 sprint months for message broker integration

### Year 3: Redesign Requirements

**Most likely major redesigns:**

1. **Periodization Engine Rewrite** (24-30 months)
   - Initial architecture didn't model mesocycles, blocks, or adaptation
   - Coaches in year 2-3 demand real periodization, not session-level planning
   - **Required:** Full periodization engine with block planning, supercompensation modeling, tapering
   - **Cost:** 8-12 sprint months — effectively a new major subsystem

2. **ML Pipeline Rearchitecture** (24-36 months)
   - After 2 years of outcome data, the organization wants predictive models
   - Current data model lacks features needed for ML (no counterfactuals, no outcome-linked prescriptions)
   - **Required:** Feature engineering pipeline, training infrastructure, model serving, A/B testing
   - **Cost:** 6-10 sprint months — significant infrastructure investment

3. **Multi-Tenancy Performance Overhaul** (30-36 months)
   - At 50+ organizations, shared schema with organization_id filtering becomes slow
   - Indexing strategy breaks down (selectivity of org_id decreases as orgs grow)
   - **Required:** Schema-per-tenant or partition-per-tenant architecture
   - **Cost:** 6-8 sprint months — database rearchitecture

4. **Exercise Library Scaling** (24-36 months)
   - 5K+ exercises with complex mapping matrices become unmanageable
   - maintenance burden for exercise_demand_mapping grows quadratically
   - **Required:** Auto-classification of exercises using movement pattern analysis + ML
   - **Cost:** 4-6 sprint months for exercise intelligence pipeline

---

## 9. Final Production Readiness Score

### Scorecard

| Area | Current Score (/100) | After Recommended Changes | Rationale |
|------|---------------------|--------------------------|-----------|
| Sports Science | 45 | 78 | Strong deficit-fitness model but no adaptation/periodization/recovery completeness |
| Architecture | 55 | 82 | Clean DDD boundaries emerging but missing 4 contexts, incorrect splitting in Program Generation |
| Scalability | 40 | 75 | CSP at 10K athletes needs decomposition; DB needs materialized views + caching + broker |
| Explainability | 50 | 88 | Good audit trail infrastructure but no reasoning records or decision trees yet |
| Extensibility | 55 | 80 | Event-driven foundation good but no alternative generators or what-if simulation |
| Maintainability | 60 | 78 | Configuration explosion risk high; needs inheritance + UI + versioning |
| Operational Readiness | 35 | 72 | No background jobs, no caching strategy, no production monitoring |
| AI Readiness | 20 | 65 | Coach feedback + outcome learning infrastructure doesn't exist yet; no counterfactual support |

### Production Readiness Verdict

| Criterion | Value |
|-----------|-------|
| **Overall Score** | **52/100** (45+55+40+50+55+60+35+20) ÷ 8 |
| **Target for Limited Production** | 65/100 minimum |
| **Target for Full Production** | 80/100 minimum |
| **Gap to Limited Production** | Requires completion of 5 HIGH items (~4-6 sprint months) |
| **Gap to Full Production** | Requires completion of all items (~12-18 sprint months) |

**Verdict:** **BUILD PILOT ONLY**

### Conditions for Pilot

**Pilot scope:**
- Max 5 organizations
- Max 500 athletes total
- Max 3 sports (Cricket + 2 others)
- Coach feedback collection enabled but pattern learning NOT required
- Manual configuration management (no auto-suggestion)

**Pass/fail criteria for pilot (measured at 90 days):**

| Metric | Target | Critical Threshold |
|--------|--------|-------------------|
| Coach acceptance rate (first recommendation) | > 60% | < 40% = fail |
| Coach acceptance rate (after 1 modification) | > 80% | < 60% = fail |
| Empty recommendation rate | < 2% | > 5% = fail |
| Top-3 week-over-week stability (Jaccard > 0.5) | > 70% of athletes | < 50% = fail |
| API P95 latency | < 3s | > 10s = fail |
| Data completeness (athletes with valid ACWR) | > 90% | < 70% = fail |
| Injury rate vs baseline | Not elevated | Elevated at p < 0.05 = fail |

### Recommended Build Order

| Phase | Duration | Deliverables | Score Target |
|-------|----------|-------------|-------------|
| **Pilot Launch** | Month 1-3 | Core pipeline + execution tracking + basic explainability | 52 → 58 |
| **Observability** | Month 2-3 | Monitoring + alerts + background jobs | 58 → 62 |
| **Recovery Model** | Month 3-5 | Recovery context + sleep/travel/stress integration + PreSessionGate enhancement | 62 → 68 |
| **Periodization Blocks** | Month 4-7 | Mesocycle/microcycle aggregates + block planning | 68 → 74 |
| **Configuration UI** | Month 5-8 | Config inheritance + versioning + UI | 74 → 78 |
| **Learning Loop** | Month 7-12 | Coach pattern learning + outcome measurement + alternative generation | 78 → 85 |

---

## Final Verdict

FORGE V2's revised architecture is **structurally sound but conceptually incomplete** for the full problem space of intelligent program design. It excels at deficit detection, exercise selection, and auditability. It fails to model the fundamental physiological processes it claims to optimize: adaptation, periodization, and recovery.

The architecture is appropriate for a **Phase 1-2 system** (tracking + progression). To reach Phase 3 (intelligent planning), it requires:

1. **Periodization aggregates** (mesocycle, block, competition phase)
2. **Adaptation modeling** (dose-response, supercompensation, decay)
3. **Recovery completeness** (sleep, travel, environment, stress, illness)
4. **Solver decomposition** (heuristic + CP-SAT + CSP + rules engine)
5. **Production infrastructure** (message broker, background workers, caching, monitoring)

The system should **not ship to full production** without these components. A controlled pilot with 5 organizations and 500 athletes is the responsible next step.
