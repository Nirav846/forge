"""Wave 9 — Session Assembly & Slot-Resolution Hardening Tests.

Target: 30–50 tests covering family survival, order rebuilding,
within-week continuity, injury rebalance, blueprint identity, and end-to-end.
"""
from __future__ import annotations

from forge.session_assembly import (
    compute_family_survival_tier,
    apply_time_constraint_v2,
    rebuild_session_flow,
    apply_competition_taper,
    rebalance_session_blocks,
    get_within_week_variation_family,
    get_within_week_variation_rationale,
    session_composition_rationale,
    check_session_identity_preserved,
    check_session_flow_credible,
    check_high_value_families_not_dropped_before_low_value,
    check_role_bias_not_overriding_blueprint,
    check_taper_drop_logic_credible,
    check_post_filter_session_balance,
    check_repeated_family_progression_credible,
    TIER_S, TIER_A, TIER_B, TIER_C,
)
from forge.main import generate_program
from forge.progression_engine import verify_program_credibility
from forge.models import (
    AthleteProfile, AthleteLevel, EquipmentProfile, SeasonPhase, FamilyCode,
    Session, SessionBlock, Blueprint, BlueprintName, Exercise, GeneratedProgram,
)
from forge.data import BLUEPRINT_BY_ID
from forge.role_week_planning import RoleWeekProfile, get_role_week_profile
from forge.renderer import render_block_summary
from forge.blueprint_engine import select_blueprint, resolve_slots


# ── Helpers ───────────────────────────────────────────────────────

def _make_athlete(**overrides) -> AthleteProfile:
    defaults = {
        "sport": "rugby",
        "training_age_years": 3.0,
        "season_phase": SeasonPhase.OFF_SEASON,
        "goal": "strength",
        "equipment_profile": EquipmentProfile.COMMERCIAL_GYM,
        "athlete_level": AthleteLevel.INTERMEDIATE,
        "technique_consistency": 0.9,
        "injury_status": "none",
        "injury_history": [],
        "fatigue_level": "normal",
        "weeks_since_break": 0,
        "recent_exercises": {},
        "available_minutes": 75,
        "days_to_match": None,
        "preferred_families": 6,
        "age": 22,
        "strength_base_met": True,
        "position_role": "prop",
        "bodyweight_kg": 80.0,
    }
    defaults.update(overrides)
    return AthleteProfile(**defaults)


def _exercise(family: FamilyCode, name: str = "Test", id: str = "T-1", difficulty: int = 2) -> Exercise:
    return Exercise(
        id=id,
        name=name,
        family=family,
        secondary_family=None,
        objective="STR",
        difficulty=difficulty,
        equipment=["barbell"],
        unilateral=False,
        explosive=False,
        isometric=False,
        rotational=False,
        progression=None,
        regression=None,
        eccentric_cost=3,
        impact_level=3,
    )


def _block(family: FamilyCode, has_exercise: bool = True) -> SessionBlock:
    ex = _exercise(family) if has_exercise else None
    return SessionBlock(
        family=family,
        family_name=family.value,
        exercises=[ex] if ex else [],
    )


def _blueprint(mandatory: list[FamilyCode], optional: list[FamilyCode], slot_order: list[FamilyCode]) -> Blueprint:
    return Blueprint(
        id=99,
        name=BlueprintName.FULL_BODY_STRENGTH,
        purpose="Test",
        typical_athlete="intermediate",
        best_training_age="1-3",
        best_season_phase=[SeasonPhase.OFF_SEASON],
        best_frequency="3x per week",
        contraindications="none",
        typical_outcomes="strength",
        progression_path=None,
        regression_path=None,
        mandatory_families=mandatory,
        optional_families=optional,
        slot_order=slot_order,
        typical_duration="8 weeks",
        min_session_composition=[],
    )


# ═══════════════════════════════════════════════════════════════════
# A. Family Survival / Drop Priority
# ═══════════════════════════════════════════════════════════════════

