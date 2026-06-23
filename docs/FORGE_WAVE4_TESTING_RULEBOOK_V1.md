# FORGE Wave 4 — Testing / Benchmarking Rulebook

## Testing Categories

FORGE defines 6 internal testing categories:

| Category ID             | Label                          | Blocked For                              | Max Exercises |
|-------------------------|--------------------------------|------------------------------------------|--------------|
| `lower_body_strength`   | Lower Body Strength Test       | beginner, youth, return_to_play          | 2            |
| `upper_body_strength`   | Upper Body Strength Test       | beginner, youth, return_to_play          | 2            |
| `jump_power`            | Jump / Power Test              | (none)                                   | 2            |
| `sprint_speed`          | Sprint / Speed Test            | return_to_play                           | 2            |
| `conditioning_benchmark`| Conditioning Benchmark         | return_to_play                           | 1            |
| `movement_technical`    | Movement / Technical Benchmark | (none)                                   | 3            |

## Where Testing is Allowed

### Week 1 — Baseline
- **All athletes**: `movement_technical` baseline
- **Non-RTP**: `jump_power` added

### Week 5-6 — Mid-Block Checkpoint (realization weeks)
- **Non-RTP, non-deload**: `jump_power` + `sprint_speed` checkpoint

### Week 8 — Exit Testing (test week)
- **Advanced/Intermediate**: Full battery — lower/upper strength, jump, sprint, conditioning
- **Beginner/Youth**: Battery minus maximal strength tests; `movement_technical` included
- **Return-to-play**: Battery minus strength, sprint, conditioning; `movement_technical` included

## Where Testing is Blocked

| Condition                         | Blocked Categories                           |
|-----------------------------------|----------------------------------------------|
| Beginner or Youth (age < 16)      | `lower_body_strength`, `upper_body_strength` |
| Return-to-play                    | All strength, sprint, conditioning           |
| Competition proximity (≤2 days)   | All testing                                 |
| Deload blueprint (BP13)           | All testing (no exit test)                  |

## How Testing Affects Sessions

Testing sessions are marked with `testing_categories` on the `Session` dataclass. The `render_coach_session()` and `render_session()` functions display `[TEST]` markers with category labels.

Testing does **not** generate actual test protocols. It marks sessions for awareness and reduces training stress implicitly through volume reduction (fewer slot families as the block progresses).

## Future Scope

Actual test protocol generation (e.g., "3RM Back Squat" or "CMJ x 3 trials") would be a natural extension but is not part of Wave 4.
