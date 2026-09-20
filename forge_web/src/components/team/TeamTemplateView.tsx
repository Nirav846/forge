import React from 'react';
import { ArrowLeft, Trophy, Calendar, Clock, Target, Dumbbell, Users, Activity, GitCompare } from 'lucide-react';
import { TeamTemplate } from '../../types/ui';
import { normalizeProgramResponse } from '../../lib/transformers';
import { CoachSummaryMode } from '../program/modes/CoachSummaryMode';

interface TeamTemplateViewProps {
  template: TeamTemplate;
  onAdapt: (template: TeamTemplate) => void;
  onBack: () => void;
}

const DAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

export function TeamTemplateView({ template, onAdapt, onBack }: TeamTemplateViewProps) {
  const program = template.program_snapshot
    ? normalizeProgramResponse(template.program_snapshot.result_snapshot)
    : null;

  return (
    <div className="max-w-4xl mx-auto w-full h-full flex flex-col py-8 px-6">
      <button onClick={onBack} className="flex items-center gap-1.5 text-sm text-slate-500 hover:text-slate-800 mb-6 w-fit">
        <ArrowLeft className="w-4 h-4" /> Back to Entry
      </button>

      {/* Header */}
      <div className="flex items-start justify-between mb-8">
        <div className="flex items-center gap-3">
          <Trophy className="w-7 h-7 text-indigo-600" />
          <div>
            <h2 className="text-xl font-bold text-slate-900">{template.name}</h2>
            <p className="text-sm text-slate-500">
              {template.sport} &middot; {template.level} &middot; {template.phase.replace('_', ' ')}
            </p>
          </div>
        </div>
        <button
          onClick={() => onAdapt(template)}
          disabled={!program}
          className="flex items-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white text-sm font-semibold px-5 py-2.5 rounded-xl transition-colors"
        >
          <GitCompare className="w-4 h-4" /> Adapt for Athlete
        </button>
      </div>

      {/* Meta cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mb-8">
        <div className="bg-white border border-slate-200 rounded-xl p-4">
          <Calendar className="w-4 h-4 text-indigo-500 mb-1.5" />
          <div className="text-lg font-bold text-slate-900">{template.program_length_weeks}w</div>
          <div className="text-xs text-slate-500">Program Length</div>
        </div>
        <div className="bg-white border border-slate-200 rounded-xl p-4">
          <Clock className="w-4 h-4 text-indigo-500 mb-1.5" />
          <div className="text-lg font-bold text-slate-900">{template.sessions_per_week}</div>
          <div className="text-xs text-slate-500">Sessions / Week</div>
        </div>
        <div className="bg-white border border-slate-200 rounded-xl p-4">
          <Target className="w-4 h-4 text-indigo-500 mb-1.5" />
          <div className="text-lg font-bold text-slate-900">{template.minutes_per_session}m</div>
          <div className="text-xs text-slate-500">Per Session</div>
        </div>
        <div className="bg-white border border-slate-200 rounded-xl p-4">
          <Dumbbell className="w-4 h-4 text-indigo-500 mb-1.5" />
          <div className="text-sm font-bold text-slate-900 truncate">{DAY_NAMES[template.match_day] || 'Sat'}</div>
          <div className="text-xs text-slate-500">Match Day</div>
        </div>
      </div>

      {/* Calendar summary */}
      <div className="bg-white border border-slate-200 rounded-xl p-4 mb-8">
        <div className="flex items-center gap-2 mb-3">
          <Activity className="w-4 h-4 text-indigo-500" />
          <span className="text-sm font-semibold text-slate-900">Weekly Schedule</span>
        </div>
        <div className="flex gap-1.5">
          {DAY_NAMES.map((day, i) => {
            const isMatch = i === template.match_day;
            const isTrain = template.team_training_days?.includes(i);
            const isHeavy = template.heavy_field_days?.includes(i);
            let cls = 'flex-1 text-center text-xs py-1.5 rounded-md font-medium ';
            if (isMatch) cls += 'bg-indigo-100 text-indigo-700';
            else if (isHeavy) cls += 'bg-amber-100 text-amber-700';
            else if (isTrain) cls += 'bg-emerald-100 text-emerald-700';
            else cls += 'bg-slate-100 text-slate-400';
            let label = day;
            if (isMatch) label += ' 🏆';
            return <div key={i} className={cls}>{label}</div>;
          })}
        </div>
      </div>

      {/* Program */}
      {program ? (
        <div className="flex-1 overflow-y-auto">
          <CoachSummaryMode viewModel={program.viewModel} />
        </div>
      ) : (
        <div className="flex-1 flex items-center justify-center text-slate-400 text-sm">
          No program generated yet. Generate the template first.
        </div>
      )}
    </div>
  );
}
