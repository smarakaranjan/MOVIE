# Movie Explorer

A full-stack movie exploration application built with Django REST Framework and React.

> **🚀 Quick Start:** See [NEXT_STEPS.md](./NEXT_STEPS.md) for detailed setup instructions.

## Features

- 🎬 Browse movies with Netflix-style UI
- 🎭 Explore actors and directors
- 🔍 Advanced filtering and search
- 📱 Responsive design with dark theme
- ♾️ Infinite scroll for movies
- 🎨 Beautiful glassmorphism UI
- ✅ Comprehensive test coverage
- ✅ Comprehensive test coverage

## Tech Stack

### Backend
- Django 5.0+
- Django REST Framework
- SQLite (default) / PostgreSQL (production)
- Django Filter
- DRF Spectacular (API Documentation)

### Frontend
- React 19
- Redux Toolkit
- React Router DOM
- Tailwind CSS
- Vite
- Axios

## Prerequisites

### For Local Development
- Python 3.11+
- Node.js 20+
- npm or yarn

### For Docker
- Docker 20.10+
- Docker Compose 2.0+

## Quick Start

### Option 1: Docker (Recommended)

#### Production Build (with Nginx)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd movie-explorer
   ```

2. **Start all services:**
   ```bash
   # Using Makefile
   make rebuild
   
   # Or using Docker Compose
   docker-compose up --build
   ```

3. **Populate the database:**
   ```bash
   # Using Makefile
   make populate
   
   # Or using Docker Compose
   docker-compose exec backend python manage.py movies
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/api/docs/swagger/

#### Development Build (with Vite - Hot Reload)

For development with hot-reload, use `Dockerfile.dev`:

1. **Update docker-compose.yml:**
   ```yaml
   frontend:
     build:
       dockerfile: Dockerfile.dev  # Change this line
     ports:
       - "5173:5173"  # Change port mapping
   ```

2. **Rebuild:**
   ```bash
   docker-compose up --build frontend
   ```

3. **Access:** http://localhost:5173 (with hot-reload)

### Option 2: Local Development

#### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Populate database:**
   ```bash
   python manage.py movies
   ```

6. **Start development server:**
   ```bash
   python manage.py runserver
   ```

   Backend will run on: http://localhost:8000

#### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

4. **Update `.env` file:**
   ```env
   VITE_API_URL=http://localhost:8000/api
   ```

5. **Start development server:**
   ```bash
   npm run dev
   ```

   Frontend will run on: http://localhost:5173

## Environment Variables

### ⚠️ Important: .env Files Are NOT Shipped

**.env files should NEVER be committed to git or shipped with Docker images.**

They are:
- ✅ Used locally for development
- ✅ Excluded from git (via .gitignore)
- ✅ NOT included in Docker images
- ✅ Passed to Docker via docker-compose.yml

### Local Development

#### Backend (Optional)

Create a `.env` file in the `backend/` directory (optional for development):

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (if using PostgreSQL)
# DATABASE_URL=postgresql://user:password@localhost:5432/movie_explorer

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Note:** The backend works without a `.env` file in development mode with default settings.

#### Frontend (Required for Local Dev)

Create a `.env` file in the `frontend/` directory:

```env
# Backend API URL
VITE_API_URL=http://localhost:8000/api
```

**Important:** 
- For local development: `VITE_API_URL=http://localhost:8000/api`
- The frontend code uses `import.meta.env.VITE_API_URL` to get this value
- If not set, it defaults to `http://localhost:8000/api`

### Docker (No .env Files Needed!)

**Environment variables are configured in `docker-compose.yml`:**

#### Frontend (Build-time)
- `VITE_API_URL` is passed as a **build argument** during Docker build
- Set in `docker-compose.yml` under `build.args`
- Built into the image at build time

#### Backend (Runtime)
- Environment variables are set in `docker-compose.yml` under `environment:`
- Can optionally use `env_file:` to load from a `.env` file (but file is NOT in image)
- Variables are passed at runtime, not built into image

