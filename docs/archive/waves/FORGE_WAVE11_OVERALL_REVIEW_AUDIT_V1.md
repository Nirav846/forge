# FORGE Wave 11 — overall_review.txt Audit

Audit of how `sample/overall_review.txt` was used (or misused) in the 4 Wave 11
planning documents.

---

## Section 1 — What overall_review.txt Actually Says

The file has two clearly separated halves, split at line 111:

- **Lines 1–110**: Coach / program-quality / product feedback from an NSCA-CSCS
  certified S&C coach and sports scientist.
- **Lines 112–377**: Code review report (FastAPI, architecture, testing, config,
  security, maintainability).

### All Findings from Lines 1–110 (Coach Feedback)

| # | Finding | Classification | Severity | Implementation Relevance |
|---|---------|---------------|----------|-------------------------|
| F01 | Role-specific differentiation is a strength | COACH_PROGRAMMING (praise) | N/A | N/A — existing strength |
| F02 | Adaptive periodization / Adj column is a strength | COACH_PROGRAMMING (praise) | N/A | N/A — existing strength |
| F03 | Exposure tracking (density metrics) is a strength | COACH_PRODUCT (praise) | N/A | N/A — existing strength |
| F04 | Transparent rationale sections build trust | COACH_PRODUCT (praise) | N/A | N/A — existing strength |
| F05 | No explicit load management metrics (volume-load, monotony, strain) | COACH_PRODUCT | Medium | Later |
| F06 | Limited exercise progression — beginner programs repeat same exercises for 8 weeks | COACH_PROGRAMMING | Medium | Wave 12+ |
| F07 | Generic cueing — "Land soft, stick each rep" too vague | COACH_PRODUCT | Low | Later |
| F08 | In-season volume too high — 3x/week heavy strength in competition phase | COACH_PROGRAMMING | Critical | Wave 11A |
| F09 | No integration with sport practice load (on-court training) | COACH_PRODUCT | Medium | Later |
| F10 | Sport-specific exercise additions recommended (volleyball: 7, tennis: 7, soccer: 7 exercises) | COACH_PRODUCT | Medium | Later |
| F11 | Enhanced sport-specific cueing examples (6 cue transformations) | COACH_PRODUCT | Low | Later |
| F12 | Exercise dropdown / progression tiers UI feature request | COACH_PRODUCT | Medium | Later |
| F13 | Load management / periodization controls feature request | COACH_PRODUCT | Medium | Later |
| F14 | Workout structuring tools (warm-up builder, duration slider, intensity zones) | COACH_PRODUCT | Medium | Later |
| F15 | Sport practice load integration feature request | COACH_PRODUCT | Medium | Later |
| F16 | Data visualization / reporting feature request | COACH_PRODUCT | Low | Later |

### All Findings from Lines 112–377 (Code Review)

| # | Finding | Classification | Severity | Implementation Relevance |
|---|---------|---------------|----------|-------------------------|
| F17 | Overall rating 7.5/10 — solid foundation | PLATFORM_ENGINEERING | N/A | N/A — summary |
| F18 | Inconsistent import styles (absolute vs relative) | PLATFORM_ENGINEERING | Low | Later |
| F19 | Magic numbers / hardcoded values in calculate_reps_and_intensity | PLATFORM_ENGINEERING | Medium | Later |
| F20 | Missing type hints in some functions | PLATFORM_ENGINEERING | Low | Later |
| F21 | Long functions (calculate_reps_and_intensity >40 lines) | PLATFORM_ENGINEERING | Medium | Later |
| F22 | Insufficient error handling — generic try/except blocks | PLATFORM_ENGINEERING | High | Later |
| F23 | Missing business-level input validation | PLATFORM_ENGINEERING | Medium | Later |
| F24 | No circuit breaker or retry logic for DB connections | PLATFORM_ENGINEERING | Medium | Later |
| F25 | Limited test coverage — integration-only, no unit test suite | PLATFORM_ENGINEERING | High | Later |
| F26 | No CI/CD pipeline | PLATFORM_ENGINEERING | Medium | Later |
| F27 | No code linting or formatting | PLATFORM_ENGINEERING | Low | Later |
| F28 | Hardcoded feature flags without validation | PLATFORM_ENGINEERING | Low | Later |
| F29 | No authentication / authorization on API endpoints | PLATFORM_ENGINEERING | **Critical** | Wave 11C (if production) |
| F30 | No rate limiting | PLATFORM_ENGINEERING | Medium | Later |
| F31 | Database query optimization — no application-layer optimization | PLATFORM_ENGINEERING | Medium | Later |
| F32 | No caching layer for frequently accessed data | PLATFORM_ENGINEERING | Medium | Later |
| F33 | Scattered configuration across codebase | PLATFORM_ENGINEERING | Medium | Later |
| F34 | No environment-specific configurations | PLATFORM_ENGINEERING | Low | Later |
| F35 | Missing inline documentation / docstrings | PLATFORM_ENGINEERING | Low | Later |
| F36 | No custom API documentation beyond auto-generated OpenAPI | PLATFORM_ENGINEERING | Low | Later |
| F37 | Priority recommendations: auth, error handling, test coverage, CI/CD | PLATFORM_ENGINEERING | Various | See individual |

