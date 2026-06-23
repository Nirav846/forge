#!/usr/bin/env python3
"""
FORGE Pattern Harvester — repeatable workflow to extract coaching patterns
from any source document and output directly-ingestible Pattern DB entries.

Modes:
  init       Create a new harvest session file
  add        Add a pattern to an existing harvest
  export     Export harvest as markdown (ingestible into FORGE_PATTERN_DATABASE.md)
  append     Append exported patterns directly to FORGE_PATTERN_DATABASE.md
  stats      Show pattern statistics for the database

Usage:
  python forge_pattern_harvester.py init source.yaml --title "..." --author "..."
  python forge_pattern_harvester.py add source.yaml --interactive
  python forge_pattern_harvester.py export source.yaml
  python forge_pattern_harvester.py append source.yaml
"""

import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

# ── Constants ──────────────────────────────────────────────────────────

CATEGORIES = {
    "Session Structure": (1, 999),
    "Warm-Up": (1000, 1999),
    "Power": (2000, 2999),
    "Strength": (3000, 3499),
    "Accessory": (3500, 3999),
    "Conditioning": (4000, 4999),
    "Progression": (5000, 5999),
    "Periodization": (6000, 6999),
    "Recovery": (7000, 7999),
    "Exercise Selection": (8000, 8999),
    "Coaching Principles": (9000, 9999),
}

CLASSIFICATIONS = ["Universal", "Common", "Situational", "Rare"]
SOURCE_TYPES = ["Book", "Certification", "Real Program", "Research", "Manual"]

PATTERN_DB_PATH = "FORGE_PATTERN_DATABASE.md"
HARVEST_TEMPLATE = """# Harvest Session: {title}
# Generated: {date}
# Source: {source_title} by {source_author}
# Type: {source_type} | Sport: {sport} | Credibility: {credibility}

source:
  title: "{source_title}"
  author: "{source_author}"
  organization: "{organization}"
  sport: "{sport}"
  type: "{source_type}"
  credibility: {credibility}
  priority: "{priority}"

patterns: []  # Pattern entries go here
"""


# ── Helpers ────────────────────────────────────────────────────────────

def _next_pattern_id(category: str, existing_ids: set) -> str:
    lo, hi = CATEGORIES.get(category, (9000, 9999))
    used = {int(pid) for pid in existing_ids if lo <= int(pid) <= hi}
    candidate = lo
    while candidate in used:
        candidate += 1
    if candidate > hi:
        print(f"  Warning: ID range exhausted for {category} ({lo}-{hi})")
        candidate = hi
    return f"P-{candidate:04d}"


def _load_db_ids() -> set:
    ids = set()
    if not os.path.exists(PATTERN_DB_PATH):
        return ids
    with open(PATTERN_DB_PATH) as f:
        for line in f:
            m = re.match(r".*\bP-(\d{4})\b", line)
            if m:
                ids.add(m.group(1))
    return ids


def _load_harvest(path: str) -> dict:
    import yaml
    with open(path) as f:
        return yaml.safe_load(f)


def _save_harvest(path: str, data: dict):
    import yaml
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def _classification_confidence_score(classification: str, confidence: int) -> str:
    return f"{classification} (c={confidence})"


def _format_conditions(conds: dict) -> str:
    parts = []
    for key in ["sport", "level", "season", "equipment"]:
        val = conds.get(key, ["Any"])
        if isinstance(val, list):
            parts.append(f"{key.capitalize()}: [{', '.join(val)}]")
        elif val:
            parts.append(f"{key.capitalize()}: [{val}]")
        else:
            parts.append(f"{key.capitalize()}: [Any]")
    return " ".join(parts)


def _generate_harvest_yaml_path(source_title: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9]+", "_", source_title.lower()).strip("_")
    return f"harvest_{safe}.yaml"


# ── Commands ───────────────────────────────────────────────────────────

