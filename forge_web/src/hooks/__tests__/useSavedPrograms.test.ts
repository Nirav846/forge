import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act, waitFor } from '@testing-library/react';
import { useSavedPrograms } from '../useSavedPrograms';

vi.mock('../lib/storage', () => ({
  saveArtifact: vi.fn(),
  loadArtifact: vi.fn(),
  deleteArtifact: vi.fn(),
  duplicateArtifact: vi.fn(),
  updateArtifact: vi.fn(),
}));

describe('useSavedPrograms', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should initialize with default values', () => {
    const { result } = renderHook(() => useSavedPrograms());
    
    expect(result.current.isSaving).toBe(false);
    expect(result.current.isLoading).toBe(false);
    expect(result.current.isDeleting).toBe(false);
    expect(result.current.saveError).toBeNull();
    expect(result.current.loadError).toBeNull();
    expect(result.current.deleteError).toBeNull();
  });

  it('should handle save error', async () => {
    const { saveArtifact } = await import('../lib/storage');
    vi.mocked(saveArtifact).mockRejectedValue(new Error('Save failed'));

    const { result } = renderHook(() => useSavedPrograms());

    await act(async () => {
      await result.current.saveProgram({
        id: 'test-id',
        athlete_display_name: 'Test Athlete',
        blueprint_label: 'Test Program',
        sport: 'Rugby',
        position: 'Prop',
        week: 1,
        day: 1,
        exercises: [],
        notes: '',
        status: 'draft',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      });
    });

    expect(result.current.saveError).toBe('Save failed');
  });

  it('should clear errors on demand', () => {
    const { result } = renderHook(() => useSavedPrograms());

    act(() => {
      result.current.clearErrors();
    });

    expect(result.current.saveError).toBeNull();
    expect(result.current.loadError).toBeNull();
    expect(result.current.deleteError).toBeNull();
  });
});
