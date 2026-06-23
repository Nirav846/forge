# FORGE Generation Stress Test

## Summary

| Metric | Value |
|--------|-------|
| Total programs generated | 168 (14 blueprints × 3 levels × 4 equipment) |
| Programs that crashed | **0** |
| Programs with missing mandatory families | **0** |
| Total exercise slots allocated | ~16,308 |
| Unique exercises used | 181 of 191 |
| Exercises never used | **10** (all SLHD) |
| Difficulty-bypassing substitutions | **2,851** (17.5% of all selections) |
| Blueprints with broken "All" optional | **3** |

---

## Critical Issues (must fix before production)

### 1. SLHD Family Completely Inaccessible

**Severity: CRITICAL**

Single Leg Hip Dominant (SLHD) is not referenced in any blueprint's mandatory list, slot order, or optional list. The 10 SLHD exercises are never selected:

| Exercise | Difficulty | Equipment |
|----------|-----------|-----------|
| Single-Leg Glute Bridge | L1 | Bodyweight |
| Split Stance RDL | L2 | DB/Bodyweight |
| SL RDL (floor touch) | L2 | Bodyweight/Light DB |
| Single-Leg Bridge (elevated) | L2 | Bench |
| Weighted SL RDL | L3 | DB/KB |
| Single-Leg Hip Thrust | L3 | Barbell/Bench |
| Isometric Hamstring Hold | L3 | Partner/Wall |
| Single-Leg RDL (loaded) | L4 | DB/KB (heavy) |
| Band-Resisted Nordic | L3 | Band + Strap |
| Nordic Hamstring Curl | L4 | Partner/Strap |

