# Forge Demand Lifecycle Engine (Phase 5)
# Role: Principal Software Architect
# Description: Multi-factor demand state computation.
# Demand priority considers: Assessment deficit, Role weighting, Injury risk,
# Training history, Recovery state. No single-factor decisions.

import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Query, status
from pydantic import BaseModel, Field

from domain_events import DomainEventEmitter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("forge-demand-lifecycle-engine")

db_pool = None
router = APIRouter()
event_emitter = DomainEventEmitter()

# -------------------------------------------------------------
# 1. Pydantic Models
# -------------------------------------------------------------

class DemandStateRequest(BaseModel):
    athlete_id: int = Field(..., gt=0)
    organization_id: Optional[int] = None
    role_id: Optional[int] = None
    demand_deficits: Optional[Dict[str, float]] = None
    role_priorities: Optional[Dict[str, int]] = None
    injury_risk_score: Optional[float] = Field(None, ge=0, le=100)
    acwr: Optional[float] = None
    recovery_score: Optional[float] = Field(None, ge=0, le=100)
    fatigue_score: Optional[float] = Field(None, ge=0, le=100)
    historical_scores: Optional[List[Dict[str, Any]]] = None


class DemandScoreInfo(BaseModel):
    demand_name: str
    demand_score: float = Field(..., ge=0, le=100)
    trend_score: float = Field(..., ge=-100, le=100, description="Positive = improving")
    priority_score: float = Field(..., ge=0, le=100)
    risk_adjusted_score: float = Field(..., ge=0, le=100)
    components: Dict[str, float]


class DemandStateResponse(BaseModel):
    athlete_id: int
    demands: List[DemandScoreInfo]
    total_demands: int
    calculation_version: str = "1.0.0"


# -------------------------------------------------------------
# 2. Service Layer
# -------------------------------------------------------------

