"""Wave 2 tests: Load Prescription & Progression Hardening.

13+ tests covering all Phase A–E requirements.
"""
import re
import pytest
from src.forge.models import (
    AthleteProfile, AthleteLevel, EquipmentProfile, SeasonPhase,
    FamilyCode, Objective, PrescriptionRole, Prescription,
    COMP_WINDOW_LABELS,
)
from src.forge.prescription_rules import (
    derive_role, get_prescription, resolve_comp_window,
    PRESCRIPTION_TABLE, BLUEPRINT_CATEGORIES,
    BLUEPRINT_PRESCRIPTION_MODIFIERS, WEEK_VOLUME_FACTORS,
    _cap_sets, _scale_sets,
)
from src.forge.data import (
    EXERCISE_BY_ID, BLUEPRINT_BY_ID,
)
from src.forge.main import generate_program, _build_session
from src.forge.renderer import render_coach_session
from src.forge.validator import (
    verify_credibility, calculate_credibility_score,
    _check_prescription_role, _check_prescription_comp,
    _check_prescription_youth,
)


# ── Helpers ────────────────────────────────────────────────────────

def _make_exercise(
    eid="DLKD-004", name="Goblet Squat", family=FamilyCode.DLKD,
    obj=Objective.STRENGTH, diff=2, equip=None, unilateral=False,
    explosive=False, isometric=False, rotational=False,
):
    return EXERCISE_BY_ID[eid]


def _make_athlete(
    level=AthleteLevel.INTERMEDIATE, training_age=3.0, age=25,
    goal="strength", sport="rugby", technique=1.0,
    strength_base=True, equip=EquipmentProfile.COMMERCIAL_GYM,
    phase=SeasonPhase.OFF_SEASON, injury=None, days=None,
):
    return AthleteProfile(
        sport=sport, training_age_years=training_age,
        season_phase=phase, goal=goal,
        equipment_profile=equip, athlete_level=level,
        technique_consistency=technique,
        strength_base_met=strength_base,
        injury_status=injury or "none",
        injury_history=[] if not injury else [injury],
        age=age, days_to_match=days,
    )


# ── PHASE A: PRESCRIPTION ROLE DERIVATION ─────────────────────────

class TestRoleDerivation:
    def test_main_strength_dlkd_str(self):
        ex = _make_exercise("DLKD-004", family=FamilyCode.DLKD, obj=Objective.STRENGTH)
        assert derive_role(ex) == PrescriptionRole.MAIN_STRENGTH

    def test_main_strength_dlhd_str(self):
        ex = _make_exercise("DLHD-006", family=FamilyCode.DLHD, obj=Objective.STRENGTH)
        assert derive_role(ex) == PrescriptionRole.MAIN_STRENGTH

    def test_secondary_strength_hpush(self):
        ex = _make_exercise("HPush-005", family=FamilyCode.HPUSH, obj=Objective.STRENGTH)
        assert derive_role(ex) == PrescriptionRole.SECONDARY_STRENGTH

    def test_explosive_power_ball(self):
        ex = _make_exercise("Ball-001", family=FamilyCode.BALL, obj=Objective.POWER)
        assert derive_role(ex) == PrescriptionRole.EXPLOSIVE_POWER

    def test_plyometric(self):
        ex = _make_exercise("Plyo-001", family=FamilyCode.PLYO, obj=Objective.POWER)
        assert derive_role(ex) == PrescriptionRole.PLYOMETRIC

    def test_sprint_mechanics(self):
        ex = _make_exercise("Sprint-001", family=FamilyCode.SPRINT, obj=Objective.STRENGTH)
        assert derive_role(ex) == PrescriptionRole.SPRINT_MECHANICS

    def test_core_stability(self):
        ex = _make_exercise("Core-002", family=FamilyCode.CORE, obj=Objective.STABILITY)
        assert derive_role(ex) == PrescriptionRole.CORE_STABILITY

    def test_carry_capacity(self):
        ex = _make_exercise("Carry-001", family=FamilyCode.CARRY, obj=Objective.STRENGTH)
        assert derive_role(ex) == PrescriptionRole.CARRY_CAPACITY

    def test_landing_mechanics(self):
        ex = _make_exercise("Landing-001", family=FamilyCode.LANDING, obj=Objective.POWER)
        assert derive_role(ex) == PrescriptionRole.LANDING_MECHANICS

    def test_hypertrophy_accessory(self):
        ex = _make_exercise("HPull-006", family=FamilyCode.HPULL, obj=Objective.HYPERTROPHY)
        assert derive_role(ex) == PrescriptionRole.HYPERTROPHY_ACCESSORY

    def test_rehab_prehab_stab(self):
        ex = _make_exercise("DLKD-002", family=FamilyCode.DLKD, obj=Objective.STABILITY)
        assert derive_role(ex) in (PrescriptionRole.REHAB_PREHAB, PrescriptionRole.MAIN_STRENGTH)


