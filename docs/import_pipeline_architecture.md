# Forge Exercise Import Pipeline Architecture

This document details the software architecture, data mapping rules, validation parameters, and deduplication logic of the **Forge Exercise Import Pipeline**.

---

## 1. ETL Pipeline Pipeline Flow

The import pipeline is structured as a class-based, atomic ETL process:

```
[Raw JSON File]
      │
      ▼
 1. [EXTRACT]       ──> Read JSON array, deserialize file, handle encodings
      │
      ▼
 2. [TRANSFORM]
    ├── A. Validate ──> Filter out records missing name/muscles or having invalid enums
    ├── B. Dedupe   ──> Skip exact matches. Flag similarity > 85%
    ├── C. Map      ──> Resolve equipment synonyms (e.g., Hex Bar -> Trap Bar)
    └── D. Tag      ──> Generate S&C labels (Anterior/Posterior chain, Unilateral/Bilateral)
      │
      ▼
 3. [LOAD]          ──> Execute atomic transactional DML insertions in PostgreSQL
      │
      ▼
[PostgreSQL Database]
```

---

## 2. Normalized Database Expansion

To support deep anatomical filtering, the pipeline implements a schema migration adding normalized muscle records:

```
                  ┌───────────────┐
                  │   EXERCISES   │
                  └───────┬───────┘
                          │ (1:N)
                          ▼
                  ┌───────────────┐
                  │EXERCISE_MUSCLE│ (role: Primary/Secondary)
                  └───────┬───────┘
                          │ (N:1)
                          ▼
                  ┌───────────────┐
                  │    MUSCLES    │ (category: Lower Body, Core, etc.)
                  └───────────────┘
```

### Muscle Categorization Matrix

Lookups are automatically categorized during ingestion:
- **Lower Body**: `quadriceps`, `glutes`, `hamstrings`, `calves`
- **Upper Body - Push**: `chest`, `shoulders`, `triceps`
- **Upper Body - Pull**: `lats`, `biceps`, `trapezius`
- **Core**: `abs`, `obliques`, `lower back`
- **Other**: Default classification for minor stabilizer muscles.

---

## 3. Auto-Tagging Rules Heuristics

The transformation engine analyzes the exercise meta-properties to generate sports-science tags dynamically:

1. **Unilateral**: Triggered if the name or instruction text contains single-limb keywords (`single-leg`, `unilateral`, `one-arm`, `one-leg`, `bulgarian`, `split`, etc.).
2. **Bilateral**: Assigned to barbell or trap-bar compound exercises if not flagged as unilateral.
3. **Posterior Chain**: Generated if any glute, hamstring, lower back, calves, lats, or trapezius muscles are targeted.
4. **Anterior Chain**: Generated if quadriceps, chest, or shoulder muscles are listed.
5. **Explosive**: Triggered if the category is `plyometrics` or instructions mention velocity/explosiveness.
6. **Accessory**: Assigned to isolation exercises or stretching categories.

---

## 4. Validation & Quality Checks

Exercises must pass strict quality controls to prevent database corruption:
- **Name Check**: String presence required; empty names are rejected.
- **Difficulty Mapping**: Standardized to `Beginner`, `Intermediate`, `Advanced`, or `Elite`. Out-of-bounds levels are rejected.
- **Mechanics Mapping**: Sanitized to `Compound`, `Isolation`, or `N/A`.
- **Force Mapping**: Sanitized to `Push`, `Pull`, `Static`, or `N/A`.
- **Muscle Completeness**: Exercises must list at least one primary muscle group.

---

## 5. Duplicate & Fuzzy Match Detection

To maintain data cleanliness over multiple import runs, the system implements a two-stage deduplication filter:

### Stage 1: Exact Name Check
Matches the stripped, lowercase name of the incoming exercise against the existing catalog. If an exact match is found, the exercise is skipped.

### Stage 2: Fuzzy Similarity Ratio (difflib)
Calculates string similarity using Levenshtein-based ratios (`SequenceMatcher`):
- **Formula**: Ratio = $2.0 \times \frac{M}{T}$ (where $M$ is the number of matching characters and $T$ is the total characters in both strings).
- **Threshold**: **`0.85` (85%)**.
- **Action**: Matches exceeding 85% similarity (e.g. "Barbell Squats" vs "Barbell Back Squat") are logged as warnings and skipped to prevent duplicate records, prompting S&C administrators for manual review.

---

## 6. Execution Modes

The pipeline script ([`src/import_pipeline.py`](../src/import_pipeline.py)) automatically detects execution environments:
1. **Production mode**: Triggered when `DATABASE_URL` is set. Runs queries using the `psycopg2` driver, committing all lookups and mappings in atomic transactions.
2. **Dry-run (Mock) mode**: Default fallback if `DATABASE_URL` is empty. Executes all transformations, validations, and deduplication logic, tracing SQL queries to standard out without database dependencies.
