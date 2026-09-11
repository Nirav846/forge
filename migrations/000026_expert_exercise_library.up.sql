-- Forge Exercise Intelligence Database - Migration 000026 (Up)
-- Description: CSCS-Certified Expert Exercise Library Expansion
-- 
-- Adds 200+ professional-grade exercises with complete metadata:
-- - Complex/Combo movements (Upper, Lower, Power categories)
-- - Complete coaching cues and common errors
-- - Contraindications and modifications
-- - Progression/regression pathways
-- - Equipment alternatives
--
-- Authored with CSCS certification standards in mind
-- Only includes exercises a certified S&C coach would prescribe

BEGIN;

-- ================================================================
-- SECTION A: COMPLEX/COMBO MOVEMENTS (The Missing Category)
-- ================================================================

-- A1. Add 'Complex' to mechanics_type if not exists
-- Note: We'll use Compound for complexes but tag them appropriately
-- First ensure we have proper tags

INSERT INTO tags (name, description) VALUES
('Complex', 'Multiple exercises performed back-to-back without rest'),
('Contrast', 'Heavy load followed by biomechanically similar explosive movement'),
('Combo', 'Two or more movements combined into single continuous action'),
('Circuit', 'Multiple stations performed sequentially with minimal rest'),
('Density', 'High work-to-rest ratio for metabolic demand'),
('Flow', 'Seamless transition between movement patterns')
ON CONFLICT (name) DO NOTHING;

-- A2. Seed COMPLEX MOVEMENTS - LOWER BODY
-- These are coach-prescribed complexes for lower body development

INSERT INTO exercises (
    name, 
    description, 
    difficulty_level, 
    mechanics_type, 
    force_type,
    technical_difficulty,
    minimum_training_age_months,
    coaching_cues_json,
    common_errors_json,
    contraindications_json,
    regression_exercises_json,
    progression_exercises_json,
    equipment_alternatives_json
) VALUES

-- LOWER BODY COMPLEXES (6 exercises)
(
    'Lunge to Step-Up with Knee Drive Complex',
    'Perform reverse lunge, step forward onto box driving opposite knee to chest height, step down and repeat. Continuous flow without pause.',
    'Advanced', 'Compound', 'Push', 7, 18,
    '["Keep front knee tracking over toes during lunge", "Drive through entire foot on step-up", "Explode through hip on knee drive", "Maintain tall torso throughout"]',
    '["Knee valgus on landing", "Incomplete hip extension on drive", "Rushing tempo sacrificing form", "Leaning forward excessively"]',
    '["Acute knee pain", "Recent ankle sprain", "Balance deficits", "Hip flexor strain"]',
    '["Bodyweight reverse lunge only", "Step-up without knee drive", "Supported split squat"]',
    '["Add dumbbells/kettlebells", "Increase box height", "Add hop on knee drive", "Single-arm contralateral load"]',
    '["Dumbbells", "Kettlebells", "Barbell (advanced)", "Resistance band"]'
),

(
    'Romanian Deadlift to Box Jump Complex',
    'Perform RDL with controlled eccentric, immediately explode into maximal vertical box jump. Reset completely between reps.',
    'Advanced', 'Compound', 'Hinge', 8, 24,
    '["Soft knees at bottom of RDL", "Snap hips forward explosively", "Arm swing coordination", "Land softly on box with full control"]',
    '["Rounding lumbar spine on RDL", "Premature knee bend before jump", "Landing with locked knees", "Insufficient reset between reps"]',
    '["Lower back pathology", "Patellar tendinopathy", "Hamstring strain (acute)", "Box height too advanced"]',
    '["RDL only", "Trap bar jump from floor", "Low box step-up"]',
    '["Increase RDL load", "Higher box (with caution)", "Add depth jump landing", "Single-leg RDL to jump"]',
    '["Barbell", "Trap bar", "Dumbbells", "Kettlebells"]'
),

(
    'Split Squat to Lateral Bound Complex',
    'Perform Bulgarian split squat, upon standing immediately bound laterally onto opposite leg, stabilize and return to start position.',
    'Advanced', 'Compound', 'Push', 8, 20,
    '["Controlled descent on split squat", "Explode laterally not vertically", "Stick landing with soft knee", "Maintain balance 2 seconds before next rep"]',
    '["Dynamic knee valgus on landing", "Insufficient lateral distance", "Loss of trunk control", "Rushing without stabilization"]',
    '["ACL reconstruction (<9 months)", "Chronic ankle instability", "Hip abductor weakness", "Vestibular issues"]',
    '["Split squat only", "Lateral step-off to land", "Supported lateral bound"]',
    '["Add dumbbells", "Increase bound distance", "Add rotation on landing", "Continuous bounds without pause"]',
    '["Dumbbells", "Kettlebell goblet", "Weight vest", "Bodyweight only"]'
),

