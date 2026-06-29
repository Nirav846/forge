"""Planning layer: converts athlete profile + blueprint + calendar into weekly strategies and session intents."""

from typing import Optional
from .models import AthleteProfile, MovementSlot, SessionIntent, SessionPlacement, WeeklyStrategy, WeeklyProgressionPlan
from .progression_planner import plan_weekly_progression
from .role_week_planning import RoleWeekProfile
from .role_profiles import get_slot_template

# ── Constants ─────────────────────────────────────────────

DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

WEEK_TYPE_PURPOSES = {
    "accumulation": {"primary_focus": "strength", "stress": "moderate", "volume_mod": 1.0, "intensity_mod": 0.85},
    "intensification": {"primary_focus": "strength", "stress": "high", "volume_mod": 1.0, "intensity_mod": 1.0},
    "realization": {"primary_focus": "power", "stress": "high", "volume_mod": 0.85, "intensity_mod": 1.05},
    "taper": {"primary_focus": "maintenance", "stress": "low", "volume_mod": 0.7, "intensity_mod": 0.9},
    "test": {"primary_focus": "testing", "stress": "low", "volume_mod": 0.6, "intensity_mod": 0.8},
}

DEFAULT_EXPOSURE_BUDGETS = {
    "Fast Bowler": {"sprint": 3, "jump": 2, "landing": 4, "eccentric": 3, "rotational": 2, "conditioning": 2, "upper_push": 2, "upper_pull": 2},
    "Spin Bowler": {"sprint": 1, "jump": 1, "landing": 2, "eccentric": 2, "rotational": 4, "conditioning": 2, "upper_push": 2, "upper_pull": 2},
    "Batter": {"sprint": 2, "jump": 2, "landing": 2, "eccentric": 2, "rotational": 4, "conditioning": 1, "upper_push": 3, "upper_pull": 2},
    "Wicketkeeper": {"sprint": 2, "jump": 1, "landing": 2, "eccentric": 2, "rotational": 2, "conditioning": 1, "upper_push": 2, "upper_pull": 2},
    "All Rounder": {"sprint": 2, "jump": 2, "landing": 3, "eccentric": 3, "rotational": 3, "conditioning": 2, "upper_push": 2, "upper_pull": 2},
    "*": {"sprint": 2, "jump": 2, "landing": 2, "eccentric": 2, "rotational": 2, "conditioning": 2, "upper_push": 2, "upper_pull": 2},
}

# Intent type for each circular distance before match day.
# dist=0 → match day itself, dist=1 → day before match, etc.
DIST_TO_INTENT = {
    0: "Recovery",
    1: "Primer",
    2: "Speed",
    3: "Power",
    4: "Strength",
    5: "Conditioning",
    6: "Conditioning",
}

# Day-selection priority (lower = picked first when slots are limited).
# Strength is the most important session type, then Power, then the rest.
DIST_PRIORITY = {
    4: 1,  # Strength
    3: 2,  # Power
    5: 3,  # Conditioning
    2: 4,  # Speed
    1: 5,  # Primer
    6: 6,  # Conditioning (cyclic overflow)
    0: 7,  # Recovery / match
}

INTENT_EXPOSURE_STRATEGIES = {
    "Strength": {"sprint": 1.0, "jump": 1.0, "landing": 1.2, "eccentric": 1.5, "rotational": 0.8, "conditioning": 0.5, "upper_push": 1.2, "upper_pull": 1.2},
    "Power": {"sprint": 1.2, "jump": 1.5, "landing": 1.2, "eccentric": 1.0, "rotational": 1.0, "conditioning": 0.5, "upper_push": 1.0, "upper_pull": 1.0},
    "Speed": {"sprint": 1.5, "jump": 0.5, "landing": 0.8, "eccentric": 0.5, "rotational": 0.5, "conditioning": 0.3, "upper_push": 0.5, "upper_pull": 0.5},
    "Primer": {"sprint": 0.3, "jump": 0.3, "landing": 0.3, "eccentric": 0.3, "rotational": 0.3, "conditioning": 0.2, "upper_push": 0.3, "upper_pull": 0.3},
    "Recovery": {"sprint": 0, "jump": 0, "landing": 0, "eccentric": 0.3, "rotational": 0, "conditioning": 0, "upper_push": 0, "upper_pull": 0},
    "Conditioning": {"sprint": 0.8, "jump": 0.5, "landing": 0.8, "eccentric": 0.5, "rotational": 0.5, "conditioning": 1.5, "upper_push": 0.5, "upper_pull": 0.5},
}

