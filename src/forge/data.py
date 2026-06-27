"""
FORGE seed data — embedded directly in Python.
No SQL, no JSON, no YAML. Hardcoded datasets.
"""
from .models import (
    Exercise, ExerciseFamily, Blueprint, ConditioningProtocol,
    FamilyCode, Objective, SeasonPhase, BlueprintName
)

# ── Helper to parse family string ─────────────────────────────────
def _fc(s: str) -> FamilyCode:
    return FamilyCode(s)

def _obj(s: str) -> Objective:
    return Objective(s)

# ── Exercise competition metadata inference ────────────────────────

# Base fatigue by family (1-5)
_EX_FATIGUE_BASE = {
    "DLKD": 3, "DLHD": 3, "SLKD": 3, "SLHD": 3,
    "HPush": 3, "HPull": 3, "VPush": 3, "VPull": 3,
    "Plyo": 3, "Ball": 3, "Sprint": 3, "Landing": 3,
    "Rot": 2, "Carry": 2, "Core": 1, "Acc": 2,
    "Agility": 3, "Cond": 4,
}
# Base impact by family (1-5)
_EX_IMPACT_BASE = {
    "DLKD": 3, "DLHD": 3, "SLKD": 3, "SLHD": 3,
    "HPush": 3, "HPull": 3, "VPush": 3, "VPull": 3,
    "Plyo": 4, "Ball": 4, "Sprint": 3, "Landing": 4,
    "Rot": 2, "Carry": 2, "Core": 1, "Acc": 2,
    "Agility": 3, "Cond": 3,
}
# Base eccentric by family (1-5)
_EX_ECCENTRIC_BASE = {
    "DLKD": 3, "DLHD": 3, "SLKD": 3, "SLHD": 3,
    "HPush": 3, "HPull": 3, "VPush": 2, "VPull": 3,
    "Plyo": 2, "Ball": 1, "Sprint": 1, "Landing": 2,
    "Rot": 2, "Carry": 1, "Core": 1, "Acc": 2,
    "Agility": 1, "Cond": 1,
}
# Competition role by family
_EX_ROLE = {
    "DLKD": "strength", "DLHD": "strength", "SLKD": "strength", "SLHD": "strength",
    "HPush": "strength", "HPull": "strength", "VPush": "strength", "VPull": "strength",
    "Plyo": "speed_power", "Ball": "speed_power", "Sprint": "speed_power", "Landing": "speed_power",
    "Rot": "accessory", "Carry": "carry", "Core": "core", "Acc": "accessory",
    "Agility": "speed_power", "Cond": "speed_power",
}
# Explicit overrides for exercises where inference is wrong
_EX_COMP_OVERRIDES: dict[str, dict] = {}


def _infer_exercise_comp_metadata(ed: dict) -> dict:
    fam = ed["family"]
    diff = ed["difficulty"]
    explosive = ed.get("explosive", False)
    isometric = ed.get("isometric", False)
    name = ed.get("name", "").lower()

    eid = ed["id"]
    if eid in _EX_COMP_OVERRIDES:
        return _EX_COMP_OVERRIDES[eid]

    fatigue = _EX_FATIGUE_BASE.get(fam, 3)
    impact = _EX_IMPACT_BASE.get(fam, 3)
    eccentric = _EX_ECCENTRIC_BASE.get(fam, 3)
    role = _EX_ROLE.get(fam, "strength")

    # Adjustments
    if diff >= 4:
        fatigue = min(fatigue + 1, 5)
        eccentric = min(eccentric + 1, 5)
    if explosive:
        impact = min(impact + 1, 5)
    if isometric:
        eccentric = 1
        fatigue = max(fatigue - 1, 1)

    # High-fatigue exercises
    if "barbell back squat" in name or "front squat" in name or "conventional deadlift" in name:
        fatigue = min(fatigue + 1, 5)
        if "conventional deadlift" in name:
            eccentric = min(eccentric + 1, 5)
        impact = min(impact + 1, 5)
    if "trap bar deadlift" in name:
        fatigue = min(fatigue + 1, 5)
    # High-eccentric exercises
    if "nordic" in name:
        eccentric = 5
        fatigue = 4
    if "depth jump" in name:
        impact = 5
        eccentric = 4
        fatigue = 4
    if "rdl" in name and fam == "DLHD":
        eccentric = 5
    if "good morning" in name:
        eccentric = 5
    if "stiff-leg" in name or "stiff leg" in name or "straight-leg" in name:
        eccentric = 5
    # Sprint-specific: full sprints are high impact
    if fam == "Sprint" and ("acceleration" in name or "flying" in name or "fall-in" in name or "resisted sprint" in name or "sled" in name or "fallin" in name):
        impact = min(impact + 2, 5)
    # Low-fatigue bodyweight/unloaded exercises
    if "air squat" in name or "wall push-up" in name or "wall drill" in name or "marching" in name:
        fatigue = max(fatigue - 1, 2)
    if "incline push-up" in name or "push-up" == name:
        fatigue = max(fatigue - 1, 2)
    # Loaded carries
    if "farmer" in name or "suitcase" in name or "waiter" in name or "front rack" in name:
        fatigue = 3

    return {
        "fatigue_cost": fatigue,
        "impact_level": impact,
        "eccentric_cost": eccentric,
        "competition_role": role,
    }


