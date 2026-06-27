"""Team template persistence — reuses artifact_store directory with type=team prefix."""
from __future__ import annotations
import json
import os
import uuid
from datetime import datetime, timezone
from typing import Optional

from .artifact_store import ARTIFACTS_DIR, _ensure_dir


def _team_path(template_id: str) -> str:
    return os.path.join(ARTIFACTS_DIR, f"team_{template_id}.json")


def save_team_template(template: dict) -> dict:
    _ensure_dir()
    tid = template.get("id") or uuid.uuid4().hex[:12]
    now = datetime.now(timezone.utc).isoformat()
    artifact = {
        "type": "team",
        "id": tid,
        "created_at": now,
        "updated_at": now,
        "version": 1,
        **template,
        "id": tid,
    }
    with open(_team_path(tid), "w", encoding="utf-8") as f:
        json.dump(artifact, f, indent=2, default=str)
    return artifact


def load_team_template(template_id: str) -> Optional[dict]:
    path = _team_path(template_id)
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def list_team_templates() -> list[dict]:
    _ensure_dir()
    templates = []
    for fname in sorted(os.listdir(ARTIFACTS_DIR), reverse=True):
        if fname.startswith("team_") and fname.endswith(".json"):
            try:
                with open(os.path.join(ARTIFACTS_DIR, fname), "r", encoding="utf-8") as f:
                    t = json.load(f)
                templates.append({
                    "id": t["id"],
                    "name": t.get("name", ""),
                    "sport": t.get("sport", ""),
                    "level": t.get("level", ""),
                    "phase": t.get("phase", ""),
                    "goal": t.get("goal", ""),
                    "created_at": t.get("created_at", ""),
                    "updated_at": t.get("updated_at", ""),
                    "program_length_weeks": t.get("program_length_weeks", 0),
                    "sessions_per_week": t.get("sessions_per_week", 0),
                })
            except (json.JSONDecodeError, KeyError):
                continue
    return templates


def update_team_template(template_id: str, **fields) -> Optional[dict]:
    template = load_team_template(template_id)
    if template is None:
        return None
    allowed = {"name", "sport", "level", "phase", "goal", "program_length_weeks",
               "sessions_per_week", "minutes_per_session", "match_day",
               "team_training_days", "heavy_field_days", "travel_days",
               "equipment_profile", "coach_notes", "program_snapshot"}
    for k, v in fields.items():
        if k in allowed:
            template[k] = v
    template["updated_at"] = datetime.now(timezone.utc).isoformat()
    with open(_team_path(template_id), "w", encoding="utf-8") as f:
        json.dump(template, f, indent=2, default=str)
    return template


def delete_team_template(template_id: str) -> bool:
    path = _team_path(template_id)
    if not os.path.exists(path):
        return False
    os.remove(path)
    return True
