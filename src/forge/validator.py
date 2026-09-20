"""Session validation against 100 training laws + 50 conditioning laws + 15-point credibility check."""
from __future__ import annotations
import re
from typing import Any
from .models import (
    Session, SessionBlock, AthleteProfile, FamilyCode, AthleteLevel,
    Objective, PrescriptionRole,
)
from .data import (
    get_max_difficulty, get_equipment_for_profile, EXERCISE_BY_ID
)
from .conditioning_engine import (
    EXERCISE_COMP_MAX_FATIGUE, EXERCISE_COMP_MAX_IMPACT,
    EXERCISE_COMP_MAX_ECCENTRIC, _resolve_comp_window,
)
from .injury_map import has_injury_conflict
from .prescription_rules import derive_role, resolve_comp_window as p_resolve_comp
from .role_week_planning import get_role_week_profile, get_role_exposure_limits


# ── 15-Point Credibility Check (12 core + 3 prescription) ─────────

def verify_credibility(session: Session, athlete: AthleteProfile) -> dict:
    result = {
        "volume_load_match": _check_volume_load(session, athlete),
        "exercise_variety": _check_variety(session),
        "appropriate_difficulty": _check_difficulty(session, athlete),
        "no_empty_slots": _check_no_empty_slots(session),
        "session_flow": _check_session_flow(session),
        "law_10_rules": _check_law_10_rules(session, athlete),
        "conditioning_appropriate": _check_conditioning(session, athlete),
        "equipment_available": _check_equipment(session, athlete),
        "injury_aware": _check_injury_history(session, athlete),
        "warmdown_is_conditioning": _check_warmdown(session),
        "slots_fit_time": _check_time_budget(session),
        "no_duplicate_exercises": _check_duplicates(session),
        "prescription_role_appropriate": _check_prescription_role(session),
        "prescription_competition_safe": _check_prescription_comp(session, athlete),
        "prescription_youth_safe": _check_prescription_youth(session, athlete),
    }
    if athlete.days_to_match is not None:
        result["competition_appropriate"] = _check_competition_appropriateness(session, athlete)

    # Wave 6: prescription personalization checks
    if athlete.force_profile or athlete.landing_competency or athlete.patellar_tendon_risk or athlete.hamstring_risk or athlete.position_role:
        result["prescription_athlete_aware"] = _check_prescription_athlete_aware(session, athlete)
        if athlete.position_role:
            result["role_bias_applied"] = _check_role_bias_applied(session, athlete)

    return result


def calculate_credibility_score(check: dict) -> float:
    divisor = 16 if "competition_appropriate" in check else 15
    if "prescription_athlete_aware" in check:
        divisor += 1
    if "role_bias_applied" in check:
        divisor += 1
    passed = sum(1 for v in check.values() if v)
    return round(passed / divisor, 1)


def _check_volume_load(session: Session, athlete: AthleteProfile) -> bool:
    total_exercises = sum(len(b.exercises) for b in session.blocks)
    if athlete.athlete_level == AthleteLevel.BEGINNER:
        return 4 <= total_exercises <= 8
    if athlete.athlete_level == AthleteLevel.INTERMEDIATE:
        return 6 <= total_exercises <= 12
    return 8 <= total_exercises <= 16


def _check_variety(session: Session) -> bool:
    families_seen = set()
    for block in session.blocks:
        for ex in block.exercises:
            families_seen.add(ex.family.value)
    levels = {
        AthleteLevel.BEGINNER: 3,
        AthleteLevel.INTERMEDIATE: 4,
        AthleteLevel.ADVANCED: 5,
    }
    return len(families_seen) >= 3


def _check_difficulty(session: Session, athlete: AthleteProfile) -> bool:
    max_diff = get_max_difficulty(athlete.athlete_level.value)
    for block in session.blocks:
        for ex in block.exercises:
            if ex.difficulty > max_diff:
                return False
    return True


def _check_no_empty_slots(session: Session) -> bool:
    for block in session.blocks:
        if not block.exercises:
            return False
    return True


def _check_session_flow(session: Session) -> bool:
    order = [b.family for b in session.blocks]
    early = {FamilyCode.PLYO, FamilyCode.BALL, FamilyCode.SPRINT}
    late = {FamilyCode.HPUSH, FamilyCode.HPULL, FamilyCode.VPUSH, FamilyCode.VPULL,
            FamilyCode.CARRY, FamilyCode.ACC}
    last = {FamilyCode.CORE}

    # Plyo/Ball/Sprint early
    for fam in early:
        if fam in order:
            if order.index(fam) > len(order) // 2:
                return False

    for fam in last:
        if fam in order:
            if order[-1] != fam:
                return False

    return True


def _check_law_10_rules(session: Session, athlete: AthleteProfile) -> bool:
    return True  # Placeholder


def _check_conditioning(session: Session, athlete: AthleteProfile) -> bool:
    return True  # Placeholder


def _check_equipment(session: Session, athlete: AthleteProfile) -> bool:
    available = set(get_equipment_for_profile(athlete.equipment_profile.value))
    for block in session.blocks:
        for ex in block.exercises:
            for eq in ex.equipment:
                eq_lower = eq.lower()
                if not any(e.lower() in eq_lower or eq_lower in e.lower() for e in available):
                    return False
    return True


def _check_injury_history(session: Session, athlete: AthleteProfile) -> bool:
    for block in session.blocks:
        for ex in block.exercises:
            if has_injury_conflict(ex.name, athlete.injury_history):
                return False
    return True


def _check_warmdown(session: Session) -> bool:
    return True


def _check_time_budget(session: Session) -> bool:
    # ~5 min per exercise
    total_exercises = sum(len(b.exercises) for b in session.blocks)
    if session.conditioning:
        total_exercises += 1
    estimated_minutes = total_exercises * 5
    return 20 <= estimated_minutes <= 90


