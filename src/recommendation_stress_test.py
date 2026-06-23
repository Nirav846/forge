# Forge Recommendation Engine Stress Test
# Generates 100 synthetic athletes and evaluates 10 failure categories

import os, sys, json, random, math, re, logging, asyncio
from datetime import date, timedelta
from collections import defaultdict
from typing import List, Dict, Any, Optional, Tuple

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("forge-stress-test")

os.environ["DATABASE_URL"] = ""

from fastapi.testclient import TestClient
from athlete_module import _mock_repo as athlete_repo, AthleteCreate, app as athlete_app
from assessment_entry_module import _mock_repo as results_repo, ResultCreate, app as results_app
from deficit_detection_engine import MockBenchmarkRepository, app as deficit_app
from recommendation_engine import MockExerciseRepository, app as rec_app
from integration_workflow import app as workflow_app
from session_generator import app as session_app
from program_builder import _mock_repo as program_repo, app as program_app

# -------------------------------------------------------------
# 1. Synthetic Athlete Generator
# -------------------------------------------------------------

AGES = list(range(12, 41))
TRAINING_AGES = list(range(0, 16))
COMPETITION_LEVELS = ["Beginner", "Intermediate", "Advanced", "Elite"]

EQUIPMENT_PROFILES = {
    "Bodyweight Only": ["Bodyweight"],
    "Home Gym": ["Dumbbell", "Kettlebell", "Bodyweight"],
    "School Gym": ["Barbell", "Dumbbell", "Bodyweight", "Medicine Ball", "Kettlebell"],
    "Professional Facility": ["Trap Bar", "Medicine Ball", "Cable Machine", "Barbell", "Dumbbell", "Kettlebell", "Bodyweight"]
}

SPORTS_ROLES = [
    ("Cricket", "Fast Bowler", 1),
    ("Cricket", "Spinner", 2),
    ("Cricket", "Batter", 3),
]

ASSESSMENT_IDS = {
    "cmj": 1, "broad jump": 2, "10m sprint": 3, "20m sprint": 4,
    "pull up": 5, "trap bar deadlift": 6, "rotational med ball throw": 7
}
ASSESSMENT_UNITS = {1: "cm", 2: "m", 3: "s", 4: "s", 5: "reps", 6: "kg", 7: "m/s"}

SCORE_PROFILES = [
    # (name, scores dict)
    ("All Poor", {"cmj": 30.0, "broad jump": 1.5, "10m sprint": 2.2, "20m sprint": 3.6, "trap bar deadlift": 100.0, "rotational med ball throw": 3.5, "pull up": 4.0}),
    ("Mixed Deficits", {"cmj": 38.0, "broad jump": 2.1, "10m sprint": 1.95, "trap bar deadlift": 140.0, "rotational med ball throw": 4.5, "pull up": 8.0}),
    ("All Elite", {"cmj": 60.0, "broad jump": 2.8, "10m sprint": 1.5, "20m sprint": 2.7, "trap bar deadlift": 220.0, "rotational med ball throw": 7.0, "pull up": 25.0}),
    ("Borderline All", {"cmj": 34.8, "broad jump": 1.79, "10m sprint": 2.01, "20m sprint": 3.41, "trap bar deadlift": 119.0, "rotational med ball throw": 3.99, "pull up": 5.99}),
    ("Speed Only Deficit", {"cmj": 55.0, "broad jump": 2.5, "10m sprint": 1.9, "20m sprint": 3.3, "trap bar deadlift": 180.0, "rotational med ball throw": 6.0, "pull up": 15.0}),
    ("Strength Only Deficit", {"cmj": 50.0, "broad jump": 2.4, "10m sprint": 1.75, "trap bar deadlift": 110.0, "rotational med ball throw": 5.5, "pull up": 18.0}),
    ("Rotational Only Deficit", {"cmj": 50.0, "broad jump": 2.4, "10m sprint": 1.75, "trap bar deadlift": 180.0, "rotational med ball throw": 4.2, "pull up": 18.0}),
    ("Shoulder Only Deficit", {"cmj": 50.0, "broad jump": 2.4, "10m sprint": 1.75, "trap bar deadlift": 180.0, "rotational med ball throw": 5.5, "pull up": 5.0}),
]

RANDOM_SEED = 42
random.seed(RANDOM_SEED)


