# FORGE Wave 1 Sprint Plan — Implementation Audit & Scope

**Source:** `FORGE_BOOK_HARDENING_ROADMAP_V1.md` 4-wave plan
**Audit:** 15 top Core items against live `D:\forge\src\forge\` codebase
**Scope:** 12 items, ~19 hours
**Design principle:** Fix active bugs first, then highest-credibility structural improvements, then fill critical exercise gaps.

---

## Part 1: Audit Summary

### Codebase state: 5 of 15 items are "active bugs"

| Item | Title | Audit finding | Priority |
|------|-------|---------------|----------|
| T-RULE-01 | Rest period by objective | **Active bug.** `rest_period` hardcoded `"60-90s"` in `main.py:263` for all objectives. Field exists but never derived. | Fix now |
| T-RULE-14 | Load spike prevention | **Active bug.** No week-over-week load tracking exists. No load metrics. Would need a proxy system. | Fix now |
| T-RULE-10 | Mastery-based progression gate | **Partial.** `technique_consistency` field exists on `AthleteProfile` (models.py:173), used in `determine_level()` (blueprint_engine.py:78-87) but never as a continuous gate within level. | Fix now |
| T-RULE-11 | Bilateral→unilateral rule | **Partial.** `strength_base_met` uses fragile `hasattr()` pattern in `blueprint_engine.py:84`. No proper field. | Fix now |
| T-RULE-21 | Training age priority | **Missing.** `AthleteProfile` has `training_age_years` but no `age` field (models.py:166-181). Cannot compute `min(training_age, age_cap)`. | Fix now |
| T-WU-05 | Warmup phase structure | **Partial.** `WarmupPhase`/`WarmupProtocol` models exist (models.py:197-207). `select_warmup()` already groups by phase (warmup_engine.py:898-928). But `SESSION_TYPE_WARMUPS` is flat drill-ID lists (line 806-819), not phase-ordered per sport. | Fix now |
| T-WU-06 | Athlete-profile differentiation | **Partial.** "youth" and "return_to_play" keys exist in `SESSION_TYPE_WARMUPS` (line 814-815) but `select_warmup()` never uses `athlete.athlete_level` to key into them. | Wave 2 |
| T-EX-06 | Landing mechanics | **Missing.** No `LANDING` FamilyCode. `Plyo-016` (Single-Leg Landing) exists as Plyo but no dedicated landing progression family. | Fix now |
| T-EX-08 | Sprint mechanics | **Partial.** Warmup sprint drills exist (SM-01 through SM-07). Sprint family has 22 exercises (exercises_data.py). Sprint-019 through Sprint-022 use `"MECH/COD"` and `"SPD/MECH"` objectives not in `Objective` enum — silently falls to `STRENGTH`. | Fix now |
| T-RULE-13 | Exercise monotony | **Partial.** `running_recent` dict tracks `last_used` per exercise (main.py:266-269). `_least_recently_used()` (exercise_selector.py:95-109) uses binary seen/not-seen scoring. No 2x/week cap. | Fix now |
| T-RULE-16 | Previous injury risk | **Partial.** `injury_map` duplicated 3x across `exercise_selector.py:79-86`, `substitution_engine.py:113-118`, `validator.py:123-128`. `_injury_conflict()` is all-or-nothing blocking, not risk scoring. | Fix now |
| T-RULE-30 | Stable→unstable gating | **Missing.** No `surface` field on `Exercise` (models.py:70-88). No stable/unstable concept in exercise data. | Fix now |
| T-RULE-32 | RAMP phase audit | **Partial.** Drills already have `phase` field ("raise"/"activate"/"potentiate"/"prepare"). `select_warmup()` already groups by phase. RAMP phase field on `WarmupDrill` model exists. Need to formalize and audit. | Fix now |
| T-RULE-04 | RM zone prescription | **Deferred.** No load prescription system exists (no sets/reps/weight%). `target_intensity` is hardcoded `"moderate"` (main.py:262). Would need a new load model. | Wave 2 |
| T-RULE-02 | Novice linear progression | **Deferred.** System selects exercises only — no load prescription. Touches models.py, exercise_selector.py, main.py, renderer.py. Realistically 8-12h, not 4h. | Wave 2 |

### Cross-cutting issues found

1. **`injury_map` duplicated 3 files** — must refactor to shared module before changing
2. **Sprint-019–022 use invalid `Objective` strings** — `"MECH/COD"` and `"SPD/MECH"` not in `Objective` enum; silently default to `STRENGTH`
3. **No `age` field on `AthleteProfile`** — blocks T-RULE-21 and all youth-age logic
4. **Hardcoded `target_intensity` and `rest_period`** — both are strings in `main.py:262-263` set every session regardless of objective
5. **`strength_base_met` uses fragile `hasattr()`** — blueprint_engine.py:84 only checked for advanced level; not a proper field

---

## Part 2: Recommended Sprint Scope (12 items, ~19h)

### Group A: Safety Fixes (5 items, 5h)

#### A1. T-RULE-01 — Rest Period by Objective (1h)

**Files changed:** `models.py`, `main.py`, `data.py`

```diff
--- models.py (add mapping constant)
+OBJECTIVE_REST_MAP: dict[str, str] = {
+    "STR": "3-5min",
+    "POW": "3-5min",
+    "HYP": "60-90s",
+    "COND": "30-60s",
+    "MOB": "30-60s",
+    "STAB": "60-90s",
+}