# ── Surface inference ─────────────────────────────────────────────

def _infer_surface(ed: dict) -> str:
    name = ed.get("name", "").lower()
    keywords = ["bosu", "balance pad", "unstable", "wobble", "dynadisc", "swiss ball", "stability ball"]
    if any(k in name for k in keywords):
        return "unstable"
    return "stable"


# ── Import exercise data ──────────────────────────────────────────
from .exercises_data import EXERCISES_DATA as _EXERCISES_RAW

EXERCISES: list[Exercise] = []
EXERCISE_BY_ID: dict[str, Exercise] = {}
EXERCISES_BY_FAMILY: dict[str, list[Exercise]] = {}

for ed in _EXERCISES_RAW:
    sec = ed["secondary_family"]
    comp = _infer_exercise_comp_metadata(ed)
    ex = Exercise(
        id=ed["id"],
        name=ed["name"],
        family=_fc(ed["family"]),
        secondary_family=_fc(sec) if sec else None,
        objective=_obj(ed["objective"]) if ed["objective"] in [e.value for e in Objective] else Objective.STRENGTH,
        difficulty=ed["difficulty"],
        equipment=ed["equipment"] if isinstance(ed["equipment"], list) else [ed["equipment"]],
        unilateral=ed["unilateral"],
        explosive=ed["explosive"],
        isometric=ed["isometric"],
        rotational=ed["rotational"],
        progression=ed.get("progression"),
        regression=ed.get("regression"),
        surface=_infer_surface(ed),
        fatigue_cost=comp["fatigue_cost"],
        impact_level=comp["impact_level"],
        eccentric_cost=comp["eccentric_cost"],
        competition_role=comp["competition_role"],
    )
    EXERCISES.append(ex)
    EXERCISE_BY_ID[ex.id] = ex
    fam = ex.family.value
    if fam not in EXERCISES_BY_FAMILY:
        EXERCISES_BY_FAMILY[fam] = []
    EXERCISES_BY_FAMILY[fam].append(ex)

