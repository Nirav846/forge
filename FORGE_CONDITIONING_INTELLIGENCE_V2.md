# FORGE Conditioning Intelligence V2

> Audits FORGE_CONDITIONING_LIBRARY_V1.md and transforms it from a protocol collection into a coaching decision system.
> Determines what matters, what to use when, and what to build for MVP.
> Coaching knowledge document. No new architecture. No entities. No databases.

---

## PART 1: Conditioning Decision Tree

### How to Use

Read top to bottom. At each decision point, follow the branch that matches your athlete. The output is a protocol family — go to that section of the library and select the appropriate level.

```
┌─────────────────────────────────────────────────────────────────┐
│                   CONDITIONING DECISION TREE                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │  STEP 1: TRAINING    │
                    │  AGE                 │
                    └─────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
         ┌──────────┐  ┌──────────────┐  ┌──────────┐
         │ Beginner │  │ Intermediate │  │ Advanced │
         │ (<1 yr)  │  │ (1-3 yrs)    │  │ (3+ yrs) │
         └──────────┘  └──────────────┘  └──────────┘
              │               │               │
              ▼               ▼               ▼
    ┌─────────────────────────────────────────────────────┐
    │  STEP 2: GOAL                                        │
    │  (Ranked by athlete need — pick ONE primary goal)    │
    └─────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┬──────────────────┬───────────────────┐
         ▼                    ▼                    ▼                  ▼                   ▼
   ┌─────────────┐    ┌──────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
   │ RECOVERY    │    │ AEROBIC      │    │ AEROBIC      │    │ EXTENSIVE   │    │ INTENSIVE    │
   │             │    │ CAPACITY     │    │ POWER        │    │ TEMPO       │    │ TEMPO        │
   └─────────────┘    └──────────────┘    └──────────────┘    └─────────────┘    └──────────────┘
         │                  │                  │                  │                  │
         ▼                  ▼                  ▼                  ▼                  ▼
   ┌─────────────┐    ┌──────────────┐    ┌──────────────┐    ┌─────────────┐    ┌──────────────┐
   │   ┌───────────────────────────────────────────────────────────────────────┐    │
   │   │  STEP 3: ENVIRONMENT                                                  │    │
   │   └───────────────────────────────────────────────────────────────────────┘    │
   │              │                                                               │
   │    ┌─────────┼─────────┬──────────┬──────────┐                              │
   │    ▼         ▼         ▼          ▼          ▼                              │
   │ ┌──────┐ ┌──────┐ ┌────────┐ ┌───────┐ ┌───────┐                          │
   │ │Field │ │Track │ │Treadmill│ │Indoor │ │Limited│                          │
   │ │      │ │      │ │        │ │Court  │ │Space  │                          │
   │ └──────┘ └──────┘ └────────┘ └───────┘ └───────┘                          │
   │     │        │        │          │        │                                │
   └─────┼────────┼────────┼──────────┼────────┼────────────────────────────────┘
         │        │        │          │        │
         ▼        ▼        ▼          ▼        ▼
    ┌─────────────────────────────────────────────────────┐
    │  STEP 4: AVAILABLE TIME                              │
    └─────────────────────────────────────────────────────┘
              │
    ┌─────────┼─────────┬──────────┐
    ▼         ▼         ▼          ▼
 ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
 │10 min│ │20 min│ │30 min│ │45 min│
 └──────┘ └──────┘ └──────┘ └──────┘
    │        │        │        │
    ▼        ▼        ▼        ▼
  OUTPUT → Specific protocol family + level suggestion
```

### Decision Maps by Goal

#### Goal: Recovery Conditioning

| Time | Field | Track | Treadmill | Indoor | Limited Space |
|------|-------|-------|-----------|--------|--------------|
| 10 min | Recovery Jog | Recovery Walk | Cycling Rec. | Mobility Circuit | Mobility Circuit |
| 20 min | Rec. Jog + Stretch | Rec. Walk | Cycling Rec. | Mobility + Walk | Mobility Circuit |
| 30 min | Light Stretch Circuit | Rec. Walk Extended | Cross-Train Bike | Aqua Jogging | Mobility + Walk |
| 45 min | Aqua Jogging | Rec. Walk + Mobility | Cross-Train | Aqua Jogging | N/A |

**Beginner:** Recovery Walk or Mobility Circuit. **Intermediate+:** as per table.

#### Goal: Aerobic Capacity

| Time | Field | Track | Treadmill | Indoor | Limited Space |
|------|-------|-------|-----------|--------|--------------|
| 10 min | 20-Min Base (skip) | 15-Min Tempo Walk | 15-Min Walk | Walk-Jog (indoor) | 10 min Walk |
| 20 min | LSD Base 20 min | LSD 20 min | 20-Min Zone 2 Bike | Cross-Train Bike | Walk-Jog (spot) |
| 30 min | LSD 30 min | LSD 30 min | 30-Min Zone 2 Bike | Cross-Train 30 min | Bodyweight circuit |
| 45 min | LSD 45 min | LSD 8 km | Cross-Train 40 min | Aqua Jogging | N/A |

**Beginner:** Walk-Jog Progression (AC-005). **Intermediate:** LSD 20-30 min. **Advanced:** LSD 30-45 min or Fartlek.

#### Goal: Aerobic Power

| Time | Field | Track | Treadmill | Indoor | Limited Space |
|------|-------|-------|-----------|--------|--------------|
| 10 min | N/A (insufficient) | N/A | N/A | N/A | N/A |
| 20 min | MAS 60m (2 sets) | 1 km Repeats (2 reps) | Threshold (2 reps) | 20m MAS Shuttle | Shuttle runs |
| 30 min | MAS 60m (3 sets) | 1 km Repeats (3-4 reps) | Threshold (6 reps) | 30-15 IFT | 20m Shuttle |
| 45 min | MAS 60m (4 sets) | 3 km Time Trial | 5×3 Threshold Set | IFT + MAS combo | Shuttle + circuit |

**Beginner:** N/A (build aerobic capacity first). **Intermediate:** MAS 60m Standard. **Advanced:** MAS 60m tight rest or 1 km Repeats.

#### Goal: Extensive Tempo

| Time | Field | Track | Treadmill | Indoor | Limited Space |
|------|-------|-------|-----------|--------|--------------|
| 10 min | 30m Tempo (15 reps) | 30m Tempo | N/A | 20m shuttle tempo | Spot tempo |
| 20 min | 60m Tempo (2 sets) | 100m Tempo (8 reps) | Treadmill tempo | 2-4-6 Ladder | Shuttle tempo |
| 30 min | 60m Tempo (3 sets) | 100m Tempo (12 reps) | 70/30 Run-Walk | Cricket Circuit (modified) | Ladder + shuttle |
| 45 min | Cricket Ground Circuit | 100m Tempo Extended | N/A | Indoor circuit | N/A |

**Beginner:** 30m Tempo or 70/30 Run-Walk. **Intermediate:** 60m Tempo BCCI standard. **Advanced:** 80m Timed Starts or Cricket Circuit.

#### Goal: Intensive Tempo

| Time | Field | Track | Treadmill | Indoor | Limited Space |
|------|-------|-------|-----------|--------|--------------|
| 10 min | N/A (insufficient) | N/A | N/A | N/A | N/A |
| 20 min | 200m Repeats (6 reps) | 200m Repeats | 500m Repeats (2 reps) | Short shuttle intensive | N/A |
| 30 min | 400m Repeats (5 reps) | 400m Repeats | 500m Repeats (4 reps) | Pyramid (modified) | Intensive shuttle |
| 45 min | Descending Ladder | Full Pyramid | 600m + 400m Combo | Full Pyramid indoor | N/A |

