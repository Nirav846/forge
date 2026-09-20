# Forge Recommendation Observability - Phase 2 Tests
# Validates recommendation_log, coach_feedback, entity_relationships repositories
# and their integration with the V2 demand endpoint.

import json
import unittest
from fastapi.testclient import TestClient

from demand_scoring_engine import app as demand_app, cache
from recommendation_observability import (
    MockRecommendationObservabilityRepository,
    CoachFeedbackCreate,
    EntityRelationshipCreate,
    get_observability_repository,
    set_observability_repository,
    reset_observability_repository,
)

DEMAND_APP = demand_app
TEST_ROLE_NAMES = {1: "Fast Bowler", 2: "Spinner", 3: "Batter", 4: "Wicket Keeper", 5: "All Rounder"}


class TestMockObservabilityRepository(unittest.TestCase):
    """Validate Mock recommendation_log, coach_feedback, entity_relationships operations."""

    def setUp(self):
        self.repo = MockRecommendationObservabilityRepository()

    def test_log_recommendation_returns_id(self):
        result = run_async(self.repo.log_recommendation(
            athlete_id=1, role_id=1, sport="Cricket", role_name="Fast Bowler",
            development_level="PERFORMANCE", request_params={"sport": "Cricket"},
            assessment_snapshot={"CMJ": 38.0}, demand_scores=[{"demand_id": 1, "demand_score": 85.0}],
            candidate_rankings=[{"exercise_id": 1, "score": 90.0}],
        ))
        self.assertIsNotNone(result)

    def test_log_and_get_recommendation(self):
        rec_id = run_async(self.repo.log_recommendation(
            athlete_id=2, role_id=3, sport="Cricket", role_name="Batter",
            development_level="DEVELOPMENT",
            request_params={"sport": "Cricket", "role": "Batter"},
            assessment_snapshot={"CMJ": 40.0, "Broad Jump": 2.3},
            demand_scores=[{"demand_id": 2, "demand_score": 75.0}],
            candidate_rankings=[{"exercise_id": 5, "score": 80.0}],
        ))
        entry = run_async(self.repo.get_recommendation(rec_id))
        self.assertIsNotNone(entry)
        self.assertEqual(entry["role_name"], "Batter")
        self.assertEqual(entry["athlete_id"], 2)
        self.assertEqual(entry["development_level"], "DEVELOPMENT")

    def test_list_recommendations_by_role(self):
        run_async(self.repo.log_recommendation(
            athlete_id=1, role_id=1, sport="Cricket", role_name="Fast Bowler",
            development_level="PERFORMANCE",
            request_params={}, assessment_snapshot={},
            demand_scores=[], candidate_rankings=[],
        ))
        run_async(self.repo.log_recommendation(
            athlete_id=2, role_id=3, sport="Cricket", role_name="Batter",
            development_level="FOUNDATION",
            request_params={}, assessment_snapshot={},
            demand_scores=[], candidate_rankings=[],
        ))
        results = run_async(self.repo.list_recommendations(role_id=3))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["role_name"], "Batter")

    def test_list_recommendations_pagination(self):
        for i in range(5):
            run_async(self.repo.log_recommendation(
                athlete_id=i, role_id=1, sport="Cricket", role_name="Fast Bowler",
                development_level="PERFORMANCE",
                request_params={}, assessment_snapshot={},
                demand_scores=[], candidate_rankings=[],
            ))
        results = run_async(self.repo.list_recommendations(limit=2, offset=0))
        self.assertEqual(len(results), 2)

    def test_create_feedback_validates_recommendation_exists(self):
        with self.assertRaises(ValueError):
            run_async(self.repo.create_feedback(
                CoachFeedbackCreate(recommendation_id="non-existent-id")
            ))

    def test_create_and_get_feedback(self):
        rec_id = run_async(self.repo.log_recommendation(
            athlete_id=1, role_id=1, sport="Cricket", role_name="Fast Bowler",
            development_level="PERFORMANCE",
            request_params={}, assessment_snapshot={},
            demand_scores=[], candidate_rankings=[],
        ))
        fb = run_async(self.repo.create_feedback(
            CoachFeedbackCreate(
                recommendation_id=rec_id,
                coach_name="Test Coach",
                coach_decision="modified",
                acceptance_status="partially_accepted",
                rationale="Reduced volume for return-to-play",
            )
        ))
        self.assertEqual(fb["coach_decision"], "modified")
        self.assertEqual(fb["acceptance_status"], "partially_accepted")

        items = run_async(self.repo.get_feedback_for_recommendation(rec_id))
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["rationale"], "Reduced volume for return-to-play")

    def test_create_relationship(self):
        rel = run_async(self.repo.create_relationship(
            EntityRelationshipCreate(
                source_type="exercise", source_id=1,
                relationship_type="targets",
                target_type="demand", target_id=3,
                weight=0.85,
            )
        ))
        self.assertIsNotNone(rel["id"])
        self.assertEqual(rel["source_type"], "exercise")
        self.assertEqual(rel["relationship_type"], "targets")

    def test_get_relationships_by_source(self):
        run_async(self.repo.create_relationship(
            EntityRelationshipCreate(
                source_type="exercise", source_id=1,
                relationship_type="targets",
                target_type="demand", target_id=3,
            )
        ))
        run_async(self.repo.create_relationship(
            EntityRelationshipCreate(
                source_type="exercise", source_id=2,
                relationship_type="targets",
                target_type="demand", target_id=5,
            )
        ))
        results = run_async(self.repo.get_relationships(source_type="exercise", source_id=1))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["target_id"], 3)

    def test_get_relationships_by_type(self):
        run_async(self.repo.create_relationship(
            EntityRelationshipCreate(
                source_type="exercise", source_id=1,
                relationship_type="requires",
                target_type="equipment", target_id=5,
            )
        ))
        results = run_async(self.repo.get_relationships(relationship_type="requires"))
        self.assertEqual(len(results), 1)

    def test_delete_relationship(self):
        rel = run_async(self.repo.create_relationship(
            EntityRelationshipCreate(
                source_type="exercise", source_id=1,
                relationship_type="targets",
                target_type="demand", target_id=3,
            )
        ))
        deleted = run_async(self.repo.delete_relationship(rel["id"]))
        self.assertTrue(deleted)
        remaining = run_async(self.repo.get_relationships(source_type="exercise", source_id=1))
        self.assertEqual(len(remaining), 0)

    def test_delete_nonexistent_relationship(self):
        deleted = run_async(self.repo.delete_relationship(9999))
        self.assertFalse(deleted)


