import { useEffect, useState } from "react";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { fetchDirectors, setFilters } from "./directorsSlice";
import { Link } from "react-router-dom";
import { useToast } from "../../hooks/useToast.jsx";
import Pagination from "../../components/Pagination";

const DirectorsList = () => {
  const dispatch = useAppDispatch();
  const { showToast, ToastContainer } = useToast();

  const { items: directors, status, error, pagination } = useAppSelector(
    (state) => state.directors
  );

  const [localFilters, setLocalFilters] = useState({
    name: "",
    page: 1,
  });

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    const updatedFilters = { ...localFilters, [name]: value, page: 1 };
    setLocalFilters(updatedFilters);
    dispatch(setFilters(updatedFilters));
    dispatch(fetchDirectors(updatedFilters));
  };

  const handlePageChange = (newPage) => {
    const updatedFilters = { ...localFilters, page: newPage };
    setLocalFilters(updatedFilters);
    dispatch(setFilters(updatedFilters));
    dispatch(fetchDirectors(updatedFilters));
  };

  useEffect(() => {
    dispatch(fetchDirectors(localFilters));
  }, [dispatch]);

  // Show toast only for errors
  useEffect(() => {
    if (status === "failed" && error) {
      showToast(error, "error");
    }
  }, [status, error, showToast]);

  return (
    <div className="bg-black min-h-screen text-white">
      <ToastContainer />
      {/* Header */}
      <div className="bg-gradient-to-b from-black via-black/95 to-transparent pb-6 pt-6 px-8">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold mb-6 tracking-tight">Directors</h1>
          
          {/* Search and Filters - Same Level */}
          <div className="flex flex-wrap items-center gap-3">
            {/* Search Bar */}
            <div className="relative flex-1 min-w-[250px]">
              <input
                type="text"
                name="name"
                placeholder="Search for directors..."
                value={localFilters.name}
                onChange={handleFilterChange}
                className="w-full bg-white/10 backdrop-blur-sm border border-white/20 rounded-md px-4 py-3 pl-11 text-white placeholder-white/50 focus:outline-none focus:border-white/40 focus:bg-white/15 transition-all"
              />
              <svg
                className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-white/50"
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
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="px-8 pb-12">
        <div className="max-w-7xl mx-auto">
          {/* Loading State */}
          {status === "loading" && (
            <div className="flex items-center justify-center py-20">
              <div className="flex flex-col items-center gap-4">
                <div className="w-12 h-12 border-4 border-white/20 border-t-white rounded-full animate-spin"></div>
                <p className="text-white/50">Loading directors...</p>
              </div>
            </div>
          )}

          {/* Error State */}
          {status === "failed" && (
            <div className="flex items-center justify-center py-20">
              <div className="text-center">
                <p className="text-white/50 mb-4">Unable to load directors</p>
                <button
                  onClick={() => {
                    dispatch(fetchDirectors(localFilters));
                  }}
                  className="inline-flex items-center gap-2 px-6 py-3 bg-white/10 hover:bg-white/20 border border-white/20 rounded-md text-white transition-colors"
                >
                  <svg
                    className="w-5 h-5"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                    />
                  </svg>
                  Try Again
                </button>
              </div>
            </div>
          )}

          {/* Empty State */}
          {status === "succeeded" && directors.length === 0 && (
            <div className="flex items-center justify-center py-20">
              <div className="text-center">
                <p className="text-white/50">No directors found</p>
              </div>
            </div>
          )}

          {/* Directors Grid */}
          {status === "succeeded" && directors.length > 0 && (
            <>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
                {directors.map((director) => (
                  <Link
                    key={director.id}
                    to={`/directors/${director.id}`}
                    className="group relative aspect-[2/3] rounded overflow-hidden transition-transform duration-300 hover:scale-110 hover:z-10"
                  >
                    {/* Director Image */}
                    {director.image_url ? (
                      <img
                        src={director.image_url}
                        alt={director.name}
                        className="absolute inset-0 w-full h-full object-cover"
                        onError={(e) => {
                          e.target.style.display = 'none';
                          e.target.nextSibling.style.display = 'flex';
                        }}
                      />
                    ) : null}
                    {/* Image Placeholder */}
                    <div 
                      className={`absolute inset-0 bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center ${director.image_url ? 'hidden' : ''}`}
                    >
                      <div className="text-white/20 text-4xl font-bold">
                        {director.name.slice(0, 2).toUpperCase()}
                      </div>
                    </div>

                    {/* Hover Overlay */}
                    <div className="absolute inset-0 bg-gradient-to-t from-black via-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-3">
                      <h3 className="text-white font-semibold text-sm mb-1 line-clamp-2">
                        {director.name}
                      </h3>
                      {director.date_of_birth && (
                        <p className="text-white/70 text-xs mb-2">
                          {new Date(director.date_of_birth).getFullYear()}
                        </p>
                      )}
                    </div>
                  </Link>
                ))}
              </div>

              {/* Pagination */}
              <Pagination
                currentPage={localFilters.page}
                totalPages={pagination?.total_pages || 0}
                onPageChange={handlePageChange}
              />
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default DirectorsList;

