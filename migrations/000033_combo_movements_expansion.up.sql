-- Forge Exercise Intelligence Database - Migration 000033 (Up)
-- Description: COMBO MOVEMENTS LIBRARY EXPANSION
-- 
-- Adds 35+ professional-grade Combo exercises with complete metadata:
-- - Upper Body Combos (12 exercises)
-- - Lower Body Combos (12 exercises)
-- - Power/Full Body Combos (11 exercises)
-- - Complete coaching cues and common errors
-- - Contraindications and modifications
-- - Progression/regression pathways
-- - Equipment alternatives
--
-- Authored with CSCS certification standards in mind
-- Differentiates Combo (continuous single action) from Complex (back-to-back without rest)

BEGIN;

-- ================================================================
-- SECTION A: VERIFY TAGS EXIST
-- ================================================================

-- Ensure Combo tag exists (should already exist from migration 000026)
INSERT INTO tags (name, description) VALUES
('Combo', 'Two or more movements combined into single continuous action')
ON CONFLICT (name) DO NOTHING;

-- ================================================================
-- SECTION B: UPPER BODY COMBOS (12 exercises)
-- ================================================================

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

-- UPPER BODY COMBOS
(
    'Pull-Up to Push-Up Combo',
    'Perform pull-up, immediately transition to floor for push-up without pause. Continuous flow between upper body pull and push patterns.',
    'Advanced', 'Compound', 'Pull-Push', 7, 18,
    '["Full hang to chin over bar on pull-up", "Quick controlled drop to floor", "Hands directly under shoulders for push-up", "Maintain rigid plank throughout"]',
    '["Incomplete range on pull-up", "Sagging hips on push-up", "Rushing transition losing form", "Flaring elbows excessively"]',
    '["Shoulder impingement", "Rotator cuff pathology", "Wrist pain", "Inability to perform strict pull-up"]',
    '["Band-assisted pull-up + knee push-up", "Inverted row + incline push-up", "Lat pulldown + push-up"]',
    '["Add weight vest", "Archer pull-up to archer push-up", "Muscle-up transition variant", "Clapping push-up finish"]',
    '["Pull-up bar + floor", "Gymnastic rings", "TRX suspension trainer", "Resistance bands"]'
),

(
    'Inverted Row to Pike Push-Up Combo',
    'Complete inverted row bringing chest to bar, walk feet forward and transition into pike push-up targeting shoulders.',
    'Advanced', 'Compound', 'Pull-Push', 7, 20,
    '["Chest to bar on row", "Walk feet forward smoothly", "Hips high in pike position", "Lower head toward floor between hands"]',
    '["Incomplete row contraction", "Hips sagging in pike", "Neck craning instead of shoulder flexion", "Feet too close reducing difficulty"]',
    '["Shoulder instability", "Lumbar spine issues", "Wrist limitations", "Poor core control"]',
    '["Knee pike push-up only", "Standard inverted row only", "Wall handstand hold progression"]',
    '["Elevate feet on box", "Add tempo pauses", "Handstand push-up progression", "Ring variant"]',
    '["Barbell in rack", "Gymnastic rings", "TRX straps", "Smith machine bar"]'
),

(
    'Face Pull to External Rotation Combo',
    'Perform face pull bringing rope to forehead, immediately transition to external rotation hold at 90 degrees abduction.',
    'Intermediate', 'Isolation', 'Pull', 5, 12,
    '["Pull rope toward forehead with elbows high", "Externally rotate shoulders at end range", "Squeeze rear delts and external rotators", "Control return to start"]',
    '["Using momentum instead of control", "Elbows dropping below shoulders", "Incomplete external rotation", "Shrugging traps excessively"]',
    '["Acute shoulder dislocation", "Severe rotator cuff tear", "Post-surgical shoulder (<6 months)"]',
    '["Band pull-aparts only", "Cable external rotation isolated", "Prone Y-T-W raises"]',
    '["Increase resistance", "Add isometric hold 3-5 seconds", "Single-arm variant", "Add internal rotation return"]',
    '["Cable machine with rope", "Resistance band", "Theraband", "Light dumbbells prone"]'
),

