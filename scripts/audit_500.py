"""500-program audit: stratified random sampling across profiles."""
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.forge.models import (
    AthleteProfile, AthleteLevel, EquipmentProfile, SeasonPhase,
)
from src.forge.main import generate_program
from src.forge.renderer import render_program


SPORTS = ["rugby", "tennis", "soccer", "basketball", "track", "swimming", "american_football", "volleyball"]
GOALS = ["strength", "power", "hypertrophy", "conditioning", "mass", "speed", "power_maintenance", "return_to_sport"]
LEVELS = [AthleteLevel.BEGINNER, AthleteLevel.INTERMEDIATE, AthleteLevel.ADVANCED]
EQUIPMENTS = list(EquipmentProfile)
PHASES = list(SeasonPhase)
INJURIES = [["low_back"], ["acl_left"], ["shoulder"], ["hamstring"], []]


def random_profile():
    level = random.choice(LEVELS)
    training_age = {AthleteLevel.BEGINNER: (0, 1.5), AthleteLevel.INTERMEDIATE: (1, 4), AthleteLevel.ADVANCED: (3, 8)}
    lo, hi = training_age[level]
    injuries = random.choice(INJURIES)
    p = AthleteProfile(
        sport=random.choice(SPORTS),
        training_age_years=round(random.uniform(lo, hi), 1),
        season_phase=random.choice(PHASES),
        goal=random.choice(GOALS),
        equipment_profile=random.choice(EQUIPMENTS),
        athlete_level=level,
        technique_consistency=round(random.uniform(0.7, 1.0), 2),
        injury_status="none",
        injury_history=injuries,
        fatigue_level=random.choice(["normal", "high"]),
        weeks_since_break=0,
    )
    if level == AthleteLevel.ADVANCED and random.random() < 0.7:
        p.strength_base_met = True
    return p


def main():
    n = 500
    results = []
    failures = []

    for i in range(n):
        try:
            athlete = random_profile()
            program = generate_program(athlete)
            results.append(program)
        except Exception as e:
            failures.append((i, str(e)))

    total_sessions = sum(len(p.sessions) for p in results)
    total_blocks = sum(len(s.blocks) for p in results for s in p.sessions)
    empty_slots = sum(1 for p in results for s in p.sessions for b in s.blocks if not b.exercises)
    creds = [p.credibility_score for p in results]
    avg_cred = sum(creds) / len(creds) if creds else 0
    blueprints_used = set(p.blueprint_id for p in results)

    print(f"{'=' * 60}")
    print(f"500-PROGRAM AUDIT RESULTS")
    print(f"{'=' * 60}")
    print(f"Programs generated:  {len(results)}")
    print(f"Total sessions:      {total_sessions}")
    print(f"Total blocks:        {total_blocks}")
    print(f"Empty slots:         {empty_slots}")
    print(f"Crashes:             {len(failures)}")
    print(f"Blueprints used:     {len(blueprints_used)} ({sorted(blueprints_used)})")
    print(f"Average credibility: {avg_cred:.3f}/1.0 ({avg_cred*100:.1f}%)")
    print(f"Min credibility:     {min(creds):.2f}")
    print(f"Max credibility:     {max(creds):.2f}")
    p80 = sum(1 for c in creds if c >= 0.8)
    p90 = sum(1 for c in creds if c >= 0.9)
    print(f"Cred >=0.8:   {p80}/{len(creds)} ({p80/len(creds)*100:.0f}%)")
    print(f"Cred >=0.9:   {p90}/{len(creds)} ({p90/len(creds)*100:.0f}%)")

    if failures:
        print(f"\nFAILURES:")
        for idx, msg in failures:
            print(f"  Run {idx}: {msg}")

    creds_by_bp = {}
    for p in results:
        creds_by_bp.setdefault(p.blueprint_id, []).append(p.credibility_score)
    print(f"\nPer-blueprint credibility:")
    for bp_id in sorted(creds_by_bp):
        cs = creds_by_bp[bp_id]
        avg_c = sum(cs) / len(cs)
        print(f"  BP{bp_id:>2}: {avg_c:.3f} avg ({len(cs):>3} programs)")


if __name__ == "__main__":
    main()
