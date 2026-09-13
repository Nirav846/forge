/**
 * Exercise Card Component - Compact Design
 * Displays individual exercise with optimized space usage
 */

import React, { useState } from 'react';
import { Exercise } from './exercise.service';

interface ExerciseCardProps {
  exercise: Exercise;
  onClick?: () => void;
}

export const ExerciseCard: React.FC<ExerciseCardProps> = ({ exercise, onClick }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  
  const getDifficultyBadge = (difficulty: string) => {
    switch (difficulty) {
      case 'Beginner': return 'bg-green-100 text-green-700 border-green-200';
      case 'Intermediate': return 'bg-blue-100 text-blue-700 border-blue-200';
      case 'Advanced': return 'bg-orange-100 text-orange-700 border-orange-200';
      default: return 'bg-gray-100 text-gray-700 border-gray-200';
    }
  };

  const getDifficultyIcon = (difficulty: string) => {
    switch (difficulty) {
      case 'Beginner': return 'B';
      case 'Intermediate': return 'I';
      case 'Advanced': return 'A';
      default: return '?';
    }
  };

  return (
    <div 
      className="bg-white rounded-lg shadow-sm hover:shadow-md transition-all cursor-pointer border border-gray-200 overflow-hidden group"
      onClick={onClick}
    >
      {/* Compact Header - Name inline with badges */}
      <div className="px-3 py-2.5 bg-gradient-to-r from-gray-50 to-white border-b border-gray-100">
        <div className="flex items-center justify-between gap-2">
          <h3 className="text-sm font-semibold text-gray-900 truncate flex-1" title={exercise.name}>
            {exercise.name}
          </h3>
          <div className="flex items-center gap-1.5 flex-shrink-0">
            <span 
              className={`px-2 py-0.5 rounded text-xs font-bold border ${getDifficultyBadge(exercise.difficulty)}`}
              title={`${exercise.difficulty} Level`}
            >
              {getDifficultyIcon(exercise.difficulty)}
            </span>
            {exercise.is_pain_safe && (
              <span className="w-5 h-5 rounded-full bg-green-100 text-green-600 flex items-center justify-center text-xs" title="Pain-Safe Exercise">
                ✓
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Compact Meta Row */}
      <div className="px-3 py-2 bg-white">
        <div className="flex items-center gap-2 text-xs">
          <span className="px-2 py-0.5 bg-blue-50 text-blue-700 rounded font-medium truncate max-w-[120px]" title={exercise.movement_pattern}>
            {exercise.movement_pattern}
          </span>
          <span className="px-2 py-0.5 bg-purple-50 text-purple-700 rounded truncate max-w-[100px]" title={exercise.equipment}>
            {exercise.equipment}
          </span>
          <span className="text-gray-400 truncate flex-1 text-[11px]" title={exercise.category}>
            {exercise.category}
          </span>
        </div>
      </div>

      {/* Expandable Details - Only shown when expanded */}
      {isExpanded && (
        <div className="px-3 pb-3 pt-2 border-t border-gray-100 bg-gray-50 space-y-3 text-xs">
          {/* Quick Info Grid */}
          <div className="grid grid-cols-2 gap-2">
            <div>
              <span className="font-semibold text-gray-700 block mb-1">✓ Coaching Cues</span>
              <ul className="space-y-0.5 text-gray-600">
                {exercise.coaching_cues.slice(0, 3).map((cue, idx) => (
                  <li key={idx} className="truncate">• {cue}</li>
                ))}
                {exercise.coaching_cues.length > 3 && (
                  <li className="text-gray-400 italic">+{exercise.coaching_cues.length - 3} more</li>
                )}
              </ul>
            </div>
            <div>
              <span className="font-semibold text-gray-700 block mb-1">⚠️ Common Errors</span>
              <ul className="space-y-0.5 text-red-600">
                {exercise.common_errors.slice(0, 2).map((error, idx) => (
                  <li key={idx} className="truncate">• {error}</li>
                ))}
                {exercise.common_errors.length > 2 && (
                  <li className="text-gray-400 italic">+{exercise.common_errors.length - 2} more</li>
                )}
              </ul>
            </div>
          </div>

          {/* Contraindications */}
          {exercise.contraindications.length > 0 && (
            <div className="bg-orange-50 border border-orange-200 rounded p-2">
              <span className="font-semibold text-orange-800 block mb-1">🚫 Contraindications</span>
              <ul className="space-y-0.5 text-orange-700">
                {exercise.contraindications.slice(0, 2).map((contra, idx) => (
                  <li key={idx} className="truncate">• {contra}</li>
                ))}
              </ul>
            </div>
          )}

          {/* Progressions & Regressions */}
          <div className="grid grid-cols-2 gap-2">
            <div className="bg-green-50 rounded p-2">
              <span className="font-semibold text-green-700 block mb-1">📈 Progressions</span>
              <ul className="space-y-0.5 text-green-600">
                {exercise.progressions.slice(0, 2).map((prog, idx) => (
                  <li key={idx} className="truncate text-[11px]">• {prog}</li>
                ))}
              </ul>
            </div>
            <div className="bg-blue-50 rounded p-2">
              <span className="font-semibold text-blue-700 block mb-1">📉 Regressions</span>
              <ul className="space-y-0.5 text-blue-600">
                {exercise.regressions.slice(0, 2).map((reg, idx) => (
                  <li key={idx} className="truncate text-[11px]">• {reg}</li>
                ))}
              </ul>
            </div>
          </div>

          {/* Equipment Alternatives */}
          {exercise.equipment_alternatives && exercise.equipment_alternatives.length > 0 && (
            <div className="bg-gray-100 rounded p-2">
              <span className="font-semibold text-gray-700 block mb-1">🔄 Equipment Alternatives</span>
              <p className="text-gray-600 text-[11px]">{exercise.equipment_alternatives.join(', ')}</p>
            </div>
          )}
        </div>
      )}

      {/* Compact Toggle Footer */}
      <div className="px-3 py-2 bg-gray-50 border-t border-gray-100">
        <button
          onClick={(e) => {
            e.stopPropagation();
            setIsExpanded(!isExpanded);
          }}
          className="w-full py-1.5 text-xs font-medium text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors flex items-center justify-center gap-1"
        >
          {isExpanded ? (
            <>
              <span>Collapse</span>
              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
              </svg>
            </>
          ) : (
            <>
              <span>Quick View</span>
              <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </>
          )}
        </button>
      </div>
    </div>
  );
};

export default ExerciseCard;
