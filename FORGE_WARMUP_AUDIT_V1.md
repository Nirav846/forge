# FORGE Warmup Audit V1

**Date:** 2026-06-20
**Auditor:** opencode (mimo-v2.5-free)
**Scope:** Warmup engine (warmup_engine.py) and library spec (FORGE_WARMUP_LIBRARY_V1.md)

---

## 1. Current coverage inventory

### Total warmup drills in engine

| Category | Count in spec | Count in engine | Missing |
|----------|--------------|----------------|---------|
| Raise (R-*) | 14 | 14 | 0 |
| Hip Mobility (HM-*) | 18 | 3 | 15 |
| Thoracic/Shoulder (TS-*) | 14 | 3 | 11 |
| Core Activation (CA-*) | 10 | 2 | 8 |
| Ankle/Foot (AF-*) | 8 | 1 | 7 |
| Neck/Cervical (NC-*) | 6 | 1 | 5 |
| Glute Activation (GA-*) | 8 | 2 | 6 |
| Hamstring Activation (HA-*) | 4 | 1 | 3 |
| Potentiation (P-*) | 10 | 6 | 4 |
| Sport-Specific (SS-*) | 14 | 3 | 11 |
| **TOTAL** | **106** | **36** | **70** |

**Drill IDs in engine dictionary:** 36 unique drills out of 106 specified.

### Phase tagging

Every drill in the engine has a `phase` field set to one of: `raise`, `activate`, `potentiate`, `prepare`. The RAMP tagging is present for all 36 drills.

### Selection changes by

| Factor | Currently varies? | Notes |
|--------|-------------------|-------|
| gym vs ground vs court | **NO** | Warmup selection only by `session_type` string, not environment. |
| session type | **YES** | Different drill lists for strength/power/speed/conditioning/competition/youth/RTP. |
| athlete level | **NO** | `level` field on drills is always `"all"`. No filtering. |
| sport | **NO** | `sport_relevance` field exists but is not used in selection logic. |

---

## 2. Session-type coverage

### Lower-body strength gym session

**Output (strength session type):**
- Raise: Forward jog (2 min), Skipping (1 min)
- Activate: World's greatest stretch (1 min), Glute bridge (30s), Cat-cow (30s), Dead bug (30s)
- Potentiate: Sub-max bench (1 min), Sub-max squat (1 min)
- **Total:** 7.5 min

**Coach credibility:** Partial. Missing hip mobility drills (leg swings, fire hydrant), missing hamstring activation (Nordic curl), missing band activation (lateral band walk). The potentiate phase includes bench press for a lower-body session, which is mismatched. A coach would expect squat-pattern potentiation only.

### Upper-body strength gym session

**Output:** Same as lower-body (strength session type does not distinguish upper/lower). Sub-max bench and squat both appear.

**Coach credibility:** Low. Upper-body session should emphasize shoulder/ T-spine mobility, scapular activation, and bench/pull potentiation. Squat potentiation is wasted.

### Speed session

**Output (speed session type):**
- Raise: Forward jog, Backward jog, Side shuffle, Carioca (5 min)
- Activate: Leg swings front/back, Leg swings side/side, World's greatest stretch, Lateral band walk (4 min)
- Potentiate: Build-up sprint (60-80%), Skips for height (2 min)
- **Total:** 11 min

**Coach credibility:** Moderate. Missing sprint mechanics drills (A-Skip, B-Skip, wall drills, ankling). The potentiate phase includes only two drills; a real speed warmup would have 4-6 sprint drills (marches, skips, bounds, buildups). The raise phase is generic jogging, not progressive acceleration.

### Field conditioning session

**Output (conditioning session type):**
- Raise: Forward jog, Side shuffle (3 min)
- Activate: Leg swings, World's greatest stretch, Plank (3 min)
- Potentiate: Build-up sprint (1 min)
- **Total:** 7 min

**Coach credibility:** Low. Too short (7 min vs typical 14-18 min). Missing dynamic stretching, missing movement prep at goal pace. Plank is not appropriate for conditioning warmup (core activation is fine but not in potentiate). No final bout at target intensity.

### Court conditioning session

**Output:** Same as field conditioning (no environment differentiation).

**Coach credibility:** Very low. No split-step prep, no lateral shuffle patterns, no decel/re-accel footwork, no ankle stiffness drills. Court warmup must differ from field.

### Power/plyometric session

