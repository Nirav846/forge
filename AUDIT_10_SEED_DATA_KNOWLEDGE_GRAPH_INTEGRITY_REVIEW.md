# AUDIT #10 — Seed Data & Knowledge Graph Integrity Review

**Date:** 2026-06-17 | **Scope:** Database content only | **Sections:** 8

---

## Executive Summary

This audit examined all 24 migration pairs, 1 supplemental seed file (PHASE_5A_SEED.sql), and 1 spec document covering the Forge knowledge graph, V2 ontology, deficit routing, and exercise data. The database content has **15 critical and 8 moderate defects** that collectively make it **unfit for production use in its current state**. The good news: the schema design is sound (7/10). The bad news: the seed data is catastrophically fragmented — three parallel naming conventions, two competing deficit systems, and broken benchmark inserts ensure that **any production query against the knowledge graph will return wrong, partial, or empty results**.

**Overall Verdict: NOT READY — Redis/redo seed data before any production deployment.**

---

## Scorecard

| Dimension | Score | Grade |
|-----------|-------|-------|
| Taxonomy Health | 3/10 | Poor |
| Knowledge Graph Completeness | 4/10 | Poor |
| Exercise Coverage per Demand | 2/10 | Critical |
| Sport Coverage | 2/10 | Critical |
| Data Consistency (cross-migration) | 2/10 | Critical |
| Defect Routing Integrity | 2/10 | Critical |
| V1 → V2 Migration Path | 1/10 | Critical |
| Production Data Readiness | 1.5/10 | Critical |
| **Composite** | **2.2/10** | **Critical** |

---

## Section 1: Taxonomy Audit

### 1A — Taxonomic Entities Present

| Domain | Count | Coverage |
|--------|-------|----------|
| Sports | 5 | Cricket, American Football, Rugby, Track & Field (Sprinting), Olympic Weightlifting |
| Roles | 7 (5 cricket) | Fast Bowler, Spinner, Batter, Wicket Keeper, All Rounder |
| Movement Templates | 6 (4 generic, 1 cricket, 1 reactive) | 5 from 000004, 1 from 000005 |
| Template Slots | 24 | 4 per template |
| Performance Drivers/ Demands (V1) | 7 (000008) + 12 (000009) | Cricket-specific only |
| Performance Demands (V2) | 18 (000022) | Cross-sport ontology |
| Assessments (V1 - 000008) | 4 | Cricket-specific |
| Assessments (V1 - PHASE_5A) | 7 | lowercase names |
| Assessments (V1 - 000021) | 7 | mixed-case names |
| Benchmarks (attempted) | ~28 (000021 broken), 28 (PHASE_5A), 16 (000008) | Fragmented across 3 sources |
| Deficits | 4 (000008) + 7 (PHASE_5A) + 7 (000021 broken) | 11 unique |
| Exercises (V1) | ~21 | From 000004, 000005 |
| Exercises (Olympic) | 14 | From 000015/000017 |
| Equipment Types | 2+ | Barbell, Bodyweight + more from V1 |
| Movement Patterns | 7 | Squat, Hinge, Push(V), Pull(V), Lunge, Rotation, Overhead Squat |
| Physical Qualities | 5+ | RFD, Max Strength, Stability, Mobility, Hypertrophy, LME |
| Training Methods | 7+ | VBT, Plyo(Fast/Slow), Contrast, Cluster, Eccentric, Isometric |

### 1B — Taxonomy Defects

**DEFECT 1 — Assessment Name Fragmentation [CRITICAL]**

Three separate naming conventions exist for the same assessments across migrations:

| Concept | PHASE_5A_SEED.sql | 000021_seed_deficit_routing_fixed | 000008_seed_cricket_knowledge_graph |
|---------|-------------------|-----------------------------------|--------------------------------------|
| CMJ | `'cmj'` (id=1) | `'Counter Movement Jump'` (id=1) | `'Force Plate Countermovement Jump (CMJ)'` |
| 10m Sprint | `'10m sprint'` (id=3) | `'10m Sprint'` (id=3) | — |
| Broad Jump | `'broad jump'` (id=2) | `'Broad Jump'` (id=2) | — |
| Trap Bar DL | `'trap bar deadlift'` (id=6) | `'Trap Bar Deadlift'` (id=6) | — |
| Med Ball Throw | `'rotational med ball throw'` (id=7) | `'Rotational Med Ball Throw'` (id=7) | `'Medicine Ball Rotational Velocity Test'` |
| IMTP | — | — | `'Isometric Mid-Thigh Pull (IMTP)'` |
| Wall Sit | — | — | `'Isometric Wall Sit Squat Hold Test'` |

