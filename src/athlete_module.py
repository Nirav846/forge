# Forge Athlete Module
# Role: Principal Domain Architect
# Description: Production-grade FastAPI service layer, Pydantic schema validation, 
# and relational database repository layer for Athlete profile management.

import os
import logging
from typing import List, Dict, Any, Optional, Literal
from datetime import date, datetime

from fastapi import FastAPI, HTTPException, Depends, Query, status
from pydantic import BaseModel, Field, field_validator

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("forge-athlete-module")

app = FastAPI(
    title="Forge Athlete Module",
    description="Core management system for athlete profiles, sports, and roles.",
    version="1.0.0"
)

# Global database connection pool
db_pool = None

# Centralized role name map for Cricket
ROLE_NAMES = {1: "Fast Bowler", 2: "Spinner", 3: "Batter", 4: "Wicket Keeper", 5: "All Rounder"}

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

# -------------------------------------------------------------
# 1. Pydantic Models (Schemas)
# -------------------------------------------------------------

class AthleteBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100, example="Nirav")
    last_name: str = Field(..., min_length=1, max_length=100, example="Patel")
    date_of_birth: date = Field(..., example="1998-05-20")
    gender: Literal['Male', 'Female', 'Other', 'Prefer Not to Say'] = Field(..., example="Male")
    sport_id: int = Field(..., example=1)
    role_id: int = Field(..., example=1)
    dominant_side: Literal['Left', 'Right', 'Ambidextrous'] = Field(..., example="Right")
    competition_level: Literal['Beginner', 'Intermediate', 'Advanced', 'Elite'] = Field(..., example="Elite")
    training_age_years: int = Field(..., example=8)
    training_age_months: int = Field(..., example=96, ge=0)

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, v: date) -> date:
        if v >= date.today():
            raise ValueError("Date of birth must be in the past")
        return v

    @field_validator("training_age_years")
    @classmethod
    def validate_training_age(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Training age cannot be negative")
        return v


class AthleteCreate(AthleteBase):
    pass


class AthleteUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100, example="Nirav")
    last_name: Optional[str] = Field(None, min_length=1, max_length=100, example="Patel")
    date_of_birth: Optional[date] = Field(None, example="1998-05-20")
    gender: Optional[Literal['Male', 'Female', 'Other', 'Prefer Not to Say']] = Field(None, example="Male")
    sport_id: Optional[int] = Field(None, example=1)
    role_id: Optional[int] = Field(None, example=1)
    dominant_side: Optional[Literal['Left', 'Right', 'Ambidextrous']] = Field(None, example="Right")
    competition_level: Optional[Literal['Beginner', 'Intermediate', 'Advanced', 'Elite']] = Field(None, example="Elite")
    training_age_years: Optional[int] = Field(None, example=9)
    training_age_months: Optional[int] = Field(None, example=108, ge=0)

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, v: Optional[date]) -> Optional[date]:
        if v is not None and v >= date.today():
            raise ValueError("Date of birth must be in the past")
        return v

    @field_validator("training_age_years")
    @classmethod
    def validate_training_age(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v < 0:
            raise ValueError("Training age cannot be negative")
        return v


class AthleteResponse(AthleteBase):
    athlete_id: int = Field(..., alias="id")
    created_at: datetime
    updated_at: datetime

    model_config = {
        "populate_by_name": True,
        "json_encoders": {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat()
        }
    }


# -------------------------------------------------------------
# 2. Repository Interface & Mock / Postgres Implementations
# -------------------------------------------------------------

class AthleteRepository:
    """Interface for Athlete database operations."""
    async def create(self, athlete: AthleteCreate) -> Dict[str, Any]:
        raise NotImplementedError()

    async def get_by_id(self, athlete_id: int) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    async def update(self, athlete_id: int, athlete: AthleteUpdate) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    async def delete(self, athlete_id: int) -> bool:
        raise NotImplementedError()

    async def list_all(self, sport_id: Optional[int] = None, role_id: Optional[int] = None) -> List[Dict[str, Any]]:
        raise NotImplementedError()


class MockAthleteRepository(AthleteRepository):
    """Local mock database for development and testing."""
    def __init__(self):
        self.athletes: Dict[int, Dict[str, Any]] = {}
        self.counter = 1
        
        # Populate initial test record
        self.create_sync(
            AthleteCreate(
                first_name="Nirav",
                last_name="Patel",
                date_of_birth=date(1998, 5, 20),
                gender="Male",
                sport_id=1,
                role_id=1,
                dominant_side="Right",
                competition_level="Elite",
                training_age_years=8,
                training_age_months=96
            )
        )

    def create_sync(self, athlete: AthleteCreate) -> Dict[str, Any]:
        athlete_id = self.counter
        self.counter += 1
        
        now = datetime.utcnow()
        record = {
            "id": athlete_id,
            "created_at": now,
            "updated_at": now,
            **athlete.model_dump()
        }
        self.athletes[athlete_id] = record
        return record

    async def create(self, athlete: AthleteCreate) -> Dict[str, Any]:
        return self.create_sync(athlete)

    async def get_by_id(self, athlete_id: int) -> Optional[Dict[str, Any]]:
        return self.athletes.get(athlete_id)

    async def update(self, athlete_id: int, athlete: AthleteUpdate) -> Optional[Dict[str, Any]]:
        if athlete_id not in self.athletes:
            return None
        
        current = self.athletes[athlete_id]
        update_data = athlete.model_dump(exclude_unset=True)
        
        updated_record = {
            **current,
            **update_data,
            "updated_at": datetime.utcnow()
        }
        self.athletes[athlete_id] = updated_record
        return updated_record

    async def delete(self, athlete_id: int) -> bool:
        if athlete_id in self.athletes:
            del self.athletes[athlete_id]
            return True
        return False

    async def list_all(self, sport_id: Optional[int] = None, role_id: Optional[int] = None) -> List[Dict[str, Any]]:
        results = list(self.athletes.values())
        if sport_id is not None:
            results = [r for r in results if r["sport_id"] == sport_id]
        if role_id is not None:
            results = [r for r in results if r["role_id"] == role_id]
        return sorted(results, key=lambda x: x["id"], reverse=True)


class PostgreSqlAthleteRepository(AthleteRepository):
    """PostgreSQL production execution using asyncpg connection logic."""
    def __init__(self, pool=None):
        self.pool = pool  # asyncpg connection pool

    async def create(self, athlete: AthleteCreate) -> Dict[str, Any]:
        query = """
            INSERT INTO athletes (first_name, last_name, date_of_birth, gender, sport_id, role_id, dominant_side, competition_level, training_age_years)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            RETURNING id, first_name, last_name, date_of_birth, gender, sport_id, role_id, dominant_side, competition_level, training_age_years, created_at, updated_at;
        """
        if not self.pool:
            raise RuntimeError("No active database pool configured.")
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                query,
                athlete.first_name,
                athlete.last_name,
                athlete.date_of_birth,
                athlete.gender,
                athlete.sport_id,
                athlete.role_id,
                athlete.dominant_side,
                athlete.competition_level,
                athlete.training_age_years
            )
            return dict(row) if row else {}

    async def get_by_id(self, athlete_id: int) -> Optional[Dict[str, Any]]:
        query = """
            SELECT id, first_name, last_name, date_of_birth, gender, sport_id, role_id, dominant_side, competition_level, training_age_years, created_at, updated_at
            FROM athletes
            WHERE id = $1;
        """
        if not self.pool:
            return None
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, athlete_id)
            return dict(row) if row else None

    async def update(self, athlete_id: int, athlete: AthleteUpdate) -> Optional[Dict[str, Any]]:
        update_data = athlete.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_by_id(athlete_id)

        set_clauses = []
        values = []
        for i, (k, v) in enumerate(update_data.items(), start=1):
            set_clauses.append(f"{k} = ${i}")
            values.append(v)
        
        athlete_id_index = len(values) + 1
        values.append(athlete_id)

        query = f"""
            UPDATE athletes
            SET {', '.join(set_clauses)}, updated_at = CURRENT_TIMESTAMP
            WHERE id = ${athlete_id_index}
            RETURNING id, first_name, last_name, date_of_birth, gender, sport_id, role_id, dominant_side, competition_level, training_age_years, created_at, updated_at;
        """
        if not self.pool:
            return None
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *values)
            return dict(row) if row else None

    async def delete(self, athlete_id: int) -> bool:
        query = "DELETE FROM athletes WHERE id = $1;"
        if not self.pool:
            return False
        async with self.pool.acquire() as conn:
            result = await conn.execute(query, athlete_id)
            return "DELETE 1" in result

    async def list_all(self, sport_id: Optional[int] = None, role_id: Optional[int] = None) -> List[Dict[str, Any]]:
        query = """
            SELECT id, first_name, last_name, date_of_birth, gender, sport_id, role_id, dominant_side, competition_level, training_age_years, created_at, updated_at
            FROM athletes
            WHERE 1=1
        """
        params = []
        param_index = 1
        if sport_id is not None:
            query += f" AND sport_id = ${param_index}"
            params.append(sport_id)
            param_index += 1
        if role_id is not None:
            query += f" AND role_id = ${param_index}"
            params.append(role_id)
            param_index += 1
        
        query += " ORDER BY id DESC;"

        if not self.pool:
            return []
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *params)
            return [dict(r) for r in rows]


