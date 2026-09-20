# Forge Assessment Entry Module
# Role: Principal Sports Scientist
# Description: Production-grade FastAPI service layer, Pydantic validations, 
# and relational database repository layer for recording athlete assessment scores and querying history.

import os
import logging
from typing import List, Dict, Any, Optional
from datetime import date, datetime

from fastapi import FastAPI, HTTPException, Depends, Query, status
from pydantic import BaseModel, Field, field_validator

# Import Athlete mock repository for integrated mock validations
try:
    from athlete_module import _mock_repo as athlete_repo
except ImportError:
    athlete_repo = None

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("forge-assessment-entry")

app = FastAPI(
    title="Forge Assessment Entry Module",
    description="Interface for recording athlete test scores and retrieving historical S&C progressions.",
    version="1.0.0"
)

# Global database connection pool
db_pool = None

@app.on_event("startup")
async def startup_event():
    global db_pool
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        import asyncpg
        try:
            db_pool = await asyncpg.create_pool(db_url)
            logger.info("Successfully connected to PostgreSQL connection pool.")
        except Exception as e:
            logger.error(f"Failed to create PostgreSQL connection pool: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    global db_pool
    if db_pool:
        await db_pool.close()
        logger.info("PostgreSQL connection pool closed.")

# Core S&C Assessment Units lookup for validation
ASSESSMENT_UNITS = {
    1: "cm",      # CMJ
    2: "m",       # Broad Jump
    3: "s",       # 10m Sprint
    4: "s",       # 20m Sprint
    5: "reps",    # Pull Up
    6: "kg",      # Trap Bar Deadlift
    7: "m/s"      # Rotational Med Ball Throw
}

# -------------------------------------------------------------
# 1. Pydantic Models (Schemas)
# -------------------------------------------------------------

class ResultCreate(BaseModel):
    athlete_id: int = Field(..., example=101)
    assessment_id: int = Field(..., example=1)
    score: float = Field(..., gt=0.0, example=38.50)
    unit: str = Field(..., example="cm")
    test_date: date = Field(..., example="2026-06-15")

    @field_validator("test_date")
    @classmethod
    def validate_date(cls, v: date) -> date:
        if v > date.today():
            raise ValueError("Test date cannot be in the future")
        return v


class ResultResponse(ResultCreate):
    id: int
    created_at: datetime

    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat()
        }
    }


# -------------------------------------------------------------
# 2. Repository Interface & Mock / Postgres Implementations
# -------------------------------------------------------------

class AssessmentResultRepository:
    """Interface for Assessment Results database operations."""
    async def record_result(self, result: ResultCreate) -> Dict[str, Any]:
        raise NotImplementedError()

    async def get_by_id(self, result_id: int) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    async def get_history(self, athlete_id: int, assessment_id: Optional[int] = None) -> List[Dict[str, Any]]:
        raise NotImplementedError()

    async def delete_result(self, result_id: int) -> bool:
        raise NotImplementedError()


class MockAssessmentResultRepository(AssessmentResultRepository):
    """Local mock database pre-seeded with S&C history logs."""
    def __init__(self):
        self.results: Dict[int, Dict[str, Any]] = {}
        self.counter = 1
        self.pre_seed()

    def pre_seed(self):
        # Seed historical CMJ scores for Athlete 101 to check progress tracking
        history = [
            (date(2026, 3, 1), 34.50),
            (date(2026, 4, 1), 35.80),
            (date(2026, 5, 1), 37.00),
            (date(2026, 6, 1), 38.50)
        ]
        for dt, score in history:
            res_id = self.counter
            self.counter += 1
            self.results[res_id] = {
                "id": res_id,
                "athlete_id": 101,
                "assessment_id": 1,
                "score": score,
                "unit": "cm",
                "test_date": dt,
                "created_at": datetime.utcnow()
            }

    async def record_result(self, result: ResultCreate) -> Dict[str, Any]:
        # 1. Validate assessment exists
        if result.assessment_id not in ASSESSMENT_UNITS:
            raise ValueError(f"Assessment ID {result.assessment_id} is not supported.")

        # 2. Validate unit matches assessment type
        expected_unit = ASSESSMENT_UNITS[result.assessment_id]
        if result.unit != expected_unit:
            raise ValueError(f"Unit mismatch for assessment ID {result.assessment_id}. Expected '{expected_unit}', got '{result.unit}'.")

        # 3. Validate athlete profile exists (if mock repo is loaded)
        if athlete_repo and not await athlete_repo.get_by_id(result.athlete_id):
            raise ValueError(f"Athlete with ID {result.athlete_id} does not exist.")

        res_id = self.counter
        self.counter += 1
        
        record = {
            "id": res_id,
            "created_at": datetime.utcnow(),
            **result.model_dump()
        }
        self.results[res_id] = record
        return record

    async def get_by_id(self, result_id: int) -> Optional[Dict[str, Any]]:
        return self.results.get(result_id)

    async def get_history(self, athlete_id: int, assessment_id: Optional[int] = None) -> List[Dict[str, Any]]:
        records = [
            r for r in self.results.values() 
            if r["athlete_id"] == athlete_id
        ]
        if assessment_id is not None:
            records = [r for r in records if r["assessment_id"] == assessment_id]
        
        # Sort historically: newest first
        return sorted(records, key=lambda x: x["test_date"], reverse=True)

    async def delete_result(self, result_id: int) -> bool:
        if result_id in self.results:
            del self.results[result_id]
            return True
        return False


