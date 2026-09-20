import pytest
from src.forge.models import AthleteProfile, BlockResponse
from src.forge.block_autoregulation import classify_band_change, build_block_response, recommend_next_block_shift, get_next_block_blueprint_bias

def test_classify_band_change():
    assert classify_band_change("low", "moderate") == "improved"
    assert classify_band_change("moderate", "high") == "improved"
    assert classify_band_change("high", "elite") == "improved"
    assert classify_band_change("elite", "high") == "regressed"
    assert classify_band_change("high", "moderate") == "regressed"
    assert classify_band_change("moderate", "low") == "regressed"
    assert classify_band_change("low", "low") == "same"
    assert classify_band_change("moderate", "moderate") == "same"
    assert classify_band_change("high", "high") == "same"
    assert classify_band_change("elite", "elite") == "same"
    assert classify_band_change(None, "low") == "unknown"
    assert classify_band_change("low", None) == "unknown"
    assert classify_band_change("invalid", "low") == "unknown"
    assert classify_band_change("low", "invalid") == "unknown"

def test_build_block_response_no_prior():
    # When no prior data, block response should still be creatable with default values
    athlete = AthleteProfile(
        sport="Cricket",
        training_age_years=5,
        season_phase="off_season",
        goal="Power",
        equipment_profile="Commercial Gym",
        athlete_level="Advanced",
        technique_consistency=0.9,
        injury_status="none",
        fatigue_level="normal",
        weeks_since_break=0,
        cmj_band="moderate",
        sprint_10m_band="high",
        squat_strength_band="moderate",
        aerobic_band="low"
    )
    # No prior profile or program
    response = build_block_response(None, athlete, None)
    assert response.prior_blueprint_id == ""
    assert response.prior_goal == ""
    assert response.start_test_bands == {"cmj_band": None, "sprint_10m_band": None, "squat_strength_band": None, "aerobic_band": None}
    assert response.end_test_bands == {"cmj_band": "moderate", "sprint_10m_band": "high", "squat_strength_band": "moderate", "aerobic_band": "low"}
    assert response.improvements == []
    assert response.stalls == []
    assert response.regressions == []
    assert response.recommended_shift == "Maintain current focus."
    assert response.notes == []