--- main.py:258-264
-        block = SessionBlock(
-            family=family,
-            family_name=family.value,
-            exercises=[ex] if ex else [],
-            target_intensity="moderate",
-            rest_period="60-90s",
-        )
+        block = SessionBlock(
+            family=family,
+            family_name=family.value,
+            exercises=[ex] if ex else [],
+            target_intensity="moderate",
+            rest_period=OBJECTIVE_REST_MAP.get(ex.objective.value if ex else "STR", "60-90s"),
+        )
```

**Acceptance criteria:**
- Strength/power blocks show `rest_period="3-5min"` instead of `"60-90s"`
- Hypertrophy blocks remain `"60-90s"`
- Conditioning blocks show `"30-60s"`
- No change in program behavior — only rendered output field

---

#### A2. T-RULE-14 — Load Spike Prevention (2h)

**Files changed:** `main.py`, `models.py`

Load proxy: use `sum(ex.difficulty * 2 for ex in session_exercises)` as estimated load. The 1RM/percentage system doesn't exist, so we use a difficulty-based load proxy.

```diff
--- models.py (add to Session or AthleteProfile)
+@dataclass  
+class WeeklyLoad:
+    week: int
+    total_difficulty: int = 0
+    total_exercises: int = 0

--- main.py:136-150  (generation loop)
+    weekly_loads: list[WeeklyLoad] = []
+
     for week in range(1, weeks + 1):
+        week_load = WeeklyLoad(week=week)
         for day in range(1, freq + 1):
             session = _build_session(...)
+            ses_load = sum(ex.difficulty * 2 for b in session.blocks for ex in b.exercises if ex)
+            week_load.total_difficulty += ses_load
+            week_load.total_exercises += len([ex for b in session.blocks for ex in b.exercises if ex])
             sessions.append(session)
+        weekly_loads.append(week_load)
+
+    # Enforce 15% week-over-week cap
+    for i in range(1, len(weekly_loads)):
+        prev = weekly_loads[i-1].total_difficulty or 1
+        curr = weekly_loads[i].total_difficulty
+        if curr > prev * 1.15:
+            # Reduce: cap at 115% of previous
+            scale = (prev * 1.15) / curr
+            weekly_loads[i].total_difficulty = int(prev * 1.15)
+            # Signal to render that this week was capped
+            sessions[i-1].load_capped = True  # or add a week-level flag
+        elif curr < prev * 0.7:
+            weekly_loads[i].total_difficulty = int(prev * 0.7)
+            sessions[i-1].load_floor_hit = True  # flag if below 70%
```

**Acceptance criteria:**
- Week-over-week increase capped at 15% (using difficulty proxy)
- If week N is >115% of week N-1, the computed load is clamped and a flag is set
- If week N is <70% of week N-1 (excessive drop), a flag is set
- No change to exercise selection logic — purely post-hoc load constraint

---

#### A3. T-RULE-10 — Mastery-Based Progression Gate (1h)

**Files changed:** `exercise_selector.py`

```diff
--- exercise_selector.py
 def select_exercise(
     slot_family: FamilyCode,
     athlete_level: AthleteLevel,
     equipment_profile: EquipmentProfile,
     recent_exercises: dict[str, dict],
     injury_history: list[str],
     days_to_match: Optional[int] = None,
+    technique_consistency: float = 1.0,
 ) -> Optional[Exercise]:
     comp_window = _resolve_comp_window(days_to_match)
     max_diff = get_max_difficulty(athlete_level.value)
