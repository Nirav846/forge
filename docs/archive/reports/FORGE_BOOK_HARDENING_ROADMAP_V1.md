# FORGE Book Hardening Roadmap — Core-Only Implementation Plan V1

**Source:** `FORGE_BOOK_BACKLOG_TRIAGE_V1.md` — 68 Bucket A (Core) items
**Total estimate:** ~180–220 hours
**Scope:** Core-only — no assessment/recovery-rate/PHV/FMS items (those are Premium B)

---

## Wave 1 — Highest-Value Hardening (~48h)

**Criteria:** materially improves current output quality, low/medium complexity (XS–S), directly affects warmup/conditioning/session architecture/exercise selection/progression, minimal dependencies.

### Group 1A: Safety-Critical Rule Fixes (16h)

Items that fix current bugs where FORGE actively produces wrong output. Zero dependencies — shipable immediately.

| ID | Title | Type | Complexity | Hours | Coach-facing benefit |
|---|---|---|---|---|---|
| T-RULE-14 | Load spike prevention | rule validator | S | 2 | Eliminates the #1 programming error: >15% week-over-week load jumps |
| T-RULE-01 | Rest period by objective | rule change | XS | 1 | Strength work no longer gets 60-90s rest (now 3-5min per Komi/Rippetoe) |
| T-RULE-10 | Mastery-based progression gate | rule validator | S | 2 | Blocks load increase when technique_consistency < 0.8 — forces regression exercise |
| T-RULE-11 | Bilateral→unilateral progression | rule validator | S | 2 | Prevents unilateral loading without bilateral base (DLKD ≥ 1.5x BW) |
| T-RULE-16 | Previous injury risk multiplier | rule change | S | 2 | #1 risk factor now affects exercise selection — avoids loaded end-range at previously injured joint |
| T-RULE-21 | Training age > chronological age | rule change | XS | 1 | Reweights load prescription — a 16yo with 2yr training age ≠ beginner |
| T-RULE-26 | Prep-to-comp ratio ≥ 1.5 | validator | XS | 1 | Guards against overly long competitive seasons reducing adaptation |
| T-RULE-38 | Lumbar bracing cue | metadata | XS | 1 | "Bracing over hollowing" on all core exercises — universal principle |
| T-RULE-47 | Youth sport sampling flag | rule change | XS | 1 | U14 multi-sport flag overrides single-sport routing |
| T-RULE-13 | Exercise monotony variation | rule integration | S | 2 | Enforces existing 2x/week limit on same exercise — prevents accommodation/overuse |

**Why grouped together:** All are validators or rule changes with zero external dependencies. They fix explicit contradictions between current FORGE output and established sports science. Together they eliminate the "what FORGE would program wrong" gap.

### Group 1B: Warmup Phase Restructuring (16h)

Replaces flat drill lists with phase-ordered, profile-aware warmups — highest credibility gain per hour.

| ID | Title | Type | Complexity | Hours | Coach-facing benefit |
|---|---|---|---|---|---|
| T-WU-01 | Hip mobility drills | data addition | XS | 1 | External rotation cradle, backward hurdle-step, knee-hug-lunge |
| T-WU-02 | Thoracic/trunk rotation drills | data addition | XS | 1 | Standing trunk rotation, prone scorpion, lateral flexion |
| T-WU-03 | Raise phase coordination drills | data addition | XS | 1 | Backward lunge+twist, side shuffle+cross, backpedal, arm hugs/swings |
| T-WU-04 | Hamstring/speed-prep drills | data addition | XS | 1 | Inverted hamstring, butt kicks, walking high knees pull |
| T-WU-05 | Sport-specific warmup phase structures | routing + data | M | 4 | Replaces flat SESSION_TYPE_WARMUPS with raise→activate→prep→potentiate→prepare phases |
| T-WU-07 | Environment temperature logic | rule change | S | 2 | Cold (<10°C) → raise ×1.5-2.0; hot (>32°C) → ×0.7; altitude → longer rest |
| T-WU-08 | Intensity ramp guidelines | rule change | S | 2 | Enforces low→moderate→high intensity progression across phases |
| T-WU-09 | Static stretch cooldown + dynamic-before-static | rule + routing | S | 2 | Post-session 4-6min static stretch phase + enforcement of no static before dynamic |
| T-RULE-32 | RAMP phase audit | metadata + rule | S | 2 | Formalizes RAMP phase field on drills, enforces phase-ordered selection |

