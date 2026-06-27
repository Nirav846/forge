import { useCallback } from 'react';

const PRESETS = [45, 60, 75] as const;

interface SessionLengthSliderProps {
  value: number;
  onChange: (minutes: number) => void;
}

export default function SessionLengthSlider({ value, onChange }: SessionLengthSliderProps) {
  return (
    <div className="space-y-2">
      <input
        type="range"
        min={30}
        max={90}
        step={5}
        value={value}
        onChange={e => onChange(Number(e.target.value))}
        className="w-full h-1.5 bg-slate-200 rounded-full appearance-none cursor-pointer accent-indigo-500 [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:bg-indigo-500 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:shadow-sm"
      />
      <div className="flex items-center justify-between">
        <span className="text-xs text-slate-500 font-medium">{value} min</span>
        <div className="flex gap-1.5">
          {PRESETS.map(p => (
            <button
              key={p}
              onClick={() => onChange(p)}
              className={`px-2 py-0.5 rounded text-[11px] font-medium transition-all border ${
                value === p
                  ? 'bg-indigo-50 border-indigo-300 text-indigo-700'
                  : 'bg-white border-slate-200 text-slate-400 hover:border-slate-300'
              }`}
            >
              {p}m
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
