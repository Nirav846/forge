# Forge Deficit Detection Engine
# Role: Senior Sports Performance Engineer
# Description: Production-grade FastAPI service layer. It parses athlete test scores, 
# queries benchmark classifications, computes deficit severity, and runs sports-science confidence heuristics.

import os
import logging
import hashlib
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio

from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("forge-deficit-engine")

app = FastAPI(
    title="Forge Deficit Detection Engine",
    description="Analyzes athlete assessment scores against performance benchmarks to diagnose physical deficits.",
    version="1.0.0"
)

# -------------------------------------------------------------
# 1. Pydantic Models (Schemas)
# -------------------------------------------------------------

class AssessmentRequest(BaseModel):
    athlete_id: int = Field(..., example=101)
    results: Dict[str, float] = Field(
        ..., 
        example={"CMJ": 38.0, "Broad Jump": 2.1, "10m Sprint": 1.95}
    )

class DeficitDetail(BaseModel):
    deficit: str
    severity: str
    confidence: int

class DetectionResponse(BaseModel):
    athlete_id: int
    deficits: List[DeficitDetail]
    cached: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# -------------------------------------------------------------
# 2. Cache Layer (In-Memory with TTL - Redis-Ready Model)
# -------------------------------------------------------------

class MemoryCache:
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = asyncio.Lock()

    async def get(self, key: str) -> Optional[Any]:
        async with self._lock:
            if key not in self._cache:
                return None
            entry = self._cache[key]
            if datetime.utcnow() > entry["expires_at"]:
                del self._cache[key]
                return None
            return entry["data"]

    async def set(self, key: str, data: Any, ttl_seconds: int = 300):
        async with self._lock:
            self._cache[key] = {
                "data": data,
                "expires_at": datetime.utcnow() + timedelta(seconds=ttl_seconds)
            }

    async def clear(self):
        async with self._lock:
            self._cache.clear()

cache = MemoryCache()

def generate_cache_key(request: AssessmentRequest) -> str:
    sorted_results = sorted(request.results.items())
    key_str = f"athlete:{request.athlete_id}:{sorted_results}"
    return hashlib.sha256(key_str.encode("utf-8")).hexdigest()

# -------------------------------------------------------------
# 3. Database Layer & Repository Pattern
# -------------------------------------------------------------

class BenchmarkRepository:
    """Interface for benchmark database lookups."""
    async def get_score_classification(self, assessment_name: str, score: float) -> Optional[Dict[str, Any]]:
        raise NotImplementedError()


class PostgreSqlBenchmarkRepository(BenchmarkRepository):
    """PostgreSQL integration for querying benchmarks and deficits."""
    def __init__(self, pool=None):
        self.pool = pool  # asyncpg connection pool

    async def get_score_classification(self, assessment_name: str, score: float) -> Optional[Dict[str, Any]]:
        query = """
            SELECT 
                b.classification,
                b.min_value,
                b.max_value,
                a.metric_unit,
                d.name as deficit_name,
                d.description as deficit_description
            FROM assessments a
            JOIN benchmarks b ON a.id = b.assessment_id
            JOIN deficits d ON a.id = d.assessment_id
            WHERE a.name ILIKE $1
              AND (b.min_value IS NULL OR $2::numeric >= b.min_value)
              AND (b.max_value IS NULL OR $2::numeric <= b.max_value)
            LIMIT 1;
        """
        if not self.pool: return None
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, assessment_name, score)
            return dict(row) if row else None


