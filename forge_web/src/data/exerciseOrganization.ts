/**
 * Enhanced Exercise Library Organization
 * Professional UI/UX structure with super-categories, curated collections, and normalized vocabularies
 */

// ============================================================================
// SUPER-CATEGORY STRUCTURE (7 main groups for intuitive navigation)
// ============================================================================

export interface SuperCategory {
  id: string;
  name: string;
  icon: string;
  description: string;
  color: string;
  categories: string[];
}

export const SUPER_CATEGORIES: SuperCategory[] = [
  {
    id: 'lower-body',
    name: 'Lower Body Strength',
    icon: '🦵',
    description: 'Build foundational leg strength and power',
    color: 'blue',
    categories: ['DLKD', 'DLHD', 'SLKD', 'SLHD'],
  },
  {
    id: 'upper-body',
    name: 'Upper Body Strength',
    icon: '💪',
    description: 'Develop pushing and pulling strength',
    color: 'red',
    categories: ['HPush', 'VPush', 'HPull', 'VPull'],
  },
  {
    id: 'core-stability',
    name: 'Core & Stability',
    icon: '🎯',
    description: 'Anti-rotation, carries, and rotational control',
    color: 'green',
    categories: ['Core', 'Carry', 'Rot'],
  },
  {
    id: 'power-explosive',
    name: 'Power & Explosiveness',
    icon: '⚡',
    description: 'Jumps, throws, and ballistic movements',
    color: 'yellow',
    categories: ['Plyo', 'Landing', 'Ball', 'Explosive Performance'],
  },
  {
    id: 'speed-agility',
    name: 'Speed & Agility',
    icon: '🏃',
    description: 'Sprinting, acceleration, and change of direction',
    color: 'orange',
    categories: ['Sprint', 'Acc', 'Agility'],
  },
  {
    id: 'supportive',
    name: 'Supportive Training',
    icon: '🔧',
    description: 'Activation, assessment, conditioning, recovery',
    color: 'purple',
    categories: ['Activation', 'Assessment', 'Cond', 'Recovery'],
  },
];

// ============================================================================
// ENHANCED CATEGORY DEFINITIONS (Full names, no abbreviations)
// ============================================================================

export interface EnhancedCategory {
  id: string;
  name: string;
  fullName: string;
  icon: string;
  description: string;
  superCategoryId: string;
  movementPatterns: string[]; // Simplified patterns for this category
}

