# FORGE Program Generation Rulebook V1

> Exactly how FORGE generates a coach-credible session from a blueprint.
> This is the master specification. A developer can build the entire generator from this document alone.
> No software architecture. No AI. No scoring systems. Deterministic rules only.

---

## SECTION 1: Session Generation Sequence

The generation engine follows exactly 8 steps, in order. No step is skipped. No step is reordered.

### Step 1: Select Blueprint

Input: Athlete profile (sport, training age, season phase, injury status, goal).
Output: One blueprint from the 14 in FORGE_BLUEPRINT_SELECTION_GUIDE_V1.md.

Selection is deterministic. Use the selection decision tree from the guide:
- Injury active → Return to Sport (12)
- Season phase determines filter
- Training age narrows within phase
- Sport type selects the final blueprint (court → Court Sport AD, contact → Rugby Off-Season, etc.)

### Step 2: Determine Athlete Level

Three levels only. No sub-levels.

| Level | Definition | Max Difficulty | Max Load % |
|-------|-----------|----------------|------------|
| **Beginner** | Training age < 1 year OR inconsistent technique (<80% reps at target depth/speed) | L2 | 60-70% 1RM estimated |
| **Intermediate** | Training age 1-3 years AND consistent technique AND no movement red flags | L3 | 75-85% 1RM |
| **Advanced** | Training age 3+ years AND consistent technique AND established strength base (≥1.5x BW squat M, ≥1.2x BW squat F) | L4-L5 | 85-95% 1RM |

### Step 3: Determine Equipment Profile

Four equipment profiles. These are fixed categories — no mixing.

| Profile | Available Equipment | Constraints |
|---------|-------------------|-------------|
| **Field Only** | Bodyweight, bands, med balls, cones, field space | No barbells. No dumbbells. No racks. No machines. |
| **Basic Gym** | Barbell, squat rack, flat bench, dumbbells (up to 40kg), cable station | No specialty bars. No chains. No bands beyond light/medium. No sled. |
| **Commercial Gym** | Full dumbbell set (5-50kg), cables, machines, barbells, racks, leg press | No specialty bars (safety squat, trap bar) unless verified. No strongman implements. |
| **Elite Facility** | Full access: barbells, specialty bars, dumbbells, cables, machines, plyo boxes, hurdles, med balls, sleds, strongman implements, turf | No constraints beyond safety. |

### Step 4: Resolve Blueprint Slot Order

The blueprint's slot_order is a flat list of family codes. This step expands it into the final ordered list of slots.

Rules:
- Mandatory families are always included
- Optional families are included if they do not cause the session to exceed 6 total slots
- When optional families compete for the same slot position, rotate weekly (not per-session)
- Slot order is final after this step — it does not change per session within a block

### Step 5: Select Exercise Per Slot

For each slot in the resolved slot_order, select exactly one exercise.

Selection follows Section 2 rules: difficulty-matching first, then equipment match, then rotation rules.

### Step 6: Validate Against Section 9 Credibility Checks

Run all credibility checks. If any check fails, return to Step 5 and replace the violating exercise.

Maximum 3 retries per slot. On 3rd failure, substitute the family (per Section 7 rules).

### Step 7: Assign Load, Sets, Reps, Rest

For each selected exercise, assign:
- **Sets**: blueprint-dependent (3-5 sets for strength, 2-5 for power, 2-3 for accessories)
- **Reps**: within the family's target range (Section 6)
- **Load**: based on athlete level and progression history (Section 6)
- **Rest**: based on block type (power: 2-5 min, strength: 2-4 min, accessory: 60-90s)

### Step 8: Generate Final Session

Output: Ordered list of exercises with assigned sets, reps, load, rest, and coaching cues.

The session is now ready for delivery. No further validation is required — Step 6 validated it.

---

## SECTION 2: Exercise Selection Rules

### 2.1 Universal Selection Order

For every slot, select the exercise using this priority order:

1. **Difficulty match**: Exercise difficulty ≤ athlete level (L1-L5 → Beginner-Advanced)
2. **Equipment match**: Exercise equipment ∈ available equipment profile
3. **Competency**: If exercise has been performed in the last 4 weeks with good technique, prefer it over a new exercise
4. **Rotation**: If all else is equal, select the exercise least recently used in this slot
5. **Fallback**: If no exercise matches criteria 1-4, substitute to a lower difficulty within the same family

### 2.2 Per-Family Selection Priorities

Each family has a prioritised list. The generator selects the highest-priority exercise that matches athlete level and equipment. Lower priority is selected only if higher priority is unavailable.

#### DLKD (Bilateral Knee Dominant)

| Priority | Exercise | Diff | Equipment | Notes |
|----------|----------|------|-----------|-------|
| 1 | Back Squat | L3 | Basic Gym+ | Default choice when available and athlete can brace |
| 2 | Front Squat | L3 | Basic Gym+ | Preferred when thoracic mobility limits back squat |
| 3 | Goblet Squat | L1 | Basic Gym+ | Beginner default, warm-up, or equipment-limited |
| 4 | Safety Bar Squat | L3 | Elite | Shoulder health limitation |
| 5 | Box Squat | L3 | Basic Gym+ | When hip mechanics need patterning |
| 6 | Belt Squat | L3 | Elite | Spinal loading concern |
| 7 | Bodyweight Squat | L1 | Field Only | No equipment available |
| 8 | Leg Press | L2 | Commercial+ | When spinal loading must be minimised |

#### DLHD (Bilateral Hip Dominant)

| Priority | Exercise | Diff | Equipment | Notes |
|----------|----------|------|-----------|-------|
| 1 | Conventional Deadlift | L3 | Basic Gym+ | Default for strength-focused blocks |
| 2 | Romanian Deadlift | L2 | Basic Gym+ | Preferred for hamstring emphasis |
| 3 | Sumo Deadlift | L3 | Basic Gym+ | When anatomy or mobility favours wider stance |
| 4 | Trap Bar Deadlift | L2 | Elite | Lower back friendly alternative |
| 5 | Kettlebell Swing | L1 | Field Only | Power-focused hip hinge, minimal equipment |
| 6 | Good Morning | L3 | Basic Gym+ | Supplementary hamstring/spinal erector work |
| 7 | Glute Bridge (Loaded) | L1 | Field Only | No equipment or beginner posterior chain |
| 8 | Hip Thrust | L2 | Basic Gym+ | Glute emphasis over hamstring |

#### SLKD (Single Leg Knee Dominant)

| Priority | Exercise | Diff | Equipment | Notes |
|----------|----------|------|-----------|-------|
| 1 | Bulgarian Split Squat | L2 | Basic Gym+ | Highest unilateral loading potential |
| 2 | Walking Lunge | L1 | Field Only | Beginner/field friendly |
| 3 | Reverse Lunge | L1 | Field Only | Less knee stress than forward lunge |
| 4 | Step-Up | L1 | Basic Gym+ | Height adjustable, low skill demand |
| 5 | Lateral Lunge | L2 | Field Only | Frontal plane variation |
| 6 | Split Squat (rear foot on floor) | L1 | Basic Gym+ | Regression from Bulgarian |
| 7 | Single Leg Press | L2 | Commercial+ | Controlled unilateral loading |
| 8 | Curtsy Lunge | L2 | Field Only | Multi-planar variation |

