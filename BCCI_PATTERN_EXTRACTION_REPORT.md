# BCCI Pattern Extraction Report

## Source
BCCI-ASCA Cricket-Specific S&C Program (ref.txt:9-36), Cricket 12-Week Pre-Season (ref.txt:37-70), Cricket Fielding-Specific S&C (ref.txt:71-97), plus 5 additional cricket programs (ref.txt:924-940). Validated against 58-program corpus (ref.txt:921-1112) and FORGE Blueprint Catalog V1.

---

## 1. Session Architecture

### BCCI-ASCA Gym Session (ref.txt:17-26)
```
Block Order      | Movement Slot
-----------------|----------------
Mobility         | Mobility
Activation       | Activation
Power            | Power
Primary Strength | Bilateral Strength
Secondary Strength | Unilateral Strength
Supplementary    | Accessory
Core             | Core
```

### Cricket Pre-Season (ref.txt:53-60)
```
Power Slot
Primary Strength (Bilateral)
Secondary Strength (Unilateral)
Horizontal Pull
Horizontal Push
Accessory
Core
```

### Cricket Fielding-Specific (ref.txt:81-89)
```
Mobility
Activation
COD Slot
Speed Slot
Power Slot
Unilateral Knee Slot
Horizontal Pull Slot
Core Slot
```

### Key Insight
BCCI follows the **universal session architecture** found across all 58 programs:
```
Mobility → Activation → Power → Primary Strength → Secondary Strength → Pull → Push → Accessory → Core
```

**FORGE already captures this** — the pattern matches Blueprint A (Power-First Gym Strength, ref.txt:701-714) at 67% frequency.

**Cricket-specific variation:** BCCI places Unilateral BEFORE Pull/Push. This differs from the generic pattern where Pull/Push can come before unilateral. The fielding blueprint puts COD and Speed BEFORE Power.

---

## 2. Movement Family Frequency — Cricket-Specific

| Family | Frequency (58-prog) | Cricket-Specific Note |
|--------|--------------------|----------------------|
| Core | 100% | Always last |
| Mobility | 95% | Always first |
| Bilateral Knee | 90% | Primary strength slot |
| Horizontal Pull | 90% | Supplementary, after unilateral |
| Activation | 85% | Between mobility and power |
| Power | 85% | Jump/ballistic, before fatigue |
| Horizontal Push | 80% | Supplementary, after pull |
| Bilateral Hip | 75% | Can replace or pair with DLKD |
| Unilateral Knee | 72% | Secondary strength in BCCI (higher than 58-prog avg of 70%) |
| Sprint/COD | 65% | Fielding-specific blueprint |
| Vertical Pull | 55% | Not in BCCI-ASCA gym session |
| Throw/Rotational | 45% | Higher in cricket (rotational power) |
| Carry | 30% | Not in BCCI-ASCA gym session |
| Unilateral Hip | 25% | Cricket fielding (single-leg RDL) |
| Vertical Push | 20% | Not in BCCI-ASCA gym session |

### FORGE Gap
**BCCI-ASCA gym session uses 7 slots:** Mobility, Activation, Power, Bilateral Strength, Unilateral Strength, Accessory, Core. It does NOT include HPush or HPull as dedicated slots — those are folded into "Accessory" or "Supplementary". This is a condensed blueprint (7 slots) vs FORGE's typical 8-9 slots.

**Cricket Pre-Season** adds HPush + HPull as explicit slots (8 total), matching FORGE's Blueprint A.

**Cricket Fielding** adds COD + Speed, removing bilateral strength in favor of unilateral knee.

**Conclusion:** BCCI uses 3 distinct blueprints depending on phase/emphasis, not 1. FORGE should ensure its catalog can express all three via slot reordering, not new blueprints.

---

## 3. Session Ordering Rules — Cricket-Specific

