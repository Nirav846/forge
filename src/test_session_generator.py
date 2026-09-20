# Forge Session Generator Engine - Unit Tests
# Role: Principal Systems Engineer
# Description: Unit tests verifying complete session layout compilations,
# zero movement pattern duplication, equipment/difficulty cap filtering, and FastAPI endpoint contracts.

import unittest
from datetime import date
from fastapi.testclient import TestClient

# Reset mock database helpers
from athlete_module import _mock_repo as athlete_repo, AthleteCreate
from session_generator import app, SessionGenerateRequest

class TestSessionGenerator(unittest.TestCase):

    def setUp(self):
        # Reset mock repository state
        athlete_repo.athletes.clear()
        athlete_repo.counter = 1
        
        self.client = TestClient(app)
        
        # Seed mock Athlete (ID = 1)
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

    def test_generate_session_structure_success(self):
        # Generate session using Cricket template
        response = self.client.post(
            "/api/v1/sessions/generate",
            json={
                "template_name": "Cricket Fast Bowler Power",
                "athlete_id": 1,
                "equipment": ["Trap Bar", "Medicine Ball", "Cable Machine", "Bodyweight"]
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Verify athlete name and metadata
        self.assertEqual(data["athlete_id"], 1)
        self.assertEqual(data["athlete_name"], "Nirav Patel")
        self.assertEqual(data["template_name"], "Cricket Fast Bowler Power")
        
        # Verify complete structure is generated
        self.assertIn("warmup", data)
        self.assertEqual(len(data["warmup"]), 1)
        
        self.assertIn("primary", data)
        self.assertIn("secondary", data)
        self.assertIn("accessory", data)
        self.assertIn("core", data)
        self.assertIn("conditioning", data)
        
        # Verify parameter mapping per section
        primary = data["primary"]
        self.assertEqual(primary["sets"], 4)
        self.assertEqual(primary["reps"], 3)
        self.assertEqual(primary["intensity"], "80% 1RM (RPE 8)")
        self.assertEqual(primary["rest_seconds"], 90)
        
        secondary = data["secondary"]
        self.assertEqual(secondary["sets"], 3)
        self.assertEqual(secondary["reps"], 5)
        self.assertEqual(secondary["intensity"], "75% 1RM (RPE 7)")
        self.assertEqual(secondary["rest_seconds"], 90)

    def test_generate_session_zero_duplicate_patterns(self):
        # Generate session
        response = self.client.post(
            "/api/v1/sessions/generate",
            json={
                "template_name": "Cricket Fast Bowler Power",
                "athlete_id": 1,
                "equipment": ["Trap Bar", "Medicine Ball", "Cable Machine", "Bodyweight"]
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Collect primary movement patterns of all selected exercises
        patterns = []
        patterns.append(data["warmup"][0]["movement_pattern"])
        patterns.append(data["primary"]["movement_pattern"])
        patterns.append(data["secondary"]["movement_pattern"])
        patterns.append(data["accessory"]["movement_pattern"])
        patterns.append(data["core"]["movement_pattern"])
        patterns.append(data["conditioning"]["movement_pattern"])
        
        # Enforce zero duplicates: total unique patterns must equal the total exercise count
        self.assertEqual(len(patterns), 6)
        self.assertEqual(len(set(patterns)), 6, f"Duplicate movement patterns found: {patterns}")

    def test_generate_session_respect_equipment_filters(self):
        # Sprints and bodyweight only (exclude Trap Bar, Medicine Ball, Cable Machine)
        response = self.client.post(
            "/api/v1/sessions/generate",
            json={
                "template_name": "Cricket Fast Bowler Power",
                "athlete_id": 1,
                "equipment": ["Bodyweight"]
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Hex Bar Jump Squat requires "Trap Bar", so it should NOT be selected as Primary lift
        primary_name = data["primary"]["name"]
        self.assertNotEqual(primary_name, "Trap Bar Jump Squat")
        
        # All exercises must only use Bodyweight
        all_exercises = [
            data["warmup"][0],
            data["primary"],
            data["secondary"],
            data["accessory"],
            data["core"],
            data["conditioning"]
        ]
        
        # Check that none of the selected exercises require unlisted equipment
        # In mock data, A-Skip, Single-Leg Lateral Bound, and Depth Jump are Bodyweight.
        for ex in all_exercises:
            self.assertIn(ex["name"], [
                "Single-Leg Lateral Bound",
                "A-Skip",
                "Single-Leg Isometric Wall Sit",
                "Depth Jump",
                "Nordic Hamstring Curl",
                "Plank with Rotation",
                "Burpee",
                "Bodyweight Squat"
            ])

    def test_generate_session_respect_difficulty_cap(self):
        # Limit athlete to Beginner level
        response = self.client.post(
            "/api/v1/sessions/generate",
            json={
                "template_name": "Cricket Fast Bowler Power",
                "athlete_id": 1,
                "difficulty_cap": "Beginner",
                "equipment": ["Trap Bar", "Medicine Ball", "Cable Machine", "Bodyweight"]
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        all_exercises = [
            data["warmup"][0],
            data["primary"],
            data["secondary"],
            data["accessory"],
            data["core"],
            data["conditioning"]
        ]
        
        for ex in all_exercises:
            self.assertIn(ex["difficulty_level"], ["Beginner"])

    def test_generate_session_athlete_not_found(self):
        response = self.client.post(
            "/api/v1/sessions/generate",
            json={"template_name": "Cricket Fast Bowler Power", "athlete_id": 999}
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"])

if __name__ == "__main__":
    unittest.main()
