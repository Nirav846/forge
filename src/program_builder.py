# Forge Program Builder V1
# Role: Principal Performance Architect
# Description: Production-grade FastAPI service layer, Pydantic schema validation,
# and relational database repository layer for generating 4-week training programs.

import os
import re
import uuid
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import asyncio

from fastapi import FastAPI, HTTPException, Depends, Query, status
from pydantic import BaseModel, Field

# Imports from existing modules
from athlete_module import get_athlete_repository, AthleteRepository, ROLE_NAMES
from assessment_entry_module import get_results_repository, AssessmentResultRepository
from deficit_detection_engine import DeficitDetectionService, MockBenchmarkRepository, PostgreSqlBenchmarkRepository
import athlete_module as _athlete_module
import assessment_entry_module as _assessment_module
from recommendation_engine import (
    MockExerciseRepository,
    PostgreSqlExerciseRepository,
    RecommendationRequest,
    get_exercise_recommendations,
    training_months_to_level
)
from exercise_substitution_engine import get_substitutions
from exercise_classification import classify_exercise, determine_primary_adaptation, determine_force_vector

# Setup logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("forge-program-builder")

app = FastAPI(
    title="Forge Program Builder V1",
    description="Generates, retrieves, and manages 4-week structured S&C training programs with weekly progressions.",
    version="1.0.0"
)

# Global pool variable for database connection lifecycle
db_pool = None

# Feature flag: use default_exercise from template slots instead of pool rotation
USE_DEFAULT_EXERCISE = os.getenv("USE_DEFAULT_EXERCISE", "false").lower() in ("1", "true", "yes")

# In-memory staged program store
_staged_programs: Dict[str, Dict[str, Any]] = {}

@app.on_event("startup")
async def startup_event():
    global db_pool
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        import asyncpg
        try:
            db_pool = await asyncpg.create_pool(db_url)
            logger.info("Successfully connected to PostgreSQL connection pool.")
            _athlete_module.db_pool = db_pool
            _assessment_module.db_pool = db_pool
            logger.info("Shared db_pool with athlete_module and assessment_entry_module.")
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

class ProgramGenerateRequest(BaseModel):
    athlete_id: int = Field(..., example=101)
    sessions_per_week: int = Field(..., ge=2, le=4, example=3)
    name: Optional[str] = Field(None, example="4-Week Power Block")
    goal: Optional[str] = Field(None, example="Power")
    equipment: Optional[List[str]] = Field(None, example=["Trap Bar", "Medicine Ball"])
    difficulty_cap: Optional[str] = Field(None, example="Advanced")


class ProgramExerciseResponse(BaseModel):
    id: int
    exercise_id: int
    name: str
    description: Optional[str] = None
    difficulty_level: str
    mechanics_type: str
    force_type: str
    display_order: int
    sets: int
    reps: int
    intensity: str
    rest_seconds: int


class ProgramSessionResponse(BaseModel):
    id: int
    session_number: int
    exercises: List[ProgramExerciseResponse]


class ProgramWeekResponse(BaseModel):
    id: int
    week_number: int
    focus: str
    sessions: List[ProgramSessionResponse]


class ProgramResponse(BaseModel):
    id: int
    athlete_id: int
    name: str
    goal: str
    sessions_per_week: int
    weeks: List[ProgramWeekResponse]
    created_at: datetime
    updated_at: datetime

    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }


class StageRequest(BaseModel):
    athlete_id: int = Field(..., example=101)
    sessions_per_week: int = Field(..., ge=2, le=4, example=3)
    name: Optional[str] = Field(None, example="4-Week Power Block")
    goal: Optional[str] = Field(None, example="Power")
    equipment: Optional[List[str]] = Field(None, example=["Trap Bar", "Medicine Ball"])
    difficulty_cap: Optional[str] = Field(None, example="Advanced")
    use_default_exercise: Optional[bool] = Field(None, description="Override USE_DEFAULT_EXERCISE feature flag for this request")


class ConfirmRequest(BaseModel):
    stage_id: str = Field(..., example="uuid-string")


class StagedProgramResponse(BaseModel):
    stage_id: str
    status: str
    athlete_id: int
    name: str
    goal: str
    sessions_per_week: int
    week_count: int
    created_at: datetime

    model_config = {
        "json_encoders": {
            datetime: lambda v: v.isoformat()
        }
    }


class SwapPreviewRequest(BaseModel):
    stage_id: str = Field(..., example="uuid-string")
    slot_id: int = Field(..., example=201)
    target_exercise_id: int = Field(..., example=501)


class SwapWeekDetail(BaseModel):
    week_number: int
    session_number: int
    exercise_id: int
    name: str
    exercise_class: Optional[str] = None
    sets: int
    reps: int
    intensity: str
    rest_seconds: int


