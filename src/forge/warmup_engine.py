"""Warmup engine — selects and structures warmups based on session type and athlete level."""

from .models import WarmupDrill, WarmupPhase, WarmupProtocol, AthleteLevel, AthleteProfile


# Warmup Drill Library (106 drills from FORGE_WARMUP_LIBRARY_V1.md)
WARMUP_DRILLS = {
    # Raise Drills (14)
    "R-01": WarmupDrill(
        id="R-01",
        name="Forward jog",
        phase="raise",
        duration_sec=120,  # 2 min
        level="all",
        sport_relevance="All",
        progression="Jog with high knees",
        regression="Walk",
        coaching_cue="Light feet, tall posture"
    ),
    "R-02": WarmupDrill(
        id="R-02",
        name="Backward jog",
        phase="raise",
        duration_sec=60,  # 1 min
        level="all",
        sport_relevance="All",
        progression="Backward skip",
        regression="Backward walk",
        coaching_cue="Stay on balls of feet"
    ),
    "R-03": WarmupDrill(
        id="R-03",
        name="Side shuffle",
        phase="raise",
        duration_sec=60,  # 1 min
        level="all",
        sport_relevance="Court + field",
        progression="Shuffle + touch ground",
        regression="Slow side step",
        coaching_cue="Stick the landing, don't cross feet"
    ),
    "R-04": WarmupDrill(
        id="R-04",
        name="Carioca",
        phase="raise",
        duration_sec=60,  # 1 min
        level="all",
        sport_relevance="All",
        progression="Faster rhythm",
        regression="Slow, exaggerated",
        coaching_cue="Hips face forward, only legs rotate"
    ),
    "R-05": WarmupDrill(
        id="R-05",
        name="Skipping (basic)",
        phase="raise",
        duration_sec=60,  # 1 min
        level="all",
        sport_relevance="All",
        progression="High knees skip",
        regression="March in place",
        coaching_cue="Soft feet, quick ground contact"
    ),
    "R-06": WarmupDrill(
        id="R-06",
        name="Jumping jacks",
        phase="raise",
        duration_sec=30,  # 30s
        level="all",
        sport_relevance="All",
        progression="Cross-jacks",
        regression="Half-jacks",
        coaching_cue="Land soft"
    ),
    "R-07": WarmupDrill(
        id="R-07",
        name="Arm circles (big)",
        phase="raise",
        duration_sec=30,  # 30s
        level="all",
        sport_relevance="Overhead sports",
        progression="With light DB (1-2kg)",
        regression="Without weight",
        coaching_cue="Full circle, touch ears"
    ),
    "R-08": WarmupDrill(
        id="R-08",
        name="Arm circles (reverse)",
        phase="raise",
        duration_sec=30,  # 30s
        level="all",
        sport_relevance="Overhead sports",
        progression="With light DB",
        regression="Without weight",
        coaching_cue="Don't arch back"
    ),
    "R-09": WarmupDrill(
        id="R-09",
        name="Knee hugs (walking)",
        phase="raise",
        duration_sec=30,  # 30s
        level="all",
        sport_relevance="All",
        progression="Faster walk",
        regression="Held 5s each",
        coaching_cue="Pull knee to chest, stay tall"
    ),
    "R-10": WarmupDrill(
        id="R-10",
        name="Quad pulls (walking)",
        phase="raise",
        duration_sec=30,  # 30s
        level="all",
        sport_relevance="All",
        progression="Faster walk",
        regression="Held 5s each",
        coaching_cue="Heel to glute, don't lean forward"
    ),
    "R-11": WarmupDrill(
        id="R-11",
        name="Lunge with twist (walking)",
        phase="raise",
        duration_sec=30,  # 30s
        level="all",
        sport_relevance="Rotational sports",
        progression="Add reach",
        regression="Small twist",
        coaching_cue="Front knee at 90°, rotate through torso"
    ),
    "R-12": WarmupDrill(
        id="R-12",
        name="Ankle hops (in place)",
        phase="raise",
        duration_sec=30,  # 30s
        level="all",
        sport_relevance="All",
        progression="Lateral hops",
        regression="Single direction",
        coaching_cue="Minimal knee bend, spring from ankles"
    ),
    "R-13": WarmupDrill(
        id="R-13",
        name="Bear crawl",
        phase="raise",
        duration_sec=30,  # 30s
        level="all",
        sport_relevance="Contact + field",
        progression="Bear crawl forward/back",
        regression="Knee taps",
        coaching_cue="Flat back, crawl from hips"
    ),
    "R-14": WarmupDrill(
        id="R-14",
        name="Skier swings",
        phase="raise",
        duration_sec=30,  # 30s
        level="all",
        sport_relevance="All",
        progression="Add hop",
        regression="No hop",
        coaching_cue="Weight shifts side to side, soft knees"
    ),

    # Hip Mobility & Activation Drills (18) - simplified for now
    "HM-01": WarmupDrill(
        id="HM-01",
        name="Leg swings (front/back)",
        phase="activate",
        duration_sec=60,  # 30s/leg
        level="all",
        sport_relevance="All",
        progression="Increase ROM",
        regression="Hold support",
        coaching_cue="Swing from hip, not lower back"
    ),
    "HM-02": WarmupDrill(
        id="HM-02",
        name="Leg swings (side/side)",
        phase="activate",
        duration_sec=60,  # 30s/leg
        level="all",
        sport_relevance="All",
        progression="Increase ROM",
        regression="Small range",
        coaching_cue="Keep torso still, only leg moves"
    ),
    "HM-03": WarmupDrill(
        id="HM-03",
        name="World's greatest stretch",
        phase="activate",
        duration_sec=60,  # 30s/side
        level="all",
        sport_relevance="All",
        progression="Pulse at end range",
        regression="Kneeling version",
        coaching_cue="Open chest to ceiling, back knee off ground"
    ),

    # Thoracic Spine & Shoulder Drills (14) - simplified
    "TS-01": WarmupDrill(
        id="TS-01",
        name="Cat-cow",
        phase="activate",
        duration_sec=30,  # 30s
        level="all",
        sport_relevance="All",
        progression="Slow + deep",
        regression="Minimal ROM",
        coaching_cue="Breathe into the movement"
    ),
    "TS-05": WarmupDrill(
        id="TS-05",
        name="Wall slides",
        phase="activate",
        duration_sec=30,  # 10 reps
        level="all",
        sport_relevance="All",
        progression="Add band tension",
        regression="Smaller ROM",
        coaching_cue="Keep wrists and elbows on wall"
    ),
    "TS-06": WarmupDrill(
        id="TS-06",
        name="Band pull-aparts",
        phase="activate",
        duration_sec=30,  # 10-15 reps
        level="all",
        sport_relevance="All",
        progression="Thinner band",
        regression="Wider band",
        coaching_cue="Squeeze shoulder blades, arms straight"
    ),

    # Core Activation Drills (10) - simplified
    "CA-01": WarmupDrill(
        id="CA-01",
        name="Dead bug",
        phase="activate",
        duration_sec=30,  # 6/side
        level="all",
        sport_relevance="All",
        progression="Add band resistance",
        regression="Leg only",
        coaching_cue="Press low back into floor, move opposite limbs"
    ),
    "CA-03": WarmupDrill(
        id="CA-03",
        name="Plank (front)",
        phase="activate",
        duration_sec=60,  # 30-90s
        level="all",
        sport_relevance="All",
        progression="Alternate leg lift",
        regression="Knee-down",
        coaching_cue="Squeeze glutes, pull belly to spine"
    ),

    # Ankle & Foot Drills (8) - simplified
    "AF-01": WarmupDrill(
        id="AF-01",
        name="Ankle circles",
        phase="activate",
        duration_sec=60,  # 30s each direction/ankle
        level="all",
        sport_relevance="All",
        progression="Full circle",
        regression="Small circle",
        coaching_cue="Move only ankle, keep leg still"
    ),

    # Neck & Cervical Drills (6) - simplified
    "NC-01": WarmupDrill(
        id="NC-01",
        name="Chin tucks",
        phase="activate",
        duration_sec=30,  # 10 reps
        level="all",
        sport_relevance="All",
        progression="Hold 5s at end",
        regression="",
        coaching_cue="Make a double chin, lengthen back of neck"
    ),

    # Activation Drills — Glutes (8) - simplified
    "GA-01": WarmupDrill(
        id="GA-01",
        name="Glute bridge (double)",
        phase="activate",
        duration_sec=30,  # 15 reps
        level="all",
        sport_relevance="All",
        progression="Single leg",
        regression="Bridges",
        coaching_cue="Squeeze glutes at top, 2s hold"
    ),
    "GA-08": WarmupDrill(
        id="GA-08",
        name="Lateral band walk",
        phase="activate",
        duration_sec=60,  # 10 steps each way
        level="all",
        sport_relevance="All",
        progression="Band below knees",
        regression="No band",
        coaching_cue="Stay in athletic stance, toes forward"
    ),

    # Activation Drills — Hamstrings (4) - simplified
    "HA-01": WarmupDrill(
        id="HA-01",
        name="Nordic curl (eccentric)",
        phase="activate",
        duration_sec=30,  # 4-6 reps
        level="all",
        sport_relevance="All",
        progression="Full ROM",
        regression="",
        coaching_cue="Lower slowly, control descent, catch with hands"
    ),

    # Potentiation Drills (10) - simplified
    "P-01": WarmupDrill(
        id="P-01",
        name="Box jump (build-up)",
        phase="potentiate",
        duration_sec=60,  # 3 × 3
        level="all",
        sport_relevance="All",
        progression="Higher box",
        regression="",
        coaching_cue="Land soft, stick each rep"
    ),
    "P-05": WarmupDrill(
        id="P-05",
        name="Band-resisted sprint starts",
        phase="potentiate",
        duration_sec=60,  # 3 × 10m
        level="all",
        sport_relevance="All",
        progression="Longer distance",
        regression="",
        coaching_cue="Drive hard for 5 steps"
    ),
    "P-06": WarmupDrill(
        id="P-06",
        name="Build-up sprint (60-80%)",
        phase="potentiate",
        duration_sec=60,  # 3 × 20m
        level="all",
        sport_relevance="All",
        progression="Full speed",
        regression="",
        coaching_cue="Progressive acceleration, tall posture"
    ),
    "P-08": WarmupDrill(
        id="P-08",
        name="Sub-max bench (50-60%)",
        phase="potentiate",
        duration_sec=60,  # 3 × 5
        level="all",
        sport_relevance="All",
        progression="Increase weight",
        regression="",
        coaching_cue="Explosive concentric, controlled descent"
    ),
    "P-09": WarmupDrill(
        id="P-09",
        name="Sub-max squat (50-60%)",
        phase="potentiate",
        duration_sec=60,  # 3 × 5
        level="all",
        sport_relevance="All",
        progression="Increase weight",
        regression="",
        coaching_cue="Stand fast, controlled descent"
    ),
    "P-10": WarmupDrill(
        id="P-10",
        name="Skips for height",
        phase="potentiate",
        duration_sec=60,  # 3 × 20m
        level="all",
        sport_relevance="All",
        progression="Single-leg bounding",
        regression="",
        coaching_cue="Max height, minimal ground contact"
    ),

    # Sport-Specific Drills (14) - simplified
    "SS-11": WarmupDrill(
        id="SS-11",
        name="Box breathing + heart rate prep",
        phase="prepare",
        duration_sec=60,  # 1 min
        level="all",
        sport_relevance="All",
        progression="",
        regression="",
        coaching_cue="Competition readiness"
    ),
    "SS-12": WarmupDrill(
        id="SS-12",
        name="Sport-specific acceleration start",
        phase="prepare",
        duration_sec=60,  # 4 × 10m
        level="all",
        sport_relevance="All",
        progression="",
        regression="",
        coaching_cue="Sport-specific first-step direction"
    ),
    "SS-14": WarmupDrill(
        id="SS-14",
        name="Visualisation + movement",
        phase="prepare",
        duration_sec=60,  # 1 min
        level="all",
        sport_relevance="All",
        progression="",
        regression="",
        coaching_cue="Motor imagery paired with movement"
    ),
    # Missing referenced drills
    "HM-06": WarmupDrill(
        id="HM-06",
        name="Fire hydrant circles",
        phase="activate",
        duration_sec=30,  # 10 each way/leg
        level="all",
        sport_relevance="All",
        progression="Add ankle weight",
        regression="Smaller circle",
        coaching_cue="Don't lean to support side"
    ),
    "HM-10": WarmupDrill(
        id="HM-10",
        name="Lateral band walk",
        phase="activate",
        duration_sec=60,  # 10 steps each way
        level="all",
        sport_relevance="All",
        progression="Band below knees",
        regression="No band",
        coaching_cue="Stay in athletic stance, toes forward"
    ),
    "HM-11": WarmupDrill(
        id="HM-11",
        name="Cossack squat",
        phase="activate",
        duration_sec=60,  # 30s/side
        level="all",
        sport_relevance="All",
        progression="Deeper squat, hands overhead",
        regression="Shallow squat, hold support",
        coaching_cue="Shift weight fully to bent leg, keep heel down"
    ),
    "HM-12": WarmupDrill(
        id="HM-12",
        name="Lateral lunge",
        phase="activate",
        duration_sec=60,  # 30s/side
        level="all",
        sport_relevance="All",
        progression="Add reach to grounded foot",
        regression="Smaller step, hold support",
        coaching_cue="Push hips back, lead with hips not knees"
    ),
    "HM-13": WarmupDrill(
        id="HM-13",
        name="Half-kneeling hip flexor stretch",
        phase="activate",
        duration_sec=60,  # 30s/side
        level="all",
        sport_relevance="All",
        progression="Add overhead reach to same side",
        regression="Hands on front knee, smaller lean",
        coaching_cue="Squeeze glute of back leg, drive hips forward"
    ),
    # New thoracic / shoulder drills
    "TS-08": WarmupDrill(
        id="TS-08",
        name="Quadruped T-spine rotation",
        phase="activate",
        duration_sec=60,  # 30s/side
        level="all",
        sport_relevance="All",
        progression="Reach hand behind head",
        regression="Smaller rotation arc",
        coaching_cue="Rotate through mid-back, keep hips square"
    ),
    "TS-09": WarmupDrill(
        id="TS-09",
        name="Band YTWs",
        phase="activate",
        duration_sec=60,  # 5 reps each shape
        level="all",
        sport_relevance="Overhead sports",
        progression="Thinner band, slower tempo",
        regression="No band, bodyweight only",
        coaching_cue="Squeeze shoulder blades, keep ribs down"
    ),
    "TS-10": WarmupDrill(
        id="TS-10",
        name="Band shoulder external rotation",
        phase="activate",
        duration_sec=60,  # 10/side
        level="all",
        sport_relevance="Overhead sports",
        progression="Heavier band",
        regression="Lighter band, smaller ROM",
        coaching_cue="Elbow pinned to ribs, rotate from shoulder"
    ),
    # New potentiation drills
    "P-11": WarmupDrill(
        id="P-11",
        name="Pogo jumps",
        phase="potentiate",
        duration_sec=30,  # 3 × 10
        level="all",
        sport_relevance="All",
        progression="Higher, faster rebound",
        regression="Smaller hops, no height",
        coaching_cue="Minimal knee bend, stiff ankles, quick ground contact"
    ),
    "P-12": WarmupDrill(
        id="P-12",
        name="Straight-leg bound",
        phase="potentiate",
        duration_sec=30,  # 3 × 20m
        level="all",
        sport_relevance="Speed sports",
        progression="Increase distance per bound",
        regression="Straight-leg march (SLM-07)",
        coaching_cue="Keep leg straight, paw back, tall posture"
    ),
    "TS-03": WarmupDrill(
        id="TS-03",
        name="Half-kneeling T-spine rotation",
        phase="activate",
        duration_sec=30,  # 30s/side
        level="all",
        sport_relevance="All",
        progression="Reach overhead",
        regression="No weight",
        coaching_cue="Rotate toward front leg, reach behind"
    ),
    "TS-07": WarmupDrill(
        id="TS-07",
        name="Pass-through (PVC)",
        phase="activate",
        duration_sec=30,  # 10 reps
        level="all",
        sport_relevance="All",
        progression="Narrower grip",
        regression="Wider grip",
        coaching_cue="Keep arms straight, go overhead and back"
    ),
    "AF-07": WarmupDrill(
        id="AF-07",
        name="Single-leg balance (eyes open)",
        phase="activate",
        duration_sec=30,  # 30s/leg
        level="all",
        sport_relevance="All",
        progression="Eyes closed, unstable surface",
        regression="Touch support",
        coaching_cue="Focus on a spot, feel foot tripod"
    ),
    "SS-01": WarmupDrill(
        id="SS-01",
        name="Shadow batting",
        phase="potentiate",
        duration_sec=120,  # 2 min
        level="all",
        sport_relevance="Cricket",
        progression="With bat",
        regression="Without bat",
        coaching_cue="Rotational preparation, hip to shoulder separation"
    ),
    "SS-03": WarmupDrill(
        id="SS-03",
        name="Rugby lineout jumps",
        phase="potentiate",
        duration_sec=60,  # 5 jumps
        level="all",
        sport_relevance="Rugby",
        progression="With contact",
        regression="Lower height",
        coaching_cue="Hip extension, timing, overhead catch"
    ),
    "P-03": WarmupDrill(
        id="P-03",
        name="Med ball slam",
        phase="potentiate",
        duration_sec=60,  # 5 × 3
        level="all",
        sport_relevance="All",
        progression="Heavier ball",
        regression="Lighter ball",
        coaching_cue="Full-body extension into slam"
    ),
    # Sprint mechanics drills
    "SM-01": WarmupDrill(
        id="SM-01",
        name="A-March",
        phase="activate",
        duration_sec=60,  # 2 × 20m
        level="all",
        sport_relevance="Speed sports",
        progression="Faster rhythm",
        regression="Slow march",
        coaching_cue="High knee drive, opposite arm action"
    ),
    "SM-02": WarmupDrill(
        id="SM-02",
        name="A-Skip",
        phase="activate",
        duration_sec=60,  # 2 × 20m
        level="all",
        sport_relevance="Speed sports",
        progression="Add speed",
        regression="A-March",
        coaching_cue="Quick ground contact, tall posture"
    ),
    "SM-03": WarmupDrill(
        id="SM-03",
        name="B-Skip",
        phase="activate",
        duration_sec=60,  # 2 × 20m
        level="all",
        sport_relevance="Speed sports",
        progression="Add speed",
        regression="A-Skip",
        coaching_cue="Extend leg, paw back aggressively"
    ),
    "SM-04": WarmupDrill(
        id="SM-04",
        name="Wall Drill March",
        phase="activate",
        duration_sec=30,  # 3 × 5s
        level="all",
        sport_relevance="Speed sports",
        progression="Switches",
        regression="Lean only",
        coaching_cue="45° lean, drive knee up, toe up"
    ),
    "SM-05": WarmupDrill(
        id="SM-05",
        name="Wall Drill Switch",
        phase="activate",
        duration_sec=30,  # 3 × 5s
        level="all",
        sport_relevance="Speed sports",
        progression="Faster switches",
        regression="Wall Drill March",
        coaching_cue="Quick exchange, maintain posture"
    ),
    "SM-06": WarmupDrill(
        id="SM-06",
        name="Ankling",
        phase="raise",
        duration_sec=30,  # 2 × 20m
        level="all",
        sport_relevance="Speed sports",
        progression="Faster",
        regression="Slow",
        coaching_cue="Minimal knee bend, ankle stiffness"
    ),
    "SM-07": WarmupDrill(
        id="SM-07",
        name="Straight Leg March",
        phase="activate",
        duration_sec=30,  # 2 × 20m
        level="all",
        sport_relevance="Speed sports",
        progression="Add speed",
        regression="Slow",
        coaching_cue="Lock knee, snap down from hip"
    ),
    # Court drills
    "CT-01": WarmupDrill(
        id="CT-01",
        name="Split-step prep",
        phase="activate",
        duration_sec=30,  # 3 × 10
        level="all",
        sport_relevance="Court sports",
        progression="Reactive",
        regression="Slow",
        coaching_cue="Load hips, light jump, land soft"
    ),
    "CT-02": WarmupDrill(
        id="CT-02",
        name="Reactive shuffle",
        phase="activate",
        duration_sec=30,  # 3 × 10m
        level="all",
        sport_relevance="Court sports",
        progression="Coach cue direction",
        regression="Pre-planned",
        coaching_cue="Low stance, quick feet, react to signal"
    ),
    "CT-03": WarmupDrill(
        id="CT-03",
        name="Lateral shuffle (dynamic)",
        phase="raise",
        duration_sec=30,  # 2 × 20m
        level="all",
        sport_relevance="Court sports",
        progression="Add touch",
        regression="Slow",
        coaching_cue="Stay low, don't cross feet"
    ),
    "CT-04": WarmupDrill(
        id="CT-04",
        name="Crossover run",
        phase="raise",
        duration_sec=30,  # 2 × 20m
        level="all",
        sport_relevance="Court sports",
        progression="Faster",
        regression="Slow",
        coaching_cue="Rotate hips, drive across body"
    ),
    "CT-05": WarmupDrill(
        id="CT-05",
        name="Lunge-recover pattern",
        phase="activate",
        duration_sec=30,  # 3 × 5 each side
        level="all",
        sport_relevance="Court sports",
        progression="Add speed",
        regression="Slow",
        coaching_cue="Push off front foot, recover to stance"
    ),
    "CT-06": WarmupDrill(
        id="CT-06",
        name="Decel/re-accel footwork",
        phase="potentiate",
        duration_sec=30,  # 3 × 10m decel + 10m accel
        level="all",
        sport_relevance="Court sports",
        progression="Reactive",
        regression="Pre-planned",
        coaching_cue="Short steps to decel, explode out"
    ),
    # Additional sport-specific overhead drills
    "SS-02": WarmupDrill(
        id="SS-02",
        name="Bowling run-up rehearsals",
        phase="potentiate",
        duration_sec=60,  # 3 × 10m
        level="all",
        sport_relevance="Cricket",
        progression="Full run-up",
        regression="Short run-up",
        coaching_cue="Loading hip, counter-rotation"
    ),
    "SS-05": WarmupDrill(
        id="SS-05",
        name="Shadow groundstrokes",
        phase="potentiate",
        duration_sec=120,  # 2 min
        level="all",
        sport_relevance="Tennis",
        progression="With racket",
        regression="Without racket",
        coaching_cue="Multi-directional movement, rotation"
    ),
    "SS-06": WarmupDrill(
        id="SS-06",
        name="Serve prep (band)",
        phase="potentiate",
        duration_sec=60,  # 10/side
        level="all",
        sport_relevance="Tennis",
        progression="Heavier band",
        regression="Lighter band",
        coaching_cue="Shoulder external rotation + hip drive"
    ),
    "SS-07": WarmupDrill(
        id="SS-07",
        name="Shadow net play",
        phase="potentiate",
        duration_sec=120,  # 2 min
        level="all",
        sport_relevance="Badminton",
        progression="With racket",
        regression="Without racket",
        coaching_cue="Deep lunges, rapid recovery"
    ),
    "SS-08": WarmupDrill(
        id="SS-08",
        name="Shadow overhead clears",
        phase="potentiate",
        duration_sec=60,  # 10/side
        level="all",
        sport_relevance="Badminton",
        progression="With racket",
        regression="Without racket",
        coaching_cue="Scapular retraction, hip hinge"
    ),
}

