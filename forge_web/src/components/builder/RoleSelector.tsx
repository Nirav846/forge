import { useMemo } from 'react';
import { roleProfiles } from '../../data/roleProfiles';
import { User } from 'lucide-react';

interface RoleSelectorProps {
  sport: string;
  value: string;
  onChange: (role: string) => void;
}

/** Map user-facing sport labels to internal sport names used in roleProfiles */
const SPORT_ALIAS: Record<string, string> = {
  Cricket: 'Cricket',
  Badminton: 'Badminton',
  Tennis: 'Tennis',
  Volleyball: 'Volleyball',
  Football: 'Football',
  Rugby: 'Rugby Union',
  Soccer: 'Soccer',
  Basketball: 'Basketball',
};

export default function RoleSelector({ sport, value, onChange }: RoleSelectorProps) {
  const internalSport = SPORT_ALIAS[sport] || sport;

  const roles = useMemo(() => {
    if (!sport) return [];
    const sportRoles = roleProfiles.filter(p => p.sport === internalSport);
    if (sportRoles.length === 0) {
      return [{ role: 'General', primaryDemands: ['General athletic development'], priorityMovements: [] }];
    }
    return sportRoles.map(p => ({
      role: p.role,
      primaryDemands: p.primaryDemands.slice(0, 2),
      priorityMovements: p.priorityMovements.slice(0, 2),
    }));
  }, [sport, internalSport]);

  if (!sport) return null;

  return (
    <div className="grid grid-cols-1 gap-1.5">
      {roles.map(({ role, primaryDemands }) => (
        <button
          key={role}
          onClick={() => onChange(role)}
          className={`flex items-start gap-2.5 px-3 py-2.5 rounded-lg text-left transition-all border ${
            value === role
              ? 'bg-indigo-50 border-indigo-300 text-indigo-700 shadow-sm'
              : 'bg-white border-slate-200 text-slate-600 hover:border-slate-300 hover:bg-slate-50'
          }`}
        >
          <User className="w-4 h-4 mt-0.5 shrink-0" />
          <div className="min-w-0">
            <div className="text-xs font-medium">{role}</div>
            <div className="text-[11px] text-slate-400 leading-tight mt-0.5 line-clamp-2">
              {primaryDemands[0] || 'General athletic development'}
            </div>
          </div>
        </button>
      ))}
    </div>
  );
}