# Shared instance for DI
_mock_repo = MockAthleteRepository()

def get_athlete_repository() -> AthleteRepository:
    if db_pool:
        logger.info("FACTORY: get_athlete_repository() -> PostgreSqlAthleteRepository")
        return PostgreSqlAthleteRepository(db_pool)
    logger.info("FACTORY: get_athlete_repository() -> MockAthleteRepository")
    return _mock_repo

# -------------------------------------------------------------
# 3. FastAPI REST Endpoints
# -------------------------------------------------------------

@app.post(
    "/api/v1/athletes",
    response_model=AthleteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Athlete Profile",
    description="Validates inputs and saves a new athlete profile to the database."
)
async def create_athlete(
    request: AthleteCreate,
    repo: AthleteRepository = Depends(get_athlete_repository)
):
    logger.info(f"Creating profile for: {request.first_name} {request.last_name}")
    try:
        athlete = await repo.create(request)
        return athlete
    except Exception as e:
        logger.error(f"Error creating athlete: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create profile. Error: {str(e)}"
        )


@app.get(
    "/api/v1/athletes/{id}",
    response_model=AthleteResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Athlete Profile",
    description="Loads a single athlete profile by its primary identifier."
)
async def get_athlete(
    id: int,
    repo: AthleteRepository = Depends(get_athlete_repository)
):
    athlete = await repo.get_by_id(id)
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Athlete with ID {id} not found."
        )
    return athlete