#### SLHD (Single Leg Hip Dominant)

| Priority | Exercise | Diff | Equipment | Notes |
|----------|----------|------|-----------|-------|
| 1 | Single Leg RDL | L2 | Basic Gym+ | Default unilateral hinge |
| 2 | Single Leg Romanian Deadlift (banded) | L1 | Field Only | Beginner regression |
| 3 | Single Leg Glute Bridge | L1 | Field Only | No equipment alternative |
| 4 | Nordic Curl | L2 | Field Only | Hamstring focus, partner/strap required |
| 5 | Single Leg Hip Thrust | L1 | Basic Gym+ | Glute emphasis |
| 6 | Reversed Nordic (Single Leg) | L2 | Field Only | Quad emphasis, eccentric control |

#### HPush (Horizontal Push)

| Priority | Exercise | Diff | Equipment | Notes |
|----------|----------|------|-----------|-------|
| 1 | Barbell Bench Press | L2 | Basic Gym+ | Default horizontal push |
| 2 | Dumbbell Bench Press | L2 | Basic Gym+ | Preferred when unilateral focus or shoulder issues |
| 3 | Incline Dumbbell Press | L2 | Basic Gym+ | Upper chest emphasis |
| 4 | Push-Up | L1 | Field Only | Beginner/field friendly, scales with load |
| 5 | Floor Press | L2 | Basic Gym+ | Shoulder safe variation |
| 6 | Incline Barbell Press | L2 | Basic Gym+ | Upper chest, heavier loading |
| 7 | Dip (weighted) | L2 | Commercial+ | Lower chest emphasis |
| 8 | Machine Chest Press | L1 | Commercial+ | Controlled alternative |

#### HPull (Horizontal Pull)

| Priority | Exercise | Diff | Equipment | Notes |
|----------|----------|------|-----------|-------|
| 1 | Barbell Row | L2 | Basic Gym+ | Default horizontal pull, highest loading |
| 2 | Dumbbell Row (single arm) | L1 | Basic Gym+ | Unilateral, allows greater ROM |
| 3 | Cable Row | L1 | Commercial+ | Constant tension, easy load adjustment |
| 4 | Inverted Row | L1 | Field Only | Bodyweight, beginner friendly |
| 5 | Prone Row (on incline bench) | L1 | Basic Gym+ | Spinal support variation |
| 6 | T-Bar Row | L2 | Commercial+ | Heavy loading alternative |
| 7 | Pendlay Row | L2 | Basic Gym+ | Explosive row variant |
| 8 | Meadows Row | L3 | Commercial+ | Advanced unilateral variation |

#### VPush (Vertical Push)

| Priority | Exercise | Diff | Equipment | Notes |
|----------|----------|------|-----------|-------|
| 1 | Overhead Press (barbell) | L2 | Basic Gym+ | Default vertical push |
| 2 | Dumbbell Overhead Press | L2 | Basic Gym+ | Unilateral accommodation |
| 3 | Push Press | L2 | Basic Gym+ | Power-focused vertical push |
| 4 | Seated Dumbbell Press | L2 | Basic Gym+ | Spinal support |
| 5 | Arnold Press | L2 | Basic Gym+ | Rotational element |
| 6 | Landmine Press | L1 | Field Only | Shoulder safe, beginner friendly |
| 7 | Handstand Push-Up (progression) | L2 | Field Only | Advanced bodyweight option |
| 8 | Machine Shoulder Press | L1 | Commercial+ | Controlled alternative |

#### VPull (Vertical Pull)

| Priority | Exercise | Diff | Equipment | Notes |
|----------|----------|------|-----------|-------|
| 1 | Pull-Up | L2 | Basic Gym+ | Default vertical pull |
| 2 | Chin-Up | L2 | Basic Gym+ | More bicep involvement |
| 3 | Lat Pulldown | L1 | Commercial+ | Beginner/regression |
| 4 | Neutral Grip Pull-Up | L2 | Basic Gym+ | Shoulder friendly |
| 5 | Banded Pull-Up | L1 | Field Only | Assisted progression |
| 6 | Negative Pull-Up | L1 | Field Only | Eccentric-focused progression |
| 7 | Wide Grip Pulldown | L1 | Commercial+ | Lat width emphasis |
| 8 | Straight Arm Pulldown | L1 | Commercial+ | Lat isolation |

#### Ball (Ballistic / Explosive)

| Priority | Exercise | Diff | Equipment | Notes |
|----------|----------|------|-----------|-------|
| 1 | Power Clean | L4 | Basic Gym+ | Default for advanced athletes with Olympic lift proficiency |
| 2 | Hang Clean | L3 | Basic Gym+ | Preferred over full clean — lower skill demand |
| 3 | Clean Pull | L2 | Basic Gym+ | RFD focus without catch complexity |
| 4 | Med Ball Slam | L1 | Field Only | Beginner/field friendly ballistic |
| 5 | Med Ball Overhead Throw | L1 | Field Only | Upper body power |
| 6 | Med Ball Chest Pass | L1 | Field Only | Horizontal power |
| 7 | KB Swing | L1 | Field Only | Hip power, minimal equipment |
| 8 | Push Press | L2 | Basic Gym+ | Upper body power |
| 9 | Snatch Pull | L3 | Basic Gym+ | Advanced RFD |
| 10 | Jump Squat | L1 | Field Only | Lower body power, bodyweight only |

#### Plyo (Plyometric)

| Priority | Exercise | Diff | Equipment | Notes |
|----------|----------|------|-----------|-------|
| 1 | Countermovement Jump | L1 | Field Only | Default plyometric, minimal equipment |
| 2 | Broad Jump | L1 | Field Only | Horizontal power assessment |
| 3 | Box Jump (low box, high intent) | L1 | Basic Gym+ | Reactive strength, box ≤ knee height |
| 4 | Pogo Jump | L1 | Field Only | Reactive strength, minimal ground contact |
| 5 | Hurdle Hop | L2 | Basic Gym+ | Advanced reactive, requires depth perception |
| 6 | Lateral Bound | L2 | Field Only | Frontal plane plyometric |
| 7 | Depth Jump | L4 | Basic Gym+ | Advanced reactive, requires strength base |
| 8 | Single Leg Hop | L2 | Field Only | Unilateral plyometric |
| 9 | Clap Push-Up | L2 | Field Only | Upper body plyometric |
| 10 | Box Jump (tall box) | L1 | Basic Gym+ | NOT for power — requires landing control, low eccentric load |

#### Sprint/COD (Sprint / Change of Direction)

