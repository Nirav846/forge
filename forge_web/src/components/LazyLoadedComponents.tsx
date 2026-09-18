/**
 * Lazy-loaded Exercise Library with Suspense
 * Improves initial load time by code-splitting the heavy exercise library
 */
import { lazy, Suspense, useState, useEffect } from 'react';

// Lazy import the exercise library
const ExerciseLibraryLazy = lazy(() => 
  import('../modules/exercises/ExerciseLibrary').then(module => ({
    default: module.default
  }))
);

// Lazy import complexes library
const ComplexesLibraryLazy = lazy(() => 
  import('../components/ComplexesLibrary').then(module => ({
    default: module.default
  }))
);

// Lazy import workout builder
const WorkoutBuilderLazy = lazy(() => 
  import('../components/WorkoutBuilder').then(module => ({
    default: module.default
  }))
);

interface LoadingFallbackProps {
  message?: string;
}

function LoadingFallback({ message = 'Loading...' }: LoadingFallbackProps) {
  return (
    <div className="flex flex-col items-center justify-center h-full min-h-[400px] bg-gray-50">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
      <p className="text-gray-600 font-medium">{message}</p>
      <p className="text-sm text-gray-500 mt-2">Loading exercise data...</p>
    </div>
  );
}

interface LazyExerciseLibraryProps {
  onExit?: () => void;
}

export function LazyExerciseLibrary({ onExit }: LazyExerciseLibraryProps) {
  const [loadError, setLoadError] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState(0);

  // Clear error on retry
  useEffect(() => {
    if (retryCount > 0) {
      setLoadError(null);
    }
  }, [retryCount]);

  if (loadError) {
    return (
      <div className="flex flex-col items-center justify-center h-full min-h-[400px] bg-red-50">
        <div className="text-red-500 text-5xl mb-4">⚠️</div>
        <h3 className="text-lg font-bold text-red-800 mb-2">Failed to load Exercise Library</h3>
        <p className="text-red-600 mb-4">{loadError}</p>
        <button
          onClick={() => setRetryCount(prev => prev + 1)}
          className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <Suspense fallback={<LoadingFallback message="Loading Exercise Library..." />}>
      <ExerciseLibraryLazy 
        key={`exercise-lib-${retryCount}`} 
        onExit={onExit} 
        onError={(error: any) => {
          console.error('Exercise Library failed to load:', error);
          setLoadError(error?.message || 'Unknown error occurred');
        }}
      />
    </Suspense>
  );
}

interface LazyComplexesLibraryProps {
  onExit?: () => void;
}

export function LazyComplexesLibrary({ onExit }: LazyComplexesLibraryProps) {
  const [loadError, setLoadError] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState(0);

  if (loadError) {
    return (
      <div className="flex flex-col items-center justify-center h-full min-h-[400px] bg-red-50">
        <div className="text-red-500 text-5xl mb-4">⚠️</div>
        <h3 className="text-lg font-bold text-red-800 mb-2">Failed to load Complexes Library</h3>
        <p className="text-red-600 mb-4">{loadError}</p>
        <button
          onClick={() => setRetryCount(prev => prev + 1)}
          className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <Suspense fallback={<LoadingFallback message="Loading Complexes Library..." />}>
      <ComplexesLibraryLazy 
        key={`complexes-lib-${retryCount}`} 
        onExit={onExit}
      />
    </Suspense>
  );
}

interface LazyWorkoutBuilderProps {
  onExit?: () => void;
}

export function LazyWorkoutBuilder({ onExit }: LazyWorkoutBuilderProps) {
  const [loadError, setLoadError] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState(0);

  if (loadError) {
    return (
      <div className="flex flex-col items-center justify-center h-full min-h-[400px] bg-red-50">
        <div className="text-red-500 text-5xl mb-4">⚠️</div>
        <h3 className="text-lg font-bold text-red-800 mb-2">Failed to load Workout Builder</h3>
        <p className="text-red-600 mb-4">{loadError}</p>
        <button
          onClick={() => setRetryCount(prev => prev + 1)}
          className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <Suspense fallback={<LoadingFallback message="Loading Workout Builder..." />}>
      <WorkoutBuilderLazy 
        key={`workout-builder-${retryCount}`} 
        onExit={onExit}
      />
    </Suspense>
  );
}
