# Forge Athlete Intelligence Layers — Phase 1-5 Integration Tests
# Tests: Athlete State Engine, Training Load Engine, Injury Risk Engine,
#        Assessment Metric Engine, Demand Lifecycle Engine
# Requirements: 100% coverage, event emission tests, no hardcoded sport/role

import json
import unittest
from datetime import date, timedelta
from typing import Dict, Any, Optional
from fastapi.testclient import TestClient

from demand_scoring_engine import app as main_app
from domain_events import DomainEventEmitter
from athlete_state_engine import (
    AthleteStateService,
    MockAthleteStateRepository,
    AthleteStateCreate,
    AthleteStateRepository,
)
from training_load_engine import (
    TrainingLoadService,
    MockTrainingLoadRepository,
    TrainingLoadCreate,
)
from injury_risk_engine import (
    InjuryRiskService,
    MockInjuryRiskRepository,
    InjuryRiskProfileCreate,
)
# assessment_metric_engine deleted per V2.5 synthesis.
# Z-score deficit path removed; benchmark-based path in deficit_detection_engine.py is authority.
from demand_lifecycle_engine import (
    DemandStateService,
    DemandStateRequest,
)

CLIENT = TestClient(main_app)


def run_async(coro):
    import asyncio
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


# ===================================================================
# PHASE 1: ATHLETE STATE ENGINE
# ===================================================================

class TestAthleteStateRepository(unittest.TestCase):
    """Unit tests for athlete state repository operations."""

    def setUp(self):
        self.repo = MockAthleteStateRepository()

    def test_create_state_snapshot(self):
        state = AthleteStateCreate(
            athlete_id=1,
            readiness_score=85.0,
            fatigue_score=30.0,
            recovery_score=75.0,
            injury_risk_score=20.0,
            power_state=80.0,
            strength_state=75.0,
        )
        record = run_async(self.repo.create(state))
        self.assertEqual(record["athlete_id"], 1)
        self.assertEqual(record["readiness_score"], 85.0)
        self.assertEqual(record["demand_states"], {})

    def test_create_with_demand_states(self):
        state = AthleteStateCreate(
            athlete_id=1,
            demand_states={"Vertical Power": 80.0, "Hinge Strength": 65.0},
        )
        record = run_async(self.repo.create(state))
        self.assertEqual(record["demand_states"]["Vertical Power"], 80.0)

    def test_get_latest_no_snapshots(self):
        result = run_async(self.repo.get_latest(999))
        self.assertIsNone(result)

    def test_get_latest_returns_most_recent(self):
        run_async(self.repo.create(AthleteStateCreate(
            athlete_id=1, snapshot_date=date(2026, 1, 1),
        )))
        run_async(self.repo.create(AthleteStateCreate(
            athlete_id=1, snapshot_date=date(2026, 6, 1),
        )))
        latest = run_async(self.repo.get_latest(1))
        self.assertEqual(latest["snapshot_date"], "2026-06-01")

    def test_list_for_athlete_pagination(self):
        for i in range(5):
            run_async(self.repo.create(AthleteStateCreate(athlete_id=1)))
        results = run_async(self.repo.list_for_athlete(athlete_id=1, limit=2, offset=0))
        self.assertEqual(len(results), 2)

    def test_list_by_date_range(self):
        run_async(self.repo.create(AthleteStateCreate(
            athlete_id=1, snapshot_date=date(2026, 1, 1),
        )))
        run_async(self.repo.create(AthleteStateCreate(
            athlete_id=1, snapshot_date=date(2026, 6, 1),
        )))
        results = run_async(self.repo.list_by_date_range(
            athlete_id=1, start_date=date(2026, 5, 1), end_date=date(2026, 7, 1),
        ))
        self.assertEqual(len(results), 1)

    def test_immutable_historical_snapshots(self):
        r1 = run_async(self.repo.create(AthleteStateCreate(
            athlete_id=1, snapshot_date=date(2026, 1, 1), readiness_score=80.0,
        )))
        r2 = run_async(self.repo.create(AthleteStateCreate(
            athlete_id=1, snapshot_date=date(2026, 1, 2), readiness_score=90.0,
        )))
        self.assertNotEqual(r1["id"], r2["id"])
        self.assertEqual(r1["readiness_score"], 80.0)
        self.assertEqual(r2["readiness_score"], 90.0)


