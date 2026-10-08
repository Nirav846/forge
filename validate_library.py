#!/usr/bin/env python3
"""
Validation script to check exercise library and complexes integrity
Run this before deploying changes
"""

import json
from typing import Dict, List, Tuple

def load_data() -> Tuple[List[Dict], List[Dict]]:
    with open('forge_web/src/data/exercises.json', 'r') as f:
        exercises = json.load(f)
    with open('forge_web/src/data/complexes.json', 'r') as f:
        complexes = json.load(f)
    return exercises, complexes

def validate_exercise_references(exercises: List[Dict], complexes: List[Dict]) -> List[Dict]:
    """Check that all exercise IDs in complexes exist in library"""
    errors = []
    
    exercise_ids = {str(ex['id']) for ex in exercises}
    
    for complex_item in complexes:
        for ex_ref in complex_item.get('exercises', []):
            ex_id = str(ex_ref.get('exerciseId'))
            if ex_id not in exercise_ids:
                errors.append({
                    'type': 'missing_exercise_reference',
                    'complex_id': complex_item['id'],
                    'complex_name': complex_item['name'],
                    'missing_exercise_id': ex_id,
                    'exercise_name': ex_ref.get('exerciseName')
                })
    
    return errors

def validate_metadata_completeness(exercises: List[Dict], complexes: List[Dict]) -> Dict:
    """Check for missing required fields"""
    issues = {
        'exercises': [],
        'complexes': []
    }
    
    ex_required = ['name', 'category', 'difficulty']
    ex_recommended = ['description', 'coaching_cues', 'common_errors']
    
    for ex in exercises:
        missing_required = [f for f in ex_required if not ex.get(f)]
        missing_recommended = [f for f in ex_recommended if not ex.get(f)]
        
        if missing_required:
            issues['exercises'].append({
                'id': ex['id'],
                'name': ex['name'],
                'missing_required': missing_required,
                'missing_recommended': missing_recommended
            })
    
    cplx_required = ['name', 'sport', 'role', 'intent', 'exercises']
    
    for cplx in complexes:
        missing = [f for f in cplx_required if not cplx.get(f)]
        if missing:
            issues['complexes'].append({
                'id': cplx['id'],
                'name': cplx['name'],
                'missing_fields': missing
            })
    
    return issues

def run_validation():
    print("=" * 60)
    print("FORGE EXERCISE LIBRARY VALIDATION")
    print("=" * 60)
    
    exercises, complexes = load_data()
    
    print(f"\nLoaded {len(exercises)} exercises and {len(complexes)} complexes")
    
    all_passed = True
    
    # 1. Validate exercise references
    print("\n1. Checking exercise references in complexes...")
    ref_errors = validate_exercise_references(exercises, complexes)
    if ref_errors:
        print(f"   FAILED: {len(ref_errors)} broken references found")
        for err in ref_errors[:5]:
            print(f"      - Complex {err['complex_id']} references missing exercise {err['missing_exercise_id']}")
        all_passed = False
    else:
        print("   PASSED: All exercise references valid")
    
    # 2. Validate metadata completeness
    print("\n2. Checking metadata completeness...")
    meta_issues = validate_metadata_completeness(exercises, complexes)
    
    if len(meta_issues['exercises']) > 0:
        print(f"   WARNING: {len(meta_issues['exercises'])} exercises with missing recommended fields")
    else:
        print("   PASSED: All exercises have recommended fields")
    
    if len(meta_issues['complexes']) > 0:
        print(f"   FAILED: {len(meta_issues['complexes'])} complexes with missing fields")
        all_passed = False
    else:
        print("   PASSED: All complexes have required fields")
    
    # 3. Summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    
    desc_count = sum(1 for ex in exercises if ex.get('description'))
    pain_safe_count = sum(1 for ex in exercises if ex.get('is_pain_safe'))
    bodyweight_count = sum(1 for ex in exercises if ex.get('equipment') == 'Bodyweight')
    prog_count = sum(1 for ex in exercises if ex.get('progressions'))
    reg_count = sum(1 for ex in exercises if ex.get('regressions'))
    
    print(f"Exercises with descriptions: {desc_count}/{len(exercises)} ({desc_count/len(exercises)*100:.1f}%)")
    print(f"Pain-safe exercises: {pain_safe_count}/{len(exercises)} ({pain_safe_count/len(exercises)*100:.1f}%)")
    print(f"Bodyweight exercises: {bodyweight_count}/{len(exercises)} ({bodyweight_count/len(exercises)*100:.1f}%)")
    print(f"Exercises with progressions: {prog_count}/{len(exercises)} ({prog_count/len(exercises)*100:.1f}%)")
    print(f"Exercises with regressions: {reg_count}/{len(exercises)} ({reg_count/len(exercises)*100:.1f}%)")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("VALIDATION PASSED - Ready for deployment")
    else:
        print("VALIDATION FAILED - Fix errors before deployment")
    print("=" * 60)
    
    return all_passed

if __name__ == '__main__':
    success = run_validation()
    exit(0 if success else 1)
