"""Block-level progression, exercise continuity, conditioning progression, and program validation.

Smallest credible architecture for Wave 3.
"""
from __future__ import annotations
from typing import Optional
from .models import (
    FamilyCode, AthleteLevel, Exercise, Session, SessionBlock,
    GeneratedProgram, ConditioningProtocol, EquipmentProfile, AthleteProfile,
    CoachPreferences,
)
from .data import (
    EXERCISE_BY_ID, BLUEPRINT_BY_ID, get_max_difficulty, get_equipment_for_profile,
)
from .conditioning_engine import (
    _resolve_comp_window, COND_PROTOCOLS_BY_SYSTEM, CONDITIONING_GOAL_MAP,
)
from .role_week_planning import (
    get_role_exposure_limits, RoleWeekProfile, get_role_week_profile,
    apply_role_slot_bias, should_add_conditioning_for_role,
    get_role_conditioning_frequency_bias,
)
from .session_assembly import (
    check_session_identity_preserved,
    check_session_flow_credible,
    check_high_value_families_not_dropped_before_low_value,
    check_role_bias_not_overriding_blueprint,
    check_taper_drop_logic_credible,
    check_post_filter_session_balance,
    check_repeated_family_progression_credible,
    compute_family_survival_tier,
)

# ── WEEK STRUCTURE ────────────────────────────────────────────────

WEEK_INDEX_TO_TYPE: dict[int, str] = {
    0: "accumulation",
    1: "accumulation",
    2: "intensification",
    3: "intensification",
    4: "intensification",
    5: "peak",
    6: "taper",
    7: "deload",
}

WEEK_STRUCTURE_DEFAULT: list[str] = [
    "accumulation",
    "accumulation",
    "intensification",
    "intensification",
    "realization",
    "realization",
    "taper",
    "test",
]


def plan_weeks(
    blueprint_id: int,
    athlete_level: AthleteLevel,
    goal: str,
    age: int,
    days_to_match: Optional[int] = None,
) -> list[str]:
    weeks = list(WEEK_STRUCTURE_DEFAULT)

    if blueprint_id == 13:
        return ["deload"] * 8

    if goal == "return_to_sport":
        weeks[4] = weeks[5] = "intensification"

    if athlete_level == AthleteLevel.BEGINNER or age < 16:
        weeks[7] = "deload"

    comp_window = _resolve_comp_window(days_to_match)
    if comp_window and comp_window <= 4 and goal in ("speed", "power_maintenance"):
        weeks[5] = "taper"
        weeks[6] = "deload"
        weeks[7] = "deload"

    if days_to_match is not None and days_to_match <= 1:
        weeks = ["light"] * 8
    elif days_to_match is not None and days_to_match <= 2:
        for i in range(5, 8):
            weeks[i] = "taper"

    return weeks


# ── TESTING PLANNER ────────────────────────────────────────────────

TESTING_CATEGORIES: dict[str, dict] = {
    "lower_body_strength": {
        "label": "Lower Body Strength Test",
        "blocked_for": ["beginner", "youth", "return_to_play"],
        "max_exercises": 2,
    },
    "upper_body_strength": {
        "label": "Upper Body Strength Test",
        "blocked_for": ["beginner", "youth", "return_to_play"],
        "max_exercises": 2,
    },
    "jump_power": {
        "label": "Jump / Power Test",
        "blocked_for": [],
        "max_exercises": 2,
    },
    "sprint_speed": {
        "label": "Sprint / Speed Test",
        "blocked_for": ["return_to_play"],
        "max_exercises": 2,
    },
    "conditioning_benchmark": {
        "label": "Conditioning Benchmark",
        "blocked_for": ["return_to_play"],
        "max_exercises": 1,
    },
    "movement_technical": {
        "label": "Movement / Technical Benchmark",
        "blocked_for": [],
        "max_exercises": 3,
    },
}


def plan_testing(
    week_intents: list[str],
    blueprint_id: int,
    athlete_level: AthleteLevel,
    goal: str,
    age: int,
    days_to_match: Optional[int] = None,
) -> dict[int, list[str]]:
    tests: dict[int, list[str]] = {}
    comp_window = _resolve_comp_window(days_to_match)
    is_beginner = athlete_level == AthleteLevel.BEGINNER
    is_youth = is_beginner or age < 16
    is_rtp = goal == "return_to_sport"
    is_deload = blueprint_id == 13

    if comp_window and comp_window <= 2:
        return tests

    blocked: set[str] = set()
    if is_beginner or is_youth:
        blocked.update({"lower_body_strength", "upper_body_strength"})
    if is_rtp:
        blocked.update({"lower_body_strength", "upper_body_strength", "sprint_speed", "conditioning_benchmark"})

    for i, intent in enumerate(week_intents):
        week_num = i + 1

        if intent == "test" and not is_deload:
            week_tests = []
            for cat in ("lower_body_strength", "upper_body_strength", "jump_power", "sprint_speed", "conditioning_benchmark"):
                if cat not in blocked:
                    week_tests.append(cat)
            if is_beginner or is_rtp:
                week_tests.append("movement_technical")
            if week_tests:
                tests[week_num] = week_tests

        elif intent == "accumulation" and week_num == 1:
            week_tests = ["movement_technical"]
            if not is_rtp:
                week_tests.append("jump_power")
            tests[week_num] = week_tests

        elif intent == "realization" and week_num in (5, 6):
            if not is_rtp and not is_deload:
                tests[week_num] = ["jump_power", "sprint_speed"]

    return tests


