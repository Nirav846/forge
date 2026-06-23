import React, { useState } from 'react';
import { SavedProgramArtifact, TransformationResult } from '../../../types/ui';
import { GitCompare, AlertCircle, ArrowRight, Activity, CalendarDays, Target, Box } from 'lucide-react';

interface CompareModeProps {
  currentResult: TransformationResult;
  savedPrograms: SavedProgramArtifact[];
}

export function CompareMode({ currentResult, savedPrograms }: React.PropsWithChildren<CompareModeProps>) {
  const currentVM = currentResult.viewModel;
  const [selectedPriorId, setSelectedPriorId] = useState<string>(
     savedPrograms.length > 0 ? savedPrograms[0].id : ''
  );

  const priorProgram = savedPrograms.find(p => p.id === selectedPriorId);

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
                    {p.blueprint_label} ({new Date(p.created_at).toLocaleDateString()}) - {p.status}
                 </option>
               ))}
             </select>
             
             {priorProgram && (
                <>
                  <div className="text-sm text-slate-600 border-b border-slate-100 pb-2 mb-2 mt-2">
                     {priorProgram.result_snapshot.viewModel?.summary.total_weeks} Weeks | {priorProgram.result_snapshot.viewModel?.summary.weekly_frequency}x/wk
                  </div>
                  <div className="grid grid-cols-2 gap-2 mt-3">
                     <div className="text-xs">
                        <div className="text-slate-400 uppercase tracking-wider text-[10px] font-bold">Sessions</div>
                        <div className="font-semibold text-slate-800">{priorProgram.result_snapshot.viewModel?.sessions.length}</div>
                     </div>
                     <div className="text-xs">
                        <div className="text-slate-400 uppercase tracking-wider text-[10px] font-bold">Validations</div>
                        <div className="font-semibold text-slate-800">{priorProgram.result_snapshot.viewModel?.validation.length}</div>
                     </div>
                  </div>
                </>
             )}
          </div>
       </div>

       {/* Diff View */}
       {!priorProgram ? (
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
             </div>
             
             <div className="p-6">
                <p className="text-xs text-slate-400 mb-6 bg-slate-50 p-2 rounded">
                  <AlertCircle className="w-3 h-3 inline mr-1 text-slate-400" />
                  <strong>Note:</strong> This is a frontend-rendered best-effort structural summary using snapshot matching.
                </p>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 divide-x divide-slate-100">
                   
                   {/* Left Col */}
                   <div className="space-y-6">
                      <div>
                         <h4 className="flex items-center text-xs font-bold uppercase tracking-wider text-slate-500 mb-3 border-b border-slate-100 pb-1">
                            <Target className="w-3 h-3 mr-1.5" /> High-Level Structure
                         </h4>
                         <ul className="space-y-3">
                            <DiffRow label="Duration" prior={priorProgram.result_snapshot.viewModel?.summary.total_weeks + ' Weeks'} current={currentVM?.summary.total_weeks + ' Weeks'} />
                            <DiffRow label="Frequency" prior={priorProgram.result_snapshot.viewModel?.summary.weekly_frequency + 'x'} current={currentVM?.summary.weekly_frequency + 'x'} />
                            <DiffRow label="Goal" prior={priorProgram.goal} current={currentVM?.summary.blueprint_selected || '-'} />
                         </ul>
                      </div>
                      
                      <div>
                         <h4 className="flex items-center text-xs font-bold uppercase tracking-wider text-slate-500 mb-3 border-b border-slate-100 pb-1">
                            <CalendarDays className="w-3 h-3 mr-1.5" /> Weekly Exposures
                         </h4>
                         {currentVM?.weeks.map(week => {
                            const priorWeek = priorProgram.result_snapshot.viewModel?.weeks.find((w: any) => w.week_number === week.week_number);
                            return (
                               <div key={week.week_number} className="mb-4">
                                  <div className="text-xs font-bold text-slate-800 mb-2">{week.label}</div>
                                  <ul className="space-y-2 pl-2">
                                     <DiffRow label="Type" prior={priorWeek?.exposure_summary.week_type || 'None'} current={week.exposure_summary.week_type} />
                                     <DiffRow label="Conditioning" prior={priorWeek?.exposure_summary.conditioning_density || 'None'} current={week.exposure_summary.conditioning_density} />
                                  </ul>
                               </div>
                            );
                         })}
                      </div>
                   </div>

                   {/* Right Col */}
                   <div className="space-y-6 md:pl-8">
                      <div>
                         <h4 className="flex items-center text-xs font-bold uppercase tracking-wider text-slate-500 mb-3 border-b border-slate-100 pb-1">
                            <AlertCircle className="w-3 h-3 mr-1.5" /> Warnings & Diagnostics
                         </h4>
                         
                         <div className="mb-4">
                            <div className="text-[10px] uppercase font-bold text-slate-400 tracking-wider mb-2">Previous</div>
                            <ul className="space-y-1">
                               {priorProgram.result_snapshot.viewModel?.validation.length === 0 ? <li className="text-xs text-emerald-600">Clean</li> : priorProgram.result_snapshot.viewModel?.validation.map((v: any, i: number) => (
                                 <li key={i} className="text-xs text-slate-600 line-clamp-1">{v.message}</li>
                               ))}
                            </ul>
                         </div>
                         <div>
                            <div className="text-[10px] uppercase font-bold text-slate-400 tracking-wider mb-2">Current</div>
                            <ul className="space-y-1">
                               {currentVM?.validation.length === 0 ? <li className="text-xs text-emerald-600">Clean</li> : currentVM?.validation.map((v: any, i: number) => (
                                 <li key={i} className="text-xs text-slate-600 line-clamp-1">{v.message}</li>
                               ))}
                            </ul>
                         </div>
                      </div>
                   </div>

                </div>
             </div>
          </div>
       )}
    </div>
  );
}

function DiffRow({ label, prior, current }: { label: string, prior: string, current: string }) {
  const isChanged = prior !== current;

  return (
     <li className="flex flex-col text-sm">
        <span className="text-[10px] uppercase font-bold text-slate-400 tracking-wider w-full mb-0.5">{label}</span>
        <div className="flex items-center gap-2">
           <span className={`${isChanged ? 'text-slate-500 line-through decoration-slate-300' : 'text-slate-800 font-medium'}`}>{prior}</span>
           {isChanged && (
             <>
               <ArrowRight className="w-3 h-3 text-indigo-400" />
               <span className="font-semibold text-indigo-700 bg-indigo-50 px-1.5 py-0.5 rounded">{current}</span>
             </>
           )}
        </div>
     </li>
  );
}
