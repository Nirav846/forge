# FORGE Recovery Hardening V1

**Date:** 2026-06-20
**Auditor:** opencode (mimo-v2.5-free)
**Scope:** Minimal changes to recovery engine for coach credibility

---

## 1. Fixes Made

### A. Corrected overly aggressive protocol mappings

**Competition L2:** Changed from `L4_full_regeneration` (cold water immersion) to `L3_general_circuit_bike` (mobility circuit + bike). Competition at elevated fatigue now receives intermediate recovery instead of extreme recovery.

**Conditioning L3:** Changed from `L4_full_regeneration` to `L3_pool_walk_jog`. Conditioning at high fatigue now receives pool recovery instead of cold water immersion.

### B. Added deload session mapping

Added `"deload"` key to `SESSION_TYPE_RECOVERY_MAP`:
- L1: `L1_mobility_stretch`
- L2: `L1_mobility_stretch` (stays light)
- L3: `L2_general_circuit`

Updated `_map_session_type_to_recovery_key()` to map "deload" to "deload".

### C. Fixed duplicate drill in L5_cold_immersion

Changed from two `cold_water_immersion` drills to one `cold_water_immersion` + one `general_mobility_flow`. More credible and varied.

### D. Removed dead code (optional)

Left `FATIGUE_LEVEL_PROTOCOLS` dict as dead code (never used). Can be removed in future cleanup.

---

## 2. Files Changed

| File | Changes |
|------|---------|
| `src/forge/recovery_engine.py` | Updated SESSION_TYPE_RECOVERY_MAP (competition L2, conditioning L3, added deload), updated _map_session_type_to_recovery_key, fixed L5_cold_immersion duplicate |

---

## 3. Protocols Added/Retagged

| Protocol | Change |
|----------|--------|
| L3_general_circuit_bike | Now used for competition L2 (was L4_full_regeneration) |
| L3_pool_walk_jog | Now used for conditioning L3 (was L4_full_regeneration) |
| deload mapping | New session type mapping for deload sessions |
| L5_cold_immersion | Fixed duplicate drill |

No protocols were added or removed. Only mapping corrections.

---

## 4. Before/After Example Recovery Outputs

### Example 1: Competition, elevated fatigue

**Before:**
- Session type: competition, fatigue: elevated
- Protocol: L4: Full regeneration protocol (L4)
- Drills: Cold water immersion (12 min), Full body mobility recovery (15 min), Tempo spin (20 min)
- **Total:** 45 min

**After:**
- Session type: competition, fatigue: elevated
- Protocol: L3: General circuit + bike (L3)
- Drills: Foam roll quads (2 min), Foam roll glutes (2 min), Glute bridge (30s), Deep squat hold (1 min), World's greatest stretch (1.5 min), Cat-cow (1 min), Dead bug (1 min), Child's pose (1.5 min), Easy spin (20 min)
- **Total:** 30 min

**Improvement:** More appropriate for elevated fatigue. Cold water immersion is reserved for very high/extreme fatigue.

### Example 2: Conditioning, high fatigue

**Before:**
- Session type: conditioning, fatigue: high
- Protocol: L4: Full regeneration protocol (L4)
- Drills: Cold water immersion (12 min), Full body mobility recovery (15 min), Tempo spin (20 min)
- **Total:** 45 min

**After:**
- Session type: conditioning, fatigue: high
- Protocol: L3: Pool walk/jog (L3)
- Drills: Pool walk/jog (20 min)
- **Total:** 20 min

**Improvement:** Pool recovery is more appropriate for conditioning sessions. Cold water immersion may blunt adaptation.

### Example 3: Deload, normal fatigue

**Before:**
- (No deload mapping, fell back to strength lower L1)
- Protocol: L1: Mobility + stretch (L1)
- Drills: General mobility flow (10 min)
- **Total:** 10 min

**After:**
- Session type: deload, fatigue: normal
- Protocol: L1: Mobility + stretch (L1)
- Drills: General mobility flow (10 min)
- **Total:** 10 min (unchanged)

**Note:** Deload recovery is same as L1 mobility stretch, which is appropriate.

### Example 4: Strength, very high fatigue

**Before:**
- Session type: strength, fatigue: very_high
- Protocol: L4: Full regeneration protocol (L4)
- Drills: Cold water immersion (12 min), Full body mobility recovery (15 min), Tempo spin (20 min)
- **Total:** 45 min

**After:**
- (No change, mapping unchanged)
- Protocol: L4: Full regeneration protocol (L4)
- **Total:** 45 min

**Note:** Strength very high fatigue still uses L4, which is appropriate.

---

## 5. Impact Assessment

### Coach credibility improvement

- **Competition recovery:** Now uses appropriate intermediate recovery instead of jumping to cold water immersion. Coach would accept.
- **Conditioning recovery:** Now uses pool recovery instead of cold water immersion. Coach would accept.
- **Deload recovery:** Now has dedicated mapping. Coach would accept.
- **L5_cold_immersion:** Fixed duplicate drill. More credible.

### Remaining gaps (P2)

1. **No compression/elevation guidance** – Recovery protocols don't include practical compression/elevation instructions.
2. **No sport-specific recovery** – Overhead athletes need shoulder recovery protocols.
3. **No hydration/nutrition timing** – Recovery protocols don't specify nutrition timing.
4. **No post-match phased recovery** – Post-match 4-phase recovery (immediate/early/later/evening) not accessible.

---

**Conclusion:** Recovery engine hardening corrects the most egregious mapping errors (competition and conditioning over-prescribing cold water immersion) and adds deload support. The recovery prescriptions are now coach-acceptable for most scenarios.
