import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Navbar from '../Navbar';

// Helper to render with router
const renderWithRouter = (component) => {
  return render(<BrowserRouter>{component}</BrowserRouter>);
};

describe('Navbar', () => {
  it('renders the logo and brand name', () => {
    renderWithRouter(<Navbar />);
    expect(screen.getByText('Movie Explorer')).toBeInTheDocument();
  });

  it('renders all navigation links', () => {
    renderWithRouter(<Navbar />);
    expect(screen.getByText('Movies')).toBeInTheDocument();
    expect(screen.getByText('Actors')).toBeInTheDocument();
    expect(screen.getByText('Directors')).toBeInTheDocument();
  });

  it('has correct links for navigation', () => {
    renderWithRouter(<Navbar />);
    const moviesLink = screen.getByText('Movies').closest('a');
    const actorsLink = screen.getByText('Actors').closest('a');
    const directorsLink = screen.getByText('Directors').closest('a');

    expect(moviesLink).toHaveAttribute('href', '/');
    expect(actorsLink).toHaveAttribute('href', '/actors');
    expect(directorsLink).toHaveAttribute('href', '/directors');
  });
});

