"""FORGE Local API Server — FastAPI-based HTTP interface to the FORGE engine."""
from __future__ import annotations
import json
import os
import traceback
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .main import generate_program
from .api_serializers import serialize_program, athlete_profile_from_request
from .artifact_store import (
    save_artifact, load_artifact, list_artifacts, delete_artifact, duplicate_artifact,
    update_artifact,
)
from .team_store import (
    save_team_template, load_team_template, list_team_templates,
    update_team_template, delete_team_template,
)

# ── FastAPI App ────────────────────────────────────────────────────

app = FastAPI(
    title="FORGE Engine API",
    version="1.0.0",
    description="Local API for FORGE athlete development program generation.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Pydantic Request Models ───────────────────────────────────────

class AthleteBasics(BaseModel):
    athlete_name: Optional[str] = ""
    age: Optional[int | str] = ""
    sex: Optional[str] = ""
    sport: Optional[str] = ""
    role: Optional[str] = ""
    training_age_years: Optional[int | float | str] = ""
    level: Optional[str] = "Intermediate"
    environment: Optional[str] = ""
    available_minutes: Optional[int] = 60
    frequency_per_week: Optional[int] = 3
    days_to_match: Optional[int | str] = ""


class ProgramContext(BaseModel):
    primary_goal: Optional[str] = ""
    current_phase: Optional[str] = ""
    equipment_profile: Optional[list[str]] = []
    competition_proximity_note: Optional[str] = ""
    match_day: Optional[int] = None
    team_training_days: Optional[list[int]] = None
    heavy_field_days: Optional[list[int]] = None
    travel_days: Optional[list[int]] = None


class AdvancedProfile(BaseModel):
    force_velocity_profile: Optional[str] = ""
    sprint_10m_band: Optional[str] = ""
    aerobic_band: Optional[str] = ""
    squat_strength_band: Optional[str] = ""
    cmj_band: Optional[str] = ""
    technique_consistency: Optional[str] = ""
    injury_risk_flags: Optional[list[str]] = []
    prior_block_summary: Optional[str] = ""


class ProgramGenerateRequest(BaseModel):
    mode: str = "core"
    basics: AthleteBasics = Field(default_factory=AthleteBasics)
    context: ProgramContext = Field(default_factory=ProgramContext)
    advanced: AdvancedProfile = Field(default_factory=AdvancedProfile)
    duplicate_from: Optional[str] = None


class SaveArtifactRequest(BaseModel):
    request_payload: dict
    response_payload: dict
    program_id: Optional[str] = None
    status: str = "draft"
    coach_notes: str = ""
    internal_notes: str = ""
    version: int = 1
    duplicated_from: Optional[str] = None


class UpdateArtifactRequest(BaseModel):
    status: Optional[str] = None
    coach_notes: Optional[str] = None
    internal_notes: Optional[str] = None
    version_notes: Optional[str] = None
    coach_overrides: Optional[dict] = None


# ── Error Shape ────────────────────────────────────────────────────

class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: Optional[str] = None


# ── Endpoints ──────────────────────────────────────────────────────

@app.post("/api/programs/generate")
def generate(payload: ProgramGenerateRequest):
    """Generate a FORGE program from athlete inputs.

    If `duplicate_from` is set, loads the source artifact and includes
    an adaptation log comparing the new program to the source.
    """
    try:
        data = payload.model_dump()
        profile = athlete_profile_from_request(data)
        program = generate_program(profile)
        response = serialize_program(program, request_payload=data)

        if payload.duplicate_from:
            source = load_artifact(payload.duplicate_from)
            if source is None:
                raise HTTPException(
                    status_code=404,
                    detail=ErrorResponse(
                        error_code="NOT_FOUND",
                        message=f"Source artifact {payload.duplicate_from} not found.",
                    ).model_dump(),
                )
            from .adaptation import build_adaptation_log
            source_request = source.get("request_snapshot", {})
            source_request["_artifact_id"] = payload.duplicate_from
            source_response = source.get("result_snapshot", {})
            response["adaptation"] = build_adaptation_log(
                source_request, source_response, data, response,
            )

        return response
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error_code="GENERATION_FAILED",
                message=str(e),
                details=traceback.format_exc(),
            ).model_dump(),
        )


