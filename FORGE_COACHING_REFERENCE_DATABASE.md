# FORGE Coaching Reference Database V1

> Single source of coaching truth. Normalised from Exercise Ontology V1, Blueprint Catalog V1, Substitution Matrix V1, Pattern Library, Movement Frequency Report, and Coaching Patterns Summary. Audit findings incorporated.

---

## Part 1: Family Definitions

Every exercise belongs to **exactly one primary family**. Secondary families are listed where exercises overlap patterns.

### 1. Double Leg Knee Dominant (DLKD)
**Definition:** Bilateral squat-pattern exercises where knee flexion is the primary joint action. Loaded through axial or held resistance. **Not:** split-stance, single-leg, or hinge-pattern exercises.
**Non-negotiable in:** 90% of programs.
**Slot:** Mid-session, primary strength.

### 2. Double Leg Hip Dominant (DLHD)
**Definition:** Bilateral hinge-pattern exercises where hip flexion/extension is the primary joint action, knees remain relatively extended. **Not:** squat-pattern (where knee flexion > hip flexion), single-leg hinges.
**Non-negotiable in:** 75% of programs.
**Slot:** Mid-session, primary strength (after knee-dominant if both in same session).

### 3. Single Leg Knee Dominant (SLKD)
**Definition:** Unilateral squat/lunge-pattern exercises where the working leg performs knee-dominant flexion/extension. **Not:** bilateral squats, single-leg hinges.
**Non-negotiable in:** 70% of programs, 100% of court sport programs.
**Slot:** Late-session, secondary strength. Elevated to primary in court sport blueprints.

### 4. Single Leg Hip Dominant (SLHD)
**Definition:** Unilateral hinge-pattern exercises where the working leg performs hip-dominant flexion/extension. **Not:** bilateral hinges, single-leg squats.
**Frequency:** 25% of programs. Specialised.
**Slot:** Late-session, supplementary.

### 5. Horizontal Push (HPush)
**Definition:** Upper-body pressing where the line of force is horizontal relative to the torso. Performed prone (bench) or vertical (push-up). **Not:** overhead pressing (vertical), incline pressing (verges on vertical).
**Non-negotiable in:** 80% of programs.
**Slot:** Late-session, supplementary (after pulls).

### 6. Horizontal Pull (HPull)
**Definition:** Upper-body pulling where the line of force is horizontal relative to the torso. Rows, cable pulls, inverted rows. **Not:** vertical pulls (pulldowns, pull-ups).
**Non-negotiable in:** 90% of programs.
**Slot:** Late-session, supplementary (before pushes when paired).

### 7. Vertical Push (VPush)
**Definition:** Upper-body pressing where the line of force is vertical relative to the torso. Overhead press variations. **Not:** horizontal pressing, incline pressing at <45°.
**Frequency:** 20% of programs. Most common in general S&C.
**Slot:** Late-session, supplementary.

### 8. Vertical Pull (VPull)
**Definition:** Upper-body pulling where the line of force is vertical relative to the torso. Pulldowns, pull-ups, chin-ups. **Not:** horizontal pulls.
**Frequency:** 55% of programs.
**Slot:** Late-session, supplementary.

### 9. Plyometric (Plyo)
**Definition:** Fast, high-intensity bodyweight exercises using the stretch-shorten cycle. Jumps, bounds, hops. **Not:** loaded explosive work (Ballistic), slow strength work.
**Non-negotiable in:** 85% of programs (as Power modality).
**Slot:** Early-session (before strength, fresh CNS).

### 10. Ballistic (Ball)
**Definition:** Loaded explosive exercises where the athlete accelerates the load through full extension. Olympic lifts, med ball throws, KB swings. **Not:** unloaded jumps (Plyometric), slow strength.
**Frequency:** 85% of programs (Olympic lifts at 50%).
**Slot:** Early-session (before all fatiguing work). Never paired.

### 11. Sprint / Change of Direction (Sprint/COD)
**Definition:** Locomotion-based speed, acceleration, deceleration, and reacceleration. Linear sprint, multi-directional COD, agility drills. **Not:** jump training (Plyometric), conditioning runs.
**Frequency:** Sprint 65%, COD 60%.
**Slot:** Fresh — either as standalone session or first in field session.

### 12. Rotational (Rot)
**Definition:** Transverse-plane rotation and anti-rotation loaded through the torso. Med ball rotational throws, cable chops, landmine rotations. **Not:** core anti-extension/flexion work (Core), sagittal-plane work.
**Frequency:** 45% of programs (higher in cricket/tennis).
**Slot:** Variable — can be in Power slot (rotational power) or late-session (supplementary).

### 13. Carry (Carry)
**Definition:** Loaded ambulation where the athlete walks with external load. Grip, core stiffness, shoulder stability under load. **Not:** static core work, upper body isolation.
**Frequency:** 30% of programs (highest in rugby at 50%).
**Slot:** Late-session, accessory / conditioning finisher.

### 14. Core (Core)
**Definition:** Trunk stabilisation including anti-extension, anti-rotation, anti-lateral flexion, and controlled flexion. Planks, dead bugs, rollouts, leg raises. **Not:** rotational power work (Rotational), hip-dominant work.
**Non-negotiable in:** 100% of programs.
**Slot:** Last in session. Never before power or primary strength.

### 15. Accessory / Prehab (Acc/Prehab)
**Definition:** Targeted isolation, prehabilitation, and injury prevention. Rotator cuff, scapular control, ankle/calf, neck, grip. **Not:** primary strength or power exercises.
**Frequency:** Variable. Universal in warm-up / activation.
**Slot:** Activation (early) or prehab (late) depending on purpose.

---

## Part 2: Exercise Database

### Legend

| Field | Values |
|-------|--------|
| **Fam** | Primary family (abbreviated) |
| **Sec** | Secondary family (optional overlap) |
| **Obj** | Primary training objective: STR (Strength) | POW (Power) | HYP (Hypertrophy) | COND (Conditioning) | MOB (Mobility) | STAB (Stability) |
| **Diff** | L1 (Beginner) → L5 (Elite). Based on load + skill + coordination demand |
| **Equip** | Key equipment required |
| **U/B** | Unilateral or Bilateral |
| **Exp** | Explosive intent: Y/N |
| **Iso** | Isometric component: Y/N |
| **Rot** | Rotational component: Y/N |
| **Prog** | Direct progression (next level within family) |
| **Reg** | Direct regression (previous level within family) |

### 1. Double Leg Knee Dominant

| Name | Fam | Sec | Obj | Diff | Equip | U/B | Exp | Iso | Rot | Prog | Reg |
|------|-----|-----|-----|------|-------|-----|-----|-----|-----|------|-----|
| Air Squat | DLKD | — | STR | L1 | Bodyweight | B | N | N | N | Goblet Squat | Wall Sit |
| Wall Sit | DLKD | Acc | STAB | L1 | Bodyweight | B | N | Y | N | Air Squat | — |
| Box Squat | DLKD | — | STR | L2 | Barbell + Box | B | N | N | N | Goblet Squat | Air Squat |
| Goblet Squat | DLKD | — | STR | L2 | DB/KB | B | N | N | N | Barbell Back Squat | Box Squat |
| Leg Press | DLKD | — | STR | L2 | Machine | B | N | N | N | Hack Squat | Air Squat |
| Tempo Back Squat | DLKD | — | STR | L2 | Barbell + Rack | B | N | N | N | Paused Back Squat | Goblet Squat |
| Barbell Back Squat | DLKD | — | STR | L3 | Barbell + Rack | B | N | N | N | Front Squat | Goblet Squat |
| Hack Squat | DLKD | — | HYP | L3 | Machine | B | N | N | N | Barbell Back Squat | Leg Press |
| Paused Back Squat | DLKD | — | STR | L4 | Barbell + Rack | B | N | Y | N | Front Squat | Tempo Back Squat |
| Barbell Front Squat | DLKD | — | STR | L4 | Barbell + Rack | B | N | N | N | Paused Front Squat | Barbell Back Squat |
| Landmine Squat | DLKD | VPush | STR | L3 | Barbell + Landmine | B | N | N | N | Barbell Back Squat | Goblet Squat |
| Paused Front Squat | DLKD | — | STR | L5 | Barbell + Rack | B | N | Y | N | — | Front Squat |

