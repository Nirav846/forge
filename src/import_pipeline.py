# Forge Exercise Import Pipeline
# Role: Senior Backend Engineer
# Description: Production-ready ETL pipeline script written in Python. It parses exercise JSONs, 
# validates fields, maps muscles/equipment, auto-tags exercises, and inserts them into PostgreSQL.

import os
import json
import logging
from typing import List, Dict, Any, Tuple
from difflib import SequenceMatcher

# Setup Logging to both stdout and a rolling log file
log_dir = "d:/forge/logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "import_pipeline.log")

logger = logging.getLogger("forge-import-pipeline")
logger.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# File Handler
fh = logging.FileHandler(log_file, mode='a', encoding='utf-8')
fh.setFormatter(formatter)
logger.addHandler(fh)

# Console Handler
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

# -------------------------------------------------------------
# 1. Muscle & Equipment Mapping Catalogs
# -------------------------------------------------------------

MUSCLE_CATEGORY_MAP = {
    "quadriceps": "Lower Body",
    "glutes": "Lower Body",
    "hamstrings": "Lower Body",
    "calves": "Lower Body",
    "chest": "Upper Body - Push",
    "shoulders": "Upper Body - Push",
    "triceps": "Upper Body - Push",
    "lats": "Upper Body - Pull",
    "biceps": "Upper Body - Pull",
    "trapezius": "Upper Body - Pull",
    "abs": "Core",
    "obliques": "Core",
    "lower back": "Core"
}

EQUIPMENT_MAP = {
    "barbell": "Barbell",
    "dumbbell": "Dumbbell",
    "kettlebell": "Kettlebell",
    "cable": "Cable Machine",
    "bands": "Resistance Bands",
    "bodyweight": "Bodyweight",
    "other": "Other"
}

# -------------------------------------------------------------
# 2. S&C Auto-Tagging Rules Engine
# -------------------------------------------------------------

def generate_tags(exercise: Dict[str, Any], mapped_equipment: str) -> List[str]:
    tags = []
    name_lower = exercise["name"].lower()
    desc_lower = " ".join(exercise.get("instructions", [])).lower()
    primary_muscles = [m.lower() for m in exercise.get("primaryMuscles", [])]
    secondary_muscles = [m.lower() for m in exercise.get("secondaryMuscles", [])]
    all_muscles = primary_muscles + secondary_muscles

    # Rule 1: Unilateral Work
    unilateral_keywords = ["single-leg", "unilateral", "one-arm", "one-leg", "bulgarian", "split", "single-arm"]
    is_unilateral = any(kw in name_lower or kw in desc_lower for kw in unilateral_keywords)
    if is_unilateral:
        tags.append("Unilateral")
    
    # Rule 2: Bilateral Work
    if not is_unilateral and mapped_equipment in ["Barbell", "Trap Bar"]:
        tags.append("Bilateral")

    # Rule 3: Posterior Chain
    posterior_muscles = ["glutes", "hamstrings", "lower back", "calves", "lats", "trapezius"]
    if any(m in primary_muscles for m in posterior_muscles):
        tags.append("Posterior Chain")
    elif any(m in secondary_muscles for m in posterior_muscles):
        tags.append("Posterior Chain")

    # Rule 4: Anterior Chain
    anterior_muscles = ["quadriceps", "chest", "shoulders"]
    if any(m in primary_muscles for m in anterior_muscles):
        tags.append("Anterior Chain")

    # Rule 5: Explosive movements
    if exercise.get("category", "").lower() == "plyometrics" or "explosive" in desc_lower:
        tags.append("Explosive")

    # Rule 6: Accessory/Rehab categorizations
    if exercise.get("mechanic", "").lower() == "isolation" or exercise.get("category", "").lower() == "stretching":
        tags.append("Accessory")

    return list(set(tags))

# -------------------------------------------------------------
# 3. Data Validation
# -------------------------------------------------------------

