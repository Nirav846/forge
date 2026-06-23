-- Forge Exercise Intelligence Database - Migration 000022 (Down)
-- Description: Rollback V2 Ontology Foundation
--
-- Fully reverses migration 000022:
--   Drops all new tables, removes added columns, cleans up seed data.
--   Existing V1 tables (movement_templates, template_slots, etc.) are
--   completely unaffected.

BEGIN;

-- ================================================================
-- SECTION E: DOMAIN EVENTS
-- ================================================================
DROP TABLE IF EXISTS domain_events CASCADE;

-- ================================================================
-- SECTION D: EXECUTION TRACKING
-- ================================================================
ALTER TABLE program_session_exercises
    DROP COLUMN IF EXISTS metadata_json;

ALTER TABLE program_session_exercises
    DROP COLUMN IF EXISTS completion_notes;

ALTER TABLE program_session_exercises
    DROP COLUMN IF EXISTS completed;

ALTER TABLE program_session_exercises
    DROP COLUMN IF EXISTS actual_rpe;

ALTER TABLE program_session_exercises
    DROP COLUMN IF EXISTS actual_intensity;

ALTER TABLE program_session_exercises
    DROP COLUMN IF EXISTS actual_reps;

ALTER TABLE program_session_exercises
    DROP COLUMN IF EXISTS actual_sets;

-- ================================================================
-- SECTION C: ASSESSMENT FOUNDATION
-- ================================================================
DROP TABLE IF EXISTS metric_demand_mapping CASCADE;
DROP TABLE IF EXISTS assessment_metrics CASCADE;

-- ================================================================
-- SECTION A: PERFORMANCE DEMAND LAYER
-- ================================================================
DROP TABLE IF EXISTS injury_risk_demand_mapping CASCADE;
DROP TABLE IF EXISTS assessment_demand_mapping CASCADE;
DROP TABLE IF EXISTS role_demand_priority CASCADE;
DROP TABLE IF EXISTS exercise_demand_mapping CASCADE;

-- Drop trigger on performance_demands before dropping table
DROP TRIGGER IF EXISTS trigger_update_performance_demands_timestamp
    ON performance_demands;

DROP TABLE IF EXISTS performance_demands CASCADE;

-- ================================================================
-- SECTION B: ONTOLOGY RECONSTRUCTION
-- ================================================================

-- Remove columns from physical_qualities
ALTER TABLE physical_qualities
    DROP COLUMN IF EXISTS metadata_json;

ALTER TABLE physical_qualities
    DROP COLUMN IF EXISTS deprecated_replacement_id;

ALTER TABLE physical_qualities
    DROP COLUMN IF EXISTS is_active;

ALTER TABLE physical_qualities
    DROP COLUMN IF EXISTS display_order;

ALTER TABLE physical_qualities
    DROP COLUMN IF EXISTS parent_quality_id;

ALTER TABLE physical_qualities
    DROP COLUMN IF EXISTS category_id;

-- Remove columns from movement_patterns
ALTER TABLE movement_patterns
    DROP COLUMN IF EXISTS metadata_json;

ALTER TABLE movement_patterns
    DROP COLUMN IF EXISTS deprecated_replacement_id;

ALTER TABLE movement_patterns
    DROP COLUMN IF EXISTS is_active;

ALTER TABLE movement_patterns
    DROP COLUMN IF EXISTS display_order;

ALTER TABLE movement_patterns
    DROP COLUMN IF EXISTS parent_pattern_id;

ALTER TABLE movement_patterns
    DROP COLUMN IF EXISTS family_id;

-- Drop the new lookup tables
DROP TABLE IF EXISTS quality_categories CASCADE;
DROP TABLE IF EXISTS movement_pattern_families CASCADE;

COMMIT;
