# Forge Demand Scoring Engine (V2)
# Role: Senior Backend Engineer
# Description: Performance Demand Architecture — replaces V1 template-driven routing
# with direct demand-to-exercise scoring. Runs alongside V1 via ENGINE_MODE feature flag.

import os
import json
import logging
import hashlib
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import asyncio

from fastapi import FastAPI, HTTPException, Depends, Query, status
from pydantic import BaseModel, Field

from exercise_classification import classify_exercise, determine_primary_adaptation, determine_force_vector
from recommendation_observability import (
    RecommendationObservabilityRepository,
    get_observability_repository,
    router as observability_router,
)
from athlete_state_engine import router as athlete_state_router
from training_load_engine import router as training_load_router
from injury_risk_engine import router as injury_risk_router
from demand_lifecycle_engine import router as demand_lifecycle_router
from domain_events import DomainEventEmitter

# Development level constants and helpers
LEVEL_ORDINAL = {"FOUNDATION": 1, "DEVELOPMENT": 2, "PERFORMANCE": 3}
TECH_DIFF_CAP = {"FOUNDATION": 3, "DEVELOPMENT": 6, "PERFORMANCE": 10}

def training_months_to_level(months: int) -> str:
    if months >= 36:
        return "PERFORMANCE"
    elif months >= 12:
        return "DEVELOPMENT"
    return "FOUNDATION"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("forge-demand-scoring-engine")

db_pool = None

app = FastAPI(
    title="Forge Demand Scoring Engine (V2)",
    description="Performance Demand-based exercise recommendation engine. Replaces V1 template routing.",
    version="2.0.0"
)
app.include_router(observability_router)
app.include_router(athlete_state_router)
app.include_router(training_load_router)
app.include_router(injury_risk_router)
app.include_router(demand_lifecycle_router)

@app.on_event("startup")
async def startup_event():
    global db_pool
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        import asyncpg
        try:
            db_pool = await asyncpg.create_pool(db_url)
            logger.info("Successfully connected to PostgreSQL connection pool.")
            # Wire event_emitter to all engine modules
            import athlete_state_engine as ase
            import training_load_engine as tle
            import injury_risk_engine as ire
            import demand_lifecycle_engine as dle
            from domain_events import DomainEventEmitter
            for mod in (ase, tle, ire, dle):
                mod.db_pool = db_pool
                mod.event_emitter.set_pool(db_pool)
            from recommendation_observability import db_pool as obs_pool
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

class DemandScoreRequest(BaseModel):
    sport: str = Field(..., example="Cricket")
    role: str = Field(..., example="Fast Bowler")
    athlete_id: Optional[int] = Field(default=None, example=1, description="Optional athlete ID for observability logging")
    results: Dict[str, float] = Field(
        default_factory=dict,
        example={"CMJ": 38.0, "Broad Jump": 2.1, "10m Sprint": 1.95}
    )
    equipment: List[str] = Field(..., example=["Trap Bar", "Medicine Ball"])
    difficulty_cap: str = Field(default="Advanced", example="Advanced")
    training_age_months: int = Field(default=96, ge=0, example=96)
    development_level: Optional[str] = Field(default=None, example="PERFORMANCE")

    model_config = {
        "json_schema_extra": {
            "example": {
                "sport": "Cricket",
                "role": "Fast Bowler",
                "results": {"CMJ": 38.0, "Broad Jump": 2.1, "10m Sprint": 1.95},
                "equipment": ["Trap Bar", "Medicine Ball"],
                "difficulty_cap": "Advanced",
                "training_age_months": 96
            }
        }
    }

class DemandScore(BaseModel):
    demand_id: int
    demand_name: str
    priority: int
    category: str
    demand_score: float
    exercise_count: int

