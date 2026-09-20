"""Recovery engine — selects recovery protocols based on fatigue level and session type."""

from .models import RecoveryDrill, RecoveryProtocol, AthleteProfile


# Recovery Drill Library (simplified from FORGE_RECOVERY_LIBRARY_V1.md)
RECOVERY_DRILLS = {
    # General recovery circuit stations
    "foam_roll_quads": RecoveryDrill(
        name="Foam roll quads",
        duration_sec=120,  # 2 min/leg
        notes="Slow, find tight spots"
    ),
    "foam_roll_glutes": RecoveryDrill(
        name="Foam roll glutes",
        duration_sec=120,  # 2 min/side
        notes="Sit on roller, cross ankle to knee"
    ),
    "glute_bridge": RecoveryDrill(
        name="Glute bridge (bodyweight)",
        duration_sec=30,  # 15 reps
        notes="3s up, 3s down"
    ),
    "deep_squat_hold": RecoveryDrill(
        name="Deep squat hold",
        duration_sec=60,  # 60s
        notes="Elbows push knees out"
    ),
    "worlds_greatest_stretch": RecoveryDrill(
        name="World's greatest stretch",
        duration_sec=90,  # 45s/side
        notes="Pulse at end range"
    ),
    "cat_cow": RecoveryDrill(
        name="Cat-cow",
        duration_sec=60,  # 1 min
        notes="Breathe deeply"
    ),
    "dead_bug": RecoveryDrill(
        name="Dead bug",
        duration_sec=60,  # 6/side
        notes="Slow and controlled"
    ),
    "childs_pose": RecoveryDrill(
        name="Child's pose",
        duration_sec=90,  # 90s
        notes="Breathe into lower back"
    ),
    
    # Lower body recovery circuit
    "foam_roll_hamstrings": RecoveryDrill(
        name="Foam roll hamstrings",
        duration_sec=120,  # 2 min/leg
        notes="Roll from knee to glute"
    ),
    "lacrosse_ball_glute": RecoveryDrill(
        name="Lacrosse ball glute",
        duration_sec=60,  # 1 min/side
        notes="Sit on ball, find trigger points"
    ),
    "band_hamstring_stretch": RecoveryDrill(
        name="Band hamstring stretch",
        duration_sec=90,  # 45s/leg
        notes="Supine, flex foot"
    ),
    "quad_stretch_lying": RecoveryDrill(
        name="Quad stretch (lying)",
        duration_sec=90,  # 45s/leg
        notes="Side lying, pull heel"
    ),
    "couch_stretch": RecoveryDrill(
        name="Couch stretch",
        duration_sec=120,  # 60s/leg
        notes="Quad + hip flexor"
    ),
    "adductor_rock": RecoveryDrill(
        name="Adductor rock",
        duration_sec=90,  # 45s
        notes="Seated, soles together, push knees down"
    ),
    "walk_easy": RecoveryDrill(
        name="Walk (easy)",
        duration_sec=180,  # 3 min
        notes="On grass or track"
    ),
    
    # Upper body recovery circuit
    "foam_roll_tspine": RecoveryDrill(
        name="Foam roll T-spine",
        duration_sec=120,  # 2 min
        notes="Roll from mid-back to upper-back"
    ),
    "lacrosse_ball_shoulder": RecoveryDrill(
        name="Lacrosse ball shoulder",
        duration_sec=60,  # 1 min/side
        notes="On floor, ball under rear delt"
    ),
    "band_pull_apart": RecoveryDrill(
        name="Band pull-apart",
        duration_sec=30,  # 15 reps
        notes="Slow, squeeze at end"
    ),
    "pvc_pass_throughs": RecoveryDrill(
        name="PVC pass-throughs",
        duration_sec=30,  # 10 reps
        notes="Narrow as comfortable"
    ),
    "shoulder_cars": RecoveryDrill(
        name="Shoulder CARs",
        duration_sec=30,  # 3 each direction/side
        notes="Full circle"
    ),
    "neck_cars": RecoveryDrill(
        name="Neck CARs",
        duration_sec=24,  # 2 each direction
        notes="Slow, controlled"
    ),
    "wall_slides": RecoveryDrill(
        name="Wall slides",
        duration_sec=30,  # 10 reps
        notes="Focus on scapular control"
    ),
    "childs_pose_side_reach": RecoveryDrill(
        name="Child's pose + side reach",
        duration_sec=90,  # 45s/side
        notes="Reach hands to the side"
    ),
    
    # Full body recovery circuit
    "foam_roll_full_back": RecoveryDrill(
        name="Foam roll full back",
        duration_sec=180,  # 3 min
        notes="Lats, T-spine, glutes"
    ),
    "lacrosse_ball_feet": RecoveryDrill(
        name="Lacrosse ball feet",
        duration_sec=60,  # 1 min/side
        notes="Arch, heel, ball of foot"
    ),
    "hip_cars": RecoveryDrill(
        name="Hip CARs",
        duration_sec=30,  # 3 each direction/side
        notes="Standing, controlled"
    ),
    "supine_90_90_hamstring": RecoveryDrill(
        name="Supine 90/90 hamstring stretch",
        duration_sec=90,  # 45s/leg
        notes="Flex foot, hold"
    ),
    "figure_4_glute": RecoveryDrill(
        name="Figure 4 glute stretch",
        duration_sec=90,  # 45s/leg
        notes="Supine, pull chest"
    ),
    "side_lying_tspine_rotation": RecoveryDrill(
        name="Side-lying T-spine rotation",
        duration_sec=90,  # 45s/side
        notes="Open to ceiling"
    ),
    "seated_adductor_stretch": RecoveryDrill(
        name="Seated adductor stretch",
        duration_sec=120,  # 60s
        notes="Soles together, push knees"
    ),
    "deep_breathing": RecoveryDrill(
        name="Deep breathing (box pattern)",
        duration_sec=180,  # 3 min
        notes="4-4-4-4 count"
    ),
    
    # Pool recovery
    "pool_walk_jog": RecoveryDrill(
        name="Pool walk/jog",
        duration_sec=1200,  # 15-20 min
        notes="Walk in chest-deep water, progressive to high-knee jog"
    ),
    "deep_water_running": RecoveryDrill(
        name="Deep water running",
        duration_sec=1200,  # 20 min
        notes="Flotation belt, aqua jog"
    ),
    "pool_recovery_circuit": RecoveryDrill(
        name="Pool recovery circuit",
        duration_sec=1500,  # 25 min
        notes="5 exercises x 45s each: pool walk, high knees, side shuffle, cross-over, backwards jog"
    ),
    "cold_water_immersion": RecoveryDrill(
        name="Cold water immersion",
        duration_sec=720,  # 10-12 min
        notes="10-15°C, 2 min in + 1 min out x 3-4 circuits"
    ),
    
    # Bike recovery
    "easy_spin": RecoveryDrill(
        name="Easy spin",
        duration_sec=1200,  # 15-20 min
        notes="Stationary bike, 60-70 RPM, RPE 2-3"
    ),
    "tempo_spin": RecoveryDrill(
        name="Tempo spin",
        duration_sec=1200,  # 20 min
        notes="5 min easy, 10 min at 80 RPM RPE 3-4, 5 min easy cool-down"
    ),
    "bike_intervals": RecoveryDrill(
        name="Intervals (recovery pace)",
        duration_sec=900,  # 15 min
        notes="3 min easy + 1 min moderate x 3-4. RPM 70-90"
    ),
    
    # Mobility recovery
    "general_mobility_flow": RecoveryDrill(
        name="General mobility flow",
        duration_sec=600,  # 10 min
        notes="Deep squat hold, WGS, cat-cow, child's pose. 2 min each"
    ),
    "hip_mobility_recovery": RecoveryDrill(
        name="Hip mobility recovery",
        duration_sec=720,  # 12 min
        notes="90/90 switch, lateral lunge, pigeon, couch stretch. 3 min each side"
    ),
    "tspine_shoulder_recovery": RecoveryDrill(
        name="T-spine & shoulder recovery",
        duration_sec=600,  # 10 min
        notes="Thread needle, foam roller extension, band pull-apart, shoulder CARs"
    ),
    "full_body_mobility_recovery": RecoveryDrill(
        name="Full body mobility recovery",
        duration_sec=900,  # 15 min
        notes="All hip + T-spine/shoulder combined + ankle CARs + neck CARs"
    ),
    
    # Travel recovery
    "travel_walk": RecoveryDrill(
        name="Walk",
        duration_sec=600,  # 10 min
        notes="On arrival walk + hydration + light mobility"
    ),
    "travel_evening_spin": RecoveryDrill(
        name="Easy spin (evening)",
        duration_sec=900,  # 15 min
        notes="Stationary bike easy spin"
    ),
    "travel_evening_circuit": RecoveryDrill(
        name="Recovery circuit (evening)",
        duration_sec=1200,  # 20 min
        notes="General recovery circuit"
    ),
    "travel_morning_activation": RecoveryDrill(
        name="Light activation + mobility",
        duration_sec=900,  # 15 min
        notes="Hip CARs, ankle CARs, cat-cow"
    ),
    
    # Post-match recovery
    "post_match_hydration": RecoveryDrill(
        name="Hydration + carb/protein refuel + light walk",
        duration_sec=900,  # 15 min
        notes="Immediate 0-15 min post"
    ),
    "post_match_compression": RecoveryDrill(
        name="Compression + elevation + light mobility",
        duration_sec=1200,  # 20 min
        notes="Early 15-60 min post"
    ),
    "post_match_later": RecoveryDrill(
        name="Pool or bike + recovery circuit",
        duration_sec=2400,  # 40 min
        notes="Later 2-4 hr post"
    ),
    "post_match_evening": RecoveryDrill(
        name="Lower body recovery + sleep prep",
        duration_sec=1500,  # 25 min
        notes="Evening after meal"
    ),
}

