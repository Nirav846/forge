# FORGE Role Week Profile Rulebook V1.0

## Overview

`RoleWeekProfile` defines how a sport role should be planned across a week, independent of specific exercises or prescriptions. It is a **deterministic, coach-readable structure** that biases week architecture without destroying blueprint identity.

## Structure

```python
@dataclass(frozen=True)
class RoleWeekProfile:
    force_emphasis: float           # 0.0–1.0
    velocity_emphasis: float        # 0.0–1.0
    conditioning_emphasis: float    # 0.0–1.0
    rotation_emphasis: float          # 0.0–1.0
    landing_emphasis: float         # 0.0–1.0
    upper_body_emphasis: float      # 0.0–1.0
    eccentric_tolerance: str        # "high" | "moderate" | "low"
    collision_tolerance: str          # "high" | "moderate" | "low"
    sprint_exposure_target: str     # "high" | "moderate" | "low"
    jump_exposure_target: str       # "high" | "moderate" | "low"
    decel_exposure_target: str      # "high" | "moderate" | "low"
    rotation_exposure_target: str  # "high" | "moderate" | "low"
    conditioning_density_bias: str  # "high" | "moderate" | "low"
    family_priority: list[str]     # Family codes to prioritize
    family_de_priority: list[str]  # Family codes to de-prioritize
```

## Role Profiles

### Rugby

| Role | Force | Velocity | Conditioning | Rotation | Landing | Sprint | Collision | Notes |
|------|-------|----------|--------------|----------|---------|--------|-----------|-------|
| prop | 0.9 | 0.2 | 0.4 | 0.3 | 0.3 | low | high | Maximal force + collision; sprint moderated |
| hooker | 0.8 | 0.3 | 0.5 | 0.4 | 0.4 | low | high | Scrummaging + repeat work |
| lock | 0.8 | 0.3 | 0.5 | 0.4 | 0.6 | low | high | Jump-landing (lineout) + force |
| back_row | 0.6 | 0.5 | 0.7 | 0.4 | 0.5 | moderate | high | Hybrid force + repeat running |
| scrum_half | 0.4 | 0.7 | 0.6 | 0.5 | 0.3 | high | low | Speed + agility |
| fly_half | 0.4 | 0.6 | 0.6 | 0.6 | 0.3 | moderate | low | Rotational + distribution |
| centre | 0.5 | 0.6 | 0.6 | 0.5 | 0.4 | moderate | high | Collision + acceleration |
| back_three | 0.3 | 0.8 | 0.5 | 0.4 | 0.4 | high | low | Max velocity + elastic |

### Cricket

| Role | Force | Velocity | Conditioning | Rotation | Landing | Sprint | Eccentric | Notes |
|------|-------|----------|--------------|----------|---------|--------|-----------|-------|
| fast_bowler | 0.5 | 0.6 | 0.5 | 0.5 | 0.6 | high | high | Sprint + landing + rotation managed; DLHD/Rot/VPush de-prioritized |
| spin_bowler | 0.4 | 0.4 | 0.4 | 0.8 | 0.2 | low | low | Rotational control + repeatability |
| batter | 0.5 | 0.6 | 0.5 | 0.7 | 0.3 | moderate | moderate | Rotational power + acceleration |
| wicketkeeper | 0.5 | 0.4 | 0.4 | 0.5 | 0.5 | low | moderate | Low squat stance + lateral coverage |
| all_rounder | 0.5 | 0.5 | 0.6 | 0.5 | 0.5 | moderate | moderate | Balanced across all demands |

### Tennis

| Role | Force | Velocity | Conditioning | Rotation | Landing | Sprint | Conditioning Density | Notes |
|------|-------|----------|--------------|----------|---------|--------|---------------------|-------|
| singles | 0.4 | 0.6 | 0.7 | 0.6 | 0.5 | moderate | high | Repeat court conditioning + COD |
| doubles | 0.4 | 0.6 | 0.5 | 0.5 | 0.4 | low | moderate | Explosive first-step + serve-volley |

### Badminton

| Role | Force | Velocity | Conditioning | Landing | Sprint | Conditioning Density | Notes |
|------|-------|----------|--------------|---------|--------|---------------------|-------|
| singles | 0.4 | 0.7 | 0.7 | 0.5 | high | high | Repeat lunge + court coverage |
| doubles | 0.4 | 0.6 | 0.5 | 0.4 | low | moderate | Explosive short-burst + jump-smash |

### Volleyball

| Role | Force | Velocity | Conditioning | Landing | Jump | Rotation | Notes |
|------|-------|----------|--------------|---------|------|----------|-------|
| middle_blocker | 0.6 | 0.6 | 0.5 | 0.9 | high | low | Block-jump + landing emphasis |
| outside_hitter | 0.5 | 0.6 | 0.5 | 0.7 | high | moderate | Approach jump + shoulder management |
| opposite | 0.6 | 0.5 | 0.5 | 0.6 | high | high | Attack + rotational loading |
| setter | 0.4 | 0.5 | 0.5 | 0.3 | low | moderate | Footwork + overhead tolerance |
| libero | 0.3 | 0.5 | 0.6 | 0.4 | low | low | Lateral coverage + repeat movement |

### Soccer / Football

| Role | Force | Velocity | Conditioning | Landing | Sprint | Decel | Notes |
|------|-------|----------|--------------|---------|--------|-------|-------|
| goalkeeper | 0.5 | 0.5 | 0.4 | 0.7 | low | low | Lateral dive + explosive push |
| centre_back | 0.7 | 0.5 | 0.6 | 0.4 | moderate | moderate | Duel robustness + aerial |
| fullback | 0.5 | 0.7 | 0.7 | 0.4 | high | high | Acceleration + repeat running |
| midfielder | 0.5 | 0.6 | 0.8 | 0.4 | high | high | Conditioning density + repeat running |
| winger | 0.3 | 0.8 | 0.6 | 0.4 | high | high | Max acceleration + first-step |
| striker | 0.5 | 0.7 | 0.6 | 0.5 | high | high | Finishing power + acceleration |

### Basketball

| Role | Force | Velocity | Conditioning | Landing | Sprint | Notes |
|------|-------|----------|--------------|---------|--------|-------|
| guard | 0.3 | 0.8 | 0.7 | 0.5 | high | COD + ball-handling |
| wing | 0.5 | 0.7 | 0.6 | 0.6 | high | Transition + defensive slide |
| big | 0.8 | 0.4 | 0.5 | 0.7 | low | Post strength + rebounding jump |

## Fallback Rules

1. **Unknown role** → sport-level default
2. **Unknown sport** → neutral profile (all 0.5, all targets "moderate")
3. **No role provided** → sport-level default
4. **No sport provided** → neutral profile

## Integration Notes

- Role does **not** override blueprint identity. A "Sprint Development" blueprint still looks like Sprint Development.
- Role **biases** which optional families are prioritized, which exposure caps are applied, and how conditioning is distributed.
- Role profiles are **static** (not yet adjusted for season phase or goal).
