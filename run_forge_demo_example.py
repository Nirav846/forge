from src.forge.main import generate_program
from src.forge.models import AthleteProfile
from src.forge.renderer import render_coach_program

athlete = AthleteProfile(
    sport="rugby",
    position_role="prop",
    goal="strength",
    training_age=3.0,
    athlete_level="intermediate",
    available_equipment=["barbell", "dumbbell", "bench", "bands"],
    available_minutes=75,
    frequency=3,
    days_to_match=5,
)

program = generate_program(athlete)

print(render_coach_program(program))