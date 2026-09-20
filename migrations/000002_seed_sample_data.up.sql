-- Forge Exercise Intelligence Database - Migration 000002 (Up)
-- Description: Seed lookup tables and sample exercises with complete mappings.

-- -------------------------------------------------------------
-- Seed Lookup Tables
-- -------------------------------------------------------------

-- Seed Equipment
INSERT INTO equipment (name, category, description) VALUES
('Barbell', 'Free Weights', 'Standard 20kg Olympic barbell'),
('Dumbbell', 'Free Weights', 'Standard hand-held dumbbells'),
('Kettlebell', 'Free Weights', 'Traditional cast iron or competition kettlebells'),
('Trap Bar', 'Free Weights', 'Hexagonal barbell designed for deadlifting and neutral-grip work'),
('Cable Machine', 'Cables', 'Pulley systems with variable attachments'),
('Resistance Bands', 'Bands/Chains', 'Elastic latex bands providing progressive resistance'),
('Medicine Ball', 'Specialty/Accessory', 'Weighted balls used for explosive throwing and core work'),
('Bodyweight', 'Bodyweight', 'No external resistance required besides gravity'),
('Foam Roller', 'Specialty/Accessory', 'High-density foam cylinder for self-myofascial release'),
('Slide Board', 'Specialty/Accessory', 'Low-friction surface for lateral sliding movements');

-- Seed Movement Patterns
INSERT INTO movement_patterns (name, description) VALUES
('Squat', 'Bilateral or unilateral knee-dominant deep flexion and extension'),
('Hinge', 'Hip-dominant flexion and extension with minimal knee travel'),
('Push (Horizontal)', 'Pressing resistance away from the chest in the horizontal plane'),
('Push (Vertical)', 'Pressing resistance overhead in the vertical plane'),
('Pull (Horizontal)', 'Pulling resistance toward the torso in the horizontal plane'),
('Pull (Vertical)', 'Pulling resistance down toward the shoulders in the vertical plane'),
('Lunge (Single-Leg)', 'Asymmetric lower body stance isolating one limb at a time'),
('Carry', 'Locomotion under loaded conditions to build structural integrity'),
('Rotation', 'Force generation in the transverse plane around a vertical axis'),
('Anti-Rotation', 'Isometric resistance to rotation in the transverse plane');

-- Seed Physical Qualities
INSERT INTO physical_qualities (name, description) VALUES
('Maximal Strength', 'The maximum amount of force a muscle or muscle group can generate'),
('Rate of Force Development', 'The speed at which force can be produced (explosive power)'),
('Hypertrophy', 'Muscular enlargement and structural remodeling'),
('Aerobic Capacity', 'Efficiency of cardiorespiratory energy systems during long durations'),
('Anaerobic Power', 'High-intensity energy production during short, intense bursts'),
('Local Muscular Endurance', 'Ability of muscles to sustain repeated contractions against submaximal load'),
('Mobility', 'Active range of motion about a joint system'),
('Stability', 'Ability to maintain joint alignment and control under loaded or dynamic states');

-- Seed Training Methods
INSERT INTO training_methods (name, description) VALUES
('Concentric-Only', 'Focus on the shortening phase of contraction, minimizing eccentric load'),
('Eccentric Overload', 'Loading the lengthening phase of contraction beyond concentric capacity'),
('Isometric (Yielding)', 'Holding a static position and resisting gravity/collapse'),
('Isometric (Overcoming)', 'Pushing/pulling against an immovable object with maximum effort'),
('Plyometric (Fast)', 'Ground contact times under 250ms leveraging the stretch-shortening cycle'),
('Plyometric (Slow)', 'Ground contact times over 250ms (countermovement jumps, etc.)'),
('Velocity-Based Training', 'Adjusting loading based on real-time bar velocity monitoring'),
('Cluster Sets', 'Intra-set rest periods (e.g., 10-15s) between reps to maintain power output'),
('Contrast Training', 'Pairing a heavy strength movement with an explosive biomechanically similar movement');

