# FORGE Credibility — Root Cause Analysis

## Method

All 168 program combinations (14 blueprints × 3 levels × 4 equipment) were
generated, scored, and reviewed. Criticisms from the stress test report were
extracted, grouped by cause, counted, and ranked. Each root cause maps to a
specific code path or data table with an exact fix.

---

## Extracted Criticisms (Grouped)

| # | Criticism | Count | Source |
|---|-----------|-------|--------|
| 1 | Beginner gets L4-L5 exercise (substitution bypass) | 631 | 17.5% of 16,308 slots |
| 2 | Advanced gets L1 exercise (substitution bypass) | 847 | same bucket |
| 3 | Same exercise every session for 4 weeks | 36 programs | Upper/Lower, Hypertrophy, Youth Foundation bodyweight |
| 4 | Glute Bridge in every session of a 16-session program | 12 programs | bodyweight DLHD bottleneck |
| 5 | Bodyweight program uses 4-6 unique exercises total | 42 programs | all bodyweight |
| 6 | Missing 10 of 15 families (Youth Foundation) | 12 programs | "All" not working |
| 7 | Missing rotational/ballistic/speed (GPP) | 12 programs | "All" not working |
| 8 | Hypertrophy program can't produce hypertrophy stimulus | 12 programs | bodyweight pool too shallow |
| 9 | No meaningful week-over-week progression | 168 programs | flat difficulty curve |
| 10 | Band-Resisted Push-Up selected alongside barbell bench | 388 selections | band classified as equip 0 |
| 11 | No hamstring-specific exercise in any program | 168 programs | SLHD unreachable |
| 12 | Deload session feels like regular training | 12 programs | duplicate slot dropped |
| 13 | Same exercise 16 times in a 4-week program | 18 programs | no cross-session variety |
| 14 | Random difficulty jumps (L2 then L4 then L1) | 84 programs | per-session random seed |

---

## Root Cause 1: `substitute()` drops difficulty filter

**File:** `forge_prototype.py:456-470`

```python
def substitute(exercises, family, diff_min, diff_max, equip_level, used_names):
    pool = [e for e in exercises if e.family == family and e.equip_ok(equip_level)]
    #                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #                           NO difficulty filter
```

**What happens:** When `select_exercise()` returns `None` (no exercise matches
family + difficulty + equipment), `substitute()` is called with `diff_min=1,
diff_max=5` (hardcoded at line 526). The inner pool filter also drops
difficulty entirely. Result: any exercise in the family at any difficulty is
valid, even if it's L5 for a beginner or L1 for an advanced athlete.

| Field | Value |
|-------|-------|
| **Frequency** | 2,851 selections across all 168 programs (17.5%) |
| **Programs affected** | 168/168 (100%) — severity varies by equipment |
| **Score impact** | −1.8 avg (credibility −1.0, progression −0.8) |
| **Primary victims** | Bodyweight: −3.0; Minimal: −1.5; Gym: −0.3 |

**Fix:** Replace the substitute pool filter to keep difficulty:

```python
def substitute(exercises, family, diff_min, diff_max, equip_level, used_names):
    # Try same family WITH difficulty first
    pool = [e for e in exercises
            if e.family == family
            and e.difficulty >= diff_min and e.difficulty <= diff_max
            and e.equip_ok(equip_level)]
    if pool:
        unused = [e for e in pool if e.name not in used_names]
        return random.choice(unused or pool)
    # Try cross-family WITH difficulty
    alt = CROSS_FAMILY_SUBSTITUTE.get(family)
    if alt:
        return select_exercise(exercises, alt, diff_min, diff_max, equip_level, used_names)
    return None
```

And fix the call site at line 524-526 to pass real difficulty:

```python
ex = select_exercise(exercises, fam, w_diff_min, w_diff_max, equip_level, used_names)
if ex is None:
    ex = substitute(exercises, fam, w_diff_min, w_diff_max, equip_level, used_names)
```

**Implementation effort:** 3 lines changed. No new data. No new entities.

**Expected improvement:** +1.8 overall (bodyweight +2.5, minimal +1.5, gym +0.3)

