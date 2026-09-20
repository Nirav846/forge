import pytest
from src.forge.models import AthleteProfile, BlockResponse, AthleteLevel, SeasonPhase, EquipmentProfile
from src.forge.block_autoregulation import classify_band_change, build_block_response, recommend_next_block_shift, get_next_block_blueprint_bias
from src.forge.blueprint_engine import select_blueprint
from src.forge.prescription_rules import get_athlete_prescription_modifiers, PrescriptionRole
from src.forge.main import generate_program
from src.forge.data import BLUEPRINT_BY_ID, BLUEPRINTS

def test_classify_band_change_improved():
    assert classify_band_change('low', 'moderate') == 'improved'
    assert classify_band_change('moderate', 'high') == 'improved'
    assert classify_band_change('high', 'elite') == 'improved'

def test_classify_band_change_regressed():
    assert classify_band_change('elite', 'high') == 'regressed'
    assert classify_band_change('high', 'moderate') == 'regressed'
    assert classify_band_change('moderate', 'low') == 'regressed'

def test_classify_band_change_same():
    assert classify_band_change('low', 'low') == 'same'
    assert classify_band_change('moderate', 'moderate') == 'same'
    assert classify_band_change('high', 'high') == 'same'
    assert classify_band_change('elite', 'elite') == 'same'

def test_classify_band_change_unknown():
    assert classify_band_change(None, 'low') == 'unknown'
    assert classify_band_change('low', None) == 'unknown'
    assert classify_band_change('invalid', 'low') == 'unknown'
    assert classify_band_change('low', 'invalid') == 'unknown'

def test_build_block_response_with_prior_no_change():
    prior = AthleteProfile(
        sport='Rowing',
        training_age_years=4,
        season_phase='off_season',
        goal='Endurance',
        equipment_profile='Commercial Gym',
        athlete_level='Intermediate',
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='high',
        squat_strength_band='moderate',
        aerobic_band='low'
    )
    current = prior
    response = build_block_response(prior, current, None)
    assert response.improvements == []
    assert response.stalls == ['cmj', 'sprint_10m', 'squat_strength', 'aerobic']
    assert response.regressions == []
    assert response.recommended_shift == 'Maintain current focus.'
    # Check notes format
    assert any('cmj stalled' in note.lower() for note in response.notes)
    assert any('sprint_10m stalled' in note.lower() for note in response.notes)
    assert any('squat_strength stalled' in note.lower() for note in response.notes)
    assert any('aerobic stalled' in note.lower() for note in response.notes)

def test_build_block_response_strength_up_cmj_same():
    prior = AthleteProfile(
        sport='Rugby',
        training_age_years=5,
        season_phase='off_season',
        goal='Strength',
        equipment_profile='Commercial Gym',
        athlete_level='Advanced',
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='moderate',
        squat_strength_band='low',
        aerobic_band='moderate'
    )
    current = AthleteProfile(
        sport='Rugby',
        training_age_years=5,
        season_phase='off_season',
        goal='Strength',
        equipment_profile='Commercial Gym',
        athlete_level='Advanced',
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='moderate',
        squat_strength_band='moderate',
        aerobic_band='moderate'
    )
    # We need to provide prior_blueprint_id and prior_goal for BlockResponse, but build_block_response will compute them from prior_program if given, or from prior_profile.
    # Since we are not passing prior_program, it will use prior_profile to get goal, but prior_blueprint_id will be empty string.
    response = build_block_response(prior, current, None)
    assert 'squat_strength' in response.improvements
    assert 'cmj' in response.stalls
    assert 'sprint_10m' in response.stalls
    assert 'aerobic' in response.stalls
    assert any('squat_strength improved' in note for note in response.notes)
    assert any('cmj stalled' in note for note in response.notes)

def test_build_block_response_multiple_improvements():
    prior = AthleteProfile(
        sport='Basketball',
        training_age_years=3,
        season_phase='pre_season',
        goal='Explosiveness',
        equipment_profile='Commercial Gym',
        athlete_level='Intermediate',
        technique_consistency=0.85,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='low',
        sprint_10m_band='low',
        squat_strength_band='low',
        aerobic_band='low'
    )
    current = AthleteProfile(
        sport='Basketball',
        training_age_years=3,
        season_phase='pre_season',
        goal='Explosiveness',
        equipment_profile='Commercial Gym',
        athlete_level='Intermediate',
        technique_consistency=0.85,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='high',
        sprint_10m_band='moderate',
        squat_strength_band='moderate',
        aerobic_band='moderate'
    )
    response = build_block_response(prior, current, None)
    assert set(response.improvements) == {'cmj', 'sprint_10m', 'squat_strength', 'aerobic'}
    assert response.stalls == []
    assert response.regressions == []
    assert any('cmj improved' in note for note in response.notes)
    assert any('sprint_10m improved' in note for note in response.notes)
    assert any('squat_strength improved' in note for note in response.notes)
    assert any('aerobic improved' in note for note in response.notes)

