import { ProgramRequest, ProgramResponse } from '../types';
import { normalizeProgramResponse } from './transformers';
import { mockBackendResponses, defaultEmptyRequest } from './mockFixtures';

// Re-export this for backwards compatibility with LeftPanel state init
export { defaultEmptyRequest };

/**
 * Mocks the backend API request.
 * Instead of returning perfect data, it simulating receiving a dirty payload
 * from a Python backend and running it through the transformer.
 */
export async function generateProgramMock(request: ProgramRequest): Promise<any> {
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 1500));

  // Determine what fake payload to return based on inputs
  let rawPayload = mockBackendResponses.base;
  const sportType = request.basics.sport.toLowerCase();

  if (sportType.includes('rugby')) {
    rawPayload = mockBackendResponses.rugby_prop;
  } else if (sportType.includes('tennis')) {
    rawPayload = mockBackendResponses.tennis_singles;
  } else if (sportType.includes('cricket')) {
    rawPayload = mockBackendResponses.cricket_bowler;
  } else if (request.basics.athlete_name.toLowerCase() === 'error') {
     // A way to test the error state explicitly
     throw new Error("Simulated Backend Timeout 504 - The server failed to respond in time.");
  } else if (request.basics.athlete_name.toLowerCase() === 'broken') {
     // Return a malformed response to test transformer safety
     rawPayload = mockBackendResponses.malformed_fake_error;
  }

  // Update dynamic fields to make it feel responsive
  const adjustedPayload = {
     ...rawPayload,
     summary: {
        ...rawPayload.summary,
        weekly_frequency: request.basics.frequency_per_week || rawPayload.summary.weekly_frequency,
        competition_window: request.basics.days_to_match ? `${request.basics.days_to_match} days out` : rawPayload.summary.competition_window,
     }
  };

  // Run through normalization layer
  // Actually, we return the raw payload now, so App.tsx can hold both the raw and the normalized via TransformationResult
  return adjustedPayload;
}