class SwapPreviewResponse(BaseModel):
    unchanged: bool
    current_exercise_name: str
    new_exercise_name: str
    reason: str
    weeks: List[SwapWeekDetail]


class CoachOverrideEntry(BaseModel):
    stage_id: str
    slot_id: int
    original_exercise_id: int
    selected_exercise_id: int
    override_reason: Optional[str] = None
    overridden_by: Optional[str] = None


# In-memory coach override store (indexed by stage_id -> slot_id -> entry)
_coach_overrides: Dict[str, Dict[int, CoachOverrideEntry]] = {}


# -------------------------------------------------------------
# 2. S&C Progression Rules Helper
# -------------------------------------------------------------

def parse_baseline_reps(volume_target: str, slot_type: str) -> int:
    """Parses baseline reps from a template's volume string (e.g. '3x5' -> 5) or returns defaults."""
    if volume_target:
        # Match pattern like "3x5" or "4x6"
        match = re.search(r"\d+x(\d+)", volume_target)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                pass
    
    # Default fallbacks per slot type
    defaults = {
        "Primary": 5,
        "Secondary": 6,
        "Accessory": 8,
        "Core": 10
    }
    return defaults.get(slot_type, 8)


def calculate_reps_and_intensity(
    week_num: int,
    baseline_reps: int,
    exercise_class: str = "Max Strength",
    force_type: str = "Push",
    slot_type: str = "Primary",
    exercise_name: str = ""
) -> tuple[int, int, str, int]:
    """
    Computes sets, reps, intensity, and rest periods for a given week
    using exercise_class metadata instead of fragile name-based matching.
    """
    # Normalize
    cls = exercise_class.lower() if exercise_class else ""
    force_lower = force_type.lower()
    slot_lower = slot_type.lower()

    # Determine base sets per week
    if week_num == 1:
        sets = 3
    elif week_num == 2:
        sets = 4
    elif week_num == 3:
        sets = 4
    elif week_num == 4:
        sets = 2
    else:
        raise ValueError("Only 4-week programs are supported.")

    # Determine rest period (peak week gets extended rest for heavy)
    is_explosive = cls in ("plyometric", "sprint drill", "medicine ball", "accessory", "isometric", "core stability")
    rest_seconds = 120 if (week_num == 3 and not is_explosive) else 90

    # Branch on exercise_class
    if cls == "olympic lift":
        reps = baseline_reps if week_num != 3 else max(2, baseline_reps - 2)
        intensity_map = {
            1: "70% 1RM (Velocity Focus, RPE 7)",
            2: "75% 1RM (Velocity Focus, RPE 8)",
            3: "80% 1RM (Peak Power, RPE 9)",
            4: "60% 1RM (Technique / Deload, RPE 6)"
        }
        intensity = intensity_map[week_num]
        return sets, reps, intensity, rest_seconds

    elif cls == "ballistic":
        reps = baseline_reps if week_num != 3 else max(2, baseline_reps - 2)
        intensity_map = {
            1: "30% 1RM (Max Velocity, RPE 7)",
            2: "35% 1RM (Max Velocity, RPE 8)",
            3: "40% 1RM (Max Velocity, RPE 9)",
            4: "30% 1RM (Deload Velocity, RPE 6)"
        }
        intensity = intensity_map[week_num]
        return sets, reps, intensity, rest_seconds

    elif cls == "medicine ball":
        reps = baseline_reps if week_num != 3 else max(2, baseline_reps - 2)
        intensity_map = {
            1: "Max Effort (2-4 kg)",
            2: "Max Effort (2-4 kg)",
            3: "Max Effort (3-5 kg)",
            4: "Light Effort (2-3 kg)"
        }
        intensity = intensity_map[week_num]
        return sets, reps, intensity, rest_seconds

    elif cls == "plyometric":
        reps = baseline_reps if week_num != 3 else max(2, baseline_reps - 2)
        intensity_map = {
            1: "Bodyweight (Max Distance/Height, RPE 7)",
            2: "Bodyweight (Max Distance/Height, RPE 8)",
            3: "Bodyweight (Max Distance/Height, RPE 9)",
            4: "Bodyweight (RPE 6)"
        }
        intensity = intensity_map[week_num]
        return sets, reps, intensity, rest_seconds

    elif cls == "isometric":
        reps = baseline_reps
        intensity_map = {
            1: "Bodyweight (Max Tension, RPE 7)",
            2: "Bodyweight (Max Tension, RPE 8)",
            3: "Bodyweight (Max Tension, RPE 9)",
            4: "Bodyweight (RPE 6)"
        }
        intensity = intensity_map[week_num]
        return sets, reps, intensity, rest_seconds

    elif cls == "sprint drill":
        reps = baseline_reps
        intensity_map = {
            1: "Max Velocity, RPE 7",
            2: "Max Velocity, RPE 8",
            3: "Max Velocity, RPE 9",
            4: "Submax Technique, RPE 6"
        }
        intensity = intensity_map[week_num]
        return sets, reps, intensity, rest_seconds

    elif cls == "core stability":
        reps = baseline_reps
        intensity_map = {
            1: "Controlled Tempo, RPE 7",
            2: "Controlled Tempo, RPE 8",
            3: "Max Tension, RPE 9",
            4: "Controlled Tempo, RPE 6"
        }
        intensity = intensity_map[week_num]
        return sets, reps, intensity, rest_seconds

    # Max Strength, Ballistic, Accessory — standard lifting progression
    else:
        reps = baseline_reps if week_num != 3 else max(2, baseline_reps - 2)
        intensity_map = {
            1: "75% 1RM (RPE 7)",
            2: "80% 1RM (RPE 8)",
            3: "85% 1RM (RPE 9)",
            4: "60% 1RM (RPE 6)"
        }
        intensity = intensity_map[week_num]
        return sets, reps, intensity, rest_seconds



