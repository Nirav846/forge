"""Deterministic prescription rules — sets, reps, loading, progression.

Single source of truth for all prescription logic.
No magic numbers scattered in files.
"""
from typing import Optional
from .models import (
    Exercise, FamilyCode, Objective, AthleteLevel,
    PrescriptionRole, Prescription, COMP_WINDOW_LABELS,
    AthleteProfile, SeasonPhase,
)
from .data import BLUEPRINT_BY_ID


# ── ROLE DERIVATION ────────────────────────────────────────────────

def derive_role(ex: Exercise) -> PrescriptionRole:
    fam = ex.family
    obj = ex.objective

    if fam == FamilyCode.CORE:
        return PrescriptionRole.CORE_STABILITY
    if fam == FamilyCode.SPRINT:
        return PrescriptionRole.SPRINT_MECHANICS
    if fam == FamilyCode.LANDING:
        return PrescriptionRole.LANDING_MECHANICS
    if fam == FamilyCode.CARRY:
        return PrescriptionRole.CARRY_CAPACITY
    if fam == FamilyCode.PLYO:
        return PrescriptionRole.PLYOMETRIC
    if fam == FamilyCode.BALL:
        return PrescriptionRole.EXPLOSIVE_POWER
    if fam == FamilyCode.ACC:
        return PrescriptionRole.REHAB_PREHAB
    if fam in (FamilyCode.DLKD, FamilyCode.DLHD) and obj == Objective.STRENGTH:
        return PrescriptionRole.MAIN_STRENGTH
    if fam in (FamilyCode.SLKD, FamilyCode.SLHD):
        if obj == Objective.STRENGTH:
            return PrescriptionRole.SECONDARY_STRENGTH
        if obj in (Objective.HYPERTROPHY, Objective.STABILITY):
            return PrescriptionRole.HYPERTROPHY_ACCESSORY
    if fam in (FamilyCode.HPUSH, FamilyCode.HPULL, FamilyCode.VPUSH, FamilyCode.VPULL):
        if obj == Objective.STRENGTH:
            return PrescriptionRole.SECONDARY_STRENGTH
        if obj == Objective.HYPERTROPHY:
            return PrescriptionRole.HYPERTROPHY_ACCESSORY
        if obj == Objective.POWER:
            return PrescriptionRole.EXPLOSIVE_POWER
    if obj == Objective.HYPERTROPHY:
        return PrescriptionRole.HYPERTROPHY_ACCESSORY
    if obj == Objective.CONDITIONING:
        return PrescriptionRole.CONDITIONING_LIFT
    if obj in (Objective.MOBILITY, Objective.STABILITY):
        return PrescriptionRole.REHAB_PREHAB
    return PrescriptionRole.SECONDARY_STRENGTH


# ── BASE PRESCRIPTION TABLE ────────────────────────────────────────
# Key: (PrescriptionRole, level_str, objective_str)
# Value: {sets, reps, loading_method, intensity_note, rest_seconds, progression_method}

_BASE = PrescriptionRole
_B = AthleteLevel.BEGINNER.value
_I = AthleteLevel.INTERMEDIATE.value
_A = AthleteLevel.ADVANCED.value

