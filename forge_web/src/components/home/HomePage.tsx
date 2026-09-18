import React, { useState, useEffect } from 'react';
import { ChevronRight } from 'lucide-react';
import { SavedProgramArtifact } from '../../types/ui';
import { SavedProgramsDrawer } from '../program/SavedProgramsDrawer';
import ExerciseLibrary from '../../modules/exercises/ExerciseLibrary';
import exerciseService, { Exercise } from '../../modules/exercises/exercise.service';
import { HomePageHeader } from './HomePageHeader';
import { HomePageActions } from './HomePageActions';
import { SmartCollectionsGrid, SmartCollection } from './SmartCollectionsGrid';
import { RecentWorkoutsSection, FavoriteExercisesSection, RecentWorkout, FavoriteExercise } from './RecentWorkoutsSection';
import { RoleTemplatesSection, TemplateInfo } from './RoleTemplatesSection';
import { Zap, TrendingUp, Activity, Target } from 'lucide-react';

export type TemplateType = 'rugby_prop' | 'tennis_singles' | 'cricket_bowler';

const TEMPLATES: TemplateInfo[] = [
  { id: 'rugby_prop', sport: 'Rugby Union', role: 'Tighthead Prop', description: 'Max Force & Scrum Dominance — collision sport profile', icon: '🏉', category: 'Strength' },
  { id: 'tennis_singles', sport: 'Tennis', role: 'Singles Player', description: 'Court Speed & Change of Direction — court sport profile', icon: '🎾', category: 'Power' },
  { id: 'cricket_bowler', sport: 'Cricket', role: 'Fast Bowler', description: 'Eccentric Tolerance & Delivery Velocity — field sport profile', icon: '🏏', category: 'Power' },
];

const SMART_COLLECTIONS: SmartCollection[] = [
  { 
    id: 'mobility', 
    name: 'Mobility & Prep', 
    icon: Zap,
    color: 'from-emerald-500 to-teal-600',
    description: 'Dynamic warmups and movement prep',
    filter: (ex: any) => ex.category === 'Activation' || ex.subcategory?.includes('Mobility'),
  },
  { 
    id: 'power', 
    name: 'Power Development', 
    icon: TrendingUp,
    color: 'from-orange-500 to-red-600',
    description: 'Ballistic, plyo, and speed work',
    filter: (ex: any) => ['Ball', 'Plyo', 'Landing'].includes(ex.category) || ex.category === 'Explosive Performance',
  },
  { 
    id: 'upper', 
    name: 'Upper Body', 
    icon: Activity,
    color: 'from-blue-500 to-indigo-600',
    description: 'Push, pull, and shoulder health',
    filter: (ex: any) => ['HPush', 'VPush', 'HPull', 'VPull'].includes(ex.category),
  },
  { 
    id: 'lower', 
    name: 'Lower Body', 
    icon: Target,
    color: 'from-purple-500 to-pink-600',
    description: 'Squat, hinge, and unilateral work',
    filter: (ex: any) => ['DLKD', 'DLHD', 'SLKD', 'SLHD'].includes(ex.category),
  },
  { 
    id: 'core', 
    name: 'Core & Carry', 
    icon: Target,
    color: 'from-cyan-500 to-blue-600',
    description: 'Anti-rotation, bracing, and loaded carries',
    filter: (ex: any) => ['Core', 'Carry', 'Rot'].includes(ex.category),
  },
];

interface HomePageProps {
  onSelectSource: (sourceId: string) => void;
  onSelectTemplate: (template: TemplateType) => void;
  onStartFresh: () => void;
  onStartTeamTemplate: () => void;
  onOpenLibrary: () => void;
  onOpenComplexes?: () => void;
  onOpenWorkout?: () => void;
  savedPrograms: SavedProgramArtifact[];
}

interface TodaysFocus {
  title: string;
  description: string;
  icon: React.ComponentType<{ className?: string }>;
  color: string;
  action: () => void;
}

