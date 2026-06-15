-- Forge Exercise Intelligence Database - Migration 000008 (Down)
-- Description: Clean up seeded Cricket knowledge graph data.

-- Truncate child junctions first
TRUNCATE TABLE 
    deficit_movement_templates,
    deficit_training_methods,
    driver_assessments,
    benchmarks,
    deficits,
    assessments,
    performance_drivers,
    roles
RESTART IDENTITY CASCADE;
