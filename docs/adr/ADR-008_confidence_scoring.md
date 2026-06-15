# ADR-008: Heuristic Confidence Weighting for Physical Diagnostics

## Status
Accepted

## Context
When diagnosing physical deficits (e.g. Power Deficit, Strength Deficit) from athlete test scores, single-test assessments can contain execution variance, athlete fatigue, or metric noise. We need a way to quantify how confident the S&C engine is of a diagnosed deficit to avoid prescribing redundant or wrong programs.

## Decision
We implemented a dynamic confidence-scoring heuristic in the service layer:
- **Baseline Confidence ($80\%$)**: Assigned if a single test indicates a deficit.
- **Cross-Validation Boost ($+12\%$)**: If multiple distinct test protocols target the same deficit (e.g., both `CMJ` and `Broad Jump` showing a Power Deficit), the confidence is boosted to a maximum of **$92\%$**.
- **Conflict Reduction ($60\%$)**: If one test shows a deficit while another related test shows optimal capability, the confidence is reduced to **$60\%$** to reflect contradictory data.

## Consequences
### Positive:
- **High Diagnostics Reliability**: Prevents premature training program adjustments based on a single outlier test score.
- **Explainable AI**: Provides coaches with a clear percentage indicating the strength of the system's diagnosis.
### Negative:
- **Algorithmic Complexity**: Requires keeping track of test mappings (many-to-one deficits) within the service layer.
- **Testing Dependency**: Requires coaches to run multiple testing batteries to unlock the highest confidence classifications.
