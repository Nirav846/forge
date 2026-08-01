# AUDIT #5 — DOMAIN MODEL VALIDATION
# FORGE V2 Final Architecture Freeze Review

**Review Mode:** Domain Architect + Elite Sports Scientist + DDD Reviewer
**Date:** 2026-06-17
**Scope:** Bounded context completeness, aggregate design, entity lifecycles, sports science workflows, periodization, explainability, future scale
**Rule:** Do not re-argue accepted fixes (ACWR, CSP, composite objectives, competition calendar, pipeline config)

---

## SECTION A — Domain Scorecard

| Category | Score /10 | Reason |
|----------|-----------|--------|
| Athlete State | 8 | Readiness, recovery, fatigue, sleep, wellness covered. Missing: psychological readiness, menstrual cycle, illness. |
| Training Load | 9 | Daily/weekly/ACWR/trends covered. Missing: tissue-specific load (tendon, bone), mechanical load decomposition. |
| Injury Risk | 7 | Profile + multi-factor risk covered. Missing: injury registry (history, type, severity, recurrence), reinjury probability. |
| Assessment | 8 | Broad coverage. Missing: biological age, maturation, psychological assessments. |
| Demand | 8 | Performance demands + scoring + lifecycle. Missing: demand dependencies (DAG), synergistic/antagonistic demands. |
| Performance Model | 6 | Sport + role models defined conceptually but no versioning, no evidence-weighting, no model lifecycle. |
| Exposure Planning | 5 | Targets + dose-response claimed but no explicit exposure entity with frequency/volume/reps/sets per quality per phase. |
| Session Planning | 7 | Objectives + sequencing + competition constraints. Missing: session intent, coach annotation, session type definitions. |
| Exercise | 9 | Catalog + mappings + diversity. Comprehensive. |
| Progression | 6 | Rules + levels + demand-awareness. Missing: progression state machine, regression handling, stall detection. |
| Competition | 6 | Events + windows + red zones. Missing: season structure (pre/in/post/off), tournament format, travel schedule. |
| Adaptation | 5 | PreSessionGate + overrides. Missing: actual adaptation modeling (supercompensation, decay, dose-response curves). |

**Weighted Average: 6.8 / 10**

---

## SECTION B — Missing Bounded Contexts

---

### B1. PERIODIZATION CONTEXT — SEVERITY: CRITICAL

**Cannot absorb into:** Session Planning or Competition domains. Session planning handles individual sessions. Competition handles events. Periodization is the *organizing principle* that structures time between competitions into meaningful training blocks with specific adaptation goals, loading trends, and recovery phases.

**What's missing:**
- Training phases (preparatory, competitive, transition)
- Sub-phases (general preparation, specific preparation, pre-competition, competition, active rest)
- Block types (accumulation, intensification, realization, deload, taper, transition)
- Mesocycle entity with loading trajectory (linear, step, undulating, conjugate)
- Microcycle entity with session distribution (2:1 loading, 3:1, daily undulating)
- Macrocycle entity with annual/quadrennial plan

**Why this matters:**
Without a Periodization context, the system schedules sessions in a vacuum. It cannot answer:
- "Are we in a general preparation block or competition phase?" → different loading strategy
- "Should this week be an intensification week or a realization week?" → different volume/intensity targets
- "When does the deload occur relative to competition?" → critical for peaking
- "Is this athlete following a linear, undulating, or conjugate periodization model?" → different exercise selection logic

**Suggested aggregate root:** `PeriodizationPlan`

---

### B2. REHABILITATION & RETURN-TO-SPORT CONTEXT — SEVERITY: CRITICAL

**Cannot absorb into:** Injury Risk domain. Injury Risk is *preventive* — it identifies athletes at elevated risk and suggests intervention. Rehabilitation is *restorative* — it manages the entire pathway from injury occurrence through tissue healing, reconditioning, and return-to-play clearance. These are fundamentally different lifecycles with different entities, protocols, and gating criteria.