def test_build_block_response_with_regressions():
    prior = AthleteProfile(
        sport='Soccer',
        training_age_years=4,
        season_phase='off_season',
        goal='Endurance',
        equipment_profile='Commercial Gym',
        athlete_level='Advanced',
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='elite',
        sprint_10m_band='elite',
        squat_strength_band='elite',
        aerobic_band='elite'
    )
    current = AthleteProfile(
        sport='Soccer',
        training_age_years=4,
        season_phase='off_season',
        goal='Endurance',
        equipment_profile='Commercial Gym',
        athlete_level='Advanced',
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='moderate',
        squat_strength_band='moderate',
        aerobic_band='moderate'
    )
    response = build_block_response(prior, current, None)
    assert set(response.regressions) == {'cmj', 'sprint_10m', 'squat_strength', 'aerobic'}
    assert response.improvements == []
    assert response.stalls == []
    assert any('cmj regressed' in note for note in response.notes)
    assert any('sprint_10m regressed' in note for note in response.notes)
    assert any('squat_strength regressed' in note for note in response.notes)
    assert any('aerobic regressed' in note for note in response.notes)

def test_recommend_next_block_shift_power_conversion():
    prior = AthleteProfile(
        sport='Rugby',
        training_age_years=5,
        season_phase='off_season',
        goal='Strength',
        equipment_profile='Commercial Gym',
        athlete_level='Advanced',
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='moderate',
        squat_strength_band='low',
        aerobic_band='moderate'
    )
    current = AthleteProfile(
        sport='Rugby',
        training_age_years=5,
        season_phase='off_season',
        goal='Strength',
        equipment_profile='Commercial Gym',
        athlete_level='Advanced',
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='moderate',
        squat_strength_band='moderate',
        aerobic_band='moderate'
    )
    # Build a minimal response to pass to recommend_next_block_shift
    response = BlockResponse(
        prior_blueprint_id='',
        prior_goal='Strength',
        start_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_band': 'low', 'aerobic_band': 'moderate'},
        end_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_band': 'moderate', 'aerobic_band': 'moderate'},
        improvements=['squat_strength'],
        stalls=['cmj'],
        regressions=[],
        recommended_shift='',
        notes=[]
    )
    shift = recommend_next_block_shift(response, current)
    assert shift['power_bias'] == 1
    assert shift['strength_bias'] == -1
    assert shift['conditioning_bias'] == 0
    assert any('power conversion' in note for note in shift['notes'])

def test_recommend_next_block_shift_aerobic_up_sprint_same():
    prior = AthleteProfile(
        sport='Tennis',
        training_age_years=4,
        season_phase='off_season',
        goal='Endurance',
        equipment_profile='Commercial Gym',
        athlete_level='Intermediate',
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='low',
        squat_strength_band='moderate',
        aerobic_band='low'
    )
    current = AthleteProfile(
        sport='Tennis',
        training_age_years=4,
        season_phase='off_season',
        goal='Endurance',
        equipment_profile='Commercial Gym',
        athlete_level='Intermediate',
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='low',
        squat_strength_band='moderate',
        aerobic_band='moderate'
    )
    response = BlockResponse(
        prior_blueprint_id='',
        prior_goal='Endurance',
        start_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'low', 'squat_strength_band': 'moderate', 'aerobic_band': 'low'},
        end_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'low', 'squat_strength_band': 'moderate', 'aerobic_band': 'moderate'},
        improvements=['aerobic'],
        stalls=['sprint_10m'],
        regressions=[],
        recommended_shift='',
        notes=[]
    )
    # Use get_next_block_blueprint_bias for tennis-specific checks
    bias = get_next_block_blueprint_bias(current, response)
    assert bias['prefer_power_speed'] == True
    assert bias['keep_sprint_emphasis'] == True
    assert any('speed / court-power emphasis' in note for note in bias['nudges'])

