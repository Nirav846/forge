# Forge Exercise Substitution Engine
# Role: Principal Exercise Intelligence Architect
# Description: Given a slot and selected exercise, returns all valid substitute exercises
# preserving movement intent, progression envelope, and athlete safety filters.

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from recommendation_engine import MockExerciseRepository, LEVEL_ORDINAL, training_months_to_level
from exercise_equivalencies import EXERCISE_EQUIVALENCIES
from exercise_classification import classify_exercise, determine_primary_adaptation, determine_force_vector


class SubstituteExercise(BaseModel):
    exercise_id: int
    name: str
    difficulty_level: str
    mechanics_type: str
    force_type: str
    exercise_class: str
    primary_adaptation: str
    force_vector: str
    movement_pattern: str
    equivalency_score: float
    recommendation_score: float
    same_category: bool
    match_reasons: List[str]


async def get_substitutions(
    slot_id: int,
    exercise_id: int,
    athlete_profile: Dict[str, Any],
    equipment: List[str],
    repo: MockExerciseRepository,
    difficulty_cap: str = "Elite",
    training_age_months: int = 0,
    development_level: Optional[str] = None
) -> List[SubstituteExercise]:
    # Auto-derive development_level from training_age_months if not provided
    if development_level is None:
        development_level = training_months_to_level(training_age_months)
    
    # 1. Fetch the current exercise metadata
    current_ex = await _find_exercise_by_id(exercise_id, repo, slot_id, equipment, difficulty_cap, training_age_months, development_level)
    if not current_ex:
        return []

    # 2. Fetch ALL exercises for this slot (with generous filters to get the full pool)
    # Coerce into our richer dict format from the raw pool (which lacks classification)
    # Re-fetch from the full mock catalog for richer metadata
    all_exercises_raw = await _get_full_catalog(repo)

    # Filter by slot and athlete gates
    candidates = []
    for ex in all_exercises_raw:
        if ex["id"] == exercise_id:
            continue  # skip current
        if slot_id not in ex.get("slots", []):
            continue
        passes = _passes_athlete_gates(ex, athlete_profile, equipment, difficulty_cap, training_age_months, development_level)
        if not passes:
            continue
        candidates.append(ex)

    # 3. Check equivalencies first
    current_name = current_ex.get("name", "")
    current_class = current_ex.get("exercise_class", "")
    current_primary_adapt = current_ex.get("primary_adaptation", "")
    current_force_vector = current_ex.get("force_vector", "")
    current_movement_pattern = current_ex.get("movement_pattern", "")
    current_force_type = current_ex.get("force_type", "")
    current_mechanics_type = current_ex.get("mechanics_type", "")

    substitutions = []
    for ex in candidates:
        ex_name = ex["name"]
        reasons = []
        same_cat = False

        # A. Check direct equivalency
        equiv = _find_equivalency(current_name, ex_name)
        if equiv:
            equiv_score = equiv["equivalency_score"]
            reasons.append(f"Exercise equivalency: {equiv['reason']}")
        else:
            equiv_score = 0.0

        # B. Same category check
        ex_class = ex.get("exercise_class", "")
        if ex_class and ex_class == current_class:
            same_cat = True
            reasons.append(f"Same exercise class: {current_class}")

        # C. Movement pattern match
        ex_mp = ex.get("movement_pattern", "")
        if ex_mp and ex_mp == current_movement_pattern:
            reasons.append(f"Same movement pattern: {current_movement_pattern}")

        # D. Force type match
        ex_ft = ex.get("force_type", "")
        if ex_ft and ex_ft == current_force_type:
            reasons.append(f"Same force type: {current_force_type}")

        # E. Mechanics type match
        ex_mt = ex.get("mechanics_type", "")
        if ex_mt and ex_mt == current_mechanics_type:
            reasons.append(f"Same mechanics type: {current_mechanics_type}")

        # F. Primary adaptation match
        ex_pa = ex.get("primary_adaptation", "")
        if ex_pa and ex_pa == current_primary_adapt:
            reasons.append(f"Same primary adaptation: {current_primary_adapt}")

        score = ex.get("recommendation_score", 0.0) or ex.get("score_components", {}).get("relevance", 0) * 0.4 * 10.0

        substitutions.append(SubstituteExercise(
            exercise_id=ex["id"],
            name=ex_name,
            difficulty_level=ex.get("difficulty_level", ""),
            mechanics_type=ex_mt,
            force_type=ex_ft,
            exercise_class=ex_class,
            primary_adaptation=ex_pa,
            force_vector=ex.get("force_vector", ""),
            movement_pattern=ex_mp,
            equivalency_score=equiv_score,
            recommendation_score=round(score, 2),
            same_category=same_cat,
            match_reasons=reasons
        ))

    # 4. Rank: equivalency first, same category, movement pattern, force type, mechanics, score
    substitutions.sort(key=_substitution_rank_key, reverse=True)

    return substitutions


