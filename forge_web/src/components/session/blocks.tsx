import React, { useState } from 'react';
import { X, ChevronUp, ChevronDown, Plus } from 'lucide-react';
import { ExerciseVM, SessionSectionVM } from '../../types/ui';
import ExerciseLibraryModal from './ExerciseLibraryModal';

interface DocExerciseRowProps {
  ex: ExerciseVM;
  index: number;
  total: number;
  onRemove?: (exerciseId: string) => void;
  onMoveUp?: (exerciseId: string) => void;
  onMoveDown?: (exerciseId: string) => void;
}

export function DocExerciseRow({ ex, index, total, onRemove, onMoveUp, onMoveDown }: DocExerciseRowProps) {
  return (
    <div className="flex items-center border-b border-slate-100 last:border-0 py-2 hover:bg-slate-50 transition-colors -mx-2 px-2 rounded group">
      <div className="flex flex-col items-center gap-0.5 mr-2 opacity-0 group-hover:opacity-100 transition-opacity">
        {onMoveUp && index > 0 && (
          <button onClick={() => onMoveUp(ex.id)} className="text-slate-400 hover:text-slate-700 p-0.5" title="Move up"><ChevronUp className="w-3 h-3" /></button>
        )}
        {onMoveDown && index < total - 1 && (
          <button onClick={() => onMoveDown(ex.id)} className="text-slate-400 hover:text-slate-700 p-0.5" title="Move down"><ChevronDown className="w-3 h-3" /></button>
        )}
      </div>
      <div className="flex-1 grid grid-cols-12 gap-2 items-center">
        <div className="col-span-4">
          <div className="font-medium text-slate-900 text-sm">{ex.name}</div>
          <div className="text-xs text-slate-500">{ex.family}</div>
        </div>
        <div className="col-span-3 text-slate-700 font-mono text-sm">{ex.sets_reps}</div>
        <div className="col-span-2 text-slate-700 text-sm">{ex.loading_method}</div>
        <div className="col-span-2 text-slate-600 text-sm">{ex.rest}</div>
        <div className="col-span-1 flex justify-end gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
          {onRemove && (
            <button onClick={() => onRemove(ex.id)} className="text-red-400 hover:text-red-600 p-0.5" title="Remove exercise">
              <X className="w-3.5 h-3.5" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

interface BlockControls {
  sessionId: string;
  blockType: 'warmup' | 'main_work' | 'conditioning';
  onRemoveExercise?: (sessionId: string, blockType: string, exerciseId: string) => void;
  onMoveExercise?: (sessionId: string, blockType: string, exerciseId: string, direction: 'up' | 'down') => void;
  onAddExercise?: (sessionId: string, blockType: string) => void;
}

function ExerciseSection({ title, section, sessionId, blockType, onRemoveExercise, onMoveExercise, onAddExercise, className = '', accentColor = 'bg-slate-500' }: {
  title: string;
  section: SessionSectionVM;
  sessionId: string;
  blockType: 'warmup' | 'main_work' | 'conditioning';
  onRemoveExercise?: (sessionId: string, blockType: string, exerciseId: string) => void;
  onMoveExercise?: (sessionId: string, blockType: string, exerciseId: string, direction: 'up' | 'down') => void;
  onAddExercise?: (sessionId: string, blockType: string) => void;
  className?: string;
  accentColor?: string;
}) {
  const [showLibrary, setShowLibrary] = useState(false);
  const exercises = section.exercises || [];

  return (
    <div className={`mb-6 ${className}`}>
      <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3 block border-b border-slate-200 pb-2">
        {section.title || title}
      </h4>
      <div className={`bg-white border text-sm border-slate-200 rounded-md p-4 relative overflow-hidden ${className.includes('bg-') ? '' : ''}`}>
        {accentColor && <div className={`absolute top-0 left-0 w-1 h-full ${accentColor === 'bg-indigo-500' ? 'bg-indigo-500' : accentColor === 'bg-emerald-500' ? 'bg-emerald-500' : 'bg-slate-300'}`}></div>}
        {exercises.length > 0 ? (
          <div>
            {exercises.map((ex, i) => (
              <DocExerciseRow key={ex.id || i} ex={ex} index={i} total={exercises.length}
                onRemove={onRemoveExercise ? (id) => onRemoveExercise(sessionId, blockType, id) : undefined}
                onMoveUp={onMoveExercise ? (id) => onMoveExercise(sessionId, blockType, id, 'up') : undefined}
                onMoveDown={onMoveExercise ? (id) => onMoveExercise(sessionId, blockType, id, 'down') : undefined}
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-6 text-slate-400 italic text-sm">No exercises added yet.</div>
        )}
        {onAddExercise && (
          <div className="mt-3 pt-3 border-t border-slate-100">
            <button onClick={() => setShowLibrary(true)} className="flex items-center gap-1.5 text-xs text-indigo-600 hover:text-indigo-800 font-semibold transition-colors">
              <Plus className="w-3 h-3" /> Add Exercise
            </button>
          </div>
        )}
      </div>

      {section.notes && (
        <div className="mt-3 pt-3 border-t border-slate-100 text-slate-600 italic text-sm">
          Coach Note: {section.notes}
        </div>
      )}

      {showLibrary && (
        <ExerciseLibraryModal
          onClose={() => setShowLibrary(false)}
          onSelect={(exercise) => {
            onAddExercise?.(sessionId, blockType);
            setShowLibrary(false);
          }}
        />
      )}
    </div>
  );
}

export function WarmupBlock({ section, sessionId, onRemoveExercise, onMoveExercise, onAddExercise }: { section: SessionSectionVM } & BlockControls) {
  if (!section.exercises || section.exercises.length === 0) return null;
  return (
    <ExerciseSection title="Warmup" section={section} sessionId={sessionId} blockType="warmup"
      onRemoveExercise={onRemoveExercise} onMoveExercise={onMoveExercise} onAddExercise={onAddExercise} />
  );
}

export function MainWorkBlock({ section, sessionId, onRemoveExercise, onMoveExercise, onAddExercise }: { section: SessionSectionVM } & BlockControls) {
  if (!section.exercises || section.exercises.length === 0) return null;
  return (
    <ExerciseSection title="Main Work" section={section} sessionId={sessionId} blockType="main_work"
      onRemoveExercise={onRemoveExercise} onMoveExercise={onMoveExercise} onAddExercise={onAddExercise}
      className="border-indigo-100" accentColor="bg-indigo-500" />
  );
}

export function ConditioningBlock({ section, sessionId, onRemoveExercise, onMoveExercise, onAddExercise }: { section: SessionSectionVM } & BlockControls) {
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
             {section.exercises.map((ex, i) => (
               <DocExerciseRow key={ex.id || i} ex={ex} index={i} total={section.exercises.length}
                 onRemove={onRemoveExercise ? (id) => onRemoveExercise(sessionId, 'conditioning', id) : undefined}
                 onMoveUp={onMoveExercise ? (id) => onMoveExercise(sessionId, 'conditioning', id, 'up') : undefined}
                 onMoveDown={onMoveExercise ? (id) => onMoveExercise(sessionId, 'conditioning', id, 'down') : undefined}
               />
             ))}
          </div>
        )}
        {section.notes && (
          <div className="text-emerald-800 italic mb-3">
            {section.notes}
          </div>
        )}
        {onAddExercise && (
          <div className="pt-3 border-t border-emerald-200">
            <LibraryAddButton sessionId={sessionId} blockType="conditioning" onAddExercise={onAddExercise} />
          </div>
        )}
      </div>
    </div>
  );
}

function LibraryAddButton({ sessionId, blockType, onAddExercise }: { sessionId: string; blockType: string; onAddExercise: (sessionId: string, blockType: string) => void }) {
  const [open, setOpen] = useState(false);
  return (
    <>
      <button onClick={() => setOpen(true)} className="flex items-center gap-1.5 text-xs text-emerald-700 hover:text-emerald-900 font-semibold transition-colors">
        <Plus className="w-3 h-3" /> Add Exercise
      </button>
      {open && (
        <ExerciseLibraryModal
          onClose={() => setOpen(false)}
          onSelect={() => { onAddExercise(sessionId, blockType); setOpen(false); }}
        />
      )}
    </>
  );
}
