-- Migration 000018: Rollback development levels
-- Reverses: ADD COLUMN minimum_level (exercises), development_level (athletes),
--           slot_requirements.minimum_level, helper function, enum type

BEGIN;

ALTER TABLE slot_requirements DROP COLUMN IF EXISTS minimum_level;
ALTER TABLE athletes         DROP COLUMN IF EXISTS development_level;
ALTER TABLE exercises        DROP COLUMN IF EXISTS minimum_level;

DROP FUNCTION IF EXISTS development_level_ordinal(athlete_development_level);

DROP TYPE IF EXISTS athlete_development_level;

COMMIT;
