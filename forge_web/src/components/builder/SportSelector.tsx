import { useCallback } from 'react';
import {
  Footprints, Telescope, Radio, Trophy, Goal, Shield, CircleDot, Activity
} from 'lucide-react';

const SPORTS = [
  { id: 'Cricket', label: 'Cricket', icon: Telescope },
  { id: 'Badminton', label: 'Badminton', icon: Footprints },
  { id: 'Tennis', label: 'Tennis', icon: Radio },
  { id: 'Volleyball', label: 'Volleyball', icon: Activity },
  { id: 'Football', label: 'Football', icon: Goal },
  { id: 'Rugby', label: 'Rugby', icon: Shield },
  { id: 'Soccer', label: 'Soccer', icon: CircleDot },
  { id: 'Basketball', label: 'Basketball', icon: Trophy },
] as const;

interface SportSelectorProps {
  value: string;
  onChange: (sport: string) => void;
}

export default function SportSelector({ value, onChange }: SportSelectorProps) {
  return (
    <div className="grid grid-cols-2 gap-2">
      {SPORTS.map(({ id, label, icon: Icon }) => (
        <button
          key={id}
          onClick={() => onChange(id)}
          className={`flex items-center gap-2 px-3 py-2.5 rounded-lg text-xs font-medium transition-all border ${
            value === id
              ? 'bg-indigo-50 border-indigo-300 text-indigo-700 shadow-sm'
              : 'bg-white border-slate-200 text-slate-600 hover:border-slate-300 hover:bg-slate-50'
          }`}
        >
          <Icon className="w-4 h-4 shrink-0" />
          {label}
        </button>
      ))}
    </div>
  );
}
