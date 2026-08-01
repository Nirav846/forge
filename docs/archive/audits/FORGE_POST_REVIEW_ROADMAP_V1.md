# FORGE Post-Review Roadmap — Wave Plan

Derived from the evidence matrix (`FORGE_COACH_FEEDBACK_EVIDENCE_MATRIX_V1.md`),
synthesis (`FORGE_WAVE11_COACH_FEEDBACK_SYNTHESIS_V1.md`), and implementation
backlog (`FORGE_WAVE11_IMPLEMENTATION_BACKLOG_V1.md`).

---

## Guiding Principles

1. **Trust first.** The most important thing is to give coaches a reason to
   believe the system understands their world. That means fixing the clearest
   signals of "this system doesn't get it" — Goblet Squats for advanced
   athletes, ignored validation flags, and off-season volume during a match
   week.
2. **Differentiation before expansion.** Before adding new features, make the
   existing ones real. Role bias values that don't change exercise selection
   are worse than no bias values at all.
3. **Substance over surface.** Cueing language and score breakdowns matter,
   but not before the engine produces programs that coaches would rationally
   trust.

---

## Wave 11A — Trust-Critical Coach Fixes (Weeks 1-4)

**Theme**: Close the most trust-damaging gaps. Make FORGE produce programs
that a serious S&C coach would not immediately dismiss.

### Scope

| Item | Title | Why Here |
|---|---|---|
| W11-001 | Advanced bilateral lower-body exercise tier | The #1 trust-breaker. No coach takes a system seriously that prescribes Goblet Squats for advanced athletes. |
| W11-006 | In-season volume reduction rules | The #2 trust-breaker. Coaches managing competitive athletes cannot use programs with off-season volume during a season. |
| W11-007 | Replace "reduce families" with proportional reduction | Small fix that eliminates the most visibly chaotic programming pattern (qualities appearing/disappearing across weeks). |
| W11-009 | Mandate injury prevention exercise families | Addresses a welfare gap that 6/8 coaches flagged. Low complexity, high signal. |

### Why these belong together

These four changes are quick wins that address the most visible, most frequently
cited trust-damaging issues. They require no architectural changes — only rule
modifications within existing engine layers. Together they would materially
change how a coach perceives FORGE's output.

### Expected coach-facing impact

A coach reviewing the same programs after these fixes would see:
- Advanced athletes performing Barbell Squats, not Goblet Squats
- In-season programs with 2x/week, 2 sets, pre/post match protocols
- Consistent exercise categories across all weeks (no sprint appearing/
  disappearing)
- Shoulder external rotation work in overhead sports, Nordic curls in
  speed sports

These changes would not make FORGE "ready for prime time" but they would
remove the most obvious reasons to dismiss it.

### Expected engineering complexity

- **W11-001**: 2-3 days — add level-based exercise tier config, modify
  exercise selection queries
- **W11-006**: 3-5 days — add in-season rule set, test across sports
- **W11-007**: 1-2 days — replace binary removal with proportional reduction
- **W11-009**: 2-3 days — add injury prevention families, mandate rules

**Total**: ~8-13 engineering days.

---

## Wave 11B — Role Specificity & Advanced-Athlete Quality Pass (Weeks 5-8)

**Theme**: Make role differentiation real. Upgrade the engine from
"general S&C with bias labels" to genuinely sport-specific programming.

### Scope

| Item | Title | Why Here |
|---|---|---|
| W11-004 | Bias-to-exercise-selection pipeline | The defining architectural change. Role bias values must actually constrain exercise selection. |
| W11-003 | Plyometric progression pathway | Builds on W11-001's level-dependent logic but requires more exercise library work. |
| W11-002 | Deceleration/eccentric exercise family | Library expansion to cover the most frequently missing exercise category. |

### Why these belong together

These three items form a coherent "advanced athlete" package. They upgrade
the exercise library, the selection rules, and the progression model together.
Without W11-004, plyometric and eccentric additions would be available but
not targeted to the right roles.

### Expected coach-facing impact

- Roles within a sport would receive materially different programs
  (e.g., cricket Spin Bowler would have rotational exercises; Fast Bowler
  would have eccentric work)
- Advanced athletes would have genuine progression pathways (plyometrics,
  barbell loading, eccentric work)
- Speed roles would have deceleration work as a standard feature

### Expected engineering complexity

- **W11-004**: 2-4 weeks — largest single item. Requires exercise-to-bias
  tagging, selection filter creation, and pipeline integration.
- **W11-003**: 1-2 weeks — tier system + exercise library additions
- **W11-002**: 3-5 days — library additions + mandate rules

**Total**: ~3-6 weeks.

---

## Wave 11C — Validation & Infrastructure (Weeks 9-10)

**Theme**: Make the system's quality assurance self-correcting. Add
production infrastructure.

### Scope

| Item | Title | Why Here |
|---|---|---|
| W11-008 | Validation system auto-correction loop | Depends on W11-007 (proportional reduction) being in place first. |
| W11-015 | Authentication/authorization | Independent but needed before any production deployment. |
| W11-016 | CI/CD pipeline and test coverage | Independent but needed for development velocity. |

### Why these belong together

These are "quality infrastructure" items. They make the system reliable,
secure, and self-auditing. W11-008 specifically addresses the most damaging
validation issue and depends on W11-007's proportional reduction logic.

### Expected coach-facing impact

