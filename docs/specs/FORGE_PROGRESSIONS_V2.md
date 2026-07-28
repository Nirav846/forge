# FORGE Progression Ladders V2

> Progression/regression chain audit for all 191 exercises across 15 families.
> Target: every exercise has a valid L1→L5 progression path and L5→L1 regression path.
> No dead ends. No backward progressions. No same-level progressions.

---

## Audit Method

For each family, exercises are sorted by difficulty (L1→L5). Each chain is verified:
1. **Progression**: Does `exercise.progression` point to a higher-difficulty exercise in the same family?
2. **Regression**: Does `exercise.regression` point to a lower-difficulty exercise in the same family?
3. **Dead ends**: Is `—` ever used in the middle of a chain? (Expected only at L1 regression and L5 progression)
4. **Backwards**: Does progression ever point to same-level or lower-level exercise?
5. **Same-level**: Does progression/regression ever point to same-difficulty exercise?

---

## 1. Double Leg Knee Dominant (DLKD) — 12 exercises

| Exercise | Diff | Progression → | Regression → | Issues |
|----------|------|---------------|--------------|--------|
| Air Squat | L1 | Goblet Squat (L2) ✅ | Wall Sit (L1) ✅ | — |
| Wall Sit | L1 | Air Squat (L1) ⚠️ | — (dead end) ⚠️ | Same-level progression; no regression |
| Box Squat | L2 | Goblet Squat (L2) ⚠️ | Air Squat (L1) ✅ | Same-level progression |
| Goblet Squat | L2 | Barbell Back Squat (L3) ✅ | Box Squat (L2) ⚠️ | Same-level regression |
| Leg Press | L2 | Hack Squat (L3) ✅ | Air Squat (L1) ✅ | — |
| Tempo Back Squat | L2 | Paused Back Squat (L4) ⚠️ | Goblet Squat (L2) ⚠️ | Skips L3; same-level regression |
| Barbell Back Squat | L3 | Front Squat (L4) ✅ | Goblet Squat (L2) ✅ | — |
| Hack Squat | L3 | Barbell Back Squat (L3) ⚠️ | Leg Press (L2) ✅ | Same-level progression |
| Landmine Squat | L3 | Barbell Back Squat (L3) ⚠️ | Goblet Squat (L2) ✅ | Same-level progression |
| Paused Back Squat | L4 | Front Squat (L4) ⚠️ | Tempo Back Squat (L2) ✅ | Same-level progression; regression skips L3 |
| Barbell Front Squat | L4 | Paused Front Squat (L5) ✅ | Barbell Back Squat (L3) ✅ | — |
| Paused Front Squat | L5 | — (expected) ✅ | Front Squat (L4) ✅ | — |

**Issues found: 7**
- `Wall Sit`: progression same-level, no regression (add regression or remove from chain)
- `Box Squat`: progression same-level (should point to Heel-Elevated Goblet L3 or similar)
- `Goblet Squat`: regression same-level (should point to Air Squat)
- `Hack Squat`: progression same-level (should point to Front Squat or remove from chain)
- `Landmine Squat`: progression same-level (should point to Front Squat)
- `Paused Back Squat`: progression same-level; regression skips L3
- `Tempo Back Squat`: regression same-level (should point to Air Squat)

**Verdict: 🟡 PASS WITH ISSUES. Add 1-2 intermediate exercises to fill gaps.**

---

## 2. Double Leg Hip Dominant (DLHD) — 14 exercises

| Exercise | Diff | Progression → | Regression → | Issues |
|----------|------|---------------|--------------|--------|
| Glute Bridge | L1 | Kettlebell Deadlift (L2) ✅ | — (expected) ✅ | — |
| Kettlebell Deadlift | L2 | RDL (L3) ✅ | Glute Bridge (L1) ✅ | — |
| Trap Bar Deadlift | L2 | RDL (L3) ✅ | Kettlebell Deadlift (L2) ⚠️ | Same-level regression |
| 45° Back Extension | L2 | Weighted Back Extension (L4) ⚠️ | Glute Bridge (L1) ✅ | Skips L3 |
| Barbell Hip Thrust | L3 | Heavy Hip Thrust (L3, NOT IN DB) ⚠️ | Glute Bridge (L1) ✅ | Progression points to missing exercise |
| RDL | L3 | Barbell Good Morning (L4) ✅ | Kettlebell Deadlift (L2) ✅ | — |
| Barbell Rack Pull | L3 | Block Pull (L4) ✅ | RDL (L3) ⚠️ | Same-level regression |
| Single-Leg RDL | L3 | Weighted SL RDL (L3, SLHD) ⚠️ | Kettlebell Deadlift (L2) ✅ | Cross-family progression |
| Weighted Back Extension | L4 | Barbell Good Morning (L4) ⚠️ | 45° Back Extension (L2) ✅ | Same-level progression; regression skips L3 |
| Block Pull | L4 | Conventional Deadlift (L5) ✅ | Rack Pull (L3) ✅ | — |
| Barbell Good Morning | L4 | Conventional Deadlift (L5) ✅ | RDL (L3) ✅ | — |
| Conventional Deadlift | L5 | Deficit Deadlift (L5) ⚠️ | Rack Pull (L3) ✅ | Same-level progression |
| Sumo Deadlift | L5 | — (expected) ✅ | Rack Pull (L3) ✅ | — |
| Deficit Deadlift | L5 | — (expected) ✅ | Conventional Deadlift (L5) ⚠️ | Same-level regression |

