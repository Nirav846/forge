-- Forge Exercise Intelligence Database - Migration 000012 (Up)
-- Description: Create programs, program_weeks, program_sessions, and program_session_exercises tables.

-- 1. PROGRAMS TABLE
CREATE TABLE programs (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    athlete_id BIGINT NOT NULL REFERENCES athletes(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    goal VARCHAR(100) NOT NULL,
    sessions_per_week INT NOT NULL CHECK (sessions_per_week BETWEEN 2 AND 4),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Trigger for programs updated_at
CREATE TRIGGER trigger_update_programs_timestamp
    BEFORE UPDATE ON programs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 2. PROGRAM WEEKS TABLE
CREATE TABLE program_weeks (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    program_id BIGINT NOT NULL REFERENCES programs(id) ON DELETE CASCADE,
    week_number INT NOT NULL CHECK (week_number BETWEEN 1 AND 4),
    focus VARCHAR(100) NOT NULL, -- e.g., 'Base', 'Accumulation', 'Peak', 'Deload'
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_program_week UNIQUE (program_id, week_number)
);

-- 3. PROGRAM SESSIONS TABLE
CREATE TABLE program_sessions (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    week_id BIGINT NOT NULL REFERENCES program_weeks(id) ON DELETE CASCADE,
    session_number INT NOT NULL CHECK (session_number BETWEEN 1 AND 4),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_week_session UNIQUE (week_id, session_number)
);

-- 4. PROGRAM SESSION EXERCISES TABLE
CREATE TABLE program_session_exercises (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    session_id BIGINT NOT NULL REFERENCES program_sessions(id) ON DELETE CASCADE,
    exercise_id BIGINT NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    display_order INT NOT NULL CHECK (display_order >= 1),
    sets INT NOT NULL CHECK (sets > 0),
    reps INT NOT NULL CHECK (reps > 0),
    intensity VARCHAR(100) NOT NULL, -- e.g., '75% 1RM (RPE 7)'
    rest_seconds INT NOT NULL CHECK (rest_seconds >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_session_exercise_order UNIQUE (session_id, display_order)
);

-- Indexes for efficient lookups and cascade deletes
CREATE INDEX idx_programs_athlete ON programs(athlete_id);
CREATE INDEX idx_program_weeks_program ON program_weeks(program_id);
CREATE INDEX idx_program_sessions_week ON program_sessions(week_id);
CREATE INDEX idx_program_session_exercises_session ON program_session_exercises(session_id);
