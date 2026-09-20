import React, { useState, useMemo } from 'react';
import { X, Calendar, User, Target, ChevronRight, Activity, ShieldCheck, Trash2, Search, SortAsc, ArrowUpDown, Filter } from 'lucide-react';
import { SavedProgramArtifact } from '../../types/ui';

interface SavedProgramsDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  savedPrograms: SavedProgramArtifact[];
  onSelectProgram: (id: string) => void;
  onDelete?: (id: string) => void;
  activeId: string | null;
  adaptMode?: boolean;
}

type SortKey = 'updated_desc' | 'updated_asc' | 'name_asc';

export function SavedProgramsDrawer({
  isOpen,
  onClose,
  savedPrograms,
  onSelectProgram,
  onDelete,
  activeId,
  adaptMode = false,
}: SavedProgramsDrawerProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [sportFilter, setSportFilter] = useState<string>('all');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [sortKey, setSortKey] = useState<SortKey>('updated_desc');

  const sports = useMemo(() => {
    const s = new Set(savedPrograms.map(p => p.sport).filter(Boolean));
    return Array.from(s).sort();
  }, [savedPrograms]);

  const filtered = useMemo(() => {
    let list = [...savedPrograms];

    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      list = list.filter(p => p.athlete_display_name.toLowerCase().includes(q));
    }

    if (sportFilter !== 'all') {
      list = list.filter(p => p.sport === sportFilter);
    }

    if (statusFilter !== 'all') {
      list = list.filter(p => p.status === statusFilter);
    }

    list.sort((a, b) => {
      if (sortKey === 'updated_desc') return new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime();
      if (sortKey === 'updated_asc') return new Date(a.updated_at).getTime() - new Date(b.updated_at).getTime();
      return a.athlete_display_name.localeCompare(b.athlete_display_name);
    });

    return list;
  }, [savedPrograms, searchQuery, sportFilter, statusFilter, sortKey]);

  if (!isOpen) return null;

  return (
    <>
      <div className="fixed inset-0 bg-slate-900/20 backdrop-blur-sm z-40" onClick={onClose}></div>
      <div className="fixed top-0 bottom-0 left-0 w-[420px] bg-white shadow-2xl z-50 flex flex-col transform transition-transform border-r border-slate-200">
        <div className="flex items-center justify-between p-4 border-b border-slate-100">
          <div>
            <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
               <Calendar className="w-5 h-5 text-indigo-600" />
               {adaptMode ? 'Select Program to Adapt' : 'Saved Programs'}
               <span className="text-sm font-normal text-slate-400 ml-1">({savedPrograms.length})</span>
            </h2>
            {adaptMode && <p className="text-xs text-slate-500 mt-0.5">Choose a saved program as the starting point for a new program</p>}
          </div>
          <button onClick={onClose} className="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-100 rounded-full transition-colors">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Search + Filters */}
        <div className="p-4 border-b border-slate-100 space-y-2 bg-white">
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              placeholder="Search by athlete name..."
              className="w-full pl-9 pr-3 py-2 text-sm bg-slate-50 border border-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-300"
            />
          </div>
          <div className="flex gap-2">
            <div className="flex-1 relative">
              <Filter className="w-3 h-3 absolute left-2 top-1/2 -translate-y-1/2 text-slate-400" />
              <select
                value={sportFilter}
                onChange={e => setSportFilter(e.target.value)}
                className="w-full pl-7 pr-2 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500/20 appearance-none"
              >
                <option value="all">All Sports</option>
                {sports.map(s => <option key={s} value={s}>{s}</option>)}
              </select>
            </div>
            <div className="flex-1">
              <select
                value={statusFilter}
                onChange={e => setStatusFilter(e.target.value)}
                className="w-full px-2 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500/20 appearance-none"
              >
                <option value="all">All Status</option>
                <option value="draft">Draft</option>
                <option value="reviewed">Reviewed</option>
                <option value="approved">Approved</option>
                <option value="archive">Archive</option>
              </select>
            </div>
            <div className="flex-none">
              <select
                value={sortKey}
                onChange={e => setSortKey(e.target.value as SortKey)}
                className="px-2 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500/20 appearance-none"
                title="Sort order"
              >
                <option value="updated_desc">Newest</option>
                <option value="updated_asc">Oldest</option>
                <option value="name_asc">A-Z</option>
              </select>
            </div>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-slate-50">
          {filtered.length === 0 ? (
            <div className="text-center text-slate-500 py-12 text-sm italic">
              {savedPrograms.length === 0
                ? 'No programs saved yet. Generate and save a draft.'
                : 'No programs match the current filters.'}
            </div>
          ) : (
            filtered.map(prog => (
              <div 
                key={prog.id}
                className={`bg-white border rounded-xl p-4 cursor-pointer hover:border-indigo-300 transition-all shadow-sm group ${activeId === prog.id ? 'border-indigo-500 ring-1 ring-indigo-500' : 'border-slate-200'}`}
                onClick={() => onSelectProgram(prog.id)}
              >
                <div className="flex justify-between items-start mb-2">
                   <div className="font-bold text-slate-900">{prog.athlete_display_name}</div>
                   <div className="flex items-center gap-1">
                     <div className={`text-[10px] font-bold uppercase tracking-wide px-2 py-0.5 rounded ${
                        prog.status === 'reviewed' ? 'bg-emerald-100 text-emerald-700' : 
                        prog.status === 'approved' ? 'bg-blue-100 text-blue-700' :
                        'bg-amber-100 text-amber-700'
                     }`}>
                        {prog.status}
                     </div>
                     {onDelete && (
                       <button
                         onClick={(e) => { e.stopPropagation(); onDelete(prog.id); }}
                         className="opacity-0 group-hover:opacity-100 p-1 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded transition-all"
                         title="Delete program"
                       >
                         <Trash2 className="w-3.5 h-3.5" />
                       </button>
                     )}
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
                      <span className="truncate">{prog.sport}{prog.role && prog.role !== '-' ? ` - ${prog.role}` : ''}</span>
                   </div>
                   <div className="flex items-center text-slate-500">
                      <ShieldCheck className="w-3.5 h-3.5 mr-1.5 shrink-0" />
                      <span>{prog.mode === 'premium' ? 'Premium' : 'Core'}</span>
                   </div>
                   <div className="flex items-center text-slate-400">
                      <span>v{prog.version} • <span title={new Date(prog.updated_at).toLocaleString()}>{new Date(prog.updated_at).toLocaleDateString()}</span></span>
                   </div>
                   {prog.week_label && prog.week_label !== '-' && (
                     <div className="flex items-center text-slate-400 col-span-2 pt-1 border-t border-slate-50">
                       <Calendar className="w-3 h-3 mr-1.5 shrink-0" />
                       <span>{prog.week_label}</span>
                     </div>
                   )}
                </div>

                {(prog.coach_overrides?.sessions && Object.keys(prog.coach_overrides.sessions).length > 0) && (
                  <div className="mt-2 pt-2 border-t border-amber-100">
                    <span className="text-[10px] text-amber-600 font-bold uppercase tracking-wider">Has coach overrides</span>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </>
  );
}