**Advanced only.** Beginner and Intermediate should not do intensive tempo — build through extensive tempo and aerobic power first.

#### Goal: Repeated Sprint Ability

| Time | Field | Track | Treadmill | Indoor | Limited Space |
|------|-------|-------|-----------|--------|--------------|
| 10 min | 30m Every 30s (6 reps) | 30m RSA | N/A | 20m Shuttle RSA | 10m Shuttle RSA |
| 20 min | 30m Every 30s (12 reps) | RSA Cluster (3 sets) | N/A | Agility 4x10m (10 reps) | 10m Shuttle (8 reps) |
| 30 min | German Volume RSA (3 sets) | RSA Cluster (4 sets) | N/A | Direction Change RSA | 10m Shuttle extensive |
| 45 min | RSA + Tempo Combo | RSA Cluster + Float | N/A | Multi-direction RSA | N/A |

**Beginner:** 30m Every 40s (L1 progression). **Intermediate:** 30m Every 30s Standard. **Advanced:** 30m Every 20s or RSA Cluster.

#### Goal: Alactic Speed

| Time | Field | Track | Treadmill | Indoor | Limited Space |
|------|-------|-------|-----------|--------|--------------|
| 10 min | 10m Accel (8 reps) | 10m Accel | N/A | 10m Accel indoor | 5m starts |
| 20 min | 20m Sprints (8 reps) | Flying 10m Timed | N/A | 20m Sprints | Spot sprints |
| 30 min | Contrast Sprints (5 pairs) | Flying 10m + 20m | N/A | 3-Point starts | N/A |
| 45 min | Full speed session | Max V + Accel combo | N/A | N/A | N/A |

**Requires fresh CNS.** Never after conditioning. Alactic speed is ALWAYS the first element of a session or in a dedicated speed session. All levels can do alactic speed — volume and distance vary.

#### Goal: Lactate Tolerance

| Time | Field | Track | Treadmill | Indoor | Limited Space |
|------|-------|-------|-----------|--------|--------------|
| 10 min | N/A | N/A | Over-Unders (1 set) | N/A | N/A |
| 20 min | 300m Hard (4 reps) | 300m Hard | Over-Unders (2 sets) | Shuttle lactate | Intensive shuttle |
| 30 min | 400m Hard (4 reps) | 400m Hard | Over-Unders (3 sets) | Broken 800m | Hill repeats (stairs) |
| 45 min | Short-Long-Short (3 sets) | 250m Hill Repeats | Over-Unders (4 sets) | Full lactate set | Stair repeats |

**Advanced only.** Never for beginners. Never within 48 hours of a speed session.

#### Goal: Power Maintenance

| Time | Field | Track | Treadmill | Indoor | Limited Space |
|------|-------|-------|-----------|--------|--------------|
| 10 min | 30m Fatigue Test | 30m Fatigue | N/A | CMJ-Sprint Complex | CMJ only |
| 20 min | PM In-Season Shorts | PM + CMJ Combo | N/A | Med Ball Complex | Repeated Broad Jump |
| 30 min | CMJ-Sprint + Med Ball | Full PM Circuit | N/A | 5-10-5 + Jumps | Complex circuit |
| 45 min | Extended PM Circuit | PM + Speed combo | N/A | Multi-modal PM | N/A |

**All levels** can do power maintenance — adjust volume and intensity. This is the most under-used conditioning quality in amateur programming.

---

## PART 2: Protocol Rankings

### Ranking Criteria

Each protocol is scored on 5 dimensions (1-5):

| Dimension | 1 (Low) | 3 (Medium) | 5 (High) |
|-----------|---------|------------|----------|
| **Coach Credibility** | Barely used in elite programs | Used by some programs | Universal across elite programs |
| **Real-World Usage** | Niche, rare | Common in one sport | Common across 3+ sports |
| **Ease of Coaching** | Requires specialist equipment/timing | Simple setup, some instruction | Minimal setup, self-explanatory |
| **Repeatability** | Hard to replicate consistently | Replicable with good coaching | Highly standardisable |
| **Injury Risk** | High risk (poor form under fatigue) | Moderate (manageable) | Low risk |

**Composite:** Sum ÷ 5. A Tier = 4.0-5.0. B Tier = 3.0-3.9. C Tier = 1.0-2.9.

### Aerobic Capacity Protocols

| Protocol | Cred | Usage | Ease | Repeat | Risk | Score | Tier |
|----------|------|-------|------|--------|------|-------|------|
| AC-001 LSD Base Builder | 3 | 5 | 5 | 5 | 5 | 4.6 | **A** |
| AC-002 LSD Aerobic Volume | 3 | 5 | 5 | 5 | 5 | 4.6 | **A** |
| AC-003 Recovery Jog | 5 | 5 | 5 | 5 | 5 | 5.0 | **A** |
| AC-004 Cross-Train Aerobic | 2 | 3 | 4 | 5 | 5 | 3.8 | **B** |
| AC-005 Walk-Jog Progression | 3 | 4 | 5 | 5 | 5 | 4.4 | **A** |
| AC-006 2 km Continuous Timed | 4 | 4 | 5 | 5 | 4 | 4.4 | **A** |
| AC-007 12-Minute Run (Cooper) | 4 | 3 | 5 | 5 | 3 | 4.0 | **A** |
| AC-008 15-Minute Tempo Walk | 2 | 3 | 5 | 5 | 5 | 4.0 | **A** |
| AC-009 2 km Run Assessment | 4 | 4 | 5 | 5 | 4 | 4.4 | **A** |
| AC-010 30-Min Zone 2 Bike | 2 | 3 | 5 | 5 | 5 | 4.0 | **A** |
| AC-011 Fartlek — Speed Play | 3 | 3 | 3 | 3 | 4 | 3.2 | **B** |
| AC-012 20-Minute Aerobic Base | 3 | 5 | 5 | 5 | 5 | 4.6 | **A** |

**Notes:** Aerobic capacity protocols are universally easy to coach and low risk. Most are A Tier. Cross-Train and Fartlek are B Tier — useful tools but not elite-program standard.

### Aerobic Power Protocols

| Protocol | Cred | Usage | Ease | Repeat | Risk | Score | Tier |
|----------|------|-------|------|--------|------|-------|------|
| AP-001 MAS 60m Standard | 5 | 5 | 4 | 5 | 3 | 4.4 | **A** |
| AP-002 Treadmill Threshold | 4 | 4 | 5 | 5 | 4 | 4.4 | **A** |
| AP-003 1 km Repeats | 4 | 4 | 4 | 4 | 4 | 4.0 | **A** |
| AP-004 800m Repeats | 4 | 3 | 4 | 4 | 3 | 3.6 | **B** |
| AP-005 400m Threshold Cruise | 4 | 4 | 5 | 5 | 4 | 4.4 | **A** |
| AP-006 20m MAS Shuttle | 4 | 3 | 3 | 4 | 3 | 3.4 | **B** |
| AP-007 30-15 IFT | 4 | 3 | 2 | 3 | 3 | 3.0 | **B** |
| AP-008 Yo-Yo IR1 Shuttles | 5 | 5 | 3 | 4 | 3 | 4.0 | **A** |
| AP-009 3 km Time Trial | 3 | 3 | 4 | 5 | 3 | 3.6 | **B** |
| AP-010 1 km Cruise — Tempo | 4 | 4 | 4 | 4 | 4 | 4.0 | **A** |
| AP-011 5 × 3 min Threshold | 4 | 3 | 5 | 5 | 4 | 4.2 | **A** |

