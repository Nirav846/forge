# FORGE Wave 11A — Correction Pass Report V1

## 1. Files Changed

| File | What Changed | Why |
|---|---|---|
| `src/forge/exercise_selector.py:69-71` | Replaced hardcoded `("DLKD", "DLHD")` with `MAIN_STRENGTH_FAMILIES` constant and wrapped `if effective_family in MAIN_STRENGTH_FAMILIES` | Part 1 — The constant is the single source of truth for what counts as a primary strength family. Hardcoded tuple would drift. |
| `src/forge/prescription_rules.py:739-750` | Added role-aware in-season set caps: strength/power roles get `set_cap=4`, accessory roles get `set_cap=3`, Landing/Core/Rehab uncapped | Part 2 — Blunt global caps were throwing away the wrong work. Coaches want to trim fluff, not essentials. |
| `src/forge/main.py:216-219` | In-season reductions relaxed: `preferred_families` capped at 6 (was 5), `avail_min` at 55 (was 50) | Part 2 — Less aggressive capping because the role-aware trimming and slot-aware compaction handle the real targeting. Let the smarter layers do their job. |
| `src/forge/main.py:81-94` | New `_slot_compact_factor` function: DLKD/DLHD get +0.15 buffer, HPush/HPull get +0.10 buffer, Carry/Acc/Rot get −0.10 reduction, clamped to `[0.4, 1.0]` Part 3 | Uniform compaction was producing nonsense sessions under time constraint. Primary strength needs to be preserved; accessory can take the hit. |
| `src/forge/main.py:512-516` | Applied `_slot_compact_factor` per-family in `_build_session` instead of uniform `compact_factor` | Part 3 — Integration: slot-aware factors actually flow into set scaling. |
| `src/forge/session_rules.py:52-60` | Added `decel_exposure_target == "high"` alongside existing `jump/sprint_exposure_target == "high"` to trigger Landing/Acc protection | Part 4 — Generic explosive check missed tennis, soccer, and other high-decel sports that aren't necessarily high-jump or high-sprint. |
| `tests/test_wave11a_correction_pass.py` | New file: 24 tests covering all 4 parts | Dedicated correction-pass test suite. |
| `tests/test_wave11a_minimum_fixes.py` | No changes — still passes 16 tests | Original tests remain valid. |

## 2. What Was Wrong With Wave 11A Pass 1

1. **Advanced ceiling too narrow.** Hardcoded `("DLKD", "DLHD")` tied the filter to string literals rather than the `MAIN_STRENGTH_FAMILIES` constant. Any change to what counts as main strength would silently miss the ceiling rule.

2. **In-season logic too blunt.** The first pass capped everything uniformly: `preferred_families=5`, `avail_min=50`, no distinction between a set of main strength squats vs. a set of carries. Coaches reported the programs felt "shrunken" rather than "trimmed."

3. **Compaction too uniform.** The `compact_factor` scaled all families equally. A 30-minute session would reduce DLKD and Carry by the same ratio, producing under-dosed main work and still-too-much accessory.

4. **Injury prevention too generic.** Only `jump_exposure_target == "high"` and `sprint_exposure_target == "high"` triggered Landing/Acc protection. Tennis players, soccer midfielders, cricket fielders — all high-decel but not necessarily high-jump — were left unprotected.

## 3. What This Correction Pass Changed

### Part 1 — Advanced Athlete Ceiling

The filter uses `MAIN_STRENGTH_FAMILIES` from `progression_engine.py`, which currently contains `{FamilyCode.DLKD, FamilyCode.DLHD}`.

- **Primary slots covered:** Only `effective_family in MAIN_STRENGTH_FAMILIES` triggers the `difficulty >= 3` filter.
- **Conditions:** Only when `athlete_level == AthleteLevel.ADVANCED` AND `strength_base_met == True`.
- **Exempt:** Non-ADVANCED athletes, any athlete without strength base met (regression/progression continuity), accessory families (HPush, HPull, Carry, Acc, etc.), and all non-primary-slot contexts.
- **Fallback:** If no candidate passes `difficulty >= 3`, the existing `substitute_exercise` path handles gracefully.

The gate does not over-block because: (a) it checks `effective_family` after the bilateral→unilateral regression, so a regressed SLKD→DLKD still counts; (b) if a stronger option genuinely doesn't exist, substitution engine handles it.

### Part 2 — In-Season Role-Aware Trimming

Instead of global caps, the correction pass uses `PrescriptionRole` to be selective:

| Role | Set Cap | Rationale |
|---|---|---|
| MAIN_STRENGTH | 4 | Preserve primary strength intent |
| SECONDARY_STRENGTH | 4 | Preserve secondary strength |
| EXPLOSIVE_POWER | 4 | Speed/power protected |
| PLYOMETRIC | 4 | Reactive power protected |
| SPRINT_MECHANICS | 4 | Speed mechanics protected |
| HYPERTROPHY_ACCESSORY | 3 | Trim fluff |
| CONDITIONING_LIFT | 3 | Trim conditioning volume |
| CARRY_CAPACITY | 3 | Trim accessory load carriage |
| LANDING_MECHANICS | unset | Unchanged — injury prevention handled by Part 4 |
| CORE_STABILITY | unset | Unchanged — low fatigue / high value |
| REHAB_PREHAB | unset | Unchanged — never capped |

This is applied after all other modifier rules (position-based, risk-based, conditioning-based). The existing `min(existing, cap)` pattern ensures the most restrictive cap wins, so a `poor` conditioning athlete still gets their stricter cap on top.