PRESCRIPTION_TABLE: dict[tuple[PrescriptionRole, str, str], dict] = {
    # ── MAIN STRENGTH ──────────────────────────────────────────────
    (_BASE.MAIN_STRENGTH, _B, "STR"): {
        "sets": "3-4", "reps": "8-12",
        "loading_method": "straight sets",
        "intensity_note": "RPE 7-8",
        "rest_seconds": 180, "progression_method": "double_progression",
    },
    (_BASE.MAIN_STRENGTH, _I, "STR"): {
        "sets": "4", "reps": "6-8",
        "loading_method": "straight sets",
        "intensity_note": "RPE 7-9",
        "rest_seconds": 240, "progression_method": "double_progression",
    },
    (_BASE.MAIN_STRENGTH, _A, "STR"): {
        "sets": "4-5", "reps": "3-5",
        "loading_method": "straight sets",
        "intensity_note": "RPE 8-9",
        "rest_seconds": 300, "progression_method": "linear",
    },
    (_BASE.MAIN_STRENGTH, _B, "POW"): {
        "sets": "3-4", "reps": "3-5",
        "loading_method": "straight sets",
        "intensity_note": "explosive, RPE 7",
        "rest_seconds": 180, "progression_method": "exposure",
    },
    (_BASE.MAIN_STRENGTH, _I, "POW"): {
        "sets": "4", "reps": "3-5",
        "loading_method": "straight sets",
        "intensity_note": "explosive, RPE 7-8",
        "rest_seconds": 240, "progression_method": "exposure",
    },
    (_BASE.MAIN_STRENGTH, _A, "POW"): {
        "sets": "4-5", "reps": "2-4",
        "loading_method": "clusters",
        "intensity_note": "explosive, RPE 8",
        "rest_seconds": 300, "progression_method": "exposure",
    },
    (_BASE.MAIN_STRENGTH, _B, "HYP"): {
        "sets": "3-4", "reps": "10-15",
        "loading_method": "straight sets",
        "intensity_note": "RPE 6-8",
        "rest_seconds": 90, "progression_method": "double_progression",
    },
    (_BASE.MAIN_STRENGTH, _I, "HYP"): {
        "sets": "4", "reps": "10-12",
        "loading_method": "straight sets",
        "intensity_note": "RPE 7-8",
        "rest_seconds": 90, "progression_method": "double_progression",
    },
    (_BASE.MAIN_STRENGTH, _A, "HYP"): {
        "sets": "4", "reps": "8-10",
        "loading_method": "straight sets",
        "intensity_note": "RPE 7-8",
        "rest_seconds": 90, "progression_method": "double_progression",
    },

    # ── SECONDARY STRENGTH ─────────────────────────────────────────
    (_BASE.SECONDARY_STRENGTH, _B, "STR"): {
        "sets": "3", "reps": "8-12",
        "loading_method": "straight sets",
        "intensity_note": "RPE 7-8",
        "rest_seconds": 90, "progression_method": "double_progression",
    },
    (_BASE.SECONDARY_STRENGTH, _I, "STR"): {
        "sets": "3", "reps": "8-10",
        "loading_method": "straight sets",
        "intensity_note": "RPE 7-8",
        "rest_seconds": 90, "progression_method": "double_progression",
    },
    (_BASE.SECONDARY_STRENGTH, _A, "STR"): {
        "sets": "3-4", "reps": "6-8",
        "loading_method": "straight sets",
        "intensity_note": "RPE 7-8",
        "rest_seconds": 120, "progression_method": "double_progression",
    },
    (_BASE.SECONDARY_STRENGTH, _B, "HYP"): {
        "sets": "3", "reps": "12-15",
        "loading_method": "straight sets",
        "intensity_note": "RPE 6-8",
        "rest_seconds": 60, "progression_method": "double_progression",
    },
    (_BASE.SECONDARY_STRENGTH, _I, "HYP"): {
        "sets": "3-4", "reps": "12-15",
        "loading_method": "straight sets",
        "intensity_note": "RPE 7-8",
        "rest_seconds": 60, "progression_method": "double_progression",
    },
    (_BASE.SECONDARY_STRENGTH, _A, "HYP"): {
        "sets": "3-4", "reps": "10-15",
        "loading_method": "straight sets / drop sets",
        "intensity_note": "RPE 7-9",
        "rest_seconds": 60, "progression_method": "double_progression",
    },
    (_BASE.SECONDARY_STRENGTH, _B, "POW"): {
        "sets": "3", "reps": "3-5",
        "loading_method": "straight sets",
        "intensity_note": "explosive, RPE 7",
        "rest_seconds": 120, "progression_method": "exposure",
    },
    (_BASE.SECONDARY_STRENGTH, _I, "POW"): {
        "sets": "3-4", "reps": "3-5",
        "loading_method": "straight sets",
        "intensity_note": "explosive, RPE 7-8",
        "rest_seconds": 120, "progression_method": "exposure",
    },
    (_BASE.SECONDARY_STRENGTH, _A, "POW"): {
        "sets": "3-4", "reps": "3",
        "loading_method": "clusters",
        "intensity_note": "explosive, RPE 8",
        "rest_seconds": 150, "progression_method": "exposure",
    },

    # ── HYPERTROPHY ACCESSORY ─────────────────────────────────────
    (_BASE.HYPERTROPHY_ACCESSORY, _B, "HYP"): {
        "sets": "3", "reps": "12-15",
        "loading_method": "straight sets",
        "intensity_note": "RPE 6-8",
        "rest_seconds": 60, "progression_method": "double_progression",
    },
    (_BASE.HYPERTROPHY_ACCESSORY, _I, "HYP"): {
        "sets": "3-4", "reps": "12-15",
        "loading_method": "straight sets",
        "intensity_note": "RPE 7-8",
        "rest_seconds": 60, "progression_method": "double_progression",
    },
    (_BASE.HYPERTROPHY_ACCESSORY, _A, "HYP"): {
        "sets": "3-4", "reps": "10-15",
        "loading_method": "straight sets / myo-reps",
        "intensity_note": "RPE 7-9",
        "rest_seconds": 45, "progression_method": "double_progression",
    },

    # ── EXPLOSIVE POWER ──────────────────────────────────────────
    (_BASE.EXPLOSIVE_POWER, _B, "POW"): {
        "sets": "3-4", "reps": "3-5",
        "loading_method": "clusters",
        "intensity_note": "explosive, submaximal",
        "rest_seconds": 120, "progression_method": "exposure",
    },
    (_BASE.EXPLOSIVE_POWER, _I, "POW"): {
        "sets": "4-5", "reps": "3-5",
        "loading_method": "clusters",
        "intensity_note": "explosive, RPE 7-8",
        "rest_seconds": 150, "progression_method": "exposure",
    },
    (_BASE.EXPLOSIVE_POWER, _A, "POW"): {
        "sets": "4-5", "reps": "2-4",
        "loading_method": "clusters / complexes",
        "intensity_note": "max intent, RPE 8-9",
        "rest_seconds": 180, "progression_method": "exposure",
    },

    # ── PLYOMETRIC ──────────────────────────────────────────────
    (_BASE.PLYOMETRIC, _B, "POW"): {
        "sets": "2-3", "reps": "4-6",
        "loading_method": "ground contact",
        "intensity_note": "quality, 2-3s reset",
        "rest_seconds": 90, "progression_method": "exposure",
    },
    (_BASE.PLYOMETRIC, _I, "POW"): {
        "sets": "3-4", "reps": "4-6",
        "loading_method": "ground contact",
        "intensity_note": "max intent",
        "rest_seconds": 120, "progression_method": "exposure",
    },
    (_BASE.PLYOMETRIC, _A, "POW"): {
        "sets": "4-5", "reps": "3-5",
        "loading_method": "shock / complex",
        "intensity_note": "max intent, reactive",
        "rest_seconds": 150, "progression_method": "exposure",
    },

    # ── SPRINT MECHANICS ────────────────────────────────────────
    (_BASE.SPRINT_MECHANICS, _B, "STR"): {
        "sets": "3-4", "reps": "15-20m",
        "loading_method": "quality reps",
        "intensity_note": "technique focus",
        "rest_seconds": 120, "progression_method": "exposure",
    },
    (_BASE.SPRINT_MECHANICS, _I, "STR"): {
        "sets": "4-5", "reps": "20-30m",
        "loading_method": "quality reps",
        "intensity_note": "build to max",
        "rest_seconds": 150, "progression_method": "exposure",
    },
    (_BASE.SPRINT_MECHANICS, _A, "STR"): {
        "sets": "4-6", "reps": "20-40m",
        "loading_method": "quality reps",
        "intensity_note": "max velocity or accel",
        "rest_seconds": 180, "progression_method": "exposure",
    },
    (_BASE.SPRINT_MECHANICS, _B, "POW"): {
        "sets": "3-4", "reps": "10-20m",
        "loading_method": "flying starts",
        "intensity_note": "build speed",
        "rest_seconds": 150, "progression_method": "exposure",
    },
    (_BASE.SPRINT_MECHANICS, _I, "POW"): {
        "sets": "4-5", "reps": "20-30m",
        "loading_method": "flying starts",
        "intensity_note": "max speed",
        "rest_seconds": 180, "progression_method": "exposure",
    },
    (_BASE.SPRINT_MECHANICS, _A, "POW"): {
        "sets": "4-6", "reps": "20-40m",
        "loading_method": "flying starts / resisted",
        "intensity_note": "max velocity or resisted",
        "rest_seconds": 180, "progression_method": "exposure",
    },

    # ── CORE STABILITY ──────────────────────────────────────────
    (_BASE.CORE_STABILITY, _B, "STAB"): {
        "sets": "2-3", "reps": "20-30s holds / 8-12 reps",
        "loading_method": "controlled",
        "intensity_note": "quality, brace",
        "rest_seconds": 45, "progression_method": "exposure",
    },
    (_BASE.CORE_STABILITY, _I, "STAB"): {
        "sets": "3", "reps": "30-45s holds / 10-15 reps",
        "loading_method": "controlled",
        "intensity_note": "quality, anti-movement",
        "rest_seconds": 45, "progression_method": "exposure",
    },
    (_BASE.CORE_STABILITY, _A, "STAB"): {
        "sets": "3-4", "reps": "45-60s holds / 12-15 reps",
        "loading_method": "controlled / loaded",
        "intensity_note": "quality, anti-movement",
        "rest_seconds": 45, "progression_method": "exposure",
    },

    # ── CARRY CAPACITY ──────────────────────────────────────────
    (_BASE.CARRY_CAPACITY, _B, "STR"): {
        "sets": "3", "reps": "20-30m",
        "loading_method": "loaded carry",
        "intensity_note": "posture, brace",
        "rest_seconds": 60, "progression_method": "exposure",
    },
    (_BASE.CARRY_CAPACITY, _I, "STR"): {
        "sets": "3-4", "reps": "30-40m",
        "loading_method": "loaded carry",
        "intensity_note": "posture, heavy",
        "rest_seconds": 60, "progression_method": "exposure",
    },
    (_BASE.CARRY_CAPACITY, _A, "STR"): {
        "sets": "4", "reps": "40-50m",
        "loading_method": "loaded carry / farmer",
        "intensity_note": "max load, posture",
        "rest_seconds": 90, "progression_method": "exposure",
    },

    # ── LANDING MECHANICS ───────────────────────────────────────
    (_BASE.LANDING_MECHANICS, _B, "POW"): {
        "sets": "3", "reps": "3-5",
        "loading_method": "quality",
        "intensity_note": "soft landing, knee tracking",
        "rest_seconds": 60, "progression_method": "exposure",
    },
    (_BASE.LANDING_MECHANICS, _I, "POW"): {
        "sets": "3-4", "reps": "3-5",
        "loading_method": "quality",
        "intensity_note": "soft landing, knee tracking",
        "rest_seconds": 60, "progression_method": "exposure",
    },
    (_BASE.LANDING_MECHANICS, _A, "POW"): {
        "sets": "4", "reps": "4-6",
        "loading_method": "quality / reactive",
        "intensity_note": "soft landing, knee tracking",
        "rest_seconds": 60, "progression_method": "exposure",
    },

    # ── REHAB / PREHAB ──────────────────────────────────────────
    (_BASE.REHAB_PREHAB, _B, "STAB"): {
        "sets": "2-3", "reps": "10-15",
        "loading_method": "controlled",
        "intensity_note": "pain-free, quality",
        "rest_seconds": 45, "progression_method": "exposure",
    },
    (_BASE.REHAB_PREHAB, _I, "STAB"): {
        "sets": "2-3", "reps": "12-15",
        "loading_method": "controlled",
        "intensity_note": "pain-free, quality",
        "rest_seconds": 45, "progression_method": "exposure",
    },
    (_BASE.REHAB_PREHAB, _A, "STAB"): {
        "sets": "3", "reps": "12-15",
        "loading_method": "controlled",
        "intensity_note": "pain-free, quality",
        "rest_seconds": 45, "progression_method": "exposure",
    },

    # ── CONDITIONING LIFT ───────────────────────────────────────
    (_BASE.CONDITIONING_LIFT, _B, "COND"): {
        "sets": "2-3", "reps": "15-20",
        "loading_method": "circuit density",
        "intensity_note": "controlled",
        "rest_seconds": 45, "progression_method": "exposure",
    },
    (_BASE.CONDITIONING_LIFT, _I, "COND"): {
        "sets": "3", "reps": "15-20",
        "loading_method": "circuit density",
        "intensity_note": "moderate pace",
        "rest_seconds": 45, "progression_method": "exposure",
    },
    (_BASE.CONDITIONING_LIFT, _A, "COND"): {
        "sets": "3-4", "reps": "15-20",
        "loading_method": "circuit density",
        "intensity_note": "moderate pace, short rest",
        "rest_seconds": 30, "progression_method": "exposure",
    },
}


