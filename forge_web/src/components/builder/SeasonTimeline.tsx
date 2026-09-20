import { useCallback } from 'react';

const SEGMENTS = [
  { key: 'off_season', label: 'Off-season', color: 'bg-slate-400', activeColor: 'bg-indigo-500' },
  { key: 'pre_season', label: 'Pre-season', color: 'bg-blue-300', activeColor: 'bg-blue-600' },
  { key: 'in_season', label: 'In-season', color: 'bg-emerald-300', activeColor: 'bg-emerald-600' },
  { key: 'taper', label: 'Taper', color: 'bg-amber-300', activeColor: 'bg-amber-500' },
  { key: 'return_to_play', label: 'Return-to-play', color: 'bg-rose-300', activeColor: 'bg-rose-500' },
] as const;

const DISPLAY_LABELS: Record<string, string> = {
  off_season: 'Off-Season',
  pre_season: 'Pre-Season',
  in_season: 'In-Season',
  taper: 'Taper',
  return_to_play: 'Return-to-Play',
};

interface SeasonTimelineProps {
  value: string;
  onChange: (phase: string) => void;
}

export default function SeasonTimeline({ value, onChange }: SeasonTimelineProps) {
  return (
    <div className="flex rounded-lg overflow-hidden border border-slate-200 h-8">
      {SEGMENTS.map(({ key, label, activeColor }) => {
        const active = value === key || value === label;
        return (
          <button
            key={key}
            onClick={() => onChange(key)}
            className={`flex-1 text-[11px] font-medium transition-all border-r last:border-r-0 border-slate-200 ${
              active
                ? `${activeColor} text-white shadow-inner`
                : 'bg-white text-slate-500 hover:bg-slate-50'
            }`}
          >
            {label}
          </button>
        );
      })}
    </div>
  );
}
