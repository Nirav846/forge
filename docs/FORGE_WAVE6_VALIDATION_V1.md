# FORGE Wave 6 — Validation

## New Validator Checks

### `prescription_athlete_aware`

**Purpose**: Ensure force-deficient athletes don't get velocity-biased strength prescriptions (high reps on main lifts).

**Logic**:
```python
if athlete.force_profile == "force_deficient":
    for ex in main_strength_exercises:
        if max_rep_in_prescription > 12:
            return False
return True
```

**Failure example**: Force-deficient athlete gets `reps: "8-12"` on MAIN_STRENGTH → FAIL

### `role_bias_applied`

**Purpose**: Minimal check that role was considered (placeholder for future expansion).

**Logic**: Returns True if `position_role` is set (role bias is applied via personalization notes).

## Validation Examples

### Same Blueprint, Different Profiles → Different Prescriptions

| Athlete | Blueprint | MAIN_STRENGTH Reps | Intensity Note |
|---|---|---|---|
| Force-deficient | Strength | `5-7` | `RPE 7-9, heavy bias` |
| Velocity-deficient | Strength | `6-8` | `RPE 7-9, velocity-friendly` |
| Balanced | Strength | `6-8` | `RPE 7-9` |

### Same Blueprint, Different Roles → Different Prescriptions

| Athlete | Blueprint | PLYOMETRIC Note | SPRINT_MECHANICS Note |
|---|---|---|---|
| Prop (rugby) | Strength | `set_cap: 3` | — |
| Backline (rugby) | Strength | `reactive emphasis` | `max velocity` |
| Singles (tennis) | Court Sport | — | `set_cap: 3, court conditioning density` |
| Doubles (tennis) | Court Sport | — | `first-step emphasis` |

### Role + Profile Stacking

| Athlete | MAIN_STRENGTH Reps | Note |
|---|---|---|
| Force-deficient prop | `5-7` | `RPE 7-9, heavy bias, maximal force emphasis` |
| Force-deficient backline | `5-7` | `RPE 7-9, heavy bias` |
| Velocity-deficient prop | `6-8` | `RPE 7-9, velocity-friendly, maximal force emphasis` |

### Competition Window Still Wins

Even with athlete/role personalization, competition taper rules override:
- `days_to_match <= 3` → comp window modifiers still reduce sets/intensity
- Force-deficient prop with `days_to_match=2` still gets `set_factor: 0.7` and `submaximal`

## What Validator Catches

| Scenario | Validator Check | Result |
|---|---|---|
| Force-deficient gets `8-12` on squat | `prescription_athlete_aware` | FAIL |
| No role notes when role provided | `role_bias_applied` | FAIL (if implemented) |
| Patellar risk gets aggressive plyo | Not caught (exercise filtered in Wave 5) | PASS |
| Hamstring risk gets max-v sprint | Not caught (exercise filtered in Wave 5) | PASS |

## What Validator Does NOT Police

- Philosophical disagreements on optimal dosing
- Minor rep range differences (e.g., `5-7` vs `6-8`)
- Exact note wording matching
- Whether a specific role bias is "optimal"

The validator only catches **clear failures** where the personalization logic should have triggered but didn't.