@app.post("/api/programs")
def save(payload: SaveArtifactRequest):
    """Save a generated program artifact."""
    try:
        artifact = save_artifact(
            request_payload=payload.request_payload,
            response_payload=payload.response_payload,
            program_id=payload.program_id,
            status=payload.status,
            coach_notes=payload.coach_notes,
            internal_notes=payload.internal_notes,
            version=payload.version,
            duplicated_from=payload.duplicated_from,
        )
        return artifact
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error_code="SAVE_FAILED",
                message=str(e),
            ).model_dump(),
        )


@app.get("/api/programs")
def list_all():
    """List all saved program artifacts (summary only)."""
    try:
        return {"artifacts": list_artifacts()}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error_code="LIST_FAILED",
                message=str(e),
            ).model_dump(),
        )


@app.get("/api/programs/{program_id}")
def get_one(program_id: str):
    """Load a single program artifact with full payloads."""
    artifact = load_artifact(program_id)
    if artifact is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                error_code="NOT_FOUND",
                message=f"Artifact {program_id} not found.",
            ).model_dump(),
        )
    return artifact


@app.delete("/api/programs/{program_id}")
def delete(program_id: str):
    """Delete a saved program artifact."""
    deleted = delete_artifact(program_id)
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                error_code="NOT_FOUND",
                message=f"Artifact {program_id} not found.",
            ).model_dump(),
        )
    return {"deleted": program_id}


@app.patch("/api/programs/{program_id}")
def patch(program_id: str, payload: UpdateArtifactRequest):
    """Update specific fields on an existing artifact (status, notes)."""
    fields = payload.model_dump(exclude_none=True)
    if not fields:
        raise HTTPException(status_code=400, detail=ErrorResponse(error_code="NO_FIELDS", message="No fields to update.").model_dump())
    artifact = update_artifact(program_id, **fields)
    if artifact is None:
        raise HTTPException(status_code=404, detail=ErrorResponse(error_code="NOT_FOUND", message=f"Artifact {program_id} not found.").model_dump())
    return artifact


@app.post("/api/programs/{program_id}/duplicate")
def duplicate(program_id: str):
    """Duplicate a saved program artifact."""
    artifact = duplicate_artifact(program_id)
    if artifact is None:
        raise HTTPException(
            status_code=404,
            detail=ErrorResponse(
                error_code="NOT_FOUND",
                message=f"Artifact {program_id} not found.",
            ).model_dump(),
        )
    return artifact


# ── Team Template Models ─────────────────────────────────────────────

class TeamTemplateCreateRequest(BaseModel):
    name: str
    sport: str
    level: str = "Intermediate"
    phase: str = "pre_season"
    goal: str = ""
    program_length_weeks: int = 4
    sessions_per_week: int = 3
    minutes_per_session: int = 60
    match_day: int = 5
    team_training_days: list[int] = [0, 2, 4]
    heavy_field_days: list[int] = [1, 3]
    travel_days: list[int] = []
    equipment_profile: list[str] = []
    coach_notes: str = ""
    program_snapshot: Optional[dict] = None


class TeamTemplateUpdateRequest(BaseModel):
    name: Optional[str] = None
    coach_notes: Optional[str] = None
    program_snapshot: Optional[dict] = None


class TeamAdaptRequest(BaseModel):
    athlete_name: str
    role: str = ""
    age: int | str = ""
    training_age_years: int | float | str = ""
    match_day: Optional[int] = None
    team_training_days: Optional[list[int]] = None
    heavy_field_days: Optional[list[int]] = None
    travel_days: Optional[list[int]] = None
    yoyo_ir1: Optional[float] = None
    yoyo_ir2: Optional[float] = None
    bronco: Optional[float] = None
    cmj: Optional[float] = None
    injury_flags: list[str] = []
    coach_intent: str = ""


# ── Team Template Endpoints ─────────────────────────────────────────

@app.post("/api/teams/templates")
def create_team_template(payload: TeamTemplateCreateRequest):
    try:
        data = payload.model_dump()
        template = save_team_template(data)
        return template
    except Exception as e:
        raise HTTPException(status_code=500, detail=ErrorResponse(error_code="TEMPLATE_CREATE_FAILED", message=str(e)).model_dump())