(
    'Chin-Up to Dip Combo',
    'Complete chin-up, dismount and immediately perform parallel bar dip. Alternating vertical pull and vertical push.',
    'Advanced', 'Compound', 'Pull-Push', 8, 24,
    '["Full chin-up with supinated grip", "Quick controlled dismount", "Shoulders depressed before dip descent", "Full lockout at top of dip"]',
    '["Half reps on either movement", "Forward lean excessive on dip", "Swinging to generate momentum", "Incomplete elbow extension"]',
    '["Elbow tendinopathy", "Shoulder anterior instability", "Wrist pathology", "Sternum pain"]',
    '["Band-assisted chin-up + bench dip", "Lat pulldown + push-up", "Negative-only training"]',
    '["Weighted chin-up to weighted dip", "Archer chin-up variant", "Ring dip addition", "Muscle-up as alternative"]',
    '["Pull-up bar + dip station", "Power tower", "Gymnastic rings", "Parallel bars"]'
),

(
    'Renegade Row to Push-Up Combo',
    'In plank position with dumbbells, perform single-arm row, return to center, execute push-up, repeat opposite arm.',
    'Advanced', 'Compound', 'Pull-Push', 7, 18,
    '["Solid plank position throughout", "Row elbow close to body", "Return dumbbell with control", "Push-up with full range"]',
    '["Hips rotating during row", "Incomplete push-up depth", "Rushing compromising stability", "Holding breath throughout"]',
    '["Lumbar instability", "Wrist pain", "Shoulder impingement", "Core weakness"]',
    '["Knee plank row + knee push-up", "Standard row + standard push-up separate", "Plank hold + row only"]',
    '["Heavier dumbbells", "Add pause at bottom", "Continuous alternating without pause", "Feet elevated variant"]',
    '["Hex dumbbells", "Kettlebells", "Resistance bands anchored", "Slider discs"]'
),

(
    'Z Press to Landmine Press Combo',
    'Seated Z press with dumbbells overhead, stand and immediately transition to landmine press with same implement.',
    'Advanced', 'Compound', 'Push', 8, 24,
    '["Sit tall with legs extended", "Press dumbbells strictly overhead", "Stand smoothly maintaining position", "Drive landmine press with leg drive"]',
    '["Leaning back in Z press", "Incomplete lockout", "Rushing transition", "Using too much leg drive on landmine portion"]',
    '["Lumbar disc pathology", "Shoulder impingement", "Hamstring tightness limiting Z position", "Hip mobility restrictions"]',
    '["Seated dumbbell press only", "Standing landmine press only", "Half-kneeling press progression"]',
    '["Increase load", "Add tempo variations", "Single-arm landmine press", "Add rotation element"]',
    '["Dumbbells + landmine attachment", "Kettlebells", "Barbell + landmine", "Sandbag"]'
),

(
    'Farmer Carry to Overhead Press Combo',
    'Carry heavy implements for distance, immediately rack and press overhead without rest.',
    'Intermediate', 'Compound', 'Push', 6, 15,
    '["Tall posture during carry", "Brace core against load", "Clean to rack position efficiently", "Strict press to lockout"]',
    '["Leaning during carry", "Incomplete overhead lockout", "Using momentum on press", "Dropping implements unsafely"]',
    '["Shoulder instability", "Lumbar compression issues", "Grip pathology", "Overhead mobility restrictions"]',
    '["Lighter carry + separate press", "Suitcase carry only", "Seated dumbbell press only"]',
    '["Heavier implements", "Longer carry distance", "Single-arm variant", "Walking overhead press"]',
    '["Kettlebells", "Dumbbells", "Farmer handles", "Trap bar"]'
),

(
    'Battle Rope Slam to Burpee Combo',
    'Perform alternating battle rope slams for time, immediately drop into burpee and jump, return to ropes.',
    'Advanced', 'Metabolic', 'Push-Pull', 6, 15,
    '["Aggressive rope slams using hips", "Quick transition to burpee", "Full extension on jump", "Immediate return to rope rhythm"]',
    '["Using only arms on ropes", "Incomplete burpee extension", "Landing stiff-legged", "Loss of rope tempo"]',
    '["Lower back acute pain", "Wrist issues", "Cardiovascular limitations", "Shoulder pathology"]',
    '["Rope slams only", "Step-back burpee", "Separate movements with rest"]',
    '["Heavier ropes", "Longer work intervals", "Add push-up to burpee", "Tuck jump variation"]',
    '["Battle ropes", "Heavy ropes", "Slam balls alternative", "Medicine ball throws"]'
),

