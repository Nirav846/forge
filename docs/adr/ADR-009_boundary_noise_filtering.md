# ADR-009: Borderline Benchmark Proximity Penalties

## Status
Accepted

## Context
Physical testing (e.g. Countermovement Jumps, Deadlifts) has intrinsic margins of error due to sensor calibration, daily athlete sleep fluctuations, or coaching timer variations. If an athlete's test score lies right next to a classification boundary (e.g., scoring $34.8\text{ cm}$ on a CMJ where the Poor threshold is $<35\text{ cm}$), treating the diagnosis with absolute certainty can lead to incorrect programming.

## Decision
We implemented a **boundary proximity penalty** in the service layer. If an athlete's score falls within $5\%$ of a benchmark classification boundary (either a `min_value` or a `max_value`), we apply a flat **$-10\%$** penalty to the diagnostic confidence.

$$\text{Proximity} = \frac{|\text{Score} - \text{Boundary}|}{\text{Boundary}} \le 0.05 \implies \text{Confidence} = \text{Confidence} - 10$$

## Consequences
### Positive:
- **Noise Filtering**: Compensates for daily athlete performance variance and equipment inaccuracy by highlighting "borderline" cases.
- **Improved Coaching Intuition**: Flags cases where coaches should double-check mechanics rather than relying blindly on programmatic prescriptions.
### Negative:
- **Boundary Range Sensitivity**: For very narrow ranges (where the distance between min and max bounds is less than $10\%$), every score in that classification will trigger the penalty. This is solved by using wider, standardized population ranges or setting soft bounds.
