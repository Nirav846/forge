# FORGE V2.5 — Synthesis & Execution Roadmap

**Role:** Chief Architect + Performance Director + Principal Sports Scientist
**Input:** Audits #1-11
**Goal:** Smallest version that produces coach-credible programs

---

## Core Diagnosis (Not Repeating Audit Findings)

Forge V1/V2 has one architectural strength and one fatal flaw:

**Strength:** The V2 demand ontology (quality × movement pattern) is biomechanically correct and genuinely novel.

**Flaw:** The system assumes demand scores → program priority. This produces programs for a "generic athlete with test scores" rather than a real athlete in a real training context.

The fix requires adding **5 coaching decision variables** that transform demand scores from a programming *driver* into a programming *modifier*. That's V2.5.

---

## SECTION 1 — Minimum Essential Concepts

From 11 audits, these are the ONLY concepts required to bridge classification → coaching:

| # | Concept | Why Essential (Not Nice-to-Have) |
|---|---------|----------------------------------|
| 1 | **Macro-Phase** | Every coaching decision starts with "what time of year is it?" Off-season, pre-season, in-season, post-season, return-to-play. Phase determines: frequency, volume, intensity, exercise selection, progression rate, and whether deficits should be fixed at all. Without it, the system defaults to "permanent off-season" — wrong for >50% of athletes. |
| 2 | **Coach Intent per Quality × Phase** | The single most important coaching input. "This pre-season, develop power, maintain strength, minimise hypertrophy." Three toggles—DEVELOP, MAINTAIN, MINIMISE—replace the automatic deficit-focus that breaks the system for in-season, elite, and return-to-play athletes. |
| 3 | **Competition Calendar** | Dates are not optional. In-season athletes need "days to next competition" driving volume and exercise selection (no heavy eccentric work within 48h of game). Off-season athletes need "weeks until pre-season starts" to progress blocks. Tournament athletes need "session type: competition, travel, recovery" for each day. |
| 4 | **Training Load (All Sources)** | S&C is 20-40% of total training load for team sport athletes. The system currently generates S&C programs in isolation. It needs total load — sport practice hours + S&C volume + competition load — to determine whether volume is appropriate. Without this, S&C programs cause overtraining 100% of the time when added to existing team training. |
| 5 | **Injury Modifications** | Not a database of injury types. A simple list of "permanent exercise restrictions per athlete." Examples: "avoid back squat >80% due to lumbar stress fracture history," "avoid Nordic curls due to hamstring graft (ACLR)." This gates exercise selection BEFORE demand matching. |
| 6 | **Minimum Effective Dose Table** | Per quality × phase: what is the MINIMUM weekly volume to maintain vs develop? For in-season: 2×5 heavy singles maintain max strength. For off-season: 4×5-8 needed to develop it. This single table makes in-season programming coherent. The current system has no "enough" concept — it always prescribes development volume regardless of phase. |
| 7 | **Asymmetry Flags** | Not a deep analysis. Binary flag per athlete: inter-limb difference >10% on any bilateral→unilateral test? Yes → require unilateral emphasis in this phase. No → bilateral work is fine. Changes exercise selection from "Barbell Back Squat" to "RFESS + Split Squat" until symmetry is restored. |
| 8 | **Progression Rate Curve** | Per phase: aggressive (off-season, novice), moderate (pre-season, intermediate), conservative (in-season, advanced), minimal (late in-season, elite). This replaces the single linear progression model that plateaus advanced athletes and overtrains in-season ones. |
| 9 | **Athlete Readiness (Today)** | Sleep quality (1-5), soreness (1-5), mood (1-5), stress (1-5). Four questions. Combined into a readiness score that trims volume (low readiness → -20% volume, same intensity) or shifts exercise selection (low readiness → no heavy eccentrics). Without this, the system is blind to daily variation, which is the #1 reason coaches override programs. |
| 10 | **Total Weekly Capacity** | Per athlete: max S&C sessions/week in this phase. An in-season athlete can do 2. An off-season athlete can do 4. A youth athlete can do 3 (accounting for sport + school). This replaces the fixed "2-4 sessions" from program_design_rules with a per-athlete, per-phase variable. |

---

## SECTION 2 — MVP / Beta / V3 Classification

