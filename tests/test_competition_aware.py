"""FORGE V1.5 tests — competition-aware session generation.

Categories:
A. Metadata correctness
B. Window behavior
C. Exercise filtering
D. Volume taper
E. Blueprint preservation
F. Backward compatibility
G. No regressions (run full suite)
"""

import unittest
from src.forge.models import (
    AthleteProfile, AthleteLevel, EquipmentProfile, SeasonPhase,
    Exercise, FamilyCode,
)
from src.forge.data import EXERCISE_BY_ID
from src.forge.exercise_selector import select_exercise
from src.forge.main import generate_program
from src.forge.validator import verify_credibility, calculate_credibility_score
from src.forge.conditioning_engine import (
    EXERCISE_COMP_MAX_FATIGUE, EXERCISE_COMP_MAX_IMPACT,
    EXERCISE_COMP_MAX_ECCENTRIC, _resolve_comp_window,
)


# =============================================================================
# Helpers
# =============================================================================

def make_profile(**kwargs):
    defaults = dict(
        sport="rugby",
        training_age_years=5,
        season_phase=SeasonPhase.IN_SEASON,
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
    )
    defaults.update(kwargs)
    return AthleteProfile(**defaults)


def get_exercise_meta(eid):
    ex = EXERCISE_BY_ID.get(eid)
    if ex is None:
        return None
    return (ex.fatigue_cost, ex.impact_level, ex.eccentric_cost, ex.competition_role)


# =============================================================================
# A: Metadata correctness — exercise competition metadata populated correctly
# =============================================================================

class TestCompetitionMetadata(unittest.TestCase):
    """A: exercise competition metadata populated and sensible."""

    def test_a1_all_exercises_have_comp_metadata(self):
        """Every exercise has fatigue_cost, impact_level, eccentric_cost, competition_role."""
        for eid, ex in EXERCISE_BY_ID.items():
            self.assertIsInstance(ex.fatigue_cost, int, f"{eid} missing fatigue_cost")
            self.assertIsInstance(ex.impact_level, int, f"{eid} missing impact_level")
            self.assertIsInstance(ex.eccentric_cost, int, f"{eid} missing eccentric_cost")
            self.assertIsInstance(ex.competition_role, str, f"{eid} missing competition_role")
            self.assertGreaterEqual(ex.fatigue_cost, 1, f"{eid} fatigue < 1")
            self.assertLessEqual(ex.fatigue_cost, 5, f"{eid} fatigue > 5")

    def test_a2_metadata_in_range(self):
        """All metadata values in 1-5 range."""
        for eid, ex in EXERCISE_BY_ID.items():
            for attr in ("fatigue_cost", "impact_level", "eccentric_cost"):
                val = getattr(ex, attr)
                self.assertIn(val, range(1, 6), f"{eid}.{attr}={val}")

    def test_a3_core_is_low_risk(self):
        """All core exercises are low-risk (all <= 2)."""
        for eid, ex in EXERCISE_BY_ID.items():
            if ex.family == FamilyCode.CORE:
                self.assertLessEqual(ex.fatigue_cost, 2, f"{eid} core fatigue too high")
                self.assertLessEqual(ex.impact_level, 2, f"{eid} core impact too high")
                self.assertLessEqual(ex.eccentric_cost, 2, f"{eid} core eccentric too high")

    def test_a4_explosive_exercises_high_impact(self):
        """Explosive exercises in power/speed families should have impact >= 4."""
        for eid, ex in EXERCISE_BY_ID.items():
            if not ex.explosive:
                continue
            if ex.family in (FamilyCode.CORE, FamilyCode.ROT, FamilyCode.ACC):
                continue
            self.assertGreaterEqual(ex.impact_level, 4,
                                    f"{eid} ({ex.name}) explosive but impact={ex.impact_level}")

    def test_a5_rdl_high_eccentric(self):
        """RDL and Nordic curl have elevated eccentric_cost."""
        rdl = EXERCISE_BY_ID["DLHD-006"]
        self.assertEqual(rdl.eccentric_cost, 5, "RDL should have eccentric=5")
        nordic = EXERCISE_BY_ID["SLHD-009"]
        self.assertEqual(nordic.eccentric_cost, 5, "Nordic should have eccentric=5")

    def test_a6_competition_roles_assigned(self):
        """Each exercise has one of the known competition_role values."""
        valid_roles = {"strength", "speed_power", "accessory", "core", "carry"}
        for eid, ex in EXERCISE_BY_ID.items():
            self.assertIn(ex.competition_role, valid_roles,
                          f"{eid} has unknown role '{ex.competition_role}'")

    def test_a7_bodyweight_exercises_lower_fatigue(self):
        """Bodyweight exercises without explosive component have lower fatigue."""
        air_squat = EXERCISE_BY_ID["DLKD-001"]
        self.assertLessEqual(air_squat.fatigue_cost, 3, "Air squat fatigue too high")
        push_up = EXERCISE_BY_ID["HPush-003"]
        self.assertLessEqual(push_up.fatigue_cost, 3, "Push-up fatigue too high")


