-- Rollback Phase 2 Elite Library
BEGIN;

-- Delete exercises added in Phase 2
DELETE FROM exercises WHERE source_organization IN (
    'USOPC', 'UKSCA', 'ALTIS', 'Strongman Corp', 'EXOS', 
    'McGill Method', 'Frans Bosch', 'IOC Consensus', 'Swedish School',
    'FMS/SFMA', 'Gray Cook', 'MLB Sports Med', 'FMS', 'SFMA',
    'WSM', 'Rugby S&C', 'CrossFit', 'MMA Conditioning', 'Firefighter Prep'
) AND id > (SELECT COALESCE(MAX(id), 0) FROM exercises WHERE source_organization NOT IN (
    'USOPC', 'UKSCA', 'ALTIS', 'Strongman Corp', 'EXOS', 
    'McGill Method', 'Frans Bosch', 'IOC Consensus', 'Swedish School',
    'FMS/SFMA', 'Gray Cook', 'MLB Sports Med', 'FMS', 'SFMA',
    'WSM', 'Rugby S&C', 'CrossFit', 'MMA Conditioning', 'Firefighter Prep'
));

-- Remove migration record
DELETE FROM schema_migrations WHERE version = '000027';

COMMIT;
