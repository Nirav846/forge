# ADR-006: Relational Diagnostic Engine

## Status
Accepted

## Context
In athletic performance systems, translating raw assessment test scores into diagnosed deficits and corrective movement templates has traditionally been handled by complex application-layer switch-case statements, if-else chains, or hardcoded rules. However, this logic becomes brittle and hard to maintain as more sports, roles, and tests are added. We need a flexible, data-driven way to evaluate scores, map deficits, and prescribe templates dynamically.

## Decision
We decided to implement a **Relational Diagnostic Engine** where all diagnostic routing, benchmark ranges, deficits, and corrective mappings are stored in the database in 3NF and resolved dynamically via SQL range joins:
- Benchmark classifications are determined by checking which range ($min\_value \le score \le max\_value$) the raw test score falls into.
- Deficits, corrective training methods, and movement templates are resolved using standard SQL foreign keys and junction table joins.
- PostgreSQL aggregate functions like `ARRAY_AGG(DISTINCT ...)` are utilized to compile lists of recommended methods and templates in a single query.

## Consequences
### Positive:
- **Zero Application Code Changes for New Sports**: Adding a new sport (e.g., Tennis or Badminton) or test only requires database insertions in the respective lookup tables. The backend service code remains unchanged.
- **Single-Query Resolution**: Resolving the entire diagnostic and prescription chain (Assessment Score $\to$ Benchmark $\to$ Deficit $\to$ Training Methods $\to$ Movement Templates) is done in a single PostgreSQL query, reducing database roundtrips.
- **Relational Integrity**: Foreign keys ensure that no orphaned deficits or invalid training methods can be set.

### Negative:
- **Database Load**: Moving matching logic into SQL queries increases database CPU utilization, although this is heavily mitigated by indexing on `assessment_id` and `min_value`/`max_value`.
- **Query Complexity**: The diagnostic query is complex and relies on multiple joins, which requires developers to write and test raw SQL carefully.