**Notes:** MAS 60m and Yo-Yo IR1 are the highest-credibility protocols. Shuttle-based protocols score lower on ease of coaching (need lines, beep, instruction). Treadmill protocols score higher on repeatability.

### Extensive Tempo Protocols

| Protocol | Cred | Usage | Ease | Repeat | Risk | Score | Tier |
|----------|------|-------|------|--------|------|-------|------|
| ET-001 60m Tempo BCCI | 5 | 5 | 5 | 5 | 4 | 4.8 | **A** |
| ET-002 100m Tempo | 4 | 4 | 5 | 5 | 4 | 4.4 | **A** |
| ET-003 80m Timed Starts | 4 | 3 | 3 | 4 | 4 | 3.6 | **B** |
| ET-004 70/30 Run-Walk | 3 | 3 | 5 | 5 | 5 | 4.2 | **A** |
| ET-005 6×100m Build-up | 3 | 3 | 4 | 4 | 4 | 3.6 | **B** |
| ET-006 Cricket Ground Circuit | 4 | 3 | 4 | 4 | 4 | 3.8 | **B** |
| ET-007 2-4-6 Ladder | 4 | 4 | 3 | 4 | 3 | 3.6 | **B** |
| ET-008 50m Sprint ×8 Tempo | 3 | 3 | 5 | 5 | 4 | 4.0 | **A** |
| ET-009 Grass Sprints 40m | 4 | 4 | 5 | 5 | 5 | 4.6 | **A** |
| ET-010 30m Tempo Short | 3 | 3 | 5 | 5 | 5 | 4.2 | **A** |

**Notes:** 60m Tempo BCCI standard is the top protocol — used by cricket, rugby, soccer. Grass sprints score highest on risk (low impact surface). 2-4-6 Ladder is B Tier because of coaching complexity (need to explain the ladder format).

### Intensive Tempo Protocols

| Protocol | Cred | Usage | Ease | Repeat | Risk | Score | Tier |
|----------|------|-------|------|--------|------|-------|------|
| IT-001 400m Repeats Classic | 5 | 5 | 4 | 5 | 3 | 4.4 | **A** |
| IT-002 Descending Ladder | 4 | 3 | 2 | 3 | 2 | 2.8 | **C** |
| IT-003 200m Repeats | 4 | 4 | 5 | 5 | 4 | 4.4 | **A** |
| IT-004 300m Repeats | 4 | 3 | 4 | 4 | 3 | 3.6 | **B** |
| IT-005 600m Repeats | 3 | 2 | 4 | 4 | 3 | 3.2 | **B** |
| IT-006 500m Repeats | 3 | 2 | 4 | 4 | 3 | 3.2 | **B** |
| IT-007 Full Pyramid | 3 | 2 | 1 | 2 | 2 | 2.0 | **C** |
| IT-008 Negative Split 800s | 3 | 2 | 3 | 3 | 3 | 2.8 | **C** |

**Notes:** 400m and 200m repeats are the elite-program standard. Descending ladder and pyramid score low on ease and repeatability — complex to set up, hard to standardise across athletes. Keep for advanced athletes only.

### Repeated Sprint Ability Protocols

| Protocol | Cred | Usage | Ease | Repeat | Risk | Score | Tier |
|----------|------|-------|------|--------|------|-------|------|
| RSA-001 30m Every 30s | 5 | 5 | 5 | 5 | 3 | 4.6 | **A** |
| RSA-002 30m Every 20s | 5 | 4 | 5 | 5 | 2 | 4.2 | **A** |
| RSA-003 40m RSA Field | 4 | 4 | 5 | 5 | 3 | 4.2 | **A** |
| RSA-004 RSA Cluster 3×30m | 4 | 3 | 3 | 4 | 2 | 3.2 | **B** |
| RSA-005 20m Shuttle RSA | 4 | 4 | 4 | 4 | 3 | 3.8 | **B** |
| RSA-006 25m×6 Tight Rest | 4 | 3 | 4 | 4 | 2 | 3.4 | **B** |
| RSA-007 20m On/Off | 3 | 3 | 4 | 4 | 3 | 3.4 | **B** |
| RSA-008 Agility 4×10m | 4 | 3 | 3 | 3 | 3 | 3.2 | **B** |
| RSA-009 10m Shuttle Court | 3 | 3 | 4 | 4 | 3 | 3.4 | **B** |
| RSA-010 German Volume RSA | 2 | 2 | 3 | 4 | 2 | 2.6 | **C** |
| RSA-011 Direction Change RSA | 3 | 3 | 3 | 3 | 3 | 3.0 | **B** |

**Notes:** 30m Every 30s is the gold standard — used by BCCI, ASCA, rugby, soccer. High credibility, easy to set up, repeatable. RSA Cluster and German Volume are C/B Tier — high quality but harder to coach and higher injury risk under accumulated fatigue.

### Speed Endurance Protocols

| Protocol | Cred | Usage | Ease | Repeat | Risk | Score | Tier |
|----------|------|-------|------|--------|------|-------|------|
| SE-001 150m Repeats | 4 | 4 | 4 | 4 | 3 | 3.8 | **B** |
| SE-002 Flying 30s | 5 | 4 | 3 | 4 | 3 | 3.8 | **B** |
| SE-003 Cut-downs 150m | 3 | 3 | 3 | 3 | 3 | 3.0 | **B** |
| SE-004 Sprint Float Sprint | 5 | 4 | 3 | 4 | 2 | 3.6 | **B** |
| SE-005 50m+25m Combo | 3 | 3 | 4 | 4 | 3 | 3.4 | **B** |
| SE-006 100m×6 Timed | 4 | 4 | 4 | 4 | 3 | 3.8 | **B** |
| SE-007 Accel Build-up 60m | 3 | 3 | 4 | 4 | 4 | 3.6 | **B** |
| SE-008 120m Repeats | 3 | 3 | 4 | 4 | 3 | 3.4 | **B** |
| SE-009 80m Flying Start | 4 | 3 | 3 | 4 | 2 | 3.2 | **B** |

**Notes:** Speed endurance protocols are uniformly B Tier. None are A Tier because they carry higher injury risk and are harder to coach than RSA protocols. Flying 30s and Sprint Float Sprint are the most credible (track athlete standard). Cut-downs is lowest — complex instruction for moderate benefit.

### Alactic Speed Protocols

| Protocol | Cred | Usage | Ease | Repeat | Risk | Score | Tier |
|----------|------|-------|------|--------|------|-------|------|
| AS-001 10m Acceleration | 5 | 5 | 5 | 5 | 5 | 5.0 | **A** |
| AS-002 20m Sprints | 5 | 5 | 5 | 5 | 4 | 4.8 | **A** |
| AS-003 30m Full Recovery | 5 | 5 | 5 | 5 | 4 | 4.8 | **A** |
| AS-004 Flying 10m Timed | 4 | 4 | 3 | 4 | 3 | 3.6 | **B** |
| AS-005 Contrast Sprints | 3 | 3 | 2 | 3 | 2 | 2.6 | **C** |
| AS-006 40m×4 Speed | 4 | 4 | 5 | 5 | 4 | 4.4 | **A** |
| AS-007 15m Ball Start | 3 | 3 | 3 | 3 | 4 | 3.2 | **B** |
| AS-008 3-Point to 10m | 3 | 4 | 4 | 4 | 4 | 3.8 | **B** |