# ── Exercise Families ──────────────────────────────────────────────
FAMILIES_DATA = [
    {"id": "DLKD", "name": "Double Leg Knee Dominant", "definition": "Bilateral squat-pattern exercises where knee flexion is the primary joint action.", "non_negotiable_in": "90% of programs", "default_slot": "mid"},
    {"id": "DLHD", "name": "Double Leg Hip Dominant", "definition": "Bilateral hinge-pattern exercises where hip flexion/extension is primary.", "non_negotiable_in": "75% of programs", "default_slot": "mid"},
    {"id": "SLKD", "name": "Single Leg Knee Dominant", "definition": "Unilateral squat/lunge-pattern exercises.", "non_negotiable_in": "70% of programs", "default_slot": "late"},
    {"id": "SLHD", "name": "Single Leg Hip Dominant", "definition": "Unilateral hinge-pattern exercises.", "non_negotiable_in": "25% of programs", "default_slot": "late"},
    {"id": "HPush", "name": "Horizontal Push", "definition": "Upper-body pressing where line of force is horizontal.", "non_negotiable_in": "80% of programs", "default_slot": "late"},
    {"id": "HPull", "name": "Horizontal Pull", "definition": "Upper-body pulling where line of force is horizontal.", "non_negotiable_in": "90% of programs", "default_slot": "late"},
    {"id": "VPush", "name": "Vertical Push", "definition": "Upper-body pressing where line of force is vertical.", "non_negotiable_in": "20% of programs", "default_slot": "late"},
    {"id": "VPull", "name": "Vertical Pull", "definition": "Upper-body pulling where line of force is vertical.", "non_negotiable_in": "55% of programs", "default_slot": "late"},
    {"id": "Plyo", "name": "Plyometric", "definition": "Fast, high-intensity bodyweight exercises using stretch-shorten cycle.", "non_negotiable_in": "85% of programs", "default_slot": "early"},
    {"id": "Ball", "name": "Ballistic", "definition": "Loaded explosive exercises where athlete accelerates load through full extension.", "non_negotiable_in": "85% of programs", "default_slot": "early"},
    {"id": "Sprint", "name": "Sprint / Change of Direction", "definition": "Locomotion-based speed, acceleration, deceleration, and reacceleration.", "non_negotiable_in": "65% of programs", "default_slot": "early"},
    {"id": "Rot", "name": "Rotational", "definition": "Transverse-plane rotation and anti-rotation loaded through the torso.", "non_negotiable_in": "45% of programs", "default_slot": "variable"},
    {"id": "Carry", "name": "Carry", "definition": "Loaded ambulation where athlete walks with external load.", "non_negotiable_in": "30% of programs", "default_slot": "late"},
    {"id": "Core", "name": "Core", "definition": "Trunk stabilisation including anti-extension, anti-rotation, anti-lateral flexion, and controlled flexion.", "non_negotiable_in": "100% of programs", "default_slot": "last"},
    {"id": "Landing", "name": "Landing Mechanics", "definition": "Progressive landing skill development from double-leg stick through single-leg reactive landings.", "non_negotiable_in": "60% of programs", "default_slot": "early"},
    {"id": "Acc", "name": "Accessory / Prehab", "definition": "Targeted isolation, prehabilitation, and injury prevention.", "non_negotiable_in": "Variable", "default_slot": "early"},
    {"id": "Agility", "name": "Agility", "definition": "Multi-directional footwork, reactive change of direction, and deceleration control.", "non_negotiable_in": "40% of programs", "default_slot": "early"},
    {"id": "Cond", "name": "Conditioning", "definition": "Metabolic conditioning and repeated-effort stamina work.", "non_negotiable_in": "25% of programs", "default_slot": "last"},
]

