import { useState, useMemo, useCallback, useEffect } from 'react';
import { ProgramRequest, Mode } from '../types';
import { RawAthleteBasics } from '../types/api';
import { Zap, Play, AlertCircle, Settings2 } from 'lucide-react';
import { AppStatus } from '../App';
import SportSelector from './builder/SportSelector';
import RoleSelector from './builder/RoleSelector';
import { RoleInfoPanel } from './builder/RoleInfoPanel';
import SeasonTimeline from './builder/SeasonTimeline';
import GoalSelector from './builder/GoalSelector';
import WeeklySchedule from './builder/WeeklySchedule';
import SessionLengthSlider from './builder/SessionLengthSlider';
import { daysToNumbers } from '../lib/calendar';

interface LeftPanelProps {
  request: ProgramRequest;
  setRequest: React.Dispatch<React.SetStateAction<ProgramRequest>>;
  onGenerate: (builtRequest?: ProgramRequest) => void;
  status: AppStatus;
}

// ponytail: compile-time guard — every user-editable basics field must have a
// BuilderState counterpart. Adding a field here fails the build if BuilderState
// doesn't have the corresponding camelCase field.
// sex, days_to_match have no UI controls yet — add when needed.
type _STATE_CHECK = {
  athlete_name: BuilderState['athleteName'];
  age: BuilderState['age'];
  training_age_years: BuilderState['trainingAge'];
  environment: BuilderState['environments'];
};
void {} as _STATE_CHECK;

const SCORED_ENV_OPTIONS = [
  { value: 'Gym', label: 'Gym', emoji: '🏋️' },
  { value: 'Field', label: 'Field', emoji: '🏃' },
  { value: 'Court', label: 'Court', emoji: '🏸' },
] as const;

function toggleEnvironment(setBuilder: React.Dispatch<React.SetStateAction<BuilderState>>, env: string, checked: boolean): void {
  setBuilder(prev => ({
    ...prev,
    environments: checked
      ? [...prev.environments, env]
      : prev.environments.filter(e => e !== env),
  }));
}

interface BuilderState {
  athleteName: string;
  sport: string;
  role: string;
  seasonPhase: string;
  goal: string;
  trainingDays: number[];
  sessionLength: number;
  age: number | '';
  trainingAge: number | '';
  environments: string[];
}

function buildRequest(state: BuilderState, mode: Mode): ProgramRequest {
  const matchDay = state.trainingDays.length > 0 ? state.trainingDays[state.trainingDays.length - 1] + 1 : 5;
  // ponytail: legacy single-env field is recomputed from selected checkboxes — keeps backend happy.
  const primaryEnv = state.environments[0] || '';
  const basics: RawAthleteBasics = {
    athlete_name: state.athleteName,
    sport: state.sport === 'Rugby' ? 'Rugby Union' : state.sport,
    role: state.role,
    level: 'Intermediate',
    age: state.age,
    training_age_years: state.trainingAge,
    frequency_per_week: state.trainingDays.length || 3,
    available_minutes: state.sessionLength,
    environment: primaryEnv as RawAthleteBasics['environment'],
  };
  return {
    mode,
    basics,
    context: {
      primary_goal: state.goal,
      current_phase: state.seasonPhase,
      program_length_weeks: 4,
      match_day: matchDay,
      team_training_days: [...state.trainingDays],
      available_environments: state.environments,  // ponytail: multi-select drives per-session env
    },
    advanced: {
      injury_risk_flags: [],
    },
  };
}

