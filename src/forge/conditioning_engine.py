"""Conditioning selection and generation engine with competition proximity + movement-profile routing."""
from typing import Optional
from .models import (
    Session, SessionBlock, ConditioningProtocol,
    AthleteLevel, FamilyCode, AthleteProfile,
)
from .data import (
    CONDITIONING_PROTOCOLS, COND_PROTOCOL_BY_ID,
    COND_PROTOCOLS_BY_SYSTEM, COND_DECISION_MAP
)
from .athlete_profile_rules import score_conditioning_for_athlete

CONDITIONING_GOAL_MAP = {
    "recovery": "Recovery Conditioning",
    "aerobic_capacity": "Aerobic Capacity",
    "aerobic_power": "Aerobic Power",
    "extensive_tempo": "Extensive Tempo",
    "intensive_tempo": "Intensive Tempo",
    "rsa": "Repeated Sprint Ability",
    "alactic_speed": "Alactic Speed",
    "lactate_tolerance": "Lactate Tolerance",
    "power_maintenance": "Power Maintenance",
}

ENV_CATEGORY_MAP = {
    "ground": "field",
    "field": "field",
    "track": "field",
    "court": "court",
    "gym": "gym",
    "recovery": "recovery",
    "pool": "recovery",
}

# Competition proximity windows → exercise-level fatigue/impact/eccentric thresholds
EXERCISE_COMP_MAX_FATIGUE = {None: 5, 6: 5, 4: 4, 2: 3, 1: 2}
EXERCISE_COMP_MAX_IMPACT = {None: 5, 6: 5, 4: 4, 2: 3, 1: 2}
EXERCISE_COMP_MAX_ECCENTRIC = {None: 5, 6: 5, 4: 4, 2: 3, 1: 2}

# Competition proximity windows → session_role + impact constraints
COMP_ROLES_BY_WINDOW = {
    None: None,           # no restriction
    6:    None,           # >=6 days: full range
    4:    ["main_conditioning", "top_up_conditioning", "power_maintenance", "recovery_flush"],  # 4-5
    2:    ["main_conditioning", "top_up_conditioning", "power_maintenance", "recovery_flush"],  # 2-3
    1:    ["power_maintenance", "recovery_flush"],                                               # <=1
}
COMP_MAX_IMPACT_BY_WINDOW = {
    None: 5, 6: 5, 4: 4, 2: 3, 1: 2,
}

# Preferred movement profiles per sport (in priority order)
SPORT_MOVEMENT_PROFILES: dict[str, list[str]] = {
    "any": [],
    "cricket": ["linear_tempo", "accel_decel", "linear_speed_endurance", "linear_rsa"],
    "rugby": ["linear_tempo", "accel_decel", "linear_speed_endurance", "linear_rsa"],
    "soccer": ["linear_tempo", "accel_decel", "linear_speed_endurance", "linear_rsa"],
    "hockey": ["linear_tempo", "change_of_direction", "accel_decel", "linear_speed_endurance"],
    "tennis": ["court_shuffle", "change_of_direction", "accel_decel", "court_diagonal", "court_rally_repeat"],
    "badminton": ["court_shuffle", "change_of_direction", "court_diagonal", "accel_decel"],
    "basketball": ["court_shuffle", "change_of_direction", "accel_decel"],
    "volleyball": ["court_shuffle", "change_of_direction", "accel_decel", "court_rally_repeat"],
    "squash": ["court_shuffle", "court_rally_repeat", "change_of_direction"],
    "track": ["linear_tempo", "linear_speed_endurance", "linear_rsa"],
    "netball": ["court_shuffle", "change_of_direction", "accel_decel"],
    "american_football": ["linear_tempo", "accel_decel", "linear_rsa"],
}


def _resolve_comp_window(days_to_match: Optional[int]) -> int:
    if days_to_match is None:
        return None
    if days_to_match >= 6:
        return 6
    if days_to_match >= 4:
        return 4
    if days_to_match >= 2:
        return 2
    return 1


def _preferred_movement_profiles(sport: str) -> list[str]:
    sport_lower = sport.lower().strip() if sport else "any"
    return SPORT_MOVEMENT_PROFILES.get(sport_lower, [])


def _competition_ok(proto: ConditioningProtocol, window: int) -> bool:
    roles = COMP_ROLES_BY_WINDOW.get(window)
    if roles and proto.session_role not in roles:
        return False
    max_impact = COMP_MAX_IMPACT_BY_WINDOW.get(window, 5)
    if proto.impact_level > max_impact:
        return False
    return True


def _movement_match(proto: ConditioningProtocol, preferred: list[str]) -> int:
    if not preferred:
        return 0
    if proto.movement_profile in preferred:
        return 2
    return 0


def generate_conditioning(
    session: Session,
    athlete_level: AthleteLevel,
    goal: str,
    environment: str = "field",
    time_available: int = 20,
    sport: str = "any",
    days_to_match: Optional[int] = 14,
    athlete_profile: Optional[AthleteProfile] = None,
) -> Optional[ConditioningProtocol]:
    selected = select_conditioning(athlete_level, goal, environment,
                                   time_available, sport, days_to_match,
                                   athlete_profile=athlete_profile)
    if selected is None:
        return None

    adjusted = apply_level_adjustment(selected, athlete_level)
    return adjusted


