import { Mode, Level } from './api';

// --- LAYER 3: UI VIEW MODELS (What React renders) ---

export type ProgramStatus = 'draft' | 'reviewed' | 'approved' | 'archive';

export interface SavedProgramArtifact {
  id: string;
  created_at: string;
  updated_at: string;
  version: number;
  status: ProgramStatus;
  
  // Metadata for list view
  athlete_display_name: string;
  sport: string;
  role: string;
  goal: string;
  blueprint_label: string;
  week_label: string;
  mode: 'core' | 'premium';
  
  // Scaffolding for coach workflows
  coach_notes: string;
  internal_notes: string;
  
  // Payloads
  request_snapshot: any; // ProgramRequest
  result_snapshot: TransformationResult;
}

export interface TransformerWarning {
  path: string;
  issue: string;
  action_taken: string;
}

export interface TransformationResult {
  viewModel: ProgramViewModel | null;
  warnings: TransformerWarning[];
  rawPayload: any;
}

// Exercises are guaranteed to have these fields via transformer
export interface ExerciseVM {
  id: string;
  name: string;
  family: string;
  sets_reps: string;
  loading_method: string;
  rest: string;
  progression_note?: string;
  coach_note?: string;
}

export interface SessionSectionVM {
  title: string;
  exercises: ExerciseVM[];
  notes?: string;
}

export interface SessionVM {
  id: string;
  name: string;
  week_number: number;
  session_number: number;
  focus: string;
  warmup: SessionSectionVM;
  main_work: SessionSectionVM;
  conditioning: SessionSectionVM;
  session_notes?: string;
}

export interface ProgramSummaryVM {
  blueprint_selected: string;
  total_weeks: number;
  weekly_frequency: number;
  conditioning_emphasis: string;
  competition_window: string;
  role_emphasis: string;
}

export interface ValidationNoteVM {
  type: 'info' | 'warning' | 'success' | 'error';
  message: string;
}

export interface ProgramMetadataVM {
  generated_at: string;
  request_id: string;
  api_version: string;
}

export interface WeeklyExposureVM {
  sprint_exposure: string;
  jump_landing_exposure: string;
  deceleration_exposure: string;
  eccentric_stress: string;
  conditioning_density: string;
  week_type: string;
  testing_markers: string[];
  adjustment_notes: string[];
}

export interface WeekVM {
  week_number: number;
  label: string;
  exposure_summary: WeeklyExposureVM;
  sessions: SessionVM[];
}

export interface ProgramViewModel {
  metadata: ProgramMetadataVM;
  summary: ProgramSummaryVM;
  weeks: WeekVM[];
  sessions: SessionVM[]; // flat list for raw/backwards compat
  rationale: string[];
  personalization_notes: string[];
  validation: ValidationNoteVM[];
  dropped_constraints: string[];
}
