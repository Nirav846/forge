# FORGE Conditioning Library Rebalance V2

**Starting count:** 91 protocols (41 A-tier, 42 B-tier, 8 C-tier)
**Target count:** ~100 protocols

---

## A. Protocols That Stay As-Is

### Aerobic Capacity — all 12 stay
AC-001 through AC-012. These are foundational, sport-agnostic. Only change: add sport_tags=["any"] and environment_category.

### Aerobic Power — all 11 stay
AP-001 through AP-011. Add sport_tags and environment_category.

### Extensive Tempo — all 10 stay
ET-001 through ET-010. Add sport_tags and environment_category.

### Alactic Speed — all 8 stay
AS-001 through AS-008. Add sport_tags and environment_category.

### Power Maintenance — all 7 stay
PM-001 through PM-007. Add sport_tags and environment_category.

### Recovery Conditioning — all 6 stay
RC-001 through RC-006. Add sport_tags and environment_category.

---

## B. Protocols That Need Reclassification

### Speed Endurance — reclassify environment
| ID | Current environment | New environment_category | Change |
|----|-------------------|------------------------|--------|
| SE-001 (150m Repeats) | ["Track"] | field | Track-only, but 150m works on field |
| SE-002 (Flying 30s) | ["Track"] | field | Same |
| SE-003 (Cut-downs) | ["Track"] | field | Same |
| SE-006 (100m × 6) | ["Track"] | field | Same |
| SE-008 (120m Repeats) | ["Track"] | field | Same |
| SE-009 (80m Flying Start) | ["Track"] | field | Same |
| SE-005 (50m × 8 + 25m × 6) | ["Field", "Track"] | field | Already field-compatible |
| SE-007 (Accel Build-up 60m) | ["Track", "Field"] | field | Already field-compatible |
| SE-004 (Sprint Float Sprint) | ["Track"] | field | Add Field to environment list |

### Intensive Tempo — add Field to environments
IT-001 through IT-008 are all ["Track"] currently. Field sport athletes need 400m/200m/300m repeats too. Add "Field" to environment lists.

### Lactate Tolerance — add Field to environments
LT-001 through LT-005, LT-007, LT-009 are all ["Track"]/["Field"] split. LT-008 is ["Hill"]. Add "Field" to some of the track-only ones.

---

## C. Protocols That Get Sport Applicability Tags

Each protocol gets:
- `environment_category`: field/court/gym/recovery
- `sport_tags`: list of sports or ["any"]

### environment_category assignment
- All AC protocols → field (AC-004, AC-010 which are gym → field+gym)
- All AP protocols → field (AP-006/007/008 which are court → field+court)
- All ET → field
- All IT → field
- All RSA → field (RSA-005/008/009/011 which are court → field+court)
- All SE → field
- All AS → field (AS-001/007 which are court → field+court)
- All LT → field
- All PM → field (PM-005/006 which are court → field+court)
- All RC → recovery

### sport_tags assignment
| Sport tags | Protocols |
|------------|-----------|
| ["any"] | AC-001/002/003/004/005/006/007/008/009/010/011/012 |
| ["any"] | RC-001/002/003/004/005/006 |
| ["cricket", "rugby", "soccer"] | ET-001/002/003/004/005/008/009/010 |
| ["cricket"] | ET-006 (Cricket Ground Circuit), ET-007 (2-4-6 Ladder), RSA-001/002 (BCCI standard) |
| ["cricket", "rugby", "soccer"] | AP-001 (MAS 60m), AP-003 (1 km Repeats), AP-011 (5×3 min) |
| ["soccer", "rugby"] | AP-008 (Yo-Yo IR1) |
| ["tennis", "badminton", "basketball"] | AP-006 (20m MAS Shuttle), AP-007 (30-15 IFT) |
| ["tennis", "badminton"] | RSA-009 (10m Shuttle RSA) |
| ["any"] | AS-001/002/003/004/006 |
| ["any"] | PM-001/002/003/004/005 |
| ["tennis", "badminton", "basketball"] | PM-006 (5-10-5 Shuttle) |
| ["any"] | LT-001/002/004/006/009 |
| ["cricket", "rugby", "soccer"] | LT-003/005 (complex protocols for advanced team sport) |
| ["any"] | SE-001/002/003/004/005/006/007/008/009 |

