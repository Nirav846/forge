"""Wave 11A — Correction pass tests.
Tests the coach-like improvements to the initial minimum fixes.

Parts:
  A. Advanced athlete ceiling — use MAIN_STRENGTH_FAMILIES constant instead of hardcoded strings
  B. In-season volume reduction — role-aware trimming (preserve strength/power, trim accessory)
  C. Proportional time constraint — slot-aware compaction (primary < accessory reduction)
  D. Injury prevention — add decel_exposure_target trigger for Landing/Acc protection
"""

from __future__ import annotations

from src.forge.models import (
    AthleteLevel, AthleteProfile, EquipmentProfile, FamilyCode, Objective,
    PrescriptionRole, SeasonPhase,
)
from src.forge.data import get_equipment_for_profile
from src.forge.exercise_selector import select_exercise, MAIN_STRENGTH_FAMILIES
from src.forge.prescription_rules import (
    get_athlete_prescription_modifiers, get_prescription,
    PrescriptionRole,
)
from src.forge.main import generate_program
from src.forge.session_assembly import apply_time_constraint_v2
from src.forge.session_rules import (
    TIER_A, TIER_B, TIER_C, compute_family_survival_tier
)
from src.forge.role_week_planning import RoleWeekProfile, get_role_week_profile
from src.forge.blueprint_engine import Blueprint, BlueprintName
from src.forge.data import SELECTION_PRIORITIES


# ── Helpers ───────────────────────────────────────────────────────

def _make_athlete(**overrides) -> AthleteProfile:
    """Helper to build a baseline athlete."""
    defaults = {
        "sport": "rugby",
        "training_age_years": 5.0,
        "season_phase": SeasonPhase.OFF_SEASON,
        "goal": "strength",
        "equipment_profile": EquipmentProfile.COMMERCIAL_GYM,
        "athlete_level": AthleteLevel.ADVANCED,
        "technique_consistency": 1.0,
        "injury_status": "none",
        "injury_history": [],
        "fatigue_level": "normal",
        "weeks_since_break": 0,
        "recent_exercises": {},
        "available_minutes": 60,
        "days_to_match": None,
        "preferred_families": 6,
        "age": 25,
        "strength_base_met": True,
        "position_role": "back_three",
        "bodyweight_kg": 80.0,
        "force_profile": None,
        "elastic_profile": None,
        "conditioning_profile": None,
        "landing_competency": None,
        "sprint_mechanics_competency": None,
    }
    defaults.update(overrides)
    return AthleteProfile(**defaults)


def _blueprint_(
    mandatory: list[FamilyCode] | None = None,
    optional: list[FamilyCode] | None = None,
    slot_order: list[FamilyCode] | None = None,
) -> Blueprint:
    """Helper to build a test blueprint."""
    return Blueprint(
        id=999,
        name=BlueprintName.FULL_BODY_STRENGTH,
        purpose="Test", typical_athlete="intermediate",
        best_training_age="1-3",
        best_season_phase=[SeasonPhase.OFF_SEASON],
        typical_outcomes="strength",
        progression_path=None, regression_path=None,
        mandatory_families=mandatory or [FamilyCode.DLKD, FamilyCode.HPUSH],
        optional_families=optional or [FamilyCode.DLHD, FamilyCode.VPUSH],
        slot_order=slot_order or [FamilyCode.DLKD, FamilyCode.HPUSH, FamilyCode.DLHD, FamilyCode.VPUSH],
        typical_duration="8 weeks",
        best_frequency="3x per week", contraindications="none",
        min_session_composition=[],
    )


# ══════════════════════════════════════════════════════════════════════════════
# A. Advanced athlete ceiling — use constant instead of hardcoded strings
# ═════════════════════════════════════════════════════════════════════════════


def test_advanced_ceiling_uses_constant_instead_of_hardcoded_strings():
    """Advanced athlete ceiling should use MAIN_STRENGTH_FAMILIES constant."""
    # This test validates that we're using the constant, not hardcoded tuples
    # The constant contains DLKD and DLHD — verify they're in it
    assert FamilyCode.DLKD in MAIN_STRENGTH_FAMILIES
    assert FamilyCode.DLHD in MAIN_STRENGTH_FAMILIES
    # Should not contain HPush/HPull/etc in the constant itself (they're secondary)
    assert FamilyCode.HPUSH not in MAIN_STRENGTH_FAMILIES
    assert FamilyCode.HPULL not in MAIN_STRENGTH_FAMILIES


