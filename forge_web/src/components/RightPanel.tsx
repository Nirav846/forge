import React, { useState } from 'react';
import { ProgramRequest } from '../types';
import { TransformationResult } from '../types/ui';
import { Code, FileJson, AlertCircle, TerminalSquare, BrainCircuit, Wrench } from 'lucide-react';

interface RightPanelProps {
  result: TransformationResult | null;
  request: ProgramRequest;
}

export default function RightPanel({ result, request }: RightPanelProps) {
  const [topMode, setTopMode] = useState<'coach' | 'engineering'>('coach');
  const [activeDebugTab, setActiveDebugTab] = useState<'warnings' | 'input' | 'raw' | 'output'>('input');

  return (
    <div className="flex flex-col h-full bg-slate-900 border-l border-slate-800">
      
      {/* Top Mode Toggle */}
      <div className="flex p-2 bg-slate-950 border-b border-slate-800 shrink-0">
         <div className="flex bg-slate-900 rounded-lg p-1 w-full border border-slate-700">
            <button 
               onClick={() => setTopMode('coach')}
               className={`flex-1 py-1.5 text-xs font-semibold rounded-md flex items-center justify-center gap-1.5 transition-all ${topMode === 'coach' ? 'bg-indigo-600 text-white shadow-sm' : 'text-slate-400 hover:text-slate-200'}`}
            >
               <BrainCircuit className="w-3.5 h-3.5" /> Intelligence
            </button>
            <button 
               onClick={() => setTopMode('engineering')}
               className={`flex-1 py-1.5 text-xs font-semibold rounded-md flex items-center justify-center gap-1.5 transition-all ${topMode === 'engineering' ? 'bg-indigo-600 text-white shadow-sm' : 'text-slate-400 hover:text-slate-200'}`}
            >
               <Wrench className="w-3.5 h-3.5" /> Engineering
            </button>
         </div>
      </div>

      {topMode === 'coach' && (
         <div className="flex-1 overflow-y-auto p-5 hide-scrollbar bg-slate-900 text-slate-300">
            {!result?.viewModel ? (
               <div className="text-center text-slate-500 italic mt-12 text-sm">
                  Generate a program to view coaching intelligence and logic traces.
               </div>
            ) : (
               <div className="space-y-8">
                  <div className="border-b border-slate-800 pb-2">
                     <h2 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
                        FORGE Engine Reasoning
                     </h2>
                     <p className="text-xs text-slate-400 mt-1">Insight into blueprint selection, substitutions and scaling logic.</p>
                  </div>
                  
                  {/* Validation Notes */}
                  {result.viewModel.validation.length > 0 && (
                     <div>
                        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">Model Validation</h3>
                        <div className="space-y-2">
                           {result.viewModel.validation.map((v, i) => (
                              <div key={i} className={`p-3 rounded-md text-sm border flex items-start gap-2
                                 ${v.type === 'error' ? 'bg-red-900/20 border-red-900/50 text-red-200' : 
                                   v.type === 'warning' ? 'bg-amber-900/20 border-amber-900/50 text-amber-200' : 
                                   'bg-sky-900/20 border-sky-900/50 text-sky-200'}`
                              }>
                                <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
                                <div>{v.message}</div>
                              </div>
                           ))}
                        </div>
                     </div>
                  )}

                  {/* Optimization Log */}
                  <div>
                     <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">Rationale & Substitutions</h3>
                     <ul className="space-y-3">
                        {result.viewModel.rationale.length === 0 ? (
                           <li className="text-sm text-slate-500 italic">Standard generation, no unique overrides.</li>
                        ) : result.viewModel.rationale.map((rat, i) => (
                           <li key={i} className="text-sm text-slate-300 bg-slate-800/50 p-3 rounded-lg border border-slate-700/50 shadow-inner">
                              {rat}
                           </li>
                        ))}
                     </ul>
                  </div>

                  {/* Personalization Factors */}
                  <div>
                     <h3 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">Personalization Applied</h3>
                     <ul className="space-y-3">
                        {result.viewModel.personalization_notes.length === 0 ? (
                           <li className="text-sm text-slate-500 italic">No advanced profile inputs applied.</li>
                        ) : result.viewModel.personalization_notes.map((note, i) => (
                           <li key={i} className="text-sm text-slate-300 bg-emerald-900/10 p-3 rounded-lg border border-emerald-900/30">
                              {note}
                           </li>
                        ))}
                     </ul>
                  </div>

               </div>
            )}
         </div>
      )}

      {topMode === 'engineering' && (
         <div className="flex flex-col h-full overflow-hidden">
            {/* Engineer Tabs */}
            <div className="flex bg-slate-950 p-1 border-b border-slate-800 shrink-0 overflow-x-auto hide-scrollbar">
               <button 
                onClick={() => setActiveDebugTab('input')}
                className={`px-3 py-2 text-xs font-medium rounded-md whitespace-nowrap transition-colors flex items-center gap-1.5 flex-1 justify-center ${activeDebugTab === 'input' ? 'bg-slate-800 text-white' : 'text-slate-400 hover:text-slate-200'}`}
              >
                 <Code className="w-3.5 h-3.5" /> Req JSON
              </button>
              <button 
                onClick={() => setActiveDebugTab('warnings')}
                className={`px-3 py-2 text-xs font-medium rounded-md whitespace-nowrap transition-colors flex items-center gap-1.5 flex-1 justify-center ${activeDebugTab === 'warnings' ? 'bg-slate-800 text-white' : 'text-slate-400 hover:text-slate-200'}`}
              >
                <TerminalSquare className="w-3.5 h-3.5" /> Transform
                {result && result.warnings.length > 0 && (
                   <span className="bg-amber-500/20 text-amber-400 px-1.5 py-0.5 rounded text-[10px] ml-1">{result.warnings.length}</span>
                )}
              </button>
               <button 
                onClick={() => setActiveDebugTab('raw')}
                disabled={!result}
                className={`px-3 py-2 text-xs font-medium rounded-md whitespace-nowrap transition-colors flex items-center gap-1.5 flex-1 justify-center ${activeDebugTab === 'raw' ? 'bg-slate-800 text-white' : 'text-slate-400 hover:text-slate-200 disabled:opacity-50 disabled:cursor-not-allowed'}`}
              >
                 <FileJson className="w-3.5 h-3.5" /> Raw API
              </button>
              <button 
                onClick={() => setActiveDebugTab('output')}
                disabled={!result?.viewModel}
                className={`px-3 py-2 text-xs font-medium rounded-md whitespace-nowrap transition-colors flex items-center gap-1.5 flex-1 justify-center ${activeDebugTab === 'output' ? 'bg-slate-800 text-white' : 'text-slate-400 hover:text-slate-200 disabled:opacity-50 disabled:cursor-not-allowed'}`}
              >
                 <FileJson className="w-3.5 h-3.5" /> UI Model
              </button>
            </div>

            {/* Engineer Content */}
            <div className="flex-1 overflow-y-auto p-4 hide-scrollbar">
               {activeDebugTab === 'warnings' && (
                  <div className="space-y-6">
                     <div className="border-b border-slate-800 pb-2">
                        <h3 className="text-xs uppercase font-bold tracking-wider text-slate-500 mb-1">Transformer Log</h3>
                        <p className="text-slate-400 text-xs text-balance">Review how the frontend normalization layer mutated the raw payload for UI safety.</p>
                     </div>
                     
                     {!result ? (
                        <div className="text-slate-500 italic text-sm text-center mt-10">Generate a program to view logs.</div>
                     ) : result.warnings.length === 0 ? (
                        <div className="text-emerald-500 text-sm flex items-center"><AlertCircle className="w-4 h-4 mr-2"/> Clean Transform: No interventions needed.</div>
                     ) : (
                        <div className="space-y-3">
                           {result.warnings.map((w, i) => (
                              <div key={i} className="bg-slate-800/50 p-3 rounded-lg border border-amber-900/30 text-xs">
                                 <div className="flex items-center text-amber-400 font-mono mb-1.5 font-bold">
                                    {w.path}
                                 </div>
                                 <div className="text-slate-300 font-medium mb-1">Issue: <span className="font-normal text-slate-400">{w.issue}</span></div>
                                 <div className="text-slate-300 font-medium">Action: <span className="font-normal text-emerald-400/80">{w.action_taken}</span></div>
                              </div>
                           ))}
                        </div>
                     )}
                  </div>
               )}

               {activeDebugTab === 'input' && (
                  <div className="space-y-4">
                     <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                        <h3 className="text-xs uppercase font-bold tracking-wider text-slate-500">Request Payload</h3>
                     </div>
                     <pre className="text-[10px] sm:text-xs font-mono text-slate-300 bg-slate-950 p-3 rounded-lg overflow-x-auto border border-slate-800 leading-relaxed shadow-inner">
                        {JSON.stringify(request, null, 2)}
                     </pre>
                  </div>
               )}

               {activeDebugTab === 'raw' && result && (
                  <div className="space-y-4">
                     <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                        <h3 className="text-xs uppercase font-bold tracking-wider text-slate-500">Raw API Output</h3>
                     </div>
                     <div className="bg-slate-800/50 p-3 text-xs text-slate-400 rounded-md mb-2 leading-relaxed">
                        The exact dirty JSON captured directly from the simulated Python backend prior to normalization.
                     </div>
                     <pre className="text-[10px] sm:text-xs font-mono text-slate-400 bg-slate-950 p-3 rounded-lg overflow-x-auto border border-slate-800 leading-relaxed shadow-inner">
                        {JSON.stringify(result.rawPayload, null, 2)}
                     </pre>
                  </div>
               )}

               {activeDebugTab === 'output' && result && result.viewModel && (
                  <div className="space-y-4">
                     <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                        <h3 className="text-xs uppercase font-bold tracking-wider text-slate-500">UI ViewModel</h3>
                     </div>
                     <div className="bg-emerald-900/10 p-3 text-xs text-emerald-500/80 rounded-md mb-2 leading-relaxed border border-emerald-900/20">
                        The sanitized shape supplied to React components. Arrays are guaranteed to exist.
                     </div>
                     <pre className="text-[10px] sm:text-xs font-mono text-slate-300 bg-slate-950 p-3 rounded-lg overflow-x-auto border border-emerald-900/30 leading-relaxed shadow-inner">
                        {JSON.stringify(result.viewModel, null, 2)}
                     </pre>
                  </div>
               )}

            </div>
         </div>
      )}
    </div>
  );
}