# ── Main Functions ────────────────────────────────────────

def plan_weekly_strategy(
    week_number: int,
    week_type: str,
    athlete: AthleteProfile,
    role_profile: Optional[dict],
    role_week_profile: RoleWeekProfile,
    calendar_context: dict,
) -> WeeklyStrategy:
    """Create a weekly strategy for the given week."""
    base = WEEK_TYPE_PURPOSES.get(week_type, WEEK_TYPE_PURPOSES["accumulation"])
    role_budget = _get_exposure_budget(role_profile, athlete.role)
    stress_mod = _calendar_stress_modifier(calendar_context, week_type)
    exposure_budget = _allocate_exposures(role_budget, base["stress"], stress_mod)

    # Calendar designs the week first — determines which days sessions land on,
    # what each session's intent type is, and how exposures are allocated.
    placements = design_weekly_structure(
        frequency=athlete.frequency_per_week,
        calendar_context=calendar_context,
        exposure_budget=exposure_budget,
    )

    # Generate progression plan for this week
    progression_plan = plan_weekly_progression(
        week_type=week_type,
        week_number=week_number,
        athlete=athlete,
        role_name=(role_profile or {}).get("role", athlete.role or ""),
    )

    session_intents = _generate_session_intents(
        week_type=week_type,
        frequency=athlete.frequency_per_week,
        athlete=athlete,
        role_profile=role_profile,
        calendar_context=calendar_context,
        exposure_budget=exposure_budget,
        placements=placements,
        progression_plan=progression_plan,
    )
    rationale = _build_weekly_rationale(week_type, role_profile, calendar_context, placements)

    return WeeklyStrategy(
        week_number=week_number,
        week_type=week_type,
        primary_focus=base["primary_focus"],
        stress_level=base["stress"],
        volume_modifier=base["volume_mod"],
        intensity_modifier=base["intensity_mod"],
        exposure_budget=exposure_budget,
        session_intents=session_intents,
        rationale=rationale,
        progression=progression_plan,
    )


def design_weekly_structure(
    frequency: int,
    calendar_context: dict,
    exposure_budget: dict[str, int],
) -> list[SessionPlacement]:
    """Plan which days sessions land on and what intent each has.

    When a match day is known, works backwards from it:
      Match day      → Recovery (or not selected at all — lowest priority)
      D-1            → Primer
      D-2, D-3      → Speed / Power
      D-4            → Strength
      D-5 / D-6     → Conditioning

    When no match day is specified, spreads sessions evenly.
    """
    if frequency <= 0:
        return []

    match_day = calendar_context.get("match_day")
    travel_days = set(calendar_context.get("travel_days", []))
    team_training_days = calendar_context.get("team_training_days", [])

    # Build the pool of usable days
    if team_training_days:
        available = sorted(set(team_training_days) - travel_days)
    else:
        available = sorted(set(range(7)) - travel_days)
    if not available:
        available = list(range(7))

    if match_day is None or match_day < 0:
        return _balanced_placements(frequency, available, exposure_budget)

    return _match_backed_placements(frequency, match_day, available, exposure_budget)


def _match_backed_placements(
    frequency: int,
    match_day: int,
    available: list[int],
    exposure_budget: dict[str, int],
) -> list[SessionPlacement]:
    """Design sessions backwards from match day."""

    def dist_before(d: int) -> int:
        return (match_day - d) % 7

    # Pick the best days from the available pool
    scored = sorted(
        available,
        key=lambda d: (DIST_PRIORITY.get(dist_before(d), 99), d),
    )

    selected = set(scored[:frequency])
    # If we still need slots, fall back to any remaining days
    if len(selected) < frequency:
        for d in range(7):
            if len(selected) >= frequency:
                break
            selected.add(d)

    sorted_days = sorted(selected)

    return [
        SessionPlacement(
            day_of_week=DAY_NAMES[d],
            intent_type=DIST_TO_INTENT.get(dist_before(d), "Strength"),
            session_number=i + 1,
            exposure_allocation=_intent_exposure_allocation(
                exposure_budget,
                DIST_TO_INTENT.get(dist_before(d), "Strength"),
                frequency,
            ),
        )
        for i, d in enumerate(sorted_days)
    ]


