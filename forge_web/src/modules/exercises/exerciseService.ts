/**
 * Exercise Library Module - FORGE S&C System
 * 
 * Provides comprehensive exercise browsing, filtering, and search capabilities
 * for CSCS-certified coaches.
 */

export interface Exercise {
  id: number;
  name: string;
  category: string;
  subcategory: string;
  force_vector: string;
  equipment_needed: string;
  difficulty_level: string;
  source_organization: string;
  coaching_cues: string[];
  common_errors: string[];
  contraindications: string[];
  regressions: string[];
  progressions: string[];
  equipment_alternatives: string[];
  created_at: string;
}

export interface ExerciseFilters {
  category?: string;
  subcategory?: string;
  force_vector?: string;
  difficulty_level?: string;
  equipment?: string;
  source?: string;
  search_query?: string;
}

export const EXERCISE_CATEGORIES = [
  'Olympic',
  'Barbell Variation',
  'Loaded Carry',
  'Core',
  'Plyometric',
  'Deceleration/COD',
  'Gymnastics',
  'Strongman',
  'Conditioning',
  'MetCon',
  'Power',
  'Rehab/Prehab',
  'Posterior Chain'
];

export const DIFFICULTY_LEVELS = [
  'Beginner',
  'Intermediate',
  'Advanced',
  'Elite'
];

export const FORCE_VECTORS = [
  'Vertical',
  'Horizontal',
  'Multi-planar',
  'Rotation'
];

export const SOURCE_ORGANIZATIONS = [
  'NSCA',
  'UKSCA',
  'EXOS',
  'ALTIS',
  'USAW',
  'StrongFirst',
  'McGill',
  'UEFA Medical',
  'IOC Research',
  'NFL Combine',
  'Gymnastics',
  'FIG',
  'USAG',
  'Strongman Corp',
  'CrossFit',
  'Westside',
  'Brooks'
];

export async function fetchExercises(filters?: ExerciseFilters): Promise<Exercise[]> {
  const params = new URLSearchParams();
  
  if (filters) {
    if (filters.category) params.append('category', filters.category);
    if (filters.subcategory) params.append('subcategory', filters.subcategory);
    if (filters.force_vector) params.append('force_vector', filters.force_vector);
    if (filters.difficulty_level) params.append('difficulty_level', filters.difficulty_level);
    if (filters.equipment) params.append('equipment', filters.equipment);
    if (filters.source) params.append('source', filters.source);
    if (filters.search_query) params.append('search', filters.search_query);
  }
  
  const response = await fetch(`/api/exercises?${params.toString()}`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch exercises');
  }
  
  return response.json();
}

export async function fetchExerciseById(id: number): Promise<Exercise> {
  const response = await fetch(`/api/exercises/${id}`);
  
  if (!response.ok) {
    throw new Error('Failed to fetch exercise');
  }
  
  return response.json();
}

export function filterExercises(exercises: Exercise[], filters: ExerciseFilters): Exercise[] {
  return exercises.filter(exercise => {
    if (filters.category && exercise.category !== filters.category) return false;
    if (filters.subcategory && exercise.subcategory !== filters.subcategory) return false;
    if (filters.force_vector && exercise.force_vector !== filters.force_vector) return false;
    if (filters.difficulty_level && exercise.difficulty_level !== filters.difficulty_level) return false;
    if (filters.equipment && !exercise.equipment_needed.toLowerCase().includes(filters.equipment.toLowerCase())) return false;
    if (filters.source && !exercise.source_organization.includes(filters.source)) return false;
    if (filters.search_query) {
      const query = filters.search_query.toLowerCase();
      const matchesName = exercise.name.toLowerCase().includes(query);
      const matchesCategory = exercise.category.toLowerCase().includes(query);
      const matchesEquipment = exercise.equipment_needed.toLowerCase().includes(query);
      if (!matchesName && !matchesCategory && !matchesEquipment) return false;
    }
    return true;
  });
}

export function getDifficultyColor(level: string): string {
  switch (level) {
    case 'Beginner': return 'text-green-600 bg-green-100';
    case 'Intermediate': return 'text-blue-600 bg-blue-100';
    case 'Advanced': return 'text-orange-600 bg-orange-100';
    case 'Elite': return 'text-red-600 bg-red-100';
    default: return 'text-gray-600 bg-gray-100';
  }
}

export function getCategoryIcon(category: string): string {
  const icons: Record<string, string> = {
    'Olympic': '🏋️',
    'Barbell Variation': '💪',
    'Loaded Carry': '🚶',
    'Core': '🎯',
    'Plyometric': '⚡',
    'Deceleration/COD': '🔄',
    'Gymnastics': '🤸',
    'Strongman': '🪨',
    'Conditioning': '🏃',
    'MetCon': '🔥',
    'Power': '💥',
    'Rehab/Prehab': '🏥',
    'Posterior Chain': '🦵'
  };
  return icons[category] || '📋';
}
