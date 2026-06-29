"""Exercise selection engine."""
import random
from typing import Optional, Union
from .models import (
    Exercise, FamilyCode, AthleteLevel, EquipmentProfile, AthleteProfile, CoachPreferences,
    MovementSlot,
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

# Movement-pattern → keyword family to detect pattern on a candidate exercise.
# Used by _movement_pattern_score below; one source of truth.
_PATTERN_KEYWORDS: dict[str, tuple[str, ...]] = {
    "squat": ("squat", "leg press", "goblet", "split squat"),
    "hinge": ("deadlift", "rdl", "hinge", "hip thrust", "glute bridge", "swing"),
    "push": ("press", "push up", "bench", "overhead"),
    "pull": ("row", "pull", "chin", "lat pulldown", "pullover"),
    "rotation": ("rotation", "chop", "med ball", "pallof"),
    "carry": ("carry", "farmer", "suitcase", "waiter"),
    "core": ("plank", "crunch", "core", "dead bug", "bird dog"),
    "plyo": ("jump", "plyo", "bound", "hop", "depth", "reactive"),
    "sprint": ("sprint", "run", "shuffle", "acceleration"),
    "eccentric": ("nordic", "eccentric", "decline", "drop", "landing"),
}

# Intent → exercise-name / family heuristic for bonus scoring.
_INTENT_KEYWORDS: dict[str, tuple[str, ...]] = {
    "eccentric": ("nordic", "eccentric", "decline", "drop"),
    "power": ("jump", "throw", "slam", "explosive", "power"),
    "stability": ("isometric", "hold", "stability", "balance"),
    "mobility": ("mobility", "stretch", "rotation drill"),
    "activation": ("activation", "band", "warm"),
}

# ── Progression tier: difficulty (1-5) → tier (0-2) ──────────────
_EXERCISE_TIER: dict[str, int] = {}
for _eid, _ex in EXERCISE_BY_ID.items():
    _EXERCISE_TIER[_eid] = min(2, max(0, _ex.difficulty - 1))

# Global cross-program diversity tracker: ex_id -> usage count
_recent_exercises_global: dict[str, int] = {}


def _matches_priority(exercise: Exercise, category: str) -> bool:
    """Check if an exercise matches a priority category.

    Checks name (existing), family (category keyword matches exercise family),
    and secondary_family (sport name embedded in category).
    """
    # 1. Name match (existing behaviour)
    if category.lower() in exercise.name.lower():
        return True

    # 2. Family match: category keyword matches exercise family
    family_keywords: dict[str, list[str]] = {
        "plyo": ["plyo", "jump", "reactive", "depth"],
        "agility": ["agility", "cod", "change of direction", "shuffle", "reaction"],
        "core": ["core", "plank", "crunch", "rotation"],
        "acc": ["acc", "acceleration", "balance", "stability", "collision", "contact"],
        "sprint": ["sprint", "speed", "max velocity"],
        "landing": ["landing", "absorption", "deceleration"],
        "dlhd": ["hinge", "deadlift", "rdl"],
        "dlkd": ["squat", "leg press"],
        "slhd": ["single leg hinge", "sl rdl"],
        "slkd": ["single leg squat", "lunge", "step down"],
        "hpush": ["bench", "push up", "press"],
        "hpull": ["row", "pull", "scap"],
        "vpush": ["overhead", "military", "shoulder press"],
        "vpull": ["pull up", "lat", "pullover"],
        "rot": ["rotation", "chop", "med ball rotational"],
    }
    for family, keywords in family_keywords.items():
        if exercise.family.value.lower() == family:
            if any(kw in category.lower() for kw in keywords):
                return True

    # 3. Secondary_family match: exercise sport tag appears in category
    if exercise.secondary_family and exercise.secondary_family.value.lower() in category.lower():
        return True

    return False


def select_exercise(
    slot: Union[MovementSlot, FamilyCode, None] = None,
    athlete_level: AthleteLevel = AthleteLevel.BEGINNER,
    equipment_profile: EquipmentProfile = EquipmentProfile.FIELD_ONLY,
    recent_exercises: dict[str, dict] = None,
    injury_history: list[str] = None,
    days_to_match: Optional[int] = None,
    technique_consistency: float = 1.0,
    strength_base_met: bool = True,
    athlete_profile: Optional[AthleteProfile] = None,
    coach_prefs: Optional[CoachPreferences] = None,
    power_multiplier: float = 1.0,
    week_type: str = "accumulation",
    session_intent: Optional[object] = None,
    slot_family: Optional[FamilyCode] = None,
) -> Optional[Exercise]:
    """Select an exercise for a slot.

    Accepts either:
      - a MovementSlot as first positional (preferred — coach-aware selection)
      - a FamilyCode as first positional (legacy positional form)
      - slot_family=... kw (legacy keyword form, used by progression_engine)
    """
    recent_exercises = recent_exercises if recent_exercises is not None else {}
    injury_history = injury_history if injury_history is not None else []
    # ponytail: backward-compat aggregation for all three call shapes
    if slot is None and slot_family is not None:
        slot = slot_family
    if isinstance(slot, MovementSlot):
        movement_slot: Optional[MovementSlot] = slot
        family = slot.family
    elif isinstance(slot, FamilyCode):
        movement_slot = None
        family = slot
    elif slot is None:
        raise TypeError("select_exercise requires a slot or slot_family")

    comp_window = _resolve_comp_window(days_to_match)
    max_diff = get_max_difficulty(athlete_level.value)
    available_equip = get_equipment_for_profile(equipment_profile.value)

    # Technique gate: force regression-level difficulty when mastery is low
    if technique_consistency < 0.8:
        max_diff = min(max_diff, 1)

    # Bilateral→unilateral gate: downgrade single-leg to double-leg if base not met
    effective_family = family
    if not strength_base_met:
        if family == FamilyCode.SLKD:
            effective_family = FamilyCode.DLKD
        elif family == FamilyCode.SLHD:
            effective_family = FamilyCode.DLHD

    # Slot-driven difficulty ceiling: tier ± 1 around the slot's progression_tier
    if movement_slot is not None:
        slot_tier = max(1, min(5, int(movement_slot.progression_tier)))
        difficulty_floor = max(1, slot_tier - 1)
        difficulty_ceiling = min(5, slot_tier + 1)
        max_diff = min(max_diff, difficulty_ceiling)
    else:
        difficulty_floor = 1
        difficulty_ceiling = max_diff

    # Equipment preference override from the slot
    if movement_slot and movement_slot.equipment_preference:
        available_equip = list({e.lower() for e in movement_slot.equipment_preference})

    priority_ids = SELECTION_PRIORITIES.get(effective_family.value, [])

    candidates = []
    for eid in priority_ids:
        ex = EXERCISE_BY_ID.get(eid)
        if ex is None:
            continue
        if ex.difficulty > max_diff:
            continue
        # Slot-aware difficulty floor: tier±1 lower bound for non-mobility slots
        if movement_slot is not None and ex.difficulty < difficulty_floor:
            if movement_slot.intent not in ("mobility", "activation", "recovery"):
                continue
        if not _equipment_available(ex, available_equip):
            continue
        if has_injury_conflict(ex.name, injury_history):
            continue
        if not _exercise_competition_ok(ex, comp_window):
            continue
        if athlete_profile and is_exercise_risk_flagged(ex, athlete_profile):
            continue

        # Sub-substitution whitelist: if slot.substitutions is set, prefer it
        if movement_slot and movement_slot.substitutions:
            slot_sub_names = {s.lower() for s in movement_slot.substitutions}
            # Keep the candidate; ranking is boosted later for matches.

        candidates.append(ex)

    # Wave 11a — Advanced athlete ceiling: enforce minimum difficulty for main strength
    if athlete_level == AthleteLevel.ADVANCED and strength_base_met:
        if effective_family in MAIN_STRENGTH_FAMILIES:
            candidates = [ex for ex in candidates if ex.difficulty >= 3]

    # Wave 14 — Coach preferences: variant filtering
    if coach_prefs and candidates:
        # Preferred deadlift variant
        if family == FamilyCode.DLHD and coach_prefs.preferred_deadlift:
            variant = coach_prefs.preferred_deadlift.lower().replace("_", " ")
            filtered = [ex for ex in candidates if variant in ex.name.lower()]
            if filtered:
                candidates = filtered

        # Preferred squat variant
        if family == FamilyCode.DLKD and coach_prefs.preferred_squat:
            variant = coach_prefs.preferred_squat.lower().replace("_", " ")
            if variant == "barbell":
                filtered = [ex for ex in candidates if "barbell" in ex.name.lower() or "front squat" in ex.name.lower() or "safety bar" in ex.name.lower()]
            else:
                filtered = [ex for ex in candidates if variant in ex.name.lower()]
            if filtered:
                candidates = filtered

        # Preferred press variant
        if family == FamilyCode.VPUSH and coach_prefs.preferred_press:
            variant = coach_prefs.preferred_press.lower().replace("_", " ")
            filtered = [ex for ex in candidates if variant in ex.name.lower()]
            if filtered:
                candidates = filtered

        # Avoid Olympic lifts
        if coach_prefs.avoid_olympic_lifts:
            olympic_keywords = ["clean", "snatch", "jerk", "olympic"]
            candidates = [ex for ex in candidates if not any(kw in ex.name.lower() for kw in olympic_keywords)]

        # Bias unilateral: boost single-leg families scores
        if coach_prefs.bias_unilateral_work and family in (FamilyCode.SLHD, FamilyCode.SLKD):
            scored = [(ex, 1 if "split" in ex.name.lower() or "lunge" in ex.name.lower() or "single leg" in ex.name.lower() else 0) for ex in candidates]
            candidates = [ex for _, ex in sorted(scored, key=lambda x: -x[1])]

    if not candidates:
        return substitute_exercise(
            family,
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
                    if _matches_priority(ex, cat):
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

        # Slot-aware weighting: pattern + intent + substitutions
        if movement_slot is not None:
            w += _slot_pattern_score(ex, movement_slot.movement_pattern)
            w += _slot_intent_score(ex, movement_slot.intent)
            if movement_slot.substitutions:
                if any(s.lower() in ex.name.lower() for s in movement_slot.substitutions):
                    w += 3.0

        # Progression plan bias: complexity, velocity, eccentric
        if session_intent and session_intent.progression:
            pp = session_intent.progression
            diff_diff = abs(ex.difficulty - pp.complexity_level)
            w += max(0, 4 - diff_diff) * 0.5
            if pp.velocity_emphasis == "explosive" and ex.explosive:
                w *= 1.5
            elif pp.velocity_emphasis == "controlled" and not ex.explosive:
                w *= 1.2
            if pp.eccentric_emphasis > 1.0 and ex.family in (FamilyCode.DLHD, FamilyCode.SLHD, FamilyCode.LANDING):
                w *= pp.eccentric_emphasis
        else:
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


def _slot_pattern_score(ex: Exercise, pattern: str) -> float:
    """+2.0 when the exercise name matches the slot's movement pattern."""
    keywords = _PATTERN_KEYWORDS.get(pattern, ())
    if not keywords:
        return 0.0
    name_lower = ex.name.lower()
    if any(kw in name_lower for kw in keywords):
        return 2.0
    return 0.0


def _slot_intent_score(ex: Exercise, intent: str) -> float:
    """Bonus when the exercise matches the slot's training intent (eccentric, power…)."""
    keywords = _INTENT_KEYWORDS.get(intent, ())
    if not keywords:
        return 0.0
    name_lower = ex.name.lower()
    if any(kw in name_lower for kw in keywords):
        return 1.5
    return 0.0



