# Template Coverage Repair Plan

## 1. Coverage Matrix (Mock Mode)

| Role ↓ \ Goal → | Power | Strength | Acceleration | Rotational Power | Speed Maintenance | Shoulder Robustness | Reactive Agility |
|---|---|---|---|---|---|---|---|
| **Fast Bowler** | ✅ 100 | ❌ 404 | ❌ 404 | ❌ 404 | ❌ 404 | ❌ 404 | ❌ 404 |
| **Spinner** | ✅ 101 | ❌ 404 | ❌ 404 | ✅ 101 | ❌ 404 | ❌ 404 | ❌ 404 |
| **Batter** | ✅ 102 | ✅ 102 | ✅ 102 | ❌ 404 | ❌ 404 | ❌ 404 | ❌ 404 |
| **Wicket Keeper** | ❌ 404 | ❌ 404 | ❌ 404 | ❌ 404 | ❌ 404 | ❌ 404 | ❌ 404 |
| **All Rounder** | ❌ 404 | ❌ 404 | ❌ 404 | ❌ 404 | ❌ 404 | ❌ 404 | ❌ 404 |

**Coverage: 6/35 cells (17.1%)**
- 3 batting cells (Power, Strength, Acceleration → template 102)
- 2 spinner cells (Power, Rotational Power → template 101)
- 1 fast bowler cell (Power → template 100)
- 0 keeper cells, 0 all-rounder cells

---

## 2. Full Deficit Pipeline Trace

### Program Builder path (`program_builder.py:674-683` → `recommendation_engine.py:267-296`)

| Deficit Name | Source Assessment | → Goal | FB | Sp | Bat | WK | AR |
|---|---|---|---|---|---|---|---|
| Power Deficit | CMJ | Power | ✅100 | ✅101 | ✅102 | ❌ | ❌ |
| Mobility Restriction | Broad Jump | Power | ✅100 | ✅101 | ✅102 | ❌ | ❌ |
| Acceleration Deficit | 10m Sprint | Power | ✅100 | ✅101 | ✅102 | ❌ | ❌ |
| Speed Deficit | 20m Sprint | Power | ✅100 | ✅101 | ✅102 | ❌ | ❌ |
| Strength Deficit | Trap Bar Deadlift | **Strength** | ❌ | ❌ | ✅102 | ❌ | ❌ |
| Rotational Power Deficit | Rotational Med Ball | Power | ✅100 | ✅101 | ✅102 | ❌ | ❌ |
| Shoulder Robustness Deficit | Pull Up | **Strength** | ❌ | ❌ | ✅102 | ❌ | ❌ |

### Integration Workflow path (`integration_workflow.py:191-199` → `recommendation_engine.py:267-296`)

| Deficit Name | → Goal | FB | Sp | Bat | WK | AR |
|---|---|---|---|---|---|---|
| Power Deficit | Power | ✅100 | ✅101 | ✅102 | ❌ | ❌ |
| Acceleration Deficit | Power | ✅100 | ✅101 | ✅102 | ❌ | ❌ |
| Mobility Restriction | **Shoulder Robustness** | ❌ | ❌ | ❌ | ❌ | ❌ |
| Speed Deficit (default) | Power | ✅100 | ✅101 | ✅102 | ❌ | ❌ |
| Strength Deficit (default) | Power | ✅100 | ✅101 | ✅102 | ❌ | ❌ |
| Rotational Power Deficit (default) | Power | ✅100 | ✅101 | ✅102 | ❌ | ❌ |
| Shoulder Robustness Deficit (default) | Power | ✅100 | ✅101 | ✅102 | ❌ | ❌ |

### Key Difference Between Paths

| Deficit | Program Builder Goal | Integration Workflow Goal | Impact |
|---|---|---|---|
| Strength Deficit | **Strength** | Power (default) | PB: FB/Sp/WK/AR 404; IW: OK via Power |
| Shoulder Robustness Deficit | **Strength** | Power (default) | PB: FB/Sp/WK/AR 404; IW: OK via Power |
| Mobility Restriction | **Power** | **Shoulder Robustness** | PB: OK (3/5 roles); IW: ALL 404 |

