"""FORGE program generator — single entry point."""
from __future__ import annotations
from typing import Optional
from .models import (
    AthleteProfile, AthleteLevel, EquipmentProfile,
    SeasonPhase, Objective, GeneratedProgram, Session,
    SessionBlock, FamilyCode, Exercise, CoachPreferences,
)
from .data import (
    BLUEPRINTS, get_max_difficulty, get_equipment_for_profile,
    EXERCISE_BY_ID, EXERCISES_BY_FAMILY, SELECTION_PRIORITIES,
)
from .blueprint_engine import (
    select_blueprint, determine_level, resolve_slots, get_equipment_profile,
    apply_time_constraint,
)
from .exercise_selector import select_exercise
from .test_adjustment_engine import get_adjustments
from .conditioning_engine import generate_conditioning, _resolve_comp_window
from .renderer import render_program, render_coach_program
from .validator import verify_credibility, calculate_credibility_score
from .warmup_engine import select_warmup
from .recovery_engine import select_recovery
from .data import BLUEPRINT_BY_ID
from .models import WarmupProtocol, RecoveryProtocol, Session, OBJECTIVE_REST_MAP, OBJECTIVE_INTENSITY_MAP
from .prescription_rules import get_prescription, resolve_comp_window
from .progression_engine import (
    select_or_continue, WEEK_INDEX_TO_TYPE, progress_conditioning,
    verify_program_credibility, calculate_program_credibility_score,
    program_exposure_summary, plan_weeks, plan_testing,
    review_week, adjust_next_week,
)
from .athlete_profile_rules import (
    get_weekly_emphasis_bias, describe_weekly_bias,
    get_role_weekly_notes,
)
from .role_week_planning import (
    get_role_week_profile, apply_role_slot_bias,
    should_add_conditioning_for_role, get_role_week_notes,
    render_role_week_summary, get_role_exposure_limits,
)
from .session_rules import (
    check_session_identity_preserved,
    check_session_flow_credible,
    check_high_value_families_not_dropped_before_low_value,
    check_role_bias_not_overriding_blueprint,
    check_taper_drop_logic_credible,
    check_post_filter_session_balance,
    check_repeated_family_progression_credible,
)
from .session_assembly import (
    apply_time_constraint_v2,
    apply_competition_taper,
    rebuild_session_flow,
    rebalance_session_blocks,
    get_within_week_variation_family,
    get_within_week_variation_rationale,
    session_composition_rationale,
    resolve_weekly_schedule,
    adjust_slots_for_calendar,
    apply_coach_preferences,
    apply_sprint_exposure_floor,
    apply_sprint_multiplier,
)


def _sport_to_environment(sport: str) -> str:
    """Map sport to training environment."""
    sport_lower = sport.lower()
    if any(keyword in sport_lower for keyword in ["tennis", "badminton", "basketball", "volleyball", "squash"]):
        return "court"
    elif any(keyword in sport_lower for keyword in ["soccer", "football", "rugby", "cricket", "hockey", "track", "field"]):
        return "ground"
    else:
        return "gym"


def _adjust_session_type_for_environment(session_type: str, environment: str, blueprint_id: int = 1) -> str:
    """Adjust session type based on environment."""
    if session_type == "speed" and environment == "court":
        return "court_speed"
    if session_type == "strength" and environment == "court":
        return "court_strength"
    return session_type


def _slot_compact_factor(family: FamilyCode, base_factor: float) -> float:
    """Return family-aware compact factor. Primary strength compacted less."""
    if base_factor >= 1.0:
        return 1.0
    # ponytail: Phase-2 primary strength families get +0.15 buffer
    if family.value in ("DLKD", "DLHD"):
        return min(1.0, base_factor + 0.15)
    # HPush/HPull are Phase-2 primary in session flow, +0.10 buffer
    if family.value in ("HPush", "HPull"):
        return min(1.0, base_factor + 0.10)
    # Accessory fatigue-heavy families get trimmed more aggressively
    if family.value in ("Carry", "Acc", "Rot"):
        return max(0.4, base_factor - 0.10)
    return base_factor


