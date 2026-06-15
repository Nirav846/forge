-- Forge Exercise Intelligence Database - Migration 000004 (Up)
-- Description: Seed movement templates, slots, requirements, progressions, and exercise fallbacks.

-- -------------------------------------------------------------
-- Seed Movement Templates
-- -------------------------------------------------------------

INSERT INTO movement_templates (name, sport_id, athlete_role, training_goal) VALUES
(
    'Lower Body Power', 
    (SELECT id FROM sports WHERE name = 'American Football'), 
    'All', 
    'Develop rate of force development (RFD), explosive triple extension, and maximal power in the lower body.'
),
(
    'Acceleration Development', 
    (SELECT id FROM sports WHERE name = 'Track & Field (Sprinting)'), 
    'Sprinters', 
    'Enhance horizontal force application, landing stiffness, and initial drive phase mechanics.'
),
(
    'Rotational Power', 
    (SELECT id FROM sports WHERE name = 'Track & Field (Throws)'), 
    'Throwers', 
    'Maximize hip-shoulder separation, rotational velocity, and force transfer through the kinetic chain.'
),
(
    'Shoulder Robustness', 
    (SELECT id FROM sports WHERE name = 'Rugby'), 
    'All', 
    'Enhance glenohumeral stability, scapular control, and rotator cuff capacity to reduce injury risk in contact sports.'
),
(
    'Reactive Agility', 
    (SELECT id FROM sports WHERE name = 'Basketball'), 
    'Guards/Forwards', 
    'Improve landing mechanics, decelerative capacity, and stretch-shortening cycle (SSC) efficiency during direction changes.'
);

-- -------------------------------------------------------------
-- Seed Template Slots
-- -------------------------------------------------------------

-- Slots for: Lower Body Power
INSERT INTO template_slots (template_id, slot_type, name, display_order, notes) VALUES
((SELECT id FROM movement_templates WHERE name = 'Lower Body Power'), 'Primary', 'Bilateral Power/Strength Lift', 1, 'Heavy compound lift tracking bar speed if possible.'),
((SELECT id FROM movement_templates WHERE name = 'Lower Body Power'), 'Secondary', 'Unilateral Power/Stability', 2, 'Focus on unilateral hip stability and velocity.'),
((SELECT id FROM movement_templates WHERE name = 'Lower Body Power'), 'Accessory', 'Posterior Chain Force Production', 3, 'Target glute/hamstring extension velocity.'),
((SELECT id FROM movement_templates WHERE name = 'Lower Body Power'), 'Core', 'Rotational Trunk Power', 4, 'Transfer lower body force through the torso.');

-- Slots for: Acceleration Development
INSERT INTO template_slots (template_id, slot_type, name, display_order, notes) VALUES
((SELECT id FROM movement_templates WHERE name = 'Acceleration Development'), 'Primary', 'Explosive Hinge/Extension', 1, 'Olympic pull or high-velocity hinge to train hip drive.'),
((SELECT id FROM movement_templates WHERE name = 'Acceleration Development'), 'Secondary', 'Unilateral Drive Strength', 2, 'Build single-leg strength matching sprint posture.'),
((SELECT id FROM movement_templates WHERE name = 'Acceleration Development'), 'Accessory', 'Posterior Chain Knee Flexion', 3, 'Isolate hamstrings for injury reduction during sprinting.'),
((SELECT id FROM movement_templates WHERE name = 'Acceleration Development'), 'Core', 'Trunk Stability in Motion', 4, 'Resist trunk collapse and rotation during stride.');

-- Slots for: Rotational Power
INSERT INTO template_slots (template_id, slot_type, name, display_order, notes) VALUES
((SELECT id FROM movement_templates WHERE name = 'Rotational Power'), 'Primary', 'Rotational Power Slam', 1, 'Explosive medicine ball throws simulating throwing mechanics.'),
((SELECT id FROM movement_templates WHERE name = 'Rotational Power'), 'Secondary', 'Base Strength Lift', 2, 'Heavy pull to build foundational absolute strength.'),
((SELECT id FROM movement_templates WHERE name = 'Rotational Power'), 'Accessory', 'Unilateral Push Strength', 3, 'Support rotational torque with unilateral shoulder press.'),
((SELECT id FROM movement_templates WHERE name = 'Rotational Power'), 'Core', 'Anti-Rotation Stiffness', 4, 'Build isometric torso rigidity to transfer hip power.');

