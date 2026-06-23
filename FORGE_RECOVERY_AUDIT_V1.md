# FORGE Recovery Audit V1

**Date:** 2026-06-20
**Auditor:** opencode (mimo-v2.5-free)
**Scope:** Recovery engine (recovery_engine.py) and library spec (FORGE_RECOVERY_LIBRARY_V1.md)

---

## 1. Current recovery inventory

### Recovery drills in engine

| Category | Count in spec | Count in engine | Notes |
|----------|--------------|----------------|-------|
| General recovery circuit | 8 stations | 8 | All present |
| Lower body recovery circuit | 8 stations | 8 | All present |
| Upper body recovery circuit | 8 stations | 8 | All present |
| Full body recovery circuit | 8 stations | 8 | All present |
| Pool recovery | 4 protocols | 4 | All present |
| Bike recovery | 3 protocols | 3 | All present |
| Mobility recovery | 4 protocols | 4 | All present |
| Travel recovery | 4 phases | 4 | Drills present, but not in protocols |
| Post-match recovery | 4 phases | 4 | Drills present, but not in protocols |
| Tournament recovery | 2 protocols | 0 | **Missing from protocols** |
| **Total drills** | **~50** | **47** | 3 travel/post-match drills missing from RECOVERY_DRILLS dict |

### Recovery protocols in engine

| Category | Count in spec | Count in engine | Notes |
|----------|--------------|----------------|-------|
| L1 protocols | 1 | 1 | Present |
| L2 protocols | 4 | 4 | Present |
| L3 protocols | 5 | 5 | Present |
| L4 protocols | 3 | 3 | Present |
| L5 protocols | 2 | 2 | Present |
| Travel protocols | 4 | 0 | **Missing** |
| Tournament protocols | 2 | 0 | **Missing** |
| Post-match phases | 1 (4 phases) | 0 | **Missing** |
| **Total protocols** | **22** | **15** | 7 protocols missing |

### Recovery changes by

| Factor | Currently varies? | Notes |
|--------|-------------------|-------|
| fatigue level | **YES** | L1-L5 mapped to different protocols. |
| session type | **YES** | strength/power/speed/conditioning/competition mapped to different protocols per fatigue level. |
| sport | **NO** | No sport-specific recovery. |
| environment | **NO** | No gym/field/court differentiation. |

---

## 2. Recovery realism

### L1 (Low fatigue — normal training)

**Output:** L1: Mobility + stretch — General mobility flow (10 min).

**Coach credibility:** Acceptable. After a standard session, 10 min mobility flow is reasonable. However, a coach might prefer a shorter stretch (5 min) or a walk. The protocol is generic but usable.

### L2 (Moderate fatigue — hard session)

**Strength:** L2: Lower body recovery circuit — foam rolling, stretching, walk (20 min).

**Coach credibility:** Good. Lower-body focused after heavy lifting is appropriate. Includes foam rolling, mobility, and light walk. A coach would accept this.

**Power:** L2: General recovery circuit — foam rolling, mobility, cat-cow, dead bug, child's pose (20 min).

**Coach credibility:** Moderate. General circuit is fine, but missing hip flexor stretch (couch stretch) and hamstring stretch. Power sessions stress hips more than general.

**Speed:** L2: Lower body recovery circuit — same as strength.

**Coach credibility:** Good. Speed sessions are lower-body dominant; lower-body recovery is appropriate.

**Conditioning:** L2: General recovery circuit — same as power.

**Coach credibility:** Moderate. Conditioning may be full-body; general circuit is fine. Missing bike or pool option for active recovery.

**Competition:** L2: General recovery circuit — same as power.

**Coach credibility:** Low. Competition recovery should include compression, elevation, hydration. General circuit is not enough.

### L3 (High fatigue — competition, travel)

**Strength:** L3: General circuit + bike — foam rolling, mobility, easy spin (30 min).

**Coach credibility:** Good. Combining circuit with bike is appropriate for high fatigue. The bike spin is long (20 min) but acceptable.

**Speed:** L3: Pool walk/jog (20 min).

**Coach credibility:** Moderate. Pool recovery after speed session is appropriate. However, only 20 min pool walk/jog is less effective than a combined circuit + pool.

**Conditioning:** L4: Full regeneration protocol — cold water immersion, full body mobility, tempo spin (45 min).

**Coach credibility:** Questionable. Jumping from L2 general circuit to L4 full regeneration (cold water immersion) is a big leap. L3 should be an intermediate step (e.g., pool + circuit). Cold water immersion after conditioning may blunt adaptation (as noted in spec: "Do not do after strength session").

**Competition:** L4: Full regeneration protocol — same as conditioning.

**Coach credibility:** Acceptable. Competition may justify L4, but the mapping for competition L2 is also L4 (see below). This means competition fatigue always jumps to L4, skipping L3.

### L4 (Very high fatigue — tournament block)

**All session types:** L4: Full regeneration protocol — cold water immersion, full body mobility, tempo spin (45 min).

**Coach credibility:** Acceptable for tournament days. Cold water immersion, mobility, and bike are appropriate. However, the protocol is identical for all session types; a coach might want more variety (e.g., contrast therapy, pool recovery).

### L5 (Extreme fatigue — end of tour)

**All session types:** L5: Rest day + recovery modalities — general mobility flow, easy spin (30 min).

**Coach credibility:** Moderate. Rest day with light mobility and spin is reasonable. However, the protocol is identical to L1 mobility flow + bike. A coach might expect more rest (no bike) or sleep extension guidance.

### Specific environment differentiation

