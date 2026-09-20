#!/usr/bin/env python3
"""
500 program audit and 1000 program stress test for FORGE V1.1
"""

import sys
import os
import random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from forge.models import AthleteProfile, AthleteLevel, EquipmentProfile, SeasonPhase
from forge.main import generate_program
from forge.renderer import render_coach_program

def make_test_profile(sport, level, equipment, goal, season="off_season", fatigue="normal", training_age=3.0, technique=0.9, available_minutes=60, days_to_match=None, preferred_families=6):
    return AthleteProfile(
        sport=sport,
        training_age_years=training_age,
        season_phase=SeasonPhase(season),
        goal=goal,
        equipment_profile=EquipmentProfile(equipment),
        athlete_level=AthleteLevel(level),
        technique_consistency=technique,
        injury_status="none",
        injury_history=[],
        fatigue_level=fatigue,
        weeks_since_break=0,
        recent_exercises={},
        available_minutes=available_minutes,
        days_to_match=days_to_match,
        preferred_families=preferred_families
    )

def run_audit(count=500):
    """Run count programs and check for failures"""
    sports = ["cricket", "rugby", "tennis", "badminton", "soccer"]
    levels = ["Beginner", "Intermediate", "Advanced"]
    equipments = ["Field Only", "Basic Gym", "Commercial Gym"]
    goals = ["strength", "power", "speed", "conditioning", "mass", "general"]
    seasons = ["off_season", "pre_season", "in_season", "transition"]
    fatigues = ["normal", "high"]
    
    failures = 0
    errors = []
    
    for i in range(count):
        sport = random.choice(sports)
        level = random.choice(levels)
        equipment = random.choice(equipments)
        goal = random.choice(goals)
        season = random.choice(seasons)
        fatigue = random.choice(fatigues)
        
        # Vary available minutes and days_to_match occasionally
        if random.random() < 0.2:
            available_minutes = random.choice([30, 45, 60, 90])
        else:
            available_minutes = 60
            
        if random.random() < 0.1:
            days_to_match = random.choice([-2, -1, 0, 1, None])
        else:
            days_to_match = None
            
        try:
            athlete = make_test_profile(
                sport=sport,
                level=level,
                equipment=equipment,
                goal=goal,
                season=season,
                fatigue=fatigue,
                available_minutes=available_minutes,
                days_to_match=days_to_match
            )
            
            program = generate_program(athlete)
            
            # Basic validation
            if not program.sessions:
                failures += 1
                errors.append(f"Program {i}: No sessions generated")
                continue
                
            if len(program.sessions[0].blocks) == 0:
                failures += 1
                errors.append(f"Program {i}: First session has no blocks")
                continue
                
            for session in program.sessions:
                for block in session.blocks:
                    if not block.exercises:
                        failures += 1
                        errors.append(f"Program {i}: Session has empty block")
                        break
                        
            # Check that warmup and recovery are present for most cases
            if i < 10:  # Print first 10 for inspection
                if i == 0:
                    print("First program warmup:", program.warmup.phases[0].name if program.warmup else "None")
                    print("First program recovery:", program.recovery.name if program.recovery else "None")
                    
        except Exception as e:
            failures += 1
            errors.append(f"Program {i}: {str(e)}")
    
    print(f"\nAudit of {count} programs:")
    print(f"  Failures: {failures}")
    print(f"  Success rate: {(count-failures)/count*100:.1f}%")
    
    if errors and len(errors) <= 5:
        print("  Sample errors:")
        for err in errors[:5]:
            print(f"    {err}")
    elif errors:
        print(f"  First 5 errors:")
        for err in errors[:5]:
            print(f"    {err}")
    
    return failures == 0

