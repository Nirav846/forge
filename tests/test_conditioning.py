"""Tests for conditioning engine — environment routing, sport tags, backward compatibility."""
import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.forge.conditioning_engine import select_conditioning, generate_conditioning
from src.forge.models import AthleteLevel, Session, ConditioningProtocol


class TestConditioningEnvironmentRouting(unittest.TestCase):
    """Test that environment_category determines protocol selection."""

    def test_field_sport_gets_field_protocol(self):
        p = select_conditioning(AthleteLevel.INTERMEDIATE, "aerobic_capacity", "ground", 20)
        self.assertIsNotNone(p)
        self.assertEqual(p.environment_category, "field")

    def test_court_sport_gets_court_protocol(self):
        p = select_conditioning(AthleteLevel.INTERMEDIATE, "aerobic_power", "court", 20, "tennis")
        self.assertIsNotNone(p)
        self.assertEqual(p.environment_category, "court")

    def test_gym_environment_gets_gym_protocol(self):
        p = select_conditioning(AthleteLevel.INTERMEDIATE, "aerobic_power", "gym", 20)
        self.assertIsNotNone(p)
        self.assertEqual(p.environment_category, "gym")

    def test_recovery_goal_gets_recovery_protocol(self):
        p = select_conditioning(AthleteLevel.BEGINNER, "recovery", "field", 20)
        self.assertIsNotNone(p)
        self.assertEqual(p.environment_category, "recovery")

    def test_court_rsa_short_time(self):
        p = select_conditioning(AthleteLevel.INTERMEDIATE, "rsa", "court", 10, "tennis")
        self.assertIsNotNone(p)
        self.assertEqual(p.environment_category, "court")

    def test_gym_intensive_tempo(self):
        p = select_conditioning(AthleteLevel.ADVANCED, "intensive_tempo", "gym", 20)
        self.assertIsNotNone(p)
        self.assertEqual(p.environment_category, "gym")

    def test_field_extensive_tempo(self):
        p = select_conditioning(AthleteLevel.INTERMEDIATE, "extensive_tempo", "ground", 20)
        self.assertIsNotNone(p)
        self.assertEqual(p.environment_category, "field")


class TestConditioningSportTags(unittest.TestCase):
    """Test that sport_tags filters protocols appropriately."""

    def test_cricket_gets_cricket_tagged(self):
        p = select_conditioning(AthleteLevel.ADVANCED, "rsa", "ground", 30, "cricket")
        self.assertIsNotNone(p)
        self.assertIn("cricket", p.sport_tags)

    def test_soccer_fallback_to_any(self):
        p = select_conditioning(AthleteLevel.INTERMEDIATE, "aerobic_capacity", "ground", 20, "soccer")
        self.assertIsNotNone(p)
        self.assertIn("any", p.sport_tags)

    def test_tennis_gets_court_protocol(self):
        p = select_conditioning(AthleteLevel.INTERMEDIATE, "aerobic_power", "court", 30, "tennis")
        self.assertIsNotNone(p)
        self.assertEqual(p.environment_category, "court")

    def test_badminton_gets_court_rsa(self):
        p = select_conditioning(AthleteLevel.ADVANCED, "rsa", "court", 20, "badminton")
        self.assertIsNotNone(p)
        self.assertEqual(p.environment_category, "court")


class TestConditioningBackwardCompat(unittest.TestCase):
    """Test that existing call patterns still work."""

    def test_no_sport_param(self):
        p = select_conditioning(AthleteLevel.INTERMEDIATE, "aerobic_capacity", "field", 20)
        self.assertIsNotNone(p)

    def test_generate_conditioning_no_sport(self):
        session = Session(blocks=[])
        p = generate_conditioning(session, AthleteLevel.INTERMEDIATE, "aerobic_capacity")
        self.assertIsNotNone(p)