export function HomePage({ 
  onSelectSource, 
  onSelectTemplate, 
  onStartFresh, 
  onStartTeamTemplate, 
  onOpenLibrary,
  onOpenComplexes,
  onOpenWorkout,
  savedPrograms 
}: HomePageProps) {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const [libraryOpen, setLibraryOpen] = useState(false);
  const [favorites, setFavorites] = useState<FavoriteExercise[]>([]);
  const [recentWorkouts, setRecentWorkouts] = useState<RecentWorkout[]>([]);
  const [collectionCounts, setCollectionCounts] = useState<Record<string, number>>({});
  const [allExercises, setAllExercises] = useState<Exercise[]>([]);

  useEffect(() => {
    exerciseService.getExercises().then(setAllExercises).catch(console.error);
  }, []);

  useEffect(() => {
    const stored = localStorage.getItem('forge_favorites');
    if (stored && allExercises.length > 0) {
      try {
        const favIds = JSON.parse(stored);
        const favExercises = allExercises
          .filter(ex => favIds.includes(ex.id.toString()))
          .slice(0, 8)
          .map(ex => ({ id: ex.id.toString(), name: ex.name, category: ex.category }));
        setFavorites(favExercises);
      } catch (e) {
        console.error('Failed to load favorites:', e);
      }
    }
  }, [allExercises]);

  useEffect(() => {
    if (allExercises.length === 0) return;
    const counts: Record<string, number> = {};
    SMART_COLLECTIONS.forEach(col => {
      counts[col.id] = allExercises.filter(col.filter).length;
    });
    setCollectionCounts(counts);
  }, [allExercises]);

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

  const getTodaysFocus = (): TodaysFocus => {
    const hour = new Date().getHours();
    
    if (hour < 12) {
      return {
        title: 'Morning Mobility',
        description: 'Start your day with dynamic movement preparation',
        icon: Zap,
        color: 'from-emerald-500 to-teal-600',
        action: () => handleCollectionClick('mobility'),
      };
    }
    
    if (hour < 17) {
      return {
        title: 'Power Development',
        description: 'Peak performance window - focus on explosive work',
        icon: TrendingUp,
        color: 'from-orange-500 to-red-600',
        action: () => handleCollectionClick('power'),
      };
    }
    
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
    onOpenLibrary();
    console.log('Opening collection:', collectionId);
  };

  const handleFavoriteClick = (exercise: FavoriteExercise) => {
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
        <HomePageHeader 
          savedPrograms={savedPrograms}
          favoritesLength={favorites.length}
          allExercisesLength={allExercises.length}
        />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
          
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
              <Activity className="w-6 h-6 text-white/60 group-hover:text-white transition-colors" />
            </div>
          </div>

          <HomePageActions
            allExercisesLength={allExercises.length}
            onStartTeamTemplate={onStartTeamTemplate}
            onOpenLibrary={onOpenLibrary}
            onOpenComplexes={onOpenComplexes}
            onOpenWorkout={onOpenWorkout}
            setLibraryOpen={setLibraryOpen}
          />

          <SmartCollectionsGrid
            smartCollections={SMART_COLLECTIONS}
            collectionCounts={collectionCounts}
            onCollectionClick={handleCollectionClick}
            onOpenLibrary={onOpenLibrary}
          />

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <FavoriteExercisesSection
              favorites={favorites}
              onFavoriteClick={handleFavoriteClick}
              onOpenLibrary={onOpenLibrary}
            />
            <RecentWorkoutsSection
              recentWorkouts={recentWorkouts}
              onRecentClick={handleRecentClick}
              onDrawerOpen={() => setDrawerOpen(true)}
              onStartTeamTemplate={onStartTeamTemplate}
            />
          </div>

          <RoleTemplatesSection
            templates={TEMPLATES}
            onSelectTemplate={onSelectTemplate}
            onStartFresh={onStartFresh}
          />
        </div>
      </div>

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