**Output (power session type):**
- Raise: Forward jog, Side shuffle, Skipping (4 min)
- Activate: Leg swings, World's greatest stretch, Glute bridge (2.5 min)
- Potentiate: Box jump, Band-resisted sprint starts (2 min)
- **Total:** 8.5 min

**Coach credibility:** Moderate. Missing med-ball throws (rotational, slams), missing broad jumps, missing plyometric prep drills. The potentiate phase includes only box jump and sprint start; a power session should include multiple explosive patterns.

### Mixed modal / GPP session

**Output:** Falls back to strength session type (no dedicated mapping).

**Coach credibility:** Low. GPP session should blend strength/power/conditioning warmup elements. Using pure strength warmup misses conditioning prep.

### Deload session

**Output:** No deload session type exists. Falls back to strength.

**Coach credibility:** Low. Deload warmup should be shorter, lower intensity, focused on mobility and blood flow, not sub-max lifts.

---

## 3. Missing high-value sprint/ground drills

| Drill | Present in engine? | Present in spec? | Used in speed warmup? |
|-------|-------------------|------------------|----------------------|
| Ankling | **NO** | **NO** | — |
| A-March | **NO** | **NO** | — |
| A-Skip | **NO** | **NO** | — |
| B-Skip | **NO** | **NO** | — |
| C-Skip | **NO** | **NO** | — |
| Straight Leg March | **NO** | **NO** | — |
| Straight Leg Bound | **NO** | **NO** | — |
| Wall Drill March | **NO** | **NO** | — |
| Wall Drill Switch | **NO** | **NO** | — |
| Fast Leg | **NO** | **NO** | — |
| Build-up accelerations | **YES** (P-06) | YES | YES |
| Wicket-style rhythm drills | **NO** | **NO** | — |

**Conclusion:** The warmup engine lacks the entire sprint mechanics drill library. Speed warmups are generic jogging + two potentiation drills, not a proper sprint prep sequence.

---

## 4. Missing high-value court drills

| Drill | Present in engine? | Present in spec? | Used in any warmup? |
|-------|-------------------|------------------|---------------------|
| Split-step prep | **NO** | **NO** | — |
| Reactive shuffle | **NO** | **NO** | — |
| Lateral shuffle (dynamic) | **YES** (R-03) | YES | YES |
| Crossover run | **NO** | **NO** | — |
| Carioca / hip-turn footwork | **YES** (R-04) | YES | YES |
| Lunge-recover patterns | **NO** | **NO** | — |
| Decel/re-accel footwork | **NO** | **NO** | — |
| Multi-directional hop / ankle stiffness | **NO** | **NO** | — |

**Conclusion:** Court warmup includes only side shuffle and carioca from the raise phase. No court-specific activation, no split-step prep, no deceleration/re-acceleration patterns. Tennis/badminton warmups are generic, not court-specific.

---

## 5. Throwing / overhead athlete prep coverage

| Component | Present in engine? | Notes |
|-----------|-------------------|-------|
| Hip flexor activation | **PARTIAL** | HM-16 (kneeling hip flexor stretch) exists in spec but not in engine. |
| Trunk/anti-rotation prep | **PARTIAL** | CA-05 (Pallof press) exists in spec but not in engine. |
| T-spine mobility | **YES** | TS-01 (cat-cow) present, TS-02/03/04 missing. |
| Scap/serratus activation | **PARTIAL** | TS-08 (scap push-ups) exists in spec but not in engine. |
| Hip-shoulder separation | **PARTIAL** | R-11 (lunge with twist) present, but not used in any session type. |
| Med-ball potentiation | **PARTIAL** | P-03/P-04 exist in spec but not in engine. |

**Sport-specific support:**
- Cricket fast bowlers: No bowling run-up rehearsals (SS-02 missing), no counter-rotation prep.
- Cricket batters: No shadow batting (SS-01 missing), no rotational prep.
- Tennis serve players: No serve prep (SS-06 missing), no shoulder external rotation.
- Badminton smash players: No overhead clear prep (SS-08 missing), no scapular retraction.

**Conclusion:** Overhead athlete prep is absent. The engine cannot differentiate between a cricket bowler and a soccer player.

---

## 6. Warmup realism

### Real coach's gym warmup

