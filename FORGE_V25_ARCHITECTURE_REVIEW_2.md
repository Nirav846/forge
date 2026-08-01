# FORGE V2.5 ARCHITECTURE REVIEW 2

## Roles: Software Architect (20yr) / S&C Coach (25yr) / Product Owner

---

## TASK 1: REVIEW THE IMPLEMENTATION PLAN

### Verdict: The plan is still 2x-3x too big for MVP.

The plan estimates 3,235 lines across 31 files over 12-18 days. The core logic (template resolution + exercise selection + substitution) is roughly 300 lines. The remaining 2,900 lines are scaffolding — migrations, models, repositories, tests, and seed data inflating to fill the architecture.

Below is the line-by-line assessment.

---

### `exercise_families` table

**KEEP** — But simpler. 15 rows, one table, one migration, done.

The table is correct:
```sql
CREATE TABLE exercise_families (id, name, description, display_order);
INSERT INTO exercise_families (name) VALUES ('Double Leg Knee Dominant'), ...;
```

**What to REMOVE**: The `category` column. It's unused metadata. Lower Body / Upper Body / Core / Explosive / Field is obvious from the family name. Coaches know that "Sprint" is a field category. No query filters by category. Remove it.

**Plan had**: 40 lines. **Should be**: 20 lines.

---

### `exercise_family_mapping` table

**KEEP** — This is the critical link between existing exercises and the new family taxonomy.

**What to REMOVE**: The `is_primary` column. In MVP every exercise maps to exactly one family. Cross-family mapping is a future concern. Remove it.

**Plan had**: 7 lines + seed data. **Should be**: 5 lines + seed data.

---

### `equipment_categories` table

**REMOVE** — This entire concept is over-engineered for MVP.

The existing DB already has:
- `equipment` table (individual items: Barbell, Dumbbell, Bodyweight, etc.)
- `exercise_equipment` junction table (which exercises need which equipment)

For MVP, the coach selects available equipment from a checkbox list. The system filters exercises by checking `exercise_equipment` against the selected list. Done.

The 5-category abstraction (Full Gym, Basic Gym, Dumbbells Only, Field Only, Hotel Gym) is a **UI convenience**, not a database concern. It belongs in the frontend as presets that expand to equipment checkboxes. Adding it to the schema now forces maintenance of a mapping table that changes every time a gym buys a new piece of equipment.

**Risk with this in MVP**: Schema churn. Equipment inventories change. Mappings get stale. The data layer has no business knowing that a "Hotel Gym" has dumbbells but not a barbell.

**Coaching value**: 0/10. No coach has ever said "I wish my program generator knew my equipment category."

**Remove**: `equipment_categories`, `equipment_category_mapping`, migration 000027, seed data file, repository.

---

### `equipment_category_mapping` table

**REMOVE** (same reasoning as above)

---

### `session_intents` table

**REMOVE** — Five hardcoded values do not need a database table.

Use a Python enum:
```python
from enum import Enum

class SessionIntent(str, Enum):
    STRENGTH = "Strength"
    POWER = "Power"
    SPEED = "Speed"
    CONDITIONING = "Conditioning"
    RECOVERY = "Recovery"
```

Total: 7 lines. Zero migrations. Zero maintenance.

**The plan's defense**: "The table lets coaches add new intents later." The product vision freezes intents at 5. If a coach asks for a 6th, adding a DB row takes 30 seconds and doesn't require a pre-built table.

**Coaching value**: 1/10. Intents are ontology, not user-generated content.

**Remove**: `session_intents` table, migration 000028, `intent_family_priorities`, seed mapping SQL.

---

### `intent_family_priorities` table

**REMOVE** — This table exists to answer "which families belong in a Strength session?" But the template **already answers this question** by defining which family slots appear in each session. The table would duplicate information that's already implicit in the template structure.

If every Strength session across every template uses the same 10 families, then maybe a lookup table makes sense. But they don't — a Fast Bowler Strength session and a Rugby Forward Strength session use different family mixes. The template IS the intent-to-family mapping.

**Coaching value**: 0/10. This table has no coaching analog. No coach thinks "let me look up which families are allowed in a Power session."

**Remove**: This table entirely. Let templates define their own slots. That's their job.

---

### `templates_v2`, `template_sessions_v2`, `session_family_slots` tables

**SIMPLIFY** — Or rather, **move to Python data files for MVP**.

