"""Local JSON file-based artifact persistence for FORGE programs."""
from __future__ import annotations
import json
import os
import uuid
import shutil
from datetime import datetime, timezone
from typing import Optional


ARTIFACTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".forge_artifacts")

SCHEMA_VERSION = 1
"""Current artifact schema version. Increment when breaking structure changes are made."""


def _ensure_dir():
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)


def _artifact_path(program_id: str) -> str:
    return os.path.join(ARTIFACTS_DIR, f"{program_id}.json")


# ── Coach Override Merge / Normalize ───────────────────────────────────


def _normalize_coach_overrides(raw: dict) -> dict:
    """Convert old flat override shape to nested session-first shape.

    Old shape (v1.1):
      { "session_locks": {"sess_0": true},
        "session_notes": {"sess_0": "note"},
        "exercise_swaps": {"ex_0": {...}},
        "prescription_edits": {"ex_0": {...}} }

    New shape (v1.2+):
      { "sessions": {"sess_0": { "locked": true, "note": "note",
          "exercises": {"ex_0": { "swap": {...}, "prescription": {...}}}}} }

    Returns the normalized dict. Safe to call on already-normalized data.
    """
    if raw is None or not isinstance(raw, dict):
        return {}
    # Already nested? Look for top-level "sessions" key.
    if "sessions" in raw:
        return raw
    # Convert flat layout keys into nested form.
    flat_locks = raw.get("session_locks", {}) or {}
    flat_notes = raw.get("session_notes", {}) or {}
    flat_swaps = raw.get("exercise_swaps", {}) or {}
    flat_edits = raw.get("prescription_edits", {}) or {}

    if not (flat_locks or flat_notes or flat_swaps or flat_edits):
        return raw  # empty, keep as-is

    sessions: dict = {}

    # Collect exercise-level overrides keyed by exercise_id
    # but we need to know which session each exercise belongs to.
    # Flat format stores by exercise_id directly — we store them
    # under a synthetic "" session key for the frontend to sort out,
    # OR we can store them under the first session that uses them.
    # Safest: put them under a session "" if we can't determine mapping.
    # Better: we use the existing frontend rebuild logic — just keep
    # a flat exercises map at top level for migration compatibility.

    # Actually, the simplest approach: store flat exercise data under
    # an empty session key and let the frontend access it either way.
    # Even simpler: just keep it as a flat exercise-level map but
    # nest session-level data. This is what the old format essentially was,
    # and the new format nests session-level data.

    # For migration: put session-level fields into sessions map,
    # put exercise-level fields into a top-level "exercises" key
    # that mirrors the old flat format under sessions[""].exercises.
    all_session_ids = set(list(flat_locks.keys()) + list(flat_notes.keys()))
    for sid in all_session_ids:
        so: dict = {}
        if sid in flat_locks:
            so["locked"] = flat_locks[sid]
        if sid in flat_notes:
            so["note"] = flat_notes[sid]
        sessions[sid] = so

    # For exercise-level overrides, since we can't map them to
    # sessions in the old flat format, store them in each session's
    # exercises map if that session exists, otherwise a generic key.
    if flat_swaps or flat_edits:
        ex_target: dict = {}
        for ex_id, swap_data in flat_swaps.items():
            ex_target[ex_id] = ex_target.get(ex_id, {})
            ex_target[ex_id]["swap"] = swap_data
        for ex_id, edit_data in flat_edits.items():
            ex_target[ex_id] = ex_target.get(ex_id, {})
            ex_target[ex_id]["prescription"] = edit_data

        if ex_target:
            # Try to distribute to known sessions
            placed = set()
            for sid in sessions:
                sessions[sid]["exercises"] = ex_target
                placed = set(ex_target.keys())
                break
            if not placed:
                sessions["_ex"] = {"exercises": ex_target}

    return {"sessions": sessions} if sessions else {}


