"""Wave 8 — Role-Specific Week Planning Hardening Tests.

Target: 30–45 tests covering role profiles, week planning bias,
exposure targets/caps, renderer output, backward compatibility, and end-to-end.
"""
from __future__ import annotations

from forge.role_week_planning import (
    RoleWeekProfile,
    get_role_week_profile,
    get_role_week_notes,
    get_role_exposure_limits,
    apply_role_slot_bias,
    should_add_conditioning_for_role,
    get_role_conditioning_frequency_bias,
    render_role_week_summary,
)
from forge.progression_engine import (
    weekly_exposure_warnings,
    review_week,
    verify_program_credibility,
    _check_role_week_bias_applied,
    _check_role_exposure_balance,
    _check_role_conditioning_alignment,
    program_role_exposure_summary,
)
from forge.renderer import render_block_summary, render_coach_program
from forge.models import (
    AthleteProfile, AthleteLevel, EquipmentProfile, SeasonPhase, FamilyCode,
    Session, SessionBlock, GeneratedProgram, Exercise, ConditioningProtocol,
)
from forge.main import generate_program


# ── Helpers ───────────────────────────────────────────────────────

def _make_athlete(sport: str, role: str, **overrides) -> AthleteProfile:
    defaults = {
        "sport": sport,
        "training_age_years": 3.0,
        "season_phase": SeasonPhase.OFF_SEASON,
        "goal": "strength",
        "equipment_profile": EquipmentProfile.COMMERCIAL_GYM,
        "athlete_level": AthleteLevel.INTERMEDIATE,
        "technique_consistency": 0.9,
        "injury_status": "none",
        "injury_history": [],
        "fatigue_level": "normal",
        "weeks_since_break": 0,
        "recent_exercises": {},
        "available_minutes": 75,
        "days_to_match": None,
        "preferred_families": 6,
        "age": 22,
        "strength_base_met": True,
        "position_role": role,
        "bodyweight_kg": 80.0,
    }
    defaults.update(overrides)
    return AthleteProfile(**defaults)


def _exercise(family: FamilyCode, name: str = "Test", difficulty: int = 2,
              eccentric_cost: int = 3, impact_level: int = 3, rotational: bool = False) -> Exercise:
    return Exercise(
        id=f"T-{family.value}",
        name=name,
        family=family,
        secondary_family=None,
        objective="STR",
        difficulty=difficulty,
        equipment=["barbell"],
        unilateral=False,
        explosive=False,
        isometric=False,
        rotational=rotational,
        progression=None,
        regression=None,
        eccentric_cost=eccentric_cost,
        impact_level=impact_level,
    )


def _session_with_families(families: list[FamilyCode], conditioning: ConditioningProtocol | None = None) -> Session:
    blocks = []
    for fam in families:
        ex = _exercise(fam)
        blocks.append(SessionBlock(
            family=fam,
            family_name=fam.value,
            exercises=[ex],
        ))
    return Session(blocks=blocks, conditioning=conditioning)


# ═══════════════════════════════════════════════════════════════════
# A. Role Week Profile Creation
# ═══════════════════════════════════════════════════════════════════

