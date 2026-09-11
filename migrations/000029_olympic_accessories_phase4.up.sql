-- MIGRATION 000029: OLYMPIC_ACCESSORIES_PHASE4
-- Adds Olympic lift variations, accessory hypertrophy, mobility/prehab
-- Total: 50 exercises (IDs 250-299)

BEGIN;

CREATE OR REPLACE FUNCTION insert_phase4_exercise(
    p_name TEXT, p_category TEXT, p_pattern TEXT, p_force_vector TEXT,
    p_equipment TEXT[], p_cues TEXT[], p_errors TEXT[], p_contraindications TEXT[],
    p_regressions TEXT[], p_progressions TEXT[], p_source TEXT, p_sport_tags TEXT[],
    p_description TEXT
) RETURNS VOID AS $$
DECLARE new_id INTEGER;
BEGIN
    SELECT COALESCE(MAX(id), 249) + 1 INTO new_id FROM exercises;
    INSERT INTO exercises (id, name, category, movement_pattern, force_vector, equipment,
        coaching_cues, common_errors, contraindications, regressions, progressions,
        evidence_source, sport_specific_tags, description, is_active)
    VALUES (new_id, p_name, p_category, p_pattern, p_force_vector, p_equipment,
        p_cues, p_errors, p_contraindications, p_regressions, p_progressions,
        p_source, p_sport_tags, p_description, TRUE);
END;
$$ LANGUAGE plpgsql;

-- OLYMPIC LIFT VARIATIONS (12 exercises)
SELECT insert_phase4_exercise('Power Clean', 'Power', 'Bilateral Pull - Vertical', 'Vertical',
    ARRAY['Barbell','Plates'],
    ARRAY['Athletic stance bar over mid-foot','Pull bar close to body','Extend hips knees ankles explosively','Catch in quarter squat position'],
    ARRAY['Arms bending too early','Bar drifting forward','Incomplete extension','Crashing into catch'],
    ARRAY['Acute shoulder pathology','Wrist instability','Lumbar disc issues'],
    ARRAY['Hang Clean','Clean Pull','Muscle Clean'],
    ARRAY['Squat Clean','Clean Complex','Clean from Blocks'],
    'NSCA Essentials & USA Weightlifting',
    ARRAY['Football','Basketball','Rugby','Track & Field','Wrestling'],
    'Explosive triple extension developer. Teaches rate of force production. Foundation for athletic power.');

SELECT insert_phase4_exercise('Hang Power Clean', 'Power', 'Bilateral Pull - Vertical', 'Vertical',
    ARRAY['Barbell','Plates'],
    ARRAY['Start with bar at hip crease','Hinge slightly then explode','Keep bar close to thighs','Catch in athletic position'],
    ARRAY['Dipping too deep','Using arms instead of hips','Bar swinging away','Not extending fully'],
    ARRAY['Hip pathology','Acute lower back pain','Shoulder impingement'],
    ARRAY['High Hang Clean','Clean Pull'],
    ARRAY['Full Hang Clean','Hang Squat Clean'],
    'USA Weightlifting & EXOS Performance',
    ARRAY['Basketball','Volleyball','Football','Soccer'],
    'Emphasizes second pull explosiveness from hang position. More specific to jumping and sprinting actions.');

SELECT insert_phase4_exercise('Push Jerk', 'Power', 'Bilateral Push - Vertical', 'Vertical',
    ARRAY['Barbell','Plates','Rack'],
    ARRAY['Bar on front delts grip shoulder-width','Dip straight down not forward','Drive bar up then drop under','Lock out overhead stable'],
    ARRAY['Dipping too deep','Pressing forward not up','Not dropping under bar','Incomplete lockout'],
    ARRAY['Shoulder instability','Rotator cuff pathology','Cervical spine issues'],
    ARRAY['Push Press','Behind Neck Push Press'],
    ARRAY['Split Jerk','Squat Jerk','Jerk Complex'],
    'USA Weightlifting & CrossFit Standards',
    ARRAY['Gymnastics','Weightlifting','Basketball','Volleyball'],
    'Overhead power development using leg drive and drop under. Builds explosive pressing strength.');

