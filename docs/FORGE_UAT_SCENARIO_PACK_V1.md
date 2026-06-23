# FORGE UAT Scenario Pack v1

## How to Use

Each scenario includes:
- **Scenario ID**: Unique identifier
- **Athlete Input**: Summary of what to enter in the frontend
- **Checklist**: What a tester should verify
- **Pass/Fail Criteria**: Binary pass/fail for each check
- **Tier**: Core or Premium
- **Coach Expectation**: What a credible S&C coach should see

Run all scenarios against a live backend (`python run_forge_api.py`) + frontend (`npm run dev`).

---

## A. Core Mode Scenarios

### CORE-01: General Fitness Adult

| Field | Value |
|-------|-------|
| Athlete Name | General Adult |
| Sport | general |
| Level | Intermediate |
| Available Minutes | 60 |
| Goal | conditioning |
| Mode | core |

**Checklist:**
- [ ] Backend returns 200 with valid payload
- [ ] Response contains `metadata`, `summary`, `sessions`, `weeks`, `rationale`, `personalization_notes`, `validation`
- [ ] Sessions render in Block Builder view
- [ ] Coach Summary tab shows rationale text
- [ ] Right Panel Engineering tab shows Raw API payload
- [ ] Save artifact succeeds
- [ ] Reloaded artifact matches original

**Pass if:** Program generates without error, renders in all 3 views (Coach Summary, Block Builder, Delivery), survives save→reload round-trip.

---

### CORE-02: Youth Athlete

| Field | Value |
|-------|-------|
| Athlete Name | Youth Athlete |
| Sport | rugby |
| Level | Beginner |
| Age | 16 |
| Training Age | 1 year |
| Available Minutes | 45 |
| Goal | strength |
| Mode | core |

**Checklist:**
- [ ] Program generates at Intermediate level (youth safety cap)
- [ ] Exercises within difficulty range for level
- [ ] Sessions not overloaded (> 6 families per session)
- [ ] Coach summary references appropriate level

**Pass if:** Youth generates safe, level-appropriate program. No Advanced-difficulty exercises.

---

### CORE-03: No Sport Role, No Advanced Fields

| Field | Value |
|-------|-------|
| Athlete Name | Minimal Athlete |
| Sport | (empty) |
| Level | Intermediate |
| Available Minutes | 60 |
| Goal | strength |
| Mode | core |

**Checklist:**
- [ ] Backend accepts empty sport (falls back to "athlete")
- [ ] Generic blueprint selected
- [ ] No crash in rationale or personalization view
- [ ] Sessions render with valid exercises

**Pass if:** Program generates without error. Sport defaults to "athlete".

---

### CORE-04: Deload / Maintenance

| Field | Value |
|-------|-------|
| Athlete Name | Deload Athlete |
| Sport | rugby |
| Level | Intermediate |
| Days to Match | 0 |
| Available Minutes | 45 |
| Goal | strength |
| Mode | core |

**Checklist:**
- [ ] Summary shows "Recovery" or "Deload" goal
- [ ] Limited sessions / reduced volume
- [ ] Credibility score present

**Pass if:** Recovery/deload program generated with appropriate low volume.

---

## B. Premium / Sport-Specific Scenarios

### PREM-01: Rugby Prop

| Field | Value |
|-------|-------|
| Athlete Name | Rugby Prop |
| Sport | rugby |
| Role | prop |
| Level | Advanced |
| Age | 26 |
| Training Age | 6 years |
| Available Minutes | 50 |
| Goal | strength |
| Mode | premium |
| Force-Velocity Profile | Force Deficit |
| Injury Flags | Right Shoulder |

**Checklist:**
- [ ] Blueprint appropriate for rugby prop (high force emphasis)
- [ ] Shoulder overhead risk noted in personalization
- [ ] Force-deficit loading bias (lower-rep strength)
- [ ] Coach summary mentions prop role

**Pass if:** Program emphasizes maximal force, avoids overhead loading, references prop-specific coaching.

---

### PREM-02: Rugby Backline

| Field | Value |
|-------|-------|
| Athlete Name | Rugby Back |
| Sport | rugby |
| Role | backline |
| Level | Advanced |
| Age | 24 |
| Training Age | 4 years |
| Available Minutes | 60 |
| Goal | power |
| Mode | premium |
| Force-Velocity Profile | Velocity Deficit |
| Injury Flags | Hamstring |

**Checklist:**
- [ ] Velocity/speed-power emphasis in notes
- [ ] Hamstring risk noted — sprint exposure capped
- [ ] Backline role mentioned in summary

**Pass if:** Program balances power work with hamstring-aware sprint dosing.

---

### PREM-03: Cricket Fast Bowler

| Field | Value |
|-------|-------|
| Athlete Name | Cricket Bowler |
| Sport | cricket |
| Role | fast_bowler |
| Level | Advanced |
| Age | 25 |
| Training Age | 5 years |
| Available Minutes | 55 |
| Goal | power |
| Mode | premium |
| Injury Flags | Lumbar Spine, Hamstring |

**Checklist:**
- [ ] Lumbar risk noted — hinge dosing moderated
- [ ] Hamstring risk noted — sprint capped
- [ ] Fast bowler role referenced
- [ ] Rotation exposure moderated per role

**Pass if:** Program shows lumbar-aware loading, hamstring protection, bowler-specific notes.

---

