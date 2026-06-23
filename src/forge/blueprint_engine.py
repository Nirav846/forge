"""Blueprint selection and slot resolution engines."""
from __future__ import annotations
from typing import Optional
from .models import (
    AthleteProfile, AthleteLevel, Blueprint, BlueprintName,
    FamilyCode, SeasonPhase, EquipmentProfile, BlockResponse
)
from .data import BLUEPRINTS, BLUEPRINT_BY_ID
from .block_autoregulation import get_next_block_blueprint_bias
from .prescription_rules import BLUEPRINT_CATEGORIES
from .session_rules import compute_family_survival_tier
from .session_assembly import (
    apply_time_constraint_v2,
    rebuild_session_flow,
    apply_competition_taper,
)
from .role_week_planning import RoleWeekProfile



def select_blueprint(athlete: AthleteProfile, block_response: Optional[BlockResponse] = None) -> Blueprint:
    # Handle special cases first (injury, return_to_sport) - these are not influenced by block response
    if athlete.injury_status == "active" or athlete.goal == "return_to_sport":
        return BLUEPRINT_BY_ID[12]

    # Determine block response to use: explicit argument, or from athlete, or None
    effective_block_response = block_response
    if effective_block_response is None and hasattr(athlete, 'block_response'):
        effective_block_response = athlete.block_response

    # Get candidate blueprints using the original logic (shortlist by season phase, then narrow by sport)
    bps = _shortlist_by_season_phase(athlete)
    if not bps:
        bps = [BLUEPRINT_BY_ID[1]]

    if len(bps) > 1:
        bps = _narrow_by_sport(athlete, bps)

    # If we have a block response and more than one candidate, apply bias to choose the best
    if effective_block_response is not None and len(bps) > 1:
        bias = get_next_block_blueprint_bias(athlete, effective_block_response)
        # Score each blueprint based on the bias
        scored = []
        for bp in bps:
            score = _score_blueprint_for_bias(bp, bias, athlete, effective_block_response)
            scored.append((score, bp))
        # Sort by score descending, then by original order (stable sort)
        scored.sort(key=lambda x: x[0], reverse=True)
        # Return the blueprint with the highest score
        return scored[0][1]
    else:
        # No bias or only one candidate: return the first (original behavior)
        return bps[0]


def _score_blueprint_for_bias(bp: Blueprint, bias: dict, athlete: AthleteProfile, block_response: BlockResponse) -> int:
    """Score a blueprint based on how well it matches the block response bias."""
    score = 0
    bp_id = bp.id
    bp_category = BLUEPRINT_CATEGORIES.get(bp_id, "strength_dominant")
    has_sprint_mandatory = FamilyCode.SPRINT in bp.mandatory_families

    # prefer_power_speed: favor power/speed oriented blueprints
    if bias.get("prefer_power_speed"):
        if bp_category in ("strength_power", "power_speed", "sprint_development"):
            score += 2

    # prefer_speed_power: favor speed/power oriented blueprints (similar to above)
    if bias.get("prefer_speed_power"):
        if bp_category in ("sprint_development", "power_speed", "strength_power"):
            score += 2

    # reduce_conditioning: avoid conditioning-heavy blueprints
    if bias.get("reduce_conditioning"):
        if bp_category in ("strength_conditioning", "gpp"):
            score -= 2

    # lower_fatigue: prefer lower fatigue blueprints (heuristic based on id)
    if bias.get("lower_fatigue"):
        if bp_id in (6, 7, 12, 13):  # Power Maintenance, Youth Foundation, Return to Sport, Deload
            score += 2

    # keep_sprint_emphasis: prefer blueprints that mandate sprint work
    if bias.get("keep_sprint_emphasis"):
        if has_sprint_mandatory:
            score += 2

    # add_conditioning_bias: favor conditioning emphasis
    if bias.get("add_conditioning_bias"):
        if bp_category in ("strength_conditioning", "gpp"):
            score += 2

    # maintain_same_blueprint: if we have a prior blueprint, prefer to stay the same or similar
    if bias.get("maintain_same_blueprint"):
        prior_bp_id = block_response.prior_blueprint_id
        if prior_bp_id.isdigit() and int(prior_bp_id) == bp_id:
            score += 3  # strong preference for same blueprint
        elif prior_bp_id.isdigit():
            # Optional: could add points for same category or regression/progression path
            prior_category = BLUEPRINT_CATEGORIES.get(int(prior_bp_id), "strength_dominant")
            if prior_category == bp_category:
                score += 1

    return score


