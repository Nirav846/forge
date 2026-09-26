/**
 * Complexes Library with lazy-loaded data
 * Improves initial bundle size by loading complexes data on demand
 */
import React, { useState, useEffect, useMemo } from 'react';
import { 
  Filter, Search, Activity, Zap, Shield, Clock, 
  ChevronRight, X, CheckCircle, Dumbbell, Users, 
  TrendingUp, Award, PlayCircle, PlusCircle 
} from 'lucide-react';

interface Complex {
  id: string;
  name: string;
  sport: string;
  role: string;
  plane: string;
  intent: string;
  description: string;
  exercises: Array<{
    exerciseId: string | number;
    exerciseName: string;
    sets: number;
    reps: string;
    restSeconds: number;
  }>;
  coachingNotes: string;
  equipment: string[];
}

interface FilterState {
  sport: string;
  role: string;
  plane: string;
  intent: string;
  search: string;
}

interface ComplexesLibraryProps {
  onExit?: () => void;
}

const ComplexesLibrary: React.FC<ComplexesLibraryProps> = ({ onExit }) => {
  const [complexesData, setComplexesData] = useState<Complex[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);
  
  const [filters, setFilters] = useState<FilterState>({
    sport: 'All',
    role: 'All',
    plane: 'All',
    intent: 'All',
    search: ''
  });
  
  const [selectedComplex, setSelectedComplex] = useState<Complex | null>(null);
  // Per-card expansion state for the "+X more" links (opens inline instead of a modal)
  const [expandedCards, setExpandedCards] = useState<Set<string>>(new Set());
  const [availableRoles, setAvailableRoles] = useState<string[]>([]);

  const toggleCardExpanded = (id: string) => {
    setExpandedCards(prev => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  // Lazy load complexes data using fetch
  useEffect(() => {
    const loadComplexes = async () => {
      try {
        setIsLoading(true);
        const response = await fetch('./data/complexes.json');
        if (!response.ok) throw new Error('Failed to load complexes');
        const data = await response.json();
        const list: any[] = Array.isArray(data) ? data : (data?.complexes ?? []);
        // Normalize each record defensively so a single malformed entry cannot
        // crash rendering (which previously left the page blank).
        const normalized: Complex[] = list.map((c: any) => ({
          id: String(c?.id ?? crypto.randomUUID?.() ?? Math.random().toString(36).slice(2)),
          name: String(c?.name ?? 'Untitled complex'),
          sport: String(c?.sport ?? 'Unknown'),
          role: String(c?.role ?? 'Unknown'),
          plane: String(c?.plane ?? 'Unknown'),
          intent: String(c?.intent ?? 'Unknown'),
          description: String(c?.description ?? ''),
          coachingNotes: String(c?.coachingNotes ?? ''),
          equipment: Array.isArray(c?.equipment) ? c.equipment.map((e: any) => String(e)) : [],
          exercises: Array.isArray(c?.exercises)
            ? c.exercises.map((e: any) => ({
                exerciseId: e?.exerciseId ?? '',
                exerciseName: String(e?.exerciseName ?? 'Unknown exercise'),
                sets: Number(e?.sets ?? 0),
                reps: String(e?.reps ?? '-'),
                restSeconds: Number(e?.restSeconds ?? 0),
              }))
            : [],
        }));
        setComplexesData(normalized);
        setLoadError(null);
      } catch (error) {
        console.error('Failed to load complexes data:', error);
        setLoadError('Failed to load complexes library');
      } finally {
        setIsLoading(false);
      }
    };
    
    loadComplexes();
  }, []);

  // Extract unique values for filters
  const sports = ['All', ...Array.from(new Set(complexesData.map(c => c.sport)))];
  const planes = ['All', ...Array.from(new Set(complexesData.map(c => c.plane)))];
  const intents = ['All', ...Array.from(new Set(complexesData.map(c => c.intent)))];

  // Update available roles when sport changes
  useEffect(() => {
    if (filters.sport === 'All') {
      setAvailableRoles(['All', ...Array.from(new Set(complexesData.map(c => c.role)))]);
    } else {
      const sportRoles = complexesData
        .filter(c => c.sport === filters.sport)
        .map(c => c.role);
      setAvailableRoles(['All', ...Array.from(new Set(sportRoles))]);

      // Reset role if current selection is not available
      if (filters.role !== 'All' && !sportRoles.includes(filters.role)) {
        setFilters(prev => ({ ...prev, role: 'All' }));
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters.sport, complexesData]);

  // Filter complexes
  const filteredComplexes = useMemo(() => {
    return complexesData.filter(complex => {
      const matchesSport = filters.sport === 'All' || complex.sport === filters.sport;
      const matchesRole = filters.role === 'All' || complex.role === filters.role;
      const matchesPlane = filters.plane === 'All' || complex.plane === filters.plane;
      const matchesIntent = filters.intent === 'All' || complex.intent === filters.intent;
      const matchesSearch = filters.search === '' ||
        complex.name.toLowerCase().includes(filters.search.toLowerCase()) ||
        complex.description.toLowerCase().includes(filters.search.toLowerCase());

      return matchesSport && matchesRole && matchesPlane && matchesIntent && matchesSearch;
    });
  }, [complexesData, filters]);

  // Show loading state (all hooks must run before any conditional return)
  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center h-screen bg-gray-50">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mb-4"></div>
        <p className="text-gray-600 font-medium">Loading Complexes Library...</p>
      </div>
    );
  }

  // Show error state
  if (loadError) {
    return (
      <div className="flex flex-col items-center justify-center h-screen bg-red-50">
        <div className="text-red-500 text-5xl mb-4">⚠️</div>
        <h3 className="text-lg font-bold text-red-800 mb-2">{loadError}</h3>
        <button
          onClick={() => window.location.reload()}
          className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors mt-4"
        >
          Reload Page
        </button>
      </div>
    );
  }

  const getBadgeColor = (type: string, value: string) => {
    const colors: Record<string, Record<string, string>> = {
      sport: {
        Cricket: 'bg-blue-100 text-blue-800 border-blue-200',
        Tennis: 'bg-green-100 text-green-800 border-green-200',
        Badminton: 'bg-red-100 text-red-800 border-red-200',
        Football: 'bg-orange-100 text-orange-800 border-orange-200',
        Rugby: 'bg-purple-100 text-purple-800 border-purple-200'
      },
      plane: {
        Sagittal: 'bg-blue-50 text-blue-700 border-blue-200',
        Frontal: 'bg-green-50 text-green-700 border-green-200',
        Transverse: 'bg-purple-50 text-purple-700 border-purple-200',
        'Multi-Planar': 'bg-indigo-50 text-indigo-700 border-indigo-200'
      },
      intent: {
        Preparation: 'bg-yellow-50 text-yellow-700 border-yellow-200',
        Power: 'bg-red-50 text-red-700 border-red-200',
        Stability: 'bg-blue-50 text-blue-700 border-blue-200',
        Agility: 'bg-orange-50 text-orange-700 border-orange-200',
        Conditioning: 'bg-purple-50 text-purple-700 border-purple-200',
        Recovery: 'bg-green-50 text-green-700 border-green-200'
      }
    };
    return colors[type]?.[value] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const getIcon = (intent: string) => {
    switch(intent) {
      case 'Preparation': return <Activity className="w-4 h-4" />;
      case 'Power': return <Zap className="w-4 h-4" />;
      case 'Stability': return <Shield className="w-4 h-4" />;
      case 'Agility': return <TrendingUp className="w-4 h-4" />;
      case 'Conditioning': return <Clock className="w-4 h-4" />;
      case 'Recovery': return <Award className="w-4 h-4" />;
      default: return <Activity className="w-4 h-4" />;
    }
  };

  const handleAddToWorkout = (complex: Complex) => {
    alert(`Added "${complex.name}" to workout!\n\nThis will add all ${complex.exercises.length} exercises with prescribed sets/reps.`);
    setSelectedComplex(null);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="py-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                {onExit && (
                  <button
                    onClick={onExit}
                    className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                    title="Back to Home"
                  >
                    <ChevronRight className="w-5 h-5 rotate-180" />
                  </button>
                )}
                <div>
                  <h1 className="text-3xl font-bold text-gray-900">Exercise Complexes</h1>
                  <p className="mt-1 text-sm text-gray-500">
                    Sport-specific multi-exercise sequences for athletic performance
                  </p>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <div className="bg-blue-50 px-3 py-1 rounded-full">
                  <span className="text-sm font-medium text-blue-700">
                    {filteredComplexes.length} Complexes
                  </span>
                </div>
              </div>
            </div>

            {/* Search Bar */}
            <div className="relative mb-4">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                placeholder="Search complexes by name or description..."
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-lg leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
                value={filters.search}
                onChange={(e) => setFilters(prev => ({ ...prev, search: e.target.value }))}
              />
            </div>

            {/* Filters */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              {/* Sport Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Sport</label>
                <select
                  value={filters.sport}
                  onChange={(e) => setFilters(prev => ({ ...prev, sport: e.target.value }))}
                  className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                >
                  {sports.map(sport => (
                    <option key={sport} value={sport}>{sport}</option>
                  ))}
                </select>
              </div>

              {/* Role Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Role</label>
                <select
                  value={filters.role}
                  onChange={(e) => setFilters(prev => ({ ...prev, role: e.target.value }))}
                  disabled={filters.sport === 'All' ? false : availableRoles.length <= 1}
                  className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md disabled:bg-gray-100"
                >
                  {availableRoles.map(role => (
                    <option key={role} value={role}>{role}</option>
                  ))}
                </select>
              </div>

              {/* Plane Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Plane of Motion</label>
                <select
                  value={filters.plane}
                  onChange={(e) => setFilters(prev => ({ ...prev, plane: e.target.value }))}
                  className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                >
                  {planes.map(plane => (
                    <option key={plane} value={plane}>{plane}</option>
                  ))}
                </select>
              </div>

              {/* Intent Filter */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Training Intent</label>
                <select
                  value={filters.intent}
                  onChange={(e) => setFilters(prev => ({ ...prev, intent: e.target.value }))}
                  className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
                >
                  {intents.map(intent => (
                    <option key={intent} value={intent}>{intent}</option>
                  ))}
                </select>
              </div>
            </div>

            {/* Active Filters */}
            {(filters.sport !== 'All' || filters.role !== 'All' || filters.plane !== 'All' || filters.intent !== 'All' || filters.search) && (
              <div className="mt-4 flex flex-wrap gap-2">
                {filters.sport !== 'All' && (
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    {filters.sport}
                    <button onClick={() => setFilters(prev => ({ ...prev, sport: 'All' }))} className="ml-1 hover:text-blue-900">
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                )}
                {filters.role !== 'All' && (
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    {filters.role}
                    <button onClick={() => setFilters(prev => ({ ...prev, role: 'All' }))} className="ml-1 hover:text-green-900">
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                )}
                {filters.plane !== 'All' && (
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                    {filters.plane}
                    <button onClick={() => setFilters(prev => ({ ...prev, plane: 'All' }))} className="ml-1 hover:text-purple-900">
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                )}
                {filters.intent !== 'All' && (
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                    {filters.intent}
                    <button onClick={() => setFilters(prev => ({ ...prev, intent: 'All' }))} className="ml-1 hover:text-orange-900">
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                )}
                {filters.search && (
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                    "{filters.search}"
                    <button onClick={() => setFilters(prev => ({ ...prev, search: '' }))} className="ml-1 hover:text-gray-900">
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                )}
                <button
                  onClick={() => setFilters({ sport: 'All', role: 'All', plane: 'All', intent: 'All', search: '' })}
                  className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-200 text-gray-700 hover:bg-gray-300"
                >
                  Clear All
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {filteredComplexes.length === 0 ? (
          <div className="text-center py-12">
            <Users className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No complexes found</h3>
            <p className="mt-1 text-sm text-gray-500">Try adjusting your filters or search terms.</p>
            <button
              onClick={() => setFilters({ sport: 'All', role: 'All', plane: 'All', intent: 'All', search: '' })}
              className="mt-6 inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
            >
              Clear all filters
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredComplexes.map(complex => (
              <div key={complex.id} className="bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200">
                <div className="p-6">
                  {/* Header */}
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">{complex.name}</h3>
                      <p className="text-sm text-gray-500 mt-1">{complex.role} • {complex.sport}</p>
                    </div>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getBadgeColor('sport', complex.sport)}`}>
                      {complex.sport}
                    </span>
                  </div>

                  {/* Badges */}
                  <div className="flex flex-wrap gap-2 mb-4">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getBadgeColor('plane', complex.plane)}`}>
                      {complex.plane}
                    </span>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getBadgeColor('intent', complex.intent)}`}>
                      {getIcon(complex.intent)}
                      <span className="ml-1">{complex.intent}</span>
                    </span>
                  </div>

                  {/* Description */}
                  <p className="text-sm text-gray-600 mb-4 line-clamp-2">{complex.description}</p>

                  {/* Exercise Preview */}
                  <div className="mb-4">
                    <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Exercises</h4>
                    <div className="space-y-2">
                      {(() => {
                        // Defensive: tolerate malformed records so a single bad
                        // entry can never blank out the whole page.
                        const exercises = Array.isArray(complex.exercises) ? complex.exercises : [];
                        const isExpanded = expandedCards.has(complex.id);
                        const visible = isExpanded ? exercises : exercises.slice(0, 3);
                        return (
                          <>
                            {visible.map((exercise, idx) => (
                              <div key={idx} className="flex items-center justify-between text-sm">
                                <span className="text-gray-700 truncate flex-1">
                                  {idx + 1}. {String(exercise?.exerciseName ?? 'Unknown exercise')}
                                </span>
                                <span className="text-gray-500 text-xs ml-2">
                                  {String(exercise?.sets ?? '-')}x{String(exercise?.reps ?? '-')}
                                </span>
                              </div>
                            ))}
                            {exercises.length > 3 && (
                              <button
                                type="button"
                                aria-expanded={isExpanded}
                                onClick={(e) => {
                                  e.preventDefault();
                                  e.stopPropagation();
                                  toggleCardExpanded(complex.id);
                                }}
                                className="text-xs text-blue-600 hover:text-blue-700 font-medium italic flex items-center gap-1 w-full text-left"
                              >
                                {isExpanded ? 'Show less' : `+${exercises.length - 3} more exercises`}
                                <ChevronRight className={`w-3 h-3 transition-transform ${isExpanded ? 'rotate-90' : ''}`} />
                              </button>
                            )}
                          </>
                        );
                      })()}
                    </div>
                  </div>

                  {/* Action Button */}
                  <button
                    onClick={() => setSelectedComplex(complex)}
                    className="w-full inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  >
                    View Protocol
                    <ChevronRight className="ml-2 w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Detail Modal */}
      {selectedComplex && (
        <div className="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
          <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            {/* Background overlay */}
            <div 
              className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" 
              aria-hidden="true"
              onClick={() => setSelectedComplex(null)}
            ></div>

            <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>

            <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full">
              {/* Modal Header */}
              <div className="bg-gray-50 px-4 py-3 sm:px-6 flex justify-between items-start">
                <div>
                  <h3 className="text-lg leading-6 font-medium text-gray-900" id="modal-title">
                    {selectedComplex.name}
                  </h3>
                  <p className="mt-1 text-sm text-gray-500">
                    {selectedComplex.role} • {selectedComplex.sport} • {selectedComplex.intent}
                  </p>
                </div>
                <button
                  onClick={() => setSelectedComplex(null)}
                  className="bg-white rounded-md text-gray-400 hover:text-gray-500 focus:outline-none"
                >
                  <X className="h-6 w-6" />
                </button>
              </div>

              {/* Modal Body */}
              <div className="px-4 py-5 sm:p-6">
                {/* Key Info Grid */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                  <div className="bg-blue-50 p-3 rounded-lg">
                    <div className="text-xs font-medium text-blue-600 uppercase">Plane</div>
                    <div className="text-sm font-semibold text-blue-900">{selectedComplex.plane}</div>
                  </div>
                  <div className="bg-green-50 p-3 rounded-lg">
                    <div className="text-xs font-medium text-green-600 uppercase">Exercises</div>
                    <div className="text-sm font-semibold text-green-900">{selectedComplex.exercises.length}</div>
                  </div>
                  <div className="bg-purple-50 p-3 rounded-lg">
                    <div className="text-xs font-medium text-purple-600 uppercase">Duration</div>
                    <div className="text-sm font-semibold text-purple-900">~15 min</div>
                  </div>
                  <div className="bg-orange-50 p-3 rounded-lg">
                    <div className="text-xs font-medium text-orange-600 uppercase">Equipment</div>
                    <div className="text-sm font-semibold text-orange-900">{selectedComplex.equipment.length}</div>
                  </div>
                </div>

                {/* Description */}
                <div className="mb-6">
                  <h4 className="text-sm font-medium text-gray-900 mb-2">Purpose</h4>
                  <p className="text-sm text-gray-600">{selectedComplex.description}</p>
                </div>

                {/* Exercise List */}
                <div className="mb-6">
                  <h4 className="text-sm font-medium text-gray-900 mb-3">Protocol</h4>
                  <div className="space-y-3">
                    {selectedComplex.exercises.map((exercise, idx) => (
                      <div key={idx} className="flex items-start p-3 bg-gray-50 rounded-lg">
                        <div className="flex-shrink-0 h-8 w-8 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-sm font-bold mr-3">
                          {idx + 1}
                        </div>
                        <div className="flex-1">
                          <div className="font-medium text-gray-900">{exercise.exerciseName}</div>
                          <div className="text-sm text-gray-600 mt-1">
                            <span className="font-medium">Sets:</span> {exercise.sets} • 
                            <span className="font-medium ml-2">Reps:</span> {exercise.reps} • 
                            <span className="font-medium ml-2">Rest:</span> {exercise.restSeconds}s
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Coaching Notes */}
                <div className="mb-6">
                  <h4 className="text-sm font-medium text-gray-900 mb-2">Coaching Notes</h4>
                  <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4">
                    <p className="text-sm text-yellow-700">{selectedComplex.coachingNotes}</p>
                  </div>
                </div>

                {/* Equipment */}
                <div>
                  <h4 className="text-sm font-medium text-gray-900 mb-2">Equipment Needed</h4>
                  <div className="flex flex-wrap gap-2">
                    {selectedComplex.equipment.map((item, idx) => (
                      <span key={idx} className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                        <Dumbbell className="w-3 h-3 mr-1" />
                        {item}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Modal Footer */}
              <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                <button
                  type="button"
                  onClick={() => handleAddToWorkout(selectedComplex)}
                  className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm"
                >
                  <PlusCircle className="w-4 h-4 mr-2" />
                  Add to Workout
                </button>
                <button
                  type="button"
                  onClick={() => setSelectedComplex(null)}
                  className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ComplexesLibrary;
