'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { DndContext, closestCenter, KeyboardSensor, PointerSensor, useSensor, useSensors, DragEndEvent } from '@dnd-kit/core';
import { arrayMove, SortableContext, sortableKeyboardCoordinates, verticalListSortingStrategy, useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { GripVertical, Trash2, Plus, Save, Printer, X, Activity, Clock, Target } from 'lucide-react';

interface WorkoutExercise {
  id: string;
  name: string;
  category?: string;
  sets: number;
  reps: string;
  load: string;
  rest: number; // in seconds
  notes: string;
}

interface WorkoutSession {
  id: string;
  name: string;
  focus: string;
  duration: string;
  exercises: WorkoutExercise[];
  lastModified: number;
}

interface WorkoutBuilderProps {
  onSave?: (workout: WorkoutSession) => void;
  onExit?: () => void;
  initialWorkout?: WorkoutSession | null;
}

const DEFAULT_WORKOUT: WorkoutSession = {
  id: '',
  name: '',
  focus: '',
  duration: '',
  exercises: [],
  lastModified: Date.now(),
};

function SortableExerciseRow({ 
  exercise, 
  onChange, 
  onRemove, 
  attributes 
}: { 
  exercise: WorkoutExercise; 
  onChange: (id: string, field: keyof WorkoutExercise, value: any) => void;
  onRemove: (id: string) => void;
  attributes: any;
}) {
  const { attributes: sortableAttributes, listeners, setNodeRef, transform, transition, isDragging } = useSortable({ id: exercise.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
    opacity: isDragging ? 0.5 : 1,
  };

  return (
    <div ref={setNodeRef} style={style} className="flex items-center gap-2 p-3 bg-white border border-gray-200 rounded-lg mb-2 hover:shadow-md transition-shadow">
      <button {...sortableAttributes} {...listeners} className="p-2 text-gray-400 hover:text-gray-600 cursor-grab active:cursor-grabbing">
        <GripVertical size={18} />
      </button>
      
      <div className="flex-1 grid grid-cols-1 md:grid-cols-6 gap-3 items-center">
        <div className="md:col-span-2 font-medium text-gray-800 truncate" title={exercise.name}>
          {exercise.name}
          {exercise.category && (
            <span className="block text-xs text-gray-500 font-normal">{exercise.category}</span>
          )}
        </div>
        
        <input
          type="number"
          min="1"
          value={exercise.sets}
          onChange={(e) => onChange(exercise.id, 'sets', parseInt(e.target.value) || 1)}
          className="w-full px-2 py-1 border border-gray-300 rounded text-center focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Sets"
        />
        
        <input
          type="text"
          value={exercise.reps}
          onChange={(e) => onChange(exercise.id, 'reps', e.target.value)}
          className="w-full px-2 py-1 border border-gray-300 rounded text-center focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Reps"
        />
        
        <input
          type="text"
          value={exercise.load}
          onChange={(e) => onChange(exercise.id, 'load', e.target.value)}
          className="w-full px-2 py-1 border border-gray-300 rounded text-center focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Load"
        />
        
        <div className="flex items-center gap-2">
          <input
            type="number"
            min="0"
            step="15"
            value={exercise.rest}
            onChange={(e) => onChange(exercise.id, 'rest', parseInt(e.target.value) || 0)}
            className="w-full px-2 py-1 border border-gray-300 rounded text-center focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Rest"
          />
          <span className="text-xs text-gray-500">s</span>
        </div>
      </div>

      <textarea
        value={exercise.notes}
        onChange={(e) => onChange(exercise.id, 'notes', e.target.value)}
        className="hidden md:block w-32 px-2 py-1 border border-gray-300 rounded text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
        placeholder="Notes..."
        rows={1}
      />

      <button
        onClick={() => onRemove(exercise.id)}
        className="p-2 text-red-400 hover:text-red-600 hover:bg-red-50 rounded-full transition-colors"
        title="Remove exercise"
      >
        <Trash2 size={18} />
      </button>
    </div>
  );
}

export default function WorkoutBuilder({ onSave, onExit, initialWorkout }: WorkoutBuilderProps) {
  const [workout, setWorkout] = useState<WorkoutSession>(initialWorkout || DEFAULT_WORKOUT);
  const [hasChanges, setHasChanges] = useState(false);

  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  // Load from localStorage if no initial workout provided
  useEffect(() => {
    if (!initialWorkout) {
      const saved = localStorage.getItem('forge_current_workout');
      if (saved) {
        try {
          setWorkout(JSON.parse(saved));
        } catch (e) {
          console.error('Failed to load workout', e);
        }
      }
    }
  }, [initialWorkout]);

  // Auto-save to localStorage
  useEffect(() => {
    if (hasChanges) {
      const timeoutId = setTimeout(() => {
        localStorage.setItem('forge_current_workout', JSON.stringify(workout));
        setHasChanges(false);
        if (onSave) onSave(workout);
      }, 500); // Debounce saves
      return () => clearTimeout(timeoutId);
    }
  }, [workout, hasChanges, onSave]);

  const updateExercise = useCallback((id: string, field: keyof WorkoutExercise, value: any) => {
    setWorkout(prev => ({
      ...prev,
      lastModified: Date.now(),
      exercises: prev.exercises.map(ex => 
        ex.id === id ? { ...ex, [field]: value } : ex
      )
    }));
    setHasChanges(true);
  }, []);

  const removeExercise = useCallback((id: string) => {
    if (confirm('Remove this exercise from the workout?')) {
      setWorkout(prev => ({
        ...prev,
        lastModified: Date.now(),
        exercises: prev.exercises.filter(ex => ex.id !== id)
      }));
      setHasChanges(true);
    }
  }, []);

  const addExercise = useCallback((exerciseData: Partial<WorkoutExercise>) => {
    const newExercise: WorkoutExercise = {
      id: crypto.randomUUID(),
      name: exerciseData.name || 'New Exercise',
      category: exerciseData.category,
      sets: exerciseData.sets || 3,
      reps: exerciseData.reps || '8-12',
      load: exerciseData.load || '',
      rest: exerciseData.rest || 60,
      notes: exerciseData.notes || '',
    };

    setWorkout(prev => ({
      ...prev,
      lastModified: Date.now(),
      exercises: [...prev.exercises, newExercise]
    }));
    setHasChanges(true);
    return newExercise.id; // Return ID to allow scrolling/focusing
  }, []);

  const handleDragEnd = useCallback((event: DragEndEvent) => {
    const { active, over } = event;
    if (over && active.id !== over.id) {
      setWorkout(prev => {
        const oldIndex = prev.exercises.findIndex(ex => ex.id === active.id);
        const newIndex = prev.exercises.findIndex(ex => ex.id === over.id);
        return {
          ...prev,
          lastModified: Date.now(),
          exercises: arrayMove(prev.exercises, oldIndex, newIndex)
        };
      });
      setHasChanges(true);
    }
  }, []);

  const clearWorkout = () => {
    if (confirm('Are you sure you want to clear the entire workout? This cannot be undone.')) {
      setWorkout({ ...DEFAULT_WORKOUT, id: crypto.randomUUID() });
      setHasChanges(true);
      localStorage.removeItem('forge_current_workout');
    }
  };

  const exportWorkout = () => {
    const date = new Date().toLocaleDateString();
    let content = `FORGE WORKOUT: ${workout.name || 'Untitled'}\n`;
    content += `Date: ${date}\n`;
    content += `Focus: ${workout.focus || 'General'}\n`;
    content += `Duration: ${workout.duration || 'N/A'}\n\n`;
    content += `EXERCISES:\n`;
    content += `----------------------------------------\n`;
    
    workout.exercises.forEach((ex, idx) => {
      content += `${idx + 1}. ${ex.name} (${ex.category || 'N/A'})\n`;
      content += `   Sets: ${ex.sets} | Reps: ${ex.reps} | Load: ${ex.load || 'BW'} | Rest: ${ex.rest}s\n`;
      if (ex.notes) content += `   Notes: ${ex.notes}\n`;
      content += `----------------------------------------\n`;
    });

    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `forge-workout-${date.replace(/\//g, '-')}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Expose addExercise to parent via window event for Library integration
  useEffect(() => {
    const handleAddFromLibrary = (e: CustomEvent) => {
      addExercise(e.detail);
      // Optional: Show toast notification here
    };
    window.addEventListener('forge-add-to-workout', handleAddFromLibrary as EventListener);
    return () => window.removeEventListener('forge-add-to-workout', handleAddFromLibrary as EventListener);
  }, [addExercise]);

  if (workout.exercises.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center h-full min-h-[400px] text-center p-8 bg-gray-50 rounded-xl border-2 border-dashed border-gray-300">
        <Activity size={64} className="text-gray-400 mb-4" />
        <h3 className="text-xl font-bold text-gray-700 mb-2">Your Workout Board is Empty</h3>
        <p className="text-gray-500 max-w-md mb-6">
          Start building your session by adding exercises from the Library, or load a template to get started quickly.
        </p>
        <div className="flex gap-4">
          <button 
            onClick={() => window.dispatchEvent(new CustomEvent('forge-open-library'))}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            Browse Library
          </button>
          <button 
            onClick={clearWorkout} // Actually just resets state in this context, but effectively does nothing if already empty
            className="px-6 py-2 bg-white text-gray-700 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors font-medium"
          >
            Reset Board
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Header / Meta Data */}
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
          <div className="flex-1 space-y-4">
            <input
              type="text"
              value={workout.name}
              onChange={(e) => {
                setWorkout(prev => ({ ...prev, name: e.target.value, lastModified: Date.now() }));
                setHasChanges(true);
              }}
              placeholder="Workout Name (e.g., Upper Power)"
              className="w-full text-2xl font-bold text-gray-900 border-b-2 border-transparent focus:border-blue-500 outline-none pb-1 placeholder-gray-300"
            />
            <div className="flex flex-wrap gap-4">
              <div className="flex items-center gap-2 text-gray-600">
                <Target size={18} className="text-blue-500" />
                <input
                  type="text"
                  value={workout.focus}
                  onChange={(e) => {
                    setWorkout(prev => ({ ...prev, focus: e.target.value, lastModified: Date.now() }));
                    setHasChanges(true);
                  }}
                  placeholder="Focus Area"
                  className="border-b border-gray-300 focus:border-blue-500 outline-none py-1 bg-transparent w-48"
                />
              </div>
              <div className="flex items-center gap-2 text-gray-600">
                <Clock size={18} className="text-green-500" />
                <input
                  type="text"
                  value={workout.duration}
                  onChange={(e) => {
                    setWorkout(prev => ({ ...prev, duration: e.target.value, lastModified: Date.now() }));
                    setHasChanges(true);
                  }}
                  placeholder="Duration (e.g., 45 min)"
                  className="border-b border-gray-300 focus:border-blue-500 outline-none py-1 bg-transparent w-32"
                />
              </div>
            </div>
          </div>
          
          <div className="flex gap-2">
            <button onClick={exportWorkout} className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg" title="Export/Print">
              <Printer size={20} />
            </button>
            <button onClick={clearWorkout} className="p-2 text-red-600 hover:bg-red-50 rounded-lg" title="Clear All">
              <Trash2 size={20} />
            </button>
            {onExit && (
              <button onClick={onExit} className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg" title="Close Builder">
                <X size={20} />
              </button>
            )}
          </div>
        </div>

        {/* Column Headers */}
        <div className="hidden md:grid grid-cols-6 gap-3 px-5 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">
          <div className="col-span-2">Exercise</div>
          <div className="text-center">Sets</div>
          <div className="text-center">Reps</div>
          <div className="text-center">Load</div>
          <div className="text-center">Rest (s)</div>
          {/* Notes column header is implicit in the row layout */}
        </div>
      </div>

      {/* Exercise List */}
      <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
        <SortableContext items={workout.exercises.map(e => e.id)} strategy={verticalListSortingStrategy}>
          <div className="space-y-2">
            {workout.exercises.map((exercise) => (
              <SortableExerciseRow
                key={exercise.id}
                exercise={exercise}
                onChange={updateExercise}
                onRemove={removeExercise}
                attributes={{}}
              />
            ))}
          </div>
        </SortableContext>
      </DndContext>

      {/* Add Button */}
      <div className="pt-4">
        <button
          onClick={() => window.dispatchEvent(new CustomEvent('forge-open-library'))}
          className="w-full py-4 border-2 border-dashed border-gray-300 rounded-xl text-gray-500 hover:border-blue-500 hover:text-blue-600 hover:bg-blue-50 transition-all flex items-center justify-center gap-2 font-medium"
        >
          <Plus size={20} />
          Add Exercise from Library
        </button>
      </div>
      
      {hasChanges && (
        <div className="fixed bottom-6 right-6 bg-blue-600 text-white px-4 py-2 rounded-lg shadow-lg text-sm font-medium animate-pulse">
          Saving...
        </div>
      )}
    </div>
  );
}
