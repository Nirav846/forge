# FORGE_GAPS_REPORT — Knowledge Gaps & Missing Domains

> Identifies what FORGE's coaching knowledge is missing.
> Every gap is a place where the system may generate low-credibility output
> because the underlying pattern database has insufficient evidence.
> Gaps are actionable: each includes a recommendation for filling it.

---

## Gap Scoring

Each gap is scored on two axes:

- **Impact** (1–5): How much does this gap reduce FORGE output quality?
- **Fill Difficulty** (1–5): How hard is it to close this gap (1 = easy, 5 = requires new source acquisition)?

Priority = Impact + Fill Difficulty. Higher = close first.

---

## GAP 1: Missing Sports Coverage

### Current Sports Covered

| Sport | Blueprints | Exercise Families | Conditioning Protocols | Sources |
|-------|-----------|-------------------|----------------------|---------|
| Rugby / American Football | Full | Full | Full | 9 sources |
| Tennis / Badminton / Basketball / Volleyball / Netball / Squash | Partial | Full | Full | 8 sources |
| Track & Field / Sprint | Full | Full | Full | 5 sources |
| General S&C | Full | Full | Full | 20 sources |

### Missing Sports

| Sport | Impact | Fill Difficulty | Priority | Gap Detail |
|-------|--------|----------------|----------|------------|
| **Football (Soccer)** | 5 | 2 | 7 | Most globally played sport. Zero dedicated blueprints. Generic blueprints used. No sport-specific mandatory exercise rules. Conditioning library covers generic systems but no soccer-specific RSA protocols (e.g., Yo-Yo IR1 integration, position-specific COD demands). |
| **Field Hockey** | 3 | 3 | 6 | Similar demands to court sports but with unique trunk flexion posture and equipment constraints. No dedicated blueprint or sport-specific rules. |
| **Baseball / Softball** | 3 | 3 | 6 | Unique demands: rotational power (batting), overhead throwing, short-duration explosive sprints. No dedicated blueprint. Rotational family exists but no sport-specific progression. |
| **Swimming** | 2 | 4 | 6 | Unique dry-land S&C requirements. No aquatic-specific family or programming rules. |
| **Combat Sports (Boxing, MMA, Wrestling)** | 2 | 4 | 6 | Unique conditioning demands (intermittent high-intensity + strength endurance). No sport-specific conditioning protocols or blueprint. |
| **Golf** | 1 | 3 | 4 | Rotational power emphasis. Low injury risk. Low priority. |
| **Cycling** | 1 | 4 | 5 | Unique lower-body dominant adaptation. No cycling-specific strength transfer rules. |
| **Winter Sports (Skiing, Ice Hockey)** | 2 | 4 | 6 | Unique demands: eccentric strength (skiing), skating-specific hip mechanics (hockey). No dedicated blueprints. |

**Recommendation:** Add Football (Soccer) as next sport expansion. Requires: 1 dedicated blueprint, soccer-specific COD conditioning protocols, position-specific rules (forward vs defender volume differences).

---

## GAP 2: Missing Conditioning Methods

### Systems Covered (10 of 10)

| System | Protocols | A-Tier | B-Tier | C-Tier | Status |
|--------|-----------|--------|--------|--------|--------|
| Recovery Conditioning | ✓ | ✓ | ✓ | — | Complete |
| Aerobic Capacity | ✓ | ✓ | ✓ | — | Complete |
| Aerobic Power | ✓ | ✓ | ✓ | — | Complete |
| Extensive Tempo | ✓ | ✓ | ✓ | — | Complete |
| Intensive Tempo | ✓ | ✓ | ✓ | — | Complete |
| Repeated Sprint Ability | ✓ | ✓ | ✓ | — | Complete |
| Alactic Speed | ✓ | ✓ | ✓ | — | Complete |
| Lactate Tolerance | ✓ | ✓ | ✓ | — | Complete |
| Power Maintenance | ✓ | ✓ | ✓ | — | Complete |
| (Empty) | — | — | — | — | Structure allows 1 more system |

