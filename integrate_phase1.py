#!/usr/bin/env python3
"""
Integrate Phase 1 enriched metadata into exercises_data.py
"""
import json
import re

# Load enriched data
with open('/workspace/enriched_exercises_phase1.json', 'r') as f:
    enriched_data = json.load(f)

# Create mapping by ID
enriched_map = {ex['id']: ex for ex in enriched_data}

# Read original file
with open('/workspace/src/forge/exercises_data.py', 'r') as f:
    original_content = f.read()

# Parse the EXERCISES_DATA list
# Find the start of EXERCISES_DATA
match = re.search(r'EXERCISES_DATA\s*=\s*\[(.*?)\n\]', original_content, re.DOTALL)
if not match:
    raise ValueError("Could not find EXERCISES_DATA list")

# Extract individual exercise dictionaries
exercise_pattern = r'\{\s*\"id\":\s*\"([^\"]+)\".*?\n\s*\}'
exercises_raw = re.findall(exercise_pattern, original_content, re.DOTALL)

print(f"Found {len(exercises_raw)} exercises in original file")
print(f"Found {len(enriched_map)} exercises in enriched data")

# Build new exercises with enriched metadata
new_exercises = []
for ex_id in enriched_map.keys():
    ex = enriched_map[ex_id]
    
    # Format the exercise dictionary with proper indentation
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
    new_exercises.append(exercise_str)

# Build the new file content
header = '''"""
Exercise Library - Production Ready (Phase 1 Enriched)
=======================================================
Total Exercises: 299
Movement Families: 18
Enrichment Date: Phase 1 Complete

New Metadata Fields Added:
- coaching_cues: Technical instruction cues (4 per exercise)
- common_faults: Typical movement errors (4 per exercise)
- contraindications: When NOT to use the exercise (3 per exercise)
- equipment_alternatives: Substitute equipment options (3 per exercise)
- technical_difficulty: Complexity rating 1-10
- training_age_min_months: Minimum experience required
- force_vector: Biomechanical classification
- sport_tags: Sport applicability tags
"""

EXERCISES_DATA = [
'''

footer = '''
]
'''

new_content = header + ',\n'.join(new_exercises) + footer

# Write the new file
with open('/workspace/src/forge/exercises_data.py', 'w') as f:
    f.write(new_content)

print(f"\n✅ Successfully integrated {len(new_exercises)} enriched exercises")
print(f"📁 Updated: /workspace/src/forge/exercises_data.py")
print(f"📊 File size: {len(new_content):,} characters")

# Verify the file is valid Python
try:
    with open('/workspace/src/forge/exercises_data.py', 'r') as f:
        exec(f.read())
    print("✅ File is valid Python syntax")
except Exception as e:
    print(f"❌ Syntax error: {e}")