**Summary:**
- ✅ **Local Dev:** Create `.env` files (not committed to git)
- ✅ **Docker:** Environment variables in `docker-compose.yml` (no .env files needed)
- ❌ **Never:** Commit .env files to git or include in Docker images

## Project Structure

```
movie-explorer/
├── backend/
│   ├── config/          # Django settings
│   ├── movies/          # Movies app
│   ├── utils/           # Utilities (pagination, exceptions)
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── api/         # API clients
│   │   ├── app/         # Redux store
│   │   ├── components/  # Reusable components
│   │   ├── features/    # Feature modules
│   │   ├── hooks/      # Custom hooks
│   │   └── utils/      # Utilities
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── Makefile
└── README.md
```

## Available Scripts

### Backend (Django)

```bash
# Run development server
python manage.py runserver

# Run migrations
python manage.py migrate

# Create migrations
python manage.py makemigrations

# Populate database
python manage.py movies

# Create superuser
python manage.py createsuperuser

# Run tests
pytest
```

### Frontend (React)

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

## Docker Commands

See [README.Docker.md](./README.Docker.md) for complete Docker documentation.

### Quick Reference

```bash
# Using Makefile
make rebuild      # Build and start
make logs         # View logs
make populate     # Populate database
make down         # Stop services
make clean        # Clean everything

# Using Docker Compose
docker-compose up --build -d
docker-compose logs -f
docker-compose exec backend python manage.py movies
docker-compose down
docker-compose down -v
```

## API Endpoints

- **Movies:** `/api/movies/`
- **Actors:** `/api/actors/`
- **Directors:** `/api/directors/`
- **Genres:** `/api/genres/`
- **API Docs:** `/api/docs/swagger/`

## Development

### Backend Development

1. Backend runs on http://localhost:8000
2. Code changes are auto-reloaded (Django development server)
3. Database is SQLite by default (stored in `backend/db.sqlite3`)

### Frontend Development

1. Frontend runs on http://localhost:5173 (Vite dev server)
2. Hot Module Replacement (HMR) enabled
3. API calls go to backend at http://localhost:8000/api

### Environment Configuration

#### Local Development

**You need a `.env` file in the frontend directory** to configure the API URL:

1. Create `frontend/.env`:
   ```env
   VITE_API_URL=http://localhost:8000/api
   ```

2. The frontend code reads this via `import.meta.env.VITE_API_URL`

3. If not set, it defaults to `http://localhost:8000/api`

#### Docker

**No .env files needed!** Environment variables are configured in `docker-compose.yml`:

- **Frontend:** `VITE_API_URL` is passed as build arg (see `docker-compose.yml` line 30)
- **Backend:** Environment variables are set in `docker-compose.yml` (lines 15-18)

The `.env` files are:
- ✅ Used for local development
- ❌ NOT committed to git (in .gitignore)
- ❌ NOT included in Docker images
- ✅ Configured in docker-compose.yml instead

## Troubleshooting

### Frontend can't connect to backend

1. **Check backend is running:**
   ```bash
   curl http://localhost:8000/api/movies/
   ```

2. **Check `.env` file exists in frontend:**
   ```bash
   cat frontend/.env
   ```

3. **Verify API URL in code:**
   - Check `frontend/src/api/client.js`
   - Should use `import.meta.env.VITE_API_URL`

### Port conflicts

If ports 3000, 5173, or 8000 are in use:

**Docker:** Edit `docker-compose.yml` port mappings

**Local:** 
- Backend: Edit `manage.py runserver 0.0.0.0:8001`
- Frontend: Vite will suggest alternative port

### Database issues

**Reset database:**
```bash
# Local
rm backend/db.sqlite3
python manage.py migrate
python manage.py movies

# Docker
docker-compose exec backend python manage.py flush
docker-compose exec backend python manage.py movies
```

## Production Deployment

1. Set `DEBUG=False` in backend settings
2. Use PostgreSQL instead of SQLite
3. Configure proper CORS settings
4. Set up SSL/TLS certificates
5. Use environment variables for secrets
6. Configure static file serving

## License

MIT

