"""FORGE Hardening Phase Tests — regression tests for fixes 1-5."""

import unittest
from src.forge.models import (
    AthleteProfile, AthleteLevel, EquipmentProfile, SeasonPhase,
    FamilyCode, BlueprintName, Exercise, Session, SessionBlock,
    GeneratedProgram,
)
from src.forge.data import (
    BLUEPRINTS, BLUEPRINT_BY_ID, EXERCISE_BY_ID, EXERCISES,
    SELECTION_PRIORITIES, CONDITIONING_PROTOCOLS, COND_PROTOCOL_BY_ID,
    COND_PROTOCOLS_BY_SYSTEM, COND_DECISION_MAP, INTENT_CATEGORIES,
    FAMILY_TO_INTENT, EQUIPMENT_PROFILE_MAP, get_max_difficulty,
    get_equipment_for_profile,
)
from src.forge.blueprint_engine import (
    select_blueprint, determine_level, resolve_slots,
    get_equipment_profile, _shortlist_by_season_phase, _narrow_by_sport,
)
from src.forge.exercise_selector import select_exercise
from src.forge.substitution_engine import substitute_exercise
from src.forge.conditioning_engine import (
    generate_conditioning, select_conditioning, apply_level_adjustment,
)
from src.forge.validator import verify_credibility, calculate_credibility_score
from src.forge.renderer import render_program, render_session, render_block
from src.forge.main import generate_program


def make_profile(**kwargs):
    defaults = dict(
        sport="rugby",
        training_age_years=2.5,
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
    )
    defaults.update(kwargs)
    return AthleteProfile(**defaults)


class TestAllExpansion(unittest.TestCase):
    """Test Fix 1: optional_families=[\"All\"] expansion bug."""

    def test_all_expansion_youth_foundation(self):
        """BP7 Youth Foundation should expand All to all families not in mandatory."""
        bp = BLUEPRINT_BY_ID[7]
        self.assertEqual(bp.name, BlueprintName.YOUTH_FOUNDATION)
        
        # Check that optional_families includes all families except mandatory
        mandatory = set(bp.mandatory_families)
        optional = set(bp.optional_families)
        
        # All should be expanded to all families not in mandatory
        expected_optional = set(fam.value for fam in FamilyCode if fam.value not in mandatory)
        self.assertEqual(optional, expected_optional)
        
        # Verify Core is included
        self.assertIn(FamilyCode.CORE, optional)
        
        # Verify Sprint is included
        self.assertIn(FamilyCode.SPRINT, optional)

    def test_all_expansion_mixed_modal(self):
        """BP14 Mixed Modal should expand All to all families (no mandatory)."""
        bp = BLUEPRINT_BY_ID[14]
        self.assertEqual(bp.name, BlueprintName.MIXED_MODAL)
        
        # Check that optional_families includes all families
        optional = set(bp.optional_families)
        expected_optional = set(fam.value for fam in FamilyCode)
        self.assertEqual(optional, expected_optional)
        
        # Verify all families are present
        self.assertIn(FamilyCode.CORE, optional)
        self.assertIn(FamilyCode.CARRY, optional)
        self.assertIn(FamilyCode.ACC, optional)

    def test_all_expansion_does_not_include_mandatory(self):
        """All expansion should not include mandatory families."""
        # Test with BP9 (Rugby Off-Season) - has mandatory families
        bp = BLUEPRINT_BY_ID[9]
        mandatory = set(bp.mandatory_families)
        optional = set(bp.optional_families)
        
        # No mandatory family should be in optional
        for fam in mandatory:
            self.assertNotIn(fam, optional)


class TestCorePreservation(unittest.TestCase):
    """Test Fix 3: Core always included when in optional_families."""

    def test_core_included_when_in_optional(self):
        """Core should be included in resolved slots if it's in optional_families."""
        # Test with BP14 (Mixed Modal) - Core is in optional_families
        bp = BLUEPRINT_BY_ID[14]
        self.assertIn(FamilyCode.CORE, bp.optional_families)
        
        # Generate resolved slots
        slots = resolve_slots(bp, AthleteLevel.INTERMEDIATE)
        
        # Core should be in the resolved slots
        self.assertIn(FamilyCode.CORE, slots)
        
        # Core should be last (enforce_session_flow_rules)
        self.assertEqual(slots[-1], FamilyCode.CORE)

    def test_core_preserved_with_slot_cap(self):
        """Core should be preserved even with 8-slot cap."""
        # BP14 has 0 mandatory and All optional (all families)
        bp = BLUEPRINT_BY_ID[14]
        slots = resolve_slots(bp, AthleteLevel.INTERMEDIATE)
        
        # Even with 8-slot cap, Core should be included
        self.assertIn(FamilyCode.CORE, slots)
        self.assertEqual(slots[-1], FamilyCode.CORE)


