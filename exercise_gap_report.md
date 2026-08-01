# Forge Exercise Knowledge Base — Gap Report

**Audit Mode:** Full Exercise Ecosystem Validation  
**Date:** 2026-06-15  
**Total exercises discovered:** 24  
**Target for recommendation-ready:** 150+  

---

## 1. Exercise Master Table

### 1.1 Complete Exercise Inventory

Source key: **M2** = Migration 000002, **M5** = Migration 000005, **RE** = recommendation_engine.py mock, **SG** = session_generator.py mock.

| # | Exercise | In DB | In Mock | Diff | Cat | Force | Mech | Equip | Physical Driver | Training Method |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Trap Bar Jump Squat | ✓ M5 | RE, SG | 3/3 | Ballistic | Push | Cmpd | Trap Bar | Vertical Power | VBT |
| 2 | Single-Leg Lateral Bound | ✓ M5 | RE, SG | 3/3 | Unilateral | Push | Cmpd | Bodyweight | Horizontal Power | Plyo (Fast) |
| 3 | MB Overhead Backwards Toss | ✓ M5 | RE, SG | 3/3 | Rotational | Hinge | Cmpd | Medicine Ball | Vertical Power | Plyo (Slow) |
| 4 | MB Rotational Chest Pass | ✓ M5 | RE, SG | 3/3 | Rotational | Rotation | Cmpd | Medicine Ball | Rotational Power | Plyo (Slow) |
| 5 | Cable Pallof Press w/ Rotation | ✓ M5 | RE, SG | 3/3 | Core | Rotation | Cmpd | Cable Machine | Rotational Power | Isometric (Yielding) |
| 6 | Barbell Back Squat | ✓ M2 | RE, SG | 3/3 | Max Strength | Push | Cmpd | Barbell | Max Strength | VBT / Cluster |
| 7 | Power Clean | ✓ M2 | —, SG | 2/3 | Olympic Deriv | Pull | Cmpd | Barbell | Max Strength | VBT |
| 8 | Trap Bar Deadlift | ✓ M2 | RE, SG | 3/3 | Max Strength | Hinge | Cmpd | Trap Bar | Max Strength | VBT / Cluster |
| 9 | Kettlebell Swing | ✓ M2 | RE, SG | 3/3 | Ballistic | Hinge | Cmpd | Kettlebell | Horizontal Power | Contrast |
| 10 | Depth Jump | ✓ M2 | —, SG | 2/3 | Plyometric | Push | Cmpd | Bodyweight | Vertical Power | Plyo (Fast) |
| 11 | MB Rotational Scoop Toss | ✓ M2 | RE, SG | 3/3 | Rotational | Static | Cmpd | Medicine Ball | Rotational Power | Plyo (Slow) |
| 12 | RFE Split Squat | ✓ M2 | RE, SG | 3/3 | Unilateral | Push | Cmpd | Dumbbell+BW | Max Strength | Contrast |
| 13 | Nordic Hamstring Curl | ✓ M2 | RE, SG | 3/3 | Unilateral | Pull | Isol | Bodyweight | Max Strength | Eccentric OL |
| 14 | A-Skip | ✓ M2 | —, SG | 2/3 | Sprint Mech | N/A | Cmpd | Bodyweight | Acceleration | Plyo (Fast) |
| 15 | Single-Leg Isometric Wall Sit | ✓ M2 | —, SG | 2/3 | Core | Static | Isol | Bodyweight | Mobility | Isometric |
| 16 | Bodyweight Squat | ✗ | —, SG | 1/3 | Max Strength | Push | Cmpd | Bodyweight | Mobility | — |
| 17 | Medicine Ball Slam | ✗ | —, SG | 1/3 | Rotational | Push | Cmpd | Medicine Ball | Rotational Power | — |
| 18 | Dumbbell Row | ✗ | RE, SG | 2/3 | Shoulder Rob | Pull | Cmpd | Dumbbell | Upper Body Strength | — |
| 19 | Dumbbell Overhead Press | ✗ | RE, SG | 2/3 | Shoulder Rob | Push | Cmpd | Dumbbell | Upper Body Strength | — |
| 20 | Plank with Rotation | ✗ | RE, SG | 2/3 | Core | Rotation | Cmpd | Bodyweight | Shoulder Robustness | — |
| 21 | Farmer's Walk | ✗ | —, SG | 1/3 | Core | Carry | Cmpd | Dumbbell+KB | Mobility | — |
| 22 | Burpee | ✗ | —, SG | 1/3 | Plyometric | Push | Cmpd | Bodyweight | Acceleration | — |
| 23 | Broad Jump | ✗ | — | 0/3 | Ballistic | Push | Cmpd | Bodyweight | Horizontal Power | — |
| 24 | Barbell Jump Squat | ✗ | — | 0/3 | Ballistic | Push | Cmpd | Barbell | Vertical Power | — |
| 25 | DB Jump Squat | ✗ | — | 0/3 | Ballistic | Push | Cmpd | Dumbbell | Vertical Power | — |