# Priority-ordered exercise IDs per family (from Rulebook Section 2.2)
SELECTION_PRIORITIES: dict[str, list[str]] = {
    "Acc": ["Acc-002", "Acc-015", "Acc-001", "Acc-005", "Acc-014", "Acc-021", "Acc-003", "Acc-004", "Acc-006", "Acc-007", "Acc-008", "Acc-009", "Acc-010", "Acc-011", "Acc-012", "Acc-013", "Acc-016", "Acc-017", "Acc-018", "Acc-019", "Acc-020", "Acc-022", "Acc-023", "Acc-024", "Acc-025", "Acc-026", "Acc-027", "Acc-028", "ACC-100", "ACC-101"],
    "Agility": ["AGI-100", "AGI-101", "AGI-102", "AGI-103", "AGI-104"],
    "Ball": ["Ball-001", "Ball-002", "Ball-003", "Ball-004", "Ball-005", "Ball-006", "Ball-007", "Ball-008", "Ball-009", "Ball-010", "Ball-011", "Ball-012", "Ball-013", "Ball-014"],
    "Carry": ["Carry-001", "Carry-012", "Carry-002", "Carry-013", "Carry-003", "Carry-004", "Carry-005", "Carry-006", "Carry-007", "Carry-008", "Carry-009", "Carry-010", "Carry-011", "Carry-014", "Carry-015", "Carry-016", "Carry-017"],
    "Core": ["Core-002", "Core-003", "Core-011", "Core-016", "Core-021", "Core-001", "Core-004", "Core-005", "Core-006", "Core-007", "Core-008", "Core-009", "Core-010", "Core-012", "Core-013", "Core-014", "Core-015", "Core-017", "Core-018", "Core-019", "Core-020"],
    "Cond": ["COND-100"],
    "DLHD": ["DLHD-006", "DLHD-012", "DLHD-011", "DLHD-009", "DLHD-014", "DLHD-002", "DLHD-003", "DLHD-007", "DLHD-001", "DLHD-004", "DLHD-005", "DLHD-008", "DLHD-010", "DLHD-013", "DLHD-015", "DLHD-016", "DLHD-017", "DLHD-100"],
    "DLKD": ["DLKD-004", "DLKD-007", "DLKD-010", "DLKD-011", "DLKD-003", "DLKD-006", "DLKD-009", "DLKD-012", "DLKD-001", "DLKD-002", "DLKD-005", "DLKD-008", "DLKD-013"],
    "HPull": ["HPull-005", "HPull-009", "HPull-011", "HPull-003", "HPull-004", "HPull-006", "HPull-007", "HPull-008", "HPull-001", "HPull-002", "HPull-010", "HPull-012"],
    "HPush": ["HPush-006", "HPush-005", "HPush-008", "HPush-003", "HPush-004", "HPush-007", "HPush-001", "HPush-002", "HPush-009", "HPush-010", "HPush-011"],
    "Plyo": ["Plyo-002", "Plyo-004", "Plyo-003", "Plyo-013", "Plyo-001", "Plyo-005", "Plyo-006", "Plyo-007", "Plyo-008", "Plyo-009", "Plyo-010", "Plyo-011", "Plyo-012", "Plyo-014", "Plyo-015", "Plyo-016", "PLYO-100", "PLYO-101", "PLYO-102"],
    "Rot": ["Rot-006", "Rot-010", "Rot-003", "Rot-005", "Rot-007", "Rot-001", "Rot-002", "Rot-004", "Rot-008", "Rot-009", "Rot-011", "Rot-012", "Rot-013", "Rot-014", "Rot-015", "Rot-016", "Rot-017", "ROT-100"],
    "SLHD": ["SLHD-005", "SLHD-008", "SLHD-009", "SLHD-002", "SLHD-003", "SLHD-006", "SLHD-001", "SLHD-004", "SLHD-007", "SLHD-010", "SLHD-011", "SLHD-012"],
    "SLKD": ["SLKD-005", "SLKD-008", "SLKD-012", "SLKD-002", "SLKD-003", "SLKD-006", "SLKD-007", "SLKD-009", "SLKD-010", "SLKD-011", "SLKD-001", "SLKD-004", "SLKD-013", "SLKD-100"],
    "Landing": ["Landing-001", "Landing-002", "Landing-003", "Landing-004", "Landing-005", "Landing-006", "Landing-007", "Landing-008", "LANDING-100"],
    "Sprint": ["Sprint-023", "Sprint-024", "Sprint-025", "Sprint-026", "Sprint-027", "Sprint-028", "Sprint-029", "Sprint-003", "Sprint-007", "Sprint-009", "Sprint-011", "Sprint-012", "Sprint-001", "Sprint-002", "Sprint-004", "Sprint-005", "Sprint-006", "Sprint-008", "Sprint-010", "Sprint-013", "Sprint-014", "Sprint-015", "Sprint-016", "Sprint-017", "Sprint-018", "Sprint-019", "Sprint-020", "Sprint-021", "Sprint-022", "SPRINT-100"],
    "VPull": ["VPull-005", "VPull-006", "VPull-009", "VPull-010", "VPull-012", "VPull-001", "VPull-002", "VPull-003", "VPull-004", "VPull-007", "VPull-008", "VPull-011", "VPull-013", "VPull-014"],
    "VPush": ["VPush-008", "VPush-006", "VPush-005", "VPush-009", "VPush-010", "VPush-002", "VPush-003", "VPush-004", "VPush-001", "VPush-007", "VPush-011", "VPush-012", "VPush-013", "VPush-014"],
}

