# FORGE Frontend–Backend API Contract v1

## 1. Generate Program

### Request: `POST /api/programs/generate`

```json
{
  "mode": "core | premium",
  "basics": {
    "athlete_name": "string (optional, default '')",
    "age": "number | '' (optional, default 18)",
    "sex": "string (optional, default '')",
    "sport": "string (optional, default 'athlete')",
    "role": "string (optional, maps to position_role)",
    "training_age_years": "number | '' (optional, default 0)",
    "level": "'Beginner' | 'Intermediate' | 'Advanced' (optional, default 'Intermediate')",
    "environment": "string (optional, maps to EquipmentProfile)",
    "available_minutes": "number (optional, default 60)",
    "frequency_per_week": "number (informational, frequency is blueprint-driven)",
    "days_to_match": "number | '' (optional, drives competition taper)"
  },
  "context": {
    "primary_goal": "string (optional, default 'strength')",
    "current_phase": "string (optional, maps to SeasonPhase)",
    "equipment_profile": "string[] (optional)",
    "competition_proximity_note": "string (optional, informational only)"
  },
  "advanced": {
    "force_velocity_profile": "'Force Deficit' | 'Velocity Deficit' | 'Balanced' | '' (optional)",
    "sprint_10m_band": "string (optional, mapped to sprint_10m_band)",
    "aerobic_band": "string (optional, mapped to aerobic_band)",
    "squat_strength_band": "string (optional, mapped to squat_strength_band)",
    "cmj_band": "string (optional, mapped to cmj_band)",
    "technique_consistency": "'Low' | 'Medium' | 'High' | '' (optional, default 0.85)",
    "injury_risk_flags": "string[] (optional, mapped to injury_history + risk flags)",
    "prior_block_summary": "string (optional, informational only)"
  }
}
```

**Required:** only `basics.athlete_name` has a UI gate (Generate button disabled without it). Backend handles missing/empty fields gracefully.

### Response

```json
{
  "metadata": {
    "generated_at": "ISO 8601 timestamp",
    "request_id": "string",
    "api_version": "1.0.0"
  },
  "summary": {
    "blueprint_selected": "string — blueprint name",
    "blueprint_id": "number",
    "total_weeks": "number",
    "weekly_frequency": "number",
    "conditioning_emphasis": "string",
    "competition_window": "string — 'X days out' or 'Off-season'",
    "role_emphasis": "string — role + sport context",
    "level": "string",
    "goal": "string",
    "equipment_profile": "string",
    "credibility_score": "number 0.0–1.0"
  },
  "weeks": [
    {
      "week_number": "number",
      "label": "string",
      "exposure_summary": {
        "sprint_exposure": "string",
        "jump_landing_exposure": "string",
        "deceleration_exposure": "string",
        "eccentric_stress": "string",
        "conditioning_density": "string",
        "week_type": "string — accumulation/intensification/peak/taper/deload/test",
        "testing_markers": "string[]",
        "adjustment_notes": "string[]"
      },
      "sessions": ["Session (same shape as sessions[] below)"]
    }
  ],
  "sessions": [
    {
      "id": "string — stable identifier",
      "name": "string",
      "week_number": "number",
      "session_number": "number",
      "focus": "string — derived from exercise families",
      "warmup": {
        "title": "string",
        "exercises": ["Exercise"],
        "notes": "string | null"
      },
      "main_work": {
        "title": "string",
        "exercises": ["Exercise"],
        "notes": "string | null"
      },
      "conditioning": {
        "title": "string",
        "exercises": ["Exercise"],
        "notes": "string | null"
      },
      "session_notes": "string | null",
      "week_type": "string",
      "testing_markers": "string[]",
      "total_duration_min": "number",
      "load_capped": "boolean"
    }
  ],
  "rationale": "string[] — blueprint selection and planning decisions",
  "personalization_notes": "string[] — athlete-specific adjustments",
  "validation": [
    {
      "type": "'info' | 'warning' | 'success' | 'error'",
      "message": "string"
    }
  ],
  "dropped_constraints": "string[]"
}
```

### Exercise Shape

```json
{
  "id": "string — stable exercise ID",
  "name": "string",
  "family": "string — FamilyCode value or family name",
  "sets_reps": "string — e.g. '3 x 10'",
  "loading_method": "string — e.g. 'RPE 7', '85% 1RM'",
  "rest": "string — e.g. '90s', '2:00 min'",
  "progression_note": "string | null",
  "coach_note": "string | null",
  "difficulty": "number",
  "equipment": "string[]"
}
```

