-- Forge Exercise Intelligence Database - Migration 000024 (Up)
-- Description: Athlete State, Training Load, and Injury Risk Layers
--
-- Creates 3 new tables + 1 view + extends domain_events:
--   1. athlete_state_snapshots  — immutable readiness records per point in time
--   2. training_load_events     — sport-agnostic session load with optional metrics
--   3. injury_risk_profiles     — computed multi-factor risk per athlete
--   4. acute_chronic_load_view  — ACWR calculation view
--
-- Also extends domain_events aggregate_type CHECK to support new event types
-- emitted by the new intelligence services.

BEGIN;

-- ================================================================
-- SECTION 0: Extend domain_events for new aggregate types
-- ================================================================

ALTER TABLE domain_events
    DROP CONSTRAINT IF EXISTS domain_events_aggregate_type_check;

ALTER TABLE domain_events
    ADD CONSTRAINT domain_events_aggregate_type_check
    CHECK (aggregate_type IN (
        'athlete', 'assessment', 'program', 'session',
        'injury', 'exercise', 'template', 'organization',
        'athlete_state', 'training_load', 'injury_risk',
        'demand_score', 'recommendation', 'metric'
    ));

-- ================================================================
-- SECTION 1: athlete_state_snapshots
-- Immutable point-in-time record of athlete readiness.
-- Never overwritten — each assessment or state recalculation
-- creates a new row for full historical traceability.
-- ================================================================

CREATE TABLE IF NOT EXISTS athlete_state_snapshots (
    id                  BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    athlete_id          BIGINT NOT NULL REFERENCES athletes(id) ON DELETE CASCADE,
    organization_id     BIGINT DEFAULT NULL,
    snapshot_date       DATE NOT NULL,

    -- Composite readiness scores (0-100 scale)
    readiness_score     DECIMAL(5, 2) CHECK (readiness_score IS NULL OR readiness_score BETWEEN 0 AND 100),
    fatigue_score       DECIMAL(5, 2) CHECK (fatigue_score IS NULL OR fatigue_score BETWEEN 0 AND 100),
    recovery_score      DECIMAL(5, 2) CHECK (recovery_score IS NULL OR recovery_score BETWEEN 0 AND 100),
    injury_risk_score   DECIMAL(5, 2) CHECK (injury_risk_score IS NULL OR injury_risk_score BETWEEN 0 AND 100),

    -- Core demand state scores (0-100 scale)
    -- These represent the athlete's CURRENT CAPACITY for each demand category
    power_state         DECIMAL(5, 2) CHECK (power_state IS NULL OR power_state BETWEEN 0 AND 100),
    strength_state      DECIMAL(5, 2) CHECK (strength_state IS NULL OR strength_state BETWEEN 0 AND 100),
    speed_state         DECIMAL(5, 2) CHECK (speed_state IS NULL OR speed_state BETWEEN 0 AND 100),
    mobility_state      DECIMAL(5, 2) CHECK (mobility_state IS NULL OR mobility_state BETWEEN 0 AND 100),
    work_capacity_state DECIMAL(5, 2) CHECK (work_capacity_state IS NULL OR work_capacity_state BETWEEN 0 AND 100),

    -- Extensible — future demand categories without schema changes
    demand_states       JSONB NOT NULL DEFAULT '{}'::jsonb,

    -- Metadata
    calculation_version VARCHAR(20) NOT NULL DEFAULT '1.0.0',
    source_event_id     BIGINT REFERENCES domain_events(id) ON DELETE SET NULL,
    metadata_json       JSONB DEFAULT '{}'::jsonb,

    created_at          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Enforce one snapshot per athlete per day (no duplicates)
    UNIQUE (athlete_id, snapshot_date)
);

CREATE INDEX IF NOT EXISTS idx_athlete_state_athlete
    ON athlete_state_snapshots(athlete_id, snapshot_date DESC);

CREATE INDEX IF NOT EXISTS idx_athlete_state_org
    ON athlete_state_snapshots(organization_id, snapshot_date DESC);

COMMENT ON TABLE athlete_state_snapshots IS
    'Immutable point-in-time athlete readiness records. Each snapshot captures holistic state: readiness, fatigue, recovery, injury risk, and demand-specific capacities. Never overwritten — enables longitudinal analysis and AI training.';
COMMENT ON COLUMN athlete_state_snapshots.demand_states IS
    'Extensible JSONB for future demand categories beyond the standard 5 core states. Keys are demand_name or demand_id, values are 0-100 scores.';

-- ================================================================
-- SECTION 2: training_load_events
-- Sport-agnostic session load recording. Each row represents one
-- training session or competition with RPE-based internal load
-- and optional external load metrics.
--
-- Metric definitions are NOT hardcoded. Sport scientists configure
-- which metrics to track per sport/phase via entity_relationships
-- or application-level configuration.
-- ================================================================

