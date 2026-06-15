-- Forge Exercise Intelligence Database - Migration 000009 (Up)
-- Description: Seed comprehensive Cricket S&C Knowledge Graph.

-- -------------------------------------------------------------
-- 1. Seed Training Methods (Ensure All Exist)
-- -------------------------------------------------------------
INSERT INTO training_methods (name, description) VALUES
('Max Strength', 'High load, low velocity strength training targeting motor unit recruitment.'),
('Dynamic Effort', 'Submaximal loads executed at maximal concentric velocities to train rate of force development.'),
('Plyometrics', 'Exercises leveraging the stretch-shortening cycle (SSC) to improve elastic force output.'),
('Sprint Training', 'Maximal velocity running drills to develop acceleration and top-end speed mechanics.'),
('COD Training', 'Change of Direction protocols targeting decelerative control and lateral force generation.'),
('Rotational Power', 'Explosive exercises in the transverse plane targeting rotational velocity.'),
('Mobility', 'Active range of motion exercises designed to increase joint mobility and decrease restriction.')
ON CONFLICT (name) DO UPDATE SET description = EXCLUDED.description;

-- -------------------------------------------------------------
-- 2. Seed Performance Drivers (Strength, Power, Acceleration, Speed, Rotational Power, Reactive Agility, Work Capacity, Shoulder Robustness)
-- -------------------------------------------------------------

-- Drivers for: Fast Bowler
INSERT INTO performance_drivers (role_id, name, description, priority) VALUES
((SELECT id FROM roles WHERE name = 'Fast Bowler'), 'Power', 'Explosive vertical and horizontal force production in bowling stride.', 'Primary'),
((SELECT id FROM roles WHERE name = 'Fast Bowler'), 'Speed', 'Maximal running velocity in bowling run-up.', 'Primary'),
((SELECT id FROM roles WHERE name = 'Fast Bowler'), 'Shoulder Robustness', 'Shoulder stability and integrity to withstand landing block forces.', 'Primary'),
((SELECT id FROM roles WHERE name = 'Fast Bowler'), 'Strength', 'Absolute force capacity to support bone density and joint loads.', 'Secondary'),
((SELECT id FROM roles WHERE name = 'Fast Bowler'), 'Work Capacity', 'Repeat bowl capacity and multi-spell endurance.', 'Secondary')
ON CONFLICT DO NOTHING;

-- Drivers for: Spinner
INSERT INTO performance_drivers (role_id, name, description, priority) VALUES
((SELECT id FROM roles WHERE name = 'Spinner'), 'Rotational Power', 'Explosive transverse torque generation to maximize spin revolutions.', 'Primary'),
((SELECT id FROM roles WHERE name = 'Spinner'), 'Shoulder Robustness', 'Stabilization of glenohumeral joint during high volume spells.', 'Primary'),
((SELECT id FROM roles WHERE name = 'Spinner'), 'Strength', 'Foundational trunk and pelvic absolute strength.', 'Secondary'),
((SELECT id FROM roles WHERE name = 'Spinner'), 'Reactive Agility', 'Rapid response and lateral dive capability in fielding.', 'Secondary')
ON CONFLICT DO NOTHING;

-- Drivers for: Batter
INSERT INTO performance_drivers (role_id, name, description, priority) VALUES
((SELECT id FROM roles WHERE name = 'Batter'), 'Acceleration', 'Initial drive velocity when executing runs or charging bowlers.', 'Primary'),
((SELECT id FROM roles WHERE name = 'Batter'), 'Speed', 'Maximal sprinting speed between wickets.', 'Primary'),
((SELECT id FROM roles WHERE name = 'Batter'), 'Reactive Agility', 'Lateral evasion and rapid weight shifts in batting stance.', 'Primary'),
((SELECT id FROM roles WHERE name = 'Batter'), 'Strength', 'Grip and forearm absolute force output to maintain bat control.', 'Secondary'),
((SELECT id FROM roles WHERE name = 'Batter'), 'Power', 'Vertical force generation to drive high-velocity bat swings.', 'Secondary')
ON CONFLICT DO NOTHING;

