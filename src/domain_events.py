# Forge Domain Events Emitter
# Role: Staff Backend Engineer
# Description: Consistent event sourcing utility for all services.
# Every state mutation emits a domain event for audit, AI training, and replay.

import json
import logging
from typing import Any, Dict, Optional
from datetime import datetime, timezone

logger = logging.getLogger("forge-domain-events")


class DomainEventEmitter:
    """Event emitter that writes to the domain_events table or falls back to logging.

    In production, writes to the PostgreSQL domain_events table.
    In test/development, logs the event if no database pool is available.
    This ensures every service CAN emit events without depending on database availability,
    and events are NEVER lost silently.
    """

    def __init__(self, db_pool=None):
        self._pool = db_pool

    def set_pool(self, pool) -> None:
        self._pool = pool

    async def emit(
        self,
        aggregate_type: str,
        aggregate_id: int,
        event_type: str,
        event_data: Dict[str, Any],
        organization_id: Optional[int] = None,
    ) -> Optional[Dict[str, Any]]:
        """Emit a domain event. Returns the event record if stored, None if only logged."""
        now = datetime.now(timezone.utc)

        if self._pool:
            try:
                query = """
                    INSERT INTO domain_events
                        (aggregate_type, aggregate_id, event_type, event_data, occurred_at, organization_id)
                    VALUES ($1, $2, $3, $4::jsonb, $5, $6)
                    RETURNING id, aggregate_type, aggregate_id, event_type, event_data, occurred_at, organization_id;
                """
                async with self._pool.acquire() as conn:
                    row = await conn.fetchrow(
                        query,
                        aggregate_type,
                        aggregate_id,
                        event_type,
                        json.dumps(event_data),
                        now,
                        organization_id,
                    )
                    logger.info(
                        "Event emitted: %s/%s (%s) — id=%s",
                        aggregate_type, aggregate_id, event_type, row["id"],
                    )
                    return dict(row)
            except Exception as e:
                logger.warning("Failed to store domain event %s/%s: %s", aggregate_type, event_type, e)

        logger.info(
            "[EVENT] %s/%s %s — data=%s",
            aggregate_type, aggregate_id, event_type,
            json.dumps(event_data, default=str)[:200],
        )
        return None

    async def emit_athlete_state_calculated(
        self,
        athlete_id: int,
        snapshot_id: int,
        readiness_score: float,
        organization_id: Optional[int] = None,
        **extra,
    ) -> Optional[Dict[str, Any]]:
        return await self.emit(
            aggregate_type="athlete_state",
            aggregate_id=athlete_id,
            event_type="AthleteStateCalculated",
            event_data={
                "snapshot_id": snapshot_id,
                "readiness_score": readiness_score,
                **extra,
            },
            organization_id=organization_id,
        )

    async def emit_training_load_recorded(
        self,
        athlete_id: int,
        load_event_id: int,
        load_score: float,
        session_type: str,
        organization_id: Optional[int] = None,
        **extra,
    ) -> Optional[Dict[str, Any]]:
        return await self.emit(
            aggregate_type="training_load",
            aggregate_id=athlete_id,
            event_type="TrainingLoadRecorded",
            event_data={
                "load_event_id": load_event_id,
                "load_score": load_score,
                "session_type": session_type,
                **extra,
            },
            organization_id=organization_id,
        )

    async def emit_acwr_calculated(
        self,
        athlete_id: int,
        acwr: float,
        acute_load: float,
        chronic_load: float,
        organization_id: Optional[int] = None,
        **extra,
    ) -> Optional[Dict[str, Any]]:
        return await self.emit(
            aggregate_type="training_load",
            aggregate_id=athlete_id,
            event_type="ACWRCalculated",
            event_data={
                "acwr": acwr,
                "acute_7_day_load": acute_load,
                "chronic_28_day_load": chronic_load,
                **extra,
            },
            organization_id=organization_id,
        )

    async def emit_injury_risk_updated(
        self,
        athlete_id: int,
        profile_id: int,
        risk_level: str,
        risk_score: float,
        organization_id: Optional[int] = None,
        **extra,
    ) -> Optional[Dict[str, Any]]:
        return await self.emit(
            aggregate_type="injury_risk",
            aggregate_id=athlete_id,
            event_type="InjuryRiskUpdated",
            event_data={
                "profile_id": profile_id,
                "risk_level": risk_level,
                "risk_score": risk_score,
                **extra,
            },
            organization_id=organization_id,
        )

    async def emit_demand_score_calculated(
        self,
        athlete_id: int,
        demand_id: int,
        demand_score: float,
        trend_score: float,
        priority_score: float,
        organization_id: Optional[int] = None,
        **extra,
    ) -> Optional[Dict[str, Any]]:
        return await self.emit(
            aggregate_type="demand_score",
            aggregate_id=demand_id,
            event_type="DemandScoreCalculated",
            event_data={
                "athlete_id": athlete_id,
                "demand_score": demand_score,
                "trend_score": trend_score,
                "priority_score": priority_score,
                **extra,
            },
            organization_id=organization_id,
        )

    async def emit_assessment_metrics_extracted(
        self,
        athlete_id: int,
        assessment_id: int,
        metrics: Dict[str, Any],
        organization_id: Optional[int] = None,
        **extra,
    ) -> Optional[Dict[str, Any]]:
        return await self.emit(
            aggregate_type="metric",
            aggregate_id=assessment_id,
            event_type="AssessmentMetricsExtracted",
            event_data={
                "athlete_id": athlete_id,
                "metrics": metrics,
                **extra,
            },
            organization_id=organization_id,
        )
