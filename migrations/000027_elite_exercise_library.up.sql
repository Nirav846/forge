-- Migration: 000027_elite_exercise_library
-- Source: NSCA, UKSCA, ASCA, EXOS, ALTIS, Olympic Centers
-- Intent: Add professional-grade, categorized exercises with full coaching metadata
-- Phase: 1 of 3 (Foundational Elite Movements)

BEGIN;

-- Helper function to insert exercises with full metadata
CREATE OR REPLACE FUNCTION add_elite_exercise(
    p_name TEXT, p_category TEXT, p_subcategory TEXT, p_intent TEXT,
    p_equipment TEXT[], p_coaching_cues TEXT[], p_common_errors TEXT[],
    p_contraindications TEXT[], p_regressions TEXT[], p_progressions TEXT[],
    p_source_org TEXT, p_sport_specific TEXT[]
) RETURNS VOID AS $$
DECLARE
    v_exercise_id BIGINT;
BEGIN
    INSERT INTO exercises (
        name, category, subcategory, intent, equipment,
        coaching_cues, common_errors, contraindications, regressions, progressions,
        source_organization, sport_specific_tags, created_at
    ) VALUES (
        p_name, p_category, p_subcategory, p_intent, p_equipment,
        p_coaching_cues, p_common_errors, p_contraindications, p_regressions, p_progressions,
        p_source_org, p_sport_specific, NOW()
    ) RETURNING id INTO v_exercise_id;
    
    -- Add description separately if needed, or assume name is descriptive enough for now
    -- Adding a generic but professional description template
    UPDATE exercises SET 
        description = 'Elite level ' || p_intent || ' movement targeting ' || p_subcategory || '. Prescribed for ' || p_source_org || ' based programming.'
    WHERE id = v_exercise_id;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- CATEGORY 1: POWER & ELASTICITY (ALTIS / OLYMPIC CENTER STYLE)
-- Focus: Rate of Force Development (RFD), Stiffness, Elastic Recoil
-- ============================================================================

-- 1. Snap Down (ALTIS)
SELECT add_elite_exercise(
    'Snap Down', 'Power', 'Elastic/Plyometric', 'Stiffness/Acceleration',
    ARRAY['Bodyweight'],
    ARRAY['Tall posture, ribs down', 'Snap hands violently to hips', 'Land flat-footed and STICK', 'Immediate rebound'],
    ARRAY['Landing with bent waist', 'Heel strike', 'Slow arm action', 'Collapsing on landing'],
    ARRAY['Acute ankle sprain', 'Severe plantar fasciitis'],
    ARRAY['Snap Down to Box', 'Countermovement Jump'],
    ARRAY['Jump Squat', 'Depth Jump'],
    'ALTIS',
    ARRAY['Sprint Start', 'Change of Direction', 'Basketball', 'Football']
);

-- 2. Dribble Hop (ALTIS)
SELECT add_elite_exercise(
    'Dribble Hop', 'Power', 'Elastic/Plyometric', 'Ankle Stiffness',
    ARRAY['Bodyweight'],
    ARRAY['Minimal knee bend', 'Quick ground contact', 'Relaxed upper body', 'Rhythmic bouncing'],
    ARRAY['Sinking too deep', 'Heavy landing', 'Holding breath', 'Arm swinging'],
    ARRAY['Achilles tendonitis', 'Shin splints'],
    ARRAY['Pogo Jump', 'Single Leg Dribble'],
    ARRAY['Depth Drop to Stick', 'Hurdle Hops'],
    'ALTIS',
    ARRAY['Sprinting', 'Distance Running', 'Boxing']
);

