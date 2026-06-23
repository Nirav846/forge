# Exercise Classification Utilities
# Standalone module to avoid circular imports between recommendation_engine and exercise_substitution_engine.

from typing import Dict, Any


def classify_exercise(ex: Dict[str, Any]) -> str:
    """Determine exercise_class from exercise metadata."""
    name_lower = ex.get("name", "").lower()
    force_type = ex.get("force_type", "")
    mechanics_type = ex.get("mechanics_type", "")

    # Olympic lifts
    olympic_names = ["power clean", "hang clean", "squat clean", "clean and jerk",
                     "power snatch", "hang snatch", "snatch balance", "clean pull",
                     "mid-thigh pull", "high pull", "snatch pull", "push jerk",
                     "split jerk", "push press"]
    for name in olympic_names:
        if name in name_lower:
            return "Olympic Lift"

    # Ballistic (loaded jumps — before plyometric to catch "jump squat" specifically)
    if "jump squat" in name_lower:
        return "Ballistic"

    # Medicine ball
    if "medicine ball" in name_lower or "mb " in name_lower or name_lower.startswith("mb "):
        return "Medicine Ball"

    # Plyometric (unloaded jumps, bounds, hops)
    if any(w in name_lower for w in ["bound", "hop", "depth jump", "skip"]):
        return "Plyometric"

    # Isometric
    if any(w in name_lower for w in ["plank", "isometric", "wall sit"]):
        return "Isometric"

    # Sprint
    if any(w in name_lower for w in ["sprint", "a-skip", "b-skip"]):
        return "Sprint Drill"

    # Core
    if any(w in name_lower for w in ["pallof", "rotation", "anti-rotat"]):
        return "Core Stability"

    # Max Strength
    strength_names = ["deadlift", "squat", "press", "row", "bench", "clean", "snatch", "curl", "extension"]
    if any(s in name_lower for s in strength_names):
        return "Max Strength"

    # Accessory fallback
    return "Accessory"


def determine_primary_adaptation(ex: Dict[str, Any]) -> str:
    """Determine primary adaptation from exercise metadata."""
    ex_class = ex.get("exercise_class", classify_exercise(ex))
    name_lower = ex.get("name", "").lower()

    if ex_class == "Olympic Lift":
        return "Power"
    if ex_class == "Plyometric":
        return "Power"
    if ex_class == "Medicine Ball":
        if "rotational" in name_lower or "scoop" in name_lower:
            return "Rotational Power"
        return "Power"
    if ex_class == "Max Strength":
        if "nordic" in name_lower:
            return "Eccentric Control"
        return "Strength"
    if ex_class == "Isometric":
        return "Stability"
    if ex_class == "Core Stability":
        return "Stability"
    if ex_class == "Sprint Drill":
        return "Acceleration"
    return "Strength"


def determine_force_vector(ex: Dict[str, Any]) -> str:
    """Determine force vector from exercise metadata."""
    force_type = ex.get("force_type", "")
    name_lower = ex.get("name", "").lower()
    ex_class = ex.get("exercise_class", classify_exercise(ex))

    if "rotational" in name_lower or "rotation" in name_lower or force_type == "Rotation":
        return "Rotational"
    if any(w in name_lower for w in ["lateral", "side"]):
        return "Lateral"
    if any(w in name_lower for w in ["bound", "hop"]):
        return "Lateral"
    if ex_class in ("Olympic Lift", "Plyometric", "Sprint Drill"):
        return "Vertical"
    if ex_class == "Medicine Ball":
        return "Horizontal"
    return "Axial"
