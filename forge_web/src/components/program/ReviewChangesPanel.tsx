import React, { useMemo } from 'react';
import { DiffChange, diffRequests } from '../../lib/adaptationDiff';
import { Check, X, ArrowRight } from 'lucide-react';
import type { ProgramRequest } from '../../types';

interface ReviewChangesPanelProps {
  sourceRequest: ProgramRequest;
  currentRequest: ProgramRequest;
  onToggleChange: (changeId: string) => void;
  rejectedChangeIds: Set<string>;
}

const SECTION_LABELS: Record<string, string> = {
  basics: 'Athlete Details',
  context: 'Program Settings',
  advanced: 'Performance Data',
};

export function ReviewChangesPanel({ sourceRequest, currentRequest, onToggleChange, rejectedChangeIds }: ReviewChangesPanelProps) {
  const changes = useMemo(
    () => diffRequests(sourceRequest, currentRequest),
    [sourceRequest, currentRequest]
  );

  const bySection = useMemo(() => {
    const map: Record<string, DiffChange[]> = {};
    for (const c of changes) {
      if (!map[c.section]) map[c.section] = [];
      map[c.section].push(c);
    }
    return map;
  }, [changes]);

  if (changes.length === 0) return null;

  return (
    <div className="bg-amber-50 border border-amber-200 rounded-xl overflow-hidden">
      <div className="px-4 py-3 bg-amber-100/50 border-b border-amber-200 flex items-center gap-2">
        <span className="text-xs font-bold text-amber-800 uppercase tracking-wider">
          {changes.length} Change{changes.length !== 1 ? 's' : ''} from Source
        </span>
      </div>
      <div className="divide-y divide-amber-200/50">
        {Object.entries(bySection).map(([section, sectionChanges]) => (
          <div key={section}>
            <div className="px-4 py-1.5 bg-amber-100/30 text-[10px] font-bold text-amber-700 uppercase tracking-wider">
              {SECTION_LABELS[section] || section}
            </div>
            {sectionChanges.map(c => {
              const isAccepted = !rejectedChangeIds.has(c.id);
              return (
                <div key={c.id} className="px-4 py-2 flex items-start gap-3 text-sm hover:bg-amber-100/20">
                  <button
                    onClick={() => onToggleChange(c.id)}
                    className={`shrink-0 mt-0.5 w-5 h-5 rounded-full flex items-center justify-center border transition-colors ${
                      isAccepted
                        ? 'bg-emerald-500 border-emerald-500 text-white'
                        : 'bg-white border-red-300 text-red-500 hover:bg-red-50'
                    }`}
                    title={isAccepted ? 'Click to reject change' : 'Click to accept change'}
                  >
                    {isAccepted ? <Check className="w-3 h-3" /> : <X className="w-3 h-3" />}
                  </button>
                  <div className="flex-1 min-w-0">
                    <div className="font-medium text-slate-800 text-xs mb-0.5">{c.label}</div>
                    <div className="flex items-center gap-1.5 text-xs text-slate-500">
                      {isAccepted ? (
                        <>
                          <span className="line-through text-red-500">{fmt(c.oldValue)}</span>
                          <ArrowRight className="w-3 h-3 text-slate-400 shrink-0" />
                          <span className="text-emerald-600 font-medium">{fmt(c.newValue)}</span>
                        </>
                      ) : (
                        <span className="text-slate-600 font-medium">{fmt(c.oldValue)}</span>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        ))}
      </div>
    </div>
  );
}

function fmt(val: any): string {
  if (val === null || val === undefined || val === '') return '(empty)';
  if (Array.isArray(val)) return val.length ? val.join(', ') : '(empty)';
  return String(val);
}
