# Forge Recommendation Observability Module (Phase 2)
# Role: Senior Backend Engineer
# Description: Recommendation logging, coach feedback, and entity relationship management
# for observability, drift analysis, and continuous improvement.

import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, Depends, Query, status
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("forge-recommendation-observability")

db_pool = None

router = APIRouter()

# -------------------------------------------------------------
# 1. Pydantic Models (Schemas)
# -------------------------------------------------------------

class RecommendationLogEntry(BaseModel):
    recommendation_id: str
    athlete_id: Optional[int] = None
    role_id: int
    sport: str
    role_name: str
    development_level: str
    engine_version: str = "2.0.0"
    execution_time_ms: Optional[int] = None
    cached: bool = False
    created_at: Optional[str] = None


class CoachFeedbackCreate(BaseModel):
    recommendation_id: str = Field(..., description="UUID from recommendation_log")
    coach_id: Optional[int] = None
    coach_name: Optional[str] = None
    coach_decision: str = Field(default="approved", pattern=r"^(approved|modified|rejected|overridden)$")
    acceptance_status: str = Field(default="accepted", pattern=r"^(accepted|partially_accepted|rejected)$")
    override_details: Optional[Dict[str, Any]] = None
    rationale: Optional[str] = None
    notes: Optional[str] = None


class CoachFeedbackResponse(BaseModel):
    id: int
    recommendation_id: str
    coach_id: Optional[int] = None
    coach_name: Optional[str] = None
    coach_decision: str
    acceptance_status: str
    override_details: Optional[Dict[str, Any]] = None
    rationale: Optional[str] = None
    notes: Optional[str] = None
    created_at: str


class EntityRelationshipCreate(BaseModel):
    source_type: str = Field(..., max_length=50)
    source_id: int
    relationship_type: str = Field(..., max_length=100)
    target_type: str = Field(..., max_length=50)
    target_id: int
    weight: float = Field(default=1.0, ge=0, le=100)
    metadata: Optional[Dict[str, Any]] = None


class EntityRelationshipResponse(BaseModel):
    id: int
    source_type: str
    source_id: int
    relationship_type: str
    target_type: str
    target_id: int
    weight: float
    metadata: Optional[Dict[str, Any]] = None
    created_at: str


# -------------------------------------------------------------
# 2. Repository Interface
# -------------------------------------------------------------

