import { describe, it, expect, beforeEach, vi } from 'vitest';
import { renderHook, act, waitFor } from '@testing-library/react';
import { useAppSettings, DEFAULT_SETTINGS } from './SettingsModal';

const STORAGE_KEY = 'forge_app_settings';

describe('useAppSettings defaults', () => {
  beforeEach(() => {
    localStorage.clear();
    document.documentElement.classList.remove('dark', 'light', 'density-compact');
    vi.restoreAllMocks();
  });

  it('defaults to dark theme and compact density for new users', () => {
    expect(DEFAULT_SETTINGS.theme).toBe('dark');
    expect(DEFAULT_SETTINGS.density).toBe('compact');

    const { result } = renderHook(() => useAppSettings());
    expect(result.current.settings.theme).toBe('dark');
    expect(result.current.settings.density).toBe('compact');
    expect(result.current.isLoaded).toBe(true);
  });

  it('applies dark + density-compact classes on first effect run (no light flash)', async () => {
    const { result } = renderHook(() => useAppSettings());
    await waitFor(() => {
      expect(document.documentElement.classList.contains('dark')).toBe(true);
      expect(document.documentElement.classList.contains('density-compact')).toBe(true);
    });
    // Settings modal itself is not open; App gates it behind isLoaded which is true.
    expect(result.current.isLoaded).toBe(true);
  });

  it('user can change theme/density later and it persists', async () => {
    const { result } = renderHook(() => useAppSettings());
    act(() => {
      result.current.updateSettings({ theme: 'light', density: 'comfortable' });
    });
    expect(result.current.settings.theme).toBe('light');
    expect(result.current.settings.density).toBe('comfortable');
    const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
    expect(stored.theme).toBe('light');
    expect(stored.density).toBe('comfortable');

    await waitFor(() => {
      expect(document.documentElement.classList.contains('light')).toBe(true);
      expect(document.documentElement.classList.contains('dark')).toBe(false);
      expect(document.documentElement.classList.contains('density-compact')).toBe(false);
    });
  });

  it('loads persisted settings over defaults on next mount', () => {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({ theme: 'system', density: 'comfortable' })
    );
    const { result } = renderHook(() => useAppSettings());
    expect(result.current.settings.theme).toBe('system');
    expect(result.current.settings.density).toBe('comfortable');
    // Unset keys still fall back to defaults
    expect(result.current.settings.animations).toBe(DEFAULT_SETTINGS.animations);
  });

  it('resetSettings restores dark + compact defaults and clears storage', () => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ theme: 'light' }));
    const { result } = renderHook(() => useAppSettings());
    act(() => result.current.resetSettings());
    expect(result.current.settings.theme).toBe('dark');
    expect(result.current.settings.density).toBe('compact');
    expect(localStorage.getItem(STORAGE_KEY)).toBeNull();
  });
});
