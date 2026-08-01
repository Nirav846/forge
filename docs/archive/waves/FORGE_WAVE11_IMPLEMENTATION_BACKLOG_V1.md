# FORGE Wave 11 — Implementation Backlog

This backlog maps coach feedback to specific FORGE system areas. Each item is
grounded in the evidence matrix (`FORGE_COACH_FEEDBACK_EVIDENCE_MATRIX_V1.md`).
Items are organized by subsystem, then by priority within subsystem.

**Priority scale**:
- **P0**: Fix before next external coach trial. Trust-critical.
- **P1**: High-value but can follow initial fixes.
- **P2**: Important but not blocking.
- **P3**: Later enhancement.

---

## Exercise Selection Engine

### W11-001: Advanced bilateral lower-body exercise tier

| Field | Value |
|---|---|
| Priority | **P0** |
| Complexity | Small |
| Evidence | CF-001 (all 8 sports — Goblet Squat for advanced athletes) |
| Code area | `exercise_library` → level-based exercise tier mapping |

**Problem**: Advanced athletes (Training Age 5+ years, Strength Base Met = Yes)
receive Goblet Squats as a primary strength exercise. This is appropriate for
beginners/intermediates but signals the system doesn't understand high-performance
S&C.

**What needs to change**: The exercise selection engine needs a level-dependent
exercise progression rule for bilateral lower-body work:
- Beginner → Goblet Squat (or Air Squat → Goblet Squat within block)
- Intermediate → Goblet Squat or Barbell Back Squat (depending on equipment tier)
- Advanced → Barbell Back Squat OR Trap Bar Deadlift OR Front Squat

**Suggested approach**: Add an `advanced_bilateral_exercise` field to the role
profile or level config. When `training_age >= 5` and `level == "advanced"`,
default to Barbell Back Squat. Replace Goblet Squat in all exercise slots with
the appropriate variant.

**Validation**: Regenerate all advanced samples. Verify no Goblet Squat appears
in any advanced program. Run coach re-review on football/rugby advanced packs.

---

### W11-002: Deceleration/eccentric exercise family

| Field | Value |
|---|---|
| Priority | **P0** |
| Complexity | Medium |
| Evidence | CF-006 (7/8 sports — no deceleration or eccentric work) |
| Code area | `exercise_library` → add new exercise family; `session_assembly` → mandate inclusion |

**Problem**: Programs across all sports show zero eccentric or deceleration
exercises in many weeks. Football: "Week 2-8 all show 0 eccentric exercises —
where is the deceleration control work for high-speed running?" This is an
injury risk and a credibility gap.

**What needs to change**:
1. Add deceleration/eccentric as a recognized exercise family in the library
   (exercises: Nordic Curl, Single-Leg RDL, Eccentric Step-Down, Deceleration
   Drill, Lateral Bound with Stick, Single-Leg Landing Hold)
2. Mandate at least 1 eccentric/deceleration exercise per session for all
   programs with sprint or landing exposure above Moderate
3. For speed roles (Winger, Fullback, Back Three, Guard, Striker, Scrum Half),
   require 2+ eccentric exercises per week minimum

**Suggested approach**: Add `eccentric_focus` tag to exercises. In session
assembly, check total eccentric exposure for the week. If below threshold
(e.g., <2 sessions with eccentric work), insert from the family. Prioritize
Nordic curls for hamstring injury prevention.

**Validation**: Regenerate football/rugby samples. Verify eccentric exposure
is >0 in all weeks. Run injury prevention audit across all sports.

---

### W11-003: Plyometric progression pathway

| Field | Value |
|---|---|
| Priority | **P0** |
| Complexity | Medium |
| Evidence | CF-004 (all 8 sports — no plyometric progression) |
| Code area | `exercise_library` → plyometric tier system; `progression_engine` → plyometric advancement rules |

**Problem**: All levels receive the same plyometric exercises. No progression
from basic jump patterns to advanced reactive work. Coaches across all sports
independently note this as a significant gap.

**What needs to change**: Build a 3-tier plyometric progression:
- **Beginner**: Pogo Jumps, Box Step-Downs, Squat Jumps (low height, focus on
  landing mechanics)