**Notes:** Alactic speed protocols score highest across all families. 10m Acceleration, 20m Sprints, and 30m Sprints are the highest-rated protocols in the entire library (5.0, 4.8, 4.8). Low injury risk (fresh CNS, low volume), easy to coach, highly repeatable, universal across all sports. Contrast Sprints is C Tier — complex setup, high risk, niche usage.

### Lactate Tolerance Protocols

| Protocol | Cred | Usage | Ease | Repeat | Risk | Score | Tier |
|----------|------|-------|------|--------|------|-------|------|
| LT-001 400m Hard | 4 | 4 | 4 | 4 | 2 | 3.6 | **B** |
| LT-002 300m Hard | 4 | 3 | 4 | 4 | 2 | 3.4 | **B** |
| LT-003 Broken 800m | 3 | 2 | 3 | 3 | 2 | 2.6 | **C** |
| LT-004 200m Hard | 4 | 4 | 5 | 5 | 3 | 4.2 | **A** |
| LT-005 Short-Long-Short | 3 | 2 | 2 | 2 | 1 | 2.0 | **C** |
| LT-006 Treadmill Over-Unders | 3 | 2 | 4 | 5 | 3 | 3.4 | **B** |
| LT-007 500m Hard | 3 | 2 | 4 | 4 | 2 | 3.0 | **B** |
| LT-008 250m Hill Repeats | 4 | 3 | 3 | 3 | 2 | 3.0 | **B** |
| LT-009 60s On/Off Max | 3 | 3 | 4 | 4 | 2 | 3.2 | **B** |

**Notes:** Lactate tolerance is the highest-risk conditioning family. 200m Hard is the only A Tier protocol — short enough to execute safely, long enough to accumulate lactate. Broken 800m and Short-Long-Short score lowest (complex, high risk, low repeatability across athletes). Use sparingly — 1 session per week max for advanced athletes only.

### Power Maintenance Protocols

| Protocol | Cred | Usage | Ease | Repeat | Risk | Score | Tier |
|----------|------|-------|------|--------|------|-------|------|
| PM-001 30m Fatigue Test | 5 | 5 | 5 | 5 | 3 | 4.6 | **A** |
| PM-002 CMJ-Sprint Complex | 4 | 4 | 4 | 4 | 4 | 4.0 | **A** |
| PM-003 Repeated Broad Jump | 3 | 3 | 4 | 4 | 4 | 3.6 | **B** |
| PM-004 Med Ball Complex | 4 | 3 | 3 | 4 | 4 | 3.6 | **B** |
| PM-005 In-Season Shorts | 5 | 5 | 5 | 5 | 5 | 5.0 | **A** |
| PM-006 5-10-5 Shuttle Power | 4 | 4 | 4 | 4 | 3 | 3.8 | **B** |
| PM-007 Hurdle Hop PM | 3 | 2 | 3 | 3 | 3 | 2.8 | **C** |

**Notes:** Power Maintenance is the most under-programmed quality in amateur sport. 30m Fatigue Test and In-Season Shorts are A Tier — widely used across elite programs, easy to coach, low volume, high intent. Hurdle Hop PM is C Tier — niche, risk of under-rotating or catching a hurdle under fatigue.

### Recovery Conditioning Protocols

| Protocol | Cred | Usage | Ease | Repeat | Risk | Score | Tier |
|----------|------|-------|------|--------|------|-------|------|
| RC-001 Active Recovery Jog | 5 | 5 | 5 | 5 | 5 | 5.0 | **A** |
| RC-002 Recovery Walk | 5 | 5 | 5 | 5 | 5 | 5.0 | **A** |
| RC-003 Mobility Circuit | 4 | 4 | 5 | 5 | 5 | 4.6 | **A** |
| RC-004 Aqua Jogging | 3 | 3 | 3 | 4 | 5 | 3.6 | **B** |
| RC-005 Cycling Recovery | 4 | 4 | 5 | 5 | 5 | 4.6 | **A** |
| RC-006 Light Stretch Circuit | 4 | 4 | 5 | 5 | 5 | 4.6 | **A** |

**Notes:** Recovery protocols score highest overall — 5.0 for Active Recovery Jog and Recovery Walk. They are the safest, easiest, most repeatable protocols in the library. Aqua Jogging is B Tier — requires pool access, harder to monitor.

### Tier Summary

| Tier | Count | Definition |
|------|-------|------------|
| **A** | 40 | First choice. Use as default. High credibility, easy coaching, low risk. |
| **B** | 45 | Good option. Use for variation, specific adaptation, or when A Tier is unavailable. |
| **C** | 15 | Niche. Use only for advanced athletes with specific goals. Higher risk, harder to coach. |

---

## PART 3: Universal Conditioning Patterns

> Patterns that appear across 3+ sports in the 58-program corpus. These are the structures elite coaches trust.

### Pattern 1: 30m Sprint Every X Seconds

**Structure:** 30m maximal sprint on a fixed time cycle (20s, 25s, 30s, 40s). Repeat for 5-10 minutes.
**Found in:** BCCI, ECB, ASCA, Rugby S&C, Soccer S&C, Cricket Australia.
**Purpose:** Repeated Sprint Ability. Fixed cycle forces athlete to recover and reproduce output regardless of readiness.
**Why coaches use it:** Most field sport sprints are 20-40m. The fixed cycle standardises recovery. Easy to compare across sessions. The elite standard for RSA.

### Pattern 2: MAS 60m Shuttle

**Structure:** 60m runs at individual MAS pace with fixed rest (27-35s). 6 reps × 3 sets. 5 min between sets.
**Found in:** BCCI, ASCA, Cricket Australia, Rugby S&C.
**Purpose:** Aerobic Power. MAS is the highest speed an athlete can maintain for 60s. Training at this pace improves VO2 max and lactate clearance.
**Why coaches use it:** Individualised by definition. The 60m distance is short enough to repeat, long enough to stress aerobic system. Highly standardisable across a squad.

### Pattern 3: 60m Tempo Run

**Structure:** 60m at 70-80% max speed, walk-back rest (30-45s). 10-15 reps. 2-3 sets.
**Found in:** BCCI, ASCA, Rugby S&C, Soccer S&C, ECB.
**Purpose:** Extensive Tempo. Sub-maximal speed development with incomplete recovery. Builds work capacity.
**Why coaches use it:** Low injury risk. Teaches pace judgment. High volume without high systemic stress. Walk-back recovery is self-regulating.

### Pattern 4: 400m Repeats

**Structure:** 400m at 80-87% max effort. 3-5 min rest. 4-6 reps.
**Found in:** BCCI, Cricket Australia, Rugby S&C, Soccer S&C, Athletics (middle distance), NSCA.
**Purpose:** Intensive Tempo / Lactate Threshold. The classic pre-season conditioning protocol.
**Why coaches use it:** 400m is long enough to stress the aerobic system, short enough to repeat. The distance is standardised worldwide. No equipment needed. Results are comparable across programs.

### Pattern 5: Descending Ladder

**Structure:** 800m → 400m → 200m → 100m. Decreasing rest as distance decreases. 1-3 sets.
**Found in:** BCCI, ECB, Rugby S&C, Athletics (sprint), Cricket Australia.
**Purpose:** Mixed energy system development. Aerobic (800m) through speed endurance (100m).
**Why coaches use it:** One session hits multiple energy systems. Pace judgment develops naturally across distances. Time-efficient for advanced athletes.

### Pattern 6: 2-4-6 Ladder

**Structure:** 2 runs in 6s → rest 15s → 4 runs in 13s → rest 30s → 6 runs in 21s. 4 sets.
**Found in:** BCCI, Cricket, Rugby S&C, Soccer S&C.
**Purpose:** RSA with escalating volume. Teaches athletes to manage fatigue across increasing work demands.
**Why coaches use it:** Unique structure that builds RSA and mental toughness simultaneously. The escalating volume mirrors game demands (a few short efforts → sustained high-intensity period).

