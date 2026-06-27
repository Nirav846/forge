import React, { useState, useEffect } from 'react';
import { ProgramViewModel, ProgramStatus } from '../../types/ui';
import { Save, Copy, FileText, Download, Printer, CheckCircle, GitCompare, Library, Clock, StickyNote, ChevronDown, Loader2, AlertCircle } from 'lucide-react';
import { SaveIndicator, SaveState } from '../SaveIndicator';

interface ProgramWorkspaceHeaderProps {
  viewModel: ProgramViewModel;
  requestName: string;
  status: ProgramStatus;
  onSaveDraft: () => void;
  onDuplicate: () => void;
  onExportPDF: () => void;
  onExportJSON: () => void;
  onPrintMode: () => void;
  onMarkReviewed: () => void;
  onCompare: () => void;
  onUpdateNotes?: (notes: string, field: 'coach_notes' | 'internal_notes') => Promise<boolean> | void;
  coachNotes?: string;
  internalNotes?: string;
  reviewSaveState?: SaveState;
  notesSaveState?: SaveState;
}

export function ProgramWorkspaceHeader({
  viewModel,
  requestName,
  status,
  onSaveDraft,
  onDuplicate,
  onExportPDF,
  onExportJSON,
  onPrintMode,
  onMarkReviewed,
  onCompare,
  onUpdateNotes,
  coachNotes = '',
  internalNotes = '',
  reviewSaveState: parentReviewSave = 'idle',
  notesSaveState: parentNotesSave = 'idle',
}: ProgramWorkspaceHeaderProps) {
  const [notesOpen, setNotesOpen] = useState(false);
  const [localCoachNotes, setLocalCoachNotes] = useState(coachNotes);
  const [localInternalNotes, setLocalInternalNotes] = useState(internalNotes);
  const [localCoachSave, setLocalCoachSave] = useState<SaveState>('idle');
  const [localInternalSave, setLocalInternalSave] = useState<SaveState>('idle');

  useEffect(() => { setLocalCoachNotes(coachNotes); }, [coachNotes]);
  useEffect(() => { setLocalInternalNotes(internalNotes); }, [internalNotes]);

  const handleSaveCoachNotes = async () => {
    if (localCoachNotes === coachNotes || !onUpdateNotes) return;
    setLocalCoachSave('saving');
    try {
      const result = onUpdateNotes(localCoachNotes, 'coach_notes');
      if (result instanceof Promise) await result;
      setLocalCoachSave('saved');
      setTimeout(() => setLocalCoachSave('idle'), 2000);
    } catch {
      setLocalCoachSave('error');
      setTimeout(() => setLocalCoachSave('idle'), 4000);
    }
  };

  const handleSaveInternalNotes = async () => {
    if (localInternalNotes === internalNotes || !onUpdateNotes) return;
    setLocalInternalSave('saving');
    try {
      const result = onUpdateNotes(localInternalNotes, 'internal_notes');
      if (result instanceof Promise) await result;
      setLocalInternalSave('saved');
      setTimeout(() => setLocalInternalSave('idle'), 2000);
    } catch {
      setLocalInternalSave('error');
      setTimeout(() => setLocalInternalSave('idle'), 4000);
    }
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm mb-6 overflow-hidden">
      {/* Top Main Command Bar */}
      <div className="px-5 py-4 flex flex-col md:flex-row md:items-start justify-between gap-4 border-b border-slate-100 bg-slate-50">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <h1 className="text-xl font-bold text-slate-900 tracking-tight leading-tight">
              {viewModel.summary.blueprint_selected}
            </h1>
            {status === 'reviewed' ? (
              <span className="flex items-center gap-1 text-emerald-700 bg-emerald-100 px-2.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wide border border-emerald-200">
                <CheckCircle className="w-3 h-3" /> Reviewed
              </span>
            ) : status === 'draft' ? (
               <span className="flex items-center gap-1 text-amber-700 bg-amber-100 px-2.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wide border border-amber-200">
                 Draft
               </span>
            ) : null}
          </div>
          
          <div className="flex flex-wrap items-center text-sm text-slate-500 space-x-2">
            <span className="font-semibold text-slate-800">{requestName || 'Athlete'}</span>
            <span className="text-slate-300">&bull;</span>
            <span>Role: <strong>{viewModel.summary.role_emphasis}</strong></span>
            <span className="text-slate-300">&bull;</span>
            <span className="flex items-center gap-1"><Clock className="w-3.5 h-3.5" /> {new Date(viewModel.metadata.generated_at).toLocaleDateString()}</span>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2">
           <button onClick={onCompare} className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-slate-700 bg-white border border-slate-200 hover:bg-slate-50 rounded-md transition-colors shadow-sm">
             <GitCompare className="w-3.5 h-3.5 text-indigo-500" /> Compare
           </button>
           <button onClick={onSaveDraft} className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-slate-700 bg-white border border-slate-200 hover:bg-slate-50 rounded-md transition-colors shadow-sm">
             <Save className="w-3.5 h-3.5 text-slate-400" /> Save
           </button>
           <button onClick={onDuplicate} className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-slate-700 bg-white border border-slate-200 hover:bg-slate-50 rounded-md transition-colors shadow-sm">
             <Copy className="w-3.5 h-3.5 text-slate-400" /> Duplicate
           </button>
           
           <div className="w-px h-5 bg-slate-200 mx-1"></div>
           
           <button onClick={onPrintMode} className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-slate-700 bg-white border border-slate-200 hover:bg-slate-50 rounded-md transition-colors shadow-sm">
             <Printer className="w-3.5 h-3.5 text-slate-400" /> Print
           </button>
           <button onClick={onExportJSON} className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold text-slate-700 bg-white border border-slate-200 hover:bg-slate-50 rounded-md transition-colors shadow-sm">
             <Download className="w-3.5 h-3.5 text-slate-400" /> JSON
           </button>

           <div className="w-px h-5 bg-slate-200 mx-1"></div>

           <button onClick={onMarkReviewed} className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-bold rounded-md transition-colors shadow-sm ${
                status === 'reviewed' 
                  ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' 
                  : 'bg-emerald-600 text-white hover:bg-emerald-700 border border-transparent'
              }`}
           >
              <CheckCircle className="w-3.5 h-3.5" /> 
              <SaveIndicator state={parentReviewSave} />
              {parentReviewSave === 'idle' && (status === 'reviewed' ? 'Reviewed' : 'Approve')}
           </button>
        </div>
      </div>

      {/* Meta Properties Strip */}
      <div className="grid grid-cols-2 md:grid-cols-4 divide-x divide-slate-100 border-t border-slate-100">
         <div className="p-3 bg-white">
            <div className="text-[10px] uppercase font-bold tracking-wider text-slate-400 mb-0.5">Length</div>
            <div className="text-sm font-semibold text-slate-800">{viewModel.summary.total_weeks} Weeks</div>
         </div>
         <div className="p-3 bg-white">
            <div className="text-[10px] uppercase font-bold tracking-wider text-slate-400 mb-0.5">Frequency</div>
            <div className="text-sm font-semibold text-slate-800">{viewModel.summary.weekly_frequency}x / week</div>
         </div>
         <div className="p-3 bg-white">
            <div className="text-[10px] uppercase font-bold tracking-wider text-slate-400 mb-0.5">Match Proximity</div>
            <div className="text-sm font-semibold text-slate-800">{viewModel.summary.competition_window}</div>
         </div>
         <div className="p-3 bg-white">
            <div className="text-[10px] uppercase font-bold tracking-wider text-slate-400 mb-0.5">Cond Emphasis</div>
            <div className="text-sm font-semibold text-slate-800">{viewModel.summary.conditioning_emphasis}</div>
         </div>
      </div>

      {/* Coach Notes Section */}
      {onUpdateNotes && (
        <div className="border-t border-slate-100">
          <button
            onClick={() => setNotesOpen(!notesOpen)}
            className="flex items-center justify-between w-full px-5 py-2.5 text-xs font-semibold text-slate-500 hover:text-slate-700 hover:bg-slate-50 transition-colors"
          >
            <span className="flex items-center gap-1.5">
              <StickyNote className="w-3.5 h-3.5" /> Coach Notes
              {localCoachNotes && <span className="text-emerald-600 font-normal">({localCoachNotes.length} chars)</span>}
            </span>
            <ChevronDown className={`w-3.5 h-3.5 transition-transform ${notesOpen ? 'rotate-180' : ''}`} />
          </button>
          {notesOpen && (
            <div className="px-5 pb-4 space-y-3">
              <div>
                <div className="flex items-center justify-between mb-1">
                  <label className="text-[10px] uppercase font-bold tracking-wider text-slate-400">Coach Notes</label>
                  <SaveIndicator state={localCoachSave} />
                </div>
                <textarea
                  value={localCoachNotes}
                  onChange={e => setLocalCoachNotes(e.target.value)}
                  onBlur={handleSaveCoachNotes}
                  placeholder="Add coach-facing notes for this program..."
                  className="w-full text-sm border border-slate-200 rounded-md p-2.5 bg-white text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-300 resize-none"
                  rows={2}
                />
                {localCoachSave === 'error' && (
                  <p className="text-xs text-red-600 mt-1 flex items-center gap-1"><AlertCircle className="w-3 h-3" /> Save failed — text preserved</p>
                )}
              </div>
              <div>
                <div className="flex items-center justify-between mb-1">
                  <label className="text-[10px] uppercase font-bold tracking-wider text-slate-400">Internal Notes</label>
                  <SaveIndicator state={localInternalSave} />
                </div>
                <textarea
                  value={localInternalNotes}
                  onChange={e => setLocalInternalNotes(e.target.value)}
                  onBlur={handleSaveInternalNotes}
                  placeholder="Add internal notes..."
                  className="w-full text-sm border border-slate-200 rounded-md p-2.5 bg-white text-slate-800 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-300 resize-none"
                  rows={2}
                />
                {localInternalSave === 'error' && (
                  <p className="text-xs text-red-600 mt-1 flex items-center gap-1"><AlertCircle className="w-3 h-3" /> Save failed — text preserved</p>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
