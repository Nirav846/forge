-- Migration 000019: Revert to backfilled minimum_level values
-- Restores the 000018 backfill values (all FOUNDATION for exercises with
-- minimum_training_age_months = 0).

BEGIN;

UPDATE exercises SET minimum_level = 'FOUNDATION'::athlete_development_level WHERE name = 'Clean Pull';
UPDATE exercises SET minimum_level = 'FOUNDATION'::athlete_development_level WHERE name = 'Mid-Thigh Pull';
UPDATE exercises SET minimum_level = 'FOUNDATION'::athlete_development_level WHERE name = 'High Pull';
UPDATE exercises SET minimum_level = 'FOUNDATION'::athlete_development_level WHERE name = 'Snatch Pull';
UPDATE exercises SET minimum_level = 'FOUNDATION'::athlete_development_level WHERE name = 'Hang Clean';
UPDATE exercises SET minimum_level = 'FOUNDATION'::athlete_development_level WHERE name = 'Squat Clean';
UPDATE exercises SET minimum_level = 'FOUNDATION'::athlete_development_level WHERE name = 'Clean and Jerk';
UPDATE exercises SET minimum_level = 'FOUNDATION'::athlete_development_level WHERE name = 'Power Snatch';
UPDATE exercises SET minimum_level = 'FOUNDATION'::athlete_development_level WHERE name = 'Hang Snatch';
UPDATE exercises SET minimum_level = 'FOUNDATION'::athlete_development_level WHERE name = 'Snatch Balance';
UPDATE exercises SET minimum_level = 'FOUNDATION'::athlete_development_level WHERE name = 'Overhead Squat';
UPDATE exercises SET minimum_level = 'FOUNDATION'::athlete_development_level WHERE name = 'Push Press';
UPDATE exercises SET minimum_level = 'FOUNDATION'::athlete_development_level WHERE name = 'Push Jerk';
UPDATE exercises SET minimum_level = 'FOUNDATION'::athlete_development_level WHERE name = 'Split Jerk';

COMMIT;
