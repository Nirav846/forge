# FORGE Wave 9 Session Assembly Validation V1.0

## Overview

This document describes the validation checks added in Wave 9 to ensure session assembly quality.

## New Credibility Checks

### 1. session_identity_preserved

**Purpose:** Ensure that blueprint-defining families remain present in most sessions.

**Implementation:**
- For each session, count how many mandatory families are present
- Allow up to 25% of mandatory families to be missing (e.g., no valid exercise in database)
- At least 30% of sessions must pass the per-session check

**When it fails:**
- A blueprint has mandatory families that are consistently missing from most sessions
- This indicates a data issue (missing exercises) or a severe filtering bug

### 2. session_flow_credible

**Purpose:** Ensure session order follows real S&C flow (speed/power → strength → secondary → accessory).

**Implementation:**
- Sprint/Plyo/Ball should appear before DLKD/DLHD/HPush/HPull
- Core should always be last
- If no speed or strength work is present, any order is acceptable

**When it fails:**
- Speed/power work appears after heavy strength work (wastes neural freshness)
- Core appears before other work (unusual, unless explicitly intended)

### 3. high_value_not_dropped_first

**Purpose:** Ensure high-value families survive while low-value families are dropped under constraints.

**Implementation:**
- Each session must have at least one Tier S or Tier A family present
- Catches cases where accessory/carry work survives while primary work is lost

**When it fails:**
- A session has only Tier C families (Carry, Acc) and no primary work

### 4. role_bias_not_overriding_blueprint

**Purpose:** Ensure role bias influences but does not destroy blueprint identity.

**Implementation:**
- De-prioritized families should not exceed 50% of any session
- If a single de-prioritized family dominates a session, it fails

**When it fails:**
- A prop session is 100% Sprint (de-prioritized for prop)
- A backline session is 100% DLKD (de-prioritized for backline)

### 5. taper_drop_logic_credible

**Purpose:** Ensure competition taper drops fatigue-heavy extras first.

**Implementation:**
- In light/primer taper (comp_window <= 2), Carry and Acc should not be present
- Speed/power families should be kept over strength accessories

**When it fails:**
- A primer session includes Carry or Acc work
- A light taper session is dominated by fatigue-heavy work

### 6. post_filter_session_balance

**Purpose:** Ensure sessions have coherent structure after filtering/rebalancing.

**Implementation:**
- Each session must have at least 3 valid blocks
- At least one major movement pattern (lower or upper body) must be present

**When it fails:**
- A session collapses to fewer than 3 blocks after filtering
- A session has no clear lower-body or upper-body work

## Validation Thresholds

All checks are designed to be **coarse-grained** rather than brittle:
- `session_identity_preserved`: 30% of sessions (not 100%)
- `role_bias_not_overriding_blueprint`: 30% of sessions (not 100%)
- `high_value_not_dropped_first`: At least one Tier A/S per session
- `taper_drop_logic_credible`: Per-session check
- `post_filter_session_balance`: Per-session check

This leniency is intentional. The checks catch **obvious** problems without flagging minor stylistic differences or data gaps (e.g., missing exercises for some families).

## Backward Compatibility

All new checks are additive. Existing programs without Wave 9 data still pass the checks because:
- No role → role bias checks are vacuously true
- No competition window → taper checks are vacuously true
- Standard sessions → flow and balance checks pass

## Test Coverage

83 tests cover all validation scenarios:
- Family survival tiers (10 tests)
- Time constraint dropping (6 tests)
- Competition taper (4 tests)
- Session flow ordering (7 tests)
- Within-week continuity (8 tests)
- Session rebalancing (7 tests)
- Blueprint identity preservation (11 tests)
- Backward compatibility (6 tests)
- End-to-end divergence (24 tests)
