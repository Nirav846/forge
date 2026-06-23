# FORGE Program Artifact Schema v1

## Overview

Each saved program is a single JSON file stored in `.forge_artifacts/`. The schema is self-contained — all request/response data is embedded.

## Current Version

```
SCHEMA_VERSION = 1
```

## Structure

```json
{
  "id": "prog_a1b2c3d4e5f6",
  "schema_version": 1,
  "created_at": "2026-06-23T06:00:00+00:00",
  "updated_at": "2026-06-23T06:30:00+00:00",
  "version": 1,
  "status": "draft",

  "athlete_display_name": "John Smith",
  "sport": "rugby",
  "role": "prop",
  "goal": "strength",
  "blueprint_label": "Rugby Strength",
  "week_label": "Off-season",
  "mode": "core",

  "coach_notes": "",
  "internal_notes": "",
  "version_notes": "",
  "duplicated_from": null,

  "request_snapshot": { /* ... full ProgramRequest payload */ },
  "result_snapshot": { /* ... full RawProgramResponse payload */ }
}
```

## Field Reference

### Identity Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | `prog_` prefix + 12 hex chars from UUID4 |
| `schema_version` | integer | yes | Always `1` for v1 artifacts. Incremented on breaking changes. |
| `created_at` | string (ISO 8601) | yes | UTC timestamp of first save |
| `updated_at` | string (ISO 8601) | yes | UTC timestamp of last modification |
| `version` | integer | yes | Starts at 1, incremented on duplicate |
| `status` | string | yes | One of: `draft`, `reviewed` |

### Display Metadata (Derived)

These fields are extracted from request/response snapshots for quick scanning in list views.

| Field | Source | Description |
|-------|--------|-------------|
| `athlete_display_name` | `request_snapshot.basics.athlete_name` | Display name for library |
| `sport` | `request_snapshot.basics.sport` | Sport or "General" |
| `role` | `request_snapshot.basics.role` | Position/role or "-" |
| `goal` | `request_snapshot.context.primary_goal` | Goal or "-" |
| `blueprint_label` | `result_snapshot.summary.blueprint_selected` | Blueprint name |
| `week_label` | `result_snapshot.summary.competition_window` | Competition window label |
| `mode` | `request_snapshot.mode` | `core` or `premium` |

### Coach Notes

| Field | Type | Description |
|-------|------|-------------|
| `coach_notes` | string | Coach-facing notes (set on save or via PATCH) |
| `internal_notes` | string | Internal use notes (set on save or via PATCH) |
| `version_notes` | string | Auto-set on duplicate: "Duplicated from prog_xxx" |
| `duplicated_from` | string or null | Original artifact ID if duplicated |

### Payload Snapshots

| Field | Type | Description |
|-------|------|-------------|
| `request_snapshot` | object | Exact `ProgramRequest` payload at time of generation/save |
| `result_snapshot` | object | Exact `RawProgramResponse` payload at time of generation/save |

## List View (Summary)

When listing artifacts, payloads are stripped. List entries contain only:

```
id, schema_version, created_at, updated_at, version, status,
athlete_display_name, sport, role, goal, blueprint_label,
week_label, mode, coach_notes, internal_notes, version_notes,
duplicated_from
```

## Schema Evolution Policy

1. **Additive changes** (adding new fields): Increment `SCHEMA_VERSION` minor (e.g. 1 → 1.1). Old artifacts remain readable.
2. **Breaking changes** (removing/renaming fields): Increment `SCHEMA_VERSION` major (e.g. 1 → 2). Old artifacts must be migrated or marked as legacy.
3. **On load**: Code should check `schema_version` and apply backward-compat logic for missing fields. Old artifacts without `schema_version` should still load gracefully.

## File Path

```
.forge_artifacts/{id}.json
```

Where `id` is `prog_` + 12 hex chars (e.g. `prog_a1b2c3d4e5f6.json`).

## Example

```json
{
  "id": "prog_a1b2c3d4e5f6",
  "schema_version": 1,
  "created_at": "2026-06-23T06:00:00+00:00",
  "updated_at": "2026-06-23T06:30:00+00:00",
  "version": 1,
  "status": "draft",
  "athlete_display_name": "John Smith",
  "sport": "rugby",
  "role": "prop",
  "goal": "strength",
  "blueprint_label": "Rugby Strength (Front Row)",
  "week_label": "Off-season",
  "mode": "core",
  "coach_notes": "Reduce volume in week 3 per coach feedback",
  "internal_notes": "",
  "version_notes": "",
  "duplicated_from": null,
  "request_snapshot": { "mode": "core", "basics": { ... }, "context": { ... }, "advanced": { ... } },
  "result_snapshot": { "metadata": { ... }, "summary": { ... }, "sessions": [...], ... }
}
```