- **Intermediate**: Box Jumps (controlled), Broad Jumps, Bounding, Med Ball
  Throws
- **Advanced**: Depth Jumps (12-24"), Single-Leg Hops, Lateral Bounds, Reactive
  Box Jumps, Single-Leg Landing Holds

Progression should be both across levels and within blocks (e.g., Pogo Jumps →
Squat Jumps by week 4 of a beginner block).

**Suggested approach**: Create a `plyometric_progression` config per sport with
tiered exercise lists. The session assembly engine selects from the appropriate
tier based on athlete level. Add a mid-block advancement trigger at week 4 where
appropriate.

**Validation**: Regenerate badminton/basketball samples. Verify plyometric
progression across Beginner→Intermediate→Advanced. Check that advanced
programs include depth jumps or single-leg variants, not just basic jumping.

---

## Role Modeling Engine

### W11-004: Bias-to-exercise-selection pipeline

| Field | Value |
|---|---|
| Priority | **P0** |
| Complexity | Large |
| Evidence | CF-002 (all 8 sports — role differentiation is bias-only) |
| Code area | `role_profiles` → `exercise_selection` pipeline |

**Problem**: Role bias values (velocity: 0.8, force: 0.6, rotation: 0.7, etc.)
are aspirational metrics that do not constrain exercise selection. A "rotation
emphasis 0.8" role gets the same exercises as a "rotation emphasis 0.2" role.
Exercise selection is shared across roles at the same level.

**What needs to change**: The pipeline from role profile → exercise selection
must be made causal. When a role has elevated rotation emphasis, the engine
should preferentially select rotational exercises (med ball throws, cable chops,
landmine rotations) and deprioritize non-rotational alternatives.

**Suggested approach**: Add a exercise-to-bias mapping layer. Each exercise is
tagged with its primary bias contribution (force, velocity, rotation, eccentric,
landing, conditioning). When assembling a session, the engine selects exercises
that match the role's bias profile. Roles with rotation >0.6 get mandatory
rotational exercise in each session.

**Minimum viable change**: Fix the most egregious gaps first — cricket rotation
emphasis, badminton singles vs doubles differentiation, basketball guard/wing/big
separation. Full exercise-to-bias mapping can follow.

**Validation**: Regenerate cricket samples. Verify Spin Bowler (rotation
emphasis 0.8) programs include rotational exercises. Regenerate basketball
samples. Verify Guard (velocity emphasis 0.8) programs differ materially from
Big (force emphasis 0.8).

---

### W11-005: Compound / dual-role support

| Field | Value |
|---|---|
| Priority | P2 |
| Complexity | Small |
| Evidence | CF-017 (cricket — all-rounder not represented) |
| Code area | `role_profiles` → compound role type |

**Problem**: Cricket all-rounder programs are "generic full-body strength
programs" that represent neither bowling nor batting demands. The role blends
requirements into an average rather than alternating focus.

**What needs to change**: Add a compound role type that alternates emphasis
across sessions within a microcycle rather than blending into a single profile.
Session A: bowling focus (eccentric, sprint). Session B: batting focus
(rotational power, upper-body ballistic).

**Validation**: Regenerate cricket all-rounder samples. Verify session-level
variation between bowling-specific and batting-specific profiles.

---

## Periodization Engine

### W11-006: In-season volume reduction rules

| Field | Value |
|---|---|
| Priority | **P0** |
| Complexity | Medium |
| Evidence | CF-003 (all 8 sports — in-season volume too high) |
| Code area | `periodization_engine` → seasonal context rules |

**Problem**: The seasonal context flag is set (Off-Season, Pre-Season, In-Season)
but does not alter programming parameters. In-season programs maintain the same
volume, frequency, and intensity as off-season programs.

**What needs to change**: Implement in-season-specific rules:
- **Frequency**: Reduce from 3-4x/week to 1-2x/week
- **Volume**: 2 working sets per exercise (from 3-4)
- **Intensity**: Maintain or increase intensity (keep RPE 7-9, drop volume)
- **Conditioning**: Remove or reduce to sport-practice only
- **Exercises per session**: Max 12-15 (from 18-24)
- **Pre-match**: Add activation protocol 24-48h before match
- **Post-match**: Add recovery protocol (low-intensity, mobility-based)

**Suggested approach**: Add an `in_season_volume_multiplier` to the block
configuration. Default 0.5 for sets and exercise count. Allow sport/role
overrides. Add pre/post match day awareness to the weekly scheduler.

**Validation**: Regenerate in-season samples for all sports. Verify volume
reduction. Run match-day scheduling tests. Coach re-review on rugby/football
in-season samples.

---

### W11-007: Replace "reduce families" with proportional volume reduction

| Field | Value |
|---|---|
| Priority | **P0** |
| Complexity | Small |
| Evidence | CF-013, CF-020 (badminton, basketball, cricket, rugby — chaotic week-to-week variation) |
| Code area | `auto_regulation` → impact response logic |

**Problem**: When the system detects "high impact" from a previous week, it
removes entire exercise categories (sprint, rotation, etc.) rather than
proportionally reducing volume. This causes chaotic programming where qualities
appear and disappear across weeks.

**What needs to change**: Replace the binary "reduce families" with a
proportional reduction:
- Reduce sets across ALL categories by 1 (not removing any entirely)
- Implement a floor: each category must appear in at least 1 session/week
- Log the reduction rationale
- Cap week-over-week volume swing at 30%

**Validation**: Regenerate badminton Doubles Intermediate A and basketball
Wing Intermediate A (the two samples explicitly flagged as chaotic). Verify
consistent category presence across all weeks.

---

### W11-008: Validation system auto-correction loop

| Field | Value |
|---|---|
| Priority | **P0** |
| Complexity | Large |
| Evidence | CF-005, CF-012 (5/8 sports — validation flags but no correction) |
| Code area | `validation` → `program_builder` / `session_assembly` feedback loop |

**Problem**: The validation system detects volume-load mismatches and emits
"Check volume load match: needs attention" warnings, but the program is
delivered with the mismatch intact. The feedback loop is informational only.

**What needs to change**: When a validation warning fires, the program builder
should:
1. Accept the validation output as a constraint input
2. Reduce sets/number of exercises in the overreaching categories
3. Re-validate the corrected program
4. Either output the corrected version OR include the warning as a visible
   header with the auto-correction already applied

**Minimum viable change**: Wire the volume-load match check into session
assembly. When total weekly volume-load exceeds the target by >20%, auto-reduce
by dropping 1 set from the accessory categories first, then secondary lifts.
Only then, if still mismatched, reduce primary lift sets.

**Validation**: Re-run validation on all previously flagged samples. Verify
"needs attention" count drops to 0 or near-0 (some edge cases may remain).
Coach re-review on previously flagged programs.

---

## Session Assembly / Exposure Balancing

### W11-009: Mandate injury prevention exercise families

| Field | Value |
|---|---|
| Priority | **P0** |
| Complexity | Small |
| Evidence | CF-009 (6/8 sports — no shoulder, hamstring, ACL prevention work) |
| Code area | `exercise_library` → injury prevention families; `session_assembly` → mandate rules |

**Problem**: No systematic injury prevention work appears across any sport.
Overhead sports lack shoulder external rotation. Speed sports lack Nordic curls.
Cutting sports lack ACL prevention. Collision sports lack neck/shoulder prehab.

**What needs to change**: Add mandatory injury prevention exercise families
per sport category:
- **Overhead sports** (badminton, tennis, volleyball, basketball): shoulder
  external rotation (band), YTWL, face pulls, scapular stability — 1 per session
- **Speed/cutting sports** (soccer, football, rugby backs): Nordic curls,
  single-leg landing progressions, COP drills — 2 per week minimum
- **Collision sports** (rugby forwards, football linemen): neck stability,
  shoulder prehab, deceleration absorption — 2 per week minimum
- **All sports**: groin strengthening (Copenhagen Adduction, etc.) for change-of-direction athletes

**Validation**: Regenerate all sport samples. Audit presence of injury
prevention exercises. Verify overhead sports have shoulder work, speed sports
have hamstring work, collision sports have neck/shoulder work.

---

### W11-010: Beginner within-block exercise progression

| Field | Value |
|---|---|
| Priority | P1 |
| Complexity | Small |
| Evidence | CF-010 (5/8 sports — beginner programs stagnate for 8 weeks) |
| Code area | `progression_engine` → within-block exercise advancement |

**Problem**: Beginner programs repeat the same exercises (Air Squat, Wall Push-Up)
across all 8 weeks with only set/rep changes. Coaches expect a progression
narrative even within beginner blocks.

**What needs to change**: Add a mid-block (week 4 or 5) exercise advancement
trigger. For beginner programs, this could be:
- Air Squat → Goblet Squat at week 4
- Wall Push-Up → Incline Push-Up at week 4
- Glute Bridge → Single-Leg Glute Bridge at week 4

**Validation**: Regenerate beginner samples. Verify exercise change at week 4+
in at least 50% of exercise slots.

---

### W11-011: Conditioning movement-pattern awareness

| Field | Value |
|---|---|
| Priority | P1 |
| Complexity | Medium |
| Evidence | CF-008 (6/8 sports — conditioning too linear) |
| Code area | `conditioning_engine` → protocol selection |

**Problem**: Conditioning protocols are selected purely by metabolic demand
(MAS, RSA, intervals) without considering the movement pattern. Court sports
get linear shuttle running instead of multi-directional work.

**What needs to change**: Add movement-pattern classification to conditioning
protocols:
- **Linear**: Straight-line runs, MAS shuttles
- **Multi-directional**: COD drills, lateral shuffles, carioca, defensive slides
- **Sport-pattern**: Block jumps (volleyball), approach jumps (volleyball),
  defensive shuffles (basketball), split-step + sprint (tennis)

Select protocols based on sport category first, then metabolic demand:
- Court sports (badminton, tennis, volleyball, basketball) → default to
  multi-directional
- Field sports (football, rugby, soccer) → mix linear and multi-directional
  based on role (backs: more multi-directional, forwards: more linear)

**Validation**: Regenerate court sport samples. Verify conditioning includes
multi-directional protocols, not only linear shuttles.

---

## Warm-up / Prep Logic

### W11-012: Session-aware dynamic warm-up generation

| Field | Value |
|---|---|
| Priority | P1 |
| Complexity | Medium |
| Evidence | CF-014 (football, rugby, volleyball — generic warm-ups) |
| Code area | `session_assembly` → warm-up generation |

**Problem**: Warm-ups are identical across roles and sessions regardless of
the session's emphasis, exercise selection, or intensity demands.

**What needs to change**: Build a warm-up generator that uses the session's
Raise/Activate/Potentiate structure but selects exercises based on:
- Primary movement patterns in the session (squat pattern → leg swings,
  hip openers; overhead work → shoulder activation)
- Landing/decel demands (if session has plyometrics → landing mechanics
  prep)
- Intensity (if session has heavy strength → low-intensity activation;
  if sprint session → progressively faster accelerations)
- Sport context (court sports get lateral movement prep, field sports get
  linear acceleration prep)

**Validation**: Generate warm-ups for contrasting sessions (heavy lower-body day
vs. sprint day). Verify content differs appropriately.

---

## Output / Serialization / Coach Delivery Layer

### W11-013: Credibility score sub-component breakdown

| Field | Value |
|---|---|
| Priority | P1 |
| Complexity | Small |
| Evidence | CF-019 (soccer, tennis, volleyball — score opacity) |
| Code area | `validation` → score serialization |

**Problem**: The credibility score is a single number (0.89, 0.93, 0.96, 1.0).
Coaches cannot see what drove the deduction.

**What needs to change**: Publish a score breakdown alongside the total:
- Volume-load match: score (e.g., 0.85) + brief explanation
- Exercise appropriateness: score
- Progression logic: score
- Role-specificity alignment: score
- Overall: computed as weighted average

**Validation**: Generate programs spanning the score range. Verify breakdown
is informative and actionable.

---

### W11-014: Sport-specific cue template layer

| Field | Value |
|---|---|
| Priority | P2 |
| Complexity | Small |
| Evidence | CF-011 (overall review, soccer, tennis, volleyball — generic cueing) |
| Code area | `output_serializer` → cue templating |

**Problem**: Cues like "Land soft, stick each rep" appear regardless of sport
context. A volleyball landing cue differs from a basketball landing cue.

**What needs to change**: Add a sport-context key to exercise cue metadata.
When generating output, select the cue variant matching the sport:
- Volleyball: "Absorb through hips and knees, reset for the next block jump"
- Basketball: "Absorb and immediately prepare for the next rebound or cut"
- General: "Land soft, stick each rep" (current fallback)

**Validation**: Generate volleyball and basketball programs for the same
exercise (Box Jump). Verify cue text differs by sport context.

---

## Infrastructure / Coach Workflow

### W11-015: Implement authentication/authorization

| Field | Value |
|---|---|
| Priority | **P0** |
| Complexity | Medium |
| Evidence | CF-018 (code review — no auth on API endpoints) |
| Code area | API layer → FastAPI security utilities |

**Problem**: API endpoints have no authentication or authorization. This is a
critical security gap for any production deployment.

**What needs to change**: Implement OAuth2 or JWT-based authentication using
FastAPI's built-in security utilities. Apply to all program generation, athlete
management, and assessment entry endpoints.

**Validation**: Automated auth tests for all endpoints. Penetration testing for
common auth bypass patterns.

---

### W11-016: Add CI/CD pipeline and test coverage

| Field | Value |
|---|---|
| Priority | P1 |
| Complexity | Medium |
| Evidence | CF-018 (code review — no CI/CD, limited test coverage) |
| Code area | Infrastructure → GitHub Actions / test framework |

**Problem**: No automated test execution, linting, or deployment pipeline.
Test coverage is limited to integration tests with no unit test suite for core
business logic.

**What needs to change**:
- Set up GitHub Actions workflow for PR checks (lint, typecheck, unit tests)
- Set coverage targets (minimum 70% for business logic modules)
- Add linting (ruff/flake8) and formatting (black) to CI
- Configure automated deployment for staging environment

**Validation**: CI passes on all PRs. Coverage reports meet threshold.
Deployment completes without manual intervention.

---

## Two-Track View

Items below are organized by track. **Coach-trust track** items must be fixed
before the next external coach trial. **Platform-track** items are necessary for
production deployment but do not affect coach-trial readiness.

### Coach-Trust Track — P0 (Fix before next external coach trial)
| ID | Title | Complexity |
|---|---|---|
| W11-001 | Advanced bilateral lower-body exercise tier | Small |
| W11-002 | Deceleration/eccentric exercise family | Medium |
| W11-003 | Plyometric progression pathway | Medium |
| W11-004 | Bias-to-exercise-selection pipeline | Large |
| W11-006 | In-season volume reduction rules | Medium |
| W11-007 | Replace "reduce families" with proportional reduction | Small |
| W11-008 | Validation system auto-correction loop | Large |
| W11-009 | Mandate injury prevention exercise families | Small |

### Platform Track — P0 (Required for production, not for coach trial)
| ID | Title | Complexity |
|---|---|---|
| W11-015 | Authentication/authorization | Medium |

Note: Platform-track P0 items are critical for security/stability but are not
coach-trial blockers. They belong in Wave 11C or later, not Wave 11A.

### P1 — High-value next wave (5 items)
| ID | Title | Complexity |
|---|---|---|
| W11-010 | Beginner within-block exercise progression | Small |
| W11-011 | Conditioning movement-pattern awareness | Medium |
| W11-012 | Session-aware warm-up generation | Medium |
| W11-013 | Credibility score sub-component breakdown | Small |
| W11-016 | CI/CD pipeline and test coverage | Medium |

### P2 — Important but not blocking (3 items)
| ID | Title | Complexity |
|---|---|---|
| W11-005 | Compound / dual-role support | Small |
| W11-014 | Sport-specific cue template layer | Small |

### P3 — Later enhancement
| ID | Title | Complexity |
|---|---|---|
| (future) | Sport-specific drill library | Large |
| (future) | Sport practice load integration | Large |
| (future) | Coach override / editing workflow | Large |
