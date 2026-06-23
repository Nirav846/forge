import React, { useState } from 'react';
import { AppStatus } from '../App';
import { Target, Calendar, Clock, Activity, AlertCircle, Dumbbell, ShieldAlert, CheckCircle, FileText, Layers, Eye, GitCompare } from 'lucide-react';
import { TransformationResult, ProgramStatus, SavedProgramArtifact } from '../types/ui';
import { ProgramWorkspaceHeader } from './program/ProgramWorkspaceHeader';
import { CoachSummaryMode } from './program/modes/CoachSummaryMode';
import { ProgramBuilderMode } from './program/modes/ProgramBuilderMode';
import { AthleteDeliveryMode } from './program/modes/AthleteDeliveryMode';
import { CompareMode } from './program/modes/CompareMode';

interface CenterPanelProps {
  result: TransformationResult | null;
  status: AppStatus;
  errorMessage: string | null;
  requestName: string;
  artifactStatus: ProgramStatus;
  savedPrograms: SavedProgramArtifact[];
  onSaveDraft: () => void;
  onMarkReviewed: () => void;
  onOpenDocument: () => void;
  onDuplicate: () => void;
  onUpdateNotes?: (notes: string, field: 'coach_notes' | 'internal_notes') => void;
  coachNotes?: string;
  internalNotes?: string;
}

export type ReviewMode = 'summary' | 'builder' | 'athlete' | 'compare';

