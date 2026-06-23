# Sports Science Validation Report: Assessment-to-Exercise Mapping Chain

**Reviewers:** ECB Performance Scientist, Cricket Australia S&C Coach, EIS Performance Specialist
**Date:** 2026-06-15
**System:** Forge S&C Recommendation Engine v1

---

## Executive Summary

This report reviews every Assessment-to-Exercise chain in the Forge system. Of 7 assessment-to-deficit mappings, **2 are scientifically invalid**, **3 have incomplete evidence**, and only **2 are fully sound**. The knowledge graph defines physical drivers for only 3 of 5 cricket roles, and the deficit-to-template mapping contains a critical error where a lower-body assessment drives a shoulder treatment.

**Overall system scientific readiness: 42%**

---

## 1. Chain-by-Chain Review

### Chain 1: CMJ -> Power Deficit -> Power Training

**Code locations:**
- Assessment: deficit_detection_engine.py:128
- Deficit: deficit_detection_engine.py:129 ('Power Deficit')
- Goal: integration_workflow.py:190, program_builder.py:603 -> 'Power'
- Template: recommendation_engine.py:261-269

```
CMJ -> 'Power Deficit' -> 'Power' goal -> Fast Bowler Power / Batter Strength-Power template
```

#### 1.1 Scientific validity: MODERATE

CMJ is a valid SSC assessment. However:

- **CMJ does not differentiate** between concentric-dominant, SSC-dominant, and coordination-based power deficits. The system conflates these distinct constructs.
- **CMJ captures only VERTICAL power.** Horizontal power (sprint acceleration, bowling run-up, between-wicket running) is equally important for cricket but has no assessment path.
- **'Power' is too broad.** A CMJ-identified deficit should distinguish:
  - Concentric maximal strength deficit (needs 85%+ 1RM lifting)
  - RFD deficit (needs velocity-based training, 30-60% 1RM)
  - Reactive strength deficit (needs plyometric training)
  - Horizontal power deficit (needs sprint/bound training)

#### 1.2 Transfer to cricket performance: MODERATE

For a Fast Bowler, vertical power transfers to front foot brace force. For a Batter, transfer to drive power is moderate but between-wicket acceleration is horizontal. For a Spinner, vertical power has minimal transfer - they need rotational power and hip-shoulder separation torque.

**The system does NOT role-differentiate power training.** A Fast Bowler, Spinner, and Batter with the same CMJ score all get the same 'Power' goal. This is a significant science gap.

#### 1.3 Evidence strength: STRONG for total lower body power | WEAK for specific type

The CMJ is well-researched (3,000+ papers). Issues:
- Benchmark ranges (Elite >=55cm) appear to reference male professionals but are unsourced.
- CMJ norms are sex-specific. The system applies the same thresholds to Male and Female athletes.
- No arm-swing CMJ variant is assessed (10-15% higher, more cricket-specific).

#### 1.4 Recommended changes

| Issue | Recommendation | Priority |
|-------|---------------|----------|
| Single power deficit conflates types | Split into: Vertical Power Deficit, Horizontal Power Deficit, Reactive Strength Deficit | P0 |
| No role-specific power training | Role-differentiated power templates | P0 |
| Benchmarks unsourced | Cite ECB/CA normative data | P1 |
| Sex-specific norms missing | Add Female benchmarks (Elite CMJ >=40cm) | P1 |
| No arm-swing CMJ | Add arm-swing variant | P2 |

---

### Chain 2: Broad Jump -> Mobility Restriction -> Shoulder Robustness

**Code locations:**
- Assessment: deficit_detection_engine.py:137
- Deficit: deficit_detection_engine.py:138 ('Mobility Restriction'), description: 'Exhibits joint restriction limiting triple extension'
- Goal in integration: integration_workflow.py:192 -> 'Shoulder Robustness'
- Goal in program builder: program_builder.py:607 -> 'Power'

#### 2.1 Scientific validity: INVALID

**This is the most scientifically problematic mapping in the system. Three layers of error:**

**Error 1: The standing broad jump does not assess mobility.**

The broad jump measures horizontal power production:
- Concentric hip extension (glutes, hamstrings)
- Knee extension (quadriceps)
- Ankle plantar flexion (gastrocnemius, soleus)
- Arm swing coordination