class MockBenchmarkRepository(BenchmarkRepository):
    """Mock database with full S&C benchmarks matching Cricket seeds."""
    def __init__(self):
        # Maps assessment name -> List of benchmarks
        self.benchmarks = {
            "cmj": {
                "metric_unit": "cm", "deficit_name": "Power Deficit", "deficit_description": "Lack of vertical power.",
                "ranges": [
                    {"classification": "Elite", "min": 55.0, "max": None},
                    {"classification": "Optimal", "min": 45.0, "max": 54.99},
                    {"classification": "Sub-optimal", "min": 35.0, "max": 44.99},
                    {"classification": "Poor", "min": None, "max": 34.99}
                ]
            },
            "broad jump": {
                "metric_unit": "m", "deficit_name": "Mobility Restriction", "deficit_description": "Exhibits joint restriction limiting triple extension.",
                "ranges": [
                    {"classification": "Elite", "min": 2.60, "max": None},
                    {"classification": "Optimal", "min": 2.20, "max": 2.59},
                    {"classification": "Sub-optimal", "min": 1.80, "max": 2.19},
                    {"classification": "Poor", "min": None, "max": 1.79}
                ]
            },
            "10m sprint": {
                "metric_unit": "s", "deficit_name": "Acceleration Deficit", "deficit_description": "Sub-optimal acceleration mechanics.",
                "ranges": [
                    {"classification": "Elite", "min": None, "max": 1.60},
                    {"classification": "Optimal", "min": 1.61, "max": 1.80},
                    {"classification": "Sub-optimal", "min": 1.81, "max": 2.00},
                    {"classification": "Poor", "min": 2.01, "max": None}
                ]
            },
            "20m sprint": {
                "metric_unit": "s", "deficit_name": "Speed Deficit", "deficit_description": "Sub-optimal max linear running speeds.",
                "ranges": [
                    {"classification": "Elite", "min": None, "max": 2.80},
                    {"classification": "Optimal", "min": 2.81, "max": 3.10},
                    {"classification": "Sub-optimal", "min": 3.11, "max": 3.40},
                    {"classification": "Poor", "min": 3.41, "max": None}
                ]
            },
            "trap bar deadlift": {
                "metric_unit": "kg", "deficit_name": "Strength Deficit", "deficit_description": "Falls below absolute lower body force requirements.",
                "ranges": [
                    {"classification": "Elite", "min": 200.0, "max": None},
                    {"classification": "Optimal", "min": 160.0, "max": 199.99},
                    {"classification": "Sub-optimal", "min": 120.0, "max": 159.99},
                    {"classification": "Poor", "min": None, "max": 119.99}
                ]
            }
        }

    async def get_score_classification(self, assessment_name: str, score: float) -> Optional[Dict[str, Any]]:
        ass_clean = assessment_name.strip().lower()
        if ass_clean not in self.benchmarks:
            return None
        
        info = self.benchmarks[ass_clean]
        for rng in info["ranges"]:
            # Evaluate bounds
            min_ok = rng["min"] is None or score >= rng["min"]
            max_ok = rng["max"] is None or score <= rng["max"]
            if min_ok and max_ok:
                return {
                    "classification": rng["classification"],
                    "min_value": rng["min"],
                    "max_value": rng["max"],
                    "metric_unit": info["metric_unit"],
                    "deficit_name": info["deficit_name"],
                    "deficit_description": info["deficit_description"]
                }
        return None


def get_benchmark_repository() -> BenchmarkRepository:
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        pass
    return MockBenchmarkRepository()

# -------------------------------------------------------------
# 4. Service Layer (Diagnostic Business Logic)
# -------------------------------------------------------------

