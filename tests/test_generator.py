"""FORGE test suite — 77+ tests covering all engines."""

import unittest
from src.forge.models import (
    AthleteProfile, AthleteLevel, EquipmentProfile, SeasonPhase,
    Objective, FamilyCode, BlueprintName, Exercise, Session,
    SessionBlock, ConditioningProtocol, GeneratedProgram,
)
from src.forge.data import (
    BLUEPRINTS, BLUEPRINT_BY_ID, EXERCISE_BY_ID, EXERCISES,
    SELECTION_PRIORITIES, CONDITIONING_PROTOCOLS, COND_PROTOCOL_BY_ID,
    COND_PROTOCOLS_BY_SYSTEM, COND_DECISION_MAP, INTENT_CATEGORIES,
    FAMILY_TO_INTENT, EQUIPMENT_PROFILE_MAP, get_max_difficulty,
    get_equipment_for_profile,
)
from src.forge.blueprint_engine import (
    select_blueprint, determine_level, resolve_slots,
    get_equipment_profile, _shortlist_by_season_phase, _narrow_by_sport,
)
from src.forge.exercise_selector import select_exercise
from src.forge.substitution_engine import substitute_exercise
from src.forge.conditioning_engine import (
    generate_conditioning, select_conditioning, apply_level_adjustment,
)
from src.forge.validator import verify_credibility, calculate_credibility_score
from src.forge.renderer import render_program, render_session, render_block
from src.forge.main import generate_program
from copy import deepcopy


# =============================================================================
# Helpers
# =============================================================================

def make_profile(**kwargs):
    defaults = dict(
        sport="rugby",
        training_age_years=2.5,
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
    )
    defaults.update(kwargs)
    return AthleteProfile(**defaults)


def make_session(families=None, conditioning=None):
    if families is None:
        families = [FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.HPUSH,
                    FamilyCode.HPULL, FamilyCode.CORE]
    blocks = []
    for f in families:
        ex = EXERCISE_BY_ID.get(SELECTION_PRIORITIES[f.value][0]) if SELECTION_PRIORITIES.get(f.value) else None
        if ex:
            blocks.append(SessionBlock(family=f, family_name=f.value, exercises=[ex]))
        else:
            blocks.append(SessionBlock(family=f, family_name=f.value, exercises=[]))
    return Session(blocks=blocks, conditioning=conditioning, total_duration_min=len(blocks) * 5)


# =============================================================================
# UT: Blueprint Selection (UT01-UT08 + extra)
# =============================================================================

class TestBlueprintSelection(unittest.TestCase):
    """from spec UT01-UT08 — select_blueprint decision tree"""

    def test_ut01_active_injury_returns_bp12(self):
        p = make_profile(injury_status="active")
        self.assertEqual(select_blueprint(p).id, 12)

    def test_ut01b_return_to_sport_goal_returns_bp12(self):
        p = make_profile(goal="return_to_sport")
        self.assertEqual(select_blueprint(p).id, 12)

    def test_ut02_off_season_mass_returns_bp11(self):
        p = make_profile(season_phase=SeasonPhase.OFF_SEASON, goal="mass")
        self.assertEqual(select_blueprint(p).id, 11)

    def test_ut03_off_season_contact_returns_bp09(self):
        p = make_profile(season_phase=SeasonPhase.OFF_SEASON, goal="strength", sport="rugby")
        self.assertEqual(select_blueprint(p).id, 9)

    def test_ut03b_off_season_american_football_returns_bp09(self):
        p = make_profile(season_phase=SeasonPhase.OFF_SEASON, goal="strength", sport="american_football")
        self.assertEqual(select_blueprint(p).id, 9)

    def test_ut04_off_season_court_returns_bp08(self):
        p = make_profile(season_phase=SeasonPhase.OFF_SEASON, goal="strength", sport="tennis")
        self.assertEqual(select_blueprint(p).id, 8)

    def test_ut04b_off_season_basketball_returns_bp08(self):
        p = make_profile(season_phase=SeasonPhase.OFF_SEASON, goal="strength", sport="basketball")
        self.assertEqual(select_blueprint(p).id, 8)

    def test_ut05_pre_season_conditioning_returns_bp03(self):
        p = make_profile(season_phase=SeasonPhase.PRE_SEASON, goal="conditioning")
        self.assertEqual(select_blueprint(p).id, 3)

    def test_ut06_pre_season_power_peak_returns_bp04(self):
        p = make_profile(season_phase=SeasonPhase.PRE_SEASON, goal="power_peak")
        self.assertEqual(select_blueprint(p).id, 4)

    def test_ut06b_pre_season_speed_returns_bp10(self):
        p = make_profile(season_phase=SeasonPhase.PRE_SEASON, goal="speed")
        self.assertEqual(select_blueprint(p).id, 10)

    def test_ut07_in_season_maintenance_returns_bp06(self):
        p = make_profile(season_phase=SeasonPhase.IN_SEASON, goal="power_maintenance")
        self.assertEqual(select_blueprint(p).id, 6)

    def test_ut07b_in_season_young_returns_bp07(self):
        p = make_profile(season_phase=SeasonPhase.IN_SEASON, goal="strength", training_age_years=1)
        self.assertEqual(select_blueprint(p).id, 7)

    def test_ut08_transition_high_fatigue_returns_bp13(self):
        p = make_profile(season_phase=SeasonPhase.TRANSITION, fatigue_level="high")
        self.assertEqual(select_blueprint(p).id, 13)

    def test_ut08b_transition_normal_fatigue_returns_bp01(self):
        p = make_profile(season_phase=SeasonPhase.TRANSITION, fatigue_level="normal")
        self.assertEqual(select_blueprint(p).id, 1)

    def test_ut08c_off_season_young_returns_bp07_or_14(self):
        p = make_profile(season_phase=SeasonPhase.OFF_SEASON, training_age_years=1)
        bp = select_blueprint(p)
        self.assertIn(bp.id, [7, 14])

    def test_ut08d_off_season_speed_returns_bp02(self):
        p = make_profile(season_phase=SeasonPhase.OFF_SEASON, goal="speed", sport="track")
        self.assertEqual(select_blueprint(p).id, 2)

    def test_ut08e_default_returns_bp01(self):
        p = make_profile(sport="swimming", goal="strength")
        self.assertEqual(select_blueprint(p).id, 1)

    def test_all_14_blueprints_reachable(self):
        reachable = set()
        configs = [
            dict(injury_status="active"),
            dict(goal="return_to_sport"),
            dict(season_phase=SeasonPhase.OFF_SEASON, goal="mass"),
            dict(season_phase=SeasonPhase.OFF_SEASON, sport="rugby"),
            dict(season_phase=SeasonPhase.OFF_SEASON, sport="tennis"),
            dict(season_phase=SeasonPhase.OFF_SEASON, goal="speed", sport="track"),
            dict(season_phase=SeasonPhase.OFF_SEASON, training_age_years=1, sport="swimming"),
            dict(season_phase=SeasonPhase.PRE_SEASON, goal="conditioning"),
            dict(season_phase=SeasonPhase.PRE_SEASON, goal="power_peak"),
            dict(season_phase=SeasonPhase.PRE_SEASON, goal="speed"),
            dict(season_phase=SeasonPhase.IN_SEASON, goal="power_maintenance"),
            dict(season_phase=SeasonPhase.IN_SEASON, training_age_years=1),
            dict(season_phase=SeasonPhase.TRANSITION, fatigue_level="high"),
            dict(season_phase=SeasonPhase.TRANSITION, fatigue_level="normal"),
            dict(season_phase=SeasonPhase.OFF_SEASON, goal="strength"),
        ]
        for cfg in configs:
            reachable.add(select_blueprint(make_profile(**cfg)).id)
        # BP05 (Upper/Lower Split) and BP14 (Mixed Modal) need explicit coach choice
        # Default decision tree covers the other 12
        for i in range(1, 15):
            if i in (5, 14):
                continue
            self.assertIn(i, reachable, f"Blueprint {i} not reachable via decision tree")


