-- Forge Exercise Intelligence Database - Migration 000022 (Up)
-- Description: V2 Ontology Foundation — Performance Demand Architecture
--
-- Establishes the Performance Demand Architecture without breaking backward
-- compatibility. All existing tables, templates, and application code remain
-- fully functional. The V2 ontology runs alongside V1.
--
-- Sections:
--   A. Performance Demand Layer (performance_demands, exercise_demand_mapping,
--      role_demand_priority, assessment_demand_mapping, injury_risk_demand_mapping)
--   B. Ontology Reconstruction (movement_pattern_families, quality_categories,
--      extends movement_patterns + physical_qualities)
--   C. Assessment Foundation (assessment_metrics, metric_demand_mapping)
--   D. Execution Tracking (program_session_exercises execution columns)
--   E. Domain Events (domain_events)
--   F. Seed Data (families, categories, 18 demands, role mappings)

BEGIN;

-- ================================================================
-- SECTION A: PERFORMANCE DEMAND LAYER
-- ================================================================

-- ----------------------------------------------------------------
-- A1. performance_demands — Central ontology pivot
--      Each demand = 1 PRIMARY quality × 1 PRIMARY movement pattern.
--      demand_type allows non-biomotor demands (Sensory-Motor, Metabolic,
--      Cognitive) without schema changes.
-- ----------------------------------------------------------------
CREATE TABLE IF NOT EXISTS performance_demands (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    demand_type VARCHAR(50) NOT NULL DEFAULT 'Biomotor'
        CHECK (demand_type IN ('Biomotor', 'Sensory-Motor', 'Metabolic', 'Cognitive')),
    primary_quality_id BIGINT REFERENCES physical_qualities(id) ON DELETE SET NULL,
    primary_pattern_id BIGINT REFERENCES movement_patterns(id) ON DELETE SET NULL,
    display_order INT NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    metadata_json JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER trigger_update_performance_demands_timestamp
    BEFORE UPDATE ON performance_demands
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ----------------------------------------------------------------
-- A2. exercise_demand_mapping — M:N between exercises and demands.
--      Will eventually replace exercise_physical_qualities as the
--      primary exercise-attribute junction.
-- ----------------------------------------------------------------
CREATE TABLE IF NOT EXISTS exercise_demand_mapping (
    exercise_id BIGINT NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    demand_id BIGINT NOT NULL REFERENCES performance_demands(id) ON DELETE CASCADE,
    relevance_score INT NOT NULL DEFAULT 5
        CHECK (relevance_score BETWEEN 1 AND 10),
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    metadata_json JSONB DEFAULT '{}'::jsonb,
    PRIMARY KEY (exercise_id, demand_id)
);

CREATE INDEX idx_exercise_demand_rev ON exercise_demand_mapping(demand_id, exercise_id);
CREATE INDEX idx_exercise_demand_score ON exercise_demand_mapping(demand_id, relevance_score DESC);

-- ----------------------------------------------------------------
-- A3. role_demand_priority — Replaces template-driven routing.
--      Maps roles → demands with priority scores for the constraint
--      solver and weighted scoring engine.
-- ----------------------------------------------------------------
CREATE TABLE IF NOT EXISTS role_demand_priority (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    role_id BIGINT NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    demand_id BIGINT NOT NULL REFERENCES performance_demands(id) ON DELETE CASCADE,
    priority INT NOT NULL CHECK (priority BETWEEN 1 AND 100),
    category VARCHAR(50) NOT NULL DEFAULT 'Secondary'
        CHECK (category IN ('Primary', 'Secondary', 'Tertiary')),
    metadata_json JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (role_id, demand_id)
);

CREATE INDEX idx_role_demand_role ON role_demand_priority(role_id, priority DESC);

-- ----------------------------------------------------------------
-- A4. assessment_demand_mapping — Links assessments to the demands
--      they measure. Each assessment can measure multiple demands
--      with varying weights (e.g., CMJ measures both Vertical Power
--      AND Reactive Strength).
-- ----------------------------------------------------------------
CREATE TABLE IF NOT EXISTS assessment_demand_mapping (
    assessment_id BIGINT NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    demand_id BIGINT NOT NULL REFERENCES performance_demands(id) ON DELETE CASCADE,
    weight DECIMAL(3,2) NOT NULL DEFAULT 1.00
        CHECK (weight BETWEEN 0.00 AND 1.00),
    PRIMARY KEY (assessment_id, demand_id)
);

CREATE INDEX idx_assessment_demand_rev ON assessment_demand_mapping(demand_id, assessment_id);

-- ----------------------------------------------------------------
-- A5. injury_risk_demand_mapping — Maps injury types to the
--      performance demands whose deficit increases injury risk.
--      Uses a VARCHAR injury_type reference (FK to future
--      injury_types table).
-- ----------------------------------------------------------------
CREATE TABLE IF NOT EXISTS injury_risk_demand_mapping (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    injury_type VARCHAR(100) NOT NULL,
    demand_id BIGINT NOT NULL REFERENCES performance_demands(id) ON DELETE CASCADE,
    relationship VARCHAR(50) NOT NULL DEFAULT 'protective'
        CHECK (relationship IN ('protective', 'risk_factor', 'bidirectional')),
    weight DECIMAL(3,2) NOT NULL DEFAULT 1.00
        CHECK (weight BETWEEN 0.00 AND 1.00),
    metadata_json JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (injury_type, demand_id)
);

CREATE INDEX idx_injury_risk_demand ON injury_risk_demand_mapping(demand_id);

-- ================================================================
-- SECTION B: ONTOLOGY RECONSTRUCTION
-- ================================================================

-- ----------------------------------------------------------------
-- B1. movement_pattern_families — Groups movement patterns into
--      biomechanically coherent families (e.g., Lower Body Bilateral,
--      Upper Body Push, Core & Trunk).
-- ----------------------------------------------------------------
CREATE TABLE IF NOT EXISTS movement_pattern_families (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    display_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------
-- B2. quality_categories — Categorises physical qualities into
--      higher-level groups (Force-Velocity, Metabolic, Morphological,
--      Joint-Structural).
-- ----------------------------------------------------------------
CREATE TABLE IF NOT EXISTS quality_categories (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    display_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------
-- B3. Extend movement_patterns with hierarchy and metadata.
--      All new columns are nullable — existing application code is
--      unaffected.
-- ----------------------------------------------------------------
ALTER TABLE movement_patterns
    ADD COLUMN IF NOT EXISTS family_id BIGINT
        REFERENCES movement_pattern_families(id) ON DELETE SET NULL;

ALTER TABLE movement_patterns
    ADD COLUMN IF NOT EXISTS parent_pattern_id BIGINT
        REFERENCES movement_patterns(id) ON DELETE SET NULL;

ALTER TABLE movement_patterns
    ADD COLUMN IF NOT EXISTS display_order INT NOT NULL DEFAULT 0;

ALTER TABLE movement_patterns
    ADD COLUMN IF NOT EXISTS is_active BOOLEAN NOT NULL DEFAULT TRUE;

ALTER TABLE movement_patterns
    ADD COLUMN IF NOT EXISTS deprecated_replacement_id BIGINT
        REFERENCES movement_patterns(id) ON DELETE SET NULL;

ALTER TABLE movement_patterns
    ADD COLUMN IF NOT EXISTS metadata_json JSONB DEFAULT '{}'::jsonb;

-- ----------------------------------------------------------------
-- B4. Extend physical_qualities with hierarchy and metadata.
-- ----------------------------------------------------------------
ALTER TABLE physical_qualities
    ADD COLUMN IF NOT EXISTS category_id BIGINT
        REFERENCES quality_categories(id) ON DELETE SET NULL;

ALTER TABLE physical_qualities
    ADD COLUMN IF NOT EXISTS parent_quality_id BIGINT
        REFERENCES physical_qualities(id) ON DELETE SET NULL;

ALTER TABLE physical_qualities
    ADD COLUMN IF NOT EXISTS display_order INT NOT NULL DEFAULT 0;

ALTER TABLE physical_qualities
    ADD COLUMN IF NOT EXISTS is_active BOOLEAN NOT NULL DEFAULT TRUE;

ALTER TABLE physical_qualities
    ADD COLUMN IF NOT EXISTS deprecated_replacement_id BIGINT
        REFERENCES physical_qualities(id) ON DELETE SET NULL;

ALTER TABLE physical_qualities
    ADD COLUMN IF NOT EXISTS metadata_json JSONB DEFAULT '{}'::jsonb;

-- ================================================================
-- SECTION C: ASSESSMENT FOUNDATION
-- ================================================================

-- ----------------------------------------------------------------
-- C1. assessment_metrics — Decomposes assessment protocols into
--      individual measurable outputs (e.g., CMJ produces height,
--      RSI, peak force/BW, impulse, GCT, ecc RFD, con RFD).
-- ----------------------------------------------------------------
CREATE TABLE IF NOT EXISTS assessment_metrics (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    assessment_id BIGINT NOT NULL REFERENCES assessments(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    unit VARCHAR(30) NOT NULL,
    higher_is_better BOOLEAN NOT NULL DEFAULT TRUE,
    display_order INT NOT NULL DEFAULT 0,
    metadata_json JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (assessment_id, name)
);

CREATE INDEX idx_assessment_metrics_assessment ON assessment_metrics(assessment_id);

-- ----------------------------------------------------------------
-- C2. metric_demand_mapping — Maps individual metrics to demands.
--      Allows precise deficit computation: "Athlete is weak on CMJ
--      RSI → Reactive Strength deficit."
-- ----------------------------------------------------------------
CREATE TABLE IF NOT EXISTS metric_demand_mapping (
    metric_id BIGINT NOT NULL REFERENCES assessment_metrics(id) ON DELETE CASCADE,
    demand_id BIGINT NOT NULL REFERENCES performance_demands(id) ON DELETE CASCADE,
    weight DECIMAL(3,2) NOT NULL DEFAULT 1.00
        CHECK (weight BETWEEN 0.00 AND 1.00),
    metadata_json JSONB DEFAULT '{}'::jsonb,
    PRIMARY KEY (metric_id, demand_id)
);

CREATE INDEX idx_metric_demand_rev ON metric_demand_mapping(demand_id, metric_id);

-- ================================================================
-- SECTION D: EXECUTION TRACKING
-- ================================================================

-- ----------------------------------------------------------------
-- D1. Execution columns on program_session_exercises.
--      Prescription columns (sets, reps, intensity, rest_seconds)
--      remain unchanged. Execution columns (actual_*) sit alongside
--      them, NULL until the session is completed.
--      This enables ACWR from ACTUAL load, not prescribed load.
-- ----------------------------------------------------------------
ALTER TABLE program_session_exercises
    ADD COLUMN IF NOT EXISTS actual_sets INT
        CHECK (actual_sets IS NULL OR actual_sets >= 0);

ALTER TABLE program_session_exercises
    ADD COLUMN IF NOT EXISTS actual_reps INT
        CHECK (actual_reps IS NULL OR actual_reps >= 0);

ALTER TABLE program_session_exercises
    ADD COLUMN IF NOT EXISTS actual_intensity VARCHAR(100);

ALTER TABLE program_session_exercises
    ADD COLUMN IF NOT EXISTS actual_rpe INT
        CHECK (actual_rpe IS NULL OR (actual_rpe BETWEEN 1 AND 10));

ALTER TABLE program_session_exercises
    ADD COLUMN IF NOT EXISTS completed BOOLEAN NOT NULL DEFAULT FALSE;

ALTER TABLE program_session_exercises
    ADD COLUMN IF NOT EXISTS completion_notes TEXT;

ALTER TABLE program_session_exercises
    ADD COLUMN IF NOT EXISTS metadata_json JSONB DEFAULT '{}'::jsonb;

-- ================================================================
-- SECTION E: DOMAIN EVENTS
-- ================================================================

-- ----------------------------------------------------------------
-- E1. domain_events — Immutable, append-only event log.
--      Every meaningful action writes one row: athlete.created,
--      assessment.completed, program.generated, session.completed.
--      Powers AI training, audit, analytics, and causal analysis.
--      NEVER UPDATE or DELETE rows in this table.
-- ----------------------------------------------------------------
CREATE TABLE IF NOT EXISTS domain_events (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    aggregate_type VARCHAR(50) NOT NULL
        CHECK (aggregate_type IN (
            'athlete', 'assessment', 'program', 'session',
            'injury', 'exercise', 'template', 'organization'
        )),
    aggregate_id BIGINT NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB NOT NULL DEFAULT '{}'::jsonb,
    occurred_at TIMESTAMPTZ NOT NULL,
    recorded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    organization_id BIGINT DEFAULT NULL
);

-- Critical indexes for event sourcing patterns
CREATE INDEX idx_domain_events_aggregate
    ON domain_events(aggregate_type, aggregate_id, occurred_at DESC);

CREATE INDEX idx_domain_events_type
    ON domain_events(event_type, occurred_at DESC);

CREATE INDEX idx_domain_events_org
    ON domain_events(organization_id, occurred_at DESC);

CREATE INDEX idx_domain_events_occurred
    ON domain_events(occurred_at DESC);

-- ================================================================
-- SECTION F: SEED DATA
-- ================================================================

-- ----------------------------------------------------------------
-- F1. Seed movement_pattern_families (6 families)
-- ----------------------------------------------------------------
INSERT INTO movement_pattern_families (name, description, display_order) VALUES
    ('Lower Body Bilateral',
     'Two-legged stance patterns: squatting, hip hinging, and vertical jumping.',
     1),
    ('Lower Body Unilateral',
     'Single-leg stance patterns: lunging, stepping, bounding.',
     2),
    ('Upper Body Push',
     'Pressing and extending movements away from the midline.',
     3),
    ('Upper Body Pull',
     'Pulling and retracting movements toward the midline.',
     4),
    ('Core & Trunk',
     'Rotational, anti-rotational, and load carriage patterns for trunk control.',
     5),
    ('Specialty',
     'Complex or sport-specific patterns requiring combined mobility and stability.',
     6)
ON CONFLICT (name) DO NOTHING;

-- ----------------------------------------------------------------
-- F2. Seed quality_categories (4 categories)
-- ----------------------------------------------------------------
INSERT INTO quality_categories (name, description, display_order) VALUES
    ('Force-Velocity',
     'Qualities related to force production magnitude and rate (Max Strength, RFD).',
     1),
    ('Metabolic',
     'Qualities related to energy system capacity and endurance (Aerobic, Anaerobic, LME).',
     2),
    ('Morphological',
     'Qualities related to tissue structure and composition (Hypertrophy).',
     3),
    ('Joint-Structural',
     'Qualities related to joint range of motion and control (Mobility, Stability).',
     4)
ON CONFLICT (name) DO NOTHING;

-- ----------------------------------------------------------------
-- F3. Set family_id on existing movement_patterns
-- ----------------------------------------------------------------
DO $$
DECLARE
    v_fam_lower_bilat BIGINT;
    v_fam_lower_uni   BIGINT;
    v_fam_upper_push  BIGINT;
    v_fam_upper_pull  BIGINT;
    v_fam_core        BIGINT;
    v_fam_specialty   BIGINT;
BEGIN
    SELECT id INTO v_fam_lower_bilat FROM movement_pattern_families WHERE name = 'Lower Body Bilateral';
    SELECT id INTO v_fam_lower_uni   FROM movement_pattern_families WHERE name = 'Lower Body Unilateral';
    SELECT id INTO v_fam_upper_push  FROM movement_pattern_families WHERE name = 'Upper Body Push';
    SELECT id INTO v_fam_upper_pull  FROM movement_pattern_families WHERE name = 'Upper Body Pull';
    SELECT id INTO v_fam_core        FROM movement_pattern_families WHERE name = 'Core & Trunk';
    SELECT id INTO v_fam_specialty   FROM movement_pattern_families WHERE name = 'Specialty';

    UPDATE movement_patterns SET family_id = v_fam_lower_bilat, display_order = 1 WHERE name = 'Squat' AND family_id IS NULL;
    UPDATE movement_patterns SET family_id = v_fam_lower_bilat, display_order = 2 WHERE name = 'Hinge' AND family_id IS NULL;
    UPDATE movement_patterns SET family_id = v_fam_lower_uni,   display_order = 1 WHERE name = 'Lunge (Single-Leg)' AND family_id IS NULL;
    UPDATE movement_patterns SET family_id = v_fam_upper_push,  display_order = 1 WHERE name = 'Push (Horizontal)' AND family_id IS NULL;
    UPDATE movement_patterns SET family_id = v_fam_upper_push,  display_order = 2 WHERE name = 'Push (Vertical)' AND family_id IS NULL;
    UPDATE movement_patterns SET family_id = v_fam_upper_pull,  display_order = 1 WHERE name = 'Pull (Horizontal)' AND family_id IS NULL;
    UPDATE movement_patterns SET family_id = v_fam_upper_pull,  display_order = 2 WHERE name = 'Pull (Vertical)' AND family_id IS NULL;
    UPDATE movement_patterns SET family_id = v_fam_core,        display_order = 1 WHERE name = 'Rotation' AND family_id IS NULL;
    UPDATE movement_patterns SET family_id = v_fam_core,        display_order = 2 WHERE name = 'Anti-Rotation' AND family_id IS NULL;
    UPDATE movement_patterns SET family_id = v_fam_core,        display_order = 3 WHERE name = 'Carry' AND family_id IS NULL;
    UPDATE movement_patterns SET family_id = v_fam_specialty,   display_order = 1 WHERE name = 'Overhead Squat' AND family_id IS NULL;
END $$;

-- ----------------------------------------------------------------
-- F4. Set category_id on existing physical_qualities
-- ----------------------------------------------------------------
DO $$
DECLARE
    v_cat_fv   BIGINT;
    v_cat_met  BIGINT;
    v_cat_morph BIGINT;
    v_cat_js   BIGINT;
BEGIN
    SELECT id INTO v_cat_fv   FROM quality_categories WHERE name = 'Force-Velocity';
    SELECT id INTO v_cat_met  FROM quality_categories WHERE name = 'Metabolic';
    SELECT id INTO v_cat_morph FROM quality_categories WHERE name = 'Morphological';
    SELECT id INTO v_cat_js   FROM quality_categories WHERE name = 'Joint-Structural';

    UPDATE physical_qualities SET category_id = v_cat_fv,   display_order = 1 WHERE name = 'Maximal Strength' AND category_id IS NULL;
    UPDATE physical_qualities SET category_id = v_cat_fv,   display_order = 2 WHERE name = 'Rate of Force Development' AND category_id IS NULL;
    UPDATE physical_qualities SET category_id = v_cat_met,  display_order = 1 WHERE name = 'Aerobic Capacity' AND category_id IS NULL;
    UPDATE physical_qualities SET category_id = v_cat_met,  display_order = 2 WHERE name = 'Anaerobic Power' AND category_id IS NULL;
    UPDATE physical_qualities SET category_id = v_cat_met,  display_order = 3 WHERE name = 'Local Muscular Endurance' AND category_id IS NULL;
    UPDATE physical_qualities SET category_id = v_cat_morph, display_order = 1 WHERE name = 'Hypertrophy' AND category_id IS NULL;
    UPDATE physical_qualities SET category_id = v_cat_js,   display_order = 1 WHERE name = 'Mobility' AND category_id IS NULL;
    UPDATE physical_qualities SET category_id = v_cat_js,   display_order = 2 WHERE name = 'Stability' AND category_id IS NULL;
END $$;

-- ----------------------------------------------------------------
-- F5. Seed 18 performance demands
--      Each demand = 1 PRIMARY quality × 1 PRIMARY movement pattern.
--      Names follow biomechanical function: [Action] × [Quality].
-- ----------------------------------------------------------------
DO $$
DECLARE
    v_mp_squat    BIGINT;
    v_mp_hinge    BIGINT;
    v_mp_push_h   BIGINT;
    v_mp_push_v   BIGINT;
    v_mp_pull_h   BIGINT;
    v_mp_pull_v   BIGINT;
    v_mp_lunge    BIGINT;
    v_mp_carry    BIGINT;
    v_mp_rotation BIGINT;
    v_mp_anti_rot BIGINT;
    v_pq_max_str  BIGINT;
    v_pq_rfd      BIGINT;
    v_pq_hyper    BIGINT;
    v_pq_anaer    BIGINT;
    v_pq_lme      BIGINT;
    v_pq_mob      BIGINT;
    v_pq_stab     BIGINT;
BEGIN
    -- Resolve movement pattern IDs
    SELECT id INTO v_mp_squat    FROM movement_patterns WHERE name = 'Squat';
    SELECT id INTO v_mp_hinge    FROM movement_patterns WHERE name = 'Hinge';
    SELECT id INTO v_mp_push_h   FROM movement_patterns WHERE name = 'Push (Horizontal)';
    SELECT id INTO v_mp_push_v   FROM movement_patterns WHERE name = 'Push (Vertical)';
    SELECT id INTO v_mp_pull_h   FROM movement_patterns WHERE name = 'Pull (Horizontal)';
    SELECT id INTO v_mp_pull_v   FROM movement_patterns WHERE name = 'Pull (Vertical)';
    SELECT id INTO v_mp_lunge    FROM movement_patterns WHERE name = 'Lunge (Single-Leg)';
    SELECT id INTO v_mp_carry    FROM movement_patterns WHERE name = 'Carry';
    SELECT id INTO v_mp_rotation FROM movement_patterns WHERE name = 'Rotation';
    SELECT id INTO v_mp_anti_rot FROM movement_patterns WHERE name = 'Anti-Rotation';

    -- Resolve physical quality IDs
    SELECT id INTO v_pq_max_str FROM physical_qualities WHERE name = 'Maximal Strength';
    SELECT id INTO v_pq_rfd     FROM physical_qualities WHERE name = 'Rate of Force Development';
    SELECT id INTO v_pq_hyper   FROM physical_qualities WHERE name = 'Hypertrophy';
    SELECT id INTO v_pq_anaer   FROM physical_qualities WHERE name = 'Anaerobic Power';
    SELECT id INTO v_pq_lme     FROM physical_qualities WHERE name = 'Local Muscular Endurance';
    SELECT id INTO v_pq_mob     FROM physical_qualities WHERE name = 'Mobility';
    SELECT id INTO v_pq_stab    FROM physical_qualities WHERE name = 'Stability';

    -- Insert 18 demands (Biomotor type)
    INSERT INTO performance_demands (name, description, demand_type, primary_quality_id, primary_pattern_id, display_order) VALUES
    -- 1-3: Power demands (RFD based)
    ('Vertical Power',
     'Explosive vertical force production through bilateral leg extension. Required for jumping, blocking, and rapid hip extension.',
     'Biomotor', v_pq_rfd, v_mp_squat, 1),
    ('Horizontal Drive Power',
     'Explosive horizontal force production through hip-driven extension. Required for sprint acceleration, starting mechanics, and hip drive.',
     'Biomotor', v_pq_rfd, v_mp_hinge, 2),
    ('Rotational Explosive Power',
     'Explosive transverse plane torque generation through hip-shoulder separation. Required for throwing, striking, and cutting.',
     'Biomotor', v_pq_rfd, v_mp_rotation, 3),

    -- 4-9: Strength demands (Max Strength based)
    ('Squat Strength',
     'Maximum bilateral lower body force production through knee-dominant flexion-extension. Foundation for all lower body power.',
     'Biomotor', v_pq_max_str, v_mp_squat, 4),
    ('Hinge Strength',
     'Maximum hip-dominant force production through posterior chain engagement. Foundation for sprint force, deadlift, and postural integrity.',
     'Biomotor', v_pq_max_str, v_mp_hinge, 5),
    ('Horizontal Push Strength',
     'Maximum pressing force in the horizontal plane through chest, shoulder, and triceps coordination.',
     'Biomotor', v_pq_max_str, v_mp_push_h, 6),
    ('Horizontal Pull Strength',
     'Maximum pulling force in the horizontal plane through back, rear shoulder, and biceps engagement.',
     'Biomotor', v_pq_max_str, v_mp_pull_h, 7),
    ('Vertical Push Strength',
     'Maximum overhead pressing force requiring shoulder stability, thoracic extension, and trunk rigidity.',
     'Biomotor', v_pq_max_str, v_mp_push_v, 8),
    ('Vertical Pull Strength',
     'Maximum pulling force in the vertical plane through latissimus dorsi, biceps, and scapular retraction.',
     'Biomotor', v_pq_max_str, v_mp_pull_v, 9),

    -- 10-12: Unilateral demands (Lunge based)
    ('Single-Leg Strength',
     'Maximum unilateral lower body force production through single-leg stance. Critical for sprint stance phase, cutting, and step-up power.',
     'Biomotor', v_pq_max_str, v_mp_lunge, 10),
    ('Single-Leg Stability',
     'Dynamic joint control and alignment maintenance during single-leg stance. Required for landing, cutting, and deceleration control.',
     'Biomotor', v_pq_stab, v_mp_lunge, 11),
    ('Single-Leg Power',
     'Explosive unilateral force production through single-leg extension. Required for bounding, hopping, and reactive stepping.',
     'Biomotor', v_pq_rfd, v_mp_lunge, 12),

    -- 13-14: Core demands
    ('Anti-Rotation Core Stability',
     'Isometric trunk rigidity resisting rotational forces. Required for force transfer between lower and upper body, spinal protection.',
     'Biomotor', v_pq_stab, v_mp_anti_rot, 13),
    ('Rotational Core Control',
     'Controlled rotational torque production through torso engagement. Required for Med Ball throws, cable rotations, and sport-specific torque.',
     'Biomotor', v_pq_stab, v_mp_rotation, 14),

    -- 15-16: Structural demands (Mobility based)
    ('Squat Mobility & Positioning',
     'Active range of motion in ankle dorsiflexion, knee flexion, and hip flexion required for deep squat positioning and injury prevention.',
     'Biomotor', v_pq_mob, v_mp_squat, 15),
    ('Hip Hinge Mobility',
     'Active range of motion in hip flexion with neutral spine required for deadlift positioning, sprint posture, and hamstring health.',
     'Biomotor', v_pq_mob, v_mp_hinge, 16),

    -- 17: Work capacity
    ('Loaded Carry Endurance',
     'Sustained load carriage under locomotion demanding postural integrity, grip endurance, and trunk rigidity over time.',
     'Biomotor', v_pq_lme, v_mp_carry, 17),

    -- 18: Structural adaptation
    ('General Hypertrophy & Structural Adaptation',
     'Muscular enlargement and connective tissue remodelling through progressive mechanical tension. Foundation for long-term force production capacity.',
     'Biomotor', v_pq_hyper, v_mp_squat, 18)
    ON CONFLICT (name) DO NOTHING;
END $$;

-- ----------------------------------------------------------------
-- F6. Seed role_demand_priority for Cricket roles
--      Maps the 5 cricket roles to their priority demands.
--      Priority 1-100: higher = more important for the role.
-- ----------------------------------------------------------------
DO $$
DECLARE
    v_sport_cricket BIGINT;
    v_role_fast    BIGINT;
    v_role_spin    BIGINT;
    v_role_bat     BIGINT;
    v_role_wk      BIGINT;
    v_role_ar      BIGINT;
    v_demand RECORD;
BEGIN
    SELECT id INTO v_sport_cricket FROM sports WHERE name = 'Cricket' LIMIT 1;
    IF v_sport_cricket IS NULL THEN
        RETURN;
    END IF;

    SELECT id INTO v_role_fast FROM roles WHERE sport_id = v_sport_cricket AND name = 'Fast Bowler' LIMIT 1;
    SELECT id INTO v_role_spin FROM roles WHERE sport_id = v_sport_cricket AND name = 'Spinner' LIMIT 1;
    SELECT id INTO v_role_bat  FROM roles WHERE sport_id = v_sport_cricket AND name = 'Batter' LIMIT 1;
    SELECT id INTO v_role_wk   FROM roles WHERE sport_id = v_sport_cricket AND name = 'Wicket Keeper' LIMIT 1;
    SELECT id INTO v_role_ar   FROM roles WHERE sport_id = v_sport_cricket AND name = 'All Rounder' LIMIT 1;

    -- Fast Bowler: high-force, high-power demands
    INSERT INTO role_demand_priority (role_id, demand_id, priority, category)
    SELECT v_role_fast, id, priority, category FROM (VALUES
        ('Vertical Power', 100, 'Primary'),
        ('Horizontal Drive Power', 95, 'Primary'),
        ('Hinge Strength', 90, 'Primary'),
        ('Rotational Explosive Power', 85, 'Primary'),
        ('Squat Strength', 80, 'Primary'),
        ('Single-Leg Stability', 75, 'Secondary'),
        ('Anti-Rotation Core Stability', 70, 'Secondary'),
        ('Rotational Core Control', 65, 'Secondary'),
        ('Loaded Carry Endurance', 60, 'Secondary'),
        ('Horizontal Pull Strength', 55, 'Secondary'),
        ('Vertical Push Strength', 50, 'Tertiary'),
        ('General Hypertrophy & Structural Adaptation', 45, 'Tertiary')
    ) AS d(name, priority, category)
    JOIN performance_demands pd ON pd.name = d.name
    ON CONFLICT (role_id, demand_id) DO NOTHING;

    -- Spinner: rotational dominant
    INSERT INTO role_demand_priority (role_id, demand_id, priority, category)
    SELECT v_role_spin, id, priority, category FROM (VALUES
        ('Rotational Explosive Power', 100, 'Primary'),
        ('Rotational Core Control', 95, 'Primary'),
        ('Anti-Rotation Core Stability', 90, 'Primary'),
        ('Hinge Strength', 85, 'Primary'),
        ('Horizontal Pull Strength', 80, 'Secondary'),
        ('Vertical Pull Strength', 75, 'Secondary'),
        ('Squat Strength', 70, 'Secondary'),
        ('Single-Leg Stability', 65, 'Secondary'),
        ('Hip Hinge Mobility', 60, 'Secondary'),
        ('Squat Mobility & Positioning', 55, 'Tertiary'),
        ('Loaded Carry Endurance', 50, 'Tertiary'),
        ('General Hypertrophy & Structural Adaptation', 45, 'Tertiary')
    ) AS d(name, priority, category)
    JOIN performance_demands pd ON pd.name = d.name
    ON CONFLICT (role_id, demand_id) DO NOTHING;

    -- Batter: multi-directional power + speed
    INSERT INTO role_demand_priority (role_id, demand_id, priority, category)
    SELECT v_role_bat, id, priority, category FROM (VALUES
        ('Horizontal Drive Power', 100, 'Primary'),
        ('Rotational Explosive Power', 95, 'Primary'),
        ('Vertical Power', 90, 'Primary'),
        ('Single-Leg Stability', 85, 'Primary'),
        ('Single-Leg Power', 80, 'Secondary'),
        ('Horizontal Pull Strength', 75, 'Secondary'),
        ('Anti-Rotation Core Stability', 70, 'Secondary'),
        ('Squat Strength', 65, 'Secondary'),
        ('Hinge Strength', 60, 'Secondary'),
        ('Squat Mobility & Positioning', 55, 'Tertiary'),
        ('Hip Hinge Mobility', 50, 'Tertiary'),
        ('General Hypertrophy & Structural Adaptation', 45, 'Tertiary')
    ) AS d(name, priority, category)
    JOIN performance_demands pd ON pd.name = d.name
    ON CONFLICT (role_id, demand_id) DO NOTHING;

    -- Wicket Keeper: squat endurance + reactive lateral power
    INSERT INTO role_demand_priority (role_id, demand_id, priority, category)
    SELECT v_role_wk, id, priority, category FROM (VALUES
        ('Squat Strength', 100, 'Primary'),
        ('Squat Mobility & Positioning', 95, 'Primary'),
        ('Single-Leg Stability', 90, 'Primary'),
        ('Single-Leg Power', 85, 'Primary'),
        ('Vertical Power', 80, 'Secondary'),
        ('Rotational Core Control', 75, 'Secondary'),
        ('Anti-Rotation Core Stability', 70, 'Secondary'),
        ('Horizontal Drive Power', 65, 'Secondary'),
        ('Loaded Carry Endurance', 60, 'Secondary'),
        ('General Hypertrophy & Structural Adaptation', 55, 'Tertiary'),
        ('Horizontal Pull Strength', 50, 'Tertiary'),
        ('Horizontal Push Strength', 45, 'Tertiary')
    ) AS d(name, priority, category)
    JOIN performance_demands pd ON pd.name = d.name
    ON CONFLICT (role_id, demand_id) DO NOTHING;

    -- All Rounder: balanced generalist
    INSERT INTO role_demand_priority (role_id, demand_id, priority, category)
    SELECT v_role_ar, id, priority, category FROM (VALUES
        ('Vertical Power', 90, 'Primary'),
        ('Horizontal Drive Power', 85, 'Primary'),
        ('Squat Strength', 85, 'Primary'),
        ('Hinge Strength', 80, 'Primary'),
        ('Rotational Explosive Power', 75, 'Secondary'),
        ('Single-Leg Stability', 75, 'Secondary'),
        ('Anti-Rotation Core Stability', 70, 'Secondary'),
        ('Loaded Carry Endurance', 65, 'Secondary'),
        ('Horizontal Pull Strength', 60, 'Tertiary'),
        ('Horizontal Push Strength', 55, 'Tertiary'),
        ('General Hypertrophy & Structural Adaptation', 50, 'Tertiary'),
        ('Hip Hinge Mobility', 45, 'Tertiary')
    ) AS d(name, priority, category)
    JOIN performance_demands pd ON pd.name = d.name
    ON CONFLICT (role_id, demand_id) DO NOTHING;
END $$;

-- ----------------------------------------------------------------
-- F7. Seed initial exercise_demand_mapping for existing exercises.
--      Maps each exercise to its primary and secondary demands based
--      on its existing movement_pattern + physical_quality mappings.
--      This ensures the constraint solver can immediately find
--      exercises by demand.
-- ----------------------------------------------------------------
DO $$
DECLARE
    v_demand RECORD;
    v_exercise RECORD;
    v_mp_id BIGINT;
    v_pq_id BIGINT;
    v_score INT;
    v_is_primary BOOLEAN;
BEGIN
    -- Map each exercise to demands based on its movement pattern + quality mappings
    FOR v_exercise IN
        SELECT e.id AS exercise_id, e.name
        FROM exercises e
    LOOP
        -- For each demand whose pattern matches the exercise's primary pattern
        -- AND whose quality matches a high-scored quality for that exercise
        FOR v_demand IN
            SELECT pd.id AS demand_id, pd.name AS demand_name,
                   pd.primary_quality_id, pd.primary_pattern_id
            FROM performance_demands pd
            WHERE pd.is_active = TRUE
        LOOP
            -- Check if this exercise has the required movement pattern
            SELECT mp.id INTO v_mp_id
            FROM exercise_movement_patterns emp
            JOIN movement_patterns mp ON emp.movement_pattern_id = mp.id
            WHERE emp.exercise_id = v_exercise.exercise_id
              AND mp.id = v_demand.primary_pattern_id
              AND emp.pattern_priority = 'Primary'
            LIMIT 1;

            IF v_mp_id IS NOT NULL THEN
                -- Check if this exercise has the required physical quality
                SELECT epq.relevance_score INTO v_score
                FROM exercise_physical_qualities epq
                WHERE epq.exercise_id = v_exercise.exercise_id
                  AND epq.physical_quality_id = v_demand.primary_quality_id
                LIMIT 1;

                IF v_score IS NOT NULL AND v_score >= 6 THEN
                    v_is_primary := (v_score >= 9);

                    INSERT INTO exercise_demand_mapping
                        (exercise_id, demand_id, relevance_score, is_primary)
                    VALUES
                        (v_exercise.exercise_id, v_demand.demand_id, v_score, v_is_primary)
                    ON CONFLICT (exercise_id, demand_id) DO NOTHING;
                END IF;
            END IF;
        END LOOP;
    END LOOP;
END $$;

-- ----------------------------------------------------------------
-- Index Strategy — complement to existing indexes
-- ----------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_demands_quality_pattern
    ON performance_demands(primary_quality_id, primary_pattern_id);

CREATE INDEX IF NOT EXISTS idx_demands_active
    ON performance_demands(is_active, display_order);

CREATE INDEX IF NOT EXISTS idx_movement_patterns_family
    ON movement_patterns(family_id, display_order);

CREATE INDEX IF NOT EXISTS idx_movement_patterns_active
    ON movement_patterns(is_active);

CREATE INDEX IF NOT EXISTS idx_physical_qualities_category
    ON physical_qualities(category_id, display_order);

CREATE INDEX IF NOT EXISTS idx_physical_qualities_active
    ON physical_qualities(is_active);

COMMIT;