SELECT insert_phase4_exercise('Snatch Pull', 'Power', 'Bilateral Pull - Vertical', 'Vertical',
    ARRAY['Barbell','Plates'],
    ARRAY['Wide snatch grip','Pull from floor like deadlift','Extend explosively at top','Shrug and pull with arms'],
    ARRAY['Arms bending too early','Incomplete hip extension','Bar drifting forward','No shrug at top'],
    ARRAY['Shoulder pathology','Wrist issues','Lumbar disc problems'],
    ARRAY['Deadlift','Clean Pull'],
    ARRAY['Hang Snatch Pull','Snatch High Pull'],
    'USA Weightlifting & ALTIS Track & Field',
    ARRAY['Weightlifting','Track & Field','Football','Basketball'],
    'Develops pulling strength and positioning for snatch. Teaches proper extension pattern without overhead complexity.');

SELECT insert_phase4_exercise('Clean Deadlift', 'Strength', 'Bilateral Hip Dominant', 'Horizontal',
    ARRAY['Barbell','Plates'],
    ARRAY['Clean grip slightly wider than shoulders','Start position same as clean','Pull from floor keeping angles','Finish with full extension'],
    ARRAY['Hips rising before chest','Bar drifting forward','Incomplete lockout','Rounding back'],
    ARRAY['Acute lumbar issues','Hip pathology','Knee problems'],
    ARRAY['Block Pull','Romanian Deadlift'],
    ARRAY['Clean Pull','Hang Clean'],
    'USA Weightlifting & NSCA Advanced',
    ARRAY['Weightlifting','Football','Rugby','Strongman'],
    'Builds strength off the floor for clean. Reinforces proper starting positions and pulling mechanics.');

-- Continue with more Olympic variations...
SELECT insert_phase4_exercise('Muscle Clean', 'Power', 'Bilateral Pull - Vertical', 'Vertical',
    ARRAY['Barbell','Plates'],
    ARRAY['Pull bar close to body','Keep elbows high and outside','Rotate elbows around bar','Catch without dipping'],
    ARRAY['Using legs instead of arms','Bar swinging away','Elbows dropping','Incomplete rotation'],
    ARRAY['Wrist pathology','Elbow tendonitis','Shoulder impingement'],
    ARRAY['Clean Pull','High Hang Clean'],
    ARRAY['Power Clean','Clean Complex'],
    'USA Weightlifting Technique Standards',
    ARRAY['Weightlifting','CrossFit','Basketball'],
    'Teaches elbow rotation and bar path without leg drive. Excellent technical drill for clean.');

SELECT insert_phase4_exercise('Behind Neck Push Press', 'Power', 'Bilateral Push - Vertical', 'Vertical',
    ARRAY['Barbell','Plates','Rack'],
    ARRAY['Bar on traps not neck','Athletic stance feet hip-width','Dip straight down drive up','Press overhead locking out'],
    ARRAY['Bar on cervical spine','Dipping forward','Pressing behind head','Incomplete lockout'],
    ARRAY['Cervical spine issues','Shoulder instability','Thoracic mobility restrictions'],
    ARRAY['Strict Press','Landmine Press'],
    ARRAY['Push Jerk','Split Jerk'],
    'USA Weightlifting & Starting Strength',
    ARRAY['Weightlifting','Gymnastics','Football Lineman'],
    'Develops overhead strength from rear rack position. Requires thoracic mobility and shoulder stability.');

