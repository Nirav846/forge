import React from 'react';
import { X, Calendar, User, Target, ChevronRight, Activity, ShieldCheck } from 'lucide-react';
import { SavedProgramArtifact } from '../../types/ui';

interface SavedProgramsDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  savedPrograms: SavedProgramArtifact[];
  onSelectProgram: (id: string) => void;
  activeId: string | null;
}

export function SavedProgramsDrawer({
  isOpen,
  onClose,
  savedPrograms,
  onSelectProgram,
  activeId
}: SavedProgramsDrawerProps) {
  if (!isOpen) return null;

  return (
    <>
      <div className="fixed inset-0 bg-slate-900/20 backdrop-blur-sm z-40" onClick={onClose}></div>
      <div className="fixed top-0 bottom-0 left-0 w-[400px] bg-white shadow-2xl z-50 flex flex-col transform transition-transform border-r border-slate-200">
        <div className="flex items-center justify-between p-4 border-b border-slate-100">
          <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
             <Calendar className="w-5 h-5 text-indigo-600" />
             Saved Programs
          </h2>
          <button onClick={onClose} className="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-full transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>
        
        <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-slate-50">
          {savedPrograms.length === 0 ? (
            <div className="text-center text-slate-500 py-12 text-sm italic">
              No programs saved yet. Generate and save a draft.
            </div>
          ) : (
            savedPrograms.map(prog => (
              <div 
                key={prog.id}
                onClick={() => onSelectProgram(prog.id)}
                className={`bg-white border rounded-xl p-4 cursor-pointer hover:border-indigo-300 transition-all shadow-sm ${activeId === prog.id ? 'border-indigo-500 ring-1 ring-indigo-500' : 'border-slate-200'}`}
              >
                <div className="flex justify-between items-start mb-2">
                   <div className="font-bold text-slate-900">{prog.athlete_display_name}</div>
                   <div className={`text-[10px] font-bold uppercase tracking-wide px-2 py-0.5 rounded ${
                      prog.status === 'reviewed' ? 'bg-emerald-100 text-emerald-700' : 
                      'bg-amber-100 text-amber-700'
                   }`}>
                      {prog.status}
                   </div>
                </div>
                
                <div className="text-sm font-medium text-slate-700 mb-3">{prog.blueprint_label}</div>
                
                <div className="grid grid-cols-2 gap-y-2 gap-x-4 text-xs mt-3 border-t border-slate-100 pt-3">
                   <div className="flex items-center text-slate-500">
                      <Target className="w-3.5 h-3.5 mr-1.5 shrink-0" />
                      <span className="truncate">{prog.goal}</span>
                   </div>
                   <div className="flex items-center text-slate-500">
                      <Activity className="w-3.5 h-3.5 mr-1.5 shrink-0" />
                      <span className="truncate">{prog.sport} - {prog.role}</span>
                   </div>
                   <div className="flex items-center text-slate-500">
                      <ShieldCheck className="w-3.5 h-3.5 mr-1.5 shrink-0" />
                      <span>{prog.mode === 'premium' ? 'Premium (Advanced)' : 'Core Profile'}</span>
                   </div>
                   <div className="flex items-center text-slate-400">
                      <span>v{prog.version} • {new Date(prog.updated_at).toLocaleDateString()}</span>
                   </div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </>
  );
}
