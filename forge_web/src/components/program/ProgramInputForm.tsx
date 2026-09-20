import React, { useState, useEffect, useMemo } from 'react';
import {
  User, Target, Calendar, Dumbbell, FileText, ChevronDown, ChevronRight,
  AlertCircle, Zap, Play, ArrowLeft, Activity, Clock, MapPin, Shield,
  Plus, X, BarChart3, BookOpen, Settings
} from 'lucide-react';
import { ProgramRequest, Mode } from '../../types';
import { RawProgramRequest, CoachPreferences } from '../../types/api';
import { TransformationResult } from '../../types/ui';
import { generateProgram as apiGenerate } from '../../lib/api';
import { generateProgramMock } from '../../lib/mockApi';
import { normalizeProgramResponse } from '../../lib/transformers';
import { loadArtifact as apiLoad } from '../../lib/api';
import { getRoleProfile, RoleProfile, roleProfiles } from '../../data/roleProfiles';
import { SPORT_OPTIONS } from '../../data/sportList';
import CoachPreferencesModal, { loadPreferences } from './CoachPreferencesModal';
import { ReviewChangesPanel } from './ReviewChangesPanel';
import { diffRequests } from '../../lib/adaptationDiff';

const DAYS = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'] as const;
const PHASES = ['Off-season','Pre-season','In-Season','Taper','Return-to-play'] as const;
const GOALS = ['Max Strength','Speed','Power','Hypertrophy','Maintenance'] as const;
const LEVELS = ['Beginner','Intermediate','Advanced'] as const;
const EQUIPMENT_OPTIONS = ['Full Gym','Barbell+rack','DB+KB','Bands','Bodyweight','Field only'] as const;
const INJURY_SEVERITY = ['None','Mild','Moderate','Severe'] as const;

interface ProgramInputFormProps {
  sourceProgramId?: string;
  templateValues?: Partial<ProgramRequest>;
  onProgramGenerated?: (result: TransformationResult, request: ProgramRequest) => void;
  onBack?: () => void;
}

interface FormState {
  athlete_name: string;
  sport: string;
  role: string;
  level: string;
  age: number | '';
  training_age_years: number | '';
  phase: string;
  goal: string;
  program_length_weeks: number;
  sessions_per_week: number;
  minutes_per_session: number;
  match_day: string;
  team_training_days: string[];
  heavy_field_days: string[];
  travel_days: string[];
  equipment: string[];
  injury_flags: string[];
  injury_severity: string;
  coach_intent: string;
  yoyo_ir1: string;
  yoyo_ir2: string;
  bronco: string;
  cmj_band: string;
}

const INITIAL: FormState = {
  athlete_name: '', sport: '', role: '', level: 'Intermediate',
  age: '', training_age_years: '',
  phase: '', goal: '', program_length_weeks: 4, sessions_per_week: 3, minutes_per_session: 60,
  match_day: '', team_training_days: [], heavy_field_days: [], travel_days: [],
  equipment: [], injury_flags: [], injury_severity: 'None',
  coach_intent: '',
  yoyo_ir1: '', yoyo_ir2: '', bronco: '', cmj_band: '',
};

function toggleDay(days: string[], day: string): string[] {
  return days.includes(day) ? days.filter(d => d !== day) : [...days, day];
}

function buildRequest(state: FormState, mode: Mode): ProgramRequest {
  const prefs = loadPreferences();
  const hasPrefs = Object.values(prefs).some(v => v !== undefined && v !== false && v !== '' && !(typeof v === 'number' && v === 90));
  return {
    mode,
    basics: {
      athlete_name: state.athlete_name,
      sport: state.sport,
      role: state.role,
      level: state.level as any,
      age: state.age,
      training_age_years: state.training_age_years,
      frequency_per_week: state.sessions_per_week,
      available_minutes: state.minutes_per_session,
    },
    context: {
      primary_goal: state.goal,
      current_phase: state.phase,
      equipment_profile: state.equipment,
      competition_proximity_note: state.coach_intent,
      program_length_weeks: state.program_length_weeks,
      match_day: state.match_day,
      team_training_days: state.team_training_days,
      heavy_field_days: state.heavy_field_days,
      travel_days: state.travel_days,
      coach_intent: state.coach_intent,
      injury_severity: state.injury_severity as any,
    },
    advanced: {
      injury_risk_flags: state.injury_flags,
      yoyo_ir1: state.yoyo_ir1,
      yoyo_ir2: state.yoyo_ir2,
      bronco: state.bronco,
      cmj_band: state.cmj_band,
    },
    coach_preferences: hasPrefs ? prefs : undefined,
  };
}