-- Slots for: Shoulder Robustness
INSERT INTO template_slots (template_id, slot_type, name, display_order, notes) VALUES
((SELECT id FROM movement_templates WHERE name = 'Shoulder Robustness'), 'Primary', 'Overhead Push Stability', 1, 'Overhead work developing scapular control and strength.'),
((SELECT id FROM movement_templates WHERE name = 'Shoulder Robustness'), 'Secondary', 'Scapular Pull Strength', 2, 'Unilateral/bilateral rows balancing the upper back.'),
((SELECT id FROM movement_templates WHERE name = 'Shoulder Robustness'), 'Accessory', 'Rotator Cuff & Posterior Shoulder', 3, 'High rep control isolating shoulder stabilizers.'),
((SELECT id FROM movement_templates WHERE name = 'Shoulder Robustness'), 'Core', 'Anti-Extension Core', 4, 'Resist lumbar hyperextension during overhead bracing.');

-- Slots for: Reactive Agility
INSERT INTO template_slots (template_id, slot_type, name, display_order, notes) VALUES
((SELECT id FROM movement_templates WHERE name = 'Reactive Agility'), 'Primary', 'Reactive Force Absorption', 1, 'Fast plyometrics focusing on minimal ground contact times.'),
((SELECT id FROM movement_templates WHERE name = 'Reactive Agility'), 'Secondary', 'Unilateral Deceleration Strength', 2, 'Single-leg controls focusing on braking/landing mechanics.'),
((SELECT id FROM movement_templates WHERE name = 'Reactive Agility'), 'Accessory', 'Lateral Force Production', 3, 'Slide or lateral push movements for side-to-side power.'),
((SELECT id FROM movement_templates WHERE name = 'Reactive Agility'), 'Core', 'Anti-Rotation Core Control', 4, 'Bracing the pelvis against rotational forces.');

-- -------------------------------------------------------------
-- Seed Slot Requirements (Exercise Matching Constraints)
-- -------------------------------------------------------------

-- Requirements for: Lower Body Power
INSERT INTO slot_requirements (slot_id, movement_pattern_id, physical_quality_id, training_method_id, equipment_id, difficulty_level, min_relevance_score, min_specificity_rating) VALUES
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Lower Body Power' AND ts.display_order = 1),
    (SELECT id FROM movement_patterns WHERE name = 'Squat'),
    (SELECT id FROM physical_qualities WHERE name = 'Rate of Force Development'),
    (SELECT id FROM training_methods WHERE name = 'Velocity-Based Training'),
    (SELECT id FROM equipment WHERE name = 'Barbell'),
    'Intermediate', 7, 7
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Lower Body Power' AND ts.display_order = 2),
    (SELECT id FROM movement_patterns WHERE name = 'Lunge (Single-Leg)'),
    (SELECT id FROM physical_qualities WHERE name = 'Stability'),
    NULL,
    (SELECT id FROM equipment WHERE name = 'Dumbbell'),
    'Intermediate', 6, 6
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Lower Body Power' AND ts.display_order = 3),
    (SELECT id FROM movement_patterns WHERE name = 'Hinge'),
    (SELECT id FROM physical_qualities WHERE name = 'Rate of Force Development'),
    (SELECT id FROM training_methods WHERE name = 'Contrast Training'),
    (SELECT id FROM equipment WHERE name = 'Kettlebell'),
    'Beginner', 6, 5
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Lower Body Power' AND ts.display_order = 4),
    (SELECT id FROM movement_patterns WHERE name = 'Rotation'),
    (SELECT id FROM physical_qualities WHERE name = 'Rate of Force Development'),
    NULL,
    (SELECT id FROM equipment WHERE name = 'Medicine Ball'),
    'Beginner', 7, 7
);

-- Requirements for: Acceleration Development
INSERT INTO slot_requirements (slot_id, movement_pattern_id, physical_quality_id, training_method_id, equipment_id, difficulty_level, min_relevance_score, min_specificity_rating) VALUES
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Acceleration Development' AND ts.display_order = 1),
    (SELECT id FROM movement_patterns WHERE name = 'Hinge'),
    (SELECT id FROM physical_qualities WHERE name = 'Rate of Force Development'),
    (SELECT id FROM training_methods WHERE name = 'Velocity-Based Training'),
    (SELECT id FROM equipment WHERE name = 'Barbell'),
    'Advanced', 8, 8
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Acceleration Development' AND ts.display_order = 2),
    (SELECT id FROM movement_patterns WHERE name = 'Lunge (Single-Leg)'),
    (SELECT id FROM physical_qualities WHERE name = 'Maximal Strength'),
    NULL,
    (SELECT id FROM equipment WHERE name = 'Dumbbell'),
    'Intermediate', 7, 7
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Acceleration Development' AND ts.display_order = 3),
    (SELECT id FROM movement_patterns WHERE name = 'Hinge'),
    (SELECT id FROM physical_qualities WHERE name = 'Maximal Strength'),
    (SELECT id FROM training_methods WHERE name = 'Eccentric Overload'),
    (SELECT id FROM equipment WHERE name = 'Bodyweight'),
    'Advanced', 8, 8
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Acceleration Development' AND ts.display_order = 4),
    (SELECT id FROM movement_patterns WHERE name = 'Anti-Rotation'),
    (SELECT id FROM physical_qualities WHERE name = 'Stability'),
    NULL,
    (SELECT id FROM equipment WHERE name = 'Resistance Bands'),
    'Beginner', 6, 6
);

