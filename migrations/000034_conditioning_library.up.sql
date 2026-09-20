-- Migration 000034: Sport-Specific Conditioning Library
-- Adds resisted sprinting, assisted sprinting, and deceleration training
-- Based on CSCS speed development protocols

-- Add conditioning tags if not exist
INSERT INTO exercise_tags (name, description)
VALUES 
  ('Resisted Sprint', 'Sprinting against external resistance to develop acceleration and force production'),
  ('Assisted Sprint', 'Sprinting with external assistance to achieve supramaximal velocities'),
  ('Deceleration', 'Training to absorb braking forces and rapidly reduce momentum'),
  ('Speed Development', 'Exercises focused on improving linear sprint performance')
ON CONFLICT (name) DO NOTHING;

-- Insert conditioning exercises
INSERT INTO exercises 
  (id, name, pattern, instructions, equipment, primary_muscles, progression, regression, common_mistakes, sets_reps_rest, created_at, updated_at)
VALUES
  -- RESISTED SPRINTING (sp_res_01 to sp_res_07)
  (
    'sp_res_01',
    'Heavy Sled Push',
    'EXPLOSIVE',
    'Load a sled with heavy resistance (70-100% bodyweight). Assume a low push position with both hands on the sled uprights, arms locked, torso at a 45-degree angle to the ground. Drive aggressively with short powerful steps, maintaining forward lean throughout. Push for 10-20 meters focusing on maximal effort on every step.',
    'Sled',
    ARRAY['Glutes', 'Quads', 'Calves', 'Core'],
    'Increase sled load to 100-120% bodyweight or extend distance to 30m',
    'Reduce load to 50-60% bodyweight or shorten distance to 10m',
    'Rounding the lower back, taking steps too long, standing up too early, allowing elbows to bend',
    '4-6 sets x 10-20m, 2-3 min rest',
    NOW(),
    NOW()
  ),
  (
    'sp_res_02',
    'Light Sled Sprint',
    'EXPLOSIVE',
    'Attach a sled via waist harness with light resistance (10-30% bodyweight). Sprint at maximal velocity for 20-40 meters maintaining upright sprint mechanics. Focus on maintaining or increasing top speed rather than fighting the load. The resistance should be light enough to preserve sprint technique throughout.',
    'Sled',
    ARRAY['Hip Flexors', 'Glutes', 'Quads', 'Calves'],
    'Increase distance to 50m or slightly increase load',
    'Reduce load to 5-10% bodyweight or shorten distance to 15m',
    'Overloading the sled causing form breakdown, shortening stride length excessively, leaning too far forward, reducing arm drive',
    '5-8 sets x 20-40m, 2-3 min rest',
    NOW(),
    NOW()
  ),
  (
    'sp_res_03',
    'Band-Resisted Start',
    'EXPLOSIVE',
    'Anchor a heavy resistance band at waist height behind the athlete. Step forward to create tension, then assume a staggered two-point or three-point start position. On the signal, explode forward against band resistance for 10-15 meters. Focus on powerful first steps with aggressive ground contact and forward body lean.',
    'Band',
    ARRAY['Glutes', 'Quads', 'Calves', 'Core'],
    'Use a thicker band or extend distance to 20m',
    'Use a lighter band or reduce distance to 8m',
    'Starting with too much tension causing compensatory lean, popping up too quickly, incomplete hip extension on first steps, looking down at the ground',
    '4-6 sets x 10-15m, 2-3 min rest',
    NOW(),
    NOW()
  ),
  (
    'sp_res_04',
    'Partner Resistance Sprint',
    'EXPLOSIVE',
    'The athlete wears a waist harness connected to a resistance band or towel held by a partner behind them. Sprint forward at 80-95% effort for 15-25 meters while the partner provides consistent moderate resistance. The partner should maintain steady tension without jerking or suddenly releasing resistance.',
    'Bodyweight',
    ARRAY['Glutes', 'Quads', 'Calves', 'Core'],
    'Increase partner resistance or extend distance to 30m',
    'Reduce partner resistance or shorten distance to 10m',
    'Partner applying too much resistance, athlete compensating with excessive forward lean, inconsistent partner resistance, athlete decelerating before the finish',
    '4-6 sets x 15-25m, 2-3 min rest',
    NOW(),
    NOW()
  ),
  (
    'sp_res_05',
    'Weighted Vest Sprint',
    'EXPLOSIVE',
    'Wear a properly fitted weighted vest loaded to 5-15% bodyweight. Perform short sprints of 10-30 meters maintaining normal sprint mechanics. The vest should sit snug against the torso without shifting during running. Focus on maintaining arm drive, knee lift, and ground contact mechanics despite the added load.',
    'Bodyweight',
    ARRAY['Hip Flexors', 'Glutes', 'Quads', 'Calves'],
    'Increase vest load up to 20% bodyweight or extend sprint distance',
    'Reduce vest load to 3-5% bodyweight or shorten distance to 10m',
    'Overloading the vest causing form breakdown, shifting to shorter strides, reduced arm swing, leaning too far forward to compensate for weight',
    '5-8 sets x 10-30m, 2-3 min rest',
    NOW(),
    NOW()
  ),
  (
    'sp_res_06',
    'Resistance Band Sprint (waist)',
    'EXPLOSIVE',
    'Attach a resistance band around the waist with a partner or anchor point behind the athlete. Sprint forward against band tension for 15-30 meters maintaining upright sprint posture. The band should provide progressive resistance that peaks at maximal velocity. Focus on maintaining stride frequency and ground force production despite the resistance.',
    'Band',
    ARRAY['Hip Flexors', 'Glutes', 'Quads', 'Calves'],
    'Use a thicker band or increase sprint distance to 40m',
    'Use a lighter band or reduce distance to 10m',
    'Allowing the band to pull the hips backward, shortening stride excessively, reducing arm drive, not maintaining upright torso position',
    '5-6 sets x 15-30m, 2-3 min rest',
    NOW(),
    NOW()
  ),
  (
    'sp_res_07',
    'Hill Sprint',
    'EXPLOSIVE',
    'Find a hill with a moderate gradient of 5-10 degrees. Sprint uphill at maximal effort for 20-40 meters maintaining aggressive drive mechanics. Focus on powerful ground contacts, high knee drive, and strong arm action. The incline naturally enforces forward lean and exaggerated hip extension without external load.',
    'Bodyweight',
    ARRAY['Glutes', 'Quads', 'Calves', 'Core'],
    'Increase gradient, extend distance, or reduce rest periods',
    'Use a gentler gradient (3-5 degrees) or reduce distance to 15m',
    'Leaning too far forward at the trunk, taking overly long steps, looking down at the feet, allowing the arms to stop driving',
    '4-8 sets x 20-40m, 2-4 min rest',
    NOW(),
    NOW()
  ),

  -- ASSISTED SPRINTING (sp_assist_01 to sp_assist_05)
  (
    'sp_assist_01',
    'Band-Assisted Sprint',
    'EXPLOSIVE',
    'Anchor a light resistance band overhead or at chest height in front of the athlete. Hold the band with both hands and let it pull you forward slightly beyond normal sprint velocity. Sprint for 15-30 meters allowing the band to assist the acceleration phase. Maintain relaxed, efficient mechanics while running at supramaximal speed.',
    'Band',
    ARRAY['Hip Flexors', 'Glutes', 'Quads', 'Calves'],
    'Use a stronger band for greater assistance or increase distance',
    'Use a lighter band or reduce distance to 10m',
    'Tensing against the band instead of relaxing, overstriding due to excessive assistance, losing posture control, gripping the band too tightly',
    '4-6 sets x 15-30m, 2-3 min rest',
    NOW(),
    NOW()
  ),
  (
    'sp_assist_02',
    'Downhill Sprint (3-5° gradient)',
    'EXPLOSIVE',
    'Sprint down a gentle decline of 3-5 degrees for 30-50 meters at maximal effort. The gradient provides gravitational assistance to increase ground contact speed. Focus on maintaining upright posture and quick ground contacts rather than reaching with the front foot. Keep the trunk tall and allow the legs to cycle faster than on flat ground.',
    'Bodyweight',
    ARRAY['Quads', 'Glutes', 'Calves', 'Core'],
    'Increase gradient up to 7 degrees or extend distance',
    'Reduce gradient to 2-3 degrees or shorten distance to 20m',
    'Leaning back to brake on the descent, overstriding to slow down, excessive braking forces, not maintaining arm drive at higher speeds',
    '4-6 sets x 30-50m, 3-4 min rest',
    NOW(),
    NOW()
  ),
  (
    'sp_assist_03',
    'Overspeed Stair Sprint',
    'AGILITY',
    'Sprint up a staircase taking one or two steps per stride at maximal cadence. The stepping pattern forces rapid leg turnover and high knee drive. Focus on quick, light contacts with each step while maintaining aggressive arm action. This drill accelerates neural firing rates and promotes faster leg cycling.',
    'Bodyweight',
    ARRAY['Quads', 'Glutes', 'Calves', 'Hip Flexors'],
    'Increase number of stairs, reduce ground contact time, or add light load',
    'Reduce stair count, walk back for recovery, or use larger stairs',
    'Stomping on the steps instead of quick contacts, losing arm rhythm, leaning too far forward, taking steps too slowly',
    '4-6 sets x 10-20 steps, 2-3 min rest',
    NOW(),
    NOW()
  ),
  (
    'sp_assist_04',
    'Motor-Paced Sprint',
    'SPORT_SPECIFIC',
    'The athlete runs alongside or behind a bicycle, motorcycle, or vehicle moving at slightly above maximum sprint speed (105-110%). Sprint for 30-60 meters attempting to match or stay ahead of the pacing vehicle. This provides a visual and physical reference for supramaximal velocity. Requires a safe, controlled environment with an experienced pilot.',
    'Bodyweight',
    ARRAY['Hip Flexors', 'Glutes', 'Quads', 'Calves'],
    'Increase pace to 112-115% of max velocity or extend distance',
    'Reduce pace to 102-105% or shorten distance to 20m',
    'Sacrificing form to keep pace, running too close to the vehicle, excessive tension in the shoulders and neck, uneven breathing pattern',
    '3-5 sets x 30-60m, 4-6 min rest',
    NOW(),
    NOW()
  ),
  (
    'sp_assist_05',
    'Towel Overspeed',
    'SPORT_SPECIFIC',
    'A partner stands in front of the athlete holding a towel at chest height. The athlete grips the towel ends and the partner pulls forward while the athlete sprints. The pulling force assists the athlete beyond their normal top speed for 15-25 meters. Focus on maintaining tall posture and relaxed, rapid leg turnover.',
    'Bodyweight',
    ARRAY['Hip Flexors', 'Glutes', 'Quads', 'Calves'],
    'Partner increases pulling force or extend distance to 30m',
    'Reduce pulling force or shorten distance to 10m',
    'Gripping the towel too tightly causing upper body tension, leaning back against the pull, partner pulling inconsistently, athlete losing balance at supramaximal speeds',
    '3-5 sets x 15-25m, 2-3 min rest',
    NOW(),
    NOW()
  ),

  -- DECELERATION TRAINING (sp_decel_01 to sp_decel_06)
  (
    'sp_decel_01',
    'Stick Landing (single leg)',
    'AGILITY',
    'Stand on a 12-24 inch box. Step off and land on a single leg, absorbing the impact by flexing the hip, knee, and ankle simultaneously. Hold the landing position for 2-3 seconds with the knee tracking over the second toe and the trunk stable. Reset and repeat, alternating legs between sets.',
    'Box',
    ARRAY['Quads', 'Glutes', 'Core', 'Calves'],
    'Increase box height to 24-36 inches or add a lateral component',
    'Use a lower box (6-12 inches) or land on both legs initially',
    'Allowing the knee to cave inward (valgus), stiff-legged landing, excessive trunk lean, not holding the landing position long enough',
    '3-4 sets x 5-8 reps each leg, 90 sec rest',
    NOW(),
    NOW()
  ),
  (
    'sp_decel_02',
    'Sprint to Stop',
    'AGILITY',
    'Sprint at 80-100% effort for 10-20 meters, then rapidly decelerate to a complete stop within 3-5 steps. Drop the hips, widen the base, and use short choppy steps to absorb braking forces. Hold the stopped position for 2 seconds with knees soft and weight distributed evenly.',
    'Bodyweight',
    ARRAY['Quads', 'Glutes', 'Hamstrings', 'Core'],
    'Increase sprint speed, reduce stopping distance, or add a direction change after stopping',
    'Reduce sprint speed to 60-70% or allow more stopping distance',
    'Stopping with stiff legs, allowing the chest to drop too far forward, losing balance during deceleration, not dropping the hips low enough',
    '4-6 sets x 1 rep, 90 sec rest',
    NOW(),
    NOW()
  ),
  (
    'sp_decel_03',
    'Single Leg Decel (knee soft)',
    'AGILITY',
    'Build up to 70-80% sprint speed over 10-15 meters, then decelerate to a stop on a single leg within 3-4 steps. Absorb the braking forces through a flexed hip and knee with the knee staying aligned over the toes. Hold the single-leg stance for 2-3 seconds maintaining trunk stability. Alternate legs each repetition.',
    'Bodyweight',
    ARRAY['Quads', 'Glutes', 'Calves', 'Core'],
    'Increase approach speed, reduce stopping distance, or add a single-leg hop before decelerating',
    'Reduce approach speed to 50-60% or allow both feet to finish the stop',
    'Knee valgus collapse during braking, landing on a straight leg, trunk rotation or excessive lean, rushing through the hold phase',
    '3-4 sets x 4-6 reps each leg, 90 sec rest',
    NOW(),
    NOW()
  ),
  (
    'sp_decel_04',
    'Multi-Directional Decel',
    'AGILITY',
    'Set up cones in a T-shape or star pattern at 5-10 meter distances. Sprint to the first cone, then rapidly decelerate and change direction toward the next cone. Emphasize lowering the center of mass, planting the outside foot, and redirecting force through the hips. Complete 3-5 direction changes before finishing.',
    'Bodyweight',
    ARRAY['Quads', 'Glutes', 'Hip Adductors', 'Core'],
    'Increase sprint speed between cones, add more cones, or reduce cone distances',
    'Walk or jog between cones initially, use wider cone spacing',
    'Rounding the turns instead of sharp deceleration, standing tall during direction changes, not dropping the hips, crossing the feet during lateral movements',
    '3-5 sets x 1 rep through full pattern, 2 min rest',
    NOW(),
    NOW()
  ),
  (
    'sp_decel_05',
    'Drop Decel (box 12-24")',
    'AGILITY',
    'Stand on a 12-24 inch box. Step off and immediately upon landing, decelerate to a complete stop within 2-3 steps in a forward direction. Absorb the landing forces through the legs while simultaneously braking forward momentum. Hold the final stopped position for 2 seconds with hips low and chest up.',
    'Box',
    ARRAY['Quads', 'Glutes', 'Calves', 'Core'],
    'Increase box height, add a lateral step-off, or reduce stopping steps to 1-2',
    'Use a lower box (6-12 inches) or separate the landing and deceleration into two phases',
    'Landing with stiff legs, allowing the knees to cave inward, not absorbing forces through the hips, losing balance during the deceleration phase',
    '3-4 sets x 5-8 reps, 90 sec rest',
    NOW(),
    NOW()
  ),
  (
    'sp_decel_06',
    'Penultimate Step Drill',
    'AGILITY',
    'Set up two cones 15-20 meters apart. Sprint between them, then on the final 3-4 steps, practice an exaggerated penultimate (second-to-last) step that lowers the center of mass and prepares for rapid deceleration. The penultimate step should be slightly longer with a lower hip position. Finish by stopping within 1-2 steps after the penultimate foot contact.',
    'Bodyweight',
    ARRAY['Quads', 'Glutes', 'Calves', 'Core'],
    'Increase sprint speed, reduce total stopping distance, or add a change of direction after stopping',
    'Walk through the penultimate step pattern first, then gradually add speed',
    'Making the penultimate step too long causing overextension, not lowering the hips enough, rushing through the final deceleration steps, keeping the trunk too upright',
    '4-6 sets x 4-6 reps, 90 sec rest',
    NOW(),
    NOW()
  )