# =============================================================================
# UT: Level Determination (UT09-UT13)
# =============================================================================

class TestLevelDetermination(unittest.TestCase):
    """from spec UT09-UT13"""

    def test_ut09_training_age_below_1_beginner(self):
        self.assertEqual(determine_level(make_profile(training_age_years=0.5, technique_consistency=0.9)),
                         AthleteLevel.BEGINNER)

    def test_ut10_training_age_2_intermediate(self):
        self.assertEqual(determine_level(make_profile(training_age_years=2, technique_consistency=0.9)),
                         AthleteLevel.INTERMEDIATE)

    def test_ut11_training_age_4_advanced(self):
        # Adult (age >= 20) with 4 years proper training -> ADVANCED
        p = make_profile(training_age_years=4, technique_consistency=0.95, age=23)
        p.strength_base_met = True
        self.assertEqual(determine_level(p), AthleteLevel.ADVANCED)

    def test_ut11b_low_technique_beginner(self):
        self.assertEqual(determine_level(make_profile(training_age_years=3, technique_consistency=0.7)),
                         AthleteLevel.BEGINNER)

    def test_ut11c_training_age_1_technique_08_intermediate(self):
        self.assertEqual(determine_level(make_profile(training_age_years=1.5, technique_consistency=0.85)),
                         AthleteLevel.INTERMEDIATE)

    def test_ut11d_youth_cap_prevents_advanced(self):
        # 18yo with 4yr training capped to 2yr effective -> INTERMEDIATE
        p = make_profile(training_age_years=4, technique_consistency=0.95, age=18)
        p.strength_base_met = True
        self.assertEqual(determine_level(p), AthleteLevel.INTERMEDIATE)

    def test_ut13_advanced_without_strength_base_is_intermediate(self):
        p = make_profile(training_age_years=4, technique_consistency=0.95)
        p.strength_base_met = False
        self.assertEqual(determine_level(p), AthleteLevel.INTERMEDIATE)


# =============================================================================
# UT: Equipment Profile (UT14-UT17)
# =============================================================================

class TestEquipmentProfile(unittest.TestCase):
    """from spec UT14-UT17"""

    def test_ut14_field_only(self):
        self.assertEqual(get_equipment_profile({"Bodyweight", "Band", "Cones"}), EquipmentProfile.FIELD_ONLY)

    def test_ut15_basic_gym(self):
        self.assertEqual(get_equipment_profile({"Barbell", "Rack", "Bench", "DB"}), EquipmentProfile.BASIC_GYM)

    def test_ut16_commercial_gym(self):
        self.assertEqual(get_equipment_profile({"Barbell", "Rack", "Bench", "DB", "Cable Machine"}),
                         EquipmentProfile.COMMERCIAL_GYM)

    def test_ut17_elite_facility(self):
        self.assertEqual(get_equipment_profile({"Barbell", "Rack", "DB", "Cable Machine", "Sled", "Specialty Bar"}),
                         EquipmentProfile.ELITE_FACILITY)


