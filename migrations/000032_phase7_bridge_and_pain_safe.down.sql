-- Rollback for Migration 000032: Phase 7
DELETE FROM exercises WHERE id BETWEEN 301 AND 335;