(
    'Medicine Ball Scoop Toss to Push-Up Combo',
    'Perform scoop toss for distance, sprint to retrieve, return and immediately execute push-ups.',
    'Intermediate', 'Power', 'Push', 5, 12,
    '["Triple extension on toss", "Aggressive sprint retrieval", "Quick transition to push-up position", "Maintain push-up quality when fatigued"]',
    '["Incomplete extension on toss", "Slow retrieval reducing intensity", "Sagging hips on push-up", "Poor pacing"]',
    '["Shoulder pathology", "Ankle/knee issues for sprinting", "Lower back pain", "Wrist limitations"]',
    '["Stationary toss only", "Walk retrieval", "Incline push-up variant"]',
    '["Heavier ball", "Longer sprint distance", "Add clap push-up", "Continuous circuit format"]',
    '["Medicine ball 4-6kg", "Slam ball", "Weighted implement", "Sandbag"]'
),

(
    'Band Pull-Apart to Push-Up Combo',
    'Perform band pull-apart for scapular activation, immediately drop and execute push-up set.',
    'Intermediate', 'Compound', 'Pull-Push', 4, 10,
    '["Squeeze shoulder blades on pull-apart", "Control eccentric return", "Quick transition to push-up", "Full range push-up execution"]',
    '["Using momentum on pull-apart", "Incomplete scapular retraction", "Rushing push-up descent", "Partial lockout"]',
    '["Shoulder instability", "Wrist pain", "Pectoral strain", "Band snap risk (check integrity)"]',
    '["Lighter band resistance", "Wall push-up", "Separate movements initially"]',
    '["Heavier band", "Add pause on pull-apart", "Decline push-up", "Continuous flow without pause"]',
    '["Resistance band", "Theraband", "Cable machine", "Light dumbbells reverse fly"]'
),

(
    'TRX Row to TRX Push-Up Combo',
    'Complete TRX inverted row, flip body position without releasing straps, perform TRX push-up.',
    'Advanced', 'Compound', 'Pull-Push', 6, 15,
    '["Full body tension on row", "Smooth transition flipping position", "Maintain plank on push-up", "Control instability throughout"]',
    '["Losing tension during transition", "Incomplete row range", "Hips sagging on push-up", "Grip slipping on handles"]',
    '["Shoulder instability", "Core weakness", "Grip limitations", "Recent shoulder surgery"]',
    '["Row only initially", "Separate push-up training", "Feet closer for easier variant"]',
    '["Single-arm row to push-up", "Add pistol squat between sets", "Archer push-up variant", "Feet elevated"]',
    '["TRX suspension trainer", "Gymnastic rings", "Resistance bands anchored", "Slider system"]'
),

(
    'Kettlebell Clean to Rack Hold to Press Combo',
    'Clean kettlebell to rack position, hold for stability, then press overhead. Can be performed as continuous flow.',
    'Intermediate', 'Compound', 'Push', 5, 12,
    '["Explosive hip drive on clean", "Soft catch in rack position", "Stable rack before pressing", "Vertical press path to lockout"]',
    '["Banging forearm excessively", "Rack position too low", "Pressing before stable", "Leaning back on press"]',
    '["Wrist pathology", "Shoulder impingement", "Elbow tendinopathy", "Limited thoracic mobility"]',
    '["Dead stop clean", "Rack hold only", "Floor press progression"]',
    '["Heavier kettlebell", "Double kettlebell", "Add squat before clean", "Jerk finish"]',
    '["Kettlebell", "Dumbbell", "Barbell", "Sandbag"]'
);

-- ================================================================
-- SECTION C: LOWER BODY COMBOS (12 exercises)
-- ================================================================

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

