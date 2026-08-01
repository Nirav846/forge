# AUDIT #6 — DATA FLOW & EXPLAINABILITY AUDIT
# Complete Decision Trace with Fast Bowler Example

**Review Mode:** Data Flow Validation | Decision Traceability | Audit Trail Completeness
**Date:** 2026-06-17
**Rule:** Do not review architecture. Do not suggest new contexts. Do not redesign. Trace only.

---

## ATHLETE PROFILE

| Attribute | Value | Source |
|-----------|-------|--------|
| Role | Fast Bowler | `roles.name` |
| Sport | Cricket | `sports.name` |
| Training Age | 4 years (48 months) | `athletes.training_age_months` |
| Development Level | PERFORMANCE | `training_months_to_level(48)` → `>= 36` |
| CMJ | ~31 cm (z = -1.8, mean = 40, std = 5) | `assessment_results` |
| 10m Sprint | ~1.95 s (z = -0.9) — using API example value | `assessment_results` |
| ACWR | 1.12 | `acute_chronic_load_view` |
| Readiness | 74 | `athlete_state_snapshots.readiness_score` |
| Competition | 5 days away | `competition_calendar` (conceptual) |

---

## SECTION A — COMPLETE DECISION TRACE

---

### DECISION 1: Assessment → Metric Deficit

**Actual endpoint:** `assessment_metric_engine.py` → `POST /api/v2/metric-deficits/compute`

**Code path:** `AssessmentMetricService.compute_metric_deficits()` at assessment_metric_engine.py:250-320

**What happens:**

```
CMJ assessment (id=1) has 5 metrics:
  jump_height  (id=1, higher_is_better=True)
  peak_power   (id=2, higher_is_better=True)
  eccentric_rate (id=3, higher_is_better=True)
  concentric_time (id=4, higher_is_better=False)
  RSI_mod      (id=5, higher_is_better=True)

For jump_height = 31 cm:
  norm = repo.norms[1] = {"mean": 40.0, "std": 5.0, "sport": "Generic"}
  z_score = (31.0 - 40.0) / 5.0 = -1.8
  deficit_severity = max(0, min(1, -(-1.8) / 3)) = max(0, min(1, 0.6)) = 0.6
  # z-scores below -3.0 would give severity = 1.0
  # z-scores at 0 or positive would give severity = 0.0
```

**Answer table:**

| Question | Answer |
|----------|--------|
| What data caused the decision? | CMJ jump_height = 31 cm. Norm values: mean=40, std=5. |
| Which rule caused the decision? | `severity = max(0, min(1, -z / 3))` when `higher_is_better=True` |
| Which table caused the decision? | `assessment_metrics` (for metric definition + higher_is_better flag), `metric_norms` (for mean, std) |
| Can the coach understand the reason? | PARTIALLY. They see z-score = -1.8 and severity = 0.6. But the hardcoded "/3" denominator is unexplained — why 3? Why not 2 or 4? |
| Can the decision be reproduced exactly? | **YES IF** the norm values are versioned. Currently norms have no version column. If a norm changes, historical reproducibility breaks. |

**BLACK BOX WARNING:** The `/3` denominator is a hardcoded assumption that a z-score of -3 represents complete deficit. There is no configuration table for this. No explanation is stored. A coach cannot know why -1.8 z-score maps to 0.6 severity rather than 0.45 or 0.75.

---

### DECISION 2: Metric Deficit → Demand Score (FIRST system)

**Actual endpoint:** `demand_scoring_engine.py` → `POST /api/v2/demand-recommendations`

**Code path:** `compute_role_demand_scores()` at demand_scoring_engine.py:947-979

**NOTE: THIS IS THE FIRST MAJOR EXPLAINABILITY GAP.** The demand_scoring_engine does NOT use the metric deficits computed in Decision 1. It computes its OWN deficits from raw assessment scores using a DIFFERENT formula.

**What actually happens:**

