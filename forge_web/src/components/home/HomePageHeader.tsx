import React from 'react';
import { SavedProgramArtifact } from '../../types/ui';

interface HomePageHeaderProps {
  savedPrograms: SavedProgramArtifact[];
  favoritesLength: number;
  allExercisesLength: number;
}

export function HomePageHeader({ savedPrograms, favoritesLength, allExercisesLength }: HomePageHeaderProps) {
  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Morning';
    if (hour < 17) return 'Afternoon';
    return 'Evening';
  };

  return (
    <div className="bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-700 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
          <div>
            <h1 className="text-3xl sm:text-4xl font-bold mb-2">
              Good {getGreeting()}, Coach
            </h1>
            <p className="text-indigo-100 text-lg">
              Ready to build something great today?
            </p>
          </div>
          
          {/* Quick Stats */}
          <div className="flex gap-4 sm:gap-6">
            <div className="bg-white/10 backdrop-blur-sm rounded-xl px-4 py-3 text-center">
              <div className="text-2xl font-bold">{savedPrograms.length}</div>
              <div className="text-xs text-indigo-200">Programs</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-xl px-4 py-3 text-center">
              <div className="text-2xl font-bold">{favoritesLength}</div>
              <div className="text-xs text-indigo-200">Favorites</div>
            </div>
            <div className="bg-white/10 backdrop-blur-sm rounded-xl px-4 py-3 text-center">
              <div className="text-2xl font-bold">{allExercisesLength}</div>
              <div className="text-xs text-indigo-200">Exercises</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