+    # Apply technique gate: reduce effective max difficulty
+    if technique_consistency < 0.8:
+        max_diff = min(max_diff, 1)  # force regression to difficulty-1 exercises
+    elif technique_consistency < 0.9:
+        max_diff = max_diff  # normal for level
     ...
```

**Acceptance criteria:**
- When `technique_consistency < 0.8`, effective `max_diff` is clamped to 1 (regression exercises only)
- When `technique_consistency >= 0.9`, normal level-based difficulty applies
- Restriction is per-forwarded from `_build_session()` — need to add `technique_consistency` parameter through call chain

---

#### A4. T-RULE-11 — Bilateral→Unilateral Gate (1h)

**Files changed:** `models.py`, `exercise_selector.py`

```diff
--- models.py (add to AthleteProfile)
 class AthleteProfile:
     ...
     preferred_families: int = 6
+    strength_base_met: bool = True  # 1.5x BW squat prerequisite for unilateral

--- blueprint_engine.py:84 (replace hasattr)
-        if hasattr(athlete, 'strength_base_met') and not athlete.strength_base_met:
+        if not athlete.strength_base_met:
             return AthleteLevel.INTERMEDIATE

--- exercise_selector.py:17 (add parameter and gate)
 def select_exercise(
     ...
     technique_consistency: float = 1.0,
+    strength_base_met: bool = True,
 ) -> Optional[Exercise]:
+    # Bilateral→unilateral gate
+    if slot_family in (FamilyCode.SLKD, FamilyCode.SLHD) and not strength_base_met:
+        sub_family = {FamilyCode.SLKD: FamilyCode.DLKD, FamilyCode.SLHD: FamilyCode.DLHD}[slot_family]
+        slot_family = sub_family  # downgrade to bilateral variant
```

**Acceptance criteria:**
- When `strength_base_met=False`, SLKD and SLHD exercises are never selected
- They downgrade to DLKD/DLHD equivalents
- Passing `strength_base_met=True` (default) preserves current behavior

---

#### A5. T-RULE-21 — Training Age Priority (1h)

**Files changed:** `models.py`, `blueprint_engine.py`

```diff
--- models.py:166
 class AthleteProfile:
     ...
     preferred_families: int = 6
+    age: int = 18  # chronological age

--- blueprint_engine.py:78-87  (determine_level)
 def determine_level(athlete: AthleteProfile) -> AthleteLevel:
-    if athlete.training_age_years < 1 or athlete.technique_consistency < 0.8:
+    effective_ta = athlete.training_age_years
+    if athlete.age < 20:
+        effective_ta = min(athlete.training_age_years, max(0, (athlete.age - 14) * 0.5))
+    if effective_ta < 1 or athlete.technique_consistency < 0.8:
         return AthleteLevel.BEGINNER
-    if 1 <= athlete.training_age_years < 3 and athlete.technique_consistency >= 0.8:
+    if 1 <= effective_ta < 3 and athlete.technique_consistency >= 0.8:
         return AthleteLevel.INTERMEDIATE
-    if athlete.training_age_years >= 3 and athlete.technique_consistency >= 0.8:
+    if effective_ta >= 3 and athlete.technique_consistency >= 0.8:
         if not athlete.strength_base_met:
             return AthleteLevel.INTERMEDIATE
         return AthleteLevel.ADVANCED
```

Also update `_shortlist_by_season_phase()` which also uses `training_age_years` directly (lines 27, 53).

**Acceptance criteria:**
- A 16yo with 2yr training age gets `effective_ta=1.0` (capped at `(16-14)*0.5 = 1.0`)
- A 25yo with 2yr training age gets `effective_ta=2.0` (full training age)
- The `age` field defaults to 18 for backward compatibility

---

### Group B: Structural Warmup Improvements (2 items, 6h)

#### B1. T-WU-05 — Sport-Specific Warmup Phase Structure (4h)

**Files changed:** `warmup_engine.py`

```diff
--- warmup_engine.py:806-819  (replace SESSION_TYPE_WARMUPS)
-SESSION_TYPE_WARMUPS = {
-    "strength": ["R-01", "R-05", ...],
-    ...
-}