```python
# demand_scoring_engine.py:906-944
# compute_deficit_factor_sync() — completely independent deficit computation

# CMJ = 31.0 → "CMJ" in assessment_name → is_sprint=False
deficit_severity = 1.0 - min(31.0 / 50.0, 1.0)  # = 1.0 - 0.62 = 0.38

# Maps to demands via assessment_demand_mappings:
# CMJ → Vertical Power (weight=1.0): weighted = 0.38 * 1.0 = 0.38
# CMJ → Single-Leg Power (weight=0.6): weighted = 0.38 * 0.6 = 0.228

# 10m Sprint = 1.95 → is_sprint=True
deficit_severity = 1.0 - min(1.95 / 3.0, 1.0)  # = 1.0 - 0.65 = 0.35

# Maps to demands:
# 10m Sprint → Horizontal Drive Power (weight=0.8): 0.35 * 0.8 = 0.28
# 10m Sprint → Single-Leg Power (weight=0.6): 0.35 * 0.6 = 0.21

# Final deficit_factors:
# Vertical Power = max(0.38) = 0.38
# Horizontal Drive Power = max(0.28) = 0.28
# Single-Leg Power = max(0.228, 0.21) = 0.228
```

Then demand scores are computed:
```python
# Fast Bowler demands + deficit_factors
# level_mult = 1.0 (PERFORMANCE)
# demand_score = priority_weight * (1 + deficit) * level_mult * 100

# Vertical Power (priority=100): 1.0 * (1.0 + 0.38) * 1.0 * 100 = 138.00
# Horizontal Drive Power (95): 0.95 * (1.0 + 0.28) * 1.0 * 100 = 121.60
# Hinge Strength (90): 0.90 * (1.0 + 0.0) * 1.0 * 100 = 90.00
# Rotational Explosive Power (85): 0.85 * (1.0 + 0.0) * 1.0 * 100 = 85.00
# Squat Strength (80): 0.80 * (1.0 + 0.0) * 1.0 * 100 = 80.00
# Single-Leg Stability (75): 0.75 * (1.0 + 0.0) * 1.0 * 100 = 75.00
# (remaining demands have deficit=0, score = priority_weight * 100)
```

**Answer table:**

| Question | Answer |
|----------|--------|
| What data caused the decision? | Raw CMJ=31.0, raw sprint=1.95. NOT the z-scores from Decision 1. |
| Which rule caused the decision? | `deficit = 1 - min(raw/50, 1)` for CMJ. `deficit = 1 - min(raw/3, 1)` for sprint. |
| Which table caused the decision? | `assessment_demand_mapping` (for weight), `role_demand_priority` (for priority), `assessment_results` (for raw scores). |
| Can the coach understand the reason? | **NO — BLACK BOX.** The formula `1 - min(raw/50, 1)` uses hardcoded normalization denominators. Why 50cm for CMJ? Why 3s for sprint? These are not stored in any table. Coach sees 138.0 but cannot decompose it. |
| Can the decision be reproduced exactly? | **YES** if the hardcoded denominators never change. But they live in source code, not configuration — a deployment changes them silently. |

**CRITICAL EXPLAINABILITY FAILURE:** The same assessment (CMJ z=-1.8) produces deficit=0.6 in the assessment_metric_engine but deficit=0.38 in the demand_scoring_engine. Two different systems, two different deficit values, no reconciliation. A coach who inspects both endpoints gets contradictory answers.

---

### DECISION 3: Deficit → Demand Score (SECOND system — demand lifecycle)

**Actual endpoint:** `demand_lifecycle_engine.py` → `POST /api/v2/demand-states/compute`

**Code path:** `DemandStateService._compute_single_demand()` at demand_lifecycle_engine.py:148-228

**NOTE: ANOTHER EXPLAINABILITY GAP.** There is a THIRD deficit-to-demand-score computation that uses DIFFERENT formulas and INCLUDES factors the demand_scoring_engine ignores.

**What actually happens (if this endpoint is called):**

