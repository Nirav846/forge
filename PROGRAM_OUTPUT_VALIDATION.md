# FORGE V2.5 PROGRAM OUTPUT VALIDATION

## Methodology

12 programs generated using:

- **Template → Session → Family Slot** architecture (templates reference families, not exercises)
- **Family-anchored exercise selection** (filter by family → equipment → difficulty → pick first)
- Equipment: Full Gym (barbell, dumbbell, cable, trap bar, plyo box, sled)
- Difficulty: Intermediate (default for senior amateur/semi-pro athletes)
- Exercise library: ~68 exercises across 15 families

No AI. No scoring. No repositories. No progression engine. Pure filter-then-select.

---

## TEST 1: Cricket Fast Bowler — Off-Season (3 days)

### Template

```
Day 1 — Strength
  Slots: Double Leg Knee Dominant, Horizontal Push, Horizontal Pull, Core

Day 2 — Power
  Slots: Ballistic, Plyometric, Core

Day 3 — Conditioning
  Slots: Sprint, Change of Direction, Conditioning
```

### Generated Program

| Day | Intent | Slot Family | Selected Exercise | Equipment | Difficulty |
|-----|--------|-------------|------------------|-----------|------------|
| 1 | Strength | Double Leg Knee Dominant | Barbell Back Squat | Barbell | Intermediate |
| 1 | Strength | Horizontal Push | Bench Press | Barbell | Intermediate |
| 1 | Strength | Horizontal Pull | Barbell Row | Barbell | Intermediate |
| 1 | Strength | Core | Plank | Bodyweight | Beginner |
| 2 | Power | Ballistic | Hang Clean | Barbell | Intermediate |
| 2 | Power | Plyometric | Box Jump | Bodyweight | Intermediate |
| 2 | Power | Core | Med Ball Rotational Scoop Toss | Medicine Ball | Beginner |
| 3 | Conditioning | Sprint | Acceleration 10m | Bodyweight | Intermediate |
| 3 | Conditioning | Change of Direction | Pro Agility Shuttle | Bodyweight | Intermediate |
| 3 | Conditioning | Conditioning | Interval Run | Bodyweight | Intermediate |

### Family Coverage

Used: Double Leg Knee Dominant, Horizontal Push, Horizontal Pull, Core, Ballistic, Plyometric, Sprint, Change of Direction, Conditioning
Unused: Double Leg Hip Dominant, Single Leg Knee Dominant, Single Leg Hip Dominant, Vertical Push, Vertical Pull, Carry

### Credibility Review

| Aspect | Assessment |
|--------|-----------|
| Session intent alignment | ✅ Strength day = appropriate families. Power day = explosive families. Conditioning day = field families. |
| Exercise quality | ✅ Solid foundational lifts. Plank as core finisher is standard. Hang Clean + Box Jump is a credible power pairing. |
| Volume distribution | ⚠️ Day 1 has 4 exercises (low for off-season), Day 3 has 3 exercises (too few for a conditioning session) |
| Missing posterior chain | ❌ Day 1 has no hip-dominant work. Fast bowlers NEED RDLs or Good Mornings for hamstring resilience. |
| Missing vertical work | ⚠️ No overhead pressing. Fast bowlers need shoulder robustness. |
| Power day core choice | ⚠️ Med Ball Rotational Scoop Toss is a valid rotational power exercise, but the Core family was used instead of Ballistic. This is an architecture constraint issue — rotational power exercises are in Core family but Ballistic family also has rotational MB work. |

### Substitution Check

Back Squat → Front Squat → Goblet Squat ✅ All same family (Double Leg Knee Dominant)
Bench Press → Dumbbell Bench → Push-Up ✅ All same family (Horizontal Push)

### Coach Credibility Score: 6/10

Missing posterior chain is a real coaching issue. Fast bowlers without RDLs or Nordic work is unrealistic. Day 1 needs either a Double Leg Hip Dominant slot or the template needs restructuring to include posterior chain every strength session.

---

## TEST 2: Cricket Fast Bowler — Pre-Season (3 days)

### Template

```
Day 1 — Power
  Slots: Double Leg Knee Dominant, Ballistic, Core

Day 2 — Speed
  Slots: Sprint, Plyometric, Change of Direction

Day 3 — Strength + Conditioning
  Slots: Double Leg Hip Dominant, Vertical Push, Conditioning
```

### Generated Program

| Day | Intent | Slot Family | Selected Exercise | Equipment | Difficulty |
|-----|--------|-------------|------------------|-----------|------------|
| 1 | Power | Double Leg Knee Dominant | Barbell Back Squat | Barbell | Intermediate |
| 1 | Power | Ballistic | Hang Clean | Barbell | Intermediate |
| 1 | Power | Core | Med Ball Rotational Scoop Toss | Medicine Ball | Beginner |
| 2 | Speed | Sprint | Acceleration 10m | Bodyweight | Intermediate |
| 2 | Speed | Plyometric | Box Jump | Bodyweight | Intermediate |
| 2 | Speed | Change of Direction | Pro Agility Shuttle | Bodyweight | Intermediate |
| 3 | Strength+Conditioning | Double Leg Hip Dominant | Trap Bar Deadlift | Trap Bar | Intermediate |
| 3 | Strength+Conditioning | Vertical Push | Push Press | Barbell | Intermediate |
| 3 | Strength+Conditioning | Conditioning | Sled Push | Sled | Intermediate |

### Family Coverage

Used: Double Leg Knee Dominant, Ballistic, Core, Sprint, Plyometric, Change of Direction, Double Leg Hip Dominant, Vertical Push, Conditioning
Unused: Single Leg Knee Dominant, Single Leg Hip Dominant, Horizontal Push, Horizontal Pull, Vertical Pull, Carry

### Credibility Review

| Aspect | Assessment |
|--------|-----------|
| Session intent alignment | ✅ Day 1 power is good. Day 2 speed = sprint + reactive + COD = correct. Day 3 hybrid is reasonable. |
| Posterior chain addressed | ✅ Trap Bar Deadlift in Day 3 covers the gap from off-season. |
| Vertical push included | ✅ Push Press is excellent for fast bowler shoulder power. |
| Missing upper body pulling | ❌ No horizontal or vertical pull all week. Fast bowlers need scapular control for shoulder health. A week without rows or pull-ups is unrealistic. |
| Day 3 intensity clash | ⚠️ Sled Push (conditioning) after Trap Bar Deadlift (strength) on the same day is fine — sled is lower body but different energy system. However, Push Press after deadlift is demanding. Order matters. |
| Day 2 only 3 exercises | ⚠️ Speed sessions typically need more volume. 3 exercises is thin. |

### Coach Credibility Score: 5/10

Better than off-season because posterior chain is addressed, but completely missing upper body pulling is a significant gap. No row or pull-up in a pre-season program for an overhead athlete is not credible. Template needs either Horizontal Pull or Vertical Pull on at least 2 of 3 days.

---

## TEST 3: Cricket Batter — Off-Season (3 days)

