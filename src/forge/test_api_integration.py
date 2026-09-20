"""Tests for the FORGE API integration layer."""
import unittest
import json
import os
import tempfile
import shutil
from unittest.mock import patch

from src.forge.api_serializers import (
    serialize_program,
    athlete_profile_from_request,
    _map_fv_profile,
    _map_band,
)
from src.forge.artifact_store import (
    save_artifact,
    load_artifact,
    list_artifacts,
    delete_artifact,
    duplicate_artifact,
    update_artifact,
    ARTIFACTS_DIR,
    SCHEMA_VERSION,
)
from src.forge.main import generate_program


class TestAPISerializers(unittest.TestCase):
    """Test the API serializer functions."""

    def setUp(self):
        self.core_payload = {
            "mode": "core",
            "basics": {
                "athlete_name": "Test Athlete",
                "sport": "rugby",
                "level": "Intermediate",
                "frequency_per_week": 3,
                "available_minutes": 60,
            },
            "context": {"primary_goal": "strength"},
            "advanced": {},
        }

        self.premium_payload = {
            "mode": "premium",
            "basics": {
                "athlete_name": "Pro Player",
                "sport": "tennis",
                "role": "Singles Player",
                "age": 24,
                "level": "Advanced",
                "training_age_years": 5,
                "frequency_per_week": 4,
                "available_minutes": 45,
                "days_to_match": 14,
                "environment": "Commercial Gym",
            },
            "context": {
                "primary_goal": "power",
                "current_phase": "Pre-Season",
            },
            "advanced": {
                "force_velocity_profile": "Velocity Deficit",
                "sprint_10m_band": "<1.65s",
                "aerobic_band": "Elite",
                "squat_strength_band": "1.5x BW",
                "cmj_band": "High",
                "technique_consistency": "High",
                "injury_risk_flags": ["Right Shoulder", "Lumbar Spine"],
                "prior_block_summary": "Responded well to cluster sets.",
            },
        }

    def test_athlete_profile_from_request_core(self):
        """Core request maps to AthleteProfile with defaults."""
        profile = athlete_profile_from_request(self.core_payload)
        self.assertEqual(profile.sport, "rugby")
        self.assertEqual(profile.goal, "strength")
        self.assertIsNone(profile.force_profile)
        self.assertFalse(profile.lumbar_risk)
        self.assertEqual(profile.available_minutes, 60)

    def test_athlete_profile_from_request_premium(self):
        """Premium request maps all fields correctly."""
        profile = athlete_profile_from_request(self.premium_payload)
        self.assertEqual(profile.sport, "tennis")
        self.assertEqual(profile.goal, "power")
        self.assertEqual(profile.position_role, "Singles Player")
        self.assertEqual(profile.force_profile, "velocity_deficient")
        self.assertEqual(profile.sprint_10m_band, "low")
        self.assertEqual(profile.aerobic_band, "high")
        self.assertEqual(profile.squat_strength_band, "avg")
        self.assertEqual(profile.cmj_band, "high")
        self.assertTrue(profile.shoulder_overhead_risk)
        self.assertTrue(profile.lumbar_risk)
        self.assertEqual(profile.days_to_match, 14)

    def test_athlete_profile_empty_payload(self):
        """Empty payload should produce a valid AthleteProfile."""
        profile = athlete_profile_from_request({})
        self.assertEqual(profile.sport, "athlete")
        self.assertEqual(profile.goal, "strength")
        self.assertEqual(profile.available_minutes, 60)

    def test_athlete_profile_minimal_payload(self):
        """Minimal payload (just athlete_name) should work."""
        payload = {
            "mode": "core",
            "basics": {"athlete_name": "Minimal"},
            "context": {},
            "advanced": {},
        }
        profile = athlete_profile_from_request(payload)
        self.assertEqual(profile.sport, "athlete")
        self.assertIsInstance(profile, object)

    def test_athlete_profile_injury_flags(self):
        """Injury risk flags correctly map to boolean risks."""
        payload = {
            "mode": "core",
            "basics": {"athlete_name": "Injured"},
            "context": {},
            "advanced": {
                "injury_risk_flags": ["Hamstring", "Patellar Tendon", "Lumbar Spine", "Right Shoulder"]
            },
        }
        profile = athlete_profile_from_request(payload)
        self.assertTrue(profile.hamstring_risk)
        self.assertTrue(profile.patellar_tendon_risk)
        self.assertTrue(profile.lumbar_risk)
        self.assertTrue(profile.shoulder_overhead_risk)
        self.assertFalse(profile.ankle_foot_risk)

    def test_serialize_program_has_required_keys(self):
        """Serialized program response has all required top-level keys."""
        profile = athlete_profile_from_request(self.core_payload)
        program = generate_program(profile)
        result = serialize_program(program, self.core_payload)

        required_keys = [
            "metadata", "summary", "weeks", "sessions",
            "rationale", "personalization_notes", "validation", "dropped_constraints",
        ]
        for key in required_keys:
            self.assertIn(key, result, f"Missing key: {key}")

        # Check summary fields
        summary_keys = [
            "blueprint_selected", "total_weeks", "weekly_frequency",
            "conditioning_emphasis", "competition_window", "role_emphasis",
            "level", "goal", "equipment_profile", "credibility_score",
        ]
        for key in summary_keys:
            self.assertIn(key, result["summary"], f"Missing summary key: {key}")

    def test_serialize_program_session_structure(self):
        """Each serialized session has the expected structure."""
        profile = athlete_profile_from_request(self.core_payload)
        program = generate_program(profile)
        result = serialize_program(program, self.core_payload)

        self.assertGreater(len(result["sessions"]), 0)

        session = result["sessions"][0]
        session_keys = [
            "id", "name", "week_number", "session_number", "focus",
            "warmup", "main_work", "conditioning",
            "session_notes", "week_type", "testing_markers",
            "total_duration_min", "load_capped",
        ]
        for key in session_keys:
            self.assertIn(key, session, f"Missing session key: {key}")

        # Check section structure
        for section_key in ["warmup", "main_work", "conditioning"]:
            section = session[section_key]
            self.assertIn("title", section)
            self.assertIn("exercises", section)
            self.assertIsInstance(section["exercises"], list)

    def test_serialize_program_exercise_structure(self):
        """Each exercise in main_work has required fields."""
        profile = athlete_profile_from_request(self.core_payload)
        program = generate_program(profile)
        result = serialize_program(program, self.core_payload)

        for session in result["sessions"]:
            for ex in session["main_work"]["exercises"]:
                for field in ["id", "name", "family", "sets_reps", "loading_method", "rest"]:
                    self.assertIn(field, ex, f"Exercise missing {field}")

    def test_serialize_program_with_days_to_match(self):
        """Program with days_to_match should reflect competition proximity."""
        payload = dict(self.core_payload)
        payload["basics"]["days_to_match"] = 2
        profile = athlete_profile_from_request(payload)
        program = generate_program(profile)
        result = serialize_program(program, payload)

        self.assertIn("taper", result["summary"]["competition_window"].lower())

    def test_serialize_program_recovery(self):
        """days_to_match=0 should generate a recovery program."""
        payload = dict(self.core_payload)
        payload["basics"]["days_to_match"] = 0
        profile = athlete_profile_from_request(payload)
        program = generate_program(profile)
        result = serialize_program(program, payload)

        self.assertIn("recovery", result["summary"]["goal"].lower())

    def test_personalization_notes_included(self):
        """Personalization notes from backend are surfaced in API response."""
        profile = athlete_profile_from_request(self.premium_payload)
        program = generate_program(profile)
        result = serialize_program(program, self.premium_payload)

        # Premium should generate at least some personalization notes
        self.assertGreater(len(result["personalization_notes"]), 0)

    def test_rationale_not_empty(self):
        """Rationale should contain at least the blueprint name."""
        profile = athlete_profile_from_request(self.core_payload)
        program = generate_program(profile)
        result = serialize_program(program, self.core_payload)

        self.assertGreater(len(result["rationale"]), 0)
        self.assertIn(result["summary"]["blueprint_selected"], str(result["rationale"]))

    def test_map_fv_profile(self):
        """Force-velocity profile string mapping."""
        self.assertEqual(_map_fv_profile("Force Deficit"), "force_deficient")
        self.assertEqual(_map_fv_profile("Velocity Deficit"), "velocity_deficient")
        self.assertEqual(_map_fv_profile("Balanced"), "balanced")
        self.assertIsNone(_map_fv_profile(""))
        self.assertIsNone(_map_fv_profile("Unknown"))

    def test_map_band(self):
        """Band string mapping."""
        self.assertEqual(_map_band("Elite (>2.0x BW)"), "high")
        self.assertEqual(_map_band("High"), "high")
        self.assertEqual(_map_band("Solid (1.5x BW)"), "avg")
        self.assertEqual(_map_band("Average"), "avg")
        self.assertEqual(_map_band("<1.65s"), "low")
        self.assertIsNone(_map_band(""))


