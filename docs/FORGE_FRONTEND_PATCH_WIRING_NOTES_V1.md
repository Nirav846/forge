# FORGE Frontend PATCH Wiring Notes

## Overview

`PATCH /api/programs/{id}` was introduced in Wave 10 for lightweight field
updates. Wave 10.5 wired the frontend to use it. This doc documents the
contract, the UI flows that use it, and failure-handling expectations.

## Fields updated by PATCH

| Field | Type | Example | Notes |
|---|---|---|---|
| `status` | string | `"draft"` / `"reviewed"` | Toggles review workflow |
| `coach_notes` | string | Any free-text | Coach-facing notes |
| `internal_notes` | string | Any free-text | Internal-use notes |

The whitelist in `artifact_store.py` (`ALLOWED_UPDATE_FIELDS`) controls
which fields PATCH accepts. Currently it is `{"status", "coach_notes",
"internal_notes"}`. Unknown fields are silently ignored (not rejected).

## Save vs PATCH: which action uses what

| Action | Method | When |
|---|---|---|
| Initial save | `POST /api/programs` (full) | First save of a generated program |
| Re-save (update) | `POST /api/programs` (full) | Explicit "Save" button click — overwrites request + response payload |
| Toggle reviewed | `PATCH /api/programs/{id}` | Mark Reviewed / Approve button |
| Update coach notes | `PATCH /api/programs/{id}` | Blur of coach notes textarea |
| Update internal notes | `PATCH /api/programs/{id}` | Blur of internal notes textarea |

The full save (`POST`) writes the complete request and response payload.
PATCH updates only the specified fields and does not touch the payloads.

## Save / review flows

### Review status toggle
1. User clicks "Approve" (or "Mark Reviewed").
2. Frontend immediately toggles the local status (optimistic).
3. Frontend calls `PATCH /api/programs/{id}` with `{ status: "reviewed" }`.
4. On success: status badge updates, `updated_at` refreshes.
5. On failure: status reverts to previous value, error toast shown.

### Coach notes edit
1. User types in the coach notes textarea.
2. On blur, frontend calls `PATCH /api/programs/{id}` with
   `{ coach_notes: "<current text>" }`.
3. On success: local state updated, save indicator shows "Saved".
4. On failure: indicator shows "Error", text preserved for retry.

### Internal notes edit
Same flow as coach notes, but uses `internal_notes` field.

## Failure handling expectations

- **Network error**: Status reverts on review toggle; notes text is
  preserved on notes edit. User can retry.
- **Backend returns error**: Same behavior as network error — local state
  is not corrupted.
- **Backend unreachable (mock fallback mode)**: PATCH calls are silently
  skipped. The UI functions in local-only mode (no persistence across
  page reloads, but in-memory state is correct during the session).

## Artifact update contract

`PATCH /api/programs/{id}`

Request body:
```json
{
  "status": "reviewed",
  "coach_notes": "Coach-facing text here",
  "internal_notes": "Internal notes here"
}
```

All fields are optional. Only provided fields are updated.

Response:
```json
{
  "id": "<artifact_id>",
  "status": "reviewed",
  "coach_notes": "Coach-facing text here",
  "internal_notes": "Internal notes here",
  "updated_at": "2026-06-23T12:00:00+00:00"
}
```

Returns the full updated artifact. `updated_at` always changes on success.

## Future extension points

- Adding fields to PATCH: add the field name to `ALLOWED_UPDATE_FIELDS`
  in `artifact_store.py`, then wire the frontend field to call
  `updateArtifact(id, { field: value })`.
- Batch PATCH: currently one field group at a time. Could batch by
  debouncing the notes save timer.
- Optimistic retry: notes could benefit from a short debounce + retry
  if the UX pattern proves valuable during trials.