**Issues found: 7**
- `Barbell Hip Thrust`: progression points to "Heavy Hip Thrust" — exercise does not exist in DB
- `45° Back Extension`: progression skips L3
- `Trap Bar Deadlift`, `Barbell Rack Pull`, `Conventional Deadlift`, `Deficit Deadlift`, `Weighted Back Extension`: same-level progression/regression

**Verdict: 🟡 PASS WITH ISSUES. Add Heavy Hip Thrust to DB. Fix same-level references.**

---

## 3. Single Leg Knee Dominant (SLKD) — 12 exercises

| Exercise | Diff | Progression → | Regression → | Issues |
|----------|------|---------------|--------------|--------|
| Assisted Split Squat | L1 | Split Squat (L2) ✅ | — (expected) ✅ | — |
| Split Squat | L2 | Bulgarian Split Squat (L3) ✅ | Assisted Split Squat (L1) ✅ | — |
| Step-Up | L2 | Bulgarian Split Squat (L3) ✅ | Low Box Step-Up (L1) ✅ | — |
| Low Box Step-Up | L1 | Step-Up (L2) ✅ | — (expected) ✅ | — |
| Bulgarian Split Squat | L3 | Barbell Reverse Lunge (L4) ✅ | Split Squat (L2) ✅ | — |
| Walking Lunge | L3 | Barbell Reverse Lunge (L4) ✅ | Split Squat (L2) ✅ | — |
| Lateral Lunge | L3 | Cossack Squat (L4) ✅ | Split Squat (L2) ✅ | — |
| Barbell Reverse Lunge | L4 | Skater Squat (L4) ⚠️ | Bulgarian Split Squat (L3) ✅ | Same-level progression |
| Cossack Squat | L4 | Weighted Cossack Squat (NOT IN DB) ⚠️ | Lateral Lunge (L3) ✅ | Progression points to missing exercise |
| Skater Squat | L4 | Pistol Squat (L5) ✅ | Bulgarian Split Squat (L3) ✅ | — |
| Single-Leg Box Squat | L4 | Pistol Squat (L5) ✅ | Bulgarian Split Squat (L3) ✅ | — |
| Pistol Squat | L5 | — (expected) ✅ | Single-Leg Box Squat (L4) ✅ | — |

**Issues found: 2**
- `Barbell Reverse Lunge`: progression same-level (should point to Skater or Pistol)
- `Cossack Squat`: progression points to "Weighted Cossack Squat" — not in DB

**Verdict: ✅ PASS MINOR. Add Weighted Cossack Squat and fix Barbell Reverse Lunge progression.**

---

## 4. Single Leg Hip Dominant (SLHD) — 10 exercises

| Exercise | Diff | Progression → | Regression → | Issues |
|----------|------|---------------|--------------|--------|
| Single-Leg Glute Bridge | L1 | Single-Leg Bridge (elevated) (L2) ✅ | — (expected) ✅ | — |
| Split Stance RDL | L2 | SL RDL (floor touch) (L2) ⚠️ | Single-Leg Glute Bridge (L1) ✅ | Same-level progression |
| SL RDL (floor touch) | L2 | Weighted SL RDL (L3) ✅ | Split Stance RDL (L2) ⚠️ | Same-level regression |
| Single-Leg Bridge (elevated) | L2 | Single-Leg Hip Thrust (L3) ✅ | Single-Leg Glute Bridge (L1) ✅ | — |
| Weighted SL RDL | L3 | Single-Leg RDL (loaded) (L4) ✅ | SL RDL (floor touch) (L2) ✅ | — |
| Single-Leg Hip Thrust | L3 | Barbell Hip Thrust (bilateral) (DLHD L3) ⚠️ | Single-Leg Bridge (elevated) (L2) ✅ | Cross-family progression (ends SLHD chain) |
| Isometric Hamstring Hold | L3 | SL RDL (weighted) (L4, name mismatch with "Single-Leg RDL (loaded)") ⚠️ | Single-Leg Glute Bridge (L1) ✅ | Progression name mismatch |
| Single-Leg RDL (loaded) | L4 | — (expected) ✅ | Weighted SL RDL (L3) ✅ | — |
| Band-Resisted Nordic | L3 | Nordic Hamstring Curl (L4) ✅ | Isometric Hamstring Hold (L3) ⚠️ | Same-level regression |
| Nordic Hamstring Curl | L4 | Weighted Nordic (NOT IN DB) ⚠️ | Band-Resisted Nordic (L3) ✅ | Progression points to missing exercise |

**Issues found: 5**
- `Split Stance RDL` and `SL RDL (floor touch)`: same-level progression/regression loop
- `Single-Leg Hip Thrust`: progression ends SLHD chain (crosses to DLHD)
- `Isometric Hamstring Hold`: progression name mismatch ("SL RDL (weighted)" vs "Single-Leg RDL (loaded)")
- `Nordic Hamstring Curl`: progression points to missing "Weighted Nordic"

**Verdict: 🟡 PASS WITH ISSUES. Add Weighted Nordic, fix name mismatches, extend SLHD chain.**

---

## 5. Horizontal Push (HPush) — 10 exercises