def _shortlist_by_season_phase(athlete: AthleteProfile) -> list[Blueprint]:
    phase = athlete.season_phase
    effective_ta = _effective_training_age(athlete)

    if phase == SeasonPhase.OFF_SEASON:
        if effective_ta < 2:
            return [BLUEPRINT_BY_ID[7], BLUEPRINT_BY_ID[14]]
        if athlete.goal == "mass":
            return [BLUEPRINT_BY_ID[11]]
        if athlete.sport in ("rugby", "american_football", "rugby_union", "rugby_league"):
            return [BLUEPRINT_BY_ID[9]]
        if athlete.sport in ("tennis", "badminton", "basketball", "volleyball", "netball", "squash"):
            return [BLUEPRINT_BY_ID[8]]
        if athlete.goal == "speed":
            return [BLUEPRINT_BY_ID[2]]
        return [BLUEPRINT_BY_ID[1]]

    if phase == SeasonPhase.PRE_SEASON:
        if athlete.goal == "conditioning":
            return [BLUEPRINT_BY_ID[3]]
        if athlete.goal == "speed":
            return [BLUEPRINT_BY_ID[10]]
        if athlete.goal == "power_peak":
            return [BLUEPRINT_BY_ID[4]]
        return [BLUEPRINT_BY_ID[1]]

    if phase == SeasonPhase.IN_SEASON:
        if athlete.fatigue_level == "high":
            return [BLUEPRINT_BY_ID[13]]
        if athlete.goal == "power_maintenance":
            return [BLUEPRINT_BY_ID[6]]
        if effective_ta < 2:
            return [BLUEPRINT_BY_ID[7]]
        return [BLUEPRINT_BY_ID[1]]

    if phase == SeasonPhase.TRANSITION:
        if athlete.fatigue_level == "high":
            return [BLUEPRINT_BY_ID[13]]
        return [BLUEPRINT_BY_ID[1]]

    return [BLUEPRINT_BY_ID[1]]


def _narrow_by_sport(athlete: AthleteProfile, bps: list[Blueprint]) -> list[Blueprint]:
    contact_sports = ("rugby", "american_football", "rugby_union", "rugby_league")
    court_sports = ("tennis", "badminton", "basketball", "volleyball", "netball", "squash")

    for bp in bps:
        if athlete.sport in contact_sports and bp.name == BlueprintName.RUGBY_OFF_SEASON:
            return [bp]
        if athlete.sport in court_sports and bp.name == BlueprintName.COURT_SPORT_AD:
            return [bp]

    return [bps[0]]


def _effective_training_age(athlete: AthleteProfile) -> float:
    ta = athlete.training_age_years
    if athlete.age < 20:
        cap = max(0, (athlete.age - 14) * 0.5)
        ta = min(ta, cap)
    return ta


def determine_level(athlete: AthleteProfile) -> AthleteLevel:
    effective_ta = _effective_training_age(athlete)
    if effective_ta < 1 or athlete.technique_consistency < 0.8:
        return AthleteLevel.BEGINNER
    if 1 <= effective_ta < 3 and athlete.technique_consistency >= 0.8:
        return AthleteLevel.INTERMEDIATE
    if effective_ta >= 3 and athlete.technique_consistency >= 0.8:
        if not athlete.strength_base_met:
            return AthleteLevel.INTERMEDIATE
        return AthleteLevel.ADVANCED
    return AthleteLevel.BEGINNER


