#!/usr/bin/env python3
"""
FORGE EXERCISE LIBRARY - PHASE 1 METADATA ENRICHMENT
Adds critical missing metadata to all 299 exercises:
- Coaching cues (4 per exercise)
- Common faults (4 per exercise)  
- Contraindications (3 per exercise)
- Equipment alternatives (3 per exercise)
- Technical difficulty (1-10 scale)
- Training age minimum (months)
- Force vector classification
- Expanded sport tags
"""

import json
from src.forge.exercises_data import EXERCISES_DATA

# ============================================================================
# INTELLIGENT METADATA MAPS BY EXERCISE FAMILY
# ============================================================================

COACHING_CUES_DB = {
    "DLKD": [
        "Keep chest tall and core braced throughout movement",
        "Push through mid-foot, not toes or heels",
        "Knees track over toes, don't let them cave inward",
        "Control the descent, don't drop into the bottom",
        "Maintain neutral spine from start to finish",
        "Hip hinge first, then bend the knees",
        "Full depth: hip crease below knee cap",
        "Drive through floor explosively on ascent"
    ],
    "DLHD": [
        "Keep chest tall and core braced throughout movement",
        "Push through mid-foot, not toes or heels",
        "Knees track over toes, don't let them cave inward",
        "Control the descent, don't drop into the bottom",
        "Maintain neutral spine from start to finish",
        "Single-leg balance before initiating movement",
        "Full depth: hip crease below knee cap",
        "Drive through floor explosively on ascent"
    ],
    "SLKD": [
        "Keep chest tall and core braced throughout movement",
        "Push through mid-foot of working leg",
        "Knee tracks over toes on working leg",
        "Control the descent, don't drop into the bottom",
        "Maintain neutral spine from start to finish",
        "Hip hinge first, then bend the knee",
        "Full depth: hip crease below knee cap",
        "Drive through floor explosively on ascent"
    ],
    "ULPD": [
        "Pack shoulders down and back before initiating",
        "Keep elbows at 45-degree angle to torso",
        "Full range: bar touches upper chest",
        "Maintain tight core and glutes engaged",
        "Wrist stacked directly over elbow",
        "Control the eccentric for 2-3 seconds",
        "Press through full extension without locking out hard",
        "Shoulder blades move together on descent"
    ],
    "HPush": [
        "Pack shoulders down and back before initiating",
        "Keep elbows at 45-degree angle to torso",
        "Full range: hands touch ground/bench",
        "Maintain tight core and glutes engaged",
        "Hands stacked directly over shoulders",
        "Control the eccentric for 2-3 seconds",
        "Press through full extension without locking out hard",
        "Shoulder blades protract at top"
    ],
    "HNGE": [
        "Soft knees, push hips back to start",
        "Feel stretch in hamstrings, not lower back",
        "Maintain neutral spine throughout",
        "Bar stays close to body, almost touching",
        "Squeeze glutes hard at top position",
        "Don't hyperextend at the top",
        "Hips and shoulders rise together",
        "Lats engaged to keep bar path vertical"
    ],
    "HPull": [
        "Initiate with shoulder blade retraction",
        "Pull elbows back, not just hands",
        "Squeeze shoulder blades together at top",
        "Control the eccentric phase",
        "Keep core braced throughout",
        "Don't shrug shoulders toward ears",
        "Full stretch at bottom position",
        "Lead with elbows on pulling motion"
    ],
    "VPush": [
        "Pack shoulders down before pressing",
        "Core braced, ribs down",
        "Press straight overhead, not forward",
        "Full lockout without excessive lean",
        "Control the descent",
        "Head stays neutral, eyes forward",
        "Don't arch lower back excessively",
        "Breath out on press, in on descent"
    ],
    "VPull": [
        "Initiate with lat engagement",
        "Pull to upper chest, not behind neck",
        "Squeeze shoulder blades down and back",
        "Control the eccentric fully",
        "Don't use momentum or swinging",
        "Keep chest tall throughout",
        "Full stretch at top position",
        "Elbows drive down toward hips"
    ],
    "BRDG": [
        "Feet flat, drive through heels",
        "Posterior pelvic tilt at top position",
        "Ribs down, don't overextend lumbar spine",
        "Squeeze glutes, not lower back",
        "Hold top position for 2-second pause",
        "Chin tucked, eyes looking at knees",
        "Progressive tension from bottom to top",
        "Single-leg: keep pelvis level throughout"
    ],
    "CRCH": [
        "Core braced like preparing for a punch",
        "Posterior pelvic tilt, ribs down",
        "Neck long, chin slightly tucked",
        "Arms extended overhead or at chest",
        "Slow controlled tempo, no momentum",
        "Exhale fully at top of crunch",
        "Focus on rectus abdominis contraction",
        "Don't pull on neck with hands"
    ],
    "ROT": [
        "Pivot back foot on rotational movements",
        "Power comes from hip rotation, not arms",
        "Maintain athletic stance throughout",
        "Core tight, transfer force through trunk",
        "Eyes follow the movement pattern",
        "Control the deceleration phase",
        "Equal training on both sides",
        "Breathe out on exertion phase"
    ],
    "CRRY": [
        "Tall posture, don't lean toward load",
        "Core braced, ribs down",
        "Shoulders packed, not shrugged",
        "Small controlled steps",
        "Don't let load swing or rotate",
        "Grip tight throughout carry",
        "Neutral head position",
        "Purposeful ground contact with each step"
    ],
    "PLYO": [
        "Land softly like a ninja, absorb impact",
        "Quick ground contact, minimize time on floor",
        "Full triple extension on takeoff",
        "Arms coordinate with leg action",
        "Reset between reps for quality",
        "Land in athletic stance ready to move",
        "Progress height/distance gradually",
        "Focus on landing mechanics before intensity"
    ],
    "Landing": [
        "Land softly like a ninja, absorb impact",
        "Knees track over toes on landing",
        "Full foot contact, not just toes",
        "Hips back, athletic stance",
        "Quiet landing = good mechanics",
        "Reset between reps for quality",
        "Progress height gradually",
        "Focus on form before intensity"
    ],
    "SPRT": [
        "Forward lean on acceleration phase",
        "Drive knees high, punch arms",
        "Stay on balls of feet",
        "Relax face and upper body",
        "Breathe rhythmically, don't hold breath",
        "Progressive build-up in speed",
        "Quality over quantity on reps",
        "Full recovery between sprints"
    ],
    "Agility": [
        "Low center of gravity on direction changes",
        "Plant foot outside base of support",
        "Sharp cuts, not rounded turns",
        "Eyes up, scan the environment",
        "Decelerate before reaccelerating",
        "Use arms for balance and power",
        "Stay on balls of feet",
        "Simulate game-like intensity"
    ],
    "Ball": [
        "Track ball with eyes from release",
        "Position body behind ball trajectory",
        "Soft hands on catch",
        "Absorb impact through legs",
        "Quick transition to throw",
        "Proper grip for throw type",
        "Step toward target on throw",
        "Follow through completely"
    ],
    "MOBL": [
        "Move slowly through full range",
        "Breathe deeply, relax into positions",
        "No forcing or bouncing",
        "Focus on areas of restriction",
        "Active mobility preferred over passive",
        "Control end ranges with strength",
        "Smooth transitions between positions",
        "Mind-muscle connection throughout"
    ],
    "ACTV": [
        "Purposeful movement preparation",
        "Progressive intensity build-up",
        "Activate target muscle groups",
        "Dynamic stretching over static",
        "Movement-specific patterns",
        "Increase heart rate gradually",
        "Prime nervous system",
        "Sport-specific drills included"
    ],
    "Cond": [
        "Maintain consistent pace throughout",
        "Focus on breathing rhythm",
        "Proper form even when fatigued",
        "Stay mentally engaged",
        "Hydrate appropriately",
        "Monitor heart rate zones",
        "Cool down properly after",
        "Progress duration/intensity gradually"
    ],
    "RCVR": [
        "Gentle movement to increase blood flow",
        "Focus on relaxation and breathing",
        "Low intensity, conversational pace",
        "Address areas of tightness",
        "Parasympathetic activation",
        "Hydration and nutrition timing",
        "Sleep and stress management",
        "Listen to body signals"
    ],
    "ASMT": [
        "Baseline measurement conditions",
        "Consistent testing protocol",
        "Proper warm-up beforehand",
        "Maximal effort on test day",
        "Record all relevant metrics",
        "Compare to normative data",
        "Track progress over time",
        "Rest adequately between tests"
    ]
}