-- 3. Hang Power Clean (Mid-Thigh)
SELECT add_elite_exercise(
    'Hang Power Clean (Mid-Thigh)', 'Power', 'Olympic Derivative', 'Triple Extension',
    ARRAY['Barbell', 'Platform'],
    ARRAY['Shoulders over bar', 'Violent hip extension', 'Pull under bar quickly', 'Rack on front deltoids'],
    ARRAY['Early arm bend', 'Catching on clavicle', 'Heaving torso', 'Wide stance'],
    ARRAY['Lower back injury', 'Wrist impingement', 'Shoulder dislocation history'],
    ARRAY['High Pull', 'Clean Deadlift'],
    ARRAY['Power Clean from Floor', 'Hang Clean + Jerk'],
    'NSCA / Olympic Center',
    ARRAY['Football Lineman', 'Rugby Forwards', 'Throwers']
);

-- 4. Med Ball Rotational Throw (Side Step)
SELECT add_elite_exercise(
    'Med Ball Rotational Throw (Side Step)', 'Power', 'Rotational', 'Transverse Plane Power',
    ARRAY['Medicine Ball', 'Wall'],
    ARRAY['Step away from wall', 'Rotate hips first', 'Whip arm through', 'Follow through fully'],
    ARRAY['Arm dominant only', 'No hip rotation', 'Planting feet flat', 'Not resetting'],
    ARRAY['Acute oblique strain', 'Lumbar disc herniation'],
    ARRAY['Seated Rotational Throw', 'Half-Kneeling Throw'],
    ARRAY['Running Rotational Throw', 'Heavier Ball'],
    'EXOS',
    ARRAY['Baseball', 'Tennis', 'Golf', 'Cricket Batting']
);

-- 5. Broad Jump to Stick
SELECT add_elite_exercise(
    'Broad Jump to Stick', 'Power', 'Horizontal Jump', 'Deceleration Control',
    ARRAY['Bodyweight', 'Sand Pit/Mat'],
    ARRAY['Arm swing back then forward', 'Double arm drive', 'Land softly', 'Hold landing 2 seconds'],
    ARRAY['Knee valgus on landing', 'Heel strike', 'Falling backward', 'No arm swing'],
    ARRAY['ACL reconstruction < 6 months', 'Patellar tendinopathy'],
    ARRAY['Squat Jump', 'Standing Long Jump (no stick)'],
    ARRAY['Multiple Broad Jumps', 'Box Jump Over'],
    'NSCA',
    ARRAY['Football', 'Rugby', 'Basketball']
);

-- ============================================================================
-- CATEGORY 2: MAX STRENGTH & FUNCTIONAL (UKSCA / NSCA STYLE)
-- Focus: Force Production, Structural Integrity, Unilateral Stability
-- ============================================================================

-- 6. Landmine Split Squat
SELECT add_elite_exercise(
    'Landmine Split Squat', 'Strength', 'Unilateral Lower', 'Hypertrophy/Stability',
    ARRAY['Landmine', 'Barbell'],
    ARRAY['Staggered stance', 'Keep torso tall', 'Drive through front heel', 'Control descent'],
    ARRAY['Front knee caving in', 'Leaning too far forward', 'Back knee slamming', 'Short ROM'],
    ARRAY['Severe knee arthritis', 'Hip impingement'],
    ARRAY['Goblet Split Squat', 'Bodyweight Split Squat'],
    ARRAY['Elevated Front Foot Split Squat', 'Add Pause'],
    'UKSCA',
    ARRAY['Soccer', 'Rugby Backs', 'Tennis']
);

-- 7. Single Arm Farmer''s Carry
SELECT add_elite_exercise(
    'Single Arm Farmer''s Carry', 'Strength', 'Loaded Carry', 'Anti-Lateral Flexion',
    ARRAY['Kettlebell', 'Dumbbell', 'Trap Bar'],
    ARRAY['Tall spine', 'Brace core hard', 'Do not lean away', 'Smooth walking gait'],
    ARRAY['Leaning to side', 'Shrugging shoulder', 'Short steps', 'Holding breath'],
    ARRAY['Acute shoulder dislocation', 'Severe scoliosis'],
    ARRAY['Suitcase Carry (light)', 'Static Hold'],
    ARRAY['Heavier Load', 'Uneven Surface Walk', 'Overhead Carry'],
    'EXOS',
    ARRAY['All Sports', 'Strongman', 'MMA']
);