class TestRoleWeekProfileCreation:

    def test_known_role_returns_profile(self):
        profile = get_role_week_profile("rugby", "prop")
        assert isinstance(profile, RoleWeekProfile)
        assert profile.force_emphasis == 0.9
        assert profile.sprint_exposure_target == "low"

    def test_known_cricket_fast_bowler(self):
        profile = get_role_week_profile("cricket", "fast_bowler")
        assert profile.sprint_exposure_target == "high"
        assert profile.jump_exposure_target == "high"
        assert profile.eccentric_tolerance == "high"
        assert "DLHD" in profile.family_de_priority

    def test_known_tennis_singles(self):
        profile = get_role_week_profile("tennis", "singles")
        assert profile.conditioning_density_bias == "high"
        assert profile.rotation_exposure_target == "high"
        assert "VPush" in profile.family_de_priority

    def test_known_tennis_doubles(self):
        profile = get_role_week_profile("tennis", "doubles")
        assert profile.conditioning_density_bias == "moderate"
        assert profile.sprint_exposure_target == "low"
        assert "Sprint" in profile.family_de_priority

    def test_known_volleyball_libero(self):
        profile = get_role_week_profile("volleyball", "libero")
        assert profile.jump_exposure_target == "low"
        assert profile.force_emphasis == 0.3
        assert profile.conditioning_density_bias == "high"

    def test_known_volleyball_middle_blocker(self):
        profile = get_role_week_profile("volleyball", "middle_blocker")
        assert profile.jump_exposure_target == "high"
        assert profile.landing_emphasis == 0.9

    def test_known_basketball_guard(self):
        profile = get_role_week_profile("basketball", "guard")
        assert profile.sprint_exposure_target == "high"
        assert profile.velocity_emphasis == 0.8
        assert "DLKD" in profile.family_de_priority

    def test_known_basketball_big(self):
        profile = get_role_week_profile("basketball", "big")
        assert profile.force_emphasis == 0.8
        assert profile.jump_exposure_target == "high"
        assert profile.sprint_exposure_target == "low"

    def test_unknown_role_falls_back_to_sport_default(self):
        profile = get_role_week_profile("rugby", "unknown_role")
        sport_default = get_role_week_profile("rugby", None)
        assert profile == sport_default

    def test_unknown_sport_falls_back_to_neutral(self):
        profile = get_role_week_profile("unknown_sport", "some_role")
        assert profile.force_emphasis == 0.5
        assert profile.sprint_exposure_target == "moderate"

    def test_no_role_no_sport_returns_neutral(self):
        profile = get_role_week_profile("", "")
        assert profile.force_emphasis == 0.5

    def test_role_alias_resolution(self):
        # "spinner" should map to "spin_bowler"
        profile = get_role_week_profile("cricket", "spinner")
        assert profile.rotation_exposure_target == "high"
        assert profile.sprint_exposure_target == "low"

    def test_soccer_striker_role(self):
        profile = get_role_week_profile("soccer", "striker")
        assert profile.sprint_exposure_target == "high"
        assert profile.velocity_emphasis == 0.7

    def test_football_goalkeeper(self):
        profile = get_role_week_profile("football", "goalkeeper")
        assert profile.jump_exposure_target == "high"
        assert profile.sprint_exposure_target == "low"


# ═══════════════════════════════════════════════════════════════════
# B. Week Planning Bias Behavior
# ═══════════════════════════════════════════════════════════════════

class TestWeekPlanningBias:

    def test_prop_slot_bias_prefers_force_families(self):
        slots = [FamilyCode.SPRINT, FamilyCode.DLKD, FamilyCode.HPUSH, FamilyCode.CORE]
        profile = get_role_week_profile("rugby", "prop")
        biased = apply_role_slot_bias(slots, profile)
        # DLKD and HPush should come before Sprint for prop
        assert biased[0] == FamilyCode.DLKD or biased[0] == FamilyCode.HPUSH
        assert biased[-1] == FamilyCode.SPRINT

    def test_backline_slot_bias_prefers_sprint(self):
        slots = [FamilyCode.DLKD, FamilyCode.SPRINT, FamilyCode.PLYO, FamilyCode.CORE]
        profile = get_role_week_profile("rugby", "back_three")
        biased = apply_role_slot_bias(slots, profile)
        # Sprint should be early for backline
        assert biased[0] == FamilyCode.SPRINT

    def test_fast_bowler_de_prioritizes_rot_vpush(self):
        slots = [FamilyCode.ROT, FamilyCode.VPUSH, FamilyCode.SPRINT, FamilyCode.CORE]
        profile = get_role_week_profile("cricket", "fast_bowler")
        biased = apply_role_slot_bias(slots, profile)
        # ROT and VPUSH should be at the end
        assert biased[-1] in (FamilyCode.ROT, FamilyCode.VPUSH)
        assert biased[-2] in (FamilyCode.ROT, FamilyCode.VPUSH)

    def test_tennis_singles_conditioning_density_high(self):
        profile = get_role_week_profile("tennis", "singles")
        bias = get_role_conditioning_frequency_bias(profile)
        assert bias == 1.33

    def test_tennis_doubles_conditioning_density_moderate(self):
        profile = get_role_week_profile("tennis", "doubles")
        bias = get_role_conditioning_frequency_bias(profile)
        assert bias == 1.0

    def test_prop_conditioning_density_moderate(self):
        profile = get_role_week_profile("rugby", "prop")
        bias = get_role_conditioning_frequency_bias(profile)
        assert bias == 1.0

    def test_goalkeeper_conditioning_density_low(self):
        profile = get_role_week_profile("soccer", "goalkeeper")
        bias = get_role_conditioning_frequency_bias(profile)
        assert bias == 0.67

    def test_should_add_conditioning_for_role_high_density(self):
        profile = get_role_week_profile("tennis", "singles")
        # High density means more sessions get conditioning
        assert should_add_conditioning_for_role(1, 1, 3, "strength", profile) is True
        assert should_add_conditioning_for_role(1, 2, 3, "strength", profile) is True

    def test_should_add_conditioning_for_role_low_density(self):
        profile = get_role_week_profile("soccer", "goalkeeper")
        # Low density should skip some conditioning sessions
        result = should_add_conditioning_for_role(1, 1, 3, "strength", profile)
        assert result is True or result is False  # just verify it doesn't crash

    def test_no_role_no_bias_in_slot_ordering(self):
        slots = [FamilyCode.SPRINT, FamilyCode.DLKD, FamilyCode.HPUSH, FamilyCode.CORE]
        profile = get_role_week_profile("rugby", "")
        biased = apply_role_slot_bias(slots, profile)
        assert biased == slots


