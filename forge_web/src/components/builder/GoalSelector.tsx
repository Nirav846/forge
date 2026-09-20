const GOALS = ['Speed', 'Power', 'Strength', 'Hypertrophy', 'Maintenance', 'Conditioning'] as const;

interface GoalSelectorProps {
  value: string;
  onChange: (goal: string) => void;
}

export default function GoalSelector({ value, onChange }: GoalSelectorProps) {
  return (
    <div className="flex flex-wrap gap-1.5">
      {GOALS.map(g => (
        <button
          key={g}
          onClick={() => onChange(g)}
          className={`px-3 py-1.5 rounded-md text-xs font-medium transition-all border ${
            value === g
              ? 'bg-indigo-50 border-indigo-300 text-indigo-700'
              : 'bg-white border-slate-200 text-slate-500 hover:border-slate-300 hover:bg-slate-50'
          }`}
        >
          {g}
        </button>
      ))}
    </div>
  );
}
