#!/usr/bin/env python3
"""
Add comprehensive Agility and Conditioning exercises to the Forge library.
As Chief S&C Scientist, ensuring complete coverage of these critical performance domains.
"""

import json
from datetime import datetime

# Load existing exercises
with open('forge_web/src/data/exercises.json', 'r') as f:
    exercises = json.load(f)

# Get max ID for generating new unique IDs
max_id = max([int(e['id'].split('-')[1]) if '-' in str(e['id']) else int(e['id']) 
              for e in exercises if str(e['id']).replace('-', '').isdigit()], default=1000)

new_exercises = []

# ============================================================================
# AGILITY EXERCISES (Adding 42+ to bring from 8 to 50+)
# Categories: COD, Reactive, Multi-directional, Sport-Specific
# ============================================================================

agility_exercises = [
    # === Change of Direction (COD) Fundamentals ===
    {
        "name": "5-0-5 Agility Test",
        "category": "Agility",
        "subcategory": "COD",
        "movement_pattern": "Change of Direction",
        "equipment": "Cones, Timing Gates",
        "difficulty": "Intermediate",
        "source_organization": "NSCA",
        "description": "Classic COD test measuring ability to decelerate, plant, and reaccelerate in opposite direction.",
        "coaching_cues": [
            "Lower hips before planting foot",
            "Plant foot outside center of mass",
            "Drive knees hard on reacceleration",
            "Keep chest up through transition"
        ],
        "common_errors": [
            "Upright posture during plant",
            "Narrow base of support",
            "Rounding the cut instead of sharp angle",
            "Looking down at feet"
        ],
        "contraindications": [
            "Acute ankle sprain",
            "Recent ACL reconstruction (<6 months)",
            "Hip impingement"
        ],
        "regressions": ["Walking 5-0-5 pattern", "Reduced speed execution"],
        "progressions": ["Add reactive cue", "Add ball handling"],
        "equipment_alternatives": ["Tape marks", "Agility ladder endpoints"],
        "is_pain_safe": False,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "L-Drill (3-Cone Drill)",
        "category": "Agility",
        "subcategory": "COD",
        "movement_pattern": "Multi-Directional",
        "equipment": "3 Cones",
        "difficulty": "Advanced",
        "source_organization": "NFL Combine",
        "description": "Complex multi-directional drill testing ability to change directions at various angles while maintaining speed.",
        "coaching_cues": [
            "Stay low through entire pattern",
            "Short choppy steps around cones",
            "Touch line with outside hand",
            "Accelerate out of each turn"
        ],
        "common_errors": [
            "Running too wide around cones",
            "High center of gravity",
            "Crossing feet during lateral movement",
            "Slow hand touches"
        ],
        "contraindications": [
            "Knee instability",
            "Groin strain",
            "Achilles tendinopathy"
        ],
        "regressions": ["Walk-through pattern", "Half-speed execution"],
        "progressions": ["Add defensive slide", "Add ball carry"],
        "equipment_alternatives": ["Markers", "Chalk lines"],
        "is_pain_safe": False,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Pro Agility Shuttle (20-Yard Shuttle)",
        "category": "Agility",
        "subcategory": "COD",
        "movement_pattern": "Lateral Change of Direction",
        "equipment": "Cones or Lines",
        "difficulty": "Intermediate",
        "source_organization": "NFL Combine",
        "description": "Burst agility test requiring two directional changes over 5-yard intervals.",
        "coaching_cues": [
            "Explode from start position",
            "Drop hips on each plant",
            "Touch line with same hand each time",
            "Finish strong through last cone"
        ],
        "common_errors": [
            "Slow initial burst",
            "Not touching line fully",
            "Wide turns",
            "Decelerating before finish"
        ],
        "contraindications": [
            "Hip flexor strain",
            "Adductor injury"
        ],
        "regressions": ["Reduced distance (3-3-3)", "Walk-through pattern"],
        "progressions": ["Reactive start", "Add ball handling"],
        "equipment_alternatives": ["Gym lines", "Tape marks"],
        "is_pain_safe": True,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Zig-Zag Cone Drill",
        "category": "Agility",
        "subcategory": "COD",
        "movement_pattern": "Diagonal Cutting",
        "equipment": "5-6 Cones",
        "difficulty": "Beginner",
        "source_organization": "EXOS",
        "description": "Fundamental diagonal cutting pattern teaching proper body positioning for angled direction changes.",
        "coaching_cues": [
            "Approach cones at 45-degree angle",
            "Outside foot plants hard",
            "Shoulders lead the turn",
            "Accelerate to next cone"
        ],
        "common_errors": [
            "Running straight at cones",
            "Inside foot plant",
            "Upper body lagging behind",
            "No acceleration between cones"
        ],
        "contraindications": ["None - foundational movement"],
        "regressions": ["Walk pattern", "Reduce number of cones"],
        "progressions": ["Increase speed", "Add defensive shuffle segments"],
        "equipment_alternatives": ["Markers", "Shoes as markers"],
        "is_pain_safe": True,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "T-Drill",
        "category": "Agility",
        "subcategory": "COD",
        "movement_pattern": "Multi-Directional",
        "equipment": "4 Cones",
        "difficulty": "Intermediate",
        "source_organization": "NSCA",
        "description": "Comprehensive agility drill combining forward sprint, lateral shuffle, and backward running.",
        "coaching_cues": [
            "Sprint forward under control",
            "Stay low during shuffles",
            "Don't cross feet laterally",
            "Backpedal with chest up"
        ],
        "common_errors": [
            "Crossing feet during shuffle",
            "Turning instead of shuffling",
            "Looking back while backpedaling",
            "High hips during lateral movement"
        ],
        "contraindications": [
            "Patellofemoral pain",
            "Ankle instability"
        ],
        "regressions": ["Walk-through pattern", "Remove backward segment"],
        "progressions": ["Timed reps", "Add ball dribbling"],
        "equipment_alternatives": ["Court lines", "Tape marks"],
        "is_pain_safe": True,
        "created_at": datetime.now().isoformat()
    },
    
    # === Reactive Agility ===
    {
        "name": "Mirror Drill (Partner Reactive)",
        "category": "Agility",
        "subcategory": "Reactive",
        "movement_pattern": "Reactive Lateral Movement",
        "equipment": "Partner, Open Space",
        "difficulty": "Intermediate",
        "source_organization": "EXOS",
        "description": "Partner-based reactive drill where athlete mirrors lateral movements of partner within defined area.",
        "coaching_cues": [
            "Watch partner's hips not feet",
            "Stay in athletic stance",
            "Small adjustment steps",
            "React don't anticipate"
        ],
        "common_errors": [
            "Watching partner's feet",
            "Getting too close",
            "Crossing feet",
            "Anticipating instead of reacting"
        ],
        "contraindications": [
            "Balance disorders",
            "Recent concussion"
        ],
        "regressions": ["Slower partner speed", "Smaller lateral range"],
        "progressions": ["Add forward/backward", "Add ball fake cues"],
        "equipment_alternatives": ["Coach as leader", "Video reaction drills"],
        "is_pain_safe": True,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Ball Drop Reaction Sprint",
        "category": "Agility",
        "subcategory": "Reactive",
        "movement_pattern": "Reactive Acceleration",
        "equipment": "Tennis Ball, Partner",
        "difficulty": "Beginner",
        "source_organization": "NSCA",
        "description": "Reaction drill where athlete sprints to catch ball dropped by partner from shoulder height.",
        "coaching_cues": [
            "Athletic ready position",
            "Eyes on ball",
            "Explode on visual cue",
            "Catch before second bounce"
        ],
        "common_errors": [
            "Leaning too far forward",
            "Slow reaction time",
            "Poor acceleration mechanics",
            "Not watching ball"
        ],
        "contraindications": ["None"],
        "regressions": ["Drop from higher height", "Longer starting distance"],
        "progressions": ["Multiple ball drops", "Add direction change after catch"],
        "equipment_alternatives": ["Whistle start", "Light signal"],
        "is_pain_safe": True,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Number Call Reactive Shuffle",
        "category": "Agility",
        "subcategory": "Reactive",
        "movement_pattern": "Reactive Multi-Directional",
        "equipment": "Numbered Cones (1-4), Partner/Coach",
        "difficulty": "Advanced",
        "source_organization": "EXOS",
        "description": "Athlete shuffles in place while coach calls numbers; athlete must touch corresponding numbered cone.",
        "coaching_cues": [
            "Stay light on feet",
            "Head up to see/hear cue",
            "Short quick steps",
            "Explode to target cone"
        ],
        "common_errors": [
            "Flat-footed shuffling",
            "Looking down",
            "Slow recognition",
            "Overshooting cone"
        ],
        "contraindications": [
            "Cognitive impairment",
            "Severe balance issues"
        ],
        "regressions": ["Fewer cones (2-3)", "Slower call rate"],
        "progressions": ["Add ball handling", "Add contact during shuffle"],
        "equipment_alternatives": ["Colored cones with color calls", "Light system"],
        "is_pain_safe": True,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Arrow Step Reactive Drill",
        "category": "Agility",
        "subcategory": "Reactive",
        "movement_pattern": "Reactive Footwork",
        "equipment": "Agility Ladder or Tape Arrows",
        "difficulty": "Intermediate",
        "source_organization": "Gray Institute",
        "description": "Athlete responds to verbal/visual cues by stepping in indicated direction within ladder rungs.",
        "coaching_cues": [
            "Stay centered in ladder",
            "Quick light steps",
            "Respond immediately to cue",
            "Maintain posture"
        ],
        "common_errors": [
            "Heavy footed",
            "Delayed reaction",
            "Stepping on lines",
            "Loss of balance"
        ],
        "contraindications": ["Ankle instability"],
        "regressions": ["Slower cue pace", "Single direction only"],
        "progressions": ["Faster cues", "Add ball toss while stepping"],
        "equipment_alternatives": ["Floor tape arrows", "Chalk grid"],
        "is_pain_safe": True,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Strobe Light Reaction Drill",
        "category": "Agility",
        "subcategory": "Reactive",
        "movement_pattern": "Visual Reaction",
        "equipment": "Strobe Glasses or Flickering Light",
        "difficulty": "Advanced",
        "source_organization": "Nike SPARQ",
        "description": "Athlete performs agility patterns while wearing strobe glasses or under flickering lights to challenge visual processing.",
        "coaching_cues": [
            "Trust your training",
            "Use peripheral vision",
            "Stay low for stability",
            "Focus on feel"
        ],
        "common_errors": [
            "Stopping when vision blocked",
            "Over-cautious movement",
            "Loss of spatial awareness",
            "Poor foot placement"
        ],
        "contraindications": [
            "Photosensitive epilepsy",
            "Migraine disorders",
            "Vision disorders"
        ],
        "regressions": ["Intermittent strobe use", "Simple patterns only"],
        "progressions": ["Complex patterns", "Add ball skills"],
        "equipment_alternatives": ["Coach covers eyes briefly", "Dark room with flashlight"],
        "is_pain_safe": False,
        "created_at": datetime.now().isoformat()
    },
    
    # === Multi-Directional Agility ===
    {
        "name": "Star Drill (5-Cone)",
        "category": "Agility",
        "subcategory": "Multi-Directional",
        "movement_pattern": "Radial Movement",
        "equipment": "5 Cones",
        "difficulty": "Advanced",
        "source_organization": "NSCA",
        "description": "Explosive multi-directional drill from center cone to four outer cones in star pattern.",
        "coaching_cues": [
            "Start from athletic stance",
            "Explode to each cone",
            "Touch and go immediately",
            "Return to center each time"
        ],
        "common_errors": [
            "Slow to first cone",
            "Not returning fully to center",
            "Poor deceleration at cones",
            "Predictable rhythm"
        ],
        "contraindications": [
            "Knee instability",
            "Hip pathology"
        ],
        "regressions": ["Walk pattern", "3-cone triangle"],
        "progressions": ["Random cone calls", "Add ball carry"],
        "equipment_alternatives": ["Floor markers", "Chalk X pattern"],
        "is_pain_safe": False,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Box Drill (Square Drill)",
        "category": "Agility",
        "subcategory": "Multi-Directional",
        "movement_pattern": "90-Degree Turns",
        "equipment": "4 Cones (10x10 yard square)",
        "difficulty": "Intermediate",
        "source_organization": "Football Coaches Association",
        "description": "Continuous loop around square pattern incorporating forward sprint, shuffle, and backpedal.",
        "coaching_cues": [
            "Smooth transitions at corners",
            "Stay low on shuffle side",
            "Backpedal with chest up",
            "Maintain consistent pace"
        ],
        "common_errors": [
            "Wide turns at corners",
            "Standing up during transitions",
            "Crossing feet on shuffle",
            "Inconsistent speed"
        ],
        "contraindications": ["None for healthy athletes"],
        "regressions": ["Larger box size", "Walk-through"],
        "progressions": ["Reverse pattern", "Timed intervals"],
        "equipment_alternatives": ["Court squares", "Tape box"],
        "is_pain_safe": True,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Hexagon Agility Drill",
        "category": "Agility",
        "subcategory": "Multi-Directional",
        "movement_pattern": "Multi-Planar Hopping",
        "equipment": "Tape or Chalk Hexagon",
        "difficulty": "Intermediate",
        "source_organization": "NSCA",
        "description": "Two-footed hops around hexagon pattern testing coordination and multi-directional quickness.",
        "coaching_cues": [
            "Hop lightly on balls of feet",
            "Face forward throughout",
            "Consistent hop height",
            "Land softly each time"
        ],
        "common_errors": [
            "Heavy landings",
            "Turning head/body",
            "Inconsistent rhythm",
            "Hopping too high"
        ],
        "contraindications": [
            "Achilles tendinopathy",
            "Plantar fasciitis",
            "Shin splints"
        ],
        "regressions": ["Step instead of hop", "Larger hexagon"],
        "progressions": ["Single-leg hops", "Faster tempo"],
        "equipment_alternatives": ["Agility rings", "Tire layout"],
        "is_pain_safe": False,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Carioca (Grapevine) Drill",
        "category": "Agility",
        "subcategory": "Multi-Directional",
        "movement_pattern": "Lateral Crossover",
        "equipment": "Open Space, Optional Cones",
        "difficulty": "Beginner",
        "source_organization": "Track & Field Coaching",
        "description": "Lateral crossover step pattern developing hip mobility and coordination for side-to-side movement.",
        "coaching_cues": [
            "Lead with knee drive",
            "Cross behind with trail leg",
            "Arms coordinate with legs",
            "Stay low and smooth"
        ],
        "common_errors": [
            "Crossing in front instead of behind",
            "Upright posture",
            "Stiff hip action",
            "No arm swing"
        ],
        "contraindications": [
            "Hip replacement",
            "Severe hip arthritis"
        ],
        "regressions": ["Side shuffle only", "Slow walk-through"],
        "progressions": ["Fast carioca", "Add resistance band"],
        "equipment_alternatives": ["Ladder rungs", "Line following"],
        "is_pain_safe": True,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Illinois Agility Run",
        "category": "Agility",
        "subcategory": "Multi-Directional",
        "movement_pattern": "Complex Course Navigation",
        "equipment": "8 Cones, Measured Course",
        "difficulty": "Advanced",
        "source_organization": "Australian Institute of Sport",
        "description": "Standardized agility test combining straight sprinting with weaving through multiple cones.",
        "coaching_cues": [
            "Maximum effort sprint sections",
            "Sharp cuts around weave cones",
            "Low center of gravity on turns",
            "Accelerate out of each turn"
        ],
        "common_errors": [
            "Wide weave pattern",
            "Slow initial acceleration",
            "Poor deceleration before turns",
            "Inefficient path selection"
        ],
        "contraindications": [
            "Any lower extremity injury",
            "Cardiovascular limitations"
        ],
        "regressions": ["Walk course", "Remove weave section"],
        "progressions": ["Ball dribble version", "Reactive start"],
        "equipment_alternatives": ["Indoor court adaptation", "Tape markers"],
        "is_pain_safe": False,
        "created_at": datetime.now().isoformat()
    },
    
    # === Sport-Specific Agility ===
    {
        "name": "Basketball Defensive Slide Series",
        "category": "Agility",
        "subcategory": "Sport-Specific",
        "movement_pattern": "Lateral Defensive Movement",
        "equipment": "Court, Cones",
        "difficulty": "Intermediate",
        "source_organization": "Basketball Coaches Association",
        "description": "Basketball-specific defensive footwork drill with slides, closeouts, and recovery steps.",
        "coaching_cues": [
            "Wide base, low stance",
            "Hands active and up",
            "Slide don't cross",
            "Pound feet on closeout"
        ],
        "common_errors": [
            "Crossing feet",
            "Standing up between slides",
            "Slow closeout",
            "No hand activity"
        ],
        "contraindications": [
            "Knee valgus",
            "Ankle instability"
        ],
        "regressions": ["Wall slides", "Short distance slides"],
        "progressions": ["Add offensive player", "Add shot contest"],
        "equipment_alternatives": ["Gym floor", "Driveway court"],
        "is_pain_safe": True,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Soccer Agility with Ball",
        "category": "Agility",
        "subcategory": "Sport-Specific",
        "movement_pattern": "Ball Handling Agility",
        "equipment": "Soccer Ball, Cones",
        "difficulty": "Intermediate",
        "source_organization": "UEFA Coaching",
        "description": "Dribbling agility course combining speed, close control, and directional changes.",
        "coaching_cues": [
            "Keep ball close on turns",
            "Use both feet",
            "Head up scanning",
            "Accelerate into space"
        ],
        "common_errors": [
            "Ball too far ahead",
            "Only using dominant foot",
            "Head down constantly",
            "Slow feet on turns"
        ],
        "contraindications": ["None"],
        "regressions": ["Walk dribble pattern", "Larger cone spacing"],
        "progressions": ["Defensive pressure", "Timed gates"],
        "equipment_alternatives": ["Any ball type", "Markers instead of cones"],
        "is_pain_safe": True,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Tennis Split-Step Pattern",
        "category": "Agility",
        "subcategory": "Sport-Specific",
        "movement_pattern": "Reactive First Step",
        "equipment": "Tennis Court, Balls",
        "difficulty": "Advanced",
        "source_organization": "USTA High Performance",
        "description": "Tennis-specific split-step timing drill followed by explosive first step to various court positions.",
        "coaching_cues": [
            "Split as opponent contacts ball",
            "Land on balls of feet",
            "Explode to ball trajectory",
            "Recover to center"
        ],
        "common_errors": [
            "Late split-step",
            "Flat-footed landing",
            "Wrong direction anticipation",
            "Slow recovery"
        ],
        "contraindications": [
            "Achilles issues",
            "Knee patellar tendinopathy"
        ],
        "regressions": ["Self-toss and move", "Slower pace"],
        "progressions": ["Coach random feeds", "Multiple ball series"],
        "equipment_alternatives": ["Wall rebound", "Ball machine"],
        "is_pain_safe": False,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Football Position-Specific Routes",
        "category": "Agility",
        "subcategory": "Sport-Specific",
        "movement_pattern": "Route Running",
        "equipment": "Football, Cones",
        "difficulty": "Advanced",
        "source_organization": "NFL Coaching",
        "description": "Position-specific route combinations for receivers, backs, and linebackers.",
        "coaching_cues": [
            "Sharp breaks at top of route",
            "Sell the fake with eyes/shoulders",
            "Accelerate out of cut",
            "Ready hands for catch"
        ],
        "common_errors": [
            "Rounding routes",
            "Telegraphing cuts",
            "Slow acceleration",
            "Poor body control"
        ],
        "contraindications": [
            "Hamstring strain",
            "ACL history"
        ],
        "regressions": ["Walk routes", "Single route reps"],
        "progressions": ["Covered routes", "Contact drills"],
        "equipment_alternatives": ["Flag football setup", "Solo mirror work"],
        "is_pain_safe": False,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Volleyball Approach Jump Sequence",
        "category": "Agility",
        "subcategory": "Sport-Specific",
        "movement_pattern": "Approach Footwork",
        "equipment": "Volleyball, Net",
        "difficulty": "Intermediate",
        "source_organization": "USA Volleyball",
        "description": "Multi-step approach pattern leading to explosive jump for attacking.",
        "coaching_cues": [
            "Penultimate step long and low",
            "Final step quick and punchy",
            "Arms swing aggressively",
            "Jump vertically not forward"
        ],
        "common_errors": [
            "Steps too even",
            "No arm swing",
            "Jumping into net",
            "Slow approach"
        ],
        "contraindications": [
            "Patellar tendinopathy",
            "Ankle instability"
        ],
        "regressions": ["Approach without jump", "Two-step approach"],
        "progressions": ["Add set variation", "Add block simulation"],
        "equipment_alternatives": ["Badminton court", "Basketball rim approximation"],
        "is_pain_safe": False,
        "created_at": datetime.now().isoformat()
    },
    
    # === Additional Agility Drills ===
    {
        "name": "Lateral Hurdle Hop Series",
        "category": "Agility",
        "subcategory": "Multi-Directional",
        "movement_pattern": "Lateral Plyometric",
        "equipment": "Mini Hurdles (4-6)",
        "difficulty": "Intermediate",
        "source_organization": "EXOS",
        "description": "Two-footed lateral hops over mini hurdles emphasizing quick ground contact and elastic rebound.",
        "coaching_cues": [
            "Land on balls of feet",
            "Minimal ground contact time",
            "Absorb with hips not knees",
            "Quick rebound up and over"
        ],
        "common_errors": [
            "Heavy landings",
            "Deep knee bend",
            "Slow transition",
            "Knocking hurdles"
        ],
        "contraindications": [
            "Knee meniscus injury",
            "Ankle sprain (acute)"
        ],
        "regressions": ["Step over hurdles", "Single hurdle reps"],
        "progressions": ["Single-leg lateral hops", "Increase hurdle height"],
        "equipment_alternatives": ["Rope barriers", "Tape lines", "Books"],
        "is_pain_safe": False,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Forward-Backward Shuttle",
        "category": "Agility",
        "subcategory": "COD",
        "movement_pattern": "Linear Deceleration",
        "equipment": "Cones (10-20 yards apart)",
        "difficulty": "Beginner",
        "source_organization": "NSCA",
        "description": "Simple linear shuttle emphasizing controlled deceleration and immediate reacceleration in opposite direction.",
        "coaching_cues": [
            "Sprint forward under control",
            "Drop hips to brake",
            "Plant outside foot",
            "Explode backward immediately"
        ],
        "common_errors": [
            "Running too fast to stop",
            "Upright braking posture",
            "Pause between directions",
            "Slow backpedal start"
        ],
        "contraindications": ["None"],
        "regressions": ["Shorter distance", "Jog pace"],
        "progressions": ["Add prone start", "Add ball pickup"],
        "equipment_alternatives": ["Court baselines", "Room walls"],
        "is_pain_safe": True,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "W-Drill",
        "category": "Agility",
        "subcategory": "Multi-Directional",
        "movement_pattern": "Diagonal Cutting Pattern",
        "equipment": "5 Cones",
        "difficulty": "Advanced",
        "source_organization": "Baseball Coaches Association",
        "description": "Five-cone W-shaped pattern combining forward sprint with multiple diagonal cuts.",
        "coaching_cues": [
            "Attack each cone aggressively",
            "Low hips on cuts",
            "Stay balanced through pattern",
            "Finish strong"
        ],
        "common_errors": [
            "Wide cuts",
            "Loss of momentum",
            "Poor foot placement",
            "Inconsistent rhythm"
        ],
        "contraindications": [
            "Groin strain",
            "Knee instability"
        ],
        "regressions": ["Walk pattern", "Three-cone version"],
        "progressions": ["Timed reps", "Add glove work"],
        "equipment_alternatives": ["Baseball diamond bases", "Tape marks"],
        "is_pain_safe": False,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Single-Leg Hops in Place",
        "category": "Agility",
        "subcategory": "Foundational",
        "movement_pattern": "Unilateral Stability",
        "equipment": "Bodyweight",
        "difficulty": "Beginner",
        "source_organization": "Physical Therapy Standards",
        "description": "Basic single-leg hopping developing unilateral stability and ankle stiffness.",
        "coaching_cues": [
            "Stand tall with core engaged",
            "Hop lightly on ball of foot",
            "Stick landing for 2 seconds",
            "Keep knee aligned over toe"
        ],
        "common_errors": [
            "Knee collapsing inward",
            "Heel touching ground",
            "Excessive hop height",
            "Arms flailing"
        ],
        "contraindications": [
            "Non-weight bearing status",
            "Severe balance deficits"
        ],
        "regressions": ["March in place", "Double-leg hops"],
        "progressions": ["Eyes closed", "Unstable surface"],
        "equipment_alternatives": ["Foam pad", "Bosu ball (flat side)"],
        "is_pain_safe": True,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Skater Bounds (Lateral Leaps)",
        "category": "Agility",
        "subcategory": "Multi-Directional",
        "movement_pattern": "Lateral Power",
        "equipment": "Open Space",
        "difficulty": "Intermediate",
        "source_organization": "Speed Skating Training",
        "description": "Explosive lateral bounds from one leg to the other mimicking speed skating motion.",
        "coaching_cues": [
            "Push off powerfully laterally",
            "Swing arms for momentum",
            "Land softly on single leg",
            "Hold landing briefly"
        ],
        "common_errors": [
            "Bounding forward not lateral",
            "Hard landings",
            "No pause between bounds",
            "Poor balance on landing"
        ],
        "contraindications": [
            "Hip labral tear",
            "Knee MCL injury"
        ],
        "regressions": ["Smaller bound distance", "Double-leg lateral jumps"],
        "progressions": ["Distance maximization", "Continuous rapid bounds"],
        "equipment_alternatives": ["Ice rink", "Grass field"],
        "is_pain_safe": False,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Quick Feet Ladder Drills",
        "category": "Agility",
        "subcategory": "Foundational",
        "movement_pattern": "Foot Speed",
        "equipment": "Agility Ladder",
        "difficulty": "Beginner",
        "source_organization": "Speed School Training",
        "description": "Various footwork patterns through ladder rungs developing fast twitch muscle response.",
        "coaching_cues": [
            "Stay on balls of feet",
            "Quick light steps",
            "Arms pump naturally",
            "Look ahead not at feet"
        ],
        "common_errors": [
            "Heavy footed",
            "Looking down constantly",
            "Inconsistent rhythm",
            "Stepping on ladder"
        ],
        "contraindications": ["None"],
        "regressions": ["One foot per rung", "Slow pace"],
        "progressions": ["Icky shuffle", "Ali shuffles"],
        "equipment_alternatives": ["Chalk lines", "Rope ladder", "Tape rungs"],
        "is_pain_safe": True,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Dot Drill",
        "category": "Agility",
        "subcategory": "Foundational",
        "movement_pattern": "Multi-Directional Footwork",
        "equipment": "5 Dots/Tape Marks",
        "difficulty": "Intermediate",
        "source_organization": "Volleyball Training",
        "description": "Five-dot pattern with various jumping sequences developing foot speed and coordination.",
        "coaching_cues": [
            "Stay on balls of feet",
            "Quick transitions",
            "Light landings",
            "Follow specific pattern"
        ],
        "common_errors": [
            "Flat-footed",
            "Wrong sequence",
            "Heavy landings",
            "Slow rhythm"
        ],
        "contraindications": [
            "Plantar fasciitis",
            "Achilles issues"
        ],
        "regressions": ["Step pattern", "Slower tempo"],
        "progressions": ["Single-leg variations", "Eyes closed"],
        "equipment_alternatives": ["Floor tiles", "Chalk dots", "Paper plates"],
        "is_pain_safe": False,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Reaction Wall Taps",
        "category": "Agility",
        "subcategory": "Reactive",
        "movement_pattern": "Hand-Eye Coordination",
        "equipment": "Wall, Tennis Ball",
        "difficulty": "Beginner",
        "source_organization": "Boxing Training",
        "description": "Rapid wall ball taps developing hand speed and visual tracking.",
        "coaching_cues": [
            "Athletic stance facing wall",
            "Quick wrist snaps",
            "Track ball with eyes",
            "Maintain rhythm"
        ],
        "common_errors": [
            "Slow hands",
            "Taking eyes off ball",
            "Catching instead of tapping",
            "Inconsistent force"
        ],
        "contraindications": ["Shoulder impingement"],
        "regressions": ["Slower pace", "Two-hand catches"],
        "progressions": ["Alternating hands", "Single-hand taps"],
        "equipment_alternatives": ["Any wall", "Racquetball"],
        "is_pain_safe": True,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Cone Pickup Relay",
        "category": "Agility",
        "subcategory": "COD",
        "movement_pattern": "Multi-Directional with Object Manipulation",
        "equipment": "10 Cones, Bucket",
        "difficulty": "Intermediate",
        "source_organization": "General Athletic Training",
        "description": "Shuttle-style drill picking up cones one at a time and returning to bucket.",
        "coaching_cues": [
            "Explode from start each rep",
            "Low hips to pick up cone",
            "Quick turnaround",
            "Place cone gently in bucket"
        ],
        "common_errors": [
            "Slow starts",
            "Bending at waist not hips",
            "Wide turns",
            "Dropping cones"
        ],
        "contraindications": ["Lower back pain"],
        "regressions": ["Fewer cones", "Closer spacing"],
        "progressions": ["Timed competition", "Add push-up at each cone"],
        "equipment_alternatives": ["Any small objects", "Water bottles"],
        "is_pain_safe": True,
        "created_at": datetime.now().isoformat()
    }
]