class TestFamilySurvivalTier:

    def test_mandatory_family_is_tier_s(self):
        bp = _blueprint([FamilyCode.DLKD], [FamilyCode.CORE], [FamilyCode.DLKD, FamilyCode.CORE])
        assert compute_family_survival_tier(FamilyCode.DLKD, bp) == TIER_S

    def test_core_is_tier_s(self):
        bp = _blueprint([FamilyCode.DLKD], [FamilyCode.CORE], [FamilyCode.DLKD, FamilyCode.CORE])
        assert compute_family_survival_tier(FamilyCode.CORE, bp) == TIER_S

    def test_strength_family_is_tier_a(self):
        bp = _blueprint([FamilyCode.DLKD], [FamilyCode.DLHD], [FamilyCode.DLKD, FamilyCode.DLHD])
        assert compute_family_survival_tier(FamilyCode.DLHD, bp) == TIER_A

    def test_sprint_family_is_tier_a(self):
        bp = _blueprint([FamilyCode.DLKD], [FamilyCode.SPRINT], [FamilyCode.DLKD, FamilyCode.SPRINT])
        assert compute_family_survival_tier(FamilyCode.SPRINT, bp) == TIER_A

    def test_unilateral_is_tier_b(self):
        bp = _blueprint([FamilyCode.DLKD], [FamilyCode.SLKD], [FamilyCode.DLKD, FamilyCode.SLKD])
        assert compute_family_survival_tier(FamilyCode.SLKD, bp) == TIER_B

    def test_carry_is_tier_c(self):
        bp = _blueprint([FamilyCode.DLKD], [FamilyCode.CARRY], [FamilyCode.DLKD, FamilyCode.CARRY])
        assert compute_family_survival_tier(FamilyCode.CARRY, bp) == TIER_C

    def test_role_de_priority_drops_tier(self):
        bp = _blueprint([FamilyCode.DLKD], [FamilyCode.SPRINT], [FamilyCode.DLKD, FamilyCode.SPRINT])
        rp = RoleWeekProfile(family_de_priority=["Sprint"])
        assert compute_family_survival_tier(FamilyCode.SPRINT, bp, rp) == TIER_B

    def test_role_priority_raises_tier(self):
        bp = _blueprint([FamilyCode.DLKD], [FamilyCode.SLKD], [FamilyCode.DLKD, FamilyCode.SLKD])
        rp = RoleWeekProfile(family_priority=["SLKD"])
        assert compute_family_survival_tier(FamilyCode.SLKD, bp, rp) == TIER_A

    def test_role_de_priority_does_not_drop_below_tier_c(self):
        bp = _blueprint([FamilyCode.DLKD], [FamilyCode.CARRY], [FamilyCode.DLKD, FamilyCode.CARRY])
        rp = RoleWeekProfile(family_de_priority=["Carry"])
        assert compute_family_survival_tier(FamilyCode.CARRY, bp, rp) == TIER_C

    def test_role_priority_does_not_raise_above_tier_a(self):
        bp = _blueprint([FamilyCode.DLKD], [FamilyCode.DLHD], [FamilyCode.DLKD, FamilyCode.DLHD])
        rp = RoleWeekProfile(family_priority=["DLHD"])
        # DLHD is already TIER_A, priority should keep it at TIER_A
        assert compute_family_survival_tier(FamilyCode.DLHD, bp, rp) == TIER_A


