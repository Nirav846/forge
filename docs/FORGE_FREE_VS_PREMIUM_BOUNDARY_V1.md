# FORGE Free/Core vs Premium — Product Boundary V1

**Purpose:** Define the explicit product boundary between FORGE Free (Core/Bucket A) and FORGE Premium (Bucket B). Every free user sees a credible, coach-like system that works with zero assessment data. Premium unlocks data-driven precision.

**Source:** FORGE_BOOK_BACKLOG_TRIAGE_V1.md (68 Core, 12 Premium, 14 Reference items)

---

## Section A — FORGE FREE / CORE Definition

FORGE Free is a **deterministic, input-limited training system** that delivers credible programs using only profile-level data. It asks nothing of the user beyond what a casual athlete knows about themselves: their sport, age, training history, available equipment, and schedule. No tests, no screens, no wearable data. The system mirrors what a competent S&C coach would prescribe after a 5-minute intake conversation.

The free system is not a "trial" or a "demo" — it is a complete training generator for athletes who train by feel, by schedule, and by coach observation rather than by laboratory metrics. Its limitations are explicit and honest: it cannot adjust for injury history at tissue level, cannot periodize from test results, and cannot gate exercise selection on movement quality scores. Within those bounds, it applies every established principle of periodization: load progression, energy system specificity, phase-appropriate intensity, competition tapering, and fatigue management.

Free exists because the majority of athletes globally have **no access to FMS screening, VBT equipment, ACWR dashboards, or maturation assessment**. FORGE Free should be the best possible training program generator for that athlete. When those assessment tools become available, the user upgrades to Premium.

### Inputs the free system uses

Starts from what currently exists in FORGE's model, plus items from Bucket A that introduce new fields:

- **sport** (existing)
- **training_goal** (existing)
- **training_age** / **level** (existing — level determines linear/double/advanced progression engine)
- **equipment_profile** — field only / basic gym / commercial gym / elite facility (existing)
- **environment** — gym / ground / court (existing, extended by T-WU-07 for temperature branching)
- **available_minutes** (existing)
- **session_frequency** (existing)
- **days_to_match / competition_proximity** (existing — drives taper, T-RULE-12)
- **age_band** (existing — drives T-RULE-22 developmental stage, T-RULE-34 age-group guidelines)
- **cricket_role** — batsman / bowler / wicketkeeper / all-rounder (existing, extended by T-RULE-36 for role-specific slot architecture)
- **tennis_playing_style** — serve+volley / baseliner / counterpuncher / all-court (new, from T-COND-09)
- **position** — wide_player / central_midfielder / defender (new, from T-COND-11 for field sport positional conditioning)
- **sex** — male / female (existing, drives T-RULE-24 ACL prevention modifier)
- **recovery_capacity** — good / average / poor (new — subjective self-report flag used by T-RULE-39 free version)
- **technique_consistency** — 0.0–1.0 (existing, newly enforced by T-RULE-10 mastery gate)
- **competitive_peak_priority** — primary / secondary / tertiary (new, from T-RULE-27)
- **sport_sampling** — bool for U14 multi-sport flag (new, from T-RULE-47)

### What the free system does NOT depend on

These inputs are never required, never prompted, and never used for routing in Free:

- FMS total score or asymmetry flags
- ACWR / chronic workload ratio
- MAS (maximum aerobic speed) test results
- Sprint test results (10m, 20m, 30m)
- Jump test results (CMJ, squat jump, drop jump)
- Estimated or measured 1RM strength test results
- ROM (range of motion) screen results
- Pain or asymmetry data
- Menstrual cycle phase
- PHV / maturation stage assessment
- Velocity-based training (VBT) data
- Heart rate variability (HRV)
- Wellness questionnaire scores
- Injury history with tissue type and healing phase
- Active injury restrictions with tissue specificity

### What the free system delivers

Without test data, FORGE Free still delivers:

- **Periodized macrocycles** (T-RULE-08: MAC duration by competition calendar)
- **Verkhoshansky block periodization** (T-RULE-09: concentrated SPP blocks)
- **Bompa step loading** (T-RULE-07: low→medium→high intensity week patterns)
- **Phase-specific progression** (T-RULE-06: accumulation→intensification→realization; T-RULE-25: general→specific)
- **RM-zone-appropriate exercise selection** (T-RULE-04: heavy/medium/light zones)
- **Energy-system-appropriate conditioning** (T-RULE-05: ATP-CP/glycolysis/aerobic slotting)
- **Novice linear progression** (T-RULE-02) and **intermediate double progression** (T-RULE-03)
- **Mastery-based technique gate** (T-RULE-10: blocks progression when technique_consistency < 0.8)
- **Bilateral→unilateral gating** (T-RULE-11: minimum strength ratio before unilateral loading)
- **Load spike prevention** (T-RULE-14: 15% week-over-week cap)
- **Connective tissue stress cap** (T-RULE-15)
- **Previous injury risk multiplier** (T-RULE-16: modifies exercise selection without tissue-specific loading)
- **Competition tapering** (T-RULE-12, T-RULE-27)
- **Rest period durations by objective** (T-RULE-01: 3–5min strength, 60–90s hypertrophy, 30–60s endurance)
- **Stable→unstable surface gating** (T-RULE-30)
- **Power→strength→accessory sequencing** (T-RULE-31)
- **5-stage plyometric progression** (T-RULE-33) with age-group volume caps
- **Age-group-appropriate training** (T-RULE-34: 6–9 fundamental, 10–13 patterns+basic strength, 14–17 strength+power, 18+ advanced)
- **RAMP phase-ordered warmups** (T-RULE-32) with sport-specific templates (T-WU-05), environment branching (T-WU-07), intensity ramps (T-WU-08), RTP warmup tiers (T-WU-10), youth games (T-WU-11), reactive/partner formats (T-WU-12)
- **ACL prevention exercises** for female athletes (T-RULE-24, T-RULE-37) without cycle phase tracking
- **Conditioning progression chains** (T-COND-15) with time-based and distance-based MAS/LT/IT protocols
- **Sport-specific conditioning** for cricket batting (T-COND-06), fielding (T-COND-07), wicketkeeper (T-COND-08), tennis playing styles (T-COND-09), squash (T-COND-10), field sport positions (T-COND-11)
- **Sport-specific blueprints** for field sport speed-strength (BP15), combat sport prep (BP16), throwing athlete overhead (BP17)
- **Cricket role-specific session architecture** (T-RULE-36)
- **Exercise library expansions** across 11 domains (hip flexors, Pallof press, shoulder deceleration, groin/adductor, ankle/foot, landing mechanics, med-ball patterns, sprint mechanics, court footwork, cricket-specific, tennis-specific)

Any S&C coach would recognise this as a capable, principled training system. Its output is credible for any athlete training without diagnostic assessment data.

---

## Section B — FORGE PREMIUM Definition

FORGE Premium is an **assessment-driven training system** that uses objective measurement data to override, gate, and personalise every dimension of program generation. Where Free is deterministic from profile inputs, Premium is responsive to actual athlete data: movement quality scores gate exercise selection, workload ratios trigger deloads, test results set precise intensity zones, maturation stage adjusts volume ceilings, and injury tissue type governs loading protocols.

Premium requires an administering coach or clinician who collects and enters assessment data. The system does not assume self-report for clinical-grade inputs (tissue type, FMS, VBT, PHV). The premium workflow is designed for S&C coaches working with assessed athletes — school strength programs, academy setups, college teams, and professional environments where screening infrastructure exists.

The free-to-premium boundary is not artificial. Every Premium feature requires data that Free cannot plausibly collect or validate. Premium does not simply add "more features" — it adds a **different class of features** that depend on a measurement feedback loop. A free user who has never done an FMS screen cannot benefit from an FMS gate. A free user who has never worn a VBT device cannot use velocity zones. Premium is the system that makes that data work.

### Premium-only inputs

These are never collected or prompted in Free. When present in the athlete profile, they unlock Premium features:

- **injury_history** — structured timeline with injury date, tissue type (muscle/tendon/ligament/bone), body part, severity grade, and return-to-play date
- **active_injury_restrictions** — current movement prohibitions with clearance criteria
- **fms_total_score** — integer 0–21 from certified Functional Movement Screen
- **fms_asymmetry_flags** — list of asymmetry scores > 1 per movement
- **acwr_value** — acute:chronic workload ratio (requires 4+ weeks of load tracking)
- **mas_test_result** — maximum aerobic speed in m/s from field or lab test
- **sprint_test_results** — 10m, 20m, 30m split times
- **jump_test_results** — CMJ height (cm), squat jump, drop jump reactive strength index
- **strength_test_results** — estimated or measured 1RM for key lifts (squat, deadlift, bench, pull-up, etc.)
- **rom_data** — range of motion measurements per joint with pain reports
- **asymmetry_data** — bilateral strength/power asymmetry percentages
- **menstrual_cycle_phase** — follicular / ovulatory / luteal / menstrual for female athlete periodization
- **phv_status** — pre-PHV / circa-PHV / post-PHV from Mirwald equation or clinical estimate
- **maturation_stage** — Tanner stage or age-at-PHV offset
- **vbt_velocity_data** — mean velocity (m/s) per exercise per session from linear encoder / Tendo / GymAware
- **wellness_scores** — daily readiness questionnaire (sleep quality, soreness, mood, stress, fatigue)
- **coach_override_notes** — free-text coaching observations that modify program generation

### Premium-only features (from Bucket B items)

Each feature below is described with what it changes, what data it requires, why it cannot live in Free, and its estimated value.

---

#### T-RULE-41: ACWR Programming Override

**What it does differently from free:** Free uses a simple 15% week-over-week load spike cap (T-RULE-14). Premium integrates the acute:chronic workload ratio into real-time blueprint selection. When ACWR > 1.5, the next session is force-routed to a Deload blueprint regardless of the scheduled plan. When ACWR < 0.8 for two consecutive weeks, a reload (controlled load increase) is triggered. ACWR also replaces the flat 15% cap with a dynamic load ceiling: chronic load × 1.5 = maximum acute load, which adapts as the athlete's fitness base grows.

**What data it requires:** Minimum 4 weeks of continuous load data (session RPE × duration, or external load from GPS/accelerometer) to establish the chronic baseline. Requires consistent data entry for every session.

**Why it can't be in free/core:** ACWR is meaningless without longitudinal load tracking. Free users who train inconsistently or skip session logging would see erratic, misleading ACWR values that degrade program quality. The 15% week-over-week cap is a safe, universal fallback.

**Estimated premium value:** Athletes with consistent load tracking get load management that adapts to their actual fitness trajectory rather than a fixed percentage. Reduces non-functional overreaching by routing to deload at the right time rather than on a fixed schedule. For high-volume athletes (2+ sessions/day), this is the difference between sustainable training and accumulated fatigue.

---

#### T-RULE-42: FMS Movement Screen Gate

**What it does differently from free:** Free uses technique_consistency (a coach-reported 0.0–1.0 rating) to gate progression (T-RULE-10) and bilateral/unilateral strength ratios (T-RULE-11) to gate unilateral loading. Premium gates the **entire blueprint assignment** on FMS results. An athlete with FMS total < 14 is routed to a corrective exercise blueprint before any development blueprint. Asymmetry > 1 on any FMS movement forces unilateral-only exercise selection for that movement pattern. Pain during any FMS screen triggers a medical referral route and switches to RTP programming.

**What data it requires:** FMS total score (0–21) and per-movement asymmetry flags. Requires certified FMS assessment by a qualified coach or clinician. Cannot be self-reported reliably.

**Why it can't be in free/core:** FMS certification is a specific qualification. Self-reported movement quality scores are unreliable. Forcing corrective routing based on incorrect scores would produce worse programs than the free system's conservative assumptions (assume movement competence in the absence of evidence).

**Estimated premium value:** For assessed athletes, prevents the single most common programming error: loading movement dysfunction. A squad with average FMS < 14 running a standard strength block is accumulating injury risk with every session. Premium catches this before it happens.

---

#### T-RULE-20: RTS Blueprint Phase Progression (with clearance criteria)