def test_recommend_next_block_shift_youth_poor_response():
    prior = AthleteProfile(
        sport='Swimming',
        training_age_years=1,
        season_phase='off_season',
        goal='Endurance',
        equipment_profile='Commercial Gym',
        athlete_level='Beginner',
        technique_consistency=0.6,
        injury_status='none',
        fatigue_level='high',
        weeks_since_break=0,
        cmj_band='low',
        sprint_10m_band='low',
        squat_strength_band='low',
        aerobic_band='low'
    )
    current = AthleteProfile(
        sport='Swimming',
        training_age_years=1,
        season_phase='off_season',
        goal='Endurance',
        equipment_profile='Commercial Gym',
        athlete_level='Beginner',
        technique_consistency=0.6,
        injury_status='none',
        fatigue_level='high',
        weeks_since_break=0,
        cmj_band='low',
        sprint_10m_band='low',
        squat_strength_band='low',
        aerobic_band='low'
    )
    response = BlockResponse(
        prior_blueprint_id='',
        prior_goal='Endurance',
        start_test_bands={'cmj_band': 'low', 'sprint_10m_band': 'low', 'squat_strength_band': 'low', 'aerobic_band': 'low'},
        end_test_bands={'cmj_band': 'low', 'sprint_10m_band': 'low', 'squat_strength_band': 'low', 'aerobic_band': 'low'},
        improvements=[],
        stalls=[],
        regressions=['cmj', 'sprint_10m', 'squat_strength', 'aerobic'],
        recommended_shift='',
        notes=[]
    )
    shift = recommend_next_block_shift(response, current)
    # From the code: if len(response.improvements) == 0 and len(response.regressions) >= 2:
    #   strength_bias -= 1
    #   power_bias -= 1
    #   conditioning_bias -= 1
    #   notes.append("multiple regressions with no improvements; recommending conservative reload / repeat emphasis")
    # But note: we have 4 regressions and 0 improvements, so this condition is met.
    assert shift['strength_bias'] == -1
    assert shift['power_bias'] == -1
    assert shift['conditioning_bias'] == -1
    assert any('conservative reload' in note for note in shift['notes'])

def test_get_next_block_blueprint_bias_strength_up():
    athlete = AthleteProfile(
        sport='Weightlifting',
        training_age_years=5,
        season_phase='off_season',
        goal='Strength',
        equipment_profile='Commercial Gym',
        athlete_level='Advanced',
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='moderate',
        squat_strength_band='low',
        aerobic_band='moderate'
    )
    block_response = BlockResponse(
        prior_blueprint_id='',
        prior_goal='Strength',
        start_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_band': 'low', 'aerobic_band': 'moderate'},
        end_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_band': 'moderate', 'aerobic_band': 'moderate'},
        improvements=['squat_strength'],
        stalls=[],
        regressions=[],
        recommended_shift='Maintain current focus.',
        notes=['squat_strength improved (low->moderate)']
    )
    bias = get_next_block_blueprint_bias(athlete, block_response)
    assert isinstance(bias, dict)
    # We expect that for a strength improvement, there might be some bias
    # The exact keys depend on the athlete profile, but we can check that the bias dict is not empty
    assert len(bias) > 0

def test_get_next_block_blueprint_bias_regressed():
    athlete = AthleteProfile(
        sport='Weightlifting',
        training_age_years=5,
        season_phase='off_season',
        goal='Strength',
        equipment_profile='Commercial Gym',
        athlete_level='Advanced',
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='moderate',
        squat_strength_band='elite',
        aerobic_band='moderate'
    )
    block_response = BlockResponse(
        prior_blueprint_id='',
        prior_goal='Strength',
        start_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_band': 'elite', 'aerobic_band': 'moderate'},
        end_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_bank': 'low', 'aerobic_bank': 'moderate'},
        improvements=[],
        stalls=[],
        regressions=['squat_strength'],
        recommended_shift='Maintain current focus.',
        notes=['squat_strength regressed (elite->low)']
    )
    bias = get_next_block_blueprint_bias(athlete, block_response)
    assert isinstance(bias, dict)
    assert len(bias) > 0

def test_prescription_modifiers_strength_band_affects_squat():
    athlete_low = AthleteProfile(
        sport='Weightlifting',
        training_age_years=5,
        season_phase='off_season',
        goal='Strength',
        equipment_profile='Commercial Gym',
        athlete_level='Advanced',
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='moderate',
        squat_strength_band='low',  # Low band
        aerobic_band='moderate'
    )
    athlete_high = AthleteProfile(
        sport='Weightlifting',
        training_age_years=5,
        season_phase='off_season',
        goal='Strength',
        equipment_profile='Commercial Gym',
        athlete_level='Advanced',
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='moderate',
        squat_strength_band='high',  # High band
        aerobic_band='moderate'
    )
    # We need to get a prescription for a squat exercise, role: MAIN_STRENGTH (since back_squat is likely a main strength exercise)
    from src.forge.prescription_rules import get_athlete_prescription_modifiers
    # We need to create an exercise object for back_squat to get its role, but we can also infer that for squat strength band, the role is MAIN_STRENGTH or SECONDARY_STRENGTH.
    # For simplicity, we will use MAIN_STRENGTH and assume the exercise is a main strength lift.
    mod_low = get_athlete_prescription_modifiers(athlete_low, PrescriptionRole.MAIN_STRENGTH)
    mod_high = get_athlete_prescription_modifiers(athlete_high, PrescriptionRole.MAIN_STRENGTH)
    # We expect that the modifier for strength (e.g., intensity note bias) might be different
    # Since the prescription rules are complex, we just check that the modifiers are not identical (they might be, but we hope not)
    # For the purpose of this test, we assume that the band affects the modifier.
    # We'll check one specific modifier: the intensity_note_bias
    assert mod_low != mod_high, "Expect different modifiers for low vs high squat strength band"