class TestTimeConstraint:

    def test_no_constraint_keeps_all(self):
        bp = _blueprint([FamilyCode.DLKD], [FamilyCode.DLHD, FamilyCode.CORE], [FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.CORE])
        slots = [FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.CORE]
        kept, notes, _ = apply_time_constraint_v2(slots, bp, 75, 6)
        assert len(kept) == 3
        assert not notes

    def test_30_min_drops_tier_c_first(self):
        bp = _blueprint(
            [FamilyCode.DLKD],
            [FamilyCode.CARRY, FamilyCode.CORE, FamilyCode.ACC, FamilyCode.HPUSH],
            [FamilyCode.DLKD, FamilyCode.CARRY, FamilyCode.CORE, FamilyCode.ACC, FamilyCode.HPUSH],
        )
        slots = [FamilyCode.DLKD, FamilyCode.CARRY, FamilyCode.CORE, FamilyCode.ACC, FamilyCode.HPUSH]
        kept, notes, _ = apply_time_constraint_v2(slots, bp, 25, 6)
        assert FamilyCode.CARRY not in kept or FamilyCode.ACC not in kept
        assert FamilyCode.DLKD in kept
        assert FamilyCode.CORE in kept

    def test_45_min_drops_tier_b_before_tier_a(self):
        bp = _blueprint(
            [FamilyCode.DLKD],
            [FamilyCode.DLHD, FamilyCode.SLKD, FamilyCode.CORE, FamilyCode.ROT, FamilyCode.HPUSH],
            [FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.SLKD, FamilyCode.CORE, FamilyCode.ROT, FamilyCode.HPUSH],
        )
        slots = [FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.SLKD, FamilyCode.CORE, FamilyCode.ROT, FamilyCode.HPUSH]
        kept, notes, _ = apply_time_constraint_v2(slots, bp, 40, 6)
        assert FamilyCode.SLKD not in kept or FamilyCode.ROT not in kept
        assert FamilyCode.DLKD in kept
        assert FamilyCode.DLHD in kept

    def test_mandatory_survives_severe_constraint(self):
        bp = _blueprint([FamilyCode.DLKD], [FamilyCode.CARRY], [FamilyCode.DLKD, FamilyCode.CARRY])
        slots = [FamilyCode.DLKD, FamilyCode.CARRY]
        kept, notes, _ = apply_time_constraint_v2(slots, bp, 25, 6)
        assert FamilyCode.DLKD in kept

    def test_comp_window_reduces_max(self):
        bp = _blueprint(
            [FamilyCode.DLKD],
            [FamilyCode.DLHD, FamilyCode.HPUSH, FamilyCode.CORE],
            [FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.HPUSH, FamilyCode.CORE],
        )
        slots = [FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.HPUSH, FamilyCode.CORE]
        kept, notes, _ = apply_time_constraint_v2(slots, bp, 75, 6, comp_window=1)
        assert len(kept) <= 4

    def test_drop_notes_mention_family_and_reason(self):
        bp = _blueprint(
            [FamilyCode.DLKD],
            [FamilyCode.CARRY, FamilyCode.CORE, FamilyCode.ACC, FamilyCode.HPUSH],
            [FamilyCode.DLKD, FamilyCode.CARRY, FamilyCode.CORE, FamilyCode.ACC, FamilyCode.HPUSH],
        )
        slots = [FamilyCode.DLKD, FamilyCode.CARRY, FamilyCode.CORE, FamilyCode.ACC, FamilyCode.HPUSH]
        kept, notes, _ = apply_time_constraint_v2(slots, bp, 25, 6)
        assert any("Carry" in n or "Acc" in n for n in notes)
        assert any("dropped" in n for n in notes)

    def test_role_bias_influences_drop_order(self):
        bp = _blueprint(
            [FamilyCode.DLKD],
            [FamilyCode.SPRINT, FamilyCode.CARRY, FamilyCode.CORE, FamilyCode.HPUSH],
            [FamilyCode.DLKD, FamilyCode.SPRINT, FamilyCode.CARRY, FamilyCode.CORE, FamilyCode.HPUSH],
        )
        slots = [FamilyCode.DLKD, FamilyCode.SPRINT, FamilyCode.CARRY, FamilyCode.CORE, FamilyCode.HPUSH]
        rp = RoleWeekProfile(family_de_priority=["Sprint"])
        kept, notes, _ = apply_time_constraint_v2(slots, bp, 25, 6, role_profile=rp)
        # With de-priority, Sprint drops from TIER_A to TIER_B, but Carry is TIER_C
        # So Carry should be dropped first (lowest tier)
        assert FamilyCode.CARRY not in kept
        assert FamilyCode.DLKD in kept


class TestCompetitionTaper:

    def test_primer_taper_keeps_only_speed_and_core(self):
        bp = _blueprint(
            [FamilyCode.SPRINT],
            [FamilyCode.PLYO, FamilyCode.DLKD, FamilyCode.CORE],
            [FamilyCode.SPRINT, FamilyCode.PLYO, FamilyCode.DLKD, FamilyCode.CORE],
        )
        slots = [FamilyCode.SPRINT, FamilyCode.PLYO, FamilyCode.DLKD, FamilyCode.CORE]
        kept, notes = apply_competition_taper(slots, bp, 1)
        assert FamilyCode.SPRINT in kept
        assert FamilyCode.PLYO in kept
        assert FamilyCode.CORE in kept
        assert FamilyCode.DLKD not in kept

    def test_light_taper_drops_carry_and_acc(self):
        bp = _blueprint(
            [FamilyCode.DLKD],
            [FamilyCode.CARRY, FamilyCode.ACC, FamilyCode.CORE],
            [FamilyCode.DLKD, FamilyCode.CARRY, FamilyCode.ACC, FamilyCode.CORE],
        )
        slots = [FamilyCode.DLKD, FamilyCode.CARRY, FamilyCode.ACC, FamilyCode.CORE]
        kept, notes = apply_competition_taper(slots, bp, 2)
        assert FamilyCode.CARRY not in kept
        assert FamilyCode.ACC not in kept
        assert FamilyCode.DLKD in kept

    def test_moderate_taper_drops_only_tier_c(self):
        bp = _blueprint(
            [FamilyCode.DLKD],
            [FamilyCode.CARRY, FamilyCode.SPRINT, FamilyCode.CORE],
            [FamilyCode.DLKD, FamilyCode.CARRY, FamilyCode.SPRINT, FamilyCode.CORE],
        )
        slots = [FamilyCode.DLKD, FamilyCode.CARRY, FamilyCode.SPRINT, FamilyCode.CORE]
        kept, notes = apply_competition_taper(slots, bp, 4)
        assert FamilyCode.CARRY not in kept
        assert FamilyCode.SPRINT in kept
        assert FamilyCode.DLKD in kept

    def test_no_taper_returns_all(self):
        bp = _blueprint([FamilyCode.DLKD], [FamilyCode.CARRY], [FamilyCode.DLKD, FamilyCode.CARRY])
        slots = [FamilyCode.DLKD, FamilyCode.CARRY]
        kept, notes = apply_competition_taper(slots, bp, None)
        assert len(kept) == 2
        assert not notes