-- LOWER BODY COMBOS
(
    'Curtsy to Reverse Lunge Combo',
    'Step back and across into curtsy lunge, return to center and immediately step straight back into reverse lunge. Continuous alternating flow.',
    'Intermediate', 'Compound', 'Push', 5, 12,
    '["Cross leg behind on curtsy", "Lower until both knees at 90 degrees", "Return to center smoothly", "Step straight back for reverse lunge"]',
    '["Knee collapsing inward on curtsy", "Incomplete depth", "Rushing compromising balance", "Trunk leaning excessively"]',
    '["IT band syndrome", "Patellofemoral pain", "Hip labral issues", "Balance deficits"]',
    '["Supported curtsy only", "Reverse lunge only", "Bodyweight squat progression"]',
    '["Add dumbbells", "Increase range of motion", "Add hop transition", "Continuous without pause"]',
    '["Dumbbells", "Kettlebell goblet", "Bodyweight", "Smith machine"]'
),

(
    'Lateral Lunge to Skater Hop Combo',
    'Perform lateral lunge to side, explode into skater hop landing on opposite leg, immediately lateral lunge other direction.',
    'Advanced', 'Compound', 'Push', 7, 18,
    '["Deep lateral lunge with foot flat", "Explode through entire foot", "Land softly on opposite leg", "Immediately sink into next lunge"]',
    '["Dynamic knee valgus", "Insufficient lateral distance", "Landing with locked knee", "Loss of trunk control"]',
    '["ACL reconstruction <9 months", "Chronic ankle instability", "Hip abductor weakness", "Vestibular issues"]',
    '["Lateral lunge only", "Skater hop without lunge", "Supported lateral step-off"]',
    '["Add distance on hop", "Continuous bounds", "Add reach to ground", "Weighted vest"]',
    '["Bodyweight", "Dumbbells", "Weight vest", "Resistance band"]'
),

(
    'Step-Up to Knee Drive Combo',
    'Step onto box driving through lead leg, at top explosively drive opposite knee to chest height, step down controlled.',
    'Intermediate', 'Compound', 'Push', 5, 12,
    '["Entire foot on box", "Drive through heel not toes", "Explode knee drive from hip", "Control eccentric step-down"]',
    '["Pushing off trailing leg", "Incomplete knee drive height", "Rushing descent", "Leaning forward excessively"]',
    '["Knee pathology", "Hip flexor strain", "Ankle dorsiflexion restriction", "Balance deficits"]',
    '["Lower box height", "Step-up only", "Supported knee raise"]',
    '["Higher box", "Add dumbbells", "Add hop on knee drive", "Continuous without touch-down"]',
    '["Box/platform", "Bench", "Stairs", "Dumbbells for load"]'
),

(
    'Cossack Squat to Skater Hop Combo',
    'Descend into deep Cossack squat to one side, explode up and laterally into skater hop landing on opposite leg.',
    'Advanced', 'Compound', 'Push', 7, 20,
    '["Deep squat with one leg extended", "Drive through entire foot", "Explode laterally not vertically", "Stick landing 2 seconds"]',
    '["Heel lifting on squat leg", "Incomplete depth", "Landing with knee valgus", "Rushing without stabilization"]',
    '["Adductor strain", "Hip mobility restrictions", "Ankle instability", "Knee meniscus issues"]',
    '["Cossack squat to box", "Skater hops only", "Supported lateral lunge"]',
    '["Add reach to ground", "Continuous bounds", "Weighted Cossack", "Increase hop distance"]',
    '["Bodyweight", "Kettlebell counterbalance", "Dumbbell", "Weight vest"]'
),

(
    'Bulgarian Split Squat to Broad Jump Combo',
    'Complete Bulgarian split squat, upon standing explode forward into maximal broad jump, reset and repeat.',
    'Advanced', 'Compound', 'Push', 8, 24,
    '["Controlled descent on split squat", "Drive through front foot", "Explode forward on jump", "Land softly absorbing impact"]',
    '["Front knee collapsing", "Incomplete squat depth", "Jumping vertically not horizontally", "Stiff landing"]',
    '["Patellar tendinopathy", "Hip flexor pathology", "Ankle instability", "Recent lower extremity injury"]',
    '["Split squat only", "Broad jump from bilateral", "Box step-up progression"]',
    '["Add dumbbells", "Increase jump distance goal", "Single-leg hop finish", "Continuous variant"]',
    '["Dumbbells", "Kettlebells", "Barbell", "Bodyweight"]'
),