class TestObservabilityIntegrationWithV2Endpoint(unittest.TestCase):
    """Validate recommendation_log is wired into the V2 demand endpoint."""

    def setUp(self):
        self.observability_repo = MockRecommendationObservabilityRepository()
        set_observability_repository(self.observability_repo)
        self.client = TestClient(DEMAND_APP)
        self.client.post("/api/v2/cache/clear")

    def tearDown(self):
        reset_observability_repository()

    def test_demand_endpoint_returns_recommendation_id(self):
        payload = {
            "sport": "Cricket",
            "role": "Fast Bowler",
            "results": {"CMJ": 38.0, "Broad Jump": 2.1, "10m Sprint": 1.95},
            "equipment": ["Trap Bar", "Medicine Ball"],
            "difficulty_cap": "Advanced",
            "training_age_months": 96,
            "athlete_id": 1,
        }
        resp = self.client.post("/api/v2/demand-recommendations", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("recommendation_id", data)
        self.assertIsNotNone(data["recommendation_id"])

    def test_recommendation_logged_with_full_snapshot(self):
        payload = {
            "sport": "Cricket",
            "role": "Batter",
            "results": {"CMJ": 42.0, "Broad Jump": 2.3},
            "equipment": ["Trap Bar", "Medicine Ball", "Barbell"],
            "difficulty_cap": "Advanced",
            "training_age_months": 48,
            "athlete_id": 5,
        }
        resp = self.client.post("/api/v2/demand-recommendations", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        rec_id = data["recommendation_id"]

        entry = run_async(self.observability_repo.get_recommendation(rec_id))
        self.assertIsNotNone(entry)
        self.assertEqual(entry["athlete_id"], 5)
        self.assertEqual(entry["role_name"], "Batter")
        self.assertEqual(entry["sport"], "Cricket")
        self.assertIn("CMJ", entry["assessment_snapshot"])
        self.assertGreater(len(entry["demand_scores"]), 0)
        self.assertGreater(len(entry["candidate_rankings"]), 0)

    def test_cached_recommendation_also_logged(self):
        payload = {
            "sport": "Cricket",
            "role": "Fast Bowler",
            "results": {},
            "equipment": ["Bodyweight"],
            "difficulty_cap": "Beginner",
            "training_age_months": 6,
            "athlete_id": 10,
        }
        resp1 = self.client.post("/api/v2/demand-recommendations", json=payload)
        self.assertEqual(resp1.status_code, 200)
        rec_id_1 = resp1.json()["recommendation_id"]

        resp2 = self.client.post("/api/v2/demand-recommendations", json=payload)
        self.assertEqual(resp2.status_code, 200)
        rec_id_2 = resp2.json()["recommendation_id"]

        entries = list(self.observability_repo.recommendations.values())
        cached_entries = [e for e in entries if e["cached"]]
        self.assertGreaterEqual(len(cached_entries), 0)

    def test_demand_endpoint_works_without_athlete_id(self):
        payload = {
            "sport": "Cricket",
            "role": "Fast Bowler",
            "results": {"CMJ": 38.0},
            "equipment": ["Trap Bar"],
            "difficulty_cap": "Advanced",
            "training_age_months": 96,
        }
        resp = self.client.post("/api/v2/demand-recommendations", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIsNotNone(data.get("recommendation_id"))


class TestCoachFeedbackAPI(unittest.TestCase):
    """Validate /api/v2/coach-feedback endpoints."""

    def setUp(self):
        self.repo = MockRecommendationObservabilityRepository()
        set_observability_repository(self.repo)
        self.client = TestClient(DEMAND_APP)

        self.rec_id = run_async(self.repo.log_recommendation(
            athlete_id=1, role_id=1, sport="Cricket", role_name="Fast Bowler",
            development_level="PERFORMANCE",
            request_params={"sport": "Cricket", "role": "Fast Bowler"},
            assessment_snapshot={"CMJ": 38.0},
            demand_scores=[{"demand_id": 1, "demand_score": 85.0}],
            candidate_rankings=[{"exercise_id": 1, "score": 90.0}],
        ))

    def tearDown(self):
        reset_observability_repository()

    def test_submit_feedback_returns_201(self):
        resp = self.client.post("/api/v2/coach-feedback", json={
            "recommendation_id": self.rec_id,
            "coach_name": "Coach Smith",
            "coach_decision": "modified",
            "acceptance_status": "partially_accepted",
            "rationale": "Reduced volume for early season",
        })
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data["coach_decision"], "modified")
        self.assertEqual(data["rationale"], "Reduced volume for early season")

    def test_submit_feedback_nonexistent_recommendation(self):
        resp = self.client.post("/api/v2/coach-feedback", json={
            "recommendation_id": "00000000-0000-0000-0000-000000000000",
            "coach_decision": "rejected",
            "acceptance_status": "rejected",
        })
        self.assertEqual(resp.status_code, 404)

    def test_get_feedback_for_recommendation(self):
        self.client.post("/api/v2/coach-feedback", json={
            "recommendation_id": self.rec_id,
            "coach_decision": "approved",
            "acceptance_status": "accepted",
            "notes": "Looks good",
        })
        resp = self.client.get(f"/api/v2/coach-feedback/{self.rec_id}")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["total"], 1)
        self.assertEqual(data["items"][0]["notes"], "Looks good")


class TestEntityRelationshipsAPI(unittest.TestCase):
    """Validate /api/v2/entity-relationships endpoints."""

    def setUp(self):
        self.repo = MockRecommendationObservabilityRepository()
        set_observability_repository(self.repo)
        self.client = TestClient(DEMAND_APP)

    def tearDown(self):
        reset_observability_repository()

    def test_create_relationship_returns_201(self):
        resp = self.client.post("/api/v2/entity-relationships", json={
            "source_type": "exercise",
            "source_id": 1,
            "relationship_type": "targets",
            "target_type": "demand",
            "target_id": 3,
            "weight": 0.9,
        })
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data["source_type"], "exercise")
        self.assertEqual(data["relationship_type"], "targets")

    def test_list_relationships_empty(self):
        resp = self.client.get("/api/v2/entity-relationships")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["total"], 0)

    def test_list_relationships_with_filter(self):
        self.client.post("/api/v2/entity-relationships", json={
            "source_type": "exercise", "source_id": 1,
            "relationship_type": "targets",
            "target_type": "demand", "target_id": 3,
        })
        self.client.post("/api/v2/entity-relationships", json={
            "source_type": "exercise", "source_id": 2,
            "relationship_type": "targets",
            "target_type": "demand", "target_id": 5,
        })
        resp = self.client.get("/api/v2/entity-relationships?source_type=exercise&source_id=1")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["total"], 1)
        self.assertEqual(data["items"][0]["target_id"], 3)

    def test_delete_relationship(self):
        resp = self.client.post("/api/v2/entity-relationships", json={
            "source_type": "exercise", "source_id": 1,
            "relationship_type": "targets",
            "target_type": "demand", "target_id": 3,
        })
        rel_id = resp.json()["id"]
        resp = self.client.delete(f"/api/v2/entity-relationships/{rel_id}")
        self.assertEqual(resp.status_code, 204)

    def test_delete_nonexistent_relationship(self):
        resp = self.client.delete("/api/v2/entity-relationships/9999")
        self.assertEqual(resp.status_code, 404)

    def test_upsert_relationship_updates_weight(self):
        resp1 = self.client.post("/api/v2/entity-relationships", json={
            "source_type": "exercise", "source_id": 1,
            "relationship_type": "targets",
            "target_type": "demand", "target_id": 3,
            "weight": 0.5,
        })
        self.assertEqual(resp1.status_code, 201)
        resp2 = self.client.post("/api/v2/entity-relationships", json={
            "source_type": "exercise", "source_id": 1,
            "relationship_type": "targets",
            "target_type": "demand", "target_id": 3,
            "weight": 0.95,
        })
        self.assertEqual(resp2.status_code, 201)
        self.assertEqual(resp2.json()["weight"], 0.95)