## 2. Error Payload

All errors return:

```json
{
  "detail": {
    "error_code": "GENERATION_FAILED | SAVE_FAILED | LIST_FAILED | NOT_FOUND",
    "message": "human-readable description",
    "details": "optional stack trace or additional context"
  }
}
```

HTTP status codes: `400` (validation), `404` (not found), `500` (server error).

## 3. Required vs Optional Field Matrix

| Section | Field | Required | Backend Source | Notes |
|---------|-------|----------|---------------|-------|
| summary | blueprint_selected | always | GeneratedProgram.blueprint_name | |
| summary | total_weeks | always | GeneratedProgram.duration | |
| summary | weekly_frequency | always | Computed from blueprint | May not match frontend input |
| summary | conditioning_emphasis | always | Derived from goal + season | |
| summary | competition_window | always | Computed from days_to_match | |
| summary | role_emphasis | always | From position_role + sport | |
| sessions | id | always | Generated `sess_{idx}` | Stable within a generation |
| sessions | warmup | always | Program warmup (shared) | Same warmup copied to all sessions |
| sessions | main_work | always | Session.blocks flattened | Empty array if no exercises |
| sessions | conditioning | always | Session.conditioning | Empty array if none |
| weeks | exposure_summary | always | Computed | Currently largely placeholder |
| rationale | | optional | Generated from blueprint/goal | |
| personalization_notes | | optional | program.personalization_notes | |
| validation | | optional | Derived from credibility checks | |
| dropped_constraints | | optional | | |

## 4. Fields That Are "Real" vs "Derived in Transformer"

**Real (supplied by backend):**
- All fields in the response JSON above

**Derived in the frontend transformer (`transformers.ts`):**
- Fallback IDs for exercises that lack them (generated client-side)
- Default strings for missing fields
- Weeks array inferred from sessions if `weeks[]` is missing
- Validation entry for zero sessions
- `generated_at` fallback if missing

## 5. Mapping: Backend Domain → API JSON

| Domain Model | API Field | Serializer |
|-------------|-----------|-----------|
| GeneratedProgram.blueprint_name | summary.blueprint_selected | Direct |
| GeneratedProgram.duration | summary.total_weeks | Direct |
| GeneratedProgram.frequency | summary.weekly_frequency | Computed |
| GeneratedProgram.goal | summary.goal | Direct |
| GeneratedProgram.equipment_profile | summary.equipment_profile | Direct |
| GeneratedProgram.credibility_score | summary.credibility_score | Direct |
| GeneratedProgram.personalization_notes | personalization_notes | Direct |
| GeneratedProgram.warmup | sessions[].warmup | Serialized as warmup section |
| Session.blocks[] | sessions[].main_work.exercises | Flattened, each exercise with prescription |
| Session.conditioning | sessions[].conditioning | Serialized as conditioning section |
| Session.week_type | sessions[].week_type, weeks[].exposure_summary.week_type | Direct |
| Session.testing_categories | sessions[].testing_markers | Direct |
| Session.adjustment_note | sessions[].session_notes | Direct |
| SessionBlock.exercises[] + Prescription | main_work.exercises[].sets_reps, loading_method, rest | Combined |
| Plan weeks + testing | weeks[].exposure_summary.testing_markers | Computed from test plan |
| AthleteProfile.days_to_match | summary.competition_window | Computed label |

## 6. Fields Missing from Backend That Frontend Assumes

The frontend `RawSessionSection` includes `notes` at the section level. The current backend does not produce section-level notes for warmup/main_work/conditioning; these are `null`. The transformer handles this gracefully.

The frontend `CoachSummaryMode` shows `dropped_constraints`. The backend currently doesn't track these at the API output level; the field is an empty array.

The frontend `WeeklyExposureVM` has detailed fields (`sprint_exposure`, `jump_landing_exposure`, etc.) that the backend `program_exposure_summary` computes, but is not currently surfaced in the API serializer in full detail. Values are `"Not specified"` placeholders.

## 7. Stable IDs

- Programs: `prog_{uuid hex[:12]}` — stable after save
- Sessions: `sess_{index}` — stable within a generation
- Exercises: use backend `Exercise.id` field (e.g. `ex_001`, `ex_002`)
- Artifacts: `prog_{uuid hex[:12]}` — persistent in artifact store

These IDs are deterministic within a single generation but will change on re-generation (as exercises may change). Saved artifacts preserve their IDs.

## 8. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-06-23 | Initial integration pass contract |
