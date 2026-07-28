# FORGE Blueprint V2

> 14 universal training blueprints with block annotations.
> Architecture frozen. No new entities. No new families.
> Backward compatible with V1 — blocks are annotations, not replacements.

---

## Block System

### Block Types

| Block | Purpose | Families | Rules |
|-------|---------|----------|-------|
| **Warmup** | Increase body temp, tissue prep | Acc/Prehab, Core (low-level) | diff ≤ L2, bodyweight/band only, no explosive, no strength sets |
| **Activation** | Low-level muscle recruitment before work | Acc/Prehab, Core | diff ≤ L2, no explosive, 8-12 reps, submaximal intensity |
| **Power** | Rate of force development, CNS preparation | Ball, Plyo, Rot | Always first work block. Must be fresh — preceded by Warmup only. Explosive=True required. Single exercises only (no superset). |
| **Strength** | Primary strength work | DLKD, DLHD, SLKD, SLHD, HPush, HPull, VPush, VPull, Rot, Carry | After Power/Conditioning. May be paired (superset A1/A2). 3-5 reps for primary, 6-12 for secondary. |
| **Accessory** | Supplementary, isolation, prehab | Acc/Prehab, Carry, Rot | After Strength. Higher reps (10-20). May include prehab. |
| **Core** | Trunk stabilization | Core | Always latest block. Never before Power or Strength. |
| **Conditioning** | Energy system development | Carry, Sprint/COD, Plyo (low-intensity) | After Strength, never before Power. Can be standalone or last block. |

### Universal Block Ordering Rules

```
1. Warmup → Activation → [Power] → [Conditioning] → Strength → Accessory → Core
2. Power is NEVER before Warmup or Activation
3. Core is ALWAYS last (after Accessory)
4. Conditioning is NEVER before Power
5. Activation is NEVER after Power
6. Blocks can be empty (optional) but ordering is preserved
```

### Block Annotation Format

```python
blocks = [
    ("warmup", ["Acc/Prehab"]),           # 2-4 Acc/Prehab exercises
    ("activation", ["Acc/Prehab", "Core"]), # 1-2 activation exercises
    ("power", ["Ball", "Plyo"]),           # explosive only
    ("strength", ["DLKD", "DLHD", "SLKD", "SLHD", "HPush", "HPull", "VPush", "VPull", "Rot", "Carry"]),
    ("accessory", ["Acc/Prehab", "Carry", "Rot"]),
    ("core", ["Core"]),
    ("conditioning", ["Carry", "Sprint/COD", "Plyo"]),
]
```

---

## Blueprint 1: Full Body Strength

| Field | V1 Value | V2 Change |
|-------|----------|-----------|
| **Purpose** | General strength accrual | Unchanged |
| **Typical Athlete** | Beginner-intermediate, off-season | Unchanged |
| **Frequency** | 3-4 sessions / week | Unchanged |
| **Session Structure** | 2-3 strength families + accessory finisher | **Block structure now explicit** |
| **Slot Order** | Ball → DLKD → HPush → DLHD/HPull → Core | Mapped to blocks below |

### Block Sequence

| # | Block | Mandatory | Families | Notes |
|---|-------|-----------|----------|-------|
| 1 | Warmup | ✅ | Acc/Prehab | 2-3 exercises, diff ≤ L2, bodyweight/band |
| 2 | Activation | Optional | Acc/Prehab, Core | 1-2 exercises, submax |
| 3 | Power | ✅ | Ball | 1 exercise, explosive=True, standalone (no superset) |
| 4 | Strength | ✅ | DLKD, HPush, DLHD/HPull | Slots 1-2: primary (lower rep). Slots 3+: secondary (paired) |
| 5 | Core | ✅ | Core | Last block. 1-2 exercises. |
| 6 | Conditioning | Optional | Carry, Sprint/COD | Finisher only when extra time available |