function applySnapshot(state: FormState, snapshot: any): FormState {
  const b = snapshot?.basics || {};
  const c = snapshot?.context || {};
  const a = snapshot?.advanced || {};
  return {
    ...state,
    athlete_name: b.athlete_name || '',
    sport: b.sport || '',
    role: b.role || '',
    level: b.level || 'Intermediate',
    age: b.age ?? '',
    training_age_years: b.training_age_years ?? '',
    phase: c.current_phase || '',
    goal: c.primary_goal || '',
    program_length_weeks: c.program_length_weeks ?? 4,
    sessions_per_week: b.frequency_per_week ?? 3,
    minutes_per_session: b.available_minutes ?? 60,
    match_day: c.match_day || '',
    team_training_days: c.team_training_days || [],
    heavy_field_days: c.heavy_field_days || [],
    travel_days: c.travel_days || [],
    equipment: c.equipment_profile || [],
    injury_flags: a.injury_risk_flags || [],
    injury_severity: c.injury_severity || 'None',
    coach_intent: c.coach_intent || '',
    yoyo_ir1: a.yoyo_ir1 || '',
    yoyo_ir2: a.yoyo_ir2 || '',
    bronco: a.bronco || '',
    cmj_band: a.cmj_band || '',
  };
}

function applyTemplate(state: FormState, template: Partial<ProgramRequest>): FormState {
  return applySnapshot(state, {
    basics: template.basics || {},
    context: template.context || {},
    advanced: template.advanced || {},
  });
}