# ── COMPETITION WINDOW MODIFIERS ──────────────────────────────────

COMP_WINDOW_MODIFIERS: dict[int, dict] = {
    6: {"set_factor": 1.0, "trim_accessories": False, "notes": "Full training week"},
    4: {"set_factor": 0.85, "trim_accessories": True, "notes": "Moderate — reduce accessory volume"},
    2: {"set_factor": 0.7, "trim_accessories": True, "notes": "Light — preserve power, reduce strength volume"},
    1: {"set_factor": 0.5, "trim_accessories": True, "notes": "Primer — technique only, minimal volume"},
}


# ── BLUEPRINT CATEGORIES ──────────────────────────────────────────

BLUEPRINT_CATEGORIES: dict[int, str] = {
    1: "strength_dominant",
    2: "strength_power",
    3: "strength_conditioning",
    4: "power_speed",
    5: "hypertrophy",
    6: "power_maintenance",
    7: "youth_foundation",
    8: "court_sport",
    9: "strength_dominant",
    10: "sprint_development",
    11: "hypertrophy",
    12: "return_to_play",
    13: "deload",
    14: "gpp",
}


def get_blueprint_category(blueprint_id: int) -> str:
    return BLUEPRINT_CATEGORIES.get(blueprint_id, "strength_dominant")


