import React, { useState, useMemo } from 'react';
import { SavedProgramArtifact, TransformationResult, SessionVM, ExerciseVM, CoachOverrides } from '../../../types/ui';
import { GitCompare, AlertCircle, ArrowRight, Activity, CalendarDays, Target, Box, Lock, MessageSquarePlus, Edit2, Repeat, Plus, Minus, RotateCcw } from 'lucide-react';

interface CompareModeProps {
  currentResult: TransformationResult;
  savedPrograms: SavedProgramArtifact[];
}

export function CompareMode({ currentResult, savedPrograms }: CompareModeProps) {
  const currentVM = currentResult.viewModel;
  const [selectedPriorId, setSelectedPriorId] = useState<string>(
     savedPrograms.length > 0 ? savedPrograms[0].id : ''
  );

  const priorProgram = savedPrograms.find(p => p.id === selectedPriorId);
  const priorVM = priorProgram?.result_snapshot?.viewModel;

  const compareResult = useMemo(() => {
    if (!currentVM || !priorVM) return null;
    return buildCompare(currentVM, priorVM, currentResult, priorProgram);
  }, [currentVM, priorVM, currentResult, priorProgram]);

  return (
    <div className="space-y-6">
       
       <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm flex flex-col md:flex-row gap-6 items-start">
          <div className="flex-1">
             <h3 className="text-sm font-bold text-slate-500 uppercase tracking-wider mb-2">Current Active Artifact</h3>
             <div className="text-xl font-bold text-slate-900">{currentVM?.summary.blueprint_selected}</div>
             <div className="text-sm text-slate-600 border-b border-slate-100 pb-2 mb-2">
                {currentVM?.summary.total_weeks} Weeks | {currentVM?.summary.weekly_frequency}x/wk
             </div>
             <div className="grid grid-cols-2 gap-2 mt-3">
                <div className="text-xs">
                   <div className="text-slate-400 uppercase tracking-wider text-[10px] font-bold">Sessions</div>
                   <div className="font-semibold text-slate-800">{currentVM?.sessions.length}</div>
                </div>
                <div className="text-xs">
                   <div className="text-slate-400 uppercase tracking-wider text-[10px] font-bold">Validations</div>
                   <div className="font-semibold text-slate-800">{currentVM?.validation.length}</div>
                </div>
             </div>
          </div>
          
          <div className="hidden md:flex flex-col justify-center items-center px-4 self-stretch text-slate-300">
             <GitCompare className="w-8 h-8" />
             <div className="text-xs font-bold uppercase mt-2">VS</div>
          </div>

          <div className="flex-1 w-full relative">
             <h3 className="text-sm font-bold text-slate-500 uppercase tracking-wider mb-2">Baseline Comparison</h3>
             <select 
               value={selectedPriorId} 
               onChange={(e) => setSelectedPriorId(e.target.value)}
               className="w-full text-base font-bold text-indigo-900 bg-indigo-50 border border-indigo-200 rounded-md p-2 shadow-sm focus:ring focus:ring-indigo-200"
             >
               <option value="" disabled>Select an artifact to compare...</option>
               {savedPrograms.map(p => (
                 <option key={p.id} value={p.id}>
                    {p.athlete_display_name} - {p.blueprint_label} ({new Date(p.created_at).toLocaleDateString()})
                 </option>
               ))}
             </select>
             
             {priorProgram && (
                <>
                  <div className="text-sm text-slate-600 border-b border-slate-100 pb-2 mb-2 mt-2">
                     {priorVM?.summary.total_weeks} Weeks | {priorVM?.summary.weekly_frequency}x/wk
                  </div>
                  <div className="grid grid-cols-2 gap-2 mt-3">
                     <div className="text-xs">
                        <div className="text-slate-400 uppercase tracking-wider text-[10px] font-bold">Sessions</div>
                        <div className="font-semibold text-slate-800">{priorVM?.sessions.length}</div>
                     </div>
                     <div className="text-xs">
                        <div className="text-slate-400 uppercase tracking-wider text-[10px] font-bold">Validations</div>
                        <div className="font-semibold text-slate-800">{priorVM?.validation.length}</div>
                     </div>
                  </div>
                </>
             )}
          </div>
       </div>

       {!compareResult ? (
          <div className="text-center p-12 bg-white rounded-xl border border-dashed border-slate-300">
             <Box className="w-10 h-10 mx-auto text-slate-300 mb-4" />
             <p className="text-slate-500 font-medium">Select a saved artifact to see structural differences.</p>
          </div>
       ) : (
          <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
             <div className="px-6 py-4 bg-slate-50 border-b border-slate-200 flex justify-between items-center">
                <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider flex items-center gap-2">
                   <Activity className="w-4 h-4 text-slate-500" /> Structural Delta
                </h3>
                <span className="text-xs text-slate-400 bg-slate-100 px-2 py-1 rounded">
                  {compareResult.changedCount} change{compareResult.changedCount !== 1 ? 's' : ''}
                </span>
             </div>
             
             <div className="p-6 space-y-8">

                {/* High-level structure */}
                <div>
                  <h4 className="flex items-center text-xs font-bold uppercase tracking-wider text-slate-500 mb-3 border-b border-slate-100 pb-1">
                     <Target className="w-3 h-3 mr-1.5" /> High-Level Structure
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <DiffRow label="Duration" prior={`${priorVM?.summary.total_weeks} Weeks`} current={`${currentVM?.summary.total_weeks} Weeks`} />
                      <DiffRow label="Frequency" prior={`${priorVM?.summary.weekly_frequency}x/wk`} current={`${currentVM?.summary.weekly_frequency}x/wk`} />
                      <DiffRow label="Goal" prior={priorProgram?.goal || '-'} current={currentVM?.summary.blueprint_selected || '-'} />
                    </div>
                    <div className="space-y-2">
                      <DiffRow label="Blueprint" prior={priorVM?.summary.blueprint_selected} current={currentVM?.summary.blueprint_selected} />
                      <DiffRow label="Conditioning Emphasis" prior={priorVM?.summary.conditioning_emphasis} current={currentVM?.summary.conditioning_emphasis} />
                      <DiffRow label="Competition Window" prior={priorVM?.summary.competition_window} current={currentVM?.summary.competition_window} />
                    </div>
                  </div>
                </div>

                {/* Week/Session structure */}
                {compareResult.weekDiffs.length > 0 && (
                  <div>
                    <h4 className="flex items-center text-xs font-bold uppercase tracking-wider text-slate-500 mb-3 border-b border-slate-100 pb-1">
                       <CalendarDays className="w-3 h-3 mr-1.5" /> Weekly & Session Changes
                    </h4>
                    <div className="space-y-3">
                      {compareResult.weekDiffs.map((wd, i) => (
                        <div key={i} className="bg-slate-50 rounded-lg p-4 border border-slate-200">
                          <div className="text-sm font-bold text-slate-800 mb-2">{wd.label}</div>
                          <div className="space-y-1.5">
                            {wd.changes.map((c, j) => (
                              <DiffRow key={j} label={c.label} prior={c.prior} current={c.current} />
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Exercise changes by week */}
                {compareResult.exerciseDiffs.length > 0 && (
                  <div>
                    <h4 className="flex items-center text-xs font-bold uppercase tracking-wider text-slate-500 mb-3 border-b border-slate-100 pb-1">
                       <Repeat className="w-3 h-3 mr-1.5" /> Exercise Changes
                    </h4>
                    <div className="space-y-4">
                      {compareResult.exerciseDiffs.map((ed, i) => (
                        <div key={i} className="bg-white rounded-lg border border-slate-200 overflow-hidden">
                          <div className="bg-slate-100 px-4 py-2 text-xs font-bold text-slate-700 flex items-center gap-2 border-b border-slate-200">
                            <Activity className="w-3 h-3" /> {ed.sessionName}
                          </div>
                          <div className="divide-y divide-slate-100">
                            {ed.added.map((ex, j) => (
                              <div key={`add-${j}`} className="px-4 py-2 flex items-center gap-2 text-sm bg-emerald-50">
                                <Plus className="w-3 h-3 text-emerald-600 shrink-0" />
                                <span className="text-emerald-800 font-medium">{ex}</span>
                                <span className="text-[10px] text-emerald-600 font-bold uppercase ml-auto">Added</span>
                              </div>
                            ))}
                            {ed.removed.map((ex, j) => (
                              <div key={`rem-${j}`} className="px-4 py-2 flex items-center gap-2 text-sm bg-red-50">
                                <Minus className="w-3 h-3 text-red-600 shrink-0" />
                                <span className="text-red-800 font-medium line-through">{ex}</span>
                                <span className="text-[10px] text-red-600 font-bold uppercase ml-auto">Removed</span>
                              </div>
                            ))}
                            {ed.swapped.map((ex, j) => (
                              <div key={`swp-${j}`} className="px-4 py-2 flex items-center gap-2 text-sm bg-indigo-50">
                                <Repeat className="w-3 h-3 text-indigo-600 shrink-0" />
                                <span className="text-indigo-800 font-medium">{ex}</span>
                                <span className="text-[10px] text-indigo-600 font-bold uppercase ml-auto">Swapped</span>
                              </div>
                            ))}
                            {ed.changedPrescription.map((ex, j) => (
                              <div key={`pre-${j}`} className="px-4 py-2 flex items-center gap-2 text-sm bg-amber-50">
                                <Edit2 className="w-3 h-3 text-amber-600 shrink-0" />
                                <span className="text-amber-800 font-medium">{ex}</span>
                                <span className="text-[10px] text-amber-600 font-bold uppercase ml-auto">Prescription</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Adaptation diff from rawPayload */}
                {currentResult.rawPayload?.adaptation?.changes?.length > 0 && (
                  <div>
                    <h4 className="flex items-center text-xs font-bold uppercase tracking-wider text-slate-500 mb-3 border-b border-slate-100 pb-1">
                       <RotateCcw className="w-3 h-3 mr-1.5" /> Adaptation Log
                    </h4>
                    <div className="bg-slate-50 rounded-lg p-4 border border-slate-200">
                      <div className="space-y-1.5">
                        {currentResult.rawPayload.adaptation.changes.map((c: string, i: number) => (
                          <div key={i} className="flex items-start gap-2 text-sm">
                            <ArrowRight className="w-3 h-3 text-indigo-400 shrink-0 mt-0.5" />
                            <span className="text-slate-700">{c}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

                {/* Coach Override diffs */}
                {compareResult.overrideDiffs.length > 0 && (
                  <div>
                    <h4 className="flex items-center text-xs font-bold uppercase tracking-wider text-slate-500 mb-3 border-b border-slate-100 pb-1">
                       <Lock className="w-3 h-3 mr-1.5" /> Coach Override Differences
                    </h4>
                    <div className="space-y-2">
                      {compareResult.overrideDiffs.map((od, i) => (
                        <DiffRow key={i} label={od.label} prior={od.prior} current={od.current} />
                      ))}
                    </div>
                  </div>
                )}

                {/* Validation Diffs */}
                <div>
                  <h4 className="flex items-center text-xs font-bold uppercase tracking-wider text-slate-500 mb-3 border-b border-slate-100 pb-1">
                     <AlertCircle className="w-3 h-3 mr-1.5" /> Validation & Diagnostics
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <div className="text-[10px] uppercase font-bold text-slate-400 tracking-wider mb-2">Previous</div>
                      <ul className="space-y-1">
                         {priorVM?.validation.length === 0 ? <li className="text-xs text-emerald-600">Clean</li> : priorVM?.validation.map((v: any, i: number) => (
                           <li key={i} className={`text-xs ${compareResult.newValidations.includes(v.message) ? 'line-through text-red-400' : 'text-slate-600'}`}>{v.message}</li>
                         ))}
                      </ul>
                    </div>
                    <div>
                      <div className="text-[10px] uppercase font-bold text-slate-400 tracking-wider mb-2">Current</div>
                      <ul className="space-y-1">
                         {currentVM?.validation.length === 0 ? <li className="text-xs text-emerald-600">Clean</li> : currentVM?.validation.map((v: any, i: number) => (
                           <li key={i} className={`text-xs ${compareResult.removedValidations.includes(v.message) ? 'text-emerald-600 font-medium' : 'text-slate-600'}`}>
                             {v.message}
                             {compareResult.newValidations.includes(v.message) && <span className="text-amber-600 ml-1 text-[10px] font-bold uppercase">(New)</span>}
                           </li>
                         ))}
                      </ul>
                    </div>
                  </div>
                </div>

                {/* No changes found */}
                {compareResult.changedCount === 0 && (
                  <div className="text-center py-6 text-slate-400 text-sm italic">
                    No structural differences found between these artifacts.
                  </div>
                )}
             </div>
          </div>
       )}
    </div>
  );
}

function DiffRow({ label, prior, current }: { label: string, prior: string | undefined, current: string | undefined }) {
  const isChanged = prior !== current;

  if (!isChanged) return null;

  return (
     <li className="flex flex-col text-sm list-none">
        <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider w-full mb-0.5">{label}</span>
        <div className="flex items-center gap-2">
           <span className="text-slate-500 line-through decoration-slate-300">{prior || '(none)'}</span>
           <ArrowRight className="w-3 h-3 text-indigo-400 shrink-0" />
           <span className="font-semibold text-indigo-700 bg-indigo-50 px-1.5 py-0.5 rounded">{current || '(none)'}</span>
        </div>
     </li>
  );
}

interface WeekDiff {
  label: string;
  changes: { label: string; prior: string; current: string }[];
}

interface ExerciseDiff {
  sessionName: string;
  added: string[];
  removed: string[];
  swapped: string[];
  changedPrescription: string[];
}

interface OverrideDiff {
  label: string;
  prior: string;
  current: string;
}

interface CompareResult {
  changedCount: number;
  weekDiffs: WeekDiff[];
  exerciseDiffs: ExerciseDiff[];
  overrideDiffs: OverrideDiff[];
  newValidations: string[];
  removedValidations: string[];
}

function buildCompare(currentVM: any, priorVM: any, currentResult: TransformationResult, priorProgram?: SavedProgramArtifact): CompareResult {
  const weekDiffs: WeekDiff[] = [];
  const exerciseDiffs: ExerciseDiff[] = [];
  const overrideDiffs: OverrideDiff[] = [];
  const newValidations: string[] = [];
  const removedValidations: string[] = [];
  let changedCount = 0;

  // — Week comparison —
  const priorWeeks = priorVM?.weeks || [];
  const currentWeeks = currentVM?.weeks || [];
  const allWeekNums = new Set([
    ...priorWeeks.map((w: any) => w.week_number),
    ...currentWeeks.map((w: any) => w.week_number)
  ]);

  for (const wn of allWeekNums) {
    const pw = priorWeeks.find((w: any) => w.week_number === wn);
    const cw = currentWeeks.find((w: any) => w.week_number === wn);
    const changes: { label: string; prior: string; current: string }[] = [];

    if (!pw) {
      changes.push({ label: 'Status', prior: '(not present)', current: 'Added' });
    } else if (!cw) {
      changes.push({ label: 'Status', prior: 'Present', current: '(removed)' });
    } else {
      if (pw.exposure_summary?.week_type !== cw.exposure_summary?.week_type) {
        changes.push({ label: 'Week Type', prior: pw.exposure_summary.week_type || '-', current: cw.exposure_summary.week_type || '-' });
      }
      if ((pw.sessions?.length || 0) !== (cw.sessions?.length || 0)) {
        changes.push({ label: 'Session Count', prior: `${pw.sessions?.length || 0}`, current: `${cw.sessions?.length || 0}` });
      }
      if (pw.exposure_summary?.sprint_exposure !== cw.exposure_summary?.sprint_exposure) {
        changes.push({ label: 'Sprint Exposure', prior: pw.exposure_summary?.sprint_exposure || '-', current: cw.exposure_summary?.sprint_exposure || '-' });
      }
      if (pw.exposure_summary?.conditioning_density !== cw.exposure_summary?.conditioning_density) {
        changes.push({ label: 'Cond. Density', prior: pw.exposure_summary?.conditioning_density || '-', current: cw.exposure_summary?.conditioning_density || '-' });
      }
    }

    if (changes.length > 0) {
      const label = pw?.label || cw?.label || `Week ${wn}`;
      weekDiffs.push({ label, changes });
      changedCount += changes.length;
    }
  }

  // — Exercise comparison (by session) —
  const priorSessions = priorVM?.sessions || [];
  const currentSessions = currentVM?.sessions || [];
  const allSessionIds = new Set([
    ...priorSessions.map((s: any) => s.id),
    ...currentSessions.map((s: any) => s.id)
  ]);

  for (const sid of allSessionIds) {
    const ps = priorSessions.find((s: any) => s.id === sid);
    const cs = currentSessions.find((s: any) => s.id === sid);
    const added: string[] = [];
    const removed: string[] = [];
    const swapped: string[] = [];
    const changedPrescription: string[] = [];

    const priorExercises = ps ? [...(ps.main_work?.exercises || []), ...(ps.warmup?.exercises || []), ...(ps.conditioning?.exercises || [])] : [];
    const currentExercises = cs ? [...(cs.main_work?.exercises || []), ...(cs.warmup?.exercises || []), ...(cs.conditioning?.exercises || [])] : [];

    const priorNames = new Set(priorExercises.map((e: any) => e.name));
    const currentNames = new Set(currentExercises.map((e: any) => e.name));

    for (const e of currentExercises) {
      if (!priorNames.has(e.name)) added.push(e.name);
    }
    for (const e of priorExercises) {
      if (!currentNames.has(e.name)) removed.push(e.name);
    }

    // Check prescription changes for same-named exercises
    if (ps && cs) {
      const priorMain = ps.main_work?.exercises || [];
      const currentMain = cs.main_work?.exercises || [];
      for (const ce of currentMain) {
        const pe = priorMain.find((e: any) => e.name === ce.name);
        if (pe) {
          if (pe.sets_reps !== ce.sets_reps || pe.loading_method !== ce.loading_method || pe.rest !== ce.rest) {
            changedPrescription.push(`${ce.name} (prescription changed)`);
          }
        }
      }
    }

    if (added.length > 0 || removed.length > 0 || swapped.length > 0 || changedPrescription.length > 0) {
      const sessionName = cs?.name || ps?.name || sid;
      exerciseDiffs.push({ sessionName, added, removed, swapped, changedPrescription });
      changedCount += added.length + removed.length + swapped.length + changedPrescription.length;
    }
  }

  // — Coach override diffs (nested sessions model) —
  const priorOverrides: CoachOverrides = priorProgram?.coach_overrides || {};
  const priorOverrideSessions = priorOverrides.sessions || {};
  let totalPriorOverrides = 0;
  for (const sid of Object.keys(priorOverrideSessions)) {
    const so = priorOverrideSessions[sid];
    if (so.locked) totalPriorOverrides++;
    if (so.note) totalPriorOverrides++;
    const exs = so.exercises || {};
    for (const exId of Object.keys(exs)) {
      if (exs[exId].swap) totalPriorOverrides++;
      if (exs[exId].prescription) totalPriorOverrides++;
    }
  }

  if (totalPriorOverrides > 0) {
    overrideDiffs.push({ label: 'Coach Overrides', prior: `${totalPriorOverrides} override(s) applied`, current: 'Base (no overrides)' });
    changedCount++;
  }

  // — Validation diffs —
  const priorMsgs = new Set<string>((priorVM?.validation || []).map((v: any) => v.message));
  const currentMsgs = new Set<string>((currentVM?.validation || []).map((v: any) => v.message));

  for (const m of currentMsgs) {
    if (!priorMsgs.has(m)) {
      newValidations.push(m);
      changedCount++;
    }
  }
  for (const m of priorMsgs) {
    if (!currentMsgs.has(m)) {
      removedValidations.push(m);
      changedCount++;
    }
  }

  return { changedCount, weekDiffs, exerciseDiffs, overrideDiffs, newValidations, removedValidations };
}
