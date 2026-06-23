# Forge Demonstration Integration Workflow
# Role: Principal Integration Architect
# Description: Orchestrates athlete profile creation, test log recording,
# deficit diagnostics, and exercise recommendations.
# Supports V1 (Template) and V2 (Demand) engines via ENGINE_MODE feature flag.

import os
import logging
from typing import List, Dict, Any, Optional, Literal
from datetime import date, datetime

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

# Import existing modules and repositories directly
from athlete_module import _mock_repo as athlete_repo, AthleteCreate
from assessment_entry_module import _mock_repo as results_repo, ResultCreate, ASSESSMENT_UNITS
from deficit_detection_engine import DeficitDetectionService, MockBenchmarkRepository, DeficitDetail
from recommendation_engine import MockExerciseRepository, RecommendationRequest, get_exercise_recommendations, training_months_to_level

# V2 Demand Scoring Engine (feature-flag gated)
from demand_scoring_engine import (
    MockDemandRepository as V2MockDemandRepository,
    get_demand_repository as get_v2_repo,
    compute_role_demand_scores,
    DemandScoreRequest as V2DemandScoreRequest,
)

# ENGINE_MODE feature flag: v1 (default), v2, or dual
ENGINE_MODE = os.getenv("ENGINE_MODE", "v1").lower()

logger = logging.getLogger("forge-integration-workflow")
app = FastAPI(
    title="Forge Integration Orchestration Engine",
    description="Wires athlete profile setups, test logging, and exercise recommendations. Supports V1 (Template) and V2 (Demand) engines.",
    version="2.0.0"
)

# -------------------------------------------------------------
# 1. Pydantic Integration Models
# -------------------------------------------------------------

class WorkflowRequest(BaseModel):
    first_name: str = Field(..., example="Nirav")
    last_name: str = Field(..., example="Patel")
    date_of_birth: date = Field(..., example="1998-05-20")
    gender: Literal['Male', 'Female', 'Other', 'Prefer Not to Say'] = Field("Male", example="Male")
    sport: str = Field("Cricket", example="Cricket")
    role: str = Field("Fast Bowler", example="Fast Bowler")
    dominant_side: str = Field("Right", example="Right")
    competition_level: str = Field("Elite", example="Elite")
    training_age_years: int = Field(8, example=8)
    training_age_months: int = Field(96, example=96)
    results: Dict[str, float] = Field(
        ..., 
        example={"CMJ": 38.0, "Broad Jump": 2.1, "10m Sprint": 1.95}
    )
    equipment: List[str] = Field(..., example=["Trap Bar", "Medicine Ball"])
    difficulty_cap: str = Field("Advanced", example="Advanced")


class ExerciseDetail(BaseModel):
    id: int
    name: str
    difficulty_level: str
    mechanics_type: str
    recommendation_score: float


class PrescribedTemplate(BaseModel):
    template_name: str
    training_goal: str
    slots: List[Dict[str, Any]]


class WorkflowResponse(BaseModel):
    athlete_id: int
    athlete_name: str
    diagnosed_deficits: List[DeficitDetail]
    prescribed_templates: List[PrescribedTemplate]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# -------------------------------------------------------------
# 2. Sequence Diagram (Documentation)
# -------------------------------------------------------------
"""
SEQUENCE DIAGRAM:
Client            Integration API            Athlete DB        Results DB        Deficit Engine        Recommender
  │                     │                        │                 │                   │                    │
  ├─(POST workflow)───> │                        │                 │                   │                    │
  │                     ├─(create_profile)─────> [athletes]        │                   │                    │
  │                     │ <──(returns ID 101)────┤                 │                   │                    │
  │                     │                                          │                   │                    │
  │                     ├─(record_scores)────────────────────────> [results]           │                    │
  │                     │ <──(returns OK)──────────────────────────┤                   │                    │
  │                     │                                                              │                    │
  │                     ├─(evaluate_deficits)────────────────────────────────────────> [heuristics]         │
  │                     │ <──(returns: Power, Acceleration Deficits)───────────────────┤                    │
  │                     │                                                                                   │
  │                     ├─(query_corrective_templates)────────────────────────────────────────────────────> [recommender]
  │                     │ <──(returns: Lower Body Power, Acceleration Dev templates)────────────────────────┤
  │                     │                                                                                   │
  │                     ├─(compile_exercise_pool_per_slot)────────────────────────────────────────────────> [spec_scoring]
  │                     │ <──(returns: Trap Bar Jump Squats, Bounds, tosses)────────────────────────────────┤
  │                     │                                                                                   │
  │ <──(JSON payload)───┤                                                                                   │
"""

