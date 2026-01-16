const Pagination = ({ currentPage, totalPages, onPageChange }) => {
  if (!totalPages || totalPages <= 1) return null;

  const handlePrevious = () => {
    if (currentPage > 1) {
      onPageChange(currentPage - 1);
    }
  };

  const handleNext = () => {
    if (currentPage < totalPages) {
      onPageChange(currentPage + 1);
    }
  };

  const handlePageClick = (page) => {
    if (page !== currentPage) {
      onPageChange(page);
    }
  };

  // Generate page numbers with ellipsis
  const getPageNumbers = () => {
    const pages = [];
    
    // Show first page
    if (currentPage > 3) {
      pages.push(1);
      if (currentPage > 4) {
        pages.push('ellipsis-start');
      }
    }
    
    // Show pages around current page
    const start = Math.max(1, currentPage - 2);
    const end = Math.min(totalPages, currentPage + 2);
    for (let i = start; i <= end; i++) {
      pages.push(i);
    }
    
    // Show last page
    if (currentPage < totalPages - 2) {
      if (currentPage < totalPages - 3) {
        pages.push('ellipsis-end');
      }
      pages.push(totalPages);
    }
    
    return pages;
  };

  return (
    <div className="flex justify-center items-center gap-2 mt-12">
      {/* Previous Button */}
      <button
        onClick={handlePrevious}
        disabled={currentPage === 1}
        className="px-4 py-2 bg-white/10 hover:bg-white/20 border border-white/20 rounded-md text-white text-sm font-medium transition-all disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:bg-white/10 flex items-center gap-2 backdrop-blur-sm"
      >
        <svg
          className="w-4 h-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M15 19l-7-7 7-7"
          />
        </svg>
        <span>Previous</span>
      </button>

      {/* Page Numbers */}
      <div className="flex items-center gap-1">
        {getPageNumbers().map((page, idx) => {
          if (page === 'ellipsis-start' || page === 'ellipsis-end') {
            return (
              <span key={`ellipsis-${idx}`} className="px-2 text-white/50">
                ...
              </span>
            );
          }
          
          const isActive = page === currentPage;
          return (
            <button
              key={page}
              onClick={() => handlePageClick(page)}
              className={`min-w-[40px] h-10 px-3 rounded-md text-sm font-medium transition-all ${
                isActive
                  ? 'bg-white text-black font-semibold'
                  : 'bg-white/10 hover:bg-white/20 border border-white/20 text-white backdrop-blur-sm'
              }`}
            >
              {page}
            </button>
          );
        })}
      </div>

      {/* Next Button */}
      <button
        onClick={handleNext}
        disabled={currentPage >= totalPages}
        className="px-4 py-2 bg-white/10 hover:bg-white/20 border border-white/20 rounded-md text-white text-sm font-medium transition-all disabled:opacity-30 disabled:cursor-not-allowed disabled:hover:bg-white/10 flex items-center gap-2 backdrop-blur-sm"
      >
        <span>Next</span>
        <svg
          className="w-4 h-4"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 5l7 7-7 7"
          />
        </svg>
      </button>
    </div>
  );
};

export default Pagination;

