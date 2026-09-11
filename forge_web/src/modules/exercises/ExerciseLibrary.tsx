/**
 * Exercise Library Page
 * Browse, filter, and search all exercises
 */

import React, { useState, useEffect } from 'react';
import exerciseService, { Exercise, ExerciseFilters } from './exercise.service';
import ExerciseCard from './ExerciseCard';

const ExerciseLibrary: React.FC = () => {
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState<ExerciseFilters>({
    category: '',
    movement_pattern: '',
    difficulty: '',
    is_pain_safe: false,
  });
  const [filterOptions, setFilterOptions] = useState<{
    categories: string[];
    movementPatterns: string[];
    difficulties: string[];
  }>({
    categories: [],
    movementPatterns: [],
    difficulties: [],
  });

  useEffect(() => {
    loadExercises();
    loadFilterOptions();
  }, []);

  const loadExercises = async (customFilters?: ExerciseFilters) => {
    try {
      setLoading(true);
      const activeFilters = customFilters || filters;
      
      // Add search query if present
      if (searchQuery) {
        const results = await exerciseService.searchExercises(searchQuery);
        setExercises(results);
      } else {
        const results = await exerciseService.getExercises(activeFilters);
        setExercises(results);
      }
      setError(null);
    } catch (err) {
      setError('Failed to load exercises. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const loadFilterOptions = async () => {
    try {
      const options = await exerciseService.getFilterOptions();
      setFilterOptions(options);
    } catch (err) {
      console.error('Failed to load filter options:', err);
    }
  };

  const handleFilterChange = (key: keyof ExerciseFilters, value: any) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    loadExercises(newFilters);
  };

  const resetFilters = () => {
    const emptyFilters: ExerciseFilters = {};
    setFilters(emptyFilters);
    setSearchQuery('');
    loadExercises(emptyFilters);
  };

  const togglePainSafe = () => {
    const newValue = !filters.is_pain_safe;
    handleFilterChange('is_pain_safe', newValue);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Exercise Library</h1>
          <p className="mt-2 text-gray-600">
            Browse {exercises.length} CSCS-certified exercises from authoritative sources
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search and Filters */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
            {/* Search */}
            <div className="lg:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Search Exercises
              </label>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && loadExercises()}
                placeholder="Search by name or description..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Category Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Category
              </label>
              <select
                value={filters.category || ''}
                onChange={(e) => handleFilterChange('category', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Categories</option>
                {filterOptions.categories.map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>

            {/* Movement Pattern Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Movement Pattern
              </label>
              <select
                value={filters.movement_pattern || ''}
                onChange={(e) => handleFilterChange('movement_pattern', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Patterns</option>
                {filterOptions.movementPatterns.map(pattern => (
                  <option key={pattern} value={pattern}>{pattern}</option>
                ))}
              </select>
            </div>

            {/* Difficulty Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Difficulty
              </label>
              <select
                value={filters.difficulty || ''}
                onChange={(e) => handleFilterChange('difficulty', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Levels</option>
                {filterOptions.difficulties.map(diff => (
                  <option key={diff} value={diff}>{diff}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Pain-Safe Toggle & Reset */}
          <div className="mt-4 flex items-center justify-between">
            <label className="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                checked={filters.is_pain_safe || false}
                onChange={togglePainSafe}
                className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
              />
              <span className="text-sm font-medium text-gray-700">
                Show Pain-Safe Only (Return-to-Play)
              </span>
            </label>

            <button
              onClick={resetFilters}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
            >
              Reset Filters
            </button>
          </div>
        </div>

        {/* Results Count */}
        <div className="mb-6">
          <p className="text-sm text-gray-600">
            Showing <span className="font-semibold">{exercises.length}</span> exercises
          </p>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="flex justify-center items-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {/* Exercise Grid */}
        {!loading && !error && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {exercises.map(exercise => (
              <ExerciseCard 
                key={exercise.id} 
                exercise={exercise}
                onClick={() => {
                  // Could open modal or navigate to detail page
                  console.log('Clicked exercise:', exercise.name);
                }}
              />
            ))}
          </div>
        )}

        {/* Empty State */}
        {!loading && !error && exercises.length === 0 && (
          <div className="text-center py-12">
            <h3 className="text-lg font-medium text-gray-900 mb-2">No exercises found</h3>
            <p className="text-gray-600 mb-4">Try adjusting your filters or search query</p>
            <button
              onClick={resetFilters}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              Clear All Filters
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default ExerciseLibrary;