```python
# For Vertical Power with deficit=0.38 (from demand_scoring_engine, if fed as demand_deficits):

# Step 1: deficit_normalized = max(0, min(1, 0.38)) = 0.38
# Step 2: base_score = 100 - (0.38 * 100) = 62.0
# Step 3: role_multiplier = 100/100 = 1.0 (priority 100)
# Step 4: demand_score = 62.0 * 1.0 = 62.0

# Now apply factors the demand_scoring_engine IGNORES:
# injury_risk adjustment: if injury_risk=25 → adj = 1 - 25/100 = 0.75
# ACWR adjustment: 1.12 → 0.8<1.12<1.3... elif 1.12>1.0 or 1.12<1.3? 
#   Actually: if acwr < 0.8 or acwr > 1.5: 0.8
#            elif acwr < 1.0 or acwr > 1.3: 0.9
#            else: 1.0
#   1.12: not < 0.8, not > 1.5 → check elif: 1.12 > 1.0 → adj = 0.9
# recovery adjustment: if recovery=70 → adj = 70/100 = 0.7
# fatigue adjustment: if fatigue=30 → adj = 1 - 30/200 = 0.85

# risk_adjusted = 62.0 * 0.75 * 0.9 * 0.7 * 0.85 = 62.0 * 0.40 = 24.87
# priority_score = 100 - 24.87 = 75.13
```

**Result:** The SAME demand (Vertical Power) scores 138.0 in demand_scoring_engine but risk_adjusts to 24.87 in demand_lifecycle_engine. These are different numbers representing different concepts, but the coach sees no explanation of which score was used for which decision.

**Answer table:**

| Question | Answer |
|----------|--------|
| What data caused the decision? | deficit=0.38, ACWR=1.12, recovery=70, fatigue=30, injury_risk=25 |
| Which rule caused the decision? | `risk_adjusted = base_score * role_mult * injury_adj * acwr_adj * recovery_adj * fatigue_adj` |
| Which table caused the decision? | `role_demand_priority`, `injury_risk_profiles`, `athlete_state_snapshots`, `acute_chronic_load_view` |
| Can the coach understand the reason? | **PARTIALLY.** The `components` dict captures each factor. But why ACWR 1.12 → adj 0.9? The zone thresholds (0.8, 1.0, 1.3, 1.5) are hardcoded. |
| Can the decision be reproduced exactly? | **NO — BLACK BOX.** ACWR zone thresholds are hardcoded at demand_lifecycle_engine.py:180-185. No configuration table. |

---

### DECISION 4: Demand Score → Exposure Target

**Actual code:** **DOES NOT EXIST.**

There is no exposure target entity, table, or computation in the codebase. No `demand_exposure_targets` table. No `compute_exposure_targets()` function. The Exposure Planning domain is conceptual — it does not exist in code.

**What the system actually does:** After computing demand scores, it jumps directly to exercise selection (Decision 5). There is no intermediate step that determines "this athlete needs 3 sessions of Vertical Power work this week, 2 sessions of Hinge Strength."

**Explainability status:** **MISSING — NO TRACE POSSIBLE.**
- The system cannot explain "why 2x per week for this demand?"
- The system cannot explain "why 3x per week for that demand?"
- There is no exposure target to trace

---

### DECISION 5: Exposure Target → Objective Assignment

**Actual code:** **DOES NOT EXIST.**

No objective entity. No primary/secondary/tertiary objective selection. No `session_objectives` table. The demand_scoring_engine computes demand scores and then selects exercises for each demand directly.

**What the system actually does:** For each scored demand (in priority order), it fetches exercises and ranks them. There is no consolidation into session-level objectives.

**Explainability status:** **MISSING — NO TRACE POSSIBLE.**
- The system cannot explain "why was Vertical Power the primary objective?"
- The system cannot explain "why were these 3 demands combined in this session?"
- There is no objective assignment to trace

---

### DECISION 6: Objective Assignment → Session Sequencing

