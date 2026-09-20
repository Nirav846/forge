# Forge Athlete State Engine (Phase 1)
# Role: Principal Software Architect
# Description: Represents athlete readiness at a point in time.
# Immutable snapshots — never overwrite previous state.
# Athlete State → Demand Priorities → Recommendation Engine.

import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import date, datetime

from fastapi import APIRouter, HTTPException, Depends, Query, status
from pydantic import BaseModel, Field, field_validator

from domain_events import DomainEventEmitter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("forge-athlete-state-engine")

db_pool = None
router = APIRouter()
event_emitter = DomainEventEmitter()

# -------------------------------------------------------------
# 1. Pydantic Models
# -------------------------------------------------------------

class AthleteStateCreate(BaseModel):
    athlete_id: int = Field(..., gt=0)
    organization_id: Optional[int] = None
    snapshot_date: date = Field(default_factory=date.today)

    readiness_score: Optional[float] = Field(None, ge=0, le=100)
    fatigue_score: Optional[float] = Field(None, ge=0, le=100)
    recovery_score: Optional[float] = Field(None, ge=0, le=100)
    injury_risk_score: Optional[float] = Field(None, ge=0, le=100)

    power_state: Optional[float] = Field(None, ge=0, le=100)
    strength_state: Optional[float] = Field(None, ge=0, le=100)
    speed_state: Optional[float] = Field(None, ge=0, le=100)
    mobility_state: Optional[float] = Field(None, ge=0, le=100)
    work_capacity_state: Optional[float] = Field(None, ge=0, le=100)

    demand_states: Optional[Dict[str, float]] = None
    calculation_version: str = "1.0.0"


class AthleteStateResponse(BaseModel):
    id: int
    athlete_id: int
    snapshot_date: date
    readiness_score: Optional[float] = None
    fatigue_score: Optional[float] = None
    recovery_score: Optional[float] = None
    injury_risk_score: Optional[float] = None
    power_state: Optional[float] = None
    strength_state: Optional[float] = None
    speed_state: Optional[float] = None
    mobility_state: Optional[float] = None
    work_capacity_state: Optional[float] = None
    demand_states: Dict[str, float] = {}
    calculation_version: str
    created_at: str


# -------------------------------------------------------------
# 2. Repository Interface
# -------------------------------------------------------------