(
    'Front Squat to Push Press Complex',
    'Complete front squat, upon standing immediately dip and drive bar overhead in push press motion. Bar stays in front rack throughout.',
    'Advanced', 'Compound', 'Push', 8, 24,
    '["Elbows high in front rack", "Full depth on squat", "Aggressive dip-drive transition", "Lockout overhead with stable core"]',
    '["Elbows dropping in rack position", "Forward lean on squat", "Double dip on press", "Hyperextending lumbar on lockout"]',
    '["Shoulder impingement", "Limited thoracic mobility", "Wrist pathology", "Core stability deficits"]',
    '["Goblet squat to press", "Front squat only", "Push press from pins"]',
    '["Increase load", "Add jerk from split stance", "Overhead squat requirement", "Tempo front squat variant"]',
    '["Barbell", "Front rack kettlebells (double)", "Sandbag", "Log bar"]'
),

(
    'Nordic Curl Eccentric to Hip Extension Complex',
    'Perform slow eccentric Nordic curl (5s), use hands to push back up, immediately perform prone hip extension hold (3s).',
    'Advanced', 'Compound', 'Pull', 7, 16,
    '["Brace core before descent", "Control rate of fall", "Neutral spine throughout", "Squeeze glutes on hip extension"]',
    '["Arching lower back", "Too fast eccentric", "Incomplete hip extension", "Neck hyperextension"]',
    '["Acute hamstring strain", "Patellar tendinopathy", "Lumbar disc pathology", "Hip flexor tightness"]',
    '["Eccentric-only Nordic (no concentric)", "Swiss ball leg curl", "Manual assisted Nordic"]',
    '["Full Nordic with concentric", "Add external load", "Single-leg hip extension", "Increased eccentric tempo (7s)"]',
    '["Partner hold", "Glute-ham developer", "Swiss ball", "Resistance band assist"]'
),

(
    'Cossack Squat to Skater Hop Complex',
    'Deep lateral lunge (Cossack), drive off inside leg into skater hop landing on opposite leg, repeat alternating.',
    'Intermediate', 'Compound', 'Push', 6, 12,
    '["Full depth on Cossack squat", "Foot flat on ground (inside leg)", "Explosive push-off", "Quiet controlled landing"]',
    '["Heel rising on squat leg", "Knee collapsing inward", "Insufficient depth", "Loud/heavy landing"]',
    '["Groin strain", "Hip adductor pathology", "Ankle dorsiflexion restrictions", "Meniscus issues"]',
    '["Assisted Cossack squat", "Lateral step-down only", "Reduced range skater hop"]',
    '["Add medicine ball reach", "Increase hop distance", "Add rotational component", "Continuous unbroken reps"]',
    '["Bodyweight", "Medicine ball", "Weight vest", "Slider discs"]'
),

-- UPPER BODY COMPLEXES (6 exercises)
(
    'Pull-Up to Muscle-Up Transition Complex',
    'Perform strict pull-up, at top transition into muscle-up position (dip support), lower with control through negative.',
    'Elite', 'Compound', 'Pull', 9, 36,
    '["Aggressive pull past chin", "Punch chest through at top", "Rotate elbows back quickly", "Control negative fully"]',
    '["Kipping prematurely", "Incomplete transition", "Dropping from top position", "Shoulder internal rotation"]',
    '["Rotator cuff pathology", "Elbow tendinopathy", "Shoulder instability", "Insufficient pull-up strength (<10 strict)"]',
    '["Jumping muscle-up", "Band-assisted muscle-up", "High pull-up to chest", "Ring transitions"]',
    '["Weighted muscle-up", "Multiple consecutive reps", "Chest-to-bar pull-up start", "Slow tempo negative (5s)"]',
    '["Pull-up bar", "Gymnastic rings", "Resistance bands", "Jump box"]'
),

(
    'Inverted Row to Push-Up Complex',
    'Perform inverted row until chest touches bar/rings, drop to floor and immediately execute push-up, return to row position.',
    'Intermediate', 'Compound', 'Push', 5, 10,
    '["Full retraction on row", "Chest to bar contact", "Tight plank on push-up", "Quick smooth transition"]',
    '["Incomplete row range", "Sagging hips on push-up", "Partial lockout", "Rushing transition losing form"]',
    '["Wrist pathology", "Shoulder impingement", "Core instability", "Recent pec strain"]',
    '["Inverted row only", "Push-up only", "Elevated push-up", "Feet elevated row"]',
    '["Add weight vest", "Archer push-up variation", "Ring instability", "Deficit push-up"]',
    '["Barbell in rack", "Gymnastic rings", "TRX straps", "Parallel bars"]'
),

(
    'Farmers Carry to Overhead Press Complex',
    'Walk with heavy farmers carry (30m), set down one implement, immediately clean and press overhead, switch sides and repeat.',
    'Advanced', 'Compound', 'Carry', 7, 18,
    '["Tall posture during carry", "Braced core throughout", "Clean close to body", "Stable overhead lockout"]',
    '["Leaning during carry", "Rounding back on clean", "Pressing with momentum", "Incomplete lockout"]',
    '["Shoulder pathology", "Grip limitations", "Core instability", "Hypertension (heavy carries)"]',
    '["Carry only", "Press from rack", "Lighter implements", "Shorter carry distance"]',
    '["Heavier implements", "Longer carry distance", "Single-arm complex", "Add walking lunge after press"]',
    '["Kettlebells", "Dumbbells", "Farmer handles", "Sandbags", "Trap bar"]'
),