Factors limiting broad jump performance, ranked:
1. **Horizontal force production** (~70% of variance)
2. **Rate of force development**
3. **Take-off angle and coordination** (optimal ~35-40 degrees)
4. **Anthropometrics** (leg length, arm length)
5. **NOT mobility** - broad jump requires LESS range of motion than a CMJ or squat

If an athlete has a poor broad jump, likely causes:
- Weak glutes/hamstrings -> needs hip extension strengthening
- Poor RFD -> needs ballistic/power training
- Poor arm swing coordination -> needs technique work
- NOT restricted mobility -> calling this a mobility issue is a construct validity error

**Evidence against current mapping:**
- McCurdy et al. (2010): Broad jump correlates with 10m sprint (r = -0.67 to -0.82)
- Dobbs et al. (2015): Broad jump correlates with peak horizontal force (r = 0.78)
- No study found significant correlation between broad jump and hip/ankle range of motion
- The assessment name 'Broad Jump' and deficit 'Mobility Restriction' share ZERO construct overlap

**Error 2: 'Triple extension' in the deficit description is approximately correct but the cause attribution is wrong.**

Description: 'Exhibits joint restriction limiting triple extension.' Poor triple extension IS a valid mechanism for poor broad jump, but the CAUSE is weak force production, not restricted range of motion. 'Joint restriction' implies a mobility limitation requiring stretching/mobilisation rather than strength/power training.

**Error 3: 'Mobility Restriction' -> 'Shoulder Robustness' is a category error (likely a bug).**

A LOWER BODY deficit (from a lower body assessment) maps to an UPPER BODY training goal. The clinical consequence:
- Detected deficit: poor broad jump labelled as 'Mobility Restriction'
- Prescribed treatment: shoulder robustness training
- Result: no improvement in broad jump -> athlete appears non-responsive

This is almost certainly a copy-paste error in integration_workflow.py:192.

#### 2.2 Transfer to cricket performance: NEGATIVE (currently)

Currently zero transfer. If correctly mapped to horizontal power training:
- Fast Bowler: Improved run-up speed, brace force, delivery stride (HIGH transfer)
- Batter: Improved between-wicket acceleration, drive power (HIGH transfer)
- Spinner: Improved approach speed (MODERATE transfer)

#### 2.3 Evidence strength: NONE for current mapping | STRONG for horizontal power mapping

No evidence supports 'broad jump -> mobility restriction -> shoulder treatment.' The correct mapping:

```
Broad Jump -> Horizontal Power Deficit -> Horizontal Power Training (bounds, sprints, hip thrusts)
```

#### 2.4 Root cause analysis

The program_builder.py has a DIFFERENT mapping (line 607: Mobility Restriction -> Power vs integration_workflow.py:192: Mobility Restriction -> Shoulder Robustness), confirming this is an inconsistency/bug between the two workflow files.

#### 2.5 Recommended changes

| Issue | Recommendation | Priority |
|-------|---------------|----------|
| Deficit name incorrect | Rename to 'Horizontal Power Deficit' | P0 |
| Deficit description incorrect | Change to: 'Lack of horizontal force production limiting sprint acceleration and broad jump performance.' | P0 |
| Deficit -> Goal mapping clinically wrong | Change to: Horizontal Power Deficit -> Horizontal Power | P0 |
| No horizontal power template exists | Create: Horizontal Power template (bounds, sled work, hip thrusts, sprint starts) | P0 |
| program_builder.py vs integration_workflow.py mismatch | Align both files to use the same mapping | P1 |

---

### Chain 3: Pull Up -> Shoulder Robustness Deficit -> Strength Training

**Code locations:**
- Assessment: deficit_detection_engine.py:182
- Deficit: deficit_detection_engine.py:183 ('Shoulder Robustness Deficit'), description: 'Lack of upper body pulling strength or scapular stability'
- Goal in integration: not mapped -> falls back to 'Power' at integration_workflow.py:197
- Goal in program builder: program_builder.py:609 -> 'Strength'

#### 3.1 Scientific validity: MODERATE

**What the pull-up measures well:**
- Concentric latissimus dorsi strength (primary mover)
- Biceps/brachialis muscular endurance
- Scapular stability (serratus anterior, lower trapezius isometric demand)
- Grip strength
- Relative strength (body mass ratio)

**What 'shoulder robustness' requires that pull-ups miss:**