def test_prescription_modifiers_aerobic_band_affects_running():
    athlete_low = AthleteProfile(
        sport='Running',
        training_age_years=4,
        season_phase='pre_season',
        goal='Endurance',
        equipment_profile='Commercial Gym',
        athlete_level='Intermediate',
        technique_consistency=0.85,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='moderate',
        squat_strength_band='moderate',
        aerobic_band='low'  # Low aerobic
    )
    athlete_high = AthleteProfile(
        sport='Running',
        training_age_years=4,
        season_phase='pre_season',
        goal='Endurance',
        equipment_profile='Commercial Gym',
        athlete_level='Intermediate',
        technique_consistency=0.85,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='moderate',
        squat_strength_band='moderate',
        aerobic_band='high'  # High aerobic
    )
    from src.forge.prescription_rules import get_athlete_prescription_modifiers
    # For a tempo run, which is a conditioning exercise, the role is CONDITIONING_LIFT
    mod_low = get_athlete_prescription_modifiers(athlete_low, PrescriptionRole.CONDITIONING_LIFT)
    mod_high = get_athlete_prescription_modifiers(athlete_high, PrescriptionRole.CONDITIONING_LIFT)
    assert mod_low != mod_high, "Expect different modifiers for low vs high aerobic band"

def test_generate_program_different_block_response_changes_output():
    # Create two athletes that are identical except for prior block response (via different current bands)
    # We'll simulate two different prior blocks by setting different current bands
    # and then set the block_response attribute on the athlete.
    # We need to set days_to_match to a value to avoid the issue with None
    # Also need to use proper enums for equipment_profile and season_phase
    base = {
        'sport': 'Rowing',
        'training_age_years': 4,
        'season_phase': SeasonPhase.OFF_SEASON,
        'goal': 'Endurance',
        'equipment_profile': EquipmentProfile.COMMERCIAL_GYM,
        'athlete_level': AthleteLevel.INTERMEDIATE,
        'technique_consistency': 0.9,
        'injury_status': 'none',
        'fatigue_level': 'normal',
        'weeks_since_break': 0,
        'days_to_match': 7,  # Set to avoid None which causes issues
    }
    # Athlete A: low bands
    athlete_a = AthleteProfile(
        **base,
        cmj_band='low',
        sprint_10m_band='low',
        squat_strength_band='low',
        aerobic_band='low'
    )
    # Athlete B: high bands
    athlete_b = AthleteProfile(
        **base,
        cmj_band='high',
        sprint_10m_band='high',
        squat_strength_band='high',
        aerobic_band='high'
    )
    # We need to simulate that these are the current profiles, and we have a prior profile that shows a change.
    # For athlete A: no change (prior = current)
    prior_a = athlete_a
    response_a = build_block_response(prior_a, athlete_a, None)
    athlete_a.block_response = response_a
    # For athlete B: improved from low to high
    prior_b = AthleteProfile(
        **base,
        cmj_band='low',
        sprint_10m_band='low',
        squat_strength_band='low',
        aerobic_band='low'
    )
    response_b = build_block_response(prior_b, athlete_b, None)
    athlete_b.block_response = response_b
    # Generate programs
    program_a = generate_program(athlete_a)
    program_b = generate_program(athlete_b)
    # We expect the programs to be different
    # We'll compare the personalization notes, which should include the block review note.
    # The block review note will be different because the block_response is different.
    notes_a = program_a.personalization_notes
    notes_b = program_b.personalization_notes
    # We expect that the block review note is present in both but different
    block_notes_a = [note for note in notes_a if note.startswith('Block Review:')]
    block_notes_b = [note for note in notes_b if note.startswith('Block Review:')]
    assert len(block_notes_a) > 0, "Expected block review note in program A"
    assert len(block_notes_b) > 0, "Expected block review note in program B"
    # The notes should be different because the block responses are different
    assert block_notes_a[0] != block_notes_b[0], "Expect different block review notes for different block responses"

