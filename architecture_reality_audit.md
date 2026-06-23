# Architecture Reality Audit

## 1. Template Resolution Path

### Full Program Generation Pipeline

```
Client POST /api/v1/programs/generate
    │
    ├─ program_builder.py:1018 (FastAPI endpoint)
    │   └─ ProgramBuilderService.build_and_save()
    │       └─ generate_program()  [line 685]
    │           │
    │           ├─ 1. athlete_repo.get_by_id()  → MockAthleteRepository (always)
    │           │
    │           ├─ 2. Resolve sport_name/role_name
    │           │     Mock: {1:"Fast Bowler", 2:"Spinner", 3:"Batter"}  [line 707]
    │           │     DB:   SELECT name FROM sports/roles WHERE id = $1   [line 713-718]
    │           │
    │           ├─ 3. resolve_athlete_deficits_and_goal()  [line 626]
    │           │     ├─ 3a. results_repo.get_history()  → MockAssessmentResultRepository (always)
    │           │     ├─ 3b. Hardcoded assessment_id→name mapping  [line 646-653]
    │           │     ├─ 3c. DeficitDetectionService(MockBenchmarkRepository)
    │           │     │     └─ detect_deficits() → repo.get_score_classification()
    │           │     │           MockBenchmarkRepository: 7 hardcoded assessments  [line 127-191]
    │           │     │           PostgreSqlBenchmarkRepository: SQL query  [line 101-115]
    │           │     │           → BUT get_benchmark_repository() ALWAYS returns Mock  [line 215-219]
    │           │     └─ 3d. Hardcoded deficit_goal_map  [line 674-682]
    │           │
    │           ├─ 4. Build RecommendationRequest(sport, role, goal, equipment, difficulty)
    │           │
    │           ├─ 5. get_exercise_recommendations()  [line 745]
    │           │     ├─ repo = PostgreSqlExerciseRepository if DB_URL+pool else MockExerciseRepository
    │           │     └─ repo.get_template(sport, role, goal)  [line 799]
    │           │           ├─ MockExerciseRepository.get_template():
    │           │           │     3 hardcoded role branches, 3 hardcoded goal patterns  [line 267-296]
    │           │           │     → All other role+goal combos return None → 404
    │           │           └─ PostgreSqlExerciseRepository.get_template():
    │           │                 SQL query on movement_templates  [line 155-161]
    │           │                 → 6 DB templates (1 Cricket, 5 non-Cricket sport)
    │           │           ⚠ get_repository() ALWAYS returns MockExerciseRepository  [line 763-770]
    │           │
    │           └─ 6. Progression calculation (hardcoded 4-week S&C rules)  [line 224-345]
    │
    └─ program_repo.create_program()
          MockProgramRepository → in-memory dict
          PostgreSqlProgramRepository → SQL INSERT (only if DB_URL+pool)
```

### All Template Selection Points

| Location | Mode | What It Does |
|---|---|---|
| `recommendation_engine.py:799` | Production | `repo.get_template(sport, role, goal)` — dispatches to Mock or PostgreSql |
| `recommendation_engine.py:153-178` | DB path | SQL: `SELECT FROM movement_templates WHERE sport ILIKE $1 AND athlete_role ILIKE $2 AND training_goal ILIKE $3` — then fallback to sport-agnostic |
| `recommendation_engine.py:267-296` | Mock path | 3 if/elif blocks: Fast Bowler→Power, Spinner→Power/RotPower, Batter→Power/Strength/Acceleration |
| `program_builder.py:743` | Conditional | `PostgreSqlExerciseRepository(pool) if db_url and pool else MockExerciseRepository()` |
| `session_generator.py:464` | Conditional | `PostgreSqlExerciseRepository(pool) if pool else MockExerciseRepository()` |
| `integration_workflow.py:212` | **Always Mock** | Hardcoded `MockExerciseRepository()` |
| `knowledge_graph_service.py` | **Always Mock** | Uses separate `MockKnowledgeGraphRepository()` with its own hardcoded deficit logic |

### Key Finding: PostgreSqlExerciseRepository.get_template() EXISTS and works

It queries `movement_templates` with a sport+role+goal filter and falls back to sport-agnostic goal matching. If DATABASE_URL is set and db_pool is connected, program_builder.py:743 WILL use it instead of MockExerciseRepository. However:

