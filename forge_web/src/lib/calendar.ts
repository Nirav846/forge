/**
 * Simple calendar utilities for FORGE web app.
 */

export function daysToNumbers(days: string | number | (string | number)[]): number[] {
  if (typeof days === 'number') {
    return [days];
  }
  if (typeof days === 'string') {
    const trimmed = days.trim();
    if (trimmed === '') {
      return [];
    }
    // Handle comma-separated or space-separated values
    return trimmed
      .split(/[,\s]+/)
      .map(d => parseInt(d.trim(), 10))
      .filter(n => !isNaN(n));
  }
  if (Array.isArray(days)) {
    return days.map(d => typeof d === 'string' ? parseInt(d, 10) : d).filter(n => !isNaN(n));
  }
  return [];
}

export function formatDayName(dayNumber: number): string {
  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  return days[dayNumber % 7] || `Day ${dayNumber}`;
}

export function formatDayShort(dayNumber: number): string {
  const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  return days[dayNumber % 7] || `D${dayNumber}`;
}
