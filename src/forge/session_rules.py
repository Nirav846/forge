"""Shared session/rule helpers used by session_assembly and progression_engine.

Pure validation/comparison/helper functions with no assembly or progression logic.
"""
from __future__ import annotations
from typing import Optional
from .models import FamilyCode, Blueprint, SessionBlock
from .role_week_planning import RoleWeekProfile

# ── TIER DEFINITIONS ──────────────────────────────────────────────

TIER_S = 0   # Session identity
TIER_A = 1   # High-value support
TIER_B = 2   # Optional support
TIER_C = 3   # First drop

FAMILY_BASE_TIER: dict[str, int] = {
    "DLKD": TIER_A, "DLHD": TIER_A,
    "HPush": TIER_A, "HPull": TIER_A,
    "Sprint": TIER_A, "Plyo": TIER_A, "Ball": TIER_A, "Landing": TIER_A,
    "SLKD": TIER_B, "SLHD": TIER_B,
    "VPush": TIER_B, "VPull": TIER_B,
    "Rot": TIER_B,
    "Carry": TIER_C, "Acc": TIER_C,
    "Core": TIER_S,
}


def compute_family_survival_tier(
    family: FamilyCode,
    blueprint: Blueprint,
    role_profile: Optional[RoleWeekProfile] = None,
) -> int:
    """Return the survival tier for a family in a session."""
    fam_val = family.value

    if fam_val in [f.value for f in blueprint.mandatory_families]:
        return TIER_S
    if fam_val == "Core":
        return TIER_S

    tier = FAMILY_BASE_TIER.get(fam_val, TIER_B)

    if role_profile and role_profile.family_de_priority:
        if fam_val in role_profile.family_de_priority:
            tier = min(tier + 1, TIER_C)

    if role_profile and role_profile.family_priority:
        if fam_val in role_profile.family_priority:
            tier = max(tier - 1, TIER_A)

    return tier


# ── CREDIBILITY CHECKS ──────────────────────────────────────────

def check_session_identity_preserved(
    session_blocks: list[SessionBlock],
    blueprint: Blueprint,
) -> bool:
    """Check that blueprint-defining families are still present."""
    present = {b.family.value for b in session_blocks if b.exercises}
    for mf in blueprint.mandatory_families:
        if mf.value not in present:
            return False
    return True


def check_session_flow_credible(
    session_blocks: list[SessionBlock],
) -> bool:
    """Check that session order follows credible S&C flow."""
    if not session_blocks:
        return True

    positions = {}
    for i, b in enumerate(session_blocks):
        if b.exercises:
            positions[b.family.value] = i

    has_strength = any(f in positions for f in ("DLKD", "DLHD", "HPush", "HPull"))
    has_speed = any(f in positions for f in ("Sprint", "Plyo", "Ball"))

    if has_speed and has_strength:
        speed_pos = min(positions.get(f, 99) for f in ("Sprint", "Plyo", "Ball") if f in positions)
        strength_pos = min(positions.get(f, 99) for f in ("DLKD", "DLHD", "HPush", "HPull") if f in positions)
        if speed_pos > strength_pos:
            return False

    if "Core" in positions:
        core_pos = positions["Core"]
        last_pos = max(positions.values())
        if core_pos != last_pos:
            return False

    return True


def check_high_value_families_not_dropped_before_low_value(
    kept: list[FamilyCode],
    dropped: list[FamilyCode],
    blueprint: Blueprint,
    role_profile: Optional[RoleWeekProfile] = None,
) -> bool:
    """Check that no high-value family was dropped while a low-value family survived."""
    kept_tiers = {compute_family_survival_tier(f, blueprint, role_profile) for f in kept}
    dropped_tiers = {compute_family_survival_tier(f, blueprint, role_profile) for f in dropped}

    if not dropped_tiers or not kept_tiers:
        return True

    max_dropped = min(dropped_tiers)
    min_kept = min(kept_tiers)

    return max_dropped >= min_kept


def check_role_bias_not_overriding_blueprint(
    session_blocks: list[SessionBlock],
    blueprint: Blueprint,
    role_profile: Optional[RoleWeekProfile] = None,
) -> bool:
    """Check that role bias did not destroy blueprint identity."""
    if not role_profile or not role_profile.family_de_priority:
        return True

    present = {b.family.value for b in session_blocks if b.exercises}
    mandatory = {f.value for f in blueprint.mandatory_families}

    if not mandatory.issubset(present):
        return False

    de_prio_count = sum(1 for f in present if f in role_profile.family_de_priority)
    if len(present) > 0 and de_prio_count / len(present) > 0.3:
        return False

    return True


def check_taper_drop_logic_credible(
    kept: list[FamilyCode],
    dropped: list[FamilyCode],
    comp_window: Optional[int],
    blueprint: Blueprint,
    role_profile: Optional[RoleWeekProfile] = None,
) -> bool:
    """Check that competition taper dropped fatigue-heavy extras first."""
    if comp_window is None or comp_window > 4:
        return True

    if comp_window <= 2:
        kept_vals = {f.value for f in kept}
        dropped_vals = {f.value for f in dropped}

        for acc_fam in ("Carry", "Acc"):
            if acc_fam in kept_vals:
                return False

    return True


def check_post_filter_session_balance(
    session_blocks: list[SessionBlock],
) -> bool:
    """Check that after filtering, session still has coherent structure."""
    valid = [b for b in session_blocks if b.exercises and any(b.exercises)]
    if len(valid) < 3:
        return False
    lower = any(b.family.value in ("DLKD", "DLHD", "SLKD", "SLHD") for b in valid)
    upper = any(b.family.value in ("HPush", "HPull", "VPush", "VPull") for b in valid)
    return lower or upper


def check_repeated_family_progression_credible(
    sessions: list[SessionBlock],
    week: int,
    freq: int,
) -> bool:
    """Check that repeated family within same week shows intentional variation."""
    if len(sessions) < freq * 2:
        return True

    week_start = (week - 1) * freq
    week_sessions = sessions[week_start:week_start + freq]
    family_exercises: dict[str, list[str]] = {}

    for session in week_sessions:
        for block in session.blocks:
            if block.exercises and block.exercises[0]:
                fam = block.family.value
                ex_id = block.exercises[0].id
                if fam not in family_exercises:
                    family_exercises[fam] = []
                family_exercises[fam].append(ex_id)

    for fam, ex_ids in family_exercises.items():
        if len(ex_ids) >= 2:
            if ex_ids[0] == ex_ids[1]:
                if fam not in ("DLKD", "DLHD", "HPush", "HPull"):
                    return False

    return True