-- Seed Sports
INSERT INTO sports (name, category, description) VALUES
('American Football', 'Team Sports', 'Requires high power, speed, agility, and absolute strength'),
('Basketball', 'Team Sports', 'Requires high vertical jump capacity, lateral agility, and aerobic/anaerobic repeat sprint capacity'),
('Soccer', 'Team Sports', 'Requires multi-directional speed, endurance, and decelerative capacity'),
('Olympic Weightlifting', 'Strength Sports', 'Requires extreme explosive power, mobility, speed, and precision'),
('Powerlifting', 'Strength Sports', 'Requires absolute maximal strength in Squat, Bench Press, and Deadlift'),
('Track & Field (Sprinting)', 'Individual Sports', 'Requires maximum rate of force development, acceleration, and top-end speed'),
('Track & Field (Throws)', 'Individual Sports', 'Requires extreme rotational power, absolute strength, and coordination'),
('Rugby', 'Team Sports', 'Requires contact-specific strength, power, and continuous aerobic/anaerobic capacity');

-- Seed Tags
INSERT INTO tags (name) VALUES
('Primary Lift'),
('Accessory'),
('Warm-up'),
('Rehab'),
('Unilateral'),
('Bilateral'),
('Posterior Chain'),
('Anterior Chain'),
('Explosive');

-- -------------------------------------------------------------
-- Seed Core Exercises
-- -------------------------------------------------------------

INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type) VALUES
('Barbell Back Squat', 'Place a barbell on the upper back (trapezius), descend by bending the hips and knees until thighs are parallel or below, then return to the starting position.', 'Intermediate', 'Compound', 'Push'),
('Power Clean', 'Pull a barbell dynamically from the floor to the shoulders, catching it in a quarter-squat position. Key for developing explosive power.', 'Advanced', 'Compound', 'Pull'),
('Rear Foot Elevated Split Squat', 'Stand with one foot resting behind on a bench or box. Hold weights and descend by bending the front knee, focusing on quad and glute development.', 'Intermediate', 'Compound', 'Push'),
('Trap Bar Deadlift', 'Step inside the hex bar, grip the handles, and lift by extending the hips and knees, keeping a flat back. Highly versatile strength movement.', 'Intermediate', 'Compound', 'Hinge'),
('Kettlebell Swing', 'Swing a kettlebell from between the legs to shoulder height, driving the movement through explosive hip extension.', 'Beginner', 'Compound', 'Hinge'),
('Depth Jump', 'Step off a box, land on the ground, and immediately jump as high as possible, minimizing ground contact time to train reactive strength.', 'Elite', 'Compound', 'Push'),
('Medicine Ball Rotational Scoop Toss', 'Throw a medicine ball forcefully sideways against a wall, utilizing the hips and core to generate rotational power.', 'Beginner', 'Compound', 'Static'),
('A-Skip', 'A coordination and warm-up drill involving high knees and a skipping rhythm to train sprint mechanics.', 'Beginner', 'Compound', 'N/A'),
('Single-Leg Isometric Wall Sit', 'Hold a wall sit position on a single leg, training quadriceps endurance and patellar tendon adaptation.', 'Intermediate', 'Isolation', 'Static'),
('Nordic Hamstring Curl', 'Kneel with ankles secured, lower the torso slowly toward the floor using the hamstrings to resist gravity, then push back up.', 'Advanced', 'Isolation', 'Pull');

-- -------------------------------------------------------------
-- Seed Many-to-Many Mappings (Using Subqueries/CTEs)
-- -------------------------------------------------------------