(
    'Romanian Deadlift to Good Morning Combo',
    'Perform RDL with barbell, at top immediately transition into good morning with same bar, hinge at hips continuously.',
    'Advanced', 'Compound', 'Hinge', 7, 18,
    '["Soft knees on RDL", "Bar close to body", "Transition by raising torso slightly", "Hinge deeply on good morning"]',
    '["Rounding lumbar spine", "Bar drifting forward", "Incomplete hip extension", "Using quads instead of hamstrings"]',
    '["Lower back pathology", "Hamstring strain acute", "Hip impingement", "Core stability deficits"]',
    '["RDL only", "Good morning only", "Bodyweight hip hinge pattern"]',
    '["Increase load", "Tempo variations", "Single-leg RDL to good morning", "Add squat at end"]',
    '["Barbell", "Dumbbells", "Kettlebells", "Resistance band"]'
),

(
    'Reverse Lunge to Hurdle Hop Combo',
    'Step back into reverse lunge, explode up and hop over hurdle laterally, land and repeat opposite direction.',
    'Advanced', 'Compound', 'Push', 7, 18,
    '["Deep reverse lunge", "Explode through front leg", "Clear hurdle with knee lift", "Land softly stabilizing"]',
    '["Incomplete lunge depth", "Hitting hurdle", "Landing stiff", "Loss of balance on landing"]',
    '["Patellar tendinopathy", "Ankle sprain history", "Hip flexor strain", "Balance deficits"]',
    '["Reverse lunge only", "Hurdle hop from bilateral", "Low hurdle or line"]',
    '["Higher hurdle", "Add dumbbells", "Continuous alternating", "Increase distance between hurdles"]',
    '["Hurdles", "Cones", "Lines on floor", "Dumbbells for load"]'
),

(
    'Front Squat to Jump Squat Combo',
    'Complete front squat with barbell, upon reaching parallel explode upward into jump squat releasing bar to rack.',
    'Advanced', 'Compound', 'Push', 8, 24,
    '["Elbows high in front rack", "Full depth on squat", "Explode through entire foot", "Release bar safely at top"]',
    '["Elbows dropping", "Forward lean", "Incomplete depth before jumping", "Landing before re-racking"]',
    '["Shoulder impingement", "Wrist pathology", "Patellar tendinopathy", "Core stability issues"]',
    '["Goblet squat to jump", "Front squat only", "Jump squat bodyweight"]',
    '["Increase load", "Add depth jump landing", "Continuous touch-and-go", "Overhead squat variant"]',
    '["Barbell", "Safety squat bar", "Kettlebell goblet", "Sandbag"]'
),

(
    'Single-Leg RDL to Box Step-Up Combo',
    'Perform single-leg RDL touching floor, return to standing and immediately step onto box with same leg.',
    'Advanced', 'Compound', 'Hinge-Push', 7, 20,
    '["Hinge at hip keeping leg extended", "Touch floor with control", "Return to standing", "Drive through foot onto box"]',
    '["Rounding back", "Bending standing knee excessively", "Using momentum", "Incomplete box step-up"]',
    '["Hamstring strain", "Balance deficits", "Knee pathology", "Hip mobility restrictions"]',
    '["Supported single-leg RDL", "Box step-up only", "Bilateral RDL to step-up"]',
    '["Add dumbbells", "Higher box", "Continuous without pause", "Add knee drive at top"]',
    '["Dumbbells", "Kettlebell", "Barbell", "Bodyweight"]'
),

(
    'Goblet Squat to Calf Raise Combo',
    'Complete goblet squat, upon standing immediately rise onto toes for calf raise, lower heels and repeat.',
    'Intermediate', 'Compound', 'Push', 4, 10,
    '["Hold kettlebell at chest", "Full depth squat", "Drive through entire foot", "Rise onto toes at top"]',
    '["Heels lifting on squat", "Incomplete depth", "Rushing calf raise", "Leaning forward"]',
    '["Ankle pathology", "Achilles tendinopathy", "Knee pain", "Limited dorsiflexion"]',
    '["Bodyweight squat", "Calf raise only", "Box squat progression"]',
    '["Heavier kettlebell", "Single-leg calf raise", "Pause at bottom", "Jump squat finish"]',
    '["Kettlebell", "Dumbbell", "Barbell front rack", "Weight plate"]'
),