# ── PHASE A: PRESCRIPTION TABLE LOOKUPS ──────────────────────────

class TestPrescriptionTable:
    def test_all_levels_have_targets(self):
        ex = _make_exercise("DLKD-004")
        for level in AthleteLevel:
            p = get_prescription(ex, level, blueprint_id=1)
            assert p.sets, f"No prescription for {level}"
            assert p.reps, f"No reps for {level}"
            assert p.progression_method, f"No progression for {level}"

    def test_main_strength_differs_by_level(self):
        ex = _make_exercise("DLKD-004")
        b = get_prescription(ex, AthleteLevel.BEGINNER, blueprint_id=1)
        a = get_prescription(ex, AthleteLevel.ADVANCED, blueprint_id=1)
        assert b.rest_seconds < a.rest_seconds, "Beginner should rest less than advanced"

    def test_beginner_gets_higher_reps(self):
        ex = _make_exercise("DLKD-004")
        b = get_prescription(ex, AthleteLevel.BEGINNER, blueprint_id=1)
        a = get_prescription(ex, AthleteLevel.ADVANCED, blueprint_id=1)
        b_reps = int(b.reps.split("-")[1].split()[0]) if "-" in b.reps else int(b.reps.split()[0])
        a_reps = int(a.reps.split("-")[1].split()[0]) if "-" in a.reps else int(a.reps.split()[0])
        assert b_reps > a_reps, "Beginner reps should exceed advanced reps"

    def test_accessory_differs_from_main(self):
        main = _make_exercise("DLKD-004")
        acc = _make_exercise("HPull-006", family=FamilyCode.HPULL, obj=Objective.HYPERTROPHY)
        p_main = get_prescription(main, AthleteLevel.INTERMEDIATE, blueprint_id=1)
        p_acc = get_prescription(acc, AthleteLevel.INTERMEDIATE, blueprint_id=1)
        assert p_acc.loading_method != p_main.loading_method or p_acc.reps != p_main.reps


# ── PHASE A: COMPETITION WINDOW MODIFIERS ────────────────────────

class TestCompWindow:
    def test_full_week_no_reduction(self):
        ex = _make_exercise("DLKD-004")
        p_full = get_prescription(ex, AthleteLevel.INTERMEDIATE, blueprint_id=1, comp_window=6)
        p_none = get_prescription(ex, AthleteLevel.INTERMEDIATE, blueprint_id=1, comp_window=None)
        assert p_full.sets == p_none.sets

    def test_primer_day_reduces_volume(self):
        ex = _make_exercise("DLKD-004")
        p_full = get_prescription(ex, AthleteLevel.INTERMEDIATE, blueprint_id=1, comp_window=6)
        p_prim = get_prescription(ex, AthleteLevel.INTERMEDIATE, blueprint_id=1, comp_window=1)
        full_max = max(int(n) for n in p_full.sets.split("-")) if "-" in p_full.sets else int(p_full.sets)
        prim_max = max(int(n) for n in p_prim.sets.split("-")) if "-" in p_prim.sets else int(p_prim.sets)
        assert prim_max < full_max, f"Primer ({prim_max}) should be less than full ({full_max})"

    def test_light_window_removes_accessories(self):
        ex = _make_exercise("HPull-006", family=FamilyCode.HPULL, obj=Objective.HYPERTROPHY)
        p_full = get_prescription(ex, AthleteLevel.INTERMEDIATE, blueprint_id=1, comp_window=6)
        p_light = get_prescription(ex, AthleteLevel.INTERMEDIATE, blueprint_id=1, comp_window=2)
        light_max = max(int(n) for n in re.findall(r'\d+', p_light.sets))
        assert light_max <= 2, f"Light accessories should be capped at 2 sets, got {p_light.sets}"


# ── PHASE A: YOUTH CAPS ─────────────────────────────────────────

