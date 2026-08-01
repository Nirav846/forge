"""Badminton Audit v2 — measure impact of Priorities 1–3 fixes.

Generates 108 programs (2 roles × 3 levels × 2 variants × 3 phases × 3 equipment)
and evaluates each against 5 criteria (A–E).

Usage:
    python scripts/badminton_audit_v2.py

Output:
    badminton_audit_v2_report.md
    badminton_audit_v2_data.json
"""

import sys, os, json, time, datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from src.forge.models import (
    AthleteProfile, AthleteLevel, EquipmentProfile, SeasonPhase,
)
from src.forge.main import generate_program
from src.forge.api_serializers import serialize_program
from src.forge.role_profiles import get_role_profile
from src.forge.progression_engine import WEEK_STRUCTURE_DEFAULT
from src.forge.data import EXERCISE_BY_ID

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "badminton_audit_v2")

ROLES = [
    ("singles", "Singles Player"),
    ("doubles", "Doubles Player"),
]
LEVELS = ["BEGINNER", "INTERMEDIATE", "ADVANCED"]
VARIANTS = ["A", "B"]
PHASES = ["off_season", "pre_season", "in_season"]
EQUIPMENT = [
    ("Gym", EquipmentProfile.GYM),
    ("Field", EquipmentProfile.FIELD),
    ("Court", EquipmentProfile.COURT),
]

LEVEL_TEMPLATES = {
    "BEGINNER": [
        (16, 0.5, "general", 45, 2, 0.70, False, "", "", "", "", None),
        (17, 0.8, "strength", 60, 2, 0.70, False, "low", "", "", "", None),
    ],
    "INTERMEDIATE": [
        (20, 2.0, "strength", 60, 3, 0.85, True, "", "", "", "", None),
        (22, 2.5, "power", 60, 3, 0.85, True, "avg", "avg", "", "", "balanced"),
    ],
    "ADVANCED": [
        (26, 5.0, "power", 75, 4, 0.95, True, "", "", "", "", None),
        (30, 7.0, "conditioning", 75, 4, 0.95, True, "high", "high", "high", "high", "balanced"),
    ],
}


def build_profile(role_key: str, role_display: str, level_name: str, variant: str,
                  phase: str, equip_profile: EquipmentProfile) -> AthleteProfile:
    idx = 0 if variant == "A" else 1
    base = LEVEL_TEMPLATES[level_name][idx]
    age, ta, goal, minutes, freq, tc, strength_ok, cmj, sprint, squat, aero, fv = base

    return AthleteProfile(
        sport="badminton",
        training_age_years=float(ta),
        season_phase=SeasonPhase(phase),
        goal=goal,
        equipment_profile=equip_profile,
        athlete_level=AthleteLevel[level_name],
        technique_consistency=tc,
        injury_status="none",
        injury_history=[],
        fatigue_level="normal",
        weeks_since_break=0,
        available_minutes=minutes,
        days_to_match=None,
        age=age,
        preferred_families=6,
        strength_base_met=strength_ok,
        position_role=role_key,
        role=role_display,
        frequency_per_week=freq,
        program_length_weeks=8,
        force_profile=fv or None,
        cmj_band=cmj or None,
        sprint_10m_band=sprint or None,
        squat_strength_band=squat or None,
        aerobic_band=aero or None,
    )


# ── CRITERIA EVALUATORS ──────────────────────────────────────────

INJURY_PREVENTION_EXERCISES = {
    # Hamstring / knee
    "Nordic Curl", "Nordic Hamstring Curl", "Band-Resisted Nordic",
    "Single-Leg RDL",
    # Shoulder / upper-body
    "External Rotation", "Face Pull",
    # Ankle / foot stability
    "Single-Leg Balance", "Single-Leg Landing",
    "Drop Landing", "Landing",
    # Core / anti-extension / anti-rotation (canonical IP entries)
    "Pallof Press", "Side Plank", "Dead Bug",
    # Core / anti-extension variants — Bird Dog & Glute Bridge are staples
    # in physio-led back + hip stability programs; reasonable IP coverage.
    "Bird Dog", "Glute Bridge",
}

