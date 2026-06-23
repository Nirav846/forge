# FORGE_PATTERN_EXTRACTION_TEMPLATE — Standard Extraction Format

> A single format for every extracted coaching pattern.
> No methodology branding. No opinions. Only patterns.

---

## Extraction Rules

1. **One pattern per entry.** If a source contains multiple patterns, extract separately.
2. **No methodology names.** Replace "Westside conjugate method used" with "Maximal effort day followed by dynamic effort day in weekly undulating pattern."
3. **No opinions.** "This is the best way to train athletes" is discarded. Track only what the source does.
4. **Preserve contradictions.** If two sources disagree, both patterns are extracted and marked as contradictory.
5. **Real programs > theory.** When a manual says "do X" but a real program does "Y", the real program pattern is primary. Both are extracted — real program gets confidence ×1.5.
6. **Context matters.** Every pattern includes the conditions under which it was observed (sport, level, season phase, equipment).
7. **Frequency tracking.** Record how many programs/sources exhibit this pattern. Single-source patterns are tagged `rare`.

---

## Template Structure

```yaml
PATTERN_ID: P-XXXX
  # Unique identifier. Incremented per-new-pattern.
  # Ranges: P-0001–P-0999 (session structure)
  #         P-1000–P-1999 (warm-up)
  #         P-2000–P-2999 (power)
  #         P-3000–P-3999 (strength)
  #         P-4000–P-4999 (conditioning)
  #         P-5000–P-5999 (progression)
  #         P-6000–P-6999 (periodization)
  #         P-7000–P-7999 (recovery)
  #         P-8000–P-8999 (exercise selection)
  #         P-9000–P-9999 (coaching principles)

category: Session Structure | Warm-Up | Power | Strength | Conditioning
  | Progression | Periodization | Recovery | Exercise Selection | Coaching Principles

pattern:
  description: >
    One sentence describing what the source actually does.
    Example: "Full body sessions place knee-dominant strength before hip-dominant strength."
  conditions:
    sport: [list of sports where observed]
    level: [Beginner | Intermediate | Advanced | All]
    season_phase: [Off-Season | Pre-Season | In-Season | Transition | All]
    equipment: [Field Only | Basic Gym | Commercial Gym | Elite Facility | Any]
    athlete_type: [Youth | Adult | Masters | Return-to-Sport | Any]

variations:
  # If the pattern has different forms under different conditions
  - variation: "Description of the variation"
    conditions:
      sport: [different sport]
      level: [different level]

sources:
  - title: "Source Title"
    author: "Author / Organization"
    type: Book | Certification | Real Program | Research | Manual
    sport: "Primary sport of this source"
    credibility: 0.0-1.0
    citation: "[FORGE_SOURCE_CATALOG.md reference — e.g. TIER A: Rugby / American Football]"

frequency:
  occurrences: N       # Number of programs/sources exhibiting this pattern
  total_sources: M     # Number of sources examined for this pattern
  percentage: X%       # occurrences / total_sources * 100

contradictions:
  # If another source does the opposite, reference it here
  - pattern_id: P-XXXX
    source: "Contradicting source title"
    description: "How the contradiction manifests"

confidence: Universal | Common | Situational | Rare
  # Universal: 90-100% of sources agree. Non-negotiable.
  # Common:    50-89% of sources agree. Strong preference, not mandatory.
  # Situational: 10-49%. Dependent on conditions in the pattern entry.
  # Rare: <10% or single source. Informational, not prescriptive.

extracted_by: "FORGE Knowledge Extraction System V1"
extraction_date: "YYYY-MM-DD"
```

---

## Field Definitions

### PATTERN_ID
- System-assigned. Use the range appropriate to the category.
- When extracting, leave as TBD. Assign when entering into FORGE_PATTERN_DATABASE.md.

### pattern.description
- **Do:** "Every full body session includes at least one knee-dominant and one hip-dominant exercise."
- **Do NOT:** "The Full Body blueprint requires both knee and hip work."
- **Do NOT:** "You must always include squats and deadlifts in the same session."
- Rule: Remove methodology branding. Describe what is done, not what should be done.

### pattern.conditions
- Every condition field must be populated. If the source does not specify, use "Any."
- `sport` field uses FORGE sport taxonomy: rugby, american_football, tennis, badminton, basketball, volleyball, netball, squash, track_field, football, general.

### variations
- Use when the same source provides different forms of the pattern under different conditions.
- Example: "Full body strength pattern for in-season uses 2x/week frequency; off-season uses 3-4x/week."

