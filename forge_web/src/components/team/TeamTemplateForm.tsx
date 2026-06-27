import React, { useState } from 'react';
import { ArrowLeft, Save, Trophy, Loader2, AlertCircle } from 'lucide-react';
import { createTeamTemplate, generateProgram as apiGenerate, updateTeamTemplate, listTeamTemplates } from '../../lib/api';
import { normalizeProgramResponse } from '../../lib/transformers';
import { TeamTemplate } from '../../types/ui';

interface TeamTemplateFormProps {
  onComplete: (template: TeamTemplate) => void;
  onBack: () => void;
}

export function TeamTemplateForm({ onComplete, onBack }: TeamTemplateFormProps) {
  const [name, setName] = useState('');
  const [sport, setSport] = useState('');
  const [level, setLevel] = useState('Intermediate');
  const [phase, setPhase] = useState('pre_season');
  const [goal, setGoal] = useState('');
  const [programLengthWeeks, setProgramLengthWeeks] = useState(4);
  const [sessionsPerWeek, setSessionsPerWeek] = useState(3);
  const [minutesPerSession, setMinutesPerSession] = useState(60);
  const [matchDay, setMatchDay] = useState(5);
  const [teamTrainingDays, setTeamTrainingDays] = useState('0,2,4');
  const [heavyFieldDays, setHeavyFieldDays] = useState('1,3');
  const [equipment, setEquipment] = useState('');
  const [coachNotes, setCoachNotes] = useState('');

  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async () => {
    if (!name.trim() || !sport.trim()) {
      setError('Name and Sport are required.');
      return;
    }
    setSaving(true);
    setError(null);
    try {
      // 1. Create the team template (metadata only)
      const created = await createTeamTemplate({
        name: name.trim(),
        sport,
        level,
        phase,
        goal,
        program_length_weeks: programLengthWeeks,
        sessions_per_week: sessionsPerWeek,
        minutes_per_session: minutesPerSession,
        match_day: matchDay,
        team_training_days: teamTrainingDays.split(',').map(Number).filter(n => !isNaN(n)),
        heavy_field_days: heavyFieldDays.split(',').map(Number).filter(n => !isNaN(n)),
        travel_days: [],
        equipment_profile: equipment.split(',').map(s => s.trim()).filter(Boolean),
        coach_notes: coachNotes,
      });

      // 2. Generate a program using template fields as the request
      const genPayload: any = {
        mode: 'core',
        basics: {
          sport,
          level,
          training_age_years: 5,
          available_minutes: minutesPerSession,
          frequency_per_week: sessionsPerWeek,
        },
        context: {
          primary_goal: goal || 'General preparation',
          current_phase: phase,
          match_day: matchDay,
          team_training_days: [0, 2, 4],
          heavy_field_days: [1, 3],
        },
        advanced: {},
      };

      const rawProgram = await apiGenerate(genPayload);

      // 3. Save program_snapshot to the template
      const snapshot = {
        request_snapshot: genPayload,
        result_snapshot: rawProgram,
      };
      const updated = await updateTeamTemplate(created.id, { program_snapshot: snapshot });

      onComplete(updated as TeamTemplate);
    } catch (err: any) {
      setError(err.message || 'Failed to generate team template.');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto w-full h-full flex flex-col py-8 px-6">
      <button onClick={onBack} className="flex items-center gap-1.5 text-sm text-slate-500 hover:text-slate-800 mb-6 w-fit">
        <ArrowLeft className="w-4 h-4" /> Back
      </button>

      <div className="flex items-center gap-3 mb-8">
        <Trophy className="w-7 h-7 text-indigo-600" />
        <div>
          <h2 className="text-xl font-bold text-slate-900">New Team Template</h2>
          <p className="text-sm text-slate-500">Create a template program structure for your team</p>
        </div>
      </div>

      {error && (
        <div className="mb-4 flex items-center gap-2 text-sm text-red-700 bg-red-50 border border-red-200 rounded-lg px-4 py-3">
          <AlertCircle className="w-4 h-4 shrink-0" />
          {error}
        </div>
      )}

      <div className="flex-1 overflow-y-auto space-y-5 pr-2">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Template Name *</label>
            <input value={name} onChange={e => setName(e.target.value)} placeholder="e.g. Senior Men's Rugby" className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Sport *</label>
            <input value={sport} onChange={e => setSport(e.target.value)} placeholder="e.g. Rugby Union" className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Level</label>
            <select value={level} onChange={e => setLevel(e.target.value)} className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
              <option>Beginner</option>
              <option>Intermediate</option>
              <option>Advanced</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Phase</label>
            <select value={phase} onChange={e => setPhase(e.target.value)} className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
              <option value="pre_season">Pre-Season</option>
              <option value="in_season">In-Season</option>
              <option value="off_season">Off-Season</option>
              <option value="transition">Transition</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Goal</label>
            <input value={goal} onChange={e => setGoal(e.target.value)} placeholder="e.g. Strength & Power" className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Weeks</label>
            <input type="number" min={1} max={52} value={programLengthWeeks} onChange={e => setProgramLengthWeeks(Number(e.target.value))} className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Sessions / Week</label>
            <input type="number" min={1} max={14} value={sessionsPerWeek} onChange={e => setSessionsPerWeek(Number(e.target.value))} className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Minutes / Session</label>
            <input type="number" min={15} max={180} step={5} value={minutesPerSession} onChange={e => setMinutesPerSession(Number(e.target.value))} className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Match Day (0=Mon..6=Sun)</label>
            <input type="number" min={0} max={6} value={matchDay} onChange={e => setMatchDay(Number(e.target.value))} className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Training Days (comma, 0-6)</label>
            <input value={teamTrainingDays} onChange={e => setTeamTrainingDays(e.target.value)} placeholder="0,2,4" className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Heavy Days (comma, 0-6)</label>
            <input value={heavyFieldDays} onChange={e => setHeavyFieldDays(e.target.value)} placeholder="1,3" className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Equipment (comma-separated)</label>
          <input value={equipment} onChange={e => setEquipment(e.target.value)} placeholder="e.g. Barbell, Dumbbell, Plyo Box" className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">Coach Notes</label>
          <textarea value={coachNotes} onChange={e => setCoachNotes(e.target.value)} rows={3} className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500" />
        </div>
      </div>

      <div className="pt-6 border-t border-slate-200 mt-6">
        <button
          onClick={handleGenerate}
          disabled={saving}
          className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white font-semibold px-6 py-3 rounded-xl transition-colors"
        >
          {saving ? <Loader2 className="w-5 h-5 animate-spin" /> : <Save className="w-5 h-5" />}
          {saving ? 'Generating...' : 'Generate Team Template'}
        </button>
      </div>
    </div>
  );
}
