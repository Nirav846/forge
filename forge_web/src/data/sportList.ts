export const SUPPORTED_SPORTS = ['Badminton', 'Cricket', 'Football', 'Rugby Union', 'Soccer', 'Tennis', 'Volleyball'] as const;
export type SupportedSport = typeof SUPPORTED_SPORTS[number];
export const SPORT_OPTIONS = [...SUPPORTED_SPORTS, 'Other'];