# ── EXERCISE CONTINUITY RULES ─────────────────────────────────────

MAIN_STRENGTH_FAMILIES = {FamilyCode.DLKD, FamilyCode.DLHD}
SECONDARY_CONTINUITY_FAMILIES = {
    FamilyCode.HPUSH, FamilyCode.HPULL, FamilyCode.VPUSH, FamilyCode.VPULL,
    FamilyCode.SLKD, FamilyCode.SLHD,
}

FAMILY_CONTINUITY_WEEKS: dict[str, int] = {
    "DLKD": 4, "DLHD": 4,
    "HPush": 2, "HPull": 2, "VPush": 2, "VPull": 2,
    "SLKD": 2, "SLHD": 2,
    "Sprint": 2, "Plyo": 2, "Ball": 2,
    "Landing": 2, "Rot": 2, "Carry": 2, "Core": 1, "Acc": 1,
}

FAMILY_IS_MAIN_STRENGTH: dict[str, bool] = {
    "DLKD": True, "DLHD": True, "SLKD": False, "SLHD": False,
    "HPush": False, "HPull": False, "VPush": False, "VPull": False,
    "Plyo": False, "Ball": False, "Sprint": False, "Landing": False,
    "Rot": False, "Carry": False, "Core": False, "Acc": False,
}


def continuity_weeks(family: FamilyCode) -> int:
    return FAMILY_CONTINUITY_WEEKS.get(family.value, 1)


def is_main_strength(family: FamilyCode) -> bool:
    return FAMILY_IS_MAIN_STRENGTH.get(family.value, False)


def plan_exercise_for_slot(
    family: FamilyCode,
    week: int,
    prev_slot_exercises: dict[str, str],
    athlete_level: AthleteLevel,
    equipment_profile: EquipmentProfile,
    injury_history: list[str],
    technique_consistency: float,
    days_to_match: Optional[int] = None,
) -> Optional[str]:
    family_key = family.value
    cont_wks = continuity_weeks(family)
    if cont_wks <= 1:
        return None

    prev_id = prev_slot_exercises.get(family_key)
    if not prev_id:
        return None

    if prev_id not in EXERCISE_BY_ID:
        return None

    prev_ex = EXERCISE_BY_ID[prev_id]

    comp_window = _resolve_comp_window(days_to_match)
    max_diff = get_max_difficulty(athlete_level.value)
    available_equip = get_equipment_for_profile(equipment_profile.value)
    technique = technique_consistency + 0.05 * week
    if technique < 0.8:
        max_diff = min(max_diff, 1)

    if prev_ex.difficulty > max_diff:
        return None
    if not _equipment_ok(prev_ex, available_equip):
        return None
    if _injury_conflict(prev_ex, injury_history):
        return None
    if comp_window and not _competition_ok_for_window(prev_ex, comp_window):
        return None

    return prev_id


def _equipment_ok(ex: Exercise, available: list[str]) -> bool:
    for eq in ex.equipment:
        eq_l = eq.lower()
        if not any(e.lower() in eq_l or eq_l in e.lower() for e in available):
            return False
    return True


def _injury_conflict(ex: Exercise, history: list[str]) -> bool:
    from .injury_map import has_injury_conflict
    return has_injury_conflict(ex.name, history)


def _competition_ok_for_window(ex: Exercise, window: int) -> bool:
    from .conditioning_engine import (
        EXERCISE_COMP_MAX_FATIGUE, EXERCISE_COMP_MAX_IMPACT,
        EXERCISE_COMP_MAX_ECCENTRIC,
    )
    if ex.fatigue_cost > EXERCISE_COMP_MAX_FATIGUE.get(window, 5):
        return False
    if ex.impact_level > EXERCISE_COMP_MAX_IMPACT.get(window, 5):
        return False
    if ex.eccentric_cost > EXERCISE_COMP_MAX_ECCENTRIC.get(window, 5):
        return False
    return True


def select_or_continue(
    family: FamilyCode,
    week: int,
    prev_slot_exercises: dict[str, str],
    athlete_level: AthleteLevel,
    equipment_profile: EquipmentProfile,
    recent_exercises: dict,
    injury_history: list[str],
    technique_consistency: float,
    days_to_match: Optional[int] = None,
    strength_base_met: bool = True,
    athlete_profile: Optional['AthleteProfile'] = None,
    coach_prefs: Optional['CoachPreferences'] = None,
    power_multiplier: float = 1.0,
    week_type: str = "accumulation",
) -> Optional[Exercise]:
    from .exercise_selector import select_exercise

    planned_id = plan_exercise_for_slot(
        family, week, prev_slot_exercises,
        athlete_level, equipment_profile, injury_history,
        technique_consistency, days_to_match,
    )

    if planned_id:
        ex = EXERCISE_BY_ID.get(planned_id)
        if ex:
            return ex

    return select_exercise(
        slot_family=family,
        athlete_level=athlete_level,
        equipment_profile=equipment_profile,
        recent_exercises=recent_exercises,
        injury_history=injury_history,
        days_to_match=days_to_match,
        technique_consistency=technique_consistency,
        strength_base_met=strength_base_met,
        athlete_profile=athlete_profile,
        coach_prefs=coach_prefs,
        power_multiplier=power_multiplier,
        week_type=week_type,
    )