Three tables, three migrations, a repository, a resolver service, and seed data for something that is **static configuration**, not user-generated content.

For MVP, templates are created by the development team (informed by the S&C coach). They are not created by users. They do not need to be stored in a database, indexed, queried, or transactionally protected.

**MVP approach**: A single Python file:
```python
TEMPLATES = {
    ("Cricket", "Fast Bowler", "Adult", "Off Season", 3): {
        "name": "Fast Bowler — Off Season — 3 Day",
        "sessions": [
            {"intent": "Strength", "slots": ["Double Leg Knee Dominant", "Horizontal Push", "Horizontal Pull", "Core"]},
            {"intent": "Power", "slots": ["Ballistic", "Plyometric", "Core"]},
            {"intent": "Conditioning", "slots": ["Sprint", "Change of Direction", "Conditioning"]},
        ]
    },
    # ... more templates
}
```

Total: ~80 lines for 12-15 templates. Zero migrations. Zero repositories. Zero resolvers. Zero seed SQL.

**When to add DB tables**: When coaches need to create, save, and manage their own templates. That's post-MVP.

**The plan's concern**: "200+ exercises, 1000+ variants" — DB tables don't help here. Exercise filtering is already handled by `exercise_family_mapping` + `exercise_equipment`. Templates are always small (10-30 per sport).

**Remove**: 3 SQL tables, 2 migration files, repository, resolver service.

---

### `000031_seed_equipment_extensions` migration

**REMOVE** — New equipment (Plyo Box, Sled, Agility Cones, Bike/Rower, Pull-up Bar) can be added by a simple INSERT into the existing `equipment` table when and if needed. A dedicated migration for 5 rows is noise.

**Remove**: This migration file.

---

### `000032_seed_templates_cricket` and `000033_seed_templates_soccer_rugby` migrations

**REMOVE** — Templates live in Python data files for MVP, as argued above. SQL seed data for templates adds a migration dependency every time a template changes. Python data files can be modified without running migrations.

**Remove**: Both migration files.

---

### Models directory (5 separate files)

**SIMPLIFY** — For MVP, a single `models.py` file with 3-4 Pydantic models:

```python
class GenerateRequest(BaseModel):
    sport: str
    role: str
    age_group: str = "Adult"
    phase: str
    frequency: int

class GeneratedSession(BaseModel):
    intent: str
    exercises: list[dict]  # {name, family, equipment, difficulty}

class GeneratedProgram(BaseModel):
    name: str
    sessions: list[GeneratedSession]

class SubstitutionRequest(BaseModel):
    exercise_id: int
    equipment: list[str]
    difficulty_cap: str = "Elite"

class SubstitutionResult(BaseModel):
    alternatives: list[dict]
```

Total: ~40 lines in one file. The plan had 5 files totaling ~150 lines.

**Remove**: Separate `athlete.py`, `context.py`, `template.py`, `exercise.py`, `substitution.py`. Single `models.py`.

---

### Repository layer (4 files, ~335 lines)

**REMOVE ENTIRELY** — Repositories exist to abstract database access. For MVP, data comes from:
- In-memory exercise library (Python dict)
- In-memory template definitions (Python dict)  
- Simple SQL queries against existing `exercises` + `exercise_equipment` tables (if using DB)

Neither use case requires a repository abstraction. The in-memory approach needs list/dict lookups. The DB approach needs 3-4 simple SELECT queries. Abstracting either behind repositories adds files + interfaces + dependency injection for zero benefit at MVP scale.

**When to add**: When the application grows to need multiple data backends (e.g., PostgreSQL for production + SQLite for testing). This is probably never for this application.

**Remove**: `repositories/__init__.py`, `exercise_repository.py`, `template_repository.py`, `family_repository.py`, `equipment_repository.py`.

---

### Data directory (5 files, ~480 lines)

**SIMPLIFY** — Seed data is necessary. But 5 separate files is fragmentation.

For MVP: One `seed_data.py` file with:
- `FAMILIES`: 15 strings (or a list of dicts with id+name)
- `EXERCISES`: ~68 dicts with {name, family, equipment, difficulty}
- `TEMPLATES`: ~15 template dicts as shown above
- `EQUIPMENT_PROFILES` (optional, for UI presets): {"Hotel Gym": ["Dumbbell", "Bodyweight", "Resistance Bands"]}

Total: ~350 lines in one file. Replace 5 files.

