-- Forge Exercise Intelligence Database - Migration 000033 (Down)
-- Description: ROLLBACK COMBO MOVEMENTS LIBRARY EXPANSION

BEGIN;

-- Remove Combo tag assignments
DELETE FROM exercise_tags
WHERE tag_id = (SELECT id FROM tags WHERE name = 'Combo')
AND exercise_id IN (
    SELECT id FROM exercises 
    WHERE name LIKE '%Combo%'
);

-- Remove Combo exercises
DELETE FROM exercises
WHERE name IN (
    -- Upper Body Combos
    'Pull-Up to Push-Up Combo',
    'Inverted Row to Pike Push-Up Combo',
    'Face Pull to External Rotation Combo',
    'Chin-Up to Dip Combo',
    'Renegade Row to Push-Up Combo',
    'Z Press to Landmine Press Combo',
    'Farmer Carry to Overhead Press Combo',
    'Battle Rope Slam to Burpee Combo',
    'Medicine Ball Scoop Toss to Push-Up Combo',
    'Band Pull-Apart to Push-Up Combo',
    'TRX Row to TRX Push-Up Combo',
    'Kettlebell Clean to Rack Hold to Press Combo',
    
    -- Lower Body Combos
    'Curtsy to Reverse Lunge Combo',
    'Lateral Lunge to Skater Hop Combo',
    'Step-Up to Knee Drive Combo',
    'Cossack Squat to Skater Hop Combo',
    'Bulgarian Split Squat to Broad Jump Combo',
    'Romanian Deadlift to Good Morning Combo',
    'Reverse Lunge to Hurdle Hop Combo',
    'Front Squat to Jump Squat Combo',
    'Single-Leg RDL to Box Step-Up Combo',
    'Goblet Squat to Calf Raise Combo',
    'Walking Lunge to Jump Lunge Combo',
    'Hip Thrust to Jump Combo',
    
    -- Power/Full Body Combos
    'Power Clean to Broad Jump Combo',
    'Snatch Pull to Overhead Med Ball Slam Combo',
    'Back Squat to Hurdle Hop Combo',
    'Thruster to Box Jump Combo',
    'Kettlebell Swing to Jump Squat Combo',
    'Medicine Ball Scoop Toss to Sprint Combo',
    'Burpee to Broad Jump Combo',
    'Battle Rope Waves to Slam Ball Combo',
    'Box Jump to Depth Drop Combo',
    'Clean Pull to Vertical Jump Combo',
    'Sandbag Shoulder to Sprint Combo'
);

-- Note: We do NOT remove the 'Combo' tag itself as it may be referenced elsewhere
-- If you want to remove the tag entirely, uncomment the following line:
-- DELETE FROM tags WHERE name = 'Combo';

COMMIT;
