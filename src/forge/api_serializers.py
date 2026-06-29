"""FORGE API serializers — transforms domain objects into frontend-stable JSON payloads."""
from __future__ import annotations
from typing import Any, Optional
from datetime import datetime, timezone
from .models import (
    GeneratedProgram, Session, SessionBlock, Exercise,
    Prescription, ConditioningProtocol, WarmupProtocol,
    AthleteProfile, CoachPreferences, AthleteLevel, EquipmentProfile, SeasonPhase,
    FamilyCode, WeeklyProgressionPlan,
)
from .progression_engine import program_role_exposure_summary, plan_weeks, plan_testing, WEEK_INDEX_TO_TYPE
from .role_week_planning import get_role_week_profile, render_role_week_summary
from .data import BLUEPRINT_BY_ID


def _rest_sec_to_str(secs: int) -> str:
    if secs >= 120:
        return f"{secs // 60}:{secs % 60:02d} min"
    return f"{secs}s"


def _serialize_prescription(p: Optional[Prescription]) -> dict:
    if p is None:
        return {}
    return {
        "sets": p.sets,
        "reps": p.reps,
        "loading_method": p.loading_method,
        "intensity_note": p.intensity_note,
        "progression_method": p.progression_method,
        "rest_seconds": p.rest_seconds,
    }


def _serialize_progression_plan(plan: WeeklyProgressionPlan) -> dict:
    return {
        "volume_modifier": plan.volume_modifier,
        "intensity_modifier": plan.intensity_modifier,
        "density_modifier": plan.density_modifier,
        "complexity_level": plan.complexity_level,
        "velocity_emphasis": plan.velocity_emphasis,
        "eccentric_emphasis": plan.eccentric_emphasis,
    }


def _serialize_weekly_strategy(strategy: object) -> dict:
    result = {
        "week_number": strategy.week_number,
        "week_type": strategy.week_type,
        "primary_focus": strategy.primary_focus,
        "stress_level": strategy.stress_level,
        "volume_modifier": strategy.volume_modifier,
        "intensity_modifier": strategy.intensity_modifier,
        "exposure_budget": strategy.exposure_budget,
        "rationale": strategy.rationale,
    }
    if strategy.progression:
        result["progression"] = _serialize_progression_plan(strategy.progression)
    return result


def _serialize_session_intent(intent: Optional[object]) -> Optional[dict]:
    if not intent:
        return None
    return {
        "purpose": intent.purpose,
        "qualities": intent.qualities,
        "fatigue_cost": intent.fatigue_cost,
        "placement": intent.placement,
        "exposure_targets": intent.exposure_targets,
    }


def _serialize_exercise(ex: Exercise, block: SessionBlock) -> dict:
    p = block.prescription
    sets_reps = f"{p.sets} x {p.reps}" if p else "- x -"
    rest_str = _rest_sec_to_str(p.rest_seconds) if p else (block.rest_period or "60s")
    loading_method = p.loading_method if p else ""
    return {
        "id": ex.id,
        "name": ex.name,
        "family": block.family_name or ex.family.value,
        "sets_reps": sets_reps,
        "loading_method": loading_method,
        "rest": rest_str,
        "progression_note": p.progression_method if p and p.progression_method else None,
        "coach_note": None,
        "difficulty": ex.difficulty,
        "equipment": ex.equipment,
    }


def _serialize_warmup_to_section(warmup: Optional[WarmupProtocol]) -> Optional[dict]:
    if not warmup or not warmup.phases:
        return None
    exercises = []
    for phase in warmup.phases:
        for drill in phase.drills:
            exercises.append({
                "id": drill.id,
                "name": drill.name,
                "family": drill.phase,
                "sets_reps": f"{1} x {drill.duration_sec // 60}min" if drill.duration_sec >= 60 else f"{1} x {drill.duration_sec}s",
                "loading_method": "BW",
                "rest": "30s",
                "progression_note": drill.progression or None,
                "coach_note": drill.coaching_cue or None,
            })
    title = "Warmup"
    if warmup.phases:
        title = f"Warmup: {' + '.join(p.name for p in warmup.phases if p.drills)}"
    return {
        "title": title[:80],
        "exercises": exercises,
        "notes": None,
    }