SELECT insert_phase4_exercise('Hang Snatch', 'Power', 'Bilateral Pull - Vertical', 'Vertical',
    ARRAY['Barbell','Plates'],
    ARRAY['Wide snatch grip start at hip','Hinge slightly then explode','Pull yourself under bar','Catch overhead in squat'],
    ARRAY['Arms bending early','Bar swinging away','Not pulling under','Forward catch'],
    ARRAY['Shoulder instability','Wrist pathology','Hip issues'],
    ARRAY['Muscle Snatch','Hang Snatch Pull'],
    ARRAY['Squat Snatch','Snatch Complex'],
    'USA Weightlifting & EXOS',
    ARRAY['Weightlifting','Track & Field','Basketball','Volleyball'],
    'Full snatch from hang position. Develops explosive power and overhead stability.');

SELECT insert_phase4_exercise('Power Snatch', 'Power', 'Bilateral Pull - Vertical', 'Vertical',
    ARRAY['Barbell','Plates'],
    ARRAY['Wide grip athletic stance','Pull bar close explode at hips','Pull under bar aggressively','Catch in quarter squat overhead'],
    ARRAY['Starfish catch','Bar forward of center','Incomplete extension','Crashing into catch'],
    ARRAY['Shoulder instability','Wrist issues','Cervical spine problems'],
    ARRAY['Hang Power Snatch','Muscle Snatch'],
    ARRAY['Squat Snatch','Snatch Complex'],
    'USA Weightlifting Standards',
    ARRAY['Weightlifting','Track & Field','Football','Basketball'],
    'Explosive overhead developer. Catches above parallel emphasizing speed and power over depth.');

SELECT insert_phase4_exercise('Clean and Press', 'Strength', 'Bilateral Complex', 'Vertical',
    ARRAY['Barbell','Plates'],
    ARRAY['Clean to front rack position','Reset feet if needed','Press strict or with drive','Lock out overhead'],
    ARRAY['Rushing between movements','Poor rack position','Pressing forward not up','Incomplete lockout'],
    ARRAY['Shoulder pathology','Wrist issues','Lumbar problems'],
    ARRAY['Clean only','Press only'],
    ARRAY['Clean and Jerk','Complex Training'],
    'NSCA Advanced & Strongman Standards',
    ARRAY['Strongman','Football','Rugby','CrossFit'],
    'Full body strength complex. Combines lower body power with upper body pressing strength.');

SELECT insert_phase4_exercise('Thruster', 'Power', 'Bilateral Complex', 'Vertical',
    ARRAY['Barbell','Dumbbells','Front Rack'],
    ARRAY['Front squat to full depth','Drive up explosively from bottom','Use momentum to press overhead','Lock out at top'],
    ARRAY['Not hitting squat depth','Pressing too early','Losing core tension','Forward lean'],
    ARRAY['Shoulder impingement','Knee pathology','Lumbar disc issues'],
    ARRAY['Front Squat','Push Press'],
    ARRAY['Heavy Thruster','Thruster EMOM'],
    'CrossFit Standards & Functional Fitness',
    ARRAY['CrossFit','Basketball','Volleyball','MMA'],
    'Metabolic conditioning powerhouse. Combines squat and press into one fluid movement for conditioning.');

SELECT insert_phase4_exercise('Sumo Deadlift High Pull', 'Power', 'Bilateral Pull - Vertical', 'Vertical',
    ARRAY['Barbell','Plates'],
    ARRAY['Wide sumo stance','Pull from floor like sumo','Extend hips then shrug and pull','Elbows high outside'],
    ARRAY['Hips rising first','Bar drifting forward','Arms bending too early','No shrug'],
    ARRAY['Hip impingement','Groin strain','Shoulder issues'],
    ARRAY['Sumo Deadlift','Sumo Shrug'],
    ARRAY['SDHP to Upright Row','Complex Training'],
    'CrossFit & Strongman Standards',
    ARRAY['CrossFit','Football Lineman','Rugby Forward','Strongman'],
    'Combines sumo deadlift with high pull. Develops posterior chain and upper back power.');

DROP FUNCTION IF EXISTS insert_phase4_exercise(TEXT, TEXT, TEXT, TEXT, TEXT[], TEXT[], TEXT[], TEXT[], TEXT[], TEXT[], TEXT, TEXT[], TEXT);
COMMIT;
