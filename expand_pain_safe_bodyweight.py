#!/usr/bin/env python3
"""
Script to expand pain-safe and bodyweight exercise tags
Based on exercise characteristics and equipment
"""

import json

def load_exercises():
    with open('forge_web/src/data/exercises.json', 'r') as f:
        return json.load(f)

def save_exercises(exercises):
    with open('forge_web/src/data/exercises.json', 'w') as f:
        json.dump(exercises, f, indent=2)

def should_be_pain_safe(exercise):
    """Determine if exercise should be tagged as pain-safe"""
    category = exercise.get('category', '')
    difficulty = exercise.get('difficulty', 'Beginner')
    equipment = exercise.get('equipment', '')
    name = exercise.get('name', '').lower()
    
    # Pain-safe categories
    safe_categories = ['Activation', 'Mobility', 'Assessment', 'CORE']
    if category in safe_categories:
        return True
    
    # Bodyweight exercises at beginner/intermediate level
    if equipment == 'Bodyweight' and difficulty in ['Beginner', 'Intermediate']:
        # Check for low-impact indicators
        impact_keywords = ['jump', 'plyo', 'bound', 'hop', 'sprint']
        if not any(kw in name for kw in impact_keywords):
            return True
    
    # Band exercises are generally pain-safe
    if 'Band' in equipment:
        return True
    
    # Isometric holds are pain-safe
    isometric_keywords = ['hold', 'bridge', 'plank', 'wall sit', 'dead bug']
    if any(kw in name for kw in isometric_keywords):
        return True
    
    return False

def should_be_bodyweight(exercise):
    """Determine if exercise can be done with bodyweight only"""
    equipment = exercise.get('equipment', '')
    
    # Already bodyweight
    if equipment == 'Bodyweight':
        return True
    
    # Can be modified to bodyweight
    bodyweight_alternatives = ['Barbell', 'Dumbbell', 'Kettlebell', 'Med Ball', 'Band', 'Cable']
    if any(eq in equipment for eq in bodyweight_alternatives):
        # Check if it's a fundamental movement that can be bodyweight
        category = exercise.get('category', '')
        fundamental_categories = ['DLKD', 'DLHD', 'SLKD', 'SLHD', 'PUSH', 'PULL', 'CORE', 'PLYO']
        if category in fundamental_categories:
            return True
    
    return False

def expand_tags():
    exercises = load_exercises()
    
    # Track changes
    pain_safe_added = 0
    bodyweight_added = 0
    
    for exercise in exercises:
        # Expand pain-safe tagging
        if not exercise.get('is_pain_safe', False):
            if should_be_pain_safe(exercise):
                exercise['is_pain_safe'] = True
                pain_safe_added += 1
        
        # Expand bodyweight alternatives
        equipment = exercise.get('equipment', '')
        if equipment != 'Bodyweight' and should_be_bodyweight(exercise):
            if 'Bodyweight' not in equipment:
                # Add bodyweight as alternative
                if 'equipment_alternatives' not in exercise:
                    exercise['equipment_alternatives'] = []
                if 'Bodyweight' not in exercise['equipment_alternatives']:
                    exercise['equipment_alternatives'].append('Bodyweight')
                    bodyweight_added += 1
    
    print(f"Added {pain_safe_added} pain-safe exercises")
    print(f"Added {bodyweight_added} bodyweight alternatives")
    
    # Verify
    pain_safe_count = sum(1 for ex in exercises if ex.get('is_pain_safe'))
    bodyweight_count = sum(1 for ex in exercises if ex.get('equipment') == 'Bodyweight')
    bodyweight_alt_count = sum(1 for ex in exercises if 'Bodyweight' in ex.get('equipment_alternatives', []))
    
    print(f"\nTotal pain-safe exercises: {pain_safe_count}/{len(exercises)} ({pain_safe_count/len(exercises)*100:.1f}%)")
    print(f"Total bodyweight-only exercises: {bodyweight_count}/{len(exercises)} ({bodyweight_count/len(exercises)*100:.1f}%)")
    print(f"Exercises with bodyweight alternative: {bodyweight_alt_count}/{len(exercises)} ({bodyweight_alt_count/len(exercises)*100:.1f}%)")
    
    save_exercises(exercises)
    print("\nSaved updated exercises.json")

if __name__ == '__main__':
    expand_tags()
