#!/usr/bin/env python3
"""Generate 500 programs, categorize every selection, surface credibility issues."""

import sys, os, random
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(__file__))
from forge_prototype import (
    Exercise, load_exercises, load_blueprints,
    generate_session, generate_program,
    FAMILIES_SHORT, FAMILIES_LONG,
)

random.seed(42)
exercises = load_exercises()
blueprints = load_blueprints()
levels = ["beginner", "intermediate", "advanced"]
equips = ["bodyweight", "minimal", "basic gym", "full gym"]
equip_map = {"bodyweight": 0, "minimal": 1, "basic gym": 2, "full gym": 3}

# Build exercise lookup
ex_by_name = {e.name: e for e in exercises}

# ── 500-program generation ────────────────────────────────────────────────

all_selections = []  # list of (bp, level, equip, week, session, family, exercise)
empty_slots = []
overall_stats = Counter()

for bp in blueprints:
    for lvl in levels:
        for equip in equips:
            eq_lvl = equip_map[equip]
            freq = int(bp.frequency[0])
            for w in range(1, 5):
                for s in range(freq):
                    session = generate_session(exercises, bp, *{
                        "beginner": (1, 2),
                        "intermediate": (2, 4),
                        "advanced": (3, 5),
                    }[lvl], eq_lvl, w, s)
                    if session:
                        for fam, ex in session:
                            all_selections.append((bp.name, lvl, equip, w, s, fam, ex))
                            overall_stats[ex.name] += 1
                    else:
                        empty_slots.append((bp.name, lvl, equip, w, s))

print(f"Total programs: {len(blueprints) * len(levels) * len(equips)}")
print(f"Total selections: {len(all_selections)}")
print(f"Empty slots: {len(empty_slots)}")
print()

# ── Most frequently selected exercises ────────────────────────────────────

print("=" * 70)
print("  TOP 30 MOST SELECTED EXERCISES")
print("=" * 70)
for name, count in overall_stats.most_common(30):
    ex = ex_by_name[name]
    print(f"  {count:4d}x  L{ex.difficulty} {name:40s} [{ex.family:10s}] ({ex.equipment})")

# ── Exercise overuse per-program ──────────────────────────────────────────
# For each program, count how many times the same exercise appears

print()
print("=" * 70)
print("  EXERCISE OVERUSE (same exercise >1 per program)")
print("=" * 70)

# Hash by (bp, lvl, equip) = one program
overuse_examples = []
for bp in blueprints:
    for lvl in levels:
        for equip in equips:
            eq_lvl = equip_map[equip]
            freq = int(bp.frequency[0])
            program_exercises = []
            for w in range(1, 5):
                for s in range(freq):
                    session = generate_session(exercises, bp, *{
                        "beginner": (1, 2),
                        "intermediate": (2, 4),
                        "advanced": (3, 5),
                    }[lvl], eq_lvl, w, s)
                    program_exercises.extend([(w, s, fam, ex.name) for fam, ex in session])
            
            name_counts = Counter(ex_name for _, _, _, ex_name in program_exercises)
            for ex_name, cnt in name_counts.items():
                if cnt > 1:
                    overuse_examples.append((bp.name, lvl, equip, ex_name, cnt))

# Sort by most overused first
overuse_examples.sort(key=lambda x: -x[4])
print(f"  Programs with exercise repetition: {len(set((b,l,e) for b,l,e,_,_ in overuse_examples))}")
for bp, lvl, equip, ex_name, cnt in overuse_examples[:20]:
    print(f"  {ex_name:45s} appears {cnt}x in {bp:35s} {lvl:12s} {equip}")

# ── Cross-family substitution frequency ──────────────────────────────────

print()
print("=" * 70)
print("  CROSS-FAMILY SUBSTITUTION (select_exercise returned None)")
print("=" * 70)

# We need to track when substitute() was hit. We'll re-run with tracking.
# Actually, let's just check the most common low-credibility patterns.

# ── Low-credibility: L1 exercise in a high-difficulty slot ────────────────

print()
print("=" * 70)
print("  LOW-CREDIBILITY: L1 exercise in L3+ context (beyond beginner weeks 3-4)")
print("=" * 70)

l1_in_high_context = []
for bp_name, lvl, equip, w, s, fam, ex in all_selections:
    if ex.difficulty == 1 and lvl in ("intermediate", "advanced"):
        l1_in_high_context.append((bp_name, lvl, equip, w, fam, ex.name))

# Also check: beginner week 3+ with L1 (range goes to 2-3, L1 is below)
for bp_name, lvl, equip, w, s, fam, ex in all_selections:
    if ex.difficulty == 1 and lvl == "beginner" and w >= 3:
        l1_in_high_context.append((bp_name, lvl, equip, w, fam, ex.name))

