"""Warmup hardening tests — environment routing, session-type diffs, sport awareness."""
import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from forge.warmup_engine import (
    select_warmup, WARMUP_DRILLS, ENVIRONMENT_DRILLS,
    SESSION_TYPE_WARMUPS, SPORT_PREP_DRILLS
)
from forge.models import AthleteProfile, AthleteLevel, EquipmentProfile, SeasonPhase


def make_profile(**kwargs):
    defaults = dict(
        sport="rugby",
        training_age_years=5,
        season_phase=SeasonPhase.IN_SEASON,
        goal="strength",
        equipment_profile=EquipmentProfile.COMMERCIAL_GYM,
        athlete_level=AthleteLevel.INTERMEDIATE,
        fatigue_level="normal",
        days_to_match=3,
    )
    defaults.update(kwargs)
    return AthleteProfile(**defaults)


class TestNewWarmupDrillsExist(unittest.TestCase):
    """All new drills added in hardening phase must exist."""

    def test_pogo_jumps_exist(self):
        self.assertIn("P-11", WARMUP_DRILLS)
        self.assertEqual(WARMUP_DRILLS["P-11"].phase, "potentiate")

    def test_straight_leg_bound_exist(self):
        self.assertIn("P-12", WARMUP_DRILLS)
        self.assertEqual(WARMUP_DRILLS["P-12"].phase, "potentiate")

    def test_band_ytws_exist(self):
        self.assertIn("TS-09", WARMUP_DRILLS)
        self.assertEqual(WARMUP_DRILLS["TS-09"].phase, "activate")

    def test_band_shoulder_er_exist(self):
        self.assertIn("TS-10", WARMUP_DRILLS)
        self.assertEqual(WARMUP_DRILLS["TS-10"].phase, "activate")

    def test_cossack_squat_exist(self):
        self.assertIn("HM-11", WARMUP_DRILLS)
        self.assertEqual(WARMUP_DRILLS["HM-11"].phase, "activate")

    def test_lateral_lunge_exist(self):
        self.assertIn("HM-12", WARMUP_DRILLS)
        self.assertEqual(WARMUP_DRILLS["HM-12"].phase, "activate")

    def test_hip_flexor_stretch_exist(self):
        self.assertIn("HM-13", WARMUP_DRILLS)
        self.assertEqual(WARMUP_DRILLS["HM-13"].phase, "activate")

    def test_quadruped_t_spine_exist(self):
        self.assertIn("TS-08", WARMUP_DRILLS)
        self.assertEqual(WARMUP_DRILLS["TS-08"].phase, "activate")


class TestWarmupEnvironmentRouting(unittest.TestCase):
    """Environment-appropriate warmup selection."""

    def test_gym_strength_excludes_sprint_mechanics(self):
        athlete = make_profile(sport="rugby")
        protocol = select_warmup(athlete, "strength", "gym")
        drill_ids = [d.id for phase in protocol.phases for d in phase.drills]
        sm_drills = [d for d in drill_ids if d.startswith("SM-")]
        self.assertEqual(
            len(sm_drills), 0,
            f"Gym strength warmup should not include sprint mechanics: {sm_drills}"
        )

    def test_gym_strength_excludes_court_drills(self):
        athlete = make_profile(sport="rugby")
        protocol = select_warmup(athlete, "strength", "gym")
        drill_ids = [d.id for phase in protocol.phases for d in phase.drills]
        ct_drills = [d for d in drill_ids if d.startswith("CT-")]
        self.assertEqual(
            len(ct_drills), 0,
            f"Gym strength warmup should not include court drills: {ct_drills}"
        )

    def test_ground_strength_includes_sprint_mechanics_if_in_session(self):
        athlete = make_profile(sport="rugby")
        protocol = select_warmup(athlete, "speed", "ground")
        drill_ids = [d.id for phase in protocol.phases for d in phase.drills]
        sm_drills = [d for d in drill_ids if d.startswith("SM-")]
        self.assertGreater(
            len(sm_drills), 0,
            f"Speed session on ground should include sprint mechanics: {drill_ids}"
        )

    def test_court_strength_session_type_exists(self):
        self.assertIn("court_strength", SESSION_TYPE_WARMUPS)
        self.assertGreater(len(SESSION_TYPE_WARMUPS["court_strength"]), 0)

    def test_court_strength_includes_court_drills(self):
        athlete = make_profile(sport="tennis")
        protocol = select_warmup(athlete, "court_strength", "court")
        drill_ids = [d.id for phase in protocol.phases for d in phase.drills]
        ct_drills = [d for d in drill_ids if d.startswith("CT-")]
        self.assertGreater(
            len(ct_drills), 0,
            f"Court strength warmup should include court drills: {drill_ids}"
        )

    def test_court_environment_includes_sprint_mechanics(self):
        """Court environment should no longer exclude sprint mechanics."""
        court_drills = ENVIRONMENT_DRILLS["court"]
        sm_in_court = [d for d in court_drills if d.startswith("SM-")]
        self.assertGreater(
            len(sm_in_court), 0,
            "Court environment should include sprint mechanics drills"
        )