# ── BLUEPRINT PRESCRIPTION OVERRIDES ──────────────────────────────

BLUEPRINT_PRESCRIPTION_MODIFIERS: dict[str, dict] = {
    "youth_foundation": {
        "notes": "Capped sets at 3, no low-rep strength, prefer 8-12 range",
        "set_cap": 3,
        "rep_floor": 6,
        "force_rehab_role": False,
        "intensity_shift": "conservative",
    },
    "power_speed": {
        "notes": "Reduce strength volume, preserve explosive work",
        "main_strength_set_factor": 0.75,
        "explosive_set_factor": 1.0,
        "shorter_rest_explosive": False,
    },
    "hypertrophy": {
        "notes": "Higher rep ranges, shorter rest, more density",
        "rep_shift": "+2-3 reps",
        "rest_factor": 0.75,
        "prefer_hypertrophy_role": True,
    },
    "deload": {
        "notes": "All sets capped at 2, easy intensity",
        "set_cap": 2,
        "intensity_note": "RPE 5-6",
        "rest_factor": 1.0,
    },
    "return_to_play": {
        "notes": "Low volume, high quality, rehab-first",
        "set_cap": 3,
        "rep_floor": 8,
        "force_intensity": "RPE 6-7",
    },
    "sprint_development": {
        "notes": "Sprint work maintained, strength supportive",
        "sprint_set_factor": 1.0,
        "main_strength_set_factor": 0.8,
    },
    "power_maintenance": {
        "notes": "Low volume, high stimulus, keep power",
        "set_cap": 3,
        "main_strength_set_factor": 0.5,
        "explosive_set_factor": 1.0,
    },
    "strength_conditioning": {
        "notes": "Strength maintained, not maximised due to cond stress",
        "main_strength_set_factor": 0.85,
    },
    "gpp": {
        "notes": "Balanced exposure, nothing maximised",
        "set_cap": 4,
        "strength_set_factor": 0.85,
    },
    "court_sport": {
        "notes": "Single-leg and rotational emphasis, strength maintained",
        "sl_set_factor": 1.1,
        "rot_set_factor": 1.0,
    },
}