-- 8. Nordic Hamstring Curl (Eccentric Only)
SELECT add_elite_exercise(
    'Nordic Hamstring Curl (Eccentric)', 'Strength', 'Posterior Chain', 'Eccentric Overload',
    ARRAY['Partner', 'Nordic Bench', 'Mat'],
    ARRAY['Hips extended', 'Lower slowly', 'Resist gravity', 'Catch with hands at bottom'],
    ARRAY['Hips flexing early', 'Dropping fast', 'Neck craning', 'Toes not anchored'],
    ARRAY['Acute hamstring tear', 'Knee ligament instability'],
    ARRAY['Slider Leg Curl', 'Eccentric Slide'],
    ARRAY['Full Nordic Curl', 'Add Band Assistance'],
    'ASCA / Soccer Science',
    ARRAY['Soccer', 'Sprinting', 'Rugby', 'AFL']
);

-- 9. Zercher Squat
SELECT add_elite_exercise(
    'Zercher Squat', 'Strength', 'Bilateral Lower', 'Core/Anterior Chain',
    ARRAY['Barbell', 'Squat Rack', 'Pad'],
    ARRAY['Bar in elbow crooks', 'Chest up', 'Sit back and down', 'Drive elbows up'],
    ARRAY['Rounding back', 'Knees caving', 'Elbows slipping', 'Heels lifting'],
    ARRAY['Elbow bursitis', 'Severe lower back issues'],
    ARRAY['Goblet Squat', 'Front Squat'],
    ARRAY['Zercher Good Morning', 'Zercher Reverse Lunge'],
    'Strongman / Rugby S&C',
    ARRAY['Rugby Forwards', 'Football Lineman', 'Wrestling']
);

-- 10. Weighted Pull-Up (Neutral Grip)
SELECT add_elite_exercise(
    'Weighted Pull-Up (Neutral Grip)', 'Strength', 'Vertical Pull', 'Upper Body Strength',
    ARRAY['Pull-up Bar', 'Dip Belt', 'Dumbbell'],
    ARRAY['Dead hang start', 'Pull chest to bar', 'Squeeze shoulder blades', 'Control down'],
    ARRAY['Kipping/swinging', 'Partial ROM', 'Neck craning', 'Shrugging at top'],
    ARRAY['Shoulder impingement', 'Elbow tendonitis', 'Recent rotator cuff surgery'],
    ARRAY['Band Assisted Pull-Up', 'Inverted Row'],
    ARRAY['Archer Pull-Up', 'Muscle-Up Progression'],
    'NSCA',
    ARRAY['Climbing', 'Gymnastics', 'Swimming', 'Rowing']
);

-- ============================================================================
-- CATEGORY 3: COMPLEXES & CONTRAST (THE MISSING LINK)
-- Focus: Post-Activation Potentiation (PAP), Flow, Density
-- Structure: Heavy Strength -> Explosive Movement
-- ============================================================================

-- 11. LOWER COMPLEX: Lunge to Step-Up Knee Drive
SELECT add_elite_exercise(
    'Lunge to Step-Up Knee Drive Complex', 'Complex', 'Lower Body Flow', 'Unilateral Strength/Power',
    ARRAY['Dumbbells', 'Box'],
    ARRAY['Reverse lunge deep', 'Drive front foot into box', 'Explode up to knee drive', 'Balance at top'],
    ARRAY['Stepping too short', 'Knee collapsing inward', 'No pause between reps', 'Rushing tempo'],
    ARRAY['Acute knee meniscus tear', 'Severe balance issues'],
    ARRAY['Reverse Lunge Only', 'Step-Up Only'],
    ARRAY['Add Jump at Top', 'Heavier DBs', 'Reduce Ground Contact Time'],
    'UKSCA / Pro Soccer',
    ARRAY['Soccer', 'Basketball', 'Volleyball', 'Tennis']
);