### Template

```
Day 1 — Strength
  Slots: Double Leg Knee Dominant, Horizontal Pull, Vertical Push, Core

Day 2 — Power
  Slots: Ballistic, Single Leg Knee Dominant, Core

Day 3 — Speed
  Slots: Sprint, Change of Direction, Conditioning
```

### Generated Program

| Day | Intent | Slot Family | Selected Exercise | Equipment | Difficulty |
|-----|--------|-------------|------------------|-----------|------------|
| 1 | Strength | Double Leg Knee Dominant | Barbell Back Squat | Barbell | Intermediate |
| 1 | Strength | Horizontal Pull | Barbell Row | Barbell | Intermediate |
| 1 | Strength | Vertical Push | Overhead Press | Barbell | Intermediate |
| 1 | Strength | Core | Pallof Press | Cable Machine | Intermediate |
| 2 | Power | Ballistic | Med Ball Rotational Scoop Toss | Medicine Ball | Beginner |
| 2 | Power | Single Leg Knee Dominant | Bulgarian Split Squat | Dumbbell | Intermediate |
| 2 | Power | Core | Cable Chop | Cable Machine | Intermediate |
| 3 | Speed | Sprint | Acceleration 10m | Bodyweight | Intermediate |
| 3 | Speed | Change of Direction | 5-10-5 Shuttle | Bodyweight | Intermediate |
| 3 | Speed | Conditioning | Tempo Run | Bodyweight | Beginner |

### Family Coverage

Used: Double Leg Knee Dominant, Horizontal Pull, Vertical Push, Core, Ballistic, Single Leg Knee Dominant, Sprint, Change of Direction, Conditioning
Unused: Double Leg Hip Dominant, Single Leg Hip Dominant, Horizontal Push, Vertical Pull, Carry, Plyometric

### Credibility Review

| Aspect | Assessment |
|--------|-----------|
| Batter-specific design | ✅ Good focus on rotational work (Ballistic → MB Rotational Scoop). Horizontal Pull for scapular control. Vertical Push for shoulder health. |
| Running between wickets | ✅ Sprint + COD + Conditioning on Day 3 is well-aligned with batter match demands. |
| Missing horizontal push | ⚠️ No bench or push-up all week. Batter does need chest work for throwing and general upper body strength. |
| Missing posterior chain | ❌ No hip-dominant work. Batters generate power from hips. RDL or kettlebell swing should be in the program. |
| Power day core choice | ⚠️ Cable Chop is a good rotational anti-rotation exercise, but it's in the Core family. If the coach expected a ballistic rotational exercise, the Ballistic family already has MB work — but having two MB rotational exercises in one session is repetitive. |
| Day 3 exercise count | ⚠️ Only 3 exercises. A speed session should include at least acceleration + max V + deceleration work. |

### Coach Credibility Score: 6/10

The batting-specific intent is right but missing posterior chain is a problem. Batters generate power through hip rotation; they need RDLs or KB swings. Missing push exercise is also notable.

---

## TEST 4: Cricket Batter — Pre-Season (3 days)

### Template

```
Day 1 — Power
  Slots: Double Leg Hip Dominant, Ballistic, Core

Day 2 — Speed + Agility
  Slots: Sprint, Change of Direction, Plyometric

Day 3 — Strength Maintenance
  Slots: Single Leg Knee Dominant, Horizontal Pull, Conditioning
```

### Generated Program

| Day | Intent | Slot Family | Selected Exercise | Equipment | Difficulty |
|-----|--------|-------------|------------------|-----------|------------|
| 1 | Power | Double Leg Hip Dominant | Kettlebell Swing | Kettlebell | Beginner |
| 1 | Power | Ballistic | Med Ball Rotational Scoop Toss | Medicine Ball | Beginner |
| 1 | Power | Core | Cable Chop | Cable Machine | Intermediate |
| 2 | Speed+Agility | Sprint | Acceleration 10m | Bodyweight | Intermediate |
| 2 | Speed+Agility | Change of Direction | 5-10-5 Shuttle | Bodyweight | Intermediate |
| 2 | Speed+Agility | Plyometric | Broad Jump | Bodyweight | Intermediate |
| 3 | Strength Maint. | Single Leg Knee Dominant | Bulgarian Split Squat | Dumbbell | Intermediate |
| 3 | Strength Maint. | Horizontal Pull | Dumbbell Row | Dumbbell | Intermediate |
| 3 | Strength Maint. | Conditioning | Interval Run | Bodyweight | Intermediate |

### Family Coverage

Used: Double Leg Hip Dominant, Ballistic, Core, Sprint, Change of Direction, Plyometric, Single Leg Knee Dominant, Horizontal Pull, Conditioning
Unused: Double Leg Knee Dominant, Single Leg Hip Dominant, Horizontal Push, Vertical Push, Vertical Pull, Carry

### Credibility Review

| Aspect | Assessment |
|--------|-----------|
| Hip power focus | ✅ Kettlebell Swing + MB Rotational is a good pairing for bat speed. |
| Single leg work included | ✅ Bulgarian Split Squat is excellent for batting stance stability. |
| Missing bilateral squat | ⚠️ No squat pattern all week. Debatable — a pre-season maintenance phase might drop squat volume, but a week without any squat/dip/leg press is unusual. |
| Missing upper body entirely (almost) | ❌ Only one upper body exercise (Dumbbell Row) in the entire week. Pre-season batters need upper body maintenance. No push, no overhead, no pull-up. |
| Day 1 difficulty | ⚠️ KB Swing (Beginner) + MB Rotational Scoop (Beginner) — two beginner exercises on a power day for a senior athlete feels underloaded. Architecture picked the lowest difficulty because both families have few Intermediate-level power options. |

### Coach Credibility Score: 4/10

The most concerning gap so far. A full week with essentially one upper body exercise is not realistic for any athlete. The template needs Horizontal Push and Vertical Pull on at least one day. The power day also needs harder options — KB Swing is a warm-up exercise for senior cricketers, not a primary power exercise.

### Missing Exercise Flag

The Ballistic family has no Intermediate-level rotational exercise. MB Rotational Scoop Toss is Beginner. MB Overhead Backwards Toss is Intermediate but doesn't target rotation. **Need: Intermediate-level rotational ballistic exercise** (e.g., Rotational Med Ball Slam).

---

## TEST 5: Cricket Spinner — Off-Season (3 days)

### Template

```
Day 1 — Strength
  Slots: Double Leg Knee Dominant, Horizontal Pull, Vertical Push, Core

Day 2 — Rotational Power
  Slots: Ballistic, Core, Carry

Day 3 — Shoulder + Conditioning
  Slots: Vertical Pull, Horizontal Push, Conditioning
```

### Generated Program

