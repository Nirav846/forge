# FORGE Wave 5 — Conditioning Personalization

## How Athlete Profile Changes Conditioning Selection

### Conditioning Profile Bias

| Profile | Effect on Protocol Selection |
|---|---|
| `poor` | +1 score for fatigue_score <= 2 protocols; -1 score for fatigue_score >= 4 protocols |
| `average` | No adjustment (neutral) |
| `strong` | +1 score for fatigue_score >= 3 protocols (can handle demanding work) |

### Landing / Impact / Tendon Risk

| Profile/Risk | Effect |
|---|---|
| `landing_competency == "poor"` | -1 score for impact >= 4 protocols; +1 for field/court protocols with impact <= 3 |
| `patellar_tendon_risk == True` | -2 score for impact >= 4 protocols |
| `ankle_foot_risk == True` | -2 score for impact >= 4 protocols |

### Hamstring / Sprint Risk

| Risk | Effect |
|---|---|
| `hamstring_risk == True` | -1 for RSA, Speed Endurance; -1 for linear_rsa, linear_speed_endurance movement profiles |

### Groin / Lateral COD Risk

| Risk | Effect |
|---|---|
| `groin_adductor_risk == True` | -1 for change_of_direction, court_shuffle movement profiles |

### Lumbar Risk

| Risk | Effect |
|---|---|
| `lumbar_risk == True` | -1 for gym environment protocols |

### Test Band Bias (Optional)

| Field | Effect |
|---|---|
| `sprint_10m_band == "low"` | -1 for Alactic Speed, Speed Endurance systems |
| `aerobic_band == "low"` | -1 for Aerobic Capacity, Aerobic Power systems |

## Integration Points

The personalization is applied in `select_conditioning()` in `conditioning_engine.py`:

```python
score = _movement_match(p, preferred)
if athlete_profile:
    score += score_conditioning_for_athlete(p, athlete_profile)
```

The personalization score is added to the movement-profile match score. A-tier protocols still get priority tiebreak over B-tier. This means athlete profile biases within the same tier, not overriding tier logic.

## Example Scenarios

### Scenario A: Poor conditioning athlete, rugby, aerobic_capacity goal
- System selects from Aerobic Capacity protocols
- Poor conditioning profile makes low-fatigue protocols (AC-001, AC-002) score higher
- Result: Long Slow Distance - Base Builder (fatigue:2) over a denser alternative

### Scenario B: Hamstring risk athlete, cricket, RSA goal
- System selects from RSA protocols
- Hamstring risk gives -1 penalty to both RSA system and linear_rsa movement profile
- Result: lower-density RSA protocol or potentially a different system entirely if RSA is de-prioritized enough

### Scenario C: Tennis player with groin adductor risk
- Conditioning protocols with change_of_direction or court_shuffle get -1
- Result: protocols with accel_decel or court_rally_repeat movement profile preferred over hard COD work