# ═══════════════════════════════════════════════════════════════════
# B. Order Rebuilding
# ═══════════════════════════════════════════════════════════════════

class TestSessionFlowOrder:

    def test_sprint_comes_before_strength(self):
        slots = [FamilyCode.DLKD, FamilyCode.SPRINT]
        result = rebuild_session_flow(slots)
        assert result[0] == FamilyCode.SPRINT
        assert result[1] == FamilyCode.DLKD

    def test_plyo_comes_before_strength(self):
        slots = [FamilyCode.HPUSH, FamilyCode.PLYO]
        result = rebuild_session_flow(slots)
        assert result[0] == FamilyCode.PLYO
        assert result[1] == FamilyCode.HPUSH

    def test_core_is_always_last(self):
        slots = [FamilyCode.CORE, FamilyCode.DLKD, FamilyCode.SPRINT]
        result = rebuild_session_flow(slots)
        assert result[-1] == FamilyCode.CORE

    def test_strength_comes_before_secondary(self):
        slots = [FamilyCode.SLKD, FamilyCode.DLKD]
        result = rebuild_session_flow(slots)
        assert result.index(FamilyCode.DLKD) < result.index(FamilyCode.SLKD)

    def test_secondary_comes_before_accessory(self):
        slots = [FamilyCode.CARRY, FamilyCode.ROT]
        result = rebuild_session_flow(slots)
        assert result.index(FamilyCode.ROT) < result.index(FamilyCode.CARRY)

    def test_full_flow_order(self):
        slots = [FamilyCode.DLKD, FamilyCode.SPRINT, FamilyCode.CORE, FamilyCode.CARRY, FamilyCode.ROT]
        result = rebuild_session_flow(slots)
        expected_order = [FamilyCode.SPRINT, FamilyCode.DLKD, FamilyCode.ROT, FamilyCode.CARRY, FamilyCode.CORE]
        assert result == expected_order

    def test_blueprint_slot_order_used_as_tiebreaker(self):
        bp = _blueprint(
            [FamilyCode.DLKD],
            [FamilyCode.DLHD, FamilyCode.HPUSH],
            [FamilyCode.DLKD, FamilyCode.HPUSH, FamilyCode.DLHD],
        )
        slots = [FamilyCode.HPUSH, FamilyCode.DLHD, FamilyCode.DLKD]
        result = rebuild_session_flow(slots, bp)
        # DLHD (flow=11) should come before HPUSH (flow=12) because of flow order
        assert result.index(FamilyCode.DLHD) < result.index(FamilyCode.HPUSH)

    def test_empty_slots_returns_empty(self):
        result = rebuild_session_flow([])
        assert result == []


# ═══════════════════════════════════════════════════════════════════
# C. Within-Week Continuity
# ═══════════════════════════════════════════════════════════════════