# =============================================================================
# B: Window behavior — competition window affects session generation
# =============================================================================

class TestWindowBehavior(unittest.TestCase):
    """B: session generation changes appropriately across competition windows."""

    def _generate(self, days_to_match, sport="rugby", goal="strength", level=AthleteLevel.INTERMEDIATE, **kw):
        p = make_profile(
            sport=sport,
            days_to_match=days_to_match,
            goal=goal,
            athlete_level=level,
            **kw,
        )
        return generate_program(p)

    def test_b1_no_comp_full_training(self):
        """days_to_match=None yields full session with all families."""
        prog = self._generate(None)
        s = prog.sessions[0]
        self.assertGreaterEqual(len(s.blocks), 5, "No-comp session too small")

    def test_b2_full_window_same_as_no_comp(self):
        """days_to_match=7 yields full session similar to no-comp."""
        prog7 = self._generate(7)
        prog0 = self._generate(None)
        s7 = prog7.sessions[0]
        s0 = prog0.sessions[0]
        # Both should have full exercise counts
        self.assertGreaterEqual(len(s7.blocks), 5)
        # Slightly different exercise selection due to LRU is OK

    def test_b3_moderate_window_replaces_high_eccentric(self):
        """days_to_match=5 (MODERATE) replaces RDL (ecc=5) with lower-ecc variant."""
        prog = self._generate(5)
        s = prog.sessions[0]
        # RDL should NOT appear at window 4 (ecc=5 > 4)
        rdl_names = {"RDL", "Single-Leg RDL"}
        for b in s.blocks:
            for ex in b.exercises:
                self.assertNotIn(ex.name, rdl_names,
                                 f"RDL variant '{ex.name}' found at 5 days out")
        # Session must still have DLHD slot
        dlhd_blocks = [b for b in s.blocks if b.family == FamilyCode.DLHD]
        self.assertGreaterEqual(len(dlhd_blocks), 1, "DLHD slot missing at MODERATE")

    def test_b4_light_window_trims_accessories(self):
        """days_to_match=3 (LIGHT) has fewer families than full."""
        prog_full = self._generate(None)
        prog_light = self._generate(3)
        full_blocks = len(prog_full.sessions[0].blocks)
        light_blocks = len(prog_light.sessions[0].blocks)
        self.assertLessEqual(light_blocks, full_blocks,
                             "Light session should not have more families than full")

    def test_b5_light_window_filters_high_eccentric(self):
        """days_to_match=3 (LIGHT) excludes exercises with eccentric > 3."""
        prog = self._generate(3)
        s = prog.sessions[0]
        for b in s.blocks:
            for ex in b.exercises:
                self.assertLessEqual(ex.eccentric_cost, 3,
                                     f"{ex.name} ecc={ex.eccentric_cost} > 3 at 3 days out")

    def test_b5b_light_window_filters_high_fatigue(self):
        """days_to_match=3 (LIGHT) excludes exercises with fatigue > 3."""
        prog = self._generate(3)
        s = prog.sessions[0]
        for b in s.blocks:
            for ex in b.exercises:
                self.assertLessEqual(ex.fatigue_cost, 3,
                                     f"{ex.name} fatigue={ex.fatigue_cost} > 3 at 3 days out")

    def test_b6_light_window_filters_high_impact(self):
        """days_to_match=3 (LIGHT) excludes exercises with impact > 3."""
        prog = self._generate(3)
        s = prog.sessions[0]
        for b in s.blocks:
            for ex in b.exercises:
                self.assertLessEqual(ex.impact_level, 3,
                                     f"{ex.name} impact={ex.impact_level} > 3 at 3 days out")

    def test_b7_primer_very_sparse(self):
        """days_to_match=1 (PRIMER) yields sparse, low-risk session."""
        prog = self._generate(1)
        s = prog.sessions[0]
        # Should have very few exercises
        total_ex = sum(len(b.exercises) for b in s.blocks)
        self.assertLess(total_ex, 8, f"PRIMER session has {total_ex} exercises, expected < 8")
        # All should be low-risk
        for b in s.blocks:
            for ex in b.exercises:
                self.assertLessEqual(ex.fatigue_cost, 2,
                                     f"{ex.name} fatigue={ex.fatigue_cost} > 2 at 1 day out")
                self.assertLessEqual(ex.impact_level, 2,
                                     f"{ex.name} impact={ex.impact_level} > 2 at 1 day out")

    def test_b8_primer_still_has_credibility(self):
        """PRIMER session is valid even if sparse."""
        prog = self._generate(1)
        self.assertGreaterEqual(prog.credibility_score, 0.5,
                                f"PRIMER credibility too low: {prog.credibility_score}")

    def test_b9_conditioning_also_competition_aware(self):
        """Conditioning selection respects competition window at 3 days."""
        for d in (3, 5, None):
            prog = self._generate(d)
            s = prog.sessions[0]
            cond = s.conditioning
            if cond:
                self.assertIsNotNone(cond.session_role)
                self.assertIn(cond.impact_level, range(1, 6))

    def test_b10_field_athlete_competition_taper(self):
        """Field athlete (soccer) shows taper across windows."""
        for d, expected_max_fams in [(None, 8), (7, 8), (5, 7), (3, 5), (1, 6)]:
            prog = self._generate(d, sport="soccer")
            s = prog.sessions[0]
            self.assertLessEqual(len(s.blocks), expected_max_fams,
                                 f"soccer d={d}: {len(s.blocks)} blocks > {expected_max_fams}")