export const ENHANCED_CATEGORIES: Record<string, EnhancedCategory> = {
  // Lower Body - Knee Dominant
  'DLKD': {
    id: 'DLKD',
    name: 'Knee Dominant (Double Leg)',
    fullName: 'Double Leg Knee Dominant',
    icon: '🦵',
    description: 'Squats and knee-focused bilateral movements',
    superCategoryId: 'lower-body',
    movementPatterns: ['Squat', 'Lunge', 'Step-Up'],
  },
  'DLHD': {
    id: 'DLHD',
    name: 'Hip Dominant (Double Leg)',
    fullName: 'Double Leg Hip Dominant',
    icon: '🍑',
    description: 'Deadlifts and hip hinge bilateral movements',
    superCategoryId: 'lower-body',
    movementPatterns: ['Hinge', 'Hip Extension'],
  },
  'SLKD': {
    id: 'SLKD',
    name: 'Knee Dominant (Single Leg)',
    fullName: 'Single Leg Knee Dominant',
    icon: '🦵',
    description: 'Unilateral squats and lunges',
    superCategoryId: 'lower-body',
    movementPatterns: ['Single Leg Squat', 'Split Squat', 'Lunge'],
  },
  'SLHD': {
    id: 'SLHD',
    name: 'Hip Dominant (Single Leg)',
    fullName: 'Single Leg Hip Dominant',
    icon: '🍑',
    description: 'Unilateral deadlifts and bridges',
    superCategoryId: 'lower-body',
    movementPatterns: ['Single Leg Hinge', 'Single Leg Bridge'],
  },
  // Upper Body - Push
  'HPush': {
    id: 'HPush',
    name: 'Horizontal Push',
    fullName: 'Horizontal Pushing',
    icon: '👊',
    description: 'Push-ups, bench press, horizontal pressing',
    superCategoryId: 'upper-body',
    movementPatterns: ['Horizontal Press'],
  },
  'VPush': {
    id: 'VPush',
    name: 'Vertical Push',
    fullName: 'Vertical Pushing',
    icon: '🙌',
    description: 'Overhead press, push press',
    superCategoryId: 'upper-body',
    movementPatterns: ['Vertical Press'],
  },
  // Upper Body - Pull
  'HPull': {
    id: 'HPull',
    name: 'Horizontal Pull',
    fullName: 'Horizontal Pulling',
    icon: '🤸',
    description: 'Rows, face pulls, horizontal pulling',
    superCategoryId: 'upper-body',
    movementPatterns: ['Horizontal Pull'],
  },
  'VPull': {
    id: 'VPull',
    name: 'Vertical Pull',
    fullName: 'Vertical Pulling',
    icon: '🧗',
    description: 'Pull-ups, lat pulldowns',
    superCategoryId: 'upper-body',
    movementPatterns: ['Vertical Pull'],
  },
  // Core
  'Core': {
    id: 'Core',
    name: 'Core Stability',
    fullName: 'Core & Anti-Rotation',
    icon: '🎯',
    description: 'Planks, anti-rotation, bracing',
    superCategoryId: 'core-stability',
    movementPatterns: ['Anti-Rotation', 'Anti-Extension', 'Bracing'],
  },
  'Carry': {
    id: 'Carry',
    name: 'Loaded Carries',
    fullName: 'Loaded Carries & Walks',
    icon: '🏋️',
    description: 'Farmer walks, suitcase carries',
    superCategoryId: 'core-stability',
    movementPatterns: ['Carry'],
  },
  'Rot': {
    id: 'Rot',
    name: 'Rotational Power',
    fullName: 'Rotational Strength & Power',
    icon: '🔄',
    description: 'Rotational throws and exercises',
    superCategoryId: 'core-stability',
    movementPatterns: ['Rotation'],
  },
  // Power & Plyometrics
  'Plyo': {
    id: 'Plyo',
    name: 'Plyometrics',
    fullName: 'Plyometric Jumps & Bounds',
    icon: '💥',
    description: 'Jumps, bounds, explosive takeoffs',
    superCategoryId: 'power-explosive',
    movementPatterns: ['Jump', 'Bound', 'Hop'],
  },
  'Landing': {
    id: 'Landing',
    name: 'Landing Mechanics',
    fullName: 'Landing & Deceleration',
    icon: '🛬',
    description: 'Safe landing technique and deceleration',
    superCategoryId: 'power-explosive',
    movementPatterns: ['Land', 'Decelerate'],
  },
  'Ball': {
    id: 'Ball',
    name: 'Medicine Ball',
    fullName: 'Medicine Ball Throws',
    icon: '🏀',
    description: 'Med ball slams and throws',
    superCategoryId: 'power-explosive',
    movementPatterns: ['Throw', 'Slam'],
  },
  'Explosive Performance': {
    id: 'Explosive Performance',
    name: 'Olympic Derivatives',
    fullName: 'Explosive Performance & Olympic Lifts',
    icon: '⚡',
    description: 'Cleans, snatches, power exercises',
    superCategoryId: 'power-explosive',
    movementPatterns: ['Clean', 'Snatch', 'Triple Extension'],
  },
  // Speed & Agility
  'Sprint': {
    id: 'Sprint',
    name: 'Sprinting',
    fullName: 'Linear Sprinting',
    icon: '🏃',
    description: 'Acceleration and max velocity running',
    superCategoryId: 'speed-agility',
    movementPatterns: ['Sprint', 'Accelerate'],
  },
  'Acc': {
    id: 'Acc',
    name: 'Acceleration',
    fullName: 'Acceleration & First Step',
    icon: '🚀',
    description: 'Initial acceleration and first step quickness',
    superCategoryId: 'speed-agility',
    movementPatterns: ['First Step', 'Short Acceleration'],
  },
  'Agility': {
    id: 'Agility',
    name: 'Agility & COD',
    fullName: 'Agility & Change of Direction',
    icon: '⚡',
    description: 'Change of direction, reactive drills',
    superCategoryId: 'speed-agility',
    movementPatterns: ['Cut', 'Shuffle', 'React'],
  },
  // Supportive
  'Activation': {
    id: 'Activation',
    name: 'Movement Prep',
    fullName: 'Activation & Movement Preparation',
    icon: '🔌',
    description: 'Warm-up and muscle activation',
    superCategoryId: 'supportive',
    movementPatterns: ['Activate', 'Mobilize'],
  },
  'Assessment': {
    id: 'Assessment',
    name: 'Testing & Screening',
    fullName: 'Assessment & Movement Screening',
    icon: '📊',
    description: 'Performance tests and movement screens',
    superCategoryId: 'supportive',
    movementPatterns: ['Test', 'Screen'],
  },
  'Cond': {
    id: 'Cond',
    name: 'Conditioning',
    fullName: 'Energy System Development',
    icon: '❤️',
    description: 'Cardiovascular and metabolic conditioning',
    superCategoryId: 'supportive',
    movementPatterns: ['Interval', 'Continuous'],
  },
  'Recovery': {
    id: 'Recovery',
    name: 'Recovery & Mobility',
    fullName: 'Recovery & Regeneration',
    icon: '🧘',
    description: 'Mobility work and regeneration',
    superCategoryId: 'supportive',
    movementPatterns: ['Stretch', 'Release'],
  },
};

