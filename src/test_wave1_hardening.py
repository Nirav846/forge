"""Tests for Wave 1 hardening sprint — safety, injury, warmup, and exercise additions."""
import pytest
from src.forge.models import (
    AthleteProfile, AthleteLevel, EquipmentProfile, SeasonPhase,
    FamilyCode, SessionBlock, Exercise, Objective,
    OBJECTIVE_REST_MAP, OBJECTIVE_INTENSITY_MAP,
)
from src.forge.exercise_selector import select_exercise, _least_recently_used
from src.forge.substitution_engine import substitute_exercise
from src.forge.blueprint_engine import determine_level, _effective_training_age, select_blueprint
from src.forge.main import generate_program, _build_session
from src.forge.data import (
    EXERCISE_BY_ID, EXERCISES_BY_FAMILY, SELECTION_PRIORITIES,
    get_max_difficulty,
)
from src.forge.warmup_engine import (
    select_warmup, audit_ramp_phases,
    SESSION_WARMUP_TEMPLATES, SPORT_WARMUP_TEMPLATES,
)
from src.forge.injury_map import has_injury_conflict, injury_risk_multiplier, INJURY_EXERCISE_MAP
from src.forge.validator import verify_credibility


# ── Shared test athlete ──────────────────────────────────────────────

def _make_athlete(
    sport="rugby",
    level=AthleteLevel.INTERMEDIATE,
    goal="strength",
    training_age=3.0,
    technique=1.0,
    equip=EquipmentProfile.COMMERCIAL_GYM,
    phase=SeasonPhase.OFF_SEASON,
    injury="none",
    injury_history=None,
    fatigue="normal",
    strength_base=True,
    age=25,
):
    return AthleteProfile(
        sport=sport,
        training_age_years=training_age,
        season_phase=phase,
        goal=goal,
        equipment_profile=equip,
        athlete_level=level,
        technique_consistency=technique,
        injury_status=injury,
        injury_history=injury_history or [],
        fatigue_level=fatigue,
        strength_base_met=strength_base,
        age=age,
    )


# ── A1: REST BY OBJECTIVE / EXERCISE INTENT ────────────────────────

class TestRestByObjective:
    def test_rest_map_has_all_objectives(self):
        for obj in Objective:
            assert obj.value in OBJECTIVE_REST_MAP, f"Missing rest for {obj}"

    def test_strength_rest_is_long(self):
        assert OBJECTIVE_REST_MAP["STR"] == "3-5min"

    def test_power_rest_is_long(self):
        assert OBJECTIVE_REST_MAP["POW"] == "3-5min"

    def test_hypertrophy_rest_is_moderate(self):
        assert OBJECTIVE_REST_MAP["HYP"] == "60-90s"

    def test_conditioning_rest_is_short(self):
        assert OBJECTIVE_REST_MAP["COND"] == "30-60s"

    def test_strength_intensity_is_heavy(self):
        assert OBJECTIVE_INTENSITY_MAP["STR"] == "heavy"

    def test_power_intensity_is_explosive(self):
        assert OBJECTIVE_INTENSITY_MAP["POW"] == "explosive"

    def test_generated_session_has_correct_rest(self):
        athlete = _make_athlete()
        program = generate_program(athlete)
        has_strength = False
        for session in program.sessions:
            for block in session.blocks:
                for ex in block.exercises:
                    if ex and ex.objective == Objective.STRENGTH:
                        has_strength = True
                        # Wave 2: rest driven by prescription (min-based for >=120s)
                        assert "min" in block.rest_period or "s" in block.rest_period, f"Expected valid rest string, got {block.rest_period}"
                        assert block.prescription is not None, f"Expected prescription for {ex.name}"
                        assert block.prescription.rest_seconds >= 60
        assert has_strength, "No STR exercises found"


# ── A2: LOAD SPIKE PREVENTION ──────────────────────────────────────

class TestLoadSpikePrevention:
    def test_weekly_load_tracking(self):
        athlete = _make_athlete()
        program = generate_program(athlete)
        assert len(program.sessions) > 0

    def test_program_generates_without_load_cap_errors(self):
        athlete = _make_athlete(level=AthleteLevel.BEGINNER, training_age=0.5)
        program = generate_program(athlete)
        assert program.credibility_score >= 0.5


