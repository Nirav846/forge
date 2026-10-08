# Exercise Library Completion Plan - Phased Approach

> **Status note (updated 2026-09-24):** Much of the "missing metadata" listed
> below has since been implemented — coaching cues, common faults,
> contraindications, technical difficulty (`migrations/000020`), and
> progression chains (`build_progression_chains.py`) are present in current
> data. Verify each gap against `docs/DATA_MODEL.md` before working it; treat
> this document as a tracked TODO list, not a current-state analysis. The
> baseline below is historical.

## Current State Analysis *(historical baseline)*

**Total Exercises:** 198 conditioning exercises
**Existing Categories:** 29 systems (Aerobic, Anaerobic, Recovery, Mobility, Assessment, etc.)

### Critical Gaps Identified:

#### 1. Missing Metadata Fields (0/198 exercises have these): *(mostly resolved — verify per field)*
- ✗ coaching_cues (4 specific cues per exercise)
- ✗ common_faults (4 common errors to watch)
- ✗ contraindications (when NOT to prescribe)
- ✗ regressions (3 regression options - currently only has singular 'regression')
- ✗ progressions (3 progression pathways - currently only has singular 'progression')
- ✗ equipment_alternatives
- ✗ technical_difficulty (1-10 rating)
- ✗ training_age_min (minimum training age requirement)
- ✗ force_vector (force classification)

#### 2. Incomplete Metadata Coverage:
- sport_tags: Only 13/198 exercises (6.5%)
- progression/regression: Only 135/198 exercises (68%)

#### 3. Underrepresented Categories (<5 exercises each):
- Recovery/Mobility: 1
- Stability/Proprioception: 1
- Neuromuscular Training: 1
- Activation/Strength: 1
- Core Stability: 1
- Tendon Health: 1
- Warm-up: 1
- Aerobic Base: 2
- Mobility/Recovery: 2
- Recovery/Neurological: 2
- Recovery/Lifestyle: 2
- Recovery/Nutritional: 2
- Strength/Stability: 2

---

## Phased Implementation Strategy

### **PHASE 1: Core Metadata Enrichment** (Priority: CRITICAL)
**Goal:** Add essential coaching metadata to ALL 198 existing exercises

**Tasks:**
1. Add `coaching_cues` array (4 cues) to all exercises
2. Add `common_faults` array (4 faults) to all exercises
3. Add `contraindications` array to all exercises
4. Expand singular `regression` → `regressions` array (3 options)
5. Expand singular `progression` → `progressions` array (3 pathways)
6. Add `equipment_alternatives` array
7. Add `technical_difficulty` rating (1-10)
8. Add `training_age_min` (in months/years)
9. Add `force_vector` classification

**Deliverable:** `phase1_metadata_enrichment.json` (198 exercises with complete metadata)

---

### **PHASE 2: Sport-Specific Tagging Expansion** (Priority: HIGH)
**Goal:** Expand sport_tags from 13/198 to 198/198 (100% coverage)

**Tasks:**
1. Add comprehensive sport_tags to all exercises including:
   - Cricket (batting, bowling, fielding, wicket-keeping)
   - Tennis (singles, doubles, serve, baseline)
   - Badminton (singles, doubles, net play, rear court)
   - Football/Soccer (position-specific)
   - Basketball (guard, forward, center)
   - Volleyball (setter, hitter, libero)
   - Rugby (forwards, backs)
   - Athletics (sprinters, endurance, jumpers, throwers)
   - Multi-sport tags for general athletic development

**Deliverable:** `phase2_sport_tags_complete.json` (198 exercises with full sport tagging)

---

### **PHASE 3: Category Expansion - Recovery & Mobility** (Priority: MEDIUM)
**Goal:** Expand underrepresented recovery and mobility categories

**Target Additions (30-40 new exercises):**

#### Recovery Modalities (15 exercises):
- Active Recovery protocols
- Passive Recovery modalities
- Sleep optimization protocols
- Hydrotherapy (contrast baths, ice baths)
- Compression therapy
- Massage techniques (self-myofascial release)
- Breathing protocols (parasympathetic activation)
- Meditation/visualization
- Nutrition timing for recovery
- Hydration strategies