export default function LeftPanel({ request, setRequest, onGenerate, status }: LeftPanelProps) {
  const isGenerating = status === 'loading';

  // Local builder state — initialised from request on mount
  const [builder, setBuilder] = useState<BuilderState>(() => {
    const b = request.basics;
    const c = request.context;
    const days = daysToNumbers(c.team_training_days || []).filter(i => i >= 0);
    const sport = b.sport === 'Rugby Union' ? 'Rugby' : (b.sport || '');
    return {
      athleteName: b.athlete_name || '',
      sport,
      role: b.role || '',
      seasonPhase: c.current_phase || '',
      goal: c.primary_goal || '',
      trainingDays: days,
      sessionLength: b.available_minutes || 60,
      age: typeof b.age === 'number' ? b.age : '',
      trainingAge: typeof b.training_age_years === 'number' ? b.training_age_years : '',
      // ponytail: prefer available_environments; fall back to single environment; then default ['Gym'].
      environments: c.available_environments && c.available_environments.length > 0
        ? c.available_environments
        : (b.environment ? [b.environment] : ['Gym']),
    };
  });

  // Sync builder back to parent request on every change (for save/load)
  useEffect(() => {
    const req = buildRequest(builder, request.mode);
    setRequest(req);
  }, [builder, request.mode, setRequest]);

  const update = useCallback((field: keyof BuilderState, value: any) => {
    setBuilder(prev => ({ ...prev, [field]: value }));
  }, []);

  const mode = request.mode;
  const setMode = useCallback((m: Mode) => {
    setRequest(prev => ({ ...prev, mode: m }));
  }, [setRequest]);

  const athleteMissing = !builder.athleteName.trim();
  const sportMissing = !builder.sport;
  const roleMissing = !builder.role;
  const canGenerate = !athleteMissing && !sportMissing && !roleMissing;

  const handleGenerate = useCallback(() => {
    if (!canGenerate || isGenerating) return;
    const req = buildRequest(builder, request.mode);
    setRequest(req);
    onGenerate(req);
  }, [builder, request.mode, canGenerate, isGenerating, setRequest, onGenerate]);

  const errors: string[] = useMemo(() => {
    const e: string[] = [];
    if (athleteMissing) e.push('Athlete name is required');
    if (sportMissing) e.push('Select a sport');
    if (roleMissing) e.push('Select a role');
    return e;
  }, [athleteMissing, sportMissing, roleMissing]);

  return (
    <div className="flex flex-col h-full">
      {/* Top sticky: name input + mode toggle + generate */}
      <div className="sticky top-0 bg-white border-b border-slate-200 z-20 shadow-sm">
        <div className="p-4 pb-3 space-y-3">
          {/* Mode toggle */}
          <div className="flex bg-slate-100 p-0.5 rounded-lg">
            <button
              onClick={() => setMode('core')}
              className={`flex-1 py-1.5 text-xs font-medium rounded-md transition-all ${mode === 'core' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
            >
              Core Mode
            </button>
            <button
              onClick={() => setMode('premium')}
              className={`flex-1 py-1.5 text-xs font-medium rounded-md transition-all flex items-center justify-center gap-1 ${mode === 'premium' ? 'bg-indigo-50 text-indigo-700 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
            >
              <Settings2 className="w-3 h-3" /> Premium
            </button>
          </div>

          {/* Athlete name — keyboard only */}
          <div>
            <label className="block text-xs font-medium text-slate-700 mb-1">Athlete Name *</label>
            <input
              type="text"
              value={builder.athleteName}
              onChange={e => update('athleteName', e.target.value)}
              className="w-full px-3 py-2 text-sm bg-slate-50 border border-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white transition-all"
              placeholder="e.g. John Doe"
            />
          </div>

          {/* Age + Training Age — optional */}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1">Age</label>
              <input
                type="number"
                min={0}
                value={builder.age}
                onChange={e => update('age', e.target.value === '' ? '' : Number(e.target.value))}
                className="w-full px-3 py-2 text-sm bg-slate-50 border border-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white transition-all"
                placeholder="e.g. 22"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-700 mb-1">Training Age (yrs)</label>
              <input
                type="number"
                step="0.5"
                min={0}
                value={builder.trainingAge}
                onChange={e => update('trainingAge', e.target.value === '' ? '' : Number(e.target.value))}
                className="w-full px-3 py-2 text-sm bg-slate-50 border border-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white transition-all"
                placeholder="e.g. 2.5"
              />
            </div>
          </div>

          {/* Environments — multi-select; engine auto-assigns each session */}
          <div>
            <label className="block text-xs font-medium text-slate-700 mb-1">Available Environments</label>
            <div className="flex gap-4 mt-1">
              {SCORED_ENV_OPTIONS.map(({ value, label, emoji }) => (
                <label key={value} className="flex items-center gap-1.5 text-sm text-slate-700">
                  <input
                    type="checkbox"
                    checked={builder.environments.includes(value)}
                    onChange={e => toggleEnvironment(setBuilder, value, e.target.checked)}
                    className="rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
                  />
                  {emoji} {label}
                </label>
              ))}
            </div>
            <p className="text-[10px] text-slate-400 mt-1">
              Sessions auto-assign to the most suitable environment; per-session override still available.
            </p>
          </div>

          {/* Generate button */}
          <button
            onClick={handleGenerate}
            disabled={isGenerating || !canGenerate}
            className="w-full bg-slate-900 hover:bg-slate-800 disabled:bg-slate-300 disabled:cursor-not-allowed text-white py-2.5 rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-2"
          >
            {isGenerating ? (
              <span className="flex items-center gap-2"><Zap className="w-4 h-4 animate-pulse" /> Generating...</span>
            ) : (
              <span className="flex items-center gap-2"><Play className="w-4 h-4" /> Generate Program</span>
            )}
          </button>
          {errors.length > 0 && !isGenerating && (
            <div className="flex items-center gap-1.5 text-xs text-red-600 bg-red-50 px-2 py-1.5 rounded border border-red-200">
              <AlertCircle className="w-3 h-3 shrink-0" />
              <span>{errors.length} required field{errors.length !== 1 ? 's' : ''} missing</span>
            </div>
          )}
        </div>
      </div>

      {/* Scrollable builder sections */}
      <div className="flex-1 overflow-y-auto p-4 space-y-5">
        {/* Sport */}
        <section className="space-y-2">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Sport</h3>
          <SportSelector value={builder.sport} onChange={v => update('sport', v)} />
        </section>

        {/* Role — shown only after sport is selected */}
        {builder.sport && (
          <section className="space-y-2">
            <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Role / Position</h3>
            <RoleSelector
              sport={builder.sport}
              value={builder.role}
              onChange={v => update('role', v)}
            />
            {builder.role && (
              <div className="mt-4">
                <RoleInfoPanel sport={builder.sport} role={builder.role} />
              </div>
            )}
          </section>
        )}

        {/* Season */}
        <section className="space-y-2">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Season Phase</h3>
          <SeasonTimeline value={builder.seasonPhase} onChange={v => update('seasonPhase', v)} />
        </section>

        {/* Goal */}
        <section className="space-y-2">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Primary Goal</h3>
          <GoalSelector value={builder.goal} onChange={v => update('goal', v)} />
        </section>

        {/* Weekly Schedule */}
        <section className="space-y-2">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Training Days</h3>
          <WeeklySchedule value={builder.trainingDays} onChange={v => update('trainingDays', v)} />
        </section>

        {/* Session Length */}
        <section className="space-y-2">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Session Length</h3>
          <SessionLengthSlider value={builder.sessionLength} onChange={v => update('sessionLength', v)} />
        </section>
      </div>
    </div>
  );
}
