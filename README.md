# Service Alpha

A FastAPI-based service for contract search and analysis with PostgreSQL, Redis, and Celery worker support.

## Features

- FastAPI REST API with automatic documentation (Swagger UI at `/docs`, ReDoc at `/redoc`)
- PostgreSQL database for data persistence
- Redis for caching and Celery task queue
- Celery worker for background task processing
- Static file serving with sample HTML/CSS
- Health check endpoints for monitoring
- Docker and Docker Compose support

## Prerequisites

- Docker and Docker Compose
- Git
- (Optional) Python 3.11+ for local development

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd service_alpha
```

### 2. Configure Environment Variables

Create or update the `.env` file in the project root:

```bash
# Database Configuration
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# DeepSeek API Configuration (required for AI features)
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Zakupki Base URL
ZAKUPKI_BASE_URL=https://zakupki.gov.ru
```

**Important**: Replace `your_deepseek_api_key_here` with your actual DeepSeek API key.

### 3. Run with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up --build -d
```

### 4. Access the Application

- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Static Files**: http://localhost:8000/static/index.html
- **Health Check**: http://localhost:8000/health
- **Root Endpoint**: http://localhost:8000/

The service is also accessible on standard HTTP port 80: http://localhost/

## Service Architecture

The Docker Compose setup includes:

1. **PostgreSQL Database** (`db` service)
   - Port: 5432
   - Database: `dbname`
   - User: `user`
   - Password: `password`

2. **Redis Cache** (`redis` service)
   - Port: 6379
   - Used for caching and Celery task queue

3. **FastAPI Web Application** (`web` service)
   - Ports: 80 and 8000
   - Auto-reload enabled for development
   - Static files served from `/static` directory

4. **Celery Worker** (optional, can be added to docker-compose)

## API Endpoints

### Core Endpoints

- `GET /` - Service information and available endpoints
- `GET /health` - Health check with service status
- `GET /static/*` - Static file serving

### Search API

- `POST /api/search` - Create a new search task
- `GET /api/search/{search_id}` - Get search results
- `GET /api/search` - List all searches

### Example Usage

```bash
# Health check
curl http://localhost:8000/health

# Create a search task
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"object_name": "construction materials", "limit_contracts": 5}'
```

## Development

### Local Development (without Docker)

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables in `.env` file

3. Run the application:
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

4. Run Celery worker (in separate terminal):
   ```bash
   celery -A app.worker.celery_app worker --loglevel=info
   ```

### Running Tests

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app tests/
```

## Docker Commands

### Useful Docker Compose Commands

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# View logs
docker-compose logs
docker-compose logs -f  # Follow logs
docker-compose logs web  # Logs for specific service

# Rebuild and restart
docker-compose up --build -d

# Check service status
docker-compose ps
```

### Individual Docker Commands

```bash
# Build Docker image
docker build -t service-alpha .

# Run container
docker run -p 8000:8000 --env-file .env service-alpha

# Access container shell
docker exec -it <container_id> /bin/bash
```

## Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection URL | `postgresql+asyncpg://user:password@db:5432/dbname` |
| `REDIS_URL` | Redis connection URL | `redis://redis:6379/0` |
| `DEEPSEEK_API_KEY` | DeepSeek API key for AI features | (required) |
| `ZAKUPKI_BASE_URL` | Base URL for Zakupki API | `https://zakupki.gov.ru` |

## Project Structure

```
service_alpha/
├── app/                    # FastAPI application
│   ├── __init__.py
│   ├── main.py            # Main FastAPI app with static files
│   ├── database.py        # Database configuration
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── celery_app.py      # Celery configuration
│   ├── worker.py          # Celery tasks
│   ├── worker_simple.py   # Simplified worker
│   └── routers/           # API routers
│       └── search.py      # Search endpoints
├── alembic/               # Database migrations
├── static/                # Static assets
│   ├── index.html         # Static homepage
│   └── style.css          # CSS styles
├── tests/                 # Test files
├── .env                   # Environment variables
├── .gitignore
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── main.py                # Legacy main file
├── requirements.txt       # Python dependencies
├── test_worker.py         # Worker tests
└── verify_docker_setup.sh # Docker verification script
```

## Troubleshooting

### Common Issues

1. **Port already in use**: Change port mappings in `docker-compose.yml` or stop conflicting services.

2. **Database connection errors**: Ensure PostgreSQL is running and credentials in `.env` match docker-compose settings.

3. **Missing DeepSeek API key**: Obtain an API key from DeepSeek and add it to `.env` file.

4. **Static files not loading**: Check that the `static` directory exists and contains files.

### Docker Issues

```bash
# Check if Docker is running
docker ps

# Check container logs
docker-compose logs web

# Rebuild from scratch
docker-compose down -v
docker-compose up --build
```

### Database Migrations

If you need to run database migrations:

```bash
# Enter the web container
docker-compose exec web bash

# Run migrations
alembic upgrade head
```

## License

[Add your license information here]

## Support

For issues and questions, please check the GitHub repository or contact the development team.