-- Drivers for: Wicket Keeper
INSERT INTO performance_drivers (role_id, name, description, priority) VALUES
((SELECT id FROM roles WHERE name = 'Wicket Keeper'), 'Reactive Agility', 'Ultra-fast lateral diving and catching reaction speeds.', 'Primary'),
((SELECT id FROM roles WHERE name = 'Wicket Keeper'), 'Strength', 'Lower body isometric squat bracing strength.', 'Primary'),
((SELECT id FROM roles WHERE name = 'Wicket Keeper'), 'Power', 'Vertical reactive elastic power for launching out of stance.', 'Secondary'),
((SELECT id FROM roles WHERE name = 'Wicket Keeper'), 'Acceleration', 'Rapid multi-directional acceleration for ball pursuit.', 'Secondary')
ON CONFLICT DO NOTHING;

-- Drivers for: All Rounder
INSERT INTO performance_drivers (role_id, name, description, priority) VALUES
((SELECT id FROM roles WHERE name = 'All Rounder'), 'Work Capacity', 'High anaerobic/aerobic capacity to support batting and bowling workloads.', 'Primary'),
((SELECT id FROM roles WHERE name = 'All Rounder'), 'Strength', 'Foundational multi-joint force production capability.', 'Primary'),
((SELECT id FROM roles WHERE name = 'All Rounder'), 'Power', 'Bilateral lower body extension velocity.', 'Primary'),
((SELECT id FROM roles WHERE name = 'All Rounder'), 'Acceleration', 'Dynamic short sprint speed.', 'Secondary'),
((SELECT id FROM roles WHERE name = 'All Rounder'), 'Speed', 'Top-end linear sprint velocity.', 'Secondary')
ON CONFLICT DO NOTHING;

-- -------------------------------------------------------------
-- 3. Seed Assessments (CMJ, Broad Jump, 10m Sprint, 20m Sprint, Pull Up, Trap Bar Deadlift, Rotational Med Ball Throw)
-- -------------------------------------------------------------
INSERT INTO assessments (name, description, metric_unit) VALUES
('CMJ', 'Countermovement Jump test executed on a force plate or jump mat to evaluate vertical power.', 'cm'),
('Broad Jump', 'Standing horizontal jump test measuring horizontal explosive power and force projection.', 'm'),
('10m Sprint', 'Linear sprint test from stationary start to evaluate acceleration mechanics.', 's'),
('20m Sprint', 'Linear sprint test evaluating transitional speed and near-maximum velocity.', 's'),
('Pull Up', 'Bodyweight pull up test to assess upper body pulling relative strength and shoulder girdle robustness.', 'reps'),
('Trap Bar Deadlift', 'Maximal load deadlift performed using a hex bar to evaluate absolute lower body strength.', 'kg'),
('Rotational Med Ball Throw', 'Transverse medicine ball throw against a wall to evaluate rotational power output.', 'm/s')
ON CONFLICT (name) DO UPDATE SET description = EXCLUDED.description, metric_unit = EXCLUDED.metric_unit;

-- -------------------------------------------------------------
-- 4. Map Performance Drivers to Assessments
-- -------------------------------------------------------------
INSERT INTO driver_assessments (performance_driver_id, assessment_id) VALUES
-- Fast Bowler mappings
((SELECT id FROM performance_drivers WHERE role_id = (SELECT id FROM roles WHERE name = 'Fast Bowler') AND name = 'Power'), (SELECT id FROM assessments WHERE name = 'CMJ')),
((SELECT id FROM performance_drivers WHERE role_id = (SELECT id FROM roles WHERE name = 'Fast Bowler') AND name = 'Power'), (SELECT id FROM assessments WHERE name = 'Broad Jump')),
((SELECT id FROM performance_drivers WHERE role_id = (SELECT id FROM roles WHERE name = 'Fast Bowler') AND name = 'Speed'), (SELECT id FROM assessments WHERE name = '20m Sprint')),
((SELECT id FROM performance_drivers WHERE role_id = (SELECT id FROM roles WHERE name = 'Fast Bowler') AND name = 'Shoulder Robustness'), (SELECT id FROM assessments WHERE name = 'Pull Up')),
((SELECT id FROM performance_drivers WHERE role_id = (SELECT id FROM roles WHERE name = 'Fast Bowler') AND name = 'Strength'), (SELECT id FROM assessments WHERE name = 'Trap Bar Deadlift')),

