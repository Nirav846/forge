"""Athlete profile personalization and risk-aware rules for Wave 5."""
from __future__ import annotations
from typing import Optional
from .models import (
    AthleteProfile, Exercise, FamilyCode, ConditioningProtocol,
    AthleteLevel,
)

# Exercise family → personalization scoring labels
STRENGTH_FAMILIES = {FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.SLKD, FamilyCode.SLHD}
EXPLOSIVE_FAMILIES = {FamilyCode.PLYO, FamilyCode.BALL, FamilyCode.SPRINT}
LOWER_STRENGTH_FAMILIES = {FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.SLKD, FamilyCode.SLHD}
UPPER_PUSH_FAMILIES = {FamilyCode.HPUSH, FamilyCode.VPUSH}

# Exercise IDs for high-risk variants
HIGH_ECC_HINGE_IDS = {"DLHD-006", "DLHD-008", "DLHD-011", "DLHD-001"}  # RDL, SL RDL, Good Morning, Glute Bridge (low)
HIGH_ROTATION_IDS = {"Rot-009", "Rot-010", "Rot-011", "Rot-012", "Rot-013", "Rot-014", "Rot-016", "Rot-017"}


# ── Part 2: Exercise Personalization Bias ──────────────────────────

def get_exercise_personalization_bias(ex: Exercise, profile: AthleteProfile) -> int:
    """Return a scoring bias (-1, 0, +1) for this exercise given the athlete profile.

    Positive means "prefer this exercise", negative means "avoid this exercise".
    Applied as a tiebreaker in exercise selection.
    """
    bias = 0
    fp = profile.force_profile
    ep = profile.elastic_profile
    lp = profile.landing_competency
    sm = profile.sprint_mechanics_competency

    # Force / velocity profile
    if fp == "force_deficient":
        if ex.family in STRENGTH_FAMILIES and not ex.explosive:
            bias += 1
        if ex.family in EXPLOSIVE_FAMILIES:
            bias -= 1
    elif fp == "velocity_deficient":
        if ex.family in EXPLOSIVE_FAMILIES:
            bias += 1
        if ex.family in STRENGTH_FAMILIES and not ex.explosive:
            bias -= 1

    # Elastic profile → explosive bias
    if ep == "strong":
        if ex.family in (FamilyCode.PLYO, FamilyCode.BALL):
            bias += 1
    elif ep == "poor":
        if ex.family == FamilyCode.PLYO and ex.difficulty >= 3:
            bias -= 1

    # Landing competency → landing exercise choice
    if lp == "poor":
        if ex.family == FamilyCode.LANDING:
            if ex.difficulty >= 3:
                bias -= 2  # Strongly avoid advanced landings
            else:
                bias += 1  # Prefer basic landing prep
        if ex.family == FamilyCode.PLYO and ex.impact_level >= 4:
            bias -= 1
    elif lp == "strong":
        if ex.family == FamilyCode.LANDING and ex.difficulty >= 4:
            bias += 1

    # Sprint mechanics → drill vs output
    if sm == "poor":
        if ex.family == FamilyCode.SPRINT:
            if ex.difficulty <= 2:
                bias += 1  # Prefer drills
            else:
                bias -= 1  # Avoid full sprinting
    elif sm == "strong":
        if ex.family == FamilyCode.SPRINT and ex.difficulty >= 3:
            bias += 1

    return bias


# ── Risk-aware exercise filtering ──────────────────────────────────

