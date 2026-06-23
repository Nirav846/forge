# Real-World Coaching Comparison Audit

## Source Data

| Source | What It Contains |
|--------|-----------------|
| Coaching Patterns Summary | 58 elite programs across 7 sports |
| Movement Frequency Report | % frequency of each family in real programs |
| Program Output Validation | 12+ FORGE-generated programs scored 4-7/10 |
| Stress Test | 168 programs, 12,107 selections, 1,962 empty slots |
| Bodyweight Analysis | Bodyweight-specific empty slot patterns |
| Blueprint Architecture Review | Cross-sport session architecture comparison |

---

## 1. Session Structure Comparison

### Real-World Session Architecture (85%+ of elite programs)

```
Mobility → Activation → Power → Primary Strength → Secondary Strength → Pull → Push → Core
```

Every elite program follows this sequence. It never varies in intent:
- **Power before strength** — non-negotiable
- **Fresh before fatigue** — speed/power first
- **Core last** — always

### FORGE Session Architecture

```
[Resolved from slot_order + mandatory + optional]
```

FORGE generates slot sequences that *happen* to be ordered correctly 85% of the time (because the blueprints were seeded from real programs). But the architecture has **no concept of session blocks**. A FORGE session is a flat list of family slots. There is no:

- Warm-up block (mobility + activation before anything loaded)
- Power block (one or more explosive families, always first)
- Strength block (primary then secondary, with pairing logic)
- Core block (always last)

### Concrete Example

**Real coach session (Full Body Strength):**
```
1. Foam rolling / mobility (5 min)
2. Activation: glute bridges, band pull-aparts, dead bugs (8 min)
3. Power: Med ball chest pass (3×5) OR Box jump (3×3)
4. Primary strength: Back squat (3×5)
5. Secondary strength: RDL (3×8) + Pull-up (3×8) — paired superset
6. Accessory: DB bench (3×10) + DB row (3×10) — paired superset
7. Core: Plank + dead bug circuit (8 min)
8. Prehab: Band work (5 min)
```

**FORGE output (Full Body Strength, bodyweight, intermediate):**
```
Ballistic — [exercise]
DLKD — [exercise]
HPush — [exercise]
DLHD / HPull — [exercise]
Core — [exercise]
```

**Deficits:**
- No warm-up or activation block
- No block concept — exercises are listed without superset/pairing information
- Core appears alone without prehab
- No guidance on sets/reps/rest between blocks

---

## 2. Specific Pattern Gaps

### Pattern 1: Warm-Up / Activation (Present in 95% of elite programs)