# -------------------------------------------------------------
# 3. API Route Implementation
# -------------------------------------------------------------

@app.post(
    "/api/v1/integration/athlete-workflow",
    response_model=WorkflowResponse,
    status_code=status.HTTP_200_OK,
    summary="End-to-End Athlete Prescription Flow",
    description="Registers an athlete, records test results, computes physical deficits, and compiles recommended exercise routines."
)
async def run_athlete_workflow(request: WorkflowRequest):
    logger.info(f"Running integrated workflow for athlete: {request.first_name} {request.last_name} (ENGINE_MODE={ENGINE_MODE})")

    # ENGINE_MODE feature flag: redirect to V2 if set to "v2"
    if ENGINE_MODE == "v2":
        logger.info("ENGINE_MODE=v2: delegating to V2 demand engine")
        return await run_athlete_workflow_v2(request)

    # Step 1: Create Athlete Profile
    # Map Sport and Role names to lookup IDs for mock alignment
    sport_id = 1 if request.sport.lower() == "cricket" else 99
    role_id = 1 if "bowl" in request.role.lower() else 99

    try:
        ath_create = AthleteCreate(
            first_name=request.first_name,
            last_name=request.last_name,
            date_of_birth=request.date_of_birth,
            gender=request.gender,
            sport_id=sport_id,
            role_id=role_id,
            dominant_side=request.dominant_side,
            competition_level=request.competition_level,
            training_age_years=request.training_age_years,
            training_age_months=request.training_age_months
        )
        athlete = await athlete_repo.create(ath_create)
        athlete_id = athlete["id"]
    except Exception as e:
        logger.error(f"Failed to create integrated athlete profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Athlete creation failure: {str(e)}"
        )

    # Step 2: Record Assessment Results
    assessment_map = {
        "cmj": 1,
        "broad jump": 2,
        "10m sprint": 3,
        "20m sprint": 4,
        "pull up": 5,
        "trap bar deadlift": 6,
        "rotational med ball throw": 7
    }

    recorded_ids = []
    for test_name, score in request.results.items():
        clean_name = test_name.strip().lower()
        if clean_name not in assessment_map:
            logger.warning(f"Unmapped assessment test skipped: '{test_name}'")
            continue
        
        ass_id = assessment_map[clean_name]
        unit = ASSESSMENT_UNITS[ass_id]
        
        try:
            res_create = ResultCreate(
                athlete_id=athlete_id,
                assessment_id=ass_id,
                score=score,
                unit=unit,
                test_date=date.today()
            )
            rec = await results_repo.record_result(res_create)
            recorded_ids.append(rec["id"])
        except Exception as e:
            logger.error(f"Failed to record assessment score for '{test_name}': {e}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Score log failure for test '{test_name}': {str(e)}"
            )

    # Step 3: Run Deficit Diagnostics
    try:
        diag_service = DeficitDetectionService(MockBenchmarkRepository())
        deficits = await diag_service.detect_deficits(request.results)
    except Exception as e:
        logger.error(f"Failed to execute deficit detection diagnostics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Diagnostics engine error."
        )

    # Step 4: Map Deficits to Movement Templates using database-driven routing
    # Query templates for each deficit and get exercise recommendations
    exercise_repo = MockExerciseRepository()
    
    prescribed_templates = []
    for d in deficits:
        # Query templates for this deficit (database-driven)
        templates = await exercise_repo.get_templates_for_deficit(d.deficit)
        
        logger.info(f"DEFICIT ROUTING: deficit={d.deficit}, templates_found={len(templates)}")
        
        if not templates:
            logger.warning(f"No templates found for deficit '{d.deficit}'. Skipping.")
            continue
        
        # Deterministic selection: first template by ID
        selected_template = templates[0]
        goal_target = selected_template["name"]
        
        logger.info(f"DEFICIT ROUTING: selected_template={selected_template['id']}/{goal_target}")
        
        # Step 5: Query Recommendations for this goal
        development_level = training_months_to_level(request.training_age_months)
        rec_req = RecommendationRequest(
            sport=request.sport,
            role=request.role,
            goal=goal_target,
            equipment=request.equipment,
            difficulty_cap=request.difficulty_cap,
            training_age_months=request.training_age_months,
            development_level=development_level
        )
        
        try:
            # Call recommendations directly using the Mock Exercise Repository
            rec_response = await get_exercise_recommendations(rec_req, repo=MockExerciseRepository())
            
            # Map slots to response
            slots_data = []
            for slot in rec_response.slots:
                # Include top 3 recommended exercises
                exercises = [
                    {
                        "id": ex.id,
                        "name": ex.name,
                        "recommendation_score": ex.recommendation_score,
                        "difficulty_level": ex.difficulty_level,
                        "mechanics_type": ex.mechanics_type
                    }
                    for ex in slot.exercise_pool[:3]
                ]
                slots_data.append({
                    "slot_name": slot.slot_name,
                    "slot_type": slot.slot_type,
                    "progression": slot.progression,
                    "recommended_exercises": exercises
                })

            prescribed_templates.append(
                PrescribedTemplate(
                    template_name=rec_response.template_name,
                    training_goal=rec_response.training_goal,
                    slots=slots_data
                )
            )
        except Exception as e:
            logger.warning(f"Could not resolve template recommendations for goal '{goal_target}': {e}")
            continue

    return WorkflowResponse(
        athlete_id=athlete_id,
        athlete_name=f"{request.first_name} {request.last_name}",
        diagnosed_deficits=deficits,
        prescribed_templates=prescribed_templates
    )