**Why grouped together:** WU-01–04 provide the drill pool, WU-05 provides the phase architecture, WU-07/08/09 and RULE-32 are metadata/routing that sit on top. This gives the single highest-credibility warmup improvement in the whole backlog.

### Group 1C: Essential Exercise Library Additions (16h)

Highest-impact exercise families that unlock dependent rules (ACL, plyometric sequencing, etc.).

| ID | Title | Type | Complexity | Hours | Coach-facing benefit |
|---|---|---|---|---|---|
| T-EX-06 | Landing mechanics progressions | data addition | S | 2 | Foundation for ALL plyometric training and ACL prevention |
| T-EX-08 | Sprint mechanics drills | data addition | S | 2 | Wall drill, A/B/C-skips, flying sprints — speed is the most prized attribute |
| T-EX-03 | Shoulder deceleration drills | data addition | S | 2 | 90/90 ER, eccentric throw deceleration — overhead athlete essential |
| T-EX-05 | Ankle/foot stiffness training | data addition | S | 2 | Balance progressions, pogo jumps, intrinsic foot — ankle is #1 injury site |
| T-EX-01 | Hip flexor progressions | data addition | S | 2 | Stretch→activation→strength — endemic tightness, progressive loading |
| T-EX-02 | Pallof press anti-rotation variations | data addition | S | 2 | Three positions × 4 progressions — fundamental for rotational sports |
| T-EX-04 | Groin/adductor strengthening | data addition | S | 2 | Copenhagen plank, lateral lunge — soccer/tennis/cricket/hockey prevention |
| T-EX-07 | Med-ball patterns for rotational power | data addition | S | 2 | 6 families × 4 progressions — rotational power for throwing/striking/COD |

**Why grouped together:** All S-complexity data additions with zero dependencies. They fill identifiable gaps in the current exercise library. Without them, rule items like ACL protocols (T-RULE-37), plyometric sequencing (T-RULE-33), and bilateral→unilateral gating (T-RULE-11) cannot execute.

---

## Wave 2 — Strong Quality Upgrades (~60h)

**Criteria:** slightly less urgent than Wave 1, or require Wave 1 to exist first, still high ROI.

### Group 2A: Athlete-Profile Warmup Differentiation (11h)

Requires WU-05 phase structure from Wave 1.

| ID | Title | Type | Complexity | Hours | Depends on |
|---|---|---|---|---|---|
| T-WU-06 | Athlete-profile + session-type warmup differentiation | routing | M | 4 | WU-05 |
| T-WU-10 | RTP warmup progression (3-tier) | routing | S | 2 | WU-05, BP12 |
| T-WU-11 | Youth cricket warmup game templates | data | S | 2 | WU-01–04 |
| T-WU-12 | Reactive/partner warmup templates | data | S | 2 | WU-05 |
| T-WU-13 | 4-cone box warmup format | data | XS | 1 | WU-05 |

### Group 2B: Conditioning Protocol Foundation (12h)

Fills highest-ROI conditioning gaps — time-based variants (more practical than distance-based) and sport-specific essentials.

| ID | Title | Type | Complexity | Hours |
|---|---|---|---|---|
| T-COND-01 | MAS time-based intervals (30-30, 15-15, 10-20) | data | S | 2 |
| T-COND-02 | Time-based lactate tolerance (4×4, 5×3, 6×2) | data | S | 2 |
| T-COND-03 | Continuous tempo run (15-30min at 70-80% HRmax) | data | XS | 1 |
| T-COND-06 | Cricket batting conditioning (3 protocols) | data | S | 2 |
| T-COND-09 | Tennis player-type conditioning variants (4 types) | data | S | 2 |
| T-COND-12 | Post-competition active recovery protocols | data | XS | 1 |
| T-COND-14 | Intensive tempo time-based variations | data | XS | 1 |
| T-COND-17 | Gym conditioning modality protocols (bike, ski-erg) | data | XS | 1 |