**Remove**: `data/__init__.py`, `families.py`, `exercises.py`, `equipment_categories.py`, `templates.py`. Single `seed_data.py` in the root of the v25 package.

---

### Services (4 files, ~455 lines)

**SIMPLIFY** — The logic is:
1. Look up a template by 5 keys → dict lookup
2. For each family slot, pick an exercise → filter by family, then equipment, then difficulty → pick first
3. For substitution → same family, filter by equipment, rank by difficulty match → return list

This is ~100 lines of logic, not 455.

**MVP approach**: A single `forge.py` module with 3 functions:

```python
def resolve_template(sport, role, age, phase, frequency) -> dict: ...
def populate_template(template, equipment, difficulty_cap) -> list[dict]: ...
def substitute(exercise_id, family, equipment, difficulty_cap) -> list[dict]: ...
```

Total: ~100 lines in one file.

**Remove**: `services/__init__.py`, `template_resolver.py`, `exercise_selector.py`, `substitution_engine.py`, `program_populator.py`. Single `forge.py`.

---

### Tests (5 files, ~500 lines)

**SIMPLIFY** — A single test file with 4-5 tests:
1. Template resolution returns correct template for a known input
2. Population fills all slots with valid exercises
3. Substitution returns same-family exercises only
4. Equipment filter excludes exercises requiring unavailable gear
5. E2E: Cricket Fast Bowler pipeline produces complete draft

Total: ~200 lines in one file.

**Remove**: 5 separate test files. Single `test_forge.py`.

---

### Summary: REMOVED COMPLEXITY

| Concept | Removed | Lines Saved |
|---------|---------|------------|
| `equipment_categories` table + migration | Entirely | 80 |
| `equipment_category_mapping` table + migration | Entirely | (included above) |
| `session_intents` table + migration | Entirely | 60 |
| `intent_family_priorities` table | Entirely | (included above) |
| `templates_v2` + `template_sessions_v2` + `session_family_slots` tables + migrations | Entirely | 80 |
| `000031_seed_equipment_extensions` migration | Entirely | 60 |
| `000032_seed_templates_cricket` migration | Entirely | 200 |
| `000033_seed_templates_soccer_rugby` migration | Entirely | 200 |
| `exercise_families.category` column | Removed column | 5 |
| `exercise_family_mapping.is_primary` column | Removed column | 3 |
| Models directory (5 files) | Merged to 1 file | 100 |
| Repositories directory (5 files) | Entirely removed | 340 |
| Data directory (5 files) | Merged to 1 file | 150 |
| Services directory (5 files) | Merged to 1 file | 300 |
| Tests directory (5 files) | Merged to 1 file | 300 |
| Separate app.py | Merged endpoint | 150 |
| **Total** | **~20 files removed** | **~2,028 lines saved** |

**New totals**: ~11 files, ~1,200 lines, 4-7 days instead of 12-18.

---

## TASK 2: EXERCISE ARCHITECTURE

### Structure for MVP

```
Family (15 entries, static)
  name: str

Exercise (60-80 entries, growing)
  name: str
  family: str              ← The substitution anchor (FK to Family)
  equipment: list[str]     ← What equipment is needed (reuse existing equipment table)
  difficulty: str          ← Beginner / Intermediate / Advanced / Elite
```

### Minimum Metadata (MVP)

| Field | Required? | Why |
|-------|-----------|-----|
| `id` | ✓ | Uniquely identify |
| `name` | ✓ | Display to coach |
| `family` | ✓ | Substitution anchor. Hard constraint. |
| `equipment` | ✓ | Equipment filter. Multi-value from existing `equipment` table. |
| `difficulty` | ✓ | Difficulty cap filter. 4-tier, matches existing schema. |

**5 fields. Not 10. Not 15.**

### Deferred Metadata

| Field | When | Why not now |
|-------|------|-------------|
| `mechanics_type` | Defer | Already exists in `exercises` table but unused by V2.5 logic |
| `force_type` | Defer | Already exists but unused by V2.5 logic |
| `technical_difficulty` | Defer | Doesn't drive substitution in MVP |
| `minimum_training_age_months` | Defer | Already exists but unused by V2.5 logic |
| `coaching_tags` | Defer | "Explosive", "Posterior Chain" — nice for filtering but not essential |
| `description` | Defer | Already exists in DB, useful for display but not logic |
| `primary_adaptation` | Defer | V2 concept. Remove from V2.5 schema entirely. |
| `force_vector` | Defer | V2 concept. Remove from V2.5 schema entirely. |
| `exercise_class` | Defer | V2 concept. Remove from V2.5 schema entirely. |