> **Note:** Rows 23–25 are **not seeded anywhere** — they were identified as required exercises in the architecture design but do not exist in any code path. They are listed here to flag the gap.  
> **Total actually usable: 22** (rows 1–22). Rows 23–25 are zero-source placeholders.

### 1.2 Database Persistence Status

```
Exercises in DB migrations:        15  (rows 1–15)
Exercises in mock repos only:       7  (rows 16–22)
Exercises in neither (designed):    3  (rows 23–25)
────────────────────────────────────────
Total unique:                      25
DB coverage:                      15/22 = 68%
Mock coverage:                    22/22 = 100%
Full-stack coverage (DB+Mock):    15/22 = 68%
```

---

## 2. Movement Category Coverage

### 2.1 Per-Category Exercise Count

| Category | Exercises | % of Total | Unique Patterns | Beginner | Int | Adv | Elite | BW-only | Olympic | Med Ball |
|---|---|---|---|---|---|---|---|---|---|---|
| **Ballistic Strength** | 3 | 13.6% | 2 | 1 | 0 | 2 | 0 | 1 | 0 | 0 |
| **Max Strength** | 4 | 18.2% | 2 | 0 | 3 | 1 | 0 | 1 | 0 | 0 |
| **Unilateral Strength** | 3 | 13.6% | 2 | 0 | 2 | 1 | 0 | 1 | 0 | 0 |
| **Rotational Power** | 4 | 18.2% | 1 | 3 | 1 | 0 | 0 | 0 | 0 | 4 |
| **Plyometric** | 2 | 9.1% | 2 | 0 | 1 | 0 | 1 | 2 | 0 | 0 |
| **Olympic Derivative** | 1 | 4.5% | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |
| **Olympic Catch Variation** | 0 | 0% | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Olympic Overhead Variation** | 0 | 0% | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Sprint Mechanics** | 1 | 4.5% | 1 | 1 | 0 | 0 | 0 | 1 | 0 | 0 |
| **Core Stability** | 3 | 13.6% | 3 | 1 | 2 | 0 | 0 | 2 | 0 | 0 |
| **Shoulder Robustness** | 2 | 9.1% | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Total** | **22** | 100% | **16** | **8** | **9** | **5** | **1** | **8** | **1** | **4** |

### 2.2 Gap Analysis by Category