| Concept | When | Rationale |
|---------|------|-----------|
| Macro-Phase | **MUST (MVP)** | Without it, every program is wrong for half the year |
| Coach Intent per Quality × Phase | **MUST (MVP)** | This is the key input that replaces deficit-driven decision-making |
| Competition Calendar | **MUST (MVP)** | Phases need dates; in-season needs proximity logic |
| Training Load (All Sources) | **SHOULD (Beta)** | Can ship without it if phases are conservative about S&C-only volume |
| Injury Modifications | **MUST (MVP)** | Without this, the system prescribes dangerous exercises |
| Minimum Effective Dose Table | **SHOULD (Beta)** | Can use fixed % of off-season volume for in-season as interim |
| Asymmetry Flags | **SHOULD (Beta)** | Important for returning athletes; can hard-code for MVP |
| Progression Rate Curve | **SHOULD (Beta)** | Can use single moderate rate for MVP; phased rates in Beta |
| Athlete Readiness (Today) | **SHOULD (Beta)** | Transformative for coach trust; MVP can ship without it if overrides are well-captured |
| Total Weekly Capacity | **MUST (MVP)** | Prevents 4-session programs for in-season athletes |

**MVP (6 concepts):** Macro-Phase, Coach Intent, Competition Calendar, Injury Modifications, Total Weekly Capacity, and a hard-coded MED table (off-season = full volume, in-season = 50% volume).

---

## SECTION 3 — Minimum Coaching Model (Passes 5 Cases)

### The Model

```
┌─────────────────────────────────────────────────────────────┐
│ COACH STRATEGY (set once per phase)                         │
│                                                             │
│  Phase: [Off-Season | Pre-Season | In-Season | Post-Season]│
│  Competition Calendar: [first_match / next_match / last]    │
│                                                             │
│  Per Quality (V2 Demands, ~8-10 for cricket):               │
│    Intent: [DEVELOP | MAINTAIN | MINIMISE]                  │
│    Weekly Freq: [1 | 2 | 3] (derived from intent)          │
│                                                             │
│  Injury Modifications: [permanent exercise restrictions]     │
│  Weekly Capacity: [max S&C sessions]                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PROGRAM GENERATOR (runs Coach Strategy + Athlete Data)      │
│                                                             │
│  1. Intent → volume tier (from MED table)                   │
│  2. Competition proximity → modify this week's load         │
│  3. Injury modifications → block unsafe exercises           │
│  4. Asymmetry flags → add unilateral variants               │
│  5. Demand scores → MODIFY exercise emphasis within intent  │
│     (NOT primary driver — deficits tweak, not dictate)      │
│  6. Readiness (Beta+) → trim today's volume if low          │
│                                                             │
│  Output: program_session_exercises with sets, reps,         │
│          intensity, rest, and equipment per session          │
└─────────────────────────────────────────────────────────────┘
```

### How This Transforms Each Case

**Elite Fast Bowler (in-season):**
- Current: Deficit-driven → tries to fix everything → overtraining + wrong emphasis
- V2.5: Coach sets intent → Strength MAINTAIN, Power MAINTAIN, Speed MAINTAIN, Rotational Power MAINTAIN
- Generator sees "maintain" → uses MED volumes (2×3 squats at 85%, 2×3 trap bar jumps, 2×5 med ball throws)
- Injury mod: stress fracture history → no back squat >80%, use trap bar deadlift instead
- Weekly capacity: 2 sessions (matches + travel consume the week)
- **Result:** Credible in-season program. Coach might tweak exercises but the structure is correct.

**Developing Spinner (off-season, U19):**
- Current: Deficit-driven → targets rotational power only → misses general athletic development
- V2.5: Coach sets intent → Strength DEVELOP, Power DEVELOP, Rotational Power DEVELOP, Mobility DEVELOP
- Generator sees "develop" on most qualities → broader program across 8 demands
- Uses FOUNDATION development level → no complex Olympic variants
- Weekly capacity: 3 sessions (school + academy load considered)
- **Result:** Not perfect (still no maturation model), but a credible general athletic development program.

**Professional Batter (in-season):**
- Current: Deficit-driven → tries to fix his back/hip niggles by adding work → wrong
- V2.5: Coach sets intent → Power MAINTAIN, Acceleration MAINTAIN, everything else MINIMISE
- Competition proximity: next match in 4 days → program for day -4, -3, -2: activation only from day -2
- Generator outputs 2 maintenance sessions/week with low volume, high intent
- Injury mod: hip niggles → split squats instead of bilateral work
- **Result:** Credible. The batter might actually do this program. Current version would be deleted.

**Soccer Midfielder (female, in-season):**
- Current: System cannot represent a midfielder at all (no aerobic concept, no menstrual cycle)
- V2.5: Still can't fully represent aerobic capacity, BUT:
  - Phase = in-season → all intents = MAINTAIN
  - Generator doesn't try to "fix" anything
  - Injury mod: 2 previous hamstring strains → Nordic curls every session, hamstring:RDL emphasis
  - Competition proximity: match today → rest tomorrow → light session day-2
  - Total capacity: 2 S&C/week (6 team sessions already)
  - **Result:** Improves from "dangerous" to "acceptable but incomplete." Still needs aerobic concept for full soccer support, but doesn't hurt the athlete.

