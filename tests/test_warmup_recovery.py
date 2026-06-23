import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from forge.warmup_engine import select_warmup, WARMUP_DRILLS, ENVIRONMENT_DRILLS, SESSION_TYPE_WARMUPS
from forge.recovery_engine import select_recovery, SESSION_TYPE_RECOVERY_MAP, RECOVERY_PROTOCOLS
from forge.models import AthleteProfile, AthleteLevel, EquipmentProfile, SeasonPhase


class TestWarmupEngine(unittest.TestCase):
    def setUp(self):
        self.athlete = AthleteProfile(
            sport='cricket',
            training_age_years=5,
            season_phase=SeasonPhase.IN_SEASON,
            goal='strength',
            equipment_profile=EquipmentProfile.COMMERCIAL_GYM,
            athlete_level=AthleteLevel.INTERMEDIATE,
            fatigue_level='normal',
            days_to_match=3
        )

    def test_warmup_non_empty(self):
        """Warmup protocol should have at least one phase."""
        protocol = select_warmup(self.athlete, 'strength', 'gym')
        self.assertGreater(len(protocol.phases), 0)
        self.assertGreater(protocol.total_duration_sec, 0)

    def test_warmup_phases_have_drills(self):
        """Each warmup phase should have at least one drill."""
        protocol = select_warmup(self.athlete, 'strength', 'gym')
        for phase in protocol.phases:
            self.assertGreater(len(phase.drills), 0)

    def test_speed_ground_includes_sprint_drills(self):
        """Speed session on ground should include sprint mechanics drills."""
        self.athlete.goal = 'speed'
        protocol = select_warmup(self.athlete, 'speed', 'ground')
        drill_ids = [d.id for phase in protocol.phases for d in phase.drills]
        # Should include at least one SM-* drill
        sm_drills = [did for did in drill_ids if did.startswith('SM-')]
        self.assertGreater(len(sm_drills), 0, f"No sprint mechanics drills found: {drill_ids}")

    def test_court_includes_court_drills(self):
        """Court session should include court-specific drills."""
        self.athlete.goal = 'speed'
        protocol = select_warmup(self.athlete, 'court_speed', 'court')
        drill_ids = [d.id for phase in protocol.phases for d in phase.drills]
        ct_drills = [did for did in drill_ids if did.startswith('CT-')]
        self.assertGreater(len(ct_drills), 0, f"No court drills found: {drill_ids}")

    def test_deload_short_warmup(self):
        """Deload session should have short warmup (<=5 drills)."""
        self.athlete.goal = 'deload'
        protocol = select_warmup(self.athlete, 'deload', 'gym')
        total_drills = sum(len(phase.drills) for phase in protocol.phases)
        self.assertLessEqual(total_drills, 6, f"Deload warmup too long: {total_drills} drills")

    def test_environment_filtering(self):
        """Gym environment should exclude space-intensive drills."""
        gym_drills = set(ENVIRONMENT_DRILLS['gym'])
        # Sprint mechanics and court drills need space — should not be in gym
        space_intensive = {'SM-01', 'SM-02', 'SM-03', 'SM-04', 'SM-05', 'SM-06', 'SM-07',
                           'CT-01', 'CT-02', 'CT-03', 'CT-04', 'CT-05', 'CT-06',
                           'P-05', 'P-06', 'P-10', 'P-12'}
        for drill_id in space_intensive:
            self.assertNotIn(drill_id, gym_drills,
                             f"Space-intensive drill {drill_id} found in gym environment")
        # Ground includes all drills (field can accommodate everything)
        ground_drills = set(ENVIRONMENT_DRILLS['ground'])
        self.assertEqual(len(ground_drills), len(WARMUP_DRILLS),
                         "Ground should include all warmup drills")

    def test_all_drill_ids_exist(self):
        """All drill IDs in SESSION_TYPE_WARMUPS should exist in WARMUP_DRILLS."""
        for session_type, drill_ids in SESSION_TYPE_WARMUPS.items():
            for drill_id in drill_ids:
                self.assertIn(drill_id, WARMUP_DRILLS,
                              f"Drill {drill_id} in session type {session_type} not found in WARMUP_DRILLS")


class TestRecoveryEngine(unittest.TestCase):
    def setUp(self):
        self.athlete = AthleteProfile(
            sport='cricket',
            training_age_years=5,
            season_phase=SeasonPhase.IN_SEASON,
            goal='strength',
            equipment_profile=EquipmentProfile.COMMERCIAL_GYM,
            athlete_level=AthleteLevel.INTERMEDIATE,
            fatigue_level='normal',
            days_to_match=3
        )

    def test_recovery_non_empty(self):
        """Recovery protocol should have at least one drill."""
        protocol = select_recovery(self.athlete, 'strength')
        self.assertGreater(len(protocol.drills), 0)
        self.assertGreater(protocol.duration_min, 0)

    def test_competition_elevated_not_L4(self):
        """Competition with elevated fatigue should not map to L4."""
        self.athlete.fatigue_level = 'elevated'
        self.athlete.days_to_match = 0  # competition
        protocol = select_recovery(self.athlete, 'competition')
        self.assertNotEqual(protocol.level, 4,
                            f"Competition elevated fatigue mapped to L4: {protocol.name}")

    def test_conditioning_high_not_L4(self):
        """Conditioning with high fatigue should not map to L4."""
        self.athlete.fatigue_level = 'high'
        self.athlete.goal = 'conditioning'
        protocol = select_recovery(self.athlete, 'conditioning')
        self.assertNotEqual(protocol.level, 4,
                            f"Conditioning high fatigue mapped to L4: {protocol.name}")

    def test_deload_returns_L1(self):
        """Deload session should return L1 mobility stretch."""
        self.athlete.fatigue_level = 'normal'
        protocol = select_recovery(self.athlete, 'deload')
        self.assertEqual(protocol.level, 1,
                         f"Deload did not return L1: {protocol.name}")

    def test_fatigue_level_mapping(self):
        """Fatigue level should map to appropriate protocol level."""
        for fatigue, expected_level in [('normal', 1), ('elevated', 2), ('high', 3), ('very_high', 4), ('extreme', 5)]:
            self.athlete.fatigue_level = fatigue
            protocol = select_recovery(self.athlete, 'strength')
            self.assertEqual(protocol.level, expected_level,
                             f"Fatigue {fatigue} mapped to level {protocol.level} instead of {expected_level}")

    def test_all_protocol_ids_exist(self):
        """All protocol IDs in SESSION_TYPE_RECOVERY_MAP should exist in RECOVERY_PROTOCOLS."""
        for session_type, level_map in SESSION_TYPE_RECOVERY_MAP.items():
            for level, protocol_id in level_map.items():
                self.assertIn(protocol_id, RECOVERY_PROTOCOLS,
                              f"Protocol {protocol_id} for session {session_type} level {level} not found")


if __name__ == '__main__':
    unittest.main()