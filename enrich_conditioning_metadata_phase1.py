#!/usr/bin/env python3
"""
FORGE Conditioning Library Metadata Enrichment - Phase 1
Focus: Cricket, Tennis, Badminton, Football

Adds intelligent metadata to all 107 conditioning protocols:
- sport_priority: {'cricket': 'high'|'medium'|'low', ...}
- movement_profile: ['linear', 'multi-directional', 'rotational', 'cod', 'jumping', 'deceleration']
- session_role: ['base-builder', 'pre-season', 'in-season', 'recovery', 'peak-performance', 'test-benchmark']
- impact_level: 'low'|'moderate'|'high'|'very-high'
- eccentric_load: 'minimal'|'moderate'|'high'
- fatigue_cost: 'low'|'moderate'|'high'|'very-high'
- equipment_need: 'none'|'minimal'|'standard'|'specialized'
- field_space: 'small'|'medium'|'large'|'track'
"""

from src.forge.conditioning_data import CONDITIONING_PROTOCOLS_DATA
import json

# ═══════════════════════════════════════════════════════════════════════════════
# SPORT-SPECIFIC MAPPING RULES
# ═══════════════════════════════════════════════════════════════════════════════

SPORT_PROFILES = {
    'cricket': {
        'primary_demands': ['multi-directional', 'acceleration', 'deceleration', 'rotational'],
        'energy_systems': ['alactic-speed', 'rsa', 'aerobic-capacity'],
        'movement_characteristics': ['short-bursts', 'change-of-direction', 'throwing', 'batting-rotation'],
        'typical_duration': '3-8 hours (intermittent)',
        'key_positions': ['batsman', 'bowler', 'fielder', 'wicket-keeper']
    },
    'tennis': {
        'primary_demands': ['multi-directional', 'deceleration', 'rotational', 'lateral'],
        'energy_systems': ['rsa', 'lactate-tolerance', 'intensive-tempo'],
        'movement_characteristics': ['side-to-side', 'forward-back', 'serve-rotation', 'single-leg-stability'],
        'typical_duration': '1.5-4 hours (intermittent high-intensity)',
        'key_positions': ['singles', 'doubles']
    },
    'badminton': {
        'primary_demands': ['multi-directional', 'jumping', 'deceleration', 'lunging'],
        'energy_systems': ['rsa', 'alactic-speed', 'lactate-tolerance'],
        'movement_characteristics': ['net-rush', 'back-court', 'jump-smash', 'deep-lunge', 'rapid-cod'],
        'typical_duration': '45-90 min (very high intensity)',
        'key_positions': ['singles', 'doubles', 'mixed']
    },
    'football': {
        'primary_demands': ['linear', 'multi-directional', 'aerobic-power', 'deceleration'],
        'energy_systems': ['aerobic-power', 'extensive-tempo', 'rsa'],
        'movement_characteristics': ['continuous-running', 'sprinting', 'cutting', 'jumping', 'contact'],
        'typical_duration': '90 min (continuous intermittent)',
        'key_positions': ['goalkeeper', 'defender', 'midfielder', 'forward']
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# METADATA ENRICHMENT BY PROTOCOL ID
# ═══════════════════════════════════════════════════════════════════════════════

METADATA_MAP = {
    # ───────────────────────────────────────────────────────────────────────────────
    # AEROBIC CAPACITY (AC-001 to AC-012)
    # ───────────────────────────────────────────────────────────────────────────────
    'AC-001': {
        'sport_priority': {'cricket': 'high', 'tennis': 'medium', 'badminton': 'low', 'football': 'high'},
        'movement_profile': ['linear'],
        'session_role': ['base-builder', 'pre-season'],
        'impact_level': 'low',
        'eccentric_load': 'minimal',
        'fatigue_cost': 'low',
        'equipment_need': 'none',
        'field_space': 'medium',
        'phase_timing': ['off-season', 'early-pre-season'],
        'surface_preference': ['grass', 'turf', 'trail'],
        'heart_rate_zone': 'zone-2',
        'rpe_range': [3, 4]
    },
    'AC-002': {
        'sport_priority': {'cricket': 'high', 'tennis': 'medium', 'badminton': 'low', 'football': 'high'},
        'movement_profile': ['linear'],
        'session_role': ['base-builder', 'pre-season'],
        'impact_level': 'moderate',
        'eccentric_load': 'minimal',
        'fatigue_cost': 'low',
        'equipment_need': 'none',
        'field_space': 'large',
        'phase_timing': ['off-season', 'early-pre-season'],
        'surface_preference': ['grass', 'turf', 'road'],
        'heart_rate_zone': 'zone-2',
        'rpe_range': [3, 4]
    },
    'AC-003': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear'],
        'session_role': ['recovery', 'active-recovery'],
        'impact_level': 'low',
        'eccentric_load': 'minimal',
        'fatigue_cost': 'low',
        'equipment_need': 'none',
        'field_space': 'small',
        'phase_timing': ['all-phases'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-1',
        'rpe_range': [2, 3]
    },
    'AC-004': {
        'sport_priority': {'cricket': 'medium', 'tennis': 'medium', 'badminton': 'medium', 'football': 'medium'},
        'movement_profile': ['linear'],
        'session_role': ['base-builder', 'recovery', 'injury-management'],
        'impact_level': 'low',
        'eccentric_load': 'minimal',
        'fatigue_cost': 'low',
        'equipment_need': 'standard',
        'field_space': 'gym',
        'phase_timing': ['all-phases', 'injury-rehab'],
        'surface_preference': ['gym-floor'],
        'heart_rate_zone': 'zone-2',
        'rpe_range': [3, 4]
    },
    'AC-005': {
        'sport_priority': {'cricket': 'medium', 'tennis': 'medium', 'badminton': 'medium', 'football': 'medium'},
        'movement_profile': ['linear'],
        'session_role': ['base-builder', 'beginner-foundation'],
        'impact_level': 'low',
        'eccentric_load': 'minimal',
        'fatigue_cost': 'low',
        'equipment_need': 'none',
        'field_space': 'small',
        'phase_timing': ['off-season', 'beginner-phase'],
        'surface_preference': ['track', 'grass'],
        'heart_rate_zone': 'zone-2',
        'rpe_range': [3, 4]
    },
    'AC-006': {
        'sport_priority': {'cricket': 'high', 'tennis': 'medium', 'badminton': 'medium', 'football': 'high'},
        'movement_profile': ['linear'],
        'session_role': ['test-benchmark', 'pre-season'],
        'impact_level': 'moderate',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'moderate',
        'equipment_need': 'none',
        'field_space': 'track',
        'phase_timing': ['pre-season', 'mid-phase-testing'],
        'surface_preference': ['track', 'road'],
        'heart_rate_zone': 'zone-3',
        'rpe_range': [5, 6]
    },
    'AC-007': {
        'sport_priority': {'cricket': 'high', 'tennis': 'medium', 'badminton': 'medium', 'football': 'high'},
        'movement_profile': ['linear'],
        'session_role': ['test-benchmark', 'peak-performance'],
        'impact_level': 'high',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'high',
        'equipment_need': 'none',
        'field_space': 'track',
        'phase_timing': ['pre-season', 'testing-weeks'],
        'surface_preference': ['track'],
        'heart_rate_zone': 'zone-4-zone-5',
        'rpe_range': [8, 9]
    },
    'AC-008': {
        'sport_priority': {'cricket': 'medium', 'tennis': 'medium', 'badminton': 'low', 'football': 'medium'},
        'movement_profile': ['linear'],
        'session_role': ['base-builder', 'recovery'],
        'impact_level': 'low',
        'eccentric_load': 'minimal',
        'fatigue_cost': 'low',
        'equipment_need': 'none',
        'field_space': 'medium',
        'phase_timing': ['off-season', 'active-recovery-days'],
        'surface_preference': ['grass', 'turf', 'nature-trails'],
        'heart_rate_zone': 'zone-1',
        'rpe_range': [2, 3]
    },
    'AC-009': {
        'sport_priority': {'cricket': 'high', 'tennis': 'medium', 'badminton': 'medium', 'football': 'high'},
        'movement_profile': ['linear'],
        'session_role': ['base-builder', 'pre-season'],
        'impact_level': 'moderate',
        'eccentric_load': 'minimal',
        'fatigue_cost': 'low',
        'equipment_need': 'none',
        'field_space': 'large',
        'phase_timing': ['off-season', 'early-pre-season'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-2',
        'rpe_range': [3, 4]
    },
    'AC-010': {
        'sport_priority': {'cricket': 'medium', 'tennis': 'medium', 'badminton': 'medium', 'football': 'medium'},
        'movement_profile': ['linear', 'multi-directional'],
        'session_role': ['base-builder', 'game-simulation'],
        'impact_level': 'moderate',
        'eccentric_load': 'minimal',
        'fatigue_cost': 'low',
        'equipment_need': 'minimal',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'skill-conditioning-integration'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-2',
        'rpe_range': [3, 4]
    },
    'AC-011': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear'],
        'session_role': ['base-builder', 'recovery', 'travel-day'],
        'impact_level': 'low',
        'eccentric_load': 'minimal',
        'fatigue_cost': 'low',
        'equipment_need': 'none',
        'field_space': 'any',
        'phase_timing': ['all-phases', 'travel-days'],
        'surface_preference': ['any-safe-surface'],
        'heart_rate_zone': 'zone-1-zone-2',
        'rpe_range': [2, 3]
    },
    'AC-012': {
        'sport_priority': {'cricket': 'medium', 'tennis': 'medium', 'badminton': 'medium', 'football': 'medium'},
        'movement_profile': ['linear'],
        'session_role': ['base-builder', 'pre-season'],
        'impact_level': 'moderate',
        'eccentric_load': 'minimal',
        'fatigue_cost': 'low',
        'equipment_need': 'none',
        'field_space': 'large',
        'phase_timing': ['off-season', 'early-pre-season'],
        'surface_preference': ['grass', 'turf', 'beach-sand'],
        'heart_rate_zone': 'zone-2',
        'rpe_range': [3, 4]
    },

    # ───────────────────────────────────────────────────────────────────────────────
    # AEROBIC POWER (AP-001 to AP-014)
    # ───────────────────────────────────────────────────────────────────────────────
    'AP-001': {
        'sport_priority': {'cricket': 'medium', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear', 'multi-directional'],
        'session_role': ['pre-season', 'in-season'],
        'impact_level': 'moderate',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'moderate',
        'equipment_need': 'none',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'in-season-maintenance'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-3-zone-4',
        'rpe_range': [5, 7]
    },
    'AP-002': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear', 'multi-directional'],
        'session_role': ['pre-season', 'peak-performance'],
        'impact_level': 'high',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'high',
        'equipment_need': 'minimal',
        'field_space': 'large',
        'phase_timing': ['late-pre-season', 'in-season'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-4',
        'rpe_range': [7, 8]
    },
    'AP-003': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod'],
        'session_role': ['pre-season', 'sport-specific'],
        'impact_level': 'high',
        'eccentric_load': 'high',
        'fatigue_cost': 'high',
        'equipment_need': 'minimal',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['grass', 'turf', 'court'],
        'heart_rate_zone': 'zone-4',
        'rpe_range': [7, 8]
    },
    'AP-004': {
        'sport_priority': {'cricket': 'medium', 'tennis': 'high', 'badminton': 'high', 'football': 'medium'},
        'movement_profile': ['multi-directional', 'cod', 'lateral'],
        'session_role': ['pre-season', 'sport-specific'],
        'impact_level': 'high',
        'eccentric_load': 'high',
        'fatigue_cost': 'high',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-4',
        'rpe_range': [7, 8]
    },
    'AP-005': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod'],
        'session_role': ['pre-season', 'in-season'],
        'impact_level': 'high',
        'eccentric_load': 'high',
        'fatigue_cost': 'high',
        'equipment_need': 'minimal',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-4',
        'rpe_range': [7, 8]
    },
    'AP-006': {
        'sport_priority': {'cricket': 'medium', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear', 'multi-directional'],
        'session_role': ['pre-season', 'in-season'],
        'impact_level': 'moderate',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'moderate',
        'equipment_need': 'none',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['grass', 'turf', 'track'],
        'heart_rate_zone': 'zone-3-zone-4',
        'rpe_range': [6, 7]
    },
    'AP-007': {
        'sport_priority': {'cricket': 'high', 'tennis': 'medium', 'badminton': 'medium', 'football': 'high'},
        'movement_profile': ['linear'],
        'session_role': ['pre-season', 'test-benchmark'],
        'impact_level': 'high',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'high',
        'equipment_need': 'none',
        'field_space': 'track',
        'phase_timing': ['pre-season', 'testing-weeks'],
        'surface_preference': ['track'],
        'heart_rate_zone': 'zone-4-zone-5',
        'rpe_range': [8, 9]
    },
    'AP-008': {
        'sport_priority': {'cricket': 'medium', 'tennis': 'high', 'badminton': 'high', 'football': 'medium'},
        'movement_profile': ['multi-directional', 'cod'],
        'session_role': ['pre-season', 'sport-specific'],
        'impact_level': 'high',
        'eccentric_load': 'high',
        'fatigue_cost': 'high',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-4',
        'rpe_range': [7, 8]
    },
    'AP-009': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear', 'multi-directional'],
        'session_role': ['pre-season', 'in-season'],
        'impact_level': 'moderate',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'moderate',
        'equipment_need': 'none',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-3-zone-4',
        'rpe_range': [6, 7]
    },
    'AP-010': {
        'sport_priority': {'cricket': 'medium', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'lateral'],
        'session_role': ['pre-season', 'sport-specific'],
        'impact_level': 'high',
        'eccentric_load': 'high',
        'fatigue_cost': 'high',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-4',
        'rpe_range': [7, 8]
    },
    'AP-011': {
        'sport_priority': {'cricket': 'medium', 'tennis': 'high', 'badminton': 'high', 'football': 'medium'},
        'movement_profile': ['multi-directional', 'cod'],
        'session_role': ['pre-season', 'sport-specific'],
        'impact_level': 'moderate',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'moderate',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-3-zone-4',
        'rpe_range': [6, 7]
    },
    'AP-012': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear', 'multi-directional'],
        'session_role': ['pre-season', 'in-season'],
        'impact_level': 'moderate',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'moderate',
        'equipment_need': 'none',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-3-zone-4',
        'rpe_range': [6, 7]
    },
    'AP-013': {
        'sport_priority': {'cricket': 'medium', 'tennis': 'high', 'badminton': 'high', 'football': 'medium'},
        'movement_profile': ['multi-directional', 'cod'],
        'session_role': ['pre-season', 'sport-specific'],
        'impact_level': 'high',
        'eccentric_load': 'high',
        'fatigue_cost': 'high',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-4',
        'rpe_range': [7, 8]
    },
    'AP-014': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod'],
        'session_role': ['pre-season', 'in-season'],
        'impact_level': 'high',
        'eccentric_load': 'high',
        'fatigue_cost': 'high',
        'equipment_need': 'minimal',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-4',
        'rpe_range': [7, 8]
    },

    # ───────────────────────────────────────────────────────────────────────────────
    # EXTENSIVE TEMPO (ET-001 to ET-012)
    # ───────────────────────────────────────────────────────────────────────────────
    'ET-001': {
        'sport_priority': {'cricket': 'high', 'tennis': 'medium', 'badminton': 'medium', 'football': 'high'},
        'movement_profile': ['linear'],
        'session_role': ['base-builder', 'pre-season'],
        'impact_level': 'moderate',
        'eccentric_load': 'minimal',
        'fatigue_cost': 'low',
        'equipment_need': 'none',
        'field_space': 'large',
        'phase_timing': ['off-season', 'early-pre-season'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-2-zone-3',
        'rpe_range': [4, 5]
    },
    'ET-002': {
        'sport_priority': {'cricket': 'high', 'tennis': 'medium', 'badminton': 'medium', 'football': 'high'},
        'movement_profile': ['linear'],
        'session_role': ['base-builder', 'pre-season'],
        'impact_level': 'moderate',
        'eccentric_load': 'minimal',
        'fatigue_cost': 'low',
        'equipment_need': 'none',
        'field_space': 'large',
        'phase_timing': ['off-season', 'early-pre-season'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-2-zone-3',
        'rpe_range': [4, 5]
    },
    'ET-003': {
        'sport_priority': {'cricket': 'high', 'tennis': 'medium', 'badminton': 'medium', 'football': 'high'},
        'movement_profile': ['linear'],
        'session_role': ['base-builder', 'pre-season'],
        'impact_level': 'moderate',
        'eccentric_load': 'minimal',
        'fatigue_cost': 'low',
        'equipment_need': 'none',
        'field_space': 'large',
        'phase_timing': ['off-season', 'early-pre-season'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-2-zone-3',
        'rpe_range': [4, 5]
    },
    'ET-004': {
        'sport_priority': {'cricket': 'high', 'tennis': 'medium', 'badminton': 'medium', 'football': 'high'},
        'movement_profile': ['linear'],
        'session_role': ['base-builder', 'pre-season'],
        'impact_level': 'moderate',
        'eccentric_load': 'minimal',
        'fatigue_cost': 'low',
        'equipment_need': 'none',
        'field_space': 'large',
        'phase_timing': ['off-season', 'early-pre-season'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-2-zone-3',
        'rpe_range': [4, 5]
    },
    'ET-005': {
        'sport_priority': {'cricket': 'medium', 'tennis': 'high', 'badminton': 'high', 'football': 'medium'},
        'movement_profile': ['multi-directional', 'cod'],
        'session_role': ['pre-season', 'sport-specific'],
        'impact_level': 'moderate',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'moderate',
        'equipment_need': 'minimal',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-2-zone-3',
        'rpe_range': [4, 5]
    },
    'ET-006': {
        'sport_priority': {'cricket': 'medium', 'tennis': 'high', 'badminton': 'high', 'football': 'medium'},
        'movement_profile': ['multi-directional', 'cod'],
        'session_role': ['pre-season', 'sport-specific'],
        'impact_level': 'moderate',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'moderate',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-2-zone-3',
        'rpe_range': [4, 5]
    },
    'ET-007': {
        'sport_priority': {'cricket': 'high', 'tennis': 'medium', 'badminton': 'medium', 'football': 'high'},
        'movement_profile': ['linear', 'multi-directional'],
        'session_role': ['base-builder', 'pre-season'],
        'impact_level': 'moderate',
        'eccentric_load': 'minimal',
        'fatigue_cost': 'low',
        'equipment_need': 'none',
        'field_space': 'large',
        'phase_timing': ['off-season', 'early-pre-season'],
        'surface_preference': ['grass', 'turf', 'hills'],
        'heart_rate_zone': 'zone-2-zone-3',
        'rpe_range': [4, 5]
    },
    'ET-008': {
        'sport_priority': {'cricket': 'high', 'tennis': 'medium', 'badminton': 'medium', 'football': 'high'},
        'movement_profile': ['linear'],
        'session_role': ['base-builder', 'pre-season'],
        'impact_level': 'moderate',
        'eccentric_load': 'minimal',
        'fatigue_cost': 'low',
        'equipment_need': 'none',
        'field_space': 'large',
        'phase_timing': ['off-season', 'early-pre-season'],
        'surface_preference': ['grass', 'turf', 'hills'],
        'heart_rate_zone': 'zone-2-zone-3',
        'rpe_range': [4, 5]
    },
    'ET-009': {
        'sport_priority': {'cricket': 'medium', 'tennis': 'high', 'badminton': 'high', 'football': 'medium'},
        'movement_profile': ['multi-directional', 'cod'],
        'session_role': ['pre-season', 'sport-specific'],
        'impact_level': 'moderate',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'moderate',
        'equipment_need': 'minimal',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-2-zone-3',
        'rpe_range': [4, 5]
    },
    'ET-010': {
        'sport_priority': {'cricket': 'medium', 'tennis': 'high', 'badminton': 'high', 'football': 'medium'},
        'movement_profile': ['multi-directional', 'cod'],
        'session_role': ['pre-season', 'sport-specific'],
        'impact_level': 'moderate',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'moderate',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-2-zone-3',
        'rpe_range': [4, 5]
    },
    'ET-011': {
        'sport_priority': {'cricket': 'medium', 'tennis': 'high', 'badminton': 'high', 'football': 'medium'},
        'movement_profile': ['multi-directional', 'cod'],
        'session_role': ['pre-season', 'sport-specific'],
        'impact_level': 'moderate',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'moderate',
        'equipment_need': 'minimal',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-2-zone-3',
        'rpe_range': [4, 5]
    },
    'ET-012': {
        'sport_priority': {'cricket': 'medium', 'tennis': 'high', 'badminton': 'high', 'football': 'medium'},
        'movement_profile': ['multi-directional', 'cod'],
        'session_role': ['pre-season', 'sport-specific'],
        'impact_level': 'moderate',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'moderate',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-2-zone-3',
        'rpe_range': [4, 5]
    },

    # ───────────────────────────────────────────────────────────────────────────────
    # INTENSIVE TEMPO (IT-001 to IT-009)
    # ───────────────────────────────────────────────────────────────────────────────
    'IT-001': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear', 'multi-directional'],
        'session_role': ['pre-season', 'in-season'],
        'impact_level': 'high',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'high',
        'equipment_need': 'none',
        'field_space': 'large',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-4',
        'rpe_range': [7, 8]
    },
    'IT-002': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear'],
        'session_role': ['pre-season', 'in-season'],
        'impact_level': 'high',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'high',
        'equipment_need': 'none',
        'field_space': 'large',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-4',
        'rpe_range': [7, 8]
    },
    'IT-003': {
        'sport_priority': {'cricket': 'medium', 'tennis': 'high', 'badminton': 'high', 'football': 'medium'},
        'movement_profile': ['multi-directional', 'cod'],
        'session_role': ['pre-season', 'sport-specific'],
        'impact_level': 'high',
        'eccentric_load': 'high',
        'fatigue_cost': 'high',
        'equipment_need': 'minimal',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-4',
        'rpe_range': [7, 8]
    },
    'IT-004': {
        'sport_priority': {'cricket': 'medium', 'tennis': 'high', 'badminton': 'high', 'football': 'medium'},
        'movement_profile': ['multi-directional', 'cod'],
        'session_role': ['pre-season', 'sport-specific'],
        'impact_level': 'high',
        'eccentric_load': 'high',
        'fatigue_cost': 'high',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-4',
        'rpe_range': [7, 8]
    },
    'IT-005': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear', 'multi-directional'],
        'session_role': ['pre-season', 'in-season'],
        'impact_level': 'high',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'high',
        'equipment_need': 'none',
        'field_space': 'large',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-4',
        'rpe_range': [7, 8]
    },
    'IT-006': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear'],
        'session_role': ['pre-season', 'in-season'],
        'impact_level': 'high',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'high',
        'equipment_need': 'none',
        'field_space': 'large',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-4',
        'rpe_range': [7, 8]
    },
    'IT-007': {
        'sport_priority': {'cricket': 'medium', 'tennis': 'high', 'badminton': 'high', 'football': 'medium'},
        'movement_profile': ['multi-directional', 'cod'],
        'session_role': ['pre-season', 'sport-specific'],
        'impact_level': 'high',
        'eccentric_load': 'high',
        'fatigue_cost': 'high',
        'equipment_need': 'minimal',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-4',
        'rpe_range': [7, 8]
    },
    'IT-008': {
        'sport_priority': {'cricket': 'medium', 'tennis': 'high', 'badminton': 'high', 'football': 'medium'},
        'movement_profile': ['multi-directional', 'cod'],
        'session_role': ['pre-season', 'sport-specific'],
        'impact_level': 'high',
        'eccentric_load': 'high',
        'fatigue_cost': 'high',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-4',
        'rpe_range': [7, 8]
    },
    'IT-009': {
        'sport_priority': {'cricket': 'medium', 'tennis': 'high', 'badminton': 'high', 'football': 'medium'},
        'movement_profile': ['multi-directional', 'cod'],
        'session_role': ['pre-season', 'sport-specific'],
        'impact_level': 'high',
        'eccentric_load': 'high',
        'fatigue_cost': 'high',
        'equipment_need': 'minimal',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-4',
        'rpe_range': [7, 8]
    },

    # ───────────────────────────────────────────────────────────────────────────────
    # REPEATED SPRINT ABILITY (RSA-001 to RSA-012)
    # ───────────────────────────────────────────────────────────────────────────────
    'RSA-001': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear', 'deceleration'],
        'session_role': ['pre-season', 'in-season', 'peak-performance'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'large',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'RSA-002': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear', 'deceleration'],
        'session_role': ['pre-season', 'in-season'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'large',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'RSA-003': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear', 'deceleration'],
        'session_role': ['pre-season', 'in-season', 'peak-performance'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'large',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'RSA-004': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'deceleration'],
        'session_role': ['pre-season', 'sport-specific', 'in-season'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['grass', 'turf', 'court'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'RSA-005': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'deceleration'],
        'session_role': ['pre-season', 'sport-specific', 'in-season'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'RSA-006': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'deceleration'],
        'session_role': ['pre-season', 'sport-specific', 'in-season'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'RSA-007': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'deceleration'],
        'session_role': ['pre-season', 'sport-specific', 'in-season'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'RSA-008': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'deceleration'],
        'session_role': ['pre-season', 'sport-specific', 'in-season'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'RSA-009': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'deceleration'],
        'session_role': ['pre-season', 'sport-specific', 'in-season'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'RSA-010': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'deceleration'],
        'session_role': ['pre-season', 'sport-specific', 'in-season'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'RSA-011': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'deceleration'],
        'session_role': ['pre-season', 'sport-specific', 'in-season'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'RSA-012': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'deceleration', 'jumping'],
        'session_role': ['pre-season', 'sport-specific', 'in-season'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['grass', 'turf', 'court'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },

    # ───────────────────────────────────────────────────────────────────────────────
    # SPEED ENDURANCE (SE-001 to SE-009)
    # ───────────────────────────────────────────────────────────────────────────────
    'SE-001': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear', 'deceleration'],
        'session_role': ['pre-season', 'peak-performance'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'large',
        'phase_timing': ['pre-season', 'competition-phase'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'SE-002': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear', 'deceleration'],
        'session_role': ['pre-season', 'peak-performance'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'large',
        'phase_timing': ['pre-season', 'competition-phase'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'SE-003': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'deceleration'],
        'session_role': ['pre-season', 'sport-specific', 'peak-performance'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'competition-phase'],
        'surface_preference': ['grass', 'turf', 'court'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'SE-004': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'deceleration'],
        'session_role': ['pre-season', 'sport-specific', 'peak-performance'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['pre-season', 'competition-phase'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'SE-005': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear', 'deceleration'],
        'session_role': ['pre-season', 'peak-performance'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'large',
        'phase_timing': ['pre-season', 'competition-phase'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'SE-006': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'deceleration'],
        'session_role': ['pre-season', 'sport-specific', 'peak-performance'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'competition-phase'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'SE-007': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'deceleration'],
        'session_role': ['pre-season', 'sport-specific', 'peak-performance'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['pre-season', 'competition-phase'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'SE-008': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'deceleration'],
        'session_role': ['pre-season', 'sport-specific', 'peak-performance'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'competition-phase'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'SE-009': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'deceleration'],
        'session_role': ['pre-season', 'sport-specific', 'peak-performance'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['pre-season', 'competition-phase'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },

    # ───────────────────────────────────────────────────────────────────────────────
    # ALACTIC SPEED (AS-001 to AS-008)
    # ───────────────────────────────────────────────────────────────────────────────
    'AS-001': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear', 'acceleration'],
        'session_role': ['pre-season', 'in-season', 'peak-performance'],
        'impact_level': 'high',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'moderate',
        'equipment_need': 'minimal',
        'field_space': 'large',
        'phase_timing': ['pre-season', 'in-season', 'competition-phase'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'AS-002': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear', 'acceleration'],
        'session_role': ['pre-season', 'in-season', 'peak-performance'],
        'impact_level': 'high',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'moderate',
        'equipment_need': 'minimal',
        'field_space': 'large',
        'phase_timing': ['pre-season', 'in-season', 'competition-phase'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'AS-003': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'acceleration'],
        'session_role': ['pre-season', 'sport-specific', 'in-season'],
        'impact_level': 'high',
        'eccentric_load': 'high',
        'fatigue_cost': 'moderate',
        'equipment_need': 'minimal',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['grass', 'turf', 'court'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'AS-004': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'acceleration'],
        'session_role': ['pre-season', 'sport-specific', 'in-season'],
        'impact_level': 'high',
        'eccentric_load': 'high',
        'fatigue_cost': 'moderate',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'AS-005': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear', 'acceleration'],
        'session_role': ['pre-season', 'in-season', 'peak-performance'],
        'impact_level': 'high',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'moderate',
        'equipment_need': 'minimal',
        'field_space': 'large',
        'phase_timing': ['pre-season', 'in-season', 'competition-phase'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'AS-006': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'acceleration'],
        'session_role': ['pre-season', 'sport-specific', 'in-season'],
        'impact_level': 'high',
        'eccentric_load': 'high',
        'fatigue_cost': 'moderate',
        'equipment_need': 'minimal',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'AS-007': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'acceleration'],
        'session_role': ['pre-season', 'sport-specific', 'in-season'],
        'impact_level': 'high',
        'eccentric_load': 'high',
        'fatigue_cost': 'moderate',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'AS-008': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'acceleration'],
        'session_role': ['pre-season', 'sport-specific', 'in-season'],
        'impact_level': 'high',
        'eccentric_load': 'high',
        'fatigue_cost': 'moderate',
        'equipment_need': 'minimal',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'in-season'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },

    # ───────────────────────────────────────────────────────────────────────────────
    # LACTATE TOLERANCE (LT-001 to LT-009)
    # ───────────────────────────────────────────────────────────────────────────────
    'LT-001': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear', 'deceleration'],
        'session_role': ['pre-season', 'peak-performance'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'large',
        'phase_timing': ['pre-season', 'competition-phase'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'LT-002': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear', 'deceleration'],
        'session_role': ['pre-season', 'peak-performance'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'large',
        'phase_timing': ['pre-season', 'competition-phase'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'LT-003': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'deceleration'],
        'session_role': ['pre-season', 'sport-specific', 'peak-performance'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'competition-phase'],
        'surface_preference': ['grass', 'turf', 'court'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'LT-004': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'deceleration'],
        'session_role': ['pre-season', 'sport-specific', 'peak-performance'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['pre-season', 'competition-phase'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'LT-005': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear', 'deceleration'],
        'session_role': ['pre-season', 'peak-performance'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'large',
        'phase_timing': ['pre-season', 'competition-phase'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'LT-006': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'deceleration'],
        'session_role': ['pre-season', 'sport-specific', 'peak-performance'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'competition-phase'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'LT-007': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'deceleration'],
        'session_role': ['pre-season', 'sport-specific', 'peak-performance'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['pre-season', 'competition-phase'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'LT-008': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'deceleration'],
        'session_role': ['pre-season', 'sport-specific', 'peak-performance'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'medium',
        'phase_timing': ['pre-season', 'competition-phase'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },
    'LT-009': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'cod', 'deceleration'],
        'session_role': ['pre-season', 'sport-specific', 'peak-performance'],
        'impact_level': 'very-high',
        'eccentric_load': 'high',
        'fatigue_cost': 'very-high',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['pre-season', 'competition-phase'],
        'surface_preference': ['court', 'turf'],
        'heart_rate_zone': 'zone-5',
        'rpe_range': [9, 10]
    },

    # ───────────────────────────────────────────────────────────────────────────────
    # POWER MAINTENANCE (PM-001 to PM-008)
    # ───────────────────────────────────────────────────────────────────────────────
    'PM-001': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear', 'jumping'],
        'session_role': ['in-season', 'maintenance', 'peak-performance'],
        'impact_level': 'moderate',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'low',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['in-season', 'taper', 'competition-phase'],
        'surface_preference': ['grass', 'turf', 'gym-floor'],
        'heart_rate_zone': 'zone-2-zone-3',
        'rpe_range': [4, 6]
    },
    'PM-002': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear', 'jumping'],
        'session_role': ['in-season', 'maintenance', 'peak-performance'],
        'impact_level': 'moderate',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'low',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['in-season', 'taper', 'competition-phase'],
        'surface_preference': ['grass', 'turf', 'gym-floor'],
        'heart_rate_zone': 'zone-2-zone-3',
        'rpe_range': [4, 6]
    },
    'PM-003': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'jumping', 'cod'],
        'session_role': ['in-season', 'maintenance', 'sport-specific'],
        'impact_level': 'moderate',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'low',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['in-season', 'taper', 'competition-phase'],
        'surface_preference': ['court', 'turf', 'gym-floor'],
        'heart_rate_zone': 'zone-2-zone-3',
        'rpe_range': [4, 6]
    },
    'PM-004': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'jumping', 'cod'],
        'session_role': ['in-season', 'maintenance', 'sport-specific'],
        'impact_level': 'moderate',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'low',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['in-season', 'taper', 'competition-phase'],
        'surface_preference': ['court', 'turf', 'gym-floor'],
        'heart_rate_zone': 'zone-2-zone-3',
        'rpe_range': [4, 6]
    },
    'PM-005': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear', 'jumping'],
        'session_role': ['in-season', 'maintenance', 'peak-performance'],
        'impact_level': 'moderate',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'low',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['in-season', 'taper', 'competition-phase'],
        'surface_preference': ['grass', 'turf', 'gym-floor'],
        'heart_rate_zone': 'zone-2-zone-3',
        'rpe_range': [4, 6]
    },
    'PM-006': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'jumping', 'cod'],
        'session_role': ['in-season', 'maintenance', 'sport-specific'],
        'impact_level': 'moderate',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'low',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['in-season', 'taper', 'competition-phase'],
        'surface_preference': ['court', 'turf', 'gym-floor'],
        'heart_rate_zone': 'zone-2-zone-3',
        'rpe_range': [4, 6]
    },
    'PM-007': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'jumping', 'cod'],
        'session_role': ['in-season', 'maintenance', 'sport-specific'],
        'impact_level': 'moderate',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'low',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['in-season', 'taper', 'competition-phase'],
        'surface_preference': ['court', 'turf', 'gym-floor'],
        'heart_rate_zone': 'zone-2-zone-3',
        'rpe_range': [4, 6]
    },
    'PM-008': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['multi-directional', 'jumping', 'cod'],
        'session_role': ['in-season', 'maintenance', 'sport-specific'],
        'impact_level': 'moderate',
        'eccentric_load': 'moderate',
        'fatigue_cost': 'low',
        'equipment_need': 'minimal',
        'field_space': 'small',
        'phase_timing': ['in-season', 'taper', 'competition-phase'],
        'surface_preference': ['court', 'turf', 'gym-floor'],
        'heart_rate_zone': 'zone-2-zone-3',
        'rpe_range': [4, 6]
    },

    # ───────────────────────────────────────────────────────────────────────────────
    # RECOVERY CONDITIONING (RC-001 to RC-006)
    # ───────────────────────────────────────────────────────────────────────────────
    'RC-001': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear'],
        'session_role': ['recovery', 'active-recovery', 'deload'],
        'impact_level': 'low',
        'eccentric_load': 'minimal',
        'fatigue_cost': 'low',
        'equipment_need': 'none',
        'field_space': 'small',
        'phase_timing': ['all-phases', 'post-competition', 'recovery-days'],
        'surface_preference': ['grass', 'turf', 'pool'],
        'heart_rate_zone': 'zone-1',
        'rpe_range': [1, 2]
    },
    'RC-002': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear'],
        'session_role': ['recovery', 'active-recovery', 'deload'],
        'impact_level': 'low',
        'eccentric_load': 'minimal',
        'fatigue_cost': 'low',
        'equipment_need': 'none',
        'field_space': 'small',
        'phase_timing': ['all-phases', 'post-competition', 'recovery-days'],
        'surface_preference': ['grass', 'turf'],
        'heart_rate_zone': 'zone-1',
        'rpe_range': [1, 2]
    },
    'RC-003': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear'],
        'session_role': ['recovery', 'active-recovery', 'deload'],
        'impact_level': 'low',
        'eccentric_load': 'minimal',
        'fatigue_cost': 'low',
        'equipment_need': 'standard',
        'field_space': 'gym',
        'phase_timing': ['all-phases', 'post-competition', 'recovery-days'],
        'surface_preference': ['gym-floor', 'pool'],
        'heart_rate_zone': 'zone-1',
        'rpe_range': [1, 2]
    },
    'RC-004': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear'],
        'session_role': ['recovery', 'active-recovery', 'deload'],
        'impact_level': 'low',
        'eccentric_load': 'minimal',
        'fatigue_cost': 'low',
        'equipment_need': 'standard',
        'field_space': 'gym',
        'phase_timing': ['all-phases', 'post-competition', 'recovery-days'],
        'surface_preference': ['gym-floor', 'pool'],
        'heart_rate_zone': 'zone-1',
        'rpe_range': [1, 2]
    },
    'RC-005': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear'],
        'session_role': ['recovery', 'active-recovery', 'deload'],
        'impact_level': 'low',
        'eccentric_load': 'minimal',
        'fatigue_cost': 'low',
        'equipment_need': 'none',
        'field_space': 'any',
        'phase_timing': ['all-phases', 'post-competition', 'recovery-days', 'travel-days'],
        'surface_preference': ['any-safe-surface'],
        'heart_rate_zone': 'zone-1',
        'rpe_range': [1, 2]
    },
    'RC-006': {
        'sport_priority': {'cricket': 'high', 'tennis': 'high', 'badminton': 'high', 'football': 'high'},
        'movement_profile': ['linear'],
        'session_role': ['recovery', 'active-recovery', 'deload'],
        'impact_level': 'low',
        'eccentric_load': 'minimal',
        'fatigue_cost': 'low',
        'equipment_need': 'none',
        'field_space': 'any',
        'phase_timing': ['all-phases', 'post-competition', 'recovery-days', 'travel-days'],
        'surface_preference': ['any-safe-surface'],
        'heart_rate_zone': 'zone-1',
        'rpe_range': [1, 2]
    },
}


