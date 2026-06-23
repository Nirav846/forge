import { 
  TransformerWarning, 
  TransformationResult, 
  ProgramViewModel, 
  SessionSectionVM, 
  ExerciseVM, 
  SessionVM, 
  ValidationNoteVM, 
  ProgramMetadataVM, 
  ProgramSummaryVM 
} from '../types/ui';

import { RawProgramResponse, RawSessionSection, RawExercise } from '../types/api';

/**
 * Adapter/Transformer layer.
 * Normalizes a raw, potentially dirty backend response into the exact canonical `ProgramViewModel` required by the UI.
 * Returns TransformationResult containing the safe ViewModel, parsing warnings, and the raw payload.
 */
export function normalizeProgramResponse(raw: any): TransformationResult {
  const warnings: TransformerWarning[] = [];

  if (!raw || typeof raw !== 'object') {
    warnings.push({ path: 'root', issue: 'Response is not a valid JSON object', action_taken: 'Returning null ViewModel' });
    return { viewModel: null, warnings, rawPayload: raw };
  }

  // Helper to log warnings safely
  const warn = (path: string, issue: string, action_taken: string) => warnings.push({ path, issue, action_taken });

  // Normalize Metadata
  const metadata: ProgramMetadataVM = {
    generated_at: raw?.metadata?.generated_at || new Date().toISOString(),
    request_id: raw?.metadata?.request_id || `req_fallback_${Math.random().toString(36).substring(7)}`,
    api_version: raw?.metadata?.api_version || '1.0.0',
  };

  if (!raw?.metadata?.generated_at) warn('metadata.generated_at', 'Missing timestamp', 'Generated local timestamp');

  // Normalize Summary
  const summary: ProgramSummaryVM = {
    blueprint_selected: raw?.summary?.blueprint_selected || 'Fallback Blueprint (Missing Data)',
    total_weeks: typeof raw?.summary?.total_weeks === 'number' ? raw.summary.total_weeks : 0,
    weekly_frequency: typeof raw?.summary?.weekly_frequency === 'number' ? raw.summary.weekly_frequency : 0,
    conditioning_emphasis: raw?.summary?.conditioning_emphasis || 'None Specified',
    competition_window: raw?.summary?.competition_window || 'Unknown',
    role_emphasis: raw?.summary?.role_emphasis || 'General',
  };

  if (!raw?.summary?.blueprint_selected) warn('summary.blueprint_selected', 'Missing blueprint name', 'Used fallback string');

  // Normalize Exercises
  const normalizeExercise = (ex: any, index: number, path: string): ExerciseVM => {
    if (!ex?.name) warn(`${path}[${index}].name`, 'Missing exercise name', 'Used placeholder');
    return {
      id: ex?.id || `ex_${Date.now()}_${index}`,
      name: ex?.name || 'Unknown Exercise',
      family: ex?.family || 'General',
      sets_reps: ex?.sets_reps || '- x -',
      loading_method: ex?.loading_method || '-',
      rest: ex?.rest || '-',
      progression_note: ex?.progression_note || undefined,
      coach_note: ex?.coach_note || undefined,
    };
  };

  // Normalize Session Section
  const normalizeSection = (sec: any, defaultTitle: string, path: string): SessionSectionVM => {
    if (!sec || typeof sec !== 'object') {
       if (sec !== undefined && sec !== null) warn(path, 'Malformed section', 'Replaced with empty section');
       return { title: defaultTitle, exercises: [] };
    }
    return {
      title: sec.title || defaultTitle,
      exercises: Array.isArray(sec.exercises) ? sec.exercises.map((ex, i) => normalizeExercise(ex, i, `${path}.exercises`)) : [],
      notes: sec.notes || undefined,
    };
  };

  // Normalize Sessions
  const sessions: SessionVM[] = Array.isArray(raw?.sessions) 
    ? raw.sessions.map((sess: any, index: number) => ({
        id: sess?.id || `sess_${index}`,
        name: sess?.name || `Session ${index + 1}`,
        week_number: typeof sess?.week_number === 'number' ? sess.week_number : 1,
        session_number: typeof sess?.session_number === 'number' ? sess.session_number : (index + 1),
        focus: sess?.focus || 'General Focus',
        warmup: normalizeSection(sess?.warmup, 'Warmup', `sessions[${index}].warmup`),
        main_work: normalizeSection(sess?.main_work, 'Main Work', `sessions[${index}].main_work`),
        conditioning: normalizeSection(sess?.conditioning, 'Conditioning', `sessions[${index}].conditioning`),
        session_notes: sess?.session_notes || undefined,
      }))
    : [];

  if (!Array.isArray(raw?.sessions) || raw.sessions.length === 0) {
    warn('sessions', 'No sessions array found', 'Created empty sessions array');
  }

  // Normalize Weeks
  const normalizeExposure = (exp: any): any => ({
    sprint_exposure: exp?.sprint_exposure || 'Not specified',
    jump_landing_exposure: exp?.jump_landing_exposure || 'Not specified',
    deceleration_exposure: exp?.deceleration_exposure || 'Not specified',
    eccentric_stress: exp?.eccentric_stress || 'Not specified',
    conditioning_density: exp?.conditioning_density || 'Not specified',
    week_type: exp?.week_type || 'Standard',
    testing_markers: Array.isArray(exp?.testing_markers) ? exp.testing_markers : [],
    adjustment_notes: Array.isArray(exp?.adjustment_notes) ? exp.adjustment_notes : [],
  });

  const weeksMap = new Map();
  if (Array.isArray(raw?.weeks)) {
    raw.weeks.forEach((w: any) => {
       if (w.week_number) {
          weeksMap.set(w.week_number, {
             week_number: w.week_number,
             label: w.label || `Week ${w.week_number}`,
             exposure_summary: normalizeExposure(w.exposure_summary),
             sessions: []
          });
       }
    });
  }

  // Fallback for missing weeks array (infer from sessions)
  sessions.forEach(sess => {
    if (!weeksMap.has(sess.week_number)) {
      weeksMap.set(sess.week_number, {
        week_number: sess.week_number,
        label: `Week ${sess.week_number}`,
        exposure_summary: normalizeExposure({}),
        sessions: []
      });
    }
    weeksMap.get(sess.week_number).sessions.push(sess);
  });

  const weeks = Array.from(weeksMap.values()).sort((a, b) => a.week_number - b.week_number);

  // Normalize rationale/notes
  const rationale: string[] = Array.isArray(raw?.rationale) ? raw.rationale : [];
  const personalization_notes: string[] = Array.isArray(raw?.personalization_notes) ? raw.personalization_notes : [];
  const dropped_constraints: string[] = Array.isArray(raw?.dropped_constraints) ? raw.dropped_constraints : [];
  
  const validation: ValidationNoteVM[] = Array.isArray(raw?.validation) 
    ? raw.validation.map((v: any) => ({
        type: ['info', 'warning', 'error', 'success'].includes(v?.type) ? v.type : 'info',
        message: v?.message || 'Unknown validation note'
      }))
    : [];

  if(!Array.isArray(raw?.sessions) || raw.sessions.length === 0) {
      validation.push({type: 'error', message: 'Transformer Warning: Received zero sessions from backend payload.'});
  }

  const viewModel: ProgramViewModel = {
    metadata,
    summary,
    weeks,
    sessions,
    rationale,
    personalization_notes,
    validation,
    dropped_constraints,
  };

  return { viewModel, warnings, rawPayload: raw };
}
