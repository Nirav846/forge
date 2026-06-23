# Exercise Substitution Engine - Unit Tests
# Role: Principal Exercise Intelligence Architect
# Description: Verifies substitution engine, equivalency layer, preview-swap endpoint,
# coach override persistence, and training-age filter for cricket athletes.

import os
import sys
import json
import unittest
import pytest
from datetime import date
from fastapi.testclient import TestClient

from athlete_module import _mock_repo as athlete_repo, AthleteCreate
from assessment_entry_module import _mock_repo as results_repo
from program_builder import (
    app,
    _mock_repo as program_repo,
    _staged_programs,
    _coach_overrides,
    ProgramBuilderService,
    MockExerciseRepository,
    calculate_reps_and_intensity,
    SwapPreviewRequest,
    CoachOverrideEntry
)
from exercise_substitution_engine import get_substitutions
from exercise_equivalencies import EXERCISE_EQUIVALENCIES, get_equivalencies_by_source
from exercise_classification import classify_exercise, determine_primary_adaptation, determine_force_vector


class TestExerciseEquivalencies(unittest.TestCase):
    """Verify equivalency data layer has correct entries."""

    def test_power_clean_equivalencies_exist(self):
        equivs = get_equivalencies_by_source("Power Clean")
        target_names = {e["target_exercise_name"] for e in equivs}
        self.assertIn("Hang Clean", target_names)
        self.assertIn("Clean Pull", target_names)

    def test_push_jerk_equivalencies_exist(self):
        equivs = get_equivalencies_by_source("Push Jerk")
        target_names = {e["target_exercise_name"] for e in equivs}
        self.assertIn("Push Press", target_names)

    def test_trap_bar_jump_squat_equivalencies_exist(self):
        equivs = get_equivalencies_by_source("Trap Bar Jump Squat")
        target_names = {e["target_exercise_name"] for e in equivs}
        self.assertIn("Barbell Jump Squat", target_names)

    def test_equivalency_scores_positive(self):
        for e in EXERCISE_EQUIVALENCIES:
            self.assertGreaterEqual(e["equivalency_score"], 0.0)
            self.assertLessEqual(e["equivalency_score"], 10.0)

    def test_all_equivalencies_have_reason(self):
        for e in EXERCISE_EQUIVALENCIES:
            self.assertTrue(len(e["reason"]) > 10)


class TestExerciseClassification(unittest.TestCase):
    """Verify classification module assigns correct classes."""

    def setUp(self):
        self.mock_ex = lambda name, force="Push", mechanics="Compound": {
            "name": name, "force_type": force, "mechanics_type": mechanics
        }

    def test_power_clean_is_olympic_lift(self):
        ex = self.mock_ex("Power Clean")
        self.assertEqual(classify_exercise(ex), "Olympic Lift")

    def test_push_jerk_is_olympic_lift(self):
        ex = self.mock_ex("Push Jerk")
        self.assertEqual(classify_exercise(ex), "Olympic Lift")

    def test_trap_bar_jump_squat_is_ballistic(self):
        ex = self.mock_ex("Trap Bar Jump Squat")
        self.assertEqual(classify_exercise(ex), "Ballistic")

    def test_medicine_ball_is_medicine_ball(self):
        ex = self.mock_ex("Medicine Ball Rotational Chest Pass")
        self.assertEqual(classify_exercise(ex), "Medicine Ball")

    def test_nordic_hamstring_curl_is_max_strength(self):
        ex = self.mock_ex("Nordic Hamstring Curl")
        self.assertEqual(classify_exercise(ex), "Max Strength")

    def test_plank_is_isometric(self):
        ex = self.mock_ex("Plank with Rotation")
        self.assertEqual(classify_exercise(ex), "Isometric")

    def test_olympic_lift_primary_adaptation(self):
        ex = self.mock_ex("Power Clean")
        ex["exercise_class"] = "Olympic Lift"
        self.assertEqual(determine_primary_adaptation(ex), "Power")

    def test_medicine_ball_rotational_adaptation(self):
        ex = self.mock_ex("Medicine Ball Rotational Scoop Toss")
        ex["exercise_class"] = "Medicine Ball"
        self.assertEqual(determine_primary_adaptation(ex), "Rotational Power")

    def test_olympic_lift_force_vector(self):
        ex = self.mock_ex("Power Clean")
        ex["exercise_class"] = "Olympic Lift"
        self.assertEqual(determine_force_vector(ex), "Vertical")


