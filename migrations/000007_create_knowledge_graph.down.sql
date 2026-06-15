-- Forge Exercise Intelligence Database - Migration 000007 (Down)
-- Description: Drop all tables, triggers, and indices created in migration 000007.

-- Drop Junction/Dependent Tables First
DROP TABLE IF EXISTS deficit_movement_templates CASCADE;
DROP TABLE IF EXISTS deficit_training_methods CASCADE;
DROP TABLE IF EXISTS deficits CASCADE;
DROP TABLE IF EXISTS benchmarks CASCADE;
DROP TABLE IF EXISTS driver_assessments CASCADE;
DROP TABLE IF EXISTS assessments CASCADE;
DROP TABLE IF EXISTS performance_drivers CASCADE;
DROP TABLE IF EXISTS roles CASCADE;