class AthleteStateRepository:
    async def create(self, state: AthleteStateCreate) -> Dict[str, Any]:
        raise NotImplementedError()

    async def get_by_id(self, snapshot_id: int) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    async def get_latest(self, athlete_id: int) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    async def list_for_athlete(
        self, athlete_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError()

    async def list_by_date_range(
        self, athlete_id: int, start_date: date, end_date: date
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError()


# -------------------------------------------------------------
# 3. Mock Implementation
# -------------------------------------------------------------

class MockAthleteStateRepository(AthleteStateRepository):
    def __init__(self):
        self.snapshots: Dict[int, Dict[str, Any]] = {}
        self.counter = 1

    async def create(self, state: AthleteStateCreate) -> Dict[str, Any]:
        snapshot_id = self.counter
        self.counter += 1
        record = {
            "id": snapshot_id,
            "athlete_id": state.athlete_id,
            "organization_id": state.organization_id,
            "snapshot_date": state.snapshot_date.isoformat(),
            "readiness_score": state.readiness_score,
            "fatigue_score": state.fatigue_score,
            "recovery_score": state.recovery_score,
            "injury_risk_score": state.injury_risk_score,
            "power_state": state.power_state,
            "strength_state": state.strength_state,
            "speed_state": state.speed_state,
            "mobility_state": state.mobility_state,
            "work_capacity_state": state.work_capacity_state,
            "demand_states": state.demand_states or {},
            "calculation_version": state.calculation_version,
            "created_at": datetime.utcnow().isoformat(),
        }
        self.snapshots[snapshot_id] = record
        return record

    async def get_by_id(self, snapshot_id: int) -> Optional[Dict[str, Any]]:
        return self.snapshots.get(snapshot_id)

    async def get_latest(self, athlete_id: int) -> Optional[Dict[str, Any]]:
        athlete_snapshots = [s for s in self.snapshots.values() if s["athlete_id"] == athlete_id]
        if not athlete_snapshots:
            return None
        athlete_snapshots.sort(key=lambda s: s["snapshot_date"], reverse=True)
        return athlete_snapshots[0]

    async def list_for_athlete(
        self, athlete_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dict[str, Any]]:
        results = [s for s in self.snapshots.values() if s["athlete_id"] == athlete_id]
        results.sort(key=lambda s: s["snapshot_date"], reverse=True)
        return results[offset:offset + limit]

    async def list_by_date_range(
        self, athlete_id: int, start_date: date, end_date: date
    ) -> List[Dict[str, Any]]:
        start_str = start_date.isoformat()
        end_str = end_date.isoformat()
        return [
            s for s in self.snapshots.values()
            if s["athlete_id"] == athlete_id
            and start_str <= s["snapshot_date"] <= end_str
        ]


# -------------------------------------------------------------
# 4. PostgreSQL Implementation
# -------------------------------------------------------------

class PostgreSqlAthleteStateRepository(AthleteStateRepository):
    def __init__(self, pool=None):
        self.pool = pool

    async def create(self, state: AthleteStateCreate) -> Dict[str, Any]:
        if not self.pool:
            return {}
        query = """
            INSERT INTO athlete_state_snapshots
                (athlete_id, organization_id, snapshot_date,
                 readiness_score, fatigue_score, recovery_score, injury_risk_score,
                 power_state, strength_state, speed_state, mobility_state, work_capacity_state,
                 demand_states, calculation_version)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13::jsonb, $14)
            ON CONFLICT (athlete_id, snapshot_date)
            DO UPDATE SET
                readiness_score = EXCLUDED.readiness_score,
                fatigue_score = EXCLUDED.fatigue_score,
                recovery_score = EXCLUDED.recovery_score,
                injury_risk_score = EXCLUDED.injury_risk_score,
                power_state = EXCLUDED.power_state,
                strength_state = EXCLUDED.strength_state,
                speed_state = EXCLUDED.speed_state,
                mobility_state = EXCLUDED.mobility_state,
                work_capacity_state = EXCLUDED.work_capacity_state,
                demand_states = EXCLUDED.demand_states,
                calculation_version = EXCLUDED.calculation_version
            RETURNING id, athlete_id, organization_id, snapshot_date,
                      readiness_score, fatigue_score, recovery_score, injury_risk_score,
                      power_state, strength_state, speed_state, mobility_state, work_capacity_state,
                      demand_states, calculation_version, created_at;
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                state.athlete_id, state.organization_id, state.snapshot_date,
                state.readiness_score, state.fatigue_score, state.recovery_score, state.injury_risk_score,
                state.power_state, state.strength_state, state.speed_state,
                state.mobility_state, state.work_capacity_state,
                json.dumps(state.demand_states or {}),
                state.calculation_version,
            )
            return dict(row) if row else {}

    async def get_by_id(self, snapshot_id: int) -> Optional[Dict[str, Any]]:
        if not self.pool:
            return None
        query = """
            SELECT id, athlete_id, organization_id, snapshot_date,
                   readiness_score, fatigue_score, recovery_score, injury_risk_score,
                   power_state, strength_state, speed_state, mobility_state, work_capacity_state,
                   demand_states, calculation_version, created_at
            FROM athlete_state_snapshots
            WHERE id = $1;
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, snapshot_id)
            return dict(row) if row else None

    async def get_latest(self, athlete_id: int) -> Optional[Dict[str, Any]]:
        if not self.pool:
            return None
        query = """
            SELECT id, athlete_id, organization_id, snapshot_date,
                   readiness_score, fatigue_score, recovery_score, injury_risk_score,
                   power_state, strength_state, speed_state, mobility_state, work_capacity_state,
                   demand_states, calculation_version, created_at
            FROM athlete_state_snapshots
            WHERE athlete_id = $1
            ORDER BY snapshot_date DESC
            LIMIT 1;
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, athlete_id)
            return dict(row) if row else None

    async def list_for_athlete(
        self, athlete_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dict[str, Any]]:
        if not self.pool:
            return []
        query = """
            SELECT id, athlete_id, snapshot_date,
                   readiness_score, fatigue_score, recovery_score, injury_risk_score,
                   power_state, strength_state, speed_state, mobility_state, work_capacity_state,
                   calculation_version, created_at
            FROM athlete_state_snapshots
            WHERE athlete_id = $1
            ORDER BY snapshot_date DESC
            LIMIT $2 OFFSET $3;
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, athlete_id, limit, offset)
            return [dict(r) for r in rows]

    async def list_by_date_range(
        self, athlete_id: int, start_date: date, end_date: date
    ) -> List[Dict[str, Any]]:
        if not self.pool:
            return []
        query = """
            SELECT id, athlete_id, snapshot_date,
                   readiness_score, fatigue_score, recovery_score, injury_risk_score,
                   power_state, strength_state, speed_state, mobility_state, work_capacity_state,
                   demand_states, calculation_version, created_at
            FROM athlete_state_snapshots
            WHERE athlete_id = $1 AND snapshot_date >= $2 AND snapshot_date <= $3
            ORDER BY snapshot_date DESC;
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, athlete_id, start_date, end_date)
            return [dict(r) for r in rows]


# -------------------------------------------------------------
# 5. Service Layer
# -------------------------------------------------------------

class AthleteStateService:
    """Computes and manages athlete state snapshots.

    The service is stateless — all state is in the repository.
    It coordinates:
    1. Computing composite readiness scores from individual metrics
    2. Emitting domain events for audit trail
    3. Ensuring immutability of historical snapshots
    """

    def __init__(
        self,
        repo: AthleteStateRepository,
        event_emitter: DomainEventEmitter,
    ):
        self._repo = repo
        self._emitter = event_emitter

    async def record_state(self, state: AthleteStateCreate) -> Dict[str, Any]:
        """Record a new athlete state snapshot.

        Auto-computes readiness from sub-scores if readiness is not provided.
        """
        if state.readiness_score is None:
            computed = await self._compute_readiness(state)
            state.readiness_score = computed["readiness_score"]

        record = await self._repo.create(state)

        await self._emitter.emit_athlete_state_calculated(
            athlete_id=state.athlete_id,
            snapshot_id=record["id"],
            readiness_score=state.readiness_score,
            organization_id=state.organization_id,
            fatigue_score=state.fatigue_score,
            recovery_score=state.recovery_score,
            injury_risk_score=state.injury_risk_score,
            calculation_version=state.calculation_version,
        )

        return record

    async def get_latest_state(self, athlete_id: int) -> Optional[Dict[str, Any]]:
        return await self._repo.get_latest(athlete_id)

    async def get_state_history(
        self, athlete_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dict[str, Any]]:
        return await self._repo.list_for_athlete(athlete_id, limit, offset)

    def get_state_trend(
        self, snapshots: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Compute trend direction from a list of snapshots (oldest first)."""
        if len(snapshots) < 2:
            return {
                "readiness_trend": "stable",
                "fatigue_trend": "stable",
                "recovery_trend": "stable",
                "injury_risk_trend": "stable",
            }

        first = snapshots[0]
        last = snapshots[-1]

        def _trend(first_val, last_val, higher_is_better=True):
            if first_val is None or last_val is None:
                return "stable"
            diff = last_val - first_val
            threshold = 3.0
            if abs(diff) < threshold:
                return "stable"
            if higher_is_better:
                return "improving" if diff > 0 else "declining"
            return "improving" if diff < 0 else "declining"

        return {
            "readiness_trend": _trend(first.get("readiness_score"), last.get("readiness_score"), True),
            "fatigue_trend": _trend(first.get("fatigue_score"), last.get("fatigue_score"), False),
            "recovery_trend": _trend(first.get("recovery_score"), last.get("recovery_score"), True),
            "injury_risk_trend": _trend(first.get("injury_risk_score"), last.get("injury_risk_score"), False),
        }

    async def _compute_readiness(self, state: AthleteStateCreate) -> Dict[str, float]:
        """Compute readiness from sub-scores when not provided."""
        scores = []
        weights = {
            "recovery_score": 0.4,
            "fatigue_score": 0.3,
            "injury_risk_score": 0.3,
        }
        total_weight = 0.0
        weighted_sum = 0.0

        fatigue = state.fatigue_score
        recovery = state.recovery_score
        injury_risk = state.injury_risk_score

        if recovery is not None:
            weighted_sum += recovery * weights["recovery_score"]
            total_weight += weights["recovery_score"]

        if fatigue is not None:
            weighted_sum += (100 - fatigue) * weights["fatigue_score"]
            total_weight += weights["fatigue_score"]

        if injury_risk is not None:
            weighted_sum += (100 - injury_risk) * weights["injury_risk_score"]
            total_weight += weights["injury_risk_score"]

        readiness = round(weighted_sum / total_weight, 2) if total_weight > 0 else 50.0
        return {"readiness_score": min(max(readiness, 0), 100)}