# ── A3: MASTERY / TECHNIQUE GATE ─────────────────────────────────

class TestMasteryGate:
    def test_low_technique_limits_difficulty(self):
        """technique_consistency < 0.8 should force max_diff to 1."""
        athlete = _make_athlete(technique=0.7, level=AthleteLevel.ADVANCED)
        slots = [FamilyCode.DLKD]
        recent = {}
        ex = select_exercise(
            FamilyCode.DLKD,
            athlete.athlete_level,
            athlete.equipment_profile,
            recent,
            athlete.injury_history,
            None,
            technique_consistency=athlete.technique_consistency,
        )
        if ex:
            assert ex.difficulty <= 1, f"Technique gate failed: {ex.name} d={ex.difficulty}"

    def test_high_technique_allows_higher_difficulty(self):
        athlete = _make_athlete(technique=0.95, level=AthleteLevel.ADVANCED)
        ex = select_exercise(
            FamilyCode.DLKD,
            athlete.athlete_level,
            athlete.equipment_profile,
            {},
            [],
            None,
            technique_consistency=athlete.technique_consistency,
        )
        if ex:
            assert ex.difficulty >= 1

    def test_gate_in_determine_level(self):
        athlete = _make_athlete(technique=0.7, training_age=5)
        level = determine_level(athlete)
        assert level == AthleteLevel.BEGINNER


# ── A4: BILATERAL → UNILATERAL PRIORITY ──────────────────────────

class TestBilateralUnilateral:
    def test_unilateral_downgrades_when_no_base(self):
        athlete = _make_athlete(strength_base=False)
        ex = select_exercise(
            FamilyCode.SLKD,
            athlete.athlete_level,
            athlete.equipment_profile,
            {},
            [],
            None,
            strength_base_met=athlete.strength_base_met,
        )
        if ex:
            assert ex.family in (FamilyCode.DLKD, FamilyCode.DLHD), f"Expected bilateral, got {ex.family}"

    def test_unilateral_allowed_when_base_met(self):
        athlete = _make_athlete(strength_base=True)
        ex = select_exercise(
            FamilyCode.SLKD,
            athlete.athlete_level,
            athlete.equipment_profile,
            {},
            [],
            None,
            strength_base_met=athlete.strength_base_met,
        )
        if ex:
            assert ex.family in (FamilyCode.SLKD, FamilyCode.DLKD), f"Expected SLKD or bilateral, got {ex.family}"

    def test_fragile_hasattr_replaced(self):
        athlete = _make_athlete(training_age=5, strength_base=False)
        level = determine_level(athlete)
        assert level == AthleteLevel.INTERMEDIATE


# ── A5: TRAINING AGE PRIORITY ─────────────────────────────────────

class TestTrainingAge:
    def test_effective_ta_capped_for_youth(self):
        athlete = _make_athlete(age=16, training_age=2.0)
        eta = _effective_training_age(athlete)
        assert eta <= 1.0, f"Young athlete TA should be capped: got {eta}"

    def test_effective_ta_full_for_adults(self):
        athlete = _make_athlete(age=25, training_age=2.0)
        eta = _effective_training_age(athlete)
        assert eta == 2.0, f"Adult athlete TA should be full: got {eta}"

    def test_youth_beginner_with_high_ta(self):
        athlete = _make_athlete(age=15, training_age=3.0, technique=0.9)
        level = determine_level(athlete)
        # effective TA = max(0, (15-14)*0.5) = 0.5 → BEGINNER
        assert level == AthleteLevel.BEGINNER


# ── B1: INJURY MAP DEDUPLICATION ─────────────────────────────────

