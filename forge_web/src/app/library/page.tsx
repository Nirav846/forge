'use client';

import React, { useState, useEffect } from 'react';
import { Exercise, ExerciseFilters, fetchExercises, EXERCISE_CATEGORIES, DIFFICULTY_LEVELS, FORCE_VECTORS, SOURCE_ORGANIZATIONS, getDifficultyColor, getCategoryIcon } from '@/modules/exercises/exerciseService';

export default function ExerciseLibraryPage() {
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedExercise, setSelectedExercise] = useState<Exercise | null>(null);
  
  const [filters, setFilters] = useState<ExerciseFilters>({
    search_query: '',
    category: undefined,
    difficulty_level: undefined,
    force_vector: undefined
  });

  useEffect(() => {
    loadExercises();
  }, [filters]);

  async function loadExercises() {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchExercises(filters);
      setExercises(data);
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
      force_vector: undefined
    });
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">📚 FORGE Exercise Library</h1>
          <p className="mt-2 text-gray-600">
            CSCS-Certified Exercise Database • {exercises.length} Exercises Available
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          
          {/* Filters Sidebar */}
          <div className="lg:col-span-1 space-y-4">
            <div className="bg-white rounded-lg shadow p-4">
              <h2 className="font-semibold text-gray-900 mb-4">🔍 Filters</h2>
              
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
                  Category
                </label>
                <select
                  value={filters.category || ''}
                  onChange={(e) => updateFilter('category', e.target.value || undefined)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">All Categories</option>
                  {EXERCISE_CATEGORIES.map(cat => (
                    <option key={cat} value={cat}>{cat}</option>
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

              {/* Clear Filters Button */}
              <button
                onClick={clearFilters}
                className="w-full px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors"
              >
                Clear All Filters
              </button>
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
                <p className="text-gray-600">No exercises found matching your filters.</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {exercises.map(exercise => (
                  <div
                    key={exercise.id}
                    onClick={() => setSelectedExercise(exercise)}
                    className="bg-white rounded-lg shadow p-4 hover:shadow-md transition-shadow cursor-pointer"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <h3 className="font-semibold text-gray-900 flex items-center">
                        <span className="mr-2">{getCategoryIcon(exercise.category)}</span>
                        {exercise.name}
                      </h3>
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