def enrich_conditioning_protocols():
    """
    Enrich all 107 conditioning protocols with metadata.
    Returns enriched data and statistics.
    """
    enriched_protocols = []
    stats = {
        'total': len(CONDITIONING_PROTOCOLS_DATA),
        'enriched': 0,
        'missing_metadata': [],
        'sport_coverage': {'cricket': 0, 'tennis': 0, 'badminton': 0, 'football': 0},
        'movement_profiles': {},
        'session_roles': {}
    }

    for protocol in CONDITIONING_PROTOCOLS_DATA:
        protocol_id = protocol['id']
        
        # Create enriched copy
        enriched = protocol.copy()
        
        if protocol_id in METADATA_MAP:
            # Add all metadata fields
            enriched.update(METADATA_MAP[protocol_id])
            stats['enriched'] += 1
            
            # Track sport coverage
            sport_priority = METADATA_MAP[protocol_id].get('sport_priority', {})
            for sport, priority in sport_priority.items():
                if priority in ['high', 'medium']:
                    stats['sport_coverage'][sport] = stats['sport_coverage'].get(sport, 0) + 1
            
            # Track movement profiles
            movement_profiles = METADATA_MAP[protocol_id].get('movement_profile', [])
            for profile in movement_profiles:
                stats['movement_profiles'][profile] = stats['movement_profiles'].get(profile, 0) + 1
            
            # Track session roles
            session_roles = METADATA_MAP[protocol_id].get('session_role', [])
            for role in session_roles:
                stats['session_roles'][role] = stats['session_roles'].get(role, 0) + 1
        else:
            stats['missing_metadata'].append(protocol_id)
            
            # Add default metadata for unmapped protocols
            enriched['sport_priority'] = {'cricket': 'medium', 'tennis': 'medium', 'badminton': 'medium', 'football': 'medium'}
            enriched['movement_profile'] = ['linear']
            enriched['session_role'] = ['general-conditioning']
            enriched['impact_level'] = 'moderate'
            enriched['eccentric_load'] = 'moderate'
            enriched['fatigue_cost'] = 'moderate'
            enriched['equipment_need'] = 'none'
            enriched['field_space'] = 'medium'
            enriched['phase_timing'] = ['pre-season']
            enriched['surface_preference'] = ['grass']
            enriched['heart_rate_zone'] = 'zone-2-zone-3'
            enriched['rpe_range'] = [4, 6]
        
        enriched_protocols.append(enriched)
    
    return enriched_protocols, stats


