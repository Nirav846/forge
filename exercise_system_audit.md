# Forge Exercise System Audit

**Author:** Principal S&C Architect  
**Date:** 2026-06-15  
**Scope:** Full-stack audit of database schema, migrations, seed data, template architecture, recommendation logic, and program builder.

---

## 1. Current Exercise Ontology Map

### 1.1 Entity-Relationship (as-deployed)

```
sports ──── roles ──── performance_drivers ──── driver_assessments ──── assessments
  │                                                                        │
  │                                                                  benchmarks
  │                                                                        │
  │                                                                   deficits ──── deficit_training_methods ──── training_methods
  │                                                                        │
  │                                                                  deficit_movement_templates ──── movement_templates
  │                                                                                                        │
movement_templates ──── template_slots ──── slot_requirements ──── movement_patterns
                        │                                            physical_qualities
                        │                                            equipment
                   slot_progressions                                  training_methods
                        │
                   slot_exercise_fallbacks ──── exercises
                                                  │
                                            exercise_equipment ──── equipment
                                            exercise_movement_patterns ──── movement_patterns
                                            exercise_physical_qualities ──── physical_qualities
                                            exercise_training_methods ──── training_methods
                                            exercise_sport_mapping ──── sports
                                            exercise_tags ──── tags
                                            exercise_muscles ──── muscles
```

### 1.2 Table Inventory

| Table | Rows (Seeded) | Purpose |
|---|---|---|
| `exercises` | **15** (DB) + 9 (mock-only) = **24 total** | Core exercise registry |
| `movement_templates` | 5 (general) + 1 (cricket) = **6** | Training templates |
| `template_slots` | 20 (4 per template × 5) + 4 (cricket) = **24** | Slot configurations |
| `slot_requirements` | 16 (general) + 4 (cricket) = **20** | Slot→exercise constraint rules |
| `slot_progressions` | 16 (general) + 4 (cricket) = **20** | Weekly progression envelopes |
| `slot_exercise_fallbacks` | **2** | Static substitution rules |
| `movement_patterns` | **10** | Squat, Hinge, Push/Pull, Lunge, Carry, Rotation, Anti-Rotation |
| `physical_qualities` | **8** | Max Strength, RFD, Hypertrophy, Aerobic, Anaerobic, LME, Mobility, Stability |
| `training_methods` | 9 (general) + 8 (cricket) = **17** | VBT, Cluster, Contrast, Plyo, Isometric, etc. |
| `equipment` | **10** | Barbell, Dumbbell, Kettlebell, Trap Bar, Cable, Bands, MB, Bodyweight, Foam Roller, Slide Board |
| `tags` | **8** | Primary Lift, Accessory, Warm-up, Rehab, Unilateral, Bilateral, Posterior Chain, Anterior Chain, Explosive |
| `muscles` | **0** (table exists, no seed) | Anatomical muscle groups |
| `movement_categories` | **DOES NOT EXIST** | Needed for exercise family grouping |
| `performance_drivers` | ~12 (cricket roles) | Role-specific physical demands |
| `assessments` | 4 (original) + 7 (cricket) = **11** | Testing protocols |
| `deficits` | 4 (original) + 5 (cricket) = **9** | Diagnosed weaknesses |

### 1.3 Exercise Count Gap

| Source | Count | Status |
|---|---|---|
| DB migrations | 15 | Persisted |
| `session_generator.py` mock | 24 | In-memory only (9 not in DB) |
| `recommendation_engine.py` mock | 14 | In-memory only (subset) |
| **Total unique exercises** | **24** | |
| **Target for recommendation-ready** | **150+** | **626% increase needed** |

---

## 2. Missing Exercise Metadata

### 2.1 Current `exercises` Table Columns

```sql
id              BIGINT        ✓
name            VARCHAR(255)  ✓  UNIQUE
description     TEXT          ✓
difficulty_level VARCHAR(50)  ✓  Beginner|Intermediate|Advanced|Elite
mechanics_type  VARCHAR(50)   ✓  Compound|Isolation|Static|N/A
force_type      VARCHAR(50)   ✓  Push|Pull|Hinge|Carry|Static|N/A
search_vector   tsvector      ✓  Full-text search
created_at      TIMESTAMPTZ   ✓
updated_at      TIMESTAMPTZ   ✓
```

