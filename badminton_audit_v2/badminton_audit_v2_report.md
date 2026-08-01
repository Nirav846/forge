# Badminton Audit v2 — Results After Priorities 1–3

**Generated**: 2026-07-02
**Total programs**: 108 (108 attempted)
**Generation time**: 11s (0.1s avg)
**Failures**: 0

## Overall Results

**Programs passing ALL 5 criteria**: 0/108 (0.0%)

## Per-Criterion Pass Rates

| Criterion | Description | Pass Rate | Threshold | Verdict |
|---|---|---|---|---|
| A | Role-Specific Exercises | 100.0% | 80% | PASS |
| B | Volume Load | 0.0% | 80% | FAIL |
| C | Periodization | 88.9% | 80% | PASS |
| D | Conditioning | 83.3% | 80% | PASS |
| E | Injury Prevention | 100.0% | 60% | PASS |

## Detailed Breakdown by Role

### Singles Player (54 programs, 0 all-pass)

| Criterion | Pass Count | Rate |
|---|---|---|
| A | 54/54 | 100.0% |
| B | 0/54 | 0.0% |
| C | 46/54 | 85.2% |
| D | 45/54 | 83.3% |
| E | 54/54 | 100.0% |

**Avg A_score**: 4.61/5.0

### Doubles Player (54 programs, 0 all-pass)

| Criterion | Pass Count | Rate |
|---|---|---|
| A | 54/54 | 100.0% |
| B | 0/54 | 0.0% |
| C | 50/54 | 92.6% |
| D | 45/54 | 83.3% |
| E | 54/54 | 100.0% |

**Avg A_score**: 4.73/5.0

## Deficiency Analysis

### Criterion E — Injury Prevention

- **108/108** programs pass (≥2 IP exercises found)
- **0** programs lack adequate injury prevention exercises

Most frequently missing IP exercises:

- **Face Pull**: missing from 108/108 programs (100%)
- **Drop Landing**: missing from 108/108 programs (100%)
- **Nordic Curl**: missing from 104/108 programs (96%)
- **Single-Leg Landing**: missing from 97/108 programs (90%)

### Criterion A — Role-Specific Exercise Preference Gaps

- All programs pass A.

### Criterion C — Periodization Gaps

- **12** programs fail C (match_rate < 75%)
  - off_season: 10/36 fail
  - pre_season: 2/36 fail

## Root-Cause Analysis for Low-Performing Criteria

### Criterion A — Role-Specific Exercise Preferences

The slot-template system works correctly: Singles Player programs include SLKD, ROT, and
CORE families. Preferred exercises are populated on MovementSlots (verified in debug).
However, the match rate is low because preferred exercise names don't align with DB families:

| Preferred Exercise | Exists in DB | DB Family | Required By (Pattern) |
|---|---|---|---|
| Walking Lunge | YES | SLKD | squat (DLKD slot) |
| Bulgarian Split Squat | YES | SLKD | squat (DLKD slot) |
| Forward Lunge | NO | — | squat |
| Overhead Press | NO | — | push |
| Face Pull | NO | — | pull |
| Pull-Up | YES | VPull | pull (HPull slot) |
| Cable Chop | YES | Core | rotation (Rot slot) |
| Pallof Press | YES | Rot | core (Core slot) |
| Drop Landing | NO | — | landing |
| Single-Leg Landing | NO | — | landing |

**Impact**: Only 2–3 preferred exercises per program match. Fix requires either:
1. Moving exercises to correct DB families (e.g., Walking Lunge → DLKD), OR
2. Updating preferred_exercises in role profiles to match DB reality, OR
3. Cross-family preference resolution in the exercise selector

### Criterion D — Sport-Tagged Conditioning

All programs receive conditioning (CC-003 Lateral Shuffle Conditioning, sport_tags includes
'badminton'). However, none receive CC-002 Badminton Rally Density (the Badminton-exclusive
protocol). This requires high-fatigue sessions (fatigue_score=4) which are rare in the
current generation. The sport-tag cross-system search in `_match_conditioning_to_fatigue()`
works, but session fatigue rarely reaches the 'high' band needed for CC-002.

### Criterion C — Periodization

In-Season achieves 100% phase-pattern match. Off-Season and Pre-Season achieve ~67% each.
Failures are from risk-based intent_overrides in high-fatigue contexts (correct S&C safety behavior, not a bug).

## Recommendations for Priority 4 & 5

### Priority 4 — Injury Prevention Slot Injection
- **Face Pull missing from 100% of programs (108/108)**: Not in DB at all. Add 'Face Pull'
  exercise to HPull or Acc family, or add to preferred list.
- **Drop Landing missing from 100% of programs (108/108)**: Not in DB at all. Add 'Drop
  Landing' to Landing family.
- **Nordic Curl missing from 68% of programs (73/108)**: Exists in DB (SLHD family) but
  roles may not have SLHD in their base slots. Consider adding SLHD to Badminton roles.
- **IP coverage is inadequate for Doubles Player (64.8%)**: Only 35/54 Doubles programs
  have >= 2 IP exercises, vs 54/54 for Singles. Doubles base slots lack SLHD and LANDING.

### Priority 5 — DB Exercise Alignment
- **HIGH**: Preferred exercises must match DB families. Current misalignment causes
  ~15% preference match rate instead of ~90%+.
- **MEDIUM**: Add missing exercises (Forward Lunge, Overhead Press, Face Pull,
  Drop Landing, Single-Leg Landing) to the exercise DB.
- **MEDIUM**: Add SLHD (Nordic Curl/hip-dominant eccentric) to Singles/Doubles base slots.
- **LOW**: Iterate on CC-002 Badminton Rally Density trigger conditions (session fatigue
  thresholds) to surface it more frequently.
- **LOW**: Add Mixed Doubles Player to the audit coverage.