+# Phase-ordered warmup templates per session type + sport
+SESSION_WARMUP_TEMPLATES = {
+    "strength": {
+        "raise": ["R-01", "R-05"],
+        "activate": ["HM-03", "GA-01", "TS-09"],
+        "potentiate": ["P-08", "P-09"],
+        "prepare": [],
+    },
+    "power": {
+        "raise": ["R-01", "R-05"],
+        "activate": ["HM-01", "HM-03", "GA-01", "TS-07"],
+        "potentiate": ["P-11", "P-01", "P-05"],
+        "prepare": [],
+    },
+    "speed": {
+        "raise": ["R-01", "R-02", "R-03", "R-04"],
+        "activate": ["HM-01", "HM-02", "HM-03", "HM-10", "GA-08", "SM-01", "SM-02", "SM-03", "SM-04", "SM-05", "SM-06", "SM-07"],
+        "potentiate": ["P-06", "P-10", "P-12"],
+        "prepare": [],
+    },
+    "conditioning": {
+        "raise": ["R-01", "R-05"],
+        "activate": ["HM-03", "GA-01", "CA-01"],
+        "potentiate": ["P-11", "P-06"],
+        "prepare": [],
+    },
+    "competition": {
+        "raise": ["R-01", "R-03", "R-05", "R-14"],
+        "activate": ["HM-03", "HM-10", "TS-03", "GA-08", "CA-01"],
+        "potentiate": ["P-01", "P-03", "P-06"],
+        "prepare": ["SS-14", "SS-11"],
+    },
+    "youth": {
+        "raise": ["R-01", "R-05", "R-14"],
+        "activate": ["HM-03", "GA-01", "CA-01", "AF-01"],
+        "potentiate": ["P-10", "P-01"],
+        "prepare": [],
+    },
+    "return_to_play": {
+        "raise": ["R-01"],
+        "activate": ["HM-03", "CA-01", "AF-07", "NC-01"],
+        "potentiate": [],
+        "prepare": [],
+    },
+    "deload": {
+        "raise": ["R-01", "R-05"],
+        "activate": ["HM-03", "GA-01", "CA-01"],
+        "potentiate": [],
+        "prepare": [],
+    },
+    "court_speed": {
+        "raise": ["R-01", "R-03", "R-04", "CT-03", "CT-04"],
+        "activate": ["HM-01", "HM-02", "HM-03", "CT-01", "CT-02", "CT-05", "CT-06"],
+        "potentiate": ["P-06", "P-10"],
+        "prepare": [],
+    },
+    "court_strength": {
+        "raise": ["R-01", "CT-03", "CT-04"],
+        "activate": ["HM-03", "HM-01", "CT-01", "CT-02", "CT-05", "GA-01", "CA-01", "TS-07"],
+        "potentiate": ["P-09"],
+        "prepare": [],
+    },
+}

+SERVE_SPECIFIC_WARMUPS = {
+    "tennis": {
+        "raise": ["R-01", "R-03", "R-05"],
+        "activate": ["HM-03", "TS-03", "shoulder_prone_y", "shoulder_band_pull", "trunk_rotation_band", "lateral_lunge_walk"],
+        "potentiate": ["P-01", "serve_toss_repeat", "shadow_swing_progressive"],
+        "prepare": ["SS-05", "SS-06"],
+    },
+    "cricket": {
+        "raise": ["R-01", "R-03", "R-05"],
+        "activate": ["HM-03", "HM-10", "GA-01", "shoulder_band_pull", "trunk_rotation_band"],
+        "potentiate": ["P-01", "med_ball_rotational_throw"],
+        "prepare": ["SS-01", "SS-02"],
+    },
+}
+
+# Keep legacy flat lists for backward compat
+SESSION_TYPE_WARMUPS = {k: sum(v.values(), []) for k, v in SESSION_WARMUP_TEMPLATES.items()}
```

Update `select_warmup()` to use phase-ordered templates and sport-specific overrides:

```diff
--- warmup_engine.py:869-931
 def select_warmup(athlete, session_type, environment="gym"):