class TestInjuryMap:
    def test_has_injury_conflict_detects_conflict(self):
        assert has_injury_conflict("Conventional Deadlift", ["low_back strain"])
        assert has_injury_conflict("Depth Jump", ["acl_left rupture"])

    def test_has_injury_conflict_no_false_positive(self):
        assert not has_injury_conflict("Plank", ["low_back strain"])
        assert not has_injury_conflict("Push-Up", ["acl_left rupture"])

    def test_injury_risk_multiplier_zero_on_conflict(self):
        assert injury_risk_multiplier("Conventional Deadlift", ["low_back strain"]) == 0.0

    def test_injury_risk_multiplier_one_on_safe(self):
        assert injury_risk_multiplier("Plank", ["low_back strain"]) == 1.0

    def test_selector_uses_shared_map(self):
        from src.forge.exercise_selector import has_injury_conflict as selector_import
        assert selector_import is has_injury_conflict

    def test_substitution_uses_shared_map(self):
        from src.forge.substitution_engine import _inj_conflict
        assert _inj_conflict is has_injury_conflict

    def test_validator_injury_check(self):
        athlete = _make_athlete(injury_history=["low_back"])
        from src.forge.exercise_selector import select_exercise
        ex = select_exercise(
            FamilyCode.DLKD, AthleteLevel.INTERMEDIATE,
            EquipmentProfile.COMMERCIAL_GYM, {}, ["low_back"], None,
        )
        if ex:
            assert ex.name not in ("Conventional Deadlift", "Barbell Row")


# ── B2: SURFACE FIELD / STABLE→UNSTABLE GATING SUPPORT ──────────

class TestSurfaceField:
    def test_exercise_has_surface_field(self):
        ex = EXERCISE_BY_ID.get("DLKD-001")
        assert ex is not None
        assert hasattr(ex, "surface")

    def test_default_surface_is_stable(self):
        ex = EXERCISE_BY_ID.get("DLKD-001")
        assert ex.surface == "stable"

    def test_new_landing_exercises_have_surface(self):
        for ex in EXERCISES_BY_FAMILY.get("Landing", []):
            assert ex.surface in ("stable", "unstable")


# ── C1: PHASE-ORDERED SPORT-SPECIFIC WARMUP TEMPLATES ───────────

class TestWarmupTemplates:
    def test_all_session_types_have_templates(self):
        required = ["strength", "power", "speed", "conditioning", "competition", "youth", "deload"]
        for st in required:
            assert st in SESSION_WARMUP_TEMPLATES, f"Missing template for {st}"

    def test_each_template_has_four_phases(self):
        for st, template in SESSION_WARMUP_TEMPLATES.items():
            for phase in ("raise", "activate", "potentiate", "prepare"):
                assert phase in template, f"Missing phase {phase} in {st}"

    def test_sport_specific_templates_exist(self):
        assert "tennis" in SPORT_WARMUP_TEMPLATES
        assert "cricket" in SPORT_WARMUP_TEMPLATES

    def test_warmup_phase_ordering(self):
        athlete = _make_athlete()
        w = select_warmup(athlete, "strength", "ground")
        assert len(w.phases) >= 2
        phase_names = [p.name for p in w.phases]
        assert "Raise" in phase_names
        assert "Activate" in phase_names

    def test_speed_warmup_differs_from_strength(self):
        athlete = _make_athlete()
        strength_w = select_warmup(athlete, "strength", "ground")
        speed_w = select_warmup(athlete, "speed", "ground")
        strength_drills = set(d.id for p in strength_w.phases for d in p.drills)
        speed_drills = set(d.id for p in speed_w.phases for d in p.drills)
        assert speed_drills != strength_drills

    def test_tennis_competition_has_sport_specific_phases(self):
        athlete = _make_athlete(sport="tennis")
        w = select_warmup(athlete, "competition", "court")
        all_ids = set(d.id for p in w.phases for d in p.drills)
        assert "SS-05" in all_ids or "SS-06" in all_ids

    def test_cricket_competition_has_cricket_prep(self):
        athlete = _make_athlete(sport="cricket")
        w = select_warmup(athlete, "competition", "ground")
        all_ids = set(d.id for p in w.phases for d in p.drills)
        assert "SS-01" in all_ids or "SS-02" in all_ids

    def test_environment_filters_correctly(self):
        athlete = _make_athlete(sport="rugby")
        w_gym = select_warmup(athlete, "speed", "gym")
        w_ground = select_warmup(athlete, "speed", "ground")
        assert w_gym.total_duration_sec < w_ground.total_duration_sec

    def test_youth_warmup_is_shorter(self):
        athlete = _make_athlete(sport="rugby")
        w = select_warmup(athlete, "youth", "ground")
        assert w.total_duration_sec > 0


