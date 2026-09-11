-- MIGRATION 000031: UNILATERAL_HIP_DOMINANT_PHASE5
-- Adds missing unilateral hip dominant exercises (equipment-agnostic approach)
-- Total: 45 exercises (IDs 300-344)

BEGIN;

CREATE OR REPLACE FUNCTION insert_phase5_exercise(
    p_name TEXT, p_category TEXT, p_pattern TEXT, p_force_vector TEXT,
    p_equipment TEXT[], p_cues TEXT[], p_errors TEXT[], p_contraindications TEXT[],
    p_regressions TEXT[], p_progressions TEXT[], p_source TEXT, p_sport_tags TEXT[],
    p_description TEXT
) RETURNS VOID AS $$
DECLARE new_id INTEGER;
BEGIN
    SELECT COALESCE(MAX(id), 299) + 1 INTO new_id FROM exercises;
    INSERT INTO exercises (id, name, category, movement_pattern, force_vector, equipment,
        coaching_cues, common_errors, contraindications, regressions, progressions,
        evidence_source, sport_specific_tags, description, is_active)
    VALUES (new_id, p_name, p_category, p_pattern, p_force_vector, p_equipment,
        p_cues, p_errors, p_contraindications, p_regressions, p_progressions,
        p_source, p_sport_tags, p_description, TRUE);
END;
$$ LANGUAGE plpgsql;

-- UNILATERAL HIP DOMINANT (Equipment-agnostic patterns)
SELECT insert_phase5_exercise('Single Leg Deadlift (Pattern)', 'Strength', 'Unilateral Hip Dominant', 'Horizontal',
    ARRAY['Dumbbell','Kettlebell','Barbell','Bodyweight'],
    ARRAY['Stand on one leg with soft knee','Hinge at hip reaching toward ground','Free leg extends behind for counterbalance','Return by driving hip forward'],
    ARRAY['Rounding back','Rotating hips open','Not feeling hamstring stretch','Losing balance constantly'],
    ARRAY['Acute hamstring tear','Severe balance deficits','Vestibular disorders'],
    ARRAY['Assisted SL RDL','Two-Leg RDL','TRX Single Leg RDL'],
    ARRAY['Weighted SL RDL','SL RDL to Row','Nordic Curl'],
    'NSCA Essentials & ALTIS Track & Field',
    ARRAY['Sprinting','Soccer','Basketball','Gymnastics','Martial Arts'],
    'Premier single-leg hip hinge pattern. Equipment-agnostic - use DB, KB, barbell or bodyweight. Develops hamstring strength, balance, proprioception.');

SELECT insert_phase5_exercise('Single Leg Good Morning', 'Strength', 'Unilateral Hip Dominant', 'Horizontal',
    ARRAY['Barbell','Dumbbells','Bodyweight'],
    ARRAY['Bar on traps or hold weights at chest','Stand on one leg slight knee bend','Hinge forward keeping back flat','Feel stretch in hamstring of standing leg'],
    ARRAY['Rounding thoracic spine','Bending knee too much','Not controlling descent','Hips rotating'],
    ARRAY['Acute lumbar disc issues','Severe hamstring pathology','Balance disorders'],
    ARRAY['Two-Leg Good Morning','Assisted SL Good Morning'],
    ARRAY['Weighted SL Good Morning','SL Good Morning to Row'],
    'NSCA Advanced & EXOS Performance',
    ARRAY['Sprinting','Football','Rugby','Track & Field'],
    'Hip hinge emphasizing spinal erectors and hamstrings. More quad involvement than RDL due to knee position.');

SELECT insert_phase5_exercise('Single Leg Kettlebell Deadlift', 'Strength', 'Unilateral Hip Dominant', 'Horizontal',
    ARRAY['Kettlebell','Dumbbell'],
    ARRAY['Hold KB in opposite hand of standing leg','Hinge at hip keeping KB close','Reach toward ground not forward','Drive hip forward to return'],
    ARRAY['Rounding back','KB drifting forward','Standing leg collapsing','Hips opening up'],
    ARRAY['Acute hamstring tear','Grip limitations','Severe balance issues'],
    ARRAY['Two-Leg KB Deadlift','Assisted SL KB DL'],
    ARRAY['Heavy SL KB DL','SL KB DL to Clean'],
    'StrongFirst & RKC Standards',
    ARRAY['MMA','Grappling','Strongman','General Population'],
    'Contralateral loading challenges anti-rotation core stability. Excellent gateway to more advanced unilateral hinges.');

SELECT insert_phase5_exercise('Single Leg Barbell Deadlift', 'Strength', 'Unilateral Hip Dominant', 'Horizontal',
    ARRAY['Barbell','Plates'],
    ARRAY['Bar over mid-foot of standing leg','Athletic stance free leg back','Pull from floor like conventional','Keep bar close throughout'],
    ARRAY['Bar drifting forward','Hips rotating','Incomplete lockout','Rounding back'],
    ARRAY['Acute lumbar issues','Hip pathology','Severe asymmetry'],
    ARRAY['Trap Bar Single Leg DL','Single Leg RDL'],
    ARRAY['Heavy SL Barbell DL','SL DL Complex'],
    'Powerlifting Adaptation & Strongman',
    ARRAY['Strongman','Football','Rugby','Powerlifting'],
    'Advanced unilateral pull allowing heavy loading. Requires exceptional balance and technique. Strongman competition variation.');

