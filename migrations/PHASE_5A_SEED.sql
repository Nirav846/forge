-- SUPERSEDED by 000025_unify_assessment_naming_convention
-- This file is kept for reference only. Do not apply directly.
-- 000025 provides the same content with unified naming convention.
-- Seed assessments, deficits, benchmarks, and routing mappings
BEGIN;

-- Insert assessments (OVERRIDING SYSTEM VALUE to handle identity columns)
INSERT INTO assessments (id, name, metric_unit, description) OVERRIDING SYSTEM VALUE VALUES
  (1, 'cmj', 'cm', 'Vertical jump test measuring lower body power output'),
  (2, 'broad jump', 'm', 'Horizontal jump test measuring triple extension power'),
  (3, '10m sprint', 's', 'Linear acceleration test measuring initial drive phase mechanics'),
  (4, '20m sprint', 's', 'Max velocity sprint test measuring top-end speed'),
  (5, 'pull up', 'reps', 'Upper body pulling strength and scapular stability test'),
  (6, 'trap bar deadlift', 'kg', 'Lower body absolute strength test'),
  (7, 'rotational med ball throw', 'm/s', 'Rotational power test measuring transverse plane torque')
ON CONFLICT (id) DO NOTHING;

-- Insert deficits
INSERT INTO deficits (id, assessment_id, name, description) OVERRIDING SYSTEM VALUE VALUES
  (1, 1, 'Power Deficit', 'Lack of vertical power and rate of force development'),
  (2, 3, 'Acceleration Deficit', 'Sub-optimal acceleration mechanics and horizontal force application'),
  (3, 2, 'Mobility Restriction', 'Joint restriction limiting triple extension and movement quality'),
  (4, 4, 'Speed Deficit', 'Sub-optimal max linear running speeds and stride mechanics'),
  (5, 6, 'Strength Deficit', 'Falls below absolute lower body force production requirements'),
  (6, 7, 'Rotational Power Deficit', 'Lack of rotational power and explosive transverse torque'),
  (7, 5, 'Shoulder Robustness Deficit', 'Lack of upper body pulling strength or scapular stability')
ON CONFLICT (id) DO NOTHING;

-- Insert benchmarks
-- CMJ
INSERT INTO benchmarks (assessment_id, name, classification, min_value, max_value) VALUES
  (1, 'cmj_elite', 'Elite', 55.0, NULL),
  (1, 'cmj_optimal', 'Optimal', 45.0, 54.99),
  (1, 'cmj_suboptimal', 'Sub-optimal', 35.0, 44.99),
  (1, 'cmj_poor', 'Poor', NULL, 34.99)
ON CONFLICT (assessment_id, name) DO NOTHING;

-- Broad Jump
INSERT INTO benchmarks (assessment_id, name, classification, min_value, max_value) VALUES
  (2, 'bj_elite', 'Elite', 2.60, NULL),
  (2, 'bj_optimal', 'Optimal', 2.20, 2.59),
  (2, 'bj_suboptimal', 'Sub-optimal', 1.80, 2.19),
  (2, 'bj_poor', 'Poor', NULL, 1.79)
ON CONFLICT (assessment_id, name) DO NOTHING;

-- 10m Sprint
INSERT INTO benchmarks (assessment_id, name, classification, min_value, max_value) VALUES
  (3, 'sprint10_elite', 'Elite', NULL, 1.60),
  (3, 'sprint10_optimal', 'Optimal', 1.61, 1.80),
  (3, 'sprint10_suboptimal', 'Sub-optimal', 1.81, 2.00),
  (3, 'sprint10_poor', 'Poor', 2.01, NULL)
ON CONFLICT (assessment_id, name) DO NOTHING;

-- 20m Sprint
INSERT INTO benchmarks (assessment_id, name, classification, min_value, max_value) VALUES
  (4, 'sprint20_elite', 'Elite', NULL, 2.80),
  (4, 'sprint20_optimal', 'Optimal', 2.81, 3.10),
  (4, 'sprint20_suboptimal', 'Sub-optimal', 3.11, 3.40),
  (4, 'sprint20_poor', 'Poor', 3.41, NULL)
ON CONFLICT (assessment_id, name) DO NOTHING;

-- Pull Up
INSERT INTO benchmarks (assessment_id, name, classification, min_value, max_value) VALUES
  (5, 'pullup_elite', 'Elite', 20.0, NULL),
  (5, 'pullup_optimal', 'Optimal', 12.0, 19.99),
  (5, 'pullup_suboptimal', 'Sub-optimal', 6.0, 11.99),
  (5, 'pullup_poor', 'Poor', NULL, 5.99)
ON CONFLICT (assessment_id, name) DO NOTHING;

-- Trap Bar Deadlift
INSERT INTO benchmarks (assessment_id, name, classification, min_value, max_value) VALUES
  (6, 'tbd_elite', 'Elite', 200.0, NULL),
  (6, 'tbd_optimal', 'Optimal', 160.0, 199.99),
  (6, 'tbd_suboptimal', 'Sub-optimal', 120.0, 159.99),
  (6, 'tbd_poor', 'Poor', NULL, 119.99)
ON CONFLICT (assessment_id, name) DO NOTHING;

-- Rotational Med Ball Throw
INSERT INTO benchmarks (assessment_id, name, classification, min_value, max_value) VALUES
  (7, 'rot_elite', 'Elite', 6.0, NULL),
  (7, 'rot_optimal', 'Optimal', 5.0, 5.99),
  (7, 'rot_suboptimal', 'Sub-optimal', 4.0, 4.99),
  (7, 'rot_poor', 'Poor', NULL, 3.99)
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