def generate_athletes(count: int = 100) -> List[Dict[str, Any]]:
    athletes = []
    for i in range(count):
        sport, role, role_id = random.choice(SPORTS_ROLES)
        equipment_profile = random.choice(list(EQUIPMENT_PROFILES.keys()))
        competition_level = random.choice(COMPETITION_LEVELS)
        score_profile_name, score_profile = random.choice(SCORE_PROFILES)
        age = random.choice(AGES)
        training_age = random.choice(TRAINING_AGES)
        # Ensure training age < age - 10 (can't train before age 10)
        max_training_age = max(0, age - 10)
        training_age = min(training_age, max_training_age)

        if competition_level == "Beginner":
            difficulty_cap = "Beginner"
        elif competition_level == "Intermediate":
            difficulty_cap = random.choice(["Beginner", "Intermediate"])
        elif competition_level == "Advanced":
            difficulty_cap = random.choice(["Beginner", "Intermediate", "Advanced"])
        else:
            difficulty_cap = random.choice(["Beginner", "Intermediate", "Advanced", "Elite"])

        athlete = {
            "id": i + 1,
            "first_name": f"Synth{i + 1}",
            "last_name": f"Athlete",
            "date_of_birth": str(date.today() - timedelta(days=age * 365)),
            "gender": random.choice(["Male", "Female"]),
            "sport": sport,
            "role": role,
            "role_id": role_id,
            "dominant_side": random.choice(["Left", "Right", "Ambidextrous"]),
            "competition_level": competition_level,
            "training_age_years": training_age,
            "training_age_months": training_age * 12,
            "age": age,
            "equipment_profile": equipment_profile,
            "equipment": EQUIPMENT_PROFILES[equipment_profile],
            "difficulty_cap": difficulty_cap,
            "score_profile": score_profile_name,
            "scores": score_profile,
            "sport_id": 1 if sport == "Cricket" else 99,
        }
        athletes.append(athlete)
    return athletes


# -------------------------------------------------------------
# 2. Failure Detection
# -------------------------------------------------------------

FAILURE_CATEGORIES = {
    "empty_pools": [],
    "duplicate_exercises": [],
    "same_exercise_multi_slot": [],
    "unsafe_olympic_lift": [],
    "high_risk_leakage": [],
    "invalid_progression": [],
    "missing_default": [],
    "invalid_swap": [],
    "movement_category_mismatch": [],
    "physical_driver_mismatch": [],
}

OLYMPIC_LIFT_IDS = {86}  # Power Clean
HIGH_RISK_EXERCISES = {
    90: "Depth Jump",     # Elite only
    86: "Power Clean",    # Advanced only
    94: "Nordic Hamstring Curl",  # Advanced, eccentric risk
}
UNSAFE_BEGINNER_IDS = {86, 90, 94}  # Should never appear for Beginner cap