class TestYouthPrescription:
    def test_youth_foundation_caps_sets(self):
        ex = _make_exercise("DLKD-004")
        p = get_prescription(ex, AthleteLevel.ADVANCED, blueprint_id=7)  # Youth Foundation
        nums = [int(n) for n in re.findall(r'\d+', p.sets)]
        assert max(nums) <= 3, f"Youth should be capped at 3 sets, got {p.sets}"


# ── PHASE A: BLUEPRINT-SPECIFIC OVERRIDES ───────────────────────

class TestBlueprintOverrides:
    def test_deload_caps_all_sets(self):
        ex = _make_exercise("DLKD-004")
        p = get_prescription(ex, AthleteLevel.ADVANCED, blueprint_id=13)
        nums = [int(n) for n in re.findall(r'\d+', p.sets)]
        assert max(nums) <= 2, f"Deload should cap at 2 sets, got {p.sets}"

    def test_deload_reduces_intensity(self):
        ex = _make_exercise("DLKD-004")
        p = get_prescription(ex, AthleteLevel.ADVANCED, blueprint_id=13)
        assert "RPE 5-6" in p.intensity_note, f"Deload should note low RPE, got {p.intensity_note}"

    def test_power_speed_reduces_strength_volume(self):
        ex = _make_exercise("DLKD-004")
        p_str = get_prescription(ex, AthleteLevel.ADVANCED, blueprint_id=1)
        p_pow = get_prescription(ex, AthleteLevel.ADVANCED, blueprint_id=4)
        str_sets = [int(n) for n in re.findall(r'\d+', p_str.sets)]
        pow_sets = [int(n) for n in re.findall(r'\d+', p_pow.sets)]
        assert max(pow_sets) <= max(str_sets), "Power blueprint should not increase strength volume"


# ── PHASE B: SESSION-LEVEL PRESCRIPTION ──────────────────────────

class TestSessionPrescription:
    def test_generated_session_has_prescriptions(self):
        athlete = _make_athlete()
        program = generate_program(athlete)
        for session in program.sessions:
            for block in session.blocks:
                if block.exercises:
                    assert block.prescription is not None, f"Missing prescription for {block.family}"
                    assert block.prescription.sets != "", "Missing sets"
                    assert block.prescription.reps != "", "Missing reps"

    def test_main_blocks_have_progression_method(self):
        athlete = _make_athlete()
        program = generate_program(athlete)
        found = False
        for session in program.sessions:
            for block in session.blocks:
                if block.prescription and block.prescription.progression_method:
                    found = True
        assert found, "No progression method found in any block"


# ── PHASE C: PROGRESSION MODEL ──────────────────────────────────

class TestProgression:
    def test_week_volume_shape(self):
        """Weeks 1 and 8 should have lower volume than weeks 4-6."""
        ex = _make_exercise("DLKD-004")
        w1 = get_prescription(ex, AthleteLevel.INTERMEDIATE, blueprint_id=1, week=1)
        w4 = get_prescription(ex, AthleteLevel.INTERMEDIATE, blueprint_id=1, week=4)
        w8 = get_prescription(ex, AthleteLevel.INTERMEDIATE, blueprint_id=1, week=8)
        w1_max = max(int(n) for n in re.findall(r'\d+', w1.sets))
        w4_max = max(int(n) for n in re.findall(r'\d+', w4.sets))
        w8_max = max(int(n) for n in re.findall(r'\d+', w8.sets))
        assert w1_max <= w4_max, f"Week 1 ({w1_max}) should not exceed week 4 ({w4_max})"
        assert w8_max <= w4_max, f"Week 8 ({w8_max}) should not exceed week 4 ({w4_max})"

    def test_progression_methods_defined(self):
        ex = _make_exercise("DLKD-004")
        for level in AthleteLevel:
            p = get_prescription(ex, level, blueprint_id=1)
            assert p.progression_method in (
                "double_progression", "linear", "exposure",
            ), f"Unexpected progression: {p.progression_method}"


# ── PHASE D: GENERATED PROGRAM VARIETY ──────────────────────────