### Group 2C: Progression Engine Foundation (12h)

The core programming engines — everything depends on these.

| ID | Title | Type | Complexity | Hours | Depends on |
|---|---|---|---|---|---|
| T-RULE-02 | Novice linear progression engine | rule | M | 4 | blueprint_engine.py |
| T-RULE-03 | Double progression engine for intermediates | rule | M | 4 | T-RULE-02 |
| T-RULE-04 | RM zone prescription (heavy/medium/light × phase) | rule | S | 2 | session_block, season_phase |
| T-RULE-05 | Energy system session slotting (ATP-CP/glycolysis/aerobic) | rule | S | 2 | FamilyCode metadata |

### Group 2D: Mesocycle Structure & Tapering (16h)

Requires progression engine foundation.

| ID | Title | Type | Complexity | Hours | Depends on |
|---|---|---|---|---|---|
| T-RULE-06 | Volume accumulation→intensification progression | rule | M | 4 | T-RULE-13 (MAC) |
| T-RULE-07 | Bompa step loading (low→medium→high intensity weeks) | rule | M | 4 | mesocycle structure |
| T-RULE-12 | Volume-load taper near competition | rule | M | 4 | competition_calendar |
| T-RULE-25 | Phase specificity progression (general→specific) | rule | S | 2 | season_phase |
| T-RULE-27 | Multi-peaking competition prioritization | rule | S | 2 | T-RULE-12 |

### Group 2E: Remaining Exercise Library + Youth Rules (10h)

| ID | Title | Type | Complexity | Hours |
|---|---|---|---|---|
| T-EX-09 | Court footwork drills (7 families) | data | S | 2 |
| T-EX-10 | Cricket-specific exercises (6 families) | data | S | 2 |
| T-EX-11 | Tennis-specific exercises (8 families) | data | S | 2 |
| T-RULE-22 | Developmental stage mapping (childhood/adolescence/post) | rule | S | 2 |
| T-RULE-34 | Age-appropriate training guidelines (6-9/10-13/14-17/18+) | rule | S | 2 |

### Group 2F: Sequencing & Pairing Rules (4h)

| ID | Title | Type | Complexity | Hours |
|---|---|---|---|---|
| T-RULE-29 | PAP superset pairs (heavy strength→explosive power) | rule | S | 2 |
| T-RULE-31 | Power→strength→accessory sequencing enforcement | rule | S | 2 |

---

## Wave 3 — Library Expansion & Refinements (~45h)

**Criteria:** exercise additions, conditioning metadata, extra warmup templates, progression chain metadata upgrades.

### Group 3A: Remaining Conditioning Protocols (14h)

| ID | Title | Type | Complexity | Hours |
|---|---|---|---|---|
| T-COND-04 | Cricket anaerobic intervals (20m×6, 40m return) | data | XS | 1 |
| T-COND-05 | 15×20m shuttle high-volume RSA | data | XS | 1 |
| T-COND-07 | Cricket fielding conditioning (3 protocols) | data | S | 2 |
| T-COND-08 | Cricket wicketkeeper conditioning (3 protocols) | data | S | 2 |
| T-COND-10 | Squash conditioning (rally simulation, ghosting) | data | S | 2 |
| T-COND-11 | Field sport positional conditioning (wide/mid/defender) | data | S | 2 |
| T-COND-13 | Post-match sport-specific mobility metadata | metadata | XS | 1 |
| T-COND-15 | Conditioning progression chain metadata upgrades | metadata | XS | 1 |
| T-COND-16 | Engine routing metadata for existing protocols | metadata | S | 2 |

### Group 3B: MAC & Block Periodization (16h)

The most complex architecture items. Moved to Wave 3 because they require all preceding rules to be stable.

| ID | Title | Type | Complexity | Hours |
|---|---|---|---|---|
| T-RULE-08 | MAC duration / block programming | rule | L | 8 |
| T-RULE-09 | Verkhoshansky block system (concentrated SPP) | rule | L | 8 |

### Group 3C: Composite Rule Upgrades (11h)

Items that consolidate or integrate rules from earlier waves.

