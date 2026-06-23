-- Migration 000018: Replace training_age_months with athlete development levels
-- Moves from time-based to competency-based gating model.
--
-- Creates:
--   athlete_development_level enum (FOUNDATION, DEVELOPMENT, PERFORMANCE)
--   exercises.minimum_level column (backfilled from minimum_training_age_months)
--   athletes.development_level column (backfilled from training_age_months)
--   slot_requirements.minimum_level column (backfilled from difficulty_level)
--
-- Backward compatible: existing columns remain and continue to be populated.

BEGIN;

-- ============================================================
-- Step 1: Create the development level enum
-- ============================================================
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'athlete_development_level') THEN
        CREATE TYPE athlete_development_level AS ENUM ('FOUNDATION', 'DEVELOPMENT', 'PERFORMANCE');
    END IF;
END
$$;

-- ============================================================
-- Step 2: Add minimum_level to exercises
-- ============================================================
ALTER TABLE exercises
    ADD COLUMN IF NOT EXISTS minimum_level athlete_development_level;

-- Backfill: map minimum_training_age_months -> development level
--   0-5 months  -> FOUNDATION  (entry-level, no prerequisites)
--   6-23 months -> DEVELOPMENT (has basic training foundation)
--   24+ months  -> PERFORMANCE (established training history)
UPDATE exercises
    SET minimum_level = CASE
        WHEN minimum_training_age_months >= 24 THEN 'PERFORMANCE'::athlete_development_level
        WHEN minimum_training_age_months >= 6  THEN 'DEVELOPMENT'::athlete_development_level
        ELSE 'FOUNDATION'::athlete_development_level
    END
    WHERE minimum_level IS NULL;

-- All existing exercises must have a minimum_level now
ALTER TABLE exercises
    ALTER COLUMN minimum_level SET NOT NULL;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'exercises_minimum_level_check') THEN
        ALTER TABLE exercises ADD CONSTRAINT exercises_minimum_level_check CHECK (minimum_level IS NOT NULL);
    END IF;
END
$$;

-- ============================================================
-- Step 3: Add development_level to athletes
-- ============================================================
ALTER TABLE athletes
    ADD COLUMN IF NOT EXISTS development_level athlete_development_level;

-- Backfill: map training_age_months -> development level
--   0-11 months  -> FOUNDATION  (novice)
--   12-35 months -> DEVELOPMENT (intermediate)
--   36+ months   -> PERFORMANCE (experienced)
UPDATE athletes
    SET development_level = CASE
        WHEN training_age_months >= 36 THEN 'PERFORMANCE'::athlete_development_level
        WHEN training_age_months >= 12 THEN 'DEVELOPMENT'::athlete_development_level
        ELSE 'FOUNDATION'::athlete_development_level
    END
    WHERE development_level IS NULL;

ALTER TABLE athletes
    ALTER COLUMN development_level SET NOT NULL;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'athletes_development_level_check') THEN
        ALTER TABLE athletes ADD CONSTRAINT athletes_development_level_check CHECK (development_level IS NOT NULL);
    END IF;
END
$$;

-- ============================================================
-- Step 4: Add minimum_level to slot_requirements
-- ============================================================
ALTER TABLE slot_requirements
    ADD COLUMN IF NOT EXISTS minimum_level athlete_development_level;

-- Backfill: map difficulty_level -> minimum development level
--   Beginner -> FOUNDATION
--   Intermediate -> DEVELOPMENT
--   Advanced/Elite -> PERFORMANCE
UPDATE slot_requirements
    SET minimum_level = CASE
        WHEN difficulty_level IN ('Advanced', 'Elite') THEN 'PERFORMANCE'::athlete_development_level
        WHEN difficulty_level = 'Intermediate'         THEN 'DEVELOPMENT'::athlete_development_level
        WHEN difficulty_level = 'Beginner'             THEN 'FOUNDATION'::athlete_development_level
        ELSE 'FOUNDATION'::athlete_development_level
    END
    WHERE minimum_level IS NULL AND difficulty_level IS NOT NULL;

-- ============================================================
-- Step 5: Create helper function for level ordering comparison
-- ============================================================
CREATE OR REPLACE FUNCTION development_level_ordinal(level athlete_development_level)
RETURNS integer AS $$
BEGIN
    RETURN CASE level
        WHEN 'FOUNDATION'   THEN 1
        WHEN 'DEVELOPMENT'  THEN 2
        WHEN 'PERFORMANCE'  THEN 3
    END;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

COMMIT;
