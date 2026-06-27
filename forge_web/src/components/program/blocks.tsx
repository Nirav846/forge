import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Target, Activity, MoreHorizontal, Edit2, Repeat, Lock, LockOpen, MessageSquarePlus, Check, X, GripVertical, Copy, Trash2, ArrowUpDown, Plus, ChevronUp, ChevronDown } from 'lucide-react';
import { SessionVM, ExerciseVM, SessionOverride, ExerciseSwap, PrescriptionEdit } from '../../types/ui';
import ExerciseLibraryModal from '../session/ExerciseLibraryModal';

const DAY_OPTIONS = [1, 2, 3, 4, 5, 6, 7] as const;

interface SessionCardProps {
  session: SessionVM;
  sessionOverride?: SessionOverride;
  onToggleLock: (sessionId: string, locked: boolean) => void;
  onAddNote: (sessionId: string, note: string) => void;
  onClearNote: (sessionId: string) => void;
  onSwapExercise: (sessionId: string, exerciseId: string, swap: ExerciseSwap) => void;
  onEditPrescription: (sessionId: string, exerciseId: string, edit: PrescriptionEdit) => void;
  onDuplicateSession?: (sessionId: string) => void;
  onDeleteSession?: (sessionId: string) => void;
  onMoveSession?: (sessionId: string, newSessionNumber: number) => void;
  onReorderSession?: (sessionId: string, direction: 'up' | 'down') => void;
  onRemoveExercise?: (sessionId: string, blockType: string, exerciseId: string) => void;
  onMoveExercise?: (sessionId: string, blockType: string, exerciseId: string, direction: 'up' | 'down') => void;
  onAddExercise?: (sessionId: string, blockType: string, exercise: { name: string; family: string }) => void;
}

function computeIntent(session: SessionVM) {
  const allExes = [
    ...(session.warmup?.exercises || []),
    ...(session.main_work?.exercises || []),
    ...(session.conditioning?.exercises || []),
  ];
  const families = [...new Set(allExes.map(e => e.family))];
  return {
    goal: session.focus || 'General',
    fatigue_cost: allExes.filter(e => ['Squat', 'Hinge', 'Deadlift', 'Power', 'Plyo'].includes(e.family)).length > 2 ? 'High' : allExes.length > 6 ? 'Moderate' : 'Low',
    exposures: families.slice(0, 4).join(', '),
  };
}