# ── WEEK-TYPE PROGRESSION VOLUME ───────────────────────────────────

WEEK_TYPE_VOLUME_FACTORS: dict[str, float] = {
    "accumulation": 0.85,
    "intensification": 1.0,
    "realization": 1.05,
    "taper": 0.80,
    "test": 0.65,
    "deload": 0.60,
    "light": 0.50,
}

WEEK_PROGRESSION_NOTES: dict[int, str] = {
    1: "Accumulation — establish base volume",
    2: "Accumulation — build exposure",
    3: "Intensification — progress",
    4: "Intensification — maintain",
    5: "Peak — high quality",
    6: "Peak — high quality",
    7: "Taper — reduce volume",
    8: "Taper / Deload — reduced load",
}


# ── MAIN PRESCRIPTION FUNCTION ─────────────────────────────────────

def get_prescription(
    ex: Exercise,
    level: AthleteLevel,
    blueprint_id: int,
    comp_window: Optional[int] = None,
    week: int = 1,
    week_type: str = "accumulation",
    athlete_profile: Optional[AthleteProfile] = None,
) -> Prescription:
    role = derive_role(ex)
    obj = ex.objective.value
    level_str = level.value

    # Look up base prescription
    key = (role, level_str, obj)
    if key not in PRESCRIPTION_TABLE:
        # Fallback: try (role, level_str, "STR")
        key = (role, level_str, "STR")
    if key not in PRESCRIPTION_TABLE:
        return Prescription(
            sets="3", reps="8-12",
            loading_method="straight sets",
            intensity_note="RPE 7-8",
            progression_method="double_progression",
            rest_seconds=90,
        )

    base = dict(PRESCRIPTION_TABLE[key])

    # Apply blueprint category modifier
    bp_cat = get_blueprint_category(blueprint_id)
    bp_mod = BLUEPRINT_PRESCRIPTION_MODIFIERS.get(bp_cat, {})

    set_cap = bp_mod.get("set_cap")
    if set_cap:
        base["sets"] = _cap_sets(base["sets"], set_cap)

    int_override = bp_mod.get("force_intensity") or bp_mod.get("intensity_note")
    if int_override:
        base["intensity_note"] = int_override

    # Strength-conditional set factors from blueprint
    mssf = bp_mod.get("main_strength_set_factor")
    if mssf and role == PrescriptionRole.MAIN_STRENGTH:
        base["sets"] = _scale_sets(base["sets"], mssf)
    ssf = bp_mod.get("strength_set_factor")
    if ssf and role in (PrescriptionRole.MAIN_STRENGTH, PrescriptionRole.SECONDARY_STRENGTH):
        base["sets"] = _scale_sets(base["sets"], ssf)

    # Apply competition window modifier
    if comp_window is not None:
        comp_mod = COMP_WINDOW_MODIFIERS.get(comp_window, {})
        sf = comp_mod.get("set_factor", 1.0)
        if sf < 1.0:
            base["sets"] = _scale_sets(base["sets"], sf)
        if comp_mod.get("trim_accessories") and role in (
            PrescriptionRole.HYPERTROPHY_ACCESSORY,
            PrescriptionRole.REHAB_PREHAB,
            PrescriptionRole.CONDITIONING_LIFT,
        ):
            base["sets"] = _cap_sets(base["sets"], 2)
        if comp_window <= 2:
            base["intensity_note"] = base.get("intensity_note", "") + ", submaximal"

    # Apply week-type volume factor (primary driver)
    wf = WEEK_TYPE_VOLUME_FACTORS.get(week_type, 1.0)
    base["sets"] = _scale_sets(base["sets"], wf)

    # Youth override: cap sets at 3, no low-rep work
    if bp_cat in ("youth_foundation",) or (hasattr(level, 'value') and level == AthleteLevel.BEGINNER and week <= 2):
        base["sets"] = _cap_sets(base["sets"], 3)

    # Wave 6: Apply athlete profile prescription modifiers
    if athlete_profile:
        ap_mods = get_athlete_prescription_modifiers(athlete_profile, role)
        role_mods = get_role_prescription_modifiers(
            athlete_profile.position_role,
            athlete_profile.sport,
            role,
        )
        combined = _merge_presc_mods(ap_mods, role_mods)
        if combined.get("set_cap"):
            base["sets"] = _cap_sets(base["sets"], combined["set_cap"])
        if combined.get("intensity_note_bias"):
            base["intensity_note"] = base.get("intensity_note", "") + combined["intensity_note_bias"]
        if combined.get("rep_shift") == "lower":
            base["reps"] = _shift_reps_lower(base["reps"])

    return Prescription(
        sets=base.get("sets", "3"),
        reps=base.get("reps", "8-12"),
        loading_method=base.get("loading_method", "straight sets"),
        intensity_note=base.get("intensity_note", "RPE 7-8"),
        progression_method=base.get("progression_method", "double_progression"),
        rest_seconds=base.get("rest_seconds", 90),
    )