-- Requirements for: Rotational Power
INSERT INTO slot_requirements (slot_id, movement_pattern_id, physical_quality_id, training_method_id, equipment_id, difficulty_level, min_relevance_score, min_specificity_rating) VALUES
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Rotational Power' AND ts.display_order = 1),
    (SELECT id FROM movement_patterns WHERE name = 'Rotation'),
    (SELECT id FROM physical_qualities WHERE name = 'Rate of Force Development'),
    (SELECT id FROM training_methods WHERE name = 'Plyometric (Slow)'),
    (SELECT id FROM equipment WHERE name = 'Medicine Ball'),
    'Beginner', 8, 8
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Rotational Power' AND ts.display_order = 2),
    (SELECT id FROM movement_patterns WHERE name = 'Hinge'),
    (SELECT id FROM physical_qualities WHERE name = 'Maximal Strength'),
    (SELECT id FROM training_methods WHERE name = 'Cluster Sets'),
    (SELECT id FROM equipment WHERE name = 'Trap Bar'),
    'Intermediate', 9, 8
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Rotational Power' AND ts.display_order = 3),
    (SELECT id FROM movement_patterns WHERE name = 'Push (Horizontal)'),
    (SELECT id FROM physical_qualities WHERE name = 'Hypertrophy'),
    NULL,
    (SELECT id FROM equipment WHERE name = 'Dumbbell'),
    'Intermediate', 5, 5
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Rotational Power' AND ts.display_order = 4),
    (SELECT id FROM movement_patterns WHERE name = 'Anti-Rotation'),
    (SELECT id FROM physical_qualities WHERE name = 'Stability'),
    NULL,
    (SELECT id FROM equipment WHERE name = 'Cable Machine'),
    'Beginner', 7, 7
);

-- Requirements for: Shoulder Robustness
INSERT INTO slot_requirements (slot_id, movement_pattern_id, physical_quality_id, training_method_id, equipment_id, difficulty_level, min_relevance_score, min_specificity_rating) VALUES
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Shoulder Robustness' AND ts.display_order = 1),
    (SELECT id FROM movement_patterns WHERE name = 'Push (Vertical)'),
    (SELECT id FROM physical_qualities WHERE name = 'Stability'),
    NULL,
    (SELECT id FROM equipment WHERE name = 'Barbell'),
    'Intermediate', 7, 6
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Shoulder Robustness' AND ts.display_order = 2),
    (SELECT id FROM movement_patterns WHERE name = 'Pull (Horizontal)'),
    (SELECT id FROM physical_qualities WHERE name = 'Stability'),
    NULL,
    (SELECT id FROM equipment WHERE name = 'Cable Machine'),
    'Intermediate', 7, 7
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Shoulder Robustness' AND ts.display_order = 3),
    (SELECT id FROM movement_patterns WHERE name = 'Rotation'),
    (SELECT id FROM physical_qualities WHERE name = 'Local Muscular Endurance'),
    NULL,
    (SELECT id FROM equipment WHERE name = 'Resistance Bands'),
    'Beginner', 6, 6
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Shoulder Robustness' AND ts.display_order = 4),
    (SELECT id FROM movement_patterns WHERE name = 'Anti-Rotation'),
    (SELECT id FROM physical_qualities WHERE name = 'Stability'),
    NULL,
    (SELECT id FROM equipment WHERE name = 'Bodyweight'),
    'Beginner', 7, 6
);