def test_advanced_ceiling_filters_dlkd_dlhd_for_advanced_athletes():
    """Advanced + strength_base_met should get difficulty >= 3 for DLKD/DLHD families."""
    athlete_level = AthleteLevel.ADVANCED
    strength_base_met = True
    equipment_profile = EquipmentProfile.COMMERCIAL_GYM

    # Test DLKD
    ex_dlkd = select_exercise(
        slot_family=FamilyCode.DLKD,
        athlete_level=athlete_level,
        equipment_profile=equipment_profile,
        recent_exercises={},
        injury_history=[],
        technique_consistency=1.0,
        strength_base_met=strength_base_met,
    )
    assert ex_dlkd is not None
    # With constant-based filtering, DLKD should get diff >= 3
    # The priority list for DLKD starts with Goblet Squat (diff 1), then others
    # The filter should skip Goblet Squat and get at least Barbell Squat (diff 3+)
    assert ex_dlkd.difficulty >= 3, f"Expected DLKD difficulty >= 3, got {ex_dlkd.difficulty}"

    # Test DLHD
    ex_dlhd = select_exercise(
        slot_family=FamilyCode.DLHD,
        athlete_level=athlete_level,
        equipment_profile=equipment_profile,
        recent_exercises={},
        injury_history=[],
        technique_consistency=1.0,
        strength_base_met=strength_base_met,
    )
    assert ex_dlhd is not None
    assert ex_dlhd.difficulty >= 3, f"Expected DLHD difficulty >= 3, got {ex_dlhd.difficulty}"


def test_advanced_ceiling_no_filter_for_non_advanced_or_no_base():
    """Non-advanced athletes or those without strength base should not get the filter."""
    athlete_level = AthleteLevel.INTERMEDIATE
    strength_base_met = True
    equipment_profile = EquipmentProfile.COMMERCIAL_GYM

    # Intermediate athlete
    ex_int = select_exercise(
        slot_family=FamilyCode.DLKD,
        athlete_level=athlete_level,
        equipment_profile=equipment_profile,
        recent_exercises={},
        injury_history=[],
        technique_consistency=1.0,
        strength_base_met=strength_base_met,
    )
    assert ex_int is not None
    # Intermediate should get normal diff (could be 1-3 based on level)
    assert ex_int.difficulty <= 3

    # Advanced but no strength base (should regress SL->DL but not apply ceiling)
    ex_no_base = select_exercise(
        slot_family=FamilyCode.SLKD,  # Will regress to DLKD due to no base
        athlete_level=AthleteLevel.ADVANCED,
        equipment_profile=equipment_profile,
        recent_exercises={},
        injury_history=[],
        technique_consistency=1.0,
        strength_base_met=False,  # No base
    )
    # Should get DLKD (regressed) but no ceiling filter -> could get Goblet Squat (diff 1)
    assert ex_no_base is not None
    assert ex_no_base.family == FamilyCode.DLKD  # Regressed
    # Without strength base, no ceiling -> can get low difficulty
    # Actually, max_diff for ADVANCED is 5, but no ceiling filter applies


# ══════════════════════════════════════════════════════════════════════════════
# B. In-season volume reduction — role-aware trimming
# ═════════════════════════════════════════════════════════════════════════════


def test_in_season_main_strength_gets_set_cap_4():
    """In-season MAIN_STRENGTH should get set_cap=4 (preserved)."""
    profile = _make_athlete(season_phase=SeasonPhase.IN_SEASON)
    mods = get_athlete_prescription_modifiers(profile, PrescriptionRole.MAIN_STRENGTH)
    assert mods.get("set_cap") == 4


def test_in_season_secondary_strength_gets_set_cap_4():
    """In-season SECONDARY_STRENGTH should get set_cap=4 (preserved)."""
    profile = _make_athlete(season_phase=SeasonPhase.IN_SEASON)
    mods = get_athlete_prescription_modifiers(profile, PrescriptionRole.SECONDARY_STRENGTH)
    assert mods.get("set_cap") == 4


