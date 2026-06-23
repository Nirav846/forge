# FORGE Competition Window Rulebook — V1.5

## Overview

Five competition windows defined by `days_to_match`. Each window alters exercise eligibility, slot composition, and volume for the main lifting session.

## Window Definitions

| Window | days_to_match | Code | Session feel |
|--------|---------------|------|-------------|
| NONE | None | None | No competition constraint |
| FULL | ≥6 | 6 | Full training, all exercises |
| MODERATE | 4-5 | 4 | Moderate taper, cap fatigue |
| LIGHT | 2-3 | 2 | Low fatigue, speed-power emphasis |
| PRIMER | ≤1 | 1 | Activation only, no fatigue |

## Constraints by Window

### NONE (no competition date)
- **Allowed fatigue**: 1-5
- **Allowed impact**: 1-5
- **Allowed eccentric**: 1-5
- **Volume**: Full (all families, all exercises)
- **Session feel**: Normal training session
- **Conditioning**: Full range

### FULL (≥6 days out)
- **Allowed fatigue**: 1-5
- **Allowed impact**: 1-5
- **Allowed eccentric**: 1-5
- **Volume**: Full (same as NONE)
- **Session feel**: Normal training session
- **Conditioning**: Full range

### MODERATE (4-5 days out)
- **Allowed fatigue**: 1-4
- **Allowed impact**: 1-4
- **Allowed eccentric**: 1-4
- **Volume**: Slight reduction (max 7 families)
- **What's filtered**: Exercises with any metric >4 (e.g., RDL ecc=5, Depth Jump impact=5)
- **Session feel**: Strong training session, but avoids the most damaging exercises
- **Conditioning**: Still works, but cap impact at 4

**Examples of what still works at MODERATE:**
- Back Squat (F4/I4/E3) ← fatigue=4 ≤4, impact=4 ≤4, eccentric=3 ≤4 ✓
- Bench Press (F3/I3/E3) ✓
- Deadlift variants with ecc≤4 ← RDL out, Block Pull/Rack Pull in
- Plyometrics (F3/I4/E2) ← impact=4 ≤4 ✓

**Examples of what's filtered:**
- RDL (ecc=5)
- Depth Jump (impact=5)
- Conventional Deadlift (F5)

### LIGHT (2-3 days out)
- **Allowed fatigue**: 1-3
- **Allowed impact**: 1-3
- **Allowed eccentric**: 1-3
- **Volume**: Reduced (max 5 families, accessory trimmed)
- **What's filtered**: Exercises with any metric >3
- **Session feel**: Maintain movement patterns, no soreness generators, keep speed exposure
- **Conditioning**: Cap impact at 3, only top_up/power_maintenance/recovery_flush

**Examples of what still works at LIGHT:**
- Goblet Squat (F3/I3/E3) ✓
- Bench Press (F3/I3/E3) ✓
- Barbell Rack Pull (F3/I3/E3) ✓
- Dumbbell Row (F3/I3/E3) ✓
- A-Skip (F3/I3/E1) ✓
- All Core ✓

**Examples of what's filtered:**
- Back Squat (F4) ← fatigue 4 > 3
- RDL (ecc=5)
- Depth Jump (impact=5)
- Squat Jump (impact=5)
- Pendlay Row (F4)
- Nordic Curl (ecc=5)
- Block Pull (F4)

### PRIMER (≤1 day out)
- **Allowed fatigue**: 1-2
- **Allowed impact**: 1-2
- **Allowed eccentric**: 1-2
- **Volume**: Very reduced (max 4 families, light session path)
- **What's kept**: Core, carries, light accessory, band work, activation
- **What's filtered**: All strength exercises (F≥3), all power/speed exercises (impact≥4), all eccentric exercises
- **Session feel**: Activation and mobility only. CNS preparation without fatigue
- **Conditioning**: Only recovery_flush or power_maintenance

**What still works at PRIMER:**
- All Core exercises ✓
- Pallof press variants ✓
- Band pull-aparts, face pulls ✓
- Light carries ✓
- Stretching/prehab ✓

**What's filtered:**
- Every strength exercise (all have F≥3)
- All plyometrics (impact≥4)
- All ballistics (impact≥4)
- All sprint exercises except Marching (most have impact≥4 or fatigue≥4)

## Slot-Level Adjustments

### By Window

| Window | Max Families | What gets trimmed first |
|--------|------------|------------------------|
| NONE | 8 | Nothing |
| FULL | 8 | Nothing |
| MODERATE | 7 | Accessory, then rotational |
| LIGHT | 5 | Accessory, rotational, single-leg variants |
| PRIMER | 4 | All optional, keep mandatory only |

### Blueprint Identity Preservation

- Mandatory families (from blueprint) are always kept
- Power/speed families are preserved at all windows including LIGHT (keeps Sprint/Plyo slots)
- Core is always present (moved to end by session flow rules)
- Accessory is the first to be trimmed

## Interaction with Existing Blueprints

**Full Body Strength (bp01):** At LIGHT, drops Acc, keeps DLKD/HPush/DLHD/HPull/Core. Exercise substitutions filter the high-risk variants.

**Sprint Development (bp10):** At LIGHT, keeps Sprint but drops Plyo (all Plyo exercises have impact≥4). Sprint exercises like A-Skip and Marching pass.

**Rugby Off-Season (bp09):** More families available → more trimming at LIGHT. Still keeps mandatory contact-prep work.

**Deload (bp13):** Already designed as light session. Competition logic adds additional exercise-level filtering.

## Sport-Agnostic Assumptions

1. Lower body eccentric loading is the highest pre-competition risk (DOMS directly impairs running/jumping)
2. High impact (plyometrics, sprinting) is the second-highest risk (tissue stress, delayed recovery)
3. Upper body strength work can be kept closer to competition than lower body (less interference with sport performance)
4. Core/stability/prehab can always be performed regardless of competition proximity
5. Speed/power work should be preserved as close to competition as possible (maintain CNS readiness)

## Validation

The 13th validator check `competition_appropriate` flags sessions where >1 exercise violates the window constraints. This is a warning-level check — 0-1 violations per session is acceptable (accounts for substitution fallback gaps).