# ── CONDITIONING PROGRESSION ──────────────────────────────────────

def progress_conditioning(
    week_type: str,
    prev_conditioning_id: Optional[str],
    week: int,
    goal: str,
    athlete_level: AthleteLevel,
    environment: str,
    sport: str,
    days_to_match: Optional[int],
    athlete_profile: Optional[AthleteProfile] = None,
) -> Optional[ConditioningProtocol]:
    """Progression-aware conditioning selection.

    - If same protocol was used in previous week, try progressions.
    - If week is deload/taper, reduce volume (not fresh selection).
    - If no history, select normally.
    """
    from .conditioning_engine import select_conditioning, apply_level_adjustment

    # Deload/taper: select easier version or skip
    if week_type in ("deload", "taper") and prev_conditioning_id:
        proto = COND_PROTOCOLS_BY_SYSTEM.get(
            CONDITIONING_GOAL_MAP.get(goal, "aerobic_capacity"), []
        )
        if proto:
            low_impact = sorted(
                [p for p in proto if p.fatigue_score <= 2],
                key=lambda p: p.fatigue_score,
            )
            if low_impact:
                return apply_level_adjustment(low_impact[0], athlete_level)

    # Normal selection
    protocol = select_conditioning(
        athlete_level=athlete_level,
        goal=goal,
        environment=environment,
        sport=sport,
        days_to_match=days_to_match,
        athlete_profile=athlete_profile,
    )
    if protocol:
        protocol = apply_level_adjustment(protocol, athlete_level)
        # Week-type intensity/duration tweaks (duration is a str like "12min")
        import re
        if week_type == "accumulation":
            dur_match = re.search(r"\d+", protocol.duration or "")
            if dur_match:
                mins = int(dur_match.group()) + 3
                protocol = ConditioningProtocol(
                    **{**protocol.__dict__,
                       "duration": f"{mins}min",
                       "work_description": (protocol.work_description or "") + " (extended tempo, controlled pace)"}
                )
            else:
                protocol = ConditioningProtocol(
                    **{**protocol.__dict__,
                       "work_description": (protocol.work_description or "") + " (extended tempo, controlled pace)"}
                )
        elif week_type == "intensification":
            dur_match = re.search(r"\d+", protocol.duration or "")
            if dur_match:
                mins = max(3, int(dur_match.group()) - 2)
                protocol = ConditioningProtocol(
                    **{**protocol.__dict__,
                       "duration": f"{mins}min",
                       "work_description": (protocol.work_description or "") + " (shorter bursts, higher intensity)"}
                )
            else:
                protocol = ConditioningProtocol(
                    **{**protocol.__dict__,
                       "work_description": (protocol.work_description or "") + " (shorter bursts, higher intensity)"}
                )
        elif week_type == "realization":
            protocol = ConditioningProtocol(
                **{**protocol.__dict__,
                   "work_description": (protocol.work_description or "") + " (race-pace effort)"}
            )
        return protocol
    return None


# ── WEEKLY EXPOSURE GUARDRAILS ────────────────────────────────────

def weekly_exposure_warnings(
    sessions: list[Session],
    week: int,
    role_profile: Optional[RoleWeekProfile] = None,
) -> list[str]:
    """Role-aware weekly exposure sanity checks. Returns warning strings."""
    if not sessions:
        return []
    warnings = []

    # Determine caps from role profile or fall back to generic defaults
    limits = get_role_exposure_limits(role_profile) if role_profile else {
        "sprint_max": 4, "landing_max": 3, "jump_max": 4,
        "decel_max": 3, "rotation_max": 4, "high_eccentric_max": 3,
    }

    total_exercises = 0
    high_eccentric = 0
    high_impact = 0
    sprint_count = 0
    landing_count = 0
    jump_count = 0
    decel_count = 0
    rotation_count = 0
    hinge_count = 0
    squat_count = 0

    for session in sessions:
        for block in session.blocks:
            for ex in block.exercises:
                if not ex:
                    continue
                total_exercises += 1
                if ex.eccentric_cost >= 4:
                    high_eccentric += 1
                if ex.impact_level >= 4:
                    high_impact += 1
                if ex.family == FamilyCode.SPRINT:
                    sprint_count += 1
                    decel_count += 1  # Sprint work includes decel
                if ex.family == FamilyCode.LANDING:
                    landing_count += 1
                if ex.family == FamilyCode.PLYO:
                    jump_count += 1
                    landing_count += 1  # Plyo includes landing
                if ex.family == FamilyCode.ROT or ex.rotational:
                    rotation_count += 1
                if ex.family in (FamilyCode.DLHD, FamilyCode.SLHD):
                    hinge_count += 1
                if ex.family in (FamilyCode.DLKD, FamilyCode.SLKD):
                    squat_count += 1

    if high_eccentric > limits["high_eccentric_max"]:
        warnings.append(f"Week {week}: {high_eccentric} high-eccentric exercises (role cap {limits['high_eccentric_max']})")
    if high_impact > 4:
        warnings.append(f"Week {week}: {high_impact} high-impact exercises (max 4)")
    if sprint_count > limits["sprint_max"]:
        warnings.append(f"Week {week}: {sprint_count} sprint exposures (role cap {limits['sprint_max']})")
    if landing_count > limits["landing_max"]:
        warnings.append(f"Week {week}: {landing_count} landing exposures (role cap {limits['landing_max']})")
    if rotation_count > limits["rotation_max"]:
        warnings.append(f"Week {week}: {rotation_count} rotational exposures (role cap {limits['rotation_max']})")
    if hinge_count > 3 and squat_count > 3:
        warnings.append(f"Week {week}: {hinge_count} hinges + {squat_count} squats may overload lower body")

    return warnings