class TestWarmupSessionTypeDifferentiation(unittest.TestCase):
    """Different session types get meaningfully different warmups."""

    def test_conditioning_warmup_has_potentiation(self):
        athlete = make_profile(goal="conditioning")
        protocol = select_warmup(athlete, "conditioning", "ground")
        drill_ids = [d.id for phase in protocol.phases for d in phase.drills]
        potentiate = [d for d in drill_ids if WARMUP_DRILLS[d].phase == "potentiate"]
        self.assertGreater(
            len(potentiate), 0,
            f"Conditioning warmup should have potentiation phase: {drill_ids}"
        )

    def test_power_warmup_includes_pogo_jumps(self):
        athlete = make_profile(goal="power")
        protocol = select_warmup(athlete, "power", "gym")
        drill_ids = [d.id for phase in protocol.phases for d in phase.drills]
        self.assertIn(
            "P-11", drill_ids,
            f"Power warmup should include pogo jumps: {drill_ids}"
        )

    def test_strength_warmup_includes_band_ytws(self):
        athlete = make_profile(goal="strength")
        protocol = select_warmup(athlete, "strength", "gym")
        drill_ids = [d.id for phase in protocol.phases for d in phase.drills]
        self.assertIn(
            "TS-09", drill_ids,
            f"Strength warmup should include band YTWs: {drill_ids}"
        )

    def test_speed_warmup_includes_straight_leg_bound(self):
        athlete = make_profile(goal="speed")
        protocol = select_warmup(athlete, "speed", "ground")
        drill_ids = [d.id for phase in protocol.phases for d in phase.drills]
        self.assertIn(
            "P-12", drill_ids,
            f"Speed warmup should include straight-leg bound: {drill_ids}"
        )

    def test_deload_warmup_short(self):
        athlete = make_profile(goal="deload")
        protocol = select_warmup(athlete, "deload", "gym")
        total_drills = sum(len(phase.drills) for phase in protocol.phases)
        self.assertLessEqual(total_drills, 6,
                             f"Deload warmup too long: {total_drills} drills")

    def test_return_to_play_warmup_low_intensity(self):
        athlete = make_profile(goal="return_to_sport")
        protocol = select_warmup(athlete, "return_to_play", "gym")
        drill_ids = [d.id for phase in protocol.phases for d in phase.drills]
        potentiate = [d for d in drill_ids if WARMUP_DRILLS[d].phase == "potentiate"]
        self.assertEqual(
            len(potentiate), 0,
            f"Return-to-play warmup should have no potentiation: {drill_ids}"
        )


