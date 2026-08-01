# FORGE Wave 5 — Risk-Aware Exercise Rules

## How Risk Flags Modify Exercise Selection

The risk system operates at two levels:

1. **Filtering** — `is_exercise_risk_flagged()` returns True/False. Flagged exercises are removed from candidate lists entirely.
2. **Bias** — `get_exercise_personalization_bias()` returns -1, 0, or +1. Used as a tiebreaker within non-flagged candidates.

### Lumbar Risk (`lumbar_risk: True`)

**Filtering rules:**
- DLHD/SLHD exercises with `eccentric_cost >= 4` are blocked (RDL, Single-Leg RDL, Good Morning, stiff-leg variants)
- Rotational exercises with `difficulty >= 3` and IDs in HIGH_ROTATION_IDS blocked (Rot-009 through Rot-017)
- Barbell Back Squat and Front Squat at difficulty >= 4 blocked (spinal compression concern)

**Bias:**
- `less_hinge_rotation` in weekly bias → reduces hinge/rotation combination in the block

### Patellar Tendon Risk (`patellar_tendon_risk: True`)

**Filtering rules:**
- Landing exercises with `difficulty >= 3` blocked (Lateral Box Jump Stick, SL Box Jump Stick, Depth Jump Stick, etc.)
- Plyometric exercises with `difficulty >= 4` blocked
- Depth/drop squat variants blocked

**Conditioning impact:** High-impact conditioning protocols (impact >= 4) get -2 score penalty.

### Hamstring Risk (`hamstring_risk: True`)

**Filtering rules:**
- High-eccentric hinge exercises blocked (RDL, Good Morning, stiff-leg variants, eccentric_cost >= 4)
- Sprint exercises with `difficulty >= 4` blocked (Max-V Sprint, Flying 20/30m, Sled Sprint, etc.)

**Conditioning impact:** RSA and Speed Endurance protocols get -1 score penalty.

### Shoulder Overhead Risk (`shoulder_overhead_risk: True`)

**Filtering rules:**
- VPush exercises with `difficulty >= 3` blocked (Barbell Overhead Press, Push Press, etc.)
- VPull exercises with `difficulty >= 4` involving pull-up/chin-up variants blocked

**Safe alternatives remain:** Band Overhead Press (d:1), Half-Kneeling Landmine Press (d:2), and other low-difficulty overhead work are still available.

### Groin / Adductor Risk (`groin_adductor_risk: True`)

**Filtering rules:**
- Sprint exercises containing "lateral", "crossover", or "shuffle" blocked
- SLKD exercises with `difficulty >= 4` containing "lateral" blocked

**Conditioning impact:** Change of direction and court shuffle movement profiles get -1 score penalty.

### Ankle / Foot Risk (`ankle_foot_risk: True`)

**Filtering rules:**
- Plyometric exercises with `difficulty >= 4` blocked
- Landing exercises with `difficulty >= 4` blocked if single-leg
- Sprint exercises with `difficulty >= 4` blocked if "max" or "flying"

## Substitution Behavior

The substitution engine (`substitution_engine.py`) respects athlete risk flags at all 4 priority levels:

| Priority | Behavior | Risk-Aware? |
|---|---|---|
| 1. Same family, next available | Iterates priority list, returns first valid | Yes — skips risk-flagged |
| 2. Same intent, different family | Cross-family substitution within intent category | Yes — skips risk-flagged |
| 3. Same equipment, any family | Scans all exercises matching equipment | Yes — skips risk-flagged |
| 4. Emergency fallback | Returns None | N/A |

If all candidates in a family are risk-flagged, the engine falls through to the next priority level rather than silently selecting a risky exercise.

## What This Is NOT

- **Not a rehab engine.** No corrective exercises, no graded exposure protocols, no return-to-play timelines.
- **Not a diagnosis tool.** Risk flags are coach-provided inputs, not engine-inferred.
- **Not a substitute for medical advice.** The engine modifies training load, not medical treatment.
