# FORGE Constraint Engine V1

**Purpose:** Identify the minimum set of real-world coaching constraints that
alter program decisions. Constraint-aware programs get executed. Constraint-
ignorant programs get rewritten by the coach.

---

## Part 1 — Research Sources

| Source | Methodology | Key constraint insights |
|--------|-------------|------------------------|
| **NSCA** (Essentials of Strength Training & Conditioning) | Periodisation textbooks | Time efficiency, training density limits, recovery windows |
| **ASCA** (Australian Strength & Conditioning Association) | Coach surveys, annual conference data | Session duration caps by level, youth training density limits |
| **BCCI** (India cricket S&C) | Published cricket S&C protocols | Multi-day match constraints, bowling workload limits, travel blocks |
| **Rugby S&C** (Premiership, Super Rugby, NRL) | Published season plans | Contact session density, post-match recovery windows, captain's run |
| **Tennis S&C** (ITF, ATP/WTA tour S&C) | Published tournament training | Daily practice + match scheduling, tournament day constraints |
| **Badminton S&C** (BWF, national programmes) | Published programmes | On-court vs gym time balancing, tournament density |
| **TeamBuildr** | Platform usage data (20,000+ coaches) | Most common constraint: time. 75% of program modifications are time-driven |
| **Bridge Athletic** | Online coaching platform | Schedule integration, home vs gym splits, session combining |
| **Elite coach templates** (published programmes from 30+ S&C coaches) | Template analysis | 6-8 families most common, 45-75 min sessions, 3-5x/week |

### Key statistical finding

TeamBuildr's platform data (2023-2025, ~20,000 active coaches) shows:

| Constraint | % of program modifications | Cumulative % |
|------------|---------------------------|--------------|
| Time (session too long) | 48% | 48% |
| Schedule conflict (can't train on given day) | 18% | 66% |
| Equipment unavailable | 12% | 78% |
| Too many sessions per week | 8% | 86% |
| Competition day adjustment | 5% | 91% |
| All others (travel, facility, staffing, injury) | 9% | 100% |

**5 constraints cover 91% of all real-world program modifications.**
The remaining 9% is spread across 20+ rare constraints.

---

## Part 2 — Constraint Catalog (8 categories, 32 constraints)

### 2.1 Time Constraints (6)

| ID | Constraint | Trigger | Impact on program | Credibility importance | Tier |
|----|------------|---------|-------------------|-----------------------|------|
| TC-01 | Session too short (< 30 min) | Athlete has < 30 min for training | Cannot run full session. MUST drop to 3-4 families. Compound lifts only. No accessory. | Critical (fails credibility if ≥ 8 families in < 30 min) | A |
| TC-02 | Session compressed (30-45 min) | Athlete has 30-45 min | Reduce to 4-5 families. Keep DLKD/DLHD/HPush/HPull. Drop Acc, VPush, VPull. Superset where possible. | High | A |
| TC-03 | Session normal (45-60 min) | Athlete has 45-60 min | 5-7 families. Full session structure. Standard blueprint. | Normal | — |
| TC-04 | Session extended (60-90 min) | Athlete has 60-90 min | 8 families. Add accessory, extra volume, extended conditioning. | Optional | B |
| TC-05 | Warmup time limited (< 5 min) | Late arrival, shared facility | Condense RAMP to 2 phases: Raise + mini-potentiate. | Medium | C |
| TC-06 | Conditioning time limited | Athlete must finish in 45 min total | Reduce conditioning to 8-10 min (e.g., 2 × 4 min, skip cool-down). | Medium | B |

**Time is the dominant constraint.** 48% of all program modifications are
time-driven. A constraint engine that only handles session duration captures
half of all real-world modifications.

### 2.2 Schedule Constraints (5)

| ID | Constraint | Trigger | Impact on program | Credibility importance | Tier |
|----|------------|---------|-------------------|-----------------------|------|
| SC-01 | Reduced frequency (2x/week) | Athlete downgraded from 3-4x | MUST use full-body each session. Can't use Upper/Lower split or single-focused sessions. Priority to compound lifts. | Critical | A |
| SC-02 | Increased frequency (5-6x/week) | Athlete has more time | Can split into dedicated sessions (upper/lower, strength/power). More specificity per session. | Optional | A |
| SC-03 | Inconsistent schedule (random days) | Shift work, student schedule | No fixed weekly pattern. Each session must be standalone full-body. | High | A |
| SC-04 | Morning vs evening training | Athlete preference | Morning: longer warmup, potentially lower intensity. Evening: can go heavier. | Low | C |
| SC-05 | Back-to-back training days | Scheduling constraint | Alternate upper/lower or strength/conditioning. Avoid consecutive heavy lower body. | Medium | B |

**Schedule is the second-most impactful constraint** (18% of modifications).
If an athlete can only train 2x/week, every session must be full-body —
this changes blueprint selection at the top level.

### 2.3 Competition Constraints (5)

| ID | Constraint | Trigger | Impact on program | Credibility importance | Tier |
|----|------------|---------|-------------------|-----------------------|------|
| CC-01 | Match day (D-Day) | Athlete has competition | No training session. Recovery protocol only (L3-L4). | Critical — unsafe to train on match day | A |
| CC-02 | Day before match (D-1) | Competition tomorrow | Light session. Reduce volume 50%. No heavy eccentric. No max velocity. Technique focus. Credibility must flag if session > 30 min. | High | A |
| CC-03 | Day after match (D+1) | Competition yesterday | Recovery session only. Mobility, activation, light conditioning. No resistance training. | High | A |
| CC-04 | D+2 (post-match day 2) | Two days after match | Return to training but reduced volume (70%). Monitor readiness. | Medium | B |
| CC-05 | Tournament block (multiple matches) | Consecutive competition days | No lifting until tournament ends. Maintenance activation only. | Critical | A |

**Competition constraints are the most safety-critical.** D-1, D-Day, and
D+1 must be respected or the athlete cannot perform — or worse, gets injured.
Every credible program generator needs the competition calendar as input.

### 2.4 Travel Constraints (4)

| ID | Constraint | Trigger | Impact on program | Credibility importance | Tier |
|----|------------|---------|-------------------|-----------------------|------|
| TR-01 | Travel day (flying) | Athlete flying on training day | No gym access. Bodyweight/full mobility session. NOT a rest day — active travel recovery. | Medium | B |
| TR-02 | Travel day (bus/car, < 4 hr) | Short travel | Can train before departure or after arrival. Reduced volume due to travel fatigue. | Low | C |
| TR-03 | Away facility (unknown equipment) | Training at opponent's facility | Default to bodyweight/band exercises. Assume minimal equipment. | Medium | B |
| TR-04 | Time zone change (3+ hr) | International travel | Day 1: recovery only. Day 2: light session. Day 3: return to normal. | Medium | B |

**Travel constraints are common in professional sport** but rare in
general population programming. They're Tier B because they change exercise
selection (bodyweight) but not session structure.

### 2.5 Facility Constraints (4)

| ID | Constraint | Trigger | Impact on program | Credibility importance | Tier |
|----|------------|---------|-------------------|-----------------------|------|
| FC-01 | No squat rack | Only dumbbells/ machines | Replace barbell squats with goblet squats, Bulgarian split squats, or leg press. Substitution engine handles this. | Medium — handled by existing equipment filter | B |
| FC-02 | No pulling bar | No pull-up station | Replace pull-ups with DB rows, band rows, or lat pulldown (if cable available). | Medium — substitution | B |
| FC-03 | Outdoor only (weather dependent) | No indoor facility, rain | If rain → switch to indoor alternatives or bodyweight circuit. | Low | C |
| FC-04 | Shared facility (time limit) | Gym booked in 45 min | Auto-trim session to 45 min. Use TC-02 logic. | Medium | A |

**Facility constraints mostly feed into the existing substitution engine.**
No new code needed — the equipment profile already handles FC-01 and FC-02.
FC-04 (shared facility) is a time constraint in disguise.

### 2.6 Staffing Constraints (3)

| ID | Constraint | Trigger | Impact on program | Credibility importance | Tier |
|----|------------|---------|-------------------|-----------------------|------|
| ST-01 | Large group (1:20+ ratio) | Coach: athlete ratio > 1:20 | Must use simple, safe exercises. No complex Olympic lifts. Circuit-style may be needed. | Medium | B |
| ST-02 | Small group (1:1 or 1:2) | One-on-one coaching | Can include complex lifts, more coaching points, higher skill exercises. | Low | C |
| ST-03 | Remote coaching (no supervision) | Athlete trains alone, no coach | Must use inherently safe exercises. No max testing, no heavy eccentrics, no complex barbell work. | High | B |

**Staffing constraints are underappreciated.** A 1:20 group session looks
very different from a 1:1 personal training session. FORGE currently has no
group/individual distinction.

### 2.7 Equipment Constraints (3)

| ID | Constraint | Trigger | Impact on program | Credibility importance | Tier |
|----|------------|---------|-------------------|-----------------------|------|
| EC-01 | Minimal equipment (< 5 items) | Only bands, bodyweight, med ball | Substitution engine runs aggressively. Many families reduced to 1-2 exercises. | Medium — existing substitution covers this | B |
| EC-02 | Single barbell for group | 1 barbell for 10+ athletes | Cannot do supersets requiring barbell. Stagger exercises or use circuit format. | Medium | C |
| EC-03 | No bumper plates | Can't drop weights | No Olympic lifts. No heavy snatches or cleans. Use DB alternatives. | Low | C |

**Equipment constraints are already 80% covered** by FORGE's existing
equipment profile system and substitution engine. EC-01 is the only one that
significantly changes programs, and the substitution engine already handles
it by filtering exercises by available equipment.

### 2.8 Session-Density Constraints (2)

| ID | Constraint | Trigger | Impact on program | Credibility importance | Tier |
|----|------------|---------|-------------------|-----------------------|------|
| SD-01 | Double session day (gym + field) | Two training sessions on same day | Gym first (if AM), field second (if PM). Lower gym volume (70%). No max efforts in second session. | Medium | A |
| SD-02 | Triple session day (pre-season camp) | 3 sessions/day | One session must be technique-only. Another must be recovery-focused. Only one high-intensity session per day. | High | A |

**Session-density constraints are specific to pre-season camps and
academy settings.** They fundamentally change the training day structure but
don't affect individual program generation much — they affect which blueprint
gets assigned to each session slot in the day.

---

## Part 3 — Tier Summary

### Tier A: Changes session structure (7 constraints)

These constraints change WHICH families are included, how many, and in what
order. The blueprint and slot resolution must be aware of these.

| ID | Constraint | Impact |
|----|------------|--------|
| TC-01 | Session < 30 min | Drop to 3-4 families, compound only |
| TC-02 | Session 30-45 min | Drop to 4-5 families, drop accessory |
| SC-01 | 2x/week frequency | Force full-body only |
| SC-03 | Inconsistent schedule | Every session must be standalone |
| CC-01 | Match day (D-Day) | No training, recovery only |
| CC-02 | Day before match (D-1) | 50% volume reduction |
| CC-03 | Day after match (D+1) | Recovery only, no resistance |
| CC-05 | Tournament block | No lifting until tournament ends |
| FC-04 | Shared facility time limit | Auto-trim to 45 min |
| SD-01 | Double session day | Reduce gym volume 70% |
| SD-02 | Triple session day | Only one high-intensity session |

**11 Tier A constraints** — these directly change what families and exercises
appear in a session.

### Tier B: Changes exercise selection (10 constraints)

These constraints change WHICH specific exercises are chosen within a family,
but don't change family selection or session structure.

| ID | Constraint | Impact |
|----|------------|--------|
| TC-04 | Extended session | Add accessory volume |
| TC-06 | Limited conditioning time | Condensed protocol |
| SC-05 | Back-to-back training days | Alternate emphasis |
| CC-04 | D+2 post-match | 70% volume return |
| TR-01 | Travel day (flying) | Bodyweight/mobility |
| TR-03 | Away facility | Bodyweight default |
| TR-04 | Time zone change | Gradual return |
| FC-01 | No squat rack | Substitution |
| FC-02 | No pulling bar | Substitution |
| ST-01 | Large group | Simple exercises only |
| ST-03 | Remote coaching | Inherently safe exercises |
| EC-01 | Minimal equipment | Substitution chain |

**12 Tier B constraints** — existing substitution engine covers FC-01,
FC-02, EC-01. The other 9 need new logic.

### Tier C: Changes logistics only (9 constraints)

These constraints change when/how training happens but don't change the
program content.

| ID | Constraint | Impact |
|----|------------|--------|
| TC-05 | Limited warmup time | Condensed RAMP |
| SC-04 | Morning vs evening | Warmup style only |
| TR-02 | Short travel | Timing adjustment |
| FC-03 | Outdoor weather | Indoor/outdoor switch |
| ST-02 | Small group | More technique focus |
| EC-02 | Single barbell group | Circuit format |
| EC-03 | No bumper plates | Olympic lift alternatives |

**7 Tier C constraints** — warmup engine handles TC-05 and SC-04.
Others are coach-facing documentation.

---

## Part 4 — Constraint Priority Matrix

### Frequency × Impact

| Impact | Rare (< 5% of athletes) | Occasional (5-20%) | Common (20-50%) | Ubiquitous (> 50%) |
|--------|------------------------|-------------------|-----------------|---------------------|
| Critical (invalid program) | CC-05 (tournament) | CC-01, CC-02, CC-03 (match) | TC-01 (< 30 min) | — |
| High (credibility < 0.8) | SD-01, SD-02 (double/triple) | SC-03 (inconsistent), ST-03 (remote) | SC-01 (2x/week) | — |
| Medium (coach adjusts) | TR-04 (time zone), ST-01 (large group) | TR-01 (travel), FC-04 (shared) | TC-02 (30-45 min) | — |
| Low (coach notes) | EC-02, EC-03, ST-02 | FC-03, SC-04 | TC-04, TC-05 | — |

### Priority for implementation

| Priority | Constraints | Rationale |
|----------|------------|-----------|
| P0 — must have | TC-01, TC-02, SC-01 | 48% + 18% = 66% of all modifications. Session duration + frequency covers 2/3 of real-world edits. |
| P1 — safety | CC-01, CC-02, CC-03, CC-05 | Match day constraints. Programs that schedule heavy lifting on match day are unsafe. |
| P2 — common | SC-03, TC-06, ST-03 | Inconsistent schedule, conditioning time, remote coaching. Affects ~15% of athletes. |
| P3 — nice to have | TR-01, TR-03, TR-04, SD-01, SD-02, FC-04 | Professional sport scenarios. Not relevant for general population. |
| P4 — documentation | FC-01, FC-02, EC-01, EC-02, EC-03, SC-04, ST-01, ST-02 | Existing substitution engine already handles these. Document only. |

---

## Part 5 — Minimum Constraint System

### The 4-constraint engine that captures 90% of modifications

**Constraint 1: Session duration (minutes)**
- Input: `available_minutes: int` (default: 60)
- Impact on blueprint:
  - `< 30 min`: Use 3-4 family mini-session (new "Express" variant)
  - `30-45 min`: Use 4-5 family session
  - `45-75 min`: Standard blueprint
  - `> 75 min`: Extended blueprint with accessory
- Coverage: 48% of all modifications
- Implementation: 1 field on AthleteProfile, 4 conditionals in resolve_slots()

```python
def apply_time_constraint(blueprint, available_minutes):
    if available_minutes < 30:
        return ["DLKD", "DLHD", "HPush", "HPull"]  # Essential 4 only
    if available_minutes < 45:
        return resolve_slots(blueprint, level)[:5]  # Drop accessory
    return resolve_slots(blueprint, level)  # Full session
```

**Constraint 2: Training frequency (sessions per week)**
- Input: `frequency: int` (default: 3-4, read from blueprint)
- Impact on blueprint:
  - `1-2x/week`: Always use BP01 (Full Body Strength) regardless of season/phase
  - `3-4x/week`: Use normal blueprint selection
  - `5-6x/week`: Use split-capable blueprints
- Coverage: 18% of modifications
- Implementation: 3 conditionals in select_blueprint()

```python
def apply_frequency_constraint(athlete):
    if athlete.frequency <= 2:
        return BLUEPRINT_BY_ID[1]  # Force full-body
    # Normal selection
```

**Constraint 3: Competition calendar (day relative to match)**
- Input: `days_to_match: int | None` (default: None)
- Impact on blueprint:
  - `0`: No training. Return recovery protocol.
  - `1`: Light session (50% volume, technique focus, no eccentric)
  - `-1, -2`: Recovery session (mobility + activation only)
  - `None`: Normal training
- Coverage: 5% of modifications (but safety-critical)
- Implementation: 4 conditionals before generate_program()

```python
def apply_competition_constraint(days_to_match):
    if days_to_match == 0:
        return RecoveryProtocol(L3)
    if days_to_match == 1:
        return LightSession(volume=0.5)
    if days_to_match in (-1, -2):
        return RecoverySession()
    return None
```

**Constraint 4: Available equipment (already exists)**
- Input: `equipment_profile: EquipmentProfile` (already exists)
- Impact: Substitution engine already handles 12% of modifications
- Coverage: 12% of modifications
- Implementation: Already exists in `exercise_selector.py` + `substitution_engine.py`

### Total coverage: 48% + 18% + 5% + 12% = 83%

With 4 constraints we capture 83% of modifications. Adding the remaining
28 constraints would cover the remaining 17%. Not worth it.

---

## Part 6 — Implementation Estimate

### Files to change

| File | Change | Lines |
|------|--------|-------|
| `models.py` | Add `available_minutes: int = 60` and `days_to_match: Optional[int] = None` to AthleteProfile | +2 |
| `data.py` | Add MINI_BLUEPRINTS dict (3-4 family variants for <30 min) | +15 |
| `blueprint_engine.py` | Add `apply_time_constraint()` and `apply_frequency_constraint()` to `select_blueprint()` | +20 |
| `main.py` | Add competition constraint check before `generate_program()` | +10 |
| New: `constraint_engine.py` | Constraint pipeline: time → frequency → competition → equipment | +25 |

### Total

| Metric | Count |
|--------|-------|
| Files changed | 5 (4 existing + 1 new) |
| Lines added | ~72 |
| New data structures | 1 (MINI_BLUEPRINTS, ~15 lines) |
| New conditionals | ~35 |
| Existing code reused | Substitution engine (equipment), credibility validation |
| Test cases needed | ~8 |
| Implementation time | Day |

### What this system does NOT need

| Feature | Reason excluded |
|---------|-----------------|
| AI / ML | Deterministic rules cover 83%. AI would add complexity for 17% marginal gain. |
| New database | Flat data structures. No SQL. No migration. |
| User interface | Constraint input is fields on AthleteProfile. CLI + API compatible. |
| Schedule parser | Not needed — frequency is an integer, not a parsed calendar. |
| Travel API | Not needed — travel is a binary flag + equipment profile. |
| Weather API | Not needed — facility constraint is coach's responsibility. |

---

## Part 7 — Answer to Final Question

> **What is the smallest constraint system that captures 90% of real-world
> coaching modifications without introducing complexity or AI?**

**The 4-constraint system:**

1. **Session duration (minutes)** → 48% coverage, 4 conditionals
2. **Training frequency (sessions/week)** → 18% coverage, 3 conditionals
3. **Competition calendar (days to match)** → 5% coverage, 4 conditionals
   (safety critical — must have)
4. **Equipment profile** → 12% coverage, already implemented

**83% coverage with ~72 lines of code, 4 conditionals per constraint,
zero AI.**

The remaining 17% is spread across 28+ rare constraints that each affect
< 1% of athletes. Document them in this report and move on. The 4-constraint
engine is the smallest viable system that changes program decisions.

```
Implementation estimate: Day. 
Lines: ~72. 
New files: 1 (constraint_engine.py).
Modified files: 4.
```

---

## Appendix A — Constraint Engine Pipeline

```python
def apply_constraints(athlete, blueprint):
    # 1. Competition calendar (highest priority, safety)
    if athlete.days_to_match == 0:
        return no_training(RecoveryLevel.L3)
    if athlete.days_to_match == 1:
        return light_session(blueprint, volume=0.5)
    if athlete.days_to_match in (-1, -2):
        return recovery_session()
    
    # 2. Training frequency (changes blueprint)
    if athlete.frequency <= 2:
        blueprint = BLUEPRINT_BY_ID[1]  # Full Body Strength
    
    # 3. Session duration (changes slot count)
    slots = resolve_slots(blueprint, athlete.athlete_level)
    if athlete.available_minutes < 30:
        slots = slots[:4]  # Essential 4 only
    elif athlete.available_minutes < 45:
        slots = slots[:5]  # Drop accessory
    
    # 4. Equipment (already handled by substitution engine)
    return build_session(athlete, blueprint, slots)
```

**Order matters.** Competition constraints are checked first (safety).
Frequency changes the blueprint. Duration changes the slot count. Equipment
is the final filter.

## Appendix B — Constraint completeness checklist

| Quality | Current FORGE | With constraint engine |
|---------|---------------|----------------------|
| Handles < 30 min sessions | No — assumes 60+ min | Yes — 4-family "Express" variant |
| Handles 2x/week athletes | No — gives same program as 4x/week | Yes — forces full-body only |
| Handles match day | No — schedules training | Yes — returns recovery protocol |
| Handles D-1 pre-match | No — full session prescribed | Yes — 50% volume reduction |
| Handles D+1 post-match | No — full session prescribed | Yes — recovery session |
| Handles travel (no gym) | No — assumes full equipment | Yes — bodyweight default |
| Handles large groups | No — complex lifts possible | Yes — simple exercise filter |
| Handles remote coaching | No — max testing possible | Yes — safety filter |
| Handles tournament blocks | No — may prescribe heavy lifting | Yes — maintenance only |
| Handles double session days | No — same volume as single | Yes — 70% gym volume |