class TestConditioningEdgeCases(unittest.TestCase):
    """Test edge cases and guards."""

    def test_beginner_no_intensive_tempo(self):
        p = select_conditioning(AthleteLevel.BEGINNER, "intensive_tempo", "field", 20)
        self.assertIsNone(p)

    def test_intermediate_no_lactate_tolerance(self):
        p = select_conditioning(AthleteLevel.INTERMEDIATE, "lactate_tolerance", "field", 30)
        self.assertIsNone(p)

    def test_advanced_gets_lactate_tolerance(self):
        p = select_conditioning(AthleteLevel.ADVANCED, "lactate_tolerance", "field", 30)
        self.assertIsNotNone(p)

    def test_no_protocol_for_invalid_goal(self):
        p = select_conditioning(AthleteLevel.INTERMEDIATE, "invalid_goal", "field", 20)
        self.assertIsNone(p)

    def test_no_decision_map_empty_slot(self):
        p = select_conditioning(AthleteLevel.INTERMEDIATE, "aerobic_capacity", "field", 10)
        self.assertIsNotNone(p)  # Falls back to system, not None


class TestConditioningProtocolData(unittest.TestCase):
    """Test that conditioning_data is consistent."""

    def test_all_protocols_have_env_cat(self):
        from src.forge.data import CONDITIONING_PROTOCOLS
        for p in CONDITIONING_PROTOCOLS:
            self.assertIn(p.environment_category, ("field", "court", "gym", "recovery"),
                          f"{p.id} has invalid env_cat: {p.environment_category}")

    def test_all_protocols_have_sport_tags(self):
        from src.forge.data import CONDITIONING_PROTOCOLS
        for p in CONDITIONING_PROTOCOLS:
            self.assertTrue(len(p.sport_tags) > 0, f"{p.id} has empty sport_tags")

    def test_no_empty_protocol_selection(self):
        """Every valid goal+env+level combo should return a protocol."""
        for goal in ["aerobic_capacity", "aerobic_power", "extensive_tempo", "recovery"]:
            for env in ["field", "court", "gym"]:
                p = select_conditioning(AthleteLevel.INTERMEDIATE, goal, env, 20)
                self.assertIsNotNone(p, f"No protocol for goal={goal}, env={env}")


class TestConditioningCompetitionProximity(unittest.TestCase):
    """Test competition-aware protocol filtering."""

    def test_days_to_match_1_limits_impact(self):
        p = select_conditioning(AthleteLevel.BEGINNER, "recovery", "field", 20, "any", days_to_match=1)
        self.assertIsNotNone(p)
        self.assertLessEqual(p.impact_level, 2, f"{p.id} impact {p.impact_level} > 2 for day-before-match")

    def test_days_to_match_1_blocks_high_impact_systems(self):
        p = select_conditioning(AthleteLevel.ADVANCED, "alactic_speed", "ground", 20, "soccer", days_to_match=1)
        self.assertIsNone(p, "Alactic speed should be unavailable day before match")

    def test_days_to_match_1_prefers_recovery_role(self):
        p = select_conditioning(AthleteLevel.BEGINNER, "recovery", "field", 20, "any", days_to_match=1)
        self.assertIsNotNone(p)
        self.assertIn(p.session_role, ("power_maintenance", "recovery_flush"))

    def test_days_to_match_2_3_limits_impact(self):
        for d in (2, 3):
            p = select_conditioning(AthleteLevel.INTERMEDIATE, "aerobic_power", "ground", 20, "soccer", days_to_match=d)
            self.assertIsNotNone(p, f"No protocol for days_to_match={d}")
            self.assertLessEqual(p.impact_level, 3, f"{p.id} impact {p.impact_level} > 3 for days_to_match={d}")

    def test_days_to_match_6_allows_high_impact(self):
        p = select_conditioning(AthleteLevel.ADVANCED, "rsa", "ground", 30, "soccer", days_to_match=6)
        self.assertIsNotNone(p)
        # Should allow normal training impact
        self.assertIn(p.session_role, ("main_conditioning", "top_up_conditioning", "power_maintenance", "speed_support"))

    def test_days_to_match_none_no_restriction(self):
        p = select_conditioning(AthleteLevel.ADVANCED, "rsa", "ground", 30, "soccer", days_to_match=None)
        self.assertIsNotNone(p)

    def test_default_days_to_match_backward_compat(self):
        p = select_conditioning(AthleteLevel.INTERMEDIATE, "aerobic_capacity", "field", 20)
        self.assertIsNotNone(p)