### Missing Conditioning Knowledge

| Gap | Impact | Fill Difficulty | Priority | Detail |
|-----|--------|----------------|----------|--------|
| **Altitude training protocols** | 2 | 4 | 6 | CL035 mentions altitude adjustment but no protocols designed for altitude. Missing: hypoxic training protocols, sea-level return guidelines. |
| **Heat acclimation protocols** | 3 | 3 | 6 | CL034 mentions heat adjustment but no protocols designed for hot environments. Missing: wet-bulb globe temperature (WBGT) integration, hydration protocols with conditioning. |
| **Return-to-play conditioning progression** | 4 | 3 | 7 | No specific return-to-play (RTP) conditioning progression. Current system only has RTS Foundation — which covers strength but not conditioning re-entry. Missing: graduated aerobic re-introduction after concussion, lower-body injury re-entry protocols. |
| **Youth-specific conditioning volumes** | 3 | 3 | 6 | CL027-028 cover youth limits but no positive prescription. Missing: what SHOULD youth do, not just what they shouldn't. Play-based conditioning protocols absent. |
| **Pool/anti-gravity conditioning** | 1 | 4 | 5 | Low-impact alternatives for injured athletes. Missing: deep-water running protocols, pool-based interval templates. |

**Recommendation:** Highest priority is RTP conditioning progression (Gap 3) — currently the system can return an athlete to strength work but has no structured conditioning re-entry pathway.

---

## GAP 3: Missing Youth Models

### Current Youth Coverage

| Aspect | Status | Detail |
|--------|--------|--------|
| Youth Foundation Blueprint (U14-U20) | ✓ Exists | Blueprint 07 is dedicated youth program |
| Youth Level Caps | ✓ Implemented | U16 max Intermediate, no 1RM, no depth jumps |
| Youth Conditioning Limits | ✓ Implemented | No lactate tolerance (CL027), HSR ≤ 400m/session |
| Youth Progression Model | ✗ Missing | No structured progression framework for youth athletes |
| Youth LTAD Integration | ✗ Missing | No long-term athletic development (LTAD) model alignment |
| Youth Sport-Specific Rules | ✗ Missing | No differentiation between early-specialization sports (gymnastics, tennis) and late-specialization sports (rugby, football) |
| Youth Assessment Protocols | ✗ Missing | No youth-specific movement screens or fitness tests |
| Youth Bio-Banding Integration | ✗ Missing | No maturity offset calculation (Khamis-Roche, Mirwald) |

### Youth Knowledge Gaps

| Gap | Impact | Fill Difficulty | Priority | Detail |
|-----|--------|----------------|----------|--------|
| **Pre-pubescent training guidelines** | 4 | 3 | 7 | Current system treats "youth" as U14-U20 monolithic group. Missing: differentiation between pre-pubescent (U12), circum-pubescent (U12-U15), and post-pubescent (U15-U20). Each has different trainability, injury risk profile, and adaptation window. |
| **LTAD stage modeling** | 4 | 4 | 8 | FORGE has no concept of LTAD stages (FUNdamentals, Learn to Train, Train to Train, Train to Compete, Train to Win). Blueprint 07 covers "Youth Foundation" but doesn't differentiate between a 12-year-old beginner (Train to Train) and a 17-year-old advanced (Train to Compete). |
| **Peak height velocity calibration** | 3 | 5 | 8 | During PHV, injury risk spikes (apophysitis, growth plate injuries) and strength gains plateau. MISSING: PHV detection, training volume reduction rules around PHV, tendon-specific loading protocols during growth spurts. |
| **Early vs late specialization rules** | 3 | 3 | 6 | FORGE does not distinguish between sports where early specialization is required (gymnastics, figure skating — peak performance pre-puberty) and those where it's harmful (rugby, football — increased injury, burnout). Missing: sport-specific youth pathway differentiation. |
| **Youth strength trainability** | 2 | 2 | 4 | Current system caps youth at Intermediate. This is safe but conservative. Missing: nuance that pre-pubescent strength gains are primarily neural (no hypertrophy from testosterone), post-pubescent introduces hypertrophy window. Missing: youth-specific rep ranges (higher reps, lower load for neural adaptation). |
| **Youth plyometric progression** | 3 | 2 | 5 | P-2002 (≤30 ground contacts) and P-2005 (no depth jumps >1ft) cover safety but MISSING: proper youth plyometric progression from low-intensity (pogo jumps, skipping) to moderate (box jumps, hurdle hops) to high (depth jumps). No age-based plyometric volume tables. |