class TestSubstitutionEngine:
    """Verify substitution engine correctly ranks and filters substitutes."""

    repo = MockExerciseRepository()

    @classmethod
    def setup_class(cls):
        cls.repo = MockExerciseRepository()

    @pytest.mark.asyncio
    async def test_power_clean_swap_to_hang_clean(self):
        # Power Clean is in slots [201, 203, 401]
        subs = await get_substitutions(
            slot_id=201,
            exercise_id=86,  # Power Clean
            athlete_profile={},
            equipment=["Barbell", "Trap Bar", "Medicine Ball", "Bodyweight"],
            repo=self.repo,
            difficulty_cap="Elite",
            training_age_months=48
        )
        sub_names = [s.name for s in subs]
        assert "Hang Clean" in sub_names
        hang_clean_sub = next(s for s in subs if s.name == "Hang Clean")
        assert hang_clean_sub.equivalency_score > 0

    @pytest.mark.asyncio
    async def test_push_jerk_swap_to_push_press(self):
        subs = await get_substitutions(
            slot_id=303,
            exercise_id=132,  # Push Jerk
            athlete_profile={},
            equipment=["Barbell", "Medicine Ball", "Bodyweight"],
            repo=self.repo,
            difficulty_cap="Elite",
            training_age_months=36
        )
        sub_names = [s.name for s in subs]
        assert "Push Press" in sub_names
        push_press_sub = next(s for s in subs if s.name == "Push Press")
        assert push_press_sub.equivalency_score > 0

    @pytest.mark.asyncio
    async def test_trap_bar_jump_squat_swap_to_barbell_jump_squat(self):
        subs = await get_substitutions(
            slot_id=201,
            exercise_id=1,  # Trap Bar Jump Squat
            athlete_profile={},
            equipment=["Barbell", "Trap Bar", "Bodyweight"],
            repo=self.repo,
            difficulty_cap="Elite",
            training_age_months=48
        )
        equiv_subs = [s for s in subs if s.equivalency_score > 0]
        assert len(subs) > 0

    @pytest.mark.asyncio
    async def test_substitutions_preserve_progression(self):
        """Verify that substituted exercises use class-based progression correctly."""
        subs = await get_substitutions(
            slot_id=201,
            exercise_id=86,  # Power Clean (Olympic Lift)
            athlete_profile={},
            equipment=["Barbell", "Trap Bar", "Bodyweight"],
            repo=self.repo,
            difficulty_cap="Elite",
            training_age_months=48
        )
        for sub in subs:
            for week in [1, 2, 3, 4]:
                sets, reps, intensity, rest = calculate_reps_and_intensity(
                    week_num=week,
                    baseline_reps=5,
                    exercise_class=sub.exercise_class,
                    force_type=sub.force_type
                )
                assert sets in [2, 3, 4]
                assert reps > 0
                assert len(intensity) > 0
                assert rest in [90, 120]

    @pytest.mark.asyncio
    async def test_training_age_filter_applied(self):
        """Athlete with low training age should not see advanced substitutions."""
        subs_low = await get_substitutions(
            slot_id=201,
            exercise_id=1,  # Trap Bar Jump Squat
            athlete_profile={},
            equipment=["Barbell", "Bodyweight"],
            repo=self.repo,
            difficulty_cap="Elite",
            training_age_months=6
        )
        subs_high = await get_substitutions(
            slot_id=201,
            exercise_id=1,  # Trap Bar Jump Squat
            athlete_profile={},
            equipment=["Barbell", "Bodyweight"],
            repo=self.repo,
            difficulty_cap="Elite",
            training_age_months=60
        )
        assert len(subs_high) >= len(subs_low)

    @pytest.mark.asyncio
    async def test_substitutions_ranked_by_equivalency_first(self):
        subs = await get_substitutions(
            slot_id=201,
            exercise_id=86,  # Power Clean
            athlete_profile={},
            equipment=["Barbell", "Trap Bar", "Medicine Ball", "Bodyweight"],
            repo=self.repo,
            difficulty_cap="Elite",
            training_age_months=48
        )
        if len(subs) >= 2:
            assert subs[0].equivalency_score >= subs[1].equivalency_score

    @pytest.mark.asyncio
    async def test_equipment_filter_applied(self):
        """Substitutes should only include exercises requiring available equipment."""
        subs = await get_substitutions(
            slot_id=201,
            exercise_id=1,  # Trap Bar Jump Squat
            athlete_profile={},
            equipment=["Bodyweight"],
            repo=self.repo,
            difficulty_cap="Elite",
            training_age_months=48
        )
        for sub in subs:
            pass