def _merge_presc_mods(a: dict, b: dict) -> dict:
    """Merge two prescription modifier dicts, b taking precedence."""
    merged = dict(a)
    for k, v in b.items():
        if k == "intensity_note_bias":
            merged[k] = merged.get(k, "") + v
        else:
            merged[k] = v
    return merged


def _shift_reps_lower(reps_str: str) -> str:
    """Shift rep range to the lower end. '6-8' → '5-6', '3-5' → '3-4'."""
    import re
    nums = re.findall(r"\d+", reps_str)
    if not nums:
        return reps_str
    ints = [int(n) for n in nums]
    if len(ints) == 1:
        return str(max(1, ints[0] - 1))
    shifted = [max(1, ints[0] - 1), max(1, ints[1] - 1)]
    if shifted[0] >= shifted[1]:
        return str(shifted[1])
    return f"{shifted[0]}-{shifted[1]}"


# ── PRESCRIPTION AGGREGATION (full session) ────────────────────────

def prescription_for_session_block(
    exercises: list[Exercise],
    level: AthleteLevel,
    blueprint_id: int,
    comp_window: Optional[int] = None,
    week: int = 1,
    week_type: str = "accumulation",
) -> list[Prescription]:
    return [get_prescription(ex, level, blueprint_id, comp_window, week, week_type) for ex in exercises]


# ── HELPERS ─────────────────────────────────────────────────────────

def _cap_sets(sets_str: str, cap: int) -> str:
    """Cap max set count. '3-4' with cap 3 → '3'. '4-5' with cap 3 → '3'."""
    import re
    nums = re.findall(r"\d+", sets_str)
    if not nums:
        return str(cap)
    ints = [int(n) for n in nums]
    capped = [min(n, cap) for n in ints]
    if len(capped) == 1:
        return str(capped[0])
    if capped[0] == capped[1]:
        return str(capped[0])
    return f"{capped[0]}-{capped[1]}"


def _scale_sets(sets_str: str, factor: float) -> str:
    """Scale set counts by factor. '4-5' with 0.75 → '3-4'."""
    import re
    nums = re.findall(r"\d+", sets_str)
    if not nums:
        return sets_str
    ints = [int(n) for n in nums]
    scaled = [max(1, round(n * factor)) for n in ints]
    if len(scaled) == 1:
        return str(scaled[0])
    if scaled[0] == scaled[1]:
        return str(scaled[0])
    return f"{scaled[0]}-{scaled[1]}"


# ── COMPETITION WINDOW RESOLUTION ─────────────────────────────────

def resolve_comp_window(days_to_match: Optional[int]) -> Optional[int]:
    """Convert days to match → comp window code (1/2/4/6/None)."""
    if days_to_match is None:
        return None
    if days_to_match <= 1:
        return 1
    if days_to_match <= 3:
        return 2
    if days_to_match <= 5:
        return 4
    return 6


# ── WAVE 6: ATHLETE PROFILE PRESCRIPTION MODIFIERS ────────────────