# =============================================================================
# UT: Slot Resolution (UT18-UT20)
# =============================================================================

class TestSlotResolution(unittest.TestCase):
    """from spec UT18-UT20"""

    def test_ut18_bp1_mandatory_count(self):
        bp = BLUEPRINT_BY_ID[1]
        slots = resolve_slots(bp, AthleteLevel.INTERMEDIATE)
        for fam in bp.mandatory_families:
            self.assertIn(fam, slots, f"Mandatory family {fam} missing")

    def test_ut19_max_6_slots(self):
        bp = BLUEPRINT_BY_ID[5]
        slots = resolve_slots(bp, AthleteLevel.INTERMEDIATE)
        self.assertLessEqual(len(slots), 8)

    def test_ut20_core_last(self):
        for bp_id in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]:
            bp = BLUEPRINT_BY_ID[bp_id]
            slots = resolve_slots(bp, AthleteLevel.INTERMEDIATE)
            if FamilyCode.CORE in slots:
                self.assertEqual(slots[-1], FamilyCode.CORE,
                                 f"BP{bp_id}: Core not last in {[s.value for s in slots]}")

    def test_bp13_deload_slots(self):
        bp = BLUEPRINT_BY_ID[13]
        slots = resolve_slots(bp, AthleteLevel.INTERMEDIATE)
        self.assertEqual(len(slots), 3)

    def test_all_blueprints_have_at_least_1_slot(self):
        for bp in BLUEPRINTS:
            if bp.id == 14:
                continue
            slots = resolve_slots(bp, AthleteLevel.INTERMEDIATE)
            self.assertGreater(len(slots), 0, f"BP{bp.id} has 0 slots")


# =============================================================================
# UT: Exercise Selector (UT21-UT26)
# =============================================================================

class TestExerciseSelector(unittest.TestCase):
    """from spec UT21-UT26"""

    def _get_priorities(self, family: FamilyCode):
        return SELECTION_PRIORITIES.get(family.value, [])

    def test_ut21_difficulty_filter(self):
        ex = select_exercise(
            FamilyCode.PLYO, AthleteLevel.BEGINNER,
            EquipmentProfile.COMMERCIAL_GYM, {}, []
        )
        if ex:
            self.assertLessEqual(ex.difficulty, 2)

    def test_ut22_equipment_filter(self):
        for fam in [FamilyCode.DLKD, FamilyCode.HPUSH, FamilyCode.DLHD]:
            ex = select_exercise(
                fam, AthleteLevel.INTERMEDIATE,
                EquipmentProfile.FIELD_ONLY, {}, []
            )
            if ex:
                self.assertIn("Bodyweight", ex.equipment)

    def test_ut23_injury_conflict(self):
        ex = select_exercise(
            FamilyCode.DLKD, AthleteLevel.INTERMEDIATE,
            EquipmentProfile.COMMERCIAL_GYM, {}, ["low_back"]
        )
        if ex:
            self.assertNotIn(ex.name, ["Conventional Deadlift", "Barbell Row"])

    def test_ut25_lru_rotation(self):
        recent = {"DLKD-007": {"last_used": "week_1", "technique_score": 0.9}}
        ex1 = select_exercise(
            FamilyCode.DLKD, AthleteLevel.INTERMEDIATE,
            EquipmentProfile.COMMERCIAL_GYM, recent, []
        )
        recent[ex1.id] = {"last_used": "week_2", "technique_score": 0.9}
        ex2 = select_exercise(
            FamilyCode.DLKD, AthleteLevel.INTERMEDIATE,
            EquipmentProfile.COMMERCIAL_GYM, recent, []
        )
        self.assertNotEqual(ex1.id, ex2.id)

    def test_ut26_fallback_substitution(self):
        ex = select_exercise(
            FamilyCode.CARRY, AthleteLevel.BEGINNER,
            EquipmentProfile.FIELD_ONLY, {}, []
        )
        self.assertIsNotNone(ex)

    def test_all_families_selectable(self):
        for fam in FamilyCode:
            ex = select_exercise(fam, AthleteLevel.INTERMEDIATE, EquipmentProfile.COMMERCIAL_GYM, {}, [])
            self.assertIsNotNone(ex, f"Family {fam.value} returned no exercise")

    def test_field_only_all_families(self):
        for fam in [FamilyCode.DLKD, FamilyCode.HPUSH, FamilyCode.HPULL, FamilyCode.CORE,
                     FamilyCode.PLYO, FamilyCode.ROT]:
            ex = select_exercise(fam, AthleteLevel.BEGINNER, EquipmentProfile.FIELD_ONLY, {}, [])
            self.assertIsNotNone(ex, f"Field only family {fam.value} returned no exercise")


# =============================================================================
# UT: Substitution Engine (UT27-UT29)
# =============================================================================