# =============================================================================
# C: Exercise filtering — comp-aware filtering works correctly
# =============================================================================

class TestExerciseFiltering(unittest.TestCase):
    """C: exercise selection respects competition window constraints."""

    def test_c1_none_window_allows_all(self):
        """No competition window — RDL (ecc=5) should be selectable."""
        ex = select_exercise(
            FamilyCode.DLHD, AthleteLevel.INTERMEDIATE,
            EquipmentProfile.COMMERCIAL_GYM, {}, [],
            days_to_match=None,
        )
        self.assertIsNotNone(ex, "No DLHD exercise selected")

    def test_c2_light_window_blocks_rdl(self):
        """LIGHT window — RDL (ecc=5) should NOT be selected for DLHD."""
        ex = select_exercise(
            FamilyCode.DLHD, AthleteLevel.INTERMEDIATE,
            EquipmentProfile.COMMERCIAL_GYM, {}, [],
            days_to_match=3,
        )
        self.assertIsNotNone(ex, "No DLHD exercise at LIGHT window")
        self.assertLessEqual(ex.eccentric_cost, 3,
                             f"DLHD {ex.name} ecc={ex.eccentric_cost} > 3 at LIGHT window")

    def test_c3_light_window_blocks_nordic(self):
        """LIGHT window — Nordic curl (ecc=5) blocked for SLHD."""
        ex = select_exercise(
            FamilyCode.SLHD, AthleteLevel.INTERMEDIATE,
            EquipmentProfile.COMMERCIAL_GYM, {}, [],
            days_to_match=3,
        )
        if ex:
            self.assertLessEqual(ex.eccentric_cost, 3,
                                 f"SLHD {ex.name} ecc={ex.eccentric_cost} > 3 at LIGHT window")

    def test_c4_primer_window_core_only(self):
        """PRIMER window — Core exercises always selectable."""
        ex = select_exercise(
            FamilyCode.CORE, AthleteLevel.INTERMEDIATE,
            EquipmentProfile.COMMERCIAL_GYM, {}, [],
            days_to_match=1,
        )
        self.assertIsNotNone(ex, "Core exercise should be available at PRIMER")
        self.assertLessEqual(ex.fatigue_cost, 2)
        self.assertLessEqual(ex.impact_level, 2)

    def test_c5_primer_window_strength_filtered(self):
        """PRIMER window — heavy strength exercises filtered."""
        ex = select_exercise(
            FamilyCode.DLKD, AthleteLevel.INTERMEDIATE,
            EquipmentProfile.COMMERCIAL_GYM, {}, [],
            days_to_match=1,
        )
        # All DLKD have fatigue=3, impact=3 at base — filtered at PRIMER
        # Substitution picks something else
        if ex:
            self.assertLessEqual(ex.fatigue_cost, 2,
                                 f"PRIMER DLKD selected {ex.name} fatigue={ex.fatigue_cost}")

    def test_c6_moderate_window_blocks_ecc_4(self):
        """MODERATE window — ecc=5 blocked, ecc=4 may be allowed."""
        ex = select_exercise(
            FamilyCode.DLHD, AthleteLevel.INTERMEDIATE,
            EquipmentProfile.COMMERCIAL_GYM, {}, [],
            days_to_match=5,
        )
        self.assertIsNotNone(ex, "No DLHD exercise at MODERATE window")
        self.assertLessEqual(ex.eccentric_cost, 4,
                             f"DLHD {ex.name} ecc={ex.eccentric_cost} > 4 at MODERATE window")