CREATE TABLE IF NOT EXISTS training_load_events (
    id                  BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    athlete_id          BIGINT NOT NULL REFERENCES athletes(id) ON DELETE CASCADE,
    organization_id     BIGINT DEFAULT NULL,
    session_date        DATE NOT NULL,
    session_type        VARCHAR(50) NOT NULL DEFAULT 'training'
                        CHECK (session_type IN ('training', 'competition', 'recovery', 'other')),
    duration_minutes    INT NOT NULL CHECK (duration_minutes > 0),
    session_rpe         INT NOT NULL CHECK (session_rpe BETWEEN 1 AND 10),

    -- Internal load (calculated: duration_minutes * session_rpe)
    load_score          DECIMAL(10, 2) NOT NULL CHECK (load_score >= 0),

    -- External load metrics — sport-agnostic generic fields
    -- Sport-specific metrics are stored in optional_metrics JSONB
    sprint_count        INT DEFAULT NULL CHECK (sprint_count IS NULL OR sprint_count >= 0),
    jump_count          INT DEFAULT NULL CHECK (jump_count IS NULL OR jump_count >= 0),
    throw_count         INT DEFAULT NULL CHECK (throw_count IS NULL OR throw_count >= 0),
    high_speed_distance DECIMAL(8, 2) DEFAULT NULL CHECK (high_speed_distance IS NULL OR high_speed_distance >= 0),

    -- Extensible: any sport-specific or context-specific metrics
    optional_metrics    JSONB NOT NULL DEFAULT '{}'::jsonb,

    -- Metadata
    source              VARCHAR(100) DEFAULT NULL,
    notes               TEXT DEFAULT NULL,
    metadata_json       JSONB DEFAULT '{}'::jsonb,

    created_at          TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_training_load_athlete
    ON training_load_events(athlete_id, session_date DESC);

CREATE INDEX IF NOT EXISTS idx_training_load_date
    ON training_load_events(session_date DESC);

CREATE INDEX IF NOT EXISTS idx_training_load_org
    ON training_load_events(organization_id, session_date DESC);

CREATE INDEX IF NOT EXISTS idx_training_load_type
    ON training_load_events(session_type);

COMMENT ON TABLE training_load_events IS
    'Sport-agnostic training session load records. Internal load via session RPE × duration. External load via optional generic metrics (sprint_count, jump_count, throw_count, high_speed_distance) plus extensible optional_metrics JSONB. No sport-specific columns. All metric definitions are configurable at the application layer.';

-- ================================================================
-- SECTION 3: acute_chronic_load_view
-- Materialized view for ACWR (Acute:Chronic Workload Ratio).
-- 7-day acute load / 28-day chronic load.
-- Calculated per athlete per day using rolling windows.
-- ================================================================

CREATE OR REPLACE VIEW acute_chronic_load_view AS
WITH daily_load AS (
    SELECT
        athlete_id,
        session_date,
        SUM(load_score) AS daily_load
    FROM training_load_events
    GROUP BY athlete_id, session_date
),
rolling_windows AS (
    SELECT
        athlete_id,
        session_date,
        daily_load,
        -- Acute: 7-day rolling sum (including current day)
        SUM(daily_load) OVER (
            PARTITION BY athlete_id
            ORDER BY session_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS acute_7_day_load,
        -- Chronic: 28-day rolling sum (including current day)
        SUM(daily_load) OVER (
            PARTITION BY athlete_id
            ORDER BY session_date
            ROWS BETWEEN 27 PRECEDING AND CURRENT ROW
        ) AS chronic_28_day_load
    FROM daily_load
)
SELECT
    athlete_id,
    session_date,
    daily_load,
    acute_7_day_load,
    chronic_28_day_load,
    CASE
        WHEN chronic_28_day_load > 0
        THEN ROUND((acute_7_day_load::DECIMAL / (chronic_28_day_load / 28.0 * 7.0))::DECIMAL, 2)
        ELSE NULL
    END AS acwr,
    '1.0.0' AS calculation_version
FROM rolling_windows
ORDER BY athlete_id, session_date DESC;

COMMENT ON VIEW acute_chronic_load_view IS
    'ACWR calculation view. Version 1.0.0: 7-day acute / 28-day chronic ratio. Acute = 7-day rolling sum. Chronic = 28-day rolling sum normalized to 7-day equivalent. View ensures calculation is always up-to-date.';

-- ================================================================
-- SECTION 4: injury_risk_profiles
-- Computed multi-factor injury risk for each athlete.
-- Combines demand deficits, training load, compliance, and
-- assessment trends into an explainable risk score.
-- Each profile is versioned and time-bounded.
-- ================================================================

CREATE TABLE IF NOT EXISTS injury_risk_profiles (
    id                      BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    athlete_id              BIGINT NOT NULL REFERENCES athletes(id) ON DELETE CASCADE,
    organization_id         BIGINT DEFAULT NULL,

    -- Temporal bounds (NULL = active/latest)
    valid_from              DATE NOT NULL DEFAULT CURRENT_DATE,
    valid_until             DATE DEFAULT NULL,

    -- Risk assessment
    risk_level              VARCHAR(20) NOT NULL DEFAULT 'moderate'
                            CHECK (risk_level IN ('low', 'moderate', 'high', 'critical')),
    risk_score              DECIMAL(5, 2) NOT NULL CHECK (risk_score BETWEEN 0 AND 100),
    risk_factors            JSONB NOT NULL DEFAULT '[]'::jsonb,
    recommended_interventions JSONB NOT NULL DEFAULT '[]'::jsonb,

    -- Explainability: breakdown of what contributed to the risk score
    score_breakdown         JSONB NOT NULL DEFAULT '{}'::jsonb,

    -- Metadata
    calculation_version     VARCHAR(20) NOT NULL DEFAULT '1.0.0',
    source_event_id         BIGINT REFERENCES domain_events(id) ON DELETE SET NULL,
    metadata_json           JSONB DEFAULT '{}'::jsonb,

    created_at              TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_injury_risk_athlete
    ON injury_risk_profiles(athlete_id, valid_from DESC);

CREATE INDEX IF NOT EXISTS idx_injury_risk_level
    ON injury_risk_profiles(risk_level);

CREATE INDEX IF NOT EXISTS idx_injury_risk_org
    ON injury_risk_profiles(organization_id);

COMMENT ON TABLE injury_risk_profiles IS
    'Computed multi-factor injury risk for each athlete. Combines demand deficits (from injury_risk_demand_mapping), training load (ACWR), compliance, and assessment trends into an explainable risk score with factor breakdown. Each profile is versioned and time-bounded for historical tracking.';

COMMIT;
