-- Forge Exercise Intelligence Database - Migration 000004 (Down)
-- Description: Cleanly truncate templates seed data and reset identity sequences.

TRUNCATE TABLE 
    slot_exercise_fallbacks,
    slot_progressions,
    slot_requirements,
    template_slots,
    movement_templates
RESTART IDENTITY CASCADE;
