-- Forge Exercise Intelligence Database - Migration 000010 (Up)
-- Description: Create athletes table, constraints, triggers, and indexes.

CREATE TABLE athletes (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(20) NOT NULL CHECK (
        gender IN ('Male', 'Female', 'Other', 'Prefer Not to Say')
    ),
    sport_id BIGINT REFERENCES sports(id) ON DELETE CASCADE,
    role_id BIGINT REFERENCES roles(id) ON DELETE CASCADE,
    dominant_side VARCHAR(20) NOT NULL CHECK (
        dominant_side IN ('Left', 'Right', 'Ambidextrous')
    ),
    competition_level VARCHAR(50) NOT NULL CHECK (
        competition_level IN ('Beginner', 'Intermediate', 'Advanced', 'Elite')
    ),
    training_age_years INT NOT NULL CHECK (
        training_age_years >= 0
    ),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Trigger for athletes updated_at
CREATE TRIGGER trigger_update_athletes_timestamp
    BEFORE UPDATE ON athletes
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Indexes for Athletes Module
CREATE INDEX idx_athletes_sport ON athletes(sport_id);
CREATE INDEX idx_athletes_role ON athletes(role_id);
