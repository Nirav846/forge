# FORGE Exposure Rulebook V1

## Exposure Buckets

Five tracked exposure types that matter for coaching decisions:

| Bucket | Code | What it measures | Why it matters |
|--------|------|-----------------|----------------|
| Sprint | `sprint_exp` | Max-velocity and acceleration sprint exposures | CNS readiness, hamstring injury risk, speed maintenance |
| Jump | `jump_exp` | Plyometric and ballistic landing exposures | Tendon health, reactive strength, landing mechanics |
| Eccentric | `eccentric_exp` | High-eccentric-cost exercise exposures | DOMS risk, muscle damage accumulation, pre-comp tapering |
| Deceleration | `decel_exp` | Braking/COD/deceleration exposures | Hamstring injury risk (eccentric braking), agility maintenance |
| Rotational | `rot_exp` | Rotational power and anti-rotation exposures | Core integrity, sport-specific force transfer |

## Exercise-to-Bucket Mapping

Every exercise maps to zero or more exposure buckets via its `family`, `competition_role`, and metadata flags.

### Sprint Bucket

| Contributes | Families / Criteria |
|------------|-------------------|
| Yes | Sprint family (all 22 exercises) |
| Yes | Any conditioning protocol with `movement_profile` in: `linear_speed_endurance`, `linear_rsa`, `accel_decel` |
| No | All other exercises and protocols |

**Weekly minimums:**
- Sprint-development blueprints (BP4, BP10): ≥2 sprint exposures/week
- Field sport athletes (soccer, rugby, cricket): ≥1 sprint exposure/week in-season
- Court sport athletes: ≥2 COD acceleration exposures/week (counts toward sprint bucket at 50%)

**Weekly maximums:**
- All athletes: ≤4 high-intensity sprint exposures/week (sessions with Sprint family or speed-endurance conditioning)
- Acute:chronic sprint spike >1.5 → force reduction next session

### Jump Bucket

| Contributes | Families / Criteria |
|------------|-------------------|
| Yes | Plyo family (all 16 exercises) |
| Yes | Ball family (all 14 exercises) — counted as jump exposure |
| Yes | Conditioning protocols with `impact_level >= 4` AND `eccentric_cost >= 3` (covers RSA, intensive tempo with bounding) |
| No | All other exercises |

**Weekly minimums:**
- Power-blueprints (BP2, BP4, BP9): ≥2 jump exposures/week
- All athletes: ≥1 jump exposure/week during in-season (maintain reactive strength)
- Beginners: ≥1 low-intensity jump exposure/week (pogos, ankle hops)

**Weekly maximums:**
- ≤3 high-impact jump sessions/week (impact ≥4)
- ≤2 sessions with depth jumps or single-leg landings
- 48h minimum between high-impact jump sessions

### Eccentric Bucket

| Contributes | Families / Criteria |
|------------|-------------------|
| Yes | Any exercise with `eccentric_cost >= 4` |
| Yes | DLHD exercises with `eccentric_cost >= 3` (most hinge patterns) |
| Yes | SLHD exercises with `eccentric_cost >= 3` (single-leg hinge patterns) |
| Yes | Conditioning protocols with `eccentric_cost >= 3` |
| No | Core, Carry, Acc (eccentric always ≤2) |

**Current high-eccentric exercises (eccentric_cost >= 4):**

| Exercise | Ecc | Fatigue |
|----------|-----|---------|
| RDL | 5 | 3 |
| Single-Leg RDL | 5 | 3 |
| Nordic Hamstring Curl | 5 | 4 |
| Band-Resisted Nordic | 5 | 4 |
| Weighted Nordic | 5 | 4 |
| Conventional Deadlift | 5 | 5 |
| Barbell Good Morning | 5 | 4 |
| Stiff-Leg Deadlift | 5 | — |
| Deficit Deadlift | 4 | 4 |
| Sumo Deadlift | 4 | 4 |
| Block Pull | 4 | 4 |
| Weighted Back Extension | 4 | 4 |
| Barbell Front Squat | 4 | 5 |
| Pendlay Row | 4 | 4 |
| Muscle-Up | 4 | 4 |
| Depth Jump | 4 | 4 |
| Various single-leg | 4 | 4 |

**Weekly minimums:**
- Strength blueprints: ≥6 eccentric exposures/week (sufficient for adaptation)
- No minimum for in-season maintenance phases

