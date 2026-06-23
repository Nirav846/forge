import React from 'react';
import { ProgramViewModel } from '../../../types/ui';

export function AthleteDeliveryMode({ viewModel, requestName }: { viewModel: ProgramViewModel, requestName: string }) {

  const handlePrint = () => {
     window.print();
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200" id="athlete-delivery-view">
      <style>{`
        @media print {
          @page { margin: 18mm 15mm; }
          body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
          #athlete-delivery-view .print-page-break { page-break-before: always; }
          #athlete-delivery-view .print-break-inside { page-break-inside: avoid; }
          #athlete-delivery-view .session-exercise-row { page-break-inside: avoid; }
          #athlete-delivery-view .print-text-sm { font-size: 11pt; }
        }
      `}</style>

       {/* Delivery Actions */}
       <div className="px-6 py-4 border-b border-slate-100 flex justify-between items-center bg-slate-50 rounded-t-xl print:hidden">
          <div>
             <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider">Athlete Handout View</h3>
             <p className="text-xs text-slate-500 mt-0.5">Optimized for desktop or PDF reading. Internal metrics are hidden.</p>
          </div>
          <button onClick={handlePrint} className="text-xs font-semibold px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition">
             Print Document
          </button>
       </div>

       {/* Print Document Area */}
       <div className="p-8 md:p-12 print:p-6 max-w-[850px] mx-auto text-slate-900 font-sans bg-white print:bg-white shadow-[0_0_40px_rgba(0,0,0,0.02)] print:shadow-none min-h-[1056px]">

           {/* Document Header */}
           <div className="flex flex-col md:flex-row justify-between items-start md:items-end border-b-4 border-slate-900 pb-6 mb-10 gap-4 print-break-inside">
              <div>
                 <div className="text-[10px] font-black uppercase tracking-[0.2em] text-slate-400 mb-2">Performance Blueprint</div>
                 <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight leading-none text-slate-900 mb-2">{viewModel.summary.blueprint_selected}</h1>
                 <div className="text-sm font-bold text-slate-500 tracking-wider uppercase">Phase Length: {viewModel.summary.total_weeks} Weeks</div>
              </div>
              <div className="text-left md:text-right bg-slate-50 p-4 border border-slate-200 w-full md:w-auto">
                 <div className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Prepared For</div>
                 <div className="text-xl font-bold text-slate-900">{requestName || 'Athlete Name'}</div>
                 <div className="text-sm font-medium text-slate-600 mt-1">{viewModel.summary.role_emphasis}</div>
              </div>
           </div>

           <div className="space-y-16">
              {viewModel.weeks.map((week, wIdx) => (
                 <div key={week.week_number} className={`${wIdx > 0 ? 'print-page-break' : ''}`}>

                    <div className="flex items-center gap-4 mb-6 border-b-2 border-slate-200 pb-2">
                       <h2 className="text-2xl font-black text-slate-900 uppercase tracking-tight">{week.label}</h2>
                       <div className="flex-1"></div>
                       <div className="text-xs font-bold text-slate-500 uppercase tracking-wider">{week.exposure_summary.week_type}</div>
                    </div>

                    <div className="space-y-12">
                       {week.sessions.map(sess => (
                          <div key={sess.id} className="print-break-inside shadow-sm border border-slate-200 rounded overflow-hidden">
                             <div className="bg-slate-900 text-white px-5 py-3 flex justify-between items-center">
                                <h3 className="font-bold uppercase tracking-wider text-sm flex items-center gap-2">
                                  <span className="text-indigo-400">Session {sess.session_number}</span> <span className="opacity-50">/</span> {sess.name}
                                </h3>
                                <span className="text-[10px] font-bold text-slate-900 tracking-widest uppercase bg-white px-2 py-0.5 rounded-sm">{sess.focus}</span>
                             </div>

                             <div className="px-5 py-4 bg-white divide-y divide-slate-100">

                                {sess.warmup.exercises.length > 0 && (
                                   <div className="pt-2 pb-4 session-exercise-row">
                                      <div className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-3 flex justify-between px-2 bg-slate-50 py-1 rounded">
                                         <span>Activation & Prep</span>
                                         <span>Rounds/Reps</span>
                                      </div>
                                      <div className="space-y-2 px-2">
                                         {sess.warmup.exercises.map((ex, eIdx) => (
                                            <div key={eIdx} className="flex justify-between items-start text-sm session-exercise-row">
                                               <span className="font-medium text-slate-700">{ex.name}</span>
                                               <span className="font-mono text-slate-500 text-xs font-semibold">{ex.sets_reps}</span>
                                            </div>
                                         ))}
                                      </div>
                                   </div>
                                )}

                                {sess.main_work.exercises.length > 0 && (
                                   <div className="py-4 session-exercise-row">
                                      <div className="text-[10px] font-black text-slate-900 uppercase tracking-widest mb-3 flex justify-between px-2 bg-slate-100 py-1.5 rounded">
                                         <span className="w-1/2">Main Block</span>
                                         <span className="w-1/4 text-center">Volume</span>
                                         <span className="w-1/4 text-right">Target</span>
                                      </div>
                                      <div className="space-y-4 px-2">
                                         {sess.main_work.exercises.map((ex, eIdx) => (
                                            <div key={eIdx} className="flex items-start text-sm border-b border-slate-50 pb-2 last:border-0 last:pb-0 session-exercise-row">
                                               <div className="w-1/2 font-bold text-slate-900 leading-tight pr-4">
                                                  {ex.name}
                                                  {ex.progression_note && <div className="text-[11px] font-normal text-slate-500 mt-1 whitespace-pre-wrap">{ex.progression_note}</div>}
                                                  {ex.coach_note && <div className="text-[11px] font-bold text-indigo-700 mt-1">Note: {ex.coach_note}</div>}
                                               </div>
                                               <div className="w-1/4 text-center text-slate-800 font-mono font-bold tracking-tight">{ex.sets_reps}</div>
                                               <div className="w-1/4 text-right text-slate-700 font-medium">{ex.loading_method}</div>
                                            </div>
                                         ))}
                                      </div>
                                   </div>
                                )}

                                {sess.conditioning.exercises.length > 0 && (
                                   <div className="pt-4 pb-2 session-exercise-row">
                                      <div className="text-[10px] font-black text-slate-500 uppercase tracking-widest mb-3 flex justify-between px-2 bg-slate-50 py-1 rounded">
                                         <span className="w-1/2">Energy Systems</span>
                                         <span className="w-1/4 text-center">Volume</span>
                                         <span className="w-1/4 text-right">Intensity</span>
                                      </div>
                                      <div className="space-y-3 px-2">
                                         {sess.conditioning.exercises.map((ex, eIdx) => (
                                            <div key={eIdx} className="flex justify-between items-start text-sm session-exercise-row">
                                               <div className="w-1/2 font-medium text-slate-800 pr-4">{ex.name}</div>
                                               <div className="w-1/4 text-center text-slate-600 font-mono md:text-sm text-xs">{ex.sets_reps}</div>
                                               <div className="w-1/4 text-right text-slate-600 text-xs md:text-sm">{ex.loading_method}</div>
                                            </div>
                                         ))}
                                      </div>
                                   </div>
                                )}
                             </div>
                          </div>
                       ))}
                    </div>
                 </div>
              ))}
           </div>

           {/* Footer / Branding */}
           <div className="mt-16 pt-6 border-t-2 border-slate-900 flex justify-between items-center text-xs print-break-inside">
              <div className="font-bold text-slate-900 tracking-widest uppercase">FORGE Athletics</div>
              <div className="text-slate-400">Generated: {new Date(viewModel.metadata.generated_at).toLocaleDateString()}</div>
           </div>
       </div>

    </div>
  );
}
