import React from 'react';
import { Loader2, Check, AlertCircle } from 'lucide-react';

export type SaveState = 'idle' | 'saving' | 'saved' | 'error';

export function SaveIndicator({ state }: { state: SaveState }) {
  if (state === 'idle') return null;
  return (
    <span className="inline-flex items-center gap-1 text-xs font-medium transition-opacity duration-150">
      {state === 'saving' && (
        <>
          <Loader2 className="w-3 h-3 animate-spin text-slate-400" />
          <span className="text-slate-400">Saving...</span>
        </>
      )}
      {state === 'saved' && (
        <>
          <Check className="w-3 h-3 text-emerald-500" />
          <span className="text-emerald-600">Saved</span>
        </>
      )}
      {state === 'error' && (
        <>
          <AlertCircle className="w-3 h-3 text-red-500" />
          <span className="text-red-600">Save failed</span>
        </>
 )}
    </span>
  );
}