def test_blueprint_selection_divergence():
    # Test that different athletes get different blueprint biases
    rugby_athlete = AthleteProfile(
        sport='Rugby',
        training_age_years=4,
        season_phase='off_season',
        goal='Strength',
        equipment_profile='Commercial Gym',
        athlete_level='Intermediate',
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='moderate',
        squat_strength_band='low',
        aerobic_band='moderate'
    )
    tennis_athlete = AthleteProfile(
        sport='Tennis',
        training_age_years=4,
        season_phase='off_season',
        goal='Endurance',
        equipment_profile='Commercial Gym',
        athlete_level='Intermediate',
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='low',
        squat_strength_band='moderate',
        aerobic_band='low'
    )
    # Rugby response: squat_strength improved, cmj stalled -> prefer_speed_power = True
    rugby_response = BlockResponse(
        prior_blueprint_id='',
        prior_goal='Strength',
        start_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_band': 'low', 'aerobic_band': 'moderate'},
        end_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_band': 'moderate', 'aerobic_band': 'moderate'},
        improvements=['squat_strength'],
        stalls=['cmj'],
        regressions=[],
        recommended_shift='Maintain current focus.',
        notes=['squat_strength improved (low->moderate)', 'cmj stalled (moderate->moderate)']
    )
    # Tennis response: aerobic improved, sprint_10m stalled -> prefer_power_speed = True, keep_sprint_emphasis = True
    tennis_response = BlockResponse(
        prior_blueprint_id='',
        prior_goal='Endurance',
        start_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'low', 'squat_strength_band': 'moderate', 'aerobic_band': 'low'},
        end_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'low', 'squat_strength_band': 'moderate', 'aerobic_band': 'moderate'},
        improvements=['aerobic'],
        stalls=['sprint_10m'],
        regressions=[],
        recommended_shift='Maintain current focus.',
        notes=['aerobic improved (low->moderate)', 'sprint_10m stalled (low->low)']
    )
    # We will get the blueprint bias for each athlete with their respective responses
    bias_rugby = get_next_block_blueprint_bias(rugby_athlete, rugby_response)
    bias_tennis = get_next_block_blueprint_bias(tennis_athlete, tennis_response)
    # For rugby with squat_strength improvement and cmj stalled, we expect prefer_speed_power to be True
    assert bias_rugby['prefer_speed_power'] == True
    # For tennis with aerobic improvement and sprint_10m stalled, we expect prefer_power_speed and keep_sprint_emphasis to be True
    assert bias_tennis['prefer_power_speed'] == True
    assert bias_tennis['keep_sprint_emphasis'] == True
    # These should be different
    assert bias_rugby != bias_tennis, "Expect different bias for different sports"

def test_backward_compatibility_no_block_response():
    athlete = AthleteProfile(
        sport='Cycling',
        training_age_years=3,
        season_phase=SeasonPhase.OFF_SEASON,
        goal='Endurance',
        equipment_profile=EquipmentProfile.COMMERCIAL_GYM,
        athlete_level=AthleteLevel.INTERMEDIATE,
        technique_consistency=0.85,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='moderate',
        squat_strength_band='moderate',
        aerobic_band='moderate',
        days_to_match=7,  # Set to avoid None which causes issues
    )
    # Ensure no block_response attribute
    if hasattr(athlete, 'block_response'):
        del athlete.block_response
    # Generate program without block response (should be same as before Wave 7)
    program_no_response = generate_program(athlete)
    assert program_no_response is not None
    # We can also check that the personalization notes do not contain block review notes when block_response is None
    # But note: our current main.py will not add block review notes if block_response is None or not present.
    block_notes = [note for note in program_no_response.personalization_notes if note.startswith('Block Review:')]
    assert len(block_notes) == 0, "Expected no block review notes when no block response"

def test_block_response_mixed_improvements_and_regressions():
    """Test when some bands improved and others regressed"""
    prior = AthleteProfile(
        sport='Soccer',
        training_age_years=5,
        season_phase='off_season',
        goal='Endurance',
        equipment_profile='Commercial Gym',
        athlete_level='Advanced',
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='high',
        sprint_10m_band='elite',
        squat_strength_band='elite',
        aerobic_band='elite'
    )
    current = AthleteProfile(
        sport='Soccer',
        training_age_years=5,
        season_phase='off_season',
        goal='Endurance',
        equipment_profile='Commercial Gym',
        athlete_level='Advanced',
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='high',
        sprint_10m_band='moderate',  # Regressed
        squat_strength_band='elite',  # Same
        aerobic_band='high'  # Regressed
    )
    response = build_block_response(prior, current, None)
    assert 'sprint_10m' in response.regressions
    assert 'aerobic' in response.regressions
    assert 'cmj' in response.stalls
    assert 'squat_strength' in response.stalls

