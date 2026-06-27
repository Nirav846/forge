/// <reference types="vite/client" />
import type { ProgramRequest } from '../types';

const API_BASE = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000';

async function apiFetch(path: string, options?: RequestInit): Promise<any> {
  const url = `${API_BASE}${path}`;
  const res = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
  });
  if (!res.ok) {
    let detail = `HTTP ${res.status}`;
    try {
      const body = await res.json();
      detail = body?.detail?.message || body?.message || JSON.stringify(body);
    } catch {
      detail = res.statusText || detail;
    }
    throw new Error(detail);
  }
  return res.json();
}

export async function generateProgram(request: ProgramRequest): Promise<any> {
  return apiFetch('/api/programs/generate', {
    method: 'POST',
    body: JSON.stringify(request),
  });
}

export async function saveArtifact(payload: {
  request_payload: ProgramRequest;
  response_payload: any;
  program_id?: string;
  status?: string;
  coach_notes?: string;
  internal_notes?: string;
}): Promise<any> {
  return apiFetch('/api/programs', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function listArtifacts(): Promise<{ artifacts: any[] }> {
  return apiFetch('/api/programs');
}

export async function loadArtifact(programId: string): Promise<any> {
  return apiFetch(`/api/programs/${programId}`);
}

export async function deleteArtifact(programId: string): Promise<any> {
  return apiFetch(`/api/programs/${programId}`, {
    method: 'DELETE',
  });
}

export async function updateArtifact(programId: string, fields: Record<string, any>): Promise<any> {
  return apiFetch(`/api/programs/${programId}`, {
    method: 'PATCH',
    body: JSON.stringify(fields),
  });
}

export async function duplicateArtifact(programId: string): Promise<any> {
  return apiFetch(`/api/programs/${programId}/duplicate`, {
    method: 'POST',
    body: JSON.stringify({}),
  });
}

// ── Team Template API ───────────────────────────────────────────────

export async function createTeamTemplate(payload: Record<string, any>): Promise<any> {
  return apiFetch('/api/teams/templates', {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}

export async function listTeamTemplates(): Promise<{ templates: any[] }> {
  return apiFetch('/api/teams/templates');
}

export async function loadTeamTemplate(templateId: string): Promise<any> {
  return apiFetch(`/api/teams/templates/${templateId}`);
}

export async function updateTeamTemplate(templateId: string, fields: Record<string, any>): Promise<any> {
  return apiFetch(`/api/teams/templates/${templateId}`, {
    method: 'PUT',
    body: JSON.stringify(fields),
  });
}

export async function deleteTeamTemplate(templateId: string): Promise<any> {
  return apiFetch(`/api/teams/templates/${templateId}`, {
    method: 'DELETE',
  });
}

export async function adaptTeamTemplate(templateId: string, payload: Record<string, any>): Promise<any> {
  return apiFetch(`/api/teams/templates/${templateId}/adapt`, {
    method: 'POST',
    body: JSON.stringify(payload),
  });
}