-    drill_ids = list(SESSION_TYPE_WARMUPS.get(session_type, SESSION_TYPE_WARMUPS["strength"]))
+    # Phase-ordered template lookup
+    template = SESSION_WARMUP_TEMPLATES.get(session_type, SESSION_WARMUP_TEMPLATES["strength"])
+    
+    # Sport-specific override for tennis/cricket
+    sport = athlete.sport.lower().strip()
+    if sport in SERVE_SPECIFIC_WARMUPS and session_type == "competition":
+        template = SERVE_SPECIFIC_WARMUPS[sport]
+    
+    drill_ids = sum(template.values(), [])
     
     # Sport-aware substitution for competition warmup
     if session_type == "competition":
-        sport = athlete.sport.lower().strip()
         sport_prep = SPORT_PREP_DRILLS.get(sport, [])
         if sport_prep:
             drill_ids = [did for did in drill_ids if did not in {"SS-14", "SS-11"}]
@@ -891,6 +906,11 @@ def select_warmup(athlete, session_type, environment="gym"):
     # Group by phase
     phases_dict = {}
     for drill in drills:
+        # Use template phase ordering, not drill's self-reported phase
+        phase = next(
+            (pn for pn, pids in template.items() if drill.id in pids),
+            drill.phase
+        )
         phase = drill.phase
         if phase not in phases_dict:
             phases_dict[phase] = []
```

**Acceptance criteria:**
- `select_warmup()` produces phase-ordered output using template structure, not flat lists
- Tennis competition warmup uses tennis-specific template (with shoulder prep, serve prep)
- Cricket competition warmup uses cricket-specific template
- All existing session types still produce valid warmups
- Legacy `SESSION_TYPE_WARMUPS` flat dict maintained for backward compatibility

---

#### B2. T-RULE-32 — RAMP Phase Audit (2h)

**Files changed:** `warmup_engine.py`

```diff
--- warmup_engine.py (add phase audit function)
+def audit_ramp_phases() -> dict:
+    """Audit all warmup drills for RAMP phase completeness."""
+    phase_counts = {"raise": 0, "activate": 0, "potentiate": 0, "prepare": 0}
+    unassigned = []
+    for did, drill in WARMUP_DRILLS.items():
+        if drill.phase in phase_counts:
+            phase_counts[drill.phase] += 1
+        else:
+            unassigned.append(did)
+    return {
+        "phase_counts": phase_counts,
+        "unassigned": unassigned,
+        "total_drills": len(WARMUP_DRILLS),
+        "phases_present": [p for p, c in phase_counts.items() if c > 0],
+    }

 def select_warmup(athlete, session_type, environment="gym"):
+    # Normalize phase field on all drills
+    for did, drill in WARMUP_DRILLS.items():
+        if drill.phase not in ("raise", "activate", "potentiate", "prepare"):
+            drill.phase = {"R": "raise", "HM": "activate", "P": "potentiate", "SS": "prepare", 
+                           "SM": "activate", "GA": "activate", "TS": "activate", 
+                           "CA": "activate", "NC": "activate", "AF": "activate",
+                           "CT": "activate"}.get(drill.id.split("-")[0], "raise")
```

**Acceptance criteria:**
- `audit_ramp_phases()` returns a dict with phase counts and any unassigned drills
- All drills have a valid RAMP phase (raise/activate/potentiate/prepare)
- Drills with non-standard phase values are auto-corrected
---



### Group C: Injury Prevention & Refactoring (2 items, 3h)

#### C1. T-RULE-16 — Previous Injury Risk Refactor (2h)

**Files changed:** `injury_map.py` (new), `exercise_selector.py`, `substitution_engine.py`, `validator.py`

```diff
+++ injury_map.py (new file — shared module)
+"""Shared injury-exercise conflict maps. Single source of truth."""
+
+INJURY_EXERCISE_MAP: dict[str, list[str]] = {
+    "low_back": ["Conventional Deadlift", "Barbell Row", "Barbell Good Morning", "Good Morning"],
+    "acl_left": ["Depth Jump", "Pistol Squat", "Single-Leg Depth Jump"],
+    "acl_right": ["Depth Jump", "Pistol Squat", "Single-Leg Depth Jump"],
+    "shoulder": ["Barbell Bench Press", "Barbell Overhead Press", "Muscle-Up"],
+    "patellar": ["Depth Jump", "Pistol Squat", "Bulgarian Split Squat"],
+    "hamstring": ["Conventional Deadlift", "RDL", "Nordic Hamstring Curl", "Stiff-Leg Deadlift"],
+}
+
+def has_injury_conflict(exercise_name: str, injury_history: list[str]) -> bool:
+    for injury in injury_history:
+        for key in INJURY_EXERCISE_MAP:
+            if key in injury.lower():
+                if exercise_name in INJURY_EXERCISE_MAP[key]:
+                    return True
+    return False
+
+def injury_risk_multiplier(exercise_name: str, injury_history: list[str]) -> float:
+    """Return 1.0 (no conflict) or 0.0 (blocked) — future: graduated scoring."""
+    return 0.0 if has_injury_conflict(exercise_name, injury_history) else 1.0
```

Then replace all 3 inline copies with imports:

```diff
--- exercise_selector.py:78-92
- def _injury_conflict(...)
+ from .injury_map import has_injury_conflict as _injury_conflict

