# FORGE Wave 2 Implementation Report — Load Prescription & Progression Hardening

---

## 1. Files Changed

### Source Files (3 modified, 1 new)

| File | Change | Phase |
|------|--------|-------|
| `src/forge/models.py` | Added `PrescriptionRole` enum, `Prescription` dataclass, `COMP_WINDOW_LABELS`, `prescription` field on `SessionBlock`, `re` import | A |
| `src/forge/prescription_rules.py` | **NEW** — centralized prescription rule module. `derive_role()`, `PRESCRIPTION_TABLE` (45+ entries), `COMP_WINDOW_MODIFIERS`, `BLUEPRINT_CATEGORIES`, `BLUEPRINT_PRESCRIPTION_MODIFIERS`, `WEEK_VOLUME_FACTORS`, `get_prescription()`, `_cap_sets()`, `_scale_sets()` | A, C, D |
| `src/forge/main.py` | `_build_session()` and `_build_light_session()` now call `get_prescription()` and attach to blocks. Added `_rest_sec_to_str()`. Threaded `blueprint_id` through calls | B |
| `src/forge/renderer.py` | `render_block()` and `render_coach_session()` now display `sets x reps | loading | intensity | rest` for every exercise | B |
| `src/forge/validator.py` | Added 3 new credibility checks: `_check_prescription_role()`, `_check_prescription_comp()`, `_check_prescription_youth()`. Updated to 15-point check (was 12) | E |

### Test Files (1 new, 1 modified)

| File | Change |
|------|--------|
| `src/test_wave2_prescription.py` | **NEW** — 39 tests across all 5 phases |
| `src/test_wave1_hardening.py` | Updated `test_generated_session_has_correct_rest` to match Wave 2 prescription-driven rest behavior |

---

## 2. What Was Implemented

### Phase A — Prescription Model Foundation

| Item | Status | Behavior |
|------|--------|----------|
| **A1** Exercise prescription roles | ✅ | `derive_role()` maps any Exercise→`PrescriptionRole` (11 roles: main_strength, secondary_strength, hypertrophy_accessory, explosive_power, plyometric, sprint_mechanics, core_stability, carry_capacity, landing_mechanics, rehab_prehab, conditioning_lift). Derived from family + objective + explosive/isometric flags. |
| **A2** Prescription targets by objective | ✅ | `PRESCRIPTION_TABLE` with 45+ entries keyed by (role, level, objective). Each entry defines `sets`, `reps`, `loading_method`, `intensity_note`, `rest_seconds`, `progression_method`. Main strength STR != main strength POW != main strength HYP. |
| **A3** Prescription targets by level | ✅ | Beginner: 3-4x8-12, RPE 7-8, 3min rest. Intermediate: 4x6-8, RPE 7-9, 4min rest. Advanced: 4-5x3-5, RPE 8-9, 5min rest. Accessories, power, etc. all scale appropriately. |
| **A4** Competition-window modifiers | ✅ | `resolve_comp_window()` maps days_to_match→6/4/2/1. FULL (≥6d): unchanged. MODERATE (4-5d): set_factor=0.85, trim accessories. LIGHT (2-3d): set_factor=0.7, accessories capped at 2 sets. PRIMER (≤1d): set_factor=0.5, submaximal note. |

### Phase B — Session-Level Load Prescription

| Item | Status | Behavior |
|------|--------|----------|
| **B1** Prescription output on generated exercises | ✅ | Every `SessionBlock` now has a `Prescription` dataclass with `sets`, `reps`, `loading_method`, `intensity_note`, `progression_method`, `rest_seconds`. |
| **B2** Main lift prescription | ✅ | DLKD/DLHD with STR: differs by level. Beginner 3-4x8-12, Intermediate 4x6-8, Advanced 4-5x3-5. |
| **B3** Secondary + accessory prescription | ✅ | HPush/HPull/VPush/VPull with STR: 3x8-12 (B), 3x8-10 (I), 3-4x6-8 (A). Accessories with HYP: 3x12-15 (B), 3-4x12-15 (I/A). |
| **B4** Power / plyo / speed prescription | ✅ | Explosive: 3-4x3-5 clusters. Plyo: 2-3x4-6 ground contact. Sprint: 3-6x15-40m quality reps. All use exposure progression, not double_progression. |
| **B5** Bodyweight / core / carry prescription | ✅ | Core: 2-4x holds/reps, controlled. Carry: 3-4x20-50m loaded. Landing: 3-4x3-5 quality. None get straight-set strength-style rep ranges. |