**What's missing:**
- Injury registry (injury type, date, mechanism, severity grade, tissue affected, imaging findings)
- Rehab protocol entity (phased: acute → sub-acute → strengthening → sport-specific → RTS)
- Rehab exercises distinct from performance exercises (controlled loading, tissue-specific dosing)
- Return-to-sport gate with objective criteria (strength symmetry, functional tests, sport-specific movements)
- Reinjury risk assessment (historically informed)
- Graduated return-to-play protocol (stage 1: individual training, stage 2: modified team training, stage 3: full team training, stage 4: match play with minutes restriction)

**Why this matters:**
Athletes get injured. Without a Rehab context, the system has no way to:
- Design progressive loading for a post-ACL athlete (different demands, different progression curve)
- Gate return-to-sport on objective criteria (LSI > 90%, hop test symmetry, etc.)
- Distinguish between "training load" and "rehab load" (different tissues, different adaptation rates)
- Manage the transition from rehab → full training without re-injury

**Suggested aggregate root:** `InjuryRecord` and `RehabProtocol`

---

### B3. LONG-TERM ATHLETE DEVELOPMENT (LTAD) CONTEXT — SEVERITY: HIGH

**Cannot absorb into:** Athlete State or Progression domains. LTAD is a distinct framework with its own stages, age windows, and developmental priorities. It governs *what* to develop and *when* based on biological maturation, not just training age.

**What's missing:**
- LTAD stage entity (FUNDAMENTALS, LEARNING-TO-TRAIN, TRAINING-TO-TRAIN, TRAINING-TO-COMPETE, TRAINING-TO-WIN, ACTIVE-FOR-LIFE)
- Maturation assessment (biological age, PHV — peak height velocity, maturity offset)
- Chronological age windows per stage
- Stage-specific training priorities (e.g., TRAINING-TO-TRAIN: aerobic base + strength, TRAINING-TO-COMPETE: sport-specific + tactical)
- Sensitive period windows (windows of trainability for speed, strength, stamina, skill, suppleness)
- Stage transition gates (criteria for advancing to next stage)

**Why this matters:**
Without LTAD, the system treats a 14-year-old and a 24-year-old identically, differing only on `training_age` and `development_level`. This is insufficient because:
- A 14-year-old in PHV has reduced coordination and increased injury risk — training must be modified
- Sensitive periods exist where certain adaptations are optimized (e.g., speed before PHV, strength 12-18 months after PHV)
- Early specialization vs. sampling debate — the system needs to support both approaches explicitly
- LTAD governs training-to-competition ratios differently across stages

**Suggested aggregate root:** `LTADProfile`

---

### B4. COACH INTELLIGENCE & WORKFLOW CONTEXT — SEVERITY: HIGH

**Cannot absorb into:** Adaptation domain. Adaptation handles overrides at the session level. Coach Intelligence is about capturing coach *intent*, *decision rationale*, and *pattern learning* over time. It is a meta-domain that observes and learns from coach behavior rather than making planning decisions.