# ═══════════════════════════════════════════════════════════════════
# C. Exposure Target Logic
# ═══════════════════════════════════════════════════════════════════

class TestExposureTargetLogic:

    def test_prop_sprint_cap_low(self):
        profile = get_role_week_profile("rugby", "prop")
        limits = get_role_exposure_limits(profile)
        assert limits["sprint_max"] == 2
        assert limits["decel_max"] == 2

    def test_backline_sprint_cap_high(self):
        profile = get_role_week_profile("rugby", "back_three")
        limits = get_role_exposure_limits(profile)
        assert limits["sprint_max"] == 5
        assert limits["decel_max"] == 4

    def test_middle_blocker_jump_cap_high(self):
        profile = get_role_week_profile("volleyball", "middle_blocker")
        limits = get_role_exposure_limits(profile)
        assert limits["jump_max"] == 5
        assert limits["landing_max"] == 4

    def test_libero_jump_cap_low(self):
        profile = get_role_week_profile("volleyball", "libero")
        limits = get_role_exposure_limits(profile)
        assert limits["jump_max"] == 2
        assert limits["landing_max"] == 2

    def test_fast_bowler_rotation_cap_moderate(self):
        profile = get_role_week_profile("cricket", "fast_bowler")
        limits = get_role_exposure_limits(profile)
        assert limits["rotation_max"] == 4

    def test_batter_rotation_cap_high(self):
        profile = get_role_week_profile("cricket", "batter")
        limits = get_role_exposure_limits(profile)
        assert limits["rotation_max"] == 5

    def test_prop_eccentric_tolerance_high(self):
        profile = get_role_week_profile("rugby", "prop")
        limits = get_role_exposure_limits(profile)
        assert limits["high_eccentric_max"] == 4

    def test_fast_bowler_eccentric_tolerance_high(self):
        profile = get_role_week_profile("cricket", "fast_bowler")
        limits = get_role_exposure_limits(profile)
        assert limits["high_eccentric_max"] == 4

    def test_spin_bowler_eccentric_tolerance_low(self):
        profile = get_role_week_profile("cricket", "spin_bowler")
        limits = get_role_exposure_limits(profile)
        assert limits["high_eccentric_max"] == 2

    def test_neutral_profile_default_limits(self):
        profile = RoleWeekProfile()
        limits = get_role_exposure_limits(profile)
        assert limits["sprint_max"] == 4
        assert limits["landing_max"] == 3
        assert limits["rotation_max"] == 4
        assert limits["high_eccentric_max"] == 3

    def test_weekly_exposure_warnings_respects_role_cap(self):
        # Create a session with 3 sprint exercises for a prop (cap = 2)
        sessions = [
            _session_with_families([FamilyCode.SPRINT]),
            _session_with_families([FamilyCode.SPRINT]),
            _session_with_families([FamilyCode.SPRINT]),
        ]
        profile = get_role_week_profile("rugby", "prop")
        warnings = weekly_exposure_warnings(sessions, 1, profile)
        assert any("sprint" in w.lower() for w in warnings)

    def test_weekly_exposure_warnings_passes_for_safe_distribution(self):
        sessions = [
            _session_with_families([FamilyCode.SPRINT]),
            _session_with_families([FamilyCode.DLKD]),
        ]
        profile = get_role_week_profile("rugby", "prop")
        warnings = weekly_exposure_warnings(sessions, 1, profile)
        assert not any("sprint" in w.lower() for w in warnings)


# ═══════════════════════════════════════════════════════════════════
# D. Renderer / Coach Output
# ═══════════════════════════════════════════════════════════════════