-- 1. Exercise <-> Equipment Mappings
INSERT INTO exercise_equipment (exercise_id, equipment_id, is_required) VALUES
((SELECT id FROM exercises WHERE name = 'Barbell Back Squat'), (SELECT id FROM equipment WHERE name = 'Barbell'), TRUE),
((SELECT id FROM exercises WHERE name = 'Power Clean'), (SELECT id FROM equipment WHERE name = 'Barbell'), TRUE),
((SELECT id FROM exercises WHERE name = 'Rear Foot Elevated Split Squat'), (SELECT id FROM equipment WHERE name = 'Dumbbell'), FALSE),
((SELECT id FROM exercises WHERE name = 'Rear Foot Elevated Split Squat'), (SELECT id FROM equipment WHERE name = 'Bodyweight'), TRUE),
((SELECT id FROM exercises WHERE name = 'Trap Bar Deadlift'), (SELECT id FROM equipment WHERE name = 'Trap Bar'), TRUE),
((SELECT id FROM exercises WHERE name = 'Kettlebell Swing'), (SELECT id FROM equipment WHERE name = 'Kettlebell'), TRUE),
((SELECT id FROM exercises WHERE name = 'Depth Jump'), (SELECT id FROM equipment WHERE name = 'Bodyweight'), TRUE),
((SELECT id FROM exercises WHERE name = 'Medicine Ball Rotational Scoop Toss'), (SELECT id FROM equipment WHERE name = 'Medicine Ball'), TRUE),
((SELECT id FROM exercises WHERE name = 'A-Skip'), (SELECT id FROM equipment WHERE name = 'Bodyweight'), TRUE),
((SELECT id FROM exercises WHERE name = 'Single-Leg Isometric Wall Sit'), (SELECT id FROM equipment WHERE name = 'Bodyweight'), TRUE),
((SELECT id FROM exercises WHERE name = 'Nordic Hamstring Curl'), (SELECT id FROM equipment WHERE name = 'Bodyweight'), TRUE);

-- 2. Exercise <-> Movement Pattern Mappings
INSERT INTO exercise_movement_patterns (exercise_id, movement_pattern_id, pattern_priority) VALUES
((SELECT id FROM exercises WHERE name = 'Barbell Back Squat'), (SELECT id FROM movement_patterns WHERE name = 'Squat'), 'Primary'),
((SELECT id FROM exercises WHERE name = 'Power Clean'), (SELECT id FROM movement_patterns WHERE name = 'Hinge'), 'Primary'),
((SELECT id FROM exercises WHERE name = 'Power Clean'), (SELECT id FROM movement_patterns WHERE name = 'Squat'), 'Secondary'),
((SELECT id FROM exercises WHERE name = 'Rear Foot Elevated Split Squat'), (SELECT id FROM movement_patterns WHERE name = 'Lunge (Single-Leg)'), 'Primary'),
((SELECT id FROM exercises WHERE name = 'Trap Bar Deadlift'), (SELECT id FROM movement_patterns WHERE name = 'Hinge'), 'Primary'),
((SELECT id FROM exercises WHERE name = 'Trap Bar Deadlift'), (SELECT id FROM movement_patterns WHERE name = 'Squat'), 'Secondary'),
((SELECT id FROM exercises WHERE name = 'Kettlebell Swing'), (SELECT id FROM movement_patterns WHERE name = 'Hinge'), 'Primary'),
((SELECT id FROM exercises WHERE name = 'Depth Jump'), (SELECT id FROM movement_patterns WHERE name = 'Squat'), 'Primary'),
((SELECT id FROM exercises WHERE name = 'Medicine Ball Rotational Scoop Toss'), (SELECT id FROM movement_patterns WHERE name = 'Rotation'), 'Primary'),
((SELECT id FROM exercises WHERE name = 'A-Skip'), (SELECT id FROM movement_patterns WHERE name = 'Lunge (Single-Leg)'), 'Primary'),
((SELECT id FROM exercises WHERE name = 'Single-Leg Isometric Wall Sit'), (SELECT id FROM movement_patterns WHERE name = 'Squat'), 'Primary'),
((SELECT id FROM exercises WHERE name = 'Nordic Hamstring Curl'), (SELECT id FROM movement_patterns WHERE name = 'Hinge'), 'Primary');

