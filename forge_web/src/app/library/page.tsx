'use client';

import React, { useState, useEffect } from 'react';
import { Exercise, ExerciseFilters, exerciseService } from '@/modules/exercises/exercise.service';
import { 
  EXERCISE_CATEGORIES, 
  DIFFICULTY_LEVELS, 
  FORCE_VECTORS, 
  SOURCE_ORGANIZATIONS, 
  getDifficultyColor, 
  getCategoryIcon 
} from '@/modules/exercises/exerciseService';

export default function ExerciseLibraryPage() {
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedExercise, setSelectedExercise] = useState<Exercise | null>(null);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [favorites, setFavorites] = useState<Set<string>>(new Set());
  const [showFavoritesOnly, setShowFavoritesOnly] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [filterOptions, setFilterOptions] = useState<{
    categories: string[];
    movementPatterns: string[];
    equipment: string[];
    difficulties: string[];
    sources: string[];
  } | null>(null);
  
  const [filters, setFilters] = useState<ExerciseFilters>({
    search_query: '',
    category: undefined,
    difficulty_level: undefined,
    force_vector: undefined,
    equipment: undefined,
    movement_pattern: undefined,
    has_coaching_cues: undefined
  });

  // Load favorites from localStorage
  useEffect(() => {
    const savedFavorites = localStorage.getItem('forge_favorites');
    if (savedFavorites) {
      setFavorites(new Set(JSON.parse(savedFavorites)));
    }
  }, []);

  // Load filter options
  useEffect(() => {
    async function loadFilterOptions() {
      try {
        const options = await exerciseService.getFilterOptions();
        setFilterOptions(options);
      } catch (err) {
        console.error('Failed to load filter options:', err);
      }
    }
    loadFilterOptions();
  }, []);

  // Save favorites to localStorage
  useEffect(() => {
    localStorage.setItem('forge_favorites', JSON.stringify(Array.from(favorites)));
  }, [favorites]);

  useEffect(() => {
    loadExercises();
  }, [filters, showFavoritesOnly]);

  async function loadExercises() {
    setLoading(true);
    setError(null);
    try {
      const data = await exerciseService.getExercises(filters);
      // Filter by favorites if needed
      const filtered = showFavoritesOnly 
        ? data.filter(ex => favorites.has(String(ex.id)))
        : data;
      setExercises(filtered);
    } catch (err) {
      setError('Failed to load exercises. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  function updateFilter<K extends keyof ExerciseFilters>(key: K, value: ExerciseFilters[K]) {
    setFilters(prev => ({ ...prev, [key]: value }));
  }

  function clearFilters() {
    setFilters({
      search_query: '',
      category: undefined,
      difficulty_level: undefined,
      force_vector: undefined,
      equipment: undefined,
      movement_pattern: undefined,
      has_coaching_cues: undefined
    });
    setShowFavoritesOnly(false);
  }

  function toggleFavorite(exerciseId: string) {
    setFavorites(prev => {
      const next = new Set(prev);
      if (next.has(exerciseId)) {
        next.delete(exerciseId);
      } else {
        next.add(exerciseId);
      }
      return next;
    });
  }

  function addToWorkout(exercise: Exercise) {
    // Get existing workout plan from localStorage
    const existing = localStorage.getItem('forge_current_workout');
    const workout = existing ? JSON.parse(existing) : [];
    
    // Add exercise if not already present
    if (!workout.find((e: any) => e.id === exercise.id)) {
      workout.push({
        id: exercise.id,
        name: exercise.name,
        sets: 3,
        reps: '8-12',
        notes: ''
      });
      localStorage.setItem('forge_current_workout', JSON.stringify(workout));
      
      // Show toast notification
      alert(`✅ "${exercise.name}" added to workout!`);
    } else {
      alert(`ℹ️ "${exercise.name}" is already in your workout.`);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">📚 FORGE Exercise Library</h1>
                <p className="mt-2 text-gray-600">
                  CSCS-Certified Exercise Database • {exercises.length} Exercises Available{showFavoritesOnly && ' (Favorites Only)'}
                </p>
              </div>
              {/* Mobile Sidebar Toggle */}
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="lg:hidden p-2 text-gray-500 hover:text-gray-700"
              >
                🔍
              </button>
            </div>
            <div className="flex items-center gap-3">
              {/* View Mode Toggle */}
              <div className="flex items-center bg-gray-100 rounded-lg p-1">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${viewMode === 'grid' ? 'bg-white shadow text-blue-600' : 'text-gray-600 hover:text-gray-900'}`}
                >
                  ▦ Grid
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${viewMode === 'list' ? 'bg-white shadow text-blue-600' : 'text-gray-600 hover:text-gray-900'}`}
                >
                  ☰ List
                </button>
              </div>
              {/* Favorites Filter */}
              <button
                onClick={() => setShowFavoritesOnly(!showFavoritesOnly)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors flex items-center gap-2 ${showFavoritesOnly ? 'bg-yellow-100 text-yellow-800 border-2 border-yellow-400' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
              >
                <span>⭐</span>
                <span>Favorites ({favorites.size})</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          
          {/* Filters Sidebar */}
          <div className={`lg:col-span-1 space-y-4 transition-all duration-300 ${sidebarOpen ? 'block' : 'hidden lg:block'}`}>
            <div className="bg-white rounded-lg shadow p-4">
              <div className="flex items-center justify-between mb-4">
                <h2 className="font-semibold text-gray-900">🔍 Filters</h2>
                <button
                  onClick={() => setSidebarOpen(false)}
                  className="lg:hidden text-gray-500 hover:text-gray-700"
                >
                  ✕
                </button>
              </div>
              
              {/* Search */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Search
                </label>
                <input
                  type="text"
                  value={filters.search_query || ''}
                  onChange={(e) => updateFilter('search_query', e.target.value || undefined)}
                  placeholder="Search exercises..."
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              {/* Category Filter */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Movement Pattern
                </label>
                <select
                  value={filters.category || ''}
                  onChange={(e) => updateFilter('category', e.target.value || undefined)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">All Patterns</option>
                  {EXERCISE_CATEGORIES.map(cat => (
                    <option key={cat} value={cat}>{cat}</option>
                  ))}
                </select>
              </div>

              {/* Equipment Filter */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Equipment
                </label>
                <select
                  value={filters.equipment || ''}
                  onChange={(e) => updateFilter('equipment', e.target.value || undefined)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={!filterOptions}
                >
                  <option value="">All Equipment</option>
                  {filterOptions?.equipment.map(eq => (
                    <option key={eq} value={eq}>{eq}</option>
                  ))}
                </select>
              </div>

              {/* Difficulty Filter */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Difficulty
                </label>
                <select
                  value={filters.difficulty_level || ''}
                  onChange={(e) => updateFilter('difficulty_level', e.target.value || undefined)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">All Levels</option>
                  {DIFFICULTY_LEVELS.map(level => (
                    <option key={level} value={level}>{level}</option>
                  ))}
                </select>
              </div>

              {/* Force Vector Filter */}
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Force Vector
                </label>
                <select
                  value={filters.force_vector || ''}
                  onChange={(e) => updateFilter('force_vector', e.target.value || undefined)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">All Vectors</option>
                  {FORCE_VECTORS.map(vector => (
                    <option key={vector} value={vector}>{vector}</option>
                  ))}
                </select>
              </div>

              {/* Has Coaching Cues Toggle */}
              <div className="mb-4">
                <label className="flex items-center gap-2 text-sm font-medium text-gray-700 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={filters.has_coaching_cues || false}
                    onChange={(e) => updateFilter('has_coaching_cues', e.target.checked || undefined)}
                    className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                  />
                  Has Coaching Cues
                </label>
              </div>

              {/* Clear Filters Button */}
              <button
                onClick={clearFilters}
                className="w-full px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors"
              >
                Clear All Filters
              </button>

              {/* Active Filters Count */}
              <div className="mt-3 pt-3 border-t border-gray-200">
                <p className="text-xs text-gray-500">
                  Active filters:{' '}
                  {[filters.category, filters.equipment, filters.difficulty_level, filters.force_vector, filters.has_coaching_cues].filter(Boolean).length}
                </p>
              </div>
            </div>

            {/* Stats */}
            <div className="bg-white rounded-lg shadow p-4">
              <h3 className="font-semibold text-gray-900 mb-2">📊 Quick Stats</h3>
              <div className="space-y-2 text-sm text-gray-600">
                <div className="flex justify-between">
                  <span>Total Exercises:</span>
                  <span className="font-medium">{exercises.length}</span>
                </div>
                <div className="flex justify-between">
                  <span>Categories:</span>
                  <span className="font-medium">{EXERCISE_CATEGORIES.length}</span>
                </div>
                <div className="flex justify-between">
                  <span>Sources:</span>
                  <span className="font-medium">{SOURCE_ORGANIZATIONS.length}</span>
                </div>
              </div>
            </div>
          </div>

          {/* Exercise List */}
          <div className="lg:col-span-3">
            {loading ? (
              <div className="bg-white rounded-lg shadow p-8 text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p className="mt-4 text-gray-600">Loading exercises...</p>
              </div>
            ) : error ? (
              <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
                <p className="text-red-600">{error}</p>
              </div>
            ) : exercises.length === 0 ? (
              <div className="bg-white rounded-lg shadow p-8 text-center">
                <p className="text-gray-600">
                  {showFavoritesOnly 
                    ? "No favorite exercises found. Click the star icon on exercises to add them to your favorites!"
                    : "No exercises found matching your filters."}
                </p>
              </div>
            ) : (
              <div className={viewMode === 'grid' ? "grid grid-cols-1 md:grid-cols-2 gap-4" : "space-y-3"}>
                {exercises.map(exercise => (
                  <div
                    key={exercise.id}
                    onClick={() => setSelectedExercise(exercise)}
                    className={`bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow cursor-pointer ${viewMode === 'list' ? 'flex items-center justify-between' : ''}`}
                  >
                    <div className={viewMode === 'list' ? 'flex-1' : ''}>
                      <div className="flex items-start justify-between mb-2">
                        <h3 className="font-semibold text-gray-900 flex items-center">
                          <span className="mr-2">{getCategoryIcon(exercise.category)}</span>
                          {exercise.name}
                        </h3>
                        {viewMode === 'list' && (
                          <div className="flex items-center gap-2">
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                toggleFavorite(String(exercise.id));
                              }}
                              className={`p-2 rounded-full hover:bg-gray-100 transition-colors ${favorites.has(String(exercise.id)) ? 'text-yellow-500' : 'text-gray-400'}`}
                              title={favorites.has(String(exercise.id)) ? 'Remove from favorites' : 'Add to favorites'}
                            >
                              <svg className="w-5 h-5" fill={favorites.has(String(exercise.id)) ? 'currentColor' : 'none'} stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                              </svg>
                            </button>
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                addToWorkout(exercise);
                              }}
                              className="p-2 rounded-full hover:bg-blue-50 text-blue-600 transition-colors"
                              title="Add to workout"
                            >
                              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                              </svg>
                            </button>
                          </div>
                        )}
                      </div>
                      
                      <div className="flex flex-wrap gap-2 mb-3">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${getDifficultyColor(exercise.difficulty_level)}`}>
                          {exercise.difficulty_level}
                        </span>
                        <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
                          {exercise.category}
                        </span>
                        <span className="px-2 py-1 bg-blue-50 text-blue-700 rounded text-xs">
                          {exercise.force_vector}
                        </span>
                      </div>
                      
                      <div className="text-sm text-gray-600">
                        <p className="truncate">
                          <span className="font-medium">Source:</span> {exercise.source_organization}
                        </p>
                        <p className="truncate mt-1">
                          <span className="font-medium">Equipment:</span> {exercise.equipment_needed}
                        </p>
                      </div>
                    </div>
                    
                    {viewMode === 'grid' && (
                      <div className="flex items-center gap-2 mt-3 pt-3 border-t border-gray-100">
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            toggleFavorite(String(exercise.id));
                          }}
                          className={`p-1.5 rounded-full hover:bg-gray-100 transition-colors ${favorites.has(String(exercise.id)) ? 'text-yellow-500' : 'text-gray-400'}`}
                          title={favorites.has(String(exercise.id)) ? 'Remove from favorites' : 'Add to favorites'}
                        >
                          <svg className="w-4 h-4" fill={favorites.has(String(exercise.id)) ? 'currentColor' : 'none'} stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
                          </svg>
                        </button>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            addToWorkout(exercise);
                          }}
                          className="p-1.5 rounded-full hover:bg-blue-50 text-blue-600 transition-colors"
                          title="Add to workout"
                        >
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                          </svg>
                        </button>
                        <span className="ml-auto text-xs text-gray-500">Click for details →</span>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Exercise Detail Modal */}
      {selectedExercise && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-3xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6">
              {/* Header */}
              <div className="flex justify-between items-start mb-4">
                <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                  <span className="mr-2">{getCategoryIcon(selectedExercise.category)}</span>
                  {selectedExercise.name}
                </h2>
                <button
                  onClick={() => setSelectedExercise(null)}
                  className="text-gray-400 hover:text-gray-600"
                >
                  ✕
                </button>
              </div>

              {/* Meta Info */}
              <div className="flex flex-wrap gap-2 mb-6">
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getDifficultyColor(selectedExercise.difficulty_level)}`}>
                  {selectedExercise.difficulty_level}
                </span>
                <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">
                  {selectedExercise.category}
                </span>
                <span className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm">
                  {selectedExercise.force_vector}
                </span>
                <span className="px-3 py-1 bg-purple-50 text-purple-700 rounded-full text-sm">
                  {selectedExercise.source_organization}
                </span>
              </div>

              {/* Coaching Cues */}
              <div className="mb-6">
                <h3 className="font-semibold text-gray-900 mb-2 flex items-center">
                  <span className="mr-2">✅</span> Coaching Cues
                </h3>
                <ul className="list-disc list-inside space-y-1 text-gray-700">
                  {selectedExercise.coaching_cues.map((cue, idx) => (
                    <li key={idx}>{cue}</li>
                  ))}
                </ul>
              </div>

              {/* Common Errors */}
              <div className="mb-6">
                <h3 className="font-semibold text-gray-900 mb-2 flex items-center">
                  <span className="mr-2">⚠️</span> Common Errors
                </h3>
                <ul className="list-disc list-inside space-y-1 text-red-600">
                  {selectedExercise.common_errors.map((error, idx) => (
                    <li key={idx}>{error}</li>
                  ))}
                </ul>
              </div>

              {/* Contraindications */}
              <div className="mb-6">
                <h3 className="font-semibold text-gray-900 mb-2 flex items-center">
                  <span className="mr-2">🚫</span> Contraindications
                </h3>
                <ul className="list-disc list-inside space-y-1 text-orange-600">
                  {selectedExercise.contraindications.map((item, idx) => (
                    <li key={idx}>{item}</li>
                  ))}
                </ul>
              </div>

              {/* Progressions & Regressions Grid */}
              <div className="grid grid-cols-2 gap-4 mb-6">
                <div>
                  <h3 className="font-semibold text-gray-900 mb-2">📈 Progressions</h3>
                  <ul className="list-disc list-inside space-y-1 text-green-700 text-sm">
                    {selectedExercise.progressions.map((prog, idx) => (
                      <li key={idx}>{prog}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900 mb-2">📉 Regressions</h3>
                  <ul className="list-disc list-inside space-y-1 text-blue-700 text-sm">
                    {selectedExercise.regressions.map((reg, idx) => (
                      <li key={idx}>{reg}</li>
                    ))}
                  </ul>
                </div>
              </div>

              {/* Equipment */}
              <div className="mb-6">
                <h3 className="font-semibold text-gray-900 mb-2">🏋️ Equipment Needed</h3>
                <p className="text-gray-700">{selectedExercise.equipment_needed}</p>
                {selectedExercise.equipment_alternatives && selectedExercise.equipment_alternatives.length > 0 && (
                  <>
                    <h4 className="font-medium text-gray-900 mt-2 mb-1">Alternatives:</h4>
                    <ul className="list-disc list-inside space-y-1 text-gray-600 text-sm">
                      {selectedExercise.equipment_alternatives.map((alt, idx) => (
                        <li key={idx}>{alt}</li>
                      ))}
                    </ul>
                  </>
                )}
              </div>

              {/* Close Button */}
              <button
                onClick={() => setSelectedExercise(null)}
                className="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