def select_conditioning(
    athlete_level: AthleteLevel,
    goal: str,
    environment: str = "field",
    time_available: int = 20,
    sport: str = "any",
    days_to_match: Optional[int] = 14,
    athlete_profile: Optional[AthleteProfile] = None,
) -> Optional[ConditioningProtocol]:
    if goal == "intensive_tempo" and athlete_level == AthleteLevel.BEGINNER:
        return None
    if goal == "lactate_tolerance" and athlete_level != AthleteLevel.ADVANCED:
        return None

    comp_window = _resolve_comp_window(days_to_match)
    preferred = _preferred_movement_profiles(sport)

    # Step 1: Use decision map (goal + environment + time)
    protocol_id = _lookup_decision_map(goal, environment, time_available)
    if protocol_id and protocol_id in COND_PROTOCOL_BY_ID:
        proto = COND_PROTOCOL_BY_ID[protocol_id]
        if _level_ok(proto, athlete_level) and _competition_ok(proto, comp_window):
            return proto

    # Step 2: Fallback — select by energy system + environment_category + sport_tags + competition proximity + movement_profile
    system_name = CONDITIONING_GOAL_MAP.get(goal)
    if not system_name:
        return None

    candidates = COND_PROTOCOLS_BY_SYSTEM.get(system_name, [])
    if not candidates:
        return None

    a_tier = [p for p in candidates if p.tier == "A"]
    if a_tier:
        candidates = a_tier

    env_cat = ENV_CATEGORY_MAP.get(environment.replace(" ", "_").lower(), "field")

    scored: list[tuple[int, ConditioningProtocol]] = []
    for p in candidates:
        if not _level_ok(p, athlete_level):
            continue
        if p.environment_category != env_cat:
            continue
        if sport != "any" and "any" not in p.sport_tags and sport not in p.sport_tags:
            continue
        if not _competition_ok(p, comp_window):
            continue
        score = _movement_match(p, preferred)
        if athlete_profile:
            score += score_conditioning_for_athlete(p, athlete_profile)
        scored.append((score, p))

    if not scored:
        # Final fallback: any candidate in the system (still respecting comp window + env)
        for p in candidates:
            if _level_ok(p, athlete_level) and p.environment_category == env_cat and _competition_ok(p, comp_window):
                return p
        return None

    scored.sort(key=lambda x: (-x[0], 0 if x[1].tier == "A" else 1))
    return scored[0][1]


def _lookup_decision_map(goal: str, environment: str, time_available: int) -> Optional[str]:
    time_key = time_available
    if time_key not in (10, 20, 30, 45):
        time_key = 20

    env_key = environment.replace(" ", "_").lower()
    env_map = {
        "field": "field", "track": "track", "treadmill": "treadmill",
        "indoor": "indoor", "limited_space": "limited_space",
        "limited space": "limited_space",
        "ground": "field", "court": "court", "gym": "treadmill",
        "recovery": "field",
    }
    env_key = env_map.get(env_key, "field")

    goal_map = {
        "recovery": "recovery", "aerobic_capacity": "aerobic_capacity",
        "aerobic_power": "aerobic_power", "extensive_tempo": "extensive_tempo",
        "intensive_tempo": "intensive_tempo", "rsa": "rsa",
        "alactic_speed": "alactic_speed", "lactate_tolerance": "lactate_tolerance",
        "power_maintenance": "power_maintenance",
    }
    goal_key = goal_map.get(goal)
    if not goal_key:
        return None

    goal_data = COND_DECISION_MAP.get(goal_key, {})
    env_data = goal_data.get(env_key, {})
    return env_data.get(time_key)


def _level_ok(protocol: ConditioningProtocol, athlete_level: AthleteLevel) -> bool:
    level_str = protocol.level.lower()
    al = athlete_level.value.lower()
    if "all" in level_str or "any" in level_str:
        return True
    if al in level_str:
        return True
    if al == "beginner" and "beginner" in level_str:
        return True
    if al == "intermediate" and ("intermediate" in level_str or "advanced" in level_str):
        return True
    if al == "advanced" and "elite" in level_str:
        return True
    return False


def apply_level_adjustment(
    protocol: ConditioningProtocol,
    athlete_level: AthleteLevel,
) -> ConditioningProtocol:
    if not protocol.level_variants:
        return protocol

    level_map = {"Beginner": 1, "Intermediate": 2, "Advanced": 4}
    level = level_map.get(athlete_level.value, 2)
    variant = protocol.level_variants.get(level, {})
    if not variant:
        return protocol

    return ConditioningProtocol(
        id=protocol.id,
        name=protocol.name,
        objective=protocol.objective,
        system=protocol.system,
        level=protocol.level,
        environment=protocol.environment,
        duration=variant.get("duration", protocol.duration),
        work_description=variant.get("work_description", protocol.work_description),
        rest=variant.get("rest", protocol.rest),
        sets=variant.get("sets", protocol.sets),
        total_volume=variant.get("total_volume", protocol.total_volume),
        fatigue_score=protocol.fatigue_score,
        progression=protocol.progression,
        regression=protocol.regression,
        tier=protocol.tier,
        work_rest_ratio=protocol.work_rest_ratio,
        level_variants=protocol.level_variants,
        environment_category=protocol.environment_category,
        sport_tags=protocol.sport_tags,
        movement_profile=protocol.movement_profile,
        session_role=protocol.session_role,
        fatigue_cost=protocol.fatigue_cost,
        impact_level=protocol.impact_level,
        eccentric_cost=protocol.eccentric_cost,
    )
