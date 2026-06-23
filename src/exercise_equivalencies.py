# Exercise Equivalency Data Layer
# Maps source exercises to equivalent substitutes with scoring and rationale.

from typing import List, Dict, Any

# Schema:
# source_exercise_id -> target_exercise_id
# equivalency_score: 1-10 (10 = perfect substitute, preserves all intent)
# reason: why this equivalency is valid

EXERCISE_EQUIVALENCIES: List[Dict[str, Any]] = [
    # Trap Bar Jump Squat equivalents
    {
        "source_exercise_name": "Trap Bar Jump Squat",
        "target_exercise_name": "Barbell Jump Squat",
        "equivalency_score": 9.0,
        "reason": "Same explosive bilateral squat pattern. Barbell replaces trap bar. Slightly higher spinal loading but identical force-velocity profile."
    },
    {
        "source_exercise_name": "Trap Bar Jump Squat",
        "target_exercise_name": "Kettlebell Swing",
        "equivalency_score": 6.5,
        "reason": "Both develop explosive hip extension but different loading pattern and force vector. Acceptable substitute when no jump variation is available."
    },
    # Power Clean equivalents
    {
        "source_exercise_name": "Power Clean",
        "target_exercise_name": "Hang Clean",
        "equivalency_score": 9.5,
        "reason": "Same catch mechanics and force curve. Hang clean starts from mid-thigh (removes floor pull). Nearly identical power output and RFD stimulus."
    },
    {
        "source_exercise_name": "Power Clean",
        "target_exercise_name": "Clean Pull",
        "equivalency_score": 8.5,
        "reason": "Same explosive triple extension without catch. Slightly lower skill demand but identical force production through the pull phase."
    },
    {
        "source_exercise_name": "Power Clean",
        "target_exercise_name": "Mid-Thigh Pull",
        "equivalency_score": 7.5,
        "reason": "No catch required, but mid-thigh pull delivers the highest RFD stimulus among derivatives. Good substitute for power development without catch complexity."
    },
    # Push Jerk equivalents
    {
        "source_exercise_name": "Push Jerk",
        "target_exercise_name": "Push Press",
        "equivalency_score": 8.5,
        "reason": "Same dip-drive overhead pattern. Push press has no re-bend (simpler receiving position). Slightly lower power demand but identical movement intent."
    },
    {
        "source_exercise_name": "Push Jerk",
        "target_exercise_name": "Split Jerk",
        "equivalency_score": 9.0,
        "reason": "Same overhead receiving intent. Split jerk uses split stance for stability. Higher technical demand but equivalent power output."
    },
    # Split Jerk equivalents
    {
        "source_exercise_name": "Split Jerk",
        "target_exercise_name": "Push Jerk",
        "equivalency_score": 8.5,
        "reason": "Same overhead intent. Push jerk uses quarter-squat catch instead of split. Good regression when split stance stability is limited."
    },
    {
        "source_exercise_name": "Split Jerk",
        "target_exercise_name": "Push Press",
        "equivalency_score": 7.0,
        "reason": "Simpler overhead pattern without re-bend catch. Acceptable when full jerk technique is not yet developed."
    },
    # Medicine Ball Rotational equivalents
    {
        "source_exercise_name": "Medicine Ball Rotational Scoop Toss",
        "target_exercise_name": "Medicine Ball Rotational Chest Pass",
        "equivalency_score": 8.5,
        "reason": "Same rotational power intent. Scoop toss emphasizes upward trajectory, chest pass emphasizes horizontal velocity. Excellent rotational substitute."
    },
    {
        "source_exercise_name": "Medicine Ball Rotational Scoop Toss",
        "target_exercise_name": "Medicine Ball Overhead Backwards Toss",
        "equivalency_score": 6.5,
        "reason": "Different force vector (overhead vs rotational). Still develops explosive power but misses rotational specificity."
    },
    # Barbell Back Squat equivalents
    {
        "source_exercise_name": "Barbell Back Squat",
        "target_exercise_name": "Rear Foot Elevated Split Squat",
        "equivalency_score": 7.5,
        "reason": "Same squat pattern with unilateral emphasis. RFESS reduces load but adds stability demand. Good substitute when bilateral loading is contraindicated."
    },
    {
        "source_exercise_name": "Barbell Back Squat",
        "target_exercise_name": "Overhead Squat",
        "equivalency_score": 6.0,
        "reason": "Same squat mechanics but with overhead bar position. Drastically different stability demand and load capacity. Acceptable only for experienced athletes."
    },
    # Trap Bar Deadlift equivalents
    {
        "source_exercise_name": "Trap Bar Deadlift",
        "target_exercise_name": "Kettlebell Swing",
        "equivalency_score": 7.0,
        "reason": "Both develop posterior chain hip drive. Deadlift allows heavier loading, swing emphasizes velocity. Good substitute for power-focused sessions."
    },
    {
        "source_exercise_name": "Trap Bar Deadlift",
        "target_exercise_name": "Clean Pull",
        "equivalency_score": 7.5,
        "reason": "Both are bilateral posterior chain pulls. Clean pull from floor has similar hip hinge mechanics. Good substitute for strength-power development."
    },
    # Nordic Hamstring Curl equivalents
    {
        "source_exercise_name": "Nordic Hamstring Curl",
        "target_exercise_name": "Single-Leg Isometric Wall Sit",
        "equivalency_score": 5.0,
        "reason": "Both target posterior chain and knee flexors. Different mechanics but similar eccentric hamstring loading. Acceptable when Nordic contraindicated."
    },
    # Single-Leg Lateral Bound equivalents
    {
        "source_exercise_name": "Single-Leg Lateral Bound",
        "target_exercise_name": "Depth Jump",
        "equivalency_score": 6.0,
        "reason": "Both are plyometric. Bound is lateral and unilateral, depth jump is bilateral and vertical. Different force vector but same explosive intent."
    },
    # Dumbbell Overhead Press equivalents
    {
        "source_exercise_name": "Dumbbell Overhead Press",
        "target_exercise_name": "Push Press",
        "equivalency_score": 7.5,
        "reason": "Same overhead pressing pattern. Push press adds leg drive for heavier loading. Good substitute for developing overhead strength with barbell."
    },
    # Power Snatch equivalents
    {
        "source_exercise_name": "Power Snatch",
        "target_exercise_name": "Hang Snatch",
        "equivalency_score": 9.0,
        "reason": "Same snatch mechanics. Hang version starts from mid-thigh. Nearly identical overhead receiving position and force production."
    },
    {
        "source_exercise_name": "Power Snatch",
        "target_exercise_name": "Snatch Pull",
        "equivalency_score": 7.5,
        "reason": "Same wide-grip pull pattern without overhead catch. Good technical progression for athletes developing snatch mechanics."
    },
]


def get_equivalencies_by_source(source_exercise_name: str) -> List[Dict[str, Any]]:
    return [e for e in EXERCISE_EQUIVALENCIES if e["source_exercise_name"] == source_exercise_name]


def get_equivalency(source_exercise_name: str, target_exercise_name: str) -> Dict[str, Any]:
    for e in EXERCISE_EQUIVALENCIES:
        if e["source_exercise_name"] == source_exercise_name and e["target_exercise_name"] == target_exercise_name:
            return e
    return None