print(f"  L1 in intermediate/advanced or beginner week 3+: {len(l1_in_high_context)}")
for item in l1_in_high_context[:20]:
    print(f"  {item[2]:12s} {item[1]:12s} week{item[3]} {item[4]:10s} {item[5]}")

# ── Low-credibility: same exercise used every session in a program ───────

print()
print("=" * 70)
print("  LOW-CREDIBILITY: Same family, same exercise, every session (monotony)")
print("=" * 70)

# Check: for a given (bp, lvl, equip), does every session for a given family
# use the same exercise?
family_monotony = []
for bp in blueprints:
    for lvl in levels:
        for equip in equips:
            eq_lvl = equip_map[equip]
            freq = int(bp.frequency[0])
            # For each family, track what exercise was selected per session
            fam_ex_per_week = defaultdict(set)
            for w in range(1, 5):
                for s in range(freq):
                    session = generate_session(exercises, bp, *{
                        "beginner": (1, 2),
                        "intermediate": (2, 4),
                        "advanced": (3, 5),
                    }[lvl], eq_lvl, w, s)
                    for fam, ex in session:
                        fam_ex_per_week[fam].add(ex.name)
            
            for fam, ex_names in fam_ex_per_week.items():
                if len(ex_names) == 1:
                    ex_name = list(ex_names)[0]
                    # Only flag if freq >= 3 (more than 3 times with same exercise)
                    if freq >= 3:
                        family_monotony.append((bp.name, lvl, equip, fam, ex_name))

print(f"  Families with only 1 exercise used across all sessions: {len(family_monotony)}")
for item in sorted(family_monotony, key=lambda x: -overall_stats.get(x[4], 0))[:20]:
    print(f"  {item[3]:10s} {item[4]:40s} in {item[0]:35s} {item[1]:12s} {item[2]}")

# ── Glute Bridge overuse specifically ─────────────────────────────────────

print()
print("=" * 70)
print("  GLUTE BRIDGE USAGE PATTERN (RC1 benchmark exercise)")
print("=" * 70)
gb_count = overall_stats.get("Glute Bridge", 0)
gb_contexts = [(b, l, e, w) for b, l, e, w, s, f, ex in all_selections if ex.name == "Glute Bridge"]
print(f"  Total: {gb_count} times")
gb_by_level = Counter(c[1] for c in gb_contexts)
gb_by_equip = Counter(c[2] for c in gb_contexts)
print(f"  By level: {dict(gb_by_level)}")
print(f"  By equipment: {dict(gb_by_equip)}")

# ── Empty slot analysis ───────────────────────────────────────────────────

print()
print("=" * 70)
print("  EMPTY SLOTS (substitute returned None)")
print("=" * 70)
print(f"  Total: {len(empty_slots)}")
empty_by_context = Counter((e[1], e[2]) for e in empty_slots)
for (lvl, equip), cnt in empty_by_context.most_common():
    print(f"  {lvl:12s} {equip:12s}: {cnt} slots")

# ── Bodyweight-specific selection patterns for gap families ─────────────

print()
print("=" * 70)
print("  BODYWEIGHT: What fills Ball, DLHD, VPush, VPull, HPull slots?")
print("=" * 70)

gap_fams = ["Ball", "DLHD", "VPush", "VPull", "HPull"]
for gf in gap_fams:
    bw_selections_for_gf = [(ex, bp_name, lvl, w)
                            for bp_name, lvl, equip, w, s, fam, ex in all_selections
                            if equip == "bodyweight" and fam == gf]
    print(f"\n  {gf} (bodyweight): {len(bw_selections_for_gf)} selections total")
    ex_counter = Counter()
    for ex, bp_name, lvl, w in bw_selections_for_gf:
        ex_counter[ex.name] += 1
    for ex_name, cnt in ex_counter.most_common(10):
        ex = ex_by_name[ex_name]
        print(f"    {cnt:4d}x  L{ex.difficulty} {ex_name:40s}")


# ── Cross-family substitution analysis for bodyweight ────────────────────

print()
print("=" * 70)
print("  BODYWEIGHT: Cross-family substitution detection")
print("=" * 70)

# Re-run with substitution tracking. We track which families had select_exercise fail.
# Since we can't instrument the function without modifying it, we check the pattern:
# if a family's bodyweight pool is empty at a given diff range, but selection exists,
# it MUST have come from cross-family.