-- Requirements for: Reactive Agility
INSERT INTO slot_requirements (slot_id, movement_pattern_id, physical_quality_id, training_method_id, equipment_id, difficulty_level, min_relevance_score, min_specificity_rating) VALUES
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Reactive Agility' AND ts.display_order = 1),
    (SELECT id FROM movement_patterns WHERE name = 'Squat'),
    (SELECT id FROM physical_qualities WHERE name = 'Rate of Force Development'),
    (SELECT id FROM training_methods WHERE name = 'Plyometric (Fast)'),
    (SELECT id FROM equipment WHERE name = 'Bodyweight'),
    'Elite', 9, 9
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Reactive Agility' AND ts.display_order = 2),
    (SELECT id FROM movement_patterns WHERE name = 'Lunge (Single-Leg)'),
    (SELECT id FROM physical_qualities WHERE name = 'Stability'),
    NULL,
    (SELECT id FROM equipment WHERE name = 'Kettlebell'),
    'Intermediate', 7, 7
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Reactive Agility' AND ts.display_order = 3),
    (SELECT id FROM movement_patterns WHERE name = 'Push (Horizontal)'),
    (SELECT id FROM physical_qualities WHERE name = 'Rate of Force Development'),
    NULL,
    (SELECT id FROM equipment WHERE name = 'Slide Board'),
    'Intermediate', 6, 6
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Reactive Agility' AND ts.display_order = 4),
    (SELECT id FROM movement_patterns WHERE name = 'Anti-Rotation'),
    (SELECT id FROM physical_qualities WHERE name = 'Stability'),
    NULL,
    (SELECT id FROM equipment WHERE name = 'Cable Machine'),
    'Intermediate', 7, 7
);

-- -------------------------------------------------------------
-- Seed Slot Progressions
-- -------------------------------------------------------------

-- Progressions for: Lower Body Power
INSERT INTO slot_progressions (slot_id, progression_type, intensity_target, volume_target, progression_rule, deload_protocol) VALUES
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Lower Body Power' AND ts.display_order = 1),
    'Velocity-Based', '0.75-0.85 m/s', '4x3', 
    'Monitor velocity of first rep. If velocity > 0.85 m/s, increase load by 5-10 lbs. If velocity < 0.75 m/s, reduce load.', 
    'Perform 2 sets of 3 reps at 60% of current training load.'
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Lower Body Power' AND ts.display_order = 2),
    'Double Progression', 'RPE 8', '3x5 each leg', 
    'Maintain weight and attempt to add 1 rep per set each week. Once 3 sets of 7 reps are completed at RPE 8, increase weight by 5 lbs and reset volume to 3x5.', 
    'Reduce volume to 2 sets of 5 reps at the current weight.'
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Lower Body Power' AND ts.display_order = 3),
    'Linear Load', 'RPE 7-8', '3x10', 
    'Add 5 lbs weekly if all reps are completed under control with flat back.', 
    'Reduce volume by 50% (3 sets of 5 reps) and keep intensity constant.'
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Lower Body Power' AND ts.display_order = 4),
    'Qualitative/Technique', 'Max Velocity', '3x6 each side', 
    'Maintain high explosive execution. Increase ball weight by 2 lbs only if triple extension velocity is preserved.', 
    'Decrease reps to 3 per side, focusing on maximum speed and rest periods.'
);

-- Progressions for: Acceleration Development
INSERT INTO slot_progressions (slot_id, progression_type, intensity_target, volume_target, progression_rule, deload_protocol) VALUES
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Acceleration Development' AND ts.display_order = 1),
    'Velocity-Based', '0.90-1.00 m/s', '5x2',
    'Load is adjusted to maintain speed. If velocity exceeds 1.00 m/s, add 5 lbs. If it drops below 0.90 m/s, strip weight.',
    'Drop sets to 3, intensity to 50% load.'
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Acceleration Development' AND ts.display_order = 2),
    'Double Progression', 'RPE 8-9', '3x6 each leg',
    'Increase load by 5-10 lbs when all sets are completed for 6 reps with clean posture.',
    'Reduce load by 15%, preserve set/rep structure.'
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Acceleration Development' AND ts.display_order = 3),
    'Qualitative/Technique', '5s eccentric', '3x4-6',
    'Increase reps from 4 to 6. Focus on slowing down the eccentric phase. Add manual load once 6 reps with 5s eccentric can be done.',
    'Reduce sets to 2, drop eccentric duration to 3s.'
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Acceleration Development' AND ts.display_order = 4),
    'Qualitative/Technique', 'RPE 7', '3x10s hold',
    'Increase hold time by 5s each session up to 20s. Once achieved, increase band tension and drop time back to 10s.',
    'Reduce duration of holds to 5s, preserve sets.'
);