**What it does differently from free:** Free BP12 (Return-to-Sport) is a flat progression by week number: week 1 mobility, week 2 strength start, week 3 loading. Premium replaces week-based progression with **objective clearance gates** between four phases: pain-free ROM → motor control → strength normalization → full loading. The athlete cannot advance without meeting objective criteria: symmetrical ROM, strength within 10% of contralateral side, asymmetry < 5% on FMS, pain-free during phase exercises.

**What data it requires:** FMS scores, bilateral strength test results (isometric or dynamic), ROM measurements, pain reports. Repeated testing at each phase gate.

**Why it can't be in free/core:** Clearance gates require repeated assessment data — the system must know the athlete's current state to authorise advancement. Without test data, week-number progression is a credible approximation. With test data, it becomes clinical-grade return-to-sport programming.

**Estimated premium value:** Reduces re-injury rate during RTS by preventing premature loading. Week-number progression is a guess; clearance-gated progression is evidence-based. For post-injury athletes, this is the highest-value premium feature.

---

#### T-RULE-39: Rippetoe Recovery-Based Athlete Classification

**What it does differently from free:** Free classifies progression engine by training_age alone (beginner→linear, intermediate→double progression, advanced→block periodization). Premium replaces training_age with **observed recovery rate**: novice (recovers within 24–72h → linear progression), intermediate (recovers weekly → weekly undulation), advanced (multi-week recovery → block periodization). An athlete can be chronologically "advanced" but recover like a novice after a layoff, or be a fast-recovering "intermediate" who should use linear progression despite longer training history.

**What data it requires:** Multiple sessions of recovery observation — subjective recovery_capacity flag alone is insufficient. Requires session-by-session readiness/performance tracking over 2–4 weeks to determine actual recovery curve.

**Why it can't be in free/core:** The free version uses a subjective self-report flag (good/average/poor) as an approximate input. Premium's recovery rate classification requires observed data across sessions. Without it, training_age is a reasonable proxy. With it, the progression engine adapts to the athlete's actual biology.

**Estimated premium value:** Catches mismatches where training_age-based classification over- or under-estimates the athlete's adaptive capacity. Prevents advanced-classified athletes from stalling on double progression when they actually need block periodization.

---

#### T-RULE-40: PHV-Adjusted Volume Ceiling

**What it does differently from free:** Free uses age_band and developmental_stage (childhood/adolescence/post-adolescence mapped from age) to set volume and complexity limits (T-RULE-22, T-RULE-34). Premium uses **actual PHV status** (pre/circa/post) to apply a precise volume ceiling multiplier: circa-PHV volume = 0.6× normal, with mandatory mobility emphasis. Pre-PHV and post-PHV are used for loading decisions beyond what age-based estimation can provide.

**What data it requires:** PHV assessment — typically the Mirwald equation (requires seated height, standing height, age) or clinical estimate. Requires a coach or clinician to take anthropometric measurements.

**Why it can't be in free/core:** Age bands are an approximation. A 14-year-old could be pre-PHV, circa-PHV, or post-PHV depending on maturation rate. Without the actual assessment, volume ceilings are conservative age-band estimates. Training a circa-PHV athlete at full volume because their age suggests they should tolerate it risks overuse injury.

**Estimated premium value:** Protects the circa-PHV athlete — the highest injury-risk period in youth sport — from overuse. Age banding is blurry (±2 years around PHV); actual PHV measurement is precise. For academy/youth programs, this is the edge that prevents losing developing athletes to injury.

---

#### T-RULE-43: Tendon/Ligament Healing Phase Loading

**What it does differently from free:** Free applies the previous_injury_multiplier (T-RULE-16) which modifies exercise selection for previously injured athletes but does not tissue-type or phase-specifically adjust loading. Premium tracks the healing timeline per tissue type: muscle (4–8wk healing), tendon (8–52wk remodelling), ligament (12–52wk), bone (6–12wk). Loading caps are applied by percentage of healing phase completed — e.g., during tendon remodelling (weeks 8–52), loading is capped at 30% of pre-injury at week 8, progressing to 80% by week 26, with full loading only after week 52.

**What data it requires:** Injury date, tissue type (clinical diagnosis), body part, severity grade. This is clinical data that requires a healthcare professional.