class TestSportAwareCompetitionWarmup(unittest.TestCase):
    """Competition warmup should be sport-aware."""

    def test_sport_prep_drills_defined(self):
        self.assertIn("cricket", SPORT_PREP_DRILLS)
        self.assertIn("tennis", SPORT_PREP_DRILLS)
        self.assertIn("badminton", SPORT_PREP_DRILLS)
        self.assertIn("rugby", SPORT_PREP_DRILLS)
        self.assertIn("soccer", SPORT_PREP_DRILLS)
        self.assertIn("basketball", SPORT_PREP_DRILLS)
        self.assertIn("volleyball", SPORT_PREP_DRILLS)

    def test_cricket_competition_includes_batting(self):
        athlete = make_profile(sport="cricket")
        protocol = select_warmup(athlete, "competition", "ground")
        drill_ids = [d.id for phase in protocol.phases for d in phase.drills]
        self.assertIn(
            "SS-01", drill_ids,
            f"Cricket competition warmup should include shadow batting: {drill_ids}"
        )

    def test_tennis_competition_includes_groundstrokes(self):
        athlete = make_profile(sport="tennis")
        protocol = select_warmup(athlete, "competition", "court")
        drill_ids = [d.id for phase in protocol.phases for d in phase.drills]
        self.assertIn(
            "SS-05", drill_ids,
            f"Tennis competition warmup should include shadow groundstrokes: {drill_ids}"
        )

    def test_badminton_competition_includes_overhead_clears(self):
        athlete = make_profile(sport="badminton")
        protocol = select_warmup(athlete, "competition", "court")
        drill_ids = [d.id for phase in protocol.phases for d in phase.drills]
        self.assertIn(
            "SS-08", drill_ids,
            f"Badminton competition warmup should include overhead clears: {drill_ids}"
        )

    def test_rugby_competition_includes_lineout_jumps(self):
        athlete = make_profile(sport="rugby")
        protocol = select_warmup(athlete, "competition", "ground")
        drill_ids = [d.id for phase in protocol.phases for d in phase.drills]
        self.assertIn(
            "SS-03", drill_ids,
            f"Rugby competition warmup should include lineout jumps: {drill_ids}"
        )

    def test_unknown_sport_competition_no_crash(self):
        athlete = make_profile(sport="esports")
        protocol = select_warmup(athlete, "competition", "gym")
        self.assertGreater(len(protocol.phases), 0)
        self.assertGreater(protocol.total_duration_sec, 0)


class TestWarmupPhaseOrdering(unittest.TestCase):
    """Warmup phases should be in correct order."""

    def test_phases_in_order(self):
        athlete = make_profile()
        protocol = select_warmup(athlete, "strength", "gym")
        phase_names = [p.name.lower() for p in protocol.phases]
        expected_order = ["raise", "activate", "potentiate", "prepare"]
        filtered = [p for p in expected_order if p in phase_names]
        self.assertEqual(
            phase_names, filtered,
            f"Phases out of order: {phase_names}"
        )

    def test_competition_warmup_has_sport_prep_drill(self):
        athlete = make_profile(sport="cricket")
        protocol = select_warmup(athlete, "competition", "ground")
        drill_ids = [d.id for phase in protocol.phases for d in phase.drills]
        bash = [d for d in drill_ids if d.startswith("SS-")
                and WARMUP_DRILLS[d].phase == "potentiate"]
        self.assertGreater(
            len(bash), 0,
            f"Competition warmup should have sport-prep potentiate drills: {drill_ids}"
        )


