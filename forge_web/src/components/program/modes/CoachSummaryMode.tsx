import React from 'react';
import { ProgramViewModel } from '../../../types/ui';
import { AlertCircle, Target, Activity, CheckCircle, Flame, ShieldAlert, Cpu } from 'lucide-react';

export function CoachSummaryMode({ viewModel }: { viewModel: ProgramViewModel }) {
  return (
    <div className="space-y-6">
       
       {viewModel.dropped_constraints.length > 0 && (
         <div className="bg-amber-50 border border-amber-200 p-4 rounded-xl flex items-start">
            <AlertCircle className="w-5 h-5 text-amber-500 mt-0.5 mr-3 shrink-0" />
            <div>
               <h4 className="text-sm font-semibold text-amber-800">Dropped Constraints</h4>
               <ul className="text-sm text-amber-700 mt-1 list-disc list-inside">
                  {viewModel.dropped_constraints.map((note, i) => (
                     <li key={i}>{note}</li>
                  ))}
               </ul>
            </div>
         </div>
       )}

       <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          
          <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
             <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-4 flex items-center border-b border-slate-100 pb-2">
               <Cpu className="w-4 h-4 mr-2 text-indigo-500" /> FORGE Rationale
             </h3>
             <ul className="space-y-3">
               {viewModel.rationale.length > 0 ? viewModel.rationale.map((rat, i) => (
                  <li key={i} className="text-sm text-slate-700 flex items-start">
                     <div className="w-1.5 h-1.5 rounded-full bg-indigo-400 mt-2 mr-2 shrink-0"></div>
                     <span>{rat}</span>
                  </li>
               )) : (
                 <li className="text-sm text-slate-500 italic">No rationale provided by backend.</li>
               )}
             </ul>
          </div>

          <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
             <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider mb-4 flex items-center border-b border-slate-100 pb-2">
               <Target className="w-4 h-4 mr-2 text-emerald-500" /> Personalization Vectors
             </h3>
             <ul className="space-y-3">
               {viewModel.personalization_notes.length > 0 ? viewModel.personalization_notes.map((note, i) => (
                  <li key={i} className="text-sm text-slate-700 flex items-start">
                     <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-2 mr-2 shrink-0"></div>
                     <span>{note}</span>
                  </li>
               )) : (
                 <li className="text-sm text-slate-500 italic">Standard block applied.</li>
               )}
             </ul>
          </div>
       </div>

       {/* Weekly Summaries */}
       <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
          <div className="bg-slate-50 px-5 py-3 border-b border-slate-200 flex justify-between items-center">
             <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider">Weekly Exposure Mapping</h3>
          </div>
          <div className="divide-y divide-slate-100">
             {viewModel.weeks.map(week => (
                <div key={week.week_number} className="p-5 flex flex-col md:flex-row gap-6">
                   <div className="w-32 shrink-0">
                      <div className="text-sm font-bold text-slate-900 mb-1">{week.label}</div>
                      <div className="inline-block px-2 py-0.5 bg-slate-100 text-slate-600 text-xs font-semibold rounded">{week.exposure_summary.week_type}</div>
                      
                      {week.exposure_summary.testing_markers.length > 0 && (
                         <div className="mt-3">
                            <div className="text-[10px] uppercase font-bold text-amber-600 tracking-wider mb-1">Testing:</div>
                            {week.exposure_summary.testing_markers.map((t, i) => (
                               <div key={i} className="text-xs text-slate-700 bg-amber-50 px-1 py-0.5 rounded border border-amber-100 mb-1">{t}</div>
                            ))}
                         </div>
                      )}
                   </div>

                   <div className="flex-1 grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div>
                         <div className="text-[10px] uppercase font-bold text-slate-400 tracking-wider mb-1">Sprint Vol</div>
                         <div className="text-sm font-medium text-slate-800">{week.exposure_summary.sprint_exposure}</div>
                      </div>
                      <div>
                         <div className="text-[10px] uppercase font-bold text-slate-400 tracking-wider mb-1">Jump/Land</div>
                         <div className="text-sm font-medium text-slate-800">{week.exposure_summary.jump_landing_exposure}</div>
                      </div>
                      <div>
                         <div className="text-[10px] uppercase font-bold text-slate-400 tracking-wider mb-1">Deceleration</div>
                         <div className="text-sm font-medium text-slate-800">{week.exposure_summary.deceleration_exposure}</div>
                      </div>
                      <div>
                         <div className="text-[10px] uppercase font-bold text-slate-400 tracking-wider mb-1">Cond Density</div>
                         <div className="text-sm font-medium text-slate-800">{week.exposure_summary.conditioning_density}</div>
                      </div>
                   </div>
                </div>
             ))}
          </div>
       </div>

    </div>
  );
}