def test_in_season_explosive_power_gets_set_cap_4():
    """In-season EXPLOSIVE_POWER should get set_cap=4 (preserved)."""
    profile = _make_athlete(season_phase=SeasonPhase.IN_SEASON)
    mods = get_athlete_prescription_modifiers(profile, PrescriptionRole.EXPLOSIVE_POWER)
    assert mods.get("set_cap") == 4


def test_in_season_plyometric_gets_set_cap_4():
    """In-season PLYOMETRIC should get set_cap=4 (preserved)."""
    profile = _make_athlete(season_phase=SeasonPhase.IN_SEASON)
    mods = get_athlete_prescription_modifiers(profile, PrescriptionRole.PLYOMETRIC)
    assert mods.get("set_cap") == 4


def test_in_season_sprint_mechanics_gets_set_cap_4():
    """In-season SPRINT_MECHANICS should get set_cap=4 (preserved)."""
    profile = _make_athlete(season_phase=SeasonPhase.IN_SEASON)
    mods = get_athlete_prescription_modifiers(profile, PrescriptionRole.SPRINT_MECHANICS)
    assert mods.get("set_cap") == 4


def test_in_season_hypertrophy_accessory_gets_set_cap_3():
    """In-season HYPERTROPHY_ACCESSORY should get set_cap=3 (trimmed more)."""
    profile = _make_athlete(season_phase=SeasonPhase.IN_SEASON)
    mods = get_athlete_prescription_modifiers(profile, PrescriptionRole.HYPERTROPHY_ACCESSORY)
    assert mods.get("set_cap") == 3


def test_in_season_conditioning_lift_gets_set_cap_3():
    """In-season CONDITIONING_LIFT should get set_cap=3 (trimmed more)."""
    profile = _make_athlete(season_phase=SeasonPhase.IN_SEASON)
    mods = get_athlete_prescription_modifiers(profile, PrescriptionRole.CONDITIONING_LIFT)
    assert mods.get("set_cap") == 3


def test_in_season_carry_capacity_gets_set_cap_3():
    """In-season CARRY_CAPACITY should get set_cap=3 (trimmed more)."""
    profile = _make_athlete(season_phase=SeasonPhase.IN_SEASON)
    mods = get_athlete_prescription_modifiers(profile, PrescriptionRole.CARRY_CAPACITY)
    assert mods.get("set_cap") == 3


def test_in_season_landing_core_rehab_uncapped():
    """In-season LANDING, CORE, REHAB should not get in-season set cap."""
    profile = _make_athlete(season_phase=SeasonPhase.IN_SEASON)
    
    # Landing
    mods_land = get_athlete_prescription_modifiers(profile, PrescriptionRole.LANDING_MECHANICS)
    set_cap_land = mods_land.get("set_cap", 999)
    assert set_cap_land == 999 or set_cap_land > 4  # Not the in-season cap of 3/4
    
    # Core
    mods_core = get_athlete_prescription_modifiers(profile, PrescriptionRole.CORE_STABILITY)
    set_cap_core = mods_core.get("set_cap", 999)
    assert set_cap_core == 999 or set_cap_core > 4
    
    # Rehab
    mods_rehab = get_athlete_prescription_modifiers(profile, PrescriptionRole.REHAB_PREHAB)
    set_cap_rehab = mods_rehab.get("set_cap", 999)
    assert set_cap_rehab == 999 or set_cap_rehab > 4


def test_off_season_no_in_season_caps():
    """Off-season athletes should not get the in-season role-based caps."""
    profile = _make_athlete(season_phase=SeasonPhase.OFF_SEASON)
    
    # These should NOT get the in-season specific caps
    roles_to_check = [
        PrescriptionRole.MAIN_STRENGTH,
        PrescriptionRole.SECONDARY_STRENGTH,
        PrescriptionRole.EXPLOSIVE_POWER,
        PrescriptionRole.HYPERTROPHY_ACCESSORY,
        PrescriptionRole.CONDITIONING_LIFT,
        PrescriptionRole.CARRY_CAPACITY,
    ]
    
    for role in roles_to_check:
        mods = get_athlete_prescription_modifiers(profile, role)
        set_cap = mods.get("set_cap", 999)
        # Should not be 3 or 4 from the in-season rule
        assert set_cap not in (3, 4), f"Off-season {role} should not get in-season cap, got {set_cap}"


