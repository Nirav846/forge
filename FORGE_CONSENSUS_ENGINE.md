# FORGE_CONSENSUS_ENGINE — Pattern Consensus Classification System

> Tracks every pattern's frequency, sport coverage, source depth, and contradictions.
> Outputs a confidence classification: Universal / Common / Situational / Rare.
> No pattern is promoted into FORGE rules without consensus review.

---

## Consensus Classification Thresholds

### Universal (90–100%)
- Pattern observed in ≥90% of relevant sources
- Zero contradictions from credible sources
- Cross-sport validity (observed in ≥3 sports)
- **Action:** Pattern graduates to a FORGE non-negotiable law (critical severity)

### Common (50–89%)
- Pattern observed in ≥50% of relevant sources
- Contradictions exist but are outweighed by evidence volume
- At least 2 independent sources (different organizations/authors)
- **Action:** Pattern becomes a FORGE default behavior (warning severity)
- May be overridden by explicit athlete constraints

### Situational (10–49%)
- Pattern observed in <50% of sources but consistently in specific conditions
- Condition-dependent validity (sport-specific, level-specific, equipment-specific)
- **Action:** Pattern becomes a conditional rule — applied only when conditions match
- Flagged in FORGE_GAPS_REPORT.md if more evidence is needed

### Rare (<10%)
- Pattern observed in ≤1 source, or <10% of examined sources
- Insufficient evidence to generalize
- **Action:** Stored for reference. Not promoted to FORGE rules unless:
  - Source credibility ≥ 0.95 AND
  - Pattern does not contradict any existing rule AND
  - External validation can be found

---

## Consensus Review Process

```
STEP 1: Extract
  Pattern enters FORGE_PATTERN_DATABASE.md with raw frequency data.
  No confidence label assigned yet.

STEP 2: Frequency Check
  Count occurrences across all examined sources.
  Calculate: percentage = occurrences / total_sources × 100

STEP 3: Contradiction Check
  FOR EACH existing pattern in the same domain:
    IF this pattern contradicts:
      Record contradiction.
      De-escalate both patterns by one tier.
      Flag for manual review.

STEP 4: Source Quality Filter
  IF all sources are same organization (e.g., all FORGE manuals):
    Maximum possible confidence = Common (never Universal without external validation).
  IF at least one source is a Real Program AND one is a Certification/Book:
    Pattern eligible for Universal if frequency ≥ 90%.
  IF only one source type:
    De-escalate one tier.

STEP 5: Sport Distribution Check
  Count sports where pattern was observed.
  IF pattern observed in <3 sports:
    Limit to Common maximum (even if frequency >90%).
  Exception: sport-specific patterns (e.g., carry requirements for contact sports)
    can be Universal within their sport category.

STEP 6: Assign Confidence
  Apply thresholds from the classification table above.
  Record in FORGE_PATTERN_DATABASE.md consensus field.
  Log the rationale in the Consensus Decision Log below.

STEP 7: Promote or File
  IF Universal AND externally validated:
    Pattern is a candidate for FORGE non-negotiable law.
    Propose as an addition to FORGE_RULEBOOK.
  IF Common:
    Pattern is a candidate for FORGE default behavior.
    Document as expected but overridable.
  IF Situational OR Rare:
    Pattern is stored for reference.
    Archived until more sources validate.
```

---

## Current Consensus Classifications

### Complete Consensus Log

