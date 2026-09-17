import React, { useState, useEffect } from 'react';
import { 
  Dumbbell, 
  Trophy, 
  Users, 
  Plus, 
  ChevronRight, 
  Activity, 
  Sparkles, 
  ArrowRight,
  Star,
  Clock,
  Target,
  Zap,
  TrendingUp,
  Calendar,
  Filter,
  Search
} from 'lucide-react';
import { SavedProgramArtifact } from '../types/ui';
import { SavedProgramsDrawer } from './program/SavedProgramsDrawer';
import ExerciseLibrary from '../modules/exercises/ExerciseLibrary';
import exerciseService, { Exercise } from '../modules/exercises/exercise.service';

export type TemplateType = 'rugby_prop' | 'tennis_singles' | 'cricket_bowler';

interface TemplateInfo {
  id: TemplateType;
  sport: string;
  role: string;
  description: string;
  icon: string;
  category: string;
}

const TEMPLATES: TemplateInfo[] = [
  { id: 'rugby_prop', sport: 'Rugby Union', role: 'Tighthead Prop', description: 'Max Force & Scrum Dominance — collision sport profile', icon: '🏉', category: 'Strength' },
  { id: 'tennis_singles', sport: 'Tennis', role: 'Singles Player', description: 'Court Speed & Change of Direction — court sport profile', icon: '🎾', category: 'Power' },
  { id: 'cricket_bowler', sport: 'Cricket', role: 'Fast Bowler', description: 'Eccentric Tolerance & Delivery Velocity — field sport profile', icon: '🏏', category: 'Power' },
];

// Smart Collections - curated exercise groups
const SMART_COLLECTIONS = [
  { 
    id: 'mobility', 
    name: 'Mobility & Prep', 
    icon: Zap,
    color: 'from-emerald-500 to-teal-600',
    description: 'Dynamic warmups and movement prep',
    filter: (ex: any) => ex.family?.includes('Mobility') || ex.family?.includes('Prep'),
    count: 0
  },
  { 
    id: 'power', 
    name: 'Power Development', 
    icon: TrendingUp,
    color: 'from-orange-500 to-red-600',
    description: 'Ballistic, plyo, and speed work',
    filter: (ex: any) => ['Ball', 'Plyo', 'Sprint'].some(k => ex.family?.includes(k)),
    count: 0
  },
  { 
    id: 'upper', 
    name: 'Upper Body', 
    icon: Activity,
    color: 'from-blue-500 to-indigo-600',
    description: 'Push, pull, and shoulder health',
    filter: (ex: any) => ['HPush', 'HPull', 'VPush', 'VPull'].some(k => ex.family?.includes(k)),
    count: 0
  },
  { 
    id: 'lower', 
    name: 'Lower Body', 
    icon: Target,
    color: 'from-purple-500 to-pink-600',
    description: 'Squat, hinge, and unilateral work',
    filter: (ex: any) => ['DLKD', 'DLHD', 'SLKD', 'SLHD'].some(k => ex.family?.includes(k)),
    count: 0
  },
  { 
    id: 'core', 
    name: 'Core & Carry', 
    icon: Target,
    color: 'from-cyan-500 to-blue-600',
    description: 'Anti-rotation, bracing, and loaded carries',
    filter: (ex: any) => ['Core', 'Carry', 'Rot'].some(k => ex.family?.includes(k)),
    count: 0
  },
];

interface HomePageProps {
  onSelectSource: (sourceId: string) => void;
  onSelectTemplate: (template: TemplateType) => void;
  onStartFresh: () => void;
  onStartTeamTemplate: () => void;
  onOpenLibrary: () => void;
  onOpenWorkout?: () => void;
  savedPrograms: SavedProgramArtifact[];
}

interface FavoriteExercise {
  id: string;
  name: string;
  family: string;
}

interface RecentWorkout {
  id: string;
  name: string;
  date: string;
  athlete: string;
  sport: string;
}