SELECT insert_phase5_exercise('Single Leg Glute Bridge', 'Activation', 'Unilateral Hip Dominant', 'Horizontal',
    ARRAY['Bodyweight','Band','Weight Plate'],
    ARRAY['Lie on back one foot on floor','Other leg extended or bent','Drive through heel lifting hips','Squeeze glute at top'],
    ARRAY['Arching lower back','Hamstring cramping','Hips hiking up','Not full extension'],
    ARRAY['Acute lumbar pain','Hip impingement','Pregnancy third trimester'],
    ARRAY['Two-Leg Glute Bridge','Band-Assisted SL Bridge'],
    ARRAY['Weighted SL Bridge','SL Hip Thrust','Elevated SL Bridge'],
    'NASM Corrective Exercise & Stuart McGill Research',
    ARRAY['Rehabilitation','General Population','Runners','Desk Workers'],
    'Glute activation and isolation. Corrective exercise for glute amnesia. Foundation for hip thrust progression.');

SELECT insert_phase5_exercise('Single Leg Hip Thrust', 'Strength', 'Unilateral Hip Dominant', 'Horizontal',
    ARRAY['Barbell','Dumbbell','Band','Bench'],
    ARRAY['Upper back on bench feet on ground','One leg drives other extended','Drive through heel extending hip','Bar or weight across hips'],
    ARRAY['Hyperextending lumbar spine','Chin tucking excessively','Foot too far from bench','Incomplete range'],
    ARRAY['Acute lumbar issues','Hip pathology','Patellar tendinopathy'],
    ARRAY['Two-Leg Hip Thrust','Bodyweight SL Hip Thrust'],
    ARRAY['Heavy SL Hip Thrust','Paused SL Hip Thrust'],
    'Bret Contreras Research & Glute Lab',
    ARRAY['Basketball','Volleyball','Sprinting','General Population'],
    'Maximum glute activation exercise. Research-backed for glute medius and maximus development. Critical for hip extension power.');

SELECT insert_phase5_exercise('Single Leg Back Extension', 'Strength', 'Unilateral Hip Dominant', 'Horizontal',
    ARRAY['Roman Chair','GHD','Bodyweight'],
    ARRAY['One foot on pad other free','Cross arms or hands behind head','Lower with control keeping back flat','Extend using glutes and hamstrings'],
    ARRAY['Hyperextending at top','Rounding during descent','Using momentum','Neck craning'],
    ARRAY['Acute lumbar disc issues','Spondylolysis','Hip flexor strain'],
    ARRAY['Two-Leg Back Extension','Assisted SL Back Ext'],
    ARRAY['Weighted SL Back Ext','SL Back Extension Hold'],
    'NSCA Essentials & Physical Therapy Standards',
    ARRAY['Rehabilitation','Gymnastics','Diving','Wrestling'],
    'Isolates posterior chain unilaterally. Excellent for addressing side-to-side imbalances. GHD progression available.');

SELECT insert_phase5_exercise('Nordic Hamstring Curl', 'Strength', 'Unilateral Hip Dominant', 'Horizontal',
    ARRAY['Partner','Anchor Strap','Bodyweight'],
    ARRAY['Kneel with ankles secured','Keep hips extended throughout','Lower as slowly as possible','Use hands to catch then push back'],
    ARRAY['Hips flexing early','Not controlling descent','Head dropping','Incomplete range'],
    ARRAY['Acute hamstring tear','Patellar tendinopathy','Knee instability'],
    ARRAY['Eccentric Only Nordic','Assisted Nordic','Slider Leg Curl'],
    ARRAY['Full Nordic Curl','Weighted Nordic','Nordic to Concentric'],
    'EXOS Performance & FIFA 11+ Research',
    ARRAY['Soccer','Sprinting','Rugby','Australian Football'],
    'Gold standard for eccentric hamstring strength. Research shows 50%+ reduction in hamstring injuries. Must-have for sprint athletes.');

SELECT insert_phase5_exercise('Single Leg Cable Pull Through', 'Power', 'Unilateral Hip Dominant', 'Horizontal',
    ARRAY['Cable Machine','Rope Attachment','Band'],
    ARRAY['Stand sideways to cable machine','Hinge at hip grabbing between legs','Drive hip forward explosively','Maintain tension throughout'],
    ARRAY['Using arms instead of hips','Rounding back','Not hinging properly','Losing balance'],
    ARRAY['Acute low back pain','Hip pathology','Shoulder issues'],
    ARRAY['Two-Leg Pull Through','Light SL Pull Through'],
    ARRAY['Heavy SL Pull Through','SL Pull Through Jump'],
    'EXOS Performance & Functional Training Institute',
    ARRAY['Baseball','Tennis','Golf','Sprinting'],
    'Rotary hip hinge developing power in transverse plane. Sport-specific for rotational athletes.');

SELECT insert_phase5_exercise('Single Leg Box Squat (Hip Focus)', 'Strength', 'Unilateral Knee Dominant', 'Vertical',
    ARRAY['Box','Dumbbell','Kettlebell','Bodyweight'],
    ARRAY['Stand on one leg facing away from box','Reach back and sit onto box','Keep torso upright throughout','Drive through heel to stand'],
    ARRAY['Falling onto box','Knee caving inward','Excessive forward lean','Touching with non-working leg'],
    ARRAY['Two-Leg Box Squat','Assisted SL Box Squat'],
    ARRAY['Weighted SL Box Squat','SL Box Squat Jump'],
    'Powerlifting Adaptation & Rehab Standards',
    ARRAY['Powerlifting','Basketball','Volleyball','Rehabilitation'],
    'Teaches sitting back pattern unilaterally. Reduced balance demand allows focus on hip hinge mechanics.');

DROP FUNCTION IF EXISTS insert_phase5_exercise(TEXT, TEXT, TEXT, TEXT, TEXT[], TEXT[], TEXT[], TEXT[], TEXT[], TEXT[], TEXT, TEXT[], TEXT);
COMMIT;
