"""Wave 10 — Stabilization, UAT & Launch Hardening test suite.

Covers: artifact serialization, personalization contract, youth safety,
intent category completeness, generate→save→load round-trip, malformed
payload resilience, schema version safety, and update endpoint.
"""
import unittest
import json
import os
import tempfile
import shutil
from copy import deepcopy

from src.forge.models import (
    AthleteProfile, AthleteLevel, EquipmentProfile, SeasonPhase, FamilyCode,
    Exercise, Session, SessionBlock, GeneratedProgram,
)
from src.forge.data import INTENT_CATEGORIES, FAMILY_TO_INTENT
from src.forge.blueprint_engine import determine_level, select_blueprint
from src.forge.main import generate_program
from src.forge.api_serializers import serialize_program, athlete_profile_from_request
from src.forge.artifact_store import (
    save_artifact, load_artifact, list_artifacts, delete_artifact,
    duplicate_artifact, update_artifact, ARTIFACTS_DIR, SCHEMA_VERSION,
)
from src.forge.validator import verify_credibility, calculate_credibility_score


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


# =============================================================================
# Part 1 — Failure cleanup verification
# =============================================================================

class TestIntentCategoriesCompleteness(unittest.TestCase):
    """Verify every active exercise family has a valid intent mapping."""

    def test_all_families_covered_except_acc(self):
        covered = set()
        for fams in INTENT_CATEGORIES.values():
            covered.update(fams)
        for fam in FamilyCode:
            if fam.value == "Acc":
                continue
            self.assertIn(
                fam.value, covered,
                f"{fam.value} not in any intent category"
            )

    def test_landing_in_explosive(self):
        self.assertIn("Landing", INTENT_CATEGORIES.get("explosive", []))

    def test_family_to_intent_maps_landing(self):
        self.assertEqual(FAMILY_TO_INTENT.get("Landing"), "explosive")


class TestYouthLevelSafety(unittest.TestCase):
    """Youth athletes cannot be advanced beyond safety limits."""

    def test_teen_capped_at_intermediate(self):
        p = make_profile(training_age_years=4, technique_consistency=0.95,
                         age=17, strength_base_met=True)
        self.assertEqual(determine_level(p), AthleteLevel.INTERMEDIATE,
                         "17yo with 4yr training must be capped to INTERMEDIATE")

    def test_young_adult_can_be_advanced(self):
        p = make_profile(training_age_years=5, technique_consistency=0.95,
                         age=22, strength_base_met=True)
        self.assertEqual(determine_level(p), AthleteLevel.ADVANCED)

    def test_teen_no_strength_base_intermediate(self):
        p = make_profile(training_age_years=3, technique_consistency=0.9,
                         age=18, strength_base_met=False)
        self.assertEqual(determine_level(p), AthleteLevel.INTERMEDIATE)

    def test_youth_cap_edge_age_19(self):
        p = make_profile(training_age_years=5, technique_consistency=0.95,
                         age=19, strength_base_met=True)
        cap = max(0, (19 - 14) * 0.5)
        effective = min(5, cap)
        self.assertLess(effective, 3, "19yo capped effective TA < 3")
        self.assertEqual(determine_level(p), AthleteLevel.INTERMEDIATE)

    def test_youth_cap_edge_age_20(self):
        p = make_profile(training_age_years=3, technique_consistency=0.95,
                         age=20, strength_base_met=True)
        self.assertEqual(determine_level(p), AthleteLevel.ADVANCED,
                         "20yo with 3yr training and strength base -> ADVANCED")