**Olympic Sprinter (pre-competition):**
- Current: Gym-first model is wrong for sprinters
- V2.5: Coach sets Power DEVELOP, Acceleration MAINTAIN, Speed MAINTAIN
- Competition calendar: 3 months to championships → appropriate phasing
- Even so, the model still treats gym as primary. This case reveals the model's limit — sprint training needs TRACK-first programming.
- **Result:** Borderline. Acceptable if positioned as "this is your supplementary S&C program, not your sprint program." Coach would use it as a gym supplement checker, not the main program.

### Case Test Summary

| Case | V1/V2 | V2.5 |
|------|-------|------|
| Elite Fast Bowler (in-season) | FAIL | PASS (barely — credible maintenance) |
| Developing Spinner (off-season) | MARGINAL FAIL | PASS (credible off-season development) |
| Professional Batter (in-season) | FAIL | PASS (credible maintenance + niggle-aware) |
| Soccer Midfielder (female, in-season) | FAIL | MARGINAL PASS (not harmful, but aerobic gap remains) |
| Olympic Sprinter (pre-comp) | FAIL | MARGINAL PASS (correct supplementary S&C, still no track-primary model) |

3/5 PASS, 2/5 MARGINAL PASS. This is acceptable for V2.5.

---

## SECTION 4 — Revised Bounded Context Map

### Current (11 contexts)

```
Athlete Management │ Assessment │ Deficit Detection │ Performance Intelligence
Exercise Library  │ Templates  │ Program Design     │ Program Execution
Athlete State     │ Observability │ Coach Feedback
```

### V2.5 (4 contexts)

```
┌─────────────────────────────────────────────────────────────┐
│                     COACHING STRATEGY (NEW)                  │
│                                                             │
│  Responsibilities:                                           │
│  - Store Macro-Phase + Coach Intent per Quality              │
│  - Manage Competition Calendar                               │
│  - Hold MED Table (minimum doses per phase)                  │
│  - Track Injury Modifications (permanent restrictions)       │
│  - Compute Proximity-to-Competition logic                    │
│                                                             │
│  What was merged: Coach Intent (new) + Competition (new)     │
│  + Injury Context (from Athlete State) + MED (new)           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     ATHLETE                                  │
│                                                             │
│  Responsibilities:                                           │
│  - Profile (sport, role, development level)                  │
│  - Assessment Results + Scores                               │
│  - Training Load History (all sources)                       │
│  - Asymmetry Flags (computed from assessments)               │
│  - Readiness (daily wellness)                                │
│  - Session Actuals (completed work vs prescribed)            │
│                                                             │
│  What was merged: Athlete Mgmt + Assessment + Deficit        │
│  + Athlete State (load, readiness) + Execution tracking      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     PERFORMANCE INTELLIGENCE (SIMPLIFIED)     │
│                                                             │
│  Responsibilities:                                           │
│  - V2 Demands (quality × pattern) — keep current model       │
│  - Role→Demand Priorities                                    │
│  - Exercise→Demand Mapping                                   │
│  - Assessment→Demand Mapping                                 │
│  - Exercise Library + Templates + Slots + Equipment          │
│  - Exercise Equivalencies (finally seed these)               │
│                                                             │
│  What was merged: Performance Intelligence + Exercise        │
│  Library + Templates. Deleted: V1 performance_drivers,       │
│  V1 deficit routing, z-score path.                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     PROGRAM GENERATOR                        │
│                                                             │
│  Responsibilities:                                           │
│  - Read Coach Strategy + Athlete + Performance Intelligence  │
│  - Apply phase-appropriate progression rules                 │
│  - Apply injury modifications (block unsafe exercises)       │
│  - Apply asymmetry flags (add unilateral variants)           │
│  - Apply proximity-to-competition (trim volume)              │
│  - Apply demand scores (modify emphasis within intent)       │
│  - Generate program_session_exercises                        │
│  - Log domain events                                         │
│                                                             │
│  What was merged: Program Design + Program Execution         │
│  + Observability (keep event logging).                       │
└─────────────────────────────────────────────────────────────┘
```

### What Changed

| Change | Why |
|--------|-----|
| **Coaching Strategy created** | Was missing entirely. This is the most important new context. |
| **Athlete now owns deficits + readiness** | Deficits are attributes of an athlete, not a separate system. Readiness is an athlete attribute. |
| **Performance Intelligence owns ALL ontology** | One unified demand system. V1 drivers deleted. V2 demands survive. |
| **Program Generator becomes the orchestrator** | Reads from 3 other contexts and produces output. Cleanest possible architecture. |
| **Coach Feedback → deleted as separate context** | Overrides are logged in the Generator context as audit trail. Not a bounded context. |
| **Observability → merged into Generator** | Keep domain_events table, delete separate Obs service. |

---

## SECTION 5 — Revised Data Flow

