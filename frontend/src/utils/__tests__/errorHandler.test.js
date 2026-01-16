import { describe, it, expect } from 'vitest';
import { getErrorMessage, getErrorCode } from '../errorHandler';

describe('errorHandler', () => {
  describe('getErrorMessage', () => {
    it('handles custom backend error format', () => {
      const error = {
        response: {
          data: {
            error: {
              message: 'Custom error message',
            },
          },
        },
      };
      expect(getErrorMessage(error)).toBe('Custom error message');
    });

    it('handles DRF error format', () => {
      const error = {
        response: {
          data: {
            detail: 'DRF error message',
          },
        },
      };
      expect(getErrorMessage(error)).toBe('DRF error message');
    });

    it('handles validation errors array', () => {
      const error = {
        response: {
          data: {
            release_year: ['This field is required.'],
          },
        },
      };
      expect(getErrorMessage(error)).toBe('Release Year: This field is required.');
    });

    it('handles network errors', () => {
      const error = {
        message: 'Network Error',
      };
      expect(getErrorMessage(error)).toBe('Network Error');
    });

    it('handles unknown error format', () => {
      const error = {};
      expect(getErrorMessage(error)).toBe('Failed to process request. Please try again later.');
    });
  });

  describe('getErrorCode', () => {
    it('extracts error code from custom format', () => {
      const error = {
        response: {
          data: {
            error: {
              code: 'NOT_FOUND',
            },
          },
        },
      };
      expect(getErrorCode(error)).toBe('NOT_FOUND');
    });

    it('returns null when no code present', () => {
      const error = {
        response: {
          data: {
            detail: 'Some error',
          },
        },
      };
      expect(getErrorCode(error)).toBeNull();
    });
  });
});