class ScoredExercise(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    difficulty_level: str
    mechanics_type: str
    force_type: str
    relevance_score: float
    demand_name: str
    demand_id: int
    exercise_class: Optional[str] = None
    primary_adaptation: Optional[str] = None
    force_vector: Optional[str] = None

class DemandRecommendationResponse(BaseModel):
    sport: str
    athlete_role: str
    development_level: str
    demands: List[DemandScore]
    exercises: List[ScoredExercise]
    engine_mode: str = "v2"
    cached: bool = False
    recommendation_id: Optional[str] = Field(default=None, description="UUID from recommendation_log for coach feedback")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# -------------------------------------------------------------
# 2. Cache Layer (In-Memory with TTL)
# -------------------------------------------------------------

class MemoryCache:
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        async with self._lock:
            if key not in self._cache:
                return None
            entry = self._cache[key]
            if datetime.utcnow() > entry["expires_at"]:
                del self._cache[key]
                return None
            return entry["data"]

    async def set(self, key: str, data: Any, ttl_seconds: int = 300):
        async with self._lock:
            self._cache[key] = {
                "data": data,
                "expires_at": datetime.utcnow() + timedelta(seconds=ttl_seconds)
            }

    async def clear(self):
        async with self._lock:
            self._cache.clear()

cache = MemoryCache()

def generate_cache_key(request: DemandScoreRequest) -> str:
    dev_level = request.development_level or training_months_to_level(request.training_age_months)
    sorted_results = json.dumps(request.results, sort_keys=True) if request.results else ""
    key_str = (
        f"{request.sport.lower()}:{request.role.lower()}:{sorted_results}:"
        f"{sorted(request.equipment)}:{request.difficulty_cap.lower()}:{dev_level}"
    )
    return hashlib.sha256(key_str.encode("utf-8")).hexdigest()

# -------------------------------------------------------------
# 3. Repository Pattern
# -------------------------------------------------------------

class DemandRepository:
    async def get_role_by_name(self, sport: str, role: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    async def get_demand_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    async def get_role_demands(self, role_name: str, sport: str) -> List[Dict[str, Any]]:
        raise NotImplementedError()

    async def get_exercises_for_demand(
        self, demand_id: int, difficulty_cap: str, equipment: List[str],
        training_age_months: int = 0, development_level: str = "FOUNDATION"
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError()

    async def get_assessment_demand_mapping(self, assessment_name: str) -> List[Dict[str, Any]]:
        raise NotImplementedError()


class PostgreSqlDemandRepository(DemandRepository):
    def __init__(self, pool=None):
        self.pool = pool

    async def get_role_by_name(self, sport: str, role: str) -> Optional[Dict[str, Any]]:
        query = """
            SELECT r.id, r.name, s.name as sport_name
            FROM roles r
            JOIN sports s ON r.sport_id = s.id
            WHERE s.name ILIKE $1 AND r.name ILIKE $2
            LIMIT 1;
        """
        if not self.pool:
            return None
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, sport, role)
            return dict(row) if row else None

    async def get_demand_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        query = """
            SELECT id, name, description, demand_type, primary_quality_id, primary_pattern_id,
                   display_order, is_active
            FROM performance_demands
            WHERE name ILIKE $1 AND is_active = TRUE
            LIMIT 1;
        """
        if not self.pool:
            return None
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, name)
            return dict(row) if row else None

    async def get_role_demands(self, role_name: str, sport: str) -> List[Dict[str, Any]]:
        query = """
            SELECT pd.id, pd.name, pd.description, rdp.priority, rdp.category
            FROM role_demand_priority rdp
            JOIN performance_demands pd ON rdp.demand_id = pd.id
            JOIN roles r ON rdp.role_id = r.id
            JOIN sports s ON r.sport_id = s.id
            WHERE r.name ILIKE $1 AND s.name ILIKE $2 AND pd.is_active = TRUE
            ORDER BY rdp.priority DESC;
        """
        if not self.pool:
            return []
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, role_name, sport)
            return [dict(r) for r in rows]

    async def get_exercises_for_demand(
        self, demand_id: int, difficulty_cap: str, equipment: List[str],
        training_age_months: int = 0, development_level: str = "FOUNDATION"
    ) -> List[Dict[str, Any]]:
        diff_rank = {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Elite": 4}
        cap = diff_rank.get(difficulty_cap, 2)
        dev_ord = LEVEL_ORDINAL.get(development_level, 1)
        tech_cap = TECH_DIFF_CAP.get(development_level, 3)

        query = """
            SELECT e.id, e.name, e.description, e.difficulty_level, e.mechanics_type, e.force_type,
                   edm.relevance_score,
                   e.minimum_level, e.technical_difficulty
            FROM exercises e
            JOIN exercise_demand_mapping edm ON e.id = edm.exercise_id
            WHERE edm.demand_id = $1
              AND e.difficulty_level = ANY($2::varchar[])
              AND (e.technical_difficulty IS NULL OR e.technical_difficulty <= $3::int)
              AND (
                  CASE e.difficulty_level
                      WHEN 'Beginner' THEN 1
                      WHEN 'Intermediate' THEN 2
                      WHEN 'Advanced' THEN 3
                      WHEN 'Elite' THEN 4
                  END <= $4::int
              )
              AND NOT EXISTS (
                  SELECT 1
                  FROM exercise_equipment ee
                  JOIN equipment eq ON ee.equipment_id = eq.id
                  WHERE ee.exercise_id = e.id
                    AND ee.is_required = TRUE
                    AND eq.name <> 'Bodyweight'
                    AND eq.name <> ALL($5::varchar[])
              )
            ORDER BY edm.relevance_score DESC;
        """
        if not self.pool:
            return []
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, demand_id, list(diff_rank.keys()), tech_cap, cap, equipment)
            return [dict(r) for r in rows]

    async def get_assessment_demand_mapping(self, assessment_name: str) -> List[Dict[str, Any]]:
        query = """
            SELECT adm.assessment_id, adm.demand_id, adm.weight,
                   pd.name as demand_name, a.name as assessment_name
            FROM assessment_demand_mapping adm
            JOIN assessments a ON adm.assessment_id = a.id
            JOIN performance_demands pd ON adm.demand_id = pd.id
            WHERE a.name ILIKE $1;
        """
        if not self.pool:
            return []
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, assessment_name)
            return [dict(r) for r in rows]


