import { ExerciseVM, SessionSectionVM } from '../../types/ui';

export function ExerciseRow({ ex }: { ex: ExerciseVM }) {
  return (
    <div className="flex border-b border-slate-100 last:border-0 py-2 hover:bg-slate-50 transition-colors -mx-2 px-2 rounded">
      <div className="w-1/4 pr-4">
        <div className="font-medium text-slate-900">{ex.name}</div>
        <div className="text-xs text-slate-500">{ex.family}</div>
      </div>
      <div className="w-1/5 pr-4 text-slate-700 font-mono text-sm">{ex.sets_reps}</div>
      <div className="w-1/5 pr-4 text-slate-700 text-sm">{ex.loading_method}</div>
      <div className="w-1/5 pr-4 text-slate-600 text-sm">{ex.rest}</div>
      <div className="w-[15%] text-slate-500 text-xs italic border-l border-slate-200 pl-4">{ex.coach_note || '-'}</div>
    </div>
  );
}

export function WarmupBlock({ section }: { section: SessionSectionVM }) {
  if (!section.exercises || section.exercises.length === 0) return null;
  return (
    <div className="mb-6">
      <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3 block border-b border-slate-200 pb-2">
        {section.title || 'Warmup'}
      </h4>
      <div className="bg-white border text-sm border-slate-200 rounded-md p-4">
        {section.exercises.map((ex, i) => <ExerciseRow key={ex.id || i} ex={ex} />)}
        {section.notes && (
          <div className="mt-3 pt-3 border-t border-slate-100 text-slate-600 italic">
            Coach Note: {section.notes}
          </div>
        )}
      </div>
    </div>
  );
}

export function MainWorkBlock({ section }: { section: SessionSectionVM }) {
  if (!section.exercises || section.exercises.length === 0) return null;
  return (
    <div className="mb-6">
      <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3 block border-b border-slate-200 pb-2">
        {section.title || 'Main Work'}
      </h4>
      <div className="bg-white border text-sm border-indigo-100 rounded-md p-4 shadow-sm relative overflow-hidden">
        <div className="absolute top-0 left-0 w-1 h-full bg-indigo-500"></div>
        {section.exercises.map((ex, i) => <ExerciseRow key={ex.id || i} ex={ex} />)}
      </div>
    </div>
  );
}

export function ConditioningBlock({ section }: { section: SessionSectionVM }) {
  if (!section.exercises || section.exercises.length === 0 && !section.notes) return null;
  return (
    <div className="mb-6">
      <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3 block border-b border-slate-200 pb-2">
        {section.title || 'Conditioning / Energy Systems'}
      </h4>
      <div className="bg-emerald-50 border border-emerald-100 rounded-md p-4 text-sm relative overflow-hidden">
         <div className="absolute top-0 left-0 w-1 h-full bg-emerald-500"></div>
        {section.exercises.length > 0 && (
          <div className="mb-3">
             {section.exercises.map((ex, i) => <ExerciseRow key={ex.id || i} ex={ex} />)}
          </div>
        )}
        {section.notes && (
          <div className="text-emerald-800 italic">
            {section.notes}
          </div>
        )}
      </div>
    </div>
  );
}