COMMON_FAULTS_DB = {
    "DLKD": [
        "Knee valgus (knees caving inward)",
        "Excessive forward lean or chest collapse",
        "Heels lifting off ground",
        "Incomplete depth (parallel or above)",
        "Lower back rounding at bottom",
        "Knees shooting forward past toes excessively",
        "Uneven weight distribution",
        "Holding breath during rep"
    ],
    "ULPD": [
        "Elbows flared out too wide",
        "Incomplete range of motion",
        "Arching lower back excessively",
        "Bar path not vertical",
        "Wrists bending backward",
        "Shoulder shrugging at top",
        "Bouncing bar off chest",
        "Head lifting off bench"
    ],
    "HNGE": [
        "Turning squat into deadlift",
        "Rounding lower back under load",
        "Bar drifting away from body",
        "Hyperextending at lockout",
        "Shoulders rising before hips",
        "Knees collapsing inward",
        "Not engaging lats properly",
        "Dropping hips too low"
    ],
    "BRDG": [
        "Overextending lumbar spine",
        "Using lower back instead of glutes",
        "Incomplete hip extension",
        "Feet too far from glutes",
        "Pelvis tilting anteriorly",
        "Neck craning upward",
        "Rushing the movement",
        "Uneven hip height"
    ],
    "CRCH": [
        "Pulling on neck with hands",
        "Using hip flexors instead of abs",
        "Incomplete range of motion",
        "Holding breath throughout",
        "Jerky momentum-based movement",
        "Lower back arching off floor",
        "Chin jutting forward",
        "Rushing the eccentric"
    ],
    "ROT": [
        "Rotating from lumbar instead of thoracic",
        "Back foot not pivoting",
        "Arms doing work instead of core",
        "Loss of athletic stance",
        "Eyes not tracking movement",
        "Poor deceleration control",
        "Imbalanced left/right training",
        "Holding breath during rotation"
    ],
    "CRRY": [
        "Leaning toward loaded side",
        "Shoulders hiking up",
        "Core not braced properly",
        "Steps too long or uncontrolled",
        "Load swinging or rotating",
        "Grip failing mid-carry",
        "Head looking down",
        "Shuffling instead of walking"
    ],
    "PLYO": [
        "Heavy loud landings",
        "Insufficient recovery between reps",
        "Incomplete triple extension",
        "Arms not coordinating",
        "Landing with straight legs",
        "Knee valgus on landing",
        "Too much volume too soon",
        "Poor technique when fatigued"
    ],
    "SPRT": [
        "Upright posture during acceleration",
        "Insufficient knee drive",
        "Heel striking instead of forefoot",
        "Tense face and jaw",
        "Irregular breathing pattern",
        "Starting too fast, fading late",
        "Poor arm carriage",
        "Inadequate recovery between reps"
    ],
    "AGIL": [
        "High center of gravity on cuts",
        "Wide plant foot placement",
        "Rounded turning path",
        "Looking down instead of up",
        "Insufficient deceleration",
        "Arms not used for balance",
        "Flat-footed movements",
        "Sub-maximal intensity"
    ],
    "MOBL": [
        "Forcing beyond current range",
        "Bouncing in stretched position",
        "Holding breath during stretches",
        "Ignoring pain signals",
        "Passive hanging without engagement",
        "Skipping painful restricted areas",
        "Jerky uncontrolled movements",
        "No mind-muscle connection"
    ],
    "ACTV": [
        "Static stretching before activity",
        "Too high intensity too soon",
        "Skipping target muscle activation",
        "Generic non-specific movements",
        "Insufficient heart rate elevation",
        "No nervous system priming",
        "Missing sport-specific elements",
        "Rushed incomplete routine"
    ],
    "RCVR": [
        "Too high intensity for recovery",
        "Ignoring breathing focus",
        "Skipping hydration/nutrition",
        "Poor sleep hygiene",
        "High stress during session",
        "Dismissing body signals",
        "Inconsistent recovery protocols",
        "Over-reliance on passive modalities"
    ],
    "ASMT": [
        "Inconsistent testing conditions",
        "Insufficient warm-up",
        "Sub-maximal effort",
        "Poor measurement technique",
        "Ignoring relevant context",
        "Comparing to wrong standards",
        "Testing too frequently",
        "Inadequate rest between tests"
    ]
}