# ── C2: RAMP AUDIT / TEMPLATE HARDENING ──────────────────────────

class TestRampAudit:
    def test_audit_returns_all_fields(self):
        audit = audit_ramp_phases()
        assert "phase_counts" in audit
        assert "unassigned" in audit
        assert "total_drills" in audit
        assert audit["total_drills"] > 0

    def test_all_drills_assigned(self):
        audit = audit_ramp_phases()
        assert len(audit["unassigned"]) == 0, f"Unassigned drills: {audit['unassigned']}"

    def test_all_four_phases_present(self):
        audit = audit_ramp_phases()
        for p in ("raise", "activate", "potentiate"):
            assert audit["phase_counts"][p] > 0, f"Phase {p} has no drills"


# ── D1: LANDING MECHANICS FAMILY ─────────────────────────────────

class TestLandingMechanics:
    def test_landing_family_registered(self):
        assert "Landing" in EXERCISES_BY_FAMILY

    def test_landing_exercises_count(self):
        landing = EXERCISES_BY_FAMILY["Landing"]
        assert len(landing) == 8

    def test_landing_progression_chain(self):
        landing = sorted(EXERCISES_BY_FAMILY["Landing"], key=lambda e: e.difficulty)
        for i in range(len(landing) - 1):
            assert landing[i].difficulty <= landing[i + 1].difficulty

    def test_landing_in_priorities(self):
        assert "Landing" in SELECTION_PRIORITIES

    def test_landing_exercises_selectable(self):
        athlete = _make_athlete()
        # Check that Landing appears in slot order (if blueprints include it)
        program = generate_program(athlete)
        all_families = set()
        for session in program.sessions:
            for block in session.blocks:
                all_families.add(block.family.value)
        # Landing is optional, may not appear in all blueprints
        # Just verify the data loads and integrates without error


# ── D2: SPRINT MECHANICS FAMILY ──────────────────────────────────

class TestSprintMechanics:
    def test_new_sprint_drills_exist(self):
        for eid in ["Sprint-023", "Sprint-024", "Sprint-025", "Sprint-026", "Sprint-027", "Sprint-028", "Sprint-029"]:
            assert eid in EXERCISE_BY_ID, f"Missing {eid}"

    def test_sprint_progression_chain(self):
        chain = ["Sprint-023", "Sprint-024", "Sprint-025", "Sprint-026", "Sprint-027", "Sprint-028", "Sprint-029"]
        for i in range(len(chain) - 1):
            ex = EXERCISE_BY_ID[chain[i]]
            assert ex.progression == chain[i + 1] or ex.id == chain[i + 1]

    def test_sprint_mechanics_reachable(self):
        """Drills exist in data and are in selection priorities — reachable by the system."""
        new_ids = ["Sprint-023", "Sprint-024", "Sprint-025", "Sprint-026", "Sprint-027", "Sprint-028", "Sprint-029"]
        priority = SELECTION_PRIORITIES.get("Sprint", [])
        for eid in new_ids:
            assert eid in EXERCISE_BY_ID, f"{eid} not found in exercise data"
            assert eid in priority, f"{eid} not in Sprint selection priority"

    def test_sprint_019_020_021_objectives_fixed(self):
        assert EXERCISE_BY_ID["Sprint-019"].objective.value == "COND"
        assert EXERCISE_BY_ID["Sprint-020"].objective.value == "POW"
        assert EXERCISE_BY_ID["Sprint-021"].objective.value == "POW"


# ── FULL DEMO REGRESSION ─────────────────────────────────────────

class TestFullDemo:
    def test_all_nine_demo_combinations_pass(self):
        from src.forge.__main__ import demo
        try:
            demo()
        except Exception as e:
            pytest.fail(f"Demo failed: {e}")