-- Spinner mappings
((SELECT id FROM performance_drivers WHERE role_id = (SELECT id FROM roles WHERE name = 'Spinner') AND name = 'Rotational Power'), (SELECT id FROM assessments WHERE name = 'Rotational Med Ball Throw')),
((SELECT id FROM performance_drivers WHERE role_id = (SELECT id FROM roles WHERE name = 'Spinner') AND name = 'Shoulder Robustness'), (SELECT id FROM assessments WHERE name = 'Pull Up')),
((SELECT id FROM performance_drivers WHERE role_id = (SELECT id FROM roles WHERE name = 'Spinner') AND name = 'Strength'), (SELECT id FROM assessments WHERE name = 'Trap Bar Deadlift')),

-- Batter mappings
((SELECT id FROM performance_drivers WHERE role_id = (SELECT id FROM roles WHERE name = 'Batter') AND name = 'Acceleration'), (SELECT id FROM assessments WHERE name = '10m Sprint')),
((SELECT id FROM performance_drivers WHERE role_id = (SELECT id FROM roles WHERE name = 'Batter') AND name = 'Speed'), (SELECT id FROM assessments WHERE name = '20m Sprint')),
((SELECT id FROM performance_drivers WHERE role_id = (SELECT id FROM roles WHERE name = 'Batter') AND name = 'Strength'), (SELECT id FROM assessments WHERE name = 'Pull Up')),
((SELECT id FROM performance_drivers WHERE role_id = (SELECT id FROM roles WHERE name = 'Batter') AND name = 'Power'), (SELECT id FROM assessments WHERE name = 'CMJ')),

-- Wicket Keeper mappings
((SELECT id FROM performance_drivers WHERE role_id = (SELECT id FROM roles WHERE name = 'Wicket Keeper') AND name = 'Strength'), (SELECT id FROM assessments WHERE name = 'Trap Bar Deadlift')),
((SELECT id FROM performance_drivers WHERE role_id = (SELECT id FROM roles WHERE name = 'Wicket Keeper') AND name = 'Power'), (SELECT id FROM assessments WHERE name = 'CMJ')),
((SELECT id FROM performance_drivers WHERE role_id = (SELECT id FROM roles WHERE name = 'Wicket Keeper') AND name = 'Acceleration'), (SELECT id FROM assessments WHERE name = '10m Sprint')),

-- All Rounder mappings
((SELECT id FROM performance_drivers WHERE role_id = (SELECT id FROM roles WHERE name = 'All Rounder') AND name = 'Strength'), (SELECT id FROM assessments WHERE name = 'Trap Bar Deadlift')),
((SELECT id FROM performance_drivers WHERE role_id = (SELECT id FROM roles WHERE name = 'All Rounder') AND name = 'Power'), (SELECT id FROM assessments WHERE name = 'CMJ')),
((SELECT id FROM performance_drivers WHERE role_id = (SELECT id FROM roles WHERE name = 'All Rounder') AND name = 'Acceleration'), (SELECT id FROM assessments WHERE name = '10m Sprint'))
ON CONFLICT DO NOTHING;

-- -------------------------------------------------------------
-- 5. Seed Benchmarks (For all 7 Assessments)
-- -------------------------------------------------------------

-- CMJ
INSERT INTO benchmarks (assessment_id, name, min_value, max_value, classification) VALUES
((SELECT id FROM assessments WHERE name = 'CMJ'), 'CMJ Elite', 55.00, NULL, 'Elite'),
((SELECT id FROM assessments WHERE name = 'CMJ'), 'CMJ Optimal', 45.00, 54.99, 'Optimal'),
((SELECT id FROM assessments WHERE name = 'CMJ'), 'CMJ Sub-optimal', 35.00, 44.99, 'Sub-optimal'),
((SELECT id FROM assessments WHERE name = 'CMJ'), 'CMJ Poor', NULL, 34.99, 'Poor')
ON CONFLICT (assessment_id, name) DO NOTHING;

-- Broad Jump
INSERT INTO benchmarks (assessment_id, name, min_value, max_value, classification) VALUES
((SELECT id FROM assessments WHERE name = 'Broad Jump'), 'Broad Jump Elite', 2.60, NULL, 'Elite'),
((SELECT id FROM assessments WHERE name = 'Broad Jump'), 'Broad Jump Optimal', 2.20, 2.59, 'Optimal'),
((SELECT id FROM assessments WHERE name = 'Broad Jump'), 'Broad Jump Sub-optimal', 1.80, 2.19, 'Sub-optimal'),
((SELECT id FROM assessments WHERE name = 'Broad Jump'), 'Broad Jump Poor', NULL, 1.79, 'Poor')
ON CONFLICT (assessment_id, name) DO NOTHING;

