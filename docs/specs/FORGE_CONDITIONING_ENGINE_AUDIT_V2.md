# FORGE Conditioning Engine Audit V2

**Date:** 2026-06-20
**Auditor:** opencode (big-pickle)
**Scope:** Full audit of conditioning_data.py (91 protocols), conditioning_engine.py, and integration in main.py

---

## 1. Current Taxonomy

### How protocols are classified
Protocols are grouped by **energy system** into 10 categories:

| Category | Count | ID Range |
|----------|-------|----------|
| Aerobic Capacity | 12 | AC-001 to AC-012 |
| Aerobic Power | 11 | AP-001 to AP-011 |
| Extensive Tempo | 10 | ET-001 to ET-010 |
| Intensive Tempo | 8 | IT-001 to IT-008 |
| Repeated Sprint Ability | 11 | RSA-001 to RSA-011 |
| Speed Endurance | 9 | SE-001 to SE-009 |
| Alactic Speed | 8 | AS-001 to AS-008 |
| Lactate Tolerance | 9 | LT-001 to LT-009 |
| Power Maintenance | 7 | PM-001 to PM-007 |
| Recovery Conditioning | 6 | RC-001 to RC-006 |

### How the engine chooses a protocol
The selection flow in `select_conditioning()`:

1. **Guard checks**: Beginner skips intensive_tempo; non-Advanced skips lactate_tolerance
2. **Decision map lookup**: `_lookup_decision_map(goal, environment, time_available)` → returns protocol_id if match found
3. **Fallback**: If decision map fails, select by energy system:
   - Filter by system name (goal → system map)
   - Filter by tier (prefer A)
   - Filter by level
   - Filter by environment match (partial string match against protocol.environment list)

### Selection dependencies

| Input | Used? | How |
|-------|-------|-----|
| goal | Yes | Maps to energy system, then decision map key |
| environment | Partial | Decision map uses field/track/treadmill/indoor/limited_space. Fallback does partial string match. **No court environment in decision map.** |
| session type | No | Not directly referenced |
| sport | **No** | **Not used anywhere** |
| athlete level | Yes | Guard checks + level filter + level_variants adjustment |
| available time | Yes | Decision map key (10/20/30/45 min) |
| days_to_match | No | Not referenced in conditioning engine |

---

## 2. Environment Realism

### FIELD conditioning
Current protocols: AC-001/002/003/005/011/012, AP-001/003/008/011, ET-001 through ET-010, RSA-001/002/003/004/006/007/010, SE-005/007, AS-001/002/003/005/006/008, LT-009, PM-001/002/003/006, RC-001

**Typical output for generic field athlete, aerobic_capacity goal, 30min:**
→ AC-001 "Long Slow Distance — Base Builder" (20-30 min continuous run)

**Problem:** A cricket fast bowler and a soccer midfielder get the same protocol.

### COURT conditioning
Current protocols with `"Court"` in environment field: AP-006 (20m MAS Shuttle), AP-007 (30-15 IFT), AP-008 (Yo-Yo IR1), RSA-005 (20m Shuttle RSA), RSA-008 (Agility 4×10m), RSA-009 (10m Shuttle RSA — Court Sport), RSA-011 (Direction Change RSA), AS-001 (10m Acceleration), AS-007 (15m Ball Start Sprints), PM-005/006

**But the decision map has NO "court" environment key.** Court environment string falls through to fallback which does `environment.lower() in e.lower()` — e.g., "court" matches protocols listing "Court" in their environment list.

**Typical output for court sport, aerobic_power goal, 30min:**
→ Decision map "indoor" → AP-007 (30-15 IFT) or fallback → AP-001 (MAS 60m Standard — track/field protocol)

**Problem:** No court-specific routing. Court athletes may get field protocols.

### GYM conditioning
Protocols with `"Gym"` environment: AC-004 (Cross-Training Aerobic), AC-010 (30-Minute Zone 2 Bike), AP-002 (Treadmill Threshold Intervals), LT-006 (Treadmill Over-Unders), RC-005 (Cycling Recovery), PM-002/003/004/007

**Problem:** Only 4 gym-specific aerobic/power/tempo options. No KB/DB circuits, no rower HIIT, no bike HIIT.

### RECOVERY conditioning
RC-001 through RC-006: Active Recovery Jog, Recovery Walk, Mobility Circuit, Aqua Jogging, Cycling Recovery, Light Stretch Circuit.

**Problem:** All passive or low-intensity aerobic only. No low-fatigue conditioning options that maintain work capacity.

---

## 3. Sport Realism

### Cricket fast bowler
- **Current output (goal: conditioning → aerobic_power, field, 20-30min):** AP-001 MAS 60m Standard or generic field tempo
- **Coach would:** Reject. Fast bowlers need intermittent high-intensity with incomplete recovery (simulating spell demands), not straight-line MAS.
- **Missing:** Bowling-spell simulation intervals, multi-directional RSA with decel emphasis, variable recovery conditioning.

### Cricket batter
- **Current output (goal: speed → alactic_speed, field, 20min):** AS-002 20m Sprints
- **Coach would:** Accept for speed work but reject for conditioning days. Batter needs longer intermittent efforts with explosive singles/twos.
- **Missing:** Intermittent high-intensity with walking recovery (simulating running between wickets).

