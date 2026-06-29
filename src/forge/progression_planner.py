"""Weekly progression planning — volume, intensity, density, complexity, velocity, eccentric per week."""

from typing import Optional
from .models import AthleteProfile, WeeklyProgressionPlan, SeasonPhase


WEEK_TYPE_PROGRESSION = {
    "accumulation": {"volume_mod": 1.1, "intensity_mod": 0.85, "density_mod": 0.9, "complexity": 2, "velocity": "controlled", "eccentric": 1.0},
    "intensification": {"volume_mod": 1.0, "intensity_mod": 1.0, "density_mod": 1.0, "complexity": 3, "velocity": "controlled", "eccentric": 1.1},
    "realization": {"volume_mod": 0.85, "intensity_mod": 1.05, "density_mod": 1.1, "complexity": 4, "velocity": "explosive", "eccentric": 0.8},
    "peak": {"volume_mod": 0.9, "intensity_mod": 1.0, "density_mod": 1.0, "complexity": 4, "velocity": "explosive", "eccentric": 0.9},
    "taper": {"volume_mod": 0.7, "intensity_mod": 0.9, "density_mod": 0.8, "complexity": 3, "velocity": "controlled", "eccentric": 0.7},
    "test": {"volume_mod": 0.6, "intensity_mod": 0.8, "density_mod": 0.7, "complexity": 2, "velocity": "controlled", "eccentric": 0.5},
    "deload": {"volume_mod": 0.6, "intensity_mod": 0.8, "density_mod": 0.8, "complexity": 2, "velocity": "controlled", "eccentric": 0.6},
    "light": {"volume_mod": 0.5, "intensity_mod": 0.7, "density_mod": 0.7, "complexity": 1, "velocity": "controlled", "eccentric": 0.5},
}

ROLE_PROGRESSION_MODIFIERS = {
    "Fast Bowler": {"eccentric": 1.3, "complexity_bump": 1},
    "Batter": {"velocity_override": "explosive", "volume": 0.9},
    "Spin Bowler": {"intensity": 0.9, "density": 0.9},
    "Wicketkeeper": {"eccentric": 0.8, "volume": 0.9},
    "All Rounder": {"volume": 1.0, "intensity": 1.0},
}


def _level_adjustments(level: str, week_type: str) -> dict:
    if level == "Beginner":
        return {"complexity_bump": -1, "intensity": 0.85, "volume": 1.1}
    elif level == "Advanced":
        return {"complexity_bump": 1, "intensity": 1.05, "volume": 0.85}
    return {"complexity_bump": 0, "intensity": 1.0, "volume": 1.0}


def _role_adjustments(role_name: str) -> dict:
    for key, mods in ROLE_PROGRESSION_MODIFIERS.items():
        if key in role_name:
            return mods
    return {}


def _calendar_adjustments(athlete_profile: AthleteProfile) -> dict:
    result = {}
    if athlete_profile.season_phase == SeasonPhase.IN_SEASON:
        result["volume"] = 0.7
        result["intensity"] = 1.0
        result["density"] = 0.8
    if athlete_profile.days_to_match is not None and 1 <= athlete_profile.days_to_match <= 5:
        taper = 1.0 - (1.0 - 0.6) * (1.0 - (athlete_profile.days_to_match - 1) / 4.0)
        result["volume"] = result.get("volume", 1.0) * taper
        result["intensity"] = result.get("intensity", 1.0) * (1.0 + (1.0 - taper) * 0.3)
        result["density"] = result.get("density", 1.0) * (0.8 + 0.2 * taper)
    return result


def plan_weekly_progression(
    week_type: str,
    week_number: int,
    athlete: AthleteProfile,
    role_name: str = "",
) -> WeeklyProgressionPlan:
    # 1. Base progression from week type
    base = WEEK_TYPE_PROGRESSION.get(week_type, WEEK_TYPE_PROGRESSION["accumulation"])

    # 2. Level adjustments
    level_mods = _level_adjustments(athlete.athlete_level.value, week_type)

    # 3. Role adjustments
    role_mods = _role_adjustments(role_name or athlete.role)

    # 4. Calendar adjustments
    cal_mods = _calendar_adjustments(athlete)

    # 5. Combine
    volume = base["volume_mod"] * level_mods.get("volume", 1.0) * role_mods.get("volume", 1.0) * cal_mods.get("volume", 1.0)
    intensity = base["intensity_mod"] * level_mods.get("intensity", 1.0) * role_mods.get("intensity", 1.0) * cal_mods.get("intensity", 1.0)
    density = base["density_mod"] * level_mods.get("density", 1.0) * role_mods.get("density", 1.0) * cal_mods.get("density", 1.0)
    complexity = base["complexity"] + level_mods.get("complexity_bump", 0) + role_mods.get("complexity_bump", 0)
    velocity = role_mods.get("velocity_override", base["velocity"])
    eccentric = base["eccentric"] * level_mods.get("eccentric", 1.0) * role_mods.get("eccentric", 1.0) * cal_mods.get("eccentric", 1.0)

    # Clamp
    volume = max(0.5, min(1.4, volume))
    intensity = max(0.7, min(1.15, intensity))
    density = max(0.6, min(1.3, density))
    complexity = max(1, min(5, int(round(complexity))))
    eccentric = max(0.3, min(1.6, eccentric))

    return WeeklyProgressionPlan(
        volume_modifier=round(volume, 2),
        intensity_modifier=round(intensity, 2),
        density_modifier=round(density, 2),
        complexity_level=complexity,
        velocity_emphasis=velocity,
        eccentric_emphasis=round(eccentric, 2),
    )