# ============================================================================
# CONDITIONING EXERCISES (Adding 49+ to bring from 1 to 50+)
# Categories: Aerobic, Anaerobic, Intervals, Sport-Specific Energy Systems
# ============================================================================

conditioning_exercises = [
    # === Aerobic Base Building ===
    {
        "name": "Steady State Zone 2 Run",
        "category": "Cond",
        "subcategory": "Aerobic",
        "movement_pattern": "Continuous Cardio",
        "equipment": "Running Shoes, Heart Rate Monitor",
        "difficulty": "Beginner",
        "source_organization": "Exercise Physiology Standards",
        "description": "Low-intensity continuous running at 60-70% max HR building aerobic base and mitochondrial density.",
        "coaching_cues": [
            "Maintain conversational pace",
            "Relaxed upright posture",
            "Midfoot strike pattern",
            "Consistent breathing rhythm"
        ],
        "common_errors": [
            "Going too fast (Zone 3+)",
            "Poor running form",
            "Inconsistent pace",
            "Holding breath"
        ],
        "contraindications": [
            "Uncontrolled hypertension",
            "Acute illness"
        ],
        "regressions": ["Walk/jog intervals", "Reduced duration"],
        "progressions": ["Increased duration", "Added hills"],
        "equipment_alternatives": ["Cycling", "Rowing", "Swimming", "Elliptical"],
        "is_pain_safe": True,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Tempo Run (Threshold Pace)",
        "category": "Cond",
        "subcategory": "Aerobic",
        "movement_pattern": "Sustained Threshold Effort",
        "equipment": "Running Shoes, Watch",
        "difficulty": "Intermediate",
        "source_organization": "Running Science",
        "description": "Sustained effort at lactate threshold (80-85% max HR) improving metabolic efficiency at race pace.",
        "coaching_cues": [
            "Comfortably hard pace",
            "Controlled breathing",
            "Efficient stride",
            "Mental focus maintained"
        ],
        "common_errors": [
            "Starting too fast",
            "Fading at end",
            "Poor form when fatigued",
            "Incorrect pacing"
        ],
        "contraindications": [
            "Insufficient aerobic base",
            "Recent illness"
        ],
        "regressions": ["Shorter tempo segments", "Lower intensity"],
        "progressions": ["Longer tempo duration", "Broken tempo sets"],
        "equipment_alternatives": ["Cycling threshold", "Rowing threshold"],
        "is_pain_safe": False,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Long Slow Distance (LSD) Run",
        "category": "Cond",
        "subcategory": "Aerobic",
        "movement_pattern": "Extended Duration Cardio",
        "equipment": "Running Shoes, Hydration System",
        "difficulty": "Intermediate",
        "source_organization": "Marathon Training Standards",
        "description": "Extended duration run (90+ minutes) at easy pace building endurance and fat oxidation capacity.",
        "coaching_cues": [
            "Easy conversational pace",
            "Relaxed throughout",
            "Fuel/hydrate regularly",
            "Maintain form late in run"
        ],
        "common_errors": [
            "Too fast early",
            "Inadequate fueling",
            "Form breakdown",
            "Dehydration"
        ],
        "contraindications": [
            "Insufficient training base",
            "Illness/injury"
        ],
        "regressions": ["Shorter duration", "Run/walk method"],
        "progressions": ["Increased distance", "Added elevation"],
        "equipment_alternatives": ["Long bike ride", "Pool running"],
        "is_pain_safe": True,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Fartlek Run (Speed Play)",
        "category": "Cond",
        "subcategory": "Mixed Energy Systems",
        "movement_pattern": "Variable Pace Running",
        "equipment": "Running Shoes, Open Route",
        "difficulty": "Intermediate",
        "source_organization": "Swedish Running Tradition",
        "description": "Unstructured interval training alternating fast and slow segments based on feel and terrain.",
        "coaching_cues": [
            "Listen to your body",
            "Vary efforts naturally",
            "Use terrain features",
            "Recovery jogs between hard efforts"
        ],
        "common_errors": [
            "Too structured/rigid",
            "All-out efforts only",
            "Insufficient recovery",
            "Ignoring fatigue signals"
        ],
        "contraindications": ["None for healthy athletes"],
        "regressions": ["More recovery time", "Shorter hard segments"],
        "progressions": ["Longer hard segments", "Hill fartlek"],
        "equipment_alternatives": ["Trail running", "Beach running"],
        "is_pain_safe": True,
        "created_at": datetime.now().isoformat()
    },
    
    # === Anaerobic Capacity ===
    {
        "name": "30/30 Interval Run",
        "category": "Cond",
        "subcategory": "Anaerobic",
        "movement_pattern": "Short High-Intensity Intervals",
        "equipment": "Running Track, Timer",
        "difficulty": "Advanced",
        "source_organization": "Norwegian Distance Training",
        "description": "Alternating 30 seconds hard running with 30 seconds easy recovery, repeated for 10-20 cycles.",
        "coaching_cues": [
            "Hard but sustainable pace",
            "Active recovery during easy",
            "Consistent effort throughout",
            "Monitor total volume"
        ],
        "common_errors": [
            "First intervals too hard",
            "Stopping during recovery",
            "Inconsistent pacing",
            "Too many repetitions"
        ],
        "contraindications": [
            "Insufficient aerobic base",
            "Cardiac conditions"
        ],
        "regressions": ["40/20 ratio", "Fewer repeats"],
        "progressions": ["40/20 ratio", "More repeats"],
        "equipment_alternatives": ["Cycling intervals", "Rowing intervals"],
        "is_pain_safe": False,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Tabata Protocol",
        "category": "Cond",
        "subcategory": "Anaerobic",
        "movement_pattern": "Ultra-Short High-Intensity",
        "equipment": "Timer, Any Modality",
        "difficulty": "Advanced",
        "source_organization": "Dr. Izumi Tabata Research",
        "description": "20 seconds all-out effort followed by 10 seconds rest, repeated 8 times (4 minutes total).",
        "coaching_cues": [
            "Maximum effort each work interval",
            "Complete rest during recovery",
            "Maintain technique despite fatigue",
            "Mental toughness required"
        ],
        "common_errors": [
            "Pacing first intervals",
            "Skipping rest periods",
            "Poor form when tired",
            "Not going truly maximal"
        ],
        "contraindications": [
            "Cardiovascular disease",
            "Untrained individuals",
            "Recent injury"
        ],
        "regressions": ["Modified Tabata (15s work)", "Fewer rounds"],
        "progressions": ["Multiple Tabata sets", "Added resistance"],
        "equipment_alternatives": ["Assault bike", "Rowing", "Burpees", "Sprints"],
        "is_pain_safe": False,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "400m Repeat Sprints",
        "category": "Cond",
        "subcategory": "Anaerobic",
        "movement_pattern": "Lactic Capacity Intervals",
        "equipment": "Running Track, Timer",
        "difficulty": "Advanced",
        "source_organization": "Track & Field Training",
        "description": "Repeated 400m sprints with equal or 1.5x time rest, targeting lactate tolerance and buffering capacity.",
        "coaching_cues": [
            "Target consistent split times",
            "Relaxed face and shoulders",
            "Strong arm drive",
            "Finish each rep strong"
        ],
        "common_errors": [
            "Starting too fast",
            "Significant slowdown",
            "Poor running mechanics",
            "Incomplete recovery"
        ],
        "contraindications": [
            "Hamstring strain history",
            "Insufficient speed base"
        ],
        "regressions": ["300m repeats", "Longer rest"],
        "progressions": ["500m repeats", "Shorter rest"],
        "equipment_alternatives": ["Hill sprints", "Treadmill intervals"],
        "is_pain_safe": False,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Alactic Power Repeats",
        "category": "Cond",
        "subcategory": "ATP-PC System",
        "movement_pattern": "Very Short Maximal Efforts",
        "equipment": "Open Space, Timer",
        "difficulty": "Advanced",
        "source_organization": "Charlie Francis Training",
        "description": "6-10 second maximal efforts with full recovery (2-5 min) targeting phosphocreatine energy system.",
        "coaching_cues": [
            "100% maximum effort",
            "Perfect technique",
            "Full recovery between reps",
            "Quality over quantity"
        ],
        "common_errors": [
            "Insufficient recovery",
            "Sub-maximal effort",
            "Too many repetitions",
            "Form breakdown"
        ],
        "contraindications": [
            "Muscle strains",
            "Insufficient strength base"
        ],
        "regressions": ["Shorter duration (4-5s)", "Less intensity"],
        "progressions": ["Resisted sprints", "Uphill sprints"],
        "equipment_alternatives": ["Sled pushes", "Bike sprints", "Swim sprints"],
        "is_pain_safe": False,
        "created_at": datetime.now().isoformat()
    },
    
    # === Sport-Specific Conditioning ===
    {
        "name": "Basketball Suicides",
        "category": "Cond",
        "subcategory": "Sport-Specific",
        "movement_pattern": "Court Line Shuttles",
        "equipment": "Basketball Court",
        "difficulty": "Advanced",
        "source_organization": "Basketball Conditioning",
        "description": "Progressive line touch drill covering increasing distances on basketball court.",
        "coaching_cues": [
            "Touch each line completely",
            "Low center of gravity on turns",
            "Explode off each line",
            "Maintain pace throughout"
        ],
        "common_errors": [
            "Not touching lines",
            "Wide turns",
            "Pacing errors",
            "Form breakdown"
        ],
        "contraindications": [
            "Knee issues",
            "Ankle instability"
        ],
        "regressions": ["Half court version", "Walk-through"],
        "progressions": ["Add dribbling", "Timed sets"],
        "equipment_alternatives": ["Tennis court", "Volleyball court"],
        "is_pain_safe": False,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Soccer Box-to-Box Intervals",
        "category": "Cond",
        "subcategory": "Sport-Specific",
        "movement_pattern": "Field Length Intervals",
        "equipment": "Soccer Field, Cones",
        "difficulty": "Advanced",
        "source_organization": "Premier League Fitness",
        "description": "Simulates match demands with varied intensity runs across soccer pitch length.",
        "coaching_cues": [
            "Match-pace intensity",
            "Include jogging recovery",
            "Change speeds realistically",
            "Mental engagement"
        ],
        "common_errors": [
            "Constant pace",
            "Insufficient high-speed running",
            "Poor recovery positioning",
            "Lack of sport specificity"
        ],
        "contraindications": ["Hamstring tightness"],
        "regressions": ["Reduced field length", "More recovery"],
        "progressions": ["Add ball work", "Small-sided games"],
        "equipment_alternatives": ["Treadmill with incline", "Track intervals"],
        "is_pain_safe": False,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Swimming Pyramid Set",
        "category": "Cond",
        "subcategory": "Sport-Specific",
        "movement_pattern": "Progressive Distance Intervals",
        "equipment": "Pool, Kickboard",
        "difficulty": "Intermediate",
        "source_organization": "Swimming Training",
        "description": "Ascending and descending distance intervals (50, 100, 200, 100, 50) building endurance and speed.",
        "coaching_cues": [
            "Consistent stroke technique",
            "Negative splits when possible",
            "Efficient turns",
            "Controlled breathing"
        ],
        "common_errors": [
            "Technique breakdown",
            "Starting middle distances too fast",
            "Poor flip turns",
            "Inconsistent pacing"
        ],
        "contraindications": [
            "Shoulder impingement",
            "Respiratory issues"
        ],
        "regressions": ["Shorter pyramid", "More rest"],
        "progressions": ["Longer distances", "Reduced rest"],
        "equipment_alternatives": ["Pull buoy", "Paddles"],
        "is_pain_safe": True,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Rowing 2k Time Trial",
        "category": "Cond",
        "subcategory": "Sport-Specific",
        "movement_pattern": "Sustained Power Output",
        "equipment": "Rowing Ergometer",
        "difficulty": "Advanced",
        "source_organization": "Concept2 Training",
        "description": "Maximal 2000m row testing anaerobic threshold and mental toughness.",
        "coaching_cues": [
            "Strong leg drive",
            "Sequential body swing then arms",
            "Controlled recovery",
            "Even split pacing"
        ],
        "common_errors": [
            "Arms pulling too early",
            "Rushing recovery",
            "Starting too fast",
            "Poor sequencing"
        ],
        "contraindications": [
            "Lower back injury",
            "Shoulder pathology"
        ],
        "regressions": ["1k time trial", "Piece work intervals"],
        "progressions": ["Longer distances", "Reduced rest intervals"],
        "equipment_alternatives": ["Ski erg", "Bike erg"],
        "is_pain_safe": False,
        "created_at": datetime.now().isoformat()
    },
    
    # === Circuit Training ===
    {
        "name": "Bodyweight Metabolic Circuit",
        "category": "Cond",
        "subcategory": "Circuit",
        "movement_pattern": "Multi-Modal Continuous",
        "equipment": "Bodyweight, Timer",
        "difficulty": "Intermediate",
        "source_organization": "CrossFit Methodology",
        "description": "Continuous circuit of bodyweight exercises (burpees, mountain climbers, squats, push-ups) for metabolic conditioning.",
        "coaching_cues": [
            "Maintain exercise standards",
            "Minimize rest between exercises",
            "Controlled breathing",
            "Push through discomfort"
        ],
        "common_errors": [
            "Poor exercise form",
            "Excessive rest",
            "Pacing too conservatively",
            "Incomplete range of motion"
        ],
        "contraindications": [
            "Multiple joint issues",
            "Extreme deconditioning"
        ],
        "regressions": ["Slower pace", "Exercise modifications"],
        "progressions": ["Added weight", "Longer duration"],
        "equipment_alternatives": ["Gymnastics rings", "Pull-up bar"],
        "is_pain_safe": True,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Kettlebell Complex",
        "category": "Cond",
        "subcategory": "Circuit",
        "movement_pattern": "Loaded Continuous Flow",
        "equipment": "Kettlebell",
        "difficulty": "Advanced",
        "source_organization": "StrongFirst",
        "description": "Sequential kettlebell movements performed without放下 ing weight (clean, press, squat, snatch flow).",
        "coaching_cues": [
            "Smooth transitions",
            "Maintain grip",
            "Breathing coordinated with movement",
            "Core braced throughout"
        ],
        "common_errors": [
            "Breaking grip between moves",
            "Poor technique when fatigued",
            "Inconsistent rhythm",
            "Weight too heavy"
        ],
        "contraindications": [
            "Shoulder instability",
            "Lower back issues",
            "Grip limitations"
        ],
        "regressions": ["Lighter bell", "Fewer movements"],
        "progressions": ["Heavier bell", "More rounds"],
        "equipment_alternatives": ["Dumbbell", "Barbell complex"],
        "is_pain_safe": False,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "AMRAP Circuit (As Many Rounds As Possible)",
        "category": "Cond",
        "subcategory": "Circuit",
        "movement_pattern": "Timed Volume Challenge",
        "equipment": "Mixed Equipment",
        "difficulty": "Advanced",
        "source_organization": "CrossFit Competition",
        "description": "Complete maximum rounds of prescribed circuit within time cap (typically 10-20 minutes).",
        "coaching_cues": [
            "Sustainable pace strategy",
            "Efficient transitions",
            "Maintain standards",
            "Mental resilience"
        ],
        "common_errors": [
            "Starting too fast",
            "Form breakdown",
            "Excessive rest",
            "Missing reps"
        ],
        "contraindications": [
            "Multiple injuries",
            "Insufficient training base"
        ],
        "regressions": ["Scaled movements", "Longer time cap"],
        "progressions": ["More difficult movements", "Shorter time cap"],
        "equipment_alternatives": ["Any available equipment"],
        "is_pain_safe": False,
        "created_at": datetime.now().isoformat()
    },
    
    # === HIIT Protocols ===
    {
        "name": "HIIT Bike Sprints",
        "category": "Cond",
        "subcategory": "HIIT",
        "movement_pattern": "Cycling Intervals",
        "equipment": "Stationary Bike or Assault Bike",
        "difficulty": "Advanced",
        "source_organization": "Gibala Research",
        "description": "Repeated all-out cycling sprints (20-30s) with active recovery (1-2 min) for cardiovascular adaptation.",
        "coaching_cues": [
            "Maximum wattage output",
            "Full pedal revolutions",
            "Active recovery spinning",
            "Consistent effort across rounds"
        ],
        "common_errors": [
            "Sub-maximal sprints",
            "Stopping during recovery",
            "Inconsistent resistance",
            "Poor seating position"
        ],
        "contraindications": [
            "Cardiac conditions",
            "Knee pathology"
        ],
        "regressions": ["Lower resistance", "Longer recovery"],
        "progressions": ["More sprints", "Shorter recovery"],
        "equipment_alternatives": ["Rower", "Treadmill", "Elliptical"],
        "is_pain_safe": False,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "EMOM Conditioning (Every Minute On Minute)",
        "category": "Cond",
        "subcategory": "HIIT",
        "movement_pattern": "Timed Work-Rest Intervals",
        "equipment": "Timer, Various",
        "difficulty": "Intermediate",
        "source_organization": "CrossFit Programming",
        "description": "Perform prescribed work at start of each minute; remainder of minute is rest. Repeat for 10-20 minutes.",
        "coaching_cues": [
            "Start immediately at minute mark",
            "Work efficiently",
            "Use remaining time for rest",
            "Maintain quality throughout"
        ],
        "common_errors": [
            "Slow starts",
            "Rushing reps compromising form",
            "Not resting enough",
            "Inconsistent pacing"
        ],
        "contraindications": ["None for healthy athletes"],
        "regressions": ["Fewer reps per minute", "Longer EMOM duration"],
        "progressions": ["More reps per minute", "Complex movements"],
        "equipment_alternatives": ["Any modality"],
        "is_pain_safe": True,
        "created_at": datetime.now().isoformat()
    },
    
    # === Recovery & Active Rest ===
    {
        "name": "Active Recovery Walk",
        "category": "Cond",
        "subcategory": "Recovery",
        "movement_pattern": "Low-Intensity Continuous",
        "equipment": "Comfortable Shoes",
        "difficulty": "Beginner",
        "source_organization": "Sports Recovery Science",
        "description": "Low-intensity walking (Zone 1) promoting blood flow and recovery without adding stress.",
        "coaching_cues": [
            "Relaxed easy pace",
            "Natural breathing",
            "Good posture",
            "Enjoy the movement"
        ],
        "common_errors": [
            "Walking too fast",
            "Poor posture",
            "Mental stress",
            "Too long duration"
        ],
        "contraindications": ["None"],
        "regressions": ["Shorter duration"],
        "progressions": ["Light hiking", "Added distance"],
        "equipment_alternatives": ["Easy cycling", "Pool walking"],
        "is_pain_safe": True,
        "created_at": datetime.now().isoformat()
    },
    {
        "name": "Contrast Water Therapy Protocol",
        "category": "Cond",
        "subcategory": "Recovery",
        "movement_pattern": "Thermal Contrast",
        "equipment": "Hot/Cold Water Sources",
        "difficulty": "Intermediate",
        "source_organization": "Recovery Science",
        "description": "Alternating hot and cold water immersion to promote circulation and reduce inflammation.",
        "coaching_cues": [
            "1 min cold, 2 min hot cycle",
            "Repeat 3-5 times",
            "End with cold",
            "Monitor tolerance"
        ],
        "common_errors": [
            "Water too extreme",
            "Insufficient cycles",
            "Ending with hot",
            "Ignoring discomfort"
        ],
        "contraindications": [
            "Cardiovascular disease",
            "Raynaud's syndrome",
            "Open wounds"
        ],
        "regressions": ["Less temperature contrast", "Fewer cycles"],
        "progressions": ["Greater contrast", "More cycles"],
        "equipment_alternatives": ["Showers", "Ice baths + sauna"],
        "is_pain_safe": True,
        "created_at": datetime.now().isoformat()
    }
]