def is_exercise_risk_flagged(ex: Exercise, profile: AthleteProfile) -> bool:
    """Return True if this exercise should be avoided due to athlete risk flags."""
    name_lower = ex.name.lower()

    # Lumbar risk
    if profile.lumbar_risk:
        if ex.family in (FamilyCode.DLHD, FamilyCode.SLHD):
            # High-eccentric hinges are risky
            if ("rdl" in name_lower or "good morning" in name_lower
                    or "stiff leg" in name_lower or "stiff-leg" in name_lower
                    or "straight-leg" in name_lower or "straight leg" in name_lower):
                return True
            if ex.id in HIGH_ECC_HINGE_IDS:
                return True
            if ex.eccentric_cost >= 4:
                return True
        # Heavy rotational loading
        if ex.family == FamilyCode.ROT and ex.difficulty >= 3:
            if ex.id in HIGH_ROTATION_IDS:
                return True
        # Avoid heavy spinal compression
        if ex.family == FamilyCode.DLKD and ex.difficulty >= 4:
            if "barbell back squat" in name_lower or "front squat" in name_lower:
                return True

    # Patellar tendon risk
    if profile.patellar_tendon_risk:
        if ex.family == FamilyCode.LANDING and ex.difficulty >= 3:
            return True
        if ex.family == FamilyCode.PLYO and ex.difficulty >= 4:
            return True
        if ex.family == FamilyCode.DLKD and ex.difficulty >= 4:
            if "depth" in name_lower or "drop" in name_lower:
                return True

    # Shoulder overhead risk
    if profile.shoulder_overhead_risk:
        if ex.family == FamilyCode.VPUSH and ex.difficulty >= 3:
            return True
        if ex.family == FamilyCode.VPULL and ex.difficulty >= 4:
            if "pull-up" in name_lower or "pullup" in name_lower or "chin-up" in name_lower:
                return True

    # Hamstring risk
    if profile.hamstring_risk:
        if ex.family == FamilyCode.DLHD:
            if ("rdl" in name_lower or "good morning" in name_lower
                    or "stiff leg" in name_lower or "stiff-leg" in name_lower
                    or "straight-leg" in name_lower):
                return True
            if ex.eccentric_cost >= 4:
                return True
        if ex.family == FamilyCode.SPRINT and ex.difficulty >= 4:
            return True

    # Groin / adductor risk
    if profile.groin_adductor_risk:
        if ex.family == FamilyCode.SPRINT:
            if "lateral" in name_lower or "crossover" in name_lower or "shuffle" in name_lower:
                return True
        if ex.family == FamilyCode.SLKD and ex.difficulty >= 4:
            if "lateral" in name_lower:
                return True

    # Ankle / foot risk
    if profile.ankle_foot_risk:
        if ex.family == FamilyCode.PLYO and ex.difficulty >= 4:
            return True
        if ex.family == FamilyCode.LANDING and ex.difficulty >= 4:
            if "single-leg" in name_lower or "single leg" in name_lower:
                return True
        if ex.family == FamilyCode.SPRINT and ex.difficulty >= 4:
            if "max" in name_lower or "flying" in name_lower:
                return True

    return False


def filter_exercises_for_athlete(
    candidates: list[Exercise],
    profile: AthleteProfile,
) -> list[Exercise]:
    """Remove exercises that conflict with athlete risk flags."""
    if not _has_risk_flags(profile):
        return candidates
    return [ex for ex in candidates if not is_exercise_risk_flagged(ex, profile)]


def _has_risk_flags(profile: AthleteProfile) -> bool:
    return any([
        profile.lumbar_risk,
        profile.patellar_tendon_risk,
        profile.hamstring_risk,
        profile.shoulder_overhead_risk,
        profile.groin_adductor_risk,
        profile.ankle_foot_risk,
    ])


# ── Exercise scoring wrapper (for sort-based personalization) ──────

def score_exercise_for_athlete(ex: Exercise, profile: AthleteProfile) -> int:
    """Combined score: risk filter + personalization bias.

    Risk-flagged exercises get -10 (ensured last).
    Otherwise base score + bias.
    """
    if _has_risk_flags(profile) and is_exercise_risk_flagged(ex, profile):
        return -10
    return get_exercise_personalization_bias(ex, profile)


def personalize_exercise_list(
    exercises: list[Exercise],
    profile: AthleteProfile,
) -> list[Exercise]:
    """Sort exercises by athlete fit (best first)."""
    return sorted(exercises, key=lambda ex: -score_exercise_for_athlete(ex, profile))


# ── Part 3: Conditioning Personalization ───────────────────────────

