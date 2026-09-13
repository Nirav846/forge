/**
 * Exercise Library Page
 * Browse, filter, and search all exercises with left navigation panel
 */

import React, { useState, useEffect, useMemo } from 'react';
import exerciseService, { Exercise, ExerciseFilters } from './exercise.service';
import ExerciseCard from './ExerciseCard';

// Category display names and groupings
const CATEGORY_GROUPS: Record<string, { name: string; icon: string; description: string }> = {
  // Lower Body
  'DLKD': { name: 'Double Leg - Knee Dominant', icon: '🦵', description: 'Squats, lunges, knee-focused movements' },
  'DLHD': { name: 'Double Leg - Hip Dominant', icon: '🍑', description: 'Deadlifts, hinges, hip-focused movements' },
  'SLKD': { name: 'Single Leg - Knee Dominant', icon: '🦵', description: 'Single leg squats, step-ups' },
  'SLHD': { name: 'Single Leg - Hip Dominant', icon: '🍑', description: 'Single leg deadlifts, bridges' },
  // Upper Body Push
  'HPush': { name: 'Horizontal Push', icon: '➡️', description: 'Push-ups, bench press variations' },
  'VPush': { name: 'Vertical Push', icon: '⬆️', description: 'Overhead press, push press' },
  // Upper Body Pull
  'HPull': { name: 'Horizontal Pull', icon: '⬅️', description: 'Rows, face pulls' },
  'VPull': { name: 'Vertical Pull', icon: '⬇️', description: 'Pull-ups, lat pulldowns' },
  // Core
  'Core': { name: 'Core & Stability', icon: '🎯', description: 'Anti-rotation, planks, carries' },
  'Carry': { name: 'Carries', icon: '🏋️', description: 'Farmer walks, suitcase carries' },
  'Rot': { name: 'Rotation', icon: '🔄', description: 'Rotational power and stability' },
  // Power & Plyometrics
  'Plyo': { name: 'Plyometrics', icon: '💥', description: 'Jumps, bounds, explosive movements' },
  'Landing': { name: 'Landing Mechanics', icon: '🛬', description: 'Deceleration, landing technique' },
  'Ball': { name: 'Medicine Ball', icon: '🏀', description: 'Med ball throws and slams' },
  // Speed & Agility
  'Sprint': { name: 'Sprinting', icon: '🏃', description: 'Acceleration, max velocity' },
  'Acc': { name: 'Acceleration', icon: '🚀', description: 'First step, initial acceleration' },
  'Agility': { name: 'Agility', icon: '⚡', description: 'Change of direction, reactive drills' },
  // Supportive
  'Activation': { name: 'Activation', icon: '🔌', description: 'Glute, core, shoulder activation' },
  'Assessment': { name: 'Assessment', icon: '📊', description: 'Movement screens, tests' },
  'Cond': { name: 'Conditioning', icon: '❤️', description: 'Energy system development' },
  'Recovery': { name: 'Recovery', icon: '🧘', description: 'Mobility, regeneration work' },
};

const DIFFICULTY_COLORS = {
  Beginner: 'bg-green-100 text-green-800 border-green-200',
  Intermediate: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  Advanced: 'bg-red-100 text-red-800 border-red-200',
};

