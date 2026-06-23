# FORGE Test Band Progressions V1.0

## Overview
This document details how test bands (`cmj_band`, `sprint_10m_band`, `squat_strength_band`, `aerobic_band`) influence progression and prescription in FORGE Wave 7.

## Test Band Definitions
Each test band can have one of the following values:
- `"low"`: Below average performance
- `"moderate"`: Average performance (also represented as `"avg"` in some contexts)
- `"high"`: Above average performance
- `"elite"`: Elite performance (optional, not always used)

## Progression Logic
Wave 7 introduces deterministic rules for interpreting changes in test bands between blocks:

### Band Change Classification
- `Low → Moderate` or `Avg`: Improvement
- `Moderate/Avg → High`: Improvement
- `High → Elite`: Improvement
- Reverse transitions: Regression
- No change: Stall
- Unknown if either value is missing or invalid

### Application to Specific Bands
1. **CMJ Band (cmj_band)**: Reflects explosive power and jump performance.
2. **Sprint 10m Band (sprint_10m_band)**: Reflects acceleration and early-speed capability.
3. **Squat Strength Band (squat_strength_band)**: Reflects maximal lower-body strength.
4. **Aerobic Band (aerobic_band)**: Reflects aerobic capacity and endurance.

## Influence on Prescription
Test bands now directly affect prescription dosing (see `src/forge/prescription_rules.py` Wave 7 modifications):

### Strength Work (squat_strength_band)
- Low & force-deficient → lower rep strength work, heavier loading bias
- High/elite → power bias / explosive execution

### Plyo/Jump Work (cmj_band)
- Low → conservative lower-complexity plyo (volume capped)
- High/elite & good landing competency → reactive and advanced plyo dosing

### Sprint/Speed Work (sprint_10m_band)
- Low → acceleration quality focus, lower density
- High/elite → velocity-oriented velocity exposure

### Conditioning (aerobic_band)
- Low → aerobic support focus
- High/elite → minimal generic aerobic volume (set cap of 2)

## Integration with Existing Waves
- Builds upon Wave 5 (test bands exist but were underused)
- Compatible with Wave 6 (prescription personalization)
- Works alongside Wave 4 (week structure and testing markers)