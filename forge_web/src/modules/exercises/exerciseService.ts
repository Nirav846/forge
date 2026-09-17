/**
 * Exercise Library API Service - Legacy Compatibility Layer
 * Provides fetchExercises and other exports for backward compatibility
 */

import exerciseService, { Exercise, ExerciseFilters } from './exercise.service';

export type { Exercise, ExerciseFilters };

export const EXERCISE_CATEGORIES = [
  'DLKD', 'DLHD', 'SLKD', 'SLHD',
  'HPush', 'VPush', 'HPull', 'VPull',
  'Core', 'Carry', 'Rot',
  'Plyo', 'Landing', 'Ball',
  'Explosive Performance',
  'Sprint', 'Acc', 'Agility',
  'Activation', 'Assessment', 'Cond', 'Recovery'
];

export const DIFFICULTY_LEVELS = ['Beginner', 'Intermediate', 'Advanced'];

export const FORCE_VECTORS = [
  'Vertical', 'Horizontal', 'Rotational', 'Multi-planar', 'N/A'
];

export const SOURCE_ORGANIZATIONS = [
  'NSCA', 'NASM', 'ACE', 'ACSM', 'EXOS', 'PhysiApp', 'Custom'
];

export function getDifficultyColor(difficulty: string): string {
  switch (difficulty) {
    case 'Beginner': return 'bg-green-100 text-green-700 border-green-200';
    case 'Intermediate': return 'bg-blue-100 text-blue-700 border-blue-200';
    case 'Advanced': return 'bg-orange-100 text-orange-700 border-orange-200';
    default: return 'bg-gray-100 text-gray-700 border-gray-200';
  }
}

export function getCategoryIcon(category: string): string {
  const icons: Record<string, string> = {
    'DLKD': '🦵', 'DLHD': '🍑', 'SLKD': '🦵', 'SLHD': '🍑',
    'HPush': '👊', 'VPush': '🙌', 'HPull': '🤸', 'VPull': '🧗',
    'Core': '🎯', 'Carry': '🏋️', 'Rot': '🔄',
    'Plyo': '💥', 'Landing': '🛬', 'Ball': '🏀',
    'Explosive Performance': '⚡',
    'Sprint': '🏃', 'Acc': '🚀', 'Agility': '⚡',
    'Activation': '🔌', 'Assessment': '📊', 'Cond': '❤️', 'Recovery': '🧘'
  };
  return icons[category] || '📋';
}

export async function fetchExercises(filters?: ExerciseFilters): Promise<Exercise[]> {
  return exerciseService.getExercises(filters);
}

export async function fetchExerciseById(id: number | string): Promise<Exercise> {
  return exerciseService.getExerciseById(id);
}

export async function fetchFilterOptions(): Promise<{
  categories: string[];
  movementPatterns: string[];
  equipment: string[];
  difficulties: string[];
  sources: string[];
}> {
  return exerciseService.getFilterOptions();
}

export default exerciseService;
