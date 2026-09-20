import React, { useState, useEffect } from 'react';
import { getAllScenarios, loadResults, saveResult, resetResults, downloadUATResults, UATScenario } from '../lib/uat_scenarios';
import { X, Check, XCircle, RotateCcw, ClipboardList, Download } from 'lucide-react';

interface UATRunnerProps {
  onClose: () => void;
  onLoadScenario: (inputs: Record<string, any>) => void;
}

export function UATRunner({ onClose, onLoadScenario }: UATRunnerProps) {
  const [activeId, setActiveId] = useState<string | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);
  const results = loadResults();
  const scenarios = getAllScenarios();

  const active = scenarios.find(s => s.id === activeId);

  const completedCount = scenarios.filter(s => {
    const r = results[s.id];
    if (!r) return false;
    const checks = Object.fromEntries(Object.entries(r).filter(([k]) => !k.startsWith('_')));
    return Object.keys(checks).length > 0 && Object.values(checks).every(v => v === true);
  }).length;

  const totalCount = scenarios.reduce((acc, s) => acc + s.checks.length, 0);
  const passedCount = scenarios.reduce((acc, s) => {
    const r = results[s.id];
    if (!r) return acc;
    const checks = Object.fromEntries(Object.entries(r).filter(([k]) => !k.startsWith('_')));
    return acc + Object.values(checks).filter(v => v === true).length;
  }, 0);

  const handleToggle = (scenarioId: string, key: string, value: boolean) => {
    saveResult(scenarioId, key, value);
    setRefreshKey(k => k + 1);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-8 pb-8 bg-black/40 overflow-y-auto">
      <div className="bg-white rounded-xl shadow-2xl border border-slate-200 w-full max-w-3xl max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-5 py-4 border-b border-slate-200 bg-slate-50 rounded-t-xl">
          <div className="flex items-center gap-2">
            <ClipboardList className="w-5 h-5 text-indigo-600" />
            <h2 className="text-lg font-bold text-slate-900">UAT Test Runner</h2>
            <span className="text-xs text-slate-500 ml-2">
              {completedCount}/{scenarios.length} scenarios complete &middot; {passedCount}/{totalCount} checks passed
            </span>
          </div>
          <div className="flex items-center gap-2">
            <button onClick={downloadUATResults} className="flex items-center gap-1 text-xs text-indigo-600 hover:text-indigo-800 px-2 py-1 rounded hover:bg-indigo-50 transition-colors">
              <Download className="w-3 h-3" /> Export JSON
            </button>
            <button onClick={() => { resetResults(); setRefreshKey(k => k + 1); }} className="flex items-center gap-1 text-xs text-slate-500 hover:text-red-600 px-2 py-1 rounded hover:bg-red-50 transition-colors">
              <RotateCcw className="w-3 h-3" /> Reset
            </button>
            <button onClick={onClose} className="text-slate-400 hover:text-slate-700 p-1 rounded hover:bg-slate-200 transition-colors">
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        <div className="flex flex-1 min-h-0 overflow-hidden">
          {/* Scenario list */}
          <div className="w-56 flex-none border-r border-slate-200 overflow-y-auto bg-slate-50">
            {scenarios.map(s => {
              const r = results[s.id];
              const checks = r ? Object.fromEntries(Object.entries(r).filter(([k]) => !k.startsWith('_'))) : {};
              const done = Object.keys(checks).length > 0 && Object.values(checks).every(v => v === true);
              const anyFail = Object.values(checks).some(v => v === false);
              return (
                <button
                  key={s.id}
                  onClick={() => setActiveId(s.id)}
                  className={`w-full text-left px-3 py-2.5 text-xs border-b border-slate-100 hover:bg-slate-100 transition-colors ${activeId === s.id ? 'bg-white font-semibold text-indigo-700 shadow-sm' : 'text-slate-700'}`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-bold">{s.id}</span>
                    {done ? <Check className="w-3 h-3 text-emerald-500" /> : anyFail ? <XCircle className="w-3 h-3 text-red-400" /> : null}
                  </div>
                  <div className="text-slate-400 truncate mt-0.5">{s.title}</div>
                </button>
              );
            })}
          </div>

          {/* Detail panel */}
          <div className="flex-1 overflow-y-auto p-5">
            {!active && (
              <div className="text-center text-slate-400 pt-12">
                <ClipboardList className="w-12 h-12 mx-auto mb-3 opacity-40" />
                <p className="font-semibold">Select a scenario</p>
                <p className="text-xs mt-1">Click a scenario to run through its checklist</p>
              </div>
            )}
            {active && <ScenarioDetail scenario={active} results={results[active.id] || {}} onToggle={(k, v) => handleToggle(active.id, k, v)} onLoad={() => onLoadScenario(active.inputs)} />}
          </div>
        </div>
      </div>
    </div>
  );
}

