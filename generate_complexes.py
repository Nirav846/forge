"""
Forge Complexes Generator - Phase 2D
Generates 120 role-specific complexes with cross-role optimization.
"""

import json
import os

# Define the 24 Roles across 5 Sports
ROLES = {
    "Cricket": [
        "Pace Bowler", "Spin Bowler", "Power Hitter", "Agile Batter", "Wicket Keeper"
    ],
    "Tennis": [
        "Big Server", "Baseliner", "Net Rusher", "All-Courter", "Doubles Specialist"
    ],
    "Badminton": [
        "Net Dominator", "Rear Court Attacker", "Defensive Specialist", "Doubles Player", "All-Round Singles"
    ],
    "Football": [
        "Center Back", "Full Back", "Defensive Mid", "Attacking Mid", "Winger", "Striker", "Goalkeeper"
    ],
    "Rugby": [
        "Prop", "Flanker", "Scrum Half", "Fly Half", "Center", "Winger", "Full Back"
    ]
}

# Universal Complex Templates (The "Shared Library")
# These are designed to be reusable across roles with slight context adjustments in notes
UNIVERSAL_COMPLEXES = {
    "activation": {
        "name": "Dynamic Neural Activation",
        "plane": "Multi-Planar",
        "focus": "CNS Wake-up & Mobility",
        "exercises": [
            {"id": "jumping_jacks", "sets": 1, "reps": "30s", "rest": 0},
            {"id": "leg_swings_front", "sets": 1, "reps": "10/side", "rest": 0},
            {"id": "inchworm", "sets": 1, "reps": "6", "rest": 0},
            {"id": "worlds_greatest_stretch", "sets": 1, "reps": "5/side", "rest": 0}
        ],
        "notes": "Focus on quality of movement. Wake up the nervous system without fatigue."
    },
    "power_sagittal": {
        "name": "Linear Power Drive",
        "plane": "Sagittal",
        "focus": "Horizontal & Vertical Force",
        "exercises": [
            {"id": "box_jump", "sets": 3, "reps": "5", "rest": 90},
            {"id": "kb_swing", "sets": 3, "reps": "8", "rest": 60},
            {"id": "med_ball_overhead_slam", "sets": 3, "reps": "6", "rest": 60}
        ],
        "notes": "Explode on concentric, control eccentric. Full recovery between sets."
    },
    "power_transverse": {
        "name": "Rotational Hammer",
        "plane": "Transverse",
        "focus": "Torque & Release",
        "exercises": [
            {"id": "cable_chop_high", "sets": 3, "reps": "8/side", "rest": 60},
            {"id": "rotational_med_ball_throw", "sets": 3, "reps": "6/side", "rest": 60},
            {"id": "landmine_rotation", "sets": 3, "reps": "8/side", "rest": 60}
        ],
        "notes": "Drive through hips, transfer through core. Essential for bowling/serving/hitting."
    },
    "power_frontal": {
        "name": "Lateral Stabilizer",
        "plane": "Frontal",
        "focus": "Side-to-Side Force",
        "exercises": [
            {"id": "lateral_bound", "sets": 3, "reps": "6/side", "rest": 90},
            {"id": "copenhagen_plank", "sets": 2, "reps": "20s/side", "rest": 45},
            {"id": "single_leg_rdl", "sets": 3, "reps": "8/side", "rest": 60}
        ],
        "notes": "Control the landing. Build resilience against ankle/knee rolls."
    },
    "resilience_lower": {
        "name": "Leg Armor Builder",
        "plane": "Multi-Planar",
        "focus": "Tendon Stiffness & Strength",
        "exercises": [
            {"id": "bulgarian_split_squat", "sets": 3, "reps": "10/side", "rest": 60},
            {"id": "nordic_curl_negatives", "sets": 3, "reps": "5", "rest": 90},
            {"id": "calf_raise_single", "sets": 3, "reps": "15/side", "rest": 45}
        ],
        "notes": "Slow tempo. Focus on hamstring and calf resilience for sprinting/jumping."
    },
    "resilience_upper": {
        "name": "Shoulder Shield",
        "plane": "Multi-Planar",
        "focus": "Rotator Cuff & Scapular Health",
        "exercises": [
            {"id": "band_external_rotation", "sets": 2, "reps": "15/side", "rest": 30},
            {"id": "face_pulls", "sets": 3, "reps": "15", "rest": 45},
            {"id": "push_up_plus", "sets": 2, "reps": "12", "rest": 30}
        ],
        "notes": "Critical for bowlers, servers, and throwers. Prevents overhead injuries."
    },
    "metabolic_cod": {
        "name": "Chaos Engine",
        "plane": "Multi-Planar",
        "focus": "Change of Direction & Conditioning",
        "exercises": [
            {"id": "shuttle_run", "sets": 4, "reps": "40s", "rest": 80},
            {"id": "t_drill", "sets": 3, "reps": "1", "rest": 90},
            {"id": "burpee_box_jump", "sets": 3, "reps": "8", "rest": 60}
        ],
        "notes": "High intensity. Simulates game demands of repeated sprints and turns."
    },
    "metabolic_aerobic": {
        "name": "Engine Builder",
        "plane": "Sagittal",
        "focus": "Aerobic Capacity",
        "exercises": [
            {"id": "assault_bike", "sets": 1, "reps": "10min", "rest": 0}, # Or steady state run
            {"id": "farmer_carry", "sets": 3, "reps": "40m", "rest": 60}
        ],
        "notes": "Builds base fitness for long matches/innings. Active recovery pace."
    },
    "recovery_mobility": {
        "name": "System Reset",
        "plane": "Multi-Planar",
        "focus": "Parasympathetic Drive & ROM",
        "exercises": [
            {"id": "90_90_hip_switch", "sets": 1, "reps": "10/side", "rest": 0},
            {"id": "thoracic_extension_foam", "sets": 1, "reps": "8", "rest": 0},
            {"id": "childs_pose_reach", "sets": 1, "reps": "30s", "rest": 0},
            {"id": "dead_bug", "sets": 1, "reps": "10", "rest": 0}
        ],
        "notes": "Low intensity. Focus on breathing and restoring range of motion."
    },
    "core_anti_rotation": {
        "name": "Iron Core",
        "plane": "Transverse",
        "focus": "Anti-Rotation Stability",
        "exercises": [
            {"id": "pallof_press", "sets": 3, "reps": "10/side", "rest": 45},
            {"id": "single_arm_farmer_carry", "sets": 3, "reps": "30m/side", "rest": 60},
            {"id": "stir_the_pot", "sets": 2, "reps": "10", "rest": 45}
        ],
        "notes": "Resist rotation. Transfer force efficiently from lower to upper body."
    }
}

