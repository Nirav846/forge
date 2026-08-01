"""Audit sport-specific exercise coverage across all roles."""

import sys
from collections import defaultdict

sys.path.insert(0, "src")

from forge.exercises_data import EXERCISES_DATA
from forge.role_week_planning import _SPORT_DEFAULTS, _ROLE_PROFILES
from forge.models import FamilyCode


SPORTS = ["cricket", "badminton", "tennis", "volleyball", "rugby", "soccer", "football", "basketball"]

FAMILY_LABELS = {
    "DLKD": "Squat (DLKD)",
    "DLHD": "Hinge (DLHD)",
    "SLKD": "Single-Leg Squat (SLKD)",
    "SLHD": "Single-Leg Hinge (SLHD)",
    "HPush": "Horizontal Push",
    "HPull": "Horizontal Pull",
    "VPush": "Vertical Push",
    "VPull": "Vertical Pull",
    "Plyo": "Plyometric",
    "Ball": "Ball / Implement",
    "Sprint": "Sprint / Acceleration",
    "Landing": "Landing Mechanics",
    "Rot": "Rotation",
    "Carry": "Carry / Loaded Walk",
    "Core": "Core Stability",
    "Acc": "Accessory / Prehab",
    "Agility": "Agility / COD",
    "Cond": "Conditioning",
}

FAMILY_USAGE = {
    "DLKD": "Squat pattern - bilateral knee-dominant",
    "DLHD": "Hinge pattern - bilateral hip-dominant",
    "SLKD": "Single-leg squat/lunge pattern",
    "SLHD": "Single-leg hinge pattern",
    "HPush": "Horizontal pushing (bench, row)",
    "HPull": "Horizontal pulling (row, lat)",
    "VPush": "Vertical pushing (overhead press)",
    "VPull": "Vertical pulling (pull-up, lat pulldown)",
    "Plyo": "Plyometric / explosive movement",
    "Ball": "Ball / implement manipulation",
    "Sprint": "Sprint / acceleration mechanics",
    "Landing": "Landing mechanics and absorption",
    "Rot": "Rotational power and control",
    "Carry": "Loaded carry / trunk stability under load",
    "Core": "Core stability and anti-movement",
    "Acc": "Accessory / prehab / injury prevention",
    "Agility": "Agility / change of direction",
    "Cond": "Conditioning / energy system development",
}

ROLE_NEEDS_DESC = {
    "prop": "Scrummaging power, collision readiness, neck + shoulder robustness",
    "hooker": "Scrum + lineout power, mobility for throws",
    "lock": "Lineout jumping, collision force, scrum power",
    "back_row": "All-round athleticism, breakdown work, link play",
    "scrum_half": "Agility, passing accuracy, quick decision-making",
    "fly_half": "Distributor, kicking, evasion, game management",
    "centre": "Midfield collisions, line-breaking power, passing",
    "back_three": "Open-field running, high-ball catching, finishing",
    "fast_bowler": "Repeated high-velocity bowling, eccentric hamstring, landing",
    "spin_bowler": "Rotation-dominant, trunk control, shoulder stability",
    "batter": "Rotational power, sprint between wickets, throwing",
    "wicketkeeper": "Agility, crouched stability, explosive diving",
    "all_rounder": "Balanced batting + bowling demands",
    "singles": "High-volume court coverage, endurance, power",
    "doubles": "Net play, overhead power, lateral agility",
    "middle_blocker": "Vertical jumping, blocking, landing absorption",
    "outside_hitter": "Attack jumping, arm swing power, lateral movement",
    "opposite": "Back-court attack, blocking, rotation power",
    "setter": "Hand-eye coordination, overhead control, agility",
    "libero": "Defensive coverage, diving, passing accuracy",
    "goalkeeper": "Diving, explosive lateral movement, landing",
    "centre_back": "Aerial duels, physical defending, heading",
    "fullback": "Tactical speed, recovery running, crossing",
    "midfielder": "Endurance, change of direction, passing",
    "winger": "Pure speed, finishing, 1v1 attacking",
    "striker": "Finishing, explosive acceleration, hold-up play",
    "guard": "Ball handling, agility, perimeter shooting",
    "wing": "Slashing drives, perimeter D, lateral quickness",
    "big": "Post play, rebounding, verticality, interior D",
}


