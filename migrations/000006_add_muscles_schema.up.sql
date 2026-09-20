-- Forge Exercise Intelligence Database - Migration 000006 (Up)
-- Description: Create muscles lookup and exercise_muscles junction table.

-- -------------------------------------------------------------
-- Muscles Table
-- -------------------------------------------------------------
CREATE TABLE muscles (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL CHECK (
        category IN ('Lower Body', 'Upper Body - Push', 'Upper Body - Pull', 'Core', 'Other')
    ),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Trigger for muscles updated_at
CREATE TRIGGER trigger_update_muscles_timestamp
    BEFORE UPDATE ON muscles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- -------------------------------------------------------------
-- Exercise <-> Muscles Junction Table (Many-to-Many with Role)
-- -------------------------------------------------------------
CREATE TABLE exercise_muscles (
    exercise_id BIGINT NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    muscle_id BIGINT NOT NULL REFERENCES muscles(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (
        role IN ('Primary', 'Secondary')
    ),
    PRIMARY KEY (exercise_id, muscle_id, role)
);

-- -------------------------------------------------------------
-- Indexes
-- -------------------------------------------------------------

-- Reverse index to answer: "Find all exercises that target Quadriceps as a Primary muscle"
CREATE INDEX idx_exercise_muscles_rev ON exercise_muscles(muscle_id, exercise_id, role);

-- Index for resolving an exercise's muscular profile quickly
CREATE INDEX idx_exercise_muscles_lookup ON exercise_muscles(exercise_id, role);