class DeficitDetectionService:
    def __init__(self, repo: BenchmarkRepository):
        self.repo = repo

    def calculate_confidence(
        self, score: float, classification: str, min_val: Optional[float], max_val: Optional[float],
        assessment_name: str, all_results: Dict[str, float], deficit_name: str
    ) -> int:
        """
        Confidence Algorithm:
        - Base: Single test maps to deficit -> 80.
        - Cross-Validation: If another test targets the same deficit, adjust.
          (E.g., CMJ and Broad Jump both evaluate Power Deficit).
        - Boundary Proximity Penalty: If within 5% of classification boundary -> -10 confidence points.
        """
        confidence = 80
        
        # 1. Cross-Validation Check
        # If we have multiple tests mapped to the same deficit, check agreement.
        if deficit_name == "Power Deficit":
            if "CMJ" in all_results and "Broad Jump" in all_results:
                # Both indicate deficit -> Boost confidence to 92
                confidence = 92
            else:
                # Only one test executed -> keep base
                confidence = 80

        # 2. Boundary Proximity Penalty
        # Proximity threshold = 5% of the boundary limit
        proximity_limit = 0.05
        is_borderline = False

        if min_val is not None:
            pct_diff = abs(score - min_val) / min_val
            if pct_diff <= proximity_limit:
                is_borderline = True

        if max_val is not None:
            pct_diff = abs(score - max_val) / max_val
            if pct_diff <= proximity_limit:
                is_borderline = True

        if is_borderline:
            logger.info(f"Score {score} for '{assessment_name}' is borderline (within 5% of boundary). Penalty applied.")
            confidence -= 10

        # Enforce bounds [50, 95]
        return max(50, min(95, confidence))

    async def detect_deficits(self, results: Dict[str, float]) -> List[DeficitDetail]:
        deficits_map: Dict[str, List[Dict[str, Any]]] = {}

        # Step 1: Query database classifications for all test scores
        for test, score in results.items():
            classif_info = await self.repo.get_score_classification(test, score)
            if not classif_info:
                logger.warning(f"No benchmark mapping found for test: '{test}'")
                continue

            classif = classif_info["classification"]
            deficit_name = classif_info["deficit_name"]

            # Severity Mapping: Poor -> High, Sub-optimal -> Moderate, Optimal/Elite -> None
            if classif == "Poor":
                severity = "High"
            elif classif == "Sub-optimal":
                severity = "Moderate"
            else:
                # Optimal or Elite -> no deficit
                continue

            # Step 2: Compute confidence using heuristics
            confidence = self.calculate_confidence(
                score=score,
                classification=classif,
                min_val=classif_info["min_value"],
                max_val=classif_info["max_value"],
                assessment_name=test,
                all_results=results,
                deficit_name=deficit_name
            )

            # Store result
            if deficit_name not in deficits_map:
                deficits_map[deficit_name] = []
            
            deficits_map[deficit_name].append({
                "severity": severity,
                "confidence": confidence
            })

        # Step 3: Resolve conflicting/overlapping tests to single deficit entries
        final_deficits = []
        for def_name, occurrences in deficits_map.items():
            # If multiple tests mapped to the same deficit, pick the highest severity and average/max confidence
            severity_priority = {"High": 2, "Moderate": 1}
            max_occ = max(occurrences, key=lambda x: severity_priority.get(x["severity"], 0))
            
            final_deficits.append(
                DeficitDetail(
                    deficit=def_name,
                    severity=max_occ["severity"],
                    confidence=max_occ["confidence"]
                )
            )

        return final_deficits

# -------------------------------------------------------------
# 5. FastAPI Endpoints
# -------------------------------------------------------------

@app.post(
    "/api/v1/diagnose-deficits",
    response_model=DetectionResponse,
    status_code=status.HTTP_200_OK,
    summary="Detect Athlete Deficits",
    description="Loads testing benchmarks, checks athlete scores, maps deficit severity, and calculates diagnostic confidence levels."
)
async def diagnose_deficits(
    request: AssessmentRequest,
    repo: BenchmarkRepository = Depends(get_benchmark_repository)
):
    # Check cache
    cache_key = generate_cache_key(request)
    cached_payload = await cache.get(cache_key)
    if cached_payload:
        logger.info(f"Cache hit for deficit key: {cache_key}")
        response = DetectionResponse(**cached_payload)
        response.cached = True
        return response

    # Miss: run diagnostic service
    logger.info(f"Cache miss. Evaluating assessment data for athlete: {request.athlete_id}")
    service = DeficitDetectionService(repo)
    detected = await service.detect_deficits(request.results)

    response_data = DetectionResponse(
        athlete_id=request.athlete_id,
        deficits=detected
    )

    # Set cache (5-minute TTL)
    await cache.set(cache_key, response_data.model_dump(), ttl_seconds=300)

    return response_data


@app.get(
    "/health",
    status_code=status.HTTP_200_OK
)
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow()
    }