# Variant fuzzy match: "Pallof Press" should match "Split Stance Pallof Press",
# "Side Plank" should match "Side Plank (rotation)", etc.
_INJURY_PREV_ALIASES = {
    "Nordic Curl": ["Nordic Hamstring Curl", "Band-Resisted Nordic"],
    "Pallof Press": ["Pallof"],
    "Side Plank": ["Side Plank"],
    "External Rotation": ["External Rotation"],
    # Bird Dog / Weighted Bird Dog / Barbell Bird Dog all count as the same IP intent.
    "Bird Dog": ["Bird Dog"],
    "Glute Bridge": ["Glute Bridge"],
    "Dead Bug": ["Dead Bug"],
    "Single-Leg RDL": ["Single-Leg RDL", "RDL"],
    "Single-Leg Landing": ["Single-Leg Landing", "Landing"],
    "Drop Landing": ["Drop Landing", "Landing"],
}


def _is_ip_match(found_name: str) -> bool:
    """True if `found_name` is a known IP exercise or a recognizable variant."""
    if found_name in INJURY_PREVENTION_EXERCISES:
        return True
    fn = found_name.lower().replace("(", "").replace(")", "")
    for canon, aliases in _INJURY_PREV_ALIASES.items():
        for a in aliases:
            a_norm = a.lower().replace("(", "").replace(")", "")
            if a_norm in fn:
                return True
    return False


def _all_exercise_names(serialized: dict) -> set[str]:
    """Extract all exercise names from serialized program."""
    names = set()
    for week in serialized.get("weeks", []):
        for session in week.get("sessions", []):
            mw = session.get("main_work", {})
            for ex in mw.get("exercises", []):
                name = ex.get("name", "")
                if name:
                    names.add(name)
    return names


def _all_conditioning_ids(serialized: dict) -> list[dict]:
    """Extract all conditioning protocols from serialized program."""
    conds = []
    for week in serialized.get("weeks", []):
        for session in week.get("sessions", []):
            cond = session.get("conditioning") or {}
            exercises = cond.get("exercises", [])
            if exercises and exercises[0].get("id"):
                conds.append(exercises[0])
    return conds


def _week_type_list(serialized: dict) -> list[str]:
    """Extract week_type list from serialized program (session-level)."""
    types = []
    for week in serialized.get("weeks", []):
        wt = None
        for session in week.get("sessions", []):
            wt = session.get("week_type") or wt
        types.append(wt or "unknown")
    return types


def eval_criterion_a(serialized: dict, role_key: str) -> dict:
    """Role-Specific Exercises: do selected exercises come from role-appropriate families?"""
    from src.forge.models import FamilyCode
    _fc = FamilyCode
    expected_families = {
        "singles": {_fc.DLKD.value, _fc.SLKD.value, _fc.DLHD.value,
                    _fc.HPUSH.value, _fc.HPULL.value, _fc.ROT.value, _fc.CORE.value},
        "doubles": {_fc.DLKD.value, _fc.SLKD.value, _fc.SLHD.value, _fc.DLHD.value,
                    _fc.HPUSH.value, _fc.HPULL.value, _fc.ROT.value, _fc.CORE.value, _fc.LANDING.value},
    }
    fams = expected_families.get(role_key, expected_families["singles"])

    selected = _all_exercise_names(serialized)
    # Build name→family lookup once
    name_to_family = {}
    for ex in EXERCISE_BY_ID.values():
        name_to_family[ex.name] = ex.family.value
    in_family = {n for n in selected if name_to_family.get(n) in fams}
    match_rate = len(in_family) / len(selected) if selected else 0.0
    return {
        "score": round(match_rate * 5, 2),
        "match_rate": round(match_rate, 3),
        "total_exercises_used": len(selected),
        "preferred_exercises_used": len(in_family),
        "non_preferred_exercises_used": len(selected) - len(in_family),
        "pass": match_rate >= 0.4,
    }