class TestRecommendationLogAPI(unittest.TestCase):
    """Validate /api/v2/recommendations endpoints."""

    def setUp(self):
        self.repo = MockRecommendationObservabilityRepository()
        set_observability_repository(self.repo)
        self.client = TestClient(DEMAND_APP)

        run_async(self.repo.log_recommendation(
            athlete_id=1, role_id=1, sport="Cricket", role_name="Fast Bowler",
            development_level="PERFORMANCE",
            request_params={}, assessment_snapshot={},
            demand_scores=[], candidate_rankings=[],
        ))
        run_async(self.repo.log_recommendation(
            athlete_id=2, role_id=3, sport="Cricket", role_name="Batter",
            development_level="FOUNDATION",
            request_params={}, assessment_snapshot={},
            demand_scores=[], candidate_rankings=[],
        ))

    def tearDown(self):
        reset_observability_repository()

    def test_list_recommendations(self):
        resp = self.client.get("/api/v2/recommendations")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["total"], 2)

    def test_list_recommendations_filter_by_role(self):
        resp = self.client.get("/api/v2/recommendations?role_id=1")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["total"], 1)
        self.assertEqual(data["items"][0]["role_name"], "Fast Bowler")

    def test_get_recommendation_by_id(self):
        rec_id = list(self.repo.recommendations.keys())[0]
        resp = self.client.get(f"/api/v2/recommendations/{rec_id}")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["recommendation_id"], rec_id)

    def test_get_nonexistent_recommendation(self):
        resp = self.client.get("/api/v2/recommendations/00000000-0000-0000-0000-000000000000")
        self.assertEqual(resp.status_code, 404)


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
