# ADR-005: SQL-Based S&C Specificity Scoring

## Status
Accepted

## Context
When ranking exercises for template slots, the system needs to evaluate relevance, sport specificity, transfer coefficients, tag matches, and mechanics alignment. Doing this in application memory requires fetching the entire exercise library and mapping metadata arrays to Python, which increases application memory overhead.

## Decision
We chose to execute the scoring and ranking calculations directly inside PostgreSQL queries using SQL math and `COALESCE` statements, returning a pre-sorted candidate pool.

## Consequences
### Positive:
- **Zero Memory Overhead**: The API server receives only the sorted, filtered candidate exercises, keeping memory utilization flat regardless of total catalog size.
- **Query Optimization**: PostgreSQL can optimize execution plans since all constraints and ordering variables are declared in a single query.
### Negative:
- **Database CPU Load**: Computation shifts to the database server. This is mitigated by cache blocks.
- **Algorithm Portability**: The S&C scoring logic is written in SQL syntax, making changes to the formula require database query updates rather than simple Python modifications.
