import { useCallback, useMemo } from 'react';

const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] as const;

interface WeeklyScheduleProps {
  value: number[];
  onChange: (days: number[]) => void;
}

export default function WeeklySchedule({ value, onChange }: WeeklyScheduleProps) {
  const count = value.length;

  const toggleDay = useCallback((dayIndex: number) => {
    const next = value.includes(dayIndex)
      ? value.filter(d => d !== dayIndex)
      : [...value, dayIndex].sort((a, b) => a - b);
    onChange(next);
  }, [value, onChange]);

  return (
    <div>
      <div className="flex gap-1">
        {DAYS.map((day, i) => {
          const active = value.includes(i);
          return (
            <button
              key={day}
              onClick={() => toggleDay(i)}
              className={`flex-1 py-2 rounded-md text-xs font-medium transition-all border ${
                active
                  ? 'bg-indigo-50 border-indigo-300 text-indigo-700'
                  : 'bg-white border-slate-200 text-slate-400 hover:border-slate-300'
              }`}
            >
              {day}
            </button>
          );
        })}
      </div>
      <p className="text-[11px] text-slate-400 mt-1.5">
        {count === 0 ? 'Select training days' : `${count} session${count !== 1 ? 's' : ''} per week`}
      </p>
    </div>
  );
}
