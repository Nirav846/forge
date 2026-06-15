# ADR-004: Dual-Layer Caching Strategy for Recommendation API

## Status
Accepted

## Context
Resolving exercise recommendations is a computationally heavy operation requiring multi-table SQL queries, enum conversions, and score sorts. Since exercise catalogs and template parameters change infrequently, re-evaluating requests on every API call is highly redundant and leads to high database CPU load under scale.

## Decision
We implemented a dual-layer caching architecture:
- **L1 Cache**: In-Memory local dictionary with TTL for rapid, single-node lookups.
- **L2 Cache**: Redis cache utilizing a SHA-256 hash of the normalized request parameters as keys.

## Consequences
### Positive:
- **Sub-millisecond Latencies**: Cache hits return resolved plans instantly, avoiding database calls entirely.
- **Scalability**: Mitigates database congestion during peak team sync sessions (e.g. 50 athletes loading workouts at the same time).
### Negative:
- **Stale Data Risks**: Changes to template requirements or exercise entries are not immediately visible until the 5-minute TTL expires, unless a cache clear/invalidation route is explicitly invoked.