def _substitution_rank_key(sub: SubstituteExercise) -> tuple:
    return (
        sub.equivalency_score,            # 1. Direct equivalent (highest weight)
        1 if sub.same_category else 0,     # 2. Same category
        1 if any("movement pattern" in r for r in sub.match_reasons) else 0,  # 3. Same movement pattern
        1 if any("force type" in r for r in sub.match_reasons) else 0,        # 4. Same force type
        1 if any("mechanics type" in r for r in sub.match_reasons) else 0,    # 5. Same mechanics
        sub.recommendation_score            # 6. Recommendation score
    )


async def _find_exercise_by_id(exercise_id: int, repo: MockExerciseRepository, slot_id: int,
                                equipment: List[str], difficulty_cap: str, training_age_months: int,
                                development_level: str = "FOUNDATION") -> Optional[Dict[str, Any]]:
    catalog = await _get_full_catalog(repo)
    for ex in catalog:
        if ex["id"] == exercise_id:
            return ex
    return None


def _find_equivalency(source_name: str, target_name: str) -> Optional[Dict]:
    for e in EXERCISE_EQUIVALENCIES:
        if e["source_exercise_name"] == source_name and e["target_exercise_name"] == target_name:
            return e
    return None


def _passes_athlete_gates(ex: Dict[str, Any], athlete_profile: Dict[str, Any],
                          equipment: List[str], difficulty_cap: str,
                          training_age_months: int, development_level: str = "FOUNDATION") -> bool:
    # Development level gate (competency-based)
    dev_ord = LEVEL_ORDINAL.get(development_level, 1)
    if LEVEL_ORDINAL.get(ex.get("minimum_level", "FOUNDATION"), 1) > dev_ord:
        return False
    # Technical difficulty cap
    tech_cap = {"FOUNDATION": 3, "DEVELOPMENT": 6, "PERFORMANCE": 10}
    ex_tech = ex.get("technical_difficulty")
    if ex_tech is None or ex_tech > tech_cap.get(development_level, 3):
        return False
    # Difficulty cap
    diff_rank = {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Elite": 4}
    if diff_rank.get(ex.get("difficulty_level", "Beginner"), 1) > diff_rank.get(difficulty_cap, 4):
        return False
    # Equipment filter
    for req_eq in ex.get("required_equipment", []):
        if req_eq == "Bodyweight":
            continue
        if req_eq not in equipment:
            return False
    return True


def _resolve_template_id(slot_id: int) -> int:
    # Template mapping: 200s -> template 100, 300s -> 101, 400s -> 102
    if slot_id >= 400:
        return 102
    if slot_id >= 300:
        return 101
    return 100


_FULL_CATALOG_CACHE = None


async def _get_full_catalog(repo: MockExerciseRepository) -> List[Dict[str, Any]]:
    global _FULL_CATALOG_CACHE
    if _FULL_CATALOG_CACHE is not None:
        return _FULL_CATALOG_CACHE
    # Fetch all exercises by querying each slot's full pool with generous gates
    # then deduplicate by id
    all_ex = {}
    slot_ids = [201, 202, 203, 204, 301, 302, 303, 304, 401, 402, 403, 404]
    # Reset cache before building to avoid stale data
    _FULL_CATALOG_CACHE = None
    for sid in slot_ids:
        pool = await repo.get_ranked_exercises(
            slot_id=sid,
            template_id=_resolve_template_id(sid),
            difficulty_cap="Elite",
            equipment=["Barbell", "Trap Bar", "Medicine Ball", "Kettlebell", "Dumbbell", "Cable Machine", "Bodyweight"],
            training_age_months=999,
            development_level="PERFORMANCE"
        )
        import sys
        print(f"DEBUG: slot {sid} -> {len(pool)} exercises: {[ex['id'] for ex in pool]}", file=sys.stderr)
        for ex in pool:
            all_ex[ex["id"]] = ex
    _FULL_CATALOG_CACHE = list(all_ex.values())
    return _FULL_CATALOG_CACHE



