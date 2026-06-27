import React, { useState } from 'react';
import { Settings, X } from 'lucide-react';
import type { CoachPreferences } from '../../types/api';

const STORAGE_KEY = 'forge_coach_preferences';

const DEFAULTS: CoachPreferences = {
  preferredDeadlift: undefined,
  preferredSquat: undefined,
  preferredPress: undefined,
  avoidOlympicLifts: false,
  avoidHighSorenessNearMatch: false,
  minSprintExposuresPerWeek: 1,
  preferredConditioningStyle: 'mixed',
  biasUnilateralWork: false,
  preferVelocityBasedLoading: false,
  preferredTempo: '20X0',
  preferredRestBetweenSets: 90,
};

export function loadPreferences(): CoachPreferences {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? { ...DEFAULTS, ...JSON.parse(raw) } : { ...DEFAULTS };
  } catch { return { ...DEFAULTS }; }
}

type DeadliftOpt = CoachPreferences['preferredDeadlift'];
type SquatOpt = CoachPreferences['preferredSquat'];
type PressOpt = CoachPreferences['preferredPress'];
type CondStyle = CoachPreferences['preferredConditioningStyle'];

const inputCls = 'w-full px-3 py-2 text-sm rounded-md border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-300 bg-white';
const labelCls = 'block text-xs font-medium text-slate-600 mb-1';

