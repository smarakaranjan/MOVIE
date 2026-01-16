import React, { useEffect, useState, useRef, useCallback } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { getDirector } from "../../api/directorsApi";
import { getMovies } from "../../api/moviesApi";
import { getErrorMessage, getErrorCode } from "../../utils/errorHandler";
import { useToast } from "../../hooks/useToast.jsx";

const DirectorDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { showToast, ToastContainer } = useToast();
  const [director, setDirector] = useState(null);
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState(null);
  const [errorCode, setErrorCode] = useState(null);
  const [moviesPage, setMoviesPage] = useState(1);
  const [hasMoreMovies, setHasMoreMovies] = useState(false);
  const observerTarget = useRef(null);

  useEffect(() => {
    const fetchDirector = async () => {
      try {
        setLoading(true);
        setError(null);
        setErrorCode(null);
        const data = await getDirector(id);
        setDirector(data);
        // Set initial movies from detail response
        if (data.movies) {
          setMovies(data.movies);
          // Check if there are more movies to load
          setHasMoreMovies(data.movies_count > data.movies.length);
        }
      } catch (err) {
        const errorMessage = getErrorMessage(err);
        const code = getErrorCode(err);
        setError(errorMessage);
        setErrorCode(code);
        
        showToast(errorMessage, "error");
        
        if (code === "NOT_FOUND") {
          setTimeout(() => {
            navigate("/directors");
          }, 3000);
        }
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchDirector();
      setMoviesPage(1);
      setMovies([]);
    }
  }, [id, showToast, navigate]);

  // Load more movies
  const loadMoreMovies = useCallback(async () => {
    if (loadingMore || !hasMoreMovies || !director) return;

    try {
      setLoadingMore(true);
      const response = await getMovies({
        director: director.name,
        page: moviesPage + 1,
        page_size: 12,
        ordering: '-release_year'
      });
      
      if (response.results && response.results.length > 0) {
        setMovies(prev => [...prev, ...response.results]);
        setMoviesPage(prev => prev + 1);
        setHasMoreMovies(response.pagination?.current_page < response.pagination?.total_pages);
      } else {
        setHasMoreMovies(false);
      }
    } catch (err) {
      showToast(getErrorMessage(err), "error");
      setHasMoreMovies(false);
    } finally {
      setLoadingMore(false);
    }
  }, [director, moviesPage, loadingMore, hasMoreMovies, showToast]);

  // Intersection Observer for infinite scroll
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && hasMoreMovies && !loadingMore) {
          loadMoreMovies();
        }
      },
      { threshold: 0.1 }
    );

    const currentTarget = observerTarget.current;
    if (currentTarget) {
      observer.observe(currentTarget);
    }

    return () => {
      if (currentTarget) {
        observer.unobserve(currentTarget);
      }
    };
  }, [loadMoreMovies, hasMoreMovies, loadingMore]);

  if (loading) {
    return (
      <div className="bg-black min-h-screen text-white flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-white/20 border-t-white rounded-full animate-spin"></div>
          <p className="text-white/50">Loading director...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-black min-h-screen text-white">
        <ToastContainer />
        <div className="px-8 pt-6">
          <div className="max-w-7xl mx-auto">
            <Link
              to="/directors"
              className="inline-flex items-center gap-2 text-white/70 hover:text-white transition-colors mb-6"
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
                  d="M15 19l-7-7 7-7"
                />
              </svg>
              Back to Directors
            </Link>
          </div>
        </div>
        <div className="flex items-center justify-center min-h-[60vh] px-8">
          <div className="text-center">
            {errorCode === "NOT_FOUND" ? (
              <>
                <h2 className="text-2xl font-bold text-white mb-2">Director Not Found</h2>
                <p className="text-white/50 mb-4">Redirecting to directors...</p>
              </>
            ) : (
              <>
                <h2 className="text-2xl font-bold text-white mb-2">Something Went Wrong</h2>
                <p className="text-white/50 mb-4">Please try again later</p>
                <button
                  onClick={() => navigate("/directors")}
                  className="inline-flex items-center gap-2 px-6 py-3 bg-white/10 hover:bg-white/20 border border-white/20 rounded-md text-white transition-colors"
                >
                  Go Back
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    );
  }

  if (!director) {
    return (
      <div className="bg-black min-h-screen text-white flex items-center justify-center">
        <div className="text-white/50">Director not found</div>
      </div>
    );
  }

  return (
    <div className="bg-black min-h-screen text-white">
      <ToastContainer />
      {/* Back Button */}
      <div className="px-8 pt-6">
        <div className="max-w-7xl mx-auto">
          <Link
            to="/directors"
            className="inline-flex items-center gap-2 text-white/70 hover:text-white transition-colors mb-6"
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
                d="M15 19l-7-7 7-7"
              />
            </svg>
            Back to Directors
          </Link>
        </div>
      </div>

      {/* Director Header */}
      <div className="px-8 pb-12">
        <div className="max-w-7xl mx-auto">
          <div className="mb-8">
            <div className="flex items-start gap-6 mb-6">
              {/* Director Image */}
              <div className="flex-shrink-0">
                {director.image_url ? (
                  <img
                    src={director.image_url}
                    alt={director.name}
                    className="w-48 h-48 rounded-full object-cover border-4 border-white/20"
                    onError={(e) => {
                      e.target.style.display = 'none';
                      e.target.nextSibling.style.display = 'flex';
                    }}
                  />
                ) : null}
                <div className={`w-48 h-48 rounded-full bg-gradient-to-br from-gray-700 to-gray-900 flex items-center justify-center text-white/50 font-bold text-6xl border-4 border-white/20 ${director.image_url ? 'hidden' : ''}`}>
                  {director.name.charAt(0).toUpperCase()}
                </div>
              </div>
              
              <div className="flex-1">
                <h1 className="text-5xl font-bold mb-4 tracking-tight">
                  {director.name}
                </h1>
                {director.date_of_birth && (
                  <div className="text-white/70 mb-4">
                    <span>Born: {new Date(director.date_of_birth).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}</span>
                  </div>
                )}
                {director.bio && (
                  <p className="text-white/80 text-lg leading-relaxed max-w-3xl">
                    {director.bio}
                  </p>
                )}
              </div>
            </div>
          </div>

          {/* Movies */}
          {movies && movies.length > 0 && (
            <div className="mb-8">
              <h2 className="text-2xl font-semibold mb-4 text-white/90">Directed Movies</h2>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
                {movies.map((movie) => (
                  <Link
                    key={movie.id}
                    to={`/movies/${movie.id}`}
                    className="group relative aspect-[2/3] rounded overflow-hidden transition-transform duration-300 hover:scale-110 hover:z-10"
                  >
                    {/* Movie Poster */}
                    {movie.image_url ? (
                      <img
                        src={movie.image_url}
                        alt={movie.title}
                        className="absolute inset-0 w-full h-full object-cover"
                        onError={(e) => {
                          e.target.style.display = 'none';
                          e.target.nextSibling.style.display = 'flex';
                        }}
                      />
                    ) : null}
                    {/* Poster Placeholder */}
                    <div 
                      className={`absolute inset-0 bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center ${movie.image_url ? 'hidden' : ''}`}
                    >
                      <div className="text-white/20 text-4xl font-bold">
                        {movie.title.slice(0, 2).toUpperCase()}
                      </div>
                    </div>

                    {/* Hover Overlay */}
                    <div className="absolute inset-0 bg-gradient-to-t from-black via-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-end p-3">
                      <h3 className="text-white font-semibold text-sm mb-1 line-clamp-2">
                        {movie.title}
                      </h3>
                      <p className="text-white/70 text-xs mb-2">
                        {movie.release_year}
                      </p>
                      {movie.rating && (
                        <p className="text-white/70 text-xs">
                          ⭐ {movie.rating}
                        </p>
                      )}
                    </div>
                  </Link>
                ))}
              </div>
              
              {/* Infinite Scroll Trigger */}
              {hasMoreMovies && (
                <div ref={observerTarget} className="flex justify-center items-center py-8">
                  {loadingMore && (
                    <div className="flex flex-col items-center gap-2">
                      <div className="w-8 h-8 border-4 border-white/20 border-t-white rounded-full animate-spin"></div>
                      <p className="text-white/50 text-sm">Loading more movies...</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DirectorDetail;

