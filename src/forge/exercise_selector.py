"""Exercise selection engine."""
from typing import Optional
from .models import (
    Exercise, FamilyCode, AthleteLevel, EquipmentProfile, AthleteProfile,
)
from .data import (
    EXERCISE_BY_ID, EXERCISES_BY_FAMILY, SELECTION_PRIORITIES,
    get_max_difficulty, get_equipment_for_profile
)
from .substitution_engine import substitute_exercise
from .conditioning_engine import (
    EXERCISE_COMP_MAX_FATIGUE, EXERCISE_COMP_MAX_IMPACT, EXERCISE_COMP_MAX_ECCENTRIC,
    _resolve_comp_window,
)
from .injury_map import has_injury_conflict
from .athlete_profile_rules import (
    is_exercise_risk_flagged, get_exercise_personalization_bias,
)


def select_exercise(
    slot_family: FamilyCode,
    athlete_level: AthleteLevel,
    equipment_profile: EquipmentProfile,
    recent_exercises: dict[str, dict],
    injury_history: list[str],
    days_to_match: Optional[int] = None,
    technique_consistency: float = 1.0,
    strength_base_met: bool = True,
    athlete_profile: Optional[AthleteProfile] = None,
) -> Optional[Exercise]:
    comp_window = _resolve_comp_window(days_to_match)
    max_diff = get_max_difficulty(athlete_level.value)
    available_equip = get_equipment_for_profile(equipment_profile.value)

    # Technique gate: force regression-level difficulty when mastery is low
    if technique_consistency < 0.8:
        max_diff = min(max_diff, 1)

    # Bilateral→unilateral gate: downgrade single-leg to double-leg if base not met
    effective_family = slot_family
    if not strength_base_met:
        if slot_family == FamilyCode.SLKD:
            effective_family = FamilyCode.DLKD
        elif slot_family == FamilyCode.SLHD:
            effective_family = FamilyCode.DLHD

    priority_ids = SELECTION_PRIORITIES.get(effective_family.value, [])

    candidates = []
    for eid in priority_ids:
        ex = EXERCISE_BY_ID.get(eid)
        if ex is None:
            continue
        if ex.difficulty > max_diff:
            continue
        if not _equipment_available(ex, available_equip):
            continue
        if has_injury_conflict(ex.name, injury_history):
            continue
        if not _exercise_competition_ok(ex, comp_window):
            continue
        if athlete_profile and is_exercise_risk_flagged(ex, athlete_profile):
            continue
        candidates.append(ex)

    if not candidates:
        return substitute_exercise(
            effective_family if effective_family != slot_family else slot_family,
            athlete_level, equipment_profile,
            injury_history, recent_exercises, None, days_to_match,
            athlete_profile=athlete_profile,
        )

    if athlete_profile and (athlete_profile.force_profile or athlete_profile.elastic_profile
            or athlete_profile.landing_competency or athlete_profile.sprint_mechanics_competency):
        scored = [(ex, get_exercise_personalization_bias(ex, athlete_profile)) for ex in candidates]
        scored.sort(key=lambda x: (-x[1], _recent_score(x[0], recent_exercises)))
        return scored[0][0]

    return _least_recently_used(candidates, recent_exercises)


def _exercise_competition_ok(ex: Exercise, window: int) -> bool:
    """Check if an exercise is allowed in the given competition window."""
    if window is None:
        return True
    max_fatigue = EXERCISE_COMP_MAX_FATIGUE.get(window, 5)
    max_impact = EXERCISE_COMP_MAX_IMPACT.get(window, 5)
    max_eccentric = EXERCISE_COMP_MAX_ECCENTRIC.get(window, 5)
    if ex.fatigue_cost > max_fatigue:
        return False
    if ex.impact_level > max_impact:
        return False
    if ex.eccentric_cost > max_eccentric:
        return False
    return True


def _equipment_available(exercise: Exercise, available_equip: list[str]) -> bool:
    for eq in exercise.equipment:
        eq_lower = eq.lower()
        if not any(e.lower() in eq_lower or eq_lower in e.lower() for e in available_equip):
            return False
    return True


def _recent_score(ex: Exercise, recent_exercises: dict) -> int:
    if ex.id in recent_exercises:
        last = recent_exercises[ex.id].get("last_used", "")
        if "week" in str(last) or "day" in str(last):
            return 1
    return -1


def _least_recently_used(
    candidates: list[Exercise], recent_exercises: dict[str, dict]
) -> Exercise:
    scored = []
    for ex in candidates:
        if ex.id in recent_exercises:
            last = recent_exercises[ex.id].get("last_used", "")
            score = 0
            if "week" in str(last) or "day" in str(last):
                score = 1
        else:
            score = -1
        scored.append((score, ex))
    scored.sort(key=lambda x: x[0])
    return scored[0][1]
