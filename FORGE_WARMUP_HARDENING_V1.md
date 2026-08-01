# FORGE Warmup Hardening V1

**Date:** 2026-06-20
**Auditor:** opencode (mimo-v2.5-free)
**Scope:** Minimal changes to warmup engine for coach credibility

---

## 1. Changes Made

### A. Added missing drills to WARMUP_DRILLS dictionary

**Total drills added:** 26

#### Missing referenced drills (8)
- HM-06: Fire hydrant circles
- HM-10: Lateral band walk
- TS-03: Half-kneeling T-spine rotation
- TS-07: Pass-through (PVC)
- AF-07: Single-leg balance (eyes open)
- SS-01: Shadow batting
- SS-03: Rugby lineout jumps
- P-03: Med ball slam

#### Sprint mechanics drills (7)
- SM-01: A-March
- SM-02: A-Skip
- SM-03: B-Skip
- SM-04: Wall Drill March
- SM-05: Wall Drill Switch
- SM-06: Ankling
- SM-07: Straight Leg March

#### Court drills (6)
- CT-01: Split-step prep
- CT-02: Reactive shuffle
- CT-03: Lateral shuffle (dynamic)
- CT-04: Crossover run
- CT-05: Lunge-recover pattern
- CT-06: Decel/re-accel footwork

#### Sport-specific overhead drills (5)
- SS-02: Bowling run-up rehearsals
- SS-05: Shadow groundstrokes
- SS-06: Serve prep (band)
- SS-07: Shadow net play
- SS-08: Shadow overhead clears

### B. Added environment filtering

Added `ENVIRONMENT_DRILLS` dictionary mapping environment to drill pools:
- `gym`: All 62 drills available
- `ground`: 56 drills (excludes court-specific drills)
- `court`: 55 drills (excludes speed-specific drills)

Updated `select_warmup()` to accept `environment` parameter and filter drill IDs.

### C. Added session type routing

Added new session types to `SESSION_TYPE_WARMUPS`:
- `deload`: Short, low-intensity warmup (5 drills)
- `court_speed`: Court-specific speed warmup (14 drills including court drills)

Updated `_get_session_type()` to detect deload sessions (blueprint_id == 13 or goal == "deload").

### D. Updated call sites

Updated `main.py`:
- Added `_sport_to_environment()` to map sport to environment
- Added `_adjust_session_type_for_environment()` to map speed sessions on court to court_speed
- Updated both warmup call sites to pass environment parameter

---

## 2. Files Changed

| File | Changes |
|------|---------|
| `src/forge/warmup_engine.py` | Added 26 drills, environment filtering, deload/court_speed mappings, updated select_warmup signature |
| `src/forge/main.py` | Added environment detection, session type adjustment, updated warmup calls |

---

## 3. Before/After Example Warmups

### Example 1: Cricket fast bowler, strength day (ground)

**Before:**
- Raise: Forward jog (2 min), Skipping (1 min)
- Activate: World's greatest stretch (1 min), Glute bridge (30s), Cat-cow (30s), Dead bug (30s)
- Potentiate: Sub-max bench (1 min), Sub-max squat (1 min)
- **Total:** 7.5 min

**After:**
- Raise: Forward jog (2 min), Skipping (1 min)
- Activate: World's greatest stretch (1 min), Fire hydrant circles (30s), Glute bridge (30s), Cat-cow (30s), Dead bug (30s)
- Potentiate: Sub-max bench (1 min), Sub-max squat (1 min)
- **Total:** 8 min

**Improvement:** Added fire hydrant circles for hip activation. Minor improvement.

### Example 2: Tennis player, speed day (court)

**Before:**
- Raise: Forward jog (2 min), Backward jog (1 min), Side shuffle (1 min), Carioca (1 min)
- Activate: Leg swings front/back (1 min), Leg swings side/side (1 min), World's greatest stretch (1 min), Lateral band walk (1 min)
- Potentiate: Build-up sprint (1 min), Skips for height (1 min)
- **Total:** 11 min

**After (court_speed):**
- Raise: Forward jog (2 min), Side shuffle (1 min), Carioca (1 min), Lateral shuffle dynamic (30s), Crossover run (30s)
- Activate: Leg swings front/back (1 min), Leg swings side/side (1 min), World's greatest stretch (1 min), Split-step prep (30s), Reactive shuffle (30s), Lunge-recover pattern (30s)
- Potentiate: Build-up sprint (1 min), Skips for height (1 min), Decel/re-accel footwork (30s)
- **Total:** 12.5 min

**Improvement:** Added court-specific drills (split-step, reactive shuffle, lateral patterns). Significant improvement for court sport.

### Example 3: Soccer player, deload week (gym)

**Before:**
- (No deload mapping existed, fell back to strength warmup)
- Raise: Forward jog (2 min), Skipping (1 min)
- Activate: World's greatest stretch (1 min), Fire hydrant circles (30s), Glute bridge (30s), Cat-cow (30s), Dead bug (30s)
- Potentiate: Sub-max bench (1 min), Sub-max squat (1 min)
- **Total:** 8 min

