-- Forge Exercise Intelligence Database - Migration 000005 (Down)
-- Description: Clean up seeded Cricket exercises, templates, slots, and mappings.

DELETE FROM slot_progressions 
WHERE slot_id IN (
    SELECT id FROM template_slots WHERE template_id = (SELECT id FROM movement_templates WHERE name = 'Cricket Fast Bowler Power')
);

DELETE FROM slot_requirements 
WHERE slot_id IN (
    SELECT id FROM template_slots WHERE template_id = (SELECT id FROM movement_templates WHERE name = 'Cricket Fast Bowler Power')
);

DELETE FROM template_slots 
WHERE template_id = (SELECT id FROM movement_templates WHERE name = 'Cricket Fast Bowler Power');

DELETE FROM movement_templates 
WHERE name = 'Cricket Fast Bowler Power';

DELETE FROM exercise_tags WHERE exercise_id IN (
    SELECT id FROM exercises WHERE name IN (
        'Trap Bar Jump Squat', 
        'Single-Leg Lateral Bound', 
        'Medicine Ball Overhead Backwards Toss', 
        'Medicine Ball Rotational Chest Pass', 
        'Cable Pallof Press with Rotation'
    )
);

DELETE FROM exercise_sport_mapping WHERE exercise_id IN (
    SELECT id FROM exercises WHERE name IN (
        'Trap Bar Jump Squat', 
        'Single-Leg Lateral Bound', 
        'Medicine Ball Overhead Backwards Toss', 
        'Medicine Ball Rotational Chest Pass', 
        'Cable Pallof Press with Rotation'
    )
);

DELETE FROM exercise_training_methods WHERE exercise_id IN (
    SELECT id FROM exercises WHERE name IN (
        'Trap Bar Jump Squat', 
        'Single-Leg Lateral Bound', 
        'Medicine Ball Overhead Backwards Toss', 
        'Medicine Ball Rotational Chest Pass', 
        'Cable Pallof Press with Rotation'
    )
);

DELETE FROM exercise_physical_qualities WHERE exercise_id IN (
    SELECT id FROM exercises WHERE name IN (
        'Trap Bar Jump Squat', 
        'Single-Leg Lateral Bound', 
        'Medicine Ball Overhead Backwards Toss', 
        'Medicine Ball Rotational Chest Pass', 
        'Cable Pallof Press with Rotation'
    )
);

DELETE FROM exercise_movement_patterns WHERE exercise_id IN (
    SELECT id FROM exercises WHERE name IN (
        'Trap Bar Jump Squat', 
        'Single-Leg Lateral Bound', 
        'Medicine Ball Overhead Backwards Toss', 
        'Medicine Ball Rotational Chest Pass', 
        'Cable Pallof Press with Rotation'
    )
);

DELETE FROM exercise_equipment WHERE exercise_id IN (
    SELECT id FROM exercises WHERE name IN (
        'Trap Bar Jump Squat', 
        'Single-Leg Lateral Bound', 
        'Medicine Ball Overhead Backwards Toss', 
        'Medicine Ball Rotational Chest Pass', 
        'Cable Pallof Press with Rotation'
    )
);

DELETE FROM exercises WHERE name IN (
    'Trap Bar Jump Squat', 
    'Single-Leg Lateral Bound', 
    'Medicine Ball Overhead Backwards Toss', 
    'Medicine Ball Rotational Chest Pass', 
    'Cable Pallof Press with Rotation'
);