def score_conditioning_for_athlete(
    proto: ConditioningProtocol,
    profile: AthleteProfile,
) -> int:
    """Return a bias score for this conditioning protocol given athlete profile.

    Higher = better fit. 0 = neutral. Negative = worse fit.
    """
    score = 0
    cp = profile.conditioning_profile

    # Conditioning profile bias
    if cp == "poor":
        if proto.fatigue_score <= 2:
            score += 1
        if proto.fatigue_score >= 4:
            score -= 1
    elif cp == "strong":
        if proto.fatigue_score >= 3:
            score += 1

    # Elastic / landing bias
    lp = profile.landing_competency
    if lp == "poor":
        if proto.impact_level >= 4:
            score -= 1
        if proto.environment_category in ("court", "field") and proto.impact_level <= 3:
            score += 1
    if profile.patellar_tendon_risk or profile.ankle_foot_risk:
        if proto.impact_level >= 4:
            score -= 2

    # Hamstring risk → reduce max sprint density in conditioning
    if profile.hamstring_risk:
        if proto.system == "Repeated Sprint Ability":
            score -= 1
        if proto.system == "Speed Endurance":
            score -= 1
        if proto.movement_profile in ("linear_rsa", "linear_speed_endurance"):
            score -= 1

    # Groin risk → reduce hard lateral COD
    if profile.groin_adductor_risk:
        if proto.movement_profile in ("change_of_direction", "court_shuffle"):
            score -= 1

    # Lumbar risk → avoid trunk-loaded gym conditioning
    if profile.lumbar_risk:
        if proto.environment_category == "gym":
            score -= 1

    # Test band bias
    if profile.sprint_10m_band == "low" and proto.system in ("Alactic Speed", "Speed Endurance"):
        score -= 1
    if profile.aerobic_band == "low" and proto.system in ("Aerobic Capacity", "Aerobic Power"):
        score -= 1

    return score


def personalize_conditioning_protocols(
    protocols: list[ConditioningProtocol],
    profile: AthleteProfile,
) -> list[ConditioningProtocol]:
    """Sort conditioning protocols by athlete fit (best first)."""
    if not _has_personalization_flags(profile):
        return protocols
    return sorted(protocols, key=lambda p: -score_conditioning_for_athlete(p, profile))


def _has_personalization_flags(profile: AthleteProfile) -> bool:
    return any([
        profile.conditioning_profile,
        profile.landing_competency,
        profile.patellar_tendon_risk,
        profile.ankle_foot_risk,
        profile.hamstring_risk,
        profile.groin_adductor_risk,
        profile.lumbar_risk,
        profile.sprint_10m_band,
        profile.aerobic_band,
    ])


# ── Part 4: Weekly Focus Bias ──────────────────────────────────────

def get_weekly_emphasis_bias(profile: AthleteProfile) -> dict:
    """Return a small dict of weekly emphasis modifiers based on athlete profile.

    Returns:
        dict with optional keys:
        - more_lower_strength: bool (bias toward squat/hinge volume)
        - less_plyo_density: bool (reduce plyo exposure)
        - more_landing_prep: bool (increase landing mechanics exposure)
        - less_hinge_rotation: bool (reduce hinge/rotation combo)
        - less_overhead: bool (reduce overhead pushing/pulling)
        - more_sprint_drills: bool (prefer sprint drills over max v)
        - less_sprint_density: bool (reduce total sprint exposure)
        - less_impact_cond: bool (prefer low-impact conditioning)
        - less_lateral_cod: bool (reduce lateral COD work)
    """
    bias: dict = {}
    fp = profile.force_profile
    lp = profile.landing_competency
    sm = profile.sprint_mechanics_competency

    if fp == "force_deficient":
        bias["more_lower_strength"] = True
    elif fp == "velocity_deficient":
        bias["more_explosive_emphasis"] = True

    if lp == "poor":
        bias["more_landing_prep"] = True
        bias["less_plyo_density"] = True
    elif lp == "strong":
        bias["less_plyo_density"] = False

    if sm == "poor":
        bias["more_sprint_drills"] = True
        bias["less_sprint_density"] = True
    elif sm == "strong":
        bias["less_sprint_density"] = False

    if profile.lumbar_risk:
        bias["less_hinge_rotation"] = True

    if profile.shoulder_overhead_risk:
        bias["less_overhead"] = True

    if profile.hamstring_risk:
        bias["less_sprint_density"] = True

    if profile.groin_adductor_risk:
        bias["less_lateral_cod"] = True

    if profile.patellar_tendon_risk or profile.ankle_foot_risk:
        bias["less_plyo_density"] = True
        bias["less_impact_cond"] = True

    return bias


# ── WAVE 6: ROLE-BASED WEEKLY BIAS ──────────────────────────────