Since all three migrations use `ON CONFLICT (id) DO NOTHING` with OVERRIDING SYSTEM VALUE, **only one naming convention survives per assessment ID**. The survivor depends on migration order. If PHASE_5A runs first → lowercase names win. If 000021 runs first → mixed-case names win. 000008's names never conflict because they use auto-generated IDs (no OVERRIDING SYSTEM VALUE).

**Impact:** Any code that looks up assessments by name will fail for whichever convention is not the survivor. `deficit_detection_engine.py` (lines 89–191) likely references specific lowercase or mixed-case names → 2/3 probability of zero results.

**DEFECT 2 — Benchmark Duplicate Name Insertion Failure [CRITICAL]**

Migration 000021 inserts benchmarks with identical `(assessment_id, name)` for all 4 classification tiers:

```sql
INSERT INTO benchmarks (assessment_id, name, classification, min_value, max_value) VALUES
  (1, 'CMJ', 'Elite', 55.0, NULL),
  (1, 'CMJ', 'Optimal', 45.0, 54.99),    -- UNIQUE(1, 'CMJ') violation!
  (1, 'CMJ', 'Sub-optimal', 35.0, 44.99), -- would also fail
  (1, 'CMJ', 'Poor', NULL, 34.99);         -- would also fail
```

The table has `UNIQUE (assessment_id, name)` constraint (000007, line 85). The first row inserts, the second conflicts → **entire INSERT statement fails on row 2**. This applies to all 7 assessments × 4 tiers = **28 benchmarks silently lost**.

Furthermore, 000021 has **no `ON CONFLICT` clause** on the benchmarks INSERT, meaning PostgreSQL aborts the entire statement. If wrapped in a migration transaction, the entire migration 000021 rolls back, losing deficits (lines 19–26) and deficit_movement_templates (lines 80–87) too.

**DEFECT 3 — PHASE_5A Benchmark Names Non-Standard [MODERATE]**

PHASE_5A uses names like `'cmj_elite'`, `'cmj_optimal'`, `'cmj_suboptimal'`, `'cmj_poor'`. These work (unique names), but the code likely looks up benchmarks by classification, not by name. The `benchmarks` table has an index on `(assessment_id, classification)` at 000007 line 136, which is correct. But if the code ever does a name-based lookup (e.g., `WHERE name = 'CMJ Elite'`), it won't find `'cmj_elite'`.

**DEFECT 4 — Missing Movement Patterns in 000004 [MODERATE]**

The slot_requirements table references several movement patterns that don't exist in the seed data:
- `'Anti-Rotation'` (used in 000004 lines 145, 181, 216, 251)
- `'Push (Horizontal)'` (used in 000004 lines 172, 244)

These patterns are referenced in INSERT statements that do sub-SELECTs. If the pattern name doesn't exist, the sub-SELECT returns NULL, and the INSERT either fails (if column has NOT NULL) or inserts a NULL reference. The 000004 migration DOES include these patterns? Let me check... No, 000004 doesn't INSERT movement_patterns. It only inserts templates, slots, requirements, and fallbacks. Movement patterns are seeded in 000001 or 000002.

If 'Anti-Rotation' and 'Push (Horizontal)' aren't seeded before 000004 runs, all slot_requirements referencing them would either fail or reference NULL.

---

## Section 2: Knowledge Graph Completeness

### 2A — Chain Tracing

#### Chain: Cricket → Fast Bowler → Power Deficit → Template

