'use client';

import React, { useState, useEffect } from 'react';

export interface ComplexExercise {
  id: string;
  sets: number;
  reps: string;
  rest: number;
}

export interface Complex {
  id: string;
  name: string;
  sport: string;
  role: string;
  plane: string;
  intent: string;
  focus: string;
  description: string;
  exercises: ComplexExercise[];
  coachingNotes: string;
  equipment: string[];
}

class ComplexService {
  private complexes: Complex[] = [];
  private loaded = false;

  async loadComplexes(): Promise<void> {
    if (this.loaded) return;
    
    try {
      const response = await fetch('./data/complexes.json');
      if (!response.ok) throw new Error('Failed to load complexes');
      this.complexes = await response.json();
      this.loaded = true;
    } catch (error) {
      console.error('Error loading complexes:', error);
      throw error;
    }
  }

  async getComplexes(filters?: {
    sport?: string;
    role?: string;
    plane?: string;
    intent?: string;
  }): Promise<Complex[]> {
    await this.loadComplexes();
    
    let filtered = [...this.complexes];
    
    if (filters?.sport) {
      filtered = filtered.filter(c => c.sport === filters.sport);
    }
    if (filters?.role) {
      filtered = filtered.filter(c => c.role === filters.role);
    }
    if (filters?.plane) {
      filtered = filtered.filter(c => c.plane === filters.plane);
    }
    if (filters?.intent) {
      filtered = filtered.filter(c => c.intent === filters.intent);
    }
    
    return filtered;
  }

  async getComplexById(id: string): Promise<Complex | undefined> {
    await this.loadComplexes();
    return this.complexes.find(c => c.id === id);
  }

  async getSports(): Promise<string[]> {
    await this.loadComplexes();
    return [...new Set(this.complexes.map(c => c.sport))].sort();
  }

  async getRoles(sport?: string): Promise<string[]> {
    await this.loadComplexes();
    let roles = this.complexes.map(c => c.role);
    if (sport) {
      roles = this.complexes.filter(c => c.sport === sport).map(c => c.role);
    }
    return [...new Set(roles)].sort();
  }

  async getPlanes(): Promise<string[]> {
    await this.loadComplexes();
    return [...new Set(this.complexes.map(c => c.plane))].sort();
  }

  async getIntents(): Promise<string[]> {
    await this.loadComplexes();
    return [...new Set(this.complexes.map(c => c.intent))].sort();
  }

  async getFilterOptions() {
    await this.loadComplexes();
    return {
      sports: [...new Set(this.complexes.map(c => c.sport))].sort(),
      roles: [...new Set(this.complexes.map(c => c.role))].sort(),
      planes: [...new Set(this.complexes.map(c => c.plane))].sort(),
      intents: [...new Set(this.complexes.map(c => c.intent))].sort(),
    };
  }
}

export const complexService = new ComplexService();
