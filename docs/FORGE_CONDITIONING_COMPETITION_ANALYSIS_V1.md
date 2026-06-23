# FORGE V1.3 — Competition Proximity Analysis

## Summary

- **Date**: 2026-06-20
- **Feature**: `days_to_match` parameter filters and ranks conditioning protocols based on proximity to competition
- **Integration point**: `select_conditioning()` — both Step 1 (decision map) and Step 2 (system fallback)
- **Backward compatibility**: default `days_to_match=14` (effectively unrestricted)

## Competition Windows

| Window | days_to_match | Allowed Session Roles | Max Impact | Rationale |
|---|---|---|---|---|
| None | — | All (no restriction) | 5 | No upcoming competition |
| Far | ≥6 | All (no restriction) | 5 | Normal training phase |
| Medium | 4–5 | main_conditioning, top_up_conditioning, power_maintenance | 4 | Pre-competition — limit impactful work |
| Close | 2–3 | main_conditioning, top_up_conditioning, power_maintenance | 3 | Competition taper — low impact only |
| Match | ≤1 | power_maintenance, recovery_flush | 2 | Day before / match day — very light |

## Implementation Details

### `_resolve_comp_window(days_to_match)`
- `None` → `None` (no restriction)
- `>=6` → `6` (far out)
- `>=4` → `4` (medium)
- `>=2` → `2` (close)
- `<2` → `1` (match)

### `_competition_ok(proto, window)`
Two checks:
1. If window has role restrictions → `proto.session_role` must be in allowed set
2. If window has impact cap → `proto.impact_level` must be ≤ max

Both must pass for a protocol to be selectable.

### Integration Points
- **Decision map path (Step 1)**: After `_level_ok`, checks `_competition_ok` — prevents direct decision map from bypassing competition logic
- **System fallback (Step 2)**: Filter applied in scoring loop, plus in the final fallback iteration
- **Edge case**: If no protocol passes both filters, returns `None` (previously would return first candidate regardless)

## Test Results

| Test | Scenario | Expected | Result |
|---|---|---|---|
| test_days_to_match_1_limits_impact | recovery, field, Beginner, d=1 | impact ≤ 2 | PASS |
| test_days_to_match_1_prefers_recovery_role | recovery, field, Beginner, d=1 | recovery_flush/power_maintenance | PASS |
| test_days_to_match_1_blocks_high_impact_systems | alactic_speed, d=1 | None | PASS |
| test_days_to_match_2_3_limits_impact | aerobic_power, d=2/3 | impact ≤ 3 | PASS |
| test_days_to_match_6_allows_high_impact | rsa, d=6 | normal session_roles | PASS |
| test_days_to_match_none_no_restriction | rsa, d=None | returns protocol | PASS |
| test_default_days_to_match_backward_compat | default param | returns protocol | PASS |

## Behavioral Changes

1. **Old behavior**: `select_conditioning` ignored competition proximity entirely. The decision map and system fallback would return the first matching protocol regardless of competition window.
2. **New behavior**: Both code paths filter by role/impact constraints. Protocols inappropriate for the competition window are excluded.
3. **Edge case**: Previously, calling `select_conditioning` for `alactic_speed` on `days_to_match=1` would return a high-impact sprint protocol. Now correctly returns `None`.
4. **Regressions**: 3 old test combinations (aerobic_power+Beginner, rsa+Beginner, power_maintenance+Beginner) now return `None` because no library protocol supports those combos. This is correct — the old fallback was masking the gap.