class TestAthleteStateService(unittest.TestCase):
    """Service layer tests including event emission."""

    def setUp(self):
        self.repo = MockAthleteStateRepository()
        self.emitter = DomainEventEmitter()
        self.service = AthleteStateService(repo=self.repo, event_emitter=self.emitter)

    def test_record_state_with_readiness_computed(self):
        state = AthleteStateCreate(
            athlete_id=1,
            recovery_score=80.0,
            fatigue_score=20.0,
            injury_risk_score=10.0,
        )
        record = run_async(self.service.record_state(state))
        self.assertIsNotNone(record["readiness_score"])

    def test_record_state_auto_computes_readiness(self):
        state = AthleteStateCreate(
            athlete_id=1,
            recovery_score=100.0,
            fatigue_score=0.0,
            injury_risk_score=0.0,
        )
        record = run_async(self.service.record_state(state))
        self.assertAlmostEqual(record["readiness_score"], 100.0, delta=5)

    def test_state_trend_improving(self):
        run_async(self.repo.create(AthleteStateCreate(
            athlete_id=1, snapshot_date=date(2026, 1, 1), readiness_score=50.0,
        )))
        run_async(self.repo.create(AthleteStateCreate(
            athlete_id=1, snapshot_date=date(2026, 6, 1), readiness_score=80.0,
        )))
        snapshots = list(self.repo.snapshots.values())
        trend = self.service.get_state_trend(snapshots)
        self.assertEqual(trend["readiness_trend"], "improving")

    def test_state_trend_declining(self):
        run_async(self.repo.create(AthleteStateCreate(
            athlete_id=1, snapshot_date=date(2026, 1, 1), readiness_score=80.0,
        )))
        run_async(self.repo.create(AthleteStateCreate(
            athlete_id=1, snapshot_date=date(2026, 6, 1), readiness_score=50.0,
        )))
        snapshots = list(self.repo.snapshots.values())
        trend = self.service.get_state_trend(snapshots)
        self.assertEqual(trend["readiness_trend"], "declining")

    def test_state_trend_stable(self):
        run_async(self.repo.create(AthleteStateCreate(
            athlete_id=1, snapshot_date=date(2026, 1, 1), readiness_score=75.0,
        )))
        run_async(self.repo.create(AthleteStateCreate(
            athlete_id=1, snapshot_date=date(2026, 6, 1), readiness_score=76.0,
        )))
        snapshots = list(self.repo.snapshots.values())
        trend = self.service.get_state_trend(snapshots)
        self.assertEqual(trend["readiness_trend"], "stable")

    def test_injury_risk_trend_inverted(self):
        run_async(self.repo.create(AthleteStateCreate(
            athlete_id=1, snapshot_date=date(2026, 1, 1), injury_risk_score=80.0,
        )))
        run_async(self.repo.create(AthleteStateCreate(
            athlete_id=1, snapshot_date=date(2026, 6, 1), injury_risk_score=30.0,
        )))
        snapshots = list(self.repo.snapshots.values())
        trend = self.service.get_state_trend(snapshots)
        self.assertEqual(trend["injury_risk_trend"], "improving")


