/**
 * Enhanced Exercise Card Component
 * Professional UI/UX with muscle group previews, equipment icons, and improved visual hierarchy
 */

import React, { useState } from 'react';
import { Exercise } from './exercise.service';
import { 
  getMuscleGroups, 
  getEquipmentDisplay,
  getSuperCategoryByCategoryId,
  ENHANCED_CATEGORIES 
} from '../../data/exerciseOrganization';

interface ExerciseCardProps {
  exercise: Exercise;
  onClick?: () => void;
}

interface ExerciseModalProps {
  exercise: Exercise;
  isOpen: boolean;
  onClose: () => void;
}

const ExerciseModal: React.FC<ExerciseModalProps> = ({ exercise, isOpen, onClose }) => {
  if (!isOpen) return null;

  const categoryInfo = ENHANCED_CATEGORIES[exercise.category];
  const superCategory = categoryInfo ? getSuperCategoryByCategoryId(exercise.category) : null;
  const muscleGroups = getMuscleGroups(exercise.category);
  const equipmentIcons = getEquipmentDisplay(exercise.equipment);

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      {/* Backdrop */}
      <div className="fixed inset-0 bg-gray-900 bg-opacity-75 transition-opacity" onClick={onClose}></div>

      {/* Modal Panel */}
      <div className="flex min-h-full items-center justify-center p-4">
        <div className="relative bg-white rounded-2xl shadow-2xl max-w-5xl w-full max-h-[90vh] overflow-hidden flex flex-col">
          
          {/* Header - Enhanced with Super Category */}
          <div className="flex-shrink-0 px-8 py-6 bg-gradient-to-r from-indigo-50 via-white to-purple-50 border-b border-gray-200">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  {superCategory && (
                    <span className="text-lg" title={superCategory.name}>{superCategory.icon}</span>
                  )}
                  <h2 id="modal-title" className="text-2xl font-bold text-gray-900">{exercise.name}</h2>
                  <span className={`px-3 py-1 rounded-full text-sm font-bold border-2 ${
                    exercise.difficulty === 'Beginner' ? 'bg-green-100 text-green-700 border-green-300' :
                    exercise.difficulty === 'Intermediate' ? 'bg-blue-100 text-blue-700 border-blue-300' :
                    'bg-orange-100 text-orange-700 border-orange-300'
                  }`}>
                    {exercise.difficulty}
                  </span>
                  {exercise.is_pain_safe && (
                    <span className="px-3 py-1 rounded-full bg-green-100 text-green-700 text-sm font-bold border-2 border-green-300 flex items-center gap-1">
                      <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                      </svg>
                      Pain-Safe
                    </span>
                  )}
                </div>
                
                {/* Enhanced Meta Information */}
                <div className="flex items-center gap-3 text-sm flex-wrap">
                  <span className="px-3 py-1.5 bg-blue-100 text-blue-700 rounded-lg font-medium flex items-center gap-2">
                    <span>🎯</span>
                    {categoryInfo?.fullName || exercise.movement_pattern}
                  </span>
                  <div className="flex items-center gap-1">
                    {equipmentIcons.map((eq, idx) => (
                      <span key={idx} className="px-2 py-1 bg-purple-100 text-purple-700 rounded-lg font-medium" title={eq.name}>
                        {eq.icon} {eq.name}
                      </span>
                    ))}
                  </div>
                  {superCategory && (
                    <span className="px-3 py-1.5 bg-gray-100 text-gray-700 rounded-lg font-medium">
                      {superCategory.name}
                    </span>
                  )}
                </div>

                {/* Muscle Groups Preview */}
                <div className="mt-4 grid grid-cols-2 gap-3">
                  <div className="bg-red-50 rounded-lg p-3 border border-red-100">
                    <h4 className="text-xs font-semibold text-red-700 mb-2">PRIMARY MUSCLES</h4>
                    <div className="flex flex-wrap gap-1">
                      {muscleGroups.primary.map((muscle, idx) => (
                        <span key={idx} className="px-2 py-1 bg-white border border-red-200 rounded text-xs text-red-700 font-medium">
                          {muscle}
                        </span>
                      ))}
                    </div>
                  </div>
                  <div className="bg-blue-50 rounded-lg p-3 border border-blue-100">
                    <h4 className="text-xs font-semibold text-blue-700 mb-2">SECONDARY MUSCLES</h4>
                    <div className="flex flex-wrap gap-1">
                      {muscleGroups.secondary.map((muscle, idx) => (
                        <span key={idx} className="px-2 py-1 bg-white border border-blue-200 rounded text-xs text-blue-700 font-medium">
                          {muscle}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
              
              <button
                onClick={onClose}
                className="ml-4 p-2 rounded-full hover:bg-gray-200 transition-colors"
                aria-label="Close modal"
              >
                <svg className="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>

          {/* Content - Scrollable */}
          <div className="flex-1 overflow-y-auto px-8 py-6">
            <div className="grid grid-cols-2 gap-6">
              
              {/* Left Column */}
              <div className="space-y-6">
                {/* Coaching Cues */}
                <div className="bg-gradient-to-br from-emerald-50 to-green-50 rounded-xl p-5 border border-emerald-200">
                  <div className="flex items-center gap-2 mb-3">
                    <svg className="w-6 h-6 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    <h3 className="text-lg font-bold text-emerald-800">Coaching Cues</h3>
                  </div>
                  <ul className="space-y-2">
                    {exercise.coaching_cues.map((cue, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-emerald-700">
                        <span className="text-emerald-500 mt-1.5">•</span>
                        <span className="flex-1">{cue}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Common Errors */}
                <div className="bg-gradient-to-br from-red-50 to-orange-50 rounded-xl p-5 border border-red-200">
                  <div className="flex items-center gap-2 mb-3">
                    <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                    </svg>
                    <h3 className="text-lg font-bold text-red-800">Common Errors</h3>
                  </div>
                  <ul className="space-y-2">
                    {exercise.common_errors.map((error, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-red-700">
                        <span className="text-red-500 mt-1.5">•</span>
                        <span className="flex-1">{error}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Contraindications */}
                {exercise.contraindications.length > 0 && (
                  <div className="bg-gradient-to-br from-amber-50 to-yellow-50 rounded-xl p-5 border border-amber-200">
                    <div className="flex items-center gap-2 mb-3">
                      <svg className="w-6 h-6 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636" />
                      </svg>
                      <h3 className="text-lg font-bold text-amber-800">Contraindications</h3>
                    </div>
                    <ul className="space-y-2">
                      {exercise.contraindications.map((contra, idx) => (
                        <li key={idx} className="flex items-start gap-2 text-amber-700">
                          <span className="text-amber-500 mt-1.5">•</span>
                          <span className="flex-1">{contra}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>

              {/* Right Column */}
              <div className="space-y-6">
                {/* Progressions */}
                <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-5 border border-blue-200">
                  <div className="flex items-center gap-2 mb-3">
                    <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                    </svg>
                    <h3 className="text-lg font-bold text-blue-800">Progressions</h3>
                  </div>
                  <ul className="space-y-2">
                    {exercise.progressions.map((prog, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-blue-700">
                        <span className="text-blue-500 mt-1.5">▸</span>
                        <span className="flex-1">{prog}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Regressions */}
                <div className="bg-gradient-to-br from-violet-50 to-purple-50 rounded-xl p-5 border border-purple-200">
                  <div className="flex items-center gap-2 mb-3">
                    <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
                    </svg>
                    <h3 className="text-lg font-bold text-purple-800">Regressions</h3>
                  </div>
                  <ul className="space-y-2">
                    {exercise.regressions.map((reg, idx) => (
                      <li key={idx} className="flex items-start gap-2 text-purple-700">
                        <span className="text-purple-500 mt-1.5">▸</span>
                        <span className="flex-1">{reg}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Equipment Alternatives */}
                {exercise.equipment_alternatives && exercise.equipment_alternatives.length > 0 && (
                  <div className="bg-gradient-to-br from-gray-50 to-slate-50 rounded-xl p-5 border border-gray-200">
                    <div className="flex items-center gap-2 mb-3">
                      <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                      <h3 className="text-lg font-bold text-gray-800">Equipment Alternatives</h3>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {exercise.equipment_alternatives.map((alt, idx) => (
                        <span key={idx} className="px-3 py-1.5 bg-white border border-gray-300 rounded-lg text-gray-700 text-sm font-medium shadow-sm">
                          {alt}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Description */}
                {exercise.description && (
                  <div className="bg-gradient-to-br from-cyan-50 to-teal-50 rounded-xl p-5 border border-cyan-200">
                    <div className="flex items-center gap-2 mb-3">
                      <svg className="w-6 h-6 text-cyan-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <h3 className="text-lg font-bold text-cyan-800">Description</h3>
                    </div>
                    <p className="text-cyan-700 leading-relaxed">{exercise.description}</p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="flex-shrink-0 px-8 py-4 bg-gray-50 border-t border-gray-200">
            <button
              onClick={onClose}
              className="w-full py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold rounded-xl hover:from-indigo-700 hover:to-purple-700 transition-all shadow-md hover:shadow-lg"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export const ExerciseCard: React.FC<ExerciseCardProps> = ({ exercise, onClick }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  const categoryInfo = ENHANCED_CATEGORIES[exercise.category];
  const superCategory = categoryInfo ? getSuperCategoryByCategoryId(exercise.category) : null;
  const muscleGroups = getMuscleGroups(exercise.category);
  const equipmentIcons = getEquipmentDisplay(exercise.equipment);

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
    <>
      <div 
        className="bg-white rounded-xl shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-200 cursor-pointer border border-gray-200 overflow-hidden group"
        onClick={() => setIsModalOpen(true)}
      >
        {/* Enhanced Header with Super Category Icon */}
        <div className="px-3 py-2 bg-gradient-to-r from-gray-50 to-white border-b border-gray-100">
          <div className="flex items-center justify-between gap-2">
            <h3 className="text-xs font-bold text-gray-900 truncate flex-1" title={exercise.name}>
              {exercise.name}
            </h3>
            <div className="flex items-center gap-1.5 flex-shrink-0">
              {superCategory && (
                <span className="text-sm" title={superCategory.name}>{superCategory.icon}</span>
              )}
              <span 
                className={`w-5 h-5 flex items-center justify-center rounded text-[10px] font-bold border ${getDifficultyBadge(exercise.difficulty)}`}
                title={`${exercise.difficulty} Level`}
              >
                {getDifficultyIcon(exercise.difficulty)}
              </span>
              {exercise.is_pain_safe && (
                <span className="w-4 h-4 rounded-full bg-green-100 text-green-600 flex items-center justify-center text-[10px]" title="Pain-Safe Exercise">
                  ✓
                </span>
              )}
            </div>
          </div>
        </div>

        {/* Enhanced Meta Row with Equipment Icons */}
        <div className="px-3 py-2 bg-white">
          <div className="flex items-center gap-1.5 text-[10px] flex-wrap">
            <span className="px-1.5 py-0.5 bg-blue-50 text-blue-700 rounded truncate max-w-[80px]" title={categoryInfo?.fullName || exercise.movement_pattern}>
              {categoryInfo?.name || exercise.movement_pattern}
            </span>
            {equipmentIcons.slice(0, 2).map((eq, idx) => (
              <span 
                key={idx} 
                className="px-1.5 py-0.5 bg-purple-50 text-purple-700 rounded flex items-center gap-0.5" 
                title={eq.name}
              >
                {eq.icon}
              </span>
            ))}
          </div>
        </div>

        {/* Muscle Group Preview */}
        <div className="px-3 py-2 bg-gray-50 border-t border-gray-100">
          <div className="flex items-center gap-1 text-[9px]">
            <span className="text-gray-500">Primary:</span>
            <div className="flex gap-1">
              {muscleGroups.primary.slice(0, 2).map((muscle, idx) => (
                <span key={idx} className="px-1.5 py-0.5 bg-red-50 text-red-700 rounded-[4px] font-medium truncate max-w-[60px]">
                  {muscle}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Hover Hint */}
        <div className="px-3 py-1.5 bg-gradient-to-r from-indigo-50 to-purple-50 border-t border-gray-100 opacity-0 group-hover:opacity-100 transition-opacity">
          <div className="flex items-center justify-center gap-1 text-[10px] text-indigo-600 font-medium">
            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
            <span>Click for full details</span>
          </div>
        </div>
      </div>

      {/* Full Details Modal */}
      <ExerciseModal 
        exercise={exercise}
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </>
  );
};

export default ExerciseCard;