**Weekly maximums:**
- ≤3 eccentric-cost ≥4 exposures/week in-season
- ≤2 eccentric-cost ≥4 exposures/week during competition taper (+5 days)
- ≤1 eccentric-cost ≥4 exposure 2-3 days before competition
- No eccentric-cost ≥4 1 day before competition (already enforced by comp windows)

### Deceleration Bucket

| Contributes | Families / Criteria |
|------------|-------------------|
| Yes | Conditioning protocols with `movement_profile` in: `accel_decel`, `change_of_direction` |
| Yes | Sprint exercises that include deceleration mechanics (Sprint-019 Deceleration Sprint) |
| Yes | Court-specific conditioning (court_shuffle, court_diagonal, court_rally_repeat) |
| Partial | SLKD and SLHD exercises with unilateral landing (count at 50%) |
| No | Pure linear tempo conditioning, strength exercises |

**Weekly minimums:**
- Court sport athletes: ≥2 deceleration exposures/week
- Field sport athletes: ≥1 deceleration exposure/week
- All change-of-direction sports: ≥1 COD exposure/week

**Weekly maximums:**
- ≤3 high-intensity deceleration sessions/week
- Maintain 48h gap between high-decel sessions when possible

### Rotational Bucket

| Contributes | Families / Criteria |
|------------|-------------------|
| Yes | Rot family (all 17 exercises) |
| Yes | Exercises with `rotational = True` (28 exercises across families) |
| Yes | Conditioning protocols with rotational elements |
| No | Purely linear exercises |

**Weekly minimums:**
- Rotational sport athletes (golf, tennis, throwing): ≥2 rotational exposures/week
- All athletes: ≥1 anti-rotation exposure/week (Pallof press, chops, lifts)

**Weekly maximums:**
- ≤5 rotational exposures/week (soft tissue recovery)
- No specific upper limit for anti-rotation (Pallof holds are low-load)

## Conditioning Protocol Exposure Mapping

| Movement Profile | Sprint | Jump | Eccentric | Decel | Rot |
|-----------------|--------|------|-----------|-------|-----|
| linear_tempo | No | No | Yes | No | No |
| accel_decel | Yes | No | Yes | Yes | No |
| linear_speed_endurance | Yes | No | Yes | No | No |
| linear_rsa | Yes | No | Yes | Partial | No |
| change_of_direction | Partial | No | Yes | Yes | Partial |
| court_shuffle | No | No | Yes | Yes | No |
| court_diagonal | No | No | Yes | Yes | No |
| court_rally_repeat | No | No | Yes | Yes | No |
| bike_intervals | No | No | No | No | No |
| rower_intervals | No | No | No | No | No |
| treadmill_intervals | No | No | Partial | No | No |
| mixed_modal_circuit | No | Partial | Partial | No | No |
| recovery_flush | No | No | No | No | No |
| pool_recovery | No | No | No | No | No |
| mobility_recovery | No | No | No | No | No |

## Exposure Score Calculation

Each exposure bucket uses a simple counter:

```
# Per session:
sprint_count    = number of Sprint family exercises + number of sprint-mapped conditioning protocols
jump_count      = number of Plyo/Ball exercises + number of jump-mapped conditioning protocols
eccentric_count = number of exercises with eccentric_cost >= 4 + number of conditioning with eccentric_cost >= 4
decel_count     = number of decel-mapped conditioning protocols + Sprint-019 + 0.5 * SLKD/SLHD
rot_count       = number of Rot family exercises + number of rotational exercises (other families)
```

**Weekly exposure = sum of per-session counts over 7 days.**

## Example: One Week (Full Body Strength × 3 sessions)

| Session | Sprint | Jump | Eccentric | Decel | Rot |
|---------|--------|------|-----------|-------|-----|
| Mon: Full Body | 0 | 0 | 2 (RDL, Row) | 0 | 0 |
| Wed: Full Body | 0 | 0 | 1 (RDL) | 0 | 0 |
| Fri: Full Body + Cond | 1 (RSA-003) | 0 | 3 (RDL, RSA) | 1 (RSA) | 0 |
| **Weekly total** | **1** | **0** | **6** | **1** | **0** |

**Coaching interpretation:** Zero jump exposure in a week → needs plyometric injection. Only 1 sprint exposure → sprint-development athlete needs more. 6 eccentric exposures → adequate for strength maintenance but below eccentric tolerance for off-season.

## Rules That Use Exposure Counts

(See FORGE_PERIODIZATION_RULES_V1.md for the full rule set.)