| Rule | Evidence |
|------|----------|
| **Power always first** | BCCI-ASCA (ref.txt:22): Power slot right after activation, before ANY strength work |
| **Bilateral before unilateral** | BCCI-ASCA (ref.txt:23-24): Primary Strength (Bilateral) → Secondary Strength (Unilateral) |
| **Unilateral before pulls/pushes** | BCCI-ASCA (ref.txt:24-25): Unilateral Strength → Accessory (which includes pulls/pushes) |
| **Core always last** | BCCI-ASCA (ref.txt:26): Core is always the final slot |
| **COD before power in fielding** | Cricket Fielding (ref.txt:84-86): COD → Speed → Power (unique to fielding) |
| **Pull before push** | Cricket Pre-Season (ref.txt:57-58): HPull → HPush |
| **Power before speed when both present** | Cricket Fielding (ref.txt:84-87): COD → Speed → Power (speed comes after power, but COD comes before — interestingly this differs from field sport norm) |

### FORGE Gap
None significant. FORGE's slot ordering (ref.txt:701-714) matches BCCI-ASCA: Mobility → Activation → Power → Bilateral → Unilateral → HPull → HPush → Core. The only difference is BCCI-ASCA groups HPull + HPush into "Accessory" rather than separate slots.

---

## 4. Progression Rules — Cricket-Specific

### BCCI Three-Year Progression (ref.txt:31)
```
Year 1: Beginner
Year 2: Intermediate
Year 3: Advanced
```

This tracks to FORGE's difficulty levels:
- Beginner → L1-L2 exercises across families
- Intermediate → L2-L3 exercises
- Advanced → L3-L5 exercises

### Cricket 12-Week Pre-Season (ref.txt:63-64)
```
2 x 6-week cycles with deload between
```

### Additional Cricket Programs (ref.txt:927-937)
| Program | Structure | Phase Progression |
|---------|-----------|-------------------|
| Nathan Kiely (16-wk pre-season) | Single block, eccentric/isometric focus | Strength durability for fast bowling |
| Damon Bednarski (12-wk pre-season) | 3 phases | Foundation → Strength & Power → Power & Speed |
| Cricfit Fast Bowling (12-wk) | 3 phases | Strength Endurance → Strength → Power |

### Universal 3-Phase Pattern (ref.txt:1082-1084, 1107-1108)
Found across BCCI-adjacent cricket, badminton, sprint, and general S&C programs:
```
Phase 1 (4-6 wks): Strength Endurance / Accumulation  — higher volume, moderate intensity
Phase 2 (4-6 wks): Pure Strength / Intensification      — lower volume, higher intensity
Phase 3 (4-6 wks): Speed & Power / Pre-Comp             — explosive focus, lighter loads
```

### FORGE Gap
**BCCI's 3-year progression (Beginner → Intermediate → Advanced) is a macro-progression not captured in FORGE.** FORGE currently operates at the micro-level (individual exercise difficulty within a blueprint). BCCI's 3-year path represents a macro-level advancement framework: increasing complexity of exercise selection, load tolerance, and session density (more families per session).

**The 3-phase periodization (Strength Endurance → Strength → Power) is not encoded in any FORGE blueprint.** It's a block-level progression that applies across multiple blueprints. This is the most significant uncover: FORGE has blueprints (what to do in a session) but not phases (how to progress over weeks).

---

## 5. Accessory Prehab Patterns — Cricket-Specific

From the 58-program analysis and cricket-specific research:

### Universal Cricket Accessories (appear in 70%+ of cricket programs)
| Exercise | Family | Purpose | BCCI Evidence |
|----------|--------|---------|--------------|
| Face Pull | Acc/Prehab | Shoulder health, external rotation | All overhead athletes |
| Copenhagen Plank | Core (adductor) | Groin injury prevention | Fast bowler-specific |
| Standing Calf Raise | Acc/Prehab | Ankle durability | Fielding, bowling |
| Single-Leg RDL | SLHD | Hamstring eccentric control | Bowler workload management |
| Band Pull-Apart | Acc/Prehab | Scapular control, posture | Universal activation |

### BCCI-Specific Accessories (from cricket fielding + fast bowling programs)
| Exercise | Purpose | Why Cricket |
|----------|---------|-------------|
| Single-Leg Box Squat | Unilateral knee stability | Lunging fielding position |
| Decel + Reaccel | COD braking + reacceleration | Fielding (stop → throw) |
| Med Ball Rotational Throw | Rotational power | Batting, bowling, throwing |
| Isometric Hamstring Hold | Hamstring injury prevention | Fast bowling workload |
| Prone Y/T/W Raise | Scapular control, shoulder health | Throwing athletes |

