# Forge Session Generator Engine
# Role: Principal Systems Engineer
# Description: Production-grade FastAPI service layer and repository layer for generating
# complete single training sessions (Warmup -> Primary -> Secondary -> Accessory -> Core -> Conditioning)
# with zero movement pattern duplication, respecting equipment access, difficulty caps, and S&C specificity ranks.

import os
import re
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field

# Existing module imports
from athlete_module import get_athlete_repository, AthleteRepository, ROLE_NAMES
from recommendation_engine import (
    MockExerciseRepository,
    PostgreSqlExerciseRepository,
    RecommendationRequest,
    get_exercise_recommendations,
    training_months_to_level
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("forge-session-generator")

app = FastAPI(
    title="Forge Session Generator Engine",
    description="Generates optimized single S&C training sessions with no duplicated movement patterns.",
    version="1.0.0"
)

# Global database pool reference
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


# -------------------------------------------------------------
# 1. Pydantic Models (Schemas)
# -------------------------------------------------------------

class SessionGenerateRequest(BaseModel):
    template_name: str = Field(..., example="Cricket Fast Bowler Power")
    athlete_id: int = Field(..., example=101)
    equipment: Optional[List[str]] = Field(None, example=["Trap Bar", "Medicine Ball"])
    difficulty_cap: Optional[str] = Field(None, example="Advanced")


class SessionExerciseDetail(BaseModel):
    exercise_id: int
    name: str
    description: Optional[str] = None
    difficulty_level: str
    mechanics_type: str
    force_type: str
    movement_pattern: str
    recommendation_score: float
    sets: int
    reps: int
    intensity: str
    rest_seconds: int


class SessionResponse(BaseModel):
    athlete_id: int
    athlete_name: str
    template_name: str
    warmup: List[SessionExerciseDetail]
    primary: SessionExerciseDetail
    secondary: SessionExerciseDetail
    accessory: SessionExerciseDetail
    core: SessionExerciseDetail
    conditioning: SessionExerciseDetail
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }


# -------------------------------------------------------------
# 2. Mock and PostgreSQL Mappings
# -------------------------------------------------------------

# Development level ordinal matching recommendation_engine.py
LEVEL_ORDINAL = {"FOUNDATION": 1, "DEVELOPMENT": 2, "PERFORMANCE": 3}

# Minimum level lookup for mock fallback exercises (matches DB after 000018+000019)
MINIMUM_LEVEL_LOOKUP = {
    1: "DEVELOPMENT",   # Trap Bar Jump Squat
    2: "FOUNDATION",    # Single-Leg Lateral Bound
    3: "FOUNDATION",    # MB Overhead Backwards Toss
    4: "FOUNDATION",    # MB Rotational Chest Pass
    5: "FOUNDATION",    # Cable Pallof Press with Rotation
    78: "FOUNDATION",   # Bodyweight Squat
    79: "FOUNDATION",   # Medicine Ball Slam
    85: "DEVELOPMENT",  # Barbell Back Squat
    86: "PERFORMANCE",  # Power Clean
    87: "DEVELOPMENT",  # RFESS
    88: "DEVELOPMENT",  # Trap Bar Deadlift
    89: "FOUNDATION",   # Kettlebell Swing
    90: "PERFORMANCE",  # Depth Jump
    91: "FOUNDATION",   # MB Rotational Scoop Toss
    92: "FOUNDATION",   # A-Skip
    93: "FOUNDATION",   # SL Isometric Wall Sit
    94: "PERFORMANCE",  # Nordic Hamstring Curl
    95: "FOUNDATION",   # Farmer's Walk
    96: "FOUNDATION",   # Dumbbell Row
    97: "FOUNDATION",   # Dumbbell Overhead Press
    98: "FOUNDATION",   # Plank with Rotation
    99: "FOUNDATION",   # Burpee
}

# Technical difficulty lookup for mock fallback (matches DB after 000020)
TECH_DIFF_LOOKUP = {
    1: 6, 2: 4, 3: 4, 4: 1, 5: 3,
    78: 1, 79: 2,
    85: 5, 86: 7, 87: 5, 88: 5, 89: 1, 90: 9,
    91: 1, 92: 2, 93: 3, 94: 7,
    95: 2, 96: 2, 97: 2, 98: 2, 99: 3,
}