--- substitution_engine.py:112-124
- def _inj_conflict(...)
+ from .injury_map import has_injury_conflict as _inj_conflict

--- validator.py:122-137
- def _check_injury_history(...)
+ from .injury_map import has_injury_conflict
  def _check_injury_history(session, athlete):
      for block in session.blocks:
          for ex in block.exercises:
-             if _inj_conflict(...)
+             if has_injury_conflict(ex.name, athlete.injury_history):
                  return False
```

**Acceptance criteria:**
- All 3 files import from `injury_map.py` — zero code duplication
- `injury_risk_multiplier()` returns 0.0 for conflicts, 1.0 for safe (ready for scoring extension)
- Validator, selector, and substitution all use the same map
- Behavior is identical to before (backward compatible)

---

#### C2. T-RULE-30 — Stable→Unstable Surface Gating (1h)

**Files changed:** `models.py`, `data.py`, `exercise_selector.py`

```diff
--- models.py:70-88 (Exercise)
 class Exercise:
     ...
+    surface: str = "stable"  # "stable" | "unstable" | "both"
     competition_role: str = "strength"

--- data.py (add surface override func)
+def _infer_surface(ed: dict) -> str:
+    name = ed.get("name", "").lower()
+    keywords = ["bosu", "balance pad", "unstable", "wobble", "dynadisc", "swiss ball", "stability ball"]
+    if any(k in name for k in keywords):
+        return "unstable"
+    return "stable"

--- data.py:51 _infer_exercise_comp_metadata — add surface to returned dict
+    ed["surface"] = _infer_surface(ed)
```

**Acceptance criteria:**
- `Exercise.surface` defaults to `"stable"` — existing exercises unaffected
- Exercises with unstable-surface keywords auto-detect
- Future gating rule can check `surface` before selection ---

### Group D: Exercise Library Additions (2 items, 3h)

#### D1. T-EX-06 — Landing Mechanics Progressions (2h)

**Files changed:** `models.py`, `exercises_data.py`, `data.py`, `blueprint_data.py` (optional)

```diff
--- models.py (add FamilyCode)
 class FamilyCode(str, Enum):
     ...
+    LANDING = "Landing"

--- data.py (add LANDING to metadata maps)
+    "Landing": 3,  # _EX_FATIGUE_BASE
+    "Landing": 4,  # _EX_IMPACT_BASE
+    "Landing": 2,  # _EX_ECCENTRIC_BASE
+    "Landing": "speed_power",  # _EX_ROLE

