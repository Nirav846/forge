-- Forge Exercise Intelligence Database - Migration 000009 (Down)
-- Description: Clean up comprehensive seeded Cricket knowledge graph records.

DELETE FROM deficit_movement_templates WHERE deficit_id IN (
    SELECT id FROM deficits WHERE name IN ('Power Deficit', 'Strength Deficit', 'Acceleration Deficit', 'Speed Deficit', 'Mobility Restriction')
);

DELETE FROM deficit_training_methods WHERE deficit_id IN (
    SELECT id FROM deficits WHERE name IN ('Power Deficit', 'Strength Deficit', 'Acceleration Deficit', 'Speed Deficit', 'Mobility Restriction')
);

DELETE FROM deficits WHERE name IN ('Power Deficit', 'Strength Deficit', 'Acceleration Deficit', 'Speed Deficit', 'Mobility Restriction');

DELETE FROM benchmarks WHERE assessment_id IN (
    SELECT id FROM assessments WHERE name IN ('CMJ', 'Broad Jump', '10m Sprint', '20m Sprint', 'Pull Up', 'Trap Bar Deadlift', 'Rotational Med Ball Throw')
);

DELETE FROM driver_assessments WHERE assessment_id IN (
    SELECT id FROM assessments WHERE name IN ('CMJ', 'Broad Jump', '10m Sprint', '20m Sprint', 'Pull Up', 'Trap Bar Deadlift', 'Rotational Med Ball Throw')
);

DELETE FROM assessments WHERE name IN ('CMJ', 'Broad Jump', '10m Sprint', '20m Sprint', 'Pull Up', 'Trap Bar Deadlift', 'Rotational Med Ball Throw');

DELETE FROM performance_drivers WHERE name IN ('Power', 'Speed', 'Shoulder Robustness', 'Strength', 'Work Capacity', 'Rotational Power', 'Reactive Agility', 'Acceleration');

DELETE FROM training_methods WHERE name IN ('Max Strength', 'Dynamic Effort', 'Plyometrics', 'Sprint Training', 'COD Training', 'Rotational Power', 'Mobility');