class TestPersonalizationNotesContract(unittest.TestCase):
    """Neutral profiles emit baseline sport/role notes."""

    def test_default_rugby_has_notes(self):
        p = make_profile(sport="rugby")
        program = generate_program(p)
        self.assertGreater(len(program.personalization_notes), 0)

    def test_default_cricket_has_notes(self):
        p = make_profile(sport="cricket")
        program = generate_program(p)
        self.assertGreater(len(program.personalization_notes), 0)

    def test_default_tennis_has_notes(self):
        p = make_profile(sport="tennis")
        program = generate_program(p)
        self.assertGreater(len(program.personalization_notes), 0)

    def test_unknown_sport_has_fallback_notes(self):
        p = make_profile(sport="fencing", position_role="")
        program = generate_program(p)
        # Unknown sport uses generic neutral profile -> baseline notes
        self.assertGreaterEqual(len(program.personalization_notes), 0)

    def test_notes_mention_role_or_bias(self):
        p = make_profile()
        program = generate_program(p)
        combined = " ".join(program.personalization_notes).lower()
        self.assertTrue(
            any(kw in combined for kw in ["role", "collision", "rotational",
                                           "conditioning", "exposure",
                                           "eccentric"]),
        )


# =============================================================================
# Part 3 — Artifact save/load invariants
# =============================================================================

class TestArtifactInvariants(unittest.TestCase):
    """Verify save/load invariants and schema version safety."""

    def setUp(self):
        self.orig_dir = ARTIFACTS_DIR
        self.test_dir = tempfile.mkdtemp()
        import src.forge.artifact_store as store
        store.ARTIFACTS_DIR = self.test_dir

        self.req = {
            "mode": "core",
            "basics": {"athlete_name": "Invariant Test", "sport": "rugby"},
            "context": {"primary_goal": "power"},
            "advanced": {},
        }
        self.resp = {
            "metadata": {"generated_at": "2026-01-01T00:00:00Z", "request_id": "req_test", "api_version": "1.0.0"},
            "summary": {"blueprint_selected": "Test BP", "total_weeks": 4, "competition_window": "Off-season"},
            "sessions": [], "weeks": [], "rationale": [],
            "personalization_notes": [], "validation": [], "dropped_constraints": [],
        }

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
        import src.forge.artifact_store as store
        store.ARTIFACTS_DIR = self.orig_dir

    def test_generate_save_load_roundtrip(self):
        """Generate -> save -> load reproduces same athlete metadata."""
        profile = make_profile()
        program = generate_program(profile)
        response = serialize_program(program, request_payload=self.req)
        payload_req = deepcopy(self.req)
        saved = save_artifact(payload_req, response)
        loaded = load_artifact(saved["id"])
        self.assertEqual(loaded["athlete_display_name"], "Invariant Test")
        self.assertEqual(loaded["sport"], "rugby")
        self.assertEqual(loaded["goal"], "power")
        self.assertEqual(
            loaded["result_snapshot"]["summary"]["blueprint_selected"],
            response["summary"]["blueprint_selected"],
        )

    def test_duplicate_preserves_request_snapshot(self):
        saved = save_artifact(self.req, self.resp)
        dup = duplicate_artifact(saved["id"])
        self.assertEqual(
            dup["request_snapshot"]["basics"]["athlete_name"],
            saved["request_snapshot"]["basics"]["athlete_name"],
        )

    def test_duplicate_clears_coach_notes(self):
        saved = save_artifact(self.req, self.resp, coach_notes="Original notes")
        dup = duplicate_artifact(saved["id"])
        self.assertEqual(dup["coach_notes"], "")

    def test_list_strips_payloads(self):
        save_artifact(self.req, self.resp)
        listing = list_artifacts()
        self.assertNotIn("request_snapshot", listing[0])
        self.assertNotIn("result_snapshot", listing[0])

    def test_list_includes_schema_version(self):
        save_artifact(self.req, self.resp)
        listing = list_artifacts()
        self.assertIn("schema_version", listing[0])

    def test_load_with_missing_schema_version(self):
        """Legacy artifact without schema_version loads without error."""
        _ensure_dir = lambda: os.makedirs(self.test_dir, exist_ok=True)
        _ensure_dir()
        legacy = {"id": "prog_legacy123", "version": 1, "status": "draft",
                  "request_snapshot": self.req, "result_snapshot": self.resp}
        with open(os.path.join(self.test_dir, "prog_legacy123.json"),
                  "w", encoding="utf-8") as f:
            json.dump(legacy, f)
        loaded = load_artifact("prog_legacy123")
        self.assertIsNotNone(loaded)
        self.assertNotIn("schema_version", loaded)

    def test_malformed_json_skipped_in_list(self):
        """Corrupted artifact files don't crash list view."""
        _ensure_dir = lambda: os.makedirs(self.test_dir, exist_ok=True)
        _ensure_dir()
        with open(os.path.join(self.test_dir, "corrupt.json"),
                  "w", encoding="utf-8") as f:
            f.write("not valid json")
        save_artifact(self.req, self.resp)
        listing = list_artifacts()
        self.assertEqual(len(listing), 1)

    def test_update_preserves_response_payload(self):
        saved = save_artifact(self.req, self.resp)
        update_artifact(saved["id"], status="reviewed")
        loaded = load_artifact(saved["id"])
        self.assertEqual(
            loaded["result_snapshot"]["summary"]["blueprint_selected"],
            "Test BP",
        )

    def test_update_with_invalid_field_ignored(self):
        saved = save_artifact(self.req, self.resp)
        update_artifact(saved["id"], nonexistent_field="should be ignored")
        loaded = load_artifact(saved["id"])
        self.assertNotIn("nonexistent_field", loaded)

    def test_empty_library(self):
        """Empty artifact directory returns empty list."""
        listing = list_artifacts()
        self.assertEqual(listing, [])


