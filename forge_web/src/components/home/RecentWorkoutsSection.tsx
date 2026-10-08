import React from 'react';
import { Star, Clock, Calendar, ChevronRight } from 'lucide-react';
import { SavedProgramArtifact } from '../../types/ui';

interface FavoriteExercise {
  id: string;
  name: string;
  category: string;
}

interface RecentWorkout {
  id: string;
  name: string;
  date: string;
  athlete: string;
  sport: string;
}

interface FavoriteExercisesSectionProps {
  favorites: FavoriteExercise[];
  onFavoriteClick: (exercise: FavoriteExercise) => void;
  onOpenLibrary: () => void;
}

interface RecentWorkoutsSectionProps {
  recentWorkouts: RecentWorkout[];
  onRecentClick: (workout: RecentWorkout) => void;
  onDrawerOpen: () => void;
  onStartTeamTemplate: () => void;
}

export function FavoriteExercisesSection({ 
  favorites, 
  onFavoriteClick, 
  onOpenLibrary 
}: FavoriteExercisesSectionProps) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
      <div className="p-4 border-b border-slate-100 flex items-center justify-between">
        <h3 className="font-bold text-slate-900 flex items-center gap-2">
          <Star className="w-5 h-5 text-yellow-500 fill-yellow-500" />
          Quick Access Favorites
        </h3>
        <button
          onClick={onOpenLibrary}
          className="text-xs text-indigo-600 hover:text-indigo-700 font-medium"
        >
          Manage →
        </button>
      </div>
      <div className="p-4">
        {favorites.length > 0 ? (
          <div className="grid grid-cols-2 gap-3">
            {favorites.map(ex => (
              <button
                key={ex.id}
                onClick={() => onFavoriteClick(ex)}
                className="group p-3 bg-slate-50 hover:bg-indigo-50 border border-slate-200 hover:border-indigo-300 rounded-lg text-left transition-all hover:shadow-sm"
              >
                <div className="font-medium text-sm text-slate-900 group-hover:text-indigo-900 truncate">
                  {ex.name}
                </div>
                <div className="text-xs text-slate-500 group-hover:text-slate-600 mt-1">
                  {ex.category}
                </div>
              </button>
            ))}
          </div>
        ) : (
          <div className="text-center py-8">
            <Star className="w-8 h-8 text-slate-300 mx-auto mb-2" />
            <p className="text-sm text-slate-500 mb-3">No favorites yet</p>
            <button
              onClick={onOpenLibrary}
              className="text-sm text-indigo-600 hover:text-indigo-700 font-medium"
            >
              Browse exercises to add favorites →
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export function RecentWorkoutsSection({ 
  recentWorkouts, 
  onRecentClick, 
  onDrawerOpen,
  onStartTeamTemplate 
}: RecentWorkoutsSectionProps) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
      <div className="p-4 border-b border-slate-100 flex items-center justify-between">
        <h3 className="font-bold text-slate-900 flex items-center gap-2">
          <Clock className="w-5 h-5 text-blue-500" />
          Recent Programs
        </h3>
        <button
          onClick={onDrawerOpen}
          className="text-xs text-indigo-600 hover:text-indigo-700 font-medium"
        >
          View All →
        </button>
      </div>
      <div className="divide-y divide-slate-100">
        {recentWorkouts.length > 0 ? (
          recentWorkouts.map(workout => (
            <button
              key={workout.id}
              onClick={() => onRecentClick(workout)}
              className="w-full p-4 hover:bg-slate-50 transition-colors text-left group"
            >
              <div className="flex items-center justify-between">
                <div className="flex-1 min-w-0">
                  <div className="font-medium text-sm text-slate-900 group-hover:text-indigo-900 truncate">
                    {workout.name}
                  </div>
                  <div className="text-xs text-slate-500 mt-1 flex items-center gap-2">
                    <span>{workout.sport}</span>
                    <span className="w-1 h-1 bg-slate-300 rounded-full"></span>
                    <span>{workout.date}</span>
                  </div>
                </div>
                <ChevronRight className="w-4 h-4 text-slate-300 group-hover:text-indigo-500 transition-colors" />
              </div>
            </button>
          ))
        ) : (
          <div className="text-center py-8">
            <Calendar className="w-8 h-8 text-slate-300 mx-auto mb-2" />
            <p className="text-sm text-slate-500 mb-3">No programs yet</p>
            <button
              onClick={onStartTeamTemplate}
              className="text-sm text-indigo-600 hover:text-indigo-700 font-medium"
            >
              Create your first program →
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