export default function CoachPreferencesModal({ onClose }: { onClose: () => void }) {
  const [prefs, setPrefs] = useState<CoachPreferences>(loadPreferences());

  const update = <K extends keyof CoachPreferences>(key: K, val: CoachPreferences[K]) =>
    setPrefs(prev => ({ ...prev, [key]: val }));

  const handleSave = () => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(prefs));
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 flex items-center justify-center" onClick={onClose}>
      <div className="bg-white rounded-2xl shadow-2xl w-[580px] max-h-[85vh] flex flex-col" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between px-5 py-4 border-b border-slate-200">
          <h2 className="text-sm font-bold text-slate-900 flex items-center gap-2"><Settings className="w-4 h-4" /> Coach Preferences</h2>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600"><X className="w-4 h-4" /></button>
        </div>

        <div className="flex-1 overflow-y-auto px-5 py-4 space-y-5">
          <p className="text-xs text-slate-400">Preferences persist in this browser and are sent with every generation request. Override per-program in the form below.</p>

          {/* Exercise Variants */}
          <fieldset className="border border-slate-200 rounded-xl p-4 space-y-4">
            <legend className="text-xs font-bold text-slate-500 uppercase tracking-wider px-1">Preferred Exercise Variants</legend>
            <div className="grid grid-cols-3 gap-4">
              <div>
                <label className={labelCls}>Deadlift</label>
                <select value={prefs.preferredDeadlift || ''} onChange={e => update('preferredDeadlift', (e.target.value || undefined) as DeadliftOpt)} className={inputCls}>
                  <option value="">Default</option>
                  <option value="trap_bar">Trap Bar</option>
                  <option value="straight_bar">Straight Bar</option>
                  <option value="sumo">Sumo</option>
                  <option value="none">None</option>
                </select>
              </div>
              <div>
                <label className={labelCls}>Squat</label>
                <select value={prefs.preferredSquat || ''} onChange={e => update('preferredSquat', (e.target.value || undefined) as SquatOpt)} className={inputCls}>
                  <option value="">Default</option>
                  <option value="barbell">Barbell</option>
                  <option value="goblet">Goblet</option>
                  <option value="hack">Hack</option>
                  <option value="none">None</option>
                </select>
              </div>
              <div>
                <label className={labelCls}>Press</label>
                <select value={prefs.preferredPress || ''} onChange={e => update('preferredPress', (e.target.value || undefined) as PressOpt)} className={inputCls}>
                  <option value="">Default</option>
                  <option value="barbell">Barbell</option>
                  <option value="dumbbell">Dumbbell</option>
                  <option value="landmine">Landmine</option>
                  <option value="none">None</option>
                </select>
              </div>
            </div>
          </fieldset>

          {/* Avoidance */}
          <fieldset className="border border-slate-200 rounded-xl p-4 space-y-3">
            <legend className="text-xs font-bold text-slate-500 uppercase tracking-wider px-1">Avoidance</legend>
            <label className="flex items-center gap-3 cursor-pointer">
              <input type="checkbox" checked={prefs.avoidOlympicLifts || false} onChange={e => update('avoidOlympicLifts', e.target.checked)}
                className="w-4 h-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500" />
              <span className="text-sm text-slate-700">Avoid Olympic Lifts</span>
            </label>
            <label className="flex items-center gap-3 cursor-pointer">
              <input type="checkbox" checked={prefs.avoidHighSorenessNearMatch || false} onChange={e => update('avoidHighSorenessNearMatch', e.target.checked)}
                className="w-4 h-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500" />
              <span className="text-sm text-slate-700">Avoid high-soreness work near match day</span>
            </label>
          </fieldset>

          {/* Exposure Preferences */}
          <fieldset className="border border-slate-200 rounded-xl p-4 space-y-4">
            <legend className="text-xs font-bold text-slate-500 uppercase tracking-wider px-1">Exposure & Conditioning</legend>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className={labelCls}>Min sprint exposures / week</label>
                <input type="number" min={0} max={3} value={prefs.minSprintExposuresPerWeek ?? 1}
                  onChange={e => update('minSprintExposuresPerWeek', Number(e.target.value))} className={inputCls} />
              </div>
              <div>
                <label className={labelCls}>Conditioning Style</label>
                <select value={prefs.preferredConditioningStyle || 'mixed'} onChange={e => update('preferredConditioningStyle', e.target.value as CondStyle)} className={inputCls}>
                  <option value="low_intensity">Low Intensity (extensive)</option>
                  <option value="high_intensity">High Intensity (HIIT)</option>
                  <option value="mixed">Mixed</option>
                </select>
              </div>
            </div>
          </fieldset>

          {/* Philosophy */}
          <fieldset className="border border-slate-200 rounded-xl p-4 space-y-3">
            <legend className="text-xs font-bold text-slate-500 uppercase tracking-wider px-1">Philosophical</legend>
            <label className="flex items-center gap-3 cursor-pointer">
              <input type="checkbox" checked={prefs.biasUnilateralWork || false} onChange={e => update('biasUnilateralWork', e.target.checked)}
                className="w-4 h-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500" />
              <span className="text-sm text-slate-700">Bias unilateral work (single-leg deadlift, split squat, lunges)</span>
            </label>
            <label className="flex items-center gap-3 cursor-pointer">
              <input type="checkbox" checked={prefs.preferVelocityBasedLoading || false} onChange={e => update('preferVelocityBasedLoading', e.target.checked)}
                className="w-4 h-4 rounded border-slate-300 text-indigo-600 focus:ring-indigo-500" />
              <span className="text-sm text-slate-700">Prefer velocity-based loading prescriptions</span>
            </label>
          </fieldset>

          {/* General */}
          <fieldset className="border border-slate-200 rounded-xl p-4 space-y-4">
            <legend className="text-xs font-bold text-slate-500 uppercase tracking-wider px-1">General Prescription Defaults</legend>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className={labelCls}>Preferred Tempo</label>
                <input type="text" value={prefs.preferredTempo || ''} onChange={e => update('preferredTempo', e.target.value)}
                  placeholder="e.g. 20X0" className={inputCls} />
              </div>
              <div>
                <label className={labelCls}>Rest Between Sets (seconds)</label>
                <input type="number" min={30} max={300} step={15} value={prefs.preferredRestBetweenSets ?? 90}
                  onChange={e => update('preferredRestBetweenSets', Number(e.target.value))} className={inputCls} />
              </div>
            </div>
          </fieldset>
        </div>

        <div className="flex justify-end gap-3 px-5 py-4 border-t border-slate-200">
          <button onClick={onClose} className="px-4 py-2 text-sm font-medium text-slate-600 hover:bg-slate-100 rounded-lg transition-colors">Cancel</button>
          <button onClick={handleSave} className="px-6 py-2 text-sm font-medium bg-slate-900 text-white hover:bg-slate-800 rounded-lg transition-colors flex items-center gap-2">
            <Settings className="w-3.5 h-3.5" /> Save Preferences
          </button>
        </div>
      </div>
    </div>
  );
}