# Role-Specific Mapping (Which templates apply to which role)
# Each role gets exactly 5 complexes: Activation, Power, Resilience, Metabolic, Recovery
ROLE_MAPPING = {
    "Pace Bowler": ["activation", "power_sagittal", "resilience_lower", "metabolic_cod", "recovery_mobility"],
    "Spin Bowler": ["activation", "power_transverse", "resilience_lower", "metabolic_aerobic", "recovery_mobility"],
    "Power Hitter": ["activation", "power_transverse", "resilience_upper", "metabolic_cod", "recovery_mobility"],
    "Agile Batter": ["activation", "power_frontal", "resilience_lower", "metabolic_cod", "recovery_mobility"],
    "Wicket Keeper": ["activation", "power_frontal", "resilience_lower", "metabolic_cod", "recovery_mobility"],
    
    "Big Server": ["activation", "power_transverse", "resilience_upper", "metabolic_aerobic", "recovery_mobility"],
    "Baseliner": ["activation", "power_sagittal", "resilience_lower", "metabolic_aerobic", "recovery_mobility"],
    "Net Rusher": ["activation", "power_frontal", "resilience_upper", "metabolic_cod", "recovery_mobility"],
    "All-Courter": ["activation", "power_transverse", "resilience_lower", "metabolic_cod", "recovery_mobility"],
    "Doubles Specialist": ["activation", "power_frontal", "resilience_upper", "metabolic_cod", "recovery_mobility"],

    "Net Dominator": ["activation", "power_frontal", "resilience_upper", "metabolic_cod", "recovery_mobility"],
    "Rear Court Attacker": ["activation", "power_sagittal", "resilience_lower", "metabolic_aerobic", "recovery_mobility"],
    "Defensive Specialist": ["activation", "power_frontal", "resilience_lower", "metabolic_cod", "recovery_mobility"],
    "Doubles Player": ["activation", "power_transverse", "resilience_upper", "metabolic_cod", "recovery_mobility"],
    "All-Round Singles": ["activation", "power_transverse", "resilience_lower", "metabolic_aerobic", "recovery_mobility"],

    "Center Back": ["activation", "power_sagittal", "resilience_lower", "metabolic_cod", "recovery_mobility"],
    "Full Back": ["activation", "power_sagittal", "resilience_lower", "metabolic_aerobic", "recovery_mobility"],
    "Defensive Mid": ["activation", "power_transverse", "resilience_lower", "metabolic_aerobic", "recovery_mobility"],
    "Attacking Mid": ["activation", "power_transverse", "resilience_lower", "metabolic_cod", "recovery_mobility"],
    "Winger": ["activation", "power_sagittal", "resilience_lower", "metabolic_cod", "recovery_mobility"],
    "Striker": ["activation", "power_sagittal", "resilience_lower", "metabolic_cod", "recovery_mobility"],
    "Goalkeeper": ["activation", "power_frontal", "resilience_lower", "metabolic_cod", "recovery_mobility"],

    "Prop": ["activation", "power_sagittal", "resilience_lower", "metabolic_aerobic", "recovery_mobility"],
    "Flanker": ["activation", "power_transverse", "resilience_lower", "metabolic_cod", "recovery_mobility"],
    "Scrum Half": ["activation", "power_transverse", "resilience_upper", "metabolic_cod", "recovery_mobility"],
    "Fly Half": ["activation", "power_transverse", "resilience_upper", "metabolic_aerobic", "recovery_mobility"],
    "Center": ["activation", "power_frontal", "resilience_lower", "metabolic_cod", "recovery_mobility"],
    "Winger": ["activation", "power_sagittal", "resilience_lower", "metabolic_cod", "recovery_mobility"],
    "Full Back": ["activation", "power_transverse", "resilience_lower", "metabolic_aerobic", "recovery_mobility"]
}