**Actual code:** **DOES NOT EXIST.**

No sequencing engine. No session ordering logic. No fatigue carryover between sessions. No competition proximity consideration.

**What the system actually does:** The `program_builder.py` generates 4-week programs using V1 template-based logic (movement_templates → template_slots). The V2 demand_scoring_engine computes ranked exercises but does NOT sequence them into sessions. The V1 program builder fills template slots with exercises from the recommendation engine — it has NO concept of the athlete's ACWR, readiness, or competition proximity.

**For this athlete with competition in 5 days:** The V1 program builder will generate a 4-week block starting with Week 1 (Base) at 75% intensity, regardless of the competition proximity. The "5 days until competition" datum is invisible to both engines.

**Explainability status:** **MISSING — NO TRACE POSSIBLE.**
- The system cannot explain "why is this exercise in session 1 vs session 3?"
- The system cannot explain "why is this a 4-week block if competition is in 5 days?"
- There is no sequencing logic to trace

---

### DECISION 7: Session Sequencing → Exercise Selection

**Actual endpoint:** `demand_scoring_engine.py` → `POST /api/v2/demand-recommendations`

**Code path:** lines 1059-1092

**What actually happens:**

```python
# For each scored demand (in priority order):
for sd in scored_demands:  # Vertical Power (138.0), Horizontal Drive Power (121.6), Hinge Strength (90.0), ...
    exercises = await repo.get_exercises_for_demand(
        demand_id=sd["demand_id"],
        difficulty_cap="Advanced",  # from request
        equipment=["Trap Bar", "Medicine Ball"],
        training_age_months=48,
        development_level="PERFORMANCE",
    )
    
    # Each exercise gets scored:
    for ex in exercises:
        relevance = ex["relevance_score"] / 10.0  # e.g., 10/10 = 1.0
        priority_weight = sd["priority"] / 100.0  # e.g., 100/100 = 1.0
        level_mult = 1.0  # PERFORMANCE
        eq_match = 1.0  # if all equipment available, else 0.0
        
        score = relevance * priority_weight * level_mult * eq_match
        # e.g., for Trap Bar Jump Squat → Vertical Power:
        # 1.0 * 1.0 * 1.0 * 1.0 * 100 = 100.0
```

**For Vertical Power demand (priority=100), exercises available:**
| Exercise | Relevance | Score |
|----------|-----------|-------|
| Trap Bar Jump Squat | 10/10=1.0 | 1.0×1.0×1.0×1.0×100 = **100.0** |
| Power Clean | 10/10=1.0 | 1.0×1.0×1.0×1.0×100 = **100.0** |
| Depth Jump | 10/10=1.0 | 1.0×1.0×1.0×1.0×100 = **100.0** |
| Mid-Thigh Pull | 9/10=0.9 | 0.9×1.0×1.0×1.0×100 = **90.0** |
| Medicine Ball Overhead Backwards Toss | 9/10=0.9 | 0.9×1.0×1.0×1.0×100 = **90.0** |
| Barbell Back Squat | 6/10=0.6 | 0.6×1.0×1.0×1.0×100 = **60.0** |