# Phase-ordered warmup templates per session type
SESSION_WARMUP_TEMPLATES = {
    "strength": {
        "raise": ["R-01", "R-05"],
        "activate": ["HM-03", "GA-01", "TS-09", "TS-07", "CA-01", "HM-11"],
        "potentiate": ["P-08", "P-09"],
        "prepare": [],
    },
    "strength_lower": {
        "raise": ["R-01", "R-12"],
        "activate": ["HM-03", "HM-01", "GA-01", "CA-01", "HM-11", "HM-12"],
        "potentiate": ["P-09"],
        "prepare": [],
    },
    "strength_upper": {
        "raise": ["R-01", "R-05", "R-07"],
        "activate": ["TS-07", "TS-05", "TS-06", "TS-09", "TS-10", "CA-01"],
        "potentiate": ["P-08"],
        "prepare": [],
    },
    "power": {
        "raise": ["R-01", "R-05"],
        "activate": ["HM-01", "HM-03", "GA-01", "TS-07"],
        "potentiate": ["P-11", "P-01", "P-05"],
        "prepare": [],
    },
    "speed": {
        "raise": ["R-01", "R-02", "R-03", "R-04"],
        "activate": ["HM-01", "HM-02", "HM-03", "HM-10", "GA-08", "SM-01", "SM-02", "SM-03", "SM-04", "SM-05", "SM-06", "SM-07"],
        "potentiate": ["P-06", "P-10", "P-12"],
        "prepare": [],
    },
    "conditioning": {
        "raise": ["R-01", "R-05"],
        "activate": ["HM-03", "GA-01", "CA-01", "HM-11"],
        "potentiate": ["P-11", "P-06"],
        "prepare": [],
    },
    "competition": {
        "raise": ["R-01", "R-03", "R-05", "R-14"],
        "activate": ["HM-03", "HM-10", "TS-03", "GA-08", "CA-01"],
        "potentiate": ["P-01", "P-03", "P-06"],
        "prepare": ["SS-14", "SS-11"],
    },
    "youth": {
        "raise": ["R-01", "R-05", "R-14"],
        "activate": ["HM-03", "GA-01", "CA-01", "AF-01"],
        "potentiate": ["P-10", "P-01"],
        "prepare": [],
    },
    "return_to_play": {
        "raise": ["R-01"],
        "activate": ["HM-03", "CA-01", "AF-07", "NC-01"],
        "potentiate": [],
        "prepare": [],
    },
    "deload": {
        "raise": ["R-01", "R-05"],
        "activate": ["HM-03", "GA-01", "CA-01"],
        "potentiate": [],
        "prepare": [],
    },
    "court_speed": {
        "raise": ["R-01", "R-03", "R-04", "CT-03", "CT-04"],
        "activate": ["HM-01", "HM-02", "HM-03", "CT-01", "CT-02", "CT-05", "CT-06"],
        "potentiate": ["P-06", "P-10"],
        "prepare": [],
    },
    "court_strength": {
        "raise": ["R-01", "CT-03", "CT-04"],
        "activate": ["HM-03", "HM-01", "CT-01", "CT-02", "CT-05", "GA-01", "CA-01", "TS-07"],
        "potentiate": ["P-09"],
        "prepare": [],
    },
}