# Recovery Protocols (22 total from FORGE_RECOVERY_LIBRARY_V1.md)
RECOVERY_PROTOCOLS = {
    # L1 - Low fatigue
    "L1_mobility_stretch": RecoveryProtocol(
        id="L1_mobility_stretch",
        name="L1: Mobility + stretch",
        level=1,
        duration_min=10,
        drills=[
            RECOVERY_DRILLS["general_mobility_flow"]
        ],
        when="After standard session"
    ),
    
    # L2 - Moderate fatigue
    "L2_bike_recovery": RecoveryProtocol(
        id="L2_bike_recovery",
        name="L2: Bike recovery",
        level=2,
        duration_min=20,
        drills=[
            RECOVERY_DRILLS["easy_spin"]
        ],
        when="After heavy lifting, speed"
    ),
    "L2_general_circuit": RecoveryProtocol(
        id="L2_general_circuit",
        name="L2: General recovery circuit",
        level=2,
        duration_min=20,
        drills=[
            RECOVERY_DRILLS["foam_roll_quads"],
            RECOVERY_DRILLS["foam_roll_glutes"],
            RECOVERY_DRILLS["glute_bridge"],
            RECOVERY_DRILLS["deep_squat_hold"],
            RECOVERY_DRILLS["worlds_greatest_stretch"],
            RECOVERY_DRILLS["cat_cow"],
            RECOVERY_DRILLS["dead_bug"],
            RECOVERY_DRILLS["childs_pose"]
        ],
        when="After heavy lifting, speed"
    ),
    "L2_lower_body_circuit": RecoveryProtocol(
        id="L2_lower_body_circuit",
        name="L2: Lower body recovery circuit",
        level=2,
        duration_min=20,
        drills=[
            RECOVERY_DRILLS["foam_roll_hamstrings"],
            RECOVERY_DRILLS["foam_roll_quads"],
            RECOVERY_DRILLS["lacrosse_ball_glute"],
            RECOVERY_DRILLS["band_hamstring_stretch"],
            RECOVERY_DRILLS["quad_stretch_lying"],
            RECOVERY_DRILLS["couch_stretch"],
            RECOVERY_DRILLS["adductor_rock"],
            RECOVERY_DRILLS["walk_easy"]
        ],
        when="After heavy lifting, speed"
    ),
    "L2_upper_body_circuit": RecoveryProtocol(
        id="L2_upper_body_circuit",
        name="L2: Upper body recovery circuit",
        level=2,
        duration_min=20,
        drills=[
            RECOVERY_DRILLS["foam_roll_tspine"],
            RECOVERY_DRILLS["lacrosse_ball_shoulder"],
            RECOVERY_DRILLS["band_pull_apart"],
            RECOVERY_DRILLS["pvc_pass_throughs"],
            RECOVERY_DRILLS["shoulder_cars"],
            RECOVERY_DRILLS["neck_cars"],
            RECOVERY_DRILLS["wall_slides"],
            RECOVERY_DRILLS["childs_pose_side_reach"]
        ],
        when="After heavy lifting, speed"
    ),
    
    # L3 - High fatigue
    "L3_pool_walk_jog": RecoveryProtocol(
        id="L3_pool_walk_jog",
        name="L3: Pool walk/jog",
        level=3,
        duration_min=20,
        drills=[
            RECOVERY_DRILLS["pool_walk_jog"]
        ],
        when="After training"
    ),
    "L3_deep_water_running": RecoveryProtocol(
        id="L3_deep_water_running",
        name="L3: Deep water running",
        level=3,
        duration_min=20,
        drills=[
            RECOVERY_DRILLS["deep_water_running"]
        ],
        when="Heavy session, travel"
    ),
    "L3_pool_recovery_circuit": RecoveryProtocol(
        id="L3_pool_recovery_circuit",
        name="L3: Pool recovery circuit",
        level=3,
        duration_min=25,
        drills=[
            RECOVERY_DRILLS["pool_recovery_circuit"]
        ],
        when="Tournament, post-match"
    ),
    "L3_full_body_circuit": RecoveryProtocol(
        id="L3_full_body_circuit",
        name="L3: Full body recovery circuit",
        level=3,
        duration_min=30,
        drills=[
            RECOVERY_DRILLS["foam_roll_full_back"],
            RECOVERY_DRILLS["lacrosse_ball_feet"],
            RECOVERY_DRILLS["hip_cars"],
            RECOVERY_DRILLS["supine_90_90_hamstring"],
            RECOVERY_DRILLS["figure_4_glute"],
            RECOVERY_DRILLS["side_lying_tspine_rotation"],
            RECOVERY_DRILLS["seated_adductor_stretch"],
            RECOVERY_DRILLS["deep_breathing"]
        ],
        when="After match, tournament day"
    ),
    "L3_general_circuit_bike": RecoveryProtocol(
        id="L3_general_circuit_bike",
        name="L3: General circuit + bike",
        level=3,
        duration_min=30,
        drills=[
            RECOVERY_DRILLS["foam_roll_quads"],
            RECOVERY_DRILLS["foam_roll_glutes"],
            RECOVERY_DRILLS["glute_bridge"],
            RECOVERY_DRILLS["deep_squat_hold"],
            RECOVERY_DRILLS["worlds_greatest_stretch"],
            RECOVERY_DRILLS["cat_cow"],
            RECOVERY_DRILLS["dead_bug"],
            RECOVERY_DRILLS["childs_pose"],
            RECOVERY_DRILLS["easy_spin"]
        ],
        when="After match, tournament day"
    ),
    
    # L4 - Very high fatigue
    "L4_full_regeneration": RecoveryProtocol(
        id="L4_full_regeneration",
        name="L4: Full regeneration protocol",
        level=4,
        duration_min=45,
        drills=[
            RECOVERY_DRILLS["cold_water_immersion"],
            RECOVERY_DRILLS["full_body_mobility_recovery"],
            RECOVERY_DRILLS["tempo_spin"]
        ],
        when="Tournament block"
    ),
    "L4_contrast_therapy": RecoveryProtocol(
        id="L4_contrast_therapy",
        name="L4: Contrast therapy + mobility",
        level=4,
        duration_min=45,
        drills=[
            RECOVERY_DRILLS["cold_water_immersion"],  # Simplified - would alternate with hot
            RECOVERY_DRILLS["general_mobility_flow"],
            RECOVERY_DRILLS["easy_spin"]
        ],
        when="Tournament block"
    ),
    "L4_sleep_extension": RecoveryProtocol(
        id="L4_sleep_extension",
        name="L4: Sleep extension + nutrition",
        level=4,
        duration_min=30,  # Active component
        drills=[
            RECOVERY_DRILLS["general_mobility_flow"],
            RECOVERY_DRILLS["post_match_hydration"]  # Using hydration as proxy for nutrition
        ],
        when="Tournament block"
    ),
    
    # L5 - Extreme fatigue
    "L5_rest_day": RecoveryProtocol(
        id="L5_rest_day",
        name="L5: Rest day + recovery modalities",
        level=5,
        duration_min=30,  # Active recovery on rest day
        drills=[
            RECOVERY_DRILLS["general_mobility_flow"],
            RECOVERY_DRILLS["easy_spin"]
        ],
        when="End of tour, heavy block"
    ),
    "L5_cold_immersion": RecoveryProtocol(
        id="L5_cold_immersion",
        name="L5: Cold water immersion + therapy",
        level=5,
        duration_min=30,
        drills=[
            RECOVERY_DRILLS["cold_water_immersion"],
            RECOVERY_DRILLS["general_mobility_flow"]
        ],
        when="End of tour, heavy block"
    ),
}

