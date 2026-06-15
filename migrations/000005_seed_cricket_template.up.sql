-- Forge Exercise Intelligence Database - Migration 000005 (Up)
-- Description: Seed Cricket Fast Bowler athletic template, slots, exercises, and mappings.

-- -------------------------------------------------------------
-- Seed Sport: Cricket (if not exists)
-- -------------------------------------------------------------
INSERT INTO sports (name, category, description) 
VALUES ('Cricket', 'Team Sports', 'Requires high repeat sprint speed, rotational power, shoulder health, and lower body bracing capacity.')
ON CONFLICT (name) DO NOTHING;

-- -------------------------------------------------------------
-- Seed Cricket Fast Bowler Template
-- -------------------------------------------------------------
INSERT INTO movement_templates (name, sport_id, athlete_role, training_goal) VALUES
(
    'Cricket Fast Bowler Power', 
    (SELECT id FROM sports WHERE name = 'Cricket'), 
    'Fast Bowler', 
    'Develop lower body bracing capacity, explosive triple extension, and rotational power specific to the fast bowling release phase.'
);

-- -------------------------------------------------------------
-- Seed Slots
-- -------------------------------------------------------------
INSERT INTO template_slots (template_id, slot_type, name, display_order, notes) VALUES
(
    (SELECT id FROM movement_templates WHERE name = 'Cricket Fast Bowler Power'), 
    'Primary', 'Max Dynamic Output (Bilateral)', 1, 
    'Bilateral explosive lift designed to increase vertical ground reaction forces for the front-foot block.'
),
(
    (SELECT id FROM movement_templates WHERE name = 'Cricket Fast Bowler Power'), 
    'Secondary', 'Unilateral Force Production', 2, 
    'Unilateral hops or lateral bounds targeting unilateral deceleration and hip stability during the run-up.'
),
(
    (SELECT id FROM movement_templates WHERE name = 'Cricket Fast Bowler Power'), 
    'Accessory', 'Triple Extension Acceleration', 3, 
    'Accessory ballistic work utilizing a hip hinge to mimic the bowling release extension.'
),
(
    (SELECT id FROM movement_templates WHERE name = 'Cricket Fast Bowler Power'), 
    'Core', 'Trunk Rotational Velocity', 4, 
    'Rotational trunk power to transfer force from the lower body to the shoulder at release.'
);

-- -------------------------------------------------------------
-- Seed Specific Exercises for Cricket Fast Bowler
-- -------------------------------------------------------------
INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type) VALUES
(
    'Trap Bar Jump Squat', 
    'Stand inside the hex bar, squat down slightly, and jump explosively, extending the hips and knees. Focus on maximal power and landing absorbing force.', 
    'Advanced', 'Compound', 'Push'
),
(
    'Single-Leg Lateral Bound', 
    'Push off one leg sideways, jumping as far as possible laterally, landing softly on the opposite leg and stabilizing before repeating.', 
    'Intermediate', 'Compound', 'Push'
),
(
    'Medicine Ball Overhead Backwards Toss', 
    'Hold a medicine ball, descend into a shallow hinge, and explosively throw the ball backward overhead, extending the hips and shoulders.', 
    'Intermediate', 'Compound', 'Hinge'
),
(
    'Medicine Ball Rotational Chest Pass', 
    'Stand sideways to a wall, hold a medicine ball at the chest, and throw it forcefully using hip rotation and chest push.', 
    'Beginner', 'Compound', 'Rotation'
),
(
    'Cable Pallof Press with Rotation', 
    'Hold a cable at chest height, press out to anti-rotate, then execute a controlled hip-driven rotation against the cable load.', 
    'Intermediate', 'Compound', 'Rotation'
)
ON CONFLICT (name) DO NOTHING;