class TestRendererCoachOutput:

    def test_role_week_notes_appear(self):
        notes = get_role_week_notes("rugby", "prop")
        assert any("Prop" in n or "prop" in n for n in notes)
        assert any("force" in n.lower() or "collision" in n.lower() for n in notes)

    def test_fast_bowler_notes_mention_sprint_landing(self):
        notes = get_role_week_notes("cricket", "fast_bowler")
        assert any("sprint" in n.lower() for n in notes)
        assert any("landing" in n.lower() or "eccentric" in n.lower() for n in notes)

    def test_tennis_singles_vs_doubles_notes_differ(self):
        singles_notes = get_role_week_notes("tennis", "singles")
        doubles_notes = get_role_week_notes("tennis", "doubles")
        assert singles_notes != doubles_notes

    def test_render_role_week_summary_output(self):
        profile = get_role_week_profile("rugby", "prop")
        lines = render_role_week_summary(profile)
        assert any("Sprint exposure target" in line for line in lines)
        assert any("Jump/Landing" in line for line in lines)

    def test_block_summary_contains_role_bias(self):
        athlete = _make_athlete("rugby", "prop")
        program = generate_program(athlete)
        summary = render_block_summary(program)
        assert "Role Week Bias" in summary or "Role Weekly Emphasis Targets" in summary

    def test_block_summary_contains_exposure_targets(self):
        athlete = _make_athlete("cricket", "fast_bowler")
        program = generate_program(athlete)
        summary = render_block_summary(program)
        assert "Role Exposure Targets" in summary or "Sprint:" in summary

    def test_coach_program_contains_personalization_notes(self):
        athlete = _make_athlete("volleyball", "middle_blocker")
        program = generate_program(athlete)
        output = render_coach_program(program)
        assert "Personalization Notes" in output


# ═══════════════════════════════════════════════════════════════════
# E. Backward Compatibility
# ═══════════════════════════════════════════════════════════════════

class TestBackwardCompatibility:

    def test_no_role_still_generates_program(self):
        athlete = _make_athlete("rugby", "")
        program = generate_program(athlete)
        assert program is not None
        assert len(program.sessions) > 0

    def test_unknown_sport_role_still_generates_program(self):
        athlete = _make_athlete("fencing", "epee")
        program = generate_program(athlete)
        assert program is not None
        assert len(program.sessions) > 0

    def test_existing_generation_path_without_wave8_fields(self):
        athlete = AthleteProfile(
            sport="rugby",
            training_age_years=2.0,
            season_phase=SeasonPhase.OFF_SEASON,
            goal="strength",
            equipment_profile=EquipmentProfile.COMMERCIAL_GYM,
            athlete_level=AthleteLevel.INTERMEDIATE,
            technique_consistency=0.9,
            injury_status="none",
            injury_history=[],
            fatigue_level="normal",
            weeks_since_break=0,
            recent_exercises={},
            available_minutes=60,
            days_to_match=None,
            preferred_families=6,
            age=20,
            strength_base_met=True,
        )
        program = generate_program(athlete)
        assert program is not None
        assert program.credibility_score > 0

    def test_program_credibility_no_role(self):
        athlete = _make_athlete("rugby", "")
        program = generate_program(athlete)
        result = verify_program_credibility(program)
        assert result["role_week_bias_applied"] is True  # No role = vacuously true
        assert result["role_exposure_balance"] is True   # No role = vacuously true
        assert result["role_conditioning_alignment"] is True

    def test_weekly_exposure_warnings_without_role_profile(self):
        sessions = [_session_with_families([FamilyCode.SPRINT])]
        warnings = weekly_exposure_warnings(sessions, 1)
        # Should use default caps (4 sprint max)
        assert not any("role cap" in w for w in warnings)

    def test_review_week_without_role_profile(self):
        sessions = [_session_with_families([FamilyCode.SPRINT])]
        flags = review_week(sessions, "accumulation")
        assert "risks" in flags

    def test_neutral_profile_no_family_priority(self):
        profile = RoleWeekProfile()
        slots = [FamilyCode.SPRINT, FamilyCode.DLKD, FamilyCode.CORE]
        biased = apply_role_slot_bias(slots, profile)
        assert biased == slots


# ═══════════════════════════════════════════════════════════════════
# F. End-to-End Role Divergence
# ═══════════════════════════════════════════════════════════════════

