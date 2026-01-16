import { Link } from "react-router-dom";

const NotFound = () => {
  return (
    <div className="bg-black min-h-screen text-white flex items-center justify-center relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-red-600/10 rounded-full blur-3xl"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-600/10 rounded-full blur-3xl"></div>
      </div>

      <div className="text-center px-8 relative z-10">
        {/* 404 Number with Gradient */}
        <div className="mb-6">
          <h1 className="text-9xl font-black bg-gradient-to-r from-red-600 via-purple-600 to-red-600 bg-clip-text text-transparent">
            404
          </h1>
        </div>
        
        <h2 className="text-3xl font-bold mb-4 text-white/90">Page Not Found</h2>
        <p className="text-white/60 mb-10 max-w-md mx-auto text-lg">
          The page you're looking for doesn't exist or has been moved.
        </p>
        
        {/* Navigation Cards */}
        <div className="flex flex-wrap gap-4 justify-center">
          <Link
            to="/"
            className="group relative px-8 py-4 bg-white/5 hover:bg-white/10 border border-white/10 hover:border-white/20 rounded-xl text-white transition-all duration-300 hover:scale-105 backdrop-blur-sm"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-red-600/0 to-purple-600/0 group-hover:from-red-600/10 group-hover:to-purple-600/10 rounded-xl transition-all duration-300"></div>
            <div className="relative flex items-center gap-3">
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
                  d="M7 4v16M17 4v16M3 8h4m10 0h4M3 12h18M3 16h4m10 0h4M4 20h16a1 1 0 001-1V5a1 1 0 00-1-1H4a1 1 0 00-1 1v14a1 1 0 001 1z"
                />
              </svg>
              <span className="font-semibold">Go to Movies</span>
            </div>
          </Link>
          
          <Link
            to="/actors"
            className="group relative px-8 py-4 bg-white/5 hover:bg-white/10 border border-white/10 hover:border-white/20 rounded-xl text-white transition-all duration-300 hover:scale-105 backdrop-blur-sm"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-red-600/0 to-purple-600/0 group-hover:from-red-600/10 group-hover:to-purple-600/10 rounded-xl transition-all duration-300"></div>
            <div className="relative flex items-center gap-3">
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
                  d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                />
              </svg>
              <span className="font-semibold">Go to Actors</span>
            </div>
          </Link>
          
          <Link
            to="/directors"
            className="group relative px-8 py-4 bg-white/5 hover:bg-white/10 border border-white/10 hover:border-white/20 rounded-xl text-white transition-all duration-300 hover:scale-105 backdrop-blur-sm"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-red-600/0 to-purple-600/0 group-hover:from-red-600/10 group-hover:to-purple-600/10 rounded-xl transition-all duration-300"></div>
            <div className="relative flex items-center gap-3">
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
                  d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                />
              </svg>
              <span className="font-semibold">Go to Directors</span>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default NotFound;