-- -------------------------------------------------------------
-- Seed Exercise Equipment Mappings
-- -------------------------------------------------------------
INSERT INTO exercise_equipment (exercise_id, equipment_id, is_required) VALUES
((SELECT id FROM exercises WHERE name = 'Trap Bar Jump Squat'), (SELECT id FROM equipment WHERE name = 'Trap Bar'), TRUE),
((SELECT id FROM exercises WHERE name = 'Single-Leg Lateral Bound'), (SELECT id FROM equipment WHERE name = 'Bodyweight'), TRUE),
((SELECT id FROM exercises WHERE name = 'Medicine Ball Overhead Backwards Toss'), (SELECT id FROM equipment WHERE name = 'Medicine Ball'), TRUE),
((SELECT id FROM exercises WHERE name = 'Medicine Ball Rotational Chest Pass'), (SELECT id FROM equipment WHERE name = 'Medicine Ball'), TRUE),
((SELECT id FROM exercises WHERE name = 'Cable Pallof Press with Rotation'), (SELECT id FROM equipment WHERE name = 'Cable Machine'), TRUE);

-- -------------------------------------------------------------
-- Seed Exercise Movement Pattern Mappings
-- -------------------------------------------------------------
INSERT INTO exercise_movement_patterns (exercise_id, movement_pattern_id, pattern_priority) VALUES
((SELECT id FROM exercises WHERE name = 'Trap Bar Jump Squat'), (SELECT id FROM movement_patterns WHERE name = 'Squat'), 'Primary'),
((SELECT id FROM exercises WHERE name = 'Single-Leg Lateral Bound'), (SELECT id FROM movement_patterns WHERE name = 'Lunge (Single-Leg)'), 'Primary'),
((SELECT id FROM exercises WHERE name = 'Medicine Ball Overhead Backwards Toss'), (SELECT id FROM movement_patterns WHERE name = 'Hinge'), 'Primary'),
((SELECT id FROM exercises WHERE name = 'Medicine Ball Rotational Chest Pass'), (SELECT id FROM movement_patterns WHERE name = 'Rotation'), 'Primary'),
((SELECT id FROM exercises WHERE name = 'Cable Pallof Press with Rotation'), (SELECT id FROM movement_patterns WHERE name = 'Rotation'), 'Primary'),
((SELECT id FROM exercises WHERE name = 'Cable Pallof Press with Rotation'), (SELECT id FROM movement_patterns WHERE name = 'Anti-Rotation'), 'Secondary');

-- -------------------------------------------------------------
-- Seed Exercise Physical Quality Mappings
-- -------------------------------------------------------------
INSERT INTO exercise_physical_qualities (exercise_id, physical_quality_id, relevance_score) VALUES
((SELECT id FROM exercises WHERE name = 'Trap Bar Jump Squat'), (SELECT id FROM physical_qualities WHERE name = 'Rate of Force Development'), 10),
((SELECT id FROM exercises WHERE name = 'Trap Bar Jump Squat'), (SELECT id FROM physical_qualities WHERE name = 'Maximal Strength'), 8),
((SELECT id FROM exercises WHERE name = 'Single-Leg Lateral Bound'), (SELECT id FROM physical_qualities WHERE name = 'Rate of Force Development'), 8),
((SELECT id FROM exercises WHERE name = 'Single-Leg Lateral Bound'), (SELECT id FROM physical_qualities WHERE name = 'Stability'), 9),
((SELECT id FROM exercises WHERE name = 'Medicine Ball Overhead Backwards Toss'), (SELECT id FROM physical_qualities WHERE name = 'Rate of Force Development'), 9),
((SELECT id FROM exercises WHERE name = 'Medicine Ball Rotational Chest Pass'), (SELECT id FROM physical_qualities WHERE name = 'Rate of Force Development'), 8),
((SELECT id FROM exercises WHERE name = 'Cable Pallof Press with Rotation'), (SELECT id FROM physical_qualities WHERE name = 'Stability'), 9);

