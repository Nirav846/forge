import React, { useState, useEffect } from 'react';
import { X, Search, Trophy, Calendar, Target, Clock } from 'lucide-react';
import { listTeamTemplates } from '../../lib/api';
import { TeamTemplateListItem } from '../../types/ui';

interface TeamLibraryDrawerProps {
  isOpen: boolean;
  onClose: () => void;
  onSelectTemplate: (id: string) => void;
}

export function TeamLibraryDrawer({ isOpen, onClose, onSelectTemplate }: TeamLibraryDrawerProps) {
  const [templates, setTemplates] = useState<TeamTemplateListItem[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!isOpen) return;
    setLoading(true);
    listTeamTemplates()
      .then(data => setTemplates(data.templates || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [isOpen]);

  const filtered = templates.filter(t =>
    !searchQuery.trim() ||
    t.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    t.sport.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex">
      <div className="flex-1 bg-black/30" onClick={onClose} />
      <div className="w-[420px] bg-white shadow-2xl border-l border-slate-200 flex flex-col">
        <div className="flex items-center justify-between px-5 py-4 border-b border-slate-200">
          <div className="flex items-center gap-2">
            <Trophy className="w-5 h-5 text-indigo-600" />
            <h2 className="font-bold text-slate-900">Team Templates</h2>
          </div>
          <button onClick={onClose} className="p-1.5 hover:bg-slate-100 rounded-lg transition-colors">
            <X className="w-5 h-5 text-slate-500" />
          </button>
        </div>

        <div className="px-4 py-3 border-b border-slate-100">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
              placeholder="Search templates..."
              className="w-full pl-9 pr-3 py-2 border border-slate-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-2">
          {loading ? (
            <div className="text-center text-sm text-slate-400 py-8">Loading...</div>
          ) : filtered.length === 0 ? (
            <div className="text-center text-sm text-slate-400 py-8">
              {templates.length === 0 ? 'No team templates yet.' : 'No matching templates.'}
            </div>
          ) : (
            filtered.map(t => (
              <button
                key={t.id}
                onClick={() => { onSelectTemplate(t.id); onClose(); }}
                className="w-full text-left p-4 bg-white border border-slate-200 hover:border-indigo-300 hover:bg-indigo-50/30 rounded-xl transition-all"
              >
                <div className="font-semibold text-slate-900 text-sm">{t.name}</div>
                <div className="text-xs text-slate-500 mt-0.5">
                  {t.sport} &middot; {t.level} &middot; {t.phase.replace('_', ' ')}
                </div>
                <div className="flex items-center gap-4 mt-2 text-xs text-slate-400">
                  <span className="flex items-center gap-1"><Calendar className="w-3 h-3" /> {t.program_length_weeks}w</span>
                  <span className="flex items-center gap-1"><Clock className="w-3 h-3" /> {t.sessions_per_week}/wk</span>
                  <span className="flex items-center gap-1"><Target className="w-3 h-3" /> {t.goal || '—'}</span>
                </div>
              </button>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
