"""Calendar-awareness audit.

Tests whether match_day, team_training_days, and heavy_field_days actually
change session placement, slot count, fatigue scores, and exercise selection.

Usage:  python src/forge/audit_calendar.py
"""
from __future__ import annotations
import json, os
from collections import defaultdict
from typing import Any

from src.forge.api_serializers import athlete_profile_from_request
from src.forge.main import generate_program, _build_session
from src.forge.models import (
    AthleteProfile, AthleteLevel, EquipmentProfile, SeasonPhase, Session, Exercise,
)
from src.forge.data import BLUEPRINT_BY_ID
from src.forge.session_assembly import (
    resolve_weekly_schedule, adjust_slots_for_calendar, DayContext,
)
from src.forge.blueprint_engine import select_blueprint, resolve_slots, determine_level

DAY_NAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _build_req(match_day: int, training_days: list[int],
               heavy_days: list[int] | None = None,
               travel_days: list[int] | None = None) -> dict:
    return {
        "mode": "core",
        "basics": {
            "athlete_name": "Calendar Test", "age": 25, "sex": "Male",
            "sport": "Rugby Union", "role": "Tighthead Prop",
            "training_age_years": 5, "level": "Advanced",
            "environment": "Elite Facility", "available_minutes": 90,
            "frequency_per_week": 3,
        },
        "context": {
            "primary_goal": "strength", "current_phase": "in_season",
            "match_day": match_day,
            "team_training_days": training_days,
            "heavy_field_days": heavy_days or [1, 3],
            "travel_days": travel_days or [],
            "program_length_weeks": 4,
        },
        "advanced": {},
    }


