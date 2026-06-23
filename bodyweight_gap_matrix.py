#!/usr/bin/env python3
"""Phase 2: Bodyweight Gap Matrix for FORGE.

For each family × difficulty (L1–L5), shows:
- Current bodyweight exercises (equip_ok(0) == True)
- Missing levels
- Blueprint demand frequency
- Proposed minimum additions with justifications
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from forge_prototype import Exercise, load_exercises, load_blueprints, FAMILIES_SHORT, FAMILIES_LONG

exercises = load_exercises()
blueprints = load_blueprints()

# ── Classify bodyweight-accessible ──────────────────────────────────────

def bw_ok(ex: Exercise) -> bool:
    """True if the exercise is accessible at equipment level 0."""
    return ex.min_equip_level() == 0

# ── Per-family, per-difficulty inventory ─────────────────────────────────

def build_matrix():
    """Build dict: family -> { diff -> [Exercise] } for bodyweight exercises."""
    m = {f: {d: [] for d in range(1, 6)} for f in FAMILIES_SHORT}
    for ex in exercises:
        if bw_ok(ex):
            m[ex.family][ex.difficulty].append(ex)
    return m

matrix = build_matrix()

# ── Blueprint demand: how often each family is referenced ────────────────

from collections import Counter

fam_demand = Counter()
for bp in blueprints:
    for slot in bp.slot_order:
        for p in [s.strip() for s in slot.split("/")]:
            if p in FAMILIES_SHORT:
                fam_demand[p] += 1
    for f in bp.mandatory:
        fam_demand[f] += 1
    for f in bp.optional:
        if f == "All":
            for f2 in FAMILIES_SHORT:
                fam_demand[f2] += 1
        else:
            fam_demand[f] += 1

# ── Blueprint frequency per level (simplified) ──────────────────────────
# Count how many blueprint-level combos reference this family as mandatory
from collections import defaultdict

bp_level_counts = defaultdict(lambda: defaultdict(int))
for bp in blueprints:
    for level in ["beginner", "intermediate", "advanced"]:
        fams = set(bp.mandatory)
        for f in bp.optional:
            if f == "All":
                fams.update(FAMILIES_SHORT)
            else:
                fams.add(f)
        for f in fams:
            bp_level_counts[f][level] += 1

# ── Report ───────────────────────────────────────────────────────────────

def fmt_ex(ex: Exercise) -> str:
    return f"  L{ex.difficulty} {ex.name:40s} ({ex.equipment})"

def gap_severity(count: int) -> str:
    if count >= 2:
        return "ok"
    elif count == 1:
        return "thin"
    return "GAP"

print("=" * 80)
print("  BODYWEIGHT GAP MATRIX")
print(f"  Total exercises: {len(exercises)}  Bodyweight-accessible: {sum(1 for e in exercises if bw_ok(e))}")
print("=" * 80)

proposals = []

for fam in FAMILIES_SHORT:
    long = FAMILIES_LONG.get(fam, fam)
    print(f"\n{'─' * 80}")
    print(f"  {fam} — {long}")
    print(f"  Blueprint demand: {fam_demand[fam]} total references")
    print(f"  Blueprints per level: beginner={bp_level_counts[fam]['beginner']}  "
          f"intermediate={bp_level_counts[fam]['intermediate']}  "
          f"advanced={bp_level_counts[fam]['advanced']}")
    print(f"{'─' * 80}")

    total_bw = 0
    gaps = []
    for diff in range(1, 6):
        exs = matrix[fam][diff]
        status = gap_severity(len(exs))
        print(f"\n  L{diff} ({status})")
        if exs:
            total_bw += len(exs)
            for ex in exs:
                print(f"  {ex.name:42s}  [{ex.equipment}]")
        else:
            print(f"  (no bodyweight exercises)")
            gaps.append(diff)

    print(f"\n  Bodyweight total: {total_bw}  |  Gaps: {gaps if gaps else 'none'}")

    # ── Propose additions for gaps ──
    if gaps and total_bw < 2:
        reason = ""
        if fam in ("DLKD", "DLHD", "SLKD", "SLHD", "HPush", "HPull", "Core"):
            reason = "Foundation family — appears in 8+ blueprints, mandatory in most programs."
        elif fam in ("VPush", "VPull"):
            reason = "Required in Upper/Lower Split and Youth Foundation; often optional elsewhere."
        elif fam in ("Plyo", "Ball"):
            reason = "Power maintenance and sport development families."
        elif fam == "Sprint/COD":
            reason = "Critical for sport AD, Sprint Dev, Court Sport blueprints."
        elif fam == "Rot":
            reason = "Court Sport, Power + Speed occasionally need rotational work."
        elif fam == "Carry":
            reason = "Core alternative; Rugby, Strength+Conditioning use it."
        elif fam == "Acc/Prehab":
            reason = "Return to Sport and Deload depend on it; all programs benefit."

        proposals.append((fam, gaps, reason, total_bw))
        print(f"\n  >>> PROPOSED ADDITIONS: fill L{gaps} gaps")
        print(f"  >>> Justification: {reason}")

# ── Summary table ────────────────────────────────────────────────────────

print(f"\n\n{'=' * 80}")
print("  SUMMARY: FAMILIES REQUIRING ADDITIONS (bodyweight gap)")
print(f"{'=' * 80}")
print(f"\n{'Family':12s} {'Gaps':12s} {'Current':8s} {'Blueprint Ref':12s} {'Priority':8s}  Justification")
print(f"{'─'*12} {'─'*12} {'─'*8} {'─'*12} {'─'*8}  {'─'*40}")

priority_order = sorted(
    proposals,
    key=lambda p: (-fam_demand[p[0]], p[3]),  # highest demand first
)

for fam, gaps, reason, total_bw in priority_order:
    demand = fam_demand[fam]
    if demand >= 10:
        pri = "P0"
    elif demand >= 6:
        pri = "P1"
    elif demand >= 3:
        pri = "P2"
    else:
        pri = "P3"
    print(f"{fam:12s} {str(gaps):12s} {total_bw:<8d} {demand:<12d} {pri:8s}  {reason[:50]}")

# ── Detailed blueprint frequency ────────────────────────────────────────

print(f"\n\n{'=' * 80}")
print("  BLUEPRINT REFERENCE FREQUENCY (bodyweight demand)")
print(f"{'=' * 80}")
print(f"\n{'Blueprint':40s} {'Freq':6s} {'Mandatory':30s} {'Notes'}")
print(f"{'─'*40} {'─'*6} {'─'*30} {'─'*40}")
for bp in blueprints:
    print(f"{bp.name:40s} {bp.frequency:6s} {', '.join(bp.mandatory):30s} {bp.notes[:40]}")