**Why it can't be in free/core:** Tissue type and healing phase require clinical diagnosis. Self-reported "I hurt my knee" is insufficient — is it the ACL, MCL, patellar tendon, or meniscus? Each has different healing timelines and loading constraints. Free cannot operationalise this safely.

**Estimated premium value:** For athletes with significant injury history, this prevents re-injury during the highest-risk period: return to full loading before tissue remodelling is complete. The difference between "returned too soon" and "returned ready."

---

#### T-RULE-44: Velocity-Based Progression

**What it does differently from free:** Free uses double progression (reps first, then load — T-RULE-03) and technique gating (T-RULE-10) for exercise progression. Premium replaces rep-count-based progression with **velocity zones**: mean velocity > 0.9 m/s = power zone (low fatigue, high neural demand), 0.75–0.9 m/s = strength zone, < 0.75 m/s = high fatigue zone. VBT deload triggers automatically when velocity drops below the threshold for two consecutive sessions (indicating accumulated fatigue rather than strength gain).

**What data it requires:** Per-rep mean velocity data from a linear encoder, Tendo unit, GymAware, or bar-speed tracking device. This is equipment-dependent and cannot be approximated.

**Why it can't be in free/core:** Requires hardware (VBT device) that the vast majority of athletes do not own. Without the data stream, double progression is the standard evidence-based alternative. VBT adds precision but is not essential for effective training.

**Estimated premium value:** VBT is the most precise real-time fatigue management tool available. It catches strength decrements from fatigue before the athlete or coach perceives them. For advanced athletes pushing near-maximal loads, this prevents overreaching sessions that stall progress. For teams with VBT equipment, it turns every rep into a data point.

---

#### T-RULE-45: Return-to-Play 6-Phase Protocol

**What it does differently from free:** Free has BP12 (RTS) with a flat week-number progression and T-WU-10 (RTP warmup tiers by week). Premium extends this into a **6-phase RTP protocol** with objective clearance gates at every phase: (1) rest/recovery → (2) mobility restoration → (3) strength normalisation (within 10% of contralateral) → (4) functional movement → (5) sport-specific drills → (6) full participation. Each phase requires specific objective testing data to clear the gate.

**What data it requires:** At minimum: ROM measurements (phase 2→3), bilateral strength symmetry (phase 3→4), FMS or functional movement scores (phase 4→5), sport-specific performance tests (phase 5→6). This is sequential, repeated assessment data.

**Why it can't be in free/core:** The 6-phase protocol requires objective testing at every gate. Without assessment data, the system defaults to time-based progression (BP12 week-number approach), which is clinically inferior but safe and credible.

**Estimated premium value:** For post-injury athletes, gates prevent the most common cause of re-injury: premature return to sport-specific work before strength and mobility are fully restored. Each gate caught early is a re-injury prevented.

---

#### T-RULE-46: Youth Foundation Maturation-Adjusted Blueprint

**What it does differently from free:** Free BP7 (Youth Foundation) uses developmental_stage mapped from age (T-RULE-22) with age-group training guidelines (T-RULE-34). Premium adds a **maturation_phase** field to BP7 that overrides age-based assumptions: pre-PHV focuses on coordination and fundamental movement at low volume; circa-PHV applies volume × 0.6 with mandatory mobility emphasis; post-PHV unlocks full strength programming. This is T-RULE-40's PHV ceiling applied specifically within the BP7 blueprint structure, with additional exercise selection and complexity constraints per maturation phase.

**What data it requires:** Same as T-RULE-40 — PHV assessment via Mirwald equation or clinical estimate.

**Why it can't be in free/core:** Without PHV assessment, BP7 uses age bands which are ±2 years inaccurate for maturation status. Applying circa-PHV constraints to an athlete who has already passed PHV unnecessarily limits their development. Applying post-PHY programming to an athlete in circa-PHV risks overuse injury.

**Estimated premium value:** For youth programmes (BP7 is the most-used blueprint for under-18 athletes), this is the difference between training that respects biological maturity and training that guesses. The circa-PHV multiplier alone (0.6×) is the single most important load management lever for reducing youth overuse injury.

---

## Section C — BORDERLINE ITEMS

