-- Phase 35A Down: Remove plyometrics expansion
-- Reverts Phase 35A conditioning plyometrics

-- Delete exercise-tag relationships for plyometric exercises
DELETE FROM exercise_tags WHERE exercise_id IN (
    SELECT id FROM exercises WHERE id LIKE 'plyo_%'
);

-- Delete plyometric exercises
DELETE FROM exercises WHERE id LIKE 'plyo_%';

-- Remove new tags (will cascade to exercise_tags)
DELETE FROM tags WHERE name IN ('Plyometric', 'Jump Training', 'Depth Jump', 'Bounding', 'Shock Method');