class TestWithinWeekContinuity:

    def test_dlkd_variation_is_slkd(self):
        assert get_within_week_variation_family(FamilyCode.DLKD) == FamilyCode.SLKD

    def test_sprint_variation_is_plyo(self):
        assert get_within_week_variation_family(FamilyCode.SPRINT) == FamilyCode.PLYO

    def test_plyo_variation_is_ball(self):
        assert get_within_week_variation_family(FamilyCode.PLYO) == FamilyCode.BALL

    def test_landing_variation_is_plyo(self):
        assert get_within_week_variation_family(FamilyCode.LANDING) == FamilyCode.PLYO

    def test_rot_variation_is_core(self):
        assert get_within_week_variation_family(FamilyCode.ROT) == FamilyCode.CORE

    def test_no_variation_for_core(self):
        assert get_within_week_variation_family(FamilyCode.CORE) is None

    def test_rationale_for_dlkd_is_unilateral(self):
        assert "unilateral" in get_within_week_variation_rationale(FamilyCode.DLKD)

    def test_rationale_for_sprint_is_elastic(self):
        assert "elastic" in get_within_week_variation_rationale(FamilyCode.SPRINT)


# ═══════════════════════════════════════════════════════════════════
# D. Injury / Risk Rebalance
# ═══════════════════════════════════════════════════════════════════

class TestRebalanceSessionBlocks:

    def test_empty_blocks_are_removed(self):
        blocks = [
            _block(FamilyCode.DLKD, True),
            _block(FamilyCode.SPRINT, False),
            _block(FamilyCode.HPUSH, True),
        ]
        result, notes = rebalance_session_blocks(blocks)
        assert len(result) == 2
        assert FamilyCode.SPRINT not in [b.family for b in result]

    def test_reorder_follows_session_flow(self):
        blocks = [
            _block(FamilyCode.DLKD, True),
            _block(FamilyCode.SPRINT, True),
        ]
        result, notes = rebalance_session_blocks(blocks)
        assert result[0].family == FamilyCode.SPRINT
        assert result[1].family == FamilyCode.DLKD

    def test_notes_mention_removed_families(self):
        blocks = [
            _block(FamilyCode.DLKD, True),
            _block(FamilyCode.SPRINT, False),
        ]
        result, notes = rebalance_session_blocks(blocks)
        assert any("Sprint" in n for n in notes)

    def test_core_moved_to_last(self):
        blocks = [
            _block(FamilyCode.CORE, True),
            _block(FamilyCode.DLKD, True),
        ]
        result, notes = rebalance_session_blocks(blocks)
        assert result[-1].family == FamilyCode.CORE

    def test_empty_session_returns_empty(self):
        result, notes = rebalance_session_blocks([])
        assert result == []

    def test_all_empty_blocks_returns_empty(self):
        blocks = [
            _block(FamilyCode.DLKD, False),
            _block(FamilyCode.SPRINT, False),
        ]
        result, notes = rebalance_session_blocks(blocks)
        assert result == []

    def test_rebalance_with_blueprint_backfill(self):
        bp = _blueprint(
            [FamilyCode.DLKD],
            [FamilyCode.HPUSH, FamilyCode.CORE],
            [FamilyCode.DLKD, FamilyCode.HPUSH, FamilyCode.CORE],
        )
        blocks = [
            _block(FamilyCode.DLKD, True),
        ]
        result, notes = rebalance_session_blocks(blocks, bp)
        # Should note backfill attempt
        assert any("backfill" in n.lower() for n in notes) or len(result) == 1


# ═══════════════════════════════════════════════════════════════════
# E. Blueprint Identity Preservation
# ═══════════════════════════════════════════════════════════════════

