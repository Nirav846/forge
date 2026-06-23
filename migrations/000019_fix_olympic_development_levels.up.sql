-- Migration 000019: Fix Olympic lift minimum_level values
-- Migration 000018 backfilled minimum_level from minimum_training_age_months,
-- but Olympic lifts (IDs 18-31) had minimum_training_age_months=0 (they were
-- added by 000017 which didn't set training age), so they were mapped to
-- FOUNDATION. This migration corrects them.
--
-- Classification rule:
--   Derivatives without catch phase (pulls, presses) -> DEVELOPMENT
--   Derivatives with catch phase (full lifts) -> PERFORMANCE
--   High-impact/complex variants -> PERFORMANCE

BEGIN;

UPDATE exercises SET minimum_level = 'DEVELOPMENT'::athlete_development_level WHERE name = 'Clean Pull';
UPDATE exercises SET minimum_level = 'DEVELOPMENT'::athlete_development_level WHERE name = 'Mid-Thigh Pull';
UPDATE exercises SET minimum_level = 'DEVELOPMENT'::athlete_development_level WHERE name = 'High Pull';
UPDATE exercises SET minimum_level = 'DEVELOPMENT'::athlete_development_level WHERE name = 'Snatch Pull';
UPDATE exercises SET minimum_level = 'PERFORMANCE'::athlete_development_level WHERE name = 'Hang Clean';
UPDATE exercises SET minimum_level = 'PERFORMANCE'::athlete_development_level WHERE name = 'Squat Clean';
UPDATE exercises SET minimum_level = 'PERFORMANCE'::athlete_development_level WHERE name = 'Clean and Jerk';
UPDATE exercises SET minimum_level = 'PERFORMANCE'::athlete_development_level WHERE name = 'Power Snatch';
UPDATE exercises SET minimum_level = 'PERFORMANCE'::athlete_development_level WHERE name = 'Hang Snatch';
UPDATE exercises SET minimum_level = 'PERFORMANCE'::athlete_development_level WHERE name = 'Snatch Balance';
UPDATE exercises SET minimum_level = 'DEVELOPMENT'::athlete_development_level WHERE name = 'Overhead Squat';
UPDATE exercises SET minimum_level = 'DEVELOPMENT'::athlete_development_level WHERE name = 'Push Press';
UPDATE exercises SET minimum_level = 'DEVELOPMENT'::athlete_development_level WHERE name = 'Push Jerk';
UPDATE exercises SET minimum_level = 'PERFORMANCE'::athlete_development_level WHERE name = 'Split Jerk';

COMMIT;