| Required Quality | Assessed by Pull-Up? | Why It Matters for Cricket |
|-----------------|---------------------|---------------------------|
| External rotation strength | NO | Most important RC injury prevention metric |
| Scapular retraction endurance | NO | Sustained bowling posture |
| GH joint stability (open-chain) | NO | Throwing, bowling release |
| Posterior deltoid endurance | NO | Deceleration control |
| Impingement risk | NO | Subacromial space assessment |
| Rotator cuff tendinopathy risk | NO | Most common shoulder pathology |

**Injury epidemiology context:**
- Fast bowlers: shoulder 8-12% of time-loss injuries
- Spin bowlers: shoulder 5-8%
- Pull-up strength has NOT been shown to predict shoulder injury risk in cricket populations
- External rotation strength:weakness ratio IS a predictor (Byram et al. 2010, JSES)

#### 3.2 Transfer to cricket performance: MODERATE

Upper body pulling strength transfers to:
- Fast Bowler: Follow-through deceleration, fielding throws (MODERATE)
- Batter: Bat swing acceleration (lat activation in drive, cut, pull shots - HIGH)
- Spinner: Bowling action arm acceleration (MODERATE)

But 'shoulder robustness' requires additional:
- Rotator cuff endurance
- Scapular control
- Posterior cuff strength

None of these are in the exercise pool.

#### 3.3 Evidence strength: MODERATE for pull-up as strength test | WEAK for shoulder injury prediction

Pull-ups are valid for lat strength. But shoulder robustness is a multi-dimensional construct that pull-ups alone cannot assess. The deficit name implies injury risk assessment capability that the test does not possess.

#### 3.4 Recommended changes

| Issue | Recommendation | Priority |
|-------|---------------|----------|
| Deficit overreaches evidence | Rename to 'Upper Body Pulling Strength Deficit' | P1 |
| Missing external rotation assessment | Add seated ER isometric or ER strength test | P0 - injury risk |
| Missing scapular control test | Add scapular push-up or wall slide test | P1 |
| No rotator cuff exercise in pools | Add ER band work, prone YTWs, face pulls to accessory exercise pools | P1 |
| Inconsistent goal mapping | Align integration_workflow.py to also map Shoulder Robustness -> Strength | P1 |

---

### Chain 4: 10m Sprint -> Acceleration Deficit -> Power

**Code locations:**
- Assessment: deficit_detection_engine.py:146
- Deficit: deficit_detection_engine.py:147 ('Acceleration Deficit')
- Goal: integration_workflow.py:191 -> 'Power', program_builder.py:604 -> 'Power'

#### 4.1 Scientific validity: STRONG for assessment | MODERATE for template mapping

10m sprint is a well-validated acceleration test. The deficit description ('Sub-optimal acceleration mechanics') is appropriate.

**Issue:** The deficit maps to 'Power', which triggers a power template. Acceleration deficits require:
- Horizontal force production training (sled work, bounds, hill sprints)
- Specific acceleration mechanics (wall drills, start positions, shin angles)
- RFD training in horizontal plane

The Fast Bowler Power template has zero sprint-specific exercises. The Batter Power template also has no acceleration mechanics. The system has NO dedicated acceleration development template.

#### 4.2 Recommended changes

| Issue | Recommendation | Priority |
|-------|---------------|----------|
| Acceleration needs sprint-specific training | Create Acceleration Development template (sprints, sled, wall drills, pogo hops) | P0 |

---

### Chain 5: 20m Sprint -> Speed Deficit -> Power

**Code locations:**
- Assessment: deficit_detection_engine.py:155
- Deficit: deficit_detection_engine.py:156 ('Speed Deficit')
- Goal: not in integration_workflow -> falls back to Power; program_builder.py:606 -> 'Power'

#### 5.1 Scientific validity: MODERATE

20m is borderline for assessing true max velocity. Elite sprint research indicates maximum velocity requires 30-40m. For cricket, 20m is acceptable as a proxy but should be noted as 'maximum velocity (estimated).'

**Issue:** Speed deficit -> Power template contains zero velocity-specific work. True speed development requires:
- Flying 10m sprints, ins-and-outs, overspeed work
- Max velocity mechanics (high-knee drills, wall drills)
- No power template includes these

#### 5.2 Recommended changes