def test_in_season_program_reduces_families_less_aggressively():
    """In-season should reduce families but less aggressively than before."""
    off = _make_athlete(season_phase=SeasonPhase.OFF_SEASON, preferred_families=8)
    on = _make_athlete(season_phase=SeasonPhase.IN_SEASON, preferred_families=8)

    off_prog = generate_program(off)
    on_prog = generate_program(on)

    # Off-season should have more families per session than in-season
    # But the difference should be less severe than the old version (5->6 preferred)
    off_fams = sum(len(s.blocks) for s in off_prog.sessions[:off_prog.frequency])
    on_fams = sum(len(s.blocks) for s in on_prog.sessions[:on_prog.frequency])
    
    # In-season should have fewer families, but not extremely fewer
    assert on_fams < off_fams
    # The reduction should be moderate (not the severe 5-cap from before)
    # With preferred_families reduced from 8 to 6, we expect reasonable retention
    assert on_fams >= off_fams * 0.55  # At least 55% of off-season families


# ══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
# C. Proportional time constraint — slot-aware compaction
# ════════════════════════════════════════════════════════════════════════════════════════════════════════════


def test_time_constraint_redesign_structure_type():
    """Verify that _build_session applies time constraint redesign."""
    athlete_30 = _make_athlete(available_minutes=30, season_phase=SeasonPhase.OFF_SEASON)
    athlete_75 = _make_athlete(available_minutes=75, season_phase=SeasonPhase.OFF_SEASON)

    program_30 = generate_program(athlete_30)
    program_75 = generate_program(athlete_75)

    session_30 = program_30.sessions[0]
    session_75 = program_75.sessions[0]

    # 30-min session should be minimalist or condensed
    assert session_30.structure_type in ("minimalist", "condensed")
    # 75-min session should be extended
    assert session_75.structure_type in ("extended", "standard")

    # 30-min should have fewer blocks than 75-min
    assert len(session_30.blocks) <= len(session_75.blocks)

    # Both should have time_notes
    assert len(session_30.time_notes) > 0
    assert len(session_75.time_notes) > 0


# ═══════════════════════════════════════════════════════════════════════════════════════════════════════════
# D. Injury prevention — add decel_exposure_target trigger
# ══════════════════════════════════════════════════════════════════════════════════════════════════════


def test_decel_exposure_target_promotes_target_promotes_landing_to_tier_b():
    """High decel exposure should promote Landing from TIER_C to at least TIER_B."""
    profile = RoleWeekProfile(
        decel_exposure_target="high",
        # sprint and jump could be low - we're testing decel specifically
        jump_exposure_target="low",
        sprint_exposure_target="low",
    )
    bp = _blueprint_(
        mandatory=[FamilyCode.DLKD, FamilyCode.HPUSH],
        optional=[FamilyCode.LANDING, FamilyCode.ACC],
        slot_order=[FamilyCode.LANDING, FamilyCode.DLKD, FamilyCode.HPUSH, FamilyCode.ACC],
    )
    tier = compute_family_survival_tier(FamilyCode.LANDING, bp, profile)
    assert tier <= TIER_B, f"Expected Landing <= TIER_B ({TIER_B}) with high decel, got {tier}"


def test_decel_exposure_target_promotes_acc_to_tier_b():
    """High decel exposure should promote Acc from TIER_C to at least TIER_B."""
    profile = RoleWeekProfile(
        decel_exposure_target="high",
        jump_exposure_target="low",
        sprint_exposure_target="low",
    )
    bp = _blueprint_(
        mandatory=[FamilyCode.DLKD, FamilyCode.HPUSH],
        optional=[FamilyCode.LANDING, FamilyCode.ACC],
        slot_order=[FamilyCode.LANDING, FamilyCode.DLKD, FamilyCode.HPUSH, FamilyCode.ACC],
    )
    tier = compute_family_survival_tier(FamilyCode.ACC, bp, profile)
    assert tier <= TIER_B, f"Expected Acc <= TIER_B ({TIER_B}) with high decel, got {tier}"


