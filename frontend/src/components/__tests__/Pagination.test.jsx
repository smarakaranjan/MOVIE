import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import Pagination from '../Pagination';

describe('Pagination', () => {
  it('renders nothing when totalPages is 0', () => {
    const { container } = render(
      <Pagination currentPage={1} totalPages={0} onPageChange={vi.fn()} />
    );
    expect(container.firstChild).toBeNull();
  });

  it('renders nothing when totalPages is 1', () => {
    const { container } = render(
      <Pagination currentPage={1} totalPages={1} onPageChange={vi.fn()} />
    );
    expect(container.firstChild).toBeNull();
  });

  it('renders pagination controls when totalPages > 1', () => {
    render(
      <Pagination currentPage={1} totalPages={5} onPageChange={vi.fn()} />
    );
    expect(screen.getByText('Previous')).toBeInTheDocument();
    expect(screen.getByText('Next')).toBeInTheDocument();
    expect(screen.getByText('1')).toBeInTheDocument();
  });

  it('disables Previous button on first page', () => {
    render(
      <Pagination currentPage={1} totalPages={5} onPageChange={vi.fn()} />
    );
    const prevButton = screen.getByText('Previous').closest('button');
    expect(prevButton).toBeDisabled();
  });

  it('disables Next button on last page', () => {
    render(
      <Pagination currentPage={5} totalPages={5} onPageChange={vi.fn()} />
    );
    const nextButton = screen.getByText('Next').closest('button');
    expect(nextButton).toBeDisabled();
  });

  it('calls onPageChange when clicking page number', () => {
    const handlePageChange = vi.fn();
    render(
      <Pagination currentPage={2} totalPages={5} onPageChange={handlePageChange} />
    );
    const page3 = screen.getByText('3');
    fireEvent.click(page3);
    expect(handlePageChange).toHaveBeenCalledWith(3);
  });

  it('calls onPageChange when clicking Next', () => {
    const handlePageChange = vi.fn();
    render(
      <Pagination currentPage={2} totalPages={5} onPageChange={handlePageChange} />
    );
    const nextButton = screen.getByText('Next').closest('button');
    fireEvent.click(nextButton);
    expect(handlePageChange).toHaveBeenCalledWith(3);
  });

  it('calls onPageChange when clicking Previous', () => {
    const handlePageChange = vi.fn();
    render(
      <Pagination currentPage={2} totalPages={5} onPageChange={handlePageChange} />
    );
    const prevButton = screen.getByText('Previous').closest('button');
    fireEvent.click(prevButton);
    expect(handlePageChange).toHaveBeenCalledWith(1);
  });

  it('shows ellipsis for large page counts', () => {
    render(
      <Pagination currentPage={10} totalPages={20} onPageChange={vi.fn()} />
    );
    // Ellipsis should appear when current page is far from start/end
    const ellipsis = screen.queryAllByText('...');
    expect(ellipsis.length).toBeGreaterThan(0);
  });
});