| Priority | Exercise | Diff | Equipment | Notes |
|----------|----------|------|-----------|-------|
| 1 | 10m Acceleration | L2 | Field Only | Default speed quality |
| 2 | 20m Sprint | L2 | Field Only | Max velocity focus |
| 3 | 5-0-5 COD | L2 | Field Only | Change of direction assessment |
| 4 | Pro Agility | L2 | Field Only | Multi-directional COD |
| 5 | L-Drill | L2 | Field Only | Multi-directional agility |
| 6 | Resisted Sprint (sled) | L2 | Elite | Acceleration overload |
| 7 | 30m Flying Sprint | L3 | Field Only | Max velocity, requires run-up space |
| 8 | Illinois Agility | L2 | Field Only | COD with multiple direction changes |
| 9 | W-Drill | L2 | Field Only | Sport-specific COD pattern |
| 10 | Sprint with Defensive Slide | L2 | Field Only | Sport-specific transitional speed |

#### Rot (Rotational)

| Priority | Exercise | Diff | Equipment | Notes |
|----------|----------|------|-----------|-------|
| 1 | Med Ball Rotational Throw | L1 | Field Only | Rotational power |
| 2 | Cable Rotation (half-kneeling) | L1 | Commercial+ | Controlled rotational strength |
| 3 | Pallof Press | L1 | Field Only | Anti-rotation stability |
| 4 | Landmine Rotation | L1 | Basic Gym+ | Rotational strength with load progression |
| 5 | Med Ball Side Throw | L1 | Field Only | Lateral rotational power |
| 6 | Band Rotational Pull | L1 | Field Only | Portable rotation option |
| 7 | Cable Chop (high-to-low) | L1 | Commercial+ | Diagonal rotational pattern |
| 8 | Turkish Get-Up | L2 | Basic Gym+ | Full body rotational stability |

#### Carry (Loaded Carry)

| Priority | Exercise | Diff | Equipment | Notes |
|----------|----------|------|-----------|-------|
| 1 | Farmer Carry | L1 | Basic Gym+ | Default carry, grip + core + shoulder stability |
| 2 | Suitcase Carry | L1 | Basic Gym+ | Anti-lateral flexion emphasis |
| 3 | Rack Carry | L1 | Basic Gym+ | Upper back + grip |
| 4 | Overhead Carry | L1 | Basic Gym+ | Shoulder stability + core |
| 5 | Waiter Carry | L1 | Basic Gym+ | Shoulder + scapular control |
| 6 | Goblet Carry | L1 | Field Only | Field-friendly option |
| 7 | Bear Hug Carry | L1 | Basic Gym+ | Full body stability |
| 8 | Zercher Carry | L1 | Basic Gym+ | Core + hip flexor loading |

#### Core (Core / Anti-Movement)

| Priority | Exercise | Diff | Equipment | Notes |
|----------|----------|------|-----------|-------|
| 1 | Plank | L1 | Field Only | Anti-extension baseline |
| 2 | Dead Bug | L1 | Field Only | Anti-extension + coordination |
| 3 | Bird Dog | L1 | Field Only | Anti-rotation + stability |
| 4 | Pallof Press | L1 | Field Only | Anti-rotation |
| 5 | Roll-Out (ab wheel or barbell) | L2 | Basic Gym+ | Advanced anti-extension |
| 6 | Side Plank | L1 | Field Only | Anti-lateral flexion |
| 7 | Cable Chop | L1 | Commercial+ | Rotational stability |
| 8 | Hanging Leg Raise | L2 | Basic Gym+ | Advanced anti-extension with hip flexion |

#### Acc/Prehab (Accessory / Prehab)

| Priority | Exercise | Diff | Equipment | Notes |
|----------|----------|------|-----------|-------|
| 1 | Band Pull-Apart | L1 | Field Only | Scapular retraction, shoulder health |
| 2 | Face Pull | L1 | Commercial+ | External rotation + scapular |
| 3 | Glute Bridge | L1 | Field Only | Glute activation, hip stability |
| 4 | Band Lateral Walk | L1 | Field Only | Glute med activation |
| 5 | Band External Rotation | L1 | Field Only | Rotator cuff health |
| 6 | Y-T-W-L Raise | L1 | Field Only | Scapular control |
| 7 | Tib Raise | L1 | Field Only | Tibialis anterior, shin splint prevention |
| 8 | Copenhagen Adduction | L1 | Field Only | Adductor/groin health |
| 9 | Prone Hamstring Hold | L1 | Field Only | Hamstring tendon health |
| 10 | Calf Raise | L1 | Field Only | Calf/Achilles health |

### 2.3 Difficulty Level Mapping

| Athlete Level | Max Exercise Diff | Examples |
|---------------|-------------------|----------|
| Beginner | L2 | Goblet Squat, Push-Up, DB Row, Plank |
| Intermediate | L3 | Back Squat, Bench Press, Barbell Row, Pull-Up |
| Advanced | L5 | Power Clean, Depth Jump, Pendlay Row, Weighted Pull-Up |

### 2.4 Equipment Fallback Chain

If the selected exercise requires unavailable equipment, substitute using this chain within the same family:

1. Find the same exercise at a neighbouring difficulty (L+1 or L-1) that uses available equipment
2. If not found, move to the next priority exercise in the family table (Section 2.2)
3. If no exercise in the family matches available equipment, apply Section 7 (Substitution Rules)

---

## SECTION 3: Session Composition Rules

### 3.1 Universal Rules (Every Session)

| Rule | Detail |
|------|--------|
| Every session must include a warm-up block (≥10 min). | Warm-up must include movement patterns specific to the main work. |
| Every session must include a core exercise. | Core must be placed last (or in the closing block). |
| Every session must include prehab/exercise. | At minimum: band pull-apart or face pull. |
| No session exceeds 90 minutes total. | Warm-up (15-25) + Main (35-55) + Closing (10-15). |
| No session has more than 3 strength exercises. | Beyond 3, quality drops and session time balloons. |
| Power must precede strength. | Non-negotiable. If both are present, power is first. |
| Conditioning must never precede power or strength. | Conditioning is always last. |

### 3.2 Minimum Session Composition by Blueprint Type

#### Full Body Strength
- 1 DLKD (mandatory)
- 1 DLHD (mandatory)
- 1 HPush (mandatory)
- 1 HPull (mandatory)
- 1 Core (mandatory)
- 1 Acc/Prehab (mandatory)

#### Strength + Power
- 1 Ball (mandatory, explosive)
- 1 DLKD (mandatory)
- 1 DLHD (mandatory)
- 1 HPush (mandatory)
- 1 HPull (optional — rotate in)
- 1 Core (mandatory)

#### Strength + Conditioning
- 1 DLKD or DLHD (mandatory — both if possible)
- 1 HPush (mandatory)
- 1 HPull (mandatory)
- 1 conditioning finisher (mandatory)
- 1 Core (mandatory)

#### Power + Speed
- 1 Sprint/COD (mandatory, in warm-up or activation)
- 1 Plyo (mandatory)
- 1 Ball (mandatory)
- 1 Core (mandatory)

#### Upper / Lower Split — Lower Day
- 1 DLKD (mandatory)
- 1 DLHD (mandatory)
- 1 Core (mandatory)
- 1 Carry (optional)

