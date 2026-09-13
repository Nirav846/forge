import React, { useState } from 'react';
import { FileEdit, FileText, Users, Plus, ChevronRight, Activity, Trophy, Dumbbell, Sparkles, ArrowRight } from 'lucide-react';
import { SavedProgramArtifact } from '../types/ui';
import { SavedProgramsDrawer } from './program/SavedProgramsDrawer';

export type TemplateType = 'rugby_prop' | 'tennis_singles' | 'cricket_bowler';

interface TemplateInfo {
  id: TemplateType;
  sport: string;
  role: string;
  description: string;
  icon: string;
}

const TEMPLATES: TemplateInfo[] = [
  { id: 'rugby_prop', sport: 'Rugby Union', role: 'Tighthead Prop', description: 'Max Force & Scrum Dominance — collision sport profile', icon: '🏉' },
  { id: 'tennis_singles', sport: 'Tennis', role: 'Singles Player', description: 'Court Speed & Change of Direction — court sport profile', icon: '🎾' },
  { id: 'cricket_bowler', sport: 'Cricket', role: 'Fast Bowler', description: 'Eccentric Tolerance & Delivery Velocity — field sport profile', icon: '🏏' },
];

interface EntryScreenProps {
  onSelectSource: (sourceId: string) => void;
  onSelectTemplate: (template: TemplateType) => void;
  onStartFresh: () => void;
  onStartTeamTemplate: () => void;
  onOpenLibrary: () => void;
  savedPrograms: SavedProgramArtifact[];
}

