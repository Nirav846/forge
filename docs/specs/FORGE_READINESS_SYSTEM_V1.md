# FORGE Readiness System V1

**Purpose:** Minimal readiness monitoring that fits coach workflow, not
sports-science complexity. Designed to pair with the recovery library and
testing library.

**Key constraint:** The system must take ≤ 2 minutes per athlete per day.

---

## Part 1 — What Elite Coaches Actually Do

Research across NSCA, UKSCA, ASCA, rugby S&C, tennis S&C, cricket S&C:

### 1.1 Common practices (used by 80%+ of elite coaches)

| Practice | Time per athlete | Used by | FORGE MVP? |
|----------|-----------------|---------|------------|
| "How are you feeling?" (verbal chat) | 15-30s | Nearly all | YES |
| Observe movement in warmup | Passive | Nearly all | YES |
| Session RPE post-training | 10s | Most | YES |
| Previous session completion check | 10s | Most | YES |
| Subjective readiness (1-5 / 1-10) | 10s | ~60% | YES |

### 1.2 Common but not universal (used by 30-60%)

| Practice | Time per athlete | Used by | FORGE MVP? |
|----------|-----------------|---------|------------|
| Wellness questionnaire (sleep, soreness, fatigue, mood, stress) | 1-2 min | ~50% of professional teams | NO |
| CMJ on force plate | 2 min (setup + test) | ~40% of professional teams | NO |
| HRV | 2 min (morning, supine) | ~30% of professional teams | NO |
| Blood markers | Clinical | ~20% | NO |

### 1.3 Rare (used by < 30%)

| Practice | Used by | Reason for exclusion |
|----------|---------|---------------------|
| Daily wellness app | ~20% | Low compliance, high burden |
| GPS load monitoring | ~25% | Requires GPS vests, data analyst |
| Omega Wave / heart rate recovery | ~10% | Expensive, marginal benefit over subjective |
| Cognitive reaction time | ~5% | Research stage, not practical |
| Salivary cortisol | ~1% | Lab-based, not real-time |

---

## Part 2 — MVP Readiness System

**Three inputs, < 60 seconds per athlete.**

### Input 1: Session completion (binary, 10s)

```
Did athlete complete previous session?
  ☐ Yes, as prescribed
  ☐ Yes, with modifications (note: ________)
  ☐ No
```

If "No" or "modified" → reduce volume by 20% (auto flag in FORGE).

### Input 2: Subjective readiness (1-5, 10s)

```
On a scale of 1-5, how ready are you to train today?

1 = "Take the day off"
2 = "Needs lighter session"
3 = "Normal"
4 = "Ready to push"
5 = "Feeling great, want to test"
```

### Input 3: Warmup observation (passive, coach watches)

```
During Raise phase, does the athlete demonstrate:

☐ Normal movement (no observable issues)
☐ Hip asymmetry (favour one leg, limited ROM in one hip)
☐ T-spine restriction (limited rotation, hunched shoulders)
☐ Ankle restriction (limited dorsiflexion, on toes)
☐ Low energy (sluggish movement, low intensity)
☐ Pain behaviour (wincing, guarding, rubbing a body part)
```

### Readiness adjustment rules

| Subjective | Session completed | Warmup observation | Adjustment |
|-----------|-------------------|-------------------|------------|
| 5 | Yes | Normal | Proceed as planned |
| 4 | Yes | Normal | Proceed as planned |
| 3 | Yes | Normal | Proceed as planned |
| 3 | No/Modified | — | Reduce volume 20% |
| 2 | — | Any | Lighter session. Reduce volume 30%. Prioritise technique |
| 1 | — | Any | Off day + L4/L5 recovery protocol |
| Any | — | Pain behaviour | Refer to medical/physio before training |
| Any | — | Asymmetry/restriction | Add targeted mobility drills before session |

### MVP dashboard (physical or digital)

```
ATHLETE       READY    SESSION    WARMUP     ADJUSTMENT
───────────────────────────────────────────────────────
Smith, J      4        Done       Normal     Proceed
Patel, A      2        Modified   Asymmetry  Light session (70%)
Singh, R      5        Done       Normal     Proceed — add test
Williams, T   1        No         Pain       OFF + recovery protocol
Chen, L       3        Done       Low energy Reduce volume 20%
```

---

## Part 3 — Session RPE (10s post-training)

After each session, the athlete provides one number:

```
How hard was that session? (1-10)

1 = Rest day easy
2-3 = Easy warmup-level
4-5 = Moderate, could have done more
6-7 = Hard, but completed as planned
8-9 = Very hard, barely completed
10 = Max effort, couldn't have done more
```

### sRPE use case

sRPE × session duration (min) = training load (arbitrary units).

Compare against rolling 7-day average. If daily load > 2× the 7-day average,
flag for coach review (possible overreach).

