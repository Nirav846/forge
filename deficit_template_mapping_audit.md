# Deficit → Goal → Template Mapping Audit

**Date:** 2026-06-16
**Scope:** Every deficit produced by the deficit engine traced through to goal resolution, template selection, and slot structure.

---

## 1. Defect Engine: Exact Deficits Produced

Source: `deficit_detection_engine.py:123-191` — `MockBenchmarkRepository.benchmarks`

| # | Assessment Name | Produced Deficit | Deficit Description | File:Line |
|---|---|---|---|---|
| 1 | `cmj` | **Power Deficit** | "Lack of vertical power." | `deficit_detection_engine.py:129` |
| 2 | `broad jump` | **Mobility Restriction** | "Exhibits joint restriction limiting triple extension." | `deficit_detection_engine.py:138` |
| 3 | `10m sprint` | **Acceleration Deficit** | "Sub-optimal acceleration mechanics." | `deficit_detection_engine.py:147` |
| 4 | `20m sprint` | **Speed Deficit** | "Sub-optimal max linear running speeds." | `deficit_detection_engine.py:156` |
| 5 | `trap bar deadlift` | **Strength Deficit** | "Falls below absolute lower body force requirements." | `deficit_detection_engine.py:165` |
| 6 | `rotational med ball throw` | **Rotational Power Deficit** | "Lack of rotational power / explosive transverse torque." | `deficit_detection_engine.py:174` |
| 7 | `pull up` | **Shoulder Robustness Deficit** | "Lack of upper body pulling strength or scapular stability." | `deficit_detection_engine.py:183` |

**Total deficits in engine:** 7

---

## 2. Mapping Chains — Deficit → Goal → Template → Slots

### 2A. Integration Workflow Path

Source: `integration_workflow.py:191-244`

```python
deficit_template_map = {
    "Power Deficit": "Power",
    "Acceleration Deficit": "Power",
    "Mobility Restriction": "Shoulder Robustness"
}
# Fallthrough: deficits not in map → "Power" (line 199)
```

### 2B. Program Builder Path

Source: `program_builder.py:674-683`

```python
deficit_goal_map = {
    "Power Deficit": "Power",
    "Acceleration Deficit": "Power",
    "Strength Deficit": "Strength",
    "Speed Deficit": "Power",
    "Mobility Restriction": "Power",
    "Rotational Power Deficit": "Power",
    "Shoulder Robustness Deficit": "Strength"
}
# Fallthrough: deficits not in map → "Power" (line 683)
```

### 2C. Template Resolution by Goal

Source: `recommendation_engine.py:267-296` — `MockExerciseRepository.get_template()`

| Role | Goal | Template ID | Template Name | Slots |
|------|------|------------|---------------|-------|
| Fast Bowler | `power` | 100 | Cricket Fast Bowler Power | 201, 202, 203, 204 |
| Fast Bowler | anything else | — | **404 NOT FOUND** | — |
| Spinner | `power` | 101 | Cricket Spinner Rotational Power | 301, 302, 303, 304 |
| Spinner | `rotational power` | 101 | Cricket Spinner Rotational Power | 301, 302, 303, 304 |
| Spinner | anything else | — | **404 NOT FOUND** | — |
| Batter | `power` | 102 | Cricket Batter Strength/Power | 401, 402, 403, 404 |
| Batter | `strength` | 102 | Cricket Batter Strength/Power | 401, 402, 403, 404 |
| Batter | `acceleration` | 102 | Cricket Batter Strength/Power | 401, 402, 403, 404 |
| Batter | anything else | — | **404 NOT FOUND** | — |
| Wicket Keeper | any goal | — | **404 NOT FOUND** | — |
| All Rounder | any goal | — | **404 NOT FOUND** | — |

---

## 3. Full Deficit Traceability Matrix

### Integration Workflow Path