const ExerciseLibrary: React.FC = () => {
  const [allExercises, setAllExercises] = useState<Exercise[]>([]);
  const [filteredExercises, setFilteredExercises] = useState<Exercise[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('');
  const [isPainSafeOnly, setIsPainSafeOnly] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeSection, setActiveSection] = useState<string>('');
  const [categories, setCategories] = useState<string[]>([]);
  const [difficulties, setDifficulties] = useState<string[]>([]);

  useEffect(() => {
    loadData();
  }, []);

  useEffect(() => {
    const handleScroll = () => {
      const sections = filteredExercises.map(e => e.category).filter((v, i, a) => a.indexOf(v) === i);
      for (const section of sections) {
        const element = document.getElementById(`category-${section}`);
        if (element) {
          const rect = element.getBoundingClientRect();
          if (rect.top <= 150 && rect.bottom >= 150) {
            setActiveSection(section);
            break;
          }
        }
      }
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [filteredExercises]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [exercisesData, filterOptions] = await Promise.all([
        exerciseService.getExercises({}),
        exerciseService.getFilterOptions(),
      ]);
      setAllExercises(exercisesData);
      setFilteredExercises(exercisesData);
      setCategories(filterOptions.categories);
      setDifficulties(filterOptions.difficulties);
      setError(null);
    } catch (err) {
      setError('Failed to load exercises. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let result = [...allExercises];
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      result = result.filter(ex => ex.name.toLowerCase().includes(query) || ex.description.toLowerCase().includes(query) || ex.category.toLowerCase().includes(query) || ex.equipment.toLowerCase().includes(query));
    }
    if (selectedCategory) {
      result = result.filter(ex => ex.category === selectedCategory);
    }
    if (selectedDifficulty) {
      result = result.filter(ex => ex.difficulty === selectedDifficulty);
    }
    if (isPainSafeOnly) {
      result = result.filter(ex => ex.is_pain_safe);
    }
    setFilteredExercises(result);
  }, [allExercises, searchQuery, selectedCategory, selectedDifficulty, isPainSafeOnly]);

  const resetFilters = () => {
    setSearchQuery('');
    setSelectedCategory('');
    setSelectedDifficulty('');
    setIsPainSafeOnly(false);
  };

  const exercisesByCategory = useMemo(() => {
    const grouped: Record<string, Exercise[]> = {};
    filteredExercises.forEach(exercise => {
      if (!grouped[exercise.category]) {
        grouped[exercise.category] = [];
      }
      grouped[exercise.category].push(exercise);
    });
    return grouped;
  }, [filteredExercises]);

  const categoryCounts = useMemo(() => {
    const counts: Record<string, number> = {};
    allExercises.forEach(ex => {
      counts[ex.category] = (counts[ex.category] || 0) + 1;
    });
    return counts;
  }, [allExercises]);

  return (
    <div className="min-h-screen bg-gray-50 flex">
      <aside className={`fixed left-0 top-0 h-full bg-white border-r border-gray-200 transition-all duration-300 z-50 ${sidebarOpen ? 'w-72' : 'w-0'} overflow-hidden`}>
        <div className="p-4 h-full flex flex-col">
          <div className="mb-4 pb-4 border-b border-gray-200">
            <h2 className="text-lg font-bold text-gray-900">Categories</h2>
            <p className="text-xs text-gray-500 mt-1">{allExercises.length} total exercises</p>
          </div>
          <div className="mb-4 p-3 bg-blue-50 rounded-lg">
            <div className="flex justify-between items-center">
              <span className="text-sm font-medium text-blue-800">Pain-Safe</span>
              <span className="text-lg font-bold text-blue-600">{allExercises.filter(e => e.is_pain_safe).length}</span>
            </div>
          </div>
          <nav className="flex-1 overflow-y-auto space-y-1">
            <button onClick={() => setSelectedCategory('')} className={`w-full text-left px-3 py-2 rounded-lg text-sm font-medium transition-colors ${selectedCategory === '' ? 'bg-blue-100 text-blue-800' : 'text-gray-700 hover:bg-gray-100'}`}>
              <span className="flex items-center justify-between">
                <span>📚 All Exercises</span>
                <span className="text-xs bg-gray-200 px-2 py-0.5 rounded-full">{allExercises.length}</span>
              </span>
            </button>
            {Object.entries(CATEGORY_GROUPS).map(([key, info]) => {
              const count = categoryCounts[key] || 0;
              if (count === 0) return null;
              return (
                <button key={key} onClick={() => setSelectedCategory(key)} className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${selectedCategory === key ? 'bg-blue-100 text-blue-800' : 'text-gray-700 hover:bg-gray-100'}`}>
                  <span className="flex items-center justify-between">
                    <span className="truncate"><span className="mr-2">{info.icon}</span><span className="font-medium">{info.name}</span></span>
                    <span className="text-xs bg-gray-200 px-2 py-0.5 rounded-full ml-2 flex-shrink-0">{count}</span>
                  </span>
                </button>
              );
            })}
          </nav>
          <div className="pt-4 border-t border-gray-200">
            <button onClick={() => setSidebarOpen(false)} className="w-full px-3 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">← Collapse Sidebar</button>
          </div>
        </div>
      </aside>
      <main className={`flex-1 transition-all duration-300 ${sidebarOpen ? 'ml-72' : 'ml-0'}`}>
        <div className="sticky top-0 z-40 bg-white border-b border-gray-200 shadow-sm">
          <div className="px-6 py-4">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-4">
                {!sidebarOpen && (<button onClick={() => setSidebarOpen(true)} className="p-2 hover:bg-gray-100 rounded-lg transition-colors" title="Open sidebar"><svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" /></svg></button>)}
                <div>
                  <h1 className="text-2xl font-bold text-gray-900">Exercise Library</h1>
                  <p className="text-sm text-gray-600">{filteredExercises.length} exercises{selectedCategory && ` in ${CATEGORY_GROUPS[selectedCategory]?.name}`}</p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                {isPainSafeOnly && (<span className="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full font-medium">✓ Pain-Safe Only</span>)}
                {selectedDifficulty && (<span className={`px-3 py-1 text-sm rounded-full font-medium ${DIFFICULTY_COLORS[selectedDifficulty as keyof typeof DIFFICULTY_COLORS]}`}>{selectedDifficulty}</span>)}
                {(searchQuery || selectedCategory || selectedDifficulty || isPainSafeOnly) && (<button onClick={resetFilters} className="px-3 py-1 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-full transition-colors">✕ Clear all</button>)}
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex-1 relative">
                <input type="text" value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} placeholder="Search exercises by name, description, equipment..." className="w-full px-4 py-2.5 pl-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" />
                <svg className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
              </div>
              <div className="flex items-center space-x-2">
                <span className="text-sm text-gray-600">Difficulty:</span>
                {['Beginner', 'Intermediate', 'Advanced'].map((diff) => (<button key={diff} onClick={() => setSelectedDifficulty(selectedDifficulty === diff ? '' : diff)} className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors border ${selectedDifficulty === diff ? DIFFICULTY_COLORS[diff as keyof typeof DIFFICULTY_COLORS] : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'}`}>{diff.charAt(0)}</button>))}
              </div>
              <label className="flex items-center space-x-2 cursor-pointer px-3 py-2 bg-green-50 hover:bg-green-100 rounded-lg transition-colors">
                <input type="checkbox" checked={isPainSafeOnly} onChange={(e) => setIsPainSafeOnly(e.target.checked)} className="w-4 h-4 text-green-600 rounded focus:ring-green-500" />
                <span className="text-sm font-medium text-green-800 whitespace-nowrap">Pain-Safe Only</span>
              </label>
            </div>
          </div>
        </div>
        <div className="p-6">
          {loading && (<div className="flex justify-center items-center py-12"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div></div>)}
          {error && (<div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">{error}</div>)}
          {!loading && !error && filteredExercises.length === 0 && (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">🔍</div>
              <h3 className="text-xl font-medium text-gray-900 mb-2">No exercises found</h3>
              <p className="text-gray-600 mb-6">Try adjusting your search or filters to find what you are looking for</p>
              <button onClick={resetFilters} className="px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors shadow-md">Clear All Filters</button>
            </div>
          )}
          {!loading && !error && filteredExercises.length > 0 && (
            <div className="space-y-8">
              {Object.entries(exercisesByCategory).map(([category, exercises]) => {
                const catInfo = CATEGORY_GROUPS[category];
                return (
                  <div key={category} id={`category-${category}`} className="scroll-mt-32">
                    <div className="flex items-center space-x-3 mb-4 pb-3 border-b border-gray-200">
                      <span className="text-2xl">{catInfo?.icon || '📋'}</span>
                      <div>
                        <h2 className="text-xl font-bold text-gray-900">{catInfo?.name || category}</h2>
                        {catInfo?.description && (<p className="text-sm text-gray-600">{catInfo.description}</p>)}
                      </div>
                      <span className="ml-auto px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-full font-medium">{exercises.length} exercises</span>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                      {exercises.map((exercise) => (<ExerciseCard key={exercise.id} exercise={exercise} onClick={() => { console.log('Clicked exercise:', exercise.name); }} />))}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default ExerciseLibrary;
