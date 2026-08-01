# Template Inventory Audit

**Scope:** Database seed files only. No mock/repository code. No references.

---

## 1. Movement Template Inventory

| # | Name | Sport | Role | Goal (training_goal summary) | Slots | Source |
|---|---|---|---|---|---|---|
| 1 | Lower Body Power | American Football | All | "Develop rate of force development, explosive triple extension, and maximal power in the lower body." | 4 | 000004:8-14 |
| 2 | Acceleration Development | Track & Field (Sprinting) | Sprinters | "Enhance horizontal force application, landing stiffness, and initial drive phase mechanics." | 4 | 000004:16-20 |
| 3 | Rotational Power | Track & Field (Throws) | Throwers | "Maximize hip-shoulder separation, rotational velocity, and force transfer through the kinetic chain." | 4 | 000004:22-26 |
| 4 | Shoulder Robustness | Rugby | All | "Enhance glenohumeral stability, scapular control, and rotator cuff capacity to reduce injury risk in contact sports." | 4 | 000004:28-32 |
| 5 | Reactive Agility | Basketball | Guards/Forwards | "Improve landing mechanics, decelerative capacity, and stretch-shortening cycle efficiency during direction changes." | 4 | 000004:34-38 |
| 6 | Cricket Fast Bowler Power | **Cricket** | **Fast Bowler** | "Develop lower body bracing capacity, explosive triple extension, and rotational power specific to the fast bowling release phase." | 4 | 000005:14-20 |

**Total: 6 movement templates, 24 slots.**

---

## 2. Cricket Role × Goal Matrix

Query: `SELECT ... FROM movement_templates WHERE sport_id = cricket_id` returns **1 row** (template #6).

| Role | Power | Strength | Acceleration | Rotational Power | Reactive Agility | Shoulder Robustness | Mobility |
|---|---|---|---|---|---|---|---|
| **Fast Bowler** | EXISTS¹ | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING |
| **Spinner** | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING |
| **Batter** | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING |
| **Wicket Keeper** | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING |
| **All Rounder** | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING | MISSING |

¹ `Cricket Fast Bowler Power` — the only cricket-template row in the database.

### Cross-Sport Reference via deficit_movement_templates

`deficit_movement_templates` (migration 000009:227-233 and 000008:214-233) references non-Cricket templates by name without sport_id filtering. Through this junction table, the following goal templates are **theoretically reachable** for any role that triggers the mapped deficit:

| Template | Reachable Via Deficit | Source Migration |
|---|---|---|
| Lower Body Power | Power Deficit, Strength Deficit | 000009:228,230 |
| Rotational Power | Power Deficit, Rotational Core Power Deficit | 000009:229, 000008:233 |
| Acceleration Development | Acceleration Deficit, Speed Deficit | 000009:231-232 |
| Shoulder Robustness | Mobility Restriction, Local Muscular Endurance Deficit | 000009:233, 000008:237 |
| Reactive Agility | Rate of Force Development Deficit | 000008:229 |
| Cricket Fast Bowler Power | Lower Body Absolute Strength Deficit, Rate of Force Development Deficit | 000008:225,227 |

No cricket-specific mapping exists for Strength or Mobility goals.

---

## 3. Template Reality Check

| Goal Label | Real Template Row in DB? | Sport Association | Fully Seeded (slots, reqs, progressions)? |
|---|---|---|---|
| **Acceleration** | ✅ `Acceleration Development` | Track & Field (Sprinting) | ✅ 4 slots, 4 slot_req, 4 progressions, 1 fallback |
| **Rotational Power** | ✅ `Rotational Power` | Track & Field (Throws) | ✅ 4 slots, 4 slot_req, 4 progressions |
| **Reactive Agility** | ✅ `Reactive Agility` | Basketball | ✅ 4 slots, 4 slot_req, 4 progressions |
| **Shoulder Robustness** | ✅ `Shoulder Robustness` | Rugby | ✅ 4 slots, 4 slot_req, 4 progressions |

All four have **real, fully-seeded database templates**. They are not references or stubs. Each has:
- A `movement_templates` row with name, sport_id, athlete_role, training_goal
- 4 `template_slots` rows (Primary, Secondary, Accessory, Core)
- 4+ `slot_requirements` rows (exercise matching constraints)
- 4 `slot_progressions` rows (programming rules)
- (Lower Body Power and Acceleration Development additionally have `slot_exercise_fallbacks`)

The limitation is **sport association**: all four are assigned to non-Cricket sports. They are not returned by a filtered query like `WHERE sport_id = cricket_id`. They are only reachable through the `deficit_movement_templates` junction table, which bypasses sport filtering.

---

## 4. Templates That Do NOT Exist in DB Seeds

- Cricket Fast Bowler Strength (or any Strength template for Cricket)
- Cricket Spinner Power / Rotational Power (no Spinner-specific template)
- Cricket Batter Strength / Power / Acceleration (no Batter-specific template)
- Cricket Wicket Keeper template (any goal)
- Cricket All Rounder template (any goal)
- Mobility template (any sport)
- Speed Development / Speed Maintenance template (any sport — "Speed" is a `program_design_rules` quality, not a template)
- General / Foundation / Conditioning template

---

## 5. Deficit Systems Inventory

The database has **two independent deficit systems** that never intersect:

| System | Source | Deficits | Templates Referenced |
|---|---|---|---|
| Original (000008) | `deficits` seeded in 000008:160-180 | Lower Body Absolute Strength Deficit, Rate of Force Development Deficit, Rotational Core Power Deficit, Local Muscular Endurance Deficit | Lower Body Power, Cricket Fast Bowler Power, Reactive Agility, Rotational Power, Shoulder Robustness |
| Comprehensive (000009) | `deficits` seeded in 000009:173-199 | Power Deficit, Strength Deficit, Acceleration Deficit, Speed Deficit, Mobility Restriction | Lower Body Power, Rotational Power, Acceleration Development, Shoulder Robustness |

The two systems are **never joined** — no migration maps deficits from one system to the other.
