# Forge Assessment Entry Module - Unit Tests
# Role: Principal Sports Scientist
# Description: Automated unit tests checking S&C assessment validations, 
# metric units conformance, and historical progress sorting.

import unittest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from pydantic import ValidationError

from athlete_module import _mock_repo as athlete_repo
from assessment_entry_module import app, ResultCreate, _mock_repo as results_repo

class TestAssessmentEntryModule(unittest.TestCase):

    def setUp(self):
        # Reset mock repositories
        athlete_repo.athletes.clear()
        results_repo.results.clear()
        results_repo.counter = 1
        self.client = TestClient(app)

        # Pre-seed Athlete 101 in Athlete Mock DB to pass validation check
        athlete_repo.athletes[101] = {
            "id": 101,
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

        # Seed some historical CMJ scores for Athlete 101 (Assessment ID 1, unit 'cm')
        self.client.post("/api/v1/assessments/results", json={
            "athlete_id": 101, "assessment_id": 1, "score": 35.80, "unit": "cm", "test_date": "2026-04-01"
        })
        self.client.post("/api/v1/assessments/results", json={
            "athlete_id": 101, "assessment_id": 1, "score": 38.50, "unit": "cm", "test_date": "2026-06-01"
        })
        self.client.post("/api/v1/assessments/results", json={
            "athlete_id": 101, "assessment_id": 1, "score": 37.00, "unit": "cm", "test_date": "2026-05-01"
        })

    def get_valid_payload(self) -> dict:
        return {
            "athlete_id": 101,
            "assessment_id": 1, # CMJ
            "score": 38.00,
            "unit": "cm",
            "test_date": "2026-06-15"
        }

    # -------------------------------------------------------------
    # 1. Pydantic Validation Tests
    # -------------------------------------------------------------

    def test_pydantic_valid_result(self):
        payload = self.get_valid_payload()
        result = ResultCreate(**payload)
        self.assertEqual(result.score, 38.00)
        self.assertEqual(result.unit, "cm")

    def test_pydantic_invalid_future_date(self):
        payload = self.get_valid_payload()
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        payload["test_date"] = tomorrow

        with self.assertRaises(ValidationError) as ctx:
            ResultCreate(**payload)
        self.assertIn("Test date cannot be in the future", str(ctx.exception))

    def test_pydantic_invalid_score_negative(self):
        payload = self.get_valid_payload()
        payload["score"] = -2.0

        with self.assertRaises(ValidationError) as ctx:
            ResultCreate(**payload)
        self.assertIn("Input should be greater than 0", str(ctx.exception))

    # -------------------------------------------------------------
    # 2. S&C Metric Conformance and Unit Validation Tests
    # -------------------------------------------------------------

    def test_api_unit_conformance_success(self):
        # CMJ (ID 1) uses 'cm'
        payload = self.get_valid_payload()
        response = self.client.post("/api/v1/assessments/results", json=payload)
        self.assertEqual(response.status_code, 201)

    def test_api_unit_conformance_mismatch(self):
        # CMJ (ID 1) uses 'cm', try submitting 'm'
        payload = self.get_valid_payload()
        payload["unit"] = "m"
        response = self.client.post("/api/v1/assessments/results", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Unit mismatch for assessment ID 1. Expected 'cm'", response.json()["detail"])

    def test_api_invalid_assessment_id(self):
        payload = self.get_valid_payload()
        payload["assessment_id"] = 99
        response = self.client.post("/api/v1/assessments/results", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Assessment ID 99 is not supported", response.json()["detail"])

    def test_api_invalid_athlete_id(self):
        payload = self.get_valid_payload()
        payload["athlete_id"] = 999
        response = self.client.post("/api/v1/assessments/results", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Athlete with ID 999 does not exist", response.json()["detail"])

    # -------------------------------------------------------------
    # 3. Endpoint History Tracing Tests (Sorting and Progression)
    # -------------------------------------------------------------

    def test_api_history_sorting_order(self):
        # Fetch history for Athlete 101
        response = self.client.get("/api/v1/athletes/101/assessments/history")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(len(data), 3)
        
        # Verify chronological sorting: newest first (2026-06-01 -> 2026-05-01 -> 2026-04-01)
        self.assertEqual(data[0]["test_date"], "2026-06-01")
        self.assertEqual(data[0]["score"], 38.50)
        
        self.assertEqual(data[1]["test_date"], "2026-05-01")
        self.assertEqual(data[1]["score"], 37.00)
        
        self.assertEqual(data[2]["test_date"], "2026-04-01")
        self.assertEqual(data[2]["score"], 35.80)

    def test_api_get_result_by_id(self):
        response = self.client.get("/api/v1/assessments/results/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["score"], 35.80)

    def test_api_delete_result(self):
        # Delete ID 1
        response = self.client.delete("/api/v1/assessments/results/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

        # Confirm 404 on subsequent get
        get_res = self.client.get("/api/v1/assessments/results/1")
        self.assertEqual(get_res.status_code, 404)

        # Confirm history now lists only 2 items
        hist_res = self.client.get("/api/v1/athletes/101/assessments/history")
        self.assertEqual(len(hist_res.json()), 2)

if __name__ == "__main__":
    unittest.main()
