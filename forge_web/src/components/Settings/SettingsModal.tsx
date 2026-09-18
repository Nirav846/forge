import { useState, useEffect, useCallback } from 'react';
import { Moon, Sun, Monitor, Trash2, Code, Bell, BellOff, LayoutGrid, LayoutList, X } from 'lucide-react';

export type ThemeMode = 'light' | 'dark' | 'system';
export type DensityMode = 'comfortable' | 'compact';

export interface AppSettings {
  theme: ThemeMode;
  density: DensityMode;
  devMode: boolean;
  notifications: boolean;
  animations: boolean;
}

const DEFAULT_SETTINGS: AppSettings = {
  theme: 'light',
  density: 'comfortable',
  devMode: false,
  notifications: true,
  animations: true,
};

const STORAGE_KEY = 'forge_app_settings';

export function useAppSettings() {
  const [settings, setSettings] = useState<AppSettings>(DEFAULT_SETTINGS);
  const [isLoaded, setIsLoaded] = useState(false);

  // Load settings from localStorage on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored) as Partial<AppSettings>;
        setSettings(prev => ({ ...prev, ...parsed }));
      }
    } catch (e) {
      console.error('Failed to load settings:', e);
    }
    setIsLoaded(true);
  }, []);

  // Apply theme to document
  useEffect(() => {
    if (!isLoaded) return;

    const root = document.documentElement;
    const applyTheme = (theme: ThemeMode) => {
      root.classList.remove('light', 'dark');
      
      if (theme === 'system') {
        const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        root.classList.add(systemDark ? 'dark' : 'light');
      } else {
        root.classList.add(theme);
      }
    };

    applyTheme(settings.theme);

    // Listen for system theme changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = () => {
      if (settings.theme === 'system') {
        applyTheme('system');
      }
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [settings.theme, isLoaded]);

  // Apply density mode
  useEffect(() => {
    if (!isLoaded) return;
    
    const root = document.documentElement;
    if (settings.density === 'compact') {
      root.classList.add('density-compact');
    } else {
      root.classList.remove('density-compact');
    }
  }, [settings.density, isLoaded]);

  // Save settings to localStorage
  const saveSettings = useCallback((newSettings: Partial<AppSettings>) => {
    setSettings(prev => {
      const updated = { ...prev, ...newSettings };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
      return updated;
    });
  }, []);

  // Reset to defaults
  const resetSettings = useCallback(() => {
    localStorage.removeItem(STORAGE_KEY);
    setSettings(DEFAULT_SETTINGS);
  }, []);

  // Clear all app data (settings + other localStorage items)
  const clearAllData = useCallback(() => {
    const keysToRemove = [
      STORAGE_KEY,
      'forge_dev_mode',
      'forge_current_workout',
      'forge_favorites',
      'forge_coach_preferences',
      'forge_uat_results',
    ];
    keysToRemove.forEach(key => localStorage.removeItem(key));
    setSettings(DEFAULT_SETTINGS);
  }, []);

  return {
    settings,
    updateSettings: saveSettings,
    resetSettings,
    clearAllData,
    isLoaded,
  };
}

interface SettingsModalProps {
  isOpen: boolean;
  onClose: () => void;
  settings: AppSettings;
  updateSettings: (settings: Partial<AppSettings>) => void;
  resetSettings: () => void;
  clearAllData: () => void;
}

