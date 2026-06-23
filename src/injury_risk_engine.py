# Forge Injury Risk Engine (Phase 3)
# Role: Head Sports Scientist
# Description: Multi-factor injury risk assessment combining demand deficits,
# training load, compliance, and assessment trends.
# Explainable — each risk score includes a breakdown of contributing factors.

import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import date, datetime, timedelta

from fastapi import APIRouter, HTTPException, Depends, Query, status
from pydantic import BaseModel, Field

from domain_events import DomainEventEmitter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("forge-injury-risk-engine")

db_pool = None
router = APIRouter()
event_emitter = DomainEventEmitter()

# -------------------------------------------------------------
# 1. Pydantic Models
# -------------------------------------------------------------

class RiskFactor(BaseModel):
    name: str
    contribution: float = Field(..., ge=0, le=100, description="Percentage contribution to total risk")
    description: str
    current_value: Optional[float] = None
    threshold_value: Optional[float] = None

class InjuryRiskProfileCreate(BaseModel):
    athlete_id: int = Field(..., gt=0)
    organization_id: Optional[int] = None
    valid_from: date = Field(default_factory=date.today)

    risk_level: str = Field(default="moderate", pattern=r"^(low|moderate|high|critical)$")
    risk_score: float = Field(..., ge=0, le=100)
    risk_factors: List[RiskFactor] = []
    recommended_interventions: List[str] = []
    score_breakdown: Optional[Dict[str, Any]] = None
    calculation_version: str = "1.0.0"


class InjuryRiskProfileResponse(BaseModel):
    id: int
    athlete_id: int
    risk_level: str
    risk_score: float
    risk_factors: List[Dict[str, Any]] = []
    recommended_interventions: List[str] = []
    score_breakdown: Dict[str, Any] = {}
    calculation_version: str
    valid_from: str
    created_at: str


# -------------------------------------------------------------
# 2. Repository Interface
# -------------------------------------------------------------

