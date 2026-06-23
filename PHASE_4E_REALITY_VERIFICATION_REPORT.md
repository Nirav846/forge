# PHASE 4E: Reality Verification Audit Report
## Generated: 2026-06-16

---

## A. Actual Routing Source

### Database State
| Table | Row Count | Status |
|-------|-----------|--------|
| deficits | 0 | EMPTY |
| benchmarks | 0 | EMPTY |
| deficit_movement_templates | 0 | EMPTY |
| movement_templates | 5 | POPULATED |

### Environment State
- `DATABASE_URL` environment variable: **NOT SET**
- PostgreSQL reachable: YES (localhost, password auth)
- Application mode: **MOCK (no DATABASE_URL)**

### Routing Source Determination

**Current routing source: MOCK REPOSITORY ONLY**

Evidence:
1. `DATABASE_URL` env var is empty
2. `program_builder.py:668` checks `if db_url and db_pool:` → FALSE
3. `integration_workflow.py:177` directly instantiates `MockBenchmarkRepository()`
4. All routing calls `MockExerciseRepository.get_templates_for_deficit()`

**PostgreSQL path is DEAD CODE** (unreachable without DATABASE_URL).

### Hidden Routing Layers Found

| Location | Type | Content |
|----------|------|---------|
| `recommendation_engine.py:358-366` | **HARDCODED DICT** | `mapping = {"Power Deficit": [1], ...}` |
| `recommendation_engine.py:348-356` | **HARDCODED DICT** | `templates = {1: {...}, 2: {...}, ...}` |
| `deficit_detection_engine.py:149-213` | **HARDCODED DICT** | Mock benchmarks with deficit_name fields |
| `recommendation_stress_test.py:608,615` | **DOCUMENTATION** | References old hardcoded maps (cosmetic) |

**CRITICAL FINDING:** The "database-driven" routing is actually **mock-dict-driven**. We replaced one hardcoded dict with another hardcoded dict inside `MockExerciseRepository.get_templates_for_deficit()`.

---

## B. Full Execution Path Trace

### Trace: Power Deficit

```
Assessment: CMJ = 38cm (Sub-optimal)
    ↓
MockBenchmarkRepository.get_score_classification("cmj", 38)
    ↓ Returns: {"deficit_name": "Power Deficit", ...}
DeficitDetectionService.detect_deficits()
    ↓ Returns: [DeficitDetail(deficit="Power Deficit", severity="High", confidence=92)]
program_builder.py:resolve_athlete_deficits_and_goal()
    ↓ Line 700: exercise_repo = MockExerciseRepository()
    ↓ Line 702: templates = await exercise_repo.get_templates_for_deficit("Power Deficit")
    ↓ recommendation_engine.py:358-366: mapping["Power Deficit"] = [1]
    ↓ Returns: [{"id": 1, "name": "Power", ...}]
    ↓ Line 706: selected_template = templates[0]
    ↓ Line 707: goal = "Power"
    ↓
recommendation_engine.py:get_template("Cricket", "Fast Bowler", "Power")
    ↓ Line 387: s_clean = "cricket", r_clean = "fast bowler", g_clean = "power"
    ↓ Line 388-395: Matches "fast" in r_clean AND g_clean in ["power", ...]
    ↓ Returns: {"id": 100, "name": "Cricket Fast Bowler Power", ...}
    ↓
recommendation_engine.py:get_slots(100)
    ↓ Returns: [Slot 201, 202, 203, 204]
    ↓
recommendation_engine.py:get_ranked_exercises(201, 100, ...)
    ↓ Returns: [Trap Bar Jump Squat, Mid-Thigh Pull, Power Clean, ...]
```

### Trace: Mobility Restriction

```
Assessment: Broad Jump = 2.10m (Sub-optimal)
    ↓
MockBenchmarkRepository.get_score_classification("broad jump", 2.10)
    ↓ Returns: {"deficit_name": "Mobility Restriction", ...}
program_builder.py:resolve_athlete_deficits_and_goal()
    ↓ templates = get_templates_for_deficit("Mobility Restriction")
    ↓ recommendation_engine.py:361: mapping["Mobility Restriction"] = [4]
    ↓ Returns: [{"id": 4, "name": "Shoulder Robustness", ...}]
    ↓ goal = "Shoulder Robustness"
    ↓
recommendation_engine.py:get_template("Cricket", "Fast Bowler", "Shoulder Robustness")
    ↓ Line 388: "fast" in r_clean, g_clean in ["shoulder robustness", ...]
    ↓ Returns: {"id": 100, "name": "Cricket Fast Bowler Power", ...}
```

**NOTE:** Mobility Restriction → Shoulder Robustness goal, but the mock `get_template()` still returns Cricket Fast Bowler Power template because the goal normalization logic maps it to the same Cricket template.

### Trace: Acceleration Deficit