FAMILIES: list[ExerciseFamily] = []
for fd in FAMILIES_DATA:
    fid = fd["id"]
    priorities = [(i + 1, eid, "") for i, eid in enumerate(SELECTION_PRIORITIES.get(fid, []))]
    FAMILIES.append(ExerciseFamily(
        id=_fc(fid),
        name=fd["name"],
        definition=fd["definition"],
        non_negotiable_in=fd["non_negotiable_in"],
        default_slot=fd["default_slot"],
        selection_priorities=priorities,
    ))

# ── Blueprints ─────────────────────────────────────────────────────
from .blueprint_data import BLUEPRINTS_DATA as _BP_RAW

_BP_MAP = {}
for bpd in _BP_RAW:
    # Expand "All" in optional_families to all families not in mandatory
    optional_families = []
    for f in bpd["optional_families"]:
        if f == "All":
            # Add all families not in mandatory
            mandatory_codes = set(bpd["mandatory_families"])
            all_codes = [fd["id"] for fd in FAMILIES_DATA]
            for code in all_codes:
                if code not in mandatory_codes and code not in optional_families:
                    optional_families.append(code)
        else:
            optional_families.append(f)

    _BP_MAP[bpd["id"]] = Blueprint(
        id=bpd["id"],
        name=BlueprintName(bpd["name"]),
        purpose=bpd["purpose"],
        typical_athlete=bpd["typical_athlete"],
        best_training_age=bpd["best_training_age"],
        best_season_phase=[SeasonPhase(sp) for sp in bpd["best_season_phase"]],
        contraindications=bpd.get("contraindications", ""),
        typical_outcomes=bpd.get("typical_outcomes", ""),
        progression_path=BlueprintName(bpd["progression_path"]) if bpd.get("progression_path") else None,
        regression_path=BlueprintName(bpd["regression_path"]) if bpd.get("regression_path") else None,
        mandatory_families=[_fc(f) for f in bpd["mandatory_families"] if f not in ("All",)],
        optional_families=[_fc(f) for f in optional_families],
        slot_order=[_fc(f) for f in bpd["slot_order"] if f not in ("All",)],
        min_session_composition=bpd.get("min_session_composition", []),
    )

BLUEPRINTS: list[Blueprint] = sorted(_BP_MAP.values(), key=lambda b: b.id)
BLUEPRINT_BY_ID: dict[int, Blueprint] = _BP_MAP

# ── Conditioning Protocols ─────────────────────────────────────────
from .conditioning_data import CONDITIONING_PROTOCOLS_DATA as _COND_RAW

CONDITIONING_PROTOCOLS: list[ConditioningProtocol] = []
COND_PROTOCOL_BY_ID: dict[str, ConditioningProtocol] = {}
COND_PROTOCOLS_BY_SYSTEM: dict[str, list[ConditioningProtocol]] = {}
COND_DECISION_MAP: dict = {}

def _compute_env_cat(pd: dict) -> str:
    """Compute environment_category from existing protocol fields."""
    if "environment_category" in pd:
        return pd["environment_category"]
    system = pd.get("system", "")
    envs = pd.get("environment", [])
    if system == "Recovery Conditioning":
        return "recovery"
    if envs == ["Pool"] or envs == ["Any"]:
        return "recovery"
    if "Gym" in envs and not any(e in envs for e in ["Field", "Track", "Court", "Turf", "Road", "Trail", "Grass", "Hill"]):
        return "gym"
    pid = pd["id"]
    if pid in ("AP-006", "AP-007", "RSA-009"):
        return "court"
    if "Court" in envs:
        return "court"
    return "field"


