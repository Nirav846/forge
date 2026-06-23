-- Forge Exercise Intelligence Database - Migration 000025 (Up)
-- Description: Consolidated single-naming-convention seed for assessments, deficits, benchmarks, and routing.
-- Replaces PHASE_5A_SEED.sql and deleted 000021 (both regular and fixed) with unified naming.
-- Single naming convention: Proper case, descriptive but concise (e.g. 'CMJ', 'Broad Jump', '10m Sprint').

BEGIN;

-- Insert assessments with unified naming convention
INSERT INTO assessments (id, name, metric_unit, description) OVERRIDING SYSTEM VALUE VALUES
  (1, 'CMJ', 'cm', 'Vertical jump test measuring lower body power output'),
  (2, 'Broad Jump', 'm', 'Horizontal jump test measuring triple extension power'),
  (3, '10m Sprint', 's', 'Linear acceleration test measuring initial drive phase mechanics'),
  (4, '20m Sprint', 's', 'Max velocity sprint test measuring top-end speed'),
  (5, 'Pull Up', 'reps', 'Upper body pulling strength and scapular stability test'),
  (6, 'Trap Bar Deadlift', 'kg', 'Lower body absolute strength test'),
  (7, 'Rotational Med Ball Throw', 'm/s', 'Rotational power test measuring transverse plane torque')
ON CONFLICT (id) DO NOTHING;

-- Insert deficits (linked to assessments)
INSERT INTO deficits (id, assessment_id, name, description) OVERRIDING SYSTEM VALUE VALUES
  (1, 1, 'Power Deficit', 'Lack of vertical power and rate of force development'),
  (2, 3, 'Acceleration Deficit', 'Sub-optimal acceleration mechanics and horizontal force application'),
  (3, 2, 'Mobility Restriction', 'Joint restriction limiting triple extension and movement quality'),
  (4, 4, 'Speed Deficit', 'Sub-optimal max linear running speeds and stride mechanics'),
  (5, 6, 'Strength Deficit', 'Falls below absolute lower body force production requirements'),
  (6, 7, 'Rotational Power Deficit', 'Lack of rotational power and explosive transverse torque'),
  (7, 5, 'Shoulder Robustness Deficit', 'Lack of upper body pulling strength or scapular stability')
ON CONFLICT (id) DO NOTHING;

-- Insert benchmarks with unified naming
-- CMJ (assessment_id = 1)
INSERT INTO benchmarks (assessment_id, name, classification, min_value, max_value) VALUES
  (1, 'CMJ Elite', 'Elite', 55.0, NULL),
  (1, 'CMJ Optimal', 'Optimal', 45.0, 54.99),
  (1, 'CMJ Sub-optimal', 'Sub-optimal', 35.0, 44.99),
  (1, 'CMJ Poor', 'Poor', NULL, 34.99)
ON CONFLICT (assessment_id, name) DO NOTHING;

-- Broad Jump (assessment_id = 2)
INSERT INTO benchmarks (assessment_id, name, classification, min_value, max_value) VALUES
  (2, 'Broad Jump Elite', 'Elite', 2.60, NULL),
  (2, 'Broad Jump Optimal', 'Optimal', 2.20, 2.59),
  (2, 'Broad Jump Sub-optimal', 'Sub-optimal', 1.80, 2.19),
  (2, 'Broad Jump Poor', 'Poor', NULL, 1.79)
ON CONFLICT (assessment_id, name) DO NOTHING;

-- 10m Sprint (assessment_id = 3)
INSERT INTO benchmarks (assessment_id, name, classification, min_value, max_value) VALUES
  (3, '10m Sprint Elite', 'Elite', NULL, 1.60),
  (3, '10m Sprint Optimal', 'Optimal', 1.61, 1.80),
  (3, '10m Sprint Sub-optimal', 'Sub-optimal', 1.81, 2.00),
  (3, '10m Sprint Poor', 'Poor', 2.01, NULL)
ON CONFLICT (assessment_id, name) DO NOTHING;

-- 20m Sprint (assessment_id = 4)
INSERT INTO benchmarks (assessment_id, name, classification, min_value, max_value) VALUES
  (4, '20m Sprint Elite', 'Elite', NULL, 2.80),
  (4, '20m Sprint Optimal', 'Optimal', 2.81, 3.10),
  (4, '20m Sprint Sub-optimal', 'Sub-optimal', 3.11, 3.40),
  (4, '20m Sprint Poor', 'Poor', 3.41, NULL)
ON CONFLICT (assessment_id, name) DO NOTHING;

-- Pull Up (assessment_id = 5)
INSERT INTO benchmarks (assessment_id, name, classification, min_value, max_value) VALUES
  (5, 'Pull Up Elite', 'Elite', 20.0, NULL),
  (5, 'Pull Up Optimal', 'Optimal', 12.0, 19.99),
  (5, 'Pull Up Sub-optimal', 'Sub-optimal', 6.0, 11.99),
  (5, 'Pull Up Poor', 'Poor', NULL, 5.99)
ON CONFLICT (assessment_id, name) DO NOTHING;

-- Trap Bar Deadlift (assessment_id = 6)
INSERT INTO benchmarks (assessment_id, name, classification, min_value, max_value) VALUES
  (6, 'Trap Bar Deadlift Elite', 'Elite', 200.0, NULL),
  (6, 'Trap Bar Deadlift Optimal', 'Optimal', 160.0, 199.99),
  (6, 'Trap Bar Deadlift Sub-optimal', 'Sub-optimal', 120.0, 159.99),
  (6, 'Trap Bar Deadlift Poor', 'Poor', NULL, 119.99)
ON CONFLICT (assessment_id, name) DO NOTHING;

-- Rotational Med Ball Throw (assessment_id = 7)
INSERT INTO benchmarks (assessment_id, name, classification, min_value, max_value) VALUES
  (7, 'Rotational Med Ball Throw Elite', 'Elite', 6.0, NULL),
  (7, 'Rotational Med Ball Throw Optimal', 'Optimal', 5.0, 5.99),
  (7, 'Rotational Med Ball Throw Sub-optimal', 'Sub-optimal', 4.0, 4.99),
  (7, 'Rotational Med Ball Throw Poor', 'Poor', NULL, 3.99)
ON CONFLICT (assessment_id, name) DO NOTHING;

-- Deficit to Movement Template Routing
INSERT INTO deficit_movement_templates (deficit_id, movement_template_id) VALUES
  (1, 1), -- Power Deficit -> Lower Body Power
  (5, 1), -- Strength Deficit -> Lower Body Power
  (2, 2), -- Acceleration Deficit -> Acceleration Development
  (4, 2), -- Speed Deficit -> Acceleration Development
  (6, 3), -- Rotational Power Deficit -> Rotational Power
  (7, 4), -- Shoulder Robustness Deficit -> Shoulder Robustness
  (3, 4)  -- Mobility Restriction -> Shoulder Robustness
ON CONFLICT DO NOTHING;

COMMIT;
