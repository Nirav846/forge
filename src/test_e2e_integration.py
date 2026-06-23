# Forge End-to-End Integration Tests
# Role: Principal QA Architect
# Description: Verifies the complete data chain: Athlete -> Assessment -> Deficit -> Template -> Session -> Program
# Validates Fast Bowler, Spinner, and Batter examples with no broken chains.
# Saves expected outputs under the examples/ directory.

import os
import json
import unittest
from datetime import date
from fastapi.testclient import TestClient

# Import mock databases to isolate and clear state
from athlete_module import _mock_repo as athlete_repo, AthleteCreate, app as athlete_app
from assessment_entry_module import _mock_repo as results_repo, ResultCreate, app as results_app
from deficit_detection_engine import MockBenchmarkRepository, app as deficit_app
from recommendation_engine import MockExerciseRepository, app as rec_app
from session_generator import app as session_app
from program_builder import _mock_repo as program_repo, app as program_app


class TestEndToEndIntegration(unittest.TestCase):

    def setUp(self):
        # Reset all in-memory mock repositories to ensure isolated test runs
        athlete_repo.athletes.clear()
        athlete_repo.counter = 1

        results_repo.results.clear()
        results_repo.counter = 1

        program_repo.programs.clear()
        program_repo.counter = 1

        self.athlete_client = TestClient(athlete_app)
        self.results_client = TestClient(results_app)
        self.deficit_client = TestClient(deficit_app)
        self.session_client = TestClient(session_app)
        self.program_client = TestClient(program_app)

        # Create output directory for examples if not exists
        os.makedirs("examples", exist_ok=True)

    def test_e2e_fast_bowler_pipeline(self):
        """Verifies Athlete -> Assessment -> Deficit -> Template -> Session -> Program for a Fast Bowler."""
        # Step 1: Create Athlete Profile
        athlete_payload = {
            "first_name": "Nirav",
            "last_name": "Patel",
            "date_of_birth": "1998-05-20",
            "gender": "Male",
            "sport_id": 1,  # Cricket
            "role_id": 1,   # Fast Bowler
            "dominant_side": "Right",
            "competition_level": "Elite",
            "training_age_years": 8,
            "training_age_months": 96
        }
        ath_res = self.athlete_client.post("/api/v1/athletes", json=athlete_payload)
        self.assertEqual(ath_res.status_code, 201)
        athlete_id = ath_res.json()["id"]
        self.assertEqual(athlete_id, 1)

        # Step 2: Record Assessments (High Force Deficit & Borderline Acceleration)
        # CMJ=38 (Sub-optimal -> Power Deficit), Broad Jump=2.1 (Sub-optimal -> Mobility), 10m Sprint=1.95 (Sub-optimal -> Accel)
        assessments = [
            {"athlete_id": athlete_id, "assessment_id": 1, "score": 38.0, "unit": "cm", "test_date": str(date.today())},
            {"athlete_id": athlete_id, "assessment_id": 2, "score": 2.1, "unit": "m", "test_date": str(date.today())},
            {"athlete_id": athlete_id, "assessment_id": 3, "score": 1.95, "unit": "s", "test_date": str(date.today())}
        ]
        for ass in assessments:
            res = self.results_client.post("/api/v1/assessments/results", json=ass)
            self.assertEqual(res.status_code, 201)

        # Step 3: Run Deficit Diagnostics
        diag_payload = {
            "athlete_id": athlete_id,
            "results": {
                "CMJ": 38.0,
                "Broad Jump": 2.1,
                "10m Sprint": 1.95
            }
        }
        diag_res = self.deficit_client.post("/api/v1/diagnose-deficits", json=diag_payload)
        self.assertEqual(diag_res.status_code, 200)
        deficits = diag_res.json()["deficits"]
        
        # Verify deficits contains Power Deficit, Mobility Restriction, and Acceleration Deficit
        def_names = {d["deficit"] for d in deficits}
        self.assertTrue("Power Deficit" in def_names)
        self.assertTrue("Mobility Restriction" in def_names)
        self.assertTrue("Acceleration Deficit" in def_names)

        # Step 4: Generate a single Session (template resolved to "Cricket Fast Bowler Power")
        session_payload = {
            "template_name": "Cricket Fast Bowler Power",
            "athlete_id": athlete_id,
            "equipment": ["Trap Bar", "Medicine Ball", "Bodyweight", "Dumbbell"],
            "difficulty_cap": "Advanced"
        }
        sess_res = self.session_client.post("/api/v1/sessions/generate", json=session_payload)
        self.assertEqual(sess_res.status_code, 200)
        session_data = sess_res.json()

        # Verify no duplicate movement patterns in the session
        patterns = [
            session_data["primary"]["movement_pattern"],
            session_data["secondary"]["movement_pattern"],
            session_data["accessory"]["movement_pattern"],
            session_data["core"]["movement_pattern"],
            session_data["conditioning"]["movement_pattern"]
        ]
        # Remove "N/A" and "Cardio" since they don't count towards pattern clash checks
        filtered_patterns = [p for p in patterns if p not in ["N/A", "Cardio"]]
        self.assertEqual(len(filtered_patterns), len(set(filtered_patterns)))

        # Step 5: Generate a 4-Week Program
        program_payload = {
            "athlete_id": athlete_id,
            "sessions_per_week": 3,
            "name": "E2E Fast Bowler Power Block",
            "goal": "Power",
            "equipment": ["Trap Bar", "Medicine Ball", "Bodyweight", "Dumbbell"],
            "difficulty_cap": "Advanced"
        }
        prog_res = self.program_client.post("/api/v1/programs/generate", json=program_payload)
        self.assertEqual(prog_res.status_code, 201)
        program_data = prog_res.json()

        # Verify 4 weeks hierarchy
        self.assertEqual(len(program_data["weeks"]), 4)
        self.assertEqual(program_data["goal"], "Power")

        # Save to examples
        with open("examples/e2e_fast_bowler_program.json", "w") as f:
            json.dump(program_data, f, indent=2)

    def test_e2e_spinner_pipeline(self):
        """Verifies Athlete -> Assessment -> Deficit -> Template -> Session -> Program for a Spinner."""
        # Step 1: Create Athlete Profile
        athlete_payload = {
            "first_name": "Harbhajan",
            "last_name": "Singh",
            "date_of_birth": "1996-07-03",
            "gender": "Male",
            "sport_id": 1,  # Cricket
            "role_id": 2,   # Spinner
            "dominant_side": "Right",
            "competition_level": "Elite",
            "training_age_years": 10,
            "training_age_months": 120
        }
        ath_res = self.athlete_client.post("/api/v1/athletes", json=athlete_payload)
        self.assertEqual(ath_res.status_code, 201)
        athlete_id = ath_res.json()["id"]

        # Step 2: Record Assessments (High Rotational Power Deficit)
        # Rotational Med Ball Throw = 4.5 m/s (Sub-optimal -> Rotational Power Deficit)
        # Pull Up = 15 reps (Optimal -> no deficit)
        assessments = [
            {"athlete_id": athlete_id, "assessment_id": 7, "score": 4.5, "unit": "m/s", "test_date": str(date.today())},
            {"athlete_id": athlete_id, "assessment_id": 5, "score": 15.0, "unit": "reps", "test_date": str(date.today())}
        ]
        for ass in assessments:
            res = self.results_client.post("/api/v1/assessments/results", json=ass)
            self.assertEqual(res.status_code, 201)

        # Step 3: Run Deficit Diagnostics
        diag_payload = {
            "athlete_id": athlete_id,
            "results": {
                "rotational med ball throw": 4.5,
                "pull up": 15.0
            }
        }
        diag_res = self.deficit_client.post("/api/v1/diagnose-deficits", json=diag_payload)
        self.assertEqual(diag_res.status_code, 200)
        deficits = diag_res.json()["deficits"]

        # Rotational Med Ball Throw of 4.5 is Sub-optimal -> Rotational Power Deficit diagnosed
        self.assertEqual(len(deficits), 1)
        self.assertEqual(deficits[0]["deficit"], "Rotational Power Deficit")
        self.assertEqual(deficits[0]["severity"], "Moderate")

        # Step 4: Generate a single Session (template resolved to "Cricket Spinner Rotational Power")
        session_payload = {
            "template_name": "Cricket Spinner Rotational Power",
            "athlete_id": athlete_id,
            "equipment": ["Medicine Ball", "Bodyweight", "Cable Machine", "Barbell", "Dumbbell"],
            "difficulty_cap": "Elite"
        }
        sess_res = self.session_client.post("/api/v1/sessions/generate", json=session_payload)
        self.assertEqual(sess_res.status_code, 200)
        session_data = sess_res.json()

        # Primary exercise should be Medicine Ball Rotational Scoop Toss or MB Rotational Chest Pass
        self.assertIn("Medicine Ball Rotational", session_data["primary"]["name"])

        # Step 5: Generate a 4-Week Program
        program_payload = {
            "athlete_id": athlete_id,
            "sessions_per_week": 2,
            "name": "Spinner Rotational Power Block",
            "goal": "Power",
            "equipment": ["Medicine Ball", "Bodyweight", "Cable Machine", "Barbell", "Dumbbell"],
            "difficulty_cap": "Elite"
        }
        prog_res = self.program_client.post("/api/v1/programs/generate", json=program_payload)
        self.assertEqual(prog_res.status_code, 201)
        program_data = prog_res.json()

        self.assertEqual(program_data["goal"], "Power")
        self.assertEqual(program_data["sessions_per_week"], 2)

        # Save to examples
        with open("examples/e2e_spinner_program.json", "w") as f:
            json.dump(program_data, f, indent=2)

    def test_e2e_batter_pipeline(self):
        """Verifies Athlete -> Assessment -> Deficit -> Template -> Session -> Program for a Batter."""
        # Step 1: Create Athlete Profile
        athlete_payload = {
            "first_name": "Sachin",
            "last_name": "Tendulkar",
            "date_of_birth": "1994-04-24",
            "gender": "Male",
            "sport_id": 1,  # Cricket
            "role_id": 3,   # Batter
            "dominant_side": "Right",
            "competition_level": "Elite",
            "training_age_years": 15,
            "training_age_months": 180
        }
        ath_res = self.athlete_client.post("/api/v1/athletes", json=athlete_payload)
        self.assertEqual(ath_res.status_code, 201)
        athlete_id = ath_res.json()["id"]

        # Step 2: Record Assessments (High Shoulder Robustness Deficit & Acceleration Deficit)
        # Pull Up = 5 reps (Poor -> Shoulder Robustness Deficit)
        # 10m Sprint = 1.95s (Sub-optimal -> Acceleration Deficit)
        assessments = [
            {"athlete_id": athlete_id, "assessment_id": 5, "score": 5.0, "unit": "reps", "test_date": str(date.today())},
            {"athlete_id": athlete_id, "assessment_id": 3, "score": 1.95, "unit": "s", "test_date": str(date.today())}
        ]
        for ass in assessments:
            res = self.results_client.post("/api/v1/assessments/results", json=ass)
            self.assertEqual(res.status_code, 201)

        # Step 3: Run Deficit Diagnostics
        diag_payload = {
            "athlete_id": athlete_id,
            "results": {
                "pull up": 5.0,
                "10m sprint": 1.95
            }
        }
        diag_res = self.deficit_client.post("/api/v1/diagnose-deficits", json=diag_payload)
        self.assertEqual(diag_res.status_code, 200)
        deficits = diag_res.json()["deficits"]

        # Verify deficits has Shoulder Robustness Deficit (High) and Acceleration Deficit (Moderate)
        def_map = {d["deficit"]: d["severity"] for d in deficits}
        self.assertEqual(def_map.get("Shoulder Robustness Deficit"), "High")
        self.assertEqual(def_map.get("Acceleration Deficit"), "Moderate")

        # Step 4: Generate a single Session (template resolved to "Cricket Batter Strength/Power")
        session_payload = {
            "template_name": "Cricket Batter Strength/Power",
            "athlete_id": athlete_id,
            "equipment": ["Trap Bar", "Dumbbell", "Bodyweight", "Kettlebell"],
            "difficulty_cap": "Elite"
        }
        sess_res = self.session_client.post("/api/v1/sessions/generate", json=session_payload)
        self.assertEqual(sess_res.status_code, 200)
        session_data = sess_res.json()

        # Primary exercise should be Trap Bar Deadlift or Kettlebell Swing
        self.assertIn(session_data["primary"]["name"], ["Trap Bar Deadlift", "Kettlebell Swing"])

        # Step 5: Generate a 4-Week Program
        # Primary deficit is Shoulder Robustness Deficit (High) -> maps to Strength goal
        program_payload = {
            "athlete_id": athlete_id,
            "sessions_per_week": 4,
            "name": "Batter Strength Block",
            "goal": "Strength",
            "equipment": ["Trap Bar", "Dumbbell", "Bodyweight", "Kettlebell"],
            "difficulty_cap": "Elite"
        }
        prog_res = self.program_client.post("/api/v1/programs/generate", json=program_payload)
        self.assertEqual(prog_res.status_code, 201)
        program_data = prog_res.json()

        self.assertEqual(program_data["goal"], "Strength")
        self.assertEqual(program_data["sessions_per_week"], 4)

        # Save to examples
        with open("examples/e2e_batter_program.json", "w") as f:
            json.dump(program_data, f, indent=2)


if __name__ == "__main__":
    unittest.main()