#### Mobility Flow Sequences (15 exercises):
- Dynamic warm-up flows
- Static stretching sequences
- PNF stretching protocols
- Joint mobilization drills
- Fascial release sequences
- Sport-specific mobility flows
- Prehab routines

#### Activation Protocols (10 exercises):
- Glute activation sequences
- Core activation drills
- Scapular activation
- Hip flexor activation
- Foot/ankle activation
- Postural reset protocols

**Deliverable:** `phase3_recovery_mobility_expansion.json` (40 new exercises)

---

### **PHASE 4: Assessment & Testing Protocols** (Priority: MEDIUM)
**Goal:** Expand assessment category from 12 to 25+ comprehensive tests

**Target Additions (15 new exercises):**

#### Physical Competency Screens:
- Overhead Squat Assessment
- Single Leg Squat Assessment
- Push-Up Test
- Plank Endurance Test
- Y-Balance Test
- Star Excursion Balance Test

#### Performance Tests:
- Vertical Jump (CMJ, SJ, DJ)
- Broad Jump
- 5-10-5 Pro Agility
- T-Test
- 40yd Dash
- 300yd Shuttle

#### Movement Quality:
- FMS-inspired screens
- Joint-by-joint assessments
- Range of motion screens

**Deliverable:** `phase4_assessment_expansion.json` (15 new exercises)

---

### **PHASE 5: Plyometrics & Power Development** (Priority: MEDIUM)
**Goal:** Add dedicated plyometrics category (currently missing as distinct category)

**Target Additions (25-30 new exercises):**

#### Lower Body Plyometrics:
- Box jumps (various heights)
- Depth jumps
- Hurdle hops
- Bounding variations
- Single leg hops
- Skips for height/distance

#### Upper Body Plyometrics:
- Clap push-ups
- Plyo push-ups
- Medicine ball throws
- Band-resisted punches

#### Multi-Directional:
- Lateral bounds
- Zig-zag hops
- Rotational throws

**Deliverable:** `phase5_plyometrics_expansion.json` (30 new exercises)

---

### **PHASE 6: Cool-down & Regeneration** (Priority: LOW)
**Goal:** Add dedicated cool-down category (currently missing)

**Target Additions (15-20 new exercises):**
- Post-training static stretches
- Breathing cooldowns
- Neural downregulation
- Heart rate recovery protocols
- Flexibility maintenance flows

**Deliverable:** `phase6_cooldown_regeneration.json` (20 new exercises)

---

## Summary Statistics

| Phase | Focus | New Exercises | Metadata Updates | Total After Phase |
|-------|-------|---------------|------------------|-------------------|
| Current | - | 198 | Partial | 198 |
| 1 | Core Metadata | 0 | All 198 | 198 |
| 2 | Sport Tags | 0 | All 198 | 198 |
| 3 | Recovery/Mobility | 40 | New only | 238 |
| 4 | Assessment | 15 | New only | 253 |
| 5 | Plyometrics | 30 | New only | 283 |
| 6 | Cool-down | 20 | New only | 303 |

**Final Library Size:** ~300 exercises with complete metadata

---

## Production Readiness Checklist

After all phases:
- ✅ Coaching cues on 100% of exercises
- ✅ Common faults on 100% of exercises
- ✅ Contraindications on 100% of exercises
- ✅ 3 regressions per exercise
- ✅ 3 progressions per exercise
- ✅ Equipment alternatives
- ✅ Technical difficulty ratings
- ✅ Training age minimums
- ✅ Force vector classifications
- ✅ Sport-specific tags on 100%
- ✅ Balanced category distribution
- ✅ Recovery/mobility/activation coverage
- ✅ Assessment protocols
- ✅ Plyometrics category
- ✅ Cool-down protocols

---

## Recommended Order of Execution

1. **Start with Phase 1** - Metadata enrichment provides immediate value
2. **Then Phase 2** - Sport tagging enables better personalization
3. **Then Phases 3-6** - Category expansions in parallel or sequence

Each phase produces a standalone deliverable that can be integrated independently.