def _balanced_placements(
    frequency: int,
    available: list[int],
    exposure_budget: dict[str, int],
) -> list[SessionPlacement]:
    """Spread sessions evenly when no match day is set."""
    step = max(1, len(available) // frequency) if len(available) > frequency else 1
    chosen = []
    for i in range(frequency):
        idx = min(i * step, len(available) - 1)
        chosen.append(available[idx])
    while len(chosen) < frequency:
        remaining = [d for d in available if d not in chosen]
        if not remaining:
            remaining = [d for d in range(7) if d not in chosen]
        chosen.append(remaining[0] if remaining else 0)

    chosen = sorted(chosen[:frequency])
    cyclic_intents = ["Strength", "Power", "Speed", "Conditioning", "Primer", "Recovery"]

    return [
        SessionPlacement(
            day_of_week=DAY_NAMES[d],
            intent_type=cyclic_intents[i % len(cyclic_intents)],
            session_number=i + 1,
            exposure_allocation=_intent_exposure_allocation(
                exposure_budget,
                cyclic_intents[i % len(cyclic_intents)],
                frequency,
            ),
        )
        for i, d in enumerate(chosen)
    ]


def _intent_exposure_allocation(
    total_budget: dict[str, int],
    intent_type: str,
    frequency: int,
) -> dict[str, int]:
    """Allocate a portion of the weekly exposure budget to one session based on its intent."""
    weights = INTENT_EXPOSURE_STRATEGIES.get(intent_type, INTENT_EXPOSURE_STRATEGIES["Strength"])
    alloc = {}
    for key, total in total_budget.items():
        base = total // frequency
        weight = weights.get(key, 1.0)
        alloc[key] = max(0, int(round(base * weight)))
    return alloc


def _get_exposure_budget(role_profile: Optional[dict], role_name: str) -> dict[str, int]:
    """Return exposure budget for the role, with fallback to defaults."""
    if role_profile and "exposure_budget" in role_profile:
        return role_profile["exposure_budget"]
    return DEFAULT_EXPOSURE_BUDGETS.get(role_name, DEFAULT_EXPOSURE_BUDGETS["*"])


def _calendar_stress_modifier(calendar_context: dict, week_type: str) -> float:
    """Adjust stress based on calendar events (match, travel, etc.)."""
    days_to_match = calendar_context.get("days_to_match")
    if calendar_context.get("in_season") and days_to_match is not None and days_to_match <= 7:
        return 0.8
    if calendar_context.get("phase") == "Off Season":
        return 1.1
    return 1.0


def _allocate_exposures(
    role_budget: dict[str, int],
    stress_level: str,
    stress_mod: float,
) -> dict[str, int]:
    """Scale exposures by stress level and modifier."""
    multiplier = 1.0
    if stress_level == "low":
        multiplier = 0.7
    elif stress_level == "high":
        multiplier = 1.2
    multiplier *= stress_mod

    result = {}
    for key, value in role_budget.items():
        result[key] = max(1, int(round(value * multiplier)))
    return result


def _generate_session_intents(
    week_type: str,
    frequency: int,
    athlete: AthleteProfile,
    role_profile: Optional[dict],
    calendar_context: dict,
    exposure_budget: dict[str, int],
    placements: list[SessionPlacement],
    progression_plan: object = None,
) -> list[SessionIntent]:
    """Generate a SessionIntent for each session using calendar-designed placements."""
    intents = []
    for placement in placements:
        purpose, qualities, fatigue_cost, movement_priorities = _derive_session_attributes(
            week_type, placement.intent_type, role_profile, placement.session_number, frequency
        )

        progression_tier = _resolve_progression_tier(progression_plan)
        movement_slots = _build_intent_movement_slots(
            week_type=week_type,
            placement=placement.intent_type,
            purpose=purpose,
            athlete=athlete,
            role_name=(role_profile or {}).get("role", athlete.role or ""),
            sport=athlete.sport,
            progression_tier=progression_tier,
        )

        intent = SessionIntent(
            id=f"S{placement.session_number}",
            purpose=purpose,
            qualities=qualities,
            fatigue_cost=fatigue_cost,
            movement_priorities=movement_priorities,
            exposure_targets=placement.exposure_allocation,
            placement=placement.intent_type,
            week_type=week_type,
            session_number=placement.session_number,
            day_of_week=placement.day_of_week,
            progression=progression_plan,
            movement_slots=movement_slots,
        )
        intents.append(intent)
    return intents


def _derive_session_attributes(
    week_type: str,
    intent_type: str,
    role_profile: Optional[dict],
    session_num: int,
    frequency: int,
) -> tuple[str, list[str], str, list[str]]:
    """Determine purpose, qualities, fatigue, movement priorities for a session based on intent type."""

    INTENT_ATTRS = {
        "Strength": ("Strength", ["force", "eccentric"], "high", ["squat", "hinge", "push", "pull"]),
        "Power": ("Power/Speed", ["velocity", "power"], "moderate", ["hinge", "squat", "push", "pull"]),
        "Speed": ("Speed", ["velocity", "sprint"], "moderate", ["sprint", "plyo"]),
        "Primer": ("Primer", ["speed", "activation"], "low", ["sprint", "plyo", "core"]),
        "Recovery": ("Recovery", ["recovery", "mobility"], "low", ["core", "mobility"]),
        "Conditioning": ("Conditioning", ["endurance"], "high", ["conditioning", "core"]),
    }

    purpose, qualities, fatigue, movement_priorities = INTENT_ATTRS.get(intent_type, INTENT_ATTRS["Strength"])
    movement_priorities = list(movement_priorities)

    # Week-type modulation
    if week_type == "accumulation" and intent_type == "Strength":
        purpose = "General Strength"
        qualities = ["force"]
        fatigue = "moderate"
    elif week_type == "intensification" and intent_type == "Strength":
        purpose = "Max Strength"
        qualities = ["force", "velocity"]
        fatigue = "high"
    elif week_type == "realization" and intent_type in ("Power", "Speed"):
        purpose = "Power/Speed"
        qualities = ["velocity", "power"]
        fatigue = "moderate"
    elif week_type == "taper":
        if intent_type != "Recovery" and intent_type != "Primer":
            purpose = "Maintenance"
            qualities = ["force", "recovery"]
            fatigue = "low"

    # Role-specific additions
    role_name = (role_profile or {}).get("role", "")
    if role_name:
        if "Fast" in role_name:
            movement_priorities.append("sprint")
            if intent_type != "Primer":
                qualities.append("eccentric")
        if "Batter" in role_name:
            movement_priorities.append("rotational")
        if "Spin" in role_name:
            movement_priorities.append("rotational")
        if "Wicketkeeper" in role_name:
            movement_priorities.append("isometric")
            movement_priorities.append("balance")
        if "All" in role_name:
            movement_priorities.append("sprint")
            movement_priorities.append("rotational")

    return purpose, qualities, fatigue, movement_priorities


def _build_weekly_rationale(
    week_type: str,
    role_profile: Optional[dict],
    calendar_context: dict,
    placements: list[SessionPlacement],
) -> list[str]:
    """Build human-readable rationale for this week's strategy."""
    rationale = []
    rationale.append(f"Week type: {week_type.capitalize()}")
    if role_profile:
        rationale.append(f"Role emphasis: {role_profile.get('role', '')}")

    # Summarise the calendar-backed placement
    if placements:
        intent_summary = ", ".join(
            f"{p.day_of_week[:3]}-{p.intent_type}" for p in placements
        )
        rationale.append(f"Placement: {intent_summary}")

    days_to_match = calendar_context.get("days_to_match")
    if days_to_match is not None and days_to_match <= 7:
        match_day_name = DAY_NAMES[calendar_context.get("match_day", 5)]
        rationale.append(
            f"Match on {match_day_name} — sessions designed backwards from match"
        )
    return rationale


def _resolve_progression_tier(progression_plan: object | None) -> int:
    """Map a WeeklyProgressionPlan onto a 1–5 MovementSlot tier."""
    if progression_plan is None:
        return 2
    complexity = getattr(progression_plan, "complexity_level", 2) or 2
    return max(1, min(5, int(complexity)))


def _build_intent_movement_slots(
    week_type: str,
    placement: str,
    purpose: str,
    athlete: AthleteProfile,
    role_name: str,
    sport: str,
    progression_tier: int,
) -> list[MovementSlot]:
    """Build the MovementSlot list for a session.

    The selection is driven by:
      - role-based slot template from get_slot_template() (coaching layer)
      - week_type modulates intent (accumulation→strength, realization→power)
      - placement (calendar-derived intent) overrides purpose for short-cycle states
    """
    intent_label = purpose or placement or "Strength"
    # In taper/test weeks, downgrade intent even if purpose says otherwise
    if week_type in ("taper", "test") and placement not in ("Recovery", "Primer"):
        intent_label = "Maintenance"

    return get_slot_template(
        role=role_name,
        session_intent=intent_label,
        progression_tier=progression_tier,
        sport=sport,
    )