# Sport-specific warmup templates (used for competition + sport-specific prep)
SPORT_WARMUP_TEMPLATES = {
    "tennis": {
        "raise": ["R-01", "R-03", "R-05"],
        "activate": ["HM-03", "TS-03", "HM-10", "GA-08", "CA-01", "CT-01", "CT-02", "CT-05"],
        "potentiate": ["P-01", "P-06", "P-10"],
        "prepare": ["SS-05", "SS-06", "SS-11"],
    },
    "cricket": {
        "raise": ["R-01", "R-03", "R-05", "R-14"],
        "activate": ["HM-03", "HM-10", "GA-01", "CA-01", "TS-03"],
        "potentiate": ["P-01", "P-06"],
        "prepare": ["SS-01", "SS-02", "SS-11"],
    },
}

# Session type to warmup mapping (flat — backward compat)
SESSION_TYPE_WARMUPS = {k: sum(v.values(), []) for k, v in SESSION_WARMUP_TEMPLATES.items()}
# Add sport-specific flat entries too
for sport, template in SPORT_WARMUP_TEMPLATES.items():
    SESSION_TYPE_WARMUPS[f"sport_{sport}"] = sum(template.values(), [])

# Environment-specific drill pools (additive: each env includes appropriate drills)
# Gym: general + upper body + core drills. Excludes drills needing 15m+ run space.
# Ground (field): all general + sprint mechanics + sport-specific. Includes everything.
# Court: general + court-specific + sprint mechanics (court sports need acceleration prep).
#         Excludes field-sport-specific drills (cricket bowling run-ups etc).
_ENV_EXCLUDE_GYM = {"SS-01", "SS-02", "SS-03", "SS-05", "SS-06", "SS-07", "SS-08",
                     "SM-01", "SM-02", "SM-03", "SM-04", "SM-05", "SM-06", "SM-07",
                     "CT-01", "CT-02", "CT-03", "CT-04", "CT-05", "CT-06",
                     "P-05", "P-06", "P-10", "P-12"}