CONTRAINDICATIONS_DB = {
    "DLKD": [
        "Acute knee injury or instability",
        "Severe ankle mobility restrictions",
        "Recent hip surgery",
        "Uncontrolled hypertension",
        "Acute lower back pain",
        "Meniscus tear",
        "ACL reconstruction (early phase)",
        "Severe osteoarthritis in lower extremities"
    ],
    "ULPD": [
        "Shoulder impingement syndrome",
        "AC joint separation",
        "Rotator cuff tear",
        "Elbow tendonitis",
        "Wrist fracture (recent)",
        "Thoracic outlet syndrome",
        "Unstable shoulder joint",
        "Pectoral strain (acute)"
    ],
    "HNGE": [
        "Acute hamstring strain",
        "Lumbar disc herniation",
        "Sciatica flare-up",
        "Hip flexor strain",
        "Recent abdominal surgery",
        "Sacroiliac joint dysfunction",
        "Piriformis syndrome (acute)",
        "Vertebral compression fracture"
    ],
    "BRDG": [
        "Acute hip pathology",
        "SI joint instability",
        "Recent spinal fusion",
        "Hamstring avulsion",
        "Knee effusion",
        "Patellar tendinopathy (severe)",
        "Hip impingement (acute)",
        "Pelvic floor dysfunction"
    ],
    "CRCH": [
        "Hiatal hernia",
        "GERD/acid reflux (severe)",
        "Rectus diastasis (postpartum)",
        "Lower back disc issues",
        "Hip flexor strain",
        "Neck injury",
        "Recent abdominal surgery",
        "Pregnancy (third trimester)"
    ],
    "ROT": [
        "Acute oblique strain",
        "Lumbar instability",
        "Hip labral tear",
        "Thoracic spine fracture",
        "Rib fracture",
        "Recent hernia repair",
        "Spondylolisthesis",
        "Acute shoulder pathology"
    ],
    "CRRY": [
        "Shoulder dislocation history",
        "Grip strength deficiency",
        "Balance disorders",
        "Acute ankle sprain",
        "Hip abductor weakness",
        "Spinal loading contraindication",
        "Vertigo or dizziness",
        "Peripheral neuropathy"
    ],
    "PLYO": [
        "Patellar tendinopathy",
        "Achilles tendinopathy",
        "Stress fracture history",
        "ACL reconstruction (<6 months)",
        "Ankle instability",
        "Meniscus repair",
        "Osteochondral defect",
        "Severe obesity (BMI >35)"
    ],
    "SPRT": [
        "Cardiovascular disease",
        "Uncontrolled asthma",
        "Acute hamstring strain",
        "Calf strain",
        "Plantar fasciitis (severe)",
        "Hip flexor strain",
        "Recent concussion",
        "Heat intolerance"
    ],
    "AGIL": [
        "ACL deficiency",
        "Ankle instability",
        "Meniscus tear",
        "Hip dysplasia",
        "Patellofemoral pain syndrome",
        "Achilles rupture (recent)",
        "Balance disorders",
        "Neurological conditions affecting coordination"
    ],
    "MOBL": [
        "Joint hypermobility syndrome",
        "Acute muscle strain",
        "Fracture (non-healed)",
        "Joint replacement (early phase)",
        "Severe osteoporosis",
        "Spinal instability",
        "Acute inflammation",
        "Nerve compression syndromes"
    ],
    "ACTV": [
        "Fever or acute illness",
        "Severe dehydration",
        "Uncontrolled cardiac condition",
        "Acute injury in target area",
        "Severe fatigue/overtraining",
        "Heat stroke history (caution)",
        "Medication affecting heart rate",
        "Pregnancy complications"
    ],
    "RCVR": [
        "Acute infection with fever",
        "Deep vein thrombosis",
        "Open wounds or infections",
        "Severe cardiovascular disease",
        "Uncontrolled diabetes",
        "Skin conditions (for water therapy)",
        "Pacemaker (for electrical modalities)",
        "Pregnancy (certain modalities)"
    ],
    "ASMT": [
        "Acute injury or pain",
        "Illness or fever",
        "Insufficient sleep (<6 hours)",
        "Alcohol consumption (<24hrs)",
        "Intense training (<48hrs prior)",
        "Medication affecting performance",
        "Dehydration",
        "Psychological stress (extreme)"
    ]
}

