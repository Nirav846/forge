content = '''import pytest
from src.forge.models import AthleteProfile, BlockResponse, AthleteLevel, SeasonPhase, EquipmentProfile
from src.forge.block_autoregulation import classify_band_change, build_block_response, recommend_next_block_shift, get_next_block_blueprint_bias
from src.forge.blueprint_engine import select_blueprint, _score_blueprint_for_bias
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
    response = build_block_response(prior, current, None)
    assert 'squat_strength' in response.improvements
    assert 'cmj' in response.stalls
    assert 'sprint_10m' in response.stalls
    assert 'aerobic' in response.stalls
    assert any('squat_strength improved' in note for note in response.notes)
    assert any('CMJ stalled' in note for note in response.notes)

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
        cmj_band='moderate',
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
    response = build_block_response(prior, current, None)
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
    response = build_block_response(prior, current, None)
    shift = recommend_next_block_shift(response, current)
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
    response = build_block_response(prior, current, None)
    shift = recommend_next_block_shift(response, current)
    assert shift['reduce_load'] == True
    assert shift['increase_recovery'] == True
    assert any('reduce load' in note for note in shift['notes'])
    assert any('increase recovery' in note for note in shift['notes'])

def test_get_next_block_blueprint_bias_strength_up():
    block_response = BlockResponse(
        improvements=['squat_strength'],
        stalls=[],
        regressions=[],
        notes=['squat_strength improved'],
        recommended_shift='Maintain current focus.'
    )
    bias = get_next_block_blueprint_bias(block_response)
    assert isinstance(bias, dict)
    if block_response.improvements:
        assert any(score != 0 for score in bias.values()), "Expected non-zero bias for improvements"

def test_get_next_block_blueprint_bias_regressed():
    block_response = BlockResponse(
        improvements=[],
        stalls=[],
        regressions=['squat_strength'],
        notes=['squat_strength regressed'],
        recommended_shift='Maintain current focus.'
    )
    bias = get_next_block_blueprint_bias(block_response)
    assert isinstance(bias, dict)
    if block_response.regressions:
        assert any(score != 0 for score in bias.values()), "Expected non-zero bias for regressions"

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
        squat_strength_band='low',
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
        squat_strength_band='high',
        aerobic_band='moderate'
    )
    from src.forge.prescription_rules import get_athlete_prescription_modifiers
    mod_low = get_athlete_prescription_modifiers(athlete_low, PrescriptionRole.STRENGTH, 'back_squat', 4, 6)
    mod_high = get_athlete_prescription_modifiers(athlete_high, PrescriptionRole.STRENGTH, 'back_squat', 4, 6)
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
        aerobic_band='low'
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
        aerobic_band='high'
    )
    from src.forge.prescription_rules import get_athlete_prescription_modifiers
    mod_low = get_athlete_prescription_modifiers(athlete_low, PrescriptionRole.ENDURANCE, 'tempo_run', 20, 30)
    mod_high = get_athlete_prescription_modifiers(athlete_high, PrescriptionRole.ENDURANCE, 'tempo_run', 20, 30)
    assert mod_low != mod_high, "Expect different modifiers for low vs high aerobic band"

def test_generate_program_different_block_response_changes_output():
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
    athlete_a = AthleteProfile(
        **base,
        cmj_band='low',
        sprint_10m_band='low',
        squat_strength_band='low',
        aerobic_band='low'
    )
    athlete_b = AthleteProfile(
        **base,
        cmj_band='high',
        sprint_10m_band='high',
        squat_strength_band='high',
        aerobic_band='high'
    )
    prior_a = athlete_a
    response_a = build_block_response(prior_a, athlete_a, None)
    prior_b = AthleteProfile(
        **base,
        cmj_band='low',
        sprint_10m_band='low',
        squat_strength_band='low',
        aerobic_band='low'
    )
    response_b = build_block_response(prior_b, athlete_b, None)
    program_a = generate_program(athlete_a, block_response=response_a)
    program_b = generate_program(athlete_b, block_response=response_b)
    assert program_a != program_b, "Expect different programs for different block responses"

def test_blueprint_selection_divergence():
    athlete = AthleteProfile(
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
        sprint_10m_band='moderate',
        squat_strength_band='moderate',
        aerobic_band='moderate'
    )
    response_strength = BlockResponse(
        improvements=['squat_strength'],
        stalls=[],
        regressions=[],
        notes=['squat_strength improved'],
        recommended_shift='Maintain current focus.'
    )
    response_endurance = BlockResponse(
        improvements=['aerobic'],
        stalls=[],
        regressions=[],
        notes=['aerobic improved'],
        recommended_shift='Maintain current focus.'
    )
    bias_strength = get_next_block_blueprint_bias(response_strength)
    bias_endurance = get_next_block_blueprint_bias(response_endurance)
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
    program_no_response = generate_program(athlete, block_response=None)
    assert program_no_response is not None
'''
with open('D:/forge/tests/test_wave7_hardening.py', 'w') as f:
    f.write(content)