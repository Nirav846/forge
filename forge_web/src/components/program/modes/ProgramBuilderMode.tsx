import React, { useState, useCallback, useRef } from 'react';
import { ProgramViewModel, CoachOverrides, SessionOverride, ExerciseSwap, PrescriptionEdit, WeekVM, TransformerWarning, SessionVM } from '../../../types/ui';
import { SessionCard } from '../blocks';
import { Layers, Activity, CalendarDays, Target, AlertCircle, Plus, ChevronUp, ChevronDown, ShieldAlert, BarChart3, Undo2, Redo2, GripVertical } from 'lucide-react';

const DAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

interface TestAdjustmentInfo {
  has_data?: boolean;
  conditioning_multiplier?: number;
  sprint_multiplier?: number;
  power_emphasis?: string;
  power_multiplier?: number;
  adjustments?: string[];
}

interface ProgramBuilderModeProps {
  viewModel: ProgramViewModel;
  warnings?: TransformerWarning[];
  testAdjustments?: TestAdjustmentInfo;
  overrides: CoachOverrides;
  onUpdateOverrides: (overrides: CoachOverrides) => void;
  onDuplicateSession?: (sessionId: string, weekNumber: number) => void;
  onDeleteSession?: (sessionId: string, weekNumber: number) => void;
  onMoveSession?: (sessionId: string, weekNumber: number, newSessionNumber: number) => void;
  onAddSession?: (weekNumber: number) => void;
  onReorderSession?: (sessionId: string, weekNumber: number, direction: 'up' | 'down') => void;
  onRemoveExercise?: (sessionId: string, weekNumber: number, blockType: string, exerciseId: string) => void;
  onMoveExercise?: (sessionId: string, weekNumber: number, blockType: string, exerciseId: string, direction: 'up' | 'down') => void;
  onAddExercise?: (sessionId: string, weekNumber: number, blockType: string, exercise: { name: string; family: string }) => void;
  onUndo?: () => void;
  onRedo?: () => void;
  canUndo?: boolean;
  canRedo?: boolean;
}

/** Map day index (0-6) to session for a given week */
function sessionsByDay(week: WeekVM): Map<number, SessionVM[]> {
  const map = new Map<number, SessionVM[]>();
  const teamDays: string[] = week.sessions[0]?.name ? [] : [];
  week.sessions.forEach(s => {
    const dayIdx = s.session_number != null ? s.session_number - 1 : 0;
    const existing = map.get(dayIdx) || [];
    existing.push(s);
    map.set(dayIdx, existing);
  });
  return map;
}