def get_athlete_prescription_modifiers(
    profile: Optional[AthleteProfile],
    role: PrescriptionRole,
) -> dict:
    """Return athlete-profile-driven prescription modifiers.

    Returns a dict with optional keys:
    - set_cap: int (cap max sets)
    - rep_shift: str ("lower", "upper", None — which end of range to bias)
    - intensity_note_bias: str (append to intensity note)
    - rest_factor: float (scale rest seconds)
    - loading_bias: str (e.g. "heavier", "velocity")
    """
    mods: dict = {}
    if not profile:
        return mods

    fp = profile.force_profile

    # Force / velocity profile
    if fp == "force_deficient":
        if role == PrescriptionRole.MAIN_STRENGTH:
            mods["rep_shift"] = "lower"  # 6-8 → 5-6, 3-5 → 3-4
            mods["intensity_note_bias"] = ", heavy bias"
            mods["loading_bias"] = "heavier"
        elif role == PrescriptionRole.EXPLOSIVE_POWER:
            mods["intensity_note_bias"] = ", strength-bias power"
        elif role == PrescriptionRole.HYPERTROPHY_ACCESSORY:
            mods["set_cap"] = 3
            mods["intensity_note_bias"] = ", controlled"

    elif fp == "velocity_deficient":
        if role == PrescriptionRole.MAIN_STRENGTH:
            mods["intensity_note_bias"] = ", velocity-friendly"
            mods["loading_bias"] = "velocity"
        elif role == PrescriptionRole.EXPLOSIVE_POWER:
            mods["intensity_note_bias"] = ", max intent velocity"
            mods["rep_shift"] = "lower"  # 3-5 → 3-4 for power
        elif role == PrescriptionRole.PLYOMETRIC:
            mods["intensity_note_bias"] = ", reactive focus"

    # Landing competency
    lp = profile.landing_competency
    if lp == "poor":
        if role == PrescriptionRole.LANDING_MECHANICS:
            mods["set_cap"] = 3
            mods["intensity_note_bias"] = ", controlled stick focus"
        elif role == PrescriptionRole.PLYOMETRIC:
            mods["set_cap"] = 3
            mods["intensity_note_bias"] = ", low-reactive"

    # Wave 11a — In-season volume reduction (role-aware: preserve primary, trim accessory)
    if profile.season_phase == SeasonPhase.IN_SEASON:
        existing = mods.get("set_cap", 999)
        if role in (PrescriptionRole.MAIN_STRENGTH, PrescriptionRole.SECONDARY_STRENGTH,
                    PrescriptionRole.EXPLOSIVE_POWER, PrescriptionRole.PLYOMETRIC,
                    PrescriptionRole.SPRINT_MECHANICS):
            mods["set_cap"] = min(existing, 4)   # strength/power preserved at 4
        elif role in (PrescriptionRole.HYPERTROPHY_ACCESSORY,
                      PrescriptionRole.CONDITIONING_LIFT,
                      PrescriptionRole.CARRY_CAPACITY):
            mods["set_cap"] = min(existing, 3)   # accessory trimmed more
        # Landing, Core, Rehab remain uncapped

    # Conditioning profile
    cp = profile.conditioning_profile
    if cp == "poor":
        if role in (PrescriptionRole.CONDITIONING_LIFT, PrescriptionRole.SPRINT_MECHANICS):
            mods["set_cap"] = 3
            mods["intensity_note_bias"] = ", submaximal density"

    # Risk flags
    if profile.patellar_tendon_risk:
        if role == PrescriptionRole.PLYOMETRIC:
            mods["set_cap"] = 2
            mods["intensity_note_bias"] = ", low-impact"

    if profile.hamstring_risk:
        if role == PrescriptionRole.SPRINT_MECHANICS:
            mods["set_cap"] = 3
            mods["intensity_note_bias"] = ", controlled exposure"

    if profile.shoulder_overhead_risk:
        if role in (PrescriptionRole.EXPLOSIVE_POWER, PrescriptionRole.SECONDARY_STRENGTH):
            mods["intensity_note_bias"] = ", overhead modified"

    if profile.lumbar_risk:
        if role in (PrescriptionRole.MAIN_STRENGTH, PrescriptionRole.SECONDARY_STRENGTH):
            mods["intensity_note_bias"] = ", lumbar-aware"

    # ── Wave 7: Test-Band-Driven Prescription Bias ──────────────────
    # 1. Strength work (squat_strength_band)
    ssb = getattr(profile, "squat_strength_band", None)
    if ssb:
        ssb_l = ssb.lower()
        if role in (PrescriptionRole.MAIN_STRENGTH, PrescriptionRole.SECONDARY_STRENGTH):
            if ssb_l == "low" and getattr(profile, "force_profile", None) == "force_deficient":
                mods["rep_shift"] = "lower"
                mods["intensity_note_bias"] = mods.get("intensity_note_bias", "") + ", heavy loading focus"
                mods["loading_bias"] = "heavier"
            elif ssb_l in ("high", "elite"):
                mods["intensity_note_bias"] = mods.get("intensity_note_bias", "") + ", power bias / explosive execution"

    # 2. Plyo / jump work (cmj_band)
    cmjb = getattr(profile, "cmj_band", None)
    if cmjb:
        cmjb_l = cmjb.lower()
        if role == PrescriptionRole.PLYOMETRIC:
            if cmjb_l == "low":
                mods["set_cap"] = min(mods.get("set_cap", 999), 3)
                mods["intensity_note_bias"] = mods.get("intensity_note_bias", "") + ", conservative lower-complexity plyo"
            elif cmjb_l in ("high", "elite") and getattr(profile, "landing_competency", None) != "poor":
                mods["intensity_note_bias"] = mods.get("intensity_note_bias", "") + ", reactive and advanced plyo dosing"

    # 3. Sprint / speed work (sprint_10m_band)
    s10b = getattr(profile, "sprint_10m_band", None)
    if s10b:
        s10b_l = s10b.lower()
        if role == PrescriptionRole.SPRINT_MECHANICS:
            if s10b_l == "low":
                mods["intensity_note_bias"] = mods.get("intensity_note_bias", "") + ", acceleration quality focus, lower density"
                mods["set_cap"] = min(mods.get("set_cap", 999), 3)
            elif s10b_l in ("high", "elite"):
                mods["intensity_note_bias"] = mods.get("intensity_note_bias", "") + ", velocity-oriented velocity exposure"

    # 4. Conditioning (aerobic_band)
    ab = getattr(profile, "aerobic_band", None)
    if ab:
        ab_l = ab.lower()
        if role == PrescriptionRole.CONDITIONING_LIFT:
            if ab_l == "low":
                mods["intensity_note_bias"] = mods.get("intensity_note_bias", "") + ", aerobic support focus"
            elif ab_l in ("high", "elite"):
                mods["intensity_note_bias"] = mods.get("intensity_note_bias", "") + ", minimal generic aerobic volume"
                mods["set_cap"] = min(mods.get("set_cap", 999), 2)

    return mods