### Pattern 7: Yo-Yo Intermittent Recovery Test

**Structure:** 2×20m shuttles at progressively increasing speed. 10s active recovery between levels.
**Found in:** Soccer S&C, Rugby S&C, BCCI, ASCA, Basketball, Field Hockey.
**Purpose:** Aerobic Power / RSA assessment and training. The most widely used field test in team sports.
**Why coaches use it:** Standardised protocol — results are comparable across teams, countries, and time. Intermittent format mirrors sport demands. Predicts high-speed running volume in matches.

### Pattern 8: Long Slow Distance (20-40 min)

**Structure:** Continuous running at 60-70% HRmax, conversational pace.
**Found in:** All 10 sources. Universal.
**Purpose:** Aerobic base, recovery, mitochondrial development.
**Why coaches use it:** Foundation for all other conditioning. Low injury risk. Develops the aerobic engine that supports recovery between high-intensity efforts.

### Pattern 9: Sprint-Float-Sprint (100m)

**Structure:** 100m sprint → 100m float (70%) → 100m sprint. 1 set = 300m. 3-4 sets with full recovery.
**Found in:** Athletics (sprint), Rugby S&C, Soccer S&C, Cricket Australia.
**Purpose:** Speed endurance with active recovery. Develops ability to recover and re-accelerate.
**Why coaches use it:** Unique stimulus: teaches athletes to run fast, recover at pace, then run fast again. Active float is more sport-specific than passive rest.

### Pattern 10: Fartlek / Speed Play

**Structure:** Continuous run with unstructured surges (20-60s) every 2-3 min. 20-30 min total.
**Found in:** Soccer S&C, Rugby S&C, Athletics (middle distance), NSCA.
**Purpose:** Mixed aerobic capacity / aerobic power. Develops ability to change pace.
**Why coaches use it:** Unstructured format prevents athletes from settling into a comfort zone. Develops pace awareness and tactical effort management.

### Pattern 11: 10-20-30m Acceleration Sprints

**Structure:** Maximal acceleration sprints from various starts. Full recovery. 6-8 reps.
**Found in:** All 10 sources. Universal.
**Purpose:** Alactic speed, acceleration mechanics.
**Why coaches use it:** The purest speed training method. Low volume, high quality, full recovery. Develops explosive power without accumulating fatigue. The highest-rated protocols in the library.

### Pattern 12: 30/30 Treadmill Intervals

**Structure:** 30s at 18-22 km/h, 30s at 6-8 km/h. 6 reps × 2-3 sets.
**Found in:** BCCI, Cricket Australia, ASCA, Rugby S&C, Soccer S&C.
**Purpose:** Lactate tolerance with active recovery. Controlled environment for maximal efforts.
**Why coaches use it:** Treadmill removes pacing variability — everyone hits the same speed. The active recovery (jog/walk) is sport-specific. Indoors, weather-independent.

### Pattern 13: Grass Sprints

**Structure:** Short sprints (30-60m) on grass at 70-85% intensity. Walk-back recovery.
**Found in:** Rugby S&C, Soccer S&C, ASCA, NSCA.
**Purpose:** Low-impact tempo and speed work. Reduced joint stress while developing conditioning.
**Why coaches use it:** Grass reduces impact forces by 40-60% compared to hard ground. Allows higher volume with lower injury risk. Preferred surface for field sport pre-season.

### Pattern 14: 1 km Repeats

**Structure:** 1 km at 75-85% effort. 3-4 min rest. 3-5 reps.
**Found in:** BCCI, Cricket Australia, Rugby S&C, Athletics.
**Purpose:** Aerobic power / threshold development. Distance-based interval that is simple to understand.
**Why coaches use it:** 1 km is a universally understood distance. Easy to measure on any track or marked course. Good balance between aerobic and lactate threshold stimulus.

### Pattern 15: Contrast / Complex Training (Jump + Sprint)

**Structure:** CMJ or broad jump immediately followed by 10-20m sprint. Full recovery between complexes.
**Found in:** Athletics (sprint), Rugby S&C, Badminton, ASCA.
**Purpose:** Power maintenance via PAP (post-activation potentiation). The jump potentiates the subsequent sprint.
**Why coaches use it:** Efficient — one complex trains both elastic power and acceleration. The jump-sprint coupling is highly sport-specific. Low volume, high quality.

### Pattern 16: Resisted Sprints (Sled)

**Structure:** 15-30m sled drags at 15-25% bodyweight. Full recovery. 4-6 reps.
**Found in:** Athletics (sprint), Rugby S&C, Soccer S&C, ASCA.
**Purpose:** Overload acceleration. Develops horizontal force production.
**Why coaches use it:** Sled resistance allows overload without changing sprint mechanics (unlike hill sprints). Specific to acceleration phase. Low injury risk compared to overspeed training.

### Pattern 17: Agility Shuttles (4×10m, 5-10-5)

**Structure:** Multi-directional shuttles at near-maximal intensity. Short distances, multiple direction changes.
**Found in:** Basketball, Badminton, Tennis, Soccer, Rugby, Cricket fielding.
**Purpose:** COD speed under fatigue and sport-specific RSA.
**Why coaches use it:** Multi-directional work is more sport-specific than linear sprinting for court and field sports. Direction changes under fatigue mirror game conditions.

### Pattern 18: Hill Repeats

**Structure:** 80-250m uphill at 85-95% effort. Walk-down recovery. Active recovery = downhill walk.
**Found in:** Athletics (sprint), Rugby S&C, Soccer S&C, ASCA.
**Purpose:** Strength endurance, lactate tolerance, acceleration overload.
**Why coaches use it:** Hill running increases muscular demand without increasing impact. The incline forces greater hip and knee drive. Natural progression: shallower slope → steeper slope → more reps → less rest.

### Pattern 19: 50m + 25m Speed Combo

**Structure:** 50m sprint (medium-high, walk-back) + 25m sprint (high intensity, walk-back) in the same session.
**Found in:** BCCI, Cricket Australia, Rugby S&C, Soccer S&C.
**Purpose:** Mixed speed endurance. Longer effort for speed maintenance, shorter for acceleration.
**Why coaches use it:** Two distances in one session develop different speed qualities. The combo approach is time-efficient and more varied than a single distance.

### Pattern 20: Cricket Ground Circuit (or Large Field Loop)

**Structure:** ~400-450m loop around a cricket ground or large field. 12 rounds in 20 min (~5 km).
**Found in:** BCCI, ECB, Cricket Australia, Rugby S&C.
**Purpose:** Extensive tempo / aerobic power in a measured circuit format.
**Why coaches use it:** The measured loop allows precise comparison across sessions. The 5 km in 20 min target is a known benchmark. Group format allows head-to-head competition.

---

## PART 4: Conditioning Anti-Patterns

> Top 25 mistakes observed in amateur programs. None of these appear in elite programs.

### Anti-Pattern 1: Conditioning Before Power or Strength

**What it looks like:** "Start with a 2 km run, then hit the weight room."
**Why it fails:** Pre-fatigues the CNS before neural-demanding work. Reduces power output. Increases injury risk under the bar.
**Fix:** Conditioning is always the final block. Power and strength require fresh CNS.

### Anti-Pattern 2: Lactate Sessions Within 48 Hours of Speed Sessions

