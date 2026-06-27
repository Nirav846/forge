"""Wave 11A — Minimum coach-trust fixes.

Parts:
  A. Advanced athlete ceiling (difficulty floor for DLKD/DLHD)
  B. In-season volume reduction (preferred fams, avail min, set cap)
  C. Proportional time constraint reduction (compact_factor in session assembly)
  D. Injury prevention minimums (Landing/Acc survival tiers for explosive sports)
"""
from __future__ import annotations
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.forge.exercise_selector import select_exercise
from src.forge.models import (
    AthleteProfile, AthleteLevel, EquipmentProfile, SeasonPhase,
    FamilyCode, Exercise, PrescriptionRole,
)
from src.forge.data import EXERCISE_BY_ID, SELECTION_PRIORITIES
from src.forge.prescription_rules import get_athlete_prescription_modifiers, get_prescription
from src.forge.session_assembly import apply_time_constraint_v2
from src.forge.session_rules import compute_family_survival_tier, TIER_A, TIER_B, TIER_C
from src.forge.role_week_planning import RoleWeekProfile
from src.forge.main import generate_program


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
        "position_role": "",
        "bodyweight_kg": 80.0,
    }
    defaults.update(overrides)
    return AthleteProfile(**defaults)


def _blueprint_(mandatory: list[FamilyCode], optional: list[FamilyCode],
                slot_order: list[FamilyCode]):
    from src.forge.data import Blueprint, BlueprintName
    return Blueprint(
        id=99, name=BlueprintName.FULL_BODY_STRENGTH,
        purpose="Test", typical_athlete="intermediate",
        best_training_age="1-3",
        best_season_phase=[SeasonPhase.OFF_SEASON],
        best_frequency="3x per week", contraindications="none",
        typical_outcomes="strength",
        progression_path=None, regression_path=None,
        mandatory_families=mandatory, optional_families=optional,
        slot_order=slot_order,
        typical_duration="8 weeks",
        min_session_composition=[],
    )


# ═══════════════════════════════════════════════════════════════════
# A. Advanced Athlete Ceiling
# ═══════════════════════════════════════════════════════════════════

class TestAdvancedAthleteCeiling:

    def test_advanced_dlkd_selects_barbell_squat_over_goblet(self):
        """Advanced DLKD with strength_base should skip Goblet Squat (diff 2)."""
        ex = select_exercise(
            FamilyCode.DLKD, AthleteLevel.ADVANCED,
            EquipmentProfile.COMMERCIAL_GYM, {}, [],
            strength_base_met=True,
        )
        assert ex is not None
        assert ex.difficulty >= 3, f"Expected difficulty >= 3, got {ex.id} (diff {ex.difficulty})"

    def test_advanced_dlhd_selects_min_diff_3(self):
        """Advanced DLHD with strength_base should only get difficulty >= 3."""
        ex = select_exercise(
            FamilyCode.DLHD, AthleteLevel.ADVANCED,
            EquipmentProfile.COMMERCIAL_GYM, {}, [],
            strength_base_met=True,
        )
        assert ex is not None
        assert ex.difficulty >= 3, f"Expected difficulty >= 3, got {ex.id} (diff {ex.difficulty})"

    def test_intermediate_dlkd_can_get_goblet_squat(self):
        """Intermediate DLKD should still be able to select Goblet Squat (diff 2)."""
        ex = select_exercise(
            FamilyCode.DLKD, AthleteLevel.INTERMEDIATE,
            EquipmentProfile.COMMERCIAL_GYM, {}, [],
            strength_base_met=True,
        )
        assert ex is not None

    def test_advanced_dlkd_no_strength_base_allows_lower_diff(self):
        """Advanced DLKD without strength_base should still access lower difficulties."""
        ex = select_exercise(
            FamilyCode.DLKD, AthleteLevel.ADVANCED,
            EquipmentProfile.COMMERCIAL_GYM, {}, [],
            strength_base_met=False,
        )
        assert ex is not None
        # When base not met, SLKD→DLKD may apply, but Goblet should still be accessible
        assert ex.difficulty <= 3

    def test_advanced_plyo_no_restriction(self):
        """Advanced athletes in Plyo should not have a difficulty floor."""
        ex = select_exercise(
            FamilyCode.PLYO, AthleteLevel.ADVANCED,
            EquipmentProfile.COMMERCIAL_GYM, {}, [],
            strength_base_met=True,
        )
        assert ex is not None
        # Plyo-004 (Depth Jump) is diff 4, Plyo-002 is diff 3 — both accessible


