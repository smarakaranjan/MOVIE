// import { useEffect, useState } from "react";
// import { useAppDispatch, useAppSelector } from "../../app/hooks";
// import { fetchMovies, setFilters } from "./moviesSlice";
// import { fetchGenres } from "../genres/genresSlice";
// import { fetchActors } from "../actors/actorsSlice";
// import { fetchDirectors } from "../directors/directorsSlice";

// const MovieList = () => {
//   const dispatch = useAppDispatch();

//   const { items: movies, status, error } = useAppSelector(
//     (state) => state.movies
//   );
//   const { items: genres } = useAppSelector((state) => state.genres);
//   const { items: actors } = useAppSelector((state) => state.actors);
//   const { items: directors } = useAppSelector((state) => state.directors);

//   // Local filter state
//   const [localFilters, setLocalFilters] = useState({
//     genre: "",
//     actor: "",
//     director: "",
//     release_year: "",
//     title: "",
//     page: 1,
//   });

//   // ---------------- Handlers ----------------
//   const handleFilterChange = (e) => {
//     const { name, value } = e.target;
//     setLocalFilters((prev) => ({ ...prev, [name]: value, page: 1 }));
//   };

//   const handleApplyFilters = () => {
//     dispatch(setFilters(localFilters));
//     dispatch(fetchMovies(localFilters));
//   };

//   const handlePageChange = (newPage) => {
//     const updatedFilters = { ...localFilters, page: newPage };
//     setLocalFilters(updatedFilters);
//     dispatch(setFilters(updatedFilters));
//     dispatch(fetchMovies(updatedFilters));
//   };

//   // ---------------- Fetch initial data ----------------
//   useEffect(() => {
//     dispatch(fetchGenres());
//     dispatch(fetchActors());
//     dispatch(fetchDirectors());
//     dispatch(fetchMovies(localFilters));
//   }, [dispatch]);

//   return (
//     <div className="p-6">
//       <h1 className="text-3xl font-bold mb-6">Movie Explorer</h1>

//       {/* Filters */}
//       <div className="flex flex-wrap gap-4 mb-6 items-end">
//         {/* Movie Title Search */}
//         <input
//           type="text"
//           name="title"
//           placeholder="Search by movie title..."
//           value={localFilters.title}
//           onChange={handleFilterChange}
//           className="border rounded p-2 flex-1 min-w-[200px]"
//         />

//         {/* Genre Dropdown */}
//         <select
//           name="genre"
//           value={localFilters.genre}
//           onChange={handleFilterChange}
//           className="border rounded p-2"
//         >
//           <option value="">All Genres</option>
//           {genres.map((g) => (
//             <option key={g.id} value={g.name}>
//               {g.name}
//             </option>
//           ))}
//         </select>

//         {/* Actor Dropdown */}
//         <select
//           name="actor"
//           value={localFilters.actor}
//           onChange={handleFilterChange}
//           className="border rounded p-2"
//         >
//           <option value="">All Actors</option>
//           {actors.map((a) => (
//             <option key={a.id} value={a.name}>
//               {a.name}
//             </option>
//           ))}
//         </select>

//         {/* Director Dropdown */}
//         <select
//           name="director"
//           value={localFilters.director}
//           onChange={handleFilterChange}
//           className="border rounded p-2"
//         >
//           <option value="">All Directors</option>
//           {directors.map((d) => (
//             <option key={d.id} value={d.name}>
//               {d.name}
//             </option>
//           ))}
//         </select>

//         {/* Release Year */}
//         <input
//           type="number"
//           name="release_year"
//           placeholder="Release Year"
//           value={localFilters.release_year}
//           onChange={handleFilterChange}
//           className="border rounded p-2 w-[120px]"
//         />

//         <button
//           onClick={handleApplyFilters}
//           className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
//         >
//           Apply
//         </button>
//       </div>