def cmd_init(args):
    """Initialize a new harvest session file."""
    out_path = args.output or _generate_harvest_yaml_path(args.title)
    if os.path.exists(out_path):
        print(f"  Error: {out_path} already exists. Use a different name or remove it.")
        sys.exit(1)
    content = HARVEST_TEMPLATE.format(
        title=args.title,
        date=str(date.today()),
        source_title=args.title,
        source_author=args.author,
        source_type=args.type,
        sport=args.sport,
        credibility=args.credibility,
        organization=args.org or "Unknown",
        priority=args.priority or "P2",
    )
    with open(out_path, "w") as f:
        f.write(content)
    print(f"  Harvest session created: {out_path}")
    print(f"  Edit the YAML to add patterns, then run:")
    print(f"    python forge_pattern_harvester.py validate {out_path}")
    print(f"    python forge_pattern_harvester.py export {out_path}")


def cmd_add(args):
    """Add patterns interactively or from args."""
    data = _load_harvest(args.harvest)
    existing_ids = _load_db_ids()
    harvest_ids = set()
    for p in data.get("patterns", []):
        pid = p.get("id", "")
        if pid and pid.startswith("P-"):
            harvest_ids.add(pid[2:])

    if "patterns" not in data or not isinstance(data.get("patterns"), list):
        data["patterns"] = []

    if args.interactive:
        _add_interactive(data, existing_ids | harvest_ids)
    elif args.pattern and args.category:
        _add_from_args(args, data, existing_ids | harvest_ids)
    else:
        print("  Provide --interactive or --pattern + --category")
        sys.exit(1)

    _save_harvest(args.harvest, data)
    print(f"  Pattern added to {args.harvest}")


def _add_interactive(data: dict, existing_ids: set):
    print("  Entering interactive pattern entry. Empty name to finish.\n")
    while True:
        category = _prompt_choice("Category", list(CATEGORIES.keys()))
        if category is None:
            break
        pid = _next_pattern_id(category, existing_ids)
        print(f"    Assigned ID: {pid}")
        pattern = input("  Pattern description: ").strip()
        if not pattern:
            break
        sport = input("  Sport(s) comma-separated [Any]: ").strip() or "Any"
        level = input("  Level [All]: ").strip() or "All"
        season = input("  Season [Any]: ").strip() or "Any"
        equip = input("  Equipment [Any]: ").strip() or "Any"
        classification = _prompt_choice("Classification", CLASSIFICATIONS)
        confidence = _prompt_int("Confidence (1-5)", 1, 5)
        evidence = input("  Evidence quote/summary (optional): ").strip()
        contradiction = input("  Contradicts pattern ID (optional): ").strip()

        entry = {
            "id": pid,
            "category": category,
            "pattern": pattern,
            "conditions": {
                "sport": [s.strip() for s in sport.split(",")],
                "level": level,
                "season": season,
                "equipment": equip,
            },
            "classification": classification,
            "confidence": confidence,
        }
        if evidence:
            entry["evidence"] = evidence
        if contradiction:
            entry["contradiction"] = contradiction

        if "patterns" not in data or not isinstance(data["patterns"], list):
            data["patterns"] = []
        data["patterns"].append(entry)
        existing_ids.add(pid[2:])
        print(f"    Added {pid}\n")


def _prompt_choice(label: str, options: list):
    print(f"\n  {label}:")
    for i, opt in enumerate(options, 1):
        print(f"    {i}. {opt}")
    while True:
        raw = input(f"  Choice (1-{len(options)}, or empty to skip): ").strip()
        if not raw:
            return None
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(options):
                return options[idx]
        except ValueError:
            pass
        print(f"    Invalid. Enter 1-{len(options)}.")


def _prompt_int(label: str, lo: int, hi: int) -> int:
    while True:
        raw = input(f"  {label} ({lo}-{hi}): ").strip()
        try:
            val = int(raw)
            if lo <= val <= hi:
                return val
        except ValueError:
            pass


