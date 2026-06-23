-- Forge Exercise Intelligence Database - Migration 000025 (Down)
-- Description: Remove unified naming convention assessments, deficits, benchmarks, and routing.

BEGIN;

DELETE FROM deficit_movement_templates WHERE deficit_id IN (1, 2, 3, 4, 5, 6, 7);

DELETE FROM benchmarks WHERE assessment_id IN (1, 2, 3, 4, 5, 6, 7)
  AND name IN (
    'CMJ Elite', 'CMJ Optimal', 'CMJ Sub-optimal', 'CMJ Poor',
    'Broad Jump Elite', 'Broad Jump Optimal', 'Broad Jump Sub-optimal', 'Broad Jump Poor',
    '10m Sprint Elite', '10m Sprint Optimal', '10m Sprint Sub-optimal', '10m Sprint Poor',
    '20m Sprint Elite', '20m Sprint Optimal', '20m Sprint Sub-optimal', '20m Sprint Poor',
    'Pull Up Elite', 'Pull Up Optimal', 'Pull Up Sub-optimal', 'Pull Up Poor',
    'Trap Bar Deadlift Elite', 'Trap Bar Deadlift Optimal', 'Trap Bar Deadlift Sub-optimal', 'Trap Bar Deadlift Poor',
    'Rotational Med Ball Throw Elite', 'Rotational Med Ball Throw Optimal', 'Rotational Med Ball Throw Sub-optimal', 'Rotational Med Ball Throw Poor'
  );

DELETE FROM deficits WHERE id IN (1, 2, 3, 4, 5, 6, 7);

DELETE FROM assessments WHERE id IN (1, 2, 3, 4, 5, 6, 7);

COMMIT;