def test_block_response_all_same():
    """Test when all bands are the same"""
    prior = AthleteProfile(
        sport='Basketball',
        training_age_years=3,
        season_phase='pre_season',
        goal='Explosiveness',
        equipment_profile='Commercial Gym',
        athlete_level='Intermediate',
        technique_consistency=0.85,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='moderate',
        squat_strength_band='moderate',
        aerobic_band='moderate'
    )
    current = prior
    response = build_block_response(prior, current, None)
    assert response.improvements == []
    assert len(response.stalls) == 4
    assert response.regressions == []

def test_block_response_single_band_change():
    """Test when only one band changes"""
    prior = AthleteProfile(
        sport='Tennis',
        training_age_years=4,
        season_phase='off_season',
        goal='Endurance',
        equipment_profile='Commercial Gym',
        athlete_level='Intermediate',
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='low',
        sprint_10m_band='low',
        squat_strength_band='low',
        aerobic_band='low'
    )
    current = AthleteProfile(
        sport='Tennis',
        training_age_years=4,
        season_phase='off_season',
        goal='Endurance',
        equipment_profile='Commercial Gym',
        athlete_level='Intermediate',
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',  # Only this changed
        sprint_10m_band='low',
        squat_strength_band='low',
        aerobic_band='low'
    )
    response = build_block_response(prior, current, None)
    assert response.improvements == ['cmj']
    assert response.stalls == ['sprint_10m', 'squat_strength', 'aerobic']
    assert response.regressions == []

def test_shift_recommendation_rugby_backline():
    """Test Rugby backline (speed/power emphasis) shift"""
    athlete = AthleteProfile(
        sport='Rugby',
        training_age_years=5,
        season_phase='off_season',
        goal='Strength',
        equipment_profile='Commercial Gym',
        athlete_level='Advanced',
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='moderate',
        squat_strength_band='moderate',
        aerobic_band='moderate',
        force_profile='velocity_deficient'  # Key for velocity deficient
    )
    response = BlockResponse(
        prior_blueprint_id='',
        prior_goal='Strength',
        start_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_band': 'moderate', 'aerobic_band': 'moderate'},
        end_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_band': 'moderate', 'aerobic_band': 'moderate'},
        improvements=[],
        stalls=['sprint_10m'],
        regressions=[],
        recommended_shift='',
        notes=[]
    )
    shift = recommend_next_block_shift(response, athlete)
    # velocity_deficient + sprint_10m stalled -> power_bias += 1
    assert shift['power_bias'] == 1

def test_shift_recommendation_aerobic_regressed_strength_block():
    """Test when aerobic regresses during a strength block"""
    athlete = AthleteProfile(
        sport='Weightlifting',
        training_age_years=5,
        season_phase='off_season',
        goal='Strength',
        equipment_profile='Commercial Gym',
        athlete_level='Advanced',
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='moderate',
        squat_strength_band='moderate',
        aerobic_band='moderate'
    )
    response = BlockResponse(
        prior_blueprint_id='',
        prior_goal='Strength',
        start_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_band': 'moderate', 'aerobic_band': 'high'},
        end_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_band': 'moderate', 'aerobic_band': 'low'},
        improvements=[],
        stalls=[],
        regressions=['aerobic'],
        recommended_shift='',
        notes=[]
    )
    shift = recommend_next_block_shift(response, athlete)
    # aerobic regressed during strength block -> conditioning_bias += 1
    assert shift['conditioning_bias'] == 1

def test_blueprint_bias_rugby_with_force_profile():
    """Test Rugby athlete with force_deficient profile"""
    athlete = AthleteProfile(
        sport='Rugby',
        training_age_years=5,
        season_phase='off_season',
        goal='Strength',
        equipment_profile='Commercial Gym',
        athlete_level='Advanced',
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='moderate',
        squat_strength_band='low',
        aerobic_band='moderate',
        force_profile='force_deficient'
    )
    response = BlockResponse(
        prior_blueprint_id='',
        prior_goal='Strength',
        start_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_band': 'low', 'aerobic_band': 'moderate'},
        end_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_band': 'moderate', 'aerobic_band': 'moderate'},
        improvements=['squat_strength'],
        stalls=['cmj'],
        regressions=[],
        recommended_shift='Maintain current focus.',
        notes=['squat_strength improved', 'cmj stalled']
    )
    bias = get_next_block_blueprint_bias(athlete, response)
    assert bias['prefer_speed_power'] == True