class TestConditioningMovementProfile(unittest.TestCase):
    """Test movement-profile-aware routing."""

    def test_court_tennis_prefers_court_profile(self):
        p = select_conditioning(AthleteLevel.INTERMEDIATE, "aerobic_power", "court", 20, "tennis")
        self.assertIsNotNone(p)
        self.assertIn(p.movement_profile,
                      ("court_shuffle", "court_rally_repeat", "court_diagonal", "accel_decel", "change_of_direction"))

    def test_field_soccer_prefers_linear_profile(self):
        p = select_conditioning(AthleteLevel.INTERMEDIATE, "aerobic_capacity", "ground", 30, "soccer")
        self.assertIsNotNone(p)
        self.assertIn(p.movement_profile,
                      ("linear_tempo", "accel_decel", "linear_speed_endurance", "linear_rsa"))

    def test_gym_gets_mixed_modal_profile(self):
        p = select_conditioning(AthleteLevel.INTERMEDIATE, "aerobic_power", "gym", 20)
        self.assertIsNotNone(p)
        self.assertEqual(p.environment_category, "gym")
        self.assertIn(p.movement_profile,
                      ("mixed_modal_circuit", "bike_intervals", "rower_intervals", "treadmill_intervals"))

    def test_unknown_sport_defaults_to_any(self):
        p = select_conditioning(AthleteLevel.INTERMEDIATE, "aerobic_capacity", "field", 20, "esports")
        self.assertIsNotNone(p)


class TestConditioningMetadataPresence(unittest.TestCase):
    """Test that all protocols carry new metadata fields."""

    def test_all_protocols_have_movement_profile(self):
        from src.forge.data import CONDITIONING_PROTOCOLS
        valid = {"linear_tempo", "linear_speed_endurance", "linear_rsa", "accel_decel",
                 "change_of_direction", "court_shuffle", "court_rally_repeat", "court_diagonal",
                 "mixed_modal_circuit", "bike_intervals", "rower_intervals", "treadmill_intervals",
                 "recovery_flush", "pool_recovery", "mobility_recovery"}
        for p in CONDITIONING_PROTOCOLS:
            self.assertIn(p.movement_profile, valid, f"{p.id} invalid movement_profile: {p.movement_profile}")

    def test_all_protocols_have_session_role(self):
        from src.forge.data import CONDITIONING_PROTOCOLS
        valid = {"main_conditioning", "top_up_conditioning", "speed_support", "power_maintenance", "recovery_flush"}
        for p in CONDITIONING_PROTOCOLS:
            self.assertIn(p.session_role, valid, f"{p.id} invalid session_role: {p.session_role}")

    def test_all_protocols_have_fatigue_cost_in_range(self):
        from src.forge.data import CONDITIONING_PROTOCOLS
        for p in CONDITIONING_PROTOCOLS:
            self.assertBetween(p.fatigue_cost, 1, 5, f"{p.id} fatigue_cost {p.fatigue_cost} out of range")

    def test_all_protocols_have_impact_level_in_range(self):
        from src.forge.data import CONDITIONING_PROTOCOLS
        for p in CONDITIONING_PROTOCOLS:
            self.assertBetween(p.impact_level, 1, 5, f"{p.id} impact_level {p.impact_level} out of range")

    def test_all_protocols_have_eccentric_cost_in_range(self):
        from src.forge.data import CONDITIONING_PROTOCOLS
        for p in CONDITIONING_PROTOCOLS:
            self.assertBetween(p.eccentric_cost, 1, 5, f"{p.id} eccentric_cost {p.eccentric_cost} out of range")

    def assertBetween(self, value, lo, hi, msg=""):
        self.assertGreaterEqual(value, lo, msg)
        self.assertLessEqual(value, hi, msg)