class TestWarmupEnvironmentFilteringIntegration(unittest.TestCase):
    """End-to-end warmup environment filtering."""

    def test_tennis_gym_strength_gets_gym_appropriate(self):
        athlete = make_profile(sport="tennis", goal="strength")
        protocol = select_warmup(athlete, "strength", "gym")
        drill_ids = [d.id for phase in protocol.phases for d in phase.drills]
        # Should have wall slides (TS-05) but not CT-01 (split-step — needs space)
        self.assertIn("TS-07", drill_ids)
        space_intensive = {'SM-01', 'SM-02', 'CT-01', 'P-05', 'P-06'}
        for sid in space_intensive:
            self.assertNotIn(sid, drill_ids,
                             f"Space-intensive drill {sid} in gym warmup")

    def test_rugby_ground_speed_gets_full_warmup(self):
        athlete = make_profile(sport="rugby", goal="speed")
        protocol = select_warmup(athlete, "speed", "ground")
        drill_ids = [d.id for phase in protocol.phases for d in phase.drills]
        # Should have sprint mechanics
        self.assertTrue(
            any(d.startswith("SM-") for d in drill_ids),
            f"Ground speed warmup missing sprint mechanics: {drill_ids}"
        )

    def test_basketball_court_gets_court_appropriate(self):
        athlete = make_profile(sport="basketball")
        protocol = select_warmup(athlete, "court_strength", "court")
        drill_ids = [d.id for phase in protocol.phases for d in phase.drills]
        ct_drills = [d for d in drill_ids if d.startswith("CT-")]
        self.assertGreater(
            len(ct_drills), 0,
            f"Basketball strength on court should have court drills: {drill_ids}"
        )
        # Should not have cricket-specific drills
        self.assertNotIn("SS-01", drill_ids)
        self.assertNotIn("SS-02", drill_ids)


class TestWarmupSportPrepDrills(unittest.TestCase):
    """SPORT_PREP_DRILLS entries reference valid drills."""

    def test_all_sport_prep_drill_ids_exist(self):
        for sport, drill_ids in SPORT_PREP_DRILLS.items():
            for did in drill_ids:
                self.assertIn(
                    did, WARMUP_DRILLS,
                    f"Sport prep drill {did} for {sport} not in WARMUP_DRILLS"
                )


class TestWarmupNewSessionTypes(unittest.TestCase):
    """New session type warmups should be populated."""

    def test_strength_lower_defined(self):
        self.assertIn("strength_lower", SESSION_TYPE_WARMUPS)
        self.assertGreater(len(SESSION_TYPE_WARMUPS["strength_lower"]), 0)

    def test_strength_upper_defined(self):
        self.assertIn("strength_upper", SESSION_TYPE_WARMUPS)
        self.assertGreater(len(SESSION_TYPE_WARMUPS["strength_upper"]), 0)

    def test_strength_lower_favors_hip_drills(self):
        """strength_lower should emphasize hip/glute activation."""
        lower_ids = SESSION_TYPE_WARMUPS["strength_lower"]
        has_glute = "GA-01" in lower_ids
        has_cossack = "HM-11" in lower_ids
        self.assertTrue(
            has_glute or has_cossack,
            f"strength_lower missing hip/glute drills: {lower_ids}"
        )

    def test_strength_upper_favors_shoulder_drills(self):
        """strength_upper should emphasize shoulder/scap activation."""
        upper_ids = SESSION_TYPE_WARMUPS["strength_upper"]
        has_band_ytws = "TS-09" in upper_ids
        has_band_er = "TS-10" in upper_ids
        self.assertTrue(
            has_band_ytws or has_band_er,
            f"strength_upper missing shoulder activation drills: {upper_ids}"
        )


class TestVolleyballConditioning(unittest.TestCase):
    """Volleyball-specific conditioning protocols should be selectable."""

    def test_volleyball_court_rsa_selectable(self):
        from forge.conditioning_engine import select_conditioning
        from forge.models import AthleteLevel
        p = select_conditioning(
            AthleteLevel.INTERMEDIATE, "rsa", "court", 20, "volleyball"
        )
        self.assertIsNotNone(p)
        self.assertEqual(p.environment_category, "court")
        self.assertIn("volleyball", p.sport_tags)

    def test_volleyball_movement_profile_prioritized(self):
        from forge.conditioning_engine import select_conditioning, SPORT_MOVEMENT_PROFILES
        profiles = SPORT_MOVEMENT_PROFILES.get("volleyball", [])
        self.assertIn("court_rally_repeat", profiles)
        self.assertIn("court_shuffle", profiles)
        self.assertIn("change_of_direction", profiles)
        self.assertIn("accel_decel", profiles)

    def test_volleyball_cc006_in_decision_map(self):
        from forge.data import COND_DECISION_MAP
        rsa_court_20 = COND_DECISION_MAP.get("rsa", {}).get("court", {}).get(20)
        self.assertIsNotNone(rsa_court_20)