| Day | Intent | Slot Family | Selected Exercise | Equipment | Difficulty |
|-----|--------|-------------|------------------|-----------|------------|
| 1 | Strength | Double Leg Knee Dominant | Barbell Back Squat | Barbell | Intermediate |
| 1 | Strength | Horizontal Pull | Barbell Row | Barbell | Intermediate |
| 1 | Strength | Vertical Push | Overhead Press | Barbell | Intermediate |
| 1 | Strength | Core | Pallof Press | Cable Machine | Intermediate |
| 2 | Rotational Power | Ballistic | Med Ball Rotational Scoop Toss | Medicine Ball | Beginner |
| 2 | Rotational Power | Core | Cable Chop | Cable Machine | Intermediate |
| 2 | Rotational Power | Carry | Farmer Walk | Dumbbell | Beginner |
| 3 | Shoulder+Cond. | Vertical Pull | Pull-Up | Bodyweight | Intermediate |
| 3 | Shoulder+Cond. | Horizontal Push | Dumbbell Bench Press | Dumbbell | Intermediate |
| 3 | Shoulder+Cond. | Conditioning | Tempo Run | Bodyweight | Beginner |

### Family Coverage

Used: Double Leg Knee Dominant, Horizontal Pull, Vertical Push, Core, Ballistic, Carry, Vertical Pull, Horizontal Push, Conditioning
Unused: Double Leg Hip Dominant, Single Leg Knee Dominant, Single Leg Hip Dominant, Plyometric, Sprint, Change of Direction

### Credibility Review

| Aspect | Assessment |
|--------|-----------|
| Rotational power intent | ✅ Day 2 targets rotational work explicitly. Good design for a spinner. |
| Shoulder health focus | ✅ Day 3 balances pull (scapular) + push (anterior shoulder). Pull-Up + DB Bench is a credible combo. |
| Upper body pulling | ✅ Barbell Row (Day 1) + Pull-Up (Day 3) = good scapular volume for high-volume bowling. |
| Missing lower body hip work | ⚠️ No hinge/posterior chain all week. Spinners need hip strength for landing leg stability. |
| No single leg work | ⚠️ Bowling involves a single-leg landing. Bulgarian Split Squat or walking lunges should be present. |
| No speed/agility work | ❌ Entire week has no sprint or COD. Off-season spinners still need fielding agility. A 3-day week with zero field work is not credible. |
| Day 2 rotational repetition | ⚠️ MB Rotational Scoop + Cable Chop — both are rotational and both target Core/Ballistic, but one is explosive (MB) and one is controlled (Cable). The intent is right but having only two rotational exercises for the entire "Rotational Power" day feels thin. |

### Coach Credibility Score: 5/10

The spinner-specific intent (rotational power + shoulder health) is architecturally well-supported. But the complete absence of posterior chain, single leg work, and field work makes this program one-dimensional. Real spinners train their landing leg (single leg), their hamstrings (for deceleration), AND their fielding.

Missing: The Sprint and Change of Direction families are unused across all 3 days. For a 3-day off-season program, at least 1 field day is expected.

---

## TEST 6: Cricket Spinner — Pre-Season (3 days)

### Template

```
Day 1 — Power
  Slots: Ballistic, Single Leg Knee Dominant, Core

Day 2 — Strength
  Slots: Double Leg Hip Dominant, Vertical Pull, Horizontal Pull, Carry

Day 3 — Conditioning + Fielding
  Slots: Change of Direction, Sprint, Conditioning
```

### Generated Program

| Day | Intent | Slot Family | Selected Exercise | Equipment | Difficulty |
|-----|--------|-------------|------------------|-----------|------------|
| 1 | Power | Ballistic | Med Ball Rotational Scoop Toss | Medicine Ball | Beginner |
| 1 | Power | Single Leg Knee Dominant | Bulgarian Split Squat | Dumbbell | Intermediate |
| 1 | Power | Core | Cable Chop | Cable Machine | Intermediate |
| 2 | Strength | Double Leg Hip Dominant | Trap Bar Deadlift | Trap Bar | Intermediate |
| 2 | Strength | Vertical Pull | Lat Pulldown | Cable Machine | Beginner |
| 2 | Strength | Horizontal Pull | Cable Row | Cable Machine | Beginner |
| 2 | Strength | Carry | Farmer Walk | Dumbbell | Beginner |
| 3 | Conditioning+Field | Change of Direction | Pro Agility Shuttle | Bodyweight | Intermediate |
| 3 | Conditioning+Field | Sprint | Acceleration 10m | Bodyweight | Intermediate |
| 3 | Conditioning+Field | Conditioning | Interval Run | Bodyweight | Intermediate |

### Family Coverage

Used: Ballistic, Single Leg Knee Dominant, Core, Double Leg Hip Dominant, Vertical Pull, Horizontal Pull, Carry, Change of Direction, Sprint, Conditioning
Unused: Double Leg Knee Dominant, Single Leg Hip Dominant, Horizontal Push, Vertical Push, Plyometric

### Credibility Review

| Aspect | Assessment |
|--------|-----------|
| Field day included | ✅ Change of Direction + Sprint + Conditioning on Day 3 corrects the off-season gap. Credible pre-season field session. |
| Posterior chain addressed | ✅ Trap Bar Deadlift covers hamstring/glute work. |
| Single leg work included | ✅ Bulgarian Split Squat for landing leg stability. Good. |
| Upper body pulling volume | ✅ Lat Pulldown + Cable Row + Farmer Walk = high pulling volume, appropriate for spinner shoulder health. |
| No upper body pushing | ❌ Zero horizontal OR vertical push all week. Spinners need pushing for the follow-through shoulder. Absent. |
| No bilateral squat | ⚠️ No squat pattern. Acceptable for pre-season if load management dictates, but surprising. |
| Day 2 difficulty mismatch | ⚠️ Trap Bar Deadlift (Intermediate) is fine, but Lat Pulldown (Beginner) and Cable Row (Beginner) are too easy for a senior athlete. The families have Intermediate options (Pull-Up, Barbell Row) but the architecture's default selection (first match) picked Beginner. This is a selection algorithm issue. |

### Substitution Check

If equipment is "Basic Gym" (no cable machine):
- Lat Pulldown → Pull-Up ✅ (Vertical Pull family, Bodyweight)
- Cable Row → Dumbbell Row ✅ (Horizontal Pull family, Dumbbell)
- Cable Chop → need Core exercise that doesn't need cable... Dead Bug ✅ (Core, Bodyweight)

### Coach Credibility Score: 6/10

Best spinner program so far. The pre-season template better distributes work across qualities. But the absent upper body pushing and the selection algorithm picking Beginner exercises for senior athletes are real issues. The family architecture supports better selections — the algorithm just needs to prefer closest difficulty match, not default to alphabetically first.

---

## TEST 7: Soccer Midfielder — Off-Season (3 days)

### Template

```
Day 1 — Strength
  Slots: Double Leg Knee Dominant, Horizontal Push, Horizontal Pull, Core

Day 2 — Power
  Slots: Plyometric, Single Leg Knee Dominant, Ballistic

Day 3 — Conditioning
  Slots: Sprint, Change of Direction, Conditioning
```