export function SessionCard({ session, sessionOverride, onToggleLock, onAddNote, onClearNote, onSwapExercise, onEditPrescription, onDuplicateSession, onDeleteSession, onMoveSession, onReorderSession, onRemoveExercise, onMoveExercise, onAddExercise }: SessionCardProps) {
  const isLocked = sessionOverride?.locked ?? false;
  const sessionNote = sessionOverride?.note ?? null;
  const [isAddingNote, setIsAddingNote] = useState(false);
  const [noteInput, setNoteInput] = useState('');
  const [menuOpen, setMenuOpen] = useState(false);
  const [moveOpen, setMoveOpen] = useState(false);
  const [showIntent, setShowIntent] = useState(false);
  const [addExerciseBlock, setAddExerciseBlock] = useState<string | null>(null);
  const menuRef = useRef<HTMLDivElement>(null);
  const intent = computeIntent(session);

  useEffect(() => {
    if (!menuOpen) { setMoveOpen(false); return; }
    const handler = (e: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setMenuOpen(false);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, [menuOpen]);

  // ── Exercise drag-and-drop ──
  const dragExRef = useRef<{ id: string; blockType: string } | null>(null);

  const getBlock = useCallback((bt: string) =>
    bt === 'warmup' ? session.warmup
    : bt === 'main_work' ? session.main_work
    : session.conditioning, [session]);

  const handleExDragStart = useCallback((e: React.DragEvent, exerciseId: string, blockType: string) => {
    if (isLocked) { e.preventDefault(); return; }
    dragExRef.current = { id: exerciseId, blockType };
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', exerciseId);
  }, [isLocked]);

  const handleExDrop = useCallback((e: React.DragEvent, targetBlockType: string, targetIndex: number) => {
    e.preventDefault();
    const src = dragExRef.current;
    if (!src) return;
    const srcBlock = getBlock(src.blockType);
    const srcExercise = srcBlock?.exercises.find(ex => ex.id === src.id);
    if (src.blockType !== targetBlockType && onRemoveExercise && onAddExercise && srcExercise) {
      onRemoveExercise(session.id, src.blockType, src.id);
      onAddExercise(session.id, targetBlockType, { name: srcExercise.name, family: srcExercise.family });
    }
    dragExRef.current = null;
  }, [session.id, getBlock, onRemoveExercise, onAddExercise]);

  const handleExDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  }, []);

  return (
    <div className={`bg-white rounded-2xl border ${isLocked ? 'border-amber-300 ring-1 ring-amber-300' : 'border-slate-200'} shadow-sm overflow-hidden flex flex-col h-full transition-all`}>
      <div className="bg-slate-900 p-4 text-white">
        <div className="flex justify-between items-center mb-2">
          <div className="flex items-center gap-2">
            {onReorderSession && (
              <div className="flex flex-col gap-0.5 mr-1">
                <button onClick={() => onReorderSession(session.id, 'up')} className="text-slate-500 hover:text-white transition-colors leading-none p-0.1"><GripVertical className="w-3 h-3" /></button>
              </div>
            )}
            <div className="text-xs font-bold text-slate-400 tracking-wider flex items-center gap-2">
              SESSION {session.session_number}
              {isLocked && <span className="bg-amber-500/20 text-amber-500 px-1.5 py-0.5 rounded text-[10px] uppercase">Locked</span>}
            </div>
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
              onClick={() => onToggleLock(session.id, !isLocked)}
              className={isLocked ? 'text-amber-500 hover:text-amber-400' : 'text-slate-500 hover:text-slate-300'}
              title={isLocked ? "Unlock Session" : "Lock Session"}
            >
              {isLocked ? <Lock className="w-3.5 h-3.5" /> : <LockOpen className="w-3.5 h-3.5" />}
            </button>
            <div className="relative" ref={menuRef}>
              <button onClick={() => setMenuOpen(!menuOpen)} className="text-slate-500 hover:text-slate-300 p-0.5" title="Session Actions">
                <MoreHorizontal className="w-4 h-4" />
              </button>
              {menuOpen && (
                <div className="absolute right-0 top-6 w-48 bg-white rounded-xl border border-slate-200 shadow-xl z-50 py-1 text-sm text-slate-700">
                  {onDuplicateSession && (
                    <button onClick={() => { onDuplicateSession(session.id); setMenuOpen(false); }} className="w-full flex items-center gap-2 px-4 py-2 hover:bg-slate-50 text-left">
                      <Copy className="w-3.5 h-3.5 text-slate-400" /> Duplicate Session
                    </button>
                  )}
                  {onDeleteSession && (
                    <button onClick={() => { onDeleteSession(session.id); setMenuOpen(false); }} className="w-full flex items-center gap-2 px-4 py-2 hover:bg-red-50 text-red-600 text-left">
                      <Trash2 className="w-3.5 h-3.5" /> Delete Session
                    </button>
                  )}
                  {onMoveSession && (
                    <div>
                      <button onClick={() => setMoveOpen(!moveOpen)} className="w-full flex items-center justify-between gap-2 px-4 py-2 hover:bg-slate-50 text-left">
                        <span className="flex items-center gap-2"><ArrowUpDown className="w-3.5 h-3.5 text-slate-400" /> Move to Day</span>
                        <span className="text-slate-300">{moveOpen ? '▾' : '▸'}</span>
                      </button>
                      {moveOpen && (
                        <div className="pl-8 pb-1">
                          {DAY_OPTIONS.map(d => (
                            <button key={d} onClick={() => { onMoveSession(session.id, d); setMenuOpen(false); }} className={`w-full text-left px-2 py-1 text-xs hover:bg-slate-50 rounded ${d === session.session_number ? 'text-indigo-600 font-bold' : 'text-slate-600'}`}>
                              Session {d}
                            </button>
                          ))}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
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
              value={noteInput}
              onChange={e => setNoteInput(e.target.value)}
              placeholder="Type a note for this session..."
              className="flex-1 text-sm px-2 py-1 border border-amber-200 rounded text-slate-800 bg-white"
              onKeyDown={(e) => {
                if (e.key === 'Enter' && noteInput.trim()) {
                  onAddNote(session.id, noteInput.trim());
                  setNoteInput('');
                  setIsAddingNote(false);
                }
              }}
            />
            <button
              onClick={() => {
                if (noteInput.trim()) {
                  onAddNote(session.id, noteInput.trim());
                  setNoteInput('');
                }
                setIsAddingNote(false);
              }}
              className="text-xs text-indigo-600 font-semibold px-2 hover:text-indigo-800"
            >Save</button>
            <button onClick={() => { setIsAddingNote(false); setNoteInput(''); }} className="text-xs text-slate-500 font-semibold px-2 hover:text-slate-800">Cancel</button>
          </div>
        )}

        {sessionNote && !isAddingNote && (
          <div className="px-4 py-2 bg-amber-50 border-b border-amber-100 text-sm text-amber-900 flex justify-between items-center">
            <span className="flex items-center gap-1.5"><MessageSquarePlus className="w-3 h-3 text-amber-600" /> {sessionNote}</span>
            <button onClick={() => onClearNote(session.id)} className="text-[10px] text-amber-600/70 hover:text-amber-600 font-bold uppercase">Clear</button>
          </div>
        )}

        {/* Intent / rationale expandable */}
        <button onClick={() => setShowIntent(!showIntent)} className="w-full px-4 py-2 flex items-center justify-between text-xs font-semibold text-slate-500 hover:text-indigo-700 hover:bg-indigo-50/50 transition-colors border-b border-slate-100">
          <span>Session Intent & Rationale</span>
          <span className="text-slate-300">{showIntent ? '▾' : '▸'}</span>
        </button>
        {showIntent && (
          <div className="px-4 py-3 bg-indigo-50/40 border-b border-indigo-100 grid grid-cols-3 gap-4 text-xs">
            <div>
              <div className="font-bold text-indigo-700 uppercase tracking-wider text-[10px] mb-1">Goal</div>
              <div className="text-slate-700 font-medium">{intent.goal}</div>
            </div>
            <div>
              <div className="font-bold text-amber-700 uppercase tracking-wider text-[10px] mb-1">Fatigue Cost</div>
              <div className="text-slate-700 font-medium">{intent.fatigue_cost}</div>
            </div>
            <div>
              <div className="font-bold text-emerald-700 uppercase tracking-wider text-[10px] mb-1">Exposures</div>
              <div className="text-slate-700 font-medium">{intent.exposures}</div>
            </div>
          </div>
        )}

        {renderBlock(session, 'warmup', sessionOverride, isLocked, onRemoveExercise, onMoveExercise, onAddExercise, onSwapExercise, onEditPrescription, handleExDragStart, handleExDrop, handleExDragOver, (bt) => setAddExerciseBlock(bt))}

        {renderBlock(session, 'main_work', sessionOverride, isLocked, onRemoveExercise, onMoveExercise, onAddExercise, onSwapExercise, onEditPrescription, handleExDragStart, handleExDrop, handleExDragOver, (bt) => setAddExerciseBlock(bt))}

        {renderBlock(session, 'conditioning', sessionOverride, isLocked, onRemoveExercise, onMoveExercise, onAddExercise, onSwapExercise, onEditPrescription, handleExDragStart, handleExDrop, handleExDragOver, (bt) => setAddExerciseBlock(bt))}

      </div>

      {addExerciseBlock && (
        <ExerciseLibraryModal
          onClose={() => setAddExerciseBlock(null)}
          onSelect={(exercise) => {
            onAddExercise?.(session.id, addExerciseBlock, exercise);
            setAddExerciseBlock(null);
          }}
        />
      )}
    </div>
  );
}

// ── Block renderer (warmup / main_work / conditioning) ──
function renderBlock(
  session: SessionVM,
  blockType: 'warmup' | 'main_work' | 'conditioning',
  sessionOverride: SessionOverride | undefined,
  isLocked: boolean,
  onRemoveExercise: ((sessionId: string, blockType: string, exerciseId: string) => void) | undefined,
  onMoveExercise: ((sessionId: string, blockType: string, exerciseId: string, direction: 'up' | 'down') => void) | undefined,
  onAddExercise: ((sessionId: string, blockType: string, exercise: { name: string; family: string }) => void) | undefined,
  onSwapExercise: ((sessionId: string, exerciseId: string, swap: ExerciseSwap) => void) | undefined,
  onEditPrescription: ((sessionId: string, exerciseId: string, edit: PrescriptionEdit) => void) | undefined,
  onDragStart: (e: React.DragEvent, exerciseId: string, blockType: string) => void,
  onDrop: (e: React.DragEvent, targetBlockType: string, targetIndex: number) => void,
  onDragOver: (e: React.DragEvent) => void,
  onOpenLibrary: (blockType: string) => void,
) {
  const section = blockType === 'warmup' ? session.warmup
    : blockType === 'main_work' ? session.main_work
    : session.conditioning;

  if (!section || !section.exercises || section.exercises.length === 0) {
    if (blockType === 'main_work') {
      return (
        <div className="p-6 text-center text-slate-400 text-sm italic bg-slate-50/50 flex-1">
          No loadable programming vectors supplied for Main Work.
        </div>
      );
    }
    return null;
  }

  const blockTitle = blockType === 'warmup' ? (section.title || 'Warmup Phase')
    : blockType === 'main_work' ? (section.title || 'Main Work')
    : (section.title || 'Conditioning');

  const isMainWork = blockType === 'main_work';

  return (
    <div className={`p-4 border-b border-slate-100 bg-white ${blockType === 'conditioning' ? 'bg-indigo-50/20' : ''}`}
      onDragOver={onDragOver}
      onDrop={(e) => onDrop(e, blockType, section.exercises.length)}
    >
      <h5 className={`text-xs font-bold uppercase tracking-wider mb-3 flex items-center ${isMainWork ? 'text-slate-900' : 'text-slate-500'}`}>
        {blockType === 'warmup' && <Target className="w-3 h-3 mr-1.5" />}
        {blockType === 'conditioning' && <Activity className="w-3 h-3 mr-1.5" />}
        {blockTitle}
      </h5>
      <div className="space-y-2">
        {section.exercises.map((ex, idx) => {
          const exOverride = sessionOverride?.exercises?.[ex.id];
          const swap = exOverride?.swap;
          const edit = exOverride?.prescription;
          return (
            <ExerciseRow
              key={ex.id || `${blockType}-${idx}`}
              exercise={ex}
              isWarmup={blockType !== 'main_work'}
              isMainWork={isMainWork}
              isSessionLocked={isLocked}
              index={idx}
              total={section.exercises.length}
              swapOverride={swap}
              prescriptionOverride={edit}
              onSwap={onSwapExercise ? (swapData) => onSwapExercise(session.id, ex.id, swapData) : undefined}
              onEditPrescription={onEditPrescription ? (editData) => onEditPrescription(session.id, ex.id, editData) : undefined}
              onRemove={onRemoveExercise ? (id) => onRemoveExercise(session.id, blockType, id) : undefined}
              onMoveUp={onMoveExercise ? (id) => onMoveExercise(session.id, blockType, id, 'up') : undefined}
              onMoveDown={onMoveExercise ? (id) => onMoveExercise(session.id, blockType, id, 'down') : undefined}
              onDragStart={(e) => onDragStart(e, ex.id, blockType)}
              onDrop={(e) => onDrop(e, blockType, idx)}
              onDragOver={onDragOver}
            />
          );
        })}
      </div>
      {!isLocked && onAddExercise && (
        <button onClick={() => onOpenLibrary(blockType)} className="mt-2 flex items-center gap-1 text-xs text-indigo-600 hover:text-indigo-800 font-semibold">
          <Plus className="w-3 h-3" /> Add Exercise
        </button>
      )}
    </div>
  );
}

// ── ExerciseRow ──
interface ExerciseRowProps {
  exercise: ExerciseVM;
  isWarmup?: boolean;
  isMainWork?: boolean;
  isSessionLocked?: boolean;
  swapOverride?: ExerciseSwap;
  prescriptionOverride?: PrescriptionEdit;
  onSwap?: (swap: ExerciseSwap) => void;
  onEditPrescription?: (edit: PrescriptionEdit) => void;
  onRemove?: (exerciseId: string) => void;
  onMoveUp?: (exerciseId: string) => void;
  onMoveDown?: (exerciseId: string) => void;
  index?: number;
  total?: number;
  onDragStart?: (e: React.DragEvent) => void;
  onDrop?: (e: React.DragEvent) => void;
  onDragOver?: (e: React.DragEvent) => void;
}

const PRESCRIPTION_PRESETS: Record<string, { label: string; sets_reps: string; loading_method: string; rest: string }[]> = {
  Strength: [
    { label: 'Strength 1', sets_reps: '3x5', loading_method: '85%', rest: '180s' },
    { label: 'Strength 2', sets_reps: '4x6', loading_method: '80%', rest: '150s' },
    { label: 'Strength 3', sets_reps: '5x5', loading_method: '82%', rest: '180s' },
  ],
  Hypertrophy: [
    { label: 'Hypertrophy 1', sets_reps: '3x8', loading_method: '75%', rest: '90s' },
    { label: 'Hypertrophy 2', sets_reps: '3x10', loading_method: '70%', rest: '60s' },
    { label: 'Hypertrophy 3', sets_reps: '4x8', loading_method: '72%', rest: '75s' },
  ],
  Power: [
    { label: 'Power 1', sets_reps: '3x3', loading_method: 'RPE 8', rest: '120s' },
    { label: 'Power 2', sets_reps: '4x4', loading_method: 'RPE 7', rest: '120s' },
  ],
  Endurance: [
    { label: 'Endurance 1', sets_reps: '3x12', loading_method: '60%', rest: '45s' },
    { label: 'Endurance 2', sets_reps: '2x15', loading_method: '55%', rest: '30s' },
  ],
};

export function ExerciseRow({
  exercise, isWarmup = false, isMainWork = true, isSessionLocked = false,
  swapOverride, prescriptionOverride, onSwap, onEditPrescription,
  onRemove, onMoveUp, onMoveDown, index = 0, total = 0,
  onDragStart, onDrop, onDragOver
}: ExerciseRowProps) {
  const [showSwapInput, setShowSwapInput] = useState(false);
  const [showEditInput, setShowEditInput] = useState(false);
  const [swapName, setSwapName] = useState('');
  const [editSetsReps, setEditSetsReps] = useState(exercise.sets_reps);
  const [editLoad, setEditLoad] = useState(exercise.loading_method);
  const [editRest, setEditRest] = useState(exercise.rest);

  const isSwapped = !!swapOverride;
  const isEdited = !!prescriptionOverride;

  // Reset edit fields when exercise changes
  useEffect(() => {
    setEditSetsReps(prescriptionOverride?.sets_reps || exercise.sets_reps);
    setEditLoad(prescriptionOverride?.loading_method || exercise.loading_method);
    setEditRest(prescriptionOverride?.rest || exercise.rest);
  }, [exercise.id, exercise.sets_reps, exercise.loading_method, exercise.rest, prescriptionOverride]);

  if (isWarmup) {
    return (
      <div
        className="group relative flex items-center bg-white border border-slate-200 rounded-md p-2 shadow-sm text-sm hover:border-slate-300 transition-colors"
        draggable={!isSessionLocked}
        onDragStart={onDragStart}
        onDragOver={onDragOver}
        onDrop={onDrop}
      >
        {!isSessionLocked && (
          <div className="flex items-center gap-0.5 mr-1 cursor-grab active:cursor-grabbing" title="Drag to reorder">
            <GripVertical className="w-3 h-3 text-slate-300" />
          </div>
        )}
        <div className="flex items-center gap-0.5 mr-1 opacity-0 group-hover:opacity-100 transition-opacity shrink-0">
          {onMoveUp && index > 0 && <button onClick={() => onMoveUp(exercise.id)} className="text-slate-400 hover:text-slate-700 p-0.5" title="Move up"><ChevronUp className="w-3 h-3" /></button>}
          {onMoveDown && index < total - 1 && <button onClick={() => onMoveDown(exercise.id)} className="text-slate-400 hover:text-slate-700 p-0.5" title="Move down"><ChevronDown className="w-3 h-3" /></button>}
        </div>
        <div className="flex-1 font-medium text-slate-700 pr-8">{exercise.name}</div>
        <div className="w-24 text-right text-slate-500 font-mono text-xs">{exercise.sets_reps}</div>
        <div className="w-16 text-right text-slate-400 text-xs">{exercise.loading_method}</div>
        {onRemove && !isSessionLocked && (
          <button onClick={() => onRemove(exercise.id)} className="ml-1 text-red-300 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity p-0.5" title="Remove exercise">
            <X className="w-3.5 h-3.5" />
          </button>
        )}
      </div>
    );
  }

  const displayName = swapOverride ? swapOverride.new_name : exercise.name;
  const displayFamily = swapOverride ? swapOverride.new_family : exercise.family;
  const displaySetsReps = prescriptionOverride?.sets_reps || exercise.sets_reps;
  const displayLoad = prescriptionOverride?.loading_method || exercise.loading_method;
  const displayRest = prescriptionOverride?.rest || exercise.rest;

  return (
    <div
      className={`group relative flex flex-col bg-white border ${isSwapped ? 'border-indigo-300' : isEdited ? 'border-amber-300' : 'border-slate-200'} rounded-xl shadow-sm border-l-4 ${isSwapped ? 'border-l-indigo-500' : isEdited ? 'border-l-amber-500' : 'border-l-slate-400'} overflow-hidden transition-all hover:shadow-md`}
      draggable={!isSessionLocked}
      onDragStart={onDragStart}
      onDragOver={onDragOver}
      onDrop={onDrop}
    >
      <div className="flex flex-wrap items-center p-3 gap-y-2">
        {!isSessionLocked && (
          <div className="cursor-grab active:cursor-grabbing mr-2 text-slate-300 hover:text-slate-500" title="Drag to reorder">
            <GripVertical className="w-3.5 h-3.5" />
          </div>
        )}
        <div className="flex-1 min-w-[150px] pr-4">
          <div className="flex items-center gap-2">
            <div className="font-bold text-slate-900">{displayName}</div>
            {isSwapped && <span className="bg-indigo-100 text-indigo-700 text-[9px] px-1.5 py-0.5 rounded font-bold uppercase tracking-wider">Swapped</span>}
            {isEdited && !isSwapped && <span className="bg-amber-100 text-amber-700 text-[9px] px-1.5 py-0.5 rounded font-bold uppercase tracking-wider">Edited</span>}
          </div>
          <div className="text-xs text-slate-400 mt-0.5">{displayFamily}</div>
        </div>

        {/* Clickable prescription display — opens inline popover */}
        <div
          className={`flex divide-x divide-slate-200 bg-slate-50 rounded border ${isEdited ? 'border-amber-200' : 'border-slate-200'} px-1 py-1 mr-6 cursor-pointer hover:bg-amber-50/50 transition-colors ${!isSessionLocked ? 'cursor-pointer' : ''}`}
          onClick={() => { if (!isSessionLocked) setShowEditInput(!showEditInput); }}
          title="Click to edit prescription"
        >
          <div className="px-3">
            <div className="text-[10px] uppercase text-slate-400 font-bold tracking-wide">Sets/Reps</div>
            <div className="font-mono text-sm font-semibold text-slate-800">{displaySetsReps}</div>
          </div>
          <div className="px-3">
            <div className="text-[10px] uppercase text-slate-400 font-bold tracking-wide">Load/RPE</div>
            <div className="font-mono text-sm font-semibold text-indigo-700">{displayLoad}</div>
          </div>
          <div className="px-3">
            <div className="text-[10px] uppercase text-slate-400 font-bold tracking-wide">Rest</div>
            <div className="font-mono text-sm font-semibold text-slate-600">{displayRest}</div>
          </div>
        </div>
      </div>

      {(!isSwapped && !isEdited) && (exercise.coach_note || exercise.progression_note) && (
        <div className="bg-slate-50 px-4 py-2 text-xs border-t border-slate-100 flex flex-col gap-1.5">
          {exercise.coach_note && (
            <div className="text-slate-600"><span className="font-bold text-slate-500 uppercase tracking-wider text-[10px]">Coach Note:</span> {exercise.coach_note}</div>
          )}
          {exercise.progression_note && (
            <div className="text-indigo-800"><span className="font-bold text-indigo-400 uppercase tracking-wider text-[10px]">Progression:</span> {exercise.progression_note}</div>
          )}
        </div>
      )}

      {/* Swap Input Panel */}
      {showSwapInput && (
        <div className="p-3 bg-indigo-50 border-t border-indigo-100 space-y-2">
          <div className="text-xs font-bold text-indigo-800 uppercase tracking-wider">Swap Exercise</div>
          <div className="flex gap-2">
            <input
              type="text"
              value={swapName}
              onChange={e => setSwapName(e.target.value)}
              placeholder="Enter new exercise name..."
              className="flex-1 text-sm px-2 py-1.5 border border-indigo-200 rounded bg-white"
              onKeyDown={(e) => {
                if (e.key === 'Enter' && swapName.trim() && onSwap) {
                  onSwap({ original_name: exercise.name, original_family: exercise.family, new_name: swapName.trim(), new_family: exercise.family });
                  setSwapName('');
                  setShowSwapInput(false);
                }
              }}
            />
            <button onClick={() => { if (swapName.trim() && onSwap) { onSwap({ original_name: exercise.name, original_family: exercise.family, new_name: swapName.trim(), new_family: exercise.family }); setSwapName(''); } setShowSwapInput(false); }} className="text-xs bg-indigo-600 text-white px-2 py-1 rounded font-bold"><Check className="w-3 h-3" /></button>
            <button onClick={() => setShowSwapInput(false)} className="text-xs text-slate-500 px-2 py-1 font-bold"><X className="w-3 h-3" /></button>
          </div>
        </div>
      )}

      {/* Edit Prescription Popover (inline, with presets) */}
      {showEditInput && (
        <div className="p-3 bg-amber-50 border-t border-amber-100 space-y-3">
          <div className="flex items-center justify-between">
            <div className="text-xs font-bold text-amber-800 uppercase tracking-wider">Edit Prescription</div>
            <button onClick={() => setShowEditInput(false)} className="text-slate-400 hover:text-slate-600"><X className="w-3 h-3" /></button>
          </div>

          {/* Prescription presets */}
          <div className="space-y-1.5">
            <div className="text-[10px] font-bold text-amber-700 uppercase tracking-wider">Presets</div>
            <div className="flex flex-wrap gap-1">
              {Object.entries(PRESCRIPTION_PRESETS).map(([category, presets]) => (
                <div key={category} className="flex items-center gap-1 bg-white rounded border border-amber-200 px-1.5 py-0.5">
                  <span className="text-[9px] font-bold text-amber-600 mr-0.5">{category}:</span>
                  {presets.map(p => (
                    <button
                      key={p.label}
                      onClick={() => { setEditSetsReps(p.sets_reps); setEditLoad(p.loading_method); setEditRest(p.rest); }}
                      className="text-[10px] px-1.5 py-0.5 rounded bg-amber-100 text-amber-800 hover:bg-amber-200 font-medium transition-colors"
                      title={p.label}
                    >
                      {p.sets_reps}
                    </button>
                  ))}
                </div>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-3 gap-2">
            <div>
              <label className="text-[10px] text-amber-700 block mb-0.5">Sets/Reps</label>
              <input type="text" value={editSetsReps} onChange={e => setEditSetsReps(e.target.value)} className="w-full text-sm px-2 py-1 border border-amber-200 rounded bg-white" />
            </div>
            <div>
              <label className="text-[10px] text-amber-700 block mb-0.5">Load/RPE</label>
              <input type="text" value={editLoad} onChange={e => setEditLoad(e.target.value)} className="w-full text-sm px-2 py-1 border border-amber-200 rounded bg-white" />
            </div>
            <div>
              <label className="text-[10px] text-amber-700 block mb-0.5">Rest</label>
              <input type="text" value={editRest} onChange={e => setEditRest(e.target.value)} className="w-full text-sm px-2 py-1 border border-amber-200 rounded bg-white" />
            </div>
          </div>
          <div className="flex justify-end gap-2 pt-1">
            <button onClick={() => { onEditPrescription?.({ sets_reps: editSetsReps, loading_method: editLoad, rest: editRest }); setShowEditInput(false); }} className="text-xs bg-amber-600 text-white px-3 py-1 rounded font-bold">Apply</button>
            <button onClick={() => setShowEditInput(false)} className="text-xs text-slate-500 px-2 py-1">Cancel</button>
          </div>
        </div>
      )}

      {/* Coach Actions Overlay (Hover) */}
      {!isSessionLocked && (
        <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity flex gap-1 bg-white/90 backdrop-blur pb-1 pl-1 rounded-bl">
          <div className="flex flex-col gap-0.5 mr-1 border-r border-slate-200 pr-1">
            {onMoveUp && index > 0 && <button onClick={() => onMoveUp(exercise.id)} className="p-1 text-slate-400 hover:text-slate-700 rounded" title="Move up"><ChevronUp className="w-3 h-3" /></button>}
            {onMoveDown && index < total - 1 && <button onClick={() => onMoveDown(exercise.id)} className="p-1 text-slate-400 hover:text-slate-700 rounded" title="Move down"><ChevronDown className="w-3 h-3" /></button>}
          </div>
          <div className="flex flex-col gap-1">
            <button
              onClick={() => { setShowSwapInput(!showSwapInput); setShowEditInput(false); }}
              className="p-1.5 text-slate-400 hover:text-indigo-600 hover:bg-slate-100 rounded"
              title="Swap Exercise"
            >
              <Repeat className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => { setShowEditInput(!showEditInput); setShowSwapInput(false); }}
              className="p-1.5 text-slate-400 hover:text-amber-600 hover:bg-slate-100 rounded"
              title="Edit Prescription"
            >
              <Edit2 className="w-3.5 h-3.5" />
            </button>
            {onRemove && (
              <button onClick={() => onRemove(exercise.id)} className="p-1.5 text-red-300 hover:text-red-600 hover:bg-red-50 rounded" title="Remove exercise">
                <X className="w-3.5 h-3.5" />
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