#### Upper / Lower Split — Upper Day
- 1 HPush (mandatory)
- 1 HPull (mandatory)
- 1 VPush (optional)
- 1 VPull (optional)
- 1 Acc/Prehab (mandatory)
- 1 Core (mandatory)

#### Power Maintenance
- 1 Ball (mandatory)
- 1 Plyo (mandatory)
- 1 Core (mandatory)

#### Youth Foundation (U14-U20)
- 1 DLKD or DLHD (mandatory)
- 1 HPush (mandatory)
- 1 HPull (mandatory)
- 1 Core (mandatory)
- 1 movement skill (mandatory, in warm-up)
- No power block (circuit-based strength instead)
- No 1RM testing

#### Court Sport AD
- 1 Sprint/COD (mandatory, in activation)
- 1 Plyo (mandatory)
- 1 SLKD (mandatory)
- 1 HPull (mandatory)
- 1 Rot (mandatory)
- 1 Core (mandatory)

#### Rugby Off-Season
- 1 Ball (mandatory)
- 1 DLKD (mandatory)
- 1 HPush (mandatory)
- 1 HPull (mandatory)
- 1 Carry (mandatory)
- 1 Neck prep (mandatory, in warm-up)
- 1 Core (mandatory)
- 1 Conditioning finisher (mandatory)

#### Sprint Development
- 1 Sprint/COD (mandatory, in activation — technical)
- 1 Plyo (mandatory)
- 1 DLHD (mandatory)
- 1 Core (mandatory)

#### Hypertrophy / Mass Accrual
- 1 compound lower (mandatory)
- 1 compound upper push (mandatory)
- 1 compound upper pull (mandatory)
- 2+ isolation exercises (mandatory)
- 1 Core (mandatory)
- No power block (unless in power-hypertrophy hybrid phase)

#### Return to Sport (Foundation)
- 1 Acc/Prehab injury-specific (mandatory)
- 1 regressed DLKD or DLHD (mandatory)
- 1 Core (mandatory, controlled only)
- 0 explosive exercises
- All exercises pain-free

#### Deload / Active Recovery
- 1 Warm-up (mandatory — mobility emphasis)
- All other blocks optional
- If strength included: 50-60% 1RM, 2-3 RIR
- No power
- No conditioning

#### Mixed Modal (GPP)
- Rotates across 3 session types (Strength, Power, Conditioning emphasis)
- All 15 families touched at least 1-2x per week
- Core in every session
- Power before strength in any session with both

### 3.3 Session Volume Limits

| Block Type | Min Sets | Max Sets | Min Reps | Max Reps |
|------------|----------|----------|----------|----------|
| Power | 2 | 5 | 2 | 6 |
| Strength (primary) | 3 | 5 | 3 | 8 |
| Strength (secondary) | 2 | 4 | 6 | 12 |
| Accessory | 2 | 3 | 10 | 20 |
| Core | 2 | 4 | 8 | 20 |
| Plyometric (ground contacts) | — | 30 total | — | — |

---

## SECTION 4: Family Balance Rules

### 4.1 Push/Pull Balance

| Rule | Detail |
|------|--------|
| **Horizontal push : horizontal pull ratio** | Maximum 1:1. Pull may exceed push. Push must never exceed pull across the week. |
| **Per session** | If HPush is included, HPull must also be included (same session). |
| **Vertical push : vertical pull ratio** | 1:1 target. If VPush is included, VPull should be included within the same microcycle. |
| **Total push : total pull** | Across a training week, total pulling volume (HPull + VPull) must equal or exceed total pushing volume (HPush + VPush). |

### 4.2 Knee/Hip Balance

| Rule | Detail |
|------|--------|
| **DLKD : DLHD ratio** | 1:1 across the training week. No quality is sacrificed for the other. |
| **Per session minimum** | At least one knee-dominant AND one hip-dominant exercise per full body session. |
| **Sprint/COD emphasis weeks** | Hip-dominant may exceed knee-dominant by up to 2:1 (sprint athletes need more posterior chain). |
| **Court sport emphasis weeks** | Knee-dominant may exceed hip-dominant by up to 2:1 (court athletes need more single-leg knee work). |

### 4.3 Anterior/Posterior Balance

| Rule | Detail |
|------|--------|
| **Posterior chain minimum** | Every session must contain at least one posterior chain exercise (DLHD, SLHD, or horizontal pull). |
| **Posterior : anterior volume ratio** | Across the training week, posterior chain volume must equal or exceed anterior chain volume. |
| **Quad-dominant sessions** | If a session is quad-dominant (DLKD primary, front squat emphasis), posterior chain volume must be at least 60% of anterior chain in the same session. |

### 4.4 Core Balance

| Rule | Detail |
|------|--------|
| **Anti-extension** | Must appear in every session (plank, dead bug, roll-out). |
| **Anti-rotation** | Must appear at least 2x/week (pallof press, bird dog with reach, cable anti-rotation). |
| **Anti-lateral flexion** | Must appear at least 1x/week (side plank, suitcase carry). |
| **Flexion work** | Optional only. Crunches and sit-ups are not core training — they are warm-up or accessory level. |
| **Core is always last** | Never placed before power or strength in any session. |

### 4.5 Rotational Balance

| Rule | Detail |
|------|--------|
| **Rotational sport athletes** | Rotational work minimum 1x/week. Includes med ball throws, cable rotation, landmine rotation. |
| **Linear-dominant athletes** | Rotational work minimum 1x/2 weeks. Enforced for shoulders health, not just sport-specificity. |
| **Anti-rotation before rotation** | Anti-rotation exercises (pallof press, half-kneeling chop) must be mastered before active rotational work. |
| **Progression** | Stable surface → half-kneeling → standing → single-leg → loaded rotation. |

### 4.6 Single-Leg Balance

| Rule | Detail |
|------|--------|
| **Field and court sport athletes** | Single-leg work minimum 1:1 ratio with bilateral work across the week. |
| **Sprint athletes** | Single-leg work minimum 1:2 ratio with bilateral work. |
| **Non-field/non-court athletes** | Single-leg work at least 1x/week for asymmetry exposure. |
| **Single-leg progression** | Stable surface, bodyweight → stable surface, loaded → unstable surface, bodyweight → dynamic (lunge walks, step-ups with knee drive). |

---

## SECTION 5: Exercise Rotation Rules

### 5.1 When Exercises Rotate

| Trigger | Action |
|---------|--------|
| Every 4-6 weeks (end of block) | Rotate 1-2 exercises per movement family. Never rotate all exercises at once. |
| Athlete reports joint pain during exercise | Rotate to a mechanically different variation within the same family immediately. |
| Athlete misses reps on the same exercise for 3 consecutive sessions | Rotate to a variation. Do not grind on a stale exercise. |
| Exercise no longer produces improvement over 4 weeks (plateau confirmed) | Rotate within the same family. |

### 5.2 When Exercises Stay