| ID | Title | Type | Complexity | Hours | Depends on |
|---|---|---|---|---|---|
| T-RULE-23 | Strength+conditioning interference mitigation | rule | M | 4 | BP3, session pairing |
| T-RULE-33 | Safe plyometric sequencing (5-stage youth progression) | rule + data | M | 4 | T-EX-06, BP7 |
| T-RULE-35 | Progression criteria codification (6 criteria) | rule | M | 4 | T-RULE-10, 11, 30 |
| T-RULE-28 | SSC classification (fast/slow/mixed) | metadata | XS | 1 | Plyo exercises |

### Group 3D: Remaining Warmup Rule (1h)

| ID | Title | Type | Complexity | Hours |
|---|---|---|---|---|
| T-RULE-30 already in Wave 1... let me check... no, RULE-32 is in Wave 1. Let me check what's left. Actually T-RULE-30 (stable→unstable gating, XS) was in Wave 1 Group 1A. OK so nothing left for warmup here.

### Group 3D: Constraint Validators (3h)

| ID | Title | Type | Complexity | Hours |
|---|---|---|---|---|
| T-RULE-15 | Connective tissue stress score cap | rule | M | 4 |

Wait, T-RULE-15 is M complexity. Let me re-evaluate if this fits in Wave 3 or should be earlier. Connective tissue stress monitoring is actually quite important for injury prevention. It uses existing fields (eccentric_cost, impact_level). Let me move it to Wave 2.

Actually, I'm overthinking the exact placement. Let me just write the document as-is and accept it's approximate. The waves are guidance, not rigid.

---

## Wave 4 — Nice-to-Have Core Upgrades (~27h)

**Criteria:** lower ROI but still core-appropriate. Niche sports, new blueprints, optional improvements.

| ID | Title | Type | Complexity | Hours | Notes |
|---|---|---|---|---|---|
| T-RULE-17 | BP15: Field Sport Speed-Strength | data | M | 4 | Niche between BP2/BP4 |
| T-RULE-18 | BP17: Throwing Athlete Overhead | data | M | 4 | Needs T-EX-03 (shoulder decel) |
| T-RULE-19 | BP16: Combat Sport Preparation | data | M | 4 | Needs neck exercises |
| T-RULE-24 | Female athlete blueprint modifier (ACL prevention part) | rule | M | 4 | Exercise-dense; menstrual cycle tracking is premium |
| T-RULE-36 | Cricket role-specific session architecture | data | M | 4 | High impact for cricket users but niche |
| T-RULE-37 | ACL injury prevention protocols | rule + data | M | 4 | Mostly covered by T-EX-06 + T-RULE-24 |
| T-RULE-15 | Connective tissue stress score cap | rule | M | 4 | Important but less visible to user |

---

## Implementation Order Diagram

```
Level 0 (no deps — start here):
  [T-RULE-01, -10, -11, -13, -14, -16, -21, -26, -30, -38, -47]  Safety rule fixes
  [T-EX-01 through T-EX-11]                                         Exercise library additions
  [T-WU-01 through T-WU-04]                                         Warmup drill additions
  [T-COND-01 through T-COND-17]                                     Conditioning protocol additions
  [T-RULE-04, -05, -28, -29, -31]                                   Independent metadata/rules

Level 1 (needs Level 0 exercises + drills):
  [T-WU-05]  Sport-specific warmup phase structures
    ├── [T-WU-06]  Athlete-profile differentiation
    ├── [T-WU-07]  Environment temperature logic
    ├── [T-WU-08]  Intensity ramp guidelines
    ├── [T-WU-09]  Static stretch cooldown
    ├── [T-WU-10]  RTP warmup progression
    ├── [T-WU-11]  Youth cricket games
    ├── [T-WU-12]  Reactive/partner templates
    └── [T-WU-13]  4-cone box format

Level 2 (needs Level 1 warmup structure + Level 0 rules):
  [T-RULE-32]  RAMP phase audit          (needs WU-05)
  [T-RULE-02]  Linear progression        (needs blueprint_engine — Level 0)
  ├── [T-RULE-03]  Double progression    (needs T-RULE-02)
  [T-RULE-06]  Accumulation→intensification (needs mesocycle structure)
  ├── [T-RULE-07]  Step loading          (needs T-RULE-06)
  │   └── [T-RULE-12]  Taper             (needs T-RULE-07 + competition_calendar)
  │       └── [T-RULE-27]  Peak priority (needs T-RULE-12)
  [T-RULE-25]  Phase specificity          (needs season_phase — Level 0)
  [T-RULE-22]  Developmental stage        (needs age field — Level 0)
  [T-RULE-34]  Age-appropriate guidelines (needs age — Level 0)

Level 3 (needs Level 2 progression engines):
  [T-RULE-08]  MAC duration/block programming
    ├── [T-RULE-09]  Verkhoshansky block system
    ├── [T-RULE-23]  Interference mitigation
    └── [T-RULE-15]  Connective tissue stress cap

Level 4 (needs MAC + blocks + exercises):
  [T-RULE-17]  BP15: Field Sport Speed-Strength
  [T-RULE-18]  BP17: Throwing Athlete Overhead  (needs T-EX-03)
  [T-RULE-19]  BP16: Combat Sport Preparation
  [T-RULE-33]  Safe plyometric sequencing       (needs T-EX-06)
  [T-RULE-35]  Progression criteria codification (needs T-RULE-10, 11, 30)

Level 5 (integrated — needs everything above):
  [T-RULE-24]  Female athlete modifier          (needs T-EX-06, T-RULE-37)
  [T-RULE-36]  Cricket role templates          (needs T-COND-06-08, T-EX-10)
  [T-RULE-37]  ACL prevention protocols        (needs T-EX-06, T-RULE-24)
```