--- exercises_data.py (add ~10 exercises)
+{
+    "id": "Landing-001", "name": "Box Jump Stick (low, 6-12in)", "family": "Landing",
+    "secondary_family": None, "objective": "POW",
+    "difficulty": 1, "equipment": ["Box"],
+    "unilateral": False, "explosive": True, "isometric": False, "rotational": False,
+    "progression": "Landing-003", "regression": None,
+},
+{
+    "id": "Landing-002", "name": "Box Jump Stick (moderate, 12-18in)", "family": "Landing",
+    "secondary_family": None, "objective": "POW",
+    "difficulty": 2, "equipment": ["Box"],
+    "unilateral": False, "explosive": True, "isometric": False, "rotational": False,
+    "progression": "Landing-005", "regression": "Landing-001",
+},
+... (add ~8 more: lateral landing, single-leg stick, depth jump, etc.)

--- data.py (add SELECTION_PRIORITIES entry)
+    "Landing": ["Landing-001", "Landing-002", ...],
+    "Landing": [fam for fam, pri in FAMILIES_DATA],  # FAMILIES_DATA entry
```

**Acceptance criteria:**
- 8-10 landing mechanics exercises added in a new `LANDING` family
- Progressions from double-leg low box → single-leg reactive
- Exercises appear in SELECTION_PRIORITIES and are selectable
- All metadata fields populated (fatigue, impact, eccentric, role)

---

#### D2. T-EX-08 — Sprint Mechanics Drills (1h)

**Files changed:** `exercises_data.py`, `data.py`

```diff
--- exercises_data.py (add sprint mechanics exercises)
+{
+    "id": "Sprint-023", "name": "Acceleration Wall Drill", "family": "Sprint",
+    "secondary_family": None, "objective": "STR",
+    "difficulty": 1, "equipment": ["Bodyweight"],
+    "unilateral": False, "explosive": False, "isometric": False, "rotational": False,
+    "progression": "Sprint-024", "regression": None,
+},
+{
+    "id": "Sprint-024", "name": "A-Skip", "family": "Sprint",
+    "secondary_family": None, "objective": "STR",
+    "difficulty": 2, "equipment": ["Bodyweight"],
+    "unilateral": False, "explosive": False, "isometric": False, "rotational": False,
+    "progression": "Sprint-025", "regression": "Sprint-023",
+},
+{
+    "id": "Sprint-025", "name": "B-Skip", "family": "Sprint",
+    "secondary_family": None, "objective": "STR",
+    "difficulty": 2, "equipment": ["Bodyweight"],
+    "unilateral": False, "explosive": False, "isometric": False, "rotational": False,
+    "progression": "Sprint-026", "regression": "Sprint-023",
+},
+{
+    "id": "Sprint-026", "name": "C-Skip", "family": "Sprint",
+    "secondary_family": None, "objective": "STR",
+    "difficulty": 3, "equipment": ["Bodyweight"],
+    "unilateral": False, "explosive": True, "isometric": False, "rotational": False,
+    "progression": "Sprint-027", "regression": "Sprint-024",
+},
+{
+    "id": "Sprint-027", "name": "Flying Sprint 10m", "family": "Sprint",
+    "secondary_family": None, "objective": "POW",
+    "difficulty": 3, "equipment": ["Cones"],
+    "unilateral": False, "explosive": True, "isometric": False, "rotational": False,
+    "progression": "Sprint-028", "regression": "Sprint-026",
+},
+{
+    "id": "Sprint-028", "name": "Flying Sprint 20m", "family": "Sprint",
+    "secondary_family": None, "objective": "POW",
+    "difficulty": 4, "equipment": ["Cones"],
+    "unilateral": False, "explosive": True, "isometric": False, "rotational": False,
+    "progression": "Sprint-029", "regression": "Sprint-027",
+},
+{
+    "id": "Sprint-029", "name": "Flying Sprint 30m", "family": "Sprint",
+    "secondary_family": None, "equipment": ["Cones"],
+    "unilateral": False, "explosive": True, "isometric": False, "rotational": False,
+    "progression": None, "regression": "Sprint-028",
+},