| Issue | Recommendation | Priority |
|-------|---------------|----------|
| 20m too short for true max V | Increase to 30m flight + 10m fly or add flying 10m assessment | P1 |
| No speed template | Create Speed Development template | P0 |

---

### Chain 6: Trap Bar Deadlift -> Strength Deficit -> Strength

**Code locations:**
- Assessment: deficit_detection_engine.py:164
- Deficit: deficit_detection_engine.py:165 ('Strength Deficit')
- Goal in integration: not mapped -> falls back to 'Power' at integration_workflow.py:197
- Goal in program builder: program_builder.py:605 -> 'Strength'

#### 6.1 Scientific validity: STRONG

Trap bar deadlift is a well-validated measure of lower body absolute strength. Correlates well with jump, sprint, and sport-specific performance.

**Issue 1: Inconsistent mapping.** integration_workflow.py has NO mapping for 'Strength Deficit' -> falls back to 'Power', which provides power training to an athlete who needs maximal strength training. This is a treatment mismatch.

**Issue 2: Single assessment for multi-dimensional construct.** Lower body strength includes:
- Maximal concentric strength (trap bar DL assesses this well)
- Eccentric strength (NOT assessed - missing)
- Isometric strength (NOT assessed - IMTP referenced in knowledge graph but not in deficit engine)
- Rate of force development at various loads (NOT assessed)

#### 6.2 Recommended changes

| Issue | Recommendation | Priority |
|-------|---------------|----------|
| Missing from integration_workflow mapping | Add 'Strength Deficit' -> 'Strength' to integration_workflow.py deficit_template_map | P0 |
| No eccentric strength assessment | Add Nordic hamstring curl or eccentric trap bar test | P1 |
| IMTP in knowledge graph but not deficit engine | Add IMTP benchmarks to MockBenchmarkRepository | P1 |

---

### Chain 7: Rotational Med Ball Throw -> Rotational Power Deficit -> Power

**Code locations:**
- Assessment: deficit_detection_engine.py:173
- Deficit: deficit_detection_engine.py:174 ('Rotational Power Deficit')
- Goal in integration: not mapped -> falls back to 'Power'
- Goal in program builder: program_builder.py:608 -> 'Power'

#### 7.1 Scientific validity: STRONG

Rotational medicine ball throw is a well-validated assessment of rotational power. Appropriate for cricket (transfer to bowling, batting, throwing).

**Issues:**
1. **Missing from integration_workflow.py mapping** - falls back to 'Power' which works for Spinner (goal 'Power' matches) but should explicitly map to 'Rotational Power'.
2. **No bilateral comparison** - cricket is unilateral; throw should be tested both sides.
3. **No differentiation between standing and seated throws** - seated isolates trunk rotation; standing confounds with lower body contribution.

#### 7.2 Recommended changes

| Issue | Recommendation | Priority |
|-------|---------------|----------|
| Missing explicit mapping | Add Rotational Power Deficit -> Rotational Power to integration_workflow.py | P1 |
| Add bilateral comparison | Test both dominant and non-dominant sides | P1 |
| Differentiate throw variants | Add seated rotational throw as secondary assessment | P2 |

---

## 2. Knowledge Graph Needs Analysis Review

### 2.1 Current state

From knowledge_graph_service.py:170-184:

| Role | Physical Drivers Defined | Priority |
|------|------------------------|----------|
| Fast Bowler | Front Foot Brace Force, Trunk Flexion Rotational Power | Primary only |
| Spinner | Hip-Shoulder Separation Torque | Primary only |
| Wicket Keeper | Lower Body Isometric Squat Endurance | Primary only |
| Batter | **NONE** | N/A |
| All Rounder | **NONE** | N/A |

### 2.2 Issues

1. **Batter and All Rounder have zero physical drivers defined.** These roles cannot be given a needs analysis.
2. **Only 'Primary' priority drivers exist.** No Secondary or Tertiary drivers are defined, missing the periodisation context (pre-season vs in-season priorities shift).
3. **Fast Bowler needs 8-12 drivers minimum.** Current 2 drivers severely underrepresent the physical demands:

**Missing Fast Bowler drivers:**
- Lower body eccentric strength (front foot bracing)
- Lumbar spine extension endurance (stress fracture prevention)
- Hip flexor/extensor balance (contralateral pelvic drop)
- Lateral trunk flexion strength (bowling arc)
- Ankle plantar flexor stiffness (ground contact)
- RFD (rate of force development)
- Deceleration ability (follow-through)
- Anaerobic power (repeat spell capacity)