// ============================================================================
// CURATED COLLECTIONS (Goal-oriented browsing)
// ============================================================================

export interface Collection {
  id: string;
  name: string;
  description: string;
  icon: string;
  color: string;
  goal: string;
  filterCriteria: {
    categories?: string[];
    difficulties?: string[];
    is_pain_safe?: boolean;
    equipment?: string[];
    tags?: string[];
  };
  recommendedFor: string[];
}

export const CURATED_COLLECTIONS: Collection[] = [
  {
    id: 'foundation-five',
    name: 'Foundation Five',
    description: 'Essential movement patterns every athlete needs',
    icon: '⭐',
    color: 'gold',
    goal: 'Build fundamental strength',
    filterCriteria: {
      categories: ['DLKD', 'DLHD', 'HPush', 'HPull', 'Core'],
      difficulties: ['Beginner', 'Intermediate'],
    },
    recommendedFor: ['All athletes', 'Beginners', 'Return to training'],
  },
  {
    id: 'pain-safe',
    name: 'Pain-Safe Protocol',
    description: 'Exercises safe for training around injuries',
    icon: '✓',
    color: 'green',
    goal: 'Train safely with limitations',
    filterCriteria: {
      is_pain_safe: true,
    },
    recommendedFor: ['Injured athletes', 'Return to play', 'Pain management'],
  },
  {
    id: 'no-equipment',
    name: 'No Equipment Needed',
    description: 'Effective bodyweight exercises anywhere',
    icon: '🏠',
    color: 'blue',
    goal: 'Train at home or traveling',
    filterCriteria: {
      equipment: ['Bodyweight', 'None'],
    },
    recommendedFor: ['Home training', 'Travel', 'Limited facilities'],
  },
  {
    id: 'power-developer',
    name: 'Power Developer',
    description: 'Explosive exercises for athletic performance',
    icon: '💥',
    color: 'red',
    goal: 'Increase rate of force development',
    filterCriteria: {
      categories: ['Plyo', 'Ball', 'Explosive Performance'],
    },
    recommendedFor: ['Team sport athletes', 'Power athletes', 'In-season maintenance'],
  },
  {
    id: 'speed-school',
    name: 'Speed School',
    description: 'Linear speed and acceleration development',
    icon: '🚀',
    color: 'orange',
    goal: 'Get faster in straight lines',
    filterCriteria: {
      categories: ['Sprint', 'Acc'],
    },
    recommendedFor: ['Field sport athletes', 'Track athletes', 'Speed development'],
  },
  {
    id: 'single-leg-stability',
    name: 'Single Leg Stability',
    description: 'Unilateral strength and balance',
    icon: '⚖️',
    color: 'purple',
    goal: 'Improve balance and prevent injuries',
    filterCriteria: {
      categories: ['SLKD', 'SLHD'],
    },
    recommendedFor: ['Runners', 'Court sport athletes', 'Injury prevention'],
  },
  {
    id: 'upper-body-push-pull',
    name: 'Upper Body Balance',
    description: 'Balanced pushing and pulling strength',
    icon: '💪',
    color: 'indigo',
    goal: 'Build balanced upper body strength',
    filterCriteria: {
      categories: ['HPush', 'VPush', 'HPull', 'VPull'],
    },
    recommendedFor: ['All athletes', 'Posture improvement', 'Shoulder health'],
  },
  {
    id: 'quick-session',
    name: 'Quick Session (15 min)',
    description: 'High-impact exercises for short workouts',
    icon: '⏱️',
    color: 'teal',
    goal: 'Maximum results in minimum time',
    filterCriteria: {
      difficulties: ['Beginner', 'Intermediate'],
    },
    tags: ['time-efficient'],
    recommendedFor: ['Busy schedules', 'Active recovery days', 'Travel'],
  },
  {
    id: 'advanced-athlete',
    name: 'Advanced Athlete',
    description: 'Challenging exercises for experienced trainees',
    icon: '🏆',
    color: 'slate',
    goal: 'Maximize performance potential',
    filterCriteria: {
      difficulties: ['Advanced'],
    },
    recommendedFor: ['Experienced athletes', 'Off-season training', 'Performance peaks'],
  },
  {
    id: 'prehab-special',
    name: 'Prehab Special',
    description: 'Injury prevention and resilience building',
    icon: '🛡️',
    color: 'emerald',
    goal: 'Bulletproof your body',
    filterCriteria: {
      categories: ['Activation', 'SLKD', 'SLHD', 'Landing', 'Core'],
    },
    recommendedFor: ['Injury prevention', 'High-risk athletes', 'Longevity'],
  },
];