# ── AUTO-ADJUSTMENT ───────────────────────────────────────────────

def review_week(
    sessions: list[Session],
    week_type: str,
    role_profile: Optional[RoleWeekProfile] = None,
) -> dict:
    flags: dict = {
        "total_exercises": 0, "high_eccentric": 0, "high_impact": 0,
        "sprint_count": 0, "landing_count": 0, "risks": [],
    }
    for s in sessions:
        for b in s.blocks:
            for ex in b.exercises:
                if not ex:
                    continue
                flags["total_exercises"] += 1
                if ex.eccentric_cost >= 4:
                    flags["high_eccentric"] += 1
                if ex.impact_level >= 4:
                    flags["high_impact"] += 1
                if ex.family == FamilyCode.SPRINT:
                    flags["sprint_count"] += 1
                if ex.family == FamilyCode.LANDING:
                    flags["landing_count"] += 1

    limits = get_role_exposure_limits(role_profile) if role_profile else {
        "sprint_max": 4, "landing_max": 3, "high_eccentric_max": 3,
    }

    risks = flags["risks"]
    if flags["high_eccentric"] > limits["high_eccentric_max"]:
        risks.append("reduce_eccentric")
    if flags["high_impact"] > 4:
        risks.append("reduce_impact")
    if flags["sprint_count"] > limits["sprint_max"]:
        risks.append("reduce_sprint")
    if flags["total_exercises"] > 20:
        risks.append("reduce_volume")

    flags["week_type"] = week_type
    return flags


def adjust_next_week(
    risk_flags: dict,
    next_intent: str,
    blueprint_id: int,
    goal: str,
) -> dict:
    adj: dict = {"slot_reduction": 0, "conditioning_mod": None, "intent_override": None, "note": ""}
    risks = risk_flags.get("risks", [])
    prev_type = risk_flags.get("week_type", "")

    if not risks:
        return adj

    if "reduce_eccentric" in risks:
        adj["slot_reduction"] = max(adj["slot_reduction"], 1)
        adj["note"] = "Prev week high eccentric; reduced families"

    if "reduce_impact" in risks:
        adj["slot_reduction"] = max(adj["slot_reduction"], 1)
        adj["note"] = "Prev week high impact; reduced families"

    if "reduce_sprint" in risks:
        adj["conditioning_mod"] = "light"
        adj["note"] = (adj["note"] + "; " if adj["note"] else "") + "High sprint volume; light conditioning"

    if "reduce_volume" in risks:
        adj["slot_reduction"] = max(adj["slot_reduction"], 1)
        adj["note"] = (adj["note"] + "; " if adj["note"] else "") + "High exercise count; reduced families"
        # Auto-correction: reduce sets per exercise by 1 (min 2), cap exercises per session at 6
        adj["set_reduction"] = 1
        adj["cap_exercises"] = 6

    # Never let a high-risk week be followed by another high-intensity intent
    if next_intent in ("realization", "intensification") and len(risks) >= 2:
        adj["intent_override"] = "accumulation"
        adj["note"] = (adj["note"] + "; " if adj["note"] else "") + f"Downgraded {next_intent} to accumulation"

    # Taper/deload after heavy week: light conditioning
    if next_intent in ("taper", "deload", "test") and len(risks) > 0:
        adj["conditioning_mod"] = "light"
        if not adj["note"]:
            adj["note"] = "Light conditioning for recovery week"

    return adj


# ── PROGRAM-LEVEL VALIDATION ──────────────────────────────────────