### Mandatory Blocks
Warmup, Power, Strength, Core

### Optional Blocks
Activation, Conditioning

### Block Ordering Rules
- Power before Strength (non-negotiable)
- Core after Strength (non-negotiable)
- Warmup before anything loaded (non-negotiable)
- Activation between Warmup and Power (when present)

---

## Blueprint 2: Strength + Power

| Field | V1 Value | V2 Change |
|-------|----------|-----------|
| **Purpose** | Hybrid strength-power development | Unchanged |
| **Typical Athlete** | Intermediate-advanced, field sport off-season | Unchanged |
| **Frequency** | 4-5 sessions / week | Unchanged |
| **Session Structure** | Explosive primer → heavy compound → lighter explosive → accessory | **Block structure now explicit** |

### Block Sequence

| # | Block | Mandatory | Families | Notes |
|---|-------|-----------|----------|-------|
| 1 | Warmup | ✅ | Acc/Prehab | 2-3 exercises, diff ≤ L2 |
| 2 | Activation | Optional | Acc/Prehab, Core | 1 exercise, submax |
| 3 | Power | ✅ | Ball | 1 exercise, explosive ONLY. Must be standalone — no superset. |
| 4 | Strength | ✅ | DLKD, HPush/HPull, DLHD | 3-4 exercises. May be paired (A1/A2 superset format). |
| 5 | Core | ✅ | Core | Last block. 1-2 exercises. |
| 6 | Conditioning | Optional | Sprint/COD, Carry | Only as finisher. Never displaces Strength volume. |

### Mandatory Blocks
Warmup, Power, Strength, Core

### Optional Blocks
Activation, Conditioning

### Block Ordering Rules
- Power standalone — never superset with ANY exercise
- Power before Strength — non-negotiable
- HPush/HPull paired as superset in Strength block
- Core absolute last

---

## Blueprint 3: Strength + Conditioning

| Field | V1 Value | V2 Change |
|-------|----------|-----------|
| **Purpose** | Strength maintenance + energy system development | Unchanged |
| **Typical Athlete** | Team sport, pre-season | Unchanged |
| **Frequency** | 3-4 sessions / week | Unchanged |
| **Session Structure** | Strength circuit → conditioning finisher | **Block structure now explicit** |

### Block Sequence

| # | Block | Mandatory | Families | Notes |
|---|-------|-----------|----------|-------|
| 1 | Warmup | ✅ | Acc/Prehab | Must include movement prep (A-skips, high knees) |
| 2 | Activation | Optional | Acc/Prehab, Core | Submax, pre-activation |
| 3 | Strength | ✅ | DLKD/DLHD, HPush, HPull | Circuit format (low rest, 60-90s between sets). 3 exercises. |
| 4 | Conditioning | ✅ | Sprint/COD, Carry, Plyo (low) | Must be after Strength. High-intensity intervals or strongman. |
| 5 | Core | ✅ | Core | Last block. 1-2 exercises. |
| 6 | Power | Optional | Ball, Plyo | Only if athlete can handle before Strength. Rare in this BP. |

### Mandatory Blocks
Warmup, Strength, Conditioning, Core

### Optional Blocks
Activation, Power

### Block Ordering Rules
- Conditioning after Strength (non-negotiable — the opposite would interfere with strength)
- Core after Conditioning (non-negotiable — core work is the hard stop)
- Power is optional but if included, goes BEAT THE CONDITIONING, not before Strength

Wait, that doesn't make sense. Let me re-think Power in this context. In a Strength + Conditioning blueprint, Power would go before Strength (since Power always before fatiguing work). But the whole point of this blueprint is that it's a conditioning-emphasis day. Let me leave Power as optional, only before Strength when included.

---

## Blueprint 4: Power + Speed

