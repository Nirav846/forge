# FORGE Program Artifact Storage v1

## Storage Choice: JSON File Store

**Decision:** Local JSON files stored in `.forge_artifacts/` at the repo root.

**Rationale:**
- No external database dependencies (zero infrastructure).
- Human-readable for debugging.
- Simplest possible implementation — each artifact is one JSON file.
- Easy to gitignore (`.forge_artifacts/`).
- Easy to backup, copy, or migrate.
- SQLite would add a query layer with no benefit at this scale (prototype/integration pass).

**Trade-off:** No concurrent multi-user access, no indexing, no relational queries. All acceptable for a locally-demoed coaching workspace.

## Artifact Schema

```json
{
  "id": "prog_a1b2c3d4e5f6 — UUID hex prefix",
  "created_at": "2026-06-23T06:00:00+00:00 — ISO 8601",
  "updated_at": "2026-06-23T06:30:00+00:00 — ISO 8601",
  "version": 1,
  "status": "draft | reviewed",
  "athlete_display_name": "string — from request.basics.athlete_name",
  "sport": "string",
  "role": "string",
  "goal": "string",
  "blueprint_label": "string — from response.summary.blueprint_selected",
  "week_label": "string — from response.summary.competition_window",
  "mode": "core | premium",
  "coach_notes": "string — coach-facing notes",
  "internal_notes": "string — internal use notes",
  "version_notes": "string — e.g. 'Duplicated from prog_xxx'",
  "duplicated_from": "string | null — original artifact ID if duplicated",

  "request_snapshot": { /* full ProgramRequest payload */ },
  "result_snapshot": { /* full RawProgramResponse payload */ }
}
```

## Canonical vs Derived Fields

| Field | Type | Notes |
|-------|------|-------|
| `id` | Canonical | Generated on save, immutable |
| `created_at` | Canonical | Set once on save |
| `updated_at` | Canonical | Updated on re-save |
| `version` | Canonical | Incremented on re-save or duplicate |
| `status` | Canonical | `draft` initially, can be set to `reviewed` |
| `athlete_display_name` | Derived | From `request_snapshot.basics.athlete_name` |
| `sport` | Derived | From `request_snapshot.basics.sport` |
| `role` | Derived | From `request_snapshot.basics.role` |
| `goal` | Derived | From `request_snapshot.context.primary_goal` |
| `blueprint_label` | Derived | From `result_snapshot.summary.blueprint_selected` |
| `week_label` | Derived | From `result_snapshot.summary.competition_window` |
| `request_snapshot` | Canonical | Exact request payload at time of generation |
| `result_snapshot` | Canonical | Exact response payload at time of generation |
| `coach_notes` | Canonical | User-editable |
| `internal_notes` | Canonical | User-editable |

## Save/Load Lifecycle

```
Generate Program
  │
  ▼
RawProgramResponse returned (not saved yet)
  │
  ▼
User clicks "Save"
  │
  ▼
POST /api/programs  →  artifact_store.save_artifact()
  │
  ▼
JSON written to .forge_artifacts/{id}.json
  │
  ▼
Artifact summary returned to frontend
```

```
User opens Library Drawer
  │
  ▼
GET /api/programs  →  artifact_store.list_artifacts()
  │
  ▼
Summary metadata returned (no payloads)
  │
  ▼
User selects artifact
  │
  ▼
GET /api/programs/{id}  →  artifact_store.load_artifact()
  │
  ▼
Full artifact (with payloads) returned → transformer normalizes → UI renders
```

```
User clicks "Duplicate"
  │
  ▼
POST /api/programs/{id}/duplicate  →  artifact_store.duplicate_artifact()
  │
  ▼
New artifact file created with incremented version
```

```
User clicks "Delete"
  │
  ▼
DELETE /api/programs/{id}  →  artifact_store.delete_artifact()
  │
  ▼
File removed from disk
```

## Directory Layout

```
.forge_artifacts/
├── prog_a1b2c3d4e5f6.json
├── prog_f6e5d4c3b2a1.json
└── ...
```

Each file is self-contained JSON with no external references.

## Git

Add `.forge_artifacts/` to `.gitignore` to prevent committing generated artifacts.

## Future Considerations

- Migrate to SQLite when/if concurrent access, search, or relational queries are needed.
- Add artifact export/import for sharing programs between coaches.
- Add request/response schema versioning for forward compatibility.
