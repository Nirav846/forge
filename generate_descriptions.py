#!/usr/bin/env python3
"""
Script to auto-generate exercise descriptions using AI patterns
Based on coaching cues and common errors
"""

import json

def load_exercises():
    with open('forge_web/src/data/exercises.json', 'r') as f:
        return json.load(f)

def save_exercises(exercises):
    with open('forge_web/src/data/exercises.json', 'w') as f:
        json.dump(exercises, f, indent=2)

def generate_description_from_cues(exercise):
    """Generate description from coaching cues and exercise metadata"""
    name = exercise.get('name', 'Exercise')
    cues = exercise.get('coaching_cues', [])
    category = exercise.get('category', 'General')
    equipment = exercise.get('equipment', 'Bodyweight')
    difficulty = exercise.get('difficulty', 'Beginner')
    
    # Map categories to movement types
    category_map = {
        'DLKD': 'double-leg knee-dominant',
        'DLHD': 'double-leg hip-dominant', 
        'SLKD': 'single-leg knee-dominant',
        'SLHD': 'single-leg hip-dominant',
        'PUSH': 'pushing',
        'PULL': 'pulling',
        'CORE': 'core stability',
        'PLYO': 'plyometric',
        'Sprint': 'sprinting',
        'Agility': 'agility',
        'Landing': 'landing mechanics',
        'Activation': 'activation',
        'Acc': 'accessory',
        'Assessment': 'assessment',
        'Mobility': 'mobility'
    }
    
    movement_type = category_map.get(category, category.lower())
    
    # Build description template
    if equipment == 'Bodyweight':
        equip_phrase = "using only bodyweight"
    elif 'Band' in equipment:
        equip_phrase = "using resistance bands"
    elif 'Barbell' in equipment:
        equip_phrase = "using a barbell"
    elif 'Dumbbell' in equipment or 'DB' in equipment:
        equip_phrase = "using dumbbells"
    elif 'Kettlebell' in equipment or 'KB' in equipment:
        equip_phrase = "using a kettlebell"
    elif 'Med Ball' in equipment or 'Medicine Ball' in equipment:
        equip_phrase = "using a medicine ball"
    else:
        equip_phrase = f"with {equipment.lower()}"
    
    # Generate base description
    desc_templates = {
        'Beginner': f"A foundational {movement_type} exercise {equip_phrase}, ideal for building basic movement patterns and strength.",
        'Intermediate': f"A {movement_type} exercise {equip_phrase} designed to develop moderate strength and technical proficiency.",
        'Advanced': f"An advanced {movement_type} exercise {equip_phrase} requiring high levels of strength, coordination, and technique.",
        'Elite': f"An elite-level {movement_type} exercise {equip_phrase} for maximum power and performance development."
    }
    
    base_desc = desc_templates.get(difficulty, desc_templates['Intermediate'])
    
    # Add key focus points from coaching cues
    if cues:
        key_points = []
        for cue in cues[:2]:  # Use first 2 cues
            # Extract key action from cue
            if 'chest' in cue.lower():
                key_points.append("maintaining an upright torso")
            if 'core' in cue.lower() or 'brace' in cue.lower():
                key_points.append("bracing the core")
            if 'knee' in cue.lower():
                key_points.append("proper knee alignment")
            if 'hip' in cue.lower():
                key_points.append("hip hinge mechanics")
            if 'control' in cue.lower():
                key_points.append("controlled movement tempo")
            if 'drive' in cue.lower() or 'push' in cue.lower():
                key_points.append("explosive ground contact")
            if 'land' in cue.lower():
                key_points.append("soft, quiet landing")
        
        if key_points:
            unique_points = list(dict.fromkeys(key_points))[:2]  # Remove duplicates, max 2
            focus_phrase = " Focus on " + " and ".join(unique_points) + "."
            base_desc += focus_phrase
    
    return base_desc

def add_descriptions():
    exercises = load_exercises()
    
    missing_desc = [ex for ex in exercises if not ex.get('description') or ex.get('description') == '']
    print(f"Found {len(missing_desc)} exercises without descriptions")
    
    updated_count = 0
    for exercise in missing_desc:
        description = generate_description_from_cues(exercise)
        exercise['description'] = description
        updated_count += 1
    
    print(f"Generated descriptions for {updated_count} exercises")
    
    # Verify
    with_desc = sum(1 for ex in exercises if ex.get('description') and ex.get('description') != '')
    print(f"\nTotal exercises with descriptions: {with_desc}/{len(exercises)} ({with_desc/len(exercises)*100:.1f}%)")
    
    save_exercises(exercises)
    print("\nSaved updated exercises.json")
    print("\nNOTE: Auto-generated descriptions should be reviewed by qualified coaches")

if __name__ == '__main__':
    add_descriptions()
