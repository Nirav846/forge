"""Shared injury-exercise conflict maps — single source of truth."""

INJURY_EXERCISE_MAP: dict[str, list[str]] = {
    "low_back": ["Conventional Deadlift", "Barbell Row", "Barbell Good Morning", "Good Morning"],
    "acl_left": ["Depth Jump", "Pistol Squat", "Single-Leg Depth Jump"],
    "acl_right": ["Depth Jump", "Pistol Squat", "Single-Leg Depth Jump"],
    "shoulder": ["Barbell Bench Press", "Barbell Overhead Press", "Muscle-Up"],
    "patellar": ["Depth Jump", "Pistol Squat", "Bulgarian Split Squat"],
    "hamstring": ["Conventional Deadlift", "RDL", "Nordic Hamstring Curl", "Stiff-Leg Deadlift"],
}


def has_injury_conflict(exercise_name: str, injury_history: list[str]) -> bool:
    for injury in injury_history:
        for key in INJURY_EXERCISE_MAP:
            if key in injury.lower():
                if exercise_name in INJURY_EXERCISE_MAP[key]:
                    return True
    return False


def injury_risk_multiplier(exercise_name: str, injury_history: list[str]) -> float:
    return 0.0 if has_injury_conflict(exercise_name, injury_history) else 1.0