def _load_existing():
    sport_ex = defaultdict(list)
    for ex in EXERCISES_DATA:
        sf = ex.get("secondary_family")
        if sf and sf.lower() in SPORTS:
            sport_ex[sf.lower()].append(ex)
        elif sf and sf.lower() == "football":
            sport_ex["football"].append(ex)
    return sport_ex


def _families_for_sport(sport: str) -> list[str]:
    roles = _ROLE_PROFILES.get(sport, {})
    families = set()
    for role, profile in roles.items():
        families.update(profile.family_priority)
    return sorted(families, key=_family_sort_key)


def _family_sort_key(f: str) -> int:
    order = [
        "DLKD", "DLHD", "SLKD", "SLHD",
        "Sprint", "Plyo", "Ball", "Landing",
        "Rot", "Carry",
        "HPush", "HPull", "VPush", "VPull",
        "Core", "Acc", "Agility", "Cond",
    ]
    try:
        return order.index(f)
    except ValueError:
        return len(order)


def _coverage_grade(existing: int, needed: int) -> str:
    if needed <= 0:
        return "-"
    ratio = existing / needed if needed else 0
    if ratio >= 1.0:
        return "full"
    if ratio >= 0.5:
        return "partial"
    return "gap"


MANDATORY_FAMILIES_PER_SPORT = {
    "cricket": {
        "batter": {"Rot": 2, "Sprint": 2, "Ball": 1, "HPush": 1, "HPull": 1, "Core": 2},
        "fast_bowler": {"Sprint": 2, "Landing": 2, "SLKD": 2, "SLHD": 3, "Core": 2, "Acc": 2},
        "spin_bowler": {"Rot": 2, "Core": 2, "HPush": 1, "HPull": 1},
        "wicketkeeper": {"SLKD": 2, "Core": 2, "Rot": 1, "Landing": 1, "DLKD": 1},
        "all_rounder": {"Sprint": 2, "Rot": 2, "DLKD": 1, "SLKD": 1, "Core": 2},
    },
    "badminton": {
        "singles": {"Sprint": 3, "Landing": 2, "SLKD": 2, "SLHD": 2, "Core": 2, "Agility": 2, "Cond": 1},
        "doubles": {"Plyo": 2, "Ball": 1, "VPush": 1, "VPull": 1, "SLKD": 2, "Landing": 1},
    },
    "tennis": {
        "singles": {"Sprint": 2, "Landing": 2, "SLKD": 2, "SLHD": 2, "Core": 2, "Rot": 2, "Agility": 2},
        "doubles": {"Plyo": 2, "Ball": 1, "VPush": 1, "VPull": 1, "Landing": 1},
    },
    "volleyball": {
        "middle_blocker": {"Plyo": 3, "Landing": 3, "DLKD": 1, "VPush": 1, "VPull": 1, "Core": 2},
        "outside_hitter": {"Plyo": 3, "Landing": 3, "HPush": 1, "HPull": 1, "Rot": 1, "Core": 2},
        "opposite": {"Plyo": 3, "Landing": 2, "HPush": 1, "HPull": 1, "Rot": 2, "Core": 2},
        "setter": {"SLKD": 2, "SLHD": 1, "Core": 2, "Rot": 1},
        "libero": {"Landing": 2, "SLKD": 2, "SLHD": 1, "Sprint": 1, "Core": 2},
    },
    "rugby": {
        "prop": {"DLKD": 2, "DLHD": 2, "HPush": 2, "HPull": 1, "Core": 2, "Carry": 1, "Acc": 2},
        "hooker": {"DLKD": 2, "DLHD": 2, "HPush": 2, "Core": 2, "Carry": 1, "Landing": 1, "Acc": 2},
        "lock": {"DLKD": 2, "DLHD": 2, "Plyo": 2, "Landing": 2, "HPush": 1, "Core": 2, "Acc": 2},
        "back_row": {"DLKD": 2, "DLHD": 2, "Sprint": 2, "Core": 2, "Carry": 1, "Acc": 2},
        "scrum_half": {"Sprint": 2, "Ball": 1, "SLKD": 2, "SLHD": 1, "Core": 2, "Agility": 2},
        "fly_half": {"Sprint": 2, "Rot": 1, "Ball": 2, "Core": 2, "SLKD": 2, "Agility": 2},
        "centre": {"Sprint": 2, "Plyo": 1, "Ball": 1, "DLKD": 1, "Core": 2, "Acc": 2},
        "back_three": {"Sprint": 3, "Plyo": 2, "Ball": 2, "Core": 2, "Landing": 2, "Agility": 2},
    },
    "soccer": {
        "goalkeeper": {"Plyo": 2, "Landing": 3, "Ball": 1, "SLKD": 2, "SLHD": 2, "Core": 2},
        "centre_back": {"DLKD": 2, "DLHD": 2, "Sprint": 2, "Core": 2, "Carry": 1, "Acc": 2, "Landing": 1},
        "fullback": {"Sprint": 3, "SLKD": 2, "SLHD": 2, "Core": 2, "Carry": 1, "Agility": 2, "Landing": 1},
        "midfielder": {"Sprint": 2, "SLKD": 2, "SLHD": 2, "Core": 2, "Carry": 1, "Agility": 2, "Cond": 1},
        "winger": {"Sprint": 3, "Plyo": 1, "Ball": 2, "Core": 2, "Agility": 2, "Landing": 1},
        "striker": {"Sprint": 3, "Plyo": 2, "Ball": 2, "Landing": 1, "DLKD": 1, "Agility": 2},
    },
    "football": {
        "goalkeeper": {"Plyo": 2, "Landing": 3, "Ball": 1, "SLKD": 2, "SLHD": 2, "Core": 2},
        "centre_back": {"DLKD": 2, "DLHD": 2, "Sprint": 2, "Core": 2, "Carry": 1, "Acc": 2, "Landing": 1},
        "fullback": {"Sprint": 3, "SLKD": 2, "SLHD": 2, "Core": 2, "Carry": 1, "Agility": 2, "Landing": 1},
        "midfielder": {"Sprint": 2, "SLKD": 2, "SLHD": 2, "Core": 2, "Carry": 1, "Agility": 2, "Cond": 1},
        "winger": {"Sprint": 3, "Plyo": 1, "Ball": 2, "Core": 2, "Agility": 2, "Landing": 1},
        "striker": {"Sprint": 3, "Plyo": 2, "Ball": 2, "Landing": 1, "DLKD": 1, "Agility": 2},
    },
    "basketball": {
        "guard": {"Sprint": 3, "Plyo": 2, "Ball": 2, "SLKD": 2, "SLHD": 2, "Core": 2},
        "wing": {"Sprint": 2, "Plyo": 3, "Ball": 2, "HPush": 1, "HPull": 1, "Core": 2, "Landing": 2},
        "big": {"DLKD": 2, "DLHD": 2, "Plyo": 3, "Landing": 3, "HPush": 1, "HPull": 1, "Core": 2},
    },
}