def test_blueprint_bias_youth_good_response():
    """Test youth athlete with good response (should not lower fatigue)"""
    athlete = AthleteProfile(
        sport='Soccer',
        training_age_years=2,
        season_phase='off_season',
        goal='Endurance',
        equipment_profile='Commercial Gym',
        athlete_level='Beginner',
        technique_consistency=0.7,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='low',
        sprint_10m_band='low',
        squat_strength_band='low',
        aerobic_band='low',
        age=16
    )
    response = BlockResponse(
        prior_blueprint_id='',
        prior_goal='Endurance',
        start_test_bands={'cmj_band': 'low', 'sprint_10m_band': 'low', 'squat_strength_band': 'low', 'aerobic_band': 'low'},
        end_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_band': 'moderate', 'aerobic_band': 'moderate'},
        improvements=['cmj', 'sprint_10m', 'squat_strength', 'aerobic'],
        stalls=[],
        regressions=[],
        recommended_shift='Maintain current focus.',
        notes=['cmj improved', 'sprint_10m improved', 'squat_strength improved', 'aerobic improved']
    )
    bias = get_next_block_blueprint_bias(athlete, response)
    # Good response, so lower_fatigue should be False
    assert bias['lower_fatigue'] == False
    assert bias['maintain_same_blueprint'] == False

def test_prescription_modifiers_plyo_with_low_cmj():
    """Test plyometric prescription with low cmj band"""
    athlete = AthleteProfile(
        sport='Basketball',
        training_age_years=3,
        season_phase='pre_season',
        goal='Explosiveness',
        equipment_profile='Commercial Gym',
        athlete_level='Intermediate',
        technique_consistency=0.85,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='low',
        sprint_10m_band='moderate',
        squat_strength_band='moderate',
        aerobic_band='moderate'
    )
    from src.forge.prescription_rules import get_athlete_prescription_modifiers
    mod = get_athlete_prescription_modifiers(athlete, PrescriptionRole.PLYOMETRIC)
    # Low cmj band should result in set_cap and conservative note
    assert mod.get('set_cap') is not None
    assert 'conservative' in mod.get('intensity_note_bias', '').lower()

def test_prescription_modifiers_sprint_with_high_band():
    """Test sprint prescription with high sprint band"""
    athlete = AthleteProfile(
        sport='Soccer',
        training_age_years=4,
        season_phase='in_season',
        goal='Speed',
        equipment_profile='Commercial Gym',
        athlete_level='Advanced',
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='high',
        sprint_10m_band='high',
        squat_strength_band='high',
        aerobic_band='moderate'
    )
    from src.forge.prescription_rules import get_athlete_prescription_modifiers
    mod = get_athlete_prescription_modifiers(athlete, PrescriptionRole.SPRINT_MECHANICS)
    # High sprint band should result in velocity-oriented note
    assert 'velocity' in mod.get('intensity_note_bias', '').lower()

def test_prescription_modifiers_main_strength_with_high_band():
    """Test main strength prescription with high squat strength band"""
    athlete = AthleteProfile(
        sport='Powerlifting',
        training_age_years=6,
        season_phase='off_season',
        goal='Strength',
        equipment_profile='Commercial Gym',
        athlete_level='Advanced',
        technique_consistency=0.95,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='high',
        sprint_10m_band='high',
        squat_strength_band='high',
        aerobic_band='high'
    )
    from src.forge.prescription_rules import get_athlete_prescription_modifiers
    mod = get_athlete_prescription_modifiers(athlete, PrescriptionRole.MAIN_STRENGTH)
    # High squat strength band should result in power bias note
    assert 'power' in mod.get('intensity_note_bias', '').lower() or 'explosive' in mod.get('intensity_note_bias', '').lower()

def test_generate_program_with_tennis_athlete():
    """Test generating a program for a tennis athlete"""
    athlete = AthleteProfile(
        sport='Tennis',
        training_age_years=4,
        season_phase=SeasonPhase.OFF_SEASON,
        goal='Endurance',
        equipment_profile=EquipmentProfile.COMMERCIAL_GYM,
        athlete_level=AthleteLevel.INTERMEDIATE,
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='moderate',
        squat_strength_band='moderate',
        aerobic_band='moderate',
        days_to_match=7
    )
    # Set a block response
    response = build_block_response(athlete, athlete, None)
    athlete.block_response = response
    program = generate_program(athlete)
    assert program is not None
    assert len(program.sessions) > 0