### How Substitution Uses This

```python
def get_substitutes(family_name: str, equipment: list[str], difficulty_cap: str):
    """
    1. Filter exercises by family (hard constraint)
    2. Filter by equipment: exercise's required equipment all in coach's available equipment
    3. Filter by difficulty: exercise.difficulty <= difficulty_cap
    4. Sort: same difficulty first, then adjacent
    """
    candidates = [ex for ex in EXERCISES if ex.family == family_name]
    candidates = [ex for ex in candidates if all(eq in equipment for eq in ex.equipment)]
    candidates = [ex for ex in candidates if DIFFICULTY[ex.difficulty] <= DIFFICULTY[difficulty_cap]]
    candidates.sort(key=lambda ex: DIFFICULTY[ex.difficulty], reverse=True)
    return candidates
```

**3 filters. 1 sort. 15 lines. No repository. No scoring. No AI.**

### Future Variant Support

Add a nullable `parent_exercise_id` column to the `exercises` table:

```sql
ALTER TABLE exercises
ADD COLUMN parent_exercise_id BIGINT REFERENCES exercises(id) ON DELETE SET NULL;
```

Then variants are just exercises with a parent:
```
Barbell Back Squat (parent: null)
  └── Safety Bar Squat (parent: Barbell Back Squat id)
  └── Front Squat (parent: Barbell Back Squat id)
```

The substitution engine checks: if `parent_exercise_id` is set, the variant inherits the parent's family. This is a **single column change** and doesn't touch any MVP code.

**Do not build in MVP.** Add the column when the first coach asks "can I offer Safety Bar Squat as an option?" Until then, Safety Bar Squat is just another exercise in the library.

---

## TASK 3: TEMPLATE ARCHITECTURE

### Verdict: Template → Session → Family Slot is sufficient.

**Yes, this is enough.** No changes needed.

### Justification

The template defines:
- Which sport/role/age/phase/frequency it applies to (5-key lookup)
- Which sessions it contains (each with an intent)
- Which family slots each session contains (ordered list)

This produces a complete structural skeleton. The exercise population step fills the skeleton.

### What is NOT needed in the template

| Concept | Needed? | Why |
|---------|---------|-----|
| Session location (Gym/Field) | **No** | Implicit from family slots. If template has Sprint/COD families, it's a field session. |
| Session duration | **No** | Coach decides. Not relevant to exercise selection. |
| Progression rules | **No** | Deferred. MVP selects exercises only. |
| Min/max exercises per slot | **No** | Always 1 in MVP. |
| Equipment override per session | **No** | Equipment is athlete-level, not session-level. |
| Coach notes | **No** | Post-MVP when coaches customize templates. |

### Example: Minimum viable template

```python
TEMPLATES = {
    ("Cricket", "Fast Bowler", "Adult", "Off Season", 3): {
        "name": "Fast Bowler — Off Season — 3 Day",
        "sessions": [
            {"intent": "Strength",     "slots": ["Double Leg Knee Dominant", "Horizontal Push", "Horizontal Pull", "Core"]},
            {"intent": "Power",        "slots": ["Ballistic", "Plyometric", "Core"]},
            {"intent": "Conditioning", "slots": ["Sprint", "Change of Direction", "Conditioning"]},
        ]
    },
}
```

That's it. The template resolver is a dict lookup. Total code for the resolver: 3 lines.

---

## TASK 4: SUBSTITUTION ARCHITECTURE

### Verdict: Yes, substitutions can be implemented with fewer than 5 fields.

### Minimal Model: 3 fields

| Field | Purpose | Example |
|-------|---------|---------|
| `family` | Hard constraint — never leave this family | `"Double Leg Knee Dominant"` |
| `equipment` | Filter — remove exercises that need unavailable gear | `["Barbell", "Bodyweight"]` |
| `difficulty` | Filter — cap by athlete level | `"Intermediate"` |

**3 fields. The substitution engine is entirely a filter + sort.**

### Implementation (entire engine)

