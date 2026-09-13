/**
 * Exercise Card Component
 * Displays individual exercise with all metadata
 */

import React, { useState } from 'react';
import { Exercise } from './exercise.service';

interface ExerciseCardProps {
  exercise: Exercise;
  onClick?: () => void;
}

export const ExerciseCard: React.FC<ExerciseCardProps> = ({ exercise, onClick }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  
  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'Beginner': return 'bg-green-100 text-green-800';
      case 'Intermediate': return 'bg-yellow-100 text-yellow-800';
      case 'Advanced': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div 
      className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow cursor-pointer border border-gray-200"
      onClick={onClick}
    >
      {/* Header */}
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xl font-bold text-gray-900 mb-1">{exercise.name}</h3>
          <p className="text-sm text-gray-600">{exercise.category} • {exercise.subcategory}</p>
        </div>
        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getDifficultyColor(exercise.difficulty)}`}>
          {exercise.difficulty}
        </span>
      </div>

      {/* Description */}
      <p className="text-gray-700 mb-4 line-clamp-2">{exercise.description}</p>

      {/* Meta Tags - Source organization removed as requested */}
      <div className="flex flex-wrap gap-2 mb-4">
        <span className="px-2 py-1 bg-blue-50 text-blue-700 text-xs rounded">
          {exercise.movement_pattern}
        </span>
        <span className="px-2 py-1 bg-purple-50 text-purple-700 text-xs rounded">
          {exercise.equipment}
        </span>
        {exercise.is_pain_safe && (
          <span className="px-2 py-1 bg-green-50 text-green-700 text-xs rounded font-semibold">
            ✓ Pain-Safe
          </span>
        )}
      </div>

      {/* Expandable Details */}
      {isExpanded && (
        <div className="mt-4 pt-4 border-t border-gray-200 space-y-3">
          <div>
            <h4 className="font-semibold text-gray-800 mb-1">Coaching Cues:</h4>
            <ul className="list-disc list-inside text-sm text-gray-700">
              {exercise.coaching_cues.map((cue, idx) => (
                <li key={idx}>{cue}</li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-gray-800 mb-1">Common Errors:</h4>
            <ul className="list-disc list-inside text-sm text-red-700">
              {exercise.common_errors.map((error, idx) => (
                <li key={idx}>{error}</li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-gray-800 mb-1">Contraindications:</h4>
            <ul className="list-disc list-inside text-sm text-orange-700">
              {exercise.contraindications.map((contra, idx) => (
                <li key={idx}>{contra}</li>
              ))}
            </ul>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <h4 className="font-semibold text-gray-800 mb-1">Regressions:</h4>
              <ul className="list-disc list-inside text-sm text-gray-700">
                {exercise.regressions.map((reg, idx) => (
                  <li key={idx}>{reg}</li>
                ))}
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-gray-800 mb-1">Progressions:</h4>
              <ul className="list-disc list-inside text-sm text-gray-700">
                {exercise.progressions.map((prog, idx) => (
                  <li key={idx}>{prog}</li>
                ))}
              </ul>
            </div>
          </div>

          <div>
            <h4 className="font-semibold text-gray-800 mb-1">Equipment Alternatives:</h4>
            <p className="text-sm text-gray-700">{exercise.equipment_alternatives.join(', ')}</p>
          </div>
        </div>
      )}

      {/* Toggle Button */}
      <button
        onClick={(e) => {
          e.stopPropagation();
          setIsExpanded(!isExpanded);
        }}
        className="mt-4 w-full py-2 text-sm font-medium text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded transition-colors"
      >
        {isExpanded ? 'Show Less' : 'View Details'}
      </button>
    </div>
  );
};

export default ExerciseCard;
