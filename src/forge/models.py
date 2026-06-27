from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import re


class FamilyCode(str, Enum):
    DLKD = "DLKD"
    DLHD = "DLHD"
    SLKD = "SLKD"
    SLHD = "SLHD"
    HPUSH = "HPush"
    HPULL = "HPull"
    VPUSH = "VPush"
    VPULL = "VPull"
    PLYO = "Plyo"
    BALL = "Ball"
    SPRINT = "Sprint"
    LANDING = "Landing"
    ROT = "Rot"
    CARRY = "Carry"
    CORE = "Core"
    ACC = "Acc"
    AGILITY = "Agility"
    COND = "Cond"
    VOLLEYBALL = "Volleyball"
    TENNIS = "Tennis"
    SOCCER = "Soccer"
    DECELERATION = "Deceleration"


class Objective(str, Enum):
    STRENGTH = "STR"
    POWER = "POW"
    HYPERTROPHY = "HYP"
    CONDITIONING = "COND"
    MOBILITY = "MOB"
    STABILITY = "STAB"


class PrescriptionRole(str, Enum):
    MAIN_STRENGTH = "main_strength"
    SECONDARY_STRENGTH = "secondary_strength"
    HYPERTROPHY_ACCESSORY = "hypertrophy_accessory"
    EXPLOSIVE_POWER = "explosive_power"
    PLYOMETRIC = "plyometric"
    SPRINT_MECHANICS = "sprint_mechanics"
    CORE_STABILITY = "core_stability"
    CARRY_CAPACITY = "carry_capacity"
    LANDING_MECHANICS = "landing_mechanics"
    REHAB_PREHAB = "rehab_prehab"
    CONDITIONING_LIFT = "conditioning_lift"


@dataclass
class Prescription:
    sets: str = ""
    reps: str = ""
    loading_method: str = ""
    intensity_note: str = ""
    progression_method: str = ""
    rest_seconds: int = 60


COMP_WINDOW_LABELS: dict[int, str] = {
    6: "FULL",
    4: "MODERATE",
    2: "LIGHT",
    1: "PRIMER",
}


