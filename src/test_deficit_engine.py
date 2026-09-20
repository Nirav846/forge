# Forge Deficit Detection Engine - Unit Tests
# Role: Senior Sports Performance Engineer
# Description: Automated unit tests to verify S&C range lookups, deficit severity, 
# boundary proximity penalties, and cross-validation confidence score boosts.

import unittest
import asyncio
from deficit_detection_engine import DeficitDetectionService, MockBenchmarkRepository, AssessmentRequest, generate_cache_key

# Event loop runner helper for async testing
def run_async(coro):
    return asyncio.get_event_loop().run_until_complete(coro)

class TestDeficitDetectionEngine(unittest.TestCase):

    def setUp(self):
        self.repo = MockBenchmarkRepository()
        self.service = DeficitDetectionService(self.repo)

    def test_single_test_suboptimal_strength(self):
        # Trap Bar Deadlift of 140kg is Sub-optimal (Range: 120 to 160)
        results = {"Trap Bar Deadlift": 140.0}
        detected = run_async(self.service.detect_deficits(results))
        
        self.assertEqual(len(detected), 1)
        self.assertEqual(detected[0].deficit, "Strength Deficit")
        # Single test, no boundary penalty -> Base confidence 80
        self.assertEqual(detected[0].confidence, 80)

    def test_cross_validation_power_deficit(self):
        # CMJ of 38.0cm is Sub-optimal (Range: 35.0 to 44.99)
        # Broad Jump of 2.10m is Sub-optimal (Range: 1.80 to 2.19)
        # Both CMJ and Broad Jump map to Power Deficit in S&C logic.
        results = {
            "CMJ": 38.0,
            "Broad Jump": 2.10
        }
        
        # When both are evaluated, the confidence gets boosted to 92 due to cross-validation.
        detected = run_async(self.service.detect_deficits(results))
        
        # Verify Power Deficit is detected and has 92% confidence
        power_def = next((d for d in detected if d.deficit == "Power Deficit"), None)
        self.assertIsNotNone(power_def)
        self.assertEqual(power_def.severity, "Moderate")
        self.assertEqual(power_def.confidence, 92)

    def test_boundary_proximity_penalty(self):
        # CMJ of 34.8cm is Poor (< 35.0), but is extremely close (within 5% of boundary).
        # This should trigger a -10 boundary proximity penalty.
        results = {"CMJ": 34.8}
        detected = run_async(self.service.detect_deficits(results))
        
        self.assertEqual(len(detected), 1)
        self.assertEqual(detected[0].deficit, "Power Deficit")
        self.assertEqual(detected[0].severity, "High") # Poor maps to High severity
        # Base (80) - Penalty (10) = 70% confidence
        self.assertEqual(detected[0].confidence, 70)

    def test_optimal_score_no_deficit(self):
        # CMJ of 48.0cm is Optimal (Range: 45.0 to 54.99).
        # No deficit should be logged.
        results = {"CMJ": 48.0}
        detected = run_async(self.service.detect_deficits(results))
        self.assertEqual(len(detected), 0)

    def test_cache_key_generation(self):
        req1 = AssessmentRequest(athlete_id=1, results={"CMJ": 38.0, "Broad Jump": 2.1})
        req2 = AssessmentRequest(athlete_id=1, results={"Broad Jump": 2.1, "CMJ": 38.0})
        
        key1 = generate_cache_key(req1)
        key2 = generate_cache_key(req2)
        
        # Key should be deterministic and ignore dictionary insertion order
        self.assertEqual(key1, key2)

if __name__ == "__main__":
    unittest.main()
