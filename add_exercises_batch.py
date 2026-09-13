#!/usr/bin/env python3
"""Add missing exercises to Landing, Medicine Ball, Sprinting, and Acceleration categories"""

import json

# Load existing exercises
with open('/workspace/forge_web/src/data/exercises.json', 'r') as f:
    exercises = json.load(f)

# Get max ID - handle mixed types
max_id = 0
for ex in exercises:
    try:
        ex_id = int(ex['id'])
        if ex_id > max_id:
            max_id = ex_id
    except (ValueError, TypeError):
        pass

new_exercises = []

# ============== LANDING MECHANICS (Add 12 more to reach 25) ==============
landing_exercises = [
    {
        "name": "Box Jump Down with Stick",
        "category": "Landing",
        "subcategory": "Vertical Deceleration",
        "movement_pattern": "Jump-Down",
        "equipment": "Plyo Box",
        "difficulty": "Beginner",
        "source_organization": "NSCA",
        "description": "Teaching proper landing mechanics from low height with emphasis on quiet, controlled landing position.",
        "coaching_cues": ["Land softly like a ninja", "Knees track over toes", "Absorb impact through hips and knees", "Hold landing position 3 seconds"],
        "common_errors": ["Loud/heavy landing", "Knee valgus collapse", "Insufficient hip flexion", "Immediate rebound"],
        "contraindications": ["Acute ankle sprain", "Patellar tendinopathy flare-up"],
        "regressions": ["Step-down from box", "Lower box height"],
        "progressions": ["Increase box height", "Add unstable surface", "Single-leg landing"],
        "equipment_alternatives": ["Bench step", "Low platform"],
        "is_pain_safe": True
    },
    {
        "name": "Single-Leg Hop and Stick",
        "category": "Landing",
        "subcategory": "Unilateral Deceleration",
        "movement_pattern": "Hop-Land",
        "equipment": "Bodyweight",
        "difficulty": "Intermediate",
        "source_organization": "EXOS",
        "description": "Develop single-leg landing stability and control, critical for cutting and change of direction sports.",
        "coaching_cues": ["Hop forward 6-12 inches", "Land on same foot", "Keep knee aligned with toe", "Freeze on landing"],
        "common_errors": ["Dynamic knee valgus", "Excessive trunk lean", "Foot pronation", "Inability to hold position"],
        "contraindications": ["Recent ACL reconstruction", "Ankle instability", "Balance deficits"],
        "regressions": ["Two-leg hop and stick", "Smaller hop distance", "Supported single-leg balance"],
        "progressions": ["Increase hop distance", "Multi-directional hops", "Add external load"],
        "equipment_alternatives": ["Floor marker for distance", "Tape line"],
        "is_pain_safe": False
    },
    {
        "name": "Lateral Bound with Stick",
        "category": "Landing",
        "subcategory": "Frontal Plane Deceleration",
        "movement_pattern": "Side-to-Side Hop",
        "equipment": "Bodyweight",
        "difficulty": "Intermediate",
        "source_organization": "EXOS",
        "description": "Develop frontal plane landing control essential for lateral sports movements.",
        "coaching_cues": ["Push off outside foot", "Land on opposite foot", "Control the landing", "Stick for 2 seconds"],
        "common_errors": ["Knee collapsing inward", "Trunk leaning too far", "Quick rebound", "Flat-footed landing"],
        "contraindications": ["Hip adductor strain", "MCL injury", "Lateral ankle instability"],
        "regressions": ["Smaller lateral step", "Two-foot lateral jump", "Supported lateral lean"],
        "progressions": ["Increase distance", "Continuous bounds", "Add rotation"],
        "equipment_alternatives": ["Tape lines for markers", "Cones"],
        "is_pain_safe": False
    },
    {
        "name": "Drop Landing from 12 inch Box",
        "category": "Landing",
        "subcategory": "Reactive Landing",
        "movement_pattern": "Drop-Jump Land",
        "equipment": "Plyo Box",
        "difficulty": "Intermediate",
        "source_organization": "NSCA",
        "description": "Reactive landing drill teaching rapid absorption of ground reaction forces.",
        "coaching_cues": ["Step off don't jump", "Prepare to land before contact", "Absorb quickly and quietly", "Athletic stance finish"],
        "common_errors": ["Jumping up before dropping", "Stiff-legged landing", "Excessive noise on contact", "Poor posture at landing"],
        "contraindications": ["Achilles tendinopathy", "Plantar fasciitis", "Recent lower body injury"],
        "regressions": ["Lower box height (6 inch)", "Step-down instead of drop"],
        "progressions": ["Increase box height", "Single-leg drop", "Add immediate jump"],
        "equipment_alternatives": ["Low bench", "Aerobic stepper"],
        "is_pain_safe": False
    },
    {
        "name": "Wall Drop Landing Drill",
        "category": "Landing",
        "subcategory": "Postural Control",
        "movement_pattern": "Fall-Catch",
        "equipment": "Wall",
        "difficulty": "Beginner",
        "source_organization": "FMS",
        "description": "Teaches proper landing posture using wall support for feedback on body alignment.",
        "coaching_cues": ["Lean forward from ankles", "Let gravity pull you", "Catch yourself with lunge", "Stay tall through torso"],
        "common_errors": ["Bending at waist", "Looking down", "Rushing the catch", "Uneven foot placement"],
        "contraindications": ["Shoulder impingement", "Severe balance issues"],
        "regressions": ["Smaller lean angle", "Hand support available"],
        "progressions": ["Increase lean", "Eyes closed", "Unstable surface"],
        "equipment_alternatives": ["Partner assist", "TRX suspension"],
        "is_pain_safe": True
    },
    {
        "name": "Depth Jump to Box",
        "category": "Landing",
        "subcategory": "Reactive Strength",
        "movement_pattern": "Drop-Jump-Up",
        "equipment": "Plyo Boxes (2)",
        "difficulty": "Advanced",
        "source_organization": "Westside Barbell",
        "description": "Advanced plyometric utilizing stretch-shortening cycle for maximum vertical output after landing.",
        "coaching_cues": ["Minimize ground contact time", "Explode immediately on contact", "Land soft on top box", "Use arms for momentum"],
        "common_errors": ["Long ground contact", "Double dip before jumping", "Landing stiff on box", "Looking down mid-air"],
        "contraindications": ["Patellar tendinopathy", "History of ACL injury", "Lower back issues"],
        "regressions": ["Drop landing without jump", "Lower box heights", "Countermovement jump to box"],
        "progressions": ["Increase drop height", "Single-leg variation", "Add external load vest"],
        "equipment_alternatives": ["Stacked plates", "Bench and step"],
        "is_pain_safe": False
    },
    {
        "name": "Medicine Ball Overhead Slam Landing",
        "category": "Landing",
        "subcategory": "Integrated Deceleration",
        "movement_pattern": "Slam-Squat",
        "equipment": "Medicine Ball",
        "difficulty": "Intermediate",
        "source_organization": "EXOS",
        "description": "Combines upper body power with lower body landing mechanics in integrated pattern.",
        "coaching_cues": ["Slam ball aggressively", "Immediately absorb into squat", "Keep chest up on landing", "Reset between reps"],
        "common_errors": ["Rounding back on slam", "Not squatting after slam", "Knees caving in", "Holding breath"],
        "contraindications": ["Shoulder impingement", "Lower back disc issues", "Hip flexor strain"],
        "regressions": ["Lighter ball", "No slam just toss", "Squat without ball"],
        "progressions": ["Heavier ball", "Jump slam", "Rotational slam"],
        "equipment_alternatives": ["Sandbag", "Rope slam"],
        "is_pain_safe": False
    },
    {
        "name": "Deceleration Lunge Matrix",
        "category": "Landing",
        "subcategory": "Multi-Directional Control",
        "movement_pattern": "Lunge-Hold",
        "equipment": "Bodyweight",
        "difficulty": "Intermediate",
        "source_organization": "Gray Institute",
        "description": "Teaches deceleration control in all planes of motion through lunge patterns.",
        "coaching_cues": ["Step in each direction", "Absorb weight smoothly", "Hold end position 2 sec", "Stay balanced throughout"],
        "common_errors": ["Rushing between positions", "Knee past toe excessively", "Trunk leaning", "Heel lifting"],
        "contraindications": ["Knee osteoarthritis", "Meniscus tear", "Hip impingement"],
        "regressions": ["Partial range", "Support holding", "Forward-back only"],
        "progressions": ["Add rotation", "Weighted vest", "Eyes closed"],
        "equipment_alternatives": ["Tape grid", "Cones"],
        "is_pain_safe": False
    },
    {
        "name": "Snap-Down Drill",
        "category": "Landing",
        "subcategory": "Rapid Position Change",
        "movement_pattern": "Stand-Squat",
        "equipment": "Bodyweight",
        "difficulty": "Beginner",
        "source_organization": "NSCA",
        "description": "Quick transition from standing to athletic position teaching rapid force absorption.",
        "coaching_cues": ["Start tall on toes", "Drop quickly to squat", "Land in athletic stance", "Hands ready position"],
        "common_errors": ["Slow descent", "Landing upright", "Feet too narrow", "Arms not engaged"],
        "contraindications": ["Acute knee pain", "Ankle mobility restrictions"],
        "regressions": ["Slower tempo", "Shallow squat depth", "Wide stance"],
        "progressions": ["Add jump before snap", "Single-leg snap", "Reaction cue variations"],
        "equipment_alternatives": ["Mirror for feedback", "Coach visual cue"],
        "is_pain_safe": True
    },
    {
        "name": "Zig-Zag Hop and Stick",
        "category": "Landing",
        "subcategory": "Diagonal Deceleration",
        "movement_pattern": "Diagonal Hop",
        "equipment": "Cones",
        "difficulty": "Advanced",
        "source_organization": "EXOS",
        "description": "Multi-planar landing drill combining forward and lateral components for sport-specificity.",
        "coaching_cues": ["Hop diagonally forward", "Land on opposite foot", "Control each landing", "Change direction sharply"],
        "common_errors": ["Poor angle selection", "Uncontrolled landings", "Foot placement errors", "Rushing sequence"],
        "contraindications": ["ACL reconstruction < 6 months", "Ankle instability", "Proprioception deficits"],
        "regressions": ["Two-foot hops", "Slower tempo", "Shorter distances"],
        "progressions": ["Increase speed", "Add ball handling", "Random directional calls"],
        "equipment_alternatives": ["Tape marks", "Agility ladder"],
        "is_pain_safe": False
    },
    {
        "name": "Single-Leg Romanian Deadlift to Landing",
        "category": "Landing",
        "subcategory": "Eccentric Control",
        "movement_pattern": "Hinge-Hop-Land",
        "equipment": "Dumbbell",
        "difficulty": "Advanced",
        "source_organization": "StrongFirst",
        "description": "Combines eccentric hip hinge with single-leg landing for posterior chain loading and control.",
        "coaching_cues": ["Hinge back on one leg", "Light hop at bottom", "Land softly same foot", "Return to standing"],
        "common_errors": ["Rounding spine", "Knee valgus on landing", "Loss of balance", "Rushing movement"],
        "contraindications": ["Lower back disc issues", "Hamstring strain", "Significant balance deficits"],
        "regressions": ["Two-leg RDL", "No hop version", "Light or no weight"],
        "progressions": ["Heavier load", "Higher hop", "Eyes closed"],
        "equipment_alternatives": ["Kettlebell", "Band resistance", "Cable machine"],
        "is_pain_safe": False
    },
    {
        "name": "Reactive Landing to Sprint",
        "category": "Landing",
        "subcategory": "Transition Mechanics",
        "movement_pattern": "Drop-Sprint",
        "equipment": "Plyo Box",
        "difficulty": "Advanced",
        "source_organization": "NSCA",
        "description": "Teaches rapid transition from landing absorption to horizontal acceleration.",
        "coaching_cues": ["Drop from box", "Absorb landing efficiently", "Immediately sprint forward", "Drive knees aggressively"],
        "common_errors": ["Pausing after landing", "Upright sprint posture", "Overstriding first steps", "Looking back at box"],
        "contraindications": ["Hamstring strain", "Hip flexor injury", "Recent ACL/MCL injury"],
        "regressions": ["Step-off instead of drop", "Walk after landing", "Shorter sprint distance"],
        "progressions": ["Higher box", "Longer sprint", "Add defender"],
        "equipment_alternatives": ["Low bench", "Grass field"],
        "is_pain_safe": False
    }
]