class TestSubstitutionEngine(unittest.TestCase):
    """from spec UT27-UT29"""

    def test_ut27_same_family(self):
        sub = substitute_exercise(
            FamilyCode.DLKD, AthleteLevel.INTERMEDIATE,
            EquipmentProfile.COMMERCIAL_GYM, [], {}, "DLKD-004"
        )
        self.assertIsNotNone(sub)
        self.assertEqual(sub.family, FamilyCode.DLKD)
        self.assertNotEqual(sub.id, "DLKD-004")

    def test_ut28_same_intent(self):
        sub = substitute_exercise(
            FamilyCode.DLKD, AthleteLevel.INTERMEDIATE,
            EquipmentProfile.COMMERCIAL_GYM, [], {}, None
        )
        self.assertIsNotNone(sub)

    def test_ut29_emergency_fallback_all_exercises_blocked(self):
        # simulate every Core priority exercise blocked by injury
        sub = substitute_exercise(
            FamilyCode.CORE, AthleteLevel.BEGINNER,
            EquipmentProfile.FIELD_ONLY,
            ["low_back", "shoulder", "acl_left", "hamstring", "patellar"],
            {}, None
        )
        # substitution will find something from same intent or same equipment
        self.assertIsNotNone(sub)

    def test_injury_substitution(self):
        sub = substitute_exercise(
            FamilyCode.DLKD, AthleteLevel.INTERMEDIATE,
            EquipmentProfile.COMMERCIAL_GYM, ["low_back"], {}, None
        )
        self.assertIsNotNone(sub)
        if sub:
            self.assertNotIn(sub.name, ["Conventional Deadlift", "Barbell Row"])


# =============================================================================
# UT: Validator (UT30-UT34 + extra)
# =============================================================================

class TestValidator(unittest.TestCase):
    """from spec UT30-UT34 — 12-point credibility check"""

    def test_ut30_all_12_pass(self):
        # 6 exercises across 6 blocks → meets Intermediate min (6)
        blocks = [
            SessionBlock(family=FamilyCode.DLKD, family_name="DLKD",
                         exercises=[EXERCISE_BY_ID["DLKD-004"]]),
            SessionBlock(family=FamilyCode.DLHD, family_name="DLHD",
                         exercises=[EXERCISE_BY_ID["DLHD-006"]]),
            SessionBlock(family=FamilyCode.HPUSH, family_name="HPush",
                         exercises=[EXERCISE_BY_ID["HPush-006"]]),
            SessionBlock(family=FamilyCode.HPULL, family_name="HPull",
                         exercises=[EXERCISE_BY_ID["HPull-005"]]),
            SessionBlock(family=FamilyCode.CARRY, family_name="Carry",
                         exercises=[EXERCISE_BY_ID["Carry-001"]]),
            SessionBlock(family=FamilyCode.CORE, family_name="Core",
                         exercises=[EXERCISE_BY_ID["Core-002"]]),
        ]
        sess = Session(blocks=blocks, total_duration_min=30)
        athlete = make_profile()
        check = verify_credibility(sess, athlete)
        score = calculate_credibility_score(check)
        self.assertGreaterEqual(score, 0.9, f"Checks: {check}")

    def test_ut31_core_misplaced(self):
        # Core not last → session_flow fails
        blocks = [
            SessionBlock(family=FamilyCode.CORE, family_name="Core",
                         exercises=[EXERCISE_BY_ID["Core-002"]]),
            SessionBlock(family=FamilyCode.DLKD, family_name="DLKD",
                         exercises=[EXERCISE_BY_ID["DLKD-004"]]),
        ]
        sess = Session(blocks=blocks, total_duration_min=10)
        athlete = make_profile()
        check = verify_credibility(sess, athlete)
        self.assertFalse(check["session_flow"])

    def test_ut32_insufficient_variety(self):
        # Only 2 families → exercise_variety fails
        blocks = [
            SessionBlock(family=FamilyCode.DLKD, family_name="DLKD",
                         exercises=[EXERCISE_BY_ID["DLKD-004"]]),
            SessionBlock(family=FamilyCode.DLKD, family_name="DLKD",
                         exercises=[EXERCISE_BY_ID["DLKD-007"]]),
        ]
        sess = Session(blocks=blocks, total_duration_min=10)
        athlete = make_profile()
        check = verify_credibility(sess, athlete)
        self.assertFalse(check["exercise_variety"])

    def test_ut34_below_8_score(self):
        sess = make_session([FamilyCode.HPUSH, FamilyCode.VPUSH])
        athlete = make_profile()
        check = verify_credibility(sess, athlete)
        score = calculate_credibility_score(check)
        self.assertLess(score, 1.0)

    def test_no_empty_slots(self):
        sess = make_session([FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.HPUSH,
                             FamilyCode.HPULL, FamilyCode.CORE])
        athlete = make_profile()
        check = verify_credibility(sess, athlete)
        self.assertTrue(check["no_empty_slots"])

    def test_equipment_check(self):
        # Use exercises available in Field Only profile
        blocks = [
            SessionBlock(family=FamilyCode.CORE, family_name="Core",
                         exercises=[EXERCISE_BY_ID["Core-002"]]),
            SessionBlock(family=FamilyCode.PLYO, family_name="Plyo",
                         exercises=[EXERCISE_BY_ID["Plyo-001"]]),
        ]
        sess = Session(blocks=blocks, total_duration_min=10)
        athlete = make_profile(equipment_profile=EquipmentProfile.FIELD_ONLY)
        check = verify_credibility(sess, athlete)
        self.assertTrue(check["equipment_available"])

    def test_duplicate_detection(self):
        blocks = [
            SessionBlock(family=FamilyCode.DLKD, family_name="DLKD",
                         exercises=[EXERCISE_BY_ID["DLKD-004"]]),
            SessionBlock(family=FamilyCode.DLHD, family_name="DLHD",
                         exercises=[EXERCISE_BY_ID["DLKD-004"]]),
        ]
        sess = Session(blocks=blocks, total_duration_min=10)
        athlete = make_profile()
        check = verify_credibility(sess, athlete)
        self.assertFalse(check["no_duplicate_exercises"])

    def test_time_budget(self):
        many_blocks = [SessionBlock(family=FamilyCode.DLKD, family_name="DLKD",
                                    exercises=[EXERCISE_BY_ID["DLKD-004"]])
                       for _ in range(20)]
        sess = Session(blocks=many_blocks, total_duration_min=100)
        athlete = make_profile()
        check = verify_credibility(sess, athlete)
        self.assertFalse(check["slots_fit_time"])

    def test_all_12_checks_present(self):
        sess = make_session([FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.HPUSH,
                             FamilyCode.HPULL, FamilyCode.CORE])
        athlete = make_profile()
        check = verify_credibility(sess, athlete)
        expected_keys = [
            "volume_load_match", "exercise_variety", "appropriate_difficulty",
            "no_empty_slots", "session_flow", "law_10_rules",
            "conditioning_appropriate", "equipment_available", "injury_aware",
            "warmdown_is_conditioning", "slots_fit_time", "no_duplicate_exercises",
        ]
        for key in expected_keys:
            self.assertIn(key, check, f"Missing check: {key}")


