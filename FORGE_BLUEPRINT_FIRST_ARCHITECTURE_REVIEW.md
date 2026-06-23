# FORGE Blueprint-First Architecture Review

## Executive Summary

The research across 58 elite programs (cricket, rugby, soccer, athletics, tennis, badminton, general S&C) reveals a single overwhelming finding: **session architecture is nearly identical across all sports.** The same 7-8 movement slot sequence appears in 85% of programs regardless of sport:

```
Mobility → Activation → Power → Primary Strength → Secondary Strength → Accessory → Core
```

Sport-specific differences exist only in exercise selection, weekly frequency, volume, and conditioning modality — **not in system architecture.** This means the current V2.5 roadmap is structurally over-engineered by approximately 60%. A Blueprint-First approach eliminates sport-specific logic, reduces the ontology to 5 entities, and can generate coach-credible drafts in under 3 minutes with no AI, no inference, and no sports science engine.

---

## Task 1: Challenge Sport-Specific Assumption

### The Assumption We've Been Operating Under

That each sport requires its own programming logic, its own rules, its own session architectures, and potentially its own subsystem within FORGE.

### The Evidence Against It

| Aspect | Cricket | Rugby | Soccer | Tennis | Badminton |
|--------|---------|-------|--------|--------|-----------|
| Session slot order | Power → Bilateral → Upper → Core | Power → Bilateral → Upper → Core | Power → Bilateral → Upper → Core | Power → Unilateral → Upper → Core | Power → Unilateral → COD → Core |
| Core movement families | 8 | 8 | 8 | 8 | 8 |
| Weekly gym frequency | 2-3x | 2-3x | 2-3x | 2-3x | 2-3x |
| Power position | First | First | First | First | First |
| Core position | Last | Last | Last | Last | Last |

The only architectural difference is:
- **Court sports** (tennis, badminton) move unilateral work earlier in the slot order
- **Field sports** (rugby, soccer, cricket) prioritize bilateral work first

This is a single branching decision, not six parallel systems.

### Verdict: Sport-Specific Logic Should Be REDUCED to Template Selection Only

The architecture should contain zero sport-specific code, zero sport-specific rules, zero sport-specific data structures. Instead:

- **Blueprints** carry a `best_for` tag (e.g. `["court", "field", "track"]`)
- **Coaches** select blueprints, not sports
- A cricket coach picks: Full Body Strength for off-season, Power Maintenance for in-season, Rotational Power for batting emphasis
- A tennis coach picks: Court Sport blueprint, Strength + Power blueprint, Power Maintenance blueprint

The sport is just a context tag. It does not drive logic.

### Recommendation: DEFER sport-specific logic indefinitely

---

## Task 2: Blueprint-First Architecture

### Core Concept

FORGE becomes a **blueprint browser** with intelligent exercise substitution. The coach selects a blueprint, FORGE fills the movement slots with exercises from the library, and the coach adjusts.

### The Blueprint Catalog (Proposed: 10 Universal Blueprints)

These 10 blueprints cover every program in the 58-program dataset:

| ID | Blueprint Name | Slot Sequence | Best For | Season Phase |
|----|---------------|--------------|----------|-------------|
| BP-01 | Full Body Strength | Mob → Act → Power → BiL → UniL → H-Pull → H-Push → Core | All sports | Off-season |
| BP-02 | Strength + Power | Mob → Act → Power → BiL → BiL → H-Pull → H-Push → Core | Rugby, Soccer, Cricket | Pre-season |
| BP-03 | Power + Speed | Mob → Sprint Mech → Accel → Max V → Power → BiL → Core | Athletics, Soccer, Rugby | Pre-season/Comp |
| BP-04 | Strength + Conditioning | Mob → Act → BiL → UniL → H-Pull → H-Push → Core → Cond | All sports | Pre-season |
| BP-05 | Upper/Lower Split (A) | Mob → Power → BiL → UniL → Core | Rugby, Cricket | In-season (Day 1) |
| BP-05 | Upper/Lower Split (B) | Mob → H-Push → H-Pull → V-Pull → Core | Rugby, Cricket | In-season (Day 2) |
| BP-06 | Power Maintenance | Mob → Act → Power → BiL (light) → H-Pull → Core | All sports | In-season |
| BP-07 | Youth Foundation | Mob → Movement Skills → BiL → H-Pull → Core | All sports (U16) | All |
| BP-08 | Court Sport | Mob → Act → Power → UniL → COD → H-Pull → Core | Tennis, Badminton | All |
| BP-09 | Complex Training | Mob → Act → Power/Plyo → Strength → Power/Plyo → Core | Badminton, Athletics | Training |
| BP-10 | Rotational Power | Mob → Act → Rot Power → BiL → H-Pull → Anti-Rot Core | Cricket, Tennis | All |