### 1. Rippetoe Recovery Rate Classification (T-RULE-39)

**Free version:** Subjective self-report flag (recovery_capacity = good / average / poor). The progression engine uses this as a tiebreaker when training_age is ambiguous (e.g., an "intermediate" who self-reports "poor" recovery may be routed toward block periodization earlier). No longitudinal tracking required.

**Premium version:** Observed recovery rate from 2–4 weeks of session-by-session readiness or performance data. Algorithm classifies athlete as novice (24–72h recovery), intermediate (weekly recovery), or advanced (multi-week recovery). Overrides training_age-based classification.

**Recommendation:** Split as implemented. Free gets the subjective self-report flag for approximate routing. Premium gets the observed-data classification. The flag is low-burden; the classification is high-value.

---

### 2. Female Athlete ACL Modifier — Menstrual Cycle Phase (T-RULE-24)

**Free version:** ACL prevention exercises (Nordic curls, single-leg landing drills, hip abductor work) are added deterministically for all female athletes regardless of cycle phase. The exercise selection is identical across the cycle. This is still evidence-based prevention.

**Premium version:** Menstrual cycle phase tracking (follicular / ovulatory / luteal / menstrual) periodizes strength and power session timing. ACL prevention exercises are still always present, but high-intensity plyometrics and strength work are preferentially scheduled during the follicular phase when ACL injury risk is lower and strength gains are optimised. Luteal phase emphasises technique and lower-intensity work.

**Recommendation:** Split as implemented. Free gets the deterministic ACL prevention exercise addition — this is non-negotiable basic care. Premium gets the cycle-phase periodization overlay, which requires daily phase tracking and delivers a meaningful but secondary benefit.

---

### 3. Technique Gate (T-RULE-10) — Coach-Reported vs Sensor-Measured

**Free version:** technique_consistency is a coach-reported or self-reported rating (0.0–1.0) evaluated per session. The coach watches the athlete and estimates consistency. The T-RULE-10 mastery gate (threshold = 0.8) enforces regression when this drops below.

**Premium version:** technique_consistency is measured objectively via VBT velocity data (consistent velocity across reps = consistent technique), force plate data (symmetrical force production = symmetrical technique), or video analysis integration. No subjective rating needed.

**Recommendation:** Keep in Free with coach-reported rating. The gate function (regression when below threshold) is the same — only the measurement source differs. Adding sensor-based measurement to Premium would be natural if VBT (T-RULE-44) is implemented, but the gate itself is Core.

---

### 4. Previous Injury Risk Multiplier (T-RULE-16) — Time-Based vs Tissue-Specific

**Free version:** Applies a general previous_injury_multiplier to risk calculation. A previously injured athlete gets modified exercise selection for 6 months post-return, avoiding loaded end-range at the previously injured joint. No tissue-type differentiation.

**Premium version:** T-RULE-43 (tendon/ligament healing phase loading) replaces the generic 6-month window with tissue-specific healing timelines. The "modified exercise selection" becomes loading caps and phase-specific protocols.

**Recommendation:** T-RULE-16 is Core — a generic 6-month protection window is better than nothing and requires no clinical data. The upgrade path to tissue-specific loading (T-RULE-43) is Premium. Clear, clean boundary.

---

### 5. Connective Tissue Stress Score (T-RULE-15) — Aggregate vs Individualised

**Free version:** Uses generic eccentric_cost and impact_level from exercise metadata to calculate a weekly eccentric stress score. The cap is a population-level threshold. All athletes with similar programming get the same cap.

**Premium version:** Individualises the connective tissue cap based on injury history (tissue-specific resilience), FMS asymmetry data (unilateral loading bias), and ACWR (current fatigue state). The cap becomes dynamic: lower for previously injured tendons, higher for robust athletes.

**Recommendation:** Keep T-RULE-15 in Free. The population-level cap is still protective and evidence-based. Individualised adjustment would be a natural Premium extension but does not warrant its own Bucket B item currently.

---

## Section D — MIGRATION PATH

### What triggers the upgrade

A Free user upgrades to Premium when any of the following are true:

1. **They have assessment data to enter.** FMS scores, PHV measurements, VBT data, or injury timeline with tissue diagnosis. The system detects these additional fields and unlocks Premium features.

2. **They have 4+ weeks of consistent session logging.** ACWR becomes meaningful with a 4-week chronic baseline. Premium ACWR override activates automatically when the data supports it.

3. **A coach or clinician creates a Premium profile on behalf of an athlete.** The Premium tier is designed for coach-administered workflows — the coach enters screening data, the system generates assessment-adjusted programs.

4. **The athlete's specific situation requires Premium features.** Injury rehab (RTP phase progression), youth athlete with PHV assessment, or advanced athlete with VBT equipment.

There is no artificial paywall on inputs that are already in Free. The upgrade is **data-driven**: enter assessment data, get Premium output. If no assessment data exists, the system stays in Free mode.

### What new data collection is needed

When a Free user initiates Premium, the following data collection and input steps are needed:

| Data | Collection method | Who collects | Minimum frequency |
|---|---|---|---|
| FMS screen | Certified FMS assessment | Coach / clinician | Every 6–8 weeks or post-RTP |
| PHV / maturation | Mirwald equation (heights + age) or clinical estimate | Coach / clinician | Once per season for U18 |
| VBT velocity data | Linear encoder / Tendo / GymAware | Athlete / coach | Every working set |
| ACWR loading | Session RPE × duration logging | Athlete / coach | Every session |
| Injury timeline | Clinical diagnosis record | Clinician | At injury + return |
| Bilateral strength | Isometric or dynamic testing | Coach / clinician | Per mesocycle |
| Menstrual cycle phase | Daily tracking app or self-report | Athlete | Daily |
| Wellness scores | Daily readiness questionnaire | Athlete | Daily |

### What changes in program output

When Premium data is available, these changes occur in the generated program:

| Domain | Free output | Premium output |
|---|---|---|
| Blueprint selection | Based on goal + sport + level | Overridden by ACWR (deload route), FMS (corrective route), injury (RTP route) |
| Exercise selection | RM zone + energy system + family code | Gated by FMS asymmetry, bilateral strength ratios, technique consistency, healing phase caps |
| Progression engine | Linear (novice) / double (intermediate) / age-based | Recovery-rate-classified engine, VBT velocity zones, PHV-adjusted ceilings |
| Volume prescription | Based on blueprint defaults, age band, training_goal | Dynamic: PHV × 0.6 during circa-PHV, ACWR-capped, connective tissue score-adjusted |
| RTS / RTP | Week-number progression (BP12) with 3-tier warmup | 4-phase clearance-gated RTS (T-RULE-20) + 6-phase RTP protocol (T-RULE-45) |
| Youth loading | Age-band-based (T-RULE-22, T-RULE-34) | PHV-status-based volume ceiling + maturation-adjusted BP7 (T-RULE-46) |
| Female athlete | ACL prevention exercises always present | Cycle-phase periodized strength/power scheduling + ACL prevention |
| Deload trigger | Fixed schedule (Bompa step) + optional self-report | ACWR > 1.5 automatic route, VBT velocity-drop detection |
| Warmup template | Sport + session_type + environment driven | FMS-driven corrective warmup inclusions (if asymmetry detected) |
| Conditioning | Sport + level + environment driven | MAS-test-paced protocols, sprint-test-graded intervals |

The Free→Premium transition is not a replacement — it is a **precision overlay**. Every Free feature still runs underneath. Premium adds gates, overrides, and adjustments that the data justifies. If data entry stops, the system degrades gracefully back to Free defaults.

---

## Section E — WHAT FREE DELIBERATELY SACRIFICES

FORGE Free is honest about what it gives up. These are deliberate product decisions, not gaps:

1. **No injury branch specificity.** Free applies a generic previous_injury_multiplier (T-RULE-16) and modifies exercise selection for 6 months post-return. It does not tissue-type the injury, track healing phase, or apply loading caps per week-of-recovery. An athlete with a grade 1 hamstring strain and an athlete with an ACL reconstruction get the same "previously injured" treatment in Free. Premium (T-RULE-43, T-RULE-20, T-RULE-45) provides tissue-specific loading and phase-gated RTP.

