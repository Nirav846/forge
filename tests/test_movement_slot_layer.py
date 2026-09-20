"""Movement Slot Layer — self-check.

Verifies the four architectural invariants introduced by the MovementSlot layer:
  1. get_slot_template returns MovementSlot lists with sensible tier/intent per role
  2. planning_engine populates intent.movement_slots per session
  3. The selector accepts a MovementSlot and respects progression_tier ± 1
  4. Different roles produce different slot templates (e.g. Batter has rotation)
"""
from __future__ import annotations
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.forge.models import (
    AthleteProfile, AthleteLevel, EquipmentProfile, SeasonPhase,
    FamilyCode, MovementSlot,
)
from src.forge.role_profiles import get_slot_template
from src.forge.planning_engine import (
    plan_weekly_strategy, _resolve_progression_tier,
)
from src.forge.role_week_planning import get_role_week_profile
from src.forge.exercise_selector import select_exercise


def _athlete(role: str = "Batter", sport: str = "Cricket") -> AthleteProfile:
    return AthleteProfile(
        sport=sport,
        training_age_years=0.5,
        season_phase=SeasonPhase.OFF_SEASON,
        goal="strength",
        equipment_profile=EquipmentProfile.COMMERCIAL_GYM,
        athlete_level=AthleteLevel.BEGINNER,
        technique_consistency=0.85,
        role=role,
        position_role=role,
        match_day=5,
        team_training_days=[0, 2, 4],
        program_length_weeks=8,
        frequency_per_week=3,
    )


def test_slot_template_basics():
    slots = get_slot_template(role="Batter", session_intent="Strength", progression_tier=2)
    assert isinstance(slots, list) and slots, "slot template must be non-empty"
    for s in slots:
        assert isinstance(s, MovementSlot), f"each item must be MovementSlot, got {type(s)}"
        assert 1 <= s.progression_tier <= 5, f"tier out of range: {s.progression_tier}"
        assert 1 <= s.priority <= 4, f"priority out of range: {s.priority}"
    families = {s.family for s in slots}
    assert FamilyCode.ROT in families, "Batter Strength session must include rotation"
    print(f"  PASS test_slot_template_basics ({len(slots)} slots: {sorted(f.value for f in families)})")


def test_slot_template_per_role_differs():
    batter = {s.family for s in get_slot_template("Batter", "Strength", 2)}
    fast_bowler = {s.family for s in get_slot_template("Fast Bowler", "Strength", 2)}
    wk = {s.family for s in get_slot_template("Wicketkeeper", "Strength", 2)}
    assert FamilyCode.ROT in batter, "Batter should have ROT slot"
    assert FamilyCode.ROT not in fast_bowler or FamilyCode.SLHD in fast_bowler, \
        "Fast Bowler should NOT centre on rotation; should have eccentric/hinge"
    assert FamilyCode.SLKD in wk, "Wicketkeeper should have unilateral squat slot"
    # Each role carries different family mix
    assert batter != fast_bowler, "Batter and Fast Bowler templates must differ"
    print("  PASS test_slot_template_per_role_differs")


def test_intent_intensity_modulation():
    strength = get_slot_template("Batter", "Strength", 2)
    primer = get_slot_template("Batter", "Primer", 2)
    speed = get_slot_template("Batter", "Speed", 2)
    # Primer/Recovery: short list with mostly core/mobility
    assert len(primer) <= 3, f"Primer session should be compact, got {len(primer)}"
    # Speed: emphasises plyo
    speed_fams = {s.family for s in speed}
    assert FamilyCode.PLYO in speed_fams or any("plyo" in s.movement_pattern for s in speed), \
        f"Speed session missing plyo: {speed_fams}"
    print(f"  PASS test_intent_intensity_modulation "
          f"(strength={len(strength)}, primer={len(primer)}, speed={len(speed)})")


def test_tier_progression_clamped():
    assert _resolve_progression_tier(None) == 2
    # Boundaries
    assert 1 <= _resolve_progression_tier(type("X", (), {"complexity_level": 0})()) <= 5
    assert _resolve_progression_tier(type("X", (), {"complexity_level": 10})()) == 5
    print("  PASS test_tier_progression_clamped")


def test_planning_engine_populates_movement_slots():
    athlete = _athlete(role="Batter")
    role_profile_data = {"role": "Batter"}
    role_week = get_role_week_profile(athlete.sport, athlete.position_role)
    strategy = plan_weekly_strategy(
        week_number=1,
        week_type="accumulation",
        athlete=athlete,
        role_profile=role_profile_data,
        role_week_profile=role_week,
        calendar_context={
            "match_day": 5,
            "travel_days": [],
            "team_training_days": [0, 2, 4],
            "phase": "off_season",
        },
    )
    assert strategy.session_intents, "weekly strategy must have session intents"
    for intent in strategy.session_intents:
        assert intent.movement_slots, f"session {intent.id} missing movement_slots"
        for ms in intent.movement_slots:
            assert isinstance(ms, MovementSlot)
    print(f"  PASS test_planning_engine_populates_movement_slots "
          f"({len(strategy.session_intents)} sessions, "
          f"first slot tier={strategy.session_intents[0].movement_slots[0].progression_tier})")


def test_selector_accepts_movement_slot():
    athlete = _athlete(role="Batter")
    slot = MovementSlot(
        family=FamilyCode.DLKD,
        movement_pattern="squat",
        intent="strength",
        progression_tier=2,
        priority=1,
        substitutions=["Back Squat"],
    )
    ex = select_exercise(
        slot=slot,
        athlete_level=AthleteLevel.INTERMEDIATE,
        equipment_profile=EquipmentProfile.COMMERCIAL_GYM,
        recent_exercises={},
        injury_history=[],
        athlete_profile=athlete,
    )
    assert ex is not None, "selector must return an exercise for a valid slot"
    assert ex.family == FamilyCode.DLKD, f"selected family mismatch: {ex.family}"
    # Tier ± 1 around 2 => exercises with difficulty in {1,2,3}
    assert 1 <= ex.difficulty <= 3, f"difficulty out of tier window: {ex.difficulty}"
    print(f"  PASS test_selector_accepts_movement_slot -> {ex.name} (difficulty={ex.difficulty})")


def test_legacy_call_shape_still_works():
    """The FamilyCode-first positional shape must still return an exercise."""
    athlete = _athlete(role="Batter")
    ex = select_exercise(
        FamilyCode.DLHD,
        AthleteLevel.INTERMEDIATE,
        EquipmentProfile.COMMERCIAL_GYM,
        {},
        [],
        athlete_profile=athlete,
    )
    assert ex is not None, "legacy FamilyCode call shape broke"
    assert ex.family == FamilyCode.DLHD
    print(f"  PASS test_legacy_call_shape_still_works -> {ex.name}")


if __name__ == "__main__":
    print("Movement Slot Layer self-check:")
    test_slot_template_basics()
    test_slot_template_per_role_differs()
    test_intent_intensity_modulation()
    test_tier_progression_clamped()
    test_planning_engine_populates_movement_slots()
    test_selector_accepts_movement_slot()
    test_legacy_call_shape_still_works()
    print("\nALL PASS")