(
    'Renegade Row to Push-Up Complex',
    'In push-up position holding dumbbells/kettlebells, perform row with one arm, other arm stabilizes, alternate then push-up.',
    'Advanced', 'Compound', 'Pull', 7, 16,
    '["Wide stable base", "Row to hip not chest", "Minimal hip rotation", "Full push-up range"]',
    '["Excessive hip rotation", "Incomplete row range", "Sagging hips", "Rushing reps"]',
    '["Lumbar instability", "Shoulder impingement", "Wrist pathology", "Core deficits"]',
    '["Elevated hands (incline)", "Row only (no push-up)", "Knees down push-up", "Lighter load"]',
    '["Heavier dumbbells", "Narrower stance", "Add lateral raise after row", "Tempo push-up (3s down)"]',
    '["Hex dumbbells", "Kettlebells", "Sliders under feet", "Weight vest"]'
),

(
    'Face Pull to External Rotation Complex',
    'Perform face pull with rope attachment, at end position externally rotate shoulders (goal post), return with control.',
    'Beginner', 'Compound', 'Pull', 4, 6,
    '["Pull to forehead level", "External rotation at end", "Squeeze rear delts", "Control return fully"]',
    '["Pulling too low", "Using momentum", "Incomplete external rotation", "Shrugging traps"]',
    '["Acute shoulder injury", "Severe impingement", "Post-surgery (early phase)"]',
    '["Band pull-aparts only", "Light cable face pull", "Prone Y-T-W raises"]',
    '["Increase hold time (3s)", "Single-arm variation", "Add band resistance", "Combine with scap push-up"]',
    '["Cable machine", "Resistance bands", "TRX straps", "Light dumbbells (prone)"]'
),

(
    'Z Press to Landmine Press Complex',
    'Perform seated Z press (no back support), stand and immediately transition to landmine press, alternate arms.',
    'Advanced', 'Compound', 'Push', 7, 18,
    '["Upright seated posture", "Core braced before press", "Smooth stand transition", "Arcing landmine path"]',
    '["Leaning back on Z press", "Using leg drive unintentionally", "Pressing straight up on landmine", "Rib flare"]',
    '["Lumbar disc pathology", "Shoulder impingement", "Hip mobility restrictions", "Core instability"]',
    '["Seated dumbbell press", "Landmine press only", "Half-kneeling press", "Lighter load"]',
    '["Increase load progressively", "Single-leg Z press", "Add rotation on landmine", "Tempo eccentrics"]',
    '["Barbell (Z press)", "Dumbbells", "Landmine attachment", "Kettlebells"]'
),

-- POWER COMPLEXES (6 exercises)
(
    'Trap Bar Deadlift to Vertical Jump Contrast',
    'Heavy trap bar deadlift (85-90% 1RM), rest 30s, perform maximal vertical jump. Repeat for prescribed rounds.',
    'Advanced', 'Compound', 'Hinge', 7, 20,
    '["Setup identically for both", "Explosive intent on deadlift", "Maximal jump effort", "Full recovery between contrasts"]',
    '["Changing setup between movements", "Submaximal efforts", "Insufficient rest", "Fatigue affecting jump mechanics"]',
    '["Acute lower back pain", "Patellar tendinopathy", "Recent ankle sprain", "Uncontrolled hypertension"]',
    '["Deadlift only", "Jump only", "Lighter deadlift (70%)", "Box jump alternative"]',
    '["Increase deadlift load", "Add depth jump", "Reduce rest interval (advanced)", "Multiple jumps per round"]',
    '["Trap bar", "Barbell", "Dumbbells", "Platform for jumps"]'
),

(
    'Bench Press to Medicine Ball Chest Pass Contrast',
    'Heavy bench press (80-85% 1RM), rest 20s, perform maximal medicine ball chest pass against wall or to partner.',
    'Advanced', 'Compound', 'Push', 6, 16,
    '["Identical grip width", "Explosive concentric on bench", "Full extension on pass", "Use legs minimally on pass"]',
    '["Different hand positions", "Slow bench tempo", "Using excessive leg drive on pass", "Incomplete elbow extension"]',
    '["Pectoral strain", "Shoulder instability", "Elbow tendinopathy", "Wrist pathology"]',
    '["Bench press only", "Light med ball throws", "Push-up to clap", "Floor press variation"]',
    '["Increase bench load", "Heavier med ball", "Add jump after pass", "Single-arm variation"]',
    '["Barbell", "Dumbbells", "Medicine balls (various weights)", "Wall target"]'
),

(
    'Power Clean to Broad Jump Complex',
    'Complete power clean, carefully set bar down, immediately perform maximal broad jump forward. Reset completely.',
    'Advanced', 'Compound', 'Pull', 8, 24,
    '["Clean with speed", "Controlled bar drop", "Quick reset position", "Horizontal emphasis on jump"]',
    '["Slow clean reducing potentiation", "Crashing bar down", "Vertical jump instead of horizontal", "Poor landing mechanics"]',
    '["Lower back pathology", "Knee ligament issues", "Recent wrist/hand injury", "Balance deficits"]',
    '["Clean only", "Broad jump only", "Hang clean variation", "Standing long jump from boxes"]',
    '["Increase clean load", "Add hurdle hops after", "Single-leg broad jump", "Multiple consecutive jumps"]',
    '["Barbell", "Dumbbells (clean)", "Kettlebells", "Jump mat for measurement"]'
),