class DemandStateService:
    """Computes multi-factor demand states.

    Formula:
      demand_score = base_score × role_multiplier × risk_adjustment × recovery_adjustment

    Where:
      base_score = 100 - (deficit_severity × 100)  — the higher the deficit, the lower the score
      role_multiplier = priority / 100              — role importance (1.0 for top priority)
      risk_adjustment = 1 - (injury_risk / 100)     — high risk reduces effective capacity
      recovery_adjustment = recovery / 100          — low recovery reduces effective capacity

    All adjustments are transparent and logged in the components dict.
    """

    def __init__(self, event_emitter: DomainEventEmitter):
        self._emitter = event_emitter

    async def compute_demand_states(
        self, request: DemandStateRequest
    ) -> DemandStateResponse:
        if not request.demand_deficits:
            raise ValueError("demand_deficits is required")

        demands = []
        for demand_name, deficit_severity in request.demand_deficits.items():
            score = self._compute_single_demand(
                demand_name=demand_name,
                deficit_severity=deficit_severity,
                role_priority=request.role_priorities.get(demand_name) if request.role_priorities else None,
                injury_risk_score=request.injury_risk_score,
                acwr=request.acwr,
                recovery_score=request.recovery_score,
                fatigue_score=request.fatigue_score,
                historical_scores=request.historical_scores,
            )
            demands.append(score)

        demands.sort(key=lambda d: d.risk_adjusted_score, reverse=True)

        response = DemandStateResponse(
            athlete_id=request.athlete_id,
            demands=demands,
            total_demands=len(demands),
        )

        for d in demands:
            await self._emitter.emit_demand_score_calculated(
                athlete_id=request.athlete_id,
                demand_id=hash(d.demand_name) % 10000,
                demand_score=d.demand_score,
                trend_score=d.trend_score,
                priority_score=d.priority_score,
                organization_id=request.organization_id,
                demand_name=d.demand_name,
            )

        return response

    def _compute_trend(
        self,
        demand_name: str,
        historical_scores: Optional[List[Dict[str, Any]]],
    ) -> float:
        """Compute trend from historical scores.
        Returns a value from -100 (declining fast) to +100 (improving fast).
        """
        if not historical_scores or len(historical_scores) < 2:
            return 0.0

        scores = []
        for h in historical_scores:
            if isinstance(h.get(demand_name), (int, float)):
                scores.append(h[demand_name])

        if len(scores) < 2:
            return 0.0

        first_avg = sum(scores[:len(scores)//2]) / (len(scores)//2)
        last_avg = sum(scores[len(scores)//2:]) / (len(scores) - len(scores)//2)

        diff = last_avg - first_avg
        max_change = 100.0
        trend = (diff / max_change) * 100
        return round(max(-100, min(100, trend)), 2)

    def _compute_single_demand(
        self,
        demand_name: str,
        deficit_severity: float,
        role_priority: Optional[int] = None,
        injury_risk_score: Optional[float] = None,
        acwr: Optional[float] = None,
        recovery_score: Optional[float] = None,
        fatigue_score: Optional[float] = None,
        historical_scores: Optional[List[Dict[str, Any]]] = None,
    ) -> DemandScoreInfo:
        components: Dict[str, float] = {}

        # 1. Base score from deficit (inverted: lower deficit = higher score)
        deficit_normalized = max(0, min(1, deficit_severity))
        base_score = 100.0 - (deficit_normalized * 100.0)
        components["deficit_score"] = round(base_score, 2)

        # 2. Role priority multiplier
        role_multiplier = (role_priority / 100.0) if role_priority else 0.5
        components["role_multiplier"] = round(role_multiplier, 2)

        # 3. Injury risk adjustment
        injury_adj = 1.0
        if injury_risk_score is not None:
            injury_adj = 1.0 - (injury_risk_score / 100.0)
            injury_adj = max(0.1, min(1.0, injury_adj))
        components["injury_risk_adjustment"] = round(injury_adj, 2)

        # 4. ACWR adjustment
        acwr_adj = 1.0
        if acwr is not None:
            if acwr < 0.8 or acwr > 1.5:
                acwr_adj = 0.8
            elif acwr < 1.0 or acwr > 1.3:
                acwr_adj = 0.9
            else:
                acwr_adj = 1.0
        components["acwr_adjustment"] = round(acwr_adj, 2)

        # 5. Recovery adjustment
        recovery_adj = 1.0
        if recovery_score is not None:
            recovery_adj = recovery_score / 100.0
            recovery_adj = max(0.1, min(1.0, recovery_adj))
        components["recovery_adjustment"] = round(recovery_adj, 2)

        # 6. Fatigue adjustment
        fatigue_adj = 1.0
        if fatigue_score is not None:
            fatigue_adj = 1.0 - (fatigue_score / 200.0)
            fatigue_adj = max(0.5, min(1.0, fatigue_adj))
        components["fatigue_adjustment"] = round(fatigue_adj, 2)

        # 7. Combined demand score (multiplicative factors)
        demand_score = round(base_score * role_multiplier, 2)
        components["raw_demand_score"] = demand_score

        # 8. Risk-adjusted score (all adjustments applied)
        risk_adjusted = round(
            demand_score * injury_adj * acwr_adj * recovery_adj * fatigue_adj,
            2,
        )
        components["risk_adjusted_score"] = risk_adjusted

        # 9. Trend score
        trend_score = self._compute_trend(demand_name, historical_scores)
        components["trend_score"] = trend_score

        # 10. Priority score (inverse of risk-adjusted: lower capacity = higher priority)
        priority_score = round(100.0 - risk_adjusted, 2)
        components["priority_score"] = priority_score

        return DemandScoreInfo(
            demand_name=demand_name,
            demand_score=demand_score,
            trend_score=trend_score,
            priority_score=priority_score,
            risk_adjusted_score=risk_adjusted,
            components=components,
        )


# -------------------------------------------------------------
# 3. Factory / DI
# -------------------------------------------------------------

def get_demand_state_service() -> DemandStateService:
    return DemandStateService(event_emitter=event_emitter)


# -------------------------------------------------------------
# 4. API Endpoints
# -------------------------------------------------------------

@router.post(
    "/api/v2/demand-states/compute",
    summary="Compute Multi-Factor Demand States",
    description="Compute demand states considering deficits, role, injury risk, load, and recovery.",
)
async def compute_demand_states(
    request: DemandStateRequest,
    service: DemandStateService = Depends(get_demand_state_service),
):
    try:
        result = await service.compute_demand_states(request)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