@app.get("/api/teams/templates")
def list_team_templates_endpoint():
    try:
        return {"templates": list_team_templates()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=ErrorResponse(error_code="TEMPLATE_LIST_FAILED", message=str(e)).model_dump())


@app.get("/api/teams/templates/{template_id}")
def get_team_template(template_id: str):
    template = load_team_template(template_id)
    if template is None:
        raise HTTPException(status_code=404, detail=ErrorResponse(error_code="NOT_FOUND", message=f"Template {template_id} not found.").model_dump())
    return template


@app.put("/api/teams/templates/{template_id}")
def update_team_template_endpoint(template_id: str, payload: TeamTemplateUpdateRequest):
    fields = payload.model_dump(exclude_none=True)
    if not fields:
        raise HTTPException(status_code=400, detail=ErrorResponse(error_code="NO_FIELDS", message="No fields to update.").model_dump())
    template = update_team_template(template_id, **fields)
    if template is None:
        raise HTTPException(status_code=404, detail=ErrorResponse(error_code="NOT_FOUND", message=f"Template {template_id} not found.").model_dump())
    return template


@app.delete("/api/teams/templates/{template_id}")
def delete_team_template_endpoint(template_id: str):
    deleted = delete_team_template(template_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=ErrorResponse(error_code="NOT_FOUND", message=f"Template {template_id} not found.").model_dump())
    return {"deleted": template_id}


@app.post("/api/teams/templates/{template_id}/adapt")
def adapt_team_template(template_id: str, payload: TeamAdaptRequest):
    """Adapt a team template to an individual athlete.

    Loads the template's request_snapshot, overlays athlete-specific
    details, then generates an individual program using the same
    pipeline as a normal generate call with duplicate_from pointing
    to the template.
    """
    template = load_team_template(template_id)
    if template is None:
        raise HTTPException(status_code=404, detail=ErrorResponse(error_code="NOT_FOUND", message=f"Template {template_id} not found.").model_dump())

    try:
        base = template.get("program_snapshot") or {}
        base_request = base.get("request_snapshot", {})

        # Build a generate request from template + athlete overrides
        gen_req = ProgramGenerateRequest(
            mode=base_request.get("mode", "core"),
            basics=AthleteBasics(
                athlete_name=payload.athlete_name,
                age=payload.age,
                sport=template.get("sport", ""),
                role=payload.role,
                level=template.get("level", "Intermediate"),
                training_age_years=payload.training_age_years,
                available_minutes=template.get("minutes_per_session", 60),
                frequency_per_week=template.get("sessions_per_week", 3),
            ),
            context=ProgramContext(
                primary_goal=template.get("goal", ""),
                current_phase=template.get("phase", ""),
                equipment_profile=template.get("equipment_profile", []),
                competition_proximity_note=payload.coach_intent or "",
                match_day=payload.match_day or template.get("match_day"),
                team_training_days=payload.team_training_days or template.get("team_training_days"),
                heavy_field_days=payload.heavy_field_days or template.get("heavy_field_days"),
                travel_days=payload.travel_days or template.get("travel_days"),
            ),
            advanced=AdvancedProfile(
                injury_risk_flags=payload.injury_flags,
                cmj_band=payload.cmj,
                yoyo_ir1=payload.yoyo_ir1,
                yoyo_ir2=payload.yoyo_ir2,
                bronco=payload.bronco,
            ),
        )

        return generate(gen_req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=ErrorResponse(error_code="ADAPT_FAILED", message=str(e)).model_dump())


@app.get("/api/health")
def health():
    """Health check endpoint."""
    return {"status": "ok", "version": "1.0.0"}


# ── CLI Entrypoint ────────────────────────────────────────────────

def run_server(host: str = "127.0.0.1", port: int = 8000, reload: bool = False):
    """Start the FORGE API server."""
    import uvicorn
    print(f"FORGE API server starting on http://{host}:{port}")
    print(f"Artifact storage: {os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.forge_artifacts')}")
    uvicorn.run("src.forge.api_server:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    run_server()