ROLE_WEEKLY_NOTES: dict[str, dict[str, list[str]]] = {
    "cricket": {
        "fast_bowler": [
            "Fast bowler role -> sprint & unilateral emphasis; lumbar-friendly hinge dosing",
            "Fast bowler -> shoulder support work prioritised",
        ],
        "spinner": [
            "Spinner role -> rotational control & repeatability emphasis",
        ],
        "batter": [
            "Batter role -> rotational power & upper-body ballistic support",
        ],
        "wicketkeeper": [
            "Wicketkeeper role -> squat isometric & lateral coverage emphasis",
        ],
    },
    "rugby": {
        "prop": [
            "Prop role -> maximal force & collision robustness emphasis",
        ],
        "lock": [
            "Lock role -> jump-landing & scrum force emphasis",
        ],
        "back_row": [
            "Back-row role -> hybrid force & repeat-running emphasis",
        ],
        "halfback": [
            "Halfback role -> speed-power & agility emphasis",
        ],
        "backline": [
            "Backline role -> speed-power & elastic emphasis",
        ],
    },
    "tennis": {
        "singles": [
            "Singles role -> court conditioning & repeat COD emphasis",
        ],
        "doubles": [
            "Doubles role -> explosive first-step & serve-volley emphasis",
        ],
    },
    "badminton": {
        "singles": [
            "Singles role -> repeat lunge & court coverage emphasis",
        ],
        "doubles": [
            "Doubles role -> explosive short-burst & jump-smash emphasis",
        ],
    },
    "volleyball": {
        "middle": [
            "Middle role -> jump-landing & block-jump emphasis",
        ],
        "outside": [
            "Outside role -> approach jump & shoulder management emphasis",
        ],
        "setter": [
            "Setter role -> footwork & overhead tolerance emphasis",
        ],
        "libero": [
            "Libero role -> lateral coverage & low-overhead bias",
        ],
    },
    "soccer": {
        "goalkeeper": [
            "Goalkeeper role -> lateral dive & explosive push emphasis",
        ],
        "defender": [
            "Defender role -> accel/decel & duel robustness emphasis",
        ],
        "midfielder": [
            "Midfielder role -> conditioning density & repeat running emphasis",
        ],
        "forward": [
            "Forward role -> acceleration & finishing power emphasis",
        ],
    },
}