class InjuryRiskRepository:
    async def create(self, profile: InjuryRiskProfileCreate) -> Dict[str, Any]:
        raise NotImplementedError()

    async def get_latest(self, athlete_id: int) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    async def list_for_athlete(
        self, athlete_id: int, limit: int = 20, offset: int = 0
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError()


# -------------------------------------------------------------
# 3. Mock Implementation
# -------------------------------------------------------------

class MockInjuryRiskRepository(InjuryRiskRepository):
    def __init__(self):
        self.profiles: Dict[int, Dict[str, Any]] = {}
        self.counter = 1

    async def create(self, profile: InjuryRiskProfileCreate) -> Dict[str, Any]:
        profile_id = self.counter
        self.counter += 1
        record = {
            "id": profile_id,
            "athlete_id": profile.athlete_id,
            "organization_id": profile.organization_id,
            "valid_from": profile.valid_from.isoformat(),
            "valid_until": None,
            "risk_level": profile.risk_level,
            "risk_score": profile.risk_score,
            "risk_factors": [f.model_dump() for f in profile.risk_factors],
            "recommended_interventions": profile.recommended_interventions,
            "score_breakdown": profile.score_breakdown or {},
            "calculation_version": profile.calculation_version,
            "created_at": datetime.utcnow().isoformat(),
        }
        self.profiles[profile_id] = record
        return record

    async def get_latest(self, athlete_id: int) -> Optional[Dict[str, Any]]:
        athlete_profiles = [p for p in self.profiles.values() if p["athlete_id"] == athlete_id]
        if not athlete_profiles:
            return None
        athlete_profiles.sort(key=lambda p: p["valid_from"], reverse=True)
        return athlete_profiles[0]

    async def list_for_athlete(
        self, athlete_id: int, limit: int = 20, offset: int = 0
    ) -> List[Dict[str, Any]]:
        results = [p for p in self.profiles.values() if p["athlete_id"] == athlete_id]
        results.sort(key=lambda p: p["valid_from"], reverse=True)
        return results[offset:offset + limit]


# -------------------------------------------------------------
# 4. PostgreSQL Implementation
# -------------------------------------------------------------

class PostgreSqlInjuryRiskRepository(InjuryRiskRepository):
    def __init__(self, pool=None):
        self.pool = pool

    async def create(self, profile: InjuryRiskProfileCreate) -> Dict[str, Any]:
        if not self.pool:
            return {}
        query = """
            INSERT INTO injury_risk_profiles
                (athlete_id, organization_id, valid_from,
                 risk_level, risk_score, risk_factors,
                 recommended_interventions, score_breakdown, calculation_version)
            VALUES ($1, $2, $3, $4, $5, $6::jsonb, $7::jsonb, $8::jsonb, $9)
            RETURNING id, athlete_id, organization_id, valid_from::text, valid_until,
                      risk_level, risk_score, risk_factors,
                      recommended_interventions, score_breakdown,
                      calculation_version, created_at;
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                profile.athlete_id, profile.organization_id, profile.valid_from,
                profile.risk_level, profile.risk_score,
                json.dumps([f.model_dump() for f in profile.risk_factors]),
                json.dumps(profile.recommended_interventions),
                json.dumps(profile.score_breakdown or {}),
                profile.calculation_version,
            )
            return dict(row) if row else {}

    async def get_latest(self, athlete_id: int) -> Optional[Dict[str, Any]]:
        if not self.pool:
            return None
        query = """
            SELECT id, athlete_id, organization_id, valid_from::text, valid_until,
                   risk_level, risk_score, risk_factors,
                   recommended_interventions, score_breakdown,
                   calculation_version, created_at
            FROM injury_risk_profiles
            WHERE athlete_id = $1 AND (valid_until IS NULL OR valid_until >= CURRENT_DATE)
            ORDER BY valid_from DESC
            LIMIT 1;
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, athlete_id)
            return dict(row) if row else None

    async def list_for_athlete(
        self, athlete_id: int, limit: int = 20, offset: int = 0
    ) -> List[Dict[str, Any]]:
        if not self.pool:
            return []
        query = """
            SELECT id, athlete_id, valid_from::text, valid_until,
                   risk_level, risk_score, calculation_version, created_at
            FROM injury_risk_profiles
            WHERE athlete_id = $1
            ORDER BY valid_from DESC
            LIMIT $2 OFFSET $3;
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, athlete_id, limit, offset)
            return [dict(r) for r in rows]


# -------------------------------------------------------------
# 5. Service Layer
# -------------------------------------------------------------

class InjuryRiskService:
    """Multi-factor injury risk assessment.

    Combines:
    1. Demand deficits (from athlete state snapshots)
    2. Training load (ACWR from training_load_events)
    3. Assessment trends (from state history)
    4. Injury risk demand mapping (from reference data)

    All calculations are explainable — the score_breakdown shows
    exactly what contributed to the final risk score.
    """

    def __init__(
        self,
        risk_repo: InjuryRiskRepository,
        event_emitter: DomainEventEmitter,
    ):
        self._repo = risk_repo
        self._emitter = event_emitter

    async def assess_risk(
        self,
        athlete_id: int,
        demand_scores: Optional[Dict[str, float]] = None,
        acwr: Optional[float] = None,
        load_compliance: Optional[float] = None,
        assessment_trend: Optional[str] = None,
        organization_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Compute an explainable injury risk assessment.

        Each parameter contributes to the overall risk score.
        The breakdown shows the contribution of each factor.
        """
        factors: List[RiskFactor] = []
        breakdown: Dict[str, Any] = {}
        total_weight = 0.0
        weighted_risk = 0.0

        # Factor 1: Demand deficits (40% weight)
        deficit_risk = self._assess_demand_deficits(demand_scores)
        if deficit_risk["score"] is not None:
            weight = 0.40
            weighted_risk += deficit_risk["score"] * weight
            total_weight += weight
            factors.append(RiskFactor(
                name="Demand Deficits",
                contribution=round(deficit_risk["score"] * 100 / 100, 1),
                description="Risk from performance demand deficits",
                current_value=deficit_risk["score"],
                threshold_value=0.2,
            ))
            breakdown["demand_deficits"] = {
                "score": deficit_risk["score"],
                "weight": weight,
                "details": deficit_risk.get("details", {}),
            }

        # Factor 2: ACWR (25% weight)
        acwr_risk = self._assess_acwr(acwr)
        if acwr_risk["score"] is not None:
            weight = 0.25
            weighted_risk += acwr_risk["score"] * weight
            total_weight += weight
            factors.append(RiskFactor(
                name="Training Load (ACWR)",
                contribution=round(acwr_risk["score"] * 100 / 100, 1),
                description="Risk from acute:chronic workload ratio",
                current_value=acwr,
                threshold_value=1.5,
            ))
            breakdown["acwr"] = {
                "score": acwr_risk["score"],
                "weight": weight,
                "details": acwr_risk.get("details", {}),
            }

        # Factor 3: Compliance (20% weight)
        compliance_risk = self._assess_compliance(load_compliance)
        if compliance_risk["score"] is not None:
            weight = 0.20
            weighted_risk += compliance_risk["score"] * weight
            total_weight += weight
            factors.append(RiskFactor(
                name="Load Compliance",
                contribution=round(compliance_risk["score"] * 100 / 100, 1),
                description="Risk from training compliance gaps",
                current_value=load_compliance,
                threshold_value=0.8,
            ))
            breakdown["compliance"] = {
                "score": compliance_risk["score"],
                "weight": weight,
                "details": compliance_risk.get("details", {}),
            }

        # Factor 4: Assessment trend (15% weight)
        trend_risk = self._assess_trend(assessment_trend)
        if trend_risk["score"] is not None:
            weight = 0.15
            weighted_risk += trend_risk["score"] * weight
            total_weight += weight
            factors.append(RiskFactor(
                name="Assessment Trend",
                contribution=round(trend_risk["score"] * 100 / 100, 1),
                description="Risk from declining assessment performance",
                current_value={"declining": 1.0, "stable": 0.5, "improving": 0.0}.get(
                    assessment_trend or "", 0.5
                ),
                threshold_value=0.7,
            ))
            breakdown["assessment_trend"] = {
                "score": trend_risk["score"],
                "weight": weight,
                "details": trend_risk.get("details", {}),
            }

        final_risk = round(weighted_risk / total_weight, 2) if total_weight > 0 else 0.0

        risk_level = self._risk_level_from_score(final_risk)
        interventions = self._generate_interventions(factors, risk_level)

        profile = InjuryRiskProfileCreate(
            athlete_id=athlete_id,
            organization_id=organization_id,
            risk_level=risk_level,
            risk_score=final_risk,
            risk_factors=factors,
            recommended_interventions=interventions,
            score_breakdown=breakdown,
        )

        record = await self._repo.create(profile)

        await self._emitter.emit_injury_risk_updated(
            athlete_id=athlete_id,
            profile_id=record["id"],
            risk_level=risk_level,
            risk_score=final_risk,
            organization_id=organization_id,
            risk_factors=[f.name for f in factors],
        )

        return record

    def _assess_demand_deficits(
        self, demand_scores: Optional[Dict[str, float]]
    ) -> Dict[str, Any]:
        if not demand_scores:
            return {"score": None, "details": {}}
        low_scores = [v for v in demand_scores.values() if v is not None and v < 40]
        details = {
            "total_demands": len(demand_scores),
            "deficient_demands": len(low_scores),
            "deficit_ratio": round(len(low_scores) / max(len(demand_scores), 1), 2),
        }
        deficit_ratio = details["deficit_ratio"]
        score = min(deficit_ratio * 2, 1.0)
        return {"score": score, "details": details}

    def _assess_acwr(self, acwr: Optional[float]) -> Dict[str, Any]:
        if acwr is None:
            return {"score": None, "details": {}}
        details = {"acwr": acwr}
        if acwr < 0.8:
            score = 0.3
            details["zone"] = "low_load"
        elif acwr < 1.0:
            score = 0.1
            details["zone"] = "normal_low"
        elif acwr <= 1.3:
            score = 0.1
            details["zone"] = "optimal"
        elif acwr <= 1.5:
            score = 0.5
            details["zone"] = "elevated"
        else:
            score = 1.0
            details["zone"] = "danger"
        return {"score": score, "details": details}

    def _assess_compliance(self, compliance: Optional[float]) -> Dict[str, Any]:
        if compliance is None:
            return {"score": None, "details": {}}
        details = {"compliance_rate": compliance}
        if compliance >= 0.9:
            score = 0.0
        elif compliance >= 0.8:
            score = 0.2
        elif compliance >= 0.6:
            score = 0.5
        else:
            score = 0.8
        return {"score": score, "details": details}

    def _assess_trend(self, trend: Optional[str]) -> Dict[str, Any]:
        if trend is None:
            return {"score": None, "details": {}}
        details = {"trend": trend}
        score_map = {"declining": 0.7, "stable": 0.3, "improving": 0.1}
        score = score_map.get(trend, 0.3)
        return {"score": score, "details": details}

    def _risk_level_from_score(self, score: float) -> str:
        if score >= 0.7:
            return "critical"
        elif score >= 0.5:
            return "high"
        elif score >= 0.25:
            return "moderate"
        return "low"

    def _generate_interventions(
        self, factors: List[RiskFactor], risk_level: str
    ) -> List[str]:
        interventions = []
        for f in factors:
            if f.name == "Demand Deficits" and f.contribution > 30:
                interventions.append("Address performance demand deficits with targeted strength/power work")
            if f.name == "Training Load (ACWR)" and f.contribution > 30:
                interventions.append("Reduce training load or increase recovery days")
            if f.name == "Load Compliance" and f.contribution > 30:
                interventions.append("Improve training attendance and session completion")
            if f.name == "Assessment Trend":
                interventions.append("Investigate declining assessment scores with sport scientist")

        if risk_level in ("high", "critical"):
            interventions.append("Schedule sports medicine review")
            interventions.append("Implement modified training program with reduced load")

        return list(set(interventions))