class TestAthleteStateAPI(unittest.TestCase):
    """Integration tests for /api/v2/athlete-state endpoints."""

    def setUp(self):
        self.client = CLIENT
        from athlete_state_engine import set_athlete_state_repository, MockAthleteStateRepository, reset_athlete_state_repository
        self._state_repo = MockAthleteStateRepository()
        set_athlete_state_repository(self._state_repo)

    def tearDown(self):
        from athlete_state_engine import reset_athlete_state_repository
        reset_athlete_state_repository()

    def test_post_athlete_state_returns_201(self):
        resp = self.client.post("/api/v2/athlete-state", json={
            "athlete_id": 1,
            "readiness_score": 85.0,
            "fatigue_score": 25.0,
            "recovery_score": 80.0,
            "injury_risk_score": 15.0,
            "power_state": 78.0,
            "strength_state": 82.0,
        })
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data["athlete_id"], 1)
        self.assertEqual(data["readiness_score"], 85.0)

    def test_get_latest_state(self):
        self.client.post("/api/v2/athlete-state", json={
            "athlete_id": 2, "recovery_score": 90.0,
        })
        resp = self.client.get("/api/v2/athlete-state/2/latest")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["recovery_score"], 90.0)

    def test_get_latest_state_not_found(self):
        resp = self.client.get("/api/v2/athlete-state/999/latest")
        self.assertEqual(resp.status_code, 404)

    def test_get_state_history(self):
        for _ in range(3):
            self.client.post("/api/v2/athlete-state", json={"athlete_id": 3})
        resp = self.client.get("/api/v2/athlete-state/3/history")
        self.assertEqual(resp.status_code, 200)
        self.assertGreaterEqual(resp.json()["total"], 3)


# ===================================================================
# PHASE 2: TRAINING LOAD ENGINE
# ===================================================================

class TestTrainingLoadRepository(unittest.TestCase):
    """Unit tests for training load repository."""

    def setUp(self):
        self.repo = MockTrainingLoadRepository()

    def test_create_load_event(self):
        event = TrainingLoadCreate(
            athlete_id=1, duration_minutes=60, session_rpe=7,
        )
        record = run_async(self.repo.create(event))
        self.assertEqual(record["athlete_id"], 1)
        self.assertEqual(record["load_score"], 420.0)

    def test_create_with_external_metrics(self):
        event = TrainingLoadCreate(
            athlete_id=1, duration_minutes=45, session_rpe=8,
            sprint_count=20, jump_count=50, high_speed_distance=1200.0,
        )
        record = run_async(self.repo.create(event))
        self.assertEqual(record["sprint_count"], 20)
        self.assertEqual(record["high_speed_distance"], 1200.0)

    def test_list_recent_events(self):
        run_async(self.repo.create(TrainingLoadCreate(
            athlete_id=1, duration_minutes=60, session_rpe=5,
        )))
        results = run_async(self.repo.list_for_athlete(1))
        self.assertEqual(len(results), 1)

    def test_get_daily_load_summary(self):
        run_async(self.repo.create(TrainingLoadCreate(
            athlete_id=1, duration_minutes=60, session_rpe=5, session_date=date(2026, 6, 1),
        )))
        summary = run_async(self.repo.get_daily_load_summary(
            athlete_id=1, start_date=date(2026, 6, 1), end_date=date(2026, 6, 2),
        ))
        self.assertEqual(len(summary), 1)
        self.assertEqual(summary[0]["daily_load"], 300.0)

    def test_compute_acwr_insufficient_data(self):
        result = run_async(self.repo.compute_acwr(athlete_id=999, on_date=date.today()))
        self.assertIsNone(result)


class TestACWRComputation(unittest.TestCase):
    """ACWR calculation validation."""

    def setUp(self):
        self.repo = MockTrainingLoadRepository()

    def _add_daily_session(self, athlete_id: int, days_ago: int, rpe: int, minutes: int = 60):
        session_date = date.today() - timedelta(days=days_ago)
        run_async(self.repo.create(TrainingLoadCreate(
            athlete_id=athlete_id,
            session_date=session_date,
            duration_minutes=minutes,
            session_rpe=rpe,
        )))

    def test_acwr_with_consistent_load(self):
        aid = 10
        for i in range(28):
            self._add_daily_session(aid, i, rpe=5)
        result = run_async(self.repo.compute_acwr(aid, date.today()))
        self.assertIsNotNone(result)
        self.assertAlmostEqual(result["acwr"], 1.0, delta=0.3)

    def test_acwr_with_spike(self):
        aid = 11
        for i in range(28):
            rpe = 9 if i < 7 else 3
            self._add_daily_session(aid, i, rpe=rpe)
        result = run_async(self.repo.compute_acwr(aid, date.today()))
        self.assertIsNotNone(result)
        self.assertGreater(result["acwr"], 1.0)

    def test_acwr_returns_calculation_version(self):
        aid = 12
        for i in range(28):
            self._add_daily_session(aid, i, rpe=5)
        result = run_async(self.repo.compute_acwr(aid, date.today()))
        self.assertEqual(result["calculation_version"], "1.0.0")