1. `get_repository()` in recommendation_engine.py:763-770 **always returns Mock** (the `if db_url:` branch is `pass`)
2. Only program_builder.py:743 and session_generator.py:464 bypass `get_repository()` and instantiate `PostgreSqlExerciseRepository` directly

---

## 2. Database vs Application Authority

| Domain | Authority | Evidence |
|---|---|---|
| **Deficits** | **DUPLICATED** | DB: `deficits` table (migrations 000008:160-180, 000009:173-199). Mock: 7 hardcoded in `MockBenchmarkRepository.__init__` (deficit_detection_engine.py:127-191). The mock has 2 deficits not in DB (`Rotational Power Deficit`, `Shoulder Robustness Deficit`). The DB has 2 deficit systems (000008 has 4, 000009 has 5) that never intersect. |
| **Deficit→Goal mappings** | **APPLICATION_DRIVEN** | Hardcoded in `program_builder.py:674-683` and `integration_workflow.py:191-195`. No DB table stores deficit→goal mapping. The DB has `deficit_movement_templates` but it maps deficit→template (not deficit→goal) and **no code queries it**. |
| **Deficit→Template mappings** | **DUPLICATED** | DB: `deficit_movement_templates` junction table seeded in migrations 000008:214-233 and 000009:227-233. App: `integration_workflow.py:191-195` hardcodes 3 mappings. Knowledge graph service has its own hardcoded mappings. No code queries `deficit_movement_templates`. |
| **Movement Templates** | **DUPLICATED** | DB: 6 templates in `movement_templates` (000004:8-38, 000005:14-20). Mock: 3 templates in `MockExerciseRepository.get_template()` (recommendation_engine.py:267-296). The PostgreSql repository CAN query the DB but is rarely used. |
| **Slot Requirements** | **DATABASE_DRIVEN** | DB: `slot_requirements` table (000004:84-256). `PostgreSqlExerciseRepository.get_ranked_exercises()` queries it via SQL JOIN (recommendation_engine.py:208-261). Mock: uses hardcoded `score_components`. |
| **Slot Progressions** | **DUPLICATED** | DB: `slot_progressions` table (000004:263-395, 000005:198-222). `PostgreSqlExerciseRepository.get_slot_progression()` queries it (recommendation_engine.py:192-202). Mock: `MockExerciseRepository.get_slot_progression()` returns hardcoded dict (recommendation_engine.py:322-338). |
| **Exercise Rankings** | **APPLICATION_DRIVEN** | PostgreSql: SQL scoring formula in `get_ranked_exercises()` (recommendation_engine.py:216-221). Mock: pre-computed `score_components` dict per exercise (recommendation_engine.py:362-461+). No DB table stores recommendation scores. |
| **Athlete Role Definitions** | **DUPLICATED** | DB: `roles` table (migrations 000008:7-32). App: `role_map = {1: "Fast Bowler", 2: "Spinner", 3: "Batter"}` in `program_builder.py:707` and `session_generator.py:434` — **both miss Wicket Keeper (ID 4) and All Rounder (ID 5)**. |
| **Program Design Rules** | **DATABASE_DRIVEN (unused)** | DB: `program_design_rules` table (000013:5-114). **No code queries this table.** All progression rules are hardcoded in `calculate_reps_and_intensity()` (program_builder.py:224-345). |
| **Sports Science Rules** | **DATABASE_DRIVEN (unused)** | DB: `sports_science_rules` table (000014:3-79). **No code queries this table.** |
| **Exercise Catalog** | **TRIPLICATED** | DB: `exercises` table (000005:50-76). Mock: `session_generator.py:134-157` (`MOCK_EXERCISES`). Mock: `recommendation_engine.py:352-461` (mock `get_ranked_exercises` pool). Three independent lists, all slightly different. |

---

## 3. Mock Dependency Audit

