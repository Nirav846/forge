/**
 * FORGE Coach Console — wired to the real FORGE Python API.
 *
 * API calls go through src/lib/api.ts (real fetch).
 * Normalization still goes through src/lib/transformers.ts.
 * MockApi is preserved as a dev/safety fallback if the backend is unreachable.
 */
import { useState, useEffect, useCallback, useRef } from 'react';
import { ProgramRequest, Mode } from './types';
import { TransformationResult, SavedProgramArtifact, ProgramStatus, WeekVM, SessionVM, ExerciseVM, TeamTemplate, TeamTemplateListItem } from './types/ui';
import type { SaveState } from './components/SaveIndicator';
import { generateProgram as apiGenerate } from './lib/api';
import { saveArtifact as apiSave, listArtifacts as apiList, loadArtifact as apiLoad, deleteArtifact as apiDelete, duplicateArtifact as apiDuplicate, updateArtifact as apiPatch, loadTeamTemplate } from './lib/api';
import { generateProgramMock } from './lib/mockApi';
import { normalizeProgramResponse } from './lib/transformers';
import { mockScenarios, defaultEmptyRequest } from './lib/mockFixtures';
import LeftPanel from './components/LeftPanel';
import CenterPanel from './components/CenterPanel';
import RightPanel from './components/RightPanel';
import { ErrorBoundary } from './components/ErrorBoundary';
import { Activity, Library, ClipboardCheck, AlertTriangle, Plus } from 'lucide-react';
import { SavedProgramsDrawer } from './components/program/SavedProgramsDrawer';
import { ProgramDocumentView } from './components/program/ProgramDocumentView';
import { UATRunner } from './components/UATRunner';
import { EntryScreen, TemplateType } from './components/EntryScreen';
import { TeamTemplateForm } from './components/team/TeamTemplateForm';
import { TeamTemplateView } from './components/team/TeamTemplateView';
import { TeamAdaptationWizard } from './components/team/TeamAdaptationWizard';
import { TeamLibraryDrawer } from './components/team/TeamLibraryDrawer';

export type AppStatus = 'idle' | 'loading' | 'success' | 'error';
type TeamStage = 'team_form' | 'team_view' | 'team_adapt' | null;

