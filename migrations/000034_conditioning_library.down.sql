-- Migration 000034 Down: Remove conditioning library
-- Removes sport-specific conditioning exercises and tags

-- Remove tag mappings for conditioning exercises
DELETE FROM exercise_tag_map 
WHERE exercise_id IN (
  'sp_res_01', 'sp_res_02', 'sp_res_03', 'sp_res_04', 'sp_res_05', 'sp_res_06', 'sp_res_07',
  'sp_assist_01', 'sp_assist_02', 'sp_assist_03', 'sp_assist_04', 'sp_assist_05',
  'sp_decel_01', 'sp_decel_02', 'sp_decel_03', 'sp_decel_04', 'sp_decel_05', 'sp_decel_06'
);

-- Remove conditioning exercises
DELETE FROM exercises 
WHERE id IN (
  'sp_res_01', 'sp_res_02', 'sp_res_03', 'sp_res_04', 'sp_res_05', 'sp_res_06', 'sp_res_07',
  'sp_assist_01', 'sp_assist_02', 'sp_assist_03', 'sp_assist_04', 'sp_assist_05',
  'sp_decel_01', 'sp_decel_02', 'sp_decel_03', 'sp_decel_04', 'sp_decel_05', 'sp_decel_06'
);

-- Remove conditioning tags (only if no other exercises use them)
DELETE FROM exercise_tags 
WHERE name IN ('Resisted Sprint', 'Assisted Sprint', 'Deceleration', 'Speed Development')
AND id NOT IN (
  SELECT DISTINCT tag_id FROM exercise_tag_map
);