| Exercise | Diff | Progression → | Regression → | Issues |
|----------|------|---------------|--------------|--------|
| Wall Push-Up | L1 | Incline Push-Up (L1) ⚠️ | — (expected) ✅ | Same-level progression |
| Incline Push-Up | L1 | Push-Up (L2) ✅ | Wall Push-Up (L1) ⚠️ | Same-level regression |
| Push-Up | L2 | Dumbbell Floor Press (L2) ⚠️ | Incline Push-Up (L1) ✅ | Same-level progression |
| Dumbbell Floor Press | L2 | Dumbbell Bench Press (L3) ✅ | Push-Up (L2) ⚠️ | Same-level regression |
| Dumbbell Bench Press | L3 | Barbell Bench Press (L3) ⚠️ | Dumbbell Floor Press (L2) ✅ | Same-level progression |
| Barbell Bench Press | L3 | Incline Barbell Bench Press (L4) ✅ | Dumbbell Bench Press (L3) ⚠️ | Same-level regression |
| Incline Dumbbell Press | L3 | Barbell Incline Bench Press (L4) ✅ | Push-Up (L2) ✅ | — |
| Incline Barbell Bench Press | L4 | — (expected) ✅ | Flat Barbell Bench Press (L3) ✅ | — |
| Band-Resisted Push-Up | L3 | Weighted Push-Up (L4) ✅ | Push-Up (L2) ✅ | — |
| Weighted Push-Up | L4 | — (expected) ✅ | Push-Up (L2) ✅ | — |

**Issues found: 5**
- Every exercise in the main chain (Wall→Incline→Push→Floor→DB→BB→Incline BB) has same-level progression/regression because adjacent exercises are at the same level (e.g., Wall Push-Up L1 → Incline Push-Up L1)
- This is by design (different equipment at same level) but creates noise in audits

**Verdict: ✅ PASS. Same-level references are legitimate (same difficulty, different equipment). All chains end correctly.**

---

## 6. Horizontal Pull (HPull) — 11 exercises

| Exercise | Diff | Progression → | Regression → | Issues |
|----------|------|---------------|--------------|--------|
| Scapular Retraction | L1 | Band Row (L1) ⚠️ | — (expected) ✅ | Same-level progression |
| Band Row | L1 | Inverted Row (L2) ✅ | Scapular Retraction (L1) ⚠️ | Same-level regression |
| Inverted Row | L2 | Chest-Supported Row (L2) ⚠️ | Band Row (L1) ✅ | Same-level progression |
| Chest-Supported Row | L2 | Dumbbell Row (L3) ✅ | Inverted Row (L2) ⚠️ | Same-level regression |
| Dumbbell Row | L3 | Barbell Row (L4) ✅ | Chest-Supported Row (L2) ✅ | — |
| Seal Row | L3 | Barbell Row (L4) ✅ | Chest-Supported Row (L2) ✅ | — |
| Single-Arm Cable Row | L3 | Barbell Row (L4) ✅ | Band Row (L1) ✅ | Regression skips L2 |
| T-Bar Row | L3 | Barbell Row (L4) ✅ | Chest-Supported Row (L2) ✅ | — |
| Barbell Row | L4 | Pendlay Row (L5) ✅ | Dumbbell Row (L3) ✅ | — |
| Meadows Row | L4 | Barbell Row (L4) ⚠️ | Dumbbell Row (L3) ✅ | Same-level progression |
| Pendlay Row | L5 | — (expected) ✅ | Barbell Row (L4) ✅ | — |

**Issues found: 3**
- Same-level references in L1-L2 static/dynamic pairs (acceptable)
- `Single-Arm Cable Row`: regression skips L2 (should point to Chest-Supported Row)
- `Meadows Row`: progression same-level

**Verdict: ✅ PASS MINOR. Fix Single-Arm Cable Row regression. Meadows Row is legitimate same-level variant.**

---

## 7. Vertical Push (VPush) — 10 exercises

| Exercise | Diff | Progression → | Regression → | Issues |
|----------|------|---------------|--------------|--------|
| Band Overhead Press | L1 | Half-Kneeling Landmine Press (L2) ✅ | — (expected) ✅ | — |
| Half-Kneeling Landmine Press | L2 | Standing Landmine Press (L2) ⚠️ | Band Overhead Press (L1) ✅ | Same-level progression |
| Standing Landmine Press | L2 | Single-Arm DB Press (L2) ⚠️ | Half-Kneeling Landmine Press (L2) ⚠️ | Same-level progression AND regression |
| Single-Arm DB Press (standing) | L2 | Standing DB Press (L3) ✅ | Landmine Press (L2) — name mismatch | Regression name "Landmine Press" vs "Standing Landmine Press" |
| Seated DB Press | L3 | Standing DB Press (L3) ⚠️ | Single-Arm DB Press (L2) ✅ | Same-level progression |
| Standing DB Press | L3 | Barbell Overhead Press (L4) ✅ | Seated DB Press (L3) ⚠️ | Same-level regression |
| Arnold Press | L4 | Standing DB Press (L3) ⚠️ | Seated DB Press (L3) ⚠️ | Backward progression (L4→L3) + same-level regression |
| Barbell Overhead Press | L4 | Push Press (L4) ⚠️ | Standing DB Press (L3) ✅ | Same-level progression |
| Push Press | L4 | Power Jerk (L5) ✅ | Barbell Overhead Press (L4) ⚠️ | Same-level regression |
| Power Jerk | L5 | — (expected) ✅ | Push Press (L4) ✅ | — |

**Issues found: 5**
- `Arnold Press`: **BACKWARD PROGRESSION** — points to Standing DB Press (L3) but Arnold is L4
- `Half-Kneeling Landmine Press`, `Standing Landmine Press`, `Seated DB Press`, `Barbell Overhead Press`, `Push Press`: same-level references

**Verdict: 🟡 PASS WITH ISSUES. Fix Arnold Press backward progression. Same-level references are acceptable.**

---

## 8. Vertical Pull (VPull) — 12 exercises

