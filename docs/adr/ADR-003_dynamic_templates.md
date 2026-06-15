# ADR-003: Dynamic Constraint-Based Slots for Movement Templates

## Status
Accepted

## Context
Traditional S&C software hardcodes lists of exercises in workouts. This breaks down when an athlete lacks access to specific equipment (e.g. training at home vs. elite facility) or has an injury. We need a way to model workout templates that adapts dynamically.

## Decision
We chose to design `movement_templates` with slots that contain *requirements* (constraints on movement patterns, equipment, qualities, methods) rather than linking directly to static exercises. 

## Consequences
### Positive:
- **Automatic Substitutions**: The recommendation engine can resolve alternative exercises on the fly based on the available equipment list.
- **Coach Abstraction**: Coaches can program high-level plans (e.g. "Primary Bilateral Hinge Lift") and let the platform resolve the optimal exercise.
### Negative:
- **Query Latency**: Reassembling a template requires parsing multiple requirement tables and running matching calculations. This is mitigated by L1/L2 caching.