2. **No test-driven periodization.** Free uses training_age, level, and subjective recovery_capacity to select progression engines. It does not use MAS, sprint, jump, or strength test results to set intensity zones, pace intervals, or grade plyometric selection. Premium uses test results to calibrate every dimension of program intensity.

3. **No screening-based exercise gating.** Free assumes movement competence. It applies technique_consistency gates (T-RULE-10) and bilateral strength ratios (T-RULE-11), but does not gate blueprint assignment on FMS scores. An athlete with an FMS score of 10 would be assigned the same blueprint as an athlete with a score of 18 in Free. Premium catches this at the assignment level (T-RULE-42).

4. **No ACWR-based load management.** Free uses Bompa step loading (T-RULE-07) for scheduled deloads and a 15% week-over-week cap (T-RULE-14) for spike prevention. These are population-level safe defaults. Premium replaces them with the athlete's actual chronic load baseline, dynamically adjusting the load ceiling as fitness changes (T-RULE-41).

5. **No maturation-adjusted youth loading beyond age bands.** Free uses developmental_stage mapped from age (T-RULE-22) and age-group guidelines (T-RULE-34). A circa-PHV 14-year-old gets the same volume ceiling as a pre-PHV 14-year-old. Premium applies the PHV volume multiplier (0.6× during circa-PHV) and adjusts BP7 exercise selection by maturation phase (T-RULE-40, T-RULE-46).

6. **No VBT-based progression.** Free uses double progression (reps-first, then load) for intermediates and linear progression for beginners. These are well-established evidence-based methods. Premium replaces them with velocity zones and automatic deload detection from VBT data (T-RULE-44).

7. **No individual corrective exercise blocks.** Free routes all athletes through standard blueprints. If an athlete needs corrective work (asymmetry, mobility deficit, motor control issue), Free cannot generate a dedicated corrective block. The athlete would either regress within an existing blueprint or manually adjust. Premium routes FMS-flagged athletes to corrective blueprints (T-RULE-42).

8. **No menstrual cycle phase periodization.** Free adds ACL prevention exercises for all female athletes — this is non-negotiable. It does not periodize strength/power session timing around the menstrual cycle. Premium (T-RULE-24 extension) schedules high-intensity work in the follicular phase and emphasises technique in the luteal phase.

9. **No objective recovery rate classification.** Free uses training_age and a subjective self-report flag. Premium classifies recovery rate from observed data across multiple sessions, enabling more precise progression engine selection (T-RULE-39).

10. **No coach override system.** Free generates programs from inputs alone. If a coach wants to manually override a session, the program must be edited externally. Premium accepts coach_override_notes that modify program generation at the rule level.

### What Free still does well

Despite these sacrifices, FORGE Free remains a credible training system. The items above represent **precision improvements, not fundamental capability gaps**. Free applies the following evidence-based principles without needing assessment data:

- Periodized macrocycles with Verkhoshansky block structure
- Bompa step loading with built-in deload weeks
- Phase-appropriate intensity (accumulation → intensification)
- Energy system specificity in conditioning selection
- Competition-tapered peaking
- Load spike prevention (15% week-over-week cap)
- Connective tissue stress monitoring (aggregate)
- Previous injury protection (non-tissue-specific)
- Novice linear and intermediate double progression
- Mastery-based technique gating (coach-reported)
- Bilateral-to-unilateral strength gating
- Stable-to-unstable surface progression
- Power-before-strength-before-accessory sequencing
- Age-group-appropriate volume and complexity limits
- 5-stage plyometric progression with volume caps
- RAMP phase-ordered warmups
- Sport-specific templates, roles, and positions
- ACL prevention for female athletes
- Deterministic exercise selection by RM zone and energy system

A coach using FORGE Free can confidently generate programs for any athlete who does not have access to movement screening, fitness testing, or wearable technology. When that data becomes available, Premium is ready to receive it and respond with the next level of precision.

---

*Document version: V1*  
*Classification: Core / Premium boundary definition*  
*Source: FORGE_BOOK_BACKLOG_TRIAGE_V1.md (94 triaged items: 68 Core, 12 Premium, 14 Reference)*
