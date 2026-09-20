-- Phase 2 Down Migration: Remove Elite Library Phase 2 exercises (IDs 66-105)

DELETE FROM exercises WHERE id BETWEEN 66 AND 105;

-- Reset sequence if needed
SELECT setval('exercises_id_seq', (SELECT MAX(id) FROM exercises));