for ex in landing_exercises:
    new_ex = ex.copy()
    max_id += 1
    new_ex['id'] = max_id
    new_ex['created_at'] = '2024-01-15T00:00:00Z'
    new_exercises.append(new_ex)

print(f"Added {len(landing_exercises)} Landing Mechanics exercises")

# ============== MEDICINE BALL (Add 11 more to reach 25) ==============
medball_exercises = [
    {
        "name": "Med Ball Rotational Throw (Wall)",
        "category": "Ball",
        "subcategory": "Rotational Power",
        "movement_pattern": "Rotational Throw",
        "equipment": "Medicine Ball",
        "difficulty": "Intermediate",
        "source_organization": "EXOS",
        "description": "Develop rotational power through the kinetic chain with lateral throw against wall.",
        "coaching_cues": ["Load through back hip", "Rotate hips first", "Release at chest height", "Follow through completely"],
        "common_errors": ["Arms only no rotation", "Early release", "Poor foot pivot", "No hip engagement"],
        "contraindications": ["Shoulder impingement", "Oblique strain", "Lower back disc issues"],
        "regressions": ["Lighter ball", "Slower tempo", "No step just rotate"],
        "progressions": ["Heavier ball", "Increase distance", "Jump into throw"],
        "equipment_alternatives": ["Cable machine", "Band resistance"],
        "is_pain_safe": False
    },
    {
        "name": "Med Ball Overhead Back Toss",
        "category": "Ball",
        "subcategory": "Posterior Chain Power",
        "movement_pattern": "Overhead Throw",
        "equipment": "Medicine Ball",
        "difficulty": "Advanced",
        "source_organization": "Westside Barbell",
        "description": "Explosive posterior chain development through overhead backward throw.",
        "coaching_cues": ["Load into hip hinge", "Sweep arms back", "Snap hips forward", "Release overhead"],
        "common_errors": ["Using arms only", "Not hipping loading", "Looking up too early", "Incomplete follow through"],
        "contraindications": ["Shoulder instability", "Lower back acute injury", "Neck issues"],
        "regressions": ["Lighter ball", "Smaller range", "Partner catch instead of toss"],
        "progressions": ["Heavier ball", "Single-leg variation", "Jump before toss"],
        "equipment_alternatives": ["Sandbag", "Weighted implement"],
        "is_pain_safe": False
    },
    {
        "name": "Med Ball Chest Pass (Seated)",
        "category": "Ball",
        "subcategory": "Upper Body Power",
        "movement_pattern": "Chest Pass",
        "equipment": "Medicine Ball",
        "difficulty": "Beginner",
        "source_organization": "NSCA",
        "description": "Isolate upper body pushing power by eliminating leg drive through seated position.",
        "coaching_cues": ["Ball at chest", "Elbows tucked", "Explode through arms", "Full extension"],
        "common_errors": ["Leaning back", "Wide elbow flare", "Incomplete extension", "Slow release"],
        "contraindications": ["Shoulder impingement", "Wrist pain", "Pectoral strain"],
        "regressions": ["Lighter ball", "Shorter distance", "Two-hand underhand"],
        "progressions": ["Heavier ball", "Increase distance", "Add jump stand-up pass"],
        "equipment_alternatives": ["Cable chest press", "Band press"],
        "is_pain_safe": True
    },
    {
        "name": "Med Ball Slam (Overhead)",
        "category": "Ball",
        "subcategory": "Total Body Power",
        "movement_pattern": "Overhead Slam",
        "equipment": "Medicine Ball",
        "difficulty": "Intermediate",
        "source_organization": "EXOS",
        "description": "Full body power expression through aggressive overhead slam pattern.",
        "coaching_cues": ["Reach tall with ball", "Load hips back", "Slam down aggressively", "Catch on bounce"],
        "common_errors": ["Rounding spine", "Only using arms", "Not catching eccentric", "Looking down"],
        "contraindications": ["Lower back disc issues", "Shoulder impingement", "Hip flexor strain"],
        "regressions": ["Lighter ball", "Slower controlled throw", "No catch just pick up"],
        "progressions": ["Heavier ball", "Jump slam", "Single-arm slam"],
        "equipment_alternatives": ["Sandbag", "Battle ropes"],
        "is_pain_safe": False
    },
    {
        "name": "Med Ball Side Throw (Kneeling)",
        "category": "Ball",
        "subcategory": "Anti-Rotation Core",
        "movement_pattern": "Lateral Throw",
        "equipment": "Medicine Ball",
        "difficulty": "Intermediate",
        "source_organization": "Gray Institute",
        "description": "Develop anti-rotation core stability while producing lateral force from kneeling position.",
        "coaching_cues": ["Kneel both knees", "Rotate torso only", "Keep hips square", "Throw from chest"],
        "common_errors": ["Hip rotation", "Leaning sideways", "Dropping elbows", "Incomplete rotation"],
        "contraindications": ["Knee pain", "Oblique strain", "Shoulder issues"],
        "regressions": ["Lighter ball", "Smaller rotation", "Partner hand-off"],
        "progressions": ["Heavier ball", "Half-kneeling stance", "Add band resistance"],
        "equipment_alternatives": ["Cable woodchop", "Band rotation"],
        "is_pain_safe": False
    },
    {
        "name": "Med Ball Scoop Toss",
        "category": "Ball",
        "subcategory": "Hip Extension Power",
        "movement_pattern": "Underhand Throw",
        "equipment": "Medicine Ball",
        "difficulty": "Beginner",
        "source_organization": "NSCA",
        "description": "Teach triple extension through low-to-high scoop tossing pattern.",
        "coaching_cues": ["Ball between legs", "Hinge at hips", "Extend ankles knees hips", "Release at eye level"],
        "common_errors": ["Squatting not hinging", "Arms only", "Early release", "No ankle extension"],
        "contraindications": ["Lower back acute pain", "Hamstring strain"],
        "regressions": ["Lighter ball", "Smaller range", "No step"],
        "progressions": ["Heavier ball", "Step into throw", "Single-leg scoop"],
        "equipment_alternatives": ["Kettlebell swing", "Band pull-through"],
        "is_pain_safe": True
    },
    {
        "name": "Med Ball Russian Twist Throw",
        "category": "Ball",
        "subcategory": "Rotational Endurance",
        "movement_pattern": "Rotational Core",
        "equipment": "Medicine Ball",
        "difficulty": "Intermediate",
        "source_organization": "StrongFirst",
        "description": "Build rotational core endurance through controlled twist and catch pattern.",
        "coaching_cues": ["Feet elevated", "Lean back slightly", "Rotate full range", "Partner catches"],
        "common_errors": ["Feet touching ground", "Limited rotation", "Rushing reps", "Rounding spine"],
        "contraindications": ["Lower back disc issues", "Hip flexor strain", "Balance deficits"],
        "regressions": ["Feet on ground", "Lighter ball", "No throw just touch"],
        "progressions": ["Higher feet elevation", "Heavier ball", "Faster tempo"],
        "equipment_alternatives": ["Cable rotation", "Landmine rotation"],
        "is_pain_safe": False
    },
    {
        "name": "Med Ball Wall Bounce Catch",
        "category": "Ball",
        "subcategory": "Reactive Power",
        "movement_pattern": "Catch-Decelerate",
        "equipment": "Medicine Ball, Wall",
        "difficulty": "Advanced",
        "source_organization": "EXOS",
        "description": "Develop reactive strength and deceleration capacity through rapid catch-throw cycles.",
        "coaching_cues": ["Athletic stance", "Soft hands ready", "Absorb on catch", "Immediately redirect"],
        "common_errors": ["Stiff arms", "Late reaction", "Poor stance", "Dropping ball"],
        "contraindications": ["Wrist issues", "Shoulder instability", "Reaction time deficits"],
        "regressions": ["Self-toss catch", "Slower tempo", "Two-hand only"],
        "progressions": ["Faster tempo", "Single-hand catch", "Add movement"],
        "equipment_alternatives": ["React ball", "Tennis ball against wall"],
        "is_pain_safe": False
    },
    {
        "name": "Med Ball Push-Up Pass",
        "category": "Ball",
        "subcategory": "Upper Body Reactive",
        "movement_pattern": "Push-Up Throw",
        "equipment": "Medicine Ball",
        "difficulty": "Advanced",
        "source_organization": "NSCA",
        "description": "Combine push-up strength with explosive chest passing for upper body power.",
        "coaching_cues": ["Hands on ball", "Lower to ball", "Explode up releasing ball", "Catch on descent"],
        "common_errors": ["Sagging hips", "Incomplete push", "Late catch", "Wide hand placement"],
        "contraindications": ["Wrist pain", "Shoulder impingement", "Pectoral injury"],
        "regressions": ["Knees down", "No pass just push", "Partner assist"],
        "progressions": ["Feet elevated", "Clap push-up catch", "Single-arm variation"],
        "equipment_alternatives": ["Push-up handles", "Parallettes"],
        "is_pain_safe": False
    },
    {
        "name": "Med Ball Lateral Step Throw",
        "category": "Ball",
        "subcategory": "Lateral Power Transfer",
        "movement_pattern": "Step-Throw",
        "equipment": "Medicine Ball",
        "difficulty": "Intermediate",
        "source_organization": "Gray Institute",
        "description": "Train lateral force production and transfer through stepping throw pattern.",
        "coaching_cues": ["Step laterally", "Load back leg", "Transfer weight forward", "Throw across body"],
        "common_errors": ["No step", "Poor weight transfer", "Arms only", "No hip rotation"],
        "contraindications": ["Hip adductor strain", "Knee valgus", "Ankle instability"],
        "regressions": ["Smaller step", "Lighter ball", "No throw just rotation"],
        "progressions": ["Larger step", "Heavier ball", "Add jump"],
        "equipment_alternatives": ["Cable lift", "Band lateral throw"],
        "is_pain_safe": False
    },
    {
        "name": "Med Ball Bridge March Throw",
        "category": "Ball",
        "subcategory": "Posterior Chain Stability",
        "movement_pattern": "Bridge-Pass",
        "equipment": "Medicine Ball",
        "difficulty": "Intermediate",
        "source_organization": "EXOS",
        "description": "Challenge glute bridge stability while adding dynamic partner passing component.",
        "coaching_cues": ["Bridge hips high", "March one knee up", "Pass ball under thigh", "Maintain bridge"],
        "common_errors": ["Hips dropping", "Arching back", "Rushing march", "Uneven hips"],
        "contraindications": ["Lower back acute pain", "Hip flexor strain", "Glute injury"],
        "regressions": ["No march just bridge", "Hold ball static", "Feet on ground"],
        "progressions": ["Heavier ball", "Faster march", "Single-leg bridge"],
        "equipment_alternatives": ["Swiss ball bridge", "Band resisted bridge"],
        "is_pain_safe": True
    }
]

