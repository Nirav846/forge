import React from 'react';
import { Users, ArrowRight, Plus } from 'lucide-react';
import { TemplateType } from './HomePage';

interface TemplateInfo {
  id: TemplateType;
  sport: string;
  role: string;
  description: string;
  icon: string;
  category: string;
}

interface RoleTemplatesSectionProps {
  templates: TemplateInfo[];
  onSelectTemplate: (template: TemplateType) => void;
  onStartFresh: () => void;
}

export function RoleTemplatesSection({ 
  templates, 
  onSelectTemplate, 
  onStartFresh 
}: RoleTemplatesSectionProps) {
  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
          <Users className="w-5 h-5 text-indigo-600" />
          Start from Role Template
        </h3>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {templates.map(t => (
          <button
            key={t.id}
            onClick={() => onSelectTemplate(t.id)}
            className="group bg-white border border-slate-200 hover:border-indigo-300 hover:bg-indigo-50/50 rounded-xl p-5 text-left transition-all hover:shadow-md"
          >
            <div className="text-3xl mb-3">{t.icon}</div>
            <div className="font-bold text-slate-900 group-hover:text-indigo-900 mb-1">
              {t.sport}
            </div>
            <div className="text-sm font-medium text-indigo-600 mb-2">{t.role}</div>
            <div className="text-xs text-slate-500 line-clamp-2">{t.description}</div>
            <div className="mt-3 flex items-center gap-2">
              <span className="text-xs font-medium text-slate-400 bg-slate-100 px-2 py-1 rounded-full">
                {t.category}
              </span>
              <ArrowRight className="w-3 h-3 text-slate-300 group-hover:text-indigo-500 transition-colors" />
            </div>
          </button>
        ))}
      </div>

      {/* Start Fresh Link */}
      <div className="text-center pt-4 pb-8">
        <button
          onClick={onStartFresh}
          className="text-sm text-slate-500 hover:text-indigo-600 transition-colors flex items-center justify-center gap-2 group"
        >
          <Plus className="w-4 h-4 group-hover:scale-110 transition-transform" />
          Start Fresh — build from scratch
        </button>
      </div>
    </div>
  );
}