```
Assessment: 10m Sprint = 1.95s (Sub-optimal)
    ↓
MockBenchmarkRepository.get_score_classification("10m sprint", 1.95)
    ↓ Returns: {"deficit_name": "Acceleration Deficit", ...}
program_builder.py:resolve_athlete_deficits_and_goal()
    ↓ templates = get_templates_for_deficit("Acceleration Deficit")
    ↓ recommendation_engine.py:360: mapping["Acceleration Deficit"] = [2]
    ↓ Returns: [{"id": 2, "name": "Acceleration Development", ...}]
    ↓ goal = "Acceleration Development"
    ↓
recommendation_engine.py:get_template("Cricket", "Fast Bowler", "Acceleration Development")
    ↓ Line 388: "fast" in r_clean, g_clean in ["acceleration development", "acceleration"]
    ↓ Returns: {"id": 100, "name": "Cricket Fast Bowler Power", ...}
```

### Trace: Rotational Power Deficit

```
Assessment: Rotational Med Ball Throw = 4.5 m/s (Sub-optimal)
    ↓
MockBenchmarkRepository.get_score_classification("rotational med ball throw", 4.5)
    ↓ Returns: {"deficit_name": "Rotational Power Deficit", ...}
program_builder.py:resolve_athlete_deficits_and_goal()
    ↓ templates = get_templates_for_deficit("Rotational Power Deficit")
    ↓ recommendation_engine.py:364: mapping["Rotational Power Deficit"] = [3]
    ↓ Returns: [{"id": 3, "name": "Rotational Power", ...}]
    ↓ goal = "Rotational Power"
    ↓
recommendation_engine.py:get_template("Cricket", "Fast Bowler", "Rotational Power")
    ↓ Line 388: "fast" in r_clean, g_clean = "rotational power"
    ↓ **NO MATCH** - g_clean not in ["power", "shoulder robustness", "acceleration development", "acceleration"]
    ↓ Returns: None
    ↓
recommendation_engine.py:870: raises HTTPException 404 "No movement template found"
```

**CRITICAL BUG FOUND:** Rotational Power Deficit → 404 error for Fast Bowler because mock `get_template()` doesn't support "rotational power" goal for Fast Bowler role.

---

## C. Remaining Hardcoded Mappings

### 1. MockExerciseRepository.get_templates_for_deficit() (recommendation_engine.py:358-366)
```python
mapping = {
    "Power Deficit": [1],
    "Acceleration Deficit": [2],
    "Mobility Restriction": [4],
    "Speed Deficit": [2],
    "Strength Deficit": [1],
    "Rotational Power Deficit": [3],
    "Shoulder Robustness Deficit": [4]
}
```
**Status:** NEW hardcoded mapping (replaced old one, same problem)

### 2. MockExerciseRepository.get_template() goal normalization (recommendation_engine.py:376-385)
```python
if g_clean == "power" or g_clean == "lower body power":
    g_clean = "power"
elif g_clean == "acceleration development" or g_clean == "acceleration":
    g_clean = "acceleration"
elif g_clean == "rotational power":
    g_clean = "rotational power"
elif g_clean == "shoulder robustness":
    g_clean = "shoulder robustness"
```
**Status:** Required for backward compatibility with goal-based API

### 3. MockExerciseRepository.get_template() role/goal matching (recommendation_engine.py:387-421)
```python
if s_clean == "cricket":
    if "bowl" in r_clean or "fast" in r_clean:
        if g_clean in ["power", "shoulder robustness", "acceleration development", "acceleration"]:
            return {"id": 100, ...}
    elif "spin" in r_clean:
        if g_clean in ["power", "rotational power", "shoulder robustness"]:
            return {"id": 101, ...}
    elif "bat" in r_clean:
        if g_clean in ["power", "strength", "acceleration", "acceleration development"]:
            return {"id": 102, ...}
```
**Status:** CRITICAL BUG - Missing "rotational power" for Fast Bowler, missing "acceleration" for Spinner

### 4. MockBenchmarkRepository benchmarks (deficit_detection_engine.py:149-213)
```python
self.benchmarks = {
    "cmj": {"deficit_name": "Power Deficit", ...},
    "broad jump": {"deficit_name": "Mobility Restriction", ...},
    ...
}
```
**Status:** NECESSARY for mock mode - assessment → deficit detection requires this

---

## D. Generic Template Reachability

### Fast Bowler
| Template | Reachable? | Reason |
|----------|------------|--------|
| Power (1) | ✅ YES | goal="power" maps to template 100 |
| Acceleration Development (2) | ✅ YES | goal="acceleration" maps to template 100 |
| Rotational Power (3) | ❌ NO | g_clean="rotational power" not in Fast Bowler's goal list |
| Shoulder Robustness (4) | ✅ YES | goal="shoulder robustness" maps to template 100 |

**BUG:** Fast Bowler cannot receive Rotational Power training despite deficit.