def _compute_sport_tags(pd: dict) -> list[str]:
    """Compute sport_tags from existing protocol fields."""
    if "sport_tags" in pd:
        return pd["sport_tags"]
    pid = pd["id"]
    system = pd.get("system", "")
    envs = pd.get("environment", [])
    tag_map = {
        "ET-006": ["cricket"],
        "ET-007": ["cricket"],
        "AP-006": ["tennis", "badminton", "basketball"],
        "AP-007": ["tennis", "badminton", "basketball"],
        "AP-008": ["soccer", "rugby"],
        "RSA-009": ["tennis", "badminton"],
        "RSA-005": ["cricket", "rugby", "soccer", "tennis", "badminton"],
        "RSA-008": ["cricket", "rugby", "soccer", "tennis", "badminton"],
        "RSA-011": ["cricket", "rugby", "soccer", "tennis", "badminton"],
        "PM-006": ["tennis", "badminton", "basketball", "cricket", "rugby", "soccer"],
        "CC-006": ["volleyball", "basketball"],
        "CC-007": ["tennis", "badminton", "volleyball", "squash"],
    }
    if pid in tag_map:
        return tag_map[pid]
    if system == "Recovery Conditioning":
        return ["any"]
    if envs == ["Pool"] or envs == ["Any"]:
        return ["any"]
    if "Gym" in envs and not any(e in envs for e in ["Field", "Track", "Court", "Turf", "Road", "Trail", "Grass"]):
        return ["any"]
    if pid.startswith("AC-") or pid.startswith("AS-") or pid.startswith("SE-"):
        return ["any"]
    if pid in ("PM-001", "PM-002", "PM-003", "PM-004", "PM-005"):
        return ["any"]
    return ["cricket", "rugby", "soccer", "hockey"]


def _compute_movement_profile(pd: dict, env_cat: str) -> str:
    """Infer movement_profile from protocol fields."""
    if "movement_profile" in pd:
        return pd["movement_profile"]
    pid = pd["id"]
    system = pd.get("system", "")
    name = pd.get("name", "").lower()

    if env_cat == "recovery":
        if "pool" in name or "aqua" in name:
            return "pool_recovery"
        if "mobility" in name or "stretch" in name or "circuit" in name:
            return "mobility_recovery"
        return "recovery_flush"

    if env_cat == "gym":
        if "bike" in pid or "bike" in name:
            return "bike_intervals"
        if "rower" in pid or "row" in name or "250m" in name:
            return "rower_intervals"
        if "treadmill" in name:
            return "treadmill_intervals"
        if "kettlebell" in name or "kb/" in name or "db circuit" in name or "kb/db" in name:
            return "mixed_modal_circuit"
        return "mixed_modal_circuit"

    if env_cat == "court":
        if pid.startswith("CC-"):
            if pid in ("CC-001", "CC-002", "CC-006"):
                return "court_rally_repeat"
            if pid == "CC-003":
                return "court_shuffle"
            if pid in ("CC-004", "CC-007"):
                return "court_diagonal"
            if pid == "CC-005":
                return "accel_decel"
        if pid == "AP-006" or pid == "AP-007":
            return "change_of_direction"
        if pid == "RSA-009" or pid == "RSA-005" or pid == "RSA-008" or pid == "RSA-011":
            return "accel_decel"
        if pid in ("AS-001", "AS-007"):
            return "accel_decel"
        if pid == "PM-006":
            return "change_of_direction"
        return "court_shuffle"

    # field environment
    if pid.startswith("AC-"):
        return "linear_tempo"
    if pid.startswith("ET-"):
        return "linear_tempo"
    if pid.startswith("IT-"):
        return "linear_tempo"
    if pid.startswith("SE-"):
        return "linear_speed_endurance"
    if pid.startswith("RSA-"):
        return "linear_rsa"
    if pid.startswith("AS-"):
        return "accel_decel"
    if pid.startswith("LT-"):
        return "linear_tempo"
    if pid.startswith("PM-"):
        if pid == "PM-006":
            return "change_of_direction"
        return "accel_decel"
    if pid.startswith("AP-"):
        if pid in ("AP-006", "AP-007", "AP-008"):
            return "change_of_direction"
        return "linear_tempo"
    if pid == "FC-001":
        return "accel_decel"
    return "linear_tempo"