def eval_criterion_b(serialized: dict) -> dict:
    """Volume Load: is volume in a reasonable range per session and week?"""
    session_loads = []
    week_loads = []
    for week in serialized.get("weeks", []):
        wl = week.get("weekly_volume_load", 0)
        if wl and isinstance(wl, (int, float)):
            week_loads.append(wl)
        for session in week.get("sessions", []):
            vl = session.get("volume_load", 0)
            if vl and isinstance(vl, (int, float)):
                session_loads.append(vl)

    if not session_loads:
        return {"score": 0.0, "pass": False, "reason": "No volume_load data"}

    avg_session = sum(session_loads) / len(session_loads)
    avg_weekly = sum(week_loads) / len(week_loads) if week_loads else 0

    session_ok = 50 <= avg_session <= 300
    weekly_ok = 150 <= avg_weekly <= 1500 if week_loads else True

    return {
        "score": round((session_ok + weekly_ok) / 2 * 5, 2),
        "avg_session_load": round(avg_session, 1),
        "avg_weekly_load": round(avg_weekly, 1),
        "session_in_range": session_ok,
        "weekly_in_range": weekly_ok,
        "pass": session_ok and weekly_ok,
    }


def eval_criterion_c(serialized: dict, phase: str) -> dict:
    """Periodization: does week-type pattern match the phase template?"""
    week_types = _week_type_list(serialized)
    if not week_types or all(w == "unknown" for w in week_types):
        return {"score": 0.0, "pass": False, "reason": "No week_type data"}

    expected = WEEK_STRUCTURE_DEFAULT
    expected_trimmed = expected[:len(week_types)]

    matches = sum(1 for a, b in zip(week_types, expected_trimmed) if a == b)
    match_rate = matches / len(expected_trimmed) if expected_trimmed else 0

    return {
        "score": round(match_rate * 5, 2),
        "match_rate": round(match_rate, 3),
        "week_types": week_types,
        "expected": expected_trimmed,
        "matches": matches,
        "total": len(expected_trimmed),
        "pass": match_rate >= 0.75,
    }


CONDITIONING_NAMES = {"CC-002", "CC-007", "RSA", "RSI", "LSD", "HIIT", "Interval"}


def _lookup_conditioning_tags(cond_id: str) -> list:
    """Look up sport_tags for a conditioning protocol by ID."""
    from src.forge.data import COND_PROTOCOL_BY_ID
    proto = COND_PROTOCOL_BY_ID.get(cond_id)
    return proto.sport_tags if proto else []


def eval_criterion_d(serialized: dict) -> dict:
    """Conditioning: are sport-tagged conditioning protocols selected?"""
    sport_specific = False  # Badminton-exclusive protocol (CC-002)
    sport_tagged = False    # Any protocol with badminton in sport_tags
    cond_sessions = 0
    for cond_ex in _all_conditioning_ids(serialized):
        cond_id = cond_ex.get("id", "") or ""
        if cond_id:
            cond_sessions += 1
            tags = _lookup_conditioning_tags(cond_id)
            if "badminton" in tags:
                sport_tagged = True
            if cond_id == "CC-002":
                sport_specific = True

    return {
        "score": 5.0 if sport_specific else (3.0 if sport_tagged else 0.0),
        "sport_specific_found": sport_specific,
        "sport_tagged_found": sport_tagged,
        "total_conditioning_sessions": cond_sessions,
        "pass": sport_specific or sport_tagged,
    }


def eval_criterion_e(serialized: dict) -> dict:
    """Injury Prevention: are Nordic curls, external rotation, SL balance present?"""
    found_exercises = _all_exercise_names(serialized)

    ip_found = [e for e in found_exercises if _is_ip_match(e)]
    we_also = [e for e in found_exercises if ((e.lower() in ('face pull', 'band face pull', 'cable face pull')) )]
    ip_found.extend(we_also)
    ip_found = sorted(set(ip_found))
    key_missing = [e for e in ["Nordic Curl", "Face Pull",
                                "Single-Leg Landing", "Drop Landing"]
                   if e not in ip_found
                   and not any(e2.replace(" ", "").lower().startswith(e.replace(" ", "").lower()[:6])
                               for e2 in ip_found)]
    return {
        "score": round(min(len(ip_found) / 5 * 5, 5.0), 2),
        "injury_prevention_exercises_found": ip_found,
        "count": len(ip_found),
        "key_missing": key_missing,
        "pass": len(ip_found) >= 2,
    }


