# FORGE Coach Review Action Backlog

_Generated: 2026-06-23 21:25_

## 1. Purpose

This document converts external S&C coach review feedback into actionable product and engineering work items. Each item is grounded in specific coach comments from the review pass. Items are grouped by system area and prioritized by cross-sport impact and coach sentiment severity.

## 2. Action Items

| ID | Title | Source Sport(s) | Source Feedback Summary | System Area | Wave/Milestone | Priority | Confidence | Notes |
|---|---|---|---|---|---|---|---|---|
| BL-01 | Replace Goblet Squat with Barbell Squat for advanced athletes (Trainin | All 8 sports | Goblet Squat persists through advanced levels — athletes with 5+ years training age need barbell loa | Exercise Selection Engine | Wave 1 | Critical | High | Fix is localized to level-based exercise selection logic |
| BL-02 | Build in-season programming mode with volume reduction | All 8 sports | In-season samples maintain off-season volumes — 3x/week with full strength sessions inappropriate du | Periodization Engine | Wave 1 | Critical | High | Requires new seasonal context rules: reduce to 2x/week, 2 sets/exercise |
| BL-03 | Implement real role-differentiated exercise selection | All 8 sports | Role differentiation is superficial — exercise selection nearly identical across roles despite diffe | Role Modeling Engine | Wave 1 | Critical | High | Most impactful change. Requires per-role exercise trees, not just bias multiplie |
| BL-04 | Build structured plyometric progression model | All 8 sports | No plyometric progression across levels — beginner/ Intermediate/Advanced all use same jump exercise | Exercise Progression Engine | Wave 1 | Critical | High | Clear progression path: Pogo Jumps -> Box Jumps -> Depth Jumps -> Single-Leg |
| BL-05 | Upgrade validation warnings to auto-correction | All 8 sports | 'Check volume load match: needs attention' warnings appear in 20+ samples but system does not auto-c | Validation System | Wave 1 | Critical | High | When volume load mismatch detected, system should auto-reduce sets/duration |
| BL-06 | Add deceleration/eccentric exercise category across all programs | All 8 sports | Deceleration and eccentric work largely absent from all programs — critical for injury prevention | Exercise Library / Engine | Wave 2 | High | High | Add Nordic curls, SL RDLs, deceleration drills as mandatory category |
| BL-07 | Create sport-specific drill library per sport and role | All 8 sports | No sport-specific drills — goalkeeper dives, scrum engagement, lineout jumps, tackle prep all missin | Sport Intelligence Layer | Wave 2 | High | Medium | Largest new feature. Requires sport-by-sport exercise intelligence build-out |
| BL-08 | Replace linear conditioning with multi-directional sport-specific cond | All 8 sports | Conditioning is linear shuttle-based — needs COD, lateral, multi-directional patterns for sport tran | Conditioning Engine | Wave 2 | High | Medium | Replace some MAS work with sport-specific movement patterns |
| BL-09 | Add shoulder injury prevention protocols (external rotation, scapular  | All 8 sports | No shoulder external rotation work, no rotator cuff strengthening despite sport-specific overhead de | Injury Prevention Module | Wave 2 | High | Medium | Common gap across all overhead sports |
| BL-10 | Add hamstring injury prevention (Nordic curls) across all sports | All 8 sports | No hamstring injury prevention work — Nordic curls absent from all programs | Injury Prevention Module | Wave 2 | Medium | High | Simple addition with high injury prevention value |
| BL-11 | Implement beginner exercise progression within blocks | Soccer, Tennis, Volleyball, Badminton, Basketball | Beginner programs repeat same exercises (Air Squat, Wall Push-Up) across all 8 weeks with only volum | Exercise Progression Engine | Wave 2 | Medium | High | Add simple within-block progression or coach notification notes |
| BL-12 | Replace generic cues with sport-specific coaching language | All 8 sports | Cues like 'Land soft, stick each rep' are too generic — need sport-specific versions | Rendering / Output | Wave 2 | Medium | Medium | Build cue template per sport with sport-specific analogies |
| BL-13 | Publish credibility score breakdown criteria | Soccer, Tennis, Volleyball | Coaches question why a program scores 0.89 vs 1.0 — criteria not transparent | Validation System / Output | Wave 3 | Low | Medium | Add score component breakdown to program output |
| BL-14 | Implement authentication/authorization for production API | System-wide | Code review identified missing auth as critical security gap. No OAuth2/JWT protection on endpoints | Infrastructure / Security | Wave 1 | Critical | High | From code review report — prerequisite for production deployment |
| BL-15 | Add comprehensive test suite and CI/CD pipeline | System-wide | Code review found limited test coverage, no CI/CD, no linting/formatting standards | Infrastructure / QA | Wave 1 | High | High | From code review report — needed for reliability and team velocity |

## 3. Grouping by System Area

### Conditioning Engine

- **BL-08** (High): Replace linear conditioning with multi-directional sport-specific conditioning

### Exercise Library / Engine

- **BL-06** (High): Add deceleration/eccentric exercise category across all programs

### Exercise Progression Engine

- **BL-04** (Critical): Build structured plyometric progression model
- **BL-11** (Medium): Implement beginner exercise progression within blocks

### Exercise Selection Engine

- **BL-01** (Critical): Replace Goblet Squat with Barbell Squat for advanced athletes (Training Age 5+)

### Infrastructure / QA

- **BL-15** (High): Add comprehensive test suite and CI/CD pipeline

### Infrastructure / Security

- **BL-14** (Critical): Implement authentication/authorization for production API

### Injury Prevention Module

- **BL-09** (High): Add shoulder injury prevention protocols (external rotation, scapular stability)
- **BL-10** (Medium): Add hamstring injury prevention (Nordic curls) across all sports

### Periodization Engine

- **BL-02** (Critical): Build in-season programming mode with volume reduction

### Rendering / Output

- **BL-12** (Medium): Replace generic cues with sport-specific coaching language

### Role Modeling Engine

- **BL-03** (Critical): Implement real role-differentiated exercise selection

### Sport Intelligence Layer

- **BL-07** (High): Create sport-specific drill library per sport and role

### Validation System

- **BL-05** (Critical): Upgrade validation warnings to auto-correction

### Validation System / Output

- **BL-13** (Low): Publish credibility score breakdown criteria