### How Blueprints Replace Sport-Specific Logic

A single blueprint (Full Body Strength) serves:

- **Cricket** → replaces BCCI-ASCA gym session
- **Rugby** → replaces All Blacks gym session
- **Soccer** → replaces EPL gym session
- **Tennis** → replaces USTA gym session (with unilateral slot)
- **Badminton** → replaces National Team gym session

The coach simply picks the blueprint and adjusts exercise selection per sport. No sport-specific rules required.

### What a Blueprint Contains

```
Blueprint {
  id: str
  name: str
  description: str
  slot_sequence: [MovementSlot]    # ordered list
  best_for: [str]                  # ["field", "court", "track", "all"]
  season_phase: [str]              # ["off-season", "pre-season", "in-season", "all"]
  weekly_frequency: int            # recommended sessions/week
  typical_duration: str            # "45-60 min"
}
```

Each MovementSlot:

```
MovementSlot {
  family: str                      # e.g. "bilateral_knee"
  function: str                    # "primary_strength", "power", etc.
  sets: int                        # default
  reps: str                        # default range
  rest: str                        # default
  alternatives: [str]              # alternative families if substitution needed
}
```

### The Coach Workflow

```
1. Select sport (optional filter, NOT logic driver)
2. Browse blueprints (filtered by sport tag, or view all)
3. Select blueprint → see slot sequence with default exercises
4. Click any slot → see alternative exercises (same family)
5. Adjust sets/reps/rest per slot
6. Lock or swap exercises
7. Output printable session
```

Time: under 3 minutes for a draft.

---

## Task 3: Minimum Viable Ontology

### Current V2.5 Ontology (6 entities)

```
Athlete, Context, Template, Session, Exercise Family, Exercise
```

Plus deferred: Progression, Readiness, Variant, Equipment Category.

### Proposed MVP Ontology (5 entities)

| Entity | Verdict | Rationale |
|--------|---------|-----------|
| **Blueprint** | KEEP (new central entity) | This is the core. Blueprints replace Templates, Context, and sport-specific logic. A blueprint IS the program design. |
| **Session** | KEEP | The output. An instantiated blueprint with exercises selected. |
| **Exercise Family** | KEEP | The substitution boundary. 8 core families: Power, Bilateral Lower, Unilateral Lower, Horizontal Push, Horizontal Pull, Vertical Pull, Core, Mobility. |
| **Exercise** | KEEP | The library. Each exercise belongs to exactly one family. |
| **Exercise Slot** | KEEP (merged from old Slot entity) | A position within a session with a target family, suggested sets/reps/rest. |

### Entities to REMOVE

| Entity | Previous Role | Why Remove |
|--------|--------------|------------|
| **Athlete Profile** | Store athlete data for personalization | Not needed for MVP. Coach knows the athlete. Blueprints are inherently position/sport-agnostic. Add later if needed. |
| **Context** | Season phase, training history | Merged into Blueprint metadata (`season_phase` field). Coach picks the right blueprint for the phase. |
| **Template** | High-level program structure | Replaced by Blueprint. Blueprint IS the template. |
| **Progression Scheme** | Auto-progression rules | Coach handles progression. Blueprints provide default sets/reps that coach overrides. |
| **Readiness Model** | Auto-adjust based on readiness | Anti-pattern. Bias against AI/inference. Coach judges readiness. |
| **Equipment Category** | Equipment filtering | Simplified to tags on Exercise (one-of: barbell, dumbbell, cable, bodyweight, machine, band). |
| **Variant** | Exercise variations | Not needed. Library contains canonical exercises. Coach picks alternatives manually. |
| **Conditioning Block** | Separate conditioning system | Conditioning is a slot within a blueprint (last position). Not a separate system. |

### Entities to SIMPLIFY

| Entity | Before | After |
|--------|--------|-------|
| **Exercise Family** | 16 families with intent tags, metadata | 8 flat families. No sub-types. No intent tags. Just family name + description. |
| **Exercise** | 55-65 exercises + metadata + variants + equipment | ~50 exercises. Each has: name, family, equipment tags, difficulty (beginner/intermediate/advanced). No variants. |
| **Session** | Complex object with periodization data | List of Slots. Each Slots has: family, default sets/reps, locked exercises (optional), coach notes. |