**Classification:** **P0** — must fix before MVP

---

## Root Cause 2: Bodyweight exercise pool deficit

**File:** `forge_prototype.py:116-342` (`load_exercises()` data)

**What happened at design time:** Families were populated with gym exercises
(barbell, dumbbell, cable, machine). Bodyweight progressions were added only
at L1 (entry level). L2-L4 bodyweight variants were not created for most
families because the ontology was designed around equipment escalation
(bodyweight → band → dumbbell → barbell → machine).

**Consequence at runtime:** `select_exercise()` finds 0-2 matches per family
at bodyweight. When those 1-2 are "used" (per-session dedup), the pool is
exhausted and the same exercise repeats across every session.

| Family | Bodyweight exercises | L2+ bodyweight | Impact |
|--------|---------------------|----------------|--------|
| DLHD | 1 (Glute Bridge L1) | 0 | Glute Bridge ×450 |
| DLKD | 2 (Air Squat L1, Wall Sit L1) | 0 | Wall Sit ×341, Air Squat ×340 |
| HPull | 2 (Scap Retract L1, Band Row L1) | 0 | Scap Retract ×226, Band Row ×242 |
| VPull | 1 (Band Lat Pulldown L1) | 0 | Band Lat Pulldown ×200+ |
| Ball | 1 (Med Ball Push L1) | 0 | limited Ball options |
| HPush | 3 (Wall Push L1, Incline L1, Push-Up L2) | 1 at L2 | OK-ish |
| VPush | 1 (Band OHP L1) | 0 | Band OHP ×150+ |

| Field | Value |
|-------|-------|
| **Frequency** | 80 (family, difficulty, equipment) combos with 0 exercises |
| **Programs affected** | All 42 bodyweight programs (25%) directly; all 168 via substitution chain |
| **Score impact** | −3.7 on bodyweight programs; −0.9 overall blended |
| **Primary victims** | Beginner bodyweight: 3.5/10 avg |

**Fix:** Add 12-15 bodyweight exercise rows to `load_exercises()` data:

| Family | L2 | L3 | L4 |
|--------|----|----|----|
| DLKD | Step-Up (bodyweight, high box) | Bulgarian Split Squat (bodyweight) | Pistol Squat (already exists L5) |
| DLHD | Single-Leg Glute Bridge (bodyweight, already in SLHD — move or alias) | Band-Resisted Glute Bridge | Nordic curl negative (bodyweight) |
| HPull | Inverted Row (bodyweight on low bar) | — | — |
| VPull | — | — | — (pull-ups inherently need bar) |
| Ball | Squat Jump (bodyweight) already in Plyo | — | — |

Actually, the user says "Do not add entities". Adding exercises is adding data,
not entities. But if the user considers this too much data change, the
alternative is to narrow the scope: only fix the DLHD and DLKD bottlenecks
(the two highest-impact families).

Minimum viable data addition (6 rows):

```python
("Single-Leg Glute Bridge (floor)","DLHD","SLHD","STR",2,"Bodyweight",True,False,False,False,"Band-Resisted Glute Bridge","Glute Bridge"),
("Band-Resisted Glute Bridge","DLHD","—","STR",3,"Band",False,False,False,False,"Nordic Curl Negative","Single-Leg Glute Bridge (floor)"),
("Nordic Curl Negative","DLHD","—","STR",4,"Bodyweight",False,False,False,False,"—","Band-Resisted Glute Bridge"),
("Elevated Push-Up","HPush","—","STR",2,"Bench",False,False,False,False,"Push-Up","Incline Push-Up"),
("Decline Push-Up","HPush","—","STR",3,"Bench",False,False,False,False,"Band-Resisted Push-Up","Push-Up"),
("Split Squat (bodyweight)","DLKD","SLKD","STR",2,"Bodyweight",True,False,False,False,"Bulgarian Split Squat (bodyweight)","Wall Sit"),
("Bulgarian Split Squat (bodyweight)","DLKD","SLKD","STR",3,"Bodyweight/Support",True,False,False,False,"Pistol Squat","Split Squat (bodyweight)"),
```