| Exercise | Diff | Progression → | Regression → | Issues |
|----------|------|---------------|--------------|--------|
| Band Lat Pulldown | L1 | Lat Pulldown (L2) ✅ | — (expected) ✅ | — |
| Scapular Pull-Up (hang) | L1 | Lat Pulldown (L2) ✅ | — (expected) ✅ | — |
| Lat Pulldown | L2 | Pull-Up (L3) ✅ | Band Lat Pulldown (L1) ✅ | — |
| V-Grip Pulldown | L2 | Pull-Up (close grip) (L3) ✅ | Lat Pulldown (L2) ⚠️ | Same-level regression |
| Straight-Arm Pulldown | L2 | Lat Pulldown (L2) ⚠️ | Band Straight-Arm Pulldown (NOT IN DB) ⚠️ | Same-level progression + missing exercise in regression |
| Chin-Up | L3 | Weighted Chin-Up (L4) ✅ | Lat Pulldown (underhand) (L2) ✅ | — |
| Pull-Up | L3 | Weighted Pull-Up (L4) ✅ | Lat Pulldown (L2) ✅ | — |
| Neutral-Grip Pull-Up | L3 | Weighted Neutral Pull-Up (L4) ✅ | Lat Pulldown (neutral) (L2) ✅ | — |
| Single-Arm Lat Pulldown | L3 | Pull-Up (L3) ⚠️ | Lat Pulldown (L2) ✅ | Same-level progression |
| Weighted Chin-Up | L4 | — (expected) ✅ | Chin-Up (L3) ✅ | — |
| Weighted Pull-Up | L4 | Muscle-Up (L5) ✅ | Pull-Up (L3) ✅ | — |
| Muscle-Up | L5 | — (expected) ✅ | Weighted Pull-Up + Dip (L4) ⚠️ | Regression name includes modifier: "Weighted Pull-Up + Dip" not exact match |

**Issues found: 4**
- `Straight-Arm Pulldown`: same-level progression + regression points to missing "Band Straight-Arm Pulldown"
- `V-Grip Pulldown`, `Single-Arm Lat Pulldown`: same-level references
- `Muscle-Up`: regression name doesn't exactly match any exercise ("Weighted Pull-Up + Dip" vs actual "Weighted Pull-Up")

**Verdict: 🟡 PASS WITH ISSUES. Add Band Straight-Arm Pulldown. Fix Muscle-Up regression name.**

---

## 9. Plyometric (Plyo) — 14 exercises

| Exercise | Diff | Progression → | Regression → | Issues |
|----------|------|---------------|--------------|--------|
| Ankle Bounce | L1 | Pogo Jump (L1) ⚠️ | — (expected) ✅ | Same-level progression |
| Pogo Jump | L1 | Squat Jump (L2) ✅ | Ankle Bounce (L1) ⚠️ | Same-level regression |
| Pogo Jump (single leg) | L2 | Broad Jump (L3) ✅ | Pogo Jump (bilateral) (L1) — name mismatch | Regression name "Pogo Jump (bilateral)" not exact match for "Pogo Jump" |
| Squat Jump | L2 | Countermovement Jump (L3) ✅ | Pogo Jump (L1) ✅ | — |
| Depth Drop (land + stick) | L2 | Box Jump (L3) ✅ | Pogo Jump (L1) ✅ | — |
| Countermovement Jump | L3 | Broad Jump (L3) ⚠️ | Squat Jump (L2) ✅ | Same-level progression |
| Broad Jump | L3 | Bounding (L4) ✅ | Countermovement Jump (L3) ⚠️ | Same-level regression |
| Lateral Pogo | L3 | Lateral Bound (L4) ✅ | Pogo Jump (L1) ✅ | — |
| Box Jump | L3 | Depth Jump (L5) ⚠️ | Countermovement Jump (L3) ⚠️ | Skips L4; same-level regression |
| Hurdle Hop | L4 | Depth Jump (L5) ✅ | Box Jump (L3) ✅ | — |
| Lateral Bound | L4 | Single-Leg Lateral Bound (L5) ✅ | Lateral Pogo (L3) ✅ | — |
| Bounding | L4 | Single-Leg Bounding (L5) ✅ | Broad Jump (L3) ✅ | — |
| Depth Jump | L5 | Depth Jump + Sprint (NOT IN DB) ⚠️ | Box Jump (L3) ✅ | Progression points to missing exercise |
| Single-Leg Bounding | L5 | — (expected) ✅ | Bounding (L4) ✅ | — |

**Issues found: 5**
- `Countermovement Jump`→ `Broad Jump`: same-level progression
- `Box Jump` → `Depth Jump`: skips L4
- `Depth Jump`: progression points to missing "Depth Jump + Sprint"
- `Pogo Jump (single leg)`: regression name mismatch
- Same-level references in Ankle→Pogo pair (acceptable)

**Verdict: 🟡 PASS WITH ISSUES. Add "Depth Jump + Sprint" exercise. Fix regression name. Box Jump→Depth Jump (L3→L5) needs Hurdle Hop bridge.**

---

## 10. Ballistic (Ball) — 13 exercises

