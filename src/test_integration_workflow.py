# Forge Integration Workflow - Unit/Integration Tests
# Role: Principal Integration Architect
# Description: Validates the end-to-end athlete creation, test score logging, 
# deficit diagnostics, and recommended exercise compilation flow.

import json
import unittest
from fastapi.testclient import TestClient

from athlete_module import _mock_repo as athlete_repo
from assessment_entry_module import _mock_repo as results_repo
from integration_workflow import app

class TestIntegrationWorkflow(unittest.TestCase):

    def setUp(self):
        # Reset mock databases
        athlete_repo.athletes.clear()
        athlete_repo.counter = 1
        results_repo.results.clear()
        results_repo.counter = 1
        self.client = TestClient(app)

    def test_end_to_end_athlete_prescription_flow(self):
        # 1. Prepare workflow request matching Cricket Fast Bowler test case
        payload = {
            "first_name": "Nirav",
            "last_name": "Patel",
            "date_of_birth": "1998-05-20",
            "gender": "Male",
            "sport": "Cricket",
            "role": "Fast Bowler",
            "dominant_side": "Right",
            "competition_level": "Elite",
            "training_age_years": 8,
            "training_age_months": 96,
            "results": {
                "CMJ": 38.00,
                "Broad Jump": 2.10,
                "10m Sprint": 1.95
            },
            "equipment": ["Trap Bar", "Medicine Ball"],
            "difficulty_cap": "Advanced"
        }

        # 2. Invoke integration endpoint
        response = self.client.post("/api/v1/integration/athlete-workflow", json=payload)
        
        # 3. Assert HTTP response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # 4. Verify athlete profile creation
        self.assertEqual(data["athlete_id"], 1)
        self.assertEqual(data["athlete_name"], "Nirav Patel")
        
        # 5. Verify deficit diagnostics (CMJ and Broad Jump agreement)
        deficits = data["diagnosed_deficits"]
        self.assertEqual(len(deficits), 3)
        
        # Search for Power Deficit with 92% confidence (CMJ + Broad Jump cross-validation)
        power_def = next((d for d in deficits if d["deficit"] == "Power Deficit"), None)
        self.assertIsNotNone(power_def)
        self.assertEqual(power_def["severity"], "Moderate")
        self.assertEqual(power_def["confidence"], 92)

        # Search for Acceleration Deficit with 70% confidence (single 10m sprint test, borderline penalty applied)
        acc_def = next((d for d in deficits if d["deficit"] == "Acceleration Deficit"), None)
        self.assertIsNotNone(acc_def)
        self.assertEqual(acc_def["severity"], "Moderate")
        self.assertEqual(acc_def["confidence"], 70)

        # Search for Mobility Restriction with 70% confidence (single broad jump test, borderline penalty applied)
        mob_def = next((d for d in deficits if d["deficit"] == "Mobility Restriction"), None)
        self.assertIsNotNone(mob_def)
        self.assertEqual(mob_def["severity"], "Moderate")
        self.assertEqual(mob_def["confidence"], 70)

        # 6. Verify prescribed movement templates and exercise pools
        templates = data["prescribed_templates"]
        self.assertGreater(len(templates), 0)
        
        # The recommendation matching sport='Cricket', role='Fast Bowler', goal='Power'
        # should resolve to the 'Cricket Fast Bowler Power' template.
        bowler_template = next((t for t in templates if "Fast Bowler" in t["template_name"]), None)
        self.assertIsNotNone(bowler_template)
        self.assertEqual(bowler_template["template_name"], "Cricket Fast Bowler Power")
        
        # Verify that Slot 1 ('Max Dynamic Output (Bilateral)') includes 'Trap Bar Jump Squat'
        slots = bowler_template["slots"]
        slot_1 = next((s for s in slots if s["slot_type"] == "Primary"), None)
        self.assertIsNotNone(slot_1)
        self.assertEqual(slot_1["slot_name"], "Max Dynamic Output (Bilateral)")
        
        exercises = slot_1["recommended_exercises"]
        self.assertGreater(len(exercises), 0)
        
        # First exercise should be 'Trap Bar Jump Squat' since it has the highest specificity score (99.00)
        top_ex = exercises[0]
        self.assertEqual(top_ex["name"], "Trap Bar Jump Squat")
        self.assertEqual(top_ex["recommendation_score"], 99.00)
        self.assertEqual(top_ex["difficulty_level"], "Advanced")

        # Save JSON output example for verification report
        print("\nINTEGRATION WORKFLOW DEMO JSON RESPONSE EXAMPLE:")
        print(json.dumps(data, indent=2))

if __name__ == "__main__":
    unittest.main()