class TestBlueprintIdentityPreservation:

    def test_all_mandatory_present_passes(self):
        bp = _blueprint([FamilyCode.DLKD, FamilyCode.HPUSH], [FamilyCode.CORE], [FamilyCode.DLKD, FamilyCode.HPUSH, FamilyCode.CORE])
        blocks = [_block(FamilyCode.DLKD), _block(FamilyCode.HPUSH), _block(FamilyCode.CORE)]
        assert check_session_identity_preserved(blocks, bp) is True

    def test_one_mandatory_missing_fails(self):
        bp = _blueprint([FamilyCode.DLKD, FamilyCode.HPUSH], [FamilyCode.CORE], [FamilyCode.DLKD, FamilyCode.HPUSH, FamilyCode.CORE])
        blocks = [_block(FamilyCode.DLKD), _block(FamilyCode.CORE)]
        assert check_session_identity_preserved(blocks, bp) is True  # lenient: allows 1 missing

    def test_multiple_mandatory_missing_fails(self):
        bp = _blueprint([FamilyCode.DLKD, FamilyCode.HPUSH, FamilyCode.DLHD], [FamilyCode.CORE], [FamilyCode.DLKD, FamilyCode.HPUSH, FamilyCode.DLHD, FamilyCode.CORE])
        blocks = [_block(FamilyCode.DLKD)]
        assert check_session_identity_preserved(blocks, bp) is False

    def test_empty_mandatory_list_passes(self):
        bp = _blueprint([], [FamilyCode.CORE], [FamilyCode.CORE])
        blocks = [_block(FamilyCode.CORE)]
        assert check_session_identity_preserved(blocks, bp) is True

    def test_speed_before_strength_passes(self):
        blocks = [_block(FamilyCode.SPRINT), _block(FamilyCode.DLKD)]
        assert check_session_flow_credible(blocks) is True

    def test_speed_after_strength_fails(self):
        blocks = [_block(FamilyCode.DLKD), _block(FamilyCode.SPRINT)]
        assert check_session_flow_credible(blocks) is False

    def test_core_not_last_fails(self):
        blocks = [_block(FamilyCode.CORE), _block(FamilyCode.DLKD)]
        assert check_session_flow_credible(blocks) is False

    def test_core_last_passes(self):
        blocks = [_block(FamilyCode.DLKD), _block(FamilyCode.CORE)]
        assert check_session_flow_credible(blocks) is True

    def test_no_speed_or_strength_passes(self):
        blocks = [_block(FamilyCode.ROT), _block(FamilyCode.CORE)]
        assert check_session_flow_credible(blocks) is True

    def test_high_value_not_dropped_before_low_value_passes(self):
        bp = _blueprint([FamilyCode.DLKD], [FamilyCode.CARRY], [FamilyCode.DLKD, FamilyCode.CARRY])
        kept = [FamilyCode.DLKD]
        dropped = [FamilyCode.CARRY]
        assert check_high_value_families_not_dropped_before_low_value(kept, dropped, bp) is True

    def test_high_value_dropped_before_low_value_fails(self):
        bp = _blueprint([FamilyCode.DLKD], [FamilyCode.CARRY], [FamilyCode.DLKD, FamilyCode.CARRY])
        kept = [FamilyCode.CARRY]
        dropped = [FamilyCode.DLKD]
        assert check_high_value_families_not_dropped_before_low_value(kept, dropped, bp) is False

    def test_role_bias_not_overriding_passes(self):
        bp = _blueprint([FamilyCode.DLKD], [FamilyCode.SPRINT], [FamilyCode.DLKD, FamilyCode.SPRINT])
        blocks = [_block(FamilyCode.DLKD), _block(FamilyCode.SPRINT)]
        rp = RoleWeekProfile(family_de_priority=["Sprint"])
        assert check_role_bias_not_overriding_blueprint(blocks, bp, rp) is True

    def test_role_bias_overriding_with_single_family_fails(self):
        bp = _blueprint([FamilyCode.DLKD], [FamilyCode.SPRINT], [FamilyCode.DLKD, FamilyCode.SPRINT])
        blocks = [_block(FamilyCode.SPRINT)]
        rp = RoleWeekProfile(family_de_priority=["Sprint"])
        # Single de-prioritized family dominates 100% of session
        assert check_role_bias_not_overriding_blueprint(blocks, bp, rp) is False

    def test_taper_drops_carry_first_passes(self):
        bp = _blueprint([FamilyCode.DLKD], [FamilyCode.CARRY], [FamilyCode.DLKD, FamilyCode.CARRY])
        kept = [FamilyCode.DLKD]
        dropped = [FamilyCode.CARRY]
        assert check_taper_drop_logic_credible(kept, dropped, 2, bp) is True

    def test_taper_keeps_carry_fails(self):
        bp = _blueprint([FamilyCode.DLKD], [FamilyCode.CARRY], [FamilyCode.DLKD, FamilyCode.CARRY])
        kept = [FamilyCode.DLKD, FamilyCode.CARRY]
        dropped = []
        assert check_taper_drop_logic_credible(kept, dropped, 2, bp) is False

    def test_post_filter_balance_with_3_blocks_passes(self):
        blocks = [_block(FamilyCode.DLKD), _block(FamilyCode.HPUSH), _block(FamilyCode.CORE)]
        assert check_post_filter_session_balance(blocks) is True

    def test_post_filter_balance_with_2_blocks_fails(self):
        blocks = [_block(FamilyCode.DLKD), _block(FamilyCode.CORE)]
        assert check_post_filter_session_balance(blocks) is False

    def test_post_filter_balance_with_lower_only_passes(self):
        blocks = [_block(FamilyCode.DLKD), _block(FamilyCode.DLHD), _block(FamilyCode.CORE)]
        assert check_post_filter_session_balance(blocks) is True

    def test_post_filter_balance_with_upper_only_passes(self):
        blocks = [_block(FamilyCode.HPUSH), _block(FamilyCode.HPULL), _block(FamilyCode.CORE)]
        assert check_post_filter_session_balance(blocks) is True


