import { useState, useRef, useEffect } from "react";

const InfiniteScrollSelect = ({
  value,
  onChange,
  options = [],
  placeholder = "Select...",
  className = "",
  onLoadMore,
  hasMore = false,
  loading = false,
  name,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const dropdownRef = useRef(null);
  const listRef = useRef(null);

  // Filter options based on search term, exclude "All" options from dropdown list
  const filteredOptions = options.filter((option) => {
    const matchesSearch = option.name.toLowerCase().includes(searchTerm.toLowerCase());
    const isAllOption = option.id === "" || option.name.startsWith("All ");
    return matchesSearch && !isAllOption;
  });
  
  // Get the "All" option separately
  const allOption = options.find((opt) => opt.id === "" || opt.name.startsWith("All "));

  // Handle scroll to load more
  useEffect(() => {
    const listElement = listRef.current;
    if (!listElement || !isOpen) return;

    const handleScroll = () => {
      const { scrollTop, scrollHeight, clientHeight } = listElement;
      // Load more when scrolled to 80% of the list
      if (scrollTop + clientHeight >= scrollHeight * 0.8 && hasMore && !loading) {
        onLoadMore?.();
      }
    };

    listElement.addEventListener("scroll", handleScroll);
    return () => listElement.removeEventListener("scroll", handleScroll);
  }, [isOpen, hasMore, loading, onLoadMore]);

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
        setSearchTerm("");
      }
    };

    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isOpen]);

  const selectedOption = options.find((opt) => opt.name === value || (value === "" && (opt.id === "" || opt.name.startsWith("All "))));

  const handleSelect = (option) => {
    // If "All" option is selected, set value to empty string
    const valueToSet = (option.id === "" || option.name.startsWith("All ")) ? "" : option.name;
    onChange({
      target: {
        name,
        value: valueToSet,
      },
    });
    setIsOpen(false);
    setSearchTerm("");
  };

  return (
    <div ref={dropdownRef} className={`relative ${className}`}>
      {/* Selected Value Display */}
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className={`w-full bg-white/10 border border-white/20 rounded-md px-4 py-3 text-white text-sm focus:outline-none focus:border-white/40 focus:bg-white/15 transition-all min-w-[200px] text-left flex items-center justify-between hover:bg-white/15 ${
          isOpen ? "bg-white/15 border-white/30" : ""
        }`}
      >
        <span className={selectedOption ? "truncate" : "text-white/50 truncate"}>
          {selectedOption ? selectedOption.name : placeholder}
        </span>
        <svg
          className={`w-4 h-4 flex-shrink-0 ml-2 transition-transform duration-200 ${
            isOpen ? "rotate-180" : ""
          }`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </button>

      {/* Dropdown */}
      {isOpen && (
        <div className="absolute z-50 w-full mt-1 bg-black/98 backdrop-blur-md border border-white/20 rounded-lg shadow-2xl max-h-72 overflow-hidden animate-fade-in">
          {/* Search Input */}
          <div className="p-3 border-b border-white/10 bg-white/5">
            <div className="relative">
              <svg
                className="absolute left-2 top-1/2 transform -translate-y-1/2 w-4 h-4 text-white/50"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search..."
                className="w-full bg-white/10 border border-white/20 rounded-md pl-8 pr-3 py-2 text-white text-sm placeholder-white/50 focus:outline-none focus:border-white/40 focus:bg-white/15 transition-all"
                autoFocus
              />
            </div>
          </div>

          {/* Options List */}
          <div
            ref={listRef}
            className="overflow-y-auto max-h-56 custom-scrollbar"
          >
            {/* Show "All" option at the top if it exists */}
            {allOption && (
              <button
                key={allOption.id || "all"}
                type="button"
                onClick={() => handleSelect(allOption)}
                className={`w-full px-4 py-2.5 text-left text-sm transition-all border-b border-white/5 ${
                  value === allOption.name || value === ""
                    ? "bg-white/15 text-white font-medium"
                    : "text-white/90 hover:bg-white/10 hover:text-white"
                }`}
              >
                <span className="flex items-center gap-2">
                  {value === allOption.name || value === "" ? (
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fillRule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                  ) : (
                    <span className="w-4 h-4" />
                  )}
                  {allOption.name}
                </span>
              </button>
            )}

            {filteredOptions.length === 0 && !loading && searchTerm && (
              <div className="px-4 py-8 text-white/40 text-sm text-center">
                <svg
                  className="w-8 h-8 mx-auto mb-2 opacity-50"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={1.5}
                    d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                No options found
              </div>
            )}

            {filteredOptions.map((option, index) => (
              <button
                key={option.id}
                type="button"
                onClick={() => handleSelect(option)}
                className={`w-full px-4 py-2.5 text-left text-sm transition-all ${
                  value === option.name
                    ? "bg-white/15 text-white font-medium"
                    : "text-white/90 hover:bg-white/10 hover:text-white"
                } ${index === 0 && !allOption ? "border-t border-white/5" : ""}`}
              >
                <span className="flex items-center gap-2">
                  {value === option.name ? (
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                      <path
                        fillRule="evenodd"
                        d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                  ) : (
                    <span className="w-4 h-4" />
                  )}
                  {option.name}
                </span>
              </button>
            ))}

            {/* Loading indicator */}
            {loading && (
              <div className="px-4 py-4 text-center border-t border-white/10">
                <div className="flex items-center justify-center gap-2 text-white/60 text-sm">
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                  <span>Loading more...</span>
                </div>
              </div>
            )}

            {/* End of list indicator */}
            {!hasMore && filteredOptions.length > 0 && (
              <div className="px-4 py-3 text-white/30 text-xs text-center border-t border-white/10 bg-white/5">
                <span className="flex items-center justify-center gap-1">
                  <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                    <path
                      fillRule="evenodd"
                      d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z"
                      clipRule="evenodd"
                    />
                  </svg>
                  End of list
                </span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default InfiniteScrollSelect;