class TestConditioningHockeyRouting(unittest.TestCase):
    """Hockey should have its own movement profile."""

    def test_hockey_has_own_movement_profile(self):
        from forge.conditioning_engine import SPORT_MOVEMENT_PROFILES
        self.assertIn("hockey", SPORT_MOVEMENT_PROFILES)
        self.assertIn("change_of_direction", SPORT_MOVEMENT_PROFILES["hockey"])


class TestConditioningNewSports(unittest.TestCase):
    """Newly added sports should have movement profiles."""

    def test_netball_has_movement_profile(self):
        from forge.conditioning_engine import SPORT_MOVEMENT_PROFILES
        self.assertIn("netball", SPORT_MOVEMENT_PROFILES)

    def test_american_football_has_movement_profile(self):
        from forge.conditioning_engine import SPORT_MOVEMENT_PROFILES
        self.assertIn("american_football", SPORT_MOVEMENT_PROFILES)


class TestConditioningProtocolTiers(unittest.TestCase):
    """All protocols should have tier rankings."""

    def test_cc_protocols_have_tiers(self):
        from forge.conditioning_data import PROTOCOL_TIERS
        for pid in ("CC-001", "CC-002", "CC-003", "CC-004", "CC-005", "CC-006", "CC-007"):
            self.assertIn(pid, PROTOCOL_TIERS, f"{pid} missing from PROTOCOL_TIERS")

    def test_gc_protocols_have_tiers(self):
        from forge.conditioning_data import PROTOCOL_TIERS
        for pid in ("GC-001", "GC-002", "GC-003"):
            self.assertIn(pid, PROTOCOL_TIERS, f"{pid} missing from PROTOCOL_TIERS")

    def test_fc001_has_tier(self):
        from forge.conditioning_data import PROTOCOL_TIERS
        self.assertIn("FC-001", PROTOCOL_TIERS)


class TestSessionTypeRoutingFromMain(unittest.TestCase):
    """main.py session type routing should produce expected warmups."""

    def test_court_sport_gets_court_strength_warmup(self):
        from forge.main import _get_session_type, _adjust_session_type_for_environment, _sport_to_environment
        from forge.models import AthleteProfile, AthleteLevel, EquipmentProfile, SeasonPhase
        athlete = AthleteProfile(
            sport="tennis",
            training_age_years=3,
            season_phase=SeasonPhase.OFF_SEASON,
            goal="strength",
            equipment_profile=EquipmentProfile.COMMERCIAL_GYM,
            athlete_level=AthleteLevel.INTERMEDIATE,
        )
        session_type = _get_session_type(athlete, 8)  # BP08 = Court Sport AD
        environment = _sport_to_environment(athlete.sport)
        adjusted = _adjust_session_type_for_environment(session_type, environment, 8)
        self.assertEqual(adjusted, "court_strength")
        protocol = select_warmup(athlete, adjusted, environment)
        drill_ids = [d.id for phase in protocol.phases for d in phase.drills]
        ct_drills = [d for d in drill_ids if d.startswith("CT-")]
        self.assertGreater(
            len(ct_drills), 0,
            f"Court strength warmup missing court drills: {drill_ids}"
        )

    def test_ground_sport_gets_strength_warmup(self):
        from forge.main import _get_session_type, _adjust_session_type_for_environment, _sport_to_environment
        from forge.models import AthleteProfile, AthleteLevel, EquipmentProfile, SeasonPhase
        athlete = AthleteProfile(
            sport="rugby",
            training_age_years=3,
            season_phase=SeasonPhase.OFF_SEASON,
            goal="strength",
            equipment_profile=EquipmentProfile.COMMERCIAL_GYM,
            athlete_level=AthleteLevel.INTERMEDIATE,
        )
        session_type = _get_session_type(athlete, 1)
        environment = _sport_to_environment(athlete.sport)
        adjusted = _adjust_session_type_for_environment(session_type, environment, 1)
        self.assertEqual(adjusted, "strength")


if __name__ == "__main__":
    unittest.main()
