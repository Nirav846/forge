/**
 * Error Logging Service
 * Centralized error handling with logging, reporting, and user-friendly messages
 */

export type ErrorSeverity = 'low' | 'medium' | 'high' | 'critical';

export interface LoggedError {
  id: string;
  message: string;
  severity: ErrorSeverity;
  timestamp: number;
  context?: Record<string, any>;
  originalError?: Error;
  recovered: boolean;
}

class ErrorLogger {
  private errors: LoggedError[] = [];
  private maxErrors = 50;
  private listeners: Set<(error: LoggedError) => void> = new Set();

  /**
   * Log an error with context and severity
   */
  log(
    message: string,
    error?: Error,
    severity: ErrorSeverity = 'medium',
    context?: Record<string, any>
  ): LoggedError {
    const loggedError: LoggedError = {
      id: `err_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      message,
      severity,
      timestamp: Date.now(),
      context,
      originalError: error,
      recovered: false,
    };

    // Store error
    this.errors.unshift(loggedError);
    if (this.errors.length > this.maxErrors) {
      this.errors.pop();
    }

    // Notify listeners
    this.listeners.forEach(listener => listener(loggedError));

    // Console output based on severity
    const consoleMethod = severity === 'critical' ? 'error' : severity === 'high' ? 'error' : 'warn';
    console[consoleMethod](`[${severity.toUpperCase()}] ${message}`, error || '', context || '');

    // TODO: In production, send to error tracking service (Sentry, LogRocket, etc.)
    // if (import.meta.env.PROD && severity !== 'low') {
    //   this.sendToTrackingService(loggedError);
    // }

    return loggedError;
  }

  /**
   * Handle API errors with user-friendly messages
   */
  handleApiError(error: any, endpoint: string, action: string): LoggedError {
    let message = `Failed to ${action}`;
    let severity: ErrorSeverity = 'medium';

    if (error instanceof TypeError && error.message.includes('fetch')) {
      message = 'Network error. Please check your connection and try again.';
      severity = 'high';
    } else if (error?.message?.includes('HTTP 4')) {
      message = `Request failed: ${error.message}`;
      severity = 'medium';
    } else if (error?.message?.includes('HTTP 5')) {
      message = 'Server error. Please try again later.';
      severity = 'high';
    } else if (error?.message) {
      message = error.message;
    }

    return this.log(message, error, severity, { endpoint, action });
  }

  /**
   * Attempt to recover from an error with a fallback value
   */
  recover<T>(
    fn: () => T,
    fallback: T,
    errorMessage: string,
    severity: ErrorSeverity = 'low'
  ): T {
    try {
      return fn();
    } catch (error) {
      const loggedError = this.log(errorMessage, error as Error, severity);
      loggedError.recovered = true;
      return fallback;
    }
  }

  /**
   * Get recent errors
   */
  getRecentErrors(limit = 10): LoggedError[] {
    return this.errors.slice(0, limit);
  }

  /**
   * Clear all errors
   */
  clear(): void {
    this.errors = [];
  }

  /**
   * Subscribe to error events
   */
  subscribe(callback: (error: LoggedError) => void): () => void {
    this.listeners.add(callback);
    return () => this.listeners.delete(callback);
  }

  /**
   * Get error statistics
   */
  getStats(): { total: number; bySeverity: Record<ErrorSeverity, number> } {
    const stats = {
      total: this.errors.length,
      bySeverity: {
        low: 0,
        medium: 0,
        high: 0,
        critical: 0,
      } as Record<ErrorSeverity, number>,
    };

    this.errors.forEach(err => {
      stats.bySeverity[err.severity]++;
    });

    return stats;
  }

  // Private method for sending to tracking service
  private async sendToTrackingService(error: LoggedError): Promise<void> {
    // Implement integration with Sentry, LogRocket, or similar
    // Example: Sentry.captureException(error.originalError, { contexts: { error } });
    console.debug('Would send to tracking service:', error);
  }
}

// Singleton instance
export const errorLogger = new ErrorLogger();

/**
 * Higher-order function for wrapping async operations with error handling
 */
export function withErrorHandling<T extends (...args: any[]) => Promise<any>>(
  fn: T,
  errorMessage: string,
  severity: ErrorSeverity = 'medium'
): T {
  return (async (...args: Parameters<T>): Promise<ReturnType<T>> => {
    try {
      return await fn(...args);
    } catch (error) {
      errorLogger.handleApiError(error, 'unknown', errorMessage);
      throw error;
    }
  }) as T;
}

export default errorLogger;
