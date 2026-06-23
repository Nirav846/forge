export interface UATChecklistItem {
  label: string;
  key: string;
}

export interface UATScenario {
  id: string;
  tier: 'core' | 'premium' | 'edge';
  title: string;
  description: string;
  inputs: Record<string, any>;
  checks: UATChecklistItem[];
  passCriteria: string;
}

const SCENARIOS: UATScenario[] = [
  {
    id: 'CORE-01', tier: 'core',
    title: 'General Fitness Adult',
    description: 'Basic core-mode generation for an intermediate general athlete with conditioning goal.',
    inputs: { athlete_name: 'General Adult', sport: 'general', level: 'Intermediate', available_minutes: 60, goal: 'conditioning', mode: 'core' },
    checks: [
      { label: 'Backend returns 200 with valid payload', key: 'status_200' },
      { label: 'Response has metadata, summary, sessions, weeks, rationale, personalization_notes, validation', key: 'has_keys' },
      { label: 'Sessions render in Block Builder view', key: 'builder_renders' },
      { label: 'Coach Summary tab shows rationale text', key: 'summary_shows' },
      { label: 'Right Panel shows Raw API payload', key: 'raw_payload' },
      { label: 'Save artifact succeeds', key: 'save_ok' },
      { label: 'Reloaded artifact matches original', key: 'reload_match' },
    ],
    passCriteria: 'Generates without error, renders in all 3 views, survives save→reload round-trip.',
  },
  {
    id: 'CORE-02', tier: 'core',
    title: 'Youth Athlete',
    description: '16yo rugby beginner — verify youth safety cap prevents Advanced level.',
    inputs: { athlete_name: 'Youth Athlete', sport: 'rugby', level: 'Beginner', age: 16, training_age: 1, available_minutes: 45, goal: 'strength', mode: 'core' },
    checks: [
      { label: 'Program generates at Intermediate level (youth safety cap)', key: 'youth_cap' },
      { label: 'Exercises within difficulty range for level', key: 'diff_ok' },
      { label: 'No more than 6 families per session', key: 'family_limit' },
      { label: 'Coach summary references appropriate level', key: 'summary_ref' },
    ],
    passCriteria: 'Youth generates safe, level-appropriate program. No Advanced-difficulty exercises.',
  },
  {
    id: 'CORE-03', tier: 'core',
    title: 'No Sport Role / Minimal',
    description: 'Empty sport field, all advanced fields left default.',
    inputs: { athlete_name: 'Minimal Athlete', sport: '', level: 'Intermediate', available_minutes: 60, goal: 'strength', mode: 'core' },
    checks: [
      { label: 'Backend accepts empty sport (falls back to "athlete")', key: 'empty_sport' },
      { label: 'Generic blueprint selected', key: 'generic_bp' },
      { label: 'No crash in rationale or personalization view', key: 'rationale_ok' },
      { label: 'Sessions render with valid exercises', key: 'sessions_render' },
    ],
    passCriteria: 'Program generates without error. Sport defaults to "athlete".',
  },
  {
    id: 'CORE-04', tier: 'core',
    title: 'Deload / Maintenance',
    description: 'Days to match = 0 should trigger a recovery/deload program.',
    inputs: { athlete_name: 'Deload Athlete', sport: 'rugby', level: 'Intermediate', days_to_match: 0, available_minutes: 45, goal: 'strength', mode: 'core' },
    checks: [
      { label: 'Summary shows "Recovery" or "Deload" goal', key: 'deload_goal' },
      { label: 'Limited sessions / reduced volume', key: 'reduced_vol' },
      { label: 'Credibility score present', key: 'cred_score' },
    ],
    passCriteria: 'Recovery/deload program generated with appropriate low volume.',
  },
  {
    id: 'PREM-01', tier: 'premium',
    title: 'Rugby Prop (Force Deficit)',
    description: 'Advanced rugby prop with force deficit, right shoulder injury flag.',
    inputs: { athlete_name: 'Rugby Prop', sport: 'rugby', role: 'prop', level: 'Advanced', age: 26, training_age: 6, available_minutes: 50, goal: 'strength', mode: 'premium', force_velocity_profile: 'Force Deficit', injury_flags: ['Right Shoulder'] },
    checks: [
      { label: 'Blueprint appropriate for rugby prop (high force emphasis)', key: 'bp_force' },
      { label: 'Shoulder overhead risk noted in personalization', key: 'shoulder_risk' },
      { label: 'Force-deficit loading bias (lower-rep strength)', key: 'force_bias' },
      { label: 'Coach summary mentions prop role', key: 'prop_role' },
    ],
    passCriteria: 'Emphasizes maximal force, avoids overhead loading, references prop-specific coaching.',
  },
  {
    id: 'PREM-02', tier: 'premium',
    title: 'Rugby Backline (Velocity Deficit)',
    description: 'Advanced rugby backline with velocity deficit, hamstring flag.',
    inputs: { athlete_name: 'Rugby Back', sport: 'rugby', role: 'backline', level: 'Advanced', age: 24, training_age: 4, available_minutes: 60, goal: 'power', mode: 'premium', force_velocity_profile: 'Velocity Deficit', injury_flags: ['Hamstring'] },
    checks: [
      { label: 'Velocity/speed-power emphasis in notes', key: 'velocity_notes' },
      { label: 'Hamstring risk noted — sprint exposure capped', key: 'hstring_risk' },
      { label: 'Backline role mentioned in summary', key: 'backline_role' },
    ],
    passCriteria: 'Balances power work with hamstring-aware sprint dosing.',
  },
  {
    id: 'PREM-03', tier: 'premium',
    title: 'Cricket Fast Bowler',
    description: 'Advanced cricket fast bowler with lumbar and hamstring flags.',
    inputs: { athlete_name: 'Cricket Bowler', sport: 'cricket', role: 'fast_bowler', level: 'Advanced', age: 25, training_age: 5, available_minutes: 55, goal: 'power', mode: 'premium', injury_flags: ['Lumbar Spine', 'Hamstring'] },
    checks: [
      { label: 'Lumbar risk noted — hinge dosing moderated', key: 'lumbar_risk' },
      { label: 'Hamstring risk noted — sprint capped', key: 'hstring_cap' },
      { label: 'Fast bowler role referenced', key: 'bowler_role' },
      { label: 'Rotation exposure moderated per role', key: 'rot_mod' },
    ],
    passCriteria: 'Shows lumbar-aware loading, hamstring protection, bowler-specific notes.',
  },
  {
    id: 'PREM-04', tier: 'premium',
    title: 'Cricket Batter',
    description: 'Intermediate cricket batter, power goal.',
    inputs: { athlete_name: 'Cricket Batter', sport: 'cricket', role: 'batter', level: 'Intermediate', age: 23, training_age: 3, available_minutes: 50, goal: 'power', mode: 'premium' },
    checks: [
      { label: 'Batter role referenced in notes', key: 'batter_ref' },
      { label: 'Rotational emphasis present', key: 'rot_emphasis' },
      { label: 'Upper-body and core work appropriate for batting', key: 'ub_core' },
    ],
    passCriteria: 'References batting role with appropriate movement patterns.',
  },
  {
    id: 'PREM-05', tier: 'premium',
    title: 'Tennis Singles',
    description: 'Advanced tennis singles player, power goal.',
    inputs: { athlete_name: 'Tennis Player', sport: 'tennis', role: 'singles', level: 'Advanced', age: 22, training_age: 4, available_minutes: 50, goal: 'power', mode: 'premium' },
    checks: [
      { label: 'Rotational emphasis noted', key: 'rot_notes' },
      { label: 'Sprint/deceleration work present', key: 'sprint_decel' },
      { label: 'Conditioning density appropriate for tennis', key: 'cond_density' },
    ],
    passCriteria: 'Shows tennis-specific loading with rotational and deceleration focus.',
  },
  {
    id: 'PREM-06', tier: 'premium',
    title: 'Volleyball Middle Blocker',
    description: 'Advanced volleyball MB, poor landing, patellar tendon flag.',
    inputs: { athlete_name: 'Volleyball Player', sport: 'volleyball', role: 'middle_blocker', level: 'Advanced', age: 22, training_age: 4, available_minutes: 60, goal: 'power', mode: 'premium', cmj_band: 'High', landing_competency: 'Poor', injury_flags: ['Patellar Tendon'] },
    checks: [
      { label: 'Jump/landing emphasis in notes', key: 'jump_notes' },
      { label: 'Patellar tendon risk — reactive jump density reduced', key: 'patellar_risk' },
      { label: 'Poor landing competency — plyo sets capped', key: 'landing_cap' },
      { label: 'Middle blocker role referenced', key: 'mb_role' },
    ],
    passCriteria: 'Shows jump-landing work with caps for patellar risk and landing quality.',
  },
  {
    id: 'PREM-07', tier: 'premium',
    title: 'Basketball Guard',
    description: 'Advanced basketball guard, power goal.',
    inputs: { athlete_name: 'Basketball Guard', sport: 'basketball', role: 'guard', level: 'Advanced', age: 24, training_age: 5, available_minutes: 60, goal: 'power', mode: 'premium' },
    checks: [
      { label: 'Guard role referenced', key: 'guard_ref' },
      { label: 'Sprint exposure elevated per role', key: 'sprint_elev' },
      { label: 'Jump/landing work present', key: 'jump_work' },
      { label: 'Deceleration emphasis per role', key: 'decel_emph' },
    ],
    passCriteria: 'Shows basketball-specific loading with guard movement demands.',
  },
  {
    id: 'PREM-08', tier: 'premium',
    title: 'Soccer Midfielder',
    description: 'Advanced soccer midfielder, conditioning goal.',
    inputs: { athlete_name: 'Soccer Midfielder', sport: 'soccer', role: 'midfielder', level: 'Advanced', age: 23, training_age: 4, available_minutes: 60, goal: 'conditioning', mode: 'premium' },
    checks: [
      { label: 'Midfielder role referenced', key: 'mf_ref' },
      { label: 'High conditioning density', key: 'high_cond' },
      { label: 'Sprint exposure elevated', key: 'sprint_mf' },
      { label: 'Deceleration emphasis present', key: 'decel_mf' },
    ],
    passCriteria: 'Shows soccer-specific conditioning with midfielder running demands.',
  },
  {
    id: 'EDGE-01', tier: 'edge',
    title: 'Very Short Session (20 min)',
    description: 'Only 20 minutes available — should reduce families and duration.',
    inputs: { athlete_name: 'Short Session', available_minutes: 20, goal: 'strength', mode: 'core' },
    checks: [
      { label: 'Program generates with reduced families (≤4)', key: 'reduced_fams' },
      { label: 'Sessions are shorter but coherent', key: 'short_coherent' },
      { label: 'No crash in any view', key: 'no_crash' },
    ],
    passCriteria: 'Generates shorter but coherent sessions.',
  },
  {
    id: 'EDGE-02', tier: 'edge',
    title: 'Competition Taper (D2M=3)',
    description: '3 days to match should produce taper program.',
    inputs: { athlete_name: 'Taper', days_to_match: 3, goal: 'power', mode: 'core' },
    checks: [
      { label: 'Summary mentions "taper"', key: 'taper_ref' },
      { label: 'Sessions show reduced volume', key: 'reduced_vol' },
      { label: 'Credibility score still present', key: 'cred_ok' },
    ],
    passCriteria: 'Taper-summary mentions taper, sessions show reduced volume.',
  },
  {
    id: 'EDGE-03', tier: 'edge',
    title: 'Multiple Injury Flags',
    description: 'Four simultaneous injury flags.',
    inputs: { athlete_name: 'Injured Athlete', injury_flags: ['Lumbar Spine', 'Hamstring', 'Patellar Tendon', 'Right Shoulder'], goal: 'strength', mode: 'premium' },
    checks: [
      { label: 'All risk flags reflected in personalization notes', key: 'all_flags' },
      { label: 'Program generates without error', key: 'gen_ok' },
      { label: 'Notes mention lumbar, hamstring, patellar, shoulder', key: 'notes_mention' },
    ],
    passCriteria: 'All risk flags reflected, program generates without error.',
  },
  {
    id: 'EDGE-04', tier: 'edge',
    title: 'Missing Optional Fields',
    description: 'Only athlete name set, everything else empty/default.',
    inputs: { athlete_name: 'Minimal' },
    checks: [
      { label: 'Backend accepts', key: 'backend_accepts' },
      { label: 'Program generates', key: 'program_gen' },
      { label: 'No crash in any UI view', key: 'no_ui_crash' },
      { label: 'Save succeeds', key: 'save_ok' },
    ],
    passCriteria: 'Backend accepts minimal payload, program generates, no crash anywhere.',
  },
];