### FORGE Gap
**Most accessories above exist in FORGE's exercise database** (FORGE_COACHING_REFERENCE_DATABASE.md lines 384-410). The gap is not exercise availability — it's **prescription**: FORGE doesn't encode which accessories are mandatory for specific profiles (cricket bowler → Copenhagen, Med Ball throws). This belongs in blueprint-level "Mandatory Families" annotations, not a new system.

---

## 6. Testing Battery

BCCI-ASCA standardized testing (ref.txt:33-35):
- 10m sprint (acceleration)
- 20m sprint (max velocity)
- Standing long jump (lower body power)
- Yo-Yo intermittent recovery test (aerobic capacity)
- Bronco Test (aerobic capacity — rugby-inspired)

### FORGE Gap
**FORGE has no testing/tracking framework.** Tests are currently out of scope per earlier constraints, but they're foundational to BCCI's programming. If FORGE ever adds testing, these 5 tests form the minimum cricket battery.

---

## 7. Coaching Principles Unique to BCCI/Cricket

| Principle | Source | Implication for FORGE |
|-----------|--------|----------------------|
| **Standardized across all levels** (U-19 to senior) | BCCI-ASCA (ref.txt:29) | Same blueprint, different difficulty. FORGE already handles this via diff_min/diff_max. |
| **Rotational power is sport-specific** | Programs G (ref.txt:793-803) | Rotational family is higher priority in cricket. FORGE's diff_min/diff_max already allows this via sport profiles. |
| **Hanstring eccentric control is non-negotiable** | Nathan Kiely program (ref.txt:926-928) | SLHD family has elevated importance for bowlers. Not encoded in any current blueprint. |
| **Bronco Test for aerobic capacity** | BCCI-ASCA (ref.txt:35) | Conditioning modality unique to cricket. Not in FORGE scope. |
| **"Cricket has 3 distinct session types"** | Programs 1-3 (ref.txt:9-97) | Gym strength, pre-season full-body, fielding-specific. FORGE Blueprint A + Blueprint D + Blueprint G already cover these. |

---

## 8. Gap Analysis: What BCCI Does That FORGE Doesn't Capture

| Gap | SeverITY | Solution |
|-----|----------|----------|
| **3-phase periodization** (Strength Endurance → Strength → Power) | HIGH | Add as phase progression parameter to blueprints (shared across all blueprints, not new entity) |
| **3-year macro-progression** (Beginner → Intermediate → Advanced) | MEDIUM | Map to existing difficulty levels (L1-L2 → L2-L3 → L3-L5). This is already possible through diff_min/diff_max — just needs documentation. |
| **Cricket-specific accessory prescription** (for bowlers vs batters vs fielders) | MEDIUM | Document in blueprint "Mandatory Families" notes. Not a new entity. |
| **HPush + HPull folded into "Accessory" in condensed blueprints** | LOW | Already handled by FORGE's slot ordering — just make HPush/HPull optional in condensed variants. |
| **COD before Power in fielding sessions** | LOW | Court Sport blueprint (Blueprint D) already has COD → Power sequencing. Cricket fielding maps to this. |
| **Testing battery** | LOW | Out of scope per earlier constraints. Documented for future reference. |

### Summary: FORGE Covers ~75% of BCCI-ASCA Patterns

What's covered:
- Session architecture (Power-First, Bilateral → Unilateral, Core Last)
- Exercise families (all 15 families in BCCI's repertoire)
- Difficulty progression (L1-L5 maps to BCCI's 3-year arc)
- Push/Pull balance (Pull before Push)
- Power placement (always fresh)

What's not covered:
- Block-level periodization (Strength Endurance → Strength → Power)
- Phase progression attached to blueprints
- Profile-specific accessory prescription (bowler vs batter vs fielder)
- Testing battery
- Macro-level athlete journey (Beginner → Intermediate → Advanced as named phases)

### Recommendation
None of these gaps require new entities or architecture changes. The biggest gap — 3-phase periodization — can be solved by adding a `phase` parameter to blueprints (values: `accumulation`, `intensification`, `peaking`), which adjusts volume, intensity, and exercise selection within the existing blueprint structure. This is a data change, not an architecture change.
