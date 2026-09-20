"""Quick test of API serializer."""
from src.forge.api_serializers import athlete_profile_from_request, serialize_program
from src.forge.main import generate_program

payload = {
    "mode": "core",
    "basics": {
        "athlete_name": "Test Athlete",
        "sport": "rugby",
        "level": "Intermediate",
        "frequency_per_week": 3,
        "available_minutes": 60,
    },
    "context": {"primary_goal": "strength"},
    "advanced": {},
}

profile = athlete_profile_from_request(payload)
program = generate_program(profile)
serialized = serialize_program(program, payload)

print(f"blueprint: {serialized['summary']['blueprint_selected']}")
print(f"sessions: {len(serialized['sessions'])}")
print(f"weeks: {len(serialized['weeks'])}")
print(f"rationale: {len(serialized['rationale'])} items")
print(f"personalization: {len(serialized['personalization_notes'])} items")
print(f"validation: {len(serialized['validation'])} items")

s0 = serialized["sessions"][0]
print(f"\nSession 0 keys: {list(s0.keys())}")
print(f"  warmup exercises: {len(s0['warmup']['exercises'])}")
print(f"  main work exercises: {len(s0['main_work']['exercises'])}")
print(f"  cond exercises: {len(s0['conditioning']['exercises'])}")
if s0["main_work"]["exercises"]:
    ex0 = s0["main_work"]["exercises"][0]
    print(f"  first exercise: {ex0['name']} {ex0['sets_reps']} {ex0['loading_method']} rest={ex0['rest']}")

print("\nALL KEYS present check:")
required = ["metadata", "summary", "weeks", "sessions", "rationale", "personalization_notes", "validation", "dropped_constraints"]
for k in required:
    if k in serialized:
        print(f"  + {k}")
    else:
        print(f"  - {k} MISSING")

print("\nTest passed!" if serialized["sessions"] else "\nFAILED: no sessions")
