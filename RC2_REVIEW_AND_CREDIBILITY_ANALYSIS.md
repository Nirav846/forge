# RC2 Review & Credibility Analysis

## Summary of Empirical Findings

**168 programs × 4 weeks = 12,107 exercise selections analyzed.**

| Metric | Value |
|--------|-------|
| Total selection slots | 12,107 |
| Empty slots (family expected but not generated) | **1,962** |
| Misleveled exercises (L1 for advanced) | **0** (RC1 confirmed) |
| Glute Bridge for non-beginner | **0** (RC1 confirmed) |
| Cross-family substitutions | Heavy (see below) |
| Programs with exercise repetition | 167/168 |

---

## 1. Where Empty Slots Actually Occur

### By Family (all equipment levels)

| Family | Empty Slots | Primary Cause |
|--------|-------------|---------------|
| **HPull** | 342 | Only L1 bodyweight; no L2+ options |
| **Acc/Prehab** | 255 | No L3+ bodyweight; always optional → skipped |
| **"All" (RC5 bug)** | 229 | Optional pool mis-handling in 3 blueprints |
| **Rot** | 118 | No L3+ bodyweight |
| **Carry** | 106 | Zero bodyweight exists |
| **Core** | 81 | No L4+ bodyweight |
| **DLHD** | 64 | Only Glute Bridge L1 bodyweight |
| **HPush** | 67 | No L4+ bodyweight (less relevant — HPush rarely needs L4+ in practice) |
| **VPull** | 39 | Only Band Lat Pulldown L1 |
| **VPush** | 0 | Always fills via cross-family → HPush |
| **Ball** | 0 | Always fills via cross-family → Plyo |
| **DLKD** | 0 | Always fills via cross-family → SLKD |

### Key Insight

**Ball and VPush have zero empty slots** despite having almost no bodyweight
exercises, because cross-family substitution handles them. But HPull fails for
bodyweight because VPull (its cross-family partner) also has nothing at L2+.

---

## 2. Review of Each Proposed Exercise

### 2.1 Glute Bridge March (DLHD L2)

**Current behavior:** DLHD bodyweight = Glute Bridge L1 only. All 245 non-beginner
DLHD bodyweight slots cross-substitute to SLHD (Band-Resisted Nordic, SL RDL,
Split Stance RDL). 64 empty slots remain for advanced bodyweight.

**Verdict: KEEP** — but note: only closes beginner/intermediate gap, not advanced.

**Coaching rationale:**
- DLHD→SLHD cross-family is frequency-high (245×) but movement-pattern compatible
  (both hip-dominant). A coach might not even notice the substitution.
- However: Glute Bridge March is a natural L1→L2 overload within DLHD's own
  progression. It lets the system stay in-family for beginner week 3-4 and
  intermediate without relying on SLHD.
- It doesn't fix advanced bodyweight DLHD (diff 3-5 still has nothing) — but
  that's a small population (advanced bodyweight is rare in practice).

**Expected credibility impact:** +0.2 (reduces cross-family for beginner/intermediate)

### 2.2 Burpee / Burpee + Tuck Jump (Ball L2/L4)

**Current behavior:** Ball has 0 bodyweight exercises across all 5 levels.
191 Ball bodyweight slots are filled by cross-family → Plyo (Bounding, Broad Jump,
CMJ, etc.). Zero empty slots.

**Verdict: REJECT** — Ball→Plyo cross-family is already credible; Burpee makes it worse.

**Coaching rationale:**
- Ballistic training with bodyweight IS plyometric training. A coach prescribing
  "Plyo for Ball day" is normal. The SJ→CMJ→Broad Jump→Bounding progression
  covers the same power output as a bodyweight Ball progression would.
- Burpee is primarily a **conditioning/metcon** exercise, not power. It has a
  push-up (strength endurance) and jump (explosive), but its primary coaching
  use is cardiovascular conditioning, not ballistic power development.
