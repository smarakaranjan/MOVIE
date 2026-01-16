# Movie Explorer - Docker Setup

This guide explains how to run the Movie Explorer application using Docker.

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)
- Make (optional, for convenience commands)

## Quick Start

### Using Makefile (Recommended)
```bash
make rebuild    # Build and start all services
```

### Using Docker Compose
```bash
docker-compose up --build
```

**Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs/swagger/

## Services

### Backend (Django)
- **Port:** 8000
- **Container:** movie-explorer-backend
- **Database:** SQLite (default)
- **Auto-migrations:** Runs on container start

### Frontend (React + Vite)
- **Port:** 3000
- **Container:** movie-explorer-frontend
- **Server:** Nginx
- **Build:** Multi-stage build for optimized production bundle

## Environment Variables

### Backend
Create a `.env` file in the `backend/` directory:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,backend
```

### Frontend
The frontend uses environment variables for API URL:
- `VITE_API_URL` - Backend API URL (default: http://localhost:8000/api)

## Commands Reference

### Using Makefile

| Makefile Command | Description |
|-----------------|-------------|
| `make build` | Build all containers |
| `make up` | Start all services in background |
| `make up-logs` | Start all services with logs |
| `make down` | Stop all services |
| `make restart` | Restart all services |
| `make logs` | View all logs |
| `make logs-backend` | View backend logs only |
| `make logs-frontend` | View frontend logs only |
| `make shell-backend` | Access backend container shell |
| `make shell-frontend` | Access frontend container shell |
| `make migrate` | Run database migrations |
| `make populate` | Populate database with movies |
| `make superuser` | Create Django superuser |
| `make clean` | Remove all containers and volumes |
| `make rebuild` | Rebuild and start all services |

### Using Docker Compose (Direct)

| Docker Compose Command | Equivalent Makefile |
|----------------------|-------------------|
| `docker-compose build` | `make build` |
| `docker-compose up -d` | `make up` |
| `docker-compose up` | `make up-logs` |
| `docker-compose down` | `make down` |
| `docker-compose restart` | `make restart` |
| `docker-compose logs -f` | `make logs` |
| `docker-compose logs -f backend` | `make logs-backend` |
| `docker-compose logs -f frontend` | `make logs-frontend` |
| `docker-compose exec backend bash` | `make shell-backend` |
| `docker-compose exec frontend sh` | `make shell-frontend` |
| `docker-compose exec backend python manage.py migrate` | `make migrate` |
| `docker-compose exec backend python manage.py movies` | `make populate` |
| `docker-compose exec backend python manage.py createsuperuser` | `make superuser` |
| `docker-compose down -v` | `make clean` |
| `docker-compose up --build -d` | `make rebuild` |

### Common Operations

**Start services:**
```bash
# Using Makefile
make up

# Using Docker Compose
docker-compose up -d
```

**View logs:**
```bash
# Using Makefile
make logs

# Using Docker Compose
docker-compose logs -f
```

**Stop services:**
```bash
# Using Makefile
make down

# Using Docker Compose
docker-compose down
```

**Rebuild containers:**
```bash
# Using Makefile
make rebuild

# Using Docker Compose
docker-compose up --build -d
```

**Populate database:**
```bash
# Using Makefile
make populate

# Using Docker Compose
docker-compose exec backend python manage.py movies
```

**Run backend management commands:**
```bash
# Using Makefile
make migrate
make superuser

# Using Docker Compose
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

## Development

For development with hot-reload:

1. **Backend:** The backend uses volume mounting, so code changes are reflected immediately
2. **Frontend:** Rebuild the frontend container after code changes:
   ```bash
   docker-compose up --build frontend
   ```

## Production Considerations

For production deployment:

1. Set `DEBUG=False` in backend settings
2. Use a production database (PostgreSQL recommended)
3. Configure proper CORS settings
4. Use environment variables for secrets
5. Set up SSL/TLS certificates
6. Configure proper static file serving

## Troubleshooting

### Port already in use
If ports 3000 or 8000 are already in use, modify the port mappings in `docker-compose.yml`:
```yaml
ports:
  - "3001:80"  # Change frontend port
  - "8001:8000"  # Change backend port
```

### Database issues
To reset the database:
```bash
docker-compose exec backend python manage.py flush
docker-compose exec backend python manage.py movies
```

### Clear all containers and volumes
```bash
docker-compose down -v
```