# We'll check: for each bodyweight program, which (family, level) combos used exercises
# from a DIFFERENT family than the slot family.
bw_crossfam = defaultdict(list)
for bp_name, lvl, equip, w, s, fam, ex in all_selections:
    if equip != "bodyweight":
        continue
    if ex.family != fam:
        bw_crossfam[(bp_name, lvl, fam)].append(
            f"  slot={fam} used={ex.family} {ex.name} L{ex.difficulty}"
        )

# Count by original family
bw_crossfam_by_fam = Counter()
for (bp_name, lvl, fam), selections in bw_crossfam.items():
    bw_crossfam_by_fam[fam] += len(selections)

print(f"\n  Families that most frequently receive cross-family substitutions (bodyweight):")
for fam, cnt in bw_crossfam_by_fam.most_common():
    print(f"  {fam:10s}: {cnt} cross-family substitutions")
    # Show a few examples for each
    examples = 0
    for (bp_name, lvl, slot_fam), selections in bw_crossfam.items():
        if slot_fam == fam:
            for sel in selections[:3]:
                print(f"    {bp_name:35s} {lvl:12s} {sel}")
                examples += 1
                if examples >= 2:
                    break
        if examples >= 2:
            break


# ── Least-selected families (coverage gaps) ──────────────────────────────

print()
print("=" * 70)
print("  FAMILY COVERAGE (% of sessions containing each family)")
print("=" * 70)
fam_in_sessions = defaultdict(int)
total_sessions = 0
for bp in blueprints:
    for lvl in levels:
        for equip in equips:
            eq_lvl = equip_map[equip]
            freq = int(bp.frequency[0])
            for w in range(1, 5):
                for s in range(freq):
                    total_sessions += 1
                    session = generate_session(exercises, bp, *{
                        "beginner": (1, 2),
                        "intermediate": (2, 4),
                        "advanced": (3, 5),
                    }[lvl], eq_lvl, w, s)
                    fams_in_this = set(f for f, _ in session)
                    for f in fams_in_this:
                        fam_in_sessions[f] += 1

for fam in FAMILIES_SHORT:
    pct = fam_in_sessions[fam] / total_sessions * 100
    bar = "#" * int(pct / 2)
    print(f"  {fam:10s} {bar} {pct:.0f}% ({fam_in_sessions[fam]}/{total_sessions})")

# ── Bodyweight-specific analysis ──────────────────────────────────────────

print()
print("=" * 70)
print("  BODYWEIGHT-SPECIFIC: Empty slots by family")
print("=" * 70)

# For bodyweight programs, track which families caused empty slots
bw_empty_fams = defaultdict(int)
for bp in blueprints:
    for lvl in levels:
        eq_lvl = 0  # bodyweight
        freq = int(bp.frequency[0])
        for w in range(1, 5):
            for s in range(freq):
                session = generate_session(exercises, bp, *{
                    "beginner": (1, 2),
                    "intermediate": (2, 4),
                    "advanced": (3, 5),
                }[lvl], eq_lvl, w, s)
                if not session:
                    bw_empty_fams["ALL"] += 1
                else:
                    # Can't detect which families were empty from outside
                    pass

print(f"  Bodyweight programs with empty sessions: {bw_empty_fams.get('ALL', 0)}")

# Let me instrument this properly by re-running with tracking
print()
print("  (Detailed family-level empty slot tracking below)")

# Properly track empty slots per family across ALL equipment levels
from forge_prototype import resolve_slot_families

all_empty_detail = Counter()
for bp in blueprints:
    for lvl in levels:
        diff = {"beginner": (1, 2), "intermediate": (2, 4), "advanced": (3, 5)}[lvl]
        for eq_label in equips:
            eq_lvl = equip_map[eq_label]
            freq = int(bp.frequency[0])
            for w in range(1, 5):
                for s in range(freq):
                    session = generate_session(exercises, bp, diff[0], diff[1], eq_lvl, w, s)
                    expected = resolve_slot_families(bp.slot_order, bp.mandatory, bp.optional)
                    session_fams = set(f for f, _ in session)
                    for fam in expected:
                        if fam not in session_fams:
                            all_empty_detail[(fam, lvl, eq_label, bp.name)] += 1

print()
print(f"  Total empty family slots: {sum(all_empty_detail.values())}")
print()
print(f"  Empty slots by family (all equipment, up to 30):")
fam_aggr_all = Counter()
for (fam, lvl, eq, bp_name), cnt in all_empty_detail.most_common(30):
    print(f"  {fam:10s} {lvl:12s} {eq:12s} {bp_name:35s}: {cnt}x")
    fam_aggr_all[fam] += cnt
print()
print(f"  Empty slots aggregated by family:")
for fam, cnt in fam_aggr_all.most_common():
    print(f"  {fam:10s}: {cnt}x")