| Pattern ID | Description | Frequency | Sports | Contradictions | Assigned | Rationale |
|-----------|-------------|-----------|--------|---------------|----------|-----------|
| P-0001 | Full body session composition | 3/3 (100%) | 3 | None | **Common** | Only FORGE sources; no external validation |
| P-0002 | Session slot limit ≤6 | 16/17 (94%) | 7 | None | **Universal** | Multi-sport, multi-source, well-documented |
| P-0003 | Power before strength sequencing | 6/6 (100%) | 5 | None | **Universal** | Consistent across real programs and theory |
| P-0004 | Core is last block | 7/8 (87.5%) | 5 | P-0005 | **Common** | Majority but exception exists in U/L splits |
| P-0005 | Core mid-session (U/L split) | 2/8 (25%) | 1 | P-0004 | **Rare** | Single context, limited sport distribution |
| P-0006 | Warm-up precedes loaded work | 16/16 (100%) | 7 | None | **Universal** | Absolute consensus across all source types |
| P-0007 | Conditioning is final element | 8/8 (100%) | 6 | None (exception noted) | **Universal** | With documented alactic speed carve-out |
| P-0008 | Cool-down ≥5 min | 4/8 (50%) | 4 | None | **Common** | Widely recommended, not universally enforced |
| P-0009 | Max 3 strength exercises/session | 15/16 (94%) | 6 | None | **Universal** | Strong multi-source consensus |
| P-2001 | Power blocks full recovery | 5/5 (100%) | 5 | None | **Universal** | Uncontested across all source types |
| P-2002 | Plyometric contacts ≤30/session | 4/4 (100%) | 4 | None | **Universal** | Research-validated + real program |
| P-2003 | Olympic lifts first | 3/4 (75%) | 3 | None | **Common** | Conditional on Olympic-lift inclusion |
| P-2004 | Depth jumps require 1.5x BW squat | 3/3 (100%) | 4 | None | **Universal** | Consistent safety rule |
| P-2005 | Beginners no Oly lifts/depth jumps | 4/4 (100%) | 5 | None | **Universal** | Safety-focused, multi-source |
| P-3001 | Knee + hip dominant every session | 10/10 (100%) | 6 | None | **Universal** | Absolute consensus |
| P-3002 | Push + pull every session | 11/12 (92%) | 6 | None | **Universal** | Near-universal |
| P-3003 | Pull volume ≥ push volume | 5/5 (100%) | 5 | None | **Universal** | Consistent across all sources |
| P-3004 | Posterior chain ≥ anterior chain | 4/4 (100%) | 4 | None | **Universal** | Strong agreement |
| P-3005 | Exercise difficulty matches level | 17/17 (100%) | 7 | None | **Universal** | Absolute consensus |
| P-3006 | Strength working sets 1-3 RIR | 3/3 (100%) | 4 | None | **Common** | Limited source diversity |
| P-3007 | Hip-knee balance by sport | 4/4 (100%) | 4 | None | **Common** | Sport-specific applicability |
| P-4001 | One energy system per session | 3/3 (100%) | 5 | None | **Universal** | Consistent across sources |
| P-4002 | Cond: volume before intensity | 3/3 (100%) | 4 | None | **Common** | Limited source diversity |
| P-4003 | Aerobic base before HIIT <1yr | 3/3 (100%) | 5 | None | **Universal** | Well-validated |
| P-4004 | Beginners no lactate tolerance | 3/3 (100%) | 5 | None | **Universal** | Consistent safety rule |
| P-4005 | RSA every 40s for beginners | 2/2 (100%) | 2 | None | **Situational** | FORGE-only sources; no external validation |
| P-4006 | In-season cond volume 50% | 4/4 (100%) | 4 | None | **Common** | Consistent but specific figure unvalidated |
| P-4007 | HIIT max 2 sessions/week | 4/4 (100%) | 4 | None | **Common** | Agreed principle, varying exact limit |
| P-4008 | A-tier default, C-tier niche | 2/2 (100%) | 3 | None | **Situational** | FORGE-specific tiering; not external |
| P-4009 | Cond duration limits | 3/3 (100%) | 5 | None | **Universal** | Physiologically grounded |
| P-4010 | Cond session ≥1 data point | 2/4 (50%) | 2 | None | **Situational** | Sport-dependent enforcement |
| P-5001 | Strength: reps before load | 4/4 (100%) | 5 | None | **Universal** | Consistent across all sources |
| P-5002 | Power: velocity → load → complexity | 3/3 (100%) | 3 | None | **Common** | Limited source diversity |
| P-5003 | Deload every 4-6 weeks | 4/5 (80%) | 4 | None | **Common** | Varying exact interval |
| P-5004 | Accessory progression faster | 2/2 (100%) | 2 | None | **Situational** | FORGE-only; single source type |
| P-6001 | Off-season volume before intensity | 4/4 (100%) | 4 | None | **Common** | Consistent principle |
| P-6002 | Pre-season decrease volume | 4/4 (100%) | 4 | None | **Common** | Consistent principle |
| P-6003 | In-season maintenance only | 4/4 (100%) | 5 | None | **Universal** | Near-absolute consensus |
| P-6004 | Competition week volume -20-30% | 2/2 (100%) | 3 | None | **Common** | Limited source diversity |
| P-7001 | HIIT cond 48h recovery minimum | 3/3 (100%) | 4 | None | **Universal** | Physiological necessity |
| P-7002 | Recovery cond RPE ≤3 | 2/2 (100%) | 3 | None | **Common** | Limited source diversity |
| P-8001 | Substitution: same family first | 3/3 (100%) | 5 | None | **Universal** | Logical, well-documented |
| P-8002 | Cross-family sub by intent | 2/2 (100%) | 4 | None | **Common** | FORGE-specific structure |
| P-8003 | Exercise rotation 4-6 weeks | 3/3 (100%) | 4 | None | **Common** | Consistent among S&C sources |
| P-8004 | Progression overrides rotation | 2/2 (100%) | 3 | None | **Common** | Limited source diversity |
| P-8005 | Max 30% new exercises/session | 1/3 (33%) | 1 | None | **Rare** | Single source |
| P-8006 | Sport-specific mandatory exercises | 5/5 (100%) | 5 | None | **Universal** | Sport-category specific; universal within category |

