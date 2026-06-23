import { ProgramRequest } from '../types';

export const mockScenarios: Record<string, Partial<ProgramRequest>> = {
  rugby_prop: {
    mode: 'premium',
    basics: {
      athlete_name: 'Big Tom', age: 28, sex: 'Male', sport: 'Rugby Union', role: 'Tighthead Prop',
      training_age_years: 8, level: 'Advanced', environment: 'Pro Facility', available_minutes: 60,
      frequency_per_week: 4, days_to_match: 6,
    },
    context: {
      primary_goal: 'Max Force & Scrum Dominance', current_phase: 'In-Season',
      equipment_profile: ['Full Gym', 'Bands', 'Chains', 'Prowler'],
      competition_proximity_note: 'Match day Saturday. Need high force, low fatigue late in week.',
    },
    advanced: {
      force_velocity_profile: 'Force Deficit', sprint_10m_band: '1.80s+', aerobic_band: 'Moderate',
      squat_strength_band: 'Elite (>2.0x BW)', cmj_band: 'Average', technique_consistency: 'High',
      injury_risk_flags: ['Neck', 'Lower Back'], prior_block_summary: 'Responded well to cluster sets.',
    }
  },
  tennis_singles: {
    mode: 'premium',
    basics: {
      athlete_name: 'Elena S.', age: 24, sex: 'Female', sport: 'Tennis', role: 'Singles Player',
      training_age_years: 5, level: 'Advanced', environment: 'Commercial Gym', available_minutes: 45,
      frequency_per_week: 3, days_to_match: 14,
    },
    context: {
      primary_goal: 'Court Speed & Change of Direction', current_phase: 'Pre-Season (Late)',
      equipment_profile: ['Dumbbells', 'Kettlebells', 'Cable Machine', 'Medicine Balls'],
      competition_proximity_note: 'Tournament starts in 2 weeks. Tapering volume.',
    },
    advanced: {
      force_velocity_profile: 'Velocity Deficit', sprint_10m_band: '<1.65s', aerobic_band: 'Elite',
      squat_strength_band: 'Solid (1.5x BW)', cmj_band: 'High', technique_consistency: 'Medium',
      injury_risk_flags: ['Right Shoulder', 'Left Ankle'], prior_block_summary: 'Needs more core rotational power.',
    }
  },
  cricket_bowler: {
    mode: 'premium',
    basics: {
      athlete_name: 'Jasprit K.', age: 26, sex: 'Male', sport: 'Cricket', role: 'Fast Bowler',
      training_age_years: 6, level: 'Intermediate', environment: 'Field/Track', available_minutes: 90,
      frequency_per_week: 3, days_to_match: 5,
    },
    context: {
      primary_goal: 'Eccentric Tolerance & Delivery Velocity', current_phase: 'In-Season',
      equipment_profile: ['Basic Weights', 'Bands', 'Medicine Balls'],
      competition_proximity_note: 'Bowling 10 overs on Sunday.',
    },
    advanced: {
      force_velocity_profile: 'Balanced', sprint_10m_band: '1.70s', aerobic_band: 'High',
      squat_strength_band: 'Average (1.2x BW)', cmj_band: 'Moderate', technique_consistency: 'Medium',
      injury_risk_flags: ['Lumbar Spine', 'Hamstring string'], prior_block_summary: 'Struggled with high volume deadlifts.',
    }
  }
};

export const defaultEmptyRequest: ProgramRequest = {
  mode: 'core',
  basics: {
    athlete_name: '', age: '', sex: '', sport: '', role: '',
    training_age_years: '', level: 'Intermediate', environment: '',
    available_minutes: 60, frequency_per_week: 3, days_to_match: '',
  },
  context: {
    primary_goal: '', current_phase: '', equipment_profile: [], competition_proximity_note: '',
  },
  advanced: {
    force_velocity_profile: '', sprint_10m_band: '', aerobic_band: '', squat_strength_band: '',
    cmj_band: '', technique_consistency: '', injury_risk_flags: [], prior_block_summary: '',
  }
};

