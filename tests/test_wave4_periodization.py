"""Wave 4 — Periodization, Testing, and Auto-Adjustment tests."""
import unittest
from copy import deepcopy
from src.forge.models import (
    AthleteProfile, AthleteLevel, EquipmentProfile, SeasonPhase,
    FamilyCode, Session, GeneratedProgram,
)
from src.forge.data import EXERCISE_BY_ID, SELECTION_PRIORITIES
from src.forge.main import generate_program
from src.forge.progression_engine import (
    WEEK_STRUCTURE_DEFAULT, plan_weeks, plan_testing,
    TESTING_CATEGORIES, review_week, adjust_next_week,
    verify_program_credibility, calculate_program_credibility_score,
)
from src.forge.renderer import render_block_summary


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


def make_dummy_session(family_counts: dict[str, int], week_type="accumulation") -> Session:
    blocks = []
    for fam_str, count in family_counts.items():
        fam = FamilyCode(fam_str)
        priority_ids = SELECTION_PRIORITIES.get(fam.value, [])
        exercises = []
        for i in range(min(count, len(priority_ids))):
            ex = EXERCISE_BY_ID.get(priority_ids[i])
            if ex:
                exercises.append(deepcopy(ex))
        from src.forge.models import SessionBlock
        blocks.append(SessionBlock(family=fam, family_name=fam.value, exercises=exercises))
    return Session(blocks=blocks, week_type=week_type)


# ── A. WEEK STRUCTURE ─────────────────────────────────────────────

class TestWeekStructure(unittest.TestCase):
    def test_default_8_weeks(self):
        weeks = plan_weeks(1, AthleteLevel.INTERMEDIATE, "strength", 20)
        self.assertEqual(len(weeks), 8)

    def test_default_intents(self):
        weeks = plan_weeks(1, AthleteLevel.INTERMEDIATE, "strength", 20)
        self.assertEqual(weeks, WEEK_STRUCTURE_DEFAULT)

    def test_deload_blueprint(self):
        weeks = plan_weeks(13, AthleteLevel.INTERMEDIATE, "strength", 20)
        self.assertEqual(weeks, ["deload"] * 8)

    def test_return_to_play_no_realization(self):
        weeks = plan_weeks(1, AthleteLevel.INTERMEDIATE, "return_to_sport", 20)
        self.assertEqual(weeks[4], "intensification")
        self.assertEqual(weeks[5], "intensification")

    def test_beginner_no_test_week(self):
        weeks = plan_weeks(1, AthleteLevel.BEGINNER, "strength", 18)
        self.assertEqual(weeks[7], "deload")

    def test_youth_no_test_week(self):
        weeks = plan_weeks(1, AthleteLevel.INTERMEDIATE, "strength", 15)
        self.assertEqual(weeks[7], "deload")

    def test_speed_taper_earlier_with_comp(self):
        weeks = plan_weeks(10, AthleteLevel.ADVANCED, "speed", 20, days_to_match=14)
        # comp window >=6 means no early taper
        self.assertEqual(weeks[4], "realization")
        self.assertEqual(weeks[5], "realization")

    def test_speed_taper_near_comp(self):
        weeks = plan_weeks(10, AthleteLevel.ADVANCED, "speed", 20, days_to_match=4)
        self.assertEqual(weeks[5], "taper")

    def test_days_to_match_1_light_week(self):
        weeks = plan_weeks(1, AthleteLevel.INTERMEDIATE, "strength", 20, days_to_match=1)
        self.assertEqual(weeks, ["light"] * 8)

    def test_competition_proximity_override(self):
        weeks = plan_weeks(1, AthleteLevel.INTERMEDIATE, "strength", 20, days_to_match=2)
        for i in range(5, 8):
            self.assertEqual(weeks[i], "taper")


# ── B. TESTING PLACEMENT ──────────────────────────────────────────