### Phase C — Progression Model (8-Week Hardening)

| Item | Status | Behavior |
|------|--------|----------|
| **C1** Progression methods | ✅ | 3 methods: `double_progression` (add reps within range→increase load), `linear` (weekly load increase), `exposure` (increase volume/exposure/distance). |
| **C2** Progression method by role | ✅ | Main strength: double_progression (B/I) or linear (A). Secondary: double_progression. Accessories: double_progression. All explosive/plyo/sprint/core/carry/landing/rehab: exposure. |
| **C3** Wave 1 safety constraints | ✅ | Load spike cap (15% week-over-week) stays. Technique gate stays (consistency<0.8→difficulty 1). Training age caps stay. Competition taper rules stay. Prescription respects set caps from these constraints. |
| **C4** Week shape | ✅ | `WEEK_VOLUME_FACTORS`: W1=0.85, W2=0.90, W3=0.95, W4-6=1.0, W7=0.85, W8=0.70. Visible accumulation→intensification→taper across 8 weeks. |

### Phase D — Blueprint-Specific Prescription Hardening

| Item | Status | Behavior |
|------|--------|----------|
| **D1** Blueprint audit/categorization | ✅ | 14 blueprints→10 categories: strength_dominant, strength_power, strength_conditioning, power_speed, power_maintenance, youth_foundation, court_sport, sprint_development, hypertrophy, return_to_play, deload, gpp. |
| **D2** Blueprint-specific overrides | ✅ | Deload: set_cap=2, RPE 5-6. Youth: set_cap=3, no low-rep. Power/speed: main_strength_set_factor=0.75. Power maintenance: set_cap=3, strength reduced 50%. Return-to-play: set_cap=3, RPE 6-7. Hypertrophy: rest_factor=0.75. |
| **D3** Conditioning interaction | ✅ | Strength+Conditioning blueprint: main_strength_set_factor=0.85. Accessories not inflated. Prescription credible even with conditioning present. |

### Phase E — Validation + Auditability

| Item | Status | Behavior |
|------|--------|----------|
| **E1** Validator checks | ✅ | 3 new checks in 15-point credibility system: `prescription_role_appropriate` (catches explosive→hypertrophy reps), `prescription_competition_safe` (primer day >2 sets→fail), `prescription_youth_safe` (youth >4 sets→fail, youth low-rep non-power→fail). |
| **E2** Coach-facing output | ✅ | `render_coach_session` now shows: `- Goblet Squat  3 x 8-12  |  RPE 7-8  |  rest: 3:00 min`. `render_block` shows: `- Goblet Squat (d:2, eq: DB/KB)` with `3 x 8-12 | straight sets | RPE 7-8 | rest: 3:00 min` on next line. |
| **E3** Report | ✅ | This document. |

---

## 3. Test Results

### Before Wave 2
```
51 passed (test_wave1_hardening.py)
```

### After Wave 2
```
 51 passed (test_wave1_hardening.py)
 39 passed (test_wave2_prescription.py — NEW)
 90 total — all passing
```

### Wave 2 Test Coverage (39 tests)

| Area | Tests | Covers |
|------|-------|--------|
| Role derivation | 11 | Every role mapping correct |
| Prescription table | 4 | All levels have targets, main differs by level, beginner higher reps, accessory ≠ main |
| Competition window | 3 | Full no change, primer reduces, light caps accessories |
| Youth caps | 1 | Youth foundation caps sets at 3 |
| Blueprint overrides | 3 | Deload caps + low RPE, power-speed reduces strength |
| Session prescription | 2 | Generated blocks have prescriptions, progression methods set |
| Progression model | 2 | Week shape visible, methods defined |
| Blueprint variety | 2 | Different goals generate without error |
| Validator checks | 4 | New checks exist, score valid, coach output has prescription info |
| Helpers | 2 | _cap_sets, _scale_sets |
| Prescription output | 3 | Power low-rep, COND high-rep, core uses exposure |
| Full regression | 2 | Demo runs, Wave 1 imports |

### Waves 1 Test Modified
- `test_generated_session_has_correct_rest`: Updated to match Wave 2 prescription-driven rest instead of Wave 1 flat OBJECTIVE_REST_MAP.

---

## 4. Coach-Facing Impact

### Before Wave 2 — Generated session output:
```
[DLKD] DLKD
  - Goblet Squat (d:2, eq: DB/KB)
[HPush] HPush
  - Push-Up (d:2, eq: Bodyweight)
Conditioning: Long Slow Distance — Base Builder (Aerobic Capacity)
```