# Mapping from fatigue level to protocol IDs
FATIGUE_LEVEL_PROTOCOLS = {
    1: ["L1_mobility_stretch"],
    2: ["L2_bike_recovery", "L2_general_circuit", "L2_lower_body_circuit", "L2_upper_body_circuit"],
    3: ["L3_pool_walk_jog", "L3_deep_water_running", "L3_pool_recovery_circuit", "L3_full_body_circuit", "L3_general_circuit_bike"],
    4: ["L4_full_regeneration", "L4_contrast_therapy", "L4_sleep_extension"],
    5: ["L5_rest_day", "L5_cold_immersion"]
}

# Session type to recovery mapping (from Part 7 of the library)
SESSION_TYPE_RECOVERY_MAP = {
    "strength_lower": {
        1: "L1_mobility_stretch",  # MR-02 equivalent
        2: "L2_lower_body_circuit",  # RC-02 + BR-01 equivalent
        3: "L3_general_circuit_bike"  # RC-01 + PR-03 equivalent
    },
    "strength_upper": {
        1: "L1_mobility_stretch",  # MR-03 equivalent
        2: "L2_upper_body_circuit",  # RC-03 + BR-01 equivalent
        3: "L3_general_circuit_bike"  # RC-04 + PR-01 equivalent
    },
    "power": {
        1: "L1_mobility_stretch",  # MR-01 equivalent
        2: "L2_general_circuit",  # RC-01 + BR-01 equivalent
        3: "L3_general_circuit_bike"  # RC-02 + BR-02 equivalent
    },
    "speed": {
        1: "L1_mobility_stretch",  # MR-02 equivalent
        2: "L2_lower_body_circuit",  # RC-02 + BR-01 equivalent
        3: "L3_pool_walk_jog"  # RC-01 + PR-01 equivalent
    },
    "conditioning": {
        1: "L1_mobility_stretch",  # MR-01 equivalent
        2: "L2_general_circuit",  # RC-01 + BR-02 equivalent
        3: "L3_pool_walk_jog"  # Changed from L4 to L3
    },
    "competition": {
        1: "L2_general_circuit",  # RC-01 equivalent
        2: "L3_general_circuit_bike",  # Changed from L4 to L3
        3: "L4_full_regeneration"  # PR-04 + RC-04 + sleep equivalent
    },
    "deload": {
        1: "L1_mobility_stretch",
        2: "L1_mobility_stretch",  # deload stays light
        3: "L2_general_circuit"
    }
}