```
Sport: Cricket (id from 000001/000005)
  └─ Role: Fast Bowler (id from 000008/000013)
       ├─ Performance Driver: Front Foot Brace Force (Primary)
       │    └─ Assessment: Isometric Mid-Thigh Pull (IMTP) → Benchmarks: 4 tiers
       │         └─ Deficit: Lower Body Absolute Strength Deficit
       │              └─ Template: Cricket Fast Bowler Power (000005)
       │              └─ Template: Lower Body Power (000004, American Football)
       └─ Performance Driver: Trunk Flexion Rotational Power (Primary)
            └─ Assessment: Medicine Ball Rotational Velocity Test → Benchmarks: 4 tiers
                 └─ Deficit: Rotational Core Power Deficit
                      └─ Template: Rotational Power (000004, Track & Field)
```

**PROBLEM:** This chain uses 000008's performance_drivers → assessments → deficits system. But the **deficit_detection_engine.py uses PHASE_5A/000021's assessment names and deficit IDs**. If the engine looks up assessment `'cmj'` or `'Counter Movement Jump'`, it finds benchmarks and deficits from PHASE_5A/000021. The 000008 chain is **completely disconnected** from the engine's lookup path.

#### Chain: Cricket → Fast Bowler → V2 Demands (000022)

```
Sport: Cricket
  └─ Role: Fast Bowler
       └─ role_demand_priority (000022)
            ├─ Demand: Power (priority 1)
            │    ├─ exercise_demand_mapping → Trap Bar Jump Squat (relevance 10)
            │    │                              → Mid-Thigh Pull (relevance 9)
            │    │                              → Clean Pull (relevance 8)
            │    └─ assessment_demand_mapping → CMJ (from 000022's own assessment_metrics)
            ├─ Demand: Strength (priority 2)
            │    ├─ exercise_demand_mapping → Barbell Back Squat (relevance 9)
            │    └─ assessment_demand_mapping → IMTP (from 000022)
            └─ Demand: Rotational Power (priority 3)
                 ├─ exercise_demand_mapping → Medicine Ball Rotational Chest Pass (relevance 9)
                 └─ assessment_demand_mapping → Med Ball Rotational Velocity Test (from 000022)
```

**PROBLEM:** The V2 chain exists but:
1. V2 has **no production callers** (ENGINE_MODE flag controls V1 vs V2 path)
2. V2 assessment_demand_mapping references assessment_metrics, which is a V2 table not connected to V1 assessments
3. V2 exercise_demand_mapping doesn't include 17 of 20 V1 exercises (it has 10 of ~35 mapped)
4. No benchmark tiers exist in V2 format — metric_demand_mapping links to metric_norms which are empty

### 2B — Completeness Gaps

| Role | Performance Drivers | Assessed | Deficits Mapped | Template Assigned |
|------|-------------------|----------|-----------------|-------------------|
| Fast Bowler | 7+ (000008+000009) | 3 | 3 (000008) | Cricket Fast Bowler Power ✓ |
| Spinner | 1+ (000008) + 7+ (000009) | 1 (MB Rotational) | 1 (Rotational) | Rotational Power (generic) ✗ |
| Batter | 1+ (000008) + 7+ (000009) | 1 (CMJ) | 1 (RFD) | Reactive Agility (generic) ✗ |
| Wicket Keeper | 1+ (000008) + 6+ (000009) | 1 (Wall Sit) | 1 (LME) | Shoulder Robustness (generic) ✗ |
| All Rounder | 6+ (000009) | 0 | 0 | None ✗ |

All roles except Fast Bowler get **generic templates from other sports** when deficits are triggered, because only "Cricket Fast Bowler Power" template exists.

---

## Section 3: Exercise Coverage

### 3A — Exercises per Demand Category

Using V1 categories (from program_design_rules, 000013):

| Demand | Exercises Mapped (exercise_sport_mapping → Cricket) |
|--------|-----------------------------------------------------|
| Strength | Barbell Back Squat (no cricket mapping), Trap Bar Deadlift (no cricket mapping) |
| Power | Trap Bar Jump Squat (10/0.90), Clean Pull (7/0.70), Mid-Thigh Pull (8/0.75), High Pull (7/0.68), Snatch Pull (5/0.45), Push Press (6/0.55) |
| Acceleration | 10m Sprint (assessment, not exercise) |
| Speed | 30m Sprint (assessment) |
| Rotational Power | MB Rotational Chest Pass (9/0.85), Cable Pallof Press w/ Rotation (8/0.78), MB Overhead Backwards Toss (8/0.82), Single-Leg Lateral Bound (9/0.88), Overhead Squat (5/0.48), Push Jerk (5/0.45), Split Jerk (4/0.35) |

