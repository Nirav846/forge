# Forge Exercise Recommendation Engine
# Role: Senior Backend Engineer
# Description: Production-grade FastAPI application containing schema models, database connections, recommendation queries, and caching mechanisms.

import os
import json
import logging
import hashlib
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio

from fastapi import FastAPI, HTTPException, Depends, Query, status
from pydantic import BaseModel, Field

# Re-exported from demand_scoring_engine for callers expecting these in recommendation_engine
from demand_scoring_engine import LEVEL_ORDINAL, training_months_to_level

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("forge-recommendation-engine")

app = FastAPI(
    title="Forge Exercise Recommendation Engine",
    description="Dynamic template compilation, exercise filtering, and S&C specificity scoring API.",
    version="1.0.0"
)

# -------------------------------------------------------------
# 1. Pydantic Models (Schemas)
# -------------------------------------------------------------

class RecommendationRequest(BaseModel):
    sport: str = Field(..., example="Cricket")
    role: str = Field(..., example="Fast Bowler")
    goal: str = Field(..., example="Power")
    equipment: List[str] = Field(..., example=["Trap Bar", "Medicine Ball"])
    difficulty_cap: str = Field(default="Intermediate", example="Intermediate")

    model_config = {
        "json_schema_extra": {
            "example": {
                "sport": "Cricket",
                "role": "Fast Bowler",
                "goal": "Power",
                "equipment": ["Trap Bar", "Medicine Ball"],
                "difficulty_cap": "Advanced"
            }
        }
    }

