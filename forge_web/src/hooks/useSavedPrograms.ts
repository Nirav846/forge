/**
 * Custom hook for managing saved programs with error handling
 */
import { useState, useCallback } from 'react';
import type { SavedProgramArtifact, ProgramStatus } from '../types/ui';
import { 
  saveArtifact as apiSave, 
  loadArtifact as apiLoad, 
  deleteArtifact as apiDelete, 
  duplicateArtifact as apiDuplicate, 
  updateArtifact as apiPatch 
} from '../lib/api';
import { errorLogger } from '../lib/errorLogger';

interface UseSavedProgramsReturn {
  isSaving: boolean;
  isLoading: boolean;
  isDeleting: boolean;
  saveError: string | null;
  loadError: string | null;
  deleteError: string | null;
  saveProgram: (payload: {
    request_payload: any;
    response_payload: any;
    program_id?: string;
    status?: string;
    coach_notes?: string;
    internal_notes?: string;
  }) => Promise<SavedProgramArtifact | null>;
  loadProgram: (id: string) => Promise<any | null>;
  deleteProgram: (id: string) => Promise<boolean>;
  duplicateProgram: (id: string) => Promise<any | null>;
  updateNotes: (id: string, notes: string, field: 'coach_notes' | 'internal_notes') => Promise<boolean>;
  updateStatus: (id: string, status: ProgramStatus) => Promise<boolean>;
  clearErrors: () => void;
}

export function useSavedPrograms(): UseSavedProgramsReturn {
  const [isSaving, setIsSaving] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [deleteError, setDeleteError] = useState<string | null>(null);

  const saveProgram = useCallback(async (payload: {
    request_payload: any;
    response_payload: any;
    program_id?: string;
    status?: string;
    coach_notes?: string;
    internal_notes?: string;
  }): Promise<SavedProgramArtifact | null> => {
    setIsSaving(true);
    setSaveError(null);

    try {
      const saved = await apiSave(payload);
      return saved;
    } catch (err: any) {
      errorLogger.handleApiError(err, '/api/programs', 'save program');
      setSaveError(err.message || 'Failed to save program');
      return null;
    } finally {
      setIsSaving(false);
    }
  }, []);

  const loadProgram = useCallback(async (id: string): Promise<any | null> => {
    setIsLoading(true);
    setLoadError(null);

    try {
      const artifact = await apiLoad(id);
      return artifact;
    } catch (err: any) {
      errorLogger.handleApiError(err, `/api/programs/${id}`, 'load program');
      setLoadError(err.message || 'Failed to load program');
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const deleteProgram = useCallback(async (id: string): Promise<boolean> => {
    setIsDeleting(true);
    setDeleteError(null);

    try {
      await apiDelete(id);
      return true;
    } catch (err: any) {
      errorLogger.handleApiError(err, `/api/programs/${id}`, 'delete program');
      setDeleteError(err.message || 'Failed to delete program');
      return false;
    } finally {
      setIsDeleting(false);
    }
  }, []);

  const duplicateProgram = useCallback(async (id: string): Promise<any | null> => {
    setIsSaving(true);
    setSaveError(null);

    try {
      const dup = await apiDuplicate(id);
      return dup;
    } catch (err: any) {
      errorLogger.handleApiError(err, `/api/programs/${id}/duplicate`, 'duplicate program');
      setSaveError(err.message || 'Failed to duplicate program');
      return null;
    } finally {
      setIsSaving(false);
    }
  }, []);

  const updateNotes = useCallback(async (
    id: string, 
    notes: string, 
    field: 'coach_notes' | 'internal_notes'
  ): Promise<boolean> => {
    try {
      const updated = await apiPatch(id, { [field]: notes });
      return true;
    } catch (err: any) {
      errorLogger.handleApiError(err, `/api/programs/${id}`, 'update notes');
      return false;
    }
  }, []);

  const updateStatus = useCallback(async (id: string, status: ProgramStatus): Promise<boolean> => {
    try {
      const updated = await apiPatch(id, { status });
      return true;
    } catch (err: any) {
      errorLogger.handleApiError(err, `/api/programs/${id}`, 'update status');
      return false;
    }
  }, []);

  const clearErrors = useCallback(() => {
    setSaveError(null);
    setLoadError(null);
    setDeleteError(null);
  }, []);

  return {
    isSaving,
    isLoading,
    isDeleting,
    saveError,
    loadError,
    deleteError,
    saveProgram,
    loadProgram,
    deleteProgram,
    duplicateProgram,
    updateNotes,
    updateStatus,
    clearErrors,
  };
}