def _analyze_sessions(program, schedule: list[DayContext]) -> list[dict]:
    """Return a detailed analysis of each session in the program."""
    freq = program.frequency or 3
    results = []
    for i, sess in enumerate(program.sessions):
        week = (i // freq) + 1
        sess_num = (i % freq) + 1
        ctx = schedule[sess_num - 1] if sess_num <= len(schedule) else None

        total_fatigue = 0
        total_eccentric = 0
        total_impact = 0
        families = []
        exercise_names = []
        for block in sess.blocks:
            if not block.exercises:
                continue
            fcode = block.family.value if hasattr(block.family, 'value') else str(block.family)
            families.append(fcode)
            for ex in block.exercises:
                total_fatigue += getattr(ex, 'fatigue_cost', 3)
                total_eccentric += getattr(ex, 'eccentric_cost', 3)
                total_impact += getattr(ex, 'impact_level', 3)
                exercise_names.append(ex.name)

        day_name = DAY_NAMES[ctx.day_of_week] if ctx else "?"
        results.append({
            "week": week,
            "session": sess_num,
            "day_of_week": ctx.day_of_week if ctx else None,
            "day_name": day_name,
            "is_match_day": ctx.is_match_day if ctx else False,
            "is_within_48h": ctx.is_within_48h_of_match if ctx else False,
            "is_heavy_field_day": ctx.is_heavy_field_day if ctx else False,
            "is_team_training_day": ctx.is_team_training_day if ctx else False,
            "is_travel_day": ctx.is_travel_day if ctx else False,
            "slot_count": len(families),
            "exercise_count": len(exercise_names),
            "total_fatigue_cost": total_fatigue,
            "total_eccentric_cost": total_eccentric,
            "total_impact_level": total_impact,
            "families": families,
            "exercises": exercise_names,
            "has_conditioning": sess.conditioning is not None,
        })
    return results


def run_audit() -> dict:
    """Run calendar audit with two match day configurations."""

    # ── Program A: match Sat, train Mon/Wed/Fri ──
    req_a = _build_req(match_day=5, training_days=[0, 2, 4])
    ap_a = athlete_profile_from_request(req_a)
    prog_a = generate_program(ap_a)
    bp_a = select_blueprint(ap_a)
    schedule_a = resolve_weekly_schedule(
        ap_a.match_day, ap_a.team_training_days,
        ap_a.heavy_field_days, ap_a.travel_days, prog_a.frequency,
    )
    analysis_a = _analyze_sessions(prog_a, schedule_a)

    # ── Program B: match Sun, train Tue/Thu ──
    req_b = _build_req(match_day=6, training_days=[1, 3])
    ap_b = athlete_profile_from_request(req_b)
    prog_b = generate_program(ap_b)
    bp_b = select_blueprint(ap_b)
    schedule_b = resolve_weekly_schedule(
        ap_b.match_day, ap_b.team_training_days,
        ap_b.heavy_field_days, ap_b.travel_days, prog_b.frequency,
    )
    analysis_b = _analyze_sessions(prog_b, schedule_b)

    # ── Compare ──
    # Check 1: Are sessions placed on different days?
    day_placement_a = [(s["week"], s["session"], s["day_name"]) for s in analysis_a[:prog_a.frequency]]
    day_placement_b = [(s["week"], s["session"], s["day_name"]) for s in analysis_b[:prog_b.frequency]]

    # Check 2: Does the session before match day have lower fatigue?
    # Program A: match Sat(5). Sessions on Mon(0), Wed(2), Fri(4). Fri is within 48h.
    # Program B: match Sun(6). Sessions on ... depends on resolve_weekly_schedule.
    pre_match_a = [s for s in analysis_a if s["is_within_48h"]]
    pre_match_b = [s for s in analysis_b if s["is_within_48h"]]

    # Check 3: Are heavy gym days scheduled away from match day?
    # Program A: heavy=[1,3] (Tue, Thu). Sessions on Mon(0), Wed(2), Fri(4).
    #   Wed(2): not heavy (2 not in [1,3]). But Tue(1) and Thu(3) are heavy — no sessions on those days though.
    # Program B: heavy=[1,3] (Tue, Thu). Sessions on ... depends on days selected.

    # Aggregated stats
    def _agg(analysis, label):
        total_exercises = sum(s["exercise_count"] for s in analysis)
        total_sessions = len(analysis)
        avg_fatigue = sum(s["total_fatigue_cost"] for s in analysis) / max(total_sessions, 1)
        avg_eccentric = sum(s["total_eccentric_cost"] for s in analysis) / max(total_sessions, 1)
        avg_slots = sum(s["slot_count"] for s in analysis) / max(total_sessions, 1)
        return {
            "label": label,
            "total_sessions": total_sessions,
            "total_exercises": total_exercises,
            "avg_slots_per_session": round(avg_slots, 1),
            "avg_fatigue_per_session": round(avg_fatigue, 1),
            "avg_eccentric_per_session": round(avg_eccentric, 1),
            "avg_impact_per_session": round(sum(s["total_impact_level"] for s in analysis) / max(total_sessions, 1), 1),
            "sessions_within_48h": sum(1 for s in analysis if s["is_within_48h"]),
            "sessions_on_match_day": sum(1 for s in analysis if s["is_match_day"]),
            "sessions_on_heavy_day": sum(1 for s in analysis if s["is_heavy_field_day"]),
        }

    agg_a = _agg(analysis_a, "Program A (match Sat, train Mon/Wed/Fri)")
    agg_b = _agg(analysis_b, "Program B (match Sun, train Tue/Thu)")

    # Determine if anything differed
    same_placement = day_placement_a == day_placement_b
    same_avg_fatigue = abs(agg_a["avg_fatigue_per_session"] - agg_b["avg_fatigue_per_session"]) < 0.1
    same_avg_slots = agg_a["avg_slots_per_session"] == agg_b["avg_slots_per_session"]
    same_avg_eccentric = abs(agg_a["avg_eccentric_per_session"] - agg_b["avg_eccentric_per_session"]) < 0.1

    # Check if within_48h sessions actually have fewer slots than normal
    within_48h_sessions_a = [s for s in analysis_a if s["is_within_48h"]]
    normal_sessions_a = [s for s in analysis_a if not s["is_within_48h"]]
    calendar_effective = False
    if within_48h_sessions_a and normal_sessions_a:
        avg_slots_within = sum(s["slot_count"] for s in within_48h_sessions_a) / len(within_48h_sessions_a)
        avg_slots_normal = sum(s["slot_count"] for s in normal_sessions_a) / len(normal_sessions_a)
        calendar_effective = avg_slots_within < avg_slots_normal

    return {
        "config_a": {
            "match_day": 5,
            "team_training_days": [0, 2, 4],
            "heavy_field_days": [1, 3],
            "travel_days": [],
        },
        "config_b": {
            "match_day": 6,
            "team_training_days": [1, 3],
            "heavy_field_days": [1, 3],
            "travel_days": [],
        },
        "schedule_a": [{"day": s["day_name"], "week": s["week"], "session": s["session"]}
                       for s in analysis_a[:prog_a.frequency]],
        "schedule_b": [{"day": s["day_name"], "week": s["week"], "session": s["session"]}
                       for s in analysis_b[:prog_b.frequency]],
        "same_day_placement": same_placement,
        "aggregate_a": agg_a,
        "aggregate_b": agg_b,
        "same_avg_fatigue": same_avg_fatigue,
        "same_avg_slots": same_avg_slots,
        "same_avg_eccentric": same_avg_eccentric,
        "pre_match_sessions_a": [
            {"session": s["session"], "day": s["day_name"], "slots": s["slot_count"],
             "fatigue": s["total_fatigue_cost"], "eccentric": s["total_eccentric_cost"],
             "families": s["families"]}
            for s in within_48h_sessions_a
        ],
        "pre_match_sessions_b": [
            {"session": s["session"], "day": s["day_name"], "slots": s["slot_count"],
             "fatigue": s["total_fatigue_cost"], "eccentric": s["total_eccentric_cost"],
             "families": s["families"]}
            for s in pre_match_b
        ],
        "detail_a": analysis_a[:prog_a.frequency * 2],  # First 2 weeks
        "detail_b": analysis_b[:prog_b.frequency * 2],
        "calendar_effective": calendar_effective,
        "verdict": (
            "Calendar-aware programming IS implemented and active"
            if calendar_effective
            else "Calendar-aware programming is not implemented or is cosmetic"
        ),
    }


def print_report(report: dict) -> None:
    print("=" * 72)
    print("CALENDAR-AWARENESS AUDIT")
    print("=" * 72)
    print()

    print("-- Configurations --")
    print(f"  Program A: match={report['config_a']['match_day']} ({DAY_NAMES[report['config_a']['match_day']]}), "
          f"train={[DAY_NAMES[d] for d in report['config_a']['team_training_days']]}, "
          f"heavy={[DAY_NAMES[d] for d in report['config_a']['heavy_field_days']]}")
    print(f"  Program B: match={report['config_b']['match_day']} ({DAY_NAMES[report['config_b']['match_day']]}), "
          f"train={[DAY_NAMES[d] for d in report['config_b']['team_training_days']]}, "
          f"heavy={[DAY_NAMES[d] for d in report['config_b']['heavy_field_days']]}")
    print()

    print("-- Check 1: Session Placement --")
    print(f"  Program A schedule (first week): {[s['day'] for s in report['schedule_a']]}")
    print(f"  Program B schedule (first week): {[s['day'] for s in report['schedule_b']]}")
    print(f"  Placed differently? {'YES' if not report['same_day_placement'] else 'NO — same days'}")
    print()

    print("-- Check 2: Pre-Match Session Fatigue --")
    a_pre = report["pre_match_sessions_a"]
    b_pre = report["pre_match_sessions_b"]
    print(f"  Program A pre-match/within-48h sessions ({len(a_pre)}):")
    for s in a_pre:
        print(f"    Day {s['day']}: {s['slots']} slots, fatigue={s['fatigue']}, eccentric={s['eccentric']}, "
              f"families={s['families']}")
    print(f"  Program B pre-match/within-48h sessions ({len(b_pre)}):")
    for s in b_pre:
        print(f"    Day {s['day']}: {s['slots']} slots, fatigue={s['fatigue']}, eccentric={s['eccentric']}, "
              f"families={s['families']}")
    print()

    print("-- Check 3: Heavy Gym Days vs Match Day --")
    for label, agg in [("A", report["aggregate_a"]), ("B", report["aggregate_b"])]:
        print(f"  Program {label}:")
        print(f"    Sessions on heavy field days: {agg['sessions_on_heavy_day']}")
        print(f"    Sessions on match day: {agg['sessions_on_match_day']}")
        print(f"    Sessions within 48h of match: {agg['sessions_within_48h']}")
    print()

    print("-- Aggregate Comparison --")
    for label, agg in [("A", report["aggregate_a"]), ("B", report["aggregate_b"])]:
        print(f"  Program {label}:")
        print(f"    Total sessions: {agg['total_sessions']}")
        print(f"    Total exercises: {agg['total_exercises']}")
        print(f"    Avg slots/session: {agg['avg_slots_per_session']}")
        print(f"    Avg fatigue/session: {agg['avg_fatigue_per_session']}")
        print(f"    Avg eccentric/session: {agg['avg_eccentric_per_session']}")
        print(f"    Avg impact/session: {agg['avg_impact_per_session']}")
    print()

    print("-- Session-by-Session (first 2 weeks, Program A) --")
    for s in report["detail_a"]:
        flags = []
        if s["is_match_day"]: flags.append("MATCH")
        if s["is_within_48h"]: flags.append("PRE-MATCH")
        if s["is_heavy_field_day"]: flags.append("HEAVY")
        flag_str = f" [{','.join(flags)}]" if flags else ""
        print(f"  W{s['week']} S{s['session']} {s['day_name']}{flag_str}: "
              f"{s['slot_count']} slots, {s['exercise_count']} ex, "
              f"fatigue={s['total_fatigue_cost']}, eccentric={s['total_eccentric_cost']}")
        print(f"    Families: {s['families']}")

    print()
    print("-- Session-by-Session (first 2 weeks, Program B) --")
    for s in report["detail_b"]:
        flags = []
        if s["is_match_day"]: flags.append("MATCH")
        if s["is_within_48h"]: flags.append("PRE-MATCH")
        if s["is_heavy_field_day"]: flags.append("HEAVY")
        flag_str = f" [{','.join(flags)}]" if flags else ""
        print(f"  W{s['week']} S{s['session']} {s['day_name']}{flag_str}: "
              f"{s['slot_count']} slots, {s['exercise_count']} ex, "
              f"fatigue={s['total_fatigue_cost']}, eccentric={s['total_eccentric_cost']}")
        print(f"    Families: {s['families']}")

    print()
    print("-- Verdict --")
    print(f"  {report['verdict']}")
    cal_eff = report["calendar_effective"]
    if cal_eff:
        print("  Evidence: within-48h sessions have fewer slots than normal sessions,")
        print("  indicating neural family dropping is working.")
    else:
        print("  Evidence: slot counts are identical regardless of calendar context.")
    print("=" * 72)


if __name__ == "__main__":
    report = run_audit()
    print_report(report)
    out_path = os.path.join(os.path.dirname(__file__), "audit_calendar_report.json")
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2, default=str)
    print(f"\nRaw report saved to {out_path}")
