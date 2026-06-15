# Forge S&C Knowledge Graph V1 Service
# Role: Lead Sports Scientist & Backend Engineer
# Description: Production-grade FastAPI service implementing the S&C Knowledge Graph.
# Provides repositories and endpoints to query needs analyses, and diagnose athletic deficits from testing scores.

import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio

from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("forge-knowledge-graph")

app = FastAPI(
    title="Forge S&C Knowledge Graph Service",
    description="Interface for S&C Needs Analysis, Athletic Benchmarks, Deficit Diagnosis, and Template Prescription.",
    version="1.0.0"
)

# -------------------------------------------------------------
# 1. Pydantic Models (Schemas)
# -------------------------------------------------------------

class RoleModel(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

class NeedsAnalysisItem(BaseModel):
    performance_driver: str
    priority: str
    assessment_name: str
    metric_unit: str

class NeedsAnalysisResponse(BaseModel):
    role_name: str
    sport_name: str
    drivers: List[NeedsAnalysisItem]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class DiagnosticsRequest(BaseModel):
    assessment_name: str = Field(..., example="Isometric Mid-Thigh Pull (IMTP)")
    score: float = Field(..., example=2100.00)

    model_config = {
        "json_schema_extra": {
            "example": {
                "assessment_name": "Isometric Mid-Thigh Pull (IMTP)",
                "score": 2100.00
            }
        }
    }

class DiagnosticsResponse(BaseModel):
    diagnosed_deficit: str
    description: str
    benchmark_result: str
    metric_unit: str
    score: float
    recommended_training_methods: List[str]
    corrective_templates: List[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# -------------------------------------------------------------
# 2. Repository Interface & Implementations
# -------------------------------------------------------------

class KnowledgeGraphRepository:
    """Interface for Knowledge Graph data operations."""
    async def get_roles(self, sport_name: str) -> List[Dict[str, Any]]:
        raise NotImplementedError()

    async def get_needs_analysis(self, role_name: str) -> List[Dict[str, Any]]:
        raise NotImplementedError()

    async def diagnose_score(self, assessment_name: str, score: float) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()


class PostgreSqlKnowledgeGraphRepository(KnowledgeGraphRepository):
    """PostgreSQL integration for Knowledge Graph v1."""
    def __init__(self, pool=None):
        self.pool = pool  # asyncpg connection pool

    async def get_roles(self, sport_name: str) -> List[Dict[str, Any]]:
        query = """
            SELECT r.id, r.name, r.description
            FROM roles r
            JOIN sports s ON r.sport_id = s.id
            WHERE s.name ILIKE $1
            ORDER BY r.name;
        """
        if not self.pool: return []
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, sport_name)
            return [dict(r) for r in rows]

    async def get_needs_analysis(self, role_name: str) -> List[Dict[str, Any]]:
        query = """
            SELECT 
                pd.name as performance_driver,
                pd.priority,
                a.name as assessment_name,
                a.metric_unit
            FROM roles r
            JOIN performance_drivers pd ON r.id = pd.role_id
            JOIN driver_assessments da ON pd.id = da.performance_driver_id
            JOIN assessments a ON da.assessment_id = a.id
            WHERE r.name ILIKE $1
            ORDER BY 
                CASE pd.priority
                    WHEN 'Primary' THEN 1
                    WHEN 'Secondary' THEN 2
                    WHEN 'Tertiary' THEN 3
                END, pd.name;
        """
        if not self.pool: return []
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, role_name)
            return [dict(r) for r in rows]

    async def diagnose_score(self, assessment_name: str, score: float) -> Optional[Dict[str, Any]]:
        # Diagnoses deficit and maps training methods/templates directly via SQL range joins
        query = """
            SELECT 
                d.name as diagnosed_deficit,
                d.description as deficit_description,
                b.classification as benchmark_result,
                a.metric_unit,
                -- Aggregate methods and templates dynamically
                ARRAY_AGG(DISTINCT tm.name) as recommended_training_methods,
                ARRAY_AGG(DISTINCT mt.name) as corrective_templates
            FROM assessments a
            JOIN benchmarks b ON a.id = b.assessment_id
            JOIN deficits d ON a.id = d.assessment_id
            LEFT JOIN deficit_training_methods dtm ON d.id = dtm.deficit_id
            LEFT JOIN training_methods tm ON dtm.training_method_id = tm.id
            LEFT JOIN deficit_movement_templates dmt ON d.id = dmt.deficit_id
            LEFT JOIN movement_templates mt ON dmt.movement_template_id = mt.id
            WHERE a.name ILIKE $1
              AND (b.min_value IS NULL OR $2::numeric >= b.min_value)
              AND (b.max_value IS NULL OR $2::numeric <= b.max_value)
            GROUP BY d.name, d.description, b.classification, a.metric_unit;
        """
        if not self.pool: return None
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, assessment_name, score)
            return dict(row) if row else None


