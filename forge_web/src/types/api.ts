export type Mode = 'core' | 'premium';
export type Level = 'Beginner' | 'Intermediate' | 'Advanced';

// --- LAYER 1: RAW API CONTRACT (What Python sends) ---
export interface RawAthleteBasics {
  athlete_name?: string;
  age?: number | '';
  sex?: 'Male' | 'Female' | 'Other' | '';
  sport?: string;
  role?: string;
  training_age_years?: number | '';
  level?: Level;
  environment?: 'Pro Facility' | 'Commercial Gym' | 'Home Gym' | 'Field/Track' | '';
  available_minutes?: number;
  frequency_per_week?: number;
  days_to_match?: number | '';
}

export interface RawProgramContext {
  primary_goal?: string;
  current_phase?: string;
  equipment_profile?: string[];
  competition_proximity_note?: string;
}

export interface RawAdvancedProfile {
  force_velocity_profile?: string;
  sprint_10m_band?: string;
  aerobic_band?: string;
  squat_strength_band?: string;
  cmj_band?: string;
  technique_consistency?: 'Low' | 'Medium' | 'High' | '';
  injury_risk_flags?: string[];
  prior_block_summary?: string;
}

export interface RawProgramRequest {
  mode: Mode;
  basics: RawAthleteBasics;
  context: RawProgramContext;
  advanced: RawAdvancedProfile;
}

export interface RawExercise {
  id?: string;
  name?: string;
  family?: string;
  sets_reps?: string;
  loading_method?: string;
  rest?: string;
  progression_note?: string;
  coach_note?: string;
}

export interface RawSessionSection {
  title?: string;
  exercises?: RawExercise[];
  notes?: string;
}

export interface RawSession {
  id?: string;
  name?: string;
  week_number?: number;
  session_number?: number;
  focus?: string;
  warmup?: RawSessionSection;
  main_work?: RawSessionSection;
  conditioning?: RawSessionSection;
  session_notes?: string;
}

export interface RawProgramSummary {
  blueprint_selected?: string;
  total_weeks?: number;
  weekly_frequency?: number;
  conditioning_emphasis?: string;
  competition_window?: string;
  role_emphasis?: string;
}

export interface RawValidationNote {
  type?: 'info' | 'warning' | 'success' | 'error';
  message?: string;
}

export interface RawProgramMetadata {
  generated_at?: string;
  request_id?: string;
  api_version?: string;
}

export interface RawWeeklyExposure {
  sprint_exposure?: string;
  jump_landing_exposure?: string;
  deceleration_exposure?: string;
  eccentric_stress?: string;
  conditioning_density?: string;
  week_type?: string;
  testing_markers?: string[];
  adjustment_notes?: string[];
}

export interface RawWeek {
  week_number?: number;
  label?: string;
  exposure_summary?: RawWeeklyExposure;
}

export interface RawProgramResponse {
  metadata?: RawProgramMetadata;
  summary?: RawProgramSummary;
  weeks?: RawWeek[];
  sessions?: RawSession[];
  rationale?: string[];
  personalization_notes?: string[];
  validation?: RawValidationNote[];
  dropped_constraints?: string[];
}