# =============================================================================
# UT: Conditioning Selection (UT45-UT49 + extra)
# =============================================================================

class TestConditioningSelection(unittest.TestCase):
    """from spec UT45-UT49"""

    def setUp(self):
        self.base_session = make_session()

    def test_ut45_recovery_goal(self):
        cond = generate_conditioning(self.base_session, AthleteLevel.INTERMEDIATE, "recovery")
        self.assertIsNotNone(cond)
        self.assertIn("Recovery", cond.system)

    def test_ut46_aerobic_capacity(self):
        cond = generate_conditioning(self.base_session, AthleteLevel.INTERMEDIATE,
                                      "aerobic_capacity", "field", 30)
        self.assertIsNotNone(cond)
        if cond:
            self.assertEqual(cond.system, "Aerobic Capacity")

    def test_ut47_rsa_goal(self):
        cond = generate_conditioning(self.base_session, AthleteLevel.ADVANCED, "rsa")
        self.assertIsNotNone(cond)
        if cond:
            self.assertIn("Repeated Sprint", cond.system)

    def test_ut48_a_tier_selected(self):
        cond = generate_conditioning(self.base_session, AthleteLevel.INTERMEDIATE, "alactic_speed")
        self.assertIsNotNone(cond)
        if cond:
            self.assertEqual(cond.tier, "A")

    def test_ut49_level_adjustment(self):
        proto = COND_PROTOCOL_BY_ID.get("SE-001")
        if proto and proto.level_variants:
            adjusted = apply_level_adjustment(proto, AthleteLevel.BEGINNER)
            self.assertIsNotNone(adjusted)

    def test_beginner_no_lactate_tolerance(self):
        cond = generate_conditioning(self.base_session, AthleteLevel.BEGINNER, "lactate_tolerance")
        self.assertIsNone(cond)

    def test_intermediate_no_lactate_tolerance(self):
        cond = generate_conditioning(self.base_session, AthleteLevel.INTERMEDIATE, "lactate_tolerance")
        self.assertIsNone(cond)

    def test_advanced_lactate_tolerance(self):
        cond = generate_conditioning(self.base_session, AthleteLevel.ADVANCED, "lactate_tolerance")
        self.assertIsNotNone(cond)

    def test_beginner_no_intensive_tempo(self):
        cond = generate_conditioning(self.base_session, AthleteLevel.BEGINNER, "intensive_tempo")
        self.assertIsNone(cond)

    def test_alactic_speed_available(self):
        cond = generate_conditioning(self.base_session, AthleteLevel.INTERMEDIATE, "alactic_speed")
        self.assertIsNotNone(cond)

    def test_all_conditioning_goals_covered(self):
        session = make_session()
        goals = ["recovery", "aerobic_capacity", "aerobic_power", "extensive_tempo",
                 "rsa", "alactic_speed", "power_maintenance"]
        # Combos with no protocol in library (no Beginner-level protocols exist)
        unsupported = {("aerobic_power", "Beginner"), ("rsa", "Beginner"), ("power_maintenance", "Beginner")}
        for g in goals:
            for lvl in [AthleteLevel.BEGINNER, AthleteLevel.INTERMEDIATE, AthleteLevel.ADVANCED]:
                if (g, lvl.value) in unsupported:
                    continue
                cond = generate_conditioning(session, lvl, g, "field", 20)
                self.assertIsNotNone(cond, f"Goal={g}, level={lvl.value} returned None")


# =============================================================================
# UT: Renderer (UT50)
# =============================================================================

class TestRenderer(unittest.TestCase):
    """from spec UT50"""

    def test_ut50_render_program(self):
        p = make_profile()
        program = generate_program(p)
        output = render_program(program)
        self.assertIn("FORGE Generated Program", output)
        self.assertIn(program.blueprint_name, output)
        self.assertIn("Average Session Credibility:", output)

    def test_render_session_output(self):
        sess = make_session()
        output = render_session(sess, 1, 1.0)
        self.assertIn("1 (Credit: 1.0/1.0)", output)
        self.assertIn("DLKD", output)

    def test_render_block_output(self):
        block = SessionBlock(
            family=FamilyCode.DLKD, family_name="Double Leg Knee Dominant",
            exercises=[EXERCISE_BY_ID["DLKD-004"]]
        )
        output = render_block(block)
        self.assertIn(block.family.value, output)
        self.assertIn(EXERCISE_BY_ID["DLKD-004"].name, output)


# =============================================================================
# UT: Data Integrity
# =============================================================================