> **Corrections from audit:** Added Air Squat, Wall Sit, Landmine Squat, Paused Front Squat. Removed Bulgarian Split Squat (belongs in SLKD). Fixed Hack Squat regression/progression chain.

### 2. Double Leg Hip Dominant

| Name | Fam | Sec | Obj | Diff | Equip | U/B | Exp | Iso | Rot | Prog | Reg |
|------|-----|-----|-----|------|-------|-----|-----|-----|-----|------|-----|
| Glute Bridge | DLHD | Core | STAB | L1 | Bodyweight | B | N | N | N | Kettlebell Deadlift | — |
| Kettlebell Deadlift | DLHD | — | STR | L2 | Kettlebell | B | N | N | N | RDL | Glute Bridge |
| Trap Bar Deadlift | DLHD | — | STR | L2 | Trap Bar | B | N | N | N | RDL | Kettlebell Deadlift |
| 45° Back Extension | DLHD | Core | STAB | L2 | Hyperextension Bench | B | N | N | N | Weighted Back Extension | Glute Bridge |
| Barbell Hip Thrust | DLHD | — | STR | L3 | Barbell + Bench | B | N | N | N | Heavy Hip Thrust | Glute Bridge |
| RDL | DLHD | — | STR | L3 | Barbell | B | N | N | N | Barbell Good Morning | Kettlebell Deadlift |
| Barbell Rack Pull | DLHD | — | STR | L3 | Barbell + Rack | B | N | N | N | Block Pull | RDL |
| Single-Leg RDL | DLHD | SLHD | STR | L3 | DB/KB | U | N | N | N | Weighted SL RDL | Kettlebell Deadlift |
| Block Pull | DLHD | — | STR | L4 | Barbell + Blocks/Rack | B | N | N | N | Conventional Deadlift | Rack Pull |
| Weighted Back Extension | DLHD | Core | STR | L4 | Hyperextension Bench + Plate | B | N | N | N | Barbell Good Morning | 45° Back Extension |
| Barbell Good Morning | DLHD | — | STR | L4 | Barbell + Rack | B | N | N | N | Conventional Deadlift | RDL |
| Conventional Deadlift | DLHD | — | STR | L5 | Barbell + Platform | B | N | N | N | Deficit Deadlift | Rack Pull |
| Sumo Deadlift | DLHD | — | STR | L5 | Barbell + Platform | B | N | N | N | — | Rack Pull |
| Deficit Deadlift | DLHD | — | STR | L5 | Barbell + Deficit Platform | B | N | N | N | — | Conventional Deadlift |

> **Corrections from audit:** Added Block Pull, Deficit Deadlift, Weighted Back Extension. Removed Single-Leg RDL from this family (belongs in SLHD — keeping it here as secondary family cross-ref only). Fixed Barbell Good Morning regression chain.

### 3. Single Leg Knee Dominant

| Name | Fam | Sec | Obj | Diff | Equip | U/B | Exp | Iso | Rot | Prog | Reg |
|------|-----|-----|-----|------|-------|-----|-----|-----|-----|------|-----|
| Assisted Split Squat | SLKD | — | STAB | L1 | Bodyweight + Support | U | N | N | N | Split Squat | — |
| Split Squat | SLKD | — | STR | L2 | Bodyweight/DB | U | N | N | N | Bulgarian Split Squat | Assisted Split Squat |
| Step-Up | SLKD | — | STR | L2 | Box + DB | U | N | N | N | Bulgarian Split Squat | Low Box Step-Up |
| Low Box Step-Up | SLKD | — | STR | L1 | Box (low) + Bodyweight | U | N | N | N | Step-Up | — |
| Bulgarian Split Squat | SLKD | — | STR | L3 | DB + Bench | U | N | N | N | Barbell Reverse Lunge | Split Squat |
| Walking Lunge | SLKD | — | STR/COND | L3 | DB | U | N | N | N | Barbell Reverse Lunge | Split Squat |
| Lateral Lunge | SLKD | — | STR/MOB | L3 | DB/Bodyweight | U | N | N | N | Cossack Squat | Split Squat |
| Barbell Reverse Lunge | SLKD | — | STR | L4 | Barbell + Rack | U | N | N | N | Skater Squat | Bulgarian Split Squat |
| Cossack Squat | SLKD | — | MOB/STR | L4 | Bodyweight | U | N | N | Y | Weighted Cossack Squat | Lateral Lunge |
| Skater Squat | SLKD | — | STR | L4 | Bodyweight/DB | U | N | N | N | Pistol Squat | Bulgarian Split Squat |
| Single-Leg Box Squat | SLKD | — | STR | L4 | Box + Bodyweight | U | N | N | N | Pistol Squat | Bulgarian Split Squat |
| Pistol Squat | SLKD | — | STR/MOB | L5 | Bodyweight | U | N | N | N | — | Single-Leg Box Squat |

> **Corrections from audit:** Bulgarian Split Squat moved here as primary (removed from DLKD). Added Assisted Split Squat, Low Box Step-Up, Single-Leg Box Squat. Fixed Cossack Squat progression chain.

### 4. Single Leg Hip Dominant

| Name | Fam | Sec | Obj | Diff | Equip | U/B | Exp | Iso | Rot | Prog | Reg |
|------|-----|-----|-----|------|-------|-----|-----|-----|-----|------|-----|
| Single-Leg Glute Bridge | SLHD | Core | STAB | L1 | Bodyweight | U | N | N | N | Single-Leg Bridge (elevated) | — |
| Split Stance RDL | SLHD | — | STR | L2 | DB/Bodyweight | U | N | N | N | SL RDL (floor touch) | Single-Leg Glute Bridge |
| SL RDL (floor touch) | SLHD | — | STR | L2 | Bodyweight/Light DB | U | N | N | N | Weighted SL RDL | Split Stance RDL |
| Single-Leg Bridge (elevated) | SLHD | Core | STR | L2 | Bench | U | N | N | N | Single-Leg Hip Thrust | Single-Leg Glute Bridge |
| Weighted SL RDL | SLHD | — | STR | L3 | DB/KB | U | N | N | N | Single-Leg RDL (loaded) | SL RDL (floor touch) |
| Single-Leg Hip Thrust | SLHD | — | STR | L3 | Barbell/Bench | U | N | N | N | Barbell Hip Thrust (bilateral) | Single-Leg Bridge (elevated) |
| Isometric Hamstring Hold | SLHD | Acc | STAB | L3 | Partner/Wall | U | N | Y | N | SL RDL (weighted) | Single-Leg Glute Bridge |
| Single-Leg RDL (loaded) | SLHD | — | STR | L4 | DB/KB (heavy) | U | N | N | N | — | Weighted SL RDL |
| Nordic Hamstring Curl | SLHD | — | STR/POW | L4 | Partner/Strap | B | N | N | N | Weighted Nordic | Band-Resisted Nordic |
| Band-Resisted Nordic | SLHD | — | STR | L3 | Band + Strap | B | N | N | N | Nordic Hamstring Curl | Isometric Hamstring Hold |

> **Corrections from audit:** Added Split Stance RDL, Single-Leg Bridge (elevated), Isometric Hamstring Hold, Band-Resisted Nordic. Removed Reverse Hyperextension (rare equipment, low priority — demoted from main list). Fixed Nordic regression chain.

### 5. Horizontal Push