def _compute_session_role(pd: dict, system: str, fatigue_score: int) -> str:
    """Infer session_role from protocol fields."""
    if "session_role" in pd:
        return pd["session_role"]
    if system == "Recovery Conditioning":
        return "recovery_flush"
    if system == "Power Maintenance":
        return "power_maintenance"
    if system == "Alactic Speed":
        return "speed_support"
    if system == "Speed Endurance":
        return "speed_support"
    if fatigue_score <= 2:
        return "top_up_conditioning"
    if fatigue_score >= 5:
        return "main_conditioning"
    pid = pd["id"]
    if pid.startswith("CC-") or pid.startswith("GC-"):
        return "main_conditioning"
    return "main_conditioning"


def _compute_impact_level(pd: dict, env_cat: str, system: str, fatigue_score: int) -> int:
    """Infer impact_level (1-5) from protocol fields."""
    if "impact_level" in pd:
        return pd["impact_level"]
    if env_cat == "recovery":
        return 1
    if env_cat == "gym":
        if "bike" in pd["id"] or "bike" in pd.get("name", "").lower():
            return 1
        if "rower" in pd["id"] or "row" in pd.get("name", "").lower():
            return 2
        if "treadmill" in pd.get("name", "").lower():
            return 3
        return 2
    if env_cat == "court":
        if "shuffle" in pd.get("name", "").lower():
            return 3
        return 4
    # field
    if system == "Alactic Speed" or system == "Speed Endurance":
        return 4
    if system == "Repeated Sprint Ability":
        return 4
    if fatigue_score >= 4:
        return 4
    if system == "Aerobic Capacity":
        return 3
    if system == "Extensive Tempo":
        return 3
    return 3


def _compute_eccentric_cost(pd: dict, env_cat: str, movement_profile: str) -> int:
    """Infer eccentric_cost (1-5) from protocol fields."""
    if "eccentric_cost" in pd:
        return pd["eccentric_cost"]
    if env_cat == "recovery":
        return 1
    if env_cat == "gym":
        if "bike" in movement_profile:
            return 1
        if "rower" in movement_profile:
            return 2
        return 2
    if env_cat == "court":
        if movement_profile in ("court_shuffle", "court_diagonal", "court_rally_repeat"):
            return 4
        if movement_profile == "accel_decel":
            return 3
        if movement_profile == "change_of_direction":
            return 3
        return 3
    # field
    if movement_profile in ("linear_speed_endurance", "linear_rsa"):
        return 3
    if movement_profile == "linear_tempo":
        if "tempo" in pd.get("name", "").lower() and "grass" in pd.get("name", "").lower():
            return 2
        return 3
    if movement_profile == "accel_decel":
        return 3
    if movement_profile == "change_of_direction":
        return 3
    return 3


for pd in _COND_RAW:
    _env_cat = _compute_env_cat(pd)
    _system = pd.get("system", "")
    _fatigue = pd.get("fatigue_score", 2)
    _movement = _compute_movement_profile(pd, _env_cat)
    proto = ConditioningProtocol(
        id=pd["id"],
        name=pd["name"],
        objective=pd["objective"],
        system=_system,
        level=pd.get("level", "All levels"),
        environment=pd.get("environment", ["Field"]),
        duration=pd.get("duration", "20-30 min"),
        work_description=pd.get("work_description", ""),
        rest=pd.get("rest", "None"),
        sets=pd.get("sets", "1"),
        total_volume=pd.get("total_volume", ""),
        fatigue_score=_fatigue,
        progression=pd.get("progression", ""),
        regression=pd.get("regression", ""),
        tier=pd.get("tier", "B"),
        work_rest_ratio=pd.get("work_rest_ratio"),
        environment_category=_env_cat,
        sport_tags=_compute_sport_tags(pd),
        movement_profile=_movement,
        session_role=_compute_session_role(pd, _system, _fatigue),
        fatigue_cost=_fatigue,
        impact_level=_compute_impact_level(pd, _env_cat, _system, _fatigue),
        eccentric_cost=_compute_eccentric_cost(pd, _env_cat, _movement),
    )
    CONDITIONING_PROTOCOLS.append(proto)
    COND_PROTOCOL_BY_ID[proto.id] = proto
    sys = proto.system
    if sys not in COND_PROTOCOLS_BY_SYSTEM:
        COND_PROTOCOLS_BY_SYSTEM[sys] = []
    COND_PROTOCOLS_BY_SYSTEM[sys].append(proto)

