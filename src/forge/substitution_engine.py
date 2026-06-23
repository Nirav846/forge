"""Substitution engine — 4-priority chain fallback."""
from typing import Optional
from .models import (
    Exercise, FamilyCode, AthleteLevel, EquipmentProfile, AthleteProfile,
)
from .data import (
    EXERCISE_BY_ID, EXERCISES_BY_FAMILY, SELECTION_PRIORITIES,
    CROSS_FAMILY_SUBSTITUTION, INTENT_CATEGORIES, FAMILY_TO_INTENT,
    get_max_difficulty, get_equipment_for_profile,
)
from .models import Exercise as Ex
from .conditioning_engine import (
    EXERCISE_COMP_MAX_FATIGUE, EXERCISE_COMP_MAX_IMPACT, EXERCISE_COMP_MAX_ECCENTRIC,
    _resolve_comp_window,
)
from .injury_map import has_injury_conflict as _inj_conflict
from .athlete_profile_rules import is_exercise_risk_flagged


def _ex_comp_ok(ex: Exercise, window: int) -> bool:
    if window is None:
        return True
    if ex.fatigue_cost > EXERCISE_COMP_MAX_FATIGUE.get(window, 5):
        return False
    if ex.impact_level > EXERCISE_COMP_MAX_IMPACT.get(window, 5):
        return False
    if ex.eccentric_cost > EXERCISE_COMP_MAX_ECCENTRIC.get(window, 5):
        return False
    return True


def substitute_exercise(
    family: FamilyCode,
    athlete_level: AthleteLevel,
    equipment_profile: EquipmentProfile,
    injury_history: list[str],
    recent_exercises: dict[str, dict],
    current_exercise_id: Optional[str] = None,
    days_to_match: Optional[int] = None,
    athlete_profile: Optional[AthleteProfile] = None,
) -> Optional[Exercise]:
    comp_window = _resolve_comp_window(days_to_match)
    max_diff = get_max_difficulty(athlete_level.value)
    available_equip = get_equipment_for_profile(equipment_profile.value)
    priority_ids = SELECTION_PRIORITIES.get(family.value, [])

    # Priority 1: Same family, next available (different from current)
    for eid in priority_ids:
        if current_exercise_id and eid == current_exercise_id:
            continue
        ex = EXERCISE_BY_ID.get(eid)
        if ex is None:
            continue
        if ex.difficulty > max_diff:
            continue
        if not _equip_ok(ex, available_equip):
            continue
        if _inj_conflict(ex, injury_history):
            continue
        if not _ex_comp_ok(ex, comp_window):
            continue
        if athlete_profile and is_exercise_risk_flagged(ex, athlete_profile):
            continue
        return ex

    # Priority 2: Same intent, different family
    intent = FAMILY_TO_INTENT.get(family.value)
    if intent:
        for sub_fam_code in INTENT_CATEGORIES.get(intent, []):
            if sub_fam_code == family.value:
                continue
            sub_fam = FamilyCode(sub_fam_code)
            sub_ids = SELECTION_PRIORITIES.get(sub_fam_code, [])
            for eid in sub_ids:
                ex = EXERCISE_BY_ID.get(eid)
                if ex is None:
                    continue
                if ex.difficulty > max_diff:
                    continue
                if not _equip_ok(ex, available_equip):
                    continue
                if _inj_conflict(ex, injury_history):
                    continue
                if not _ex_comp_ok(ex, comp_window):
                    continue
                if athlete_profile and is_exercise_risk_flagged(ex, athlete_profile):
                    continue
                return ex

    # Priority 3: Same equipment, any family
    all_ex = list(EXERCISE_BY_ID.values())
    for ex in all_ex:
        if current_exercise_id and ex.id == current_exercise_id:
            continue
        if ex.family == family:
            continue
        if ex.difficulty > max_diff:
            continue
        if not _equip_ok(ex, available_equip):
            continue
        if _inj_conflict(ex, injury_history):
            continue
        if not _ex_comp_ok(ex, comp_window):
            continue
        if athlete_profile and is_exercise_risk_flagged(ex, athlete_profile):
            continue
        return ex

    # Priority 4: Emergency fallback — return None
    return None


def _equip_ok(exercise: Exercise, available_equip: list[str]) -> bool:
    for eq in exercise.equipment:
        eq_lower = eq.lower()
        if not any(e.lower() in eq_lower or eq_lower in e.lower() for e in available_equip):
            return False
    return True