### Current Flow

```
Assessment Scores → Benchmark Comparison → Deficit ID → Deficit Priority
  → Demand Matching → Exercise Selection → Template Population → Program
```

Every step is automated. No coach input. No context. No phase awareness.

### V2.5 Flow

```
                                 ┌─────────────────────────────┐
                                 │     COACHING STRATEGY       │
                                 │                             │
  ┌────────────┐                │  Phase: Off-Season          │
  │ COMPETITION│                │  Intent: {Power: DEVELOP    │
  │ CALENDAR   │────────────────│          Strength: DEVELOP  │
  │            │                │          Speed: MAINTAIN}   │
  │ Match:  Jan│  proximity →  │  Capacity: 3 S&C/week       │
  │ Off:  Now  │  weeks until  │  MED: Maintenance doses     │
  └────────────┘   prep start  └─────────────────────────────┘
                                           │ intent + phase
                                           ▼
┌──────────────┐              ┌─────────────────────────────┐
│   ATHLETE    │              │     PROGRAM GENERATOR       │
│              │  scores      │                             │
│ Assessments  │─────────────▶│  1. Read Strategy           │
│ → Benchmarks │              │  2. Apply Phase Rules       │
│ → deficits   │              │  3. Block Injured Exercises │
│              │              │  4. Apply Asymmetry Fix     │
│ Injury Hist  │─────────────▶│  5. Apply Competition       │
│              │  restrictions│     Proximity Trim          │
│ Readiness    │─────────────▶│  6. Score Demands           │
│ (wellness)   │  today mod   │     (WITHIN intent bounds)  │
│              │              │  7. Select Exercises        │
│ Load History │─────────────▶│     (by demand + phase)     │
│ (all sources)│  load ctx    │  8. Set Volumes (by MED)    │
│              │              │  9. Set Progress Rate       │
│ Asymmetry    │─────────────▶│     (by phase rate curve)   │
│              │  flags       │ 10. Generate Weekly Program │
└──────────────┘              │                             │
                              │  OUT: program_sessions with │
┌──────────────┐              │       exercises, sets, reps,│
│ PERF INTEL   │              │       intensity, rest       │
│              │  exercise    │                             │
│ V2 Demands   │─────────────▶└─────────────────────────────┘
│ → Role Dem   │                                              │
│ → Exer Map   │                                              ▼
│ Templates    │                                     ┌──────────────┐
│ Equivalents  │                                     │   COACH      │
└──────────────┘                                     │   REVIEWS    │
                                                     │              │
                                                     │  Accept /    │
                                                     │  Modify /    │
                                                     │  Reject      │
                                                     │              │
                                                     │  stored as   │
                                                     │  override log│
                                                     └──────────────┘
```

### Key Changes from Current

| Change | Why |
|--------|-----|
| **Coach Strategy is the primary input** | Not deficits. The coach's intent for THIS PHASE determines everything. |
| **Phase is explicit** | Every quality has a phase-appropriate goal. |
| **Deficits modify within bounds** | If intent = MAINTAIN, a power deficit doesn't trigger more power work — it triggers a note: "power below threshold, but in-season maintenance only." |
| **Competition proximity gates load** | Within 48h of competition → no heavy eccentric work, volume trimmed. |
| **Injury blocks before demand matches** | Unsafe exercises are removed from the candidate pool BEFORE demand matching. |
| **Coach reviews and overrides are expected** | Not a failure state. The system logs them for improvement. |

---

## SECTION 6 — Everything That Should Be Deleted

### Migrations

| File | Why Delete |
|------|-----------|
| `000021_seed_deficit_routing.up.sql` | Superseded by `_fixed` version. Both have benchmark bugs (duplicate names, inserts fail). Delete both. |
| `000021_seed_deficit_routing_fixed.up.sql` | Bugs unfixed. PHASE_5A provides cleaner deficit routing. Delete. |
| `000015_olympic_lift_framework.up.sql` | Superseded by 000017_repair. Delete original. |
| `PHASE_5A_SEED.sql` | Keep this one (better benchmark names). Move content into a cleaned-up 000021 replacement. |

### Tables / Concepts

