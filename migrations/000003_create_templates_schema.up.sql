-- Forge Exercise Intelligence Database - Migration 000003 (Up)
-- Description: Create movement templates, template slots, slot requirements, slot progressions, and exercise fallbacks.

-- -------------------------------------------------------------
-- Core Templates and Slots Tables
-- -------------------------------------------------------------

-- 1. MOVEMENT TEMPLATES
CREATE TABLE movement_templates (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    sport_id BIGINT REFERENCES sports(id) ON DELETE SET NULL,
    athlete_role VARCHAR(100) DEFAULT 'All',
    training_goal VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Trigger for movement_templates updated_at
CREATE TRIGGER trigger_update_movement_templates_timestamp
    BEFORE UPDATE ON movement_templates
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 2. TEMPLATE SLOTS
CREATE TABLE template_slots (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    template_id BIGINT NOT NULL REFERENCES movement_templates(id) ON DELETE CASCADE,
    slot_type VARCHAR(50) NOT NULL CHECK (
        slot_type IN ('Primary', 'Secondary', 'Accessory', 'Core')
    ),
    name VARCHAR(100) NOT NULL,
    display_order INT NOT NULL,
    notes TEXT,
    UNIQUE (template_id, display_order)
);

-- -------------------------------------------------------------
-- Slot Requirements, Progressions, and Fallbacks
-- -------------------------------------------------------------

-- 3. SLOT REQUIREMENTS (Dynamic constraints for selecting exercises)
-- Note: Multiple rows for a single slot represent OR relations (alternative options).
-- Columns within a single row represent AND relations (combined constraints).
CREATE TABLE slot_requirements (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    slot_id BIGINT NOT NULL REFERENCES template_slots(id) ON DELETE CASCADE,
    movement_pattern_id BIGINT REFERENCES movement_patterns(id) ON DELETE SET NULL,
    physical_quality_id BIGINT REFERENCES physical_qualities(id) ON DELETE SET NULL,
    training_method_id BIGINT REFERENCES training_methods(id) ON DELETE SET NULL,
    equipment_id BIGINT REFERENCES equipment(id) ON DELETE SET NULL,
    difficulty_level VARCHAR(50) CHECK (
        difficulty_level IN ('Beginner', 'Intermediate', 'Advanced', 'Elite')
    ),
    min_relevance_score INT CHECK (min_relevance_score BETWEEN 1 AND 10),
    min_specificity_rating INT CHECK (min_specificity_rating BETWEEN 1 AND 10),
    is_mandatory BOOLEAN NOT NULL DEFAULT TRUE
);

-- 4. SLOT PROGRESSIONS (Strength & Conditioning programming rules)
CREATE TABLE slot_progressions (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    slot_id BIGINT NOT NULL REFERENCES template_slots(id) ON DELETE CASCADE,
    progression_type VARCHAR(50) NOT NULL CHECK (
        progression_type IN ('Linear Load', 'Double Progression', 'Velocity-Based', 'RPE-Based', 'Undulating', 'Qualitative/Technique')
    ),
    intensity_target VARCHAR(100) NOT NULL, -- e.g., "75-80% 1RM", "RPE 8", "0.75-0.85 m/s"
    volume_target VARCHAR(100) NOT NULL,    -- e.g., "3x5", "4x4", "3x8-10"
    progression_rule TEXT NOT NULL,
    deload_protocol TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Trigger for slot_progressions updated_at
CREATE TRIGGER trigger_update_slot_progressions_timestamp
    BEFORE UPDATE ON slot_progressions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 5. SLOT EXERCISE FALLBACKS (Explicit mapping for manual/static substitutions)
CREATE TABLE slot_exercise_fallbacks (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    slot_id BIGINT NOT NULL REFERENCES template_slots(id) ON DELETE CASCADE,
    preferred_exercise_id BIGINT NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    fallback_exercise_id BIGINT NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    preference_rank INT NOT NULL CHECK (preference_rank > 0),
    CONSTRAINT chk_different_exercises CHECK (preferred_exercise_id <> fallback_exercise_id),
    UNIQUE (slot_id, preferred_exercise_id, fallback_exercise_id),
    UNIQUE (slot_id, preferred_exercise_id, preference_rank)
);

-- -------------------------------------------------------------
-- Index Recommendations for Templates
-- -------------------------------------------------------------

-- Index template_slots by template_id to pull a complete template configuration instantly
CREATE INDEX idx_template_slots_template ON template_slots(template_id, display_order);

-- Index requirements by slot_id for database compiler resolution during exercise matching
CREATE INDEX idx_slot_requirements_slot ON slot_requirements(slot_id);

-- Index progressions by slot_id
CREATE INDEX idx_slot_progressions_slot ON slot_progressions(slot_id);

-- Index fallbacks by slot and preferred exercise for quick fallback resolution
CREATE INDEX idx_slot_fallbacks_lookup ON slot_exercise_fallbacks(slot_id, preferred_exercise_id, preference_rank);
