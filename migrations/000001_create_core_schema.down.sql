-- Forge Exercise Intelligence Database - Migration 000001 (Down)
-- Description: Drop all tables, indexes, triggers, and functions created in up migration.

-- Drop Junction Tables (dependent tables first)
DROP TABLE IF EXISTS exercise_tags CASCADE;
DROP TABLE IF EXISTS exercise_sport_mapping CASCADE;
DROP TABLE IF EXISTS exercise_training_methods CASCADE;
DROP TABLE IF EXISTS exercise_physical_qualities CASCADE;
DROP TABLE IF EXISTS exercise_movement_patterns CASCADE;
DROP TABLE IF EXISTS exercise_equipment CASCADE;

-- Drop Core Tables
DROP TABLE IF EXISTS exercises CASCADE;
DROP TABLE IF EXISTS tags CASCADE;
DROP TABLE IF EXISTS sports CASCADE;
DROP TABLE IF EXISTS training_methods CASCADE;
DROP TABLE IF EXISTS physical_qualities CASCADE;
DROP TABLE IF EXISTS movement_patterns CASCADE;
DROP TABLE IF EXISTS equipment CASCADE;

-- Drop Trigger Functions
DROP FUNCTION IF EXISTS update_updated_at_column CASCADE;

-- Drop Extensions (Optional: normally kept, but clean for reset)
-- DROP EXTENSION IF EXISTS "pg_trgm";
-- DROP EXTENSION IF EXISTS "uuid-ossp";