| Delete | Why |
|--------|-----|
| **V1 `performance_drivers` system** | Three tables (`performance_drivers`, `driver_assessments`, `deficit_training_methods`) replaced by V2 demands. V1's 12 cricket drivers overlap with V2's 18 demands. Delete the V1 rows, keep the V2 ontology. |
| **Z-score deficit path in `assessment_metric_engine`** | Dead code from first session audit. Zero production callers. Delete the file. |
| **`sports_science_rules` table** | 7 rules are too few to be useful and too many to maintain. Delete the table. Hard-code the 2 rules that matter (Nordic curl volume cap, jump squat load cap) into the generator. |
| **`program_design_rules` table** | Cricket-specific seed data that duplicates what Coach Intent + MED Table + V2 priorities provide. Delete the table. Replace with actual logic. |
| **`exercise_class`, `primary_adaptation`, `force_vector` columns** | Zero values populated across 35 exercises. Deleting a column is not worth migration effort; set them all to NULL and ignore them. |
| **`slot_exercise_fallbacks` table** | Only 2 pairs seeded. 0% coverage. Delete the table; add equivalencies to `exercise_equivalencies` instead. |
| **`athlete_state_snapshots` readiness scores** | No input data exists to compute readiness. The columns produce confidence-destroying zeros. Remove the auto-generated defaults. Let readiness start empty until Beta adds wellness inputs. |
| **`program_coach_overrides` table** | Keep! This is valuable. Don't delete — its purpose changes from "audit log" to "coaching intent learning data." |

### Concepts / Approaches

| Delete | Why |
|--------|-----|
| **Assessment-to-deficit as primary program driver** | Replaced by Coach Intent. Deficits become modifiers within intent bounds. |
| **Linear-only progression** | Replaced by phase-appropriate progression rates. |
| **"Fix everything" philosophy** | Replaced by "develop what matters, maintain what's enough, ignore what's excessive." |
| **Generic templates from other sports** | Lower Body Power (American Football) should not be the default for a cricketer. Delete generic template defaults; use V2 demand→exercise mapping directly. |
| **Reactive Agility movement template** | No sport seeds use it. Delete. |
| **The concept that "more S&C is always better"** | Delete from the design philosophy. Total load awareness means S&C is one part of the athlete's week, not the center of it. |

### Services / Files