def validate_exercise(exercise: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errors = []
    if not exercise.get("name"):
        errors.append("Missing field: 'name'")
    
    # Check difficulty mappings
    level = exercise.get("level", "").lower()
    if level not in ["beginner", "intermediate", "expert", "advanced", "elite"]:
        errors.append(f"Invalid level: '{exercise.get('level')}'")

    # Check mechanics
    mechanic = exercise.get("mechanic")
    if mechanic and mechanic.lower() not in ["compound", "isolation", None]:
        errors.append(f"Invalid mechanic type: '{mechanic}'")

    # Check force type
    force = exercise.get("force")
    if force and force.lower() not in ["push", "pull", "static", None]:
        errors.append(f"Invalid force type: '{force}'")

    # Check muscle structures
    if not exercise.get("primaryMuscles"):
        errors.append("Missing field: 'primaryMuscles'")

    return len(errors) == 0, errors

# -------------------------------------------------------------
# 4. Duplicate and Similarity Detection
# -------------------------------------------------------------

def detect_duplicates(name: str, existing_names: List[str], threshold: float = 0.85) -> Tuple[str, float]:
    """
    Returns the most similar existing name if similarity exceeds threshold, 
    otherwise returns empty string.
    """
    name_clean = name.strip().lower()
    for existing in existing_names:
        existing_clean = existing.strip().lower()
        if name_clean == existing_clean:
            return existing, 1.0
        
        # Calculate sequence similarity
        similarity = SequenceMatcher(None, name_clean, existing_clean).ratio()
        if similarity >= threshold:
            return existing, similarity
            
    return "", 0.0

# -------------------------------------------------------------
# 5. Database Connector & Inserter
# -------------------------------------------------------------

class DatabasePipelineLoader:
    """Handles insertions into PostgreSQL or executes mock writes to logging if disconnected."""
    def __init__(self, dsn: Optional[str] = None):
        self.dsn = dsn
        self.conn = None
        self.use_mock = True

        if dsn:
            try:
                import psycopg2
                self.conn = psycopg2.connect(dsn)
                self.conn.autocommit = False
                self.use_mock = False
                logger.info("Successfully established PostgreSQL connection pool for ETL pipeline.")
            except Exception as e:
                logger.error(f"Failed to connect to PostgreSQL: {e}. Falling back to dry-run/mock mode.")

    def load_exercise_transaction(self, exercise: Dict[str, Any], mapped_equipment: str, tags: List[str]) -> bool:
        if self.use_mock:
            # Print mock SQL trace for validation
            logger.debug(f"[SQL Dry-Run] INSERT INTO exercises (name, mechanics_type, force_type, difficulty_level) VALUES ('{exercise['name']}', ...)")
            return True

        cursor = self.conn.cursor()
        try:
            # 1. Map difficulty, mechanics, force casing to schema requirements
            level_map = {"beginner": "Beginner", "intermediate": "Intermediate", "expert": "Advanced", "advanced": "Advanced", "elite": "Elite"}
            mech_map = {"compound": "Compound", "isolation": "Isolation"}
            force_map = {"push": "Push", "pull": "Pull", "static": "Static"}

            level = level_map.get(exercise["level"].lower(), "Intermediate")
            mechanic = mech_map.get(exercise.get("mechanic", "").lower(), "N/A")
            force = force_map.get(exercise.get("force", "").lower(), "N/A")
            description = " ".join(exercise.get("instructions", []))

            # 2. Insert Core Exercise
            cursor.execute(
                """
                INSERT INTO exercises (name, description, difficulty_level, mechanics_type, force_type)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (exercise["name"], description, level, mechanic, force)
            )
            exercise_id = cursor.fetchone()[0]

            # 3. Resolve and Map Equipment
            cursor.execute("SELECT id FROM equipment WHERE name = %s LIMIT 1;", (mapped_equipment,))
            eq_row = cursor.fetchone()
            if not eq_row:
                # Insert equipment lookup if not exists
                cursor.execute(
                    "INSERT INTO equipment (name, category) VALUES (%s, 'Other') RETURNING id;", 
                    (mapped_equipment,)
                )
                equipment_id = cursor.fetchone()[0]
            else:
                equipment_id = eq_row[0]
            
            cursor.execute(
                "INSERT INTO exercise_equipment (exercise_id, equipment_id, is_required) VALUES (%s, %s, TRUE) ON CONFLICT DO NOTHING;",
                (exercise_id, equipment_id)
            )

            # 4. Map Muscles (Primary)
            for muscle in exercise.get("primaryMuscles", []):
                muscle_name = muscle.title()
                cat = MUSCLE_CATEGORY_MAP.get(muscle.lower(), "Other")
                cursor.execute("INSERT INTO muscles (name, category) VALUES (%s, %s) ON CONFLICT (name) DO UPDATE SET updated_at = NOW() RETURNING id;", (muscle_name, cat))
                muscle_id = cursor.fetchone()[0]
                cursor.execute("INSERT INTO exercise_muscles (exercise_id, muscle_id, role) VALUES (%s, %s, 'Primary') ON CONFLICT DO NOTHING;", (exercise_id, muscle_id))

            # 5. Map Muscles (Secondary)
            for muscle in exercise.get("secondaryMuscles", []):
                muscle_name = muscle.title()
                cat = MUSCLE_CATEGORY_MAP.get(muscle.lower(), "Other")
                cursor.execute("INSERT INTO muscles (name, category) VALUES (%s, %s) ON CONFLICT (name) DO UPDATE SET updated_at = NOW() RETURNING id;", (muscle_name, cat))
                muscle_id = cursor.fetchone()[0]
                cursor.execute("INSERT INTO exercise_muscles (exercise_id, muscle_id, role) VALUES (%s, %s, 'Secondary') ON CONFLICT DO NOTHING;", (exercise_id, muscle_id))

            # 6. Map Auto-Generated Tags
            for tag in tags:
                cursor.execute("INSERT INTO tags (name) VALUES (%s) ON CONFLICT (name) DO NOTHING RETURNING id;", (tag,))
                tag_row = cursor.fetchone()
                if tag_row:
                    tag_id = tag_row[0]
                else:
                    cursor.execute("SELECT id FROM tags WHERE name = %s;", (tag,))
                    tag_id = cursor.fetchone()[0]
                cursor.execute("INSERT INTO exercise_tags (exercise_id, tag_id) VALUES (%s, %s) ON CONFLICT DO NOTHING;", (exercise_id, tag_id))

            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Transaction failed for exercise '{exercise['name']}': {e}")
            return False
        finally:
            cursor.close()

    def close(self):
        if self.conn:
            self.conn.close()

# -------------------------------------------------------------
# 6. Core ETL Pipeline Execution
# -------------------------------------------------------------

def run_import_pipeline(json_filepath: str, dsn: Optional[str] = None):
    logger.info("=" * 60)
    logger.info(f"Starting Forge Exercise Import Pipeline. Source: {json_filepath}")
    logger.info("=" * 60)

    # Simulated existing DB records for duplication matching
    existing_exercise_names = [
        "Barbell Back Squat", "Power Clean", "Rear Foot Elevated Split Squat", 
        "Trap Bar Deadlift", "Kettlebell Swing", "Depth Jump", 
        "Medicine Ball Rotational Scoop Toss", "A-Skip", 
        "Single-Leg Isometric Wall Sit", "Nordic Hamstring Curl"
    ]

    # Initialize loader
    loader = DatabasePipelineLoader(dsn)

    # Stats tracking
    stats = {
        "read": 0,
        "valid": 0,
        "invalid": 0,
        "exact_duplicates": 0,
        "fuzzy_duplicates": 0,
        "imported": 0,
        "failed": 0
    }

    # Extract phase
    try:
        with open(json_filepath, "r", encoding="utf-8") as f:
            exercises_data = json.load(f)
    except Exception as e:
        logger.error(f"Failed to read source JSON dataset: {e}")
        return

    # Transform & Load phases
    for raw_ex in exercises_data:
        stats["read"] += 1
        name = raw_ex.get("name", "Unknown")

        # 1. Validation Checks
        is_valid, errors = validate_exercise(raw_ex)
        if not is_valid:
            logger.warning(f"Validation failed for '{name}'. Reasons: {', '.join(errors)}")
            stats["invalid"] += 1
            continue
        stats["valid"] += 1

        # 2. Duplicate Detection
        dup_match, similarity = detect_duplicates(name, existing_names=existing_exercise_names)
        if similarity == 1.0:
            logger.info(f"Skipping exact duplicate found in database: '{name}'")
            stats["exact_duplicates"] += 1
            continue
        elif similarity >= 0.85:
            # Fuzzy match flagging
            logger.warning(f"Fuzzy duplicate warning for '{name}'. Close match: '{dup_match}' ({similarity*100:.1f}% similarity). Skipping for manual review.")
            stats["fuzzy_duplicates"] += 1
            continue

        # 3. Equipment & Synonym Mapping
        raw_eq = raw_ex.get("equipment", "bodyweight").lower()
        mapped_eq = EQUIPMENT_MAP.get(raw_eq, "Other")
        # Handle Hex Bar synonym
        if "hex bar" in name.lower() and mapped_eq == "Other":
            mapped_eq = "Trap Bar"

        # 4. Auto-Generate Tags
        generated_tags = generate_tags(raw_ex, mapped_eq)

        # 5. Load (Insert) to Database
        success = loader.load_exercise_transaction(raw_ex, mapped_eq, generated_tags)
        if success:
            logger.info(f"Successfully imported exercise: '{name}' (Mapped Equipment: {mapped_eq}, Tags: {generated_tags})")
            stats["imported"] += 1
            # Add to list to prevent duplication within the same import run
            existing_exercise_names.append(name)
        else:
            stats["failed"] += 1

    loader.close()

    # Final summary reports
    logger.info("=" * 60)
    logger.info("ETL Pipeline Execution Complete. Summary:")
    logger.info(f"  - Total Records Evaluated: {stats['read']}")
    logger.info(f"  - Validated: {stats['valid']}")
    logger.info(f"  - Invalid / Rejected: {stats['invalid']}")
    logger.info(f"  - Exact Duplicates Skipped: {stats['exact_duplicates']}")
    logger.info(f"  - Fuzzy Matches Flagged/Skipped: {stats['fuzzy_duplicates']}")
    logger.info(f"  - Successfully Ingested: {stats['imported']}")
    logger.info(f"  - Failed Writes: {stats['failed']}")
    logger.info("=" * 60)

if __name__ == "__main__":
    # In practice, DSN is read from environment variable DATABASE_URL
    # For local verification, pipeline runs in Dry-Run/Mock mode on the sample JSON.
    sample_file = "d:/forge/examples/free_exercise_db_sample.json"
    run_import_pipeline(sample_file)
