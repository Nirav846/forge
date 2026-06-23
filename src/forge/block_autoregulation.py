"""Wave 7 — Block Autoregulation Engine."""
from typing import Optional, Any
from .models import AthleteProfile, GeneratedProgram, BlockResponse

BAND_ORDER = {
    "low": 1,
    "avg": 2,
    "moderate": 2,
    "high": 3,
    "elite": 4,
}

BAND_NAMES = {
    "cmj_band": "cmj",
    "sprint_10m_band": "sprint_10m",
    "squat_strength_band": "squat_strength",
    "aerobic_band": "aerobic",
}


def classify_band_change(before: Optional[str], after: Optional[str]) -> str:
    """Classify change from before and after bands as improved, same, regressed, or unknown."""
    if before is None or after is None:
        return "unknown"
    
    b = before.strip().lower()
    a = after.strip().lower()
    
    if b not in BAND_ORDER or a not in BAND_ORDER:
        return "unknown"
        
    val_b = BAND_ORDER[b]
    val_a = BAND_ORDER[a]
    
    if val_a > val_b:
        return "improved"
    elif val_a < val_b:
        return "regressed"
    else:
        return "same"


def build_block_response(
    prior_profile: Optional[AthleteProfile],
    current_profile: AthleteProfile,
    prior_program: Optional[GeneratedProgram] = None
) -> BlockResponse:
    """Build a BlockResponse summary showing how the athlete responded to the prior block."""
    # Use profile snapshot from prior program if prior_profile not explicitly passed
    if prior_profile is None and prior_program is not None:
        prior_profile = getattr(prior_program, "athlete_profile", None)

    prior_blueprint_id = ""
    prior_goal = ""
    if prior_program is not None:
        prior_blueprint_id = str(getattr(prior_program, "blueprint_id", ""))
        prior_goal = getattr(prior_program, "goal", "")
    elif prior_profile is not None:
        prior_goal = getattr(prior_profile, "goal", "")

    start_test_bands = {}
    end_test_bands = {}
    improvements = []
    stalls = []
    regressions = []
    notes = []

    for field_name, short_name in BAND_NAMES.items():
        before_val = getattr(prior_profile, field_name, None) if prior_profile else None
        after_val = getattr(current_profile, field_name, None)
        
        start_test_bands[field_name] = before_val
        end_test_bands[field_name] = after_val
        
        change = classify_band_change(before_val, after_val)
        if change == "improved":
            improvements.append(short_name)
            notes.append(f"{short_name} improved ({before_val}→{after_val})")
        elif change == "same":
            stalls.append(short_name)
            notes.append(f"{short_name} stalled ({before_val}→{after_val})")
        elif change == "regressed":
            regressions.append(short_name)
            notes.append(f"{short_name} regressed ({before_val}→{after_val})")

    # Call recommend_next_block_shift to determine shift and recommended shift string
    temp_response = BlockResponse(
        prior_blueprint_id=prior_blueprint_id,
        prior_goal=prior_goal,
        start_test_bands=start_test_bands,
        end_test_bands=end_test_bands,
        improvements=improvements,
        stalls=stalls,
        regressions=regressions,
        recommended_shift="",
        notes=notes
    )
    
    rec = recommend_next_block_shift(temp_response, current_profile)
    rec_notes = rec.get("notes", [])
    recommended_shift = "; ".join(rec_notes) if rec_notes else "Maintain current focus."

    return BlockResponse(
        prior_blueprint_id=prior_blueprint_id,
        prior_goal=prior_goal,
        start_test_bands=start_test_bands,
        end_test_bands=end_test_bands,
        improvements=improvements,
        stalls=stalls,
        regressions=regressions,
        recommended_shift=recommended_shift,
        notes=notes
    )