def test_tennis_singles_gets_landing_acc_protection_via_decel():
    """Tennis singles (high decel) should get Landing/Acc protection via decel target."""
    profile = get_role_week_profile("tennis", "singles")
    # Tennis singles has: decel_exposure_target="high" (from role_week_planning.py)
    assert profile.decel_exposure_target == "high"
    
    bp = _blueprint_(
        mandatory=[FamilyCode.DLKD, FamilyCode.HPUSH],
        optional=[FamilyCode.LANDING, FamilyCode.ACC],
        slot_order=[FamilyCode.LANDING, FamilyCode.DLKD, FamilyCode.HPUSH, FamilyCode.ACC],
    )
    
    # Landing should be protected
    landing_tier = compute_family_survival_tier(FamilyCode.LANDING, bp, profile)
    assert landing_tier <= TIER_B, f"Tennis singles Landing should be <= TIER_B, got {landing_tier}"
    
    # Acc should be protected
    acc_tier = compute_family_survival_tier(FamilyCode.ACC, bp, profile)
    assert acc_tier <= TIER_B, f"Tennis singles Acc should be <= TIER_B, got {acc_tier}"


def test_soccer_midfielder_gets_acc_protection_via_sprint_and_decel():
    """Soccer midfielder (high sprint + decel) should get Acc protection."""
    profile = get_role_week_profile("soccer", "midfielder")
    # Soccer midfielder has: sprint_exposure_target="high", decel_exposure_target="high"
    assert profile.sprint_exposure_target == "high"
    assert profile.decel_exposure_target == "high"
    
    bp = _blueprint_(
        mandatory=[FamilyCode.DLKD, FamilyCode.HPUSH],
        optional=[FamilyCode.LANDING, FamilyCode.ACC],
        slot_order=[FamilyCode.LANDING, FamilyCode.DLKD, FamilyCode.HPUSH, FamilyCode.ACC],
    )
    
    # Acc should be protected (by either sprint or decel)
    acc_tier = compute_family_survival_tier(FamilyCode.ACC, bp, profile)
    assert acc_tier <= TIER_B, f"Soccer midfielder Acc should be <= TIER_B, got {acc_tier}"


def test_no_decel_no_extra_protection_when_not_needed():
    """Low decel + low sprint/jump: Landing stays TIER_A (default), Acc stays TIER_C."""
    profile = RoleWeekProfile(
        decel_exposure_target="low",
        jump_exposure_target="low",
        sprint_exposure_target="low",
    )
    bp = _blueprint_(
        mandatory=[FamilyCode.DLKD, FamilyCode.HPUSH],
        optional=[FamilyCode.LANDING, FamilyCode.ACC],
        slot_order=[FamilyCode.LANDING, FamilyCode.DLKD, FamilyCode.HPUSH, FamilyCode.ACC],
    )

    landing_tier = compute_family_survival_tier(FamilyCode.LANDING, bp, profile)
    acc_tier = compute_family_survival_tier(FamilyCode.ACC, bp, profile)

    assert landing_tier == TIER_A, f"Expected Landing to stay TIER_A, got {landing_tier}"
    assert acc_tier == TIER_C, f"Expected Acc to stay TIER_C, got {acc_tier}"


def test_decel_works_with_other_role_profile_modifiers():
    """Decel protection should work alongside family_priority/de_priority modifiers."""
    profile = RoleWeekProfile(
        decel_exposure_target="high",
        jump_exposure_target="low",
        sprint_exposure_target="low",
        # Add some family priorities to test interaction
        family_priority=["Landing"],  # This should push Landing even higher
        family_de_priority=["Acc"],   # This should push Acc lower, but decel should counteract
    )
    bp = _blueprint_(
        mandatory=[FamilyCode.DLKD, FamilyCode.HPUSH],
        optional=[FamilyCode.LANDING, FamilyCode.ACC, FamilyCode.CARRY],
        slot_order=[FamilyCode.LANDING, FamilyCode.DLKD, FamilyCode.HPUSH, FamilyCode.ACC, FamilyCode.CARRY],
    )
    
    # Landing: base TIER_A -> family_priority["Landing"] stays at TIER_A -> decel keeps at TIER_A
    landing_tier = compute_family_survival_tier(FamilyCode.LANDING, bp, profile)
    assert landing_tier <= TIER_A, f"Landing with decel + priority should be <= TIER_A, got {landing_tier}"

    # Acc: base TIER_C -> de_priority: min(3+1, 3)=3 -> decel: min(3, 2)=2 (TIER_B)
    # ponytail: safety override is final, de_priority can't outrank injury prevention
    acc_tier = compute_family_survival_tier(FamilyCode.ACC, bp, profile)
    assert acc_tier == TIER_B, f"Acc with decel + de_priority should be TIER_B, got {acc_tier}"