-- 12. LOWER COMPLEX: RDL to Box Jump
SELECT add_elite_exercise(
    'RDL to Box Jump Contrast', 'Complex', 'Posterior/Power', 'Eccentric Loading to Plyo',
    ARRAY['Barbell', 'Box'],
    ARRAY['Hinge hips back', 'Feel stretch in hamstrings', 'Drop bar and immediately jump', 'Land soft'],
    ARRAY['Rounding back on RDL', 'Pausing too long before jump', 'Landing stiff'],
    ARRAY['Acute hamstring strain', 'Low back pain'],
    ARRAY['RDL Only', 'Box Jump Only'],
    ARRAY['Heavier RDL', 'Higher Box'],
    'NSCA Contrast Method',
    ARRAY['Sprinting', 'Football', 'Rugby']
);

-- 13. UPPER COMPLEX: Renegade Row to Push-Up
SELECT add_elite_exercise(
    'Renegade Row to Push-Up Complex', 'Complex', 'Upper Body Flow', 'Core Stability/Upper Strength',
    ARRAY['Dumbbells', 'Floor'],
    ARRAY['Plank position tight', 'Row one arm', 'Return', 'Push-up', 'Alternate arms'],
    ARRAY['Hips rotating', 'Sagging lower back', 'Flaring elbows', 'Rushing form'],
    ARRAY['Wrist carpal tunnel', 'Shoulder instability', 'Lower back pain'],
    ARRAY['Plank Hold', 'Standard Push-Up', 'Single Arm Row'],
    ARRAY['Slower Tempo', 'Feet Elevated', 'Heavier DBs'],
    'EXOS / MMA S&C',
    ARRAY['MMA', 'Wrestling', 'Swimming', 'CrossFit']
);

-- 14. UPPER COMPLEX: Inverted Row to Pike Push-Up
SELECT add_elite_exercise(
    'Inverted Row to Pike Push-Up', 'Complex', 'Upper Body Flow', 'Pull/Push Balance',
    ARRAY['TRX / Bar', 'Floor'],
    ARRAY['Row chest to bar', 'Reset feet', 'Pike hips up', 'Lower head to floor'],
    ARRAY['Sagging hips on row', 'Not going deep enough on push-up', 'Neck craning'],
    ARRAY['Shoulder impingement', 'Vertigo/Dizziness'],
    ARRAY['Knee Tuck Row', 'Wall Pike Push-Up'],
    ARRAY['Feet Elevated Row', 'Deficit Pike Push-Up'],
    'Calisthenics Pro',
    ARRAY['Gymnastics', 'Climbing', 'Swimming']
);

-- 15. POWER COMPLEX: Trap Bar Deadlift to Vertical Jump
SELECT add_elite_exercise(
    'Trap Bar Deadlift to Vertical Jump', 'Complex', 'Total Body Power', 'PAP Contrast',
    ARRAY['Trap Bar', 'Jump Mat'],
    ARRAY['Heavy double (85%)', 'Explosive concentric', 'Drop bar', 'Immediate max vertical'],
    ARRAY['Resting too long between lift/jump', 'Poor jump technique', 'Rounding back'],
    ARRAY['Acute back injury', 'Knee pathology'],
    ARRAY['Trap Bar DL Only', 'CMJ Only'],
    ARRAY['Increase DL Load', 'Add Depth Jump'],
    'NSCA / ALTIS',
    ARRAY['Basketball', 'Volleyball', 'High Jump', 'Football WR']
);

-- 16. POWER COMPLEX: Bench Press to Med Ball Chest Pass
SELECT add_elite_exercise(
    'Bench Press to Med Ball Chest Pass', 'Complex', 'Upper Power', 'Horizontal Push PAP',
    ARRAY['Barbell', 'Medicine Ball', 'Wall'],
    ARRAY['Heavy bench rep', 'Rack bar', 'Grab ball', 'Explosive chest pass'],
    ARRAY['Bouncing ball', 'Poor bench form', 'Waiting too long'],
    ARRAY['Shoulder AC joint separation', 'Pec tear history'],
    ARRAY['Bench Only', 'Med Ball Throw Only'],
    ARRAY['Heavier Bench', 'Lighter/Faster Ball'],
    'EXOS Baseball',
    ARRAY['Baseball', 'Football QB', 'Tennis Serve']
);