class TestConditioningGapRepair(unittest.TestCase):
    """Test that V1.4 library gap repairs work correctly."""

    def test_beginner_aerobic_power_field_protocol_exists(self):
        p = select_conditioning(AthleteLevel.BEGINNER, "aerobic_power", "field", 20, "soccer")
        self.assertIsNotNone(p)
        self.assertEqual(p.environment_category, "field")
        self.assertIn("Beginner", p.level)

    def test_beginner_rsa_field_protocol_exists(self):
        p = select_conditioning(AthleteLevel.BEGINNER, "rsa", "field", 20, "soccer")
        self.assertIsNotNone(p)
        self.assertEqual(p.environment_category, "field")
        self.assertIn("Beginner", p.level)

    def test_beginner_power_maintenance_field_protocol_exists(self):
        p = select_conditioning(AthleteLevel.BEGINNER, "power_maintenance", "field", 10, "soccer")
        self.assertIsNotNone(p)
        self.assertEqual(p.environment_category, "field")
        self.assertIn("Beginner", p.level)

    def test_ap012_fills_10_min_decision_map(self):
        p = select_conditioning(AthleteLevel.BEGINNER, "aerobic_power", "field", 10, "soccer")
        self.assertIsNotNone(p)
        self.assertEqual(p.id, "AP-012")

    def test_new_protocols_correctly_tagged_field(self):
        from src.forge.data import CONDITIONING_PROTOCOLS
        for pid in ("AP-012", "RSA-012", "PM-008"):
            p = next(x for x in CONDITIONING_PROTOCOLS if x.id == pid)
            self.assertEqual(p.environment_category, "field")
            self.assertTrue(len(p.sport_tags) > 0)

    def test_new_protocols_have_full_v13_metadata(self):
        from src.forge.data import CONDITIONING_PROTOCOLS
        for pid in ("AP-012", "RSA-012", "PM-008"):
            p = next(x for x in CONDITIONING_PROTOCOLS if x.id == pid)
            self.assertTrue(hasattr(p, 'movement_profile'))
            self.assertTrue(hasattr(p, 'session_role'))
            self.assertTrue(hasattr(p, 'fatigue_cost'))
            self.assertTrue(hasattr(p, 'impact_level'))
            self.assertTrue(hasattr(p, 'eccentric_cost'))

    def test_new_protocols_no_regression_on_existing(self):
        supported = [("field", "aerobic_capacity"), ("field", "extensive_tempo"),
                     ("field", "alactic_speed"), ("field", "recovery"),
                     ("court", "aerobic_capacity"), ("court", "extensive_tempo"),
                     ("gym", "aerobic_capacity"), ("gym", "extensive_tempo"), ("gym", "recovery")]
        for env, goal in supported:
            p = select_conditioning(AthleteLevel.INTERMEDIATE, goal, env, 20)
            self.assertIsNotNone(p, f"Regression: goal={goal} env={env}")

    def test_comp_window_2_allows_new_beginner_ap(self):
        p = select_conditioning(AthleteLevel.BEGINNER, "aerobic_power", "field", 20, "soccer", days_to_match=2)
        self.assertIsNotNone(p)
        self.assertLessEqual(p.impact_level, 3)

    def test_comp_window_1_allows_pm008(self):
        p = select_conditioning(AthleteLevel.BEGINNER, "power_maintenance", "field", 10, "soccer", days_to_match=1)
        self.assertIsNotNone(p)
        self.assertEqual(p.id, "PM-008")
        self.assertLessEqual(p.impact_level, 2)

    def test_ap012_progresses_to_ap001(self):
        from src.forge.data import CONDITIONING_PROTOCOLS
        ap012 = next(x for x in CONDITIONING_PROTOCOLS if x.id == "AP-012")
        self.assertIn("AP-001", ap012.progression)

    def test_rsa012_progresses_to_rsa001(self):
        from src.forge.data import CONDITIONING_PROTOCOLS
        rsa012 = next(x for x in CONDITIONING_PROTOCOLS if x.id == "RSA-012")
        self.assertIn("RSA-001", rsa012.progression)

    def test_pm008_progresses_to_pm002(self):
        from src.forge.data import CONDITIONING_PROTOCOLS
        pm008 = next(x for x in CONDITIONING_PROTOCOLS if x.id == "PM-008")
        self.assertIn("PM-002", pm008.progression)


if __name__ == "__main__":
    unittest.main()