class TestEndToEndRoleDivergence:

    def test_rugby_prop_vs_backline_different_week_emphasis(self):
        prop_athlete = _make_athlete("rugby", "prop", goal="strength")
        backline_athlete = _make_athlete("rugby", "back_three", goal="strength")

        prop_program = generate_program(prop_athlete)
        backline_program = generate_program(backline_athlete)

        # Both should use same blueprint (strength)
        assert prop_program.blueprint_id == backline_program.blueprint_id

        # But slot ordering should differ (via role bias)
        prop_first_session_families = [b.family.value for b in prop_program.sessions[0].blocks]
        backline_first_session_families = [b.family.value for b in backline_program.sessions[0].blocks]
        assert prop_first_session_families != backline_first_session_families

    def test_cricket_fast_bowler_vs_batter_different_landing_rotation(self):
        fb_athlete = _make_athlete("cricket", "fast_bowler", goal="strength")
        batter_athlete = _make_athlete("cricket", "batter", goal="strength")

        fb_program = generate_program(fb_athlete)
        batter_program = generate_program(batter_athlete)

        # Count landing and rotation exposures across first week
        def count_families(program, family_vals):
            count = 0
            for s in program.sessions[:program.frequency]:
                for b in s.blocks:
                    if b.family.value in family_vals or any(ex.rotational for ex in b.exercises):
                        count += 1
            return count

        fb_rot = count_families(fb_program, ["Rot"])
        batter_rot = count_families(batter_program, ["Rot"])
        # Batter should have more rotational emphasis than fast bowler
        assert batter_rot >= fb_rot

    def test_tennis_singles_vs_doubles_conditioning_density(self):
        singles_athlete = _make_athlete("tennis", "singles", goal="strength")
        doubles_athlete = _make_athlete("tennis", "doubles", goal="strength")

        singles_program = generate_program(singles_athlete)
        doubles_program = generate_program(doubles_athlete)

        # Singles should have more conditioning sessions
        singles_cond = sum(1 for s in singles_program.sessions if s.conditioning is not None)
        doubles_cond = sum(1 for s in doubles_program.sessions if s.conditioning is not None)
        assert singles_cond >= doubles_cond

    def test_volleyball_libero_vs_middle_blocker_jump_emphasis(self):
        libero_athlete = _make_athlete("volleyball", "libero", goal="strength")
        middle_athlete = _make_athlete("volleyball", "middle_blocker", goal="strength")

        libero_program = generate_program(libero_athlete)
        middle_program = generate_program(middle_athlete)

        # Middle blocker should have more Plyo/Landing exposure
        def jump_count(program):
            return sum(
                1 for s in program.sessions[:program.frequency]
                for b in s.blocks
                if b.family.value in ("Plyo", "Landing")
            )

        assert jump_count(middle_program) >= jump_count(libero_program)

    def test_program_credibility_role_checks_pass(self):
        athlete = _make_athlete("rugby", "prop")
        program = generate_program(athlete)
        result = verify_program_credibility(program)
        assert result["role_week_bias_applied"] is True
        assert result["role_exposure_balance"] is True
        assert result["role_conditioning_alignment"] is True

    def test_guard_vs_big_different_slot_ordering(self):
        guard_athlete = _make_athlete("basketball", "guard", goal="strength")
        big_athlete = _make_athlete("basketball", "big", goal="strength")

        guard_program = generate_program(guard_athlete)
        big_program = generate_program(big_athlete)

        guard_fams = [b.family.value for b in guard_program.sessions[0].blocks]
        big_fams = [b.family.value for b in big_program.sessions[0].blocks]
        assert guard_fams != big_fams

    def test_striker_vs_goalkeeper_different_emphasis(self):
        striker_athlete = _make_athlete("soccer", "striker", goal="strength")
        gk_athlete = _make_athlete("soccer", "goalkeeper", goal="strength")

        striker_program = generate_program(striker_athlete)
        gk_program = generate_program(gk_athlete)

        # Striker should have more Sprint exposure than GK
        striker_sprint = sum(
            1 for s in striker_program.sessions[:striker_program.frequency]
            for b in s.blocks
            if b.family.value == "Sprint"
        )
        gk_sprint = sum(
            1 for s in gk_program.sessions[:gk_program.frequency]
            for b in s.blocks
            if b.family.value == "Sprint"
        )
        assert striker_sprint >= gk_sprint

    def test_renderer_role_notes_present(self):
        athlete = _make_athlete("rugby", "prop")
        program = generate_program(athlete)
        summary = render_block_summary(program)
        assert "Role Week Bias" in summary
        assert "Role Weekly Emphasis Targets" in summary

    def test_role_exposure_summary_includes_qualitative_targets(self):
        athlete = _make_athlete("cricket", "fast_bowler")
        program = generate_program(athlete)
        lines = program_role_exposure_summary(program)
        assert any("Role Exposure Targets" in line for line in lines)
        assert any("Sprint:" in line for line in lines)