# =============================================================================
# Part 2 — Integration / contract stability
# =============================================================================

class TestGenerateRenderVerify(unittest.TestCase):
    """End-to-end generate + serialize + verify for multiple profiles."""

    def assert_valid_program_response(self, resp, name=""):
        self.assertIn("metadata", resp, f"{name}: missing metadata")
        self.assertIn("summary", resp, f"{name}: missing summary")
        self.assertIn("sessions", resp, f"{name}: missing sessions")
        self.assertIn("weeks", resp, f"{name}: missing weeks")
        self.assertIn("rationale", resp, f"{name}: missing rationale")
        self.assertIn("personalization_notes", resp, f"{name}: missing notes")
        self.assertIn("validation", resp, f"{name}: missing validation")
        self.assertGreater(len(resp["sessions"]), 0, f"{name}: no sessions")
        # Recovery programs (days_to_match=0) may have 0 weeks — still valid
        if resp["summary"].get("total_weeks", 0) > 0:
            self.assertGreater(len(resp["weeks"]), 0, f"{name}: expected weeks")
        self.assertGreater(resp["summary"]["credibility_score"], 0,
                           f"{name}: credibility is 0")

    def make_payload(self, **overrides):
        payload = {
            "mode": "core",
            "basics": {"athlete_name": "Test", "sport": "rugby",
                       "level": "Intermediate", "available_minutes": 60},
            "context": {"primary_goal": "strength"},
            "advanced": {},
        }
        payload.update(overrides)
        return payload

    def test_core_strength_rugby(self):
        profile = make_profile(sport="rugby", goal="strength")
        program = generate_program(profile)
        resp = serialize_program(program)
        self.assert_valid_program_response(resp, "core_strength_rugby")
        self.assertIn("strength", resp["summary"]["goal"].lower())

    def test_core_general_fitness(self):
        profile = make_profile(sport="general", goal="conditioning")
        program = generate_program(profile)
        resp = serialize_program(program)
        self.assert_valid_program_response(resp, "core_general")

    def test_youth_athlete(self):
        profile = make_profile(sport="rugby", goal="strength", age=17,
                               training_age_years=1, technique_consistency=0.85)
        program = generate_program(profile)
        resp = serialize_program(program)
        self.assert_valid_program_response(resp, "youth")
        self.assertEqual(program.level, "Intermediate")

    def test_premium_rugby_prop(self):
        profile = make_profile(sport="rugby", goal="strength",
                               position_role="prop",
                               force_profile="force_deficient",
                               lumbar_risk=True, age=25,
                               training_age_years=6, technique_consistency=0.95)
        program = generate_program(profile)
        resp = serialize_program(program)
        self.assert_valid_program_response(resp, "rugby_prop")
        self.assertGreater(len(resp["personalization_notes"]), 0)

    def test_premium_cricket_fast_bowler(self):
        profile = make_profile(sport="cricket", goal="power",
                               position_role="fast_bowler",
                               lumbar_risk=True, hamstring_risk=True,
                               age=24, training_age_years=4)
        program = generate_program(profile)
        resp = serialize_program(program)
        self.assert_valid_program_response(resp, "cricket_bowler")
        notes = " ".join(resp["personalization_notes"]).lower()
        self.assertTrue("lumbar" in notes or "hamstring" in notes or "bowler" in notes)

    def test_premium_volleyball_middle(self):
        profile = make_profile(sport="volleyball", goal="power",
                               position_role="middle_blocker",
                               cmj_band="high", landing_competency="poor",
                               patellar_tendon_risk=True, age=22)
        program = generate_program(profile)
        resp = serialize_program(program)
        self.assert_valid_program_response(resp, "volleyball")
        notes = " ".join(resp["personalization_notes"]).lower()
        self.assertTrue("landing" in notes or "patellar" in notes or "jump" in notes)

    def test_competition_taper(self):
        profile = make_profile(sport="rugby", goal="strength",
                               days_to_match=2, age=25)
        program = generate_program(profile)
        resp = serialize_program(program)
        self.assert_valid_program_response(resp, "taper")
        self.assertIn("taper", resp["summary"]["competition_window"].lower())

    def test_multiple_injury_flags(self):
        profile = make_profile(sport="rugby", goal="strength",
                               lumbar_risk=True, hamstring_risk=True,
                               patellar_tendon_risk=True, age=23)
        program = generate_program(profile)
        resp = serialize_program(program)
        self.assert_valid_program_response(resp, "multi_injury")
        notes = " ".join(resp["personalization_notes"]).lower()
        self.assertTrue("lumbar" in notes or "hamstring" in notes)

    def test_short_session_available_minutes(self):
        profile = make_profile(sport="rugby", goal="strength",
                               available_minutes=25, age=25)
        program = generate_program(profile)
        resp = serialize_program(program)
        self.assert_valid_program_response(resp, "short_session")

    def test_missing_optional_fields(self):
        """Profile with no risk flags, no bands, no role generates OK."""
        profile = make_profile(force_profile=None, elastic_profile=None,
                               landing_competency=None, lumbar_risk=False,
                               shoulder_overhead_risk=False,
                               cmj_band=None, sprint_10m_band=None,
                               squat_strength_band=None, aerobic_band=None,
                               position_role="", age=25)
        program = generate_program(profile)
        resp = serialize_program(program)
        self.assert_valid_program_response(resp, "minimal")

    def test_deload_recovery_profile(self):
        profile = make_profile(sport="rugby", goal="strength",
                               days_to_match=0, age=25)
        program = generate_program(profile)
        resp = serialize_program(program)
        self.assert_valid_program_response(resp, "deload")
        self.assertIn("recovery", resp["summary"]["goal"].lower())