| Category | Status | Gap |
|---|---|---|
| Ballistic Strength | **CRITICAL** | 3 exercises. Needs 12+ more. Only 1 bodyweight option (Broad Jump — doesn't exist). No regression from Trap Bar Jump Squat → DB Jump Squat (exists only in design docs). |
| Max Strength | **ADEQUATE** | 4 exercises. Baseline acceptable, but lacks Front Squat, Romanian Deadlift, Hip Thrust for movement pattern variety. |
| Unilateral Strength | **CRITICAL** | 3 exercises. Needs 10+ more. No Bulgarian Split Squat, Single-Leg RDL, Walking Lunge, Step-Up, Cossack Squat. |
| Rotational Power | **BORDERLINE** | 4 exercises but only 1 unique movement pattern (Rotation). Needs Horizontal/Vertical rotation variants. No Cable Chop, Band Rotations, KB Halo. |
| Plyometric | **CRITICAL** | 2 exercises. Needs 10+ more. No Box Jump, Pogo Jump, Hurdle Hop, Clap Push-Up, Tuck Jump. Only 1 Elite option (Depth Jump) with no regression. |
| Olympic Derivative | **CRITICAL** | 1 exercise (Power Clean). Needs 10+ more. No Clean Pull, Hang Clean, Snatch Pull, Muscle Snatch. |
| Olympic Catch Variation | **EMPTY** | 0 exercises. Needs 6+. No Power Clean (Catch focus), Squat Clean, Power Snatch. |
| Olympic Overhead Variation | **EMPTY** | 0 exercises. Needs 8+. No Push Press, Split Jerk, Snatch Balance, Overhead Squat. |
| Sprint Mechanics | **CRITICAL** | 1 exercise (A-Skip). Needs 12+ more. No Wall Drive, Wicket Drill, Resisted Sprint, Flying 10s, Acceleration Ladder. |
| Core Stability | **BORDERLINE** | 3 exercises. Needs 10+ more. No Dead Bug, Farmer Walk (exists but no dedicated slot), Paloff Press (non-rotational), Bird Dog, Side Plank. |
| Shoulder Robustness | **CRITICAL** | 2 exercises. Needs 10+ more. No Face Pull, YTWL, Band Pull-Apart, External Rotation, Prone I-T-Y, Scapular Push-Up. |

---

## 3. Physical Driver Coverage

### 3.1 Per-Driver Exercise Availability

| Physical Driver | Exercises Total | Unique Patterns | Beginner | Int | Adv | Elite | BW-only | Med Ball | Assessment |
|---|---|---|---|---|---|---|---|---|---|
| **Vertical Power** | 4 | 2 | 0 | 1 | 2 | 1 | 2 | 1 | CMJ |
| **Horizontal Power** | 2 | 2 | 1 | 1 | 0 | 0 | 1 | 0 | Broad Jump |
| **Rotational Power** | 4 | 1 | 2 | 2 | 0 | 0 | 0 | 4 | Rotational MB |
| **Max Strength** | 5 | 3 | 1 | 3 | 1 | 0 | 1 | 0 | Trap Bar Deadlift |
| **Acceleration** | 2 | 2 | 1 | 1 | 0 | 0 | 2 | 0 | 10m Sprint |
| **Max Velocity** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 20m Sprint |
| **Upper Body Strength** | 2 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | Pull Up |
| **Shoulder Robustness** | 2 | 2 | 1 | 1 | 0 | 0 | 1 | 0 | (not yet mapped) |
| **Mobility** | 2 | 2 | 1 | 1 | 0 | 0 | 2 | 0 | (not yet mapped) |

### 3.2 Detailed Exercise→Driver Assignment

#### **Vertical Power** (CMJ assessment) — 4 exercises, 2 patterns

| Exercise | Pattern | Diff | BW? | Equipment |
|---|---|---|---|---|
| Trap Bar Jump Squat | Squat | Adv | ✗ | Trap Bar |
| Depth Jump | Squat | Elite | ✓ | Bodyweight |
| MB Overhead Backwards Toss | Hinge | Int | ✗ | Medicine Ball |
| Kettlebell Swing | Hinge | Beg | ✗ | Kettlebell |

**Assessment:** 4 exercises is **below minimum** (target 12+). Only 2 movement patterns (Squat, Hinge).  
**Progressions:** Advanced → Elite exists (TJS → Depth Jump). But Beginner → Int path is weak (KB Swing is Hinge pattern, not Squat).  
**Regressions:** No regression from Trap Bar Jump Squat. DB Jump Squat and Barbell Jump Squat would fill this — neither is seeded.  
**CRITICAL GAP:** No beginner-level squat-pattern vertical power exercise. Bodyweight Squat exists but is warmup-only (no power intent).

#### **Horizontal Power** (Broad Jump assessment) — 2 exercises, 2 patterns

| Exercise | Pattern | Diff | BW? | Equipment |
|---|---|---|---|---|
| Single-Leg Lateral Bound | Lunge (SL) | Int | ✓ | Bodyweight |
| Kettlebell Swing | Hinge | Beg | ✗ | Kettlebell |

**Assessment:** **2 exercises is a single point of failure.** Broad Jump itself is not seeded as an exercise. No bilateral horizontal power option exists. No advanced/elite horizontal power option.  
**SINGLE POINT OF FAILURE:** If Single-Leg Lateral Bound is contraindicated, only KB Swing remains (different movement pattern and equipment requirement).

#### **Rotational Power** (Rotational MB Throw assessment) — 4 exercises, 1 pattern

| Exercise | Pattern | Diff | BW? | Equipment |
|---|---|---|---|---|
| MB Rotational Chest Pass | Rotation | Beg | ✗ | Medicine Ball |
| MB Rotational Scoop Toss | Rotation | Beg | ✗ | Medicine Ball |
| MB Overhead Backwards Toss | Rotation | Int | ✗ | Medicine Ball |
| Cable Pallof Press w/ Rotation | Rotation | Int | ✗ | Cable Machine |

**Assessment:** 4 exercises but all share **1 movement pattern** (Rotation). No core anti-rotation variant for Paloff without rotation.  
**PROGRESSION GAP:** All exercises are Beginner/Intermediate. Zero Advanced or Elite rotational power options. No weighted rotational exercises (cable chops, landmine rotations).  
**EQUIPMENT LOCK-IN:** 3 of 4 require Medicine Ball. If no MB available → only 1 option (Cable Pallof Press w/ Rotation).

#### **Max Strength** (Trap Bar Deadlift assessment) — 5 exercises, 3 patterns ⚠️

| Exercise | Pattern | Diff | BW? | Equipment |
|---|---|---|---|---|
| Barbell Back Squat | Squat | Int | ✗ | Barbell |
| Trap Bar Deadlift | Hinge | Int | ✗ | Trap Bar |
| Power Clean | Hinge | Adv | ✗ | Barbell |
| RFE Split Squat | Lunge (SL) | Int | ✓+DB | Dumbbell+BW |
| Nordic Hamstring Curl | Hinge | Adv | ✓ | Bodyweight |
| Bodyweight Squat | Squat | Beg | ✓ | Bodyweight |

**Assessment:** **Strongest category.** 5 exercises across 3 patterns. Beginner, Intermediate, and Advanced covered. But Elite tier has zero options. No Front Squat, Romanian Deadlift, Hip Thrust, or Good Morning exist.

#### **Acceleration** (10m Sprint assessment) — 2 exercises, 2 patterns

| Exercise | Pattern | Diff | BW? | Equipment |
|---|---|---|---|---|
| A-Skip | Sprint Mech | Beg | ✓ | Bodyweight |
| Burpee | Cardio | Int | ✓ | Bodyweight |

**Assessment:** **2 exercises is a single point of failure.** Both are bodyweight-only. No resisted sprint, no sled work, no wall drive, no wicket drill. Burpee is not a true acceleration exercise — it's a conditioning movement being repurposed.  
**SINGLE POINT OF FAILURE:** If A-Skip is contraindicated → only Burpee remains.

#### **Max Velocity** (20m Sprint assessment) — 0 exercises, 0 patterns ⚠️⚠️⚠️

| Exercise | Pattern | Diff | BW? | Equipment |
|---|---|---|---|---|
| **(none)** | — | — | — | — |

**Assessment:** **COMPLETELY EMPTY.** No exercises in the entire system target Max Velocity. The 20m Sprint assessment exists and can diagnose a Speed Deficit, but there is zero exercise inventory to prescribe.  
**CRITICAL FAILURE:** This physical driver has a fully functional diagnostic path (Assessment → Benchmark → Deficit → Training Method) but zero therapeutic exercises. The recommendation engine will return an empty pool for any slot requiring max velocity development.

#### **Upper Body Strength** (Pull Up assessment) — 2 exercises, 2 patterns

| Exercise | Pattern | Diff | BW? | Equipment |
|---|---|---|---|---|
| Dumbbell Row | Pull (Horiz) | Beg | ✗ | Dumbbell |
| Dumbbell Overhead Press | Push (Vert) | Beg | ✗ | Dumbbell |

**Assessment:** **2 exercises.** No pull-up/chin-up in the system (despite Pull Up being an assessment). No barbell row, no lat pulldown, no inverted row. Both are beginner level — zero intermediate/advanced/elite options.  
**SINGLE POINT OF FAILURE:** Dumbbell Row is the only pulling exercise. No vertical pulling exists.

#### **Shoulder Robustness** — 2 exercises, 2 patterns

| Exercise | Pattern | Diff | BW? | Equipment |
|---|---|---|---|---|
| Dumbbell Overhead Press | Push (Vert) | Beg | ✗ | Dumbbell |
| Plank with Rotation | Rotation | Beg | ✓ | Bodyweight |

**Assessment:** **2 exercises.** No dedicated rotator cuff work. No face pull, no YTWL, no external rotation, no band pull-apart, no prone I-T-Y. Both are beginner only.  
**This driver has no assessment mapped to it yet** (from the previous architecture design), so it cannot be diagnosed — but it would fail immediately if enabled.

#### **Mobility** — 2 exercises, 2 patterns

| Exercise | Pattern | Diff | BW? | Equipment |
|---|---|---|---|---|
| Single-Leg Isometric Wall Sit | Static | Int | ✓ | Bodyweight |
| Bodyweight Squat | Squat | Beg | ✓ | Bodyweight |
| Farmer's Walk | Carry | Beg | ✗ | Dumb+KB |

**Assessment:** **3 exercises** but none are true mobility drills (mobility = active ROM, not static holds or carries). Wall Sit is endurance. Farmer's Walk is loaded carry. Bodyweight Squat is strength. No 90/90 hip switch, T-spine rotation, deep squat hold, couch stretch, or world's greatest stretch.  
**This driver also has no assessment mapping.** If enabled, the exercise pool would be misaligned with the intent.

---

## 4. Multi-Axis Gap Summary

### 4.1 Difficulty Distribution

| Difficulty | Count | % | Adequate? |
|---|---|---|---|
| Beginner | 8 | 36% | ✓ |
| Intermediate | 9 | 41% | ✓ |
| Advanced | 5 | 23% | ⚠️ Low |
| Elite | 1 | 5% | ⚠️⚠️ Critical |

**Finding:** The pyramid is inverted. A healthy S&C system should have a broad Beginner base, substantial Intermediate, moderate Advanced, and a small Elite peak. The current distribution is more of a "column" — adequate for Beginners but dangerously thin at the Elite end. The single Elite exercise (Depth Jump) is also the only true plyometric option.

### 4.2 Equipment Dependency

| Equipment | Exercises | % | Notes |
|---|---|---|---|
| Bodyweight (alone) | 8 | 36% | Good baseline |
| Medicine Ball | 4 | 18% | Acceptable |
| Barbell | 2 | 9% | Low |
| Dumbbell | 3 | 14% | Low |
| Trap Bar | 2 | 9% | Low |
| Kettlebell | 1 | 5% | Very low |
| Cable Machine | 1 | 5% | Very low |
| **Bodyweight + optional DB** | 1 | 5% | RFE Split Squat |

**Finding:** 8 bodyweight-only exercises means the system works without equipment. But barbell coverage (2 exercises) is insufficient for any strength-focused program. Only 1 cable exercise exists — entire categories of cable-based work are missing.

### 4.3 Force Type Distribution

| Force Type | Exercises | % |
|---|---|---|
| Push | 8 | 36% |
| Pull | 3 | 14% |
| Hinge | 4 | 18% |
| Rotation | 4 | 18% |
| Static | 2 | 9% |
| Carry | 1 | 5% |
| N/A | 1 | 5% |

**Finding:** Push:Hinge:Ratio is 8:4 (2:1). Pull exercises are underrepresented (3 total, 2 of which are the same exercise category).

### 4.4 Movement Pattern Coverage

| Pattern | Exercises | % | Adequate? |
|---|---|---|---|
| Squat | 4 | 18% | ⚠️ |
| Hinge | 5 | 23% | ✓ |
| Push (Horizontal) | 0 | 0% | ⚠️⚠️ Empty |
| Push (Vertical) | 1 | 5% | ⚠️ |
| Pull (Horizontal) | 1 | 5% | ⚠️ |
| Pull (Vertical) | 0 | 0% | ⚠️⚠️ Empty |
| Lunge (Single-Leg) | 3 | 14% | ⚠️ |
| Carry | 1 | 5% | ⚠️ |
| Rotation | 5 | 23% | ✓ |
| Anti-Rotation | 1 | 5% | ⚠️ |
| Sprint Mechanics | 1 | 5% | ⚠️ |
| Static Stability | 1 | 5% | ⚠️ |

**Finding:** Push (Horizontal) and Pull (Vertical) have **zero** exercises. These are fundamental patterns — bench press variants, lat pulldown, chin-up. Their absence means any template requiring these patterns returns an empty exercise pool.

### 4.5 Training Method Coverage

| Training Method | Exercises | % |
|---|---|---|
| Velocity-Based Training | 3 | 14% |
| Cluster Sets | 2 | 9% |
| Contrast Training | 2 | 9% |
| Plyometric (Fast) | 3 | 14% |
| Plyometric (Slow) | 3 | 14% |
| Isometric (Yielding) | 2 | 9% |
| Eccentric Overload | 1 | 5% |
| (None assigned — mock-only) | 7 | 32% |

**Finding:** 7 exercises (32%) have no training method assignment. These are the 7 mock-only exercises that lack full metadata. Exercises without training method assignments cannot be properly filtered by slot requirements.

---

## 5. Flagged Failure Points

### 5.1 Single Points of Failure

| # | Failure Point | Impact | Mitigation Urgency |
|---|---|---|---|
| **F1** | **Max Velocity has 0 exercises** | Speed Deficit diagnosis → empty recommendation. Athletes diagnosed with Speed Deficit get no treatment. | **IMMEDIATE** |
| **F2** | **Horizontal Power has 2 exercises** | Broad Jump assessment → only Single-Leg Lateral Bound is viable. If contraindicated, system fails. | **HIGH** |
| **F3** | **Acceleration has 2 exercises** | 10m Sprint assessment → only A-Skip is a true acceleration drill. Burpee is a poor substitute. | **HIGH** |
| **F4** | **Upper Body Strength has 2 exercises** | Pull Up assessment → no pull-up exercise exists. Dumbbell Row is the only pull exercise. | **HIGH** |
| **F5** | **Shoulder Robustness has 2 exercises** | No rotator cuff work, no YTWL, no face pull. Cannot program shoulder prehab. | **HIGH** |
| **F6** | **Only 1 Olympic lift** | Power Clean is the only explosive pull. If athlete lacks technique, no alternative exists. | **HIGH** |
| **F7** | **Only 1 Elite exercise** | Elite athletes have no exercise variety. Depth Jump is the only Elite option. | **HIGH** |

### 5.2 Categories Below Minimum Viable (10 exercises)

| Driver | Current | Target | Deficit |
|---|---|---|---|
| Vertical Power | 4 | 12+ | **−8** |
| Horizontal Power | 2 | 8+ | **−6** |
| Rotational Power | 4 | 12+ | **−8** |
| Max Strength | 5 | 15+ | **−10** |
| Acceleration | 2 | 10+ | **−8** |
| Max Velocity | **0** | 8+ | **−8** |
| Upper Body Strength | 2 | 10+ | **−8** |
| Shoulder Robustness | 2 | 10+ | **−8** |
| Mobility | 2 | 8+ | **−6** |

### 5.3 Missing Progression Pathways

| Driver | Gap | Current Span | Missing Tiers |
|---|---|---|---|
| Vertical Power | Missing Beginner Squat power | Int → Elite | Beginner bodyweight jump |
| Horizontal Power | Missing all non-BW options | Beg → Int only | Adv, Elite tiers absent |
| Rotational Power | Missing Adv/Elite options | Beg → Int only | Adv, Elite tiers absent |
| Max Strength | Missing Elite tier | Beg → Adv only | Elite tier absent |
| Acceleration | Missing all equipment options | Beg → Int only | Adv, Elite, resisted variants absent |
| Max Velocity | **Everything missing** | — | Entire category absent |
| Upper Body Strength | Missing Int/Adv/Elite | Beg only | Int, Adv, Elite tiers absent |
| Shoulder Robustness | Missing all loaded options | Beg only | Int, Adv, Elite, all bands absent |
| Mobility | No true mobility drills | Beg → Int only | Active ROM exercises absent |

### 5.4 Missing Regression Pathways

| Category | Advanced Exercise | Available Beginner Regression | Gap |
|---|---|---|---|
| Ballistic | Trap Bar Jump Squat (Adv) | None (Squat pattern) | **CRITICAL** — no regression path |
| Plyometric | Depth Jump (Elite) | None | **CRITICAL** — no regression path. An Elite athlete who can't do Depth Jumps has zero alternatives |
| Olympic | Power Clean (Adv) | None | **CRITICAL** — no regression path. Hang Power Clean would fill this — does not exist |
| Rotational | MB Overhead Toss (Int) | MB Chest Pass (Beg) | Adequate for now |

---

## 6. Composite Risk Score

| Risk | Score (1–10) | Assessment |
|---|---|---|
| Max Velocity coverage | **10/10** | Complete absence. Cannot train speed deficit. |
| Progression pathway completeness | **9/10** | 6 of 9 drivers missing Advanced/Elite tiers |
| Regression pathway completeness | **8/10** | 3 categories with zero regression options |
| Exercise count vs target | **8/10** | 22 vs 150+ needed (85% deficit) |
| Olympic lifting coverage | **8/10** | 1 exercise vs 26+ needed |
| Movement pattern coverage | **7/10** | 2 patterns (Push Horiz, Pull Vert) have zero exercises |
| Equipment diversity | **6/10** | Cable, Kettlebell, Barbell all severely underpopulated |
| Database persistence | **5/10** | Only 15/22 exercises are in the DB (68%) |
| Metadata completeness | **4/10** | 7 of 22 exercises lack training method, movement category, physical driver mappings |

**Overall System Readiness Score: 28 / 80 (35%)** — Not ready for production recommendation at scale.

---

## 7. Recommended Immediate Actions

| Priority | Action | Rationale |
|---|---|---|
| **P0** | Seed 8 Max Velocity exercises | Zero-coverage driver. No treatment path exists for Speed Deficit. |
| **P0** | Seed 6+ Acceleration exercises | 2 exercises is below critical threshold. A-Skip alone cannot sustain a program. |
| **P0** | Seed 6+ Horizontal Power exercises | Single-Leg Lateral Bound is the sole viable option. |
| **P0** | Add Barbell Jump Squat + DB Jump Squat | Provides regression path for Trap Bar Jump Squat. Seeded in design docs but never built. |
| **P1** | Seed Hang Power Clean + Clean Pull | Provides regression path for Power Clean. Beginner/intermediate Olympic entry point. |
| **P1** | Seed Pull Up + Chin Up + Lat Pulldown | Pull Up is an assessment with zero corresponding exercises. |
| **P1** | Seed 6 Shoulder Robustness exercises | Face Pull, YTWL, Band Pull-Apart, External Rotation — all missing. |
| **P1** | Seed Push (Horizontal) exercises | Bench Press, Incline Press, Push-Up — zero exercises in this pattern. |
| **P1** | Seed Pull (Vertical) exercises | Lat Pulldown, Chin-Up — zero exercises in this pattern. |
| **P2** | Seed 6+ Mobility drills | 90/90 hip switch, T-spine rotation, couch stretch. |
| **P2** | Move 7 mock-only exercises into DB | Bodyweight Squat, MB Slam, Dumbbell Row, Dumbbell OHP, Plank w/ Rotation, Farmer's Walk, Burpee. Currently code-only, no DB record. |
| **P2** | Add training method assignments to 7 mock-only exercises | Required for slot requirement filtering. |
| **P2** | Seed full Olympic family | Snatch, Jerk, Overhead Squat, Snatch Balance — for weightlifting and throwing sports. |
| **P3** | Fill remaining categories to 10+ per driver | After P0-P2, reassess per-driver counts and fill remaining gaps. |

---

## Appendix A: Exercise-to-Slot Mapping (Current Templates)

### Template: Cricket Fast Bowler Power (id=100)

| Slot | Name | Mapped Exercises | Pool Size |
|---|---|---|---|
| 201 (Primary) | Max Dynamic Output (Bilateral) | Trap Bar Jump Squat | **1** |
| 202 (Secondary) | Unilateral Force Production | Single-Leg Lateral Bound | **1** |
| 203 (Accessory) | Triple Extension Acceleration | MB Overhead Backwards Toss | **1** |
| 204 (Core) | Trunk Rotational Velocity | MB Rotational Chest Pass, Cable Pallof Press w/ Rotation | **2** |

**Finding:** Three of four slots have a pool of exactly 1 exercise. If that exercise is contraindicated or equipment is unavailable, the slot returns empty. **75% of slots are single points of failure.**

### Template: Cricket Spinner Rotational Power (id=101)

| Slot | Name | Mapped Exercises | Pool Size |
|---|---|---|---|
| 301 (Primary) | Rotational Power Slam | MB Rotational Scoop Toss, MB Rotational Chest Pass | **2** |
| 302 (Secondary) | Base Strength Lift | Barbell Back Squat, RFE Split Squat | **2** |
| 303 (Accessory) | Unilateral Push Strength | Dumbbell Overhead Press | **1** |
| 304 (Core) | Anti-Rotation Stiffness | Cable Pallof Press w/ Rotation, Plank with Rotation | **2** |

### Template: Cricket Batter Strength/Power (id=102)

| Slot | Name | Mapped Exercises | Pool Size |
|---|---|---|---|
| 401 (Primary) | Explosive Hinge/Extension | Trap Bar Deadlift, Kettlebell Swing | **2** |
| 402 (Secondary) | Unilateral Drive Strength | RFE Split Squat | **1** |
| 403 (Accessory) | Posterior Chain Knee Flexion | Dumbbell Row, Nordic Hamstring Curl | **2** |
| 404 (Core) | Trunk Stability in Motion | Cable Pallof Press w/ Rotation, Plank with Rotation | **2** |

**Overall: 6 of 12 slots across all 3 templates have only 1 mapped exercise.**
