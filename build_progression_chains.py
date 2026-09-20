#!/usr/bin/env python3
"""
Script to build progression/regression chains for exercises
"""

import json

def load_exercises():
    with open('forge_web/src/data/exercises.json', 'r') as f:
        return json.load(f)

def save_exercises(exercises):
    with open('forge_web/src/data/exercises.json', 'w') as f:
        json.dump(exercises, f, indent=2)

def get_difficulty_rank(difficulty):
    ranks = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3, 'Elite': 4}
    return ranks.get(difficulty, 2)

def build_progression_chains():
    exercises = load_exercises()
    
    by_pattern = {}
    for ex in exercises:
        pattern = ex.get('movement_pattern', ex.get('category', 'Unknown'))
        if pattern not in by_pattern:
            by_pattern[pattern] = []
        by_pattern[pattern].append(ex)
    
    print(f"Grouped exercises into {len(by_pattern)} movement patterns")
    
    chains_built = 0
    for pattern, ex_list in by_pattern.items():
        if len(ex_list) < 2:
            continue
        
        sorted_exercises = sorted(ex_list, key=lambda x: get_difficulty_rank(x.get('difficulty', 'Beginner')))
        
        for i, ex in enumerate(sorted_exercises):
            updated = False
            
            if i > 0:
                prev_id = sorted_exercises[i-1]['id']
                if 'regressions' not in ex:
                    ex['regressions'] = []
                if prev_id not in ex['regressions']:
                    ex['regressions'].append(prev_id)
                    updated = True
            
            if i < len(sorted_exercises) - 1:
                next_id = sorted_exercises[i+1]['id']
                if 'progressions' not in ex:
                    ex['progressions'] = []
                if next_id not in ex['progressions']:
                    ex['progressions'].append(next_id)
                    updated = True
            
            if updated:
                chains_built += 1
    
    print(f"Built {chains_built} progression/regression links")
    
    with_progressions = sum(1 for ex in exercises if ex.get('progressions'))
    with_regressions = sum(1 for ex in exercises if ex.get('regressions'))
    
    print(f"\nExercises with progressions: {with_progressions}/{len(exercises)} ({with_progressions/len(exercises)*100:.1f}%)")
    print(f"Exercises with regressions: {with_regressions}/{len(exercises)} ({with_regressions/len(exercises)*100:.1f}%)")
    
    save_exercises(exercises)
    print("\nSaved updated exercises.json")
    print("\nMANUAL REVIEW REQUIRED: Review progression chains for safety")

if __name__ == '__main__':
    build_progression_chains()