-- 17. ROTATIONAL COMPLEX: Landmine Rotational Press to Woodchop
SELECT add_elite_exercise(
    'Landmine Rotational Press to Woodchop', 'Complex', 'Rotational Flow', 'Core/Oblique Power',
    ARRAY['Landmine', 'Handle'],
    ARRAY['Press across body', 'Rotate hips', 'Flow into woodchop down', 'Engage obliques'],
    ARRAY['Using only arms', 'No hip rotation', 'Lower back rounding'],
    ARRAY['Acute lumbar strain', 'Hip labral tear'],
    ARRAY['Pallof Press', 'Cable Woodchop'],
    ARRAY['Heavier Load', 'Single Leg Stance'],
    'UKSCA Golf/Tennis',
    ARRAY['Golf', 'Tennis', 'Baseball', 'Hockey']
);

-- 18. DECELERATION COMPLEX: Lateral Bound to Stick
SELECT add_elite_exercise(
    'Lateral Bound to Stick', 'Complex', 'Frontal Plane', 'Deceleration/Stability',
    ARRAY['Bodyweight', 'Cones'],
    ARRAY['Push off lateral leg', 'Fly through air', 'Land on opposite leg', 'Stick 3 seconds'],
    ARRAY['Knee valgus', 'Touching other foot down', 'Falling over', 'Stiff landing'],
    ARRAY['Ankle sprain', 'Knee MCL injury'],
    ARRAY['Side Step', 'Small Hop'],
    ARRAY['Continuous Bounds', 'Add Reach'],
    'ALTIS / Physio',
    ARRAY['Basketball', 'Soccer', 'Tennis', 'Badminton']
);

-- ============================================================================
-- CATEGORY 4: MOBILITY & PREHAB (PHYSIO / ALTIS STYLE)
-- Focus: Range of Motion, Tissue Quality, Injury Mitigation
-- ============================================================================

-- 19. 90/90 Hip Switch
SELECT add_elite_exercise(
    '90/90 Hip Switch', 'Mobility', 'Hip', 'Internal/External Rotation',
    ARRAY['Mat'],
    ARRAY['Front shin parallel', 'Back shin parallel', 'Tall spine', 'Rotate hips without hands'],
    ARRAY['Leaning back', 'Lifting foot off ground', 'Rounding spine'],
    ARRAY['Acute hip labral tear', 'Severe hip OA'],
    ARRAY['Supported 90/90', 'Single Side Hold'],
    ARRAY['Add Lean Forward', 'Add Reach Through'],
    'ALTIS / FMS',
    ARRAY['All Sports', 'Yoga', 'Martial Arts']
);

-- 20. Thoracic Spine Windmill (Foam Roller)
SELECT add_elite_exercise(
    'Thoracic Spine Windmill', 'Mobility', 'T-Spine', 'Rotation/Extension',
    ARRAY['Foam Roller'],
    ARRAY['Lie on side on roller', 'Open top arm across body', 'Follow with eyes', 'Breathe into ribs'],
    ARRAY['Rolling too fast', 'Holding breath', 'Lifting hips off roller'],
    ARRAY['Severe osteoporosis', 'Acute rib fracture'],
    ARRAY['Cat-Cow', 'Thread the Needle'],
    ARRAY['Add Reach Under', 'Longer Hold'],
    'EXOS / Physio',
    ARRAY['Swimming', 'Baseball', 'Golf', 'Tennis']
);

-- 21. Copenhagen Plank (Short Lever)
SELECT add_elite_exercise(
    'Copenhagen Plank (Short Lever)', 'Prehab', 'Adductor/Groin', 'Isometric Strength',
    ARRAY['Bench', 'Mat'],
    ARRAY['Top foot on bench', 'Bottom knee on floor', 'Lift hips', 'Squeeze groin'],
    ARRAY['Hips sagging', 'Shoulder collapsing', 'Holding breath'],
    ARRAY['Acute groin strain', 'Hip adductor tear'],
    ARRAY['Side Plank', 'Clam Shell'],
    ARRAY['Long Lever (Foot on bench)', 'Add Hip Dip'],
    'Soccer Science / UKSCA',
    ARRAY['Soccer', 'Hockey', 'Rugby', 'MMA']
);