-- Progressions for: Rotational Power
INSERT INTO slot_progressions (slot_id, progression_type, intensity_target, volume_target, progression_rule, deload_protocol) VALUES
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Rotational Power' AND ts.display_order = 1),
    'Qualitative/Technique', 'Max Velocity', '4x6',
    'Add medicine ball weight only if throwing velocity remains explosive.',
    'Reduce sets to 2, focus on maximum execution velocity.'
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Rotational Power' AND ts.display_order = 2),
    'RPE-Based', 'RPE 8-9', '4x(2+2) [20s rest]',
    'Add 10 lbs when all cluster reps are executed below RPE 9.',
    'Drop to 2 sets, decrease intensity to RPE 6.'
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Rotational Power' AND ts.display_order = 3),
    'Linear Load', 'RPE 8', '3x8-10',
    'Add 2.5 lbs per dumbbell weekly if all reps are executed under control.',
    'Reduce volume by 50%.'
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Rotational Power' AND ts.display_order = 4),
    'Linear Load', 'RPE 8', '3x8 each side',
    'Increase stack load by 1 plate once all reps can be completed with minimal hip rotation.',
    'Keep resistance constant, reduce reps to 4 per side.'
);

-- Progressions for: Shoulder Robustness
INSERT INTO slot_progressions (slot_id, progression_type, intensity_target, volume_target, progression_rule, deload_protocol) VALUES
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Shoulder Robustness' AND ts.display_order = 1),
    'Linear Load', '70% 1RM / RPE 7-8', '3x8',
    'Increase load by 5 lbs once 3 sets of 8 are completed with clean shoulder mechanics.',
    'Reduce intensity by 10% and sets to 2.'
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Shoulder Robustness' AND ts.display_order = 2),
    'Double Progression', 'RPE 8', '3x10-12',
    'Progress reps to 12. Once achieved on all sets, increase load and drop reps back to 10.',
    'Keep weight, reduce reps to 8.'
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Shoulder Robustness' AND ts.display_order = 3),
    'Qualitative/Technique', 'RPE 6-7', '3x15',
    'Focus on control and tempo (2s concentric, 2s eccentric). Increase band thickness once tempo is held.',
    'Perform 2 sets of 10 reps, focusing on stability.'
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Shoulder Robustness' AND ts.display_order = 4),
    'RPE-Based', 'RPE 8', '3x30s',
    'Increase hold time by 5s per workout until 45s is reached, then add resistance (e.g. weight plate on back).',
    'Reduce hold times to 15s.'
);

-- Progressions for: Reactive Agility
INSERT INTO slot_progressions (slot_id, progression_type, intensity_target, volume_target, progression_rule, deload_protocol) VALUES
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Reactive Agility' AND ts.display_order = 1),
    'Qualitative/Technique', 'Ground < 200ms', '4x4',
    'Increase drop height of box by 2 inches only if ground contact time remains under 200ms.',
    'Reduce drop height by 6 inches, decrease reps to 2 per set.'
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Reactive Agility' AND ts.display_order = 2),
    'Double Progression', 'RPE 8', '3x6 each leg',
    'Increase weight by 5 lbs when all sets can be controlled with perfect balance and alignment.',
    'Perform bodyweight only landing stabilization sets.'
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Reactive Agility' AND ts.display_order = 3),
    'Qualitative/Technique', 'Max Power', '3x30s',
    'Maintain low hip position. Increase velocity of slides to increase power output.',
    'Reduce duration to 15s at light pace.'
),
(
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Reactive Agility' AND ts.display_order = 4),
    'RPE-Based', 'RPE 8', '3x10',
    'Increase load by one plate when posture remains fully rigid without hip shift.',
    'Reduce stack load by 30%.'
);

-- -------------------------------------------------------------
-- Seed Sample Exercise Fallbacks (Static Substitution Rules)
-- -------------------------------------------------------------

INSERT INTO slot_exercise_fallbacks (slot_id, preferred_exercise_id, fallback_exercise_id, preference_rank) VALUES
(
    -- Barbell Back Squat -> Trap Bar Deadlift in Lower Body Power Primary Slot
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Lower Body Power' AND ts.display_order = 1),
    (SELECT id FROM exercises WHERE name = 'Barbell Back Squat'),
    (SELECT id FROM exercises WHERE name = 'Trap Bar Deadlift'),
    1
),
(
    -- Power Clean -> Kettlebell Swing in Acceleration Development Primary Slot
    (SELECT ts.id FROM template_slots ts JOIN movement_templates mt ON ts.template_id = mt.id WHERE mt.name = 'Acceleration Development' AND ts.display_order = 1),
    (SELECT id FROM exercises WHERE name = 'Power Clean'),
    (SELECT id FROM exercises WHERE name = 'Kettlebell Swing'),
    1
);
