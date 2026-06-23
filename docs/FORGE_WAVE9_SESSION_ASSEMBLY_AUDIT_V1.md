# FORGE Wave 9 — Session Assembly Audit V1.0

## Overview

This audit traces the current session assembly layer in FORGE to identify exactly how a session is built from blueprint → slots → exercises → final session, and where the output can feel incoherent despite passing all existing validation checks.

## Current Session Assembly Flow

### Step 1: Blueprint Selection (`blueprint_engine.py:select_blueprint`)

1. Shortlist by season phase (`_shortlist_by_season_phase`)
2. Narrow by sport (`_narrow_by_sport`)
3. Apply block autoregulation bias (Wave 7) if prior block response exists

**Winner:** The first matching blueprint is returned.

### Step 2: Slot Resolution (`blueprint_engine.py:resolve_slots`)

```
slots = mandatory_families + optional_families(sorted by slot_order)
# Cap at 8 families
if Core in optional and not in slots: append Core
sorted_slots = sort_by_slot_order(slots)
enforce_session_flow_rules(sorted_slots)  # only moves Core to end
```

**Current ordering:** Only Core is forced to last position. All other families stay in `slot_order` from the blueprint.

### Step 3: Time / Competition Constraint (`main.py:generate_program` → `blueprint_engine.py:apply_time_constraint`)

```python
# Competition proximity reduces preferred count first
if comp_window == 4: preferred = min(7, preferred)
elif comp_window == 2: preferred = min(5, preferred)
elif comp_window == 1: preferred = min(4, preferred)

# Then apply_time_constraint
if available_minutes < 30: max_fams = min(4, preferred)
elif < 45: max_fams = min(5, preferred)
elif < 60: max_fams = min(7, preferred)
else: max_fams = min(8, preferred)

mandatory_fams = {"DLKD", "DLHD", "HPush", "HPull", "Core"}
result = priority_fams[:max_fams]
remaining = max_fams - len(result)
result.extend(optional_fams[:remaining])
```

**Problem 1:** `mandatory_fams` is a **hardcoded set** that may not match the blueprint's actual `mandatory_families`. If a blueprint's mandatory families are `{Sprint, Plyo, Ball, DLKD}`, `apply_time_constraint` will still treat DLKD/HPush/HPull/Core as mandatory, potentially dropping Sprint/Plyo/Ball first — destroying the blueprint identity.

**Problem 2:** `apply_time_constraint` does not reorder families after dropping. The remaining families stay in their original slot order, which may not reflect a coach-like session flow.

**Problem 3:** No consideration of family fatigue cost, impact, or competition role when deciding what to drop. A heavy DLKD exercise could survive while a low-fatigue Sprint primer is dropped.

### Step 4: Role Slot Bias (`main.py:generate_program` → `role_week_planning.py:apply_role_slot_bias`)

```python
effective_slots = apply_role_slot_bias(effective_slots, role_profile)
```

Role bias reorders families based on `family_priority` and `family_de_priority`. This happens **after** time constraint. If a de-prioritized family survived time constraint, it just gets moved to the end of the slot list — it does NOT get dropped.

**Problem 4:** A role-de-prioritized family that the blueprint doesn't strictly need can survive all the way to session construction, pushed to the end but still taking a slot that could have been used for a more valuable family.

### Step 5: Session Construction (`main.py:_build_session`)

```python
for family in slots:
    ex = select_or_continue(family, week, prev_slot_exercises, ...)
    block = SessionBlock(family=family, exercises=[ex] if ex else [])
    blocks.append(block)
```

**Problem 5:** Each family is processed independently. No awareness of the session context:
- If a family has no valid exercise (injury, equipment, competition), the block is created with an empty exercises list
- No session re-balance: if 3 families are empty, the session just has 3 empty blocks
- No reordering of remaining families to maintain flow after empty blocks

**Problem 6:** `select_or_continue` only maintains cross-week continuity (same exercise ID). There is no within-week continuity: if `Sprint` appears in Session 1 and Session 3 of the same week, both get independently selected exercises, potentially identical with no progression logic.

### Step 6: Exercise Selection (`exercise_selector.py:select_exercise` / `progression_engine.py:select_or_continue`)

```python
select_or_continue():
    # Try to continue previous exercise from prev_slot_exercises
    planned_id = plan_exercise_for_slot(family, week, prev_slot_exercises, ...)
    # If still valid (difficulty, equipment, injury, competition), return it
    # Otherwise, select_exercise() — picks from priority list, filtering by injury/equipment/comp
    # If no candidates, substitute_exercise() — 4-priority fallback chain
```

**Problem 7:** If `select_exercise` returns None (no candidates after filtering), the session block is empty. `substitute_exercise` may return a completely different family, but the block still has the **original family label**, creating a mismatch between `block.family` and `block.exercises[0].family`.

**Problem 8:** Injury filtering is per-exercise. If `Sprint` is filtered out due to hamstring risk, but `Plyo` survives, the session might have a plyo block where a sprint block was expected, with no re-ordering to maintain flow.

### Step 7: Conditioning Addition (`main.py:_build_session`)

```python
if should_add_conditioning_for_role(week, day, freq, conditioning_goal, role_profile):
    conditioning = progress_conditioning(...)
```

**Problem 9:** Conditioning is added at the end of the session. This is correct for most cases, but there is no check for whether the session already has high fatigue or high impact, which could make conditioning inappropriate.

### Step 8: Session Output

The session is returned as a list of blocks in slot order, with conditioning appended.

