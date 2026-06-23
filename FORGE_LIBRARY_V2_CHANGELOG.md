# FORGE Library V2 Changelog

**Date:** 2026-06-19
**Author:** AI-assisted implementation
**Total Exercises:** 201 → 241 (+40)

---

## Summary

V2 eliminates 7 empty cells and 8 single-exercise cells from V1's coverage matrix. New systems include a complete Hip Flexor progression (L1–L5, Acc family) and Pallof progression (L1–L5, Rot family). Sport-specific gaps in Sprint (deceleration, lateral shuffle, crossover, sled push) and Plyo (single-leg depth jump, single-leg landing) are filled.

---

## Changes by Family

### Acc (+7)
- Acc-022 Wall March L1 (Hip Flexor system)
- Acc-023 Dead Bug (Hip Flexor) L1
- Acc-024 Band Hip Flexion L2
- Acc-025 Seated Hip Flexor Raise L3
- Acc-026 Bench Hip Flexor Lean Back L4
- Acc-027 Standing Cable Hip Flexion L5
- Acc-028 Cable Face Pull L3 (accessory)

### Ball (+1)
- Ball-014 Med Ball Overhead Slam (max) L5

### Carry (+4)
- Carry-014 Single-Arm Farmer Carry L1
- Carry-015 Heavy Bear Hug Carry L5
- Carry-016 Single-Arm Overhead Carry L4
- Carry-017 Bottom-Up KB Carry L5

### Core (0)
- No changes

### DLHD (+3)
- DLHD-015 Prone Hip Extension L1
- DLHD-016 Kettlebell Swing (two-arm) L3
- DLHD-017 Cable Pull-Through L3

### DLKD (+1)
- DLKD-013 Heel-Elevated Barbell Squat L5

### HPull (+1)
- HPull-012 Yates Row L5

### HPush (+1)
- HPush-011 Barbell Floor Press L5

### Plyo (+2)
- Plyo-015 Single-Leg Depth Jump L5
- Plyo-016 Single-Leg Landing (soft) L3

### Rot (+7)
- Rot-011 Pallof Hold L1
- Rot-012 Standing Pallof Press L3
- Rot-013 Split Stance Pallof Press L4
- Rot-014 Pallof Walkout L4
- Rot-015 Single-Leg Pallof Press L5
- Rot-016 Reactive Pallof Press L5
- Rot-017 Reactive Rotational Catch & Throw L5

### SLHD (+2)
- SLHD-011 Weighted Nordic Hamstring Curl L5
- SLHD-012 Bird Dog Hip Extension L1

### SLKD (+1)
- SLKD-013 Weighted Pistol Squat L5

### Sprint (+4)
- Sprint-019 Deceleration Sprint (drop-stop) L3
- Sprint-020 Reactive Lateral Shuffle L4
- Sprint-021 Crossover Step + Accelerate L4
- Sprint-022 Sled Push L4

### VPull (+2)
- VPull-013 Band Lat Pulldown L1
- VPull-014 Archer Pull-Up L5

### VPush (+4)
- VPush-011 Half-Kneeling DB Overhead Press L1
- VPush-012 Split Jerk L5
- VPush-013 Elevated Pike Push-Up L3
- VPush-014 Tall-Kneeling Landmine Press L2

---

## Coverage Improvement

| Metric | V1 | V2 |
|--------|----|----|
| Empty cells | 7 | 0 |
| Single-exercise cells | 14 | 6 |
| Exercises < 11/family | — | 0 |
| Hip Flexor system | No | L1–L5 |
| Pallof system | L1 only | L1–L5 |

## Regression Check

- `src/forge/data.py`: SELECTION_PRIORITIES appended with new IDs (existing order preserved)
- Progression chains: 27 pre-existing external references unchanged; 0 new breaks
- All 241 IDs load cleanly
- No schema changes, entity changes, or family additions
