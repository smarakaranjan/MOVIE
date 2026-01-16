# Testing Guide

This guide explains how to write and run tests for the Movie Explorer React application.

## Setup

The project uses:
- **Vitest** - Fast test runner
- **React Testing Library** - Component testing utilities
- **@testing-library/jest-dom** - Custom matchers for DOM assertions

## Running Tests

```bash
# Run tests in watch mode (recommended for development)
npm test

# Run tests once
npm test -- --run

# Run tests with UI (interactive)
npm run test:ui

# Run tests with coverage
npm run test:coverage
```

## Test File Structure

Tests are organized alongside the code they test:

```
src/
├── components/
│   ├── Navbar.jsx
│   └── __tests__/
│       └── Navbar.test.jsx
├── features/
│   └── movies/
│       ├── moviesSlice.js
│       └── __tests__/
│           └── moviesSlice.test.js
└── utils/
    ├── errorHandler.js
    └── __tests__/
        └── errorHandler.test.js
```

## Writing Tests

### Component Tests

Test components by rendering them and checking the output:

```jsx
import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import MyComponent from '../MyComponent';

// Helper for components that use React Router
const renderWithRouter = (component) => {
  return render(<BrowserRouter>{component}</BrowserRouter>);
};

describe('MyComponent', () => {
  it('renders correctly', () => {
    renderWithRouter(<MyComponent />);
    expect(screen.getByText('Expected Text')).toBeInTheDocument();
  });
});
```

### Testing User Interactions

Use `fireEvent` or `userEvent` to simulate user actions:

```jsx
import { fireEvent } from '@testing-library/react';

it('handles button click', () => {
  const handleClick = vi.fn();
  render(<Button onClick={handleClick}>Click me</Button>);
  
  fireEvent.click(screen.getByText('Click me'));
  expect(handleClick).toHaveBeenCalled();
});
```

### Testing Redux Slices

Test Redux slices by dispatching actions and checking state:

```jsx
import { describe, it, expect } from 'vitest';
import moviesReducer, { fetchMovies } from '../moviesSlice';

describe('moviesSlice', () => {
  const initialState = {
    items: [],
    status: 'idle',
    error: null,
  };

  it('handles fetchMovies.pending', () => {
    const action = fetchMovies.pending('requestId', {});
    const state = moviesReducer(initialState, action);
    expect(state.status).toBe('loading');
  });
});
```

### Testing Async Actions

Mock API calls and test async behavior:

```jsx
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { configureStore } from '@reduxjs/toolkit';
import moviesReducer, { fetchMovies } from '../moviesSlice';
import * as moviesApi from '../../../api/moviesApi';

// Mock the API
vi.mock('../../../api/moviesApi');

describe('fetchMovies thunk', () => {
  let store;

  beforeEach(() => {
    store = configureStore({
      reducer: {
        movies: moviesReducer,
      },
    });
  });

  it('fetches movies successfully', async () => {
    const mockMovies = [{ id: 1, title: 'Test Movie' }];
    moviesApi.getMovies.mockResolvedValue({ results: mockMovies });

    await store.dispatch(fetchMovies({}));
    
    const state = store.getState().movies;
    expect(state.items).toEqual(mockMovies);
    expect(state.status).toBe('succeeded');
  });
});
```

### Testing Hooks

Test custom hooks using `renderHook`:

```jsx
import { renderHook, act } from '@testing-library/react';
import { useToast } from '../useToast';

describe('useToast', () => {
  it('shows and hides toast', () => {
    const { result } = renderHook(() => useToast());
    
    act(() => {
      result.current.showToast('Test message', 'error');
    });
    
    expect(result.current.toasts).toHaveLength(1);
  });
});
```

## Common Testing Patterns

### Mocking API Calls

```jsx
import { vi } from 'vitest';
import * as api from '../api';

vi.mock('../api');

it('calls API correctly', async () => {
  api.getMovies.mockResolvedValue({ results: [] });
  // ... test code
});
```

### Testing with Redux

```jsx
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import { render } from '@testing-library/react';

const renderWithRedux = (component, { initialState = {} } = {}) => {
  const store = configureStore({
    reducer: {
      movies: moviesReducer,
    },
    preloadedState: initialState,
  });
  
  return {
    ...render(<Provider store={store}>{component}</Provider>),
    store,
  };
};
```

### Testing Router Components

```jsx
import { MemoryRouter } from 'react-router-dom';

const renderWithRouter = (component, { route = '/' } = {}) => {
  return render(
    <MemoryRouter initialEntries={[route]}>
      {component}
    </MemoryRouter>
  );
};
```

## Best Practices

1. **Test Behavior, Not Implementation**
   - Test what users see and do, not internal implementation details
   - Use `getByRole`, `getByLabelText`, `getByText` instead of `getByTestId`

2. **Keep Tests Simple**
   - One assertion per test when possible
   - Test one thing at a time

3. **Use Descriptive Test Names**
   ```jsx
   // Good
   it('displays error message when API call fails', () => {});
   
   // Bad
   it('works', () => {});
   ```

4. **Mock External Dependencies**
   - Mock API calls, timers, and browser APIs
   - Keep tests fast and isolated

5. **Clean Up After Tests**
   - Vitest automatically cleans up, but be mindful of side effects

## Available Matchers

From `@testing-library/jest-dom`:

- `toBeInTheDocument()` - Element exists in DOM
- `toHaveTextContent()` - Element has specific text
- `toHaveClass()` - Element has CSS class
- `toBeVisible()` - Element is visible
- `toBeDisabled()` - Element is disabled
- `toHaveAttribute()` - Element has attribute
- `toBeEmptyDOMElement()` - Element is empty

## Example Test Files

See these files for examples:
- `src/components/__tests__/Navbar.test.jsx` - Component with routing
- `src/components/__tests__/Pagination.test.jsx` - Component with interactions
- `src/utils/__tests__/errorHandler.test.js` - Utility function tests
- `src/features/movies/__tests__/moviesSlice.test.js` - Redux slice tests

## Debugging Tests

1. **Use `screen.debug()`** to see the rendered output:
   ```jsx
   render(<MyComponent />);
   screen.debug(); // Prints the DOM
   ```

2. **Use `screen.logTestingPlaygroundURL()`** to get testing suggestions:
   ```jsx
   screen.logTestingPlaygroundURL();
   ```

3. **Run tests in watch mode** to see changes immediately:
   ```bash
   npm test
   ```

## Coverage

Generate coverage reports:

```bash
npm run test:coverage
```

Coverage reports are generated in `coverage/` directory. Aim for:
- **Statements**: > 80%
- **Branches**: > 75%
- **Functions**: > 80%
- **Lines**: > 80%

## CI/CD Integration

Tests can be run in CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run tests
  run: npm test -- --run
```

## Troubleshooting

### Tests not finding modules
- Check import paths are correct
- Ensure `vite.config.js` has proper test configuration

### Router errors
- Wrap components with `BrowserRouter` or `MemoryRouter` in tests

### Redux errors
- Provide a store using `Provider` in test setup

### Async issues
- Use `waitFor` for async operations:
  ```jsx
  import { waitFor } from '@testing-library/react';
  
  await waitFor(() => {
    expect(screen.getByText('Loaded')).toBeInTheDocument();
  });
  ```

