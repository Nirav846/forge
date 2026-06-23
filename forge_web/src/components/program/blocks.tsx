import React, { useState } from 'react';
import { Target, Activity, MoreHorizontal, Edit2, Repeat, Lock, LockOpen, MessageSquarePlus } from 'lucide-react';
import { SessionVM, ExerciseVM } from '../../types/ui';

export function SessionCard({ session }: { session: SessionVM }) {
  const [isLocked, setIsLocked] = useState(false);
  const [sessionNote, setSessionNote] = useState<string | null>(null);
  const [isAddingNote, setIsAddingNote] = useState(false);

  return (
    <div className={`bg-white rounded-2xl border ${isLocked ? 'border-amber-300 ring-1 ring-amber-300' : 'border-slate-200'} shadow-sm overflow-hidden flex flex-col h-full bg-white transition-all`}>
       <div className="bg-slate-900 p-4 text-white">
          <div className="flex justify-between items-center mb-2">
             <div className="text-xs font-bold text-slate-400 tracking-wider flex items-center gap-2">
                SESSION {session.session_number}
                {isLocked && <span className="bg-amber-500/20 text-amber-500 px-1.5 py-0.5 rounded text-[10px] uppercase">Locked</span>}
             </div>
             
             <div className="flex items-center gap-3">
                <button 
                  onClick={() => setIsAddingNote(!isAddingNote)} 
                  className="text-slate-500 hover:text-slate-300"
                  title="Add Coach Note"
                >
                   <MessageSquarePlus className="w-3.5 h-3.5" />
                </button>
                <button 
                  onClick={() => setIsLocked(!isLocked)} 
                  className={isLocked ? 'text-amber-500 hover:text-amber-400' : 'text-slate-500 hover:text-slate-300'}
                  title={isLocked ? "Unlock Session" : "Lock Session"}
                >
                   {isLocked ? <Lock className="w-3.5 h-3.5" /> : <LockOpen className="w-3.5 h-3.5" />}
                </button>
                <div className="text-[10px] uppercase font-bold bg-slate-800 border border-slate-700 px-2 py-0.5 rounded text-slate-300">{session.focus}</div>
             </div>
          </div>
          <h4 className="text-lg font-bold flex items-center justify-between">
            {session.name}
          </h4>
       </div>

       <div className="p-0 flex-1 bg-slate-50/50 flex flex-col">
          
          {isAddingNote && (
            <div className="p-3 bg-amber-50 border-b border-amber-100 flex gap-2">
               <input 
                 type="text" 
                 placeholder="Type a note for this session..." 
                 className="flex-1 text-sm px-2 py-1 border border-amber-200 rounded text-slate-800 bg-white"
                 onKeyDown={(e) => {
                   if (e.key === 'Enter') {
                      setSessionNote(e.currentTarget.value);
                      setIsAddingNote(false);
                   }
                 }}
               />
               <button onClick={() => setIsAddingNote(false)} className="text-xs text-slate-500 font-semibold px-2 hover:text-slate-800">Cancel</button>
            </div>
          )}

          {sessionNote && !isAddingNote && (
             <div className="px-4 py-2 bg-amber-50 border-b border-amber-100 text-sm text-amber-900 flex justify-between items-center">
                <span className="flex items-center gap-1.5"><MessageSquarePlus className="w-3 h-3 text-amber-600" /> {sessionNote}</span>
                <button onClick={() => setSessionNote(null)} className="text-[10px] text-amber-600/70 hover:text-amber-600 font-bold uppercase">Clear</button>
             </div>
          )}

          {/* Warmup */}
          {session.warmup && session.warmup.exercises && session.warmup.exercises.length > 0 && (
             <div className="p-4 border-b border-slate-100 bg-white">
                <h5 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3 flex items-center">
                   <Target className="w-3 h-3 mr-1.5" /> {session.warmup.title || 'Warmup Phase'}
                </h5>
                <div className="space-y-2">
                   {session.warmup.exercises.map((ex, idx) => (
                      <ExerciseRow key={ex.id || `w-${idx}`} exercise={ex} isWarmup={true} isSessionLocked={isLocked} />
                   ))}
                </div>
             </div>
          )}

          {/* Main Work */}
          {session.main_work && session.main_work.exercises && session.main_work.exercises.length > 0 ? (
             <div className="p-4 border-b border-slate-100 bg-white">
                <h5 className="text-xs font-bold text-slate-900 uppercase tracking-wider mb-3">
                   {session.main_work.title || 'Main Work'}
                </h5>
                <div className="space-y-4">
                   {session.main_work.exercises.map((ex, idx) => (
                      <ExerciseRow key={ex.id || `m-${idx}`} exercise={ex} isWarmup={false} isSessionLocked={isLocked} />
                   ))}
                </div>
             </div>
          ) : (
            <div className="p-6 text-center text-slate-400 text-sm italic bg-slate-50/50 flex-1">
               No loadable programming vectors supplied for Main Work.
            </div>
          )}

          {/* Conditioning */}
          {session.conditioning && session.conditioning.exercises && session.conditioning.exercises.length > 0 && (
             <div className="p-4 bg-indigo-50/20">
                <h5 className="text-xs font-bold text-indigo-700 uppercase tracking-wider mb-3 flex items-center">
                   <Activity className="w-3 h-3 mr-1.5" /> {session.conditioning.title || 'Conditioning'}
                </h5>
                <div className="space-y-2">
                   {session.conditioning.exercises.map((ex, idx) => (
                      <ExerciseRow key={ex.id || `c-${idx}`} exercise={ex} isWarmup={true} isSessionLocked={isLocked} />
                   ))}
                </div>
             </div>
          )}
       </div>
    </div>
  );
}