(
    'Walking Lunge to Jump Lunge Combo',
    'Perform walking lunge for distance, immediately transition into explosive jump lunges in place.',
    'Advanced', 'Compound', 'Push', 6, 15,
    '["Full stride on walking lunge", "Both knees at 90 degrees", "Explode switching legs mid-air", "Land softly alternating"]',
    '["Short steps", "Knee hitting ground", "Incomplete leg switch", "Landing stiff-legged"]',
    '["Patellar tendinopathy", "Hip flexor strain", "Knee meniscus issues", "Cardiovascular limitations"]',
    '["Walking lunge only", "Jump lunge from static", "Step-back lunge progression"]',
    '["Add dumbbells", "Longer walking distance", "Continuous jump lunges", "Weighted vest"]',
    '["Dumbbells", "Kettlebells", "Bodyweight", "Weight vest"]'
),

(
    'Hip Thrust to Jump Combo',
    'Complete hip thrust with barbell, upon lockout immediately unload and perform vertical jump, reset and repeat.',
    'Advanced', 'Compound', 'Hinge', 7, 18,
    '["Full hip extension on thrust", "Squeeze glutes at top", "Quick bar release", "Maximal vertical jump"]',
    '["Incomplete hip extension", "Hyperextending lumbar", "Slow transition", "Submaximal jump effort"]',
    '["Lumbar pathology", "Hip impingement", "Patellar tendinopathy", "Pelvic floor dysfunction"]',
    '["Hip thrust only", "Jump only", "Glute bridge progression"]',
    '["Heavier hip thrust", "Higher jump target", "Single-leg hip thrust", "Broad jump variant"]',
    '["Barbell", "Dumbbell", "Resistance band", "Hip thrust machine"]'
);

-- ================================================================
-- SECTION D: POWER/FULL BODY COMBOS (11 exercises)
-- ================================================================

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

-- POWER COMBOS
(
    'Power Clean to Broad Jump Combo',
    'Execute power clean catching at shoulders, immediately drop bar and explode into maximal broad jump.',
    'Advanced', 'Power', 'Pull-Push', 8, 24,
    '["Explosive triple extension on clean", "Catch in athletic position", "Quick safe bar drop", "Maximal horizontal jump"]',
    '["Incomplete clean pull", "Catching too high", "Rushing jump setup", "Landing stiff"]',
    '["Shoulder pathology", "Lower back issues", "Patellar tendinopathy", "Wrist limitations"]',
    '["Hang clean only", "Broad jump only", "Deadlift to jump progression"]',
    '["Increase clean load", "Longer jump distance", "Add depth jump", "Continuous circuit"]',
    '["Barbell", "Dumbbells", "Kettlebells", "Trap bar"]'
),

(
    'Snatch Pull to Overhead Med Ball Slam Combo',
    'Perform snatch pull to mid-thigh, immediately catch medicine ball and slam overhead to ground.',
    'Advanced', 'Power', 'Pull-Push', 7, 20,
    '["Explosive pull from floor", "Extend fully at hips", "Catch ball at chest", "Aggressive overhead slam"]',
    '["Incomplete extension", "Early arm bend", "Catching ball too low", "Using only arms on slam"]',
    '["Shoulder impingement", "Lower back pathology", "Wrist issues", "Core instability"]',
    '["Snatch pull only", "Med ball slam only", "High pull progression"]',
    '["Heavier pull load", "Heavier med ball", "Continuous repetitions", "Add jump after slam"]',
    '["Barbell + med ball", "Dumbbells + slam ball", "Kettlebell + sandbag", "Trap bar + med ball"]'
),