| # | MockRepository | File | Why Exists | Production Reachable? | Risk | Recommended Action |
|---|---|---|---|---|---|---|
| 1 | `MockBenchmarkRepository` | deficit_detection_engine.py:123 | Fallback benchmark data | **YES — always.** `get_benchmark_repository()` (line 215-219) checks DATABASE_URL but always returns Mock. The PostgreSql implementation exists but is never wired. | **HIGH** — Production bypasses DB benchmarks entirely. | Wire `get_benchmark_repository()` to return `PostgreSqlBenchmarkRepository` when DATABASE_URL is set. |
| 2 | `MockExerciseRepository` | recommendation_engine.py:264 | Fallback template + exercise data | **YES — conditionally.** `get_repository()` (line 763-770) always returns Mock. But `program_builder.py:743` and `session_generator.py:464` conditionally instantiate PostgreSql. Integration_workflow hardcodes Mock. | **HIGH** — Default DI path always uses Mock. Integration workflow always Mock. | Wire `get_repository()` to actually use PostgreSql. Fix integration_workflow to not hardcode Mock. |
| 3 | `MockKnowledgeGraphRepository` | knowledge_graph_service.py:156 | Fallback KG data | **YES — always.** `get_graph_repository()` (line 237-242) checks DATABASE_URL but always returns Mock. | **HIGH** — All knowledge graph endpoints serve hardcoded data. | Wire to PostgreSql when DATABASE_URL is set. |
| 4 | `MockAthleteRepository` | athlete_module.py:122 | Fallback athlete data | **YES — always.** `get_athlete_repository()` (line 298-304) checks DATABASE_URL but always returns Mock. | **HIGH** — All athlete CRUD goes to in-memory dict, lost on restart. | Wire to PostgreSql when DATABASE_URL is set. |
| 5 | `MockAssessmentResultRepository` | assessment_entry_module.py:91 | Fallback results data | **YES — always.** `get_results_repository()` (line 249-253) checks DATABASE_URL but always returns Mock. | **HIGH** — All assessment results go to in-memory, lost on restart. | Wire to PostgreSql when DATABASE_URL is set. |
| 6 | `MockProgramRepository` | program_builder.py:365 | Fallback program persistence | **YES — conditionally.** `get_program_repository()` (line 604-608) returns PostgreSqlProgramRepository only if both DATABASE_URL AND db_pool are set. | **MEDIUM** — Has working DB path, but most setups without DB pool fall back to in-memory. | None needed — conditional logic is correct. |

### Critical Finding: 5 of 6 repository factory functions have `if db_url: pass` — they check for DATABASE_URL then do nothing

```python
# deficit_detection_engine.py:215-219
def get_benchmark_repository():
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        pass                    # ← Dead code
    return MockBenchmarkRepository()

# recommendation_engine.py:763-770
def get_repository():
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        pass                    # ← Dead code
    return MockExerciseRepository()

# athlete_module.py:298-304
def get_athlete_repository():
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        pass                    # ← Dead code
    return _mock_repo

# assessment_entry_module.py:249-253
def get_results_repository():
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        pass                    # ← Dead code
    return _mock_repo

# knowledge_graph_service.py:237-242
def get_graph_repository():
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        pass                    # ← Dead code
    return MockKnowledgeGraphRepository()
```

### Contrast: program_builder.py has the ONLY correctly wired factory

```python
# program_builder.py:604-608
def get_program_repository():
    db_url = os.getenv("DATABASE_URL")
    if db_url and db_pool:
        return PostgreSqlProgramRepository(db_pool)  # ← Actually returns DB implementation
    return _mock_repo
```

---

## 4. Hardcoded Sports Science Logic

### 4a. Deficit → Goal Mappings

| File | Lines | Logic | DB Equivalent |
|---|---|---|---|
| `program_builder.py` | 674-682 | `{"Power Deficit":"Power","Acceleration Deficit":"Power","Strength Deficit":"Strength","Speed Deficit":"Power","Mobility Restriction":"Power","Rotational Power Deficit":"Power","Shoulder Robustness Deficit":"Strength"}` | None — no `deficit_goals` table exists |
| `integration_workflow.py` | 191-195 | `{"Power Deficit":"Power","Acceleration Deficit":"Power","Mobility Restriction":"Shoulder Robustness"}` + default `"Power"` | Same — no table exists |

### 4b. Role → Template / Role → Name Mappings