---

## Section 2 — Audit of the 4 Wave 11 Docs

### 2a. Evidence Matrix (`FORGE_COACH_FEEDBACK_EVIDENCE_MATRIX_V1.md`)

#### Correct uses
- **CF-003** (in-season volume) — correctly cites `overall_review.txt:22` (F08).
  Classification is correct (programming logic / periodization engine). ✓
- **CF-007** (sport-specific drills) — correctly cites `overall_review.txt:26` (F10).
  Classification is correct (exercise selection / missing library). ✓
- **CF-010** (beginner stagnation) — correctly cites `overall_review.txt:18` (F06).
  Classification is correct (programming logic / progression engine). ✓
- **CF-011** (generic cueing) — correctly cites `overall_review.txt:20` (F07).
  Classification is correct (presentation / UX). ✓
- **CF-015** (practice load) — correctly cites `overall_review.txt:24` (F09).
  Classification is correct (system architecture). ✓
- **CF-018** (code quality) — correctly cites `overall_review.txt:112-377` (F17-F37).
  Classification is correct (system architecture / engineering). ✓

#### Omissions
- `overall_review.txt`'s praise findings (F01–F04) are not represented as evidence
  rows. This is acceptable — the evidence matrix is problem-focused and strengths
  are covered in the synthesis doc.
- F05 (no load management metrics) is not represented. This is a product feature
  request, not a programming fix. Omission is reasonable for a Wave 11
  programming-focused plan.
- F12–F16 (product feature requests) are not represented. Omission is reasonable.
- F19 (magic numbers), F21 (long functions), F22 (error handling), F23 (validation),
  F25 (test coverage), etc. — none are individually represented. Instead, they
  are aggregated into CF-018. This is correct — none of these merit standalone
  evidence rows in a coach-programming-focused plan.

#### Misclassifications
- None. CF-003, CF-007, CF-010, CF-011, CF-015, CF-018 are all correctly scoped.
- However, the evidence matrix **does not explicitly tag which rows come from**
  **`overall_review.txt`'s coach feedback** vs **platform/code-review feedback**.
  CF-018 could be misinterpreted as a "coach-facing" concern. A reader glancing
  at the table might not realize CF-018 is a platform/engineering item.

#### Priority distortion
- **None observed.** CF-003 (in-season volume, Critical) correctly outranks
  CF-018 (code quality, High). Coach-trust items dominate the severity ranking.

---

### 2b. Synthesis (`FORGE_WAVE11_COACH_FEEDBACK_SYNTHESIS_V1.md`)

#### Correct uses
- The synthesis uses `overall_review.txt` as a secondary source (cited in
  strengths, weaknesses, and trust-breaking sections).
- F08 (in-season volume) is correctly cited as a trust-breaking issue.
- F06 (beginner stagnation) is correctly cited as a weakness.
- F07 (generic cueing) is correctly cited as cosmetic/small fix.

#### Omissions
- The code review section (F17–F37) is not mentioned. This is **correct** — the
  synthesis is explicitly a "coach feedback synthesis." Platform engineering
  feedback does not belong in the primary narrative.
- However, the synthesis does not acknowledge that `overall_review.txt` contains
  platform feedback that was intentionally excluded. A brief note would improve
  transparency.

#### Misclassifications
- None. The synthesis correctly keeps the narrative focused on coach-facing
  programming issues.

#### Priority distortion
- **None observed.** The 5 trust-breaking issues (Section 4) are all
  COACH_PROGRAMMING. No platform item appears in the "Must fix before next
  trial" list (Section 7).

---

### 2c. Implementation Backlog (`FORGE_WAVE11_IMPLEMENTATION_BACKLOG_V1.md`)