export function HomePage({ 
  onSelectSource, 
  onSelectTemplate, 
  onStartFresh, 
  onStartTeamTemplate, 
  onOpenLibrary,
  onOpenWorkout,
  savedPrograms 
}: HomePageProps) {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [templateOpen, setTemplateOpen] = useState(false);
  const [libraryOpen, setLibraryOpen] = useState(false);
  const [favorites, setFavorites] = useState<FavoriteExercise[]>([]);
  const [recentWorkouts, setRecentWorkouts] = useState<RecentWorkout[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [collectionCounts, setCollectionCounts] = useState<Record<string, number>>({});
  const [allExercises, setAllExercises] = useState<Exercise[]>([]);

  // Load all exercises on mount
  useEffect(() => {
    exerciseService.getExercises().then(setAllExercises).catch(console.error);
  }, []);

  // Load favorites from localStorage
  useEffect(() => {
    const stored = localStorage.getItem('forge_favorites');
    if (stored && allExercises.length > 0) {
      try {
        const favIds = JSON.parse(stored);
        const favExercises = allExercises
          .filter(ex => favIds.includes(ex.id.toString()))
          .slice(0, 8)
          .map(ex => ({ id: ex.id.toString(), name: ex.name, family: ex.family }));
        setFavorites(favExercises);
      } catch (e) {
        console.error('Failed to load favorites:', e);
      }
    }
  }, [allExercises]);

  // Calculate collection counts
  useEffect(() => {
    if (allExercises.length === 0) return;
    const counts: Record<string, number> = {};
    SMART_COLLECTIONS.forEach(col => {
      counts[col.id] = allExercises.filter(col.filter).length;
    });
    setCollectionCounts(counts);
  }, [allExercises]);

  // Build recent workouts from saved programs
  useEffect(() => {
    const recent = savedPrograms
      .slice(0, 5)
      .map(prog => ({
        id: prog.id,
        name: `${prog.athlete_display_name} - ${prog.blueprint_label}`,
        date: new Date(prog.updated_at).toLocaleDateString(),
        athlete: prog.athlete_display_name,
        sport: prog.sport,
      }));
    setRecentWorkouts(recent);
  }, [savedPrograms]);

  // Get today's focus based on time of day and day of week
  const getTodaysFocus = () => {
    const now = new Date();
    const hour = now.getHours();
    const day = now.getDay();
    
    // Morning: Mobility & Prep
    if (hour < 12) {
      return {
        title: 'Morning Mobility',
        description: 'Start your day with dynamic movement preparation',
        icon: Zap,
        color: 'from-emerald-500 to-teal-600',
        action: () => handleCollectionClick('mobility'),
      };
    }
    
    // Afternoon: Power & Performance
    if (hour < 17) {
      return {
        title: 'Power Development',
        description: 'Peak performance window - focus on explosive work',
        icon: TrendingUp,
        color: 'from-orange-500 to-red-600',
        action: () => handleCollectionClick('power'),
      };
    }
    
    // Evening: Recovery & Core
    return {
      title: 'Core & Recovery',
      description: 'Build resilience and prepare for tomorrow',
      icon: Target,
      color: 'from-cyan-500 to-blue-600',
      action: () => handleCollectionClick('core'),
    };
  };

  const todaysFocus = getTodaysFocus();
  const FocusIcon = todaysFocus.icon;

  const handleCollectionClick = (collectionId: string) => {
    // Open library with pre-applied filter
    onOpenLibrary();
    // In a real implementation, we'd pass filter params to the library
    console.log('Opening collection:', collectionId);
  };

  const handleFavoriteClick = (exercise: FavoriteExercise) => {
    // Navigate to library with this exercise highlighted
    onOpenLibrary();
    console.log('Viewing favorite:', exercise.name);
  };

  const handleRecentClick = (workout: RecentWorkout) => {
    onSelectSource(workout.id);
  };

  if (libraryOpen) {
    return (
      <div className="h-full flex flex-col">
        <div className="flex items-center justify-between p-4 border-b border-slate-200 bg-white">
          <button
            onClick={() => setLibraryOpen(false)}
            className="flex items-center gap-2 text-slate-600 hover:text-slate-900 transition-colors"
          >
            <ChevronRight className="w-5 h-5 rotate-180" />
            <span className="font-medium">Back to Home</span>
          </button>
          <h2 className="text-lg font-bold text-slate-900">Exercise Library</h2>
          <div className="w-24"></div>
        </div>
        <div className="flex-1 overflow-auto">
          <ExerciseLibrary />
        </div>
      </div>
    );
  }

  return (
    <>
      <div className="min-h-full bg-gradient-to-br from-slate-50 via-white to-indigo-50/30">
        {/* Hero Section - Command Center Header */}
        <div className="bg-gradient-to-r from-indigo-600 via-purple-600 to-indigo-700 text-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
              <div>
                <h1 className="text-3xl sm:text-4xl font-bold mb-2">
                  Good {new Date().getHours() < 12 ? 'Morning' : new Date().getHours() < 17 ? 'Afternoon' : 'Evening'}, Coach
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
                  <div className="text-2xl font-bold">{favorites.length}</div>
                  <div className="text-xs text-indigo-200">Favorites</div>
                </div>
                <div className="bg-white/10 backdrop-blur-sm rounded-xl px-4 py-3 text-center">
                  <div className="text-2xl font-bold">{allExercises.length}</div>
                  <div className="text-xs text-indigo-200">Exercises</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
          
          {/* Today's Focus Card */}
          <div 
            onClick={todaysFocus.action}
            className={`bg-gradient-to-r ${todaysFocus.color} rounded-2xl p-6 text-white cursor-pointer transform transition-all hover:scale-[1.02] hover:shadow-xl shadow-lg`}
          >
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-4">
                <div className="w-14 h-14 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center">
                  <FocusIcon className="w-7 h-7 text-white" />
                </div>
                <div>
                  <h3 className="text-xl font-bold">{todaysFocus.title}</h3>
                  <p className="text-white/90 mt-1">{todaysFocus.description}</p>
                </div>
              </div>
              <ArrowRight className="w-6 h-6 text-white/60 group-hover:text-white transition-colors" />
            </div>
          </div>

          {/* Main Action Buttons */}
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
                <div className="text-sm text-slate-500">{allExercises.length} exercises with full coaching knowledge</div>
              </div>
              <ArrowRight className="w-5 h-5 text-slate-400 group-hover:text-emerald-500 group-hover:translate-x-1 transition-all" />
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

          {/* Smart Collections Grid */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <Filter className="w-5 h-5 text-indigo-600" />
                Smart Collections
              </h3>
              <button 
                onClick={() => setLibraryOpen(true)}
                className="text-sm text-indigo-600 hover:text-indigo-700 font-medium"
              >
                View All →
              </button>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
              {SMART_COLLECTIONS.map((collection) => {
                const Icon = collection.icon;
                return (
                  <button
                    key={collection.id}
                    onClick={() => handleCollectionClick(collection.id)}
                    className="group bg-white border border-slate-200 hover:border-slate-300 rounded-xl p-4 text-left transition-all hover:shadow-md hover:-translate-y-0.5"
                  >
                    <div className={`w-10 h-10 bg-gradient-to-br ${collection.color} rounded-lg flex items-center justify-center mb-3 group-hover:scale-110 transition-transform shadow-sm`}>
                      <Icon className="w-5 h-5 text-white" />
                    </div>
                    <div className="font-semibold text-slate-900 text-sm mb-1">{collection.name}</div>
                    <div className="text-xs text-slate-500 mb-2 line-clamp-2">{collection.description}</div>
                    <div className="text-xs font-medium text-slate-400 bg-slate-100 inline-block px-2 py-1 rounded-full">
                      {collectionCounts[collection.id] || 0} exercises
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Two Column Layout: Favorites + Recent */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            {/* Favorites Section */}
            <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
              <div className="p-4 border-b border-slate-100 flex items-center justify-between">
                <h3 className="font-bold text-slate-900 flex items-center gap-2">
                  <Star className="w-5 h-5 text-yellow-500 fill-yellow-500" />
                  Quick Access Favorites
                </h3>
                <button 
                  onClick={() => setLibraryOpen(true)}
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
                        onClick={() => handleFavoriteClick(ex)}
                        className="group p-3 bg-slate-50 hover:bg-indigo-50 border border-slate-200 hover:border-indigo-300 rounded-lg text-left transition-all hover:shadow-sm"
                      >
                        <div className="font-medium text-sm text-slate-900 group-hover:text-indigo-900 truncate">
                          {ex.name}
                        </div>
                        <div className="text-xs text-slate-500 group-hover:text-slate-600 mt-1">
                          {ex.family}
                        </div>
                      </button>
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <Star className="w-8 h-8 text-slate-300 mx-auto mb-2" />
                    <p className="text-sm text-slate-500 mb-3">No favorites yet</p>
                    <button
                      onClick={() => setLibraryOpen(true)}
                      className="text-sm text-indigo-600 hover:text-indigo-700 font-medium"
                    >
                      Browse exercises to add favorites →
                    </button>
                  </div>
                )}
              </div>
            </div>

            {/* Recent Workouts Section */}
            <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
              <div className="p-4 border-b border-slate-100 flex items-center justify-between">
                <h3 className="font-bold text-slate-900 flex items-center gap-2">
                  <Clock className="w-5 h-5 text-blue-500" />
                  Recent Programs
                </h3>
                <button 
                  onClick={() => setDrawerOpen(true)}
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
                      onClick={() => handleRecentClick(workout)}
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
          </div>

          {/* Role Templates Section */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                <Users className="w-5 h-5 text-indigo-600" />
                Start from Role Template
              </h3>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {TEMPLATES.map(t => (
                <button
                  key={t.id}
                  onClick={() => onSelectTemplate(t.id)}
                  className="group bg-white border border-slate-200 hover:border-indigo-300 hover:bg-indigo-50/50 rounded-xl p-5 text-left transition-all hover:shadow-md"
                >
                  <div className="text-3xl mb-3">{t.icon}</div>
                  <div className="font-bold text-slate-900 group-hover:text-indigo-900 mb-1">
                    {t.sport}
                  </div>
                  <div className="text-sm font-medium text-indigo-600 mb-2">{t.role}</div>
                  <div className="text-xs text-slate-500 line-clamp-2">{t.description}</div>
                  <div className="mt-3 flex items-center gap-2">
                    <span className="text-xs font-medium text-slate-400 bg-slate-100 px-2 py-1 rounded-full">
                      {t.category}
                    </span>
                    <ArrowRight className="w-3 h-3 text-slate-300 group-hover:text-indigo-500 transition-colors" />
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Start Fresh Link */}
          <div className="text-center pt-4 pb-8">
            <button
              onClick={onStartFresh}
              className="text-sm text-slate-500 hover:text-indigo-600 transition-colors flex items-center justify-center gap-2 group"
            >
              <Plus className="w-4 h-4 group-hover:scale-110 transition-transform" />
              Start Fresh — build from scratch
            </button>
          </div>
        </div>
      </div>

      {/* Saved Programs Drawer */}
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
