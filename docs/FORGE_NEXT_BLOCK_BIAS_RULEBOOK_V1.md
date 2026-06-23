# FORGE Next Block Bias Rulebook V1.0

## Overview
This document details the deterministic rules used to bias the next block's blueprint emphasis based on the prior block's response and athlete profile.

## Rule Sources
The bias logic is implemented in `src/forge/block_autoregulation.py`:
- `get_next_block_blueprint_bias(athlete_profile, block_response) -> dict`
- Integrated into `select_blueprint` in `src/forge/blueprint_engine.py`

## Inputs
- `athlete_profile`: Current athlete profile (may include prior block data)
- `block_response`: Object summarizing the prior block response (see `BlockResponse` in `src/forge/models.py`)

## Bias Outputs
The function returns a dict with the following boolean flags and a list of nudges:
- `prefer_power_speed`: Favor blueprints emphasizing power then speed
- `prefer_speed_power`: Favor blueprints emphasizing speed then power
- `reduce_conditioning`: Decrease conditioning emphasis
- `lower_fatigue`: Prefer lower fatigue blueprints
- `keep_sprint_emphasis`: Maintain sprint emphasis in programming
- `add_conditioning_bias`: Increase conditioning emphasis
- `maintain_same_blueprint`: Prefer to stay on same or similar blueprint
- `nudges`: Human-readable explanations applied

## Deterministic Rules

### Rule 1: Power Conversion Bias
If the prior block showed improved squat strength but stalled CMJ:
- Set `prefer_speed_power = True`
- Nudge: "Athlete improved force but CMJ stalled -> bias next block toward power conversion, not brute force"
*(Typically applied to rugby/american football athletes)*

### Rule 2: Speed-Power Bias
If the prior block showed improved aerobic band but stalled sprint:
- Set `prefer_power_speed = True`
- Set `keep_sprint_emphasis = True`
- Nudge: "Athlete improved aerobic capacity but sprint stalled -> bias toward speed / court-power emphasis"
*(Typically applied to tennis/basketball athletes)*

### Rule 3: Youth Athlete Conservation
If the athlete is youth (age < 20 or youth role) and had poor response (no improvements, at least one regression):
- Set `lower_fatigue = True`
- Set `maintain_same_blueprint = True`
- Nudge: "Youth athlete with poor response -> stay conservative, repeat or slightly regress emphasis"

### Rule 4: Multiple Regressions
If no improvements and two or more regressions:
- Set `lower_fatigue = True`
- Nudge: "Multiple regressions with no improvements -> choose lower fatigue option"

### Rule 5: Aerobic Regression During Strength Block
If aerobic band regressed and the prior block was strength-oriented:
- Set `add_conditioning_bias = True`
- Nudge: "Aerobic band regressed during strength block -> adding mild conditioning bias"

## Blueprint Selection Integration
The bias flags are used to score candidate blueprints from the normal selection process (season phase and sport). The blueprint with the highest score is selected.

Scoring criteria (example):
- +2 for matching prefer_power_speed/prefer_speed_power categories
- -2 for conditioning flags when reduce_conditioning is true
- +2 for lower_fatigue on low-fatigue blueprints (IDs 6,7,12,13)
- +2 for keep_sprint_emphasis if sprint is mandatory
- +2 for add_conditioning_bias if conditioning emphasis
- +3 for maintain_same_blueprint if matches prior blueprint ID

## Blueprint Categories (Reference)
See `src/forge/prescription_rules.py` `BLUEPRINT_CATEGORIES`:
- 1: strength_dominant
- 2: strength_power
- 3: strength_conditioning
- 4: power_speed
- 5: hypertrophy
- 6: power_maintenance
- 7: youth_foundation
- 8: court_sport
- 9: strength_dominant
- 10: sprint_development
- 11: hypertrophy
- 12: return_to_play
- 13: deload
- 14: gpp

## Example Applications
1. Rugby prop with improved squat strength but stalled CMJ → favors blueprint 4 (Power+Speed) or 2 (Strength+Power) over pure strength.
2. Tennis player with improved aerobic but stalled sprint → favors blueprint 4 or 10 (Sprint Development) with sprint emphasis.
3. Youth athlete with poor response → favors blueprint 6 (Power Maintenance), 7 (Youth Foundation), 12 (Return to Sport), or 13 (Deload).