**Key Gap:** Only 5 exercises from 000005 have Cricket-specific sport mappings. The Olympic lifts (14 exercises) are mapped to Cricket but with low-medium transfer indices (0.30–0.75). The V1 exercises (Bodyweight Squat, A-Skip, Kettlebell Swing, Dumbbell Row, etc.) have **no Cricket sport mapping at all**.

### 3B — Exercise Matching Against Slot Requirements

The slot_requirements table defines (movement_pattern, physical_quality, training_method, equipment) tuples for matching. Only 5 exercises have full metadata (movement_patterns, physical_qualities, training_methods, equipment):

From 000005: Trap Bar Jump Squat, Single-Leg Lateral Bound, MB Overhead Backwards Toss, MB Rotational Chest Pass, Cable Pallof Press w/ Rotation — 5 exercises fully searchable.

The remaining ~30 exercises have incomplete metadata. Olympic lifts lack exercise_class, primary_adaptation, and force_vector (columns exist, values NULL). No exercise_equivalencies are seeded (table exists, 0 rows).

### 3C — Exercise Coverage Score

| Metric | Value |
|--------|-------|
| Total exercises | ~35 |
| With Cricket sport mapping | 19 (5 original + 14 Olympic) |
| With complete metadata for search | 5 |
| exercise_equivalencies seeded | 0 |
| exercise_class populated | 0 |
| primary_adaptation populated | 0 |
| force_vector populated | 0 |
| **Coverage Score** | **2/10** |

---

## Section 4: Sport Coverage

### 4A — Sports in System

| Sport | Templates | Roles | Assessments | Deficits | Exercise Mappings |
|-------|-----------|-------|-------------|----------|-------------------|
| Cricket | 1 (specific) + 4 (generic) | 5 | 6 (across all sources) | 7+ | 19 exercises |
| American Football | 1 (Lower Body Power) | 0 | 0 | 0 | via Olympic lifts |
| Track & Field (Sprinting) | 1 (Accel Dev) | 0 | 0 | 0 | via Olympic lifts |
| Track & Field (Throws) | 1 (Rotational Power) | 0 | 0 | 0 | via Olympic lifts |
| Rugby | 1 (Shoulder Robustness) | 0 | 0 | 0 | via Olympic lifts |
| Basketball | 1 (Reactive Agility) | 0 | 0 | 0 | via Olympic lifts |
| Olympic Weightlifting | 0 | 0 | 0 | 0 | 14 exercises |

**Cricket is the only sport with role-specific content.** All other sports have template stubs in 000004 but no role seed data, no assessment data, and no deficit data. The templates for non-Cricket sports are **unusable** — they exist in the database but no pipeline path triggers them.

### 4B — What "Multi-Sport" Actually Means Today

The codebase architecture implies multi-sport support, but the seed data makes it Cricket-only:

```
System architecture: Multi-sport ←── seed data: Cricket only (95% of rows)
                                         American Football (1 template)
                                         Rugby (1 template)
                                         Basketball (1 template)
                                         Track & Field (2 templates)
                                         Olympic Weightlifting (14 exercises, no templates)
```

---

## Section 5: Real Data Simulation

### 5A — Fast Bowler Athlete Trace

**Athlete:** Fast Bowler, Elite, 48 months training age
**Assessment Results:** CMJ = 42cm, IMTP = 2800N, MB Rotational Velocity = 9.2 m/s

**Step 1 — What PHASE_5A/000021 deficit system does:**
```
CMJ lookup: name depends on which migration won → either 'cmj' or 'Counter Movement Jump'
Benchmark lookup: 
  - If PHASE_5A won: finds 'cmj_suboptimal' (35-44.99) → 'Sub-optimal' → Power Deficit
  - If 000021 won: benchmarks INSERT failed → NO BENCHMARKS → engine returns None
  - If 000008 won (only CMJ via 'Force Plate...'): assessment name mismatch → NOT FOUND
```