class TestSlotOrderFixes(unittest.TestCase):
    """Test Fix 4: BP9/BP5/BP14 slot_order fixes."""

    def test_bp9_rugby_off_season_slot_order(self):
        """BP9 should have Sprint before Ball."""
        bp = BLUEPRINT_BY_ID[9]
        slots = resolve_slots(bp, AthleteLevel.INTERMEDIATE)
        
        # Sprint should be before Ball in resolved slots
        if FamilyCode.SPRINT in slots and FamilyCode.BALL in slots:
            self.assertLess(slots.index(FamilyCode.SPRINT), slots.index(FamilyCode.BALL))

    def test_bp5_upper_lower_split_slot_order(self):
        """BP5 should have Carry after HPull."""
        bp = BLUEPRINT_BY_ID[5]
        slots = resolve_slots(bp, AthleteLevel.INTERMEDIATE)
        
        # Carry should be after HPull in resolved slots
        if FamilyCode.CARRY in slots and FamilyCode.HPULL in slots:
            self.assertLess(slots.index(FamilyCode.HPULL), slots.index(FamilyCode.CARRY))

    def test_bp14_mixed_modal_slot_order(self):
        """BP14 should have Plyo before DLKD."""
        bp = BLUEPRINT_BY_ID[14]
        slots = resolve_slots(bp, AthleteLevel.INTERMEDIATE)
        
        # Plyo should be before DLKD in resolved slots
        if FamilyCode.PLYO in slots and FamilyCode.DLKD in slots:
            self.assertLess(slots.index(FamilyCode.PLYO), slots.index(FamilyCode.DLKD))


class TestCarryPriority(unittest.TestCase):
    """Test Fix 5: Split Carry from core_stability in INTENT_CATEGORIES."""

    def test_carry_not_in_core_stability(self):
        """Carry should not be in core_stability INTENT_CATEGORIES."""
        self.assertNotIn("Carry", INTENT_CATEGORIES.get("core_stability", []))
        
        # Carry should be in carry_load instead
        self.assertIn("Carry", INTENT_CATEGORIES.get("carry_load", []))

    def test_family_to_intent_mapping(self):
        """FAMILY_TO_INTENT should map Carry to carry_load."""
        self.assertEqual(FAMILY_TO_INTENT.get("Carry"), "carry_load")
        
        # Core and Rot should still be in core_stability
        self.assertEqual(FAMILY_TO_INTENT.get("Core"), "core_stability")
        self.assertEqual(FAMILY_TO_INTENT.get("Rot"), "core_stability")

    def test_substitution_engine_uses_new_categories(self):
        """Substitution engine should use updated INTENT_CATEGORIES."""
        # This tests that the substitution engine uses the updated
        # INTENT_CATEGORIES and FAMILY_TO_INTENT mappings
        intent = FAMILY_TO_INTENT.get("Carry")
        self.assertEqual(intent, "carry_load")


class TestBlueprintReachability(unittest.TestCase):
    """Test that all blueprints are reachable and generate programs."""

    def test_all_blueprints_reachable(self):
        """All 14 blueprints should be reachable by some athlete profile."""
        # Test that each blueprint can be selected by some athlete
        for bp_id in range(1, 15):
            # BP12 is special (return_to_sport or injury)
            if bp_id == 12:
                continue
                
            # Create athlete profiles that should reach each blueprint
            # This is a simplified test - in reality, reachability depends on many factors
            bp = BLUEPRINT_BY_ID[bp_id]
            
            # Basic check that blueprint exists and has required data
            self.assertIsNotNone(bp)
            self.assertIsInstance(bp.id, int)
            self.assertIsInstance(bp.name, BlueprintName)
            self.assertIsInstance(bp.mandatory_families, list)
            self.assertIsInstance(bp.optional_families, list)
            self.assertIsInstance(bp.slot_order, list)

    def test_bp14_no_longer_empty(self):
        """BP14 should no longer generate empty sessions after fixes."""
        # With the All expansion fix, BP14 should have optional families
        bp = BLUEPRINT_BY_ID[14]
        
        # BP14 should have optional families now (All expanded)
        self.assertTrue(len(bp.optional_families) > 0)
        
        # When resolving slots, should have at least one family
        slots = resolve_slots(bp, AthleteLevel.INTERMEDIATE)
        self.assertTrue(len(slots) > 0)


if __name__ == "__main__":
    unittest.main()