def _serialize_conditioning_to_section(cond: Optional[ConditioningProtocol]) -> Optional[dict]:
    if not cond:
        return None
    return {
        "title": f"Conditioning: {cond.name}",
        "exercises": [{
            "id": cond.id,
            "name": cond.name,
            "family": "Conditioning",
            "sets_reps": cond.sets,
            "loading_method": cond.work_description,
            "rest": cond.rest,
            "progression_note": cond.progression or None,
            "coach_note": f"{cond.system} | {cond.duration} | fatigue: {cond.fatigue_score}",
        }],
        "notes": f"Total volume: {cond.total_volume} | {cond.objective}",
    }


def serialize_program(
    program: GeneratedProgram,
    request_payload: Optional[dict] = None,
) -> dict:
    """Serialize a GeneratedProgram into the frontend-stable API JSON shape."""
    now = datetime.now(timezone.utc).isoformat()
    ap = program.athlete_profile
    freq = program.frequency

    # Session-level warmup (derived from program warmup)
    warmup_section = _serialize_warmup_to_section(program.warmup)

    sessions_json: list[dict] = []
    for idx, session in enumerate(program.sessions):
        week_num = (idx // freq) + 1 if freq > 0 else 1
        session_num = (idx % freq) + 1 if freq > 0 else (idx + 1)

        # Serialize main work from session blocks
        main_exercises = []
        session_focus_parts = []
        for block in session.blocks:
            if not block.exercises:
                continue
            for ex in block.exercises:
                main_exercises.append(_serialize_exercise(ex, block))
            session_focus_parts.append(block.family_name or block.family.value)
        focus = ", ".join(session_focus_parts[:3]) if session_focus_parts else "General"

        cond_section = _serialize_conditioning_to_section(session.conditioning)

        session_json: dict[str, Any] = {
            "id": f"sess_{idx}",
            "name": f"Week {week_num} — Session {session_num}",
            "week_number": week_num,
            "session_number": session_num,
            "focus": focus,
            "warmup": warmup_section or {"title": "Warmup", "exercises": [], "notes": None},
            "main_work": {
                "title": "Main Work",
                "exercises": main_exercises,
                "notes": None,
            },
            "conditioning": cond_section or {"title": "Conditioning", "exercises": [], "notes": None},
            "session_notes": session.adjustment_note or None,
            "week_type": session.week_type,
            "testing_markers": list(session.testing_categories),
            "total_duration_min": session.total_duration_min,
            "load_capped": session.load_capped,
            "intent": _serialize_session_intent(session.intent),
            "structure_type": session.structure_type or None,
            "time_notes": session.time_notes or None,
        }
        sessions_json.append(session_json)

    # Build week-level exposure summaries
    weekly_strategies = getattr(program, "weekly_strategies", [])
    blueprint = BLUEPRINT_BY_ID.get(program.blueprint_id) if program.blueprint_id else None
    week_plan = plan_weeks(
        program.blueprint_id,
        AthleteLevel(program.level) if program.level else AthleteLevel.INTERMEDIATE,
        program.goal,
        ap.age if ap else 18,
        ap.days_to_match if ap else None,
    ) if program.duration else []
    test_plan = plan_testing(
        week_plan,
        program.blueprint_id,
        AthleteLevel(program.level) if program.level else AthleteLevel.INTERMEDIATE,
        program.goal,
        ap.age if ap else 18,
        ap.days_to_match if ap else None,
    ) if program.duration else {}

    weeks_json: list[dict] = []
    for w in range(1, program.duration + 1):
        wt = week_plan[w - 1] if w <= len(week_plan) else "accumulation"
        tests = test_plan.get(w, [])
        week_sessions = [s for s in sessions_json if s["week_number"] == w]

        ws = weekly_strategies[w - 1] if w - 1 < len(weekly_strategies) else None

        # Compute per-week exposure from actual exercise data
        start_idx = (w - 1) * freq
        end_idx = min(start_idx + freq, len(program.sessions))
        w_total = 0
        w_sprint = 0
        w_jump_land = 0
        w_rot = 0
        w_hinge = 0
        w_squat = 0
        for s in program.sessions[start_idx:end_idx]:
            for b in s.blocks:
                for ex in b.exercises:
                    if not ex:
                        continue
                    w_total += 1
                    if ex.family == FamilyCode.SPRINT:
                        w_sprint += 1
                    if ex.family in (FamilyCode.LANDING, FamilyCode.PLYO):
                        w_jump_land += 1
                    if ex.family == FamilyCode.ROT or ex.rotational:
                        w_rot += 1
                    if ex.family in (FamilyCode.DLHD, FamilyCode.SLHD):
                        w_hinge += 1
                    if ex.family in (FamilyCode.DLKD, FamilyCode.SLKD):
                        w_squat += 1

        def _pct(count: int) -> float:
            return round(count / w_total * 100, 1) if w_total else 0.0

        def _label(count: int) -> str:
            pct = _pct(count)
            if pct >= 30:
                return "High"
            if pct >= 15:
                return "Moderate"
            if count > 0:
                return "Low"
            return "None"

        week_entry: dict[str, Any] = {
            "week_number": w,
            "label": f"Week {w}",
            "exposure_summary": {
                "sprint_exposure": f"{_label(w_sprint)} ({w_sprint} ex, {_pct(w_sprint)}%)",
                "jump_landing_exposure": f"{_label(w_jump_land)} ({w_jump_land} ex, {_pct(w_jump_land)}%)",
                "deceleration_exposure": f"{_label(w_rot)} ({w_rot} ex, {_pct(w_rot)}%)",
                "eccentric_stress": f"{_label(w_hinge)} ({w_hinge} ex, {_pct(w_hinge)}%)",
                "conditioning_density": f"{_label(w_squat)} ({w_squat} ex, {_pct(w_squat)}%)",
                "week_type": wt,
                "testing_markers": tests,
                "adjustment_notes": [],
            },
            "sessions": week_sessions,
        }
        if ws:
            week_entry["strategy"] = _serialize_weekly_strategy(ws)
        weeks_json.append(week_entry)

    # Build validation notes from credibility
    from .validator import verify_credibility, calculate_credibility_score
    validation_json: list[dict] = []
    if program.sessions:
        check = verify_credibility(program.sessions[0], ap)
        score = calculate_credibility_score(check)
        if score < 0.7:
            validation_json.append({"type": "warning", "message": f"Session credibility: {score:.1f}/1.0"})
        if program.credibility_score < 0.7:
            validation_json.append({"type": "warning", "message": f"Program credibility: {program.credibility_score:.1f}/1.0"})
        for key, passed in check.items():
            if not passed:
                validation_json.append({"type": "info", "message": f"Check {key.replace('_', ' ')}: needs attention"})

    # Rationale lines — describe what the engine decided
    rationale: list[str] = []
    rationale.append(f"Blueprint: {program.blueprint_name} (ID: {program.blueprint_id})")
    rationale.append(f"Goal: {program.goal} | Level: {program.level}")
    if ap and ap.position_role:
        role_profile = get_role_week_profile(ap.sport, ap.position_role)
        if role_profile:
            rationale.append(f"Role-aware planning applied: {ap.position_role}")
    if program.duration:
        rationale.append(f"Block: {program.duration} weeks, {freq}x/week — {len(program.sessions)} total sessions")
    if ap and ap.days_to_match is not None:
        rationale.append(f"Competition proximity: {ap.days_to_match} days out — {'taper applied' if ap.days_to_match <= 4 else 'normal loading'}")

    # Season phase mapping
    season_label = ""
    if ap:
        try:
            season_label = ap.season_phase.value.replace("_", " ").title()
        except Exception:
            season_label = ""
    if season_label:
        summary_conditioning = f"{season_label} — {program.goal.replace('_', ' ').title()}"
    else:
        summary_conditioning = program.goal.replace("_", " ").title()

    comp_window_str = "Unknown"
    if ap and ap.days_to_match is not None:
        from .conditioning_engine import _resolve_comp_window as resolve_cw
        cw = resolve_cw(ap.days_to_match)
        comp_window_str = f"{ap.days_to_match} days out" if cw >= 6 else f"{ap.days_to_match}d out (taper)"
    else:
        comp_window_str = "Off-season"

    role_emphasis = "General"
    if ap and ap.position_role:
        role_emphasis = f"{ap.position_role} — {ap.sport}"

    response: dict[str, Any] = {
        "metadata": {
            "generated_at": now,
            "request_id": f"req_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}_{id(program)}",
            "api_version": "1.0.0",
        },
        "summary": {
            "blueprint_selected": program.blueprint_name,
            "blueprint_id": program.blueprint_id,
            "total_weeks": program.duration,
            "weekly_frequency": freq,
            "conditioning_emphasis": summary_conditioning,
            "competition_window": comp_window_str,
            "role_emphasis": role_emphasis,
            "level": program.level,
            "goal": program.goal,
            "equipment_profile": program.equipment_profile,
            "credibility_score": program.credibility_score,
        },
        "weeks": weeks_json,
        "sessions": sessions_json,
        "rationale": rationale,
        "personalization_notes": list(program.personalization_notes),
        "validation": validation_json,
        "dropped_constraints": [],
        "test_adjustments": getattr(program.athlete_profile, "test_adjustments", None) or {"has_data": False},
    }

    return response


def athlete_profile_from_request(payload: dict) -> AthleteProfile:
    """Build AthleteProfile from a frontend ProgramRequest payload."""
    basics = payload.get("basics", {})
    context = payload.get("context", {})
    advanced = payload.get("advanced", {})

    # Determine equipment profile
    equip_map = {
        "pro facility": EquipmentProfile.ELITE_FACILITY,
        "commercial gym": EquipmentProfile.COMMERCIAL_GYM,
        "home gym": EquipmentProfile.BASIC_GYM,
        "field/track": EquipmentProfile.FIELD_ONLY,
    }
    env_str = (basics.get("environment") or "commercial gym").lower()
    equipment = equip_map.get(env_str, EquipmentProfile.COMMERCIAL_GYM)

    # Determine athlete level
    level_str = basics.get("level", "Intermediate")
    level_map = {
        "beginner": AthleteLevel.BEGINNER,
        "intermediate": AthleteLevel.INTERMEDIATE,
        "advanced": AthleteLevel.ADVANCED,
    }
    athlete_level = level_map.get(level_str.lower(), AthleteLevel.INTERMEDIATE)
    if athlete_level == AthleteLevel.BEGINNER:
        athlete_level = AthleteLevel.INTERMEDIATE

    # Determine season phase
    phase_str = context.get("current_phase", "")
    phase_map = {
        "off": SeasonPhase.OFF_SEASON,
        "pre": SeasonPhase.PRE_SEASON,
        "in": SeasonPhase.IN_SEASON,
        "transition": SeasonPhase.TRANSITION,
    }
    season_phase = SeasonPhase.OFF_SEASON
    for key, val in phase_map.items():
        if key in phase_str.lower():
            season_phase = val
            break

    goal = context.get("primary_goal", "strength") or "strength"
    training_age = basics.get("training_age_years")
    if isinstance(training_age, str) and training_age.strip() == "":
        training_age = 0
    elif training_age is None:
        training_age = 0

    age = basics.get("age")
    if isinstance(age, str) and age.strip() == "":
        age = 18
    elif age is None or age == "":
        age = 18

    days_to_match = basics.get("days_to_match")
    if isinstance(days_to_match, str) and days_to_match.strip() == "":
        days_to_match = None

    # Technique consistency
    tc_str = advanced.get("technique_consistency", "").lower()
    tc_map = {"low": 0.7, "medium": 0.85, "high": 0.95}
    technique_consistency = tc_map.get(tc_str, 0.85)

    # Injury risk flags
    injury_risk_flags = advanced.get("injury_risk_flags", [])
    if isinstance(injury_risk_flags, str):
        injury_risk_flags = [s.strip() for s in injury_risk_flags.split(",") if s.strip()]
    injury_history = [s.lower() for s in injury_risk_flags if s]

    # Parse raw test scores (strings from form -> float)
    def _to_float(v):
        if v is None or v == "" or v == "": return None
        try: return float(v)
        except: return None

    yoyo_ir1 = _to_float(advanced.get("yoyo_ir1"))
    yoyo_ir2 = _to_float(advanced.get("yoyo_ir2"))
    bronco = _to_float(advanced.get("bronco"))
    cmj_raw = _to_float(advanced.get("cmj"))

    # Parse coach preferences
    cp_raw = payload.get("coach_preferences") or {}
    coach_prefs = CoachPreferences(
        preferred_deadlift=cp_raw.get("preferred_deadlift"),
        preferred_squat=cp_raw.get("preferred_squat"),
        preferred_press=cp_raw.get("preferred_press"),
        avoid_olympic_lifts=cp_raw.get("avoid_olympic_lifts", False),
        avoid_high_soreness_near_match=cp_raw.get("avoid_high_soreness_near_match", False),
        min_sprint_exposures_per_week=cp_raw.get("min_sprint_exposures_per_week", 1),
        preferred_conditioning_style=cp_raw.get("preferred_conditioning_style", "mixed"),
        bias_unilateral_work=cp_raw.get("bias_unilateral_work", False),
        prefer_velocity_based_loading=cp_raw.get("prefer_velocity_based_loading", False),
        preferred_tempo=cp_raw.get("preferred_tempo", "20X0"),
        preferred_rest_seconds=cp_raw.get("preferred_rest_seconds", 90),
    ) if any(v is not None for v in [
        cp_raw.get("preferred_deadlift"), cp_raw.get("preferred_squat"),
        cp_raw.get("preferred_press"), cp_raw.get("avoid_olympic_lifts"),
        cp_raw.get("avoid_high_soreness_near_match"),
        cp_raw.get("min_sprint_exposures_per_week") and cp_raw.get("min_sprint_exposures_per_week") != 1,
        cp_raw.get("preferred_conditioning_style") and cp_raw.get("preferred_conditioning_style") != "mixed",
        cp_raw.get("bias_unilateral_work"), cp_raw.get("prefer_velocity_based_loading"),
        cp_raw.get("preferred_tempo") and cp_raw.get("preferred_tempo") != "20X0",
        cp_raw.get("preferred_rest_seconds") and cp_raw.get("preferred_rest_seconds") != 90,
    ]) else None

    profile = AthleteProfile(
        sport=basics.get("sport", "athlete"),
        training_age_years=float(training_age),
        season_phase=season_phase,
        goal=goal,
        equipment_profile=equipment,
        athlete_level=athlete_level,
        technique_consistency=technique_consistency,
        injury_status="none",
        injury_history=injury_history,
        fatigue_level="normal",
        weeks_since_break=0,
        available_minutes=basics.get("available_minutes", 60),
        days_to_match=days_to_match,
        age=int(age),
        preferred_families=6,
        strength_base_met=True,
        bodyweight_kg=None,
        position_role=basics.get("role", ""),
        role=basics.get("role", ""),
        program_length_weeks=int(context.get("program_length_weeks", 8)),
        frequency_per_week=int(basics.get("frequency_per_week", 3)),
        coach_intent=context.get("coach_intent", advanced.get("coach_intent", "")),
        force_profile=_map_fv_profile(advanced.get("force_velocity_profile", "")),
        elastic_profile=None,
        conditioning_profile=None,
        landing_competency=None,
        sprint_mechanics_competency=None,
        lumbar_risk="lumbar" in str(injury_history).lower() or "lower back" in str(injury_history).lower() or "back" in str(injury_history).lower(),
        patellar_tendon_risk="patellar" in str(injury_history).lower() or "knee" in str(injury_history).lower(),
        hamstring_risk="hamstring" in str(injury_history).lower(),
        shoulder_overhead_risk="shoulder" in str(injury_history).lower(),
        groin_adductor_risk="groin" in str(injury_history).lower() or "adductor" in str(injury_history).lower(),
        ankle_foot_risk="ankle" in str(injury_history).lower() or "foot" in str(injury_history).lower(),
        cmj_band=_map_band(advanced.get("cmj_band", "")),
        sprint_10m_band=_map_band(advanced.get("sprint_10m_band", "")),
        squat_strength_band=_map_band(advanced.get("squat_strength_band", "")),
        aerobic_band=_map_band(advanced.get("aerobic_band", "")),
        coach_preferences=coach_prefs,
        yoyo_ir1=yoyo_ir1,
        yoyo_ir2=yoyo_ir2,
        bronco=bronco,
        cmj=cmj_raw,
        testing_date=advanced.get("testing_date") or advanced.get("testing_date", None),
        match_day=int(context.get("match_day")) if context.get("match_day") is not None else 5,
        team_training_days=context.get("team_training_days") or [0, 2, 4],
        heavy_field_days=context.get("heavy_field_days") or [1, 3],
        travel_days=context.get("travel_days") or [],
    )

    return profile


def _map_fv_profile(val: str) -> Optional[str]:
    if not val:
        return None
    val_lower = val.lower()
    if "force" in val_lower and "deficit" in val_lower:
        return "force_deficient"
    if "velocity" in val_lower and "deficit" in val_lower:
        return "velocity_deficient"
    if "balanced" in val_lower:
        return "balanced"
    return None


def _map_band(val: str) -> Optional[str]:
    if not val:
        return None
    val_lower = val.lower()
    if "elite" in val_lower or ">2" in val_lower:
        return "high"
    if "high" in val_lower or "strong" in val_lower:
        return "high"
    if "average" in val_lower or "moderate" in val_lower or "solid" in val_lower:
        return "avg"
    if "low" in val_lower or "poor" in val_lower or "<" in val_lower:
        return "low"
    return "avg"