-- 3. Exercise <-> Physical Quality Mappings (with Relevance Score)
INSERT INTO exercise_physical_qualities (exercise_id, physical_quality_id, relevance_score) VALUES
((SELECT id FROM exercises WHERE name = 'Barbell Back Squat'), (SELECT id FROM physical_qualities WHERE name = 'Maximal Strength'), 10),
((SELECT id FROM exercises WHERE name = 'Barbell Back Squat'), (SELECT id FROM physical_qualities WHERE name = 'Hypertrophy'), 8),
((SELECT id FROM exercises WHERE name = 'Barbell Back Squat'), (SELECT id FROM physical_qualities WHERE name = 'Rate of Force Development'), 6),
((SELECT id FROM exercises WHERE name = 'Power Clean'), (SELECT id FROM physical_qualities WHERE name = 'Rate of Force Development'), 10),
((SELECT id FROM exercises WHERE name = 'Power Clean'), (SELECT id FROM physical_qualities WHERE name = 'Maximal Strength'), 8),
((SELECT id FROM exercises WHERE name = 'Rear Foot Elevated Split Squat'), (SELECT id FROM physical_qualities WHERE name = 'Maximal Strength'), 8),
((SELECT id FROM exercises WHERE name = 'Rear Foot Elevated Split Squat'), (SELECT id FROM physical_qualities WHERE name = 'Hypertrophy'), 8),
((SELECT id FROM exercises WHERE name = 'Rear Foot Elevated Split Squat'), (SELECT id FROM physical_qualities WHERE name = 'Stability'), 9),
((SELECT id FROM exercises WHERE name = 'Trap Bar Deadlift'), (SELECT id FROM physical_qualities WHERE name = 'Maximal Strength'), 10),
((SELECT id FROM exercises WHERE name = 'Trap Bar Deadlift'), (SELECT id FROM physical_qualities WHERE name = 'Rate of Force Development'), 8),
((SELECT id FROM exercises WHERE name = 'Kettlebell Swing'), (SELECT id FROM physical_qualities WHERE name = 'Rate of Force Development'), 8),
((SELECT id FROM exercises WHERE name = 'Kettlebell Swing'), (SELECT id FROM physical_qualities WHERE name = 'Local Muscular Endurance'), 6),
((SELECT id FROM exercises WHERE name = 'Depth Jump'), (SELECT id FROM physical_qualities WHERE name = 'Rate of Force Development'), 10),
((SELECT id FROM exercises WHERE name = 'Medicine Ball Rotational Scoop Toss'), (SELECT id FROM physical_qualities WHERE name = 'Rate of Force Development'), 9),
((SELECT id FROM exercises WHERE name = 'Medicine Ball Rotational Scoop Toss'), (SELECT id FROM physical_qualities WHERE name = 'Stability'), 7),
((SELECT id FROM exercises WHERE name = 'A-Skip'), (SELECT id FROM physical_qualities WHERE name = 'Stability'), 8),
((SELECT id FROM exercises WHERE name = 'Single-Leg Isometric Wall Sit'), (SELECT id FROM physical_qualities WHERE name = 'Stability'), 9),
((SELECT id FROM exercises WHERE name = 'Single-Leg Isometric Wall Sit'), (SELECT id FROM physical_qualities WHERE name = 'Local Muscular Endurance'), 8),
((SELECT id FROM exercises WHERE name = 'Nordic Hamstring Curl'), (SELECT id FROM physical_qualities WHERE name = 'Maximal Strength'), 9),
((SELECT id FROM exercises WHERE name = 'Nordic Hamstring Curl'), (SELECT id FROM physical_qualities WHERE name = 'Hypertrophy'), 8);