---

## 3. Issues by Priority

### P0 — Pipeline Breaks (404 on main code path)

| # | Issue | Root Cause | Files Affected | Fix |
|---|---|---|---|---|
| **P0-1** | Wicket Keeper has zero template support for all 7 goals | `MockExerciseRepository.get_template()` has no `"wicket"` branch | `recommendation_engine.py:267-296` | Add `elif "wicket" in r_clean:` block returning a Wicket Keeper template (reuse template 100 or create new) |
| **P0-2** | All Rounder has zero template support for all 7 goals | `MockExerciseRepository.get_template()` has no `"all"` or `"round"` branch | `recommendation_engine.py:267-296` | Add `elif "all" in r_clean:` block (reuse template 101 or 102 or create new) |
| **P0-3** | Broad Jump → "Mobility Restriction" is a construct error (horizontal power test → mobility treatment) | `MockBenchmarkRepository.__init__` sets `deficit_name: "Mobility Restriction"` for Broad Jump | `deficit_detection_engine.py:138` | Change to `"Power Deficit"` (or new `"Horizontal Power Deficit"`) |
| **P0-4** | "Mobility Restriction" → "Shoulder Robustness" in integration workflow sends lower-body deficit to upper-body template | `deficit_template_map` in `integration_workflow.py:194` | `integration_workflow.py:191-195` | Change `"Mobility Restriction": "Shoulder Robustness"` to map to `"Power"` (align with `program_builder.py`) — or remove entry (default is Power) |

### P1 — Partial Coverage (some roles get 404 for reachable goals)

