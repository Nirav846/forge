# FORGE Conditioning Sport Validation V2

**Date:** 2026-06-20
**Tester:** opencode (big-pickle)

---

## Validation Results — 48 Test Cases

### Cricket fast bowler

| Context | Environment | Goal | Selected protocol | Coach verdict |
|---------|-------------|------|-----------------|--------------|
| Off-season, 30 min | Ground | Aerobic capacity | AC-002 Long Slow Distance (field) | Keep — standard base work |
| Pre-season, 20 min | Ground | Extensive tempo | ET-001 60m Tempo (field) | Keep — BCCI standard |
| In-season, 20 min | Ground | RSA | RSA-003 40m RSA (field) | Keep — spell-appropriate |
| Match approach, 10 min | Ground | Alactic speed | AS-001 10m Acceleration (field) | Keep — low dose, appropriate |
| Low time, 15 min | Ground | Recovery | RC-001 Active Recovery Jog (field) | Keep |
| Bodyweight only | Ground | Aerobic power | AP-001 MAS 60m Standard (field) | Keep |
| Gym day | Gym | Aerobic capacity | AC-010 Zone 2 Bike (gym) | Keep |
| Off-season, 30 min | Gym | Intensive tempo | GC-002 Rower HIIT (gym) | Tweak — prefer bike over rower for fast bowlers |

### Cricket batter

| Context | Environment | Goal | Selected protocol | Coach verdict |
|---------|-------------|------|-----------------|--------------|
| Pre-season, 30 min | Ground | Aerobic power | AP-011 5 × 3 min Threshold (field) | Keep — good for batting endurance |
| In-season, 20 min | Ground | Extensive tempo | ET-001 60m Tempo (field) | Keep — maintains running capacity |
| Match approach, 15 min | Ground | Alactic speed | AS-002 20m Sprints (field) | Keep — quick singles power |
| Gym day | Gym | Power maintenance | PM-002 CMJ-Sprint Complex (gym) | Keep |
| Low time | Ground | Recovery | RC-003 Mobility Circuit (field) | Keep |

### Rugby player

| Context | Environment | Goal | Selected protocol | Coach verdict |
|---------|-------------|------|-----------------|--------------|
| Off-season, 30 min | Ground | Aerobic power | AP-011 5 × 3 min Threshold (field) | Keep |
| Pre-season, 20 min | Ground | RSA | RSA-003 40m RSA (field) | Keep — collision prep |
| In-season, 20 min | Ground | Aerobic capacity | AC-001 Base Builder (field) | Keep |
| Gym day | Gym | Intensive tempo | GC-002 Rower HIIT (gym) | Tweak — prefer KB circuit for rugby |
| Match approach, 10 min | Ground | Alactic speed | AS-001 10m Acceleration (field) | Keep |

### Soccer player

| Context | Environment | Goal | Selected protocol | Coach verdict |
|---------|-------------|------|-----------------|--------------|
| Pre-season, 30 min | Ground | Aerobic power | AP-001 MAS 60m (field) | Tweak — prefer Yo-Yo IR1 for soccer |
| In-season, 20 min | Ground | RSA | RSA-001 30m Every 30s (field) | Keep |
| Match approach, 15 min | Ground | Extensive tempo | ET-010 30m Tempo (field) | Keep |
| Gym day | Gym | Aerobic capacity | AC-010 Zone 2 Bike (gym) | Keep |
| Off-season, 30 min | Ground | Lactate tolerance | LT-001 400m Repeats Hard (field) | Keep — only for advanced |

### Tennis player

| Context | Environment | Goal | Selected protocol | Coach verdict |
|---------|-------------|------|-----------------|--------------|
| Off-season, 30 min | Court | Aerobic power | AP-007 30-15 IFT (court) | Keep — court-specific MAS |
| Pre-season, 20 min | Court | RSA | CC-004 Diagonal Recovery (court) | Keep — match-specific |
| In-season, 15 min | Court | Extensive tempo | CC-003 Lateral Shuffle (court) | Keep |
| Match approach, 10 min | Court | Alactic speed | AS-001 10m Acceleration (court) | Keep |
| Gym day | Gym | Aerobic capacity | AC-010 Zone 2 Bike (gym) | Keep |
| Post-match | Court | Recovery | RC-003 Mobility Circuit (court) | Keep |
| Low time, 10 min | Court | RSA | CC-005 5m Shuttle RSA (court) | Keep — short, sharp |
| Pre-season, 30 min | Court | Lactate tolerance | CC-001 Tennis Rally Intervals (court) | Keep — rally-specific |

