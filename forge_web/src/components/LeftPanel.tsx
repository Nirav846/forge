import React from 'react';
import { ProgramRequest, Mode } from '../types';
import { isFieldVisible } from '../lib/fieldConfig';
import { Settings2, Zap, Play } from 'lucide-react';
import { AppStatus } from '../App';

interface LeftPanelProps {
  request: ProgramRequest;
  setRequest: React.Dispatch<React.SetStateAction<ProgramRequest>>;
  onGenerate: () => void;
  status: AppStatus;
}

export default function LeftPanel({ request, setRequest, onGenerate, status }: LeftPanelProps) {
  const isGenerating = status === 'loading';
  const mode = request.mode;
  
  const updateBasics = (field: keyof ProgramRequest['basics'], value: any) => {
    setRequest(prev => ({ ...prev, basics: { ...prev.basics, [field]: value } }));
  };

  const updateContext = (field: keyof ProgramRequest['context'], value: any) => {
    setRequest(prev => ({ ...prev, context: { ...prev.context, [field]: value } }));
  };

  const updateAdvanced = (field: keyof ProgramRequest['advanced'], value: any) => {
    setRequest(prev => ({ ...prev, advanced: { ...prev.advanced, [field]: value } }));
  };

  const setMode = (mode: Mode) => {
    setRequest(prev => ({ ...prev, mode }));
  };

  return (
    <div className="flex flex-col h-full">
      {/* Top sticky section with Mode Toggle and Generate Button */}
      <div className="sticky top-0 bg-white border-b border-slate-200 p-5 z-20 shadow-sm">
        <div className="flex bg-slate-100 p-1 rounded-lg mb-4">
          <button
            onClick={() => setMode('core')}
            className={`flex-1 py-1.5 text-xs font-medium rounded-md transition-all ${request.mode === 'core' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
          >
            Core Mode
          </button>
          <button
            onClick={() => setMode('premium')}
            className={`flex-1 py-1.5 text-xs font-medium rounded-md transition-all flex items-center justify-center gap-1 ${request.mode === 'premium' ? 'bg-indigo-50 text-indigo-700 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
          >
            <Settings2 className="w-3 h-3" /> Premium
          </button>
        </div>

        <button
          onClick={onGenerate}
          disabled={isGenerating || !request.basics.athlete_name}
          className="w-full bg-slate-900 hover:bg-slate-800 disabled:bg-slate-300 disabled:cursor-not-allowed text-white py-2.5 rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-2"
        >
          {isGenerating ? (
            <span className="flex items-center gap-2"><Zap className="w-4 h-4 animate-pulse" /> Generating...</span>
          ) : (
             <span className="flex items-center gap-2"><Play className="w-4 h-4" /> Generate Program</span>
          )}
        </button>
      </div>

      {/* Scrollable Form */}
      <div className="p-5 space-y-8 flex-1">
        
        {/* Section A: Basics */}
        <section className="space-y-4">
          <h2 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Athlete Basics</h2>
          
          <div className="space-y-3">
            {isFieldVisible(mode, 'basics', 'athlete_name') && (
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Athlete Name</label>
                <input 
                  type="text" 
                  value={request.basics.athlete_name} 
                  onChange={e => updateBasics('athlete_name', e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white transition-all"
                  placeholder="e.g. John Doe"
                />
              </div>
            )}
            
            <div className="grid grid-cols-2 gap-3">
              {isFieldVisible(mode, 'basics', 'sport') && (
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Sport</label>
                  <input 
                    type="text" 
                    value={request.basics.sport} 
                    onChange={e => updateBasics('sport', e.target.value)}
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white"
                  />
                </div>
              )}
              {isFieldVisible(mode, 'basics', 'role') && (
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Role/Position</label>
                  <input 
                    type="text" 
                    value={request.basics.role} 
                    onChange={e => updateBasics('role', e.target.value)}
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white"
                  />
                </div>
              )}
            </div>

            <div className="grid grid-cols-2 gap-3">
              {isFieldVisible(mode, 'basics', 'age') && (
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Age</label>
                  <input 
                    type="number" 
                    value={request.basics.age} 
                    onChange={e => updateBasics('age', parseInt(e.target.value) || '')}
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white"
                  />
                </div>
              )}
              {isFieldVisible(mode, 'basics', 'level') && (
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Level</label>
                  <select 
                    value={request.basics.level}
                    onChange={e => updateBasics('level', e.target.value)}
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white"
                  >
                    <option value="Beginner">Beginner</option>
                    <option value="Intermediate">Intermediate</option>
                    <option value="Advanced">Advanced</option>
                  </select>
                </div>
              )}
            </div>
            
            <div className="grid grid-cols-2 gap-3">
               {isFieldVisible(mode, 'basics', 'frequency_per_week') && (
                 <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Freq (days/wk)</label>
                  <input 
                    type="number" 
                    value={request.basics.frequency_per_week} 
                    onChange={e => updateBasics('frequency_per_week', parseInt(e.target.value) || 3)}
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white"
                  />
                </div>
               )}
              {isFieldVisible(mode, 'basics', 'days_to_match') && (
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Days to Match</label>
                  <input 
                    type="number" 
                    value={request.basics.days_to_match} 
                    onChange={e => updateBasics('days_to_match', parseInt(e.target.value) || '')}
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white"
                  />
                </div>
              )}
            </div>
          </div>
        </section>

        {/* Section B: Context */}
        <section className="space-y-4">
          <h2 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Program Goal & Context</h2>
          <div className="space-y-3">
            {isFieldVisible(mode, 'context', 'primary_goal') && (
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Primary Goal</label>
                <input 
                  type="text" 
                  value={request.context.primary_goal} 
                  onChange={e => updateContext('primary_goal', e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white transition-all"
                  placeholder="e.g. Max Force, Hypertrophy"
                />
              </div>
            )}
            {isFieldVisible(mode, 'context', 'competition_proximity_note') && (
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Competition Proximity Note</label>
                <textarea 
                  value={request.context.competition_proximity_note} 
                  onChange={e => updateContext('competition_proximity_note', e.target.value)}
                  rows={2}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white resize-none"
                  placeholder="e.g. Tapering for playoffs..."
                />
              </div>
            )}
          </div>
        </section>

        {/* Section D: Advanced Profile */}
        {isFieldVisible(mode, 'advanced') && (
          <section className="space-y-4 pt-4 border-t border-slate-100">
            <h2 className="text-xs font-bold text-indigo-400 uppercase tracking-wider flex items-center gap-1">
               <Settings2 className="w-3 h-3" /> Premium Profiling
            </h2>
            <div className="space-y-3">
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">F-V Profile</label>
                <select 
                  value={request.advanced.force_velocity_profile}
                  onChange={e => updateAdvanced('force_velocity_profile', e.target.value)}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white"
                >
                  <option value="">Unknown</option>
                  <option value="Force Deficit">Force Deficit</option>
                  <option value="Velocity Deficit">Velocity Deficit</option>
                  <option value="Balanced">Balanced</option>
                </select>
              </div>

               <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">10m Sprint Band</label>
                  <input 
                    type="text" 
                    value={request.advanced.sprint_10m_band} 
                    onChange={e => updateAdvanced('sprint_10m_band', e.target.value)}
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white"
                    placeholder="e.g. <1.65s"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1">Squat Strength</label>
                  <input 
                    type="text" 
                    value={request.advanced.squat_strength_band} 
                    onChange={e => updateAdvanced('squat_strength_band', e.target.value)}
                    className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white"
                    placeholder="e.g. >2.0x BW"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Injury Risk Flags (Comma separated)</label>
                <input 
                  type="text" 
                  value={request.advanced.injury_risk_flags.join(', ')} 
                  onChange={e => updateAdvanced('injury_risk_flags', e.target.value.split(',').map(s=>s.trim()).filter(Boolean))}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white"
                  placeholder="e.g. Lumbar Spine, Right Shoulder"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Prior Block Summary</label>
                <textarea 
                  value={request.advanced.prior_block_summary} 
                  onChange={e => updateAdvanced('prior_block_summary', e.target.value)}
                  rows={2}
                  className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white resize-none"
                  placeholder="Feedback on previous block..."
                />
              </div>

            </div>
          </section>
        )}

      </div>
    </div>
  );
}
