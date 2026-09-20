import type { ProgramRequest } from '../types';

export interface DiffChange {
  id: string;
  section: 'basics' | 'context' | 'advanced';
  field: string;
  label: string;
  oldValue: any;
  newValue: any;
  path: string[];
  accepted: boolean;
}

const FIELD_LABELS: Record<string, string> = {
  athlete_name: 'Name', sport: 'Sport', role: 'Role', level: 'Level',
  age: 'Age', training_age_years: 'Training Age', available_minutes: 'Min/Session',
  frequency_per_week: 'Sessions/Week', days_to_match: 'Days to Match',
  primary_goal: 'Goal', current_phase: 'Phase', equipment_profile: 'Equipment',
  competition_proximity_note: 'Coach Intent', program_length_weeks: 'Length (Weeks)',
  match_day: 'Match Day', team_training_days: 'Training Days',
  heavy_field_days: 'Heavy Days', travel_days: 'Travel Days',
  injury_severity: 'Injury Severity',
  injury_risk_flags: 'Injury Flags', cmj_band: 'CMJ',
  force_velocity_profile: 'F-V Profile', sprint_10m_band: 'Sprint 10m',
  aerobic_band: 'Aerobic', squat_strength_band: 'Squat',
  technique_consistency: 'Technique', prior_block_summary: 'Prior Block',
  yoyo_ir1: 'Yo-Yo IR1', yoyo_ir2: 'Yo-Yo IR2', bronco: 'Bronco',
};

function fmt(val: any): string {
  if (val === null || val === undefined || val === '') return '(empty)';
  if (Array.isArray(val)) return val.length ? val.join(', ') : '(empty)';
  return String(val);
}

export function diffRequests(source: ProgramRequest, current: ProgramRequest): DiffChange[] {
  const changes: DiffChange[] = [];

  for (const section of ['basics', 'context', 'advanced'] as const) {
    const src = (source as any)[section] || {};
    const cur = (current as any)[section] || {};
    const allKeys = new Set([...Object.keys(src), ...Object.keys(cur)]);

    for (const key of allKeys) {
      const oldVal = key in src ? src[key] : undefined;
      const newVal = key in cur ? cur[key] : undefined;
      const oldStr = fmt(oldVal);
      const newStr = fmt(newVal);
      if (oldStr !== newStr) {
        changes.push({
          id: `${section}.${key}`,
          section,
          field: key,
          label: FIELD_LABELS[key] || key,
          oldValue: oldVal,
          newValue: newVal,
          path: [section, key],
          accepted: true,
        });
      }
    }
  }

  return changes;
}