### 2.2 Missing Columns

| Missing Field | Why Needed | Example Values | Risk of Absence |
|---|---|---|---|
| `technical_difficulty INT (1-10)` | Filter exercises by athlete skill; distinct from load-based `difficulty_level` | 3 (DB Jump Squat), 8 (Power Clean) | Unsafe exercise selection for novices; over-restrictive for elites |
| `training_age_months INT` | Minimum structured training experience required | 0 (A-Skip), 24 (Power Clean), 36 (Depth Jump) | Beginners prescribed high-skill Olympic lifts |
| `risk_score INT (1-5)` | Safety ceiling per competition level | 1 (Plank), 4 (Depth Jump), 5 (Power Clean miss) | Injury risk at scale; no filter for rehab populations |
| `is_olympic_lift BOOLEAN` | Separate Olympic lifts from derivatives for programming | TRUE for Power Clean, FALSE for Trap Bar Jump Squat | Cannot distinguish full lifts from safer derivatives |
| `movement_category_id FK` | Group exercises into families for slot assignment | Ballistic Strength, Plyometric, Olympic Derivative | Exercise pool is flat — no family-level reasoning |
| `is_competitive_lift BOOLEAN` | Mark exercises that ARE the sport (e.g., snatch for weightlifters) | TRUE for Power Clean (weightlifting), FALSE for most | Generic recommendation engine treats all exercises equally |

### 2.3 Missing Junction Tables

| Missing Junction | Why Needed | Example |
|---|---|---|
| `exercise_movement_categories` | Many-to-many: exercises can belong to multiple categories | Depth Jump → Plyometric + Ballistic Strength |
| `exercise_contraindications` | Exercises to avoid for specific injuries/conditions | Depth Jump contraindicated for patellar tendinopathy |
| `exercise_video_references` | Coaching cue references | URL or UUID linking to demonstration video |

---

## 3. Missing Exercise Families (Movement Categories)

The system has `movement_patterns` (biomechanical: Squat, Hinge, Push, Pull, etc.) but **no movement categories** (training intent: Olympic Derivative, Ballistic, Plyometric, etc.).

### 3.1 Current Pattern → No Category Mapping

| Movement Pattern | Used In | But Should Also Categorize As |
|---|---|---|
| Squat | Exercise matching | Ballistic Strength (Jump Squat), Max Strength (Back Squat), Unilateral Strength (Split Squat) |
| Hinge | Exercise matching | Olympic Derivative (Power Clean), Max Strength (Deadlift), Ballistic Strength (KB Swing) |
| Rotation | Exercise matching | Rotational Power (MB Throw), Core Stability (Pallof Press) |
| Lunge (Single-Leg) | Exercise matching | Unilateral Strength (RFE Split Squat), Sprint Mechanics (A-Skip) |

**Problem:** Two exercises sharing the same `movement_pattern` (Squat) but vastly different coaching intent, risk profile, and loading zones are treated identically by the recommendation engine.

### 3.2 Required Movement Categories

| Category | Training Zone | Example Exercises | Current Coverage |
|---|---|---|---|
| **Olympic Derivative** | Explosive/Strength Speed | Power Clean, Clean Pull, Hang Clean, Snatch Pull | **1 exercise** (Power Clean) |
| **Olympic Catch Variation** | Explosive/Strength Speed | Power Clean (Catch), Squat Clean, Power Snatch | **0** |
| **Olympic Overhead Variation** | Explosive/Strength Speed | Push Press, Snatch Balance, Overhead Squat, Jerk | **0** |
| **Ballistic Strength** | Explosive/Strength Speed | Trap Bar Jump Squat, Barbell Jump Squat, DB Jump Squat | **3** (some mock-only) |
| **Plyometric** | Explosive/Strength Speed | Depth Jump, Pogo Jump, Box Jump, Clap Push-Up | **1** (Depth Jump) |
| **Rotational Power** | Explosive/Strength Speed | MB Rotational Scoop Toss, MB Chest Pass, Cable Chop | **2** |
| **Max Strength** | Absolute Strength | Barbell Back Squat, Trap Bar Deadlift, Front Squat | **2** |
| **Unilateral Strength** | Absolute Strength | RFE Split Squat, Single-Leg RDL, Bulgarian Split Squat, Lunge | **2** |
| **Sprint Mechanics** | Sprint/Movement | A-Skip, Wall Drive, Wicket Drill, Resisted Sprint | **1** (A-Skip) |
| **Core Stability** | Hypertrophy/Stability | Pallof Press, Dead Bug, Plank, Farmer Walk | **3** |
| **Shoulder Robustness** | Corrective/Prehab | YTWL, Face Pull, External Rotation Hold, Band Pull-Apart | **0** dedicated |