**CRITICAL: Many exercises have identical scores.** Trap Bar Jump Squat, Power Clean, and Depth Jump all score 100.0 for Vertical Power. The sort is stable (Python's sort preserves input order) but there is NO tiebreaker rule. The final ranking depends on the order exercises were returned from `get_exercises_for_demand()`, which sorts by `relevance_score DESC`. But when relevance_score is identical (all 10), the order depends on the physical order of the exercise_demand_mapping data structure.

**Answer table:**

| Question | Answer |
|----------|--------|
| What data caused the decision? | demand_id, difficulty_cap, equipment list, training_age, development_level |
| Which rule caused the decision? | `score = relevance × priority_weight × level_mult × eq_match × 100` |
| Which table caused the decision? | `exercise_demand_mapping` (relevance_score), `exercises` (difficulty, technical_difficulty, minimum_level), `exercise_equipment` |
| Can the coach understand the reason? | **PARTIALLY.** They see the score but not the tiebreaker. If Trap Bar Jump Squat ranks above Power Clean, both at 100.0, there is NO explainable reason for the ordering. |
| Can the decision be reproduced exactly? | **NO — BLACK BOX.** If the exercise library is reseeded (changing insertion order), the ranking of equally-scored exercises changes. No seed value, no ordering guarantee. |

---

### DECISION 8: Exercise Selection → Progression

**Actual endpoint:** `program_builder.py` → `POST /generate-program`

**Code path:** Program builder calculates reps/intensity using V1 rules based on exercise class.

**What actually happens for the V1 program builder:**

```python
# program_builder.py: weekly progression (hardcoded):
# Week 1 (Base):         3 sets, 75% 1RM
# Week 2 (Accumulation): 4 sets, 80% 1RM
# Week 3 (Peak):         4 sets, 85% 1RM (reps = max(2, baseline - 2))
# Week 4 (Deload):       2 sets, 60% 1RM

# For Olympic Lift class: velocity-focused intensity
# For Core/Isometric/Sprint: different progression
```

**For this athlete with competition in 5 days:** The program builder generates a full 4-week program starting with Week 1 at 75% intensity. Week 3 (Peak) falls exactly on competition day — the athlete would be doing 85% 1RM on competition day. There is NO competition-aware logic to adjust the program start or progression.

**Answer table:**

| Question | Answer |
|----------|--------|
| What data caused the decision? | Exercise class (from `classify_exercise()`), week number (1-4) |
| Which rule caused the decision? | Hardcoded `WEEKLY_PROGRESSION` table at program_builder.py: ~570 |
| Which table caused the decision? | None. All progression rules are hardcoded. |
| Can the coach understand the reason? | **PARTIALLY.** The weekly progression (Base→Accumulation→Peak→Deload) is standard periodization. But the specific 75% → 80% → 85% → 60% values are unexplained. |
| Can the decision be reproduced exactly? | **YES** if the code never changes. But the `progression_rules` column in `program_design_rules` is TEXT (not executable), so the hardcoded values cannot be versioned or traced to configuration. |

**CRITICAL FAILURE:** Competition proximity (5 days away) is invisible to the progression logic. The program builder will generate Week 3 (Peak) at 85% intensity on competition day, which is dangerous.

---

### DECISION 9: Progression → Final Program

**Actual endpoint:** `program_builder.py`

**What actually happens:** The program builder assembles 4 weeks x N sessions with exercises, sets, reps, intensity, rest from the computed values. No validation that the program is safe given the athlete's current state. No validation that the program aligns with the competition calendar.

**Answer table:**

| Question | Answer |
|----------|--------|
| What data caused the decision? | Week focus, exercise class, baseline rep/set values |
| Which rule caused the decision? | Assembly logic at program_builder.py |
| Which table caused the decision? | `program_design_rules` (partially), `programs`, `program_weeks`, `program_sessions` |
| Can the coach understand the reason? | **PARTIALLY.** They see the 4-week structure. But "why 4 weeks and not 1 week (given competition in 5 days)?" is unanswerable. |
| Can the decision be reproduced exactly? | **NO — BLACK BOX.** Program `id` is auto-generated. No `regeneration_checksum` to verify identical output. Coach feedback refers to `recommendation_id` but the final program is disconnected from the recommendation. |

---

## SECTION B — EXPLAINABILITY SCORING

### Decision Trace Coverage

| Trace Step | Exists? | Traceable? | Reproducible? | Score |
|-----------|---------|-----------|---------------|-------|
| Assessment → Metric Deficit | YES | PARTIAL | YES (if norms versioned) | 6/10 |
| Metric Deficit → Demand Score (metric engine) | YES | PARTIAL | YES | 5/10 |
| Metric Deficit → Demand Score (demand engine) | YES | PARTIAL | PARTIAL | 4/10 |
| Demand Score → Gap Analysis | NO | N/A | N/A | 0/10 |
| Gap Analysis → Exposure Target | NO | N/A | N/A | 0/10 |
| Exposure Target → Objective Assignment | NO | N/A | N/A | 0/10 |
| Objective Assignment → Session Sequencing | NO | N/A | N/A | 0/10 |
| Session Sequencing → Exercise Selection | PARTIAL | PARTIAL | NO | 3/10 |
| Exercise Selection → Progression | PARTIAL | PARTIAL | PARTIAL | 3/10 |
| Progression → Final Program | PARTIAL | PARTIAL | NO | 2/10 |
| **Competition proximity influence** | **NO** | N/A | N/A | 0/10 |
| **ACWR/Readiness influence on selection** | **DUAL** | **NO** | **NO** | 1/10 |

### Explainability Score: 22/100

| Criterion | Score | Rationale |
|-----------|-------|-----------|
| **What** (what was decided?) | 6/10 | Outputs are explicit: demands scored, exercises ranked, program generated |
| **Why** (why this decision?) | 2/10 | Three scoring systems produce different values. Tiebreakers don't exist. Competition proximity ignored. |
| **How** (what rules applied?) | 3/10 | Rules are fragmented across 3 engines with different formulas. Key denominators are hardcoded. |
| **What if** (what if different choice?) | 0/10 | No alternative generation. No counterfactual trace. |
| **Reproduce** (same output from same input?) | 2/10 | No seed versioning. No config snapshots. Norm values unversioned. |
| **Audit trail** (can reconstruct later?) | 5/10 | recommendation_log captures snapshots. domain_events captures emissions. But audit trail cannot replay the program. |

---

## SECTION C — MISSING AUDIT TRAILS

| Missing Trail | Impact | Why It's Missing |
|---------------|--------|------------------|
| **Deficit normalization denominator provenance** | Coach cannot verify why 50cm is the CMJ max reference | Hardcoded at demand_scoring_engine.py:811 |
| **ACWR zone threshold provenance** | Coach cannot verify why 1.12 maps to adj=0.9 vs 1.0 | Hardcoded at demand_lifecycle_engine.py:180-185 |
| **Z-score severity mapping provenance** | Coach cannot verify why z=-1.8 → severity=0.6 | Hardcoded at assessment_metric_engine.py |
| **Level_multiplier provenance** | Coach cannot verify why PERFORMANCE = 1.0 vs FOUNDATION = 0.7 | Hardcoded at demand_scoring_engine.py:840 |
| **Exercise tiebreaker** | Coach cannot determine why Exercise A beat Exercise B at equal score | No tiebreaker rule exists |
| **Competition proximity** | No evidence that "5 days until competition" affected any decision | Competition domain is disconnected |
| **ACWR/Readiness integration** | No evidence that ACWR=1.12 or Readiness=74 affected exercise selection | Only used by demand_lifecycle_engine (separate endpoint) |
| **Program-to-recommendation link** | recommendation_id exists but final program table has no FK to it | No `recommendation_id` column in `programs` table |
| **Coach override rationale** | Coach changes exercise but reason is optional free-text | `coach_feedback.rationale` is nullable TEXT |
| **Decision tree record** | No single record of the full Assessment→Program decision path | No `decision_tree_nodes` table |
| **Configuration snapshot** | What config values were active when this program was generated? | No `config_snapshots` table |

---

## SECTION D — BLACK BOX RISKS

### Black Box #1: Two Deficit Systems (SEVERITY: CRITICAL)

```
assessment_metric_engine: CMJ z=-1.8 → deficit = 0.6
demand_scoring_engine:   CMJ=31.0  → deficit = 0.38
                              DIFFERENCE: 0.22 (37% error)
```

**Risk:** Coach investigates CMJ deficit, sees 0.6 in one API response and 0.38 in another. Trust is destroyed.

**Root cause:** Two independent deficit computations that don't share a common pipeline. The demand_scoring_engine was built before the assessment_metric_engine and was never updated to use its output.

### Black Box #2: Two Demand Scoring Systems (SEVERITY: CRITICAL)

```
demand_scoring_engine.get_demand_recommendations(): Vertical Power score = 138.0
demand_lifecycle_engine.compute_demand_states():    Vertical Power score = 24.87 (risk-adjusted)
                               DIFFERENCE: 113.13 (455% error)
```

**Risk:** The coach sees 138.0 in the recommendation response but the lifecycle engine would calculate 24.87. Which one is used for program generation? Neither — the V1 program builder uses its own template-based logic.

**Root cause:** The demand_lifecycle_engine and demand_scoring_engine are independent endpoints that are never combined. The program_builder uses the V1 recommendation engine, not either V2 endpoint.

### Black Box #3: Equal-Score Exercise Tiebreaker (SEVERITY: HIGH)

When 3 exercises score exactly 100.0 for Vertical Power, the ordering depends on insertion order in `exercise_demand_mappings`:

```python
"Trap Bar Jump Squat": [("Vertical Power", 10, True), ...]  # ← first
"Power Clean": [("Vertical Power", 10, True), ...]          # ← second
"Depth Jump": [("Vertical Power", 10, True), ...]           # ← third
```

**Risk:** A database reseeding or configuration reordering silently changes the top recommendation.

### Black Box #4: Competition Calendar Disconnection (SEVERITY: CRITICAL)

For an athlete with competition in 5 days:
- The demand_scoring_engine ranks exercises WITHOUT checking competition proximity
- The program_builder generates a 4-week block at 75% intensity IGNORING the competition
- Week 3 (Peak = 85% 1RM) lands exactly on competition day

**Risk:** Athlete performs maximal intensity training on competition day. Injury risk. Performance impairment.

**Root cause:** Competition proximity is NOT a parameter in any scoring function. The `competition_calendar` table may exist conceptually but is not JOINed in any query that affects program generation.

### Black Box #5: README vs Code Discrepancy (SEVERITY: HIGH)

The architecture documentation describes an integrated pipeline. The actual code has:

| Documented Feature | Actual Implementation |
|--------------------|---------------------|
| End-to-end V2 pipeline | V2 computes recommendations. V1 builds programs (different engine) |
| Exposure planning | Doesn't exist in code |
| Objective assignment | Doesn't exist in code |
| Session sequencing | Doesn't exist in code |
| Competition-aware planning | Competition calendar is conceptual only |
| Demand lifecycle feeds recommendations | Demand lifecycle is a SEPARATE API endpoint |

---

## SECTION E — REQUIRED EXPLAINABILITY IMPROVEMENTS

### E1. Unify Deficit Computation (SEVERITY: CRITICAL)

**Problem:** Two deficit systems produce different values for the same input.

**Fix (implementation-only, no architecture change):**
- Make `demand_scoring_engine.compute_deficit_factor()` read from `assessment_metric_engine`'s z-score-based deficits instead of recomputing from raw scores
- Or: delete the duplicate formula in demand_scoring_engine and route all deficit queries through assessment_metric_engine

**Traceability impact:** Single source of truth for deficit → explainable mapping from z-score to deficit severity.

### E2. Add Single-Score Integration (SEVERITY: CRITICAL)

**Problem:** Three scoring systems, three different scores for the same demand.

**Fix (implementation-only):**
- Remove the `demand_lifecycle_engine` scoring as a separate endpoint
- Fold ACWR/recovery/fatigue/injury-risk adjustments INTO the demand_scoring_engine's `compute_role_demand_scores()` function
- Single scoring pipeline: metric deficit → demand score (with state adjustments) → exercise rank

**Traceability impact:** One score to explain per demand per athlete.

### E3. Add Rule Provenance Recording (SEVERITY: HIGH)

**Problem:** Every hardcoded rule (normalization denominators, zone thresholds, level multipliers) has no explainable record.

**Fix (implementation-only):** For every scoring factor, emit a structured explanation record:

```python
# Current:
deficit_severity = 1.0 - min(score / 50.0, 1.0)

# Required:
RULES_CATALOG = {
    "cmj_deficit_denominator": {
        "value": 50.0,
        "reason": "50cm = 95th percentile for PERFORMANCE-level athletes",
        "source": "norm_data.jump_height.performance_95th_percentile",
        "version": "1.0.0"
    }
}
```

### E4. Add Competition Proximity Flag to Response (SEVERITY: HIGH)

**Problem:** Competition proximity is invisible.

**Fix (implementation-only):** Add to the recommendation response:
```json
{
  "competition_proximity_days": 5,
  "competition_overrides_applied": false,
  "reason": "Competition proximity (5 days) is within the 7-day red zone. Recommendation adjusted: no exercises exceeding RPE 7, reduced volume by 30%."
}
```

The override logic doesn't exist yet. The flag makes the gap visible rather than silent.

### E5. Add Tiebreaker Rule (SEVERITY: HIGH)

**Problem:** Equal-score exercises tied.

**Fix (implementation-only):** Deterministic tiebreaker:
```python
# Add to scoring:
secondary_sort = {
    "movement_pattern_variety": score_diversity(exercise, already_selected),
    "fatigue_impact": exercise_fatigue_cost(exercise),
    "alphabetical": exercise["name"],  # last resort
}
```

Record which tiebreaker was used in the recommendation_log.

### E6. Link Programs to Recommendations (SEVERITY: MEDIUM)

**Problem:** Final program has no FK to recommendation_id.

**Fix (implementation-only):**
```sql
ALTER TABLE programs ADD COLUMN recommendation_id UUID REFERENCES recommendation_log(recommendation_id);
```

This connects the final program output to the audit trail.

### E7. Add Config Snapshot on Program Generation (SEVERITY: MEDIUM)

**Problem:** Cannot reproduce a program from 6 months ago because configuration may have changed.

**Fix (implementation-only):**
```sql
ALTER TABLE recommendation_log ADD COLUMN config_snapshot JSONB;
-- Store: {demand_weights_version, norm_values_version, level_multiplier_version, engine_version}
```

---

## SECTION F — PRODUCTION READINESS VERDICT

### Explainability Readiness Score: 22/100

| Sub-Score | Value |
|-----------|-------|
| Decision trace coverage | 7/30 (3 of 10 trace steps exist) |
| Audit trail completeness | 5/20 (recommendation_log exists but disconnected) |
| Reproducibility | 4/20 (no config snapshots, no seed versioning) |
| Coach-facing explainability | 4/20 (hardcoded rules, dual systems, invisible tiebreakers) |
| Competition & state awareness | 2/10 (state factors exist in separate endpoint, competition absent) |

### Verdict: NOT RELEASABLE WITHOUT EXPLAINABILITY FIXES

**The engine can generate programs, but cannot explain them.** This violates FORGE's core value proposition: "Every generated decision should be explainable."

**To reach minimum explainability threshold (60/100):**

| Fix | Effort | Score Gain |
|-----|--------|------------|
| Unify deficit computation (E1) | 3-5 days | +15 |
| Single scoring integration (E2) | 5-10 days | +15 |
| Competition proximity flag (E4) | 2-3 days | +8 |
| Add tiebreaker rule (E5) | 1-2 days | +5 |
| Link programs to recommendations (E6) | 1 day | +5 |
| **Total** | **2-3 weeks** | **22 → 70** |

### Bottom Line

The codebase has three disconnected scoring systems, missing pipeline stages documented as existing, and zero competition-awareness in the actual scoring logic. A coach asking "why did the system prescribe this exercise today?" cannot get a coherent answer because the system's own internal components disagree with each other.

**The 22/100 score reflects that the system produces recommendations but cannot explain, reproduce, or audit them — which is the core promise of the entire FORGE platform.**