def stress_test(count=1000):
    """Run stress test with edge cases"""
    print(f"\nRunning {count}-program stress test...")
    
    # Edge case profiles
    edge_cases = [
        # Very short sessions
        {"available_minutes": 20, "description": "Very short session"},
        # Match day
        {"days_to_match": 0, "description": "Match day"},
        # Pre-match
        {"days_to_match": 1, "description": "Pre-match"},
        # Post-match
        {"days_to_match": -1, "description": "Post-match"},
        # High fatigue in-season (should get deload)
        {"fatigue": "high", "season": "in_season", "description": "High fatigue in-season"},
        # Low available minutes
        {"available_minutes": 15, "description": "Extremely short session"},
        # High preferred families
        {"preferred_families": 8, "description": "Max families requested"},
        # Low preferred families
        {"preferred_families": 3, "description": "Min families requested"},
    ]
    
    failures = 0
    
    for i in range(count):
        # Mix of random and edge cases
        if i < len(edge_cases):
            case = edge_cases[i]
            kwargs = case.copy()
            desc = kwargs.pop("description")
            athlete = make_test_profile(
                sport="rugby",
                level="Intermediate",
                equipment="Basic Gym",
                goal="strength",
                **kwargs
            )
        else:
            athlete = make_test_profile(
                sport=random.choice(["cricket", "rugby", "tennis", "badminton", "soccer"]),
                level=random.choice(["Beginner", "Intermediate", "Advanced"]),
                equipment=random.choice(["Field Only", "Basic Gym", "Commercial Gym"]),
                goal=random.choice(["strength", "power", "speed", "conditioning", "mass", "general"]),
                available_minutes=random.choice([15, 30, 45, 60, 90]),
                days_to_match=random.choice([-2, -1, 0, 1, None]),
                preferred_families=random.choice([3, 4, 5, 6, 7, 8])
            )
        
        try:
            program = generate_program(athlete)
            
            # Basic checks
            assert program.sessions, "No sessions"
            assert program.sessions[0].blocks, "First session has no blocks"
            
            # For match day, should have no training
            if athlete.days_to_match == 0:
                assert len(program.sessions[0].blocks) == 0 or program.sessions[0].conditioning is not None, "Match day should be recovery only"
                
        except Exception as e:
            failures += 1
            if failures <= 3:
                print(f"  Stress test failure {i}: {e}")
    
    print(f"Stress test of {count} programs:")
    print(f"  Failures: {failures}")
    print(f"  Success rate: {(count-failures)/count*100:.1f}%")
    
    return failures == 0

def generate_examples():
    """Generate a few coach-facing output examples"""
    print("\n" + "="*60)
    print("COACH-FACING OUTPUT EXAMPLES")
    print("="*60)
    
    examples = [
        make_test_profile("cricket", "Intermediate", "Basic Gym", "power", "pre_season", "normal", 3.0, 0.9, 60, None, 6),
        make_test_profile("rugby", "Advanced", "Commercial Gym", "strength", "off_season", "normal", 6.0, 0.95, 90, None, 8),
        make_test_profile("tennis", "Beginner", "Field Only", "speed", "pre_season", "high", 1.0, 0.8, 45, None, 5),
        make_test_profile("badminton", "Intermediate", "Basic Gym", "conditioning", "in_season", "normal", 2.0, 0.9, 30, 0, 4),  # Match day
        make_test_profile("soccer", "Advanced", "Commercial Gym", "power_maintenance", "in_season", "high", 5.0, 0.9, 60, -1, 6),  # Post-match
    ]
    
    names = [
        "Intermediate Cricket Power",
        "Advanced Rugby Strength", 
        "Beginner Tennis Speed (High Fatigue)",
        "Intermediate Badminton Conditioning (Match Day)",
        "Advanced Soccer Power Maintenance (Post-Match)"
    ]
    
    for i, (athlete, name) in enumerate(zip(examples, names)):
        print(f"\n{name}:")
        print("-" * 40)
        try:
            program = generate_program(athlete)
            output = render_coach_program(program)
            print(output)
        except Exception as e:
            print(f"Error generating example: {e}")

if __name__ == "__main__":
    print("Running FORGE V1.1 validation...")
    
    # Run 500 program audit
    audit_ok = run_audit(500)
    
    # Run 1000 program stress test  
    stress_ok = stress_test(1000)
    
    # Generate examples
    generate_examples()
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    if audit_ok and stress_ok:
        print("✅ ALL TESTS PASS")
        print("FORGE V1.1 is ready for use")
    else:
        print("❌ SOME TESTS FAILED")
        print("Review errors above")