# ── WAVE 6: ROLE-BASED PRESCRIPTION MODIFIERS ─────────────────────

def get_role_prescription_modifiers(
    role_key: str,
    sport: str,
    prescription_role: PrescriptionRole,
) -> dict:
    """Return prescription modifiers for a specific sport role."""
    mods: dict = {}
    if not role_key:
        return mods

    role_mods = _ROLE_PRESCRIPTION_MODS.get(sport, {}).get(role_key, {})
    return role_mods.get(prescription_role, {}).copy()


_ROLE_PRESCRIPTION_MODS: dict[str, dict[str, dict[str, dict]]] = {
    "cricket": {
        "fast_bowler": {
            PrescriptionRole.MAIN_STRENGTH: {"intensity_note_bias": ", lumbar-aware hinge dosing"},
            PrescriptionRole.SPRINT_MECHANICS: {"intensity_note_bias": ", submaximal sprint density"},
            PrescriptionRole.EXPLOSIVE_POWER: {"intensity_note_bias": ", shoulder-friendly loading"},
        },
        "spinner": {
            PrescriptionRole.EXPLOSIVE_POWER: {"intensity_note_bias": ", rotational power emphasis"},
        },
        "batter": {
            PrescriptionRole.EXPLOSIVE_POWER: {"intensity_note_bias": ", rotational power emphasis"},
        },
    },
    "rugby": {
        "prop": {
            PrescriptionRole.MAIN_STRENGTH: {"intensity_note_bias": ", maximal force emphasis"},
            PrescriptionRole.SECONDARY_STRENGTH: {"set_cap": 3},
            PrescriptionRole.PLYOMETRIC: {"set_cap": 3},
        },
        "lock": {
            PrescriptionRole.PLYOMETRIC: {"intensity_note_bias": ", jump-landing control"},
        },
        "back_row": {
            PrescriptionRole.SPRINT_MECHANICS: {"intensity_note_bias": ", repeat sprint focus"},
        },
        "backline": {
            PrescriptionRole.SPRINT_MECHANICS: {"intensity_note_bias": ", max velocity"},
            PrescriptionRole.PLYOMETRIC: {"intensity_note_bias": ", reactive emphasis"},
        },
    },
    "tennis": {
        "singles": {
            PrescriptionRole.SPRINT_MECHANICS: {"set_cap": 3},
            PrescriptionRole.CONDITIONING_LIFT: {"intensity_note_bias": ", court conditioning density"},
        },
        "doubles": {
            PrescriptionRole.EXPLOSIVE_POWER: {"intensity_note_bias": ", first-step emphasis"},
        },
    },
    "volleyball": {
        "middle": {
            PrescriptionRole.PLYOMETRIC: {"intensity_note_bias": ", block-jump loading"},
            PrescriptionRole.LANDING_MECHANICS: {"intensity_note_bias": ", repeated landing control"},
        },
        "libero": {
            PrescriptionRole.LANDING_MECHANICS: {"intensity_note_bias": ", lateral coverage"},
            PrescriptionRole.SPRINT_MECHANICS: {"set_cap": 3, "intensity_note_bias": ", short-burst"},
        },
    },
    "soccer": {
        "goalkeeper": {
            PrescriptionRole.PLYOMETRIC: {"intensity_note_bias": ", lateral dive loading"},
            PrescriptionRole.LANDING_MECHANICS: {"intensity_note_bias": ", diving landing control"},
        },
        "midfielder": {
            PrescriptionRole.SPRINT_MECHANICS: {"intensity_note_bias": ", repeat running"},
            PrescriptionRole.CONDITIONING_LIFT: {"intensity_note_bias": ", conditioning support"},
        },
        "forward": {
            PrescriptionRole.SPRINT_MECHANICS: {"intensity_note_bias": ", max acceleration"},
            PrescriptionRole.PLYOMETRIC: {"intensity_note_bias": ", finishing power"},
        },
    },
}


def describe_prescription_modifiers(mods: dict) -> list[str]:
    """Generate human-readable notes from prescription modifier dict."""
    notes = []
    if mods.get("rep_shift") == "lower":
        notes.append("Lower rep ranges for strength emphasis")
    if mods.get("loading_bias") == "heavier":
        notes.append("Heavier loading bias applied")
    if mods.get("loading_bias") == "velocity":
        notes.append("Velocity-friendly loading applied")
    ib = mods.get("intensity_note_bias", "")
    if ib:
        notes.append(f"Prescription note: {ib.strip(', ')}")
    if mods.get("set_cap"):
        notes.append(f"Sets capped at {mods['set_cap']}")
    return notes