# -------------------------------------------------------------
# 3. Repository Interface & Implementations
# -------------------------------------------------------------

class ProgramRepository:
    """Interface for Program database operations."""
    async def create_program(self, program_data: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError()

    async def get_by_id(self, program_id: int) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    async def delete_program(self, program_id: int) -> bool:
        raise NotImplementedError()


class MockProgramRepository(ProgramRepository):
    """In-memory program repository for offline execution."""
    def __init__(self):
        self.programs: Dict[int, Dict[str, Any]] = {}
        self.counter = 1

    async def create_program(self, program_data: Dict[str, Any]) -> Dict[str, Any]:
        program_id = self.counter
        self.counter += 1
        
        now = datetime.utcnow()
        program_record = {
            "id": program_id,
            "athlete_id": program_data["athlete_id"],
            "name": program_data["name"],
            "goal": program_data["goal"],
            "sessions_per_week": program_data["sessions_per_week"],
            "created_at": now,
            "updated_at": now,
            "weeks": []
        }

        week_id_counter = 100 * program_id
        session_id_counter = 1000 * program_id
        exercise_id_counter = 10000 * program_id

        for w_data in program_data["weeks"]:
            week_record = {
                "id": week_id_counter,
                "week_number": w_data["week_number"],
                "focus": w_data["focus"],
                "sessions": []
            }
            week_id_counter += 1
            
            for s_data in w_data["sessions"]:
                session_record = {
                    "id": session_id_counter,
                    "session_number": s_data["session_number"],
                    "exercises": []
                }
                session_id_counter += 1
                
                for ex_data in s_data["exercises"]:
                    ex_record = {
                        "id": exercise_id_counter,
                        "exercise_id": ex_data["exercise_id"],
                        "name": ex_data["name"],
                        "description": ex_data.get("description"),
                        "difficulty_level": ex_data["difficulty_level"],
                        "mechanics_type": ex_data["mechanics_type"],
                        "force_type": ex_data["force_type"],
                        "display_order": ex_data["display_order"],
                        "sets": ex_data["sets"],
                        "reps": ex_data["reps"],
                        "intensity": ex_data["intensity"],
                        "rest_seconds": ex_data["rest_seconds"]
                    }
                    exercise_id_counter += 1
                    session_record["exercises"].append(ex_record)
                week_record["sessions"].append(session_record)
            program_record["weeks"].append(week_record)

        self.programs[program_id] = program_record
        return program_record

    async def get_by_id(self, program_id: int) -> Optional[Dict[str, Any]]:
        return self.programs.get(program_id)

    async def delete_program(self, program_id: int) -> bool:
        if program_id in self.programs:
            del self.programs[program_id]
            return True
        return False


class PostgreSqlProgramRepository(ProgramRepository):
    """PostgreSQL production execution repository using asyncpg connection logic."""
    def __init__(self, pool=None):
        self.pool = pool

    async def create_program(self, program_data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.pool:
            raise RuntimeError("Database pool not initialized.")

        query_program = """
            INSERT INTO programs (athlete_id, name, goal, sessions_per_week)
            VALUES ($1, $2, $3, $4)
            RETURNING id, athlete_id, name, goal, sessions_per_week, created_at, updated_at;
        """
        query_week = """
            INSERT INTO program_weeks (program_id, week_number, focus)
            VALUES ($1, $2, $3)
            RETURNING id, program_id, week_number, focus;
        """
        query_session = """
            INSERT INTO program_sessions (week_id, session_number)
            VALUES ($1, $2)
            RETURNING id, week_id, session_number;
        """
        query_exercise = """
            INSERT INTO program_session_exercises (session_id, exercise_id, display_order, sets, reps, intensity, rest_seconds)
            VALUES ($1, $2, $3, $4, $5, $6, $7)
            RETURNING id, session_id, exercise_id, display_order, sets, reps, intensity, rest_seconds;
        """

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                # 1. Insert program
                p_row = await conn.fetchrow(
                    query_program,
                    program_data["athlete_id"],
                    program_data["name"],
                    program_data["goal"],
                    program_data["sessions_per_week"]
                )
                program = dict(p_row)
                program["weeks"] = []

                # 2. Insert weeks
                for w_data in program_data["weeks"]:
                    w_row = await conn.fetchrow(
                        query_week,
                        program["id"],
                        w_data["week_number"],
                        w_data["focus"]
                    )
                    week = dict(w_row)
                    week["sessions"] = []

                    # 3. Insert sessions
                    for s_data in w_data["sessions"]:
                        s_row = await conn.fetchrow(
                            query_session,
                            week["id"],
                            s_data["session_number"]
                        )
                        session = dict(s_row)
                        session["exercises"] = []

                        # 4. Insert exercises
                        for ex_data in s_data["exercises"]:
                            ex_row = await conn.fetchrow(
                                query_exercise,
                                session["id"],
                                ex_data["exercise_id"],
                                ex_data["display_order"],
                                ex_data["sets"],
                                ex_data["reps"],
                                ex_data["intensity"],
                                ex_data["rest_seconds"]
                            )
                            # Pull additional metadata from exercises table to return full info
                            meta_query = """
                                SELECT name, description, difficulty_level, mechanics_type, force_type
                                FROM exercises WHERE id = $1;
                            """
                            meta_row = await conn.fetchrow(meta_query, ex_data["exercise_id"])
                            ex_record = dict(ex_row)
                            if meta_row:
                                ex_record.update(dict(meta_row))
                            session["exercises"].append(ex_record)
                        
                        week["sessions"].append(session)
                    program["weeks"].append(week)
                
                return program

    async def get_by_id(self, program_id: int) -> Optional[Dict[str, Any]]:
        query_program = """
            SELECT id, athlete_id, name, goal, sessions_per_week, created_at, updated_at
            FROM programs
            WHERE id = $1;
        """
        if not self.pool:
            return None
        
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query_program, program_id)
            if not row:
                return None
            
            program = dict(row)
            
            # Fetch weeks
            query_weeks = """
                SELECT id, week_number, focus
                FROM program_weeks
                WHERE program_id = $1
                ORDER BY week_number;
            """
            week_rows = await conn.fetch(query_weeks, program_id)
            program["weeks"] = []
            
            for w_row in week_rows:
                week = dict(w_row)
                
                # Fetch sessions
                query_sessions = """
                    SELECT id, session_number
                    FROM program_sessions
                    WHERE week_id = $1
                    ORDER BY session_number;
                """
                session_rows = await conn.fetch(query_sessions, week["id"])
                week["sessions"] = []
                
                for s_row in session_rows:
                    session = dict(s_row)
                    
                    # Fetch exercises
                    query_exercises = """
                        SELECT pse.id, pse.exercise_id, e.name, e.description, e.difficulty_level, e.mechanics_type, e.force_type,
                               pse.display_order, pse.sets, pse.reps, pse.intensity, pse.rest_seconds
                        FROM program_session_exercises pse
                        JOIN exercises e ON pse.exercise_id = e.id
                        WHERE pse.session_id = $1
                        ORDER BY pse.display_order;
                    """
                    exercise_rows = await conn.fetch(query_exercises, session["id"])
                    session["exercises"] = [dict(ex) for ex in exercise_rows]
                    week["sessions"].append(session)
                
                program["weeks"].append(week)
            
            return program

    async def delete_program(self, program_id: int) -> bool:
        query = "DELETE FROM programs WHERE id = $1;"
        if not self.pool:
            return False
        async with self.pool.acquire() as conn:
            result = await conn.execute(query, program_id)
            return "DELETE 1" in result


# Shared repository instance for offline/in-memory mode
_mock_repo = MockProgramRepository()

def get_program_repository() -> ProgramRepository:
    db_url = os.getenv("DATABASE_URL")
    if db_url and db_pool:
        logger.info("FACTORY: get_program_repository() -> PostgreSqlProgramRepository")
        return PostgreSqlProgramRepository(db_pool)
    logger.info("FACTORY: get_program_repository() -> MockProgramRepository")
    return _mock_repo


# -------------------------------------------------------------
# 4. Service / Generation Layer
# -------------------------------------------------------------

class ProgramBuilderService:
    def __init__(
        self,
        program_repo: ProgramRepository,
        athlete_repo: AthleteRepository,
        results_repo: AssessmentResultRepository
    ):
        self.program_repo = program_repo
        self.athlete_repo = athlete_repo
        self.results_repo = results_repo

    async def resolve_athlete_deficits_and_goal(
        self, athlete: Dict[str, Any], requested_goal: Optional[str]
    ) -> str:
        """Resolves athlete deficits and maps them to a training goal."""
        if requested_goal:
            return requested_goal

        # Detect deficits from athlete history
        athlete_id = athlete["id"]
        history = await self.results_repo.get_history(athlete_id)
        
        if not history:
            # Fallback to Power goal if no assessment history
            return "Power"
        
        # Format results dict for deficit engine
        results_dict = {}
        for r in history:
            # Check what assessment mapping matches the ID
            # CMJ=1, Broad Jump=2, 10m Sprint=3, 20m Sprint=4, Pull Up=5, Trap Bar Deadlift=6
            mapping = {
                1: "cmj",
                2: "broad jump",
                3: "10m sprint",
                4: "20m sprint",
                5: "pull up",
                6: "trap bar deadlift"
            }
            ass_name = mapping.get(r["assessment_id"])
            if ass_name and ass_name not in results_dict:
                # Store the latest score
                results_dict[ass_name] = float(r["score"])
        
        # Run deficit diagnostics
        db_url = os.getenv("DATABASE_URL")
        if db_url and db_pool:
            logger.info("INLINE: benchmark repo -> PostgreSqlBenchmarkRepository")
            bench_repo = PostgreSqlBenchmarkRepository(db_pool)
        else:
            logger.info("INLINE: benchmark repo -> MockBenchmarkRepository")
            bench_repo = MockBenchmarkRepository()
        deficit_service = DeficitDetectionService(bench_repo)
        deficits = await deficit_service.detect_deficits(results_dict)
        
        if not deficits:
            return "Power"
            
        # Priority mapping: highest severity deficit first
        severity_priority = {"High": 2, "Moderate": 1}
        sorted_deficits = sorted(deficits, key=lambda x: severity_priority.get(x.severity, 0), reverse=True)
        primary_deficit = sorted_deficits[0].deficit
        
        # Query templates for this deficit (database-driven routing)
        if db_url and db_pool:
            exercise_repo = PostgreSqlExerciseRepository(db_pool)
        else:
            exercise_repo = MockExerciseRepository()
        
        templates = await exercise_repo.get_templates_for_deficit(primary_deficit)
        
        logger.info(f"DEFICIT ROUTING: deficit={primary_deficit}, templates_found={len(templates)}")
        
        if not templates:
            logger.warning(f"No templates found for deficit '{primary_deficit}'. Falling back to Power.")
            return "Power"
        
        # Deterministic selection: prefer sport-specific templates, then first by ID
        # Extract template name as goal for backward compatibility
        selected_template = templates[0]
        goal = selected_template["name"]
        
        logger.info(f"DEFICIT ROUTING: selected_template={selected_template['id']}/{goal}")
        
        return goal

    async def generate_program(
        self,
        request: ProgramGenerateRequest,
        use_default_exercise: Optional[bool] = None
    ) -> Dict[str, Any]:
        # Resolve feature flag: request override > env var > default False
        use_default = USE_DEFAULT_EXERCISE if use_default_exercise is None else use_default_exercise

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
        
        # In mock mode, map dynamically based on IDs
        sport_name = "Cricket"
        role_name = ROLE_NAMES.get(role_id, "Fast Bowler")

        db_url = os.getenv("DATABASE_URL")
        if db_url and db_pool:
            # Resolve sport and role names relationally
            async with db_pool.acquire() as conn:
                sport_row = await conn.fetchrow("SELECT name FROM sports WHERE id = $1;", sport_id)
                if sport_row:
                    sport_name = sport_row["name"]
                role_row = await conn.fetchrow("SELECT name FROM roles WHERE id = $1;", role_id)
                if role_row:
                    role_name = role_row["name"]

        # 3. Resolve goal
        goal = await self.resolve_athlete_deficits_and_goal(athlete, request.goal)

        # 4. Resolve difficulty cap, training_age_months, development_level, and equipment
        difficulty_cap = request.difficulty_cap or athlete["competition_level"]
        training_age_months = athlete.get("training_age_months", athlete.get("training_age_years", 0) * 12)
        development_level = training_months_to_level(training_age_months)
        
        # Standard equipment defaults if not provided
        equipment = request.equipment or [
            "Trap Bar", "Medicine Ball", "Kettlebell", "Dumbbell", "Cable Machine", "Barbell", "Bodyweight"
        ]

        # 5. Fetch exercise recommendations pool per slot
        rec_req = RecommendationRequest(
            sport=sport_name,
            role=role_name,
            goal=goal,
            equipment=equipment,
            difficulty_cap=difficulty_cap,
            training_age_months=training_age_months,
            development_level=development_level
        )
        
        if db_url and db_pool:
            logger.info("INLINE: exercise repo -> PostgreSqlExerciseRepository")
            rec_repo = PostgreSqlExerciseRepository(db_pool)
        else:
            logger.info("INLINE: exercise repo -> MockExerciseRepository")
            rec_repo = MockExerciseRepository()
        try:
            rec_response = await get_exercise_recommendations(rec_req, repo=rec_repo)
        except Exception as e:
            logger.error(f"Error calling recommendation engine: {e}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Failed to generate recommendations: {str(e)}"
            )

        slots = rec_response.slots
        if not slots:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"No exercise slots found for template matching sport '{sport_name}', role '{role_name}', goal '{goal}'."
            )

        # 6. Build 4-week program structure with progressions
        program_name = request.name or f"4-Week {goal} Block for {athlete['first_name']}"
        program_data = {
            "athlete_id": request.athlete_id,
            "name": program_name,
            "goal": goal,
            "sessions_per_week": request.sessions_per_week,
            "weeks": []
        }

        # S&C Weekly Progression Parameters
        week_details = [
            {"week": 1, "focus": "Base"},
            {"week": 2, "focus": "Accumulation"},
            {"week": 3, "focus": "Peak"},
            {"week": 4, "focus": "Deload"}
        ]

        for wk in week_details:
            week_num = wk["week"]
            week_record = {
                "week_number": week_num,
                "focus": wk["focus"],
                "sessions": []
            }
            
            for s_num in range(1, request.sessions_per_week + 1):
                session_record = {
                    "session_number": s_num,
                    "exercises": []
                }
                
                # Assign one exercise per template slot
                for slot in slots:
                    if use_default and slot.default_exercise is not None:
                        # Feature flag: use the slot's default exercise every session
                        selected_ex = slot.default_exercise
                    else:
                        # Legacy: rotate through pool using modulo arithmetic
                        pool = slot.exercise_pool
                        if not pool:
                            logger.warning(f"No exercises available for slot '{slot.slot_name}'. Skipping.")
                            continue
                        selected_ex = pool[(s_num - 1) % len(pool)]
                    
                    # Resolve baseline reps
                    vol_target = slot.progression.get("volume_target") if slot.progression else None
                    baseline_reps = parse_baseline_reps(vol_target, slot.slot_type)
                    
                    # Compute sets, reps, intensity, rest for this specific week
                    sets, reps, intensity, rest = calculate_reps_and_intensity(
                        week_num=week_num,
                        baseline_reps=baseline_reps,
                        exercise_class=getattr(selected_ex, 'exercise_class', None) or "",
                        force_type=selected_ex.force_type,
                        slot_type=slot.slot_type
                    )
                    
                    session_record["exercises"].append({
                        "exercise_id": selected_ex.id,
                        "name": selected_ex.name,
                        "description": selected_ex.description,
                        "difficulty_level": selected_ex.difficulty_level,
                        "mechanics_type": selected_ex.mechanics_type,
                        "force_type": selected_ex.force_type,
                        "exercise_class": getattr(selected_ex, 'exercise_class', None) or "",
                        "display_order": slot.display_order,
                        "slot_id": slot.slot_id if hasattr(slot, 'slot_id') else slot.display_order,
                        "sets": sets,
                        "reps": reps,
                        "intensity": intensity,
                        "rest_seconds": rest
                    })
                
                # Sort exercises by display_order
                session_record["exercises"].sort(key=lambda x: x["display_order"])
                week_record["sessions"].append(session_record)
            
            program_data["weeks"].append(week_record)

        return program_data

    async def build_and_save(self, request: ProgramGenerateRequest, use_default_exercise: Optional[bool] = None) -> Dict[str, Any]:
        """Generate program data and persist it to the repository."""
        program_data = await self.generate_program(request, use_default_exercise)
        created_program = await self.program_repo.create_program(program_data)
        return created_program

    async def stage_program(self, request: ProgramGenerateRequest, use_default_exercise: Optional[bool] = None) -> Dict[str, Any]:
        """Generate program data and store in-memory (staged, not persisted)."""
        program_data = await self.generate_program(request, use_default_exercise)
        stage_id = str(uuid.uuid4())
        now = datetime.utcnow()
        staged = {
            "stage_id": stage_id,
            "status": "staged",
            "program_data": program_data,
            "created_at": now
        }
        _staged_programs[stage_id] = staged
        return {
            "stage_id": stage_id,
            "status": "staged",
            "athlete_id": program_data["athlete_id"],
            "name": program_data["name"],
            "goal": program_data["goal"],
            "sessions_per_week": program_data["sessions_per_week"],
            "week_count": len(program_data["weeks"]),
            "created_at": now
        }

    async def confirm_staged(self, stage_id: str) -> Dict[str, Any]:
        """Persist a staged program to the repository."""
        staged = _staged_programs.get(stage_id)
        if not staged:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Staged program with ID '{stage_id}' not found."
            )
        if staged["status"] != "staged":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Staged program '{stage_id}' has already been confirmed."
            )
        program_data = staged["program_data"]
        created = await self.program_repo.create_program(program_data)
        staged["status"] = "confirmed"
        return created

    async def preview_swap(self, stage_id: str, slot_id: int, target_exercise_id: int) -> Dict[str, Any]:
        """Preview what happens when an exercise is swapped in a staged program."""
        staged = _staged_programs.get(stage_id)
        if not staged:
            raise HTTPException(status_code=404, detail=f"Staged program '{stage_id}' not found.")
        if staged["status"] != "staged":
            raise HTTPException(status_code=409, detail=f"Staged program '{stage_id}' is already confirmed.")

        program_data = staged["program_data"]
        weeks = program_data.get("weeks", [])

        # Find current exercise in the first session that matches this slot
        current_ex = None
        for week in weeks:
            for session in week.get("sessions", []):
                for ex in session.get("exercises", []):
                    if ex.get("slot_id") == slot_id:
                        current_ex = ex
                        break
                if current_ex:
                    break
            if current_ex:
                break

        if not current_ex:
            raise HTTPException(status_code=404, detail=f"No exercise found for slot_id {slot_id} in staged program.")

        # Find target exercise metadata from catalog
        athlete = await self.athlete_repo.get_by_id(program_data["athlete_id"])
        equipment = []  # Will populate from program generation context

        # Build mock repo to look up target exercise
        rec_repo = MockExerciseRepository()
        target_candidates = await rec_repo.get_ranked_exercises(
            slot_id=slot_id,
            template_id=_resolve_template_id_from_slot(slot_id),
            difficulty_cap="Elite",
            equipment=["Barbell", "Trap Bar", "Medicine Ball", "Kettlebell", "Dumbbell", "Cable Machine", "Bodyweight"],
            training_age_months=999,
            development_level="PERFORMANCE"
        )
        target_ex = next((e for e in target_candidates if e["id"] == target_exercise_id), None)
        if not target_ex:
            raise HTTPException(status_code=404, detail=f"Target exercise ID {target_exercise_id} not found for slot {slot_id}.")

        # Check if movement pattern and force_type match (unchanged = true)
        current_cls = current_ex.get("exercise_class", "")
        target_cls = target_ex.get("exercise_class", "")
        current_ft = current_ex.get("force_type", "")
        target_ft = target_ex.get("force_type", "")
        current_mp = current_ex.get("mechanics_type", "")
        target_mp = target_ex.get("mechanics_type", "")

        # Use classification-based comparison: same class + same force type = unchanged intent
        unchanged = (current_cls == target_cls) and (current_ft == target_ft)
        reason_parts = []

        if unchanged:
            reason_parts.append("Movement intent preserved (same exercise class and force type)")
        else:
            if current_cls != target_cls:
                reason_parts.append(f"Exercise class changed: {current_cls} -> {target_cls}")
            if current_ft != target_ft:
                reason_parts.append(f"Force type changed: {current_ft} -> {target_ft}")

        # Build week-by-week progression for the swapped exercise
        week_details = [1, 2, 3, 4]
        week_results = []
        baseline_reps = 5

        for w in week_details:
            sets, reps, intensity, rest = calculate_reps_and_intensity(
                week_num=w,
                baseline_reps=baseline_reps,
                exercise_class=target_cls,
                force_type=target_ft,
                slot_type="Primary"
            )
            week_results.append(SwapWeekDetail(
                week_number=w,
                session_number=1,
                exercise_id=target_ex["id"],
                name=target_ex["name"],
                exercise_class=target_cls or None,
                sets=sets,
                reps=reps,
                intensity=intensity,
                rest_seconds=rest
            ))

        return SwapPreviewResponse(
            unchanged=unchanged,
            current_exercise_name=current_ex["name"],
            new_exercise_name=target_ex["name"],
            reason="; ".join(reason_parts),
            weeks=week_results
        )

    async def apply_override(self, entry: CoachOverrideEntry) -> Dict[str, Any]:
        """Record a coach override for auditing."""
        stage_overrides = _coach_overrides.setdefault(entry.stage_id, {})
        stage_overrides[entry.slot_id] = entry
        return {
            "status": "recorded",
            "stage_id": entry.stage_id,
            "slot_id": entry.slot_id,
            "original_exercise_id": entry.original_exercise_id,
            "selected_exercise_id": entry.selected_exercise_id
        }