export default function ProgramInputForm({ sourceProgramId, templateValues, onProgramGenerated, onBack }: ProgramInputFormProps) {
  const [f, setF] = useState<FormState>(INITIAL);
  const [mode, setMode] = useState<Mode>('core');
  const [status, setStatus] = useState<'idle' | 'loading' | 'error'>('idle');
  const [error, setError] = useState<string | null>(null);
  const [roleOpen, setRoleOpen] = useState(false);
  const [perfOpen, setPerfOpen] = useState(false);
  const [prefsOpen, setPrefsOpen] = useState(false);
  const [loadingSource, setLoadingSource] = useState(false);

  const [customSport, setCustomSport] = useState('');
  const [sourceRequest, setSourceRequest] = useState<ProgramRequest | null>(null);
  const [reviewOpen, setReviewOpen] = useState(false);
  const [rejectedChangeIds, setRejectedChangeIds] = useState<Set<string>>(new Set());

  useEffect(() => {
    if (templateValues) {
      const next = applyTemplate(INITIAL, templateValues);
      if (next.sport && !SPORT_OPTIONS.includes(next.sport)) {
        setCustomSport(next.sport);
        next.sport = 'Other';
      }
      setF(next);
    }
  }, []);

  useEffect(() => {
    if (!sourceProgramId) return;
    setLoadingSource(true);
    (async () => {
      try {
        const artifact = await apiLoad(sourceProgramId);
        setSourceRequest(artifact.request_snapshot);
        setRejectedChangeIds(new Set());
        const next = applySnapshot(INITIAL, artifact.request_snapshot);
        if (next.sport && !SPORT_OPTIONS.includes(next.sport)) {
          setCustomSport(next.sport);
          next.sport = 'Other';
        }
        setF(next);
      } catch {
        // ponytail: try mock fallback
      } finally {
        setLoadingSource(false);
      }
    })();
  }, [sourceProgramId]);

  const profile: RoleProfile | undefined = useMemo(
    () => getRoleProfile(f.sport, f.role),
    [f.sport, f.role]
  );

  useEffect(() => {
    if (profile && profile.sport !== '*') {
      setF(prev => ({
        ...prev,
        phase: prev.phase || '',
        sessions_per_week: prev.sessions_per_week || 3,
        minutes_per_session: prev.minutes_per_session || 60,
        equipment: prev.equipment.length ? prev.equipment : [],
      }));
    }
  }, [profile]);

  const update = (field: keyof FormState, value: any) => setF(prev => ({ ...prev, [field]: value }));

  const addInjuryFlag = (flag: string) => {
    const trimmed = flag.trim();
    if (trimmed && !f.injury_flags.includes(trimmed)) {
      setF(prev => ({ ...prev, injury_flags: [...prev.injury_flags, trimmed] }));
    }
  };

  const errors = useMemo(() => {
    const e: string[] = [];
    if (!f.athlete_name.trim()) e.push('Athlete name is required');
    if (f.age !== '' && (Number(f.age) < 0 || Number(f.age) > 120)) e.push('Age must be 0–120');
    if (f.training_age_years !== '' && (Number(f.training_age_years) < 0 || Number(f.training_age_years) > 50)) e.push('Training age must be 0–50');
    if (f.program_length_weeks < 1 || f.program_length_weeks > 52) e.push('Program length must be 1–52 weeks');
    if (f.sessions_per_week < 1 || f.sessions_per_week > 7) e.push('Sessions per week must be 1–7');
    if (f.minutes_per_session < 10 || f.minutes_per_session > 240) e.push('Minutes per session must be 10–240');
    return e;
  }, [f]);

  const handleToggleChange = (changeId: string) => {
    setRejectedChangeIds(prev => {
      const next = new Set(prev);
      if (next.has(changeId)) next.delete(changeId); else next.add(changeId);
      return next;
    });
  };

  const handleSubmit = async () => {
    if (errors.length) return;
    setStatus('loading');
    setError(null);
    try {
      let request = buildRequest({ ...f, sport: f.sport === 'Other' ? customSport : f.sport }, mode);
      // Apply rejected changes: override to source values
      if (sourceRequest && rejectedChangeIds.size > 0) {
        const allChanges = diffRequests(sourceRequest, request);
        for (const change of allChanges) {
          if (rejectedChangeIds.has(change.id)) {
            request = {
              ...request,
              [change.path[0] as 'basics' | 'context' | 'advanced']: {
                ...(request as any)[change.path[0]],
                [change.field]: change.oldValue,
              },
            };
          }
        }
      }
      let rawPayload: any;
      try {
        rawPayload = await apiGenerate(request);
      } catch {
        rawPayload = await generateProgramMock(request);
      }
      const transformed = normalizeProgramResponse(rawPayload);
      onProgramGenerated?.(transformed, request);
    } catch (err: any) {
      setError(err.message || 'Generation failed');
      setStatus('error');
    }
  };

  const selCls = (active: boolean) =>
    `px-3 py-1.5 text-xs font-medium rounded-md border transition-all cursor-pointer ${
      active
        ? 'bg-indigo-50 border-indigo-300 text-indigo-700'
        : 'bg-white border-slate-200 text-slate-600 hover:border-slate-300'
    }`;

  const inputCls = (hasError?: boolean) =>
    `w-full px-3 py-2 text-sm rounded-md border transition-all focus:outline-none focus:ring-2 ${
      hasError
        ? 'bg-red-50 border-red-300 focus:ring-red-500/20'
        : 'bg-white border-slate-200 focus:ring-indigo-500/20 focus:border-indigo-300'
    }`;

  const labelCls = 'block text-xs font-medium text-slate-700 mb-1';

  if (loadingSource) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="w-8 h-8 border-4 border-slate-200 border-t-indigo-600 rounded-full animate-spin" />
        <span className="ml-3 text-sm text-slate-500">Loading source program...</span>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col bg-slate-50">
      <div className="flex-none px-6 py-4 bg-white border-b border-slate-200 flex items-center gap-4">
        {onBack && (
          <button onClick={onBack} className="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition-colors">
            <ArrowLeft className="w-5 h-5" />
          </button>
        )}
        <div>
          <h2 className="text-lg font-bold text-slate-900">Program Builder</h2>
          <p className="text-xs text-slate-500">Fill in athlete details & training parameters</p>
        </div>
        <div className="ml-auto flex items-center gap-3">
          <div className="flex bg-slate-100 p-0.5 rounded-lg">
            <button onClick={() => setMode('core')} className={`px-3 py-1.5 text-xs font-medium rounded-md transition-all ${mode === 'core' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500'}`}>Core</button>
            <button onClick={() => setMode('premium')} className={`px-3 py-1.5 text-xs font-medium rounded-md transition-all ${mode === 'premium' ? 'bg-indigo-50 text-indigo-700 shadow-sm' : 'text-slate-500'}`}>Premium</button>
          </div>
          <button onClick={() => setPrefsOpen(true)} className="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-lg transition-colors" title="Coach Preferences">
            <Settings className="w-4 h-4" />
          </button>
          <button
            onClick={handleSubmit}
            disabled={status === 'loading' || errors.length > 0}
            className="flex items-center gap-2 px-5 py-2 bg-slate-900 hover:bg-slate-800 disabled:bg-slate-300 disabled:cursor-not-allowed text-white rounded-lg text-sm font-medium transition-colors"
          >
            {status === 'loading' ? <Zap className="w-4 h-4 animate-pulse" /> : <Play className="w-4 h-4" />}
            {status === 'loading' ? 'Generating...' : 'Generate Program'}
          </button>
        </div>
      </div>

      {errors.length > 0 && (
        <div className="flex-none mx-6 mt-3 flex items-center gap-1.5 text-xs text-red-600 bg-red-50 px-3 py-2 rounded-lg border border-red-200">
          <AlertCircle className="w-3.5 h-3.5 shrink-0" />
          <span>{errors.length} validation error{errors.length !== 1 ? 's' : ''}</span>
        </div>
      )}
      {status === 'error' && error && (
        <div className="flex-none mx-6 mt-3 flex items-center gap-1.5 text-xs text-red-600 bg-red-50 px-3 py-2 rounded-lg border border-red-200">
          <AlertCircle className="w-3.5 h-3.5 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {sourceRequest && (
        <div className="flex-none mx-6 mt-3">
          <button
            onClick={() => setReviewOpen(!reviewOpen)}
            className="flex items-center gap-2 text-xs font-semibold text-amber-700 bg-amber-50 border border-amber-200 hover:bg-amber-100 px-3 py-2 rounded-lg transition-colors w-full"
          >
            <ChevronDown className={`w-3.5 h-3.5 transition-transform ${reviewOpen ? 'rotate-180' : ''}`} />
            Review Changes from Source
          </button>
          {reviewOpen && (
            <div className="mt-2">
              <ReviewChangesPanel
                sourceRequest={sourceRequest}
                currentRequest={buildRequest({ ...f, sport: f.sport === 'Other' ? customSport : f.sport }, mode)}
                onToggleChange={handleToggleChange}
                rejectedChangeIds={rejectedChangeIds}
              />
            </div>
          )}
        </div>
      )}

      <div className="flex-1 overflow-y-auto px-6 py-6 space-y-8">
        {/* Section 1: Athlete Context */}
        <section className="bg-white rounded-xl border border-slate-200 p-5 space-y-4 shadow-sm">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <User className="w-3.5 h-3.5" /> Athlete Context
          </h3>
          <div className="grid grid-cols-2 gap-4">
            <div className="col-span-2">
              <label className={labelCls}>Name *</label>
              <input type="text" value={f.athlete_name} onChange={e => update('athlete_name', e.target.value)}
                className={inputCls(!f.athlete_name.trim())} placeholder="Athlete name" />
            </div>
            <div>
              <label className={labelCls}>Sport</label>
              <select value={!f.sport ? '' : (SPORT_OPTIONS.includes(f.sport) ? f.sport : 'Other')}
                onChange={e => {
                  const val = e.target.value;
                  setF(prev => ({ ...prev, sport: val, role: '' }));
                  if (val !== 'Other') setCustomSport('');
                  setRoleOpen(true);
                }}
                className={inputCls()}>
                <option value="">Select sport</option>
                {SPORT_OPTIONS.map(s => <option key={s} value={s}>{s}</option>)}
              </select>
              {f.sport === 'Other' && (
                <input type="text" value={customSport}
                  onChange={e => setCustomSport(e.target.value)}
                  className={`${inputCls()} mt-2`} placeholder="Specify your sport" />
              )}
            </div>
            <div>
              <label className={labelCls}>Role</label>
              {f.sport && f.sport !== 'Other' && roleProfiles.some(p => p.sport === f.sport) ? (
                <select value={f.role} onChange={e => { update('role', e.target.value); setRoleOpen(true); }}
                  className={inputCls()}>
                  <option value="">Select role</option>
                  {roleProfiles.filter(p => p.sport === f.sport).map(p => p.role).map(r => (
                    <option key={r} value={r}>{r}</option>
                  ))}
                </select>
              ) : (
                <input type="text" value={f.role} onChange={e => { update('role', e.target.value); setRoleOpen(true); }}
                  className={inputCls()} placeholder="e.g. Fast Bowler" />
              )}
            </div>
            <div>
              <label className={labelCls}>Level</label>
              <select value={f.level} onChange={e => update('level', e.target.value)} className={inputCls()}>
                {LEVELS.map(l => <option key={l} value={l}>{l}</option>)}
              </select>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className={labelCls}>Age</label>
                <input type="number" value={f.age} onChange={e => update('age', e.target.value === '' ? '' : Number(e.target.value))}
                  className={inputCls()} min={0} max={120} />
              </div>
              <div>
                <label className={labelCls}>Training Age</label>
                <input type="number" value={f.training_age_years} onChange={e => update('training_age_years', e.target.value === '' ? '' : Number(e.target.value))}
                  className={inputCls()} min={0} max={50} />
              </div>
            </div>
          </div>

          {/* Role Info Panel */}
          {profile && (
            <div className="border border-indigo-100 bg-indigo-50/30 rounded-xl overflow-hidden">
              <button onClick={() => setRoleOpen(!roleOpen)}
                className="w-full flex items-center justify-between px-4 py-3 text-left">
                <span className="text-xs font-bold text-indigo-700 uppercase tracking-wider flex items-center gap-1.5">
                  <BookOpen className="w-3.5 h-3.5" /> {profile.sport} — {profile.role} Profile
                </span>
                <ChevronDown className={`w-4 h-4 text-indigo-400 transition-transform ${roleOpen ? 'rotate-180' : ''}`} />
              </button>
              {roleOpen && (
                <div className="px-4 pb-4 space-y-4 text-sm">
                  <div>
                    <p className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1.5">Primary Demands</p>
                    <div className="flex flex-wrap gap-1.5">
                      {profile.primaryDemands.map(d => (
                        <span key={d} className="text-xs bg-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full">{d}</span>
                      ))}
                    </div>
                  </div>
                  <div>
                    <p className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1.5">Priority Movements</p>
                    <div className="flex flex-wrap gap-1.5">
                      {profile.priorityMovements.map(m => (
                        <span key={m} className="text-xs bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded-full">{m}</span>
                      ))}
                    </div>
                  </div>
                  <div>
                    <p className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1.5">Exercise Categories</p>
                    <div className="flex flex-wrap gap-1.5">
                      {profile.priorityExerciseCategories.map(c => (
                        <span key={c} className="text-xs bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full">{c}</span>
                      ))}
                    </div>
                  </div>
                  <div>
                    <p className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1.5">Tests & Benchmarks</p>
                    <div className="overflow-x-auto">
                      <table className="w-full text-xs">
                        <thead>
                          <tr className="text-slate-400 border-b border-indigo-100">
                            <th className="text-left py-1 pr-4 font-medium">Test</th>
                            {Object.keys(profile.tests[0]?.benchmarks ?? {}).map(k => (
                              <th key={k} className="text-left py-1 pr-4 font-medium">{k}</th>
                            ))}
                            <th className="text-left py-1 font-medium">Description</th>
                          </tr>
                        </thead>
                        <tbody>
                          {profile.tests.map(t => (
                            <tr key={t.name} className="border-b border-indigo-50">
                              <td className="py-1.5 pr-4 text-slate-700">{t.name}</td>
                              {Object.values(t.benchmarks).map((v, i) => (
                                <td key={i} className={`py-1.5 pr-4 font-medium ${i === 0 ? 'text-emerald-600' : 'text-amber-600'}`}>{v}</td>
                              ))}
                              <td className="py-1.5 text-slate-500 text-[11px]">{t.description}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                  {profile.forgeBiases.length > 0 && (
                    <div>
                      <p className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1.5">FORGE Biases</p>
                      <ul className="text-xs text-slate-600 space-y-0.5 list-disc list-inside">
                        {profile.forgeBiases.map(b => <li key={b}>{b}</li>)}
                      </ul>
                    </div>
                  )}
                  {profile.injuryRiskFactors.length > 0 && (
                    <div>
                      <p className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-1.5">Injury Risk Factors</p>
                      <div className="flex flex-wrap gap-1.5">
                        {profile.injuryRiskFactors.map(r => (
                          <span key={r} className="text-xs bg-red-50 text-red-700 px-2 py-0.5 rounded-full border border-red-200">{r}</span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </section>

        {/* Section 2: Program Objective */}
        <section className="bg-white rounded-xl border border-slate-200 p-5 space-y-4 shadow-sm">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Target className="w-3.5 h-3.5" /> Program Objective
          </h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className={labelCls}>Phase</label>
              <select value={f.phase} onChange={e => update('phase', e.target.value)} className={inputCls()}>
                <option value="">Select phase</option>
                {PHASES.map(p => <option key={p} value={p}>{p}</option>)}
              </select>
            </div>
            <div>
              <label className={labelCls}>Goal</label>
              <select value={f.goal} onChange={e => update('goal', e.target.value)} className={inputCls()}>
                <option value="">Select goal</option>
                {GOALS.map(g => <option key={g} value={g}>{g}</option>)}
              </select>
            </div>
            <div>
              <label className={labelCls}>Length (weeks)</label>
              <input type="number" value={f.program_length_weeks} onChange={e => update('program_length_weeks', Number(e.target.value))}
                className={inputCls(f.program_length_weeks < 1 || f.program_length_weeks > 52)} min={1} max={52} />
            </div>
            <div>
              <label className={labelCls}>Sessions / week</label>
              <input type="number" value={f.sessions_per_week} onChange={e => update('sessions_per_week', Number(e.target.value))}
                className={inputCls(f.sessions_per_week < 1 || f.sessions_per_week > 7)} min={1} max={7} />
            </div>
            <div>
              <label className={labelCls}>Minutes / session</label>
              <input type="number" value={f.minutes_per_session} onChange={e => update('minutes_per_session', Number(e.target.value))}
                className={inputCls(f.minutes_per_session < 10 || f.minutes_per_session > 240)} min={10} max={240} />
              {profile && profile.sport !== '*' && <p className="text-[10px] text-slate-400 mt-0.5">Based on role profile</p>}
            </div>
          </div>
        </section>

        {/* Section 3: Weekly Rhythm */}
        <section className="bg-white rounded-xl border border-slate-200 p-5 space-y-4 shadow-sm">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Calendar className="w-3.5 h-3.5" /> Weekly Rhythm
          </h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className={labelCls}>Match Day</label>
              <select value={f.match_day} onChange={e => update('match_day', e.target.value)} className={inputCls()}>
                <option value="">Select day</option>
                {DAYS.map(d => <option key={d} value={d}>{d}</option>)}
              </select>
            </div>
          </div>
          <div className="space-y-3">
            {([
              { label: 'Team Training Days', key: 'team_training_days' as const },
              { label: 'Heavy Field Days', key: 'heavy_field_days' as const },
              { label: 'Travel Days', key: 'travel_days' as const },
            ] as const).map(({ label, key }) => (
              <div key={key}>
                <label className={labelCls}>{label}</label>
                <div className="flex flex-wrap gap-1.5">
                  {DAYS.map(d => (
                    <button key={d} onClick={() => setF(prev => ({ ...prev, [key]: toggleDay(prev[key], d) }))}
                      className={selCls(f[key].includes(d))}>
                      {d.slice(0, 3)}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Section 4: Constraints */}
        <section className="bg-white rounded-xl border border-slate-200 p-5 space-y-4 shadow-sm">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <Shield className="w-3.5 h-3.5" /> Constraints
          </h3>
          <div>
            <label className={labelCls}>Equipment Available</label>
            <div className="flex flex-wrap gap-1.5">
              {EQUIPMENT_OPTIONS.map(eq => (
                <button key={eq} onClick={() => setF(prev => ({
                  ...prev,
                  equipment: prev.equipment.includes(eq) ? prev.equipment.filter(e => e !== eq) : [...prev.equipment, eq]
                }))} className={selCls(f.equipment.includes(eq))}>
                  {eq}
                </button>
              ))}
            </div>
          </div>
          <div>
            <label className={labelCls}>Injury Flags</label>
            <div className="flex flex-wrap gap-1.5 mb-2">
              {f.injury_flags.map(flag => (
                <span key={flag} className="inline-flex items-center gap-1 text-xs font-medium bg-red-50 text-red-700 px-2 py-0.5 rounded-full border border-red-200">
                  {flag}
                  <button onClick={() => setF(prev => ({ ...prev, injury_flags: prev.injury_flags.filter(f => f !== flag) }))}
                    className="hover:text-red-900">&times;</button>
                </span>
              ))}
            </div>
            <div className="flex gap-2">
              <input type="text" placeholder="Add injury flag..."
                onKeyDown={e => { if (e.key === 'Enter') { addInjuryFlag((e.target as HTMLInputElement).value); (e.target as HTMLInputElement).value = ''; } }}
                className="flex-1 px-3 py-1.5 text-xs border border-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500/20" />
              <button onClick={() => addInjuryFlag('')} className="px-3 py-1.5 text-xs font-medium bg-red-50 text-red-700 border border-red-200 rounded-md hover:bg-red-100">
                <Plus className="w-3 h-3" />
              </button>
            </div>
          </div>
          <div>
            <label className={labelCls}>Overall Injury Concern</label>
            <div className="flex gap-1.5">
              {INJURY_SEVERITY.map(s => (
                <button key={s} onClick={() => update('injury_severity', s)}
                  className={selCls(f.injury_severity === s)}>
                  {s}
                </button>
              ))}
            </div>
          </div>
        </section>

        {/* Section 5: Coach Intent */}
        <section className="bg-white rounded-xl border border-slate-200 p-5 space-y-3 shadow-sm">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
            <FileText className="w-3.5 h-3.5" /> Coach Intent
          </h3>
          <textarea value={f.coach_intent} onChange={e => update('coach_intent', e.target.value)}
            className="w-full px-3 py-2 text-sm border border-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500/20 resize-none"
            rows={3} placeholder="Describe specific intent, focus areas, or constraints for this block..." />
        </section>

        {/* Section 6: Performance Data */}
        <section className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
          <button onClick={() => setPerfOpen(!perfOpen)}
            className="w-full flex items-center justify-between px-5 py-4 text-left">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1.5">
              <BarChart3 className="w-3.5 h-3.5" /> Performance Data <span className="text-slate-300 font-normal normal-case">(optional)</span>
            </span>
            <ChevronDown className={`w-4 h-4 text-slate-400 transition-transform ${perfOpen ? 'rotate-180' : ''}`} />
          </button>
          {perfOpen && (
            <div className="px-5 pb-5 space-y-4">
              <p className="text-xs text-slate-500">Enter test results to refine program specificity. Benchmarks shown from role profile.</p>
              <div className="grid grid-cols-2 gap-4">
                {([
                  { label: 'YoYo IR1', key: 'yoyo_ir1' as const },
                  { label: 'YoYo IR2', key: 'yoyo_ir2' as const },
                  { label: 'Bronco', key: 'bronco' as const },
                  { label: 'CMJ', key: 'cmj_band' as const },
                ] as const).map(({ label, key }) => (
                  <div key={key}>
                    <label className={labelCls}>{label}</label>
                    <input type="text" value={f[key]} onChange={e => update(key, e.target.value)}
                      className="w-full px-3 py-2 text-sm border border-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
                      placeholder="e.g. 18.2" />
                    {profile && (() => {
                      const match = profile.tests.find(t => t.name.toLowerCase().startsWith(label.toLowerCase()));
                      return match ? (
                        <p className="text-[10px] text-slate-400 mt-0.5">Benchmarks: {Object.entries(match.benchmarks).map(([k, v]) => `${k} ${v}`).join(' / ')}</p>
                      ) : null;
                    })()}
                  </div>
                ))}
              </div>
            </div>
          )}
        </section>

        <div className="h-4" />
      </div>

      {prefsOpen && <CoachPreferencesModal onClose={() => setPrefsOpen(false)} />}
    </div>
  );
}