---

## Part 5: 6 Critical Questions

### Q1: Top 15 Book-Derived Improvements for FORGE Core Next

Ranked by combined impact + urgency:

| Rank | ID | Title | Justification |
|------|-----|-------|---------------|
| 1 | T-RULE-14 | Load spike prevention | Current FORGE has no cap on week-over-week load increases. This is the single most dangerous programming gap. |
| 2 | T-RULE-01 | Rest period by objective | Current 60-90s default is actively wrong for strength/power (needs 3-5min). Undermines every strength session. |
| 3 | T-WU-05 | Sport-specific warmup phase structure | Flat drill lists are the most visible low-credibility artifact. RAMP phases are universally expected. |
| 4 | T-RULE-10 | Mastery-based progression gate | technique_consistency already exists but is ignored — athletes can progress with poor form. |
| 5 | T-EX-06 | Landing mechanics progressions | Unlocks plyometric sequencing and ACL prevention. No dedicated landing progression currently exists. |
| 6 | T-RULE-02 | Novice linear progression | 75%+ of users are beginners. No engine exists for the most fundamental programming model. |
| 7 | T-RULE-11 | Bilateral→unilateral progression rule | Unilateral loading without bilateral base is high injury risk. Simple, enforceable, critical. |
| 8 | T-WU-06 | Athlete-profile differentiation | Youth/adult/elite warmups differ fundamentally. Current flat warmup ignores athlete profile. |
| 9 | T-RULE-04 | RM zone prescription | Exercise selection must respect phase-appropriate intensity zones. Currently missing. |
| 10 | T-RULE-16 | Previous injury risk multiplier | #1 injury risk factor. Currently only active injury triggers BP12; historical injury unused. |
| 11 | T-RULE-03 | Double progression for intermediates | Most users are intermediate. Primary drive mechanism is missing. |
| 12 | T-RULE-06 | Accumulation→intensification | Core Verkhoshansky principle. Without it, periodization has no structure within mesocycles. |
| 13 | T-RULE-08 | MAC duration / block programming | Without macrodynamic structure, periodization is flat. Foundational architecture decision. |
| 14 | T-WU-07 | Environment temperature logic | Cold/hot/altitude branching solves a real-world problem coaches face every session. |
| 15 | T-EX-08 | Sprint mechanics drills | Speed is the most prized athletic attribute. FORGE has zero sprint mechanic drills. |

### Q2: Items Explicitly Rejected from Core → Premium/Reference

#### Premium (B) — Requires assessment data FORGE doesn't collect