export function ExerciseRow({ exercise, isWarmup = false, isSessionLocked = false }: { exercise: ExerciseVM, isWarmup?: boolean, isSessionLocked?: boolean }) {
  const [isSwapped, setIsSwapped] = useState(false);
  const [isEdited, setIsEdited] = useState(false);
  
  if (isWarmup) {
     return (
        <div className="group relative flex bg-white border border-slate-200 rounded-md p-2 shadow-sm text-sm hover:border-slate-300 transition-colors">
           <div className="flex-1 font-medium text-slate-700 pr-8">{exercise.name}</div>
           <div className="w-24 text-right text-slate-500 font-mono text-xs">{exercise.sets_reps}</div>
           <div className="w-16 text-right text-slate-400 text-xs">{exercise.loading_method}</div>
           
           {!isSessionLocked && (
             <div className="absolute top-1/2 -translate-y-1/2 right-2 opacity-0 group-hover:opacity-100 transition-opacity bg-white pl-2">
                <button className="text-slate-400 hover:text-indigo-600 p-1"><MoreHorizontal className="w-4 h-4" /></button>
             </div>
           )}
        </div>
     );
  }

  return (
     <div className={`group relative flex flex-col bg-white border ${isSwapped ? 'border-indigo-300' : isEdited ? 'border-amber-300' : 'border-slate-200'} rounded-xl shadow-sm border-l-4 ${isSwapped ? 'border-l-indigo-500' : isEdited ? 'border-l-amber-500' : 'border-l-slate-400'} overflow-hidden transition-all hover:shadow-md`}>
        <div className="flex flex-wrap items-center p-3 gap-y-2">
           <div className="flex-1 min-w-[150px] pr-4">
              <div className="flex items-center gap-2">
                 <div className="font-bold text-slate-900">{exercise.name}</div>
                 {isSwapped && <span className="bg-indigo-100 text-indigo-700 text-[9px] px-1.5 py-0.5 rounded font-bold uppercase tracking-wider">Swapped</span>}
                 {isEdited && !isSwapped && <span className="bg-amber-100 text-amber-700 text-[9px] px-1.5 py-0.5 rounded font-bold uppercase tracking-wider">Edited</span>}
              </div>
              <div className="text-xs text-slate-400 mt-0.5">{exercise.family}</div>
           </div>
           
           <div className="flex divide-x divide-slate-200 bg-slate-50 rounded border border-slate-200 px-1 py-1 mr-6">
              <div className="px-3">
                 <div className="text-[10px] uppercase text-slate-400 font-bold tracking-wide">Sets/Reps</div>
                 <div className="font-mono text-sm font-semibold text-slate-800">{exercise.sets_reps}</div>
              </div>
              <div className="px-3">
                 <div className="text-[10px] uppercase text-slate-400 font-bold tracking-wide">Load/RPE</div>
                 <div className="font-mono text-sm font-semibold text-indigo-700">{exercise.loading_method}</div>
              </div>
              <div className="px-3">
                 <div className="text-[10px] uppercase text-slate-400 font-bold tracking-wide">Rest</div>
                 <div className="font-mono text-sm font-semibold text-slate-600">{exercise.rest}</div>
              </div>
           </div>
        </div>
        
        {/* Notes sections */}
        {(exercise.coach_note || exercise.progression_note) && (
           <div className="bg-slate-50 px-4 py-2 text-xs border-t border-slate-100 flex flex-col gap-1.5">
              {exercise.coach_note && (
                 <div className="text-slate-600"><span className="font-bold text-slate-500 uppercase tracking-wider text-[10px]">Coach Note:</span> {exercise.coach_note}</div>
              )}
              {exercise.progression_note && (
                 <div className="text-indigo-800"><span className="font-bold text-indigo-400 uppercase tracking-wider text-[10px]">Progression:</span> {exercise.progression_note}</div>
              )}
           </div>
        )}

        {/* Coach Actions Overlay (Hover) */}
        {!isSessionLocked && (
           <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col gap-1 bg-white/90 backdrop-blur pb-1 pl-1 rounded-bl">
              <button 
                onClick={() => setIsSwapped(!isSwapped)} 
                className="p-1.5 text-slate-400 hover:text-indigo-600 hover:bg-slate-100 rounded"
                title="Swap Exercise"
              >
                 <Repeat className="w-3.5 h-3.5" />
              </button>
              <button 
                onClick={() => setIsEdited(!isEdited)} 
                className="p-1.5 text-slate-400 hover:text-amber-600 hover:bg-slate-100 rounded"
                title="Edit Prescription"
              >
                 <Edit2 className="w-3.5 h-3.5" />
              </button>
           </div>
        )}
     </div>
  );
}