#### Correct uses
- W11-001 through W11-014 all cite evidence matrix IDs that draw from
  `overall_review.txt` where appropriate.
- W11-015 and W11-016 correctly cite CF-018 (code review section).

#### Omissions
- No specific backlog item for F05 (load management metrics). This is a product
  feature, not a programming fix — omission is reasonable.
- No specific backlog item for F12–F16 (feature requests). These are UI/product
  items — omission is reasonable.

#### Misclassifications
- **Minor**: The "Summary by Priority" section (line 483+) lists W11-015 (auth)
  in a P0 footnote alongside W11-007 and W11-009. While W11-007 and W11-009 are
  coach-trust items, W11-015 is a platform/engineering item. The footnote
  groups them together without distinguishing the track. This could cause a
  reader to think auth is a Wave 11A priority.

#### Priority distortion
- **Minor distortion observed.** The P0 table (lines 483–493) lists:
  1. W11-001 (coach) ✓
  2. W11-002 (coach) ✓
  3. W11-003 (coach) ✓
  4. W11-004 (coach) ✓
  5. W11-006 (coach) ✓
  6. W11-008 (mixed — has coach-facing dimension) ✓
  
  The "Also" footnote adds W11-007, W11-009, and W11-015. W11-015 (auth) is
  the only platform item. It is correctly marked as conditional ("if production
  deployment is in scope"). However, the placement in a "P0 — Fix before next
  external coach trial" section implies auth might be a coach-trial blocker.
  **It is not.** A coach does not care about JWT tokens.
  
  **Correction needed**: Move W11-015 out of the P0 coach-trial section or
  add an explicit two-track label.

---

### 2d. Post-Review Roadmap (`FORGE_POST_REVIEW_ROADMAP_V1.md`)

#### Correct uses
- Wave 11A (trust-critical coach fixes) contains only W11-001, 006, 007, 009 —
  all COACH_PROGRAMMING. ✓
- Wave 11B (role specificity) contains W11-004, 003, 002 — all
  COACH_PROGRAMMING. ✓
- Wave 11C contains W11-008 (mixed), W11-015 (platform), W11-016 (platform).
  These are correctly grouped as a combined validation+infra wave. ✓
- The "What Can Be Shown to Coaches After Each Wave" table correctly maps
  coach-facing capability. ✓

#### Omissions
- No explicit statement that Waves 11B and 11A can proceed without 11C (infra).
- The roadmap implies a sequential dependency (11A → 11B → 11C → 12 → 13).
  In reality, 11C's auth and CI/CD items are parallel tracks that don't block
  the coach-trust items. This could cause a team to think they must complete
  auth before showing Wave 11A output to a coach.

#### Misclassifications
- None. The wave grouping is correct.

#### Priority distortion
- **None observed.** Wave 11A (the earliest wave) is 100% coach-trust programming
  items. Platform items are correctly deferred to Wave 11C.

---

## Section 3 — Final Verdict

### PASS WITH CORRECTIONS

The original Wave 11 docs **did** use `overall_review.txt` correctly in the
fundamental sense: coach-priority programming issues are not diluted by
platform/code-review feedback. All four docs keep the primary focus on
coach-trust items.

However, three minor issues need surgical correction:

1. **Evidence Matrix**: CF-018 does not explicitly tag itself as a
   PLATFORM_ENGINEERING item. A reader could misinterpret it as coach-facing.
2. **Implementation Backlog**: The P0 section (lines 483–493) groups W11-015
   (auth — platform) with coach-trust items without track separation, implying
   auth is a coach-trial blocker.
3. **Roadmap**: No explicit parallel-track view showing that platform/infra
   items are not sequential dependencies.

These are transparency issues, not priority distortions. The Wave 11A plan
remains coach-first.

---

## Section 4 — Required Corrections Made

| Doc | Correction | Why |
|-----|-----------|-----|
| Evidence Matrix | Added classification column to CF-003, CF-007, CF-010, CF-011, CF-015, CF-018 explicitly tagging each as COACH_PROGRAMMING, COACH_PRODUCT, or PLATFORM_ENGINEERING | Prevents misinterpretation of CF-018 as coach-facing |
| Implementation Backlog | Reclassified W11-015 from P0 "also" footnote to explicitly labeled PLATFORM_TRACK item; added two-track header to P0 section | Eliminates implication that auth is a coach-trial blocker |
| Roadmap | Added parallel-track note to Wave 11C and consolidated timeline | Clarifies that platform/infra items are not sequential dependencies |
