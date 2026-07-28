# FORGE Program Edit Distance Audit V1

**Date:** 2026-06-19
**Programs Generated:** 100
**Total Sessions Reviewed:** 2152
**Total Decisions:** 12856
**Overall Edit Distance:** 10.7%

---
## Part 1 — Edit Distance Model

Five edit operations define the distance between a generated program and a coach-approved program:

| Operation | Symbol | Definition |
|-----------|--------|------------|
| Keep | ✓ | Exercise is appropriate for sport/level/phase/equipment. No change needed. |
| Swap | ↔ | Exercise is close but a better option exists in the same family (different difficulty, better sport fit, better equipment match). |
| Delete | ✗ | Exercise doesn't belong — wrong family for the sport, wrong slot position, or contraindicated. |
| Add | + | A mandatory or expected family slot has no exercise (empty). Coach must fill it. |
| Reorder | ↕ | Exercise is in a suboptimal slot position (e.g. Core not last, explosive work after strength). |

**Edit Distance %** = 1 − (Keeps ÷ Total Decisions) × 100

**Result:** 10.7% of all decisions were edits (not keeps).

---
## Part 2 — Review Protocol

100 athlete profiles were generated across 5 sports (20 per sport):

### Badminton
| Metric | Value |
|--------|-------|
| Programs | 20 |
| Sessions | 424 |
| Keep | 2232 (92.4%) |
| Swap | 56 (2.3%) |
| Delete | 0 (0.0%) |
| Add | 0 (0.0%) |
| Reorder | 128 (5.3%) |
| Edit Distance | 7.6% |
| Avg Credibility | 0.94 |

### Cricket
| Metric | Value |
|--------|-------|
| Programs | 20 |
| Sessions | 432 |
| Keep | 2392 (89.0%) |
| Swap | 104 (3.9%) |
| Delete | 0 (0.0%) |
| Add | 0 (0.0%) |
| Reorder | 192 (7.1%) |
| Edit Distance | 11.0% |
| Avg Credibility | 0.94 |

### Rugby
| Metric | Value |
|--------|-------|
| Programs | 20 |
| Sessions | 480 |
| Keep | 2448 (83.6%) |
| Swap | 256 (8.7%) |
| Delete | 0 (0.0%) |
| Add | 0 (0.0%) |
| Reorder | 224 (7.7%) |
| Edit Distance | 16.4% |
| Avg Credibility | 0.91 |

### Soccer
| Metric | Value |
|--------|-------|
| Programs | 20 |
| Sessions | 432 |
| Keep | 2488 (96.0%) |
| Swap | 40 (1.5%) |
| Delete | 0 (0.0%) |
| Add | 0 (0.0%) |
| Reorder | 64 (2.5%) |
| Edit Distance | 4.0% |
| Avg Credibility | 0.95 |

### Tennis
| Metric | Value |
|--------|-------|
| Programs | 20 |
| Sessions | 384 |
| Keep | 1920 (86.0%) |
| Swap | 48 (2.2%) |
| Delete | 0 (0.0%) |
| Add | 0 (0.0%) |
| Reorder | 264 (11.8%) |
| Edit Distance | 14.0% |
| Avg Credibility | 0.92 |

---
## Part 3 — Exercise Review

Across all programs, 182 unique exercises appeared. Each was classified as Keep, Swap, or Delete per occurrence.

### Most Frequently Selected Exercises