# -------------------------------------------------------------
# 6. Factory / DI
# -------------------------------------------------------------

_injury_risk_repo_instance = None

def get_injury_risk_repository() -> InjuryRiskRepository:
    global _injury_risk_repo_instance
    if _injury_risk_repo_instance is not None:
        return _injury_risk_repo_instance
    if db_pool:
        logger.info("FACTORY: get_injury_risk_repository() -> PostgreSqlInjuryRiskRepository")
        _injury_risk_repo_instance = PostgreSqlInjuryRiskRepository(db_pool)
    else:
        logger.info("FACTORY: get_injury_risk_repository() -> MockInjuryRiskRepository")
        _injury_risk_repo_instance = MockInjuryRiskRepository()
    return _injury_risk_repo_instance


def set_injury_risk_repository(repo: InjuryRiskRepository) -> None:
    global _injury_risk_repo_instance
    _injury_risk_repo_instance = repo


def reset_injury_risk_repository() -> None:
    global _injury_risk_repo_instance
    _injury_risk_repo_instance = None


def get_injury_risk_service(
    repo: InjuryRiskRepository = Depends(get_injury_risk_repository),
) -> InjuryRiskService:
    return InjuryRiskService(risk_repo=repo, event_emitter=event_emitter)


# -------------------------------------------------------------
# 7. API Endpoints
# -------------------------------------------------------------