# Role → family bias map: +2 strong prefer, +1 prefer, -1 avoid, -2 strongly avoid
_ROLE_EXERCISE_BIAS: dict[str, dict[str, dict[str, int]]] = {
    "cricket": {
        "fast_bowler": {
            "DLKD": 1, "DLHD": -1,  # Preserve squat, reduce hinge fatigue
            "SLKD": 1, "SLHD": 1,   # Prefer unilateral
            "Sprint": 1, "Landing": 1,
            "Rot": -1,             # Reduce aggressive rotation
            "VPush": -1,           # Reduce overhead
            "Core": 1,
            "Acc": 1,
        },
        "spinner": {
            "Rot": 1, "Core": 1,
            "Sprint": -1,           # Less top-speed sprint
            "HPush": 1, "HPull": 1,
        },
        "batter": {
            "Rot": 1, "Ball": 1,
            "HPush": 1, "HPull": 1,
            "Sprint": 1,
        },
        "wicketkeeper": {
            "DLKD": 1, "SLKD": 1,   # Low squat stance
            "Sprint": -1, "Plyo": -1,
            "Core": 1, "Rot": 1,
            "Landing": 1,
        },
    },
    "rugby": {
        "prop": {
            "DLKD": 2, "DLHD": 1, "HPush": 2, "HPull": 1,
            "Plyo": -1, "Sprint": -1,
            "Core": 2, "Carry": 2,
        },
        "lock": {
            "DLKD": 2, "DLHD": 1,
            "Plyo": 1, "Landing": 1,
            "HPush": 1, "Core": 1, "Carry": 1,
        },
        "back_row": {
            "DLKD": 1, "DLHD": 1,
            "Sprint": 1, "Sprint": 1,
            "Core": 1, "Carry": 1,
        },
        "halfback": {
            "Sprint": 1, "Ball": 1,
            "SLKD": 1, "SLHD": 1,
            "Core": 1,
        },
        "backline": {
            "Sprint": 2, "Plyo": 1, "Ball": 1,
            "DLKD": -1,
            "Core": 1,
        },
    },
    "tennis": {
        "singles": {
            "Sprint": 1, "Landing": 1,
            "SLKD": 1, "SLHD": 1,
            "Core": 1, "Rot": 1,
            "VPush": -1,           # Overhead volume concern
        },
        "doubles": {
            "Plyo": 1, "Ball": 1,
            "Sprint": -1,
            "VPush": 1, "VPull": 1,
        },
    },
    "badminton": {
        "singles": {
            "Sprint": 1, "Landing": 1,
            "SLKD": 2, "SLHD": 1,
            "Core": 1,
        },
        "doubles": {
            "Plyo": 1, "Ball": 1,
            "VPush": 1, "VPull": 1,
            "SLKD": 1,
        },
    },
    "volleyball": {
        "middle": {
            "Plyo": 2, "Landing": 2,
            "DLKD": 1,
            "VPush": 1, "VPull": 1,
            "Core": 1,
        },
        "outside": {
            "Plyo": 1, "Landing": 1,
            "HPush": 1, "HPull": 1,
            "Rot": 1, "Core": 1,
        },
        "setter": {
            "SLKD": 1, "SLHD": 1,
            "VPush": -1,
            "Core": 1, "Sprint": -1,
        },
        "libero": {
            "Landing": 1,
            "SLKD": 1, "SLHD": 1,
            "Sprint": 1,
            "VPush": -1, "VPull": -1,
        },
    },
    "soccer": {
        "goalkeeper": {
            "Plyo": 2, "Landing": 2,
            "Ball": 1,
            "SLKD": 1, "SLHD": 1,
            "VPush": -1, "VPull": -1,
            "Sprint": -1,
        },
        "defender": {
            "DLKD": 1, "DLHD": 1,
            "Sprint": 1,
            "Core": 1, "Carry": 1,
        },
        "midfielder": {
            "Sprint": 1,
            "SLKD": 1, "SLHD": 1,
            "Core": 1,
        },
        "forward": {
            "Sprint": 2, "Plyo": 1, "Ball": 1,
            "Landing": 1,
            "DLKD": -1,
        },
    },
}


def get_role_exercise_bias(
    role_key: str,
    family: str | FamilyCode,
    sport: str,
) -> int:
    """Return a bias score (-2 to +2) for an exercise family based on sport role."""
    family_key = family.value if isinstance(family, FamilyCode) else family
    biases = _ROLE_EXERCISE_BIAS.get(sport, {}).get(role_key, {})
    return biases.get(family_key, 0)


def get_role_weekly_notes(sport: str, role: str) -> list[str]:
    """Return weekly emphasis notes for a specific sport role."""
    if not role:
        return []
    return ROLE_WEEKLY_NOTES.get(sport.lower(), {}).get(role.lower(), [])


def describe_weekly_bias(bias: dict) -> list[str]:
    """Generate human-readable notes from a weekly emphasis bias dict."""
    notes = []
    if bias.get("more_lower_strength"):
        notes.append("Force-deficient profile -> increased lower-strength emphasis")
    if bias.get("more_explosive_emphasis"):
        notes.append("Velocity-deficient profile -> increased explosive/power emphasis")
    if bias.get("more_landing_prep"):
        notes.append("Landing competency poor -> advanced reactive plyos capped; landing prep added")
    if bias.get("less_plyo_density"):
        notes.append("Plyo density reduced per athlete profile")
    if bias.get("less_hinge_rotation"):
        notes.append("Lumbar risk -> high-eccentric hinges reduced; rotation exposure moderated")
    if bias.get("less_overhead"):
        notes.append("Shoulder overhead risk -> overhead volume modified")
    if bias.get("more_sprint_drills"):
        notes.append("Sprint mechanics poor -> additional drill-based sprint exposure")
    if bias.get("less_sprint_density"):
        notes.append("Sprint density reduced per athlete profile")
    if bias.get("less_impact_cond"):
        notes.append("Impact/tendon risk -> lower-impact conditioning preferred")
    if bias.get("less_lateral_cod"):
        notes.append("Groin/adductor risk -> lateral COD work reduced")
    return notes