| Field | V1 Value | V2 Change |
|-------|----------|-----------|
| **Purpose** | Maximise rate of force development + velocity | Unchanged |
| **Typical Athlete** | Advanced field sport, track sprinters | Unchanged |
| **Frequency** | 3-4 sessions / week | Unchanged |
| **Session Structure** | Speed primer → plyometric/ballistic → light strength | **Block structure now explicit** |

### Block Sequence

| # | Block | Mandatory | Families | Notes |
|---|-------|-----------|----------|-------|
| 1 | Warmup | ✅ | Acc/Prehab | Dynamic stretching + movement prep. 5-10 min. |
| 2 | Activation | ✅ | Sprint/COD, Acc/Prehab | Sprint mechanics (A-skips, high knees). Low intensity. |
| 3 | Power | ✅ | Plyo, Ball | Explosive=True. Low volume (3-5 sets). Full recovery (3-5 min). |
| 4 | Strength | Optional | DLHD, HPush | Light strength (60-70% 1RM). Velocity-focused reps. |
| 5 | Core | ✅ | Core | 1-2 exercises. Low volume (maintenance only). |

### Mandatory Blocks
Warmup, Activation, Power, Core

### Optional Blocks
Strength

### Block Ordering Rules
- Sprint mechanics in Activation (not a conditioning block — technical only)
- Power before Strength — non-negotiable if Strength is present
- Core last — non-negotiable
- No Conditioning block — not the goal of this blueprint

---

## Blueprint 5: Upper / Lower Split

| Field | V1 Value | V2 Change |
|-------|----------|-----------|
| **Purpose** | Higher per-session volume per region | Unchanged |
| **Typical Athlete** | Bodybuilding, hypertrophy-focused, strength athletes | Unchanged |
| **Frequency** | 4 sessions / week | Unchanged |
| **Session Structure** | Compound → accessory → isolation | **Block structure now explicit** |

### Block Sequence — Lower Day

| # | Block | Mandatory | Families | Notes |
|---|-------|-----------|----------|-------|
| 1 | Warmup | ✅ | Acc/Prehab | Lower body focused (hip mobility, glute activation) |
| 2 | Activation | Optional | Acc/Prehab | Glute med, band lateral walks |
| 3 | Power | Optional | Plyo | Low volume (2-3 sets). Only if athletics phase. |
| 4 | Strength | ✅ | DLKD, DLHD, Carry | Primary: squat + hinge. Carry as finisher. |
| 5 | Core | ✅ | Core | Last block. 2-3 exercises. |

### Block Sequence — Upper Day

| # | Block | Mandatory | Families | Notes |
|---|-------|-----------|----------|-------|
| 1 | Warmup | ✅ | Acc/Prehab | Shoulder mobility (PVC pass-throughs, band dislocates) |
| 2 | Activation | ✅ | Acc/Prehab | Band pull-aparts, face pulls, scapular retractions |
| 3 | Strength | ✅ | VPush, HPush, VPull, HPull | Push/pull paired as supersets. Volume emphasis. |
| 4 | Accessory | ✅ | Acc/Prehab | Dumbbell Lateral Raise, Prone Raises |
| 5 | Core | ✅ | Core | Last block. | 

### Mandatory Blocks
Warmup (both days), Strength (both days), Core (both days)

### Optional Blocks
Power (lower day only), Activation (lower day), Accessory

### Block Ordering Rules
- Lower day: Power before Strength (optional), Core last
- Upper day: Activation before Strength (shoulder prep), Strength before Accessory, Core last
- Core on BOTH days (different emphasis: lower day = anti-extension, upper day = anti-rotation)

---

## Blueprint 6: Power Maintenance

| Field | V1 Value | V2 Change |
|-------|----------|-----------|
| **Purpose** | Retain power with minimal fatigue in-season | Unchanged |
| **Typical Athlete** | In-season team sport, competing court sport | Unchanged |
| **Frequency** | 1-2 sessions / week | Unchanged |
| **Session Structure** | Activation → one explosive → one plyometric → accessory | **Block structure now explicit** |