| Condition | Action |
|-----------|--------|
| Exercise is progressing (load or reps increasing per schedule) | Keep. Do not change. |
| Exercise is new (<2 weeks in rotation) | Keep for minimum 4 weeks total. |
| Exercise is a primary compound (squat, deadlift, bench) and progressing | Keep up to 8 weeks. Primary compounds change slower than accessories. |
| Athlete is preparing for competition and the exercise is part of the peaking plan | Keep through the taper. Do not change during peaking. |

### 5.3 When Progression Overrides Rotation

If the athlete is on a scheduled progression (weeks 1-4 of a 4-week block), progression rules take priority over rotation rules.

Example:
- Week 3 of 4: Goblet Squat is progressing (weight increasing per schedule)
- Rotation rule says it's been 3 weeks, consider rotating
- Progression rule overrides: keep Goblet Squat until the block ends

### 5.4 Exercise Replacement Rules

When an exercise is rotated out and needs replacement:

1. Select from the same family (Section 2.2 priority list)
2. Same difficulty level or one level higher (if athlete is ready to progress)
3. Not the same exercise that was just rotated out (minimum 8 weeks before returning to a previously rotated exercise)
4. Prefer the exercise in the family that has been unused the longest

### 5.5 Rotation Examples

| Scenario | Action |
|----------|--------|
| 4 weeks of Back Squat in DLKD slot | Rotate to Front Squat or Safety Bar Squat for weeks 5-8. Then return to Back Squat. |
| 6 weeks of Barbell Bench Press in HPush slot | Rotate to Dumbbell Bench Press for weeks 7-10. Then return to Barbell Bench Press. |
| 8 weeks of Conventional Deadlift in DLHD slot | Rotate to Trap Bar Deadlift or RDL for weeks 9-12. |
| Accessory rotation (faster) | Rotate accessories every 3-4 weeks. Band Pull-Aparts → Face Pulls → Y-T-W-L. |
| Primary compound with consistent progress | Do NOT rotate. Keep for up to 8 weeks or until progress stalls. |

---

## SECTION 6: Progression Rules

### 6.1 Strength Progression

The universal model: add reps first, then add load. Never add load when rep target has not been met.

| Step | Action | Example |
|------|--------|---------|
| 1 | Hit the top of the rep range for all sets | 3x8 at 100kg |
| 2 | Add 2-5% load | 3x8 at 105kg (adjust down to 5 reps if needed) |
| 3 | Build back to the top of the rep range | Work up to 3x8 at 105kg |
| 4 | Repeat step 2-3 | Continue until 3-5% load increase is no longer achievable within 3 sessions |

**Load increase amounts:**
- Primary compound lifts: 2.5-5 kg (upper body), 2.5-5 kg (lower body)
- Secondary lifts: 2.5-5 kg
- Dumbbell work: 1-2.5 kg per hand
- Bodyweight work: add reps (1-2 per session), then add load (vest or belt)
- When rep target is hit consistently for 2 sessions: increase load

**RIR targets by session type:**
- Strength primary sets: 1-3 RIR (reps in reserve)
- Secondary/accessory: 2-3 RIR
- Peaking phase: 0-1 RIR (touching failure, not exceeding)
- Technique/return-to-sport: 3-4 RIR

### 6.2 Power Progression

| Step | Action | Example |
|------|--------|---------|
| 1 | Increase velocity (move the same load faster) | Med ball chest pass at 5kg, throw as far as possible |
| 2 | Increase load while maintaining velocity | Med ball at 7kg, maintain throw distance |
| 3 | Increase complexity of movement | CMJ → hurdle hop → depth jump |
| 4 | Decrease ground contact time (plyometrics) | Pogo → single-leg pogo → reactive bound |

**Power progression rules:**
- Load is secondary to velocity. If load increase slows the movement, reduce load.
- Ground contacts increase before load for plyometrics.
- Jump height / throw distance must be measured. If it decreases, stop the session for that exercise.
- Power work is never taken to failure. Stop when velocity drops >10% from best rep.

### 6.3 Accessory Progression

Accessories use faster progression than primary strength work.

| Step | Action |
|------|--------|
| 1 | Increase reps within the target range (10-20) |
| 2 | Increase sets (2 → 3) |
| 3 | Decrease rest (90s → 60s) |
| 4 | Increase load (smallest increment available) |
| 5 | Change exercise (progression within family) |
| 6 | Repeat |

### 6.4 Bodyweight Progression

For bodyweight exercises (push-ups, pull-ups, inverted rows, etc.):

| Level | Push-Up Progression | Pull-Up Progression |
|-------|--------------------|--------------------|
| 1 | Incline push-up | Banded pull-up or lat pulldown |
| 2 | Full push-up (floor) | Negative pull-up |
| 3 | Close-grip / diamond push-up | Full pull-up (1-3 reps) |
| 4 | Decline push-up | Weighted pull-up (light) |
| 5 | Weighted push-up | Weighted pull-up (heavy) |

Progression: hit 3x12 at current level → advance to next level. If 3x12 cannot be achieved within 4 weeks, regress one level and increase frequency.

### 6.5 Conditioning Progression

| Phase | Action | Example |
|-------|--------|---------|
| 1 | Increase volume (distance or time) | 4x400m → 5x400m |
| 2 | Decrease rest | 2 min rest → 1:45 rest |
| 3 | Increase intensity (pace) | 5:00/km → 4:45/km |
| 4 | Change modality | Steady state → intervals → sport-specific patterns |

### 6.6 Deload Triggers

A deload is triggered when ANY of the following conditions are met:

| Condition | Action |
|-----------|--------|
| 4-6 consecutive weeks of training completed | Schedule a deload week (volume -40-60%, intensity maintained) |
| RPE of primary lift >9 for 2 consecutive sessions | Deload (CNS fatigue indicator) |
| Velocity loss >20% on warm-up set compared to previous week | Deload (neuromuscular fatigue) |
| Athlete reports sleep quality <6h for 3+ nights | Deload or reduce volume (non-training stress) |
| Competition week | If in-season, volume -20-30% (not a full deload — preserve neural readiness) |

---

## SECTION 7: Substitution Rules

### 7.1 The Substitution Priority

When an exercise cannot be used, substitute in this priority order:

1. **Same family** — Choose the next available exercise from the family's priority list (Section 2.2)
2. **Same intent** — If no exercise in the family is available, choose an exercise from a different family that produces the same training effect (Section 7.2)
3. **Same equipment** — If intent cannot be matched, choose any exercise that uses available equipment
4. **Emergency fallback** — If no viable exercise exists, skip the slot and flag it as a coaching gap

### 7.2 Intent-Based Substitution Families

When same-family substitution is not possible, substitute within the same intent category:

| Intent Category | Primary Families | Substitute Families |
|----------------|-----------------|-------------------|
| **Lower body power** | Plyo, Ball | Sprint/COD (short max efforts), Jump variations from DLKD |
| **Upper body power** | Ball (med ball throws), Plyo (clap push-ups) | VPush (push press at low weight, high velocity) |
| **Lower body strength (quad)** | DLKD, SLKD | Leg press, Step-ups, Hack squat |
| **Lower body strength (posterior)** | DLHD, SLHD | Hip thrust, Good morning, KB swing |
| **Upper body push** | HPush, VPush | Dips, Push-ups, Landmine press |
| **Upper body pull** | HPull, VPull | Band rows, Inverted row (any stance), Cable face pulls |
| **Core (anterior)** | Core (plank, dead bug, roll-out) | Carry variations, Pallof press |
| **Core (rotational)** | Rot, Core (anti-rotation) | Cable chop, Landmine rotation, Med ball throws |
| **Conditioning** | Sprint/COD, Carry, Plyo (low) | Any exercise at low load, high rep, short rest |

### 7.3 Equipment Loss Substitution

| Equipment Lost | Substitution Strategy | Example |
|---------------|---------------------|---------|
| Barbells | Switch to dumbbell + bodyweight families. All DLKD → SLKD or bodyweight squat. All DLHD → SLHD or KB swing. | Back Squat → Bulgarian Split Squat |
| Squat rack | Replace DLKD with SLKD (dumbbells) or bodyweight variants. | Back Squat → Goblet Squat → Walking Lunge |
| All weights | Field Only protocol. Bodyweight + bands + med balls only. | All strength → bodyweight progressions, band work |
| Cables | Replace cable exercises with band or dumbbell alternatives. | Cable Row → DB Row, Face Pull → Band Pull-Apart |
| Plyo boxes | Replace box jumps with ground-based jumps. | Box Jump → Broad Jump or CMJ |
| Med balls | Replace with throws using available weight (sandbag, plate). | Med Ball Throw → Slams with any available object |

### 7.4 Injury Modification Substitution

| Injury | Modify | Avoid | Preferred Substitution |
|--------|--------|-------|----------------------|
| Low back pain | All axial-loaded exercises | Back squat, deadlift, barbell row | Goblet squat, trap bar DL, chest-supported row, belt squat |
| Knee pain (patellar) | Reduce knee flexion load | Deep squat, lunge, leg extension | Hip-dominant work, shallow squats, step-ups (low box) |
| Knee pain (meniscus) | Avoid loaded rotation | Loaded rotation, deep knee flexion under load | Single-leg work (stable), hip thrust, sled push |
| Shoulder (impingement) | Reduce overhead/wide grip | Overhead press, wide pull-down, dips | Neutral grip pull-up, landmine press, floor press |
| Shoulder (labrum) | Avoid extreme ROM | Behind neck, deep dips, very wide grip | DB bench (neutral grip), narrow pull-up, face pulls |
| Hamstring strain | Reduce eccentric load/high speed | RDL, sprinting, Nordic curl | Hip thrust, leg curl (concentric only), SLDL light |
| Achilles/calf | Reduce eccentric loading | Pogo, depth jump, running sprint | Cycling, seated calf raise, CMJ (minimal bounce) |
| Concussion | No impact, no heavy load | Any plyometric, heavy compound, sprint | Light band work, low-load mobility, breathing drills |

### 7.5 Travel Substitution

| Scenario | Protocol |
|----------|----------|
| Athlete has access to hotel gym (basic) | Use Basic Gym profile. All exercises default to dumbbell and machine variants. Maintain family order. |
| Athlete has access to field only (no gym) | Use Field Only profile. Bodyweight progressions, bands, and field-based conditioning. Matches the intent of the original session (power day → jump/sprint; strength day → bodyweight circuits). |
| Athlete has no equipment | Use Field Only profile at L1 difficulty. Do not attempt to match load — match intent and volume. |

### 7.6 Crowded Gym Substitution

| Problem | Solution |
|---------|----------|
| Squat rack occupied | Substitute DLKD with next priority exercise that does not require a rack (goblet squat, Bulgarian split squat, leg press) |
| Bench occupied | Substitute HPush with next priority exercise that does not require a bench (floor press, push-up, dumbbell floor press) |
| Cable station occupied | Substitute cable exercises with band or dumbbell variants |
| Deadlift platform occupied | Substitute DLHD with RDL (barbell or dumbbell) or trap bar deadlift |

### 7.7 Exercise Occupied Substitution

If the exact exercise selected is being used by another athlete (team training):

1. Select the same exercise with the next available implement (same weight or closest available)
2. If no implement available, substitute within the same family (Section 2.2, next priority)
3. Maintain the same approximate load if possible

---

## SECTION 8: Session Flow Rules

### 8.1 The Universal Block Order

```
1.  Warm-up (mobility, soft tissue prep, low-level activation)
2.  Activation (glute activation, scapular control, movement prep)
3.  ┌─────────────────────────────────────────────────┐
    │  Power (explosive, ballistic, plyometric)        │ ← Fresh CNS required
    │  ──────────────────────────────────────────────  │
    │  Strength (compound, primary lifts)              │
    │  ──────────────────────────────────────────────  │
    │  Accessory (isolation, supplementary)            │
    └─────────────────────────────────────────────────┘
4.  Core (anti-movement, stability)
5.  Conditioning (finisher — optional per blueprint)
6.  Cool-down (brief static stretching, 5 min max)
```

### 8.2 Invariant Rules (Never Broken)

| Rule | Detail |
|------|--------|
| Power is never after strength | If both are in the session, power is always first. |
| Core is always last | Core after accessory, after conditioning. Never before power or strength. |
| Warm-up comes before any loaded work | Nothing loaded happens in the first 10 minutes of any session. |
| Activation is never after power | Activation primes the nervous system. Power IS the application. |
| Conditioning never before power or strength | If conditioning is included, it is the final training stimulus. |
| Power exercises are never superset | Standalone only. Full recovery between sets. |

### 8.3 Block Exceptions (Conditional)

| Exception | When Allowed | Blueprints |
|-----------|-------------|------------|
| Sprint/COD in activation | Sprint mechanics are technical/coaching, not conditioning. Only sub-max intensity, technique focus. | Power + Speed (4), Sprint Development (10) |
| No power block | Hypertrophy, return-to-sport, youth foundation, deload. | Hypertrophy (11), Return to Sport (12), Youth (7), Deload (13) |
| Conditioning before strength | NEVER. No exception exists. | — |
| Core before accessory | Only in tri-set structure (core is the third element of a set with two strength exercises). | Tri-set variant (not a standalone blueprint) |
| Power in activation block | Never. Power is a separate block with full recovery. | — |

### 8.4 Session Duration by Blueprint

| Blueprint | Typical Duration | Notes |
|-----------|-----------------|-------|
| Full Body Strength | 60-75 min | 3-4 exercises main work |
| Strength + Power | 75-90 min | Power need full recovery (3-5 min rest) |
| Strength + Conditioning | 60-75 min | Shorter rest, conditioning finisher adds time |
| Power + Speed | 60-75 min | Low volume, full recovery |
| Upper / Lower Split | 60-75 min per session | Higher volume per region |
| Power Maintenance | 40-50 min | Minimal volume, maintenance only |
| Youth Foundation | 50-60 min | Circuit format, includes games |
| Court Sport AD | 60-75 min | COD + power + strength + rotational |
| Rugby Off-Season | 75-90 min | Most comprehensive, highest volume |
| Sprint Development | 60-75 min | Speed session + gym work |
| Hypertrophy / Mass | 60-90 min | Higher volume, short rest |
| Return to Sport | 50-60 min | Low intensity, high control |
| Deload / Recovery | 35-50 min | Minimal stimulus, mobility focus |
| Mixed Modal (GPP) | 60-75 min | Varies by session type |