| Exercise | Appearances | Keep | Swap | Delete | Keep Rate |
|----------|-------------|------|------|--------|-----------|
| DLHD-001 Glute Bridge | 1075 | 1075 | 0 | 0 | 100.0% |
| HPush-003 Push-Up | 1024 | 1024 | 0 | 0 | 100.0% |
| Core-002 Plank | 1011 | 987 | 24 | 0 | 97.6% |
| DLKD-004 Goblet Squat | 886 | 886 | 0 | 0 | 100.0% |
| DLKD-001 Air Squat | 665 | 665 | 0 | 0 | 100.0% |
| HPull-001 Scapular Retraction | 584 | 584 | 0 | 0 | 100.0% |
| HPull-003 Inverted Row | 429 | 429 | 0 | 0 | 100.0% |
| Sprint-003 A-Skip | 412 | 412 | 0 | 0 | 100.0% |
| HPull-005 Dumbbell Row | 330 | 330 | 0 | 0 | 100.0% |
| Acc-002 Band Pull-Apart | 327 | 264 | 63 | 0 | 80.7% |
| HPush-006 Barbell Bench Press | 314 | 314 | 0 | 0 | 100.0% |
| DLHD-006 RDL | 252 | 252 | 0 | 0 | 100.0% |
| DLHD-003 Trap Bar Deadlift | 194 | 194 | 0 | 0 | 100.0% |
| SLKD-002 Split Squat | 185 | 185 | 0 | 0 | 100.0% |
| Carry-001 Farmer Carry | 185 | 76 | 109 | 0 | 41.1% |
| Ball-001 Med Ball Slam | 126 | 121 | 5 | 0 | 96.0% |
| SLKD-005 Bulgarian Split Squat | 96 | 96 | 0 | 0 | 100.0% |
| DLHD-015 Prone Hip Extension | 86 | 86 | 0 | 0 | 100.0% |
| DLKD-002 Wall Sit | 81 | 81 | 0 | 0 | 100.0% |
| Core-003 Side Plank | 79 | 79 | 0 | 0 | 100.0% |

---
## Part 4 — Blueprint Review

Each program is classified:
- **Accepted:** Edit distance ≤ 15% (coach would make minor tweaks)
- **Modified:** Edit distance 16–40% (coach would rewrite significant portions)
- **Rejected:** Edit distance > 40% (coach would start over)

| Blueprint | Total | Accepted | Modified | Rejected | Accept Rate |
|-----------|-------|----------|----------|----------|-------------|
| Court Sport Athletic Development | 4 | 4 | 0 | 0 | 100.0% |
| Deload / Active Recovery | 8 | 0 | 0 | 8 | 0.0% |
| Full Body Strength | 40 | 31 | 9 | 0 | 77.5% |
| Hypertrophy / Mass Accrual | 1 | 1 | 0 | 0 | 100.0% |
| Power Maintenance | 7 | 5 | 2 | 0 | 71.4% |
| Return to Sport (Foundation) | 11 | 0 | 11 | 0 | 0.0% |
| Rugby Off-Season | 5 | 5 | 0 | 0 | 100.0% |
| Sprint Development | 4 | 4 | 0 | 0 | 100.0% |
| Strength + Conditioning | 5 | 0 | 5 | 0 | 0.0% |
| Youth Foundation (U14-U20) | 15 | 15 | 0 | 0 | 100.0% |

---
## Part 5 — Hotspot Analysis

### Most Swapped Exercises

| Exercise | Appearances | Swaps | Swap Rate |
|----------|-------------|-------|-----------|
| Carry-001 Farmer Carry | 185 | 109 | 58.9% |
| Acc-002 Band Pull-Apart | 327 | 63 | 19.3% |
| Carry-010 Bear Hug Carry | 43 | 39 | 90.7% |
| Core-002 Plank | 1011 | 24 | 2.4% |
| Acc-001 Calf Raise | 70 | 11 | 15.7% |
| Acc-014 Single-Leg Calf Raise | 70 | 11 | 15.7% |
| Acc-003 Hollow Body Hold | 70 | 11 | 15.7% |
| Acc-004 Band Face Pull | 70 | 11 | 15.7% |
| Acc-006 Child's Pose | 66 | 11 | 16.7% |
| Acc-007 World's Greatest Stretch | 63 | 11 | 17.5% |
| Acc-008 Hip Flexor Stretch | 63 | 11 | 17.5% |
| Acc-010 5-Way Hip | 63 | 11 | 17.5% |
| Acc-011 Banded 5-Way Hip | 63 | 11 | 17.5% |
| Acc-012 Monster Walk | 63 | 11 | 17.5% |
| Acc-019 Band Shoulder External Rotation | 58 | 10 | 17.2% |

### Most Deleted Exercises

No exercises were deleted in this audit run.

### Family Edit Rates