**Root cause:** SLHD appears in slot_order of zero blueprints, mandatory lists of zero blueprints, and optional lists of zero blueprints. The "All" optional mechanism (which should catch it) is silently skipped (see Issue #4).

**Fix:** Add SLHD as an option in relevant blueprints (Upper/Lower Split, Court Sport, Return to Sport) or fix the "All" handling, or add SLHD via cross-family substitution from DLHD when appropriate.

---

### 2. Substitution Bypasses Difficulty Constraints

**Severity: CRITICAL**

When `select_exercise` fails to find an exercise matching the athlete's difficulty range + equipment, `substitute()` bypasses both constraints and returns ANY exercise in the family. This produces:

- **Beginner athletes getting L4-L5 exercises** (e.g., Single-Leg Bounding L5 for a beginner)
- **Advanced athletes getting L1 exercises** (e.g., Glute Bridge L1 for advanced bodyweight)
- **2,851 out-of-range selections** across 168 programs (17.5%)

| Blueprint | Sub count | Worst offenders |
|-----------|-----------|----------------|
| Upper/Lower Split | 460 | Band Lat Pulldown(64), Glute Bridge(36) |
| Mixed Modal GPP | 311 | Glute Bridge(35), Air Squat(24) |
| Rugby Off-Season | 265 | Wall Sit(30), Band Row(19) |
| Strength + Power | 262 | Glute Bridge(35), Wall Sit(26) |
| Full Body Strength | 260 | Glute Bridge(26), Wall Sit(23) |
| Hypertrophy | 243 | Glute Bridge(35), Air Squat(26) |
| Strength + Conditioning | 182 | Glute Bridge(24), Air Squat(23) |
| Sprint Development | 180 | Glute Bridge(25), Air Squat(18) |
| Power + Speed | 146 | Glute Bridge(27), Single-Leg Bounding(9) |
| Return to Sport | 144 | Air Squat(20), Wall Sit(16) |
| Youth Foundation | 110 | Glute Bridge(18), Wall Sit(14) |
| Deload | 67 | Wall Sit(14), Air Squat(12) |

**Fix:** `substitute()` should maintain difficulty constraints. Use `substitute` semantics: if no matching exercise at the right difficulty + equipment, expand difficulty to 1-5 but keep the equipment filter. Also consider cross-family substitution as a last resort with the right difficulty range.

---

### 3. Glute Bridge Overused (450 times)

**Severity: HIGH**

Glute Bridge (DLHD L1, Bodyweight) is the #1 most selected exercise. Breakdown:

| Equipment | Uses |
|-----------|------|
| Bodyweight | 371 |
| Minimal | 54 |
| Basic Gym | 11 |
| Full Gym | 14 |

| Level | Uses |
|-------|------|
| Beginner | 185 |
| Intermediate | 122 |
| Advanced | 143 |

**Root cause:** DLHD has exactly **one** bodyweight exercise (Glute Bridge at L1). `substitute()` bypasses difficulty and equipment, so even advanced athletes at bodyweight get Glute Bridge — the only DLHD exercise accessible without a barbell, trap bar, or hyperextension bench.

**Fix:** Add bodyweight DLHD exercises at L2-L4 (e.g., Single-Leg Glute Bridge already exists in SLHD but is inaccessible — move it or add variants). Or add a Nordic curl bodyweight progression. Or tighten `substitute()` to respect level constraints.

---

### 4. "All" in Optional is Silently Skipped

**Severity: HIGH**

Three blueprints use `optional=["All"]`:

| Blueprint | Intent | Reality |
|-----------|--------|---------|
| Youth Foundation (U14-U20) | Access to all families | No extra families added |
| Hypertrophy / Mass Accrual | All families accessible | No extra families added |
| Mixed Modal (GPP) | Rotates across all families | No extra families added |

The `resolve_slot_families` code treats "All" as a literal family name, and since "All" ∉ FAMILIES_SHORT, it's skipped in the optional selection loop without warning.

**Fix:** Handle "All" in optional by expanding to all 15 families minus already-seen ones.

---

### 5. Deload / Active Recovery Duplicate Slot

**Severity: MEDIUM**

`slot_order = ["Acc/Prehab", "DLKD / DLHD", "Core", "Acc/Prehab"]`

Acc/Prehab appears twice. The `seen` set prevents the second occurrence, so Deload only gets Acc/Prehab once per session (correct), but the slot order implies two Acc/Prehab slots. The second is silently dropped.

**Fix:** Remove the duplicate. The current behavior happens to be correct, but it's accidental — the code should warn or the slot should be cleaned up.

---

### 6. Bodyweight Athletes Get Extremely Repetitive Programs

**Severity: HIGH**

At bodyweight equipment level, many families have only 1-2 exercises total (see Diagnostic Data). This produces programs like:

**Hypertrophy / Mass Accrual, Beginner, Bodyweight (sample):**
- Session 1-16: Same 5 exercises rotating (Air Squat/Wall Sit, Glute Bridge, Push-Up/Wall Push-Up, Band Row/Scap Retraction, various core)
- Glute Bridge appears in **every single session** (16/16)
- 4 unique exercises used across a 16-session program

**All bodyweight programs across all blueprints** show:
- 2-3 exercises per family max
- Same exercises rotating session-to-session
- No meaningful progression across weeks

**Families with critical bodyweight gaps (L2+):** DLKD, DLHD, SLHD, HPush, HPull, VPush, VPull, Ball, Sprint/COD (L4+), Rot, Carry, Core (L4+), Acc/Prehab (L3+)

**Fix:** Add bodyweight progressions for these families, or reduce the number of bodyweight-exclusive programs in production, or add a "minimal equipment recommended" warning when bodyweight is selected.

---

### 7. Band-Resisted Push-Up Overused (388 times)

**Severity: MEDIUM**

Band-Resisted Push-Up (HPush L3, Band) has `min_equip_level=0` because the equipment string contains "Band". This means it's available at ALL equipment levels, making it the highest-difficulty HPush exercise accessible to bodyweight athletes.

Users with full gyms don't need a band-resisted push-up — they have barbell bench press, dumbbell bench, etc. But because the selection algorithm randomly picks from the filtered pool, Band-Resisted Push-Up gets selected alongside proper gym exercises.

**Fix:** `min_equip_level` should treat band exercises as equip level 1 (same as dumbbells), not equip level 0. Bands are not bodyweight-equivalent.

---

### 8. Upper/Lower Split: Same Exercise ×16

**Severity: MEDIUM**

Upper/Lower Split has 16 sessions over 4 weeks (4×/week). For bodyweight/minimal athletes, some families have so few options that the same exercise appears in all 16 sessions:

| Athlete | Equipment | Exercise | Appearances |
|---------|-----------|----------|-------------|
| Beginner | Bodyweight | Glute Bridge | 16/16 |
| Intermediate | Bodyweight | Glute Bridge | 16/16 |
| Advanced | Bodyweight | Glute Bridge | 16/16 |
| All levels | Bodyweight | Band Lat Pulldown | 16/16 |
| All levels | Bodyweight | Band Overhead Press | 16/16 |

**Fix:** Same as #6 — bodyweight exercise gaps. Also consider session-level deduplication: same exercise shouldn't appear more than once per day.

---

## Scoring Summary

### Automated Scoring Rubric

| Dimension | Base | Penalties Applied |
|-----------|------|-------------------|
| Coaching Credibility | 8/10 | −1 per 10% substitution-bypassed slots; −1 per overused exercise; −1 for missing families |
| Exercise Selection | 7/10 | −1 per exercise repeated 4+ times; −1 if <50% unique across sessions |
| Progression Quality | 7/10 | −1 if difficulty stays flat; −2 for backward progressions (L1 for advanced athletes) |
| Balance | 7/10 | −1 for missing family groups; −1 for "All" not working |
| Session Flow | 7/10 | −1 for inconsistent ordering; −1 for core before main strength |

### Aggregate Scores by Blueprint

| Blueprint | Credibility | Selection | Progression | Balance | Flow | Average |
|-----------|:-----------:|:---------:|:-----------:|:-------:|:----:|:-------:|
| Full Body Strength | 5 | 5 | 5 | 6 | 6 | 5.4 |
| Strength + Power | 6 | 6 | 6 | 6 | 7 | 6.2 |
| Strength + Conditioning | 5 | 5 | 5 | 6 | 6 | 5.4 |
| Power + Speed | 7 | 7 | 6 | 7 | 7 | 6.8 |
| Upper/Lower Split | 4 | 4 | 5 | 6 | 6 | 5.0 |
| Power Maintenance | 7 | 7 | 6 | 7 | 7 | 6.8 |
| Youth Foundation | 3 | 3 | 4 | 4 | 6 | 4.0 |
| Court Sport AD | 7 | 7 | 6 | 7 | 7 | 6.8 |
| Rugby Off-Season | 6 | 6 | 5 | 6 | 6 | 5.8 |
| Sprint Development | 6 | 6 | 5 | 6 | 6 | 5.8 |
| Hypertrophy/Mass | 4 | 3 | 4 | 5 | 6 | 4.4 |
| Return to Sport | 5 | 5 | 4 | 5 | 6 | 5.0 |
| Deload/Active Recovery | 6 | 5 | 5 | 6 | 7 | 5.8 |
| Mixed Modal GPP | 6 | 6 | 5 | 6 | 7 | 6.0 |

**Overall average: 5.6/10** — not production-ready.

### Score by Level

| Level | Avg Credibility |
|-------|:---------------:|
| Beginner | 4.2 |
| Intermediate | 5.8 |
| Advanced | 6.8 |

Beginner scores are dragged down by extreme repetition (only L1-L2 exercises available per family) and substitution bypass (L4-L5 exercises appearing in beginner programs).

### Score by Equipment

| Equipment | Avg Credibility |
|-----------|:---------------:|
| Bodyweight | 3.5 |
| Minimal | 5.0 |
| Basic Gym | 6.8 |
| Full Gym | 7.2 |

Bodyweight scoring is critically low due to exercise pool gaps across all families.

---

## Diagnostic Data

### Exercise Usage (Top 10 Most Selected)

| Exercise | Family | Count | Why |
|----------|--------|-------|-----|
| Glute Bridge | DLHD | 450 | Only bodyweight DLHD option |
| Band-Resisted Push-Up | HPush | 388 | Band = equip 0, accessible everywhere |
| Wall Sit | DLKD | 341 | 1 of 2 bodyweight DLKD options |
| Air Squat | DLKD | 340 | 1 of 2 bodyweight DLKD options |
| Goblet Squat | DLKD | 307 | Default DLKD at minimal+ |
| Side Plank (leg raise) | Core | 279 | |
| RKC Plank | Core | 262 | |
| Dumbbell Row | HPull | 260 | |
| Single-Leg RDL | DLHD | 253 | |
| Band Row | HPull | 242 | Band = equip 0 |

### Pool Gaps (80 family/difficulty/equipment combos with 0 exercises)

All bodyweight gaps across difficulties are concentrated in the L2-L5 range. Every family except Core and Plyo has bodyweight gaps starting at L2-L3. The most critical gaps affecting the most blueprints:

| Family | Gap | Impact |
|--------|-----|--------|
| DLHD | L2-L5 @ bodyweight | Glute Bridge is the **only** option at bodyweight |
| DLKD | L2-L5 @ bodyweight | Only Air Squat + Wall Sit at L1 |
| HPull | L2-L5 @ bodyweight | Scap Retraction L1 + Band Row L1 only |
| VPull | L2-L5 @ bodyweight | Band Lat Pulldown L1 only |
| Ball | L2-L5 @ bodyweight | Med Ball Push L1 only |

### Never-Used Exercises by Family

| Family | Never Used | Total in Family | % Missed |
|--------|-----------|-----------------|----------|
| SLHD | 10 | 10 | **100%** |
| All others | 0 | 181 | 0% |

---

## Manual Review — 10 Sample Programs

### Full Body Strength / Beginner / Bodyweight

**Score: 3/10** — Extremely repetitive. Air Squat/Wall Sit cycle for DLKD, Glute Bridge for DLHD, Push-Up/Wall Push-Up for HPush, Scap Retraction/Band Row for HPull. Ballistic slot gets inappropriate exercises (Single-Leg Bounding L5 for a beginner — substitution bypass). Wall Push-Up (L1) is too easy for horizontal push. No progression across weeks. Same exercises session after session.

**Credibility: 3** — Zero program variation across 12 sessions. A beginner would quit from boredom.
**Selection: 3** — Same 2-3 exercises per family for 4 weeks.
**Progression: 4** — Week 3-4 shift to higher difficulty, but L4-L5 ballistic for a beginner is dangerous.
**Balance: 4** — Missing single leg, rotational, carries. 5 mandatory families covered but all bilateral.
**Flow: 5** — Order is correct (ballistic → strength → core).

### Strength + Power / Intermediate / Basic Gym

**Score: 7/10** — Solid program. Good exercise variety (Paused Back Squat, Block Pull, Hang Clean, Bench Press). DLHD gets 4+ different exercises across sessions. Substitution issues at bodyweight levels resolved by "basic gym" equipment giving access to proper tools.

**Credibility: 7** — Coach could prescribe this. Exercise selection matches intent.
**Selection: 7** — Good variety. Block Pull and conventional deadlift used appropriately.
**Progression: 6** — Some reversion to L2 exercises in later weeks (Box Squat after Paused Back Squat).
**Balance: 7** — Power, strength, core, carry, rotational all represented.
**Flow: 8** — Power before strength, core at end.

### Upper/Lower Split / Advanced / Full Gym

**Score: 8/10** — The best-generated program. Full gym access gives maximum exercise selection. 147 unique exercises used across all Upper/Lower Split combos. Horsepower: Depth Jump, Pendlay Row, Conventional Deadlift, Muscle-Up. Good variety session-to-session.

**Credibility: 8** — Could be prescribed to an advanced athlete.
**Selection: 8** — Most exercises within correct difficulty range (3-5 for advanced).
**Progression: 8** — Week-over-week difficulty increase visible.
**Balance: 7** — 6 families covered per session. VPush/VPull both present. Missing SL work.
**Flow: 8** — Good ordering within sessions.

### Deload / Active Recovery / Intermediate / Minimal

**Score: 5/10** — Too heavy for a deload. Farmer's Walk (heavy) L4 at minimal equipment? Goblet Squat every session. The deload concept is lost — same exercises as a regular program.

**Credibility: 4** — Wouldn't prescribe this as a deload. Exercises are too challenging.
**Selection: 3** — Minor variety across 4 families. Goblet Squat every session.
**Progression: 5** — Random reversion between Wall Sit and Goblet Squat.
**Balance: 5** — Decent family coverage.
**Flow: 7** — Reasonable order.

### Hypertrophy / Mass Accrual / Beginner / Bodyweight

**Score: 2/10** — The worst program in the batch. 16 sessions of essentially the same 5 exercises. Glute Bridge in every single session. Band-Resisted Push-Up (L3) appearing in sessions 9-16 alongside L1 exercises. No hypertrophic stimulus possible with bodyweight only. The "mass accrual" intent is completely unmet.

**Credibility: 2** — Cannot prescribe this as a hypertrophy program.
**Selection: 2** — 5-6 exercises total across 16 sessions.
**Progression: 3** — Band-Resisted Push-Up appears in later weeks but at wrong intensity for beginner.
**Balance: 3** — 5 mandatory families only. No vertical, rotational, or carries.
**Flow: 5** — Order is correct.

### Power + Speed / Advanced / Full Gym

**Score: 9/10** — Excellent. Power Clean, Depth Jump, Flying 20m, Clean + Jerk all appropriate for advanced athlete. Speed work integrated correctly. Strong progression.

**Credibility: 9** — Track coach would approve.
**Selection: 9** — Advanced exercises selected. Good rotation.
**Progression: 8** — Week-over-week ramping.
**Balance: 8** — Power + speed focus maintained.
**Flow: 9** — Plyo → Ballistic → Strength → Sprint → Core.

### Return to Sport (Foundation) / Intermediate / Minimal

**Score: 6/10** — Good intent but execution issues. Acc/Prehab present (Face Pull not, though — that would be ideal). Goblet Squat every session is rehab-boring. Single Leg work varies nicely between Cossack Squat, Skater Squat, Bulgarian Split Squat. No hamstring-specific exercises.

**Credibility: 5** — Missing key rehab elements (hamstring, rotator cuff).
**Selection: 6** — Good single-leg variety. Poor DLKD variety.
**Progression: 6** — Random difficulty jumps (L2→L4→L2).
**Balance: 5** — Missing hamstring, VPush, HPush.
**Flow: 6** — Reasonable.

### Court Sport Athletic Development / Intermediate / Basic Gym

**Score: 8/10** — Excellent sport-specific program. Great mix of plyos, COD, rotational, single-leg. 142 unique exercises used overall — most varied blueprint.

**Credibility: 8** — Court sport coach would recognize this.
**Selection: 8** — Lateral Lunge, Med Ball Rotational Throw, 3-Cone Drill all pitch-relevant.
**Progression: 7** — Good variety.
**Balance: 8** — SLKD + Rotational + COD + HPush/HPull = complete.
**Flow: 8** — Good.

### Youth Foundation (U14-U20) / Beginner / Bodyweight

**Score: 3/10** — Too repetitive. Same 5 exercises in rotation. Youth athletes need variety and fun — Band-Resisted Push-Up and Scapular Retraction aren't engaging. No "All" optional families added means no plyo, no rotational, no carries.

**Credibility: 3** — Youth coach would reject this immediately.
**Selection: 3** — Boring exercise pool.
**Progression: 4** — Minor difficulty shift.
**Balance: 3** — Missing 10 of 15 families.
**Flow: 5** — Correct order but too few families.

### Mixed Modal (GPP) / Advanced / Full Gym

**Score: 8/10** — Solid GPP program. All core families covered. Good exercise variety (Front Squat, Deadlift, Bench, Row, Plyo, Core, Carry). "All" optional not working means no rotational, ballistic, or speed work — the main weakness.

**Credibility: 7** — Useful GPP but missing variety.
**Selection: 7** — Good within the families selected.
**Progression: 7** — Consistent difficulty.
**Balance: 7** — Missing rotational and ballistic for a "mixed modal" program.
**Flow: 8** — Good.

---

## Recurring Failures

### Failure Class A: Bodyweight exercise pool is too shallow
- Affects: All 14 blueprints, all 3 levels (but critical at beginner)
- Root cause: Most families were designed for gym-equipped athletes
- Scale: 80 pool gaps, 450 Glute Bridge uses, 10 never-used exercises
- Impact: Severe for all bodyweight programs (avg credibility 3.5/10)

### Failure Class B: Substitution silently violates athlete level
- Affects: All blueprints when equipment < "basic gym"
- Root cause: `substitute()` drops difficulty filter
- Scale: 2,851 out-of-range selections (17.5%)
- Impact: Beginners get L5 exercises; advanced athletes get L1

### Failure Class C: Family siloing makes SLHD unreachable
- Affects: All programs (no SLHD exercises ever used)
- Root cause: SLHD not in any blueprint's mandatory/optional/slot list
- Scale: 10 exercises dead code
- Impact: Missing hamstring-specific work across all programs

### Failure Class D: "All" optional mechanism is dead code
- Affects: Youth Foundation, Hypertrophy, Mixed Modal
- Root cause: "All" not expanded to actual families
- Scale: 3 blueprints with reduced optional pools
- Impact: Youth Foundation becomes 5-family-only, defeating its "variety" purpose

### Failure Class E: Band equipment classified as bodyweight
- Affects: All programs with Band exercises
- Root cause: `min_equip_level` returns 0 for band-string exercises
- Scale: 388 Band-Resisted Push-Up selections, 242 Band Row, etc.
- Impact: Band exercises compete with bodyweight exercises, degrading bodyweight-only program quality

---

## Recommendations (Priority Order)

1. **Fix SLHD accessibility** — Add SLHD to relevant blueprint optional lists or slot orders. SLHD maps to DLHD in the substitution matrix; use this to naturally include hamstring single-leg work.

2. **Fix `substitute()` difficulty filter** — Never bypass athlete level constraints. If no exercise exists at the right difficulty+equipment, try cross-family substitution with the original difficulty range before expanding difficulty.

3. **Add bodyweight progressions** — Every family needs at least 2 bodyweight exercises at each difficulty level 1-4. Current bodyweight DLHD: 1 exercise at L1, zero at L2-L5.

4. **Fix "All" optional handling** — `resolve_slot_families` should expand "All" to `FAMILIES_SHORT` minus already-seen families.

5. **Reclassify band equipment** — Band exercises should be equip level 1 (minimal), not 0 (bodyweight). This prevents Band-Resisted Push-Up from competing with Push-Up at bodyweight level.

6. **Add session-level deduplication** — Same exercise shouldn't appear more than once per session (currently possible for families that appear in multiple slots).

7. **Add week-over-week progression guarantee** — Ensure difficulty increases monotonicly across weeks (currently random each session).

8. **Remove duplicate in Deload slot_order** — Cosmetic cleanup.