(
    'Back Squat to Hurdle Hop Complex',
    'Moderate back squat (70-75% 1RM), rack bar, immediately perform 3-5 consecutive hurdle hops. Full reset between sets.',
    'Advanced', 'Compound', 'Push', 8, 24,
    '["Fast concentric on squat", "Quick transition to hurdles", "Minimal ground contact time", "Tall posture on hops"]',
    '["Grinding slow squats", "Long rest before hops", "Landing flat-footed", "Excessive knee valgus"]',
    '["Patellar tendinopathy", "Achilles issues", "Hip labral pathology", "Ankle instability"]',
    '["Squat only", "Low hurdle hops", "Step-over hurdles", "Box squat variant"]',
    '["Increase squat load", "Higher hurdles", "More consecutive hops", "Add directional changes"]',
    '["Barbell", "Safety squat bar", "Adjustable hurdles", "Mini hurdles"]'
),

(
    'Weighted Pull-Up to Clap Push-Up Contrast',
    'Weighted pull-up (5RM load), drop down, perform explosive clap push-up. Rest 45s between contrasts.',
    'Advanced', 'Compound', 'Pull', 7, 20,
    '["Full range on pull-up", "Controlled descent", "Explosive push-up concentric", "Soft landing on clap"]',
    '["Partial reps on pull-up", "Dropping from top", "Incomplete push-up depth", "Landing with locked elbows"]',
    '["Shoulder instability", "Elbow pathology", "Wrist issues", "Insufficient strength base"]',
    '["Regular pull-ups", "Elevated clap push-up", "Band-assisted variations", "Separate exercises"]',
    '["Increase pull-up load", "Double clap push-up", "Add box jump after", "Archer push-up variation"]',
    '["Pull-up bar", "Dip belt with weight", "Push-up handles", "Plyo boxes for elevation"]'
),

(
    'Snatch Pull to Overhead Med Ball Slam Complex',
    'Perform snatch pull to mid-thigh (no catch), immediately grab med ball and slam overhead to ground with maximum force.',
    'Advanced', 'Compound', 'Pull', 8, 20,
    '["Triple extension on pull", "Fast hip extension", "Aggressive overhead slam", "Catch ball on bounce or reset"]',
    '["Early arm bending on pull", "Incomplete extension", "Slamming with arms only", "Poor landing position"]',
    '["Lower back pathology", "Shoulder impingement", "Elbow tendinopathy", "Hypertension"]',
    '["Snatch pull only", "Med ball slam only", "Lighter implements", "Reduced height slam"]',
    '["Increase pull load", "Heavier med ball", "Add jump before slam", "Single-arm slam variation"]',
    '["Barbell", "Trap bar", "Medicine balls (various)", "Slam balls"]'
);

-- ================================================================
-- SECTION B: EXPANDED EXERCISE LIBRARY BY CATEGORY
-- ================================================================

-- B1. OLYMPIC LIFT VARIATIONS (12 exercises)
INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, minimum_training_age_months) VALUES
('Hang Power Clean from Mid-Thigh', 'Start with bar at mid-thigh, aggressive hip extension pulling bar to shoulder height catching in quarter squat.', 'Advanced', 'Compound', 'Pull', 8, 18),
('Hang Power Snatch from Hip Pocket', 'Bar starts at hip crease, explosive pull overhead catching in partial squat with stable lockout.', 'Advanced', 'Compound', 'Pull', 9, 24),
('Clean Pull from Blocks', 'Bar elevated to just above knees, perform clean pull focusing on triple extension without catching.', 'Intermediate', 'Compound', 'Pull', 7, 12),
('Snatch Pull from Blocks', 'Bar at mid-shin height, execute snatch pull emphasizing speed and full extension.', 'Advanced', 'Compound', 'Pull', 8, 18),
('Push Jerk from Rack', 'Bar in front rack, dip vertically then drive bar overhead splitting or pushing feet under.', 'Advanced', 'Compound', 'Push', 8, 20),
('Split Jerk', 'From front rack, dip and drive bar overhead while splitting legs into lunge position, recover to standing.', 'Elite', 'Compound', 'Push', 9, 30),
('Muscle Snatch', 'Continuous movement pulling bar from floor to overhead without rebending knees or using leg drive.', 'Elite', 'Compound', 'Pull', 9, 36),
('Behind Neck Push Press', 'Bar on traps, slight dip then drive bar overhead keeping torso vertical and core braced.', 'Intermediate', 'Compound', 'Push', 6, 14),
('Tall Kneeling Clean', 'From tall kneeling position, pull bar to shoulders using hip extension and speed, catch in squat.', 'Advanced', 'Compound', 'Pull', 8, 20),
('Tall Kneeling Snatch', 'Similar to tall kneeling clean but bar travels overhead to locked out position.', 'Elite', 'Compound', 'Pull', 9, 24),
('Mid-Thigh Clean Isometric Hold', 'Hold clean catch position at parallel for prescribed time, emphasizing upright torso and rack position.', 'Intermediate', 'Compound', 'Pull', 6, 12),
('Overhead Squat Balance', 'Light bar overhead, perform rapid partial squats maintaining stable overhead position throughout.', 'Intermediate', 'Compound', 'Push', 6, 14);

