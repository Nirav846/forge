/**
 * FORGE Coach Console — wired to the real FORGE Python API.
 *
 * API calls go through src/lib/api.ts (real fetch).
 * Normalization still goes through src/lib/transformers.ts.
 * MockApi is preserved as a dev/safety fallback if the backend is unreachable.
 */
import { useState, useEffect, useCallback } from 'react';
import { ProgramRequest, Mode } from './types';
import { TransformationResult, SavedProgramArtifact, ProgramStatus } from './types/ui';
import { generateProgram as apiGenerate } from './lib/api';
import { saveArtifact as apiSave, listArtifacts as apiList, loadArtifact as apiLoad, deleteArtifact as apiDelete, duplicateArtifact as apiDuplicate, updateArtifact as apiPatch } from './lib/api';
import { generateProgramMock } from './lib/mockApi';
import { normalizeProgramResponse } from './lib/transformers';
import { mockScenarios, defaultEmptyRequest } from './lib/mockFixtures';
import LeftPanel from './components/LeftPanel';
import CenterPanel from './components/CenterPanel';
import RightPanel from './components/RightPanel';
import { Activity, Library, ClipboardCheck } from 'lucide-react';
import { SavedProgramsDrawer } from './components/program/SavedProgramsDrawer';
import { ProgramDocumentView } from './components/program/ProgramDocumentView';
import { UATRunner } from './components/UATRunner';