EQUIPMENT_ALTERNATIVES_DB = {
    "Barbell": ["Trap bar", "Safety squat bar", "Cambered bar", "Axle bar"],
    "DB/KB": ["Resistance bands", "Water jugs", "Sandbag", "Medicine ball"],
    "Machine": ["Cable system", "Resistance bands", "Free weights", "Bodyweight variations"],
    "Box": ["Bench", "Sturdy chair", "Step platform", "Stacked plates"],
    "Rack": ["Squat stands", "Wall supports", "TRX straps", "Resistance bands"],
    "Bench": ["Floor", "Stability ball", "Incline surface", "Decline surface"],
    "Cable": ["Resistance bands", "Pulley system", "Free weights", "Bodyweight"],
    "Medicine Ball": ["Sandbag", "Weight plate", "DB/KB", "Resistance band"],
    "Foam Roller": ["Lacrosse ball", "Massage gun", "Stretching", "Manual release"],
    "Band": ["Cable machine", "Free weights", "Bodyweight resistance", "Partner resistance"],
    "Bodyweight": ["Added weight vest", "Resistance bands", "Suspension trainer", "Unstable surface"],
    "TRX": ["Resistance bands", "Gymnastic rings", "Cable machine", "Bodyweight floor variations"],
    "Slide Board": ["Towel on smooth floor", "Paper plates", "Sliders", "Ice skating motion"],
    "Agility Ladder": ["Chalk marks", "Cones", "Tape lines", "Imaginary ladder"],
    "Cones": ["Water bottles", "Shoes", "Tape marks", "Chalk circles"],
    "Jump Rope": ["Imaginary rope", "High knees", "Boxer shuffle", "Calf raises"]
}