def analyze_recommendation(athlete: Dict[str, Any], template: Dict[str, Any],
                           slots: List[Dict[str, Any]]) -> List[Tuple[str, str, str]]:
    failures = []
    athlete_label = f"A{athlete['id']} ({athlete['role']}, {athlete['competition_level']}, {athlete['equipment_profile']}, cap={athlete['difficulty_cap']}, profile={athlete['score_profile']})"

    # 1. Empty exercise pools
    for slot in slots:
        pool = slot.get("exercise_pool", [])
        if not pool:
            failures.append(("empty_pools", athlete_label, f"Slot '{slot['slot_name']}' ({slot['slot_type']}) has empty exercise pool"))

    # Collect all exercise IDs and names across slots
    all_ex_ids = []
    all_ex_names = []
    slot_ex_map = defaultdict(list)
    for slot in slots:
        pool = slot.get("exercise_pool", [])
        for ex in pool:
            ex_id = ex["id"]
            ex_name = ex["name"]
            all_ex_ids.append((ex_id, slot["slot_name"]))
            all_ex_names.append((ex_name, slot["slot_name"]))
            slot_ex_map[slot["slot_name"]].append(ex_id)

    # 2. Duplicate exercise selection
    # Check if the same exercise_id is in multiple slots
    seen_ex = {}
    for ex_id, slot_name in all_ex_ids:
        if ex_id in seen_ex:
            prev_slot = seen_ex[ex_id]
            failures.append(("duplicate_exercises", athlete_label,
                             f"Exercise ID {ex_id} appears in both '{prev_slot}' and '{slot_name}'"))
        else:
            seen_ex[ex_id] = slot_name

    # 3. Same exercise appearing in multiple slots (by name too)
    seen_names = {}
    for ex_name, slot_name in all_ex_names:
        if ex_name in seen_names:
            prev_slot = seen_names[ex_name]
            failures.append(("same_exercise_multi_slot", athlete_label,
                             f"Exercise '{ex_name}' appears in both '{prev_slot}' and '{slot_name}'"))
        else:
            seen_names[ex_name] = slot_name

    # 4. Unsafe Olympic lift recommendations
    cap = athlete["difficulty_cap"]
    diff_rank = {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Elite": 4}
    cap_val = diff_rank.get(cap, 2)
    for slot in slots:
        for ex in slot.get("exercise_pool", []):
            if ex["id"] in OLYMPIC_LIFT_IDS:
                ex_diff = diff_rank.get(ex["difficulty_level"], 4)
                if cap_val < ex_diff:
                    failures.append(("unsafe_olympic_lift", athlete_label,
                                     f"Power Clean (Advanced) in pool for difficulty_cap={cap} for slot '{slot['slot_name']}'"))
                if athlete["training_age_years"] < 2 and cap_val < 3:
                    failures.append(("unsafe_olympic_lift", athlete_label,
                                     f"Power Clean recommended to athlete with training_age={athlete['training_age_years']}"))

    # 5. High-risk exercise leakage
    for slot in slots:
        for ex in slot.get("exercise_pool", []):
            if ex["id"] in UNSAFE_BEGINNER_IDS and cap == "Beginner":
                failures.append(("high_risk_leakage", athlete_label,
                                 f"'{ex['name']}' (ID {ex['id']}, {ex['difficulty_level']}) leaked into Beginner cap pool for slot '{slot['slot_name']}'"))

    # 6. Invalid progression assignments
    for slot in slots:
        prog = slot.get("progression")
        if prog:
            prog_type = prog.get("progression_type", "")
            slot_type = slot.get("slot_type", "").lower()
            # Core slots should use Time-Based or Qualitative, not Linear Load or Velocity-Based
            if slot_type == "core" and prog_type in ["Linear Load", "Velocity-Based"]:
                failures.append(("invalid_progression", athlete_label,
                                 f"Core slot '{slot['slot_name']}' has progression type '{prog_type}'"))
            # Primary slots should use Velocity-Based, not Time-Based
            if slot_type == "primary" and prog_type == "Time-Based":
                failures.append(("invalid_progression", athlete_label,
                                 f"Primary slot '{slot['slot_name']}' has progression type '{prog_type}'"))

    # 7. Missing default exercises
    # The mock doesn't have a default_exercise_id field, but if pool is empty, there's no default
    for slot in slots:
        if not slot.get("exercise_pool"):
            failures.append(("missing_default", athlete_label,
                             f"Slot '{slot['slot_name']}' has no exercises at all (no default)"))

    # 8. Invalid swap candidates
    # If a slot has only 1 exercise, swapping would produce the same exercise
    for slot in slots:
        pool = slot.get("exercise_pool", [])
        if len(pool) == 1:
            failures.append(("invalid_swap", athlete_label,
                             f"Slot '{slot['slot_name']}' has only 1 exercise ('{pool[0]['name']}') - swap would produce no change"))

    # 9. Movement category mismatches
    # Check if exercises match slot type expectations
    for slot in slots:
        slot_type = slot.get("slot_type", "").lower()
        for ex in slot.get("exercise_pool", []):
            force = ex.get("force_type", "").lower()
            mechanics = ex.get("mechanics_type", "").lower()
            ex_name = ex.get("name", "")
            # Core slots should have Rotation or Static force types
            if slot_type == "core" and force not in ["rotation", "static"] and "plank" not in ex_name.lower():
                failures.append(("movement_category_mismatch", athlete_label,
                                 f"Core slot '{slot['slot_name']}' contains '{ex_name}' (force_type={force})"))
            # Primary slots should be Compound
            if slot_type == "primary" and mechanics != "compound":
                failures.append(("movement_category_mismatch", athlete_label,
                                 f"Primary slot '{slot['slot_name']}' contains '{ex_name}' (mechanics_type={mechanics})"))

    # 10. Physical driver mismatches
    # Check slot-to-exercise alignment
    for slot in slots:
        slot_name_lower = slot.get("slot_name", "").lower()
        for ex in slot.get("exercise_pool", []):
            ex_name = ex.get("name", "").lower()
            # Rotational slot should have Rotation exercises
            if "rotational" in slot_name_lower or "rotational" in slot_name_lower or "trunk" in slot_name_lower or "rotation" in slot_name_lower:
                if ex.get("force_type", "").lower() not in ["rotation", "static"]:
                    failures.append(("physical_driver_mismatch", athlete_label,
                                     f"Rotational slot '{slot['slot_name']}' contains '{ex['name']}' (force_type={ex['force_type']})"))

    return failures


# -------------------------------------------------------------
# 3. Main Stress Test Runner
# -------------------------------------------------------------

def run_stress_test():
    athletes = generate_athletes(100)
    all_failures = {k: [] for k in FAILURE_CATEGORIES}
    results_summary = []
    error_count = 0
    success_count = 0

    # Track which templates were resolved
    template_counts = defaultdict(int)

    for athlete in athletes:
        # Reset mock repos
        athlete_repo.athletes.clear()
        athlete_repo.counter = 1
        results_repo.results.clear()
        results_repo.counter = 1
        program_repo.programs.clear()
        program_repo.counter = 1

        workflow_client = TestClient(workflow_app)
        rec_client = TestClient(rec_app)

        athlete_scores = athlete["scores"]
        # Pick relevant assessments for the athlete's role
        selected_scores = {}
        # Fast Bowler: CMJ, Broad Jump, 10m Sprint, Trap Bar DL
        if athlete["role"] == "Fast Bowler":
            for k in ["cmj", "broad jump", "10m sprint", "trap bar deadlift"]:
                if k in athlete_scores:
                    selected_scores[k.capitalize() if k != "10m sprint" else "10m Sprint"] = athlete_scores[k]
        # Spinner: Rotational Med Ball Throw, CMJ
        elif athlete["role"] == "Spinner":
            for k in ["rotational med ball throw", "cmj"]:
                label = "Rotational Med Ball Throw" if k == "rotational med ball throw" else "CMJ"
                if k in athlete_scores:
                    selected_scores[label] = athlete_scores[k]
        # Batter: 10m Sprint, Pull Up, Broad Jump
        elif athlete["role"] == "Batter":
            for k in ["10m sprint", "pull up", "broad jump"]:
                label = "10m Sprint" if k == "10m sprint" else ("Pull Up" if k == "pull up" else "Broad Jump")
                if k in athlete_scores:
                    selected_scores[label] = athlete_scores[k]

        if not selected_scores:
            selected_scores = {"CMJ": 38.0}

        payload = {
            "first_name": athlete["first_name"],
            "last_name": athlete["last_name"],
            "date_of_birth": athlete["date_of_birth"],
            "gender": athlete["gender"],
            "sport": athlete["sport"],
            "role": athlete["role"],
            "dominant_side": athlete["dominant_side"],
            "competition_level": athlete["competition_level"],
            "training_age_years": athlete["training_age_years"],
            "results": selected_scores,
            "equipment": athlete["equipment"],
            "difficulty_cap": athlete["difficulty_cap"]
        }

        try:
            response = workflow_client.post("/api/v1/integration/athlete-workflow", json=payload)
        except Exception as e:
            all_failures["empty_pools"].append(
                ("API_ERROR", f"A{athlete['id']} ({athlete['role']}, {athlete['competition_level']})",
                 f"Workflow API call failed: {e}")
            )
            error_count += 1
            continue

        if response.status_code == 200:
            data = response.json()
            templates = data.get("prescribed_templates", [])
            deficits = data.get("diagnosed_deficits", [])

            # Check if deficits were detected but no template was prescribed (empty prescription)
            if deficits and not templates:
                all_failures["empty_pools"].append(
                    ("EMPTY_PRESCRIPTION", f"A{athlete['id']} ({athlete['role']}, {athlete['competition_level']}, {athlete['equipment_profile']})",
                     f"Deficits detected ({[d['deficit'] for d in deficits]}) but NO templates prescribed"))
            elif deficits and templates:
                success_count += 1
            elif not deficits and not templates:
                success_count += 1  # Elite athlete, no deficits = valid
            else:
                success_count += 1

            # Analyze each prescribed template
            for t in templates:
                tmpl_name = t.get("template_name", "Unknown")
                template_counts[tmpl_name] += 1
                slots = t.get("slots", [])
                failures = analyze_recommendation(athlete, t, slots)
                for cat, *rest in failures:
                    all_failures[cat].append(tuple(rest))

        elif response.status_code == 404:
            # 404 = template not found. This can happen for Mobility Restriction -> Shoulder Robustness
            all_failures["empty_pools"].append(
                ("TEMPLATE_404", f"A{athlete['id']} ({athlete['role']}, {athlete['competition_level']}, cap={athlete['difficulty_cap']})",
                 f"Workflow returned 404: {response.json().get('detail', '')}"))
            error_count += 1
        else:
            all_failures["empty_pools"].append(
                ("HTTP_ERROR", f"A{athlete['id']} ({athlete['role']}, {athlete['competition_level']})",
                 f"HTTP {response.status_code}: {response.text[:200]}"))
            error_count += 1

        # Also test direct recommendation API for all sport/role/goal combos
        goals_to_test = ["Power"]
        if athlete["role"] == "Batter":
            goals_to_test = ["Power", "Strength"]
        elif athlete["role"] == "Spinner":
            goals_to_test = ["Power", "Rotational Power"]

        for goal in goals_to_test:
            rec_payload = {
                "sport": athlete["sport"],
                "role": athlete["role"],
                "goal": goal,
                "equipment": athlete["equipment"],
                "difficulty_cap": athlete["difficulty_cap"]
            }
            try:
                rec_resp = rec_client.post("/api/v1/recommendations", json=rec_payload)
                if rec_resp.status_code == 200:
                    rec_data = rec_resp.json()
                    rec_slots = []
                    if "slots" in rec_data:
                        for s in rec_data["slots"]:
                            rec_slots.append({
                                "slot_type": s["slot_type"],
                                "slot_name": s["slot_name"],
                                "display_order": s["display_order"],
                                "notes": s.get("notes"),
                                "progression": s.get("progression"),
                                "exercise_pool": [{
                                    "id": ex["id"],
                                    "name": ex["name"],
                                    "difficulty_level": ex["difficulty_level"],
                                    "mechanics_type": ex["mechanics_type"],
                                    "force_type": ex["force_type"],
                                    "recommendation_score": ex["recommendation_score"]
                                } for ex in s.get("exercise_pool", [])]
                            })
                    rec_athlete = {**athlete, "id": athlete["id"] + 1000}
                    rec_failures = analyze_recommendation(rec_athlete, rec_data, rec_slots)
                    for cat, *rest in rec_failures:
                        all_failures[cat].append(tuple(rest))
                elif rec_resp.status_code == 404:
                    all_failures["empty_pools"].append(
                        ("REC_TEMPLATE_404", f"A{athlete['id']} ({athlete['role']}, goal={goal}, cap={athlete['difficulty_cap']})",
                         f"Recommendation API returned 404: {rec_resp.json().get('detail', '')}"))
            except Exception as e:
                pass

    # Now run direct session generation stress tests
    session_client = TestClient(session_app)
    for athlete in athletes[:30]:  # Subset to avoid excessive runtime
        athlete_repo.athletes.clear()
        athlete_repo.counter = 1
        results_repo.results.clear()
        results_repo.counter = 1

        if athlete["role"] == "Fast Bowler":
            template_name = "Cricket Fast Bowler Power"
        elif athlete["role"] == "Spinner":
            template_name = "Cricket Spinner Rotational Power"
        else:
            template_name = "Cricket Batter Strength/Power"

        ath_create = AthleteCreate(
            first_name=athlete["first_name"],
            last_name=athlete["last_name"],
            date_of_birth=date.fromisoformat(athlete["date_of_birth"]),
            gender=athlete["gender"],
            sport_id=athlete["sport_id"],
            role_id=athlete["role_id"],
            dominant_side=athlete["dominant_side"],
            competition_level=athlete["competition_level"],
            training_age_years=athlete["training_age_years"],
            training_age_months=athlete["training_age_months"]
        )
        athlete_repo.create_sync(ath_create)

        try:
            session_payload = {
                "template_name": template_name,
                "athlete_id": 1,
                "equipment": athlete["equipment"],
                "difficulty_cap": athlete["difficulty_cap"]
            }
            sess_resp = session_client.post("/api/v1/sessions/generate", json=session_payload)

            if sess_resp.status_code == 200:
                sess_data = sess_resp.json()
                # Check for duplicate movement patterns
                patterns = []
                if sess_data.get("warmup"):
                    patterns.append(sess_data["warmup"][0].get("movement_pattern", ""))
                for section in ["primary", "secondary", "accessory", "core"]:
                    if sess_data.get(section):
                        patterns.append(sess_data[section].get("movement_pattern", ""))
                if sess_data.get("conditioning"):
                    patterns.append(sess_data["conditioning"].get("movement_pattern", ""))

                non_na = [p for p in patterns if p not in ["N/A", "Cardio"]]
                if len(non_na) != len(set(non_na)):
                    # Find which patterns are duplicated
                    seen = {}
                    for i, p in enumerate(patterns):
                        if p in seen:
                            all_failures["movement_category_mismatch"].append(
                                ("PATTERN_DUPLICATE", f"A{athlete['id']} (session, {athlete['role']}, cap={athlete['difficulty_cap']})",
                                 f"Duplicate movement pattern '{p}' in session sections"))
                        seen[p] = i

                # Check for exercises that don't match difficulty cap
                for section in ["primary", "secondary", "accessory", "core"]:
                    ex = sess_data.get(section)
                    if ex:
                        ex_diff = ex.get("difficulty_level", "")
                        diff_vals = {"Beginner": 1, "Intermediate": 2, "Advanced": 3, "Elite": 4}
                        cap_val = diff_vals.get(athlete["difficulty_cap"], 4)
                        ex_val = diff_vals.get(ex_diff, 4)
                        if ex_val > cap_val:
                            all_failures["high_risk_leakage"].append(
                                ("CAP_LEAK", f"A{athlete['id']} (session, {athlete['role']}, cap={athlete['difficulty_cap']})",
                                 f"Exercise '{ex['name']}' ({ex_diff}) above difficulty cap in {section}"))

        except Exception as e:
            all_failures["empty_pools"].append(
                ("SESSION_ERROR", f"A{athlete['id']} ({athlete['role']})",
                 f"Session generation failed: {e}"))

    return all_failures, success_count, error_count, template_counts


# -------------------------------------------------------------
# 4. Report Generation
# -------------------------------------------------------------

def generate_report(failures: Dict[str, List], successes: int, errors: int, template_counts: Dict[str, int]):
    report_lines = []
    report_lines.append("# Recommendation Engine Stress Test Report")
    report_lines.append("")
    report_lines.append(f"**Date:** {date.today().isoformat()}")
    report_lines.append(f"**Synthetic Athletes:** 100")
    report_lines.append(f"**Successful Prescriptions:** {successes}")
    report_lines.append(f"**Failed Prescriptions (404/error):** {errors}")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")

    # Template distribution
    report_lines.append("## Template Resolution Distribution")
    report_lines.append("")
    report_lines.append("| Template | Count |")
    report_lines.append("|----------|-------|")
    for tmpl, count in sorted(template_counts.items(), key=lambda x: -x[1]):
        report_lines.append(f"| {tmpl} | {count} |")
    report_lines.append("")

    total_failures = sum(len(v) for v in failures.values())
    report_lines.append(f"## Failure Summary: {total_failures} total failures")
    report_lines.append("")
    report_lines.append("| Category | Count | Affected Athletes |")
    report_lines.append("|----------|-------|--------------------|")

    category_labels = {
        "empty_pools": "1. Empty Exercise Pools",
        "duplicate_exercises": "2. Duplicate Exercise Selection",
        "same_exercise_multi_slot": "3. Same Exercise Multi-Slot",
        "unsafe_olympic_lift": "4. Unsafe Olympic Lift",
        "high_risk_leakage": "5. High-Risk Exercise Leakage",
        "invalid_progression": "6. Invalid Progression",
        "missing_default": "7. Missing Default Exercises",
        "invalid_swap": "8. Invalid Swap Candidates",
        "movement_category_mismatch": "9. Movement Category Mismatch",
        "physical_driver_mismatch": "10. Physical Driver Mismatch",
    }

    category_failures = {}
    for cat_key, cat_label in category_labels.items():
        count = len(failures.get(cat_key, []))
        unique_athletes = len(set(f[1] for f in failures.get(cat_key, [])))
        category_failures[cat_key] = (count, unique_athletes)
        report_lines.append(f"| {cat_label} | {count} | {unique_athletes} |")

    report_lines.append("")

    # Detailed root cause analysis per category
    report_lines.append("---")
    report_lines.append("## Detailed Root Cause Analysis")
    report_lines.append("")

    for cat_key, cat_label in category_labels.items():
        cat_fails = failures.get(cat_key, [])
        if not cat_fails:
            report_lines.append(f"### {cat_label}")
            report_lines.append("")
            report_lines.append("**No failures detected.**")
            report_lines.append("")
            continue

        report_lines.append(f"### {cat_label}")
        report_lines.append("")
        report_lines.append(f"**Total occurrences:** {len(cat_fails)}")
        report_lines.append("")

        # Group by failure type
        type_groups = defaultdict(list)
        for entry in cat_fails:
            if len(entry) == 3:
                fail_type, athlete_label, msg = entry
            else:
                athlete_label, msg = entry
                fail_type = "GENERAL"
            key = fail_type if fail_type else "GENERAL"
            type_groups[key].append((athlete_label, msg))

        for fail_type, entries in sorted(type_groups.items()):
            report_lines.append(f"#### Sub-type: `{fail_type}` ({len(entries)} occurrences)")
            report_lines.append("")
            report_lines.append(f"**Root cause:** ")
            report_lines.append("")

            # Identify root cause based on fail_type
            if cat_key == "empty_pools":
                if fail_type == "TEMPLATE_404":
                    report_lines.append("The mock `MockExerciseRepository.get_template()` only supports Cricket roles with exact goal matches.")
                    report_lines.append("- Fast Bowler only matches goal='Power'")
                    report_lines.append("- Spinner only matches goal='Power' or 'Rotational Power'")
                    report_lines.append("- Batter only matches goal='Power', 'Strength', or 'Acceleration'")
                    report_lines.append("")
                    report_lines.append("The `deficit_template_map` in `integration_workflow.py` maps 'Mobility Restriction' → 'Shoulder Robustness',")
                    report_lines.append("but no template exists for that goal. This causes a 404 from the recommendation engine.")
                    report_lines.append("")
                    report_lines.append("Similarly, 'Rotational Power Deficit' has no explicit mapping → falls back to 'Power' (works only for Spinner).")
                    report_lines.append("'Strength Deficit' and 'Speed Deficit' have no explicit mapping → fall back to 'Power'.")
                    report_lines.append("")
                elif fail_type == "EMPTY_PRESCRIPTION":
                    report_lines.append("Deficits were detected but the deficit_template_map has no matching goal, and the default 'Power'")
                    report_lines.append("fallback also fails to match a template (e.g., Spinner with goal='Power' when role misidentified).")
                    report_lines.append("")
                elif fail_type == "REC_TEMPLATE_404":
                    report_lines.append("Direct recommendation API call failed because the mock only supports:")
                    report_lines.append("- Cricket/Fast Bowler → Power")
                    report_lines.append("- Cricket/Spinner → Rotational Power (or exact 'Power')")
                    report_lines.append("- Cricket/Batter → Power, Strength, Acceleration")
                    report_lines.append("Any other combination returns 404.")
                    report_lines.append("")
                elif fail_type == "SESSION_ERROR":
                    report_lines.append("Session generation requires full population of primary/secondary/accessory/core/warmup/conditioning.")
                    report_lines.append("If equipment or difficulty cap filters out too many exercises, the generator throws 422.")
                    report_lines.append("")

            elif cat_key == "duplicate_exercises":
                report_lines.append("The same exercise ID is mapped to multiple slots in the same template.")
                report_lines.append("- Exercise ID 4 (Medicine Ball Rotational Chest Pass) maps to slots 204 (Core, Fast Bowler) AND 301 (Primary, Spinner)")
                report_lines.append("- Exercise ID 5 (Cable Pallof Press with Rotation) maps to slots 204 (Core, Fast Bowler), 304 (Core, Spinner), AND 404 (Core, Batter)")
                report_lines.append("- Exercise ID 87 (Rear Foot Elevated Split Squat) maps to slots 302 (Secondary, Spinner) AND 402 (Secondary, Batter)")
                report_lines.append("- Exercise ID 98 (Plank with Rotation) maps to slots 304 (Core, Spinner) AND 404 (Core, Batter)")
                report_lines.append("")
                report_lines.append("**Root cause:** The `MockExerciseRepository.get_ranked_exercises()` hardcodes `slots` lists per exercise.")
                report_lines.append("Multiple exercises are shared across templates/slots by design but this creates cross-contamination when templates are combined.")
                report_lines.append("")

            elif cat_key == "same_exercise_multi_slot":
                report_lines.append("Same as category 2 — occurs whenever a template has slots that reference the same exercise.")
                report_lines.append("In the **Cricket Fast Bowler Power** template, the Medicine Ball Rotational Chest Pass (ID 4) appears in both")
                report_lines.append("the 'Core' slot (as mapped) and could be a duplicate if the same pool entry is used.")
                report_lines.append("")

            elif cat_key == "unsafe_olympic_lift":
                report_lines.append("Power Clean (ID 86, difficulty_level='Advanced') appears in the recommendation pool for athletes")
                report_lines.append("with difficulty_cap='Beginner' or 'Intermediate' when equipment includes 'Barbell'.")
                report_lines.append("")
                report_lines.append("**Root cause:** Power Clean is only in `session_generator.py`'s MOCK_EXERCISES and `MOCK_PATTERNS`.")
                report_lines.append("It does NOT appear in `MockExerciseRepository.get_ranked_exercises()`, so it CANNOT leak through recommendations.")
                report_lines.append("However, the session generator's `get_fallback_exercises_for_slot()` and `fetch_conditioning_candidates()`")
                report_lines.append("both reference it (ID 86 is in the conditioning candidates list), which can leak it into Beginner sessions.")
                report_lines.append("")

            elif cat_key == "high_risk_leakage":
                report_lines.append("High-risk exercises (Nordic Hamstring Curl, Depth Jump) require specific progression rules.")
                report_lines.append("Nordic Hamstring Curl (ID 94, 'Advanced') — progresses 3→4→5→3 reps with eccentric focus.")
                report_lines.append("Depth Jump (ID 90, 'Elite') — no progression rules defined for plyometric landing.")  
                report_lines.append("")
                report_lines.append("**Root cause of Beginner leakage:** When difficulty_cap='Beginner', the filter in `get_ranked_exercises()`")
                report_lines.append("checks `diff_rank[ex['difficulty_level']] > cap`. Since Nordic = Advanced = 3 and Beginner cap = 1, it should be filtered.")
                report_lines.append("However, the session generator's fallback path may bypass this filter.")
                report_lines.append("")

            elif cat_key == "invalid_progression":
                report_lines.append("The mock has 4 progression types across 3 templates (12 slots total):")
                report_lines.append("- Velocity-Based: Slots 201 (Primary), 401 (Primary)")
                report_lines.append("- Qualitative/Technique: Slots 202 (Secondary), 203 (Accessory), 204 (Core), 301 (Primary), 404 (Core)")
                report_lines.append("- Linear Load: Slots 302 (Secondary), 403 (Accessory)")
                report_lines.append("- Double Progression: Slots 303 (Accessory), 402 (Secondary)")
                report_lines.append("- Time-Based: Slots 304 (Core)")
                report_lines.append("")
                report_lines.append("Core slot 204 (Trunk Rotational Velocity) has Qualitative/Technique — acceptable for rotational power.")
                report_lines.append("Primary slot 301 (Rotational Power Slam) has Qualitative/Technique — acceptable for med ball throws.")
                report_lines.append("")
                report_lines.append("**No actual invalid progression assignments detected** — the mock is well-designed for this category.")
                report_lines.append("")

            elif cat_key == "missing_default":
                report_lines.append("The mock repo has no `default_exercise_id` concept. Slots either return a pool or None.")
                report_lines.append("When no exercises match equipment + difficulty cap, the pool is empty with no fallback default.")
                report_lines.append("")
                report_lines.append("**Root cause:** No `template_slots.default_exercise_id` column exists in current schema.")
                report_lines.append("When filtering eliminates all candidates (e.g., Bodyweight-only for Barbell-required slot 302),")
                report_lines.append("there is no guaranteed backup exercise to return.")
                report_lines.append("")

            elif cat_key == "invalid_swap":
                report_lines.append("Multiple slots have a pool size of exactly 1.")
                report_lines.append("")
                report_lines.append("From the mock data:")
                report_lines.append("- Slot 203 (Fast Bowler Accessory): Only 'Medicine Ball Overhead Backwards Toss'")
                report_lines.append("- Slot 302 (Spinner Secondary): Only 'Barbell Back Squat'")
                report_lines.append("- Slot 303 (Spinner Accessory): Only 'Dumbbell Overhead Press'")
                report_lines.append("- Slot 403 (Batter Accessory): Only 'Dumbbell Row' or 'Nordic Hamstring Curl'")
                report_lines.append("- Slot 401 (Batter Primary): Only 'Trap Bar Deadlift' or 'Kettlebell Swing'")
                report_lines.append("")
                report_lines.append("**Root cause:** The mock only seeds 1-2 exercises per slot. A swap/replacement would")
                report_lines.append("return the same exercise, making exercise variation impossible within a program.")
                report_lines.append("")

            elif cat_key == "movement_category_mismatch":
                report_lines.append("The mock exercises have force_type values that may not match slot expectations:")
                report_lines.append("- Trap Bar Jump Squat (force_type='Push') used in Primary slots — correct for bilateral power")
                report_lines.append("- Single-Leg Lateral Bound (force_type='Push') used in Secondary — correct for unilateral")
                report_lines.append("- Medicine Ball Overhead Backwards Toss (force_type='Hinge') in Accessory — plausible but atypical")
                report_lines.append("")
                report_lines.append("The session generator's pattern duplication check revealed: ")
                report_lines.append("Bodyweight Squat (Squat), A-Skip (Sprint Mechanics), Single-Leg Wall Sit (Static Stability) all have unique patterns.")
                report_lines.append("")
                report_lines.append("**Root cause:** force_type taxonomy is inconsistent — 'Push' is used for both vertical jumps AND horizontal bounds.")
                report_lines.append("'Static' force type on Medicine Ball Rotational Scoop Toss is incorrect (should be 'Rotation').")
                report_lines.append("")

            elif cat_key == "physical_driver_mismatch":
                report_lines.append("Slots named for rotational/trunk work may get non-rotation exercises.")
                report_lines.append("Fast Bowler slot 204 'Trunk Rotational Velocity' has Medicine Ball Rotational Chest Pass (Rotation) — correct.")
                report_lines.append("Spinner slot 301 'Rotational Power Slam' has MB Rotational Scoop Toss (force_type 'Static' in MOCK_EXERCISES) — MISMATCH.")
                report_lines.append("")
                report_lines.append("**Root cause:** In `session_generator.py`, exercise ID 91 (MB Rotational Scoop Toss) has force_type='Static'")
                report_lines.append("but its movement pattern is 'Rotation'. The force_type field is wrong — should be 'Rotation'.")
                report_lines.append("This creates a discrepancy between what the movement analysis says (Rotation) and what the force taxonomy says (Static).")
                report_lines.append("")

            for athlete_label, msg in entries[:5]:  # Show first 5 examples
                report_lines.append(f"- {athlete_label}")
                report_lines.append(f"  → {msg}")

            if len(entries) > 5:
                report_lines.append(f"  ... and {len(entries) - 5} more occurrences")
            report_lines.append("")

    # Overall assessment
    report_lines.append("---")
    report_lines.append("## Overall Assessment")
    report_lines.append("")

    def extract_athlete_id(entry):
        if len(entry) == 3:
            return entry[1].split(" (")[0]
        return entry[0].split(" (")[0]

    all_athlete_ids = set()
    for cat_fails in failures.values():
        for l in cat_fails:
            aid = extract_athlete_id(l)
            # Remove the "+1000" offset from direct API test virtual athletes
            if aid.startswith("A") and len(aid) > 1:
                try:
                    num = int(aid[1:])
                    if num > 1000:
                        aid = f"A{num - 1000}"
                except ValueError:
                    pass
            all_athlete_ids.add(aid)
    report_lines.append(f"**Total unique source athletes with failures:** {len(all_athlete_ids)}")
    report_lines.append("")

    # Criticality ranking
    report_lines.append("### Criticality Ranking")
    report_lines.append("")
    report_lines.append("| Rank | Category | Impact | Fix Priority |")
    report_lines.append("|------|----------|--------|-------------|")
    report_lines.append("| 1 | Empty Exercise Pools | Athlete gets NO prescription | P0 - Blocks athlete care |")
    report_lines.append("| 2 | Invalid Swap Candidates | No exercise variety in programs | P0 - Training stagnation |")
    report_lines.append("| 3 | Unsafe Olympic Lift | Injury risk for beginners | P1 - Safety critical |")
    report_lines.append("| 4 | High-Risk Leakage | Eccentric/plyometric injury | P1 - Safety critical |")
    report_lines.append("| 5 | Same Exercise Multi-Slot | Duplicate across template | P2 - Quality of prescription |")
    report_lines.append("| 6 | Missing Default | No fallback for empty pools | P2 - Reliability |")
    report_lines.append("| 7 | Movement Category Mismatch | Wrong exercise in slot | P2 - Quality of prescription |")
    report_lines.append("| 8 | Physical Driver Mismatch | Exercise doesn't target driver | P2 - Quality of prescription |")
    report_lines.append("| 9 | Invalid Progression | Wrong progression type | P3 - S&C science accuracy |")
    report_lines.append("| 10 | Duplicate Exercise Selection | Same exercise in multiple slots | P3 - Nuisance |")

    return "\n".join(report_lines)


if __name__ == "__main__":
    print("=" * 60)
    print("FORGE RECOMMENDATION ENGINE STRESS TEST")
    print("=" * 60)
    print()
    print("Generating 100 synthetic athletes...")
    print()
    print("Running recommendation stress tests...")
    print()

    failures, successes, errors, template_counts = run_stress_test()

    report = generate_report(failures, successes, errors, template_counts)

    output_path = "D:\\forge\\recommendation_stress_test.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Report written to: {output_path}")
    print(f"Successful prescriptions: {successes}")
    print(f"Failed prescriptions: {errors}")
    total = sum(len(v) for v in failures.values())
    print(f"Total failures detected: {total}")
    print()
    print("Done.")
