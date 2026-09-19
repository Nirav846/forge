#!/usr/bin/env python3
"""
Script to auto-tag exercises with sport/role based on complex usage
"""

import json
from collections import defaultdict

def load_data():
    with open('forge_web/src/data/exercises.json', 'r') as f:
        exercises = json.load(f)
    with open('forge_web/src/data/complexes.json', 'r') as f:
        complexes = json.load(f)
    return exercises, complexes

def save_exercises(exercises):
    with open('forge_web/src/data/exercises.json', 'w') as f:
        json.dump(exercises, f, indent=2)

def analyze_complex_usage(complexes):
    exercise_usage = defaultdict(lambda: defaultdict(set))
    
    for complex_item in complexes:
        sport = complex_item.get('sport')
        role = complex_item.get('role')
        
        if not sport or not role:
            continue
        
        for ex_ref in complex_item.get('exercises', []):
            ex_id = str(ex_ref.get('exerciseId'))
            exercise_usage[ex_id][sport].add(role)
    
    return exercise_usage

def tag_exercises_from_complexes():
    exercises, complexes = load_data()
    
    ex_by_id = {str(ex['id']): ex for ex in exercises}
    usage_map = analyze_complex_usage(complexes)
    
    print(f"Analyzed {len(complexes)} complexes")
    print(f"Found {len(usage_map)} exercises used in complexes")
    
    tagged_count = 0
    for ex_id, sport_roles in usage_map.items():
        if ex_id not in ex_by_id:
            print(f"Warning: Exercise {ex_id} not found in library")
            continue
        
        exercise = ex_by_id[ex_id]
        
        if 'sport_tags' not in exercise:
            exercise['sport_tags'] = []
        if 'role_tags' not in exercise:
            exercise['role_tags'] = {}
        
        for sport in sport_roles.keys():
            if sport not in exercise['sport_tags']:
                exercise['sport_tags'].append(sport)
        
        for sport, roles in sport_roles.items():
            if sport not in exercise['role_tags']:
                exercise['role_tags'][sport] = []
            for role in roles:
                if role not in exercise['role_tags'][sport]:
                    exercise['role_tags'][sport].append(role)
        
        tagged_count += 1
    
    print(f"\nTagged {tagged_count} exercises with sport/role information")
    
    sports_tagged = set()
    for ex in exercises:
        if 'sport_tags' in ex:
            sports_tagged.update(ex['sport_tags'])
    
    print(f"Sports covered: {sorted(sports_tagged)}")
    
    save_exercises(exercises)
    print("\nSaved updated exercises.json")
    
    untagged = [ex for ex in exercises if 'sport_tags' not in ex or len(ex['sport_tags']) == 0]
    print(f"\nExercises still untagged: {len(untagged)}")
    print("These are foundational exercises not in complexes - recommend manual tagging")

if __name__ == '__main__':
    tag_exercises_from_complexes()