**Recommendation:** This is the largest knowledge gap in FORGE. The system can keep youth SAFE but cannot OPTIMIZE youth development. Solution: implement LTAD stage modeling, add PHV detection (maturity offset calculation), differentiate U12/U15/U18 progression pathways, and add youth-specific plyometric progression tables.

---

## GAP 4: Missing Return-to-Play Models

### Current RTP Coverage

| Aspect | Status | Detail |
|--------|--------|--------|
| Return to Sport Foundation Blueprint | ✓ Exists | Blueprint 12 — focuses on prehab + light strength |
| Chronic Injury Management | ✓ Partial | Injury substitution table (10 injury types) in Substitution Matrix |
| ACL Prehab/Rehab | ✓ Partial | Exercise exclusions for ACL history |
| RTP Conditioning | ✗ Missing | No graduated conditioning re-entry (see Gap 2) |
| Concussion RTP | ✗ Missing | No concussion-specific protocols or clearance criteria |
| Post-Surgical Rehab Integration | ✗ Missing | No post-surgical timelines (weeks 1-4, 4-8, 8-12, 12+ separate phases) |
| Criteria-Based RTP Milestones | ✗ Missing | No objective return criteria (strength symmetry, hop test, YBT scores, etc.) |

### RTP Knowledge Gaps

| Gap | Impact | Fill Difficulty | Priority | Detail |
|-----|--------|----------------|----------|--------|
| **Post-surgical phase modeling** | 4 | 4 | 8 | ACL reconstruction, shoulder labrum repair, meniscectomy — each has different tissue healing timelines, load tolerance windows, and exercise contraindications. MISSING: phase-based return protocols (non-weight-bearing → partial → full → plyometric → sport-specific). Current system treats all injuries with the same "avoid explosive" rule. |
| **Strength symmetry return criteria** | 4 | 3 | 7 | No LSI (Limb Symmetry Index) requirements for return to sport. Example: ACL return typically requires LSI > 90% on quad strength, > 90% on hop tests. MISSING: sport-specific LSI thresholds, retesting intervals, and exercise progression linked to LSI scores. |
| **Pain-guided exercise modification** | 3 | 2 | 5 | Current system only flags injury history at selection time. MISSING: real-time pain response guidance. V097 (pain overrides progression) is noted but no mechanism to modify sets/reps/load based on pain response (traffic light system: green = pain-free, amber = discomfort but safe, red = stop). |
| **Tendinopathy management** | 3 | 4 | 7 | Tendinopathy (patellar, Achilles, hamstring) requires specific load management: isometric loads for immediate pain relief, heavy slow resistance for adaptation, energy storage loading for return to sport. MISSING: tendinopathy-specific exercise selection, load progression rules. |
| **Return-to-play after concussion** | 2 | 5 | 7 | Concussion RTP is sequential (rest → light aerobic → sport-specific exercise → non-contact practice → full practice → competition). MISSING: any concussion protocols. Athletes with concussion history are currently treated identically to non-concussed athletes. |
| **Reducing re-injury risk** | 4 | 4 | 8 | No secondary prevention rules. Example: athlete returning from hamstring strain has 30%+ re-injury rate in first month without eccentric hamstring loading. MISSING: automatic eccentric hamstring addition for hamstring injury history, automatic plyometric progression regression for ACL history. |