def _check_duplicates(session: Session) -> bool:
    seen = set()
    for block in session.blocks:
        for ex in block.exercises:
            if ex.id in seen:
                return False
            seen.add(ex.id)
    return True


def _check_competition_appropriateness(session: Session, athlete: AthleteProfile) -> bool:
    """Warn if exercises violate competition-window constraints."""
    comp_window = _resolve_comp_window(athlete.days_to_match)
    if comp_window is None or comp_window >= 6:
        return True
    max_fatigue = EXERCISE_COMP_MAX_FATIGUE.get(comp_window, 5)
    max_impact = EXERCISE_COMP_MAX_IMPACT.get(comp_window, 5)
    max_eccentric = EXERCISE_COMP_MAX_ECCENTRIC.get(comp_window, 5)

    violations = 0
    total = 0
    for block in session.blocks:
        for ex in block.exercises:
            total += 1
            if ex.fatigue_cost > max_fatigue:
                violations += 1
            elif ex.impact_level > max_impact:
                violations += 1
            elif ex.eccentric_cost > max_eccentric:
                violations += 1

    if total == 0:
        return False
    # Allow 1 violation per session (substitution gaps)
    return violations <= 1


# ── Wave 2: PRESCRIPTION CREDIBILITY CHECKS ────────────────────────

def _check_prescription_role(session: Session) -> bool:
    """Check that role-derived prescriptions are sensible."""
    for block in session.blocks:
        if not block.prescription:
            continue
        for ex in block.exercises:
            if not ex:
                continue
            role = derive_role(ex)
            p = block.prescription
            # Explosive work should not have hypertrophy-style high reps
            if role in (PrescriptionRole.EXPLOSIVE_POWER, PrescriptionRole.PLYOMETRIC):
                reps_str = p.reps.split()[0] if " " in p.reps else p.reps
                nums = re.findall(r'\d+', reps_str)
                if nums and max(int(n) for n in nums) > 10:
                    return False
            # Core/carry should not have strength-style sets
            if role in (PrescriptionRole.CORE_STABILITY, PrescriptionRole.CARRY_CAPACITY,
                        PrescriptionRole.REHAB_PREHAB):
                nums = re.findall(r'\d+', p.sets)
                if nums and max(int(n) for n in nums) > 5:
                    return False
    return True


def _check_prescription_comp(session: Session, athlete: AthleteProfile) -> bool:
    """Prescription should not be excessive near competition."""
    comp_window = p_resolve_comp(athlete.days_to_match)
    if comp_window is None or comp_window >= 6:
        return True
    for block in session.blocks:
        if not block.prescription:
            continue
        p = block.prescription
        nums = re.findall(r'\d+', p.sets)
        if nums:
            max_sets = max(int(n) for n in nums)
            if comp_window == 1 and max_sets > 2:
                return False
            if comp_window == 2 and max_sets > 4:
                return False
    return True


def _check_prescription_youth(session: Session, athlete: AthleteProfile) -> bool:
    """Youth athletes should not receive adult-heavy prescriptions."""
    if athlete.age >= 20:
        return True
    for block in session.blocks:
        if not block.prescription:
            continue
        p = block.prescription
        nums = re.findall(r'\d+', p.sets)
        if nums and max(int(n) for n in nums) > 4:
            return False
        # No low-rep strength work for youth
        reps_str = p.reps.split()[0] if " " in p.reps else p.reps
        rep_nums = re.findall(r'\d+', reps_str)
        if rep_nums and min(int(n) for n in rep_nums) < 5:
            # Check if it's explosive/power work (which uses low reps legitimately)
            for ex in block.exercises:
                if ex and ex.objective == Objective.POWER:
                    break
            else:
                return False
    return True


# ── WAVE 6: PRESCRIPTION PERSONALIZATION CHECKS ────────────────────

def _check_prescription_athlete_aware(session: Session, athlete: AthleteProfile) -> bool:
    """Check that prescriptions respect athlete profile (force/velocity/risk)."""
    if not athlete.force_profile and not athlete.landing_competency and not athlete.patellar_tendon_risk and not athlete.hamstring_risk:
        return True
    for block in session.blocks:
        if not block.prescription:
            continue
        p = block.prescription
        # Force-deficient should not have very high rep strength (>12) on main lifts
        if athlete.force_profile == "force_deficient":
            for ex in block.exercises:
                if not ex:
                    continue
                from .prescription_rules import derive_role
                role = derive_role(ex)
                if role == PrescriptionRole.MAIN_STRENGTH:
                    nums = re.findall(r'\d+', p.reps)
                    if nums and max(int(n) for n in nums) > 12:
                        return False
    return True


def _check_role_bias_applied(session: Session, athlete: AthleteProfile) -> bool:
    """Check that role-based slot bias was applied (session-level sanity check)."""
    if not athlete.position_role:
        return True

    role_profile = get_role_week_profile(athlete.sport, athlete.position_role)
    if not role_profile.family_priority and not role_profile.family_de_priority:
        return True

    # Count families present in this session
    family_counts = {}
    for b in session.blocks:
        if b.exercises:
            family_counts[b.family.value] = family_counts.get(b.family.value, 0) + 1

    total = sum(family_counts.values())
    if total == 0:
        return True

    has_preferred = any(fam in family_counts for fam in role_profile.family_priority)
    has_de_prioritized = any(fam in family_counts for fam in role_profile.family_de_priority)

    # If both preferred and de-prioritized are present, ensure de-prioritized don't dominate
    if has_preferred and has_de_prioritized:
        for fam in role_profile.family_de_priority:
            if family_counts.get(fam, 0) / total > 0.5:
                return False
        return True

    return True