export type AppStatus = 'idle' | 'loading' | 'success' | 'error';

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

  // Load saved artifacts from backend on mount
  useEffect(() => {
    apiList()
      .then(data => {
        if (data.artifacts) {
          // Convert summary artifacts to full artifacts by loading each
          Promise.all(data.artifacts.map((a: any) => apiLoad(a.id).catch(() => null)))
            .then(full => {
              setSavedPrograms(full.filter(Boolean));
            })
            .catch(() => {});
        }
      })
      .catch(() => {
        // Backend not reachable — use mock fallback silently
        setUseMockFallback(true);
      });
  }, []);

  const handleGenerate = useCallback(async () => {
    setStatus('loading');
    setErrorMessage(null);
    try {
      let rawPayload: any;

      if (useMockFallback) {
        rawPayload = await generateProgramMock(request);
      } else {
        rawPayload = await apiGenerate(request);
      }

      const transformed = normalizeProgramResponse(rawPayload);
      setResult(transformed);
      setStatus('success');
      setActiveArtifactStatus('draft');
      setActiveArtifactId(null);
    } catch (err: any) {
      console.error("Program generation failed", err);
      // If real API fails, try mock fallback
      if (!useMockFallback) {
        try {
          setUseMockFallback(true);
          const rawPayload = await generateProgramMock(request);
          const transformed = normalizeProgramResponse(rawPayload);
          setResult(transformed);
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
    setActiveArtifactStatus(newStatus);
    if (!useMockFallback && activeArtifactId) {
      try {
        const updated = await apiPatch(activeArtifactId, { status: newStatus });
        setSavedPrograms(prev => prev.map(p => p.id === activeArtifactId ? { ...p, status: newStatus as ProgramStatus, updated_at: updated.updated_at } : p));
      } catch (err: any) {
        setActiveArtifactStatus(activeArtifactStatus);
        console.error("Status update failed", err);
      }
    }
  };

  const handleUpdateNotes = async (notes: string, field: 'coach_notes' | 'internal_notes') => {
    if (!activeArtifactId || useMockFallback) return;
    try {
      const updated = await apiPatch(activeArtifactId, { [field]: notes });
      setSavedPrograms(prev => prev.map(p => p.id === activeArtifactId ? { ...p, [field]: notes, updated_at: updated.updated_at } : p));
    } catch (err: any) {
      console.error("Notes update failed", err);
    }
  };

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

  const handleSelectSavedProgram = async (id: string) => {
    if (useMockFallback) {
      const artifact = savedPrograms.find(p => p.id === id);
      if (!artifact) return;
      setRequest(artifact.request_snapshot);
      setResult(artifact.result_snapshot);
      setActiveArtifactId(artifact.id);
      setActiveArtifactStatus(artifact.status);
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
      setStatus('success');
      setIsDrawerOpen(false);
    } catch (err: any) {
      console.error("Load failed", err);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-slate-50 text-slate-900 font-sans overflow-hidden">
      {/* Header */}
      <header className="flex-none h-14 bg-slate-900 text-white flex items-center px-6 border-b border-slate-800 shrink-0 shadow-sm z-10">
        <Activity className="w-5 h-5 text-indigo-400 mr-3" />
        <h1 className="font-semibold tracking-wide text-sm">FORGE <span className="text-slate-400 font-normal">| Coach Console</span></h1>
        
        <div className="ml-8 flex items-center gap-2">
           <button onClick={() => setIsDrawerOpen(true)} className="flex items-center gap-2 text-xs text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 px-3 py-1.5 rounded-md transition-colors">
              <Library className="w-4 h-4" /> Library {savedPrograms.length > 0 && `(${savedPrograms.length})`}
           </button>
           <button onClick={() => setIsUATOpen(true)} className="flex items-center gap-1.5 text-xs text-emerald-300 hover:text-emerald-200 bg-emerald-900/30 hover:bg-emerald-900/50 px-2.5 py-1.5 rounded-md transition-colors border border-emerald-800/30">
              <ClipboardCheck className="w-3.5 h-3.5" /> UAT
           </button>
        </div>

        <div className="ml-auto flex items-center space-x-4 text-xs z-50">
          <span className="text-slate-400">Testing:</span>
          <button onClick={() => loadScenario('rugby_prop')} className="hover:text-indigo-300 transition-colors">Rugby (Adv)</button>
          <button onClick={() => loadScenario('tennis_singles')} className="hover:text-indigo-300 transition-colors">Tennis</button>
          <button onClick={() => loadScenario('cricket_bowler')} className="hover:text-indigo-300 transition-colors">Cricket</button>
          <span className="text-slate-600">|</span>
          <button onClick={() => loadScenario('broken')} className="text-amber-400 hover:text-amber-300 transition-colors">Broken Data</button>
          <button onClick={() => loadScenario('error')} className="text-red-400 hover:text-red-300 transition-colors">API Error</button>
        </div>
      </header>

      {/* Main 3-Panel Layout */}
      <main className="flex-1 flex overflow-hidden relative">
        {/* Left Panel: Inputs (w-96) */}
        <div className="w-96 flex-none bg-white border-r border-slate-200 overflow-y-auto shadow-[4px_0_24px_rgba(0,0,0,0.02)] z-10 flex flex-col">
          <LeftPanel 
            request={request} 
            setRequest={setRequest} 
            onGenerate={handleGenerate}
            status={status}
          />
        </div>

        {/* Center Panel: Output (flex-1) */}
        <div className="flex-1 bg-slate-50 overflow-y-auto px-8 py-8 relative">
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
          />
        </div>

        {/* Right Panel: Rationale/Debug (w-80) */}
        <div className="w-80 flex-none bg-slate-900 text-slate-300 border-l border-slate-800 overflow-y-auto text-sm shrink-0">
          <RightPanel result={result} request={request} />
        </div>
      </main>

      {/* Render Document View Modal if Open */}
      {isDocumentViewOpen && activeArtifactId && (
        <ProgramDocumentView 
           artifact={savedPrograms.find(p => p.id === activeArtifactId) || { ...savedPrograms[0], result_snapshot: result! } as any} 
           onClose={() => setIsDocumentViewOpen(false)} 
        />
      )}
      
      {/* If document view is open but no artifact is formally saved, we mock an artifact on the fly */}
      {isDocumentViewOpen && !activeArtifactId && result && (
        <ProgramDocumentView
           artifact={{
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
             mode: request.mode as any,
             coach_notes: '',
             internal_notes: '',
             request_snapshot: request,
             result_snapshot: result
           }}
           onClose={() => setIsDocumentViewOpen(false)}
        />
      )}

      {/* Render Saved Programs Drawer */}
      <SavedProgramsDrawer 
         isOpen={isDrawerOpen} 
         onClose={() => setIsDrawerOpen(false)} 
         savedPrograms={savedPrograms}
         onSelectProgram={handleSelectSavedProgram}
         activeId={activeArtifactId}
      />

      {isUATOpen && (
        <UATRunner 
          onClose={() => setIsUATOpen(false)} 
          onLoadScenario={handleLoadUATScenario}
        />
      )}
    </div>
  );
}