// ============================================================================
// NORMALIZED EQUIPMENT VOCABULARY (192 → 18 canonical types)
// ============================================================================

export const EQUIPMENT_CANONICAL = {
  'bodyweight': { name: 'Bodyweight', icon: '🧍', keywords: ['bodyweight', 'none', 'no equipment'] },
  'barbell': { name: 'Barbell', icon: '🏋️', keywords: ['barbell', 'bar', 'olympic bar'] },
  'dumbbell': { name: 'Dumbbell', icon: '🏋️‍♀️', keywords: ['dumbbell', 'db', 'dumbbells'] },
  'kettlebell': { name: 'Kettlebell', icon: '🔔', keywords: ['kettlebell', 'kb'] },
  'medicine-ball': { name: 'Medicine Ball', icon: '🏀', keywords: ['med ball', 'medicine ball', 'slam ball'] },
  'resistance-band': { name: 'Resistance Band', icon: '🎗️', keywords: ['band', 'resistance band', 'mini band'] },
  'cable-machine': { name: 'Cable Machine', icon: '🔗', keywords: ['cable', 'cable machine'] },
  'pull-up-bar': { name: 'Pull-Up Bar', icon: '🤸', keywords: ['pull-up bar', 'pull up bar', 'chin-up bar'] },
  'box': { name: 'Plyo Box', icon: '📦', keywords: ['box', 'plyo box', 'bench'] },
  'agility-ladder': { name: 'Agility Ladder', icon: '🪜', keywords: ['agility ladder', 'ladder'] },
  'cones': { name: 'Cones', icon: '🔶', keywords: ['cone', 'cones'] },
  'hurdle': { name: 'Hurdle', icon: '🚧', keywords: ['hurdle', 'low hurdle', 'mini hurdle'] },
  'sled': { name: 'Sled', icon: '🛷', keywords: ['sled', 'prowler'] },
  'foam-roller': { name: 'Foam Roller', icon: '🌀', keywords: ['foam roller', 'roller'] },
  'stability-ball': { name: 'Stability Ball', icon: '⚪', keywords: ['stability ball', 'swiss ball', 'exercise ball'] },
  'ab-wheel': { name: 'Ab Wheel', icon: '🎡', keywords: ['ab wheel', 'ab-wheel'] },
  'timer': { name: 'Timer', icon: '⏱️', keywords: ['timer', 'stopwatch', 'clock'] },
  'partner': { name: 'Partner', icon: '👥', keywords: ['partner', 'coach'] },
};

export function normalizeEquipment(equipment: string): string[] {
  const normalized: string[] = [];
  const input = equipment.toLowerCase();
  
  for (const [canonical, data] of Object.entries(EQUIPMENT_CANONICAL)) {
    for (const keyword of data.keywords) {
      if (input.includes(keyword)) {
        if (!normalized.includes(canonical)) {
          normalized.push(canonical);
        }
        break;
      }
    }
  }
  
  return normalized.length > 0 ? normalized : ['bodyweight'];
}

export function getEquipmentDisplay(equipment: string): { name: string; icon: string }[] {
  const normalized = normalizeEquipment(equipment);
  return normalized.map(key => ({
    name: EQUIPMENT_CANONICAL[key as keyof typeof EQUIPMENT_CANONICAL]?.name || equipment,
    icon: EQUIPMENT_CANONICAL[key as keyof typeof EQUIPMENT_CANONICAL]?.icon || '📦',
  }));
}

