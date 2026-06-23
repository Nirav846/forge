# FORGE Session Assembly Rulebook V1.0

## Overview

This rulebook defines how FORGE assembles a single coherent session from a blueprint's family slots, ensuring that:
1. The blueprint identity is preserved under constraints
2. The session order follows real S&C flow
3. Repeated family exposures within a week progress intentionally
4. Constraints (time, competition, injury, role) are resolved deterministically

## Tier 1: Family Survival Tiers

### Tier S — Session Identity (Must Preserve)

These families define what the blueprint IS. They survive all constraints except absolute emergency.

| Family | When Tier S |
|--------|-------------|
| Blueprint `mandatory_families` | Always Tier S |
| Core | Always Tier S (structurally expected in 100% of programs) |

**Exception:** If a mandatory family has absolutely no valid exercise (all exercises filtered by injury + equipment + competition), the family may be substituted with same-intent family. If substitution fails, the family is dropped with a warning.

### Tier A — High-Value Support (Drop Only Under Severe Pressure)

| Family | Role | When Tier A |
|--------|------|-------------|
| DLKD | Lower push, bilateral | Always Tier A for strength blueprints |
| DLHD | Lower pull, bilateral | Always Tier A for strength blueprints |
| HPush | Upper push, horizontal | Always Tier A for strength blueprints |
| HPull | Upper pull, horizontal | Always Tier A for strength blueprints |
| Sprint | Speed/acceleration | Tier A for speed/power/sprint blueprints |
| Plyo | Elastic power | Tier A for power/sprint blueprints |
| Ball | Loaded explosive | Tier A for power/sprint blueprints |
| Landing | Landing mechanics | Tier A for speed/power blueprints |

### Tier B — Optional Support (Droppable Under Time/Competition Pressure)

| Family | When Tier B |
|--------|-------------|
| SLKD | Unilateral lower push |
| SLHD | Unilateral lower pull |
| VPush | Vertical push (overhead) |
| VPull | Vertical pull |
| Rot | Rotational / anti-rotation |

### Tier C — First Drop (Drop Under Any Compression)

| Family | When Tier C |
|--------|-------------|
| Carry | Loaded carries |
| Acc | Accessory / prehab |

**Role de-priority override:** If a role profile explicitly de-prioritizes a family, that family drops one tier (e.g., Tier A → Tier B, Tier B → Tier C). If already Tier C, it becomes the first drop.

## Tier 2: Session Flow Ordering

After family survival is determined, rebuild the session order to follow this flow:

### Phase 1: Neural / Speed / Power Prep (First)
- Sprint, Plyo, Ball, Landing, Acc
- These are low-volume, high-neural. They should NOT be done after heavy fatigue.

### Phase 2: Primary Strength (Early-Mid)
- DLKD, DLHD, HPush, HPull
- These are the main session work. Done after neural prep but before secondary work.

### Phase 3: Secondary Strength (Mid-Late)
- SLKD, SLHD, VPush, VPull, Rot
- These support the primary work but are lower priority for time.

### Phase 4: Accessory / Trunk / Carry (Last)
- Core, Carry
- These are the finishers. Core is always last.

