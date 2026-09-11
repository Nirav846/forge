/**
 * Exercise Library API Service
 * Modular service for fetching and filtering exercises
 */

import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000/api/v1';

export interface Exercise {
  id: number;
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
}

export const exerciseService = {
  /**
   * Fetch all exercises with optional filters
   */
  async getExercises(filters?: ExerciseFilters): Promise<Exercise[]> {
    try {
      const params = new URLSearchParams();
      
      if (filters) {
        Object.entries(filters).forEach(([key, value]) => {
          if (value !== undefined && value !== '') {
            params.append(key, String(value));
          }
        });
      }

      const response = await axios.get(`${API_BASE}/exercises?${params.toString()}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching exercises:', error);
      throw error;
    }
  },

  /**
   * Fetch a single exercise by ID
   */
  async getExerciseById(id: number): Promise<Exercise> {
    try {
      const response = await axios.get(`${API_BASE}/exercises/${id}`);
      return response.data;
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
      const exercises = await this.getExercises();
      
      return {
        categories: [...new Set(exercises.map(e => e.category))].sort(),
        movementPatterns: [...new Set(exercises.map(e => e.movement_pattern))].sort(),
        equipment: [...new Set(exercises.map(e => e.equipment))].sort(),
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
      const response = await axios.get(`${API_BASE}/exercises/search?q=${encodeURIComponent(query)}`);
      return response.data;
    } catch (error) {
      console.error('Error searching exercises:', error);
      return [];
    }
  },

  /**
   * Get pain-safe exercises for return-to-play
   */
  async getPainSafeExercises(): Promise<Exercise[]> {
    return this.getExercises({ is_pain_safe: true });
  },

  /**
   * Get exercises by movement pattern
   */
  async getByMovementPattern(pattern: string): Promise<Exercise[]> {
    return this.getExercises({ movement_pattern: pattern });
  },

  /**
   * Get exercises by category
   */
  async getByCategory(category: string): Promise<Exercise[]> {
    return this.getExercises({ category });
  },
};

export default exerciseService;
