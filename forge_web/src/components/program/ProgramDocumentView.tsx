import React from 'react';
import { X, Printer, Download } from 'lucide-react';
import { SavedProgramArtifact } from '../../types/ui';
import { ExerciseRow } from '../session/blocks';

interface ProgramDocumentViewProps {
  artifact: SavedProgramArtifact;
  onClose: () => void;
}

export function ProgramDocumentView({ artifact, onClose }: ProgramDocumentViewProps) {
  const result = artifact.result_snapshot;
  const { viewModel } = result;

  if (!viewModel) return null;

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="fixed inset-0 bg-slate-900 z-50 flex flex-col overflow-hidden">
      {/* Top Bar - Hidden when printing */}
      <div className="print:hidden flex items-center justify-between bg-slate-950 px-6 py-3 border-b border-slate-800 shrink-0 text-white">
         <div className="font-medium text-slate-300">Document Preview <span className="text-slate-500 ml-2">v{artifact.version} - {artifact.status.toUpperCase()}</span></div>
         <div className="flex gap-3">
            <button onClick={handlePrint} className="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded text-sm transition-colors">
               <Printer className="w-4 h-4" /> Print Document
            </button>
            <button onClick={onClose} className="p-2 border border-slate-700 bg-slate-900 hover:bg-slate-800 rounded transition-colors text-slate-300">
               <X className="w-5 h-5" />
            </button>
         </div>
      </div>

      {/* Scrollable Document Area Container */}
      <div className="flex-1 overflow-y-auto bg-slate-200 print:bg-white print:overflow-visible p-8 print:p-0">
          {/* Document Auto-scaling Container */}
          <div className="max-w-[850px] mx-auto bg-white shadow-xl print:shadow-none min-h-[1100px] p-12 print:p-0">
              
              {/* Document Header */}
              <div className="border-b-4 border-slate-900 pb-6 mb-8">
                 <div className="flex justify-between items-end mb-4">
                    <div>
                       <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight leading-none mb-2">FORGE Output Document</h1>
                       <div className="text-xl font-medium text-slate-500">{viewModel.summary.blueprint_selected}</div>
                    </div>
                    <div className="text-right">
                       <div className="text-2xl font-bold text-slate-900">{artifact.athlete_display_name}</div>
                       <div className="text-sm font-medium text-slate-500">{artifact.sport} • {artifact.role}</div>
                    </div>
                 </div>
                 
                 <div className="grid grid-cols-4 gap-4 text-sm mt-6 border-t border-slate-200 pt-6">
                    <div>
                       <div className="font-bold text-slate-400 uppercase tracking-wider text-[10px]">Duration / Freq</div>
                       <div className="font-semibold text-slate-800">{viewModel.summary.total_weeks} Weeks @ {viewModel.summary.weekly_frequency}x/wk</div>
                    </div>
                    <div>
                       <div className="font-bold text-slate-400 uppercase tracking-wider text-[10px]">Conditioning Emphasis</div>
                       <div className="font-semibold text-slate-800">{viewModel.summary.conditioning_emphasis}</div>
                    </div>
                    <div>
                       <div className="font-bold text-slate-400 uppercase tracking-wider text-[10px]">Event Window</div>
                       <div className="font-semibold text-slate-800">{viewModel.summary.competition_window}</div>
                    </div>
                    <div>
                        <div className="font-bold text-slate-400 uppercase tracking-wider text-[10px]">Generated For</div>
                        <div className="font-semibold text-slate-800">{artifact.mode === 'premium' ? 'Premium Evaluation' : 'Core Overview'}</div>
                    </div>
                 </div>
              </div>

              {/* Rationale & Validation section if present */}
              {(viewModel.rationale.length > 0 || viewModel.validation.length > 0) && (
                 <div className="mb-10 text-sm">
                    <h3 className="font-bold text-slate-900 uppercase pt-2 border-t-2 border-slate-200 mb-3 block">Coach Protocol Notes</h3>
                    <div className="grid grid-cols-2 gap-8">
                        <div>
                           <div className="font-semibold text-slate-600 mb-2">Prescription Logic</div>
                           <ul className="list-disc pl-4 text-slate-700 space-y-1">
                              {viewModel.rationale.slice(0, 3).map((r, i) => <li key={i}>{r}</li>)}
                           </ul>
                        </div>
                        {artifact.coach_notes && (
                           <div>
                              <div className="font-semibold text-slate-600 mb-2">Internal Notes</div>
                              <div className="text-slate-700 italic border-l-2 border-slate-300 pl-3">
                                 "{artifact.coach_notes}"
                              </div>
                           </div>
                        )}
                    </div>
                 </div>
              )}

              {/* Blocks rendering grouped by session */}
              <div className="space-y-12">
                 {viewModel.sessions.map((sess, i) => (
                    <div key={i} className="break-inside-avoid">
                       <div className="bg-slate-100 p-3 mb-4 rounded border border-slate-300 flex justify-between items-center">
                          <h2 className="text-lg font-bold text-slate-900 uppercase">
                             Session {sess.session_number}: <span className="font-medium">{sess.name}</span>
                          </h2>
                          <span className="text-sm font-semibold text-slate-600 bg-white px-3 py-1 rounded shadow-sm">Focus: {sess.focus}</span>
                       </div>

                       <div className="space-y-6">
                           {/* Using minimal document layout for sessions */}
                           {sess.warmup.exercises.length > 0 && (
                              <div>
                                 <h4 className="text-xs font-bold text-slate-500 uppercase tracking-widest border-b border-slate-300 pb-1 mb-2">Warmup</h4>
                                 <div className="pl-2 border-l-2 border-slate-200">
                                    {sess.warmup.exercises.map((ex, exIdx) => (
                                       <div key={exIdx} className="grid grid-cols-12 gap-2 text-sm py-1 border-b border-slate-50 last:border-0">
                                          <div className="col-span-6 font-medium text-slate-800">{ex.name}</div>
                                          <div className="col-span-3 text-slate-600 font-mono">{ex.sets_reps}</div>
                                          <div className="col-span-3 text-slate-500">{ex.loading_method}</div>
                                       </div>
                                    ))}
                                 </div>
                              </div>
                           )}

                           {sess.main_work.exercises.length > 0 && (
                              <div>
                                 <h4 className="text-xs font-bold text-slate-900 uppercase tracking-widest border-b-2 border-slate-800 pb-1 mb-2">Main Work</h4>
                                 <div className="pl-2 border-l-2 border-slate-800 space-y-2">
                                    {sess.main_work.exercises.map((ex, exIdx) => (
                                       <div key={exIdx} className="grid grid-cols-12 gap-2 text-sm py-2 border-b border-slate-100">
                                          <div className="col-span-5">
                                             <div className="font-bold text-slate-900">{ex.name}</div>
                                             {ex.progression_note && <div className="text-xs text-indigo-700 mt-1 italic">{ex.progression_note}</div>}
                                          </div>
                                          <div className="col-span-2 text-slate-800 font-mono font-bold pt-0.5">{ex.sets_reps}</div>
                                          <div className="col-span-3 text-slate-700 font-medium pt-0.5">{ex.loading_method}</div>
                                          <div className="col-span-2 text-slate-500 text-xs pt-0.5">{ex.rest}</div>
                                       </div>
                                    ))}
                                 </div>
                              </div>
                           )}

                           {sess.conditioning.exercises.length > 0 && (
                              <div>
                                 <h4 className="text-xs font-bold text-slate-500 uppercase tracking-widest border-b border-slate-300 pb-1 mb-2">Conditioning</h4>
                                 <div className="pl-2 border-l-2 border-slate-200">
                                    {sess.conditioning.exercises.map((ex, exIdx) => (
                                       <div key={exIdx} className="grid grid-cols-12 gap-2 text-sm py-1 border-b border-slate-50">
                                          <div className="col-span-6 font-medium text-slate-800">{ex.name}</div>
                                          <div className="col-span-3 text-slate-600 font-mono">{ex.sets_reps}</div>
                                          <div className="col-span-3 text-slate-500">{ex.loading_method}</div>
                                       </div>
                                    ))}
                                 </div>
                                 {sess.conditioning.notes && (
                                    <div className="mt-2 text-sm italic text-slate-600 pl-4">Note: {sess.conditioning.notes}</div>
                                 )}
                              </div>
                           )}
                       </div>
                    </div>
                 ))}
              </div>

              {/* Document Footer */}
              <div className="mt-16 pt-8 border-t-2 border-slate-200 text-center text-xs text-slate-500 print:text-[10px]">
                 FORGE Advanced S&C System • Generated {new Date().toLocaleDateString()} • {artifact.id}
              </div>

          </div>
      </div>
    </div>
  );
}
