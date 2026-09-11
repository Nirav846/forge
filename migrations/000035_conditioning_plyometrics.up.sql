-- Phase 35A: Conditioning Expansion - Plyometrics & Jump Training
-- Adds 40+ plyometric exercises for power development

-- Add new tags
INSERT INTO tags (name, description) VALUES 
('Plyometric', 'Explosive stretch-shortening cycle movements'),
('Jump Training', 'Vertical and horizontal jump development'),
('Depth Jump', 'Reactive jump training from elevated surface'),
('Bounding', 'Exaggerated running pattern for power'),
('Shock Method', 'High-intensity plyometric training')
ON CONFLICT (name) DO NOTHING;

-- Get tag IDs
DO $$
DECLARE
    plyo_tag INTEGER;
    jump_tag INTEGER;
    depth_tag INTEGER;
    bound_tag INTEGER;
    shock_tag INTEGER;
BEGIN
    SELECT id INTO plyo_tag FROM tags WHERE name = 'Plyometric';
    SELECT id INTO jump_tag FROM tags WHERE name = 'Jump Training';
    SELECT id INTO depth_tag FROM tags WHERE name = 'Depth Jump';
    SELECT id INTO bound_tag FROM tags WHERE name = 'Bounding';
    SELECT id INTO shock_tag FROM tags WHERE name = 'Shock Method';

    -- VERTICAL JUMP PLYOMETRICS (12 exercises)
    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_vert_01', 'Countermovement Jump', 'EXPLOSIVE', 
     'Stand with feet shoulder-width apart. Rapidly dip down by flexing hips and knees to approximately 90 degrees, then immediately explode upward into a maximal vertical jump. Swing arms aggressively overhead during takeoff. Land softly on midfoot, absorbing impact through hips and knees. Reset completely between jumps.',
     'Bodyweight', ARRAY['Quads', 'Glutes', 'Calves'], ARRAY['Hip Flexors', 'Core'], 
     'Add arm swing emphasis, increase dip speed, or add light dumbbells (5-10% BW)', 
     'Reduce dip depth, perform squat jump without countermovement, or use box for assistance',
     'Dipping too deep (>90°), slow transition from eccentric to concentric, landing stiff-legged, not using arm swing',
     '4-6 sets x 3-5 reps, 2-3 min rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_vert_02', 'Squat Jump', 'EXPLOSIVE', 
     'Start in quarter squat position (knees at 45°). Without any preliminary dip, explode upward into maximal vertical jump. Focus on rate of force development from static position. Swing arms forcefully during takeoff. Land with soft knees and reset to starting position before next rep.',
     'Bodyweight', ARRAY['Quads', 'Glutes', 'Calves'], ARRAY['Hip Flexors', 'Core'],
     'Add light load (vest 5-10% BW), increase hold time in bottom position, or perform from deeper squat',
     'Reduce squat depth, use arm support for balance, or decrease jump height focus',
     'Rocking back before jumping, incomplete hip extension at takeoff, landing with locked knees, inconsistent starting position',
     '4-5 sets x 4-6 reps, 2-3 min rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_vert_03', 'Approach Jump', 'EXPLOSIVE', 
     'Take 3-5 preparatory steps building to moderate speed, then plant both feet and convert horizontal momentum into vertical jump. Use penultimate step to lower center of mass, then explosive double-leg takeoff. Swing arms from behind body to overhead. Emphasize rapid ground contact and maximal height.',
     'Bodyweight', ARRAY['Quads', 'Glutes', 'Calves'], ARRAY['Hip Flexors', 'Hamstrings'],
     'Increase approach speed, add more steps, or jump toward target (basketball rim, volleyball net)',
     'Reduce approach to 1-2 steps, eliminate arm swing initially, or focus on technique over height',
     'Taking steps too slowly, not converting horizontal to vertical force, poor arm timing, landing off-balance',
     '4-6 sets x 3-5 reps, 2-3 min rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_vert_04', 'Tuck Jump', 'EXPLOSIVE', 
     'Perform maximal vertical jump while simultaneously pulling knees toward chest at peak height. Bring thighs to parallel or higher, grasping shins if flexibility allows. Extend legs before landing and absorb impact with soft knees. Focus on explosive hip flexion and rapid knee pull.',
     'Bodyweight', ARRAY['Hip Flexors', 'Quads', 'Core'], ARRAY['Glutes', 'Calves'],
     'Increase tuck height (chest to knees), add multiple tucks in flight, or jump from box',
     'Reduce tuck depth, focus on jump height first, or perform standing knee drive without jump',
     'Not achieving full hip flexion, leaning forward excessively, landing before full leg extension, insufficient jump height',
     '3-5 sets x 4-6 reps, 2 min rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_vert_05', 'Pike Jump', 'EXPLOSIVE', 
     'Execute maximal vertical jump while extending legs straight forward at peak height, creating pike position. Keep legs together and toes pointed, reaching hands toward toes. Maintain straight trunk and extend hips fully before landing. Requires significant hamstring flexibility and core strength.',
     'Bodyweight', ARRAY['Hip Flexors', 'Core', 'Hamstrings'], ARRAY['Quads', 'Calves'],
     'Increase leg extension height, hold pike longer, or add rotation in pike position',
     'Perform tuck jump instead, reduce leg extension angle, or practice pike hold on ground first',
     'Bending knees during pike, rounding lower back, insufficient jump height, landing with straight legs',
     '3-4 sets x 4-5 reps, 2 min rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_vert_06', 'Single Leg Jump', 'EXPLOSIVE', 
     'Stand on one leg with slight knee flexion. Rapidly dip and explode into maximal vertical jump off single leg. Drive opposite knee upward during takeoff for momentum. Land on same leg, absorbing impact through hip and knee. Complete all reps on one side before switching.',
     'Bodyweight', ARRAY['Quads', 'Glutes', 'Calves'], ARRAY['Hip Flexors', 'Core'],
     'Add arm swing, increase dip speed, or jump to target (box, line)',
     'Use two-finger touch for balance, reduce jump height, or perform double-leg initially',
     'Knee valgus on landing, insufficient hip extension, losing balance, landing too stiffly',
     '3-4 sets x 4-5 reps each leg, 90 sec rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_vert_07', 'Alternating Single Leg Jump', 'EXPLOSIVE', 
     'Perform single leg jump, land, and immediately transition to jump off opposite leg without pause. Create rapid rhythm like skipping but with maximal vertical intent on each jump. Minimize ground contact time while maintaining jump height. Arms alternate naturally with leg action.',
     'Bodyweight', ARRAY['Quads', 'Glutes', 'Calves'], ARRAY['Hip Flexors', 'Core'],
     'Increase jump height, reduce ground contact time, or add arm swing emphasis',
     'Slow the tempo initially, reduce jump height for control, or march in place first',
     'Long ground contact times, asymmetrical jump heights, poor landing mechanics, rushing at expense of quality',
     '3-4 sets x 6-8 total reps, 90 sec rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_vert_08', 'Split Squat Jump', 'EXPLOSIVE', 
     'Start in lunge position with one foot forward, one foot back. Dip slightly then explode upward, switching leg positions in mid-air. Land softly in lunge with opposite foot forward. Continue alternating legs with each jump. Maintain upright torso throughout movement.',
     'Bodyweight', ARRAY['Quads', 'Glutes', 'Calves'], ARRAY['Hip Flexors', 'Hamstrings'],
     'Increase jump height, accelerate leg switch speed, or add light dumbbells',
     'Perform stationary lunge jumps without leg switch, reduce range of motion, or hold onto support',
     'Landing with front knee past toes, excessive forward lean, incomplete leg switch, landing heavily',
     '3-4 sets x 6-8 reps each leg, 90 sec rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_vert_09', 'Broad Jump to Vertical', 'EXPLOSIVE', 
     'Perform maximal horizontal broad jump, land, and immediately transition into maximal vertical jump. Absorb broad jump landing then redirect forces vertically without pause. Focus on rapid transition and changing force vector from horizontal to vertical.',
     'Bodyweight', ARRAY['Quads', 'Glutes', 'Calves'], ARRAY['Hamstrings', 'Hip Flexors'],
     'Increase broad jump distance, minimize transition time, or add multiple vertical jumps',
     'Reduce broad jump distance, pause between jumps initially, or perform jumps separately',
     'Long pause between jumps, poor landing from broad jump, not redirecting force effectively, losing balance',
     '3-4 sets x 4-5 combos, 2 min rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_vert_10', 'Seated Box Jump', 'EXPLOSIVE', 
     'Sit on box (knees at 90°) with feet flat on floor. Without rocking or using hands, explosively stand and jump onto higher box in front. Land softly in quarter squat on top box. Stand fully before stepping down. Eliminates stretch reflex, emphasizing concentric power.',
     'Box', ARRAY['Quads', 'Glutes', 'Calves'], ARRAY['Hip Flexors', 'Core'],
     'Increase box height, add light load, or reduce seated time before jump',
     'Use lower box, allow slight rock-back initially, or perform from standing',
     'Using hands to push off thighs, rocking backward before jumping, landing on shins, not standing fully on top',
     '4-5 sets x 3-5 reps, 2-3 min rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_vert_11', 'Hurdle Hop (vertical)', 'EXPLOSIVE', 
     'Set up mini-hurdles or cones in line (6-12 inches high). Perform continuous two-foot hops over each hurdle, focusing on minimal ground contact time and maximal rebound. Land on balls of feet, immediately springing to next hurdle. Arms provide rhythm and lift.',
     'Hurdles', ARRAY['Calves', 'Quads', 'Glutes'], ARRAY['Hip Flexors', 'Core'],
     'Increase hurdle height, add more hurdles, or reduce spacing for quicker contacts',
     'Lower hurdle height, increase spacing, or hop in place without hurdles first',
     'Long ground contact times, landing flat-footed, hitting hurdles, excessive knee bend on landing',
     '3-4 sets x 6-10 hurdles, 90 sec rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_vert_12', 'Repeated Tuck Jumps', 'EXPLOSIVE', 
     'Perform consecutive tuck jumps with minimal ground contact time between reps. Upon landing, immediately dip and explode into next tuck jump. Maintain consistent height and tuck position for prescribed duration or reps. Emphasizes reactive strength and power endurance.',
     'Bodyweight', ARRAY['Hip Flexors', 'Quads', 'Core'], ARRAY['Glutes', 'Calves'],
     'Increase number of consecutive jumps, maximize tuck height, or extend set duration',
     'Pause between jumps initially, reduce tuck depth, or perform single tuck jumps',
     'Decreasing jump height with fatigue, shallow tucks, long ground contacts, poor landing mechanics late in set',
     '3-4 sets x 6-10 reps or 10-20 sec, 2 min rest');

    -- HORIZONTAL JUMP PLYOMETRICS (10 exercises)
    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_horiz_01', 'Standing Broad Jump', 'EXPLOSIVE', 
     'Stand with feet shoulder-width apart. Dip into quarter squat, swing arms back, then explode forward and upward into maximal horizontal jump. Land with both feet simultaneously, absorbing impact by sitting back into hips. Measure distance and aim to improve.',
     'Bodyweight', ARRAY['Quads', 'Glutes', 'Calves'], ARRAY['Hamstrings', 'Hip Flexors'],
     'Add arm swing emphasis, increase dip speed, or jump to target markers',
     'Reduce jump intensity, shorten dip, or practice landing mechanics first',
     'Taking step before jump, landing with feet staggered, falling backward on landing, incomplete arm swing',
     '4-6 sets x 3-5 reps, 2-3 min rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_horiz_02', 'Single Leg Broad Jump', 'EXPLOSIVE', 
     'Stand on one leg with slight knee bend. Swing arms and non-jumping leg back, then explode forward into maximal horizontal jump off single leg. Land on same leg, absorbing impact through hip and knee. Hold landing for 2 seconds. Complete all reps before switching legs.',
     'Bodyweight', ARRAY['Quads', 'Glutes', 'Calves'], ARRAY['Hip Flexors', 'Core'],
     'Increase jump distance, add arm swing, or land into immediate next jump',
     'Use toe touch for balance, reduce jump distance, or perform double-leg initially',
     'Knee valgus on landing, insufficient hip extension, falling sideways, landing stiffly',
     '3-4 sets x 4-5 reps each leg, 2 min rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_horiz_03', 'Alternating Leg Bound', 'EXPLOSIVE', 
     'Perform exaggerated running bounds, emphasizing horizontal distance with each stride. Push off powerfully from rear leg, driving opposite knee forward. Cover maximum distance per bound while maintaining rhythm. Arms drive opposite to legs. Focus on ground contact quality over frequency.',
     'Bodyweight', ARRAY['Glutes', 'Quads', 'Calves'], ARRAY['Hamstrings', 'Hip Flexors'],
     'Increase bound distance, accelerate tempo, or add more consecutive bounds',
     'Reduce bound distance, slow tempo for control, or march with high knees first',
     'Short choppy bounds, landing on heels, poor arm action, losing forward lean',
     '3-4 sets x 6-8 bounds each leg, 2 min rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_horiz_04', 'Double Leg Bound', 'EXPLOSIVE', 
     'Stand with feet together. Perform continuous forward bounds using both feet simultaneously, like a frog jump. Swing arms forcefully, landing and immediately rebounding into next bound. Cover maximum distance while maintaining quick ground contacts.',
     'Bodyweight', ARRAY['Quads', 'Glutes', 'Calves'], ARRAY['Hip Flexors', 'Core'],
     'Increase bound distance, add more consecutive bounds, or reduce ground contact time',
     'Reduce bound distance, pause between bounds initially, or perform in place first',
     'Long ground contacts, landing flat-footed, not using arm swing, bounding too high instead of far',
     '3-4 sets x 6-10 bounds, 2 min rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_horiz_05', 'Skips for Distance', 'EXPLOSIVE', 
     'Perform exaggerated skipping motion, emphasizing horizontal propulsion with each skip. Drive knee up and forward while pushing off ground leg powerfully. Cover maximum distance per skip. Arms drive vigorously opposite to legs. Maintain tall posture throughout.',
     'Bodyweight', ARRAY['Hip Flexors', 'Quads', 'Calves'], ARRAY['Glutes', 'Core'],
     'Increase skip distance, accelerate tempo, or extend distance covered',
     'Reduce skip distance, slow tempo, or practice high knee march first',
     'Short skips, landing on heels, not driving knee forward, excessive vertical component',
     '3-4 sets x 20-30m, 90 sec rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_horiz_06', 'Hop and Stick (horizontal)', 'EXPLOSIVE', 
     'Perform single leg hop forward for distance, landing and holding position for 3 seconds. Focus on powerful takeoff and stable landing. Knee should track over toes, trunk stable. Measure hop distance. Alternate legs between sets.',
     'Bodyweight', ARRAY['Quads', 'Glutes', 'Calves'], ARRAY['Hip Flexors', 'Core'],
     'Increase hop distance, add arm swing, or perform consecutive hops before sticking',
     'Reduce hop distance, use toe touch for balance, or hop in place first',
     'Knee valgus on landing, falling forward, hopping too short, not holding landing',
     '3-4 sets x 4-5 reps each leg, 90 sec rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_horiz_07', 'Continuous Broad Jumps', 'EXPLOSIVE', 
     'Perform consecutive standing broad jumps with minimal ground contact between reps. Upon landing, immediately dip and explode into next jump. Cover maximum total distance in prescribed reps. Emphasizes reactive strength and power maintenance.',
     'Bodyweight', ARRAY['Quads', 'Glutes', 'Calves'], ARRAY['Hamstrings', 'Hip Flexors'],
     'Increase number of jumps, maximize each jump distance, or reduce ground contact time',
     'Pause between jumps initially, reduce jump distance for quality, or perform singles',
     'Decreasing jump distance with fatigue, long ground contacts, poor landing mechanics, stumbling between jumps',
     '3-4 sets x 5-8 consecutive jumps, 2-3 min rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_horiz_08', 'Lateral Bound', 'EXPLOSIVE', 
     'Stand on one leg. Explode laterally off that leg, landing on opposite leg. Absorb impact with soft knee and hip, holding for 2 seconds. Immediately explode back to starting leg. Cover maximum lateral distance while maintaining control.',
     'Bodyweight', ARRAY['Hip Abductors', 'Glutes', 'Quads'], ARRAY['Adductors', 'Core'],
     'Increase lateral distance, reduce ground contact time, or add arm swing',
     'Reduce distance, hold onto wall for balance initially, or perform in place',
     'Knee valgus on landing, insufficient lateral push, landing stiffly, losing balance',
     '3-4 sets x 5-6 bounds each direction, 90 sec rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_horiz_09', 'Skater Bounds', 'EXPLOSIVE', 
     'Perform continuous lateral bounds side-to-side, mimicking ice skating motion. Push off powerfully from one leg, landing on opposite leg while trailing leg sweeps behind. Touch ground with opposite hand if needed for balance. Maintain rhythmic flow.',
     'Bodyweight', ARRAY['Hip Abductors', 'Glutes', 'Adductors'], ARRAY['Quads', 'Core'],
     'Increase bound distance, accelerate tempo, or eliminate ground touch',
     'Reduce bound distance, slow tempo, or use wall for support',
     'Short bounds, landing on inside edge of foot, not sweeping trail leg, losing rhythm',
     '3-4 sets x 8-12 bounds total, 90 sec rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_horiz_10', 'Triple Jump Drill', 'EXPLOSIVE', 
     'Perform triple jump sequence: hop (same leg), step (opposite leg), jump (both legs). Focus on maintaining horizontal velocity through all three phases. Execute each phase explosively while preparing for next. Emphasizes sequential power application.',
     'Bodyweight', ARRAY['Quads', 'Glutes', 'Calves'], ARRAY['Hamstrings', 'Hip Flexors'],
     'Increase distance of each phase, accelerate transition speed, or add full approach',
     'Practice each phase separately, reduce intensity, or perform walk-through first',
     'Losing momentum between phases, poor sequencing, landing flat-footed, not completing all three phases',
     '3-4 sets x 3-5 sequences each leg, 2-3 min rest');

    -- DEPTH JUMPS & REACTIVE PLYOMETRICS (10 exercises)
    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_depth_01', 'Depth Jump (low box)', 'EXPLOSIVE', 
     'Stand on 12-18 inch box. Step off (do not jump), land on both feet, and immediately explode into maximal vertical jump. Minimize ground contact time (<0.2 sec). Focus on reactive response, not depth. Land softly and reset.',
     'Box', ARRAY['Quads', 'Glutes', 'Calves'], ARRAY['Hamstrings', 'Core'],
     'Increase box height gradually (max 30"), add horizontal jump component, or reduce ground contact',
     'Use lower box (6-12"), pause briefly if needed, or perform countermovement jump',
     'Stepping off with jump, long ground contact, box too high causing slow response, landing stiffly',
     '3-4 sets x 4-5 reps, 2-3 min rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_depth_02', 'Depth Jump to Broad Jump', 'EXPLOSIVE', 
     'Step off 12-18 inch box, land on both feet, and immediately explode into maximal horizontal broad jump. Convert vertical impact into horizontal propulsion. Minimize ground contact time. Focus on reactive strength and force redirection.',
     'Box', ARRAY['Quads', 'Glutes', 'Calves'], ARRAY['Hamstrings', 'Hip Flexors'],
     'Increase box height, maximize broad jump distance, or reduce ground contact time',
     'Use lower box, pause briefly if needed, or perform depth jump in place first',
     'Long ground contact, not redirecting force horizontally, box too high, poor landing from broad jump',
     '3-4 sets x 4-5 reps, 2-3 min rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_depth_03', 'Single Leg Depth Jump', 'EXPLOSIVE', 
     'Stand on one leg on 6-12 inch box. Step off, land on same leg, and immediately explode into vertical or horizontal jump. Extremely demanding - prioritize quality over height. Land on same leg, absorbing impact. Complete reps before switching.',
     'Box', ARRAY['Quads', 'Glutes', 'Calves'], ARRAY['Hip Flexors', 'Core'],
     'Increase box height slightly, add jump distance, or perform consecutive reps',
     'Use very low box (4-6"), hold onto support, or perform double-leg initially',
     'Knee valgus collapse, box too high, long ground contact, losing balance on landing',
     '2-3 sets x 3-4 reps each leg, 2-3 min rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_depth_04', 'Depth Drop to Stick', 'EXPLOSIVE', 
     'Step off 18-24 inch box, land on both feet, and absorb impact into athletic position without any subsequent jump. Focus purely on landing mechanics and force absorption. Hold landed position for 3 seconds. Develops deceleration strength.',
     'Box', ARRAY['Quads', 'Glutes', 'Calves'], ARRAY['Hamstrings', 'Core'],
     'Increase box height, add single leg variation, or reduce time to stable position',
     'Use lower box (12-18"), allow brief pause, or practice landing from step',
     'Landing stiff-legged, knee valgus, excessive forward lean, not holding position',
     '3-4 sets x 5-6 reps, 90 sec rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_depth_05', 'Depth Jump Lateral', 'EXPLOSIVE', 
     'Stand on 12-18 inch box positioned sideways to landing area. Step off, land on both feet, and immediately explode laterally away from box. Minimize ground contact. Land softly and reset. Develops multi-directional reactive strength.',
     'Box', ARRAY['Quads', 'Glutes', 'Hip Abductors'], ARRAY['Calves', 'Adductors'],
     'Increase box height, maximize lateral distance, or reduce ground contact time',
     'Use lower box, reduce lateral distance, or perform depth jump forward first',
     'Long ground contact, insufficient lateral push, landing on inside edge, box too high',
     '3-4 sets x 4-5 reps each direction, 2 min rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_depth_06', 'Stair Depth Jump', 'EXPLOSIVE', 
     'Stand on stair or platform (12-24"). Step off, land on lower surface, and immediately rebound into next step down or jump. Creates continuous reactive stimulus. Maintain quick contacts and upright posture throughout descent.',
     'Stairs/Box', ARRAY['Quads', 'Glutes', 'Calves'], ARRAY['Hamstrings', 'Core'],
     'Increase stair height, add more consecutive steps, or accelerate tempo',
     'Use lower step, pause between steps initially, or step down without jump',
     'Long ground contacts, landing heavily, losing balance, looking down at feet',
     '3-4 sets x 4-6 steps, 2 min rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_depth_07', 'Depth Jump to Box', 'EXPLOSIVE', 
     'Step off 12-18" box, land, and immediately jump onto higher box (18-30") in front. Minimize ground contact between depth drop and box jump. Focus on reactive strength translating to vertical production. Stand fully on top box.',
     'Boxes', ARRAY['Quads', 'Glutes', 'Calves'], ARRAY['Hip Flexors', 'Core'],
     'Increase starting box height, increase target box height, or reduce ground contact',
     'Use lower boxes, pause briefly if needed, or perform depth jump without box',
     'Long ground contact, landing on shins, starting box too high, not standing on top',
     '3-4 sets x 4-5 reps, 2-3 min rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_depth_08', 'Ankle Bounce (pogo)', 'EXPLOSIVE', 
     'Stand tall with knees nearly locked. Bounce repeatedly using only ankle motion, keeping ground contact extremely brief (<0.1 sec). Arms stay still or provide minimal rhythm. Focus on calf stiffness and rapid rebound. Minimal knee and hip involvement.',
     'Bodyweight', ARRAY['Calves', 'Foot Intrinsics'], ARRAY['Quads'],
     'Increase bounce height, accelerate frequency, or extend duration',
     'Reduce bounce height, slow frequency for control, or hold onto support',
     'Bending knees excessively, landing flat-footed, bouncing too high, losing rhythm',
     '3-4 sets x 20-30 sec or 30-50 contacts, 60 sec rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_depth_09', 'Drop Sprint', 'EXPLOSIVE', 
     'Step off 12-18" box positioned behind sprint start. Upon landing, immediately accelerate into 10-20m sprint. Minimize ground contact before transitioning to sprint. Converts reactive strength into acceleration.',
     'Box', ARRAY['Quads', 'Glutes', 'Calves'], ARRAY['Hamstrings', 'Hip Flexors'],
     'Increase box height, extend sprint distance, or reduce transition time',
     'Use lower box, pause briefly before sprint, or practice landing first',
     'Long pause after landing, stumbling on transition, box too high, poor sprint mechanics',
     '3-4 sets x 1 rep, 2-3 min rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_depth_10', 'Depth Jump Series', 'EXPLOSIVE', 
     'Step off 12-18" box, land, and perform 3-5 consecutive maximal jumps with minimal ground contact. First jump is reactive from depth, subsequent jumps maintain rhythm. Focus on maintaining jump height and quick contacts throughout series.',
     'Box', ARRAY['Quads', 'Glutes', 'Calves'], ARRAY['Hip Flexors', 'Core'],
     'Increase box height, add more consecutive jumps, or reduce ground contact time',
     'Use lower box, reduce number of jumps, or pause between jumps initially',
     'Decreasing jump height with reps, long ground contacts, poor landing mechanics, losing rhythm',
     '3-4 sets x 1 series (3-5 jumps), 2-3 min rest');

    -- BOUNDING COMPLEXES (8 exercises)
    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_bound_01', 'Single Leg Bounding', 'EXPLOSIVE', 
     'Perform continuous bounds on single leg, covering maximum distance per bound. Drive free knee forward aggressively while pushing off ground leg. Land on same leg, absorb, and immediately rebound. Arms drive opposite to legs. Covers 30-50m.',
     'Bodyweight', ARRAY['Glutes', 'Quads', 'Calves'], ARRAY['Hip Flexors', 'Hamstrings'],
     'Increase bound distance, accelerate tempo, or extend total distance',
     'Reduce bound distance, slow tempo, or perform double-leg bounds first',
     'Short bounds, landing on heel, poor knee drive, losing forward lean',
     '3-4 sets x 30-50m, 2 min rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_bound_02', 'Weighted Vest Bounding', 'EXPLOSIVE', 
     'Wear weighted vest (5-10% bodyweight). Perform alternating leg bounds for distance, emphasizing powerful push-off and knee drive. The added load increases strength demand while maintaining plyometric intent. Remove vest for unweighted contrast.',
     'Weighted Vest', ARRAY['Glutes', 'Quads', 'Calves'], ARRAY['Hip Flexors', 'Core'],
     'Increase vest load up to 15%, increase bound distance, or extend total distance',
     'Reduce vest load to 3-5%, reduce bound distance, or perform unweighted first',
     'Overloading vest causing slow bounds, shortened stride, poor landing mechanics, excessive fatigue',
     '3-4 sets x 20-30m, 2-3 min rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_bound_03', 'Uphill Bounding', 'EXPLOSIVE', 
     'Perform alternating bounds up gentle hill (5-10° gradient). Incline increases resistance and emphasizes knee drive and hip extension. Maintain bounding form despite grade. Focus on powerful push-off and aggressive arm action.',
     'Bodyweight', ARRAY['Glutes', 'Quads', 'Calves'], ARRAY['Hip Flexors', 'Hamstrings'],
     'Increase hill gradient, extend distance, or accelerate tempo',
     'Use gentler slope, reduce distance, or walk through pattern first',
     'Leaning too far forward, short bounds, looking at feet, reduced arm drive',
     '3-4 sets x 20-40m, 2 min rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_bound_04', 'Bounding for Height', 'EXPLOSIVE', 
     'Perform alternating bounds emphasizing vertical component over horizontal distance. Drive knee upward aggressively, spending more time in air than ground. Land softly and immediately rebound. Creates different stimulus than distance bounding.',
     'Bodyweight', ARRAY['Hip Flexors', 'Quads', 'Glutes'], ARRAY['Calves', 'Core'],
     'Increase knee drive height, extend sequence length, or add arm swing emphasis',
     'Reduce knee height initially, slow tempo, or perform standard bounds first',
     'Insufficient knee drive, long ground contacts, bounding too flat, poor arm action',
     '3-4 sets x 20-30m, 90 sec rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_bound_05', 'Crossover Bound', 'EXPLOSIVE', 
     'Perform lateral bounds with crossing pattern: right leg bounds leftward, left leg crosses behind and bounds rightward. Creates multi-planar stimulus. Cover lateral distance with each bound. Arms counterbalance leg action.',
     'Bodyweight', ARRAY['Hip Abductors', 'Adductors', 'Glutes'], ARRAY['Quads', 'Core'],
     'Increase lateral distance, accelerate tempo, or extend total distance',
     'Reduce distance, slow tempo, or practice pattern walking first',
     'Crossing too close, insufficient lateral push, losing balance, poor foot placement',
     '3-4 sets x 15-20m each direction, 90 sec rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_bound_06', 'Bounding to Sprint', 'EXPLOSIVE', 
     'Perform 4-6 powerful bounds, then immediately transition into maximal sprint for 20-30m. Use bounds to prime nervous system, then express velocity in sprint. Smooth transition critical - do not decelerate between bound and sprint.',
     'Bodyweight', ARRAY['Glutes', 'Quads', 'Calves'], ARRAY['Hamstrings', 'Hip Flexors'],
     'Increase number of bounds, extend sprint distance, or accelerate transition',
     'Reduce bounds to 2-3, shorten sprint, or practice transition walking first',
     'Decelerating before sprint, poor bound quality, awkward transition, losing sprint form',
     '3-4 sets x 4-6 bounds + 20-30m sprint, 3 min rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_bound_07', 'Resisted Bounding', 'EXPLOSIVE', 
     'Attach light resistance band around waist held by partner behind. Perform alternating bounds against resistance for 15-25m. Band provides constant tension increasing strength demand. Partner maintains steady resistance without jerking.',
     'Band', ARRAY['Glutes', 'Quads', 'Calves'], ARRAY['Hip Flexors', 'Hamstrings'],
     'Increase band resistance, extend distance, or accelerate bound tempo',
     'Reduce band resistance, shorten distance, or perform unresisted first',
     'Partner applying too much resistance, altered bound mechanics, excessive forward lean',
     '3-4 sets x 15-25m, 2 min rest');

    INSERT INTO exercises (id, name, pattern, instructions, equipment, primary_muscles, secondary_muscles, progression, regression, common_mistakes, sets_reps_rest) VALUES
    ('plyo_bound_08', 'Bounding Complex', 'EXPLOSIVE', 
     'Perform sequence: 3 double-leg bounds, 4 alternating bounds each leg, 3 single-leg bounds on right, 3 on left. Continuous movement without pause. Combines different bounding patterns for comprehensive stimulus.',
     'Bodyweight', ARRAY['Glutes', 'Quads', 'Calves'], ARRAY['Hip Flexors', 'Core'],
     'Increase reps of each type, add more patterns, or extend total distance',
     'Reduce reps, pause between patterns initially, or perform patterns separately',
     'Losing form during complex, inconsistent bound quality, rushing through transitions',
     '3-4 sets x 1 complex, 2-3 min rest');

    -- Insert exercise-tag relationships
    INSERT INTO exercise_tags (exercise_id, tag_id)
    SELECT 'plyo_vert_01', plyo_tag UNION ALL SELECT 'plyo_vert_01', jump_tag UNION ALL
    SELECT 'plyo_vert_02', plyo_tag UNION ALL SELECT 'plyo_vert_02', jump_tag UNION ALL
    SELECT 'plyo_vert_03', plyo_tag UNION ALL SELECT 'plyo_vert_03', jump_tag UNION ALL
    SELECT 'plyo_vert_04', plyo_tag UNION ALL SELECT 'plyo_vert_04', jump_tag UNION ALL
    SELECT 'plyo_vert_05', plyo_tag UNION ALL SELECT 'plyo_vert_05', jump_tag UNION ALL
    SELECT 'plyo_vert_06', plyo_tag UNION ALL SELECT 'plyo_vert_06', jump_tag UNION ALL
    SELECT 'plyo_vert_07', plyo_tag UNION ALL SELECT 'plyo_vert_07', jump_tag UNION ALL
    SELECT 'plyo_vert_08', plyo_tag UNION ALL SELECT 'plyo_vert_08', jump_tag UNION ALL
    SELECT 'plyo_vert_09', plyo_tag UNION ALL SELECT 'plyo_vert_09', jump_tag UNION ALL
    SELECT 'plyo_vert_10', plyo_tag UNION ALL SELECT 'plyo_vert_10', jump_tag UNION ALL
    SELECT 'plyo_vert_11', plyo_tag UNION ALL SELECT 'plyo_vert_11', jump_tag UNION ALL
    SELECT 'plyo_vert_12', plyo_tag UNION ALL SELECT 'plyo_vert_12', jump_tag UNION ALL
    SELECT 'plyo_horiz_01', plyo_tag UNION ALL SELECT 'plyo_horiz_01', jump_tag UNION ALL
    SELECT 'plyo_horiz_02', plyo_tag UNION ALL SELECT 'plyo_horiz_02', jump_tag UNION ALL
    SELECT 'plyo_horiz_03', plyo_tag UNION ALL SELECT 'plyo_horiz_03', bound_tag UNION ALL
    SELECT 'plyo_horiz_04', plyo_tag UNION ALL SELECT 'plyo_horiz_04', jump_tag UNION ALL
    SELECT 'plyo_horiz_05', plyo_tag UNION ALL SELECT 'plyo_horiz_05', bound_tag UNION ALL
    SELECT 'plyo_horiz_06', plyo_tag UNION ALL SELECT 'plyo_horiz_06', jump_tag UNION ALL
    SELECT 'plyo_horiz_07', plyo_tag UNION ALL SELECT 'plyo_horiz_07', jump_tag UNION ALL
    SELECT 'plyo_horiz_08', plyo_tag UNION ALL SELECT 'plyo_horiz_08', bound_tag UNION ALL
    SELECT 'plyo_horiz_09', plyo_tag UNION ALL SELECT 'plyo_horiz_09', bound_tag UNION ALL
    SELECT 'plyo_horiz_10', plyo_tag UNION ALL SELECT 'plyo_horiz_10', jump_tag UNION ALL
    SELECT 'plyo_depth_01', plyo_tag UNION ALL SELECT 'plyo_depth_01', depth_tag UNION ALL SELECT 'plyo_depth_01', shock_tag UNION ALL
    SELECT 'plyo_depth_02', plyo_tag UNION ALL SELECT 'plyo_depth_02', depth_tag UNION ALL SELECT 'plyo_depth_02', shock_tag UNION ALL
    SELECT 'plyo_depth_03', plyo_tag UNION ALL SELECT 'plyo_depth_03', depth_tag UNION ALL SELECT 'plyo_depth_03', shock_tag UNION ALL
    SELECT 'plyo_depth_04', plyo_tag UNION ALL SELECT 'plyo_depth_04', depth_tag UNION ALL
    SELECT 'plyo_depth_05', plyo_tag UNION ALL SELECT 'plyo_depth_05', depth_tag UNION ALL
    SELECT 'plyo_depth_06', plyo_tag UNION ALL SELECT 'plyo_depth_06', depth_tag UNION ALL
    SELECT 'plyo_depth_07', plyo_tag UNION ALL SELECT 'plyo_depth_07', depth_tag UNION ALL
    SELECT 'plyo_depth_08', plyo_tag UNION ALL SELECT 'plyo_depth_08', jump_tag UNION ALL
    SELECT 'plyo_depth_09', plyo_tag UNION ALL SELECT 'plyo_depth_09', shock_tag UNION ALL
    SELECT 'plyo_depth_10', plyo_tag UNION ALL SELECT 'plyo_depth_10', depth_tag UNION ALL
    SELECT 'plyo_bound_01', plyo_tag UNION ALL SELECT 'plyo_bound_01', bound_tag UNION ALL
    SELECT 'plyo_bound_02', plyo_tag UNION ALL SELECT 'plyo_bound_02', bound_tag UNION ALL
    SELECT 'plyo_bound_03', plyo_tag UNION ALL SELECT 'plyo_bound_03', bound_tag UNION ALL
    SELECT 'plyo_bound_04', plyo_tag UNION ALL SELECT 'plyo_bound_04', bound_tag UNION ALL
    SELECT 'plyo_bound_05', plyo_tag UNION ALL SELECT 'plyo_bound_05', bound_tag UNION ALL
    SELECT 'plyo_bound_06', plyo_tag UNION ALL SELECT 'plyo_bound_06', bound_tag UNION ALL
    SELECT 'plyo_bound_07', plyo_tag UNION ALL SELECT 'plyo_bound_07', bound_tag UNION ALL
    SELECT 'plyo_bound_08', plyo_tag UNION ALL SELECT 'plyo_bound_08', bound_tag
    ON CONFLICT DO NOTHING;
END $$;
