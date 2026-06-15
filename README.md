# Forge Exercise Intelligence Database

This repository contains the design, schema, migrations, and documentation for the **Forge Exercise Intelligence Database**, built on PostgreSQL. It is designed to act as a normalized, high-performance exercise registry that can scale to 10,000+ exercises and support complex athletic mappings for elite sports performance applications.

## Table of Contents
1. [Project Structure](#project-structure)
2. [Database Design & Architecture](#database-design--architecture)
3. [Setup & Migrations](#setup--migrations)
4. [Sample Queries](#sample-queries)

---

## Project Structure

```
d:/forge/
├── docs/
│   └── architecture.md            # Detailed ER diagram, normalization analysis, and index recommendations
├── migrations/
│   ├── 000001_create_core_schema.up.sql    # DDL: Core schema, lookups, junction tables, & indexes
│   ├── 000001_create_core_schema.down.sql  # DDL Rollback: Safely drops all tables and components
│   ├── 000002_seed_sample_data.up.sql      # DML: Populate lookups and sample sports science exercises
│   └── 000002_seed_sample_data.down.sql    # DML Rollback: Truncates and resets database tables
└── README.md                               # Project entrypoint
```

---

## Database Design & Architecture

The database is built on a highly normalized relational model to enforce integrity across the sports performance domain. 

### Core Features:
- **Scalability**: Designed with `BIGINT GENERATED ALWAYS AS IDENTITY` primary keys for fast index scanning and low memory overhead under 10,000+ exercises.
- **Many-to-Many Mappings**: Uses optimized junction tables for dynamic classification (Sports, Equipment, Movement Patterns, Training Methods, Physical Qualities, and Tags).
- **Advanced Performance Indexing**: Includes multi-column composite sorting indexes, reverse indexes to optimize bi-directional queries, and Full-Text Search via a generated GIN index on `tsvector` fields.

To see the detailed ER diagram, normalization analysis, and indexing strategy, please refer to [docs/architecture.md](docs/architecture.md).

---

## Setup & Migrations

### Requirements
- PostgreSQL 12+ (supports generated columns)

### Running Migrations

To apply the migrations manually, run the following commands in your PostgreSQL console or via your migration runner of choice:

#### 1. Apply Core Schema (Up)
```sql
\i migrations/000001_create_core_schema.up.sql
```

#### 2. Seed Sample Data (Up)
```sql
\i migrations/000002_seed_sample_data.up.sql
```

#### 3. Rollback (Down)
If you need to tear down the schema or reset the seed data:
```sql
-- Reset seed data
\i migrations/000002_seed_sample_data.down.sql

-- Drop core schema
\i migrations/000001_create_core_schema.down.sql
```

---

## Sample Queries

Here are common queries run by coaching software:

### 1. Find all exercises targeting a sport (e.g., "American Football") ordered by specificity and transfer index:
```sql
SELECT e.name, e.difficulty_level, esm.specificity_rating, esm.transfer_index
FROM exercises e
JOIN exercise_sport_mapping esm ON e.id = esm.exercise_id
JOIN sports s ON esm.sport_id = s.id
WHERE s.name = 'American Football'
ORDER BY esm.specificity_rating DESC, esm.transfer_index DESC;
```

### 2. Find compound exercises that train "Rate of Force Development" using "Bodyweight":
```sql
SELECT e.name, e.description
FROM exercises e
JOIN exercise_physical_qualities epq ON e.id = epq.exercise_id
JOIN physical_qualities pq ON epq.physical_quality_id = pq.id
JOIN exercise_equipment ee ON e.id = ee.exercise_id
JOIN equipment eq ON ee.equipment_id = eq.id
WHERE pq.name = 'Rate of Force Development'
  AND eq.name = 'Bodyweight'
  AND e.mechanics_type = 'Compound';
```

### 3. Full-Text search query matching "squat" or "bench":
```sql
SELECT name, description, ts_rank(search_vector, to_tsquery('english', 'squat | bench')) as rank
FROM exercises
WHERE search_vector @@ to_tsquery('english', 'squat | bench')
ORDER BY rank DESC;
```
