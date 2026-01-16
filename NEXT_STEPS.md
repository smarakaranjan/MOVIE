# Next Steps - Getting Started

Follow these steps to get your Movie Explorer application running.

## Step 1: Choose Your Setup Method

### Option A: Docker (Easiest - Recommended)
### Option B: Local Development

---

## Option A: Docker Setup

### 1. Ensure Docker is Running
```bash
docker --version
docker-compose --version
```

### 2. Build and Start Services
```bash
# Using Makefile (easier)
make rebuild

# Or using Docker Compose directly
docker-compose up --build
```

### 3. Populate the Database
```bash
# Using Makefile
make populate

# Or using Docker Compose
docker-compose exec backend python manage.py movies
```

### 4. Access the Application
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/api/docs/swagger/

### 5. Verify Everything Works
- Open http://localhost:3000 in your browser
- You should see the movies list
- Try navigating to Actors and Directors pages

---

## Option B: Local Development Setup

### Backend Setup

1. **Navigate to backend:**
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

6. **Start server:**
   ```bash
   python manage.py runserver
   ```
   Backend runs on: http://localhost:8000

### Frontend Setup

1. **Navigate to frontend:**
   ```bash
   cd frontend
   ```

2. **Create .env file:**
   ```bash
   echo "VITE_API_URL=http://localhost:8000/api" > .env
   ```

3. **Install dependencies:**
   ```bash
   npm install
   ```

4. **Start dev server:**
   ```bash
   npm run dev
   ```
   Frontend runs on: http://localhost:5173

---

## Step 2: Test the Application

### Test Frontend Pages
- ✅ Movies list: http://localhost:3000 (or 5173 for local)
- ✅ Actors list: http://localhost:3000/actors
- ✅ Directors list: http://localhost:3000/directors
- ✅ Movie detail: Click any movie
- ✅ Actor detail: Click any actor
- ✅ Director detail: Click any director

### Test Features
- ✅ Search functionality
- ✅ Filter by genre, actor, director, year
- ✅ Pagination
- ✅ Infinite scroll on detail pages
- ✅ Navigation between pages

---

## Step 3: Common Tasks

### View Logs
```bash
# Docker
make logs
# or
docker-compose logs -f

# Backend only
make logs-backend

# Frontend only
make logs-frontend
```

### Stop Services
```bash
# Docker
make down
# or
docker-compose down

# Local
# Press Ctrl+C in terminal
```

### Restart Services
```bash
# Docker
make restart
# or
docker-compose restart
```

### Access Backend Shell
```bash
# Docker
make shell-backend
# or
docker-compose exec backend bash

# Then run Django commands:
python manage.py migrate
python manage.py createsuperuser
python manage.py movies
```

### Rebuild After Code Changes
```bash
# Docker - Full rebuild
make rebuild

# Docker - Frontend only
docker-compose up --build frontend

# Local - Just restart the dev server (Ctrl+C then npm run dev)
```

---

## Step 4: Troubleshooting

### Port Already in Use
If ports 3000, 5173, or 8000 are busy:

**Docker:** Edit `docker-compose.yml`:
```yaml
ports:
  - "3001:80"   # Change frontend port
  - "8001:8000" # Change backend port
```

**Local:** 
- Backend: `python manage.py runserver 8001`
- Frontend: Vite will suggest alternative port

### Frontend Can't Connect to Backend

1. **Check backend is running:**
   ```bash
   curl http://localhost:8000/api/movies/
   ```

2. **Check .env file exists (local dev only):**
   ```bash
   cat frontend/.env
   # Should contain: VITE_API_URL=http://localhost:8000/api
   ```

3. **For Docker:** API URL is set in `docker-compose.yml` (line 31)

### Database Issues

**Reset database:**
```bash
# Docker
docker-compose exec backend python manage.py flush
docker-compose exec backend python manage.py movies

# Local
rm backend/db.sqlite3
python manage.py migrate
python manage.py movies
```

### Clear Everything and Start Fresh
```bash
# Docker
make clean
make rebuild
make populate

# Local
# Delete db.sqlite3 and node_modules, then reinstall
```

---

## Step 5: Development Workflow

### Making Code Changes

**Backend (Docker):**
- Code changes are reflected immediately (volume mounting)
- Restart if needed: `docker-compose restart backend`

**Frontend (Docker):**
- Rebuild after changes: `docker-compose up --build frontend`
- Or use `Dockerfile.dev` for hot-reload

**Local Development:**
- Backend: Auto-reloads on save
- Frontend: Hot Module Replacement (HMR) enabled

### Adding New Features

1. Make code changes
2. Test locally or rebuild Docker containers
3. Check logs if issues occur
4. Commit changes (excluding .env files)

---

## Step 6: Production Deployment (Future)

When ready for production:

1. Set `DEBUG=False` in backend
2. Use PostgreSQL instead of SQLite
3. Configure proper CORS settings
4. Set up SSL/TLS certificates
5. Use environment variables for secrets
6. Configure static file serving
7. Set up CI/CD pipeline

---

## Quick Command Reference

```bash
# Start everything
make rebuild          # or: docker-compose up --build

# View logs
make logs             # or: docker-compose logs -f

# Populate database
make populate         # or: docker-compose exec backend python manage.py movies

# Stop everything
make down             # or: docker-compose down

# Clean everything
make clean            # or: docker-compose down -v
```

---

## You're Ready! 🚀

Start with:
```bash
make rebuild
make populate
```

Then open http://localhost:3000 in your browser!

