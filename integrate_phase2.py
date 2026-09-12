#!/usr/bin/env python3
"""
Integrate Phase 2 new exercises into exercises_data.py
"""
import json

# Load existing exercises
from src.forge.exercises_data import EXERCISES_DATA

# Load new Phase 2 exercises
with open('/workspace/phase2_new_exercises.json', 'r') as f:
    new_exercises = json.load(f)

# Combine
all_exercises = EXERCISES_DATA + new_exercises

print(f"Existing exercises: {len(EXERCISES_DATA)}")
print(f"New Phase 2 exercises: {len(new_exercises)}")
print(f"Total combined: {len(all_exercises)}")

# Build the new file content with proper formatting
exercise_strings = []
for ex in all_exercises:
    exercise_str = f'''  {{
    "id": "{ex['id']}",
    "name": "{ex['name']}",
    "family": "{ex['family']}",
    "secondary_family": {repr(ex.get('secondary_family'))},
    "objective": "{ex['objective']}",
    "difficulty": {ex['difficulty']},
    "equipment": {ex['equipment']},
    "unilateral": {str(ex['unilateral']).capitalize()},
    "explosive": {str(ex['explosive']).capitalize()},
    "isometric": {str(ex['isometric']).capitalize()},
    "rotational": {str(ex['rotational']).capitalize()},
    "progression": {repr(ex.get('progression'))},
    "regression": {repr(ex.get('regression'))},
    "coaching_cues": {ex['coaching_cues']},
    "common_faults": {ex['common_faults']},
    "contraindications": {ex['contraindications']},
    "equipment_alternatives": {ex['equipment_alternatives']},
    "technical_difficulty": {ex['technical_difficulty']},
    "training_age_min_months": {ex['training_age_min_months']},
    "force_vector": "{ex['force_vector']}",
    "sport_tags": {ex['sport_tags']}
  }}'''
    exercise_strings.append(exercise_str)

header = '''"""
Exercise Library - Production Ready (Phase 1 & 2 Complete)
==========================================================
Total Exercises: 334
Movement Families: 21 (added Recovery, Activation, Assessment)
Enrichment Status: Phase 1 & 2 Complete

Metadata Fields:
- coaching_cues: Technical instruction cues (4 per exercise)
- common_faults: Typical movement errors (4 per exercise)
- contraindications: When NOT to use the exercise (3 per exercise)
- equipment_alternatives: Substitute equipment options (3 per exercise)
- technical_difficulty: Complexity rating 1-10
- training_age_min_months: Minimum experience required
- force_vector: Biomechanical classification
- sport_tags: Sport applicability tags

Category Breakdown:
- Original Strength/Power: 299 exercises
- Recovery/Mobility: 15 exercises (REC-001 to REC-015)
- Activation: 10 exercises (ACT-001 to ACT-010)
- Assessment: 10 exercises (ASMT-001 to ASMT-010)
"""

EXERCISES_DATA = [
'''

footer = '''
]
'''

new_content = header + ',\n'.join(exercise_strings) + footer

# Write the new file
with open('/workspace/src/forge/exercises_data.py', 'w') as f:
    f.write(new_content)

print(f"\n✅ Successfully integrated all {len(all_exercises)} exercises")
print(f"📁 Updated: /workspace/src/forge/exercises_data.py")
print(f"📊 File size: {len(new_content):,} characters")

# Verify the file is valid Python
try:
    with open('/workspace/src/forge/exercises_data.py', 'r') as f:
        exec(f.read())
    print("✅ File is valid Python syntax")
except Exception as e:
    print(f"❌ Syntax error: {e}")

# Show family distribution
from collections import Counter
families = Counter(ex['family'] for ex in all_exercises)
print("\n=== Final Family Distribution ===")
for fam, count in sorted(families.items()):
    print(f"{fam}: {count}")