export default function CenterPanel({ 
  result, 
  status, 
  errorMessage, 
  requestName,
  artifactStatus,
  savedPrograms,
  onSaveDraft,
  onMarkReviewed,
  onOpenDocument,
  onDuplicate,
  onUpdateNotes,
  coachNotes = '',
  internalNotes = '',
}: CenterPanelProps) {

  
  const [viewMode, setViewMode] = useState<ReviewMode>('builder');

  if (status === 'loading') {
    return (
      <div className="max-w-4xl mx-auto w-full h-full flex flex-col pt-12 items-center">
         <div className="w-16 h-16 border-4 border-slate-200 border-t-indigo-600 rounded-full animate-spin mb-6"></div>
         <h2 className="text-xl font-semibold text-slate-800">Compiling Blueprint...</h2>
         <p className="text-slate-500 text-sm mt-2">Connecting to FORGE engine & applying advanced heuristics.</p>
         
         <div className="w-full mt-12 space-y-4">
            <div className="h-32 bg-slate-200/50 rounded-xl w-full animate-pulse"></div>
            <div className="grid grid-cols-3 gap-4">
               <div className="h-24 bg-slate-200/50 rounded-xl animate-pulse delay-75"></div>
               <div className="h-24 bg-slate-200/50 rounded-xl animate-pulse delay-150"></div>
               <div className="h-24 bg-slate-200/50 rounded-xl animate-pulse delay-200"></div>
            </div>
            <div className="h-64 bg-slate-200/50 rounded-xl w-full animate-pulse delay-300 mt-8"></div>
         </div>
      </div>
    );
  }

  if (status === 'error') {
     return (
        <div className="max-w-3xl mx-auto w-full h-full flex flex-col pt-24 items-center text-center">
           <div className="w-20 h-20 bg-red-50 rounded-2xl flex items-center justify-center mb-6 border border-red-100">
              <ShieldAlert className="w-10 h-10 text-red-500" />
           </div>
           <h2 className="text-2xl font-bold text-slate-900 mb-2">Engine Communication Failed</h2>
           <p className="text-slate-500 text-sm mb-6 max-w-lg">
             The FORGE frontend shell could not safely negotiate a response from the backend. Verify payload structure in Right Panel.
           </p>
           <div className="bg-red-50 text-red-800 p-4 rounded-lg text-sm border border-red-200 break-words w-full text-left font-mono">
              {errorMessage || 'Unknown Network Error'}
           </div>
        </div>
     );
  }

  if (status === 'idle' || !result || !result.viewModel) {
    return (
      <div className="max-w-4xl mx-auto w-full h-full flex flex-col justify-center items-center text-center">
        <div className="w-20 h-20 bg-slate-100 rounded-2xl flex items-center justify-center mb-6 border border-slate-200">
           <Dumbbell className="w-10 h-10 text-slate-400" />
        </div>
        <h2 className="text-2xl font-bold text-slate-900 mb-2">FORGE Output Console</h2>
        <p className="text-slate-500 max-w-md text-sm">
          Enter {requestName ? <strong>{requestName}'s</strong> : 'athlete'} parameters in the left panel and click generate to compute a structured programming block.
        </p>
      </div>
    );
  }

  const response = result.viewModel;

  const handleExportJSON = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(result.rawPayload, null, 2));
    const dlAnchorElem = document.createElement('a');
    dlAnchorElem.setAttribute("href",     dataStr     );
    dlAnchorElem.setAttribute("download", `forge_program_${requestName || 'athlete'}.json`);
    dlAnchorElem.click();
  };

  return (
    <div className="max-w-5xl mx-auto w-full pb-12">
      
      {viewMode !== 'athlete' && (
        <ProgramWorkspaceHeader 
          viewModel={response}
          requestName={requestName}
          status={artifactStatus}
          onSaveDraft={onSaveDraft}
          onDuplicate={onDuplicate}
          onExportPDF={onOpenDocument}
          onExportJSON={handleExportJSON}
          onPrintMode={onOpenDocument}
          onMarkReviewed={onMarkReviewed}
          onCompare={() => setViewMode('compare')}
          onUpdateNotes={onUpdateNotes}
          coachNotes={coachNotes}
          internalNotes={internalNotes}
        />
      )}

      {/* Mode Navigation (Only in coach views) */}
      {viewMode !== 'athlete' && (
        <div className="flex items-center gap-2 mb-6 border-b border-slate-200 pb-px">
          <button 
            onClick={() => setViewMode('summary')}
            className={`py-2 px-4 text-sm font-bold transition-all flex items-center gap-2 border-b-2 ${viewMode === 'summary' ? 'border-indigo-600 text-indigo-700' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
          >
            <FileText className="w-4 h-4" /> Coach Summary
          </button>
          <button 
            onClick={() => setViewMode('builder')}
            className={`py-2 px-4 text-sm font-bold transition-all flex items-center gap-2 border-b-2 ${viewMode === 'builder' ? 'border-indigo-600 text-indigo-700' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
          >
            <Layers className="w-4 h-4" /> Block Builder
          </button>
          <button 
            onClick={() => setViewMode('compare')}
            className={`py-2 px-4 text-sm font-bold transition-all flex items-center gap-2 border-b-2 ${viewMode === 'compare' ? 'border-indigo-600 text-indigo-700' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
          >
            <GitCompare className="w-4 h-4" /> Compare
          </button>
          <div className="flex-1"></div>
          <button 
            onClick={() => setViewMode('athlete')}
            className={`py-1.5 px-3 mb-1 text-xs font-semibold rounded-md transition-all flex items-center gap-1.5 bg-slate-100 text-slate-600 hover:bg-slate-200`}
          >
            <Eye className="w-3.5 h-3.5" /> Athlete View
          </button>
        </div>
      )}

      {viewMode === 'summary' && <CoachSummaryMode viewModel={response} />}
      {viewMode === 'builder' && <ProgramBuilderMode viewModel={response} />}
      {viewMode === 'athlete' && (
         <div className="space-y-4">
            <button 
               onClick={() => setViewMode('builder')}
               className="print:hidden text-sm font-semibold text-indigo-600 flex items-center hover:underline"
            >
               &larr; Back to Coach Interface
            </button>
            <AthleteDeliveryMode viewModel={response} requestName={requestName} />
         </div>
      )}
      {viewMode === 'compare' && <CompareMode currentResult={result!} savedPrograms={savedPrograms} />}

    </div>
  );
}