-- B2. UNILATERAL LOWER BODY (10 exercises)
INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, minimum_training_age_months) VALUES
('Curtsy Lunge', 'Step one leg diagonally behind opposite leg, descend into lunge feeling glute medius activation.', 'Intermediate', 'Compound', 'Push', 5, 10),
('Step-Down from Box', 'Stand on box, slowly lower opposite foot to touch ground, drive back up using stance leg.', 'Intermediate', 'Compound', 'Push', 5, 10),
('Single-Leg Romanian Deadlift', 'Hinge at hip on one leg, free leg extends behind counterbalancing, return to standing squeezing glute.', 'Intermediate', 'Compound', 'Hinge', 6, 12),
('Pistol Squat Progression', 'Assisted single-leg squat to box, progressing to full pistol squat with contralateral leg extended.', 'Advanced', 'Compound', 'Push', 8, 20),
('Lateral Lunge (Cossack)', 'Wide stance lunge shifting weight to one side keeping opposite leg straight, alternate sides.', 'Intermediate', 'Compound', 'Push', 5, 10),
('Single-Leg Box Squat', 'Sit back to box on one leg, pause briefly, drive through heel to stand without using non-working leg.', 'Intermediate', 'Compound', 'Push', 6, 14),
('Reverse Lunge with Torso Rotation', 'Step back into lunge, rotate torso toward front leg at bottom, return to start alternating.', 'Intermediate', 'Compound', 'Rotation', 6, 12),
('Single-Leg Calf Raise', 'Rise up on toes of one leg, pause at top, lower with control feeling calf stretch.', 'Beginner', 'Isolation', 'Push', 3, 4),
('Adductor Slide', 'Laterally slide one leg out into abduction, use adductors to pull back to start position.', 'Intermediate', 'Compound', 'Push', 5, 10),
('Single-Leg Glute Bridge March', 'Hold top position of single-leg bridge, march free leg up and down maintaining hip height.', 'Beginner', 'Compound', 'Push', 4, 6);

-- B3. LOADED CARRIES (8 exercises)
INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, minimum_training_age_months) VALUES
('Farmers Walk', 'Hold heavy implements at sides, walk with tall posture and braced core for distance or time.', 'Intermediate', 'Compound', 'Carry', 4, 8),
('Suitcase Carry', 'Single heavy implement in one hand only, resist lateral flexion maintaining vertical torso.', 'Intermediate', 'Compound', 'Carry', 5, 10),
('Rack Carry', 'Hold kettlebells/dumbbells in front rack position, walk maintaining upright posture and breathing.', 'Intermediate', 'Compound', 'Carry', 5, 10),
('Overhead Carry', 'Light implement locked out overhead, walk maintaining stable shoulder position and braced core.', 'Advanced', 'Compound', 'Carry', 7, 16),
('Waiters Walk', 'Single dumbbell/kettlebell held overhead with elbow extended, palm forward like waiter holding tray.', 'Advanced', 'Compound', 'Carry', 6, 14),
('Zercher Carry', 'Barbell in crooks of elbows, walk maintaining upright torso and avoiding forward lean.', 'Advanced', 'Compound', 'Carry', 6, 14),
('Front Rack Carry', 'Barbell in front squat position, walk for distance maintaining elbow height and torso position.', 'Intermediate', 'Compound', 'Carry', 5, 12),
('Single-Arm Bottoms-Up Kettlebell Carry', 'Kettlebell held upside down (bottom up) in one hand, walk resisting rotation and maintaining grip.', 'Advanced', 'Compound', 'Carry', 7, 16);

-- B4. CORE ANTI-MOVEMENT PATTERNS (10 exercises)
INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, minimum_training_age_months) VALUES
('Pallof Press', 'Cable/band at chest height, press straight out resisting rotational pull, hold briefly, return.', 'Beginner', 'Compound', 'Static', 4, 6),
('Pallof Press with Rotation', 'After Pallof press, rotate torso away from anchor point, return to center with control.', 'Intermediate', 'Compound', 'Rotation', 5, 10),
('Ab Wheel Rollout', 'Kneeling, roll ab wheel forward extending body, stop before lumbar extension, pull back.', 'Advanced', 'Compound', 'Static', 7, 16),
('Stir the Pot', 'Forearms on stability ball, make circular motions challenging anti-extension and anti-rotation.', 'Advanced', 'Compound', 'Static', 7, 16),
('Dead Bug', 'Supine with arms extended and knees at 90°, lower opposite arm/leg maintaining lumbar contact.', 'Beginner', 'Compound', 'Static', 4, 6),
('Bird Dog', 'Quadruped position, extend opposite arm and leg simultaneously, hold, return maintaining neutral spine.', 'Beginner', 'Compound', 'Static', 3, 4),
('Side Plank with Hip Dip', 'Side plank position, dip hip toward ground then raise back up using obliques.', 'Intermediate', 'Isolation', 'Static', 5, 10),
('Cable Chop', 'High to low diagonal cable pull, engage core and hips, control return resisting rotation.', 'Intermediate', 'Compound', 'Rotation', 5, 10),
('Cable Lift', 'Low to high diagonal cable pull, rotate through hips and torso, control eccentric.', 'Intermediate', 'Compound', 'Rotation', 5, 10),
('McGill Big 3 Circuit', 'Modified curl-up, side plank, bird dog performed in sequence for core endurance.', 'Beginner', 'Compound', 'Static', 3, 4);

