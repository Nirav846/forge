import sys, os, re

path = os.path.join("D:", "forge", "tests", "test_wave9_session_assembly.py")
with open(path, "r") as f:
    text = f.read()

# Replace test_30_min_drops_tier_c_first
old1 = '''    def test_30_min_drops_tier_c_first(self):
        bp = _blueprint(
            [FamilyCode.DLKD],
            [FamilyCode.CARRY, FamilyCode.CORE, FamilyCode.ACC],
            [FamilyCode.DLKD, FamilyCode.CARRY, FamilyCode.CORE, FamilyCode.ACC],
        )
        slots = [FamilyCode.DLKD, FamilyCode.CARRY, FamilyCode.CORE, FamilyCode.ACC]
        kept, notes = apply_time_constraint_v2(slots, bp, 25, 6)
        assert FamilyCode.CARRY not in kept or FamilyCode.ACC not in kept
        assert FamilyCode.DLKD in kept
        assert FamilyCode.CORE in kept'''

new1 = '''    def test_30_min_drops_tier_c_first(self):
        bp = _blueprint(
            [FamilyCode.DLKD],
            [FamilyCode.CARRY, FamilyCode.CORE, FamilyCode.ACC, FamilyCode.HPUSH],
            [FamilyCode.DLKD, FamilyCode.CARRY, FamilyCode.CORE, FamilyCode.ACC, FamilyCode.HPUSH],
        )
        slots = [FamilyCode.DLKD, FamilyCode.CARRY, FamilyCode.CORE, FamilyCode.ACC, FamilyCode.HPUSH]
        kept, notes = apply_time_constraint_v2(slots, bp, 25, 6)
        assert FamilyCode.CARRY not in kept or FamilyCode.ACC not in kept
        assert FamilyCode.DLKD in kept
        assert FamilyCode.CORE in kept'''

if old1 in text:
    text = text.replace(old1, new1)
    print("Replaced test_30_min_drops_tier_c_first")
else:
    print("NOT FOUND: test_30_min_drops_tier_c_first")

# Replace test_45_min_drops_tier_b_before_tier_a
old2 = '''    def test_45_min_drops_tier_b_before_tier_a(self):
        bp = _blueprint(
            [FamilyCode.DLKD],
            [FamilyCode.DLHD, FamilyCode.SLKD, FamilyCode.CORE, FamilyCode.ROT],
            [FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.SLKD, FamilyCode.CORE, FamilyCode.ROT],
        )
        slots = [FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.SLKD, FamilyCode.CORE, FamilyCode.ROT]
        kept, notes = apply_time_constraint_v2(slots, bp, 40, 6)
        assert FamilyCode.SLKD not in kept or FamilyCode.ROT not in kept
        assert FamilyCode.DLKD in kept
        assert FamilyCode.DLHD in kept'''

new2 = '''    def test_45_min_drops_tier_b_before_tier_a(self):
        bp = _blueprint(
            [FamilyCode.DLKD],
            [FamilyCode.DLHD, FamilyCode.SLKD, FamilyCode.CORE, FamilyCode.ROT, FamilyCode.HPUSH],
            [FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.SLKD, FamilyCode.CORE, FamilyCode.ROT, FamilyCode.HPUSH],
        )
        slots = [FamilyCode.DLKD, FamilyCode.DLHD, FamilyCode.SLKD, FamilyCode.CORE, FamilyCode.ROT, FamilyCode.HPUSH]
        kept, notes = apply_time_constraint_v2(slots, bp, 40, 6)
        assert FamilyCode.SLKD not in kept or FamilyCode.ROT not in kept
        assert FamilyCode.DLKD in kept
        assert FamilyCode.DLHD in kept'''

if old2 in text:
    text = text.replace(old2, new2)
    print("Replaced test_45_min_drops_tier_b_before_tier_a")
else:
    print("NOT FOUND: test_45_min_drops_tier_b_before_tier_a")

# Replace test_drop_notes_mention_family_and_reason
old3 = '''    def test_drop_notes_mention_family_and_reason(self):
        bp = _blueprint(
            [FamilyCode.DLKD],
            [FamilyCode.CARRY, FamilyCode.CORE, FamilyCode.ACC],
            [FamilyCode.DLKD, FamilyCode.CARRY, FamilyCode.CORE, FamilyCode.ACC],
        )
        slots = [FamilyCode.DLKD, FamilyCode.CARRY, FamilyCode.CORE, FamilyCode.ACC]
        kept, notes = apply_time_constraint_v2(slots, bp, 25, 6)
        assert any("Carry" in n or "Acc" in n for n in notes)
        assert any("dropped" in n for n in notes)'''