ON CONFLICT (id) DO UPDATE SET
  name = EXCLUDED.name,
  pattern = EXCLUDED.pattern,
  instructions = EXCLUDED.instructions,
  equipment = EXCLUDED.equipment,
  primary_muscles = EXCLUDED.primary_muscles,
  progression = EXCLUDED.progression,
  regression = EXCLUDED.regression,
  common_mistakes = EXCLUDED.common_mistakes,
  sets_reps_rest = EXCLUDED.sets_reps_rest,
  updated_at = NOW();

-- Tag all conditioning exercises
INSERT INTO exercise_tag_map (exercise_id, tag_id)
SELECT e.id, t.id
FROM exercises e, exercise_tags t
WHERE e.id IN (
  'sp_res_01', 'sp_res_02', 'sp_res_03', 'sp_res_04', 'sp_res_05', 'sp_res_06', 'sp_res_07',
  'sp_assist_01', 'sp_assist_02', 'sp_assist_03', 'sp_assist_04', 'sp_assist_05',
  'sp_decel_01', 'sp_decel_02', 'sp_decel_03', 'sp_decel_04', 'sp_decel_05', 'sp_decel_06'
)
AND t.name IN ('Resisted Sprint', 'Assisted Sprint', 'Deceleration', 'Speed Development', 'EXPLOSIVE', 'AGILITY', 'SPORT_SPECIFIC')
ON CONFLICT DO NOTHING;