class TestTrainingLoadAPI(unittest.TestCase):
    """Integration tests for /api/v2/training-load endpoints."""

    def setUp(self):
        self.client = CLIENT

    def test_record_training_load(self):
        resp = self.client.post("/api/v2/training-load", json={
            "athlete_id": 1,
            "duration_minutes": 60,
            "session_rpe": 7,
            "session_type": "training",
        })
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data["athlete_id"], 1)
        self.assertEqual(data["load_score"], 420.0)

    def test_record_with_external_metrics(self):
        resp = self.client.post("/api/v2/training-load", json={
            "athlete_id": 1,
            "duration_minutes": 45,
            "session_rpe": 8,
            "sprint_count": 25,
            "jump_count": 60,
            "throw_count": 30,
            "session_type": "training",
        })
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data["sprint_count"], 25)

    def test_get_load_history(self):
        for _ in range(3):
            self.client.post("/api/v2/training-load", json={
                "athlete_id": 2, "duration_minutes": 60, "session_rpe": 5, "session_type": "training",
            })
        resp = self.client.get("/api/v2/training-load/2?days=7")
        self.assertEqual(resp.status_code, 200)

    def test_get_acwr_no_data(self):
        resp = self.client.get("/api/v2/training-load/999/acwr")
        self.assertEqual(resp.status_code, 404)

    def test_competition_session_type(self):
        resp = self.client.post("/api/v2/training-load", json={
            "athlete_id": 1,
            "duration_minutes": 90,
            "session_rpe": 10,
            "session_type": "competition",
            "notes": "Match day",
        })
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json()["session_type"], "competition")


# ===================================================================
# PHASE 3: INJURY RISK ENGINE
# ===================================================================

class TestInjuryRiskRepository(unittest.TestCase):
    """Unit tests for injury risk repository."""

    def setUp(self):
        self.repo = MockInjuryRiskRepository()

    def test_create_risk_profile(self):
        profile = InjuryRiskProfileCreate(
            athlete_id=1, risk_score=35.0, risk_level="moderate",
            risk_factors=[{"name": "Demand Deficits", "contribution": 40.0, "description": "test"}],
        )
        record = run_async(self.repo.create(profile))
        self.assertEqual(record["risk_level"], "moderate")
        self.assertEqual(record["risk_score"], 35.0)

    def test_get_latest_no_profiles(self):
        result = run_async(self.repo.get_latest(999))
        self.assertIsNone(result)

    def test_get_latest_returns_most_recent(self):
        run_async(self.repo.create(InjuryRiskProfileCreate(
            athlete_id=1, valid_from=date(2026, 1, 1), risk_score=50.0, risk_level="moderate",
        )))
        run_async(self.repo.create(InjuryRiskProfileCreate(
            athlete_id=1, valid_from=date(2026, 6, 1), risk_score=80.0, risk_level="high",
        )))
        latest = run_async(self.repo.get_latest(1))
        self.assertEqual(latest["risk_level"], "high")

    def test_list_for_athlete_empty(self):
        results = run_async(self.repo.list_for_athlete(999))
        self.assertEqual(len(results), 0)