-- -------------------------------------------------------------
-- Seed Exercise Training Method Mappings
-- -------------------------------------------------------------
INSERT INTO exercise_training_methods (exercise_id, training_method_id) VALUES
((SELECT id FROM exercises WHERE name = 'Trap Bar Jump Squat'), (SELECT id FROM training_methods WHERE name = 'Velocity-Based Training')),
((SELECT id FROM exercises WHERE name = 'Single-Leg Lateral Bound'), (SELECT id FROM training_methods WHERE name = 'Plyometric (Fast)')),
((SELECT id FROM exercises WHERE name = 'Medicine Ball Overhead Backwards Toss'), (SELECT id FROM training_methods WHERE name = 'Plyometric (Slow)')),
((SELECT id FROM exercises WHERE name = 'Medicine Ball Rotational Chest Pass'), (SELECT id FROM training_methods WHERE name = 'Plyometric (Slow)')),
((SELECT id FROM exercises WHERE name = 'Cable Pallof Press with Rotation'), (SELECT id FROM training_methods WHERE name = 'Isometric (Yielding)'));

-- -------------------------------------------------------------
-- Seed Exercise Sport Mappings
-- -------------------------------------------------------------
INSERT INTO exercise_sport_mapping (exercise_id, sport_id, specificity_rating, transfer_index) VALUES
((SELECT id FROM exercises WHERE name = 'Trap Bar Jump Squat'), (SELECT id FROM sports WHERE name = 'Cricket'), 10, 0.90),
((SELECT id FROM exercises WHERE name = 'Single-Leg Lateral Bound'), (SELECT id FROM sports WHERE name = 'Cricket'), 9, 0.88),
((SELECT id FROM exercises WHERE name = 'Medicine Ball Overhead Backwards Toss'), (SELECT id FROM sports WHERE name = 'Cricket'), 8, 0.82),
((SELECT id FROM exercises WHERE name = 'Medicine Ball Rotational Chest Pass'), (SELECT id FROM sports WHERE name = 'Cricket'), 9, 0.85),
((SELECT id FROM exercises WHERE name = 'Cable Pallof Press with Rotation'), (SELECT id FROM sports WHERE name = 'Cricket'), 8, 0.78);

-- -------------------------------------------------------------
-- Seed Exercise Tags Mappings
-- -------------------------------------------------------------
INSERT INTO exercise_tags (exercise_id, tag_id) VALUES
((SELECT id FROM exercises WHERE name = 'Trap Bar Jump Squat'), (SELECT id FROM tags WHERE name = 'Primary Lift')),
((SELECT id FROM exercises WHERE name = 'Trap Bar Jump Squat'), (SELECT id FROM tags WHERE name = 'Bilateral')),
((SELECT id FROM exercises WHERE name = 'Trap Bar Jump Squat'), (SELECT id FROM tags WHERE name = 'Explosive')),

((SELECT id FROM exercises WHERE name = 'Single-Leg Lateral Bound'), (SELECT id FROM tags WHERE name = 'Accessory')),
((SELECT id FROM exercises WHERE name = 'Single-Leg Lateral Bound'), (SELECT id FROM tags WHERE name = 'Unilateral')),
((SELECT id FROM exercises WHERE name = 'Single-Leg Lateral Bound'), (SELECT id FROM tags WHERE name = 'Explosive')),

((SELECT id FROM exercises WHERE name = 'Medicine Ball Overhead Backwards Toss'), (SELECT id FROM tags WHERE name = 'Accessory')),
((SELECT id FROM exercises WHERE name = 'Medicine Ball Overhead Backwards Toss'), (SELECT id FROM tags WHERE name = 'Bilateral')),
((SELECT id FROM exercises WHERE name = 'Medicine Ball Overhead Backwards Toss'), (SELECT id FROM tags WHERE name = 'Explosive')),
((SELECT id FROM exercises WHERE name = 'Medicine Ball Overhead Backwards Toss'), (SELECT id FROM tags WHERE name = 'Posterior Chain')),

((SELECT id FROM exercises WHERE name = 'Medicine Ball Rotational Chest Pass'), (SELECT id FROM tags WHERE name = 'Accessory')),
((SELECT id FROM exercises WHERE name = 'Medicine Ball Rotational Chest Pass'), (SELECT id FROM tags WHERE name = 'Bilateral')),
((SELECT id FROM exercises WHERE name = 'Medicine Ball Rotational Chest Pass'), (SELECT id FROM tags WHERE name = 'Explosive')),

((SELECT id FROM exercises WHERE name = 'Cable Pallof Press with Rotation'), (SELECT id FROM tags WHERE name = 'Accessory'));

