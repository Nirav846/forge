# FORGE Role Exposure Rules V1.0

## Weekly Target / Cap Logic by Role

This document defines how `RoleWeekProfile` translates into numeric weekly exposure caps and how those caps are enforced during program generation and validation.

## Base Limits (No Role)

When no role is specified, the generic caps apply:

| Exposure | Cap |
|----------|-----|
| Sprint | 4 |
| Jump / Landing | 3 |
| Deceleration | 3 |
| Rotation | 4 |
| High-Eccentric | 3 |

## Role-Aware Caps

### Sprint Caps

| Target | Sprint Max | Decel Max |
|--------|-----------|-----------|
| high | 5 | 4 |
| moderate | 4 | 3 |
| low | 2 | 2 |

### Jump / Landing Caps

| Target | Jump Max | Landing Max |
|--------|----------|--------------|
| high | 5 | 4 |
| moderate | 4 | 3 |
| low | 2 | 2 |

### Rotation Caps

| Target | Rotation Max |
|--------|--------------|
| high | 5 |
| moderate | 4 |
| low | 2 |

### High-Eccentric Caps

| Tolerance | High-Eccentric Max |
|-----------|-------------------|
| high | 4 |
| moderate | 3 |
| low | 2 |

## Role Examples

### Rugby Prop
- sprint_target = low → sprint_max = 2, decel_max = 2
- jump_target = low → jump_max = 2, landing_max = 2
- rotation_target = low → rotation_max = 2
- eccentric_tolerance = high → high_eccentric_max = 4

### Rugby Backline (back_three)
- sprint_target = high → sprint_max = 5, decel_max = 4
- jump_target = moderate → jump_max = 4, landing_max = 3
- rotation_target = low → rotation_max = 2
- eccentric_tolerance = moderate → high_eccentric_max = 3

### Cricket Fast Bowler
- sprint_target = high → sprint_max = 5, decel_max = 4
- jump_target = high → jump_max = 5, landing_max = 4
- rotation_target = moderate → rotation_max = 3
- eccentric_tolerance = high → high_eccentric_max = 4

### Cricket Batter
- sprint_target = moderate → sprint_max = 4, decel_max = 3
- jump_target = low → jump_max = 2, landing_max = 2
- rotation_target = high → rotation_max = 5
- eccentric_tolerance = moderate → high_eccentric_max = 3

### Tennis Singles
- sprint_target = moderate → sprint_max = 4, decel_max = 3
- jump_target = moderate → jump_max = 4, landing_max = 3
- rotation_target = high → rotation_max = 5
- conditioning_density = high → more conditioning sessions per week

### Tennis Doubles
- sprint_target = low → sprint_max = 2, decel_max = 2
- jump_target = moderate → jump_max = 4, landing_max = 3
- rotation_target = moderate → rotation_max = 4
- conditioning_density = moderate → baseline conditioning frequency

### Volleyball Middle Blocker
- sprint_target = low → sprint_max = 2, decel_max = 2
- jump_target = high → jump_max = 5, landing_max = 4
- rotation_target = low → rotation_max = 2
- eccentric_tolerance = high → high_eccentric_max = 4

### Volleyball Libero
- sprint_target = moderate → sprint_max = 4, decel_max = 3
- jump_target = low → jump_max = 2, landing_max = 2
- rotation_target = low → rotation_max = 2
- conditioning_density = high → more conditioning sessions

## Enforcement

### During Generation

1. `apply_role_slot_bias()` reorders slots so preferred families appear early and de-prioritized families appear late (dropped first under time constraints).
2. `should_add_conditioning_for_role()` adjusts conditioning frequency based on `conditioning_density_bias`.
3. `review_week()` uses role-aware caps when computing risk flags for next-week adjustments.

### During Validation

1. `weekly_exposure_warnings()` uses role-aware caps instead of hard constants.
2. `_check_role_exposure_balance()` checks that no week exceeds role-specific caps.
3. `_check_role_conditioning_alignment()` checks that conditioning density matches role expectations.
4. `_check_role_week_bias_applied()` checks that preferred families are actually present in the program.

## Important Constraint

Role caps are **not medical limits**. They are coaching credibility filters. A prop getting 3 sprint exposures in a week is not an injury risk — it is a coaching logic error ("why is a prop getting backline-level sprint volume?"). The system flags it so the coach can review.

## Backward Compatibility

If no role is provided, all caps fall back to the generic defaults. Existing programs without Wave 8 fields continue to generate identically.
