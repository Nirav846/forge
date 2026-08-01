# AUDIT #11 — SPORTS SCIENCE & COACHING LOGIC VALIDATION

**Role:** Elite Performance Director + Applied Sports Scientist + High Performance Coach + S&C Architect
**Date:** 2026-06-17
**Scope:** Training philosophy, coaching methodology, sports science validity — NO code, NO architecture, NO APIs

---

## Executive Summary

Forge embeds a **deficit-driven, demand-based programming philosophy** with V1 and V2 ontology layers. The methodology is **conceptually sound but practically incomplete for production deployment** in any sport context. The model works for a narrow band of athletes (developing team-sport athletes in a well-equipped setting with a single goal: get stronger/powerful) and breaks in almost every real-world scenario an S&C coach faces.

The fundamental problem: **the model confuses "correct biomechanics" with "good coaching."** The demand ontology is biomechanically coherent — each demand pairs a movement pattern with a physical quality. But coaching is not biomechanics applied linearly. It is load management, skill acquisition, psychosocial interaction, periodization artistry, and injury prevention woven together. The model captures only the first of these.

**Overall Grade: 34/100 — Weak Foundation, Major Gaps**

---

## Section 1 — Demand Model Validation

### The Current Model

```
Assessment → Benchmark → Deficit → Demand → Exercise Priority → Program
```

V1 uses 5 qualities: Strength, Power, Acceleration, Speed, Rotational Power.
V2 uses 18 performance demands across 4 types (Biomotor, Sensory-Motor, Metabolic, Cognitive) — but only Biomotor demands are seeded.

### What the Model Does Well

1. **Biomechanical coherence** — V2's demand structure (quality × movement pattern) correctly reflects that RFD in a squat is different from RFD in a hinge. This is a genuine insight.
2. **Role differentiation** — Different priority demands for Fast Bowler vs Spinner vs Batter (V2 seed) is sport-science correct.
3. **Assessment traceability** — Linking each demand to specific assessment metrics (V2 C1-C2) enables precise deficit localisation.
4. **Directionally correct for novices** — A beginner athlete with obvious weaknesses will benefit from this structured approach.

### What's Missing — The Gaps

| Missing Concept | Why It Matters | Breaks For... |
|----------------|----------------|---------------|
| **Sport-specific skill work** | No model for technical training (bowling practice, batting drills, position-specific work). Forge treats all training as S&C. | Every sport athlete — team practice IS the training |
| **Team training load** | Athletes don't just do S&C. They train with their team. Forge has no concept of practice load, game load, or how S&C interacts with sport training. | Team sport athletes |
| **Multiple concurrent demands** | An athlete has 5+ demands at once. The model picks deficits linearly. Real coaching balances competing demands simultaneously. | All athletes |
| **Demand interaction** | Improving Squat Strength may improve Vertical Power. The model treats demands as independent. | All athletes — transfer effects are ignored |
| **Maintenance vs Development** | In-season, the goal is to MAINTAIN strength, not develop it. The model only knows "deficit = train more." | In-season athletes |
| **Fatigue-dependent demand state** | An athlete's demand profile changes under fatigue. A fresh athlete has different needs than a fatigued one. | Tournament, in-season, high-volume athletes |
| **Peaking vs General Preparation** | No concept of phase-appropriate demand emphasis. Pre-season should target different demands than competition phase. | Periodised athletes |
| **Tactical/strategic demands** | "Be able to bowl 10 overs at 90mph on day 5" is a real demand. The model cannot represent it. | Elite sport |
| **Psycho-social demands** | Confidence, motivation, coach-athlete relationship, group dynamics. These drive programming decisions daily. | Real-world coaching |
| **Maturation status** | Youth athletes need different demands based on PHV, not training age. The model uses training_age_months → development level. | Youth athletes |
| **Injury history modification** | An athlete with recurrent hamstring strains should have different demand priorities regardless of test scores. | Return-to-play, chronic injury athletes |
| **Sex-specific considerations** | Female athletes have different ACL risk profiles, different strength ratios, different periodisation needs. | Female athletes |

### Situational Analysis

| Sport Type | Does the Model Work? | Why/Why Not |
|-----------|---------------------|-------------|
| **Team sports (Cricket, Rugby, Football)** | Partially — In off-season general preparation only | Cannot model sport-specific training load, position-specific tactical demands, in-season maintenance, or competition congestion |
| **Individual power sports (Sprint, Jump, Throw)** | Weak — Too generic | Elite sprinters need highly specific track work, not generic "Horizontal Drive Power" → Clean Pull. Skill/track sessions are the primary stimulus, not gym work |
| **Combat sports (Boxing, Wrestling, BJJ)** | Fails | No weight-cutting model, no striking/grappling-specific force production, no fight camp periodisation, no skill-sparring load management |
| **Endurance sports (Cycling, Running, Rowing)** | Fails | No aerobic threshold, anaerobic threshold, VO2max, lactate clearance, or aerobic efficiency concepts. Demands are purely force-based |
| **Youth athletes (U14-U18)** | Fails | No maturation adjustment, no skill development model, no playful/athletic development approach. 18 demands are too granular for a developing athlete |
| **Elite athletes (International/Pro)** | Fails — Model is too rigid | Elite athletes require nuanced programming: small windows of adaptation, highly specific stimuli, complex periodisation, psychological management. A deficit-driven rule engine cannot deliver this |

### Demand Model Score: **42/100**

Reasons:
- +20 for biomechanical coherence and V2 ontology design
- +10 for assessment traceability
- -15 for missing almost every real-world coaching consideration
- -15 for no team training load or sport-skill integration
- -10 for no in-season maintenance concept
- -8 for linear deficit→demand→exercise pipeline
- -10 for no multi-demand interaction model
- -10 for no maturation/sex/injury-history modification

---

## Section 2 — Deficit-Driven Programming Review

### The Philosophy

*"The largest deficits receive the greatest training emphasis."*

This is the central assumption of Forge. It sounds logical: fix the weakest link. But **it is frequently wrong at elite and in-season levels.**

### When It Is Correct

1. **Novice/developing athletes (Foundation/Development levels)** — A beginner with clear weaknesses benefits from targeted strengthening.
2. **Off-season general preparation** — Adequate time to address weaknesses without performance sacrifice.
3. **Return from de-training (post-injury layoff, off-season break)** — Multiple deficits exist and need broad attention.
4. **Athletes with genuine asymmetry/injury risk** — e.g., 15% inter-limb deficit in IMTP warrants focused attention.
5. **Screen/benchmark failures** — If an athlete cannot meet minimum requirements for their role/sport.

### When It Is Wrong