//       {/* Movie List */}
//       {status === "loading" && <p>Loading movies...</p>}
//       {status === "failed" && <p className="text-red-600">{error}</p>}
//       {status === "succeeded" && movies.length === 0 && (
//         <p>No movies found.</p>
//       )}
//       {status === "succeeded" && movies.length > 0 && (
//         <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
//           {movies.map((movie) => (
//             <div
//               key={movie.id}
//               className="border rounded p-4 shadow hover:shadow-lg transition"
//             >
//               <h2 className="text-xl font-semibold">{movie.title}</h2>
//               <p className="text-gray-600">{movie.release_year}</p>
//               <p>
//                 <span className="font-semibold">Director:</span>{" "}
//                 {movie.director_info?.name || "N/A"}
//               </p>
//               <p>
//                 <span className="font-semibold">Genres:</span>{" "}
//                 {movie.genres_info?.map((g) => g.name).join(", ") || "N/A"}
//               </p>
//               <p>
//                 <span className="font-semibold">Actors:</span>{" "}
//                 {movie.actors?.map((a) => a.name).join(", ") || "N/A"}
//               </p>
//             </div>
//           ))}
//         </div>
//       )}

//       {/* Pagination */}
//       {status === "succeeded" && movies.length > 0 && (
//         <div className="flex justify-center mt-6 gap-2">
//           <button
//             onClick={() => handlePageChange(Math.max(localFilters.page - 1, 1))}
//             className="px-3 py-1 border rounded hover:bg-gray-100"
//             disabled={localFilters.page === 1}
//           >
//             Prev
//           </button>
//           <span className="px-3 py-1 border rounded">{localFilters.page}</span>
//           <button
//             onClick={() => handlePageChange(localFilters.page + 1)}
//             className="px-3 py-1 border rounded hover:bg-gray-100"
//           >
//             Next
//           </button>
//         </div>
//       )}
//     </div>
//   );
// };

// export default MovieList;


import { useEffect, useState } from "react";
import { useAppDispatch, useAppSelector } from "../../app/hooks";
import { fetchMovies, setFilters } from "./moviesSlice";
import { fetchGenres } from "../genres/genresSlice";
import { fetchActors } from "../actors/actorsSlice";
import { fetchDirectors } from "../directors/directorsSlice";
import { Link } from "react-router-dom";
import { useToast } from "../../hooks/useToast.jsx";
import InfiniteScrollSelect from "../../components/InfiniteScrollSelect";
import Pagination from "../../components/Pagination";