| Environment | Currently differentiated? | Notes |
|-------------|---------------------------|-------|
| Light gym day recovery | **NO** | Same protocol as heavy gym day. |
| Heavy lower body day recovery | **YES** (L2 lower body circuit) | Good. |
| Hard sprint / field conditioning recovery | **PARTIAL** | Speed gets pool, conditioning gets L4 (too aggressive). |
| Court footwork / repeated COD recovery | **NO** | Same as general. |
| Pre-match taper recovery | **NO** | No taper-specific protocol. |
| Deload / restoration day recovery | **NO** | No deload-specific protocol. |

---

## 3. Redundancy / dead protocols

### Duplicate protocols

| Protocol | Issue |
|----------|-------|
| L5_cold_immersion | Uses `cold_water_immersion` drill twice. Redundant. Should be one drill with longer duration or replaced with contrast therapy. |

### Protocols never reachable

| Protocol | Reason unreachable |
|----------|-------------------|
| L3_deep_water_running | Not mapped in SESSION_TYPE_RECOVERY_MAP. Only appears in FATIGUE_LEVEL_PROTOCOLS[3] but that mapping is never used (engine uses SESSION_TYPE_RECOVERY_MAP first). |
| L3_pool_recovery_circuit | Not mapped in SESSION_TYPE_RECOVERY_MAP. Same as above. |
| L3_full_body_circuit | Not mapped in SESSION_TYPE_RECOVERY_MAP. Same as above. |
| L4_contrast_therapy | Not mapped in SESSION_TYPE_RECOVERY_MAP. |
| L4_sleep_extension | Not mapped in SESSION_TYPE_RECOVERY_MAP. |
| L5_cold_immersion | Not mapped in SESSION_TYPE_RECOVERY_MAP (L5_rest_day is used instead). |

**Note:** FATIGUE_LEVEL_PROTOCOLS dict exists but is never used by select_recovery (engine uses SESSION_TYPE_RECOVERY_MAP). This dict is dead code.

### Protocols too generic to matter

| Protocol | Issue |
|----------|-------|
| L1_mobility_stretch | Only contains general_mobility_flow (10 min). Very generic. Could be more targeted. |
| L5_rest_day | Contains general_mobility_flow + easy_spin. Same as L1 + bike. Not distinct enough. |

### Protocols too "sports science brochure" and not coach-usable

| Protocol | Issue |
|----------|-------|
| L4_sleep_extension | Includes general_mobility_flow + post_match_hydration. "Sleep extension" is not an active protocol; it's a recommendation. Coach would not prescribe "sleep extension" as a drill. |
| L4_contrast_therapy | Uses cold_water_immersion twice (simplified). Real contrast therapy requires alternating hot/cold. Not credible as written. |

---

## 4. Recovery gap ranking

### P0 — Coaching importance, high frequency, easy fix

| Gap | Why it matters | How often affected | Smallest fix |
|-----|----------------|-------------------|--------------|
| Competition L2 maps to L4 (skipping L3) | Competition fatigue at "elevated" level gets cold water immersion (L4) instead of intermediate recovery (L3). Too aggressive. | Every competition session with elevated fatigue | Change competition L2 mapping to L3 protocol (e.g., L3_general_circuit_bike). |
| Conditioning L3 maps to L4 (too aggressive) | Conditioning at high fatigue jumps to cold water immersion. Should be pool/circuit. | Every conditioning session with high fatigue | Change conditioning L3 mapping to L3_pool_walk_jog or L3_general_circuit_bike. |
| Travel/tournament protocols missing | No recovery protocol for travel days or tournament blocks. | Travel/tournament days | Add travel and tournament protocol mappings to SESSION_TYPE_RECOVERY_MAP. |
| Dead FATIGUE_LEVEL_PROTOCOLS dict | Confusing dead code. | Never (but维护 confusion) | Remove or integrate into selection logic. |
| L5_cold_immersion duplicate drill | Redundant drill list. | L5 recovery | Replace duplicate with contrast_therapy or remove protocol. |

### P1 — Important realism gap

| Gap | Why it matters | How often affected | Smallest fix |
|-----|----------------|-------------------|--------------|
| No sport-specific recovery | Cricket, tennis, badminton get same recovery as soccer. | All sport-specific sessions | Add sport tag filtering or sport-specific recovery circuits. |
| No environment differentiation (gym/field/court) | Court COD fatigue not addressed. | Court sessions | Add environment parameter to select_recovery. |
| No deload/restoration protocol | Deload sessions get same recovery as heavy sessions. | Deload sessions | Add "deload" session type mapping with lighter recovery. |
| No pre-match taper protocol | Pre-match recovery is same as regular. | Pre-match sessions | Add "taper" protocol for light activation + mobility. |
| Post-match phases not in protocols | Post-match 4-phase recovery (immediate/early/later/evening) not accessible. | Post-match | Add post-match protocol with phased approach. |

### P2 — Nice-to-have polish

| Gap | Why it matters | How often affected | Smallest fix |
|-----|----------------|-------------------|--------------|
| No compression/elevation guidance | Recovery protocols don't include compression/elevation instructions. | High fatigue sessions | Add notes to protocols about compression/elevation. |
| No hydration/nutrition timing | Recovery protocols don't specify nutrition timing. | All sessions | Add nutrition notes to protocol drills. |
| No sleep guidance | No sleep recommendations in recovery. | High fatigue sessions | Add sleep notes to L4/L5 protocols. |
| L4_contrast_therapy not credible | Uses cold immersion twice, no hot/cold alternation. | L4 recovery | Replace with realistic contrast protocol or remove. |

---

**Summary:** The recovery engine has 15 of 22 protocols, missing travel/tournament/post-match phases. The main issues are overly aggressive mappings for competition and conditioning, dead code, and missing sport/environment differentiation. The highest-value fixes are correcting protocol mappings and adding missing protocol categories.