@app.put(
    "/api/v1/athletes/{id}",
    response_model=AthleteResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Athlete Profile",
    description="Updates one or more fields on the athlete's profile."
)
async def update_athlete(
    id: int,
    request: AthleteUpdate,
    repo: AthleteRepository = Depends(get_athlete_repository)
):
    logger.info(f"Updating profile for athlete ID: {id}")
    athlete = await repo.update(id, request)
    if not athlete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Athlete with ID {id} not found."
        )
    return athlete


@app.delete(
    "/api/v1/athletes/{id}",
    status_code=status.HTTP_200_OK,
    summary="Delete Athlete Profile",
    description="Permanently deletes the athlete profile from the database."
)
async def delete_athlete(
    id: int,
    repo: AthleteRepository = Depends(get_athlete_repository)
):
    logger.info(f"Deleting profile for athlete ID: {id}")
    success = await repo.delete(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Athlete with ID {id} not found."
        )
    return {
        "status": "success",
        "message": f"Athlete profile with ID {id} deleted successfully."
    }


@app.get(
    "/api/v1/athletes",
    response_model=List[AthleteResponse],
    status_code=status.HTTP_200_OK,
    summary="List Athlete Profiles",
    description="Lists all athlete profiles with optional filtration by sport or role."
)
async def list_athletes(
    sport_id: Optional[int] = Query(None, description="Filter by Sport ID"),
    role_id: Optional[int] = Query(None, description="Filter by Role ID"),
    repo: AthleteRepository = Depends(get_athlete_repository)
):
    return await repo.list_all(sport_id=sport_id, role_id=role_id)


@app.get(
    "/health",
    status_code=status.HTTP_200_OK
)
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow()
    }
