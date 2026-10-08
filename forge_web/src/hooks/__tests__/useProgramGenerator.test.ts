import { describe, it, expect, vi, beforeEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useProgramGenerator } from '../useProgramGenerator';

const mockGenerate = vi.fn();

vi.mock('../lib/generator', () => ({
  generateProgram: (...args: unknown[]) => mockGenerate(...args),
}));

describe('useProgramGenerator', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockGenerate.mockReset();
  });

  it('should initialize with default values', () => {
    const { result } = renderHook(() => useProgramGenerator());
    
    expect(result.current.isGenerating).toBe(false);
    expect(result.current.generationError).toBeNull();
    expect(result.current.generatedProgram).toBeNull();
  });

  it('should handle generation error', async () => {
    mockGenerate.mockRejectedValue(new Error('Generation failed'));

    const { result } = renderHook(() => useProgramGenerator());

    await act(async () => {
      try {
        await result.current.generateProgram({
          sport: 'Rugby',
          position: 'Prop',
          week: 1,
          day: 1,
        });
      } catch (e) {
        // Expected error
      }
    });

    expect(result.current.generationError).toBe('Generation failed');
  });

  it('should clear errors on demand', () => {
    const { result } = renderHook(() => useProgramGenerator());

    act(() => {
      result.current.clearError();
    });

    expect(result.current.generationError).toBeNull();
  });

  it('should set generating state during generation', async () => {
    let resolvePromise: (value: unknown) => void;
    const pendingPromise = new Promise(resolve => {
      resolvePromise = resolve;
    });
    mockGenerate.mockReturnValue(pendingPromise);

    const { result } = renderHook(() => useProgramGenerator());

    act(() => {
      result.current.generateProgram({
        sport: 'Rugby',
        position: 'Prop',
        week: 1,
        day: 1,
      }).catch(() => {});
    });

    expect(result.current.isGenerating).toBe(true);

    act(() => {
      resolvePromise?.({ exercises: [] });
    });

    await waitFor(() => {
      expect(result.current.isGenerating).toBe(false);
    });
  });
});