### Rugby player
- **Current output (goal: conditioning → aerobic_power, field, 30min):** AP-001 MAS 60m or AP-003 1 km Repeats
- **Coach would:** Reject for specificity. Rugby needs high-intensity intermittent with collision simulation (bodyweight circuits, wrestling drills).
- **Missing:** Rugby-specific intermittent conditioning, contact-readiness circuits (bodyweight only, no contact drill requirement).

### Soccer player
- **Current output (goal: conditioning → aerobic_power, field, 20min):** AP-001 or AP-003
- **Coach would:** Partially accept. Yo-Yo IR1 (AP-008) is soccer-standard but only selected by fallback. Decision map doesn't route to it.
- **Missing:** Yo-Yo IR1 should be first choice for soccer. Small-sided games conditioning format.

### Tennis player
- **Current output (goal: conditioning → aerobic_power, court, 30min):** Falls to "indoor" in decision map → AP-007 (30-15 IFT) or fallback → AP-001 (field MAS)
- **Coach would:** Reject. Court athlete gets field protocol. Tennis needs 10-15s efforts, 20s rest, multi-directional.
- **Missing:** Tennis rally simulation (10-15s work, 20s rest), lateral shuffle intervals, diagonal recovery conditioning.

### Badminton player
- **Current output (goal: conditioning → aerobic_power, court, 20min):** Same as tennis — 30-15 IFT or generic field.
- **Coach would:** Reject even more strongly than tennis. Badminton is 5-10s rallies, 15-20s rest, extreme directional changes.
- **Missing:** Badminton rally simulation (5-10s, multi-directional explosive), split-step density conditioning, court coverage patterns.

---

## 4. Dead / Weak Protocol Categories

### Overloaded with generic field work
- **Aerobic Capacity (12 protocols):** AC-001/002/003/004/005/006/007/008/009/010/011/012 — all continuous running or basic intervals. No court differentiation.
- **Extensive Tempo (10 protocols):** ET-001/002/003/004/005/006/007/008/009/010 — all straight-line running on field/track. Cricket Ground Circuit (ET-006) is the only sport-specific one.
- **Intensive Tempo (8 protocols):** All track-based. No court or field sport variation.

### Too thin for court sports
- **Repeated Sprint Ability:** RSA-009 (10m Shuttle RSA — Court Sport) is the only court-specific one. But its environment is `["Court"]` so field sports can't reach it.
- **Aerobic Power:** AP-006 (20m MAS Shuttle), AP-007 (30-15 IFT), AP-008 (Yo-Yo IR1) have court in environment but are tier B.

### Recovery too shallow
- 6 protocols: jog, walk, mobility, aqua jog, bike, stretch
- No "low-fatigue conditioning" (e.g., light KB circuit, bike tempo at low intensity)

### Unreachable protocols
- **IT-002 Descending Ladder (tier C):** Advanced to Elite only, niche
- **IT-007 Pyramid (tier C):** Same
- **IT-008 Negative Split 800s (tier C):** Same
- **AS-005 Contrast Sprints (tier C):** Needs sled equipment
- **PM-007 Hurdle Hop (tier C):** Niche
- **RSA-010 German Volume RSA (tier C):** High volume, rare use
- **LT-003 Broken 800m and LT-005 Short-Long-Short (tier C):** Complex, hard to coach

### Duplicate/near-duplicate
- **AC-006 (2 km Continuous Timed)** and **AC-009 (2 km Run Assessment):** Nearly identical. AC-009 is a maximal test version of AC-006's steady effort.
- **AC-001 (Base Builder)** and **AC-002 (Aerobic Volume):** Different only by duration/volume. Could be variants of same protocol.

---

## 5. Gap Ranking

### P0 — Materially weak / coach-facing miss

| Gap | Why it matters | How often it affects output | Smallest viable fix |
|-----|---------------|---------------------------|-------------------|
| No court environment in decision map | Court athletes get field protocols | Every court sport session | Add "court" key to decision map |
| No sport differentiation — all field sports get same protocols | Cricket, rugby, soccer coaches would reject generic output | Every conditioning session | Add sport_tags to protocols + filter by sport |
| No court-specific conditioning protocols | Tennis/badminton get field intervals | Every court sport session | Add 4-6 court-specific protocols |

### P1 — Important specificity gap

| Gap | Why it matters | How often it affects output | Smallest viable fix |
|-----|---------------|---------------------------|-------------------|
| Gym conditioning is thin (4 options) | Athletes on gym days get field protocols | Every gym environment session | Add 2-3 gym-specific protocols (bike HIIT, KB circuit, rower) |
| Recovery conditioning is passive only | No active recovery that maintains capacity | Every recovery day | Add 1-2 low-fatigue conditioning options |
| Speed Endurance has no A-tier | Selection logic prefers A-tier, never picks speed endurance unless fallback | Never (no A-tier to pick) | Promote 1-2 SE protocols to A-tier |

### P2 — Polish

| Gap | Why it matters | How often it affects output | Smallest viable fix |
|-----|---------------|---------------------------|-------------------|
| AC-006/AC-009 near-duplicate | Confusing redundancy | Rare — both tier A, only one selected | Merge or mark one as alternative |
| SE category has only environment=["Track"] for 7/9 protocols | Field athletes never get speed endurance work | Most field sessions | Add "Field" to SE-001/003/006/008/009 environment lists |
| No days_to_match awareness | Competition-approach conditioning should differ from off-season | Every in-season session | Use days_to_match to prefer lower-fatigue protocols near competition |