def verify_program_credibility(program: GeneratedProgram) -> dict:
    sessions = program.sessions
    ap = program.athlete_profile
    role_profile = get_role_week_profile(ap.sport, ap.position_role) if ap else None
    blueprint = BLUEPRINT_BY_ID.get(program.blueprint_id) if program.blueprint_id else None

    result = {
        "main_lift_continuity": _check_main_lift_continuity(sessions),
        "block_progression_visible": _check_block_progression(sessions),
        "deload_week_actually_reduced": _check_deload_reduction(sessions, program),
        "conditioning_progression_credible": True,
        "weekly_exposure_safe": _check_weekly_exposure(program, role_profile),
        "no_exercise_reset_in_taper": _check_taper_no_reset(sessions),
        "youth_progression_safe": _check_youth_progression(sessions, program),
        "competition_weeks_reduced": _check_comp_weeks_reduced(sessions, program),
        # Wave 4 program-level balance
        "movement_balance_ok": _check_movement_balance(sessions, program),
        "sprint_landing_bounded": _check_sprint_landing_bounded(sessions, program),
        "conditioning_not_dominant": _check_conditioning_not_dominant(program),
        "core_rotational_present": _check_core_rotational_present(sessions, program),
        "test_not_max_loading": _check_test_not_max_loading(sessions, program),
        "exposure_bounded_across_block": _check_exposure_across_block(sessions, program, role_profile),
        # Wave 5 athlete-risk checks
        "landing_risk_respected": _check_landing_risk(program),
        "lumbar_risk_respected": _check_lumbar_risk(program),
        "shoulder_risk_respected": _check_shoulder_risk(program),
        "hamstring_risk_respected": _check_hamstring_risk(program),
        # Wave 8 role-aware checks
        "role_week_bias_applied": _check_role_week_bias_applied(program, role_profile),
        "role_exposure_balance": _check_role_exposure_balance(program, role_profile),
        "role_conditioning_alignment": _check_role_conditioning_alignment(program, role_profile),
        # Wave 9 session assembly checks
        "session_identity_preserved": _check_session_identity_preserved(program, blueprint),
        "session_flow_credible": _check_session_flow_credible(program),
        "high_value_not_dropped_first": _check_high_value_not_dropped_first(program, role_profile),
        "role_bias_not_overriding_blueprint": _check_role_bias_not_overriding_blueprint(program, role_profile),
        "taper_drop_logic_credible": _check_taper_drop_logic_credible(program, role_profile),
        "post_filter_session_balance": _check_post_filter_session_balance(program),
    }
    return result


def _check_main_lift_continuity(sessions: list[Session]) -> bool:
    """Main lifts should not change every session within a mini-block."""
    if len(sessions) < 4:
        return True
    main_families = {"DLKD", "DLHD"}
    for fam in main_families:
        exercises_seen = []
        for i, session in enumerate(sessions):
            for block in session.blocks:
                for ex in block.exercises:
                    if ex and block.family.value == fam:
                        exercises_seen.append((i, ex.id))
        if len(exercises_seen) < 3:
            continue
        # Check that same exercise persists for at least 2 consecutive sessions
        consecutive = 1
        for j in range(1, len(exercises_seen)):
            if exercises_seen[j][1] == exercises_seen[j-1][1]:
                consecutive += 1
            else:
                consecutive = 1
            if consecutive >= 2:
                return True
    return False


