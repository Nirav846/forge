# ADR-002: Normalized Lookup Tables for Sports Science Taxonomies

## Status
Accepted

## Context
Sports science structures (sports, equipment, movement patterns, training methods) are highly dynamic. Coaches regularly adopt new equipment (e.g. flywheels, specialty bars) or categorizations. Using hardcoded database `ENUM` types requires DDL changes (`ALTER TYPE ... ADD VALUE`), which can cause database locks in production.

## Decision
We chose to implement normalized lookup tables (e.g., `equipment`, `movement_patterns`, `sports`) and link them to exercises using many-to-many junction tables, instead of utilizing database-level ENUM types.

## Consequences
### Positive:
- **High Extensibility**: S&C administrators can add new equipment, sports, or movement patterns via standard SQL `INSERT` commands or API forms, completely avoiding schema locking.
- **Relational Integrity**: Allows linking metadata directly to lookup values (e.g., equipment category, sport classification).
### Negative:
- **Schema Complexity**: Increases the number of tables and necessitates write transactions across junction tables during imports.
