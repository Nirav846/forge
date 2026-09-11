-- Phase 4 Down Migration: Remove Olympic & Accessories (IDs 106-119)

DELETE FROM exercises WHERE id BETWEEN 106 AND 119;

-- Reset sequence if needed
SELECT setval('exercises_id_seq', (SELECT MAX(id) FROM exercises));