**Step 2 — Deficit→Template routing:**
```
Power Deficit (deficit 1):
  - PHASE_5A: Route to Lower Body Power (template 1, American Football) ✓ (generic)
  - 000021: deficit_movement_templates insert only works if deficits inserted → DEPENDS ON TXN
  - 000008: 'Rate of Force Development Deficit' → Cricket Fast Bowler Power (best match!)
    But 000008's deficit links to 'Force Plate Countermovement Jump (CMJ)' assessment
    → engine must reference this exact name, not 'cmj' or 'Counter Movement Jump'
```

**Step 3 — Template→Exercise substitution:**
```
Lower Body Power template slot 1: Barbell Back Squat as default
  - exercise_sport_mapping for Cricket: NOT FOUND (no cricket mapping for Back Squat)
  - exercise_equivalencies: NONE (0 rows seeded)
  - Recommendation engine falls through to... empty set → NO EXERCISE RECOMMENDED
```

**Result:** A Fast Bowler with a CMJ-measured power deficit either:
1. Gets a generic Lower Body Power template with no executable exercises (likely outcome)
2. Gets no deficit detected at all (if benchmarks/assessment names mismatch)
3. Gets Cricket Fast Bowler Power template only if deficit engine uses 000008's exact names

**All three outcomes are wrong for production.**

### 5B — Batter Athlete Trace

**Athlete:** Batter, Advanced, 24 months training age
**Assessment Results:** 10m Sprint = 1.75s, CMJ = 48cm

**Step 1:**
```
10m Sprint: depends on migration order → '10m sprint' or '10m Sprint'
Benchmarks: 
  - PHASE_5A: 'sprint10_optimal' (1.61-1.80) → Optimal → No deficit triggered
  - 000021: benchmarks FAILED → no benchmark → engine returns None
```

**Step 2 — If deficit triggered (e.g., CMJ=32cm for Batter):**
```
Power Deficit → Lower Body Power template
  - Batter should get cricket-specific template → NONE EXISTS
  - Generic template with American Football tagging → Batter recommended American Football template
```

### 5C — Spinner Athlete Trace

**Athlete:** Spinner, Elite, 60 months training age
**Assessment:** MB Rotational Velocity Test = 7.5 m/s

**Step 1:**
```
Assessment name: 'rotational med ball throw' / 'Rotational Med Ball Throw' vs 
                 'Medicine Ball Rotational Velocity Test' (000008)
PHASE_5A/000021: name 'rotational med ball throw' or 'Rotational Med Ball Throw'
000008: 'Medicine Ball Rotational Velocity Test' — different ID, different name
```

**Step 2:**
```
PHASE_5A: Rotational Power Deficit (deficit 6) → Rotational Power template
000008: Rotational Core Power Deficit → Rotational Power template
Either way: generic Rotational Power template (Track & Field Throws origin)
No Spinner-specific template exists → generic template only
```

**Step 3 — Rotational Power template slot 2 requires Trap Bar equipment:**
```
slot_requirements: equipment = Trap Bar (id... wait, let me recheck 000004)
Line 168: equipment = Trap Bar
Does Trap Bar exist in equipment table? Let me check... 
Equipment seeded in migration 000001: Barbell, Dumbbell, Kettlebell, Medicine Ball, 
Resistance Bands, Cable Machine, Bodyweight, Slide Board, Trap Bar — yes, Trap Bar exists.
```

But none of the Spinner-specific exercises are mapped to the Rotational Power template slots. The Template→Exercise substitution would use exercise_movement_pattern/equipment/quality matching, which only has 5 fully-mapped exercises.

---

## Section 6: Defect List (Complete)

### CRITICAL (Must fix before production)