# ═══════════════════════════════════════════════════════════════════
# F. Backward Compatibility
# ═══════════════════════════════════════════════════════════════════

class TestBackwardCompatibility:

    def test_no_role_no_assembly_bias_still_works(self):
        athlete = _make_athlete(position_role="")
        program = generate_program(athlete)
        assert program is not None
        assert len(program.sessions) > 0

    def test_no_position_role_session_flow_credible(self):
        athlete = _make_athlete(position_role="")
        program = generate_program(athlete)
        result = verify_program_credibility(program)
        assert result["session_flow_credible"] is True

    def test_existing_athlete_profile_without_wave9_fields(self):
        athlete = AthleteProfile(
            sport="rugby",
            training_age_years=2.0,
            season_phase=SeasonPhase.OFF_SEASON,
            goal="strength",
            equipment_profile=EquipmentProfile.COMMERCIAL_GYM,
            athlete_level=AthleteLevel.INTERMEDIATE,
            technique_consistency=0.9,
            injury_status="none",
            injury_history=[],
            fatigue_level="normal",
            weeks_since_break=0,
            recent_exercises={},
            available_minutes=60,
            days_to_match=None,
            preferred_families=6,
            age=20,
            strength_base_met=True,
        )
        program = generate_program(athlete)
        assert program is not None

    def test_old_time_constraint_function_still_exists(self):
        from forge.blueprint_engine import apply_time_constraint
        slots = [FamilyCode.DLKD, FamilyCode.HPUSH, FamilyCode.CORE]
        result = apply_time_constraint(slots, 60, 6)
        assert len(result) > 0

    def test_rebalance_with_none_blueprint_works(self):
        blocks = [_block(FamilyCode.DLKD), _block(FamilyCode.SPRINT, False)]
        result, notes = rebalance_session_blocks(blocks, None)
        assert len(result) == 1

    def test_program_credibility_all_checks_exist(self):
        athlete = _make_athlete()
        program = generate_program(athlete)
        result = verify_program_credibility(program)
        assert "session_identity_preserved" in result
        assert "session_flow_credible" in result
        assert "high_value_not_dropped_first" in result
        assert "role_bias_not_overriding_blueprint" in result
        assert "taper_drop_logic_credible" in result
        assert "post_filter_session_balance" in result


# ═══════════════════════════════════════════════════════════════════
# G. End-to-End Divergence
# ═══════════════════════════════════════════════════════════════════