1. **Elite athletes near physiological ceiling** — The gap between "elite" and "elite + 2%" is tiny. Chasing deficits at this level means neglecting the qualities that make the athlete elite. An elite sprinter with "average" squat strength does NOT need to squat more — they need to sprint faster. The strength deficit is not performance-limiting.
2. **In-season** — Deficit-focus during season means neglecting maintenance of high-performance qualities. An in-season fast bowler with a "mobility restriction" cannot spend 3 sessions/week on mobility without losing power/speed.
3. **Pre-competition/taper** — The week before a competition is not the time to attack deficits. The model has no "peak and maintain" logic.
4. **Return-to-play (late stage)** — After basic strength is restored, the focus must shift to sport-specific re-integration, not remaining deficits in other qualities.
5. **Athletes with 5+ moderate deficits** — Focusing on the top 1-2 creates massive opportunity cost in the other 3-4 qualities. Real coaches periodise across all qualities over a macrocycle.
6. **When the best predictor of future performance is past performance** — The deficit model ignores what the athlete is GOOD at. Often, the best strategy is to reinforce strengths and manage weaknesses, not invert this priority.
7. **In a congested calendar** — Deficit-focused programming risks doing too much with insufficient recovery.

### The Opportunity Cost Problem

A 4-session/week program with 5 qualities across program_design_rules:

| Quality | Frequency | Sets × Reps | Weekly Volume |
|---------|-----------|-------------|---------------|
| Strength (deficit #1) | 3×/week | 4×5 | 60 reps |
| Power (deficit #2) | 2×/week | 4×4 | 32 reps |
| Acceleration | 2×/week | 5×10m | 100m |
| Speed | 1×/week | 4×30m | 120m |
| Rotational Power | 2×/week | 4×5 | 40 throws |

If the model doubles down (Strength at 5×/week, making Power at 1×/week), the athlete loses 32 power reps and 200m of speed work weekly. The lost power and speed work are **opportunity cost** — and could be more detrimental to performance than the strength deficit ever was.

### The Skill-Specificity Problem

Not all deficits can be fixed in the gym. Some deficits are technical/tactical:

- Poor 10m sprint time → may be starting mechanics (skill), not force production
- Poor rotational velocity → may be technique, not core power
- Poor throwing accuracy → skill, not strength

The model assumes every deficit has an exercise-based solution. This is false.

### Deficit Programming Score: **31/100**

Reasons:
- +15 for correct in principle for novices and off-season
- +5 for linking deficits to specific exercises via templates
- -25 for no in-season maintenance logic
- -15 for no opportunity cost model
- -10 for no "good enough" thresholds
- -10 for assuming exercise-based solutions to all deficits
- -5 for no competition phasing
- -5 for no strength/weakness balance model
- -4 for no elite ceiling concept

---

## Section 3 — Assessment Battery Review

### Current Assessments

| Assessment | What It Measures | Reliability | Validity | Transfer | Practicality |
|-----------|-----------------|-------------|----------|----------|-------------|
| **CMJ (Force Plate)** | Vertical jump height, peak power, RFD | High (0.95+) | High for lower body power | Moderate | Low (needs force plates) |
| **CMJ (without force plates)** | Jump height only | Moderate (0.80) | Moderate | Moderate | High (justathrow/contact mat) |
| **IMTP** | Peak force, absolute strength | High (0.95+) | High for isometric strength | Moderate | Low (needs force plates + rack) |
| **Broad Jump** | Horizontal power, triple extension | High (0.90) | Moderate | Moderate | High (tape measure) |
| **10m Sprint** | Acceleration | High (0.95) | High | High | Moderate (needs timing gates) |
| **20m Sprint** | Max velocity | High (0.95) | High | High | Moderate (needs timing gates) |
| **Pull Up (max reps)** | Relative upper body pulling endurance | Moderate (0.80) | Moderate | Low (endurance-dominant) | High |
| **Trap Bar Deadlift (3RM)** | Lower body absolute strength | High (0.95) | High | High | Moderate (needs trap bar) |
| **MB Rotational Throw** | Rotational power | Moderate (0.85) | Moderate | Moderate | Moderate (needs radar/velocity) |
| **Isometric Wall Sit** | Isometric lower body endurance | Low (0.70) | Low (motivation-dependent) | Low | High |

### What Is Measured — Coverage Map

| Quality | Measured? | Assessment |
|---------|-----------|------------|
| Lower body power (vertical) | ✓ | CMJ |
| Lower body power (horizontal) | ✓ | Broad jump |
| Lower body absolute strength | ✓ | IMTP, Trap Bar Deadlift |
| Upper body pulling strength | ✓ (but endurance-based) | Pull up (max reps) |
| Rotational power | ✓ | MB Rotational Throw |
| Acceleration | ✓ | 10m Sprint |
| Max velocity | ✓ | 20m Sprint |
| Isometric endurance | ✓ | Wall Sit |

### Critical Gaps — What Is NOT Measured

| Quality | Why Critical | Sport Impact |
|---------|-------------|--------------|
| **Eccentric strength** | No Nordic curl, no eccentric hamstring test. Hamstring injuries are #1 in most field sports. Cannot assess or monitor eccentric capacity. | Cricket, Rugby, Football, Sprinting |
| **Aerobic capacity (VO2max)** | No beep test, no yo-yo test, no 2km time trial. Cannot assess baseline fitness or monitor conditioning. | All team sports, endurance sports |
| **Anaerobic power / Repeat sprint ability (RSA)** | No repeat sprint test, no anaerobic capacity test. Cannot assess ability to recover between high-intensity efforts. | All team sports, combat sports |
| **Agility / COD (Change of Direction)** | No 5-0-5, no Illinois, no Pro-Agility. Cannot assess deceleration or cutting ability. | All field/court sports |
| **Active mobility (specific)** | No overhead squat assessment, no dorsiflexion lunge, no 90/90 hip rotation. Generic "range of motion" not captured. | All athletes |
| **Landing mechanics** | No drop jump, no landing error scoring system. Cannot assess ACL risk. | Female athletes, youth, RTP |
| **Core endurance (specific)** | No McGill test battery, no side plank endurance. General core not assessed. | All athletes |
| **Hamstring flexibility** | No active straight leg raise, no sit-and-reach. Cannot screen for posterior chain injury risk. | Sprint/field athletes |
| **Shoulder stability/strength** | No Y-Balance upper, no closed kinetic chain upper extremity test. Cannot screen overhead athletes. | Cricket (bowlers), throwers |
| **Anthropometrics / Body composition** | No skinfolds, no circumference measures. Cannot track morphological adaptation. | All athletes (weight-class, body-conscious, hypertrophy phases) |
| **Subjective wellness** | No mood, fatigue, soreness, sleep, stress tracking (except via JSONB). Cannot adjust training based on daily readiness. | All athletes — critical for daily decision-making |
| **HRV/Resting heart rate** | No physiological readiness metric. Cannot objectively assess recovery state. | All athletes |
| **Blood markers** | No ferritin, vitamin D, creatine kinase tracking. Cannot detect overtraining or nutritional deficiencies. | Elite athletes, high-volume athletes |
| **Sleep quality/quantity** | No sleep tracking. Single biggest recovery variable, completely unmeasured. | All athletes |

### Assessment Battery Redundancy

| Assessment Pair | Redundancy | Recommendation |
|----------------|------------|---------------|
| 10m Sprint + 20m Sprint | Moderate — split 10m velocity and max velocity are distinct qualities, but both are sprint-derived. Can use a single 30m fly with split times. | Keep both, but derive from single sprint |
| CMJ + Broad Jump | Low — vertical vs horizontal power are distinct | Keep both |
| IMTP + Trap Bar Deadlift | High — both measure absolute lower body strength | Drop one (keep Trap Bar DL — dynamic, sport-specific) |

### Assessment Coverage Score: **39/100**

Reasons:
- +10 for core power/strength/speed battery
- +5 for rotational power assessment (often missed)
- +5 for good reliability on force-plate assessments
- -25 for missing eccentric hamstring assessment
- -15 for no aerobic/anaerobic capacity
- -10 for no agility/COD
- -10 for no subjective wellness/readiness
- -5 for no HRV/physiological readiness
- -5 for no mobility battery
- -5 for no landing mechanics
- -5 for no body composition
- -3 for IMTP+Deadlift redundancy
- -2 for wall sit low validity

---

## Section 4 — Exercise Prescription Logic

### Current Model

```
Demand (V2: movement_pattern × physical_quality) 
  → exercise_demand_mapping (relevance_score, is_primary)
  → Template slot matching (slot_requirements: movement_pattern, quality, training_method, equipment, difficulty_level)
  → Default exercise (default_exercise_id on template_slot)
  → Fallback (slot_exercise_fallbacks: preferred_exercise → fallback_exercise)
  → → If all fail: no exercise recommended
```

### What Works

1. **Movement pattern + quality matching is biomechanically sound** — It ensures a "power" slot gets power exercises.
2. **Sport specificity scoring** — transfer_index and specificity_rating allow prioritisation.
3. **Development level gating** — Ensures a Foundation athlete doesn't get a Split Jerk.
4. **Fallback chains** — When preferred exercise unavailable, fallback exists (only 2 seeded, but concept is sound).

### What Is Missing — The Critical Gaps

**1. No individual anatomy/limb length scaling**

A 6'5" fast bowler needs a different squat stance and Deadlift setup than a 5'8" spinner. The model prescribes "Trap Bar Deadlift" generically. Every experienced S&C coach adjusts exercise selection based on individual anthropometrics.

**2. No injury history modification**

An athlete with chronic patellar tendinopathy should NOT receive "Trap Bar Jump Squat" as a default, regardless of demand match. The model has no injury-type → exercise contraindication mapping. The `injury_risk_demand_mapping` table exists (V2 A5) but is empty — 0 rows seeded.

**3. No equipment context**

The model assumes fully-equipped gym: barbells, trap bars, force plates, cable machines, medicine balls. Real-world constraints:
- High school gym = dumbbells to 50lbs, no trap bar
- Away tour = hotel gym with 2 cables and dumbbells
- Home gym = bodyweight + resistance bands
- Low-budget program = limited equipment

The model has no "minimum equipment" vs "ideal equipment" distinction. `exercise_equipment` table exists but has no priority context.

**4. No exercise variants**

The model treats "Barbell Back Squat" as one exercise. Experienced S&C coaches use:
- High-bar vs low-bar squat
- Pause squat
- Pin squat
- Front squat
- Safety bar squat
- Belt squat
- Box squat

Each is a different stimulus. The model has no variant system.

**5. No tempo prescriptions**

"3x5 at 80%" is missing the eccentric duration, isometric pause, and concentric intent. Real prescription:
- 3×5 @ 80% — 3-0-X-0 (3s eccentric, no pause, explosive concentric)
- 3×5 @ 80% — 3-2-X-0 (3s eccentric, 2s pause, explosive concentric)

These produce very different adaptations.

**6. No set/rep scheme rationale**

The model prescribes sets×reps from program_design_rules (e.g., "3-5 sets × 3-6 reps"). But there's no logic for WHY:
- Hypertrophy stimulus: 3×8-12 at 65-75%
- Strength stimulus: 4×3-5 at 80-90%
- Power stimulus: 5×2-3 at 30-50%

The ranges are wide enough to be meaningless. A coach needs specificity based on phase goal.

**7. No RPE/session context**

Whether an exercise is prescribed early or late in a session matters enormously for quality and safety. The model has no session ordering or fatigue-aware exercise placement.

**8. No warm-up or cool-down**

Real programs have a structured warm-up (activation, movement prep, potentiation) and cool-down (de-load, stretch, mobility). The model doesn't generate these.

**9. No exercise rotation/diversity**

The model has no rule to prevent the same exercise appearing every block for years. Real coaches rotate exercises every 3-6 weeks to prevent accommodation and maintain novelty.

### Transfer Index Critique

The model uses a single `transfer_index` (0-1) to represent how well an exercise transfers to a sport. This is **too simplistic**:

- **Clean Pull → Cricket** = 0.70: But transfer index changes with phase. In off-season general preparation, 0.70 is fine. In pre-season, 0.70 is not enough — need more specific work.
- **Contralateral limb transfer**: A left-leg RFESS transfers differently to right-leg sprint stance phase.
- **Force-vector mismatch**: An exercise with high transfer index but wrong force vector (vertical force for a horizontal athlete) has near-zero real transfer.

### Exercise Selection Score: **28/100**

Reasons:
- +10 for biomechanical demand→exercise matching foundation
- +5 for sport specificity scoring concept
- +5 for development level gating
- -20 for no injury history modification
- -15 for no equipment context
- -10 for no exercise variants
- -10 for no tempo/execution prescription
- -5 for no session context/ordering
- -5 for no warm-up/cool-down
- -5 for transfer index too simplistic
- -3 for only 2 fallback pairs seeded
- -2 for no rotation/diversity rule

---

## Section 5 — Progression Model Review

### Current Progression Types (from slot_progressions)

| Type | Example | How It Works |
|------|---------|-------------|
| **Linear Loading** | "Add 2.5-5kg weekly" | Fixed load increase per time unit |
| **Double Progression** | "Increase reps from 6→8, then add load" | Reps progress first, then load |
| **Velocity-Based** | "Maintain 0.75-0.90 m/s, add load if faster" | Bar speed determines load adjustment |
| **Qualitative/Technique** | "Increase jump height while maintaining form" | Quality threshold before load increase |
| **RPE-Based** | "All sets below RPE 9, then add load" | Perceived effort determines readiness to progress |

### Scientific Validity Assessment

**Linear Loading (used for Strength in all cricket roles)**
- ✅ Works for novice athletes (6-12 weeks)
- ❌ Fails for intermediate/advanced (plateaus within 4-6 weeks)
- ❌ No autoregulation — same 2.5kg for a 200kg deadlifter and 100kg squatter affects them differently
- ❌ No fatigue management — linear increase assumes constant recovery capacity
- ⚠️ Evidence: Linear periodisation is inferior to undulating/conjugate for strength gains in trained athletes (Rhea et al., 2003; Kraemer & Ratamess, 2004)

**Double Progression (used for Spinner Strength)**
- ✅ More flexible than pure linear
- ✅ Good for hypertrophy-oriented phases
- ⚠️ Slow — a 6→8 rep progression can take 4+ weeks
- ❌ At higher intensities (>85%), adding reps before load is physiologically different stimulus (becomes endurance work)

**Velocity-Based Training (used for Power/Fast Bowler)**
- ✅ Best available autoregulation method
- ✅ Evidence-based (Mann et al., 2020)
- ❌ Requires velocity-measuring device (GymAware, Vmaxpro, etc.) — elite-only equipment
- ❌ Zone too narrow (0.75-0.90 m/s) — doesn't account for daily fatigue variation

**Qualitative/Technique (used for Power/Acceleration in most roles)**
- ✅ Correct in principle — quality before quantity
- ❌ Nearly impossible to automate — "good form" is coach's subjective judgment
- ❌ No rule for "how much quality regression is too much"
- ⚠️ Works in theory, fails in practice without human oversight

### Progression Rate vs Development Level

The model has FOUNDATION → DEVELOPMENT → PERFORMANCE levels, but:
- **No progression velocity differentiation**: A FOUNDATION athlete can progress faster (2.5kg/session) than a PERFORMANCE athlete (same exercise, same increment). The model applies the same progression rule regardless of level.
- **No detraining/re-accommodation**: After a 2-week break, the model assumes the athlete can resume at previous load. Real coaching requires 1-2 weeks of "re-introduction."
- **No stall/deload rule**: When an athlete fails to complete prescribed reps at a given weight, the model has no intervention. Real coaches: "Missed 5×3 at 120kg → repeat weight next week, or deload 10%."

### What Is Missing

| Missing Progression Concept | Why Critical |
|----------------------------|-------------|
| **Undulating periodisation** | Daily/weekly variation in volume and intensity produces better strength gains than linear (Rhea 2003) |
| **Autoregulation (beyond VBT)** | RPE-based autoregulation (APRE method), set-rep best, max reps test — needed when VBT unavailable |
| **Wave-loading** | 3-week waves: heavy/medium/light — prevents accommodation, manages fatigue |
| **Block progression** | Accumulation → Intensification → Realization → Deload (4-6 week blocks) |
| **Stall management** | What happens when the athlete can't complete the prescribed work? Repeat? Deload? Regress exercise? |
| **Rate of progression limits** | How fast is too fast? 5kg/week on squat leads to 20kg/month = 60kg in 12 weeks — unrealistic for most |
| **Exercise regressions** | When an athlete fails an exercise, what's the easier version? Trap Bar Jump Squat → Bodyweight Jump Squat → Pogo Jumps |
| **Session-to-session variation** | Same exercise 3×/week = accommodation. Real DUP: Mon heavy (5×3 @ 85%), Wed medium (4×5 @ 75%), Fri light (3×8 @ 65%) |

### Progression Score: **25/100**

Reasons:
- +10 for recognising multiple progression methods
- +5 for VBT inclusion (best available)
- +5 for qualitative progression principle
- -15 for linear-only in strength domain
- -15 for no undulating/conjugate options
- -10 for no stall/deload management
- -10 for no progression velocity by development level
- -10 for no exercise regression pathway
- -5 for no detraining/re-accommodation
- -5 for no session-to-session DUP variation

---

## Section 6 — Periodization Review

### Current Support

The model has:
- `programs`: 4-week blocks, `sessions_per_week` (2-4)
- `program_weeks`: `week_number` (1-4), `focus` (Base/Accumulation/Peak/Deload)
- `program_sessions`: up to 4 sessions/week, sequential
- `program_session_exercises`: sets, reps, intensity, rest_seconds, display_order
- `athlete_state_snapshots`: readiness/fatigue/recovery/injury_risk over time
- `training_load_events`: session RPE × duration for ACWR

### Analysis of Periodization Concepts

| Concept | Supported? | How |
|---------|-----------|-----|
| Linear periodisation | Partial | 4-week block with focus labels, but no volume/intensity manipulation across weeks |
| Block periodization | No | No accumulation→intensification→realisation progression within or across blocks |
| Undulating (DUP) | No | No daily variation in volume/intensity |
| Conjugate | No | No simultaneous training of contradictory qualities (SME/flexibility alongside max strength) |
| Tapering | No | Competition week = week 4 of program, but "Peak" focus has no defined taper protocol |
| Season integration | No | No off-season / pre-season / in-season / post-season phasing |
| Competition calendar | No | No concept of competition days, travel days, recovery days post-competition |
| Mesocycle linkage | No | Blocks are independent — no load/volume progression across multiple 4-week blocks |

### What "Focus" Currently Means

The `focus` column offers: Base, Accumulation, Peak, Deload. This looks like periodization but is **just labels**. There is no logic that:

- Week 1 (Base): higher volume, lower intensity
- Week 2 (Accumulation): peak volume, moderate intensity
- Week 3 (Peak): lower volume, higher intensity
- Week 4 (Deload): reduced volume and intensity

Every exercise in every week gets the same prescription format — sets and reps don't vary by week focus. The `program_design_rules` seed data doesn't have phase-specific prescriptions. Unless the recommendation engine explicitly manipulates volume/intensity per week focus (which no seed data supports), the focus labels are decorative.

### Periodization Readiness Score: **18/100**

Reasons:
- +5 for having a week_focus column (conceptually correct)
- +5 for 4-week block structure (base unit for periodization)
- +3 for athlete_state_snapshots (enables fatigue monitoring)
- +3 for training_load_events + ACWR (enables load management)
- -25 for no volume/intensity manipulation across weeks
- -20 for no season/phase differentiation
- -15 for no competition calendar integration
- -10 for no block/undulating/conjugate options
- -8 for no taper protocol
- -5 for focus labels being decorative (no logic driving them)
- -3 for no mesocycle linkage

---

## Section 7 — Recovery & Load Management Review

### Current Model Components

1. **training_load_events** — Session RPE × duration, plus optional external load (sprint count, jump count, throw count, high-speed distance)
2. **acute_chronic_load_view** — ACWR = 7-day acute / 28-day chronic (normalised to 7-day equivalent)
3. **athlete_state_snapshots** — Daily readiness (0-100), fatigue (0-100), recovery (0-100), injury_risk (0-100), demand states
4. **injury_risk_profiles** — Risk level (low/moderate/high/critical), score breakdown, risk factors, recommended interventions

### ACWR Critique

**What ACWR does well:**
- Retrospective load monitoring
- Flagging when chronic load is too low (de-training) or acute load spikes too high (injury risk)

**What ACWR does NOT do:**
- **Is it scientifically defensible?** — **Barely.** The original ACWR research (Gabbett 2016) has been heavily criticised:
  - Methodological flaws: Hulin et al. re-analyses found the "sweet spot" is a statistical artefact (Wang et al. 2020)
  - ICC variability: ACWR varies enormously depending on what load metric you use (sRPE vs GPS distance vs PL)
  - Publication bias: Studies finding no relationship between ACWR and injury are less published
- **Does it predict injury?** — Modest at best. Recent meta-analyses show ACWR explains <10% of injury variance (Impellizzeri et al. 2020, 2021)
- **Does it account for context?** — No. Same ACWR of 1.5 means different things for:
  - A 20-year-old vs 35-year-old
  - A well-slept vs sleep-deprived athlete
  - A low-stress vs high-stress period
  - A fully fit vs returning-from-injury athlete

**Alternative models missing:**
- **Individualised ACWR** — Each athlete has a different "normal" range
- **Exponentially weighted moving average (EWMA)** — Better than simple rolling average at detecting recent load spikes (Williams et al. 2020)
- **Total workload + monotony + strain** — Foster's model (3+ day strain index) captures training stress better than ACWR alone
- **RPE load + wellness composite** — Combining subjective wellness (sleep, soreness, mood, stress) with load metrics is more predictive than load alone

### Readiness Model Critique

`athlete_state_snapshots` captures readiness, fatigue, recovery, and injury_risk as 0-100 scores. But:

**Where do these scores come from?** The model has no:
- Subjective wellness questionnaire (sleep quality, soreness, mood, stress)
- HRV/metric data integration (no HRV field in the table)
- Menstrual cycle tracking for female athletes
- Psychological readiness/motivation scale
- Life stress (work, school, relationships) which affects recovery massively

Without input data, the readiness scores are either:
1. Manually entered by coach (burden + subjective)
2. Defaulted (useless)
3. Derived from ACWR only (circular reasoning)

### What a Real Recovery Model Needs

| Factor | In Forge? | Typical Real Implementation |
|--------|-----------|---------------------------|
| Session RPE load | ✓ (partially) | Wellness-integrated: session + daily wellness + sleep |
| ACWR | ✓ | EWMA-ACWR, individualised bandwidths |
| Sleep | ✗ | Wearable or self-report (hours, quality, latency) |
| HRV | ✗ | Morning orthostatic, Kubios/HRV4Training |
| Subjective wellness | ✗ | Hooper questionnaire / custom 5-question survey |
| Soreness/CK | ✗ | DOMS scale / creatine kinase blood test |
| Life stress | ✗ | Daily stress score (1-10) |
| Illness | ✗ | Daily illness log, immune function screen |
| Travel load | ✗ | Jet lag score, travel hours, time zone change |
| Competition load | ✗ | Game minutes, high-intensity efforts count |
| Menstrual cycle | ✗ | Phase tracking, symptom logging |
| Nutrition/Hydration | ✗ | Energy availability, hydration status |

### Recovery Model Score: **22/100**

Reasons:
- +10 for having ACWR infrastructure (better than nothing)
- +5 for athlete_state_snapshots concept
- +5 for actual_sets/reps/intensity/RPE columns (enables load tracking from reality, not prescription)
- -20 for ACWR being the sole load metric
- -15 for no subjective wellness integration
- -15 for no sleep tracking
- -10 for no HRV/physiological readiness
- -8 for no travel/competition load
- -5 for readiness scores have no input data
- -3 for ACWR scientific controversy not addressed
- -3 for no menstrual cycle tracking
- -2 for no life stress consideration

---

## Section 8 — Coach Override Review

### Question: How often would a competent S&C coach override the generated program?

The honest answer — and this is not a technology problem but a methodology problem:

| Context | Override Rate | Reasoning |
|---------|--------------|-----------|
| **Elite professional sport** | 80-90% | Too many unmodeled variables: fatigue, psychology, competition schedule, coach intuition, minor nags |
| **Collegiate/NCAA** | 60-70% | Athlete availability varies (classes, exams), injury history complex, team practice load fluctuates |
| **Youth/adolescent** | 50-60% | Maturation timing, sport sampling, psychosocial factors, enjoyment/adherence > optimal programming |
| **General population/fitness** | 30-40% | Adherence is the primary variable — "optimal" program is worthless if athlete won't do it |

### Most Common Override Reasons (Ranked by Frequency)

| Rank | Reason | Why Forge Can't Handle It |
|------|--------|--------------------------|
| 1 | **Athlete reports feeling off/fatigued** | No subjective wellness integration, no daily readiness adjustment |
| 2 | **Minor injury/nag (not in history)** | No real-time injury flagging, no exercise contraindication mapping |
| 3 | **Competition schedule change** | No dynamic calendar, no auto-adjustment for game moved/changed |
| 4 | **Coach's preferred methodology** | Deeper than any rule engine — coaching philosophy, mentorship lineage |
| 5 | **Equipment unavailable** | No equipment context per session — a program built for Week 1 assumes ideal gear |
| 6 | **Exercise causes pain/discomfort** | No per-athlete exercise tolerance tracking |
| 7 | **Athlete needs more/less rest between exercises** | No inter-set rest manipulation per athlete |
| 8 | **Athlete responds better to different exercises** | No individual response/predilection learning |
| 9 | **Phase-specific peaking requires load reduction** | No competition calendar, no taper protocol |
| 10 | **Session timing (AM vs PM)** | No chronotype or session timing consideration |

### The Real Problem

A competent S&C coach makes 20-30 micro-adjustments per session. These are not all captured by "override" — they are:

1. **Warm-up adjustments**: "He looks tight today, add 5 minutes of hip mobility before squatting"
2. **Exercise substitutions**: "She doesn't like high-bar today, switch to low-bar"
3. **Load adjustments**: "RPE looked 9 on that last set, drop 10% on the next one"
4. **Session reordering**: "We have a game tomorrow, make today an activation session instead of heavy legs"
5. **Environment adjustments**: "The gym's packed, let's do the opposite order to avoid the rack wait"

None of these are "overrides" in the system's sense. They are **real-time adaptive coaching decisions** that cannot be encoded as rules because they depend on contextual awareness the system lacks.

### Coach Acceptance Score: **22/100**

Reasons:
- +10 for having a coach_feedback table (recognises override is needed)
- +5 for recording override_reason and rationale
- +5 for session-level structure (program_sessions enable some ordering)
- -35 for daily micro-decisions completely unsupported
- -15 for no subjective wellness/readiness adjustment
- -10 for no real-time load modification
- -8 for no exercise discomfort tracking
- -5 for no session environment awareness
- -5 for elite-level coaches would reject 80%+ of generated sessions

---

## Section 9 — Real-World Case Testing

### Case 1: Elite Fast Bowler (International Level)

**Profile:** Male, 25, Professional Cricket Team, 8 years professional, off-season

**Needs:**
1. Maintain 90mph+ bowling speed
2. Reduce injury risk (previous stress fracture in lower back)
3. Improve repeat-bout capacity (overs 20-25 of spell)
4. Front foot brace force maintenance
5. Run-up speed and consistency

**Would Forge generate acceptable programming?**

- Pre-season general preparation phase: MAYBE
- The V2 demand priorities (Vertical Power 100, Horizontal Drive Power 95, Hinge Strength 90) are roughly correct for a fast bowler
- But: Forge would detect his "deficits" from assessments — every elite athlete has them. An 85% IMTP score (still elite) would be flagged as a deficit. Forge would increase emphasis on absolute strength, taking volume away from power/speed work. This is WRONG for an elite fast bowler — maintain strength, emphasise power and speed.
- Stress fracture history is not in the model. The program would load squats/deadlifts heavily without considering spinal loading context.
- No bowling workload management. Forge doesn't know he bowls 120 balls/week in team training.

**Would a coach change the program?** EVERYTHING. The coach would:
- Reduce squat volume (spinal loading concern)
- Add reactive plyometrics (SSC emphasis over absolute force)
- Include medicine ball work for trunk rotational velocity
- Manage bowling workload alongside gym sessions
- Periodise across a longer horizon (12-week block, not 4-week)

**Verdict: FAIL**

---

### Case 2: Developing Spinner (U19 Academy)

**Profile:** Male, 17, Cricket Academy, 2 years structured training, pre-season

**Needs:**
1. General athletic development (still growing)
2. Rotational power and trunk control
3. Lower body strength foundation
4. Injury prevention (shoulders, hips)
5. Enjoy training / stay motivated

**Would Forge generate acceptable programming?**

- Partial yes — Forge works best for developing athletes
- The spinner demands (Rotational Explosive Power 100, Rotational Core Control 95) are correct
- BUT: The model would prescribe exercises based on demand matching. A 17-year-old spinner would get "Medicine Ball Rotational Chest Pass" and "Cable Pallof Press." These are fine exercises but not sufficient for a developing athlete.
- The model misses: general athletic development (playful movement, variety), shoulder prehabilitation (high injury rate in young spinners), core stability in multiple planes
- The 4-week block is too short for a developing athlete. Real progression happens over 12-16 week blocks with broader focus.
- Maturation is not considered. A 17-year-old may be pre-PHV or post-PHV. Training should differ.

**Would a coach change the program?** YES, for the reasons above. The program is not WRONG but is INSUFFICIENT. A coach would add 50% more exercises (general athletic development, shoulder prehab, multi-planar core) that the model's 4-slot templates cannot accommodate.

**Verdict: MARGINAL FAIL — not wrong, but incomplete**

---

### Case 3: Professional Batter (International)

**Profile:** Male, 28, Professional Cricket Team, 10 years professional, in-season

**Needs:**
1. Maintain bat speed and power
2. Quick feet and acceleration between wickets
3. Manage back and hip niggles during season
4. Low-volume, high-intensity maintenance work
5. Batter-specific rotational power

**Would Forge generate acceptable programming?**

- FAILS — Forge has no in-season mode
- The model would detect "deficits" from periodic testing and increase work where it should maintain or reduce
- In-season, a batter cannot do 3×/week rotational power work. They play 50-over matches, field for 8 hours, bat for 2. Their body is already loaded from cricket.
- Forge would generate a 4-session/week program. A batter in-season does 2 S&C sessions max, and those are maintenance/activation.
- The model prescribes Trap Bar Deadlift sets of 3-5 — but in-season, a batter needs minimal eccentric load, focus on ballistic intent with low absolute load.

**Would a coach change the program?** COMPLETELY. The coach would:
- Reduce to 2 sessions/week
- Cut volume by 40%
- Replace heavy compounds with lighter, faster alternatives
- Add prehab/rehab work for the niggles
- Integrate with match schedule (no heavy session within 48 hours of a match)

**Verdict: FAIL**

---

### Case 4: Rugby Player (Professional)

**Profile:** Male, 24, Professional Rugby Union, back-row forward, off-season

**Needs:**
1. Absolute strength and power (contact dominance)
2. Acceleration over 5-15m (breakdown speed)
3. High-speed running capacity (chasing, covering)
4. Robustness (neck, shoulders, hamstrings)
5. Position-specific power (ruck, maul, tackle)

**Would Forge generate acceptable programming?**

- Partial — Forge's strength/power/acceleration framework fits rugby generally
- BUT: The current seed data has ZERO rugby-specific content. No rugby performance drivers. No rugby assessment benchmarks. No rugby templates (Shoulder Robustness has "Rugby All" as its sport but has generic rugby-unrelated content).
- Rugby needs: neck strengthening, impact preparation, 5m sprint specific work, tackling technique (not just gym), high-speed running conditioning (not just 10-30m sprints)
- The 4-week block is too short. Rugby off-season needs 12-16 weeks with: general prep (4 weeks), strength emphasis (4 weeks), power/contact prep (4 weeks), pre-season camp integration (4 weeks).
- Forge has no concept of collision load management — the biggest factor in rugby periodisation.

**Would a coach change the program?** FUNDAMENTALLY. The current seed data provides no rugby-specific anything. Even if populated, the model:
- Cannot account for collision load (tackles, rucks, mauls)
- Cannot integrate with team training (2-3 contact sessions/week)
- Cannot periodise impact exposure, which is THE critical variable in rugby
- Has no neck/head injury prevention framework

**Verdict: FAIL**

---

### Case 5: Soccer Midfielder (Professional)

**Profile:** Female, 23, Professional Women's Football, in-season

**Needs:**
1. High aerobic capacity (12km/match)
2. Repeat sprint ability (20-30 high-intensity efforts/match)
3. Lower body power (jumping, shooting)
4. Hamstring injury prevention (2 previous strains)
5. Menstrual cycle integration (affects performance and injury risk)

**Would Forge generate acceptable programming?**

- FAILS — Multiple critical gaps:
  1. **No aerobic capacity** — Forge has zero concept of endurance. A midfielder's primary physical quality (aerobic power) is completely unmodelled.
  2. **No repeat sprint ability** — Forge models acceleration and speed as single maximal efforts, not repeated bouts with incomplete recovery.
  3. **No hamstring strain history** — The model has no injury-specific logic. Previous hamstring strains would drastically alter exercise selection (Nordic curls, eccentrics at certain loads).
  4. **No menstrual cycle tracking** — Affects ACL risk, recovery capacity, training response. Unmodelled.
  5. **No integration with team training** — Match load + training load = total load. Forge only sees the S&C sessions.
  6. **In-season maintenance** — The model would try to "fix deficits" instead of maintaining the qualities that make her elite.

**Would a coach change the program?** COMPLETELY REPLACED. The S&C program for a female soccer midfielder in-season is:
- 2 S&C sessions: 1 maintenance strength, 1 power/prehab
- Hamstring eccentric work (Nordics, RDLs) every session
- Neuromuscular control exercises (ACL prevention)
- Load managed around menstrual cycle phase
- Primarily focused on injury prevention, not performance enhancement
- Team training (6-8 sessions/week) provides the primary conditioning stimulus

**Verdict: FAIL**

---

### Case 6: Olympic Sprinter (100m/200m)

**Profile:** Male, 22, Olympic Programme, 6 years sprint training, 3 months to major championship

**Needs:**
1. Highly specific track work (starts, drive phase, max velocity, speed endurance)
2. Gym work as SUPPLEMENT to track, not primary stimulus
3. Hamstring and groin injury prevention
4. Peaking for competition
5. Micro-loading (0.1s improvements in sprint time are massive)

**Would Forge generate acceptable programming?**

- FAILS — The model fundamentally misunderstands sprint training:
  1. Forge puts gym work as the primary programming driver. For a 100m sprinter, gym is supplementary (2 sessions/week max). Track is 5-6 sessions/week. The model should generate the TRACK program, not the gym program.
  2. "Acceleration" and "Speed" are treated as generic qualities with generic exercises (Clean Pull, Sprint Drills). Elite sprinters need highly specific track-based acceleration and speed work.
  3. The model has no concept of peaking. Three months out, the sprinter is in specific preparation, not general prep. The program must transition through specific blocks (start strength → max velocity → speed endurance → taper).
  4. No understanding of the force-velocity profile. Sprinters need to know whether their limitation is force production (horizontal) or velocity ceiling — this requires specific testing (sprint force-velocity profiling) that Forge doesn't include.
  5. No track-gym integration. Gym session content and load MUST be coordinated with track session content. Heavy squat day = no high-intensity starts that night.

**Would a coach change the program?** The entire model is inappropriate for sprint training. It's like using a distance-running training approach to programme a powerlifter. The design philosophy (deficit-driven, gym-primary, demand-exercise-template) does not match how sprint athletes are actually trained.

**Verdict: FAIL (model is inappropriate for this athlete type)**

---

### Case 7: Youth Athlete (14-year-old Multi-Sport)

**Profile:** Male, 14, plays Football, Basketball, and Athletics (jumps), PE 5×/week

**Needs:**
1. General athletic development (strength, coordination, speed)
2. Injury prevention (growth-related: Osgood-Schlatter, Sever's)
3. Skill development across multiple sports
4. FUN — adherence matters more than optimisation
5. Manageable workload alongside school

**Would Forge generate acceptable programming?**

- FAILS — Multiple fundamental issues:
  1. **Too structured** — A 14-year-old multi-sport athlete does not need 18 V2 performance demands. They need general physical preparation: learn to squat, learn to lunge, learn to jump, learn to land, learn to throw.
  2. **Development level misapplied** — The model maps training_age_months → development level. A 14-year-old with 24 months training gets "PERFORMANCE" level. This is wrong — development level should be based on biological maturation (PHV), not calendar training age.
  3. **No multi-sport load management** — He plays football 2×/week, basketball 2×/week, athletics 2×/week, PE 5×/week. Total training load is already 11+ sessions. Forge would add 2-4 more S&C sessions. This is overtraining.
  4. **No enjoyment/adherence factor** — The model prescribes optimal exercises. The real priority for a 14-year-old is: "Does he want to come back next week?" Enjoyment trumps optimisation at this stage.
  5. **Injury prevention for growth-related conditions** — No concept of Osgood-Schlatter management (avoid deep knee flexion under load during growth spurts), Sever's management (reduce impact loading when calcaneal apophysitis flares).

**Would a coach change the program?** COMPLETELY. The program for a 14-year-old should be:
- Bodyweight and dumbbell work (no heavy barbells)
- Unstructured but guided play (games, relays, obstacle courses)
- Landing mechanics drills (ACL prevention, even at this age)
- General athletic skills (sprint technique, jump technique, throw technique)
- Volume managed around growth: high knees on growth plates = reduce volume
- Ask about school, friends, other sports every session

**Verdict: FAIL**

---

### Case 8: Athlete Returning From ACL Reconstruction

**Profile:** Female, 20, Collegiate Soccer Player, 6 months post-op ACLR (hamstring autograft)

**Needs:**
1. Progressive return to running and jumping
2. Hamstring strength restoration (graft site)
3. Quadriceps strength restoration (post-op atrophy)
4. Landing mechanics retraining
5. Psychological readiness to return to sport
6. Phase-appropriate progression (cannot "max strength" in Phase 1)

**Would Forge generate acceptable programming?**

- FAILS — Dangerously so:
  1. **No return-to-play phasing** — ACLR return is 9-12 months divided into 5-6 distinct phases: (1) protection, (2) range of motion, (3) basic strength, (4) running, (5) jumping/landing, (6) sport-specific. Forge has NO phase concept.
  2. **Assessment deficits are misleading** — At 6 months post-op, she WILL have massive deficits: 40% quad deficit, 30% hamstring deficit, 50% limb symmetry index. The model would flag ALL of these and try to fix them simultaneously with 4 sessions/week of max strength work. This ignores the graft healing timeline and neural re-adaptation schedule.
  3. **Exercise selection is dangerous** — The model would recommend Barbell Back Squat (V2: Squat Strength priority). At 6 months post-op, she should not be back squatting heavy. She should be doing isometrics, then bodyweight squats, then goblet squats, then split squats, THEN back squat. The model has no progression pathway that respects graft healing.
  4. **No hamstring graft protection** — If the graft is hamstring, she cannot do Nordic curls or heavy RDLs until 9+ months. The model would happily prescribe these because they match "Hinge Strength" demand.
  5. **Psychological readiness unmodelled** — Many ACLR athletes are mentally ready for sport before their graft is biologically ready, or vice versa. The model has no mechanism to slow down or speed up progression based on psychological readiness.

**Would a coach change the program?** The generated program would be ACTIVELY HARMFUL. An ACLR athlete needs meticulous phase-based progression with:
- Phase-dependent strength targets
- Movement quality gates before load increase (e.g., "single-leg squat to 90° with no valgus collapse before adding load")
- Graft-specific loading restrictions
- Progressive sport reintegration

The model's "deficit → train more" philosophy — applied to an ACLR athlete with large deficits across everything — would create an unsafe program.

**Verdict: FAIL (DANGEROUS)**

---

## Section 10 — Final Verdict

### Score Summary

| Dimension | Score | Grade |
|-----------|-------|-------|
| 1. Demand Model | **42/100** | Weak |
| 2. Deficit Programming | **31/100** | Poor |
| 3. Assessment Coverage | **39/100** | Poor |
| 4. Exercise Selection | **28/100** | Poor |
| 5. Progression Model | **25/100** | Poor |
| 6. Periodization Readiness | **18/100** | Critical |
| 7. Recovery Model | **22/100** | Poor |
| 8. Coach Acceptance | **22/100** | Poor |
| **Composite** | **28/100** | **Poor** |

### The Verdict Question

> *"If all technical issues from Audits #1-10 were fixed tomorrow, would the underlying coaching methodology be strong enough to support production deployment?"*

**Answer: NO.** Absolutely not.

Fixing all technical issues (database, code, APIs, architecture) would fix zero of the sports science and coaching methodology problems identified in this audit. The methodology has fundamental gaps that cannot be addressed by better code or cleaner data. These are domain knowledge gaps, not implementation gaps.

The system would generate programs that are:
- **Wrong for elite athletes** (no in-season maintenance, no peaking, deficit-driven when they need strength-focused work)
- **Wrong for returning athletes** (no phase progression, dangerous exercise selection)
- **Wrong for youth athletes** (too structured, no maturation awareness)
- **Wrong for female athletes** (no menstrual cycle, different injury profiles)
- **Wrong for endurance/power/combat sports** (sport model doesn't fit)
- **Wrong for team sport athletes in-season** (no team training integration)
- **Wrong for most real-world coaching contexts** (no equipment variation, no daily readiness adjustment)

### Top 10 Sports Science Risks

| Rank | Risk | Severity |
|------|------|----------|
| 1 | **In-season deficit chasing increases injury risk** — Focusing on deficits when athlete needs maintenance overloads already-taxed systems | Critical |
| 2 | **ACL/RTP athletes given dangerous programs** — No phase progression, no graft-specific restrictions, deficit-driven approach ignores healing timelines | Critical |
| 3 | **Elite athlete performance degradation** — Fixing "deficits" in elite athletes moves training emphasis away from the qualities that make them elite | High |
| 4 | **Overtraining in youth athletes** — No awareness of maturation, no multi-sport load management, excessive structured sessions | High |
| 5 | **Female athlete-specific risks unaddressed** — No ACL prevention programming, no menstrual cycle integration, no RED-S monitoring | High |
| 6 | **Hamstring injury prevention absent** — No eccentric strength assessment, no Nordic curl programming, no hamstring:quad ratio tracking | High |
| 7 | **Aerobic under-development in team sport athletes** — No aerobic capacity concept means team sport athletes get power-only programs | High |
| 8 | **ACWR false confidence** — Relying on a contested metric to guide load decisions while ignoring sleep, stress, illness, and readiness | Moderate |
| 9 | **No collision load management for contact sports** — Rugby, American Football athletes have unmodelled impact exposure driving their training needs | High |
| 10 | **Transfer index oversimplification** — A single number cannot model exercise transfer; leads to poor exercise selection for sport-specific phases | Moderate |

### Top 10 Coaching Risks

| Rank | Risk | Severity |
|------|------|----------|
| 1 | **Coach trust erosion** — If generated programs are obviously wrong, coaches stop using the system entirely | Critical |
| 2 | **Athlete buy-in loss** — Athletes receiving generic, inappropriate programs lose faith | Critical |
| 3 | **Override fatigue** — If 80%+ of programs need changes, coaches will revert to manual programming | High |
| 4 | **No warm-up/cool-down generation** — Most injuries occur in warm-up and early session; no warm-up programming increases injury risk | High |
| 5 | **Exercise accommodation** — No exercise rotation leads to plateau and boredom | Moderate |
| 6 | **False precision** — V1 deficit thresholds with inadequate benchmark data create false positives/negatives; coaches learn to ignore deficit flags | High |
| 7 | **Development level = training age fallacy** — Mapping training months to development ignores biological maturation, skill level, and injury history | High |
| 8 | **Kitchen sink programming** — Trying to address 5+ demands in every block leads to excessive complexity and poor adherence | Moderate |
| 9 | **No deload/stall management** — Coaches must manually intervene whenever an athlete plateaus, which is every 4-6 weeks for advanced athletes | Moderate |
| 10 | **Session context blindness** — No awareness of what happened yesterday, what's happening tomorrow; programs are generated in a contextual vacuum | High |

### Top 10 Scientific Improvements

| Rank | Improvement | Evidence |
|------|------------|----------|
| 1 | **Replace linear periodisation with daily undulating periodisation (DUP)** | DUP produces superior strength and power gains compared to linear periodisation in trained athletes (Kraemer & Ratamess, 2004; Rhea et al., 2003; Painter et al., 2012) |
| 2 | **Add block periodisation framework** | Accumulation→Intensification→Realization blocks with 4-6 week durations produce superior long-term adaptation (Issurin, 2010) |
| 3 | **Replace ACWR with EWMA + subjective wellness composite** | EWMA-ACWR outperforms rolling average ACWR (Williams et al., 2020); combining with wellness is more predictive (Gabbett, 2020 critique response) |
| 4 | **Add eccentric hamstring assessment and programming** | Nordic hamstring exercise reduces hamstring injury by 50%+ (van Dyk et al., 2018; Petersen et al., 2011); missing from current battery |
| 5 | **Add aerobic/anaerobic capacity concepts** | Yo-yo intermittent recovery test predicts match performance in team sports (Krustrup et al., 2003; Bangsbo et al., 2008) |
| 6 | **Implement force-velocity profiling for power development** | Individualised FV profiling enables targeted power training (Samozino et al., 2008; Morin & Samozino, 2016) |
| 7 | **Add phase-appropriate periodisation logic** | Different training phases require different volume, intensity, and exercise selection (Bompa & Haff, 2009) |
| 8 | **Implement maturation-aware youth programming** | Train by biological age, not chronological age; different protocols for pre-PHV, circa-PHV, and post-PHV athletes (Lloyd & Oliver, 2012) |
| 9 | **Add menstrual cycle integration** | Cycle phase affects injury risk, recovery, and training response in female athletes (McNulty et al., 2020; De Souza et al., 2014) |
| 10 | **Add subjective wellness + autonomic nervous system readiness (HRV)** | Daily readiness assessment combining subjective and objective measures improves training prescription (Buchheit, 2014; Thorpe et al., 2017) |

---

## Final Statement

Forge's demand ontology is **biomechanically sophisticated** — arguably beyond what any commercial system has attempted. The V2 architecture with movement_pattern × physical_quality demands is genuinely novel and valuable.

But coaching is not applied biomechanics. It is:

- **Load management** — The art of applying the right stress at the right time, while managing total load from training, competition, and life
- **Injury prevention** — Understanding individual injury history, risk factors, and phase-appropriate precautions
- **Periodisation** — The macro-to-micro organisation of training across seasons, blocks, weeks, and sessions
- **Psychosocial management** — Motivation, confidence, group dynamics, coach-athlete relationship
- **Adherence engineering** — The best program is worthless if the athlete doesn't do it
- **Contextual intelligence** — Equipment available, time available, travel schedule, competition calendar, life stress, sleep quality

The system captures 0 of these 6 domains adequately.

Forge is **not yet a coaching tool**. It is a **biomechanical classification engine** that could become part of a coaching tool if integrated with real coaching intelligence. Its future is not as an autonomous program generator but as a decision-support layer that a human coach uses to:
- Check their bias ("Am I neglecting a quality?")
- Generate starting points ("What templates fit this athlete's profile?")
- Track changes over time (longitudinal deficit tracking)
- Model interactions ("If I emphasise power, what happens to strength maintenance?")

As an autonomous program generator that a coach presses "generate" and delivers to an athlete? That day is >3 years of sports science R&D away, even with perfect code.

**Score: 28/100 — Not ready. Return to R&D. Engage domain experts (S&C coaches working in elite sport) for at least 6 months of iterative methodology design before writing another line of code.**