class AthleteLevel(str, Enum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"


class EquipmentProfile(str, Enum):
    FIELD_ONLY = "Field Only"
    BASIC_GYM = "Basic Gym"
    COMMERCIAL_GYM = "Commercial Gym"
    ELITE_FACILITY = "Elite Facility"


class SeasonPhase(str, Enum):
    OFF_SEASON = "off_season"
    PRE_SEASON = "pre_season"
    IN_SEASON = "in_season"
    TRANSITION = "transition"


class BlueprintName(str, Enum):
    FULL_BODY_STRENGTH = "Full Body Strength"
    STRENGTH_POWER = "Strength + Power"
    STRENGTH_CONDITIONING = "Strength + Conditioning"
    POWER_SPEED = "Power + Speed"
    UPPER_LOWER_SPLIT = "Upper / Lower Split"
    POWER_MAINTENANCE = "Power Maintenance"
    YOUTH_FOUNDATION = "Youth Foundation (U14-U20)"
    COURT_SPORT_AD = "Court Sport Athletic Development"
    RUGBY_OFF_SEASON = "Rugby Off-Season"
    SPRINT_DEVELOPMENT = "Sprint Development"
    HYPERTROPHY = "Hypertrophy / Mass Accrual"
    RETURN_TO_SPORT = "Return to Sport (Foundation)"
    DELOAD = "Deload / Active Recovery"
    MIXED_MODAL = "Mixed Modal (GPP)"


@dataclass
class Exercise:
    id: str
    name: str
    family: FamilyCode
    secondary_family: Optional[FamilyCode]
    objective: Objective
    difficulty: int
    equipment: list[str]
    unilateral: bool
    explosive: bool
    isometric: bool
    rotational: bool
    progression: Optional[str]
    regression: Optional[str]
    surface: str = "stable"
    fatigue_cost: int = 3
    impact_level: int = 3
    eccentric_cost: int = 3
    competition_role: str = "strength"


OBJECTIVE_REST_MAP: dict[str, str] = {
    "STR": "3-5min",
    "POW": "3-5min",
    "HYP": "60-90s",
    "COND": "30-60s",
    "MOB": "30-60s",
    "STAB": "60-90s",
}


OBJECTIVE_INTENSITY_MAP: dict[str, str] = {
    "STR": "heavy",
    "POW": "explosive",
    "HYP": "moderate",
    "COND": "light",
    "MOB": "light",
    "STAB": "light",
}


@dataclass
class ExerciseFamily:
    id: FamilyCode
    name: str
    definition: str
    non_negotiable_in: str
    default_slot: str
    selection_priorities: list[tuple[int, str, str]]


@dataclass
class Blueprint:
    id: int
    name: BlueprintName
    purpose: str
    typical_athlete: str
    best_training_age: str
    best_season_phase: list[SeasonPhase]
    best_frequency: str = ""  # DEPRECATED — coach owns frequency via athlete.frequency_per_week
    contraindications: str = ""
    typical_outcomes: str = ""
    progression_path: Optional[BlueprintName] = None
    regression_path: Optional[BlueprintName] = None
    mandatory_families: list[FamilyCode] = field(default_factory=list)
    optional_families: list[FamilyCode] = field(default_factory=list)
    slot_order: list[FamilyCode] = field(default_factory=list)
    typical_duration: str = ""  # DEPRECATED — coach owns duration via athlete.program_length_weeks
    min_session_composition: list[dict] = field(default_factory=list)


@dataclass
class ConditioningProtocol:
    id: str
    name: str
    objective: str
    system: str
    level: str
    environment: list[str]
    duration: str
    work_description: str
    rest: str
    sets: str
    total_volume: str
    fatigue_score: int
    progression: str
    regression: str
    tier: str
    work_rest_ratio: Optional[str] = None
    level_variants: dict[int, dict] = field(default_factory=dict)
    environment_category: str = "field"
    sport_tags: list[str] = field(default_factory=lambda: ["any"])
    movement_profile: str = "linear_tempo"
    session_role: str = "main_conditioning"
    fatigue_cost: int = 3
    impact_level: int = 3
    eccentric_cost: int = 3


@dataclass
class SessionBlock:
    family: FamilyCode
    family_name: str
    exercises: list[Exercise] = field(default_factory=list)
    target_intensity: str = "moderate"
    rest_period: str = "60-90s"
    prescription: Optional[Prescription] = None


@dataclass
class Session:
    blocks: list[SessionBlock]
    conditioning: Optional[ConditioningProtocol] = None
    total_duration_min: int = 0
    load_capped: bool = False
    week_type: str = ""
    testing_categories: list[str] = field(default_factory=list)
    adjustment_note: str = ""


@dataclass
class CoachPreferences:
    preferred_deadlift: Optional[str] = None
    preferred_squat: Optional[str] = None
    preferred_press: Optional[str] = None
    avoid_olympic_lifts: bool = False
    avoid_high_soreness_near_match: bool = False
    min_sprint_exposures_per_week: int = 1
    preferred_conditioning_style: str = "mixed"
    bias_unilateral_work: bool = False
    prefer_velocity_based_loading: bool = False
    preferred_tempo: str = "20X0"
    preferred_rest_seconds: int = 90


@dataclass
class AthleteProfile:
    sport: str
    training_age_years: float
    season_phase: SeasonPhase
    goal: str
    equipment_profile: EquipmentProfile
    athlete_level: AthleteLevel
    technique_consistency: float = 1.0
    injury_status: str = "none"
    injury_history: list[str] = field(default_factory=list)
    fatigue_level: str = "normal"
    weeks_since_break: int = 0
    recent_exercises: dict[str, dict] = field(default_factory=dict)
    available_minutes: int = 60
    days_to_match: Optional[int] = None
    preferred_families: int = 6
    age: int = 18
    strength_base_met: bool = True

    # Wave 5 — Anthropometry
    bodyweight_kg: Optional[float] = None
    position_role: str = ""
    role: str = ""  # e.g. "Pace Bowler", "Tighthead Prop"

    # Wave 5 — Performance profile flags (force_deficient / velocity_deficient / balanced)
    force_profile: Optional[str] = None
    # (poor / average / strong)
    elastic_profile: Optional[str] = None
    conditioning_profile: Optional[str] = None
    landing_competency: Optional[str] = None
    sprint_mechanics_competency: Optional[str] = None

    # Wave 5 — Risk / tolerance flags
    lumbar_risk: bool = False
    patellar_tendon_risk: bool = False
    hamstring_risk: bool = False
    shoulder_overhead_risk: bool = False
    groin_adductor_risk: bool = False
    ankle_foot_risk: bool = False

    # Wave 5 — Optional test-derived tags (low / avg / high)
    cmj_band: Optional[str] = None
    sprint_10m_band: Optional[str] = None
    squat_strength_band: Optional[str] = None
    aerobic_band: Optional[str] = None

    # Wave 15 — Raw test scores for test-driven adjustments
    yoyo_ir1: Optional[float] = None
    yoyo_ir2: Optional[float] = None
    bronco: Optional[float] = None
    cmj: Optional[float] = None
    testing_date: Optional[str] = None
    test_adjustments: Optional[dict] = None

    # Wave 7 — Optional prior-block tracking
    prior_program: Optional[object] = None
    prior_profile_snapshot: Optional[object] = None
    block_response: Optional[object] = None

    # Wave 12 — Calendar-aware session placement
    match_day: int = 5  # Saturday (0=Mon, 6=Sun)
    team_training_days: list[int] = field(default_factory=lambda: [0, 2, 4])  # Mon, Wed, Fri
    heavy_field_days: list[int] = field(default_factory=lambda: [1, 3])  # Tue, Thu
    travel_days: list[int] = field(default_factory=list)

    # Wave 14 — Coach preferences
    coach_preferences: Optional[CoachPreferences] = None

    # Coach-controlled program inputs
    program_length_weeks: int = 8
    frequency_per_week: int = 3
    coach_intent: str = ""



@dataclass
class WarmupDrill:
    id: str
    name: str
    phase: str
    duration_sec: int
    level: str
    sport_relevance: str
    progression: str = ""
    regression: str = ""
    coaching_cue: str = ""


@dataclass
class WarmupPhase:
    name: str
    drills: list[WarmupDrill]
    duration_sec: int = 0


@dataclass
class WarmupProtocol:
    phases: list[WarmupPhase]
    total_duration_sec: int = 0


@dataclass
class RecoveryDrill:
    name: str
    duration_sec: int
    notes: str = ""


@dataclass
class RecoveryProtocol:
    id: str
    name: str
    level: int
    duration_min: int
    drills: list[RecoveryDrill]
    when: str = ""


@dataclass
class GeneratedProgram:
    athlete: str
    blueprint_id: int
    blueprint_name: str
    level: str
    duration: int
    frequency: int
    goal: str
    equipment_profile: str
    sessions: list[Session]
    athlete_profile: AthleteProfile
    credibility_score: float = 0.0
    warmup: Optional[WarmupProtocol] = None
    recovery: Optional[RecoveryProtocol] = None
    personalization_notes: list[str] = field(default_factory=list)


@dataclass
class BlockResponse:
    prior_blueprint_id: str
    prior_goal: str
    start_test_bands: dict[str, str | None]
    end_test_bands: dict[str, str | None]
    improvements: list[str]
    stalls: list[str]
    regressions: list[str]
    recommended_shift: str
    notes: list[str]