export function SettingsModal({ isOpen, onClose, settings, updateSettings, resetSettings, clearAllData }: SettingsModalProps) {
  const [activeTab, setActiveTab] = useState<'appearance' | 'preferences' | 'data'>('appearance');
  const [showConfirmClear, setShowConfirmClear] = useState(false);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />
      
      {/* Modal */}
      <div className="relative bg-white dark:bg-slate-900 rounded-2xl shadow-2xl w-full max-w-md mx-4 overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-slate-200 dark:border-slate-700">
          <h2 className="text-xl font-bold text-slate-900 dark:text-white">Settings</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg transition-colors"
          >
            <X className="w-5 h-5 text-slate-500 dark:text-slate-400" />
          </button>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-200 dark:border-slate-700">
          <button
            onClick={() => setActiveTab('appearance')}
            className={`flex-1 py-3 text-sm font-medium transition-colors ${
              activeTab === 'appearance'
                ? 'text-indigo-600 dark:text-indigo-400 border-b-2 border-indigo-600 dark:border-indigo-400'
                : 'text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300'
            }`}
          >
            Appearance
          </button>
          <button
            onClick={() => setActiveTab('preferences')}
            className={`flex-1 py-3 text-sm font-medium transition-colors ${
              activeTab === 'preferences'
                ? 'text-indigo-600 dark:text-indigo-400 border-b-2 border-indigo-600 dark:border-indigo-400'
                : 'text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300'
            }`}
          >
            Preferences
          </button>
          <button
            onClick={() => setActiveTab('data')}
            className={`flex-1 py-3 text-sm font-medium transition-colors ${
              activeTab === 'data'
                ? 'text-indigo-600 dark:text-indigo-400 border-b-2 border-indigo-600 dark:border-indigo-400'
                : 'text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-300'
            }`}
          >
            Data
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {activeTab === 'appearance' && (
            <>
              {/* Theme Selection */}
              <div>
                <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
                  Theme
                </label>
                <div className="grid grid-cols-3 gap-3">
                  <button
                    onClick={() => updateSettings({ theme: 'light' })}
                    className={`flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-all ${
                      settings.theme === 'light'
                        ? 'border-indigo-600 bg-indigo-50 dark:bg-indigo-900/20'
                        : 'border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600'
                    }`}
                  >
                    <Sun className={`w-6 h-6 ${settings.theme === 'light' ? 'text-indigo-600' : 'text-slate-400'}`} />
                    <span className={`text-xs font-medium ${settings.theme === 'light' ? 'text-indigo-700 dark:text-indigo-300' : 'text-slate-500 dark:text-slate-400'}`}>
                      Light
                    </span>
                  </button>
                  <button
                    onClick={() => updateSettings({ theme: 'dark' })}
                    className={`flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-all ${
                      settings.theme === 'dark'
                        ? 'border-indigo-600 bg-indigo-50 dark:bg-indigo-900/20'
                        : 'border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600'
                    }`}
                  >
                    <Moon className={`w-6 h-6 ${settings.theme === 'dark' ? 'text-indigo-600' : 'text-slate-400'}`} />
                    <span className={`text-xs font-medium ${settings.theme === 'dark' ? 'text-indigo-700 dark:text-indigo-300' : 'text-slate-500 dark:text-slate-400'}`}>
                      Dark
                    </span>
                  </button>
                  <button
                    onClick={() => updateSettings({ theme: 'system' })}
                    className={`flex flex-col items-center gap-2 p-4 rounded-xl border-2 transition-all ${
                      settings.theme === 'system'
                        ? 'border-indigo-600 bg-indigo-50 dark:bg-indigo-900/20'
                        : 'border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600'
                    }`}
                  >
                    <Monitor className={`w-6 h-6 ${settings.theme === 'system' ? 'text-indigo-600' : 'text-slate-400'}`} />
                    <span className={`text-xs font-medium ${settings.theme === 'system' ? 'text-indigo-700 dark:text-indigo-300' : 'text-slate-500 dark:text-slate-400'}`}>
                      System
                    </span>
                  </button>
                </div>
              </div>

              {/* Density Selection */}
              <div>
                <label className="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-3">
                  Display Density
                </label>
                <div className="grid grid-cols-2 gap-3">
                  <button
                    onClick={() => updateSettings({ density: 'comfortable' })}
                    className={`flex items-center gap-3 p-4 rounded-xl border-2 transition-all ${
                      settings.density === 'comfortable'
                        ? 'border-indigo-600 bg-indigo-50 dark:bg-indigo-900/20'
                        : 'border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600'
                    }`}
                  >
                    <LayoutGrid className={`w-5 h-5 ${settings.density === 'comfortable' ? 'text-indigo-600' : 'text-slate-400'}`} />
                    <span className={`text-sm font-medium ${settings.density === 'comfortable' ? 'text-indigo-700 dark:text-indigo-300' : 'text-slate-500 dark:text-slate-400'}`}>
                      Comfortable
                    </span>
                  </button>
                  <button
                    onClick={() => updateSettings({ density: 'compact' })}
                    className={`flex items-center gap-3 p-4 rounded-xl border-2 transition-all ${
                      settings.density === 'compact'
                        ? 'border-indigo-600 bg-indigo-50 dark:bg-indigo-900/20'
                        : 'border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600'
                    }`}
                  >
                    <LayoutList className={`w-5 h-5 ${settings.density === 'compact' ? 'text-indigo-600' : 'text-slate-400'}`} />
                    <span className={`text-sm font-medium ${settings.density === 'compact' ? 'text-indigo-700 dark:text-indigo-300' : 'text-slate-500 dark:text-slate-400'}`}>
                      Compact
                    </span>
                  </button>
                </div>
              </div>
            </>
          )}

          {activeTab === 'preferences' && (
            <div className="space-y-4">
              {/* Developer Mode */}
              <div className="flex items-center justify-between p-4 bg-slate-50 dark:bg-slate-800 rounded-xl">
                <div className="flex items-center gap-3">
                  <Code className="w-5 h-5 text-slate-500 dark:text-slate-400" />
                  <div>
                    <p className="text-sm font-medium text-slate-900 dark:text-white">Developer Mode</p>
                    <p className="text-xs text-slate-500 dark:text-slate-400">Enable advanced debugging features</p>
                  </div>
                </div>
                <button
                  onClick={() => {
                    updateSettings({ devMode: !settings.devMode });
                    localStorage.setItem('forge_dev_mode', String(!settings.devMode));
                  }}
                  className={`relative w-12 h-6 rounded-full transition-colors ${
                    settings.devMode ? 'bg-indigo-600' : 'bg-slate-300 dark:bg-slate-600'
                  }`}
                >
                  <div
                    className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform ${
                      settings.devMode ? 'left-7' : 'left-1'
                    }`}
                  />
                </button>
              </div>

              {/* Notifications */}
              <div className="flex items-center justify-between p-4 bg-slate-50 dark:bg-slate-800 rounded-xl">
                <div className="flex items-center gap-3">
                  {settings.notifications ? (
                    <Bell className="w-5 h-5 text-slate-500 dark:text-slate-400" />
                  ) : (
                    <BellOff className="w-5 h-5 text-slate-500 dark:text-slate-400" />
                  )}
                  <div>
                    <p className="text-sm font-medium text-slate-900 dark:text-white">Notifications</p>
                    <p className="text-xs text-slate-500 dark:text-slate-400">Show action confirmations</p>
                  </div>
                </div>
                <button
                  onClick={() => updateSettings({ notifications: !settings.notifications })}
                  className={`relative w-12 h-6 rounded-full transition-colors ${
                    settings.notifications ? 'bg-indigo-600' : 'bg-slate-300 dark:bg-slate-600'
                  }`}
                >
                  <div
                    className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform ${
                      settings.notifications ? 'left-7' : 'left-1'
                    }`}
                  />
                </button>
              </div>

              {/* Animations */}
              <div className="flex items-center justify-between p-4 bg-slate-50 dark:bg-slate-800 rounded-xl">
                <div>
                  <p className="text-sm font-medium text-slate-900 dark:text-white">Animations</p>
                  <p className="text-xs text-slate-500 dark:text-slate-400">Enable motion and transitions</p>
                </div>
                <button
                  onClick={() => updateSettings({ animations: !settings.animations })}
                  className={`relative w-12 h-6 rounded-full transition-colors ${
                    settings.animations ? 'bg-indigo-600' : 'bg-slate-300 dark:bg-slate-600'
                  }`}
                >
                  <div
                    className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-transform ${
                      settings.animations ? 'left-7' : 'left-1'
                    }`}
                  />
                </button>
              </div>

              {/* Reset Button */}
              <button
                onClick={resetSettings}
                className="w-full mt-4 py-3 px-4 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-xl text-sm font-medium transition-colors"
              >
                Reset to Defaults
              </button>
            </div>
          )}

          {activeTab === 'data' && (
            <div className="space-y-4">
              <div className="p-4 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-xl">
                <p className="text-sm text-amber-800 dark:text-amber-200">
                  <strong>Warning:</strong> Clearing data will remove all locally saved information including favorites, workout drafts, and preferences. This action cannot be undone.
                </p>
              </div>

              {!showConfirmClear ? (
                <button
                  onClick={() => setShowConfirmClear(true)}
                  className="w-full py-3 px-4 bg-red-600 hover:bg-red-700 text-white rounded-xl text-sm font-medium transition-colors flex items-center justify-center gap-2"
                >
                  <Trash2 className="w-4 h-4" />
                  Clear All Local Data
                </button>
              ) : (
                <div className="space-y-3">
                  <p className="text-sm font-medium text-slate-900 dark:text-white text-center">
                    Are you sure? This will delete all local data.
                  </p>
                  <div className="grid grid-cols-2 gap-3">
                    <button
                      onClick={() => setShowConfirmClear(false)}
                      className="py-2 px-4 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 rounded-lg text-sm font-medium transition-colors"
                    >
                      Cancel
                    </button>
                    <button
                      onClick={() => {
                        clearAllData();
                        setShowConfirmClear(false);
                      }}
                      className="py-2 px-4 bg-red-600 hover:bg-red-700 text-white rounded-lg text-sm font-medium transition-colors"
                    >
                      Yes, Clear All
                    </button>
                  </div>
                </div>
              )}

              <div className="pt-4 border-t border-slate-200 dark:border-slate-700">
                <p className="text-xs text-slate-500 dark:text-slate-400 mb-2">Stored data includes:</p>
                <ul className="text-xs text-slate-500 dark:text-slate-400 space-y-1">
                  <li>• Application settings</li>
                  <li>• Favorite exercises</li>
                  <li>• Workout builder drafts</li>
                  <li>• Coach preferences</li>
                  <li>• UAT test results</li>
                </ul>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-4 bg-slate-50 dark:bg-slate-800 border-t border-slate-200 dark:border-slate-700">
          <p className="text-xs text-slate-500 dark:text-slate-400 text-center">
            FORGE Coach Console v1.0
          </p>
        </div>
      </div>
    </div>
  );
}