### Block Sequence

| # | Block | Mandatory | Families | Notes |
|---|-------|-----------|----------|-------|
| 1 | Warmup | ✅ | Acc/Prehab | Brief (5 min). Movement prep only. |
| 2 | Activation | Optional | Acc/Prehab, Core | Submax, low volume. |
| 3 | Power | ✅ | Ball, Plyo | 1-2 exercises. Explosive=True. 3-5 sets. Full recovery. |
| 4 | Accessory | Optional | Acc/Prehab, Core | Prehab focus. Rotator cuff, scapular control. |
| 5 | Core | ✅ | Core | 1 exercise. Maintenance only. |

### Mandatory Blocks
Warmup, Power, Core

### Optional Blocks
Activation, Accessory

### Block Ordering Rules
- Power first (non-negotiable — the purpose is power maintenance)
- Core last (non-negotiable)
- No Strength block — the blueprint is specifically about POWER maintenance
- Total session volume deliberately low

---

## Blueprint 7: Youth Foundation (U14-U20)

| Field | V1 Value | V2 Change |
|-------|----------|-----------|
| **Purpose** | Build movement literacy, general strength, athleticism | Unchanged |
| **Typical Athlete** | Adolescents (13-20), beginner training age | Unchanged |
| **Frequency** | 2-3 sessions / week | Unchanged |
| **Session Structure** | Warm-up → teach one pattern → circuit → game | **Block structure now explicit. Now extends to U20.** |

### Block Sequence

| # | Block | Mandatory | Families | Notes |
|---|-------|-----------|----------|-------|
| 1 | Warmup | ✅ | Sprint/COD, Acc/Prehab | Play-based. Coordination games, low-intensity COD. |
| 2 | Activation | ✅ | Acc/Prehab, Core | Movement skills. Teach one pattern per session. |
| 3 | Strength | ✅ | DLKD/DLHD, HPush, HPull | Circuit format (3-5 exercises, 8-12 reps). Teach technique. |
| 4 | Conditioning | Optional | Sprint/COD, Plyo | Games-based (tag, relay races). Not formal intervals. |
| 5 | Core | ✅ | Core | Planks, dead bugs, bird dogs. 2-3 exercises. |

### Mandatory Blocks
Warmup, Activation, Strength, Core

### Optional Blocks
Conditioning (play-based only)

### Block Ordering Rules
- One movement pattern taught per session (rotates weekly)
- No Power block — youth athletes use circuit-based strength for power foundation
- Strength is circuit (not heavy sets) — 8-12 reps, moderate load
- Core last — but youth-appropriate (fun finisher, not grind)

---

## Blueprint 8: Court Sport Athletic Development

| Field | V1 Value | V2 Change |
|-------|----------|-----------|
| **Purpose** | Multi-directional power, deceleration, COD, lateral strength | Unchanged |
| **Typical Athlete** | Tennis, badminton, basketball, volleyball, netball | Unchanged |
| **Frequency** | 3-4 sessions / week | Unchanged |
| **Session Structure** | COD primer → plyometric → strength (single-leg) → rotational → accessory | **Block structure now explicit** |

### Block Sequence

| # | Block | Mandatory | Families | Notes |
|---|-------|-----------|----------|-------|
| 1 | Warmup | ✅ | Acc/Prehab | Court-specific mobility (ankle, hip, shoulder) |
| 2 | Activation | ✅ | Sprint/COD, Acc/Prehab | Lateral movement prep. Low-intensity COD. |
| 3 | Power | ✅ | Plyo, Ball | Lateral + vertical plyos. Low volume. |
| 4 | Strength | ✅ | SLKD, HPull, Rot | Unilateral emphasis. Single-leg primary. Rotational accessory. |
| 5 | Core | ✅ | Core | Anti-rotation focus (court-specific). Last block. |
| 6 | Conditioning | Optional | Sprint/COD | Court-specific intervals (line drills, suicide runs) |