class RecommendationObservabilityRepository:
    async def log_recommendation(
        self,
        athlete_id: Optional[int],
        role_id: int,
        sport: str,
        role_name: str,
        development_level: str,
        request_params: Dict[str, Any],
        assessment_snapshot: Dict[str, float],
        demand_scores: List[Dict[str, Any]],
        candidate_rankings: List[Dict[str, Any]],
        engine_version: str = "2.0.0",
        execution_time_ms: Optional[int] = None,
        cached: bool = False,
    ) -> Dict[str, Any]:
        raise NotImplementedError()

    async def get_recommendation(self, recommendation_id: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    async def list_recommendations(
        self,
        athlete_id: Optional[int] = None,
        role_id: Optional[int] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError()

    async def create_feedback(self, feedback: CoachFeedbackCreate) -> Dict[str, Any]:
        raise NotImplementedError()

    async def get_feedback_for_recommendation(self, recommendation_id: str) -> List[Dict[str, Any]]:
        raise NotImplementedError()

    async def create_relationship(self, rel: EntityRelationshipCreate) -> Dict[str, Any]:
        raise NotImplementedError()

    async def get_relationships(
        self,
        source_type: Optional[str] = None,
        source_id: Optional[int] = None,
        target_type: Optional[str] = None,
        target_id: Optional[int] = None,
        relationship_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError()

    async def delete_relationship(self, relationship_id: int) -> bool:
        raise NotImplementedError()


# -------------------------------------------------------------
# 3. Mock Implementation
# -------------------------------------------------------------

class MockRecommendationObservabilityRepository(RecommendationObservabilityRepository):
    def __init__(self):
        self.recommendations: Dict[str, Dict[str, Any]] = {}
        self.feedback: List[Dict[str, Any]] = []
        self.relationships: Dict[int, Dict[str, Any]] = {}
        self.rel_counter = 1
        self.feedback_counter = 1

    async def log_recommendation(
        self,
        athlete_id: Optional[int],
        role_id: int,
        sport: str,
        role_name: str,
        development_level: str,
        request_params: Dict[str, Any],
        assessment_snapshot: Dict[str, float],
        demand_scores: List[Dict[str, Any]],
        candidate_rankings: List[Dict[str, Any]],
        engine_version: str = "2.0.0",
        execution_time_ms: Optional[int] = None,
        cached: bool = False,
    ) -> Dict[str, Any]:
        recommendation_id = str(uuid4())
        record = {
            "id": len(self.recommendations) + 1,
            "recommendation_id": recommendation_id,
            "athlete_id": athlete_id,
            "role_id": role_id,
            "sport": sport,
            "role_name": role_name,
            "development_level": development_level,
            "request_params": request_params,
            "assessment_snapshot": assessment_snapshot,
            "demand_scores": demand_scores,
            "candidate_rankings": candidate_rankings,
            "engine_version": engine_version,
            "execution_time_ms": execution_time_ms,
            "cached": cached,
            "created_at": datetime.utcnow().isoformat(),
        }
        self.recommendations[recommendation_id] = record
        record["created_at"] = datetime.utcnow().isoformat()
        logger.info(f"Mock: Logged recommendation {recommendation_id} for role {role_name}")
        return recommendation_id

    async def get_recommendation(self, recommendation_id: str) -> Optional[Dict[str, Any]]:
        return self.recommendations.get(recommendation_id)

    async def list_recommendations(
        self,
        athlete_id: Optional[int] = None,
        role_id: Optional[int] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        results = list(self.recommendations.values())
        if athlete_id is not None:
            results = [r for r in results if r.get("athlete_id") == athlete_id]
        if role_id is not None:
            results = [r for r in results if r.get("role_id") == role_id]
        results.sort(key=lambda r: r["created_at"], reverse=True)
        return results[offset:offset + limit]

    async def create_feedback(self, feedback: CoachFeedbackCreate) -> Dict[str, Any]:
        if feedback.recommendation_id not in self.recommendations:
            raise ValueError(f"Recommendation {feedback.recommendation_id} not found")
        record = {
            "id": self.feedback_counter,
            "recommendation_id": feedback.recommendation_id,
            "coach_id": feedback.coach_id,
            "coach_name": feedback.coach_name,
            "coach_decision": feedback.coach_decision,
            "acceptance_status": feedback.acceptance_status,
            "override_details": feedback.override_details,
            "rationale": feedback.rationale,
            "notes": feedback.notes,
            "created_at": datetime.utcnow().isoformat(),
        }
        self.feedback_counter += 1
        self.feedback.append(record)
        return record

    async def get_feedback_for_recommendation(self, recommendation_id: str) -> List[Dict[str, Any]]:
        return [f for f in self.feedback if f["recommendation_id"] == recommendation_id]

    async def create_relationship(self, rel: EntityRelationshipCreate) -> Dict[str, Any]:
        rel_id = self.rel_counter
        self.rel_counter += 1
        record = {
            "id": rel_id,
            "source_type": rel.source_type,
            "source_id": rel.source_id,
            "relationship_type": rel.relationship_type,
            "target_type": rel.target_type,
            "target_id": rel.target_id,
            "weight": rel.weight,
            "metadata": rel.metadata or {},
            "created_at": datetime.utcnow().isoformat(),
        }
        self.relationships[rel_id] = record
        return record

    async def get_relationships(
        self,
        source_type: Optional[str] = None,
        source_id: Optional[int] = None,
        target_type: Optional[str] = None,
        target_id: Optional[int] = None,
        relationship_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        results = list(self.relationships.values())
        if source_type:
            results = [r for r in results if r["source_type"] == source_type]
        if source_id is not None:
            results = [r for r in results if r["source_id"] == source_id]
        if target_type:
            results = [r for r in results if r["target_type"] == target_type]
        if target_id is not None:
            results = [r for r in results if r["target_id"] == target_id]
        if relationship_type:
            results = [r for r in results if r["relationship_type"] == relationship_type]
        return results

    async def delete_relationship(self, relationship_id: int) -> bool:
        if relationship_id in self.relationships:
            del self.relationships[relationship_id]
            return True
        return False


# -------------------------------------------------------------
# 4. PostgreSQL Implementation
# -------------------------------------------------------------

class PostgreSqlRecommendationObservabilityRepository(RecommendationObservabilityRepository):
    def __init__(self, pool=None):
        self.pool = pool

    async def log_recommendation(
        self,
        athlete_id: Optional[int],
        role_id: int,
        sport: str,
        role_name: str,
        development_level: str,
        request_params: Dict[str, Any],
        assessment_snapshot: Dict[str, float],
        demand_scores: List[Dict[str, Any]],
        candidate_rankings: List[Dict[str, Any]],
        engine_version: str = "2.0.0",
        execution_time_ms: Optional[int] = None,
        cached: bool = False,
    ) -> Dict[str, Any]:
        if not self.pool:
            return {"recommendation_id": "no-pool"}
        query = """
            INSERT INTO recommendation_log
                (athlete_id, role_id, sport, role_name, development_level,
                 request_params, assessment_snapshot, demand_scores, candidate_rankings,
                 engine_version, execution_time_ms, cached)
            VALUES ($1, $2, $3, $4, $5, $6::jsonb, $7::jsonb, $8::jsonb, $9::jsonb, $10, $11, $12)
            RETURNING recommendation_id::text;
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                athlete_id, role_id, sport, role_name, development_level,
                json.dumps(request_params), json.dumps(assessment_snapshot),
                json.dumps(demand_scores), json.dumps(candidate_rankings),
                engine_version, execution_time_ms, cached,
            )
            return {"recommendation_id": row["recommendation_id"]}

    async def get_recommendation(self, recommendation_id: str) -> Optional[Dict[str, Any]]:
        if not self.pool:
            return None
        query = """
            SELECT id, recommendation_id::text, athlete_id, role_id, sport, role_name,
                   development_level, request_params, assessment_snapshot, demand_scores,
                   candidate_rankings, engine_version, execution_time_ms, cached, created_at
            FROM recommendation_log
            WHERE recommendation_id = $1::uuid;
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, recommendation_id)
            return dict(row) if row else None

    async def list_recommendations(
        self,
        athlete_id: Optional[int] = None,
        role_id: Optional[int] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        if not self.pool:
            return []
        conditions = []
        params = []
        param_index = 1
        if athlete_id is not None:
            conditions.append(f"athlete_id = ${param_index}")
            params.append(athlete_id)
            param_index += 1
        if role_id is not None:
            conditions.append(f"role_id = ${param_index}")
            params.append(role_id)
            param_index += 1
        where_clause = " AND ".join(conditions) if conditions else "TRUE"
        query = f"""
            SELECT id, recommendation_id::text, athlete_id, role_id, sport, role_name,
                   development_level, engine_version, execution_time_ms, cached, created_at
            FROM recommendation_log
            WHERE {where_clause}
            ORDER BY created_at DESC
            LIMIT ${param_index} OFFSET ${param_index + 1};
        """
        params.extend([limit, offset])
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *params)
            return [dict(r) for r in rows]

    async def create_feedback(self, feedback: CoachFeedbackCreate) -> Dict[str, Any]:
        if not self.pool:
            return {"id": 0, "recommendation_id": feedback.recommendation_id}
        query = """
            INSERT INTO coach_feedback
                (recommendation_id, coach_id, coach_name, coach_decision,
                 acceptance_status, override_details, rationale, notes)
            VALUES ($1::uuid, $2, $3, $4, $5, $6::jsonb, $7, $8)
            RETURNING id, recommendation_id::text, coach_id, coach_name,
                      coach_decision, acceptance_status, override_details,
                      rationale, notes, created_at;
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                feedback.recommendation_id, feedback.coach_id, feedback.coach_name,
                feedback.coach_decision, feedback.acceptance_status,
                json.dumps(feedback.override_details) if feedback.override_details else None,
                feedback.rationale, feedback.notes,
            )
            return dict(row)

    async def get_feedback_for_recommendation(self, recommendation_id: str) -> List[Dict[str, Any]]:
        if not self.pool:
            return []
        query = """
            SELECT id, recommendation_id::text, coach_id, coach_name,
                   coach_decision, acceptance_status, override_details,
                   rationale, notes, created_at
            FROM coach_feedback
            WHERE recommendation_id = $1::uuid
            ORDER BY created_at DESC;
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, recommendation_id)
            return [dict(r) for r in rows]

    async def create_relationship(self, rel: EntityRelationshipCreate) -> Dict[str, Any]:
        if not self.pool:
            return {"id": 0}
        query = """
            INSERT INTO entity_relationships
                (source_type, source_id, relationship_type, target_type, target_id, weight, metadata)
            VALUES ($1, $2, $3, $4, $5, $6, $7::jsonb)
            ON CONFLICT (source_type, source_id, relationship_type, target_type, target_id)
            DO UPDATE SET weight = EXCLUDED.weight, metadata = EXCLUDED.metadata
            RETURNING id, source_type, source_id, relationship_type, target_type,
                      target_id, weight, metadata, created_at;
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                rel.source_type, rel.source_id, rel.relationship_type,
                rel.target_type, rel.target_id, rel.weight,
                json.dumps(rel.metadata) if rel.metadata else "{}",
            )
            return dict(row)

    async def get_relationships(
        self,
        source_type: Optional[str] = None,
        source_id: Optional[int] = None,
        target_type: Optional[str] = None,
        target_id: Optional[int] = None,
        relationship_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        if not self.pool:
            return []
        conditions = []
        params = []
        param_index = 1
        if source_type:
            conditions.append(f"source_type = ${param_index}")
            params.append(source_type)
            param_index += 1
        if source_id is not None:
            conditions.append(f"source_id = ${param_index}")
            params.append(source_id)
            param_index += 1
        if target_type:
            conditions.append(f"target_type = ${param_index}")
            params.append(target_type)
            param_index += 1
        if target_id is not None:
            conditions.append(f"target_id = ${param_index}")
            params.append(target_id)
            param_index += 1
        if relationship_type:
            conditions.append(f"relationship_type = ${param_index}")
            params.append(relationship_type)
            param_index += 1
        where_clause = " AND ".join(conditions) if conditions else "TRUE"
        query = f"""
            SELECT id, source_type, source_id, relationship_type, target_type,
                   target_id, weight, metadata, created_at
            FROM entity_relationships
            WHERE {where_clause}
            ORDER BY weight DESC;
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *params)
            return [dict(r) for r in rows]

    async def delete_relationship(self, relationship_id: int) -> bool:
        if not self.pool:
            return False
        query = "DELETE FROM entity_relationships WHERE id = $1;"
        async with self.pool.acquire() as conn:
            result = await conn.execute(query, relationship_id)
            return result != "DELETE 0"


# -------------------------------------------------------------
# 5. Factory / DI
# -------------------------------------------------------------

_observability_repo_instance = None

def get_observability_repository() -> RecommendationObservabilityRepository:
    global _observability_repo_instance
    if _observability_repo_instance is not None:
        return _observability_repo_instance
    if db_pool:
        logger.info("FACTORY: get_observability_repository() -> PostgreSqlRecommendationObservabilityRepository")
        _observability_repo_instance = PostgreSqlRecommendationObservabilityRepository(db_pool)
    else:
        logger.info("FACTORY: get_observability_repository() -> MockRecommendationObservabilityRepository")
        _observability_repo_instance = MockRecommendationObservabilityRepository()
    return _observability_repo_instance


def set_observability_repository(repo: RecommendationObservabilityRepository) -> None:
    """Override the observability repo (used for test injection)."""
    global _observability_repo_instance
    _observability_repo_instance = repo


def reset_observability_repository() -> None:
    """Reset the singleton (for test isolation)."""
    global _observability_repo_instance
    _observability_repo_instance = None


# -------------------------------------------------------------
# 6. FastAPI Endpoints
# -------------------------------------------------------------

@router.get(
    "/api/v2/recommendations",
    summary="List V2 Recommendations",
    description="List recommendation log entries with optional filters."
)
async def list_recommendations(
    athlete_id: Optional[int] = Query(None),
    role_id: Optional[int] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    repo: RecommendationObservabilityRepository = Depends(get_observability_repository),
):
    items = await repo.list_recommendations(
        athlete_id=athlete_id,
        role_id=role_id,
        limit=limit,
        offset=offset,
    )
    return {"items": items, "total": len(items)}


@router.get(
    "/api/v2/recommendations/{recommendation_id}",
    summary="Get Recommendation Detail",
    description="Get full recommendation log entry with all snapshots."
)
async def get_recommendation(
    recommendation_id: str,
    repo: RecommendationObservabilityRepository = Depends(get_observability_repository),
):
    entry = await repo.get_recommendation(recommendation_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return entry


@router.post(
    "/api/v2/coach-feedback",
    status_code=status.HTTP_201_CREATED,
    summary="Submit Coach Feedback",
    description="Record coach decision, overrides, and rationale against a recommendation."
)
async def submit_coach_feedback(
    feedback: CoachFeedbackCreate,
    repo: RecommendationObservabilityRepository = Depends(get_observability_repository),
):
    try:
        result = await repo.create_feedback(feedback)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/api/v2/coach-feedback/{recommendation_id}",
    summary="Get Coach Feedback for Recommendation",
    description="Retrieve all coach feedback entries for a given recommendation."
)
async def get_coach_feedback(
    recommendation_id: str,
    repo: RecommendationObservabilityRepository = Depends(get_observability_repository),
):
    items = await repo.get_feedback_for_recommendation(recommendation_id)
    return {"items": items, "total": len(items)}


@router.post(
    "/api/v2/entity-relationships",
    status_code=status.HTTP_201_CREATED,
    summary="Create Entity Relationship",
    description="Create a relationship between two entities (upserts on conflict)."
)
async def create_relationship(
    rel: EntityRelationshipCreate,
    repo: RecommendationObservabilityRepository = Depends(get_observability_repository),
):
    result = await repo.create_relationship(rel)
    return result


@router.get(
    "/api/v2/entity-relationships",
    summary="List Entity Relationships",
    description="Query relationships with optional filters."
)
async def list_relationships(
    source_type: Optional[str] = Query(None),
    source_id: Optional[int] = Query(None),
    target_type: Optional[str] = Query(None),
    target_id: Optional[int] = Query(None),
    relationship_type: Optional[str] = Query(None),
    repo: RecommendationObservabilityRepository = Depends(get_observability_repository),
):
    items = await repo.get_relationships(
        source_type=source_type,
        source_id=source_id,
        target_type=target_type,
        target_id=target_id,
        relationship_type=relationship_type,
    )
    return {"items": items, "total": len(items)}


@router.delete(
    "/api/v2/entity-relationships/{relationship_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Entity Relationship",
)
async def delete_relationship(
    relationship_id: int,
    repo: RecommendationObservabilityRepository = Depends(get_observability_repository),
):
    deleted = await repo.delete_relationship(relationship_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Relationship not found")
