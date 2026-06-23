import { ProgramRequest } from '../types';

export type FieldMode = 'core' | 'premium';

/**
 * Formal definition of which fields belong to which mode.
 * core: Visible in all modes
 * premium: Visible only in advanced mode
 */
export const FieldModeConfig = {
  basics: {
    athlete_name: 'core' as FieldMode,
    sport: 'core' as FieldMode,
    role: 'core' as FieldMode,
    age: 'core' as FieldMode,
    level: 'core' as FieldMode,
    frequency_per_week: 'core' as FieldMode,
    available_minutes: 'core' as FieldMode,
    // Advanced/Peripheral inputs below
    sex: 'premium' as FieldMode,
    training_age_years: 'premium' as FieldMode,
    environment: 'premium' as FieldMode,
    days_to_match: 'premium' as FieldMode,
  },
  context: {
    primary_goal: 'core' as FieldMode,
    competition_proximity_note: 'premium' as FieldMode,
    current_phase: 'premium' as FieldMode,
    equipment_profile: 'premium' as FieldMode,
  },
  advanced: 'premium' as FieldMode
};

export function isFieldVisible(mode: FieldMode, section: keyof typeof FieldModeConfig, field?: string): boolean {
  if (mode === 'premium') return true; 
  if (section === 'advanced') return false; 

  if (section === 'basics' && field) {
    return FieldModeConfig.basics[field as keyof typeof FieldModeConfig.basics] === 'core';
  }
  if (section === 'context' && field) {
    return FieldModeConfig.context[field as keyof typeof FieldModeConfig.context] === 'core';
  }
  
  return true;
}