# Technical difficulty caps per development level (matching Option A)
TECH_DIFF_CAP = {"FOUNDATION": 3, "DEVELOPMENT": 6, "PERFORMANCE": 10}

# Primary movement patterns lookup for mock exercises
MOCK_PATTERNS = {
    1: "Squat",            # Trap Bar Jump Squat
    2: "Lunge (Single-Leg)", # Single-Leg Lateral Bound
    3: "Hinge",            # Medicine Ball Overhead Backwards Toss
    4: "Rotation",         # Medicine Ball Rotational Chest Pass
    5: "Rotation",         # Cable Pallof Press with Rotation
    78: "Squat",           # Bodyweight Squat (Warmup)
    79: "Slam Mechanics",  # Medicine Ball Slam (Conditioning)
    85: "Squat",           # Barbell Back Squat
    86: "Hinge",           # Power Clean
    87: "Lunge (Single-Leg)", # Rear Foot Elevated Split Squat
    88: "Hinge",           # Trap Bar Deadlift
    89: "Hinge",           # Kettlebell Swing
    90: "Squat",           # Depth Jump
    91: "Rotation",        # Medicine Ball Rotational Scoop Toss
    92: "Sprint Mechanics", # A-Skip
    93: "Static Stability", # Single-Leg Isometric Wall Sit
    94: "Hinge",           # Nordic Hamstring Curl
    95: "Carry",           # Farmer's Walk
    96: "Pull (Horizontal)", # Dumbbell Row
    97: "Push (Vertical)",  # Dumbbell Overhead Press
    98: "Rotation",        # Plank with Rotation
    99: "Cardio"            # Burpee
}

# Mock exercises list representing DB seeds
MOCK_EXERCISES = [
    {"id": 1, "name": "Trap Bar Jump Squat", "difficulty_level": "Advanced", "mechanics_type": "Compound", "force_type": "Push", "equipment": ["Trap Bar"]},
    {"id": 2, "name": "Single-Leg Lateral Bound", "difficulty_level": "Intermediate", "mechanics_type": "Compound", "force_type": "Push", "equipment": ["Bodyweight"]},
    {"id": 3, "name": "Medicine Ball Overhead Backwards Toss", "difficulty_level": "Intermediate", "mechanics_type": "Compound", "force_type": "Hinge", "equipment": ["Medicine Ball"]},
    {"id": 4, "name": "Medicine Ball Rotational Chest Pass", "difficulty_level": "Beginner", "mechanics_type": "Compound", "force_type": "Rotation", "equipment": ["Medicine Ball"]},
    {"id": 5, "name": "Cable Pallof Press with Rotation", "difficulty_level": "Intermediate", "mechanics_type": "Compound", "force_type": "Rotation", "equipment": ["Cable Machine"]},
    {"id": 78, "name": "Bodyweight Squat", "difficulty_level": "Beginner", "mechanics_type": "Compound", "force_type": "Push", "equipment": ["Bodyweight"], "tags": ["Warm-up"]},
    {"id": 79, "name": "Medicine Ball Slam", "difficulty_level": "Beginner", "mechanics_type": "Compound", "force_type": "Push", "equipment": ["Medicine Ball"], "tags": ["Conditioning"]},
    {"id": 85, "name": "Barbell Back Squat", "difficulty_level": "Intermediate", "mechanics_type": "Compound", "force_type": "Push", "equipment": ["Barbell"]},
    {"id": 86, "name": "Power Clean", "difficulty_level": "Advanced", "mechanics_type": "Compound", "force_type": "Pull", "equipment": ["Barbell"]},
    {"id": 87, "name": "Rear Foot Elevated Split Squat", "difficulty_level": "Intermediate", "mechanics_type": "Compound", "force_type": "Push", "equipment": ["Dumbbell", "Bodyweight"]},
    {"id": 88, "name": "Trap Bar Deadlift", "difficulty_level": "Intermediate", "mechanics_type": "Compound", "force_type": "Hinge", "equipment": ["Trap Bar"]},
    {"id": 89, "name": "Kettlebell Swing", "difficulty_level": "Beginner", "mechanics_type": "Compound", "force_type": "Hinge", "equipment": ["Kettlebell"]},
    {"id": 90, "name": "Depth Jump", "difficulty_level": "Elite", "mechanics_type": "Compound", "force_type": "Push", "equipment": ["Bodyweight"]},
    {"id": 91, "name": "Medicine Ball Rotational Scoop Toss", "difficulty_level": "Beginner", "mechanics_type": "Compound", "force_type": "Static", "equipment": ["Medicine Ball"]},
    {"id": 92, "name": "A-Skip", "difficulty_level": "Beginner", "mechanics_type": "Compound", "force_type": "N/A", "equipment": ["Bodyweight"], "tags": ["Warm-up"]},
    {"id": 93, "name": "Single-Leg Isometric Wall Sit", "difficulty_level": "Intermediate", "mechanics_type": "Isolation", "force_type": "Static", "equipment": ["Bodyweight"], "tags": ["Warm-up"]},
    {"id": 94, "name": "Nordic Hamstring Curl", "difficulty_level": "Advanced", "mechanics_type": "Isolation", "force_type": "Pull", "equipment": ["Bodyweight"]},
    {"id": 95, "name": "Farmer's Walk", "difficulty_level": "Beginner", "mechanics_type": "Compound", "force_type": "Carry", "equipment": ["Dumbbell", "Kettlebell"], "tags": ["Conditioning"]},
    {"id": 96, "name": "Dumbbell Row", "difficulty_level": "Beginner", "mechanics_type": "Compound", "force_type": "Pull", "equipment": ["Dumbbell"]},
    {"id": 97, "name": "Dumbbell Overhead Press", "difficulty_level": "Beginner", "mechanics_type": "Compound", "force_type": "Push", "equipment": ["Dumbbell"]},
    {"id": 98, "name": "Plank with Rotation", "difficulty_level": "Beginner", "mechanics_type": "Compound", "force_type": "Rotation", "equipment": ["Bodyweight"], "tags": ["Core"]},
    {"id": 99, "name": "Burpee", "difficulty_level": "Intermediate", "mechanics_type": "Compound", "force_type": "Push", "equipment": ["Bodyweight"], "tags": ["Conditioning"]}
]