def _add_from_args(args, data: dict, existing_ids: set):
    pid = _next_pattern_id(args.category, existing_ids)
    entry = {
        "id": pid,
        "category": args.category,
        "pattern": args.pattern,
        "conditions": {
            "sport": [s.strip() for s in args.sport.split(",")] if args.sport else ["Any"],
            "level": [s.strip() for s in args.level.split(",")] if args.level and "," in args.level else (args.level or "All"),
            "season": args.season or "Any",
            "equipment": args.equipment or "Any",
        },
        "classification": args.classification or "Situational",
        "confidence": args.confidence or 3,
    }
    if args.evidence:
        entry["evidence"] = args.evidence
    if args.contradiction:
        entry["contradiction"] = args.contradiction
    if "patterns" not in data or not isinstance(data["patterns"], list):
        data["patterns"] = []
    data["patterns"].append(entry)


def cmd_export(args):
    """Export harvest patterns as markdown blocks for FORGE_PATTERN_DATABASE.md."""
    data = _load_harvest(args.harvest)
    source = data.get("source", {})
    patterns = data.get("patterns", [])
    if not patterns:
        print("  No patterns to export.")
        return

    output = []
    output.append(f"<!-- Harvested from: {source.get('title', 'Unknown')} by {source.get('author', 'Unknown')} -->\n")

    # Group by category
    by_cat: dict[str, list] = {}
    for p in patterns:
        cat = p.get("category", "Uncategorized")
        by_cat.setdefault(cat, []).append(p)

    for cat_name in CATEGORIES:
        if cat_name not in by_cat:
            continue
        entries = by_cat[cat_name]
        for p in entries:
            block = _pattern_to_md_table(p, source)
            output.append(block)

    output_str = "\n".join(output)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output_str)
        print(f"  Exported {len(patterns)} patterns to {args.output}")
    else:
        print(output_str)

    return output_str


def _pattern_to_md_table(p: dict, source: dict) -> str:
    pid = p.get("id", "P-TBD")
    cat = p.get("category", "Uncategorized")
    pattern_desc = p.get("pattern", "")
    conds = p.get("conditions", {})
    conditions_str = _format_conditions(conds)
    classification = _classification_confidence_score(
        p.get("classification", "Situational"),
        p.get("confidence", 3),
    )
    source_ref = f"{source.get('title', 'Unknown')} — {source.get('author', 'Unknown')}"
    contradictions = p.get("contradiction", "None")
    evidence = p.get("evidence", "")

    # Build a short summary line from pattern for the title
    title_words = pattern_desc.split()[:10]
    title = " ".join(title_words) + ("..." if len(pattern_desc.split()) > 10 else "")

    lines = [
        f"### {pid}: {title}",
        "",
        "| Field | Value |",
        "|-------|-------|",
        f"| **Category** | {cat} |",
        f"| **Pattern** | {pattern_desc} |",
        f"| **Conditions** | {conditions_str} |",
        f"| **Sources** | {source_ref} |",
        f"| **Classification** | {classification} |",
        f"| **Contradictions** | {contradictions} |",
    ]
    if evidence:
        lines.append(f"| **Evidence** | {evidence} |")
    lines.append("")
    return "\n".join(lines)