export function ProgramBuilderMode({
  viewModel, warnings = [], testAdjustments, overrides, onUpdateOverrides,
  onDuplicateSession, onDeleteSession, onMoveSession, onAddSession, onReorderSession,
  onRemoveExercise, onMoveExercise, onAddExercise,
  onUndo, onRedo, canUndo = false, canRedo = false
}: ProgramBuilderModeProps) {
  const [activeWeekNum, setActiveWeekNum] = React.useState<number>(viewModel.weeks[0]?.week_number || 1);
  const [warningsOpen, setWarningsOpen] = useState(true);

  // ── Drag-and-drop session state ──
  const dragSessionRef = useRef<{ id: string; sourceWeek: number } | null>(null);

  const handleSessionDragStart = useCallback((e: React.DragEvent, sessionId: string, weekNum: number) => {
    dragSessionRef.current = { id: sessionId, sourceWeek: weekNum };
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', sessionId);
  }, []);

  const handleWeekDrop = useCallback((e: React.DragEvent, targetWeekNum: number) => {
    e.preventDefault();
    const src = dragSessionRef.current;
    if (!src || src.sourceWeek === targetWeekNum) return;
    onMoveSession?.(src.id, src.sourceWeek, 1); // move to target week, session 1
    dragSessionRef.current = null;
  }, [onMoveSession]);

  const handleWeekDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  }, []);

  // ── Edit prescription wrapper that records history ──
  const handleEditPrescription = useCallback((sessionId: string, exerciseId: string, edit: PrescriptionEdit) => {
    const current = overrides.sessions?.[sessionId] || {};
    const exercises = current.exercises || {};
    onUpdateOverrides({
      ...overrides,
      sessions: { ...(overrides.sessions || {}), [sessionId]: { ...current, exercises: { ...exercises, [exerciseId]: { prescription: edit } } } }
    });
  }, [overrides, onUpdateOverrides]);

  const handleSwapExercise = useCallback((sessionId: string, exerciseId: string, swap: ExerciseSwap) => {
    const current = overrides.sessions?.[sessionId] || {};
    const exercises = current.exercises || {};
    onUpdateOverrides({
      ...overrides,
      sessions: { ...(overrides.sessions || {}), [sessionId]: { ...current, exercises: { ...exercises, [exerciseId]: { swap } } } }
    });
  }, [overrides, onUpdateOverrides]);

  const handleToggleLock = useCallback((sessionId: string, locked: boolean) => {
    const current = overrides.sessions?.[sessionId] || {};
    onUpdateOverrides({
      ...overrides,
      sessions: { ...(overrides.sessions || {}), [sessionId]: { ...current, locked } }
    });
  }, [overrides, onUpdateOverrides]);

  const handleAddNote = useCallback((sessionId: string, note: string) => {
    const current = overrides.sessions?.[sessionId] || {};
    onUpdateOverrides({
      ...overrides,
      sessions: { ...(overrides.sessions || {}), [sessionId]: { ...current, note } }
    });
  }, [overrides, onUpdateOverrides]);

  const handleClearNote = useCallback((sessionId: string) => {
    const current = overrides.sessions?.[sessionId] || {};
    onUpdateOverrides({
      ...overrides,
      sessions: { ...(overrides.sessions || {}), [sessionId]: { ...current, note: null } }
    });
  }, [overrides, onUpdateOverrides]);

  const activeWeek = viewModel.weeks.find(w => w.week_number === activeWeekNum);
  const sessionsData = overrides.sessions || {};

  return (
    <div className="space-y-6">
      {/* ── Undo/Redo Toolbar ── */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-1">
          <button onClick={onUndo} disabled={!canUndo} className="p-1.5 rounded-md text-slate-500 hover:text-slate-800 hover:bg-slate-200 disabled:opacity-30 disabled:cursor-not-allowed transition-colors" title="Undo (Ctrl+Z)">
            <Undo2 className="w-4 h-4" />
          </button>
          <button onClick={onRedo} disabled={!canRedo} className="p-1.5 rounded-md text-slate-500 hover:text-slate-800 hover:bg-slate-200 disabled:opacity-30 disabled:cursor-not-allowed transition-colors" title="Redo (Ctrl+Y)">
            <Redo2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* ── Calendar Week View ── */}
      <div className="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm">
        {/* Week labels row */}
        <div className="grid grid-cols-7 bg-slate-50 border-b border-slate-200">
          {DAY_NAMES.map(d => (
            <div key={d} className="text-center text-[11px] font-bold text-slate-400 uppercase tracking-wider py-2 border-r border-slate-200 last:border-r-0">
              {d}
            </div>
          ))}
        </div>
        {/* Calendar grid: each week is a row */}
        <div className="divide-y divide-slate-100">
          {viewModel.weeks.map(week => {
            const isActive = activeWeekNum === week.week_number;
            const byDay = sessionsByDay(week);
            return (
              <div
                key={week.week_number}
                className={`grid grid-cols-7 min-h-[60px] transition-colors cursor-pointer ${isActive ? 'bg-indigo-50/40' : 'hover:bg-slate-50/60'}`}
                onClick={() => setActiveWeekNum(week.week_number)}
                onDragOver={handleWeekDragOver}
                onDrop={(e) => { e.stopPropagation(); handleWeekDrop(e, week.week_number); }}
              >
                {[0, 1, 2, 3, 4, 5, 6].map(dayIdx => {
                  const sessionsOnDay = byDay.get(dayIdx) || [];
                  return (
                    <div
                      key={dayIdx}
                      className="border-r border-slate-100 last:border-r-0 p-1 min-h-[60px]"
                      onDragOver={handleWeekDragOver}
                      onDrop={(e) => { e.stopPropagation(); handleWeekDrop(e, week.week_number); }}
                    >
                      <div className="text-[10px] text-slate-400 font-semibold mb-0.5">
                        {week.label.split(' ')[0] || `W${week.week_number}`}
                      </div>
                      {sessionsOnDay.map(s => (
                        <div
                          key={s.id}
                          draggable
                          onDragStart={(e) => handleSessionDragStart(e, s.id, week.week_number)}
                          className={`text-[10px] px-1 py-0.5 rounded mb-0.5 truncate font-medium cursor-grab active:cursor-grabbing ${
                            isActive ? 'bg-indigo-100 text-indigo-800' : 'bg-slate-100 text-slate-700'
                          }`}
                        >
                          {s.name}
                        </div>
                      ))}
                    </div>
                  );
                })}
              </div>
            );
          })}
        </div>
      </div>

      {/* ── Active Week Details ── */}
      {activeWeek && (
        <div className="animate-in fade-in slide-in-from-bottom-2 duration-300">
          <div className="flex items-center justify-between mb-4 border-b border-slate-200 pb-2">
            <h3 className="text-lg font-bold text-slate-900">{activeWeek.label} Workspace</h3>
            <div className="flex items-center gap-2 text-xs text-slate-500">
              <span className="flex items-center gap-1"><Activity className="w-3 h-3" /> {activeWeek.sessions.length} sessions</span>
              <span className="flex items-center gap-1"><Target className="w-3 h-3" /> {activeWeek.exposure_summary?.week_type || 'General'}</span>
            </div>
          </div>

          {activeWeek.sessions.length > 0 ? (
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 items-start">
              {activeWeek.sessions.map(session => {
                const override = sessionsData[session.id] || {};
                return (
                  <div key={session.id} className="relative group">
                    {/* Floating quick-action toolbar on hover */}
                    <div className="absolute -top-2 -right-2 z-20 opacity-0 group-hover:opacity-100 transition-opacity flex gap-0.5 bg-white rounded-lg border border-slate-200 shadow-md px-1 py-0.5">
                      {onDuplicateSession && (
                        <button onClick={() => onDuplicateSession(session.id, activeWeekNum)} className="p-1 text-slate-400 hover:text-indigo-600 rounded" title="Duplicate session">
                          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
                        </button>
                      )}
                      {onDeleteSession && (
                        <button onClick={() => onDeleteSession(session.id, activeWeekNum)} className="p-1 text-red-300 hover:text-red-600 rounded" title="Delete session">
                          <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                        </button>
                      )}
                      {onMoveSession && (
                        <div className="relative group/day-dropdown">
                          <button className="p-1 text-slate-400 hover:text-indigo-600 rounded" title="Move to day">
                            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                          </button>
                          <div className="absolute right-0 top-full mt-1 bg-white border border-slate-200 rounded-lg shadow-xl z-30 p-1 hidden group-hover/day-dropdown:block min-w-[120px]">
                            {[1, 2, 3, 4, 5, 6, 7].map(d => (
                              <button key={d} onClick={() => onMoveSession(session.id, activeWeekNum, d)} className="block w-full text-left px-3 py-1 text-xs text-slate-600 hover:bg-slate-100 rounded">
                                Session {d}
                              </button>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                    <SessionCard
                      session={session}
                      sessionOverride={override}
                      onToggleLock={handleToggleLock}
                      onAddNote={handleAddNote}
                      onClearNote={handleClearNote}
                      onSwapExercise={handleSwapExercise}
                      onEditPrescription={handleEditPrescription}
                      onDuplicateSession={onDuplicateSession ? (id) => onDuplicateSession(id, activeWeekNum) : undefined}
                      onDeleteSession={onDeleteSession ? (id) => onDeleteSession(id, activeWeekNum) : undefined}
                      onMoveSession={onMoveSession ? (id, num) => onMoveSession(id, activeWeekNum, num) : undefined}
                      onReorderSession={onReorderSession ? (id, dir) => onReorderSession(id, activeWeekNum, dir) : undefined}
                      onRemoveExercise={onRemoveExercise ? (id, bt, eid) => onRemoveExercise(id, activeWeekNum, bt, eid) : undefined}
                      onMoveExercise={onMoveExercise ? (id, bt, eid, dir) => onMoveExercise(id, activeWeekNum, bt, eid, dir) : undefined}
                      onAddExercise={onAddExercise ? (id, bt, ex) => onAddExercise(id, activeWeekNum, bt, ex) : undefined}
                    />
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="text-center py-12 bg-white rounded-xl border border-dashed border-slate-300 text-slate-400 font-medium">
              <Layers className="w-8 h-8 mx-auto mb-3 text-slate-300" />
              No sessions scheduled for this week.
            </div>
          )}
          {onAddSession && (
            <button onClick={() => onAddSession(activeWeekNum)} className="mt-6 w-full flex items-center justify-center gap-2 py-3 bg-white border-2 border-dashed border-slate-300 hover:border-indigo-400 hover:bg-indigo-50/30 rounded-xl text-sm text-slate-500 hover:text-indigo-600 transition-all">
              <Plus className="w-4 h-4" /> Add Session
            </button>
          )}
        </div>
      )}
    </div>
  );
}
