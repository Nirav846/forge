"""Exercise selection engine."""
import random
from typing import Optional
from .models import (
    Exercise, FamilyCode, AthleteLevel, EquipmentProfile, AthleteProfile, CoachPreferences,
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
from .progression_engine import MAIN_STRENGTH_FAMILIES

# ── Progression tier: difficulty (1-5) → tier (0-2) ──────────────
_EXERCISE_TIER: dict[str, int] = {}
for _eid, _ex in EXERCISE_BY_ID.items():
    _EXERCISE_TIER[_eid] = min(2, max(0, _ex.difficulty - 1))

# Global cross-program diversity tracker: ex_id -> usage count
_recent_exercises_global: dict[str, int] = {}


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
    coach_prefs: Optional[CoachPreferences] = None,
    power_multiplier: float = 1.0,
    week_type: str = "accumulation",
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

    # Wave 11a — Advanced athlete ceiling: enforce minimum difficulty for main strength
    if athlete_level == AthleteLevel.ADVANCED and strength_base_met:
        if effective_family in MAIN_STRENGTH_FAMILIES:
            candidates = [ex for ex in candidates if ex.difficulty >= 3]

    # Wave 14 — Coach preferences: variant filtering
    if coach_prefs and candidates:
        name_lower = {ex.name.lower() for ex in candidates}

        # Preferred deadlift variant
        if slot_family == FamilyCode.DLHD and coach_prefs.preferred_deadlift:
            variant = coach_prefs.preferred_deadlift.lower().replace("_", " ")
            filtered = [ex for ex in candidates if variant in ex.name.lower()]
            if filtered:
                candidates = filtered

        # Preferred squat variant
        if slot_family == FamilyCode.DLKD and coach_prefs.preferred_squat:
            variant = coach_prefs.preferred_squat.lower().replace("_", " ")
            if variant == "barbell":
                filtered = [ex for ex in candidates if "barbell" in ex.name.lower() or "front squat" in ex.name.lower() or "safety bar" in ex.name.lower()]
            else:
                filtered = [ex for ex in candidates if variant in ex.name.lower()]
            if filtered:
                candidates = filtered

        # Preferred press variant
        if slot_family == FamilyCode.VPUSH and coach_prefs.preferred_press:
            variant = coach_prefs.preferred_press.lower().replace("_", " ")
            filtered = [ex for ex in candidates if variant in ex.name.lower()]
            if filtered:
                candidates = filtered

        # Avoid Olympic lifts
        if coach_prefs.avoid_olympic_lifts:
            olympic_keywords = ["clean", "snatch", "jerk", "olympic"]
            candidates = [ex for ex in candidates if not any(kw in ex.name.lower() for kw in olympic_keywords)]

        # Bias unilateral: boost single-leg families scores
        if coach_prefs.bias_unilateral_work and slot_family in (FamilyCode.SLHD, FamilyCode.SLKD):
            scored = [(ex, 1 if "split" in ex.name.lower() or "lunge" in ex.name.lower() or "single leg" in ex.name.lower() else 0) for ex in candidates]
            candidates = [ex for _, ex in sorted(scored, key=lambda x: -x[1])]

    if not candidates:
        return substitute_exercise(
            effective_family if effective_family != slot_family else slot_family,
            athlete_level, equipment_profile,
            injury_history, recent_exercises, None, days_to_match,
            athlete_profile=athlete_profile,
        )

    # Weighted random selection from top candidates.
    # Priority order + role matching + personalization + diversity all inform weights.
    # Compute target progression tier from athlete attributes
    target_tier = 1
    if athlete_profile:
        level_tier = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}.get(athlete_level.value, 0)
        age_tier = 0 if athlete_profile.training_age_years < 2 else (1 if athlete_profile.training_age_years < 5 else 2)
        target_tier = min(level_tier, age_tier)
        if technique_consistency < 0.7:
            target_tier = max(0, target_tier - 1)
    # Sort: sport-specific first, then closest tier match
    if athlete_profile:
        sport_lower = athlete_profile.sport.lower()
        candidates.sort(key=lambda ex: (
            0 if ex.secondary_family and ex.secondary_family.value.lower() == sport_lower else 1,
            abs(_EXERCISE_TIER.get(ex.id, 1) - target_tier)
        ))
    else:
        candidates.sort(key=lambda ex: abs(_EXERCISE_TIER.get(ex.id, 1) - target_tier))
    TOP_N = 5
    pool = candidates[:TOP_N]
    weights = []
    for ex in pool:
        w = 1.0

        # Power multiplier bias
        if power_multiplier != 1.0 and ex.family in (FamilyCode.PLYO, FamilyCode.BALL):
            if power_multiplier > 1.0:
                w += 2.0 if (ex.explosive or ex.objective.value == "POW") else 0.0
            else:
                w += 2.0 if not (ex.explosive or ex.objective.value == "POW") else 0.0

        # Role priority category match
        if athlete_profile and athlete_profile.role:
            from .role_profiles import get_role_profile
            rp = get_role_profile(athlete_profile.sport, athlete_profile.role)
            if rp and rp.get('priority_exercise_categories'):
                for cat in rp['priority_exercise_categories']:
                    if cat.lower() in ex.name.lower():
                        w += 2.0
                    # Injury Prevention / Deceleration boost: prefer deceleration-family exercises
                    cat_lower = cat.lower()
                    if cat_lower in ('injury prevention', 'deceleration') and ex.secondary_family:
                        if ex.secondary_family.value.lower() == 'deceleration':
                            w += 3.0

        # Sport-specific exercise boost: prefer exercises whose secondary_family matches athlete's sport
        if athlete_profile and ex.secondary_family:
            if ex.secondary_family.value.lower() == athlete_profile.sport.lower():
                w += 2.0

        # Progression tier match boost: prefer exercises at or near target tier
        tier_distance = abs(_EXERCISE_TIER.get(ex.id, 1) - target_tier)
        w += max(0, 2 - tier_distance) * 1.5

        # Week-type difficulty bias
        wk_aim = {"accumulation": 1, "intensification": 2, "realization": 3, "taper": 1, "test": 0, "deload": 0}
        aim = wk_aim.get(week_type, 1)
        diff_diff = abs(ex.difficulty - aim)
        w += max(0, 4 - diff_diff) * 0.5

        # Coach intent keyword boost
        if athlete_profile and athlete_profile.coach_intent:
            intent_lower = athlete_profile.coach_intent.lower()
            ex_name_lower = ex.name.lower()
            for token in intent_lower.replace(",", " ").split():
                token = token.strip()
                if token and token in ex_name_lower:
                    w += 1.5

        # Personalization bias (force/elastic/landing/sprint profile)
        if athlete_profile:
            bias = get_exercise_personalization_bias(ex, athlete_profile)
            w += bias * 1.5

        # Diversity penalty — within-program
        if ex.id in recent_exercises:
            w *= 0.3

        # Diversity penalty — global (cross-program)
        global _recent_exercises_global
        count = _recent_exercises_global.get(ex.id, 0)
        if count >= 2:
            w *= 0.15
        elif count == 1:
            w *= 0.5

        weights.append(max(0.01, w))

    selected = random.choices(pool, weights=weights, k=1)[0]

    # Track globally (sticky — persists across program generations)
    _recent_exercises_global[selected.id] = _recent_exercises_global.get(selected.id, 0) + 1

    return selected


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



