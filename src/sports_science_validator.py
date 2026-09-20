import re
import json
from typing import Dict, Any, List

class SportsScienceValidator:
    """
    Validation engine evaluating S&C training programs against Coach Audit rules.
    Loads rules dynamically from examples/sports_science_rules.json.
    """
    def __init__(self, rules_path: str = "examples/sports_science_rules.json"):
        with open(rules_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.rules = {rule["rule_id"]: rule for rule in data["rules"]}

    def validate_program(self, program: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Validates the entire program hierarchy (Program -> Weeks -> Sessions -> Exercises)
        against the sports science constraints.
        Returns a list of violations (issues).
        """
        violations = []
        weekly_exercise_counts: Dict[int, Dict[str, int]] = {} # week_num -> {exercise_name: count}

        for week in program.get("weeks", []):
            week_num = week.get("week_number", 1)
            weekly_exercise_counts[week_num] = {}

            for session in week.get("sessions", []):
                session_num = session.get("session_number", 1)
                exercises = session.get("exercises", [])
                
                # Check individual exercises
                for ex in exercises:
                    ex_name = ex.get("name", "")
                    ex_name_lower = ex_name.lower()
                    intensity = ex.get("intensity", "")
                    reps = ex.get("reps", 0)
                    display_order = ex.get("display_order", 1)

                    # Track weekly occurrence for RULE_SESSION_VARIATION
                    weekly_exercise_counts[week_num][ex_name] = weekly_exercise_counts[week_num].get(ex_name, 0) + 1

                    # 1. RULE_JUMP_SQUAT_INTENSITY
                    if "jump squat" in ex_name_lower:
                        rule = self.rules.get("RULE_JUMP_SQUAT_INTENSITY")
                        if rule:
                            forbidden = rule["constraints"]["forbidden_intensity_pattern"]
                            if re.search(forbidden, intensity):
                                violations.append({
                                    "rule_id": "RULE_JUMP_SQUAT_INTENSITY",
                                    "issue": f"Jump squat '{ex_name}' in Week {week_num}, Session {session_num} has inappropriate intensity '{intensity}'.",
                                    "severity": rule["severity"],
                                    "recommended_change": "Load in speed-strength zone (30-40% 1RM) using VBT thresholds.",
                                    "reasoning": rule["description"]
                                })

                    # 2. RULE_MED_BALL_INTENSITY
                    if "medicine ball" in ex_name_lower or "mb " in ex_name_lower:
                        rule = self.rules.get("RULE_MED_BALL_INTENSITY")
                        if rule:
                            forbidden = rule["constraints"]["forbidden_pattern"]
                            if re.search(forbidden, intensity):
                                violations.append({
                                    "rule_id": "RULE_MED_BALL_INTENSITY",
                                    "issue": f"Medicine ball throw '{ex_name}' in Week {week_num}, Session {session_num} uses % 1RM loading '{intensity}'.",
                                    "severity": rule["severity"],
                                    "recommended_change": "Prescribe using ball weight (e.g., 2-4 kg) and maximum effort intent.",
                                    "reasoning": rule["description"]
                                })

                    # 3. RULE_PLANK_REPS_INTENSITY
                    if "plank" in ex_name_lower:
                        rule = self.rules.get("RULE_PLANK_REPS_INTENSITY")
                        if rule:
                            forbidden = rule["constraints"]["forbidden_intensity_pattern"]
                            if re.search(forbidden, intensity):
                                violations.append({
                                    "rule_id": "RULE_PLANK_REPS_INTENSITY",
                                    "issue": f"Plank exercise '{ex_name}' in Week {week_num}, Session {session_num} is loaded via % 1RM '{intensity}'.",
                                    "severity": rule["severity"],
                                    "recommended_change": "Use bodyweight with max isometric tension cues.",
                                    "reasoning": rule["description"]
                                })

                    # 4. RULE_NORDIC_CURL_VOLUME_SAFETY
                    if "nordic hamstring" in ex_name_lower:
                        rule = self.rules.get("RULE_NORDIC_CURL_VOLUME_SAFETY")
                        if rule:
                            max_reps = rule["constraints"]["max_reps_per_set"]
                            forbidden = rule["constraints"]["forbidden_intensity_pattern"]
                            if reps > max_reps or re.search(forbidden, intensity):
                                violations.append({
                                    "rule_id": "RULE_NORDIC_CURL_VOLUME_SAFETY",
                                    "issue": f"Nordic Hamstring Curl '{ex_name}' in Week {week_num}, Session {session_num} has reps={reps} or intensity={intensity}.",
                                    "severity": rule["severity"],
                                    "recommended_change": f"Cap reps at {max_reps} reps and load using Bodyweight (Slow Eccentric).",
                                    "reasoning": rule["description"]
                                })

                # Check CNS Exercise Pairing (RULE_CNS_EXERCISE_PAIRING)
                primary_exercises = [ex for ex in exercises if ex.get("display_order") == 1]
                if primary_exercises:
                    rule = self.rules.get("RULE_CNS_EXERCISE_PAIRING")
                    if rule and len(exercises) >= 2:
                        # Check if session exercises have no contrast or superset structure
                        # For simplicity, if display_order is sequential without pairing groupings, flag a warning
                        violations.append({
                            "rule_id": "RULE_CNS_EXERCISE_PAIRING",
                            "issue": f"Session {session_num} in Week {week_num} runs Primary exercises as straight sets without contrast pairing.",
                            "severity": rule["severity"],
                            "recommended_change": "Pair the Primary power movement with a low-load vertical jump or mobility stretch in a contrast superset.",
                            "reasoning": rule["description"]
                        })

        # 5. RULE_SESSION_VARIATION (Weekly monotony check)
        for week_num, counts in weekly_exercise_counts.items():
            rule = self.rules.get("RULE_SESSION_VARIATION")
            if rule:
                max_allowed = rule["constraints"]["max_reps_of_exercise_per_week"]
                for ex_name, count in counts.items():
                    if count > max_allowed:
                        violations.append({
                            "rule_id": "RULE_SESSION_VARIATION",
                            "issue": f"Exercise '{ex_name}' is repeated {count} times in Week {week_num}.",
                            "severity": rule["severity"],
                            "recommended_change": "Introduce training variation across weekly sessions (e.g. alternating exercise variants).",
                            "reasoning": rule["description"]
                        })

        return violations

if __name__ == "__main__":
    import sys
    # Load rules and validate target generated file
    target_program_path = "examples/program_builder_output.json"
    if len(sys.argv) > 1:
        target_program_path = sys.argv[1]
        
    print(f"Loading rules and validating program: {target_program_path}...")
    try:
        validator = SportsScienceValidator()
        with open(target_program_path, "r", encoding="utf-8") as f:
            prog_data = json.load(f)
        errors = validator.validate_program(prog_data)
        if errors:
            print(f"Validation FAILED with {len(errors)} issues:")
            print(json.dumps(errors, indent=2))
        else:
            print("Validation PASSED! The program is compliant with all S&C rules.")
    except Exception as e:
        print(f"Error during validation run: {e}")
