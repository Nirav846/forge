# Phase 1: Current Routing Audit — Evidence

## Execution Path Trace

### Path 1: integration_workflow.py (lines 186-247)
**Hardcoded Deficit → Goal Mapping:**
```python
deficit_template_map = {
    "Power Deficit": "Power",
    "Acceleration Deficit": "Power",          # COLLAPSES to same goal
    "Mobility Restriction": "Shoulder Robustness"
}
```

**Problem:** Lines 191-195 show hardcoded dict. All power-related deficits map to single "Power" goal.

### Path 2: program_builder.py (lines 686-696)
**Hardcoded Deficit → Goal Mapping:**
```python
deficit_goal_map = {
    "Power Deficit": "Power",
    "Acceleration Deficit": "Power",          # DUPLICATE
    "Strength Deficit": "Strength",
    "Speed Deficit": "Power",                 # COLLAPSES
    "Mobility Restriction": "Power",
    "Rotational Power Deficit": "Power",      # COLLAPSES
    "Shoulder Robustness Deficit": "Strength"
}
```

**Problem:** Lines 687-696. 6 deficits collapse into 2 goals (Power, Strength).

### Path 3: recommendation_engine.py
**No hardcoded deficit routing.** Uses goal parameter directly (line 869: `goal=request.goal`).

### Path 4: deficit_detection_engine.py
**Deficit Production:** Lines 297-354.
- Produces: Power Deficit, Acceleration Deficit, Mobility Restriction, Speed Deficit, Strength Deficit, Rotational Power Deficit, Shoulder Robustness Deficit
- **No routing logic.** Returns DeficitDetail objects only.

---

## Routing Audit Table

| Deficit | program_builder.py | integration_workflow.py | Final Goal | Hardcoded? |
|---------|------------------|----------------------|-----------|-----------|
| Power Deficit | "Power" | "Power" | Power | ✓ YES |
| Acceleration Deficit | "Power" | "Power" | Power | ✓ YES |
| Strength Deficit | "Strength" | NOT MAPPED | Strength | ✓ YES |
| Speed Deficit | "Power" | NOT MAPPED | Power | ✓ YES |
| Mobility Restriction | "Power" | "Shoulder Robustness" | CONFLICTING | ✓ YES |
| Rotational Power Deficit | "Power" | NOT MAPPED | Power | ✓ YES |
| Shoulder Robustness Deficit | "Strength" | NOT MAPPED | Strength | ✓ YES |

**KEY FINDING:** 
- 2 different hardcoded mappings (program_builder vs integration_workflow)
- Mobility Restriction maps to DIFFERENT goals in each path
- 6 of 7 deficits collapse to Power/Strength (only 2 distinct outcomes)

---

## Phase 2: Database Mapping Audit

**Query Results:**
```
movement_templates TABLE (5 rows):
  1. Lower Body Power (All, American Football)
  2. Acceleration Development (Sprinters, Track & Field Sprinting)
  3. Rotational Power (Throwers, Track & Field Throws)
  4. Shoulder Robustness (All, Rugby)
  5. Reactive Agility (Guards/Forwards, Basketball)
```

```
deficit_movement_templates TABLE (0 rows):
  [EMPTY - NO MAPPINGS EXIST]
```

```
deficits TABLE (0 rows):
  [EMPTY - DATABASE NOT SEEDED]
```

```
benchmarks TABLE (0 rows):
  [EMPTY - DATABASE NOT SEEDED]
```

**Critical Finding:**
- Database tables exist but are **completely empty**
- No deficit → template mappings defined
- No assessment → deficit linkages defined
- **Only Mock repository has data** (deficit_detection_engine.py lines 145-213)

---

## Phase 3: Cricket Template Reachability

**Available Templates:**
1. Lower Body Power (role: All, sport: American Football)
2. Acceleration Development (role: Sprinters, sport: Track & Field)
3. Rotational Power (role: Throwers, sport: Track & Field)
4. Shoulder Robustness (role: All, sport: Rugby)
5. Reactive Agility (role: Guards/Forwards, sport: Basketball)

**Cricket Fast Bowler Reachability:**
- Sport: Cricket (but templates are for American Football, Track & Field, Rugby, Basketball)
- Role: Fast Bowler (but templates require Sprinters, Throwers, Guards/Forwards, or All)

**Result:** Fast Bowler can access only templates with `role = 'All'`:
- ✓ Lower Body Power
- ✓ Shoulder Robustness
- ✗ Acceleration Development (Sprinters only)
- ✗ Rotational Power (Throwers only)
- ✗ Reactive Agility (Guards/Forwards only)

**Reachability Matrix:**

| Role | Lower Body Power | Acceleration Dev | Rotational Power | Shoulder Robust | Reactive Agility |
|------|-----------------|-----------------|-----------------|-----------------|-----------------|
| Fast Bowler | ✓ All | ✗ Sprinters | ✗ Throwers | ✓ All | ✗ Guards/Fwd |
| Spinner | ✓ All | ✗ Sprinters | ✗ Throwers | ✓ All | ✗ Guards/Fwd |
| Batter | ✓ All | ✗ Sprinters | ✗ Throwers | ✓ All | ✗ Guards/Fwd |
| Wicket Keeper | ✓ All | ✗ Sprinters | ✗ Throwers | ✓ All | ✗ Guards/Fwd |
| All Rounder | ✓ All | ✗ Sprinters | ✗ Throwers | ✓ All | ✗ Guards/Fwd |

**Problem:** Cricket roles have NO sport-specific templates. All templates are for other sports.

---

## Summary of Findings

**Phase 1 - Routing Audit:**
- ✓ 2 hardcoded deficit→goal maps (conflicting)
- ✓ 6 deficits collapse to 2 goals
- ✓ NO database query used; hardcoded dicts only

**Phase 2 - Database Mapping:**
- ✗ deficit_movement_templates table is EMPTY
- ✗ deficits table is EMPTY
- ✗ benchmarks table is EMPTY
- ✓ Database schema exists but data not seeded

**Phase 3 - Reachability:**
- ✗ NO Cricket templates exist
- ✗ All 5 templates are for non-Cricket sports
- ✗ Cricket roles cannot reach 3 of 5 templates
- ✓ Only 2 templates (All-role) accessible to any Cricket role