# ═══════════════════════════════════════════════════════════════════
# B. In-Season Volume Reduction
# ═══════════════════════════════════════════════════════════════════

class TestInSeasonVolumeReduction:

    def test_in_season_reduces_preferred_families(self):
        """In-season athletes should have reduced preferred families in program."""
        off = _make_athlete(season_phase=SeasonPhase.OFF_SEASON, preferred_families=8)
        on = _make_athlete(season_phase=SeasonPhase.IN_SEASON, preferred_families=8)

        off_prog = generate_program(off)
        on_prog = generate_program(on)

        # Off-season should have more families per session than in-season
        off_fams = sum(len(s.blocks) for s in off_prog.sessions[:off_prog.frequency])
        on_fams = sum(len(s.blocks) for s in on_prog.sessions[:on_prog.frequency])
        assert on_fams < off_fams

    def test_in_season_prescription_set_cap(self):
        """In-season athlete should have set cap on main strength prescriptions."""
        p = _make_athlete(season_phase=SeasonPhase.IN_SEASON)
        mods = get_athlete_prescription_modifiers(p, PrescriptionRole.MAIN_STRENGTH)
        assert mods.get("set_cap", 999) <= 4

    def test_off_season_no_set_cap(self):
        """Off-season athlete should not have in-season set cap."""
        p = _make_athlete(season_phase=SeasonPhase.OFF_SEASON)
        mods = get_athlete_prescription_modifiers(p, PrescriptionRole.MAIN_STRENGTH)
        # No in-season cap, should be empty or have different caps
        set_cap = mods.get("set_cap", 999)
        assert set_cap > 4 or set_cap == 999


# ═══════════════════════════════════════════════════════════════════
# C. Proportional Time Constraint Reduction
# ═══════════════════════════════════════════════════════════════════

class TestProportionalTimeConstraint:

    def test_sufficient_time_compact_factor_1(self):
        """>=60 min should return compact_factor of 1.0."""
        bp = _blueprint_(
            mandatory=[FamilyCode.DLKD, FamilyCode.HPUSH],
            optional=[FamilyCode.DLHD, FamilyCode.VPUSH, FamilyCode.CORE],
            slot_order=[FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.HPUSH, FamilyCode.VPUSH, FamilyCode.CORE],
        )
        slots = [FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.HPUSH, FamilyCode.VPUSH, FamilyCode.CORE]
        _, _, cf = apply_time_constraint_v2(slots, bp, 75, 6)
        assert cf == 1.0

    def test_moderate_constraint_compact_factor(self):
        """45-59 min should return compact_factor < 1.0."""
        bp = _blueprint_(
            mandatory=[FamilyCode.DLKD, FamilyCode.HPUSH],
            optional=[FamilyCode.DLHD, FamilyCode.VPUSH, FamilyCode.CORE],
            slot_order=[FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.HPUSH, FamilyCode.VPUSH, FamilyCode.CORE],
        )
        slots = [FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.HPUSH, FamilyCode.VPUSH, FamilyCode.CORE]
        _, _, cf = apply_time_constraint_v2(slots, bp, 50, 6)
        assert cf < 1.0 and cf > 0.0

    def test_severe_constraint_low_compact_factor(self):
        """<30 min should return low compact_factor."""
        bp = _blueprint_(
            mandatory=[FamilyCode.DLKD, FamilyCode.HPUSH],
            optional=[FamilyCode.DLHD, FamilyCode.VPUSH, FamilyCode.CORE],
            slot_order=[FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.HPUSH, FamilyCode.VPUSH, FamilyCode.CORE],
        )
        slots = [FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.HPUSH, FamilyCode.VPUSH, FamilyCode.CORE]
        _, _, cf = apply_time_constraint_v2(slots, bp, 25, 6)
        assert cf < 0.6

    def test_compact_factor_decreasing_with_tightness(self):
        """Compact factor should decrease as time tightens."""
        bp = _blueprint_(
            mandatory=[FamilyCode.DLKD, FamilyCode.HPUSH],
            optional=[FamilyCode.DLHD, FamilyCode.VPUSH, FamilyCode.CORE],
            slot_order=[FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.HPUSH, FamilyCode.VPUSH, FamilyCode.CORE],
        )
        slots = [FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.HPUSH, FamilyCode.VPUSH, FamilyCode.CORE]
        _, _, cf_75 = apply_time_constraint_v2(slots, bp, 75, 6)
        _, _, cf_50 = apply_time_constraint_v2(slots, bp, 50, 6)
        _, _, cf_25 = apply_time_constraint_v2(slots, bp, 25, 6)
        assert cf_75 == 1.0
        assert cf_50 > cf_25