def test_generate_program_with_rugby_athlete():
    """Test generating a program for a rugby athlete"""
    athlete = AthleteProfile(
        sport='Rugby',
        training_age_years=5,
        season_phase=SeasonPhase.OFF_SEASON,
        goal='Strength',
        equipment_profile=EquipmentProfile.COMMERCIAL_GYM,
        athlete_level=AthleteLevel.ADVANCED,
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='moderate',
        squat_strength_band='moderate',
        aerobic_band='moderate',
        days_to_match=7,
        position_role='prop'
    )
    # Set a block response
    response = build_block_response(athlete, athlete, None)
    athlete.block_response = response
    program = generate_program(athlete)
    assert program is not None
    assert len(program.sessions) > 0

def test_block_review_note_in_personalization():
    """Test that block review notes appear in personalization notes"""
    athlete = AthleteProfile(
        sport='Rowing',
        training_age_years=4,
        season_phase=SeasonPhase.OFF_SEASON,
        goal='Endurance',
        equipment_profile=EquipmentProfile.COMMERCIAL_GYM,
        athlete_level=AthleteLevel.INTERMEDIATE,
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='low',
        sprint_10m_band='low',
        squat_strength_band='low',
        aerobic_band='low',
        days_to_match=7
    )
    prior = AthleteProfile(
        sport='Rowing',
        training_age_years=4,
        season_phase=SeasonPhase.OFF_SEASON,
        goal='Endurance',
        equipment_profile=EquipmentProfile.COMMERCIAL_GYM,
        athlete_level=AthleteLevel.INTERMEDIATE,
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',  # Improved
        sprint_10m_band='moderate',  # Improved
        squat_strength_band='moderate',  # Improved
        aerobic_band='moderate',  # Improved
        days_to_match=7
    )
    response = build_block_response(prior, athlete, None)
    athlete.block_response = response
    program = generate_program(athlete)
    block_notes = [n for n in program.personalization_notes if 'Block Review' in n]
    assert len(block_notes) > 0
    # Check that the note mentions the improvements
    note_text = block_notes[0].lower()
    assert 'improved' in note_text or 'stalled' in note_text or 'regressed' in note_text

def test_backward_compatibility_with_days_to_match():
    """Test that generate_program works with days_to_match set"""
    athlete = AthleteProfile(
        sport='Running',
        training_age_years=3,
        season_phase=SeasonPhase.OFF_SEASON,
        goal='Endurance',
        equipment_profile=EquipmentProfile.COMMERCIAL_GYM,
        athlete_level=AthleteLevel.INTERMEDIATE,
        technique_consistency=0.85,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='moderate',
        squat_strength_band='moderate',
        aerobic_band='moderate',
        days_to_match=10
    )
    program = generate_program(athlete)
    assert program is not None
    assert program.blueprint_id is not None

def test_recommend_shift_no_changes():
    """Test shift recommendation when nothing changed"""
    response = BlockResponse(
        prior_blueprint_id='',
        prior_goal='Endurance',
        start_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_band': 'moderate', 'aerobic_band': 'moderate'},
        end_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_band': 'moderate', 'aerobic_band': 'moderate'},
        improvements=[],
        stalls=['cmj', 'sprint_10m', 'squat_strength', 'aerobic'],
        regressions=[],
        recommended_shift='',
        notes=[]
    )
    shift = recommend_next_block_shift(response, None)
    # All biases should be 0 since no improvements or regressions
    assert shift['strength_bias'] == 0
    assert shift['power_bias'] == 0
    assert shift['conditioning_bias'] == 0

def test_band_order_edge_cases():
    """Test band classification with edge cases"""
    # Test 'avg' which is between low and moderate
    assert classify_band_change('avg', 'moderate') == 'same'  # Both have value 2
    assert classify_band_change('low', 'avg') == 'improved'  # 1 -> 2

def test_get_next_block_blueprint_bias_empty_response():
    """Test get_next_block_blueprint_bias with empty improvements/regressions"""
    athlete = AthleteProfile(
        sport='Swimming',
        training_age_years=3,
        season_phase='off_season',
        goal='Endurance',
        equipment_profile='Commercial Gym',
        athlete_level='Intermediate',
        technique_consistency=0.85,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='moderate',
        squat_strength_band='moderate',
        aerobic_band='moderate'
    )
    response = BlockResponse(
        prior_blueprint_id='',
        prior_goal='Endurance',
        start_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_band': 'moderate', 'aerobic_band': 'moderate'},
        end_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_band': 'moderate', 'aerobic_band': 'moderate'},
        improvements=[],
        stalls=['cmj', 'sprint_10m', 'squat_strength', 'aerobic'],
        regressions=[],
        recommended_shift='',
        notes=[]
    )
    bias = get_next_block_blueprint_bias(athlete, response)
    # Should return a dict with all False values for a non-youth athlete with no improvements but stalls
    assert bias['prefer_power_speed'] == False
    assert bias['prefer_speed_power'] == False