const MoviesList = () => {
  const dispatch = useAppDispatch();
  const { showToast, ToastContainer } = useToast();

  const { items: movies, status, error, pagination } = useAppSelector(
    (state) => state.movies
  );
  const { items: genres, pagination: genresPagination, status: genresStatus } = useAppSelector((state) => state.genres);
  const { items: actors, pagination: actorsPagination, status: actorsStatus } = useAppSelector((state) => state.actors);
  const { items: directors, pagination: directorsPagination, status: directorsStatus } = useAppSelector((state) => state.directors);

  const [localFilters, setLocalFilters] = useState({
    genre: "",
    actor: "",
    director: "",
    release_year: "",
    title: "",
    page: 1,
  });

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    const updatedFilters = { ...localFilters, [name]: value, page: 1 };
    setLocalFilters(updatedFilters);
    dispatch(setFilters(updatedFilters));
    dispatch(fetchMovies(updatedFilters));
  };

  const handlePageChange = (newPage) => {
    const updatedFilters = { ...localFilters, page: newPage };
    setLocalFilters(updatedFilters);
    dispatch(setFilters(updatedFilters));
    dispatch(fetchMovies(updatedFilters));
  };

  useEffect(() => {
    // Load first page of each filter
    dispatch(fetchGenres({ page: 1, page_size: 20 }));
    dispatch(fetchActors({ page: 1, page_size: 20 }));
    dispatch(fetchDirectors({ page: 1, page_size: 20 }));
    dispatch(fetchMovies(localFilters));
  }, [dispatch]);

  // Load more handlers for infinite scroll
  const handleLoadMoreGenres = () => {
    if (genresPagination && genresPagination.current_page < genresPagination.total_pages) {
      dispatch(fetchGenres({ page: genresPagination.current_page + 1, page_size: 20 }));
    }
  };

  const handleLoadMoreActors = () => {
    if (actorsPagination && actorsPagination.current_page < actorsPagination.total_pages) {
      dispatch(fetchActors({ page: actorsPagination.current_page + 1, page_size: 20 }));
    }
  };

  const handleLoadMoreDirectors = () => {
    if (directorsPagination && directorsPagination.current_page < directorsPagination.total_pages) {
      dispatch(fetchDirectors({ page: directorsPagination.current_page + 1, page_size: 20 }));
    }
  };

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
          <h1 className="text-3xl font-bold mb-6 tracking-tight">Movies</h1>
          
          {/* Search and Filters - Same Level */}
          <div className="flex flex-wrap items-center gap-3">
            {/* Search Bar */}
            <div className="relative flex-1 min-w-[250px]">
              <input
                type="text"
                name="title"
                placeholder="Search for movies..."
                value={localFilters.title}
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
            <InfiniteScrollSelect
              name="genre"
              value={localFilters.genre}
              onChange={handleFilterChange}
              options={[{ id: "", name: "All Genres" }, ...genres]}
              placeholder="All Genres"
              onLoadMore={handleLoadMoreGenres}
              hasMore={genresPagination ? genresPagination.current_page < genresPagination.total_pages : false}
              loading={genresStatus === "loading"}
              className="min-w-[200px]"
            />
            <InfiniteScrollSelect
              name="actor"
              value={localFilters.actor}
              onChange={handleFilterChange}
              options={[{ id: "", name: "All Actors" }, ...actors]}
              placeholder="All Actors"
              onLoadMore={handleLoadMoreActors}
              hasMore={actorsPagination ? actorsPagination.current_page < actorsPagination.total_pages : false}
              loading={actorsStatus === "loading"}
              className="min-w-[200px]"
            />
            <InfiniteScrollSelect
              name="director"
              value={localFilters.director}
              onChange={handleFilterChange}
              options={[{ id: "", name: "All Directors" }, ...directors]}
              placeholder="All Directors"
              onLoadMore={handleLoadMoreDirectors}
              hasMore={directorsPagination ? directorsPagination.current_page < directorsPagination.total_pages : false}
              loading={directorsStatus === "loading"}
              className="min-w-[200px]"
            />
            <input
              type="text"
              name="release_year"
              placeholder="Year"
              value={localFilters.release_year}
              onChange={handleFilterChange}
              className="bg-white/10 border border-white/20 rounded-md px-4 py-3 text-white text-sm placeholder-white/50 focus:outline-none focus:border-white/40 focus:bg-white/15 transition-all w-24"
            />
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
                <p className="text-white/50">Loading movies...</p>
              </div>
            </div>
          )}

          {/* Error State - Show grid placeholder */}
          {status === "failed" && (
            <div className="flex items-center justify-center py-20">
              <div className="text-center">
                <p className="text-white/50 mb-4">Unable to load movies</p>
                <button
                  onClick={() => {
                    dispatch(fetchMovies(localFilters));
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

          {/* Empty State - Show grid placeholder */}
          {status === "succeeded" && movies.length === 0 && (
            <div className="flex items-center justify-center py-20">
              <div className="text-center">
                <p className="text-white/50">No movies found</p>
              </div>
            </div>
          )}

          {/* Movies Grid */}
          {status === "succeeded" && movies.length > 0 && (
            <>
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
                      {movie.genres_info && movie.genres_info.length > 0 && (
                        <div className="flex flex-wrap gap-1 mb-2">
                          {movie.genres_info.slice(0, 2).map((g) => (
                            <span
                              key={g.genre?.id || g.id}
                              className="text-xs bg-white/20 backdrop-blur-sm px-2 py-0.5 rounded text-white/90"
                            >
                              {g.genre?.name || g.name}
                            </span>
                          ))}
                        </div>
                      )}
                      {movie.director_info && (
                        <p className="text-white/60 text-xs truncate">
                          {movie.director_info.name}
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

export default MoviesList;
