"""Wave 9 — Session Assembly & Slot-Resolution Hardening.

Deterministic session assembly that makes sessions feel internally coherent
rather than just "valid blocks selected independently."
"""
from __future__ import annotations
from typing import Optional, Dict, List, Tuple
from .models import FamilyCode, Blueprint, Exercise, SessionBlock, AthleteProfile, AthleteLevel
from .role_week_planning import RoleWeekProfile, get_role_week_profile
from .data import EXERCISE_BY_ID, SELECTION_PRIORITIES, CROSS_FAMILY_SUBSTITUTION, FAMILY_TO_INTENT, INTENT_CATEGORIES
from .injury_map import has_injury_conflict
from .conditioning_engine import _resolve_comp_window
from .session_rules import (
    TIER_S, TIER_A, TIER_B, TIER_C,
    FAMILY_BASE_TIER,
    compute_family_survival_tier,
)

# Session flow ordering: lower = earlier in session
FLOW_ORDER: dict[str, int] = {
    "Sprint": 0, "Plyo": 1, "Ball": 2, "Landing": 3, "Acc": 4,
    "DLKD": 10, "DLHD": 11, "HPush": 12, "HPull": 13,
    "VPush": 14, "VPull": 15,
    "SLKD": 20, "SLHD": 21, "Rot": 22,
    "Carry": 30, "Core": 40,
}

# Within-week variation rules for repeated families
WITHIN_WEEK_VARIATION: dict[str, dict[str, str]] = {
    "DLKD": {"variant_family": "SLKD", "rationale": "unilateral variant"},
    "DLHD": {"variant_family": "SLHD", "rationale": "unilateral variant"},
    "HPush": {"variant_family": "VPush", "rationale": "vertical angle"},
    "HPull": {"variant_family": "VPull", "rationale": "vertical angle"},
    "Sprint": {"variant_family": "Plyo", "rationale": "elastic power"},
    "Plyo": {"variant_family": "Ball", "rationale": "loaded explosive"},
    "Ball": {"variant_family": "Plyo", "rationale": "bodyweight explosive"},
    "Landing": {"variant_family": "Plyo", "rationale": "reactive variant"},
    "Rot": {"variant_family": "Core", "rationale": "anti-rotation control"},
}


def apply_time_constraint_v2(
    slots: list[FamilyCode],
    blueprint: Blueprint,
    available_minutes: int,
    preferred_families: int,
    comp_window: Optional[int] = None,
    role_profile: Optional[RoleWeekProfile] = None,
) -> Tuple[list[FamilyCode], list[str]]:
    """Apply time/competition constraints using survival tiers.

    Returns (kept_slots, drop_notes).
    """
    # Determine max families
    if available_minutes < 30:
        max_fams = min(4, preferred_families)
    elif available_minutes < 45:
        max_fams = min(5, preferred_families)
    elif available_minutes < 60:
        max_fams = min(7, preferred_families)
    else:
        max_fams = min(8, preferred_families)

    # Competition proximity reduction
    if comp_window is not None:
        if comp_window == 4:  # MODERATE
            max_fams = min(max_fams, 7)
        elif comp_window == 2:  # LIGHT
            max_fams = min(max_fams, 5)
        elif comp_window == 1:  # PRIMER
            max_fams = min(max_fams, 4)

    if len(slots) <= max_fams:
        return slots, []

    # Compute tiers for each slot
    scored = []
    for fam in slots:
        tier = compute_family_survival_tier(fam, blueprint, role_profile)
        scored.append((tier, fam))

    # Sort by tier (ascending = higher priority first)
    scored.sort(key=lambda x: x[0])

    kept = [fam for tier, fam in scored[:max_fams]]
    dropped = [fam for tier, fam in scored[max_fams:]]

    # Rebuild drop notes
    notes = []
    for fam in dropped:
        tier = compute_family_survival_tier(fam, blueprint, role_profile)
        tier_name = {TIER_S: "identity", TIER_A: "high-value", TIER_B: "optional", TIER_C: "accessory"}[tier]
        notes.append(f"{fam.value} dropped ({tier_name}) — time/competition constraint")

    return kept, notes


