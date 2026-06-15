# Forge Cricket S&C Knowledge Graph Seeding Spec
**Author: Lead Strength and Conditioning Coach**  
**Date: 2026-06-15**

This document details the S&C science, metrics, mapping, and testing thresholds implemented in the comprehensive **Cricket Knowledge Graph Seed** ([`examples/cricket_knowledge_graph_seed.json`](../examples/cricket_knowledge_graph_seed.json)).

---

## 1. Athlete Role Needs Analysis Mapping

To build targeted athletic profiles, the 5 core Cricket roles are mapped to specific biomechanical performance drivers and testing protocols:

| Role | Performance Driver | Priority | Target Assessment | Assessment Metric |
| :--- | :--- | :--- | :--- | :--- |
| **Fast Bowler** | Power | Primary | CMJ / Broad Jump | cm / m |
| | Speed | Primary | 20m Sprint | s |
| | Shoulder Robustness | Primary | Pull Up | reps |
| | Strength | Secondary | Trap Bar Deadlift | kg |
| | Work Capacity | Secondary | Yo-Yo IR2 / Shuttle | m |
| **Spinner** | Rotational Power | Primary | Rotational Med Ball Throw | m/s |
| | Shoulder Robustness | Primary | Pull Up | reps |
| | Strength | Secondary | Trap Bar Deadlift | kg |
| **Batter** | Acceleration | Primary | 10m Sprint | s |
| | Speed | Primary | 20m Sprint | s |
| | Reactive Agility | Primary | CMJ / Pro Agility | cm |
| **Wicket Keeper** | Reactive Agility | Primary | CMJ / Reactive Shuttle | cm |
| | Strength | Primary | Trap Bar Deadlift | kg |
| **All Rounder** | Work Capacity | Primary | Yo-Yo IR2 | m |
| | Strength | Primary | Trap Bar Deadlift | kg |
| | Power | Primary | CMJ | cm |

---

## 2. Testing Benchmarks & Threshold Ranges

Testing results are evaluated against population thresholds to classify performance and detect deficits. 

### A. Jump & Power Thresholds
- **Countermovement Jump (CMJ)**:
  - **Elite**: $\ge 55 \text{ cm}$
  - **Optimal**: $45 - 54.99 \text{ cm}$
  - **Sub-optimal**: $35 - 44.99 \text{ cm}$
  - **Poor**: $< 35 \text{ cm}$
- **Broad Jump**:
  - **Elite**: $\ge 2.60 \text{ m}$
  - **Optimal**: $2.20 - 2.59 \text{ m}$
  - **Sub-optimal**: $1.80 - 2.19 \text{ m}$
  - **Poor**: $< 1.80 \text{ m}$

### B. Speed & Acceleration Thresholds (Lower Time is Better)
- **10m Acceleration Sprint**:
  - **Elite**: $\le 1.60 \text{ s}$
  - **Optimal**: $1.61 - 1.80 \text{ s}$
  - **Sub-optimal**: $1.81 - 2.00 \text{ s}$
  - **Poor**: $\ge 2.01 \text{ s}$
- **20m Sprint**:
  - **Elite**: $\le 2.80 \text{ s}$
  - **Optimal**: $2.81 - 3.10 \text{ s}$
  - **Sub-optimal**: $3.11 - 3.40 \text{ s}$
  - **Poor**: $\ge 3.41 \text{ s}$

### C. Strength & Ballistic Thresholds
- **Trap Bar Deadlift (1RM Equivalent)**:
  - **Elite**: $\ge 200 \text{ kg}$
  - **Optimal**: $160 - 199.99 \text{ kg}$
  - **Sub-optimal**: $120 - 159.99 \text{ kg}$
  - **Poor**: $< 120 \text{ kg}$
- **Pull Up (Max Continuous Reps)**:
  - **Elite**: $\ge 18 \text{ reps}$
  - **Optimal**: $12 - 17.99 \text{ reps}$
  - **Sub-optimal**: $6 - 11.99 \text{ reps}$
  - **Poor**: $< 6 \text{ reps}$
- **Rotational Medicine Ball Throw (Transverse Power)**:
  - **Elite**: $\ge 13.0 \text{ m/s}$
  - **Optimal**: $11.0 - 12.99 \text{ m/s}$
  - **Sub-optimal**: $9.0 - 10.99 \text{ m/s}$
  - **Poor**: $< 9.0 \text{ m/s}$

---

## 3. Deficit Resolution & S&C Prescriptions

When a physical test score falls into the **Sub-optimal** or **Poor** range, the system diagnoses a deficit and maps it to corrective training methods and templates:

1. **Power Deficit** (from poor CMJ/Broad Jump):
   - *Training Methods*: Dynamic Effort, Plyometrics, Rotational Power.
   - *Templates*: Lower Body Power, Rotational Power.
2. **Strength Deficit** (from poor Deadlift/Pull Ups):
   - *Training Methods*: Max Strength.
   - *Templates*: Lower Body Power.
3. **Acceleration Deficit** (from poor 10m Sprint):
   - *Training Methods*: Sprint Training, COD Training.
   - *Templates*: Acceleration Development.
4. **Speed Deficit** (from poor 20m Sprint):
   - *Training Methods*: Sprint Training.
   - *Templates*: Acceleration Development.
5. **Mobility Restriction** (from poor Broad Jump mechanics):
   - *Training Methods*: Mobility.
   - *Templates*: Shoulder Robustness (which contains scapular/rotator cuff mobility accessories).

---

## 4. Running the Validation Script

The script [`src/validate_knowledge_graph.py`](../src/validate_knowledge_graph.py) is a standalone auditor that validates JSON structures, verifies enum constraints, and logs errors.

To execute the validation audit:
```bash
python src/validate_knowledge_graph.py
```
This script writes logs to [`logs/validation.log`](../logs/validation.log) and outputs a console summary showing the counts of roles, assessments, warnings, and errors.