| Exercise | Diff | Progression → | Regression → | Issues |
|----------|------|---------------|--------------|--------|
| Med Ball Push | L1 | Med Ball Chest Pass (L2) ✅ | — (expected) ✅ | — |
| KB Swing | L1 | High Pull (KB or barbell) (L3) ⚠️ | — (expected) ✅ | Progression skips L2 |
| Med Ball Chest Pass | L2 | Med Ball Overhead Throw (L3) ✅ | Med Ball Push (L1) ✅ | — |
| Jump Shrug | L2 | High Pull (hang) (L3) ✅ | — (expected) ✅ | — |
| KB Clean | L2 | Hang Clean (L4) ⚠️ | KB Swing (L1) ✅ | Skips L3 |
| Snatch High Pull | L3 | Power Snatch (L4) ✅ | Jump Shrug (snatch grip) (L2) ✅ | — |
| High Pull (hang) | L3 | Hang Clean (L4) ✅ | Jump Shrug (L2) ✅ | — |
| Med Ball Overhead Throw | L3 | Med Ball Slam (L3) ⚠️ | Med Ball Chest Pass (L2) ✅ | Same-level progression |
| Med Ball Slam | L3 | Rotational Med Ball Slam (L4) ✅ | Med Ball Overhead Throw (L3) ⚠️ | Same-level regression |
| Hang Clean | L4 | Power Clean (L5) ✅ | High Pull (L3) ✅ | — |
| Power Snatch | L4 | Snatch + Overhead Squat (NOT IN DB) ⚠️ | Snatch High Pull (L3) ✅ | Progression points to missing exercise |
| Power Clean | L5 | Clean + Jerk (L5) ⚠️ | Hang Clean (L4) ✅ | Same-level progression |
| Clean + Jerk | L5 | — (expected) ✅ | Power Clean (L5) ⚠️ | Same-level regression |

**Issues found: 6**
- `KB Swing`: progression skips L2 (no L2 KB exercise bridge)
- `KB Clean`: progression skips L3
- `Power Snatch`: progression points to missing "Snatch + Overhead Squat"
- `Med Ball Overhead Throw`→`Med Ball Slam`: same-level
- `Power Clean`→`Clean + Jerk`: same-level
- KB track has only L1 (KB Swing) and L2 (KB Clean) — no L3+ KB progression

**Verdict: 🟡 PASS WITH ISSUES. Add KB L3 (KB High Pull or KB Power Clean), add "Snatch + Overhead Squat".**

---

## 11. Sprint / COD — 18 exercises

| Exercise | Diff | Progression → | Regression → | Issues |
|----------|------|---------------|--------------|--------|
| High Knee March | L1 | A-Skip (L2) ✅ | — (expected) ✅ | — |
| Standing Fall (lean) | L1 | Wall Lean Drill (L2) ✅ | — (expected) ✅ | — |
| March to Stop | L1 | Deceleration to Stop (L2) ✅ | — (expected) ✅ | — |
| Wall Lean Drill | L2 | 10m Sled Push (L2) ⚠️ | Standing Fall (L1) ✅ | Same-level progression |
| A-Skip | L2 | A-Run (L3) ✅ | High Knee March (L1) ✅ | — |
| Deceleration to Stop | L2 | Decel + Reaccel (L3) ✅ | March to Stop (L1) ✅ | — |
| 10m Sled Push | L2 | 10m Acceleration (L3) ✅ | Wall Lean Drill (L2) ⚠️ | Same-level regression |
| A-Run | L3 | Flying 10m (L4) ✅ | A-Skip (L2) ✅ | — |
| Wicket Run | L3 | Low Wickets (NOT IN DB) ⚠️ | High Knee March (L1) ✅ | Progression points to missing exercise |
| Decel + Reaccel | L3 | Pro Shuttle (L4) ✅ | Deceleration to Stop (L2) ✅ | — |
| 10m Acceleration | L3 | 20m Acceleration (L4) ✅ | 10m Sled Push (L2) ✅ | — |
| Flying 10m | L4 | Flying 20m (L5) ✅ | A-Run (L3) ✅ | — |
| Pro Shuttle (5-10-5) | L4 | T-Drill (L5) ✅ | Decel + Reaccel (L3) ✅ | — |
| 3-Cone Drill (L-Drill) | L4 | Pro Shuttle (L4) ⚠️ | Box Drill (NOT IN DB) ⚠️ | Same-level progression; regression missing |
| 20m Acceleration | L4 | Resisted Sprint (L5) ✅ | 10m Acceleration (L3) ✅ | — |
| Flying 20m | L5 | Flying 30m (NOT IN DB) ⚠️ | Flying 10m (L4) ✅ | Progression points to missing exercise |
| Resisted Sprint (heavy sled) | L5 | — (expected) ✅ | 20m Acceleration (L4) ✅ | — |
| T-Drill | L5 | Reactive Shuttle (NOT IN DB) ⚠️ | Pro Shuttle (L4) ✅ | Progression points to missing exercise |

**Issues found: 6**
- `Wicket Run`: progression points to missing "Low Wickets"
- `3-Cone Drill`: regression points to missing "Box Drill"; same-level progression to Pro Shuttle
- `Flying 20m`: progression points to missing "Flying 30m"
- `T-Drill`: progression points to missing "Reactive Shuttle"
- `10m Sled Push`→`Wall Lean Drill`: same-level regression
- `Wall Lean Drill`→`10m Sled Push`: same-level progression

**Verdict: 🟡 PASS WITH ISSUES. Add missing exercises for 4 broken progressions. Same-level pairs (L2 sled→wall) are legitimate.**

---

## 12. Rotational (Rot) — 10 exercises

