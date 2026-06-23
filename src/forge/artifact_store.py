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
        "request_snapshot": request_payload,
        "result_snapshot": response_payload,
    }

    with open(_artifact_path(artifact_id), "w", encoding="utf-8") as f:
        json.dump(artifact, f, indent=2, default=str)

    return artifact


def load_artifact(program_id: str) -> Optional[dict]:
    """Load one artifact by ID."""
    path = _artifact_path(program_id)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


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
                # Strip payloads for list view
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
                })
            except (json.JSONDecodeError, KeyError):
                continue
    return artifacts


def update_artifact(program_id: str, **fields) -> Optional[dict]:
    """Update specific fields on an existing artifact. Returns the updated artifact or None."""
    artifact = load_artifact(program_id)
    if artifact is None:
        return None
    allowed = {"status", "coach_notes", "internal_notes", "version_notes"}
    for key, val in fields.items():
        if key in allowed:
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

    with open(_artifact_path(new_id), "w", encoding="utf-8") as f:
        json.dump(new_artifact, f, indent=2, default=str)

    return new_artifact
