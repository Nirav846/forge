import React from 'react';
import { Filter } from 'lucide-react';

interface SmartCollection {
  id: string;
  name: string;
  icon: React.ComponentType<{ className?: string }>;
  color: string;
  description: string;
  filter: (ex: any) => boolean;
  count: number;
}

interface SmartCollectionsGridProps {
  smartCollections: SmartCollection[];
  collectionCounts: Record<string, number>;
  onCollectionClick: (collectionId: string) => void;
  onOpenLibrary: () => void;
}

export function SmartCollectionsGrid({ 
  smartCollections, 
  collectionCounts, 
  onCollectionClick,
  onOpenLibrary 
}: SmartCollectionsGridProps) {
  return (
    <div>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
          <Filter className="w-5 h-5 text-indigo-600" />
          Smart Collections
        </h3>
        <button
          onClick={onOpenLibrary}
          className="text-sm text-indigo-600 hover:text-indigo-700 font-medium"
        >
          View All →
        </button>
      </div>
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        {smartCollections.map((collection) => {
          const Icon = collection.icon;
          return (
            <button
              key={collection.id}
              onClick={() => onCollectionClick(collection.id)}
              className="group bg-white border border-slate-200 hover:border-slate-300 rounded-xl p-4 text-left transition-all hover:shadow-md hover:-translate-y-0.5"
            >
              <div className={`w-10 h-10 bg-gradient-to-br ${collection.color} rounded-lg flex items-center justify-center mb-3 group-hover:scale-110 transition-transform shadow-sm`}>
                <Icon className="w-5 h-5 text-white" />
              </div>
              <div className="font-semibold text-slate-900 text-sm mb-1">{collection.name}</div>
              <div className="text-xs text-slate-500 mb-2 line-clamp-2">{collection.description}</div>
              <div className="text-xs font-medium text-slate-400 bg-slate-100 inline-block px-2 py-1 rounded-full">
                {collectionCounts[collection.id] || 0} exercises
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