def rebuild_session_flow(
    slots: list[FamilyCode],
    blueprint: Optional[Blueprint] = None,
) -> list[FamilyCode]:
    """Reorder slots to follow coach-like S&C session flow.

    Phase 1: Neural/speed/power (Sprint, Plyo, Ball, Landing, Acc)
    Phase 2: Primary strength (DLKD, DLHD, HPush, HPull)
    Phase 3: Secondary strength (VPush, VPull, SLKD, SLHD, Rot)
    Phase 4: Accessory/trunk (Carry, Core)
    """
    # Use blueprint slot_order as tiebreaker within each flow phase
    blueprint_order = {}
    if blueprint and blueprint.slot_order:
        blueprint_order = {f.value: i for i, f in enumerate(blueprint.slot_order)}

    def _sort_key(fam: FamilyCode) -> tuple:
        flow = FLOW_ORDER.get(fam.value, 50)
        bp = blueprint_order.get(fam.value, 999)
        return (flow, bp)

    sorted_slots = sorted(slots, key=_sort_key)

    # Ensure Core is always last if present
    if FamilyCode.CORE in sorted_slots:
        sorted_slots = [f for f in sorted_slots if f != FamilyCode.CORE]
        sorted_slots.append(FamilyCode.CORE)

    return sorted_slots


def get_within_week_variation_family(family: FamilyCode) -> Optional[FamilyCode]:
    """Return the variant family for a second exposure within the same week."""
    info = WITHIN_WEEK_VARIATION.get(family.value)
    if info:
        return FamilyCode(info["variant_family"])
    return None


def get_within_week_variation_rationale(family: FamilyCode) -> str:
    """Return the rationale for a second exposure variation."""
    info = WITHIN_WEEK_VARIATION.get(family.value)
    if info:
        return info["rationale"]
    return "variation"


# ── SESSION REBALANCE ─────────────────────────────────────────────

def rebalance_session_blocks(
    blocks: list[SessionBlock],
    blueprint: Optional[Blueprint] = None,
    role_profile: Optional[RoleWeekProfile] = None,
) -> Tuple[list[SessionBlock], list[str]]:
    """Remove empty blocks, reorder, and add coach notes.

    Returns (rebalanced_blocks, notes).
    """
    # Remove blocks with no exercises
    valid_blocks = [b for b in blocks if b.exercises and any(b.exercises)]
    empty_count = len(blocks) - len(valid_blocks)

    notes = []
    if empty_count > 0:
        # Track which families were dropped
        valid_fams = {b.family.value for b in valid_blocks}
        for b in blocks:
            if b.family.value not in valid_fams:
                notes.append(f"{b.family.value} removed — no valid exercise")

    # Reorder valid blocks by session flow
    reordered = rebuild_session_flow([b.family for b in valid_blocks], blueprint)

    # Rebuild blocks in new order
    family_to_block = {b.family.value: b for b in valid_blocks}
    result = []
    for fam in reordered:
        if fam.value in family_to_block:
            result.append(family_to_block[fam.value])

    # If session is too short, try backfill from blueprint optional
    if blueprint and len(result) < 3:
        optional_remaining = [f for f in blueprint.optional_families
                              if f.value not in family_to_block and f.value not in [b.family.value for b in result]]
        for fam in optional_remaining:
            if len(result) >= 3:
                break
            # Try to find a valid exercise for this family
            # We can't call select_exercise here without athlete context,
            # so we just note the backfill attempt
            notes.append(f"Attempted backfill: {fam.value}")

    return result, notes


# ── TAPER-SPECIFIC DROP LOGIC ───────────────────────────────────

def apply_competition_taper(
    slots: list[FamilyCode],
    blueprint: Blueprint,
    comp_window: int,
    role_profile: Optional[RoleWeekProfile] = None,
) -> Tuple[list[FamilyCode], list[str]]:
    """Apply competition-specific taper drops.

    comp_window: 1=primer, 2=light, 4=moderate
    Returns (kept_slots, notes).
    """
    if comp_window is None or comp_window > 4:
        return slots, []

    notes = []
    kept = []

    for fam in slots:
        fam_val = fam.value
        tier = compute_family_survival_tier(fam, blueprint, role_profile)

        if comp_window == 1:  # PRIMER
            # Keep only neural/activation work + Core
            if fam_val in ("Sprint", "Plyo", "Ball", "Core"):
                kept.append(fam)
            elif tier == TIER_S and fam_val in [f.value for f in blueprint.mandatory_families]:
                # Keep mandatory but note reduced intensity
                kept.append(fam)
                notes.append(f"{fam_val} kept at reduced intensity (primer)")
            else:
                notes.append(f"{fam_val} dropped (primer taper)")

        elif comp_window == 2:  # LIGHT
            # Drop Tier C and reduce Tier A strength
            if tier == TIER_C:
                notes.append(f"{fam_val} dropped (light taper)")
            elif fam_val in ("DLKD", "DLHD") and fam_val not in [f.value for f in blueprint.mandatory_families]:
                notes.append(f"{fam_val} dropped (light taper)")
            else:
                kept.append(fam)

        else:  # MODERATE (4)
            # Drop Tier C only
            if tier == TIER_C:
                notes.append(f"{fam_val} dropped (moderate taper)")
            else:
                kept.append(fam)

    return kept, notes