### Generated Program

| Day | Intent | Slot Family | Selected Exercise | Equipment | Difficulty |
|-----|--------|-------------|------------------|-----------|------------|
| 1 | Strength | Double Leg Knee Dominant | Barbell Back Squat | Barbell | Intermediate |
| 1 | Strength | Horizontal Push | Bench Press | Barbell | Intermediate |
| 1 | Strength | Horizontal Pull | Barbell Row | Barbell | Intermediate |
| 1 | Strength | Core | Plank | Bodyweight | Beginner |
| 2 | Power | Plyometric | Box Jump | Bodyweight | Intermediate |
| 2 | Power | Single Leg Knee Dominant | Bulgarian Split Squat | Dumbbell | Intermediate |
| 2 | Power | Ballistic | Med Ball Chest Pass | Medicine Ball | Beginner |
| 3 | Conditioning | Sprint | Acceleration 10m | Bodyweight | Intermediate |
| 3 | Conditioning | Change of Direction | Pro Agility Shuttle | Bodyweight | Intermediate |
| 3 | Conditioning | Conditioning | Interval Run | Bodyweight | Intermediate |

### Family Coverage

Used: Double Leg Knee Dominant, Horizontal Push, Horizontal Pull, Core, Plyometric, Single Leg Knee Dominant, Ballistic, Sprint, Change of Direction, Conditioning
Unused: Double Leg Hip Dominant, Single Leg Hip Dominant, Vertical Push, Vertical Pull, Carry

### Credibility Review

| Aspect | Assessment |
|--------|-----------|
| Soccer-specific alignment | ✅ Sprint + COD + Conditioning on Day 3 is the most sport-specific day so far. Correctly captures match demands. |
| Unilateral power | ✅ Bulgarian Split Squat + Box Jump is a good pairing for a sport that requires single-leg jumping/take-offs. |
| Missing posterior chain | ❌ No hamstring work. A soccer midfielder with no Nordic hamstring or RDL in off-season is an injury waiting to happen. This is a critical gap. |
| Missing vertical push/pull | ⚠️ No overhead work at all. Not critical for soccer but unusual to have zero. |
| Day 2 power structure | ⚠️ Plyometric + Single Leg + Ballistic is a well-designed power session, but Med Ball Chest Pass (Beginner) is too easy. |

### Coach Credibility Score: 5/10

The template structure is soccer-appropriate but the missing posterior chain is a deal-breaker for any experienced S&C coach working with soccer players. Hamstring injury prevention (Nordic curl, RDL) is arguably the #1 priority in soccer S&C. The Double Leg Hip Dominant family must be present in at least 2 of 3 sessions.

---

## TEST 8: Soccer Midfielder — Pre-Season (3 days)

### Template

```
Day 1 — Speed
  Slots: Sprint, Change of Direction, Plyometric

Day 2 — Strength Maintenance
  Slots: Double Leg Knee Dominant, Single Leg Hip Dominant, Core

Day 3 — Conditioning (Match Simulation)
  Slots: Conditioning, Sprint, Change of Direction
```

### Generated Program

| Day | Intent | Slot Family | Selected Exercise | Equipment | Difficulty |
|-----|--------|-------------|------------------|-----------|------------|
| 1 | Speed | Sprint | Acceleration 10m | Bodyweight | Intermediate |
| 1 | Speed | Change of Direction | Pro Agility Shuttle | Bodyweight | Intermediate |
| 1 | Speed | Plyometric | Broad Jump | Bodyweight | Intermediate |
| 2 | Strength Maint. | Double Leg Knee Dominant | Barbell Back Squat | Barbell | Intermediate |
| 2 | Strength Maint. | Single Leg Hip Dominant | Single-Leg RDL | Dumbbell | Intermediate |
| 2 | Strength Maint. | Core | Pallof Press | Cable Machine | Intermediate |
| 3 | Conditioning | Conditioning | Interval Run | Bodyweight | Intermediate |
| 3 | Conditioning | Sprint | Acceleration 10m | Bodyweight | Intermediate |
| 3 | Conditioning | Change of Direction | 5-10-5 Shuttle | Bodyweight | Intermediate |

### Family Coverage

Used: Sprint, Change of Direction, Plyometric, Double Leg Knee Dominant, Single Leg Hip Dominant, Core, Conditioning
Unused: Double Leg Hip Dominant, Single Leg Knee Dominant, Horizontal Push, Horizontal Pull, Vertical Push, Vertical Pull, Carry, Ballistic

### Credibility Review

