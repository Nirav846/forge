#!/usr/bin/env python3
"""
Phase 2: Category Expansion - Add missing Recovery, Mobility, Activation, and Assessment exercises
"""
import json
from datetime import datetime

# New exercises to add for missing categories
NEW_EXERCISES = [
    # === RECOVERY & MOBILITY (15 exercises) ===
    {
        "id": "REC-001",
        "name": "Foam Roller IT Band Release",
        "family": "Recovery",
        "secondary_family": None,
        "objective": "MOB",
        "difficulty": 1,
        "equipment": ["Foam Roller"],
        "unilateral": True,
        "explosive": False,
        "isometric": False,
        "rotational": False,
        "progression": "Lacrosse Ball IT Band",
        "regression": None,
        "coaching_cues": [
            "Roll slowly, pausing on tender spots for 20-30 seconds",
            "Keep core engaged to stabilize torso",
            "Breathe deeply throughout the movement",
            "Avoid rolling directly over joints"
        ],
        "common_faults": [
            "Rolling too quickly without pausing",
            "Holding breath during pressure points",
            "Rolling directly on knee or hip joint",
            "Using bodyweight instead of controlled pressure"
        ],
        "contraindications": [
            "Acute IT band inflammation",
            "Recent knee surgery",
            "Skin conditions or open wounds"
        ],
        "equipment_alternatives": ["Lacrosse ball", "Massage gun", "Tennis ball"],
        "technical_difficulty": 1,
        "training_age_min_months": 0,
        "force_vector": "N/A - Self-myofascial release",
        "sport_tags": ["Baseball", "Basketball", "Cricket", "Football", "Rugby", "Soccer", "Tennis", "Track & Field"]
    },
    {
        "id": "REC-002",
        "name": "Foam Roller Thoracic Extension",
        "family": "Recovery",
        "secondary_family": "Mobility",
        "objective": "MOB",
        "difficulty": 1,
        "equipment": ["Foam Roller"],
        "unilateral": False,
        "explosive": False,
        "isometric": False,
        "rotational": False,
        "progression": "Foam Roller Thoracic Rotation",
        "regression": "Seated Thoracic Extension",
        "coaching_cues": [
            "Place roller at mid-back, hands supporting head",
            "Gently extend over roller, opening chest",
            "Keep hips grounded throughout movement",
            "Breathe into the stretch, don't force range"
        ],
        "common_faults": [
            "Placing roller too high on neck",
            "Arching lower back instead of thoracic spine",
            "Lifting hips off ground",
            "Bouncing instead of holding stretch"
        ],
        "contraindications": [
            "Thoracic spine injury or fracture",
            "Severe osteoporosis",
            "Recent spinal surgery"
        ],
        "equipment_alternatives": ["Yoga block", "Rolled towel", "Peanut ball"],
        "technical_difficulty": 2,
        "training_age_min_months": 1,
        "force_vector": "N/A - Mobility",
        "sport_tags": ["Baseball", "Basketball", "Cricket", "Football", "Golf", "Rugby", "Swimming", "Tennis"]
    },
    {
        "id": "REC-003",
        "name": "Couch Stretch",
        "family": "Recovery",
        "secondary_family": "Mobility",
        "objective": "MOB",
        "difficulty": 2,
        "equipment": ["Wall", "Box"],
        "unilateral": True,
        "explosive": False,
        "isometric": True,
        "rotational": False,
        "progression": "Weighted Couch Stretch",
        "regression": "Half Kneeling Hip Flexor Stretch",
        "coaching_cues": [
            "Back knee against wall, shin vertical up wall",
            "Squeeze glute of stretching leg",
            "Keep torso upright, don't lean forward",
            "Hold for 2-3 minutes per side"
        ],
        "common_faults": [
            "Leaning forward instead of staying upright",
            "Not squeezing glute",
            "Front foot too far forward",
            "Giving up too soon (needs time under tension)"
        ],
        "contraindications": [
            "Acute knee injury or patellar tendinopathy",
            "Severe hip flexor strain",
            "Recent knee surgery"
        ],
        "equipment_alternatives": ["Bed edge", "Bench", "Sofa"],
        "technical_difficulty": 2,
        "training_age_min_months": 2,
        "force_vector": "N/A - Static stretch",
        "sport_tags": ["Baseball", "Basketball", "Cricket", "Cycling", "Football", "Rugby", "Soccer", "Track & Field"]
    },
    {
        "id": "REC-004",
        "name": "90/90 Hip Switch",
        "family": "Recovery",
        "secondary_family": "Mobility",
        "objective": "MOB",
        "difficulty": 2,
        "equipment": ["Bodyweight"],
        "unilateral": True,
        "explosive": False,
        "isometric": False,
        "rotational": True,
        "progression": "90/90 with Lean",
        "regression": "Seated 90/90 Hold",
        "coaching_cues": [
            "Sit with both legs at 90 degrees, one front one side",
            "Keep both knees bent at 90 degrees throughout",
            "Rotate from hips, not spine",
            "Move slowly and control the transition"
        ],
        "common_faults": [
            "Letting back knee bend past 90",
            "Rotating through spine instead of hips",
            "Lifting opposite butt cheek off ground",
            "Moving too fast without control"
        ],
        "contraindications": [
            "Acute hip labral tear",
            "Recent hip replacement",
            "Severe hip impingement"
        ],
        "equipment_alternatives": ["Elevated surface", "Wall support", "Band assistance"],
        "technical_difficulty": 3,
        "training_age_min_months": 3,
        "force_vector": "N/A - Active mobility",
        "sport_tags": ["Baseball", "Basketball", "Cricket", "Football", "Golf", "MMA", "Rugby", "Tennis"]
    },
    {
        "id": "REC-005",
        "name": "Dead Hang Shoulder Decompression",
        "family": "Recovery",
        "secondary_family": "Mobility",
        "objective": "MOB",
        "difficulty": 1,
        "equipment": ["Pull-up Bar"],
        "unilateral": False,
        "explosive": False,
        "isometric": True,
        "rotational": False,
        "progression": "Active Dead Hang",
        "regression": "Feet-Assisted Hang",
        "coaching_cues": [
            "Grip bar slightly wider than shoulder width",
            "Relax shoulders completely, let them elevate",
            "Breathe deeply into ribcage",
            "Hold 30-60 seconds, shake out arms between"
        ],
        "common_faults": [
            "Gripping too tight (death grip)",
            "Keeping shoulders depressed actively",
            "Holding breath",
            "Swinging or kipping"
        ],
        "contraindications": [
            "Shoulder instability or dislocation history",
            "Acute rotator cuff injury",
            "Elbow ligament injury"
        ],
        "equipment_alternatives": ["Suspension trainer", "Gymnastic rings", "Sturdy branch"],
        "technical_difficulty": 1,
        "training_age_min_months": 0,
        "force_vector": "Vertical traction",
        "sport_tags": ["Baseball", "Basketball", "Cricket", "Climbing", "Football", "Gymnastics", "Rugby", "Swimming"]
    },
    {
        "id": "REC-006",
        "name": "Pec Doorway Stretch",
        "family": "Recovery",
        "secondary_family": "Mobility",
        "objective": "MOB",
        "difficulty": 1,
        "equipment": ["Doorway"],
        "unilateral": True,
        "explosive": False,
        "isometric": True,
        "rotational": False,
        "progression": "Corner Pec Stretch",
        "regression": "Seated Pec Stretch",
        "coaching_cues": [
            "Forearm on doorframe at shoulder height",
            "Step through gently until stretch felt in chest",
            "Keep shoulder blade retracted",
            "Breathe and relax into stretch"
        ],
        "common_faults": [
            "Arm too high (above shoulder)",
            "Protracting shoulder blade",
            "Leaning too aggressively",
            "Arching lower back"
        ],
        "contraindications": [
            "Shoulder impingement syndrome",
            "AC joint separation",
            "Recent pec strain"
        ],
        "equipment_alternatives": ["Wall corner", "Rack post", "Tree"],
        "technical_difficulty": 1,
        "training_age_min_months": 0,
        "force_vector": "N/A - Static stretch",
        "sport_tags": ["Baseball", "Basketball", "Cricket", "Football", "Rugby", "Swimming", "Tennis", "Volleyball"]
    },
    {
        "id": "REC-007",
        "name": "Ankle Dorsiflexion Rock",
        "family": "Recovery",
        "secondary_family": "Mobility",
        "objective": "MOB",
        "difficulty": 1,
        "equipment": ["Wall"],
        "unilateral": True,
        "explosive": False,
        "isometric": False,
        "rotational": False,
        "progression": "Weighted Ankle Rock",
        "regression": "Seated Ankle Pump",
        "coaching_cues": [
            "Foot flat, toes 2-3 inches from wall",
            "Drive knee toward wall without heel lifting",
            "Rock forward and back rhythmically",
            "Keep entire foot in contact with ground"
        ],
        "common_faults": [
            "Heel lifting off ground",
            "Knee caving inward",
            "Foot pronating excessively",
            "Too far from wall initially"
        ],
        "contraindications": [
            "Acute ankle sprain",
            "Achilles tendon rupture",
            "Recent ankle fracture"
        ],
        "equipment_alternatives": ["Band-assisted", "Slant board", "Book stack"],
        "technical_difficulty": 1,
        "training_age_min_months": 0,
        "force_vector": "N/A - Mobility drill",
        "sport_tags": ["Basketball", "Cricket", "Football", "Rugby", "Soccer", "Tennis", "Track & Field", "Volleyball"]
    },
    {
        "id": "REC-008",
        "name": "Lat Child's Pose Reach",
        "family": "Recovery",
        "secondary_family": "Mobility",
        "objective": "MOB",
        "difficulty": 1,
        "equipment": ["Mat"],
        "unilateral": False,
        "explosive": False,
        "isometric": True,
        "rotational": False,
        "progression": "Thread the Needle",
        "regression": "Regular Child's Pose",
        "coaching_cues": [
            "Sit back on heels, reach arms forward",
            "Walk hands to one side for lat bias",
            "Keep hips stacked over heels",
            "Breathe into armpit and ribcage"
        ],
        "common_faults": [
            "Lifting hips off heels",
            "Shrugging shoulders up",
            "Not reaching far enough",
            "Holding breath"
        ],
        "contraindications": [
            "Knee injury (meniscus)",
            "Pregnancy (third trimester)",
            "Severe shoulder impingement"
        ],
        "equipment_alternatives": ["Blanket under knees", "Block under chest", "Wall support"],
        "technical_difficulty": 1,
        "training_age_min_months": 0,
        "force_vector": "N/A - Static stretch",
        "sport_tags": ["Baseball", "Basketball", "Climbing", "Football", "Gymnastics", "Rugby", "Swimming", "Volleyball"]
    },
    {
        "id": "REC-009",
        "name": "Neck CARs (Controlled Articular Rotations)",
        "family": "Recovery",
        "secondary_family": "Mobility",
        "objective": "MOB",
        "difficulty": 2,
        "equipment": ["Bodyweight"],
        "unilateral": False,
        "explosive": False,
        "isometric": False,
        "rotational": True,
        "progression": "Resisted Neck CARs",
        "regression": "Neck Nods Only",
        "coaching_cues": [
            "Keep torso completely still",
            "Move only from cervical spine",
            "Make largest circle possible without pain",
            "Slow and controlled, 5 seconds each direction"
        ],
        "common_faults": [
            "Moving thoracic spine with neck",
            "Going too fast",
            "Shrugging shoulders",
            "Pushing into pain"
        ],
        "contraindications": [
            "Cervical spine injury or instability",
            "Vertigo or balance disorders",
            "Recent whiplash"
        ],
        "equipment_alternatives": ["Wall support", "Chair back", "Hand assistance"],
        "technical_difficulty": 2,
        "training_age_min_months": 1,
        "force_vector": "N/A - Active mobility",
        "sport_tags": ["Boxing", "Cricket", "Football", "Gymnastics", "MMA", "Rugby", "Wrestling", "Motorsports"]
    },
    {
        "id": "REC-010",
        "name": "World's Greatest Stretch",
        "family": "Recovery",
        "secondary_family": "Mobility",
        "objective": "MOB",
        "difficulty": 2,
        "equipment": ["Bodyweight"],
        "unilateral": True,
        "explosive": False,
        "isometric": False,
        "rotational": True,
        "progression": "With Band",
        "regression": "Split Lunge Only",
        "coaching_cues": [
            "Deep lunge position, back knee down",
            "Same side elbow to instep",
            "Rotate chest open toward ceiling",
            "Return and switch sides smoothly"
        ],
        "common_faults": [
            "Front knee collapsing inward",
            "Back knee not grounded",
            "Rushing the movement",
            "Not getting full rotation"
        ],
        "contraindications": [
            "Acute hip or knee injury",
            "Groin strain",
            "Balance disorders"
        ],
        "equipment_alternatives": ["Elevated front foot", "Wall support", "Band assist"],
        "technical_difficulty": 3,
        "training_age_min_months": 2,
        "force_vector": "N/A - Dynamic mobility",
        "sport_tags": ["Baseball", "Basketball", "Cricket", "Football", "Golf", "Rugby", "Soccer", "Tennis"]
    },
    {
        "id": "REC-011",
        "name": "Hamstring Flossing",
        "family": "Recovery",
        "secondary_family": "Mobility",
        "objective": "MOB",
        "difficulty": 1,
        "equipment": ["Band"],
        "unilateral": True,
        "explosive": False,
        "isometric": False,
        "rotational": False,
        "progression": "Heavier Band",
        "regression": "Static Hamstring Stretch",
        "coaching_cues": [
            "Band high on thigh near crease",
            "Anchor band behind you at hip height",
            "Straighten and bend knee repeatedly",
            "Feel the flossing action through hamstring"
        ],
        "common_faults": [
            "Band too low on leg",
            "Anchor point too high or low",
            "Moving too fast",
            "Not enough tension in band"
        ],
        "contraindications": [
            "Acute hamstring tear",
            "Sciatica flare-up",
            "Recent hip surgery"
        ],
        "equipment_alternatives": ["Towel", "Resistance tube", "No band (active)"],
        "technical_difficulty": 2,
        "training_age_min_months": 1,
        "force_vector": "N/A - Flossing technique",
        "sport_tags": ["Cricket", "Football", "Hockey", "Rugby", "Soccer", "Track & Field", "Tennis", "Volleyball"]
    },
    {
        "id": "REC-012",
        "name": "Adductor Rock Back",
        "family": "Recovery",
        "secondary_family": "Mobility",
        "objective": "MOB",
        "difficulty": 1,
        "equipment": ["Mat"],
        "unilateral": False,
        "explosive": False,
        "isometric": False,
        "rotational": False,
        "progression": "Side Lunge Adductor Rock",
        "regression": "Butterfly Stretch",
        "coaching_cues": [
            "Wide knee stance, feet together",
            "Rock hips back toward heels",
            "Keep spine neutral",
            "Feel stretch in inner thighs"
        ],
        "common_faults": [
            "Knees collapsing inward",
            "Rounding lower back",
            "Rocking too far back",
            "Feet lifting off ground"
        ],
        "contraindications": [
            "Acute groin strain",
            "Hip labral tear",
            "Knee MCL injury"
        ],
        "equipment_alternatives": ["Elevated knees", "Wall support", "Band assist"],
        "technical_difficulty": 1,
        "training_age_min_months": 0,
        "force_vector": "N/A - Dynamic stretch",
        "sport_tags": ["Basketball", "Cricket", "Football", "Hockey", "MMA", "Rugby", "Soccer", "Wrestling"]
    },
    {
        "id": "REC-013",
        "name": "Breathing Diaphragmatic Reset",
        "family": "Recovery",
        "secondary_family": None,
        "objective": "RECOV",
        "difficulty": 1,
        "equipment": ["Mat"],
        "unilateral": False,
        "explosive": False,
        "isometric": False,
        "rotational": False,
        "progression": "90/90 Breathing",
        "regression": None,
        "coaching_cues": [
            "Lie on back, knees bent 90 degrees on chair",
            "Hands on lower ribs",
            "Inhale through nose, expand ribs 360 degrees",
            "Exhale fully through mouth, feel ribs descend"
        ],
        "common_faults": [
            "Chest breathing instead of diaphragm",
            "Holding breath between cycles",
            "Arching lower back",
            "Rushing the breathing pattern"
        ],
        "contraindications": [
            "Severe respiratory conditions",
            "Recent abdominal surgery",
            "Uncontrolled hypertension"
        ],
        "equipment_alternatives": ["Floor only", "Bench", "Wall leg support"],
        "technical_difficulty": 1,
        "training_age_min_months": 0,
        "force_vector": "N/A - Breathing exercise",
        "sport_tags": ["All Sports"]
    },
    {
        "id": "REC-014",
        "name": "Glute Bridge March",
        "family": "Recovery",
        "secondary_family": "Activation",
        "objective": "ACT",
        "difficulty": 1,
        "equipment": ["Bodyweight"],
        "unilateral": True,
        "explosive": False,
        "isometric": False,
        "rotational": False,
        "progression": "Single Leg Glute Bridge",
        "regression": "Double Leg Glute Bridge",
        "coaching_cues": [
            "Bridge up, squeeze glutes hard",
            "Lift one foot 2-3 inches",
            "Keep hips level, don't rotate",
            "Alternate legs in controlled march"
        ],
        "common_faults": [
            "Hips dropping when lifting leg",
            "Overarching lower back",
            "Not squeezing glutes",
            "Lifting foot too high"
        ],
        "contraindications": [
            "Acute lower back injury",
            "Recent hip surgery",
            "Severe hamstring strain"
        ],
        "equipment_alternatives": ["Band above knees", "Elevated shoulders", "Slider under foot"],
        "technical_difficulty": 2,
        "training_age_min_months": 1,
        "force_vector": "Hip extension",
        "sport_tags": ["Basketball", "Cricket", "Football", "Rugby", "Soccer", "Track & Field", "Tennis", "Volleyball"]
    },
    {
        "id": "REC-015",
        "name": "Scapular Wall Slides",
        "family": "Recovery",
        "secondary_family": "Activation",
        "objective": "ACT",
        "difficulty": 1,
        "equipment": ["Wall"],
        "unilateral": False,
        "explosive": False,
        "isometric": False,
        "rotational": False,
        "progression": "Band-Resisted Wall Slides",
        "regression": "Seated Scapular Retraction",
        "coaching_cues": [
            "Back, head, and arms against wall",
            "Elbows and wrists maintain contact",
            "Slide arms up without arching back",
            "Focus on scapular upward rotation"
        ],
        "common_faults": [
            "Losing contact with wall",
            "Arching lower back",
            "Shrugging shoulders up",
            "Elbows bending"
        ],
        "contraindications": [
            "Shoulder impingement",
            "Frozen shoulder",
            "Recent rotator cuff injury"
        ],
        "equipment_alternatives": ["Foam roller on wall", "Door frame", "No wall (prone)"],
        "technical_difficulty": 2,
        "training_age_min_months": 1,
        "force_vector": "Scapular upward rotation",
        "sport_tags": ["Baseball", "Basketball", "Cricket", "Football", "Rugby", "Swimming", "Tennis", "Volleyball"]
    },
    
    # === ACTIVATION EXERCISES (10 exercises) ===
    {
        "id": "ACT-001",
        "name": "Mini Band Lateral Walk",
        "family": "Activation",
        "secondary_family": None,
        "objective": "ACT",
        "difficulty": 1,
        "equipment": ["Mini Band"],
        "unilateral": False,
        "explosive": False,
        "isometric": False,
        "rotational": False,
        "progression": "Monster Walk",
        "regression": "Clamshells",
        "coaching_cues": [
            "Band around ankles or just above knees",
            "Athletic stance, slight knee bend",
            "Step laterally, maintaining tension",
            "Keep toes pointing forward"
        ],
        "common_faults": [
            "Knees caving inward",
            "Standing too upright",
            "Taking steps too wide",
            "Losing band tension"
        ],
        "contraindications": [
            "Acute knee injury",
            "Hip bursitis flare-up",
            "Ankle instability"
        ],
        "equipment_alternatives": ["Resistance band", "Cable machine", "No band (isometric)"],
        "technical_difficulty": 1,
        "training_age_min_months": 0,
        "force_vector": "Hip abduction",
        "sport_tags": ["Basketball", "Cricket", "Football", "Rugby", "Soccer", "Tennis", "Track & Field", "Volleyball"]
    },
    {
        "id": "ACT-002",
        "name": "Band Pull-Aparts",
        "family": "Activation",
        "secondary_family": None,
        "objective": "ACT",
        "difficulty": 1,
        "equipment": ["Resistance Band"],
        "unilateral": False,
        "explosive": False,
        "isometric": False,
        "rotational": False,
        "progression": "Face Pulls",
        "regression": "Scapular Squeezes",
        "coaching_cues": [
            "Arms straight at shoulder height",
            "Pull band apart by squeezing shoulder blades",
            "Keep chest tall, don't shrug",
            "Control the return"
        ],
        "common_faults": [
            "Bending elbows",
            "Shrugging shoulders",
            "Arching lower back",
            "Using momentum"
        ],
        "contraindications": [
            "Shoulder impingement",
            "AC joint injury",
            "Rotator cuff tear"
        ],
        "equipment_alternatives": ["Cable machine", "Towel isometric", "No equipment"],
        "technical_difficulty": 1,
        "training_age_min_months": 0,
        "force_vector": "Horizontal pull",
        "sport_tags": ["Baseball", "Basketball", "Cricket", "Football", "Rugby", "Swimming", "Tennis", "Volleyball"]
    },
    {
        "id": "ACT-003",
        "name": "Dead Bug",
        "family": "Activation",
        "secondary_family": "Core",
        "objective": "ACT",
        "difficulty": 2,
        "equipment": ["Mat"],
        "unilateral": True,
        "explosive": False,
        "isometric": False,
        "rotational": False,
        "progression": "Weighted Dead Bug",
        "regression": "Single Arm/Leg Only",
        "coaching_cues": [
            "Lower back pressed into floor",
            "Arms extended toward ceiling",
            "Opposite arm and leg lower slowly",
            "Maintain ribcage down position"
        ],
        "common_faults": [
            "Lower back arching off floor",
            "Moving arm and leg on same side",
            "Dropping limbs too fast",
            "Holding breath"
        ],
        "contraindications": [
            "Acute lower back injury",
            "Diastasis recti",
            "Recent abdominal surgery"
        ],
        "equipment_alternatives": ["Bench", "Swiss ball", "Band resistance"],
        "technical_difficulty": 2,
        "training_age_min_months": 1,
        "force_vector": "Anti-extension",
        "sport_tags": ["All Sports"]
    },
    {
        "id": "ACT-004",
        "name": "Bird Dog",
        "family": "Activation",
        "secondary_family": "Core",
        "objective": "ACT",
        "difficulty": 1,
        "equipment": ["Mat"],
        "unilateral": True,
        "explosive": False,
        "isometric": False,
        "rotational": False,
        "progression": "Bird Dog Row",
        "regression": "Quadruped Hold",
        "coaching_cues": [
            "Start on all fours, neutral spine",
            "Extend opposite arm and leg",
            "Keep hips square to ground",
            "Pause at top, squeeze glute"
        ],
        "common_faults": [
            "Rotating hips",
            "Looking up instead of neutral",
            "Extending too high",
            "Rushing repetitions"
        ],
        "contraindications": [
            "Wrist injury",
            "Shoulder instability",
            "Acute lower back pain"
        ],
        "equipment_alternatives": ["Elevated hands", "Knee pad", "Wall version"],
        "technical_difficulty": 1,
        "training_age_min_months": 0,
        "force_vector": "Anti-rotation",
        "sport_tags": ["All Sports"]
    },
    {
        "id": "ACT-005",
        "name": "Pallof Press",
        "family": "Activation",
        "secondary_family": "Core",
        "objective": "ACT",
        "difficulty": 2,
        "equipment": ["Cable", "Band"],
        "unilateral": False,
        "explosive": False,
        "isometric": True,
        "rotational": False,
        "progression": "Pallof Press with Rotation",
        "regression": "Half-Kneeling Pallof",
        "coaching_cues": [
            "Stand perpendicular to cable/band",
            "Press handle straight out from chest",
            "Resist rotation, stay square",
            "Hold 2-3 seconds, return slowly"
        ],
        "common_faults": [
            "Allowing rotation toward anchor",
            "Leaning away from anchor",
            "Pressing too fast",
            "Not engaging core"
        ],
        "contraindications": [
            "Shoulder instability",
            "Acute core injury",
            "Uncontrolled hypertension"
        ],
        "equipment_alternatives": ["Resistance band", "Partner resistance", "Landmine"],
        "technical_difficulty": 2,
        "training_age_min_months": 2,
        "force_vector": "Anti-rotation",
        "sport_tags": ["Baseball", "Basketball", "Cricket", "Football", "Golf", "Rugby", "Tennis", "Volleyball"]
    },
    {
        "id": "ACT-006",
        "name": "Ankle Hops (Pogo)",
        "family": "Activation",
        "secondary_family": "Plyo",
        "objective": "ACT",
        "difficulty": 1,
        "equipment": ["Bodyweight"],
        "unilateral": False,
        "explosive": True,
        "isometric": False,
        "rotational": False,
        "progression": "Single Leg Pogos",
        "regression": "March in Place",
        "coaching_cues": [
            "Stay on balls of feet",
            "Quick, light contacts",
            "Minimal knee bend",
            "Arms relaxed at sides"
        ],
        "common_faults": [
            "Landing flat-footed",
            "Bending knees too much",
            "Heavy, loud landings",
            "Tensing shoulders"
        ],
        "contraindications": [
            "Acute Achilles injury",
            "Plantar fasciitis flare-up",
            "Recent ankle sprain"
        ],
        "equipment_alternatives": ["Jump rope", "Low box", "Grass surface"],
        "technical_difficulty": 1,
        "training_age_min_months": 0,
        "force_vector": "Vertical elastic",
        "sport_tags": ["Basketball", "Cricket", "Football", "Rugby", "Soccer", "Tennis", "Track & Field", "Volleyball"]
    },
    {
        "id": "ACT-007",
        "name": "Inchworm",
        "family": "Activation",
        "secondary_family": "Core",
        "objective": "ACT",
        "difficulty": 2,
        "equipment": ["Bodyweight"],
        "unilateral": False,
        "explosive": False,
        "isometric": False,
        "rotational": False,
        "progression": "Inchworm to Push-up",
        "regression": "Walkout Only",
        "coaching_cues": [
            "Stand tall, hinge at hips",
            "Walk hands out to plank",
            "Keep core tight in plank",
            "Walk feet to hands, stand up"
        ],
        "common_faults": [
            "Sagging hips in plank",
            "Rushing the walkout",
            "Not fully extending at top",
            "Holding breath"
        ],
        "contraindications": [
            "Wrist injury",
            "Shoulder instability",
            "Acute hamstring strain"
        ],
        "equipment_alternatives": ["Sliders", "Towel on turf", "Elevated hands"],
        "technical_difficulty": 2,
        "training_age_min_months": 1,
        "force_vector": "Dynamic core",
        "sport_tags": ["Basketball", "Cricket", "Football", "Gymnastics", "Rugby", "Soccer", "Tennis", "Wrestling"]
    },
    {
        "id": "ACT-008",
        "name": "Lateral Lunge Matrix",
        "family": "Activation",
        "secondary_family": None,
        "objective": "ACT",
        "difficulty": 2,
        "equipment": ["Bodyweight"],
        "unilateral": True,
        "explosive": False,
        "isometric": False,
        "rotational": False,
        "progression": "Curtsy Lunge Matrix",
        "regression": "Assisted Lunge",
        "coaching_cues": [
            "Step laterally, sink into hip",
            "Keep toe of stepping leg up",
            "Push off outside foot to return",
            "Control the movement in all planes"
        ],
        "common_faults": [
            "Knee caving inward",
            "Leaning too far forward",
            "Not sinking deep enough",
            "Rushing between directions"
        ],
        "contraindications": [
            "Acute knee injury",
            "Hip impingement",
            "Groin strain"
        ],
        "equipment_alternatives": ["TRX assist", "Wall support", "Elevated surface"],
        "technical_difficulty": 2,
        "training_age_min_months": 2,
        "force_vector": "Multi-planar",
        "sport_tags": ["Basketball", "Cricket", "Football", "Rugby", "Soccer", "Tennis", "Track & Field", "Volleyball"]
    },
    {
        "id": "ACT-009",
        "name": "Arm Circles Progressive",
        "family": "Activation",
        "secondary_family": None,
        "objective": "ACT",
        "difficulty": 1,
        "equipment": ["Bodyweight"],
        "unilateral": False,
        "explosive": False,
        "isometric": False,
        "rotational": True,
        "progression": "Weighted Arm Circles",
        "regression": "Small Circles Only",
        "coaching_cues": [
            "Start with small forward circles",
            "Gradually increase circle size",
            "Switch to backward circles",
            "Keep shoulders relaxed, not shrugged"
        ],
        "common_faults": [
            "Starting with circles too large",
            "Shrugging shoulders",
            "Moving too fast",
            "Arching lower back"
        ],
        "contraindications": [
            "Shoulder dislocation history",
            "Acute rotator cuff injury",
            "Frozen shoulder"
        ],
        "equipment_alternatives": ["Light weights", "Band", "Wall slides"],
        "technical_difficulty": 1,
        "training_age_min_months": 0,
        "force_vector": "Shoulder mobility",
        "sport_tags": ["Baseball", "Basketball", "Cricket", "Football", "Rugby", "Swimming", "Tennis", "Volleyball"]
    },
    {
        "id": "ACT-010",
        "name": "Hip Flexor March",
        "family": "Activation",
        "secondary_family": None,
        "objective": "ACT",
        "difficulty": 1,
        "equipment": ["Bodyweight"],
        "unilateral": True,
        "explosive": False,
        "isometric": False,
        "rotational": False,
        "progression": "Band-Resisted March",
        "regression": "Seated March",
        "coaching_cues": [
            "Stand tall, engage core",
            "Lift knee to hip height",
            "Hold 2 seconds at top",
            "Alternate legs with control"
        ],
        "common_faults": [
            "Leaning back",
            "Not lifting knee high enough",
            "Rushing the movement",
            "Swinging leg instead of lifting"
        ],
        "contraindications": [
            "Acute hip flexor strain",
            "Hip impingement",
            "Lower back injury"
        ],
        "equipment_alternatives": ["Band resistance", "Wall support", "Seated version"],
        "technical_difficulty": 1,
        "training_age_min_months": 0,
        "force_vector": "Hip flexion",
        "sport_tags": ["Cricket", "Football", "Rugby", "Soccer", "Track & Field", "Tennis", "Volleyball", "Hockey"]
    },
    
    # === ASSESSMENT EXERCISES (10 exercises) ===
    {
        "id": "ASMT-001",
        "name": "Overhead Squat Assessment",
        "family": "Assessment",
        "secondary_family": "DLKD",
        "objective": "ASSESS",
        "difficulty": 3,
        "equipment": ["PVC Pipe", "Dowel"],
        "unilateral": False,
        "explosive": False,
        "isometric": False,
        "rotational": False,
        "progression": "Barbell Overhead Squat",
        "regression": "Air Squat",
        "coaching_cues": [
            "Hold dowel overhead with wide grip",
            "Keep arms locked out throughout",
            "Squat to parallel or below",
            "Maintain dowel over mid-foot"
        ],
        "common_faults": [
            "Dowel falling forward",
            "Heels lifting off ground",
            "Knees caving inward",
            "Excessive forward lean"
        ],
        "contraindications": [
            "Shoulder impingement",
            "Acute knee injury",
            "Inability to raise arms overhead"
        ],
        "equipment_alternatives": ["Broomstick", "Light barbell", "No equipment (arms only)"],
        "technical_difficulty": 4,
        "training_age_min_months": 6,
        "force_vector": "Vertical compressive",
        "sport_tags": ["All Sports"]
    },
    {
        "id": "ASMT-002",
        "name": "Single Leg Squat Assessment",
        "family": "Assessment",
        "secondary_family": "SLKD",
        "objective": "ASSESS",
        "difficulty": 3,
        "equipment": ["Box", "Bench"],
        "unilateral": True,
        "explosive": False,
        "isometric": False,
        "rotational": False,
        "progression": "Pistol Squat Assessment",
        "regression": "Assisted Single Leg Squat",
        "coaching_cues": [
            "Stand on one leg, other leg extended",
            "Sit back to box lightly",
            "Keep knee tracking over toe",
            "Return to standing with control"
        ],
        "common_faults": [
            "Knee valgus (caving in)",
            "Hip drop on non-stance side",
            "Unable to reach box",
            "Excessive trunk lean"
        ],
        "contraindications": [
            "Acute knee injury",
            "Ankle instability",
            "Recent hip surgery"
        ],
        "equipment_alternatives": ["Chair", "Step", "TRX assist"],
        "technical_difficulty": 3,
        "training_age_min_months": 6,
        "force_vector": "Vertical unilateral",
        "sport_tags": ["Basketball", "Cricket", "Football", "Rugby", "Soccer", "Tennis", "Track & Field", "Volleyball"]
    },
    {
        "id": "ASMT-003",
        "name": "Push-Up Assessment",
        "family": "Assessment",
        "secondary_family": "HPush",
        "objective": "ASSESS",
        "difficulty": 2,
        "equipment": ["Mat"],
        "unilateral": False,
        "explosive": False,
        "isometric": False,
        "rotational": False,
        "progression": "Weighted Push-Up Assessment",
        "regression": "Incline Push-Up Assessment",
        "coaching_cues": [
            "Hands slightly wider than shoulders",
            "Body in straight line head to heels",
            "Lower until chest nearly touches ground",
            "Push back up maintaining form"
        ],
        "common_faults": [
            "Sagging hips",
            "Incomplete range of motion",
            "Flared elbows",
            "Head jutting forward"
        ],
        "contraindications": [
            "Wrist injury",
            "Shoulder instability",
            "Acute pec strain"
        ],
        "equipment_alternatives": ["Parallettes", "Handles", "Incline surface"],
        "technical_difficulty": 2,
        "training_age_min_months": 3,
        "force_vector": "Horizontal push",
        "sport_tags": ["All Sports"]
    },
    {
        "id": "ASMT-004",
        "name": "Plank Endurance Test",
        "family": "Assessment",
        "secondary_family": "Core",
        "objective": "ASSESS",
        "difficulty": 2,
        "equipment": ["Mat", "Timer"],
        "unilateral": False,
        "explosive": False,
        "isometric": True,
        "rotational": False,
        "progression": "RKC Plank Test",
        "regression": "Knee Plank Test",
        "coaching_cues": [
            "Forearms on ground, elbows under shoulders",
            "Body straight from head to heels",
            "Squeeze glutes and brace core",
            "Hold as long as form maintained"
        ],
        "common_faults": [
            "Hips sagging",
            "Hips piked up",
            "Holding breath",
            "Continuing after form breakdown"
        ],
        "contraindications": [
            "Acute lower back injury",
            "Shoulder impingement",
            "Diastasis recti"
        ],
        "equipment_alternatives": ["Bench", "TRX", "Swiss ball"],
        "technical_difficulty": 1,
        "training_age_min_months": 1,
        "force_vector": "Anti-extension",
        "sport_tags": ["All Sports"]
    },
    {
        "id": "ASMT-005",
        "name": "Y-Balance Test",
        "family": "Assessment",
        "secondary_family": None,
        "objective": "ASSESS",
        "difficulty": 3,
        "equipment": ["Y-Balance Kit", "Tape"],
        "unilateral": True,
        "explosive": False,
        "isometric": False,
        "rotational": False,
        "progression": "Star Excursion Test",
        "regression": "Single Leg Stance",
        "coaching_cues": [
            "Stand on one leg at center",
            "Reach as far as possible in each direction",
            "Return to center without touching down",
            "Complete 3 trials each direction"
        ],
        "common_faults": [
            "Lifting stance foot",
            "Touching down with reach foot",
            "Losing balance",
            "Not returning to center"
        ],
        "contraindications": [
            "Acute ankle sprain",
            "Recent knee surgery",
            "Balance disorders"
        ],
        "equipment_alternatives": ["Tape grid", "Chalk lines", "Mats with markings"],
        "technical_difficulty": 3,
        "training_age_min_months": 6,
        "force_vector": "Multi-directional stability",
        "sport_tags": ["Basketball", "Cricket", "Football", "Rugby", "Soccer", "Tennis", "Track & Field", "Volleyball"]
    },
    {
        "id": "ASMT-006",
        "name": "Shoulder Mobility Test",
        "family": "Assessment",
        "secondary_family": None,
        "objective": "ASSESS",
        "difficulty": 2,
        "equipment": ["Ruler", "Tape"],
        "unilateral": False,
        "explosive": False,
        "isometric": False,
        "rotational": False,
        "progression": "Weighted Shoulder Test",
        "regression": "Apley Scratch Test",
        "coaching_cues": [
            "Make fists, thumbs inside",
            "Reach one hand over shoulder, one behind back",
            "Try to touch fingertips",
            "Measure distance between hands"
        ],
        "common_faults": [
            "Bending elbows to cheat",
            "Rotating torso",
            "Not making fists",
            "Forcing beyond comfortable range"
        ],
        "contraindications": [
            "Shoulder dislocation history",
            "Acute rotator cuff injury",
            "Frozen shoulder"
        ],
        "equipment_alternatives": ["Towel", "Band", "Visual estimation"],
        "technical_difficulty": 2,
        "training_age_min_months": 3,
        "force_vector": "N/A - Mobility assessment",
        "sport_tags": ["Baseball", "Basketball", "Cricket", "Football", "Rugby", "Swimming", "Tennis", "Volleyball"]
    },
    {
        "id": "ASMT-007",
        "name": "Ankle Dorsiflexion Test",
        "family": "Assessment",
        "secondary_family": None,
        "objective": "ASSESS",
        "difficulty": 1,
        "equipment": ["Wall", "Ruler"],
        "unilateral": True,
        "explosive": False,
        "isometric": False,
        "rotational": False,
        "progression": "Weighted Ankle Test",
        "regression": "Seated Ankle Test",
        "coaching_cues": [
            "Foot perpendicular to wall",
            "Drive knee to touch wall",
            "Keep heel on ground",
            "Measure max distance from wall"
        ],
        "common_faults": [
            "Heel lifting",
            "Foot rotating outward",
            "Knee caving inward",
            "Not measuring consistently"
        ],
        "contraindications": [
            "Acute ankle sprain",
            "Achilles rupture",
            "Recent foot fracture"
        ],
        "equipment_alternatives": ["Box", "Step", "Angle app"],
        "technical_difficulty": 1,
        "training_age_min_months": 0,
        "force_vector": "N/A - Mobility assessment",
        "sport_tags": ["Basketball", "Cricket", "Football", "Rugby", "Soccer", "Tennis", "Track & Field", "Volleyball"]
    },
    {
        "id": "ASMT-008",
        "name": "Broad Jump Assessment",
        "family": "Assessment",
        "secondary_family": "Plyo",
        "objective": "ASSESS",
        "difficulty": 2,
        "equipment": ["Tape Measure", "Mat"],
        "unilateral": False,
        "explosive": True,
        "isometric": False,
        "rotational": False,
        "progression": "Weighted Broad Jump",
        "regression": "Squat Jump",
        "coaching_cues": [
            "Start with feet shoulder-width",
            "Swing arms back, then explode forward",
            "Land softly on both feet",
            "Stick the landing without falling"
        ],
        "common_faults": [
            "False start (foot movement)",
            "Landing unevenly",
            "Falling backward on landing",
            "Not swinging arms effectively"
        ],
        "contraindications": [
            "Acute knee injury",
            "Recent ankle sprain",
            "Lower back injury"
        ],
        "equipment_alternatives": ["Sand pit", "Force plate", "Jump mat"],
        "technical_difficulty": 2,
        "training_age_min_months": 3,
        "force_vector": "Horizontal explosive",
        "sport_tags": ["Basketball", "Cricket", "Football", "Rugby", "Soccer", "Tennis", "Track & Field", "Volleyball"]
    },
    {
        "id": "ASMT-009",
        "name": "Vertical Jump Assessment",
        "family": "Assessment",
        "secondary_family": "Plyo",
        "objective": "ASSESS",
        "difficulty": 2,
        "equipment": ["Vertec", "Wall", "Chalk"],
        "unilateral": False,
        "explosive": True,
        "isometric": False,
        "rotational": False,
        "progression": "Approach Vertical",
        "regression": "Squat Jump",
        "coaching_cues": [
            "Measure standing reach first",
            "Dip into athletic position",
            "Explode up, reach with both hands",
            "Land softly on both feet"
        ],
        "common_faults": [
            "Stepping before jump",
            "Reaching with only one hand",
            "Not measuring standing reach",
            "Landing stiff-legged"
        ],
        "contraindications": [
            "Acute knee injury",
            "Ankle instability",
            "Recent back injury"
        ],
        "equipment_alternatives": ["Jump mat", "Phone app", "Chalk on wall"],
        "technical_difficulty": 2,
        "training_age_min_months": 3,
        "force_vector": "Vertical explosive",
        "sport_tags": ["Basketball", "Cricket", "Football", "Rugby", "Soccer", "Tennis", "Track & Field", "Volleyball"]
    },
    {
        "id": "ASMT-010",
        "name": "Single Leg Hop Test",
        "family": "Assessment",
        "secondary_family": "Plyo",
        "objective": "ASSESS",
        "difficulty": 3,
        "equipment": ["Tape Measure", "Cone"],
        "unilateral": True,
        "explosive": True,
        "isometric": False,
        "rotational": False,
        "progression": "Triple Hop Test",
        "regression": "Double Leg Hop",
        "coaching_cues": [
            "Hop forward for distance",
            "Land on same leg",
            "Stick landing for 2 seconds",
            "Compare left vs right symmetry"
        ],
        "common_faults": [
            "Touching down with other leg",
            "Falling on landing",
            "Not hopping for max distance",
            "Inconsistent starting position"
        ],
        "contraindications": [
            "Recent ACL reconstruction (<6 months)",
            "Acute ankle sprain",
            "Meniscus injury"
        ],
        "equipment_alternatives": ["Force plate", "Jump mat", "Marked floor"],
        "technical_difficulty": 3,
        "training_age_min_months": 6,
        "force_vector": "Unilateral horizontal",
        "sport_tags": ["Basketball", "Cricket", "Football", "Rugby", "Soccer", "Tennis", "Track & Field", "Volleyball"]
    }
]

# Save to JSON file
output_file = '/workspace/phase2_new_exercises.json'
with open(output_file, 'w') as f:
    json.dump(NEW_EXERCISES, f, indent=2)

print(f"✅ Phase 2: Created {len(NEW_EXERCISES)} new exercises")
print(f"📁 Saved to: {output_file}")
print("\nBreakdown:")
print(f"  - Recovery/Mobility: 15 exercises (REC-001 to REC-015)")
print(f"  - Activation: 10 exercises (ACT-001 to ACT-010)")
print(f"  - Assessment: 10 exercises (ASMT-001 to ASMT-010)")
print(f"\nTotal exercises in library will be: 299 + {len(NEW_EXERCISES)} = {299 + len(NEW_EXERCISES)}")