### Mandatory Blocks
Warmup, Activation, Power, Strength, Core

### Optional Blocks
Conditioning

### Block Ordering Rules
- COD in Activation (low-intensity technique, not conditioning)
- Power before Strength (non-negotiable)
- Rotational within Strength block (paired with SLKD as superset)
- Core last — anti-rotation emphasis matches court demands

---

## Blueprint 9: Rugby Off-Season

| Field | V1 Value | V2 Change |
|-------|----------|-----------|
| **Purpose** | Build collision-ready strength, power, mass | Unchanged |
| **Typical Athlete** | Rugby union/league, American football — off-season | Unchanged |
| **Frequency** | 4-5 sessions / week | Unchanged |
| **Session Structure** | Power primer → heavy compound → strongman → contact prep → conditioning | **Block structure now explicit** |

### Block Sequence

| # | Block | Mandatory | Families | Notes |
|---|-------|-----------|----------|-------|
| 1 | Warmup | ✅ | Acc/Prehab | Neck prep, shoulder mobility, hip mobility |
| 2 | Activation | ✅ | Acc/Prehab, Core | Neck isometrics, scapular activation, glute activation |
| 3 | Power | ✅ | Ball | Olympic lift or jump. Always standalone. |
| 4 | Strength | ✅ | DLKD, HPush, HPull, Carry | Heavy compound first (3-5 reps). Carry as strength finisher. |
| 5 | Core | ✅ | Core | Anti-extension + anti-rotation. 2-3 exercises. |
| 6 | Conditioning | ✅ | Sprint/COD, Carry | Sled pushes, sprints. Contact prep at the end. |

### Mandatory Blocks
Warmup, Activation, Power, Strength, Core, Conditioning

### Optional Blocks
None — this is the most comprehensive blueprint