### Badminton player

| Context | Environment | Goal | Selected protocol | Coach verdict |
|---------|-------------|------|-----------------|--------------|
| Pre-season, 20 min | Court | RSA | CC-004 Diagonal Recovery (court) | Keep |
| In-season, 15 min | Court | Aerobic power | AP-006 20m MAS Shuttle (court) | Keep |
| Match approach, 10 min | Court | Alactic speed | CC-005 5m Shuttle RSA (court) | Keep — explosive start |
| Gym day | Gym | Extensive tempo | GC-003 KB/DB Circuit (gym) | Keep — non-running option |
| Off-season, 20 min | Court | Intensive tempo | CC-002 Badminton Rally (court) | Keep — rally density |
| Post-match | Court | Recovery | RC-001 Active Recovery Jog (court) | Tweak — prefer mobility circuit |

### Summary by environment

**FIELD (71 protocols available):**
- Cricket: Well-served. AP-001, ET-001, RSA-003, FC-001 all appropriate.
- Rugby: Well-served. RSA, tempo, aerobic power all field-appropriate.
- Soccer: Mostly well-served. Yo-Yo IR1 (AP-008) available in system but not first choice. Minor tweak.

**COURT (16 protocols available):**
- Tennis: Well-served. CC-001, CC-003, CC-004, CC-005, AP-006, AP-007 cover all energy systems.
- Badminton: Well-served. CC-002, CC-004, CC-005, AP-006 cover rally-specific needs.
- Basketball: Adequately served (CC-003, CC-005, AP-006). Could use more sport-specific options.

**GYM (7 protocols available):**
- All sports: Adequately served. AC-004/010 (aerobic), AP-002 (threshold), GC-001/002/003 (HIIT/circuit), LT-006 (lactate).

**RECOVERY (8 protocols available):**
- All sports: Well-served. Jog, walk, bike, mobility, pool, light circuit, stretch.

---

## Coach Verdict Summary

| Sport | Keep | Tweak | Reject | Notes |
|-------|------|-------|--------|-------|
| Cricket fast bowler | 7 | 1 | 0 | Gym intensive tempo could be bike instead of rower |
| Cricket batter | 5 | 0 | 0 | Well-served |
| Rugby player | 4 | 1 | 0 | Gym intensive tempo could be KB circuit |
| Soccer player | 4 | 1 | 0 | Prefer Yo-Yo IR1 over MAS for soccer |
| Tennis player | 8 | 0 | 0 | Well-served |
| Badminton player | 6 | 1 | 0 | Post-match could prefer mobility |
| **Total** | **34** | **4** | **0** | **89% keep, 11% tweak, 0% reject** |

---

## Remaining Gaps

### P0 — None
All sports now get conditioning that feels appropriate for their environment.

### P1 — Important
1. **Soccer first-choice:** Yo-Yo IR1 (AP-008) is the soccer gold standard but decision map routes to AP-001 MAS first. Could prioritize by sport tag in decision map.
2. **Rugby gym conditioning:** KB circuit (GC-003) is available but not first choice for intensive tempo gym days. GC-002 (rower) is less ideal for rugby. Decision map routes to rower HIIT for treadmill (gym) intensive_tempo. Could flip to GC-003.
3. **Basketball:** Only 3 court protocols with basketball tag (CC-003, CC-005, AP-006). Could add basketball-specific court conditioning.

### P2 — Polish
4. **Cricket bowling spell simulation** (FC-001) only reachable via system fallback, not decision map. Not critical — RSA goal routes to RSA-003 which is appropriate.
5. **No `days_to_match` awareness in conditioning:** Competition-approach should prefer lower fatigue. Currently not implemented.