-- 4. Exercise <-> Training Method Mappings
INSERT INTO exercise_training_methods (exercise_id, training_method_id) VALUES
((SELECT id FROM exercises WHERE name = 'Barbell Back Squat'), (SELECT id FROM training_methods WHERE name = 'Velocity-Based Training')),
((SELECT id FROM exercises WHERE name = 'Barbell Back Squat'), (SELECT id FROM training_methods WHERE name = 'Cluster Sets')),
((SELECT id FROM exercises WHERE name = 'Power Clean'), (SELECT id FROM training_methods WHERE name = 'Velocity-Based Training')),
((SELECT id FROM exercises WHERE name = 'Rear Foot Elevated Split Squat'), (SELECT id FROM training_methods WHERE name = 'Contrast Training')),
((SELECT id FROM exercises WHERE name = 'Trap Bar Deadlift'), (SELECT id FROM training_methods WHERE name = 'Velocity-Based Training')),
((SELECT id FROM exercises WHERE name = 'Trap Bar Deadlift'), (SELECT id FROM training_methods WHERE name = 'Cluster Sets')),
((SELECT id FROM exercises WHERE name = 'Kettlebell Swing'), (SELECT id FROM training_methods WHERE name = 'Contrast Training')),
((SELECT id FROM exercises WHERE name = 'Depth Jump'), (SELECT id FROM training_methods WHERE name = 'Plyometric (Fast)')),
((SELECT id FROM exercises WHERE name = 'Medicine Ball Rotational Scoop Toss'), (SELECT id FROM training_methods WHERE name = 'Plyometric (Slow)')),
((SELECT id FROM exercises WHERE name = 'A-Skip'), (SELECT id FROM training_methods WHERE name = 'Plyometric (Fast)')),
((SELECT id FROM exercises WHERE name = 'Single-Leg Isometric Wall Sit'), (SELECT id FROM training_methods WHERE name = 'Isometric (Yielding)')),
((SELECT id FROM exercises WHERE name = 'Nordic Hamstring Curl'), (SELECT id FROM training_methods WHERE name = 'Eccentric Overload'));

-- 5. Exercise <-> Sport Mappings (exercise_sport_mapping with Specificity Rating and Transfer Index)
INSERT INTO exercise_sport_mapping (exercise_id, sport_id, specificity_rating, transfer_index) VALUES
((SELECT id FROM exercises WHERE name = 'Barbell Back Squat'), (SELECT id FROM sports WHERE name = 'Powerlifting'), 10, 0.98),
((SELECT id FROM exercises WHERE name = 'Barbell Back Squat'), (SELECT id FROM sports WHERE name = 'American Football'), 8, 0.85),
((SELECT id FROM exercises WHERE name = 'Barbell Back Squat'), (SELECT id FROM sports WHERE name = 'Rugby'), 8, 0.82),
((SELECT id FROM exercises WHERE name = 'Barbell Back Squat'), (SELECT id FROM sports WHERE name = 'Track & Field (Sprinting)'), 7, 0.75),

((SELECT id FROM exercises WHERE name = 'Power Clean'), (SELECT id FROM sports WHERE name = 'Olympic Weightlifting'), 10, 1.00),
((SELECT id FROM exercises WHERE name = 'Power Clean'), (SELECT id FROM sports WHERE name = 'American Football'), 9, 0.92),
((SELECT id FROM exercises WHERE name = 'Power Clean'), (SELECT id FROM sports WHERE name = 'Rugby'), 9, 0.90),
((SELECT id FROM exercises WHERE name = 'Power Clean'), (SELECT id FROM sports WHERE name = 'Track & Field (Sprinting)'), 8, 0.88),

((SELECT id FROM exercises WHERE name = 'Rear Foot Elevated Split Squat'), (SELECT id FROM sports WHERE name = 'Basketball'), 9, 0.88),
((SELECT id FROM exercises WHERE name = 'Rear Foot Elevated Split Squat'), (SELECT id FROM sports WHERE name = 'Soccer'), 9, 0.85),
((SELECT id FROM exercises WHERE name = 'Rear Foot Elevated Split Squat'), (SELECT id FROM sports WHERE name = 'American Football'), 8, 0.80),