**Coverage gap:** Only 4 of 11 categories have ≥2 exercises. 3 categories have zero exercises.

---

## 4. Missing Olympic Lift Support

### 4.1 Current State

Only **1 Olympic lift** exists in the entire system: `Power Clean` (seeded in migration 000002). No snatch, no jerk, no clean & jerk, no hang variations, no block variations.

### 4.2 Required Olympic Exercise Families

| Exercise | Category | Priority | Load Zone | Risk Score | Notes |
|---|---|---|---|---|---|
| Power Clean | Olympic Derivative | **Critical** | 70-90% 1RM | 4 | Already exists. Add `technical_difficulty=8`, `training_age_months=24` |
| Hang Power Clean | Olympic Derivative | **Critical** | 60-80% 1RM | 3 | Safer entry point than floor. Required for intermediate athletes |
| Clean Pull | Olympic Derivative | **Critical** | 90-110% 1RM | 3 | Max strength variant. No catch risk |
| Power Snatch | Olympic Derivative | High | 60-80% 1RM | 5 | Full overhead mobility required |
| Snatch Pull | Olympic Derivative | High | 80-100% 1RM | 3 | No catch risk. Broad + narrow grip variants |
| Hang Snatch | Olympic Derivative | Medium | 50-70% 1RM | 4 | Transitional |
| Push Press | Olympic Overhead | **Critical** | 60-80% 1RM | 2 | Key overhead strength builder |
| Split Jerk | Olympic Overhead | Medium | 70-85% 1RM | 4 | Advanced footwork |
| Power Clean + Push Press | Olympic Derivative + Overhead | Medium | 60-75% 1RM | 3 | Complex — sport-specific for throwers |
| Snatch Balance | Olympic Overhead | Medium | 50-70% 1RM | 4 | Overhead stability. Drill, not max load |
| Muscle Snatch | Olympic Derivative | Low | 40-60% 1RM | 2 | Technique primer |
| Clean High Pull | Olympic Derivative | High | 80-100% 1RM | 2 | Max power output, zero catch risk |

### 4.3 Risk Without Olympic Support

| Missing Capability | Impact |
|---|---|
| No snatch family | Cannot program for weightlifting or throwers |
| No clean pull | Loses the highest power-output exercise (clean pull develops more power than any jump) |
| No push press | Overhead strength is limited to DB OHP and static press |
| No hang variations | Intermediate athletes cannot safely progress to full lifts |
| No technique ladder | No progression path: Hang Clean → Power Clean → Squat Clean |

---

## 5. Missing Substitution Support

### 5.1 Current State

- `slot_exercise_fallbacks` table exists with **only 2 rows** (Barbell Back Squat ↔ Trap Bar Deadlift, Power Clean ↔ Kettlebell Swing)
- Program builder uses `pool[(s_num - 1) % len(pool)]` modulo arithmetic — no explicit default, no ranked fallback
- Mock repositories hardcode exercise pools per slot — no dynamic substitution

### 5.2 Missing Capabilities