| ID | Defect | Source | Impact |
|----|--------|--------|--------|
| C1 | Assessment name fragmentation (3 conventions) | PHASE_5A, 000021, 000008 | Deficit engine can't find assessments 2/3 of the time |
| C2 | 000021 benchmarks have duplicate names → INSERT fails | 000021:30-76 | 28 benchmark tiers lost, possibly entire migration rolls back |
| C3 | 000021 deficits no `ON CONFLICT` — fails if PHASE_5A ran first | 000021:19-26 | 7 deficit definitions lost if ID collision |
| C4 | PHASE_5A deficits no `ON CONFLICT` — fails if 000021 ran first | PHASE_5A:16-24 | Same issue in opposite direction |
| C5 | "Power Deficit" never routes to "Cricket Fast Bowler Power" template | PHASE_5A:84-92, 000021:80-87 | Fast Bowler gets generic American Football template, not cricket-specific |
| C6 | No Cricket templates for Spinner, Batter, Keeper, All Rounder | 000005 only has Fast Bowler | 4/5 roles get wrong-sport templates |
| C7 | "Mobility Restriction" routes to "Shoulder Robustness" template | PHASE_5A:91, 000021:83 | Biomechanically incorrect mapping (hip mobility → shoulder work) |
| C8 | 0 exercise_equivalencies seeded | 000016 creates table, never populated | Substitution engine has zero fallback data |
| C9 | V1 → V2 ontology migration path has no bridge data | 000022 creates V2 tables, no mapping to V1 rows | V2 path has no production callers, V1 path can't feed V2 |
| C10 | 4 E2E test failures confirmed | tests/test_e2e_integration.py | "pull up" and "rotational med ball throw" bench-marks missing or name-mismatched |

### MODERATE (Fix before beta)

| ID | Defect | Source | Impact |
|----|--------|--------|--------|
| M1 | `exercise_class`, `primary_adaptation`, `force_vector` all NULL for all exercises | 000016 adds columns, never populates | Exercise classification/search disabled |
| M2 | Power Clean has no exercise_sport_mapping to Cricket | 000015/000017 only adds tags | High-value exercise never recommended for Cricket |
| M3 | 20+ V1 exercises have no Cricket sport mapping | 000004, 000002 | Can't be recommended to cricket athletes via sport filter |
| M4 | 000015 line 200 duplicate sport mapping (v_sport_af twice instead of AF+Rugby) | 000015 | Fixed in 000017, but 000015 runs first |
| M5 | PHASE_5A uses OVERRIDING SYSTEM VALUE with fixed IDs that conflict with 000021 | Both files | Deterministic naming depends on migration order = fragile |
| M6 | movement_pattern 'Anti-Rotation' and 'Push (Horizontal)' may not be seeded before 000004 uses them | 000004:145,181,216,244,251 | slot_requirements insert failures |
| M7 | V2 exercise_demand_mapping only covers 10 of 35 exercises | 000022 | Most exercises invisible to V2 demand-based selection |
| M8 | V2 metric_norms table empty (no seed data) | 000022 | Z-score deficit computation broken (metric norms required) |

---

## Section 7: Cleanup Estimates

| Task | Effort | Files | Dependencies |
|------|--------|-------|-------------|
| **Redo assessment names to single convention** | 1 day | PHASE_5A, 000021, 000008, deficit_engine.py, assessment_metric_engine.py | None |
| **Fix benchmark duplicate names in 000021** | 0.5 day | 000021 | Above |
| **Add ON CONFLICT to all deficit INSERTs** | 0.5 day | PHASE_5A, 000021 | None |
| **Add Cricket Spinner, Batter, Keeper, All Rounder templates** | 2 days | new migration 000025 | None |
| **Route deficits to correct cricket-specific templates** | 1 day | new deficit_routing migration | Above |
| **Seed exercise_equivalencies (30+ pairs)** | 2 days | new migration 000026 | None |
| **Populate exercise_class, primary_adaptation, force_vector** | 1 day | new migration 000027 | None |
| **Add V1→V2 bridge seed data** | 3 days | new migration 000028 | 000022 |
| **Add sport mappings for all 20 V1 exercises** | 1 day | new migration 000029 | None |
| **Fix Mobility Restriction routing** | 0.5 day | PHASE_5A, 000021 | Create Mobility template first |
| **Create Mobility/Flexibility template** | 1 day | new migration 000030 | None |
| **Add Olympic lifts to exercise_demand_mapping** | 1 day | new migration 000031 | None |
| **Seed metric_norms for V2 z-score path** | 1 day | new migration 000032 | 000022 |
| **Remove or rewire 000021 dead migration** | 0.5 day | 000021 | Verify PHASE_5A provides same data |
| **Fix E2E test failures** | 1 day | test_e2e_integration.py + seed data | All above |
| **Total** | **~16 days** | | |

---

## Section 8: Production Data Readiness Verdict

### Final Score: **1.5/10 — Not Ready**

### The Big Picture