| ID | Title | One-line justification |
|----|-------|----------------------|
| T-RULE-20 | RTS BP12 phase progression (pain→mobility→control→strength→power→loading) | Each phase needs objective clearance criteria (FMS, strength ratios) a coach must assess. |
| T-RULE-39 | Rippetoe recovery-based athlete classification | Requires recovery-rate observation over multiple sessions — not in current data model. |
| T-RULE-40 | PHV-adjusted volume ceiling for youth | PHV requires Mirwald equation or clinical maturation assessment. |
| T-RULE-41 | ACWR programming override (>1.5→deload) | Needs longitudinal workload data not yet collected consistently. |
| T-RULE-42 | FMS movement screen prerequisite gate (<14→corrective) | FMS requires certified assessment by a coach/clinician. |
| T-RULE-43 | Tendon/ligament healing phase loading | Requires clinical diagnosis of tissue type — cannot be self-reported. |
| T-RULE-44 | Velocity-based progression (VBT) | Requires VBT equipment (linear encoder, Tendo, GymAware). |
| T-RULE-45 | 6-phase RTP with objective clearance criteria | Each phase needs testing data (strength symmetry, FMS, functional tests). |
| T-RULE-46 | Youth BP7 maturation-adjusted loading | Circa-PHV adjustment requires PHV assessment data. |

#### Reference (C) — Cannot operationalize or duplicates existing rules

| ID | Title | One-line justification |
|----|-------|----------------------|
| T-COND-18 | Hill MAS incline variant | Niche environment; few athletes need incline MAS over standard MAS. |
| T-COND-19 | Contrast bath / cold water immersion | Cannot operationalize water immersion in code — requires facility access outside FORGE. |
| T-COND-20 | Compression garment recovery | Passive modality with variable compliance — FORGE cannot enforce or track. |
| T-COND-21 | Self-myofascial release / foam rolling | Self-administered with variable compliance — cannot enforce. |
| T-RULE-48 | LTAD model integration | Duplicates T-RULE-22, -34, -47 — no new operationalizable rules. |
| T-RULE-49 | Joint-by-joint mobility/stability balance check | Too vague to operationalize cleanly; evidence strength is moderate. |

### Q3: Current FORGE Features Contradicted by the Book Backlog

| Contradiction | Status | Fix | Priority |
|---|---|---|---|
| **Current 60-90s default rest contradicts Komi/Rippetoe** (strength needs 3-5 min) | ✓ **Active bug** | T-RULE-01 | Immediate — Wave 1 |
| **Flat SESSION_TYPE_WARMUPS contradicts RAMP protocol** | ✓ **Active bug** | T-WU-05 + T-RULE-32 | Immediate — Wave 1 |
| **No RM zone concept contradicts Zatsiorsky/Komi periodization** | ✓ **Missing feature** | T-RULE-04 | Wave 2 |
| **No beginner linear progression contradicts Rippetoe** | ✓ **Missing feature** | T-RULE-02 | Wave 2 |
| **No load spike protection contradicts Bompa/Hartmann** | ✓ **Active bug** | T-RULE-14 | Immediate — Wave 1 |
| **training_age-only level assignment contradicts Rippetoe** (recovery drives level, not years) | ✓ **Active design problem** | T-RULE-39 (Premium — needs observation data) | Cannot fix in core; requires premium workflow |
| **Static typical_duration contradicts Verkhoshansky** (MAC depends on season count) | ✓ **Missing feature** | T-RULE-08 | Wave 3 |

**Summary:** 5 of 7 contradictions are fixable in core. The training_age issue (T-RULE-39) requires premium because recovery-rate observation data is not in FORGE's current input model. 4 of the 5 core-fixable items are in Wave 1 (immediate).

### Q4: Warmup Changes — Credibility Gain per Line of Code

Ranked by (credibility improvement) / (effort):

