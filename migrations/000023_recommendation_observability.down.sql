-- Forge Exercise Intelligence Database - Migration 000023 (Down)
-- Description: Rollback Recommendation Observability Layer
--
-- Fully reverses migration 000023:
--   Drops all 3 new tables and related objects.
--   Existing V2 ontology tables are completely unaffected.

BEGIN;

-- Drop triggers first
DROP TRIGGER IF EXISTS trigger_update_coach_feedback_timestamp ON coach_feedback;

-- Drop trigger function (only if no other triggers depend on it)
DROP FUNCTION IF EXISTS trigger_set_timestamp;

-- Drop tables in dependency order
DROP TABLE IF EXISTS entity_relationships CASCADE;
DROP TABLE IF EXISTS coach_feedback CASCADE;
DROP TABLE IF EXISTS recommendation_log CASCADE;

COMMIT;