### Block Ordering Rules
- Neck prep in Warmup (non-negotiable for contact sport)
- Power standalone (never paired — Olympic lifts)
- Carry in Strength block (not Accessory — it's primary for rugby)
- Conditioning after Core (optional per session, but when included, body is already fatigued — sport-specific)

---

## Blueprint 10: Sprint Development

| Field | V1 Value | V2 Change |
|-------|----------|-----------|
| **Purpose** | Max velocity and/or acceleration improvement | Unchanged |
| **Typical Athlete** | Track sprinters, field sport speed block | Unchanged |
| **Frequency** | 3-4 sessions / week (speed + strength) | Unchanged |
| **Session Structure** | Sprint session → plyometric → strength → accessory | **Block structure now explicit** |

### Block Sequence

| # | Block | Mandatory | Families | Notes |
|---|-------|-----------|----------|-------|
| 1 | Warmup | ✅ | Acc/Prehab | Sprint-specific warmup (drills, activation) |
| 2 | Activation | ✅ | Sprint/COD, Acc/Prehab | Sprint mechanics: A-skips, high knees, wall drills |
| 3 | Power | ✅ | Plyo, Ball | Low volume plyos. Reactive. |
| 4 | Strength | ✅ | DLHD, DLKD | Hip-dominant primary. Knee-dominant secondary (lighter). |
| 5 | Core | ✅ | Core | Low volume. Maintenance only. |

### Mandatory Blocks
Warmup, Activation, Power, Strength, Core

### Optional Blocks
None

### Block Ordering Rules
- Sprint mechanics in Activation (technical, submax)
- Power before Strength (non-negotiable — sprint athletes need fresh CNS)
- Hip-dominant before knee-dominant in Strength (sprint-specific priority)
- Core last but minimal — the focus is sprint + power

---

## Blueprint 11: Hypertrophy / Mass Accrual

| Field | V1 Value | V2 Change |
|-------|----------|-----------|
| **Purpose** | Maximise muscle cross-sectional area | Unchanged |
| **Typical Athlete** | Bodybuilding phase, underweight athlete | Unchanged |
| **Frequency** | 4-6 sessions / week (PPL / Upper-Lower) | Unchanged |
| **Session Structure** | Compound → isolation → pump | **Block structure now explicit** |

### Block Sequence

| # | Block | Mandatory | Families | Notes |
|---|-------|-----------|----------|-------|
| 1 | Warmup | ✅ | Acc/Prehab | Brief (5 min). General mobility. |
| 2 | Strength | ✅ | DLKD, DLHD, HPush, HPull | Compound first (3-5 sets, 8-12 reps). Shorter rest (60-90s). |
| 3 | Accessory | ✅ | VPush, VPull, Acc/Prehab, Rot | Isolation work. Higher reps (12-20). Volume emphasis. |
| 4 | Core | ✅ | Core | 2-3 exercises. 15-20 reps. Metabolic focus. |

### Mandatory Blocks
Warmup, Strength, Accessory, Core

### Optional Blocks
Activation, Conditioning

### Block Ordering Rules
- Compound before isolation (non-negotiable for hypertrophy)
- Higher volume across all blocks (15-20 sets per session)
- Shorter rest between Strength exercises (60-90s)
- Core last but done for volume/metabolic stress, not just stability
- No Power block — not the goal of hypertrophy

---

## Blueprint 12: Return to Sport (Foundation)

| Field | V1 Value | V2 Change |
|-------|----------|-----------|
| **Purpose** | Rebuild movement capacity post-injury | Unchanged |
| **Typical Athlete** | Post-rehab (cleared by PT), ACL/hamstring/shoulder return | Unchanged |
| **Frequency** | 3-4 sessions / week | Unchanged |
| **Session Structure** | Activation → movement patterning → low-load strength → proprioception → core | **Block structure now explicit** |

### Block Sequence

| # | Block | Mandatory | Families | Notes |
|---|-------|-----------|----------|-------|
| 1 | Warmup | ✅ | Acc/Prehab | Injury-specific prep. Pain-free movement only. |
| 2 | Activation | ✅ | Acc/Prehab, Core | Low-level neuromuscular re-education. |
| 3 | Strength (regressed) | ✅ | DLKD/DLHD, SLKD, Core | Regressed versions only (L1-L2). Pain-free. |
| 4 | Prehab | ✅ | Acc/Prehab, Core | Injury-specific: rotator cuff, VMO, hamstring eccentrics. |
| 5 | Core | ✅ | Core | Last block. Controlled only. No fatigue failure. |

### Mandatory Blocks
Warmup, Activation, Strength, Prehab, Core

### Optional Blocks
Conditioning (late-stage only), Sprint/COD (late-stage, low intensity)

### Block Ordering Rules
- All exercises diff ≤ L2 (regressed versions only)
- No explosive exercises (no Power block)
- Pain is the stop signal — no exercise performed through pain
- Core last but low-intensity (stability only, not strength)
- Progression: pain-free → load increase → complexity → sport-specific → full return

---

## Blueprint 13: Deload / Active Recovery

| Field | V1 Value | V2 Change |
|-------|----------|-----------|
| **Purpose** | Systemic recovery, movement practice, connective tissue health | Unchanged |
| **Typical Athlete** | Any athlete end of block, post-competition, high fatigue | Unchanged |
| **Frequency** | 2-3 sessions / week | Unchanged |
| **Session Structure** | Mobility → light circuit → prehab → stretch | **Block structure now explicit** |

### Block Sequence

| # | Block | Mandatory | Families | Notes |
|---|-------|-----------|----------|-------|
| 1 | Warmup | ✅ | Acc/Prehab, Core | Mobility emphasis. Foam rolling. Stretching. |
| 2 | Activation | Optional | Acc/Prehab | Light activation. Not for stimulus — for movement quality. |
| 3 | Strength (light) | Optional | DLKD/DLHD, HPush, HPull | 50-60% 1RM. 2-3 RIR. Not for stimulus. |
| 4 | Accessory | Optional | Acc/Prehab, Core | Prehab focus. Connective tissue health. |

### Mandatory Blocks
Warmup

### Optional Blocks
Activation, Strength, Accessory

### Block Ordering Rules
- This IS the regression — no block is mandatory except Warmup
- 50-60% load if Strength included
- No Power block (CNS must recover)
- No Conditioning block (systemic fatigue must drop)
- Duration: minimum 5-7 days, maximum 14 days

---

## Blueprint 14: Mixed Modal (GPP)

| Field | V1 Value | V2 Change |
|-------|----------|-----------|
| **Purpose** | Broad athletic capacity across all domains | Unchanged |
| **Typical Athlete** | Off-season multi-sport, beginner, tactical | Unchanged |
| **Frequency** | 4-5 sessions / week | Unchanged |
| **Session Structure** | Varied daily. Full body → cardio → strongman → accessory. | **Block structure now explicit** |

### Block Sequence (rotates daily — 3 example permutations)

#### Session A: Strength Emphasis
| # | Block | Mandatory | Families |
|---|-------|-----------|----------|
| 1 | Warmup | ✅ | Acc/Prehab |
| 2 | Power | Optional | Ball, Plyo |
| 3 | Strength | ✅ | DLKD, HPush, HPull, DLHD |
| 4 | Core | ✅ | Core |

#### Session B: Power Emphasis
| # | Block | Mandatory | Families |
|---|-------|-----------|----------|
| 1 | Warmup | ✅ | Acc/Prehab |
| 2 | Power | ✅ | Plyo, Ball |
| 3 | Strength | ✅ | DLKD (light), DLHD |
| 4 | Accessory | ✅ | Acc/Prehab, Rot |
| 5 | Core | ✅ | Core |

#### Session C: Conditioning Emphasis
| # | Block | Mandatory | Families |
|---|-------|-----------|----------|
| 1 | Warmup | ✅ | Sprint/COD, Acc/Prehab |
| 2 | Power | ✅ | Plyo |
| 3 | Strength | ✅ | DLKD, HPush, HPull |
| 4 | Conditioning | ✅ | Carry, Sprint/COD |
| 5 | Core | ✅ | Core |

### Universal Mandatory Blocks (across all permutations)
Warmup, Core

### Universal Optional Blocks (across all permutations)
Activation, Prehab

### Block Ordering Rules
- 3 session types rotate across the week (Strength, Power, Conditioning emphasis)
- All 15 families hit at least 1-2x per week across sessions
- Core always last within each session
- Power always before Strength within each session (when both present)

---

## V1 → V2 Migration Guide

### What changes
- Each blueprint gains a `blocks` field (list of block annotations)
- Block annotations map `slot_order` families to training blocks
- Blocks carry rendering hints (headings, pairing rules, block-specific filters)
- No slot_order changes — V1 slot_order maps directly into V2 blocks

### What stays the same
- All 14 blueprints preserved
- All family codes unchanged (15 families)
- All mandatory/optional lists unchanged
- `slot_order` still drives exercise selection
- Backward compatible — blueprints without `blocks` render as V1

### Recommended Implementation

```python
@dataclass
class Blueprint:
    name: str
    frequency: str
    slot_order: list          # unchanged from V1
    mandatory: list           # unchanged from V1
    optional: list            # unchanged from V1
    blocks: list = None       # NEW: list of (block_label, [families]) tuples
    notes: str = ""
```

When `blocks` is present:
1. Render block headings (WARM-UP, POWER, STRENGTH, etc.) in output
2. Apply block filters (Power: explosive only; Warmup: diff ≤ L2, bodyweight only)
3. No change to exercise selection logic
4. No change to substitution logic

When `blocks` is absent: render as V1 (backward compatible).