// ============================================================================
// SIMPLIFIED MOVEMENT PATTERN TAXONOMY (116 → 24 core patterns)
// ============================================================================

export const MOVEMENT_PATTERN_GROUPS = {
  'squat': { name: 'Squat Pattern', patterns: ['Squat', 'DLKD', 'Stand-Squat', 'Box Squat'] },
  'hinge': { name: 'Hinge Pattern', patterns: ['Hinge', 'DLHD', 'Deadlift'] },
  'lunge': { name: 'Lunge Pattern', patterns: ['Lunge', 'Split Squat', 'Step-Up'] },
  'single-leg-squat': { name: 'Single Leg Squat', patterns: ['SLKD', 'Pistol', 'Single Leg Squat'] },
  'single-leg-hinge': { name: 'Single Leg Hinge', patterns: ['SLHD', 'Single Leg Deadlift'] },
  'horizontal-push': { name: 'Horizontal Push', patterns: ['HPush', 'Push-Up', 'Bench Press'] },
  'vertical-push': { name: 'Vertical Push', patterns: ['VPush', 'Overhead Press'] },
  'horizontal-pull': { name: 'Horizontal Pull', patterns: ['HPull', 'Row'] },
  'vertical-pull': { name: 'Vertical Pull', patterns: ['VPull', 'Pull-Up', 'Lat Pulldown'] },
  'carry': { name: 'Carry', patterns: ['Carry', 'Farmer Walk', 'Suitcase Carry'] },
  'anti-rotation': { name: 'Anti-Rotation', patterns: ['Anti-Rotation', 'Pallof Press'] },
  'rotation': { name: 'Rotation', patterns: ['Rot', 'Rotational Throw'] },
  'jump': { name: 'Jump', patterns: ['Jump', 'Plyo', 'Vertical Jump', 'Horizontal Jump'] },
  'land': { name: 'Land', patterns: ['Land', 'Landing', 'Drop-Jump', 'Decelerate'] },
  'throw': { name: 'Throw', patterns: ['Throw', 'Ball', 'Medicine Ball Throw'] },
  'slam': { name: 'Slam', patterns: ['Slam', 'Overhead Slam'] },
  'sprint': { name: 'Sprint', patterns: ['Sprint', 'Acc', 'Acceleration'] },
  'cut': { name: 'Cut', patterns: ['Cut', 'Agility', 'Change of Direction'] },
  'shuffle': { name: 'Shuffle', patterns: ['Shuffle', 'Lateral Movement'] },
  'hop': { name: 'Hop', patterns: ['Hop', 'Multi-Planar Hopping'] },
  'bound': { name: 'Bound', patterns: ['Bound', 'Lateral Bound'] },
  'clean': { name: 'Clean', patterns: ['Clean', 'Power Clean', 'Hang Clean'] },
  'snatch': { name: 'Snatch', patterns: ['Snatch', 'Power Snatch'] },
  'triple-extension': { name: 'Triple Extension', patterns: ['Triple Extension', 'Jump-Extension'] },
};

export function categorizeMovementPattern(pattern: string): string {
  const patternLower = pattern.toLowerCase();
  
  for (const [group, data] of Object.entries(MOVEMENT_PATTERN_GROUPS)) {
    for (const p of data.patterns) {
      if (patternLower.includes(p.toLowerCase()) || p.toLowerCase().includes(patternLower)) {
        return group;
      }
    }
  }
  
  return 'other';
}

// ============================================================================
// MUSCLE GROUP MAPPING (for visual previews on cards)
// ============================================================================