def _resolve_template_id_from_slot(slot_id: int) -> int:
    if slot_id >= 400:
        return 102
    if slot_id >= 300:
        return 101
    return 100


# -------------------------------------------------------------
# 5. FastAPI Endpoints
# -------------------------------------------------------------

@app.post(
    "/api/v1/programs/generate",
    response_model=ProgramResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate a Training Program",
    description="Loads the athlete profile and deficits, compiles templates, runs weekly S&C progressions, and saves the 4-week program."
)
async def generate_program(
    request: ProgramGenerateRequest,
    program_repo: ProgramRepository = Depends(get_program_repository),
    athlete_repo: AthleteRepository = Depends(get_athlete_repository),
    results_repo: AssessmentResultRepository = Depends(get_results_repository)
):
    service = ProgramBuilderService(program_repo, athlete_repo, results_repo)
    return await service.build_and_save(request)


@app.post(
    "/api/v1/programs/stage",
    response_model=StagedProgramResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Stage a Training Program",
    description="Generates program data and stages it in-memory for review before confirmation."
)
async def stage_program(
    request: StageRequest,
    program_repo: ProgramRepository = Depends(get_program_repository),
    athlete_repo: AthleteRepository = Depends(get_athlete_repository),
    results_repo: AssessmentResultRepository = Depends(get_results_repository)
):
    # Convert StageRequest to ProgramGenerateRequest for the service
    gen_req = ProgramGenerateRequest(
        athlete_id=request.athlete_id,
        sessions_per_week=request.sessions_per_week,
        name=request.name,
        goal=request.goal,
        equipment=request.equipment,
        difficulty_cap=request.difficulty_cap
    )
    service = ProgramBuilderService(program_repo, athlete_repo, results_repo)
    return await service.stage_program(gen_req, use_default_exercise=request.use_default_exercise)