**Recommendation:** Build post-surgical phase models for the 3 most common procedures (ACL reconstruction, shoulder labrum, meniscus). Add LSI-based return criteria. Add automatic secondary prevention for common re-injury patterns (eccentric hamstring after strain, isometric patellar after tendinopathy, progressive plyometrics after ACL).

---

## GAP 5: Missing Periodization Models

### Current Periodization Coverage

| Aspect | Status | Detail |
|--------|--------|--------|
| Season Phase-Based Selection | ✓ Complete | Off-season → pre-season → in-season → transition |
| Blueprint Progression Paths | ✓ Complete | Each blueprint has progression/regression paths |
| Deload Rules | ✓ Partial | Every 4-6 week deload noted (law V049) but not automatically scheduled |
| Block Periodization | ✗ Missing | No concept of mesocycle blocks within season phases |
| Concurrent Training Rules | ✗ Missing | No guidelines for concurrent strength + endurance training interference |
| Tapering Protocols | ✗ Missing | No competition taper progression (step taper, linear taper, exponential taper) |
| Undulating Periodization | ✗ Missing | No daily/weekly undulating periodization models |
| Accumulation → Intensification → Realization | ✗ Missing | No 3-phase block structure (common in track & field and weightlifting) |

### Periodization Knowledge Gaps

| Gap | Impact | Fill Difficulty | Priority | Detail |
|-----|--------|----------------|----------|--------|
| **Concurrent training interference** | 4 | 4 | 8 | FORGE treats strength and conditioning as independent selections. Research (Hickson, 1980; Wilson et al., 2012) shows concurrent strength + endurance training can blunt strength/hypertrophy adaptations. MISSING: rules for separating strength and conditioning sessions (≥6h apart for interference minimization), periodized alternation (strength blocks vs conditioning blocks), sport-specific concurrent training models. |
| **Taper/progression for competition** | 3 | 4 | 7 | No systematic taper for competition preparation. P-6002 (pre-season decrease volume) exists but no specific: step taper (maintain intensity, drop volume in discrete steps), linear taper (daily volume decrease), or exponential taper (fast/slow decay). |
| **Undulating periodization models** | 3 | 3 | 6 | DUP (Daily Undulating Periodization) varies sets/reps/load daily within the same week. WUP (Weekly Undulating Periodization) varies weekly focus. MISSING: integration of undulating models within existing blueprints. |
| **3-phase block periodization** | 3 | 4 | 7 | Track & field and weightlifting use: accumulation (high volume, moderate intensity) → intensification (moderate volume, high intensity) → realization (low volume, peak intensity). MISSING: this framework for sport-specific peaking. |
| **Microcycle structure** | 3 | 2 | 5 | Current system generates individual sessions. MISSING: microcycle-level rules (e.g., "hard day → easy day → hard day" alternation, session distribution across the week, daily undulation patterns). |

**Recommendation:** Implement concurrent training interference rules (session separation ≥6h). Add microcycle structuring (weekly session distribution with hard/easy alternation). Build periodization frameworks for the 3 major sport categories (contact, court, sprint).

---

## GAP 6: Missing Coaching Principles

### Current Coaching Knowledge

| Aspect | Status | Detail |
|--------|--------|--------|
| Player Safety Overrides | ✓ Implemented | V097-V100 — pain, missed sessions, return from break |
| Exercise Coaching Cues | ✗ Missing | No cue library. Renderer has coaching_notes field but no automated coaching cue generation. |
| Athlete Communication Frameworks | ✗ Missing | No feedback models, no athlete-coach interaction patterns |
| Group vs Individual Programming Rules | ✗ Missing | No guidance on individualization within group templates |
| Load Management Decision Trees | ✗ Partial | Fatigue level tracked, deload rules exist but automated load adjustment missing |
| Session Rating Methods | ✗ Missing | No session RPE (sRPE) integration, no load monitoring frameworks |
| Velocity-Based Training Integration | ✗ Missing | No VBT zones, no velocity drop-off thresholds, no velocity-based load adjustment |