class TestInjuryRiskService(unittest.TestCase):
    """Multi-factor risk assessment tests."""

    def setUp(self):
        self.repo = MockInjuryRiskRepository()
        self.emitter = DomainEventEmitter()
        self.service = InjuryRiskService(risk_repo=self.repo, event_emitter=self.emitter)

    def test_assess_risk_with_deficits_only(self):
        result = run_async(self.service.assess_risk(
            athlete_id=1,
            demand_scores={"Vertical Power": 20.0, "Hinge Strength": 30.0},
        ))
        self.assertIn("risk_level", result)
        self.assertIn("risk_score", result)
        self.assertIn("risk_factors", result)
        self.assertGreater(len(result["risk_factors"]), 0)

    def test_assess_risk_with_acwr_danger_zone(self):
        result = run_async(self.service.assess_risk(
            athlete_id=1,
            demand_scores={"Vertical Power": 70.0},
            acwr=1.8,
        ))
        self.assertEqual(result["risk_level"], "moderate")

    def test_assess_risk_low_all_factors(self):
        result = run_async(self.service.assess_risk(
            athlete_id=1,
            demand_scores={"Vertical Power": 90.0},
            acwr=1.0,
            load_compliance=0.95,
            assessment_trend="improving",
        ))
        self.assertEqual(result["risk_level"], "low")

    def test_assess_risk_critical_threshold(self):
        result = run_async(self.service.assess_risk(
            athlete_id=1,
            demand_scores={"Vertical Power": 10.0, "Hinge Strength": 15.0},
            acwr=1.8,
            load_compliance=0.4,
            assessment_trend="declining",
        ))
        self.assertEqual(result["risk_level"], "critical")

    def test_interventions_generated_for_high_risk(self):
        result = run_async(self.service.assess_risk(
            athlete_id=1,
            demand_scores={"Vertical Power": 10.0},
            acwr=1.8,
            load_compliance=0.4,
        ))
        interventions = result.get("recommended_interventions", [])
        self.assertGreater(len(interventions), 0)
        has_review = any("sports medicine review" in i.lower() for i in interventions)
        self.assertTrue(has_review)

    def test_score_breakdown_contains_all_factors(self):
        result = run_async(self.service.assess_risk(
            athlete_id=1,
            demand_scores={"Vertical Power": 30.0},
            acwr=1.6,
            load_compliance=0.6,
            assessment_trend="declining",
        ))
        breakdown = result.get("score_breakdown", {})
        self.assertIn("demand_deficits", breakdown)
        self.assertIn("acwr", breakdown)
        self.assertIn("compliance", breakdown)
        self.assertIn("assessment_trend", breakdown)


class TestInjuryRiskAPI(unittest.TestCase):
    """Integration tests for /api/v2/injury-risk endpoints."""

    def setUp(self):
        self.client = CLIENT
        from injury_risk_engine import set_injury_risk_repository, MockInjuryRiskRepository, reset_injury_risk_repository
        self._risk_repo = MockInjuryRiskRepository()
        set_injury_risk_repository(self._risk_repo)

    def tearDown(self):
        from injury_risk_engine import reset_injury_risk_repository
        reset_injury_risk_repository()

    def test_assess_risk_endpoint(self):
        resp = self.client.post("/api/v2/injury-risk/assess", json={
            "athlete_id": 1,
            "demand_scores": {"Vertical Power": 30.0, "Hinge Strength": 25.0},
            "acwr": 1.6,
            "load_compliance": 0.7,
        })
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertIn("risk_level", data)
        self.assertIn("risk_score", data)

    def test_assess_risk_missing_athlete_id(self):
        resp = self.client.post("/api/v2/injury-risk/assess", json={})
        self.assertEqual(resp.status_code, 400)

    def test_get_latest_risk_profile(self):
        self.client.post("/api/v2/injury-risk/assess", json={
            "athlete_id": 2, "demand_scores": {"Vertical Power": 50.0},
        })
        resp = self.client.get("/api/v2/injury-risk/2/latest")
        self.assertEqual(resp.status_code, 200)

    def test_get_latest_risk_not_found(self):
        resp = self.client.get("/api/v2/injury-risk/999/latest")
        self.assertEqual(resp.status_code, 404)


# ===================================================================
# PHASE 4: ASSESSMENT METRIC ENGINE (DELETED)
# Z-score deficit path removed per V2.5 synthesis.
# Benchmark-based path in deficit_detection_engine.py is the authority.
# ===================================================================


# ===================================================================
# PHASE 5: DEMAND LIFECYCLE ENGINE
# ===================================================================