def _merge_coach_overrides(existing: dict, patch: dict) -> dict:
    """Deep-merge a coach_overrides patch into existing overrides.

    Semantics:
      - Merge by session_id then exercise_id.
      - Setting a field to None removes it (null-clear).
      - Empty containers (exercise cleared, session cleared) are pruned.
      - Sibling fields in the same session are never wiped.
      - Returns the new coach_overrides dict (does not mutate inputs).

    The `patch` dict always uses the new nested shape:
      { "sessions": { "sess_0": { "locked": true, "note": "string"|None,
          "exercises": { "ex_0": { "swap": {...}|None,
                                    "prescription": {...}|None }}}}}}
    """
    existing = _normalize_coach_overrides(existing)
    patch = _normalize_coach_overrides(patch)
    if not patch:
        return existing
    if not existing:
        existing = {}

    existing_sessions: dict = existing.get("sessions", {})
    patch_sessions: dict = patch.get("sessions", {})

    if not patch_sessions:
        return existing

    result_sessions: dict = dict(existing_sessions)

    for sid, patch_session in patch_sessions.items():
        if patch_session is None:
            result_sessions.pop(sid, None)
            continue
        if not isinstance(patch_session, dict):
            continue

        current_session: dict = dict(result_sessions.get(sid, {})) if sid in result_sessions else {}

        # Merge session-level fields
        for field in ("locked", "note"):
            if field in patch_session:
                val = patch_session[field]
                if val is None:
                    current_session.pop(field, None)
                else:
                    current_session[field] = val

        # Merge exercise-level overrides
        patch_exercises = patch_session.get("exercises")
        if patch_exercises is not None:
            current_exercises: dict = dict(current_session.get("exercises", {})) if "exercises" in current_session else {}
            if not isinstance(patch_exercises, dict):
                pass  # ignore non-dict
            else:
                for ex_id, patch_ex in patch_exercises.items():
                    if patch_ex is None:
                        current_exercises.pop(ex_id, None)
                        continue
                    if not isinstance(patch_ex, dict):
                        continue
                    current_ex: dict = dict(current_exercises.get(ex_id, {})) if ex_id in current_exercises else {}
                    for ex_field in ("swap", "prescription"):
                        if ex_field in patch_ex:
                            val = patch_ex[ex_field]
                            if val is None:
                                current_ex.pop(ex_field, None)
                            else:
                                current_ex[ex_field] = val
                    if current_ex:
                        current_exercises[ex_id] = current_ex
                    else:
                        current_exercises.pop(ex_id, None)

                if current_exercises:
                    current_session["exercises"] = current_exercises
                else:
                    current_session.pop("exercises", None)

        # Prune empty session
        if current_session:
            result_sessions[sid] = current_session
        else:
            result_sessions.pop(sid, None)

    result: dict = {}
    if result_sessions:
        result["sessions"] = result_sessions
    return result


# ── CRUD Operations ─────────────────────────────────────────────────


def save_artifact(
    request_payload: dict,
    response_payload: dict,
    program_id: Optional[str] = None,
    status: str = "draft",
    coach_notes: str = "",
    internal_notes: str = "",
    version: int = 1,
    duplicated_from: Optional[str] = None,
) -> dict:
    """Save a program artifact. Returns the saved artifact record."""
    _ensure_dir()
    artifact_id = program_id or f"prog_{uuid.uuid4().hex[:12]}"
    now = datetime.now(timezone.utc).isoformat()

    # Extract display metadata from the response
    summary = response_payload.get("summary", {})
    meta = response_payload.get("metadata", {})

    artifact = {
        "id": artifact_id,
        "schema_version": SCHEMA_VERSION,
        "created_at": now,
        "updated_at": now,
        "version": version,
        "status": status,
        "athlete_display_name": request_payload.get("basics", {}).get("athlete_name", "Unknown Athlete"),
        "sport": request_payload.get("basics", {}).get("sport", "General"),
        "role": request_payload.get("basics", {}).get("role", "-"),
        "goal": request_payload.get("context", {}).get("primary_goal", "-"),
        "blueprint_label": summary.get("blueprint_selected", "Custom Block"),
        "week_label": summary.get("competition_window", "-"),
        "mode": request_payload.get("mode", "core"),
        "coach_notes": coach_notes,
        "internal_notes": internal_notes,
        "version_notes": "",
        "duplicated_from": duplicated_from,
        "coach_overrides": {},
        "request_snapshot": request_payload,
        "result_snapshot": response_payload,
    }

    with open(_artifact_path(artifact_id), "w", encoding="utf-8") as f:
        json.dump(artifact, f, indent=2, default=str)

    return artifact