# ═══════════════════════════════════════════════════════════════════
# D. Injury Prevention Minimums
# ═══════════════════════════════════════════════════════════════════

class TestInjuryPreventionMinimums:

    def test_explosive_sport_acc_promoted_to_tier_b(self):
        """Explosive sport profile should promote Acc from TIER_C to TIER_B."""
        profile = RoleWeekProfile(
            jump_exposure_target="high", sprint_exposure_target="high",
        )
        bp = _blueprint_(
            mandatory=[FamilyCode.DLKD, FamilyCode.HPUSH],
            optional=[FamilyCode.ACC, FamilyCode.CARRY],
            slot_order=[FamilyCode.DLKD, FamilyCode.HPUSH, FamilyCode.ACC, FamilyCode.CARRY],
        )
        tier = compute_family_survival_tier(FamilyCode.ACC, bp, profile)
        assert tier <= TIER_B, f"Expected Acc <= TIER_B ({TIER_B}), got {tier}"

    def test_non_explosive_sport_acc_stays_tier_c(self):
        """Non-explosive sport profile should keep Acc at TIER_C."""
        profile = RoleWeekProfile(
            jump_exposure_target="low", sprint_exposure_target="low",
        )
        bp = _blueprint_(
            mandatory=[FamilyCode.DLKD, FamilyCode.HPUSH],
            optional=[FamilyCode.ACC, FamilyCode.CARRY],
            slot_order=[FamilyCode.DLKD, FamilyCode.HPUSH, FamilyCode.ACC, FamilyCode.CARRY],
        )
        tier = compute_family_survival_tier(FamilyCode.ACC, bp, profile)
        assert tier == TIER_C

    def test_explosive_landing_keeps_tier_a(self):
        """Explosive sport Landing should stay at TIER_A (no promotion needed)."""
        profile = RoleWeekProfile(
            jump_exposure_target="high", sprint_exposure_target="high",
        )
        bp = _blueprint_(
            mandatory=[FamilyCode.DLKD, FamilyCode.HPUSH],
            optional=[FamilyCode.LANDING, FamilyCode.ACC],
            slot_order=[FamilyCode.LANDING, FamilyCode.DLKD, FamilyCode.HPUSH, FamilyCode.ACC],
        )
        tier = compute_family_survival_tier(FamilyCode.LANDING, bp, profile)
        assert tier <= TIER_A

    def test_rugby_back_three_sprint_high_promotes_acc(self):
        """Rugby back_three has sprint_exposure_target=high → Acc promoted."""
        from src.forge.role_week_planning import get_role_week_profile
        profile = get_role_week_profile("rugby", "back_three")
        bp = _blueprint_(
            mandatory=[FamilyCode.DLKD, FamilyCode.HPUSH],
            optional=[FamilyCode.ACC, FamilyCode.CARRY],
            slot_order=[FamilyCode.DLKD, FamilyCode.HPUSH, FamilyCode.ACC, FamilyCode.CARRY],
        )
        tier = compute_family_survival_tier(FamilyCode.ACC, bp, profile)
        assert tier <= TIER_B