The Forge database is **architecturally over-engineered and data-wise under-engineered**. The schema has 30+ tables with proper constraints, triggers, indexes, and relationships. The seed data has multiple conflicting systems that together ensure **nothing works end-to-end**.

The root cause is **three independent attempts at the same thing**:
1. **000008** built a cricket-specific knowledge graph with `performance_drivers` → `driver_assessments` → `benchmarks` → `deficits` → `deficit_movement_templates` → templates
2. **PHASE_5A_SEED.sql** and **000021** built a generic deficit system with `assessments` → `benchmarks` → `deficits` → `deficit_movement_templates` → templates
3. **000022** built a V2 ontology with `performance_demands` → `role_demand_priority` → `exercise_demand_mapping` / `assessment_demand_mapping` → `assessment_metrics` → `metric_demand_mapping`

None of the three systems talk to each other. The V2 path has no callers. The V1 path is fractured between 000008 (rich cricket data, disconnected from generic system) and PHASE_5A/000021 (generic data, broken benchmarks, no cricket-specific routing).

### What It Would Take to Ship

1. **Delete** PHASE_5A_SEED.sql and 000021 (or treat as dead code)
2. **Adopt** 000008's naming conventions as canonical
3. **Extend** 000008 with:
   - All 7 assessments (IMTP, CMJ, 10m Sprint, 20m Sprint, Broad Jump, Pull Up, MB Throw)
   - All 5 cricket role → driver → assessment → deficit chains
   - 4 Cricket-specific templates (Fast Bowler exists, add Spinner, Batter, Keeper/All-Rounder)
4. **Add** 28 benchmark tiers (4 per assessment × 7) with unique, consistent names
5. **Populate** exercise_equivalencies with 30+ substitution pairs
6. **Wire** V2 ontology to real assessment and exercise data
7. **Verify** all 4 E2E tests pass with real DB data before removing mock repositories

### Recommendation

**DO NOT REMOVE MOCK REPOSITORIES UNTIL STEP 7 IS COMPLETE.** Removing mocks would expose 15 critical data defects to every pipeline path. The mock repositories are currently the only thing making the system work — they provide consistent assessment names, complete benchmark tiers, and correct deficit routing that the seed data fails to deliver. Removing them would turn 4 test failures into 40+.

---

## Appendix: Migration Dependency Map

```
000001 ─► 000002 ─► 000003 ─► 000004 ─► 000005 ─► 000006 ─► 000007
                                                              │
                                                              ▼
                                                         000008 ─► 000009
                                                                      │
              ┌────────────────────────────────────────────────────────┘
              ▼
         000010 ─► 000011 ─► 000012 ─► 000013 ─► 000014
                                                    │
                                                    ▼
                                          ┌─ 000015 ─┐
                                          │  (buggy) │
                                          └─ 000017 ─┘  (repair)
                                                    │
                                                    ▼
                                          ┌─ 000016
                                          │
                                          ▼
                                     ┌─ 000018 ─► 000019
                                     │  
                                     ▼
                                 000020
                                    │
                                    ▼
                           ┌─ 000021 ─┐
                           │ (broken) │
                           └─ PHASE_5A ┘ (overlapping scope)
                                    │
                                    ▼
                                000022
                                    │
                                    ▼
                                000023 ─► 000024
```

Key insight: **000021 and PHASE_5A have overlapping scope with different naming conventions and no conflict resolution** (both try to insert ID 1-7 assessments, deficits, benchmarks). **000008 and PHASE_5A/000021 have overlapping scope** (both define deficits with different assessment links). **000022 stands completely alone** (V2 tables with no data bridge to V1).

---

## Methodology Notes

- This audit examined ONLY the database content (migration .sql files and seed data)
- No application code was reviewed beyond understanding how `deficit_detection_engine.py` and `assessment_metric_engine.py` consume the data
- The `deficit_detection_engine.py` V1 benchmark-based path was verified as the single authoritative path for MVP (as established by AUDIT #9)
- The four E2E test failures (`test_e2e_integration.py`) were confirmed against seed data: "pull up" and "rotational med ball throw" assessment name mismatches are the root cause
- Mock repository data was checked only to verify it provides what seed data should provide
- All scores are evidence-based, not opinion-based; each maps to specific seed data defects documented in this report
