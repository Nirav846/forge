"""Wave 8 — Role-Specific Week Planning Hardening.

Deterministic role-aware week emphasis, exposure targets, and slot bias.
This module defines *what* a role should emphasize across a week / block,
independent of specific exercises.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class RoleWeekProfile:
    """Compact deterministic profile for how a role should be planned across a week.

    All emphasis fields are 0.0–1.0 where 0.0 = no emphasis, 1.0 = maximal emphasis.
    Exposure targets are categorical: "high", "moderate", "low".
    """
    # Emphasis fields (0.0–1.0)
    force_emphasis: float = 0.5
    velocity_emphasis: float = 0.5
    conditioning_emphasis: float = 0.5
    rotation_emphasis: float = 0.5
    landing_emphasis: float = 0.5
    upper_body_emphasis: float = 0.5

    # Tolerance / robustness flags
    eccentric_tolerance: str = "moderate"   # "high", "moderate", "low"
    collision_tolerance: str = "moderate"   # "high", "moderate", "low"

    # Exposure targets per week (categorical)
    sprint_exposure_target: str = "moderate"   # "high", "moderate", "low"
    jump_exposure_target: str = "moderate"     # "high", "moderate", "low"
    decel_exposure_target: str = "moderate"     # "high", "moderate", "low"
    rotation_exposure_target: str = "moderate" # "high", "moderate", "low"
    conditioning_density_bias: str = "moderate" # "high", "moderate", "low"

    # Optional: which family families get priority when slots are constrained
    family_priority: list[str] = field(default_factory=list)
    family_de_priority: list[str] = field(default_factory=list)

    # Coach-readable notes (computed, not stored per role)
    notes: list[str] = field(default_factory=list)


# ── SPORT DEFAULTS ────────────────────────────────────────────────

_SPORT_DEFAULTS: dict[str, RoleWeekProfile] = {
    "rugby": RoleWeekProfile(
        force_emphasis=0.6, velocity_emphasis=0.5, conditioning_emphasis=0.6,
        rotation_emphasis=0.4, landing_emphasis=0.5, upper_body_emphasis=0.5,
        eccentric_tolerance="high", collision_tolerance="high",
        sprint_exposure_target="moderate", jump_exposure_target="moderate",
        decel_exposure_target="moderate", rotation_exposure_target="low",
        conditioning_density_bias="high",
    ),
    "cricket": RoleWeekProfile(
        force_emphasis=0.5, velocity_emphasis=0.5, conditioning_emphasis=0.5,
        rotation_emphasis=0.5, landing_emphasis=0.5, upper_body_emphasis=0.5,
        eccentric_tolerance="moderate", collision_tolerance="low",
        sprint_exposure_target="moderate", jump_exposure_target="low",
        decel_exposure_target="low", rotation_exposure_target="moderate",
        conditioning_density_bias="moderate",
    ),
    "tennis": RoleWeekProfile(
        force_emphasis=0.4, velocity_emphasis=0.6, conditioning_emphasis=0.6,
        rotation_emphasis=0.6, landing_emphasis=0.5, upper_body_emphasis=0.5,
        eccentric_tolerance="moderate", collision_tolerance="low",
        sprint_exposure_target="moderate", jump_exposure_target="moderate",
        decel_exposure_target="moderate", rotation_exposure_target="high",
        conditioning_density_bias="high",
    ),
    "badminton": RoleWeekProfile(
        force_emphasis=0.4, velocity_emphasis=0.6, conditioning_emphasis=0.6,
        rotation_emphasis=0.5, landing_emphasis=0.5, upper_body_emphasis=0.5,
        eccentric_tolerance="moderate", collision_tolerance="low",
        sprint_exposure_target="high", jump_exposure_target="moderate",
        decel_exposure_target="moderate", rotation_exposure_target="moderate",
        conditioning_density_bias="high",
    ),
    "volleyball": RoleWeekProfile(
        force_emphasis=0.5, velocity_emphasis=0.6, conditioning_emphasis=0.5,
        rotation_emphasis=0.4, landing_emphasis=0.7, upper_body_emphasis=0.6,
        eccentric_tolerance="high", collision_tolerance="low",
        sprint_exposure_target="low", jump_exposure_target="high",
        decel_exposure_target="low", rotation_exposure_target="low",
        conditioning_density_bias="moderate",
    ),
    "soccer": RoleWeekProfile(
        force_emphasis=0.5, velocity_emphasis=0.6, conditioning_emphasis=0.7,
        rotation_emphasis=0.3, landing_emphasis=0.4, upper_body_emphasis=0.4,
        eccentric_tolerance="moderate", collision_tolerance="low",
        sprint_exposure_target="high", jump_exposure_target="low",
        decel_exposure_target="high", rotation_exposure_target="low",
        conditioning_density_bias="high",
    ),
    "football": RoleWeekProfile(
        force_emphasis=0.5, velocity_emphasis=0.6, conditioning_emphasis=0.7,
        rotation_emphasis=0.3, landing_emphasis=0.4, upper_body_emphasis=0.4,
        eccentric_tolerance="moderate", collision_tolerance="low",
        sprint_exposure_target="high", jump_exposure_target="low",
        decel_exposure_target="high", rotation_exposure_target="low",
        conditioning_density_bias="high",
    ),
    "basketball": RoleWeekProfile(
        force_emphasis=0.5, velocity_emphasis=0.6, conditioning_emphasis=0.6,
        rotation_emphasis=0.4, landing_emphasis=0.6, upper_body_emphasis=0.5,
        eccentric_tolerance="moderate", collision_tolerance="low",
        sprint_exposure_target="high", jump_exposure_target="moderate",
        decel_exposure_target="moderate", rotation_exposure_target="low",
        conditioning_density_bias="high",
    ),
}


# ── ROLE PROFILES ─────────────────────────────────────────────────

_ROLE_PROFILES: dict[str, dict[str, RoleWeekProfile]] = {
    "rugby": {
        "prop": RoleWeekProfile(
            force_emphasis=0.9, velocity_emphasis=0.2, conditioning_emphasis=0.4,
            rotation_emphasis=0.3, landing_emphasis=0.3, upper_body_emphasis=0.7,
            eccentric_tolerance="high", collision_tolerance="high",
            sprint_exposure_target="low", jump_exposure_target="low",
            decel_exposure_target="low", rotation_exposure_target="low",
            conditioning_density_bias="moderate",
            family_priority=["DLKD", "DLHD", "HPush", "HPull", "Core", "Carry"],
            family_de_priority=["Sprint", "Plyo"],
        ),
        "hooker": RoleWeekProfile(
            force_emphasis=0.8, velocity_emphasis=0.3, conditioning_emphasis=0.5,
            rotation_emphasis=0.4, landing_emphasis=0.4, upper_body_emphasis=0.6,
            eccentric_tolerance="high", collision_tolerance="high",
            sprint_exposure_target="low", jump_exposure_target="moderate",
            decel_exposure_target="low", rotation_exposure_target="low",
            conditioning_density_bias="moderate",
            family_priority=["DLKD", "DLHD", "HPush", "Core", "Carry"],
            family_de_priority=["Sprint"],
        ),
        "lock": RoleWeekProfile(
            force_emphasis=0.8, velocity_emphasis=0.3, conditioning_emphasis=0.5,
            rotation_emphasis=0.4, landing_emphasis=0.6, upper_body_emphasis=0.6,
            eccentric_tolerance="high", collision_tolerance="high",
            sprint_exposure_target="low", jump_exposure_target="high",
            decel_exposure_target="low", rotation_exposure_target="low",
            conditioning_density_bias="moderate",
            family_priority=["DLKD", "DLHD", "Plyo", "Landing", "HPush", "Core"],
            family_de_priority=["Sprint"],
        ),
        "back_row": RoleWeekProfile(
            force_emphasis=0.6, velocity_emphasis=0.5, conditioning_emphasis=0.7,
            rotation_emphasis=0.4, landing_emphasis=0.5, upper_body_emphasis=0.5,
            eccentric_tolerance="high", collision_tolerance="high",
            sprint_exposure_target="moderate", jump_exposure_target="moderate",
            decel_exposure_target="moderate", rotation_exposure_target="low",
            conditioning_density_bias="high",
            family_priority=["DLKD", "DLHD", "Sprint", "Core", "Carry"],
            family_de_priority=[],
        ),
        "scrum_half": RoleWeekProfile(
            force_emphasis=0.4, velocity_emphasis=0.7, conditioning_emphasis=0.6,
            rotation_emphasis=0.5, landing_emphasis=0.3, upper_body_emphasis=0.5,
            eccentric_tolerance="moderate", collision_tolerance="low",
            sprint_exposure_target="high", jump_exposure_target="low",
            decel_exposure_target="moderate", rotation_exposure_target="moderate",
            conditioning_density_bias="high",
            family_priority=["Sprint", "Ball", "SLKD", "SLHD", "Core"],
            family_de_priority=["DLKD"],
        ),
        "fly_half": RoleWeekProfile(
            force_emphasis=0.4, velocity_emphasis=0.6, conditioning_emphasis=0.6,
            rotation_emphasis=0.6, landing_emphasis=0.3, upper_body_emphasis=0.5,
            eccentric_tolerance="moderate", collision_tolerance="low",
            sprint_exposure_target="moderate", jump_exposure_target="low",
            decel_exposure_target="moderate", rotation_exposure_target="high",
            conditioning_density_bias="high",
            family_priority=["Sprint", "Rot", "Ball", "Core", "SLKD"],
            family_de_priority=["DLKD"],
        ),
        "centre": RoleWeekProfile(
            force_emphasis=0.5, velocity_emphasis=0.6, conditioning_emphasis=0.6,
            rotation_emphasis=0.5, landing_emphasis=0.4, upper_body_emphasis=0.5,
            eccentric_tolerance="high", collision_tolerance="high",
            sprint_exposure_target="moderate", jump_exposure_target="low",
            decel_exposure_target="high", rotation_exposure_target="moderate",
            conditioning_density_bias="high",
            family_priority=["Sprint", "Plyo", "Ball", "DLKD", "Core"],
            family_de_priority=[],
        ),
        "back_three": RoleWeekProfile(
            force_emphasis=0.3, velocity_emphasis=0.8, conditioning_emphasis=0.5,
            rotation_emphasis=0.4, landing_emphasis=0.4, upper_body_emphasis=0.4,
            eccentric_tolerance="moderate", collision_tolerance="low",
            sprint_exposure_target="high", jump_exposure_target="moderate",
            decel_exposure_target="high", rotation_exposure_target="low",
            conditioning_density_bias="moderate",
            family_priority=["Sprint", "Plyo", "Ball", "Core"],
            family_de_priority=["DLKD"],
        ),
    },
    "cricket": {
        "fast_bowler": RoleWeekProfile(
            force_emphasis=0.5, velocity_emphasis=0.6, conditioning_emphasis=0.5,
            rotation_emphasis=0.5, landing_emphasis=0.6, upper_body_emphasis=0.5,
            eccentric_tolerance="high", collision_tolerance="low",
            sprint_exposure_target="high", jump_exposure_target="high",
            decel_exposure_target="high", rotation_exposure_target="moderate",
            conditioning_density_bias="moderate",
            family_priority=["Sprint", "Landing", "SLKD", "SLHD", "Core", "Acc"],
            family_de_priority=["DLHD", "Rot", "VPush"],
        ),
        "spin_bowler": RoleWeekProfile(
            force_emphasis=0.4, velocity_emphasis=0.4, conditioning_emphasis=0.4,
            rotation_emphasis=0.8, landing_emphasis=0.2, upper_body_emphasis=0.5,
            eccentric_tolerance="low", collision_tolerance="low",
            sprint_exposure_target="low", jump_exposure_target="low",
            decel_exposure_target="low", rotation_exposure_target="high",
            conditioning_density_bias="low",
            family_priority=["Rot", "Core", "HPush", "HPull"],
            family_de_priority=["Sprint"],
        ),
        "batter": RoleWeekProfile(
            force_emphasis=0.5, velocity_emphasis=0.6, conditioning_emphasis=0.5,
            rotation_emphasis=0.7, landing_emphasis=0.3, upper_body_emphasis=0.6,
            eccentric_tolerance="moderate", collision_tolerance="low",
            sprint_exposure_target="moderate", jump_exposure_target="low",
            decel_exposure_target="moderate", rotation_exposure_target="high",
            conditioning_density_bias="moderate",
            family_priority=["Rot", "Ball", "HPush", "HPull", "Sprint"],
            family_de_priority=["Landing"],
        ),
        "wicketkeeper": RoleWeekProfile(
            force_emphasis=0.5, velocity_emphasis=0.4, conditioning_emphasis=0.4,
            rotation_emphasis=0.5, landing_emphasis=0.5, upper_body_emphasis=0.5,
            eccentric_tolerance="moderate", collision_tolerance="low",
            sprint_exposure_target="low", jump_exposure_target="moderate",
            decel_exposure_target="low", rotation_exposure_target="moderate",
            conditioning_density_bias="low",
            family_priority=["DLKD", "SLKD", "Core", "Rot", "Landing"],
            family_de_priority=["Sprint", "Plyo"],
        ),
        "all_rounder": RoleWeekProfile(
            force_emphasis=0.5, velocity_emphasis=0.5, conditioning_emphasis=0.6,
            rotation_emphasis=0.5, landing_emphasis=0.5, upper_body_emphasis=0.5,
            eccentric_tolerance="moderate", collision_tolerance="low",
            sprint_exposure_target="moderate", jump_exposure_target="moderate",
            decel_exposure_target="moderate", rotation_exposure_target="moderate",
            conditioning_density_bias="moderate",
            family_priority=["Sprint", "Rot", "DLKD", "SLKD", "Core"],
            family_de_priority=[],
        ),
    },
    "tennis": {
        "singles": RoleWeekProfile(
            force_emphasis=0.4, velocity_emphasis=0.6, conditioning_emphasis=0.7,
            rotation_emphasis=0.6, landing_emphasis=0.5, upper_body_emphasis=0.5,
            eccentric_tolerance="moderate", collision_tolerance="low",
            sprint_exposure_target="moderate", jump_exposure_target="moderate",
            decel_exposure_target="high", rotation_exposure_target="high",
            conditioning_density_bias="high",
            family_priority=["Sprint", "Landing", "SLKD", "SLHD", "Core", "Rot"],
            family_de_priority=["VPush"],
        ),
        "doubles": RoleWeekProfile(
            force_emphasis=0.4, velocity_emphasis=0.6, conditioning_emphasis=0.5,
            rotation_emphasis=0.5, landing_emphasis=0.4, upper_body_emphasis=0.6,
            eccentric_tolerance="moderate", collision_tolerance="low",
            sprint_exposure_target="low", jump_exposure_target="moderate",
            decel_exposure_target="moderate", rotation_exposure_target="moderate",
            conditioning_density_bias="moderate",
            family_priority=["Plyo", "Ball", "VPush", "VPull"],
            family_de_priority=["Sprint"],
        ),
    },
    "badminton": {
        "singles": RoleWeekProfile(
            force_emphasis=0.4, velocity_emphasis=0.7, conditioning_emphasis=0.7,
            rotation_emphasis=0.5, landing_emphasis=0.5, upper_body_emphasis=0.5,
            eccentric_tolerance="moderate", collision_tolerance="low",
            sprint_exposure_target="high", jump_exposure_target="moderate",
            decel_exposure_target="moderate", rotation_exposure_target="moderate",
            conditioning_density_bias="high",
            family_priority=["Sprint", "Landing", "SLKD", "SLHD", "Core"],
            family_de_priority=[],
        ),
        "doubles": RoleWeekProfile(
            force_emphasis=0.4, velocity_emphasis=0.6, conditioning_emphasis=0.5,
            rotation_emphasis=0.5, landing_emphasis=0.4, upper_body_emphasis=0.6,
            eccentric_tolerance="moderate", collision_tolerance="low",
            sprint_exposure_target="low", jump_exposure_target="moderate",
            decel_exposure_target="moderate", rotation_exposure_target="moderate",
            conditioning_density_bias="moderate",
            family_priority=["Plyo", "Ball", "VPush", "VPull", "SLKD"],
            family_de_priority=["Sprint"],
        ),
    },
    "volleyball": {
        "middle_blocker": RoleWeekProfile(
            force_emphasis=0.6, velocity_emphasis=0.6, conditioning_emphasis=0.5,
            rotation_emphasis=0.3, landing_emphasis=0.9, upper_body_emphasis=0.7,
            eccentric_tolerance="high", collision_tolerance="low",
            sprint_exposure_target="low", jump_exposure_target="high",
            decel_exposure_target="low", rotation_exposure_target="low",
            conditioning_density_bias="moderate",
            family_priority=["Plyo", "Landing", "DLKD", "VPush", "VPull", "Core"],
            family_de_priority=["Sprint"],
        ),
        "outside_hitter": RoleWeekProfile(
            force_emphasis=0.5, velocity_emphasis=0.6, conditioning_emphasis=0.5,
            rotation_emphasis=0.5, landing_emphasis=0.7, upper_body_emphasis=0.6,
            eccentric_tolerance="high", collision_tolerance="low",
            sprint_exposure_target="low", jump_exposure_target="high",
            decel_exposure_target="low", rotation_exposure_target="moderate",
            conditioning_density_bias="moderate",
            family_priority=["Plyo", "Landing", "HPush", "HPull", "Rot", "Core"],
            family_de_priority=["Sprint"],
        ),
        "opposite": RoleWeekProfile(
            force_emphasis=0.6, velocity_emphasis=0.5, conditioning_emphasis=0.5,
            rotation_emphasis=0.6, landing_emphasis=0.6, upper_body_emphasis=0.7,
            eccentric_tolerance="high", collision_tolerance="low",
            sprint_exposure_target="low", jump_exposure_target="high",
            decel_exposure_target="low", rotation_exposure_target="high",
            conditioning_density_bias="moderate",
            family_priority=["Plyo", "Landing", "HPush", "HPull", "Rot", "Core"],
            family_de_priority=["Sprint"],
        ),
        "setter": RoleWeekProfile(
            force_emphasis=0.4, velocity_emphasis=0.5, conditioning_emphasis=0.5,
            rotation_emphasis=0.5, landing_emphasis=0.3, upper_body_emphasis=0.5,
            eccentric_tolerance="moderate", collision_tolerance="low",
            sprint_exposure_target="low", jump_exposure_target="low",
            decel_exposure_target="low", rotation_exposure_target="moderate",
            conditioning_density_bias="moderate",
            family_priority=["SLKD", "SLHD", "Core", "Rot"],
            family_de_priority=["VPush", "Sprint"],
        ),
        "libero": RoleWeekProfile(
            force_emphasis=0.3, velocity_emphasis=0.5, conditioning_emphasis=0.6,
            rotation_emphasis=0.4, landing_emphasis=0.4, upper_body_emphasis=0.3,
            eccentric_tolerance="moderate", collision_tolerance="low",
            sprint_exposure_target="moderate", jump_exposure_target="low",
            decel_exposure_target="moderate", rotation_exposure_target="low",
            conditioning_density_bias="high",
            family_priority=["Landing", "SLKD", "SLHD", "Sprint", "Core"],
            family_de_priority=["VPush", "VPull"],
        ),
    },
    "soccer": {
        "goalkeeper": RoleWeekProfile(
            force_emphasis=0.5, velocity_emphasis=0.5, conditioning_emphasis=0.4,
            rotation_emphasis=0.4, landing_emphasis=0.7, upper_body_emphasis=0.4,
            eccentric_tolerance="high", collision_tolerance="low",
            sprint_exposure_target="low", jump_exposure_target="high",
            decel_exposure_target="low", rotation_exposure_target="low",
            conditioning_density_bias="low",
            family_priority=["Plyo", "Landing", "Ball", "SLKD", "SLHD"],
            family_de_priority=["VPush", "VPull", "Sprint"],
        ),
        "centre_back": RoleWeekProfile(
            force_emphasis=0.7, velocity_emphasis=0.5, conditioning_emphasis=0.6,
            rotation_emphasis=0.3, landing_emphasis=0.4, upper_body_emphasis=0.5,
            eccentric_tolerance="high", collision_tolerance="high",
            sprint_exposure_target="moderate", jump_exposure_target="low",
            decel_exposure_target="moderate", rotation_exposure_target="low",
            conditioning_density_bias="high",
            family_priority=["DLKD", "DLHD", "Sprint", "Core", "Carry"],
            family_de_priority=["Plyo"],
        ),
        "fullback": RoleWeekProfile(
            force_emphasis=0.5, velocity_emphasis=0.7, conditioning_emphasis=0.7,
            rotation_emphasis=0.3, landing_emphasis=0.4, upper_body_emphasis=0.4,
            eccentric_tolerance="moderate", collision_tolerance="low",
            sprint_exposure_target="high", jump_exposure_target="low",
            decel_exposure_target="high", rotation_exposure_target="low",
            conditioning_density_bias="high",
            family_priority=["Sprint", "SLKD", "SLHD", "Core", "Carry"],
            family_de_priority=["Plyo"],
        ),
        "midfielder": RoleWeekProfile(
            force_emphasis=0.5, velocity_emphasis=0.6, conditioning_emphasis=0.8,
            rotation_emphasis=0.4, landing_emphasis=0.4, upper_body_emphasis=0.4,
            eccentric_tolerance="moderate", collision_tolerance="low",
            sprint_exposure_target="high", jump_exposure_target="low",
            decel_exposure_target="high", rotation_exposure_target="low",
            conditioning_density_bias="high",
            family_priority=["Sprint", "SLKD", "SLHD", "Core", "Carry"],
            family_de_priority=["Plyo"],
        ),
        "winger": RoleWeekProfile(
            force_emphasis=0.3, velocity_emphasis=0.8, conditioning_emphasis=0.6,
            rotation_emphasis=0.3, landing_emphasis=0.4, upper_body_emphasis=0.4,
            eccentric_tolerance="moderate", collision_tolerance="low",
            sprint_exposure_target="high", jump_exposure_target="low",
            decel_exposure_target="high", rotation_exposure_target="low",
            conditioning_density_bias="moderate",
            family_priority=["Sprint", "Plyo", "Ball", "Core"],
            family_de_priority=["DLKD"],
        ),
        "striker": RoleWeekProfile(
            force_emphasis=0.5, velocity_emphasis=0.7, conditioning_emphasis=0.6,
            rotation_emphasis=0.4, landing_emphasis=0.5, upper_body_emphasis=0.5,
            eccentric_tolerance="moderate", collision_tolerance="low",
            sprint_exposure_target="high", jump_exposure_target="moderate",
            decel_exposure_target="high", rotation_exposure_target="low",
            conditioning_density_bias="moderate",
            family_priority=["Sprint", "Plyo", "Ball", "Landing", "DLKD"],
            family_de_priority=[],
        ),
    },
    "football": {
        "goalkeeper": RoleWeekProfile(
            force_emphasis=0.5, velocity_emphasis=0.5, conditioning_emphasis=0.4,
            rotation_emphasis=0.4, landing_emphasis=0.7, upper_body_emphasis=0.4,
            eccentric_tolerance="high", collision_tolerance="low",
            sprint_exposure_target="low", jump_exposure_target="high",
            decel_exposure_target="low", rotation_exposure_target="low",
            conditioning_density_bias="low",
            family_priority=["Plyo", "Landing", "Ball", "SLKD", "SLHD"],
            family_de_priority=["VPush", "VPull", "Sprint"],
        ),
        "centre_back": RoleWeekProfile(
            force_emphasis=0.7, velocity_emphasis=0.5, conditioning_emphasis=0.6,
            rotation_emphasis=0.3, landing_emphasis=0.4, upper_body_emphasis=0.5,
            eccentric_tolerance="high", collision_tolerance="high",
            sprint_exposure_target="moderate", jump_exposure_target="low",
            decel_exposure_target="moderate", rotation_exposure_target="low",
            conditioning_density_bias="high",
            family_priority=["DLKD", "DLHD", "Sprint", "Core", "Carry"],
            family_de_priority=["Plyo"],
        ),
        "fullback": RoleWeekProfile(
            force_emphasis=0.5, velocity_emphasis=0.7, conditioning_emphasis=0.7,
            rotation_emphasis=0.3, landing_emphasis=0.4, upper_body_emphasis=0.4,
            eccentric_tolerance="moderate", collision_tolerance="low",
            sprint_exposure_target="high", jump_exposure_target="low",
            decel_exposure_target="high", rotation_exposure_target="low",
            conditioning_density_bias="high",
            family_priority=["Sprint", "SLKD", "SLHD", "Core", "Carry"],
            family_de_priority=["Plyo"],
        ),
        "midfielder": RoleWeekProfile(
            force_emphasis=0.5, velocity_emphasis=0.6, conditioning_emphasis=0.8,
            rotation_emphasis=0.4, landing_emphasis=0.4, upper_body_emphasis=0.4,
            eccentric_tolerance="moderate", collision_tolerance="low",
            sprint_exposure_target="high", jump_exposure_target="low",
            decel_exposure_target="high", rotation_exposure_target="low",
            conditioning_density_bias="high",
            family_priority=["Sprint", "SLKD", "SLHD", "Core", "Carry"],
            family_de_priority=["Plyo"],
        ),
        "winger": RoleWeekProfile(
            force_emphasis=0.3, velocity_emphasis=0.8, conditioning_emphasis=0.6,
            rotation_emphasis=0.3, landing_emphasis=0.4, upper_body_emphasis=0.4,
            eccentric_tolerance="moderate", collision_tolerance="low",
            sprint_exposure_target="high", jump_exposure_target="low",
            decel_exposure_target="high", rotation_exposure_target="low",
            conditioning_density_bias="moderate",
            family_priority=["Sprint", "Plyo", "Ball", "Core"],
            family_de_priority=["DLKD"],
        ),
        "striker": RoleWeekProfile(
            force_emphasis=0.5, velocity_emphasis=0.7, conditioning_emphasis=0.6,
            rotation_emphasis=0.4, landing_emphasis=0.5, upper_body_emphasis=0.5,
            eccentric_tolerance="moderate", collision_tolerance="low",
            sprint_exposure_target="high", jump_exposure_target="moderate",
            decel_exposure_target="high", rotation_exposure_target="low",
            conditioning_density_bias="moderate",
            family_priority=["Sprint", "Plyo", "Ball", "Landing", "DLKD"],
            family_de_priority=[],
        ),
    },
    "basketball": {
        "guard": RoleWeekProfile(
            force_emphasis=0.3, velocity_emphasis=0.8, conditioning_emphasis=0.7,
            rotation_emphasis=0.4, landing_emphasis=0.5, upper_body_emphasis=0.5,
            eccentric_tolerance="moderate", collision_tolerance="low",
            sprint_exposure_target="high", jump_exposure_target="moderate",
            decel_exposure_target="high", rotation_exposure_target="low",
            conditioning_density_bias="high",
            family_priority=["Sprint", "Plyo", "Ball", "SLKD", "SLHD", "Core"],
            family_de_priority=["DLKD", "DLHD"],
        ),
        "wing": RoleWeekProfile(
            force_emphasis=0.5, velocity_emphasis=0.7, conditioning_emphasis=0.6,
            rotation_emphasis=0.5, landing_emphasis=0.6, upper_body_emphasis=0.6,
            eccentric_tolerance="moderate", collision_tolerance="low",
            sprint_exposure_target="high", jump_exposure_target="moderate",
            decel_exposure_target="moderate", rotation_exposure_target="moderate",
            conditioning_density_bias="moderate",
            family_priority=["Sprint", "Plyo", "Ball", "HPush", "HPull", "Core"],
            family_de_priority=["DLKD"],
        ),
        "big": RoleWeekProfile(
            force_emphasis=0.8, velocity_emphasis=0.4, conditioning_emphasis=0.5,
            rotation_emphasis=0.4, landing_emphasis=0.7, upper_body_emphasis=0.6,
            eccentric_tolerance="high", collision_tolerance="high",
            sprint_exposure_target="low", jump_exposure_target="high",
            decel_exposure_target="low", rotation_exposure_target="low",
            conditioning_density_bias="moderate",
            family_priority=["DLKD", "DLHD", "Plyo", "Landing", "HPush", "HPull", "Core"],
            family_de_priority=["Sprint"],
        ),
    },
}


# ── PUBLIC API ────────────────────────────────────────────────────

def get_role_week_profile(sport: str, role: str | None) -> RoleWeekProfile:
    """Return the RoleWeekProfile for a given sport + role.

    Falls back to sport-level default if role is unknown or not provided.
    Falls back to a generic neutral profile if sport is unknown.
    """
    if not sport:
        return RoleWeekProfile()

    sport_lower = sport.lower().strip()
    role_lower = (role or "").lower().strip()

    # Direct lookup
    sport_roles = _ROLE_PROFILES.get(sport_lower, {})
    if role_lower and role_lower in sport_roles:
        return sport_roles[role_lower]

    # Try alias mappings for common variations
    _ALIASES = {
        "spin_bowler": "spin_bowler",
        "spinner": "spin_bowler",
        "fast_bowler": "fast_bowler",
        "back_row": "back_row",
        "backrow": "back_row",
        "scrum_half": "scrum_half",
        "halfback": "scrum_half",
        "fly_half": "fly_half",
        "flyhalf": "fly_half",
        "back_three": "back_three",
        "backline": "back_three",
        "middle_blocker": "middle_blocker",
        "middle": "middle_blocker",
        "outside_hitter": "outside_hitter",
        "outside": "outside_hitter",
        "centre_back": "centre_back",
        "defender": "centre_back",
        "fullback": "fullback",
        "midfielder": "midfielder",
        "forward": "striker",
        "striker": "striker",
    }
    aliased = _ALIASES.get(role_lower)
    if aliased and aliased in sport_roles:
        return sport_roles[aliased]

    # Sport default fallback
    sport_default = _SPORT_DEFAULTS.get(sport_lower)
    if sport_default:
        return sport_default

    # Generic neutral fallback
    return RoleWeekProfile()


def get_role_week_notes(sport: str, role: str | None) -> list[str]:
    """Return coach-readable weekly emphasis notes for a sport + role.

    Replaces / extends the Wave 6 version in athlete_profile_rules.py.
    """
    profile = get_role_week_profile(sport, role)
    notes = []
    role_name = (role or "General").replace("_", " ").title()
    sport_name = (sport or "Unknown").title()

    # Build a primary emphasis sentence
    emphases = []
    if profile.force_emphasis >= 0.7:
        emphases.append("maximal force")
    if profile.velocity_emphasis >= 0.7:
        emphases.append("velocity / speed-power")
    if profile.conditioning_emphasis >= 0.7:
        emphases.append("repeat conditioning")
    if profile.rotation_emphasis >= 0.7:
        emphases.append("rotational emphasis")
    if profile.landing_emphasis >= 0.7:
        emphases.append("jump-landing emphasis")
    if profile.upper_body_emphasis >= 0.7:
        emphases.append("upper-body emphasis")
    if profile.collision_tolerance == "high":
        emphases.append("collision robustness")

    if emphases:
        emphasis_str = " / ".join(emphases)
        notes.append(f"{role_name} role -> {emphasis_str} bias")
    else:
        notes.append(f"{role_name} role -> balanced week emphasis")

    # Exposure moderation notes
    if profile.sprint_exposure_target == "low":
        notes.append("Sprint exposure moderated per role")
    if profile.sprint_exposure_target == "high":
        notes.append("Sprint exposure elevated per role")
    if profile.jump_exposure_target == "low":
        notes.append("Jump/landing volume capped per role")
    if profile.jump_exposure_target == "high":
        notes.append("Jump/landing volume elevated per role")
    if profile.decel_exposure_target == "low":
        notes.append("Deceleration accumulation capped per role")
    if profile.decel_exposure_target == "high":
        notes.append("Deceleration emphasis elevated per role")
    if profile.rotation_exposure_target == "low":
        notes.append("Rotational exposure moderated per role")
    if profile.rotation_exposure_target == "high":
        notes.append("Rotational exposure elevated per role")
    if profile.conditioning_density_bias == "high":
        notes.append("Higher conditioning density than role baseline")
    elif profile.conditioning_density_bias == "low":
        notes.append("Lower conditioning density than role baseline")
    if profile.eccentric_tolerance == "high":
        notes.append("High-eccentric tolerance allowed per role")
    elif profile.eccentric_tolerance == "low":
        notes.append("High-eccentric accumulation capped per role")

    return notes


# ── EXPOSURE LIMITS ───────────────────────────────────────────────

def get_role_exposure_limits(profile: RoleWeekProfile) -> dict[str, int]:
    """Return numeric weekly caps based on role profile.

    These caps are role-aware and replace the hard constants in
    weekly_exposure_warnings.
    """
    # Base limits
    sprint_max = 4
    landing_max = 3
    jump_max = 4
    decel_max = 3
    rotation_max = 4
    high_eccentric_max = 3

    # Sprint caps
    if profile.sprint_exposure_target == "high":
        sprint_max = 5
        decel_max = 4
    elif profile.sprint_exposure_target == "low":
        sprint_max = 2
        decel_max = 2

    # Jump / landing caps
    if profile.jump_exposure_target == "high":
        jump_max = 5
        landing_max = 4
    elif profile.jump_exposure_target == "low":
        jump_max = 2
        landing_max = 2

    # Rotation caps
    if profile.rotation_exposure_target == "high":
        rotation_max = 5
    elif profile.rotation_exposure_target == "low":
        rotation_max = 2

    # Eccentric caps
    if profile.eccentric_tolerance == "high":
        high_eccentric_max = 4
    elif profile.eccentric_tolerance == "low":
        high_eccentric_max = 2

    return {
        "sprint_max": sprint_max,
        "landing_max": landing_max,
        "jump_max": jump_max,
        "decel_max": decel_max,
        "rotation_max": rotation_max,
        "high_eccentric_max": high_eccentric_max,
    }


# ── SLOT BIAS ─────────────────────────────────────────────────────

def apply_role_slot_bias(
    slots: list,  # list of FamilyCode
    profile: RoleWeekProfile,
) -> list:
    """Re-order slots to respect role priorities without violating blueprint identity.

    - Mandatory families (implied by the fact they are in slots) are kept.
    - Role-preferred families are moved earlier in the order.
    - Role-de-prioritized families are moved later (dropped first under time constraints).
    """
    if not profile.family_priority and not profile.family_de_priority:
        return list(slots)

    # Build a scoring map for re-ordering
    priority = {fam: i for i, fam in enumerate(profile.family_priority)}
    de_priority = {fam: i for i, fam in enumerate(profile.family_de_priority)}

    def _slot_score(fam) -> tuple:
        fam_val = fam.value if hasattr(fam, "value") else str(fam)
        # Prefer: priority families first, then neutral, then de-prioritized
        if fam_val in priority:
            return (0, priority[fam_val])
        if fam_val in de_priority:
            return (2, de_priority[fam_val])
        return (1, 0)

    return sorted(slots, key=_slot_score)


# ── CONDITIONING FREQUENCY BIAS ───────────────────────────────────

def get_role_conditioning_frequency_bias(profile: RoleWeekProfile) -> float:
    """Return a bias multiplier for how often conditioning should appear.

    1.0 = baseline (every other session)
    >1.0 = more frequent
    <1.0 = less frequent
    """
    if profile.conditioning_density_bias == "high":
        return 1.33
    elif profile.conditioning_density_bias == "low":
        return 0.67
    return 1.0


def should_add_conditioning_for_role(
    week: int, day: int, freq: int, goal: str, profile: RoleWeekProfile
) -> bool:
    """Role-aware conditioning frequency check.

    Wraps the base logic with a role density bias.
    """
    # Base logic: conditioning for conditioning/return-to-sport goals, or every other session
    if goal in ("conditioning", "return_to_sport"):
        return True

    base_should = (week + day) % 2 == 0
    density = get_role_conditioning_frequency_bias(profile)

    if density >= 1.33:
        # High density: add conditioning on more days
        return base_should or (week + day) % 3 == 0
    elif density <= 0.67:
        # Low density: only add on specific days, skip some
        return base_should and (week + day) % 3 != 0

    return base_should


# ── ROLE QUALITATIVE SUMMARY ──────────────────────────────────────

def render_role_week_summary(profile: RoleWeekProfile) -> list[str]:
    """Return a compact coach-readable summary of role week targets."""
    return [
        f"  Force emphasis:           {profile.force_emphasis:.1f}",
        f"  Velocity emphasis:        {profile.velocity_emphasis:.1f}",
        f"  Conditioning emphasis:    {profile.conditioning_emphasis:.1f}",
        f"  Rotation emphasis:        {profile.rotation_emphasis:.1f}",
        f"  Landing emphasis:         {profile.landing_emphasis:.1f}",
        f"  Upper-body emphasis:      {profile.upper_body_emphasis:.1f}",
        "",
        f"  Sprint exposure target:   {profile.sprint_exposure_target.title()}",
        f"  Jump/Landing exposure target: {profile.jump_exposure_target.title()}",
        f"  Deceleration exposure target: {profile.decel_exposure_target.title()}",
        f"  Rotation exposure target: {profile.rotation_exposure_target.title()}",
        f"  Conditioning density:     {profile.conditioning_density_bias.title()}",
    ]
