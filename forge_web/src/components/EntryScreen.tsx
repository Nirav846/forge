import React, { useState } from 'react';
import { FileEdit, FileText, Users, Plus, ChevronRight, Activity, Trophy } from 'lucide-react';
import { SavedProgramArtifact } from '../types/ui';
import { SavedProgramsDrawer } from './program/SavedProgramsDrawer';

export type TemplateType = 'rugby_prop' | 'tennis_singles' | 'cricket_bowler';

interface TemplateInfo {
  id: TemplateType;
  sport: string;
  role: string;
  description: string;
}

const TEMPLATES: TemplateInfo[] = [
  { id: 'rugby_prop', sport: 'Rugby Union', role: 'Tighthead Prop', description: 'Max Force & Scrum Dominance — collision sport profile' },
  { id: 'tennis_singles', sport: 'Tennis', role: 'Singles Player', description: 'Court Speed & Change of Direction — court sport profile' },
  { id: 'cricket_bowler', sport: 'Cricket', role: 'Fast Bowler', description: 'Eccentric Tolerance & Delivery Velocity — field sport profile' },
];

interface EntryScreenProps {
  onSelectSource: (sourceId: string) => void;
  onSelectTemplate: (template: TemplateType) => void;
  onStartFresh: () => void;
  onStartTeamTemplate: () => void;
  savedPrograms: SavedProgramArtifact[];
}

export function EntryScreen({ onSelectSource, onSelectTemplate, onStartFresh, onStartTeamTemplate, savedPrograms }: EntryScreenProps) {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [templateOpen, setTemplateOpen] = useState(false);

  return (
    <>
      <div className="max-w-2xl mx-auto w-full h-full flex flex-col justify-center items-center text-center px-6">
        <div className="w-16 h-16 bg-indigo-50 rounded-2xl flex items-center justify-center mb-6 border border-indigo-100">
          <FileEdit className="w-8 h-8 text-indigo-600" />
        </div>
        <h2 className="text-2xl font-bold text-slate-900 mb-2">Create New Program</h2>
        <p className="text-slate-500 text-sm mb-10 max-w-md">
          Choose how you'd like to start building a structured training block
        </p>

        <div className="w-full max-w-lg space-y-3">
          {/* Primary: Team Template (new) */}
          <button
            onClick={onStartTeamTemplate}
            className="w-full flex items-center gap-4 p-5 bg-white border-2 border-indigo-400 hover:border-indigo-500 hover:bg-indigo-50 rounded-xl transition-all shadow-sm group"
          >
            <div className="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center shrink-0 group-hover:bg-indigo-200 transition-colors">
              <Trophy className="w-6 h-6 text-indigo-700" />
            </div>
            <div className="flex-1 text-left">
              <div className="font-bold text-slate-900 text-lg">Team Template</div>
              <div className="text-sm text-slate-500">Create a team program structure, then adapt for each athlete</div>
            </div>
            <ChevronRight className="w-5 h-5 text-indigo-400 group-hover:text-indigo-500 transition-colors" />
          </button>

          {/* Secondary: Adapt Existing */}
          <button
            onClick={() => setDrawerOpen(true)}
            className="w-full flex items-center gap-4 p-4 bg-white border border-slate-200 hover:border-slate-300 hover:bg-slate-50 rounded-xl transition-all shadow-sm group"
          >
            <div className="w-10 h-10 bg-slate-100 rounded-lg flex items-center justify-center shrink-0 group-hover:bg-slate-200 transition-colors">
              <FileText className="w-5 h-5 text-slate-600" />
            </div>
            <div className="flex-1 text-left">
              <div className="font-semibold text-slate-900">Adapt Existing Program</div>
              <div className="text-sm text-slate-500">Start from a saved program as your template</div>
            </div>
            <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-slate-500 transition-colors" />
          </button>

          {/* Secondary: Start from Role Template */}
          <button
            onClick={() => setTemplateOpen(!templateOpen)}
            className="w-full flex items-center gap-4 p-4 bg-white border border-slate-200 hover:border-slate-300 hover:bg-slate-50 rounded-xl transition-all shadow-sm group"
          >
            <div className="w-10 h-10 bg-slate-100 rounded-lg flex items-center justify-center shrink-0 group-hover:bg-slate-200 transition-colors">
              <Users className="w-5 h-5 text-slate-600" />
            </div>
            <div className="flex-1 text-left">
              <div className="font-semibold text-slate-900">Start from Role Template</div>
              <div className="text-sm text-slate-500">Pick a sport and role to auto-fill defaults</div>
            </div>
            <ChevronRight className={`w-4 h-4 text-slate-400 transition-transform ${templateOpen ? 'rotate-90' : ''}`} />
          </button>

          {templateOpen && (
            <div className="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm divide-y divide-slate-100">
              {TEMPLATES.map(t => (
                <button
                  key={t.id}
                  onClick={() => onSelectTemplate(t.id)}
                  className="w-full flex items-center gap-3 p-4 text-left hover:bg-slate-50 transition-colors group"
                >
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-semibold text-slate-900 flex items-center gap-2">
                      <Activity className="w-3.5 h-3.5 text-indigo-500 shrink-0" />
                      <span>{t.sport}</span>
                      <span className="text-slate-400 font-normal">—</span>
                      <span className="font-normal text-slate-700">{t.role}</span>
                    </div>
                    <p className="text-xs text-slate-500 mt-0.5 truncate">{t.description}</p>
                  </div>
                  <ChevronRight className="w-4 h-4 text-slate-300 group-hover:text-slate-500 shrink-0" />
                </button>
              ))}
            </div>
          )}

          {/* Tertiary: Start Fresh */}
          <div className="pt-4">
            <button
              onClick={onStartFresh}
              className="text-sm text-slate-500 hover:text-slate-800 transition-colors flex items-center justify-center gap-1.5 mx-auto"
            >
              <Plus className="w-3.5 h-3.5" />
              Start Fresh — build from scratch
            </button>
          </div>
        </div>
      </div>

      <SavedProgramsDrawer
        isOpen={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        savedPrograms={savedPrograms}
        onSelectProgram={(id) => { onSelectSource(id); setDrawerOpen(false); }}
        activeId={null}
        adaptMode
      />
    </>
  );
}