# -------------------------------------------------------------
# 4b. V2 Workflow Route — Demand-Based (ENGINE_MODE = v2 or dual)
# -------------------------------------------------------------

class V2WorkflowResponse(WorkflowResponse):
    demand_scores: List[Dict[str, Any]] = Field(default_factory=list, description="Ranked performance demand scores")


@app.post(
    "/api/v2/integration/athlete-workflow",
    response_model=V2WorkflowResponse,
    status_code=status.HTTP_200_OK,
    summary="End-to-End Athlete Prescription Flow (V2 Demand Engine)",
    description="Registers an athlete, records test results, computes physical deficits, scores performance demands, and returns ranked exercises."
)
async def run_athlete_workflow_v2(request: WorkflowRequest):
    logger.info(f"[V2] Running demand-based workflow for athlete: {request.first_name} {request.last_name}")

    # Step 1: Create Athlete Profile (shared with V1)
    sport_id = 1 if request.sport.lower() == "cricket" else 99
    role_id = 1 if "bowl" in request.role.lower() else 99

    try:
        ath_create = AthleteCreate(
            first_name=request.first_name,
            last_name=request.last_name,
            date_of_birth=request.date_of_birth,
            gender=request.gender,
            sport_id=sport_id,
            role_id=role_id,
            dominant_side=request.dominant_side,
            competition_level=request.competition_level,
            training_age_years=request.training_age_years,
            training_age_months=request.training_age_months
        )
        athlete = await athlete_repo.create(ath_create)
        athlete_id = athlete["id"]
    except Exception as e:
        logger.error(f"[V2] Failed to create athlete profile: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Athlete creation failure: {str(e)}")

    # Step 2: Record Assessment Results (shared with V1)
    assessment_map = {
        "cmj": 1, "broad jump": 2, "10m sprint": 3, "20m sprint": 4,
        "pull up": 5, "trap bar deadlift": 6, "rotational med ball throw": 7
    }
    for test_name, score in request.results.items():
        clean_name = test_name.strip().lower()
        if clean_name not in assessment_map:
            logger.warning(f"[V2] Unmapped assessment test skipped: '{test_name}'")
            continue
        ass_id = assessment_map[clean_name]
        unit = ASSESSMENT_UNITS[ass_id]
        try:
            res_create = ResultCreate(athlete_id=athlete_id, assessment_id=ass_id, score=score, unit=unit, test_date=date.today())
            rec = await results_repo.record_result(res_create)
        except Exception as e:
            logger.error(f"[V2] Failed to record score for '{test_name}': {e}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Score log failure for '{test_name}': {str(e)}")

    # Step 3: Run Deficit Diagnostics (shared with V1)
    try:
        diag_service = DeficitDetectionService(MockBenchmarkRepository())
        deficits = await diag_service.detect_deficits(request.results)
    except Exception as e:
        logger.error(f"[V2] Failed to execute deficit detection: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Diagnostics engine error.")

    # Step 4: Compute Demand Scores (V2)
    development_level = training_months_to_level(request.training_age_months)
    v2_repo = V2MockDemandRepository()

    scored_demands = await compute_role_demand_scores(
        repo=v2_repo,
        sport=request.sport,
        role=request.role,
        results=request.results,
        development_level=development_level,
        equipment=request.equipment,
    )

    # Step 5: Get exercises for top demands
    v2_exercises = []
    for sd in scored_demands:
        exercises = await v2_repo.get_exercises_for_demand(
            demand_id=sd["demand_id"],
            difficulty_cap=request.difficulty_cap,
            equipment=request.equipment,
            training_age_months=request.training_age_months,
            development_level=development_level,
        )
        priority_weight = sd["priority"] / 100.0
        level_mult = {"FOUNDATION": 0.7, "DEVELOPMENT": 0.85, "PERFORMANCE": 1.0}.get(development_level, 0.7)

        for ex in exercises[:5]:  # Top 5 per demand
            relevance = ex.get("relevance_score", 5) / 10.0
            ex_equipment = v2_repo.exercise_equipment.get(ex["name"], ["Bodyweight"])
            eq_match = 1.0
            for req_eq in ex_equipment:
                if req_eq == "Bodyweight":
                    continue
                if req_eq not in request.equipment:
                    eq_match = 0.0
                    break
            score = relevance * priority_weight * level_mult * eq_match
            v2_exercises.append({
                "id": ex["id"],
                "name": ex["name"],
                "demand_name": ex["demand_name"],
                "difficulty_level": ex["difficulty_level"],
                "recommendation_score": round(score * 100.0, 2),
            })

    v2_exercises.sort(key=lambda x: x["recommendation_score"], reverse=True)

    # Step 6: Build response (maintain V1 compatibility)
    prescribed_templates = []
    for d in deficits[:2]:  # Keep V1 template format for backward compat
        templates = await MockExerciseRepository().get_templates_for_deficit(d.deficit)
        if not templates:
            continue
        selected = templates[0]
        prescribed_templates.append(PrescribedTemplate(
            template_name=selected["name"],
            training_goal=selected.get("training_goal", ""),
            slots=[{"slot_name": "V2 Demand-Driven", "slot_type": "Primary", "progression": None, "recommended_exercises": v2_exercises[:5]}]
        ))

    return V2WorkflowResponse(
        athlete_id=athlete_id,
        athlete_name=f"{request.first_name} {request.last_name}",
        diagnosed_deficits=deficits,
        prescribed_templates=prescribed_templates,
        demand_scores=scored_demands,
    )