-- Specifically tag resisted sprinting exercises
INSERT INTO exercise_tag_map (exercise_id, tag_id)
SELECT e.id, t.id
FROM exercises e, exercise_tags t
WHERE e.id IN ('sp_res_01', 'sp_res_02', 'sp_res_03', 'sp_res_04', 'sp_res_05', 'sp_res_06', 'sp_res_07')
AND t.name = 'Resisted Sprint'
ON CONFLICT DO NOTHING;

-- Specifically tag assisted sprinting exercises
INSERT INTO exercise_tag_map (exercise_id, tag_id)
SELECT e.id, t.id
FROM exercises e, exercise_tags t
WHERE e.id IN ('sp_assist_01', 'sp_assist_02', 'sp_assist_03', 'sp_assist_04', 'sp_assist_05')
AND t.name = 'Assisted Sprint'
ON CONFLICT DO NOTHING;

-- Specifically tag deceleration exercises
INSERT INTO exercise_tag_map (exercise_id, tag_id)
SELECT e.id, t.id
FROM exercises e, exercise_tags t
WHERE e.id IN ('sp_decel_01', 'sp_decel_02', 'sp_decel_03', 'sp_decel_04', 'sp_decel_05', 'sp_decel_06')
AND t.name = 'Deceleration'
ON CONFLICT DO NOTHING;
