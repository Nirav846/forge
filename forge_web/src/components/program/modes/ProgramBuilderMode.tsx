import React, { useState } from 'react';
import { ProgramViewModel } from '../../../types/ui';
import { SessionCard } from '../blocks';
import { Layers, Activity, CalendarDays, Target, AlertCircle } from 'lucide-react';

export function ProgramBuilderMode({ viewModel }: { viewModel: ProgramViewModel }) {
  const [activeWeekNum, setActiveWeekNum] = useState<number>(viewModel.weeks[0]?.week_number || 1);
  
  const activeWeek = viewModel.weeks.find(w => w.week_number === activeWeekNum);

  return (
    <div className="space-y-6">
       
       <div className="sticky top-0 z-10 bg-slate-50 border border-slate-200 rounded-xl p-3 shadow-sm mb-6 flex space-x-3 overflow-x-auto hide-scrollbar">
          {viewModel.weeks.map(week => {
             const isActive = activeWeekNum === week.week_number;
             const hasWarnings = viewModel.validation.some(v => v.message.includes(`Week ${week.week_number}`));
             
             return (
               <button
                  key={week.week_number}
                  onClick={() => setActiveWeekNum(week.week_number)}
                  className={`flex-shrink-0 w-64 text-left border rounded-lg p-3 transition-all ${
                    isActive 
                      ? 'bg-white border-indigo-400 shadow-md ring-1 ring-indigo-400' 
                      : 'bg-white/60 border-slate-200 hover:bg-white hover:border-slate-300'
                  }`}
               >
                  <div className="flex justify-between items-start mb-2">
                     <span className={`text-sm font-bold ${isActive ? 'text-indigo-800' : 'text-slate-700'}`}>
                        {week.label}
                     </span>
                     <div className="flex gap-1">
                        {week.exposure_summary.testing_markers.length > 0 && <Target className="w-3.5 h-3.5 text-amber-500" />}
                        {hasWarnings && <AlertCircle className="w-3.5 h-3.5 text-red-500" />}
                     </div>
                  </div>
                  
                  <div className="flex items-center gap-2 mb-2">
                     <span className="text-[10px] font-bold uppercase tracking-wider bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded">
                        {week.exposure_summary.week_type.substring(0, 12)}
                     </span>
                     <span className="text-xs font-medium text-slate-500 flex items-center">
                        <CalendarDays className="w-3 h-3 mr-1" /> {week.sessions.length}
                     </span>
                  </div>

                  {/* Exposure Mini Badges */}
                  <div className="flex gap-1.5 mt-2 opacity-80">
                     {week.exposure_summary.sprint_exposure !== 'Not specified' && (
                        <div className="w-2 h-2 rounded-full bg-blue-400" title={`Sprint: ${week.exposure_summary.sprint_exposure}`} />
                     )}
                     {week.exposure_summary.conditioning_density !== 'Not specified' && (
                        <div className="w-2 h-2 rounded-full bg-red-400" title={`Conditioning: ${week.exposure_summary.conditioning_density}`} />
                     )}
                     {week.exposure_summary.deceleration_exposure !== 'Not specified' && (
                        <div className="w-2 h-2 rounded-full bg-amber-400" title={`Deceleration: ${week.exposure_summary.deceleration_exposure}`} />
                     )}
                  </div>
               </button>
             );
          })}
       </div>

       {activeWeek && (
          <div className="animate-in fade-in slide-in-from-bottom-2 duration-300">
             <div className="flex items-center justify-between mb-4 border-b border-slate-200 pb-2">
                <h3 className="text-lg font-bold text-slate-900">{activeWeek.label} Workspace</h3>
             </div>
             
             {/* Sessions Grid */}
             {activeWeek.sessions.length > 0 ? (
                <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 items-start">
                   {activeWeek.sessions.map(session => (
                      <SessionCard key={session.id} session={session} />
                   ))}
                </div>
             ) : (
                <div className="text-center py-12 bg-white rounded-xl border border-dashed border-slate-300 text-slate-400 font-medium">
                   <Layers className="w-8 h-8 mx-auto mb-3 text-slate-300" />
                   No sessions scheduled for this week.
                </div>
             )}
          </div>
       )}
    </div>
  );
}
