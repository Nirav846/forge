from src.forge.main import generate_program
from src.forge.models import AthleteProfile, AthleteLevel, EquipmentProfile, SeasonPhase
from src.forge.renderer import render_coach_program, render_block_summary

athlete = AthleteProfile(
    sport="rugby",
    position_role="prop",
    goal="strength",
    training_age_years=3.0,
    athlete_level=AthleteLevel.INTERMEDIATE,
    equipment_profile=EquipmentProfile.COMMERCIAL_GYM,
    season_phase=SeasonPhase.OFF_SEASON,
    available_minutes=75,
    days_to_match=5,
)

program = generate_program(athlete)

print("=" * 100)
print("COACH PROGRAM")
print("=" * 100)
print(render_coach_program(program))

print("\n" + "=" * 100)
print("BLOCK SUMMARY")
print("=" * 100)
print(render_block_summary(program))