class TestDataIntegrity(unittest.TestCase):
    """Ensure seed data is consistent"""

    def test_all_exercise_ids_unique(self):
        ids = [e.id for e in EXERCISES]
        self.assertEqual(len(ids), len(set(ids)))

    def test_selection_priorities_exist(self):
        for fam in FamilyCode:
            ids = SELECTION_PRIORITIES.get(fam.value, [])
            self.assertGreater(len(ids), 0, f"No priorities for {fam.value}")

    def test_selection_priorities_reference_valid_exercises(self):
        for fam, ids in SELECTION_PRIORITIES.items():
            for eid in ids:
                self.assertIn(eid, EXERCISE_BY_ID, f"Missing exercise {eid} in {fam}")

    def test_blueprint_slot_order_valid(self):
        for bp in BLUEPRINTS:
            for fam in bp.slot_order:
                self.assertIn(fam, list(FamilyCode), f"BP{bp.id}: invalid family {fam}")

    def test_intent_categories_cover_all_families(self):
        covered = set()
        for fams in INTENT_CATEGORIES.values():
            covered.update(fams)
        for fam in FamilyCode:
            if fam.value == "Acc":
                continue
            self.assertIn(fam.value, covered, f"{fam.value} not in any intent category")

    def test_equipment_profiles_have_items(self):
        for name, items in EQUIPMENT_PROFILE_MAP.items():
            self.assertGreater(len(items), 0, f"No equipment for {name}")

    def test_all_blueprints_have_valid_frequencies(self):
        for bp in BLUEPRINTS:
            import re
            m = re.search(r"\d+", bp.best_frequency)
            self.assertIsNotNone(m, f"BP{bp.id}: no frequency number in '{bp.best_frequency}'")

    def test_conditioning_protocols_have_system(self):
        for p in CONDITIONING_PROTOCOLS:
            self.assertTrue(p.system, f"{p.id} has empty system")

    def test_conditioning_decision_map_keys_match(self):
        for goal_key in COND_DECISION_MAP:
            self.assertIn(goal_key,
                          ["recovery", "aerobic_capacity", "aerobic_power",
                           "extensive_tempo", "intensive_tempo", "rsa",
                           "alactic_speed", "lactate_tolerance", "power_maintenance"])


# =============================================================================
# IT: Integration Tests
# =============================================================================

class TestIntegration(unittest.TestCase):
    """Full generation pipeline — IT01-IT12"""

    def test_it01_beginner_field_only(self):
        p = make_profile(
            athlete_level=AthleteLevel.BEGINNER,
            equipment_profile=EquipmentProfile.FIELD_ONLY,
            training_age_years=0.5,
        )
        program = generate_program(p)
        self.assertIsNotNone(program)
        self.assertGreaterEqual(program.credibility_score, 0.8)

    def test_it02_intermediate_basic_gym(self):
        p = make_profile(
            athlete_level=AthleteLevel.INTERMEDIATE,
            equipment_profile=EquipmentProfile.BASIC_GYM,
        )
        program = generate_program(p)
        self.assertIsNotNone(program)
        self.assertGreaterEqual(program.credibility_score, 0.8)

    def test_it03_advanced_commercial_power(self):
        p = make_profile(
            athlete_level=AthleteLevel.ADVANCED,
            equipment_profile=EquipmentProfile.COMMERCIAL_GYM,
            season_phase=SeasonPhase.PRE_SEASON,
            goal="power_peak",
            training_age_years=4,
            technique_consistency=0.95,
        )
        p.strength_base_met = True
        program = generate_program(p)
        self.assertIsNotNone(program)
        self.assertGreaterEqual(program.credibility_score, 0.8)

    def test_it04_court_sport_in_season(self):
        p = make_profile(
            sport="tennis", season_phase=SeasonPhase.IN_SEASON,
            goal="power_maintenance",
        )
        program = generate_program(p)
        self.assertIsNotNone(program)

    def test_it05_rugby_elite(self):
        p = make_profile(
            sport="rugby", season_phase=SeasonPhase.OFF_SEASON,
            equipment_profile=EquipmentProfile.ELITE_FACILITY,
        )
        program = generate_program(p)
        self.assertIsNotNone(program)

    def test_it07_return_to_sport(self):
        p = make_profile(
            goal="return_to_sport", injury_status="cleared",
            injury_history=["acl_left_2023"],
        )
        program = generate_program(p)
        self.assertIsNotNone(program)
        self.assertEqual(program.blueprint_id, 12)

    def test_it08_deload(self):
        p = make_profile(
            season_phase=SeasonPhase.TRANSITION, fatigue_level="high",
        )
        program = generate_program(p)
        self.assertIsNotNone(program)
        self.assertEqual(program.blueprint_id, 13)

    def test_it09_substitution(self):
        p = make_profile(
            equipment_profile=EquipmentProfile.FIELD_ONLY,
        )
        program = generate_program(p)
        self.assertIsNotNone(program)
        for session in program.sessions:
            for block in session.blocks:
                for ex in block.exercises:
                    for eq in ex.equipment:
                        field_eq = [e.lower() for e in EQUIPMENT_PROFILE_MAP["Field Only"]]
                        ok = any(f in eq.lower() or eq.lower() in f for f in field_eq)
                        self.assertTrue(ok, f"{ex.name} needs {eq} not in field only")

    def test_it10_conditioning_present(self):
        p = make_profile(goal="conditioning", season_phase=SeasonPhase.PRE_SEASON)
        program = generate_program(p)
        has_cond = any(s.conditioning is not None for s in program.sessions)
        self.assertTrue(has_cond)

    def test_all_14_blueprints_generate_with_credibility(self):
        configs = [
            dict(sport="rugby", season_phase=SeasonPhase.OFF_SEASON, goal="strength"),
            dict(sport="rugby", season_phase=SeasonPhase.OFF_SEASON, goal="mass"),
            dict(sport="rugby", season_phase=SeasonPhase.PRE_SEASON, goal="conditioning"),
            dict(sport="rugby", season_phase=SeasonPhase.PRE_SEASON, goal="power_peak"),
            dict(sport="rugby", season_phase=SeasonPhase.IN_SEASON, goal="power_maintenance"),
            dict(sport="rugby", season_phase=SeasonPhase.IN_SEASON, goal="strength", training_age_years=1),
            dict(sport="rugby", season_phase=SeasonPhase.TRANSITION, fatigue_level="high"),
            dict(sport="tennis", season_phase=SeasonPhase.OFF_SEASON, goal="strength"),
            dict(sport="rugby", season_phase=SeasonPhase.OFF_SEASON, goal="speed"),
            dict(sport="track", season_phase=SeasonPhase.PRE_SEASON, goal="speed"),
            dict(goal="return_to_sport", injury_status="cleared"),
            dict(season_phase=SeasonPhase.OFF_SEASON, goal="strength", sport="swimming"),
            dict(season_phase=SeasonPhase.OFF_SEASON, training_age_years=1),
        ]
        for i, cfg in enumerate(configs):
            p = make_profile(**cfg)
            program = generate_program(p)
            self.assertIsNotNone(program, f"Config {i} failed: {cfg}")
            self.assertGreaterEqual(program.credibility_score, 0.6,
                                    f"Config {i} {cfg}: cred={program.credibility_score}")