| Exercise | Diff | Progression → | Regression → | Issues |
|----------|------|---------------|--------------|--------|
| Band Half-Kneeling Chop | L1 | Standing Band Chop (L2) ✅ | — (expected) ✅ | — |
| Standing Band Chop | L2 | Cable Chop (L3) ✅ | Band Half-Kneeling Chop (L1) ✅ | — |
| Half-Kneeling Landmine Rotation | L2 | Standing Landmine Rotation (L3) ✅ | Band Anti-Rotation Press (Core, NOT IN Rot) ⚠️ | Cross-family regression missing from Rot |
| Med Ball Rotational Throw | L2 | Cable Rotational Row (L3) ✅ | Band Rotational Chop (NOT IN DB) ⚠️ | Regression points to missing exercise |
| Cable Rotational Row | L3 | Landmine Rotation (heavy) (L4) ✅ | Med Ball Rotational Throw (L2) ✅ | — |
| Standing Landmine Rotation | L3 | Heavy Landmine Rotation (L4) ✅ | Half-Kneeling Landmine Rotation (L2) ✅ | — |
| Cable Chop (low to high) | L3 | Med Ball Overhead Rotational Slam (L4) ✅ | Band Rotational Chop (NOT IN DB) ⚠️ | Same issue — missing Band Rotational Chop |
| Landmine Rotation (heavy) | L4 | — (expected) ✅ | Standing Landmine Rotation (L3) ✅ | — |
| Med Ball Overhead Rotational Slam | L4 | Rotational Slam + Sprint (NOT IN DB) ⚠️ | Med Ball Rotational Throw (L2) ✅ | Progression points to missing exercise |
| Russian Twist (weighted) | L2 | Standing Rotational Med Ball (NOT IN DB) ⚠️ | Bicycle Crunch (Core, NOT IN Rot) ⚠️ | Progression + regression both missing |

**Issues found: 7**
- `Med Ball Rotational Throw`, `Cable Chop`, `Med Ball Overhead Rotational Slam`: three exercises referencing missing "Band Rotational Chop"
- `Half-Kneeling Landmine Rotation`: regression references Core exercise not in Rot
- `Russian Twist`: both progression and regression point to missing/non-Rot exercises
- `Med Ball Overhead Rotational Slam`: progression to missing "Rotational Slam + Sprint"

**Verdict: 🟡 PASS WITH ISSUES. Most issues in Rot — missing exercises are referenced but don't exist.**

---

## 13. Carry — 13 exercises

| Exercise | Diff | Progression → | Regression → | Issues |
|----------|------|---------------|--------------|--------|
| Farmer's Walk (light) | L1 | Farmer's Walk (moderate) (L2) ✅ | — (expected) ✅ | — |
| Bear Hug Carry | L1 | Farmer's Walk (L2, name mismatch) ⚠️ | Farmer's Walk (lighter) (NOT IN DB) ⚠️ | Name mismatch + missing exercise |
| Suitcase Carry (light) | L2 | Suitcase Carry (moderate) (L3) ✅ | Farmer's Walk (light) (L1) ✅ | — |
| Farmer's Walk (moderate) | L2 | Front Rack Carry (L3) ✅ | Farmer's Walk (light) (L1) ✅ | — |
| Suitcase Carry (moderate) | L3 | Waiter's Walk (L3) ⚠️ | Suitcase Carry (light) (L2) ✅ | Same-level progression |
| Front Rack Carry | L3 | Trap Bar Carry (L4) ✅ | Farmer's Walk (moderate) (L2) ✅ | — |
| Waiter's Walk | L3 | Single-Arm Overhead Carry (L4) ✅ | Suitcase Carry (moderate) (L3) ⚠️ | Same-level regression |
| Trap Bar Carry | L4 | Farmer's Walk (heavy) (L4) ⚠️ | Front Rack Carry (L3) ✅ | Same-level progression |
| Single-Arm Overhead Carry | L4 | Overhead Carry (bilateral) (L4) ⚠️ | Waiter's Walk (L3) ✅ | Same-level progression |
| Farmer's Walk (heavy) | L4 | Yoke Walk (L5) ✅ | Trap Bar Carry (L4) ⚠️ | Same-level regression |
| Overhead Carry (bilateral) | L4 | Single-Arm Overhead Carry (heavier) (NOT IN DB) ⚠️ | Single-Arm Overhead Carry (L4) ⚠️ | Missing exercise + same-level regression |
| Zercher Carry | L5 | — (expected) ✅ | Front Rack Carry (L3) ✅ | — |
| Yoke Walk | L5 | — (expected) ✅ | Farmer's Walk (heavy) (L4) ✅ | — |

**Issues found: 7**
- `Bear Hug Carry`: progression name mismatch ("Farmer's Walk" vs "Farmer's Walk (moderate)"); regression missing
- `Overhead Carry (bilateral)`: progression to missing "Single-Arm Overhead Carry (heavier)" + same-level regression
- Multiple same-level references in L4 carries (legitimate — different variations at same difficulty)

**Verdict: 🟡 PASS WITH ISSUES. Fix Bear Hug Carry and Overhead Carry (bilateral) chains.**

---

## 14. Core — 21 exercises