```python
def substitute(family: str, equipment: list[str], difficulty_cap: str):
    """Return all valid exercises in family, ranked by suitability."""
    available = [ex for ex in EXERCISES if ex["family"] == family]
    available = [ex for ex in available if equipment_compatible(ex, equipment)]
    available = [ex for ex in available if difficulty_ok(ex, difficulty_cap)]
    available.sort(key=lambda ex: DIFFICULTY_RANK.get(ex["difficulty"], 0), reverse=True)
    return available

def equipment_compatible(exercise: dict, available_equipment: list[str]) -> bool:
    return all(eq in available_equipment for eq in exercise.get("equipment", []))

def difficulty_ok(exercise: dict, cap: str) -> bool:
    return DIFFICULTY_RANK.get(exercise.get("difficulty", "Beginner"), 0) <= DIFFICULTY_RANK.get(cap, 4)
```

**~15 lines. No DB. No ML. No scoring weights. No AI.**

### Sorting Logic

Sort by difficulty descending within the cap. A coach requesting "Intermediate" gets:
1. All Intermediate exercises in the family (matching equipment)
2. All Beginner exercises in the family

That's it. No relevance scores. No specificity ratings. No transfer indices. The coach sees the list and picks what they want.

**Coach trust comes from simplicity, not from AI-generated "relevance scores" that the coach doesn't believe.**

### What Makes Substitution Trustworthy

1. **Family lock**: Coach knows they won't get a Bench Press when they asked for a Squat
2. **Equipment filter**: Coach knows they won't get a Barbell exercise in a hotel room
3. **Difficulty filter**: Coach knows a beginner won't get Power Cleans
4. **Transparent ordering**: "Here are your options, sorted by difficulty. Pick one."

No black-box scoring. No "our algorithm recommends." Just clear, predictable filtering.

---

## TASK 5: RECOMMENDED MVP ARCHITECTURE

### Required Entities (5, not 7)

| Entity | Why | Fields |
|--------|-----|--------|
| Athlete Profile | Input identity | sport, role, age_group |
| Training Context | Input constraints | phase, frequency, equipment |
| Template | Output structure | sessions (each with intents → family slots) |
| Exercise Family | Grouping key | name, description |
| Exercise | Concrete movement | name, family_id, equipment, difficulty |

Context is NOT a separate entity in the DB. It's the combination of (phase, frequency, equipment) passed in the API request. "Context" as an entity was unnecessary abstraction.

### Required Tables (3 new, 1 existing)

| Table | New? | Rows | Purpose |
|-------|------|------|---------|
| `exercise_families` | NEW | 15 | Family taxonomy |
| `exercise_family_mapping` | NEW | ~68 | Link exercises to families |
| `exercises` | EXISTS | ~27+ | Core exercise data (add ~40 more) |
| `equipment` + `exercise_equipment` | EXISTS | ~10 + ~100 | Equipment filtering |

**3 new tables. 1 migration (000026 — create families + mapping).**

Not 8 new tables. Not 6 migrations.

### Required Services (1 module, 3 functions)

| Function | Lines | Purpose |
|----------|-------|---------|
| `resolve_template(sport, role, age, phase, frequency)` | 3 | Dict lookup |
| `populate(template, equipment, difficulty)` | 40 | Fill family slots with exercises |
| `substitute(family, equipment, difficulty)` | 15 | Find alternative exercises |

**Total: ~60 lines of core logic.** Not 455 lines across 4 service files.

### Required APIs (2 endpoints)

| Endpoint | Input | Output |
|----------|-------|--------|
| `POST /api/v2/programs/generate` | `{sport, role, age_group, phase, frequency, equipment, difficulty_cap}` | `{name, sessions: [{intent, exercises}]}` |
| `POST /api/v2/substitutions` | `{family, equipment, difficulty_cap}` | `{alternatives: [{id, name, equipment, difficulty}]}` |

**2 endpoints. Not 5.**

### Required Seed Data (1 file, 3 sections)

| Section | Lines | Content |
|---------|-------|---------|
| Families | 20 | 15 family names |
| Exercises | 250 | ~68 exercises with name, family, equipment, difficulty |
| Templates | 80 | ~15 templates across 4 sports × 3 phases |

**Total: ~350 lines in one `seed_data.py`.** Not 480 lines across 5 files.

### Required Files