((SELECT id FROM exercises WHERE name = 'Trap Bar Deadlift'), (SELECT id FROM sports WHERE name = 'American Football'), 9, 0.88),
((SELECT id FROM exercises WHERE name = 'Trap Bar Deadlift'), (SELECT id FROM sports WHERE name = 'Rugby'), 9, 0.87),
((SELECT id FROM exercises WHERE name = 'Trap Bar Deadlift'), (SELECT id FROM sports WHERE name = 'Track & Field (Sprinting)'), 8, 0.82),

((SELECT id FROM exercises WHERE name = 'Kettlebell Swing'), (SELECT id FROM sports WHERE name = 'Track & Field (Throws)'), 8, 0.78),
((SELECT id FROM exercises WHERE name = 'Kettlebell Swing'), (SELECT id FROM sports WHERE name = 'American Football'), 7, 0.70),

((SELECT id FROM exercises WHERE name = 'Depth Jump'), (SELECT id FROM sports WHERE name = 'Basketball'), 10, 0.95),
((SELECT id FROM exercises WHERE name = 'Depth Jump'), (SELECT id FROM sports WHERE name = 'Track & Field (Sprinting)'), 10, 0.92),

((SELECT id FROM exercises WHERE name = 'Medicine Ball Rotational Scoop Toss'), (SELECT id FROM sports WHERE name = 'Track & Field (Throws)'), 9, 0.88),

((SELECT id FROM exercises WHERE name = 'A-Skip'), (SELECT id FROM sports WHERE name = 'Track & Field (Sprinting)'), 10, 0.95),
((SELECT id FROM exercises WHERE name = 'A-Skip'), (SELECT id FROM sports WHERE name = 'Soccer'), 8, 0.75),

((SELECT id FROM exercises WHERE name = 'Single-Leg Isometric Wall Sit'), (SELECT id FROM sports WHERE name = 'Basketball'), 8, 0.70),
((SELECT id FROM exercises WHERE name = 'Single-Leg Isometric Wall Sit'), (SELECT id FROM sports WHERE name = 'Soccer'), 8, 0.72),

((SELECT id FROM exercises WHERE name = 'Nordic Hamstring Curl'), (SELECT id FROM sports WHERE name = 'Soccer'), 10, 0.92),
((SELECT id FROM exercises WHERE name = 'Nordic Hamstring Curl'), (SELECT id FROM sports WHERE name = 'Track & Field (Sprinting)'), 10, 0.94),
((SELECT id FROM exercises WHERE name = 'Nordic Hamstring Curl'), (SELECT id FROM sports WHERE name = 'American Football'), 9, 0.88);

-- 6. Exercise <-> Tag Mappings
INSERT INTO exercise_tags (exercise_id, tag_id) VALUES
((SELECT id FROM exercises WHERE name = 'Barbell Back Squat'), (SELECT id FROM tags WHERE name = 'Primary Lift')),
((SELECT id FROM exercises WHERE name = 'Barbell Back Squat'), (SELECT id FROM tags WHERE name = 'Bilateral')),
((SELECT id FROM exercises WHERE name = 'Barbell Back Squat'), (SELECT id FROM tags WHERE name = 'Anterior Chain')),

((SELECT id FROM exercises WHERE name = 'Power Clean'), (SELECT id FROM tags WHERE name = 'Primary Lift')),
((SELECT id FROM exercises WHERE name = 'Power Clean'), (SELECT id FROM tags WHERE name = 'Bilateral')),
((SELECT id FROM exercises WHERE name = 'Power Clean'), (SELECT id FROM tags WHERE name = 'Posterior Chain')),
((SELECT id FROM exercises WHERE name = 'Power Clean'), (SELECT id FROM tags WHERE name = 'Explosive')),