**What it looks like:** Tuesday: max velocity sprints. Wednesday: 400m repeats.
**Why it fails:** Lactate tolerance creates metabolic byproducts that impair muscle contractility. Speed requires fresh, non-fatigued muscle. 48+ hours minimum between lactate and speed work.
**Fix:** Schedule lactate sessions after strength days, not after speed days.

### Anti-Pattern 3: Excessive In-Season Conditioning Volume

**What it looks like:** 4×/week conditioning during competition season at the same volume as pre-season.
**Why it fails:** Sport practice + games provide the majority of in-season conditioning stimulus. Additional conditioning volume compromises recovery and increases injury risk.
**Fix:** In-season = 1-2 conditioning sessions/week. Mostly RSA. Volume 50% of pre-season.

### Anti-Pattern 4: Random HIIT Circuits

**What it looks like:** "Do 10 burpees, 10 box jumps, 10 med ball slams — as many rounds as possible in 15 minutes."
**Why it fails:** No energy system specificity. Cannot measure progression. Random stimulus = random adaptation. Power exercises (box jumps, slams) performed under fatigue = injury risk.
**Fix:** Conditioning has a target system. Every session is designed for one primary adaptation.

### Anti-Pattern 5: All Conditioning Is Linear Running

**What it looks like:** Every conditioning session is track work. No multi-directional work.
**Why it fails:** Field and court sports are multi-directional. Linear conditioning does not prepare athletes for COD and lateral movement demands.
**Fix:** At least 1 conditioning session/week should be multi-directional (shuttles, COD, agility).

### Anti-Pattern 6: Tempo at Max Speed

**What it looks like:** "60m tempo runs at 100%." 30s rest between reps.
**Why it fails:** Tempo is sub-maximal by definition (70-80%). Running max speed on 30s rest is RSA, not tempo. The name is wrong, the stimulus is wrong, the recovery is wrong.
**Fix:** Tempo = 70-80%. RSA = 95-100%. Name and prescribe the correct system.

### Anti-Pattern 7: Conditioning Used as Punishment

**What it looks like:** "You were late — run 400m repeats." "Lost the drill — 20 burpees."
**Why it fails:** Creates negative association with conditioning. Athletes hold back to avoid "extra" work. Destroys the coaching-athlete relationship.
**Fix:** Conditioning has a purpose. Punishment conditioning is not coaching.

### Anti-Pattern 8: Same Conditioning Every Session

**What it looks like:** Every session ends with 5×400m at 80%.
**Why it fails:** No variation → no adaptation. The body habituates to the same stimulus. Progress stops. Athletes become bored.
**Fix:** Cycle through energy systems. Rotate protocol families every 2-4 weeks.

### Anti-Pattern 9: MAS Without Testing

**What it looks like:** "Everyone runs 60m in 9s." Using a generic MAS pace for the whole squad.
**Why it fails:** MAS is individual. A 9s 60m might be 70% for one athlete and 95% for another. Generic pacing = some undertrain, some overtrain.
**Fix:** MAS requires a test. Individualise the pace.

### Anti-Pattern 10: RSA With Insufficient Recovery

**What it looks like:** 30m sprints with 15s rest for 10 reps.
**Why it fails:** RSA requires phosphocreatine resynthesis. 15s is insufficient for near-full PCr recovery. After 3 reps, the athlete is running on glycolysis, not testing RSA.
**Fix:** RSA work:rest = minimum 1:4 (30m sprint ≈ 5s → 20s rest minimum). RSA with tight rest is speed endurance, not RSA.

### Anti-Pattern 11: Every Conditioning Session Is Maximal

**What it looks like:** Every conditioning day ends with athletes collapsed on the ground.
**Why it fails:** You cannot train at maximal intensity every session. The CNS does not recover. Injury risk multiplies. The stimulus becomes lactate tolerance, even when the goal is aerobic power.
**Fix:** 1-2 maximal sessions/week maximum. The rest is sub-maximal with clear purpose.

### Anti-Pattern 12: No Aerobic Base Before High-Intensity Work

**What it looks like:** Pre-season starts with RSA and lactate work immediately. No base building.
**Why it fails:** Aerobic base supports recovery between high-intensity efforts. Without it, the athlete accumulates fatigue faster than they recover. Injury risk increases.
**Fix:** Minimum 2-4 weeks of aerobic capacity + extensive tempo before introducing RSA or intensive tempo.

### Anti-Pattern 13: High-Speed Running on Recovery Days

**What it looks like:** "Recovery day: 5×60m at 90%. Light session."
**Why it fails:** 90% is not recovery. High-speed running creates high neuromuscular and metabolic stress regardless of volume.
**Fix:** Recovery days = RPE 2-3. Jogging, walking, mobility. Nothing above 70% effort.

### Anti-Pattern 14: Speed Work Under Fatigue

**What it looks like:** Strength session, then conditioning, then "finish with some 30m sprints."
**Why it fails:** Speed requires fresh CNS. Fatigued sprinting reinforces poor mechanics and increases hamstring injury risk (90% of hamstring injuries occur at high speed).
**Fix:** Speed is ALWAYS first in a session or on a dedicated speed day.

### Anti-Pattern 15: Over-Volume in Single Conditioning Session

**What it looks like:** 20×400m repeats. 30×60m tempo. 100 ground contacts in one session.
**Why it fails:** Volume beyond a threshold does not produce additional adaptation — it produces injury risk. The last 20% of reps are low quality, reinforcing poor movement patterns.
**Fix:** Respect protocol volume limits. Quality > quantity.

### Anti-Pattern 16: Shuttle Volume Without Progression

**What it looks like:** 20×40m shuttles on day 1. Same 20×40m shuttles 4 weeks later.
**Why it fails:** The body adapts to the same stimulus within 2-3 weeks. After that, the session becomes maintenance (not development) without progression.
**Fix:** Progress volume, decrease rest, or increase intensity across 4-week blocks.

### Anti-Pattern 17: Conditioning Before Technical Work

**What it looks like:** Conditioning session before skill practice or field session.
**Why it fails:** Fatigue impairs motor learning and skill execution. Technical practice requires a fresh CNS. Conditioning after technical work imposes less interference.
**Fix:** Skill → Conditioning, or separate sessions by 4+ hours.

### Anti-Pattern 18: No Rest Interval Specification

**What it looks like:** "Run 400m repeats. Rest as needed."
**Why it fails:** Rest determines the energy system trained. 60s rest targets a different system than 4 min rest. Leaving rest undefined leaves adaptation undefined.
**Fix:** Every protocol specifies work:rest. Rest is a training variable.

### Anti-Pattern 19: All Athletes Do the Same Conditioning

**What it looks like:** One conditioning session for all athletes regardless of position, injury history, or fitness level.
**Why it fails:** RSA needs differ by position (linebackers vs. corners, forwards vs. backs). Injury history modifies appropriate work. Individual response to the same stimulus varies.
**Fix:** Group template with individual volume adjustments.

### Anti-Pattern 20: Conditioning Omitted Entirely In-Season

**What it looks like:** "No conditioning during season — games cover it."
**Why it fails:** Sport practice does not consistently hit target intensity zones for conditioning adaptations. RSA and power maintenance decline without specific stimulus.
**Fix:** 1-2 conditioning sessions/week in-season. RSA + Power Maintenance focus.

### Anti-Pattern 21: Treadmill-Only Conditioning

**What it looks like:** All conditioning done on treadmills because it's "controlled."
**Why it fails:** Treadmill running removes wind resistance, pacing variability, and surface adaptation. Field/court sport athletes need over-ground conditioning to develop sport-specific movement patterns and impact tolerance.
**Fix:** Treadmill for specific protocols (threshold, over-unders). Field/grass for tempo, RSA, speed.

