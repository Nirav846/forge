# Forge V2 Demand Scoring Engine - Integration Tests
# Role: Senior Backend Engineer
# Description: Validates the Performance Demand Architecture — MockDemandRepository queries,
# compute_role_demand_scores for all 5 cricket roles, deficit factor computation,
# equipment gating, difficulty cap filtering, and the /api/v2/demand-recommendations endpoint.

import json
import unittest
from fastapi.testclient import TestClient

from demand_scoring_engine import (
    app,
    MockDemandRepository,
    PostgreSqlDemandRepository,
    DemandScoringService,
    compute_role_demand_scores,
    compute_deficit_factor_sync,
    training_months_to_level,
    LEVEL_ORDINAL,
    TECH_DIFF_CAP,
    cache,
)


class TestMockDemandRepositoryQueries(unittest.TestCase):
    """Validate repository interface — get_role_by_name, get_demand_by_name,
    get_role_demands, get_exercises_for_demand, get_assessment_demand_mapping."""

    def setUp(self):
        self.repo = MockDemandRepository()

    def test_get_role_by_name_exact_match(self):
        role = run_async(self.repo.get_role_by_name("Cricket", "Fast Bowler"))
        self.assertIsNotNone(role)
        self.assertEqual(role["name"], "Fast Bowler")
        self.assertEqual(role["sport_name"], "Cricket")

    def test_get_role_by_name_case_insensitive(self):
        role = run_async(self.repo.get_role_by_name("cricket", "fast bowler"))
        self.assertIsNotNone(role)
        self.assertEqual(role["name"], "Fast Bowler")

    def test_get_role_by_name_fuzzy_bowler(self):
        """Fuzzy match — any role containing 'bowl' resolves to Fast Bowler."""
        role = run_async(self.repo.get_role_by_name("Cricket", "Bowler"))
        self.assertIsNotNone(role)
        self.assertEqual(role["name"], "Fast Bowler")

    def test_get_role_by_name_fuzzy_spinner(self):
        role = run_async(self.repo.get_role_by_name("Cricket", "Spin"))
        self.assertIsNotNone(role)
        self.assertEqual(role["name"], "Spinner")

    def test_get_role_by_name_fuzzy_batter(self):
        role = run_async(self.repo.get_role_by_name("Cricket", "Bat"))
        self.assertIsNotNone(role)
        self.assertEqual(role["name"], "Batter")

    def test_get_role_by_name_fuzzy_wicket_keeper(self):
        role = run_async(self.repo.get_role_by_name("Cricket", "Keeper"))
        self.assertIsNotNone(role)
        self.assertEqual(role["name"], "Wicket Keeper")

    def test_get_role_by_name_fuzzy_all_rounder(self):
        role = run_async(self.repo.get_role_by_name("Cricket", "All"))
        self.assertIsNotNone(role)
        self.assertEqual(role["name"], "All Rounder")

    def test_get_role_by_name_no_match(self):
        role = run_async(self.repo.get_role_by_name("Cricket", "Coach"))
        self.assertIsNone(role)

    def test_get_demand_by_name(self):
        demand = run_async(self.repo.get_demand_by_name("Vertical Power"))
        self.assertIsNotNone(demand)
        self.assertEqual(demand["id"], 1)
        self.assertEqual(demand["demand_type"], "Biomotor")

    def test_get_demand_by_name_case_insensitive(self):
        demand = run_async(self.repo.get_demand_by_name("vertical power"))
        self.assertIsNotNone(demand)

    def test_get_demand_by_name_no_match(self):
        demand = run_async(self.repo.get_demand_by_name("Flying"))
        self.assertIsNone(demand)

    def test_get_role_demands_fast_bowler(self):
        demands = run_async(self.repo.get_role_demands("Fast Bowler", "Cricket"))
        self.assertEqual(len(demands), 12)
        self.assertEqual(demands[0]["name"], "Vertical Power")
        self.assertEqual(demands[0]["priority"], 100)
        self.assertEqual(demands[0]["category"], "Primary")

    def test_get_role_demands_spinner(self):
        demands = run_async(self.repo.get_role_demands("Spinner", "Cricket"))
        self.assertEqual(len(demands), 12)
        self.assertEqual(demands[0]["name"], "Rotational Explosive Power")

    def test_get_role_demands_batter(self):
        demands = run_async(self.repo.get_role_demands("Batter", "Cricket"))
        self.assertEqual(len(demands), 12)
        self.assertEqual(demands[0]["name"], "Horizontal Drive Power")

    def test_get_role_demands_wicket_keeper(self):
        demands = run_async(self.repo.get_role_demands("Wicket Keeper", "Cricket"))
        self.assertEqual(len(demands), 12)
        self.assertEqual(demands[0]["name"], "Squat Strength")

    def test_get_role_demands_all_rounder(self):
        demands = run_async(self.repo.get_role_demands("All Rounder", "Cricket"))
        self.assertEqual(len(demands), 12)
        self.assertEqual(demands[0]["name"], "Vertical Power")

    def test_get_role_demands_no_match(self):
        demands = run_async(self.repo.get_role_demands("Coach", "Cricket"))
        self.assertEqual(len(demands), 0)

    def test_get_exercises_for_demand_vertical_power(self):
        """Vertical Power (id=1) should return Trap Bar Jump Squat, MB Throw, Power Clean, etc."""
        exs = run_async(self.repo.get_exercises_for_demand(
            demand_id=1, difficulty_cap="Elite",
            equipment=["Trap Bar", "Medicine Ball", "Barbell", "Bodyweight"],
            training_age_months=96, development_level="PERFORMANCE"
        ))
        names = [e["name"] for e in exs]
        self.assertIn("Trap Bar Jump Squat", names)
        self.assertIn("Medicine Ball Overhead Backwards Toss", names)
        self.assertIn("Power Clean", names)
        self.assertIn("Depth Jump", names)
        self.assertEqual(exs[0]["relevance_score"], 10)

    def test_get_exercises_for_demand_equipment_gate(self):
        """Missing 'Trap Bar' should filter out Trap Bar Jump Squat."""
        exs = run_async(self.repo.get_exercises_for_demand(
            demand_id=1, difficulty_cap="Advanced",
            equipment=["Medicine Ball"],
            training_age_months=96, development_level="PERFORMANCE"
        ))
        names = [e["name"] for e in exs]
        self.assertNotIn("Trap Bar Jump Squat", names)

    def test_get_exercises_for_demand_difficulty_cap(self):
        """Beginner cap should exclude Advanced/Elite exercises."""
        exs = run_async(self.repo.get_exercises_for_demand(
            demand_id=13, difficulty_cap="Beginner",
            equipment=["Cable Machine", "Bodyweight"],
            training_age_months=0, development_level="FOUNDATION"
        ))
        for ex in exs:
            rank = {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Elite": 4}
            self.assertLessEqual(rank[ex["difficulty_level"]], 1)

    def test_get_exercises_for_demand_development_level_gate(self):
        """FOUNDATION athletes should not see PERFORMANCE-level exercises."""
        exs = run_async(self.repo.get_exercises_for_demand(
            demand_id=1, difficulty_cap="Elite",
            equipment=["Barbell", "Trap Bar", "Medicine Ball", "Bodyweight"],
            training_age_months=6, development_level="FOUNDATION"
        ))
        for ex in exs:
            self.assertLessEqual(LEVEL_ORDINAL.get(ex.get("minimum_level", "FOUNDATION"), 1), 1)

    def test_get_assessment_demand_mapping_cmj(self):
        mappings = run_async(self.repo.get_assessment_demand_mapping("CMJ"))
        self.assertEqual(len(mappings), 2)
        demand_names = [m["demand_name"] for m in mappings]
        self.assertIn("Vertical Power", demand_names)
        self.assertIn("Single-Leg Power", demand_names)

    def test_get_assessment_demand_mapping_broad_jump(self):
        mappings = run_async(self.repo.get_assessment_demand_mapping("Broad Jump"))
        self.assertEqual(len(mappings), 2)
        demand_names = [m["demand_name"] for m in mappings]
        self.assertIn("Horizontal Drive Power", demand_names)

    def test_get_assessment_demand_mapping_no_match(self):
        mappings = run_async(self.repo.get_assessment_demand_mapping("Unknown Test"))
        self.assertEqual(len(mappings), 0)


class TestComputeRoleDemandScores(unittest.TestCase):
    """Validate demand scoring across all 5 cricket roles with and without assessments."""

    def setUp(self):
        self.repo = MockDemandRepository()

    def test_fast_bowler_with_assessments(self):
        """Fast Bowler with CMJ=38 (deficit in Vertical Power), Broad Jump=2.1 (deficit in Hinge/Horizontal)."""
        scored = run_async(compute_role_demand_scores(
            repo=self.repo, sport="Cricket", role="Fast Bowler",
            results={"CMJ": 38.0, "Broad Jump": 2.1},
            development_level="PERFORMANCE", equipment=["Trap Bar", "Medicine Ball"]
        ))
        self.assertGreater(len(scored), 0)
        # Vertical Power: priority 100, deficit_severity=0.24 (from CMJ)
        # demand_score = (100/100) * (1.0 + 0.24) * 1.0 (PERFORMANCE) * 1.0 * 100 = 124.0
        self.assertEqual(scored[0]["demand_name"], "Vertical Power")
        self.assertEqual(scored[0]["demand_score"], 124.0)
        self.assertEqual(scored[0]["deficit_factor"], 0.24)

    def test_spinner_with_assessments(self):
        """Spinner with Rotational Med Ball Throw — should score Rotational Explosive Power highest."""
        scored = run_async(compute_role_demand_scores(
            repo=self.repo, sport="Cricket", role="Spinner",
            results={"Rotational Med Ball Throw": 8.0},
            development_level="PERFORMANCE", equipment=["Medicine Ball"]
        ))
        self.assertGreater(len(scored), 0)
        self.assertEqual(scored[0]["demand_name"], "Rotational Explosive Power")

    def test_batter_with_assessments(self):
        """Batter — Horizontal Drive Power should rank #1."""
        scored = run_async(compute_role_demand_scores(
            repo=self.repo, sport="Cricket", role="Batter",
            results={"Broad Jump": 2.1},
            development_level="PERFORMANCE", equipment=["Bodyweight"]
        ))
        self.assertGreater(len(scored), 0)
        self.assertEqual(scored[0]["demand_name"], "Horizontal Drive Power")

    def test_wicket_keeper_with_assessments(self):
        """Wicket Keeper — Squat Strength should rank #1."""
        scored = run_async(compute_role_demand_scores(
            repo=self.repo, sport="Cricket", role="Wicket Keeper",
            results={"Trap Bar Deadlift": 140.0},
            development_level="PERFORMANCE", equipment=["Trap Bar"]
        ))
        self.assertGreater(len(scored), 0)
        self.assertEqual(scored[0]["demand_name"], "Squat Strength")

    def test_all_rounder_with_assessments(self):
        """All Rounder — Vertical Power should rank #1."""
        scored = run_async(compute_role_demand_scores(
            repo=self.repo, sport="Cricket", role="All Rounder",
            results={"CMJ": 38.0},
            development_level="PERFORMANCE", equipment=["Barbell"]
        ))
        self.assertGreater(len(scored), 0)
        self.assertEqual(scored[0]["demand_name"], "Vertical Power")

    def test_no_assessments_default_deficit(self):
        """Without assessments, all demands get default deficit_factor of 0.0 (neutral)."""
        scored = run_async(compute_role_demand_scores(
            repo=self.repo, sport="Cricket", role="Fast Bowler",
            results={},
            development_level="PERFORMANCE", equipment=["Barbell"]
        ))
        self.assertGreater(len(scored), 0)
        for sd in scored:
            self.assertEqual(sd["deficit_factor"], 0.0)
            # With deficit_factor=0.0: score = priority * (1.0 + 0.0) * 1.0 * 1.0 / 100 * 100 = priority
            self.assertEqual(sd["demand_score"], float(sd["priority"]))

    def test_development_level_multiplier_foundation(self):
        scored_f = run_async(compute_role_demand_scores(
            repo=self.repo, sport="Cricket", role="Fast Bowler",
            results={"CMJ": 38.0},
            development_level="FOUNDATION", equipment=["Trap Bar"]
        ))
        scored_p = run_async(compute_role_demand_scores(
            repo=self.repo, sport="Cricket", role="Fast Bowler",
            results={"CMJ": 38.0},
            development_level="PERFORMANCE", equipment=["Trap Bar"]
        ))
        # Foundation multiplier is 0.7, Performance is 1.0
        self.assertEqual(scored_f[0]["demand_score"] / 0.7, scored_p[0]["demand_score"] / 1.0)

    def test_training_months_to_level(self):
        self.assertEqual(training_months_to_level(6), "FOUNDATION")
        self.assertEqual(training_months_to_level(24), "DEVELOPMENT")
        self.assertEqual(training_months_to_level(48), "PERFORMANCE")


class TestDeficitFactorComputation(unittest.TestCase):
    """Validate compute_deficit_factor_sync for various assessment patterns."""

    def setUp(self):
        self.repo = MockDemandRepository()

    def test_cmj_deficit(self):
        """CMJ=38 (out of 50 max) -> deficit_severity = 1 - 38/50 = 0.24, * weight 1.0 = 0.24 -> Vertical Power."""
        factors = compute_deficit_factor_sync(self.repo, {"CMJ": 38.0})
        self.assertIn("Vertical Power", factors)
        self.assertAlmostEqual(factors["Vertical Power"], 0.24, places=2)

    def test_broad_jump_deficit(self):
        """Broad Jump=2.1 (out of 3m max) -> deficit_severity = 1 - 2.1/3.0 = 0.3, * weight 1.0 = 0.30."""
        factors = compute_deficit_factor_sync(self.repo, {"Broad Jump": 2.1})
        self.assertIn("Horizontal Drive Power", factors)
        self.assertAlmostEqual(factors["Horizontal Drive Power"], 0.30, places=2)

    def test_sprint_inversion(self):
        """10m Sprint=1.95s — lower is better, so deficit_severity = 1 - min(1.95/3.0, 1.0) = 0.35."""
        factors = compute_deficit_factor_sync(self.repo, {"10m Sprint": 1.95})
        self.assertIn("Horizontal Drive Power", factors)
        self.assertAlmostEqual(factors["Horizontal Drive Power"], 0.80 * 0.35, places=2)

    def test_multiple_assessments_same_demand(self):
        """CMJ + Broad Jump both map to Horizontal Drive Power — should take max deficit."""
        factors = compute_deficit_factor_sync(self.repo, {"CMJ": 38.0, "Broad Jump": 2.1})
        # CMJ -> Horizontal Drive Power via Single-Leg Power: deficit = 0.24 * 0.6 = 0.14
        # Broad Jump -> Horizontal Drive Power: deficit = 0.30 * 1.0 = 0.30
        self.assertAlmostEqual(factors["Horizontal Drive Power"], 0.30, places=2)

    def test_empty_results(self):
        factors = compute_deficit_factor_sync(self.repo, {})
        self.assertEqual(len(factors), 0)

    def test_deadlift_assessment(self):
        """Trap Bar Deadlift=140 (out of 250 max) -> deficit_severity = 1 - 140/250 = 0.44, * 1.0 = 0.44."""
        factors = compute_deficit_factor_sync(self.repo, {"Trap Bar Deadlift": 140.0})
        self.assertIn("Hinge Strength", factors)
        self.assertAlmostEqual(factors["Hinge Strength"], 0.44, places=2)

    def test_pull_up_assessment(self):
        """Pull Up=10 (out of 20 max) -> deficit_severity = 1 - 10/20 = 0.5, * 1.0 = 0.5."""
        factors = compute_deficit_factor_sync(self.repo, {"Pull Up": 10.0})
        self.assertIn("Vertical Pull Strength", factors)
        self.assertAlmostEqual(factors["Vertical Pull Strength"], 0.50, places=2)


class TestDemandScoringService(unittest.TestCase):
    """Validate the DemandScoringService class methods."""

    def setUp(self):
        self.repo = MockDemandRepository()
        self.service = DemandScoringService(self.repo)

    def test_score_exercise_for_demand_basic(self):
        exercise = {
            "name": "Trap Bar Jump Squat",
            "relevance_score": 10,
            "difficulty_level": "Advanced",
            "mechanics_type": "Compound",
            "force_type": "Push",
        }
        score = self.service.score_exercise_for_demand(
            exercise=exercise, priority_weight=1.0,
            development_level="PERFORMANCE", equipment=["Trap Bar"]
        )
        self.assertAlmostEqual(score, 1.0 * 1.0 * 1.0 * 1.0 * 100, places=2)

    def test_score_exercise_no_equipment_match(self):
        exercise = {
            "name": "Trap Bar Jump Squat",
            "relevance_score": 10,
            "difficulty_level": "Advanced",
            "mechanics_type": "Compound",
            "force_type": "Push",
        }
        score = self.service.score_exercise_for_demand(
            exercise=exercise, priority_weight=1.0,
            development_level="PERFORMANCE", equipment=["Medicine Ball"]
        )
        # eq_match = 0.0 because Trap Bar is required but not in equipment list
        self.assertEqual(score, 0.0)

    def test_score_exercise_foundation_multiplier(self):
        exercise = {
            "name": "Dumbbell Row",
            "relevance_score": 9,
            "difficulty_level": "Beginner",
            "mechanics_type": "Compound",
            "force_type": "Pull",
        }
        score = self.service.score_exercise_for_demand(
            exercise=exercise, priority_weight=0.8,
            development_level="FOUNDATION", equipment=["Dumbbell"]
        )
        self.assertAlmostEqual(score, 0.9 * 0.8 * 0.7 * 1.0 * 100, places=2)


class TestDemandRecommendationsEndpoint(unittest.TestCase):
    """Validate the /api/v2/demand-recommendations FastAPI endpoint."""

    def setUp(self):
        self.client = TestClient(app)
        # Clear cache before each test
        self.client.post("/api/v2/cache/clear")

    def test_demand_recommendations_fast_bowler(self):
        payload = {
            "sport": "Cricket",
            "role": "Fast Bowler",
            "results": {"CMJ": 38.0, "Broad Jump": 2.1},
            "equipment": ["Trap Bar", "Medicine Ball"],
            "difficulty_cap": "Advanced",
            "training_age_months": 96,
        }
        response = self.client.post("/api/v2/demand-recommendations", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["sport"], "Cricket")
        self.assertEqual(data["athlete_role"], "Fast Bowler")
        self.assertEqual(data["engine_mode"], "v2")
        self.assertGreater(len(data["demands"]), 0)
        self.assertGreater(len(data["exercises"]), 0)
        # Top demand should be Vertical Power
        self.assertEqual(data["demands"][0]["demand_name"], "Vertical Power")
        # Top exercise should be Trap Bar Jump Squat or similar
        self.assertIn("Trap Bar", data["exercises"][0]["name"] or data["exercises"][1]["name"])

    def test_demand_recommendations_spinner(self):
        payload = {
            "sport": "Cricket",
            "role": "Spinner",
            "results": {"Rotational Med Ball Throw": 8.0},
            "equipment": ["Medicine Ball"],
            "difficulty_cap": "Advanced",
            "training_age_months": 96,
        }
        response = self.client.post("/api/v2/demand-recommendations", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["athlete_role"], "Spinner")
        self.assertEqual(data["demands"][0]["demand_name"], "Rotational Explosive Power")

    def test_demand_recommendations_batter(self):
        payload = {
            "sport": "Cricket",
            "role": "Batter",
            "results": {"Broad Jump": 2.1},
            "equipment": ["Dumbbell", "Bodyweight"],
            "difficulty_cap": "Intermediate",
            "training_age_months": 24,
        }
        response = self.client.post("/api/v2/demand-recommendations", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["athlete_role"], "Batter")
        self.assertEqual(data["development_level"], "DEVELOPMENT")
        self.assertEqual(data["demands"][0]["demand_name"], "Horizontal Drive Power")

    def test_demand_recommendations_wicket_keeper(self):
        payload = {
            "sport": "Cricket",
            "role": "Wicket Keeper",
            "results": {"Trap Bar Deadlift": 140.0},
            "equipment": ["Trap Bar", "Medicine Ball"],
            "difficulty_cap": "Advanced",
            "training_age_months": 96,
        }
        response = self.client.post("/api/v2/demand-recommendations", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["athlete_role"], "Wicket Keeper")
        self.assertEqual(data["demands"][0]["demand_name"], "Squat Strength")

    def test_demand_recommendations_all_rounder(self):
        payload = {
            "sport": "Cricket",
            "role": "All Rounder",
            "results": {"CMJ": 38.0},
            "equipment": ["Barbell", "Trap Bar", "Medicine Ball", "Dumbbell"],
            "difficulty_cap": "Elite",
            "training_age_months": 48,
        }
        response = self.client.post("/api/v2/demand-recommendations", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["athlete_role"], "All Rounder")
        self.assertEqual(data["demands"][0]["demand_name"], "Vertical Power")

    def test_unknown_role_returns_404(self):
        payload = {
            "sport": "Cricket",
            "role": "Coach",
            "results": {},
            "equipment": ["Bodyweight"],
            "difficulty_cap": "Beginner",
            "training_age_months": 0,
        }
        response = self.client.post("/api/v2/demand-recommendations", json=payload)
        self.assertEqual(response.status_code, 404)

    def test_cache_hit_returns_cached_flag(self):
        payload = {
            "sport": "Cricket",
            "role": "Fast Bowler",
            "results": {"CMJ": 38.0},
            "equipment": ["Trap Bar"],
            "difficulty_cap": "Advanced",
            "training_age_months": 96,
        }
        # First call — cache miss
        r1 = self.client.post("/api/v2/demand-recommendations", json=payload)
        self.assertEqual(r1.status_code, 200)
        self.assertFalse(r1.json()["cached"])
        # Second call — cache hit
        r2 = self.client.post("/api/v2/demand-recommendations", json=payload)
        self.assertEqual(r2.status_code, 200)
        self.assertTrue(r2.json()["cached"])

    def test_cache_clear(self):
        response = self.client.post("/api/v2/cache/clear")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

    def test_engine_mode_endpoint(self):
        response = self.client.get("/api/v2/engine-mode")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn(data["engine_mode"], ["v1", "v2", "dual"])
        self.assertEqual(data["valid_modes"], ["v1", "v2", "dual"])

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["engine_mode"], "v2")

    def test_demand_recommendations_no_results_no_deficit(self):
        """Without results, all deficit factors default to 0.0 (neutral multiplier = 1.0)."""
        payload = {
            "sport": "Cricket",
            "role": "Fast Bowler",
            "results": {},
            "equipment": ["Trap Bar", "Medicine Ball"],
            "difficulty_cap": "Advanced",
            "training_age_months": 96,
        }
        response = self.client.post("/api/v2/demand-recommendations", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        for d in data["demands"]:
            # score = priority * (1.0 + 0.0) * 1.0 (PERFORMANCE) * 1.0 / 100 * 100 = priority
            self.assertEqual(d["demand_score"], float(d["priority"]))

    def test_demand_recommendations_explicit_development_level(self):
        """Explicit development_level overrides training_age_months-derived level."""
        payload = {
            "sport": "Cricket",
            "role": "Fast Bowler",
            "results": {},
            "equipment": ["Trap Bar"],
            "difficulty_cap": "Advanced",
            "training_age_months": 6,
            "development_level": "PERFORMANCE",
        }
        response = self.client.post("/api/v2/demand-recommendations", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["development_level"], "PERFORMANCE")


class TestEquipmentGating(unittest.TestCase):
    """Validate that missing required equipment filters exercises correctly."""

    def setUp(self):
        self.repo = MockDemandRepository()

    def test_trap_bar_jump_squat_needs_trap_bar(self):
        exs = run_async(self.repo.get_exercises_for_demand(
            demand_id=1, difficulty_cap="Elite",
            equipment=["Medicine Ball"],
            training_age_months=96, development_level="PERFORMANCE"
        ))
        names = [e["name"] for e in exs]
        self.assertNotIn("Trap Bar Jump Squat", names)
        self.assertIn("Medicine Ball Overhead Backwards Toss", names)

    def test_bodyweight_exercises_always_available(self):
        exs = run_async(self.repo.get_exercises_for_demand(
            demand_id=13, difficulty_cap="Elite",
            equipment=["Bodyweight"],
            training_age_months=96, development_level="PERFORMANCE"
        ))
        names = [e["name"] for e in exs]
        self.assertIn("Plank with Rotation", names)

    def test_barbell_exercises_filtered_without_barbell(self):
        exs = run_async(self.repo.get_exercises_for_demand(
            demand_id=4, difficulty_cap="Elite",
            equipment=["Dumbbell"],
            training_age_months=96, development_level="PERFORMANCE"
        ))
        names = [e["name"] for e in exs]
        self.assertNotIn("Barbell Back Squat", names)


class TestDifficultyCapFiltering(unittest.TestCase):
    """Validate that difficulty_cap filters exercises correctly."""

    def setUp(self):
        self.repo = MockDemandRepository()

    def test_beginner_cap_excludes_advanced(self):
        exs = run_async(self.repo.get_exercises_for_demand(
            demand_id=1, difficulty_cap="Beginner",
            equipment=["Trap Bar", "Medicine Ball", "Barbell", "Bodyweight"],
            training_age_months=96, development_level="PERFORMANCE"
        ))
        for ex in exs:
            self.assertIn(ex["difficulty_level"], ["Beginner"])

    def test_elite_cap_allows_all(self):
        """Elite cap should not filter out any difficulty levels present in the data."""
        exs = run_async(self.repo.get_exercises_for_demand(
            demand_id=1, difficulty_cap="Elite",
            equipment=["Trap Bar", "Medicine Ball", "Barbell", "Bodyweight"],
            training_age_months=96, development_level="PERFORMANCE"
        ))
        levels_found = {ex["difficulty_level"] for ex in exs}
        # Should include both Intermediate and Advanced exercises (the ones mapped to demand 1)
        self.assertIn("Intermediate", levels_found)
        self.assertIn("Advanced", levels_found)
        self.assertGreater(len(exs), 0)


class TestV2WorkflowIntegration(unittest.TestCase):
    """End-to-end V2 athlete workflow through integration_workflow.py."""

    def setUp(self):
        from integration_workflow import app as iwf_app
        from athlete_module import _mock_repo as athlete_repo
        from assessment_entry_module import _mock_repo as results_repo
        athlete_repo.athletes.clear()
        athlete_repo.counter = 1
        results_repo.results.clear()
        results_repo.counter = 1
        self.client = TestClient(iwf_app)

    def test_v2_workflow_fast_bowler(self):
        payload = {
            "first_name": "Test",
            "last_name": "Bowler",
            "date_of_birth": "1998-05-20",
            "gender": "Male",
            "sport": "Cricket",
            "role": "Fast Bowler",
            "dominant_side": "Right",
            "competition_level": "Elite",
            "training_age_years": 8,
            "training_age_months": 96,
            "results": {"CMJ": 38.0, "Broad Jump": 2.1},
            "equipment": ["Trap Bar", "Medicine Ball"],
            "difficulty_cap": "Advanced",
        }
        response = self.client.post("/api/v2/integration/athlete-workflow", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("athlete_id", data)
        self.assertIn("demand_scores", data)
        self.assertGreater(len(data["demand_scores"]), 0)
        self.assertEqual(data["demand_scores"][0]["demand_name"], "Vertical Power")


# Helper to run async tests
def run_async(coro):
    import asyncio
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


if __name__ == "__main__":
    unittest.main()