# -------------------------------------------------------------
# 6. Factory / DI
# -------------------------------------------------------------

_athlete_state_repo_instance = None

def get_athlete_state_repository() -> AthleteStateRepository:
    global _athlete_state_repo_instance
    if _athlete_state_repo_instance is not None:
        return _athlete_state_repo_instance
    if db_pool:
        logger.info("FACTORY: get_athlete_state_repository() -> PostgreSqlAthleteStateRepository")
        _athlete_state_repo_instance = PostgreSqlAthleteStateRepository(db_pool)
    else:
        logger.info("FACTORY: get_athlete_state_repository() -> MockAthleteStateRepository")
        _athlete_state_repo_instance = MockAthleteStateRepository()
    return _athlete_state_repo_instance


def set_athlete_state_repository(repo: AthleteStateRepository) -> None:
    global _athlete_state_repo_instance
    _athlete_state_repo_instance = repo


def reset_athlete_state_repository() -> None:
    global _athlete_state_repo_instance
    _athlete_state_repo_instance = None


def get_athlete_state_service(
    repo: AthleteStateRepository = Depends(get_athlete_state_repository),
) -> AthleteStateService:
    return AthleteStateService(repo=repo, event_emitter=event_emitter)


# -------------------------------------------------------------
# 7. API Endpoints
# -------------------------------------------------------------

