import { useState } from 'react';
import { getRoleProfile } from '../../data/roleProfiles';
import { Activity, AlertTriangle, Target, Zap, Dumbbell, ChevronDown, ChevronRight } from 'lucide-react';

interface RoleInfoPanelProps {
  sport: string;
  role: string;
}

export function RoleInfoPanel({ sport, role }: RoleInfoPanelProps) {
  const [open, setOpen] = useState(true);
  const profile = getRoleProfile(sport, role);
  if (!profile) return null;

  return (
    <div className="bg-white rounded-xl border border-slate-200">
      <button
        onClick={() => setOpen(o => !o)}
        className="w-full flex items-center justify-between p-4 text-sm font-bold text-slate-700 hover:bg-slate-50 rounded-xl transition-colors"
      >
        <span className="flex items-center gap-2">
          <Activity className="w-4 h-4 text-indigo-500" />
          {role} — {sport} Profile
        </span>
        {open ? <ChevronDown className="w-4 h-4 text-slate-400" /> : <ChevronRight className="w-4 h-4 text-slate-400" />}
      </button>
      {open && <div className="px-4 pb-4 space-y-4">

      {profile.primaryDemands.length > 0 && (
        <div>
          <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Primary Demands</h5>
          <ul className="text-sm text-slate-600 space-y-1">
            {profile.primaryDemands.map((d, i) => (
              <li key={i} className="flex items-start gap-2">
                <span className="text-indigo-400 mt-0.5">•</span>
                {d}
              </li>
            ))}
          </ul>
        </div>
      )}

      {profile.priorityMovements.length > 0 && (
        <div>
          <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Priority Movements</h5>
          <ul className="text-sm text-slate-600 space-y-1">
            {profile.priorityMovements.map((m, i) => (
              <li key={i} className="flex items-start gap-2">
                <span className="text-indigo-400 mt-0.5">•</span>
                {m}
              </li>
            ))}
          </ul>
        </div>
      )}

      {profile.priorityExerciseCategories.length > 0 && (
        <div>
          <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-2">
            <Dumbbell className="w-3 h-3" /> Priority Exercises
          </h5>
          <div className="flex flex-wrap gap-1.5">
            {profile.priorityExerciseCategories.map((cat, i) => (
              <span key={i} className="text-xs bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded-full border border-indigo-100">
                {cat}
              </span>
            ))}
          </div>
        </div>
      )}

      {profile.forgeBiases.length > 0 && (
        <div>
          <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-2">
            <Zap className="w-3 h-3 text-amber-500" /> FORGE Biases
          </h5>
          <ul className="text-sm text-slate-600 space-y-1 list-disc list-inside">
            {profile.forgeBiases.map((b, i) => (
              <li key={i}>{b}</li>
            ))}
          </ul>
        </div>
      )}

      {profile.injuryRiskFactors.length > 0 && (
        <div>
          <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-2">
            <AlertTriangle className="w-3 h-3 text-red-500" /> Injury Risks
          </h5>
          <ul className="text-sm text-slate-600 space-y-1 list-disc list-inside">
            {profile.injuryRiskFactors.map((r, i) => (
              <li key={i}>{r}</li>
            ))}
          </ul>
        </div>
      )}

      {profile.tests.length > 0 && (
        <div>
          <h5 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-2">
            <Target className="w-3 h-3 text-green-500" /> Tests & Benchmarks
          </h5>
          <div className="text-sm text-slate-600 space-y-2">
            {profile.tests.map((test, i) => (
              <div key={i} className="bg-slate-50 rounded p-2 border border-slate-100">
                <div className="font-medium text-slate-700">{test.name}</div>
                <div className="text-xs text-slate-500 mt-0.5">{test.description}</div>
                {test.benchmarks && (
                  <div className="flex gap-3 mt-1 text-xs">
                    {Object.entries(test.benchmarks).map(([level, value]) => (
                      <span key={level} className="bg-white px-1.5 py-0.5 rounded border border-slate-200">
                        {level}: <span className="font-mono">{value}</span>
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>}
    </div>
  );
}
