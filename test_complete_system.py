#!/usr/bin/env python3
"""
Test script to verify the complete FORGE system is working end-to-end.
This tests the API server and validates that real workout programs are generated.
"""

import requests
import json
import sys

API_URL = "http://127.0.0.1:8000"

def test_program_generation():
    """Test that the API generates complete workout programs."""
    
    test_cases = [
        {
            "name": "Rugby Prop - Strength Focus",
            "payload": {
                "mode": "core",
                "basics": {
                    "athlete_name": "Big Tom",
                    "age": 28,
                    "sex": "Male",
                    "sport": "Rugby Union",
                    "role": "Tighthead Prop",
                    "training_age_years": 8,
                    "level": "Advanced",
                    "environment": "Commercial Gym",
                    "available_minutes": 60,
                    "frequency_per_week": 4
                },
                "context": {
                    "primary_goal": "Max Force & Scrum Dominance",
                    "current_phase": "Off-Season",
                    "equipment_profile": ["Barbell", "Dumbbells", "Bands", "Sled"]
                },
                "advanced": {
                    "force_velocity_profile": "Force Deficit",
                    "squat_strength_band": "Elite (>2.0x BW)",
                    "injury_risk_flags": ["Neck", "Lower Back"]
                }
            }
        },
        {
            "name": "Basketball Guard - Power & Speed",
            "payload": {
                "mode": "core",
                "basics": {
                    "athlete_name": "Marcus Johnson",
                    "age": 22,
                    "sex": "Male",
                    "sport": "Basketball",
                    "role": "Point Guard",
                    "training_age_years": 5,
                    "level": "Intermediate",
                    "environment": "Commercial Gym",
                    "available_minutes": 45,
                    "frequency_per_week": 3
                },
                "context": {
                    "primary_goal": "Power & Speed",
                    "current_phase": "Pre-Season",
                    "equipment_profile": ["Barbell", "Dumbbells", "Bands", "Medicine Balls", "Box"]
                },
                "advanced": {
                    "force_velocity_profile": "Velocity Deficit",
                    "sprint_10m_band": "<1.65s",
                    "cmj_band": "High",
                    "injury_risk_flags": ["Ankle"]
                }
            }
        },
        {
            "name": "Tennis Player - Court Speed",
            "payload": {
                "mode": "core",
                "basics": {
                    "athlete_name": "Elena S.",
                    "age": 24,
                    "sex": "Female",
                    "sport": "Tennis",
                    "role": "Singles Player",
                    "training_age_years": 5,
                    "level": "Advanced",
                    "environment": "Commercial Gym",
                    "available_minutes": 45,
                    "frequency_per_week": 3
                },
                "context": {
                    "primary_goal": "Court Speed & Change of Direction",
                    "current_phase": "Pre-Season",
                    "equipment_profile": ["Dumbbells", "Kettlebells", "Cable Machine", "Medicine Balls"]
                },
                "advanced": {
                    "force_velocity_profile": "Velocity Deficit",
                    "sprint_10m_band": "<1.65s",
                    "aerobic_band": "Elite",
                    "injury_risk_flags": ["Right Shoulder", "Left Ankle"]
                }
            }
        }
    ]
    
    print("=" * 80)
    print("FORGE SYSTEM - END-TO-END TEST")
    print("=" * 80)
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n[Test {i}/3] {test_case['name']}")
        print("-" * 80)
        
        try:
            response = requests.post(
                f"{API_URL}/api/programs/generate",
                json=test_case["payload"],
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"❌ FAILED: HTTP {response.status_code}")
                print(f"Response: {response.text[:500]}")
                all_passed = False
                continue
            
            program = response.json()
            
            # Validate structure
            checks = {
                "Has metadata": "metadata" in program,
                "Has summary": "summary" in program,
                "Has weeks": "weeks" in program and len(program["weeks"]) > 0,
                "8-week program": len(program.get("weeks", [])) == 8,
                "Has sessions": all(len(w.get("sessions", [])) > 0 for w in program.get("weeks", [])),
                "Has exercises": any(
                    len(s.get("main_work", {}).get("exercises", [])) > 0
                    for w in program.get("weeks", [])
                    for s in w.get("sessions", [])
                ),
                "Has warmup": any(
                    len(s.get("warmup", {}).get("exercises", [])) > 0
                    for w in program.get("weeks", [])
                    for s in w.get("sessions", [])
                ),
                "Has credibility score": "credibility_score" in program.get("summary", {}),
                "Has blueprint": program.get("summary", {}).get("blueprint_selected"),
                "Has rationale": "rationale" in program and len(program["rationale"]) > 0,
                "Has personalization": "personalization_notes" in program and len(program["personalization_notes"]) > 0,
            }
            
            print(f"✓ Generated program with {len(program['weeks'])} weeks")
            print(f"✓ Blueprint: {program['summary'].get('blueprint_selected', 'N/A')}")
            print(f"✓ Credibility Score: {program['summary'].get('credibility_score', 'N/A')}")
            print(f"✓ Sessions per week: {[len(w['sessions']) for w in program['weeks'][:3]]}")
            
            # Count total exercises
            total_exercises = sum(
                len(s.get("main_work", {}).get("exercises", [])) +
                len(s.get("warmup", {}).get("exercises", [])) +
                len(s.get("conditioning", {}).get("exercises", []))
                for w in program["weeks"]
                for s in w["sessions"]
            )
            print(f"✓ Total exercises across all sessions: {total_exercises}")
            
            # Show sample session
            first_session = program["weeks"][0]["sessions"][0]
            print(f"\nSample Session (Week 1, Session 1):")
            print(f"  Name: {first_session['name']}")
            print(f"  Focus: {first_session.get('focus', 'N/A')}")
            print(f"  Warmup exercises: {len(first_session.get('warmup', {}).get('exercises', []))}")
            print(f"  Main work exercises: {len(first_session.get('main_work', {}).get('exercises', []))}")
            
            # Check validation
            if "validation" in program:
                print(f"  Validation messages: {len(program['validation'])}")
            
            all_checks_passed = all(checks.values())
            if all_checks_passed:
                print(f"\n✅ PASSED: All validation checks passed")
            else:
                print(f"\n⚠️  PARTIAL: Some checks failed:")
                for check, passed in checks.items():
                    if not passed:
                        print(f"   ❌ {check}")
                all_passed = False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ FAILED: Connection error - {e}")
            print("Make sure the API server is running: python run_forge_api.py")
            all_passed = False
        except Exception as e:
            print(f"❌ FAILED: {e}")
            import traceback
            traceback.print_exc()
            all_passed = False
    
    print("\n" + "=" * 80)
    if all_passed:
        print("✅ ALL TESTS PASSED - FORGE system is generating complete workout programs!")
        print("=" * 80)
        return 0
    else:
        print("⚠️  SOME TESTS HAD ISSUES - Review output above")
        print("=" * 80)
        return 1

if __name__ == "__main__":
    sys.exit(test_program_generation())
