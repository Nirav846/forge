-- Rollback Phase 3: Remove foundational strength exercises (IDs 200-249)
BEGIN;

DELETE FROM exercises WHERE id BETWEEN 200 AND 249;

COMMIT;