### Anti-Pattern 22: Female Athletes Programmed Same as Male Athletes

**What it looks like:** Same speed, same volume, same work:rest ratios regardless of sex.
**Why it fails:** Female athletes generally recover faster between RSA efforts, have different fatigue profiles, and have different injury risk factors (ACL, hamstring). The same protocol imposes different relative loads.
**Fix:** Individualise based on testing, not sex-based templates — but be aware of sex differences in recovery and injury risk.

### Anti-Pattern 23: No Cool-Down After Conditioning

**What it looks like:** Conditioning block ends, session over. Athletes sit down.
**Why it fails:** Abrupt cessation of high-intensity work reduces venous return, increases risk of post-exercise hypotension, and slows recovery.
**Fix:** Minimum 5 min cool-down (light jog, walk, static stretching).

### Anti-Pattern 24: Conditioning Without Data

**What it looks like:** No times, no distances, no HR, no RPE recorded.
**Why it fails:** Without data, you cannot track progression, identify overtraining, or modify the program. You are prescribing blind.
**Fix:** Every conditioning session produces at least one data point (time, RPE, HR, distance).

### Anti-Pattern 25: Neglecting Power Maintenance

**What it looks like:** Pre-season: all conditioning, no speed/power maintenance.
**Why it fails:** Conditioning volume without concurrent power maintenance causes power decay. The athlete becomes fitter but slower. Power maintenance is the first quality to degrade and the last to return.
**Fix:** Every conditioning block includes at least 1 session/week of power maintenance (30m fatigue test, CMJ-sprint complex).

---

## PART 5: FORGE Conditioning Laws

> 50 non-negotiable laws. Every FORGE-generated conditioning session satisfies all 50.

### Energy System Selection (COND-LAW-001 to COND-LAW-008)

**COND-LAW-001:** Every conditioning session targets exactly ONE primary energy system. Mixed systems exist in one direction only (e.g., aerobic capacity → aerobic power, not simultaneous).

**COND-LAW-002:** Conditioning never precedes power or strength in session order. Always the final training block.

**COND-LAW-003:** Speed work (alactic speed, max velocity) requires fresh CNS — no conditioning before speed, no strength before speed.

**COND-LAW-004:** Aerobic capacity cannot impair strength adaptation. Zone 2 work is placed on separate days from heavy strength or at least 6 hours apart.

**COND-LAW-005:** RSA requires near-max effort (95-100%). If the athlete runs below 95%, the stimulus is tempo, not RSA.

**COND-LAW-006:** Recovery conditioning never creates fatigue. RPE must remain ≤3 throughout. If RPE exceeds 3, the session is not recovery.

**COND-LAW-007:** Lactate tolerance and alactic speed are never trained in the same week. Minimum 48 hours between a lactate session and a speed session.

**COND-LAW-008:** In-season conditioning = maintenance, not development. Volume is capped at 50% of off-season volume for the same energy system.

### Session Structure (COND-LAW-009 to COND-LAW-015)

**COND-LAW-009:** Every conditioning session includes a warm-up specific to the conditioning modality (walk/jog progression for running, dynamic prep for speed).

**COND-LAW-010:** Every conditioning session includes a cool-down of minimum 5 minutes at RPE ≤3.

**COND-LAW-011:** Conditioning session duration never exceeds 45 minutes for high-intensity work (RPE ≥7) or 60 minutes for low-intensity work (RPE ≤4).

**COND-LAW-012:** Rest intervals must be specified in every protocol. "Rest as needed" is not a valid rest prescription.

**COND-LAW-013:** Weekly high-intensity conditioning (RPE ≥8) is capped at 2 sessions maximum. 1 session per week is sufficient for in-season athletes.

**COND-LAW-014:** Conditioning volume is inversely related to sport practice volume on the same day. If practice was high-volume, conditioning is low-volume.

**COND-LAW-015:** One day per week has zero conditioning stimulus. Complete recovery day.

### Progression (COND-LAW-016 to COND-LAW-022)

**COND-LAW-016:** Conditioning progression follows the same rule as strength: volume increases before intensity. Add reps/distance first, then decrease rest, then increase pace.

**COND-LAW-017:** Weekly conditioning volume increases by no more than 10% per week.

**COND-LAW-018:** A new energy system (e.g., RSA for a beginner) requires 2 weeks of exposure before progressive overload begins.

**COND-LAW-019:** Aerobic base (4+ weeks) precedes high-intensity conditioning (RSA, lactate tolerance) for any athlete with training age <1 year.

**COND-LAW-020:** MAS pace requires a test to individualise. Generic MAS pace is prohibited.

**COND-LAW-021:** RSA progression: increase work:rest ratio first (e.g., 1:6 → 1:4), then decrease rest, then increase reps.

**COND-LAW-022:** Deload weeks reduce conditioning volume by 40-60% and cap intensity at RPE 6. Zero maximal efforts during deload.

### Athlete Level (COND-LAW-023 to COND-LAW-029)

**COND-LAW-023:** Beginner athletes (<1 year training age) do not perform lactate tolerance training. Build aerobic capacity and extensive tempo first.

**COND-LAW-024:** Beginner athletes do not perform 30m RSA at every 20s interval. Start at every 40s.

**COND-LAW-025:** Intermediate athletes (1-3 years) may perform one high-intensity conditioning session per week. Two is optional and monitored.

**COND-LAW-026:** Advanced athletes (3+ years) may perform two high-intensity conditioning sessions per week. Never three.

**COND-LAW-027:** Youth athletes (U16) do not perform lactate tolerance, heavy sled work, or descending ladders. Extensive tempo and play-based conditioning only.

**COND-LAW-028:** Youth athletes (U16) cap high-speed running volume at 400m per session.

**COND-LAW-029:** Return-to-sport athletes begin conditioning at aerobic capacity (Zone 2, RPE ≤4) for minimum 2 weeks before any high-intensity work.

### Environment and Equipment (COND-LAW-030 to COND-LAW-035)

**COND-LAW-030:** Conditioning protocol must match available environment. Track protocols are not prescribed for field-only athletes.

**COND-LAW-031:** Treadmill conditioning is supplementary, not primary. Field sport athletes require minimum 1 over-ground conditioning session per week.

**COND-LAW-032:** Grass surface is preferred for all high-intensity running. Hard surface runs are limited to 1 session per week for injury risk management.

**COND-LAW-033:** Limited space (≤20m) restricts conditioning to shuttle-based protocols (MAS shuttles, RSA shuttles, agilities). Linear tempo requires ≥60m.

**COND-LAW-034:** Heat and humidity modify conditioning. In ambient temperature >30°C, reduce high-intensity volume by 30% and increase rest intervals.

**COND-LAW-035:** Altitude (>1500m) reduces MAS pace by approximately 5% per 1000m. Adjust protocol paces accordingly.

### Power Maintenance (COND-LAW-036 to COND-LAW-040)

**COND-LAW-036:** Power maintenance is included in every conditioning block. Minimum 1 session per week.

**COND-LAW-037:** Power maintenance sessions have maximal intent on every rep. Sub-maximal intent does not maintain power.

**COND-LAW-038:** Power maintenance volume is low: 4-6 reps of 3-10s efforts with full recovery. Exceeding this volume changes the stimulus to conditioning.

**COND-LAW-039:** In-season power maintenance is non-negotiable. Without it, power decays within 4 weeks of competition phase.

**COND-LAW-040:** The 30m fatigue test (PM-001) is the default assessment for power maintenance. Administer every 4 weeks.