def _compact_presc_sets(presc: Prescription, factor: float) -> None:
    """Scale prescription sets by factor, modifiying in-place."""
    import re
    nums = re.findall(r"\d+", presc.sets)
    if not nums:
        return
    ints = [int(n) for n in nums]
    scaled = [max(1, round(n * factor)) for n in ints]
    if len(scaled) == 1:
        presc.sets = str(scaled[0])
    elif scaled[0] == scaled[1]:
        presc.sets = str(scaled[0])
    else:
        presc.sets = f"{scaled[0]}-{scaled[1]}"


def _rest_sec_to_str(secs: int) -> str:
    if secs >= 180:
        return f"{secs // 60}-{secs // 60 + 1}min"
    return f"{secs}s"


def _get_session_type(athlete: AthleteProfile, blueprint_id: int) -> str:
    goal = athlete.goal
    if goal in ("speed", "conditioning"):
        return "conditioning"
    if blueprint_id == 4 or goal == "power":
        return "power"
    if blueprint_id == 10 or goal == "speed":
        return "speed"
    if athlete.days_to_match == 0:
        return "competition"
    if blueprint_id == 13 or goal == "deload":
        return "deload"
    # Differentiate strength types
    if blueprint_id == 5:  # Upper / Lower Split
        # Default to full body strength — each day alternates, warmup covers both
        return "strength"
    if blueprint_id == 1:  # Full Body Strength
        return "strength"
    if blueprint_id in (2, 3):  # Strength + Power, Strength + Conditioning
        return "strength"
    return "strength"


