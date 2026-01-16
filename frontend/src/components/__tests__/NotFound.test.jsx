import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import NotFound from '../NotFound';

const renderWithRouter = (component) => {
  return render(<BrowserRouter>{component}</BrowserRouter>);
};

describe('NotFound', () => {
  it('renders 404 heading', () => {
    renderWithRouter(<NotFound />);
    expect(screen.getByText('404')).toBeInTheDocument();
  });

  it('renders page not found message', () => {
    renderWithRouter(<NotFound />);
    expect(screen.getByText('Page Not Found')).toBeInTheDocument();
  });

  it('renders navigation links', () => {
    renderWithRouter(<NotFound />);
    expect(screen.getByText('Go to Movies')).toBeInTheDocument();
    expect(screen.getByText('Go to Actors')).toBeInTheDocument();
    expect(screen.getByText('Go to Directors')).toBeInTheDocument();
  });

  it('has correct links', () => {
    renderWithRouter(<NotFound />);
    const moviesLink = screen.getByText('Go to Movies').closest('a');
    const actorsLink = screen.getByText('Go to Actors').closest('a');
    const directorsLink = screen.getByText('Go to Directors').closest('a');

    expect(moviesLink).toHaveAttribute('href', '/');
    expect(actorsLink).toHaveAttribute('href', '/actors');
    expect(directorsLink).toHaveAttribute('href', '/directors');
  });
});