@app.post(
    "/api/v1/programs/confirm",
    response_model=ProgramResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Confirm a Staged Program",
    description="Persists a previously staged program to the database."
)
async def confirm_program(
    request: ConfirmRequest,
    program_repo: ProgramRepository = Depends(get_program_repository),
    athlete_repo: AthleteRepository = Depends(get_athlete_repository),
    results_repo: AssessmentResultRepository = Depends(get_results_repository)
):
    service = ProgramBuilderService(program_repo, athlete_repo, results_repo)
    return await service.confirm_staged(request.stage_id)


@app.post(
    "/api/v1/programs/preview-swap",
    response_model=SwapPreviewResponse,
    status_code=status.HTTP_200_OK,
    summary="Preview Exercise Swap",
    description="Given a staged program, slot, and target exercise, previews the swap outcome with recalculated progression."
)
async def preview_swap(
    request: SwapPreviewRequest,
    program_repo: ProgramRepository = Depends(get_program_repository),
    athlete_repo: AthleteRepository = Depends(get_athlete_repository),
    results_repo: AssessmentResultRepository = Depends(get_results_repository)
):
    service = ProgramBuilderService(program_repo, athlete_repo, results_repo)
    return await service.preview_swap(request.stage_id, request.slot_id, request.target_exercise_id)


