---
title: Hackathon2 Todo Backend
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# Todo Backend API

RESTful API for todo task management with JWT authentication and PostgreSQL persistence.

## Features

- 6 RESTful CRUD endpoints for task management
- JWT authentication with Better Auth integration
- Multi-user support with data isolation
- PostgreSQL database (Neon Serverless)
- Automatic OpenAPI/Swagger documentation
- CORS configuration for frontend integration

## Prerequisites

- Python 3.13+
- Neon PostgreSQL account ([neon.tech](https://neon.tech))
- Better Auth secret key (shared with frontend)

## Quick Start

### 1. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file in the `backend/` directory:

```bash
cp .env.example .env
```

Edit `.env` with your actual values:

```
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require
BETTER_AUTH_SECRET=your-secret-key-min-32-characters
ALLOWED_ORIGINS=http://localhost:3000
```

### 3. Run the Server

```bash
# Development mode (with auto-reload)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000
```

Server starts at: `http://localhost:8000`

## API Documentation

### Interactive Documentation

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Endpoints

All task endpoints require JWT authentication via `Authorization: Bearer <token>` header.

#### Health Check

```
GET /api/health
```

No authentication required. Returns service health status.

#### List Tasks

```
GET /api/tasks
```

Returns all tasks for the authenticated user.

#### Create Task

```
POST /api/tasks
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"  // optional
}
```

Creates a new task. Returns task with auto-generated ID and timestamps.

#### Get Task by ID

```
GET /api/tasks/{id}
```

Returns a specific task if it belongs to the authenticated user.

#### Update Task

```
PUT /api/tasks/{id}
Content-Type: application/json

{
  "title": "Buy groceries and cook dinner",  // optional
  "description": "Updated description"  // optional
}
```

Updates task fields. Only provided fields are updated.

#### Toggle Task Completion

```
PATCH /api/tasks/{id}/complete
```

Toggles the completion status of a task (false → true or true → false).

#### Delete Task

```
DELETE /api/tasks/{id}
```

Permanently deletes a task. Returns 204 No Content on success.

## Testing

### Manual Testing with cURL

Generate a test JWT token:

```python
from jose import jwt
from datetime import datetime, timedelta

SECRET = "your-secret-key-min-32-characters"
payload = {
    "userId": "test-user-123",
    "exp": datetime.utcnow() + timedelta(days=1)
}
token = jwt.encode(payload, SECRET, algorithm="HS256")
print(token)
```

Test endpoints:

```bash
# Health check (no auth)
curl http://localhost:8000/api/health

# List tasks (with auth)
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8000/api/tasks

# Create task
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "description": "Testing API"}'
```

## Project Structure

```
backend/
├── main.py              # FastAPI app, CORS, startup
├── models.py            # Task model and Pydantic schemas
├── database.py          # DB engine, session, settings
├── auth.py              # JWT verification
├── routes/
│   └── tasks.py         # Task CRUD endpoints
├── .env                 # Environment variables (git-ignored)
├── .env.example         # Environment template
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Environment Variables

Required variables (see `.env.example` for template):

- `DATABASE_URL`: PostgreSQL connection string from Neon
- `BETTER_AUTH_SECRET`: JWT signing secret (must match frontend)
- `ALLOWED_ORIGINS`: Comma-separated CORS allowed origins

## Development

### Code Standards

- Type hints on all functions
- Docstrings for all public APIs
- SQLModel for database operations (no raw SQL)
- Environment variables for secrets
- Follow FastAPI best practices

### Database Migrations

Current setup uses `SQLModel.metadata.create_all()` for table creation.

For schema changes in production, migrate to Alembic:

```bash
pip install alembic
alembic init migrations
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

## Troubleshooting

### Database Connection Errors

- Verify `DATABASE_URL` is correct
- Check Neon project is not paused (free tier auto-pauses)
- Test connection: `psql "YOUR_DATABASE_URL"`

### JWT Verification Fails

- Ensure `BETTER_AUTH_SECRET` matches frontend
- Check token is not expired
- Verify `Authorization` header format: `Bearer <token>` (with space)

### CORS Errors

- Verify `ALLOWED_ORIGINS` includes frontend URL
- Restart server after changing `.env`
- Check browser DevTools Network tab for preflight requests

## Detailed Setup Guide

For detailed step-by-step setup instructions, see:
- `specs/001-todo-backend-api/quickstart.md`

## Specification Documents

- Feature specification: `specs/001-todo-backend-api/spec.md`
- Implementation plan: `specs/001-todo-backend-api/plan.md`
- Task breakdown: `specs/001-todo-backend-api/tasks.md`
- Data model: `specs/001-todo-backend-api/data-model.md`
- API contracts: `specs/001-todo-backend-api/contracts/api-endpoints.md`

## License

See main project LICENSE file.