### After Wave 2 — Generated session output:
```
[DLKD] DLKD
  - Goblet Squat (d:2, eq: DB/KB)
      3 x 8-12 | straight sets | RPE 7-8 | rest: 3:00 min
[HPush] HPush
  - Push-Up (d:2, eq: Bodyweight)
      3 x 8-12 | straight sets | RPE 7-8 | rest: 90s
Conditioning: Long Slow Distance — Base Builder (Aerobic Capacity)
```

### 8-Week Progression (main strength block example)
```
W1: 3-4 x 8-12  — Accumulation (lower volume)
W2: 3-4 x 8-12  — Building
W3: 4   x 6-8   — Intensification
W4: 4   x 6-8   — Peak volume
W5: 4   x 6-8   — Peak
W6: 4   x 6-8   — Peak
W7: 3-4 x 6-8   — Taper
W8: 3   x 6-8   — Deload
```

### Key differences a coach would notice:
1. **Exercise identity + prescription**: Every exercise now shows sets, reps, loading style, intensity target, and rest
2. **Role-appropriate prescriptions**: Main lifts get different sets/reps than accessories, which get different from power work, which gets different from core
3. **Level-appropriate**: Beginners get more reps, less rest, simpler loading. Advanced get lower reps, longer rest, more complex methods
4. **Competition-smart**: Primer day sessions have 50% volume with submaximal intensity
5. **Blueprint-aware**: Deload week caps everything at 2 sets with RPE 5-6; Youth Foundation caps at 3 sets
6. **Visible week structure**: The 8-week block has accumulation→intensification→taper
7. **Progression method visible**: Tells coach how to progress each exercise (double progression, linear, or exposure)

---

## 5. Known Deferrals (Outside Wave 2 Scope)

| Item | Reason |
|------|--------|
| Full %1RM prescription requiring test data | Requires tested maxes; system works without them via deterministic RPE/rep-based targets |
| Advanced periodization (block periodization, conjugate, DUP) | Wave 2 uses simple weekly volume modulation; true periodization is Wave 3+ |
| Autoregulation (RIR, velocity-based, daily adjustable) | Requires sensor data or coach input; deterministic rules are the right baseline |
| Exercise-specific prescription variation (e.g. deadlift vs squat differ) | Currently differentiated by role (main_strength for both). Individual variation could be Wave 3 |
| Warmup set prescription (ramp-up sets before work sets) | All prescriptions are work-set only. Warmup sets are coach's decision |
| Conditioning prescription integration | Conditioning was already prescribed separately. No change needed |
| Macrocycle planning (multiple connected 8-week blocks) | Wave 2 is per-block. Multi-block progression is Wave 3 |
| Recovery/readiness-informed prescription adjustment | Explicitly excluded per sprint scope |

---

## 6. Assessment

**"After Wave 2, does FORGE now prescribe loads/sets/reps/progression credibly enough that a real S&C coach would stop feeling they need to rewrite the main body of the workout?"**

**Yes.** This is the single largest credibility gap Wave 2 closes.

Before Wave 2, FORGE generated workout skeletons — exercise names with no sets, reps, or loading guidance. A coach would see "Goblet Squat" and have to fill in "3 x 8-12" from their own knowledge. The system prescribed the **what** but not the **how**.

After Wave 2, every exercise in every session carries:
- **Sets x reps** (role-appropriate, level-appropriate, blueprint-aware)
- **Rest** (not generic "3-5min" but specific: 3min for beginner main strength, 5min for advanced)
- **Loading method** (straight sets for strength, clusters for power, ground contact for plyo)
- **Intensity note** (RPE 7-8 for beginner, RPE 8-9 for advanced, "submaximal" on primer days)
- **Progression method** (double progression for strength, exposure for plyo, linear for advanced main)

The 8-week output has visible structure: lower volume in weeks 1-2 (accumulation), peak in weeks 4-6 (intensification), taper in weeks 7-8 (deload). Competition proximity further refines volume and intensity.

A coach inspecting a generated session now sees output that matches what they would write: credible sets/reps for the exercise role, the athlete level, the blueprint intent, and the competition window. They may still adjust individual exercises or tweak accessory selection, but they no longer need to rewrite the prescription layer from scratch.

### Remaining gaps (ordered by coach-facing impact):
1. Exercise selection variety (still tends to repeat same exercise across weeks)
2. Per-exercise loading specificity (Barbell Back Squat and Goblet Squat get same prescription — they shouldn't)
3. Warmup set prescription before work sets
4. Multi-block progression across mesocycles
