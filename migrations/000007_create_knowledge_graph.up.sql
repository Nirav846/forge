-- Forge Exercise Intelligence Database - Migration 000007 (Up)
-- Description: Create Forge Knowledge Graph V1 tables, constraints, and indexes.

-- -------------------------------------------------------------
-- 1. Athlete Roles
-- -------------------------------------------------------------
CREATE TABLE roles (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    sport_id BIGINT NOT NULL REFERENCES sports(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (sport_id, name)
);

-- Trigger for roles updated_at
CREATE TRIGGER trigger_update_roles_timestamp
    BEFORE UPDATE ON roles
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- -------------------------------------------------------------
-- 2. Performance Drivers (Anatomical/Physical Demands)
-- -------------------------------------------------------------
CREATE TABLE performance_drivers (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    role_id BIGINT NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    priority VARCHAR(20) NOT NULL CHECK (
        priority IN ('Primary', 'Secondary', 'Tertiary')
    ),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Trigger for performance_drivers updated_at
CREATE TRIGGER trigger_update_performance_drivers_timestamp
    BEFORE UPDATE ON performance_drivers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- -------------------------------------------------------------
-- 3. Assessments (Physical Testing Protocols)
-- -------------------------------------------------------------
CREATE TABLE assessments (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    metric_unit VARCHAR(20) NOT NULL, -- e.g. 'N', 'm/s', 'cm', 'kg'
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Trigger for assessments updated_at
CREATE TRIGGER trigger_update_assessments_timestamp
    BEFORE UPDATE ON assessments
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- -------------------------------------------------------------
-- 4. Driver <-> Assessment Junction Table (Many-to-Many)
-- -------------------------------------------------------------
CREATE TABLE driver_assessments (
    performance_driver_id BIGINT NOT NULL REFERENCES performance_drivers(id) ON DELETE CASCADE,
    assessment_id BIGINT NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    PRIMARY KEY (performance_driver_id, assessment_id)
);

-- -------------------------------------------------------------
-- 5. Benchmarks (Target Thresholds for Assessments)
-- -------------------------------------------------------------
CREATE TABLE benchmarks (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    assessment_id BIGINT NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    min_value NUMERIC(10,2), -- NULL represents negative infinity
    max_value NUMERIC(10,2), -- NULL represents positive infinity
    classification VARCHAR(50) NOT NULL CHECK (
        classification IN ('Poor', 'Sub-optimal', 'Optimal', 'Elite')
    ),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (assessment_id, name)
);

-- Trigger for benchmarks updated_at
CREATE TRIGGER trigger_update_benchmarks_timestamp
    BEFORE UPDATE ON benchmarks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- -------------------------------------------------------------
-- 6. Deficits (Physical/Biomechanical Weaknesses)
-- -------------------------------------------------------------
CREATE TABLE deficits (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    assessment_id BIGINT NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Trigger for deficits updated_at
CREATE TRIGGER trigger_update_deficits_timestamp
    BEFORE UPDATE ON deficits
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- -------------------------------------------------------------
-- 7. Deficit <-> Training Method Junction Table (Many-to-Many)
-- -------------------------------------------------------------
CREATE TABLE deficit_training_methods (
    deficit_id BIGINT NOT NULL REFERENCES deficits(id) ON DELETE CASCADE,
    training_method_id BIGINT NOT NULL REFERENCES training_methods(id) ON DELETE CASCADE,
    PRIMARY KEY (deficit_id, training_method_id)
);

-- -------------------------------------------------------------
-- 8. Deficit <-> Movement Template Junction Table (Many-to-Many)
-- -------------------------------------------------------------
CREATE TABLE deficit_movement_templates (
    deficit_id BIGINT NOT NULL REFERENCES deficits(id) ON DELETE CASCADE,
    movement_template_id BIGINT NOT NULL REFERENCES movement_templates(id) ON DELETE CASCADE,
    PRIMARY KEY (deficit_id, movement_template_id)
);

-- -------------------------------------------------------------
-- Indexes for Knowledge Graph V1
-- -------------------------------------------------------------
CREATE INDEX idx_roles_sport ON roles(sport_id);
CREATE INDEX idx_performance_drivers_role ON performance_drivers(role_id);
CREATE INDEX idx_driver_assessments_rev ON driver_assessments(assessment_id, performance_driver_id);
CREATE INDEX idx_benchmarks_assessment ON benchmarks(assessment_id, classification);
CREATE INDEX idx_deficits_assessment ON deficits(assessment_id);
CREATE INDEX idx_deficit_methods_rev ON deficit_training_methods(training_method_id, deficit_id);
CREATE INDEX idx_deficit_templates_rev ON deficit_movement_templates(movement_template_id, deficit_id);
