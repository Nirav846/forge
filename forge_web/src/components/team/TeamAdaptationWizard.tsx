import React, { useState } from 'react';
import { ArrowLeft, User, Calendar, Activity, Loader2, CheckCircle, AlertCircle } from 'lucide-react';
import { TeamTemplate } from '../../types/ui';
import { adaptTeamTemplate, generateProgram as apiGenerate } from '../../lib/api';
import { normalizeProgramResponse } from '../../lib/transformers';
import { CoachSummaryMode } from '../program/modes/CoachSummaryMode';

interface TeamAdaptationWizardProps {
  template: TeamTemplate;
  onComplete: (result: any) => void;
  onBack: () => void;
}

type Step = 'athlete' | 'calendar' | 'tests' | 'result';

const DAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

export function TeamAdaptationWizard({ template, onComplete, onBack }: TeamAdaptationWizardProps) {
  const [step, setStep] = useState<Step>('athlete');

  // Athlete
  const [athleteName, setAthleteName] = useState('');
  const [role, setRole] = useState('');
  const [age, setAge] = useState<number | ''>('');
  const [trainingAge, setTrainingAge] = useState<number | ''>('');

  // Calendar overrides
  const [matchDay, setMatchDay] = useState<number | ''>('');
  const [trainingDays, setTrainingDays] = useState('');
  const [heavyDays, setHeavyDays] = useState('');

  // Tests
  const [yoyoIr1, setYoyoIr1] = useState<number | ''>('');
  const [yoyoIr2, setYoyoIr2] = useState<number | ''>('');
  const [bronco, setBronco] = useState<number | ''>('');
  const [cmj, setCmj] = useState<number | ''>('');
  const [injuryFlags, setInjuryFlags] = useState('');
  const [coachIntent, setCoachIntent] = useState('');

  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<any>(null);

  const handleGenerate = async () => {
    if (!athleteName.trim()) {
      setError('Athlete name is required.');
      return;
    }
    setSaving(true);
    setError(null);
    try {
      const payload: Record<string, any> = {
        athlete_name: athleteName.trim(),
        role: role || template.sport,
      };
      if (age !== '') payload.age = age;
      if (trainingAge !== '') payload.training_age_years = trainingAge;
      if (matchDay !== '') payload.match_day = matchDay;
      if (trainingDays.trim()) payload.team_training_days = trainingDays.split(',').map(Number).filter(n => !isNaN(n));
      if (heavyDays.trim()) payload.heavy_field_days = heavyDays.split(',').map(Number).filter(n => !isNaN(n));
      if (yoyoIr1 !== '') payload.yoyo_ir1 = yoyoIr1;
      if (yoyoIr2 !== '') payload.yoyo_ir2 = yoyoIr2;
      if (bronco !== '') payload.bronco = bronco;
      if (cmj !== '') payload.cmj = cmj;
      if (injuryFlags.trim()) payload.injury_flags = injuryFlags.split(',').map(s => s.trim()).filter(Boolean);
      if (coachIntent.trim()) payload.coach_intent = coachIntent;

      const raw = await adaptTeamTemplate(template.id, payload);
      const transformed = normalizeProgramResponse(raw);
      setResult(transformed);
      setStep('result');
    } catch (err: any) {
      setError(err.message || 'Adaptation failed.');
    } finally {
      setSaving(false);
    }
  };

  const athleteValid = athleteName.trim().length > 0;

  return (
    <div className="max-w-4xl mx-auto w-full h-full flex flex-col py-8 px-6">
      <button onClick={onBack} className="flex items-center gap-1.5 text-sm text-slate-500 hover:text-slate-800 mb-6 w-fit">
        <ArrowLeft className="w-4 h-4" /> Back
      </button>

      <div className="flex items-center gap-2 mb-6">
        {(['athlete', 'calendar', 'tests', 'result'] as Step[]).map((s, i) => (
          <React.Fragment key={s}>
            <div className={`flex items-center gap-1.5 text-xs font-medium px-2.5 py-1 rounded-full ${step === s ? 'bg-indigo-100 text-indigo-700' : i < ['athlete', 'calendar', 'tests', 'result'].indexOf(step) ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-100 text-slate-400'}`}>
              {i + 1}. {s.charAt(0).toUpperCase() + s.slice(1)}
            </div>
            {i < 3 && <div className="w-6 h-px bg-slate-200" />}
          </React.Fragment>
        ))}
      </div>

      <h2 className="text-xl font-bold text-slate-900 mb-1">Adapt Template: {template.name}</h2>
      <p className="text-sm text-slate-500 mb-6">Customize the team template for an individual athlete</p>

      {error && (
        <div className="mb-4 flex items-center gap-2 text-sm text-red-700 bg-red-50 border border-red-200 rounded-lg px-4 py-3">
          <AlertCircle className="w-4 h-4 shrink-0" />
          {error}
        </div>
      )}

      <div className="flex-1 overflow-y-auto">
        {step === 'athlete' && (
          <div className="max-w-lg space-y-4">
            <div className="flex items-center gap-2 mb-4">
              <User className="w-5 h-5 text-indigo-500" />
              <h3 className="font-semibold text-slate-900">Athlete Details</h3>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Athlete Name *</label>
              <input value={athleteName} onChange={e => setAthleteName(e.target.value)} placeholder="e.g. John Smith" className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Role / Position</label>
              <input value={role} onChange={e => setRole(e.target.value)} placeholder={template.sport} className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Age</label>
                <input type="number" min={0} value={age} onChange={e => setAge(e.target.value ? Number(e.target.value) : '')} className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Training Age (years)</label>
                <input type="number" min={0} step={0.5} value={trainingAge} onChange={e => setTrainingAge(e.target.value ? Number(e.target.value) : '')} className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
              </div>
            </div>
            <div className="pt-4">
              <button onClick={() => setStep('calendar')} disabled={!athleteValid} className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white font-semibold px-6 py-2.5 rounded-xl transition-colors">
                Next: Calendar
              </button>
            </div>
          </div>
        )}

        {step === 'calendar' && (
          <div className="max-w-lg space-y-4">
            <div className="flex items-center gap-2 mb-4">
              <Calendar className="w-5 h-5 text-indigo-500" />
              <h3 className="font-semibold text-slate-900">Calendar Overrides <span className="text-sm font-normal text-slate-400">(leave blank to use template)</span></h3>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Match Day (0=Mon..6=Sun)</label>
              <input type="number" min={0} max={6} value={matchDay} onChange={e => setMatchDay(e.target.value ? Number(e.target.value) : '')} className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Training Days (comma, 0-6)</label>
              <input value={trainingDays} onChange={e => setTrainingDays(e.target.value)} placeholder={`${template.team_training_days?.join(',') || '0,2,4'}`} className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Heavy Field Days (comma, 0-6)</label>
              <input value={heavyDays} onChange={e => setHeavyDays(e.target.value)} placeholder={`${template.heavy_field_days?.join(',') || '1,3'}`} className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            </div>
            <div className="flex gap-3 pt-4">
              <button onClick={() => setStep('athlete')} className="text-sm text-slate-600 hover:text-slate-800 px-4 py-2.5">Back</button>
              <button onClick={() => setStep('tests')} className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-6 py-2.5 rounded-xl transition-colors">
                Next: Tests
              </button>
            </div>
          </div>
        )}

        {step === 'tests' && (
          <div className="max-w-lg space-y-4">
            <div className="flex items-center gap-2 mb-4">
              <Activity className="w-5 h-5 text-indigo-500" />
              <h3 className="font-semibold text-slate-900">Test Data <span className="text-sm font-normal text-slate-400">(optional)</span></h3>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Yo-Yo IR1</label>
                <input type="number" step={0.1} value={yoyoIr1} onChange={e => setYoyoIr1(e.target.value ? Number(e.target.value) : '')} className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Yo-Yo IR2</label>
                <input type="number" step={0.1} value={yoyoIr2} onChange={e => setYoyoIr2(e.target.value ? Number(e.target.value) : '')} className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Bronco</label>
                <input type="number" step={0.1} value={bronco} onChange={e => setBronco(e.target.value ? Number(e.target.value) : '')} className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">CMJ (cm)</label>
                <input type="number" step={0.1} value={cmj} onChange={e => setCmj(e.target.value ? Number(e.target.value) : '')} className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Injury Risk Flags (comma)</label>
              <input value={injuryFlags} onChange={e => setInjuryFlags(e.target.value)} placeholder="e.g. hamstring, groin" className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Coach Intent</label>
              <input value={coachIntent} onChange={e => setCoachIntent(e.target.value)} placeholder="e.g. Increase sprint exposure" className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            </div>
            <div className="flex gap-3 pt-4">
              <button onClick={() => setStep('calendar')} className="text-sm text-slate-600 hover:text-slate-800 px-4 py-2.5">Back</button>
              <button onClick={handleGenerate} disabled={saving} className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white font-semibold px-6 py-2.5 rounded-xl transition-colors flex items-center gap-2">
                {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
                {saving ? 'Generating...' : 'Generate Individual Program'}
              </button>
            </div>
          </div>
        )}

        {step === 'result' && result && (
          <div>
            <div className="flex items-center gap-2 mb-4 text-emerald-700">
              <CheckCircle className="w-5 h-5" />
              <h3 className="font-semibold">Program Generated for {athleteName}</h3>
            </div>
            <div className="bg-white border border-slate-200 rounded-xl p-6">
              <CoachSummaryMode viewModel={result.viewModel} />
            </div>
            <div className="flex gap-3 mt-6">
              <button onClick={() => onComplete(result)} className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-6 py-2.5 rounded-xl transition-colors">
                Open in Coach Console
              </button>
              <button onClick={onBack} className="text-sm text-slate-600 hover:text-slate-800 px-4 py-2.5">
                Back to Templates
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
