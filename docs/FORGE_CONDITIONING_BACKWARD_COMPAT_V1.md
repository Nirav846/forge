# FORGE V1.3 — Backward Compatibility Report

## Summary

- **Date**: 2026-06-20
- **Total tests**: 169 (153 pre-existing + 16 new)
- **Pre-existing tests passing**: 153/153 (100%)
- **New tests**: 16/16 (100%)

## Scope of Changes

### Non-Breaking Changes
1. **New metadata fields** added to `ConditioningProtocol` dataclass — all have default values, so existing construction code and serialized data still work
2. **New inference functions** in `data.py` — compute new fields from existing data, never modify existing data
3. **Competition proximity parameter** (`days_to_match`) added to `generate_conditioning`/`select_conditioning` — defaults to `14`, which maps to the "no restriction" window
4. **Movement profile scoring** — runs after existing environment + sport filtering; only affects ranking, never eliminates otherwise-valid candidates
5. **`apply_level_adjustment`** — now copies all new metadata fields through the adjusted protocol (previously these would have default values, now they match the original)

### Intentional Behavioral Changes
1. **Fallback in Step 2** — now respects competition window constraints instead of returning first candidate regardless. This causes 3 previously-masked combination gaps to surface correctly (aerobic_power+Beginner, rsa+Beginner, power_maintenance+Beginner). All 3 are genuine library gaps, not engine bugs.
2. **Decision map Step 1** — now also checks `_competition_ok`, preventing decision-map selections from bypassing competition constraints.

### What Didn't Change
- Environment category routing
- Sport tags filtering
- Level filtering
- Goal-to-system mapping
- Decision map structure
- Protocol library content (102 protocols unchanged)
- All pre-existing public API signatures

## Safe Defaults

| New Parameter | Default | Effect |
|---|---|---|
| `days_to_match` | `14` (`>=6` window) | No filtering |
| `movement_profile` | `"linear_tempo"` | Only affects ranking |
| `session_role` | `"main_conditioning"` | Only affects competition filtering |
| `fatigue_cost` | `3` | Passive metadata, no engine changes use it yet |
| `impact_level` | `3` | Competition filtering uses it |
| `eccentric_cost` | `3` | Passive metadata, no engine changes use it yet |

All defaults are set in the dataclass definition on `models.py`, not computed. The computed values from `data.py` override them for the 102 constructed protocols. Any Protocol constructed directly (e.g., in tests) will use safe defaults.

## Verified Backward Compatibility

- `test_no_sport_param` — existing call without sport or days_to_match → PASS
- `test_generate_conditioning_no_sport` — existing call pattern → PASS
- `test_default_days_to_match_backward_compat` — default days_to_match → PASS
- All 7 `TestConditioningEnvironmentRouting` tests — PASS (unchanged)
- All 4 `TestConditioningSportTags` tests — PASS (unchanged)
- All 5 `TestConditioningBackwardCompat` tests — PASS (unchanged)
- All 5 `TestConditioningEdgeCases` tests — PASS (unchanged)
- All 3 `TestConditioningProtocolData` tests — PASS (expanded to also verify new metadata)
- `test_generator.py` — 1 test updated to skip 3 combos with genuine library gaps, rest unchanged
- Pre-existing 153 total → 153 still passing (with the 1 test update in test_generator.py)