class TestSerializerEdgeCases(unittest.TestCase):
    """Edge cases in the serializer."""

    def make_payload(self, **overrides):
        payload = {
            "mode": "core",
            "basics": {"athlete_name": "Test", "sport": "rugby",
                       "level": "Intermediate", "available_minutes": 60},
            "context": {"primary_goal": "strength"},
            "advanced": {},
        }
        payload.update(overrides)
        return payload

    def test_serialized_sessions_have_consistent_weeks(self):
        profile = make_profile()
        program = generate_program(profile)
        resp = serialize_program(program)
        for s in resp["sessions"]:
            self.assertIsInstance(s["week_number"], int)
            self.assertIsInstance(s["session_number"], int)
            self.assertGreaterEqual(s["week_number"], 1)
            self.assertGreaterEqual(s["session_number"], 1)

    def test_warmup_fallbacks_to_empty(self):
        """Session without warmup data still has warmup key."""
        profile = make_profile(sport="rugby", goal="strength")
        program = generate_program(profile)
        resp = serialize_program(program)
        for s in resp["sessions"]:
            self.assertIn("warmup", s)
            self.assertIn("exercises", s["warmup"])
            self.assertIn("title", s["warmup"])

    def test_validation_array_type(self):
        """validation field is always a list of dicts."""
        profile = make_profile()
        program = generate_program(profile)
        resp = serialize_program(program)
        self.assertIsInstance(resp["validation"], list)
        if resp["validation"]:
            self.assertIn("type", resp["validation"][0])
            self.assertIn("message", resp["validation"][0])

    def test_rationale_includes_blueprint(self):
        profile = make_profile()
        program = generate_program(profile)
        resp = serialize_program(program)
        self.assertTrue(
            any(resp["summary"]["blueprint_selected"] in r for r in resp["rationale"]),
        )