| File | Why Delete |
|------|-----------|
| `assessment_metric_engine.py` (z-score deficit path) | Dead code. The benchmark-based path in `deficit_detection_engine.py` is the authority. |
| `knowledge_graph_service.py` (if it exists purely to bridge V1→V2 concepts that shouldn't coexist) | If it translates V1 drivers to V2 demands, delete the translation. Keep V2 demands only. |

### Services / Files to KEEP (with modification)

| File | Modification |
|------|-------------|
| `deficit_detection_engine.py` | Keep benchmark-based path. Add Coach Intent as input: if intent = MAINTAIN, deficits reduce emphasis rather than increasing it. |
| `recommendation_engine.py` | Keep exercise selection by demand. Add: injury blocking, asymmetry flag handling, phase-appropriate exercise filtering. |
| `template_service.py` | Keep template population. Add: proximity-to-competition volume trim. |

---

## SECTION 7 — 12-Week Build Roadmap

**Team:** 1 senior engineer
**Codebase:** Existing (modify, don't rewrite)
**Sport:** Cricket only (expand in V3)
**Goal:** Programs an S&C coach would find credible

---

### WEEKS 1-2: Delete & Clean

**Do NOT build anything. Delete the dead weight.**

| Day | Task | Evidence of Done |
|-----|------|-----------------|
| 1-2 | Delete 000021 seed migrations (both regular and fixed). Move PHASE_5A content into a new 000025_clean_seed migration. | Both 000021 files deleted. PHASE_5A IDs renamed to single convention. |
| 3-4 | Delete 000015 migration (superseded by 000017). | Migration chain runs from 000014 → 000016. |
| 5-6 | Delete V1 performance_drivers rows from seed data. Keep V2 demands only. | cricket knowledge graph seeding no longer creates performance_drivers. |
| 7-8 | Delete `sports_science_rules` table migration. Delete `program_design_rules` table migration. | Schema has 5 fewer tables. |
| 9-10 | Delete `assessment_metric_engine.py` z-score path. Delete `Reactive Agility` template seed row. | Engine file now only has benchmark-based path. |
| 11-12 | Delete `athlete_state_snapshots` readiness defaulting to 0. Set all to NULLable. | Schema allows NULL readiness scores. |

**Week 1-2 exit:** 6 tables/files deleted. 2 migrations removed. 1 clean PHASE_5A replacement migration written. Single assessment naming convention enforced across all seed data.

---

### WEEKS 3-4: Coach Strategy (MVP Phase Model)

**Build the coaching input layer. This is THE new core.**

| Day | Task | Evidence of Done |
|-----|------|-----------------|
| 1-3 | Create `coaching_strategies` table: athlete_id, phase (enum), valid_from, valid_to, coach_notes. | Table exists with CRUD. |
| 4-6 | Create `quality_intents` table: coaching_strategy_id, demand_id, intent (DEVELOP/MAINTAIN/MINIMISE), priority_order. Seed with cricket role defaults. | Table seeded with sensible phase defaults. |
| 7-9 | Create `competition_events` table: athlete_id, event_date, event_type (match/tournament/race), priority (A/B/C), notes. | Table exists. Coach can add upcoming matches. |
| 10-12 | Build `competition_proximity` function: days_to_next_event(event_date) → WEEK_TYPE (competition_week, prep_week, off_week). | SQL function returns correct classification. |

**Week 3-4 exit:** Coach can set phase → intent per quality → competition dates. System knows "time of year" and "what's important."

---

### WEEKS 5-6: Athlete Context (Load + Injury)

**Build the athlete awareness layer.**

| Day | Task | Evidence of Done |
|-----|------|-----------------|
| 1-2 | Add `athlete_load_entries` table: athlete_id, session_date, session_type (practice/game/conditioning/S&C), duration_minutes, session_rpe, load_score. | Table exists. Coach can log 1 week of total load. |
| 3-4 | Build rolling 28-day load view: athlete_id, total_load, load_by_type, sessions_by_type. | View returns correct aggregates. |
| 5-6 | Add `injury_modifications` table: athlete_id, exercise_id (or pattern), restriction_type (AVOID/MODIFY/CAUTION), reason, valid_from, valid_until. | Table exists. Coach can say "avoid back squat." |
| 7-8 | Build exercise blocking: Generator receives athlete_id → loads injury_mods → removes unsafe exercises from candidate pool before demand matching. | Back squat blocked by injury_mod → doesn't appear in exercise selection. |
| 9-10 | Add `asymmetry_flags` table: athlete_id, assessment_id, limb (LEFT/RIGHT), value, threshold, flagged_date, resolved_date. | Simple CRUD. |
| 11-12 | Build asymmetry→exercise modifier: if flag exists, generator prioritises unilateral over bilateral exercises for that demand. | "Squat Strength" demand → RFESS prioritized over Back Squat when left leg asymmetry >10%. |

**Week 5-6 exit:** System knows total training load, respects injury modifications, adjusts for limb asymmetry.

---

### WEEKS 7-8: Minimum Effective Dose Engine

**Build the volume intelligence layer.**

| Day | Task | Evidence of Done |
|-----|------|-----------------|
| 1-3 | Create `minimum_effective_dose` table: demand_id, phase, intent (DEVELOP/MAINTAIN/MINIMISE), min_sets_per_week, min_reps_per_week, max_sets_per_week, max_reps_per_week. | Table seeded with cricket-appropriate values. |
| 4-6 | Build MED lookup function: (demand_id, phase, intent) → volume_range. | Returns correct range. |
| 7-8 | Create `progression_rates` table: phase, training_age_group, load_increment_percent, frequency_increase_per_week, max_volume_increase_per_block. | Table seeded. |
| 9-10 | Build progression application: Generator reads phase rate → applies to exercise prescription → respects MED boundaries. | Generator output respects MED caps. |
| 11-12 | Build week-to-week carry-over: Last week's completed load → this week's starting load. Not from scratch each week. | Each week's prescription is based on previous week's actuals, not initial assessment. |

**Week 7-8 exit:** Generator produces phase-appropriate volumes. In-season = MED maintenance. Off-season = development doses.

---

### WEEKS 9-10: Generator Rewrite (Phase-Aware)

**Wire everything together. Replace the deficit-driven path.**

| Day | Task | Evidence of Done |
|-----|------|-----------------|
| 1-2 | Rewrite generator entry point: Input = athlete_id + active coaching_strategy_id. Output = program. | Old entry point replaced. Deficit-driven path is dead. |
| 3-4 | Build phase-aware exercise selection: Phase → filter exercise_demand_mapping (off-season = all exercises, pre-season = moderate complexity, in-season = simple/minimal). | Fast Bowler in-season gets Trap Bar Jump Squat, not Clean Pull. |
| 5-6 | Build competition proximity trim: If week_type = competition_week → reduce volume by 40%, remove heavy eccentrics after day -2. | Batter with match on Saturday gets minimal work Thursday-Friday. |
| 7-8 | Build coach override capture: Every generated program stores (exercise_id, sets, reps, intensity, rest). Coach modifies → stores override with reason. | Generator output matches V2.5 approach. Overrides logged. |
| 9-10 | Build seeding: Seed 30+ exercise_equivalencies rows. Seed MED rows for all 18 demands × 4 phases × 3 intents. | The tables that were empty now have data. |
| 11-12 | Integration test: Generate programs for 5 athlete profiles. Verify all 5 produce reasonable output. | Fast Bowler (off-season + in-season), Spinner, Batter (in-season), All Rounder. |

**Week 9-10 exit:** Generator produces phase-aware programs. Injuries respected. Asymmetry addressed. Competition proximity gates volume.

---

### WEEKS 11-12: Verification & Coach Review

**Prove it works. Fix remaining defects from AUDIT #10.**

| Day | Task | Evidence of Done |
|-----|------|-----------------|
| 1-2 | Fix assessment naming convention: Single convention across all seed data. Fix benchmark inserts (unique names). | All 7 assessments use one convention. 28 benchmark rows (7×4) insert without conflict. |
| 3-4 | Populate `exercise_sport_mapping` for all 20 V1 exercises → Cricket. Current: 19 populated. Target: 35. | All exercises have Cricket specificity ratings. |
| 5-6 | Populate `exercise_demand_mapping` for Olympic lifts (currently 0 of 14 mapped to V2 demands). | Clean Pull → Horizontal Drive Power etc. |
| 7-8 | Run E2E tests. Fix remaining failures. Target: 0 failures. | `test_e2e_integration.py` passes completely. |
| 9-10 | Mock removal preparation: Replace mock repository data with actual seed data. Verify all tests pass with real data. | Tests pass without mock data. |
| 11-12 | Coach review session: Have an S&C coach (internal or external) review generated programs for 3 different athletes/phases. Collect feedback. | 3 coach-credible programs exist. Coach says "I would use this as a starting point." |

**Week 11-12 exit:** All tests pass. Seed data is consistent. A coach has reviewed and found the output credible.

---

### Week-by-Week Summary

| Week | Theme | Key Deliverable |
|------|-------|----------------|
| 1-2 | DELETE | 6+ tables/files removed, seed data unified |
| 3-4 | COACH STRATEGY | Phase + Intent + Calendar model working |
| 5-6 | ATHLETE CONTEXT | Injuries + Asymmetry + Total Load |
| 7-8 | DOSE INTELLIGENCE | MED tables + Progression rates seeded |
| 9-10 | GENERATOR REWRITE | Phase-aware program generation |
| 11-12 | VERIFICATION | Tests pass, coach review positive |

---

## SECTION 8 — Final Verdict

### "What is the smallest version of FORGE that a real S&C coach would actually use?"

**Answer:** A system that can answer these 5 questions correctly:

1. **"What phase is it?"** — And therefore produce a different program for January (pre-season prep) vs June (mid-season).
2. **"What does the coach want to do?"** — Develop power, maintain strength, minimise hypertrophy. Not the same answer for every quality in every phase.
3. **"When is the next competition?"** — And therefore trim volume, remove heavy eccentrics, and switch to maintenance mode in the 48h window before game day.
4. **"What injuries does this athlete have?"** — And therefore NEVER suggest exercises that are contraindicated, regardless of demand score. No back squats for the athlete with spondylolysis history.
5. **"Is the athlete ready today?"** — And therefore produce a program that accounts for poor sleep, high soreness, or high life stress. This is a Beta feature — MVP can ship without it only if overrides are easy.

That's it. A coach will use a system that:
- Knows what time of year it is
- Asks what the coach wants to achieve
- Respects the competition schedule
- Never hurts the athlete
- Adjusts to how the athlete feels

Everything else — the 18-demand ontology, the movement pattern taxonomies, the specificity ratings, the V2 architecture — is infrastructure that supports these 5 questions. Without the answers to these 5 questions, the infrastructure produces coaching-irrelevant output.

**The current system answers 0 of these 5 questions correctly.** It doesn't know what time of year it is. It doesn't ask what the coach wants. It has no competition awareness. It ignores injury history. It has no readiness concept.

**After 12 weeks of V2.5, it answers questions 1-4 correctly and question 5 partially.** A coach at that point says:

*"The off-season program is credible. I'd change a couple of exercises and the progression rate, but the structure — frequency, volume, exercise selection by phase — is something I can work with. The in-season program is actually useful — it stops me from over-prescribing and keeps my athletes healthy through the season. I wouldn't use it for my ACL rehab guy or my sprint-only athlete, but for my 15 cricket squad athletes? Yes, this saves me real time."*

### What V2.5 Is NOT

- Not a replacement for the coach
- Not a periodisation expert
- Not a return-to-play protocol generator
- Not a 42-sport platform
- Not explainable-AI with natural language reasoning

### What V2.5 IS

- A structured starting point that's good enough that a coach modifies rather than rewrites
- A load-aware, phase-appropriate, injury-respecting program generator
- Cricket-only, 5 roles, 4 phases, 8-10 qualities
- 12 weeks of engineering to build, then real-world validation

**Final Score for V2.5 Viability: 72/100** — Credible enough for a coach to use for 80% of their athlete caseload (cricket squad athletes in standard training phases). Not credible for specialised populations (RTP, elite peaking, combat/endurance sports) until additional sport-specific work is done.

### What Success Looks Like After 12 Weeks

A cricket S&C coach opens the system:

1. **Selects athlete**: Fast Bowler, in-season
2. **Sees current phase**: In-Season (ends March 15)
3. **Sees coach intent**: Power MAINTAIN, Strength MAINTAIN, Acceleration MAINTAIN, Rotational Power MAINTAIN (sensible defaults for in-season)
4. **Sees next match**: Saturday, 4 days away
5. **Sees active injury**: Previous stress fracture (back squat >80% blocked)
6. **Reviews generated program**:

```
Session 1 (Wednesday, Day -3):
  A1: Trap Bar Deadlift — 3×3 @ 85% (RPE 8)
  B1: Trap Bar Jump Squat — 3×3 @ 30% 1RM (max intent)
  B2: MB Rotational Chest Pass — 3×6 each @ 4kg (max velocity)
  C1: Cable Pallof Press — 3×10s each @ moderate
  C2: Single-Leg RDL — 3×8 each @ light (asymmetry flag active)

Session 2 (Thursday, Day -2):
  A1: Med Ball Slam — 3×5 @ max effort
  A2: A-Skip — 3×20m
  B1: Bodyweight Squat — 2×10 (activation)
  B2: Prone Hold — 3×30s
  (Reduced volume: competition proximity)
```

The coach thinks: *"I'd swap Trap Bar Deadlift for block pulls, and reduce the Pallof volume, but this is close enough to what I'd write myself. Good starting point."*

That's V2.5.

---

### Appendix: V2.5 Domain Model (Final)

```
athletes
  ├── sport_id → sports
  ├── role_id → roles
  ├── development_level (FOUNDATION | DEVELOPMENT | PERFORMANCE)
  ├── total_weekly_capacity (int, per-phase max S&C sessions)
  └── coaching_strategies (1:N)
        ├── phase (OFF_SEASON | PRE_SEASON | IN_SEASON | POST_SEASON | RETURN_TO_PLAY)
        ├── valid_from / valid_to
        └── quality_intents (N)
              ├── demand_id → performance_demands
              ├── intent (DEVELOP | MAINTAIN | MINIMISE)
              └── priority (int)

competition_events (1:N per athlete)
  ├── event_date
  ├── event_type (match | tournament | race)
  └── priority (A | B | C)

injury_modifications (N per athlete)
  ├── exercise_id (nullable — if NULL, applies to movement pattern)
  ├── movement_pattern_id (nullable)
  ├── restriction (AVOID | MODIFY | CAUTION)
  ├── reason (text)
  └── valid_until (nullable — NULL = permanent)

asymmetry_flags (N per athlete)
  ├── assessment_id
  ├── limb (LEFT | RIGHT)
  ├── value / threshold
  └── resolved (boolean)

training_load_entries (many per athlete)
  ├── session_date
  ├── session_type (practice | game | conditioning | S&C)
  ├── duration_minutes
  ├── session_rpe
  └── load_score

minimum_effective_dose (many per demand × phase × intent)
  ├── demand_id → performance_demands
  ├── phase
  ├── intent
  ├── min_sets_per_week
  ├── max_sets_per_week
  └── min_reps_per_week / max_reps_per_week

progression_rates (per phase × development_level)
  ├── phase
  ├── development_level
  ├── load_increment_percent (weekly)
  └── max_volume_increase_per_block (percent)

performance_demands (18 rows — keep current V2 seed)
  ├── name + description
  ├── primary_quality_id → physical_qualities
  ├── primary_pattern_id → movement_patterns
  └── demand_type (currently all 'Biomotor')

role_demand_priority (keep current V2 seed)
exercise_demand_mapping (populate all 35 exercises)
assessment_demand_mapping (keep current V2 seed)
exercise_equivalencies (seed 30+ pairs)

movement_templates (5 — delete Reactive Agility)
template_slots (4 per template — keep as-is)
slot_requirements (keep)
slot_progressions (keep — progression descriptions remain)

programs (keep)
program_weeks (keep — phase awareness added)
program_sessions (keep)
program_session_exercises (keep — actuals columns added by 000024)

athlete_state_snapshots (keep table, remove auto-defaults)
injury_risk_profiles (keep table, population deferred to Beta)
training_load_events (keep — now primary load data source)
acute_chronic_load_view (keep)

domain_events (keep — valuable for all purposes)
coach_feedback → no longer a separate table; overrides logged in domain_events
```

### About the Author of This Document

This synthesis examines Forge at the intersection of software architecture and applied sports science. The author role embodies three perspectives simultaneously:
- **Chief Architect**: Cares about complexity, maintainability, and build sequence
- **Performance Director**: Cares about credible methodology, safe loading, and coach trust
- **Principal Sports Scientist**: Cares about evidence-based decision-making, athlete adaptation, and training theory

All three agree: V2.5 is 12 weeks of work, not 12 months. It requires deletion, not creation. It requires asking the coach what they want, not assuming the data knows. And it requires respecting that the athlete is a human in a season with a calendar, not a set of test scores on a demand graph.