| Capability | Current | Required |
|---|---|---|
| Default exercise per slot | Implicit (`pool[0]`) | Explicit `template_slots.default_exercise_id` column |
| Tiered fallback chain | `slot_exercise_fallbacks` has only 2 rows | 150+ exercises → meaningful substitution chains per slot |
| Same-category substitution | Not supported | Substituting Trap Bar Jump Squat → Barbell Jump Squat must keep progression envelope |
| Cross-category substitution | Not supported | Substituting Power Clean → Trap Bar Deadlift must trigger intensity/rep adjustment |
| Equipment-aware substitution | Not supported | If Trap Bar unavailable → substitute Barbell Jump Squat (≠ DB Jump Squat which needs dumbbells) |
| Difficulty-aware substitution | Not supported | If athlete is "Intermediate" → skip Depth Jump (Elite) in pool |
| Risk-aware substitution | Not supported | If athlete is "Beginner" → cap risk_score at 2 |

### 5.3 Substitution Matrix (Required Pattern)

```
Primary Slot "Max Dynamic Output (Bilateral)" — Category: Ballistic Strength

  Default: 
    Trap Bar Jump Squat (score 99, risk 2, tech_diff 4, equip: Trap Bar, diff: Advanced)
  
  Same-category fallbacks (Ballistic Strength):
    1. Barbell Jump Squat   (score 94, risk 3, tech_diff 6, equip: Barbell, diff: Advanced)
    2. DB Jump Squat         (score 88, risk 2, tech_diff 3, equip: Dumbbell, diff: Intermediate)
    3. Broad Jump            (score 82, risk 2, tech_diff 2, equip: Bodyweight, diff: Beginner)
  
  Cross-category fallback (Max Strength — same movement pattern, different zone):
    4. Barbell Back Squat    (score 75, risk 2, tech_diff 3, equip: Barbell, diff: Intermediate)
       ⚠ Warning: Changes loading zone from VBT to %1RM. Progression envelope must update.
  
  Conditional filters applied at query time:
    × Depth Jump             (risk 5 > Elite ceiling → excluded)
    × Power Clean            (tech_diff 8 > athlete capability → excluded)
    × Bulgarian Split Squat  (equipment: Dumbbell required → excluded if not available)
```

---

## 6. Migration Plan (150+ Exercise Ready Database)

### 6.1 Recommended Migrations — Implementation Order

### Phase 1: Schema Foundation (Migrations 019–020)

**Migration 019 — `movement_categories` + exercise metadata**

| Step | DDL | Backward Compat? |
|---|---|---|
| 1.1 | `CREATE TABLE movement_categories (id, name, description, training_zone, risk_baseline)` | Yes (new table) |
| 1.2 | `ALTER TABLE exercises ADD COLUMN technical_difficulty INT DEFAULT 5` | Yes (default) |
| 1.3 | `ALTER TABLE exercises ADD COLUMN training_age_months INT DEFAULT 0` | Yes (default) |
| 1.4 | `ALTER TABLE exercises ADD COLUMN risk_score INT DEFAULT 3` | Yes (default) |
| 1.5 | `CREATE TABLE exercise_movement_categories (exercise_id FK, category_id FK)` | Yes (new table) |
| 1.6 | `ALTER TABLE template_slots ADD COLUMN movement_category_id FK` | Yes (nullable) |
| 1.7 | `ALTER TABLE template_slots ADD COLUMN default_exercise_id FK` | Yes (nullable) |
| 1.8 | Index: `idx_exercise_mvmt_cat`, `idx_template_slots_cat`, `idx_template_slots_default` | Yes |

**Migration 020 — Muscles seed + exercise_contraindications**

| Step | DDL | Backward Compat? |
|---|---|---|
| 2.1 | `INSERT INTO muscles` (30+ muscles across Lower Body, Upper Body - Push, Upper Body - Pull, Core) | Yes (data only) |
| 2.2 | `CREATE TABLE exercise_contraindications (exercise_id FK, condition VARCHAR, severity ENUM)` | Yes (new table) |
| 2.3 | Index: `idx_exercise_contraindications` | Yes |

### Phase 2: Seed Data Blast (Migrations 021–022)

**Migration 021 — Movement categories + backfill existing exercises**

