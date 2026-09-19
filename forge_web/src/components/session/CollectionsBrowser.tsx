/**
 * Collections Browser Component
 * Goal-oriented exercise browsing with curated collections
 */

import React, { useState, useMemo } from 'react';
import { Exercise } from './exercise.service';
import { 
  CURATED_COLLECTIONS, 
  Collection,
  getCollectionColorClass,
  SUPER_CATEGORIES,
  getSuperCategoryColorClass
} from '../../data/exerciseOrganization';
import ExerciseCard from './ExerciseCard';

interface CollectionsBrowserProps {
  exercises: Exercise[];
  onBack?: () => void;
}

export const CollectionsBrowser: React.FC<CollectionsBrowserProps> = ({ exercises, onBack }) => {
  const [selectedCollection, setSelectedCollection] = useState<Collection | null>(null);
  const [viewMode, setViewMode] = useState<'collections' | 'super-categories'>('collections');

  // Filter exercises based on collection criteria
  const getCollectionExercises = (collection: Collection): Exercise[] => {
    return exercises.filter(exercise => {
      const criteria = collection.filterCriteria;
      
      if (criteria.categories && !criteria.categories.includes(exercise.category)) {
        return false;
      }
      
      if (criteria.difficulties && !criteria.difficulties.includes(exercise.difficulty)) {
        return false;
      }
      
      if (criteria.is_pain_safe !== undefined && exercise.is_pain_safe !== criteria.is_pain_safe) {
        return false;
      }
      
      if (criteria.equipment && criteria.equipment.length > 0) {
        const equipmentMatch = criteria.equipment.some(eq => 
          exercise.equipment.toLowerCase().includes(eq.toLowerCase())
        );
        if (!equipmentMatch) return false;
      }
      
      return true;
    });
  };

  const filteredExercises = useMemo(() => {
    if (!selectedCollection) return exercises;
    return getCollectionExercises(selectedCollection);
  }, [selectedCollection, exercises]);

  if (selectedCollection) {
    return (
      <div className="min-h-screen bg-gray-50">
        {/* Collection Header */}
        <div className={`bg-gradient-to-r ${getCollectionColorClass(selectedCollection.color)} text-white p-8`}>
          <div className="max-w-7xl mx-auto">
            <button
              onClick={() => setSelectedCollection(null)}
              className="flex items-center gap-2 text-white/80 hover:text-white mb-4 transition-colors"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
              Back to Collections
            </button>
            
            <div className="flex items-start gap-4">
              <span className="text-5xl">{selectedCollection.icon}</span>
              <div>
                <h1 className="text-3xl font-bold mb-2">{selectedCollection.name}</h1>
                <p className="text-lg text-white/90 mb-3">{selectedCollection.description}</p>
                <div className="flex items-center gap-4 text-sm">
                  <span className="px-3 py-1 bg-white/20 rounded-full">
                    🎯 {selectedCollection.goal}
                  </span>
                  <span className="px-3 py-1 bg-white/20 rounded-full">
                    📦 {filteredExercises.length} exercises
                  </span>
                </div>
              </div>
            </div>

            {/* Recommended For Tags */}
            <div className="mt-4 flex flex-wrap gap-2">
              {selectedCollection.recommendedFor.map((rec, idx) => (
                <span key={idx} className="px-3 py-1.5 bg-white/10 border border-white/20 rounded-lg text-sm">
                  ✓ {rec}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Exercises Grid */}
        <div className="max-w-7xl mx-auto p-6">
          {filteredExercises.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">🔍</div>
              <h3 className="text-xl font-medium text-gray-900 mb-2">No exercises in this collection</h3>
              <p className="text-gray-600">Try selecting a different collection</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4">
              {filteredExercises.map((exercise) => (
                <ExerciseCard key={exercise.id} exercise={exercise} />
              ))}
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 p-6">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Browse by Goal</h1>
              <p className="text-gray-600">Curated exercise collections for specific training objectives</p>
            </div>
            {onBack && (
              <button
                onClick={onBack}
                className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
                Close
              </button>
            )}
          </div>

          {/* View Mode Toggle */}
          <div className="flex gap-2">
            <button
              onClick={() => setViewMode('collections')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                viewMode === 'collections'
                  ? 'bg-blue-100 text-blue-700'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              📚 Curated Collections
            </button>
            <button
              onClick={() => setViewMode('super-categories')}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                viewMode === 'super-categories'
                  ? 'bg-blue-100 text-blue-700'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              🏷️ Movement Categories
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto p-6">
        {viewMode === 'collections' ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {CURATED_COLLECTIONS.map((collection) => {
              const exerciseCount = getCollectionExercises(collection).length;
              
              return (
                <button
                  key={collection.id}
                  onClick={() => setSelectedCollection(collection)}
                  className="group bg-white rounded-2xl shadow-sm hover:shadow-xl transition-all duration-200 overflow-hidden border border-gray-200 text-left"
                >
                  {/* Card Header with Gradient */}
                  <div className={`h-24 bg-gradient-to-r ${getCollectionColorClass(collection.color)} relative overflow-hidden`}>
                    <div className="absolute inset-0 bg-black/10"></div>
                    <div className="absolute bottom-4 left-4 right-4">
                      <div className="flex items-center gap-3">
                        <span className="text-4xl">{collection.icon}</span>
                        <div>
                          <h3 className="text-lg font-bold text-white">{collection.name}</h3>
                          <p className="text-sm text-white/90">{exerciseCount} exercises</p>
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Card Body */}
                  <div className="p-5">
                    <p className="text-gray-600 text-sm mb-4">{collection.description}</p>
                    
                    <div className="flex items-center gap-2 mb-3">
                      <span className="text-xs font-semibold text-gray-500 uppercase">Goal:</span>
                      <span className="text-sm font-medium text-gray-700">{collection.goal}</span>
                    </div>

                    {/* Recommended For */}
                    <div className="flex flex-wrap gap-1.5">
                      {collection.recommendedFor.slice(0, 3).map((rec, idx) => (
                        <span key={idx} className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-md">
                          {rec}
                        </span>
                      ))}
                      {collection.recommendedFor.length > 3 && (
                        <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-md">
                          +{collection.recommendedFor.length - 3} more
                        </span>
                      )}
                    </div>

                    {/* Hover Arrow */}
                    <div className="mt-4 flex items-center gap-2 text-blue-600 opacity-0 group-hover:opacity-100 transition-opacity">
                      <span className="text-sm font-medium">Browse collection</span>
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </div>
                </button>
              );
            })}
          </div>
        ) : (
          /* Super-Categories View */
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {SUPER_CATEGORIES.map((superCat) => {
              const categoryCount = superCat.categories.length;
              const exercisesInCategories = exercises.filter(e => 
                superCat.categories.includes(e.category)
              ).length;

              return (
                <button
                  key={superCat.id}
                  onClick={() => {
                    // Could navigate to filtered library view
                    console.log('Navigate to super-category:', superCat.id);
                  }}
                  className={`group p-6 rounded-2xl border-2 transition-all duration-200 text-left ${getSuperCategoryColorClass(superCat.color)} hover:shadow-lg`}
                >
                  <div className="flex items-start gap-4">
                    <span className="text-5xl">{superCat.icon}</span>
                    <div className="flex-1">
                      <h3 className="text-xl font-bold mb-2">{superCat.name}</h3>
                      <p className="text-sm opacity-80 mb-3">{superCat.description}</p>
                      
                      <div className="flex items-center gap-3 text-sm">
                        <span className="font-medium">
                          {categoryCount} categories
                        </span>
                        <span className="opacity-60">•</span>
                        <span className="font-medium">
                          {exercisesInCategories} exercises
                        </span>
                      </div>

                      {/* Category Pills */}
                      <div className="flex flex-wrap gap-1.5 mt-4">
                        {superCat.categories.map((catId, idx) => (
                          <span 
                            key={idx}
                            className="px-2 py-1 bg-white/60 rounded text-xs font-medium"
                          >
                            {catId}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </button>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default CollectionsBrowser;
