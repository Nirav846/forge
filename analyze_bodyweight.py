"""Targeted queries: bodyweight selections + empty slots."""

import sys, os
from collections import Counter, defaultdict
sys.path.insert(0, 'D:\\forge')
from forge_prototype import (
    load_exercises, load_blueprints, generate_session, resolve_slot_families,
    FAMILIES_SHORT,
)

random.seed(42)
exercises = load_exercises()
blueprints = load_blueprints()
levels = ["beginner", "intermediate", "advanced"]
equip_map = {"bodyweight": 0, "minimal": 1, "basic gym": 2, "full gym": 3}
ex_by_name = {e.name: e for e in exercises}

# ── Bodyweight gap family analysis ──────────────────────────────────────

print("=" * 70)
print("  BODYWEIGHT: What fills gap-family slots?")
print("=" * 70)

gap_fams = ["Ball", "DLHD", "VPush", "VPull", "HPull"]
for gf in gap_fams:
    bw_sels = []
    for bp in blueprints:
        for lvl in levels:
            diff = {"beginner": (1, 2), "intermediate": (2, 4), "advanced": (3, 5)}[lvl]
            freq = int(bp.frequency[0])
            for w in range(1, 5):
                for s in range(freq):
                    session = generate_session(exercises, bp, diff[0], diff[1], 0, w, s)
                    for fam, ex in session:
                        if fam == gf:
                            bw_sels.append((ex.name, ex.family, ex.difficulty, lvl, bp.name, w))
    print(f"\n  {gf}: {len(bw_sels)} bodyweight selections")
    ex_cnt = Counter()
    cf_cnt = 0
    for name, efam, diff, lvl, bp_name, w in bw_sels:
        ex_cnt[name] += 1
        if efam != gf:
            cf_cnt += 1
    for name, cnt in ex_cnt.most_common(15):
        ex = ex_by_name[name]
        fam_mark = " [CF]" if ex.family != gf else ""
        print(f"    {cnt:4d}x  L{ex.difficulty} {name:40s} ({ex.family}){fam_mark}")
    print(f"    --- {cf_cnt} are cross-family substitutions")

# ── Empty slot tracking ─────────────────────────────────────────────────

print()
print("=" * 70)
print("  EMPTY SLOTS (family in program but not in generated session)")
print("=" * 70)

total_empty = 0
empty_by_fam = Counter()
empty_by_combo = Counter()
for bp in blueprints:
    for lvl in levels:
        diff = {"beginner": (1, 2), "intermediate": (2, 4), "advanced": (3, 5)}[lvl]
        for eq_label, eq_lvl in equip_map.items():
            freq = int(bp.frequency[0])
            for w in range(1, 5):
                for s in range(freq):
                    session = generate_session(exercises, bp, diff[0], diff[1], eq_lvl, w, s)
                    expected = resolve_slot_families(bp.slot_order, bp.mandatory, bp.optional)
                    actual_fams = set(f for f, _ in session)
                    for fam in expected:
                        if fam not in actual_fams:
                            total_empty += 1
                            empty_by_fam[fam] += 1
                            empty_by_combo[(fam, lvl, eq_label, bp.name)] += 1

print(f"  Total empty family slots: {total_empty}")
print(f"\n  By family:")
for fam, cnt in empty_by_fam.most_common():
    print(f"    {fam:10s}: {cnt}")
print(f"\n  Worst combos:")
for (fam, lvl, eq, bp_name), cnt in empty_by_combo.most_common(30):
    print(f"    {fam:10s} {lvl:12s} {eq:12s} {bp_name:40s}: {cnt}x")

# ── Exercise overuse (repeat count distribution) ────────────────────────

print()
print("=" * 70)
print("  EXERCISE REPETITION WITHIN SAME PROGRAM (same exercise >2x)")
print("=" * 70)

heavy_repeat = []
for bp in blueprints:
    for lvl in levels:
        for eq_label, eq_lvl in equip_map.items():
            diff = {"beginner": (1, 2), "intermediate": (2, 4), "advanced": (3, 5)}[lvl]
            freq = int(bp.frequency[0])
            all_sessions = []
            for w in range(1, 5):
                for s in range(freq):
                    session = generate_session(exercises, bp, diff[0], diff[1], eq_lvl, w, s)
                    all_sessions.extend(ex.name for _, ex in session)
            name_cnt = Counter(all_sessions)
            for name, cnt in name_cnt.items():
                if cnt > 2:
                    ex = ex_by_name[name]
                    heavy_repeat.append((cnt, f"{bp.name:40s} {lvl:12s} {eq_label:12s} L{ex.difficulty} {name}"))

heavy_repeat.sort(key=lambda x: -x[0])
for cnt, desc in heavy_repeat[:30]:
    print(f"    {cnt:2d}x {desc}")

# ── Family monotony: which families always get the SAME exercise ────────

print()
print("=" * 70)
print("  NON-OBJECTIVE MATCH: L3+ strength slot getting L1-L2")
print("=" * 70)

# For advanced athletes, check if strength/family has L1-L2 exercises
misleveled = []
for bp in blueprints:
    for lvl in levels:
        for eq_label, eq_lvl in equip_map.items():
            diff = {"beginner": (1, 2), "intermediate": (2, 4), "advanced": (3, 5)}[lvl]
            freq = int(bp.frequency[0])
            for w in range(1, 5):
                for s in range(freq):
                    session = generate_session(exercises, bp, diff[0], diff[1], eq_lvl, w, s)
                    for fam, ex in session:
                        # Advanced athlete with L1 exercise
                        if lvl == "advanced" and ex.difficulty <= 1:
                            misleveled.append(f"{bp.name:40s} adv {eq_label:12s} week{w} {fam:10s} L{1} {ex.name}")
                        # Intermediate athlete with L1 exercise in week 3+
                        if lvl == "intermediate" and ex.difficulty <= 1 and w >= 3:
                            misleveled.append(f"{bp.name:40s} int {eq_label:12s} week{w} {fam:10s} L{1} {ex.name}")

for m in misleveled[:20]:
    print(f"    {m}")

if not misleveled:
    print("    None found — RC1 fix holds.")