### Coaching Knowledge Gaps

| Gap | Impact | Fill Difficulty | Priority | Detail |
|-----|--------|----------------|----------|--------|
| **Coaching cue library** | 3 | 2 | 5 | Every exercise should have an external cue (movement outcome focus) and internal cue (body position focus). MISSING: cue database linked to each exercise, cue progression (beginner → internal cues, advanced → external cues), cue modification for specific athlete learning styles. |
| **Autoregulation rules** | 4 | 3 | 7 | Current system has fixed sets/reps/rest. MISSING: autoregulation rules (RPE-based load adjustment, velocity-based intensity zones, failure-stop rules, warm-up set max velocity thresholds). The spec says "no auto-regulation" but this is a gap for program quality. |
| **Session RPE integration** | 2 | 2 | 4 | sRPE (session rating of perceived exertion) is the most common load monitoring tool in team sports. MISSING: automated sRPE tracking across sessions, acute:chronic workload ratio calculations, week-to-week load progression guided by sRPE data. |
| **Communication frameworks** | 2 | 3 | 5 | No guidance on how coaches communicate program changes, exercise substitutions, or progressions to athletes. MISSING: decision rationale templates, athlete understanding verification (teach-back method), conflict resolution protocols. |
| **Group template individualization** | 3 | 4 | 7 | Most team sport programs use group templates with individual modifications. MISSING: rules for how to individualize within a group template (e.g., 80% shared exercises, 20% individual work for position/injury discrepancies). |

**Recommendation:** Build a coaching cue database (exercise → {external cue, internal cue, beginner-friendly default}). Add autoregulation rules using warm-up set velocity/performance as intensity guide. Add sRPE tracking integration framework.

---

## GAP 7: Missing Equipment Profiles

### Current Equipment Coverage

| Profile | Equipment Items | Coverage |
|---------|----------------|----------|
| Field Only | 7 items | Bodyweight + bands + med balls + basic implements |
| Basic Gym | 10 items | Barbell + dumbbell + rack + bench + cable |
| Commercial Gym | 12 items | Above + machines + full cable |
| Elite Facility | 16 items | Everything + sled + specialty bars + rings + GHD + platform |

### Equipment Knowledge Gaps

| Condition | Impact | Fill Difficulty | Priority | Detail |
|-----------|--------|----------------|----------|--------|
| **Home gym setups** | 3 | 2 | 5 | Modern home gyms often have adjustable dumbbells + resistance bands + pull-up bar but no barbell or rack. Current system would bucket this as Field Only (no barbell) which loses all barbell exercises even when alternatives exist. |
| **Hotel/travel gym** | 2 | 2 | 4 | Limited dumbbells (up to 25kg), perhaps a cable station, often no barbell. V083 addresses travel but no dedicated profile. |
| **Rehab clinic** | 2 | 2 | 4 | Limited load (up to 20kg dumbbells), bands, cables, balance equipment. No dedicated profile. |
| **School gym (youth)** | 3 | 2 | 5 | Light barbells (20kg technique bars), no heavy dumbbells, limited rack height for youth. No dedicated profile. |

**Recommendation:** Add a "Home Gym" equipment profile between Field Only and Basic Gym. Add provisional substitution rules for travel scenarios (maintain family order, downgrade equipment).

---

## Gap Priority Matrix

| Gap | Domain | Impact | Fill Difficulty | Priority Score |
|-----|--------|--------|----------------|---------------|
| 🥇 | Youth LTAD + bio-banding | 4 | 5 | 9 |
| 🥇 | Post-surgical phase modeling | 4 | 4 | 8 |
| 🥇 | Reducing re-injury risk | 4 | 4 | 8 |
| 🥇 | Concurrent training interference | 4 | 4 | 8 |
| 🥇 | Peak height velocity calibration | 3 | 5 | 8 |
| 🥈 | Football (Soccer) sport expansion | 5 | 2 | 7 |
| 🥈 | RTP conditioning progression | 4 | 3 | 7 |
| 🥈 | Pre-pubescent training guidelines | 4 | 3 | 7 |
| 🥈 | Strength symmetry return criteria | 4 | 3 | 7 |
| 🥈 | Tendinopathy management | 3 | 4 | 7 |
| 🥈 | Concussion RTP | 2 | 5 | 7 |
| 🥈 | Autoregulation rules | 4 | 3 | 7 |
| 🥈 | Group template individualization | 3 | 4 | 7 |
| 🥈 | Taper/progression for competition | 3 | 4 | 7 |
| 🥈 | 3-phase block periodization | 3 | 4 | 7 |
| 🥉 | LTAD stage modeling | 4 | 4 | 8 |

