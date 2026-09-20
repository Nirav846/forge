"""Adaptation diff - compares source and new program snapshots for duplicateFrom."""
from __future__ import annotations
from typing import Optional


def build_adaptation_log(
    source_request: dict,
    source_response: dict,
    new_request: dict,
    new_response: dict,
) -> dict:
    """Compare source and new program payloads and log what changed."""
    changes: list[str] = []

    src_basics = source_request.get("basics", {})
    new_basics = new_request.get("basics", {})
    src_ctx = source_request.get("context", {})
    new_ctx = new_request.get("context", {})
    src_adv = source_request.get("advanced", {})
    new_adv = new_request.get("advanced", {})

    for field, label in [("athlete_name", "Athlete"), ("sport", "Sport"),
                         ("role", "Role"), ("level", "Level"),
                         ("age", "Age"), ("training_age_years", "Training age"),
                         ("available_minutes", "Available minutes"),
                         ("frequency_per_week", "Frequency"),
                         ("days_to_match", "Days to match")]:
        old = src_basics.get(field)
        new = new_basics.get(field)
        if old is not None and new is not None and str(old) != str(new):
            changes.append(f"{label}: {old} -> {new}")

    for field, label in [("primary_goal", "Goal"), ("current_phase", "Phase"),
                         ("equipment_profile", "Equipment")]:
        old = src_ctx.get(field)
        new = new_ctx.get(field)
        if old is not None and new is not None and str(old) != str(new):
            changes.append(f"{label}: {old} -> {new}")

    old_injuries = set(src_adv.get("injury_risk_flags", []) or [])
    new_injuries = set(new_adv.get("injury_risk_flags", []) or [])
    added = new_injuries - old_injuries
    removed = old_injuries - new_injuries
    if added:
        changes.append(f"Injury flags added: {', '.join(sorted(added))}")
    if removed:
        changes.append(f"Injury flags removed: {', '.join(sorted(removed))}")

    for field, label in [("force_velocity_profile", "F-V profile"),
                         ("cmj_band", "CMJ"), ("sprint_10m_band", "Sprint 10m"),
                         ("aerobic_band", "Aerobic")]:
        old = src_adv.get(field)
        new = new_adv.get(field)
        if old is not None and new is not None and str(old) != str(new):
            changes.append(f"{label}: {old} -> {new}")

    src_summary = source_response.get("summary", {})
    new_summary = new_response.get("summary", {})
    src_weeks = src_summary.get("total_weeks")
    new_weeks = new_summary.get("total_weeks")
    if src_weeks is not None and new_weeks is not None and src_weeks != new_weeks:
        changes.append(f"Weeks: {src_weeks} -> {new_weeks}")
    src_freq = src_summary.get("weekly_frequency")
    new_freq = new_summary.get("weekly_frequency")
    if src_freq is not None and new_freq is not None and src_freq != new_freq:
        changes.append(f"Frequency: {src_freq}x/wk -> {new_freq}x/wk")
    src_blueprint = src_summary.get("blueprint_selected")
    new_blueprint = new_summary.get("blueprint_selected")
    if src_blueprint and new_blueprint and src_blueprint != new_blueprint:
        changes.append(f"Blueprint: {src_blueprint} -> {new_blueprint}")

    return {
        "source_artifact_id": source_request.get("_artifact_id", ""),
        "changes": changes,
        "change_count": len(changes),
    }