new3 = '''    def test_drop_notes_mention_family_and_reason(self):
        bp = _blueprint(
            [FamilyCode.DLKD],
            [FamilyCode.CARRY, FamilyCode.CORE, FamilyCode.ACC, FamilyCode.HPUSH],
            [FamilyCode.DLKD, FamilyCode.CARRY, FamilyCode.CORE, FamilyCode.ACC, FamilyCode.HPUSH],
        )
        slots = [FamilyCode.DLKD, FamilyCode.CARRY, FamilyCode.CORE, FamilyCode.ACC, FamilyCode.HPUSH]
        kept, notes = apply_time_constraint_v2(slots, bp, 25, 6)
        assert any("Carry" in n or "Acc" in n for n in notes)
        assert any("dropped" in n for n in notes)'''

if old3 in text:
    text = text.replace(old3, new3)
    print("Replaced test_drop_notes_mention_family_and_reason")
else:
    print("NOT FOUND: test_drop_notes_mention_family_and_reason")

# Replace test_role_bias_influences_drop_order
old4 = '''    def test_role_bias_influences_drop_order(self):
        bp = _blueprint(
            [FamilyCode.DLKD],
            [FamilyCode.SPRINT, FamilyCode.CARRY, FamilyCode.CORE],
            [FamilyCode.DLKD, FamilyCode.SPRINT, FamilyCode.CARRY, FamilyCode.CORE],
        )
        slots = [FamilyCode.DLKD, FamilyCode.SPRINT, FamilyCode.CARRY, FamilyCode.CORE]
        rp = RoleWeekProfile(family_de_priority=["Sprint"])
        kept, notes = apply_time_constraint_v2(slots, bp, 25, 6, role_profile=rp)
        # Sprint should be dropped before Carry because it's de-prioritized
        if FamilyCode.SPRINT in kept and FamilyCode.CARRY in kept:
            # Both survived — only 4 slots, max is 4, nothing dropped
            pass
        else:
            assert FamilyCode.SPRINT not in kept or FamilyCode.CARRY in kept
        assert FamilyCode.DLKD in kept'''

new4 = '''    def test_role_bias_influences_drop_order(self):
        bp = _blueprint(
            [FamilyCode.DLKD],
            [FamilyCode.SPRINT, FamilyCode.CARRY, FamilyCode.CORE, FamilyCode.HPUSH],
            [FamilyCode.DLKD, FamilyCode.SPRINT, FamilyCode.CARRY, FamilyCode.CORE, FamilyCode.HPUSH],
        )
        slots = [FamilyCode.DLKD, FamilyCode.SPRINT, FamilyCode.CARRY, FamilyCode.CORE, FamilyCode.HPUSH]
        rp = RoleWeekProfile(family_de_priority=["Sprint"])
        kept, notes = apply_time_constraint_v2(slots, bp, 25, 6, role_profile=rp)
        if len(kept) < 5:
            assert FamilyCode.SPRINT not in kept
        assert FamilyCode.DLKD in kept'''

if old4 in text:
    text = text.replace(old4, new4)
    print("Replaced test_role_bias_influences_drop_order")
else:
    print("NOT FOUND: test_role_bias_influences_drop_order")

# Replace test_role_bias_overriding_with_single_family_passes
old5 = '''    def test_role_bias_overriding_with_single_family_passes(self):
        bp = _blueprint([FamilyCode.DLKD], [FamilyCode.SPRINT], [FamilyCode.DLKD, FamilyCode.SPRINT])
        blocks = [_block(FamilyCode.SPRINT)]
        rp = RoleWeekProfile(family_de_priority=["Sprint"])
        # Only 1 family present, no de-prio dominance check possible — passes
        assert check_role_bias_not_overriding_blueprint(blocks, bp, rp) is True'''

new5 = '''    def test_role_bias_overriding_with_single_family_fails(self):
        bp = _blueprint([FamilyCode.DLKD], [FamilyCode.SPRINT], [FamilyCode.DLKD, FamilyCode.SPRINT])
        blocks = [_block(FamilyCode.SPRINT)]
        rp = RoleWeekProfile(family_de_priority=["Sprint"])
        # Single de-prioritized family dominates 100% of session
        assert check_role_bias_not_overriding_blueprint(blocks, bp, rp) is False'''

if old5 in text:
    text = text.replace(old5, new5)
    print("Replaced test_role_bias_overriding_with_single_family_passes")
else:
    print("NOT FOUND: test_role_bias_overriding_with_single_family_passes")

with open(path, "w") as f:
    f.write(text)

print("Done")
