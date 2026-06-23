export * from './types/api';
export * from './types/ui';

import { RawAthleteBasics, RawProgramContext, RawAdvancedProfile, RawProgramRequest } from './types/api';
import { ProgramViewModel } from './types/ui';

// Aliases for backwards compatibility in existing frontend files
export type AthleteBasics = RawAthleteBasics;
export type ProgramContext = RawProgramContext;
export type AdvancedProfile = RawAdvancedProfile;
export type ProgramRequest = RawProgramRequest;
export type ProgramResponse = ProgramViewModel; // UI assumes ProgramResponse = the transformed view model