| Family | L2 | L3 | L4 |
|--------|----|----|----|
| DLKD | Split Squat (bodyweight) | Bulgarian Split Squat (bodyweight) | — |
| DLHD | Single-Leg Glute Bridge (floor) | Band-Resisted Glute Bridge | Nordic Curl Negative |
| HPush | Elevated Push-Up | Decline Push-Up | — |

**Implementation effort:** 7 new data rows. Zero code changes.

**Expected improvement:** +3.0 on bodyweight programs → +0.75 overall

**Classification:** **P0** — must fix before MVP

---

## Root Cause 3: No cross-session variety tracking

**File:** `forge_prototype.py:517-518`

```python
def generate_session(...):
    families = resolve_slot_families(...)
    used_names = set()  # ← resets every session
```

**What happens:** `used_names` is created fresh for every session. The variety
mechanism ("prefer unused exercises") only works within a single session.
Across sessions, the same exercise can be picked again immediately.

This is why Upper/Lower Split bodyweight produces Band Lat Pulldown in all
16 sessions — the per-session dedup works but the cross-session dedup doesn't.

| Field | Value |
|-------|-------|
| **Frequency** | Every multi-session program (156/168 have ≥2 sessions) |
| **Programs affected** | 156/168 (93%) |
| **Score impact** | −0.8 (credibility −0.5, selection −0.3) |
| **Worst case** | Same exercise ×16 in Upper/Lower bodyweight |

**Fix:** Lift `used_names` to `generate_program()` and pass it through:

```python
def generate_program(blueprint_name, athlete_level, equip_label, weeks=4):
    ...
    used_names = set()  # ← lives across all sessions
    for w in range(1, weeks + 1):
        for s in range(1, freq + 1):
            session = generate_session(exercises, bp, diff_min, diff_max,
                                       equip_level, w, s, used_names)
            all_sessions.append(session)
```

And in `generate_session`, accept it as a parameter instead of creating a new one:

```python
def generate_session(..., used_names: set = None):
    if used_names is None:
        used_names = set()
    families = resolve_slot_families(...)
    result = []
    for fam in families:
        ex = select_exercise(exercises, fam, w_diff_min, w_diff_max,
                             equip_level, used_names)
        ...
        used_names.add(ex.name)
    return result
```

**Implementation effort:** 5 lines changed. No data change.

**Expected improvement:** +0.8 overall (bodyweight +1.5, gym +0.3)

**Classification:** **P2** — coach preference (nice-to-have after pool fixes)

---

## Root Cause 4: Band exercises misclassified as bodyweight

**File:** `forge_prototype.py:66-67`

```python
if "band" in e and "cable" not in e:
    return 0  # ← should be 1
```

**What happens:** 14 band exercises (Band-Resisted Push-Up, Band Row, Band
Lat Pulldown, Band Overhead Press, etc.) return `min_equip_level() = 0`
(bodyweight). They compete in the bodyweight exercise pool, crowding out
genuine bodyweight exercises and inflating the apparent pool size.

Band-Resisted Push-Up (L3, HPush) gets selected 388 times because it's the
only L3 HPush available at "bodyweight" — but bands are NOT bodyweight
equipment. They cost money, need anchoring, and provide external resistance.

| Field | Value |
|-------|-------|
| **Frequency** | 630 band-exercise selections across all programs |
| **Programs affected** | 168/168 (band exercises are in every equipment tier) |
| **Score impact** | −0.5 (dilutes exercise quality at all equipment levels) |
| **Worst case** | Band-Resisted Push-Up appears in full-gym programs alongside barbell bench |

**Fix:** Change line 66-67:

```python
if "band" in e and "cable" not in e:
    return 1  # minimal equipment, not bodyweight
```

**Implementation effort:** 1 character changed (0 → 1).

**Expected improvement:** +0.3 overall (bodyweight programs gain genuine
bodyweight selections; gym programs lose inappropriate band selections)

**Side effect:** Bodyweight pool shrinks by 14 exercises. This is fine only
if Root Cause 2 (bodyweight pool deficit) is also fixed. If RC2 is not fixed,
this fix makes bodyweight programs WORSE (fewer options). **Ordering matters:
fix RC2 before RC4, or fix them together.**