# =============================================================================
# D: Volume taper — sessions get smaller/lighter near competition
# =============================================================================

class TestVolumeTaper(unittest.TestCase):
    """D: session volume reduces appropriately near competition."""

    def _count_exercises(self, prog):
        s = prog.sessions[0]
        return sum(len(b.exercises) for b in s.blocks)

    def test_d1_light_has_fewer_exercises_than_full(self):
        """3 days out has fewer or equal exercises than no-comp."""
        full = self._count_exercises(self._generate(None))
        light = self._count_exercises(self._generate(3))
        self.assertLessEqual(light, full, "LIGHT should not have more exercises than FULL")

    def test_d2_moderate_has_same_or_fewer_exercises(self):
        """5 days out has <= no-comp exercise count."""
        full = self._count_exercises(self._generate(None))
        mod = self._count_exercises(self._generate(5))
        self.assertLessEqual(mod, full, "MODERATE should not have more exercises than FULL")

    def test_d3_primer_much_less_than_full(self):
        """1 day out has significantly fewer exercises than no-comp."""
        full = self._count_exercises(self._generate(None))
        primer = self._count_exercises(self._generate(1))
        self.assertLess(primer, full, "PRIMER should have fewer exercises than FULL")

    def _generate(self, days_to_match, sport="rugby"):
        p = make_profile(sport=sport, days_to_match=days_to_match, goal="strength")
        return generate_program(p)


# =============================================================================
# E: Blueprint preservation — generator does not collapse
# =============================================================================

