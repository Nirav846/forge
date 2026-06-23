# FORGE V1.3 — Movement-Profile Routing Audit

## Summary

- **Date**: 2026-06-20
- **Feature**: Protocols are now ranked by movement_profile match to sport-specific preferences
- **Integration**: After environment_category + sport_tags filtering, remaining candidates are scored by movement_profile match
- **No breaking change**: All existing filtering still runs first; movement profile is a ranking tiebreaker, not a hard filter

## Movement Profiles Defined (15 total)

### Field Profiles
| Profile | Description | Typical Protocols |
|---|---|---|
| `linear_tempo` | Steady-state straight-line running | AC, ET, IT protocols |
| `linear_speed_endurance` | Max-speed straight-line with incomplete recovery | SE protocols |
| `linear_rsa` | Repeated short sprints with incomplete recovery | RSA (field) protocols |
| `accel_decel` | Acceleration/deceleration focus | AS, FC protocols |
| `change_of_direction` | COD + acceleration/deceleration | AP-006/007/008 |

### Court Profiles
| Profile | Description | Typical Protocols |
|---|---|---|
| `court_shuffle` | Lateral/court-specific movement patterns | CC-003, CC protocols |
| `court_rally_repeat` | Repeated point-play simulation | CC-001, CC-002 |
| `court_diagonal` | Diagonal court coverage patterns | CC-004 |
| `accel_decel` | Court-specific acceleration/deceleration | Court RSA protocols |
| `change_of_direction` | COD work on court | Select AP protocols |

### Gym Profiles
| Profile | Description | Typical Protocols |
|---|---|---|
| `mixed_modal_circuit` | Multi-station circuit (KB/DB/bodyweight) | GC protocol |
| `bike_intervals` | Stationary bike interval work | Bike protocol |
| `rower_intervals` | Rower interval work | Rower protocol |
| `treadmill_intervals` | Treadmill interval work | Treadmill protocol |

### Recovery Profiles
| Profile | Description | Typical Protocols |
|---|---|---|
| `recovery_flush` | General active recovery | RC protocols |
| `pool_recovery` | Pool-based recovery | Pool protocols |
| `mobility_recovery` | Mobility/stretch recovery | Select RC protocols |

## Sport-to-Movement-Profile Mapping

| Sport | Preferred Profiles (priority order) |
|---|---|
| `cricket` | linear_tempo, accel_decel, linear_speed_endurance, linear_rsa |
| `rugby` | linear_tempo, accel_decel, linear_speed_endurance, linear_rsa |
| `soccer` | linear_tempo, accel_decel, linear_speed_endurance, linear_rsa |
| `hockey` | linear_tempo, change_of_direction, accel_decel, linear_speed_endurance |
| `tennis` | court_shuffle, change_of_direction, accel_decel, court_diagonal, court_rally_repeat |
| `badminton` | court_shuffle, change_of_direction, court_diagonal, accel_decel |
| `basketball` | court_shuffle, change_of_direction, accel_decel |
| `volleyball` | court_shuffle, change_of_direction |
| `squash` | court_shuffle, court_rally_repeat, change_of_direction |
| `track` | linear_tempo, linear_speed_endurance, linear_rsa |

## Scoring

- `score = 2` if `proto.movement_profile in preferred_profiles[sport]`
- `score = 0` otherwise
- Primary sort: score descending, Secondary sort: tier (A before B)

This means a preferred-movement-profile B-tier protocol will be selected over a non-preferred A-tier protocol. If no candidate matches the preferred profile, the highest-tier protocol wins (unchanged from before).

## Test Results

| Test | Scenario | Expected | Result |
|---|---|---|---|
| test_court_tennis_prefers_court_profile | tennis, aerobic_power, court | court_shuffle/rally_repeat/diagonal/accel_decel/cod | PASS |
| test_field_soccer_prefers_linear_profile | soccer, aerobic_capacity, field | linear_tempo/accel_decel/speed_endurance/rsa | PASS |
| test_gym_gets_mixed_modal_profile | gym, aerobic_power | gym movement profile | PASS |
| test_unknown_sport_defaults_to_any | esports, aerobic_capacity, field | returns protocol | PASS |

## Interaction with Competition Proximity

Movement-profile scoring happens *after* competition proximity filtering. This means:
- A close-to-competition athlete (`days_to_match ≤ 3`) will first have high-impact/speed-support protocols removed
- The remaining low-impact candidates are then scored by movement profile match
- This prevents an otherwise well-matched protocol from being selected if it's inappropriate for the competition window

## Interaction with Environment Category

Environment category filtering runs before movement profile scoring. Protocols must have the correct `environment_category` to be candidates. The movement profile only determines ordering among environment-matching protocols.