class TestArtifactStore(unittest.TestCase):
    """Test the JSON file-based artifact store."""

    def setUp(self):
        self.orig_dir = ARTIFACTS_DIR
        self.test_dir = tempfile.mkdtemp()

        import src.forge.artifact_store as store
        store.ARTIFACTS_DIR = self.test_dir

        self.request_payload = {
            "mode": "core",
            "basics": {"athlete_name": "Store Test", "sport": "cricket"},
            "context": {"primary_goal": "conditioning"},
            "advanced": {},
        }
        self.response_payload = {
            "metadata": {"generated_at": "2026-01-01T00:00:00Z", "request_id": "req_test", "api_version": "1.0.0"},
            "summary": {"blueprint_selected": "Test Blueprint", "total_weeks": 4},
            "sessions": [],
            "weeks": [],
            "rationale": [],
            "personalization_notes": [],
            "validation": [],
            "dropped_constraints": [],
        }

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
        import src.forge.artifact_store as store
        store.ARTIFACTS_DIR = self.orig_dir

    def test_save_and_load_artifact(self):
        """Save an artifact, then load it back."""
        saved = save_artifact(self.request_payload, self.response_payload)
        self.assertIn("id", saved)
        self.assertEqual(saved["sport"], "cricket")

        loaded = load_artifact(saved["id"])
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["id"], saved["id"])
        self.assertEqual(loaded["request_snapshot"]["basics"]["sport"], "cricket")

    def test_list_artifacts(self):
        """Saved artifacts appear in the list."""
        save_artifact(self.request_payload, self.response_payload)
        save_artifact(self.request_payload, self.response_payload)
        listing = list_artifacts()
        self.assertEqual(len(listing), 2)

    def test_list_artifacts_strips_payloads(self):
        """List view should not include full payloads."""
        save_artifact(self.request_payload, self.response_payload)
        listing = list_artifacts()
        self.assertNotIn("request_snapshot", listing[0])
        self.assertNotIn("result_snapshot", listing[0])

    def test_delete_artifact(self):
        """Delete removes the artifact."""
        saved = save_artifact(self.request_payload, self.response_payload)
        self.assertTrue(delete_artifact(saved["id"]))
        self.assertIsNone(load_artifact(saved["id"]))

    def test_delete_nonexistent(self):
        """Delete of nonexistent returns False."""
        self.assertFalse(delete_artifact("nonexistent"))

    def test_duplicate_artifact(self):
        """Duplicate creates a new artifact with incremented version."""
        saved = save_artifact(self.request_payload, self.response_payload)
        dup = duplicate_artifact(saved["id"])
        self.assertIsNotNone(dup)
        self.assertNotEqual(dup["id"], saved["id"])
        self.assertEqual(dup["duplicated_from"], saved["id"])
        self.assertEqual(dup["version"], saved["version"] + 1)
        self.assertEqual(dup["request_snapshot"]["basics"]["sport"], "cricket")

    def test_duplicate_nonexistent(self):
        """Duplicate of nonexistent returns None."""
        self.assertIsNone(duplicate_artifact("nonexistent"))

    def test_load_nonexistent(self):
        """Loading nonexistent artifact returns None."""
        self.assertIsNone(load_artifact("nonexistent"))

    def test_artifact_round_trip(self):
        """Full round-trip: save → list → load → verify fields."""
        saved = save_artifact(
            self.request_payload,
            self.response_payload,
            status="reviewed",
            coach_notes="Great program",
        )
        listing = list_artifacts()
        self.assertEqual(listing[0]["status"], "reviewed")

        loaded = load_artifact(saved["id"])
        self.assertEqual(loaded["status"], "reviewed")
        self.assertEqual(loaded["coach_notes"], "Great program")
        self.assertEqual(
            loaded["result_snapshot"]["summary"]["blueprint_selected"],
            "Test Blueprint",
        )

    def test_schema_version_present(self):
        """Saved artifact has schema_version field."""
        saved = save_artifact(self.request_payload, self.response_payload)
        self.assertIn("schema_version", saved)
        self.assertEqual(saved["schema_version"], SCHEMA_VERSION)

    def test_schema_version_in_listing(self):
        """List view includes schema_version field."""
        save_artifact(self.request_payload, self.response_payload)
        listing = list_artifacts()
        self.assertIn("schema_version", listing[0])

    def test_update_artifact_status(self):
        """Update artifact status field."""
        saved = save_artifact(self.request_payload, self.response_payload)
        updated = update_artifact(saved["id"], status="reviewed")
        self.assertIsNotNone(updated)
        self.assertEqual(updated["status"], "reviewed")
        # Verify persisted
        loaded = load_artifact(saved["id"])
        self.assertEqual(loaded["status"], "reviewed")

    def test_update_artifact_coach_notes(self):
        """Update artifact coach notes."""
        saved = save_artifact(self.request_payload, self.response_payload)
        updated = update_artifact(saved["id"], coach_notes="Good program, adjust volume")
        self.assertIsNotNone(updated)
        self.assertEqual(updated["coach_notes"], "Good program, adjust volume")

    def test_update_artifact_nonexistent(self):
        """Update nonexistent artifact returns None."""
        result = update_artifact("nonexistent", status="reviewed")
        self.assertIsNone(result)

    def test_update_artifact_updated_at_changed(self):
        """Update changes updated_at timestamp."""
        saved = save_artifact(self.request_payload, self.response_payload)
        import time
        time.sleep(0.01)
        updated = update_artifact(saved["id"], coach_notes="Updated")
        self.assertGreater(updated["updated_at"], saved["updated_at"])

    # ── Coach Override Tests ─────────────────────────────────────

    def test_coach_overrides_present_in_saved(self):
        """Saved artifact contains coach_overrides field."""
        saved = save_artifact(self.request_payload, self.response_payload)
        self.assertIn("coach_overrides", saved)
        self.assertEqual(saved["coach_overrides"], {})

    def test_coach_overrides_in_listing(self):
        """List view includes coach_overrides."""
        save_artifact(self.request_payload, self.response_payload)
        listing = list_artifacts()
        self.assertIn("coach_overrides", listing[0])

    def test_update_coach_overrides_session_locks(self):
        """Update coach_overrides with session locks persists in nested format."""
        saved = save_artifact(self.request_payload, self.response_payload)
        overrides = {"sessions": {"sess_0": {"locked": True}, "sess_1": {"locked": False}}}
        updated = update_artifact(saved["id"], coach_overrides=overrides)
        self.assertIsNotNone(updated)
        self.assertEqual(updated["coach_overrides"]["sessions"]["sess_0"]["locked"], True)
        self.assertEqual(updated["coach_overrides"]["sessions"]["sess_1"]["locked"], False)
        loaded = load_artifact(saved["id"])
        self.assertEqual(loaded["coach_overrides"]["sessions"]["sess_0"]["locked"], True)

    def test_update_coach_overrides_session_notes(self):
        """Update coach_overrides with session notes persists in nested format."""
        saved = save_artifact(self.request_payload, self.response_payload)
        overrides = {"sessions": {"sess_0": {"note": "Coach: watch hip angle"}}}
        updated = update_artifact(saved["id"], coach_overrides=overrides)
        self.assertEqual(updated["coach_overrides"]["sessions"]["sess_0"]["note"], "Coach: watch hip angle")

    def test_update_coach_overrides_exercise_swaps(self):
        """Update coach_overrides with exercise swaps persists in nested format."""
        saved = save_artifact(self.request_payload, self.response_payload)
        overrides = {"sessions": {"sess_0": {"exercises": {"ex_0": {"swap": {"original_name": "Back Squat", "new_name": "Front Squat", "new_family": "Strength"}}}}}}
        updated = update_artifact(saved["id"], coach_overrides=overrides)
        self.assertEqual(updated["coach_overrides"]["sessions"]["sess_0"]["exercises"]["ex_0"]["swap"]["new_name"], "Front Squat")
        loaded = load_artifact(saved["id"])
        self.assertEqual(loaded["coach_overrides"]["sessions"]["sess_0"]["exercises"]["ex_0"]["swap"]["original_name"], "Back Squat")

    def test_update_coach_overrides_prescription_edits(self):
        """Update coach_overrides with prescription edits persists in nested format."""
        saved = save_artifact(self.request_payload, self.response_payload)
        overrides = {"sessions": {"sess_0": {"exercises": {"ex_0": {"prescription": {"sets_reps": "4 x 8", "loading_method": "75% 1RM"}}}}}}
        updated = update_artifact(saved["id"], coach_overrides=overrides)
        self.assertEqual(updated["coach_overrides"]["sessions"]["sess_0"]["exercises"]["ex_0"]["prescription"]["sets_reps"], "4 x 8")

    def test_coach_overrides_merge_on_repeated_update(self):
        """Multiple updates merge coach_overrides, not replace."""
        saved = save_artifact(self.request_payload, self.response_payload)
        update_artifact(saved["id"], coach_overrides={"sessions": {"sess_0": {"locked": True}}})
        update_artifact(saved["id"], coach_overrides={"sessions": {"sess_0": {"note": "Note"}}})
        loaded = load_artifact(saved["id"])
        self.assertEqual(loaded["coach_overrides"]["sessions"]["sess_0"]["locked"], True)
        self.assertEqual(loaded["coach_overrides"]["sessions"]["sess_0"]["note"], "Note")

    def test_artifact_reload_preserves_overrides(self):
        """Full round-trip: save, update overrides, reload preserves them."""
        saved = save_artifact(self.request_payload, self.response_payload)
        update_artifact(saved["id"], coach_overrides={"sessions": {"sess_0": {"locked": True}}})
        loaded = load_artifact(saved["id"])
        self.assertEqual(loaded["coach_overrides"]["sessions"]["sess_0"]["locked"], True)

    def test_duplicate_resets_coach_overrides(self):
        """Duplicating an artifact resets coach_overrides."""
        saved = save_artifact(self.request_payload, self.response_payload)
        update_artifact(saved["id"], coach_overrides={"sessions": {"sess_0": {"locked": True}}})
        dup = duplicate_artifact(saved["id"])
        self.assertEqual(dup["coach_overrides"], {})

    def test_coach_overrides_in_compare_fields(self):
        """coach_overrides is present when loading for comparison."""
        saved = save_artifact(self.request_payload, self.response_payload)
        update_artifact(saved["id"], coach_overrides={"sessions": {"sess_0": {"exercises": {"ex_0": {"swap": {"new_name": "Alt Exercise", "original_name": "Old Ex", "new_family": "S"}}}}}})
        loaded = load_artifact(saved["id"])
        self.assertIn("coach_overrides", loaded)
        self.assertIn("sessions", loaded["coach_overrides"])
        self.assertIn("exercises", loaded["coach_overrides"]["sessions"]["sess_0"])

    # ── Merge Safety Tests ──────────────────────────────────────

    def test_merge_preserves_different_sessions(self):
        """Patching session A does not wipe session B."""
        saved = save_artifact(self.request_payload, self.response_payload)
        update_artifact(saved["id"], coach_overrides={"sessions": {"sess_0": {"locked": True}}})
        update_artifact(saved["id"], coach_overrides={"sessions": {"sess_1": {"note": "Other session note"}}})
        loaded = load_artifact(saved["id"])
        self.assertEqual(loaded["coach_overrides"]["sessions"]["sess_0"]["locked"], True)
        self.assertEqual(loaded["coach_overrides"]["sessions"]["sess_1"]["note"], "Other session note")

    def test_merge_preserves_exercise_siblings(self):
        """Patching one exercise does not wipe another in the same session."""
        saved = save_artifact(self.request_payload, self.response_payload)
        update_artifact(saved["id"], coach_overrides={"sessions": {"sess_0": {"exercises": {"ex_a": {"swap": {"original_name": "A", "new_name": "A1", "new_family": "S"}}}}}})
        update_artifact(saved["id"], coach_overrides={"sessions": {"sess_0": {"exercises": {"ex_b": {"prescription": {"sets_reps": "3x10"}}}}}})
        loaded = load_artifact(saved["id"])
        self.assertIn("ex_a", loaded["coach_overrides"]["sessions"]["sess_0"]["exercises"])
        self.assertIn("swap", loaded["coach_overrides"]["sessions"]["sess_0"]["exercises"]["ex_a"])
        self.assertIn("prescription", loaded["coach_overrides"]["sessions"]["sess_0"]["exercises"]["ex_b"])

    def test_merge_swap_then_prescription_same_exercise(self):
        """Patching swap then prescription for same exercise preserves both."""
        saved = save_artifact(self.request_payload, self.response_payload)
        update_artifact(saved["id"], coach_overrides={"sessions": {"sess_0": {"exercises": {"ex_0": {"swap": {"original_name": "SQ", "new_name": "FSQ", "new_family": "S"}}}}}})
        update_artifact(saved["id"], coach_overrides={"sessions": {"sess_0": {"exercises": {"ex_0": {"prescription": {"sets_reps": "4x6"}}}}}})
        loaded = load_artifact(saved["id"])
        ex0 = loaded["coach_overrides"]["sessions"]["sess_0"]["exercises"]["ex_0"]
        self.assertEqual(ex0["swap"]["new_name"], "FSQ")
        self.assertEqual(ex0["prescription"]["sets_reps"], "4x6")

    # ── Clear Semantics Tests ───────────────────────────────────

    def test_clear_session_note(self):
        """Setting session note to None removes it."""
        saved = save_artifact(self.request_payload, self.response_payload)
        update_artifact(saved["id"], coach_overrides={"sessions": {"sess_0": {"note": "Original note", "locked": True}}})
        update_artifact(saved["id"], coach_overrides={"sessions": {"sess_0": {"note": None}}})
        loaded = load_artifact(saved["id"])
        self.assertNotIn("note", loaded["coach_overrides"]["sessions"]["sess_0"])
        self.assertEqual(loaded["coach_overrides"]["sessions"]["sess_0"]["locked"], True)

    def test_clear_exercise_swap(self):
        """Setting exercise swap to None removes it; prunes empty containers up."""
        saved = save_artifact(self.request_payload, self.response_payload)
        update_artifact(saved["id"], coach_overrides={"sessions": {"sess_0": {"exercises": {"ex_0": {"swap": {"original_name": "A", "new_name": "B", "new_family": "S"}}}}}})
        update_artifact(saved["id"], coach_overrides={"sessions": {"sess_0": {"exercises": {"ex_0": {"swap": None}}}}})
        loaded = load_artifact(saved["id"])
        # Full pruning chain: ex_0 cleared → exercises empty → sess_0 empty → sessions key gone
        self.assertEqual(loaded.get("coach_overrides", {}), {})

    def test_clear_prescription_override(self):
        """Setting prescription to None removes it; prunes empty containers up."""
        saved = save_artifact(self.request_payload, self.response_payload)
        update_artifact(saved["id"], coach_overrides={"sessions": {"sess_0": {"exercises": {"ex_0": {"prescription": {"sets_reps": "3x8"}}}}}})
        update_artifact(saved["id"], coach_overrides={"sessions": {"sess_0": {"exercises": {"ex_0": {"prescription": None}}}}})
        loaded = load_artifact(saved["id"])
        self.assertEqual(loaded.get("coach_overrides", {}), {})

    def test_prune_empty_exercise_override(self):
        """Clearing last override field prunes exercise and parent session."""
        saved = save_artifact(self.request_payload, self.response_payload)
        update_artifact(saved["id"], coach_overrides={"sessions": {"sess_0": {"exercises": {"ex_0": {"swap": {"original_name": "A", "new_name": "B", "new_family": "S"}}}}}})
        update_artifact(saved["id"], coach_overrides={"sessions": {"sess_0": {"exercises": {"ex_0": {"swap": None}}}}})
        loaded = load_artifact(saved["id"])
        self.assertEqual(loaded.get("coach_overrides", {}), {})

    def test_prune_empty_session_override(self):
        """Session removed when all fields cleared."""
        saved = save_artifact(self.request_payload, self.response_payload)
        update_artifact(saved["id"], coach_overrides={"sessions": {"sess_0": {"note": "Temporary"}}})
        update_artifact(saved["id"], coach_overrides={"sessions": {"sess_0": {"note": None}}})
        loaded = load_artifact(saved["id"])
        self.assertEqual(loaded.get("coach_overrides", {}), {})

    # ── Compatibility / Migration Tests ─────────────────────────

    def test_migration_old_flat_format_on_load(self):
        """Loading an artifact with old flat override format normalizes correctly."""
        saved = save_artifact(self.request_payload, self.response_payload)
        path = os.path.join(self.test_dir, f"{saved['id']}.json")
        with open(path, "r", encoding="utf-8") as f:
            artifact = json.load(f)
        artifact["coach_overrides"] = {"session_locks": {"sess_0": True}, "session_notes": {"sess_0": "old note"}}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(artifact, f, indent=2)
        loaded = load_artifact(saved["id"])
        self.assertIn("sessions", loaded["coach_overrides"])
        self.assertEqual(loaded["coach_overrides"]["sessions"]["sess_0"]["locked"], True)
        self.assertEqual(loaded["coach_overrides"]["sessions"]["sess_0"]["note"], "old note")

    def test_migration_old_flat_format_via_update(self):
        """Sending old flat format in PATCH normalizes into nested."""
        saved = save_artifact(self.request_payload, self.response_payload)
        updated = update_artifact(saved["id"], coach_overrides={"session_locks": {"sess_x": True}})
        self.assertIn("sessions", updated["coach_overrides"])
        self.assertEqual(updated["coach_overrides"]["sessions"]["sess_x"]["locked"], True)

    def test_migration_exercise_swaps_preserved(self):
        """Old flat exercise_swaps survive migration into nested sessions._ex."""
        saved = save_artifact(self.request_payload, self.response_payload)
        path = os.path.join(self.test_dir, f"{saved['id']}.json")
        with open(path, "r", encoding="utf-8") as f:
            artifact = json.load(f)
        artifact["coach_overrides"] = {"exercise_swaps": {"ex_0": {"original_name": "SQ", "new_name": "FSQ", "new_family": "S"}}}
        with open(path, "w", encoding="utf-8") as f:
            json.dump(artifact, f, indent=2)
        loaded = load_artifact(saved["id"])
        self.assertIn("sessions", loaded["coach_overrides"])
        self.assertIn("_ex", loaded["coach_overrides"]["sessions"])
        self.assertIn("exercises", loaded["coach_overrides"]["sessions"]["_ex"])
        self.assertEqual(
            loaded["coach_overrides"]["sessions"]["_ex"]["exercises"]["ex_0"]["swap"]["new_name"],
            "FSQ",
        )


if __name__ == "__main__":
    unittest.main()