def _build_light_session(athlete: AthleteProfile, level: AthleteLevel,
                          equipment: EquipmentProfile, slots: list[FamilyCode],
                          running_recent: dict, days_to_match: Optional[int] = None,
                          blueprint_id: int = 1) -> Session:
    half_slots = slots[:max(3, len(slots) // 2)]
    blocks = []
    comp_window = resolve_comp_window(days_to_match)
    for family in half_slots:
        ex = select_exercise(
            family, level, equipment, running_recent, athlete.injury_history,
            days_to_match, technique_consistency=athlete.technique_consistency,
            strength_base_met=athlete.strength_base_met,
            athlete_profile=athlete,
        )
        if ex:
            running_recent[ex.id] = {"last_used": "light_session", "technique_score": 1.0}
        obj = ex.objective.value if ex else "STR"
        block = SessionBlock(
            family=family,
            family_name=family.value,
            exercises=[ex] if ex else [],
            target_intensity=OBJECTIVE_INTENSITY_MAP.get(obj),
            rest_period=OBJECTIVE_REST_MAP.get(obj),
        )
        if ex:
            presc = get_prescription(ex, level, blueprint_id, comp_window, week=1, week_type="light", athlete_profile=athlete)
            block.prescription = presc
            block.rest_period = _rest_sec_to_str(presc.rest_seconds)
        blocks.append(block)
    total_duration = sum(len(b.exercises) * 5 for b in blocks)
    return Session(blocks=blocks, total_duration_min=total_duration)


def _build_recovery_session() -> Session:
    return Session(blocks=[], total_duration_min=0)


def generate_program(athlete: AthleteProfile) -> GeneratedProgram:
    days_to_match = athlete.days_to_match
    if days_to_match == 0:
        return _generate_recovery_program(athlete)
    if days_to_match == 1:
        return _generate_light_program(athlete)

    blueprint = select_blueprint(athlete)
    level = determine_level(athlete)
    equipment = athlete.equipment_profile
    slots = resolve_slots(blueprint, level)

    # Frequency-based slot adaptation: spread or compress families per session
    freq = athlete.frequency_per_week
    total_families = len(blueprint.slot_order)
    fam_per_session = max(3, min(total_families, round(total_families * 3.0 / freq)))
    preferred = min(getattr(athlete, 'preferred_families', 6), fam_per_session)
    avail_min = getattr(athlete, 'available_minutes', 60)
    comp_window = _resolve_comp_window(days_to_match)

    # Wave 15: test-driven adjustments
    adjustments = get_adjustments(athlete)
    athlete.test_adjustments = adjustments

    # Wave 8: role-aware week profile (needed before time constraint)
    role_profile = get_role_week_profile(athlete.sport, athlete.position_role)

    # Volume taper: reduce families near competition
    if comp_window == 4:  # MODERATE (4-5 days)
        preferred = min(preferred, 7)
    elif comp_window == 2:  # LIGHT (2-3 days)
        preferred = min(preferred, 5)
    elif comp_window == 1:  # PRIMER (<=1 day)
        preferred = min(preferred, 4)

    # Wave 11a — Season-phase volume scaling
    if athlete.season_phase == SeasonPhase.OFF_SEASON:
        preferred = min(preferred, 7)
        avail_min = min(avail_min, 90)
    elif athlete.season_phase == SeasonPhase.PRE_SEASON:
        preferred = min(preferred, 6)
        avail_min = min(avail_min, 75)
    elif athlete.season_phase == SeasonPhase.IN_SEASON:
        preferred = min(preferred, 6)
        avail_min = min(avail_min, 55)
        if freq > 2:
            freq = 2
    elif athlete.season_phase == SeasonPhase.TRANSITION:
        preferred = min(preferred, 5)
        avail_min = min(avail_min, 60)

    # Wave 9: use tier-aware time constraint with blueprint awareness
    slots, time_drop_notes, compact_factor = apply_time_constraint_v2(
        slots, blueprint, avail_min, preferred, comp_window, role_profile
    )
    # In-season: additional volume reduction (~35%) regardless of time constraint
    if athlete.season_phase == SeasonPhase.IN_SEASON:
        compact_factor = min(compact_factor, 0.65)
    # Also apply competition taper if needed
    if comp_window and comp_window <= 4:
        slots, taper_notes = apply_competition_taper(slots, blueprint, comp_window, role_profile)
        time_drop_notes.extend(taper_notes)

    # Rebuild session flow after time/taper drops
    slots = rebuild_session_flow(slots, blueprint)

    # Wave 8: apply role slot bias to final slot ordering
    slots = apply_role_slot_bias(slots, role_profile)

    # Wave 5: athlete profile weekly bias
    weekly_bias = get_weekly_emphasis_bias(athlete)
    personalization_notes = describe_weekly_bias(weekly_bias)

    # Wave 6: role-based weekly notes
    role_notes = get_role_weekly_notes(athlete.sport, athlete.position_role)
    personalization_notes.extend(role_notes)

    sessions = []
    running_recent: dict[str, dict] = {}
    prev_slot_exercises: dict[str, str] = {}

    weeks = athlete.program_length_weeks
    conditioning_goal = _get_conditioning_goal(athlete.goal)
    session_type = _get_session_type(athlete, blueprint.id)

    # Wave 4: deterministic week structure
    week_plan = plan_weeks(blueprint.id, level, athlete.goal, athlete.age, days_to_match)
    test_plan = plan_testing(week_plan, blueprint.id, level, athlete.goal, athlete.age, days_to_match)

    weekly_loads: list[int] = []
    next_week_adjustments: dict[int, dict] = {}
    program_adjustments: list[str] = time_drop_notes
    testing_summary: list[tuple[int, list[str]]] = []
    if athlete.season_phase == SeasonPhase.IN_SEASON:
        personalization_notes.append("In-season maintenance mode – volume reduced, intensity maintained.")

    for week in range(1, weeks + 1):
        week_type = week_plan[week - 1] if week <= len(week_plan) else "accumulation"

        # Apply auto-adjustments for this week
        adj = next_week_adjustments.get(week, {})
        slot_reduction = adj.get("slot_reduction", 0)
        cond_mod = adj.get("conditioning_mod")
        intent_override = adj.get("intent_override")
        adj_note = adj.get("note", "")

        if intent_override:
            week_type = intent_override
        effective_slots = slots[:max(3, len(slots) - slot_reduction)] if slot_reduction else slots
        effective_cond_goal = _get_conditioning_mod(conditioning_goal, cond_mod)

        # Check if this session/day should have testing
        week_tests = test_plan.get(week, [])

        # Wave 12: calendar-aware placement
        schedule = resolve_weekly_schedule(
            athlete.match_day, athlete.team_training_days,
            athlete.heavy_field_days, athlete.travel_days, freq,
        )

        week_exercises = []
        for day in range(1, freq + 1):
            day_ctx = schedule[day - 1] if day <= len(schedule) else None
            day_slots = effective_slots
            cal_notes: list[str] = []
            if day_ctx:
                day_slots, cal_notes = adjust_slots_for_calendar(effective_slots, day_ctx)

            session = _build_session(
                athlete=athlete,
                level=level,
                equipment=equipment,
                slots=day_slots,
                week=week,
                day=day,
                freq=freq,
                recent_exercises=running_recent,
                prev_slot_exercises=prev_slot_exercises,
                conditioning_goal=effective_cond_goal,
                days_to_match=days_to_match,
                blueprint_id=blueprint.id,
                week_type=week_type,
                testing_categories=week_tests,
                adjustment_note=adj_note,
                role_profile=role_profile,
                compact_factor=compact_factor,
                coach_prefs=athlete.coach_preferences,
                test_adjustments=athlete.test_adjustments,
                set_reduction=adj.get("set_reduction", 0),
                cap_exercises=adj.get("cap_exercises", 0),
            )
            sessions.append(session)
            week_exercises.extend([ex for b in session.blocks for ex in b.exercises if ex])

        # Wave 14 — Apply coach preferences at week level
        coach_prefs = athlete.coach_preferences
        if coach_prefs:
            week_sessions = sessions[-(freq if freq <= len(sessions) else len(sessions)):]
            week_sessions = apply_sprint_exposure_floor(list(week_sessions), coach_prefs, week)
            for i in range(len(week_sessions)):
                sidx = max(0, len(sessions) - len(week_sessions)) + i
                sessions[sidx] = apply_coach_preferences(week_sessions[i], coach_prefs, week, freq)

            if cal_notes:
                for note in cal_notes:
                    program_adjustments.append(f"Week {week}, Day {day}: {note}")
                    personalization_notes.append(f"Week {week}, Day {day}: {note}")

        if adj_note:
            program_adjustments.append(f"Week {week}: {adj_note}")

        # Track testing for summary
        if week_tests:
            testing_summary.append((week, week_tests))

        # Compute weekly load proxy (sum of difficulty * 2)
        week_load = sum(ex.difficulty * 2 for ex in week_exercises)
        weekly_loads.append(week_load)

        # Wave 4: review week and plan adjustment for next week
        if week < weeks:
            week_sessions = sessions[-(freq if freq <= len(sessions) else len(sessions)):]
            risk_flags = review_week(week_sessions, week_type, role_profile)
            next_adj = adjust_next_week(risk_flags, week_plan[week] if week < len(week_plan) else "accumulation", blueprint.id, athlete.goal)
            if next_adj.get("slot_reduction") or next_adj.get("conditioning_mod") or next_adj.get("intent_override"):
                next_week_adjustments[week + 1] = next_adj

    # Load spike prevention: cap week-over-week at 15%
    for i in range(1, len(weekly_loads)):
        prev = weekly_loads[i - 1] or 1
        curr = weekly_loads[i]
        if curr > prev * 1.15:
            scale = (prev * 1.15) / curr
            weekly_loads[i] = int(prev * 1.15)
            for j in range(min(freq, len(sessions))):
                sess_idx = (i - 1) * freq + j
                if sess_idx < len(sessions):
                    sessions[sess_idx].load_capped = True

    check = verify_credibility(sessions[0], athlete)
    credibility = calculate_credibility_score(check)

    environment = _sport_to_environment(athlete.sport)
    adjusted_session_type = _adjust_session_type_for_environment(session_type, environment, blueprint.id)
    warmup = select_warmup(athlete, adjusted_session_type, environment)
    recovery = select_recovery(athlete, session_type)

    # Wave 8: role week bias notes
    role_week_notes = get_role_week_notes(athlete.sport, athlete.position_role)
    personalization_notes.extend(role_week_notes)

    program = GeneratedProgram(
        athlete=f"{athlete.sport} Athlete ({athlete.goal})",
        blueprint_id=blueprint.id,
        blueprint_name=blueprint.name.value,
        level=level.value,
        duration=weeks,
        frequency=freq,
        goal=athlete.goal,
        equipment_profile=equipment.value,
        sessions=sessions,
        athlete_profile=athlete,
        credibility_score=credibility,
        warmup=warmup,
        recovery=recovery,
    )

    program_checks = verify_program_credibility(program)
    program_score = calculate_program_credibility_score(program_checks)
    program.credibility_score = program_score

    # Wave 6: prescription personalization notes
    from .prescription_rules import describe_prescription_modifiers
    fp = athlete.force_profile
    if fp == "force_deficient":
        personalization_notes.append("Force-deficient profile -> lower-rep strength prescriptions; heavier loading bias")
    elif fp == "velocity_deficient":
        personalization_notes.append("Velocity-deficient profile -> velocity-friendly loading; explosive emphasis")
    if athlete.landing_competency == "poor":
        personalization_notes.append("Landing competency poor -> plyo sets capped; controlled landing prescription")
    if athlete.patellar_tendon_risk:
        personalization_notes.append("Patellar tendon risk -> reactive jump density reduced")
    if athlete.hamstring_risk:
        personalization_notes.append("Hamstring risk -> sprint density capped; controlled exposure")
    if athlete.lumbar_risk:
        personalization_notes.append("Lumbar risk -> hinge dosing lumbar-aware; spinal loading moderated")

    # Wave 7: block review notes
    if hasattr(athlete, 'block_response') and athlete.block_response is not None:
        br = athlete.block_response
        # Build a concise block review string
        notes_part = "; ".join(br.notes) if br.notes else ""
        shift_part = br.recommended_shift.strip()
        if notes_part and shift_part:
            block_review_note = f"Block Review: {notes_part}; {shift_part}"
        elif notes_part:
            block_review_note = f"Block Review: {notes_part}"
        elif shift_part:
            block_review_note = f"Block Review: {shift_part}"
        else:
            block_review_note = None
        if block_review_note:
            personalization_notes.append(block_review_note)

    program.personalization_notes = personalization_notes

    return program


def _generate_recovery_program(athlete: AthleteProfile) -> GeneratedProgram:
    recovery = select_recovery(athlete, "strength")
    return GeneratedProgram(
        athlete=f"{athlete.sport} Athlete (Recovery — Match Day)",
        blueprint_id=13,
        blueprint_name="Deload / Active Recovery",
        level="N/A",
        duration=0,
        frequency=0,
        goal="recovery",
        equipment_profile=athlete.equipment_profile.value,
        sessions=[_build_recovery_session()],
        athlete_profile=athlete,
        credibility_score=1.0,
        warmup=None,
        recovery=recovery,
    )


def _generate_light_program(athlete: AthleteProfile) -> GeneratedProgram:
    days_to_match = athlete.days_to_match
    blueprint = select_blueprint(athlete)
    level = determine_level(athlete)
    equipment = athlete.equipment_profile
    slots = resolve_slots(blueprint, level)

    preferred = getattr(athlete, 'preferred_families', 6)
    avail_min = getattr(athlete, 'available_minutes', 30)
    slots = apply_time_constraint(slots, avail_min, preferred)

    running_recent: dict[str, dict] = {}
    session = _build_light_session(athlete, level, equipment, slots, running_recent, days_to_match, blueprint.id)
    session_type = _get_session_type(athlete, blueprint.id)

    check = verify_credibility(session, athlete)
    credibility = calculate_credibility_score(check)
    environment = _sport_to_environment(athlete.sport)
    adjusted_session_type = _adjust_session_type_for_environment(session_type, environment, blueprint.id)
    warmup = select_warmup(athlete, adjusted_session_type, environment)
    recovery = select_recovery(athlete, session_type)

    return GeneratedProgram(
        athlete=f"{athlete.sport} Athlete (Pre-Match — Light)",
        blueprint_id=blueprint.id,
        blueprint_name=blueprint.name.value,
        level=level.value,
        duration=1,
        frequency=1,
        goal="light_session",
        equipment_profile=equipment.value,
        sessions=[session],
        athlete_profile=athlete,
        credibility_score=credibility,
        warmup=warmup,
        recovery=recovery,
    )


def _build_session(
    athlete: AthleteProfile,
    level: AthleteLevel,
    equipment: EquipmentProfile,
    slots: list[FamilyCode],
    week: int,
    day: int,
    freq: int,
    recent_exercises: dict[str, dict],
    prev_slot_exercises: dict[str, str],
    conditioning_goal: str = "aerobic_capacity",
    days_to_match: Optional[int] = None,
    blueprint_id: int = 1,
    week_type: str = "accumulation",
    testing_categories: Optional[list[str]] = None,
    adjustment_note: str = "",
    role_profile: Optional[object] = None,
    compact_factor: float = 1.0,
    coach_prefs: Optional[CoachPreferences] = None,
    test_adjustments: Optional[dict] = None,
    set_reduction: int = 0,
    cap_exercises: int = 0,
) -> Session:
    blocks: list[SessionBlock] = []
    comp_window = resolve_comp_window(days_to_match)
    power_mult = (test_adjustments or {}).get("power_multiplier", 1.0)

    for family in slots:
        ex = select_or_continue(
            family=family,
            week=week,
            prev_slot_exercises=prev_slot_exercises,
            athlete_level=level,
            equipment_profile=equipment,
            recent_exercises=recent_exercises,
            injury_history=athlete.injury_history,
            technique_consistency=athlete.technique_consistency,
            days_to_match=days_to_match,
            athlete_profile=athlete,
            coach_prefs=coach_prefs,
            power_multiplier=power_mult,
            week_type=week_type,
        )
        if ex:
            prev_slot_exercises[family.value] = ex.id
        obj = ex.objective.value if ex else "STR"
        rest = OBJECTIVE_REST_MAP.get(obj)
        intensity = OBJECTIVE_INTENSITY_MAP.get(obj)
        block = SessionBlock(
            family=family,
            family_name=family.value,
            exercises=[ex] if ex else [],
            target_intensity=intensity,
            rest_period=rest,
        )
        if ex:
            presc = get_prescription(ex, level, blueprint_id, comp_window, week, week_type, athlete_profile=athlete)
            # Wave 14 — Coach preference: tempo & rest overrides
            if coach_prefs and coach_prefs.preferred_tempo:
                presc.loading_method = presc.loading_method  # ponytail: pass through, tempo encoded separately
            if coach_prefs and coach_prefs.preferred_rest_seconds:
                presc.rest_seconds = coach_prefs.preferred_rest_seconds
                block.rest_period = _rest_sec_to_str(presc.rest_seconds)
            # Wave 11a — Proportional compact: scale sets when time-constrained (slot-aware)
            if compact_factor < 1.0:
                family_factor = _slot_compact_factor(family, compact_factor)
                if family_factor < 1.0:
                    _compact_presc_sets(presc, family_factor)
            # Auto-correction: reduce sets when volume warning triggered
            if set_reduction and presc.sets:
                import re
                nums = re.findall(r'\d+', presc.sets)
                if nums:
                    reduced = [str(max(2, int(n) - set_reduction)) for n in nums]
                    presc.sets = reduced[0] if len(reduced) == 1 else '-'.join(reduced)
            block.prescription = presc
            block.rest_period = _rest_sec_to_str(presc.rest_seconds)
            technique = min(athlete.technique_consistency + 0.05 * week, 1.0)
            recent_exercises[ex.id] = {
                "last_used": f"week_{week}",
                "technique_score": technique,
            }
        blocks.append(block)

    # Wave 9: rebalance session — remove empty blocks and reorder
    blocks, rebalance_notes = rebalance_session_blocks(blocks, None)

    # Auto-correction: cap exercises per session when volume warning persists
    if cap_exercises and len(blocks) > cap_exercises:
        blocks = blocks[:cap_exercises]

    # Wave 15: test-driven sprint multiplier
    sprint_mult = (test_adjustments or {}).get("sprint_multiplier", 1.0)
    if sprint_mult != 1.0:
        session_pre = Session(blocks=blocks)
        session_pre = apply_sprint_multiplier(session_pre, sprint_mult)
        blocks = session_pre.blocks

    # Wave 15: test-driven conditioning adjustment
    cond_mult = (test_adjustments or {}).get("conditioning_multiplier", 1.0)
    _should_cond = should_add_conditioning_for_role(week, day, freq, conditioning_goal, role_profile)
    # In-season: remove conditioning within 48h of match
    if athlete.season_phase == SeasonPhase.IN_SEASON:
        if athlete.days_to_match is not None and athlete.days_to_match <= 2:
            _should_cond = False
    if cond_mult > 1.2 and not _should_cond:
        # Poor aerobic capacity: force conditioning into this session
        _should_cond = True
    elif cond_mult < 0.7 and _should_cond:
        # Excellent aerobic capacity: skip conditioning this session
        _should_cond = False

    if _should_cond:
        conditioning = progress_conditioning(
            week_type=week_type,
            prev_conditioning_id=prev_slot_exercises.get("_conditioning"),
            week=week,
            goal=conditioning_goal,
            athlete_level=level,
            environment=_sport_to_environment(athlete.sport),
            sport=athlete.sport,
            days_to_match=athlete.days_to_match,
            athlete_profile=athlete,
        )
        if conditioning:
            prev_slot_exercises["_conditioning"] = conditioning.id
    else:
        conditioning = None

    total_duration = sum(
        len(b.exercises) * 5 for b in blocks
    ) + (10 if conditioning else 0)

    cats = testing_categories if testing_categories else []
    return Session(
        blocks=blocks,
        conditioning=conditioning,
        total_duration_min=total_duration,
        week_type=week_type,
        testing_categories=cats,
        adjustment_note=adjustment_note,
    )


def _get_conditioning_mod(base_goal: str, modifier: Optional[str]) -> str:
    if modifier == "light":
        return "recovery"
    return base_goal


def _get_conditioning_goal(strength_goal: str) -> str:
    goal_map = {
        "general": "extensive_tempo",
        "strength": "aerobic_capacity",
        "hypertrophy": "aerobic_capacity",
        "power": "alactic_speed",
        "speed": "alactic_speed",
        "conditioning": "aerobic_power",
        "mass": "extensive_tempo",
        "fat_loss": "extensive_tempo",
        "return_to_sport": "recovery",
        "power_maintenance": "power_maintenance",
        "power_peak": "alactic_speed",
    }
    return goal_map.get(strength_goal, "aerobic_capacity")


def _should_add_conditioning(week: int, day: int, freq: int, goal: str) -> bool:
    if goal in ("conditioning", "return_to_sport"):
        return True
    return (week + day) % 2 == 0