| # | Issue | Root Cause | Files Affected | Fix |
|---|---|---|---|---|
| **P1-1** | Strength goal returns 404 for Fast Bowler & Spinner (only Batter has Strength template) | `get_template()` only serves `"strength"` for Batter | `recommendation_engine.py:289` | Option A: Remap "Strength Deficit" and "Shoulder Robustness Deficit" → "Power" in `program_builder.py:677,681`. Option B: Add FB/Spinner mock Strength entries. |
| **P1-2** | Shoulder Robustness goal returns 404 for ALL roles (dormant DB template exists in migration 000004 but mock code doesn't serve it) | `get_template()` has no branch for `"shoulder"` goal | `recommendation_engine.py:267-296` | Add a mock entry for Shoulder Robustness (for all roles or per-role), OR remove the integration_workflow path that leads here (P0-4 fix eliminates the only caller) |

### P2 — Code Quality / Maintainability

| # | Issue | Root Cause | Files Affected | Fix |
|---|---|---|---|---|
| **P2-1** | `program_builder.py:707` hardcodes 3 role IDs (1/2/3). Wicket Keeper (ID 4) and All Rounder (ID 5) silently default to Fast Bowler | `role_map` only covers 3 of 5 cricket roles | `program_builder.py:707` | Add `4: "Wicket Keeper", 5: "All Rounder"` to `role_map` |
| **P2-2** | `integration_workflow.py:191-195` has only 3 of 7 deficits explicitly mapped; 4 fall through to default "Power" | Partial mapping table | `integration_workflow.py:191-199` | Add explicit entries for all 7 deficits, or add a comment documenting the default behavior |
| **P2-3** | Program Builder maps Strength/Shoulder Robustness → "Strength" (404 for FB/Sp), while Integration Workflow maps all unlisted → "Power" (works for FB/Sp). Inconsistent behavior between paths. | Two separate mapping tables diverge | `program_builder.py:674-683` vs `integration_workflow.py:191-195` | Align both with same strategy — either both map Strength→Power or both map to dedicated Strength templates |
| **P2-4** | `deficit_detection_engine.py` has 7 mock deficits but DB migration 000009 only seeds 5 (missing Rotational Power Deficit, Shoulder Robustness Deficit). Mock-to-DB drift. | Mock and DB are out of sync | `deficit_detection_engine.py:173-190` vs `migrations/000009:173-199` | Add Rotational Power Deficit and Shoulder Robustness Deficit to migration 000009, or remove them from mock |
| **P2-5** | DB migration 000009 seeds "Mobility Restriction" → "Shoulder Robustness" in `deficit_movement_templates` (line 233), perpetuating the construct error at the DB level | DB seed mirrors the wrong S&C logic | `migrations/000009:233` | Change to map Mobility Restriction → Lower Body Power (or Rotational Power) |

---

## 4. Minimum Changes Required to Reach Production

### Phase 1 — Fix Pipeline Breaks (P0, 4 changes)

```
1. deficit_detection_engine.py:138   — Broad Jump: "Mobility Restriction" → "Power Deficit"
2. integration_workflow.py:194       — remove "Mobility Restriction" entry (falls through to "Power" default)
3. recommendation_engine.py:267-296  — add Wicket Keeper branch (reuse template 100 slots)
4. recommendation_engine.py:267-296  — add All Rounder branch (reuse template 102 slots)
```

After Phase 1, the coverage matrix becomes:

| Role | Power | Strength | Acceleration | Rotational Power | Speed Maintenance | Shoulder Robustness | Reactive Agility |
|---|---|---|---|---|---|---|---|
| **Fast Bowler** | ✅ 100 | ❌ 404 | ❌ 404 | ❌ 404 | ❌ 404 | ❌ 404 | ❌ 404 |
| **Spinner** | ✅ 101 | ❌ 404 | ❌ 404 | ✅ 101 | ❌ 404 | ❌ 404 | ❌ 404 |
| **Batter** | ✅ 102 | ✅ 102 | ✅ 102 | ❌ 404 | ❌ 404 | ❌ 404 | ❌ 404 |
| **Wicket Keeper** | ✅(100) | ❌ 404 | ❌ 404 | ❌ 404 | ❌ 404 | ❌ 404 | ❌ 404 |
| **All Rounder** | ✅(102) | ❌ 404 | ❌ 404 | ❌ 404 | ❌ 404 | ❌ 404 | ❌ 404 |

Coverage: 8/35 (22.9%). Wicket Keeper and All Rounder now have Power support.

### Phase 2 — Fix Partial Coverage (P1, 2 changes)

```
5. program_builder.py:677          — "Strength Deficit": "Strength" → "Power" (or add FB/Sp Strength templates)
6. program_builder.py:681          — "Shoulder Robustness Deficit": "Strength" → "Power" (same)
```

After Phase 2, every deficit resolves to a template for every role (assuming Phase 1 gave WK/AR Power support). Coverage is still 8/35 by direct goal resolution, but all 7 deficit → template pipelines are functional.

### Phase 3 — Code Quality (P2, as time permits)

```
7. program_builder.py:707          — add 4: "Wicket Keeper", 5: "All Rounder"
8. integration_workflow.py:191-199 — document or complete deficit_template_map
9. migrations/000009:233           — fix Mobility Restriction DB seed mapping
10. migrations/000009:173-199      — add missing deficit seeds (Rotational Power, Shoulder Robustness)
```

---

## 5. Effort Estimates

| Change | Files | Lines Changed | Effort |
|---|---|---|---|
| P0-1 (Broad Jump construct) | 1 | 1 | 2 min |
| P0-2 (integration map) | 1 | 1 | 1 min |
| P0-3 (WK mock template) | 1 | ~8 | 5 min |
| P0-4 (AR mock template) | 1 | ~8 | 5 min |
| P1-1, P1-2 (Strength→Power remap) | 1 | 2 | 2 min |
| P2-1 (role_map fix) | 1 | 1 | 1 min |
| P2-2 (integration sync) | 1 | ~4 | 3 min |
| P2-4, P2-5 (DB seeds) | 1 | ~8 | 10 min |

**Total minimum to unblock all pipelines: ~15 minutes, 4 files, 12 lines changed.**
