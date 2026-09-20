"""FORGE Engine Intelligence Audit.

Runs the generation engine across multiple controlled inputs and
measures what actually changes. Answers 7 questions about the engine's
behavior, exercise variety, progression logic, and input sensitivity.

Usage:  python -m src.forge.audit_engine_intelligence
        python src/forge/audit_engine_intelligence.py

No generation logic is modified — this script only observes.
"""
from __future__ import annotations
import json, math, itertools, re
from collections import Counter, defaultdict
from typing import Any

from src.forge.models import (
    GeneratedProgram, Session, AthleteProfile, AthleteLevel,
    EquipmentProfile, SeasonPhase,
)
from src.forge.api_serializers import athlete_profile_from_request, serialize_program
from src.forge.main import generate_program
from src.forge.data import EXERCISE_BY_ID


# ── Helpers ──────────────────────────────────────────────────────────

ExerciseFingerprint = tuple[int, int, str, str, str, float]
""" (week, session_within_week, exercise_id, sets, reps, load_factor) """


def _fingerprint(program: GeneratedProgram) -> list[ExerciseFingerprint]:
    """Return a flat list of (week, sess_idx, ex_id, sets, reps, load) per exercise."""
    out: list[ExerciseFingerprint] = []
    freq = program.frequency or 3
    for i, sess in enumerate(program.sessions):
        week = (i // freq) + 1
        sess_idx = (i % freq) + 1
        for block in sess.blocks:
            if not block.exercises:
                continue
            for ex in block.exercises:
                p = block.prescription
                sets_str = p.sets if p else "-"
                reps_str = p.reps if p else "-"
                # Rough load proxy: sets * reps * intensity_factor
                load = _parse_sets(sets_str) * _parse_reps(reps_str) * _intensity_factor(p)
                out.append((week, sess_idx, ex.id, sets_str, reps_str, load))
    return out


def _parse_sets(s: str) -> int:
    nums = re.findall(r"\d+", s)
    if not nums:
        return 1
    # If range like "3-4", take the upper end
    return max(int(n) for n in nums)


def _parse_reps(s: str) -> int:
    nums = re.findall(r"\d+", s)
    if not nums:
        return 1
    return max(int(n) for n in nums)


def _intensity_factor(p) -> float:
    if not p or not p.loading_method:
        return 1.0
    lm = p.loading_method.lower()
    if "heavy" in lm or "max" in lm or "85" in lm or "90" in lm:
        return 1.0
    if "moderate" in lm or "75" in lm or "80" in lm:
        return 0.8
    if "light" in lm or "60" in lm or "50" in lm:
        return 0.6
    if "explosive" in lm:
        return 0.7
    return 0.8


def _build_request(**overrides: Any) -> dict:
    """Return a standard ProgramRequest dict, overridden by kwargs."""
    base = {
        "mode": "core",
        "basics": {
            "athlete_name": "Audit Athlete", "age": 25, "sex": "Male",
            "sport": "Cricket", "role": "Pace Bowler",
            "training_age_years": 5, "level": "Advanced",
            "environment": "Elite Facility", "available_minutes": 90,
            "frequency_per_week": 3,
        },
        "context": {
            "primary_goal": "strength", "current_phase": "pre_season",
            "match_day": 6, "team_training_days": [0, 2, 4],
            "heavy_field_days": [1, 3], "program_length_weeks": 4,
        },
        "advanced": {},
    }
    def _deep_merge(d: dict, u: dict) -> dict:
        for k, v in u.items():
            if isinstance(v, dict) and k in d:
                d[k] = _deep_merge(d[k], v)
            else:
                d[k] = v
        return d
    return _deep_merge(base, overrides)


def _generate(req: dict) -> GeneratedProgram:
    ap = athlete_profile_from_request(req)
    return generate_program(ap)


def _summarize(program: GeneratedProgram, label: str = "") -> dict:
    """Return a program summary dict for analysis."""
    fp = _fingerprint(program)
    freq = program.frequency or 3
    weeks = program.duration or 0
    ex_ids = [e[2] for e in fp]
    unique_ex = len(set(ex_ids))
    total_slots = len(fp)
    per_week: dict[int, list] = defaultdict(list)
    for w, si, eid, sets, reps, load in fp:
        per_week[w].append(load)
    week_loads = {w: sum(loads) for w, loads in per_week.items()}

    return {
        "label": label,
        "weeks": weeks,
        "freq": freq,
        "total_sessions": len(program.sessions),
        "total_exercise_slots": total_slots,
        "unique_exercises": unique_ex,
        "uniqueness_ratio": round(unique_ex / max(total_slots, 1), 4),
        "db_exercise_count": len(EXERCISE_BY_ID),
        "variety_score": round(unique_ex / max(len(EXERCISE_BY_ID), 1), 4),
        "week_loads": dict(sorted(week_loads.items())),
        "exercise_ids": sorted(ex_ids),
        "exercise_names": sorted(set(
            EXERCISE_BY_ID.get(eid, ExerciseDummy(eid)).name
            for eid in ex_ids
        )),
    }


class ExerciseDummy:
    def __init__(self, eid): self.id = eid; self.name = eid


def _ex_name(eid: str) -> str:
    ex = EXERCISE_BY_ID.get(eid)
    return ex.name if ex else eid


# ══════════════════════════════════════════════════════════════════════
# QUESTION 1: Does every week meaningfully differ?
# ══════════════════════════════════════════════════════════════════════

def audit_week_differentiation(program: GeneratedProgram) -> dict:
    """Compare exercise lists across weeks. Report same/different/rotated."""
    fp = _fingerprint(program)
    freq = program.frequency or 3
    weeks = program.duration or 0
    week_exercises: dict[int, list[str]] = defaultdict(list)
    for w, si, eid, sets, reps, load in fp:
        week_exercises[w].append(eid)

    if len(week_exercises) < 2:
        return {"classification": "Single week", "detail": "Only one week generated"}

    sorted_weeks = sorted(week_exercises.keys())
    first = set(week_exercises[sorted_weeks[0]])
    last = set(week_exercises[sorted_weeks[-1]])
    mid_idx = len(sorted_weeks) // 2
    mid = set(week_exercises[sorted_weeks[mid_idx]])

    identical_all = all(
        set(week_exercises[w]) == first for w in sorted_weeks[1:]
    )
    identical_endpoints = (first == last)
    rotation_count = sum(1 for w in sorted_weeks if set(week_exercises[w]) != first)

    if identical_all:
        classification = "Static"
    elif not identical_endpoints and rotation_count >= weeks // 2:
        # Also check if only sets/reps changed — look at unique exercises
        # If the set of unique exercises changes, it's dynamic
        if first != mid:
            classification = "Dynamic periodization"
        else:
            classification = "Linear periodization"
    elif rotation_count > 0:
        classification = "Dynamic periodization"
    else:
        classification = "Linear periodization"

    detail = {}
    for w in sorted_weeks:
        detail[f"Week {w}"] = sorted(week_exercises[w])
    return {
        "classification": classification,
        "weeks_compared": sorted_weeks,
        "week_detail": {k: [_ex_name(e) for e in v] for k, v in detail.items()},
        "week_exercise_ids": {k: sorted(v) for k, v in week_exercises.items()},
        "first_vs_last_same": identical_endpoints,
        "weeks_with_unique_exercises": rotation_count,
    }


# ══════════════════════════════════════════════════════════════════════
# QUESTION 2: Is progression real or just copied?
# ══════════════════════════════════════════════════════════════════════

def audit_progression(program: GeneratedProgram) -> dict:
    """Track volume load proxy across weeks. Report trend."""
    fp = _fingerprint(program)
    freq = program.frequency or 3
    week_loads: dict[int, float] = defaultdict(float)
    for w, si, eid, sets, reps, load in fp:
        week_loads[w] += load

    sorted_weeks = sorted(week_loads.keys())
    loads = [week_loads[w] for w in sorted_weeks]

    if len(loads) < 3:
        trend = "Flat (too few weeks)"
    else:
        deltas = [loads[i] - loads[i - 1] for i in range(1, len(loads))]
        avg_delta = sum(deltas) / len(deltas)
        positive_count = sum(1 for d in deltas if d > 0)
        if positive_count >= len(deltas) * 0.6 and avg_delta > 0:
            trend = "Progressive"
        elif positive_count <= len(deltas) * 0.3 and avg_delta < 0:
            trend = "Declining"
        elif all(abs(d) < loads[i] * 0.05 for i, d in enumerate(deltas, 1)):
            trend = "Flat"
        else:
            trend = "Erratic"

    # Also check if prescriptive values change across weeks
    sets_reps_evolution: list[list[tuple[str, str]]] = []
    for w in sorted_weeks:
        week_sr = [(e[3], e[4]) for e in fp if e[0] == w]
        sets_reps_evolution.append(week_sr)

    return {
        "trend": trend,
        "week_loads": {f"Week {w}": round(loads[i], 1) for i, w in enumerate(sorted_weeks)},
        "avg_delta_per_week": round(avg_delta, 1) if len(loads) >= 2 else 0,
        "deltas": [round(d, 1) for d in deltas] if len(loads) >= 2 else [],
    }


# ══════════════════════════════════════════════════════════════════════
# QUESTION 3: How many unique exercises?
# ══════════════════════════════════════════════════════════════════════

def audit_exercise_variety(summary: dict) -> dict:
    """Count unique exercises vs total slots. Flag if repetitive."""
    ratio = summary["uniqueness_ratio"]
    classification: str
    if ratio >= 0.8:
        classification = "Highly varied"
    elif ratio >= 0.5:
        classification = "Moderately varied"
    elif ratio >= 0.2:
        classification = "Some repetition"
    else:
        classification = "Repetitive"
    return {
        "classification": classification,
        "unique_exercises": summary["unique_exercises"],
        "total_slots": summary["total_exercise_slots"],
        "uniqueness_ratio": ratio,
        "db_exercise_count": summary["db_exercise_count"],
        "variety_score": summary["variety_score"],
        "exercises_used": summary["exercise_names"],
    }


# ══════════════════════════════════════════════════════════════════════
# QUESTION 4: Hardcoded vs rule-based
# ══════════════════════════════════════════════════════════════════════

def audit_hardcoded_vs_rule(program: GeneratedProgram) -> dict:
    """Analyze if the same exercise is always selected for the same family."""
    # Group by family and track which exercises are chosen
    family_exercises: dict[str, set[str]] = defaultdict(set)
    family_exercise_count: dict[str, Counter] = defaultdict(Counter)
    for sess in program.sessions:
        for block in sess.blocks:
            if not block.exercises:
                continue
            fcode = block.family.value if hasattr(block.family, 'value') else str(block.family)
            for ex in block.exercises:
                family_exercises[fcode].add(ex.id)
                family_exercise_count[fcode][ex.id] += 1

    # For each family that appears, compute variety
    family_variety: dict[str, dict] = {}
    total_blocks = sum(len(v) for v in family_exercise_count.values())
    for fam, ex_counter in family_exercise_count.items():
        total = sum(ex_counter.values())
        unique = len(ex_counter)
        most_common_id, most_common_count = ex_counter.most_common(1)[0]
        most_common_pct = round(most_common_count / total * 100, 1)
        family_variety[fam] = {
            "total_appearances": total,
            "unique_exercises": unique,
            "most_common": _ex_name(most_common_id),
            "most_common_pct": most_common_pct,
        }

    # If most families use the same exercise >80% of the time, flag as hardcoded
    high_repeat_fams = sum(
        1 for v in family_variety.values() if v["most_common_pct"] >= 80
    )
    classification: str
    if high_repeat_fams >= len(family_variety) * 0.5:
        classification = "Heavily hardcoded — same exercise per family every time"
    elif high_repeat_fams > 0:
        classification = "Mixed — some families have variety, some don't"
    else:
        classification = "Rule-based — exercises vary per family"

    return {
        "classification": classification,
        "family_variety": family_variety,
        "high_repeat_families": high_repeat_fams,
        "total_families_used": len(family_variety),
    }


# ══════════════════════════════════════════════════════════════════════
# QUESTION 5: Which coach inputs actually change the program?
# ══════════════════════════════════════════════════════════════════════

def audit_input_sensitivity() -> dict:
    """Generate pairs of programs differing by one input and count changes."""
    results: dict[str, dict] = {}

    # 5a. Goal: Speed vs Power
    prog_speed = _generate(_build_request(
        **{"basics": {"role": "Fast Bowler"}, "context": {"primary_goal": "speed"}}
    ))
    prog_power = _generate(_build_request(
        **{"basics": {"role": "Fast Bowler"}, "context": {"primary_goal": "power"}}
    ))
    results["goal_speed_vs_power"] = _compare_programs(prog_speed, prog_power, "Speed", "Power")

    # 5b. Role: Pace Bowler vs Batter
    progs_bowler = _generate(_build_request(**{"basics": {"role": "Pace Bowler"}}))
    progs_batter = _generate(_build_request(**{"basics": {"role": "Batter"}}))
    results["role_bowler_vs_batter"] = _compare_programs(progs_bowler, progs_batter, "Pace Bowler", "Batter")

    # 5c. Level: Beginner vs Advanced
    prog_beginner = _generate(_build_request(**{"basics": {"level": "Beginner"}}))
    prog_advanced = _generate(_build_request(**{"basics": {"level": "Advanced"}}))
    results["level_beginner_vs_advanced"] = _compare_programs(
        prog_beginner, prog_advanced, "Beginner", "Advanced"
    )

    # 5d. Sport: Cricket vs Rugby
    prog_cricket = _generate(_build_request(**{"basics": {"sport": "Cricket", "role": "Pace Bowler"}}))
    prog_rugby = _generate(_build_request(**{"basics": {"sport": "Rugby Union", "role": "Tighthead Prop"}}))
    results["sport_cricket_vs_rugby"] = _compare_programs(
        prog_cricket, prog_rugby, "Cricket", "Rugby Union"
    )

    return results


def _compare_programs(a: GeneratedProgram, b: GeneratedProgram,
                      label_a: str, label_b: str) -> dict:
    fpa = _fingerprint(a)
    fpb = _fingerprint(b)
    ids_a = set(e[2] for e in fpa)
    ids_b = set(e[2] for e in fpb)
    shared = ids_a & ids_b
    only_a = ids_a - ids_b
    only_b = ids_b - ids_a

    change_count = len(only_a) + len(only_b)
    total_unique = len(ids_a | ids_b)
    change_ratio = round(change_count / max(total_unique, 1), 4)

    return {
        "program_a": label_a,
        "program_b": label_b,
        "sessions_a": len(a.sessions),
        "sessions_b": len(b.sessions),
        "ex_slots_a": len(fpa),
        "ex_slots_b": len(fpb),
        "unique_ex_a": len(ids_a),
        "unique_ex_b": len(ids_b),
        "shared_exercises": len(shared),
        "exercises_only_in_a": len(only_a),
        "exercises_only_in_b": len(only_b),
        "change_count": change_count,
        "change_ratio": change_ratio,
        "changed_exercises": sorted(
            [_ex_name(e) for e in only_a] + [_ex_name(e) for e in only_b]
        ),
    }


# ══════════════════════════════════════════════════════════════════════
# QUESTION 6: Which inputs are currently ignored?
# ══════════════════════════════════════════════════════════════════════

def audit_ignored_inputs() -> dict:
    """Test specific inputs to see if they change output."""
    findings: dict[str, dict] = {}

    # 6a. program_length_weeks: 4 vs 12
    p4 = _generate(_build_request(**{"context": {"program_length_weeks": 4}}))
    p12 = _generate(_build_request(**{"context": {"program_length_weeks": 12}}))
    findings["program_length_weeks"] = {
        "test": "4 vs 12 weeks requested",
        "4w_actual_weeks": p4.duration,
        "12w_actual_weeks": p12.duration,
        "different": p4.duration != p12.duration,
        "conclusion": "Used" if p4.duration != p12.duration else "IGNORED — always returns 8",
    }

    # 6b. available_minutes: 30 vs 120
    p30 = _generate(_build_request(**{"basics": {"available_minutes": 30}}))
    p120 = _generate(_build_request(**{"basics": {"available_minutes": 120}}))
    ex30 = len(_fingerprint(p30))
    ex120 = len(_fingerprint(p120))
    findings["available_minutes"] = {
        "test": "30 vs 120 minutes",
        "30min_slots": ex30,
        "120min_slots": ex120,
        "different": ex30 != ex120,
        "conclusion": "Used" if ex30 != ex120 else "IGNORED",
    }

    # 6c. equipment_profile: Field Only vs Elite Facility
    pf = _generate(_build_request(**{"basics": {"environment": "Field/Track"}}))
    pe = _generate(_build_request(**{"basics": {"environment": "Elite Facility"}}))
    fpf = _fingerprint(pf)
    fpe = _fingerprint(pe)
    ids_field = set(e[2] for e in fpf)
    ids_elite = set(e[2] for e in fpe)
    findings["equipment_profile"] = {
        "test": "Field/Track vs Elite Facility",
        "field_exercises": len(ids_field),
        "elite_exercises": len(ids_elite),
        "shared": len(ids_field & ids_elite),
        "different": ids_field != ids_elite,
        "conclusion": "Used" if ids_field != ids_elite else "IGNORED",
    }

    # 6d. frequency_per_week: 2 vs 5
    p2 = _generate(_build_request(**{"basics": {"frequency_per_week": 2}}))
    p5 = _generate(_build_request(**{"basics": {"frequency_per_week": 5}}))
    findings["frequency_per_week"] = {
        "test": "2 vs 5 sessions/week requested",
        "2w_freq": p2.frequency,
        "5w_freq": p5.frequency,
        "different": p2.frequency != p5.frequency,
        "conclusion": "Used" if p2.frequency != p5.frequency else "IGNORED",
    }

    # 6e. days_to_match (competition proximity)
    pd0 = _generate(_build_request(**{"basics": {"days_to_match": 0}}))
    pd7 = _generate(_build_request(**{"basics": {"days_to_match": 7}}))
    findings["days_to_match"] = {
        "test": "0 days (match day) vs 7 days out",
        "match_day_sessions": len(pd0.sessions),
        "far_out_sessions": len(pd7.sessions),
        "different": len(pd0.sessions) != len(pd7.sessions),
        "conclusion": "Used" if len(pd0.sessions) != len(pd7.sessions) else "IGNORED",
    }

    # 6f. season_phase: off_season vs in_season
    poff = _generate(_build_request(**{"context": {"current_phase": "off_season"}}))
    pin = _generate(_build_request(**{"context": {"current_phase": "in_season"}}))
    ex_off = len(set(e[2] for e in _fingerprint(poff)))
    ex_in = len(set(e[2] for e in _fingerprint(pin)))
    findings["season_phase"] = {
        "test": "off_season vs in_season",
        "off_season_unique": ex_off,
        "in_season_unique": ex_in,
        "different": ex_off != ex_in,
        "conclusion": "Used" if ex_off != ex_in else "IGNORED",
    }

    # 6g. coach_intent / competition_proximity_note
    p_intent = _generate(_build_request(**{"context": {"competition_proximity_note": "Increase sprint exposure"}}))
    p_no_intent = _generate(_build_request(**{"context": {"competition_proximity_note": ""}}))
    intent_ids = set(e[2] for e in _fingerprint(p_intent))
    no_intent_ids = set(e[2] for e in _fingerprint(p_no_intent))
    findings["coach_intent"] = {
        "test": "competition_proximity_note set vs empty",
        "note_set_exercises": len(intent_ids),
        "no_note_exercises": len(no_intent_ids),
        "different": intent_ids != no_intent_ids,
        "conclusion": "Used" if intent_ids != no_intent_ids else "IGNORED — not read by engine",
    }

    return findings


# ══════════════════════════════════════════════════════════════════════
# QUESTION 7: Blueprint templates vs rule-based decisions
# ══════════════════════════════════════════════════════════════════════

def audit_blueprint_vs_rules(program: GeneratedProgram) -> dict:
    """Trace exercise sources: are they from fixed slot families or dynamic rules?"""
    # Every exercise comes from a family, and families are determined by
    # blueprint.slot_order. Count how many unique families are actually used
    # vs how many the blueprint defines.
    from src.forge.blueprint_engine import select_blueprint, resolve_slots
    from src.forge.data import BLUEPRINT_BY_ID

    ap = program.athlete_profile
    bp = select_blueprint(ap)
    level = AthleteLevel(program.level) if program.level else AthleteLevel.INTERMEDIATE

    families_used: Counter[str] = Counter()
    families_seen: set[str] = set()
    for sess in program.sessions:
        for block in sess.blocks:
            fcode = block.family.value if hasattr(block.family, 'value') else str(block.family)
            families_used[fcode] += 1
            families_seen.add(fcode)

    slot_families = [f.value for f in bp.slot_order]
    mandatory = [f.value for f in bp.mandatory_families]
    optional = [f.value for f in bp.optional_families]

    extra_families = families_seen - set(slot_families) - set(mandatory)
    missing_mandatory = set(mandatory) - families_seen

    # Check if all exercises come from the blueprint's families or if substitutions occur
    from_slot = sum(1 for f in families_used if f in slot_families)
    from_optional = sum(1 for f in families_used if f in optional)
    from_other = sum(1 for f in families_used if f not in slot_families and f not in mandatory and f not in optional)

    return {
        "blueprint_name": bp.name.value,
        "blueprint_id": bp.id,
        "slot_order_families": slot_families,
        "mandatory_families": mandatory,
        "families_actually_used": sorted(families_seen),
        "extra_families_not_in_blueprint": sorted(extra_families),
        "missing_mandatory_families": sorted(missing_mandatory),
        "family_appearance_counts": dict(families_used.most_common()),
        "slots_filled_from_slot_order": from_slot,
        "slots_filled_from_optional": from_optional,
        "slots_filled_from_other": from_other,
        "total_family_appearances": sum(families_used.values()),
        "conclusion": (
            "Blueprint-driven" if from_other == 0 and not missing_mandatory
            else "Mostly blueprint-driven with substitutions"
            if from_other <= sum(families_used.values()) * 0.2
            else "Heavily rule-modified from blueprint"
        ),
    }


# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════

def run_audit() -> dict:
    """Run all 7 audit modules and return structured results."""
    report: dict[str, Any] = {
        "engine_version": "forge 1.0.0",
        "db_total_exercises": len(EXERCISE_BY_ID),
    }

    # Generate baseline program
    base_req = _build_request()
    baseline = _generate(base_req)
    baseline_summary = _summarize(baseline, "Baseline (Cricket/Pace Bowler/Advanced/Strength)")
    report["baseline"] = baseline_summary

    # Q1
    report["q1_week_differentiation"] = audit_week_differentiation(baseline)

    # Q2
    report["q2_progression"] = audit_progression(baseline)

    # Q3
    report["q3_exercise_variety"] = audit_exercise_variety(baseline_summary)

    # Q4
    report["q4_hardcoded_vs_rule"] = audit_hardcoded_vs_rule(baseline)

    # Q5
    report["q5_input_sensitivity"] = audit_input_sensitivity()

    # Q6
    report["q6_ignored_inputs"] = audit_ignored_inputs()

    # Q7
    report["q7_blueprint_vs_rules"] = audit_blueprint_vs_rules(baseline)

    return report


def print_report(report: dict) -> None:
    """Pretty-print the audit report."""
    b = report["baseline"]

    print("=" * 72)
    print("FORGE ENGINE INTELLIGENCE AUDIT")
    print("=" * 72)
    print(f"Engine:       {report['engine_version']}")
    print(f"DB exercises: {report['db_total_exercises']}")
    print(f"Baseline:     {b['label']}")
    print(f"  Weeks: {b['weeks']}, Freq: {b['freq']}/week, Sessions: {b['total_sessions']}")
    print(f"  Exercise slots: {b['total_exercise_slots']}")
    print(f"  Unique exercises: {b['unique_exercises']} (ratio: {b['uniqueness_ratio']})")
    print()

    # Q1
    q1 = report["q1_week_differentiation"]
    print(f"[1] Week Differentiation:  {q1['classification']}")
    if q1.get("week_detail"):
        for wk, exs in list(q1["week_detail"].items())[:3]:
            print(f"      {wk}: {exs[:4]}...")
        if len(q1["week_detail"]) > 3:
            print(f"      ... ({len(q1['week_detail'])} weeks total)")
    print()

    # Q2
    q2 = report["q2_progression"]
    print(f"[2] Progression Trend:    {q2['trend']}")
    for wk, load in q2["week_loads"].items():
        print(f"      {wk}: load={load}")
    print()

    # Q3
    q3 = report["q3_exercise_variety"]
    print(f"[3] Exercise Variety:     {q3['classification']}")
    print(f"      {q3['unique_exercises']} unique / {q3['total_slots']} slots = {q3['uniqueness_ratio']:.1%}")
    print(f"      vs DB size: {q3['db_exercise_count']} (variety score: {q3['variety_score']:.1%})")
    print(f"      Exercises used ({len(q3['exercises_used'])}): {', '.join(sorted(q3['exercises_used'])[:12])}")
    if len(q3['exercises_used']) > 12:
        print(f"        ... and {len(q3['exercises_used']) - 12} more")
    print()

    # Q4
    q4 = report["q4_hardcoded_vs_rule"]
    print(f"[4] Hardcoded vs Rule:    {q4['classification']}")
    for fam, info in q4["family_variety"].items():
        bar = "#" * min(int(info['most_common_pct'] / 5), 20)
        print(f"      {fam:6s}: {bar} {info['most_common_pct']:.0f}% '{info['most_common']}'  "
              f"({info['unique_exercises']} unique / {info['total_appearances']} appearances)")
    print()

    # Q5
    q5 = report["q5_input_sensitivity"]
    print("[5] Input Sensitivity:")
    for test_name, result in q5.items():
        print(f"      {test_name}:")
        print(f"        A={result['program_a']} ({result['ex_slots_a']} slots, {result['unique_ex_a']} unique)")
        print(f"        B={result['program_b']} ({result['ex_slots_b']} slots, {result['unique_ex_b']} unique)")
        print(f"        shared={result['shared_exercises']}, changed={result['change_count']} "
              f"({result['change_ratio']:.1%} of total)")
        if result['changed_exercises'] and len(result['changed_exercises']) <= 10:
            print(f"        changed: {', '.join(result['changed_exercises'])}")
        elif result['changed_exercises']:
            print(f"        changed ({len(result['changed_exercises'])} ex): "
                  f"{', '.join(result['changed_exercises'][:5])}...")
    print()

    # Q6
    q6 = report["q6_ignored_inputs"]
    print("[6] Input Ignorance Check:")
    for test_name, result in q6.items():
        emoji = "[OK]" if result.get("different") else "[IGNORED]"
        print(f"      {emoji} {test_name}: {result['conclusion']}")
    print()

    # Q7
    q7 = report["q7_blueprint_vs_rules"]
    print(f"[7] Blueprint vs Rules:   {q7['conclusion']}")
    print(f"      Blueprint: {q7['blueprint_name']} (ID={q7['blueprint_id']})")
    print(f"      Families in slot_order: {q7['slot_order_families']}")
    print(f"      Families actually used: {q7['families_actually_used']}")
    if q7['missing_mandatory_families']:
        print(f"      [WARN] Missing mandatory: {q7['missing_mandatory_families']}")
    if q7['extra_families_not_in_blueprint']:
        print(f"      + Extra (substitutions): {q7['extra_families_not_in_blueprint']}")
    print()

    print("=" * 72)
    print("END AUDIT")
    print("=" * 72)


if __name__ == "__main__":
    import time
    t0 = time.time()
    report = run_audit()
    elapsed = time.time() - t0
    print_report(report)
    print(f"\nAudit completed in {elapsed:.1f}s")

    # Optionally dump raw JSON
    import os
    out_path = os.path.join(os.path.dirname(__file__), "audit_report.json")
    with open(out_path, "w") as f:
        # Convert sets to lists for JSON
        def _clean(o):
            if isinstance(o, set):
                return sorted(o)
            return o
        json.dump(report, f, indent=2, default=_clean)
    print(f"Raw report saved to {out_path}")