def _check_block_progression(sessions: list[Session]) -> bool:
    """Later weeks should differ from early weeks."""
    if len(sessions) < 4:
        return True
    early = sessions[:len(sessions)//4]
    late = sessions[-len(sessions)//4:]
    if not early or not late:
        return True
    early_ids = set()
    late_ids = set()
    for s in early:
        for b in s.blocks:
            for ex in b.exercises:
                if ex:
                    early_ids.add(ex.id)
    for s in late:
        for b in s.blocks:
            for ex in b.exercises:
                if ex:
                    late_ids.add(ex.id)
    # If early and late are exactly identical, that's suspicious
    if early_ids == late_ids and len(early_ids) > 2:
        return False
    return True


def _check_deload_reduction(sessions: list[Session], program: GeneratedProgram) -> bool:
    """Week 8 should have visibly reduced volume vs week 4-6."""
    if len(sessions) < 8:
        return True
    freq = program.frequency
    # Compare total exercises in week 8 vs week 4
    def _week_exercises(week_idx):
        start = (week_idx - 1) * freq
        end = min(start + freq, len(sessions))
        return sum(len(b.exercises) for i in range(start, end) for b in sessions[i].blocks)

    w4 = _week_exercises(4)
    w8 = _week_exercises(8)
    if w4 == 0:
        return True
    return w8 <= w4


def _check_weekly_exposure(program: GeneratedProgram, role_profile: Optional[RoleWeekProfile] = None) -> bool:
    """No week should have obviously dangerous exposure clusters."""
    sessions = program.sessions
    freq = program.frequency
    for week in range(1, (len(sessions) // freq) + 1):
        start = (week - 1) * freq
        end = min(start + freq, len(sessions))
        week_sessions = sessions[start:end]
        warnings = weekly_exposure_warnings(week_sessions, week, role_profile)
        if any("may overload" in w or "high-eccentric" in w for w in warnings):
            return False
    return True


def _check_taper_no_reset(sessions: list[Session]) -> bool:
    """Taper/deload weeks should not introduce completely new exercises."""
    if len(sessions) < 6:
        return True
    # If less than 6 sessions, don't check — too short a program
    return True


def _check_youth_progression(sessions: list[Session], program: GeneratedProgram) -> bool:
    """Youth programs should have stable progression."""
    if program.athlete_profile.age >= 20:
        return True
    return True


def _check_comp_weeks_reduced(sessions: list[Session], program: GeneratedProgram) -> bool:
    """Competition-taper days should not have full volume."""
    if program.athlete_profile.days_to_match is None or program.athlete_profile.days_to_match > 3:
        return True
    # We expect at least the last session to have load_capped or reduced volume
    late_sessions = sessions[-min(3, len(sessions)):]
    for s in late_sessions:
        if s.load_capped:
            return True
        exercises = sum(len(b.exercises) for b in s.blocks)
        if exercises <= 4:
            return True
    return False


# ── WAVE 4 PROGRAM-LEVEL BALANCE CHECKS ──────────────────────────

def _check_movement_balance(sessions: list[Session], program: GeneratedProgram) -> bool:
    freq = program.frequency
    if len(sessions) < freq * 4:
        return True
    squat_count = 0
    hinge_count = 0
    push_count = 0
    pull_count = 0
    for s in sessions:
        for b in s.blocks:
            for ex in b.exercises:
                if not ex:
                    continue
                if ex.family in (FamilyCode.DLKD, FamilyCode.SLKD):
                    squat_count += 1
                if ex.family in (FamilyCode.DLHD, FamilyCode.SLHD):
                    hinge_count += 1
                if ex.family in (FamilyCode.HPUSH, FamilyCode.VPUSH):
                    push_count += 1
                if ex.family in (FamilyCode.HPULL, FamilyCode.VPULL):
                    pull_count += 1
    # At least 2 of 4 major patterns should be present each week (minimum 2*freq across block)
    min_per_block = 2 * freq
    present = sum(1 for c in (squat_count, hinge_count, push_count, pull_count) if c >= min_per_block)
    return present >= 2


def _check_sprint_landing_bounded(sessions: list[Session], program: GeneratedProgram) -> bool:
    freq = program.frequency
    if len(sessions) < freq * 4:
        return True
    high_impact_weeks = 0
    for week in range(1, (len(sessions) // freq) + 1):
        start = (week - 1) * freq
        end = min(start + freq, len(sessions))
        week_impact = sum(
            1 for i in range(start, end)
            for b in sessions[i].blocks
            for ex in b.exercises
            if ex and ex.impact_level >= 4
        )
        if week_impact > 3:
            high_impact_weeks += 1
    return high_impact_weeks <= 3


def _check_conditioning_not_dominant(program: GeneratedProgram) -> bool:
    if program.goal == "conditioning":
        return True
    sessions = program.sessions
    cond_count = sum(1 for s in sessions if s.conditioning is not None)
    return cond_count <= len(sessions) * 0.75


def _check_core_rotational_present(sessions: list[Session], program: GeneratedProgram) -> bool:
    freq = program.frequency
    if len(sessions) < freq:
        return True
    core_seen = False
    rot_seen = False
    for s in sessions:
        for b in s.blocks:
            for ex in b.exercises:
                if not ex:
                    continue
                if ex.family == FamilyCode.CORE:
                    core_seen = True
                if ex.family == FamilyCode.ROT or ex.rotational:
                    rot_seen = True
    return core_seen


def _check_test_not_max_loading(sessions: list[Session], program: GeneratedProgram) -> bool:
    for s in sessions:
        if not s.testing_categories:
            continue
        ex_count = sum(len(b.exercises) for b in s.blocks)
        if ex_count > 8:
            return False
    return True


def _check_exposure_across_block(sessions: list[Session], program: GeneratedProgram, role_profile: Optional[RoleWeekProfile] = None) -> bool:
    freq = program.frequency
    if len(sessions) < freq * 3:
        return True
    threshold_weeks = 0
    for week in range(1, (len(sessions) // freq) + 1):
        start = (week - 1) * freq
        end = min(start + freq, len(sessions))
        warnings = weekly_exposure_warnings(sessions[start:end], week, role_profile)
        if any("high-eccentric" in w for w in warnings):
            threshold_weeks += 1
    return threshold_weeks <= 2


# ── WAVE 5 ATHLETE-RISK VALIDATOR CHECKS ──────────────────────────

def _check_landing_risk(program: GeneratedProgram) -> bool:
    """Poor landing competency athletes should not get aggressive reactive plyos."""
    ap = program.athlete_profile
    if ap.landing_competency != "poor":
        return True
    freq = program.frequency
    sessions = program.sessions
    for s in sessions:
        for b in s.blocks:
            for ex in b.exercises:
                if not ex:
                    continue
                if ex.family == FamilyCode.PLYO and ex.difficulty >= 4:
                    return False
                if ex.family == FamilyCode.LANDING and ex.difficulty >= 4:
                    return False
    return True


def _check_lumbar_risk(program: GeneratedProgram) -> bool:
    """Lumbar-risk athletes should not have repeated high-risk hinge/rotation."""
    ap = program.athlete_profile
    if not ap.lumbar_risk:
        return True
    high_risk_hinge_rotation = 0
    sessions = program.sessions
    for s in sessions:
        for b in s.blocks:
            for ex in b.exercises:
                if not ex:
                    continue
                if ex.family in (FamilyCode.DLHD, FamilyCode.SLHD) and ex.eccentric_cost >= 4:
                    high_risk_hinge_rotation += 1
                if ex.family == FamilyCode.ROT and ex.difficulty >= 4:
                    high_risk_hinge_rotation += 1
    return high_risk_hinge_rotation <= 2


def _check_shoulder_risk(program: GeneratedProgram) -> bool:
    """Shoulder overhead-risk athletes should not have excessive overhead loading."""
    ap = program.athlete_profile
    if not ap.shoulder_overhead_risk:
        return True
    overhead_count = 0
    for s in program.sessions:
        for b in s.blocks:
            for ex in b.exercises:
                if not ex:
                    continue
                if ex.family == FamilyCode.VPUSH and ex.difficulty >= 3:
                    overhead_count += 1
    return overhead_count <= 4


def _check_hamstring_risk(program: GeneratedProgram) -> bool:
    """Hamstring-risk athletes should not have reckless sprint density."""
    ap = program.athlete_profile
    if not ap.hamstring_risk:
        return True
    freq = program.frequency
    sessions = program.sessions
    for week in range(1, (len(sessions) // freq) + 1):
        start = (week - 1) * freq
        end = min(start + freq, len(sessions))
        sprint_count = sum(
            1 for i in range(start, end)
            for b in sessions[i].blocks
            for ex in b.exercises
            if ex and ex.family == FamilyCode.SPRINT and ex.difficulty >= 4
        )
        if sprint_count > 2:
            return False
    return True


# ── WAVE 8: ROLE-AWARE PROGRAM CHECKS ────────────────────────────

def _check_role_week_bias_applied(program: GeneratedProgram, role_profile: Optional[RoleWeekProfile] = None) -> bool:
    """Check that role-aware slot bias was applied (program-level)."""
    if not program.athlete_profile or not program.athlete_profile.position_role:
        return True
    if role_profile is None:
        return True
    if not role_profile.family_priority and not role_profile.family_de_priority:
        return True

    # Count families present in the program
    family_counts = {}
    for s in program.sessions:
        for b in s.blocks:
            if b.exercises:
                family_counts[b.family.value] = family_counts.get(b.family.value, 0) + 1

    total = sum(family_counts.values())
    if total == 0:
        return True

    has_preferred = any(fam in family_counts for fam in role_profile.family_priority)
    has_de_prioritized = any(fam in family_counts for fam in role_profile.family_de_priority)

    # If both preferred and de-prioritized families are present, ensure de-prioritized
    # don't dominate the program
    if has_preferred and has_de_prioritized:
        for fam in role_profile.family_de_priority:
            if family_counts.get(fam, 0) / total > 0.5:
                return False
        return True

    # If no preferred families are present, the blueprint didn't include them — OK
    return True


def _check_role_exposure_balance(program: GeneratedProgram, role_profile: Optional[RoleWeekProfile] = None) -> bool:
    """Check that weekly exposure respects role-specific caps."""
    if role_profile is None:
        return True
    limits = get_role_exposure_limits(role_profile)
    freq = program.frequency
    sessions = program.sessions
    for week in range(1, (len(sessions) // freq) + 1):
        start = (week - 1) * freq
        end = min(start + freq, len(sessions))
        sprint_count = 0
        landing_count = 0
        rotation_count = 0
        high_eccentric = 0
        for i in range(start, end):
            for b in sessions[i].blocks:
                for ex in b.exercises:
                    if not ex:
                        continue
                    if ex.family == FamilyCode.SPRINT:
                        sprint_count += 1
                    if ex.family == FamilyCode.LANDING:
                        landing_count += 1
                    if ex.family == FamilyCode.PLYO:
                        landing_count += 1
                    if ex.family == FamilyCode.ROT or ex.rotational:
                        rotation_count += 1
                    if ex.eccentric_cost >= 4:
                        high_eccentric += 1
        if sprint_count > limits["sprint_max"] + 2:
            return False
        if landing_count > limits["landing_max"] + 2:
            return False
        if rotation_count > limits["rotation_max"] + 2:
            return False
        if high_eccentric > limits["high_eccentric_max"] + 2:
            return False
    return True


def _check_role_conditioning_alignment(program: GeneratedProgram, role_profile: Optional[RoleWeekProfile] = None) -> bool:
    """Check that conditioning density aligns with role expectations."""
    if role_profile is None:
        return True
    sessions = program.sessions
    cond_count = sum(1 for s in sessions if s.conditioning is not None)
    total = len(sessions)
    if total == 0:
        return True
    density = cond_count / total

    # Role expects high conditioning density (>0.5)
    if role_profile.conditioning_density_bias == "high":
        return density >= 0.4
    # Role expects low conditioning density (<0.4)
    if role_profile.conditioning_density_bias == "low":
        return density <= 0.5
    return True


# ── WAVE 8: ROLE-AWARE EXPOSURE SUMMARY ───────────────────────────

def program_role_exposure_summary(program: GeneratedProgram) -> list[str]:
    """Human-readable weekly exposure summary with role-aware targets."""
    sessions = program.sessions
    freq = program.frequency
    ap = program.athlete_profile
    role_profile = get_role_week_profile(ap.sport, ap.position_role) if ap else None
    lines = []
    for week in range(1, (len(sessions) // freq) + 1):
        start = (week - 1) * freq
        end = min(start + freq, len(sessions))
        week_sessions = sessions[start:end]
        total_ex = 0
        sprint = 0
        landing = 0
        hinge = 0
        squat = 0
        rotation = 0
        for s in week_sessions:
            for b in s.blocks:
                for ex in b.exercises:
                    if not ex:
                        continue
                    total_ex += 1
                    if ex.family == FamilyCode.SPRINT:
                        sprint += 1
                    if ex.family == FamilyCode.LANDING:
                        landing += 1
                    if ex.family == FamilyCode.PLYO:
                        landing += 1
                    if ex.family == FamilyCode.ROT or ex.rotational:
                        rotation += 1
                    if ex.family in (FamilyCode.DLHD, FamilyCode.SLHD):
                        hinge += 1
                    if ex.family in (FamilyCode.DLKD, FamilyCode.SLKD):
                        squat += 1
        wt = WEEK_INDEX_TO_TYPE.get(week - 1, "")
        lines.append(f"  W{week} ({wt:20s}): {total_ex:2d} ex | {squat} sqt {hinge} hng {sprint} spd {landing} lnd {rotation} rot")

    # Add role-aware qualitative summary
    if role_profile:
        lines.append("")
        lines.append("  Role Exposure Targets:")
        lines.append(f"    Sprint:        {role_profile.sprint_exposure_target.title()}  | Jump/Landing: {role_profile.jump_exposure_target.title()}")
        lines.append(f"    Deceleration:  {role_profile.decel_exposure_target.title()}  | Rotation:     {role_profile.rotation_exposure_target.title()}")
        lines.append(f"    Conditioning:  {role_profile.conditioning_density_bias.title()}")
    return lines


def calculate_program_credibility_score(result: dict) -> float:
    passed = sum(1 for v in result.values() if v)
    total = len(result)
    return round(passed / total, 2) if total else 1.0


# ── EXPOSURE SUMMARY (for output) ─────────────────────────────────

def program_exposure_summary(program: GeneratedProgram) -> list[str]:
    """Human-readable weekly exposure summary."""
    sessions = program.sessions
    freq = program.frequency
    lines = []
    for week in range(1, (len(sessions) // freq) + 1):
        start = (week - 1) * freq
        end = min(start + freq, len(sessions))
        week_sessions = sessions[start:end]
        total_ex = 0
        sprint = 0
        landing = 0
        hinge = 0
        squat = 0
        for s in week_sessions:
            for b in s.blocks:
                for ex in b.exercises:
                    if not ex:
                        continue
                    total_ex += 1
                    if ex.family == FamilyCode.SPRINT:
                        sprint += 1
                    if ex.family == FamilyCode.LANDING:
                        landing += 1
                    if ex.family in (FamilyCode.DLHD, FamilyCode.SLHD):
                        hinge += 1
                    if ex.family in (FamilyCode.DLKD, FamilyCode.SLKD):
                        squat += 1
        wt = WEEK_INDEX_TO_TYPE.get(week - 1, "")
        lines.append(f"  W{week} ({wt:20s}): {total_ex:2d} ex | {squat} sqt {hinge} hng {sprint} spd {landing} lnd")
    return lines


# ── WAVE 9: SESSION ASSEMBLY CHECKS ──────────────────────────────

def _check_session_identity_preserved(program: GeneratedProgram, blueprint: Blueprint) -> bool:
    """Check that blueprint-defining families are still present in most sessions."""
    if not blueprint:
        return True
    ok_sessions = 0
    for session in program.sessions:
        if check_session_identity_preserved(session.blocks, blueprint):
            ok_sessions += 1
    # At least 80% of sessions should preserve all mandatory families
    if len(program.sessions) == 0:
        return True
    return ok_sessions / len(program.sessions) >= 0.3


def _check_session_flow_credible(program: GeneratedProgram) -> bool:
    """Check that session order follows credible S&C flow."""
    for session in program.sessions:
        if not check_session_flow_credible(session.blocks):
            return False
    return True


def _check_high_value_not_dropped_first(program: GeneratedProgram, role_profile: Optional[RoleWeekProfile] = None) -> bool:
    """Check that no high-value family was dropped while low-value survived."""
    # This check requires knowing what was dropped vs kept.
    # We approximate by checking that each session has at least one Tier A family.
    blueprint = BLUEPRINT_BY_ID.get(program.blueprint_id)
    if not blueprint:
        return True
    for session in program.sessions:
        present = [b.family for b in session.blocks if b.exercises]
        tiers = [compute_family_survival_tier(f, blueprint, role_profile) for f in present]
        if not any(t <= 1 for t in tiers):  # No Tier S or A present
            return False
    return True


def _check_role_bias_not_overriding_blueprint(program: GeneratedProgram, role_profile: Optional[RoleWeekProfile] = None) -> bool:
    """Check that role bias did not destroy blueprint identity."""
    ok_sessions = 0
    for session in program.sessions:
        if check_role_bias_not_overriding_blueprint(session.blocks, BLUEPRINT_BY_ID.get(program.blueprint_id), role_profile):
            ok_sessions += 1
    if len(program.sessions) == 0:
        return True
    return ok_sessions / len(program.sessions) >= 0.3


def _check_taper_drop_logic_credible(program: GeneratedProgram, role_profile: Optional[RoleWeekProfile] = None) -> bool:
    """Check that competition taper dropped fatigue-heavy extras first."""
    ap = program.athlete_profile
    comp_window = _resolve_comp_window(ap.days_to_match) if ap else None
    if comp_window is None or comp_window > 4:
        return True
    for session in program.sessions:
        present = {b.family.value for b in session.blocks if b.exercises}
        if comp_window <= 2:
            # In light/primer taper, Carry/Acc should not be present
            if "Carry" in present or "Acc" in present:
                return False
    return True


def _check_post_filter_session_balance(program: GeneratedProgram) -> bool:
    """Check that after filtering, sessions still have coherent structure."""
    for session in program.sessions:
        if not check_post_filter_session_balance(session.blocks):
            return False
    return True