@router.post(
    "/api/v2/injury-risk/assess",
    status_code=status.HTTP_201_CREATED,
    summary="Assess Injury Risk",
    description="Compute multi-factor injury risk assessment with explainable breakdown.",
)
async def assess_injury_risk(
    request: Dict[str, Any],
    service: InjuryRiskService = Depends(get_injury_risk_service),
):
    athlete_id = request.get("athlete_id")
    if not athlete_id:
        raise HTTPException(status_code=400, detail="athlete_id is required")
    try:
        result = await service.assess_risk(
            athlete_id=athlete_id,
            demand_scores=request.get("demand_scores"),
            acwr=request.get("acwr"),
            load_compliance=request.get("load_compliance"),
            assessment_trend=request.get("assessment_trend"),
            organization_id=request.get("organization_id"),
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/api/v2/injury-risk/{athlete_id}/latest",
    summary="Get Latest Injury Risk Profile",
    description="Retrieve the most recent injury risk assessment for an athlete.",
)
async def get_latest_injury_risk(
    athlete_id: int,
    service: InjuryRiskService = Depends(get_injury_risk_service),
):
    result = await service._repo.get_latest(athlete_id)
    if not result:
        raise HTTPException(status_code=404, detail="No risk profile found")
    return result


@router.get(
    "/api/v2/injury-risk/{athlete_id}/history",
    summary="Get Injury Risk History",
    description="List historical risk profiles for an athlete.",
)
async def get_injury_risk_history(
    athlete_id: int,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: InjuryRiskService = Depends(get_injury_risk_service),
):
    items = await service._repo.list_for_athlete(athlete_id, limit, offset)
    return {"items": items, "total": len(items)}