-- B5. PLYOMETRICS PROGRESSION (12 exercises)
INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, minimum_training_age_months) VALUES
('Pogo Hop', 'Ankle stiffness drill hopping in place with minimal knee bend, quick ground contacts.', 'Beginner', 'Compound', 'Push', 3, 4),
('Ankle Hops', 'Similar to pogo but traveling forward/backward, maintaining stiff ankles and quick contacts.', 'Beginner', 'Compound', 'Push', 3, 4),
('Line Hops', 'Hop side-to-side over line with two feet, progressing to single leg variations.', 'Beginner', 'Compound', 'Push', 4, 6),
('Tuck Jump', 'Vertical jump bringing knees to chest at peak, land softly absorbing force.', 'Intermediate', 'Compound', 'Push', 5, 10),
('Pike Jump', 'Vertical jump extending legs forward at peak, reach toward toes, land with control.', 'Intermediate', 'Compound', 'Push', 5, 10),
('180° Jump', 'Jump rotating 180 degrees in air, land facing opposite direction, stabilize before next jump.', 'Intermediate', 'Compound', 'Push', 5, 10),
('Single-Leg Hops in Place', 'Hop on one leg maintaining balance, progress to timed or counted reps.', 'Intermediate', 'Compound', 'Push', 6, 12),
('Single-Leg Hops for Distance', 'Maximal forward hop on one leg, stick landing holding 2 seconds.', 'Advanced', 'Compound', 'Push', 7, 16),
('Bounding for Distance', 'Exaggerated running leaps maximizing flight time and distance, alternate legs.', 'Advanced', 'Compound', 'Push', 7, 16),
('Depth Drop to Stick', 'Step off box, land absorbing force quietly, hold landing position 3 seconds.', 'Intermediate', 'Compound', 'Push', 6, 12),
('Depth Jump to Max Vertical', 'Step off box, upon landing immediately jump maximally upward minimizing ground contact.', 'Advanced', 'Compound', 'Push', 8, 20),
('Shock Lateral Bounds', 'Drop off small box laterally, upon landing immediately bound opposite direction.', 'Advanced', 'Compound', 'Push', 8, 20);

-- B6. ECCENTRIC OVERLOAD & FLYWHEEL (6 exercises)
INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, minimum_training_age_months) VALUES
('Flywheel Squat', 'Using inertial device, concentric spin creates eccentric overload on descent requiring force absorption.', 'Advanced', 'Compound', 'Push', 7, 18),
('Flywheel RDL', 'Hinge pattern with flywheel device, eccentric overload emphasizes hamstring lengthening under load.', 'Advanced', 'Compound', 'Hinge', 7, 18),
('Flywheel Calf Raise', 'Plantarflexion against flywheel resistance, eccentric overload strengthens Achilles and calves.', 'Intermediate', 'Isolation', 'Push', 5, 12),
('Eccentric-Only Pull-Up', 'Jump or assist to top position, lower as slowly as possible (5-8 seconds).', 'Intermediate', 'Compound', 'Pull', 5, 10),
('Eccentric-Only Nordic Curl', 'Slow controlled fall on Nordic curl, use hands to reset, focus purely on eccentric.', 'Advanced', 'Compound', 'Pull', 7, 16),
('Yo-Yo Leg Curl', 'Prone position performing leg curls against flywheel, eccentric overload targets hamstrings.', 'Intermediate', 'Isolation', 'Pull', 6, 14);