# ── Conditioning Decision Map ──────────────────────────────────────
try:
    from .conditioning_data import CONDITIONING_DECISION_MAP as _CDM
    COND_DECISION_MAP = _CDM
except ImportError:
    COND_DECISION_MAP = {}

# ── Cross-Family Substitution Map ──────────────────────────────────
CROSS_FAMILY_SUBSTITUTION: dict[str, str] = {
    "DLKD": "SLKD",
    "DLHD": "SLHD",
    "SLKD": "DLKD",
    "SLHD": "DLHD",
    "HPush": "VPush",
    "HPull": "VPull",
    "VPush": "HPush",
    "VPull": "HPull",
    "Plyo": "Ball",
    "Ball": "Plyo",
    "Sprint": "Plyo",
    "Rot": "Core",
    "Carry": "Core",
    "Core": "Carry",
}

# ── Intent categories for cross-family substitution ──────────────
INTENT_CATEGORIES: dict[str, list[str]] = {
    "lower_push": ["DLKD", "SLKD"],
    "lower_pull": ["DLHD", "SLHD"],
    "upper_push": ["HPush", "VPush"],
    "upper_pull": ["HPull", "VPull"],
    "explosive": ["Plyo", "Ball", "Sprint", "Landing", "Agility"],
    "core_stability": ["Core", "Rot"],
    "carry_load": ["Carry"],
    "accessory": ["Acc", "Cond"],
    "sport_tag": ["Volleyball", "Tennis", "Soccer", "Deceleration"],
}

FAMILY_TO_INTENT: dict[str, str] = {}
for intent, families in INTENT_CATEGORIES.items():
    for f in families:
        FAMILY_TO_INTENT[f] = intent

# ── Equipment profiles mapping ──────────────────────────────────────
EQUIPMENT_PROFILE_MAP: dict[str, list[str]] = {
    "Field Only": ["Bodyweight", "Band", "Med Ball", "Cones", "Hurdles", "Box"],
    "Basic Gym": ["Bodyweight", "Barbell", "DB", "KB", "Band", "Bench", "Box", "Pull-Up Bar", "Med Ball", "Rack"],
    "Commercial Gym": ["Bodyweight", "Barbell", "DB", "KB", "Band", "Bench", "Box", "Pull-Up Bar", "Med Ball", "Rack", "Cable Machine", "Machine"],
    "Elite Facility": ["Bodyweight", "Barbell", "DB", "KB", "Band", "Bench", "Box", "Pull-Up Bar", "Med Ball", "Rack", "Cable Machine", "Machine", "Sled", "Platform", "Trap Bar", "Rings", "GHD", "Specialty Bar"],
}

def get_max_difficulty(level: str) -> int:
    if level == "Beginner":
        return 2
    elif level == "Intermediate":
        return 3
    return 5

def get_equipment_for_profile(profile: str) -> list[str]:
    return EQUIPMENT_PROFILE_MAP.get(profile, ["Bodyweight"])

def get_exercises_by_family(family_code: str) -> list[Exercise]:
    return EXERCISES_BY_FAMILY.get(family_code, [])

def get_family_id_from_enum(family: FamilyCode) -> str:
    return family.value

def get_blueprint_by_id(bp_id: int) -> Blueprint:
    return BLUEPRINT_BY_ID[bp_id]
