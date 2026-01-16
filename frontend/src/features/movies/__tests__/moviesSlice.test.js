import { describe, it, expect } from 'vitest';
import moviesReducer, { fetchMovies, setFilters } from '../moviesSlice';

describe('moviesSlice', () => {
  const initialState = {
    items: [],
    status: 'pending',
    error: null,
    filters: {},
    pagination: null,
  };

  it('should return initial state', () => {
    expect(moviesReducer(undefined, { type: 'unknown' })).toEqual(initialState);
  });

  it('should handle setFilters', () => {
    const filters = { genre: 'Action', page: 1 };
    const action = setFilters(filters);
    const state = moviesReducer(initialState, action);
    expect(state.filters).toEqual(filters);
  });

  it('should handle fetchMovies.pending', () => {
    const action = fetchMovies.pending('requestId', {});
    const state = moviesReducer(initialState, action);
    expect(state.status).toBe('loading');
    expect(state.error).toBeNull();
  });

  it('should handle fetchMovies.fulfilled', () => {
    const payload = {
      results: [{ id: 1, title: 'Test Movie' }],
      pagination: { current_page: 1, total_pages: 1 },
    };
    const action = fetchMovies.fulfilled(payload, 'requestId', {});
    const state = moviesReducer(initialState, action);
    expect(state.status).toBe('succeeded');
    expect(state.items).toEqual(payload.results);
    expect(state.pagination).toEqual(payload.pagination);
  });

  it('should handle fetchMovies.rejected', () => {
    const errorMessage = 'Error message';
    const action = fetchMovies.rejected(
      { message: errorMessage },
      'requestId',
      {},
      errorMessage
    );
    const state = moviesReducer(initialState, action);
    expect(state.status).toBe('failed');
    expect(state.error).toBe(errorMessage);
  });
});