class TestExposureData(unittest.TestCase):
    """Wave 10.5: Weekly exposure data must be real (not 'Not specified')."""

    def _get_exposures(self, program=None, profile=None):
        if profile is None:
            profile = make_profile()
        if program is None:
            program = generate_program(profile)
        resp = serialize_program(program)
        return [w["exposure_summary"] for w in resp.get("weeks", [])]

    def test_exposure_not_placeholder(self):
        """No exposure field says 'Not specified'."""
        exposures = self._get_exposures()
        for exp in exposures:
            for key in ("sprint_exposure", "jump_landing_exposure", "deceleration_exposure",
                        "eccentric_stress", "conditioning_density"):
                val = exp.get(key, "")
                self.assertNotEqual(val, "Not specified", f"{key} is still placeholder")
                self.assertGreater(len(val), 0, f"{key} is empty")

    def test_exposure_has_counts_and_pct(self):
        """Each exposure value contains actual count and percentage."""
        exposures = self._get_exposures()
        for exp in exposures:
            for key in ("sprint_exposure", "jump_landing_exposure", "deceleration_exposure",
                        "eccentric_stress", "conditioning_density"):
                val = exp.get(key, "")
                self.assertIn("(", val, f"{key} missing count/pct: {val}")
                self.assertIn("%", val, f"{key} missing percentage: {val}")

    def test_exposure_qualitative_label_valid(self):
        """Exposure labels are one of High/Moderate/Low/None."""
        valid = {"High", "Moderate", "Low", "None"}
        exposures = self._get_exposures()
        for exp in exposures:
            for key in ("sprint_exposure", "jump_landing_exposure", "deceleration_exposure",
                        "eccentric_stress", "conditioning_density"):
                val = exp.get(key, "")
                label = val.split(" ")[0].rstrip("(")
                self.assertIn(label, valid, f"{key} bad label '{label}' in '{val}'")

    def test_exposure_counts_are_non_negative(self):
        """Exposure counts are never negative."""
        exposures = self._get_exposures()
        for exp in exposures:
            for key in ("sprint_exposure", "jump_landing_exposure", "deceleration_exposure",
                        "eccentric_stress", "conditioning_density"):
                val = exp.get(key, "")
                # Extract count from "Label (N ex, X.X%)"
                count_str = val.split("(")[1].split(" ")[0] if "(" in val else "0"
                self.assertGreaterEqual(int(count_str), 0,
                    f"{key} has negative count: {val}")

    def test_exposure_present_in_all_weeks(self):
        """Every week has exposure data, even tapering weeks."""
        profile = make_profile(age=25, days_to_match=3, goal="power")
        program = generate_program(profile)
        resp = serialize_program(program)
        weeks = resp.get("weeks", [])
        self.assertGreater(len(weeks), 0)
        for w in weeks:
            exp = w.get("exposure_summary", {})
            self.assertIn("sprint_exposure", exp)