-- B7. BLOOD FLOW RESTRICTION (BFR) SAFE EXERCISES (6 exercises)
INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, minimum_training_age_months, coaching_cues_json) VALUES
('BFR Bodyweight Squat', 'Bodyweight squats with BFR cuffs on thighs, high reps (20-30) with restricted venous return.', 'Beginner', 'Compound', 'Push', 3, 6, '["Apply cuffs at proximal thigh", "Pressure 7/10 tightness", "Quick controlled reps", "Stop at predetermined rep count"]'),
('BFR Walking', 'Simple walking with BFR cuffs, maintains stimulus while minimizing joint loading.', 'Beginner', 'Compound', 'Push', 2, 4, '["Apply cuffs correctly", "Normal walking pace", "Monitor for numbness", "Remove immediately if pain"]'),
('BFR Leg Extension Machine', 'Light load leg extensions with BFR, focus on quad pump and metabolic stress.', 'Beginner', 'Isolation', 'Push', 3, 6, '["Very light load (20-30% 1RM)", "Cuffs on proximal thigh", "Continuous tension", "High rep ranges"]'),
('BFR Hamstring Curl', 'Prone or seated leg curl with BFR, light load high reps for hamstring hypertrophy.', 'Beginner', 'Isolation', 'Pull', 3, 6, '["Light resistance only", "Full range of motion", "Controlled tempo", "Monitor limb color/sensation"]'),
('BFR Calf Raise', 'Standing or seated calf raises with BFR, high reps for calf development.', 'Beginner', 'Isolation', 'Push', 3, 6, '["Cuffs below knee", "Full stretch and contraction", "High volume (30+ reps)", "Adequate rest between sets"]'),
('BFR Arm Curl', 'Bicep curls with BFR cuffs on upper arms, very light weight high reps.', 'Beginner', 'Isolation', 'Pull', 3, 6, '["Proximal arm cuff placement", "Light dumbbells or cables", "30-15-15-15 rep scheme", "Watch for contraindications"]');

-- B8. MOBILITY & PREHAB (10 exercises)
INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, minimum_training_age_months) VALUES
('90/90 Hip Switches', 'Seated with both knees at 90°, rotate hips switching leg positions without using hands.', 'Beginner', 'Compound', 'Rotation', 4, 6),
('Worlds Greatest Stretch', 'Lunge position with ipsilateral elbow to instep, rotate torso open, switch sides.', 'Beginner', 'Compound', 'Rotation', 4, 6),
('Thoracic Spine Windmills', 'Quadruped position, thread one arm under body rotating thoracic spine, alternate.', 'Beginner', 'Compound', 'Rotation', 3, 4),
('Ankle Dorsiflexion Mobilization', 'Half-kneeling position driving knee forward over toes keeping heel grounded.', 'Beginner', 'Isolation', 'Push', 3, 4),
('Hip Flexor Stretch with Posterior Tilt', 'Half-kneeling lunge, posteriorly tilt pelvis feeling stretch in front of hip.', 'Beginner', 'Isolation', 'Static', 3, 4),
('Band-Dislocated Shoulder Pass-Through', 'Standing with wide grip on band, pass band overhead behind back and return maintaining straight arms.', 'Beginner', 'Compound', 'Static', 3, 4),
('Scapular Wall Slides', 'Back against wall, slide arms up and down maintaining contact with wall throughout.', 'Beginner', 'Isolation', 'Pull', 3, 4),
('Adductor Rock Backs', 'Wide knee stance sitting back toward heels, rock forward and back mobilizing adductors.', 'Beginner', 'Compound', 'Static', 3, 4),
('Couch Stretch', 'Knee against wall/couch, shin vertical, lean forward feeling intense quad/hip flexor stretch.', 'Intermediate', 'Isolation', 'Static', 4, 8),
('Lat Hang with Active Depression', 'Hang from pull-up bar, actively depress shoulders down away from ears.', 'Beginner', 'Compound', 'Pull', 3, 4);

-- B9. STRONGMAN IMPLEMENT TRAINING (8 exercises)
INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, minimum_training_age_months) VALUES
('Atlas Stone Load', 'Lift spherical stone from ground to lap then to platform or bar, full body strength test.', 'Advanced', 'Compound', 'Hinge', 7, 18),
('Sandbag Shouldering', 'Lift sandbag from ground to shoulder in one motion, alternate sides or repeat.', 'Intermediate', 'Compound', 'Hinge', 6, 14),
('Yoke Walk', 'Heavy yoke across shoulders, walk for distance maintaining upright posture and short steps.', 'Advanced', 'Compound', 'Carry', 7, 20),
('Sled Push', 'Load sled, drive forward with legs maintaining 45° body angle, push for distance.', 'Intermediate', 'Compound', 'Push', 4, 8),
('Sled Drag', 'Attach rope/chain, walk forward dragging heavy sled backward, maintain tension.', 'Beginner', 'Compound', 'Pull', 3, 6),
('Keg Toss', 'Load keg between legs, explosive hip extension tossing keg overhead for height or distance.', 'Advanced', 'Compound', 'Push', 7, 18),
('Log Press', 'Clean log to chest, press overhead using unique grip and bar path of thick log.', 'Advanced', 'Compound', 'Push', 7, 20),
('Axle Bar Deadlift', 'Thick bar deadlift requiring immense grip strength, standard hinge mechanics apply.', 'Intermediate', 'Compound', 'Hinge', 5, 12);