| Step | Count | Description |
|---|---|---|
| 3.1 | 11 rows | INSERT 11 movement categories |
| 3.2 | 24 rows | Map all 24 existing exercises to categories via `exercise_movement_categories` |
| 3.3 | 24 rows | UPDATE `exercises` SET `technical_difficulty`, `training_age_months`, `risk_score` |
| 3.4 | 24 rows | UPDATE `template_slots` SET `movement_category_id` |
| 3.5 | 24 rows | UPDATE `template_slots` SET `default_exercise_id` (top-ranked per slot) |

**Migration 022 — 150 exercise seed (the bulk)**

Exercise breakdown by category:

| Category | Current | Target | New Needed | Priority |
|---|---|---|---|---|
| **Ballistic Strength** | 3 | 20 | 17 | Critical |
| **Max Strength** | 2 | 20 | 18 | Critical |
| **Unilateral Strength** | 2 | 15 | 13 | Critical |
| **Rotational Power** | 2 | 15 | 13 | Critical |
| **Plyometric** | 1 | 15 | 14 | High |
| **Olympic Derivative** | 1 | 12 | 11 | High |
| **Olympic Overhead** | 0 | 8 | 8 | High |
| **Olympic Catch Variation** | 0 | 6 | 6 | Medium |
| **Sprint Mechanics** | 1 | 15 | 14 | Critical |
| **Core Stability** | 3 | 15 | 12 | High |
| **Shoulder Robustness** | 0 | 12 | 12 | Critical |
| **Total** | **15** | **153** | **138 new** | |

Each exercise seeded with:
- `exercises` row (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, training_age_months, risk_score)
- `exercise_equipment` (1–3 rows)
- `exercise_movement_patterns` (1–2 rows)
- `exercise_physical_qualities` (1–3 rows with relevance_score)
- `exercise_training_methods` (1–2 rows)
- `exercise_sport_mapping` (3–6 rows with specificity_rating + transfer_index)
- `exercise_tags` (1–3 rows)
- `exercise_movement_categories` (1 row)
- `exercise_muscles` (2–4 rows)

### Phase 3: Template Expansion (Migration 023)

| Step | Current | Target | Notes |
|---|---|---|---|
| Movement templates | 6 | 12 | Add per-sport versions for Cricket (Batter, Spinner, WK, All Rounder) |
| Template slots | 24 | 48 | 4 per template × 12 templates |
| Slot requirements | 20 | 48 | One per slot |
| Slot progressions | 20 | 48 | One per slot |
| Slot exercise fallbacks | 2 | 200+ | 3–5 tiered fallbacks per slot |

New templates required:

| Template | Sport | Slots |
|---|---|---|
| Cricket Batter Power | Cricket | 4 |
| Cricket Spinner Rotational | Cricket | 4 |
| Cricket Wicket Keeper Agility | Cricket | 4 |
| Cricket All Rounder Conditioning | Cricket | 4 |
| Lower Body Strength (Max) | Multi-sport | 4 |
| Upper Body Strength | Multi-sport | 4 |
| Sprint & Acceleration | Multi-sport | 4 |

### Phase 4: Mock Repository Parity (No migration — code change)

Sync all four in-memory mocks to match new schema:

| Repository | Must Support |
|---|---|
| `MockBenchmarkRepository` | Physical driver → deficit resolution |
| `MockExerciseRepository` | Category filtering, risk filtering, training age filtering, `default_exercise` |
| `MockKnowledgeGraphRepository` | All 11 assessment → physical driver mappings |
| `MockProgramRepository` | Staged program storage, swap preview |

### 6.2 Total Migration Size Estimate

| Migration | Tables Created | Columns Added | Rows Inserted | Risk |
|---|---|---|---|---|
| 019 | 2 | 5 | 0 | Low |
| 020 | 1 | 0 | 30 | Low |
| 021 | 0 | 0 | 24 + 24 + 24 + 24 + 24 = 120 | Low |
| 022 | 0 | 0 | ~138 exercises × ~12 junction rows = ~1,656 | Medium |
| 023 | 0 | 0 | ~200 fallback rows + template/slot/progression data | Low |
| **Total** | **3** | **5** | **~2,000 rows** | |