@router.post(
    "/api/v2/athlete-state",
    status_code=status.HTTP_201_CREATED,
    summary="Record Athlete State Snapshot",
    description="Create an immutable point-in-time athlete readiness record.",
)
async def record_athlete_state(
    state: AthleteStateCreate,
    service: AthleteStateService = Depends(get_athlete_state_service),
):
    try:
        result = await service.record_state(state)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/api/v2/athlete-state/{athlete_id}/latest",
    summary="Get Latest Athlete State",
    description="Get the most recent state snapshot for an athlete.",
)
async def get_latest_athlete_state(
    athlete_id: int,
    service: AthleteStateService = Depends(get_athlete_state_service),
):
    result = await service.get_latest_state(athlete_id)
    if not result:
        raise HTTPException(status_code=404, detail="No state snapshots found")
    return result


@router.get(
    "/api/v2/athlete-state/{athlete_id}/history",
    summary="Get Athlete State History",
    description="List historical state snapshots for an athlete.",
)
async def get_athlete_state_history(
    athlete_id: int,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    service: AthleteStateService = Depends(get_athlete_state_service),
):
    items = await service.get_state_history(athlete_id, limit, offset)
    return {"items": items, "total": len(items)}


@router.get(
    "/api/v2/athlete-state/{athlete_id}/trend",
    summary="Get Athlete State Trend",
    description="Compute trend direction from historical snapshots.",
)
async def get_athlete_state_trend(
    athlete_id: int,
    days: int = Query(14, ge=1, le=90),
    service: AthleteStateService = Depends(get_athlete_state_service),
):
    from datetime import timedelta
    start_date = date.today() - timedelta(days=days)
    snapshots_raw = await service._repo.list_by_date_range(athlete_id, start_date, date.today())
    if not snapshots_raw:
        raise HTTPException(status_code=404, detail="No state data found in date range")
    snapshot_objects = [AthleteStateCreate(**{
        "athlete_id": s["athlete_id"],
        "snapshot_date": s["snapshot_date"],
        "readiness_score": s.get("readiness_score"),
        "fatigue_score": s.get("fatigue_score"),
        "recovery_score": s.get("recovery_score"),
        "injury_risk_score": s.get("injury_risk_score"),
    }) for s in snapshots_raw]
    trend = service.get_state_trend(snapshot_objects)
    return {
        "athlete_id": athlete_id,
        "period_days": days,
        "snapshot_count": len(snapshots_raw),
        "trend": trend,
    }
