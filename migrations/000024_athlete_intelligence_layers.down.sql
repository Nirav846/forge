-- Forge Exercise Intelligence Database - Migration 000024 (Down)
-- Description: Rollback Athlete State, Training Load, and Injury Risk Layers
--
-- Fully reverses migration 000024:
--   Drops 3 new tables + 1 view
--   Restores domain_events aggregate_type CHECK to original values
--   Existing V2 ontology and recommendation tables are unaffected.

BEGIN;

-- Drop view first
DROP VIEW IF EXISTS acute_chronic_load_view CASCADE;

-- Drop tables in dependency order
DROP TABLE IF EXISTS injury_risk_profiles CASCADE;
DROP TABLE IF EXISTS training_load_events CASCADE;
DROP TABLE IF EXISTS athlete_state_snapshots CASCADE;

-- Restore domain_events CHECK to original values
ALTER TABLE domain_events
    DROP CONSTRAINT IF EXISTS domain_events_aggregate_type_check;

ALTER TABLE domain_events
    ADD CONSTRAINT domain_events_aggregate_type_check
    CHECK (aggregate_type IN (
        'athlete', 'assessment', 'program', 'session',
        'injury', 'exercise', 'template', 'organization'
    ));

COMMIT;