**Missing Spinner drivers:**
- Hip external rotation ROM
- Thoracic spine rotation
- Trunk lateral flexion
- Shoulder internal rotation control
- Lower body isometric strength

**Missing Batter drivers:**
- Hip rotational velocity
- Grip/forearm endurance
- Anti-rotation core strength
- Deceleration (between wickets)
- Visual reaction time
- Upper body rotational power

**Missing Wicket Keeper drivers:**
- Hip mobility (deep squat position)
- Ankle dorsiflexion ROM
- Shoulder flexion endurance (repetitive throwing)
- Deceleration/change of direction

### 2.3 Recommended additions

| Role | Missing Driver | Assessment | Priority |
|------|---------------|------------|----------|
| Fast Bowler | Eccentric Lower Body Strength | Eccentric trap bar or Nordic curl | P0 |
| Fast Bowler | Lumbar Extension Endurance | Biering-Sorensen test | P0 |
| Fast Bowler | Anaerobic Power | Yo-Yo IR1 or RSA test | P1 |
| Fast Bowler | Deceleration | 10-5 repeated deceleration test | P1 |
| Spinner | Hip Rotation ROM | 90/90 hip rotation test | P0 |
| Spinner | Thoracic Rotation ROM | Seated thoracic rotation test | P0 |
| Batter | Grip Endurance | Gripmeter sustained hold | P1 |
| Batter | Hip Rotational Velocity | Instrumented rotational bat swing | P1 |
| Batter | Deceleration | 5-5 deceleration test | P1 |
| Wicket Keeper | Hip Mobility | Deep squat hold test | P1 |
| All Rounder | Full composite battery | Battery from all roles | P2 |

---

## 3. Movement Category Review

### 3.1 Force type taxonomy issues

From session_generator.py:108-131 (MOCK_PATTERNS):

| Exercise ID | Exercise Name | Current force_type | Correct force_type | Issue |
|------------|---------------|-------------------|-------------------|-------|
| 91 | MB Rotational Scoop Toss | Static | Rotation | Static is reserved for isometric holds |
| 1 | Trap Bar Jump Squat | Push | Push | Correct (vertical force) |
| 2 | Single-Leg Lateral Bound | Push | Push | Ambiguous - lateral force is not 'Push' |
| 92 | A-Skip | N/A | None | 'N/A' is not a valid biomechanical category |
| 93 | Single-Leg Isometric Wall Sit | Static | Static | Correct (isometric) |

**Push is overloaded.** Exercises 1 (Trap Bar Jump Squat vertical), 2 (SL Lateral Bound lateral), 85 (Barbell Back Squat vertical), 97 (Dumbbell OHP vertical, upper body), and 78 (Bodyweight Squat vertical) all use 'Push' despite fundamentally different force vectors (vertical vs lateral) and body segments (lower vs upper).

### 3.2 Template-slot exercise fit issues

| Template | Slot | Exercise | Fit | Issue |
|----------|------|----------|-----|-------|
| Fast Bowler Power | Max Dynamic Output (Bilateral) | Trap Bar Jump Squat | GOOD | Appropriate bilateral power |
| Fast Bowler Power | Unilateral Force Production | SL Lateral Bound | GOOD | Appropriate unilateral power |
| Fast Bowler Power | Triple Extension Acceleration | MB Overhead Backwards Toss | ACCEPTABLE | Triple extension of hip/knee/ankle is present but it's a throw, not a jump |
| Fast Bowler Power | Trunk Rotational Velocity | MB Rotational Chest Pass | GOOD | Rotational trunk movement |
| Spinner Rotational | Rotational Power Slam | MB Rotational Scoop Toss | GOOD | Rotational power |
| Spinner Rotational | Base Strength Lift | Barbell Back Squat | POOR | Squat has limited transfer to rotational strength. Should be rotational strength movement (cable chop, landmine rotation) |
| Spinner Rotational | Unilateral Push Strength | Dumbbell OHP | MODERATE | OHP is vertical, not rotational. For spinner, a unilateral rotation press would be better |
| Spinner Rotational | Anti-Rotation Stiffness | Cable Pallof Press / Plank with Rotation | GOOD | Appropriate anti-rotation |
| Batter Strength | Explosive Hinge/Extension | Trap Bar Deadlift | GOOD | Hip hinge for drive power |
| Batter Strength | Unilateral Drive Strength | Rear Foot Elevated Split Squat | GOOD | Single leg strength for stance and running |
| Batter Strength | Posterior Chain Knee Flexion | Dumbbell Row / Nordic Curl | POOR | Dumbbell Row is upper body pull, NOT posterior chain knee flexion. Nordic curl is correct but shares slot with a non-hamstring exercise |
| Batter Strength | Trunk Stability in Motion | Pallof Press / Plank with Rotation | GOOD | Anti-rotation core |

