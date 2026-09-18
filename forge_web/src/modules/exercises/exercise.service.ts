/**
 * Exercise Library API Service
 * Modular service for fetching and filtering exercises
 * Uses lazy-loaded JSON data for better initial bundle size
 */

export interface Exercise {
  id: number | string;
  name: string;
  category: string;
  subcategory: string;
  movement_pattern: string;
  equipment: string;
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
  source_organization: string;
  description: string;
  coaching_cues: string[];
  common_errors: string[];
  contraindications: string[];
  regressions: string[];
  progressions: string[];
  equipment_alternatives: string[];
  is_pain_safe: boolean;
  created_at: string;
}

export interface ExerciseFilters {
  category?: string;
  subcategory?: string;
  movement_pattern?: string;
  equipment?: string;
  difficulty?: string;
  source_organization?: string;
  is_pain_safe?: boolean;
  search?: string;
  search_query?: string;
  difficulty_level?: string;
  force_vector?: string;
  has_coaching_cues?: boolean;
}

const USE_LOCAL_DATA = true; // Offline-first: use local JSON by default

// Lazy load exercises data - will be loaded on first call
let exercisesCache: Exercise[] | null = null;
let exercisesLoadPromise: Promise<Exercise[]> | null = null;

async function getExercisesData(): Promise<Exercise[]> {
  if (exercisesCache) {
    return exercisesCache;
  }
  
  if (!exercisesLoadPromise) {
    exercisesLoadPromise = import('../../data/exercises.json')
      .then(module => {
        exercisesCache = module.default as Exercise[];
        return exercisesCache;
      })
      .catch(error => {
        console.error('Failed to load exercises data:', error);
        throw new Error('Failed to load exercise library');
      });
  }
  
  return exercisesLoadPromise;
}

export const exerciseService = {
  /**
   * Fetch all exercises with optional filters
   * Uses local data by default, falls back to API if needed
   */
  async getExercises(filters?: ExerciseFilters): Promise<Exercise[]> {
    try {
      const exercises = await getExercisesData();
      // Apply client-side filtering
      return filterExercises(exercises, filters || {});
    } catch (error) {
      console.error('Error fetching exercises:', error);
      throw error;
    }
  },

  /**
   * Fetch a single exercise by ID
   */
  async getExerciseById(id: number | string): Promise<Exercise> {
    try {
      const exercises = await getExercisesData();
      const exercise = exercises.find((e: Exercise) => String(e.id) === String(id));
      if (!exercise) throw new Error('Exercise not found');
      return exercise;
    } catch (error) {
      console.error(`Error fetching exercise ${id}:`, error);
      throw error;
    }
  },

  /**
   * Get unique values for filter dropdowns
   */
  async getFilterOptions(): Promise<{
    categories: string[];
    movementPatterns: string[];
    equipment: string[];
    difficulties: string[];
    sources: string[];
  }> {
    try {
      const exercises = await getExercisesData();
      return {
        categories: [...new Set(exercises.map(e => e.category))].sort(),
        movementPatterns: [...new Set(exercises.map(e => e.movement_pattern))].sort(),
        equipment: [...new Set(exercises.flatMap(e => e.equipment.split(', ')))].sort().filter(Boolean),
        difficulties: [...new Set(exercises.map(e => e.difficulty))].sort(),
        sources: [...new Set(exercises.map(e => e.source_organization))].sort(),
      };
    } catch (error) {
      console.error('Error fetching filter options:', error);
      return {
        categories: [],
        movementPatterns: [],
        equipment: [],
        difficulties: [],
        sources: [],
      };
    }
  },

  /**
   * Search exercises by name or description
   */
  async searchExercises(query: string): Promise<Exercise[]> {
    try {
      const exercises = await getExercisesData();
      const queryLower = query.toLowerCase();
      
      return exercises.filter(exercise => 
        exercise.name.toLowerCase().includes(queryLower) ||
        exercise.description.toLowerCase().includes(queryLower) ||
        exercise.category.toLowerCase().includes(queryLower) ||
        exercise.equipment.toLowerCase().includes(queryLower)
      );
    } catch (error) {
      console.error('Error searching exercises:', error);
      return [];
    }
  },

  /**
   * Get pain-safe exercises for return-to-play
   */
  async getPainSafeExercises(): Promise<Exercise[]> {
    const exercises = await getExercisesData();
    return filterExercises(exercises, { is_pain_safe: true });
  },

  /**
   * Get exercises by movement pattern
   */
  async getByMovementPattern(pattern: string): Promise<Exercise[]> {
    const exercises = await getExercisesData();
    return filterExercises(exercises, { movement_pattern: pattern });
  },

  /**
   * Get exercises by category
   */
  async getByCategory(category: string): Promise<Exercise[]> {
    const exercises = await getExercisesData();
    return filterExercises(exercises, { category });
  },
};

/**
 * Client-side filtering function
 */
function filterExercises(exercises: Exercise[], filters: ExerciseFilters): Exercise[] {
  return exercises.filter(exercise => {
    if (filters.category && exercise.category !== filters.category) return false;
    if (filters.subcategory && exercise.subcategory !== filters.subcategory) return false;
    if (filters.movement_pattern && exercise.movement_pattern !== filters.movement_pattern) return false;
    if (filters.difficulty && exercise.difficulty !== filters.difficulty) return false;
    if (filters.difficulty_level && exercise.difficulty !== filters.difficulty_level) return false;
    if (filters.is_pain_safe !== undefined && exercise.is_pain_safe !== filters.is_pain_safe) return false;
    if (filters.equipment && !exercise.equipment.toLowerCase().includes(filters.equipment.toLowerCase())) return false;
    if (filters.source_organization && !exercise.source_organization.includes(filters.source_organization)) return false;
    if (filters.force_vector && exercise.movement_pattern !== filters.force_vector) return false;
    if (filters.has_coaching_cues && (!exercise.coaching_cues || exercise.coaching_cues.length === 0)) return false;
    
    // Search across multiple fields
    const searchTerm = (filters.search || filters.search_query || '').toLowerCase();
    if (searchTerm) {
      const matchesName = exercise.name.toLowerCase().includes(searchTerm);
      const matchesCategory = exercise.category.toLowerCase().includes(searchTerm);
      const matchesEquipment = exercise.equipment.toLowerCase().includes(searchTerm);
      const matchesDescription = exercise.description.toLowerCase().includes(searchTerm);
      if (!matchesName && !matchesCategory && !matchesEquipment && !matchesDescription) return false;
    }
    return true;
  });
}

export default exerciseService;