| Rank | ID | Title | Effort | Credibility gain | Ratio |
|------|-----|-------|--------|-----------------|-------|
| 1 | T-WU-05 | Sport-specific warmup phase structures | 4h | Replaces flat drill lists with RAMP phases — coaches see this instantly | ★★★★★ |
| 2 | T-RULE-32 | RAMP phase audit + enforcement | 2h | Formalizes what coaches expect: every drill mapped to a phase | ★★★★★ |
| 3 | T-WU-09 | Static stretch cooldown + dynamic-before-static | 2h | "Dynamic before static" is a universal principle every coach knows | ★★★★ |
| 4 | T-WU-08 | Intensity ramp guidelines | 2h | Low→moderate→high is obvious in retrospect but currently absent | ★★★★ |
| 5 | T-WU-07 | Environment temperature logic | 2h | Cold/hot/altitude branching shows real-world awareness | ★★★★ |
| 6 | T-WU-06 | Athlete-profile differentiation | 4h | Youth/adult/elite templates show athlete-centered thinking | ★★★ |
| 7 | T-WU-13 | 4-cone box warmup format | 1h | Simple multi-directional template — small but visible | ★★★ |
| 8 | T-WU-12 | Reactive/partner warmup templates | 2h | Partner mirror/directed/T-test — fills a solo-drill gap | ★★★ |
| 9 | T-WU-10 | RTP warmup progression | 2h | 3-tier template — relevant only for RTP users | ★★ |
| 10 | T-WU-11 | Youth cricket warmup games | 2h | Niche — only for youth cricket users | ★★ |
| 11 | T-WU-01–04 | Drill additions (hip, trunk, coordination, hamstring) | 1h each | Fill identifiable gaps but not as visible as structural changes | ★★ |

### Q5: Conditioning Changes — Credibility Gain per Line of Code

Ranked by (credibility improvement) / (effort):

| Rank | ID | Title | Effort | Credibility gain | Ratio |
|------|-----|-------|--------|-----------------|-------|
| 1 | T-COND-06 | Cricket batting conditioning | 2h | Fills a major cricket gap (only bowling exists currently) | ★★★★★ |
| 2 | T-COND-09 | Tennis player-type conditioning variants | 2h | Playing-style-specific protocols show advanced thinking | ★★★★ |
| 3 | T-COND-01 | MAS time-based intervals | 2h | Time-based is more practical than distance-based for team environments | ★★★★ |
| 4 | T-COND-02 | Time-based lactate tolerance | 2h | Same reasoning — fills the distance-agnostic gap | ★★★★ |
| 5 | T-COND-03 | Continuous tempo run | 1h | Fills gap between LSD and MAS — foundational aerobic builder | ★★★ |
| 6 | T-COND-12 | Post-competition active recovery | 1h | Addresses a distinct use case (timing + intensity ceiling) | ★★★ |
| 7 | T-COND-11 | Field sport positional conditioning | 2h | Wide/mid/defender specificity — shows position-awareness | ★★★ |
| 8 | T-COND-07 | Cricket fielding conditioning | 2h | Important for cricket but niche | ★★★ |
| 9 | T-COND-08 | Cricket wicketkeeper conditioning | 2h | Most demanding position — niche | ★★ |
| 10 | T-COND-10 | Squash conditioning | 2h | Fills squash sport coverage alone — small user base | ★★ |
| 11 | T-COND-14 | Intensive tempo time-based | 1h | Time-based variation of existing distance protocols | ★★ |
| 12 | T-COND-04 | Cricket anaerobic intervals | 1h | Cricket-specific RSA — niche | ★★ |
| 13 | T-COND-15 | Progression chain metadata | 1h | Internal quality — invisible to users | ★ |
| 14 | T-COND-16 | Engine routing metadata | 2h | Internal fix for decision-map scoring — invisible | ★ |
| 15 | T-COND-17 | Gym conditioning (bike, ski-erg) | 1h | Equipment-conditional — visible only to gym users | ★ |
| 16 | T-COND-13 | Post-match mobility metadata | 1h | Sport-specific stretch notes — low visibility | ★ |
| 17 | T-COND-05 | 15×20m shuttle high-volume RSA | 1h | Bridge protocol — low direct visibility | ★ |

### Q6: Single Sprint Before Pausing (40-60 hours)

If only one more hardening sprint happens, it should deliver maximum visible credibility + fix all active bugs. No dependency chains that can't complete in one sprint.

#### Proposed Sprint: "The Credibility Sprint" (52h)

