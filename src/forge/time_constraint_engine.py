"""Time Constraint Engine — redesigns sessions for available time budget."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from .models import FamilyCode, SessionBlock, SessionIntent


@dataclass
class RedesignedSession:
    """Result of redesigning a session for a given time budget."""
    structure_type: str
    total_duration: int
    notes: list[str]


@dataclass
class TimeConstraintConfig:
    """Configuration for time constraint redesign."""
    available_minutes: int
    warmup_minutes: int = 10
    cooldown_minutes: int = 5
    transition_seconds: int = 30


def redesign_session_for_time(
    session_intent: Optional[SessionIntent],
    available_minutes: int,
    exercise_slots: list[FamilyCode],
    config: Optional[TimeConstraintConfig] = None,
) -> RedesignedSession:
    """Redesign the session to fit within the available time budget."""
    if config is None:
        config = TimeConstraintConfig(available_minutes=available_minutes)

    structure_type = _determine_structure(available_minutes)
    slots = _prioritise_slots(exercise_slots, session_intent, structure_type)
    structured_slots = _apply_structure(slots, structure_type)

    notes = [f"{structure_type.capitalize()} structure — {available_minutes} min session"]
    if structure_type == "minimalist":
        notes.append("Primary exercises only, high density, minimal rest")
    elif structure_type == "condensed":
        notes.append("Supersets where possible, moderate rest")
    elif structure_type == "extended":
        notes.append("Extended structure with adequate rest between sets")

    return RedesignedSession(
        structure_type=structure_type,
        total_duration=available_minutes,
        notes=notes,
    )


def _determine_structure(available_minutes: int) -> str:
    """Map available minutes to a session structure type."""
    if available_minutes <= 35:
        return "minimalist"
    elif available_minutes <= 50:
        return "condensed"
    elif available_minutes <= 70:
        return "standard"
    else:
        return "extended"


def _prioritise_slots(
    slots: list[FamilyCode],
    intent: Optional[SessionIntent],
    structure: str,
) -> list[FamilyCode]:
    """Filter and prioritise slots based on structure and intent."""
    max_slots = {"minimalist": 4, "condensed": 5, "standard": 7, "extended": 9}.get(structure, 7)

    if not intent or not intent.movement_priorities:
        return slots[:max_slots]

    priority_families = intent.movement_priorities
    scored = []
    for slot in slots:
        score = 0
        if slot.value in priority_families:
            score += 10
        if slot.value in ("Acc", "Core", "Rot"):
            score -= 2
        if "sprint" in intent.qualities and slot.value == "Sprint":
            score += 3
        if "velocity" in intent.qualities and slot.value in ("Sprint", "Plyo"):
            score += 2
        if "eccentric" in intent.qualities and slot.value in ("DLHD", "SLHD", "Landing"):
            score += 2
        scored.append((score, slot))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [slot for _, slot in scored[:max_slots]]


def _apply_structure(
    slots: list[FamilyCode],
    structure: str,
) -> list[FamilyCode]:
    """Apply structural changes (supersets, order) to the slots."""
    if structure in ("minimalist", "condensed"):
        # Reorder: try to alternate upper/lower
        lower = [f for f in slots if f.value in ("DLKD", "DLHD", "SLKD", "SLHD", "Sprint", "Plyo")]
        upper = [f for f in slots if f.value in ("HPush", "HPull", "VPush", "VPull")]
        other = [f for f in slots if f not in lower and f not in upper]
        reordered = []
        i, j = 0, 0
        while i < len(lower) or j < len(upper):
            if i < len(lower):
                reordered.append(lower[i])
                i += 1
            if j < len(upper):
                reordered.append(upper[j])
                j += 1
        reordered.extend(other)
        return reordered
    return slots


def adjust_prescriptions_for_time(
    blocks: list[SessionBlock],
    available_minutes: int,
    structure_type: str,
    config: TimeConstraintConfig,
) -> tuple[list[SessionBlock], list[str]]:
    """Adjust prescriptions (sets, rest) to fit within time budget."""
    notes = []
    available_for_exercises = available_minutes - config.warmup_minutes - config.cooldown_minutes
    if available_for_exercises <= 0:
        return blocks, ["No time remaining for exercises after warmup/cooldown"]

    total_estimated = _estimate_total_duration(blocks, config)
    if total_estimated <= available_for_exercises:
        return blocks, ["Session fits within available time"]

    compression_factor = available_for_exercises / total_estimated
    notes.append(f"Exercises compressed to {available_for_exercises} min (factor: {compression_factor:.2f})")

    for block in blocks:
        if not block.prescription:
            continue
        # Reduce rest periods first
        if block.prescription.rest_seconds:
            new_rest = int(block.prescription.rest_seconds * compression_factor)
            new_rest = max(30, new_rest)
            block.prescription.rest_seconds = new_rest

        # If still tight, reduce sets (keep at least 2)
        if compression_factor < 0.7 and block.prescription.sets:
            import re
            nums = re.findall(r"\d+", block.prescription.sets)
            if nums:
                ints = [int(n) for n in nums]
                reduced = [max(2, s - 1) for s in ints]
                if len(reduced) == 1:
                    block.prescription.sets = str(reduced[0])
                elif reduced[0] == reduced[1]:
                    block.prescription.sets = str(reduced[0])
                else:
                    block.prescription.sets = f"{reduced[0]}-{reduced[1]}"

    # Condensed/minimalist: superset-style rest reduction
    if structure_type in ("minimalist", "condensed"):
        for block in blocks:
            if block.prescription and block.prescription.rest_seconds:
                block.prescription.rest_seconds = int(block.prescription.rest_seconds * 0.5)
        notes.append("Superset rest intervals applied for density")

    return blocks, notes


def _estimate_total_duration(
    blocks: list[SessionBlock],
    config: TimeConstraintConfig,
) -> int:
    """Estimate total exercise time in minutes for the given blocks."""
    total_seconds = (config.warmup_minutes + config.cooldown_minutes) * 60

    for block in blocks:
        if not block.prescription:
            total_seconds += config.transition_seconds
            continue
        sets = block.prescription.sets or "3"
        reps = block.prescription.reps or "0"

        import re
        set_nums = re.findall(r"\d+", sets)
        avg_sets = sum(int(n) for n in set_nums) / len(set_nums) if set_nums else 3

        rep_nums = re.findall(r"\d+", reps)
        if rep_nums:
            avg_reps = sum(int(n) for n in rep_nums) / len(rep_nums)
        else:
            avg_reps = 0

        set_duration = avg_reps * 5 + 10  # 5 sec per rep + 10 sec setup
        total_seconds += avg_sets * set_duration
        rest = block.prescription.rest_seconds or 60
        total_seconds += (avg_sets - 1) * rest
        total_seconds += config.transition_seconds

    return int(total_seconds // 60)
