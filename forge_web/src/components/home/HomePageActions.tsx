import React from 'react';
import { Trophy, Dumbbell, Activity, ClipboardCheck, Sparkles, ArrowRight } from 'lucide-react';
import { TemplateType } from './HomePage';

interface HomePageActionsProps {
  allExercisesLength: number;
  onStartTeamTemplate: () => void;
  onOpenLibrary: () => void;
  onOpenComplexes?: () => void;
  onOpenWorkout?: () => void;
  setLibraryOpen: (open: boolean) => void;
}

export function HomePageActions({ 
  allExercisesLength, 
  onStartTeamTemplate, 
  onOpenLibrary, 
  onOpenComplexes, 
  onOpenWorkout,
  setLibraryOpen 
}: HomePageActionsProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {/* Team Template */}
      <button
        onClick={onStartTeamTemplate}
        className="flex items-center gap-4 p-5 bg-white border border-slate-200 hover:border-indigo-300 hover:bg-indigo-50/50 rounded-xl transition-all shadow-sm hover:shadow-md group text-left"
      >
        <div className="w-12 h-12 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center shrink-0 group-hover:scale-110 transition-transform shadow-md">
          <Trophy className="w-6 h-6 text-white" />
        </div>
        <div className="flex-1">
          <div className="font-bold text-slate-900 text-lg flex items-center gap-2">
            Team Template
            <Sparkles className="w-4 h-4 text-yellow-500" />
          </div>
          <div className="text-sm text-slate-500">Create team structure, adapt for athletes</div>
        </div>
        <ArrowRight className="w-5 h-5 text-slate-400 group-hover:text-indigo-500 group-hover:translate-x-1 transition-all" />
      </button>

      {/* Exercise Library */}
      <button
        onClick={() => setLibraryOpen(true)}
        className="flex items-center gap-4 p-5 bg-white border border-slate-200 hover:border-emerald-300 hover:bg-emerald-50/50 rounded-xl transition-all shadow-sm hover:shadow-md group text-left"
      >
        <div className="w-12 h-12 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-xl flex items-center justify-center shrink-0 group-hover:scale-110 transition-transform shadow-md">
          <Dumbbell className="w-6 h-6 text-white" />
        </div>
        <div className="flex-1">
          <div className="font-bold text-slate-900 text-lg">Exercise Library</div>
          <div className="text-sm text-slate-500">{allExercisesLength} exercises with full coaching knowledge</div>
        </div>
        <ArrowRight className="w-5 h-5 text-slate-400 group-hover:text-emerald-500 group-hover:translate-x-1 transition-all" />
      </button>

      {/* Complexes Library */}
      <button
        onClick={() => {
          if (onOpenComplexes) onOpenComplexes();
          else setLibraryOpen(true); // Fallback
        }}
        className="flex items-center gap-4 p-5 bg-white border border-slate-200 hover:border-purple-300 hover:bg-purple-50/50 rounded-xl transition-all shadow-sm hover:shadow-md group text-left"
      >
        <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-600 rounded-xl flex items-center justify-center shrink-0 group-hover:scale-110 transition-transform shadow-md">
          <Activity className="w-6 h-6 text-white" />
        </div>
        <div className="flex-1">
          <div className="font-bold text-slate-900 text-lg">Sport Complexes</div>
          <div className="text-sm text-slate-500">210 role-specific multi-exercise sequences</div>
        </div>
        <ArrowRight className="w-5 h-5 text-slate-400 group-hover:text-purple-500 group-hover:translate-x-1 transition-all" />
      </button>

      {/* Workout Builder */}
      <button
        onClick={() => {
          if (onOpenWorkout) onOpenWorkout();
          else setLibraryOpen(true); // Fallback
        }}
        className="flex items-center gap-4 p-5 bg-white border border-slate-200 hover:border-blue-300 hover:bg-blue-50/50 rounded-xl transition-all shadow-sm hover:shadow-md group text-left"
      >
        <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl flex items-center justify-center shrink-0 group-hover:scale-110 transition-transform shadow-md">
          <ClipboardCheck className="w-6 h-6 text-white" />
        </div>
        <div className="flex-1">
          <div className="font-bold text-slate-900 text-lg">Workout Builder</div>
          <div className="text-sm text-slate-500">Create custom training sessions</div>
        </div>
        <ArrowRight className="w-5 h-5 text-slate-400 group-hover:text-blue-500 group-hover:translate-x-1 transition-all" />
      </button>
    </div>
  );
}