--- data.py: SELECTION_PRIORITIES — add Sprint entries to beginning
+    "Sprint": ["Sprint-023", "Sprint-024", "Sprint-025", "Sprint-026", "Sprint-027", "Sprint-028", "Sprint-029", ...existing_sprint_ids],
```

Also fix the existing invalid `Objective` values:

```diff
--- exercises_data.py Sprint-019 through Sprint-022
-    "objective": "MECH/COD",
+    "objective": "COND",
-    "objective": "SPD/MECH",
+    "objective": "POW",
```

**Acceptance criteria:**
- 7 new sprint mechanics exercises added to Sprint family
- Progression from Wall Drill → A-Skip → B-Skip → C-Skip → Flying Sprint (10m→20m→30m)
- Existing Sprint-019 through Sprint-022 have valid `Objective` enum values
- Exercises appear in Sprint SELECTION_PRIORITIES

---

## Part 3: Dependency Graph

```
Level 0 (independent — any order):
  [A1] T-RULE-01  Rest period by objective       → models.py, main.py
  [A2] T-RULE-14  Load spike prevention           → main.py, models.py
  [A3] T-RULE-10  Mastery-based gate              → select_exercise call chain
  [A4] T-RULE-11  Bilateral→unilateral gate       → models.py, exercise_selector.py
  [A5] T-RULE-21  Training age priority           → models.py, blueprint_engine.py
  [C1] T-RULE-16  Injury map refactor             → injury_map.py, 3 consumers
  [C2] T-RULE-30  Surface gating                  → models.py, data.py
  [D1] T-EX-06    Landing mechanics               → models.py, data.py, exercises_data.py
  [D2] T-EX-08    Sprint mechanics                → exercises_data.py, data.py
  
Level 1 (needs Level 0 warmup drills):
  [B1] T-WU-05    Sport-specific warmup phase     → warmup_engine.py (uses drills)
  [B2] T-RULE-32  RAMP phase audit                → warmup_engine.py (formalizes phase field)
```

## Part 4: Recommended Implementation Order

| Order | Item | Hours | Why this order |
|-------|------|-------|----------------|
| 1 | C1 — Injury map refactor | 2 | Foundation — 3 other items depend on clean injury data |
| 2 | A5 — Training age priority | 1 | Simplest fix, unblocks all youth logic |
| 3 | A1 — Rest period by objective | 1 | One-line mapping, highest bug-fix ratio |
| 4 | A3 — Mastery progression gate | 1 | Uses existing field, minimal change |
| 5 | A4 — Bilateral→unilateral gate | 1 | Fixes fragile hasattr() pattern |
| 6 | C2 — Stable→unstable surface | 1 | Small field addition |
| 7 | A2 — Load spike prevention | 2 | Need week-loads architecture, moderate complexity |
| 8 | D1 — Landing mechanics | 2 | New FamilyCode — touches most files |
| 9 | D2 — Sprint mechanics | 1 | Data-only, no new FamilyCode |
| 10 | B2 — RAMP phase audit | 2 | Cleanup before warmup restructuring |
| 11 | B1 — Sport-specific warmup | 4 | Largest item — last for stability |

## Part 5: Acceptance Criteria (Global)

1. **`python -m forge` runs without errors** and produces valid output for all 3 levels × 3 equipment profiles
2. **No regression in existing output:** strength/power/hypertrophy programs still select appropriate exercises
3. **Credibility score** remains >= 0.8 for all 9 demo combinations
4. **Each item individually testable** via assertion-based self-check in its module `__main__` block

## Part 6: Items Explicitly Deferred to Wave 2

| Item | Reason | Effort | 
|------|--------|--------|
| T-WU-06 | Athlete-profile warmup diff | No dependency on other warmup items but needs session-type testing across levels | 4h |
| T-RULE-04 | RM zone prescription | Requires load model that doesn't exist | 2h |
| T-RULE-02 | Novice linear progression | Requires full load prescription system (sets/reps/weight%) | 8-12h |
| T-RULE-13 | Exercise monotony variation | Tracking exists but cap logic is small — could fit in this sprint if we swap in | 1h |
| T-EX-01-HIP | Hip flexor exercises | Pure data addition, no dependencies | 2h each |
| T-EX-02-PALLOFF | Pallof press exercises | Pure data addition | 2h each |
| T-EX-03-SHOULDER | Shoulder decel exercises | Depends on T-EX-06 landing mechanics for landing→throwing symmetry | 2h |
| T-EX-04-GROIN | Adductor exercises | Pure data addition | 2h |
| T-EX-05-ANKLE | Ankle stiffness exercises | Pure data addition | 2h |
| T-EX-07-MEDBALL | Med-ball rotational power | Pure data addition | 2h |