def main():
    existing = _load_existing()

    report: list[str] = []
    def emit(line: str = ""):
        report.append(line)
        print(line)

    emit("# Sport-Specific Exercise Coverage Audit")
    emit("")
    emit(f"Generated: auto-audit")
    emit("")
    emit(
        "Analyzes sport-specific exercise coverage by comparing existing exercises "
        "tagged with `secondary_family=<sport>` against the movement families needed "
        "by each role in that sport."
    )
    emit("")
    emit("## Coverage Summary")
    emit("")
    header = f"{'Sport':<16} {'Roles':<8} {'Existing':<10} {'Needed':<8} {'Families covered':<18} {'Families gapped':<18}"
    emit(header)
    emit("-" * len(header))
    for sport in SPORTS:
        roles = _ROLE_PROFILES.get(sport, {})
        ex_list = existing.get(sport, [])
        ex_families = set(e["family"] for e in ex_list)
        needed_families = set(_families_for_sport(sport))
        gapped = sorted(needed_families - ex_families, key=_family_sort_key)
        covered = sorted(needed_families & ex_families, key=_family_sort_key)
        emit(
            f"{sport:<16} {len(roles):<8} {len(ex_list):<10} "
            f"{len(needed_families):<8} "
            f"{','.join(covered) if covered else '-':<18} "
            f"{','.join(gapped) if gapped else '-':<18}"
        )
    emit("")

    for sport in SPORTS:
        roles = _ROLE_PROFILES.get(sport, {})
        ex_list = existing.get(sport, [])
        ex_by_family = defaultdict(list)
        for e in ex_list:
            ex_by_family[e["family"]].append(e)

        emit(f"---")
        emit(f"## {sport.title()}")
        emit("")
        sport_default = _SPORT_DEFAULTS.get(sport)
        if sport_default:
            emit(f"**Sport defaults:** force={sport_default.force_emphasis} "
                 f"velocity={sport_default.velocity_emphasis} "
                 f"conditioning={sport_default.conditioning_emphasis} "
                 f"rotation={sport_default.rotation_emphasis} "
                 f"landing={sport_default.landing_emphasis} "
                 f"upper_body={sport_default.upper_body_emphasis}")
        emit("")

        emit(f"**Existing sport-specific exercises ({len(ex_list)} total):**")
        emit("")
        if ex_list:
            tbl = f"{'ID':<14} {'Name':<40} {'Family':<10} {'Diff':<6} {'Objective':<6}"
            emit(tbl)
            emit("-" * len(tbl))
            for e in sorted(ex_list, key=lambda x: (x["family"], x["difficulty"], x["id"])):
                emit(f"{e['id']:<14} {e['name']:<40} {e['family']:<10} {e['difficulty']:<6} {e['objective']:<6}")
        else:
            emit("*(none)*")
        emit("")

        role_needs = MANDATORY_FAMILIES_PER_SPORT.get(sport, {})
        if role_needs:
            emit("### Role-by-Role Gap Analysis")
            emit("")
            for role, needed in role_needs.items():
                role_desc = ROLE_NEEDS_DESC.get(role, "")
                emit(f"**{role.replace('_', ' ').title()}** - {role_desc}")
                tbl = f"{'Family':<12} {'Label':<28} {'Need':<8} {'Existing':<10} {'Status':<10} {'Suggested Exercise':<40}"
                emit(tbl)
                emit("-" * len(tbl))
                all_gaps = []
                for fam in sorted(needed, key=_family_sort_key):
                    need_count = needed[fam]
                    existing_count = sum(1 for e in ex_list if e["family"] == fam)
                    existing_ids = [e["id"] for e in ex_list if e["family"] == fam]
                    status = _coverage_grade(existing_count, need_count)
                    suggestion = _suggest_exercise(sport, fam, existing_ids, need_count)
                    if status == "? gap":
                        all_gaps.append((fam, suggestion))
                    emit(f"{fam:<12} {FAMILY_LABELS.get(fam, fam):<28} "
                         f"{need_count:<8} {existing_count:<10} "
                         f"{status:<10} {suggestion:<40}")
                emit("")
        emit("")

    with open("sport_exercise_audit.md", "w") as f:
        f.write("\n".join(report))
    print(f"\nReport written to sport_exercise_audit.md ({len(report)} lines)")