(
    'Back Squat to Hurdle Hop Combo',
    'Complete back squat, upon standing immediately hop over hurdle forward, land and reset for next rep.',
    'Advanced', 'Compound', 'Push', 8, 24,
    '["Full depth on squat", "Explode through entire foot", "Clear hurdle with knee drive", "Land softly absorbing impact"]',
    '["Incomplete squat depth", "Hitting hurdle", "Landing with locked knees", "Forward lean excessive"]',
    '["Patellar tendinopathy", "Hip pathology", "Ankle instability", "Lower back issues"]',
    '["Squat only", "Hurdle hop only", "Box squat to step-over"]',
    '["Increase squat load", "Higher hurdle", "Continuous hops", "Add rotation"]',
    '["Barbell", "Safety squat bar", "Front rack kettlebells", "Goblet squat"]'
),

(
    'Thruster to Box Jump Combo',
    'Complete thruster (front squat to push press), drop bar and immediately perform maximal box jump.',
    'Advanced', 'Compound', 'Push', 8, 24,
    '["Full depth front squat", "Aggressive drive on press", "Quick bar drop", "Explosive box jump"]',
    '["Incomplete squat depth", "Pressing before standing", "Rushing jump setup", "Landing incomplete on box"]',
    '["Shoulder impingement", "Patellar tendinopathy", "Wrist pathology", "Box height too advanced"]',
    '["Thruster only", "Box jump only", "Goblet squat to press progression"]',
    '["Increase thruster load", "Higher box", "Continuous repetitions", "Add step-off jump"]',
    '["Barbell", "Dumbbells", "Kettlebells", "Sandbag"]'
),

(
    'Kettlebell Swing to Jump Squat Combo',
    'Perform explosive kettlebell swing, at top release handle and immediately drop into jump squat.',
    'Advanced', 'Power', 'Hinge-Push', 6, 15,
    '["Hip drive on swing", "Bell floats at top", "Quick release and drop", "Explosive jump squat"]',
    '["Using arms on swing", "Incomplete hip extension", "Rushing jump squat", "Landing stiff"]',
    '["Lower back pathology", "Patellar tendinopathy", "Hip impingement", "Grip limitations"]',
    '["Swing only", "Jump squat only", "Deadlift to jump progression"]',
    '["Heavier kettlebell", "Higher jump", "Continuous flow", "Single-leg variant"]',
    '["Kettlebell", "Dumbbell", "Sandbag", "Medicine ball"]'
),

(
    'Medicine Ball Scoop Toss to Sprint Combo',
    'Perform scoop toss for max distance, immediately sprint to retrieve ball and return to start.',
    'Intermediate', 'Power', 'Push', 5, 12,
    '["Triple extension on toss", "Aggressive follow-through", "Immediate acceleration on sprint", "Controlled deceleration returning"]',
    '["Incomplete extension", "Slow sprint start", "Poor sprint mechanics when fatigued", "Not controlling deceleration"]',
    '["Shoulder pathology", "Lower back issues", "Hamstring strain history", "Ankle instability"]',
    '["Stationary toss", "Walk retrieval", "Lighter ball"]',
    '["Heavier ball", "Longer sprint distance", "Add push-up at retrieval", "Continuous circuit"]',
    '["Medicine ball 4-8kg", "Slam ball", "Sandbag", "Weighted implement"]'
),

(
    'Burpee to Broad Jump Combo',
    'Complete full burpee with push-up, upon standing explode into maximal broad jump, reset and repeat.',
    'Advanced', 'Metabolic', 'Push-Pull', 6, 15,
    '["Full push-up on burpee", "Feet jump to hands quickly", "Stand tall before jump", "Maximal horizontal effort"]',
    '["Skipping push-up", "Slow foot return", "Jumping before fully standing", "Landing stiff"]',
    '["Shoulder pathology", "Wrist issues", "Patellar tendinopathy", "Cardiovascular limitations"]',
    '["Burpee without push-up", "Broad jump only", "Step-back burpee progression"]',
    '["Add weight vest", "Higher jump target", "Continuous without pause", "Add tuck jump"]',
    '["Bodyweight", "Weight vest", "Parallettes for push-up", "Slam ball addition"]'
),