### PREM-04: Cricket Batter

| Field | Value |
|-------|-------|
| Athlete Name | Cricket Batter |
| Sport | cricket |
| Role | batter |
| Level | Intermediate |
| Age | 23 |
| Training Age | 3 years |
| Available Minutes | 50 |
| Goal | power |
| Mode | premium |

**Checklist:**
- [ ] Batter role referenced in notes
- [ ] Rotational emphasis present
- [ ] Upper-body and core work appropriate for batting

**Pass if:** Program references batting role with appropriate movement patterns.

---

### PREM-05: Tennis Singles

| Field | Value |
|-------|-------|
| Athlete Name | Tennis Player |
| Sport | tennis |
| Role | singles |
| Level | Advanced |
| Age | 22 |
| Training Age | 4 years |
| Available Minutes | 50 |
| Goal | power |
| Mode | premium |

**Checklist:**
- [ ] Rotational emphasis noted
- [ ] Sprint/deceleration work present
- [ ] Conditioning density appropriate for tennis

**Pass if:** Program shows tennis-specific loading with rotational and deceleration focus.

---

### PREM-06: Volleyball Middle Blocker

| Field | Value |
|-------|-------|
| Athlete Name | Volleyball Player |
| Sport | volleyball |
| Role | middle_blocker |
| Level | Advanced |
| Age | 22 |
| Training Age | 4 years |
| Available Minutes | 60 |
| Goal | power |
| Mode | premium |
| CMJ Band | High |
| Landing Competency | Poor |
| Injury Flags | Patellar Tendon |

**Checklist:**
- [ ] Jump/landing emphasis in notes
- [ ] Patellar tendon risk — reactive jump density reduced
- [ ] Poor landing competency — plyo sets capped
- [ ] Middle blocker role referenced

**Pass if:** Program shows jump-landing work with appropriate caps for patellar risk and landing quality.

---

### PREM-07: Basketball Guard

| Field | Value |
|-------|-------|
| Athlete Name | Basketball Guard |
| Sport | basketball |
| Role | guard |
| Level | Advanced |
| Age | 24 |
| Training Age | 5 years |
| Available Minutes | 60 |
| Goal | power |
| Mode | premium |

**Checklist:**
- [ ] Guard role referenced
- [ ] Sprint exposure elevated per role
- [ ] Jump/landing work present
- [ ] Deceleration emphasis per role

**Pass if:** Program shows basketball-specific loading with guard movement demands.

---

### PREM-08: Soccer Midfielder

| Field | Value |
|-------|-------|
| Athlete Name | Soccer Midfielder |
| Sport | soccer |
| Role | midfielder |
| Level | Advanced |
| Age | 23 |
| Training Age | 4 years |
| Available Minutes | 60 |
| Goal | conditioning |
| Mode | premium |

**Checklist:**
- [ ] Midfielder role referenced
- [ ] High conditioning density
- [ ] Sprint exposure elevated
- [ ] Deceleration emphasis present

**Pass if:** Program shows soccer-specific conditioning with midfielder running demands.

---

## C. Constraint / Edge Scenarios

### EDGE-01: Very Short Session

| Field | Value |
|-------|-------|
| Available Minutes | 20 |
| Goal | strength |
| Mode | core |

**Checklist:**
- [ ] Program generates with reduced families (≤4)
- [ ] Sessions are shorter but coherent
- [ ] No crash in any view

---

### EDGE-02: Competition Taper

| Field | Value |
|-------|-------|
| Days to Match | 3 |
| Goal | power |
| Mode | core |

**Checklist:**
- [ ] Summary mentions "taper"
- [ ] Sessions show reduced volume
- [ ] Credibility score still present

---

### EDGE-03: Multiple Injury Flags

| Field | Value |
|-------|-------|
| Injury Flags | Lumbar Spine, Hamstring, Patellar Tendon, Right Shoulder |
| Goal | strength |
| Mode | premium |

**Checklist:**
- [ ] All risk flags reflected in personalization notes
- [ ] Program generates without error
- [ ] Notes mention lumbar, hamstring, patellar, shoulder

---

### EDGE-04: Missing Optional Fields

| Field | Value |
|-------|-------|
| Only Athlete Name set | "Minimal" |
| Everything else | empty/default |

**Checklist:**
- [ ] Backend accepts
- [ ] Program generates
- [ ] No crash in any UI view
- [ ] Save succeeds

---

### EDGE-05: Save → Reload → Compare

**Flow:**
1. Generate and save program A
2. Modify athlete name, generate and save program B
3. Open Library, load program A
4. Switch to compare tab, select program B

**Checklist:**
- [ ] Program A renders identically after reload
- [ ] Compare tab shows structural diff without crashing
- [ ] Save → reload → save idempotent

---

### EDGE-06: Backend Down

**Flow:**
1. Stop backend server
2. Try to generate

**Checklist:**
- [ ] Error banner shown (not blank screen)
- [ ] App continues to function in mock fallback mode
- [ ] Error message is coach-appropriate (not a stack trace)

---

## UAT Pass Criteria

A scenario **passes** if all checklist items pass without error, crash, or obviously wrong output.

The full UAT pack **passes** if:
1. All Core scenarios pass
2. At least 6 of 8 Premium scenarios pass
3. All Edge scenarios pass
4. No uncaught exceptions in backend logs
5. No console errors in frontend