| Deficit | Expected Goal | Actual Goal | Expected Template | Actual Template | Status |
|---------|--------------|-------------|-------------------|-----------------|--------|
| Power Deficit | Power Training | **Power** | Power-specific template | FB: Cricket Fast Bowler Power ✓ / Batter: Cricket Batter Strength/Power ✓ / Spinner: Cricket Spinner Rotational Power ✓ | **PASS** — resolves correctly for all 3 roles |
| Acceleration Deficit | **Acceleration/Sprint** Training | **Power** | Sprint/Accel template (doesn't exist) | Same as Power Deficit per role | **FAIL** — wrong training type; acceleration deficit gets power training |
| Mobility Restriction | **Lower body power** or **Horizontal power** training | **Shoulder Robustness** | Horizontal Power template (doesn't exist) | **404 NOT FOUND** for all roles | **CRITICAL FAIL** — maps lower body deficit to upper body goal; template not found → deficit silently dropped |
| Strength Deficit | **Strength** Training | **Power** (fallback) | Max Strength template (exists in DB as "Lower Body Power") | Same as Power Deficit per role | **FAIL** — strength deficit gets power training in integration workflow |
| Speed Deficit | **Speed/Max Velocity** Training | **Power** (fallback) | Speed template (doesn't exist) | Same as Power Deficit per role | **FAIL** — speed deficit gets power training |
| Rotational Power Deficit | **Rotational Power** Training | **Power** (fallback) | Rotational Power template (exists as "Cricket Spinner Rotational Power") | FB: Cricket Fast Bowler Power (wrong!) / Batter: Cricket Batter Strength/Power (wrong!) / Spinner: Cricket Spinner Rotational Power ✓ | **PARTIAL FAIL** — only Spinner gets correct template by luck |
| Shoulder Robustness Deficit | **Strength** or **Shoulder** Training | **Power** (fallback) | Shoulder Robustness template (exists in DB, not in mock) | Same as Power Deficit per role | **FAIL** — shoulder deficit gets power training |

### Program Builder Path

| Deficit | Expected Goal | Actual Goal | Expected Template | Actual Template | Status |
|---------|--------------|-------------|-------------------|-----------------|--------|
| Power Deficit | Power Training | **Power** | Power-specific template | Same as Integration Workflow | **PASS** |
| Acceleration Deficit | Acceleration/Sprint Training | **Power** | Sprint/Accel template (doesn't exist) | Same as Integration Workflow | **FAIL** — same issue |
| Mobility Restriction | Lower body / Horizontal power training | **Power** | Horizontal Power template (doesn't exist) | Same as Power Deficit per role | **WRONG DEFICIT NAME but same outcome** — at least "Power" is lower-body training |
| Strength Deficit | Strength Training | **Strength** | Max Strength template | **Batter**: Cricket Batter Strength/Power ✓ / **FB**: **404 NOT FOUND** / **Spinner**: **404 NOT FOUND** | **PARTIAL FAIL** — only Batter has a template for "Strength" goal |
| Speed Deficit | Speed/Max Velocity Training | **Power** | Speed template (doesn't exist) | Same as Power Deficit per role | **FAIL** |
| Rotational Power Deficit | Rotational Power Training | **Power** | Rotational Power template | Same as Power Deficit per role | **FAIL** — only Spinner incidentally correct |
| Shoulder Robustness Deficit | Strength or Shoulder Training | **Strength** | Max Strength template | **Batter**: Cricket Batter Strength/Power ✓ / **FB**: **404 NOT FOUND** / **Spinner**: **404 NOT FOUND** | **PARTIAL FAIL** — only Batter resolves |

---

## 4. Verdict by Deficit

### Power Deficit — ⚠️ PARTIALLY CORRECT
- Resolves correctly for all 3 roles via both paths
- **Problem:** Same template used for Power Deficit, Acceleration Deficit, and Speed Deficit — no differentiation between vertical power, horizontal power, reactive strength, and concentric power needs

### Rotational Power Deficit — ❌ FAIL
- Integration path: fallback to "Power" → FB gets Fast Bowler Power template (wrong), Spinner gets Rotational Power template (correct by luck), Batter gets Strength/Power template (wrong)
- Program builder path: same as integration
- **Root cause:** `rotational med ball throw` maps to "Rotational Power Deficit" but no explicit template mapping exists; DB migration 000009 seeds this deficit but integration_workflow.py doesn't include it in `deficit_template_map`

### Acceleration Deficit — ❌ FAIL
- Both paths: → "Power" → Fast Bowler Power template
- **Problem:** Contains zero sprint-specific exercises. Athlete diagnosed with acceleration deficit gets jump squats and bounds, not sprint starts, sled work, or wall drills
- **Root cause:** No Acceleration Development template exists in mock repos

### Strength Deficit — ❌ FAIL (integration_workflow) / ⚠️ PARTIAL (program_builder)
- Integration path: fallback to "Power" → strength deficit treated as power deficit
- Program builder path: → "Strength" → only Batter has a template for "Strength" goal; Fast Bowler and Spinner get **404 NOT FOUND**
- **Root cause:** `integration_workflow.py:199` lacks explicit mapping. `recommendation_engine.py:267-296` only maps `"strength"` goal for Batter role

### Reactive Strength Deficit — ❌ NOT IN SYSTEM
- **Does not exist as a deficit.** CMJ deficit is called "Power Deficit" and conflates concentric power, SSC function, RFD, and reactive strength into one bucket
- **Root cause:** `deficit_detection_engine.py:129` — single "Power Deficit" name for all CMJ-derived deficiencies

### Shoulder Robustness Deficit — ❌ FAIL
- Integration path: fallback to "Power" → shoulder deficit gets power training
- Program builder path: → "Strength" → only Batter resolves (Batter Strength/Power template); FB and Spinner get 404
- **Root cause:** `integration_workflow.py:199` — no explicit mapping. "Shoulder Robustness" goal exists in DB as template (migration 000004) but not in mock `get_template()` (recommendation_engine.py:267-296)

### Mobility Restriction — ❌ CRITICAL FAIL
- Integration path: → "Shoulder Robustness" → **404 NOT FOUND** for all roles (template silently dropped)
- Program builder path: → "Power" → resolves but with wrong deficit name (it's horizontal power, not mobility)
- **Root cause:** `deficit_detection_engine.py:138` — Broad Jump produces deficit name "Mobility Restriction" when it should produce "Horizontal Power Deficit". `integration_workflow.py:194` maps to "Shoulder Robustness" (upper body). DB migration 000009:233 maps Mobility Restriction → Shoulder Robustness template

---

## 5. Fallthrough Logic Analysis

### Integration Workflow (`integration_workflow.py:199`)
```python
goal_target = deficit_template_map.get(d.deficit, "Power")
```
- 3 deficiencies explicitly mapped → "Power", "Power", "Shoulder Robustness"
- 4 deficiencies fall through to default **"Power"**
- Falls through: **Strength Deficit, Speed Deficit, Rotational Power Deficit, Shoulder Robustness Deficit**

### Program Builder (`program_builder.py:683`)
```python
return deficit_goal_map.get(primary_deficit, "Power")
```
- All 7 deficiencies explicitly mapped → no fallthrough
- But "Strength" and "Shoulder Robustness Deficit"→"Strength" produce 404s for Fast Bowler and Spinner

### Template Resolution (`recommendation_engine.py:799-804`)
```python
if not template:
    raise HTTPException(status_code=404, detail=f"No movement template found...")
```
- No fallback template exists when goal doesn't match
- **Only 6 of 21 possible role×goal combinations resolve to a template** (3 roles × ~7 goals)
- Wicket Keeper, All Rounder: **zero** template resolution (0/14 combinations)

---

## 6. Unreachable Templates

| Template | Location | Why Unreachable |
|----------|----------|----------------|
| **Shoulder Robustness** (general, DB) | Migration 000004 | No mock entry in `recommendation_engine.py:get_template()`. DB template exists but mock code doesn't reference it. Only reachable via PostgreSQL path with specific goal match. |
| **Acceleration Development** (general, DB) | Migration 000004 | Same — exists in DB but no mock entry. Never resolved in mock mode. |
| **Lower Body Power** (general, DB) | Migration 000004 | Same — exists in DB but no mock entry. |
| **Rotational Power** (general, DB) | Migration 000004 | Same — exists in DB but no mock entry. |
| **Reactive Agility** (general, DB) | Migration 000004 | Same — exists in DB but no mock entry. No deficit maps to it. |

**All 5 general DB templates are unreachable in mock mode.** They are only reachable via PostgreSQL when the fallback query matches by goal name without role constraint.

---

## 7. Dead Templates

| Template | Location | Why Dead |
|----------|----------|----------|
| **Shoulder Robustness** | Migration 000004 | Mobility Restriction maps TO it (line 233), but "Shoulder Robustness" goal never reaches it in mock mode. Even if it did, it contains shoulder exercises for a lower body deficit — wrong treatment. |
| **Reactive Agility** | Migration 000004 | No deficit → goal → template chain exists. No assessment produces a deficit that would resolve to this template. Completely orphaned. |

---

## 8. Deficits Mapping to Same Template Incorrectly

| Deficits | Shared Template | Why Incorrect |
|----------|----------------|---------------|
| Power Deficit, Acceleration Deficit, Speed Deficit, Rotational Power Deficit (via fallthrough), Shoulder Robustness Deficit (via fallthrough) | **Cricket Fast Bowler Power** (template 100) for Fast Bowler role | 5 different deficiency types all get the same 4 exercises: Trap Bar Jump Squat, SL Lateral Bound, MB Overhead Toss, and a rotational core exercise. An athlete with speed deficit needs sprint mechanics; an athlete with rotational power deficit needs rotational throws; an athlete with power deficit needs vertical jump training — all get identical treatment. |
| Power Deficit, Acceleration Deficit, Speed Deficit, Strength Deficit (for Batter) | **Cricket Batter Strength/Power** (template 102) for Batter role | Same issue — 4 different deficiency types collapse to same 4 exercises: Trap Bar Deadlift, RFESS, Nordic Hamstring or Dumbbell Row, Pallof Press or Plank |

---

## 9. Complete Mapping Defects — Ranked

### P0 — Blocks correct athlete treatment

| # | Defect | File | Function | Line Range | Description |
|---|--------|------|----------|------------|-------------|
| **P0.1** | Broad Jump produces "Mobility Restriction" deficit (wrong construct) | `deficit_detection_engine.py` | `MockBenchmarkRepository.__init__` | 137-138 | Standing broad jump is a horizontal power test, NOT a mobility assessment. Deficit name should be "Horizontal Power Deficit". Description incorrectly attributes poor broad jump to "joint restriction." |
| **P0.2** | "Mobility Restriction" maps to "Shoulder Robustness" (upper body treatment for lower body deficit) | `integration_workflow.py` | `run_athlete_workflow` | 194 | `"Mobility Restriction": "Shoulder Robustness"` — lower body deficit → upper body template. Results in 404 for all roles (template not found), silently dropping the deficit. |
| **P0.3** | "Mobility Restriction" → "Shoulder Robustness" in DB seed data | `migrations/000009_comprehensive_cricket_seeds.up.sql` | — | 233 | `Mobility Restriction` deficit mapped to `Shoulder Robustness` movement template at the database level. Same clinical error persists in persistent storage. |
| **P0.4** | Strength Deficit → "Power" fallthrough in integration workflow | `integration_workflow.py` | `run_athlete_workflow` | 199 | `deficit_template_map.get("Strength Deficit", "Power")` — Strength Deficit not in the map, falls through to default "Power". Athlete needing maximal strength training gets power training. |
| **P0.5** | "Strength" goal returns 404 for Fast Bowler and Spinner | `recommendation_engine.py` | `MockExerciseRepository.get_template` | 267-296 | Only Batter role has a template for "strength" goal (line 289). Fast Bowler and Spinner get 404 when "Strength Deficit" → "Strength" goal is resolved via program builder path. |
| **P0.6** | "Shoulder Robustness" goal returns 404 for ALL roles | `recommendation_engine.py` | `MockExerciseRepository.get_template` | 267-296 | No template matches "Shoulder Robustness" goal in mock mode. The DB has a "Shoulder Robustness" template (migration 000004) but the mock code doesn't reference it. All three role→goal checks (lines 273, 281, 289) fail. |

### P1 — Incorrect training specificity

| # | Defect | File | Function | Line Range | Description |
|---|--------|------|----------|------------|-------------|
| **P1.1** | Acceleration Deficit → "Power" (no sprint-specific training) | `integration_workflow.py` + `program_builder.py` | `deficit_template_map` / `deficit_goal_map` | 193 / 676 | Both paths map Acceleration Deficit to "Power" goal. The Power template contains zero sprint-specific exercises (no sled work, wall drills, sprint starts, shin angle work). |
| **P1.2** | Speed Deficit → "Power" (no max-velocity training) | `program_builder.py` | `deficit_goal_map` | 678 | Same collapse — speed deficit gets power template. No flying sprints, overspeed work, or max-velocity mechanics. |
| **P1.3** | Rotational Power Deficit → "Power" (not explicitly "Rotational Power") | `integration_workflow.py` | `run_athlete_workflow` | 199 | Rotational Power Deficit not in `deficit_template_map` → falls to "Power". Only Spinner gets correct rotational template by coincidence (Spinner maps "power" to template 101 which is rotational). Fast Bowler and Batter get non-rotational templates. |
| **P1.4** | Rotary assessment exists but Rotational Power Deficit maps generically | `deficit_detection_engine.py` | `MockBenchmarkRepository.__init__` | 173-180 | `rotational med ball throw` correctly produces `Rotational Power Deficit`, but no pipeline correctly differentiates it from general Power Deficit. |
| **P1.5** | Shoulder Robustness Deficit → "Power" via fallthrough (integration) or "Strength" (program builder) | Both files | Both maps | 199 / 681 | Neither path maps Shoulder Robustness to a shoulder-specific goal. Integration: "Power". Program builder: "Strength" (which 404s for FB/Spinner). |

### P2 — Quality of prescription

| # | Defect | File | Function | Line Range | Description |
|---|--------|------|----------|------------|-------------|
| **P2.1** | Wicket Keeper role → 404 for all goals | `recommendation_engine.py` | `MockExerciseRepository.get_template` | 296 | No `elif` block handles "wicket keeper" or "keeper". Returns `None` at line 296 → 404. |
| **P2.2** | All Rounder role → 404 for all goals | `recommendation_engine.py` | `MockExerciseRepository.get_template` | 296 | Same — no `elif` block for "all rounder" or "all-rounder". |
| **P2.3** | integration_workflow role_id mapping assigns non-FB roles to ID 99 | `integration_workflow.py` | `run_athlete_workflow` | 113 | `role_id = 1 if "bowl" in request.role.lower() else 99` — Spinner, Batter, Wicket Keeper, All Rounder all get role_id=99. This ID doesn't match any seeded role. |
| **P2.4** | program_builder role_map only supports 3 of 5 roles | `program_builder.py` | `generate_program` | 707 | `role_map = {1: "Fast Bowler", 2: "Spinner", 3: "Batter"}` — Wicket Keeper (role_id=4) and All Rounder (role_id=5) not supported. |
| **P2.5** | Power → Fast Bowler returns same template for 5 different deficit types | `integration_workflow.py` + `program_builder.py` | both maps | 191-199 / 674-683 | Power Deficit, Acceleration Deficit, Speed Deficit, Mobility Restriction (program builder), and Rotational Power Deficit (via fallthrough) all produce the same "Power" goal, which resolves to the same template per role. |
| **P2.6** | Integration workflow iterates deficits but creates duplicate template recommendations | `integration_workflow.py` | `run_athlete_workflow` | 197-244 | Each deficit produces a separate recommendation request. If 3 deficits resolve to "Power", the workflow creates 3 identical Power template recommendations and appends all to `prescribed_templates`. Athlete with Power+Acceleration+Mobility gets 3× Power template prescription. |
| **P2.7** | Deficits not recorded as assessment→deficit in integration workflow role mapping | `integration_workflow.py` | `run_athlete_workflow` | 113 | `ASSESSMENT_UNITS` doesn't map all 7 assessment IDs (check line 156 — it references a dict from assessment_entry_module.py). |
| **P2.8** | Reactive Strength Deficit doesn't exist | `deficit_detection_engine.py` | `MockBenchmarkRepository.__init__` | 129 | CMJ → "Power Deficit" only. No "Reactive Strength Deficit" or "RFD Deficit" or "Eccentric Utilization Deficit" exists, despite CMJ being capable of diagnosing all three. |

---

## 10. Flow Diagrams

### Integration Workflow — Actual Data Flow

```
deficit_detection_engine.py          integration_workflow.py           recommendation_engine.py
┌─────────────────────┐              ┌─────────────────────┐          ┌─────────────────────┐
│ CMJ                 │              │ deficit_template_map│          │ get_template()       │
│  → Power Deficit    │——(1)———→     │  "Power Deficit"    │—(Power)→ │  "bowl"+"power"      │
│ Broad Jump           │              │    → "Power"       │          │    → Template 100    │
│  → Mobility Restrict│——(2)———→     │  "Accel Deficit"   │          │  "bat"+"power"       │
│ 10m Sprint           │              │    → "Power"       │          │    → Template 102    │
│  → Accel Deficit    │——(3)———→     │  "Mobility Restrict"│         │  "spin"+"power"      │
│ 20m Sprint           │              │    → "Shoulder Rob"│—(SR)——→  │    → Template 101    │
│  → Speed Deficit    │——(4)———→     │  (not in map)      │          │                      │
│ Trap Bar DL          │              │  → "Power" ✗      │          │ "Shoulder Robustness"│
│  → Strength Deficit │——(5)———→     │  (not in map)      │          │  → 404 ✗             │
│ Rotational MB Throw  │              │  → "Power" ✗      │          │ "Strength"           │
│  → Rot Power Deficit│——(6)———→     │  (not in map)      │          │  → only Batter ✓     │
│ Pull Up              │              │  → "Power" ✗      │          │                      │
│  → Shoulder Rob Def │——(7)———→     └─────────────────────┘          └─────────────────────┘
│                     │              ✗ = Strength, Speed, Rotational,
└─────────────────────┘                 Shoulder Robustness deficits all fall to "Power"
```

### Template Resolution — Actual Coverage (mock mode)

```
                     ┌─── Fast Bowler ───┬─── Spinner ────┬─── Batter ────┬─── WK ───┬─── AR ───┐
                     │                   │                │                │          │          │
Power                │  Template 100 ✓   │  Template 101 ✓│  Template 102 ✓│  404 ✗   │  404 ✗   │
Strength             │  404 ✗            │  404 ✗         │  Template 102 ✓│  404 ✗   │  404 ✗   │
Acceleration         │  404 ✗            │  404 ✗         │  Template 102 ✓│  404 ✗   │  404 ✗   │
Rotational Power     │  404 ✗            │  Template 101 ✓│  404 ✗         │  404 ✗   │  404 ✗   │
Shoulder Robustness  │  404 ✗            │  404 ✗         │  404 ✗         │  404 ✗   │  404 ✗   │
Speed                │  404 ✗            │  404 ✗         │  404 ✗         │  404 ✗   │  404 ✗   │
```

**6 of 35 possible role×goal combinations resolve to a template (17%).**

---

## 11. Summary of Findings by Severity

| Severity | Count | Key Issues |
|----------|-------|------------|
| **P0** | 6 | Broad Jump → Mobility Restriction construct error (P0.1); lower→upper body mapping (P0.2, P0.3); Strength Deficit fallthrough (P0.4); Strength goal 404s for FB/Spinner (P0.5); Shoulder Robustness goal 404s for all (P0.6) |
| **P1** | 5 | Acceleraton/Speed/Rotational deficits all collapse to Power; no sprint-specific training; Shoulder Robustness never resolves to shoulder template |
| **P2** | 8 | Wicket Keeper and All Rounder unsupported; role_id=99 for non-FB; only 3 of 5 roles supported; duplicate recommendations; Reactive Strength Deficit missing |
| **Total** | **19** | |

---

## File Locations Summary

| File | Line(s) | What |
|------|---------|------|
| `src/deficit_detection_engine.py` | 128-191 | All 7 deficit definitions with benchmark ranges |
| `src/deficit_detection_engine.py` | 138 | **P0.1** — Broad Jump → "Mobility Restriction" (construct error) |
| `src/integration_workflow.py` | 191-195 | `deficit_template_map` — only 3 of 7 deficits mapped |
| `src/integration_workflow.py` | 194 | **P0.2** — Mobility Restriction → "Shoulder Robustness" (wrong body part) |
| `src/integration_workflow.py` | 199 | **P0.4** — Fallthrough to "Power" for all unmapped deficits |
| `src/integration_workflow.py` | 113 | **P2.3** — role_id=99 for non-Fast-Bowlers |
| `src/program_builder.py` | 674-682 | `deficit_goal_map` — all 7 mapped, but 2 resolve to 404 |
| `src/program_builder.py` | 683 | Fallthrough to "Power" for unknown deficits |
| `src/program_builder.py` | 707 | **P2.4** — role_map only supports 3 of 5 roles |
| `src/recommendation_engine.py` | 267-296 | `get_template()` — template resolution logic |
| `src/recommendation_engine.py` | 273-279 | **P0.5** — Fast Bowler only matches "power" goal |
| `src/recommendation_engine.py` | 280-287 | Spinner only matches "power"/"rotational power" |
| `src/recommendation_engine.py` | 288-295 | Batter matches "power"/"strength"/"acceleration" |
| `src/recommendation_engine.py` | 296 | **P2.1, P2.2** — WK and All Rounder return None (404) |
| `migrations/000009_comprehensive_cricket_seeds.up.sql` | 195-198 | **P0.3** — Broad Jump → Mobility Restriction deficit in DB seed |
| `migrations/000009_comprehensive_cricket_seeds.up.sql` | 233 | **P0.3** — Mobility Restriction → Shoulder Robustness template in DB |