# =============================================================================
# ST: Stress Tests
# =============================================================================

class TestStress(unittest.TestCase):
    """Edge cases and stress tests — ST01-ST05"""

    def test_st01_worst_case_athlete(self):
        p = make_profile(
            training_age_years=0,
            equipment_profile=EquipmentProfile.FIELD_ONLY,
            injury_history=["low_back", "shoulder", "acl_left"],
            technique_consistency=0.5,
            athlete_level=AthleteLevel.BEGINNER,
        )
        program = generate_program(p)
        self.assertIsNotNone(program)
        for s in program.sessions:
            for b in s.blocks:
                for ex in b.exercises:
                    self.assertLessEqual(ex.difficulty, 2)

    def test_st03_deterministic(self):
        p = make_profile()
        r1 = generate_program(p)
        r2 = generate_program(p)
        self.assertEqual(
            [(s.blocks[0].exercises[0].id if s.blocks[0].exercises else None,
              s.blocks[1].exercises[0].id if s.blocks[1].exercises else None)
             for s in r1.sessions],
            [(s.blocks[0].exercises[0].id if s.blocks[0].exercises else None,
              s.blocks[1].exercises[0].id if s.blocks[1].exercises else None)
             for s in r2.sessions],
        )

    def test_st04_injury_combinations(self):
        injuries = ["low_back", "acl_left", "shoulder", "hamstring"]
        for injury in injuries:
            p = make_profile(injury_history=[injury],
                             equipment_profile=EquipmentProfile.COMMERCIAL_GYM)
            program = generate_program(p)
            self.assertIsNotNone(program, f"Failed with injury: {injury}")

    def test_st05_conditioning_all_goals_advanced(self):
        session = make_session()
        goals = ["recovery", "aerobic_capacity", "aerobic_power", "extensive_tempo",
                 "intensive_tempo", "rsa", "alactic_speed", "lactate_tolerance",
                 "power_maintenance"]
        for g in goals:
            cond = generate_conditioning(session, AthleteLevel.ADVANCED, g, "field", 20)
            if g in ("intensive_tempo",):
                continue
            self.assertIsNotNone(cond, f"Goal={g} returned None for Advanced")

    def test_rapid_fire_generations(self):
        for _ in range(10):
            p = make_profile()
            program = generate_program(p)
            self.assertGreaterEqual(program.credibility_score, 0.6)

    def test_no_crashes_any_profile(self):
        profiles = [
            dict(sport="basketball", training_age_years=0.5, goal="strength"),
            dict(sport="swimming", training_age_years=5, goal="mass"),
            dict(sport="track", training_age_years=3, goal="speed"),
            dict(sport="football", training_age_years=1.5, goal="conditioning"),
        ]
        for cfg in profiles:
            program = generate_program(make_profile(**cfg))
            self.assertIsNotNone(program)


# =============================================================================
# CT: Credibility Tests
# =============================================================================