_ENV_EXCLUDE_COURT = {"SS-01", "SS-02", "SS-03", "R-02"}  # field-specific prep

ENVIRONMENT_DRILLS = {
    "gym": [did for did in WARMUP_DRILLS if did not in _ENV_EXCLUDE_GYM],
    "ground": list(WARMUP_DRILLS.keys()),  # all drills available on ground/field
    "court": [did for did in WARMUP_DRILLS if did not in _ENV_EXCLUDE_COURT],
}


def _get_session_type(athlete: AthleteProfile, blueprint_id: int) -> str:
    """Determine session type from athlete and blueprint."""
    goal = athlete.goal
    if goal in ("speed", "conditioning"):
        return "conditioning"
    if blueprint_id == 4 or goal == "power":
        return "power"
    if blueprint_id == 10 or goal == "speed":
        return "speed"
    if athlete.days_to_match == 0:
        return "competition"
    if blueprint_id == 13 or goal == "deload":
        return "deload"
    return "strength"


def audit_ramp_phases() -> dict:
    phase_counts = {"raise": 0, "activate": 0, "potentiate": 0, "prepare": 0}
    unassigned = []
    for did, drill in WARMUP_DRILLS.items():
        if drill.phase in phase_counts:
            phase_counts[drill.phase] += 1
        else:
            unassigned.append(did)
    return {
        "phase_counts": phase_counts,
        "unassigned": unassigned,
        "total_drills": len(WARMUP_DRILLS),
        "phases_present": [p for p, c in phase_counts.items() if c > 0],
    }