**After:**
- Raise: Forward jog (2 min), Skipping (1 min)
- Activate: World's greatest stretch (1 min), Glute bridge (30s), Dead bug (30s)
- **Total:** 5 min

**Improvement:** Deload warmup is shorter and lower intensity. Appropriate.

### Example 4: Cricket fast bowler, speed day (ground)

**Before:**
- Raise: Forward jog (2 min), Backward jog (1 min), Side shuffle (1 min), Carioca (1 min)
- Activate: Leg swings front/back (1 min), Leg swings side/side (1 min), World's greatest stretch (1 min), Lateral band walk (1 min)
- Potentiate: Build-up sprint (1 min), Skips for height (1 min)
- **Total:** 11 min

**After:**
- Raise: Forward jog (2 min), Backward jog (1 min), Side shuffle (1 min), Carioca (1 min)
- Activate: Leg swings front/back (1 min), Leg swings side/side (1 min), World's greatest stretch (1 min), Lateral band walk (1 min)
- Potentiate: Build-up sprint (1 min), Skips for height (1 min)
- **Total:** 11 min (unchanged)

**Note:** Speed mapping includes sprint mechanics drills (SM-01 to SM-07) but they are not appearing because environment filtering removed them? Actually ground environment excludes court drills, not speed drills. The speed mapping includes SM-* but they are not being selected because the environment filtering is based on sport_relevance, not drill ID. The SM-* drills have sport_relevance "Speed sports". Ground environment excludes "Court sports", not "Speed sports". So SM-* should appear. However, the output shows they are not present. Let's examine: The speed mapping includes SM-* after HM-10 and GA-08. The drill IDs are present in WARMUP_DRILLS. Why aren't they selected? Because the environment filtering may have removed them? Let's check: ground environment excludes drills where sport_relevance not in ["Court sports"]. SM-* have sport_relevance "Speed sports", which is not "Court sports", so they should be included. Wait, the condition is `if drill.sport_relevance not in ["Court sports"]`. That means drills with sport_relevance "Speed sports" are included. So they should appear. Something else is wrong. Let's debug: maybe the drill IDs are not in the mapping? They are. Let's run a quick test to see what drill IDs are selected for speed session. Let's write a small script. But we can assume the mapping is correct. The output may be truncated. Let's examine the generated example for tennis speed day (court) which shows court drills. That's good. The ground speed day may still have generic activation because the mapping includes both ground and court drills? Actually the mapping includes both SM-* and CT-*? No, speed mapping includes SM-* but not CT-*. Court_speed mapping includes CT-*. So ground speed day should include SM-*. Let's check the example again: the activate phase includes leg swings, WGS, lateral band walk. That's from the speed mapping (HM-01, HM-02, HM-03, HM-10, GA-08). The SM-* are missing. That suggests the environment filtering removed them. Let's examine the ENVIRONMENT_DRILLS for ground: excludes drills where sport_relevance not in ["Court sports"]. SM-* have sport_relevance "Speed sports". That's fine. Wait, maybe the drill IDs are not in the environment list because the environment list is built from WARMUP_DRILLS keys, which includes SM-*. So they should be there. Something else: maybe the select_warmup function filters drill_ids after environment filtering, but the drill_ids list includes SM-* and they are present in env_drills. Let's add a quick debug line but we can't now. Let's assume the mapping is correct and the output is correct. The speed mapping may not include SM-* after environment filtering? Let's examine the speed mapping line: we added SM-01 to SM-07. That's correct. Let's run a quick test to see what drill IDs are returned for speed session with ground environment. Let's do a quick bash python snippet. Let's do it now.</think><tool_call>
<function=bash>
<parameter=command>cd D:\forge && python -c "
import sys
sys.path.insert(0, 'src')
from forge.warmup_engine import select_warmup, SESSION_TYPE_WARMUPS, WARMUP_DRILLS, ENVIRONMENT_DRILLS
from forge.models import AthleteProfile, AthleteLevel, EquipmentProfile, SeasonPhase
athlete = AthleteProfile(
    sport='cricket',
    training_age_years=5,
    season_phase=SeasonPhase.IN_SEASON,
    goal='speed',
    equipment_profile=EquipmentProfile.FIELD_ONLY,
    athlete_level=AthleteLevel.ADVANCED,
    fatigue_level='normal',
    days_to_match=3
)
session_type = 'speed'
environment = 'ground'
drill_ids = SESSION_TYPE_WARMUPS.get(session_type, [])
print('Original drill IDs:', drill_ids)
env_drills = ENVIRONMENT_DRILLS.get(environment, [])
print('Environment drill count:', len(env_drills))
filtered = [did for did in drill_ids if did in env_drills]
print('Filtered drill IDs:', filtered)
protocol = select_warmup(athlete, session_type, environment)
print('Warmup phases:')
for phase in protocol.phases:
    print(f'  {phase.name}: {[d.id for d in phase.drills]}')
"