-- 10m Sprint (Lower time is better: Elite <= 1.60s, Poor >= 2.00s)
INSERT INTO benchmarks (assessment_id, name, min_value, max_value, classification) VALUES
((SELECT id FROM assessments WHERE name = '10m Sprint'), '10m Sprint Elite', NULL, 1.60, 'Elite'),
((SELECT id FROM assessments WHERE name = '10m Sprint'), '10m Sprint Optimal', 1.61, 1.80, 'Optimal'),
((SELECT id FROM assessments WHERE name = '10m Sprint'), '10m Sprint Sub-optimal', 1.81, 2.00, 'Sub-optimal'),
((SELECT id FROM assessments WHERE name = '10m Sprint'), '10m Sprint Poor', 2.01, NULL, 'Poor')
ON CONFLICT (assessment_id, name) DO NOTHING;

-- 20m Sprint (Lower time is better: Elite <= 2.80s, Poor >= 3.40s)
INSERT INTO benchmarks (assessment_id, name, min_value, max_value, classification) VALUES
((SELECT id FROM assessments WHERE name = '20m Sprint'), '20m Sprint Elite', NULL, 2.80, 'Elite'),
((SELECT id FROM assessments WHERE name = '20m Sprint'), '20m Sprint Optimal', 2.81, 3.10, 'Optimal'),
((SELECT id FROM assessments WHERE name = '20m Sprint'), '20m Sprint Sub-optimal', 3.11, 3.40, 'Sub-optimal'),
((SELECT id FROM assessments WHERE name = '20m Sprint'), '20m Sprint Poor', 3.41, NULL, 'Poor')
ON CONFLICT (assessment_id, name) DO NOTHING;

-- Pull Up
INSERT INTO benchmarks (assessment_id, name, min_value, max_value, classification) VALUES
((SELECT id FROM assessments WHERE name = 'Pull Up'), 'Pull Up Elite', 18.00, NULL, 'Elite'),
((SELECT id FROM assessments WHERE name = 'Pull Up'), 'Pull Up Optimal', 12.00, 17.99, 'Optimal'),
((SELECT id FROM assessments WHERE name = 'Pull Up'), 'Pull Up Sub-optimal', 6.00, 11.99, 'Sub-optimal'),
((SELECT id FROM assessments WHERE name = 'Pull Up'), 'Pull Up Poor', NULL, 5.99, 'Poor')
ON CONFLICT (assessment_id, name) DO NOTHING;

-- Trap Bar Deadlift
INSERT INTO benchmarks (assessment_id, name, min_value, max_value, classification) VALUES
((SELECT id FROM assessments WHERE name = 'Trap Bar Deadlift'), 'Trap Bar Deadlift Elite', 200.00, NULL, 'Elite'),
((SELECT id FROM assessments WHERE name = 'Trap Bar Deadlift'), 'Trap Bar Deadlift Optimal', 160.00, 199.99, 'Optimal'),
((SELECT id FROM assessments WHERE name = 'Trap Bar Deadlift'), 'Trap Bar Deadlift Sub-optimal', 120.00, 159.99, 'Sub-optimal'),
((SELECT id FROM assessments WHERE name = 'Trap Bar Deadlift'), 'Trap Bar Deadlift Poor', NULL, 119.99, 'Poor')
ON CONFLICT (assessment_id, name) DO NOTHING;

-- Rotational Med Ball Throw
INSERT INTO benchmarks (assessment_id, name, min_value, max_value, classification) VALUES
((SELECT id FROM assessments WHERE name = 'Rotational Med Ball Throw'), 'Rotational Med Ball Elite', 13.00, NULL, 'Elite'),
((SELECT id FROM assessments WHERE name = 'Rotational Med Ball Throw'), 'Rotational Med Ball Optimal', 11.00, 12.99, 'Optimal'),
((SELECT id FROM assessments WHERE name = 'Rotational Med Ball Throw'), 'Rotational Med Ball Sub-optimal', 9.00, 10.99, 'Sub-optimal'),
((SELECT id FROM assessments WHERE name = 'Rotational Med Ball Throw'), 'Rotational Med Ball Poor', NULL, 8.99, 'Poor')
ON CONFLICT (assessment_id, name) DO NOTHING;