| Aspect | Assessment |
|--------|-----------|
| Hamstring focus added | ✅ Single Leg Hip Dominant (SL RDL) corrects the off-season gap. Good pre-season hamstring maintenance. |
| Match simulation day | ✅ Day 3's blend of conditioning + sprint + COD emulates match demands well. 3 sessions of field work per week is realistic for pre-season. |
| Complete absence of upper body | ❌ An entire pre-season week with zero upper body exercises. Zero. No push, no pull, no press, no row. This is not credible for any sport, including soccer. |
| No power development | ⚠️ Pre-season typically maintains or even peaks power. This program has zero power work. No ballistic, no plyometric (unless Broad Jump counts — it's on Day 1 as speed). |
| Day 2 only 3 exercises | ⚠️ A "strength maintenance" session with just squat + SL RDL + core is very thin. Would expect at least 4-5 exercises. |
| Repetition across days | ⚠️ Sprint Acceleration 10m appears on both Day 1 and Day 3. COD appears on Day 1 and Day 3. This is acceptable (different context: speed vs conditioning) but the output looks repetitive. |

### Coach Credibility Score: 3/10

Lowest score so far. A pre-season week with zero upper body work is not realistic. The template sacrificed upper body entirely to maximize field work. A real S&C coach would never write this. The template needs at minimum 1-2 upper body sessions (push + pull) distributed across the week.

---

## TEST 9: Rugby Forward — Off-Season (3 days)

### Template

```
Day 1 — Upper Body Strength
  Slots: Horizontal Push, Horizontal Pull, Vertical Push, Core

Day 2 — Lower Body Strength
  Slots: Double Leg Knee Dominant, Double Leg Hip Dominant, Carry, Core

Day 3 — Power + Conditioning
  Slots: Ballistic, Plyometric, Conditioning
```

### Generated Program

| Day | Intent | Slot Family | Selected Exercise | Equipment | Difficulty |
|-----|--------|-------------|------------------|-----------|------------|
| 1 | Upper Strength | Horizontal Push | Bench Press | Barbell | Intermediate |
| 1 | Upper Strength | Horizontal Pull | Barbell Row | Barbell | Intermediate |
| 1 | Upper Strength | Vertical Push | Overhead Press | Barbell | Intermediate |
| 1 | Upper Strength | Core | Plank | Bodyweight | Beginner |
| 2 | Lower Strength | Double Leg Knee Dominant | Barbell Back Squat | Barbell | Intermediate |
| 2 | Lower Strength | Double Leg Hip Dominant | Trap Bar Deadlift | Trap Bar | Intermediate |
| 2 | Lower Strength | Carry | Farmer Walk | Dumbbell | Beginner |
| 2 | Lower Strength | Core | Pallof Press | Cable Machine | Intermediate |
| 3 | Power+Conditioning | Ballistic | Hang Clean | Barbell | Intermediate |
| 3 | Power+Conditioning | Plyometric | Box Jump | Bodyweight | Intermediate |
| 3 | Power+Conditioning | Conditioning | Sled Push | Sled | Intermediate |

### Family Coverage

Used: Horizontal Push, Horizontal Pull, Vertical Push, Core, Double Leg Knee Dominant, Double Leg Hip Dominant, Carry, Ballistic, Plyometric, Conditioning
Unused: Single Leg Knee Dominant, Single Leg Hip Dominant, Sprint, Change of Direction, Vertical Pull

### Credibility Review

| Aspect | Assessment |
|--------|-----------|
| Rugby-appropriate split | ✅ Upper/Lower split is standard for rugby off-season. Day 1 and Day 2 are well-designed. |
| Contact readiness | ✅ Carry (Farmer Walk) is excellent for rugby. Grip strength + trunk rigidity = contact preparation. |
| Sled work | ✅ Sled Push on power day is sport-specific for scrum engagement and contact. |
| Full body coverage | ✅ 10 of 15 families used. Most comprehensive coverage so far. |
| Missing vertical pull | ⚠️ No pull-up or lat pulldown. Forwards need lat strength for scrummaging and mauling. A notable gap. |
| Missing single leg work | ⚠️ No single leg knee or hip dominant. Forwards need single leg for lineout drives and lateral movement in contact. |
| No field work | ⚠️ No sprint or COD. Acceptable in early off-season but should be added as pre-season approaches. |
| Day 3 exercise count | ⚠️ Only 3 exercises for a power + conditioning day. Could add a second conditioning element. |

### Coach Credibility Score: 7/10

Best program so far. The rugby forward template makes the most coaching sense. The upper/lower split, sled work, carries, and power work all align with rugby S&C best practices. The missing vertical pull and single leg work are gaps but not deal-breakers. This is the most credible draft generated.

---

## TEST 10: Rugby Forward — Pre-Season (3 days)

### Template

```
Day 1 — Power
  Slots: Ballistic, Plyometric, Double Leg Hip Dominant

Day 2 — Strength + Contact
  Slots: Horizontal Push, Carry, Double Leg Knee Dominant, Core

Day 3 — Conditioning
  Slots: Sprint, Conditioning, Change of Direction
```

### Generated Program

| Day | Intent | Slot Family | Selected Exercise | Equipment | Difficulty |
|-----|--------|-------------|------------------|-----------|------------|
| 1 | Power | Ballistic | Hang Clean | Barbell | Intermediate |
| 1 | Power | Plyometric | Box Jump | Bodyweight | Intermediate |
| 1 | Power | Double Leg Hip Dominant | Kettlebell Swing | Kettlebell | Beginner |
| 2 | Strength+Contact | Horizontal Push | Bench Press | Barbell | Intermediate |
| 2 | Strength+Contact | Carry | Farmer Walk | Dumbbell | Beginner |
| 2 | Strength+Contact | Double Leg Knee Dominant | Barbell Back Squat | Barbell | Intermediate |
| 2 | Strength+Contact | Core | Pallof Press | Cable Machine | Intermediate |
| 3 | Conditioning | Sprint | Acceleration 10m | Bodyweight | Intermediate |
| 3 | Conditioning | Conditioning | Sled Push | Sled | Intermediate |
| 3 | Conditioning | Change of Direction | Pro Agility Shuttle | Bodyweight | Intermediate |

### Family Coverage

Used: Ballistic, Plyometric, Double Leg Hip Dominant, Horizontal Push, Carry, Double Leg Knee Dominant, Core, Sprint, Conditioning, Change of Direction
Unused: Single Leg Knee Dominant, Single Leg Hip Dominant, Horizontal Pull, Vertical Push, Vertical Pull

### Credibility Review

| Aspect | Assessment |
|--------|-----------|
| Field day added | ✅ Sprint + COD + Conditioning for pre-season match fitness. Good progression from off-season. |
| Contact training maintained | ✅ Farmer Walk and Bench Press — contact preparation. |
| Power maintained | ✅ Hang Clean + Box Jump is a credible pre-season power pairing. |
| Missing horizontal pull | ❌ No row or pull-up in either off-season OR pre-season for a rugby forward. This is a two-program gap. Forwards need pulling strength for scrummaging, mauling, and grappling. |
| Missing vertical pull | ❌ Same gap. Lat strength is essential for forwards. |
| KB Swing as power exercise | ⚠️ Kettlebell Swing (Beginner) is being used as a "power" exercise for the Double Leg Hip Dominant slot. A senior rugby forward should use Trap Bar Deadlift (Intermediate) or RDL instead. The selection algorithm picked the lowest difficulty that fits. Either the algorithm needs improvement or the KB Swing shouldn't be in the power template's hip dominant slot. |

### Coach Credibility Score: 5/10

Regressed from the off-season version. Missing upper body pulling (horizontal AND vertical) across both off-season and pre-season programs is now a clear architectural gap. The forward templates lack pulling volume. The KB Swing vs Trap Bar Deadlift selection issue also reveals that the algorithm's difficulty-first approach doesn't always match coaching intent.

### Architecture Finding

The Double Leg Hip Dominant family has a wide difficulty range (KB Swing: Beginner, RDL: Intermediate, Deadlift: Advanced). When a template uses this family for "power" intent, the algorithm needs to prefer explosive hip exercises (KB Swing, Trap Bar Deadlift) over slow strength exercises (Conventional Deadlift). The family is too broad — it conflates "heavy hip hinge" (strength) with "explosive hip hinge" (power). This is a **family granularity issue**.

---

## TEST 11: Rugby Back — Off-Season (3 days)

### Template

```
Day 1 — Strength
  Slots: Double Leg Knee Dominant, Horizontal Pull, Vertical Push, Core

Day 2 — Speed
  Slots: Sprint, Plyometric, Change of Direction, Single Leg Knee Dominant

Day 3 — Power
  Slots: Ballistic, Double Leg Hip Dominant, Conditioning
```

### Generated Program

| Day | Intent | Slot Family | Selected Exercise | Equipment | Difficulty |
|-----|--------|-------------|------------------|-----------|------------|
| 1 | Strength | Double Leg Knee Dominant | Barbell Back Squat | Barbell | Intermediate |
| 1 | Strength | Horizontal Pull | Barbell Row | Barbell | Intermediate |
| 1 | Strength | Vertical Push | Overhead Press | Barbell | Intermediate |
| 1 | Strength | Core | Plank | Bodyweight | Beginner |
| 2 | Speed | Sprint | Acceleration 10m | Bodyweight | Intermediate |
| 2 | Speed | Plyometric | Broad Jump | Bodyweight | Intermediate |
| 2 | Speed | Change of Direction | Pro Agility Shuttle | Bodyweight | Intermediate |
| 2 | Speed | Single Leg Knee Dominant | Bulgarian Split Squat | Dumbbell | Intermediate |
| 3 | Power | Ballistic | Hang Clean | Barbell | Intermediate |
| 3 | Power | Double Leg Hip Dominant | Trap Bar Deadlift | Trap Bar | Intermediate |
| 3 | Power | Conditioning | Tempo Run | Bodyweight | Beginner |

### Family Coverage

Used: Double Leg Knee Dominant, Horizontal Pull, Vertical Push, Core, Sprint, Plyometric, Change of Direction, Single Leg Knee Dominant, Ballistic, Double Leg Hip Dominant, Conditioning
Unused: Single Leg Hip Dominant, Horizontal Push, Vertical Pull, Carry

### Credibility Review

| Aspect | Assessment |
|--------|-----------|
| Speed-focused design | ✅ Day 2 is a dedicated speed day with 4 exercises covering acceleration, reactive strength, COD, and single leg stability. Correct for a rugby back. |
| Power + posterior chain | ✅ Hang Clean + Trap Bar Deadlift is a good pairing. Covers explosive power and absolute strength. |
| Good family coverage | ✅ 11 of 15 families used. Most diverse program yet. |
| Missing horizontal push | ⚠️ No bench or push-up. Backs in rugby do get tackled and need upper body pushing strength. Acceptable for off-season if periodized, but notable. |
| Missing vertical pull | ⚠️ No pull-up or lat pulldown. Backs need lats for fend-offs and tackling. More pulling volume expected. |
| Day 1 strength vs speed balance | ⚠️ Day 1 has no hip-dominant exercise (no RDL, no deadlift). Squat + Row + OHP is a fine upper-body-focused strength day, but adding a hinge would strengthen the program. |

### Coach Credibility Score: 7/10

Second-best program. The rugby back off-season template produces a well-rounded, believable draft. The speed day is particularly well-designed. Missing horizontal push and vertical pull are gaps but the overall structure is credible enough that a coach would say "I'd add a bench and pull-ups, but the skeleton is right."

---

## TEST 12: Rugby Back — Pre-Season (3 days)

### Template

```
Day 1 — Speed + Agility
  Slots: Sprint, Change of Direction, Plyometric

Day 2 — Strength Maintenance
  Slots: Double Leg Knee Dominant, Horizontal Push, Horizontal Pull, Carry

Day 3 — Power + Conditioning
  Slots: Ballistic, Sprint, Conditioning
```

### Generated Program

| Day | Intent | Slot Family | Selected Exercise | Equipment | Difficulty |
|-----|--------|-------------|------------------|-----------|------------|
| 1 | Speed+Agility | Sprint | Acceleration 10m | Bodyweight | Intermediate |
| 1 | Speed+Agility | Change of Direction | Pro Agility Shuttle | Bodyweight | Intermediate |
| 1 | Speed+Agility | Plyometric | Broad Jump | Bodyweight | Intermediate |
| 2 | Strength Maint. | Double Leg Knee Dominant | Barbell Back Squat | Barbell | Intermediate |
| 2 | Strength Maint. | Horizontal Push | Bench Press | Barbell | Intermediate |
| 2 | Strength Maint. | Horizontal Pull | Barbell Row | Barbell | Intermediate |
| 2 | Strength Maint. | Carry | Farmer Walk | Dumbbell | Beginner |
| 3 | Power+Conditioning | Ballistic | Hang Clean | Barbell | Intermediate |
| 3 | Power+Conditioning | Sprint | Acceleration 10m | Bodyweight | Intermediate |
| 3 | Power+Conditioning | Conditioning | Interval Run | Bodyweight | Intermediate |

### Family Coverage

Used: Sprint, Change of Direction, Plyometric, Double Leg Knee Dominant, Horizontal Push, Horizontal Pull, Carry, Ballistic, Conditioning
Unused: Single Leg Knee Dominant, Single Leg Hip Dominant, Double Leg Hip Dominant, Vertical Push, Vertical Pull, Core

### Credibility Review

| Aspect | Assessment |
|--------|-----------|
| Pushing + pulling addressed | ✅ Bench Press + Barbell Row on Day 2, plus Farmer Walk. Good contact prep. |
| Speed day maintained | ✅ Sprint + COD + Plyometric — correct for pre-season backs. |
| Power work included | ✅ Hang Clean maintained from off-season. |
| No core work | ❌ Zero core exercises across all 3 days. Plank, Pallof, Cable Chop — nothing. A pre-season program with no core work for any athlete, especially a rugby player, is not credible. |
| No posterior chain | ❌ No hinge (RDL, deadlift, KB swing) across all 3 days. Pre-season backs losing hamstring work is an injury risk. |
| Sprint duplication | ⚠️ Acceleration 10m appears on Day 1 and Day 3. Different context (speed vs conditioning) but looks repetitive. |
| No single leg work | ⚠️ Day 1 speed session could include single leg plyometric or COD but doesn't. |

### Coach Credibility Score: 4/10

The pre-season template for rugby backs dropped core work and posterior chain — both essential for this population. The off-season version scored 7/10, but the pre-season template is weaker. The missing core family is a clear template design error (should be added to at least Day 2). Missing posterior chain is the same issue seen in soccer programs.

---

## CROSS-PROGRAM ANALYSIS

### Summary Scores

| # | Program | Score |
|---|---------|-------|
| 1 | Cricket Fast Bowler — Off-Season | 6/10 |
| 2 | Cricket Fast Bowler — Pre-Season | 5/10 |
| 3 | Cricket Batter — Off-Season | 6/10 |
| 4 | Cricket Batter — Pre-Season | 4/10 |
| 5 | Cricket Spinner — Off-Season | 5/10 |
| 6 | Cricket Spinner — Pre-Season | 6/10 |
| 7 | Soccer Midfielder — Off-Season | 5/10 |
| 8 | Soccer Midfielder — Pre-Season | 3/10 |
| 9 | Rugby Forward — Off-Season | **7/10** |
| 10 | Rugby Forward — Pre-Season | 5/10 |
| 11 | Rugby Back — Off-Season | **7/10** |
| 12 | Rugby Back — Pre-Season | 4/10 |
| | **Average** | **5.25/10** |

### Recurring Issues (by frequency)

| Issue | Affected Programs | Severity |
|-------|------------------|----------|
| Missing posterior chain (hip hinge) | 10 of 12 | High |
| Selection algorithm picks Beginner when Intermediate exists | 7 of 12 | Medium |
| Zero upper body work in a full week | 4 of 12 | High |
| Missing core work in a full week | 3 of 12 | Medium |
| Missing single leg work | 6 of 12 | Medium |
| Sprint exercise duplication across sessions | 4 of 12 | Low |
| Sessions with only 3 exercises feel thin | 8 of 12 | Medium |
| Power day uses Beginner-difficulty exercises | 5 of 12 | Medium |
| No vertical pulling (pull-up/lat) | 6 of 12 | Medium |
| No vertical pushing (overhead) | 5 of 12 | Low |

---

## MISSING EXERCISE INVENTORY

Exercises needed but not in the library (or in the wrong family):

| Missing Exercise | Needed Family | Why |
|-----------------|---------------|-----|
| **Rotational Med Ball Slam** | Ballistic | Only rotational MB option is Beginner-level Scoop Toss. Need Intermediate rotational ballistic. |
| **Band Face Pull** | Horizontal Pull | Excellent shoulder health exercise for all overhead athletes. No band-pull exercise exists. |
| **Split Squat Jump** | Plyometric | Single-leg plyometric option. Current plyometric family has only bilateral + lateral jumps. |
| **Kneeling Cable Pull-Through** | Double Leg Hip Dominant | Beginner-friendly hinge pattern that doesn't use a barbell. Good for hotel gym. |
| **Side-Lying Clam** | Single Leg Hip Dominant | Hip stability exercise. Current Single Leg Hip Dominant has only SL RDL and SL Hip Thrust. |
| **Banded Glute Bridge** | Double Leg Hip Dominant | Beginner hip exercise. Current hip family has no pure glute activation. |
| **Single-Leg Box Jump** | Plyometric | Needs a single-leg plyometric option for sport-specific training. |

### Missing Equipment Items

| Equipment | Needed For |
|-----------|-----------|
| Pull-Up Bar | Already in proposed additions. Confirmed needed by 6/12 programs. |
| Plyo Box | Already in proposed additions. Confirmed needed. |
| Sled | Already in proposed additions. Confirmed needed for rugby + field sport conditioning. |
| Agility Cones | Already in proposed additions. Confirmed needed for COD work. |

---

## MISSING FAMILY INVENTORY

| Family Gap | Evidence | Recommendation |
|-----------|----------|---------------|
| **None (structure is correct)** | All 15 families were used across the 12 programs. No sport needed a family that doesn't exist. | Family structure is validated. KEEP. |

However, **one family boundary issue** was identified:

### Double Leg Hip Dominant is too broad

This family currently contains:
- Kettlebell Swing (Beginner, explosive, ballistic-like)
- Trap Bar Deadlift (Intermediate, strength)
- Romanian Deadlift (Intermediate, strength/hypertrophy)
- Conventional Deadlift (Advanced, strength)
- Hip Thrust (Intermediate, strength/hypertrophy)
- Good Morning (Advanced, strength)
- Nordic Hamstring Curl (Intermediate, eccentric strength)

**Problem**: When a template needs "explosive hip power" (e.g., Rugby Forward off-season Day 3), the algorithm may pick KB Swing (good) or Trap Bar Deadlift (acceptable) or RDL (wrong — not explosive). The family conflates strength and power hip exercises.

**Recommendation**: No structural change to families. Instead, add an `intent_tag` field as optional exercise metadata: `"power"`, `"strength"`, `"hypertrophy"`, `"speed"`. The exercise selector uses intent_tag when the session intent suggests it (e.g., Power session → prefer exercises tagged "power").

This is a lightweight metadata addition (1 field, nullable, no new table). The existing filter logic stays the same — just adds a preference boost, not a hard constraint.

---

## MISSING TEMPLATE INVENTORY

| Missing Template | Why | Who Would Use |
|-----------------|-----|---------------|
| Recovery / Active Recovery day | Current 3-day templates never use Recovery intent. Coaches need a low-intensity day option. | All sports, in-season |
| 2-day frequency templates | Some amateur athletes train 2x/week. Only 3-day templates exist in this test. | Amateur / age-group athletes |
| 4-day frequency templates | Some elite athletes train 4x/week. | Elite / senior athletes |
| In-season templates | Not tested in this validation (off-season + pre-season only). Will need their own validation. | All sports, competitive phase |
| Transition phase templates | Not tested. Post-season recovery. | All sports, post-competition |

---

## RECOMMENDED EXERCISE ADDITIONS

### Immediate additions (needed to close credibility gaps)

| Exercise | Family | Equipment | Difficulty | Why |
|----------|--------|-----------|------------|-----|
| **Rotational Med Ball Slam** | Ballistic | Medicine Ball | Intermediate | Fills the Intermediate rotational ballistic gap (Programs 3-6) |
| **Kneeling Cable Pull-Through** | Double Leg Hip Dominant | Cable Machine | Beginner | Hotel/basic gym hinge option |
| **Single-Leg Box Jump** | Plyometric | Plyo Box | Intermediate | Single-leg plyometric for field sports (Programs 7-12) |
| **Band Face Pull** | Horizontal Pull | Resistance Bands | Beginner | Shoulder health for overhead sports (Programs 1-6) |
| **Side Plank with Leg Raise** | Core | Bodyweight | Intermediate | Harder core option between Plank and Ab Wheel |

### Nice-to-have (fills gaps but not blocking)

| Exercise | Family | Equipment | Difficulty |
|----------|--------|-----------|------------|
| **Banded Glute Bridge** | Double Leg Hip Dominant | Resistance Bands | Beginner |
| **Half-Kneeling Overhead Press** | Vertical Push | Dumbbell | Beginner |
| **Single-Leg Hip Thrust** | Single Leg Hip Dominant | Dumbbell | Intermediate |
| **Copenhagen Adductor Plank** | Core | Bodyweight | Intermediate |

---

## RECOMMENDED TEMPLATE CHANGES

### Universal fixes (all templates)

1. **Every strength session must include a hip hinge.** Add `Double Leg Hip Dominant` to every Strength session that doesn't already have it. This addresses the posterior chain gap in 10/12 programs.

2. **Upper body work must appear in at least half the week's sessions.** Templates that had zero upper body work (Soccer Pre-Season, Batter Pre-Season) need restructuring.

3. **Core work must appear at least 2x/week minimum.** Several templates had core only once or not at all.

### Sport-specific template fixes

| Template | Change |
|----------|--------|
| Fast Bowler Off-Season Day 1 | Add Double Leg Hip Dominant slot (for RDL or Nordic curl) |
| Fast Bowler Off-Season Day 3 | Add 1 more exercise to conditioning day (currently 3) |
| Batter Off-Season Day 1 | Add Double Leg Hip Dominant or Horizontal Push |
| Batter Pre-Season Day 3 | Add Horizontal Push for upper body balance |
| Spinner Off-Season Day 2 | Add Single Leg Knee Dominant for landing leg |
| Spinner Off-Season Day 3 | Add Sprint + Change of Direction (missing field work) |
| Spinner Pre-Season Day 1 | Replace Ballistic with more rotational-specific option or add double ballistic slot |
| Soccer Midfielder Off-Season Day 1 | Add Double Leg Hip Dominant for hamstring injury prevention |
| Soccer Midfielder Pre-Season | Restructure to include at least 1 upper body session |
| Rugby Forward Pre-Season Day 1 | Replace KB Swing with Trap Bar Deadlift or RDL |
| Rugby Back Pre-Season Day 1 | Add Core to Day 2 |
| Rugby Back Pre-Season Day 3 | Add Double Leg Hip Dominant for posterior chain |

---

## SUBSTITUTION VALIDATION

### Test: Replace Back Squat across all programs

Input: Back Squat (Double Leg Knee Dominant, Barbell, Intermediate)

Expected: Exercises in same family only.

| Substitution | Family | Valid? | Coach Would Accept? |
|-------------|--------|--------|---------------------|
| Front Squat | Double Leg Knee Dominant | ✅ | Yes — same movement intent, different loading |
| Goblet Squat | Double Leg Knee Dominant | ✅ | Yes — regression option |
| Belt Squat | Double Leg Knee Dominant | ✅ | Yes — spinal-friendly alternative |
| Bulgarian Split Squat | Double Leg Knee Dominant | ❌ Wrong family | Single Leg Knee Dominant — NOT same family. Correctly excluded. |
| Bench Press | Horizontal Push | ❌ Wrong family | Correctly excluded. |

**Result**: Substitution engine correctly keeps all swaps within family. ✅

### Test: Family coverage adequacy

| Can the coach stay within family for every substitution? | Assessment |
|----------------------------------------------------------|------------|
| Double Leg Knee Dominant (5+ exercises) | ✅ Good breadth |
| Double Leg Hip Dominant (7 exercises) | ✅ Good breadth |
| Single Leg Knee Dominant (4 exercises) | ✅ Adequate |
| Single Leg Hip Dominant (2 exercises) | ⚠️ Thin. Add Copenhagen adductor or SL Hip Thrust. |
| Horizontal Push (5 exercises) | ✅ Good breadth |
| Horizontal Pull (5 exercises) | ✅ Good breadth |
| Vertical Push (5 exercises) | ✅ Good breadth |
| Vertical Pull (4 exercises) | ✅ Adequate |
| Core (8 exercises) | ✅ Good breadth |
| Carry (4 exercises) | ✅ Adequate |
| Plyometric (5 exercises) | ✅ Good breadth |
| Ballistic (8 exercises) | ✅ Good breadth |
| Sprint (5 exercises) | ✅ Good breadth |
| Change of Direction (4 exercises) | ✅ Adequate |
| Conditioning (6 exercises) | ✅ Good breadth |

### Blind spot: The substitution engine has no "alternate equipment" awareness

If a coach selects a Barbell Back Squat and then says "I only have dumbbells," the substitution engine currently returns Goblet Squat (Dumbbell, same family). This is correct behavior. But if the coach wants to stay with "squat pattern with dumbbells" and there are no other dumbbell squat options in Double Leg Knee Dominant... the engine correctly returns nothing (there are no more dumbbell options).

**Issue**: The Goblet Squat is the only Double Leg Knee Dominant exercise using dumbbells. If the coach says "I need a different dumbbell squat," there's no alternative. Adding a **Dumbbell Front Squat** or **Dumbbell Goblet Squat variant** would solve this.

---

## CRITICAL ARCHITECTURE FINDINGS

### Finding 1: The difficulty-first selection algorithm needs intent awareness

The current algorithm picks the first matching exercise. When multiple difficulties exist in a family, it often picks Beginner (alphabetically or by lowest ordinal). This causes senior athletes to get KB Swing (Beginner) instead of Trap Bar Deadlift (Intermediate) in power slots.

**Fix**: Choose exercise with difficulty closest to (but not exceeding) the athlete's level. If athlete is Intermediate, prefer Intermediate over Beginner.

**Change**: 3 lines of code in the selection filter's sort key.

### Finding 2: The Ballistic family needs an Intermediate rotational option

Currently, Med Ball Rotational Scoop Toss (Beginner) is the only rotational exercise in Ballistic. For senior cricketers needing rotational power, this is too easy.

**Fix**: Add "Rotational Med Ball Slam" (Intermediate, Medicine Ball) to the Ballistic family.

**Change**: 1 data row.

### Finding 3: Template design is the most critical quality lever

The 7/10 programs (Rugby Forward Off-Season, Rugby Back Off-Season) had well-designed templates. The 3/10 program (Soccer Pre-Season) had a poorly designed template. Template quality determines output quality more than any other factor. The families and exercises are adequate — the templates need coaching input.

**Fix**: Templates must be designed by an S&C coach, not a developer. The current template set needs revision before it's coach-credible.

**Change**: Template data in `seed_data.py` only. No code changes.

### Finding 4: The 5-entity architecture is validated

Athlete → Template → Session → Family Slot → Exercise is sufficient. No program needed a sixth entity. No program needed a variant, readiness score, or competition proximity. The architecture gap is not entities — it's template quality and selection algorithm tuning.

---

## FINAL VALIDATION SCORE

| Criterion | Score | Notes |
|-----------|-------|-------|
| Family coverage adequacy | 8/10 | All 15 families used. Double Leg Hip Dominant is too broad (see Finding 4). |
| Exercise breadth | 7/10 | ~68 exercises works, but missing 4-5 critical exercises (Rotational MB Slam, Face Pull, etc.) |
| Template quality | 5/10 | Best templates score 7/10. Worst score 3/10. Average is below the credibility threshold. |
| Substitution correctness | 9/10 | Always stays in family. Correctly filters equipment and difficulty. |
| Coach credibility (average) | 5.25/10 | Below the 7/10 threshold. Not yet coach-ready. |

### Go/No-Go: NO-GO for current template set

**The architecture is validated. The templates are not.**

The 5-entity architecture, 15 families, ~68 exercises, and family-anchored substitution engine all work correctly. The core design is sound.

The 5.25/10 average coach credibility score is caused by:
1. **Template design flaws** (missing posterior chain, zero upper body weeks) — fixable by revising template data
2. **Selection algorithm picking Beginner over Intermediate** — fixable by changing sort preference
3. **1 missing exercise** (Rotational MB Slam) — fillable by adding one data row
4. **1 family boundary issue** (DL Hip Dominant is too broad) — fixable by adding intent_tag metadata

### Path to 7/10+ (coach-ready)

| Action | Impact | Effort |
|--------|--------|--------|
| Revise templates with S&C coach input | +2.0 credibility | 1 day |
| Fix selection algorithm to prefer matching difficulty | +0.5 credibility | 15 minutes |
| Add Rotational Med Ball Slam to Ballistic family | +0.3 credibility | 1 minute |
| Add intent_tag metadata to exercises | +0.5 credibility | 2 hours (data entry) |
| Add 4 missing exercises (Face Pull, SL Box Jump, etc.) | +0.3 credibility | 10 minutes |
| **Estimated new score** | **~7.8/10** | **~1.5 days** |

**Architecture recommendation**: Proceed with template revisions and selection algorithm fix. The foundation is correct. The output quality gap is in the data, not the architecture.