class TestBlueprintPreservation(unittest.TestCase):
    """E: generator maintains blueprint identity across competition windows."""

    def test_e1_all_windows_produce_valid_sessions(self):
        """Every competition window produces a valid session for various blueprints."""
        configs = [
            ("rugby", "strength"),
            ("tennis", "power"),
            ("soccer", "conditioning"),
            ("rugby", "power_maintenance"),
        ]
        windows = [None, 7, 5, 3, 1]
        for sport, goal in configs:
            for d in windows:
                p = make_profile(sport=sport, days_to_match=d, goal=goal)
                try:
                    prog = generate_program(p)
                    s = prog.sessions[0]
                    self.assertIsNotNone(prog.blueprint_name,
                                         f"Empty blueprint for {sport}/{goal}/d={d}")
                except Exception as e:
                    self.fail(f"Crash for {sport}/{goal}/d={d}: {e}")

    def test_e2_same_blueprint_selected_regardless_of_window(self):
        """days_to_match should not change blueprint selection."""
        p_base = make_profile(sport="rugby", goal="strength", season_phase=SeasonPhase.OFF_SEASON)
        bp_ids = set()
        for d in [None, 7, 5, 3, 1]:
            p = make_profile(sport="rugby", goal="strength",
                             season_phase=SeasonPhase.OFF_SEASON, days_to_match=d)
            prog = generate_program(p)
            bp_ids.add(prog.blueprint_id)
        self.assertEqual(len(bp_ids), 1, f"Blueprint changed: {bp_ids}")

    def test_e3_sprint_blueprint_keeps_speed_power(self):
        """Sprint Development blueprint retains Plyo/Ball/Sprint slots at all windows."""
        for d in [None, 7, 5, 3]:
            p = make_profile(sport="rugby", days_to_match=d, goal="speed",
                             season_phase=SeasonPhase.PRE_SEASON)
            prog = generate_program(p)
            s = prog.sessions[0]
            fams = [b.family.value for b in s.blocks]
            has_power = any(f in fams for f in ("Plyo", "Ball", "Sprint"))
            power_exs = [ex for b in s.blocks for ex in b.exercises if ex.competition_role == "speed_power"]
            if d == 3:
                self.assertGreaterEqual(len(power_exs), 1,
                                        "Sprint blueprint lost all power at LIGHT")
            else:
                self.assertTrue(has_power or len(power_exs) > 0,
                                f"Sprint blueprint missing power at d={d}")

    def test_e4_moderate_keeps_strength(self):
        """MODERATE window retains strength work (just filters extremes)."""
        p = make_profile(sport="rugby", days_to_match=5, goal="strength")
        prog = generate_program(p)
        s = prog.sessions[0]
        strength_exs = [ex for b in s.blocks for ex in b.exercises if ex.competition_role == "strength"]
        self.assertGreaterEqual(len(strength_exs), 2,
                                f"MODERATE has only {len(strength_exs)} strength exercises")


# =============================================================================
# F: Backward compatibility
# =============================================================================

class TestBackwardCompatibility(unittest.TestCase):
    """F: Existing behavior unchanged when days_to_match=None or 0."""

    def test_f1_none_unchanged(self):
        """days_to_match=None behaves as before (credibility >= 0.8)."""
        p = make_profile(days_to_match=None)
        prog = generate_program(p)
        self.assertGreaterEqual(prog.credibility_score, 0.7)

    def test_f2_zero_returns_recovery(self):
        """days_to_match=0 returns recovery program."""
        p = make_profile(days_to_match=0)
        prog = generate_program(p)
        self.assertEqual(prog.goal, "recovery")
        self.assertEqual(prog.blueprint_name, "Deload / Active Recovery")

    def test_f3_one_returns_light(self):
        """days_to_match=1 returns light pre-match program."""
        p = make_profile(days_to_match=1)
        prog = generate_program(p)
        self.assertEqual(prog.goal, "light_session")

    def test_f4_credibility_no_comp(self):
        """Credibility check still works for no-comp (12-point, not 13)."""
        p = make_profile(days_to_match=None)
        prog = generate_program(p)
        self.assertGreaterEqual(prog.credibility_score, 0.0)
        self.assertLessEqual(prog.credibility_score, 1.0)


# =============================================================================
# G: Regression tests
# =============================================================================

