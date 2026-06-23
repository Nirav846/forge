# FORGE Competition-Aware Session Generation — V1.5

## What Changed

### 1. Exercise Model Extended (models.py)
Four new fields on `Exercise`:
- `fatigue_cost` (int 1-5) — systemic fatigue from the exercise
- `impact_level` (int 1-5) — joint/ground impact forces
- `eccentric_cost` (int 1-5) — eccentric muscle damage risk
- `competition_role` (str) — `strength`, `speed_power`, `accessory`, `core`, `carry`

### 2. Metadata Inference (data.py)
All 241 exercises get auto-populated metadata via family-level bases with difficulty/isometric/explosive adjustments plus named overrides for specific exercises (RDL, Nordic, Depth Jump, Back Squat, etc.).

**Inference rules:**
| Family   | Fatigue Base | Impact Base | Eccentric Base | Role         |
|----------|-------------|-------------|----------------|--------------|
| DLKD     | 3           | 3           | 3              | strength     |
| DLHD     | 3           | 3           | 3              | strength     |
| SLKD     | 3           | 3           | 3              | strength     |
| SLHD     | 3           | 3           | 3              | strength     |
| HPush    | 3           | 3           | 3              | strength     |
| HPull    | 3           | 3           | 3              | strength     |
| VPush    | 3           | 3           | 2              | strength     |
| VPull    | 3           | 3           | 3              | strength     |
| Plyo     | 3           | 4           | 2              | speed_power  |
| Ball     | 3           | 4           | 1              | speed_power  |
| Sprint   | 3           | 3           | 1              | speed_power  |
| Rot      | 2           | 2           | 2              | accessory    |
| Carry    | 2           | 2           | 1              | carry        |
| Core     | 1           | 1           | 1              | core         |
| Acc      | 2           | 2           | 2              | accessory    |

**Adjustments:** diff>=4 → +1 fatigue & eccentric; explosive → +1 impact; isometric → eccentric=1, fatigue-1

### 3. Competition Windows (conditioning_engine.py)
```python
EXERCISE_COMP_MAX_FATIGUE   = {None:5, 6:5, 4:4, 2:3, 1:2}
EXERCISE_COMP_MAX_IMPACT    = {None:5, 6:5, 4:4, 2:3, 1:2}
EXERCISE_COMP_MAX_ECCENTRIC = {None:5, 6:5, 4:4, 2:3, 1:2}
```

### 4. Exercise Filtering (exercise_selector.py + substitution_engine.py)
Both `select_exercise` and `substitute_exercise` now accept `days_to_match` and filter by competition window before selection.

### 5. Volume Taper (main.py)
- `generate_program` uses `_resolve_comp_window` to adjust `preferred_families`:
  - MODERATE (4-5d): max 7 families
  - LIGHT (2-3d): max 5 families
  - PRIMER (<=1d): max 4 families (already handled by separate light path)
- Light session (`_build_light_session`) passes `days_to_match` for per-exercise filtering

### 6. Validator (validator.py)
Added 13th check `competition_appropriate` that flags sessions with >1 exercise violating competition window thresholds. Only active when `days_to_match` is set.

## Where

- `src/forge/models.py` — 4 new fields on Exercise dataclass
- `src/forge/data.py` — inference functions for exercise metadata
- `src/forge/conditioning_engine.py` — comp window thresholds
- `src/forge/exercise_selector.py` — comp-aware filtering
- `src/forge/substitution_engine.py` — comp-aware substitution
- `src/forge/main.py` — volume taper, days_to_match passthrough
- `src/forge/validator.py` — new competition appropriateness check
- `tests/test_competition_aware.py` — 43 new tests

## Why

Previously, `days_to_match` only affected the conditioning layer and a binary switch at 0/1 days. The main lifting session was completely competition-blind: a rugby player 2 days before a match could get RDLs, depth jumps, and heavy back squats alongside their teammates who had 14 days. For V1.5, the same metadata-driven filtering pattern used in the conditioning engine now applies to the main session.