for ex in medball_exercises:
    new_ex = ex.copy()
    max_id += 1
    new_ex['id'] = max_id
    new_ex['created_at'] = '2024-01-15T00:00:00Z'
    new_exercises.append(new_ex)

print(f"Added {len(medball_exercises)} Medicine Ball exercises")

# ============== SPRINTING (Add 9 more to reach 40) ==============
sprinting_exercises = [
    {
        "name": "A-Skip Drill",
        "category": "Sprint",
        "subcategory": "Mechanics",
        "movement_pattern": "Skip",
        "equipment": "Bodyweight",
        "difficulty": "Beginner",
        "source_organization": "NSCA",
        "description": "Fundamental sprint mechanics drill emphasizing knee lift and foot strike pattern.",
        "coaching_cues": ["Tall posture", "Drive knee up", "Strike ground actively", "Quick ground contact"],
        "common_errors": ["Leaning back", "Low knee lift", "Passive foot strike", "Long ground contact"],
        "contraindications": ["Hip flexor strain", "Ankle mobility restrictions"],
        "regressions": ["Slower tempo", "Marching pattern", "Wall drill first"],
        "progressions": ["Faster tempo", "A-Skip for distance", "Add arm drive"],
        "equipment_alternatives": ["Treadmill slow", "High knees march"],
        "is_pain_safe": True
    },
    {
        "name": "B-Skip Drill",
        "category": "Sprint",
        "subcategory": "Mechanics",
        "movement_pattern": "Skip-Extension",
        "equipment": "Bodyweight",
        "difficulty": "Intermediate",
        "source_organization": "EXOS",
        "description": "Advanced sprint drill emphasizing hip extension and paw-back mechanics.",
        "coaching_cues": ["Knee up then extend", "Paw back aggressively", "Stay tall", "Quick cycle"],
        "common_errors": ["Biking motion", "Incomplete extension", "Leaning forward", "Slow turnover"],
        "contraindications": ["Hamstring strain", "Hip flexor tightness", "Knee issues"],
        "regressions": ["A-Skip first", "Slower tempo", "Shorter distance"],
        "progressions": ["Faster tempo", "B-Skip bounds", "Into acceleration"],
        "equipment_alternatives": ["Wall drill", "Band resisted skip"],
        "is_pain_safe": False
    },
    {
        "name": "Fast Feet Ladder",
        "category": "Sprint",
        "subcategory": "Foot Speed",
        "movement_pattern": "Quick Steps",
        "equipment": "Agility Ladder",
        "difficulty": "Beginner",
        "source_organization": "EXOS",
        "description": "Develop rapid foot turnover and coordination through ladder drill patterns.",
        "coaching_cues": ["Quick light steps", "Stay on balls of feet", "Minimal ground contact", "Relax upper body"],
        "common_errors": ["Heavy steps", "Flat-footed", "Looking down constantly", "Tense shoulders"],
        "contraindications": ["Ankle instability", "Achilles tendinopathy"],
        "regressions": ["Slower tempo", "Wider squares", "No ladder just spots"],
        "progressions": ["Faster tempo", "Complex patterns", "Add cognitive cue"],
        "equipment_alternatives": ["Chalk marks", "Cones in line"],
        "is_pain_safe": True
    },
    {
        "name": "Flying 20s",
        "category": "Sprint",
        "subcategory": "Max Velocity",
        "movement_pattern": "Sprint",
        "equipment": "Cones",
        "difficulty": "Advanced",
        "source_organization": "NSCA",
        "description": "Develop maximum velocity sprinting through rolling start sprint over 20 yards.",
        "coaching_cues": ["Build up gradually", "Hit top speed in zone", "Stay relaxed", "Tall posture"],
        "common_errors": ["Starting too fast", "Tensing up", "Leaning forward", "Overstriding"],
        "contraindications": ["Hamstring strain history", "Hip flexor injury", "Recent groin pull"],
        "regressions": ["Flying 10s", "Slower build-up", "Shorter distance"],
        "progressions": ["Flying 30s", "Multiple reps", "Shorter rest"],
        "equipment_alternatives": ["Track markers", "Field lines"],
        "is_pain_safe": False
    },
    {
        "name": "Hill Sprints (Short)",
        "category": "Sprint",
        "subcategory": "Acceleration Power",
        "movement_pattern": "Uphill Sprint",
        "equipment": "Hill",
        "difficulty": "Intermediate",
        "source_organization": "NSCA",
        "description": "Build acceleration power and reduce hamstring strain risk through uphill sprinting.",
        "coaching_cues": ["Drive knees high", "Lean with hill", "Powerful arm drive", "Quick steps"],
        "common_errors": ["Leaning too far", "Short choppy steps", "Poor arm action", "Looking down"],
        "contraindications": ["Achilles issues", "Calf strain", "Severe deconditioning"],
        "regressions": ["Walk up first", "Shorter hill", "Slower pace"],
        "progressions": ["Steeper hill", "Longer distance", "Multiple reps"],
        "equipment_alternatives": ["Treadmill incline", "Stadium stairs"],
        "is_pain_safe": True
    },
    {
        "name": "Resisted Sled Sprint",
        "category": "Sprint",
        "subcategory": "Acceleration Strength",
        "movement_pattern": "Sled Push-Sprint",
        "equipment": "Sled",
        "difficulty": "Intermediate",
        "source_organization": "EXOS",
        "description": "Develop acceleration strength and horizontal force production through resisted sprinting.",
        "coaching_cues": ["Forward lean", "Drive legs back", "Powerful arm action", "Quick turnover"],
        "common_errors": ["Too upright", "Small steps", "Dragging feet", "Poor sled load"],
        "contraindications": ["Lower back acute pain", "Hip flexor strain", "Knee issues"],
        "regressions": ["Lighter load", "Shorter distance", "Walk first"],
        "progressions": ["Heavier load", "Longer distance", "Sprint after release"],
        "equipment_alternatives": ["Band resisted", "Partner resisted", "Parachute"],
        "is_pain_safe": False
    },
    {
        "name": "Carioca Drill",
        "category": "Sprint",
        "subcategory": "Lateral Mobility",
        "movement_pattern": "Crossover Step",
        "equipment": "Bodyweight",
        "difficulty": "Intermediate",
        "source_organization": "Gray Institute",
        "description": "Develop hip mobility and lateral coordination essential for multi-directional sports.",
        "coaching_cues": ["Cross behind", "Open hips", "Stay low", "Smooth rhythm"],
        "common_errors": ["Crossing in front", "Tall upright", "Stiff hips", "Jerky movement"],
        "contraindications": ["Hip impingement", "Groin strain", "Knee MCL issues"],
        "regressions": ["Slower tempo", "Smaller steps", "Side shuffle first"],
        "progressions": ["Faster tempo", "Add sprint burst", "Change directions"],
        "equipment_alternatives": ["Lateral bounds", "Cone weave"],
        "is_pain_safe": False
    },
    {
        "name": "Wall Drive Phase Drill",
        "category": "Sprint",
        "subcategory": "Acceleration Mechanics",
        "movement_pattern": "Wall Drive",
        "equipment": "Wall",
        "difficulty": "Beginner",
        "source_organization": "NSCA",
        "description": "Isolate and teach proper acceleration body angles and leg drive mechanics.",
        "coaching_cues": ["45 degree angle", "Drive knee up", "Strike ground behind", "Strong arm action"],
        "common_errors": ["Too upright", "Striking under hips", "Weak arm drive", "Looking up"],
        "contraindications": ["Shoulder impingement", "Wrist issues"],
        "regressions": ["Less angle", "Slower tempo", "Single leg drill"],
        "progressions": ["Faster tempo", "Band resisted", "Into short sprint"],
        "equipment_alternatives": ["Partner resist", "Sled start position"],
        "is_pain_safe": True
    },
    {
        "name": "Ins and Outs Sprint",
        "category": "Sprint",
        "subcategory": "Speed Endurance",
        "movement_pattern": "Variable Pace Sprint",
        "equipment": "Cones",
        "difficulty": "Advanced",
        "source_organization": "UEFA Medical",
        "description": "Develop speed endurance and recovery capacity through variable intensity sprinting.",
        "coaching_cues": ["Hard in zone", "Float recovery", "Maintain form when tired", "Controlled breathing"],
        "common_errors": ["Not going hard enough", "Stopping completely", "Form breakdown", "Poor pacing"],
        "contraindications": ["Poor conditioning", "Recent hamstring injury", "Cardiovascular issues"],
        "regressions": ["Shorter distances", "More recovery", "Walk outs"],
        "progressions": ["Longer hard zones", "Less recovery", "More total volume"],
        "equipment_alternatives": ["Track intervals", "Treadmill intervals"],
        "is_pain_safe": False
    }
]