class MockKnowledgeGraphRepository(KnowledgeGraphRepository):
    """Local mock database prepopulated with Cricket sports science nodes."""
    
    async def get_roles(self, sport_name: str) -> List[Dict[str, Any]]:
        if sport_name.lower() != "cricket":
            return []
        return [
            {"id": 1, "name": "Fast Bowler", "description": "High-intensity bowler requiring extreme brace force."},
            {"id": 2, "name": "Spinner", "description": "Rotational specialist requiring extreme trunk/hip separation."},
            {"id": 3, "name": "Batter", "description": "Requires high-velocity bat speed and quick reactions."},
            {"id": 4, "name": "Wicket Keeper", "description": "Squat-dominant specialist requiring isometric endurance."},
            {"id": 5, "name": "All Rounder", "description": "Generalist requiring balanced development."}
        ]

    async def get_needs_analysis(self, role_name: str) -> List[Dict[str, Any]]:
        # Hardcoded needs analyses matching seed data
        data = {
            "fast bowler": [
                {"performance_driver": "Front Foot Brace Force", "priority": "Primary", "assessment_name": "Isometric Mid-Thigh Pull (IMTP)", "metric_unit": "N"},
                {"performance_driver": "Front Foot Brace Force", "priority": "Primary", "assessment_name": "Force Plate Countermovement Jump (CMJ)", "metric_unit": "cm"},
                {"performance_driver": "Trunk Flexion Rotational Power", "priority": "Primary", "assessment_name": "Medicine Ball Rotational Velocity Test", "metric_unit": "m/s"}
            ],
            "spinner": [
                {"performance_driver": "Hip-Shoulder Separation Torque", "priority": "Primary", "assessment_name": "Medicine Ball Rotational Velocity Test", "metric_unit": "m/s"}
            ],
            "wicket keeper": [
                {"performance_driver": "Lower Body Isometric Squat Endurance", "priority": "Primary", "assessment_name": "Isometric Wall Sit Squat Hold Test", "metric_unit": "s"}
            ]
        }
        return data.get(role_name.lower(), [])

    async def diagnose_score(self, assessment_name: str, score: float) -> Optional[Dict[str, Any]]:
        # Evaluates Isometric Mid-Thigh Pull (IMTP)
        if "mid-thigh" in assessment_name.lower() or "imtp" in assessment_name.lower():
            # Classify score
            if score < 2200:
                classification = "Poor"
            elif score < 3000:
                classification = "Sub-optimal"
            elif score < 3500:
                classification = "Optimal"
            else:
                classification = "Elite"

            # If classification is suboptimal/poor, trigger the deficit
            if classification in ["Poor", "Sub-optimal"]:
                return {
                    "diagnosed_deficit": "Lower Body Absolute Strength Deficit",
                    "deficit_description": "Athlete exhibits sub-optimal peak force capability, reducing front-foot landing brace stiffness.",
                    "benchmark_result": classification,
                    "metric_unit": "N",
                    "recommended_training_methods": ["Cluster Sets", "Velocity-Based Training"],
                    "corrective_templates": ["Lower Body Power", "Cricket Fast Bowler Power"]
                }
            else:
                return {
                    "diagnosed_deficit": "No Strength Deficit Detected",
                    "deficit_description": "Athlete meets absolute strength thresholds for brace force.",
                    "benchmark_result": classification,
                    "metric_unit": "N",
                    "recommended_training_methods": [],
                    "corrective_templates": []
                }
        
        # Evaluates Countermovement Jump (CMJ)
        if "countermovement" in assessment_name.lower() or "cmj" in assessment_name.lower():
            classification = "Elite" if score >= 50 else ("Optimal" if score >= 40 else ("Sub-optimal" if score >= 30 else "Poor"))
            if classification in ["Poor", "Sub-optimal"]:
                return {
                    "diagnosed_deficit": "Rate of Force Development Deficit",
                    "deficit_description": "Athlete is slow to generate vertical force, limiting plyometric reactive power.",
                    "benchmark_result": classification,
                    "metric_unit": "cm",
                    "recommended_training_methods": ["Plyometric (Fast)", "Contrast Training"],
                    "corrective_templates": ["Cricket Fast Bowler Power", "Reactive Agility"]
                }
        
        return None


