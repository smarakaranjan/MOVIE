import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import Toast from '../Toast';

describe('Toast', () => {
  it('renders toast message', () => {
    render(<Toast message="Test message" type="info" onClose={() => {}} />);
    expect(screen.getByText('Test message')).toBeInTheDocument();
  });

  it('renders different toast types', () => {
    const { rerender } = render(
      <Toast message="Error" type="error" onClose={() => {}} />
    );
    expect(screen.getByText('Error')).toBeInTheDocument();

    rerender(<Toast message="Success" type="success" onClose={() => {}} />);
    expect(screen.getByText('Success')).toBeInTheDocument();
  });

  it('calls onClose when close button is clicked', () => {
    const handleClose = vi.fn();
    render(<Toast message="Test" type="info" onClose={handleClose} />);
    const closeButton = screen.getByRole('button');
    fireEvent.click(closeButton);
    expect(handleClose).toHaveBeenCalled();
  });
});