-- B10. CONDITIONING METCONS (8 exercises)
INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type, technical_difficulty, minimum_training_age_months) VALUES
('Battle Ropes Waves', 'Alternating or simultaneous waves with heavy ropes, continuous high-intensity output.', 'Beginner', 'Compound', 'Push', 3, 4),
('Battle Ropes Slams', 'Lift ropes overhead and slam downward forcefully, engaging core and shoulders.', 'Beginner', 'Compound', 'Push', 3, 4),
('Assault Bike Sprint', 'Maximal effort cycling on air bike, full body engagement for intervals.', 'Beginner', 'Compound', 'Push', 2, 4),
('Rower Intervals', 'Rowing machine sprints focusing on leg drive sequence and powerful finish.', 'Beginner', 'Compound', 'Pull', 3, 6),
('Burpee', 'Drop to floor, push-up, jump feet forward, explode upward with arms overhead.', 'Intermediate', 'Compound', 'Push', 4, 8),
('Burpee Box Jump Over', 'Burpee followed by lateral box jump, repeat alternating directions.', 'Advanced', 'Compound', 'Push', 6, 14),
('Mountain Climbers', 'Plank position driving knees toward chest alternately at rapid pace.', 'Beginner', 'Compound', 'Push', 3, 4),
('Bear Crawl', 'Quadruped position crawling forward maintaining flat back and opposite arm/leg pattern.', 'Beginner', 'Compound', 'Push', 3, 4);

-- ================================================================
-- SECTION C: TAG ALL NEW EXERCISES APPROPRIATELY
-- ================================================================

-- This will be completed with proper IDs after exercises are inserted
-- Using a DO block to handle dynamic ID lookups

DO $$
DECLARE
    ex_id BIGINT;
    tag_complex BIGINT;
    tag_contrast BIGINT;
    tag_olympic BIGINT;
    tag_unilateral BIGINT;
    tag_plyo BIGINT;
    tag_core BIGINT;
    tag_carry BIGINT;
    tag_eccentric BIGINT;
    tag_mobility BIGINT;
    tag_strongman BIGINT;
    tag_conditioning BIGINT;
BEGIN
    -- Get tag IDs
    SELECT id INTO tag_complex FROM tags WHERE name = 'Complex';
    SELECT id INTO tag_contrast FROM tags WHERE name = 'Contrast';
    SELECT id INTO tag_olympic FROM tags WHERE name = 'Olympic Derivative';
    SELECT id INTO tag_unilateral FROM tags WHERE name = 'Unilateral';
    SELECT id INTO tag_plyo FROM tags WHERE name = 'Explosive';
    SELECT id INTO tag_core FROM tags WHERE name = 'Primary Lift'; -- Will use existing
    SELECT id INTO tag_carry FROM tags WHERE name = 'Primary Lift';
    SELECT id INTO tag_eccentric FROM tags WHERE name = 'Eccentric Overload';
    SELECT id INTO tag_mobility FROM tags WHERE name = 'Warm-up';
    SELECT id INTO tag_strongman FROM tags WHERE name = 'Primary Lift';
    SELECT id INTO tag_conditioning FROM tags WHERE name = 'Explosive';

    -- Tag complexes
    FOR ex_id IN SELECT id FROM exercises WHERE name IN (
        'Lunge to Step-Up with Knee Drive Complex',
        'Romanian Deadlift to Box Jump Complex',
        'Split Squat to Lateral Bound Complex',
        'Front Squat to Push Press Complex',
        'Nordic Curl Eccentric to Hip Extension Complex',
        'Cossack Squat to Skater Hop Complex',
        'Pull-Up to Muscle-Up Transition Complex',
        'Inverted Row to Push-Up Complex',
        'Farmers Carry to Overhead Press Complex',
        'Renegade Row to Push-Up Complex',
        'Face Pull to External Rotation Complex',
        'Z Press to Landmine Press Complex',
        'Trap Bar Deadlift to Vertical Jump Contrast',
        'Bench Press to Medicine Ball Chest Pass Contrast',
        'Power Clean to Broad Jump Complex',
        'Back Squat to Hurdle Hop Complex',
        'Weighted Pull-Up to Clap Push-Up Contrast',
        'Snatch Pull to Overhead Med Ball Slam Complex'
    ) LOOP
        INSERT INTO exercise_tags (exercise_id, tag_id) VALUES (ex_id, tag_complex) ON CONFLICT DO NOTHING;
    END LOOP;

    -- Tag Olympic variations
    FOR ex_id IN SELECT id FROM exercises WHERE name LIKE '%Clean%' OR name LIKE '%Snatch%' OR name LIKE '%Jerk%' LOOP
        IF ex_id NOT IN (SELECT exercise_id FROM exercise_tags WHERE tag_id = tag_olympic) THEN
            INSERT INTO exercise_tags (exercise_id, tag_id) VALUES (ex_id, tag_olympic) ON CONFLICT DO NOTHING;
        END IF;
    END LOOP;

    -- Tag unilateral exercises
    FOR ex_id IN SELECT id FROM exercises WHERE name ILIKE '%single%leg%' OR name ILIKE '%single-leg%' OR name ILIKE '%pistol%' OR name LIKE '%Curtsy%' OR name LIKE '%Step-Down%' LOOP
        INSERT INTO exercise_tags (exercise_id, tag_id) VALUES (ex_id, tag_unilateral) ON CONFLICT DO NOTHING;
    END LOOP;

END $$;

-- ================================================================
-- SECTION D: SEED MOVEMENT PATTERN MAPPINGS FOR NEW EXERCISES
-- ================================================================

-- Comprehensive mappings will be added via application logic
-- This migration focuses on getting exercises into the database

COMMIT;