def cmd_validate(args):
    """Validate a harvest YAML against the extraction template rules."""
    data = _load_harvest(args.harvest)
    errors = []
    warnings = []

    source = data.get("source", {})
    required_source = ["title", "author", "sport", "type", "credibility"]
    for field in required_source:
        if not source.get(field):
            errors.append(f"  source.{field} is required")

    if source.get("type") not in SOURCE_TYPES:
        warnings.append(f"  source.type '{source.get('type')}' not in standard types: {SOURCE_TYPES}")

    patterns = data.get("patterns", [])
    if not patterns:
        warnings.append("  No patterns defined yet")

    for i, p in enumerate(patterns):
        pid = p.get("id", f"pattern[{i}]")
        if not p.get("pattern"):
            errors.append(f"  {pid}: pattern description is required")
        if p.get("pattern") and len(p["pattern"]) < 15:
            warnings.append(f"  {pid}: pattern description seems short ({len(p['pattern'])} chars)")
        if p.get("classification") not in CLASSIFICATIONS:
            errors.append(f"  {pid}: invalid classification '{p.get('classification')}'")
        conf = p.get("confidence", 0)
        if not isinstance(conf, int) or conf < 1 or conf > 5:
            errors.append(f"  {pid}: confidence must be 1-5, got {conf}")
        if not p.get("category"):
            errors.append(f"  {pid}: category is required")
        conds = p.get("conditions", {})
        if not conds:
            warnings.append(f"  {pid}: no conditions specified (assumes Any/All)")

    # Check for methodology branding in patterns
    branding_words = [
        "conjugate", "westside", "5/3/1", "smolov", "sheiko",
        "wendler", "juggernaut", "gzlcl", "best", "optimal",
        "superior", "should always", "must always", "never do",
    ]
    for i, p in enumerate(patterns):
        pid = p.get("id", f"pattern[{i}]")
        desc_lower = p.get("pattern", "").lower()
        for brand in branding_words:
            if brand in desc_lower:
                warnings.append(f"  {pid}: possible methodology branding ('{brand}'). Rephrase as neutral pattern.")

    if errors:
        print(f"  Validation FAILED — {len(errors)} error(s):")
        for e in errors:
            print(f"    {e}")
        if warnings:
            print(f"  Warnings ({len(warnings)}):")
            for w in warnings:
                print(f"    {w}")
        sys.exit(1)
    else:
        print(f"  Validation PASSED — {len(patterns)} patterns, {len(warnings)} warnings")
        for w in warnings:
            print(f"    Warning: {w}")


def cmd_append(args):
    """Export patterns and append them to FORGE_PATTERN_DATABASE.md."""
    markdown = cmd_export(args)
    if not markdown:
        return

    if not os.path.exists(PATTERN_DB_PATH):
        print(f"  Error: {PATTERN_DB_PATH} not found. Run from the FORGE root directory.")
        sys.exit(1)

    # Read current DB
    with open(PATTERN_DB_PATH) as f:
        db_content = f.read()

    # Find insertion point: before the Pattern Statistics section
    stats_marker = "## Pattern Statistics"
    if stats_marker in db_content:
        insert_pos = db_content.find(stats_marker)
        db_content = db_content[:insert_pos] + markdown + "\n" + db_content[insert_pos:]
    else:
        # Append at the end
        db_content += "\n" + markdown

    # Update pattern counts in statistics
    pattern_count = len(re.findall(r"^### P-\d{4}", db_content, re.MULTILINE))
    db_content = _update_statistics(db_content, pattern_count)

    with open(PATTERN_DB_PATH, "w") as f:
        f.write(db_content)

    print(f"  Appended to {PATTERN_DB_PATH} (now ~{pattern_count} patterns)")


def _update_statistics(content: str, total: int) -> str:
    """Update the pattern statistics table with new counts."""
    by_cat: dict[str, int] = {}
    all_ids = re.findall(r"^### (P-\d{4})", content, re.MULTILINE)
    for cat_name, (lo, hi) in CATEGORIES.items():
        cat_count = sum(1 for pid in all_ids if lo <= int(pid.split("-")[1]) <= hi)
        if cat_count > 0:
            by_cat[cat_name] = cat_count

    # Simple update: count Universal/Common/Situational/Rare markers
    univ = len(re.findall(r"\*\*Universal\*\*", content))
    comm = len(re.findall(r"\*\*Common\*\*", content))
    situ = len(re.findall(r"\*\*Situational\*\*", content))
    rare = len(re.findall(r"\*\*Rare\*\*", content))

    table_line = re.search(
        r"\| \*\*Total\*\* .*\|",
        content,
    )
    row = f"| **Total** | **{total}** | **{univ}** | **{comm}** | **{situ}** | **{rare}** | **0** |"
    if table_line:
        content = content.replace(table_line.group(), row)

    return content


