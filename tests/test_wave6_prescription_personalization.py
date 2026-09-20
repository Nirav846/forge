"""Wave 6 — Prescription Personalization & Role-Specific Hardening tests."""
import unittest
from src.forge.models import (
    AthleteProfile, AthleteLevel, EquipmentProfile, SeasonPhase,
    FamilyCode, Session, GeneratedProgram,
    PrescriptionRole,
)
from src.forge.data import EXERCISE_BY_ID, SELECTION_PRIORITIES
from src.forge.main import generate_program
from src.forge.prescription_rules import (
    get_prescription, derive_role,
)
from src.forge.athlete_profile_rules import (
    get_role_exercise_bias,
)
from src.forge.renderer import render_coach_program
from src.forge.validator import verify_credibility


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


# ── A: Prescription personalization by athlete profile ────────────

class TestPrescriptionPersonalization(unittest.TestCase):

    def test_force_deficient_prescription_lower_reps(self):
        """Force-deficient athlete should get lower rep ranges on main strength."""
        p = make_profile(force_profile="force_deficient")
        # Find a main strength exercise
        ex = None
        for e in EXERCISE_BY_ID.values():
            if e.family in (FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.SLKD, FamilyCode.SLHD):
                ex = e
                break
        self.assertIsNotNone(ex)
        presc = get_prescription(ex, AthleteLevel.INTERMEDIATE, 1, athlete_profile=p)
        # Should have lower reps (shifted down: 6-8 -> 5-7)
        self.assertIn("5-7", presc.reps)

    def test_velocity_deficient_prescription_velocity_bias(self):
        """Velocity-deficient athlete should get velocity-friendly prescriptions."""
        p = make_profile(force_profile="velocity_deficient")
        ex = None
        for e in EXERCISE_BY_ID.values():
            if e.family in (FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.SLKD, FamilyCode.SLHD):
                ex = e
                break
        self.assertIsNotNone(ex)
        presc = get_prescription(ex, AthleteLevel.INTERMEDIATE, 1, athlete_profile=p)
        # Should have velocity-friendly intensity note
        self.assertIn("velocity", presc.intensity_note.lower())

    def test_landing_competency_poor_prescription_caps(self):
        """Poor landing athlete should get capped plyo prescriptions."""
        p = make_profile(landing_competency="poor")
        ex = EXERCISE_BY_ID["Plyo-004"]  # Depth Jump
        presc = get_prescription(ex, AthleteLevel.INTERMEDIATE, 1, athlete_profile=p)
        # Should have low-reactive note
        self.assertIn("low-reactive", presc.intensity_note.lower())

    def test_patellar_tendon_risk_prescription_caps(self):
        """Patellar tendon risk should cap plyo."""
        p = make_profile(patellar_tendon_risk=True)
        ex = EXERCISE_BY_ID["Plyo-004"]  # Depth Jump - plyometric
        presc = get_prescription(ex, AthleteLevel.INTERMEDIATE, 1, athlete_profile=p)
        self.assertIn("low-impact", presc.intensity_note.lower())

    def test_hamstring_risk_prescription_caps(self):
        """Hamstring risk should cap sprint density."""
        p = make_profile(hamstring_risk=True)
        ex = EXERCISE_BY_ID["Sprint-012"]  # Max-V Sprint
        presc = get_prescription(ex, AthleteLevel.INTERMEDIATE, 1, athlete_profile=p)
        self.assertIn("controlled", presc.intensity_note.lower())

    def test_lumbar_risk_prescription_caps(self):
        """Lumbar risk should affect hinge prescriptions."""
        p = make_profile(lumbar_risk=True)
        ex = EXERCISE_BY_ID["DLHD-006"]  # RDL
        presc = get_prescription(ex, AthleteLevel.INTERMEDIATE, 1, athlete_profile=p)
        self.assertIn("lumbar", presc.intensity_note.lower())

    def test_athlete_profile_prescription_notes(self):
        """Program should have personalization notes for athlete profile."""
        p = make_profile(force_profile="force_deficient", landing_competency="poor")
        program = generate_program(p)
        self.assertGreater(len(program.personalization_notes), 0)
        # Should have at least one note about force-deficient or landing
        notes_lower = [n.lower() for n in program.personalization_notes]
        self.assertTrue(
            any("force-deficient" in n or "landing" in n for n in notes_lower)
        )


# ── B: Role / position-specific bias ─────────────────────────────────

