import { TransformationResult, WeekVM } from '../types/ui';
import { AlertCircle, Lightbulb, BarChart3, CalendarDays, Activity, Target } from 'lucide-react';

interface InsightsPanelProps {
  result: TransformationResult | null;
}

const EXPOSURE_LABELS: Record<string, string> = {
  sprint_exposure: 'Sprint',
  jump_landing_exposure: 'Jump / Landing',
  deceleration_exposure: 'Deceleration',
  eccentric_stress: 'Eccentric Stress',
  conditioning_density: 'Conditioning',
};

const EXPOSURE_COLORS: Record<string, string> = {
  sprint_exposure: 'bg-amber-500',
  jump_landing_exposure: 'bg-indigo-500',
  deceleration_exposure: 'bg-rose-500',
  eccentric_stress: 'bg-emerald-500',
  conditioning_density: 'bg-cyan-500',
};

function exposureValue(label: string): number {
  const map: Record<string, number> = {
    'High': 1, 'Moderate': 0.66, 'Low': 0.33, 'None': 0,
  };
  return map[label] ?? 0;
}

function avgExposure(weeks: WeekVM[], field: string): number {
  const vals = weeks.map(w => exposureValue((w.exposure_summary as any)[field] || 'None'));
  return vals.reduce((a, b) => a + b, 0) / vals.length;
}

export default function InsightsPanel({ result }: InsightsPanelProps) {
  if (!result?.viewModel) return null;

  const vm = result.viewModel;
  const summary = vm.summary;

  const coverageItems = Object.keys(EXPOSURE_LABELS).map(field => ({
    label: EXPOSURE_LABELS[field],
    value: avgExposure(vm.weeks, field),
    color: EXPOSURE_COLORS[field],
  }));

  const sessionGrid: { week: number; count: number }[] = vm.weeks.map(w => ({
    week: w.week_number,
    count: w.sessions.length,
  }));

  return (
    <div className="h-full bg-slate-900 text-slate-300 overflow-y-auto p-5 space-y-6">
      {/* Program Summary */}
      <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700/50 space-y-2">
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
          <Target className="w-3.5 h-3.5" /> Program Summary
        </h3>
        <div className="grid grid-cols-2 gap-2 text-sm">
          {[
            ['Blueprint', summary.blueprint_selected],
            ['Duration', `${summary.total_weeks} weeks`],
            ['Frequency', `${summary.weekly_frequency}× / week`],
            ['Conditioning', summary.conditioning_emphasis],
            ['Comp Window', summary.competition_window],
            ['Role Emphasis', summary.role_emphasis],
          ].map(([k, v]) => (
            <div key={k} className="bg-slate-900/50 rounded-lg p-2">
              <div className="text-[10px] text-slate-500 uppercase tracking-wider">{k}</div>
              <div className="font-medium text-slate-200 mt-0.5">{v || '—'}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Movement Coverage */}
      {coverageItems.some(c => c.value > 0) && (
        <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700/50 space-y-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
            <BarChart3 className="w-3.5 h-3.5" /> Movement Coverage
          </h3>
          <div className="space-y-2">
            {coverageItems.map(item => (
              <div key={item.label}>
                <div className="flex justify-between text-xs mb-0.5">
                  <span className="text-slate-400">{item.label}</span>
                  <span className="text-slate-500 font-mono">{Math.round(item.value * 100)}%</span>
                </div>
                <div className="h-2 bg-slate-700/50 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full transition-all ${item.color}`}
                    style={{ width: `${item.value * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Weekly Session Distribution */}
      {sessionGrid.length > 0 && (
        <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700/50 space-y-3">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
            <CalendarDays className="w-3.5 h-3.5" /> Session Distribution
          </h3>
          <div className="flex gap-2 flex-wrap">
            {sessionGrid.map(({ week, count }) => (
              <div key={week} className="flex-1 min-w-[40px] bg-slate-900/50 rounded-lg p-2 text-center">
                <div className="text-[10px] text-slate-500">W{week}</div>
                <div className="text-lg font-bold text-slate-200">{count}</div>
                <div className="text-[10px] text-slate-500">session{count !== 1 ? 's' : ''}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* AI Reasoning */}
      {vm.rationale.length > 0 && (
        <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700/50 space-y-2">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
            <Lightbulb className="w-3.5 h-3.5 text-amber-400" /> AI Reasoning
          </h3>
          <ul className="space-y-1.5">
            {vm.rationale.slice(0, 8).map((r, i) => (
              <li key={i} className="text-sm text-slate-300 flex items-start gap-2">
                <span className="text-amber-500/70 mt-0.5 shrink-0">•</span>
                {r}
              </li>
            ))}
            {vm.rationale.length > 8 && (
              <li className="text-xs text-slate-500 italic">+{vm.rationale.length - 8} more items</li>
            )}
          </ul>
        </div>
      )}

      {/* Warnings / Validation */}
      {vm.validation.length > 0 && (
        <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700/50 space-y-2">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
            <AlertCircle className="w-3.5 h-3.5 text-amber-400" /> Warnings
          </h3>
          <div className="space-y-1.5">
            {vm.validation.map((v, i) => (
              <div
                key={i}
                className={`text-sm p-2 rounded-lg border ${
                  v.type === 'error'
                    ? 'bg-red-900/20 border-red-900/50 text-red-200'
                    : v.type === 'warning'
                    ? 'bg-amber-900/20 border-amber-900/50 text-amber-200'
                    : v.type === 'success'
                    ? 'bg-emerald-900/20 border-emerald-900/50 text-emerald-200'
                    : 'bg-sky-900/20 border-sky-900/50 text-sky-200'
                }`}
              >
                {v.message}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Assumptions */}
      {vm.personalization_notes.length > 0 && (
        <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700/50 space-y-2">
          <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1.5">
            <Activity className="w-3.5 h-3.5 text-emerald-400" /> Assumptions
          </h3>
          <ul className="space-y-1">
            {vm.personalization_notes.map((n, i) => (
              <li key={i} className="text-sm text-slate-300 flex items-start gap-2">
                <span className="text-emerald-500/70 mt-0.5 shrink-0">•</span>
                {n}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