class PostgreSqlAssessmentResultRepository(AssessmentResultRepository):
    """PostgreSQL integration for query execution."""
    def __init__(self, pool=None):
        self.pool = pool

    async def record_result(self, result: ResultCreate) -> Dict[str, Any]:
        # Verify assessment type and units relationally
        verify_query = "SELECT metric_unit FROM assessments WHERE id = $1 LIMIT 1;"
        athlete_query = "SELECT id FROM athletes WHERE id = $1 LIMIT 1;"
        
        insert_query = """
            INSERT INTO assessment_results (athlete_id, assessment_id, score, unit, test_date)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id, athlete_id, assessment_id, score, unit, test_date, created_at;
        """
        if not self.pool:
            raise RuntimeError("Database pool not initialized.")

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                # Athlete check
                ath = await conn.fetchrow(athlete_query, result.athlete_id)
                if not ath:
                    raise ValueError(f"Athlete with ID {result.athlete_id} does not exist.")

                # Assessment check
                ass = await conn.fetchrow(verify_query, result.assessment_id)
                if not ass:
                    raise ValueError(f"Assessment ID {result.assessment_id} is not supported.")
                
                expected_unit = ass["metric_unit"]
                if result.unit != expected_unit:
                    raise ValueError(f"Unit mismatch for assessment ID {result.assessment_id}. Expected '{expected_unit}', got '{result.unit}'.")

                row = await conn.fetchrow(
                    insert_query,
                    result.athlete_id,
                    result.assessment_id,
                    result.score,
                    result.unit,
                    result.test_date
                )
                return dict(row) if row else {}

    async def get_by_id(self, result_id: int) -> Optional[Dict[str, Any]]:
        query = """
            SELECT id, athlete_id, assessment_id, score, unit, test_date, created_at
            FROM assessment_results
            WHERE id = $1;
        """
        if not self.pool: return None
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, result_id)
            return dict(row) if row else None

    async def get_history(self, athlete_id: int, assessment_id: Optional[int] = None) -> List[Dict[str, Any]]:
        query = """
            SELECT id, athlete_id, assessment_id, score, unit, test_date, created_at
            FROM assessment_results
            WHERE athlete_id = $1
        """
        params = [athlete_id]
        if assessment_id is not None:
            query += " AND assessment_id = $2"
            params.append(assessment_id)
        
        query += " ORDER BY test_date DESC;"
        
        if not self.pool: return []
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *params)
            return [dict(r) for r in rows]

    async def delete_result(self, result_id: int) -> bool:
        query = "DELETE FROM assessment_results WHERE id = $1;"
        if not self.pool: return False
        async with self.pool.acquire() as conn:
            result = await conn.execute(query, result_id)
            return "DELETE 1" in result


# Shared repository instance for dependency injection
_mock_repo = MockAssessmentResultRepository()

def get_results_repository() -> AssessmentResultRepository:
    if db_pool:
        logger.info("FACTORY: get_results_repository() -> PostgreSqlAssessmentResultRepository")
        return PostgreSqlAssessmentResultRepository(db_pool)
    logger.info("FACTORY: get_results_repository() -> MockAssessmentResultRepository")
    return _mock_repo

# -------------------------------------------------------------
# 3. FastAPI REST Endpoints
# -------------------------------------------------------------

@app.post(
    "/api/v1/assessments/results",
    response_model=ResultResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record Assessment Result",
    description="Validates the athlete and assessment, checks metric units, and records the test score."
)
async def record_result(
    request: ResultCreate,
    repo: AssessmentResultRepository = Depends(get_results_repository)
):
    logger.info(f"Recording assessment result. Athlete: {request.athlete_id}, Test: {request.assessment_id}, Score: {request.score}")
    try:
        record = await repo.record_result(request)
        return record
    except ValueError as e:
        logger.warning(f"Validation failure: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to record result: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal database transaction error."
        )


@app.get(
    "/api/v1/assessments/results/{id}",
    response_model=ResultResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Assessment Result",
    description="Retrieves a single recorded test score by its primary key."
)
async def get_result(
    id: int,
    repo: AssessmentResultRepository = Depends(get_results_repository)
):
    record = await repo.get_by_id(id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assessment result with ID {id} not found."
        )
    return record


@app.delete(
    "/api/v1/assessments/results/{id}",
    status_code=status.HTTP_200_OK,
    summary="Delete Assessment Result",
    description="Permanently deletes the recorded assessment result."
)
async def delete_result(
    id: int,
    repo: AssessmentResultRepository = Depends(get_results_repository)
):
    logger.info(f"Deleting assessment result ID: {id}")
    success = await repo.delete_result(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assessment result with ID {id} not found."
        )
    return {
        "status": "success",
        "message": f"Assessment result with ID {id} deleted successfully."
    }


@app.get(
    "/api/v1/athletes/{athlete_id}/assessments/history",
    response_model=List[ResultResponse],
    status_code=status.HTTP_200_OK,
    summary="Get Athlete Assessment History",
    description="Loads a chronologically sorted list of test score history logs for a specific athlete."
)
async def get_athlete_history(
    athlete_id: int,
    assessment_id: Optional[int] = Query(None, description="Filter history by specific assessment type ID"),
    repo: AssessmentResultRepository = Depends(get_results_repository)
):
    logger.info(f"Loading assessment history profile for athlete: {athlete_id}")
    # Verify athlete exists (if mock repo is loaded)
    if athlete_repo and not await athlete_repo.get_by_id(athlete_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Athlete with ID {athlete_id} does not exist."
        )
        
    history = await repo.get_history(athlete_id, assessment_id=assessment_id)
    return history


@app.get(
    "/health",
    status_code=status.HTTP_200_OK
)
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow()
    }