-- 22. Ankle Dorsiflexion Rock (Wall)
SELECT add_elite_exercise(
    'Ankle Dorsiflexion Rock', 'Mobility', 'Ankle', 'DF Range of Motion',
    ARRAY['Wall'],
    ARRAY['Toe close to wall', 'Knee touches wall', 'Keep heel down', 'Rock forward/back'],
    ARRAY['Heel lifting', 'Knee caving in', 'Rolling foot outward'],
    ARRAY['Acute ankle fracture', 'Severe sprain'],
    ARRAY['Seated Ankle Pump', 'Calf Stretch'],
    ARRAY['Increase Distance', 'Add Band Distraction'],
    'ALTIS / Run Lab',
    ARRAY['Running', 'Soccer', 'Basketball', 'Weightlifting']
);

-- ============================================================================
-- CATEGORY 5: ENERGY SYSTEMS & CONDITIONING (EXOS / TEAM SPORT)
-- Focus: Work Capacity, Alactic Power, Glycolytic Capacity
-- ============================================================================

-- 23. Shuttle Run (Pro Agility / 5-10-5)
SELECT add_elite_exercise(
    'Shuttle Run (5-10-5)', 'Conditioning', 'Agility', 'Change of Direction',
    ARRAY['Cones', 'Stopwatch'],
    ARRAY['Start in 3-point stance', 'Explode first 5 yards', 'Plant outside foot', 'Accelerate out'],
    ARRAY['Crossing feet', 'Wide turns', 'Standing up too tall', 'Slipping'],
    ARRAY['Acute ACL/MCL tear', 'Concussion protocol'],
    ARRAY['Line Drill', 'T-Drill'],
    ARRAY['Timed Reps', 'Add Reaction Cue'],
    'NFL Combine / NSCA',
    ARRAY['Football', 'Basketball', 'Lacrosse', 'Soccer']
);

-- 24. Hill Sprints (10-15 sec)
SELECT add_elite_exercise(
    'Hill Sprints (10-15 sec)', 'Conditioning', 'Alactic Power', 'Mechanics/Force',
    ARRAY['Hill', 'Grass/Turf'],
    ARRAY['Drive knees high', 'Punch arms', 'Stay on balls of feet', 'Walk down recovery'],
    ARRAY['Overstriding', 'Leaning back', 'Tight shoulders', 'Running flat'],
    ARRAY['Hamstring strain', 'Calf tear', 'Achilles issues'],
    ARRAY['Walk Uphill', 'Marching Drills'],
    ARRAY['Steeper Hill', 'Longer Duration (20s)'],
    'ALTIS / Sprint Coach',
    ARRAY['Sprinting', 'Football', 'Rugby', 'Soccer']
);

-- 25. Battle Ropes (30s Wave)
SELECT add_elite_exercise(
    'Battle Ropes (30s Alternating Wave)', 'Conditioning', 'Work Capacity', 'Upper Body Metcon',
    ARRAY['Battle Ropes', 'Anchor'],
    ARRAY['Athletic stance', 'Brace core', 'Whip ropes hard', 'Fast turnover'],
    ARRAY['Using lower back', 'Stopping between waves', 'Holding breath', 'Feet moving'],
    ARRAY['Shoulder impingement', 'Lower back pain', 'Hypertension'],
    ARRAY['Slower Waves', 'Single Arm'],
    ARRAY['Double Waves', 'Squat Jumps with Ropes'],
    'EXOS / MMA',
    ARRAY['MMA', 'Wrestling', 'Football', 'General Conditioning']
);

-- Drop helper function
DROP FUNCTION add_elite_exercise;

COMMIT;

-- Verification Query
-- SELECT category, subcategory, COUNT(*) FROM exercises GROUP BY category, subcategory ORDER BY category;
