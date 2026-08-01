# FORGE Wave 8 — Role Week Planning Audit V1.0

## What Gap Existed Before Wave 8

Prior to Wave 8, FORGE personalized:

- **Exercise selection** (Wave 5) — which specific exercises appear based on athlete profile
- **Prescription** (Wave 6) — sets, reps, intensity modifiers based on profile + role
- **Next-block bias** (Wave 7) — blueprint nudging based on prior block response

But **week architecture remained identical** for two athletes on the same blueprint regardless of sport role. A rugby prop and a backline player on "Full Body Strength" received the same:

- Session emphasis weighting across the week
- Conditioning density
- Exposure caps for sprint, landing, rotation, eccentric
- Slot ordering within the blueprint

This meant the **coaching logic was incomplete**: a prop needs more lower-strength / collision robustness and less sprint exposure than a backline player, even on the same blueprint. A fast bowler needs tightly managed landing + eccentric accumulation compared to a batter. A tennis singles player needs higher conditioning density than a doubles player.

## Where Blueprint-Only Week Planning Broke Down

### 1. Same blueprint, same caps

The hard caps in `weekly_exposure_warnings` (sprint > 4, landing > 3, high-eccentric > 3) were generic. They did not account for role-specific needs:

- A rugby prop should have **lower** sprint caps (max 2) because sprint is not their primary need
- A volleyball middle blocker should have **higher** jump/landing caps (max 5) because jumping is their primary sport action
- A cricket fast bowler should have **moderate** rotation caps because rotation matters but should be tightly managed alongside landing stress

### 2. Same blueprint, same conditioning frequency

Conditioning was added every other session (`(week + day) % 2 == 0`) regardless of role. But:

- A tennis singles player needs **higher** conditioning density than a doubles player
- A soccer goalkeeper needs **lower** conditioning density than a midfielder
- A volleyball libero needs **higher** repeat-movement conditioning than a middle blocker

### 3. Same blueprint, same slot ordering

Slots were ordered by blueprint `slot_order` only. Role could not nudge which families appear first or get dropped first under time constraints. But:

- A prop should prioritize `DLKD`, `HPush`, `Core` over `Sprint`
- A backline player should prioritize `Sprint`, `Plyo`, `Ball` over `DLKD`
- A fast bowler should prioritize `Sprint`, `Landing` but de-prioritize `Rot` and `VPush`

### 4. No coach-visible explanation

The renderer showed raw exercise counts (`3 sqt 2 hng 1 spd 0 lnd`) but did not explain:
- What the role *should* emphasize
- What the weekly exposure targets were
- Why two athletes on the same blueprint looked different

## Wave 8 Fix

Wave 8 introduces `RoleWeekProfile` — a deterministic role-aware week planning model that:

1. Defines role-specific emphasis (force, velocity, conditioning, rotation, landing, upper-body)
2. Defines role-specific exposure targets/caps (high/moderate/low for sprint, jump, decel, rotation, conditioning)
3. Defines role-specific slot bias (family priority / de-priority)
4. Defines role-specific conditioning density bias
5. Makes all of this visible in coach-facing output

The blueprint still determines **which families are available** (mandatory + optional), but role now determines **which of those families are emphasized**, **how much exposure is allowed**, and **how conditioning is distributed** across the week.

## Remaining Gaps

- **Season-phase × role interaction**: A prop in-season might need different emphasis than a prop off-season. Currently role profiles are static.
- **Goal × role interaction**: A prop with goal="speed" might need different bias than a prop with goal="strength". Currently role bias is applied uniformly.
- **Micro-cycle variation**: Role bias is applied to every week identically. More sophisticated micro-cycles (e.g., prop gets more collision work in week 1, more strength in week 3) are not yet implemented.
