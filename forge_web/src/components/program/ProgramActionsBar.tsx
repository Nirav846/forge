import React from 'react';
import { Save, Copy, FileText, Download, Printer, CheckCircle } from 'lucide-react';
import { ProgramStatus } from '../../types/ui';

interface ProgramActionsBarProps {
  status: ProgramStatus;
  onSaveDraft: () => void;
  onDuplicate: () => void;
  onExportPDF: () => void;
  onExportJSON: () => void;
  onPrintMode: () => void;
  onMarkReviewed: () => void;
}

export function ProgramActionsBar({
  status,
  onSaveDraft,
  onDuplicate,
  onExportPDF,
  onExportJSON,
  onPrintMode,
  onMarkReviewed
}: ProgramActionsBarProps) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-4 bg-white p-3 rounded-xl border border-slate-200 shadow-sm mb-6">
      <div className="flex items-center gap-2">
        <span className="text-xs font-bold uppercase tracking-wider text-slate-500 pl-2">Actions</span>
      </div>
      
      <div className="flex items-center gap-2 overflow-x-auto hide-scrollbar">
        <button 
          onClick={onSaveDraft}
          className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-md transition-colors"
        >
          <Save className="w-4 h-4 text-slate-500" /> Save Draft
        </button>
        <button 
          onClick={onDuplicate}
          className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-md transition-colors"
        >
          <Copy className="w-4 h-4 text-slate-500" /> Duplicate
        </button>
        
        <div className="w-px h-5 bg-slate-200 mx-1"></div>
        
        <button 
          onClick={onExportPDF}
          className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-md transition-colors"
        >
          <Download className="w-4 h-4 text-slate-500" /> PDF
        </button>
        <button 
          onClick={onExportJSON}
          className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-md transition-colors"
        >
          <FileText className="w-4 h-4 text-slate-500" /> JSON
        </button>
        <button 
          onClick={onPrintMode}
          className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 rounded-md transition-colors"
        >
          <Printer className="w-4 h-4 text-slate-500" /> Print
        </button>
        
        <div className="w-px h-5 bg-slate-200 mx-1"></div>

        <button 
          onClick={onMarkReviewed}
          className={`flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
            status === 'reviewed' || status === 'approved' 
              ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' 
              : 'bg-emerald-600 text-white hover:bg-emerald-700'
          }`}
        >
          <CheckCircle className="w-4 h-4" /> 
          {status === 'reviewed' || status === 'approved' ? 'Reviewed' : 'Mark Reviewed'}
        </button>
      </div>
    </div>
  );
}