---

## 7. Schema Findings Summary

### 7.1 What Works Well

| Feature | Assessment |
|---|---|
| Junction table pattern | Excellent. `exercise_equipment`, `exercise_movement_patterns`, `exercise_physical_qualities`, etc. are well-normalized and indexed |
| `search_vector` tsvector | Production-ready full-text search |
| `slot_exercise_fallbacks` design | Correct schema (preferred→fallback with rank). Just underpopulated (2 rows) |
| `slot_progressions` | Correct 1:1 with template_slots. Contains intensity, volume, progression rules, deload protocol |
| `program_session_exercises` | Stores sets/reps/intensity/rest per exercise instance — enables per-instance substitution |
| Trigger-based `updated_at` | Consistent across all tables |

### 7.2 What Needs Immediate Attention

| Finding | Severity | Fix |
|---|---|---|
| **No movement categories** | Critical | Migration 019 |
| **No exercise risk/training-age metadata** | Critical | Migration 019 |
| **Only 15 exercises in DB (goal: 150+)** | Critical | Migration 022 |
| **Only 2 substitution fallback rows** | High | Migration 023 |
| **Olympic lifts: only Power Clean exists** | High | Migration 022 |
| **No Shoulder Robustness exercises** | High | Migration 022 |
| **No explicit default_exercise per slot** | High | Migration 019 (column) + code change |
| **Muscles table empty (seeded no data)** | Medium | Migration 020 |
| **Mock repos diverge from DB schema** | Medium | Phase 4 code sync |
| **Mock exercises not in DB (9 orphans)** | Medium | Migration 022 or code consolidation |
| **No exercise_contraindications** | Medium | Migration 020 |
| **`ASSESSMENT_UNITS` dict hardcoded in Python** | Low | Could be data-driven from `assessments.metric_unit` |
| **`deficit_template_map` hardcoded in Python** | Low | Should be data-driven via `deficit_movement_templates` |

### 7.3 Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Migration 022 (150 exercises) creates merge conflicts with ongoing dev** | High | Medium | Seed as a single migration with `ON CONFLICT DO NOTHING`. Exercisel-level idempotent inserts |
| **Mock repos must be kept in sync with DB** | High | Medium | Introduce a `MockDataGenerator` class that reads from seed JSON fixtures rather than duplicating data in Python |
| **`technical_difficulty` + `difficulty_level` confusion** | Medium | Low | Document: `difficulty_level` = load/intensity domain (Beginner–Elite). `technical_difficulty` = coordination/skill axis (1–10). Both required for safe filtering |
| **Risk score is subjective across coaches** | Medium | Low | Publish a risk-score rubric in ADR. Use `program_design_rules` + `sports_science_rules` JSONB as override mechanism |
| **150 exercises × 12 junction tables = 1,800 INSERTs per environment** | Low | Medium | Wrap in `DO $$ BEGIN ... END $$` block. Use CTEs for subqueries. ~2s execution time |

---

## 8. Implementation Order

### Critical Path (Weeks 1–2)

```
Week 1:
  ├── Migration 019: movement_categories + exercise metadata columns
  ├── Migration 020: muscles seed + contraindications
  ├── Sync MockBenchmarkRepository → physical driver aware
  └── Backfill template_slots.default_exercise_id in mocks

Week 2:
  ├── Migration 021: category mappings + metadata backfill
  ├── Migration 022: 138 new exercises (Ballistic + Max Strength + Unilateral + Rotational Power + Sprint Mechanics + Shoulder Robustness)
  └── Sync MockExerciseRepository → category-aware + metadata-aware filtering
```

### Secondary Path (Weeks 3–4)

```
Week 3:
  ├── Migration 023: template expansion (6→12), slot expansion, 200 fallback rows
  ├── Olympic lift family: Hang Clean + Clean Pull + Snatch family (18 exercises)
  └── Plyometric family: Box Jumps, Pogos, Hurdle Hops (15 exercises)

Week 4:
  ├── Olympic Catch + Overhead variations (14 exercises)
  ├── Core Stability family expansion (12→15 exercises)
  └── Full regression: all mock repos → DB schema parity
```