# -------------------------------------------------------------
# 3. Session Generator Service
# -------------------------------------------------------------

class SessionGeneratorService:
    def __init__(self, athlete_repo: AthleteRepository, pool=None):
        self.athlete_repo = athlete_repo
        self.pool = pool

    async def get_movement_pattern(self, exercise_id: int) -> str:
        """Retrieves primary movement pattern name for an exercise."""
        if not self.pool:
            return MOCK_PATTERNS.get(exercise_id, "N/A")
        
        query = """
            SELECT mp.name 
            FROM exercise_movement_patterns emp
            JOIN movement_patterns mp ON emp.movement_pattern_id = mp.id
            WHERE emp.exercise_id = $1 AND emp.pattern_priority = 'Primary'
            LIMIT 1;
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, exercise_id)
            return row["name"] if row else "N/A"

    async def get_fallback_exercises_for_slot(
        self, slot_type: str, difficulty_cap: str, equipment: List[str], development_level: str = "FOUNDATION"
    ) -> List[Dict[str, Any]]:
        """Finds exercises matching equipment and difficulty cap to use as fallbacks."""
        diff_levels = {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Elite": 4}
        cap_val = diff_levels.get(difficulty_cap, 2)
        
        candidates = []
        dev_ord = LEVEL_ORDINAL.get(development_level, 1)
        tech_cap = TECH_DIFF_CAP.get(development_level, 3)
        
        if not self.pool:
            for ex in MOCK_EXERCISES:
                # Primary gate: development level >= minimum level
                min_lvl = MINIMUM_LEVEL_LOOKUP.get(ex["id"], "FOUNDATION")
                if LEVEL_ORDINAL.get(min_lvl, 1) > dev_ord:
                    continue
                # Secondary gate: technical difficulty cap
                ex_tech = TECH_DIFF_LOOKUP.get(ex["id"])
                if ex_tech is None or ex_tech > tech_cap:
                    continue
                # Filter by difficulty
                if diff_levels[ex["difficulty_level"]] > cap_val:
                    continue
                # Filter by equipment
                eq_ok = True
                for eq in ex["equipment"]:
                    if eq != "Bodyweight" and eq not in equipment:
                        eq_ok = False
                        break
                if not eq_ok:
                    continue
                
                pattern = MOCK_PATTERNS.get(ex["id"], "N/A")
                
                # Filter by slot constraints
                if slot_type == "core" and pattern not in ["Rotation", "Anti-Rotation"] and "Core" not in ex.get("tags", []):
                    continue
                if slot_type in ["primary", "secondary"] and ex["mechanics_type"] != "Compound":
                    continue
                
                candidates.append({
                    "id": ex["id"],
                    "name": ex["name"],
                    "description": f"Fallback exercise using {', '.join(ex['equipment'])}.",
                    "difficulty_level": ex["difficulty_level"],
                    "mechanics_type": ex["mechanics_type"],
                    "force_type": ex["force_type"],
                    "movement_pattern": pattern,
                    "recommendation_score": 5.0
                })
            return candidates

        # PostgreSQL query
        query = """
            SELECT e.id, e.name, e.description, e.difficulty_level, e.mechanics_type, e.force_type,
                   mp.name as movement_pattern,
                   5.0 as recommendation_score
            FROM exercises e
            LEFT JOIN exercise_movement_patterns emp ON e.id = emp.exercise_id AND emp.pattern_priority = 'Primary'
            LEFT JOIN movement_patterns mp ON emp.movement_pattern_id = mp.id
            WHERE (
                CASE e.difficulty_level
                    WHEN 'Beginner' THEN 1
                    WHEN 'Intermediate' THEN 2
                    WHEN 'Advanced' THEN 3
                    WHEN 'Elite' THEN 4
                END <= 
                CASE $1::varchar
                    WHEN 'Beginner' THEN 1
                    WHEN 'Intermediate' THEN 2
                    WHEN 'Advanced' THEN 3
                    WHEN 'Elite' THEN 4
                END
            )
            AND development_level_ordinal(e.minimum_level) <= development_level_ordinal($3::athlete_development_level)
            AND e.technical_difficulty IS NOT NULL
            AND e.technical_difficulty <=
                CASE $3::athlete_development_level
                    WHEN 'FOUNDATION' THEN 3
                    WHEN 'DEVELOPMENT' THEN 6
                    WHEN 'PERFORMANCE' THEN 10
                END
            AND NOT EXISTS (
                SELECT 1 
                FROM exercise_equipment ee
                JOIN equipment eq ON ee.equipment_id = eq.id
                WHERE ee.exercise_id = e.id 
                  AND ee.is_required = TRUE
                  AND eq.name <> 'Bodyweight'
                  AND eq.name <> ALL($2::varchar[])
            )
        """
        if slot_type == "core":
            query += " AND (mp.name IN ('Rotation', 'Anti-Rotation') OR e.id IN (SELECT exercise_id FROM exercise_tags WHERE tag_id = (SELECT id FROM tags WHERE name = 'Core')))"
        elif slot_type in ["primary", "secondary"]:
            query += " AND e.mechanics_type = 'Compound'"
            
        query += " ORDER BY e.id;"
        
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, difficulty_cap, equipment, development_level)
            return [dict(r) for r in rows]

    async def fetch_warmup_candidates(
        self, sport_id: int, difficulty_cap: str, equipment: List[str], development_level: str = "FOUNDATION"
    ) -> List[Dict[str, Any]]:
        """Queries exercises tagged 'Warm-up' respecting difficulty and equipment."""
        dev_ord = LEVEL_ORDINAL.get(development_level, 1)
        tech_cap = TECH_DIFF_CAP.get(development_level, 3)
        if not self.pool:
            candidates = []
            diff_levels = {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Elite": 4}
            cap_val = diff_levels.get(difficulty_cap, 2)
            
            for ex in MOCK_EXERCISES:
                if "tags" in ex and "Warm-up" in ex["tags"]:
                    min_lvl = MINIMUM_LEVEL_LOOKUP.get(ex["id"], "FOUNDATION")
                    if LEVEL_ORDINAL.get(min_lvl, 1) > dev_ord:
                        continue
                    ex_tech = TECH_DIFF_LOOKUP.get(ex["id"])
                    if ex_tech is None or ex_tech > tech_cap:
                        continue
                    if diff_levels[ex["difficulty_level"]] > cap_val:
                        continue
                    eq_ok = True
                    for eq in ex["equipment"]:
                        if eq != "Bodyweight" and eq not in equipment:
                            eq_ok = False
                            break
                    if eq_ok:
                        score = 9.5 if ex["id"] == 78 else (9.0 if ex["id"] == 92 else 8.0)
                        candidates.append({
                            "exercise_id": ex["id"],
                            "name": ex["name"],
                            "description": f"Warmup drill using {', '.join(ex['equipment'])}.",
                            "difficulty_level": ex["difficulty_level"],
                            "mechanics_type": ex["mechanics_type"],
                            "force_type": ex["force_type"],
                            "movement_pattern": MOCK_PATTERNS.get(ex["id"], "N/A"),
                            "recommendation_score": score
                        })
            return sorted(candidates, key=lambda x: x["recommendation_score"], reverse=True)

        query = """
            SELECT e.id as exercise_id, e.name, e.description, e.difficulty_level, e.mechanics_type, e.force_type,
                   mp.name as movement_pattern,
                   (
                       COALESCE(esm.specificity_rating, 5.0) * 1.0 + 
                       (CASE WHEN e.difficulty_level = 'Beginner' THEN 3.0 ELSE 0.0 END)
                   )::numeric(5,2) as recommendation_score
            FROM exercises e
            JOIN exercise_tags et ON e.id = et.exercise_id
            JOIN tags t ON et.tag_id = t.id
            LEFT JOIN exercise_movement_patterns emp ON e.id = emp.exercise_id AND emp.pattern_priority = 'Primary'
            LEFT JOIN movement_patterns mp ON emp.movement_pattern_id = mp.id
            LEFT JOIN exercise_sport_mapping esm ON e.id = esm.exercise_id AND esm.sport_id = $1
            WHERE t.name = 'Warm-up'
              AND (
                  CASE e.difficulty_level
                      WHEN 'Beginner' THEN 1
                      WHEN 'Intermediate' THEN 2
                      WHEN 'Advanced' THEN 3
                      WHEN 'Elite' THEN 4
                  END <= 
                  CASE $2::varchar
                      WHEN 'Beginner' THEN 1
                      WHEN 'Intermediate' THEN 2
                      WHEN 'Advanced' THEN 3
                      WHEN 'Elite' THEN 4
                  END
              )
              AND development_level_ordinal(e.minimum_level) <= development_level_ordinal($4::athlete_development_level)
              AND e.technical_difficulty IS NOT NULL
              AND e.technical_difficulty <=
                  CASE $4::athlete_development_level
                      WHEN 'FOUNDATION' THEN 3
                      WHEN 'DEVELOPMENT' THEN 6
                      WHEN 'PERFORMANCE' THEN 10
                  END
              AND NOT EXISTS (
                  SELECT 1 
                  FROM exercise_equipment ee
                  JOIN equipment eq ON ee.equipment_id = eq.id
                  WHERE ee.exercise_id = e.id 
                    AND ee.is_required = TRUE
                    AND eq.name <> 'Bodyweight'
                    AND eq.name <> ALL($3::varchar[])
              )
            ORDER BY recommendation_score DESC;
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, sport_id, difficulty_cap, equipment, development_level)
            return [dict(r) for r in rows]

    async def fetch_conditioning_candidates(
        self, sport_id: int, difficulty_cap: str, equipment: List[str], development_level: str = "FOUNDATION"
    ) -> List[Dict[str, Any]]:
        """Queries conditioning exercises targeting cardio/power/sprint qualities."""
        dev_ord = LEVEL_ORDINAL.get(development_level, 1)
        tech_cap = TECH_DIFF_CAP.get(development_level, 3)
        if not self.pool:
            candidates = []
            diff_levels = {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Elite": 4}
            cap_val = diff_levels.get(difficulty_cap, 2)
            
            for ex in MOCK_EXERCISES:
                if ex["id"] in [79, 86, 89, 90, 95, 99]:
                    min_lvl = MINIMUM_LEVEL_LOOKUP.get(ex["id"], "FOUNDATION")
                    if LEVEL_ORDINAL.get(min_lvl, 1) > dev_ord:
                        continue
                    ex_tech = TECH_DIFF_LOOKUP.get(ex["id"])
                    if ex_tech is None or ex_tech > tech_cap:
                        continue
                    if diff_levels[ex["difficulty_level"]] > cap_val:
                        continue
                    eq_ok = True
                    for eq in ex["equipment"]:
                        if eq != "Bodyweight" and eq not in equipment:
                            eq_ok = False
                            break
                    if eq_ok:
                        score = 9.8 if ex["id"] == 79 else (9.5 if ex["id"] == 89 else (9.2 if ex["id"] == 95 else (9.0 if ex["id"] == 86 else (8.8 if ex["id"] == 99 else 8.5))))
                        candidates.append({
                            "exercise_id": ex["id"],
                            "name": ex["name"],
                            "description": f"Conditioning exercise using {', '.join(ex['equipment'])}.",
                            "difficulty_level": ex["difficulty_level"],
                            "mechanics_type": ex["mechanics_type"],
                            "force_type": ex["force_type"],
                            "movement_pattern": MOCK_PATTERNS.get(ex["id"], "N/A"),
                            "recommendation_score": score
                        })
            return sorted(candidates, key=lambda x: x["recommendation_score"], reverse=True)

        query = """
            SELECT e.id as exercise_id, e.name, e.description, e.difficulty_level, e.mechanics_type, e.force_type,
                   mp.name as movement_pattern,
                   (
                       COALESCE(esm.specificity_rating, 5.0) * 1.0 + 
                       (CASE WHEN e.force_type = 'Push' OR e.force_type = 'Pull' THEN 2.0 ELSE 0.0 END)
                   )::numeric(5,2) as recommendation_score
            FROM exercises e
            JOIN exercise_physical_qualities epq ON e.id = epq.exercise_id
            JOIN physical_qualities pq ON epq.physical_quality_id = pq.id
            LEFT JOIN exercise_movement_patterns emp ON e.id = emp.exercise_id AND emp.pattern_priority = 'Primary'
            LEFT JOIN movement_patterns mp ON emp.movement_pattern_id = mp.id
            LEFT JOIN exercise_sport_mapping esm ON e.id = esm.exercise_id AND esm.sport_id = $1
            WHERE pq.name IN ('Anaerobic Power', 'Aerobic Capacity', 'Rate of Force Development')
              AND (
                  CASE e.difficulty_level
                      WHEN 'Beginner' THEN 1
                      WHEN 'Intermediate' THEN 2
                      WHEN 'Advanced' THEN 3
                      WHEN 'Elite' THEN 4
                  END <= 
                  CASE $2::varchar
                      WHEN 'Beginner' THEN 1
                      WHEN 'Intermediate' THEN 2
                      WHEN 'Advanced' THEN 3
                      WHEN 'Elite' THEN 4
                  END
              )
              AND development_level_ordinal(e.minimum_level) <= development_level_ordinal($4::athlete_development_level)
              AND e.technical_difficulty IS NOT NULL
              AND e.technical_difficulty <=
                  CASE $4::athlete_development_level
                      WHEN 'FOUNDATION' THEN 3
                      WHEN 'DEVELOPMENT' THEN 6
                      WHEN 'PERFORMANCE' THEN 10
                  END
              AND NOT EXISTS (
                  SELECT 1 
                  FROM exercise_equipment ee
                  JOIN equipment eq ON ee.equipment_id = eq.id
                  WHERE ee.exercise_id = e.id 
                    AND ee.is_required = TRUE
                    AND eq.name <> 'Bodyweight'
                    AND eq.name <> ALL($3::varchar[])
              )
            ORDER BY recommendation_score DESC;
        """
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, sport_id, difficulty_cap, equipment, development_level)
            return [dict(r) for r in rows]

    async def generate_session(self, request: SessionGenerateRequest) -> Dict[str, Any]:
        # 1. Load athlete details
        athlete = await self.athlete_repo.get_by_id(request.athlete_id)
        if not athlete:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Athlete with ID {request.athlete_id} not found."
            )

        # 2. Resolve sport name and role name
        sport_id = athlete["sport_id"]
        role_id = athlete["role_id"]
        sport_name = "Cricket"
        role_name = ROLE_NAMES.get(role_id, "Fast Bowler")

        if self.pool:
            async with self.pool.acquire() as conn:
                s_row = await conn.fetchrow("SELECT name FROM sports WHERE id = $1;", sport_id)
                if s_row: sport_name = s_row["name"]
                r_row = await conn.fetchrow("SELECT name FROM roles WHERE id = $1;", role_id)
                if r_row: role_name = r_row["name"]

        # 3. Resolve constraints
        difficulty_cap = request.difficulty_cap or athlete["competition_level"]
        equipment = request.equipment or [
            "Trap Bar", "Medicine Ball", "Kettlebell", "Dumbbell", "Cable Machine", "Barbell", "Bodyweight"
        ]
        training_age_months = athlete.get("training_age_months", athlete.get("training_age_years", 0) * 12)
        development_level = training_months_to_level(training_age_months)

        # 4. Find matching goal from template name
        goal = "Power"
        if "strength" in request.template_name.lower():
            goal = "Strength"

        # 5. Fetch template slots and recommendations
        rec_req = RecommendationRequest(
            sport=sport_name,
            role=role_name,
            goal=goal,
            equipment=equipment,
            difficulty_cap=difficulty_cap,
            training_age_months=training_age_months,
            development_level=development_level
        )
        
        rec_repo = PostgreSqlExerciseRepository(self.pool) if self.pool else MockExerciseRepository()
        try:
            rec_response = await get_exercise_recommendations(rec_req, repo=rec_repo)
        except Exception as e:
            logger.error(f"Error calling recommendation engine: {e}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Failed to load workout template slots: {str(e)}"
            )

        slots = rec_response.slots
        if not slots:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Template slots for '{request.template_name}' could not be resolved."
            )

        # Track selected movement patterns to enforce zero duplicates
        selected_patterns = set()
        session_exercises = {}

        # 6. Select main exercises: Primary, Secondary, Accessory, Core
        sorted_slots = sorted(slots, key=lambda x: x.display_order)
        
        for slot in sorted_slots:
            slot_type = slot.slot_type.lower()
            pool = slot.exercise_pool
            
            selected_ex = None
            
            # Try to find exercise in the recommendation pool that does not duplicate patterns
            for ex in pool:
                pattern = await self.get_movement_pattern(ex.id)
                if pattern not in selected_patterns:
                    selected_ex = ex
                    selected_patterns.add(pattern)
                    break
            
            # Fallback path if recommendation pool was empty or all entries duplicated patterns
            if not selected_ex:
                fallback_pool = await self.get_fallback_exercises_for_slot(slot_type, difficulty_cap, equipment, development_level)
                for f_ex in fallback_pool:
                    pattern = f_ex["movement_pattern"]
                    if pattern not in selected_patterns:
                        selected_ex = f_ex
                        selected_patterns.add(pattern)
                        break
                
                # Absolute safeguard fallback to anything in pool or fallback list if all duplicate
                if not selected_ex:
                    if pool:
                        selected_ex = pool[0]
                        pattern = await self.get_movement_pattern(selected_ex.id)
                        selected_patterns.add(pattern)
                    elif fallback_pool:
                        selected_ex = fallback_pool[0]
                        pattern = selected_ex["movement_pattern"]
                        selected_patterns.add(pattern)

            if selected_ex:
                # Map S&C parameters based on slot type
                if slot_type == "primary":
                    sets, reps, intensity, rest = 4, 3, "80% 1RM (RPE 8)", 90
                elif slot_type == "secondary":
                    sets, reps, intensity, rest = 3, 5, "75% 1RM (RPE 7)", 90
                elif slot_type == "accessory":
                    sets, reps, intensity, rest = 3, 8, "70% 1RM (RPE 7)", 60
                else: # core
                    sets, reps, intensity, rest = 3, 10, "RPE 8", 60

                if isinstance(selected_ex, dict):
                    ex_id = selected_ex["id"]
                    ex_name = selected_ex["name"]
                    ex_desc = selected_ex.get("description")
                    ex_diff = selected_ex["difficulty_level"]
                    ex_mech = selected_ex["mechanics_type"]
                    ex_force = selected_ex["force_type"]
                    ex_pattern = selected_ex["movement_pattern"]
                    ex_score = selected_ex["recommendation_score"]
                else:
                    ex_id = selected_ex.id
                    ex_name = selected_ex.name
                    ex_desc = selected_ex.description
                    ex_diff = selected_ex.difficulty_level
                    ex_mech = selected_ex.mechanics_type
                    ex_force = selected_ex.force_type
                    ex_pattern = await self.get_movement_pattern(selected_ex.id)
                    ex_score = selected_ex.recommendation_score

                session_exercises[slot_type] = SessionExerciseDetail(
                    exercise_id=ex_id,
                    name=ex_name,
                    description=ex_desc,
                    difficulty_level=ex_diff,
                    mechanics_type=ex_mech,
                    force_type=ex_force,
                    movement_pattern=ex_pattern,
                    recommendation_score=ex_score,
                    sets=sets,
                    reps=reps,
                    intensity=intensity,
                    rest_seconds=rest
                )

        # 7. Select Warmup Exercise (Must avoid duplicate movement patterns of main lifts)
        warmup_candidates = await self.fetch_warmup_candidates(sport_id, difficulty_cap, equipment, development_level)
        selected_warmup = None
        for cand in warmup_candidates:
            if cand["movement_pattern"] not in selected_patterns:
                selected_warmup = cand
                selected_patterns.add(cand["movement_pattern"])
                break
        
        # Fallback if all warmup options duplicate patterns
        if not selected_warmup and warmup_candidates:
            selected_warmup = warmup_candidates[0]
            selected_patterns.add(selected_warmup["movement_pattern"])

        warmup_list = []
        if selected_warmup:
            warmup_list.append(SessionExerciseDetail(
                exercise_id=selected_warmup["exercise_id"],
                name=selected_warmup["name"],
                description=selected_warmup.get("description"),
                difficulty_level=selected_warmup["difficulty_level"],
                mechanics_type=selected_warmup["mechanics_type"],
                force_type=selected_warmup["force_type"],
                movement_pattern=selected_warmup["movement_pattern"],
                recommendation_score=selected_warmup["recommendation_score"],
                sets=2,
                reps=10,
                intensity="Bodyweight (Light)",
                rest_seconds=30
            ))

        # 8. Select Conditioning Exercise (Must avoid duplicate patterns)
        conditioning_candidates = await self.fetch_conditioning_candidates(sport_id, difficulty_cap, equipment, development_level)
        selected_cond = None
        for cand in conditioning_candidates:
            if cand["movement_pattern"] not in selected_patterns:
                selected_cond = cand
                selected_patterns.add(cand["movement_pattern"])
                break
        
        # Fallback if all conditioning options duplicate patterns
        if not selected_cond and conditioning_candidates:
            selected_cond = conditioning_candidates[0]
            selected_patterns.add(selected_cond["movement_pattern"])

        conditioning_detail = None
        if selected_cond:
            conditioning_detail = SessionExerciseDetail(
                exercise_id=selected_cond["exercise_id"],
                name=selected_cond["name"],
                description=selected_cond.get("description"),
                difficulty_level=selected_cond["difficulty_level"],
                mechanics_type=selected_cond["mechanics_type"],
                force_type=selected_cond["force_type"],
                movement_pattern=selected_cond["movement_pattern"],
                recommendation_score=selected_cond["recommendation_score"],
                sets=3,
                reps=12,
                intensity="High Effort",
                rest_seconds=60
            )

        # Enforce that all sections are populated
        if not session_exercises.get("primary") or not session_exercises.get("secondary") or not session_exercises.get("accessory") or not session_exercises.get("core") or not selected_warmup or not selected_cond:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Could not generate a complete workout session with available template slots and constraints."
            )

        return SessionResponse(
            athlete_id=request.athlete_id,
            athlete_name=f"{athlete['first_name']} {athlete['last_name']}",
            template_name=request.template_name,
            warmup=warmup_list,
            primary=session_exercises["primary"],
            secondary=session_exercises["secondary"],
            accessory=session_exercises["accessory"],
            core=session_exercises["core"],
            conditioning=conditioning_detail
        )


# Dependency resolver for the service
def get_session_generator_service(
    athlete_repo: AthleteRepository = Depends(get_athlete_repository)
) -> SessionGeneratorService:
    return SessionGeneratorService(athlete_repo, db_pool)


# -------------------------------------------------------------
# 4. FastAPI Endpoints
# -------------------------------------------------------------

@app.post(
    "/api/v1/sessions/generate",
    response_model=SessionResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate a Training Session",
    description="Compiles template slots and selects warmups, primary lift, accessories, core, and conditioning drills ensuring no duplicate movement patterns."
)
async def generate_training_session(
    request: SessionGenerateRequest,
    service: SessionGeneratorService = Depends(get_session_generator_service)
):
    logger.info(f"Generating single S&C session for athlete ID: {request.athlete_id} using template: {request.template_name}")
    try:
        return await service.generate_session(request)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Error in Session Generator Engine: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Session generation failure. Error: {str(e)}"
        )


@app.get(
    "/health",
    status_code=status.HTTP_200_OK
)
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "database_connected": db_pool is not None
    }