```
src/v25/
├── __init__.py          # 0 lines (empty)
├── models.py            # 40 lines (GenerateRequest, GeneratedProgram, SubstitutionRequest, SubstitutionResult)
├── seed_data.py         # 350 lines (FAMILIES, EXERCISES, TEMPLATES)
├── forge.py             # 100 lines (resolve_template, populate, substitute)
├── app.py               # 80 lines (2 FastAPI endpoints)
└── test_forge.py        # 200 lines (4-5 tests)

Total: ~770 lines across 6 files.
```

**Not 3,235 lines across 31 files.**

---

### NOT MVP (Postpone Until Coach Feedback Proves Demand)

1. **Equipment categories** (Full Gym / Basic Gym / Hotel Gym) — UI preset, not schema
2. **Template persistence** (templates_v2 table) — Use in-memory data until coaches create custom templates
3. **Program persistence** (save/load programs) — Coaches print or screenshot drafts in MVP
4. **Session location + duration** — Implicit from family slots, not needed for exercise selection
5. **Session intent → family priority table** — Templates already define this implicitly
6. **Variant support (parent_exercise_id)** — Add column when coaches ask for it
7. **Repositories** — 3-4 simple queries don't need abstraction
8. **Session objectives** — Intent is sufficient for MVP
9. **Loading parameters (sets/reps/intensity)** — Coach fills these in. The draft is about WHICH exercises, not HOW to load them.
10. **Multiple sports beyond Cricket** — Cricket-only MVP proves the concept. Add Soccer/Rugby/Athletics in week 2. They're just data.
11. **Progression engine** — Not needed for single draft generation
12. **Coach override logging** — Not needed until coaches use the system
13. **Everything in the Architecture Graveyard** (competition, readiness, ACWR, periodization, analytics, etc.)

---

## FINAL VERDICT

### Architecture Score

| Dimension | Score (1-10) | Notes |
|-----------|-------------|-------|
| Simplicity | 9/10 | 5 entities, 2 endpoints, 1 service module, 1 data file |
| Coach Usability | 8/10 | Draft programs in 30 seconds. Coach substitutes by picking from clear lists. |
| Extensibility | 7/10 | Template data file makes adding sports easy. Substitution engine handles 1000+ exercises by keeping the same 3-filter approach. |
| Implementation Speed | 9/10 | 4-7 days to first working version. ~770 lines total. |
| Long-term Maintainability | 8/10 | Zero AI. Zero repositories. Zero over-engineering. Future changes are data changes, not code changes. |

**Overall: 41/50 — Proceed with build.**

### Go / No-Go Decision

**GO** — But only after implementing these cuts.

The original plan is a 31-file, 3,235-line behemoth. The revised MVP is a 6-file, 770-line focused build. Both produce the same output: a coach-credible draft program in under 3 minutes.

The difference is:
- Original: 12-18 days, 31 files, risk of architectural drift
- Revised: 4-7 days, 6 files, hard to over-engineer what doesn't exist

### Build Order (Revised)

**Day 1: Foundation**
1. Create migration 000026: `exercise_families` table + `exercise_family_mapping` table
2. Write `seed_data.py`: Families (15), Exercises (68), Templates (12-15)
3. Write `models.py`: 4 Pydantic models

**Day 2: Core Logic**
4. Write `forge.py`: `resolve_template` (3 lines), `populate` (40 lines), `substitute` (15 lines)
5. E2E test on command line — verify pipeline produces output for Cricket Fast Bowler

**Day 3: API + Tests**
6. Write `app.py`: 2 FastAPI endpoints
7. Write `test_forge.py`: 5 tests
8. Verify: Fast Bowler, Batter produce valid drafts. Substitutions stay in family. Equipment filter works.

**Day 4: Polish**
9. Add 2 more sports (Soccer Outfield, Rugby Forward) to `seed_data.py` — data entry only
10. Verify all 4 sports produce valid drafts
11. Measure: time from API request to populated draft

### One Final Question

Before coding, remove everything from the plan and ask for each remaining component:

**"Will removing this make the draft program materially worse?"**

If the answer is NO, it has no place in MVP.

- Equipment categories: NO → REMOVE
- Session intents table: NO → REMOVE
- Intent-family priorities: NO → REMOVE
- Template DB tables: NO → REMOVE  
- Repositories: NO → REMOVE
- Separate model files: NO → REMOVE
- Program persistence: NO → REMOVE (draft is ephemeral)
- Loading parameters: NO → REMOVE (for MVP, exercises only)

**Build what survives this question. Nothing else.**

**Recommended: Proceed with the 6-file, 770-line MVP.**
