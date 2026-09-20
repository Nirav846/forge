# Additional Wave 7 tests to reach 30+
# This script generates additional tests that we append to the test file

content = '''
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
        aerobic_band='low',
        days_to_match=7
    )
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
'''
with open('D:/forge/tests/test_wave7_hardening.py', 'a') as f:
    f.write(content)