def recommend_next_block_shift(response: BlockResponse, current_profile: Optional[AthleteProfile] = None) -> dict:
    """Recommend next block bias adjustments as a deterministic rule-based output."""
    strength_bias = 0
    power_bias = 0
    conditioning_bias = 0
    notes = []

    # 1. squat_strength improved but cmj stalled -> next block shifts toward power conversion
    if "squat_strength" in response.improvements and "cmj" in response.stalls:
        strength_bias -= 1
        power_bias += 1
        notes.append("squat_strength improved but CMJ stalled; shifting next block toward power conversion")

    # 2. sprint_10m stalled and athlete is velocity-deficient -> keep speed/power emphasis
    is_velocity_deficient = False
    if current_profile and getattr(current_profile, "force_profile", None) == "velocity_deficient":
        is_velocity_deficient = True
    
    if "sprint_10m" in response.stalls and is_velocity_deficient:
        power_bias += 1
        notes.append("sprint_10m stalled and athlete is velocity-deficient; retaining speed/power emphasis")

    # 3. aerobic_band regressed during a strength block -> next block adds mild conditioning bias
    is_strength_block = False
    if response.prior_goal and response.prior_goal.upper() in ("STR", "STRENGTH"):
        is_strength_block = True
    elif "strength" in response.prior_blueprint_id.lower():
        is_strength_block = True
        
    if "aerobic" in response.regressions and is_strength_block:
        conditioning_bias += 1
        notes.append("aerobic_band regressed during strength block; adding mild conditioning bias")

    # 4. If nothing improved and 2+ metrics regressed -> recommend conservative reload / repeat emphasis
    if len(response.improvements) == 0 and len(response.regressions) >= 2:
        strength_bias -= 1
        power_bias -= 1
        conditioning_bias -= 1
        notes.append("multiple regressions with no improvements; recommending conservative reload / repeat emphasis")

    return {
        "strength_bias": strength_bias,
        "power_bias": power_bias,
        "conditioning_bias": conditioning_bias,
        "notes": notes
    }


def get_next_block_blueprint_bias(athlete_profile: AthleteProfile, block_response: BlockResponse) -> dict:
    """Determine blueprint level nudges from the block response."""
    prefer_power_speed = False
    prefer_speed_power = False
    reduce_conditioning = False
    maintain_same_blueprint = False
    lower_fatigue = False
    keep_sprint_emphasis = False
    add_conditioning_bias = False
    nudges = []

    sport = athlete_profile.sport.lower() if athlete_profile.sport else ""
    is_rugby = any(s in sport for s in ("rugby", "american_football", "rugby_union", "rugby_league"))
    is_tennis = any(s in sport for s in ("tennis", "badminton", "squash"))

    # Rugby prop improved force but CMJ stalled -> bias next block toward power conversion, not brute force
    if is_rugby and "squat_strength" in block_response.improvements and "cmj" in block_response.stalls:
        prefer_speed_power = True
        nudges.append("Rugby athlete improved force but CMJ stalled -> bias next block toward power conversion, not brute force")

    # Tennis player improved aerobic band but sprint stalled -> bias toward speed / court-power emphasis
    if is_tennis and "aerobic" in block_response.improvements and "sprint_10m" in block_response.stalls:
        prefer_power_speed = True
        keep_sprint_emphasis = True
        nudges.append("Tennis athlete improved aerobic band but sprint stalled -> bias toward speed / court-power emphasis")

    # Youth athlete with poor response -> stay conservative, repeat or slightly regress emphasis
    is_youth = athlete_profile.age < 20 or "youth" in (athlete_profile.position_role or "").lower()
    has_poor_response = len(block_response.improvements) == 0 and len(block_response.regressions) >= 1
    if is_youth and has_poor_response:
        lower_fatigue = True
        maintain_same_blueprint = True
        nudges.append("Youth athlete with poor response -> stay conservative, repeat or slightly regress emphasis")

    # If nothing improved and 2+ metrics regressed -> choose lower fatigue option if high risk
    if len(block_response.improvements) == 0 and len(block_response.regressions) >= 2:
        lower_fatigue = True
        nudges.append("multiple regressions with no improvements -> choose lower fatigue option")

    # Aerobic regressed during a strength block -> next block adds mild conditioning bias
    is_strength_block = False
    if block_response.prior_goal and block_response.prior_goal.upper() in ("STR", "STRENGTH"):
        is_strength_block = True
    elif "strength" in block_response.prior_blueprint_id.lower():
        is_strength_block = True
        
    if "aerobic" in block_response.regressions and is_strength_block:
        add_conditioning_bias = True

    return {
        "prefer_power_speed": prefer_power_speed,
        "prefer_speed_power": prefer_speed_power,
        "reduce_conditioning": reduce_conditioning,
        "maintain_same_blueprint": maintain_same_blueprint,
        "lower_fatigue": lower_fatigue,
        "keep_sprint_emphasis": keep_sprint_emphasis,
        "add_conditioning_bias": add_conditioning_bias,
        "nudges": nudges
    }
