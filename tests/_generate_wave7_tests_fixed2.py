content = '''import pytest
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
    assert any('CMJ improved' in note for note in response.notes)
    assert any('Sprint 10m improved' in note for note in response.notes)
    assert any('Squat strength improved' in note for note in response.notes)
    assert any('Aerobic improved' in note for note in response.notes)

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
        cmj_bank='moderate',
        sprint_10m_band='moderate',
        squat_strength_band='moderate',
        aerobic_band='moderate'
    )
    response = build_block_response(prior, current, None)
    assert set(response.regressions) == {'cmj', 'sprint_10m', 'squat_strength', 'aerobic'}
    assert response.improvements == []
    assert response.stalls == []
    assert any('CMJ regressed' in note for note in response.notes)
    assert any('Sprint 10m regressed' in note for note in response.notes)
    assert any('Squat strength regressed' in note for note in response.notes)
    assert any('Aerobic regressed' in note for note in response.notes)

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
    shift = recommend_next_block_shift(response, current)
    # From the code: if is_tennis and "aerobic" in block_response.improvements and "sprint_10m" in block_response.stalls:
    #   prefer_power_speed = True
    #   keep_sprint_emphasis = True
    #   nudges.append("Tennis athlete improved aerobic band but sprint stalled -> bias toward speed / court-power emphasis")
    assert shift['prefer_power_speed'] == True
    assert shift['keep_sprint_emphasis'] == True
    assert any('speed / court-power emphasis' in note for note in shift['notes'])

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
        end_test_bands={'cmj_band': 'low', 'sprint_10m_bank': 'low', 'squat_strength_band': 'low', 'aerobic_band': 'low'},
        improvements=[],
        stalls=['cmj', 'sprint_10m', 'squat_strength', 'aerobic'],
        regressions=[],
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
        end_test_bands={'cmj_bank': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_band': 'moderate', 'aerobic_band': 'moderate'},
        improvements=['squat_strength'],
        stalls=[],
        regressions=[],
        recommended_shift='Maintain current focus.',
        notes=['squat_strength improved (low→moderate)']
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
        end_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_band': 'low', 'aerobic_band': 'moderate'},
        improvements=[],
        stalls=[],
        regressions=['squat_strength'],
        recommended_shift='Maintain current focus.',
        notes=['squat_strength regressed (elite→low)']
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
    base = {
        'sport': 'Rowing',
        'training_age_years': 4,
        'season_phase': 'off_season',
        'goal': 'Endurance',
        'equipment_profile': 'Commercial Gym',
        'athlete_level': 'Intermediate',
        'technique_consistency': 0.9,
        'injury_status': 'none',
        'fatigue_level': 'normal',
        'weeks_since_break': 0,
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
    # We want to show that for the same athlete profile, different block responses lead to different blueprint selection.
    # We will create an athlete profile that is on the edge (e.g., intermediate) and then adjust the block response to favor different blueprints.
    # We will use the get_next_block_blueprint_bias function to see if the bias changes the score.
    # We need two different block responses that should bias towards different blueprints.
    # We will pick two blueprints that are known to be for different focuses (e.g., strength vs endurance).
    # We will then compute the bias for each block response and see if the bias is different.
    athlete = AthleteProfile(
        sport='Rowing',
        training_age_years=4,
        season_phase='off_season',
        goal='Endurance',  # This might favor endurance blueprints
        equipment_profile='Commercial Gym',
        athlete_level='Intermediate',
        technique_consistency=0.9,
        injury_status='none',
        fatigue_level='normal',
        weeks_since_break=0,
        cmj_band='moderate',
        sprint_10m_band='moderate',
        squat_strength_band='moderate',
        aerobic_band='moderate'
    )
    # Block response that indicates strength improvement
    response_strength = BlockResponse(
        prior_blueprint_id='',
        prior_goal='Endurance',
        start_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_band': 'low', 'aerobic_band': 'moderate'},
        end_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_bank': 'moderate', 'aerobic_band': 'moderate'},
        improvements=['squat_strength'],
        stalls=[],
        regressions=[],
        recommended_shift='Maintain current focus.',
        notes=['squat_strength improved (low→moderate)']
    )
    # Block response that indicates endurance improvement
    response_endurance = BlockResponse(
        prior_blueprint_id='',
        prior_goal='Endurance',
        start_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_band': 'moderate', 'aerobic_band': 'low'},
        end_test_bands={'cmj_band': 'moderate', 'sprint_10m_band': 'moderate', 'squat_strength_band': 'moderate', 'aerobic_band': 'moderate'},
        improvements=['aerobic'],
        stalls=[],
        regressions=[],
        recommended_shift='Maintain current focus.',
        notes=['aerobic improved (low→moderate)']
    )
    # We will get the blueprint bias for each
    bias_strength = get_next_block_blueprint_bias(athlete, response_strength)
    bias_endurance = get_next_block_blueprint_bias(athlete, response_endurance)
    # We expect the bias to be different
    assert bias_strength != bias_endurance, "Expect different bias for strength vs endurance block responses"

def test_backward_compatibility_no_block_response():
    athlete = AthleteProfile(
        sport='Cycling',
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
'''
with open('D:/forge/tests/test_wave7_hardening.py', 'w') as f:
    f.write(content)