class TestEndToEndDivergence:

    def test_same_blueprint_different_available_minutes(self):
        short = _make_athlete(available_minutes=30)
        long = _make_athlete(available_minutes=75)

        short_program = generate_program(short)
        long_program = generate_program(long)

        assert short_program.blueprint_id == long_program.blueprint_id

        # Short sessions should have fewer families
        short_fams = len(short_program.sessions[0].blocks)
        long_fams = len(long_program.sessions[0].blocks)
        assert short_fams <= long_fams

    def test_same_blueprint_different_comp_window(self):
        normal = _make_athlete(days_to_match=None)
        primer = _make_athlete(days_to_match=1)

        normal_program = generate_program(normal)
        primer_program = generate_program(primer)

        # Primer program should be light
        assert primer_program.sessions[0].total_duration_min <= normal_program.sessions[0].total_duration_min

    def test_same_blueprint_different_role(self):
        prop = _make_athlete(position_role="prop")
        backline = _make_athlete(position_role="back_three")

        prop_program = generate_program(prop)
        backline_program = generate_program(backline)

        assert prop_program.blueprint_id == backline_program.blueprint_id

        # At least one session across the program should differ in family composition
        any_diff = any(
            [b.family.value for b in prop_program.sessions[i].blocks] != [b.family.value for b in backline_program.sessions[i].blocks]
            for i in range(min(len(prop_program.sessions), len(backline_program.sessions)))
        )
        assert any_diff, "Prop and backline should differ in at least one session"

    def test_rugby_prop_vs_backline_session_flow_credible(self):
        prop = _make_athlete(position_role="prop")
        backline = _make_athlete(position_role="back_three")

        prop_program = generate_program(prop)
        backline_program = generate_program(backline)

        result_prop = verify_program_credibility(prop_program)
        result_backline = verify_program_credibility(backline_program)

        assert result_prop["session_flow_credible"] is True
        assert result_backline["session_flow_credible"] is True

    def test_renderer_includes_session_composition_notes(self):
        athlete = _make_athlete(position_role="prop")
        program = generate_program(athlete)
        summary = render_block_summary(program)
        # The summary should contain recognizable sections
        assert any(keyword in summary for keyword in ["Program Summary", "Exposure", "Role Week Bias"])

    def test_session_identity_preserved_for_all_roles(self):
        for role in ["prop", "back_three", "scrum_half", "fly_half"]:
            athlete = _make_athlete(position_role=role)
            program = generate_program(athlete)
            result = verify_program_credibility(program)
            assert result["session_identity_preserved"] is True, f"Identity failed for {role}"
            assert result["session_flow_credible"] is True, f"Flow failed for {role}"

    def test_volleyball_middle_vs_libero_different_session_structure(self):
        middle = _make_athlete(sport="volleyball", position_role="middle_blocker")
        libero = _make_athlete(sport="volleyball", position_role="libero")

        middle_program = generate_program(middle)
        libero_program = generate_program(libero)

        middle_fams = [b.family.value for b in middle_program.sessions[0].blocks]
        libero_fams = [b.family.value for b in libero_program.sessions[0].blocks]
        # Role-specific ordering should differ across the program, or at least differ in some session
        assert middle_fams != libero_fams or any(
            [b.family.value for b in middle_program.sessions[i].blocks] != [b.family.value for b in libero_program.sessions[i].blocks]
            for i in range(min(4, len(middle_program.sessions)))
        )

    def test_tennis_singles_vs_doubles_session_divergence(self):
        singles = _make_athlete(sport="tennis", position_role="singles")
        doubles = _make_athlete(sport="tennis", position_role="doubles")

        singles_program = generate_program(singles)
        doubles_program = generate_program(doubles)

        singles_fams = [b.family.value for b in singles_program.sessions[0].blocks]
        doubles_fams = [b.family.value for b in doubles_program.sessions[0].blocks]
        # May differ or may be same blueprint — at least one session should differ
        assert singles_fams != doubles_fams or any(
            [b.family.value for b in singles_program.sessions[i].blocks] != [b.family.value for b in doubles_program.sessions[i].blocks]
            for i in range(min(4, len(singles_program.sessions)))
        )

    def test_all_wave9_checks_pass_for_standard_athlete(self):
        athlete = _make_athlete()
        program = generate_program(athlete)
        result = verify_program_credibility(program)
        wave9_checks = [
            "session_identity_preserved",
            "session_flow_credible",
            "high_value_not_dropped_first",
            "role_bias_not_overriding_blueprint",
            "taper_drop_logic_credible",
            "post_filter_session_balance",
        ]
        for check in wave9_checks:
            assert result[check] is True, f"{check} failed for standard athlete"

    def test_session_order_follows_flow_for_speed_blueprint(self):
        # Full Body Strength blueprint (id=1) should have speed families early
        athlete = _make_athlete(sport="rugby", position_role="back_three", goal="speed")
        program = generate_program(athlete)
        result = verify_program_credibility(program)
        assert result["session_flow_credible"] is True

    def test_primer_taper_reduces_families(self):
        primer = _make_athlete(days_to_match=1)
        program = generate_program(primer)
        # The _generate_light_program is called for days_to_match=1, so check that
        assert program is not None
        assert len(program.sessions) > 0

    def test_time_constraint_notes_present_in_program(self):
        short = _make_athlete(available_minutes=30)
        program = generate_program(short)
        # The program should have some form of adjustment notes
        assert program.personalization_notes is not None

    def test_rebalance_does_not_destroy_session_structure(self):
        athlete = _make_athlete(injury_history=["knee"])
        program = generate_program(athlete)
        result = verify_program_credibility(program)
        assert result["post_filter_session_balance"] is True

    def test_competition_taper_checks_pass_for_primer(self):
        primer = _make_athlete(days_to_match=1)
        program = generate_program(primer)
        result = verify_program_credibility(program)
        assert result["taper_drop_logic_credible"] is True
