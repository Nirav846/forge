-- Forge Exercise Intelligence Database - Migration 000011 (Up)
-- Description: Create assessment_results table, constraints, and indexes.

CREATE TABLE assessment_results (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    athlete_id BIGINT NOT NULL REFERENCES athletes(id) ON DELETE CASCADE,
    assessment_id BIGINT NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    score NUMERIC(10,2) NOT NULL CHECK (score > 0.00),
    unit VARCHAR(20) NOT NULL,
    test_date DATE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Indexing for rapid athlete progression search and historical charts
CREATE INDEX idx_assessment_results_athlete_lookup ON assessment_results(athlete_id, assessment_id, test_date DESC);
