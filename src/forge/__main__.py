"""FORGE demo: python -m forge — generates programs for 3 levels × 3 equipment profiles."""
from src.forge.models import (
    AthleteProfile, AthleteLevel, EquipmentProfile, SeasonPhase,
)
from src.forge.main import generate_program
from src.forge.renderer import render_program


def demo():
    levels = [AthleteLevel.BEGINNER, AthleteLevel.INTERMEDIATE, AthleteLevel.ADVANCED]
    equipments = [
        EquipmentProfile.FIELD_ONLY,
        EquipmentProfile.BASIC_GYM,
        EquipmentProfile.COMMERCIAL_GYM,
    ]

    for level in levels:
        for equip in equipments:
            athlete = AthleteProfile(
                sport="rugby",
                training_age_years={"Beginner": 0.5, "Intermediate": 2.5, "Advanced": 5}[level.value],
                season_phase=SeasonPhase.OFF_SEASON,
                goal="strength",
                equipment_profile=equip,
                athlete_level=level,
                technique_consistency={"Beginner": 0.85, "Intermediate": 0.9, "Advanced": 0.95}[level.value],
                injury_status="none",
                injury_history=[],
                fatigue_level="normal",
                weeks_since_break=0,
            )
            if level == AthleteLevel.ADVANCED:
                athlete.strength_base_met = True

            program = generate_program(athlete)
            print(render_program(program))
            print(f"\n{'=' * 60}")
            print(f"CREDIBILITY: {program.credibility_score}")
            print(f"SESSIONS: {len(program.sessions)}")
            print(f"{'=' * 60}\n")


if __name__ == "__main__":
    demo()