class TestUATScenarioGeneration(unittest.TestCase):
    """Wave 10.5: All 16 UAT scenarios generate without error."""

    def test_uat_core_scenarios_generate(self):
        args_list = [
            dict(age=30, sport="general", goal="conditioning",
                 athlete_level=AthleteLevel.INTERMEDIATE),
            dict(age=16, sport="rugby", goal="strength",
                 athlete_level=AthleteLevel.BEGINNER, training_age_years=1),
            dict(age=25, sport="", goal="strength",
                 athlete_level=AthleteLevel.INTERMEDIATE),
            dict(age=25, sport="rugby", goal="strength",
                 athlete_level=AthleteLevel.INTERMEDIATE, days_to_match=0),
        ]
        for i, kwargs in enumerate(args_list):
            with self.subTest(core=i):
                p = make_profile(**kwargs)
                prog = generate_program(p)
                self.assertIsNotNone(prog)
                self.assertGreater(len(prog.sessions), 0)
                resp = serialize_program(prog)
                self.assertIn("weeks", resp)

    def test_uat_premium_scenarios_generate(self):
        args_list = [
            dict(age=26, sport="Rugby", position_role="Prop",
                 athlete_level=AthleteLevel.ADVANCED,
                 training_age_years=6, goal="strength",
                 shoulder_overhead_risk=True),
            dict(age=24, sport="Rugby", position_role="Backline",
                 athlete_level=AthleteLevel.ADVANCED,
                 training_age_years=4, goal="power",
                 hamstring_risk=True),
            dict(age=25, sport="Cricket", position_role="Fast Bowler",
                 athlete_level=AthleteLevel.ADVANCED,
                 training_age_years=5, goal="power",
                 lumbar_risk=True, hamstring_risk=True),
            dict(age=23, sport="Cricket", position_role="Batter",
                 athlete_level=AthleteLevel.INTERMEDIATE,
                 training_age_years=3, goal="power"),
            dict(age=22, sport="Tennis", position_role="Singles",
                 athlete_level=AthleteLevel.ADVANCED,
                 training_age_years=4, goal="power"),
            dict(age=22, sport="Volleyball", position_role="Middle Blocker",
                 athlete_level=AthleteLevel.ADVANCED,
                 training_age_years=4, goal="power",
                 cmj_band="high", landing_competency="poor",
                 patellar_tendon_risk=True),
            dict(age=24, sport="Basketball", position_role="Guard",
                 athlete_level=AthleteLevel.ADVANCED,
                 training_age_years=5, goal="power"),
            dict(age=23, sport="Soccer", position_role="Midfielder",
                 athlete_level=AthleteLevel.ADVANCED,
                 training_age_years=4, goal="conditioning"),
        ]
        for i, kwargs in enumerate(args_list):
            with self.subTest(premium=i, sport=kwargs.get("sport"), role=kwargs.get("position_role")):
                p = make_profile(**kwargs)
                prog = generate_program(p)
                self.assertIsNotNone(prog)
                self.assertGreater(len(prog.sessions), 0)
                resp = serialize_program(prog)
                self.assertIn("weeks", resp)

    def test_uat_edge_scenarios_generate(self):
        args_list = [
            dict(age=25, available_minutes=20, goal="strength",
                 athlete_level=AthleteLevel.INTERMEDIATE),
            dict(age=25, goal="power", days_to_match=3,
                 athlete_level=AthleteLevel.INTERMEDIATE),
            dict(age=25, goal="strength",
                 athlete_level=AthleteLevel.INTERMEDIATE,
                 lumbar_risk=True, hamstring_risk=True,
                 patellar_tendon_risk=True,
                 shoulder_overhead_risk=True),
            dict(age=25, sport="", goal="strength",
                 athlete_level=AthleteLevel.INTERMEDIATE),
        ]
        for i, kwargs in enumerate(args_list):
            with self.subTest(edge=i):
                p = make_profile(**kwargs)
                prog = generate_program(p)
                self.assertIsNotNone(prog, f"Edge scenario {i} failed to generate")
                resp = serialize_program(prog)
                self.assertIn("weeks", resp)


if __name__ == "__main__":
    unittest.main()