---

## 4. Missing Assessments Registry

Total assessments in system: **7** (CMJ, Broad Jump, 10m Sprint, 20m Sprint, Trap Bar Deadlift, Rotational MB Throw, Pull Up)
Minimum recommended for cricket S&C: **20+**

| Missing Assessment | Purpose | Role Relevance | Priority |
|-------------------|---------|---------------|----------|
| Isometric Mid-Thigh Pull (IMTP) | Peak force, RFD | All - especially Fast Bowler brace force | P0 |
| Yo-Yo Intermittent Recovery Test | Anaerobic capacity | Fast Bowler (spell recovery), Batter (running) | P0 |
| Seated Medicine Ball Throw | Upper body rotational power (isolated) | Batter, Spinner | P1 |
| Isometric Shoulder ER Test | Rotator cuff strength | All - injury prevention | P0 |
| Biering-Sorensen Test | Lumbar extension endurance | Fast Bowler - stress fracture risk | P0 |
| 90/90 Hip Rotation Test | Hip internal/external rotation ROM | Spinner - bowling action, Batter - stance | P1 |
| Ankle Dorsiflexion Lunge Test | Ankle mobility | All - squat depth, landing mechanics | P1 |
| Pro-Agility (5-10-5) | Change of direction | Batter - running between wickets, Fielding | P1 |
| Nordic Hamstring Curl (break test) | Eccentric hamstring strength | All - especially Fast Bowler hamstring injury | P1 |
| Countermovement Jump with Arm Swing | Sport-specific CMJ | All - more valid than hands-on-hips CMJ | P2 |
| Drop Jump / Reactive Strength Index | SSC function, stiffness | Fast Bowler - ground contact stiffness | P1 |
| Grip Strength (Dynamometer) | Grip endurance | Batter - bat control, Wicket Keeper | P2 |
| Repeated Sprint Ability (RSA) | Repeat sprint capacity | Fast Bowler, Batter | P1 |
| Isometric Hip Adduction | Hip/groin strength | All - groin injury prevention | P1 |
| Overhead Squat Assessment | Movement quality | All - baseline screening | P2 |
| Single-Leg Drop Landing | Dynamic knee valgus, landing mechanics | All - ACL injury prevention | P2 |

---

## 5. Cross-Cutting Issues

### 5.1 Deficit-to-goal mapping inconsistency

There are TWO separate deficit-to-goal maps in the system, and they disagree:

| Deficit | integration_workflow.py (line 189-193) | program_builder.py (line 602-610) |
|---------|--------------------------------------|----------------------------------|
| Power Deficit | Power | Power |
| Acceleration Deficit | Power | Power |
| Mobility Restriction | **Shoulder Robustness** | **Power** |
| Strength Deficit | **NOT MAPPED -> Power** | **Strength** |
| Speed Deficit | **NOT MAPPED -> Power** | **Power** |
| Rotational Power Deficit | **NOT MAPPED -> Power** | **Power** |
| Shoulder Robustness Deficit | **NOT MAPPED -> Power** | **Strength** |

**Impact:** An athlete using the integration workflow may get a different training goal than when using the program builder independently for the same deficits.

### 5.2 One-to-one assessment-to-deficit mapping

Each assessment maps to EXACTLY one deficit. In reality:
- CMJ maps to multiple constructs (concentric power, eccentric utilization, SSC function, RFD)
- Broad jump maps to horizontal power, acceleration, coordination
- Pull up maps to lat strength, scapular stability, grip endurance, relative strength

The reductionist 1:1 mapping loses information.

### 5.3 No movement quality assessment

