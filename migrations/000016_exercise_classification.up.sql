-- Forge Exercise Intelligence Database - Migration 000016 (Up)
-- Description: Add exercise_class, primary_adaptation, force_vector columns to exercises
-- and create exercise_equivalencies table for substitution engine.

BEGIN;

-- -------------------------------------------------------------
-- 1. Add Classification Columns
-- -------------------------------------------------------------
ALTER TABLE exercises
ADD COLUMN exercise_class VARCHAR(50) CHECK (exercise_class IN (
    'Olympic Lift',
    'Ballistic',
    'Plyometric',
    'Medicine Ball',
    'Max Strength',
    'Isometric',
    'Core Stability',
    'Sprint Drill',
    'Accessory'
));

ALTER TABLE exercises
ADD COLUMN primary_adaptation VARCHAR(50) CHECK (primary_adaptation IN (
    'Power',
    'Strength',
    'Rotational Power',
    'Acceleration',
    'Speed',
    'Stability',
    'Hypertrophy',
    'Eccentric Control'
));

ALTER TABLE exercises
ADD COLUMN force_vector VARCHAR(30) CHECK (force_vector IN (
    'Vertical',
    'Horizontal',
    'Rotational',
    'Lateral',
    'Multi-Directional',
    'Axial',
    'N/A'
));

-- -------------------------------------------------------------
-- 2. Create Exercise Equivalencies Table
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS exercise_equivalencies (
    id BIGSERIAL PRIMARY KEY,
    source_exercise_id BIGINT NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    target_exercise_id BIGINT NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    equivalency_score DECIMAL(3,1) NOT NULL CHECK (equivalency_score >= 0 AND equivalency_score <= 10),
    reason TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_exercise_id, target_exercise_id)
);

CREATE INDEX idx_equivalencies_source ON exercise_equivalencies(source_exercise_id);
CREATE INDEX idx_equivalencies_target ON exercise_equivalencies(target_exercise_id);

-- -------------------------------------------------------------
-- 3. Create Coach Override Table
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS program_coach_overrides (
    id BIGSERIAL PRIMARY KEY,
    session_exercise_id BIGINT NOT NULL REFERENCES program_session_exercises(id) ON DELETE CASCADE,
    original_exercise_id BIGINT NOT NULL REFERENCES exercises(id),
    selected_exercise_id BIGINT NOT NULL REFERENCES exercises(id),
    override_reason TEXT,
    overridden_by VARCHAR(100),
    override_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_overrides_session_exercise ON program_coach_overrides(session_exercise_id);

COMMIT;