| Family | Total Occurrences | Edit Rate |
|--------|-------------------|-----------|
| Carry | 408 | 56.9% |
| Acc | 1504 | 17.0% |
| Ball | 216 | 7.4% |
| Sprint | 672 | 0.0% |
| SLKD | 360 | 0.0% |
| Rot | 96 | 0.0% |
| HPush | 1608 | 0.0% |
| DLHD | 1864 | 0.0% |
| Core | 1720 | 0.0% |
| DLKD | 1872 | 0.0% |
| HPull | 1512 | 0.0% |
| Plyo | 152 | 0.0% |

### Blueprint Edit Rates

| Blueprint | Programs | Avg Edit Distance |
|-----------|----------|--------------------|
| Court Sport Athletic Development | 4 | 0.0% |
| Deload / Active Recovery | 8 | 50.0% |
| Full Body Strength | 40 | 3.8% |
| Hypertrophy / Mass Accrual | 1 | 0.0% |
| Power Maintenance | 7 | 18.4% |
| Return to Sport (Foundation) | 11 | 26.1% |
| Rugby Off-Season | 5 | 14.3% |
| Sprint Development | 4 | 0.0% |
| Strength + Conditioning | 5 | 16.7% |
| Youth Foundation (U14-U20) | 15 | 0.0% |

---
## Part 6 — Credibility Correlation

| Credibility | Sessions | Avg Edit Rate | Keep Rate |
|-------------|----------|---------------|-----------|
| 0.8/1.0 | 240 | 8.9% | 91.1% |
| 0.9/1.0 | 1001 | 4.9% | 95.1% |
| 1.0/1.0 | 911 | 3.8% | 96.2% |

**Finding:** 
Credibility scores range from 0.8 to 1.0. 
Edit rates decrease from 8.9% (lowest credibility) to 3.8% (highest credibility).

---
## Part 7 — Improvement Loop

### Process for updating without changing architecture:

#### 1. Exercise Priorities
- **Swap-heavy exercises** should move DOWN in `SELECTION_PRIORITIES` for specific sports, or be replaced earlier in substitution chains.
- **Delete-heavy exercises** should be reviewed for sport-family appropriateness. If an exercise is consistently deleted for certain sports, add it to a sport-specific exclusion list.
- **Add operations** indicate missing families in the slot resolution. If `resolve_slots()` consistently misses a sport-essential family, adjust `slot_order` in the blueprint definition.

#### 2. Substitution Logic
- Currently `substitution_engine.py` uses 4-priority chain: same family → same intent → same equipment → fallback.
- If exercises are frequently swapped WITHIN a family, the issue is priority ordering — not substitution logic.
- If exercises are frequently swapped ACROSS families, the issue is `INTENT_CATEGORIES` grouping or `CROSS_FAMILY_SUBSTITUTION` mapping.
- Update `INTENT_CATEGORIES` and `CROSS_FAMILY_SUBSTITUTION` in `data.py` to align with sport-specific patterns.

#### 3. Blueprint Composition
- Blueprints with high rejection rates need `slot_order` and `mandatory_families` adjusted.
- `min_session_composition` can be expanded to require sport-specific families.
- For each blueprint, the `mandatory_families` list and `optional_families` list determine slot resolution. If a sport primarily uses a blueprint but misses critical families, add them to `mandatory_families`.

#### Specific Actions Identified by This Audit

| Action | Trigger | Target |
|--------|---------|--------|
| Adjust priorities | Exercise swap rate > 30% | Related `SELECTION_PRIORITIES` entry |
| Review sport fit | Exercise delete rate > 15% | Sport-family relevance mapping |
| Update intent categories | Cross-family swap rate high | `INTENT_CATEGORIES` in data.py |
| Expand blueprint slots | Add operations > 5% of total | `slot_order` in blueprint_data.py |
| Tighten session flow | Reorder operations > 10% | `enforce_session_flow_rules` in blueprint_engine.py |

---
## Appendix — Raw Summary

| Metric | Value |
|--------|-------|
| Programs Generated | 100 |
| Total Sessions | 2152 |
| Total Decisions | 12856 |
| Keeps | 11480 (89.3%) |
| Swaps | 504 (3.9%) |
| Deletes | 0 (0.0%) |
| Adds | 0 (0.0%) |
| Reorders | 872 (6.8%) |
| Overall Edit Distance | 10.7% |