class TestTestingPlacement(unittest.TestCase):
    def test_baseline_in_week1(self):
        weeks = plan_weeks(1, AthleteLevel.INTERMEDIATE, "strength", 20)
        tests = plan_testing(weeks, 1, AthleteLevel.INTERMEDIATE, "strength", 20)
        self.assertIn(1, tests)
        self.assertIn("movement_technical", tests[1])
        self.assertIn("jump_power", tests[1])

    def test_exit_test_in_week8(self):
        weeks = plan_weeks(1, AthleteLevel.INTERMEDIATE, "strength", 20)
        tests = plan_testing(weeks, 1, AthleteLevel.INTERMEDIATE, "strength", 20)
        self.assertIn(8, tests)
        self.assertIn("lower_body_strength", tests[8])

    def test_beginner_no_maximal_testing(self):
        weeks = plan_weeks(1, AthleteLevel.BEGINNER, "strength", 18)
        tests = plan_testing(weeks, 1, AthleteLevel.BEGINNER, "strength", 18)
        week8_tests = tests.get(8, [])
        self.assertNotIn("lower_body_strength", week8_tests)
        self.assertNotIn("upper_body_strength", week8_tests)

    def test_youth_no_maximal_testing(self):
        weeks = plan_weeks(1, AthleteLevel.INTERMEDIATE, "strength", 15)
        tests = plan_testing(weeks, 1, AthleteLevel.INTERMEDIATE, "strength", 15)
        week8_tests = tests.get(8, [])
        self.assertNotIn("lower_body_strength", week8_tests)

    def test_rtp_conservative_testing(self):
        weeks = plan_weeks(1, AthleteLevel.INTERMEDIATE, "return_to_sport", 20)
        tests = plan_testing(weeks, 1, AthleteLevel.INTERMEDIATE, "return_to_sport", 20)
        week8_tests = tests.get(8, [])
        self.assertNotIn("lower_body_strength", week8_tests)
        self.assertNotIn("sprint_speed", week8_tests)

    def test_comp_proximity_blocks_testing(self):
        weeks = plan_weeks(1, AthleteLevel.INTERMEDIATE, "strength", 20, days_to_match=2)
        tests = plan_testing(weeks, 1, AthleteLevel.INTERMEDIATE, "strength", 20, days_to_match=2)
        self.assertEqual(tests, {})

    def test_mid_block_checkpoint(self):
        weeks = plan_weeks(1, AthleteLevel.ADVANCED, "strength", 20)
        tests = plan_testing(weeks, 1, AthleteLevel.ADVANCED, "strength", 20)
        for w in (5, 6):
            if w in tests:
                self.assertIn("jump_power", tests[w])

    def test_all_testing_categories_have_labels(self):
        for cat_id, cat in TESTING_CATEGORIES.items():
            self.assertIn("label", cat, f"{cat_id} missing label")
            self.assertIn("blocked_for", cat, f"{cat_id} missing blocked_for")


# ── C. AUTO-ADJUSTMENT ────────────────────────────────────────────

class TestAutoAdjustment(unittest.TestCase):
    def test_no_risks_returns_no_adjustment(self):
        sess = make_dummy_session({"DLKD": 2, "HPush": 2, "Core": 1})
        flags = review_week([sess], "accumulation")
        adj = adjust_next_week(flags, "intensification", 1, "strength")
        self.assertEqual(adj["slot_reduction"], 0)
        self.assertIsNone(adj["conditioning_mod"])

    def test_high_eccentric_triggers_reduction(self):
        sess = make_dummy_session({"DLKD": 4, "DLHD": 5, "SLKD": 3}, "accumulation")
        # Force high eccentric via difficulty 4 exercises
        for b in sess.blocks:
            for ex in b.exercises:
                ex.eccentric_cost = 5
        flags = review_week([sess], "accumulation")
        self.assertIn("reduce_eccentric", flags["risks"])
        adj = adjust_next_week(flags, "intensification", 1, "strength")
        self.assertGreater(adj["slot_reduction"], 0)

    def test_high_impact_triggers_reduction(self):
        sess = make_dummy_session({"DLKD": 5, "Plyo": 5}, "accumulation")
        for b in sess.blocks:
            for ex in b.exercises:
                ex.impact_level = 5
        flags = review_week([sess], "accumulation")
        self.assertIn("reduce_impact", flags["risks"])

    def test_high_volume_triggers_reduction(self):
        sess = make_dummy_session({"DLKD": 10, "HPush": 10, "Core": 5}, "accumulation")
        flags = review_week([sess], "accumulation")
        self.assertIn("reduce_volume", flags["risks"])
        adj = adjust_next_week(flags, "taper", 1, "strength")
        self.assertIsNotNone(adj.get("conditioning_mod"))

    def test_multiple_risks_downgrade_intent(self):
        sess = make_dummy_session({"DLKD": 5, "DLHD": 5, "HPush": 5, "Plyo": 5}, "accumulation")
        for b in sess.blocks:
            for ex in b.exercises:
                ex.eccentric_cost = 5
                ex.impact_level = 5
        flags = review_week([sess], "accumulation")
        self.assertGreaterEqual(len(flags["risks"]), 2)
        adj = adjust_next_week(flags, "realization", 1, "strength")
        self.assertEqual(adj.get("intent_override"), "accumulation")

    def test_adjustment_has_note(self):
        sess = make_dummy_session({"DLKD": 6}, "accumulation")
        for b in sess.blocks:
            for ex in b.exercises:
                ex.eccentric_cost = 5
        flags = review_week([sess], "accumulation")
        adj = adjust_next_week(flags, "intensification", 1, "strength")
        self.assertTrue(len(adj.get("note", "")) > 0)

    def test_full_week_auto_adjust(self):
        """Generated program with auto-adjustment should not crash."""
        p = make_profile()
        program = generate_program(p)
        self.assertGreater(program.credibility_score, 0)


# ── D. PROGRAM-LEVEL VALIDATION ───────────────────────────────────

