# RC1 — Substitution Difficulty Filter Fix

## Root Cause

`substitute()` bypassed athlete difficulty constraints in two places:

1. **Pool filter** (`forge_prototype.py:462`):
   ```python
   pool = [e for e in exercises if e.family == family and e.equip_ok(equip_level)]
   ```
   No difficulty check. Any family member at any L1-L5 was eligible regardless of
   athlete level.

2. **Cross-family fallback** (`forge_prototype.py:469`):
   ```python
   return select_exercise(exercises, alt, 1, 5, equip_level, used_names)
   ```
   Hardcoded `1, 5` passed instead of the athlete's actual difficulty range.

3. **Call site** (`forge_prototype.py:526`):
   ```python
   ex = substitute(exercises, fam, 1, 5, equip_level, used_names)
   ```
   Same hardcoded `1, 5` — the week-adjusted difficulty was never forwarded.

**Effect:** 2,851 out-of-range selections (17.5% of all slots). Beginners got L5
exercises. Advanced athletes got L1 warmups billed as main work.

---

## Code Changes

### 1. `substitute()` pool filter — add difficulty check

```python
# Before:
pool = [e for e in exercises if e.family == family and e.equip_ok(equip_level)]

# After:
pool = [e for e in exercises if e.family == family
        and e.difficulty >= diff_min and e.difficulty <= diff_max
        and e.equip_ok(equip_level)]
```

### 2. Cross-family fallback — pass real difficulty

```python
# Before:
return select_exercise(exercises, alt, 1, 5, equip_level, used_names)

# After:
return select_exercise(exercises, alt, diff_min, diff_max, equip_level, used_names)
```

### 3. Call site — pass week-adjusted difficulty

```python
# Before:
ex = substitute(exercises, fam, 1, 5, equip_level, used_names)

# After:
ex = substitute(exercises, fam, w_diff_min, w_diff_max, equip_level, used_names)
```

**Total: 3 lines changed, zero new code.**

---

## Substitution Path Verification

| Path | Before | After |
|------|--------|-------|
| Same family, same difficulty | N/A (select_exercise handles first) | Same — unchanged |
| Same family, any difficulty | ✓ — but also returns L5 for beginners | ✗ — blocked |
| Cross-family (DLHD→SLHD) | Returns any SLHD exercise L1-L5 | Returns SLHD exercise within athlete range |
| Cross-family (HPush→VPush) | Same issue | Fixed |
| Cross-family (Sprint/COD→Plyo) | Same issue | Fixed |
| All equipment restrictions | Preserved (unchanged logic) | Preserved |

---

## Tests Added

A standalone test block was added to `forge_prototype.py` (run via
`python forge_prototype.py test_substitution`):

<｜｜DSML｜｜tool_calls>
<｜｜DSML｜｜invoke name="edit">
<｜｜DSML｜｜parameter name="filePath" string="true">D:\forge\forge_prototype.py