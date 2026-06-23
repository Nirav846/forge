# Forge Program Builder V1 - Unit Tests
# Role: Principal Performance Architect
# Description: Automated unit tests to verify 4-week program structure,
# progression logic, session distributions, repository operations, and FastAPI endpoints.

import unittest
from datetime import date
from fastapi.testclient import TestClient

# Reset helpers from existing modules
from athlete_module import _mock_repo as athlete_repo, AthleteCreate
from assessment_entry_module import _mock_repo as results_repo, ResultCreate
from program_builder import (
    app,
    _mock_repo as program_repo,
    parse_baseline_reps,
    calculate_reps_and_intensity,
    ProgramGenerateRequest
)

class TestProgramBuilder(unittest.TestCase):

    def setUp(self):
        # Reset mock databases to isolate states
        athlete_repo.athletes.clear()
        athlete_repo.counter = 1
        
        results_repo.results.clear()
        results_repo.counter = 1
        
        program_repo.programs.clear()
        program_repo.counter = 1
        
        self.client = TestClient(app)
        
        # Seed default mock Athlete (ID = 1)
        self.athlete_payload = {
            "first_name": "Nirav",
            "last_name": "Patel",
            "date_of_birth": date(1998, 5, 20),
            "gender": "Male",
            "sport_id": 1,
            "role_id": 1,
            "dominant_side": "Right",
            "competition_level": "Elite",
            "training_age_years": 8,
            "training_age_months": 96
        }
        athlete_repo.create_sync(AthleteCreate(**self.athlete_payload))

    # -------------------------------------------------------------
    # 1. Helper Function Tests
    # -------------------------------------------------------------

    def test_parse_baseline_reps(self):
        self.assertEqual(parse_baseline_reps("3x5", "Primary"), 5)
        self.assertEqual(parse_baseline_reps("4x3", "Primary"), 3)
        self.assertEqual(parse_baseline_reps("3x8-10", "Accessory"), 8)
        self.assertEqual(parse_baseline_reps("", "Primary"), 5)
        self.assertEqual(parse_baseline_reps("invalid", "Core"), 10)

    def test_calculate_reps_and_intensity(self):
        # Week 1
        sets, reps, intensity, rest = calculate_reps_and_intensity(1, 5)
        self.assertEqual((sets, reps, intensity, rest), (3, 5, "75% 1RM (RPE 7)", 90))
        
        # Week 2
        sets, reps, intensity, rest = calculate_reps_and_intensity(2, 5)
        self.assertEqual((sets, reps, intensity, rest), (4, 5, "80% 1RM (RPE 8)", 90))
        
        # Week 3
        sets, reps, intensity, rest = calculate_reps_and_intensity(3, 5)
        self.assertEqual((sets, reps, intensity, rest), (4, 3, "85% 1RM (RPE 9)", 120))
        
        # Week 4
        sets, reps, intensity, rest = calculate_reps_and_intensity(4, 5)
        self.assertEqual((sets, reps, intensity, rest), (2, 5, "60% 1RM (RPE 6)", 90))

        # Exercise-Specific S&C Progression Tests (using exercise_class metadata)
        
        # A. Nordic Hamstring Curl (Accessory class — eccentric control)
        sets, reps, intensity, rest = calculate_reps_and_intensity(1, 8, exercise_class="Accessory")
        self.assertEqual((sets, reps, intensity, rest), (3, 8, "75% 1RM (RPE 7)", 90))
        sets, reps, intensity, rest = calculate_reps_and_intensity(3, 8, exercise_class="Accessory")
        self.assertEqual((sets, reps, intensity, rest), (4, 6, "85% 1RM (RPE 9)", 90))

        # B. Isometric (Plank-style)
        sets, reps, intensity, rest = calculate_reps_and_intensity(1, 30, exercise_class="Isometric")
        self.assertEqual((sets, reps, intensity, rest), (3, 30, "Bodyweight (Max Tension, RPE 7)", 90))
        sets, reps, intensity, rest = calculate_reps_and_intensity(3, 30, exercise_class="Isometric")
        self.assertEqual((sets, reps, intensity, rest), (4, 30, "Bodyweight (Max Tension, RPE 9)", 90))

        # C. Medicine Ball
        sets, reps, intensity, rest = calculate_reps_and_intensity(1, 6, exercise_class="Medicine Ball")
        self.assertEqual((sets, reps, intensity, rest), (3, 6, "Max Effort (2-4 kg)", 90))
        sets, reps, intensity, rest = calculate_reps_and_intensity(3, 6, exercise_class="Medicine Ball")
        self.assertEqual((sets, reps, intensity, rest), (4, 4, "Max Effort (3-5 kg)", 90))

        # D. Ballistic (Jump Squat — Velocity-based %1RM)
        sets, reps, intensity, rest = calculate_reps_and_intensity(1, 3, exercise_class="Ballistic")
        self.assertEqual((sets, reps, intensity, rest), (3, 3, "30% 1RM (Max Velocity, RPE 7)", 90))
        sets, reps, intensity, rest = calculate_reps_and_intensity(3, 3, exercise_class="Ballistic")
        self.assertEqual((sets, reps, intensity, rest), (4, 2, "40% 1RM (Max Velocity, RPE 9)", 120))

        with self.assertRaises(ValueError):
            calculate_reps_and_intensity(5, 5)

    # -------------------------------------------------------------
    # 2. Program Generation S&C Core Tests
    # -------------------------------------------------------------

    def test_generate_program_2_sessions(self):
        # Seed assessment history for athlete to trigger deficits mapping -> Power goal
        # CMJ=38.0 is sub-optimal (assessment_id=1)
        results_repo.results[1] = {
            "id": 1,
            "athlete_id": 1,
            "assessment_id": 1,
            "score": 38.0,
            "unit": "cm",
            "test_date": date.today(),
            "created_at": date.today()
        }

        # Generate a program with 2 sessions/week
        response = self.client.post(
            "/api/v1/programs/generate",
            json={"athlete_id": 1, "sessions_per_week": 2, "name": "Power Block 2"}
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        
        # Verify hierarchy: Program -> 4 Weeks -> 2 Sessions -> Exercises
        self.assertEqual(data["sessions_per_week"], 2)
        self.assertEqual(len(data["weeks"]), 4)
        for week in data["weeks"]:
            self.assertEqual(len(week["sessions"]), 2)
            for session in week["sessions"]:
                # The Cricket Power template has 4 slots
                self.assertEqual(len(session["exercises"]), 4)
                # Verify exercise sort order
                display_orders = [ex["display_order"] for ex in session["exercises"]]
                self.assertEqual(display_orders, sorted(display_orders))

    def test_generate_program_3_sessions_with_progressions(self):
        # Seed assessment results for athlete (Broad Jump=2.10 maps to deficit -> Power)
        results_repo.results[1] = {
            "id": 1,
            "athlete_id": 1,
            "assessment_id": 2,
            "score": 2.10,
            "unit": "m",
            "test_date": date.today(),
            "created_at": date.today()
        }

        response = self.client.post(
            "/api/v1/programs/generate",
            json={"athlete_id": 1, "sessions_per_week": 3, "name": "Power Block 3"}
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        
        self.assertEqual(data["sessions_per_week"], 3)
        
        # Verify weekly S&C progressions
        weeks = data["weeks"]
        
        # Week 1 (Base): 3 sets, standard reps, RPE 7, 90s rest
        w1_ex = weeks[0]["sessions"][0]["exercises"][0]
        self.assertEqual(w1_ex["sets"], 3)
        self.assertEqual(w1_ex["intensity"], "30% 1RM (Max Velocity, RPE 7)")
        self.assertEqual(w1_ex["rest_seconds"], 90)
        
        # Week 2 (Accumulation): 4 sets, standard reps, RPE 8, 90s rest
        w2_ex = weeks[1]["sessions"][0]["exercises"][0]
        self.assertEqual(w2_ex["sets"], 4)
        self.assertEqual(w2_ex["intensity"], "35% 1RM (Max Velocity, RPE 8)")
        self.assertEqual(w2_ex["rest_seconds"], 90)
        
        # Week 3 (Peak): 4 sets, lower reps (baseline - 2), RPE 9, 120s rest
        w3_ex = weeks[2]["sessions"][0]["exercises"][0]
        self.assertEqual(w3_ex["sets"], 4)
        # Baseline reps parsed for Slot 1 (Bilateral) in Mock Recommender is 3 reps (VBT volume target "4x3")
        # baseline = 3 -> peak reps = max(2, 3 - 2) = 2 reps
        self.assertEqual(w3_ex["reps"], 2)
        self.assertEqual(w3_ex["intensity"], "40% 1RM (Max Velocity, RPE 9)")
        self.assertEqual(w3_ex["rest_seconds"], 120)
        
        # Week 4 (Deload): 2 sets, standard reps, RPE 6, 90s rest
        w4_ex = weeks[3]["sessions"][0]["exercises"][0]
        self.assertEqual(w4_ex["sets"], 2)
        self.assertEqual(w4_ex["reps"], 3)
        self.assertEqual(w4_ex["intensity"], "30% 1RM (Deload Velocity, RPE 6)")
        self.assertEqual(w4_ex["rest_seconds"], 90)

    def test_generate_program_4_sessions(self):
        response = self.client.post(
            "/api/v1/programs/generate",
            json={"athlete_id": 1, "sessions_per_week": 4}
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["sessions_per_week"], 4)
        for week in data["weeks"]:
            self.assertEqual(len(week["sessions"]), 4)

    def test_generate_program_no_history_fallback(self):
        # Generate program with empty assessment history
        # Should automatically fall back to Power goal
        response = self.client.post(
            "/api/v1/programs/generate",
            json={"athlete_id": 1, "sessions_per_week": 3}
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["goal"], "Power")
        self.assertEqual(len(data["weeks"]), 4)

    # -------------------------------------------------------------
    # 3. API CRUD Endpoint Tests
    # -------------------------------------------------------------

    def test_api_crud_endpoints(self):
        # 1. Generate program
        gen_res = self.client.post(
            "/api/v1/programs/generate",
            json={"athlete_id": 1, "sessions_per_week": 3, "name": "Sprint & Power"}
        )
        self.assertEqual(gen_res.status_code, 201)
        program_id = gen_res.json()["id"]

        # 2. Get program details
        get_res = self.client.get(f"/api/v1/programs/{program_id}")
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.json()["name"], "Sprint & Power")

        # 3. Delete program
        del_res = self.client.delete(f"/api/v1/programs/{program_id}")
        self.assertEqual(del_res.status_code, 200)
        self.assertEqual(del_res.json()["status"], "success")

        # 4. Confirm program is deleted (should be 404)
        confirm_res = self.client.get(f"/api/v1/programs/{program_id}")
        self.assertEqual(confirm_res.status_code, 404)

    def test_api_get_not_found(self):
        response = self.client.get("/api/v1/programs/999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"])

    def test_api_delete_not_found(self):
        response = self.client.delete("/api/v1/programs/999")
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"])

    def test_api_generate_athlete_not_found(self):
        response = self.client.post(
            "/api/v1/programs/generate",
            json={"athlete_id": 999, "sessions_per_week": 3}
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"])

if __name__ == "__main__":
    unittest.main()