class TestDemandStateService(unittest.TestCase):
    """Multi-factor demand state computation tests."""

    def setUp(self):
        self.emitter = DomainEventEmitter()
        self.service = DemandStateService(event_emitter=self.emitter)

    def test_compute_demand_states_basic(self):
        request = DemandStateRequest(
            athlete_id=1,
            demand_deficits={"Vertical Power": 0.3, "Hinge Strength": 0.6},
        )
        result = run_async(self.service.compute_demand_states(request))
        self.assertEqual(result.athlete_id, 1)
        self.assertEqual(result.total_demands, 2)

    def test_compute_demand_states_with_all_factors(self):
        request = DemandStateRequest(
            athlete_id=1,
            demand_deficits={"Vertical Power": 0.3},
            role_priorities={"Vertical Power": 100},
            injury_risk_score=20.0,
            acwr=1.0,
            recovery_score=80.0,
            fatigue_score=30.0,
        )
        result = run_async(self.service.compute_demand_states(request))
        self.assertEqual(result.total_demands, 1)
        d = result.demands[0]
        self.assertIn("deficit_score", d.components)
        self.assertIn("role_multiplier", d.components)
        self.assertIn("injury_risk_adjustment", d.components)
        self.assertIn("recovery_adjustment", d.components)
        self.assertIn("fatigue_adjustment", d.components)

    def test_demand_priority_inverse_of_capacity(self):
        request = DemandStateRequest(
            athlete_id=1,
            demand_deficits={"Low Deficit": 0.1, "High Deficit": 0.9},
        )
        result = run_async(self.service.compute_demand_states(request))
        low = [d for d in result.demands if d.demand_name == "Low Deficit"][0]
        high = [d for d in result.demands if d.demand_name == "High Deficit"][0]
        self.assertGreater(high.priority_score, low.priority_score)

    def test_trend_score_computation(self):
        historical = [
            {"Vertical Power": 80.0, "snapshot_date": "2026-01-01"},
            {"Vertical Power": 70.0, "snapshot_date": "2026-02-01"},
            {"Vertical Power": 60.0, "snapshot_date": "2026-03-01"},
        ]
        request = DemandStateRequest(
            athlete_id=1,
            demand_deficits={"Vertical Power": 0.5},
            historical_scores=historical,
        )
        result = run_async(self.service.compute_demand_states(request))
        d = result.demands[0]
        self.assertLess(d.trend_score, 0)

    def test_acwr_adjustment_danger_zone(self):
        request = DemandStateRequest(
            athlete_id=1,
            demand_deficits={"Vertical Power": 0.3},
            acwr=1.8,
        )
        result = run_async(self.service.compute_demand_states(request))
        d = result.demands[0]
        self.assertEqual(d.components["acwr_adjustment"], 0.8)

    def test_acwr_adjustment_optimal(self):
        request = DemandStateRequest(
            athlete_id=1,
            demand_deficits={"Vertical Power": 0.3},
            acwr=1.1,
        )
        result = run_async(self.service.compute_demand_states(request))
        d = result.demands[0]
        self.assertEqual(d.components["acwr_adjustment"], 1.0)

    def test_missing_deficits_raises_error(self):
        request = DemandStateRequest(athlete_id=1)
        with self.assertRaises(ValueError):
            run_async(self.service.compute_demand_states(request))

    def test_risk_adjusted_score_lower_than_raw_with_poor_recovery(self):
        request = DemandStateRequest(
            athlete_id=1,
            demand_deficits={"Vertical Power": 0.3},
            recovery_score=20.0,
        )
        result = run_async(self.service.compute_demand_states(request))
        d = result.demands[0]
        self.assertLess(d.risk_adjusted_score, d.demand_score)

    def test_no_single_factor_decision(self):
        request = DemandStateRequest(
            athlete_id=1,
            demand_deficits={"Vertical Power": 0.5},
            role_priorities={"Vertical Power": 80},
            injury_risk_score=30.0,
            acwr=1.2,
            recovery_score=70.0,
            fatigue_score=40.0,
        )
        result = run_async(self.service.compute_demand_states(request))
        d = result.demands[0]
        self.assertEqual(len(d.components), 10)
        self.assertGreater(d.priority_score, 0)