---

## Gap Closure Roadmap

### Phase 1 (Next — Fill highest-impact missing domains)

1. **Return-to-Play expansion**: Post-surgical phase models for ACL, shoulder, meniscus. Add LSI-based return criteria. Add secondary prevention rules for re-injury reduction.
2. **Concurrent training rules**: Session separation ≥6h for strength + conditioning. Periodized alternation of emphasis within microcycles.
3. **Youth differentiation**: Split Blueprint 07 (Youth Foundation) into U12, U14-U16, U18+ variants. Add PHV detection framework. Add LTAD stage alignment.

### Phase 2 (Medium-term — Strengthen existing domains)

4. **Football (Soccer) expansion**: Re-purpose Court Sport AD or create dedicated blueprint. Add soccer-specific conditioning protocols (Yo-Yo integration, position-specific COD).
5. **Autoregulation integration**: Add warm-up velocity threshold guidance. Add RPE-based load adjustment framework. Add failure-stop rules.
6. **Coaching cue library**: Build exercise → {external cue, internal cue} database. Add cue progression by athlete level.

### Phase 3 (Long-term — Complete the system)

7. **Periodization integration**: Block periodization templates for 3 major sport categories. Taper protocols. Microcycle structuring.
8. **Sports expansion**: Field hockey, baseball, combat sports, winter sports.
9. **Equipment expansion**: Home gym profile, school gym profile, hotel/travel substitution rules.

---

## Gaps by FORGE Version

| FORGE Version | Gaps Closed | Remaining Critical Gaps |
|--------------|-------------|------------------------|
| V1 (current) | None | All of the above |
| V1.1 | RTP Conditioning (Gap 2/4), Football Blueprint (Gap 1) | Youth, Periodization, Coaching |
| V2 | Youth LTAD (Gap 3), Concurrent Training (Gap 5) | Equipment, Sport Expansion |
| V2.1 | Coaching Cues (Gap 6), Autoregulation (Gap 6) | Full sport coverage |
| V3 | Sport Expansion (Gap 1 completion), Equipment (Gap 7) | Continuous improvement only |

---

## Gap Tracking Format

Each gap in this report should be converted to a pattern extraction task:

```
GAP-XXX: [Gap Title]
  Domain: [Domain]
  Impact: [1-5]
  Fill Difficulty: [1-5]
  Priority: [Impact + Fill Difficulty]
  
  Missing Knowledge:
  - [Specific pattern 1 not yet extracted]
  - [Specific pattern 2 not yet extracted]
  
  Recommended Sources:
  - [Source to mine for this knowledge]
  - [Source to mine for this knowledge]
  
  Status: Open | In Progress | Partially Filled | Closed
  Resolution Date: YYYY-MM-DD
```

---

## Auto-Gap Detection Triggers

These conditions should automatically trigger a gaps report update:

1. **Validator consistently scores < 8/10 for a specific sport or input combination** → gap in that domain's pattern coverage
2. **Substitution engine returns null > 5% of the time for a family** → gap in that family's exercise depth
3. **Conditioning selector returns null > 5% of the time for a goal/environment combination** → gap in protocol library
4. **New source added to FORGE_SOURCE_CATALOG.md** → re-check all gaps for fill potential
5. **Consensus Engine marks a pattern as Situational or Rare** → check if a gap exists in that domain