---

## D. Redundant / Weak / Dead Protocols

### Weak — promote tier
| ID | Current tier | New tier | Reason |
|----|-------------|----------|--------|
| SE-005 (50m×8 + 25m×6 Combo) | B | A | Field sport standard, high utility |
| SE-006 (100m×6) | B | A | Common field sport protocol |
| RSA-005 (20m Shuttle RSA) | B | A | Both court and field applicable |
| RSA-011 (Direction Change RSA) | B | A | High sport-specific utility |

### Dead — leave as tier C but document
IT-002 (Descending Ladder), IT-007 (Pyramid), IT-008 (Negative Split 800s), AS-005 (Contrast Sprints), PM-007 (Hurdle Hop), RSA-010 (German Volume), LT-003 (Broken 800m), LT-005 (Short-Long-Short). These stay as-is — occasionally useful for elite track athletes.

---

## E. New Protocols to Add

### Court Conditioning (5 new)
1. **CC-001 "Tennis Rally Intervals"** — 15s work / 20s rest, multi-directional court coverage. environment_category=court, sport_tags=["tennis"], fatigue=4, tier A
2. **CC-002 "Badminton Rally Density"** — 8s work / 15s rest, explosive multi-directional. environment_category=court, sport_tags=["badminton"], fatigue=4, tier A
3. **CC-003 "Lateral Shuffle Conditioning"** — 10m lateral shuffles × 5 reps, 30s rest. environment_category=court, sport_tags=["tennis", "badminton", "basketball"], fatigue=3, tier A
4. **CC-004 "Diagonal Recovery + Re-accel"** — 5m diagonal → recover → 5m diagonal opposite. environment_category=court, sport_tags=["tennis", "badminton"], fatigue=4, tier A
5. **CC-005 "Court Sport RSA — 5m Shuttle"** — 5 × 5m shuttles, 25m total per rep, 45s rest. environment_category=court, sport_tags=["tennis", "badminton", "basketball"], fatigue=4, tier A

### Gym Conditioning (2 new)
6. **GC-001 "Bike HIIT — 30s On / 30s Off"** — 30s maximal effort / 30s easy spin, 10-15 rounds. environment_category=gym, sport_tags=["any"], fatigue=4, tier A
7. **GC-002 "Rower HIIT — 250m Repeats"** — 250m maximal row / 60s easy row, 6-10 reps. environment_category=gym, sport_tags=["any"], fatigue=4, tier A
8. **GC-003 "KB/DB Circuit Conditioning"** — 4 exercises, 40s work / 20s rest, 3-4 rounds. environment_category=gym, sport_tags=["any"], fatigue=3, tier A

### Field Conditioning (1 new)
9. **FC-001 "Cricket Bowling Spell Simulation"** — 6-over simulation: 30s high-intensity work (run-up, bowl, recover), 60s walk. Repeat 6 times = 1 spell. environment_category=field, sport_tags=["cricket"], fatigue=4, tier A

### Recovery Conditioning (1 new)
10. **RC-007 "Light Bodyweight Circuit"** — Low-rep bodyweight circuit (squats, press-ups, rows, plank) at 50% effort. environment_category=recovery, sport_tags=["any"], fatigue=1, tier A
11. **RC-008 "Pool Walk/Jog Intervals"** — 2 min walk / 3 min light jog in shallow pool. environment_category=recovery, sport_tags=["any"], fatigue=1, tier A

**Total:** 91 + 11 = 102 protocols