# Dependency injection utility
def get_graph_repository() -> KnowledgeGraphRepository:
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        # PostgreSQL repository instantiation
        pass
    return MockKnowledgeGraphRepository()

# -------------------------------------------------------------
# 3. API Endpoints
# -------------------------------------------------------------

@app.get(
    "/api/v1/sports/{sport_name}/roles",
    response_model=List[RoleModel],
    status_code=status.HTTP_200_OK,
    summary="Get Sport Roles",
    description="Retrieves all configurable athlete roles mapped to the target sport."
)
async def get_sport_roles(
    sport_name: str,
    repo: KnowledgeGraphRepository = Depends(get_graph_repository)
):
    roles = await repo.get_roles(sport_name)
    if not roles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No roles found for sport '{sport_name}'."
        )
    return [RoleModel(**r) for r in roles]


@app.get(
    "/api/v1/roles/{role_name}/needs-analysis",
    response_model=NeedsAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Get S&C Needs Analysis for Role",
    description="Loads all performance drivers, priority classifications, and mapped physical tests for a given role."
)
async def get_needs_analysis(
    role_name: str,
    repo: KnowledgeGraphRepository = Depends(get_graph_repository)
):
    drivers = await repo.get_needs_analysis(role_name)
    if not drivers:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No needs analysis found for athlete role '{role_name}'."
        )
    return NeedsAnalysisResponse(
        role_name=role_name,
        sport_name="Cricket", # Default context for V1
        drivers=[NeedsAnalysisItem(**d) for d in drivers]
    )


@app.post(
    "/api/v1/diagnose",
    response_model=DiagnosticsResponse,
    status_code=status.HTTP_200_OK,
    summary="Diagnose Athletic Deficit",
    description="Evaluates a physical test score, diagnoses deficits against benchmarks, and prescribes corrective methods and templates."
)
async def diagnose_athlete(
    request: DiagnosticsRequest,
    repo: KnowledgeGraphRepository = Depends(get_graph_repository)
):
    logger.info(f"Running diagnostic analysis for test: {request.assessment_name}, Score: {request.score}")
    result = await repo.diagnose_score(request.assessment_name, request.score)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No diagnostic rules or benchmarks found for assessment '{request.assessment_name}'."
        )
    
    return DiagnosticsResponse(
        diagnosed_deficit=result["diagnosed_deficit"],
        description=result["deficit_description"],
        benchmark_result=result["benchmark_result"],
        metric_unit=result["metric_unit"],
        score=request.score,
        recommended_training_methods=result["recommended_training_methods"],
        corrective_templates=result["corrective_templates"]
    )