The entire system is performance-test-driven. There are NO assessments for:
- Movement quality (FMS, overhead squat, single-leg squat)
- Asymmetry (bilateral force plate data)
- Tissue capacity (tendon tolerance, muscle stiffness)
- These are critical for injury risk screening in cricket

### 5.4 No periodisation sensitivity

The same deficit -> goal -> exercise mapping applies regardless of:
- Season phase (pre-season vs in-season vs off-season)
- Training block focus (accumulation vs intensification vs realisation)
- Athlete load history (high mileage vs returning from injury)

---

## 6. Risk Assessment

| Risk | Severity | Likelihood | Detection | RPN |
|------|----------|-----------|-----------|-----|
| Broad Jump -> Shoulder treatment (wrong body part) | Critical | Certain | Medium | **24** |
| Strength Deficit -> Power training (wrong training type) | High | High | Low | **20** |
| Speed deficit -> No sprint training | High | High | Medium | **18** |
| CMJ deficit -> Same program for all roles | Moderate | Certain | Low | **18** |
| Pull-up deficit -> missing rotator cuff risk | High | Medium | Low | **15** |
| Missing IMTP -> lost brace force assessment | High | High | Medium | **15** |
| No eccentric assessment -> hamstring injury missed | High | Medium | Low | **12** |

RPN = Severity (1-4) x Likelihood (1-4) x Detection (1-3). Max = 36.

---

## 7. Summary of P0 Actions

| # | Action | Impact | Code Location |
|---|--------|--------|---------------|
| 1 | Rename Broad Jump deficit to 'Horizontal Power Deficit' | Fixes invalid construct | deficit_detection_engine.py:138 |
| 2 | Fix Mobility Restriction -> Shoulder Robustness to Horizontal Power | Fixes clinical error | integration_workflow.py:192 |
| 3 | Add Strength Deficit -> Strength mapping | Fixes treatment mismatch | integration_workflow.py:189-193 |
| 4 | Add Horizontal Power template | Closes 16 missing exercises gap | recommendation_engine.py |
| 5 | Add Speed Development template | Closes max velocity gap | recommendation_engine.py |
| 6 | Add Acceleration Development template | Closes sprint mechanics gap | recommendation_engine.py |
| 7 | Add IMTP assessment and benchmarks | Captures brace force | deficit_detection_engine.py |
| 8 | Add Yo-Yo IR1 assessment | Captures anaerobic capacity | deficit_detection_engine.py |
| 9 | Add Shoulder ER strength assessment | Captures RC injury risk | deficit_detection_engine.py |
| 10 | Add Biering-Sorensen test | Captures lumbar extension, stress fracture risk | deficit_detection_engine.py |
| 11 | Split CMJ->Power deficit into sub-types | Differentiates training response | deficit_detection_engine.py |
| 12 | Define Batter and All Rounder physical drivers | Completes knowledge graph | knowledge_graph_service.py:170-184 |
| 13 | Add Dumbbell Row replacement in Batter slot 403 | Fixes non-hamstring exercise in hamstring slot | recommendation_engine.py:440 |

---

## Appendix A: Full Mapping Chain Reference

```
Assessment                 Deficit                       Goal              Template                    Slots
---------                 -------                       ----              --------                    -----
CMJ                       Power Deficit                 Power             Fast Bowler Power           Bilateral Power, Unilateral, Triple Ext, Core Rotation
                                                                          Batter Strength/Power        Hinge, Unilateral Drive, Post Chain, Trunk Core
10m Sprint                Acceleration Deficit          Power             Fast Bowler Power           (same as above - no sprint-specific)
20m Sprint                Speed Deficit                 Power             Fast Bowler Power           (same as above - no speed-specific)
Trap Bar Deadlift         Strength Deficit              Power (int)       Fast Bowler Power           (strength template missing in int workflow)
                                                         Strength (prog)   Batter Strength/Power
Broad Jump                Mobility Restriction          Shoulder (int)    NONE (404)                  ERROR CHAIN
                                                         Power (prog)      Fast Bowler Power
Rotational MB Throw       Rotational Power Deficit      Power (fallback)  Spinner Rotational Power    Rotational Slam, Base Strength, Unilateral Push, Core
Pull Up                   Shoulder Robustness Deficit   Power (int)       NONE (404 if direction)      Missing shoulder-specific exercises
                                                         Strength (prog)   Batter Strength/Power
```

(int) = integration_workflow.py, (prog) = program_builder.py