def cmd_stats(args):
    """Show pattern statistics from the database."""
    if not os.path.exists(PATTERN_DB_PATH):
        print("  No FORGE_PATTERN_DATABASE.md found.")
        return
    with open(PATTERN_DB_PATH) as f:
        content = f.read()

    total = len(re.findall(r"^### P-\d{4}", content, re.MULTILINE))
    univ = len(re.findall(r"\*\*Universal\*\*", content))
    comm = len(re.findall(r"\*\*Common\*\*", content))
    situ = len(re.findall(r"\*\*Situational\*\*", content))
    rare = len(re.findall(r"\*\*Rare\*\*", content))

    print(f"\n  FORGE Pattern Database Statistics")
    print(f"  {'='*40}")
    print(f"  Total patterns: {total}")
    print(f"  Universal:      {univ}  ({univ/total*100:.0f}%)" if total else "")
    print(f"  Common:         {comm}  ({comm/total*100:.0f}%)" if total else "")
    print(f"  Situational:    {situ}  ({situ/total*100:.0f}%)" if total else "")
    print(f"  Rare:           {rare}  ({rare/total*100:.0f}%)" if total else "")

    by_cat: dict[str, int] = {}
    for cat_name, (lo, hi) in CATEGORIES.items():
        pattern_ids = re.findall(r"### (P-\d{4})", content)
        count = sum(1 for pid in pattern_ids if lo <= int(pid.split("-")[1]) <= hi)
        if count:
            by_cat[cat_name] = count
    print(f"\n  By category:")
    for name, count in sorted(by_cat.items(), key=lambda x: -x[1]):
        print(f"    {name:25s} {count}")


# ── CLI ───────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="FORGE Pattern Harvester — extract coaching patterns from any source."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # init
    p_init = sub.add_parser("init", help="Create a new harvest session")
    p_init.add_argument("--title", required=True, help="Source title")
    p_init.add_argument("--author", required=True, help="Source author/organization")
    p_init.add_argument("--type", required=True, choices=SOURCE_TYPES, help="Source type")
    p_init.add_argument("--sport", required=True, help="Primary sport")
    p_init.add_argument("--credibility", type=float, required=True, help="Credibility 0.0-1.0")
    p_init.add_argument("--org", default="", help="Organization")
    p_init.add_argument("--priority", default="P2", help="Priority P1-P5")
    p_init.add_argument("--output", help="Output YAML path")

    # add
    p_add = sub.add_parser("add", help="Add a pattern to a harvest")
    p_add.add_argument("harvest", help="Harvest YAML file")
    p_add.add_argument("--interactive", action="store_true", help="Interactive mode")
    p_add.add_argument("--category", choices=list(CATEGORIES.keys()), help="Pattern category")
    p_add.add_argument("--pattern", help="Pattern description")
    p_add.add_argument("--sport", help="Sport(s) comma-separated")
    p_add.add_argument("--level", default="All", help="Level(s) comma-separated")
    p_add.add_argument("--season", help="Season phase")
    p_add.add_argument("--equipment", help="Equipment profile")
    p_add.add_argument("--classification", choices=CLASSIFICATIONS, default="Situational")
    p_add.add_argument("--confidence", type=int, default=3)
    p_add.add_argument("--evidence", help="Evidence quote")
    p_add.add_argument("--contradiction", help="Contradicts pattern ID")

    # export
    p_exp = sub.add_parser("export", help="Export patterns as markdown")
    p_exp.add_argument("harvest", help="Harvest YAML file")
    p_exp.add_argument("--output", help="Output .md file path")

    # validate
    p_val = sub.add_parser("validate", help="Validate harvest YAML")
    p_val.add_argument("harvest", help="Harvest YAML file")

    # append
    p_app = sub.add_parser("append", help="Append patterns to FORGE_PATTERN_DATABASE.md")
    p_app.add_argument("harvest", help="Harvest YAML file")
    p_app.add_argument("--output", help="Temp output path before append")

    # stats
    sub.add_parser("stats", help="Show pattern database statistics")

    args = parser.parse_args()

    commands = {
        "init": cmd_init,
        "add": cmd_add,
        "export": cmd_export,
        "validate": cmd_validate,
        "append": cmd_append,
        "stats": cmd_stats,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
