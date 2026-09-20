import React, { useState, useMemo } from 'react';
import { Search, Plus, X } from 'lucide-react';

const EXERCISE_LIBRARY: { name: string; family: string }[] = [
  { name: 'Barbell Back Squat', family: 'Squat' },
  { name: 'Front Squat', family: 'Squat' },
  { name: 'Goblet Squat', family: 'Squat' },
  { name: 'Safety Bar Box Squat', family: 'Squat' },
  { name: 'Bulgarian Split Squat', family: 'Unilateral Leg' },
  { name: 'Rear Foot Elevated Split Squat', family: 'Unilateral Leg' },
  { name: 'Walking Lunge', family: 'Unilateral Leg' },
  { name: 'Conventional Deadlift', family: 'Hinge' },
  { name: 'Romanian Deadlift', family: 'Hinge' },
  { name: 'Trap Bar Deadlift', family: 'Hinge' },
  { name: 'Nordic Hamstring Curl', family: 'Eccentric' },
  { name: 'Bench Press', family: 'Horizontal Push' },
  { name: 'Floor Press', family: 'Horizontal Push' },
  { name: 'Incline Bench Press', family: 'Horizontal Push' },
  { name: 'Overhead Press', family: 'Vertical Push' },
  { name: 'Landmine Press', family: 'Push' },
  { name: 'Pendlay Row', family: 'Horizontal Pull' },
  { name: 'Bent Over Row', family: 'Horizontal Pull' },
  { name: 'Lat Pulldown', family: 'Vertical Pull' },
  { name: 'Pull Up', family: 'Vertical Pull' },
  { name: 'Chin Up', family: 'Vertical Pull' },
  { name: 'Med Ball Rotational Throw', family: 'Power' },
  { name: 'Medicine Ball Slam', family: 'Power' },
  { name: 'Box Jump', family: 'Plyo' },
  { name: 'Pogo Jumps', family: 'Plyo' },
  { name: 'Drop Lunge', family: 'Deceleration' },
  { name: 'Broad Jump', family: 'Plyo' },
  { name: 'Pallof Press', family: 'Anti-Rotation' },
  { name: 'Cable Chop', family: 'Rotational Core' },
  { name: 'Hanging Leg Raise', family: 'Core' },
  { name: 'Plank', family: 'Core' },
  { name: 'Dead Bug', family: 'Core' },
  { name: 'Farmer Carry', family: 'Locomotion' },
  { name: 'Sled Push', family: 'Locomotion' },
  { name: 'Sled Pull', family: 'Locomotion' },
  { name: 'Band Pull Apart', family: 'Pre-hab' },
  { name: 'Face Pull', family: 'Pre-hab' },
  { name: 'Y-T-W Raise', family: 'Pre-hab' },
  { name: 'Cat-Cow', family: 'Mobility' },
  { name: "World's Greatest Stretch", family: 'Mobility' },
  { name: 'Lateral Lunge', family: 'Mobility' },
  { name: 'Hip Flexor Stretch', family: 'Mobility' },
  { name: 'Isometric Hamstring Hold', family: 'Activation' },
  { name: 'Glute Bridge', family: 'Activation' },
  { name: 'Clam Shells', family: 'Activation' },
];

const ALL_FAMILIES = [...new Set(EXERCISE_LIBRARY.map(e => e.family))].sort();

export default function ExerciseLibraryModal({ onClose, onSelect }: { onClose: () => void; onSelect: (exercise: { name: string; family: string }) => void }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [familyFilter, setFamilyFilter] = useState('all');

  const filtered = useMemo(() => {
    return EXERCISE_LIBRARY.filter(ex => {
      const matchesSearch = !searchTerm.trim() ||
        ex.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        ex.family.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesFamily = familyFilter === 'all' || ex.family === familyFilter;
      return matchesSearch && matchesFamily;
    });
  }, [searchTerm, familyFilter]);

  return (
    <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 flex items-center justify-center" onClick={onClose}>
      <div className="bg-white rounded-2xl shadow-2xl w-[560px] max-h-[85vh] flex flex-col" onClick={e => e.stopPropagation()}>
        <div className="flex items-center justify-between gap-3 p-4 border-b border-slate-200">
          <div className="flex items-center gap-2 flex-1">
            <Search className="w-4 h-4 text-slate-400 shrink-0" />
            <input type="text" value={searchTerm} onChange={e => setSearchTerm(e.target.value)}
              placeholder="Search exercises by name or category..."
              className="flex-1 text-sm focus:outline-none text-slate-800 placeholder-slate-400"
              autoFocus />
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 text-sm font-semibold shrink-0">Cancel</button>
        </div>

        <div className="flex items-center gap-2 px-4 py-2 border-b border-slate-100 bg-slate-50">
          <select value={familyFilter} onChange={e => setFamilyFilter(e.target.value)}
            className="text-xs border border-slate-200 rounded-md px-2 py-1 bg-white text-slate-700 focus:outline-none focus:ring-1 focus:ring-indigo-300">
            <option value="all">All Families</option>
            {ALL_FAMILIES.map(f => (
              <option key={f} value={f}>{f}</option>
            ))}
          </select>
          <span className="text-xs text-slate-400 ml-auto">{filtered.length} exercise{filtered.length !== 1 ? 's' : ''}</span>
        </div>

        <div className="flex-1 overflow-y-auto p-2">
          {filtered.length === 0 ? (
            <div className="text-center py-8 text-sm text-slate-400 italic">No exercises match your search.</div>
          ) : (
            <div className="space-y-0.5">
              {filtered.map((ex, i) => (
                <button key={i} onClick={() => onSelect(ex)}
                  className="w-full flex items-center justify-between px-3 py-2.5 rounded-lg hover:bg-indigo-50 transition-colors text-left group">
                  <div className="flex items-center gap-3">
                    <div>
                      <div className="text-sm font-medium text-slate-800 group-hover:text-indigo-700">{ex.name}</div>
                      <div className="text-xs text-slate-400">{ex.family}</div>
                    </div>
                  </div>
                  <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-300 bg-slate-100 px-2 py-0.5 rounded shrink-0">{ex.family}</span>
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
