-- Forge Exercise Intelligence Database - Migration 000023 (Up)
-- Description: Recommendation Observability Layer — Phase 2
--
-- Creates 3 tables for recommendation tracking and analysis:
--   1. recommendation_log    — full snapshot of every V2 recommendation
--   2. coach_feedback        — coach decisions, overrides, rationale
--   3. entity_relationships  — generic source→target relationship table

BEGIN;

-- ================================================================
-- TABLE 1: recommendation_log
-- Stores every V2 demand recommendation with full assessment snapshot,
-- demand scores, candidate rankings, and request parameters.
-- Primarily append-only for observability, drift analysis, and AI training data.
-- ================================================================

CREATE TABLE IF NOT EXISTS recommendation_log (
    id              SERIAL PRIMARY KEY,
    recommendation_id UUID NOT NULL DEFAULT gen_random_uuid(),

    -- Context
    athlete_id      INT REFERENCES athletes(id) ON DELETE SET NULL,
    role_id         INT NOT NULL,
    sport           VARCHAR(100) NOT NULL,
    role_name       VARCHAR(100) NOT NULL,
    development_level VARCHAR(20) NOT NULL DEFAULT 'FOUNDATION',

    -- Full snapshot
    request_params     JSONB NOT NULL DEFAULT '{}'::jsonb,
    assessment_snapshot JSONB NOT NULL DEFAULT '{}'::jsonb,
    demand_scores      JSONB NOT NULL DEFAULT '[]'::jsonb,
    candidate_rankings JSONB NOT NULL DEFAULT '[]'::jsonb,

    -- Metadata
    engine_version  VARCHAR(20) NOT NULL DEFAULT '2.0.0',
    execution_time_ms INT,
    cached           BOOLEAN NOT NULL DEFAULT FALSE,

    created_at      TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_recommendation_log_athlete
    ON recommendation_log(athlete_id);
CREATE INDEX IF NOT EXISTS idx_recommendation_log_role
    ON recommendation_log(role_id);
CREATE INDEX IF NOT EXISTS idx_recommendation_log_created
    ON recommendation_log(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_recommendation_log_recommendation_id
    ON recommendation_log(recommendation_id);

COMMENT ON TABLE recommendation_log IS
    'Append-only log of every V2 demand recommendation with full snapshot for observability and drift analysis.';
COMMENT ON COLUMN recommendation_log.recommendation_id IS
    'Public UUID exposed via API for coach feedback referencing and idempotent replay.';
COMMENT ON COLUMN recommendation_log.candidate_rankings IS
    'Full ranked list of scored exercises with recommendation_score, used for drift analysis and future AI training.';

-- ================================================================
-- TABLE 2: coach_feedback
-- Captures coach decisions, overrides, and rationale against stored
-- recommendations for quality tracking and continuous improvement.
-- ================================================================

CREATE TABLE IF NOT EXISTS coach_feedback (
    id                  SERIAL PRIMARY KEY,
    recommendation_id   UUID NOT NULL REFERENCES recommendation_log(recommendation_id) ON DELETE CASCADE,
    coach_id            INT,
    coach_name          VARCHAR(200),

    -- Decision
    coach_decision      VARCHAR(20) NOT NULL DEFAULT 'approved'
                        CHECK (coach_decision IN ('approved', 'modified', 'rejected', 'overridden')),
    acceptance_status   VARCHAR(25) NOT NULL DEFAULT 'accepted'
                        CHECK (acceptance_status IN ('accepted', 'partially_accepted', 'rejected')),

    -- Override details (what was changed)
    override_details    JSONB,
    rationale           TEXT,
    notes               TEXT,

    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_coach_feedback_recommendation
    ON coach_feedback(recommendation_id);
CREATE INDEX IF NOT EXISTS idx_coach_feedback_decision
    ON coach_feedback(coach_decision);
CREATE INDEX IF NOT EXISTS idx_coach_feedback_coach
    ON coach_feedback(coach_id);

COMMENT ON TABLE coach_feedback IS
    'Coach decisions against stored recommendations for quality tracking and improvement.';

-- Trigger to auto-update updated_at
CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_coach_feedback_timestamp
    BEFORE UPDATE ON coach_feedback
    FOR EACH ROW
    EXECUTE FUNCTION trigger_set_timestamp();

-- ================================================================
-- TABLE 3: entity_relationships
-- Generic lightweight relationship table replacing full entity graph.
-- Supports any source→target pairing with typed relationship labels.
-- ================================================================

CREATE TABLE IF NOT EXISTS entity_relationships (
    id                  SERIAL PRIMARY KEY,
    source_type         VARCHAR(50) NOT NULL,
    source_id           INT NOT NULL,
    relationship_type   VARCHAR(100) NOT NULL,
    target_type         VARCHAR(50) NOT NULL,
    target_id           INT NOT NULL,
    weight              NUMERIC(5, 2) DEFAULT 1.00 CHECK (weight >= 0 AND weight <= 100),
    metadata            JSONB DEFAULT '{}'::jsonb,

    created_at          TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),

    -- Prevent duplicate relationships
    UNIQUE (source_type, source_id, relationship_type, target_type, target_id)
);

CREATE INDEX IF NOT EXISTS idx_entity_relationships_source
    ON entity_relationships(source_type, source_id);
CREATE INDEX IF NOT EXISTS idx_entity_relationships_target
    ON entity_relationships(target_type, target_id);
CREATE INDEX IF NOT EXISTS idx_entity_relationships_type
    ON entity_relationships(relationship_type);

COMMENT ON TABLE entity_relationships IS
    'Generic lightweight relationship table: source_type → relationship_type → target_type with weight.';

COMMIT;