**Real pattern:** Every elite session starts with 5-15 minutes of mobility + activation:
- Hip mobility (world's greatest stretch, 90/90)
- Shoulder mobility (band dislocates, PVC pass-throughs)
- Glute activation (glute bridges, band lateral walks)
- Core activation (dead bugs, bird dogs)
- Movement prep (A-skips, high knees, inchworms)

**In FORGE:** No warm-up block exists. The Acc/Prehab family contains individual exercises (Band Pull-Apart, Glute Med Clamshell, PVC Pass-Through) that COULD form a warm-up, but there is no mechanism to combine them into a pre-session sequence. The only blueprint that references Acc/Prehab in slot order is Return to Sport (as slot 1). 255 empty Acc/Prehab slots because it's treated as a family slot, not a warm-up block.

**Verdict: MISSING CONCEPT.** The system has warm-up materials (Acc/Prehab exercises) but no warm-up *structure*.

### Pattern 2: Paired Supersets (Present in 80%+ of programs)

**Real pattern:** Coaches pair exercises within sessions:
- Squat + Pull-up (agonist-antagonist)
- RDL + Push-up (posterior chain + upper push)
- Row + Core (pull + anti-extension)
- All in superset format: set of A → rest 60s → set of B → rest 60s → repeat

**In FORGE:** All exercises are listed linearly. No pairing, no superset logic, no rest guidance.

**Verdict: MISSING CONCEPT.** Coaching credibility requires pairing.

### Pattern 3: Olympic Lift Isolation (100% of elite programs using them)

**Real pattern:** Olympic lifts are NEVER paired with other exercises. They are always performed first in the session, isolated, with full recovery (3-5 min).

**In FORGE:** Olympic lifts (Ballistic family) are treated as a regular slot that can appear alongside anything. The Ballistic slot is placed first in most blueprints, which is architecturally correct — but there's no mechanism to prevent pairing.

**Verdict: DATA PROBLEM.** The exercises are correct but the constraint that "Ballistic is never paired" exists only in the Coaching Patterns document, not in the system.

### Pattern 4: Pull-Push Balance Within Sessions

**Real pattern:** Horizontal pull appears before horizontal push in 90% of programs (pre-exhaustion for posture). Sessions maintain rough pull-push balance. A session with 2 upper body slots always has 1 pull + 1 push.

**In FORGE:** HPull appears in slot_order only when explicitly listed. The Upper / Lower Split upper day has: VPush, HPush, VPull, HPull — good. But Full Body Strength has: HPush, DLHD / HPull — HPull is optional (split choice). This means a coach choosing DLHD over HPull gets a session with no horizontal pulling. The stress test confirmed: HPull has **342 empty slots** across all equipment levels.

**Verdict: ARCHITECTURE PROBLEM.** The `/` slot choice mechanism (DLHD / HPull) allows zero-horizontal-pull sessions in blueprints where real coaches would never allow this.

### Pattern 5: Core Always Last (100% of elite programs)

**Real pattern:** Core training is ALWAYS the last strength block in the session. Never before power or primary strength.

**In FORGE:** Core is last in the slot_order of most blueprints ✅. But there is no enforcement — if a coach reorders slots, Core could appear early. Also, Core has 81 empty slots for advanced bodyweight because L4+ bodyweight Core doesn't exist.

**Verdict: DATA PROBLEM** (empty slots) but architecture is correct.

### Pattern 6: Block Periodization (90% of programs)

**Real pattern:** Coaches organize training into 4-6 week blocks with specific focus: Strength → Power → Speed → Taper. Exercises rotate between blocks, not within sessions.

**In FORGE:** The 4-week program generation varies difficulty by week (w_diff_min/max adjustment). This crudely approximates progressive overload. But there is no block structure — weeks 1-4 are identical except for difficulty creep. Real coaches change exercises, volume, and intent by block.

**Verdict: ARCHITECTURE PROBLEM.** The system has no block concept.

### Pattern 7: 3-Day In-Season Standard (2 gym sessions/week)

**Real pattern:** In-season programs use 2 gym sessions/week. The blueprint frequency system expresses this as "2-3" but doesn't enforce season phase adjustment. A coach running "Full Body Strength" in-season gets 3-4 sessions/week, which is off-season volume.

**In FORGE:** Blueprint frequency is static. No season-phase awareness.

**Verdict: DATA PROBLEM.** Would require season tagging, not architecture change.

### Pattern 8: Activation Exercises Are Not "Strength" Work

**Real pattern:** Glute bridges, band pull-aparts, shoulder dislocates are ACTIVATION, not strength. They appear in the warm-up at low intensity. Coaches don't count them as strength exercises.

**In FORGE:** Glute Bridge (DLHD L1) is classified as a strength exercise. It gets selected as a primary DLHD strength slot exercise for bodyweight athletes (131×, all beginner). A coach seeing "DLHD: Glute Bridge" as a primary strength exercise would question the program — even though Glute Bridge is a valid exercise. The issue is classification, not the exercise itself.

**Verdict: DATA PROBLEM.** Glute Bridge should be multi-tagged as Activation/Strength, not exclusively Strength. Min difficulty for DLHD strength slots should be L2.

---

## 3. Findings Categorization

### A. Architecture Problems (3)

| # | Problem | Impact | Fix |
|---|---------|--------|-----|
| A1 | **No session block concept** — FORGE generates flat family lists. Real sessions have blocks (Warm-up → Activation → Power → Strength → Accessory → Core) with different rules per block. | High — affects every generated program | 1. Add optional `block` field to blueprint slots: `"warmup"`, `"activation"`, `"power"`, `"strength_primary"`, `"strength_secondary"`, `"core"`. Blocks group consecutive families. 2. All exercises in `"power"` block maintain explosive filter. 3. All exercises in `"activation"` block filter on `difficulty <= 2`. 4. Blocks are rendered with headings (WARM-UP, POWER, STRENGTH, CORE) |
| A2 | **"/" slot choice allows unbalanced sessions** — `"DLHD / HPull"` means either DLHD (zero pulls) or HPull (zero hip). Real coaches would never drop horizontal pulls. | Medium — creates 342 empty HPull slots | Replace `/` with a weighted pair: both families appear, system picks order. Or make slot a list (`["DLHD", "HPull"]`) where both are always included. |
| A3 | **No block periodization** — 4-week generation varies difficulty only. Real programs change exercises and intent across 4-6 week blocks. | Low for credibility (8→9), high for full system | Add optional `block_focus` parameter: `"strength"`, `"power"`, `"peak"`. Changes filter logic per block. |

### B. Data Problems (4)

| # | Problem | Impact | Fix |
|---|---------|--------|-----|
| B1 | **HPull bodyweight L2+ gap** — 342 empty slots, #1 system gap. | High — affects 286 bodyweight + 56 minimal slots | Add 1 bodyweight HPull exercise at L2 (Table Row) |
| B2 | **Glute Bridge is sole DLHD bodyweight exercise** — classified as STR/L1 but coaches use it as activation. Forces cross-family 245×. | Medium | Add DLHD L2 bodyweight (Glute Bridge March). Consider reclassifying Glute Bridge as activation/STAB only. |
| B3 | **VPull bodyweight L2+ gap** — only Band Lat Pulldown L1. 39 empty slots. | Medium | Add 1 bodyweight VPull exercise at L2 (Band Straight-Arm Pulldown) |
| B4 | **"All" optional pool bug (RC5)** — 3 blueprints have `optional=["All"]` which resolves to 15 families then randomly picks 0-2. Creates 229 empty slots. | High | Fix `resolve_slot_families` to properly handle "All": pick 2-4 families weighted by blueprint compatibility, not random from 15. |

### C. Missing Coaching Concepts (2)

| # | Concept | Impact | Fix |
|---|---------|--------|-----|
| C1 | **Warm-up / Activation block** — 95% of elite programs include mobility + activation before work. Materials exist (Acc/Prehab) but no structure. | High — every generated program currently skips warm-up | Add `"warmup"` and `"activation"` as optional pre-session blocks. Not mandatory (preserves simplicity) but auto-inserts 2-4 Acc/Prehab exercises before the first power/strength slot. *Not a new entity* — it's a rendering convention for existing families. |
| C2 | **Superset pairing** — 80%+ of programs pair exercises. No pairing = flat/unnatural session read. | Medium | Add optional `paired_with` field to slot_order entries. When present, render adjacent slots as a superset. *Not a new entity* — it's a slot_order annotation. |

---

## 4. Sufficiency Assessment

### Are Exercise Families Sufficient?

**Yes.** The 15 families cover every movement pattern in the 58-program corpus. No missing family was identified during this audit. The only gap is bodyweight coverage within existing families, not missing families.

### Are Blueprints Sufficient?

**Yes.** 14 blueprints cover all programs. The audit confirms:
- Full Body Strength → replaces BCCI-ASCA gym session, All Blacks gym, EPL academy gym
- Court Sport → replaces tennis/badminton gym sessions
- Power + Speed → replaces sprint-specific gym sessions
- Power Maintenance → replaces all in-season programs
- Return to Sport → replaces post-injury protocols
- Deload → replaces recovery blocks

**One recommendation:** The Upper / Lower Split blueprint contradicts the finding that elite coaches don't use body-part splits for field athletes. The coaching patterns document explicitly calls this an anti-pattern. Retain it (for bodybuilding/hypertrophy focus only) but add a warning label. Do not remove — some programs legitimately use it.

### Are Session Blocks Required?

**Not as a new entity.** A `block` annotation on existing slot_order entries is sufficient. Example:

```python
# Current:
slot_order = ["Ball", "DLKD", "HPush", "DLHD / HPull", "Core"]

# Proposed:
slot_order = [
    ("warmup", ["Acc/Prehab"]),           # 2-4 Acc/Prehab exercises
    ("power", ["Ball"]),                   # Power block: explosive only
    ("strength_primary", ["DLKD"]),       # Primary strength
    ("strength_secondary", ["HPush", "DLHD / HPull"]),  # May be paired
    ("core", ["Core"]),                    # Core: always last
]
```

Blocks are a *rendering convention*, not a new entity. They:
- Add headings (WARM-UP, POWER, STRENGTH, CORE)
- Apply block-specific filters (power→explosive only, activation→diff<=2)
- Enable superset rendering (adjacent exercises in strength blocks)
- Don't change exercise selection logic

### Are Pairing Rules Required?

**Not as a new entity.** Add an optional `paired_with` field to slot entries. When `slot_order` contains adjacent entries with `paired_with` pointing at each other, render them as a superset. This is a data annotation, not new code.

### Should Warm-Up/Activation Be Separate?

**Not as a separate library.** The existing Acc/Prehab exercises are sufficient for warm-up content. What's missing is the structural convention to group them before the first strength/power slot. This can be solved with the block annotation above.

---

## 5. Real vs FORGE: Head-to-Head Comparison

### Session: Full Body Strength (Intermediate, Basic Gym)

**Real coach (source: StrengthLog / BCCI-ASCA -type program):**
```
WARM-UP (8 min)
  - Band pull-apart × 15
  - Glute bridge × 10
  - Dead bug × 8 each side
  - World's greatest stretch × 5 each side

POWER (10 min)
  - Med ball chest pass 3×5  [60s rest]

STRENGTH (25 min)
  A1. Barbell back squat 3×5
  A2. Pull-up 3×8
    [superset, 90s rest]

  B1. Barbell RDL 3×8
  B2. DB bench press 3×10
    [superset, 75s rest]

CORE (7 min)
  - Plank 3×30s
  - Side plank 3×20s each
  - Dead bug 2×8 each

PREHAB (5 min)
  - Band external rotation × 15
  - Ankle dorsiflexion × 10 each
```

**FORGE output (Full Body Strength, intermediate, basic gym):**
```
Ballistic
  * Med Ball Chest Pass  [L2]  (Medicine Ball)

Double Leg Knee Dominant
  * Barbell Back Squat  [L3]  (Barbell + Rack)

Horizontal Push
  * Dumbbell Bench Press  [L3]  (DB + Bench)

Double Leg Hip Dominant / Horizontal Pull
  * Single-Leg RDL  [L3]  (DB/KB)   ← picked DLHD

Core
  * Side Plank (leg raise)  [L3]  (Bodyweight)
```

**Deficits:**
1. No warm-up → first exercise is explosive med ball work on cold muscles (not credible)
2. No superset pairing → 7 exercises would take 45+ minutes with straight sets; real coach fits in 60 min via supersets
3. No Horizontal Pull (HPull dropped because `/` chose DLHD)
4. Single-Leg RDL for DLHD slot → exercise is correct but SL RDL is cross-family
5. Core is a single exercise, not a circuit
6. No prehab block

**Score:** ~6/10 compared to real session

---

## 6. Final Recommendation

### The Smallest Change to Go From 8/10 to 9/10

**One change: Add block annotations to blueprints.**

Specifically:

### What changes

In `forge_prototype.py`, modify `Blueprint` to accept an optional `blocks` parameter:

```python
@dataclass
class Blueprint:
    name: str
    frequency: str
    slot_order: list          # unchanged
    mandatory: list           # unchanged
    optional: list            # unchanged
    blocks: list = None       # NEW: [("warmup", [...]), ("power", [...]), ...]
    notes: str = ""
```

When `blocks` is present, `generate_session`:
1. Emits a warm-up heading + 2-3 Acc/Prehab exercises (difficulty ≤ L2, bodyweight/band)
2. Emits a power heading + explosive family exercises first
3. Emits a strength heading + remaining families
4. Emits a core heading + core exercise(s) last
5. For adjacent strength slots → annotate as A1/B1 superset pairs in output

When `blocks` is absent (backward compat): current behavior.

### Why this is the smallest change

- **No new entities.** Blocks are annotations on existing blueprints.
- **No new code paths.** The exercise selection logic is unchanged.
- **No new families.** Warm-up uses existing Acc/Prehab exercises.
- **Backward compatible.** Blueprints without blocks render as today.
- **Leverages existing data.** The 255 empty Acc/Prehab slots become warm-up slots.
- **Coaching credibility impact:** +1.0+ — the biggest single lever.

Warm-up alone fixes: cold-start explosive work, missing activation, prehab as an
afterthought. Superset annotation fixes: session pacing, realistic volume.

### What does NOT change

- Exercise ontology stays frozen (15 families, 191 exercises)
- Blueprint catalog stays frozen (14 blueprints)
- Selection/substitution logic stays frozen (RC1 already fixed)
- No AI, no sport-specific logic, no new entities
- RC2 bodyweight additions stay deferred

### After this change

A FORGE-generated Full Body Strength session would look like:

```
WARM-UP
  * Band Pull-Apart  [L1]  (Band)
  * Glute Med Clamshell  [L1]  (Band/Bodyweight)
  * Dead Bug  [L1]  (Bodyweight)

POWER
  * Med Ball Chest Pass  [L2]  (Medicine Ball)

STRENGTH
  A1. Barbell Back Squat  [L3]  (Barbell + Rack)
  A2. Lat Pulldown  [L2]  (Cable Machine)

  B1. Single-Leg RDL  [L3]  (DB/KB)
  B2. Dumbbell Bench Press  [L3]  (DB + Bench)

CORE
  * Side Plank (leg raise)  [L3]  (Bodyweight)
  * Dead Bug  [L1]  (Bodyweight)
```

**Coaching credibility estimate:** 8.5-9/10 — warm-up, power isolation, superset
pairing, core circuit. The only remaining deficit is block periodization, which
is a 9→10 change.

---

## Summary Decision Matrix

| Finding | Type | Priority | Fix Lines | Credibility Gain |
|---------|------|----------|-----------|-----------------|
| Block annotations | Architecture | **P0** | ~30 | +1.0 |
| RC5: "All" optional fix | Data | **P0** | ~5 | +0.5 |
| HPull bodyweight L2 fix | Data | **P1** | 1 row | +0.5 |
| RC1 already done | Code | ✅ | 3 lines | +1.8 |
| Warm-up on empty Acc slots | Leverage | **P0** | ~10 | +0.3 |
| Glute Bridge March (DLHD L2) | Data | P1 | 1 row | +0.2 |
| Band Straight-Arm Pulldown (VPull L2) | Data | P1 | 1 row | +0.3 |
| Superset pairing annotation | Architecture | P1 | ~15 | +0.3 |
| Pike Push-Up (VPush L2) | Data | P2 | 1 row | +0.2 |
| Block periodization | Architecture | P2 | ~30 | deferred |
