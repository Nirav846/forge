# FORGE V2 Load Engine Implementation Plan

## Architecture

```
┌────────────────────────────────────────────────────┐
│                  FORGE V2 Core                      │
│                                                      │
│  ┌─────────────┐  ┌───────────┐  ┌──────────────┐  │
│  │ Load Model   │  │ Exposure  │  │ Periodization│  │
│  │ Calculator   │  │ Bucket    │  │ Rule Engine  │  │
│  │              │  │ Tracker   │  │              │  │
│  └──────┬───────┘  └─────┬─────┘  └──────┬───────┘  │
│         │                │                │          │
│         └────────────────┴────────────────┘          │
│                            │                         │
│                     ┌──────┴──────┐                  │
│                     │   Session   │                  │
│                     │  Generator  │                  │
│                     │  (modified) │                  │
│                     └─────────────┘                  │
│                            │                         │
│                     ┌──────┴──────┐                  │
│                     │  Training   │                  │
│                     │  Plan       │                  │
│                     │  (enriched) │                  │
│                     └─────────────┘                  │
└────────────────────────────────────────────────────┘
```

## Phase 1: Data Layer — New Models (Day 1-2)

### Changes to `src/forge/models.py`

**1. New dataclass: `SessionLoadMetrics`**

```
SessionLoadMetrics:
  - exercise_load: int          (sum of fatigue+impact+eccentric across all exercise blocks)
  - conditioning_load: int      (sum of conditioning protocols)
  - total_load: int             (exercise_load + conditioning_load)
  - sprint_count: int           (exposure count from Sprint family + sprint conditioning)
  - jump_count: int             (exposure count from Plyo + Ball + jump conditioning)
  - eccentric_count: int        (exercises with eccentric >= 4 + conditioning with ecc >= 4)
  - decel_count: float          (decel conditioning + 0.5*unilateral SL)
  - rot_count: int              (rot family + exercises with rotational=True)
  - fatigue_sum: int            (sum of fatigue_cost across all items)
  - impact_sum: int             (sum of impact_level across all items)
  - eccentric_sum: int          (sum of eccentric_cost across all items)
```

**2. New dataclass: `WeeklyLoadSummary`**

```
WeeklyLoadSummary:
  - week_number: int
  - sessions: list[SessionLoadMetrics]
  - total_load: int             (sum of all session total_loads)
  - avg_session_load: float
  - sprint_total: int
  - jump_total: int
  - eccentric_total: int
  - decel_total: float
  - rot_total: int
  - session_count: int
```

**3. New dataclass: `RollingLoadState`**

```
RollingLoadState:
  - acute_window: list[SessionLoadMetrics]    (last 7 days)
  - chronic_window: list[SessionLoadMetrics]  (last 28 days)
  - acute_load: int
  - chronic_load: float
  - acwr: float
```

**4. Extension to `TrainingPlan`**

Add field:
```
  - weekly_loads: list[Optional[WeeklyLoadSummary]] = field(default_factory=list)
  - rolling_load: Optional[RollingLoadState] = None
```

## Phase 2: Load Calculator Module (Day 2-3)

### New file: `src/forge/load_calculator.py`

Functions (pure, no side effects):

```
compute_exercise_load(exercise: Exercise) -> int
  → exercise.fatigue_cost + exercise.impact_level + exercise.eccentric_cost

compute_conditioning_load(protocol: ConditioningProtocol) -> int
  → protocol.fatigue_cost + protocol.impact_level + protocol.eccentric_cost

compute_session_load(session: SessionPlan) -> SessionLoadMetrics
  → iterates all blocks and conditioning, builds load metrics + exposure counts

compute_weekly_load(sessions: list[SessionPlan]) -> WeeklyLoadSummary
  → sums all session load metrics for one week

compute_rolling_load(weekly_summaries: list[WeeklyLoadSummary]) -> RollingLoadState
  → acute = last 7 days, chronic = average of last 28 days

compute_acwr(acute: int, chronic: float) -> float
  → acute / chronic (handles chronic=0 edge case)

map_exercise_to_buckets(exercise: Exercise) -> ExposureCounts
  → uses the mapping tables from the Exposure Rulebook
  → returns exposure increment for each bucket

map_conditioning_to_buckets(protocol: ConditioningProtocol, ...) -> ExposureCounts
  → uses movement_profile → exposure bucket mapping
  → returns exposure increment for each bucket
```

## Phase 3: Rule Engine (Day 3-5)

### New file: `src/forge/periodization_engine.py`

```
class PeriodizationEngine:
    """Pure function engine. No state. Input → rules → output actions."""

    def evaluate(context: RuleContext) -> list[RuleAction]
        → iterates all 30 rules
        → each rule checks conditions against context
        → returns list of actions (ADJUST_LOAD, ADD_SESSION, REPLACE_BLUEPRINT, etc.)

    def should_deload(context: RuleContext) -> bool
        → combines ACWR, load history, competition window
        → returns bool + suggested load reduction %

    def apply_load_modifications(
        session: SessionPlan,
        actions: list[RuleAction]
    ) -> SessionPlan
        → modifies session in place based on actions
        → removes exercises, replaces blocks, adjusts conditioning
```

### Rule Engine Input (RuleContext)