- Coaches would no longer see programs with system-generated red flags
  — the flags would be resolved before output
- Credibility scores would be explainable with sub-component breakdowns

### Expected engineering complexity

- **W11-008**: 2-3 weeks — architectural change to wire validation →
  correction
- **W11-015**: 1-2 weeks — FastAPI auth utilities + token management
- **W11-016**: 1 week — GitHub Actions workflow + test scaffolding

**Total**: ~4-6 weeks.

---

## Wave 12 — Periodization & Progression Sophistication (Weeks 11-16)

**Theme**: Broader engine refinement. Improve the periodization model,
conditioning specificity, warm-up generation, and beginner progression.

### Scope

| Item | Title | Why Here |
|---|---|---|
| W11-010 | Beginner within-block exercise progression | Follows from the level-tier work in W11-001/W11-003 |
| W11-011 | Conditioning movement-pattern awareness | Depends on core engine being stable after Waves 11A-C |
| W11-012 | Session-aware warm-up generation | Independent but benefits from exercise library maturity |
| W11-013 | Credibility score sub-component breakdown | Independent, small, can be done anytime |

### Expected coach-facing impact

- Beginner programs would show a progression narrative within blocks
- Conditioning would match sport movement patterns (multi-directional
  for court sports, mixed for field sports)
- Warm-ups would vary by session emphasis
- Credibility scores would be transparent and actionable

### Expected engineering complexity

- **W11-010**: 2-3 days — mid-block advancement trigger
- **W11-011**: 1-2 weeks — movement-pattern classification + protocol mapping
- **W11-012**: 1-2 weeks — warm-up generator with session context awareness
- **W11-013**: 1-2 days — score breakdown serialization

**Total**: ~3-5 weeks.

---

## Wave 13 — Library, Customization & Coach Workflow (Post-Wave 12)

**Theme**: Long-term vision features that expand FORGE's capability beyond
core program generation.

### Scope

| Item | Title | Why Here |
|---|---|---|
| W11-014 | Sport-specific cue template layer | Independent, small, can join any wave |
| W11-005 | Compound / dual-role support | Niche but valuable for cricket and hybrid athletes |
| (planned) | Sport-specific drill library | Largest single feature. Per-sport, per-role drill integration |
| (planned) | Sport practice load integration | Requires external data input API + auto-regulation |
| (planned) | Coach override / editing / compare workflow | Interactive output delivery layer |

### Expected engineering complexity

- Sport-specific drill library: 4-8 weeks per sport (phased)
- Practice load integration: 3-5 weeks
- Coach override workflow: 4-6 weeks

---

## Consolidated Timeline

```
Week 1-4   │ Wave 11A — Trust-critical fixes          │ W11-001, 006, 007, 009
Week 5-8   │ Wave 11B — Role specificity / quality    │ W11-004, 003, 002
──────────────────────────────────────────────────────────────────────────────
           │ Parallel platform track (non-blocking)   │
Week 9-10  │ Wave 11C — Validation & infra            │ W11-008, 015, 016
──────────────────────────────────────────────────────────────────────────────
Week 11-16 │ Wave 12 — Periodization refinement       │ W11-010, 011, 012, 013
Week 17+   │ Wave 13 — Library / coach workflow       │ W11-014, 005 + new
```

**Important**: Waves 11A and 11B are the coach-trust track. Wave 11C (platform
track) runs in parallel and does NOT block coach trials. Auth and CI/CD can be
added after coach feedback is collected.

---

## What Can Be Shown to Coaches After Each Wave

| Wave | Coach-trial readiness |
|---|---|
| Current | Beginner programs only. Advanced/in-season not ready. 3/8 coaches declined trial. |
| After Wave 11A | Advanced programs no longer embarrassing (no Goblet Squats). In-season programs usable. Injury prevention present. Credible for intermediate-level trial. |
| After Wave 11B | Role programs genuinely differ. Plyometric and eccentric progression exist. Ready for advanced-sport trial with caveats. |
| After Wave 11C | Validation system self-corrects. Engineering infrastructure supports deployment. |
| After Wave 12 | Conditioning is sport-specific. Warm-ups context-aware. Credibility scores transparent. |
| After Wave 13 | Sport-specific drills available. Practice load integration. Coach editing workflow. Ready for production launch. |

---

## Risk Summary

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| W11-004 (bias-to-exercise) scope underestimated | Medium | High | Start with minimum viable: fix cricket rotation + basketball separation first. Full mapping can follow. |
| Coach expectations after Wave 11A may still exceed reality | Medium | Medium | Be explicit with coaches about what Wave 11A does and does not fix. Frame as "we fixed the trust-breakers; specificity still in progress." |
| Existing test suite cannot catch regression in exercise selection | Medium | Medium | Add scenario-based tests alongside each wave. Regenerate known sample packs and diff against expected patterns. |
| W11-008 (auto-correction) introduces new bugs | Medium | High | Implement with a "dry-run" mode first. Validate correction logic on historical flagged samples before enabling in production. |

---

## Quick Reference

**If we could do only one wave**: Wave 11A (trust-critical fixes).
It removes the clearest reasons for a coach to dismiss the system.

**If we could do only three items**: W11-001 (Goblet Squat fix),
W11-004 (bias→selection pipeline), W11-008 (validation correction).

**What is already good enough**: Beginner programs, role bias framework,
exposure tracking, adaptive periodization concept.