- Adding Burpee as Ball would produce *less credible* programs — a coach seeing
  "Ballistic: Burpee" would question the classification.
- If we MUST add a bodyweight Ball exercise, **Tuck Jump** or **Split Jump** would
  be more credible (both are already in Plyo, so duplication).

**Alternative considered:** Add nothing (preferred). Bodyweight power development
IS plyometrics. The Ball→Plyo substitution is architecturally correct.

### 2.3 Table Row (HPull L2)

**Current behavior:** HPull has 342 empty slots — the **#1 gap** in the system.
Only L1 bodyweight exercises exist (Band Row, Scap Retraction). No L2+ bodyweight
option anywhere. Cross-family to VPull also has nothing at L2+.

**Verdict: KEEP** — fills the single largest gap.

**Coaching rationale:**
- Table rows (grip a sturdy table edge, walk feet out, pull chest to table) are
  a standard bodyweight horizontal row. Used universally in hotel-room, garage,
  and outdoor training.
- They are safe (table doesn't move if properly secured), coach-common, and the
  natural L2 progression from Band Row (L1).
- They fix 286 bodyweight HPull slots immediately.
- They also fix an additional ~56 minimal-equipment slots (where barbell for
  Inverted Row is unavailable).

**Expected credibility impact:** +0.8 (fills largest gap with coach-common exercise)

### 2.4 Pike Push-Up (VPush L2)

**Current behavior:** VPush bodyweight = Band Overhead Press L1. 44/53 VPush
bodyweight selections (83%) are cross-family → HPush (Band-Resisted Push-Up,
Push-Up). Zero empty slots.

**Verdict: KEEP** — but for program quality, not gap-filling.

**Coaching rationale:**
- Currently 83% of VPush bodyweight selections are horizontal pushes doing
  vertical work. A coach would notice "VPush = Push-Up" and find it odd.
- Pike Push-Up is the standard bodyweight vertical push progression. It directly
  overloads the overhead pressing motion without equipment.
- It doesn't create new slots (VPush is never empty), but it **improves the
  quality** of existing slots by keeping the movement vector correct.

**Expected credibility impact:** +0.3 (quality improvement, not gap-filling)

### 2.5 Towel Chin-Up (VPull L2)

**Current behavior:** VPull bodyweight = Band Lat Pulldown L1 only. 39 empty
slots (20 advanced, 19 intermediate bodyweight). Only 11 total bodyweight
selections — all L1.

**Verdict: REPLACE** — safety concerns and inconsistent availability.

**Safety assessment of Towel Chin-Up:**
- **Door-dependent:** A towel over a door requires a door that closes securely
  and a hinge gap wide enough. Many modern doors have minimal gaps.
- **Door damage:** Repeated loading can damage door frames, hinges, or trim.
- **Liability:** A towel slipping mid-rep is a fall risk (shoulder/head injury).
- **Availability:** Not all environments have suitable doors.

**Alternative: Band Straight-Arm Pulldown (L2)**
- Uses the same band as Band Lat Pulldown (L1), but with straight arms
  (pulldown from overhead to thighs).
- Progression within the band family: Band Lat Pulldown (L1) → Band
  Straight-Arm Pulldown (L2) → increasing band tension or grip variations.
- Safe, universally available (needs only a band + overhead anchor point),
  and coach-common.
- Fixed anchor (door frame, beam, tree branch) is more reliable than a towel.

**Revised proposal:**

```
Exercise:       Band Straight-Arm Pulldown
Difficulty:     L2
Equipment:      Band
Family:         VPull
Progression:    Narrow-Grip Straight-Arm Pulldown
Regression:     Band Lat Pulldown
```

**Expected credibility impact:** +0.4 (fills VPull bodyweight gap, safe)

---

## 3. Revised RC2 Proposal (Post-Review)

| # | Family | Exercise | Diff | Equipment | Verdict | Credibility Impact | Rationale |
|---|--------|----------|------|-----------|---------|-------------------|-----------|
| 1 | **HPull** | Table Row | L2 | Bodyweight | **KEEP** | **+0.8** (P0) | Fills #1 gap (342 empty slots) |
| 2 | **VPull** | Band Straight-Arm Pulldown | L2 | Band | **REPLACE** | **+0.4** (P1) | Safer than Towel Chin-Up, fills 39 empty slots |
| 3 | **VPush** | Pike Push-Up | L2 | Bodyweight | **KEEP** | **+0.3** (P1) | Reduces 83% cross-family; quality improvement |
| 4 | **DLHD** | Glute Bridge March | L2 | Bodyweight | **KEEP** | **+0.2** (P1) | Reduces beginner/intermediate cross-family |
| 5 | **Ball** | Burpee / Tuck Jump | — | — | **REJECT** | 0.0 | Ball→Plyo cross-family is already credible |

**4 exercises added** (not 5-6). **Expected total credibility gain: +1.7.**

---

## 4. Additional Issues Discovered (Not RC2)

### RC5: "All" Optional Pool Bug (P0)

229 empty slots come from blueprints with `optional = ["All"]`:
- Youth Foundation
- Hypertrophy / Mass Accrual
- Mixed Modal (GPP)

The code replaces `"All"` with all 15 families, then randomly picks 0-2. But
some of those families (e.g., Ball for bodyweight) produce empty slots.

This is NOT a single exercise fix — it's a logic fix in `resolve_slot_families`.
Should be addressed independently.

### Exercise Overuse

**Band-Resisted Push-Up** appears 391× total (most-selected exercise) and appears
24× in a single Upper/Lower Split program (every session for 4 weeks). This is
because it's the only HPush bodyweight option at L3, and for advanced bodyweight
it's the ONLY option at L3+.

**Root cause:** Band-Resisted Push-Up (L3) has no L4+ bodyweight HPush
progression. One-arm push-up progressions would be L4 but don't exist in the DB.
This is separate from RC2.

---

## 5. Final Ranking by Coaching Credibility

| Priority | Fix | Impact | Effort | Type |
|----------|-----|--------|--------|------|
| **P0** | HPull L2 bodyweight (Table Row) | +0.8 | 1 row | Gap-fill |
| **P0** | RC5: "All" optional logic | +0.5 | 1 line | Logic fix |
| **P1** | VPull L2 band (Band Straight-Arm Pulldown) | +0.4 | 1 row | Gap-fill |
| **P1** | VPush L2 bodyweight (Pike Push-Up) | +0.3 | 1 row | Quality |
| **P1** | DLHD L2 bodyweight (Glute Bridge March) | +0.2 | 1 row | Quality |
| **P2** | Band-Resisted Push-Up L4 progression | +0.1 | 1 row | Completeness |
| **—** | Ball Burpee | 0.0 | Rejected | — |
| **—** | Towel Chin-Up | 0.0 | Replaced | — |

**Note:** Even with all RC2 fixes, 81 Core + 67 HPush + 64 DLHD advanced bodyweight
empty slots remain. These are expected — advanced bodyweight training rarely uses
those families in pure bodyweight form, and cross-family substitution handles
most of them.

---

## 6. Decision Record

| Exercise | Decision | Coach Would Prescribe? |
|----------|----------|----------------------|
| Glute Bridge March | ✅ Keep | Yes — common bridging progression |
| Burpee | ❌ Reject | Not credible as Ballistic |
| Burpee + Tuck Jump | ❌ Reject | Tuck Jump already in Plyo |
| Table Row | ✅ Keep | Yes — standard bodyweight row |
| Pike Push-Up | ✅ Keep | Yes — standard vertical push |
| Towel Chin-Up | ❌ Replace | Safety: door-dependent, fall risk |
| Band Straight-Arm Pulldown | ✅ Replace w/ | Yes — safe, universal, coach-common |