(
    'Battle Rope Waves to Slam Ball Combo',
    'Perform alternating battle rope waves for time, immediately grab slam ball and execute overhead slams.',
    'Intermediate', 'Metabolic', 'Push-Pull', 5, 12,
    '["Aggressive rope waves using hips", "Maintain athletic stance", "Quick transition to ball", "Full extension on slams"]',
    '["Using only arms on ropes", "Standing upright", "Rushing to ball unsafely", "Incomplete slam extension"]',
    '["Shoulder pathology", "Lower back acute pain", "Wrist issues", "Cardiovascular limitations"]',
    '["Rope waves only", "Slam ball only", "Seated rope variant"]',
    '["Heavier ropes", "Heavier ball", "Longer work intervals", "Add burpee between"]',
    '["Battle ropes + slam ball", "Heavy ropes + sandbag", "TRX + med ball", "Bands + slam ball"]'
),

(
    'Box Jump to Depth Drop Combo',
    'Jump onto box, immediately step off opposite leg and perform depth drop landing softly, reset and repeat.',
    'Advanced', 'Power', 'Push', 7, 20,
    '["Explosive jump onto box", "Full extension at top", "Quick step-off", "Absorb landing silently"]',
    '["Incomplete box landing", "Stepping off too fast", "Landing loudly", "Knee valgus on landing"]',
    '["Patellar tendinopathy", "Ankle instability", "Hip pathology", "Box height too advanced"]',
    '["Box jump only", "Depth drop from lower height", "Step-up progression"]',
    '["Higher box", "Greater depth drop height", "Add broad jump after", "Continuous hops"]',
    '["Box/platform", "Plyo box", "Bench", "Steps"]'
),

(
    'Clean Pull to Vertical Jump Combo',
    'Execute clean pull to full extension without catching, immediately perform maximal vertical jump.',
    'Advanced', 'Power', 'Pull', 7, 18,
    '["Explosive pull from floor", "Full triple extension", "Land softly from pull", "Immediately jump maximally"]',
    '["Incomplete extension on pull", "Catching attempt", "Rushing jump", "Landing stiff on jump"]',
    '["Patellar tendinopathy", "Lower back pathology", "Shoulder issues", "Ankle instability"]',
    '["Clean pull only", "Vertical jump only", "High pull progression"]',
    '["Increase pull load", "Higher jump target", "Add approach", "Continuous repetitions"]',
    '["Barbell", "Dumbbells", "Kettlebells", "Trap bar"]'
),

(
    'Sandbag Shoulder to Sprint Combo',
    'Load sandbag to shoulder in one motion, immediately sprint designated distance, return and repeat opposite side.',
    'Advanced', 'Strongman', 'Push', 6, 15,
    '["Explosive hip drive on shoulder", "Secure bag on shoulder", "Aggressive sprint mechanics", "Controlled deceleration"]',
    '["Using only arms on shoulder", "Bag unstable on shoulder", "Poor sprint form", "Crashing at turnaround"]',
    '["Shoulder pathology", "Lower back issues", "Hip flexor strain", "Sprint mechanics deficits"]',
    '["Lighter bag", "Shorter sprint", "Shoulder to stationary hold", "Farmer carry progression"]',
    '["Heavier sandbag", "Longer sprint", "Add turn with bag", "Multiple shoulders before sprint"]',
    '["Sandbag", "Atlas stone", "Heavy medicine ball", "Log"]'
);

-- ================================================================
-- SECTION E: TAG ASSIGNMENTS FOR COMBO EXERCISES
-- ================================================================

-- Tag all newly added combo exercises with 'Combo' tag
-- This requires getting exercise IDs, so we'll use name-based updates

UPDATE exercise_tags
SET created_at = NOW()
WHERE EXISTS (
    SELECT 1 FROM exercises e 
    WHERE e.id = exercise_tags.exercise_id 
    AND e.name LIKE '%Combo%'
);

-- Insert tags for exercises that don't have Combo tag yet
INSERT INTO exercise_tags (exercise_id, tag_id, created_at)
SELECT e.id, t.id, NOW()
FROM exercises e
CROSS JOIN tags t
WHERE e.name LIKE '%Combo%'
AND t.name = 'Combo'
AND NOT EXISTS (
    SELECT 1 FROM exercise_tags et 
    WHERE et.exercise_id = e.id 
    AND et.tag_id = t.id
);

COMMIT;