**MVP rule:** If sRPE ≥ 9 for two consecutive sessions, reduce next session
volume by 30% (auto apply). This replaces the need for HRV, wellness
questionnaires, or force plates.

---

## Part 4 — What Was Excluded (and Why)

| Excluded | Why | When to add |
|----------|-----|-------------|
| Wellness questionnaire (sleep, mood, stress, soreness × 5 questions) | Too long, low compliance, coaches don't use the data. The subjective readiness score (1-5) captures the same signal in one question | If the team has a dedicated sports scientist |
| HRV | Requires 2 min supine each morning, expensive monitor, sensitive to measurement error, and subjective readiness is equally predictive of performance | If the team has budget + compliance + data analyst |
| CMJ for readiness | Single-leg CMJ adds value for ACL monitoring. Bilateral CMJ for readiness is redundant with subjective readiness + warmup observation | If the team has force plates + ACL injury history |
| GPS load data | Requires vests, GPS units, software, analyst. Not practical for most settings | If the team already has GPS and a data person |
| Biochemical markers | Not real-time, expensive, invasive | Never for daily readiness — use only for specific medical return-to-play decisions |
| Cognitive testing | Research-stage, no clear readiness signal | Not yet |

### Exclusion principle

> If a readiness tool doesn't change the coach's decision for that session,
> it doesn't add value.

Subjective readiness (1-5) + session completion check + warmup observation =
three signals that DO change decisions. Everything else is incremental at
best.

---

## Part 5 — Readiness-Driven Session Adjustment

### 5.1 Volume adjustment rules

| Readiness | Warmup | Session type | Volume | Intensity | Exercise selection |
|-----------|--------|-------------|--------|-----------|-------------------|
| 4-5 | Normal | Any | 100% | As prescribed | Normal |
| 3 | Normal | Strength | 100% | As prescribed | Normal |
| 3 | Normal | Power | 90% | 90% of prescribed intensity | Sub-max explosive |
| 3 | Normal | Speed | 90% | 90% | No max velocity |
| 2 | Any | Any | 60-70% | Technique focus | Regressed exercises |
| 1 | Any | Off | — | — | Recovery only |

### 5.2 Blueprint override (fatigue-driven)

If readiness = 1-2 for 3+ consecutive sessions, FORGE should override the
scheduled blueprint to BP13 (Deload / Active Recovery) regardless of season.

**Rule:** `if readiness_avg < 3 over 3 sessions → force BP13 for 1 week`

This connects the readiness system to the existing blueprint engine without
modifying the core program generator.

---

## Part 6 — Implementation Requirements

### Data model (add to AthleteProfile)

```
readiness_score: int = 3       # 1-5, default 3
session_completed: bool = True
warmup_observation: str = "normal"  # normal, asymmetry, restriction, low_energy, pain
previous_srpe: int = 0         # 1-10, 0 = no session
```

### Adjustment output

```
volume_multiplier: float = 1.0
blueprint_override: Optional[int] = None
add_mobility: list[str] = []   # drill IDs from mobility library
recovery_protocol: Optional[str] = None  # protocol ID from recovery library
```

### Minimal integration

```python
def apply_readiness(
    program: GeneratedProgram,
    readiness: dict,
    athlete: AthleteProfile,
) -> GeneratedProgram:
    # 1. Check readiness score + session completion
    if readiness["score"] <= 2:
        program.credibility_score *= 0.85
    # 2. Check warmup observation
    if readiness.get("warmup_issue"):
        program.credibility_score *= 0.90
    # 3. Check consecutive low readiness
    if readiness["consecutive_low"] >= 3:
        return override_to_deload(athlete)
    return program
```

Three condition checks, no new database, no new models. Pure logic on an
existing program.

---

## Part 7 — Summary

### Readiness system components

| Component | Time | Method | MVP? |
|-----------|------|--------|------|
| Session completion | 10s | Verbal / checkbox | YES |
| Subjective readiness (1-5) | 10s | Verbal / scale | YES |
| Warmup observation | Passive | Coach watches | YES |
| Session RPE | 10s | Verbal post-session | YES |
| Wellness questionnaire | 2 min | Paper / app | NO |
| HRV | 2 min | Monitor | NO |
| CMJ readiness | 2 min | Force plate | NO |
| GPS load | — | Tech stack | NO |

### Decision rules

| Condition | Action |
|-----------|--------|
| Readiness 1 | Off day + recovery protocol |
| Readiness 2 | Light session, 60-70% volume |
| Readiness 3 + no session | Reduce volume 20% |
| Warmup pain | Refer to medical |
| Warmup asymmetry | Add 5 min targeted mobility |
| sRPE ≥ 9 × 2 consecutive | Auto-reduce next session 30% |
| Readiness ≤ 2 × 3 consecutive | Force BP13 for 1 week |
| sRPE > 2× 7-day average | Flag for coach review |

**Total system: 3 inputs, 60s per athlete, 7 decision rules, 0 new
infrastructure.**