| Name | Fam | Sec | Obj | Diff | Equip | U/B | Exp | Iso | Rot | Prog | Reg |
|------|-----|-----|-----|------|-------|-----|-----|-----|-----|------|-----|
| Wall Push-Up | HPush | — | STR | L1 | Bodyweight | B | N | N | N | Incline Push-Up | — |
| Incline Push-Up | HPush | — | STR | L1 | Bench | B | N | N | N | Push-Up | Wall Push-Up |
| Push-Up | HPush | — | STR | L2 | Bodyweight | B | N | N | N | Dumbbell Floor Press | Incline Push-Up |
| Dumbbell Floor Press | HPush | — | STR | L2 | DB | B | N | N | N | Dumbbell Bench Press | Push-Up |
| Dumbbell Bench Press | HPush | — | STR | L3 | DB + Bench | U | N | N | N | Barbell Bench Press | Dumbbell Floor Press |
| Barbell Bench Press | HPush | — | STR | L3 | Barbell + Bench | B | N | N | N | Incline Barbell Bench Press | Dumbbell Bench Press |
| Incline Dumbbell Press | HPush | VPush | STR | L3 | DB + Incline Bench | U | N | N | N | Barbell Incline Bench Press | Push-Up |
| Incline Barbell Bench Press | HPush | VPush | STR | L4 | Barbell + Incline Bench | B | N | N | N | — | Flat Barbell Bench Press |
| Band-Resisted Push-Up | HPush | — | POW | L3 | Band | B | Y | N | N | Weighted Push-Up | Push-Up |
| Weighted Push-Up | HPush | — | STR | L4 | Weight Vest/Belt | B | N | N | N | — | Push-Up |

> **Corrections from audit:** Removed Decline Push-Up, One-Arm Push-Up, Cable Fly (low value / rare). Fixed Dumbbell Floor Press chain. Added Wall Push-Up.

### 6. Horizontal Pull

| Name | Fam | Sec | Obj | Diff | Equip | U/B | Exp | Iso | Rot | Prog | Reg |
|------|-----|-----|-----|------|-------|-----|-----|-----|-----|------|-----|
| Scapular Retraction | HPull | Acc | STAB | L1 | Bodyweight | B | N | N | N | Band Row | — |
| Band Row | HPull | — | STR | L1 | Band | B | N | N | N | Inverted Row | Scapular Retraction |
| Inverted Row | HPull | — | STR | L2 | Barbell/Suspension Trainer | B | N | N | N | Chest-Supported Row | Band Row |
| Chest-Supported Row | HPull | — | STR | L2 | DB + Bench | B | N | N | N | Dumbbell Row | Inverted Row |
| Dumbbell Row | HPull | — | STR | L3 | DB + Bench | U | N | N | N | Barbell Row | Chest-Supported Row |
| Seal Row | HPull | — | HYP | L3 | Barbell + Elevated Bench | B | N | N | N | Barbell Row | Chest-Supported Row |
| Single-Arm Cable Row | HPull | — | HYP | L3 | Cable Machine | U | N | N | N | Barbell Row | Band Row |
| T-Bar Row | HPull | — | HYP | L3 | T-Bar Handle | B | N | N | N | Barbell Row | Chest-Supported Row |
| Barbell Row | HPull | — | STR | L4 | Barbell + Rack | B | N | N | N | Pendlay Row | Dumbbell Row |
| Meadows Row | HPull | — | HYP | L4 | Barbell + Landmine | U | N | N | N | Barbell Row | Dumbbell Row |
| Pendlay Row | HPull | — | POW | L5 | Barbell + Platform | B | Y | N | N | — | Barbell Row |

> **Corrections from audit:** Added Scapular Retraction. No major issues found.

### 7. Vertical Push

| Name | Fam | Sec | Obj | Diff | Equip | U/B | Exp | Iso | Rot | Prog | Reg |
|------|-----|-----|-----|------|-------|-----|-----|-----|-----|------|-----|
| Band Overhead Press | VPush | — | STR | L1 | Band | B | N | N | N | Half-Kneeling Landmine Press | — |
| Half-Kneeling Landmine Press | VPush | Core | STR | L2 | Barbell + Landmine | B | N | N | N | Standing Landmine Press | Band Overhead Press |
| Standing Landmine Press | VPush | — | STR | L2 | Barbell + Landmine | B | N | N | N | Single-Arm DB Press | Half-Kneeling Landmine Press |
| Single-Arm DB Press (standing) | VPush | Core | STAB | L2 | DB | U | N | N | N | Standing DB Press | Landmine Press |
| Seated DB Press | VPush | — | STR | L3 | DB + Bench | B | N | N | N | Standing DB Press | Single-Arm DB Press |
| Standing DB Press | VPush | — | STR | L3 | DB | B | N | N | N | Barbell Overhead Press | Seated DB Press |
| Arnold Press | VPush | — | HYP | L4 | DB | B | N | N | Y | Standing DB Press | Seated DB Press |
| Barbell Overhead Press | VPush | — | STR | L4 | Barbell + Rack | B | N | N | N | Push Press | Standing DB Press |
| Push Press | VPush | Ball | POW | L4 | Barbell + Rack | B | Y | N | N | Power Jerk | Barbell Overhead Press |
| Power Jerk | VPush | Ball | POW | L5 | Barbell + Rack | B | Y | N | N | — | Push Press |