export default function App() {
  const [request, setRequest] = useState<ProgramRequest>(defaultEmptyRequest);
  const [result, setResult] = useState<TransformationResult | null>(null);
  const [status, setStatus] = useState<AppStatus>('idle');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  
  const [savedPrograms, setSavedPrograms] = useState<SavedProgramArtifact[]>([]);
  const [activeArtifactStatus, setActiveArtifactStatus] = useState<ProgramStatus>('draft');
  const [activeArtifactId, setActiveArtifactId] = useState<string | null>(null);
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [isDocumentViewOpen, setIsDocumentViewOpen] = useState(false);
  const [useMockFallback, setUseMockFallback] = useState(false);
  const [isUATOpen, setIsUATOpen] = useState(false);
  const [stage, setStage] = useState<string>('entry');
  const [formSourceProgramId, setFormSourceProgramId] = useState<string | undefined>();
  const [formTemplateValues, setFormTemplateValues] = useState<Partial<ProgramRequest> | undefined>();

  // Team state
  const [teamStage, setTeamStage] = useState<TeamStage>(null);
  const [currentTeamTemplate, setCurrentTeamTemplate] = useState<TeamTemplate | null>(null);
  const [isTeamLibraryOpen, setIsTeamLibraryOpen] = useState(false);
  const [coachOverrides, setCoachOverrides] = useState<Record<string, any>>({});
  const [overrideSaveState, setOverrideSaveState] = useState<'idle' | 'saving' | 'saved' | 'error'>('idle');
  const [overrideSaveTimer, setOverrideSaveTimer] = useState<ReturnType<typeof setTimeout> | null>(null);
  const [reviewSaveState, setReviewSaveState] = useState<SaveState>('idle');

  // ── Undo/Redo stack (ref avoids stale-closure + async-setter issues) ──
  const undoStack = useRef<WeekVM[][]>([]);
  const redoStack = useRef<WeekVM[][]>([]);
  const MAX_UNDO = 50;

  // Load saved artifacts from backend on mount
  useEffect(() => {
    apiList()
      .then(data => {
        if (data.artifacts) {
          // ponytail: load full details for each — simple list with no pagination yet
          Promise.all(data.artifacts.map((a: any) => apiLoad(a.id).catch(() => null)))
            .then(full => setSavedPrograms(full.filter(Boolean)))
            .catch(() => {});
        }
      })
      .catch(() => {
        setUseMockFallback(true);
      });
  }, []);

  const handleGenerate = useCallback(async (builtRequest?: ProgramRequest) => {
    const req = builtRequest || request;
    setStatus('loading');
    setErrorMessage(null);
    try {
      let rawPayload: any;

      if (useMockFallback) {
        rawPayload = await generateProgramMock(req);
      } else {
        rawPayload = await apiGenerate(req);
      }

      const transformed = normalizeProgramResponse(rawPayload);
      setResult(transformed);
      setRequest(req);
      setStatus('success');
      setActiveArtifactStatus('draft');
      setActiveArtifactId(null);
    } catch (err: any) {
      console.error("Program generation failed", err);
      // If real API fails, try mock fallback
      if (!useMockFallback) {
        try {
          setUseMockFallback(true);
          const rawPayload = await generateProgramMock(req);
          const transformed = normalizeProgramResponse(rawPayload);
          setResult(transformed);
          setRequest(req);
          setStatus('success');
          setActiveArtifactStatus('draft');
          setActiveArtifactId(null);
          return;
        } catch {}
      }
      setErrorMessage(err.message || 'Unknown generation error occurred.');
      setStatus('error');
    }
  }, [request, useMockFallback]);

  const handleSelectSource = useCallback((sourceId: string) => {
    const existing = savedPrograms.find(p => p.id === sourceId);
    if (existing) {
      setRequest(existing.request_snapshot);
      setResult(existing.result_snapshot);
      setActiveArtifactId(existing.id);
      setActiveArtifactStatus(existing.status);
      setCoachOverrides(existing.coach_overrides || {});
      setStatus('success');
      setStage('idle');
    } else {
      setFormSourceProgramId(sourceId);
      setStage('idle');
    }
  }, [savedPrograms]);

  const handleSelectTemplate = useCallback((template: TemplateType) => {
    const values = mockScenarios[template] as unknown as Partial<ProgramRequest> | undefined;
    if (values) {
      setRequest(prev => ({
        ...prev,
        ...values,
        basics: { ...prev.basics, ...values.basics },
        context: { ...prev.context, ...values.context },
        advanced: { ...prev.advanced, ...values.advanced },
      }));
    }
    setFormSourceProgramId(undefined);
    setFormTemplateValues(undefined);
    setStage('idle');
  }, []);

  const handleStartFresh = useCallback(() => {
    setFormSourceProgramId(undefined);
    setFormTemplateValues(undefined);
    setStage('idle');
  }, []);


  // ── Team Callbacks ──

  const handleStartTeamTemplate = useCallback(() => {
    setTeamStage('team_form');
    setCurrentTeamTemplate(null);
  }, []);

  const handleTeamTemplateGenerated = useCallback((template: TeamTemplate) => {
    setCurrentTeamTemplate(template);
    setTeamStage('team_view');
  }, []);

  const handleViewTeamTemplate = useCallback(async (id: string) => {
    try {
      const tpl = await loadTeamTemplate(id);
      setCurrentTeamTemplate(tpl);
      setTeamStage('team_view');
    } catch {}
  }, []);

  const handleAdaptTeamTemplate = useCallback((template: TeamTemplate) => {
    setCurrentTeamTemplate(template);
    setTeamStage('team_adapt');
  }, []);

  const handleTeamBack = useCallback(() => {
    setTeamStage(null);
    setCurrentTeamTemplate(null);
  }, []);

  const handleTeamAdaptComplete = useCallback((result: any) => {
    setResult(result);
    setStatus('success');
    setRequest(prev => ({
      ...prev,
      basics: { ...prev.basics, athlete_name: result.viewModel?.summary?.blueprint_selected || 'Adapted Athlete' },
    }));
    setTeamStage(null);
    setCurrentTeamTemplate(null);
  }, []);

  const patchWeeks = useCallback((fn: (weeks: WeekVM[]) => WeekVM[]) => {
    setResult(prev => {
      if (!prev?.viewModel) return prev;
      // snapshot before change
      undoStack.current = [...undoStack.current.slice(-(MAX_UNDO - 1)), prev.viewModel.weeks];
      redoStack.current = [];
      return { ...prev, viewModel: { ...prev.viewModel, weeks: fn(prev.viewModel.weeks) } };
    });
  }, []);

  const handleUndo = useCallback(() => {
    setResult(prev => {
      if (!prev?.viewModel || undoStack.current.length === 0) return prev;
      const prevWeeks = undoStack.current.pop()!;
      redoStack.current = [...redoStack.current, prev.viewModel.weeks];
      return { ...prev, viewModel: { ...prev.viewModel, weeks: prevWeeks } };
    });
  }, []);

  const handleRedo = useCallback(() => {
    setResult(prev => {
      if (!prev?.viewModel || redoStack.current.length === 0) return prev;
      const nextWeeks = redoStack.current.pop()!;
      undoStack.current = [...undoStack.current, prev.viewModel.weeks];
      return { ...prev, viewModel: { ...prev.viewModel, weeks: nextWeeks } };
    });
  }, []);

  // Global keyboard shortcuts: Ctrl+Z undo, Ctrl+Y redo
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'z' && !e.shiftKey) {
        e.preventDefault();
        handleUndo();
      }
      if ((e.ctrlKey || e.metaKey) && (e.key === 'y' || (e.key === 'z' && e.shiftKey))) {
        e.preventDefault();
        handleRedo();
      }
    };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [handleUndo, handleRedo]);

  const handleDuplicateSession = useCallback((sessionId: string, weekNumber: number) => {
    patchWeeks(weeks => weeks.map(w => {
      if (w.week_number !== weekNumber) return w;
      const session = w.sessions.find(s => s.id === sessionId);
      if (!session) return w;
      const copy: SessionVM = { ...session, id: `${sessionId}_copy_${Date.now()}`, name: `${session.name} (Copy)` };
      return { ...w, sessions: [...w.sessions, copy] };
    }));
  }, [patchWeeks]);

  const handleDeleteSession = useCallback((sessionId: string, weekNumber: number) => {
    patchWeeks(weeks => weeks.map(w => {
      if (w.week_number !== weekNumber) return w;
      return { ...w, sessions: w.sessions.filter(s => s.id !== sessionId) };
    }));
  }, [patchWeeks]);

  const handleMoveSession = useCallback((sessionId: string, weekNumber: number, newSessionNumber: number) => {
    patchWeeks(weeks => weeks.map(w => {
      if (w.week_number !== weekNumber) return w;
      return { ...w, sessions: w.sessions.map(s => s.id === sessionId ? { ...s, session_number: newSessionNumber } : s) };
    }));
  }, [patchWeeks]);

  const handleAddSession = useCallback((weekNumber: number) => {
    const newId = `session_${Date.now()}`;
    const emptySession: SessionVM = {
      id: newId,
      name: 'New Session',
      week_number: weekNumber,
      session_number: 1,
      focus: 'General',
      warmup: { title: 'Warmup', exercises: [] },
      main_work: { title: 'Main Work', exercises: [] },
      conditioning: { title: 'Conditioning', exercises: [] },
    };
    patchWeeks(weeks => weeks.map(w => {
      if (w.week_number !== weekNumber) return w;
      return { ...w, sessions: [...w.sessions, emptySession] };
    }));
  }, [patchWeeks]);

  const handleReorderSession = useCallback((sessionId: string, weekNumber: number, direction: 'up' | 'down') => {
    patchWeeks(weeks => weeks.map(w => {
      if (w.week_number !== weekNumber) return w;
      const idx = w.sessions.findIndex(s => s.id === sessionId);
      if (idx === -1) return w;
      const swap = idx + (direction === 'up' ? -1 : 1);
      if (swap < 0 || swap >= w.sessions.length) return w;
      const sessions = [...w.sessions];
      [sessions[idx], sessions[swap]] = [sessions[swap], sessions[idx]];
      return { ...w, sessions };
    }));
  }, [patchWeeks]);

  const handleRemoveExercise = useCallback((sessionId: string, weekNumber: number, blockType: string, exerciseId: string) => {
    patchWeeks(weeks => weeks.map(w => {
      if (w.week_number !== weekNumber) return w;
      return {
        ...w,
        sessions: w.sessions.map(s => {
          if (s.id !== sessionId) return s;
          const section = blockType as 'warmup' | 'main_work' | 'conditioning';
          return { ...s, [section]: { ...s[section], exercises: s[section].exercises.filter(e => e.id !== exerciseId) } };
        })
      };
    }));
  }, [patchWeeks]);

  const handleMoveExercise = useCallback((sessionId: string, weekNumber: number, blockType: string, exerciseId: string, direction: 'up' | 'down') => {
    patchWeeks(weeks => weeks.map(w => {
      if (w.week_number !== weekNumber) return w;
      return {
        ...w,
        sessions: w.sessions.map(s => {
          if (s.id !== sessionId) return s;
          const section = blockType as 'warmup' | 'main_work' | 'conditioning';
          const exercises = [...s[section].exercises];
          const idx = exercises.findIndex(e => e.id === exerciseId);
          const swap = idx + (direction === 'up' ? -1 : 1);
          if (swap < 0 || swap >= exercises.length) return s;
          [exercises[idx], exercises[swap]] = [exercises[swap], exercises[idx]];
          return { ...s, [section]: { ...s[section], exercises } };
        })
      };
    }));
  }, [patchWeeks]);

  const handleAddExercise = useCallback((sessionId: string, weekNumber: number, blockType: string, exercise: { name: string; family: string }) => {
    const newExercise: ExerciseVM = {
      id: `ex_${Date.now()}`,
      name: exercise.name,
      family: exercise.family,
      sets_reps: '3x10',
      loading_method: 'Moderate',
      rest: '60s',
    };
    patchWeeks(weeks => weeks.map(w => {
      if (w.week_number !== weekNumber) return w;
      return {
        ...w,
        sessions: w.sessions.map(s => {
          if (s.id !== sessionId) return s;
          const section = blockType as 'warmup' | 'main_work' | 'conditioning';
          return { ...s, [section]: { ...s[section], exercises: [...s[section].exercises, newExercise] } };
        })
      };
    }));
  }, [patchWeeks]);

  const handleLoadUATScenario = (inputs: Record<string, any>) => {
    setRequest(prev => ({
      ...prev,
      mode: inputs.mode || prev.mode,
      basics: {
        ...prev.basics,
        ...(inputs.athlete_name !== undefined && { athlete_name: inputs.athlete_name }),
        ...(inputs.sport !== undefined && { sport: inputs.sport }),
        ...(inputs.level !== undefined && { level: inputs.level }),
        ...(inputs.age !== undefined && { age: inputs.age }),
        ...(inputs.training_age !== undefined && { training_age_years: inputs.training_age }),
        ...(inputs.available_minutes !== undefined && { available_minutes: inputs.available_minutes }),
        ...(inputs.role !== undefined && { role: inputs.role }),
        ...(inputs.days_to_match !== undefined && { days_to_match: inputs.days_to_match }),
        ...(inputs.frequency_per_week !== undefined && { frequency_per_week: inputs.frequency_per_week }),
      },
      context: {
        ...prev.context,
        ...(inputs.goal !== undefined && { primary_goal: inputs.goal }),
      },
      advanced: {
        ...prev.advanced,
        ...(inputs.force_velocity_profile !== undefined && { force_velocity_profile: inputs.force_velocity_profile }),
        ...(inputs.injury_flags !== undefined && { injury_risk_flags: inputs.injury_flags }),
        ...(inputs.cmj_band !== undefined && { cmj_band: inputs.cmj_band }),
        ...(inputs.landing_competency !== undefined && { technique_consistency: inputs.landing_competency }),
      },
    }));
  };

  const loadScenario = (key: string) => {
    if (mockScenarios[key]) {
      setRequest({
        ...defaultEmptyRequest,
        ...mockScenarios[key],
      } as ProgramRequest);
    } else if (key === 'error') {
       setRequest({
         ...defaultEmptyRequest,
         basics: { ...defaultEmptyRequest.basics, athlete_name: 'error' }
       });
    } else if (key === 'broken') {
       setRequest({
         ...defaultEmptyRequest,
         basics: { ...defaultEmptyRequest.basics, athlete_name: 'broken' }
       });
    }
  };

  const handleSaveDraft = async () => {
    if (!result || !result.viewModel) return;
    const prevNotes = activeArtifactId ? savedPrograms.find(p => p.id === activeArtifactId) : undefined;

    if (useMockFallback) {
      const activeArtifact: SavedProgramArtifact = {
        id: activeArtifactId || `prog_${Date.now()}`,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        version: 1,
        status: activeArtifactStatus,
        athlete_display_name: request.basics.athlete_name || 'Unknown Athlete',
        sport: request.basics.sport || 'General',
        role: request.basics.role || '-',
        goal: request.context.primary_goal || '-',
        blueprint_label: result.viewModel.summary.blueprint_selected || 'Custom Block',
        week_label: result.viewModel.summary.competition_window || '-',
        mode: request.mode as 'core' | 'premium',
        coach_notes: prevNotes?.coach_notes ?? '',
        internal_notes: prevNotes?.internal_notes ?? '',
        coach_overrides: coachOverrides,
        request_snapshot: JSON.parse(JSON.stringify(request)),
        result_snapshot: JSON.parse(JSON.stringify(result))
      };
      setSavedPrograms(prev => {
        const exists = prev.find(p => p.id === activeArtifact.id);
        if (exists) return prev.map(p => p.id === activeArtifact.id ? activeArtifact : p);
        return [activeArtifact, ...prev];
      });
      setActiveArtifactId(activeArtifact.id);
      return;
    }

    try {
      const saved = await apiSave({
        request_payload: JSON.parse(JSON.stringify(request)),
        response_payload: JSON.parse(JSON.stringify(result.rawPayload)),
        program_id: activeArtifactId || undefined,
        status: activeArtifactStatus,
      });

      const fullArtifact: SavedProgramArtifact = {
        id: saved.id,
        created_at: saved.created_at,
        updated_at: saved.updated_at,
        version: saved.version,
        status: saved.status as ProgramStatus,
        athlete_display_name: saved.athlete_display_name,
        sport: saved.sport,
        role: saved.role,
        goal: saved.goal,
        blueprint_label: saved.blueprint_label,
        week_label: saved.week_label,
        mode: saved.mode,
        coach_notes: prevNotes?.coach_notes ?? '',
        internal_notes: prevNotes?.internal_notes ?? '',
        coach_overrides: coachOverrides,
        request_snapshot: JSON.parse(JSON.stringify(request)),
        result_snapshot: JSON.parse(JSON.stringify(result)),
      };

      setSavedPrograms(prev => {
        const exists = prev.find(p => p.id === fullArtifact.id);
        if (exists) return prev.map(p => p.id === fullArtifact.id ? fullArtifact : p);
        return [fullArtifact, ...prev];
      });
      setActiveArtifactId(fullArtifact.id);
    } catch (err: any) {
      console.error("Save failed", err);
    }
  };

  const handleMarkReviewed = async () => {
    const newStatus = activeArtifactStatus === 'draft' ? 'reviewed' : 'draft';
    setReviewSaveState('saving');
    if (!useMockFallback && activeArtifactId) {
      try {
        const updated = await apiPatch(activeArtifactId, { status: newStatus });
        setActiveArtifactStatus(newStatus);
        setSavedPrograms(prev => prev.map(p => p.id === activeArtifactId ? { ...p, status: newStatus as ProgramStatus, updated_at: updated.updated_at } : p));
        setReviewSaveState('saved');
        setTimeout(() => setReviewSaveState('idle'), 2000);
      } catch (err: any) {
        setReviewSaveState('error');
        setTimeout(() => setReviewSaveState('idle'), 4000);
        console.error("Status update failed", err);
      }
    } else {
      setActiveArtifactStatus(newStatus);
      setReviewSaveState('saved');
      setTimeout(() => setReviewSaveState('idle'), 2000);
    }
  };

  const handleUpdateNotes = async (notes: string, field: 'coach_notes' | 'internal_notes'): Promise<boolean> => {
    if (!activeArtifactId || useMockFallback) return true;
    try {
      const updated = await apiPatch(activeArtifactId, { [field]: notes });
      setSavedPrograms(prev => prev.map(p => p.id === activeArtifactId ? { ...p, [field]: notes, updated_at: updated.updated_at } : p));
      return true;
    } catch (err: any) {
      console.error("Notes update failed", err);
      return false;
    }
  };

  const handleUpdateOverrides = useCallback(async (newOverrides: Record<string, any>) => {
    setCoachOverrides(newOverrides);
    if (overrideSaveTimer) clearTimeout(overrideSaveTimer);
    if (!activeArtifactId || useMockFallback) {
      setSavedPrograms(prev => prev.map(p => p.id === activeArtifactId ? { ...p, coach_overrides: newOverrides } : p));
      return;
    }
    const timer = setTimeout(async () => {
      setOverrideSaveState('saving');
      try {
        const updated = await apiPatch(activeArtifactId, { coach_overrides: newOverrides });
        setSavedPrograms(prev => prev.map(p => p.id === activeArtifactId ? { ...p, coach_overrides: newOverrides, updated_at: updated.updated_at } : p));
        setOverrideSaveState('saved');
        setTimeout(() => setOverrideSaveState('idle'), 2000);
      } catch (err: any) {
        console.error("Override save failed", err);
        setOverrideSaveState('error');
        setTimeout(() => setOverrideSaveState('idle'), 4000);
      }
    }, 500);
    setOverrideSaveTimer(timer);
  }, [activeArtifactId, useMockFallback, overrideSaveTimer]);

  const handleDuplicate = async () => {
    if (!activeArtifactId || useMockFallback) return;
    try {
      const dup = await apiDuplicate(activeArtifactId);
      const transformed = normalizeProgramResponse(dup.result_snapshot);
      const fullArtifact: SavedProgramArtifact = {
        id: dup.id,
        created_at: dup.created_at,
        updated_at: dup.updated_at,
        version: dup.version,
        status: dup.status as ProgramStatus,
        athlete_display_name: dup.athlete_display_name,
        sport: dup.sport,
        role: dup.role,
        goal: dup.goal,
        blueprint_label: dup.blueprint_label,
        week_label: dup.week_label,
        mode: dup.mode,
        coach_notes: dup.coach_notes ?? '',
        internal_notes: dup.internal_notes ?? '',
        request_snapshot: dup.request_snapshot,
        result_snapshot: dup.result_snapshot,
      };
      setResult(transformed);
      setRequest(dup.request_snapshot);
      setSavedPrograms(prev => [fullArtifact, ...prev]);
      setActiveArtifactId(dup.id);
      setActiveArtifactStatus('draft');
    } catch (err: any) {
      console.error("Duplicate failed", err);
    }
  };

  const handleDelete = async (id: string) => {
    if (useMockFallback) {
      setSavedPrograms(prev => prev.filter(p => p.id !== id));
      if (activeArtifactId === id) {
        setActiveArtifactId(null);
        setActiveArtifactStatus('draft');
      }
      return;
    }
    try {
      await apiDelete(id);
      setSavedPrograms(prev => prev.filter(p => p.id !== id));
      if (activeArtifactId === id) {
        setActiveArtifactId(null);
        setActiveArtifactStatus('draft');
      }
    } catch (err: any) {
      console.error("Delete failed", err);
    }
  };

  const handleSelectSavedProgram = async (id: string) => {
    if (useMockFallback) {
      const artifact = savedPrograms.find(p => p.id === id);
      if (!artifact) return;
      setRequest(artifact.request_snapshot);
      setResult(artifact.result_snapshot);
      setActiveArtifactId(artifact.id);
      setActiveArtifactStatus(artifact.status);
      setCoachOverrides(artifact.coach_overrides || {});
      setStatus('success');
      setIsDrawerOpen(false);
      return;
    }

    try {
      const artifact = await apiLoad(id);
      setRequest(artifact.request_snapshot);
      const transformed = normalizeProgramResponse(artifact.result_snapshot);
      setResult(transformed);
      setActiveArtifactId(artifact.id);
      setActiveArtifactStatus(artifact.status || 'draft');
      setCoachOverrides(artifact.coach_overrides || {});
      setStatus('success');
      setIsDrawerOpen(false);
    } catch (err: any) {
      console.error("Load failed", err);
    }
  };

  const documentArtifact = activeArtifactId
    ? savedPrograms.find(p => p.id === activeArtifactId)
    : result
      ? {
          id: 'preview',
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          version: 1,
          status: activeArtifactStatus,
          athlete_display_name: request.basics.athlete_name || 'Athlete Name',
          sport: request.basics.sport || 'Sport',
          role: request.basics.role || 'Role',
          goal: request.context.primary_goal || 'Goal',
          blueprint_label: result.viewModel?.summary.blueprint_selected || 'Blueprint',
          week_label: result.viewModel?.summary.competition_window || '-',
          mode: request.mode as 'core' | 'premium',
          coach_notes: '',
          internal_notes: '',
          coach_overrides: coachOverrides,
          request_snapshot: request,
          result_snapshot: result,
        }
      : null;
  
  return (
    <div className="flex flex-col h-screen bg-slate-50 text-slate-900 font-sans overflow-hidden">
      {/* Header */}
      <header className="flex-none h-14 bg-slate-900 text-white flex items-center px-6 border-b border-slate-800 shrink-0 shadow-sm z-10">
        <Activity className="w-5 h-5 text-indigo-400 mr-3" />
        <h1 className="font-semibold tracking-wide text-sm">FORGE <span className="text-slate-400 font-normal">| Coach Console</span></h1>
        
         <div className="ml-8 flex items-center gap-2">
            <button onClick={() => setIsTeamLibraryOpen(true)} className="flex items-center gap-2 text-xs text-amber-300 hover:text-white bg-amber-900/30 hover:bg-amber-800/50 px-3 py-1.5 rounded-md transition-colors border border-amber-800/30">
               <Library className="w-4 h-4" /> Team Templates
            </button>
            <button onClick={() => setIsDrawerOpen(true)} className="flex items-center gap-2 text-xs text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 px-3 py-1.5 rounded-md transition-colors">
               <Library className="w-4 h-4" /> Library {savedPrograms.length > 0 && `(${savedPrograms.length})`}
            </button>
            <button onClick={() => setIsUATOpen(true)} className="flex items-center gap-1.5 text-xs text-emerald-300 hover:text-emerald-200 bg-emerald-900/30 hover:bg-emerald-900/50 px-2.5 py-1.5 rounded-md transition-colors border border-emerald-800/30">
               <ClipboardCheck className="w-3.5 h-3.5" /> UAT
            </button>
         </div>

        <div className="ml-auto flex items-center space-x-4 text-xs z-50">
          {useMockFallback && (
            <span className="flex items-center gap-1.5 text-amber-300 bg-amber-900/30 px-2.5 py-1 rounded-md border border-amber-800/30">
              <AlertTriangle className="w-3 h-3" /> Mock Mode
            </span>
          )}
          <span className="text-slate-400">Testing:</span>
          <button onClick={() => loadScenario('rugby_prop')} className="hover:text-indigo-300 transition-colors">Rugby (Adv)</button>
          <button onClick={() => loadScenario('tennis_singles')} className="hover:text-indigo-300 transition-colors">Tennis</button>
          <button onClick={() => loadScenario('cricket_bowler')} className="hover:text-indigo-300 transition-colors">Cricket</button>
          <span className="text-slate-600">|</span>
          <button onClick={() => loadScenario('broken')} className="text-amber-400 hover:text-amber-300 transition-colors">Broken Data</button>
          <button onClick={() => loadScenario('error')} className="text-red-400 hover:text-red-300 transition-colors">API Error</button>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex overflow-hidden relative">
        {status === 'idle' && stage === 'entry' && !teamStage ? (
          <div className="flex-1 flex items-center justify-center">
            <ErrorBoundary>
              <EntryScreen
                onSelectSource={handleSelectSource}
                onSelectTemplate={handleSelectTemplate}
                onStartFresh={handleStartFresh}
                onStartTeamTemplate={handleStartTeamTemplate}
                savedPrograms={savedPrograms}
              />
            </ErrorBoundary>
          </div>
        ) : teamStage === 'team_form' ? (
          <div className="flex-1">
            <ErrorBoundary>
              <TeamTemplateForm
                onComplete={handleTeamTemplateGenerated}
                onBack={handleTeamBack}
              />
            </ErrorBoundary>
          </div>
        ) : teamStage === 'team_view' && currentTeamTemplate ? (
          <div className="flex-1">
            <ErrorBoundary>
              <TeamTemplateView
                template={currentTeamTemplate}
                onAdapt={handleAdaptTeamTemplate}
                onBack={handleTeamBack}
              />
            </ErrorBoundary>
          </div>
        ) : teamStage === 'team_adapt' && currentTeamTemplate ? (
          <div className="flex-1">
            <ErrorBoundary>
              <TeamAdaptationWizard
                template={currentTeamTemplate}
                onComplete={handleTeamAdaptComplete}
                onBack={handleTeamBack}
              />
            </ErrorBoundary>
          </div>
        ) : (
          <>
            {/* Left Panel: Builder (w-96) */}
            <div className="w-96 flex-none bg-white border-r border-slate-200 overflow-y-auto shadow-[4px_0_24px_rgba(0,0,0,0.02)] z-10 flex flex-col">
              <ErrorBoundary>
                <LeftPanel 
                  request={request} 
                  setRequest={setRequest} 
                  onGenerate={handleGenerate}
                  status={status}
                />
              </ErrorBoundary>
            </div>

            {/* Center Panel: Output (flex-1) */}
            <div className="flex-1 bg-slate-50 overflow-y-auto px-8 py-8 relative">
              <ErrorBoundary>
                <CenterPanel 
                  result={result} 
                  status={status} 
                  errorMessage={errorMessage}
                  requestName={request.basics.athlete_name}
                  artifactStatus={activeArtifactStatus}
                  savedPrograms={savedPrograms}
                  onSaveDraft={handleSaveDraft}
                  onMarkReviewed={handleMarkReviewed}
                  onOpenDocument={() => setIsDocumentViewOpen(true)}
                  onDuplicate={handleDuplicate}
                  onUpdateNotes={handleUpdateNotes}
                  coachNotes={savedPrograms.find(p => p.id === activeArtifactId)?.coach_notes ?? ''}
                  internalNotes={savedPrograms.find(p => p.id === activeArtifactId)?.internal_notes ?? ''}
                  coachOverrides={coachOverrides}
                  onUpdateOverrides={handleUpdateOverrides}
                  reviewSaveState={reviewSaveState}
                  onDuplicateSession={handleDuplicateSession}
                  onDeleteSession={handleDeleteSession}
                  onMoveSession={handleMoveSession}
                  onAddSession={handleAddSession}
                  onReorderSession={handleReorderSession}
                  onRemoveExercise={handleRemoveExercise}
                  onMoveExercise={handleMoveExercise}
                  onAddExercise={handleAddExercise}
                  onUndo={handleUndo}
                  onRedo={handleRedo}
                  canUndo={undoStack.current.length > 0}
                  canRedo={redoStack.current.length > 0}
                />
              </ErrorBoundary>
            </div>

            {/* Right Panel: Rationale/Debug (w-80) */}
            <div className="w-80 flex-none bg-slate-900 text-slate-300 border-l border-slate-800 overflow-y-auto text-sm shrink-0">
              <ErrorBoundary>
                <RightPanel result={result} request={request} />
              </ErrorBoundary>
            </div>
          </>
        )}
      </main>

      {/* Render Document View Modal if Open */}
      {isDocumentViewOpen && documentArtifact && (
        <ProgramDocumentView 
           artifact={documentArtifact} 
           onClose={() => setIsDocumentViewOpen(false)} 
        />
      )}

      {/* Render Saved Programs Drawer */}
      <SavedProgramsDrawer 
         isOpen={isDrawerOpen} 
         onClose={() => setIsDrawerOpen(false)} 
         savedPrograms={savedPrograms}
         onSelectProgram={handleSelectSavedProgram}
         onDelete={handleDelete}
         activeId={activeArtifactId}
      />

      {isUATOpen && (
        <UATRunner 
          onClose={() => setIsUATOpen(false)} 
          onLoadScenario={handleLoadUATScenario}
        />
      )}

      <TeamLibraryDrawer
        isOpen={isTeamLibraryOpen}
        onClose={() => setIsTeamLibraryOpen(false)}
        onSelectTemplate={handleViewTeamTemplate}
      />
    </div>
  );
}