// Fixtures mimicking raw backend responses before normalization
export const mockBackendResponses: Record<string, any> = {
  base: {
    metadata: { generated_at: new Date().toISOString(), request_id: `req_${Math.random().toString(36).substring(7)}`, api_version: '1.0.0' },
    summary: { blueprint_selected: 'General Athletic Development', total_weeks: 4, weekly_frequency: 3, conditioning_emphasis: 'Maintenance', competition_window: 'Off-season', role_emphasis: 'General Physical Preparedness' },
    rationale: ['Selected General Athletic blueprint due to incomplete profile.'],
    personalization_notes: ['Ensure technique is standardized before adding progression.'],
    validation: [{ type: 'warning', message: 'Low data definition: Falling back to general blueprint.' }],
    dropped_constraints: ['Advanced force profiling skipped due to missing data.'],
    sessions: [
      { id: 's1', name: 'Full Body A', week_number: 1, session_number: 1, focus: 'Neural Drive & Structural Balance',
        warmup: { title: 'Movement Prep', exercises: [{ id: 'w1', name: 'Cat-Cow', family: 'Mobility', sets_reps: '2 x 8', loading_method: 'BW', rest: '0s' }, { id: 'w2', name: 'Pogo Jumps', family: 'Plyo', sets_reps: '2 x 15', loading_method: 'BW', rest: '30s' }] },
        main_work: { title: 'Primary Lifts', exercises: [{ id: 'm1', name: 'Goblet Squat', family: 'Squat', sets_reps: '3 x 8', loading_method: 'RPE 7', rest: '90s', coach_note: 'Focus on depth.' }, { id: 'm2', name: 'DB Romanian Deadlift', family: 'Hinge', sets_reps: '3 x 10', loading_method: 'RPE 7', rest: '90s' }] } }
    ]
  },
  rugby_prop: {
    metadata: { generated_at: new Date().toISOString(), request_id: 'req_123', api_version: '1.0.0' },
    summary: { blueprint_selected: 'Elite Collision Profile: Front Row', total_weeks: 4, weekly_frequency: 4, conditioning_emphasis: 'Maintenance', competition_window: '6 days out', role_emphasis: 'Maximal Force / Neck & Core Rigidity' },
    rationale: ['Blueprint [Elite Collision] selected based on Rugby + Tighthead Prop role.', 'Prioritizing heavy isometrics for scrum stability based on advanced profile.'],
    validation: [{ type: 'success', message: 'Equipment profile supports required heavy loading.' }, { type: 'info', message: 'Volume compressed to fit 60 min session time constraint.' }],
    personalization_notes: ['Neck injury flag detected: Swapped dynamic neck flexion for static multi-directional holds.'],
    sessions: [
      { id: 'r_s1', name: 'Heavy Isometric & Scrum Stability', week_number: 1, session_number: 1, focus: 'Max Force Generation',
        warmup: { title: 'Specific Prep: Collision Readiness', exercises: [{ id: 'rw1', name: 'Isometric Neck Holds', family: 'Neck Stability', sets_reps: '3 x 10s', loading_method: 'Partner Resisted', rest: '30s', coach_note: 'Crucial based on injury flag.' }, { id: 'rw2', name: 'Bear Crawls', family: 'Core', sets_reps: '2 x 15m', loading_method: 'BW', rest: '45s' }] },
        main_work: { title: 'Absolute Force', exercises: [{ id: 'rm1', name: 'Safety Bar Box Squat', family: 'Squat', sets_reps: '4 x 4', loading_method: '85% 1RM', rest: '180s', progression_note: 'Cluster sets applied per prior block response.' }, { id: 'rm2', name: 'Heavy Sled Push (Low)', family: 'Locomotion', sets_reps: '4 x 10m', loading_method: 'Max Weight', rest: '120s', coach_note: 'Mimic scrum posture.' }, { id: 'rm3', name: 'Zercher Hold', family: 'Anterior Core', sets_reps: '3 x 20s', loading_method: 'RPE 8', rest: '90s' }] } },
      { id: 'r_s2', name: 'Upper Body Armor', week_number: 1, session_number: 2, focus: 'Hypertrophy & Durability',
        warmup: { title: 'Shoulder Prep', exercises: [{ id: 'rw3', name: 'Band Pull-Aparts', family: 'Pre-hab', sets_reps: '3 x 20', loading_method: 'Mini Band', rest: '30s' }] },
        main_work: { title: 'Upper Primary', exercises: [{ id: 'rm4', name: 'Floor Press', family: 'Horizontal Push', sets_reps: '4 x 6', loading_method: 'RPE 8', rest: '120s' }, { id: 'rm5', name: 'Pendlay Row', family: 'Horizontal Pull', sets_reps: '4 x 8', loading_method: 'RPE 8', rest: '120s' }] } }
    ]
  },
  tennis_singles: {
    metadata: { generated_at: new Date().toISOString(), request_id: 'req_456', api_version: '1.0.0' },
    summary: { blueprint_selected: 'Court Speed & Multi-Directional Power', total_weeks: 4, weekly_frequency: 3, conditioning_emphasis: 'Alactic Power / Repeat Sprint', competition_window: '14 days out', role_emphasis: 'Velocity, Rotation, Change of Direction' },
    rationale: ['Blueprint [Court Speed] selected for Tennis Singles.', 'Reduced total axial loading to accommodate Late Pre-season status.'],
    validation: [{ type: 'warning', message: 'No barbell selected. Re-mapping heavy bilateral lifts to DB/KB equivalents.' }],
    personalization_notes: ['Right shoulder injury flag: Replaced overhead pressing with landmine variations.', 'Velocity deficit noted: Emphasizing medicine ball throws and band-assisted jumps.'],
    sessions: [
      { id: 't_s1', name: 'Rotational Power & Speed', week_number: 1, session_number: 1, focus: 'Velocity & Change of Direction',
        warmup: { title: 'Dynamic ROM & Elasticity', exercises: [{ id: 'tw1', name: 'Ankle Hops', family: 'Plyo', sets_reps: '3 x 15', loading_method: 'BW', rest: '30s' }, { id: 'tw2', name: 'Lateral Lunge', family: 'Mobility', sets_reps: '2 x 8/side', loading_method: 'BW', rest: '45s' }] },
        main_work: { title: 'Power Development', exercises: [{ id: 'tm1', name: 'Rotational Med Ball Throw', family: 'Power', sets_reps: '4 x 4/side', loading_method: '3kg MB', rest: '90s', coach_note: 'Max intent on every throw.' }, { id: 'tm2', name: 'Rear Foot Elevated Split Squat', family: 'Unilateral Leg', sets_reps: '3 x 6/side', loading_method: 'DB RPE 7', rest: '90s' }, { id: 'tm3', name: 'Landmine Press', family: 'Push', sets_reps: '3 x 8/side', loading_method: 'RPE 7.5', rest: '90s', progression_note: 'Substituted for OH Press due to shoulder flag.' }] },
        conditioning: { title: 'Court Specific Energy Systems', exercises: [{ id: 'tc1', name: 'Spider Drill', family: 'Agility', sets_reps: '4 x 1', loading_method: 'Max Speed', rest: '60s' }] } }
    ]
  },
  cricket_bowler: {
    metadata: { generated_at: new Date().toISOString(), request_id: 'req_789', api_version: '1.0.0' },
    summary: { blueprint_selected: 'Fast Bowler Eccentric Tolerance', total_weeks: 4, weekly_frequency: 3, conditioning_emphasis: 'Aerobic Base', competition_window: '5 days out', role_emphasis: 'Anterior Core, Hamstring Robustness, Delivery Force' },
    rationale: ['Blueprint [Fast Bowler] selected based on role.', 'Focusing heavily on landing leg eccentric control.'],
    validation: [{ type: 'warning', message: 'Lumbar spine flag: Avoiding heavy end-range flexion.' }, { type: 'success', message: 'Field/Track environment ideal for requisite running loads.' }],
    personalization_notes: ['Hamstring flag: Added specific isometric holds prior to eccentric lengthening.'],
    sessions: [
      { id: 'c_s1', name: 'Braking Force & Core Stiffness', week_number: 1, session_number: 1, focus: 'Eccentric Load Acceptance',
        warmup: { title: 'Pillar Prep', exercises: [{ id: 'cw1', name: 'McGill Curl Up', family: 'Core', sets_reps: '3 x 5 (10s hold)', loading_method: 'BW', rest: '30s', coach_note: 'Protect the lumbar spine.' }, { id: 'cw2', name: 'Supine Hamstring Isometric', family: 'Activation', sets_reps: '3 x 15s/side', loading_method: 'BW', rest: '45s' }] },
        main_work: { title: 'Deceleration Lifts', exercises: [{ id: 'cm1', name: 'Drop Lunge', family: 'Deceleration', sets_reps: '3 x 5/side', loading_method: 'BW', rest: '60s', coach_note: 'Focus on stiff landing.' }, { id: 'cm2', name: 'Nordic Hamstring Curl', family: 'Eccentric', sets_reps: '3 x 4', loading_method: 'BW', rest: '120s' }, { id: 'cm3', name: 'Paloff Press', family: 'Anti-Rotation', sets_reps: '3 x 10', loading_method: 'Band', rest: '60s' }] } }
    ]
  },
  malformed_fake_error: {
    // Missing metadata, missing sections, messed up exercises
    summary: { blueprint_selected: 'Broken Response Schema Test' },
    sessions: [
      { name: 'Broken Session', main_work: { exercises: [{ name: 'Just a name' }] } }
    ]
  }
};
