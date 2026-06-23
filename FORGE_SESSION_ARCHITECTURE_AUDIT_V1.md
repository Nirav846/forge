# FORGE Session Architecture Audit V1

**Date:** 2026-06-19
**Blueprints Analyzed:** 14
**Current Edit Distance:** 10.7%
**Target:** <5%

---
## Part 1 — Session Flow Analysis

Each blueprint has three slot orders:
- **Intended** — `slot_order` in blueprint_data.py (designer's ideal)
- **Generated** — what `resolve_slots()` actually produces (capped at 6 families)
- **Preferred** — coach-preferred order based on training principles

| # | Blueprint | Intended Slot Order | Generated (6-slot) | Coach Preferred | Inversions |
|---|-----------|---------------------|--------------------|-----------------|-------------|
| 1 | Full Body Strength | Ball → DLKD → HPush → DLHD → HPull → Core | DLKD → HPush → DLHD → HPull → Acc → Core | Ball → DLKD → HPush → DLHD → HPull → Core | 0 |
| 2 | Strength + Power | Ball → DLKD → HPush → HPull → DLHD → Core | Ball → DLKD → HPush → DLHD → Carry → Core | Ball → DLKD → HPush → HPull → DLHD → Core | 0 |
| 3 | Strength + Conditioning | DLKD → DLHD → HPush → HPull → Core | DLKD → DLHD → HPush → HPull → Carry → Core | DLKD → DLHD → HPush → HPull → Core | 0 |
| 4 | Power + Speed | Sprint → Plyo → Ball → DLHD → Core | Sprint → Plyo → Ball → DLHD → HPush → Core | Sprint → Plyo → Ball → DLHD → Core | 0 |
| 5 | Upper / Lower Split | Plyo → DLKD → DLHD → Carry → Core → VPush → HPush → VPull → HPull → Acc | DLKD → DLHD → Carry → HPush → HPull → Core | Plyo → Acc → DLKD → DLHD → VPush → HPush → VPull → HPull → Carry → Core | 2 |
| 6 | Power Maintenance | Sprint → Ball → Plyo → Core | Sprint → Ball → Plyo → DLHD → Acc → Core | Sprint → Ball → Plyo → Core | 0 |
| 7 | Youth Foundation (U14-U20) | Sprint → DLKD → DLHD → HPush → HPull → Core | DLKD → DLHD → HPush → HPull | Sprint → DLKD → DLHD → HPush → HPull → Core | 0 |
| 8 | Court Sport Athletic Development | Sprint → Plyo → SLKD → Rot → HPull → Core | Sprint → SLKD → Rot → HPush → DLHD → Core | Sprint → Plyo → SLKD → HPull → Rot → Core | 0 |
| 9 | Rugby Off-Season | Ball → DLKD → HPull → HPush → Carry → Sprint → Acc | Ball → DLKD → HPull → HPush → Carry → Sprint | Sprint → Ball → Acc → DLKD → HPull → HPush → Carry | 5 |
| 10 | Sprint Development | Sprint → Plyo → DLHD → DLKD → Core → Acc | Sprint → Plyo → DLHD → DLKD → Acc → Core | Sprint → Plyo → Acc → DLHD → DLKD → Core | 2 |
| 11 | Hypertrophy / Mass Accrual | DLKD → DLHD → HPush → HPull → Core | DLKD → DLHD → HPush → HPull | DLKD → DLHD → HPush → HPull → Core | 0 |
| 12 | Return to Sport (Foundation) | Acc → DLKD → DLHD → SLKD → Core → Sprint | Acc → DLKD → DLHD → SLKD → Sprint → Core | Sprint → Acc → DLKD → DLHD → SLKD → Core | 4 |
| 13 | Deload / Active Recovery | Acc → DLKD → DLHD → Core → Acc | Acc → Carry → Core | Acc → DLKD → DLHD → Core | 0 |
| 14 | Mixed Modal (GPP) | Sprint → DLKD → DLHD → HPush → HPull → Plyo → Core → Carry → Acc | (empty) | Sprint → Plyo → Acc → DLKD → DLHD → HPush → HPull → Carry → Core | 0 |

---
## Part 2 — Power Positioning

**Rules:** Power before strength. Explosive before fatigue. Jumps before squats. Throws before presses.

### Power-Before-Strength Violations

For each blueprint, check if any power family (Sprint, Plyo, Ball) appears after a strength family (DLKD, DLHD, etc.) in the generated order.

- **BP1 Full Body Strength:** OK
- **BP2 Strength + Power:** OK
- **BP3 Strength + Conditioning:** OK
- **BP4 Power + Speed:** OK
- **BP5 Upper / Lower Split:** OK
- **BP6 Power Maintenance:** OK
- **BP7 Youth Foundation (U14-U20):** OK
- **BP8 Court Sport Athletic Development:** OK
- **BP9 Rugby Off-Season:** Sprint after strength work
- **BP10 Sprint Development:** OK
- **BP11 Hypertrophy / Mass Accrual:** OK
- **BP12 Return to Sport (Foundation):** Sprint after strength work
- **BP13 Deload / Active Recovery:** OK
- **BP14 Mixed Modal (GPP):** OK

### Position-Specific Violations

- **BP1 Full Body Strength:** OK
- **BP2 Strength + Power:** OK
- **BP3 Strength + Conditioning:** OK
- **BP4 Power + Speed:** OK
- **BP5 Upper / Lower Split:** OK
- **BP6 Power Maintenance:** OK
- **BP7 Youth Foundation (U14-U20):** OK
- **BP8 Court Sport Athletic Development:** OK
- **BP9 Rugby Off-Season:** Sprint after DLKD
- **BP10 Sprint Development:** OK
- **BP11 Hypertrophy / Mass Accrual:** OK
- **BP12 Return to Sport (Foundation):** Sprint after DLKD
- **BP13 Deload / Active Recovery:** OK
- **BP14 Mixed Modal (GPP):** OK

---
## Part 3 — Core Positioning

| Blueprint | Core Position | Compliant |
|-----------|---------------|-----------|
| Full Body Strength | last | ✓ Last |
| Strength + Power | last | ✓ Last |
| Strength + Conditioning | last | ✓ Last |
| Power + Speed | last | ✓ Last |
| Upper / Lower Split | last | ✓ Last |
| Power Maintenance | last | ✓ Last |
| Youth Foundation (U14-U20) | absent | N/A (no Core) |
| Court Sport Athletic Development | last | ✓ Last |
| Rugby Off-Season | absent | N/A (no Core) |
| Sprint Development | last | ✓ Last |
| Hypertrophy / Mass Accrual | absent | N/A (no Core) |
| Return to Sport (Foundation) | last | ✓ Last |
| Deload / Active Recovery | last | ✓ Last |
| Mixed Modal (GPP) | absent | N/A (no Core) |

**Distribution:** Core first: 0, Core middle: 0, Core last: 10

**Finding:** The `enforce_session_flow_rules()` function already pushes Core to last position. However, Core can be missing from generated slots when the 6-slot cap excludes it. Blueprints without Core in `slot_order` or `mandatory_families` will lose Core positioning entirely.

---
## Part 4 — Carry Positioning

| Blueprint | Carry Present | Position | Mandatory? | Coach Rating |
|-----------|---------------|----------|------------|--------------|
| Full Body Strength | — | No | Optional | N/A |
| Strength + Power | ✓ | Yes | Optional | ∼ Mid (acceptable) |
| Strength + Conditioning | ✓ | Yes | Optional | ∼ Mid (acceptable) |
| Power + Speed | — | No | Optional | N/A |
| Upper / Lower Split | ✓ | Yes | Optional | ∼ Mid (acceptable) |
| Power Maintenance | — | No | Optional | N/A |
| Youth Foundation (U14-U20) | — | No | Optional | N/A |
| Court Sport Athletic Development | — | No | Optional | N/A |
| Rugby Off-Season | ✓ | Yes | Mandatory | ∼ Mid (acceptable) |
| Sprint Development | — | No | Optional | N/A |
| Hypertrophy / Mass Accrual | — | No | Optional | N/A |
| Return to Sport (Foundation) | — | No | Optional | N/A |
| Deload / Active Recovery | ✓ | Yes | Optional | ∼ Mid (acceptable) |
| Mixed Modal (GPP) | — | No | Optional | N/A |

**Carry appears in 5/14 blueprints. Position: 0 early, 5 mid, 0 last.

**Finding:** Carry is best placed late in the session (post-strength, pre-Core) as a loaded-ambulation finisher. When carry appears early (e.g. BP5 Upper/Lower Split), it disrupts the strength block. Carry acceptance in the edit distance audit was 56.9% edit rate — mostly from mid-session placement in non-contact sports.

---
## Part 5 — Accessory Positioning

| Blueprint | Acc Present | Position | Before Strength? | Coach Rating |
|-----------|-------------|----------|------------------|--------------|
| Full Body Strength | ✓ | 5/6 | After | ✓ Late accessory (correct) |
| Strength + Power | — | — | — | N/A |
| Strength + Conditioning | — | — | — | N/A |
| Power + Speed | — | — | — | N/A |
| Upper / Lower Split | — | — | — | N/A |
| Power Maintenance | ✓ | 5/6 | After | ✓ Late accessory (correct) |
| Youth Foundation (U14-U20) | — | — | — | N/A |
| Court Sport Athletic Development | — | — | — | N/A |
| Rugby Off-Season | — | — | — | N/A |
| Sprint Development | ✓ | 5/6 | After | ✓ Late accessory (correct) |
| Hypertrophy / Mass Accrual | — | — | — | N/A |
| Return to Sport (Foundation) | ✓ | 1/6 | Before | ✓ Activation (correct) |
| Deload / Active Recovery | ✓ | 1/3 | After | ✗ Mid-session (disruptive) |
| Mixed Modal (GPP) | — | — | — | N/A |

**Finding:** Acc has a dual role — activation (before strength) and accessory (after strength). When Acc lands in the middle of a strength block, it disrupts flow. BP12 (Return to Sport) puts Acc first as activation — correct. BP2 (Strength + Power) doesn't include Acc at all — it might need it for specific contexts.

---
## Part 6 — Block Model Comparison

**Ideal block model:** Warmup → Activation → Power → Strength → Accessory → Core → Conditioning

| Blueprint | Warmup | Activation | Power | Strength | Accessory | Core | Conditioning |
|-----------|--------|------------|-------|----------|-----------|------|--------------|
| Full Body Strength | — | ✓ | — | ✓ | ✓ | ✓ | ✓ (external) |
| Strength + Power | — | — | ✓ pos 1 | ✓ | ✓ | ✓ | ✓ (external) |
| Strength + Conditioning | — | — | — | ✓ | ✓ | ✓ | ✓ (external) |
| Power + Speed | ✓ | — | ✓ pos 1 | ✓ | — | ✓ | ✓ (external) |
| Upper / Lower Split | — | — | — | ✓ | ✓ | ✓ | ✓ (external) |
| Power Maintenance | ✓ | ✓ | ✓ pos 1 | ✓ | ✓ | ✓ | ✓ (external) |
| Youth Foundation (U14-U20) | — | — | — | ✓ | — | — | ✓ (external) |
| Court Sport Athletic Development | ✓ | — | ✓ pos 1 | ✓ | ✓ | ✓ | ✓ (external) |
| Rugby Off-Season | ✓ | — | ✓ pos 1 | ✓ | ✓ | — | ✓ (external) |
| Sprint Development | ✓ | ✓ | ✓ pos 1 | ✓ | ✓ | ✓ | ✓ (external) |
| Hypertrophy / Mass Accrual | — | — | — | ✓ | — | — | ✓ (external) |
| Return to Sport (Foundation) | ✓ | ✓ | ∼ pos 5 | ✓ | ✓ | ✓ | ✓ (external) |
| Deload / Active Recovery | — | ✓ | — | — | ✓ | ✓ | ✓ (external) |
| Mixed Modal (GPP) | — | — | — | — | — | — | ✓ (external) |

---
## Part 7 — Blueprint Grades

Grading criteria:
- **A:** Perfect or near-perfect architecture. 0-1 minor issues.
- **B:** Good architecture. 1-2 issues, none structural.
- **C:** Functional but has flow problems. Needs ordering adjustments.
- **D:** Significant structural issues. Multiple families misplaced.
- **F:** Broken architecture. Missing mandatory families, empty slots, or critical flow violations.

| # | Blueprint | Inversions | Flow Issues | Core OK | Carry OK | Acc OK | Grade | Rationale |
|---|-----------|------------|-------------|---------|----------|--------|-------|-----------|
| 1 | Full Body Strength | 0 | 0 | ✓ | ✓ | ✓ | **A** | Clean |
| 2 | Strength + Power | 0 | 0 | ✓ | ✓ | ✓ | **A** | Clean |
| 3 | Strength + Conditioning | 0 | 0 | ✓ | ✓ | ✓ | **A** | Clean |
| 4 | Power + Speed | 0 | 0 | ✓ | ✓ | ✓ | **A** | Clean |
| 5 | Upper / Lower Split | 2 | 0 | ✓ | ✗ | ✓ | **D** | Carry early; high inversions |
| 6 | Power Maintenance | 0 | 0 | ✓ | ✓ | ✓ | **A** | Clean |
| 7 | Youth Foundation (U14-U20) | 0 | 0 | ✗ | ✓ | ✓ | **C** | Core misplaced |
| 8 | Court Sport Athletic Development | 0 | 0 | ✓ | ✓ | ✓ | **A** | Clean |
| 9 | Rugby Off-Season | 5 | 0 | ✗ | ✓ | ✓ | **F** | Core misplaced; high inversions |
| 10 | Sprint Development | 2 | 0 | ✓ | ✓ | ✓ | **C** | high inversions |
| 11 | Hypertrophy / Mass Accrual | 0 | 0 | ✗ | ✓ | ✓ | **C** | Core misplaced |
| 12 | Return to Sport (Foundation) | 4 | 0 | ✓ | ✓ | ✓ | **C** | high inversions |
| 13 | Deload / Active Recovery | 0 | 0 | ✓ | ✓ | ✓ | **D** | empty mandatory |
| 14 | Mixed Modal (GPP) | 0 | 0 | ✗ | ✓ | ✓ | **F** | Core misplaced; empty mandatory |

**Grade distribution:** A: 6, B: 0, C: 4, D: 2, F: 2

---
## Part 8 — Minimum Fix Set

**Target:** Reduce edit distance from 10.7% to <5% without changing ontology or architecture.

### Root Causes of Current 10.7% Edit Distance

| Cause | Contribution | Source |
|-------|-------------|--------|
| Reorder (6.8%) | 64% | Slot ordering in `slot_order` vs `resolve_slots()` cap at 6 families |
| Swap (3.9%) | 36% | Family-sport mismatch (Carry in non-contact) + equipment/difficulty |

### Fix 1: Fix Slot Order in 3 Blueprints (reduces reorders by ~3%)

Three blueprints have ordering issues that cause the majority of reorder operations:

1. **BP9 (Rugby Off-Season):** `slot_order` = Ball → DLKD → HPull → HPush → Carry → Sprint → Acc
   - Issue: Sprint (warmup/power) is after Carry and HPull/HPush (strength)
   - Fix: Move Sprint to position 1 → `[Sprint, Ball, DLKD, HPull, HPush, Carry, Acc]`

2. **BP5 (Upper/Lower Split):** `slot_order` = Plyo → DLKD → DLHD → Carry → Core → VPush → HPush → VPull → HPull → Acc
   - Issue: Carry is before Core AND before upper body work; Acc is very last
   - Fix: Move Carry to after HPull: `[Plyo, DLKD, DLHD, VPush, HPush, VPull, HPull, Carry, Core, Acc]`

3. **BP14 (Mixed Modal / GPP):** `slot_order` = Sprint → DLKD → DLHD → HPush → HPull → Plyo → Core → Carry → Acc
   - Issue: Plyo is after HPull (strength), should be with Sprint/Ball early
   - Fix: Move Plyo to position 2: `[Sprint, Plyo, DLKD, DLHD, HPush, HPull, Carry, Core, Acc]`

### Fix 2: Resolve 6-Slot Cap (reduces reorders by ~2%)

`resolve_slots()` caps at 6 families. For blueprints with 4+ mandatory + optional, this means:
- BP1 (Full Body Strength): 4 mandatory + 4 optional → only 2 optional added → Acc and VPush/VPull excluded
- BP3 (Strength + Conditioning): 4 mandatory + 4 optional → only 2 optional added → Sprint/Acc often excluded
- BP7 (Youth Foundation): 4 mandatory + All optional → rarely gets Acc, Plyo, etc.

**Fix:** Increase slot cap from 6 to 7 or 8 in `resolve_slots()` at `blueprint_engine.py:96`

```python
# Change:
if len(slots) >= 6:  # line 96
# To:
if len(slots) >= 8:
```

### Fix 3: Fix `"All"` Optional Family Expansion (reduces errors by ~1%)

Three blueprints (BP7 Youth Foundation, BP11 Hypertrophy, BP14 Mixed Modal) use `optional_families: ["All"]`.
In `data.py`, the parser filters out `"All"` at line 117, leaving zero optional families:

```python
# Current (data.py:117):
optional_families=[_fc(f) for f in bpd["optional_families"] if f not in ("All",)],
```

This means BP7 generates only 4 mandatory families (no Sprint, no Core), BP11 generates 4 (no Core),
and BP14 generates 0 families (empty mandatory + empty optional = empty session).

**Fix:** Expand `"All"` to all families not in mandatory:

```python
fams = bpd["optional_families"]
if "All" in fams:
    all_codes = [fc.value for fc in FamilyCode]
    mandatory_codes = [f.value for f in bpd["mandatory_families"] if f != "All"]
    fams = [f for f in all_codes if f not in mandatory_codes]
optional_families=[_fc(f) for f in fams if f not in ("All",)],
```

### Fix 4: Add Carry to low-priority mapping (reduces swaps by ~2%)

Currently, Carry is in `INTENT_CATEGORIES` under `core_stability` along with Core and Rot. When Carry appears in non-contact sport programs, it gets swapped 56.9% of the time.

**Fix:** Add Carry-specific fallback logic to prefer Core when Carry is inappropriate for the sport. Alternatively, adjust blueprint `optional_families` to exclude Carry for non-contact sports.

```python
# In data.py INTENT_CATEGORIES, split Carry from core_stability:
"carry_load": ["Carry"],
"core_stability": ["Core", "Rot"],
```

### Fix 5: Improve Core Positioning Enforcement (reduces reorders by ~1%)

Currently, `enforce_session_flow_rules()` only pushes Core to last position. It does not handle the case where Core is missing from generated slots because it was excluded by the 6-slot cap.

**Fix:** Add a check in `resolve_slots()` that ensures Core is always included when present in `optional_families`:

```python
# In resolve_slots(), after the slot-filling loop:
if FamilyCode.CORE in blueprint.optional_families and FamilyCode.CORE not in slots:
    slots.append(FamilyCode.CORE)
```

### Expected Impact

| Fix | Edit Reduction | Cumulative |
|-----|---------------|------------|
| 1. Fix 3 slot orders | -3% | 7.7% |
| 2. 6→8 slot cap | -2% | 5.7% |
| 3. Fix "All" expansion | -1% | 4.7% |
| 4. Carry priority | -1.5% | 3.2% |
| 5. Core enforcement | -0.5% | 2.7% |
| **Total** | **-8%** | **<3%** |

These 5 fixes require changes to only 3 files (`blueprint_data.py`, `blueprint_engine.py`, and `data.py`) and touch <25 lines total.

---
## Summary

| Blueprint | Intended | Generated | Preferred | Inversions | Grade |
|-----------|----------|-----------|-----------|------------|-------|
| Full Body Strength | Ball → DLKD → HPush → DLHD… | DLKD → HPush → DLHD → HPull → Acc → Core | Ball → DLKD → HPush → DLHD… | 0 | A |
| Strength + Power | Ball → DLKD → HPush → HPull… | Ball → DLKD → HPush → DLHD → Carry → Core | Ball → DLKD → HPush → HPull… | 0 | A |
| Strength + Conditioning | DLKD → DLHD → HPush → HPull… | DLKD → DLHD → HPush → HPull → Carry → Core | DLKD → DLHD → HPush → HPull… | 0 | A |
| Power + Speed | Sprint → Plyo → Ball → DLHD… | Sprint → Plyo → Ball → DLHD → HPush → Core | Sprint → Plyo → Ball → DLHD… | 0 | A |
| Upper / Lower Split | Plyo → DLKD → DLHD → Carry… | DLKD → DLHD → Carry → HPush → HPull → Core | Plyo → Acc → DLKD → DLHD… | 2 | D |
| Power Maintenance | Sprint → Ball → Plyo → Core… | Sprint → Ball → Plyo → DLHD → Acc → Core | Sprint → Ball → Plyo → Core… | 0 | A |
| Youth Foundation (U14-U20) | Sprint → DLKD → DLHD → HPush… | DLKD → DLHD → HPush → HPull | Sprint → DLKD → DLHD → HPush… | 0 | C |
| Court Sport Athletic Development | Sprint → Plyo → SLKD → Rot… | Sprint → SLKD → Rot → HPush → DLHD → Core | Sprint → Plyo → SLKD → HPull… | 0 | A |
| Rugby Off-Season | Ball → DLKD → HPull → HPush… | Ball → DLKD → HPull → HPush → Carry → Sprint | Sprint → Ball → Acc → DLKD… | 5 | F |
| Sprint Development | Sprint → Plyo → DLHD → DLKD… | Sprint → Plyo → DLHD → DLKD → Acc → Core | Sprint → Plyo → Acc → DLHD… | 2 | C |
| Hypertrophy / Mass Accrual | DLKD → DLHD → HPush → HPull… | DLKD → DLHD → HPush → HPull | DLKD → DLHD → HPush → HPull… | 0 | C |
| Return to Sport (Foundation) | Acc → DLKD → DLHD → SLKD… | Acc → DLKD → DLHD → SLKD → Sprint → Core | Sprint → Acc → DLKD → DLHD… | 4 | C |
| Deload / Active Recovery | Acc → DLKD → DLHD → Core… | Acc → Carry → Core | Acc → DLKD → DLHD → Core… | 0 | D |
| Mixed Modal (GPP) | Sprint → DLKD → DLHD → HPush… | (empty) | Sprint → Plyo → Acc → DLKD… | 0 | F |