-- -------------------------------------------------------------
-- 6. Seed Deficits (Power Deficit, Strength Deficit, Acceleration Deficit, Speed Deficit, Mobility Restriction)
-- -------------------------------------------------------------
INSERT INTO deficits (assessment_id, name, description) VALUES
(
    (SELECT id FROM assessments WHERE name = 'CMJ'), 
    'Power Deficit', 
    'Athlete is lacking lower body elastic force development and vertical power output.'
),
(
    (SELECT id FROM assessments WHERE name = 'Trap Bar Deadlift'), 
    'Strength Deficit', 
    'Athlete falls below absolute lower body force requirements.'
),
(
    (SELECT id FROM assessments WHERE name = '10m Sprint'), 
    'Acceleration Deficit', 
    'Athlete displays sub-optimal initial drive phase speeds.'
),
(
    (SELECT id FROM assessments WHERE name = '20m Sprint'), 
    'Speed Deficit', 
    'Athlete exhibits sub-optimal maximum linear running speeds.'
),
(
    (SELECT id FROM assessments WHERE name = 'Broad Jump'), 
    'Mobility Restriction', 
    'Athlete exhibits joint restriction limiting full triple extension dynamics.'
)
ON CONFLICT (name) DO UPDATE SET description = EXCLUDED.description;

-- -------------------------------------------------------------
-- 7. Map Deficits to S&C Training Methods
-- -------------------------------------------------------------
INSERT INTO deficit_training_methods (deficit_id, training_method_id) VALUES
-- Power Deficit mappings
((SELECT id FROM deficits WHERE name = 'Power Deficit'), (SELECT id FROM training_methods WHERE name = 'Dynamic Effort')),
((SELECT id FROM deficits WHERE name = 'Power Deficit'), (SELECT id FROM training_methods WHERE name = 'Plyometrics')),
((SELECT id FROM deficits WHERE name = 'Power Deficit'), (SELECT id FROM training_methods WHERE name = 'Rotational Power')),

-- Strength Deficit mappings
((SELECT id FROM deficits WHERE name = 'Strength Deficit'), (SELECT id FROM training_methods WHERE name = 'Max Strength')),

-- Acceleration Deficit mappings
((SELECT id FROM deficits WHERE name = 'Acceleration Deficit'), (SELECT id FROM training_methods WHERE name = 'Sprint Training')),
((SELECT id FROM deficits WHERE name = 'Acceleration Deficit'), (SELECT id FROM training_methods WHERE name = 'COD Training')),

-- Speed Deficit mappings
((SELECT id FROM deficits WHERE name = 'Speed Deficit'), (SELECT id FROM training_methods WHERE name = 'Sprint Training')),

-- Mobility Restriction mappings
((SELECT id FROM deficits WHERE name = 'Mobility Restriction'), (SELECT id FROM training_methods WHERE name = 'Mobility'))
ON CONFLICT DO NOTHING;

-- -------------------------------------------------------------
-- 8. Map Deficits to Corrective Movement Templates
-- -------------------------------------------------------------
INSERT INTO deficit_movement_templates (deficit_id, movement_template_id) VALUES
((SELECT id FROM deficits WHERE name = 'Power Deficit'), (SELECT id FROM movement_templates WHERE name = 'Lower Body Power')),
((SELECT id FROM deficits WHERE name = 'Power Deficit'), (SELECT id FROM movement_templates WHERE name = 'Rotational Power')),
((SELECT id FROM deficits WHERE name = 'Strength Deficit'), (SELECT id FROM movement_templates WHERE name = 'Lower Body Power')),
((SELECT id FROM deficits WHERE name = 'Acceleration Deficit'), (SELECT id FROM movement_templates WHERE name = 'Acceleration Development')),
((SELECT id FROM deficits WHERE name = 'Speed Deficit'), (SELECT id FROM movement_templates WHERE name = 'Acceleration Development')),
((SELECT id FROM deficits WHERE name = 'Mobility Restriction'), (SELECT id FROM movement_templates WHERE name = 'Shoulder Robustness'))
ON CONFLICT DO NOTHING;