export function getAllScenarios(): UATScenario[] {
  return SCENARIOS;
}

export function getScenariosByTier(tier: 'core' | 'premium' | 'edge'): UATScenario[] {
  return SCENARIOS.filter(s => s.tier === tier);
}

const STORAGE_KEY = 'forge_uat_results';

export function loadResults(): Record<string, Record<string, boolean | string>> {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
  } catch { return {}; }
}

export function saveResult(scenarioId: string, key: string, passed: boolean): void {
  const all = loadResults();
  if (!all[scenarioId]) all[scenarioId] = {};
  all[scenarioId][key] = passed;
  all[scenarioId]['_updated'] = new Date().toISOString();
  localStorage.setItem(STORAGE_KEY, JSON.stringify(all));
}

export function resetResults(): void {
  localStorage.removeItem(STORAGE_KEY);
}

export interface UATExportPayload {
  exported_at: string;
  summary: { total_scenarios: number; total_checks: number; passed: number; failed: number; unchecked: number; };
  scenarios: {
    id: string;
    title: string;
    tier: string;
    checks: { label: string; key: string; result: boolean | null; }[];
    pass_criteria: string;
    all_passed: boolean;
  }[];
}

export function exportResultsAsJSON(): UATExportPayload {
  const results = loadResults();
  const scenarios = getAllScenarios();
  let totalChecks = 0;
  let passed = 0;
  let failed = 0;

  const scenarioData = scenarios.map(s => {
    const r = (results[s.id] || {}) as Record<string, boolean>;
    const checks = s.checks.map(c => {
      const val = r[c.key] ?? null;
      if (val === true) passed++;
      else if (val === false) failed++;
      totalChecks++;
      return { label: c.label, key: c.key, result: val };
    });
    const allPassed = checks.every(c => c.result === true);
    return { id: s.id, title: s.title, tier: s.tier, checks, pass_criteria: s.passCriteria, all_passed: allPassed };
  });

  return {
    exported_at: new Date().toISOString(),
    summary: {
      total_scenarios: scenarios.length,
      total_checks: totalChecks,
      passed,
      failed,
      unchecked: totalChecks - passed - failed,
    },
    scenarios: scenarioData,
  };
}

export function downloadUATResults(): void {
  const data = exportResultsAsJSON();
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `forge_uat_results_${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
  URL.revokeObjectURL(url);
}
