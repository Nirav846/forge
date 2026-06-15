-- Forge Exercise Intelligence Database - Migration 000002 (Down)
-- Description: Cleanly truncate all tables to remove seed data and reset auto-incrementing identity sequences.

-- Truncating child tables is not strictly necessary if CASCADE is used on parent tables, 
-- but explicitly listing them ensures cleanliness and clarity.
TRUNCATE TABLE 
    exercise_tags,
    exercise_sport_mapping,
    exercise_training_methods,
    exercise_physical_qualities,
    exercise_movement_patterns,
    exercise_equipment,
    exercises,
    tags,
    sports,
    training_methods,
    physical_qualities,
    movement_patterns,
    equipment
RESTART IDENTITY CASCADE;