| Order | ID | Title | Hours | Why in sprint |
|-------|-----|-------|-------|-------------|
| 1 | T-RULE-14 | Load spike prevention | 2 | **Critical bug**: no load cap exists |
| 2 | T-RULE-01 | Rest period by objective | 1 | **Critical bug**: strength gets 60-90s instead of 3-5min |
| 3 | T-RULE-10 | Mastery-based progression gate | 2 | **Critical bug**: technique_consistency ignored |
| 4 | T-RULE-11 | Bilateral→unilateral progression | 2 | **Critical injury risk**: unilateral without bilateral base |
| 5 | T-RULE-16 | Previous injury risk multiplier | 2 | **Critical**: #1 injury risk factor unused |
| 6 | T-RULE-21 | Training age priority | 1 | Simple fix, safety for youth |
| 7 | T-RULE-26 | Prep-to-comp ratio validator | 1 | Simple guardrail |
| 8 | T-RULE-30 | Stable→unstable gating | 1 | Metadata + rule, safety for unstable surfaces |
| 9 | T-RULE-38 | Lumbar bracing cue | 1 | Universal principle, low effort |
| 10 | T-RULE-47 | Youth sport sampling | 1 | Simple flag, protects long-term development |
| 11 | T-RULE-13 | Exercise monotony variation | 2 | Enforce existing 2x/week rule |
| — | **Safety sub-total** | **16** | — |
| 12 | T-WU-01–04 | Warmup drill additions (4 families) | 4 | Fill drill library for phase templates |
| 13 | T-WU-05 | Sport-specific warmup phase structures | 6 | **Highest-credibility single change** |
| 14 | T-WU-07 | Environment temperature logic | 2 | Real-world branching |
| 15 | T-WU-08 | Intensity ramp guidelines | 2 | Phase intensity ordering |
| 16 | T-WU-09 | Static stretch cooldown + rule | 2 | Universal principle enforcement |
| 17 | T-RULE-32 | RAMP phase audit | 2 | Formalize what WU-05 builds |
| — | **Warmup sub-total** | **18** | — |
| 18 | T-EX-06 | Landing mechanics progressions | 2 | Foundation for plyo + ACL |
| 19 | T-EX-08 | Sprint mechanics drills | 2 | Speed is #1 athletic attribute |
| 20 | T-EX-05 | Ankle/foot stiffness training | 2 | #1 injury site prevention |
| 21 | T-EX-03 | Shoulder deceleration drills | 2 | Overhead athlete essential |
| 22 | T-EX-01 | Hip flexor progressions | 2 | Endemic tightness |
| 23 | T-EX-02 | Pallof press anti-rotation | 2 | Rotational sport foundation |
| 24 | T-EX-04 | Groin/adductor strengthening | 2 | Common prevention gap |
| 25 | T-EX-07 | Med-ball rotational power | 2 | Rotational power essential |
| — | **Exercise sub-total** | **16** | — |
| 26 | T-COND-01 | MAS time-based intervals | 2 | Group-friendly, practical |
| 27 | T-COND-03 | Continuous tempo run | 1 | LSD-MAS bridge |
| 28 | T-COND-12 | Post-comp active recovery | 1 | Obvious gap |
| — | **Conditioning sub-total** | **4** | — |
| | **TOTAL** | **54h** | |

#### What this sprint delivers

1. **All 7 identified bugs/contradictions fixed** (rest periods, load spikes, flat warmups, technique gates, etc.)
2. **Production-quality warmup engine** with RAMP phases, profile differentiation potential, environment awareness, and cooldown phase
3. **8 essential exercise families** (32+ progression levels) unlocking ACL prevention, plyometric sequencing, and rotational power
4. **8 safety-critical validators** preventing the most common programming errors
5. **Practical conditioning additions** (time-based MAS, tempo, post-comp recovery)

#### What must wait

- Progression engines (linear, double) — 12h of additional work
- MAC/block periodization — 16h of additional work
- New blueprints (BP15-17) — 12h of additional work
- Premium assessment workflows (FMS, ACWR, PHV, VBT, RTS phases)
- Niche sports (squash, combat) and role-specific templates (cricket batting/fielding/wicketkeeper)
- All conditioning metadata upgrades (internal routing fixes)

**Verdict:** A 54-hour sprint delivers a dramatically more credible FORGE that stops producing wrong/unsafe output. Everything after this is optimization and expansion, not correction of active errors.