export const MUSCLE_GROUP_MAP: Record<string, { primary: string[]; secondary: string[] }> = {
  'DLKD': { primary: ['Quadriceps', 'Glutes'], secondary: ['Hamstrings', 'Calves', 'Core'] },
  'DLHD': { primary: ['Hamstrings', 'Glutes'], secondary: ['Lower Back', 'Core', 'Forearms'] },
  'SLKD': { primary: ['Quadriceps', 'Glutes'], secondary: ['Hamstrings', 'Calves', 'Core', 'Hip Stabilizers'] },
  'SLHD': { primary: ['Hamstrings', 'Glutes'], secondary: ['Lower Back', 'Core', 'Hip Stabilizers'] },
  'HPush': { primary: ['Chest', 'Triceps'], secondary: ['Front Delts', 'Core'] },
  'VPush': { primary: ['Shoulders', 'Triceps'], secondary: ['Upper Chest', 'Core', 'Serratus'] },
  'HPull': { primary: ['Lats', 'Rhomboids'], secondary: ['Rear Delts', 'Biceps', 'Mid-Traps'] },
  'VPull': { primary: ['Lats', 'Biceps'], secondary: ['Rhomboids', 'Rear Delts', 'Mid-Traps'] },
  'Core': { primary: ['Abs', 'Obliques'], secondary: ['Hip Flexors', 'Lower Back'] },
  'Carry': { primary: ['Core', 'Forearms'], secondary: ['Shoulders', 'Traps', 'Glutes'] },
  'Rot': { primary: ['Obliques', 'Transverse Abdominis'], secondary: ['Hips', 'Thoracic Spine'] },
  'Plyo': { primary: ['Quadriceps', 'Calves'], secondary: ['Glutes', 'Hamstrings', 'Hip Flexors'] },
  'Landing': { primary: ['Quadriceps', 'Glutes'], secondary: ['Hamstrings', 'Calves', 'Core'] },
  'Ball': { primary: ['Core', 'Shoulders'], secondary: ['Obliques', 'Lats', 'Triceps'] },
  'Explosive Performance': { primary: ['Full Body'], secondary: ['Power Chain'] },
  'Sprint': { primary: ['Hamstrings', 'Glutes'], secondary: ['Quadriceps', 'Calves', 'Hip Flexors', 'Core'] },
  'Acc': { primary: ['Quadriceps', 'Glutes'], secondary: ['Calves', 'Hip Flexors', 'Core'] },
  'Agility': { primary: ['Adductors', 'Abductors'], secondary: ['Quadriceps', 'Glutes', 'Calves', 'Core'] },
  'Activation': { primary: ['Target Muscles'], secondary: ['Stabilizers'] },
  'Assessment': { primary: ['Full Body'], secondary: ['N/A'] },
  'Cond': { primary: ['Cardiovascular System'], secondary: ['Full Body'] },
  'Recovery': { primary: ['All Muscle Groups'], secondary: ['Fascial System'] },
};

export function getMuscleGroups(category: string): { primary: string[]; secondary: string[] } {
  return MUSCLE_GROUP_MAP[category] || { primary: ['Various'], secondary: [] };
}

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

export function getCategoryBySuperCategoryId(superCategoryId: string): string[] {
  const superCat = SUPER_CATEGORIES.find(s => s.id === superCategoryId);
  return superCat?.categories || [];
}

export function getSuperCategoryByCategoryId(categoryId: string): SuperCategory | undefined {
  const enhanced = ENHANCED_CATEGORIES[categoryId];
  if (!enhanced) return undefined;
  return SUPER_CATEGORIES.find(s => s.id === enhanced.superCategoryId);
}

export function isInCollection(exerciseCategory: string, collection: Collection): boolean {
  const criteria = collection.filterCriteria;
  
  if (criteria.categories && !criteria.categories.includes(exerciseCategory)) {
    return false;
  }
  
  // Additional filters would be applied based on exercise properties
  return true;
}

export function getCollectionColorClass(color: string): string {
  const colorMap: Record<string, string> = {
    gold: 'from-yellow-400 to-orange-500',
    green: 'from-green-400 to-emerald-500',
    blue: 'from-blue-400 to-cyan-500',
    red: 'from-red-400 to-rose-500',
    orange: 'from-orange-400 to-amber-500',
    purple: 'from-purple-400 to-violet-500',
    indigo: 'from-indigo-400 to-blue-500',
    teal: 'from-teal-400 to-cyan-500',
    slate: 'from-slate-400 to-gray-500',
    emerald: 'from-emerald-400 to-green-500',
  };
  return colorMap[color] || 'from-gray-400 to-gray-500';
}

export function getSuperCategoryColorClass(color: string): string {
  const colorMap: Record<string, string> = {
    blue: 'bg-blue-50 border-blue-200 text-blue-700',
    red: 'bg-red-50 border-red-200 text-red-700',
    green: 'bg-green-50 border-green-200 text-green-700',
    yellow: 'bg-yellow-50 border-yellow-200 text-yellow-700',
    orange: 'bg-orange-50 border-orange-200 text-orange-700',
    purple: 'bg-purple-50 border-purple-200 text-purple-700',
  };
  return colorMap[color] || 'bg-gray-50 border-gray-200 text-gray-700';
}