@app.post(
    "/api/v1/programs/override",
    status_code=status.HTTP_200_OK,
    summary="Record Coach Override",
    description="Records a coach's exercise substitution for audit trail purposes."
)
async def apply_override(
    request: CoachOverrideEntry,
    program_repo: ProgramRepository = Depends(get_program_repository),
    athlete_repo: AthleteRepository = Depends(get_athlete_repository),
    results_repo: AssessmentResultRepository = Depends(get_results_repository)
):
    service = ProgramBuilderService(program_repo, athlete_repo, results_repo)
    return await service.apply_override(request)


@app.get(
    "/api/v1/programs/{id}",
    response_model=ProgramResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve Training Program Hierarchy",
    description="Returns the full nested database hierarchy: Program -> Weeks -> Sessions -> Exercises."
)
async def get_program(
    id: int,
    repo: ProgramRepository = Depends(get_program_repository)
):
    program = await repo.get_by_id(id)
    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Training program with ID {id} not found."
        )
    return program


@app.delete(
    "/api/v1/programs/{id}",
    status_code=status.HTTP_200_OK,
    summary="Delete Training Program",
    description="Permanently deletes the training program and cascading weeks, sessions, and exercises from the database."
)
async def delete_program(
    id: int,
    repo: ProgramRepository = Depends(get_program_repository)
):
    success = await repo.delete_program(id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Training program with ID {id} not found."
        )
    return {
        "status": "success",
        "message": f"Training program with ID {id} deleted successfully."
    }


@app.get(
    "/health",
    status_code=status.HTTP_200_OK
)
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "database_connected": os.getenv("DATABASE_URL") is not None and db_pool is not None
    }