---

## Consensus Summary

### Universal Patterns (candidates for non-negotiable FORGE laws)

These 23 patterns have sufficient evidence to graduate:
P-0002, P-0003, P-0006, P-0007, P-0009, P-2001, P-2002, P-2004, P-2005,
P-3001, P-3002, P-3003, P-3004, P-3005, P-4001, P-4003, P-4004, P-4009,
P-5001, P-6003, P-7001, P-8001, P-8006

### Common Patterns (candidates for FORGE defaults)

These 19 patterns are standard practice but allow exceptions:
P-0001, P-0004, P-0008, P-2003, P-3006, P-3007, P-4002, P-4006, P-4007,
P-5002, P-5003, P-6001, P-6002, P-6004, P-7002, P-8002, P-8003, P-8004

### Situational Patterns (condition-dependent)

These 2 patterns apply only in specific contexts:
P-4005 (beginner RSA start point), P-4010 (sport-dependent data tracking),
P-4008 (FORGE-specific tiering), P-5004 (FORGE-specific progression hierarchy)

### Rare Patterns (insufficient evidence)

These 3 patterns need more validation:
P-0005 (core mid-session U/L split), P-8005 (30% new exercise cap)

---

## Contradictions Requiring Resolution

| Contradiction ID | Pattern A | Pattern B | Domain | Priority | Resolution Status |
|-----------------|-----------|-----------|--------|----------|-------------------|
| C-001 | P-0004: Core is last | P-0005: Core mid-session | Session Structure | Low | Resolved: P-0005 is U/L split exception; both coexist |
| C-002 | P-0007: Conditioning last | CL003: Speed requires fresh CNS | Conditioning | None (carve-out) | Resolved: Alactic speed exception explicitly documented |
| C-003 | (Pending) | (Pending) | — | — | Awaiting contradictory pattern extraction |

---

## Consensus Decision Log

| Date | Pattern | Previous Classification | New Classification | Rationale |
|------|---------|----------------------|-------------------|-----------|
| — | All | None (initial extraction) | As assigned above | Initial population from FORGE implementation spec and source manuals |