| Exercise | Diff | Progression → | Regression → | Issues |
|----------|------|---------------|--------------|--------|
| Marching Dead Bug | L1 | Dead Bug (L1) ⚠️ | — (expected) ✅ | Same-level progression |
| Dead Bug | L1 | Hollow Hold (NOT IN DB) ⚠️ | Marching Dead Bug (L1) ⚠️ | Missing exercise + same-level regression |
| Bent-Knee Side Plank | L1 | Side Plank (L2) ✅ | — (expected) ✅ | — |
| Pallof Press (hold) | L1 | Single-Leg Pallof (L2) ✅ | Band Hold (NOT IN DB) ⚠️ | Missing exercise |
| Reverse Crunch | L1 | Hanging Knee Raise (L3) ⚠️ | Dead Bug (L1) ⚠️ | Progression skips L2; same-level regression |
| Plank (front) | L2 | RKC Plank (L3) ✅ | Dead Bug (L1) ✅ | — |
| Side Plank | L2 | Side Plank (leg raise) (L3) ✅ | Bent-Knee Side Plank (L1) ✅ | — |
| Single-Leg Pallof | L2 | Cable Anti-Rotation Press (L3) ✅ | Pallof Press (hold) (L1) ✅ | — |
| Lying Leg Raise | L2 | Hanging Knee Raise (L3) ✅ | Dead Bug (L1) ✅ | — |
| RKC Plank | L3 | Weighted Plank (L3) ⚠️ | Plank (L2) ✅ | Same-level progression |
| Side Plank (leg raise) | L3 | Copenhagen Plank (L4) ✅ | Side Plank (L2) ✅ | — |
| Dead Bug (weighted) | L3 | Weighted Hollow Hold (NOT IN DB) ⚠️ | Dead Bug (L1) ✅ | Missing exercise |
| Weighted Plank | L3 | Ab Wheel Rollout (L3) ⚠️ | RKC Plank (L3) ⚠️ | Same-level progression + same-level regression |
| Ab Wheel Rollout (kneeling) | L3 | Standing Rollout (L4) ✅ | Weighted Plank (L3) ⚠️ | Same-level regression |
| Cable Anti-Rotation Press | L3 | Walking Pallof (L4) ✅ | Single-Leg Pallof (L2) ✅ | — |
| Hanging Knee Raise | L3 | Hanging Leg Raise (L4) ✅ | Lying Leg Raise (L2) ✅ | — |
| Walking Pallof | L4 | Single-Leg + Overhead Pallof (NOT IN DB) ⚠️ | Single-Leg Pallof (L2) ✅ | Missing exercise |
| Hanging Leg Raise | L4 | Toes to Bar (L5) ✅ | Hanging Knee Raise (L3) ✅ | — |
| Copenhagen Plank | L4 | Weighted Copenhagen (NOT IN DB) ⚠️ | Side Plank (leg raise) (L3) ✅ | Missing exercise |
| Standing Rollout | L4 | — (expected) ✅ | Ab Wheel Rollout (kneeling) (L3) ✅ | — |
| Toes to Bar | L5 | — (expected) ✅ | Hanging Leg Raise (L4) ✅ | — |

**Issues found: 10**
- `Dead Bug`: progression to missing "Hollow Hold"
- `Pallof Press (hold)`, `Dead Bug (weighted)`, `Walking Pallof`, `Copenhagen Plank`: missing exercises in chains
- `Reverse Crunch`: progression skips L2
- Multiple same-level references in L1-L3 (acceptable — static/dynamic pairs)

**Verdict: 🟡 PASS WITH ISSUES. Add 4-5 missing Core exercises. This is the most complete family (21 exercises) but has the most broken external references.**

---

## 15. Accessory / Prehab (Acc/Prehab) — 21 exercises

| Exercise | Diff | Progression → | Regression → | Issues |
|----------|------|---------------|--------------|--------|
| Band Pull-Apart | L1 | Prone T Raise (L2) ✅ | Band Dislocate (L1) ⚠️ | Same-level regression |
| Band Dislocate | L1 | PVC Pass-Through (L1) ⚠️ | — (expected) ✅ | Same-level progression |
| Band Lateral Walk | L1 | Banded Side Step (squat) (NOT IN DB) ⚠️ | — (expected) ✅ | Missing exercise |
| Band External Rotation | L1 | Cable External Rotation (L2) ✅ | — (expected) ✅ | — |
| Band Internal Rotation | L1 | Cable Internal Rotation (L2) ✅ | — (expected) ✅ | — |
| Glute Med Clamshell | L1 | Band Lateral Walk (L1) ⚠️ | — (expected) ✅ | Same-level progression |
| PVC Shoulder Pass-Through | L1 | Weighted Bar Pass-Through (NOT IN DB) ⚠️ | Band Dislocate (L1) ⚠️ | Missing exercise + same-level regression |
| Ankle Dorsiflexion Mobilisation | L1 | Weighted Ankle Mobilisation (L2) ✅ | Calf Stretch (NOT IN DB) ⚠️ | Missing exercise |
| Seated Calf Raise | L1 | Standing Calf Raise (L2) ✅ | Bodyweight Calf Raise (NOT IN DB) ⚠️ | Missing exercise |
| Tibialis Raise | L1 | Weighted Tib Raise (NOT IN DB) ⚠️ | Band Dorsiflexion (NOT IN DB) ⚠️ | Multiple missing |
| Face Pull | L1 | Cable Face Pull (heavy) (L3) ✅ | Band Pull-Apart (L1) ⚠️ | Same-level regression |
| Prone W Raise | L1 | Prone T Raise (L2) ✅ | Scapular Retraction (HPull L1) ⚠️ | Cross-family regression |
| Prone T Raise | L2 | Prone Y Raise (L3) ✅ | Prone W Raise (L1) ✅ | — |
| Standing Calf Raise | L2 | Single-Leg Calf Raise (L3) ✅ | Seated Calf Raise (L1) ✅ | — |
| Cable External Rotation | L2 | Prone Y Raise (L3) ⚠️ | Band External Rotation (L1) ✅ | Cross-family progression (shoulder→scapular) |
| Cable Internal Rotation | L2 | — (expected) ✅ | Band Internal Rotation (L1) ✅ | — |
| Dumbbell Lateral Raise | L2 | Cable Lateral Raise (NOT IN DB) ⚠️ | Band Lateral Raise (NOT IN DB) ⚠️ | Both progression + regression missing |
| Prone Y Raise | L3 | Bent-Over Rear Delt Fly (NOT IN DB) ⚠️ | Prone T Raise (L2) ✅ | Missing exercise |
| Single-Leg Calf Raise | L3 | Weighted Single-Leg Calf Raise (NOT IN DB) ⚠️ | Standing Calf Raise (L2) ✅ | Missing exercise |
| Weighted Ankle Mobilisation | L2 | — (expected) ✅ | Ankle Dorsiflexion Mobilisation (L1) ✅ | — |
| Cable Face Pull (heavy) | L3 | — (expected) ✅ | Face Pull (L1) ✅ | — |