**Problem 10:** No post-assembly reordering. If the first 3 blocks are empty (exercise = None), the session starts with empty blocks, then has actual work later. This is a broken-looking session.

## Which Rules Currently "Win" When They Conflict?

| Conflict | Current Winner | Why |
|----------|---------------|-----|
| Blueprint mandatory vs time constraint | Time constraint | `apply_time_constraint` uses hardcoded mandatory set, not blueprint's actual mandatory |
| Role de-priority vs time constraint | Both survive | Time constraint doesn't know about role de-priority; role bias just reorders |
| Competition taper vs role priority | Competition taper | `comp_window` reduces `preferred` before role bias is applied |
| Injury filtering vs slot order | Slot order | Empty blocks are kept; no re-balance |
| Equipment filtering vs blueprint identity | Equipment filtering | If no exercise matches equipment, the family is empty |
| Within-week family selection | Cross-week continuity | `select_or_continue` prefers previous week's exercise, not same-week variation |

## Awkward Outputs Still Possible

### 1. Blueprint Identity Destruction
**Scenario:** A speed athlete on "Sprint Development" (mandatory: Sprint, Plyo, Ball) with 30 min available.

**Current flow:** `apply_time_constraint` with hardcoded mandatory `{DLKD, DLHD, HPush, HPull, Core}` keeps DLKD/HPush and drops Sprint/Plyo/Ball because the blueprint's actual mandatory families are not considered.

**Result:** The session is labeled "Sprint Development" but has no speed work.

### 2. Empty Block Domination
**Scenario:** An athlete with hamstring injury risk on a blueprint with Sprint, DLKD, HPush, HPull, Core.

**Current flow:** `select_or_continue` for Sprint returns None (hamstring risk filtered). `select_or_continue` for DLKD returns a valid exercise. Session blocks: `[Sprint(None), DLKD(Ex), HPush(Ex), HPull(Ex), Core(Ex)]`.

**Result:** Session starts with an empty block, then continues with valid work. No re-balance.

### 3. Bad Sequencing
**Scenario:** A strength blueprint with slot order: `[DLKD, HPush, DLHD, HPull, Core, Sprint]`.

**Current flow:** After role bias, Sprint is moved to end. Session: `[DLKD, HPush, DLHD, HPull, Core, Sprint]`.

**Result:** Sprint (neural, low-fatigue) appears after heavy strength and core. This is a waste of neural freshness. Sprint should be early.

### 4. Same Exercise Duplicated Within a Week
**Scenario:** Full Body Strength, 3x/week, all sessions have DLKD.

**Current flow:** `select_or_continue` uses `prev_slot_exercises` keyed by family value. If the same exercise ID was used last week, it continues. But within the same week, each session independently calls `select_or_continue` with the same `prev_slot_exercises` (which is updated per session, not per week).

**Result:** Sessions 1 and 2 of the same week might both have Back Squat with no intentional variation. Session 3 might have Front Squat because `prev_slot_exercises` was updated by Session 2. This is inconsistent, not progressive.

### 5. Core Disappearing
**Scenario:** Blueprint with Core in optional, time constraint reduces to 4 families.

**Current flow:** `apply_time_constraint` hardcoded mandatory includes Core. But if the blueprint's mandatory families already fill 4 slots (e.g., DLKD, DLHD, HPush, HPull), Core is dropped even though it's structurally expected.

**Result:** No trunk work in a strength session.

### 6. Accessory Surviving While Primary Work Drops
**Scenario:** A blueprint with mandatory [DLKD, DLHD] and optional [Sprint, Plyo, Carry, Acc, Core]. Time constraint = 30 min (max 4 families).

**Current flow:** `apply_time_constraint` keeps `{DLKD, DLHD, HPush, HPull}` (hardcoded). Sprint and Plyo are dropped. Carry and Acc are already gone. But if the blueprint didn't have HPush/HPull in mandatory, they could survive while Sprint/Plyo are dropped.

**Result:** Accessory strength survives while explosive/speed work is lost. This is fine for a strength block, but not for a speed block.

## Code Paths Summary

```
main.py:generate_program
  → blueprint_engine.py:select_blueprint
  → blueprint_engine.py:resolve_slots
  → blueprint_engine.py:apply_time_constraint  [HARDEN: use blueprint mandatory, not hardcoded]
  → main.py: role bias on slots  [HARDEN: drop de-prioritized before time constraint]
  → main.py: _build_session  [HARDEN: reorder, re-balance, within-week continuity]
    → progression_engine.py:select_or_continue  [HARDEN: within-week variation]
      → exercise_selector.py:select_exercise / substitution_engine.py:substitute_exercise
  → main.py: add conditioning
  → progression_engine.py:review_week  [HARDEN: session assembly quality checks]
```

## What Needs to Change

1. `apply_time_constraint` must use the blueprint's actual `mandatory_families`, not a hardcoded set
2. `apply_time_constraint` must consider competition role (speed/power/strength) when dropping, not just family count
3. Session construction must re-balance after exercise filtering: empty blocks should be removed or backfilled, and remaining blocks reordered
4. Session order must reflect real S&C flow: speed/power → primary strength → secondary strength → accessory/trunk
5. Within-week family continuity: if a family appears multiple times in the same week, the second appearance should be a purposeful variation (not a duplicate or random selection)
6. Role de-prioritized families should be dropped before time constraint, not just reordered after
7. Post-assembly validation must check session coherence (not just exercise validity)
