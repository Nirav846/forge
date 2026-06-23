# Forge Athlete Module - Unit Tests
# Role: Principal Domain Architect
# Description: Unit tests to verify validation rules, Mock CRUD repository layers, 
# and FastAPI routing endpoints using TestClient.

import unittest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from pydantic import ValidationError

from athlete_module import app, AthleteCreate, AthleteUpdate, MockAthleteRepository, _mock_repo

class TestAthleteModule(unittest.TestCase):

    def setUp(self):
        # Reset the mock repository before each test to guarantee isolated states
        _mock_repo.athletes.clear()
        _mock_repo.counter = 1
        self.repo = _mock_repo
        self.client = TestClient(app)

    def get_valid_payload(self) -> dict:
        return {
            "first_name": "Nirav",
            "last_name": "Patel",
            "date_of_birth": "1998-05-20",
            "gender": "Male",
            "sport_id": 1,
            "role_id": 1,
            "dominant_side": "Right",
            "competition_level": "Elite",
            "training_age_years": 8,
            "training_age_months": 96
        }

    # -------------------------------------------------------------
    # 1. Pydantic Validation Tests
    # -------------------------------------------------------------

    def test_pydantic_valid_payload(self):
        payload = self.get_valid_payload()
        athlete = AthleteCreate(**payload)
        self.assertEqual(athlete.first_name, "Nirav")
        self.assertEqual(athlete.training_age_years, 8)
        self.assertEqual(athlete.training_age_months, 96)

    def test_pydantic_invalid_dob_future(self):
        payload = self.get_valid_payload()
        # Set DOB to tomorrow
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        payload["date_of_birth"] = tomorrow

        with self.assertRaises(ValidationError) as ctx:
            AthleteCreate(**payload)
        
        self.assertIn("Date of birth must be in the past", str(ctx.exception))

    def test_pydantic_invalid_training_age_negative(self):
        payload = self.get_valid_payload()
        payload["training_age_years"] = -1

        with self.assertRaises(ValidationError) as ctx:
            AthleteCreate(**payload)
        
        self.assertIn("Training age cannot be negative", str(ctx.exception))

    def test_pydantic_invalid_literal_gender(self):
        payload = self.get_valid_payload()
        payload["gender"] = "InvalidGender"

        with self.assertRaises(ValidationError) as ctx:
            AthleteCreate(**payload)
        
        self.assertIn("Input should be 'Male', 'Female', 'Other' or 'Prefer Not to Say'", str(ctx.exception))

    # -------------------------------------------------------------
    # 2. Repository Layer CRUD Tests
    # -------------------------------------------------------------

    def test_repo_create_and_get(self):
        payload = self.get_valid_payload()
        create_model = AthleteCreate(**payload)
        
        # Test creation
        record = self.repo.create_sync(create_model)
        self.assertEqual(record["id"], 1)
        self.assertEqual(record["first_name"], "Nirav")
        
        # Test get_by_id
        fetched = self.client.get("/api/v1/athletes/1")
        self.assertEqual(fetched.status_code, 200)
        data = fetched.json()
        self.assertEqual(data["first_name"], "Nirav")

    # -------------------------------------------------------------
    # 3. FastAPI Endpoint CRUD Tests
    # -------------------------------------------------------------

    def test_api_create_success(self):
        payload = self.get_valid_payload()
        response = self.client.post("/api/v1/athletes", json=payload)
        self.assertEqual(response.status_code, 201)
        
        data = response.json()
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["first_name"], "Nirav")
        self.assertIn("created_at", data)
        self.assertIn("updated_at", data)

    def test_api_create_validation_failure(self):
        payload = self.get_valid_payload()
        payload["training_age_years"] = -5
        
        response = self.client.post("/api/v1/athletes", json=payload)
        self.assertEqual(response.status_code, 422) # Unprocessable Entity
        self.assertIn("detail", response.json())

    def test_api_get_not_found(self):
        response = self.client.get("/api/v1/athletes/999")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Athlete with ID 999 not found.")

    def test_api_update_success(self):
        # 1. Create first
        payload = self.get_valid_payload()
        self.client.post("/api/v1/athletes", json=payload)
        
        # 2. Update partially
        update_payload = {"first_name": "UpdatedName", "training_age_years": 10}
        response = self.client.put("/api/v1/athletes/1", json=update_payload)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["first_name"], "UpdatedName")
        self.assertEqual(data["training_age_years"], 10)
        self.assertEqual(data["last_name"], "Patel") # Should remain unchanged

    def test_api_delete_success(self):
        # 1. Create first
        payload = self.get_valid_payload()
        self.client.post("/api/v1/athletes", json=payload)
        
        # 2. Delete it
        del_response = self.client.delete("/api/v1/athletes/1")
        self.assertEqual(del_response.status_code, 200)
        self.assertEqual(del_response.json()["status"], "success")
        
        # 3. Retrieve and confirm gone (should be 404)
        get_response = self.client.get("/api/v1/athletes/1")
        self.assertEqual(get_response.status_code, 404)

    def test_api_list_with_filtration(self):
        # Create athlete 1 (Sport 1, Role 1)
        p1 = self.get_valid_payload()
        self.client.post("/api/v1/athletes", json=p1)
        
        # Create athlete 2 (Sport 2, Role 3)
        p2 = self.get_valid_payload()
        p2["sport_id"] = 2
        p2["role_id"] = 3
        p2["first_name"] = "OtherName"
        self.client.post("/api/v1/athletes", json=p2)
        
        # List all (should be 2)
        res_all = self.client.get("/api/v1/athletes")
        self.assertEqual(len(res_all.json()), 2)
        
        # List with sport filtration
        res_filter = self.client.get("/api/v1/athletes?sport_id=2")
        data = res_filter.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["first_name"], "OtherName")

if __name__ == "__main__":
    unittest.main()
