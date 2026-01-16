import React, { useEffect, useState } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import { getMovie } from "../../api/moviesApi";
import { getErrorMessage, getErrorCode } from "../../utils/errorHandler";
import { useToast } from "../../hooks/useToast.jsx";

const MovieDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { showToast, ToastContainer } = useToast();
  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [errorCode, setErrorCode] = useState(null);

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        setLoading(true);
        setError(null);
        setErrorCode(null);
        const data = await getMovie(id);
        setMovie(data);
      } catch (err) {
        const errorMessage = getErrorMessage(err);
        const code = getErrorCode(err);
        setError(errorMessage);
        setErrorCode(code);
        
        // Show toast for errors
        showToast(errorMessage, "error");
        
        // Navigate back if not found
        if (code === "NOT_FOUND") {
          setTimeout(() => {
            navigate("/");
          }, 3000);
        }
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchMovie();
    }
  }, [id, showToast, navigate]);

  if (loading) {
    return (
      <div className="bg-black min-h-screen text-white flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-white/20 border-t-white rounded-full animate-spin"></div>
          <p className="text-white/50">Loading movie...</p>
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
              to="/"
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
              Back to Movies
            </Link>
          </div>
        </div>
        <div className="flex items-center justify-center min-h-[60vh] px-8">
          <div className="text-center">
            {errorCode === "NOT_FOUND" ? (
              <>
                <h2 className="text-2xl font-bold text-white mb-2">Movie Not Found</h2>
                <p className="text-white/50 mb-4">Redirecting to movies...</p>
              </>
            ) : (
              <>
                <h2 className="text-2xl font-bold text-white mb-2">Something Went Wrong</h2>
                <p className="text-white/50 mb-4">Please try again later</p>
                <button
                  onClick={() => navigate("/")}
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

  if (!movie) {
    return (
      <div className="bg-black min-h-screen text-white flex items-center justify-center">
        <div className="text-white/50">Movie not found</div>
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
            to="/"
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
            Back to Movies
          </Link>
        </div>
      </div>

      {/* Movie Header */}
      <div className="px-8 pb-12">
        <div className="max-w-7xl mx-auto">
          <div className="mb-8">
            <h1 className="text-5xl font-bold mb-4 tracking-tight">
              {movie.title}
            </h1>
            <div className="flex items-center gap-4 text-white/70 mb-6">
              <span>{movie.release_year}</span>
              {movie.rating && (
                <>
                  <span>•</span>
                  <span>⭐ {movie.rating}</span>
                </>
              )}
            </div>
          </div>

          {/* Genres */}
          {movie.genres_info && movie.genres_info.length > 0 && (
            <div className="mb-8">
              <h2 className="text-lg font-semibold mb-3 text-white/90">Genres</h2>
              <div className="flex flex-wrap gap-2">
                {movie.genres_info.map((genre) => (
                  <span
                    key={genre.genre.id}
                    className="px-4 py-2 bg-white/10 border border-white/20 rounded-md text-sm hover:bg-white/20 transition-colors"
                  >
                    {genre.genre.name}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Movie Poster */}
          {movie.image_url && (
            <div className="mb-8">
              <img
                src={movie.image_url}
                alt={movie.title}
                className="w-full max-w-md rounded-lg shadow-2xl"
                onError={(e) => {
                  e.target.style.display = 'none';
                }}
              />
            </div>
          )}

          {/* Director */}
          {movie.director_info && (
            <div className="mb-8">
              <h2 className="text-lg font-semibold mb-3 text-white/90">Director</h2>
              <Link
                to={`/directors/${movie.director_info.id}`}
                className="flex items-center gap-4 hover:opacity-80 transition-opacity"
              >
                {movie.director_info.image_url ? (
                  <img
                    src={movie.director_info.image_url}
                    alt={movie.director_info.name}
                    className="w-16 h-16 rounded-full object-cover border-2 border-white/20"
                    onError={(e) => {
                      e.target.style.display = 'none';
                      e.target.nextSibling.style.display = 'flex';
                    }}
                  />
                ) : null}
                <div className={`w-16 h-16 rounded-full bg-gradient-to-br from-gray-700 to-gray-900 flex items-center justify-center text-white/50 font-bold text-xl ${movie.director_info.image_url ? 'hidden' : ''}`}>
                  {movie.director_info.name.charAt(0).toUpperCase()}
                </div>
                <div>
                  <p className="text-white font-medium">{movie.director_info.name}</p>
                  {movie.director_info.bio && (
                    <p className="text-white/60 text-sm mt-1">{movie.director_info.bio}</p>
                  )}
                  {movie.director_info.date_of_birth && (
                    <p className="text-white/50 text-xs mt-1">
                      Born: {new Date(movie.director_info.date_of_birth).getFullYear()}
                    </p>
                  )}
                </div>
              </Link>
            </div>
          )}

          {/* Cast (Actors) */}
          {movie.actors_info && movie.actors_info.length > 0 && (
            <div className="mb-8">
              <h2 className="text-lg font-semibold mb-4 text-white/90">Cast</h2>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
                {movie.actors_info.map((actorInfo) => (
                  <Link
                    key={actorInfo.person.id}
                    to={`/actors/${actorInfo.person.id}`}
                    className="group cursor-pointer"
                  >
                    <div className="w-full aspect-[2/3] rounded-lg bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center mb-3 overflow-hidden relative">
                      {actorInfo.person.image_url ? (
                        <img
                          src={actorInfo.person.image_url}
                          alt={actorInfo.person.name}
                          className="absolute inset-0 w-full h-full object-cover"
                          onError={(e) => {
                            e.target.style.display = 'none';
                            e.target.nextSibling.style.display = 'flex';
                          }}
                        />
                      ) : null}
                      <div className={`text-white/20 text-3xl font-bold ${actorInfo.person.image_url ? 'hidden' : 'flex'}`}>
                        {actorInfo.person.name.charAt(0).toUpperCase()}
                      </div>
                    </div>
                    <div>
                      <p className="text-white font-medium text-sm mb-1">
                        {actorInfo.person.name}
                      </p>
                      {actorInfo.character_name && (
                        <p className="text-white/60 text-xs">
                          as {actorInfo.character_name}
                        </p>
                      )}
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MovieDetail;