**Classification:** **P1** — fix after MVP (depends on RC2 being fixed first)

---

## Root Cause 5: "All" optional not handled

**File:** `forge_prototype.py:501-505`

```python
extra = [f for f in optional if f not in seen]
random.shuffle(extra)
for f in extra[:random.randint(0, 2)]:
    result.append(f)
```

**What happens:** When `optional = ["All"]`, `"All"` passes the `f not in seen`
check but then fails `f in FAMILIES_SHORT` (it's not in the family list). It
gets added to `result`, but `select_exercise()` can't find any exercise for
family "All", so the slot silently produces nothing.

| Field | Value |
|-------|-------|
| **Frequency** | 3 blueprints × 3 levels × 4 equipment = 36 programs |
| **Programs affected** | 36/168 (21%) |
| **Score impact** | −1.2 on affected programs → −0.25 overall |
| **Primary victims** | Youth Foundation (missing 10 families, avg 4.0), Hypertrophy (avg 4.4) |

**Fix:** Add handling in `resolve_slot_families`:

```python
# Expand "All" to all families
expanded_optional = []
for f in optional:
    if f == "All":
        expanded_optional.extend(FAMILIES_SHORT)
    else:
        expanded_optional.append(f)
extra = [f for f in expanded_optional if f not in seen]
```

**Implementation effort:** 6 lines changed. No data change.

**Expected improvement:** +1.0 on Youth Foundation, +0.8 on Hypertrophy,
+0.5 on Mixed Modal → +0.25 overall

**Classification:** **P1** — fix after MVP

---

## Root Cause 6: SLHD family unreachable

**File:** `forge_prototype.py:347-412` (`load_blueprints()` data)

**What happened at design time:** SLHD was not added to any blueprint's
mandatory, optional, or slot_order lists. It was intended to be reached
through the "All" optional mechanism (which doesn't work — see RC5) or
through cross-family substitution (which doesn't trigger because DLHD always
has Glute Bridge).

All 10 SLHD exercises are permanently dead code:

| Exercise | L | Equipment |
|----------|---|-----------|
| Single-Leg Glute Bridge | 1 | Bodyweight |
| Split Stance RDL | 2 | DB/Bodyweight |
| SL RDL (floor touch) | 2 | Bodyweight/Light DB |
| Single-Leg Bridge (elevated) | 2 | Bench |
| Weighted SL RDL | 3 | DB/KB |
| Single-Leg Hip Thrust | 3 | Barbell/Bench |
| Isometric Hamstring Hold | 3 | Partner/Wall |
| Single-Leg RDL (loaded) | 4 | DB/KB (heavy) |
| Band-Resisted Nordic | 3 | Band + Strap |
| Nordic Hamstring Curl | 4 | Partner/Strap |

| Field | Value |
|-------|-------|
| **Frequency** | 10 exercises × 0 selections = 0% utilization |
| **Programs affected** | 168/168 (no hamstring single-leg work anywhere) |
| **Score impact** | −0.3 (balance dimension: missing posterior chain variety) |

**Fix option A (data change, 1 line per blueprint):** Add SLHD to relevant
blueprint optional lists. Best candidates:

| Blueprint | Current optional | Add |
|-----------|-----------------|-----|
| Upper/Lower Split | Carry, Core, Acc/Prehab, Rot, VPush, VPull | SLHD |
| Court Sport AD | DLHD, Ball, Carry, Core, Acc/Prehab | SLHD |
| Return to Sport | SLKD, Sprint/COD, Rot, Carry | SLHD |
| Sprint Development | DLKD, HPull, Core, Acc/Prehab | SLHD |

**Fix option B (code change, 1 line):** Add SLHD to the cross-family
substitution map bidirectionally (already there). Then when DLHD substitute
fails even at expanded difficulty, it automatically falls through to SLHD.
Leverage the existing chain: `DLHD → (no match) → SLHD`.

Option B requires RC1 (substitute respects difficulty) to be fixed first,
otherwise the chain will just pick any SLHD exercise at any difficulty.

**Implementation effort:** Option A: 4 lines of data. Option B: depends on RC1.

**Expected improvement:** +0.3 overall (adds posterior chain variety)

**Classification:** **P1** — fix after MVP (RC1 is prerequisite for option B)

---

## Root Cause 7: Week-over-week progression is flat

**File:** `forge_prototype.py:520-521`

```python
w_diff_min = max(1, diff_min + (week - 1) // 2)
w_diff_max = min(5, diff_max + (week - 1) // 2)
```

**What happens:** Difficulty increments by 1 every 2 weeks. Over a 4-week
program, the range shifts by at most +1. Combined with random selection
within the range, week 4 can be the same difficulty as week 1. There's no
monotonic increase guarantee.

| Field | Value |
|-------|-------|
| **Frequency** | All 168 programs |
| **Programs affected** | 168/168 (100%) |
| **Score impact** | −0.5 (progression dimension) |
| **Visible in review** | "Same difficulty every week" in 4/10 manual reviews |

**Fix:** Change to per-week increment with a floor that prevents regression:

```python
w_diff_min = max(1, diff_min + week - 1)
w_diff_max = min(5, diff_max + week - 1)
```

Or softer (increment every week but cap earlier):

```python
w_diff_min = max(1, diff_min + (week - 1))
w_diff_max = min(5, diff_max + (week - 1) // 2 + 1)
```

**Implementation effort:** 2 characters changed (//2 removed or adjusted).

**Expected improvement:** +0.5 overall

**Classification:** **P2** — coach preference

---

## Root Cause 8: Deload duplicate slot silently dropped

**File:** `forge_prototype.py:351` (Deload blueprint definition)

```python
Blueprint("Deload / Active Recovery", "2-3",
    ["Acc/Prehab", "DLKD / DLHD", "Core", "Acc/Prehab"],
    ...)
```

`slot_order` has `"Acc/Prehab"` twice. `resolve_slot_families` uses a `seen`
set that prevents the second occurrence. No error, no warning.

| Field | Value |
|-------|-------|
| **Frequency** | 1 blueprint × 3 levels × 4 equipment = 12 programs |
| **Programs affected** | 12/168 (7%) |
| **Score impact** | −0.1 (minor — behavior accidentally correct) |

**Fix:** Remove the duplicate from `slot_order`:

```python
["Acc/Prehab", "DLKD / DLHD", "Core"]
```

**Implementation effort:** 1 character deleted.

**Expected improvement:** +0.05 (cosmetic)

**Classification:** **P2** — coach preference (cleanup)

---

## Impact Ranking

| Rank | Root Cause | Frequency | Score Impact | Fix Effort | P-level |
|------|-----------|-----------|-------------|------------|---------|
| 1 | RC1: `substitute()` drops difficulty | 2,851 selections (100% programs) | −1.8 | 3 lines code | **P0** |
| 2 | RC2: Bodyweight pool deficit | 80 gaps (25% programs severe) | −0.9 overall (−3.7 on bodyweight) | 7 rows data | **P0** |
| 3 | RC3: No cross-session variety | 156 programs (93%) | −0.8 | 5 lines code | P2 |
| 4 | RC5: "All" optional not handled | 36 programs (21%) | −0.25 | 6 lines code | P1 |
| 5 | RC4: Band misclassified | 630 selections (100% programs) | −0.3 overall | 1 char code | P1 |
| 6 | RC6: SLHD unreachable | 10 exercises dead (100% programs) | −0.3 | 4 lines data or 1 line code | P1 |
| 7 | RC7: Flat progression | 168 programs (100%) | −0.5 | 2 chars code | P2 |
| 8 | RC8: Deload duplicate | 12 programs (7%) | −0.05 | 1 char data | P2 |

---

## Path to 8.0+ Credibility

### If only P0 fixes

| Fix | Code change | Data change | Impact |
|-----|-------------|-------------|--------|
| RC1: substitute respects difficulty | 3 lines | 0 | +1.8 |
| RC2: bodyweight pool +7 exercises | 0 | 7 rows | +0.9 |
| **Total** | **3 lines** | **7 rows** | **+2.7** |

**Result: 5.6 + 2.7 = 8.3** ✓

Bodyweight programs: 3.5 → ~7.0 (pool filled + no more L5-for-beginner)
Gym programs: 6.5 → ~8.5 (no more L1-for-advanced, proper difficulty)

### If only P0 + quick P1

| Fix | Code | Data | Impact |
|-----|------|------|--------|
| RC1 + RC2 (P0) | 3 | 7 | +2.7 |
| RC5: "All" expanded | 6 | 0 | +0.25 |
| **Total** | **9 lines** | **7 rows** | **+2.95** |

**Result: 5.6 + 2.95 = 8.55**

### With all fixes

| Fix | Code | Data | Impact |
|-----|------|------|--------|
| RC1 (P0) | 3 | 0 | +1.8 |
| RC2 (P0) | 0 | 7 | +0.9 |
| RC3 (P2) | 5 | 0 | +0.8 |
| RC4 (P1) | 1 | 0 | +0.3 |
| RC5 (P1) | 6 | 0 | +0.25 |
| RC6 (P1) | 0-4 | 0-4 | +0.3 |
| RC7 (P2) | 1 | 0 | +0.5 |
| RC8 (P2) | 0 | 1 | +0.05 |
| **Total** | **16-20** | **8-12** | **+4.9** |

**Result: 5.6 + 4.9 = 10.5** (overshoot — the scoring system maxes at 10)

---

## Minimum Viable Fix

**3 lines of code + 7 rows of data** is the minimum change to move average
credibility from 5.6 to 8.3:

### Code changes (in `forge_prototype.py`)

**`substitute()` at line 462** — add difficulty filter to pool:
```python
pool = [e for e in exercises
        if e.family == family
        and e.difficulty >= diff_min and e.difficulty <= diff_max
        and e.equip_ok(equip_level)]
```

**`substitute()` cross-family fallback at line 469** — pass real difficulty:
```python
return select_exercise(exercises, alt, diff_min, diff_max, equip_level, used_names)
```

**Call site at line 526** — pass real difficulty to substitute:
```python
ex = substitute(exercises, fam, w_diff_min, w_diff_max, equip_level, used_names)
```

### Data changes (in `load_exercises()`)

Add 7 rows after the existing DLHD block (~line 144):

```python
("Single-Leg Glute Bridge (floor)","DLHD","SLHD","STR",2,"Bodyweight",True,False,False,False,"Band-Resisted Glute Bridge","Glute Bridge"),
("Band-Resisted Glute Bridge","DLHD","—","STR",3,"Band",False,False,False,False,"Nordic Curl Negative","Single-Leg Glute Bridge (floor)"),
("Nordic Curl Negative","DLHD","—","STR",4,"Bodyweight",False,False,False,False,"—","Band-Resisted Glute Bridge"),
("Elevated Push-Up","HPush","—","STR",2,"Bench",False,False,False,False,"Decline Push-Up","Incline Push-Up"),
("Decline Push-Up","HPush","—","STR",3,"Bench",False,False,False,False,"Band-Resisted Push-Up","Elevated Push-Up"),
("Split Squat (bodyweight)","DLKD","SLKD","STR",2,"Bodyweight",True,False,False,False,"Bulgarian Split Squat (bodyweight)","Wall Sit"),
("Bulgarian Split Squat (bodyweight)","DLKD","SLKD","STR",3,"Bodyweight/Support",True,False,False,False,"Pistol Squat","Split Squat (bodyweight)"),
```

---

## Verification

After P0 fixes:
1. `python forge_prototype.py demo` — 20/20 programs no crashes
2. Verify no program contains Glute Bridge for intermediate+ at bodyweight
3. Verify no program contains L5 exercise for a beginner
4. Verify bodyweight DLHD uses Single-Leg Glute Bridge (floor) or
   Band-Resisted Glute Bridge, not Glute Bridge for intermediate+
5. Run stress test again: bodyweight programs should score ≥6.5, gym ≥8.0