---

## SECTION 9: Coaching Credibility Checks

### 9.1 Pre-Validation Checklist

Before a session is considered valid, run these checks in order. If any check fails, the session must be adjusted.

| # | Check | Pass Condition | Failure Action |
|---|-------|---------------|----------------|
| 1 | Posterior chain present | At least one of: DLHD, SLHD, HPull, Ball (if KB Swing or Clean) | Add DLHD or HPull to session |
| 2 | Push/pull balanced | HPush count ≤ HPull count in session | Switch one push to pull or add a pull |
| 3 | Core included | At least one Core exercise | Add core (last block) |
| 4 | Appropriate difficulty | All exercises ≤ athlete max difficulty (Beginner ≤ L2, Intermediate ≤ L3, Advanced ≤ L5) | Downgrade violating exercise |
| 5 | Equipment available | Every exercise uses equipment ∈ athlete's equipment profile | Substitute per Section 7 |
| 6 | Session flow correct | Power before strength. Core last. Warm-up first. | Reorder blocks |
| 7 | Power before fatigue | Power block has no preceding strength or conditioning | Move power to first main block |
| 8 | Recovery reasonable | Rest intervals appropriate to block type (Section 6) | Adjust rest periods |
| 9 | Knee/hip balance | At least one knee dominant AND one hip dominant in full body sessions | Add missing pattern |
| 10 | No red flags | None of the Section 10 red flags are triggered | Remove violating element |
| 11 | Volume within limits | Total work within session min/max per Section 3.3 | Reduce sets or exercises |
| 12 | Rotation respects history | No exercise in last-session same slot without progression | Rotate per Section 5 |

### 9.2 Scoring

Each check is pass/fail. Score = (passed / 12) × 10.

| Score | Verdict |
|-------|---------|
| 10/10 | Perfect. Deliver. |
| 9/10 | Minor issue. Accept if coaching judgment overrides. |
| 8/10 | Acceptable. Flag the failing items as coaching notes. |
| <8/10 | DO NOT DELIVER. Return to step 5 of generation sequence and fix. |

### 9.3 Minimum acceptable score: 8/10

Any session scoring below 8/10 must be regenerated. A coach may override and deliver a session scoring 8/10 — this is the boundary of FORGE's automatic guarantee.

---

## SECTION 10: 100 Program Generation Laws

> These are the immutable rules of the generator. Every session produced by FORGE satisfies all 100 laws.
> Short. Actionable. Deterministic. No exceptions unless explicitly noted.

### Session Architecture (LAW-001 to LAW-015)

**LAW-001:** Never place conditioning before power or strength. Conditioning is always the final training stimulus.

**LAW-002:** Never prescribe an exercise above the athlete's maximum difficulty level (Beginner ≤ L2, Intermediate ≤ L3, Advanced ≤ L4-L5).

**LAW-003:** Pulling volume must equal or exceed pushing volume in every session and across every training week.

**LAW-004:** Every session must include at least one core exercise placed in the last training block.

**LAW-005:** Every session must include at least one posterior chain exercise.

**LAW-006:** Power exercises must be performed with full recovery (2-5 minutes between sets) and never superset.

**LAW-007:** No more than 3 strength exercises per session. Beyond 3, session quality degrades.

**LAW-008:** Session duration must not exceed 90 minutes.

**LAW-009:** Warm-up must include movement patterns specific to the session's main work.

**LAW-010:** A session must have a defined purpose. Every exercise must be traceable to that purpose.

**LAW-011:** No two consecutive sessions may have identical exercise lists. At least one exercise must rotate.

**LAW-012:** Static stretching before main work is prohibited.

**LAW-013:** Every session must include at least one prehab exercise (band pull-apart, face pull, glute bridge, or equivalent).

**LAW-014:** Core is never placed before power or strength in any session.

**LAW-015:** Activation (glute, scapular, movement prep) must precede any loaded work.

### Exercise Selection (LAW-016 to LAW-030)

**LAW-016:** Select the exercise matching the athlete's difficulty level before any other consideration.

**LAW-017:** Select the exercise matching available equipment before considering variety.

**LAW-018:** Never select an exercise that requires equipment not in the athlete's equipment profile.

**LAW-019:** When exercise choice is tied, prefer the exercise least recently used in that slot.

**LAW-020:** Exercise substitution within a family is always preferred over changing families.

**LAW-021:** Intent (power, strength, endurance, stability) must be preserved when substituting between families.

**LAW-022:** Olympic lifts are optional. When included, they are always the first main work exercise and never superset.

**LAW-023:** Box jumps are for power, not conditioning. Box height must not exceed knee height for power-focused sessions.

**LAW-024:** Depth jumps require a minimum 1.5x BW squat before inclusion.

**LAW-025:** Single-leg work must be bilateral-load-matched (half the load of the bilateral equivalent) on first introduction.

**LAW-026:** Carries are distance/time-based, not rep-based. Minimum 20m or 20s per set.

**LAW-027:** Med ball throws are power work and require full recovery between sets.

**LAW-028:** Sprint work is measured in meters, not time. Minimum 10m for acceleration, minimum 30m for max velocity.

**LAW-029:** Tempo runs must specify target pace and heart rate zone. "Run at moderate pace" is insufficient specification.

**LAW-030:** Plyometric ground contacts must not exceed 30 per session.

### Athlete Level (LAW-031 to LAW-040)

**LAW-031:** Beginner athletes do not perform Olympic lifts.

**LAW-032:** Beginner athletes do not perform depth jumps or any plyometric exceeding 1 foot landing height.

**LAW-033:** Beginner athletes use 60-70% 1RM or RPE 6-7 for compound lifts.

**LAW-034:** Beginner athletes must demonstrate competency (80%+ reps at target depth) before load progression.

**LAW-035:** Intermediate athletes may perform complex training (strength + plyometric pairs) only after 4 weeks of foundational work.

**LAW-036:** Advanced athletes may use velocity-based training thresholds for set termination (<20% velocity loss).

**LAW-037:** Athlete level is reassessed every 8 weeks or at the start of each new block.

**LAW-038:** A returning athlete (4+ weeks off) regresses one level for the first 2 weeks of return.

**LAW-039:** Youth athletes (U16) do not perform 1RM testing. Maximal strength is estimated via 3-5RM or velocity.

**LAW-040:** Youth athletes (U16) do not perform depth jumps, heavy Olympic lifts, or any exercise with spinal loading >50% bodyweight without demonstrated technique.

### Progression (LAW-041 to LAW-055)