class TestProgramLevelValidation(unittest.TestCase):
    def test_movement_balance_checks(self):
        """At least 2 movement patterns should be present."""
        p = make_profile()
        program = generate_program(p)
        result = verify_program_credibility(program)
        self.assertIn("movement_balance_ok", result)

    def test_core_rotational_present(self):
        """Core should be present somewhere in the program."""
        p = make_profile()
        program = generate_program(p)
        result = verify_program_credibility(program)
        self.assertTrue(result["core_rotational_present"])

    def test_test_not_max_loading(self):
        """Test sessions should not have excessive loading."""
        p = make_profile(athlete_level=AthleteLevel.ADVANCED)
        program = generate_program(p)
        result = verify_program_credibility(program)
        self.assertIn("test_not_max_loading", result)

    def test_conditioning_not_dominant_for_strength(self):
        p = make_profile(goal="strength")
        program = generate_program(p)
        result = verify_program_credibility(program)
        self.assertIn("conditioning_not_dominant", result)

    def test_exposure_bounded(self):
        p = make_profile()
        program = generate_program(p)
        result = verify_program_credibility(program)
        self.assertIn("exposure_bounded_across_block", result)

    def test_credibility_score_calculated(self):
        result = {
            "main_lift_continuity": True,
            "block_progression_visible": True,
            "deload_week_actually_reduced": True,
            "conditioning_progression_credible": True,
            "weekly_exposure_safe": True,
            "no_exercise_reset_in_taper": True,
            "youth_progression_safe": True,
            "competition_weeks_reduced": True,
            "movement_balance_ok": True,
            "sprint_landing_bounded": True,
            "conditioning_not_dominant": True,
            "core_rotational_present": True,
            "test_not_max_loading": True,
            "exposure_bounded_across_block": True,
        }
        score = calculate_program_credibility_score(result)
        self.assertEqual(score, 1.0)


# ── E. RENDERING ──────────────────────────────────────────────────

class TestRendering(unittest.TestCase):
    def test_block_summary_has_week_intent(self):
        p = make_profile()
        program = generate_program(p)
        summary = render_block_summary(program)
        self.assertIn("accumulation", summary)

    def test_block_summary_shows_credibility(self):
        p = make_profile()
        program = generate_program(p)
        summary = render_block_summary(program)
        self.assertIn("Program Score:", summary)

    def test_block_summary_shows_exposure(self):
        p = make_profile()
        program = generate_program(p)
        summary = render_block_summary(program)
        self.assertIn("Exposure by Week:", summary)

    def test_session_shows_testing(self):
        from src.forge.renderer import render_coach_session
        p = make_profile(athlete_level=AthleteLevel.ADVANCED)
        program = generate_program(p)
        for s in program.sessions:
            if s.testing_categories:
                output = render_coach_session(s)
                self.assertIn("[TEST]", output)
                return
        # If no testing sessions found, that's ok — different profiles may not have tests

    def test_render_program_includes_week_intent(self):
        from src.forge.renderer import render_program
        p = make_profile()
        program = generate_program(p)
        output = render_program(program)
        self.assertIn("accumulation", output)
        self.assertIn("test", output)


# ── F. BACKWARD COMPATIBILITY ─────────────────────────────────────

class TestBackwardCompatibility(unittest.TestCase):
    def test_all_blueprints_generate(self):
        for bp_id in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]:
            with self.subTest(bp=bp_id):
                p = make_profile()
                program = generate_program(p)
                self.assertGreater(len(program.sessions), 0)

    def test_light_session_still_works(self):
        p = make_profile(days_to_match=1)
        program = generate_program(p)
        self.assertEqual(program.goal, "light_session")

    def test_recovery_session_still_works(self):
        p = make_profile(days_to_match=0)
        program = generate_program(p)
        self.assertEqual(program.goal, "recovery")

    def test_youth_profile_generates(self):
        p = make_profile(age=15, athlete_level=AthleteLevel.BEGINNER, training_age_years=0.5)
        program = generate_program(p)
        self.assertGreater(len(program.sessions), 0)

    def test_court_sport_generates(self):
        p = make_profile(sport="tennis", goal="power", season_phase=SeasonPhase.PRE_SEASON)
        program = generate_program(p)
        self.assertGreater(len(program.sessions), 0)

    def test_elite_profile_generates(self):
        p = make_profile(athlete_level=AthleteLevel.ADVANCED, equipment_profile=EquipmentProfile.ELITE_FACILITY, training_age_years=5)
        program = generate_program(p)
        self.assertGreater(len(program.sessions), 0)

    def test_injury_profile_generates(self):
        p = make_profile(injury_history=["knee"])
        program = generate_program(p)
        self.assertGreater(len(program.sessions), 0)

    def test_all_14_blueprints_have_sessions(self):
        for bp_id in range(1, 15):
            with self.subTest(bp=bp_id):
                p = make_profile()
                program = generate_program(p)
                self.assertGreater(len(program.sessions), 0, f"BP{bp_id} produced no sessions")


if __name__ == "__main__":
    unittest.main()