**What's missing:**
- Coach intent entity (what is the coach trying to achieve with this program block?)
- Coach annotation entity (free-text + structured rationale for overrides)
- Coach behavior pattern entity (repeated modifications, preferred exercises, intensity biases)
- Coach confidence signal (how often has this coach's programming been effective?)
- Coach-athlete relationship entity (different coaches may have different effectiveness with the same athlete)
- Coaching workflow states (review → modify → approve → observe → adapt)

**Why this matters:**
Without Coach Intelligence, the system:
- Stores coach overrides but never learns from them
- Cannot distinguish between "coach replaced exercise A with B because B is better" vs. "coach replaced A with B because A was unavailable"
- Has no feedback loop to improve its recommendations based on coach expertise
- Cannot build trust — the system doesn't demonstrate learning from coach corrections

**Suggested aggregate root:** `CoachProfile` and `CoachDecision`

---

### B5. TEAM & SQUAD MANAGEMENT CONTEXT — SEVERITY: MEDIUM

**Cannot absorb into:** Athlete domain. Team sports have training sessions that are delivered to groups, not just individuals. Individual programming must coexist with shared team sessions.

**What's missing:**
- Team/squad aggregate (collection of athletes training together)
- Team session template (shared training content + individual modifications)
- Squad rotation policy (managing load across multiple competitions with squad depth)
- Position group entity (forwards vs. backs, offensive vs. defensive linemen)
- Team calendar (shared events, travel, training camps)
- Group dynamics (first-team vs. development squad, new signings, captaincy)

**Why this matters:**
Without Team management:
- The system generates ideal individual programs that cannot be delivered in a team setting
- A coach gets 30 individual programs but no "team training plan" — impossible to run a session
- Squad rotation and load management across congested fixture periods have no domain representation
- Team culture, social dynamics, and leadership — not directly relevant to FORGE but group training structure is

**Suggested aggregate root:** `Squad` and `TeamSession`

---

### B6. GOAL & TARGET SETTING CONTEXT — SEVERITY: MEDIUM

**Cannot absorb into:** Performance Model domain. Performance models describe current requirements. Goals describe *desired future state* with timeframes, milestones, and commitment levels.

**What's missing:**
- Goal entity (SMART: specific, measurable, achievable, relevant, time-bound)
- Goal hierarchy (season goal → mesocycle goal → weekly goal → session goal)
- Goal type (performance outcome, process goal, learning goal, rehabilitation goal)
- Goal progress tracking (on-track, behind, achieved, abandoned, superseded)
- Goal-commitment signal (how committed is the athlete to this goal?)
- Goal-achievement predictors (historical probability of achieving similar goals)

**Why this matters:**
The system identifies deficits and prescribes training, but it doesn't know *what the athlete is trying to achieve*. This leads to:
- Mismatch between system recommendations and athlete motivation
- No way to celebrate goal achievement (positive reinforcement loop)
- Inability to distinguish between "athlete wants to improve CMJ by 10%" vs. "athlete wants to maintain CMJ during competition season" — different strategies
- Cannot personalize goal difficulty — some athletes thrive on stretch goals, others need incremental wins

**Suggested aggregate root:** `AthleteGoal`

---

### B7. TISSUE LOAD & MECHANICAL LOAD CONTEXT — SEVERITY: MEDIUM

**Cannot absorb into:** Training Load domain. Training Load tracks session-level RPE × duration. Tissue Load tracks mechanical stress at the tissue level (tendon, bone, muscle, ligament) — a fundamentally different concept with different measurement, thresholds, and adaptation rates.

**What's missing:**
- Tissue type entity (tendon, bone, muscle, ligament, cartilage, nerve)
- Tissue-specific load metrics (tendon strain rate, bone stress, muscle damage markers)
- Tissue adaptation rate (tendons adapt slower than muscle — crucial for programming)
- Chronic tissue load (cumulative stress over weeks/months for connective tissues)
- Tissue load thresholds (bone stress reaction risk, tendinopathy risk)
- Surface/ground interaction (training surface affects tissue load)

**Why this matters:**
Without tissue load:
- The system cannot distinguish between "this athlete is fatigued" (muscle recovery in 24-48h) and "this athlete has tendinopathy risk" (tendon recovery in 72-96h+)
- Bone stress injuries (stress fractures) are a leading cause of time loss in track/field and basketball — invisible to RPE-based load
- Tendon adaptation requires different programming (isometric → eccentric → concentric → ballistic)
- Graduated return-to-run protocols after bone stress injury cannot be modeled

**Suggested aggregate root:** `TissueLoadProfile`

---

## SECTION C — Missing Aggregates

| Rank | Aggregate | Context | Reason | Severity |
|------|-----------|---------|--------|----------|
| 1 | `PeriodizationPlan` | Periodization | No organizing structure for training over time. Every session floats without block context. | CRITICAL |
| 2 | `InjuryRecord` | Rehab/RTS | No persistent record of injury history, type, severity, mechanism. Without this, reinjury prediction impossible. | CRITICAL |
| 3 | `RehabProtocol` | Rehab/RTS | No phased rehabilitation plan with tissue-specific loading, progression criteria, and return-to-sport gates. | CRITICAL |
| 4 | `LTADProfile` | LTAD | No management of biological maturation, PHV windows, or stage-appropriate training priorities. | HIGH |
| 5 | `Mesocycle` | Periodization | No 3-8 week training block with coherent adaptation goal, loading trend, and progression arc. | HIGH |
| 6 | `CoachIntent` | Coach Intelligence | No record of what the coach wanted to achieve — only what was prescribed. | HIGH |
| 7 | `CoachBehaviorPattern` | Coach Intelligence | No persistent learning from coach override patterns. | HIGH |
| 8 | `Squad` | Team Management | No aggregation of athletes into training groups with shared sessions. | MEDIUM |
| 9 | `AthleteGoal` | Goal Setting | No target-state representation for athlete development. System only knows deficits, not aspirations. | MEDIUM |
| 10 | `TissueLoadProfile` | Tissue Load | No tissue-specific mechanical load tracking. Connective tissue health invisible to current model. | MEDIUM |
| 11 | `Macrocycle` | Periodization | No annual or quadrennial plan structure. | MEDIUM |
| 12 | `Microcycle` | Periodization | No explicit week structure with loading pattern (2:1, 3:1, daily undulating). Currently implicit in session sequencing. | LOW |
| 13 | `ReturnToSportGate` | Rehab/RTS | No gating mechanism with objective criteria for return-to-play decisions. | MEDIUM |
| 14 | `MonitoringAlert` | Monitoring | No domain representation for alert thresholds, escalation, or intervention triggers. | LOW |
| 15 | `CoachAthleteRelationship` | Coach Intelligence | No model of differential coach effectiveness per athlete. | LOW |

---

## SECTION D — Lifecycle Gaps

### D1. Missing Entity Lifecycles

| Entity | Lifecycle | Missing? | Impact |
|--------|-----------|----------|--------|
| Program | Draft → Active → Modified → Completed → Archived | PARTIAL — no "Modified" state, no "Archived" state | Cannot track how programs evolve over time |
| Session | Planned → Ready → In Progress → Completed → Reviewed → Missed | PARTIAL — no "Reviewed" state, no "Missed" state | No feedback on session completion quality |
| Season | Planning → Preparation → Pre-Season → In-Season → Post-Season → Review → Transition | FULLY MISSING | No annual plan context for periodization |
| Mesocycle | Planned → Active → Completed → Reviewed | FULLY MISSING | No block-level progress tracking |
| Injury | Occurred → Assessed → Acute → Sub-Acute → Strengthening → Sport-Specific → RTS Gate → Cleared → Monitored | FULLY MISSING | No structured rehab pathway |
| Goal | Draft → Set → In Progress → On Track → Behind → Achieved → Missed → Superseded → Archived | FULLY MISSING | No goal lifecycle management |
| Coach Decision | Made → Applied → Observed → Evaluated → Learned | FULLY MISSING | No learning loop closure |
| Assessment | Scheduled → Conducted → Processing → Validated → Results Published → Compared → Expired | PARTIAL — no "Validated," "Expired," or "Compared" states | Cannot compare assessments across time reliably |
| Competition Event | Announced → Planning → Confirmed → Pre-Competition → Competition → Post-Competition → Reviewed | PARTIAL — no "Pre-competition" or "Post-competition" states | No taper or recovery planning window |
| Demand Priority | Proposed → Reviewed → Approved → Active → Deprecated | FULLY MISSING | No governance on demand priority changes |
| Exercise Mapping | Draft → Validated → Approved → Active → Deprecated → Removed | FULLY MISSING | No governance on exercise-demand mappings |

### D2. Lifecycle Invariants

Missing invariants that should be enforced:

| Invariant | Context | Why |
|-----------|---------|-----|
| A program cannot be Active if the athlete has an Active RehabProtocol with RTS stage "not cleared" | Rehab + Programming | Prevent concurrent conflicting prescriptions |
| A Session cannot be Planned during a competition red zone window without coach override | Competition + Session | Prevent missed competition peaks |
| An athlete cannot advance LTAD stage without passing stage-specific gate criteria | LTAD + Assessment | Ensure readiness for next developmental level |
| A Mesocycle cannot be Closed if any constituent Goal is still In Progress without rationale | Periodization + Goal | Prevent abandoning athlete goals mid-block |
| A RehabProtocol cannot advance from Sub-Acute to Strengthening without passing objective pain/function criteria | Rehab | Prevent re-injury from premature loading |
| An AthleteGoal cannot be Archived if it was Achieved — must transition through Celebrated state | Goal | Preserve positive reinforcement loop |

---

## SECTION E — Unsupported Sports Science Workflows

| Workflow | Supported? | Gap | Severity |
|----------|-----------|-----|----------|
| Youth Development (U12-U16) | NO | No LTAD, no biological age, no PHV windows, no sensitive periods. Systems designed for youth *must* model maturation. | CRITICAL |
| Return-to-Play after ACL reconstruction | NO | No rehab protocol, no RTS gates, no graduated loading protocol. ACL-R has specific phases (pre-op, 0-6wk, 6-12wk, 3-6mo, 6-9mo, 9mo+) each with different constraints. | CRITICAL |
| Tournament sports (3 matches in 7 days) | NO | No tournament-specific periodization, no squad rotation modeling, no match-congestion load management. | HIGH |
| Long-Term Athlete Development (LTAD) | NO | Complete LTAD framework missing. This is a foundational requirement for any youth sport platform. | HIGH |
| Combat sports with weight cutting | NO | No weight category management, no weigh-in periodization, no post-weigh-in rehydration/recovery planning. | HIGH |
| Olympic quadrennial cycle | NO | No 4-year planning horizon, no peaking for single-event competitions. | HIGH |
| Chronic injury management (tendinopathy) | NO | No tissue-specific load modeling, no tendon adaptation programming (isometrics → eccentrics → energy storage). | MEDIUM |
| Dual-sport athletes | NO | No multi-sport load context, no cross-sport transfer effects, no competing periodization calendars. | MEDIUM |
| Off-season return-to-training | NO | No detraining modeling, no re-acclimation protocol, no off-season transition from unstructured → structured training. | MEDIUM |
| Post-partum return-to-sport | NO | No post-partum physiology modeling, no pelvic floor considerations, no graduated return-to-impact protocol. | MEDIUM |
| Paralympic / adaptive sport | NO | No impairment classification modeling, no adapted exercise libraries, no equipment modification ontology. | MEDIUM |
| Altitude training camps | NO | No environmental stress integration, no altitude-specific loading, no post-camp acclimatization decay. | LOW |

---

## SECTION F — Architecture Freeze Recommendation

**Recommendation: APPROVE WITH MAJOR CHANGES**

### Rationale

The current domain model is **structurally sound for individual adult athlete programming** in single-sport, competition-phase contexts. The foundations (Athlete State, Training Load, Injury Risk, Assessment, Demand, Exercise) are well-defined with clear boundaries.

**However, the model has 4 critical gaps that prevent it from being a complete athlete development platform:**

1. **No Periodization context** — the system organizes sessions but not training blocks. Without periodization, the system is a session planner, not a program designer. This is the single biggest domain gap.
2. **No Rehabilitation / Return-to-Sport context** — athletes get injured. A performance platform must manage the full injury-to-return lifecycle. The current model stops at risk prediction.
3. **No LTAD context** — youth athletes have fundamentally different developmental needs governed by biological maturation, not training age. Without LTAD, the system cannot safely or effectively program for athletes under 18.
4. **No Coach Intelligence context** — the system generates recommendations but cannot learn from the expert (the coach). Without a learning loop, the system plateaus at its initial rule quality.

### Verdict

- **Freeze the current 12 domains** for Phase 1 implementation
- **Require 4 additional domains** (Periodization, Rehab/RTS, LTAD, Coach Intelligence) before declaring the domain model complete
- **Allow Phase 2 implementation** of the 4 additional domains as extensions to the frozen core

---

## SECTION G — Required Changes Before Architecture Freeze

### Must-Have (Freeze Blockers)

| # | Change | Domain | Rationale | Effort |
|---|--------|--------|-----------|--------|
| 1 | **Add PeriodizationPlan aggregate** with Mesocycle and Microcycle entities | NEW: Periodization | Without block-level planning, the system cannot structure training toward competition peaks. Every session lacks temporal context. | 3-4 weeks |
| 2 | **Add InjuryRecord aggregate** with injury history, type, severity, and tissue classification | NEW: Rehab/RTS | Without injury history, reinjury prediction is impossible and the system cannot distinguish primary vs. secondary prevention. | 2-3 weeks |
| 3 | **Add RehabProtocol aggregate** with phased progression (acute → sub-acute → strengthening → sport-specific → RTS) and stage-gate criteria | NEW: Rehab/RTS | Without structured rehab, the system generates performance programs that are dangerous for post-injury athletes. | 3-4 weeks |
| 4 | **Add LTADProfile aggregate** with biological age, PHV status, sensitive period windows, and stage-appropriate training constraints | NEW: LTAD | Without LTAD, youth athletes receive adult-appropriate programming with modified volume — fundamentally unsafe and unscientific. | 3-4 weeks |

### Should-Have (Pre-Production Blockers)

| # | Change | Domain | Rationale | Effort |
|---|--------|--------|-----------|--------|
| 5 | **Add CoachIntent entity** with structured intent capture (what, why, expected outcome) for every coach override | NEW: Coach Intelligence | Without intent capture, the system stores *what* the coach did but not *why*. Learning is impossible. | 1-2 weeks |
| 6 | **Add AthleteGoal aggregate** with goal hierarchy (season → mesocycle → weekly → session) and progress tracking | NEW: Goal Setting | Without goals, the system only manages deficits. Athlete development is driven by aspiration, not just gap analysis. | 2-3 weeks |
| 7 | **Add Season lifecycle states** (Planning → Preparation → Competition → Transition → Review) to Competition domain | Competition | Without season lifecycle, competition events exist in isolation. Pre-season preparation and off-season transition have no domain representation. | 1-2 weeks |
| 8 | **Add Program lifecycle states** (Draft → Active → Modified → Completed → Archived) to Session Planning domain | Session Planning | Without program lifecycle, there is no audit trail of how programs evolve through coach modification. | 1 week |

### Could-Have (Post-Production Enhancement)

| # | Change | Domain | Rationale | Effort |
|---|--------|--------|-----------|--------|
| 9 | **Add Squad aggregate** for team sports with shared team sessions + individual modifications | NEW: Team Management | Without squad modeling, team sport coaches receive 30 individual programs but no coherent team training plan. | 2-3 weeks |
| 10 | **Add TissueLoadProfile aggregate** for connective tissue stress monitoring | NEW: Tissue Load | Without tissue load, bone stress injuries and tendinopathies are invisible to the training load model. | 2-3 weeks |

---

## SUMMARY

**Current domain completeness: ~65%**

The 12 existing domains cover individual adult athlete performance programming well. The 4 critical missing domains (Periodization, Rehab/RTS, LTAD, Coach Intelligence) address the remaining 35%.

**Domain model can be frozen for implementation with the condition that:**

1. The 4 must-have aggregates are designed before coding begins (allowing the core 12 domains to proceed)
2. The 4 should-have aggregates are designed before production launch
3. The 2 could-have aggregates are designed within 12 months of production launch

**The architecture is conceptually sound.** The missing domains are not fundamental design flaws — they are scope gaps. The existing bounded contexts have clean boundaries and can coexist with the new contexts without refactoring.