def load_artifact(program_id: str) -> Optional[dict]:
    """Load one artifact by ID. Normalizes coach_overrides on load."""
    path = _artifact_path(program_id)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        artifact = json.load(f)
    # Normalize coach_overrides on load for backward compat
    if "coach_overrides" in artifact:
        artifact["coach_overrides"] = _normalize_coach_overrides(artifact["coach_overrides"])
    return artifact


def list_artifacts() -> list[dict]:
    """List all saved artifacts (summary metadata only, no payloads)."""
    _ensure_dir()
    artifacts = []
    for fname in sorted(os.listdir(ARTIFACTS_DIR), reverse=True):
        if fname.endswith(".json"):
            path = os.path.join(ARTIFACTS_DIR, fname)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    artifact = json.load(f)
                overrides = artifact.get("coach_overrides", {})
                overrides = _normalize_coach_overrides(overrides)
                artifacts.append({
                    "id": artifact["id"],
                    "schema_version": artifact.get("schema_version"),
                    "created_at": artifact["created_at"],
                    "updated_at": artifact["updated_at"],
                    "version": artifact.get("version", 1),
                    "status": artifact.get("status", "draft"),
                    "athlete_display_name": artifact.get("athlete_display_name", "Unknown"),
                    "sport": artifact.get("sport", ""),
                    "role": artifact.get("role", ""),
                    "goal": artifact.get("goal", ""),
                    "blueprint_label": artifact.get("blueprint_label", ""),
                    "week_label": artifact.get("week_label", ""),
                    "mode": artifact.get("mode", "core"),
                    "coach_notes": artifact.get("coach_notes", ""),
                    "internal_notes": artifact.get("internal_notes", ""),
                    "version_notes": artifact.get("version_notes", ""),
                    "duplicated_from": artifact.get("duplicated_from"),
                    "coach_overrides": overrides,
                })
            except (json.JSONDecodeError, KeyError):
                continue
    return artifacts


def update_artifact(program_id: str, **fields) -> Optional[dict]:
    """Update specific fields on an existing artifact. Returns the updated artifact or None."""
    artifact = load_artifact(program_id)
    if artifact is None:
        return None
    allowed = {"status", "coach_notes", "internal_notes", "version_notes", "coach_overrides"}
    for key, val in fields.items():
        if key in allowed:
            if key == "coach_overrides" and val is not None:
                existing = artifact.get("coach_overrides", {})
                artifact["coach_overrides"] = _merge_coach_overrides(existing, val)
            else:
                artifact[key] = val
    artifact["updated_at"] = datetime.now(timezone.utc).isoformat()
    with open(_artifact_path(program_id), "w", encoding="utf-8") as f:
        json.dump(artifact, f, indent=2, default=str)
    return artifact


def delete_artifact(program_id: str) -> bool:
    """Delete one artifact. Returns True if deleted, False if not found."""
    path = _artifact_path(program_id)
    if not os.path.exists(path):
        return False
    os.remove(path)
    return True


def duplicate_artifact(program_id: str) -> Optional[dict]:
    """Duplicate an artifact. Returns the new artifact or None if not found."""
    original = load_artifact(program_id)
    if original is None:
        return None

    new_id = f"prog_{uuid.uuid4().hex[:12]}"
    now = datetime.now(timezone.utc).isoformat()

    new_artifact = dict(original)
    new_artifact["id"] = new_id
    new_artifact["created_at"] = now
    new_artifact["updated_at"] = now
    new_artifact["version"] = original.get("version", 1) + 1
    new_artifact["status"] = "draft"
    new_artifact["duplicated_from"] = program_id
    new_artifact["version_notes"] = f"Duplicated from {program_id}"
    new_artifact["coach_notes"] = ""
    new_artifact["internal_notes"] = ""
    new_artifact["coach_overrides"] = {}

    with open(_artifact_path(new_id), "w", encoding="utf-8") as f:
        json.dump(new_artifact, f, indent=2, default=str)

    return new_artifact