| File | Lines | Logic | DB Equivalent |
|---|---|---|---|
| `program_builder.py` | 707 | `role_map = {1:"Fast Bowler", 2:"Spinner", 3:"Batter"}` — **missing WK (4) and AR (5)** | `roles` table |
| `session_generator.py` | 434 | `role_map = {1:"Fast Bowler", 2:"Spinner", 3:"Batter"}` — **same bug duplicated** | `roles` table |
| `recommendation_engine.py` | 272-295 | 3 hardcoded role branches: `"bowl" or "fast"`, `"spin"`, `"bat"` — **no WK or AR** | `movement_templates` table |

### 4c. Template IDs

| File | Lines | Logic |
|---|---|---|
| `program_builder.py` | 999-1004 | `_resolve_template_id_from_slot`: slot_id ≥400→102, ≥300→101, else 100 |
| `exercise_substitution_engine.py` | 179-185 | `_resolve_template_id`: same logic duplicated |
| `recommendation_engine.py` | 299-319 | `get_slots`: template 100 returns slots 201-204, 101 returns 301-304, 102 returns 401-404 |

### 4d. Exercise Classifications

| File | Lines | Logic |
|---|---|---|
| `exercise_classification.py` | 7-52 | `classify_exercise`: 10 hardcoded name-based rules (olympic_names list, "jump squat", "medicine ball", "bound", "plank", etc.) |
| `exercise_classification.py` | 55-78 | `determine_primary_adaptation`: 8 hardcoded class→adaptation mappings |
| `exercise_classification.py` | 81-97 | `determine_force_vector`: 7 hardcoded name/class→vector rules |

### 4e. Progression Rules (4-Week Program)

| File | Lines | Logic |
|---|---|---|
| `program_builder.py` | 224-345 | `calculate_reps_and_intensity`: 8 hardcoded exercise_class branches (Olympic Lift, Ballistic, Medicine Ball, Plyometric, Isometric, Sprint Drill, Core Stability, Max Strength/default). Each has a 4-week intensity map and rep scheme. |
| `program_builder.py` | 203-221 | `parse_baseline_reps`: regex parse of "NxM" strings, fallback per slot type |
| `program_builder.py` | 771-776 | `week_details`: 4-week structure hardcoded (Base, Accumulation, Peak, Deload) |

### 4f. Assessment → ID Mappings

| File | Lines | Logic |
|---|---|---|
| `program_builder.py` | 646-653 | `mapping = {1:"cmj", 2:"broad jump", 3:"10m sprint", 4:"20m sprint", 5:"pull up", 6:"trap bar deadlift"}` |
| `integration_workflow.py` | 138-146 | Same mapping, includes ID 7 for "rotational med ball throw" |
| `assessment_entry_module.py` | 31-39 | `ASSESSMENT_UNITS = {1:"cm", 2:"m", 3:"s", 4:"s", 5:"reps", 6:"kg", 7:"m/s"}` |

---

## 5. Architecture Scorecard

### Database Driven Design: 15/100

Only `slot_requirements` and `slot_progressions` are truly database-driven when the PostgreSql path is used. No factory function successfully returns a DB implementation (except `get_program_repository` which has a conditional that works). All default DI paths return mocks.

### Extensibility: 10/100

Adding 20 new templates to `movement_templates` has almost zero effect because:
- `MockExerciseRepository.get_template()` is the default, which would need code changes for each new template
- `PostgreSqlExerciseRepository.get_template()` would pick them up automatically, but can only be reached if Mock is bypassed
- `deficit_goal_map` is hardcoded — new goals need code changes
- `calculate_reps_and_intensity()` is hardcoded — new exercise classes need code changes
- `exercise_classification.py` is name-based — new exercises need code changes to be properly classified

### Maintainability: 20/100

5 out of 6 repository factory functions have dead `if db_url: pass` blocks. Two independent role_map dicts (both missing WK and AR). Three independent exercise catalogs (recommendation_engine, session_generator, DB). Two independent deficit systems (migration 000008 vs 000009). Hardcoded template IDs (100, 101, 102) scattered across 3 files.

### Sports Science Configurability: 5/100

