# Forge Deficit Detection Engine Architecture Spec
**Author: Senior Sports Performance Engineer**  
**Date: 2026-06-15**

This document specifies the software architecture, diagnostic logic, testing validation, and caching strategy of the **Forge Deficit Detection Engine**.

---

## 1. Diagnostic Pipeline Flow

The engine parses raw test scores and dynamically maps them to physical deficits:

```
[Athlete Test Scores]
         │
         ▼
 1. [Query Benchmarks]   ──> Fetch classification range & metric unit
         │
         ▼
 2. [Classify Severity]  ──> Map: Poor -> High, Sub-optimal -> Moderate
         │
         ▼
 3. [Calculate Confidence]
    ├── A. Base Rate     ──> Set 80% for single test match
    ├── B. Cross-Val     ──> Boost to 92% if multiple tests agree (CMJ + Broad Jump)
    └── C. Boundary Check──> Deduct 10% if score is within 5% of threshold
         │
         ▼
[Deficit JSON Payload]   ──> Return structured list (cached by key)
```

---

## 2. Sports Science Scoring Heuristics

### A. Severity Classification Rules
We standardize physical benchmark classifications from the database to clean API severities:
- **Poor** (score falls into the lowest tier) $\to$ **High Severity Deficit**.
- **Sub-optimal** (score falls into the second-lowest tier) $\to$ **Moderate Severity Deficit**.
- **Optimal / Elite** (score meets or exceeds targets) $\to$ **No Deficit** (filtered out).

### B. Confidence Scoring Math
Confidence measures how certain we are of the diagnosed physical weakness. It is computed dynamically:
1. **Base Rate ($80\%$)**: A single test matches a deficit.
2. **Cross-Validation Boost ($92\%$)**: If multiple tests mapped to the same deficit are executed and agree (e.g. both `CMJ` and `Broad Jump` indicate a `Power Deficit`), we increase confidence to **$92\%$**.
3. **Boundary Proximity Penalty ($-10\%$)**: If a score lies within $5\%$ of a classification boundary (e.g., CMJ of $34.8\text{ cm}$ where Poor is $<35\text{ cm}$), we apply a borderline check penalty of **$-10\%$** (with a floor of $50\%$) to reflect testing noise.
   $$\text{Proximity} = \frac{|Score - Boundary|}{Boundary} \le 0.05 \implies \text{Confidence} = \text{Confidence} - 10$$

---

## 3. Core PostgreSQL Queries

The repository layer ([`src/deficit_detection_engine.py`](../src/deficit_detection_engine.py)) resolves the classification ranges dynamically using SQL range joins:
```sql
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
WHERE a.name ILIKE :assessment_name
  AND (b.min_value IS NULL OR :score >= b.min_value)
  AND (b.max_value IS NULL OR :score <= b.max_value)
LIMIT 1;
```
By comparing the athlete's `:score` against the benchmark `min_value` and `max_value` fields (handling NULL bounds for $-\infty$ and $+\infty$), the database classifies the score in a single query.

---

## 4. API Structure

- **Endpoint**: `POST /api/v1/diagnose-deficits`
- **Request Payload**:
  ```json
  {
    "athlete_id": 101,
    "results": {
      "CMJ": 38.0,
      "Broad Jump": 2.1,
      "10m Sprint": 1.95
    }
  }
  ```
- **Response Payload (200 OK)**:
  ```json
  {
    "athlete_id": 101,
    "deficits": [
      {
        "deficit": "Power Deficit",
        "severity": "Moderate",
        "confidence": 92
      },
      {
        "deficit": "Mobility Restriction",
        "severity": "Moderate",
        "confidence": 80
      },
      {
        "deficit": "Acceleration Deficit",
        "severity": "Moderate",
        "confidence": 80
      }
    ],
    "cached": false,
    "timestamp": "2026-06-15T12:00:00Z"
  }
  ```

---

## 5. Caching Strategy

To deliver sub-millisecond response times under concurrent workloads, the service layer implements a structured caching policy:
- **Cache Key Signature**: Normalized SHA-256 hash of the `athlete_id` combined with sorted assessment values:
  - `athlete:{id}:{sorted_results}`
- **TTL Duration**: **300 seconds (5 minutes)**. This provides consistency for training templates while reducing redundant database reads.