FORCE_VECTOR_DB = {
    "DLKD": "Vertical compressive",
    "ULPD": "Vertical compressive + Horizontal shear",
    "HNGE": "Posterior chain dominant",
    "BRDG": "Hip extension dominant",
    "CRCH": "Trunk flexion",
    "ROT": "Rotational/transverse",
    "CRRY": "Anti-lateral flexion + Vertical compressive",
    "PLYO": "Vertical reactive + Stretch-shortening",
    "SPRT": "Horizontal propulsive",
    "AGIL": "Multi-directional reactive",
    "MOBL": "Non-loaded articulation",
    "ACTV": "Movement preparation",
    "RCVR": "Restorative circulation",
    "ASMT": "Diagnostic baseline"
}

SPORT_TAGS_DB = {
    "DLKD": ["Football", "Basketball", "Rugby", "Track & Field", "Wrestling", "Baseball", "Cricket", "Tennis"],
    "ULPD": ["Basketball", "Football", "Rugby", "Swimming", "Gymnastics", "Boxing", "MMA", "Tennis"],
    "HNGE": ["Track & Field", "Football", "Rugby", "Wrestling", "Rowing", "Cycling", "Speed Skating"],
    "BRDG": ["Football", "Rugby", "Track & Field", "Basketball", "Wrestling", "Gymnastics"],
    "CRCH": ["All Sports", "Boxing", "MMA", "Gymnastics", "Swimming", "Rowing"],
    "ROT": ["Baseball", "Tennis", "Golf", "Cricket", "Hockey", "Discus", "Javelin", "Boxing"],
    "CRRY": ["Football", "Rugby", "Wrestling", "MMA", "Strongman", "Basketball"],
    "PLYO": ["Basketball", "Volleyball", "Track & Field", "Tennis", "Badminton", "Netball"],
    "SPRT": ["Track & Field", "Football", "Rugby", "Basketball", "Tennis", "Badminton", "Cricket"],
    "AGIL": ["Basketball", "Tennis", "Badminton", "Football", "Rugby", "Soccer", "Cricket", "Field Hockey"],
    "MOBL": ["All Sports", "Yoga", "Pilates", "Gymnastics", "Martial Arts", "Dance"],
    "ACTV": ["All Sports"],
    "RCVR": ["All Sports"],
    "ASMT": ["All Sports"]
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_family(exercise):
    """Extract primary family from exercise"""
    return exercise.get("family", "Unknown")

def get_coaching_cues(family):
    """Get 4 coaching cues based on family"""
    cues = COACHING_CUES_DB.get(family, COACHING_CUES_DB["MOBL"])
    return cues[:4]

def get_common_faults(family):
    """Get 4 common faults based on family"""
    faults = COMMON_FAULTS_DB.get(family, COMMON_FAULTS_DB["MOBL"])
    return faults[:4]

def get_contraindications(family):
    """Get 3 contraindications based on family"""
    contras = CONTRAINDICATIONS_DB.get(family, CONTRAINDICATIONS_DB["MOBL"])
    return contras[:3]

def get_equipment_alternatives(equipment_list):
    """Get equipment alternatives based on primary equipment"""
    if not equipment_list or equipment_list[0] == "Bodyweight":
        return ["Resistance bands", "Suspension trainer", "Unstable surface"]
    
    primary = equipment_list[0]
    alternatives = EQUIPMENT_ALTERNATIVES_DB.get(primary, ["Bodyweight variations", "Resistance bands", "Cable system"])
    return alternatives[:3]

def calculate_technical_difficulty(exercise):
    """Calculate technical difficulty 1-10 based on exercise properties"""
    base_difficulty = exercise.get("difficulty", 1)
    
    # Adjust based on exercise characteristics
    multiplier = 1.0
    if exercise.get("unilateral"):
        multiplier += 0.5
    if exercise.get("explosive"):
        multiplier += 0.5
    if exercise.get("rotational"):
        multiplier += 0.3
    if exercise.get("isometric"):
        multiplier += 0.2
    
    # Equipment complexity
    equipment = exercise.get("equipment", [])
    if "Barbell" in equipment and "Rack" in equipment:
        multiplier += 0.3
    if "Machine" in equipment:
        multiplier -= 0.2
    
    tech_difficulty = min(10, max(1, int(base_difficulty * multiplier)))
    return tech_difficulty

def calculate_training_age(family, difficulty):
    """Calculate minimum training age in months"""
    base_months = {
        "MOBL": 0, "ACTV": 0, "RCVR": 0, "ASMT": 0,
        "CRCH": 1, "BRDG": 1,
        "DLKD": 2, "ULPD": 2, "HNGE": 3,
        "CRRY": 3, "ROT": 4,
        "AGIL": 4, "SPRT": 4,
        "PLYO": 6
    }
    
    base = base_months.get(family, 3)
    difficulty_bonus = (difficulty - 1) * 2
    
    return base + difficulty_bonus

def get_force_vector(family):
    """Get force vector classification"""
    return FORCE_VECTOR_DB.get(family, "General")

def get_sport_tags(family, secondary_family=None):
    """Get comprehensive sport tags"""
    base_tags = SPORT_TAGS_DB.get(family, ["All Sports"])
    
    # Add secondary family sports if applicable
    if secondary_family and secondary_family in SPORT_TAGS_DB:
        additional = SPORT_TAGS_DB[secondary_family]
        base_tags = list(set(base_tags + additional))
    
    # Remove duplicates and sort
    if "All Sports" in base_tags:
        base_tags = ["All Sports"]
    
    return sorted(base_tags)

# ============================================================================
# MAIN ENRICHMENT FUNCTION
# ============================================================================

def enrich_exercise(exercise):
    """Add all Phase 1 metadata to a single exercise"""
    family = get_family(exercise)
    secondary = exercise.get("secondary_family")
    difficulty = exercise.get("difficulty", 1)
    equipment = exercise.get("equipment", [])
    
    enriched = exercise.copy()
    
    # Add new metadata fields
    enriched["coaching_cues"] = get_coaching_cues(family)
    enriched["common_faults"] = get_common_faults(family)
    enriched["contraindications"] = get_contraindications(family)
    enriched["equipment_alternatives"] = get_equipment_alternatives(equipment)
    enriched["technical_difficulty"] = calculate_technical_difficulty(exercise)
    enriched["training_age_min_months"] = calculate_training_age(family, difficulty)
    enriched["force_vector"] = get_force_vector(family)
    enriched["sport_tags"] = get_sport_tags(family, secondary)
    
    return enriched

def main():
    print("=" * 80)
    print("FORGE EXERCISE LIBRARY - PHASE 1 METADATA ENRICHMENT")
    print("Adding: Coaching Cues, Common Faults, Contraindications,")
    print("        Equipment Alternatives, Technical Difficulty,")
    print("        Training Age, Force Vector, Sport Tags")
    print("=" * 80)
    print()
    
    # Enrich all exercises
    enriched_exercises = []
    stats = {
        "total": len(EXERCISES_DATA),
        "enriched": 0,
        "families_processed": set(),
        "sport_tags_added": 0
    }
    
    for exercise in EXERCISES_DATA:
        try:
            enriched = enrich_exercise(exercise)
            enriched_exercises.append(enriched)
            
            stats["enriched"] += 1
            stats["families_processed"].add(exercise.get("family", "Unknown"))
            if "sport_tags" in enriched:
                stats["sport_tags_added"] += 1
                
        except Exception as e:
            print(f"ERROR processing {exercise.get('id', 'Unknown')}: {e}")
            enriched_exercises.append(exercise)  # Keep original on error
    
    # Save enriched data
    output_file = "enriched_exercises_phase1.json"
    with open(output_file, 'w') as f:
        json.dump(enriched_exercises, f, indent=2)
    
    # Print report
    print("ENRICHMENT RESULTS:")
    print("-" * 80)
    print(f"Total Exercises Processed: {stats['total']}")
    print(f"Successfully Enriched:     {stats['enriched']} ({stats['enriched']/stats['total']*100:.1f}%)")
    print(f"Families Covered:          {len(stats['families_processed'])}")
    print(f"                           {sorted(stats['families_processed'])}")
    print(f"Sport Tags Added:          {stats['sport_tags_added']}")
    print()
    
    # Sample output
    print("SAMPLE ENRICHED EXERCISE:")
    print("-" * 80)
    sample = enriched_exercises[0]
    for key in ["id", "name", "family"]:
        print(f"  {key}: {sample.get(key)}")
    print(f"  coaching_cues: {sample.get('coaching_cues')}")
    print(f"  common_faults: {sample.get('common_faults')}")
    print(f"  contraindications: {sample.get('contraindications')}")
    print(f"  equipment_alternatives: {sample.get('equipment_alternatives')}")
    print(f"  technical_difficulty: {sample.get('technical_difficulty')}")
    print(f"  training_age_min_months: {sample.get('training_age_min_months')}")
    print(f"  force_vector: {sample.get('force_vector')}")
    print(f"  sport_tags: {sample.get('sport_tags')}")
    print()
    
    print(f"✓ Output saved to: {output_file}")
    print()
    print("NEXT STEPS:")
    print("  1. Review enriched_exercises_phase1.json")
    print("  2. Validate metadata quality")
    print("  3. Integrate into exercises_data.py")
    print("  4. Update database schema if needed")
    print("  5. Proceed to Phase 2 (Category Expansion)")
    print("=" * 80)

if __name__ == "__main__":
    main()