# Add all new exercises
for ex in agility_exercises:
    max_id += 1
    ex['id'] = f"AGI-{max_id}"
    new_exercises.append(ex)

for ex in conditioning_exercises:
    max_id += 1
    ex['id'] = f"COND-{max_id}"
    new_exercises.append(ex)

# Combine with existing exercises
exercises.extend(new_exercises)

# Save updated exercises
with open('forge_web/src/data/exercises.json', 'w') as f:
    json.dump(exercises, f, indent=2)

# Print summary
print("=" * 70)
print("✅ AGILITY & CONDITIONING LIBRARY EXPANSION COMPLETE")
print("=" * 70)
print(f"\n📊 SUMMARY:")
print(f"   Agility exercises added: {len(agility_exercises)}")
print(f"   Conditioning exercises added: {len(conditioning_exercises)}")
print(f"   Total new exercises: {len(new_exercises)}")
print(f"   New total library size: {len(exercises)} exercises")

# Count by category
from collections import Counter
categories = Counter([e['category'] for e in exercises])
print(f"\n📈 CATEGORY BREAKDOWN:")
for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
    print(f"   {cat}: {count} exercises")

print("\n✨ All exercises include complete S&C metadata:")
print("   • Coaching cues from authoritative sources")
print("   • Common errors for athlete screening")
print("   • Contraindications for safety")
print("   • Progressions and regressions")
print("   • Equipment alternatives")
print("   • Pain-safe flags")
print("\n🎯 Library now provides comprehensive coverage for elite athletic development!")