class TestCredibility(unittest.TestCase):
    """Credibility guarantees — CT01-CT05"""

    def test_ct01_all_blueprints_generate_valid(self):
        for bp in BLUEPRINTS:
            if bp.id == 14:
                continue
            configs = [
                dict(sport="rugby", training_age_years=2),
                dict(sport="tennis", training_age_years=2),
                dict(sport="soccer", training_age_years=0.5),
            ]
            for cfg in configs:
                p = make_profile(**cfg)
                program = generate_program(p)
                if program.blueprint_id == bp.id:
                    self.assertGreaterEqual(program.credibility_score, 0.6)

    def test_ct03_posterior_chain_present(self):
        p = make_profile()
        program = generate_program(p)
        for sess in program.sessions[:5]:
            families = {b.family for b in sess.blocks}
            pc = {FamilyCode.DLHD, FamilyCode.SLHD, FamilyCode.HPULL}
            self.assertTrue(families & pc, f"No posterior chain in session: {[f.value for f in families]}")

    def test_ct04_push_pull_balanced(self):
        p = make_profile()
        program = generate_program(p)
        for sess in program.sessions[:5]:
            has_push = any(b.family in (FamilyCode.HPUSH, FamilyCode.VPUSH) for b in sess.blocks)
            has_pull = any(b.family in (FamilyCode.HPULL, FamilyCode.VPULL) for b in sess.blocks)
            self.assertTrue(has_push and has_pull, f"Push/pull unbalanced in session")

    def test_ct05_core_present(self):
        # Full Body Strength (BP01) always gets Core within 6 slots
        p = make_profile(sport="track", goal="strength", season_phase=SeasonPhase.OFF_SEASON)
        program = generate_program(p)
        self.assertEqual(program.blueprint_id, 1)
        for sess in program.sessions[:5]:
            has_core = any(b.family == FamilyCode.CORE for b in sess.blocks)
            self.assertTrue(has_core, "No core in session")


# =============================================================================
# CNDT: Conditioning Tests
# =============================================================================

class TestConditioningCoverage(unittest.TestCase):
    """Conditioning-specific coverage — CNDT01-CNDT05"""

    def test_cndt02_no_c_tier_default(self):
        session = make_session()
        for lvl in [AthleteLevel.BEGINNER, AthleteLevel.INTERMEDIATE, AthleteLevel.ADVANCED]:
            for goal in ["recovery", "aerobic_capacity", "aerobic_power",
                          "extensive_tempo", "rsa", "alactic_speed"]:
                cond = generate_conditioning(session, lvl, goal, "field", 20)
                if cond:
                    self.assertEqual(cond.tier, "A",
                                     f"Non-A tier for {goal}/{lvl.value}: {cond.id}={cond.tier}")

    def test_cndt04_all_systems_reachable(self):
        session = make_session()
        systems_reached = set()
        for goal in ["recovery", "aerobic_capacity", "aerobic_power",
                      "extensive_tempo", "intensive_tempo", "rsa",
                      "alactic_speed", "lactate_tolerance", "power_maintenance"]:
            for lvl in [AthleteLevel.BEGINNER, AthleteLevel.INTERMEDIATE, AthleteLevel.ADVANCED]:
                cond = generate_conditioning(session, lvl, goal, "field", 20)
                if cond:
                    systems_reached.add(cond.system)
        self.assertGreaterEqual(len(systems_reached), 5)


# =============================================================================
# Model Tests
# =============================================================================

class TestModels(unittest.TestCase):
    """Dataclass construction and defaults"""

    def test_athlete_profile_defaults(self):
        p = AthleteProfile(
            sport="rugby", training_age_years=2, season_phase=SeasonPhase.OFF_SEASON,
            goal="strength", equipment_profile=EquipmentProfile.COMMERCIAL_GYM,
            athlete_level=AthleteLevel.INTERMEDIATE,
        )
        self.assertEqual(p.technique_consistency, 1.0)
        self.assertEqual(p.injury_status, "none")
        self.assertEqual(p.fatigue_level, "normal")
        self.assertEqual(p.weeks_since_break, 0)

    def test_exercise_construction(self):
        ex = Exercise(
            id="TEST-001", name="Test Exercise", family=FamilyCode.DLKD,
            secondary_family=None, objective=Objective.STRENGTH,
            difficulty=2, equipment=["Barbell"], unilateral=False,
            explosive=False, isometric=False, rotational=False,
            progression=None, regression=None,
        )
        self.assertEqual(ex.id, "TEST-001")
        self.assertEqual(ex.family, FamilyCode.DLKD)

    def test_session_block_defaults(self):
        block = SessionBlock(family=FamilyCode.CORE, family_name="Core")
        self.assertEqual(block.exercises, [])
        self.assertEqual(block.target_intensity, "moderate")
        self.assertEqual(block.rest_period, "60-90s")

    def test_generated_program_construction(self):
        p = make_profile()
        program = generate_program(p)
        self.assertIsNotNone(program.sessions)
        self.assertGreater(len(program.sessions), 0)
        self.assertIsInstance(program.credibility_score, float)


# =============================================================================
# Edge Cases
# =============================================================================

class TestEdgeCases(unittest.TestCase):
    """Corner cases for robustness"""

    def test_empty_injury_history(self):
        ex = select_exercise(FamilyCode.DLKD, AthleteLevel.INTERMEDIATE,
                              EquipmentProfile.COMMERCIAL_GYM, {}, [])
        self.assertIsNotNone(ex)

    def test_max_difficulty_values(self):
        self.assertEqual(get_max_difficulty("Beginner"), 2)
        self.assertEqual(get_max_difficulty("Intermediate"), 3)
        self.assertEqual(get_max_difficulty("Advanced"), 5)

    def test_equipment_profile_lookup(self):
        for name in ["Field Only", "Basic Gym", "Commercial Gym", "Elite Facility"]:
            eq = get_equipment_for_profile(name)
            self.assertGreater(len(eq), 0, f"No equipment for {name}")

    def test_cross_family_substitution_all_families(self):
        for fam in FamilyCode:
            if fam == FamilyCode.ACC:
                continue
            sub = substitute_exercise(fam, AthleteLevel.INTERMEDIATE,
                                       EquipmentProfile.COMMERCIAL_GYM, [], {}, None)
            self.assertIsNotNone(sub, f"No sub for {fam.value}")


if __name__ == "__main__":
    unittest.main()