def resolve_slots(blueprint: Blueprint, athlete_level: AthleteLevel) -> list[FamilyCode]:
    slots = list(blueprint.mandatory_families)

    order_map = {fam.value: i for i, fam in enumerate(blueprint.slot_order)}
    optional_sorted = sorted(blueprint.optional_families,
                             key=lambda f: order_map.get(f.value, 999))

    for fam in optional_sorted:
        if len(slots) >= 8:
            break
        if fam not in slots:
            slots.append(fam)

    # Ensure Core is always included if it's in optional_families
    if FamilyCode.CORE in blueprint.optional_families and FamilyCode.CORE not in slots:
        slots.append(FamilyCode.CORE)

    sorted_slots = _sort_by_slot_order(slots, blueprint)
    sorted_slots = enforce_session_flow_rules(sorted_slots)
    return sorted_slots


def _sort_by_slot_order(slots: list[FamilyCode], blueprint: Blueprint) -> list[FamilyCode]:
    order_map = {fam.value: i for i, fam in enumerate(blueprint.slot_order)}
    return sorted(slots, key=lambda f: order_map.get(f.value, 999))


def enforce_session_flow_rules(slots: list[FamilyCode]) -> list[FamilyCode]:
    """Wave 9: Use full session flow ordering from session_assembly."""
    return rebuild_session_flow(slots, None)


def apply_time_constraint(slots: list[FamilyCode], available_minutes: int, preferred_families: int) -> list[FamilyCode]:
    """Wave 9: Deprecated — use apply_time_constraint_v2 which considers blueprint and tiers."""
    if available_minutes < 30:
        max_fams = min(4, preferred_families)
    elif available_minutes < 45:
        max_fams = min(5, preferred_families)
    elif available_minutes < 60:
        max_fams = min(7, preferred_families)
    else:
        max_fams = min(8, preferred_families)

    if len(slots) <= max_fams:
        return slots

    mandatory_fams = {"DLKD", "DLHD", "HPush", "HPull", "Core"}
    priority_fams = [f for f in slots if f.value in mandatory_fams]
    optional_fams = [f for f in slots if f.value not in mandatory_fams]

    result = priority_fams[:max_fams]
    remaining = max_fams - len(result)
    if remaining > 0:
        result.extend(optional_fams[:remaining])

    return result


def apply_time_constraint_with_blueprint(
    slots: list[FamilyCode],
    blueprint: Blueprint,
    available_minutes: int,
    preferred_families: int,
    comp_window: Optional[int] = None,
    role_profile: Optional[RoleWeekProfile] = None,
) -> tuple[list[FamilyCode], list[str]]:
    """Wave 9: Apply time constraint using survival tiers and blueprint awareness."""
    return apply_time_constraint_v2(
        slots, blueprint, available_minutes, preferred_families, comp_window, role_profile
    )


def _has_equip(equip_lower: set[str], name: str) -> bool:
    name_l = name.lower().replace("_", " ")
    for e in equip_lower:
        e_norm = e.replace("_", " ")
        if name_l == e_norm:
            return True
        if name_l == "dumbbell" and e_norm == "db":
            return True
        if name_l == "db" and e_norm == "dumbbell":
            return True
        if name_l in e_norm or e_norm in name_l:
            return True
    return False


def get_equipment_profile(available_equipment: set[str]) -> EquipmentProfile:
    equip_lower = {e.lower() for e in available_equipment}
    has_dumbbell = _has_equip(equip_lower, "dumbbell")
    has_barbell = _has_equip(equip_lower, "barbell")
    if not has_barbell and not has_dumbbell:
        return EquipmentProfile.FIELD_ONLY
    needed_elite = ("barbell", "rack", "dumbbell", "cable", "sled", "specialty_bar")
    needed_commercial = ("barbell", "rack", "bench", "dumbbell", "cable")
    if all(_has_equip(equip_lower, e) for e in needed_elite):
        return EquipmentProfile.ELITE_FACILITY
    if all(_has_equip(equip_lower, e) for e in needed_commercial):
        return EquipmentProfile.COMMERCIAL_GYM
    return EquipmentProfile.BASIC_GYM