Almost zero. Every S&C rule is in Python code:
- Deficit thresholds → `MockBenchmarkRepository.__init__` 
- Deficit→goal mappings → `program_builder.py:674-682`
- Exercise classification → `exercise_classification.py` (name-based)
- Weekly progression → `calculate_reps_and_intensity()` (witch's brew of if/elif)
- Session structure → hardcoded 4-week Base/Accumulation/Peak/Deload

### Production Readiness: 10/100

If deployed to production with a real PostgreSQL database and DATABASE_URL set:
1. Athlete CRUD → Mock (in-memory, lost on restart)
2. Assessment results → Mock (in-memory, lost on restart)
3. Deficit detection → Mock (7 hardcoded assessments only)
4. Knowledge graph → Mock (2 hardcoded assessments only)
5. Template resolution → Mock (3 roles × 3 goals only)
6. Program persistence → PostgreSql (the one correct path)
7. Session generation → Mixed (Mock or PostgreSql depending on pool)

Every integration_workflow.py endpoint is permanently Mock-locked.

---

## 6. Final Verdict

### "If I add 20 new cricket templates directly into the database tomorrow, how much of the application automatically begins using them without code changes?"

### Percentage estimate: 5%

### Exact blockers:

| # | Blocker | File | Effect |
|---|---|---|---|
| 1 | `get_repository()` returns Mock even when DB is available | `recommendation_engine.py:763-770` | Template resolution via DI always hits Mock, not DB |
| 2 | `get_benchmark_repository()` returns Mock even when DB is available | `deficit_detection_engine.py:215-219` | Deficits always come from hardcoded data, not DB |
| 3 | `get_athlete_repository()` returns Mock even when DB is available | `athlete_module.py:298-304` | Athlete data always in-memory |
| 4 | `get_results_repository()` returns Mock even when DB is available | `assessment_entry_module.py:249-253` | Assessment results always in-memory |
| 5 | `get_graph_repository()` returns Mock even when DB is available | `knowledge_graph_service.py:237-242` | Knowledge graph always hardcoded |
| 6 | `MockExerciseRepository.get_template()` hardcodes only 3 roles × 3 goals | `recommendation_engine.py:267-296` | New templates unreachable from Mock path |
| 7 | `integration_workflow.py:212` hardcodes MockExerciseRepository | `integration_workflow.py:212` | Integration workflow permanently Mock-locked |
| 8 | `integration_workflow.py:177` hardcodes MockBenchmarkRepository | `integration_workflow.py:177` | Integration deficits permanently Mock-locked |
| 9 | `program_builder.py:707` role_map missing WK (4) and AR (5) | `program_builder.py:707` | Roles 4-5 default to "Fast Bowler" |
| 10 | `session_generator.py:434` role_map missing WK (4) and AR (5) | `session_generator.py:434` | Same bug duplicated |
| 11 | `program_builder.py:674-682` defict_goal_map hardcoded | `program_builder.py:674-682` | No DB table for deficit→goal mappings |
| 12 | `calculate_reps_and_intensity()` hardcodes all progression rules | `program_builder.py:224-345` | `program_design_rules` DB table (migration 000013) is never queried |

### Files preventing full database-driven operation:

1. **`recommendation_engine.py:763-770`** — `get_repository()` has `if db_url: pass` (dead code). Change to `return PostgreSqlExerciseRepository(pool)`.
2. **`deficit_detection_engine.py:215-219`** — `get_benchmark_repository()` has `if db_url: pass`. Change to return PostgreSqlBenchmarkRepository.
3. **`athlete_module.py:298-304`** — `get_athlete_repository()` has `if db_url: pass`. Change to return PostgreSqlAthleteRepository(pool).
4. **`assessment_entry_module.py:249-253`** — `get_results_repository()` has `if db_url: pass`. Change to return PostgreSqlAssessmentResultRepository(pool).
5. **`knowledge_graph_service.py:237-242`** — `get_graph_repository()` has `if db_url: pass`. Change to return PostgreSqlKnowledgeGraphRepository(pool).
6. **`program_builder.py:674-682`** — Hardcoded deficit_goal_map. No DB table exists. Either create a `deficit_goal_mappings` table or embed in `deficit_movement_templates`.
7. **`program_builder.py:224-345`** — Hardcoded `calculate_reps_and_intensity()`. Query `program_design_rules` table instead.
8. **`recommendation_engine.py:267-296`** — `MockExerciseRepository.get_template()` is the default path. Must either wire `get_repository()` to DB (fix #1) or extend Mock to cover all roles.