### Final Verification

```
  ├── Run: ALL 7 test files pass
  ├── Run: Full diagnostic chain: Assessment → Physical Driver → Deficit → Template → Category → Pool → Default
  ├── Run: Equipment-aware filtering (3 equipment sets, verify excluded exercises)
  ├── Run: Risk-aware filtering (Beginner vs Elite — verify Depth Jump excluded for Beginner)
  ├── Run: Training-age filtering (0mo vs 36mo — verify Power Clean excluded for 0mo)
  └── Run: Substitution chain (verify all 5 fallback tiers for each primary slot)
```

---

## Appendix A: Current Mock-Only Exercises (Not in DB)

These 9 exercises exist in Python mocks but have no database rows. Must be seeded in Migration 022.

| Exercise | Appears In | Category |
|---|---|---|
| Barbell Jump Squat | `recommendation_engine.py` | Ballistic Strength |
| DB Jump Squat | `recommendation_engine.py` | Ballistic Strength |
| Medicine Ball Slam | `session_generator.py` | Rotational Power |
| Bodyweight Squat | `session_generator.py` | Max Strength |
| Farmer's Walk | `session_generator.py` | Core Stability |
| Burpee | `session_generator.py` | Plyometric |
| Dumbbell Row | Both | Shoulder Robustness |
| Dumbbell Overhead Press | Both | Shoulder Robustness |
| Plank with Rotation | Both | Core Stability |

## Appendix B: Current DB-Only Exercises (15)

| # | Exercise | Category | Source Migration |
|---|---|---|---|
| 1 | Barbell Back Squat | Max Strength | 000002 |
| 2 | Power Clean | Olympic Derivative | 000002 |
| 3 | Rear Foot Elevated Split Squat | Unilateral Strength | 000002 |
| 4 | Trap Bar Deadlift | Max Strength | 000002 |
| 5 | Kettlebell Swing | Ballistic Strength | 000002 |
| 6 | Depth Jump | Plyometric | 000002 |
| 7 | Medicine Ball Rotational Scoop Toss | Rotational Power | 000002 |
| 8 | A-Skip | Sprint Mechanics | 000002 |
| 9 | Single-Leg Isometric Wall Sit | Core Stability | 000002 |
| 10 | Nordic Hamstring Curl | Unilateral Strength | 000002 |
| 11 | Trap Bar Jump Squat | Ballistic Strength | 000005 |
| 12 | Single-Leg Lateral Bound | Unilateral Strength | 000005 |
| 13 | Medicine Ball Overhead Backwards Toss | Rotational Power | 000005 |
| 14 | Medicine Ball Rotational Chest Pass | Rotational Power | 000005 |
| 15 | Cable Pallof Press with Rotation | Core Stability | 000005 |

## Appendix C: Scoring Algorithm Gaps

Current recommendation score formula (from `recommendation_engine.py:506`):

```python
score = (
    comp["relevance"] * 0.40 * 10.0 +      # 40% — physical quality relevance
    comp["specificity"] * 0.30 * 10.0 +     # 30% — sport specificity
    comp["transfer"] * 20.0 +               # 20% — transfer index
    comp["mechanics_bonus"] +               #  5% — mechanics alignment
    comp["tag_bonus"]                       #  5% — tag matching
)
```

**What's missing from the score:**

| Missing Factor | Weight | Why |
|---|---|---|
| **Equipment availability** | Gate (0 or 1) | Exercise is excluded, not scored down |
| **Technical difficulty vs athlete** | Gate | Excluded if `technical_difficulty > competition_level_cap` |
| **Training age** | Gate | Excluded if `athlete.training_age_months < exercise.training_age_months` |
| **Risk score vs competition level** | Gate | Excluded if `risk_score > risk_ceiling[competition_level]` |
| **Injury contraindication** | Gate | Excluded if athlete has recorded condition |
| **Movement category alignment** | +10% | Bonus if slot movement_category matches exercise's primary category |
| **Exercise variety (past N sessions)** | −5% per repeat | Penalty if same exercise was used in last 3 sessions |