function ScenarioDetail({ scenario, results, onToggle, onLoad }: {
  scenario: UATScenario;
  results: Record<string, boolean | string>;
  onToggle: (key: string, value: boolean) => void;
  onLoad: () => void;
}) {
  const allPassed = scenario.checks.every(c => results[c.key] === true);

  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-lg font-bold text-slate-900">
            <span className="text-indigo-600">{scenario.id}</span> — {scenario.title}
          </h3>
          <p className="text-sm text-slate-500 mt-1">{scenario.description}</p>
        </div>
        <span className={`text-[10px] font-bold uppercase px-2 py-1 rounded ${scenario.tier === 'core' ? 'bg-blue-100 text-blue-700' : scenario.tier === 'premium' ? 'bg-purple-100 text-purple-700' : 'bg-amber-100 text-amber-700'}`}>
          {scenario.tier}
        </span>
      </div>

      {/* Load inputs button */}
      <button onClick={onLoad} className="mb-4 flex items-center gap-1.5 text-xs font-semibold text-indigo-600 bg-indigo-50 border border-indigo-200 px-3 py-1.5 rounded-md hover:bg-indigo-100 transition-colors">
        <ClipboardList className="w-3.5 h-3.5" /> Load into Form
      </button>

      {/* Checklist */}
      <div className="space-y-2 mb-4">
        {scenario.checks.map(check => (
          <div key={check.key} className="flex items-center justify-between p-2.5 rounded-lg border border-slate-200 bg-white">
            <span className="text-sm text-slate-700">{check.label}</span>
            <div className="flex items-center gap-1">
              <button
                onClick={() => onToggle(check.key, true)}
                className={`px-2.5 py-1 text-xs font-bold rounded transition-colors ${results[check.key] === true ? 'bg-emerald-100 text-emerald-700 ring-2 ring-emerald-300' : 'bg-slate-100 text-slate-400 hover:bg-emerald-50 hover:text-emerald-600'}`}
              >
                Pass
              </button>
              <button
                onClick={() => onToggle(check.key, false)}
                className={`px-2.5 py-1 text-xs font-bold rounded transition-colors ${results[check.key] === false ? 'bg-red-100 text-red-700 ring-2 ring-red-300' : 'bg-slate-100 text-slate-400 hover:bg-red-50 hover:text-red-600'}`}
              >
                Fail
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Pass criteria & status */}
      <div className="p-3 rounded-lg bg-slate-50 border border-slate-200">
        <p className="text-xs text-slate-500 mb-2">
          <span className="font-semibold text-slate-700">Pass criteria:</span> {scenario.passCriteria}
        </p>
        <div className={`text-xs font-bold px-2 py-1 rounded inline-block ${allPassed ? 'bg-emerald-100 text-emerald-700' : 'bg-slate-200 text-slate-500'}`}>
          {allPassed ? '✓ All checks pass' : `${scenario.checks.filter(c => results[c.key] === true).length}/${scenario.checks.length} checks passed`}
        </div>
      </div>
    </div>
  );
}