# Sport-specific preparation drills for competition warmups
SPORT_PREP_DRILLS = {
    "cricket": ["SS-01", "SS-02"],
    "tennis": ["SS-05", "SS-06"],
    "badminton": ["SS-07", "SS-08"],
    "basketball": ["P-01", "SS-14"],
    "volleyball": ["P-01", "SS-14"],
    "rugby": ["SS-03"],
    "soccer": ["P-06", "SS-14"],
    "hockey": ["P-06", "SS-14"],
    "squash": ["SS-07", "SS-14"],
}


def _normalize_drill_phase(drill_id: str, current_phase: str) -> str:
    """Normalize a drill's phase to a standard RAMP phase."""
    if current_phase in ("raise", "activate", "potentiate", "prepare"):
        return current_phase
    prefix_map = {
        "R": "raise", "HM": "activate", "GA": "activate", "TS": "activate",
        "CA": "activate", "NC": "activate", "AF": "activate", "CT": "activate",
        "SM": "activate", "P": "potentiate", "SS": "prepare",
    }
    prefix = drill_id.split("-")[0]
    return prefix_map.get(prefix, "raise")


def select_warmup(athlete: AthleteProfile, session_type: str, environment: str = "gym") -> WarmupProtocol:
    """
    Select and structure a warmup based on athlete profile and session type.
    
    Args:
        athlete: Athlete profile
        session_type: Type of session (strength, power, speed, conditioning, competition, youth, return_to_play)
        environment: Training environment (gym, ground, court)
        
    Returns:
        WarmupProtocol with phases and drills
    """
    sport = athlete.sport.lower().strip()
    
    # Phase-ordered template lookup
    template = None
    if session_type == "competition" and sport in SPORT_WARMUP_TEMPLATES:
        template = SPORT_WARMUP_TEMPLATES[sport]
    if template is None:
        template = SESSION_WARMUP_TEMPLATES.get(session_type, SESSION_WARMUP_TEMPLATES["strength"])
    
    drill_ids = sum(template.values(), [])
    
    # Sport-aware substitution for competition warmup (fallback for non-sport-specific sports)
    if session_type == "competition" and sport not in SPORT_WARMUP_TEMPLATES:
        sport_prep = SPORT_PREP_DRILLS.get(sport, [])
        if sport_prep:
            drill_ids = [did for did in drill_ids if did not in {"SS-14", "SS-11"}]
            for did in sport_prep:
                if did not in drill_ids:
                    drill_ids.append(did)
    
    # Filter by environment if available
    if environment in ENVIRONMENT_DRILLS:
        env_drills = ENVIRONMENT_DRILLS[environment]
        drill_ids = [did for did in drill_ids if did in env_drills]
    
    # Get actual drill objects
    drills = [WARMUP_DRILLS[drill_id] for drill_id in drill_ids if drill_id in WARMUP_DRILLS]
    
    # Build reverse map: drill_id -> phase from template (source of truth)
    drill_to_phase = {}
    for pname, pids in template.items():
        for did in pids:
            drill_to_phase[did] = pname
    
    # Group by phase using template assignment
    phases_dict = {}
    for drill in drills:
        phase = drill_to_phase.get(drill.id, drill.phase)
        if phase not in phases_dict:
            phases_dict[phase] = []
        phases_dict[phase].append(drill)
    
    # Create WarmupPhase objects in template phase order
    phases = []
    total_duration_sec = 0
    phase_order = ["raise", "activate", "potentiate", "prepare"]
    
    for phase_name in phase_order:
        if phase_name in phases_dict:
            phase_drills = phases_dict[phase_name]
            phase_duration = sum(drill.duration_sec for drill in phase_drills)
            phases.append(WarmupPhase(
                name=phase_name.capitalize(),
                drills=phase_drills,
                duration_sec=phase_duration
            ))
            total_duration_sec += phase_duration
    
    return WarmupProtocol(
        phases=phases,
        total_duration_sec=total_duration_sec
    )