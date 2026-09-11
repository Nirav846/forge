-- Phase 5 Down Migration: Remove Unilateral Hip Dominant (IDs 120-131)

DELETE FROM exercises WHERE id BETWEEN 120 AND 131;

-- Reset sequence if needed
SELECT setval('exercises_id_seq', (SELECT MAX(id) FROM exercises));
