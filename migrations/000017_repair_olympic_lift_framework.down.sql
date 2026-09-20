-- Forge Exercise Intelligence Database - Migration 000017 (Down) - Repair
-- Description: Reverse schema changes from 000017 repair.
-- Data (exercises, tags, sport mappings) is additive and preserved.

-- 1d. Remove 'Rotation' from force_type check constraint
UPDATE exercises SET force_type = 'N/A' WHERE force_type = 'Rotation';

ALTER TABLE exercises DROP CONSTRAINT IF EXISTS exercises_force_type_check;
ALTER TABLE exercises ADD CONSTRAINT exercises_force_type_check
    CHECK (force_type IN ('Push', 'Pull', 'Hinge', 'Carry', 'Static', 'N/A'));

-- 1a. Remove default_exercise_id from template_slots
ALTER TABLE template_slots DROP COLUMN IF EXISTS default_exercise_id;

-- 1b. Remove columns from exercises
ALTER TABLE exercises DROP COLUMN IF EXISTS technical_difficulty;
ALTER TABLE exercises DROP COLUMN IF EXISTS minimum_training_age_months;

-- 1c. Remove training_age_months from athletes
ALTER TABLE athletes DROP COLUMN IF EXISTS training_age_months;
