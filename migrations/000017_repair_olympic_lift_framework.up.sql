-- Forge Exercise Intelligence Database - Migration 000017 (Up) - Repair
-- Description: Idempotent redeploy of 000015 contents with bugfixes.
-- Fixes: High Pull duplicate sport mapping (AF -> Rugby) at original line 200.
--         All INSERTs use ON CONFLICT DO NOTHING for idempotency.
--         All ALTER TABLE use IF NOT EXISTS for idempotency.
-- Safe to run regardless of whether 000015 partially or fully applied.

-- -------------------------------------------------------------
-- 1. Schema Changes (ALL idempotent)
-- -------------------------------------------------------------

-- 1a. Add default_exercise_id to template_slots
ALTER TABLE template_slots
ADD COLUMN IF NOT EXISTS default_exercise_id BIGINT REFERENCES exercises(id) ON DELETE SET NULL;

-- 1b. Add technical_difficulty and minimum_training_age_months to exercises
ALTER TABLE exercises
ADD COLUMN IF NOT EXISTS technical_difficulty INT CHECK (technical_difficulty BETWEEN 1 AND 10);

ALTER TABLE exercises
ADD COLUMN IF NOT EXISTS minimum_training_age_months INT NOT NULL DEFAULT 0 CHECK (minimum_training_age_months >= 0);

-- 1c. Add training_age_months to athletes
ALTER TABLE athletes
ADD COLUMN IF NOT EXISTS training_age_months INT NOT NULL DEFAULT 0 CHECK (training_age_months >= 0);

-- Update existing athletes: training_age_months = training_age_years * 12
UPDATE athletes SET training_age_months = training_age_years * 12
WHERE training_age_years IS NOT NULL AND training_age_years > 0
  AND (training_age_months IS NULL OR training_age_months = 0);

-- 1d. Add force_type 'Rotation' to exercises check constraint
ALTER TABLE exercises DROP CONSTRAINT IF EXISTS exercises_force_type_check;
ALTER TABLE exercises ADD CONSTRAINT exercises_force_type_check
    CHECK (force_type IN ('Push', 'Pull', 'Hinge', 'Carry', 'Static', 'Rotation', 'N/A'));

-- -------------------------------------------------------------
-- 2. Add New Tags (idempotent via ON CONFLICT)
-- -------------------------------------------------------------
INSERT INTO tags (name) VALUES
('Olympic Derivative'),
('Olympic Catch'),
('Olympic Overhead'),
('Strength-Speed')
ON CONFLICT (name) DO NOTHING;

-- -------------------------------------------------------------
-- 3. Seed Olympic Lift Exercises (14 exercises)
-- -------------------------------------------------------------

DO $$
DECLARE
    v_tag_derivative BIGINT;
    v_tag_catch BIGINT;
    v_tag_overhead BIGINT;
    v_tag_strength_speed BIGINT;
    v_tag_explosive BIGINT;
    v_tag_primary BIGINT;
    v_tag_bilateral BIGINT;
    v_tag_posterior BIGINT;
    v_eq_barbell BIGINT;
    v_eq_bodyweight BIGINT;
    v_mp_hinge BIGINT;
    v_mp_squat BIGINT;
    v_mp_pull_vert BIGINT;
    v_mp_push_vert BIGINT;
    v_mp_lunge BIGINT;
    v_mp_overhead_squat BIGINT;
    v_mp_rotation BIGINT;
    v_pq_rfd BIGINT;
    v_pq_max_strength BIGINT;
    v_pq_stability BIGINT;
    v_pq_mobility BIGINT;
    v_pq_hypertrophy BIGINT;
    v_tm_vbt BIGINT;
    v_tm_plyo_fast BIGINT;
    v_sport_owl BIGINT;
    v_sport_af BIGINT;
    v_sport_rugby BIGINT;
    v_sport_sprint BIGINT;
    v_sport_cricket BIGINT;