```
RuleContext:
  - current_weekly_summary: Optional[WeeklyLoadSummary]
  - previous_weekly_summaries: list[WeeklyLoadSummary]  (last 4+ weeks)
  - rolling_load: Optional[RollingLoadState]
  - athlete_profile: AthleteProfile
  - current_blueprint: Blueprint (not blueprint_data — the resolved plan)
  - competition_windows: list[CompetitionWindow]
  - days_since_last_session: int
  - session_index_in_week: int
```

### Rule Actions

```
enum RuleActionType:
  KEEP                    # no change
  REDUCE_LOAD_PCT         # reduce total load by X%
  REMOVE_EXERCISE_FAMILY  # remove all exercises of a family
  ADD_EXERCISE_FAMILY     # add an exercise from a family
  REPLACE_BLUEPRINT       # switch to a different blueprint
  ADD_CONDITIONING        # add a conditioning protocol
  REMOVE_CONDITIONING     # remove conditioning
  SET_MAX_IMPACT          # cap impact_level on all exercises
  SET_MAX_ECCENTRIC       # cap eccentric_cost on all exercises
  FLAG_FOR_REVIEW         # cannot resolve — flag for human coach
```

## Phase 4: Generator Integration (Day 5-7)

### Changes to `src/forge/main.py`

**`generate_program` modifications:**

1. Before session generation loop:
   - Initialize `RollingLoadState` from existing weekly summaries (or empty if new athlete)

2. Within each week:
   - Before generating sessions: evaluate periodization rules → get modifications
   - Generate sessions with modifications applied
   - After generating: compute `SessionLoadMetrics` for each session
   - Accumulate into `WeeklyLoadSummary`
   - Update `RollingLoadState`

3. After generation:
   - Attach `weekly_loads` and `rolling_load` to the returned `TrainingPlan`

4. New input parameter:
   - `load_constraints: Optional[LoadConstraints] = None` — allows callers to override reference loads

### Light Refactor to Conditioning Engine

In `src/forge/conditioning_engine.py`:
- Add exposure bucket awareness to conditioning selection
- When competition window active AND eccentric_exposures > 2, exclude high-eccentric conditioning protocols

## Phase 5: New Top-Level Entry Point (Day 7-8)

### New function: `generate_training_plan` (supersedes `generate_program`)

```
def generate_training_plan(
    athlete_profile: AthleteProfile,
    competition_date: Optional[date] = None,
    training_phase: str = "off_season",
    previous_load: Optional[list[WeeklyLoadSummary]] = None,
    **kwargs
) -> TrainingPlan:
    # 1. Select blueprint based on athlete profile + phase
    # 2. Create periodization context
    # 3. Generate progressive weekly programs
    # 4. Apply rules per week
    # 5. Return enriched TrainingPlan with load data
```

## Phase 6: Reporting (Day 8-9)

### New file: `src/forge/load_report.py`

```
def generate_weekly_report(summary: WeeklyLoadSummary) -> str:
    → Human-readable summary of weekly load and exposures

def generate_acwr_alert(state: RollingLoadState) -> Optional[str]:
    → Returns warning message if ACWR out of range

def generate_exposure_report(week: WeeklyLoadSummary) -> str:
    → Per-bucket exposure summary with coaching interpretation
```

## Phase 7: Tests (Day 9-10)

### Test file: `tests/test_load_calculator.py`
- Test each exercise load calculation
- Test each conditioning load calculation
- Test session load aggregation
- Test weekly load aggregation
- Test ACWR calculation
- Test edge cases (empty session, single exercise, zero load)

### Test file: `tests/test_periodization_engine.py`
- Test each rule in isolation
- Test rule priority ordering
- Test competition window interactions
- Test ACWR red zone forcing deload
- Test exposure deficit adding exercises
- Test exposure excess removing exercises

### Test file: `tests/test_load_report.py`
- Test report generation produces expected format
- Test ACWR alert thresholds

## Summary: Files Changed vs Created

| Action | File | Lines (est) |
|--------|------|-------------|
| Modify | `src/forge/models.py` | +60 |
| Create | `src/forge/load_calculator.py` | +200 |
| Create | `src/forge/periodization_engine.py` | +350 |
| Modify | `src/forge/main.py` | +80 |
| Modify | `src/forge/conditioning_engine.py` | +30 |
| Create | `src/forge/load_report.py` | +100 |
| Create | `tests/test_load_calculator.py` | +150 |
| Create | `tests/test_periodization_engine.py` | +300 |
| Create | `tests/test_load_report.py` | +80 |
| **Total** | | **~1350** |

## Design Decisions

1. **No model migration needed** — all new code is additive, existing V1.5 code untouched
2. **Rule engine is not a rule engine framework** — it's a sequence of if-statements in a `for` loop. No DSL, no configuration files. Rules are code. (If this needs to be user-customizable in V3, extract to a rules file format then.)
3. **Load metrics are computed post-generation** — the generator runs without load awareness, then load metrics are attached. This keeps the generator simple and V1.5-compatible. V3 may do load-aware generation.
4. **ACWR windows are session-count based, not calendar-based** — 7 most recent sessions for acute, 28 for chronic. This handles irregular training schedules.
5. **No persistence layer** — load is computed in-memory and returned with the TrainingPlan. A real deployment would persist `WeeklyLoadSummary` per athlete.