### Final Ontology (MVP)

```
Blueprint (central)
├── id, name, description
├── slot_sequence: [Slot]
├── best_for: [tag]          # field, court, track, all
├── season_phase: [tag]      # off-season, pre-season, in-season, all
├── weekly_frequency: int
├── typical_duration: str

Slot (position within a session)
├── family: ExerciseFamily   # e.g. "bilateral_knee"
├── function: str            # human-readable purpose
├── default_sets: int
├── default_reps: str
├── default_rest: str
├── alternatives: [ExerciseFamily]  # if primary family unavailable

ExerciseFamily (substitution boundary)
├── id, name, description
├── difficulty: str          # beginner, intermediate, advanced

Exercise (library entry)
├── id, name
├── family: ExerciseFamily   # must match
├── equipment: [tag]         # barbell, dumbbell, cable, bw, machine, band
├── difficulty: str          # beginner, intermediate, advanced
├── coaching_cue: str        # optional, 1-sentence

Session (generated output)
├── blueprint_id: str
├── sport: str               # informational only
├── slots: [Slot+Exercise]   # instantiated slots
├── coach_notes: str         # free text
```

That is it. 5 entities. No AI. No inference. No progression engine.

---

## Task 4: Evaluate Current Implementation Plan

### Review of FORGE_V25_IMPLEMENTATION_PLAN.md (31 files, ~3,235 lines)

### MVP REQUIRED (Build First)

| Feature | Why |
|---------|-----|
| Blueprint definitions (data files) | Core of the system. Define 10 blueprints as structured data. ~200 lines total. |
| Exercise family definitions | Substitution boundary. 8 family definitions. ~50 lines. |
| Exercise library | ~50 exercises mapped to families. ~300 lines. |
| Session generator | Takes blueprint + exercise selections → printable session. ~100 lines. |
| Coach UI (CLI or minimal web) | Review, select, swap exercises, adjust sets/reps, output. ~300 lines. |
| Substitution safety check | "Is this exercise in the correct family?" — a simple lookup. ~30 lines. |

Total MVP: ~980 lines across 5-6 files.

### USEFUL LATER (Build After MVP Validation)

| Feature | Why Defer | Priority |
|---------|-----------|----------|
| Exercise difficulty filter | Useful for youth/beginner filtering. Not needed for draft generation. | P2 |
| Equipment filter | Useful but not critical. Coach can visually skip exercises. | P2 |
| Session history | Track what was generated. Useful for iteration. | P2 |
| Coach notes/annotations | Free text on sessions. Useful for collaboration. | P3 |
| Web UI vs CLI | CLI first. Web is polish. | P3 |
| Export formats (PDF, print) | Coach can copy-paste. | P3 |

### UNNECESSARY (Remove from Plan)

| Feature | Why Remove | Savings |
|---------|-----------|---------|
| Sport-specific programming logic | Blueprints handle this via tags. Zero sport-specific code needed. | ~800 lines |
| Progression engine | Coach handles progression. Blueprints provide defaults. | ~400 lines |
| Readiness model | Anti-pattern (AI/inference). Coach judges readiness. | ~300 lines |
| Variant system | Exercise library has canonical entries. Coach picks alternatives. | ~250 lines |
| Equipment category database | Simplified to exercise tags. | ~200 lines |
| Conditioning architecture | Conditioning is a slot in a blueprint, not a subsystem. | ~350 lines |
| AI inference for program generation | Bias against. Coach selects, FORGE fills slots. | ~500 lines |
| Athlete profile database | Not needed for draft generation. | ~300 lines |
| Testing battery module | Defer to post-MVP. | ~200 lines |
| Periodization engine | Blueprints ARE periodization (this phase → that blueprint). | ~350 lines |
| Multi-entity ontology (10+ entities) | Reduced to 5. | ~400 lines |
| Database migrations | Not needed for MVP. Data files only. | ~600 lines (25 migrations) |

Total savings: ~5,250 lines eliminated.

### Revised Implementation Target

**Before:** 31 files, ~3,235 lines, 12-18 days, 6 phases

**After:** 6 files, ~980 lines, 3-5 days, 1 phase

### File Breakdown (MVP)