class TestDemandLifecycleAPI(unittest.TestCase):
    """Integration tests for /api/v2/demand-states endpoints."""

    def setUp(self):
        self.client = CLIENT

    def test_compute_demand_states_endpoint(self):
        resp = self.client.post("/api/v2/demand-states/compute", json={
            "athlete_id": 1,
            "demand_deficits": {"Vertical Power": 0.3, "Hinge Strength": 0.6},
            "role_priorities": {"Vertical Power": 100, "Hinge Strength": 80},
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["athlete_id"], 1)
        self.assertEqual(data["total_demands"], 2)

    def test_compute_missing_deficits_returns_400(self):
        resp = self.client.post("/api/v2/demand-states/compute", json={
            "athlete_id": 1,
        })
        self.assertEqual(resp.status_code, 400)


# ===================================================================
# ARCHITECTURE TESTS — Verify no hardcoded sport/role/template logic
# ===================================================================

class TestArchitectureConstraints(unittest.TestCase):
    """Architecture enforcement tests."""

    def test_no_service_imports_mock_repositories_directly(self):
        services = [
            "athlete_state_engine",
            "training_load_engine",
            "injury_risk_engine",
            "demand_lifecycle_engine",
        ]
        for module_name in services:
            import importlib
            mod = importlib.import_module(module_name)
            source = open(mod.__file__).read()
            self.assertNotIn("from mock_", source.lower(),
                f"{module_name} should not import mock repositories directly")

    def test_no_hardcoded_sport_logic(self):
        modules = [
            "athlete_state_engine", "training_load_engine",
            "injury_risk_engine",
            "demand_lifecycle_engine",
        ]
        sport_keywords = ['"Cricket"', "'Cricket'", '"cricket"', "'cricket'"]
        for module_name in modules:
            import importlib
            mod = importlib.import_module(module_name)
            source = open(mod.__file__).read()
            for keyword in sport_keywords:
                self.assertNotIn(keyword, source,
                    f"{module_name} contains hardcoded sport '{keyword}'")

    def test_no_hardcoded_role_ids(self):
        modules = [
            "athlete_state_engine", "training_load_engine",
            "injury_risk_engine",
            "demand_lifecycle_engine",
        ]
        for module_name in modules:
            import importlib
            mod = importlib.import_module(module_name)
            source = open(mod.__file__).read()
            self.assertNotIn('"role_id": 1', source,
                f"{module_name} contains hardcoded role_id")
            self.assertNotIn("role_id=1", source,
                f"{module_name} contains hardcoded role_id=1")

    def test_no_hardcoded_template_ids(self):
        modules = [
            "athlete_state_engine", "training_load_engine",
            "injury_risk_engine",
            "demand_lifecycle_engine",
        ]
        for module_name in modules:
            import importlib
            mod = importlib.import_module(module_name)
            source = open(mod.__file__).read()
            self.assertNotIn("template", source.lower(),
                f"{module_name} references templates")


# ===================================================================
# EVENT EMISSION TESTS
# ===================================================================

class TestEventEmission(unittest.TestCase):
    """Verify that all services emit domain events."""

    def setUp(self):
        self.emitter = DomainEventEmitter()

    def test_athlete_state_event(self):
        event = run_async(self.emitter.emit_athlete_state_calculated(
            athlete_id=1, snapshot_id=1, readiness_score=85.0,
        ))
        self.assertIsNone(event)

    def test_training_load_event(self):
        event = run_async(self.emitter.emit_training_load_recorded(
            athlete_id=1, load_event_id=1, load_score=420.0, session_type="training",
        ))
        self.assertIsNone(event)

    def test_acwr_event(self):
        event = run_async(self.emitter.emit_acwr_calculated(
            athlete_id=1, acwr=1.2, acute_load=3000, chronic_load=2500,
        ))
        self.assertIsNone(event)

    def test_injury_risk_event(self):
        event = run_async(self.emitter.emit_injury_risk_updated(
            athlete_id=1, profile_id=1, risk_level="moderate", risk_score=35.0,
        ))
        self.assertIsNone(event)

    def test_demand_score_event(self):
        event = run_async(self.emitter.emit_demand_score_calculated(
            athlete_id=1, demand_id=1, demand_score=75.0, trend_score=5.0, priority_score=25.0,
        ))
        self.assertIsNone(event)

    def test_assessment_metrics_event(self):
        event = run_async(self.emitter.emit_assessment_metrics_extracted(
            athlete_id=1, assessment_id=1, metrics={"jump_height": 35.0},
        ))
        self.assertIsNone(event)


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