-- -------------------------------------------------------------
-- Seed Slot Requirements
-- -------------------------------------------------------------
INSERT INTO slot_requirements (slot_id, movement_pattern_id, physical_quality_id, training_method_id, equipment_id, difficulty_level, min_relevance_score, min_specificity_rating) VALUES
(
    -- Primary Slot: Squat, RFD/Power, VBT, Trap Bar, Advanced
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Cricket Fast Bowler Power' AND ts.display_order = 1),
    (SELECT id FROM movement_patterns WHERE name = 'Squat'),
    (SELECT id FROM physical_qualities WHERE name = 'Rate of Force Development'),
    (SELECT id FROM training_methods WHERE name = 'Velocity-Based Training'),
    (SELECT id FROM equipment WHERE name = 'Trap Bar'),
    'Advanced', 8, 8
),
(
    -- Secondary Slot: Single-Leg, Stability/RFD, Plyometric, Bodyweight, Intermediate
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Cricket Fast Bowler Power' AND ts.display_order = 2),
    (SELECT id FROM movement_patterns WHERE name = 'Lunge (Single-Leg)'),
    (SELECT id FROM physical_qualities WHERE name = 'Rate of Force Development'),
    (SELECT id FROM training_methods WHERE name = 'Plyometric (Fast)'),
    (SELECT id FROM equipment WHERE name = 'Bodyweight'),
    'Intermediate', 7, 7
),
(
    -- Accessory Slot: Hinge, RFD, Plyo Slow, Medicine Ball, Intermediate
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Cricket Fast Bowler Power' AND ts.display_order = 3),
    (SELECT id FROM movement_patterns WHERE name = 'Hinge'),
    (SELECT id FROM physical_qualities WHERE name = 'Rate of Force Development'),
    (SELECT id FROM training_methods WHERE name = 'Plyometric (Slow)'),
    (SELECT id FROM equipment WHERE name = 'Medicine Ball'),
    'Intermediate', 7, 7
),
(
    -- Core Slot: Rotation, RFD, Plyo Slow, Medicine Ball, Beginner
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Cricket Fast Bowler Power' AND ts.display_order = 4),
    (SELECT id FROM movement_patterns WHERE name = 'Rotation'),
    (SELECT id FROM physical_qualities WHERE name = 'Rate of Force Development'),
    (SELECT id FROM training_methods WHERE name = 'Plyometric (Slow)'),
    (SELECT id FROM equipment WHERE name = 'Medicine Ball'),
    'Beginner', 7, 7
);

-- -------------------------------------------------------------
-- Seed Slot Progressions
-- -------------------------------------------------------------
INSERT INTO slot_progressions (slot_id, progression_type, intensity_target, volume_target, progression_rule, deload_protocol) VALUES
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Cricket Fast Bowler Power' AND ts.display_order = 1),
    'Velocity-Based', '0.75-0.90 m/s', '4x3', 
    'Increase load by 5-10 lbs if velocity exceeds 0.90 m/s on first reps. Strip load if it falls below 0.75 m/s.',
    'Reduce volume to 2 sets of 3 reps at 60% intensity.'
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Cricket Fast Bowler Power' AND ts.display_order = 2),
    'Qualitative/Technique', 'Max Velocity / Landing Stiff', '3x5 each side',
    'Increase lateral jump distance while maintaining landing stabilization control.',
    'Drop to 2 sets of 3 jumps focusing purely on vertical landing alignment.'
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Cricket Fast Bowler Power' AND ts.display_order = 3),
    'Qualitative/Technique', 'Max Effort', '3x6',
    'Increase medicine ball mass by 2 lbs if release speed and triple extension are maintained.',
    'Reduce sets to 2, reps to 3, focus on maximum speed.'
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Cricket Fast Bowler Power' AND ts.display_order = 4),
    'Qualitative/Technique', 'Max rotational velocity', '3x6 each side',
    'Focus on rapid hip opening and explosive release. Increase load if speed is kept.',
    'Perform 2 sets of 4 reps at moderate velocity.'
);
