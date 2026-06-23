"""Dump ALL FORGE exercise, family, blueprint, and conditioning data."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))
sys.stdout.reconfigure(encoding='utf-8')

from forge.data import (
    EXERCISES, EXERCISE_BY_ID, EXERCISES_BY_FAMILY,
    FAMILIES, BLUEPRINTS, BLUEPRINT_BY_ID,
    CONDITIONING_PROTOCOLS, COND_PROTOCOL_BY_ID,
    COND_PROTOCOLS_BY_SYSTEM, COND_DECISION_MAP,
    CROSS_FAMILY_SUBSTITUTION, INTENT_CATEGORIES, FAMILY_TO_INTENT,
    EQUIPMENT_PROFILE_MAP,
)
from forge.models import (
    Exercise, ExerciseFamily, Blueprint, ConditioningProtocol,
    FamilyCode, Objective, SeasonPhase, BlueprintName,
    AthleteLevel, EquipmentProfile, SessionBlock, Session,
    AthleteProfile, GeneratedProgram,
)

sep = "=" * 78
dash = "-" * 78

# ── 1. EXERCISES ────────────────────────────────────────────────────
print(sep)
print("ALL EXERCISES — FULL DATA")
print(sep)
for ex in EXERCISES:
    print(f"\nID:          {ex.id}")
    print(f"Name:        {ex.name}")
    print(f"Family:      {ex.family.value}")
    print(f"Secondary:   {ex.secondary_family.value if ex.secondary_family else None}")
    print(f"Objective:   {ex.objective.value}")
    print(f"Difficulty:  {ex.difficulty}")
    print(f"Equipment:   {ex.equipment}")
    print(f"Unilateral:  {ex.unilateral}")
    print(f"Explosive:   {ex.explosive}")
    print(f"Isometric:   {ex.isometric}")
    print(f"Rotational:  {ex.rotational}")
    print(f"Progression: {ex.progression}")
    print(f"Regression:  {ex.regression}")
print(f"\nTotal exercises: {len(EXERCISES)}")

# ── 2. EXERCISES BY FAMILY ──────────────────────────────────────────
print(f"\n{dash}")
print("EXERCISES BY FAMILY")
print(dash)
for fam_id, exs in sorted(EXERCISES_BY_FAMILY.items()):
    print(f"\n{fam_id} ({len(exs)} exercises):")
    for ex in exs:
        print(f"  {ex.id}: {ex.name} [{ex.objective.value}] diff={ex.difficulty} equip={ex.equipment}")

# ── 3. FAMILIES ─────────────────────────────────────────────────────
print(f"\n{sep}")
print("EXERCISE FAMILIES")
print(sep)
for fam in FAMILIES:
    print(f"\n{fam.id.value}: {fam.name}")
    print(f"  Definition:        {fam.definition}")
    print(f"  Non-negotiable:    {fam.non_negotiable_in}")
    print(f"  Default slot:      {fam.default_slot}")
    print(f"  Selection prios:   {[(p, eid) for p, eid, _ in fam.selection_priorities]}")

# ── 4. BLUEPRINTS ───────────────────────────────────────────────────
print(f"\n{sep}")
print("BLUEPRINTS — FULL DATA")
print(sep)
for bp in BLUEPRINTS:
    print(f"\nID:              {bp.id}")
    print(f"Name:            {bp.name.value if isinstance(bp.name, BlueprintName) else bp.name}")
    print(f"Purpose:         {bp.purpose}")
    print(f"Typical athlete: {bp.typical_athlete}")
    print(f"Best training age: {bp.best_training_age}")
    print(f"Best season phase: {[sp.value for sp in bp.best_season_phase]}")
    print(f"Best frequency:  {bp.best_frequency}")
    print(f"Contraindications: {bp.contraindications}")
    print(f"Typical outcomes: {bp.typical_outcomes}")
    print(f"Progression:     {bp.progression_path.value if bp.progression_path else None}")
    print(f"Regression:      {bp.regression_path.value if bp.regression_path else None}")
    print(f"Mandatory fams:  {[f.value for f in bp.mandatory_families]}")
    print(f"Optional fams:   {[f.value for f in bp.optional_families]}")
    print(f"Slot order:      {[f.value for f in bp.slot_order]}")
    print(f"Typical duration: {bp.typical_duration}")
    print(f"Min session comp: {bp.min_session_composition}")
print(f"\nTotal blueprints: {len(BLUEPRINTS)}")

# ── 5. CONDITIONING PROTOCOLS ──────────────────────────────────────
print(f"\n{sep}")
print("CONDITIONING PROTOCOLS — FULL DATA")
print(sep)
for cp in CONDITIONING_PROTOCOLS:
    print(f"\nID:           {cp.id}")
    print(f"Name:         {cp.name}")
    print(f"Objective:    {cp.objective}")
    print(f"System:       {cp.system}")
    print(f"Level:        {cp.level}")
    print(f"Environment:  {cp.environment}")
    print(f"Duration:     {cp.duration}")
    print(f"Work desc:    {cp.work_description[:100] if len(cp.work_description) > 100 else cp.work_description}")
    print(f"Rest:         {cp.rest}")
    print(f"Sets:         {cp.sets}")
    print(f"Total volume: {cp.total_volume}")
    print(f"Fatigue:      {cp.fatigue_score}")
    print(f"Progression:  {cp.progression}")
    print(f"Regression:   {cp.regression}")
    print(f"Tier:         {cp.tier}")
    print(f"W:R ratio:    {cp.work_rest_ratio}")
print(f"\nTotal protocols: {len(CONDITIONING_PROTOCOLS)}")

# ── 6. CONDITIONING BY SYSTEM ──────────────────────────────────────
print(f"\n{dash}")
print("CONDITIONING PROTOCOLS BY SYSTEM")
print(dash)
for sys_name, protos in sorted(COND_PROTOCOLS_BY_SYSTEM.items()):
    print(f"\n{sys_name} ({len(protos)}):")
    for p in protos:
        print(f"  {p.id}: {p.name} [{p.objective}] fatigue={p.fatigue_score} tier={p.tier}")

# ── 7. CONDITIONING DECISION MAP ────────────────────────────────────
print(f"\n{dash}")
print("CONDITIONING DECISION MAP")
print(dash)
for key, val in sorted(COND_DECISION_MAP.items()):
    print(f"{key}: {val}")

# ── 8. CROSS-FAMILY SUBSTITUTION ───────────────────────────────────
print(f"\n{dash}")
print("CROSS-FAMILY SUBSTITUTION MAP")
print(dash)
for k, v in sorted(CROSS_FAMILY_SUBSTITUTION.items()):
    print(f"  {k} <-> {v}")

# ── 9. INTENT CATEGORIES ───────────────────────────────────────────
print(f"\n{dash}")
print("INTENT CATEGORIES & FAMILY-TO-INTENT MAP")
print(dash)
for intent, fams in sorted(INTENT_CATEGORIES.items()):
    print(f"\n{intent}: {fams}")
print(f"\nFamily -> Intent:")
for f, i in sorted(FAMILY_TO_INTENT.items()):
    print(f"  {f} -> {i}")

# ── 10. EQUIPMENT PROFILES ─────────────────────────────────────────
print(f"\n{dash}")
print("EQUIPMENT PROFILES")
print(dash)
for profile, equip in sorted(EQUIPMENT_PROFILE_MAP.items()):
    print(f"{profile}: {equip}")

# ── 11. MODEL SCHEMAS ──────────────────────────────────────────────
print(f"\n{sep}")
print("MODEL SCHEMAS (Dataclass Fields)")
print(sep)
import dataclasses

models = [
    Exercise, ExerciseFamily, Blueprint, ConditioningProtocol,
    SessionBlock, Session, AthleteProfile, GeneratedProgram,
    FamilyCode, Objective, SeasonPhase, BlueprintName,
    AthleteLevel, EquipmentProfile,
]
for m in models:
    print(f"\n{m.__name__}:")
    if hasattr(m, '__dataclass_fields__'):
        for fname, fld in m.__dataclass_fields__.items():
            default = ""
            if fld.default is not dataclasses.MISSING:
                default = f" = {fld.default!r}"
            elif fld.default_factory is not dataclasses.MISSING:
                default = f" = factory({fld.default_factory})"
            print(f"  {fname}: {fld.type.__name__ if hasattr(fld.type, '__name__') else fld.type}{default}")
    elif issubclass(m, Enum):
        for val in m:
            print(f"  {val.name} = {val.value!r}")
print(f"\n{sep}")
print("END OF DUMP")
print(sep)