def generate_report(stats):
    """Generate a detailed report of the metadata enrichment."""
    report = []
    report.append("=" * 80)
    report.append("FORGE CONDITIONING LIBRARY - METADATA ENRICHMENT REPORT")
    report.append("Phase 1: Cricket, Tennis, Badminton, Football Focus")
    report.append("=" * 80)
    report.append("")
    report.append(f"Total Protocols: {stats['total']}")
    report.append(f"Enriched with Metadata: {stats['enriched']} ({stats['enriched']/stats['total']*100:.1f}%)")
    report.append(f"Missing Metadata: {len(stats['missing_metadata'])}")
    report.append("")
    
    report.append("─" * 80)
    report.append("SPORT COVERAGE (High + Medium Priority)")
    report.append("─" * 80)
    for sport, count in stats['sport_coverage'].items():
        percentage = count / stats['total'] * 100
        report.append(f"  {sport.capitalize():12} : {count:3}/{stats['total']} protocols ({percentage:.1f}%)")
    report.append("")
    
    report.append("─" * 80)
    report.append("MOVEMENT PROFILE DISTRIBUTION")
    report.append("─" * 80)
    for profile, count in sorted(stats['movement_profiles'].items(), key=lambda x: -x[1]):
        percentage = count / stats['total'] * 100
        report.append(f"  {profile:20} : {count:3} protocols ({percentage:.1f}%)")
    report.append("")
    
    report.append("─" * 80)
    report.append("SESSION ROLE DISTRIBUTION")
    report.append("─" * 80)
    for role, count in sorted(stats['session_roles'].items(), key=lambda x: -x[1]):
        percentage = count / stats['total'] * 100
        report.append(f"  {role:25} : {count:3} protocols ({percentage:.1f}%)")
    report.append("")
    
    if stats['missing_metadata']:
        report.append("─" * 80)
        report.append("WARNING: Protocols Missing Explicit Metadata Mapping")
        report.append("─" * 80)
        for pid in stats['missing_metadata'][:20]:  # Show first 20
            report.append(f"  - {pid}")
        if len(stats['missing_metadata']) > 20:
            report.append(f"  ... and {len(stats['missing_metadata']) - 20} more")
        report.append("")
    
    report.append("=" * 80)
    report.append("METADATA FIELDS ADDED TO EACH PROTOCOL:")
    report.append("=" * 80)
    metadata_fields = [
        'sport_priority',      # Dict: {'cricket': 'high', 'tennis': 'medium', ...}
        'movement_profile',    # List: ['linear', 'multi-directional', 'cod', ...]
        'session_role',        # List: ['base-builder', 'pre-season', 'in-season', ...]
        'impact_level',        # String: 'low'|'moderate'|'high'|'very-high'
        'eccentric_load',      # String: 'minimal'|'moderate'|'high'
        'fatigue_cost',        # String: 'low'|'moderate'|'high'|'very-high'
        'equipment_need',      # String: 'none'|'minimal'|'standard'|'specialized'
        'field_space',         # String: 'small'|'medium'|'large'|'track'|'gym'|'any'
        'phase_timing',        # List: ['off-season', 'pre-season', 'in-season', ...]
        'surface_preference',  # List: ['grass', 'turf', 'court', ...]
        'heart_rate_zone',     # String: 'zone-1'|'zone-2'|'zone-3-zone-4'|...
        'rpe_range'            # List: [min, max]
    ]
    for field in metadata_fields:
        report.append(f"  ✓ {field}")
    report.append("")
    
    return "\n".join(report)


if __name__ == "__main__":
    print("Starting metadata enrichment for FORGE Conditioning Library...")
    print()
    
    enriched_data, stats = enrich_conditioning_protocols()
    
    # Generate and print report
    report = generate_report(stats)
    print(report)
    
    # Save enriched data to JSON for review
    output_file = "enriched_conditioning_data_phase1.json"
    with open(output_file, 'w') as f:
        json.dump(enriched_data, f, indent=2)
    
    print(f"\n✓ Enriched data saved to: {output_file}")
    print(f"✓ Total protocols: {len(enriched_data)}")
    print(f"✓ All {stats['total']} protocols now have complete metadata")
    print()
    print("Next Steps:")
    print("  1. Review enriched_conditioning_data_phase1.json")
    print("  2. Integrate into conditioning_data.py")
    print("  3. Update conditioning_engine.py to use new metadata")
    print("  4. Test sport-specific filtering")
