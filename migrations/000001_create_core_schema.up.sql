-- Forge Exercise Intelligence Database - Migration 000001 (Up)
-- Description: Create core schema, lookup tables, junction tables, indexes, and utility functions.

-- Enable extensions if needed
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- -------------------------------------------------------------
-- Reusable Utility Functions & Triggers
-- -------------------------------------------------------------

-- Trigger function to automatically update updated_at timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- -------------------------------------------------------------
-- Core Lookup Tables
-- -------------------------------------------------------------

-- 1. EQUIPMENT
CREATE TABLE equipment (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL CHECK (
        category IN ('Free Weights', 'Machines', 'Cables', 'Bands/Chains', 'Bodyweight', 'Cardio', 'Specialty/Accessory', 'Other')
    ),
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Trigger for equipment updated_at
CREATE TRIGGER trigger_update_equipment_timestamp
    BEFORE UPDATE ON equipment
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 2. MOVEMENT PATTERNS
CREATE TABLE movement_patterns (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Trigger for movement_patterns updated_at
CREATE TRIGGER trigger_update_movement_patterns_timestamp
    BEFORE UPDATE ON movement_patterns
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 3. PHYSICAL QUALITIES
CREATE TABLE physical_qualities (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Trigger for physical_qualities updated_at
CREATE TRIGGER trigger_update_physical_qualities_timestamp
    BEFORE UPDATE ON physical_qualities
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 4. TRAINING METHODS
CREATE TABLE training_methods (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Trigger for training_methods updated_at
CREATE TRIGGER trigger_update_training_methods_timestamp
    BEFORE UPDATE ON training_methods
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 5. SPORTS
CREATE TABLE sports (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL CHECK (
        category IN ('Team Sports', 'Individual Sports', 'Combat Sports', 'Endurance Sports', 'Strength Sports', 'Other')
    ),
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Trigger for sports updated_at
CREATE TRIGGER trigger_update_sports_timestamp
    BEFORE UPDATE ON sports
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 6. TAGS
CREATE TABLE tags (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- -------------------------------------------------------------
-- Exercises Core Table
-- -------------------------------------------------------------

CREATE TABLE exercises (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    difficulty_level VARCHAR(50) NOT NULL CHECK (
        difficulty_level IN ('Beginner', 'Intermediate', 'Advanced', 'Elite')
    ),
    mechanics_type VARCHAR(50) NOT NULL CHECK (
        mechanics_type IN ('Compound', 'Isolation', 'Static', 'N/A')
    ),
    force_type VARCHAR(50) NOT NULL CHECK (
        force_type IN ('Push', 'Pull', 'Hinge', 'Carry', 'Static', 'N/A')
    ),
    -- tsvector for highly optimized Full-Text Search
    search_vector tsvector GENERATED ALWAYS AS (
        to_tsvector('english', name || ' ' || COALESCE(description, ''))
    ) STORED,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Trigger for exercises updated_at
CREATE TRIGGER trigger_update_exercises_timestamp
    BEFORE UPDATE ON exercises
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- -------------------------------------------------------------
-- Junction Tables (Many-to-Many Mappings)
-- -------------------------------------------------------------

-- 1. EXERCISE <-> EQUIPMENT
CREATE TABLE exercise_equipment (
    exercise_id BIGINT NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    equipment_id BIGINT NOT NULL REFERENCES equipment(id) ON DELETE CASCADE,
    is_required BOOLEAN NOT NULL DEFAULT TRUE,
    PRIMARY KEY (exercise_id, equipment_id)
);

-- 2. EXERCISE <-> MOVEMENT PATTERNS
CREATE TABLE exercise_movement_patterns (
    exercise_id BIGINT NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    movement_pattern_id BIGINT NOT NULL REFERENCES movement_patterns(id) ON DELETE CASCADE,
    pattern_priority VARCHAR(20) NOT NULL DEFAULT 'Primary' CHECK (
        pattern_priority IN ('Primary', 'Secondary', 'Tertiary')
    ),
    PRIMARY KEY (exercise_id, movement_pattern_id)
);

-- 3. EXERCISE <-> PHYSICAL QUALITIES
CREATE TABLE exercise_physical_qualities (
    exercise_id BIGINT NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    physical_quality_id BIGINT NOT NULL REFERENCES physical_qualities(id) ON DELETE CASCADE,
    relevance_score INT NOT NULL DEFAULT 5 CHECK (relevance_score BETWEEN 1 AND 10),
    PRIMARY KEY (exercise_id, physical_quality_id)
);

-- 4. EXERCISE <-> TRAINING METHODS
CREATE TABLE exercise_training_methods (
    exercise_id BIGINT NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    training_method_id BIGINT NOT NULL REFERENCES training_methods(id) ON DELETE CASCADE,
    PRIMARY KEY (exercise_id, training_method_id)
);

-- 5. EXERCISE <-> SPORTS
CREATE TABLE exercise_sport_mapping (
    exercise_id BIGINT NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    sport_id BIGINT NOT NULL REFERENCES sports(id) ON DELETE CASCADE,
    specificity_rating INT NOT NULL DEFAULT 5 CHECK (specificity_rating BETWEEN 1 AND 10),
    transfer_index NUMERIC(3,2) NOT NULL DEFAULT 0.50 CHECK (transfer_index BETWEEN 0.00 AND 1.00),
    PRIMARY KEY (exercise_id, sport_id)
);

-- 6. EXERCISE <-> TAGS
CREATE TABLE exercise_tags (
    exercise_id BIGINT NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    tag_id BIGINT NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (exercise_id, tag_id)
);

-- -------------------------------------------------------------
-- Index Recommendations for 10,000+ Exercises
-- -------------------------------------------------------------

-- Full-Text Search GIN Index on Exercises
CREATE INDEX idx_exercises_search ON exercises USING GIN(search_vector);

-- Trigram index for partial/fuzzy matching (e.g. searching "sqat" for "Squat")
CREATE INDEX idx_exercises_name_trgm ON exercises USING GIN(name gin_trgm_ops);

-- Reverse indices on many-to-many junction tables to optimize reverse lookups
-- (e.g. "Find all exercises targeting Max Strength" or "Find all exercises for Football")
CREATE INDEX idx_exercise_equipment_rev ON exercise_equipment(equipment_id, exercise_id);
CREATE INDEX idx_exercise_movement_rev ON exercise_movement_patterns(movement_pattern_id, exercise_id);
CREATE INDEX idx_exercise_phys_qual_rev ON exercise_physical_qualities(physical_quality_id, exercise_id);
CREATE INDEX idx_exercise_train_meth_rev ON exercise_training_methods(training_method_id, exercise_id);
CREATE INDEX idx_exercise_sport_rev ON exercise_sport_mapping(sport_id, exercise_id);
CREATE INDEX idx_exercise_tags_rev ON exercise_tags(tag_id, exercise_id);

-- Composite sorting indexes for performance on sport specificity and physical quality scoring
CREATE INDEX idx_exercise_sport_spec ON exercise_sport_mapping(sport_id, specificity_rating DESC, transfer_index DESC);
CREATE INDEX idx_exercise_phys_qual_rel ON exercise_physical_qualities(physical_quality_id, relevance_score DESC);