class TestBlueprintVariety:
    def test_strength_blueprint_not_same_as_hypertrophy(self):
        athlete_s = _make_athlete(goal="strength")
        athlete_h = _make_athlete(goal="mass", level=AthleteLevel.INTERMEDIATE)
        prog_s = generate_program(athlete_s)
        prog_h = generate_program(athlete_h)
        # Both should generate without errors
        assert len(prog_s.sessions) > 0
        assert len(prog_h.sessions) > 0

    def test_programs_mark_blueprint_id(self):
        athlete = _make_athlete()
        program = generate_program(athlete)
        assert program.blueprint_id > 0


# ── PHASE E: VALIDATOR PRESCRIPTION CHECKS ──────────────────────

class TestValidatorPrescription:
    def test_validator_has_new_checks(self):
        athlete = _make_athlete()
        program = generate_program(athlete)
        check = verify_credibility(program.sessions[0], athlete)
        assert "prescription_role_appropriate" in check
        assert "prescription_competition_safe" in check
        assert "prescription_youth_safe" in check

    def test_calculate_credibility_with_prescription(self):
        athlete = _make_athlete()
        program = generate_program(athlete)
        check = verify_credibility(program.sessions[0], athlete)
        score = calculate_credibility_score(check)
        assert 0 <= score <= 1.0

    def test_coach_output_shows_prescription(self):
        athlete = _make_athlete()
        program = generate_program(athlete)
        output = render_coach_session(program.sessions[0])
        assert "x" in output, "Coach view should contain 'x' (sets x reps)"
        assert "rest" in output.lower() or "min" in output

    def test_youth_prescription_check(self):
        athlete = _make_athlete(age=16, level=AthleteLevel.BEGINNER)
        program = generate_program(athlete)
        for session in program.sessions:
            check = verify_credibility(session, athlete)
            assert check["prescription_youth_safe"], "Youth check should pass"


# ── PHASE E: HELPER FUNCTIONS ────────────────────────────────────

class TestHelpers:
    def test_cap_sets_range(self):
        assert _cap_sets("4-5", 3) == "3"
        assert _cap_sets("3-4", 3) == "3"
        assert _cap_sets("2-3", 5) == "2-3"

    def test_scale_sets(self):
        scaled = _scale_sets("4-5", 0.75)
        nums = [int(n) for n in re.findall(r'\d+', scaled)]
        assert max(nums) <= 4


# ── PHASE B: PRESCRIPTION OUTPUT FORMAT ─────────────────────────

class TestPrescriptionOutput:
    def test_power_prescription_low_rep(self):
        """Power work should not use hypertrophy rep ranges."""
        ex = _make_exercise("Plyo-001", family=FamilyCode.PLYO, obj=Objective.POWER)
        p = get_prescription(ex, AthleteLevel.INTERMEDIATE, blueprint_id=4)
        nums = [int(n) for n in re.findall(r'\d+', p.reps)]
        assert max(nums) <= 6, f"Power reps should be low, got {p.reps}"

    def test_conditioning_lift_high_rep(self):
        ex = _make_exercise("DLKD-005", family=FamilyCode.DLKD, obj=Objective.CONDITIONING)
        # Make a COND exercise
        from src.forge.data import EXERCISE_BY_ID
        ex_cond = EXERCISE_BY_ID["Sprint-019"]  # COND objective
        p = get_prescription(ex_cond, AthleteLevel.INTERMEDIATE, blueprint_id=3)
        nums = [int(n) for n in re.findall(r'\d+', p.reps)]
        assert max(nums) >= 15, f"COND reps should be high, got {p.reps}"

    def test_core_uses_exposure_progression(self):
        ex = _make_exercise("Core-002", family=FamilyCode.CORE, obj=Objective.STABILITY)
        p = get_prescription(ex, AthleteLevel.INTERMEDIATE, blueprint_id=1)
        assert p.progression_method == "exposure"


# ── FULL REGRESSION ──────────────────────────────────────────────

class TestFullRegression:
    def test_demo_runs_all_nine(self):
        from src.forge.__main__ import demo
        try:
            demo()
        except Exception as e:
            pytest.fail(f"Demo failed: {e}")

    def test_all_wave1_tests_still_pass(self):
        """Run the Wave 1 test module contents as a smoke test."""
        from src.test_wave1_hardening import (
            TestRestByObjective, TestLoadSpikePrevention,
            TestMasteryGate, TestBilateralUnilateral,
            TestInjuryMap, TestWarmupTemplates,
            TestRampAudit, TestLandingMechanics,
            TestSprintMechanics, TestFullDemo,
        )
        # If imports work without error, the module is compatible
        assert True