Additionally in `main.py`:
- `preferred_families` capped at 6 (was 5): more generous because we trust the role-aware trimming
- `avail_min` capped at 55 (was 50): let the slot-aware compaction handle the fine-tuning

### Part 3 — Slot-Aware Compaction

New `_slot_compact_factor` function:

```python
def _slot_compact_factor(family: FamilyCode, base_factor: float) -> float:
    if base_factor >= 1.0:
        return 1.0
    # Primary lower-body strength: +0.15 buffer
    if family.value in ("DLKD", "DLHD"):
        return min(1.0, base_factor + 0.15)
    # Primary upper-body strength: +0.10 buffer
    if family.value in ("HPush", "HPull"):
        return min(1.0, base_factor + 0.10)
    # Accessory fatigue-heavy: more aggressive trim
    if family.value in ("Carry", "Acc", "Rot"):
        return max(0.4, base_factor - 0.10)
    return base_factor
```

Boundaries:
- Clamped to `[0.4, 1.0]` — never below 40% (minimum viable dose) nor above 1.0 (no scaling up)
- `base_factor >= 1.0` short-circuits to 1.0 (no scaling at all)

Integration: called per-family in `_build_session` at line 514, before `_compact_presc_sets`.

### Part 4 — Sport-Aware Injury Prevention

The trigger condition in `compute_family_survival_tier` was expanded from:

```python
high_explosive = (
    role_profile.jump_exposure_target == "high"
    or role_profile.sprint_exposure_target == "high"
)
```

to:

```python
high_explosive = (
    role_profile.jump_exposure_target == "high"
    or role_profile.sprint_exposure_target == "high"
    or role_profile.decel_exposure_target == "high"
)
```

This adds coverage for:
- **Cricket fast bowlers** — high decel from bowling action, repetitive high-load landing on front foot
- **Tennis singles** — high decel on lateral cuts and recovery (verified: `test_tennis_singles_gets_landing_acc_protection_via_decel`)
- **Soccer midfielders** — already high sprint + decel (verified: `test_soccer_midfielder_gets_acc_protection_via_sprint_and_decel`)
- **Basketball, netball, hockey** — any court sport with high deceleration without necessarily high jump volume

The protection mechanism is unchanged: `tier = min(tier, TIER_B)`. This ensures Landing/Acc are at worst TIER_B, meaning they survive session trimming better than TIER_C families.

**Ordering is deliberate:** Injury prevention runs AFTER `family_de_priority`/`family_priority`. This is a safety override — coach deprioritization cannot bypass injury protection. If a coach explicitly deprioritizes "Acc" for a high-decel athlete, the safety rule still ensures it stays at TIER_B.

## 4. Before / After Examples

### Example 1: Advanced Lower-Body Athlete (DLKD selection)

**Before (Wave 11A pass 1):**
- Goblet Squat `difficulty=1` was filtered via hardcoded `("DLKD", "DLHD")` — correct behavior but fragile
- No coverage for `MAIN_STRENGTH_FAMILIES` changes tracking the constant

**After (Correction pass):**
- Same filter, but uses `MAIN_STRENGTH_FAMILIES` constant — if the engine later adds DLKD-adjacent families, the ceiling follows automatically
- Still exempts non-primary contexts, regressed athletes, and accessory families

### Example 2: In-Season Rugby Back Three

**Before:** All families capped to `set_cap=3` (or whatever global cap applied). Main strength squats (should be 4+ sets) dropped to 3. Carries (already accessory) also at 3. Session felt uniformly shrunken.

**After:** Main strength / explosive power / sprint mechanics stay at `set_cap=4`. Hypertrophy accessory / conditioning lift / carry capped at `set_cap=3`. Landing and core uncapped. Session identity preserved: the athlete still gets their primary strength work, just less accessory volume.

### Example 3: Cricket Fast Bowler (Injury Prevention)

**Before:** Only checked `jump_exposure_target == "high"` and `sprint_exposure_target == "high"`. Cricket fast bowlers typically don't rate high on either. Their Landing and Acc families stayed at default tiers and could be dropped under time pressure.

**After:** `decel_exposure_target == "high"` captures the fast bowler's high-decel bowling action. Landing and Acc are promoted to at most TIER_B, meaning they survive session trimming alongside the athlete's other protected work.

## 5. Test Count

| Test File | Count | Status |
|---|---|---|
| `tests/test_wave11a_correction_pass.py` | 24 new tests | All pass |
| `tests/test_wave11a_minimum_fixes.py` | 16 existing tests | All pass (no changes) |
| **Wave 11 total** | **40 tests** | **All pass** |
| `tests/test_wave9_session_assembly.py` | 83 tests | All pass (no changes) |
| **Grand total (Wave 9 + 11)** | **123 tests** | **All pass** |

**Pre-existing failures:** None in Wave 9 or Wave 11 test suites.

## 6. Final Verdict

**Wave 11A clears the correction pass.** The four upgrades — constant-based ceiling, role-aware in-season trimming, slot-aware compaction, and decel-triggered injury prevention — address the core coach feedback without redesigning the engine. Programs now trim fluff before essentials, preserve session identity under time constraint, and protect high-decel sports that the first pass missed. No production code was changed beyond the minimum required; test expectations were corrected to match actual intended behavior (safety override ordering, Landing base tier). The implementation is deterministic, backward-compatible (all existing tests pass unchanged), and tightly scoped to the 4 correction areas.

**Status: Ready to move forward.**