((SELECT id FROM exercises WHERE name = 'Rear Foot Elevated Split Squat'), (SELECT id FROM tags WHERE name = 'Accessory')),
((SELECT id FROM exercises WHERE name = 'Rear Foot Elevated Split Squat'), (SELECT id FROM tags WHERE name = 'Unilateral')),
((SELECT id FROM exercises WHERE name = 'Rear Foot Elevated Split Squat'), (SELECT id FROM tags WHERE name = 'Anterior Chain')),

((SELECT id FROM exercises WHERE name = 'Trap Bar Deadlift'), (SELECT id FROM tags WHERE name = 'Primary Lift')),
((SELECT id FROM exercises WHERE name = 'Trap Bar Deadlift'), (SELECT id FROM tags WHERE name = 'Bilateral')),
((SELECT id FROM exercises WHERE name = 'Trap Bar Deadlift'), (SELECT id FROM tags WHERE name = 'Posterior Chain')),

((SELECT id FROM exercises WHERE name = 'Kettlebell Swing'), (SELECT id FROM tags WHERE name = 'Accessory')),
((SELECT id FROM exercises WHERE name = 'Kettlebell Swing'), (SELECT id FROM tags WHERE name = 'Bilateral')),
((SELECT id FROM exercises WHERE name = 'Kettlebell Swing'), (SELECT id FROM tags WHERE name = 'Posterior Chain')),
((SELECT id FROM exercises WHERE name = 'Kettlebell Swing'), (SELECT id FROM tags WHERE name = 'Explosive')),

((SELECT id FROM exercises WHERE name = 'Depth Jump'), (SELECT id FROM tags WHERE name = 'Primary Lift')),
((SELECT id FROM exercises WHERE name = 'Depth Jump'), (SELECT id FROM tags WHERE name = 'Bilateral')),
((SELECT id FROM exercises WHERE name = 'Depth Jump'), (SELECT id FROM tags WHERE name = 'Explosive')),

((SELECT id FROM exercises WHERE name = 'Medicine Ball Rotational Scoop Toss'), (SELECT id FROM tags WHERE name = 'Accessory')),
((SELECT id FROM exercises WHERE name = 'Medicine Ball Rotational Scoop Toss'), (SELECT id FROM tags WHERE name = 'Bilateral')),
((SELECT id FROM exercises WHERE name = 'Medicine Ball Rotational Scoop Toss'), (SELECT id FROM tags WHERE name = 'Explosive')),

((SELECT id FROM exercises WHERE name = 'A-Skip'), (SELECT id FROM tags WHERE name = 'Warm-up')),
((SELECT id FROM exercises WHERE name = 'A-Skip'), (SELECT id FROM tags WHERE name = 'Unilateral')),

((SELECT id FROM exercises WHERE name = 'Single-Leg Isometric Wall Sit'), (SELECT id FROM tags WHERE name = 'Warm-up')),
((SELECT id FROM exercises WHERE name = 'Single-Leg Isometric Wall Sit'), (SELECT id FROM tags WHERE name = 'Rehab')),
((SELECT id FROM exercises WHERE name = 'Single-Leg Isometric Wall Sit'), (SELECT id FROM tags WHERE name = 'Unilateral')),

((SELECT id FROM exercises WHERE name = 'Nordic Hamstring Curl'), (SELECT id FROM tags WHERE name = 'Accessory')),
((SELECT id FROM exercises WHERE name = 'Nordic Hamstring Curl'), (SELECT id FROM tags WHERE name = 'Bilateral')),
((SELECT id FROM exercises WHERE name = 'Nordic Hamstring Curl'), (SELECT id FROM tags WHERE name = 'Posterior Chain')),
((SELECT id FROM exercises WHERE name = 'Nordic Hamstring Curl'), (SELECT id FROM tags WHERE name = 'Rehab'));
