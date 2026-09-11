-- Migration: 000027_elite_exercise_library (ROLLBACK)
-- Intent: Remove Phase 1 elite exercises if needed

BEGIN;

-- Delete exercises added in this migration by name
DELETE FROM exercises WHERE name IN (
    -- Power & Elasticity
    'Snap Down',
    'Dribble Hop',
    'Hang Power Clean (Mid-Thigh)',
    'Med Ball Rotational Throw (Side Step)',
    'Broad Jump to Stick',
    
    -- Max Strength
    'Landmine Split Squat',
    'Single Arm Farmer''s Carry',
    'Nordic Hamstring Curl (Eccentric)',
    'Zercher Squat',
    'Weighted Pull-Up (Neutral Grip)',
    
    -- Complexes
    'Lunge to Step-Up Knee Drive Complex',
    'RDL to Box Jump Contrast',
    'Renegade Row to Push-Up Complex',
    'Inverted Row to Pike Push-Up',
    'Trap Bar Deadlift to Vertical Jump',
    'Bench Press to Med Ball Chest Pass',
    'Landmine Rotational Press to Woodchop',
    'Lateral Bound to Stick',
    
    -- Mobility & Prehab
    '90/90 Hip Switch',
    'Thoracic Spine Windmill',
    'Copenhagen Plank (Short Lever)',
    'Ankle Dorsiflexion Rock',
    
    -- Conditioning
    'Shuttle Run (5-10-5)',
    'Hill Sprints (10-15 sec)',
    'Battle Ropes (30s Alternating Wave)'
);

COMMIT;