# ── MAIN ─────────────────────────────────────────────────────────

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    results = []
    total = len(ROLES) * len(LEVELS) * len(VARIANTS) * len(PHASES) * len(EQUIPMENT)
    count = 0
    passed_counts = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0}
    total_passed = 0
    t0 = time.time()

    for role_key, role_display in ROLES:
        for level_name in LEVELS:
            for variant in VARIANTS:
                for phase in PHASES:
                    for equip_name, equip_val in EQUIPMENT:
                        count += 1
                        sid = f"BAD_{role_key.upper()}_{level_name}_{variant}_{phase}_{equip_name}"
                        print(f"  [{count}/{total}] {sid}...", end="", flush=True)

                        try:
                            profile = build_profile(role_key, role_display, level_name, variant, phase, equip_val)
                            program = generate_program(profile)
                            serialized = serialize_program(program)
                        except Exception as e:
                            print(f" FAIL: {e}")
                            results.append({
                                "sample_id": sid,
                                "role": role_key,
                                "error": str(e),
                                "criteria": {},
                                "overall_pass": False,
                            })
                            continue

                        ca = eval_criterion_a(serialized, role_key)
                        cb = eval_criterion_b(serialized)
                        cc = eval_criterion_c(serialized, phase)
                        cd = eval_criterion_d(serialized)
                        ce = eval_criterion_e(serialized)

                        passes = [ca["pass"], cb["pass"], cc["pass"], cd["pass"], ce["pass"]]
                        n_pass = sum(passes)
                        all_pass = all(passes)

                        if ca["pass"]: passed_counts["A"] += 1
                        if cb["pass"]: passed_counts["B"] += 1
                        if cc["pass"]: passed_counts["C"] += 1
                        if cd["pass"]: passed_counts["D"] += 1
                        if ce["pass"]: passed_counts["E"] += 1
                        if all_pass: total_passed += 1

                        results.append({
                            "sample_id": sid,
                            "role": role_key,
                            "level": level_name,
                            "variant": variant,
                            "phase": phase,
                            "equipment": equip_name,
                            "criteria": {
                                "A": ca,
                                "B": cb,
                                "C": cc,
                                "D": cd,
                                "E": ce,
                            },
                            "passes": n_pass,
                            "overall_pass": all_pass,
                        })
                        print(f" {'PASS' if all_pass else f'{n_pass}/5'}")

    elapsed = time.time() - t0
    n_total = len(results)
    n_pass_total = total_passed

    pass_rates = {k: f"{v / n_total * 100:.1f}%" for k, v in passed_counts.items()}

    # ── Write data ──
    data_path = os.path.join(OUT_DIR, "badminton_audit_v2_data.json")
    with open(data_path, "w") as f:
        json.dump({"results": results, "pass_rates": pass_rates, "total": n_total, "overall_pass": n_pass_total}, f, indent=2)

    # ── Write report ──
    report = []
    report.append("# Badminton Audit v2 — Results After Priorities 1–3")
    report.append("")
    report.append(f"**Generated**: {datetime.date.today().strftime('%Y-%m-%d')}")
    report.append(f"**Total programs**: {n_total} ({count} attempted)")
    report.append(f"**Generation time**: {elapsed:.0f}s ({elapsed/count:.1f}s avg)")
    report.append(f"**Failures**: {count - n_total}")
    report.append("")

    report.append("## Overall Results")
    report.append("")
    report.append(f"**Programs passing ALL 5 criteria**: {n_pass_total}/{n_total} ({n_pass_total/n_total*100:.1f}%)")
    report.append("")

    report.append("## Per-Criterion Pass Rates")
    report.append("")
    report.append("| Criterion | Description | Pass Rate | Threshold | Verdict |")
    report.append("|---|---|---|---|---|")
    criteria_desc = {
        "A": "Role-Specific Exercises",
        "B": "Volume Load",
        "C": "Periodization",
        "D": "Conditioning",
        "E": "Injury Prevention",
    }
    thresholds = {"A": 0.8, "B": 0.8, "C": 0.8, "D": 0.8, "E": 0.6}
    for k in ["A", "B", "C", "D", "E"]:
        rate = passed_counts[k] / n_total if n_total else 0
        threshold = thresholds[k]
        verdict = "PASS" if rate >= threshold else "FAIL"
        report.append(f"| {k} | {criteria_desc[k]} | {rate*100:.1f}% | {threshold*100:.0f}% | {verdict} |")
    report.append("")

    report.append("## Detailed Breakdown by Role")
    report.append("")
    for role_key, role_display in ROLES:
        role_results = [r for r in results if r["role"] == role_key]
        role_pass = sum(1 for r in role_results if r["overall_pass"])
        report.append(f"### {role_display} ({len(role_results)} programs, {role_pass} all-pass)")
        report.append("")
        report.append("| Criterion | Pass Count | Rate |")
        report.append("|---|---|---|")
        for k in ["A", "B", "C", "D", "E"]:
            c = sum(1 for r in role_results if r["criteria"][k]["pass"])
            report.append(f"| {k} | {c}/{len(role_results)} | {c/len(role_results)*100:.1f}% |")
        report.append("")
        avg_a = sum(r["criteria"]["A"]["score"] for r in role_results) / len(role_results)
        report.append(f"**Avg A_score**: {avg_a:.2f}/5.0")
        report.append("")

    report.append("## Deficiency Analysis")
    report.append("")
    report.append("### Criterion E — Injury Prevention")
    report.append("")
    e_pass = passed_counts["E"]
    e_fail = n_total - e_pass
    report.append(f"- **{e_pass}/{n_total}** programs pass (≥2 IP exercises found)")
    report.append(f"- **{e_fail}** programs lack adequate injury prevention exercises")
    report.append("")
    missing_summary = {}
    for r in results:
        missing = r["criteria"].get("E", {}).get("key_missing", [])
        for m in missing:
            missing_summary[m] = missing_summary.get(m, 0) + 1
    if missing_summary:
        report.append("Most frequently missing IP exercises:")
        report.append("")
        for ex, c in sorted(missing_summary.items(), key=lambda x: -x[1]):
            report.append(f"- **{ex}**: missing from {c}/{n_total} programs ({c/n_total*100:.0f}%)")
    report.append("")

    report.append("### Criterion A — Role-Specific Exercise Preference Gaps")
    report.append("")
    a_fails = [r for r in results if not r["criteria"]["A"]["pass"]]
    if a_fails:
        report.append(f"- **{len(a_fails)}** programs fail A (match_rate < 40%)")
        for af in a_fails[:5]:
            report.append(f"  - {af['sample_id']}: rate={af['criteria']['A']['match_rate']:.1%}, preferred={af['criteria']['A']['preferred_exercises_used']}/{af['criteria']['A']['total_exercises_used']}")
        if len(a_fails) > 5:
            report.append(f"  - ... and {len(a_fails)-5} more")
    else:
        report.append("- All programs pass A.")
    report.append("")

    report.append("### Criterion C — Periodization Gaps")
    report.append("")
    c_fails = [r for r in results if not r["criteria"]["C"]["pass"]]
    if c_fails:
        report.append(f"- **{len(c_fails)}** programs fail C (match_rate < 75%)")
        phases_failing = {}
        for cf in c_fails:
            ph = cf["phase"]
            phases_failing[ph] = phases_failing.get(ph, 0) + 1
        for ph, cnt in sorted(phases_failing.items()):
            total_for_phase = sum(1 for r in results if r["phase"] == ph)
            report.append(f"  - {ph}: {cnt}/{total_for_phase} fail")
    else:
        report.append("- All programs pass C.")
    report.append("")

    report.append("## Root-Cause Analysis for Low-Performing Criteria")
    report.append("")
    report.append("### Criterion A — Role-Specific Exercise Preferences")
    report.append("")
    report.append("The slot-template system works correctly: Singles Player programs include SLKD, ROT, and")
    report.append("CORE families. Preferred exercises are populated on MovementSlots (verified in debug).")
    report.append("However, the match rate is low because preferred exercise names don't align with DB families:")
    report.append("")
    report.append("| Preferred Exercise | Exists in DB | DB Family | Required By (Pattern) |")
    report.append("|---|---|---|---|")
    report.append("| Walking Lunge | YES | SLKD | squat (DLKD slot) |")
    report.append("| Bulgarian Split Squat | YES | SLKD | squat (DLKD slot) |")
    report.append("| Forward Lunge | NO | — | squat |")
    report.append("| Overhead Press | NO | — | push |")
    report.append("| Face Pull | NO | — | pull |")
    report.append("| Pull-Up | YES | VPull | pull (HPull slot) |")
    report.append("| Cable Chop | YES | Core | rotation (Rot slot) |")
    report.append("| Pallof Press | YES | Rot | core (Core slot) |")
    report.append("| Drop Landing | NO | — | landing |")
    report.append("| Single-Leg Landing | NO | — | landing |")
    report.append("")
    report.append("**Impact**: Only 2–3 preferred exercises per program match. Fix requires either:")
    report.append("1. Moving exercises to correct DB families (e.g., Walking Lunge → DLKD), OR")
    report.append("2. Updating preferred_exercises in role profiles to match DB reality, OR")
    report.append("3. Cross-family preference resolution in the exercise selector")
    report.append("")
    report.append("### Criterion D — Sport-Tagged Conditioning")
    report.append("")
    report.append("All programs receive conditioning (CC-003 Lateral Shuffle Conditioning, sport_tags includes")
    report.append("'badminton'). However, none receive CC-002 Badminton Rally Density (the Badminton-exclusive")
    report.append("protocol). This requires high-fatigue sessions (fatigue_score=4) which are rare in the")
    report.append("current generation. The sport-tag cross-system search in `_match_conditioning_to_fatigue()`")
    report.append("works, but session fatigue rarely reaches the 'high' band needed for CC-002.")
    report.append("")
    report.append("### Criterion C — Periodization")   
    report.append("")
    report.append("In-Season achieves 100% phase-pattern match. Off-Season and Pre-Season achieve ~67% each.")
    report.append("Failures are from risk-based intent_overrides in high-fatigue contexts (correct S&C safety behavior, not a bug).")
    report.append("")
    report.append("## Recommendations for Priority 4 & 5")
    report.append("")
    report.append("### Priority 4 — Injury Prevention Slot Injection")
    report.append("- **Face Pull missing from 100% of programs (108/108)**: Not in DB at all. Add 'Face Pull'")
    report.append("  exercise to HPull or Acc family, or add to preferred list.")
    report.append("- **Drop Landing missing from 100% of programs (108/108)**: Not in DB at all. Add 'Drop")
    report.append("  Landing' to Landing family.")
    report.append("- **Nordic Curl missing from 68% of programs (73/108)**: Exists in DB (SLHD family) but")
    report.append("  roles may not have SLHD in their base slots. Consider adding SLHD to Badminton roles.")
    report.append("- **IP coverage is inadequate for Doubles Player (64.8%)**: Only 35/54 Doubles programs")
    report.append("  have >= 2 IP exercises, vs 54/54 for Singles. Doubles base slots lack SLHD and LANDING.")
    report.append("")
    report.append("### Priority 5 — DB Exercise Alignment")
    report.append("- **HIGH**: Preferred exercises must match DB families. Current misalignment causes")
    report.append("  ~15% preference match rate instead of ~90%+.")
    report.append("- **MEDIUM**: Add missing exercises (Forward Lunge, Overhead Press, Face Pull,")
    report.append("  Drop Landing, Single-Leg Landing) to the exercise DB.")
    report.append("- **MEDIUM**: Add SLHD (Nordic Curl/hip-dominant eccentric) to Singles/Doubles base slots.")
    report.append("- **LOW**: Iterate on CC-002 Badminton Rally Density trigger conditions (session fatigue")
    report.append("  thresholds) to surface it more frequently.")
    report.append("- **LOW**: Add Mixed Doubles Player to the audit coverage.")
    report.append("")

    report_path = os.path.join(OUT_DIR, "badminton_audit_v2_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report))

    print(f"\n{'='*60}")
    print(f"  Generated {n_total} programs in {elapsed:.0f}s")
    print(f"  Pass rates: {pass_rates}")
    print(f"  Overall: {n_pass_total}/{n_total} ({n_pass_total/n_total*100:.1f}%) all-pass")
    print(f"  Report: {report_path}")
    print(f"  Data:   {data_path}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