A coach would expect: 3-5 min general raise, 5-8 min targeted activation/mobility (hip flexors, glutes, T-spine), 3-5 min pattern-specific potentiation (sub-max sets of the day's lifts), 2-3 min ramp sets.

**FORGE output:** Raise (3 min), Activate (2.5 min), Potentiate (2 min). Total 7.5 min. Missing hip mobility, hamstring activation, band work. Potentiate includes bench for lower-body session. **Not credible.**

### Real sprint warmup

A coach would expect: 5-8 min progressive run, 5-8 min sprint mechanics (marches, skips, bounds), 5-8 min acceleration drills (wall drills, buildups), 3-4 min full-speed buildups.

**FORGE output:** Raise (5 min generic jogging), Activate (4 min mobility), Potentiate (2 min: one sprint, one skip). Total 11 min. Missing all sprint mechanics. **Not credible.**

### Real court warmup

A coach would expect: 5-8 min general raise, 5-8 min lateral/reactive footwork (split-steps, shuffles, crossover runs), 5-8 min decel/re-accel patterns, 3-5 min sport-specific rehearsal.

**FORGE output:** Same as field conditioning (7 min). No court-specific drills. **Not credible.**

### Real pre-throw / overhead warmup

A coach would expect: 5-8 min general raise, 5-8 min shoulder/scap/T-spine prep, 5-8 min rotational/hip-shoulder separation drills, 3-5 min med-ball potentiation.

**FORGE output:** Generic strength warmup (7.5 min). No shoulder prep, no rotational drills. **Not credible.**

---

## 7. Gap ranking

### P0 — Coach would object immediately

| Gap | Why it matters | How often affected | Smallest fix |
|-----|----------------|-------------------|--------------|
| Missing sprint mechanics drills (A-Skip, B-Skip, wall drills, ankling) | Speed sessions get generic jogging warmup, not sprint prep. Every speed session. | 100% of speed sessions | Add 8-10 sprint drills to WARMUP_DRILLS dict, add to speed warmup mapping. |
| Missing court-specific drills (split-step, decel/re-accel, lateral patterns) | Court sessions get field warmup. Every court session. | 100% of court sessions | Add 6-8 court drills, create court environment routing. |
| Warmup does not vary by environment (gym/ground/court) | Same warmup for all environments. | 100% of sessions | Add environment parameter to select_warmup, create environment-specific drill pools. |
| Missing sport-specific overhead prep (cricket, tennis, badminton) | Overhead athletes get generic warmup. | 100% of overhead sport sessions | Add sport-specific drills, add sport tag filtering. |
| Referenced drill IDs missing from dictionary (HM-06, HM-10, TS-07, TS-03, AF-07, SS-01, SS-03, P-03) | Session type mappings reference drills that don't exist; those drills are silently dropped. | Every session using those mappings | Add missing drills to dictionary or update mappings. |

### P1 — Important realism / sport prep gap

| Gap | Why it matters | How often affected | Smallest fix |
|-----|----------------|-------------------|--------------|
| Strength warmup doesn't distinguish upper vs lower | Upper-body session gets squat potentiation. | 50% of strength sessions | Add upper/lower sub-type routing. |
| No deload session warmup | Deload gets full warmup. | Deload sessions | Add "deload" session type mapping with shorter, lighter warmup. |
| No youth-specific warmup adjustments | Youth gets same drills as adult. | Youth sessions | Already has youth mapping, but includes box jump (potentiate) which may not be age-appropriate. Review. |
| Warmup duration too short for some sessions | Conditioning warmup is 7 min (should be 14-18). | Conditioning sessions | Adjust drill durations or add more drills per phase. |
| Missing hip flexor activation (HM-16), Pallof press (CA-05), scap push-ups (TS-08) | Key activation drills absent. | Many sessions | Add these drills to dictionary. |

### P2 — Nice-to-have polish

| Gap | Why it matters | How often affected | Smallest fix |
|-----|----------------|-------------------|--------------|
| No athlete level filtering | Beginner gets same warmup as advanced. | All sessions | Add level-based duration scaling. |
| No sport_relevance filtering | All sports get same drills. | All sessions | Add sport tag to drill selection logic. |
| Missing travel/tournament warmup protocols | No special warmup for tournament days. | Tournament days | Add competition-specific warmup variants. |
| No time-constrained warmup option | Warmup always runs full duration. | Sessions with tight time limits | Add time-based drill trimming. |

---

**Summary:** The warmup engine has 36 of 106 drills, no environment/sport differentiation, missing all sprint mechanics and court-specific drills, and produces generic warmups that a coach would reject for speed, court, and overhead sessions. The highest-value fixes are adding missing drills and environment-based routing.