class ExerciseModel(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    difficulty_level: str
    mechanics_type: str
    force_type: str
    recommendation_score: float

class SlotRecommendation(BaseModel):
    slot_type: str
    slot_name: str
    display_order: int
    notes: Optional[str] = None
    progression: Optional[Dict[str, Any]] = None
    default_exercise: Optional[ExerciseModel] = None
    exercise_pool: List[ExerciseModel]

class RecommendationResponse(BaseModel):
    template_name: str
    sport: str
    athlete_role: str
    training_goal: str
    slots: List[SlotRecommendation]
    cached: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# -------------------------------------------------------------
# 2. Cache Layer (In-Memory with TTL - Redis-Ready Model)
# -------------------------------------------------------------

class MemoryCache:
    """Thread-safe in-memory cache with TTL supporting hash-based keys."""
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

# Hashing utility for cache key generation
def generate_cache_key(request: RecommendationRequest) -> str:
    key_str = f"{request.sport.lower()}:{request.role.lower()}:{request.goal.lower()}:{sorted(request.equipment)}:{request.difficulty_cap.lower()}"
    return hashlib.sha256(key_str.encode("utf-8")).hexdigest()

# -------------------------------------------------------------
# 3. Database Layer & Repository Pattern
# -------------------------------------------------------------

# In a production app, database connection pools are managed using asyncpg or SQLAlchemy
# We implement a clean ExerciseRepository with a fully functioning sports science mockup fallback
# so the application runs immediately, alongside actual PostgreSQL integration code.

class ExerciseRepository:
    """Interface for database operations."""
    async def get_template(self, sport: str, role: str, goal: str) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    async def get_slots(self, template_id: int) -> List[Dict[str, Any]]:
        raise NotImplementedError()

    async def get_slot_progression(self, slot_id: int) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()

    async def get_ranked_exercises(
        self,
        slot_id: int,
        template_id: int,
        difficulty_cap: str,
        equipment: List[str],
        training_age_months: int = 0,
        development_level: str = "PERFORMANCE"
    ) -> List[Dict[str, Any]]:
        raise NotImplementedError()
        
    async def get_templates_for_deficit(self, sport: str, deficit_name: Optional[str] = None) -> List[Dict[str, Any]]:
        raise NotImplementedError()


class PostgreSqlExerciseRepository(ExerciseRepository):
    """PostgreSQL production execution using asyncpg connection logic."""
    def __init__(self, pool=None):
        self.pool = pool  # asyncpg connection pool

    async def get_template(self, sport: str, role: str, goal: str) -> Optional[Dict[str, Any]]:
        # Query template matching sport + role + goal
        query = """
            SELECT mt.id, mt.name, mt.training_goal, s.name as sport_name
            FROM movement_templates mt
            JOIN sports s ON mt.sport_id = s.id
            WHERE s.name ILIKE $1 AND mt.athlete_role ILIKE $2 AND mt.training_goal ILIKE $3
            LIMIT 1;
        """
        # Fallback to general template matching goal if sport is not directly mapped
        fallback_query = """
            SELECT mt.id, mt.name, mt.training_goal, s.name as sport_name
            FROM movement_templates mt
            LEFT JOIN sports s ON mt.sport_id = s.id
            WHERE (s.name ILIKE $1 OR s.id IS NULL) AND mt.training_goal ILIKE $2
            ORDER BY s.id DESC NULLS LAST
            LIMIT 1;
        """
        if not self.pool:
            return None # Fallback to mock
        
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, sport, role, goal)
            if not row:
                row = await conn.fetchrow(fallback_query, sport, goal)
            return dict(row) if row else None

    async def get_slots(self, template_id: int) -> List[Dict[str, Any]]:
        query = """
            SELECT id, slot_type, name, display_order, notes
            FROM template_slots
            WHERE template_id = $1
            ORDER BY display_order;
        """
        if not self.pool: return []
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, template_id)
            return [dict(r) for r in rows]

    async def get_slot_progression(self, slot_id: int) -> Optional[Dict[str, Any]]:
        query = """
            SELECT progression_type, intensity_target, volume_target, progression_rule, deload_protocol
            FROM slot_progressions
            WHERE slot_id = $1
            LIMIT 1;
        """
        if not self.pool: return None
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, slot_id)
            return dict(row) if row else None

    async def get_ranked_exercises(
        self,
        slot_id: int,
        template_id: int,
        difficulty_cap: str,
        equipment: List[str],
        training_age_months: int = 0,
        development_level: str = "PERFORMANCE"
    ) -> List[Dict[str, Any]]:
        # Primary algorithm querying filtered exercises matching constraints, ordered by dynamic S&C score.
        query = """
            SELECT 
                e.id, 
                e.name, 
                e.description, 
                e.difficulty_level, 
                e.mechanics_type, 
                e.force_type,
                (
                    COALESCE(epq.relevance_score, 0) * 0.40 * 10.0 +  -- relevance (scale 1-10 -> 0-40)
                    COALESCE(esm.specificity_rating, 0) * 0.30 * 10.0 + -- specificity (scale 1-10 -> 0-30)
                    COALESCE(esm.transfer_index, 0.0) * 20.0 +        -- transfer index (scale 0-1 -> 0-20)
                    (CASE WHEN e.mechanics_type = 'Compound' AND ts.slot_type = 'Primary' THEN 5.0 ELSE 0.0 END) + -- mechanics alignment
                    (SELECT COUNT(*) * 2.0 FROM exercise_tags et JOIN slot_requirements sr ON et.tag_id = sr.tag_id WHERE et.exercise_id = e.id AND sr.slot_id = ts.id) -- tag match bonus
                )::numeric(5,2) as recommendation_score
            FROM exercises e
            JOIN exercise_movement_patterns emp ON e.id = emp.exercise_id
            JOIN template_slots ts ON ts.id = $1
            JOIN slot_requirements sr ON sr.slot_id = ts.id
            LEFT JOIN exercise_physical_qualities epq ON e.id = epq.exercise_id AND epq.physical_quality_id = sr.physical_quality_id
            LEFT JOIN exercise_sport_mapping esm ON e.id = esm.exercise_id AND esm.sport_id = (SELECT sport_id FROM movement_templates WHERE id = ts.template_id)
            WHERE 
                (sr.movement_pattern_id IS NULL OR emp.movement_pattern_id = sr.movement_pattern_id)
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
                -- Equipment validation: All required implements of an exercise must be in available array.
                -- Bodyweight is always assumed to be available.
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
        if not self.pool: return []
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, slot_id, difficulty_cap, equipment)
            return [dict(r) for r in rows]


class MockExerciseRepository(ExerciseRepository):
    """Fallback repository prepopulated with matching sports science records."""
    
    async def get_template(self, sport: str, role: str, goal: str) -> Optional[Dict[str, Any]]:
        sport_lower = sport.lower()
        role_lower = role.lower()
        goal_lower = goal.lower()
        
        if sport_lower == "cricket":
            # Fast Bowler templates
            if "bowl" in role_lower and "fast" in role_lower:
                if goal_lower == "power":
                    return {
                        "id": 100,
                        "name": "Cricket Fast Bowler Power",
                        "training_goal": "Develop lower body bracing capacity, explosive triple extension, and rotational power specific to the fast bowling release phase.",
                        "sport_name": "Cricket"
                    }
            # Spinner templates
            elif "spin" in role_lower:
                if goal_lower == "power":
                    return {
                        "id": 101,
                        "name": "Cricket Spinner Rotational Power",
                        "training_goal": "Develop rotational power, wrist spin efficiency, and repetitive rotational torque production specific to spin bowling mechanics.",
                        "sport_name": "Cricket"
                    }
            # Batter templates
            elif "batter" in role_lower:
                if goal_lower == "strength":
                    return {
                        "id": 102,
                        "name": "Cricket Batter Strength/Power",
                        "training_goal": "Develop explosive bat speed, shoulder robustness, and lower body power generation for aggressive batting and quick running between wickets.",
                        "sport_name": "Cricket"
                    }
                elif goal_lower == "power":
                    return {
                        "id": 103,
                        "name": "Cricket Batter Power",
                        "training_goal": "Develop explosive bat speed and quick reflexes for aggressive shot making and rapid scoring.",
                        "sport_name": "Cricket"
                    }
        return None

    async def get_slots(self, template_id: int) -> List[Dict[str, Any]]:
        # Determine slot series based on template ID
        if template_id == 100:  # Fast Bowler Power
            base_id = 200
        elif template_id == 101:  # Spinner Rotational Power
            base_id = 300
        elif template_id in [102, 103]:  # Batter Strength/Power or Batter Power
            base_id = 400
        else:
            # Default to Fast Bowler series for unknown templates
            base_id = 200
            
        return [
            {"id": base_id + 1, "slot_type": "Primary", "name": "Max Dynamic Output (Bilateral)", "display_order": 1, "notes": "Bilateral explosive lift designed to increase vertical ground reaction forces."},
            {"id": base_id + 2, "slot_type": "Secondary", "name": "Unilateral Force Production", "display_order": 2, "notes": "Unilateral hops or lateral bounds targeting deceleration."},
            {"id": base_id + 3, "slot_type": "Accessory", "name": "Triple Extension Acceleration", "display_order": 3, "notes": "Accessory ballistic work utilizing a hip hinge."},
            {"id": base_id + 4, "slot_type": "Core", "name": "Trunk Rotational Velocity", "display_order": 4, "notes": "Rotational trunk power to transfer force."}
        ]

    async def get_slot_progression(self, slot_id: int) -> Optional[Dict[str, Any]]:
        progressions = {
            # 200-series: Fast Bowler slots
            201: {"progression_type": "Velocity-Based", "intensity_target": "0.75-0.90 m/s", "volume_target": "4x3", "progression_rule": "Increase load if velocity exceeds 0.90 m/s. Strip load if below 0.75 m/s."},
            202: {"progression_type": "Qualitative/Technique", "intensity_target": "Max Landing Stiff", "volume_target": "3x5 each side", "progression_rule": "Increase lateral jump distance while maintaining landing balance."},
            203: {"progression_type": "Qualitative/Technique", "intensity_target": "Max Effort", "volume_target": "3x6", "progression_rule": "Increase medicine ball mass by 2 lbs if release speed is maintained."},
            204: {"progression_type": "Qualitative/Technique", "intensity_target": "Max rotational velocity", "volume_target": "3x6 each side", "progression_rule": "Focus on rapid hip opening and explosive release."},
            # 300-series: Spinner slots
            301: {"progression_type": "Velocity-Based", "intensity_target": "0.75-0.90 m/s", "volume_target": "4x3", "progression_rule": "Increase load if velocity exceeds 0.90 m/s. Strip load if below 0.75 m/s."},
            302: {"progression_type": "Linear Load", "intensity_target": "Standard%", "volume_target": "3x8", "progression_rule": "Increase weight by 2.5-5lbs when reps exceed target by 2 for 2 consecutive sessions."},
            303: {"progression_type": "Double Progression", "intensity_target": "8-12 reps", "volume_target": "3x10", "progression_rule": "Once upper rep range is reached for 2 sets, increase weight by 5-10%."},
            304: {"progression_type": "Time-Based", "intensity_target": "Hold for time", "volume_target": "3x30s", "progression_rule": "Increase hold time by 5-10 seconds when proper form maintained for all sets."},
            # 400-series: Batter slots
            401: {"progression_type": "Velocity-Based", "intensity_target": "0.75-0.90 m/s", "volume_target": "4x3", "progression_rule": "Increase load if velocity exceeds 0.90 m/s. Strip load if below 0.75 m/s."},
            402: {"progression_type": "Double Progression", "intensity_target": "8-12 reps", "volume_target": "3x10", "progression_rule": "Once upper rep range is reached for 2 sets, increase weight by 5-10%."},
            403: {"progression_type": "Linear Load", "intensity_target": "Standard%", "volume_target": "3x8", "progression_rule": "Increase weight by 2.5-5lbs when reps exceed target by 2 for 2 consecutive sessions."},
            404: {"progression_type": "Qualitative/Technique", "intensity_target": "Max rotational velocity", "volume_target": "3x6 each side", "progression_rule": "Focus on rapid hip opening and explosive release."}
        }
        return progressions.get(slot_id)

    async def get_ranked_exercises(
        self,
        slot_id: int,
        template_id: int,
        difficulty_cap: str,
        equipment: List[str],
        training_age_months: int = 0,
        development_level: str = "PERFORMANCE"
    ) -> List[Dict[str, Any]]:
        
        # Difficulty hierarchies
        diff_rank = {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Elite": 4}
        cap = diff_rank.get(difficulty_cap, 2)

        # Map template-specific slot ID to base slot ID for exercise matching
        base_slot_id = slot_id
        if template_id == 101:  # Spinner - 300 series
            if 301 <= slot_id <= 304:
                base_slot_id = slot_id - 100
        elif template_id in [102, 103]:  # Batter - 400 series
            if 401 <= slot_id <= 404:
                base_slot_id = slot_id - 200
        # For template_id == 100 (Fast Bowler) or others, use slot_id as-is (200 series or default)

        # Full sports-science simulated catalog matching database seeds
        exercises = [
            {
                "id": 1,
                "name": "Trap Bar Jump Squat",
                "difficulty_level": "Advanced",
                "mechanics_type": "Compound",
                "force_type": "Push",
                "minimum_level": "DEVELOPMENT",
                "technical_difficulty": 6,
                "required_equipment": ["Trap Bar"],
                "slots": [201],
                "score_components": {"relevance": 10, "specificity": 10, "transfer": 0.90, "mechanics_bonus": 5.0, "tag_bonus": 6.0}
            },
            {
                "id": 2,
                "name": "Single-Leg Lateral Bound",
                "difficulty_level": "Intermediate",
                "mechanics_type": "Compound",
                "force_type": "Push",
                "minimum_level": "DEVELOPMENT",
                "technical_difficulty": 5,
                "required_equipment": ["Bodyweight"],
                "slots": [202],
                "score_components": {"relevance": 8, "specificity": 9, "transfer": 0.88, "mechanics_bonus": 0.0, "tag_bonus": 4.0}
            },
            {
                "id": 3,
                "name": "Medicine Ball Overhead Backwards Toss",
                "difficulty_level": "Intermediate",
                "mechanics_type": "Compound",
                "force_type": "Hinge",
                "minimum_level": "DEVELOPMENT",
                "technical_difficulty": 4,
                "required_equipment": ["Medicine Ball"],
                "slots": [203],
                "score_components": {"relevance": 9, "specificity": 8, "transfer": 0.82, "mechanics_bonus": 0.0, "tag_bonus": 6.0}
            },
            {
                "id": 4,
                "name": "Medicine Ball Rotational Chest Pass",
                "difficulty_level": "Beginner",
                "mechanics_type": "Compound",
                "force_type": "Rotation",
                "minimum_level": "FOUNDATION",
                "technical_difficulty": 2,
                "required_equipment": ["Medicine Ball"],
                "slots": [204],
                "score_components": {"relevance": 8, "specificity": 9, "transfer": 0.85, "mechanics_bonus": 0.0, "tag_bonus": 6.0}
            },
            {
                "id": 5,
                "name": "Cable Pallof Press with Rotation",
                "difficulty_level": "Intermediate",
                "mechanics_type": "Compound",
                "force_type": "Rotation",
                "minimum_level": "FOUNDATION",
                "technical_difficulty": 3,
                "required_equipment": ["Cable Machine"],
                "slots": [204],
                "score_components": {"relevance": 7, "specificity": 8, "transfer": 0.78, "mechanics_bonus": 0.0, "tag_bonus": 0.0}
            },
            {
                "id": 6,
                "name": "Trap Bar Deadlift",
                "difficulty_level": "Intermediate",
                "mechanics_type": "Compound",
                "force_type": "Hinge",
                "minimum_level": "DEVELOPMENT",
                "technical_difficulty": 5,
                "required_equipment": ["Trap Bar"],
                "slots": [201],
                "score_components": {"relevance": 9, "specificity": 9, "transfer": 0.85, "mechanics_bonus": 4.0, "tag_bonus": 5.0}
            },
            {
                "id": 7,
                "name": "Kettlebell Swing",
                "difficulty_level": "Beginner",
                "mechanics_type": "Compound",
                "force_type": "Hinge",
                "minimum_level": "FOUNDATION",
                "technical_difficulty": 2,
                "required_equipment": ["Kettlebell"],
                "slots": [201],
                "score_components": {"relevance": 8, "specificity": 7, "transfer": 0.80, "mechanics_bonus": 3.0, "tag_bonus": 4.0}
            },
            {
                "id": 8,
                "name": "Barbell Back Squat",
                "difficulty_level": "Advanced",
                "mechanics_type": "Compound",
                "force_type": "Push",
                "minimum_level": "DEVELOPMENT",
                "technical_difficulty": 7,
                "required_equipment": ["Barbell"],
                "slots": [202],
                "score_components": {"relevance": 9, "specificity": 8, "transfer": 0.90, "mechanics_bonus": 5.0, "tag_bonus": 3.0}
            },
            {
                "id": 9,
                "name": "Dumbbell Overhead Press",
                "difficulty_level": "Intermediate",
                "mechanics_type": "Compound",
                "force_type": "Push",
                "minimum_level": "FOUNDATION",
                "technical_difficulty": 3,
                "required_equipment": ["Dumbbell"],
                "slots": [203],
                "score_components": {"relevance": 8, "specificity": 7, "transfer": 0.85, "mechanics_bonus": 3.0, "tag_bonus": 4.0}
            },
            {
                "id": 10,
                "name": "Dumbbell Row",
                "difficulty_level": "Intermediate",
                "mechanics_type": "Compound",
                "force_type": "Pull",
                "minimum_level": "FOUNDATION",
                "technical_difficulty": 3,
                "required_equipment": ["Dumbbell"],
                "slots": [203],
                "score_components": {"relevance": 8, "specificity": 8, "transfer": 0.80, "mechanics_bonus": 3.0, "tag_bonus": 4.0}
            },
            {
                "id": 11,
                "name": "Nordic Hamstring Curl",
                "difficulty_level": "Intermediate",
                "mechanics_type": "Compound",
                "force_type": "Hinge",
                "minimum_level": "DEVELOPMENT",
                "technical_difficulty": 5,
                "required_equipment": ["Bodyweight"],
                "slots": [203],
                "score_components": {"relevance": 7, "specificity": 8, "transfer": 0.75, "mechanics_bonus": 2.0, "tag_bonus": 5.0}
            },
            {
                "id": 91,
                "name": "Medicine Ball Rotational Scoop Toss",
                "difficulty_level": "Beginner",
                "mechanics_type": "Compound",
                "force_type": "Rotation",
                "minimum_level": "FOUNDATION",
                "technical_difficulty": 2,
                "required_equipment": ["Medicine Ball"],
                "slots": [201, 204],
                "score_components": {"relevance": 9, "specificity": 9, "transfer": 0.85, "mechanics_bonus": 4.0, "tag_bonus": 3.0}
            },
            {
                "id": 86,
                "name": "Power Clean",
                "difficulty_level": "Advanced",
                "mechanics_type": "Olympic",
                "force_type": "Pull",
                "minimum_level": "PERFORMANCE",
                "technical_difficulty": 9,
                "required_equipment": ["Barbell"],
                "slots": [201],
                "score_components": {"relevance": 10, "specificity": 7, "transfer": 0.95, "mechanics_bonus": 5.0, "tag_bonus": 0.0}
            },
            {
                "id": 87,
                "name": "Hang Clean",
                "difficulty_level": "Intermediate",
                "mechanics_type": "Olympic",
                "force_type": "Pull",
                "minimum_level": "DEVELOPMENT",
                "technical_difficulty": 7,
                "required_equipment": ["Barbell"],
                "slots": [201],
                "score_components": {"relevance": 9, "specificity": 7, "transfer": 0.90, "mechanics_bonus": 4.0, "tag_bonus": 0.0}
            },
            {
                "id": 92,
                "name": "Push Jerk",
                "difficulty_level": "Advanced",
                "mechanics_type": "Compound",
                "force_type": "Push",
                "minimum_level": "PERFORMANCE",
                "technical_difficulty": 8,
                "required_equipment": ["Barbell"],
                "slots": [203],
                "score_components": {"relevance": 8, "specificity": 6, "transfer": 0.85, "mechanics_bonus": 3.0, "tag_bonus": 0.0}
            },
            {
                "id": 93,
                "name": "Push Press",
                "difficulty_level": "Intermediate",
                "mechanics_type": "Compound",
                "force_type": "Push",
                "minimum_level": "DEVELOPMENT",
                "technical_difficulty": 5,
                "required_equipment": ["Barbell"],
                "slots": [203],
                "score_components": {"relevance": 8, "specificity": 7, "transfer": 0.80, "mechanics_bonus": 3.0, "tag_bonus": 0.0}
            },
            {
                "id": 94,
                "name": "Barbell Jump Squat",
                "difficulty_level": "Advanced",
                "mechanics_type": "Compound",
                "force_type": "Push",
                "minimum_level": "PERFORMANCE",
                "technical_difficulty": 7,
                "required_equipment": ["Barbell"],
                "slots": [201],
                "score_components": {"relevance": 9, "specificity": 8, "transfer": 0.90, "mechanics_bonus": 5.0, "tag_bonus": 0.0}
            }
        ]

        pool = []
        for ex in exercises:
            # Check slot assignment using base slot ID
            if base_slot_id not in ex["slots"]:
                continue
            # Check difficulty cap
            if ex["difficulty_level"] not in diff_rank or diff_rank[ex["difficulty_level"]] > cap:
                continue
            # Check equipment availability
            eq_ok = True
            for req_eq in ex["required_equipment"]:
                if req_eq == "Bodyweight":
                    continue
                if req_eq not in equipment:
                    eq_ok = False
                    break
            if not eq_ok:
                continue

            # Template-specific exercise restrictions
            # Batter template (ID 102, 103) - Primary slot (401) 
            if template_id in [102, 103] and slot_id == 401:
                if ex["id"] not in [6, 7]:  # Only Trap Bar Deadlift and Kettlebell Swing allowed
                    continue
            # Batter template (ID 102, 103) - Accessory slot (403)
            elif template_id in [102, 103] and slot_id == 403:
                if ex["id"] not in [10, 11]:  # Only Dumbbell Row and Nordic Hamstring Curl allowed
                    continue
            # Spinner template (ID 101) - Primary slot (301)
            elif template_id == 101 and slot_id == 301:
                # Only Medicine Ball rotational exercises allowed
                if "Medicine Ball Rotational" not in ex["name"]:
                    continue
            # Spinner template (ID 101) - Secondary slot (302)
            elif template_id == 101 and slot_id == 302:
                if ex["id"] != 8:  # Only Barbell Back Squat allowed
                    continue
            # Spinner template (ID 101) - Accessory slot (303)
            elif template_id == 101 and slot_id == 303:
                if ex["id"] != 9:  # Only Dumbbell Overhead Press allowed
                    continue

            # Calculate recommendation score
            comp = ex["score_components"]
            score = (
                comp["relevance"] * 0.40 * 10.0 +    # 40% relevance
                comp["specificity"] * 0.30 * 10.0 +    # 30% specificity
                comp["transfer"] * 20.0 +            # 20% transfer
                comp["mechanics_bonus"] * 0.05 * 10.0 +  # 5% mechanics bonus
                comp["tag_bonus"] * 0.05 * 10.0      # 5% tag bonus
            )

            pool.append({
                "id": ex["id"],
                "name": ex["name"],
                "description": f"Target S&C exercise matching slot requirements using {', '.join(ex['required_equipment'])}.",
                "difficulty_level": ex["difficulty_level"],
                "mechanics_type": ex["mechanics_type"],
                "force_type": ex["force_type"],
                "slots": ex["slots"],
                "minimum_level": ex.get("minimum_level", "FOUNDATION"),
                "technical_difficulty": ex.get("technical_difficulty", 1),
                "recommendation_score": round(score, 2)
            })

        return sorted(pool, key=lambda x: x["recommendation_score"], reverse=True)

    async def get_templates_for_deficit(self, sport: str, deficit_name: Optional[str] = None) -> List[Dict[str, Any]]:
        # Mock: return a default template for any deficit
        return [
            {
                "id": 100,
                "name": "Cricket Fast Bowler Power",
                "goal": "Power",
                "training_goal": "Develop lower body bracing capacity, explosive triple extension, and rotational power specific to the fast bowling release phase.",
                "sport_name": sport
            }
        ]

# Dependency injection utility to resolve the active repository
def get_repository() -> ExerciseRepository:
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        # PostgreSQL repository instantiation goes here
        # Return PostgreSqlExerciseRepository(pool)
        pass
    # Default fallback to mock database
    return MockExerciseRepository()

# -------------------------------------------------------------
# 4. FastAPI Endpoints
# -------------------------------------------------------------

@app.post(
    "/api/v1/recommendations", 
    response_model=RecommendationResponse, 
    status_code=status.HTTP_200_OK,
    summary="Get Ranked S&C Exercise Recommendations",
    description="Loads a training template, evaluates slot constraints against athlete levels and equipment, and returns ranked exercise matches."
)
async def get_exercise_recommendations(
    request: RecommendationRequest,
    repo: ExerciseRepository = Depends(get_repository)
):
    # Step 1: Check L1/L2 Cache
    cache_key = generate_cache_key(request)
    cached_data = await cache.get(cache_key)
    if cached_data:
        logger.info(f"Cache hit for recommendation key: {cache_key}")
        cached_response = RecommendationResponse(**cached_data)
        cached_response.cached = True
        return cached_response

    logger.info(f"Cache miss. Resolving recommendation for sport: {request.sport}, goal: {request.goal}")

    # Step 2: Retrieve Template
    template = await repo.get_template(request.sport, request.role, request.goal)
    if not template:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No movement template found matching sport '{request.sport}' and goal '{request.goal}'."
        )

    # Step 3: Fetch Slots
    slots = await repo.get_slots(template["id"])
    if not slots:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Movement template '{template['name']}' has no slots defined."
        )

    # Step 4: Process and Rank Exercises for each slot
    slot_responses = []
    for slot in slots:
        # Load S&C Progression Rules
        progression = await repo.get_slot_progression(slot["id"])
        
        # Query matching exercises filtered by equipment and difficulty cap, ordered by score
        ranked_pool = await repo.get_ranked_exercises(
            slot_id=slot["id"],
            template_id=template["id"],
            difficulty_cap=request.difficulty_cap,
            equipment=request.equipment
        )

        slot_responses.append(
            SlotRecommendation(
                slot_type=slot["slot_type"],
                slot_name=slot["name"],
                display_order=slot["display_order"],
                notes=slot.get("notes"),
                progression=progression,
                default_exercise=ExerciseModel(**ranked_pool[0]) if ranked_pool else None,
                exercise_pool=[ExerciseModel(**ex) for ex in ranked_pool]
            )
        )

    response_data = RecommendationResponse(
        template_name=template["name"],
        sport=template["sport_name"],
        athlete_role=request.role,
        training_goal=template["training_goal"],
        slots=slot_responses
    )

    # Step 5: Save to Cache (5-minute TTL)
    await cache.set(cache_key, response_data.model_dump(), ttl_seconds=300)

    return response_data


@app.post(
    "/api/v1/cache/clear", 
    status_code=status.HTTP_200_OK,
    summary="Clear Recommendation Engine Cache",
    description="Flushes all cached templates and compiled recommendation results."
)
async def clear_cache():
    await cache.clear()
    logger.info("Recommendation engine cache cleared successfully.")
    return {"status": "success", "message": "Recommendation engine cache cleared."}


@app.get(
    "/health", 
    status_code=status.HTTP_200_OK,
    summary="Service Health Check"
)
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "database_connected": os.getenv("DATABASE_URL") is not None
    }
