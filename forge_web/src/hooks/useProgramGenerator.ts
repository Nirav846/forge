/**
 * Custom hook for program generation with error handling and loading states
 */
import { useState, useCallback } from 'react';
import { ProgramRequest } from '../types';
import { TransformationResult } from '../types/ui';
import { generateProgram as apiGenerate } from '../lib/api';
import { generateProgramMock } from '../lib/mockApi';
import { normalizeProgramResponse } from '../lib/transformers';
import { errorLogger } from '../lib/errorLogger';

export type GenerationStatus = 'idle' | 'loading' | 'success' | 'error';

interface UseProgramGeneratorReturn {
  status: GenerationStatus;
  result: TransformationResult | null;
  errorMessage: string | null;
  generateProgram: (request: ProgramRequest, useMockFallback?: boolean) => Promise<void>;
  clearError: () => void;
  clearResult: () => void;
}

export function useProgramGenerator(): UseProgramGeneratorReturn {
  const [status, setStatus] = useState<GenerationStatus>('idle');
  const [result, setResult] = useState<TransformationResult | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const generateProgram = useCallback(async (
    request: ProgramRequest,
    useMockFallback: boolean = false
  ) => {
    setStatus('loading');
    setErrorMessage(null);

    try {
      let rawPayload: any;

      if (useMockFallback) {
        rawPayload = await generateProgramMock(request);
      } else {
        rawPayload = await apiGenerate(request);
      }

      const transformed = normalizeProgramResponse(rawPayload);
      setResult(transformed);
      setStatus('success');
    } catch (err: any) {
      console.error("Program generation failed", err);
      
      // Log the error centrally
      errorLogger.handleApiError(err, '/api/programs/generate', 'generate program');
      
      // If real API fails, try mock fallback automatically
      if (!useMockFallback) {
        try {
          errorLogger.log('API failed, attempting mock fallback', undefined, 'medium', { 
            originalError: err.message 
          });
          
          const rawPayload = await generateProgramMock(request);
          const transformed = normalizeProgramResponse(rawPayload);
          setResult(transformed);
          setStatus('success');
          errorLogger.log('Successfully recovered with mock data', undefined, 'low');
          return;
        } catch (fallbackErr: any) {
          errorLogger.log('Mock fallback also failed', fallbackErr as Error, 'high');
        }
      }
      
      const errorMsg = err.message || 'Unknown generation error occurred.';
      setErrorMessage(errorMsg);
      setStatus('error');
    }
  }, []);

  const clearError = useCallback(() => {
    setErrorMessage(null);
    if (status === 'error') {
      setStatus('idle');
    }
  }, [status]);

  const clearResult = useCallback(() => {
    setResult(null);
    setStatus('idle');
    setErrorMessage(null);
  }, []);

  return {
    status,
    result,
    errorMessage,
    generateProgram,
    clearError,
    clearResult,
  };
}
