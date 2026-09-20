# Forge Training Load Engine (Phase 2)
# Role: Head Sports Scientist
# Description: Sport-agnostic training load recording with ACWR calculation.
# Internal load via session RPE × duration. External load via configurable metrics.
# All metric definitions are at the application layer — no hardcoded logic.

import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import date, datetime, timedelta

from fastapi import APIRouter, HTTPException, Depends, Query, status
from pydantic import BaseModel, Field

from domain_events import DomainEventEmitter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("forge-training-load-engine")

db_pool = None
router = APIRouter()
event_emitter = DomainEventEmitter()

# -------------------------------------------------------------
# 1. Pydantic Models
# -------------------------------------------------------------

class TrainingLoadCreate(BaseModel):
    athlete_id: int = Field(..., gt=0)
    organization_id: Optional[int] = None
    session_date: date = Field(default_factory=date.today)
    session_type: str = Field(default="training", pattern=r"^(training|competition|recovery|other)$")
    duration_minutes: int = Field(..., gt=0)
    session_rpe: int = Field(..., ge=1, le=10)

    sprint_count: Optional[int] = Field(None, ge=0)
    jump_count: Optional[int] = Field(None, ge=0)
    throw_count: Optional[int] = Field(None, ge=0)
    high_speed_distance: Optional[float] = Field(None, ge=0)

    optional_metrics: Optional[Dict[str, Any]] = None
    source: Optional[str] = None
    notes: Optional[str] = None


class TrainingLoadResponse(BaseModel):
    id: int
    athlete_id: int
    session_date: str
    session_type: str
    duration_minutes: int
    session_rpe: int
    load_score: float
    sprint_count: Optional[int] = None
    jump_count: Optional[int] = None
    throw_count: Optional[int] = None
    high_speed_distance: Optional[float] = None
    optional_metrics: Dict[str, Any] = {}
    source: Optional[str] = None
    notes: Optional[str] = None
    created_at: str


class ACWRResponse(BaseModel):
    athlete_id: int
    session_date: str
    acute_7_day_load: Optional[float] = None
    chronic_28_day_load: Optional[float] = None
    acwr: Optional[float] = None
    calculation_version: str = "1.0.0"


# -------------------------------------------------------------
# 2. Repository Interface
# -------------------------------------------------------------