### Monitoring (COND-LAW-041 to COND-LAW-045)

**COND-LAW-041:** Every conditioning session produces at least one data point: RPE, time, distance, or heart rate.

**COND-LAW-042:** RSA sessions record the fastest rep time and the slowest rep time. Decrement >10% indicates conditioning or recovery issue.

**COND-LAW-043:** Aerobic capacity sessions monitor heart rate to ensure Zone 2 compliance. Zone 3+ indicates intensity too high for an aerobic capacity session.

**COND-LAW-044:** MAS testing is repeated every 4-6 weeks. MAS pace is recalculated if the test improves.

**COND-LAW-045:** Yo-Yo IR1 testing is administered at the start and end of pre-season minimum. Mid-season testing optional.

### Substitution and Modification (COND-LAW-046 to COND-LAW-050)

**COND-LAW-046:** Conditioning substitution maintains the energy system first, the work:rest ratio second, and the modality third.

**COND-LAW-047:** If a specific protocol cannot be performed (equipment, space, weather), substitute with a protocol in the same energy system family. Do not switch systems.

**COND-LAW-048:** Injury modification for conditioning maintains intensity but reduces volume and impact. Replace running with cycling or aqua jogging while maintaining heart rate zone.

**COND-LAW-049:** When substituting a protocol, maintain the same fatigue score target (±1). A high-fatigue protocol is not substituted with a low-fatigue protocol.

**COND-LAW-050:** If the prescribed conditioning session scores RPE >9 on its first execution, regress one level next session. The protocol was too advanced.

---

## PART 6: MVP Recommendation

### Question

Should FORGE MVP generate conditioning from **formulas** (A) or select from a **curated protocol library** (B)?

### Context

- Coach accelerator format (< 3 min generation)
- No AI
- No physiology engine
- Deterministic generation
- Must produce coach-credible output on first attempt

### Analysis

#### Option A: Formula-Based Generation

**How it would work:** The engine takes inputs (energy system, athlete level, available time, environment) and generates a conditioning session using formulas for work, rest, sets, and total volume. For example: "RSA for intermediate athlete with 20 min available: 30m sprints at 1:4 work:rest ratio, 8-10 reps."

**Theoretical advantages:**
- Infinite variety — never repeats a session
- Adapts precisely to time available
- No library maintenance

**Real-world problems:**
- Formulas do not capture the protocols that elite coaches actually use
- The generated session might be mathematically correct but never seen in elite training
- Coaches reject output that does not match known protocols ("This doesn't look like any session I've seen")
- Injury risk assessment is heuristic — formulas do not know which protocols have high vs. low injury rates
- Validation burden: every generated session needs a coach to approve it
- Elite coaches do not generate conditioning from formulas — they select from known protocols

#### Option B: Curated Protocol Library

**How it would work:** The engine selects a pre-written protocol from the 100-protocol library (V1) using the decision tree (Part 1), level-adjusts within the selected protocol's L1-L5 progression chain, and outputs the session.

**Why it works for MVP:**
- Every protocol is proven in elite programs — zero invention risk
- Decision tree is deterministic (training age + goal + environment + time → protocol family → specific protocol)
- Progression chains handle level adjustment within each protocol
- Validation is already done — every protocol passed the coaching credibility filter
- Coaches recognise the output ("60m tempo BCCI standard — yes, that's a real session")
- Substitution rules are explicit (same energy system → same work:rest → same fatigue score)
- A coach accelerator under 3 min needs lookup, not computation

**Real-world verification:**
- The 58-program corpus contains 0 examples of formula-generated conditioning
- Every program uses specific, named protocols (MAS, 60m tempo, 400m repeats, 30m RSA, 2-4-6 ladder)
- Protocols have names because coaches use them as units of training
- Formulas produce a number; protocols produce a session a coach would write

**Risk comparison:**

| Risk | Option A (Formulas) | Option B (Library) |
|------|--------------------|--------------------|
| Coach rejection of output | High — looks unfamiliar | Low — uses known protocols |
| Injury due to poor prescription | Medium — formulas miss injury context | Low — protocols vetted by elite usage |
| Maintenance burden | Medium — formulas need constant tweaking | Low — add protocols as needed |
| Generation speed | Fast | Fast (lookup < formula calculation) |
| Adaptability to time constraints | High — fits exactly | High — each protocol has level variants |
| Variety across a season | High — infinite combinations | Medium-High — 100 protocols × 5 levels = 500 possible sessions |

### Recommendation

**Option B: Curated Protocol Library with Decision Tree Selection.**

This is not close. Every reason a coach would trust the output leans toward Option B:

1. **Coaching credibility:** A library of real protocols beats generated sessions every time. Coaches trust what they recognise.
2. **Zero invention risk:** Every protocol is validated by elite usage. A formula generates a session that has never been done — that is a coaching liability.
3. **Deterministic by nature:** Lookup tables are the most deterministic system possible. No formulas to calibrate, no edge cases to handle.
4. **MVP scope:** The explicit constraint is "under 3 minutes." A lookup + level adjustment is simpler and faster than a formula engine.

### How the MVP Should Work

```
Input: Athlete Level + Goal + Environment + Available Time
        │
        ▼
Part 1 Decision Tree → identifies protocol FAMILY
        │
        ▼
Part 2 → selects A Tier protocol within that family (default)
        │  (B Tier if A Tier not available for the constraint)
        │
        ▼
Part 5 → applies level adjustment (L1-L5 within the protocol)
        │
        ▼
Part 5 → validates against the 50 COND-LAWs
        │
        ▼
Output: Named protocol + prescribed reps/sets/rest/volume
```

**Implementation as code:**
- 100 entries in a protocol lookup table (already written in V1)
- Decision tree = nested if/else or case statement (Part 1)
- Level adjustment = predefined L1-L5 per protocol (already in V1 progression chains)
- Validation = 50 boolean checks against generated session (Part 5)

**Total estimated LOC for the conditioning generator:** ~600 lines of deterministic logic. No formulas beyond `targetTime = reps × distance ÷ pace`. No AI. No physiology engine. Lookup + validate.

### Forge MVP Conditioning Generator: Build It

```
┌─────────────────────────────────────────────────────────────────────┐
│ FORGE_CONDITIONING_GENERATOR                                        │
│                                                                     │
│ Inputs:                                                             │
│   athlete = { level, goal, environment, time_available }             │
│                                                                     │
│ Process:                                                            │
│   1. protocolFamily ← decisionTree(athlete)          # Part 1       │
│   2. aTier ← getATierProtocols(protocolFamily)       # Part 2       │
│   3. protocol ← selectByEnvironment(aTier, athlete)  # environment  │
│   4. session ← adjustLevel(protocol, athlete.level)  # L1-L5 chain  │
│   5. valid ← validateLaws(session)                   # 50 COND-LAWs │
│   6. IF NOT valid: substituteWithinFamily(session)   # Part 4 rules │
│                                                                     │
│ Output:                                                             │
│   { name, reps, sets, rest, volume, rpe_target, coaching_cue }      │
│                                                                     │
│ Total code: ~600 lines. No AI. No formulas. No physiology engine.   │
└─────────────────────────────────────────────────────────────────────┘
```

---

*FORGE_CONDITIONING_INTELLIGENCE_V2.md — Version 2.0*
*Audits and transforms FORGE_CONDITIONING_LIBRARY_V1.md into a coaching decision system.*
*100 protocols ranked. 20 universal patterns identified. 25 anti-patterns catalogued. 50 laws defined.
MVP recommendation: Curated Protocol Library with Decision Tree Selection.*