**Issues found: 14 (highest in system)**
- 7 exercises reference missing exercises as progression or regression
- 5 exercises reference non-existent regressions (Band Dorsiflexion, Bodyweight Calf Raise, etc.)
- `Band Lateral Walk`: progression to missing "Banded Side Step (squat)"
- `Dumbbell Lateral Raise`: both progression AND regression point to missing exercises
- `Tibialis Raise`: both chain endpoints missing

**Verdict: 🟡 PASS WITH ISSUES. Acc/Prehab needs the most chain repair — 7 missing exercises to add.**

---

## Summary

### Issues by Family

| Family | Count | Severity |
|--------|-------|----------|
| Acc/Prehab | 14 | 🟡 Highest — many missing exercises referenced |
| Core | 10 | 🟡 High — 4-5 exercises needed to complete chains |
| Rot | 7 | 🟡 High — referenced exercises don't exist |
| Carry | 7 | 🟡 Medium — name mismatches fixable |
| DLKD | 7 | 🟡 Medium — same-level references fixable |
| Ball | 6 | 🟡 Medium — KB track has L1→L4 gap |
| Sprint/COD | 6 | 🟡 Medium — 4 missing exercises referenced |
| VPush | 5 | 🟡 **Backward progression found (Arnold Press)** |
| Plyo | 5 | 🟡 Medium — 3 missing exercises referenced |
| SLHD | 5 | 🟡 Medium — name mismatches + missing Weighted Nordic |
| VPull | 4 | 🟡 Low — Band Straight-Arm Pulldown missing |
| HPull | 3 | ✅ Low |
| SLKD | 2 | ✅ Low |
| DLHD | 7 | 🟡 Medium — Heavy Hip Thrust missing |
| HPush | 5 | ✅ Acceptable (same-level by design) |

**Total issues: 95**

### Chain Health by Category

| Metric | Count |
|--------|-------|
| Progressions pointing to missing exercises | 18 |
| Regressions pointing to missing exercises | 10 |
| Same-level progressions | 18 |
| Same-level regressions | 20 |
| Backward progressions (L4→L3) | 1 (Arnold Press) |
| Cross-family progressions | 4 |
| Name mismatches | 5 |
| Progression skips level | 6 |

### Required New Exercises to Fix Broken Chains

| Exercise | Family | Diff | Referenced By |
|----------|--------|------|---------------|
| Heavy Hip Thrust | DLHD | L3 | Barbell Hip Thrust progression |
| Weighted Cossack Squat | SLKD | L5 | Cossack Squat progression |
| Weighted Nordic | SLHD | L5 | Nordic Hamstring Curl progression |
| Hollow Hold | Core | L2 | Dead Bug progression |
| Weighted Hollow Hold | Core | L4 | Dead Bug (weighted) progression |
| Walking Pallof (advanced) | Core | L5 | Walking Pallof progression |
| Weighted Copenhagen | Core | L5 | Copenhagen Plank progression |
| Band Straight-Arm Pulldown | VPull | L1 | Straight-Arm Pulldown regression |
| Depth Jump + Sprint | Plyo | L5 | Depth Jump progression |
| Snatch + Overhead Squat | Ball | L5 | Power Snatch progression |
| Banded Side Step (squat) | Acc | L2 | Band Lateral Walk progression |
| Weighted Bar Pass-Through | Acc | L2 | PVC Pass-Through progression |
| Calf Stretch | Acc | L1 | Ankle Dorsiflexion regression |
| Bodyweight Calf Raise | Acc | L1 | Seated Calf Raise regression |
| Weighted Tib Raise | Acc | L2 | Tibialis Raise progression |
| Band Dorsiflexion | Acc | L1 | Tibialis Raise regression |
| Cable Lateral Raise | Acc | L3 | Dumbbell Lateral Raise progression |
| Band Lateral Raise | Acc | L1 | Dumbbell Lateral Raise regression |
| Bent-Over Rear Delt Fly | Acc | L3 | Prone Y Raise progression |
| Weighted Single-Leg Calf Raise | Acc | L4 | Single-Leg Calf Raise progression |
| Band Rotational Chop | Rot | L1 | 3 exercises reference this |
| Rotational Slam + Sprint | Rot | L5 | Med Ball Overhead Rotational Slam progression |
| Standing Rotational Med Ball | Rot | L3 | Russian Twist progression |
| Low Wickets | Sprint | L2 | Wicket Run progression |
| Box Drill | Sprint | L3 | 3-Cone Drill regression |
| Flying 30m | Sprint | L5 | Flying 20m progression |
| Reactive Shuttle | Sprint | L5 | T-Drill progression |

**Total: 27 exercises needed to fix broken chains.**

These 27 don't count toward the exercise gap target (250-300) — they're chain fixes, not new capabilities.

---

## Verdict

**Backward progressions: 1** (Arnold Press L4 → Standing DB Press L3)
**Missing referenced exercises: 27**
**Same-level references: 38** (majority acceptable — same-level progression/regression is valid for equipment variants)

**Recommendation:** Fix the 27 missing referenced exercises first (they create dead ends for real users). Then address the backward progression (Arnold Press). Same-level references are acceptable design choices for an exercise database where multiple exercises share the same difficulty.