EXERCISE_TEMPLATES = {
    ("cricket", "Rot"): "Cricket-Specific Rotation (med ball / cable)",
    ("cricket", "Sprint"): "Cricket Sprint Start (first-step acceleration)",
    ("cricket", "Ball"): "Fielding Throw / Catch Drill",
    ("cricket", "Landing"): "Pace Bowler Landing (single-leg absorption)",
    ("cricket", "SLHD"): "Single-Leg Hamstring Catch (eccentric)",
    ("cricket", "Acc"): "Shoulder Prehab (rotator cuff + scap)",
    ("cricket", "Core"): "Anti-Rotation Cricket Stance Hold",
    ("cricket", "DLKD"): "Cricket Squat (loaded, stance-specific)",
    ("cricket", "DLHD"): "Cricket Deadlift (hinge for bowling/batting)",
    ("cricket", "SLKD"): "Lateral Lunge for Fielding",
    ("cricket", "HPush"): "Cricket Push-up (batting follow-through)",
    ("cricket", "HPull"): "Cricket Row (sustained pull position)",
    ("badminton", "Sprint"): "Badminton Multi-Directional Sprint",
    ("badminton", "Landing"): "Lunge Landing (deep court recovery)",
    ("badminton", "SLKD"): "Deep Lunge Hold (rack leg)",
    ("badminton", "SLHD"): "Split-Stance Hamstring (rear leg)",
    ("badminton", "Core"): "Rotational Core Hold (racking stance)",
    ("badminton", "Plyo"): "Net Kill Jump (explosive overhead)",
    ("badminton", "Agility"): "Hexagonal Footwork Drill",
    ("badminton", "Cond"): "Shadow Court Movement (interval)",
    ("badminton", "Ball"): "Shuttle / Cock Drill (manipulation)",
    ("badminton", "VPush"): "Overhead Press (smash follow-through)",
    ("badminton", "VPull"): "Lat Pulldown (racket arm pull)",
    ("tennis", "Sprint"): "Tennis Split-Step to Sprint",
    ("tennis", "Landing"): "Wide Lunge Landing (recovery)",
    ("tennis", "SLKD"): "Single-Leg Plant & Drive",
    ("tennis", "SLHD"): "Split-Stance RDL (racket side)",
    ("tennis", "Core"): "Rotational Med Ball Throw (tennis stance)",
    ("tennis", "Rot"): "Cable Rotation (forehand/backhand)",
    ("tennis", "Agility"): "Baseline COD Shuffle",
    ("tennis", "Plyo"): "Overhead Smash Jump",
    ("tennis", "Ball"): "Reaction Ball Catch",
    ("tennis", "VPush"): "Overhead Press (serve follow-through)",
    ("tennis", "VPull"): "Wide-Grip Lat Pulldown (serve prep)",
    ("volleyball", "Plyo"): "Approach Jump (3-step arm swing)",
    ("volleyball", "Landing"): "Block Landing (double-leg, soft)",
    ("volleyball", "DLKD"): "Deep Squat (setter / base position)",
    ("volleyball", "VPush"): "Block Press / Overhead Stability",
    ("volleyball", "VPull"): "Scapular Pull-up (arm swing prep)",
    ("volleyball", "Core"): "Anti-Extension Core (spiking arch)",
    ("volleyball", "HPush"): "Hitting Arm Deceleration (band)",
    ("volleyball", "HPull"): "Seated Row (spiking prep)",
    ("volleyball", "SLKD"): "Single-Leg Squat (block approach)",
    ("volleyball", "SLHD"): "Single-Leg Hinge (jump prep)",
    ("volleyball", "Rot"): "Rotational Med Ball Slam (spike)",
    ("volleyball", "Agility"): "Defensive Slide & Dig",
    ("volleyball", "Acc"): "Shoulder Prehab (external rotation)",
    ("rugby", "Sprint"): "Rugby Multi-Directional Sprint",
    ("rugby", "Plyo"): "Rugby Box Jump (collision prep)",
    ("rugby", "Ball"): "Passing Under Pressure Drill",
    ("rugby", "Landing"): "High-Ball Landing (contested)",
    ("rugby", "DLKD"): "Scrum Squat (wide stance)",
    ("rugby", "DLHD"): "Rugby Deadlift (ruck prep)",
    ("rugby", "Core"): "Anti-Rotation (contact stability)",
    ("rugby", "Carry"): "Collision Pad Carry",
    ("rugby", "HPush"): "Scrum Push / Bench Variation",
    ("rugby", "HPull"): "Rugby Row (maul prep)",
    ("rugby", "SLKD"): "Single-Leg Squat (side-step)",
    ("rugby", "SLHD"): "Nordic Curl (hamstring)",
    ("rugby", "Acc"): "Neck & Shoulder Prehab",
    ("rugby", "Agility"): "Side-Step / Evasion Drill",
    ("rugby", "Cond"): "Rugby-Specific Interval",
    ("soccer", "Sprint"): "Soccer Acceleration (first 5m)",
    ("soccer", "Plyo"): "Soccer Box Jump (heading prep)",
    ("soccer", "Ball"): "Passing / Crossing Accuracy Drill",
    ("soccer", "Landing"): "Single-Leg Landing (shot follow-through)",
    ("soccer", "DLKD"): "Single-Leg Squat (kicking leg)",
    ("soccer", "DLHD"): "Soccer Deadlift (kicking hinge)",
    ("soccer", "Core"): "Anti-Rotation (kicking stability)",
    ("soccer", "Carry"): "Loaded Walk (shield carry)",
    ("soccer", "SLKD"): "Single-Leg Squat (plant leg)",
    ("soccer", "SLHD"): "Single-Leg RDL (kicking leg)",
    ("soccer", "Agility"): "Ladder / COD Circuit",
    ("soccer", "Cond"): "Repeated Sprint Ability (RSA)",
    ("soccer", "Acc"): "Hip Adductor Prehab",
    ("football", "Sprint"): "Football Acceleration (first 5m)",
    ("football", "Plyo"): "Football Box Jump (heading prep)",
    ("football", "Ball"): "Passing / Crossing Accuracy Drill",
    ("football", "Landing"): "Single-Leg Landing (shot follow-through)",
    ("football", "DLKD"): "Single-Leg Squat (kicking leg)",
    ("football", "DLHD"): "Football Deadlift (kicking hinge)",
    ("football", "Core"): "Anti-Rotation (kicking stability)",
    ("football", "Carry"): "Loaded Walk (shield carry)",
    ("football", "SLKD"): "Single-Leg Squat (plant leg)",
    ("football", "SLHD"): "Single-Leg RDL (kicking leg)",
    ("football", "Agility"): "Ladder / COD Circuit",
    ("football", "Cond"): "Repeated Sprint Ability (RSA)",
    ("football", "Acc"): "Hip Adductor Prehab",
    ("basketball", "Sprint"): "Basketball Sprint (transition)",
    ("basketball", "Plyo"): "Basketball Vertical Jump (max effort)",
    ("basketball", "Ball"): "Dribbling Under Pressure Drill",
    ("basketball", "Landing"): "Rebound Landing (absorb + explode)",
    ("basketball", "DLKD"): "Deep Squat (defensive stance)",
    ("basketball", "DLHD"): "Deadlift (post-play strength)",
    ("basketball", "Core"): "Anti-Rotation (contact finish)",
    ("basketball", "HPush"): "Pass Push (chest pass strength)",
    ("basketball", "HPull"): "Basketball Row (rebound prep)",
    ("basketball", "SLKD"): "Single-Leg Squat (cutting leg)",
    ("basketball", "SLHD"): "Single-Leg Hinge (jump prep)",
    ("basketball", "Agility"): "Defensive Slide COD",
    ("basketball", "Acc"): "Ankle Prehab / ACL Prevention",
}


def _suggest_exercise(sport: str, family: str, existing_ids: list[str], need_count: int) -> str:
    if len(existing_ids) >= need_count:
        return "(sufficient)"
    key = (sport, family)
    template = EXERCISE_TEMPLATES.get(key, "")
    if template:
        return template
    # Fallback: generate generic suggestion
    return f"{sport.title()}-Specific {FAMILY_LABELS.get(family, family)}"


if __name__ == "__main__":
    main()