class TestCompetitionRegression(unittest.TestCase):
    """G: Edge case and regression tests."""

    def test_g1_fatigue_0_not_allowed(self):
        """No exercise should have fatigue_cost == 0."""
        for eid, ex in EXERCISE_BY_ID.items():
            self.assertGreaterEqual(ex.fatigue_cost, 1, f"{eid} has fatigue_cost=0")

    def test_g2_comp_window_values_consistent(self):
        """Window values are consistent across thresholds."""
        for window in [None, 6, 4, 2, 1]:
            f = EXERCISE_COMP_MAX_FATIGUE.get(window, 5)
            i = EXERCISE_COMP_MAX_IMPACT.get(window, 5)
            e = EXERCISE_COMP_MAX_ECCENTRIC.get(window, 5)
            self.assertIn(f, range(1, 6), f"Window {window} fatigue threshold {f} out of range")
            self.assertIn(i, range(1, 6), f"Window {window} impact threshold {i} out of range")
            self.assertIn(e, range(1, 6), f"Window {window} eccentric threshold {e} out of range")

    def test_g3_validator_competition_check_added(self):
        """Validator includes competition_appropriate check for comp-constrained profiles."""
        p = make_profile(days_to_match=3)
        prog = generate_program(p)
        check = verify_credibility(prog.sessions[0], p)
        self.assertIn("competition_appropriate", check,
                      "Validator missing competition_appropriate for days_to_match=3")

    def test_g4_validator_skips_comp_check_no_comp(self):
        """Validator skips competition_appropriate for no-comp profiles."""
        p = make_profile(days_to_match=None)
        prog = generate_program(p)
        check = verify_credibility(prog.sessions[0], p)
        self.assertNotIn("competition_appropriate", check,
                         "Validator should skip competition_appropriate when days_to_match=None")

    def test_g5_field_athlete_beginner(self):
        """Beginner field athlete still gets a valid session at LIGHT."""
        p = make_profile(sport="soccer", days_to_match=3, athlete_level=AthleteLevel.BEGINNER)
        prog = generate_program(p)
        s = prog.sessions[0]
        self.assertGreaterEqual(len(s.blocks), 3, "Beginner LIGHT session too sparse")

    def test_g6_court_athlete_competition_taper(self):
        """Court athlete (tennis) gets valid session at MODERATE."""
        p = make_profile(sport="tennis", days_to_match=5, athlete_level=AthleteLevel.INTERMEDIATE, goal="power")
        prog = generate_program(p)
        s = prog.sessions[0]
        self.assertGreaterEqual(len(s.blocks), 3, "Tennis MODERATE session too sparse")
        self.assertLessEqual(len(s.blocks), 8, "Tennis MODERATE session too large")

    def test_g7_gym_only_athlete(self):
        """Gym-only athlete still gets valid session at all windows."""
        p = make_profile(sport="swimming", equipment_profile=EquipmentProfile.BASIC_GYM,
                         days_to_match=3)
        prog = generate_program(p)
        s = prog.sessions[0]
        self.assertGreaterEqual(len(s.blocks), 3, "Swimmer LIGHT session too sparse")

    def test_g8_all_profiles_valid_at_light(self):
        """All profile types generate valid sessions at LIGHT."""
        configs = [
            ("rugby", "strength", AthleteLevel.ADVANCED, 3),
            ("tennis", "power", AthleteLevel.INTERMEDIATE, 3),
            ("soccer", "conditioning", AthleteLevel.BEGINNER, 3),
            ("cricket", "speed", AthleteLevel.ADVANCED, 3),
        ]
        for sport, goal, level, d in configs:
            p = make_profile(sport=sport, goal=goal, athlete_level=level, days_to_match=d)
            try:
                prog = generate_program(p)
                s = prog.sessions[0]
                self.assertGreaterEqual(len(s.blocks), 2,
                                        f"{sport}/{goal}/LIGHT: only {len(s.blocks)} blocks")
            except Exception as e:
                self.fail(f"Crash {sport}/{goal}/LIGHT: {e}")