**LAW-041:** Strength progression follows: add reps within the target range first, then add load.

**LAW-042:** Load increases are informed by the previous 2-3 sessions' performance, not a pre-planned chart.

**LAW-043:** When an athlete cannot progress for 3 consecutive sessions, rotate the exercise before attempting load increase.

**LAW-044:** When an athlete cannot progress for 6 consecutive sessions despite exercise rotation, deload or change the movement family.

**LAW-045:** Primary compound loads increase by 2.5-5 kg per progression step. No larger increments.

**LAW-046:** Power progression: increase velocity first, then load while maintaining velocity, then complexity.

**LAW-047:** Accessory progression moves faster than primary progression: rep range → set count → load.

**LAW-048:** Bodyweight progression follows rep thresholds (3x12 at current level → advance to next level).

**LAW-049:** Deloads are scheduled every 4-6 weeks. Reactive deloads (based on fatigue markers) override scheduled deloads.

**LAW-050:** Deload volume is 40-60% of normal training volume. Intensity is maintained at normal levels.

**LAW-051:** Competition week: volume drops 20-30%, intensity is maintained. This is not a deload — this is competition preparation.

**LAW-052:** Off-season progression: build volume for 2-4 weeks before increasing intensity.

**LAW-053:** Pre-season progression: decrease volume, maintain or increase intensity, add sport specificity.

**LAW-054:** In-season progression: do not progress. Maintain. The adaptation goal is retention, not development.

**LAW-055:** Progress is measured against the athlete's own history, not against external standards or peer performance.

### Session Composition (LAW-056 to LAW-065)

**LAW-056:** Every strength session must contain at least one knee dominant and one hip dominant exercise.

**LAW-057:** Every power session must contain at least one explosive lower body and one explosive upper body exercise (can be same exercise if med ball throw or similar).

**LAW-058:** Every session (except deload and return-to-sport) must contain at least one upper body push and one upper body pull.

**LAW-059:** Every conditioning session must include a warm-up, main conditioning block with specified work:rest, and cool-down.

**LAW-060:** Full body sessions must cover lower body, upper body push, upper body pull, and core as a minimum.

**LAW-061:** Upper/lower splits must include at minimum: lower day (quad, posterior, core), upper day (horizontal push, horizontal pull, vertical pull, core).

**LAW-062:** Court sport sessions must include COD, single-leg knee work, and rotational work as mandatory elements.

**LAW-063:** Contact sport sessions (rugby, American football) must include loaded carries and neck prep in every session.

**LAW-064:** Sprint development sessions must include sprint technique work (in warm-up/activation) before any sprint effort.

**LAW-065:** Return-to-sport sessions must include injury-specific prehab before any loaded exercise.

### Rotation (LAW-066 to LAW-075)

**LAW-066:** Exercises rotate every 4-6 weeks. 1-2 exercises per family rotate per block, never all at once.

**LAW-067:** Primary compounds (squat, deadlift, bench, pull-up) may stay for up to 8 weeks if progression continues.

**LAW-068:** Accessory exercises rotate every 3-4 weeks.

**LAW-069:** An exercise rotated out does not return to the same slot for a minimum of 8 weeks.

**LAW-070:** Progression overrides rotation. If an athlete is progressing on an exercise, keep it.

**LAW-071:** Pain overrides progression. If an exercise causes joint pain, rotate it immediately regardless of progression schedule.

**LAW-072:** When rotating, select the exercise least recently used in the family.

**LAW-073:** A rotated-in exercise must be at the same difficulty level or one level higher if progression is appropriate.

**LAW-074:** Never rotate more than 30% of exercises in a single session.

**LAW-075:** Rotation is per-athlete, not per-group. Individualising rotation respects individual response.

### Substitution (LAW-076 to LAW-085)

**LAW-076:** Substitution within the same family is always preferred over substitution across families.

**LAW-077:** When same-family substitution is impossible, match the training intent (power, strength, endurance, stability).

**LAW-078:** When intent cannot be matched, match the movement plane (sagittal, frontal, transverse, or multi-planar).

**LAW-079:** Equipment loss: switch to the next available exercise in the family priority list that matches available equipment.

**LAW-080:** Injury substitution: replace the exercise causing pain with a mechanically different variation in the same family.

**LAW-081:** Injury substitution across families: select an exercise that works the same muscle group through a different movement pattern.

**LAW-082:** When no viable substitution exists, skip the slot and flag it. Do not insert a non-functional exercise.

**LAW-083:** Travel substitution: maintain family order. Downgrade equipment profile to match what is available.

**LAW-084:** Crowded gym substitution: replace the occupied exercise with one that uses available equipment. Maintain family. Maintain intent.

**LAW-085:** Emergency fallback (no equipment, no space): bodyweight L1 exercise in the same family. If impossible, skip the family for one session.

### Coaching Standards (LAW-086 to LAW-095)

**LAW-086:** Every session must have at least one measurable data point (RPE, load, jump height, sprint time, or throw distance).

**LAW-087:** Every session must have rest intervals specified for each block type.

**LAW-088:** Conditioning is never prescribed as punishment.

**LAW-089:** Every session must have 1-3 reps in reserve for all strength working sets (except competition peaking).

**LAW-090:** A session is not valid if it contains any of the 50 red flags from the Coaching Bible Section 10.

**LAW-091:** A coach must be able to articulate the purpose of every exercise in the session.

**LAW-092:** Every athlete's program must account for their injury history (known or disclosed).

**LAW-093:** The S&C program must not conflict with the sport practice load on the same day without adjustment.

**LAW-094:** A program may be individualised within the group template. One-size-fits-all is not coaching.

**LAW-095:** Every training block ends with a review. The next block is informed by that review.

### Boundary Conditions (LAW-096 to LAW-100)

**LAW-096:** If the session scores <8/10 on the credibility check, it must not be delivered. Regenerate.

**LAW-097:** If the athlete reports new pain during a session, the session stops for that exercise. Substitute before continuing.

**LAW-098:** If the athlete misses 3+ consecutive sessions (illness, travel, other commitments), the next session regresses one difficulty level.

**LAW-099:** If the athlete has not trained for 4+ weeks, the first 2 weeks back are a return-to-sport protocol regardless of training age.

**LAW-100:** When two rules conflict, the rule that prioritises athlete safety and long-term development wins. Safety over performance. Health over volume. Technique over load.

---

*FORGE_PROGRAM_GENERATION_RULEBOOK_V1.md — Version 1.0*
*This is the master specification. A developer can build the entire FORGE generator from this document alone.*
*Derived from: FORGE_COACHING_BIBLE_V1.md, FORGE_BLUEPRINT_SELECTION_GUIDE_V1.md, FORGE_BLUEPRINT_CATALOG_V1.md, FORGE_COACHING_REFERENCE_DATABASE.md, FORGE_SUBSTITUTION_MATRIX_V1.md, FORGE_PATTERN_LIBRARY.md, BCCI_PATTERN_EXTRACTION_REPORT.md, REAL_WORLD_COACHING_COMPARISON_AUDIT.md*