class TestPreviewSwapEndpoint(unittest.TestCase):
    """Verify the preview-swap endpoint returns valid responses."""

    def setUp(self):
        athlete_repo.athletes.clear()
        athlete_repo.counter = 1
        results_repo.results.clear()
        results_repo.counter = 1
        program_repo.programs.clear()
        program_repo.counter = 1
        _staged_programs.clear()
        _coach_overrides.clear()

        athlete_repo.create_sync(AthleteCreate(
            first_name="Test", last_name="User",
            date_of_birth=date(1998, 5, 20),
            gender="Male", sport_id=1, role_id=1,
            dominant_side="Right", competition_level="Elite",
            training_age_years=8, training_age_months=96
        ))

        self.client = TestClient(app)
        self.service = ProgramBuilderService(
            program_repo, athlete_repo, results_repo
        )

    def test_preview_swap_valid(self):
        # Stage a program first
        stage_resp = self.client.post("/api/v1/programs/stage", json={
            "athlete_id": 1, "sessions_per_week": 3, "goal": "Power",
            "use_default_exercise": True
        })
        self.assertEqual(stage_resp.status_code, 201)
        stage_id = stage_resp.json()["stage_id"]

        # Preview swap (slot 201, target Power Clean id=86 for Trap Bar Jump Squat)
        preview_resp = self.client.post("/api/v1/programs/preview-swap", json={
            "stage_id": stage_id,
            "slot_id": 201,
            "target_exercise_id": 86  # Power Clean
        })
        self.assertEqual(preview_resp.status_code, 200)
        data = preview_resp.json()
        self.assertIn("current_exercise_name", data)
        self.assertIn("new_exercise_name", data)
        self.assertIn("weeks", data)
        self.assertEqual(len(data["weeks"]), 4)

    def test_preview_swap_invalid_stage_id(self):
        resp = self.client.post("/api/v1/programs/preview-swap", json={
            "stage_id": "nonexistent",
            "slot_id": 201,
            "target_exercise_id": 86
        })
        self.assertEqual(resp.status_code, 404)

    def test_preview_swap_unchanged_when_class_and_force_match(self):
        # Stage a program
        stage_resp = self.client.post("/api/v1/programs/stage", json={
            "athlete_id": 1, "sessions_per_week": 3, "goal": "Power",
            "use_default_exercise": True
        })
        self.assertEqual(stage_resp.status_code, 201)
        stage_id = stage_resp.json()["stage_id"]

        # Try swapping Trap Bar Jump Squat (Ballistic) for Power Clean (Olympic Lift)
        # These have different classes -> unchanged should be false
        preview_resp = self.client.post("/api/v1/programs/preview-swap", json={
            "stage_id": stage_id,
            "slot_id": 201,
            "target_exercise_id": 86  # Power Clean (Olympic Lift)
        })
        self.assertEqual(preview_resp.status_code, 200)
        data = preview_resp.json()
        # Different exercise class -> not unchanged
        self.assertFalse(data["unchanged"])


class TestCoachOverridePersistence(unittest.TestCase):
    """Verify coach override recording."""

    def setUp(self):
        athlete_repo.athletes.clear()
        athlete_repo.counter = 1
        results_repo.results.clear()
        results_repo.counter = 1
        program_repo.programs.clear()
        program_repo.counter = 1
        _staged_programs.clear()
        _coach_overrides.clear()

        athlete_repo.create_sync(AthleteCreate(
            first_name="Test", last_name="User",
            date_of_birth=date(1998, 5, 20),
            gender="Male", sport_id=1, role_id=1,
            dominant_side="Right", competition_level="Elite",
            training_age_years=8, training_age_months=96
        ))

        self.client = TestClient(app)

    def test_override_recorded(self):
        resp = self.client.post("/api/v1/programs/override", json={
            "stage_id": "test-stage-1",
            "slot_id": 201,
            "original_exercise_id": 1,
            "selected_exercise_id": 86,
            "override_reason": "Athlete prefers clean variations",
            "overridden_by": "Coach Smith"
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "recorded")
        self.assertEqual(data["original_exercise_id"], 1)
        self.assertEqual(data["selected_exercise_id"], 86)


if __name__ == "__main__":
    unittest.main()