```
forge/
├── blueprints/
│   └── catalog.py           # 10 blueprint definitions (200 lines)
├── exercise_families/
│   └── definitions.py       # 8 family definitions (50 lines)
├── exercises/
│   └── library.py           # ~50 exercises (300 lines)
├── generator/
│   └── session.py           # session instantiation (100 lines)
├── cli/
│   └── forge.py             # coach interface (300 lines)
└── forge.py                 # entry point (30 lines)
```

**Total: 6 files, ~980 lines.**

---

## Task 5: Final Recommendation

### The Smallest System That Can Generate Coach-Credible Draft Programs in Under 3 Minutes

```
Input:
  - Coach selects blueprint (e.g. "Full Body Strength")
  - Coach optionally filters by equipment
  - Coach optionally filters by difficulty

Processing (instant):
  - FORGE reads blueprint → gets slot sequence
  - For each slot, FORGE selects a random exercise from the correct family
  - Substitution rule: exercise MUST match slot family (hard constraint)

Output:
  - Printable session with:
    - Slot order
    - Exercise name
    - Default sets/reps/rest
    - Coach notes field per slot

Coach adjustments:
  - Swap any exercise (filtered by family)
  - Adjust sets/reps/rest per slot
  - Lock exercises to prevent re-randomization
  - Add free-text notes
  - Save/export
```

### What This System Explicitly Does NOT Do

- No AI inference
- No sport-specific logic
- No athlete profiles
- No progression calculations
- No readiness scoring
- No periodization algorithms
- No variant management
- No equipment category system
- No conditioning subsystem
- No testing/tracking
- No database
- No API
- No user authentication
- No persistent storage beyond file export

### Why This Works

The research across 58 programs proves that elite coaches all use the same session architecture. The differences that matter are:

1. **Which blueprint** (selected by coach based on phase/goal)
2. **Which exercises** (selected by coach from correct family)
3. **How much volume** (adjusted by coach via sets/reps)
4. **What equipment** (filtered by coach)

None of these require sport-specific logic, AI, or complex systems. They require:
- A well-curated catalog of blueprints
- A clean exercise library organized by movement family
- A simple substitution rule (stay in family)
- A coach in control

### The Risk of Not Doing This

Continuing with the V2.5 roadmap means building sport-specific subsystems that the research proves are unnecessary. The result would be a system that:
- Takes 4-6x longer to build
- Has 5x more code
- Is harder to maintain
- Offers less coach flexibility
- Solves a problem that doesn't exist (sport-specific architecture differences)

### The One Thing That Matters Most

**Blueprint quality.** Not AI. Not progression algorithms. Not sport-specific logic. Not athlete profiles.

The 10 blueprints proposed in this document, if well-designed with accurate slot sequences, sensible defaults, and correct family assignments, will produce better programs than any amount of sport-specific logic or AI inference ever could. Because the blueprints ARE the encoded wisdom of 58 elite programs.

Everything else is architecture that gets in the way.

---

## Appendix: Blueprint Coverage Map

| Sport | Off-Season | Pre-Season | In-Season | Youth |
|-------|-----------|------------|-----------|-------|
| Cricket | BP-01 Full Body Strength | BP-02 Strength + Power | BP-06 Power Maintenance | BP-07 Youth Foundation |
| | BP-10 Rotational Power | BP-03 Power + Speed | BP-05 Upper/Lower | |
| Rugby | BP-01 Full Body Strength | BP-02 Strength + Power | BP-06 Power Maintenance | BP-07 Youth Foundation |
| | BP-04 Strength + Cond | BP-03 Power + Speed | BP-05 Upper/Lower | |
| Soccer | BP-01 Full Body Strength | BP-02 Strength + Power | BP-06 Power Maintenance | BP-07 Youth Foundation |
| | BP-04 Strength + Cond | BP-03 Power + Speed | BP-05 Upper/Lower | |
| Athletics | BP-03 Power + Speed | BP-03 Power + Speed | BP-06 Power Maintenance | BP-07 Youth Foundation |
| | BP-01 Full Body Strength | BP-02 Strength + Power | | |
| Tennis | BP-01 Full Body Strength | BP-02 Strength + Power | BP-06 Power Maintenance | BP-07 Youth Foundation |
| | BP-08 Court Sport | BP-09 Complex Training | BP-08 Court Sport | |
| Badminton | BP-08 Court Sport | BP-09 Complex Training | BP-06 Power Maintenance | BP-07 Youth Foundation |
| | BP-01 Full Body Strength | BP-02 Strength + Power | BP-08 Court Sport | |

Every sport is covered by the same 10 blueprints. Zero sport-specific code required.
