# FORGE Conditioning Taxonomy V2

**Goal:** Rebalance the existing conditioning library into a cleaner operating model. No new architecture.

---

## 1. Top-Level Categories

### FIELD_CONDITIONING
- **Purpose:** Conditioning for sports played on open ground / grass / turf with straight-line and multi-directional movement demands
- **Sports it serves:** Cricket, rugby, soccer, hockey, track, field events, American football
- **Protocol types:** Continuous running, straight-line intervals (tempo, MAS, RSA), multi-directional shuttles, sport-specific circuits (cricket ground, rugby readiness)
- **Should NOT contain:** Court-specific work (shuttle patterns under 10m, lateral-dominant patterns), gym equipment-only protocols, pool work

### COURT_CONDITIONING
- **Purpose:** Conditioning for sports played on confined courts with frequent directional changes, short explosive efforts, and rally-density work
- **Sports it serves:** Tennis, badminton, basketball, volleyball, squash, pickleball
- **Protocol types:** Short shuttle RSA, lateral shuffle intervals, diagonal recovery patterns, multi-directional MAS, rally simulation protocols, split-step density
- **Should NOT contain:** Long straight-line intervals (400m+), continuous running over 10 min, track-specific protocols

### GYM_CONDITIONING
- **Purpose:** Conditioning for gym-based sessions, low-impact days, equipment-restricted environments, and non-running conditioning
- **Sports it serves:** All sports — used on gym days, injury return, or when outdoor space is unavailable
- **Protocol types:** Bike intervals, rower HIIT, KB/DB circuits, treadmill work, mixed modal circuits, bodyweight conditioning
- **Should NOT contain:** Field/court only protocols (requires >30m straight-line space), grass/turf-specific work

### RECOVERY_CONDITIONING
- **Purpose:** Low-fatigue conditioning that maintains work capacity without adding significant training stress
- **Sports it serves:** All sports — used post-competition, deload weeks, or low-time days
- **Protocol types:** Active recovery (walk, jog, bike), mobility circuits, low-intensity pool work, light circuits (bodyweight with low reps)
- **Should NOT contain:** Protocols with fatigue_score > 2, maximal effort work, intervals with incomplete recovery

---

## 2. Secondary Tagging Model

Flat tag structure attached to each protocol:

| Field | Type | Values | Purpose |
|-------|------|--------|---------|
| `environment_category` | string | `field`, `court`, `gym`, `recovery` | Primary routing — which environment this protocol is meant for |
| `sport_tags` | list[str] | Sport names, `any`, or `all` | Secondary filtering — which sports this protocol serves |
| `energy_system` | string | (existing) | Kept from current taxonomy |
| `movement_pattern` | string | `continuous`, `intervals`, `shuttle`, `circuit`, `ladder`, `hill` | Format hint for coach display |
| `fatigue_score` | int | 1-5 | Existing field — kept as-is |
| `level` | string | (existing) | Kept from current taxonomy |
| `tier` | string | A/B/C | Kept from current taxonomy |

### sport_tags convention
- `["any"]` — protocol is sport-agnostic (e.g., AC-001 Long Slow Distance)
- `["cricket", "rugby", "soccer"]` — protocol works for these field sports
- `["tennis", "badminton"]` — protocol works for these court sports
- `["field_sports"]` — shorthand for all field sports
- `["court_sports"]` — shorthand for all court sports

---

## 3. Routing Logic (conceptual)

```
1. Competition proximity?
   → days_to_match == 0 → Recovery pathway
   → days_to_match == 1 → Light/reduced conditioning

2. Recovery need?
   → fatigue_level != "normal" or session_type == "recovery"
   → Route to RECOVERY_CONDITIONING

3. Movement environment?
   → environment == "ground" → FIELD_CONDITIONING
   → environment == "court" → COURT_CONDITIONING  
   → environment == "gym" → GYM_CONDITIONING

4. Goal / conditioning intent?
   → Map to energy system (existing goal_map)

5. Sport applicability?
   → Filter protocols by sport_tags matching athlete's sport
   → If no sport-tagged match, use "any" protocols as fallback

6. Level filter
   → Check level_ok (existing)

7. Time available
   → Prefer protocols that fit available time
```

---

## 4. What Changes vs Current

| Current | V2 |
|---------|-----|
| No environment category on protocols | Each protocol gets environment_category |
| No sport tags | Each protocol gets sport_tags (or "any") |
| Decision map has no "court" key | Decision map adds "court" environment |
| Selection ignores sport | Selection filters by sport_tags |
| Gym has 4 protocols | Gym gets 2-3 more |
| Court has 0 dedicated protocols | Court gets 4-6 dedicated protocols |
| Recovery has 6 protocols | Recovery gets 1-2 more low-fatigue options |
