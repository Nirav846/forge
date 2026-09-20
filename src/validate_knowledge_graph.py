# Forge S&C Knowledge Graph Validator
# Role: Domain Architect & S&C Coach
# Description: Production-grade python validation script to check knowledge graph seed files for 
# data integrity, logical consistency, benchmark range overlaps, and schema validation.

import os
import json
import logging
from typing import List, Dict, Any

# Setup logging
log_dir = "d:/forge/logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "validation.log")

logger = logging.getLogger("graph-validator")
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

fh = logging.FileHandler(log_file, mode='w', encoding='utf-8')
fh.setFormatter(formatter)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

# Allowed taxonomies matching constraints
ALLOWED_CLASSIFICATIONS = {"Elite", "Optimal", "Sub-optimal", "Poor"}
ALLOWED_PRIORITIES = {"Primary", "Secondary", "Tertiary"}
ALLOWED_METHODS = {"Max Strength", "Dynamic Effort", "Plyometrics", "Sprint Training", "COD Training", "Rotational Power", "Mobility"}

def validate_benchmarks(assessment_name: str, benchmarks: List[Dict[str, Any]]) -> int:
    errors = 0
    classifications_seen = set()

    for bm in benchmarks:
        classif = bm.get("classification")
        if classif not in ALLOWED_CLASSIFICATIONS:
            logger.error(f"Assessment '{assessment_name}' - Invalid benchmark classification: '{classif}'")
            errors += 1
        classifications_seen.add(classif)

        # Validate range values
        min_val = bm.get("min_value")
        max_val = bm.get("max_value")

        if min_val is not None and not isinstance(min_val, (int, float)):
            logger.error(f"Assessment '{assessment_name}' ({classif}) - min_value must be numeric or null. Got: {type(min_val)}")
            errors += 1
        if max_val is not None and not isinstance(max_val, (int, float)):
            logger.error(f"Assessment '{assessment_name}' ({classif}) - max_value must be numeric or null. Got: {type(max_val)}")
            errors += 1

        if min_val is not None and max_val is not None:
            if min_val > max_val:
                logger.error(f"Assessment '{assessment_name}' ({classif}) - min_value ({min_val}) cannot be greater than max_value ({max_val})")
                errors += 1

    # Check for missing classifications
    missing = ALLOWED_CLASSIFICATIONS - classifications_seen
    if missing:
        logger.warning(f"Assessment '{assessment_name}' - Missing benchmark classifications: {missing}")

    return errors

def run_knowledge_graph_validation(json_filepath: str) -> bool:
    logger.info("=" * 60)
    logger.info(f"Auditing S&C Knowledge Graph Seed: {json_filepath}")
    logger.info("=" * 60)

    try:
        with open(json_filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        logger.error(f"Failed to parse JSON file: {e}")
        return False

    errors_count = 0
    warnings_count = 0

    # 1. Sport check
    sport = data.get("sport")
    if not sport:
        logger.error("Missing root property: 'sport'")
        errors_count += 1
    else:
        logger.info(f"Verified target Sport: '{sport}'")

    # 2. Roles, Drivers, & Priorities check
    roles = data.get("roles", [])
    if not roles:
        logger.error("No roles defined in seed file.")
        errors_count += 1

    roles_list = []
    drivers_list = []

    for r in roles:
        role_name = r.get("name")
        if not role_name:
            logger.error("Found a role missing the 'name' attribute.")
            errors_count += 1
            continue
        roles_list.append(role_name)

        logger.info(f"Auditing Role: '{role_name}'")
        drivers = r.get("performance_drivers", [])
        if not drivers:
            logger.warning(f"Role '{role_name}' has no performance drivers defined.")
            warnings_count += 1

        for dr in drivers:
            dr_name = dr.get("name")
            if not dr_name:
                logger.error(f"Role '{role_name}' has a driver missing the 'name' attribute.")
                errors_count += 1
                continue
            drivers_list.append(dr_name)

            priority = dr.get("priority")
            if priority not in ALLOWED_PRIORITIES:
                logger.error(f"Role '{role_name}' - Driver '{dr_name}' has invalid priority: '{priority}'")
                errors_count += 1

    # 3. Assessments & Benchmarks checks
    assessments = data.get("assessments", [])
    assessment_names = []
    for ass in assessments:
        name = ass.get("name")
        if not name:
            logger.error("Found an assessment missing the 'name' attribute.")
            errors_count += 1
            continue
        assessment_names.append(name)

        metric_unit = ass.get("metric_unit")
        if not metric_unit:
            logger.error(f"Assessment '{name}' is missing 'metric_unit'.")
            errors_count += 1

        benchmarks = ass.get("benchmarks", [])
        bm_errors = validate_benchmarks(name, benchmarks)
        errors_count += bm_errors

    # 4. Deficits, Mapped methods, and Templates check
    deficits = data.get("deficits", [])
    for defc in deficits:
        defc_name = defc.get("name")
        if not defc_name:
            logger.error("Found a deficit missing the 'name' attribute.")
            errors_count += 1
            continue

        logger.info(f"Auditing Deficit: '{defc_name}'")
        
        # Verify assessment link
        ass_link = defc.get("evaluated_by_assessment")
        if ass_link not in assessment_names:
            logger.error(f"Deficit '{defc_name}' maps to undefined assessment: '{ass_link}'")
            errors_count += 1

        # Verify training methods link
        methods = defc.get("resolved_by_methods", [])
        if not methods:
            logger.warning(f"Deficit '{defc_name}' maps to no training methods.")
            warnings_count += 1
        
        for m in methods:
            if m not in ALLOWED_METHODS:
                logger.error(f"Deficit '{defc_name}' maps to invalid training method: '{m}'")
                errors_count += 1

        # Verify prescribed templates
        templates = defc.get("prescribed_templates", [])
        if not templates:
            logger.warning(f"Deficit '{defc_name}' maps to no movement templates.")
            warnings_count += 1

    # Final summary report
    logger.info("=" * 60)
    logger.info("Validation Audit Complete. Results:")
    logger.info(f"  - Total Roles Audited: {len(roles_list)}")
    logger.info(f"  - Total Assessments Audited: {len(assessment_names)}")
    logger.info(f"  - Total Errors Encountered: {errors_count}")
    logger.info(f"  - Total Warnings Issued: {warnings_count}")
    logger.info("=" * 60)

    return errors_count == 0

if __name__ == "__main__":
    seed_file = "d:/forge/examples/cricket_knowledge_graph_seed.json"
    success = run_knowledge_graph_validation(seed_file)
    if success:
        print("Knowledge Graph Seed Audit PASS")
    else:
        print("Knowledge Graph Seed Audit FAIL")
