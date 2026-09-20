-- Forge Exercise Intelligence Database - Migration 000003 (Down)
-- Description: Drop all tables and indexes created in migration 000003.

-- Drop Dependent/Junction Tables First
DROP TABLE IF EXISTS slot_exercise_fallbacks CASCADE;
DROP TABLE IF EXISTS slot_progressions CASCADE;
DROP TABLE IF EXISTS slot_requirements CASCADE;
DROP TABLE IF EXISTS template_slots CASCADE;

-- Drop Core Tables
DROP TABLE IF EXISTS movement_templates CASCADE;