export function EntryScreen({ onSelectSource, onSelectTemplate, onStartFresh, onStartTeamTemplate, onOpenLibrary, savedPrograms }: EntryScreenProps) {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [templateOpen, setTemplateOpen] = useState(false);

  return (
    <>
      <div className="max-w-3xl mx-auto w-full h-full flex flex-col justify-center items-center text-center px-6 py-12">
        {/* Hero Section */}
        <div className="w-20 h-20 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-2xl flex items-center justify-center mb-6 shadow-lg shadow-indigo-200">
          <FileEdit className="w-10 h-10 text-white" />
        </div>
        <h2 className="text-3xl font-bold text-slate-900 mb-3">Create New Program</h2>
        <p className="text-slate-500 text-base mb-10 max-w-lg leading-relaxed">
          Build structured, periodized training blocks powered by FORGE's intelligent programming engine
        </p>

        <div className="w-full max-w-xl space-y-3">
          {/* Primary: Team Template (new) - Enhanced with gradient */}
          <button
            onClick={onStartTeamTemplate}
            className="w-full flex items-center gap-4 p-5 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 rounded-xl transition-all shadow-md hover:shadow-lg group text-white"
          >
            <div className="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center shrink-0 group-hover:bg-white/30 transition-colors">
              <Trophy className="w-6 h-6 text-white" />
            </div>
            <div className="flex-1 text-left">
              <div className="font-bold text-white text-lg flex items-center gap-2">
                Team Template
                <Sparkles className="w-4 h-4 text-yellow-300" />
              </div>
              <div className="text-sm text-indigo-100">Create a team program structure, then adapt for each athlete</div>
            </div>
            <ArrowRight className="w-5 h-5 text-white/80 group-hover:text-white group-hover:translate-x-1 transition-all" />
          </button>

          {/* Exercise Library Button - Enhanced */}
          <button
            onClick={onOpenLibrary}
            className="w-full flex items-center gap-4 p-5 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 rounded-xl transition-all shadow-md hover:shadow-lg group text-white"
          >
            <div className="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center shrink-0 group-hover:bg-white/30 transition-colors">
              <Dumbbell className="w-6 h-6 text-white" />
            </div>
            <div className="flex-1 text-left">
              <div className="font-bold text-white text-lg">Exercise Library</div>
              <div className="text-sm text-emerald-100">Browse 334+ exercises with coaching cues, faults & alternatives</div>
            </div>
            <ArrowRight className="w-5 h-5 text-white/80 group-hover:text-white group-hover:translate-x-1 transition-all" />
          </button>

          {/* Secondary Options Group */}
          <div className="pt-4 pb-2">
            <div className="flex items-center gap-3 mb-4">
              <div className="flex-1 h-px bg-slate-200"></div>
              <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">Or start with</span>
              <div className="flex-1 h-px bg-slate-200"></div>
            </div>
          </div>

          {/* Adapt Existing */}
          <button
            onClick={() => setDrawerOpen(true)}
            className="w-full flex items-center gap-4 p-4 bg-white border border-slate-200 hover:border-indigo-300 hover:bg-indigo-50/50 rounded-xl transition-all shadow-sm hover:shadow-md group"
          >
            <div className="w-10 h-10 bg-slate-100 rounded-lg flex items-center justify-center shrink-0 group-hover:bg-indigo-100 transition-colors">
              <FileText className="w-5 h-5 text-slate-600 group-hover:text-indigo-600 transition-colors" />
            </div>
            <div className="flex-1 text-left">
              <div className="font-semibold text-slate-900 group-hover:text-indigo-900">Adapt Existing Program</div>
              <div className="text-sm text-slate-500 group-hover:text-slate-600">Start from a saved program as your template</div>
            </div>
            <ChevronRight className="w-5 h-5 text-slate-400 group-hover:text-indigo-500 transition-colors" />
          </button>

          {/* Role Template */}
          <button
            onClick={() => setTemplateOpen(!templateOpen)}
            className="w-full flex items-center gap-4 p-4 bg-white border border-slate-200 hover:border-indigo-300 hover:bg-indigo-50/50 rounded-xl transition-all shadow-sm hover:shadow-md group"
          >
            <div className="w-10 h-10 bg-slate-100 rounded-lg flex items-center justify-center shrink-0 group-hover:bg-indigo-100 transition-colors">
              <Users className="w-5 h-5 text-slate-600 group-hover:text-indigo-600 transition-colors" />
            </div>
            <div className="flex-1 text-left">
              <div className="font-semibold text-slate-900 group-hover:text-indigo-900">Start from Role Template</div>
              <div className="text-sm text-slate-500 group-hover:text-slate-600">Pick a sport and role to auto-fill defaults</div>
            </div>
            <ChevronRight className={`w-5 h-5 text-slate-400 group-hover:text-indigo-500 transition-transform ${templateOpen ? 'rotate-90' : ''}`} />
          </button>

          {templateOpen && (
            <div className="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm divide-y divide-slate-100 animate-in slide-in-from-top-2 duration-200">
              {TEMPLATES.map(t => (
                <button
                  key={t.id}
                  onClick={() => onSelectTemplate(t.id)}
                  className="w-full flex items-center gap-3 p-4 text-left hover:bg-slate-50 transition-colors group"
                >
                  <div className="text-2xl shrink-0">{t.icon}</div>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-semibold text-slate-900 flex items-center gap-2">
                      <span>{t.sport}</span>
                      <span className="text-slate-400 font-normal">—</span>
                      <span className="font-normal text-slate-700">{t.role}</span>
                    </div>
                    <p className="text-xs text-slate-500 mt-0.5 truncate">{t.description}</p>
                  </div>
                  <ChevronRight className="w-4 h-4 text-slate-300 group-hover:text-indigo-500 shrink-0" />
                </button>
              ))}
            </div>
          )}

          {/* Start Fresh - Minimal link style */}
          <div className="pt-4">
            <button
              onClick={onStartFresh}
              className="text-sm text-slate-500 hover:text-indigo-600 transition-colors flex items-center justify-center gap-1.5 mx-auto group"
            >
              <Plus className="w-3.5 h-3.5 group-hover:scale-110 transition-transform" />
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