class MockDemandRepository(DemandRepository):
    """Mock repository with V2 performance demand data matching Migration 000022 seed data."""

    def __init__(self):
        # 5 Cricket roles (matching athlete_module.ROLE_NAMES)
        self.roles = {
            "Fast Bowler": {"id": 1, "name": "Fast Bowler", "sport_name": "Cricket"},
            "Spinner": {"id": 2, "name": "Spinner", "sport_name": "Cricket"},
            "Batter": {"id": 3, "name": "Batter", "sport_name": "Cricket"},
            "Wicket Keeper": {"id": 4, "name": "Wicket Keeper", "sport_name": "Cricket"},
            "All Rounder": {"id": 5, "name": "All Rounder", "sport_name": "Cricket"},
        }

        # 18 Performance demands (matching 000022 F5)
        self.demands = {
            "Vertical Power": {"id": 1, "name": "Vertical Power", "description": "Explosive vertical force production through bilateral leg extension.", "demand_type": "Biomotor"},
            "Horizontal Drive Power": {"id": 2, "name": "Horizontal Drive Power", "description": "Explosive horizontal force production through hip-driven extension.", "demand_type": "Biomotor"},
            "Rotational Explosive Power": {"id": 3, "name": "Rotational Explosive Power", "description": "Explosive transverse plane torque generation.", "demand_type": "Biomotor"},
            "Squat Strength": {"id": 4, "name": "Squat Strength", "description": "Maximum bilateral lower body force through knee-dominant flexion-extension.", "demand_type": "Biomotor"},
            "Hinge Strength": {"id": 5, "name": "Hinge Strength", "description": "Maximum hip-dominant force through posterior chain engagement.", "demand_type": "Biomotor"},
            "Horizontal Push Strength": {"id": 6, "name": "Horizontal Push Strength", "description": "Maximum pressing force in the horizontal plane.", "demand_type": "Biomotor"},
            "Horizontal Pull Strength": {"id": 7, "name": "Horizontal Pull Strength", "description": "Maximum pulling force in the horizontal plane.", "demand_type": "Biomotor"},
            "Vertical Push Strength": {"id": 8, "name": "Vertical Push Strength", "description": "Maximum overhead pressing force.", "demand_type": "Biomotor"},
            "Vertical Pull Strength": {"id": 9, "name": "Vertical Pull Strength", "description": "Maximum pulling force in the vertical plane.", "demand_type": "Biomotor"},
            "Single-Leg Strength": {"id": 10, "name": "Single-Leg Strength", "description": "Maximum unilateral lower body force production.", "demand_type": "Biomotor"},
            "Single-Leg Stability": {"id": 11, "name": "Single-Leg Stability", "description": "Dynamic joint control during single-leg stance.", "demand_type": "Biomotor"},
            "Single-Leg Power": {"id": 12, "name": "Single-Leg Power", "description": "Explosive unilateral force production.", "demand_type": "Biomotor"},
            "Anti-Rotation Core Stability": {"id": 13, "name": "Anti-Rotation Core Stability", "description": "Isometric trunk rigidity resisting rotational forces.", "demand_type": "Biomotor"},
            "Rotational Core Control": {"id": 14, "name": "Rotational Core Control", "description": "Controlled rotational torque production through torso.", "demand_type": "Biomotor"},
            "Squat Mobility & Positioning": {"id": 15, "name": "Squat Mobility & Positioning", "description": "Active ROM for deep squat positioning.", "demand_type": "Biomotor"},
            "Hip Hinge Mobility": {"id": 16, "name": "Hip Hinge Mobility", "description": "Active ROM in hip flexion with neutral spine.", "demand_type": "Biomotor"},
            "Loaded Carry Endurance": {"id": 17, "name": "Loaded Carry Endurance", "description": "Sustained load carriage under locomotion.", "demand_type": "Biomotor"},
            "General Hypertrophy & Structural Adaptation": {"id": 18, "name": "General Hypertrophy & Structural Adaptation", "description": "Muscular enlargement for long-term capacity.", "demand_type": "Biomotor"},
        }

        # Role → Demand priorities (matching 000022 F6 seed data)
        self.role_demand_priorities = {
            "Fast Bowler": [
                (1, 100, "Primary"), (2, 95, "Primary"), (5, 90, "Primary"),
                (3, 85, "Primary"), (4, 80, "Primary"), (11, 75, "Secondary"),
                (13, 70, "Secondary"), (14, 65, "Secondary"), (17, 60, "Secondary"),
                (7, 55, "Secondary"), (8, 50, "Tertiary"), (18, 45, "Tertiary"),
            ],
            "Spinner": [
                (3, 100, "Primary"), (14, 95, "Primary"), (13, 90, "Primary"),
                (5, 85, "Primary"), (7, 80, "Secondary"), (9, 75, "Secondary"),
                (4, 70, "Secondary"), (11, 65, "Secondary"), (16, 60, "Secondary"),
                (15, 55, "Tertiary"), (17, 50, "Tertiary"), (18, 45, "Tertiary"),
            ],
            "Batter": [
                (2, 100, "Primary"), (3, 95, "Primary"), (1, 90, "Primary"),
                (11, 85, "Primary"), (12, 80, "Secondary"), (7, 75, "Secondary"),
                (13, 70, "Secondary"), (4, 65, "Secondary"), (5, 60, "Secondary"),
                (15, 55, "Tertiary"), (16, 50, "Tertiary"), (18, 45, "Tertiary"),
            ],
            "Wicket Keeper": [
                (4, 100, "Primary"), (15, 95, "Primary"), (11, 90, "Primary"),
                (12, 85, "Primary"), (1, 80, "Secondary"), (14, 75, "Secondary"),
                (13, 70, "Secondary"), (2, 65, "Secondary"), (17, 60, "Secondary"),
                (18, 55, "Tertiary"), (7, 50, "Tertiary"), (6, 45, "Tertiary"),
            ],
            "All Rounder": [
                (1, 90, "Primary"), (2, 85, "Primary"), (4, 85, "Primary"),
                (5, 80, "Primary"), (3, 75, "Secondary"), (11, 75, "Secondary"),
                (13, 70, "Secondary"), (17, 65, "Secondary"), (7, 60, "Tertiary"),
                (6, 55, "Tertiary"), (18, 50, "Tertiary"), (16, 45, "Tertiary"),
            ],
        }

        # Exercise → Demand mappings
        # Each tuple: (demand_name, relevance_score, is_primary)
        self.exercise_demand_mappings: Dict[str, List[Tuple[str, int, bool]]] = {
            "Trap Bar Jump Squat": [
                ("Vertical Power", 10, True), ("Horizontal Drive Power", 8, False),
                ("Squat Strength", 8, False), ("Single-Leg Power", 6, False),
            ],
            "Single-Leg Lateral Bound": [
                ("Single-Leg Power", 10, True), ("Single-Leg Stability", 9, True),
                ("Horizontal Drive Power", 7, False),
            ],
            "Medicine Ball Overhead Backwards Toss": [
                ("Vertical Power", 9, True), ("Horizontal Drive Power", 8, False),
                ("Rotational Explosive Power", 7, False),
            ],
            "Medicine Ball Rotational Chest Pass": [
                ("Rotational Explosive Power", 9, True), ("Rotational Core Control", 8, False),
                ("Horizontal Push Strength", 6, False),
            ],
            "Cable Pallof Press with Rotation": [
                ("Anti-Rotation Core Stability", 9, True), ("Rotational Core Control", 7, False),
            ],
            "Medicine Ball Rotational Scoop Toss": [
                ("Rotational Explosive Power", 10, True), ("Rotational Core Control", 8, False),
            ],
            "Barbell Back Squat": [
                ("Squat Strength", 10, True), ("Vertical Power", 6, False),
                ("General Hypertrophy & Structural Adaptation", 8, False),
                ("Squat Mobility & Positioning", 7, False),
            ],
            "Trap Bar Deadlift": [
                ("Hinge Strength", 10, True), ("Horizontal Drive Power", 9, True),
                ("Hip Hinge Mobility", 7, False),
            ],
            "Kettlebell Swing": [
                ("Horizontal Drive Power", 8, False), ("Hinge Strength", 8, False),
                ("Loaded Carry Endurance", 6, False),
            ],
            "Power Clean": [
                ("Vertical Power", 10, True), ("Horizontal Drive Power", 9, True),
                ("Hinge Strength", 8, False),
            ],
            "Clean Pull": [
                ("Vertical Power", 8, False), ("Hinge Strength", 8, False),
            ],
            "Mid-Thigh Pull": [
                ("Vertical Power", 9, True), ("Hinge Strength", 9, True),
                ("Horizontal Drive Power", 8, False),
            ],
            "High Pull": [
                ("Vertical Power", 8, False), ("Horizontal Drive Power", 7, False),
            ],
            "Snatch Pull": [
                ("Vertical Power", 7, False), ("Hinge Strength", 6, False),
            ],
            "Hang Clean": [
                ("Vertical Power", 8, False), ("Hinge Strength", 7, False),
            ],
            "Squat Clean": [
                ("Squat Strength", 8, False), ("Vertical Power", 7, False),
            ],
            "Clean and Jerk": [
                ("Vertical Power", 7, False), ("Vertical Push Strength", 8, False),
            ],
            "Power Snatch": [
                ("Vertical Power", 10, True), ("Squat Mobility & Positioning", 6, False),
            ],
            "Hang Snatch": [
                ("Vertical Power", 7, False), ("Squat Mobility & Positioning", 6, False),
            ],
            "Snatch Balance": [
                ("Squat Mobility & Positioning", 8, False), ("Single-Leg Stability", 6, False),
            ],
            "Overhead Squat": [
                ("Squat Mobility & Positioning", 9, True), ("Squat Strength", 6, False),
                ("Vertical Push Strength", 7, False),
            ],
            "Rear Foot Elevated Split Squat": [
                ("Single-Leg Strength", 10, True), ("Single-Leg Stability", 8, False),
                ("Single-Leg Power", 7, False),
            ],
            "Dumbbell Row": [
                ("Horizontal Pull Strength", 9, True), ("Vertical Pull Strength", 6, False),
            ],
            "Dumbbell Overhead Press": [
                ("Vertical Push Strength", 9, True), ("Horizontal Push Strength", 6, False),
            ],
            "Nordic Hamstring Curl": [
                ("Hinge Strength", 8, False), ("Hip Hinge Mobility", 6, False),
                ("Single-Leg Stability", 7, False),
            ],
            "Plank with Rotation": [
                ("Anti-Rotation Core Stability", 8, False), ("Rotational Core Control", 8, False),
            ],
            "Push Press": [
                ("Vertical Push Strength", 9, True), ("Vertical Power", 6, False),
            ],
            "Push Jerk": [
                ("Vertical Push Strength", 8, False), ("Vertical Power", 7, False),
            ],
            "Split Jerk": [
                ("Vertical Push Strength", 7, False), ("Single-Leg Stability", 6, False),
            ],
            "Depth Jump": [
                ("Vertical Power", 10, True), ("Single-Leg Power", 8, False),
            ],
            "A-Skip": [
                ("Single-Leg Power", 7, False), ("Single-Leg Stability", 8, False),
                ("Horizontal Drive Power", 6, False),
            ],
        }

        # Assessment → Demand mappings (from seed data logic)
        self.assessment_demand_mappings: Dict[str, List[Tuple[str, float]]] = {
            "CMJ": [("Vertical Power", 1.0), ("Single-Leg Power", 0.6)],
            "Broad Jump": [("Horizontal Drive Power", 1.0), ("Single-Leg Power", 0.5)],
            "10m Sprint": [("Horizontal Drive Power", 0.8), ("Single-Leg Power", 0.6)],
            "20m Sprint": [("Horizontal Drive Power", 0.6), ("Single-Leg Power", 0.4)],
            "Pull Up": [("Vertical Pull Strength", 1.0), ("Horizontal Pull Strength", 0.6)],
            "Trap Bar Deadlift": [("Hinge Strength", 1.0), ("Squat Strength", 0.5)],
            "Rotational Med Ball Throw": [("Rotational Explosive Power", 1.0), ("Rotational Core Control", 0.7)],
        }

        # Equipment catalog for exercises (mirrors MockExerciseRepository)
        self.exercise_equipment: Dict[str, List[str]] = {
            "Trap Bar Jump Squat": ["Trap Bar"],
            "Single-Leg Lateral Bound": ["Bodyweight"],
            "Medicine Ball Overhead Backwards Toss": ["Medicine Ball"],
            "Medicine Ball Rotational Chest Pass": ["Medicine Ball"],
            "Cable Pallof Press with Rotation": ["Cable Machine"],
            "Medicine Ball Rotational Scoop Toss": ["Medicine Ball"],
            "Barbell Back Squat": ["Barbell"],
            "Trap Bar Deadlift": ["Trap Bar"],
            "Kettlebell Swing": ["Kettlebell"],
            "Power Clean": ["Barbell"],
            "Clean Pull": ["Barbell"],
            "Mid-Thigh Pull": ["Barbell"],
            "High Pull": ["Barbell"],
            "Snatch Pull": ["Barbell"],
            "Hang Clean": ["Barbell"],
            "Squat Clean": ["Barbell"],
            "Clean and Jerk": ["Barbell"],
            "Power Snatch": ["Barbell"],
            "Hang Snatch": ["Barbell"],
            "Snatch Balance": ["Barbell"],
            "Overhead Squat": ["Barbell"],
            "Rear Foot Elevated Split Squat": ["Dumbbell", "Bodyweight"],
            "Dumbbell Row": ["Dumbbell"],
            "Dumbbell Overhead Press": ["Dumbbell"],
            "Nordic Hamstring Curl": ["Bodyweight"],
            "Plank with Rotation": ["Bodyweight"],
            "Push Press": ["Barbell"],
            "Push Jerk": ["Barbell"],
            "Split Jerk": ["Barbell"],
            "Depth Jump": ["Bodyweight"],
            "A-Skip": ["Bodyweight"],
        }

        # Exercise metadata (difficulty, mechanics, force type)
        self.exercise_metadata: Dict[str, Dict[str, Any]] = {
            "Trap Bar Jump Squat": {"difficulty_level": "Advanced", "mechanics_type": "Compound", "force_type": "Push", "minimum_level": "DEVELOPMENT", "technical_difficulty": 6},
            "Single-Leg Lateral Bound": {"difficulty_level": "Intermediate", "mechanics_type": "Compound", "force_type": "Push", "minimum_level": "FOUNDATION", "technical_difficulty": 4},
            "Medicine Ball Overhead Backwards Toss": {"difficulty_level": "Intermediate", "mechanics_type": "Compound", "force_type": "Hinge", "minimum_level": "FOUNDATION", "technical_difficulty": 4},
            "Medicine Ball Rotational Chest Pass": {"difficulty_level": "Beginner", "mechanics_type": "Compound", "force_type": "Rotation", "minimum_level": "FOUNDATION", "technical_difficulty": 1},
            "Cable Pallof Press with Rotation": {"difficulty_level": "Intermediate", "mechanics_type": "Compound", "force_type": "Rotation", "minimum_level": "FOUNDATION", "technical_difficulty": 3},
            "Medicine Ball Rotational Scoop Toss": {"difficulty_level": "Beginner", "mechanics_type": "Compound", "force_type": "Rotation", "minimum_level": "FOUNDATION", "technical_difficulty": 1},
            "Barbell Back Squat": {"difficulty_level": "Intermediate", "mechanics_type": "Compound", "force_type": "Push", "minimum_level": "DEVELOPMENT", "technical_difficulty": 5},
            "Trap Bar Deadlift": {"difficulty_level": "Intermediate", "mechanics_type": "Compound", "force_type": "Hinge", "minimum_level": "DEVELOPMENT", "technical_difficulty": 5},
            "Kettlebell Swing": {"difficulty_level": "Beginner", "mechanics_type": "Compound", "force_type": "Hinge", "minimum_level": "FOUNDATION", "technical_difficulty": 1},
            "Power Clean": {"difficulty_level": "Advanced", "mechanics_type": "Compound", "force_type": "Pull", "minimum_level": "PERFORMANCE", "technical_difficulty": 7},
            "Clean Pull": {"difficulty_level": "Intermediate", "mechanics_type": "Compound", "force_type": "Pull", "minimum_level": "DEVELOPMENT", "technical_difficulty": 3},
            "Mid-Thigh Pull": {"difficulty_level": "Intermediate", "mechanics_type": "Compound", "force_type": "Pull", "minimum_level": "DEVELOPMENT", "technical_difficulty": 4},
            "High Pull": {"difficulty_level": "Advanced", "mechanics_type": "Compound", "force_type": "Pull", "minimum_level": "DEVELOPMENT", "technical_difficulty": 5},
            "Snatch Pull": {"difficulty_level": "Advanced", "mechanics_type": "Compound", "force_type": "Pull", "minimum_level": "PERFORMANCE", "technical_difficulty": 5},
            "Hang Clean": {"difficulty_level": "Advanced", "mechanics_type": "Compound", "force_type": "Pull", "minimum_level": "DEVELOPMENT", "technical_difficulty": 6},
            "Squat Clean": {"difficulty_level": "Elite", "mechanics_type": "Compound", "force_type": "Push", "minimum_level": "PERFORMANCE", "technical_difficulty": 9},
            "Clean and Jerk": {"difficulty_level": "Elite", "mechanics_type": "Compound", "force_type": "Push", "minimum_level": "PERFORMANCE", "technical_difficulty": 10},
            "Power Snatch": {"difficulty_level": "Elite", "mechanics_type": "Compound", "force_type": "Pull", "minimum_level": "PERFORMANCE", "technical_difficulty": 8},
            "Hang Snatch": {"difficulty_level": "Advanced", "mechanics_type": "Compound", "force_type": "Pull", "minimum_level": "PERFORMANCE", "technical_difficulty": 7},
            "Snatch Balance": {"difficulty_level": "Elite", "mechanics_type": "Compound", "force_type": "Push", "minimum_level": "PERFORMANCE", "technical_difficulty": 8},
            "Overhead Squat": {"difficulty_level": "Intermediate", "mechanics_type": "Compound", "force_type": "Push", "minimum_level": "DEVELOPMENT", "technical_difficulty": 7},
            "Rear Foot Elevated Split Squat": {"difficulty_level": "Intermediate", "mechanics_type": "Compound", "force_type": "Push", "minimum_level": "DEVELOPMENT", "technical_difficulty": 5},
            "Dumbbell Row": {"difficulty_level": "Beginner", "mechanics_type": "Compound", "force_type": "Pull", "minimum_level": "FOUNDATION", "technical_difficulty": 2},
            "Dumbbell Overhead Press": {"difficulty_level": "Beginner", "mechanics_type": "Compound", "force_type": "Push", "minimum_level": "FOUNDATION", "technical_difficulty": 2},
            "Nordic Hamstring Curl": {"difficulty_level": "Advanced", "mechanics_type": "Isolation", "force_type": "Pull", "minimum_level": "PERFORMANCE", "technical_difficulty": 7},
            "Plank with Rotation": {"difficulty_level": "Beginner", "mechanics_type": "Compound", "force_type": "Rotation", "minimum_level": "FOUNDATION", "technical_difficulty": 2},
            "Push Press": {"difficulty_level": "Intermediate", "mechanics_type": "Compound", "force_type": "Push", "minimum_level": "DEVELOPMENT", "technical_difficulty": 4},
            "Push Jerk": {"difficulty_level": "Advanced", "mechanics_type": "Compound", "force_type": "Push", "minimum_level": "DEVELOPMENT", "technical_difficulty": 6},
            "Split Jerk": {"difficulty_level": "Elite", "mechanics_type": "Compound", "force_type": "Push", "minimum_level": "PERFORMANCE", "technical_difficulty": 9},
            "Depth Jump": {"difficulty_level": "Elite", "mechanics_type": "Compound", "force_type": "Push", "minimum_level": "PERFORMANCE", "technical_difficulty": 8},
            "A-Skip": {"difficulty_level": "Beginner", "mechanics_type": "Compound", "force_type": "N/A", "minimum_level": "FOUNDATION", "technical_difficulty": 1},
        }

        # Exercise ID counter (matching MockExerciseRepository IDs)
        self.exercise_ids: Dict[str, int] = {
            "Trap Bar Jump Squat": 1,
            "Single-Leg Lateral Bound": 2,
            "Medicine Ball Overhead Backwards Toss": 3,
            "Medicine Ball Rotational Chest Pass": 4,
            "Cable Pallof Press with Rotation": 5,
            "Medicine Ball Rotational Scoop Toss": 91,
            "Barbell Back Squat": 85,
            "Trap Bar Deadlift": 88,
            "Kettlebell Swing": 89,
            "Power Clean": 86,
            "Clean Pull": 120,
            "Mid-Thigh Pull": 121,
            "High Pull": 122,
            "Snatch Pull": 123,
            "Hang Clean": 124,
            "Squat Clean": 125,
            "Clean and Jerk": 126,
            "Power Snatch": 127,
            "Hang Snatch": 128,
            "Snatch Balance": 129,
            "Overhead Squat": 130,
            "Rear Foot Elevated Split Squat": 87,
            "Dumbbell Row": 96,
            "Dumbbell Overhead Press": 97,
            "Nordic Hamstring Curl": 94,
            "Plank with Rotation": 98,
            "Push Press": 131,
            "Push Jerk": 132,
            "Split Jerk": 133,
            "Depth Jump": 90,
            "A-Skip": 92,
        }

    async def get_role_by_name(self, sport: str, role: str) -> Optional[Dict[str, Any]]:
        matched_role = None
        for r_name, r_data in self.roles.items():
            if r_name.lower() == role.lower() and sport.lower() == r_data["sport_name"].lower():
                matched_role = r_data
                break
            if r_name.lower() == role.lower():
                matched_role = r_data
        if not matched_role and "bowl" in role.lower():
            matched_role = self.roles.get("Fast Bowler")
        if not matched_role and "spin" in role.lower():
            matched_role = self.roles.get("Spinner")
        if not matched_role and "bat" in role.lower():
            matched_role = self.roles.get("Batter")
        if not matched_role and ("wicket" in role.lower() or "keeper" in role.lower()):
            matched_role = self.roles.get("Wicket Keeper")
        if not matched_role and ("all" in role.lower() or "round" in role.lower()):
            matched_role = self.roles.get("All Rounder")
        return matched_role

    async def get_demand_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        for d_name, d_data in self.demands.items():
            if d_name.lower() == name.lower():
                return d_data
        return None

    async def get_role_demands(self, role_name: str, sport: str) -> List[Dict[str, Any]]:
        role = await self.get_role_by_name(sport, role_name)
        if not role:
            return []
        priorities = self.role_demand_priorities.get(role["name"], [])
        result = []
        for demand_id, priority, category in priorities:
            for d_name, d_data in self.demands.items():
                if d_data["id"] == demand_id:
                    result.append({
                        "id": demand_id,
                        "name": d_name,
                        "description": d_data["description"],
                        "priority": priority,
                        "category": category,
                    })
                    break
        return result

    async def get_exercises_for_demand(
        self, demand_id: int, difficulty_cap: str, equipment: List[str],
        training_age_months: int = 0, development_level: str = "FOUNDATION"
    ) -> List[Dict[str, Any]]:
        diff_rank = {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Elite": 4}
        cap = diff_rank.get(difficulty_cap, 2)
        dev_ord = LEVEL_ORDINAL.get(development_level, 1)
        tech_cap = TECH_DIFF_CAP.get(development_level, 3)

        # Find demand name from id
        demand_name = None
        for d_name, d_data in self.demands.items():
            if d_data["id"] == demand_id:
                demand_name = d_name
                break
        if not demand_name:
            return []

        # Find all exercises mapped to this demand
        results = []
        for ex_name, mappings in self.exercise_demand_mappings.items():
            for mapped_demand_name, relevance, is_primary in mappings:
                if mapped_demand_name == demand_name:
                    meta = self.exercise_metadata.get(ex_name, {})
                    eq = self.exercise_equipment.get(ex_name, [])

                    # Difficulty gate
                    ex_diff = meta.get("difficulty_level", "Beginner")
                    if diff_rank.get(ex_diff, 1) > cap:
                        continue

                    # Development level gate
                    ex_min_level = meta.get("minimum_level", "FOUNDATION")
                    if LEVEL_ORDINAL.get(ex_min_level, 1) > dev_ord:
                        continue

                    # Technical difficulty gate
                    ex_tech = meta.get("technical_difficulty")
                    if ex_tech is not None and ex_tech > tech_cap:
                        continue

                    # Equipment gate
                    eq_ok = True
                    for req_eq in eq:
                        if req_eq == "Bodyweight":
                            continue
                        if req_eq not in equipment:
                            eq_ok = False
                            break
                    if not eq_ok:
                        continue

                    ex_id = self.exercise_ids.get(ex_name, 0)

                    results.append({
                        "id": ex_id,
                        "name": ex_name,
                        "description": f"Targets {demand_name} using {', '.join(eq)}.",
                        "difficulty_level": ex_diff,
                        "mechanics_type": meta.get("mechanics_type", "Compound"),
                        "force_type": meta.get("force_type", "Push"),
                        "relevance_score": relevance,
                        "demand_name": demand_name,
                        "demand_id": demand_id,
                        "is_primary": is_primary,
                    })
                    break

        # Sort by relevance score descending
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results

    async def get_assessment_demand_mapping(self, assessment_name: str) -> List[Dict[str, Any]]:
        clean_name = assessment_name.strip().lower()
        for ass_name, mappings in self.assessment_demand_mappings.items():
            if ass_name.lower() == clean_name:
                result = []
                for demand_name, weight in mappings:
                    demand = await self.get_demand_by_name(demand_name)
                    if demand:
                        result.append({
                            "assessment_name": ass_name,
                            "demand_id": demand["id"],
                            "demand_name": demand_name,
                            "weight": weight,
                        })
                return result
        return []


def get_demand_repository() -> DemandRepository:
    if db_pool:
        logger.info("FACTORY: get_demand_repository() -> PostgreSqlDemandRepository")
        return PostgreSqlDemandRepository(db_pool)
    logger.info("FACTORY: get_demand_repository() -> MockDemandRepository")
    return MockDemandRepository()

# -------------------------------------------------------------
# 4. Service Layer (Demand Scoring Business Logic)
# -------------------------------------------------------------

class DemandScoringService:
    """
    Scores performance demands based on:
    - Role-specific priority weights
    - Assessment-based deficit severity
    - Athlete development level multiplier
    - Equipment availability match
    - Injury risk penalty (optional, for future use)
    """

    def __init__(self, repo: DemandRepository):
        self.repo = repo

    def compute_deficit_factor(self, results: Dict[str, float]) -> Dict[str, float]:
        """
        Compute a deficit factor per demand based on assessment results.
        Returns dict of demand_name -> deficit_factor (0.0 to 1.0).
        Higher factor = greater deficit = more urgent demand.
        """
        deficit_factors: Dict[str, float] = {}

        if not results:
            return deficit_factors

        for assessment_name, score in results.items():
            mappings = asyncio.run_coroutine_threadsafe(
                self.repo.get_assessment_demand_mapping(assessment_name),
                asyncio.get_event_loop()
            )
            # Fallback: use simple heuristic based on assessment name
            # In production, this would be async — for the mock we compute inline
            if not mappings:
                continue

            for mapping in mappings:
                demand_name = mapping["demand_name"]
                weight = mapping["weight"]
                # Simple deficit heuristic: lower scores in power/strength tests indicate deficit
                # For sprint tests, lower time = better, so invert
                is_sprint = any(x in assessment_name.lower() for x in ["sprint"])
                if is_sprint:
                    deficit_severity = 1.0 - min(score / 3.0, 1.0) if score > 0 else 1.0
                else:
                    # For CMJ, Broad Jump, etc. — lower score = more deficit
                    # Normalize: assume reasonable max of 2.5m for BJ, 50cm for CMJ, etc.
                    deficit_severity = 1.0 - min(score / 50.0, 1.0) if "CMJ" in assessment_name else (
                        1.0 - min(score / 3.0, 1.0) if "Broad" in assessment_name else
                        1.0 - min(score / 250.0, 1.0) if "Deadlift" in assessment_name else
                        1.0 - min(score / 20.0, 1.0) if "Pull" in assessment_name else
                        1.0 - min(score / 12.0, 1.0) if "Rotational" in assessment_name else
                        0.5
                    )

                # Apply weight from assessment_demand_mapping
                weighted_deficit = deficit_severity * weight

                if demand_name not in deficit_factors or weighted_deficit > deficit_factors[demand_name]:
                    deficit_factors[demand_name] = round(weighted_deficit, 2)

        return deficit_factors

    def compute_demand_scores(
        self, role_demands: List[Dict[str, Any]], results: Dict[str, float],
        development_level: str, equipment: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Score each demand for the athlete using the formula:
        demand_score = priority_weight × (1.0 + deficit_severity) × level_multiplier × equipment_match

        deficit_severity ranges 0.0-1.0 from assessment data; defaults to 0.0 (neutral).
        A measured deficit boosts the score above the baseline priority.

        Returns scored demands sorted by score descending.
        """
        level_multiplier = {"FOUNDATION": 0.7, "DEVELOPMENT": 0.85, "PERFORMANCE": 1.0}.get(development_level, 0.7)

        deficit_factors = self.compute_deficit_factor(results)

        scored = []
        for demand in role_demands:
            priority = demand["priority"]
            priority_weight = priority / 100.0  # Normalize to 0-1

            deficit_severity = deficit_factors.get(demand["name"], 0.0)
            deficit_multiplier = 1.0 + deficit_severity

            equipment_match = 1.0

            demand_score = priority_weight * deficit_multiplier * level_multiplier * equipment_match
            demand_score = round(demand_score * 100.0, 2)

            scored.append({
                "demand_id": demand["id"],
                "demand_name": demand["name"],
                "priority": priority,
                "category": demand["category"],
                "demand_score": demand_score,
                "deficit_factor": deficit_factor,
            })

        scored.sort(key=lambda x: x["demand_score"], reverse=True)
        return scored

    def score_exercise_for_demand(
        self, exercise: Dict[str, Any], priority_weight: float,
        development_level: str, equipment: List[str]
    ) -> float:
        """
        Score an exercise within a demand context:
        exercise_score = (relevance / 10) × priority_weight × level_mult × equipment_match
        """
        level_mult = {"FOUNDATION": 0.7, "DEVELOPMENT": 0.85, "PERFORMANCE": 1.0}.get(development_level, 0.7)
        relevance = exercise.get("relevance_score", 5) / 10.0

        equipment_available = equipment or []
        ex_equipment = self._get_exercise_equipment(exercise["name"])
        eq_match = 1.0
        for req_eq in ex_equipment:
            if req_eq == "Bodyweight":
                continue
            if req_eq not in equipment_available:
                eq_match = 0.0
                break

        score = relevance * priority_weight * level_mult * eq_match
        return round(score * 100.0, 2)

    def _get_exercise_equipment(self, exercise_name: str) -> List[str]:
        if hasattr(self.repo, 'exercise_equipment') and isinstance(self.repo, MockDemandRepository):
            return self.repo.exercise_equipment.get(exercise_name, ["Bodyweight"])
        return ["Bodyweight"]


# Synchronous wrapper for deficit factor computation
def compute_deficit_factor_sync(repo: DemandRepository, results: Dict[str, float]) -> Dict[str, float]:
    """Compute deficit factors synchronously using mock data lookups."""
    deficit_factors: Dict[str, float] = {}
    if not results:
        return deficit_factors

    for assessment_name, score in results.items():
        # Access mock data directly
        if hasattr(repo, 'assessment_demand_mappings') and isinstance(repo, MockDemandRepository):
            mappings = []
            clean_name = assessment_name.strip().lower()
            for ass_name, ass_mappings in repo.assessment_demand_mappings.items():
                if ass_name.lower() == clean_name:
                    for demand_name, weight in ass_mappings:
                        demand = repo.demands.get(demand_name)
                        if demand:
                            mappings.append({
                                "assessment_name": ass_name,
                                "demand_id": demand["id"],
                                "demand_name": demand_name,
                                "weight": weight,
                            })
                    break
        else:
            continue

        for mapping in mappings:
            demand_name = mapping["demand_name"]
            weight = mapping["weight"]
            is_sprint = any(x in assessment_name.lower() for x in ["sprint"])
            if is_sprint:
                deficit_severity = 1.0 - min(score / 3.0, 1.0) if score > 0 else 1.0
            else:
                deficit_severity = 1.0 - min(score / 50.0, 1.0) if "CMJ" in assessment_name else (
                    1.0 - min(score / 3.0, 1.0) if "Broad" in assessment_name else
                    1.0 - min(score / 250.0, 1.0) if "Deadlift" in assessment_name else
                    1.0 - min(score / 20.0, 1.0) if "Pull" in assessment_name else
                    1.0 - min(score / 12.0, 1.0) if "Rotational" in assessment_name else
                    0.5
                )
            weighted_deficit = round(deficit_severity * weight, 2)
            if demand_name not in deficit_factors or weighted_deficit > deficit_factors[demand_name]:
                deficit_factors[demand_name] = weighted_deficit

    return deficit_factors


async def compute_role_demand_scores(
    repo: DemandRepository, sport: str, role: str, results: Dict[str, float],
    development_level: str, equipment: List[str]
) -> List[Dict[str, Any]]:
    """Top-level async function to compute demand scores for a role."""
    role_demands = await repo.get_role_demands(role, sport)
    if not role_demands:
        return []

    deficit_factors = compute_deficit_factor_sync(repo, results)
    level_mult = {"FOUNDATION": 0.7, "DEVELOPMENT": 0.85, "PERFORMANCE": 1.0}.get(development_level, 0.7)

    scored = []
    for demand in role_demands:
        priority = demand["priority"]
        priority_weight = priority / 100.0
        deficit_severity = deficit_factors.get(demand["name"], 0.0)
        deficit_multiplier = 1.0 + deficit_severity

        equipment_match = 1.0
        demand_score = round(priority_weight * deficit_multiplier * level_mult * equipment_match * 100.0, 2)

        scored.append({
            "demand_id": demand["id"],
            "demand_name": demand["name"],
            "priority": priority,
            "category": demand["category"],
            "demand_score": demand_score,
            "deficit_factor": deficit_severity,
        })

    scored.sort(key=lambda x: x["demand_score"], reverse=True)
    return scored


async def get_sync_event_loop():
    """Helper to get or create an event loop for synchronous operations."""
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop

# -------------------------------------------------------------
# 5. FastAPI Endpoints
# -------------------------------------------------------------

@app.post(
    "/api/v2/demand-recommendations",
    response_model=DemandRecommendationResponse,
    status_code=status.HTTP_200_OK,
    summary="Get V2 Demand-Based Exercise Recommendations",
    description="Scores performance demands by priority × deficit × level, then ranks exercises per demand."
)
async def get_demand_recommendations(
    request: DemandScoreRequest,
    repo: DemandRepository = Depends(get_demand_repository),
    observability_repo: RecommendationObservabilityRepository = Depends(get_observability_repository),
):
    development_level = request.development_level or training_months_to_level(request.training_age_months)

    # Check cache
    cache_key = generate_cache_key(request)
    cached_data = await cache.get(cache_key)
    if cached_data:
        logger.info(f"Cache hit for demand recommendation key: {cache_key}")
        cached_response = DemandRecommendationResponse(**cached_data)
        cached_response.cached = True
        # Log cached recommendation synchronously to capture recommendation_id
        role_obj = await repo.get_role_by_name(request.sport, request.role)
        role_id = role_obj["id"] if role_obj else 0
        if request.sport and request.role:
            try:
                log_result = await observability_repo.log_recommendation(
                    athlete_id=request.athlete_id,
                    role_id=role_id,
                    sport=request.sport,
                    role_name=request.role,
                    development_level=cached_response.development_level,
                    request_params=request.model_dump(),
                    assessment_snapshot=request.results,
                    demand_scores=[d.model_dump() for d in cached_response.demands],
                    candidate_rankings=[e.model_dump() for e in cached_response.exercises],
                    cached=True,
                )
                if isinstance(log_result, dict):
                    cached_response.recommendation_id = log_result.get("recommendation_id")
                elif isinstance(log_result, str):
                    cached_response.recommendation_id = log_result
            except Exception as e:
                logger.warning(f"Failed to log cached recommendation: {e}")
        return cached_response

    logger.info(f"Cache miss. Computing demand scores for {request.sport} {request.role} ({development_level})")

    # Step 1: Compute demand scores
    scored_demands = await compute_role_demand_scores(
        repo=repo,
        sport=request.sport,
        role=request.role,
        results=request.results,
        development_level=development_level,
        equipment=request.equipment,
    )

    if not scored_demands:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No performance demands found for role '{request.role}' in sport '{request.sport}'."
        )

    # Step 2: Compute scored exercises for top demands
    all_scored_exercises = []
    for sd in scored_demands:
        exercises = await repo.get_exercises_for_demand(
            demand_id=sd["demand_id"],
            difficulty_cap=request.difficulty_cap,
            equipment=request.equipment,
            training_age_months=request.training_age_months,
            development_level=development_level,
        )

        for ex in exercises:
            priority_weight = sd["priority"] / 100.0
            level_mult = {"FOUNDATION": 0.7, "DEVELOPMENT": 0.85, "PERFORMANCE": 1.0}.get(development_level, 0.7)
            relevance = ex.get("relevance_score", 5) / 10.0

            ex_equipment = []
            if isinstance(repo, MockDemandRepository):
                ex_equipment = repo.exercise_equipment.get(ex["name"], ["Bodyweight"])

            eq_match = 1.0
            for req_eq in ex_equipment:
                if req_eq == "Bodyweight":
                    continue
                if req_eq not in request.equipment:
                    eq_match = 0.0
                    break

            score = relevance * priority_weight * level_mult * eq_match
            ex_with_score = {**ex, "recommendation_score": round(score * 100.0, 2)}
            all_scored_exercises.append(ex_with_score)

    # Step 3: Sort exercises by score descending
    all_scored_exercises.sort(key=lambda x: x["recommendation_score"], reverse=True)

    # Step 4: Enrich with classification metadata
    for item in all_scored_exercises:
        item["exercise_class"] = classify_exercise(item)
        item["primary_adaptation"] = determine_primary_adaptation(item)
        item["force_vector"] = determine_force_vector(item)

    # Build response
    demand_scores = [
        DemandScore(
            demand_id=sd["demand_id"],
            demand_name=sd["demand_name"],
            priority=sd["priority"],
            category=sd["category"],
            demand_score=sd["demand_score"],
            exercise_count=sum(1 for ex in all_scored_exercises if ex["demand_id"] == sd["demand_id"]),
        )
        for sd in scored_demands
    ]

    scored_exercises = [
        ScoredExercise(
            id=ex["id"],
            name=ex["name"],
            description=ex.get("description"),
            difficulty_level=ex["difficulty_level"],
            mechanics_type=ex["mechanics_type"],
            force_type=ex["force_type"],
            relevance_score=ex["recommendation_score"],
            demand_name=ex["demand_name"],
            demand_id=ex["demand_id"],
            exercise_class=ex.get("exercise_class"),
            primary_adaptation=ex.get("primary_adaptation"),
            force_vector=ex.get("force_vector"),
        )
        for ex in all_scored_exercises
    ]

    # Resolve role_id for observability logging
    role_obj = await repo.get_role_by_name(request.sport, request.role)
    role_id = role_obj["id"] if role_obj else 0

    response_data = DemandRecommendationResponse(
        sport=request.sport,
        athlete_role=request.role,
        development_level=development_level,
        demands=demand_scores,
        exercises=scored_exercises,
    )

    # Log recommendation for observability
    if request.sport and request.role:
        try:
            log_result = await observability_repo.log_recommendation(
                athlete_id=request.athlete_id,
                role_id=role_id,
                sport=request.sport,
                role_name=request.role,
                development_level=development_level,
                request_params=request.model_dump(),
                assessment_snapshot=request.results,
                demand_scores=[sd for sd in scored_demands],
                candidate_rankings=[ex for ex in all_scored_exercises],
                execution_time_ms=None,
                cached=False,
            )
            if isinstance(log_result, dict):
                response_data.recommendation_id = log_result.get("recommendation_id")
            elif isinstance(log_result, str):
                response_data.recommendation_id = log_result
        except Exception as e:
            logger.warning(f"Failed to log recommendation: {e}")

    # Cache
    await cache.set(cache_key, response_data.model_dump(), ttl_seconds=300)

    return response_data


@app.post(
    "/api/v2/cache/clear",
    status_code=status.HTTP_200_OK,
    summary="Clear V2 Demand Engine Cache",
)
async def clear_demand_cache():
    await cache.clear()
    logger.info("Demand scoring engine cache cleared.")
    return {"status": "success", "message": "Demand scoring engine cache cleared."}


@app.get(
    "/health",
    status_code=status.HTTP_200_OK,
)
async def health_check():
    return {
        "status": "healthy",
        "engine_mode": "v2",
        "timestamp": datetime.utcnow(),
        "database_connected": os.getenv("DATABASE_URL") is not None,
    }


# -------------------------------------------------------------
# 6. ENGINE_MODE Feature Flag
# -------------------------------------------------------------

ENGINE_MODE = os.getenv("ENGINE_MODE", "v1").lower()

def get_engine_mode() -> str:
    """Return the current engine mode: v1, v2, or dual."""
    return ENGINE_MODE

@app.get(
    "/api/v2/engine-mode",
    status_code=status.HTTP_200_OK,
    summary="Get Current Engine Mode",
)
async def engine_mode():
    return {
        "engine_mode": ENGINE_MODE,
        "valid_modes": ["v1", "v2", "dual"],
        "description": "v1=template engine, v2=demand engine, dual=both for validation",
    }