# Default protocols by fatigue level (used when session type mapping not found)
DEFAULT_PROTOCOLS_BY_LEVEL = {
    1: "L1_mobility_stretch",
    2: "L2_general_circuit",
    3: "L3_full_body_circuit",
    4: "L4_full_regeneration",
    5: "L5_rest_day"
}


def _get_session_type(athlete: AthleteProfile, blueprint_id: int) -> str:
    """Determine session type from athlete and blueprint (matching main.py logic)."""
    goal = athlete.goal
    if goal in ("speed", "conditioning"):
        return "conditioning"
    if blueprint_id == 4 or goal == "power":
        return "power"
    if blueprint_id == 10 or goal == "speed":
        return "speed"
    if athlete.days_to_match == 0:
        return "competition"
    return "strength"


def _get_fatigue_level(athlete: AthleteProfile) -> int:
    """
    Determine fatigue level from athlete profile.
    Simplified mapping: normal -> L1, elevated -> L2, high -> L3, etc.
    """
    fatigue_mapping = {
        "normal": 1,
        "elevated": 2,
        "high": 3,
        "very_high": 4,
        "extreme": 5
    }
    return fatigue_mapping.get(athlete.fatigue_level.lower(), 1)


def select_recovery(athlete: AthleteProfile, session_type: str) -> RecoveryProtocol:
    """
    Select a recovery protocol based on athlete fatigue level and session type.
    
    Args:
        athlete: Athlete profile
        session_type: Type of session (strength, power, speed, conditioning, competition)
        
    Returns:
        RecoveryProtocol matching the athlete's fatigue level and session type
    """
    fatigue_level = _get_fatigue_level(athlete)
    session_type_key = _map_session_type_to_recovery_key(session_type, athlete)
    
    # Try to get protocol from session type mapping
    if session_type_key in SESSION_TYPE_RECOVERY_MAP:
        level_map = SESSION_TYPE_RECOVERY_MAP[session_type_key]
        if fatigue_level in level_map:
            protocol_id = level_map[fatigue_level]
            if protocol_id in RECOVERY_PROTOCOLS:
                return RECOVERY_PROTOCOLS[protocol_id]
    
    # Fallback to default protocol for fatigue level
    default_protocol_id = DEFAULT_PROTOCOLS_BY_LEVEL.get(fatigue_level, "L1_mobility_stretch")
    return RECOVERY_PROTOCOLS.get(default_protocol_id, RECOVERY_PROTOCOLS["L1_mobility_stretch"])


def _map_session_type_to_recovery_key(session_type: str, athlete: AthleteProfile) -> str:
    """
    Map generic session type to specific recovery key based on athlete sport/goals.
    Simplified implementation.
    """
    if session_type == "strength":
        # Default to lower body strength for simplicity
        return "strength_lower"
    elif session_type == "power":
        return "power"
    elif session_type == "speed":
        return "speed"
    elif session_type == "conditioning":
        return "conditioning"
    elif session_type == "competition":
        return "competition"
    elif session_type == "deload":
        return "deload"
    else:
        return "strength_lower"  # Default fallback