for ex in sprinting_exercises:
    new_ex = ex.copy()
    max_id += 1
    new_ex['id'] = max_id
    new_ex['created_at'] = '2024-01-15T00:00:00Z'
    new_exercises.append(new_ex)

print(f"Added {len(sprinting_exercises)} Sprinting exercises")

# ============== ACCELERATION (Add 9 more to reach 45) ==============
acceleration_exercises = [
    {
        "name": "5 Yard Dash Starts",
        "category": "Acc",
        "subcategory": "Short Distance",
        "movement_pattern": "Sprint Start",
        "equipment": "Cones",
        "difficulty": "Beginner",
        "source_organization": "NSCA",
        "description": "Develop explosive starting strength and initial acceleration mechanics over ultra-short distance.",
        "coaching_cues": ["Explosive first step", "Drive phase posture", "Powerful arm punch", "Stay low first 3 steps"],
        "common_errors": ["Pop up too fast", "Short first step", "Weak arm drive", "Looking up early"],
        "contraindications": ["Acute hamstring strain", "Hip flexor injury"],
        "regressions": ["Walking start", "Slower pace", "3 yard distance"],
        "progressions": ["Resisted starts", "Reaction starts", "Multiple reps"],
        "equipment_alternatives": ["Track start blocks", "Field lines"],
        "is_pain_safe": True
    },
    {
        "name": "Falling Starts",
        "category": "Acc",
        "subcategory": "Reaction Acceleration",
        "movement_pattern": "Fall-Sprint",
        "equipment": "Bodyweight",
        "difficulty": "Intermediate",
        "source_organization": "EXOS",
        "description": "Utilize gravity to develop reaction time and initial acceleration from forward fall.",
        "coaching_cues": ["Lean until falling", "Catch yourself with sprint", "First step under center", "Drive aggressively"],
        "common_errors": ["Leaning too far", "Slow reaction", "Wide first step", "Popping up"],
        "contraindications": ["Balance deficits", "Ankle instability", "Recent fall risk"],
        "regressions": ["Smaller lean", "Partner assist", "Slower progression"],
        "progressions": ["Larger lean", "Reaction cue start", "From prone position"],
        "equipment_alternatives": ["Partner push start", "Band release"],
        "is_pain_safe": False
    },
    {
        "name": "Resisted Band Acceleration",
        "category": "Acc",
        "subcategory": "Loaded Acceleration",
        "movement_pattern": "Band Sprint",
        "equipment": "Resistance Band",
        "difficulty": "Intermediate",
        "source_organization": "EXOS",
        "description": "Build acceleration strength through horizontally resisted sprinting pattern.",
        "coaching_cues": ["Forward body angle", "Drive through resistance", "Quick leg turnover", "Strong arms"],
        "common_errors": ["Too upright", "Slow steps", "Band pulling off course", "Poor posture"],
        "contraindications": ["Hip flexor strain", "Lower back acute pain", "Shoulder issues"],
        "regressions": ["Lighter band", "Shorter distance", "Walk first"],
        "progressions": ["Heavier band", "Longer distance", "Sprint after release"],
        "equipment_alternatives": ["Sled", "Parachute", "Partner resist"],
        "is_pain_safe": False
    },
    {
        "name": "Box Step-Over Acceleration",
        "category": "Acc",
        "subcategory": "Obstacle Acceleration",
        "movement_pattern": "Step-Sprint",
        "equipment": "Low Hurdle/Box",
        "difficulty": "Intermediate",
        "source_organization": "NSCA",
        "description": "Develop acceleration after clearing obstacle simulating game situations.",
        "coaching_cues": ["Quick step over", "Land and drive", "Stay low after hurdle", "Accelerate immediately"],
        "common_errors": ["Stopping after hurdle", "Standing up", "Slow first step", "Poor hurdle clearance"],
        "contraindications": ["Knee issues", "Ankle instability", "Hip impingement"],
        "regressions": ["Lower hurdle", "Walk over first", "No sprint just step"],
        "progressions": ["Higher hurdle", "Multiple hurdles", "Add defender"],
        "equipment_alternatives": ["Cone step", "Agility ring"],
        "is_pain_safe": False
    },
    {
        "name": "Mirror Shuffle to Sprint",
        "category": "Acc",
        "subcategory": "Transition Acceleration",
        "movement_pattern": "Shuffle-Sprint",
        "equipment": "Cones",
        "difficulty": "Advanced",
        "source_organization": "EXOS",
        "description": "Train transition from lateral defensive position to forward acceleration.",
        "coaching_cues": ["Low athletic stance", "Mirror partner", "Plant and turn", "Explode forward"],
        "common_errors": ["High stance", "Slow transition", "Poor plant foot", "Telegraphing move"],
        "contraindications": ["Knee valgus", "ACL reconstruction <6mo", "Ankle instability"],
        "regressions": ["Slower shuffle", "Shorter distance", "No mirror just cone"],
        "progressions": ["Faster shuffle", "Longer sprint", "Add ball pursuit"],
        "equipment_alternatives": ["Defensive slide drill", "Cone touch drill"],
        "is_pain_safe": False
    },
    {
        "name": "Three-Point Stance Starts",
        "category": "Acc",
        "subcategory": "Power Position Start",
        "movement_pattern": "Stance-Sprint",
        "equipment": "Field",
        "difficulty": "Intermediate",
        "source_organization": "NSCA",
        "description": "Develop acceleration from traditional three-point lineman stance position.",
        "coaching_cues": ["Weight on hands", "Back leg drives first", "Low exit angle", "Powerful first steps"],
        "common_errors": ["Too much weight forward", "Slow hand removal", "High exit", "Crossing feet"],
        "contraindications": ["Wrist issues", "Shoulder impingement", "Lower back pain"],
        "regressions": ["Two-point stance", "Slower start", "Shorter distance"],
        "progressions": ["Band resisted", "Reaction starts", "Longer sprint"],
        "equipment_alternatives": ["Track blocks", "Grass field"],
        "is_pain_safe": True
    },
    {
        "name": "Zig-Zag Acceleration",
        "category": "Acc",
        "subcategory": "Multi-Directional",
        "movement_pattern": "Cut-Sprint",
        "equipment": "Cones",
        "difficulty": "Advanced",
        "source_organization": "Gray Institute",
        "description": "Develop acceleration after multiple directional changes for sport-specific patterns.",
        "coaching_cues": ["Sharp cuts", "Outside foot plant", "Low center of mass", "Accelerate after each cut"],
        "common_errors": ["Wide turns", "High stance", "Slow plants", "Poor angles"],
        "contraindications": ["Knee MCL/LCL issues", "Ankle sprains", "Hip labral tears"],
        "regressions": ["Fewer cones", "Slower pace", "Walk pattern first"],
        "progressions": ["More cones", "Faster pace", "Add defender"],
        "equipment_alternatives": ["Agility ladder exit", "T-drill"],
        "is_pain_safe": False
    },
    {
        "name": "Medicine Ball Throw to Sprint",
        "category": "Acc",
        "subcategory": "Integrated Power",
        "movement_pattern": "Throw-Sprint",
        "equipment": "Medicine Ball",
        "difficulty": "Advanced",
        "source_organization": "EXOS",
        "description": "Combine upper body power expression with immediate lower body acceleration.",
        "coaching_cues": ["Explosive throw", "Immediately sprint", "Don't watch ball", "Drive knees"],
        "common_errors": ["Watching ball", "Delayed sprint", "Poor throw mechanics", "Slow first step"],
        "contraindications": ["Shoulder impingement", "Hamstring strain", "Core injuries"],
        "regressions": ["Lighter ball", "Shorter throw", "Walk sprint"],
        "progressions": ["Heavier ball", "Longer throw", "Longer sprint"],
        "equipment_alternatives": ["Cable throw", "Band throw"],
        "is_pain_safe": False
    },
    {
        "name": "Depth Drop to Sprint",
        "category": "Acc",
        "subcategory": "Reactive Acceleration",
        "movement_pattern": "Drop-Sprint",
        "equipment": "Low Box",
        "difficulty": "Advanced",
        "source_organization": "Westside Barbell",
        "description": "Develop reactive acceleration from eccentric landing utilizing stretch-shortening cycle.",
        "coaching_cues": ["Step off box", "Absorb landing", "Immediately sprint", "Stay low"],
        "common_errors": ["Jumping off", "Pausing after land", "Standing up", "Slow reaction"],
        "contraindications": ["Patellar tendinopathy", "Achilles issues", "Recent ACL/MCL"],
        "regressions": ["Lower box", "Step off walk", "No sprint"],
        "progressions": ["Higher box", "Longer sprint", "Add resistance"],
        "equipment_alternatives": ["Low bench", "Grass surface"],
        "is_pain_safe": False
    }
]

for ex in acceleration_exercises:
    new_ex = ex.copy()
    max_id += 1
    new_ex['id'] = max_id
    new_ex['created_at'] = '2024-01-15T00:00:00Z'
    new_exercises.append(new_ex)

print(f"Added {len(acceleration_exercises)} Acceleration exercises")

# Save updated exercises
with open('/workspace/forge_web/src/data/exercises.json', 'w') as f:
    json.dump(exercises + new_exercises, f, indent=2)

total_count = len(exercises) + len(new_exercises)
print(f"\n=== SUMMARY ===")
print(f"Total new exercises added: {len(new_exercises)}")
print(f"Total exercises in library: {total_count}")