BEGIN

    -- Resolve lookups
    SELECT id INTO v_tag_derivative FROM tags WHERE name = 'Olympic Derivative';
    SELECT id INTO v_tag_catch FROM tags WHERE name = 'Olympic Catch';
    SELECT id INTO v_tag_overhead FROM tags WHERE name = 'Olympic Overhead';
    SELECT id INTO v_tag_strength_speed FROM tags WHERE name = 'Strength-Speed';
    SELECT id INTO v_tag_explosive FROM tags WHERE name = 'Explosive';
    SELECT id INTO v_tag_primary FROM tags WHERE name = 'Primary Lift';
    SELECT id INTO v_tag_bilateral FROM tags WHERE name = 'Bilateral';
    SELECT id INTO v_tag_posterior FROM tags WHERE name = 'Posterior Chain';
    SELECT id INTO v_eq_barbell FROM equipment WHERE name = 'Barbell';
    SELECT id INTO v_eq_bodyweight FROM equipment WHERE name = 'Bodyweight';
    SELECT id INTO v_mp_hinge FROM movement_patterns WHERE name = 'Hinge';
    SELECT id INTO v_mp_squat FROM movement_patterns WHERE name = 'Squat';
    SELECT id INTO v_mp_pull_vert FROM movement_patterns WHERE name = 'Pull (Vertical)';
    SELECT id INTO v_mp_push_vert FROM movement_patterns WHERE name = 'Push (Vertical)';
    SELECT id INTO v_mp_lunge FROM movement_patterns WHERE name = 'Lunge (Single-Leg)';
    SELECT id INTO v_mp_rotation FROM movement_patterns WHERE name = 'Rotation';
    SELECT id INTO v_pq_rfd FROM physical_qualities WHERE name = 'Rate of Force Development';
    SELECT id INTO v_pq_max_strength FROM physical_qualities WHERE name = 'Maximal Strength';
    SELECT id INTO v_pq_stability FROM physical_qualities WHERE name = 'Stability';
    SELECT id INTO v_pq_mobility FROM physical_qualities WHERE name = 'Mobility';
    SELECT id INTO v_pq_hypertrophy FROM physical_qualities WHERE name = 'Hypertrophy';
    SELECT id INTO v_tm_vbt FROM training_methods WHERE name = 'Velocity-Based Training';
    SELECT id INTO v_tm_plyo_fast FROM training_methods WHERE name = 'Plyometric (Fast)';
    SELECT id INTO v_sport_owl FROM sports WHERE name = 'Olympic Weightlifting';
    SELECT id INTO v_sport_af FROM sports WHERE name = 'American Football';
    SELECT id INTO v_sport_rugby FROM sports WHERE name = 'Rugby';
    SELECT id INTO v_sport_sprint FROM sports WHERE name = 'Track & Field (Sprinting)';
    SELECT id INTO v_sport_cricket FROM sports WHERE name = 'Cricket';

    -- First ensure 'Overhead Squat' movement pattern exists
    IF NOT EXISTS (SELECT 1 FROM movement_patterns WHERE name = 'Overhead Squat') THEN
        INSERT INTO movement_patterns (name, description) VALUES
        ('Overhead Squat', 'Deep squat position maintaining a barbell in a locked-out overhead position.');
    END IF;
    SELECT id INTO v_mp_overhead_squat FROM movement_patterns WHERE name = 'Overhead Squat';

    -- ================================================================
    -- 3a. OLYMPIC DERIVATIVE (Clean Pull, Mid-Thigh Pull, High Pull, Snatch Pull)
    -- ================================================================

    -- Clean Pull
    INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, minimum_training_age_months)
    VALUES (
        'Clean Pull',
        'From a deadlift start, explosively extend the hips and knees, pulling the barbell vertically. No catch. Focus on maximal triple extension velocity.',
        'Intermediate', 'Compound', 'Pull', 3, 12
    )
    ON CONFLICT (name) DO NOTHING;

    INSERT INTO exercise_equipment (exercise_id, equipment_id, is_required)
    VALUES ((SELECT id FROM exercises WHERE name = 'Clean Pull'), v_eq_barbell, TRUE)
    ON CONFLICT (exercise_id, equipment_id) DO NOTHING;

    INSERT INTO exercise_movement_patterns (exercise_id, movement_pattern_id, pattern_priority)
    VALUES ((SELECT id FROM exercises WHERE name = 'Clean Pull'), v_mp_hinge, 'Primary')
    ON CONFLICT (exercise_id, movement_pattern_id) DO NOTHING;

    INSERT INTO exercise_physical_qualities (exercise_id, physical_quality_id, relevance_score)
    VALUES ((SELECT id FROM exercises WHERE name = 'Clean Pull'), v_pq_rfd, 8),
           ((SELECT id FROM exercises WHERE name = 'Clean Pull'), v_pq_max_strength, 7)
    ON CONFLICT (exercise_id, physical_quality_id) DO NOTHING;

    INSERT INTO exercise_training_methods (exercise_id, training_method_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Clean Pull'), v_tm_vbt)
    ON CONFLICT (exercise_id, training_method_id) DO NOTHING;

    INSERT INTO exercise_sport_mapping (exercise_id, sport_id, specificity_rating, transfer_index)
    VALUES ((SELECT id FROM exercises WHERE name = 'Clean Pull'), v_sport_owl, 10, 0.90),
           ((SELECT id FROM exercises WHERE name = 'Clean Pull'), v_sport_af, 8, 0.80),
           ((SELECT id FROM exercises WHERE name = 'Clean Pull'), v_sport_rugby, 8, 0.78),
           ((SELECT id FROM exercises WHERE name = 'Clean Pull'), v_sport_sprint, 7, 0.72),
           ((SELECT id FROM exercises WHERE name = 'Clean Pull'), v_sport_cricket, 7, 0.70)
    ON CONFLICT (exercise_id, sport_id) DO NOTHING;

    INSERT INTO exercise_tags (exercise_id, tag_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Clean Pull'), v_tag_derivative),
           ((SELECT id FROM exercises WHERE name = 'Clean Pull'), v_tag_explosive),
           ((SELECT id FROM exercises WHERE name = 'Clean Pull'), v_tag_bilateral),
           ((SELECT id FROM exercises WHERE name = 'Clean Pull'), v_tag_posterior),
           ((SELECT id FROM exercises WHERE name = 'Clean Pull'), v_tag_strength_speed)
    ON CONFLICT (exercise_id, tag_id) DO NOTHING;

    -- Mid-Thigh Pull
    INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, minimum_training_age_months)
    VALUES (
        'Mid-Thigh Pull',
        'Start with the barbell at mid-thigh height (from blocks or hang). Explosively extend the hips, driving the bar upward with maximal velocity. No catch.',
        'Intermediate', 'Compound', 'Pull', 4, 24
    )
    ON CONFLICT (name) DO NOTHING;

    INSERT INTO exercise_equipment (exercise_id, equipment_id, is_required)
    VALUES ((SELECT id FROM exercises WHERE name = 'Mid-Thigh Pull'), v_eq_barbell, TRUE)
    ON CONFLICT (exercise_id, equipment_id) DO NOTHING;

    INSERT INTO exercise_movement_patterns (exercise_id, movement_pattern_id, pattern_priority)
    VALUES ((SELECT id FROM exercises WHERE name = 'Mid-Thigh Pull'), v_mp_hinge, 'Primary')
    ON CONFLICT (exercise_id, movement_pattern_id) DO NOTHING;

    INSERT INTO exercise_physical_qualities (exercise_id, physical_quality_id, relevance_score)
    VALUES ((SELECT id FROM exercises WHERE name = 'Mid-Thigh Pull'), v_pq_rfd, 10),
           ((SELECT id FROM exercises WHERE name = 'Mid-Thigh Pull'), v_pq_max_strength, 8)
    ON CONFLICT (exercise_id, physical_quality_id) DO NOTHING;

    INSERT INTO exercise_training_methods (exercise_id, training_method_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Mid-Thigh Pull'), v_tm_vbt)
    ON CONFLICT (exercise_id, training_method_id) DO NOTHING;

    INSERT INTO exercise_sport_mapping (exercise_id, sport_id, specificity_rating, transfer_index)
    VALUES ((SELECT id FROM exercises WHERE name = 'Mid-Thigh Pull'), v_sport_owl, 10, 0.95),
           ((SELECT id FROM exercises WHERE name = 'Mid-Thigh Pull'), v_sport_af, 9, 0.88),
           ((SELECT id FROM exercises WHERE name = 'Mid-Thigh Pull'), v_sport_rugby, 9, 0.85),
           ((SELECT id FROM exercises WHERE name = 'Mid-Thigh Pull'), v_sport_sprint, 8, 0.80),
           ((SELECT id FROM exercises WHERE name = 'Mid-Thigh Pull'), v_sport_cricket, 8, 0.75)
    ON CONFLICT (exercise_id, sport_id) DO NOTHING;

    INSERT INTO exercise_tags (exercise_id, tag_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Mid-Thigh Pull'), v_tag_derivative),
           ((SELECT id FROM exercises WHERE name = 'Mid-Thigh Pull'), v_tag_explosive),
           ((SELECT id FROM exercises WHERE name = 'Mid-Thigh Pull'), v_tag_bilateral),
           ((SELECT id FROM exercises WHERE name = 'Mid-Thigh Pull'), v_tag_posterior),
           ((SELECT id FROM exercises WHERE name = 'Mid-Thigh Pull'), v_tag_strength_speed)
    ON CONFLICT (exercise_id, tag_id) DO NOTHING;

    -- High Pull (BUG FIXED: duplicate v_sport_af -> v_sport_rugby)
    INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, minimum_training_age_months)
    VALUES (
        'High Pull',
        'Perform a clean pull but continue pulling the barbell upward with the arms after full extension, reaching chest height. No catch. Teaches the turnover phase.',
        'Advanced', 'Compound', 'Pull', 5, 24
    )
    ON CONFLICT (name) DO NOTHING;

    INSERT INTO exercise_equipment (exercise_id, equipment_id, is_required)
    VALUES ((SELECT id FROM exercises WHERE name = 'High Pull'), v_eq_barbell, TRUE)
    ON CONFLICT (exercise_id, equipment_id) DO NOTHING;

    INSERT INTO exercise_movement_patterns (exercise_id, movement_pattern_id, pattern_priority)
    VALUES ((SELECT id FROM exercises WHERE name = 'High Pull'), v_mp_hinge, 'Primary'),
           ((SELECT id FROM exercises WHERE name = 'High Pull'), v_mp_pull_vert, 'Secondary')
    ON CONFLICT (exercise_id, movement_pattern_id) DO NOTHING;

    INSERT INTO exercise_physical_qualities (exercise_id, physical_quality_id, relevance_score)
    VALUES ((SELECT id FROM exercises WHERE name = 'High Pull'), v_pq_rfd, 9),
           ((SELECT id FROM exercises WHERE name = 'High Pull'), v_pq_max_strength, 7)
    ON CONFLICT (exercise_id, physical_quality_id) DO NOTHING;

    INSERT INTO exercise_training_methods (exercise_id, training_method_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'High Pull'), v_tm_vbt)
    ON CONFLICT (exercise_id, training_method_id) DO NOTHING;

    -- FIXED: Changed second v_sport_af to v_sport_rugby
    INSERT INTO exercise_sport_mapping (exercise_id, sport_id, specificity_rating, transfer_index)
    VALUES ((SELECT id FROM exercises WHERE name = 'High Pull'), v_sport_owl, 10, 0.92),
           ((SELECT id FROM exercises WHERE name = 'High Pull'), v_sport_af, 8, 0.82),
           ((SELECT id FROM exercises WHERE name = 'High Pull'), v_sport_rugby, 8, 0.78),
           ((SELECT id FROM exercises WHERE name = 'High Pull'), v_sport_cricket, 7, 0.68)
    ON CONFLICT (exercise_id, sport_id) DO NOTHING;

    INSERT INTO exercise_tags (exercise_id, tag_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'High Pull'), v_tag_derivative),
           ((SELECT id FROM exercises WHERE name = 'High Pull'), v_tag_explosive),
           ((SELECT id FROM exercises WHERE name = 'High Pull'), v_tag_bilateral),
           ((SELECT id FROM exercises WHERE name = 'High Pull'), v_tag_posterior),
           ((SELECT id FROM exercises WHERE name = 'High Pull'), v_tag_strength_speed)
    ON CONFLICT (exercise_id, tag_id) DO NOTHING;

    -- Snatch Pull
    INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, minimum_training_age_months)
    VALUES (
        'Snatch Pull',
        'From a wide-grip snatch deadlift start, explosively extend the hips and knees, pulling the barbell upward. No catch. Develops explosive hip drive in the snatch pull position.',
        'Advanced', 'Compound', 'Pull', 5, 36
    )
    ON CONFLICT (name) DO NOTHING;

    INSERT INTO exercise_equipment (exercise_id, equipment_id, is_required)
    VALUES ((SELECT id FROM exercises WHERE name = 'Snatch Pull'), v_eq_barbell, TRUE)
    ON CONFLICT (exercise_id, equipment_id) DO NOTHING;

    INSERT INTO exercise_movement_patterns (exercise_id, movement_pattern_id, pattern_priority)
    VALUES ((SELECT id FROM exercises WHERE name = 'Snatch Pull'), v_mp_hinge, 'Primary'),
           ((SELECT id FROM exercises WHERE name = 'Snatch Pull'), v_mp_pull_vert, 'Secondary')
    ON CONFLICT (exercise_id, movement_pattern_id) DO NOTHING;

    INSERT INTO exercise_physical_qualities (exercise_id, physical_quality_id, relevance_score)
    VALUES ((SELECT id FROM exercises WHERE name = 'Snatch Pull'), v_pq_rfd, 9),
           ((SELECT id FROM exercises WHERE name = 'Snatch Pull'), v_pq_max_strength, 7)
    ON CONFLICT (exercise_id, physical_quality_id) DO NOTHING;

    INSERT INTO exercise_training_methods (exercise_id, training_method_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Snatch Pull'), v_tm_vbt)
    ON CONFLICT (exercise_id, training_method_id) DO NOTHING;

    INSERT INTO exercise_sport_mapping (exercise_id, sport_id, specificity_rating, transfer_index)
    VALUES ((SELECT id FROM exercises WHERE name = 'Snatch Pull'), v_sport_owl, 10, 0.93),
           ((SELECT id FROM exercises WHERE name = 'Snatch Pull'), v_sport_af, 7, 0.70),
           ((SELECT id FROM exercises WHERE name = 'Snatch Pull'), v_sport_rugby, 7, 0.68),
           ((SELECT id FROM exercises WHERE name = 'Snatch Pull'), v_sport_cricket, 5, 0.45)
    ON CONFLICT (exercise_id, sport_id) DO NOTHING;

    INSERT INTO exercise_tags (exercise_id, tag_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Snatch Pull'), v_tag_derivative),
           ((SELECT id FROM exercises WHERE name = 'Snatch Pull'), v_tag_explosive),
           ((SELECT id FROM exercises WHERE name = 'Snatch Pull'), v_tag_bilateral),
           ((SELECT id FROM exercises WHERE name = 'Snatch Pull'), v_tag_posterior),
           ((SELECT id FROM exercises WHERE name = 'Snatch Pull'), v_tag_strength_speed)
    ON CONFLICT (exercise_id, tag_id) DO NOTHING;

    -- ================================================================
    -- 3b. OLYMPIC CATCH (Power Clean, Hang Clean, Squat Clean, Clean and Jerk)
    -- ================================================================

    -- Power Clean (already exists - update with new columns)
    UPDATE exercises SET
        technical_difficulty = 7,
        minimum_training_age_months = 36
    WHERE name = 'Power Clean' AND technical_difficulty IS NULL;

    INSERT INTO exercise_tags (exercise_id, tag_id)
    SELECT id, v_tag_catch FROM exercises WHERE name = 'Power Clean'
    ON CONFLICT (exercise_id, tag_id) DO NOTHING;
    INSERT INTO exercise_tags (exercise_id, tag_id)
    SELECT id, v_tag_strength_speed FROM exercises WHERE name = 'Power Clean'
    ON CONFLICT (exercise_id, tag_id) DO NOTHING;

    -- Hang Clean
    INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, minimum_training_age_months)
    VALUES (
        'Hang Clean',
        'Starting with the barbell at mid-thigh (hang position), explosively extend the hips and pull the bar to the shoulders, catching in a quarter squat. Emphasizes velocity from the hang.',
        'Advanced', 'Compound', 'Pull', 6, 24
    )
    ON CONFLICT (name) DO NOTHING;

    INSERT INTO exercise_equipment (exercise_id, equipment_id, is_required)
    VALUES ((SELECT id FROM exercises WHERE name = 'Hang Clean'), v_eq_barbell, TRUE)
    ON CONFLICT (exercise_id, equipment_id) DO NOTHING;

    INSERT INTO exercise_movement_patterns (exercise_id, movement_pattern_id, pattern_priority)
    VALUES ((SELECT id FROM exercises WHERE name = 'Hang Clean'), v_mp_hinge, 'Primary'),
           ((SELECT id FROM exercises WHERE name = 'Hang Clean'), v_mp_squat, 'Secondary')
    ON CONFLICT (exercise_id, movement_pattern_id) DO NOTHING;

    INSERT INTO exercise_physical_qualities (exercise_id, physical_quality_id, relevance_score)
    VALUES ((SELECT id FROM exercises WHERE name = 'Hang Clean'), v_pq_rfd, 9),
           ((SELECT id FROM exercises WHERE name = 'Hang Clean'), v_pq_max_strength, 7)
    ON CONFLICT (exercise_id, physical_quality_id) DO NOTHING;

    INSERT INTO exercise_training_methods (exercise_id, training_method_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Hang Clean'), v_tm_vbt)
    ON CONFLICT (exercise_id, training_method_id) DO NOTHING;

    INSERT INTO exercise_sport_mapping (exercise_id, sport_id, specificity_rating, transfer_index)
    VALUES ((SELECT id FROM exercises WHERE name = 'Hang Clean'), v_sport_owl, 10, 0.92),
           ((SELECT id FROM exercises WHERE name = 'Hang Clean'), v_sport_af, 8, 0.82),
           ((SELECT id FROM exercises WHERE name = 'Hang Clean'), v_sport_rugby, 8, 0.80),
           ((SELECT id FROM exercises WHERE name = 'Hang Clean'), v_sport_sprint, 7, 0.75),
           ((SELECT id FROM exercises WHERE name = 'Hang Clean'), v_sport_cricket, 6, 0.60)
    ON CONFLICT (exercise_id, sport_id) DO NOTHING;

    INSERT INTO exercise_tags (exercise_id, tag_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Hang Clean'), v_tag_catch),
           ((SELECT id FROM exercises WHERE name = 'Hang Clean'), v_tag_explosive),
           ((SELECT id FROM exercises WHERE name = 'Hang Clean'), v_tag_primary),
           ((SELECT id FROM exercises WHERE name = 'Hang Clean'), v_tag_bilateral),
           ((SELECT id FROM exercises WHERE name = 'Hang Clean'), v_tag_strength_speed)
    ON CONFLICT (exercise_id, tag_id) DO NOTHING;

    -- Squat Clean (Full Clean)
    INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, minimum_training_age_months)
    VALUES (
        'Squat Clean',
        'Pull the barbell from the floor to the shoulders, receiving it in a full front squat position before standing up. Complete clean receiving position.',
        'Elite', 'Compound', 'Push', 9, 48
    )
    ON CONFLICT (name) DO NOTHING;

    INSERT INTO exercise_equipment (exercise_id, equipment_id, is_required)
    VALUES ((SELECT id FROM exercises WHERE name = 'Squat Clean'), v_eq_barbell, TRUE)
    ON CONFLICT (exercise_id, equipment_id) DO NOTHING;

    INSERT INTO exercise_movement_patterns (exercise_id, movement_pattern_id, pattern_priority)
    VALUES ((SELECT id FROM exercises WHERE name = 'Squat Clean'), v_mp_squat, 'Primary'),
           ((SELECT id FROM exercises WHERE name = 'Squat Clean'), v_mp_hinge, 'Secondary')
    ON CONFLICT (exercise_id, movement_pattern_id) DO NOTHING;

    INSERT INTO exercise_physical_qualities (exercise_id, physical_quality_id, relevance_score)
    VALUES ((SELECT id FROM exercises WHERE name = 'Squat Clean'), v_pq_rfd, 10),
           ((SELECT id FROM exercises WHERE name = 'Squat Clean'), v_pq_max_strength, 9),
           ((SELECT id FROM exercises WHERE name = 'Squat Clean'), v_pq_mobility, 8)
    ON CONFLICT (exercise_id, physical_quality_id) DO NOTHING;

    INSERT INTO exercise_training_methods (exercise_id, training_method_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Squat Clean'), v_tm_vbt)
    ON CONFLICT (exercise_id, training_method_id) DO NOTHING;

    INSERT INTO exercise_sport_mapping (exercise_id, sport_id, specificity_rating, transfer_index)
    VALUES ((SELECT id FROM exercises WHERE name = 'Squat Clean'), v_sport_owl, 10, 0.98),
           ((SELECT id FROM exercises WHERE name = 'Squat Clean'), v_sport_af, 7, 0.70),
           ((SELECT id FROM exercises WHERE name = 'Squat Clean'), v_sport_rugby, 7, 0.68),
           ((SELECT id FROM exercises WHERE name = 'Squat Clean'), v_sport_cricket, 4, 0.45)
    ON CONFLICT (exercise_id, sport_id) DO NOTHING;

    INSERT INTO exercise_tags (exercise_id, tag_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Squat Clean'), v_tag_catch),
           ((SELECT id FROM exercises WHERE name = 'Squat Clean'), v_tag_explosive),
           ((SELECT id FROM exercises WHERE name = 'Squat Clean'), v_tag_primary),
           ((SELECT id FROM exercises WHERE name = 'Squat Clean'), v_tag_bilateral)
    ON CONFLICT (exercise_id, tag_id) DO NOTHING;

    -- Clean and Jerk
    INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, minimum_training_age_months)
    VALUES (
        'Clean and Jerk',
        'Full competition lift: clean the barbell from floor to shoulders, then drive it overhead using a dip-drive movement. Complete combination lift.',
        'Elite', 'Compound', 'Push', 10, 60
    )
    ON CONFLICT (name) DO NOTHING;

    INSERT INTO exercise_equipment (exercise_id, equipment_id, is_required)
    VALUES ((SELECT id FROM exercises WHERE name = 'Clean and Jerk'), v_eq_barbell, TRUE)
    ON CONFLICT (exercise_id, equipment_id) DO NOTHING;

    INSERT INTO exercise_movement_patterns (exercise_id, movement_pattern_id, pattern_priority)
    VALUES ((SELECT id FROM exercises WHERE name = 'Clean and Jerk'), v_mp_squat, 'Primary'),
           ((SELECT id FROM exercises WHERE name = 'Clean and Jerk'), v_mp_push_vert, 'Secondary'),
           ((SELECT id FROM exercises WHERE name = 'Clean and Jerk'), v_mp_hinge, 'Tertiary')
    ON CONFLICT (exercise_id, movement_pattern_id) DO NOTHING;

    INSERT INTO exercise_physical_qualities (exercise_id, physical_quality_id, relevance_score)
    VALUES ((SELECT id FROM exercises WHERE name = 'Clean and Jerk'), v_pq_rfd, 10),
           ((SELECT id FROM exercises WHERE name = 'Clean and Jerk'), v_pq_max_strength, 9),
           ((SELECT id FROM exercises WHERE name = 'Clean and Jerk'), v_pq_stability, 9)
    ON CONFLICT (exercise_id, physical_quality_id) DO NOTHING;

    INSERT INTO exercise_training_methods (exercise_id, training_method_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Clean and Jerk'), v_tm_vbt)
    ON CONFLICT (exercise_id, training_method_id) DO NOTHING;

    INSERT INTO exercise_sport_mapping (exercise_id, sport_id, specificity_rating, transfer_index)
    VALUES ((SELECT id FROM exercises WHERE name = 'Clean and Jerk'), v_sport_owl, 10, 1.00),
           ((SELECT id FROM exercises WHERE name = 'Clean and Jerk'), v_sport_af, 6, 0.60),
           ((SELECT id FROM exercises WHERE name = 'Clean and Jerk'), v_sport_rugby, 6, 0.55),
           ((SELECT id FROM exercises WHERE name = 'Clean and Jerk'), v_sport_cricket, 3, 0.30)
    ON CONFLICT (exercise_id, sport_id) DO NOTHING;

    INSERT INTO exercise_tags (exercise_id, tag_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Clean and Jerk'), v_tag_catch),
           ((SELECT id FROM exercises WHERE name = 'Clean and Jerk'), v_tag_explosive),
           ((SELECT id FROM exercises WHERE name = 'Clean and Jerk'), v_tag_primary),
           ((SELECT id FROM exercises WHERE name = 'Clean and Jerk'), v_tag_bilateral)
    ON CONFLICT (exercise_id, tag_id) DO NOTHING;

    -- ================================================================
    -- 3c. OLYMPIC OVERHEAD (Power Snatch, Hang Snatch, Snatch Balance, Overhead Squat, Push Press, Push Jerk, Split Jerk)
    -- ================================================================

    -- Power Snatch
    INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, minimum_training_age_months)
    VALUES (
        'Power Snatch',
        'Pull the barbell from the floor to an overhead position in one motion, receiving it in a partial squat (power position). Requires wide grip and overhead mobility.',
        'Elite', 'Compound', 'Pull', 8, 48
    )
    ON CONFLICT (name) DO NOTHING;

    INSERT INTO exercise_equipment (exercise_id, equipment_id, is_required)
    VALUES ((SELECT id FROM exercises WHERE name = 'Power Snatch'), v_eq_barbell, TRUE)
    ON CONFLICT (exercise_id, equipment_id) DO NOTHING;

    INSERT INTO exercise_movement_patterns (exercise_id, movement_pattern_id, pattern_priority)
    VALUES ((SELECT id FROM exercises WHERE name = 'Power Snatch'), v_mp_hinge, 'Primary'),
           ((SELECT id FROM exercises WHERE name = 'Power Snatch'), v_mp_overhead_squat, 'Secondary')
    ON CONFLICT (exercise_id, movement_pattern_id) DO NOTHING;

    INSERT INTO exercise_physical_qualities (exercise_id, physical_quality_id, relevance_score)
    VALUES ((SELECT id FROM exercises WHERE name = 'Power Snatch'), v_pq_rfd, 10),
           ((SELECT id FROM exercises WHERE name = 'Power Snatch'), v_pq_max_strength, 8),
           ((SELECT id FROM exercises WHERE name = 'Power Snatch'), v_pq_mobility, 9),
           ((SELECT id FROM exercises WHERE name = 'Power Snatch'), v_pq_stability, 8)
    ON CONFLICT (exercise_id, physical_quality_id) DO NOTHING;

    INSERT INTO exercise_training_methods (exercise_id, training_method_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Power Snatch'), v_tm_vbt)
    ON CONFLICT (exercise_id, training_method_id) DO NOTHING;

    INSERT INTO exercise_sport_mapping (exercise_id, sport_id, specificity_rating, transfer_index)
    VALUES ((SELECT id FROM exercises WHERE name = 'Power Snatch'), v_sport_owl, 10, 0.95),
           ((SELECT id FROM exercises WHERE name = 'Power Snatch'), v_sport_af, 6, 0.60),
           ((SELECT id FROM exercises WHERE name = 'Power Snatch'), v_sport_rugby, 5, 0.50),
           ((SELECT id FROM exercises WHERE name = 'Power Snatch'), v_sport_cricket, 4, 0.35)
    ON CONFLICT (exercise_id, sport_id) DO NOTHING;

    INSERT INTO exercise_tags (exercise_id, tag_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Power Snatch'), v_tag_overhead),
           ((SELECT id FROM exercises WHERE name = 'Power Snatch'), v_tag_explosive),
           ((SELECT id FROM exercises WHERE name = 'Power Snatch'), v_tag_primary),
           ((SELECT id FROM exercises WHERE name = 'Power Snatch'), v_tag_bilateral)
    ON CONFLICT (exercise_id, tag_id) DO NOTHING;

    -- Hang Snatch
    INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, minimum_training_age_months)
    VALUES (
        'Hang Snatch',
        'Starting with the barbell at mid-thigh (hang position), explosively extend and pull the bar overhead in one motion. Develops explosive power from the hang position.',
        'Advanced', 'Compound', 'Pull', 7, 36
    )
    ON CONFLICT (name) DO NOTHING;

    INSERT INTO exercise_equipment (exercise_id, equipment_id, is_required)
    VALUES ((SELECT id FROM exercises WHERE name = 'Hang Snatch'), v_eq_barbell, TRUE)
    ON CONFLICT (exercise_id, equipment_id) DO NOTHING;

    INSERT INTO exercise_movement_patterns (exercise_id, movement_pattern_id, pattern_priority)
    VALUES ((SELECT id FROM exercises WHERE name = 'Hang Snatch'), v_mp_hinge, 'Primary'),
           ((SELECT id FROM exercises WHERE name = 'Hang Snatch'), v_mp_overhead_squat, 'Secondary')
    ON CONFLICT (exercise_id, movement_pattern_id) DO NOTHING;

    INSERT INTO exercise_physical_qualities (exercise_id, physical_quality_id, relevance_score)
    VALUES ((SELECT id FROM exercises WHERE name = 'Hang Snatch'), v_pq_rfd, 9),
           ((SELECT id FROM exercises WHERE name = 'Hang Snatch'), v_pq_max_strength, 7),
           ((SELECT id FROM exercises WHERE name = 'Hang Snatch'), v_pq_stability, 8)
    ON CONFLICT (exercise_id, physical_quality_id) DO NOTHING;

    INSERT INTO exercise_training_methods (exercise_id, training_method_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Hang Snatch'), v_tm_vbt)
    ON CONFLICT (exercise_id, training_method_id) DO NOTHING;

    INSERT INTO exercise_sport_mapping (exercise_id, sport_id, specificity_rating, transfer_index)
    VALUES ((SELECT id FROM exercises WHERE name = 'Hang Snatch'), v_sport_owl, 10, 0.93),
           ((SELECT id FROM exercises WHERE name = 'Hang Snatch'), v_sport_af, 6, 0.58),
           ((SELECT id FROM exercises WHERE name = 'Hang Snatch'), v_sport_rugby, 5, 0.48),
           ((SELECT id FROM exercises WHERE name = 'Hang Snatch'), v_sport_cricket, 4, 0.32)
    ON CONFLICT (exercise_id, sport_id) DO NOTHING;

    INSERT INTO exercise_tags (exercise_id, tag_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Hang Snatch'), v_tag_overhead),
           ((SELECT id FROM exercises WHERE name = 'Hang Snatch'), v_tag_explosive),
           ((SELECT id FROM exercises WHERE name = 'Hang Snatch'), v_tag_bilateral)
    ON CONFLICT (exercise_id, tag_id) DO NOTHING;

    -- Snatch Balance
    INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, minimum_training_age_months)
    VALUES (
        'Snatch Balance',
        'Start with the barbell overhead in a snatch grip. Dip and drive, then drop into a full overhead squat position, receiving the bar at arms length. Develops confidence and speed under the bar.',
        'Elite', 'Compound', 'Push', 8, 36
    )
    ON CONFLICT (name) DO NOTHING;

    INSERT INTO exercise_equipment (exercise_id, equipment_id, is_required)
    VALUES ((SELECT id FROM exercises WHERE name = 'Snatch Balance'), v_eq_barbell, TRUE)
    ON CONFLICT (exercise_id, equipment_id) DO NOTHING;

    INSERT INTO exercise_movement_patterns (exercise_id, movement_pattern_id, pattern_priority)
    VALUES ((SELECT id FROM exercises WHERE name = 'Snatch Balance'), v_mp_overhead_squat, 'Primary'),
           ((SELECT id FROM exercises WHERE name = 'Snatch Balance'), v_mp_push_vert, 'Secondary')
    ON CONFLICT (exercise_id, movement_pattern_id) DO NOTHING;

    INSERT INTO exercise_physical_qualities (exercise_id, physical_quality_id, relevance_score)
    VALUES ((SELECT id FROM exercises WHERE name = 'Snatch Balance'), v_pq_rfd, 7),
           ((SELECT id FROM exercises WHERE name = 'Snatch Balance'), v_pq_stability, 9),
           ((SELECT id FROM exercises WHERE name = 'Snatch Balance'), v_pq_mobility, 9)
    ON CONFLICT (exercise_id, physical_quality_id) DO NOTHING;

    INSERT INTO exercise_training_methods (exercise_id, training_method_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Snatch Balance'), v_tm_plyo_fast)
    ON CONFLICT (exercise_id, training_method_id) DO NOTHING;

    INSERT INTO exercise_sport_mapping (exercise_id, sport_id, specificity_rating, transfer_index)
    VALUES ((SELECT id FROM exercises WHERE name = 'Snatch Balance'), v_sport_owl, 10, 0.92),
           ((SELECT id FROM exercises WHERE name = 'Snatch Balance'), v_sport_af, 4, 0.40),
           ((SELECT id FROM exercises WHERE name = 'Snatch Balance'), v_sport_cricket, 3, 0.25)
    ON CONFLICT (exercise_id, sport_id) DO NOTHING;

    INSERT INTO exercise_tags (exercise_id, tag_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Snatch Balance'), v_tag_overhead),
           ((SELECT id FROM exercises WHERE name = 'Snatch Balance'), v_tag_explosive),
           ((SELECT id FROM exercises WHERE name = 'Snatch Balance'), v_tag_bilateral)
    ON CONFLICT (exercise_id, tag_id) DO NOTHING;

    -- Overhead Squat
    INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, minimum_training_age_months)
    VALUES (
        'Overhead Squat',
        'Hold a barbell overhead with a wide snatch grip. Squat to full depth while keeping the bar locked out overhead. Develops thoracic mobility, shoulder stability, and squat mechanics.',
        'Intermediate', 'Compound', 'Push', 7, 24
    )
    ON CONFLICT (name) DO NOTHING;

    INSERT INTO exercise_equipment (exercise_id, equipment_id, is_required)
    VALUES ((SELECT id FROM exercises WHERE name = 'Overhead Squat'), v_eq_barbell, TRUE)
    ON CONFLICT (exercise_id, equipment_id) DO NOTHING;

    INSERT INTO exercise_movement_patterns (exercise_id, movement_pattern_id, pattern_priority)
    VALUES ((SELECT id FROM exercises WHERE name = 'Overhead Squat'), v_mp_squat, 'Primary'),
           ((SELECT id FROM exercises WHERE name = 'Overhead Squat'), v_mp_overhead_squat, 'Secondary'),
           ((SELECT id FROM exercises WHERE name = 'Overhead Squat'), v_mp_push_vert, 'Tertiary')
    ON CONFLICT (exercise_id, movement_pattern_id) DO NOTHING;

    INSERT INTO exercise_physical_qualities (exercise_id, physical_quality_id, relevance_score)
    VALUES ((SELECT id FROM exercises WHERE name = 'Overhead Squat'), v_pq_mobility, 10),
           ((SELECT id FROM exercises WHERE name = 'Overhead Squat'), v_pq_stability, 9),
           ((SELECT id FROM exercises WHERE name = 'Overhead Squat'), v_pq_max_strength, 6)
    ON CONFLICT (exercise_id, physical_quality_id) DO NOTHING;

    INSERT INTO exercise_training_methods (exercise_id, training_method_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Overhead Squat'), v_tm_vbt)
    ON CONFLICT (exercise_id, training_method_id) DO NOTHING;

    INSERT INTO exercise_sport_mapping (exercise_id, sport_id, specificity_rating, transfer_index)
    VALUES ((SELECT id FROM exercises WHERE name = 'Overhead Squat'), v_sport_owl, 10, 0.88),
           ((SELECT id FROM exercises WHERE name = 'Overhead Squat'), v_sport_af, 6, 0.55),
           ((SELECT id FROM exercises WHERE name = 'Overhead Squat'), v_sport_rugby, 6, 0.52),
           ((SELECT id FROM exercises WHERE name = 'Overhead Squat'), v_sport_cricket, 5, 0.48)
    ON CONFLICT (exercise_id, sport_id) DO NOTHING;

    INSERT INTO exercise_tags (exercise_id, tag_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Overhead Squat'), v_tag_overhead),
           ((SELECT id FROM exercises WHERE name = 'Overhead Squat'), v_tag_bilateral),
           ((SELECT id FROM exercises WHERE name = 'Overhead Squat'), v_tag_strength_speed)
    ON CONFLICT (exercise_id, tag_id) DO NOTHING;

    -- Push Press
    INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, minimum_training_age_months)
    VALUES (
        'Push Press',
        'Dip at the knees and drive the barbell overhead using leg drive. A foundational overhead power movement that bridges strength and speed.',
        'Intermediate', 'Compound', 'Push', 4, 12
    )
    ON CONFLICT (name) DO NOTHING;

    INSERT INTO exercise_equipment (exercise_id, equipment_id, is_required)
    VALUES ((SELECT id FROM exercises WHERE name = 'Push Press'), v_eq_barbell, TRUE)
    ON CONFLICT (exercise_id, equipment_id) DO NOTHING;

    INSERT INTO exercise_movement_patterns (exercise_id, movement_pattern_id, pattern_priority)
    VALUES ((SELECT id FROM exercises WHERE name = 'Push Press'), v_mp_push_vert, 'Primary'),
           ((SELECT id FROM exercises WHERE name = 'Push Press'), v_mp_hinge, 'Secondary')
    ON CONFLICT (exercise_id, movement_pattern_id) DO NOTHING;

    INSERT INTO exercise_physical_qualities (exercise_id, physical_quality_id, relevance_score)
    VALUES ((SELECT id FROM exercises WHERE name = 'Push Press'), v_pq_rfd, 9),
           ((SELECT id FROM exercises WHERE name = 'Push Press'), v_pq_max_strength, 7),
           ((SELECT id FROM exercises WHERE name = 'Push Press'), v_pq_stability, 8)
    ON CONFLICT (exercise_id, physical_quality_id) DO NOTHING;

    INSERT INTO exercise_training_methods (exercise_id, training_method_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Push Press'), v_tm_vbt)
    ON CONFLICT (exercise_id, training_method_id) DO NOTHING;

    INSERT INTO exercise_sport_mapping (exercise_id, sport_id, specificity_rating, transfer_index)
    VALUES ((SELECT id FROM exercises WHERE name = 'Push Press'), v_sport_owl, 8, 0.75),
           ((SELECT id FROM exercises WHERE name = 'Push Press'), v_sport_af, 7, 0.68),
           ((SELECT id FROM exercises WHERE name = 'Push Press'), v_sport_rugby, 7, 0.65),
           ((SELECT id FROM exercises WHERE name = 'Push Press'), v_sport_sprint, 6, 0.58),
           ((SELECT id FROM exercises WHERE name = 'Push Press'), v_sport_cricket, 6, 0.55)
    ON CONFLICT (exercise_id, sport_id) DO NOTHING;

    INSERT INTO exercise_tags (exercise_id, tag_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Push Press'), v_tag_overhead),
           ((SELECT id FROM exercises WHERE name = 'Push Press'), v_tag_explosive),
           ((SELECT id FROM exercises WHERE name = 'Push Press'), v_tag_bilateral),
           ((SELECT id FROM exercises WHERE name = 'Push Press'), v_tag_strength_speed)
    ON CONFLICT (exercise_id, tag_id) DO NOTHING;

    -- Push Jerk
    INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, minimum_training_age_months)
    VALUES (
        'Push Jerk',
        'Dip and drive the barbell overhead, then re-bend the knees slightly to catch the bar at arms length overhead in a shallow squat. Faster than the push press.',
        'Advanced', 'Compound', 'Push', 6, 24
    )
    ON CONFLICT (name) DO NOTHING;

    INSERT INTO exercise_equipment (exercise_id, equipment_id, is_required)
    VALUES ((SELECT id FROM exercises WHERE name = 'Push Jerk'), v_eq_barbell, TRUE)
    ON CONFLICT (exercise_id, equipment_id) DO NOTHING;

    INSERT INTO exercise_movement_patterns (exercise_id, movement_pattern_id, pattern_priority)
    VALUES ((SELECT id FROM exercises WHERE name = 'Push Jerk'), v_mp_push_vert, 'Primary'),
           ((SELECT id FROM exercises WHERE name = 'Push Jerk'), v_mp_squat, 'Secondary')
    ON CONFLICT (exercise_id, movement_pattern_id) DO NOTHING;

    INSERT INTO exercise_physical_qualities (exercise_id, physical_quality_id, relevance_score)
    VALUES ((SELECT id FROM exercises WHERE name = 'Push Jerk'), v_pq_rfd, 9),
           ((SELECT id FROM exercises WHERE name = 'Push Jerk'), v_pq_stability, 8),
           ((SELECT id FROM exercises WHERE name = 'Push Jerk'), v_pq_max_strength, 7)
    ON CONFLICT (exercise_id, physical_quality_id) DO NOTHING;

    INSERT INTO exercise_training_methods (exercise_id, training_method_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Push Jerk'), v_tm_vbt)
    ON CONFLICT (exercise_id, training_method_id) DO NOTHING;

    INSERT INTO exercise_sport_mapping (exercise_id, sport_id, specificity_rating, transfer_index)
    VALUES ((SELECT id FROM exercises WHERE name = 'Push Jerk'), v_sport_owl, 9, 0.88),
           ((SELECT id FROM exercises WHERE name = 'Push Jerk'), v_sport_af, 6, 0.60),
           ((SELECT id FROM exercises WHERE name = 'Push Jerk'), v_sport_rugby, 6, 0.55),
           ((SELECT id FROM exercises WHERE name = 'Push Jerk'), v_sport_cricket, 5, 0.45)
    ON CONFLICT (exercise_id, sport_id) DO NOTHING;

    INSERT INTO exercise_tags (exercise_id, tag_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Push Jerk'), v_tag_overhead),
           ((SELECT id FROM exercises WHERE name = 'Push Jerk'), v_tag_explosive),
           ((SELECT id FROM exercises WHERE name = 'Push Jerk'), v_tag_bilateral),
           ((SELECT id FROM exercises WHERE name = 'Push Jerk'), v_tag_strength_speed)
    ON CONFLICT (exercise_id, tag_id) DO NOTHING;

    -- Split Jerk
    INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, minimum_training_age_months)
    VALUES (
        'Split Jerk',
        'Drive the barbell overhead from the shoulders, then split the legs forward and back to catch the bar at full arm extension. The most stable overhead receiving position.',
        'Elite', 'Compound', 'Push', 9, 36
    )
    ON CONFLICT (name) DO NOTHING;

    INSERT INTO exercise_equipment (exercise_id, equipment_id, is_required)
    VALUES ((SELECT id FROM exercises WHERE name = 'Split Jerk'), v_eq_barbell, TRUE)
    ON CONFLICT (exercise_id, equipment_id) DO NOTHING;

    INSERT INTO exercise_movement_patterns (exercise_id, movement_pattern_id, pattern_priority)
    VALUES ((SELECT id FROM exercises WHERE name = 'Split Jerk'), v_mp_push_vert, 'Primary'),
           ((SELECT id FROM exercises WHERE name = 'Split Jerk'), v_mp_lunge, 'Secondary')
    ON CONFLICT (exercise_id, movement_pattern_id) DO NOTHING;

    INSERT INTO exercise_physical_qualities (exercise_id, physical_quality_id, relevance_score)
    VALUES ((SELECT id FROM exercises WHERE name = 'Split Jerk'), v_pq_rfd, 10),
           ((SELECT id FROM exercises WHERE name = 'Split Jerk'), v_pq_stability, 9),
           ((SELECT id FROM exercises WHERE name = 'Split Jerk'), v_pq_max_strength, 8)
    ON CONFLICT (exercise_id, physical_quality_id) DO NOTHING;

    INSERT INTO exercise_training_methods (exercise_id, training_method_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Split Jerk'), v_tm_vbt)
    ON CONFLICT (exercise_id, training_method_id) DO NOTHING;

    INSERT INTO exercise_sport_mapping (exercise_id, sport_id, specificity_rating, transfer_index)
    VALUES ((SELECT id FROM exercises WHERE name = 'Split Jerk'), v_sport_owl, 10, 0.95),
           ((SELECT id FROM exercises WHERE name = 'Split Jerk'), v_sport_af, 6, 0.55),
           ((SELECT id FROM exercises WHERE name = 'Split Jerk'), v_sport_rugby, 5, 0.50),
           ((SELECT id FROM exercises WHERE name = 'Split Jerk'), v_sport_cricket, 4, 0.35)
    ON CONFLICT (exercise_id, sport_id) DO NOTHING;

    INSERT INTO exercise_tags (exercise_id, tag_id)
    VALUES ((SELECT id FROM exercises WHERE name = 'Split Jerk'), v_tag_overhead),
           ((SELECT id FROM exercises WHERE name = 'Split Jerk'), v_tag_explosive),
           ((SELECT id FROM exercises WHERE name = 'Split Jerk'), v_tag_bilateral),
           ((SELECT id FROM exercises WHERE name = 'Split Jerk'), v_tag_strength_speed)
    ON CONFLICT (exercise_id, tag_id) DO NOTHING;

    -- ================================================================
    -- 4. Update all existing exercises with technical_difficulty values
    -- ================================================================

    -- Update existing exercises that don't have technical_difficulty set yet
    UPDATE exercises SET technical_difficulty = 1, minimum_training_age_months = 0 WHERE name = 'Bodyweight Squat' AND technical_difficulty IS NULL;
    UPDATE exercises SET technical_difficulty = 2, minimum_training_age_months = 0 WHERE name = 'A-Skip' AND technical_difficulty IS NULL;
    UPDATE exercises SET technical_difficulty = 1, minimum_training_age_months = 0 WHERE name = 'Medicine Ball Rotational Chest Pass' AND technical_difficulty IS NULL;
    UPDATE exercises SET technical_difficulty = 1, minimum_training_age_months = 0 WHERE name = 'Medicine Ball Rotational Scoop Toss' AND technical_difficulty IS NULL;
    UPDATE exercises SET technical_difficulty = 1, minimum_training_age_months = 0 WHERE name = 'Kettlebell Swing' AND technical_difficulty IS NULL;
    UPDATE exercises SET technical_difficulty = 2, minimum_training_age_months = 0 WHERE name = 'Dumbbell Row' AND technical_difficulty IS NULL;
    UPDATE exercises SET technical_difficulty = 2, minimum_training_age_months = 0 WHERE name = 'Dumbbell Overhead Press' AND technical_difficulty IS NULL;
    UPDATE exercises SET technical_difficulty = 2, minimum_training_age_months = 0 WHERE name = 'Plank with Rotation' AND technical_difficulty IS NULL;
    UPDATE exercises SET technical_difficulty = 3, minimum_training_age_months = 0 WHERE name = 'Single-Leg Isometric Wall Sit' AND technical_difficulty IS NULL;
    UPDATE exercises SET technical_difficulty = 4, minimum_training_age_months = 6 WHERE name = 'Medicine Ball Overhead Backwards Toss' AND technical_difficulty IS NULL;
    UPDATE exercises SET technical_difficulty = 4, minimum_training_age_months = 6 WHERE name = 'Single-Leg Lateral Bound' AND technical_difficulty IS NULL;
    UPDATE exercises SET technical_difficulty = 5, minimum_training_age_months = 12 WHERE name = 'Barbell Back Squat' AND technical_difficulty IS NULL;
    UPDATE exercises SET technical_difficulty = 5, minimum_training_age_months = 12 WHERE name = 'Rear Foot Elevated Split Squat' AND technical_difficulty IS NULL;
    UPDATE exercises SET technical_difficulty = 5, minimum_training_age_months = 12 WHERE name = 'Trap Bar Deadlift' AND technical_difficulty IS NULL;
    UPDATE exercises SET technical_difficulty = 6, minimum_training_age_months = 24 WHERE name = 'Trap Bar Jump Squat' AND technical_difficulty IS NULL;
    UPDATE exercises SET technical_difficulty = 7, minimum_training_age_months = 36 WHERE name = 'Nordic Hamstring Curl' AND technical_difficulty IS NULL;
    UPDATE exercises SET technical_difficulty = 9, minimum_training_age_months = 48 WHERE name = 'Depth Jump' AND technical_difficulty IS NULL;
    UPDATE exercises SET technical_difficulty = 4, minimum_training_age_months = 6 WHERE name = 'Farmer''s Walk' AND technical_difficulty IS NULL;
    UPDATE exercises SET technical_difficulty = 3, minimum_training_age_months = 6 WHERE name = 'Medicine Ball Slam' AND technical_difficulty IS NULL;
    UPDATE exercises SET technical_difficulty = 3, minimum_training_age_months = 0 WHERE name = 'Burpee' AND technical_difficulty IS NULL;

    -- ================================================================
    -- 5. Set default_exercise_id on template slots
    -- ================================================================

    -- Cricket Fast Bowler Power slots
    UPDATE template_slots SET default_exercise_id = (SELECT id FROM exercises WHERE name = 'Trap Bar Jump Squat')
    WHERE name = 'Max Dynamic Output (Bilateral)' AND default_exercise_id IS NULL;
    UPDATE template_slots SET default_exercise_id = (SELECT id FROM exercises WHERE name = 'Single-Leg Lateral Bound')
    WHERE name = 'Unilateral Force Production' AND slot_type = 'Secondary' AND default_exercise_id IS NULL;
    UPDATE template_slots SET default_exercise_id = (SELECT id FROM exercises WHERE name = 'Medicine Ball Overhead Backwards Toss')
    WHERE name = 'Triple Extension Acceleration' AND default_exercise_id IS NULL;
    UPDATE template_slots SET default_exercise_id = (SELECT id FROM exercises WHERE name = 'Medicine Ball Rotational Chest Pass')
    WHERE name = 'Trunk Rotational Velocity' AND default_exercise_id IS NULL;

    -- Batter Strength/Power slots (from mock)
    UPDATE template_slots SET default_exercise_id = (SELECT id FROM exercises WHERE name = 'Trap Bar Deadlift')
    WHERE name = 'Explosive Hinge/Extension' AND default_exercise_id IS NULL;
    UPDATE template_slots SET default_exercise_id = (SELECT id FROM exercises WHERE name = 'Rear Foot Elevated Split Squat')
    WHERE name = 'Unilateral Drive Strength' AND default_exercise_id IS NULL;
    UPDATE template_slots SET default_exercise_id = (SELECT id FROM exercises WHERE name = 'Nordic Hamstring Curl')
    WHERE name = 'Posterior Chain Knee Flexion' AND default_exercise_id IS NULL;
    UPDATE template_slots SET default_exercise_id = (SELECT id FROM exercises WHERE name = 'Cable Pallof Press with Rotation')
    WHERE name = 'Trunk Stability in Motion' AND default_exercise_id IS NULL;

    -- Spinner slots (from mock)
    UPDATE template_slots SET default_exercise_id = (SELECT id FROM exercises WHERE name = 'Medicine Ball Rotational Scoop Toss')
    WHERE name = 'Rotational Power Slam' AND default_exercise_id IS NULL;
    UPDATE template_slots SET default_exercise_id = (SELECT id FROM exercises WHERE name = 'Barbell Back Squat')
    WHERE name = 'Base Strength Lift' AND default_exercise_id IS NULL;
    UPDATE template_slots SET default_exercise_id = (SELECT id FROM exercises WHERE name = 'Dumbbell Overhead Press')
    WHERE name = 'Unilateral Push Strength' AND default_exercise_id IS NULL;
    UPDATE template_slots SET default_exercise_id = (SELECT id FROM exercises WHERE name = 'Cable Pallof Press with Rotation')
    WHERE name = 'Anti-Rotation Stiffness' AND default_exercise_id IS NULL;

    -- Generic template slots (from 004)
    UPDATE template_slots SET default_exercise_id = (SELECT id FROM exercises WHERE name = 'Barbell Back Squat')
    WHERE name = 'Bilateral Power/Strength Lift' AND default_exercise_id IS NULL;
    UPDATE template_slots SET default_exercise_id = (SELECT id FROM exercises WHERE name = 'Rear Foot Elevated Split Squat')
    WHERE name = 'Unilateral Power/Stability' AND default_exercise_id IS NULL;
    UPDATE template_slots SET default_exercise_id = (SELECT id FROM exercises WHERE name = 'Kettlebell Swing')
    WHERE name = 'Posterior Chain Force Production' AND default_exercise_id IS NULL;
    UPDATE template_slots SET default_exercise_id = (SELECT id FROM exercises WHERE name = 'Medicine Ball Rotational Chest Pass')
    WHERE name = 'Rotational Trunk Power' AND default_exercise_id IS NULL;

END $$;
