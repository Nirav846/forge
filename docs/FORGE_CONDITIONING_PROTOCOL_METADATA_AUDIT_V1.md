# FORGE V1.3 — Conditioning Protocol Metadata Audit

## Summary

- **Date**: 2026-06-20
- **Scope**: 102 conditioning protocols
- **Fields audited**: movement_profile, session_role, fatigue_cost, impact_level, eccentric_cost
- **Inference method**: Programmatic computation in `data.py` at object construction time
- **Fallback**: All fields inferable from existing protocol data (id, system, environment, fatigue_score, tier, name)

## Field Definitions

| Field | Values | Purpose |
|---|---|---|
| `movement_profile` | 15 values (linear_tempo, court_shuffle, ...) | Describes primary movement pattern |
| `session_role` | 5 values (main_conditioning, top_up_conditioning, speed_support, power_maintenance, recovery_flush) | Describes role of protocol within a session/week |
| `fatigue_cost` | 1–5 (maps 1:1 from fatigue_score) | General fatigue contribution |
| `impact_level` | 1–5 | Joint/impact stress level |
| `eccentric_cost` | 1–5 | Eccentric loading / muscle damage potential |

## Protocol Construction

All 5 fields are set in the `for pd in _COND_RAW:` loop in `data.py`. Each has a corresponding `_compute_*` function that:

1. Checks for explicit value in protocol dict → if present, uses it
2. Falls back to inference from existing fields (id pattern, system, environment, fatigue_score, tier, name)

No protocol dicts were modified — all 102 protocols receive their metadata via inference.

## Coverage

All 102 protocols carry valid values for all 5 fields.

### Movement Profile Distribution

| Profile | Count |
|---|---|
| linear_tempo | 43 |
| accel_decel | 19 |
| linear_speed_endurance | 9 |
| linear_rsa | 7 |
| change_of_direction | 3 |
| court_shuffle | 3 |
| mobility_recovery | 3 |
| recovery_flush | 3 |
| bike_intervals | 2 |
| court_rally_repeat | 2 |
| gym_mixed_modal | 2 |
| pool_recovery | 2 |
| treadmill_intervals | 2 |
| court_diagonal | 1 |
| rower_intervals | 1 |

### Session Role Distribution

| Role | Count |
|---|---|
| main_conditioning | 60 |
| speed_support | 17 |
| top_up_conditioning | 10 |
| recovery_flush | 8 |
| power_maintenance | 7 |

### Fatigue Cost Distribution

| Cost | Count |
|---|---|
| 1 | 9 |
| 2 | 10 |
| 3 | 27 |
| 4 | 34 |
| 5 | 22 |

### Impact Level Distribution

| Level | Count |
|---|---|
| 1 | 10 |
| 2 | 3 |
| 3 | 26 |
| 4 | 63 |
| 5 | 0 |

Note: No protocol currently has impact_level=5. This is reserved for future high-impact protocols (e.g., max velocity sprinting on hard surfaces, depth jumps conditioning).

### Eccentric Cost Distribution

| Cost | Count |
|---|---|
| 1 | 10 |
| 2 | 6 |
| 3 | 80 |
| 4 | 6 |
| 5 | 0 |

Note: No protocol currently has eccentric_cost=5. This is reserved for future high-eccentric protocols (e.g., heavy eccentric loading conditioning, high-volume drop jumps).

## Inference Rules Documented

Each `_compute_*` function in `data.py` follows a structured decision tree:

1. **movement_profile**: Check explicit dict → recovery env → gym env → court env (id pattern match) → field env (id prefix match) → default linear_tempo
2. **session_role**: Check explicit → Recovery Conditioning → Power Maintenance → Alactic/Speed Endurance (speed_support) → fatigue_score ≤ 2 (top_up) → ≥ 5 (main) → default main_conditioning
3. **fatigue_cost**: Direct 1:1 map from existing fatigue_score
4. **impact_level**: Check explicit → recovery(1) → gym(bike=1, rower=2, treadmill=3, default=2) → court(shuffle=3, default=4) → field(alactic/speed endurance/rsa=4, fatigue≥4=4, aerobic/extensive=3, default=3)
5. **eccentric_cost**: Check explicit → recovery(1) → gym(bike=1, rower=2, default=2) → court(shuffle/diagonal/rally=4, accel_decel/cod=3) → field(speed_endurance/rsa=3, linear_tempo=3, default=3)

## Verification

- `test_all_protocols_have_movement_profile` — passes (37/37)
- `test_all_protocols_have_session_role` — passes
- `test_all_protocols_have_fatigue_cost_in_range` — passes
- `test_all_protocols_have_impact_level_in_range` — passes
- `test_all_protocols_have_eccentric_cost_in_range` — passes