### Ordering Rules
1. Within a phase, maintain the blueprint's slot_order if possible
2. If a phase is empty, skip it (don't force filler)
3. Core is always moved to the end of the session, even if the blueprint places it elsewhere
4. Conditioning is appended after all exercise blocks (unless blueprint explicitly says otherwise)

## Tier 3: Time Constraint Resolution

### Step 1: Determine maximum families
```
available_minutes < 30  → max 4 families
available_minutes < 45  → max 5 families
available_minutes < 60  → max 7 families
available_minutes >= 60 → max 8 families
```

### Step 2: Competition proximity reduction
```
comp_window = 4 (moderate) → max = min(max, 7)
comp_window = 2 (light)    → max = min(max, 5)
comp_window = 1 (primer)   → max = min(max, 4)
```

### Step 3: Drop families from lowest tier first
1. Start with all slots (mandatory + optional)
2. If count > max, drop from Tier C first (respecting role de-priority)
3. If still > max, drop from Tier B
4. If still > max, drop from Tier A (only under severe pressure)
5. Never drop Tier S unless absolutely necessary (substitution failed)

### Step 4: After drops, rebuild session order using Tier 2 flow rules

## Tier 4: Competition Taper Drop Logic

When `comp_window <= 2` (light/primer), additional rules apply:

### Light taper (2-3 days to match)
- Keep: Sprint, Plyo, Ball (low volume, primer-quality)
- Drop: Carry, Acc (accessory work)
- Reduce: DLKD, DLHD (reduce to primer / technique work, not heavy)
- Keep: Core (activation)

### Primer (<=1 day to match)
- Keep: Sprint, Plyo, Ball (very low volume, activation)
- Drop: DLKD, DLHD, Carry, Acc, SLKD, SLHD, VPush, VPull, Rot
- Keep: Core (light activation)
- Max 4 families total

**Important:** The blueprint's mandatory families are still respected. If a strength blueprint mandates DLKD, it stays but gets reduced to technique/activation intensity.

## Tier 5: Within-Week Family Continuity

If a family appears in multiple sessions within the same week, the second (and third) appearance should be a purposeful variation:

### Strength families (DLKD, DLHD, HPush, HPull, VPush, VPull)
- **First exposure:** Primary bilateral, full prescription
- **Second exposure:** Unilateral variant (SLKD/SLHD), reduced volume, or different angle
- **Third exposure:** Technique/quality, or same as first if only 2 exposures

### Speed families (Sprint, Plyo, Ball)
- **First exposure:** Acceleration / low-complexity / bilateral
- **Second exposure:** Max velocity / reactive / mechanics-focused / reduced volume
- **Third exposure:** Quality / low-volume / primer

### Landing families (Landing)
- **First exposure:** Stick / teach / double-leg
- **Second exposure:** Single-leg / reactive / decel
- **Third exposure:** Sport-contextual / reduced volume

### Rotational (Rot)
- **First exposure:** Anti-rotation / controlled
- **Second exposure:** Rotational power / speed

### Implementation
- Track which family has appeared in which session of the week
- For the second appearance, if the family is a strength/speed/landing/rot family, bias toward a different exercise variant:
  - If first was bilateral, second should be unilateral (if available)
  - If first was low-difficulty, second should be moderate-difficulty (if mastery allows)
  - If first was heavy, second should be reduced-fatigue / quality
- If no suitable variation exists, fall back to same exercise with reduced volume (handled by prescription rules)

## Tier 6: Session Re-Balance After Filtering

If exercise selection returns None for a family (injury, equipment, competition filtering):

### Step 1: Try same-family substitution
```
substitute_exercise(family, ...) → if valid exercise found, use it
```

### Step 2: Try same-intent substitution
```
If family is DLKD → try SLKD
If family is DLHD → try SLHD
If family is Sprint → try Plyo or Ball
If family is Plyo → try Ball or Sprint
etc.
```

### Step 3: If both fail, drop the family cleanly
1. Remove the empty block from the session
2. Reorder the remaining blocks using session flow rules
3. Add a note to the session adjustment_note: "{family} dropped — no valid exercise under current constraints"

### Step 4: Re-check session coherence
- If session now has fewer than 3 families, try to add a backfill family from the blueprint's optional list that was previously dropped
- If still < 3, mark session as "light session" with reduced volume

## Tier 7: Conflict Resolution Priority

When multiple rules push in different directions, resolve in this order:

1. **Blueprint identity** (mandatory families must survive)
2. **Injury/risk** (unsafe exercises must be filtered)
3. **Competition taper** (drop fatigue-heavy extras)
4. **Time constraint** (drop from lowest tier first)
5. **Role bias** (reorder surviving families, drop de-prioritized if needed)
6. **Session flow** (reorder to follow S&C flow)
7. **Within-week continuity** (vary second exposure)

Lower-priority rules can modify the output of higher-priority rules but cannot override them.

## Tier 8: Coach-Visible Output

Every session should include:
- Session composition rationale (what was dropped and why)
- Any substitutions made (e.g., "Sprint dropped → Plyo substituted")
- Within-week continuity notes (e.g., "Second DLKD exposure → unilateral variation")

These notes are added to `adjustment_note` or `personalization_notes`.