### sources
- Every pattern must cite ≥1 source from FORGE_SOURCE_CATALOG.md.
- Multi-source patterns cite all sources where the pattern was observed.
- The `credibility` field is the source credibility, not pattern confidence.

### frequency
- `occurrences`: count of sources where the pattern was observed.
- `total_sources`: count of sources examined that could potentially exhibit this pattern.
- `percentage`: auto-calculated from occurrences / total_sources × 100.
- If the total_sources is unknown (early extraction), mark as "est."

### contradictions
- If this pattern directly contradicts another extracted pattern, list it here.
- Both patterns remain in the database. Neither is deleted. The contradiction is flagged for FORGE_CONSENSUS_ENGINE.md review.

### confidence
- Auto-assigned based on frequency percentage (see FORGE_CONSENSUS_ENGINE.md for exact thresholds).
- Can be manually overridden in FORGE_CONSENSUS_ENGINE.md but not in the extraction template.
- The extraction template records `frequency`; `confidence` is set by consensus review.

---

## Extraction Examples

### Example 1: Good Extraction

```yaml
PATTERN_ID: P-0007

category: Session Structure

pattern:
  description: >
    Full body sessions sequence exercises: power → knee-dominant strength →
    hip-dominant strength → upper-body push → upper-body pull → core.
  conditions:
    sport: [rugby, american_football, general]
    level: [Intermediate, Advanced]
    season_phase: [Off-Season, Pre-Season]
    equipment: [Any]
    athlete_type: [Adult]

sources:
  - title: "Rugby Off-Season Strength Program"
    author: "Professional Rugby Club"
    type: Real Program
    sport: rugby
    credibility: 0.95

frequency:
  occurrences: 5
  total_sources: 8
  percentage: 62.5%

contradictions: []

confidence: TBD  # Assigned by consensus review
```

### Example 2: Extraction with Contradiction

```yaml
PATTERN_ID: P-0042

category: Conditioning

pattern:
  description: >
    High-intensity conditioning is placed at the end of the session,
    after all strength and power work is completed.
  conditions:
    sport: [Any]
    level: [All]
    season_phase: [Any]
    equipment: [Any]
    athlete_type: [Any]

sources:
  - title: "Rugby Off-Season Strength Program"
    author: "Professional Rugby Club"
    type: Real Program
    credibility: 0.95
  - title: "FORGE Rulebook V1 (100 laws + 50 red flags)"
    author: "FORGE"
    type: Manual
    credibility: 0.85

frequency:
  occurrences: 12
  total_sources: 14
  percentage: 85.7%

contradictions:
  - pattern_id: P-0043
    source: "Sprint Development Foundation"
    description: >
      Alactic speed protocol is placed before any strength work, 
      even though it is technically conditioning, because it requires
      a fresh central nervous system (CNS).
    citation: "FORGE_CONDITIONING_LAWS: CL003 — Speed requires fresh CNS."

confidence: TBD
```

---

## Anti-Patterns (What NOT to Extract)

| Do NOT Extract | Why | Instead Extract |
|----------------|-----|-----------------|
| "The conjugate method is the best approach for team sport athletes." | Methodology branding. Opinion. | "Program alternates between maximal effort, dynamic effort, and repetition days in a weekly cycle." |
| "Every athlete should squat to parallel." | Opinion masked as fact. | "87% of programs in the corpus use full ROM squats (hip crease below knee) for at least one DLKD exercise per session." |
| "Westside Barbell uses the conjugate method." | Methodology name used as shorthand. | "Athlete performs a maximal effort lift, followed by a dynamic effort lift, followed by accessory work in a single session." |
| "This program does not include enough plyometrics." | Judgment, not pattern. | "Program allocates 0 plyometric exercises per session. 73% of programs of this type allocate ≥1 plyometric." |
| "The FORGE Rulebook states..." | Self-referential. The extraction system should not cite FORGE manuals as primary evidence unless they synthesize external sources. | Cite the original source(s) the Rulebook synthesized. |

---

## Extraction Priority

When adding new sources to the catalog, extract in this order:

1. **Real programs** (highest priority — patterns observed in practice)
2. **Certification materials** (synthesized domain consensus)
3. **Published manuals** (for verification/reference)
4. **Research literature** (for contradiction detection)
5. **Unverified templates** (lowest priority — flag as unverified)

Extract all patterns from a source before moving to the next source. Do not partial-extract.