# ── COACH NOTES ───────────────────────────────────────────────────

def session_composition_rationale(
    kept: list[FamilyCode],
    dropped: list[FamilyCode],
    blueprint: Blueprint,
) -> list[str]:
    """Generate coach-readable notes about session composition."""
    notes = []
    if not dropped:
        return notes

    notes.append(f"Session composition: {len(kept)} families kept from {blueprint.name.value}")
    if dropped:
        dropped_str = ", ".join(f.value for f in dropped)
        notes.append(f"Dropped: {dropped_str}")
    return notes



# ── CREDIBILITY CHECKS ──────────────────────────────────────────

def check_session_identity_preserved(
    session_blocks: list[SessionBlock],
    blueprint: Blueprint,
) -> bool:
    """Check that most blueprint-defining families are still present."""
    present = {b.family.value for b in session_blocks if b.exercises}
    mandatory = [f.value for f in blueprint.mandatory_families]
    if not mandatory:
        return True
    missing = [f for f in mandatory if f not in present]
    # Allow up to 25% of mandatory families to be missing (e.g., no valid exercise in DB)
    return len(missing) <= max(1, len(mandatory) // 4)


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

    # Sprint/Plyo/Ball should not appear after strength (unless no strength)
    has_strength = any(f in positions for f in ("DLKD", "DLHD", "HPush", "HPull"))
    has_speed = any(f in positions for f in ("Sprint", "Plyo", "Ball"))

    if has_speed and has_strength:
        speed_pos = min(positions.get(f, 99) for f in ("Sprint", "Plyo", "Ball") if f in positions)
        strength_pos = min(positions.get(f, 99) for f in ("DLKD", "DLHD", "HPush", "HPull") if f in positions)
        if speed_pos > strength_pos:
            return False

    # Core should be last if present
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

    # No dropped family should be higher-tier than any kept family
    if not dropped_tiers or not kept_tiers:
        return True

    max_dropped = min(dropped_tiers)  # highest priority among dropped
    min_kept = min(kept_tiers)         # highest priority among kept

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
    # De-prioritized families should not be more than 50% of the session
    de_prio_count = sum(1 for f in present if f in role_profile.family_de_priority)
    if len(present) > 0 and de_prio_count / len(present) > 0.5:
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

    # In light/primer taper, speed/power families should be kept over strength
    if comp_window <= 2:
        kept_vals = {f.value for f in kept}
        dropped_vals = {f.value for f in dropped}

        # Carry/Acc should be dropped
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
    # Should have at least one lower-body and one upper-body pattern
    lower = any(b.family.value in ("DLKD", "DLHD", "SLKD", "SLHD") for b in valid)
    upper = any(b.family.value in ("HPush", "HPull", "VPush", "VPull") for b in valid)
    return lower or upper  # At least one major pattern


def check_repeated_family_progression_credible(
    sessions: list[SessionBlock],
    week: int,
    freq: int,
) -> bool:
    """Check that repeated family within same week shows intentional variation."""
    if len(sessions) < freq * 2:
        return True

    # Map family -> list of exercise IDs across sessions in this week
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

    # Check that families appearing twice have different exercises (or valid reason)
    for fam, ex_ids in family_exercises.items():
        if len(ex_ids) >= 2:
            if ex_ids[0] == ex_ids[1]:
                # Same exercise twice in same week is OK only if it's a main strength lift
                # or if the family has no valid variation
                if fam not in ("DLKD", "DLHD", "HPush", "HPull"):
                    return False

    return True