class TestRoleSpecificBias(unittest.TestCase):

    def test_role_exercise_bias(self):
        """Role should bias exercise selection."""
        bias = get_role_exercise_bias("prop", "DLKD", "rugby")
        self.assertGreater(bias, 0)  # Prop should prefer DLKD
        bias2 = get_role_exercise_bias("backline", "DLKD", "rugby")
        self.assertLess(bias2, 0)  # Backline should avoid DLKD

    def test_role_prescription_modifiers(self):
        """Role should affect prescription."""
        from src.forge.prescription_rules import get_role_prescription_modifiers
        mods = get_role_prescription_modifiers("prop", "rugby", PrescriptionRole.MAIN_STRENGTH)
        self.assertIn("intensity_note_bias", mods)

    def test_role_prescription_notes(self):
        """Program should have role-based notes."""
        p = make_profile(sport="rugby", position_role="prop")
        program = generate_program(p)
        self.assertGreater(len(program.personalization_notes), 0)
        notes_lower = [n.lower() for n in program.personalization_notes]
        self.assertTrue(
            any("prop" in n or "rugby" in n for n in notes_lower)
        )

    def test_role_prescription_interaction(self):
        """Role + profile should combine in prescriptions."""
        p = make_profile(sport="rugby", position_role="prop", force_profile="force_deficient")
        program = generate_program(p)
        # Should have both force-deficient and prop notes
        notes_lower = [n.lower() for n in program.personalization_notes]
        self.assertTrue(
            any("force-deficient" in n for n in notes_lower)
        )
        self.assertTrue(
            any("prop" in n or "rugby" in n for n in notes_lower)
        )


# ── C: Renderer / validator integration ─────────────────────────────────

class TestRendererAndValidator(unittest.TestCase):

    def test_coach_program_shows_prescription_personalization(self):
        """Coach output should show prescription personalization notes."""
        p = make_profile(force_profile="force_deficient")
        program = generate_program(p)
        output = render_coach_program(program)
        self.assertIn("Personalization Notes", output)
        self.assertIn("force-deficient", output.lower())

    def test_prescription_athlete_aware_validator(self):
        """Validator should check athlete-aware prescriptions."""
        p = make_profile(force_profile="force_deficient")
        program = generate_program(p)
        # Get first session for validation
        session = program.sessions[0]
        check = verify_credibility(session, p)
        # Should have prescription_athlete_aware check
        self.assertIn("prescription_athlete_aware", check)

    def test_role_bias_validator(self):
        """Validator should check role bias application."""
        p = make_profile(position_role="prop")
        program = generate_program(p)
        session = program.sessions[0]
        check = verify_credibility(session, p)
        # Should have role_bias_applied check
        self.assertIn("role_bias_applied", check)


# ── D: Same blueprint, different profiles/roles diverge ───────────────

class TestSameBlueprintDivergence(unittest.TestCase):

    def test_force_deficient_vs_velocity_deficient_prescriptions(self):
        """Same blueprint, different force profiles should get different prescriptions."""
        p1 = make_profile(sport="rugby", goal="strength", force_profile="force_deficient")
        p2 = make_profile(sport="rugby", goal="strength", force_profile="velocity_deficient")
        prog1 = generate_program(p1)
        prog2 = generate_program(p2)
        # Should have different personalization notes
        self.assertNotEqual(
            [n.lower() for n in prog1.personalization_notes],
            [n.lower() for n in prog2.personalization_notes],
        )

    def test_prop_vs_backline_prescriptions(self):
        """Same blueprint, different roles should get different prescriptions."""
        p1 = make_profile(sport="rugby", position_role="prop")
        p2 = make_profile(sport="rugby", position_role="backline")
        prog1 = generate_program(p1)
        prog2 = generate_program(p2)
        # Should have different personalization notes
        self.assertNotEqual(
            [n.lower() for n in prog1.personalization_notes],
            [n.lower() for n in prog2.personalization_notes],
        )

    def test_role_profile_interaction_prescriptions(self):
        """Role + profile interaction should affect prescriptions."""
        p1 = make_profile(sport="rugby", position_role="prop", force_profile="force_deficient")
        p2 = make_profile(sport="rugby", position_role="prop", force_profile="velocity_deficient")
        prog1 = generate_program(p1)
        prog2 = generate_program(p2)
        # Should have different personalization notes
        self.assertNotEqual(
            [n.lower() for n in prog1.personalization_notes],
            [n.lower() for n in prog2.personalization_notes],
        )


# ── E: Backward compatibility ─────────────────────────────────────────

class TestBackwardCompatibility(unittest.TestCase):

    def test_no_profile_no_crash(self):
        """Programs without athlete profile should still work."""
        p = make_profile()
        # Remove profile fields
        p.force_profile = None
        p.landing_competency = None
        p.position_role = None
        program = generate_program(p)
        self.assertGreater(len(program.sessions), 0)

    def test_old_prescription_still_works(self):
        """Old prescription logic should still work."""
        p = make_profile()
        ex = EXERCISE_BY_ID["DLKD-004"]  # Barbell Back Squat
        presc = get_prescription(ex, AthleteLevel.INTERMEDIATE, 1)
        self.assertIsNotNone(presc)
        self.assertGreaterEqual(int(presc.reps.split('-')[0]), 6)

    def test_missing_role_no_crash(self):
        """Missing role should not crash."""
        p = make_profile()
        p.position_role = None
        program = generate_program(p)
        self.assertGreater(len(program.sessions), 0)


if __name__ == "__main__":
    unittest.main()