### Spinner
| Template | Reachable? | Reason |
|----------|------------|--------|
| Power (1) | ✅ YES | goal="power" maps to template 101 |
| Acceleration Development (2) | ❌ NO | g_clean="acceleration" not in Spinner's goal list |
| Rotational Power (3) | ✅ YES | goal="rotational power" maps to template 101 |
| Shoulder Robustness (4) | ✅ YES | goal="shoulder robustness" maps to template 101 |

**BUG:** Spinner cannot receive Acceleration Development training.

### Batter
| Template | Reachable? | Reason |
|----------|------------|--------|
| Power (1) | ✅ YES | goal="power" maps to template 102 |
| Acceleration Development (2) | ✅ YES | goal="acceleration" maps to template 102 |
| Rotational Power (3) | ❌ NO | g_clean="rotational power" not in Batter's goal list |
| Shoulder Robustness (4) | ❌ NO | g_clean="shoulder robustness" not in Batter's goal list |

**BUG:** Batter cannot receive Rotational Power or Shoulder Robustness training.

### Wicket Keeper
| Template | Reachable? | Reason |
|----------|------------|--------|
| Power (1) | ✅ YES | goal="power" maps to template 103 |
| Acceleration Development (2) | ✅ YES | goal="acceleration" maps to template 103 |
| Rotational Power (3) | ❌ NO | g_clean="rotational power" not in WK's goal list |
| Shoulder Robustness (4) | ✅ YES | goal="shoulder robustness" maps to template 103 |

### All Rounder
| Template | Reachable? | Reason |
|----------|------------|--------|
| Power (1) | ✅ YES | goal="power" maps to template 104 |
| Acceleration Development (2) | ✅ YES | goal="acceleration" maps to template 104 |
| Rotational Power (3) | ✅ YES | goal="rotational power" maps to template 104 |
| Shoulder Robustness (4) | ✅ YES | goal="shoulder robustness" maps to template 104 |

**BEST COVERAGE:** All Rounder has access to all 4 template types.

---

## E. Architecture Score (Evidence-Based)

### Template Coverage (20 points)
- 5 movement_templates exist
- 0 Cricket-specific templates in DB (all are American Football, Track & Field, Rugby, Basketball)
- Mock provides 3 Cricket templates (100, 101, 102) + 2 new ones (103, 104)
- **Score: 10/20** (templates exist but not in DB, mock coverage partial)

### Deficit Differentiation (20 points)
- 7 deficits defined in mock
- 0 deficits in DB
- All 7 deficits have template mappings in mock dict
- **Score: 15/20** (differentiation works in mock but not validated against DB)

### Exercise Pool Depth (20 points)
- 29 mock exercises defined
- All slots have exercise pools
- Development level + tech_diff gating implemented
- **Score: 18/20** (good depth, proper filtering)

### Athletic Quality Coverage (20 points)
- 7 physical qualities assessed (CMJ, Broad Jump, 10m, 20m, Pull Up, Deadlift, Rotational Throw)
- Benchmarks defined for all 7
- Cross-validation logic for Power Deficit
- **Score: 16/20** (good coverage, but mock-only)

### Cricket Specificity (10 points)
- 5 Cricket roles defined
- 5 Cricket mock templates (100-104)
- 0 Cricket templates in movement_templates table
- **Score: 4/10** (mock-only, not in DB)

### Athlete Safety (10 points)
- Development level gating implemented
- Technical difficulty caps enforced
- Equipment filtering works
- **Score: 9/10** (safety gates working)

**TOTAL: 72/100** (up from 35/100 before refactor, but still mock-dependent)

---

## F. Recommendation

### ❌ DO NOT PROCEED TO PHASE 5

### Blockers:

1. **DATABASE_URL not set** - Application runs in mock mode, PostgreSQL path is dead code
2. **Hardcoded dict inside MockExerciseRepository** - We replaced one hardcoded mapping with another
3. **Missing goal support in mock get_template()** - Rotational Power causes 404 for Fast Bowler
4. **Database tables empty** - deficits, benchmarks, deficit_movement_templates all have 0 rows

### Required Before Phase 5:

1. **Fix mock get_template() goal lists** - Add "rotational power" to Fast Bowler, "acceleration" to Spinner
2. **Set DATABASE_URL** for PostgreSQL testing
3. **Seed database tables** using migration 000021 (with constraint fixes)
4. **Verify PostgreSQL routing** works end-to-end with real data
5. **Remove or document** the mock mapping dict as fallback only

### Architectural Debt:

The refactor **did not achieve its stated goal**. The code still contains hardcoded routing logic:
- It moved from `deficit_goal_map` in program_builder.py
- To `mapping` dict in MockExerciseRepository.get_templates_for_deficit()

The database is NOT the source of truth - the mock dict is.

**To complete Phase 4 properly:**
1. Seed database with real deficit→template mappings
2. Run application with DATABASE_URL set
3. Verify PostgreSQL routing overrides mock
4. Delete or deprecate mock mapping dict