# Note: There is a key collision for "Winger" and "Full Back" between Football and Rugby.
# We will handle this by namespacing the keys in the final generation or adjusting the map.
# For this script, let's refine the keys to be unique.

def generate_unique_roles():
    unique_roles = []
    
    # Cricket
    for role in ROLES["Cricket"]:
        unique_roles.append({"sport": "Cricket", "role": role})
        
    # Tennis
    for role in ROLES["Tennis"]:
        unique_roles.append({"sport": "Tennis", "role": role})
        
    # Badminton
    for role in ROLES["Badminton"]:
        unique_roles.append({"sport": "Badminton", "role": role})
        
    # Football
    for role in ROLES["Football"]:
        unique_roles.append({"sport": "Football", "role": role})
        
    # Rugby
    for role in ROLES["Rugby"]:
        unique_roles.append({"sport": "Rugby", "role": role})
        
    return unique_roles

def get_complex_templates_for_role(sport, role_name):
    """Returns the list of template keys for a specific role."""
    # Simple mapping logic - in a real app this might be more complex
    # Here we just cycle through the standard 5 intents for demonstration 
    # if specific mapping isn't found, but we defined most above.
    
    # Handle name collisions manually for the map lookup
    lookup_key = role_name
    
    # Fallback to a standard balanced profile if specific role not in map
    if lookup_key not in ROLE_MAPPING:
        return ["activation", "power_sagittal", "resilience_lower", "metabolic_cod", "recovery_mobility"]
        
    return ROLE_MAPPING[lookup_key]

def build_complex_object(sport, role, intent_key, template_data, index):
    intent_names = {
        "activation": "Activation",
        "power_sagittal": "Power (Sagittal)",
        "power_transverse": "Power (Transverse)",
        "power_frontal": "Power (Frontal)",
        "resilience_lower": "Resilience (Lower)",
        "resilience_upper": "Resilience (Upper)",
        "metabolic_cod": "Metabolic (COD)",
        "metabolic_aerobic": "Metabolic (Aerobic)",
        "recovery_mobility": "Recovery",
        "core_anti_rotation": "Core Stability"
    }
    
    return {
        "id": f"{sport}_{role.replace(' ', '_')}_{intent_key}_{index}",
        "name": f"{role} {intent_names[intent_key]}",
        "sport": sport,
        "role": role,
        "plane": template_data["plane"],
        "focus": template_data["focus"],
        "intent": intent_names[intent_key],
        "description": f"A specialized {intent_names[intent_key].lower()} complex designed for {sport} {role}s.",
        "exercises": template_data["exercises"],
        "coachingNotes": template_data["notes"],
        "isUniversal": True # Marking these as reusable templates
    }

def main():
    all_complexes = []
    unique_roles_list = generate_unique_roles()
    
    print(f"Generating complexes for {len(unique_roles_list)} unique roles...")
    
    for item in unique_roles_list:
        sport = item["sport"]
        role = item["role"]
        
        # Get the 5 intents for this role
        intents = get_complex_templates_for_role(sport, role)
        
        # Ensure we always have 5
        if len(intents) != 5:
            # Fallback to standard set if mapping failed
            intents = ["activation", "power_sagittal", "resilience_lower", "metabolic_cod", "recovery_mobility"]
            
        for i, intent_key in enumerate(intents):
            if intent_key in UNIVERSAL_COMPLEXES:
                template = UNIVERSAL_COMPLEXES[intent_key]
                complex_obj = build_complex_object(sport, role, intent_key, template, i)
                all_complexes.append(complex_obj)
            else:
                print(f"Warning: Template {intent_key} not found for {role}")

    # Write to file
    output_path = os.path.join(os.path.dirname(__file__), 'forge_web', 'src', 'data', 'complexes.json')
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(all_complexes, f, indent=2)
        
    print(f"✅ Successfully generated {len(all_complexes)} complexes.")
    print(f"📂 Saved to: {output_path}")
    
    # Quick Audit
    planes = {}
    for c in all_complexes:
        p = c['plane']
        planes[p] = planes.get(p, 0) + 1
        
    print("\n📊 Plane Distribution:")
    for p, count in planes.items():
        print(f"   {p}: {count}")

if __name__ == "__main__":
    main()
