-- Phase 6 Down Migration: Remove Elite Locker Room (IDs 132-171)

DELETE FROM exercises WHERE id BETWEEN 132 AND 171;

-- Reset sequence if needed
SELECT setval('exercises_id_seq', (SELECT MAX(id) FROM exercises));