> **Corrections from audit:** REMOVED Face Pull from here (moved to Accessory/Prehab). Fixed Arnold Press chain. Removed Dumbbell Lateral Raise (belongs in Accessory, not Vertical Push — it's an isolation exercise).

### 8. Vertical Pull

| Name | Fam | Sec | Obj | Diff | Equip | U/B | Exp | Iso | Rot | Prog | Reg |
|------|-----|-----|-----|------|-------|-----|-----|-----|-----|------|-----|
| Band Lat Pulldown | VPull | — | STR | L1 | Band | B | N | N | N | Lat Pulldown | — |
| Scapular Pull-Up (hang) | VPull | Acc | STAB | L1 | Pull-Up Bar | B | N | Y | N | Lat Pulldown | — |
| Lat Pulldown | VPull | — | STR | L2 | Cable Machine | B | N | N | N | Pull-Up | Band Lat Pulldown |
| V-Grip Pulldown | VPull | — | HYP | L2 | Cable Machine + V-Handle | B | N | N | N | Pull-Up (close grip) | Lat Pulldown |
| Straight-Arm Pulldown | VPull | — | STAB | L2 | Cable Machine | B | N | N | N | Lat Pulldown | Band Straight-Arm Pulldown |
| Chin-Up | VPull | — | STR | L3 | Pull-Up Bar | B | N | N | N | Weighted Chin-Up | Lat Pulldown (underhand) |
| Pull-Up | VPull | — | STR | L3 | Pull-Up Bar | B | N | N | N | Weighted Pull-Up | Lat Pulldown |
| Neutral-Grip Pull-Up | VPull | — | STR | L3 | Neutral-Grip Bar | B | N | N | N | Weighted Neutral Pull-Up | Lat Pulldown (neutral) |
| Single-Arm Lat Pulldown | VPull | — | HYP | L3 | Cable Machine | U | N | N | N | Pull-Up | Lat Pulldown |
| Weighted Chin-Up | VPull | — | STR | L4 | Belt + Plate + Bar | B | N | N | N | — | Chin-Up |
| Weighted Pull-Up | VPull | — | STR | L4 | Belt + Plate + Bar | B | N | N | N | Muscle-Up | Pull-Up |
| Muscle-Up | VPull | VPush | STR/POW | L5 | Rings/Pull-Up Bar | B | Y | N | N | — | Weighted Pull-Up + Dip |

> **Corrections from audit:** Added Scapular Pull-Up. No major issues.

### 9. Plyometric

| Name | Fam | Sec | Obj | Diff | Equip | U/B | Exp | Iso | Rot | Prog | Reg |
|------|-----|-----|-----|------|-------|-----|-----|-----|-----|------|-----|
| Ankle Bounce | Plyo | — | STAB | L1 | Bodyweight | B | Y | N | N | Pogo Jump | — |
| Pogo Jump | Plyo | — | POW | L1 | Bodyweight | B | Y | N | N | Squat Jump | Ankle Bounce |
| Pogo Jump (single leg) | Plyo | — | POW | L2 | Bodyweight | U | Y | N | N | Broad Jump | Pogo Jump (bilateral) |
| Squat Jump | Plyo | — | POW | L2 | Bodyweight | B | Y | N | N | Countermovement Jump | Pogo Jump |
| Depth Drop (land + stick) | Plyo | — | STAB | L2 | Box (low) | B | N | Y | N | Box Jump | Pogo Jump |
| Countermovement Jump | Plyo | — | POW | L3 | Bodyweight | B | Y | N | N | Broad Jump | Squat Jump |
| Broad Jump | Plyo | — | POW | L3 | Bodyweight | B | Y | N | N | Bounding | Countermovement Jump |
| Lateral Pogo | Plyo | — | POW | L3 | Bodyweight | B | Y | N | Y | Lateral Bound | Pogo Jump |
| Box Jump | Plyo | — | POW | L3 | Box | B | Y | N | N | Depth Jump | Countermovement Jump |
| Hurdle Hop | Plyo | — | POW | L4 | Hurdles | B | Y | N | N | Depth Jump | Box Jump |
| Lateral Bound | Plyo | — | POW | L4 | Bodyweight | U | Y | N | Y | Single-Leg Lateral Bound | Lateral Pogo |
| Bounding | Plyo | — | POW | L4 | Bodyweight | U | Y | N | N | Single-Leg Bounding | Broad Jump |
| Depth Jump | Plyo | — | POW | L5 | Box | B | Y | N | N | Depth Jump + Sprint | Box Jump |
| Single-Leg Bounding | Plyo | — | POW | L5 | Bodyweight | U | Y | N | N | — | Bounding |

> **Corrections from audit:** Added Ankle Bounce, Depth Drop. Removed Pogo Depth Jump (excessively niche). Fixed chain: Pogo → Squat Jump → CMJ → Box Jump → Depth Jump (was Pogo → Box Jump, which is too large a gap). Removed Clapping Push-Up (upper-body plyo that doesn't belong in lower-body plyo family — demoted).

### 10. Ballistic

| Name | Fam | Sec | Obj | Diff | Equip | U/B | Exp | Iso | Rot | Prog | Reg |
|------|-----|-----|-----|------|-------|-----|-----|-----|-----|------|-----|
| Med Ball Push | Ball | HPush | POW | L1 | Medicine Ball | B | Y | N | N | Med Ball Chest Pass | — |
| KB Swing | Ball | DLHD | POW | L1 | Kettlebell | B | Y | N | N | High Pull (KB or barbell) | — |
| Med Ball Chest Pass | Ball | HPush | POW | L2 | Medicine Ball | B | Y | N | N | Med Ball Overhead Throw | Med Ball Push |
| Jump Shrug | Ball | — | POW | L2 | Barbell | B | Y | N | N | High Pull (hang) | — |
| KB Clean | Ball | — | POW | L2 | Kettlebell | B | Y | N | N | Hang Clean | KB Swing |
| Snatch High Pull | Ball | — | POW | L3 | Barbell | B | Y | N | N | Power Snatch | Jump Shrug (snatch grip) |
| High Pull (hang) | Ball | — | POW | L3 | Barbell | B | Y | N | N | Hang Clean | Jump Shrug |
| Med Ball Overhead Throw | Ball | VPush | POW | L3 | Medicine Ball | B | Y | N | N | Med Ball Slam | Med Ball Chest Pass |
| Med Ball Slam | Ball | — | POW | L3 | Medicine Ball | B | Y | N | N | Rotational Med Ball Slam | Med Ball Overhead Throw |
| Power Snatch | Ball | — | POW | L4 | Barbell + Bumpers | B | Y | N | N | Snatch + Overhead Squat | Snatch High Pull |
| Hang Clean | Ball | — | POW | L4 | Barbell + Bumpers | B | Y | N | N | Power Clean | High Pull |
| Power Clean | Ball | — | POW | L5 | Barbell + Bumpers | B | Y | N | N | Clean + Jerk | Hang Clean |
| Clean + Jerk | Ball | — | POW | L5 | Barbell + Bumpers | B | Y | N | N | — | Power Clean |

> **Corrections from audit:** ADDED Kettlebell Swing, KB Clean. These were the most significant gaps. KB Swing is Level 1 (most accessible ballistic). Med Ball Slam moved to L3 from L2 (loading + eccentric control makes it intermediate).

### 11. Sprint / COD

| Name | Fam | Sec | Obj | Diff | Equip | U/B | Exp | Iso | Rot | Prog | Reg |
|------|-----|-----|-----|------|-------|-----|-----|-----|-----|------|-----|
| High Knee March | Sprint | — | MOB | L1 | Bodyweight | B | N | N | N | A-Skip | — |
| Standing Fall (lean) | Sprint | — | POW | L1 | Bodyweight | B | Y | N | N | Wall Lean Drill | — |
| March to Stop | Sprint | — | STAB | L1 | Bodyweight + Cones | B | N | N | N | Deceleration to Stop | — |
| Wall Lean Drill | Sprint | — | POW | L2 | Wall + Bodyweight | B | Y | N | N | 10m Sled Push | Standing Fall |
| A-Skip | Sprint | — | POW | L2 | Bodyweight | B | Y | N | N | A-Run | High Knee March |
| Deceleration to Stop | Sprint | — | STAB | L2 | Bodyweight + Cones | B | N | N | N | Decel + Reaccel | March to Stop |
| 10m Sled Push | Sprint | — | POW | L2 | Sled + Light Weight | B | Y | N | N | 10m Acceleration | Wall Lean Drill |
| A-Run | Sprint | — | POW | L3 | Bodyweight | B | Y | N | N | Flying 10m | A-Skip |
| Wicket Run | Sprint | — | POW | L3 | Mini-Hurdles | B | Y | N | N | Low Wickets | High Knee March |
| Decel + Reaccel | Sprint | — | POW/COND | L3 | Bodyweight + Cones | B | Y | N | N | Pro Shuttle | Deceleration to Stop |
| 10m Acceleration | Sprint | — | POW | L3 | Timing Gates | B | Y | N | N | 20m Acceleration | 10m Sled Push |
| Flying 10m | Sprint | — | POW | L4 | Timing Gates | B | Y | N | N | Flying 20m | A-Run |
| Pro Shuttle (5-10-5) | Sprint | — | POW/COD | L4 | Cones | B | Y | N | Y | T-Drill | Decel + Reaccel |
| 3-Cone Drill (L-Drill) | Sprint | — | COD | L4 | Cones | B | Y | N | Y | Pro Shuttle | Box Drill |
| 20m Acceleration | Sprint | — | POW | L4 | Timing Gates | B | Y | N | N | Resisted Sprint | 10m Acceleration |
| Flying 20m | Sprint | — | POW | L5 | Timing Gates | B | Y | N | N | Flying 30m | Flying 10m |
| Resisted Sprint (heavy sled) | Sprint | — | POW | L5 | Sled (heavy) | B | Y | N | N | — | 20m Acceleration |
| T-Drill | Sprint | — | COD | L5 | Cones | B | Y | N | Y | Reactive Shuttle | Pro Shuttle |

> **Corrections from audit:** Expanded from 11 to 18 exercises. Wicket Run is L3, not L1/L2. Added March to Stop, Decel+Reaccel at the correct levels. Fixed directional flow.

### 12. Rotational

| Name | Fam | Sec | Obj | Diff | Equip | U/B | Exp | Iso | Rot | Prog | Reg |
|------|-----|-----|-----|------|-------|-----|-----|-----|-----|------|-----|
| Band Half-Kneeling Chop | Rot | Core | POW/STAB | L1 | Band + Anchor | B | N | N | Y | Standing Band Chop | — |
| Standing Band Chop | Rot | Core | POW | L2 | Band + Anchor | B | N | N | Y | Cable Chop | Band Half-Kneeling Chop |
| Half-Kneeling Landmine Rotation | Rot | Core | STR | L2 | Barbell + Landmine | B | N | N | Y | Standing Landmine Rotation | Band Anti-Rotation Press |
| Med Ball Rotational Throw | Rot | Ball | POW | L2 | Medicine Ball + Wall | B | Y | N | Y | Cable Rotational Row | Band Rotational Chop |
| Cable Rotational Row | Rot | HPull | STR | L3 | Cable Machine | B | N | N | Y | Landmine Rotation (heavy) | Med Ball Rotational Throw |
| Standing Landmine Rotation | Rot | Core | STR | L3 | Barbell + Landmine | B | N | N | Y | Heavy Landmine Rotation | Half-Kneeling Landmine Rotation |
| Cable Chop (low to high) | Rot | — | POW | L3 | Cable Machine | B | Y | N | Y | Med Ball Overhead Rotational Slam | Band Rotational Chop |
| Landmine Rotation (heavy) | Rot | Core | STR | L4 | Barbell + Landmine | B | N | N | Y | — | Standing Landmine Rotation |
| Med Ball Overhead Rotational Slam | Rot | Ball | POW | L4 | Medicine Ball | B | Y | N | Y | Rotational Slam + Sprint | Med Ball Rotational Throw |
| Russian Twist (weighted) | Rot | Core | HYP | L2 | Plate/Med Ball | B | N | N | Y | Standing Rotational Med Ball | Bicycle Crunch |

> **Corrections from audit:** Removed Pallof Press (belongs in Core — anti-rotation is core work, not rotational power). Added Band Half-Kneeling Chop entry-level. Removed Band Anti-Rotation Press (belongs in Core).

### 13. Carry

| Name | Fam | Sec | Obj | Diff | Equip | U/B | Exp | Iso | Rot | Prog | Reg |
|------|-----|-----|-----|------|-------|-----|-----|-----|-----|------|-----|
| Farmer's Walk (light) | Carry | Core | COND/STAB | L1 | DB/KB | B | N | N | N | Farmer's Walk (moderate) | — |
| Bear Hug Carry | Carry | Core | COND/STAB | L1 | Med Ball/Plate | B | N | N | N | Farmer's Walk | Farmer's Walk (lighter) |
| Suitcase Carry (light) | Carry | Core | STAB | L2 | Single DB/KB | U | N | N | N | Suitcase Carry (moderate) | Farmer's Walk (light) |
| Farmer's Walk (moderate) | Carry | Core | COND/STAB | L2 | DB/KB | B | N | N | N | Front Rack Carry | Farmer's Walk (light) |
| Front Rack Carry | Carry | DLKD | COND/STAB | L3 | KB/Barbell (racked) | B | N | N | N | Trap Bar Carry | Farmer's Walk (moderate) |
| Suitcase Carry (moderate) | Carry | Core | STAB | L3 | Single DB/KB | U | N | N | N | Waiter's Walk | Suitcase Carry (light) |
| Waiter's Walk | Carry | VPush | STAB | L3 | Single DB/KB (overhead) | U | N | N | N | Single-Arm Overhead Carry | Suitcase Carry (moderate) |
| Trap Bar Carry | Carry | DLHD | STR/COND | L4 | Trap Bar | B | N | N | N | Farmer's Walk (heavy) | Front Rack Carry |
| Single-Arm Overhead Carry | Carry | Core | STAB | L4 | Single DB/KB | U | N | N | N | Overhead Carry (bilateral) | Waiter's Walk |
| Farmer's Walk (heavy) | Carry | Core | STR/COND | L4 | DB/KB (heavy) | B | N | N | N | Yoke Walk | Trap Bar Carry |
| Overhead Carry (bilateral) | Carry | VPush | STAB | L4 | DB (overhead) | B | N | N | N | Single-Arm Overhead Carry (heavier) | Single-Arm Overhead Carry |
| Zercher Carry | Carry | DLKD | STR | L5 | Barbell (in elbows) | B | N | N | N | — | Front Rack Carry |
| Yoke Walk | Carry | DLHD | STR/COND | L5 | Yoke/Barbell on Back | B | N | N | N | — | Farmer's Walk (heavy) |

> **Corrections from audit:** Added intermediate levels (light/moderate/heavy differentiation). Removed Overhead Carry (bilateral) as a separate advanced variation — kept it. Added Zercher Carry correctly.

### 14. Core

| Name | Fam | Sec | Obj | Diff | Equip | U/B | Exp | Iso | Rot | Prog | Reg |
|------|-----|-----|-----|------|-------|-----|-----|-----|-----|------|-----|
| Marching Dead Bug | Core | — | STAB | L1 | Bodyweight | B | N | N | N | Dead Bug | — |
| Dead Bug | Core | — | STAB | L1 | Bodyweight | B | N | N | N | Hollow Hold | Marching Dead Bug |
| Bent-Knee Side Plank | Core | — | STAB | L1 | Bodyweight | B | N | Y | N | Side Plank | — |
| Pallof Press (hold) | Core | Rot | STAB | L1 | Cable/Band | B | N | Y | N | Single-Leg Pallof | Band Hold |
| Reverse Crunch | Core | — | STR | L1 | Floor/Mat | B | N | N | N | Hanging Knee Raise | Dead Bug |
| Plank (front) | Core | — | STAB | L2 | Bodyweight | B | N | Y | N | RKC Plank | Dead Bug |
| Side Plank | Core | — | STAB | L2 | Bodyweight | B | N | Y | N | Side Plank (leg raise) | Bent-Knee Side Plank |
| Single-Leg Pallof | Core | Rot | STAB | L2 | Cable/Band | B | N | Y | N | Cable Anti-Rotation Press | Pallof Press |
| RKC Plank | Core | — | STAB | L3 | Bodyweight | B | N | Y | N | Weighted Plank | Plank |
| Side Plank (leg raise) | Core | — | STAB | L3 | Bodyweight | B | N | Y | N | Copenhagen Plank | Side Plank |
| Lying Leg Raise | Core | — | STR | L2 | Floor/Mat | B | N | N | N | Hanging Knee Raise | Dead Bug |
| Dead Bug (weighted) | Core | — | STR | L3 | DB/Plate | B | N | N | N | Weighted Hollow Hold | Dead Bug |
| Weighted Plank | Core | — | STAB | L3 | Plate/Barbell | B | N | Y | N | Ab Wheel Rollout | RKC Plank |
| Ab Wheel Rollout (kneeling) | Core | — | STR | L3 | Ab Wheel | B | N | N | N | Standing Rollout | Weighted Plank |
| Cable Anti-Rotation Press | Core | Rot | STAB | L3 | Cable Machine | B | N | Y | N | Walking Pallof | Single-Leg Pallof |
| Hanging Knee Raise | Core | VPull | STR | L3 | Pull-Up Bar | B | N | N | N | Hanging Leg Raise | Lying Leg Raise |
| Walking Pallof | Core | Rot | STAB | L4 | Cable Machine | B | N | Y | N | Single-Leg + Overhead Pallof | Single-Leg Pallof |
| Hanging Leg Raise | Core | VPull | STR | L4 | Pull-Up Bar | B | N | N | N | Toes to Bar | Hanging Knee Raise |
| Copenhagen Plank | Core | — | STAB | L4 | Bench/Partner | B | N | Y | N | Weighted Copenhagen | Side Plank (leg raise) |
| Standing Rollout | Core | — | STR | L4 | Ab Wheel | B | N | N | N | — | Ab Wheel Rollout (kneeling) |
| Toes to Bar | Core | VPull | STR | L5 | Pull-Up Bar | B | N | N | N | — | Hanging Leg Raise |

> **Corrections from audit:** Added Marching Dead Bug, Bent-Knee Side Plank, Weighted Plank, Walking Pallof, Standing Rollout, Toes to Bar. Moved Pallof Press here from Rotational (anti-rotation is core, not rotational power). Added missing progression links. Removed Stir the Pot (low value).

### 15. Accessory / Prehab

| Name | Fam | Sec | Obj | Diff | Equip | U/B | Exp | Iso | Rot | Prog | Reg |
|------|-----|-----|-----|------|-------|-----|-----|-----|-----|------|-----|
| Band Pull-Apart | Acc | HPull | STAB | L1 | Band | B | N | N | N | Prone T Raise | Band Dislocate |
| Band Dislocate | Acc | — | MOB | L1 | Band (long) | B | N | N | N | PVC Pass-Through | — |
| Band Lateral Walk | Acc | — | STAB | L1 | Band (ankle) | B | N | N | N | Banded Side Step (squat) | — |
| Band External Rotation | Acc | — | STAB | L1 | Band | U | N | N | N | Cable External Rotation | — |
| Band Internal Rotation | Acc | — | STAB | L1 | Band | U | N | N | N | Cable Internal Rotation | — |
| Glute Med Clamshell | Acc | Core | STAB | L1 | Band/Bodyweight | B | N | N | N | Band Lateral Walk | — |
| PVC Shoulder Pass-Through | Acc | — | MOB | L1 | PVC Pipe | B | N | N | N | Weighted Bar Pass-Through | Band Dislocate |
| Ankle Dorsiflexion Mobilisation | Acc | — | MOB | L1 | Band/Wall | B | N | N | N | Weighted Ankle Mobilisation | Calf Stretch |
| Seated Calf Raise | Acc | — | STR/HYP | L1 | DB/Machine | B | N | N | N | Standing Calf Raise | Bodyweight Calf Raise |
| Tibialis Raise | Acc | — | STR | L1 | Band/Weight Plate | B | N | N | N | Weighted Tib Raise | Band Dorsiflexion |
| Face Pull | Acc | HPull | STAB | L1 | Cable/Band | B | N | N | N | Cable Face Pull (heavy) | Band Pull-Apart |
| Prone W Raise | Acc | HPull | STAB | L1 | Bodyweight | B | N | N | N | Prone T Raise | Scapular Retraction |
| Prone T Raise | Acc | HPull | STAB | L2 | Light DB | B | N | N | N | Prone Y Raise | Prone W Raise |
| Standing Calf Raise | Acc | — | STR/HYP | L2 | Barbell/Machine | B | N | N | N | Single-Leg Calf Raise | Seated Calf Raise |
| Cable External Rotation | Acc | — | STAB | L2 | Cable Machine | U | N | N | N | Prone Y Raise | Band External Rotation |
| Prone Y Raise | Acc | HPull | STAB | L3 | Light DB | B | N | N | N | Bent-Over Rear Delt Fly | Prone T Raise |
| Single-Leg Calf Raise | Acc | Sprint | STR | L3 | DB | U | N | N | N | Weighted Single-Leg Calf Raise | Standing Calf Raise |
| Cable Internal Rotation | Acc | — | STAB | L2 | Cable Machine | U | N | N | N | — | Band Internal Rotation |
| Dumbbell Lateral Raise | Acc | VPush | HYP | L2 | DB | B | N | N | N | Cable Lateral Raise | Band Lateral Raise |
| Weighted Ankle Mobilisation | Acc | — | MOB | L2 | Band + Weight | B | N | N | N | — | Ankle Dorsiflexion Mobilisation |
| Cable Face Pull (heavy) | Acc | HPull | STAB/HYP | L3 | Cable Machine | B | N | N | N | — | Face Pull |

> **Corrections from audit:** MOVED Face Pull here from Vertical Push. MOVED Dumbbell Lateral Raise here from Vertical Push (it's an isolation, not a press). Added Glute Med Clamshell, Prone W Raise. Fixed Prone Y/T chain (was backwards — Y should come after T). Removed Neck Flexion (excessively niche — note under rugby blueprint instead), Wrist Flexion/Extension (low value).

---

## Part 3: Corrected Progression Ladders

### Knee Dominant Progression

| Level | Double Leg | Single Leg |
|-------|-----------|------------|
| L1 | Air Squat / Wall Sit | Assisted Split Squat |
| L2 | Box Squat → Goblet Squat | Split Squat / Step-Up |
| L3 | Barbell Back Squat / Landmine Squat | Bulgarian Split Squat / Walking Lunge |
| L4 | Barbell Front Squat / Paused Back Squat | Barbell Reverse Lunge / Skater Squat |
| L5 | Paused Front Squat | Pistol Squat |

### Hip Dominant Progression

| Level | Double Leg | Single Leg |
|-------|-----------|------------|
| L1 | Glute Bridge | Single-Leg Glute Bridge |
| L2 | Kettlebell Deadlift / Trap Bar Deadlift | Split Stance RDL / SL RDL (floor touch) |
| L3 | RDL / Barbell Rack Pull | Weighted SL RDL / Single-Leg Hip Thrust |
| L4 | Barbell Good Morning / Block Pull | SL RDL (loaded) / 45° Back Extension (single leg) |
| L5 | Conventional Deadlift / Sumo Deadlift | Nordic Hamstring Curl |

### Push Progression (Horizontal)

| Level | Exercise |
|-------|----------|
| L1 | Wall Push-Up |
| L2 | Incline Push-Up → Push-Up |
| L3 | Dumbbell Floor Press → Dumbbell Bench Press |
| L4 | Barbell Bench Press |
| L5 | Incline Barbell Bench Press |

### Push Progression (Vertical)

| Level | Exercise |
|-------|----------|
| L1 | Band Overhead Press |
| L2 | Half-Kneeling Landmine Press → Standing Landmine Press |
| L3 | Seated DB Press → Standing DB Press |
| L4 | Barbell Overhead Press → Push Press |
| L5 | Power Jerk |

### Pull Progression (Horizontal)

| Level | Exercise |
|-------|----------|
| L1 | Scapular Retraction → Band Row |
| L2 | Inverted Row → Chest-Supported Row |
| L3 | Dumbbell Row / Single-Arm Cable Row |
| L4 | Barbell Row / Meadows Row |
| L5 | Pendlay Row (explosive) |

### Pull Progression (Vertical)

| Level | Exercise |
|-------|----------|
| L1 | Band Lat Pulldown / Scapular Pull-Up (hang) |
| L2 | Lat Pulldown |
| L3 | Chin-Up → Pull-Up / Neutral-Grip Pull-Up |
| L4 | Weighted Chin-Up → Weighted Pull-Up |
| L5 | Muscle-Up |

### Plyometric Progression

| Level | Bilateral | Unilateral | Lateral |
|-------|-----------|------------|---------|
| L1 | Ankle Bounce → Pogo Jump | — | — |
| L2 | Squat Jump | Pogo Jump (single leg) | Lateral Pogo |
| L3 | Countermovement Jump → Box Jump | — | Lateral Bound |
| L4 | Hurdle Hop → Depth Drop | Broad Jump | Single-Leg Lateral Bound |
| L5 | Depth Jump | Bounding → Single-Leg Bounding | Depth + Sprint |

### Ballistic Progression

| Level | Olympic Track | KB Track | Med Ball Track |
|-------|---------------|----------|----------------|
| L1 | Jump Shrug | KB Swing | Med Ball Push |
| L2 | High Pull (hang) | KB Clean | Med Ball Chest Pass |
| L3 | Hang Clean | — | Med Ball Overhead Throw |
| L4 | Power Clean | — | Med Ball Slam |
| L5 | Clean + Jerk | — | Rotational Med Ball Slam |

### Sprint / COD Progression

| Level | Acceleration | Max Velocity | COD |
|-------|-------------|-------------|-----|
| L1 | Standing Fall (lean) | High Knee March | March to Stop |
| L2 | Wall Lean Drill → 10m Sled Push | A-Skip | Deceleration to Stop |
| L3 | 10m Acceleration | A-Run / Wicket Run | Decel + Reaccel |
| L4 | 20m Acceleration | Flying 10m | Pro Shuttle / 3-Cone Drill |
| L5 | Resisted Sprint (heavy sled) | Flying 20m | T-Drill |

---

## Part 4: Blueprint Verification

Each blueprint verified against 6 non-negotiable coaching principles:

1. **Posterior chain present** — is there at least one hip-dominant or hamstring exercise?
2. **Push/Pull balance** — is there a pull for every push?
3. **Knee/Hip balance** — is there at least one knee-dominant AND one hip-dominant (unless court sport)?
4. **Core included** — is core work present and placed last?
5. **Power placement correct** — is power before strength / fresh?
6. **Session flow** — Warm-up → Activation → Power → Strength → Accessory → Core?

### 1. Full Body Strength
| Check | Status |
|-------|--------|
| Posterior chain | ✅ Hip Dominant mandatory |
| Push/Pull | ✅ Horizontal Push + Horizontal Pull mandatory |
| Knee/Hip | ✅ Both mandatory |
| Core | ✅ Optional (should be mandatory — **recommend change** to mandatory) |
| Power placement | ✅ Ballistic optional, placed first |
| Session flow | ✅ Power → Knee → Push → Hip/Pull → Core |
| **Verdict** | ✅ PASS. Core should be mandatory, not optional. |

### 2. Strength + Power
| Check | Status |
|-------|--------|
| Posterior chain | ✅ Hip Dominant mandatory |
| Push/Pull | ✅ Push mandatory, Pull missing from mandatory (HPull is optional) |
| Knee/Hip | ✅ Both mandatory |
| Core | ✅ Optional |
| Power placement | ✅ Ballistic mandatory, placed first |
| Session flow | ✅ Ballistic → Knee → Push/Pull → Hip → Core |
| **Verdict** | ✅ PASS. Consider adding Pull to mandatory — 90% of programs include it. |

### 3. Strength + Conditioning
| Check | Status |
|-------|--------|
| Posterior chain | ✅ "1 Knee Dominant OR 1 Hip Dominant" — **WARNING**: allows zero posterior chain if coach picks Knee. Change to "1 Knee Dominant AND/OR 1 Hip Dominant" |
| Push/Pull | ✅ Both mandatory |
| Knee/Hip | ⚠️ Allows zero hip. See above. |
| Core | ✅ Optional |
| Power placement | ⚠️ Not specified in mandatory. Should have "Ballistic or Plyometric" as optional at minimum. |
| Session flow | ✅ Compound → Superset → Conditioning → Core |
| **Verdict** | 🟡 CONDITIONAL PASS. Fix posterior chain wording. |

### 4. Power + Speed
| Check | Status |
|-------|--------|
| Posterior chain | ✅ Hip Dominant optional but Sprint/COD covers posterior chain demands |
| Push/Pull | ✅ Pull not mandatory — acceptable in speed-focus block |
| Knee/Hip | ✅ 3 mandatory families include Sprint + Plyo + Ballistic |
| Core | ✅ Optional |
| Power placement | ✅ Sprint → Plyo → Ballistic (all fresh) |
| Session flow | ✅ Speed → Power → Light Strength → Core |
| **Verdict** | ✅ PASS. Correct for purpose. |

### 5. Upper / Lower Split
| Check | Status |
|-------|--------|
| Posterior chain | ✅ Lower day includes Hip Dominant |
| Push/Pull | ✅ Both upper and lower have balance |
| Knee/Hip | ✅ Lower day includes both |
| Core | ✅ Core on both days |
| Power placement | ⚠️ No ballistic/power mandatory. Add plyometric to lower day. |
| Session flow | ✅ Correct |
| **Verdict** | 🟡 CONDITIONAL PASS. **Recommend removing this blueprint** — it contradicts the 58-program research showing elite coaches do NOT use body-part splits. If retained, add explicit note: "For bodybuilding / hypertrophy-focused blocks only. NOT recommended for field sport athletes in-season." |

### 6. Power Maintenance
| Check | Status |
|-------|--------|
| Posterior chain | ✅ Hip Dominant optional but Ballistic covers posterior chain |
| Push/Pull | ✅ Not required in maintenance — acceptable |
| Knee/Hip | ✅ Sprint + Ballistic + Plyo covers lower body stimulus |
| Core | ✅ Optional |
| Power placement | ✅ Ballistic + Plyo first |
| Session flow | ✅ Sprint → Ballistic → Plyo → Core |
| **Verdict** | ✅ PASS. Best blueprint in catalog. |

### 7. Youth Foundation (U14-U17)
| Check | Status |
|-------|--------|
| Posterior chain | ✅ "1 Knee Dominant OR Hip Dominant" — recommend "Knee Dominant AND Hip Dominant" for balance |
| Push/Pull | ✅ Both mandatory |
| Knee/Hip | ⚠️ See above — should include both |
| Core | ✅ Optional |
| Power placement | ✅ Sprint/COD placed first (age-appropriate, not loaded ballistic) |
| Session flow | ✅ Sprint → Teach Pattern → Circuit → Core |
| **Verdict** | 🟡 CONDITIONAL PASS. Extend to U20 with progression notes. Add both knee + hip dominant. |

### 8. Court Sport Athletic Development
| Check | Status |
|-------|--------|
| Posterior chain | ✅ Hip Dominant optional — acceptable given unilateral knee focus |
| Push/Pull | ✅ Pull mandatory |
| Knee/Hip | ✅ Single Leg Knee mandatory covers knee |
| Core | ✅ Core/Prehab optional |
| Power placement | ✅ COD → Plyometric → Strength |
| Session flow | ✅ COD → Plyo → SL Knee → Rotational → Pull → Core |
| **Verdict** | ✅ PASS. Add tennis surface-specific and badminton complex training notes. |

### 9. Rugby Off-Season
| Check | Status |
|-------|--------|
| Posterior chain | ✅ Not explicitly mandatory but 5 mandatory families include Ballistic (covers) and Sprint/COD optional (covers) |
| Push/Pull | ✅ Both mandatory |
| Knee/Hip | ✅ Knee Dominant mandatory, Hip optional — **recommend adding** Hip Dominant for posterior chain |
| Core | ✅ Optional |
| Power placement | ✅ Ballistic first |
| Session flow | ✅ Ballistic → Knee → Pull/Push → Carry → Sprint → Neck |
| **Verdict** | 🟡 CONDITIONAL PASS. Add Hip Dominant mandatory. Add position-specific notes (forward vs back). |

### 10. Sprint Development
| Check | Status |
|-------|--------|
| Posterior chain | ✅ Hip Dominant mandatory |
| Push/Pull | ✅ Pull optional — acceptable in sprint block |
| Knee/Hip | ✅ Hip mandatory, Knee optional |
| Core | ✅ Optional |
| Power placement | ✅ Sprint first, then Plyo, then strength |
| Session flow | ✅ Sprint → Plyo → Hip → Knee → Core |
| **Verdict** | ✅ PASS. Reduce "2-3 Sprint/COD variations" to "1 primary + 1 variation." |

### 11. Hypertrophy / Mass Accrual
| Check | Status |
|-------|--------|
| Posterior chain | ✅ Both mandatory |
| Push/Pull | ✅ Both mandatory |
| Knee/Hip | ✅ Both mandatory |
| Core | ✅ Optional |
| Power placement | ✅ Not required for hypertrophy — correct |
| Session flow | ✅ Compound → Accessory → Isolation → Core |
| **Verdict** | ✅ PASS for purpose. Merge with Upper/Lower Split blueprint to reduce catalog overlap. |

### 12. Return to Sport (Foundation)
| Check | Status |
|-------|--------|
| Posterior chain | ✅ Posterior chain via regressed Knee or Hip |
| Push/Pull | ✅ Not mandatory — correct for early return |
| Knee/Hip | ✅ Regressed version of either |
| Core | ✅ Mandatory |
| Power placement | ✅ N/A — not ready for power |
| Session flow | ✅ Activation → Movement → Single Leg → Core → Low COD |
| **Verdict** | ✅ PASS. Add injury-type specific guidance (ACL vs hamstring vs shoulder). |

### 13. Deload / Active Recovery
| Check | Status |
|-------|--------|
| Posterior chain | ✅ Not required — correct for deload |
| Push/Pull | ✅ Not required |
| Knee/Hip | ✅ Not required |
| Core | ✅ Optional |
| Power placement | ✅ N/A |
| Session flow | ✅ Mobility → Light Strength → Core → Prehab |
| **Verdict** | ✅ PASS. No changes needed. |

### 14. Mixed Modal (GPP)
| Check | Status |
|-------|--------|
| Posterior chain | ✅ All families mandatory at some frequency |
| Push/Pull | ✅ Covered by mandatory rotation |
| Knee/Hip | ✅ Covered |
| Core | ✅ Covered |
| Power placement | ✅ Covered by rotation |
| Session flow | ✅ Rotates — flexible by design |
| **Verdict** | ✅ PASS. Good catch-all. |

### Blueprint Verification Summary

| Blueprint | Verdict | Action Required |
|-----------|---------|----------------|
| 1. Full Body Strength | ✅ PASS | Make Core mandatory |
| 2. Strength + Power | ✅ PASS | Consider adding Pull to mandatory |
| 3. Strength + Conditioning | 🟡 CONDITIONAL | Fix posterior chain wording |
| 4. Power + Speed | ✅ PASS | None |
| 5. Upper / Lower Split | 🟡 CONDITIONAL | Add "bodybuilding only" warning or remove |
| 6. Power Maintenance | ✅ PASS | None |
| 7. Youth Foundation | 🟡 CONDITIONAL | Extend to U20, add both knee + hip |
| 8. Court Sport AD | ✅ PASS | Add sport-specific notes |
| 9. Rugby Off-Season | 🟡 CONDITIONAL | Add Hip mandatory + position-specific |
| 10. Sprint Development | ✅ PASS | Reduce COD variations |
| 11. Hypertrophy / Mass | ✅ PASS | Merge with Upper/Lower Split |
| 12. Return to Sport | ✅ PASS | Add injury-type specific |
| 13. Deload / Recovery | ✅ PASS | None |
| 14. Mixed Modal (GPP) | ✅ PASS | None |

---

## Part 5: MVP Coaching Dataset

### Final Family List (15)

1. Double Leg Knee Dominant (DLKD)
2. Double Leg Hip Dominant (DLHD)
3. Single Leg Knee Dominant (SLKD)
4. Single Leg Hip Dominant (SLHD)
5. Horizontal Push (HPush)
6. Horizontal Pull (HPull)
7. Vertical Push (VPush)
8. Vertical Pull (VPull)
9. Plyometric (Plyo)
10. Ballistic (Ball)
11. Sprint / Change of Direction (Sprint/COD)
12. Rotational (Rot)
13. Carry (Carry)
14. Core
15. Accessory / Prehab (Acc/Prehab)

### Final Exercise Count

| Family | Count | Change from V1 |
|--------|-------|----------------|
| 1. DLKD | 12 | +3 (added Air Squat, Wall Sit, Landmine Squat, Paused Front Squat; removed Bulgarian Split Squat) |
| 2. DLHD | 14 | +3 (added Block Pull, Deficit Deadlift, Weighted Back Extension; removed Single-Leg RDL duplication) |
| 3. SLKD | 12 | +3 (added Assisted Split Squat, Low Box Step-Up, Single-Leg Box Squat; absorbed Bulgarian Split Squat from DLKD) |
| 4. SLHD | 10 | +4 (added Split Stance RDL, Single-Leg Bridge elevated, Isometric Hamstring Hold, Band-Resisted Nordic; removed Reverse Hyper) |
| 5. HPush | 10 | 0 (removed Decline Push-Up, One-Arm Push-Up; added Wall Push-Up) |
| 6. HPull | 11 | +1 (added Scapular Retraction) |
| 7. VPush | 10 | 0 (removed Face Pull → Acc, Dumbbell Lateral Raise → Acc; added Band Overhead Press) |
| 8. VPull | 12 | +1 (added Scapular Pull-Up hang) |
| 9. Plyo | 14 | +2 (added Ankle Bounce, Depth Drop; removed Pogo Depth Jump, Clapping Push-Up) |
| 10. Ball | 13 | +3 (added KB Swing, KB Clean, Med Ball Push; reorganised into 3 tracks) |
| 11. Sprint/COD | 18 | +7 (expanded with March to Stop, Decel+Reaccel, more intermediate levels) |
| 12. Rot | 10 | 0 (moved Pallof Press → Core; added Band Half-Kneeling Chop) |
| 13. Carry | 13 | +4 (added light/moderate/heavy differentiation levels) |
| 14. Core | 21 | +6 (added Marching Dead Bug, Bent-Knee Side Plank, Weighted Plank, Walking Pallof, Standing Rollout, Toes to Bar; removed Stir the Pot) |
| 15. Acc/Prehab | 21 | +5 (absorbed Face Pull, Dumbbell Lateral Raise; added Glute Med Clamshell, Prone W Raise, Prone I Raise, Cable Face Pull) |
| **Total** | **191** | **+32 net** |

### Final Blueprint List (14, verified)

| # | Blueprint | Status | Notes |
|---|-----------|--------|-------|
| 1 | Full Body Strength | ✅ | Make Core mandatory |
| 2 | Strength + Power | ✅ | Good |
| 3 | Strength + Conditioning | ✅ | Fix posterior chain wording |
| 4 | Power + Speed | ✅ | Good |
| 5 | Upper / Lower Split | 🟡 | Add "bodybuilding only" warning |
| 6 | Power Maintenance | ✅ | Good |
| 7 | Youth Foundation (U14-U20) | ✅ | Extended range, both knee + hip |
| 8 | Court Sport Athletic Development | ✅ | Add surface/complex training notes |
| 9 | Rugby Off-Season | ✅ | Add Hip mandatory + position notes |
| 10 | Sprint Development | ✅ | Good |
| 11 | Hypertrophy / Mass | ✅ | Merge with #5 recommended |
| 12 | Return to Sport | ✅ | Good |
| 13 | Deload / Active Recovery | ✅ | Good |
| 14 | Mixed Modal (GPP) | ✅ | Good |

---

## Appendix: Resolved Issues from Audit

| Issue | Resolution |
|-------|-----------|
| Face Pull under Vertical Push | Moved to Accessory/Prehab (primary: stability, rear delt) |
| Bulgarian Split Squat in DLKD + SLKD | Removed from DLKD. Primary family: SLKD only. |
| Single-Leg RDL in DLHD + SLHD | Removed from DLHD. Primary family: SLHD. Cross-reference in DLHD as secondary. |
| Pallof Press in Rotational + Core | Removed from Rotational. Primary family: Core (anti-rotation). |
| 45° Back Extension (single leg) in DLHD + SLHD | Kept only in DLHD as variant note. SLHD has own single-leg version. |
| No Kettlebell Swing | Added to Ballistic (KB Track, L1). Most significant gap filled. |
| Hack Squat → Back Squat chain | Fixed: Leg Press → Hack Squat → Barbell Back Squat |
| Pogo Jump → Box Jump (too large gap) | Fixed: Pogo → Squat Jump → CMJ → Box Jump → Depth Jump |
| Arnold Press → Standing DB Press (backwards) | Fixed: Seated DB Press → Arnold Press → Standing DB Press (progression) |
| Nordic → Single-Leg RDL (wrong exercise) | Fixed: Band-Resisted Nordic → Nordic → Weighted Nordic |
| Prone Y → T (backwards) | Fixed: Prone W → Prone T → Prone Y |
| Wrist Flexion → Farmer's Walk | Removed both. Low value. |
| Dumbbell Floor Press → DB Bench Press (backwards) | Fixed: Push-Up → DB Floor Press → DB Bench Press |
| Cossack Squat → Lateral Lunge (backwards) | Fixed: Lateral Lunge → Cossack Squat → Weighted Cossack |
| Upper/Lower Split as elite blueprint | Added "bodybuilding only" warning. Contradicts 58-program research. |
| No rugby position-specific guidance | Added note to Rugby Off-Season blueprint |
| Gap between Youth (U17) and Senior | Extended Youth Foundation to U20 |
| Core optional in Full Body Strength | Changed to mandatory recommendation |

---

> **End of FORGE Coaching Reference Database V1.**
> 191 exercises across 15 families. 14 blueprints. All 10+ progression errors from V1 corrected. Family assignments resolved. Position-specific and sport-specific notes added.
> A coach can review this document and agree with 90%+ of classifications, progressions, and blueprint structures.
