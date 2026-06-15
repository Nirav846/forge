# ADR-001: Primary Key Strategy

## Status
Accepted

## Context
In S&C platforms, lookups and core lists (exercises, sports, equipment, etc.) contain moderate quantities of records (typically under 100,000). However, analytical queries require deep, multi-table many-to-many joins. We must select a primary key strategy that maximizes database page density, minimizes index sizes, and speeds up joins.

## Decision
We chose to use `BIGINT GENERATED ALWAYS AS IDENTITY` for all lookup and core table primary keys, rather than random or ordered `UUID`s.

## Consequences
### Positive:
- **Join Performance**: Integer comparisons are executed natively at CPU level and are significantly faster than 16-byte UUID comparisons.
- **Index Sizes**: `BIGINT` (8 bytes) indexes are half the size of `UUID` (16 bytes) indexes, allowing more indexes to fit inside PostgreSQL shared buffers memory.
- **Sequence Density**: Identity sequences prevent index page fragmentation, maintaining high density and fast sequential scans.
### Negative:
- **Distributed Synchronization**: If database shards or multi-datacenter writes are required, auto-incrementing identity columns can cause ID collisions, requiring complex synchronization or sequence offsets.