class TrainingLoadRepository:
    async def create(self, event: TrainingLoadCreate) -> Dict[str, Any]:
        raise NotImplementedError()

    async def get_by_id(self, event_id: int) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    async def list_for_athlete(
        self, athlete_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError()

    async def list_by_date_range(
        self, athlete_id: int, start_date: date, end_date: date
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError()

    async def compute_acwr(self, athlete_id: int, on_date: date) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    async def get_daily_load_summary(
        self, athlete_id: int, start_date: date, end_date: date
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError()


# -------------------------------------------------------------
# 3. Mock Implementation
# -------------------------------------------------------------

class MockTrainingLoadRepository(TrainingLoadRepository):
    def __init__(self):
        self.events: Dict[int, Dict[str, Any]] = {}
        self.counter = 1

    async def create(self, event: TrainingLoadCreate) -> Dict[str, Any]:
        event_id = self.counter
        self.counter += 1
        load_score = round(event.duration_minutes * event.session_rpe, 2)
        record = {
            "id": event_id,
            "athlete_id": event.athlete_id,
            "organization_id": event.organization_id,
            "session_date": event.session_date.isoformat(),
            "session_type": event.session_type,
            "duration_minutes": event.duration_minutes,
            "session_rpe": event.session_rpe,
            "load_score": load_score,
            "sprint_count": event.sprint_count,
            "jump_count": event.jump_count,
            "throw_count": event.throw_count,
            "high_speed_distance": event.high_speed_distance,
            "optional_metrics": event.optional_metrics or {},
            "source": event.source,
            "notes": event.notes,
            "created_at": datetime.utcnow().isoformat(),
        }
        self.events[event_id] = record
        return record

    async def get_by_id(self, event_id: int) -> Optional[Dict[str, Any]]:
        return self.events.get(event_id)

    async def list_for_athlete(
        self, athlete_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dict[str, Any]]:
        results = [e for e in self.events.values() if e["athlete_id"] == athlete_id]
        results.sort(key=lambda e: e["session_date"], reverse=True)
        return results[offset:offset + limit]

    async def list_by_date_range(
        self, athlete_id: int, start_date: date, end_date: date
    ) -> List[Dict[str, Any]]:
        start_str = start_date.isoformat()
        end_str = end_date.isoformat()
        return [
            e for e in self.events.values()
            if e["athlete_id"] == athlete_id
            and start_str <= e["session_date"] <= end_str
        ]

    async def compute_acwr(self, athlete_id: int, on_date: date) -> Optional[Dict[str, Any]]:
        today = on_date.isoformat()
        seven_days_ago = (on_date - timedelta(days=6)).isoformat()
        twenty_eight_days_ago = (on_date - timedelta(days=27)).isoformat()

        events_28 = [
            e for e in self.events.values()
            if e["athlete_id"] == athlete_id
            and twenty_eight_days_ago <= e["session_date"] <= today
        ]
        if not events_28:
            return None

        daily_sum = {}
        for e in events_28:
            d = e["session_date"]
            daily_sum[d] = daily_sum.get(d, 0) + e["load_score"]

        sorted_dates = sorted(daily_sum.keys())
        acute_7 = sum(daily_sum[d] for d in sorted_dates if d >= seven_days_ago)
        chronic_28 = sum(daily_sum.values())

        chronic_7_day_equiv = (chronic_28 / 28.0) * 7.0 if chronic_28 > 0 else 0
        acwr = round(acute_7 / chronic_7_day_equiv, 2) if chronic_7_day_equiv > 0 else None

        return {
            "athlete_id": athlete_id,
            "session_date": today,
            "acute_7_day_load": round(acute_7, 2),
            "chronic_28_day_load": round(chronic_28, 2),
            "acwr": acwr,
            "calculation_version": "1.0.0",
        }

    async def get_daily_load_summary(
        self, athlete_id: int, start_date: date, end_date: date
    ) -> List[Dict[str, Any]]:
        events = await self.list_by_date_range(athlete_id, start_date, end_date)
        daily = {}
        for e in events:
            d = e["session_date"]
            daily[d] = daily.get(d, 0) + e["load_score"]
        return [
            {"session_date": d, "daily_load": round(s, 2)}
            for d, s in sorted(daily.items(), reverse=True)
        ]


# -------------------------------------------------------------
# 4. PostgreSQL Implementation
# -------------------------------------------------------------

class PostgreSqlTrainingLoadRepository(TrainingLoadRepository):
    def __init__(self, pool=None):
        self.pool = pool

    async def create(self, event: TrainingLoadCreate) -> Dict[str, Any]:
        if not self.pool:
            return {}
        load_score = round(event.duration_minutes * event.session_rpe, 2)
        query = """
            INSERT INTO training_load_events
                (athlete_id, organization_id, session_date, session_type,
                 duration_minutes, session_rpe, load_score,
                 sprint_count, jump_count, throw_count, high_speed_distance,
                 optional_metrics, source, notes)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12::jsonb, $13, $14)
            RETURNING id, athlete_id, organization_id, session_date::text, session_type,
                      duration_minutes, session_rpe, load_score,
                      sprint_count, jump_count, throw_count, high_speed_distance,
                      optional_metrics, source, notes, created_at;
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                event.athlete_id, event.organization_id, event.session_date, event.session_type,
                event.duration_minutes, event.session_rpe, load_score,
                event.sprint_count, event.jump_count, event.throw_count, event.high_speed_distance,
                json.dumps(event.optional_metrics or {}),
                event.source, event.notes,
            )
            return dict(row) if row else {}

    async def get_by_id(self, event_id: int) -> Optional[Dict[str, Any]]:
        if not self.pool:
            return None
        query = """
            SELECT * FROM training_load_events WHERE id = $1;
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, event_id)
            return dict(row) if row else None

    async def list_for_athlete(
        self, athlete_id: int, limit: int = 50, offset: int = 0
    ) -> List[Dict[str, Any]]:
        if not self.pool:
            return []
        query = """
            SELECT id, athlete_id, session_date::text, session_type,
                   duration_minutes, session_rpe, load_score,
                   sprint_count, jump_count, throw_count, high_speed_distance,
                   source, notes, created_at
            FROM training_load_events
            WHERE athlete_id = $1
            ORDER BY session_date DESC
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
            SELECT id, athlete_id, session_date::text, session_type,
                   duration_minutes, session_rpe, load_score,
                   sprint_count, jump_count, throw_count, high_speed_distance,
                   optional_metrics, source, notes, created_at
            FROM training_load_events
            WHERE athlete_id = $1 AND session_date >= $2 AND session_date <= $3
            ORDER BY session_date DESC;
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, athlete_id, start_date, end_date)
            return [dict(r) for r in rows]

    async def compute_acwr(self, athlete_id: int, on_date: date) -> Optional[Dict[str, Any]]:
        if not self.pool:
            return None
        query = """
            SELECT athlete_id, session_date::text, acute_7_day_load, chronic_28_day_load,
                   acwr, calculation_version
            FROM acute_chronic_load_view
            WHERE athlete_id = $1 AND session_date <= $2
            ORDER BY session_date DESC
            LIMIT 1;
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, athlete_id, on_date)
            return dict(row) if row else None

    async def get_daily_load_summary(
        self, athlete_id: int, start_date: date, end_date: date
    ) -> List[Dict[str, Any]]:
        if not self.pool:
            return []
        query = """
            SELECT session_date::text, SUM(load_score) as daily_load
            FROM training_load_events
            WHERE athlete_id = $1 AND session_date >= $2 AND session_date <= $3
            GROUP BY session_date
            ORDER BY session_date DESC;
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, athlete_id, start_date, end_date)
            return [dict(r) for r in rows]


# -------------------------------------------------------------
# 5. Service Layer
# -------------------------------------------------------------

class TrainingLoadService:
    def __init__(
        self,
        repo: TrainingLoadRepository,
        event_emitter: DomainEventEmitter,
    ):
        self._repo = repo
        self._emitter = event_emitter

    async def record_load(self, event: TrainingLoadCreate) -> Dict[str, Any]:
        record = await self._repo.create(event)

        await self._emitter.emit_training_load_recorded(
            athlete_id=event.athlete_id,
            load_event_id=record["id"],
            load_score=record["load_score"],
            session_type=event.session_type,
            organization_id=event.organization_id,
            duration_minutes=event.duration_minutes,
            session_rpe=event.session_rpe,
        )

        return record

    async def get_acwr(self, athlete_id: int, on_date: Optional[date] = None) -> Optional[Dict[str, Any]]:
        target_date = on_date or date.today()
        result = await self._repo.compute_acwr(athlete_id, target_date)

        if result and result.get("acwr") is not None:
            await self._emitter.emit_acwr_calculated(
                athlete_id=athlete_id,
                acwr=result["acwr"],
                acute_load=result["acute_7_day_load"],
                chronic_load=result["chronic_28_day_load"],
                organization_id=None,
            )

        return result

    async def get_load_history(
        self, athlete_id: int, days: int = 28
    ) -> Dict[str, Any]:
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        daily_summary = await self._repo.get_daily_load_summary(athlete_id, start_date, end_date)
        acwr = await self._repo.compute_acwr(athlete_id, end_date)
        return {
            "athlete_id": athlete_id,
            "period_days": days,
            "daily_loads": daily_summary,
            "acwr": acwr,
        }


# -------------------------------------------------------------
# 6. Factory / DI
# -------------------------------------------------------------

_training_load_repo_instance = None

def get_training_load_repository() -> TrainingLoadRepository:
    global _training_load_repo_instance
    if _training_load_repo_instance is not None:
        return _training_load_repo_instance
    if db_pool:
        logger.info("FACTORY: get_training_load_repository() -> PostgreSqlTrainingLoadRepository")
        _training_load_repo_instance = PostgreSqlTrainingLoadRepository(db_pool)
    else:
        logger.info("FACTORY: get_training_load_repository() -> MockTrainingLoadRepository")
        _training_load_repo_instance = MockTrainingLoadRepository()
    return _training_load_repo_instance


def set_training_load_repository(repo: TrainingLoadRepository) -> None:
    global _training_load_repo_instance
    _training_load_repo_instance = repo


def reset_training_load_repository() -> None:
    global _training_load_repo_instance
    _training_load_repo_instance = None


def get_training_load_service(
    repo: TrainingLoadRepository = Depends(get_training_load_repository),
) -> TrainingLoadService:
    return TrainingLoadService(repo=repo, event_emitter=event_emitter)


# -------------------------------------------------------------
# 7. API Endpoints
# -------------------------------------------------------------

@router.post(
    "/api/v2/training-load",
    status_code=status.HTTP_201_CREATED,
    summary="Record Training Load Event",
    description="Record a training session with RPE-based internal load and optional external metrics.",
)
async def record_training_load(
    event: TrainingLoadCreate,
    service: TrainingLoadService = Depends(get_training_load_service),
):
    try:
        result = await service.record_load(event)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/api/v2/training-load/{athlete_id}",
    summary="Get Training Load History",
    description="List training load events for an athlete.",
)
async def get_training_load_history(
    athlete_id: int,
    days: int = Query(28, ge=1, le=365),
    service: TrainingLoadService = Depends(get_training_load_service),
):
    result = await service.get_load_history(athlete_id, days)
    return result


@router.get(
    "/api/v2/training-load/{athlete_id}/acwr",
    summary="Get ACWR (Acute:Chronic Workload Ratio)",
    description="Compute the acute:chronic workload ratio for an athlete.",
)
async def get_acwr(
    athlete_id: int,
    on_date: Optional[date] = Query(None, description="Date for ACWR calculation (default: today)"),
    service: TrainingLoadService = Depends(get_training_load_service),
):
    result = await service.get_acwr(athlete_id, on_date)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Insufficient training load data for ACWR calculation",
        )
    return result
