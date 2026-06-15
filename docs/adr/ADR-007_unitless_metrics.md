# ADR-007: Unitless Testing Metrics

## Status
Accepted

## Context
Athletic assessments utilize diverse units of measurement: vertical jump height is measured in centimeters (`cm`), absolute strength in kilograms (`kg`), sprint time in seconds (`s`), and force plate output in Newtons (`N`). If the database or diagnostic engine enforces strict unit types or attempts inline unit conversions (e.g. converting inches to centimeters or pounds to kilograms) during benchmark range checks, it introduces significant runtime overhead and parsing logic.

## Decision
We decided to adopt a **Unitless Testing Metrics** strategy for benchmark evaluations:
- The `assessments` table stores a descriptive `metric_unit` string (e.g., `'cm'`, `'kg'`, `'s'`, `'N'`) solely for front-end rendering and coach-facing labels.
- The `benchmarks` table stores all range boundaries (`min_value`, `max_value`) as unitless `NUMERIC(10,2)` values.
- The deficit detection and recommendation engines process all raw test scores and benchmark limits as unitless numbers, relying on the client application or ingestion pipeline to supply scores in the expected standardized unit.

## Consequences
### Positive:
- **Simplified DB Joins**: Range queries run using simple numeric comparisons ($score \ge min\_value$ and $score \le max\_value$) without unit conversion functions, maximizing query performance and index utilization.
- **Dynamic Extensibility**: Easily accommodates new, unconventional testing protocols (e.g., sleep duration in hours, wellness scores on a 1-10 scale) without modifying the schema or code.
- **Low Code Complexity**: No unit conversion tables or dictionaries are needed in the backend codebase.

### Negative:
- **Ingestion Responsibility**: The responsibility of validating and converting incoming metrics (e.g., converting a coach's input of imperial pounds to kilograms) is shifted to the ETL ingestion pipeline or front-end client.
- **Accidental Mismatches**: If an ingestion source uploads a CMJ score in inches instead of centimeters, the system will evaluate it against centimeter-based benchmarks without warning, leading to false diagnoses.
