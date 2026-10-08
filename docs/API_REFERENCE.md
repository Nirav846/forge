# FORGE API Reference

**Purpose:** Request/response reference for the FastAPI server
(`src/forge/api_server.py`, default `http://127.0.0.1:8000`, started via
`python run_forge_api.py`). As of 2026-09-24. Interactive docs: `GET /docs`
(Swagger UI provided by FastAPI).

> The API has **no authentication** and is intended for local/trusted-network
> use only. See `SECURITY.md`.

## Endpoints

### `GET /api/health`
Liveness check. Returns service status and version info.

### Programs

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/api/programs/generate` | Generate an 8-week periodized program |
| `GET` | `/api/programs` | List stored programs |
| `GET` | `/api/programs/{program_id}` | Retrieve one program |
| `POST` | `/api/programs/{program_id}/duplicate` | Clone a program |

**Generate request body** (three sections):

```json
{
  "mode": "core",
  "basics": {
    "athlete_name": "John Smith", "age": 25, "sex": "Male",
    "sport": "Basketball", "role": "Point Guard",
    "training_age_years": 5, "level": "Intermediate",
    "environment": "Commercial Gym",
    "available_minutes": 45, "frequency_per_week": 3
  },
  "context": {
    "primary_goal": "Power & Speed", "current_phase": "Pre-Season",
    "equipment_profile": ["Barbell", "Dumbbells", "Bands", "Medicine Balls"]
  },
  "advanced": {
    "force_velocity_profile": "Velocity Deficit",
    "sprint_10m_band": "<1.65s", "cmj_band": "High",
    "injury_risk_flags": ["Ankle"]
  }
}
```

Response contains weekly blocks (Accumulation/Intensification/Realization/Test),
sessions (warm-up, main work, conditioning) with sets/reps/load/rest/cues,
progression notes, validation results, and a credibility score (0.0–1.0).

Errors: `400` invalid profile fields; `404` unknown program id; `500` engine failure.

```bash
curl -X POST http://127.0.0.1:8000/api/programs/generate \
  -H "Content-Type: application/json" -d @examples/request.json
```

### Team Templates

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/teams/templates` | List team templates |
| `GET` | `/api/teams/templates/{template_id}` | Retrieve one template |
| `POST` | `/api/teams/templates/{template_id}/adapt` | Adapt template to constraints |

### Exercise Library (v1)

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/api/v1/exercises` | List exercises; supports filtering (category, equipment, movement pattern, etc.) |
| `GET` | `/api/v1/exercises/search` | Text search across names/cues |
| `GET` | `/api/v1/exercises/{exercise_id}` | Single exercise with full coaching metadata |

Records follow the schema in `DATA_MODEL.md` (cues, faults, contraindications,
development level, sport mapping).

## Versioning

Breaking changes require a new path namespace (`/api/v2/...`); additive field
changes are allowed within v1. Update this page and `CHANGELOG.md` in the same PR.
