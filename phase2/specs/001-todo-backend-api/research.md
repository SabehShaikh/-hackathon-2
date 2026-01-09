# Research: Todo Backend API

**Feature**: 001-todo-backend-api
**Date**: 2026-01-08
**Phase**: Phase 0 - Research

## Codebase Analysis

**Finding**: This is a greenfield project - no existing backend code found.

**Current State**:
- No backend/ directory exists
- No Python files present
- No requirements.txt or dependencies
- Fresh implementation required

**Implication**: We have full architectural freedom to implement according to specification and constitution principles.

## Technology Stack Research

### FastAPI (Web Framework)

**Version**: 0.109.0 (stable, production-ready)

**Key Features**:
- Automatic OpenAPI/Swagger documentation
- Built-in request validation via Pydantic
- Dependency injection system (perfect for auth and DB sessions)
- Native async support (optional, can use sync for simplicity)
- HTTPException for consistent error responses

**Usage Pattern**:
```python
from fastapi import FastAPI, Depends, HTTPException
app = FastAPI()

@app.get("/api/tasks")
def get_tasks(user_id: str = Depends(get_current_user)):
    # user_id injected via dependency
    return tasks
```

**Rationale**: Meets constitution requirement for RESTful API with automatic documentation. Pydantic validation aligns with input validation requirements.

---

### SQLModel (ORM)

**Version**: 0.0.14 (built by FastAPI creator, combines SQLAlchemy + Pydantic)

**Key Features**:
- Unified model for DB and API (same class for both)
- SQLAlchemy 2.0 under the hood (battle-tested)
- Type hints for IDE support
- Automatic schema generation
- Parameterized queries (SQL injection prevention)

**Usage Pattern**:
```python
from sqlmodel import Field, SQLModel

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(min_length=1, max_length=200)
    completed: bool = Field(default=False)
```

**Rationale**: Meets constitution requirement for SQLModel ORM. Built-in validation matches specification constraints (title 1-200 chars, description max 1000).

---

### Neon Serverless PostgreSQL (Database)

**Connection**: Via standard PostgreSQL connection string

**Key Features**:
- Serverless PostgreSQL (auto-scaling)
- Standard psycopg2 driver compatibility
- Connection pooling built-in
- No special client library needed

**Connection String Format**:
```
postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/dbname?sslmode=require
```

**Driver**: psycopg2-binary (PostgreSQL adapter for Python)

**Rationale**: Meets constitution requirement for Neon PostgreSQL as single source of truth.

---

### python-jose (JWT Verification)

**Version**: 3.3.0 with cryptography extras

**Key Features**:
- JWT decode and verification
- Multiple algorithm support (HS256 for shared secret)
- Token expiration validation
- Clean exception handling

**Usage Pattern**:
```python
from jose import JWTError, jwt

payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
user_id = payload.get("userId")
```

**Rationale**: Meets specification requirement for JWT verification using BETTER_AUTH_SECRET. Lightweight and focused on JWT operations.

---

### CORS Middleware

**FastAPI Built-in**: CORSMiddleware from fastapi.middleware.cors

**Configuration**:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Rationale**: Meets specification CORS requirement. Built-in solution, no external dependency needed.

---

## Architectural Decisions

### 1. Synchronous vs Async

**Decision**: Use synchronous database operations (not async)

**Rationale**:
- Simpler code (no async/await complexity)
- SQLModel works seamlessly with sync SQLAlchemy
- Database operations are I/O bound, but Neon connection is fast
- Uvicorn can still handle concurrent requests efficiently
- Async adds complexity without significant benefit for this use case

**Trade-off**: Async could handle more concurrent connections, but not needed for initial deployment.

---

### 2. Database Session Management

**Decision**: Use FastAPI dependency injection for sessions

**Pattern**:
```python
def get_session():
    with Session(engine) as session:
        yield session

@app.get("/api/tasks")
def get_tasks(session: Session = Depends(get_session)):
    # session automatically opened and closed
```

**Rationale**:
- Automatic session lifecycle management
- No risk of forgotten session.close()
- Idiomatic FastAPI pattern
- Easy to test (mock the dependency)

---

### 3. Authentication Middleware

**Decision**: Use FastAPI dependency (not middleware)

**Pattern**:
```python
def get_current_user(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload["userId"]

@app.get("/api/tasks")
def get_tasks(user_id: str = Depends(get_current_user)):
    # user_id automatically extracted and verified
```

**Rationale**:
- Dependency injection more flexible than middleware
- Easy to exclude specific endpoints (health check)
- Better error handling per-endpoint
- Testable (mock the dependency)

**Alternative Rejected**: Global middleware would apply to all routes including health check, requiring exclusion logic.

---

### 4. Error Response Format

**Decision**: Use FastAPI HTTPException with detail field

**Pattern**:
```python
raise HTTPException(status_code=404, detail="Task not found")
# Returns: {"detail": "Task not found"}
```

**Rationale**:
- Consistent with FastAPI conventions
- Matches specification error format
- Automatic status code handling
- Compatible with frontend error parsing

---

### 5. Environment Variable Management

**Decision**: Use python-dotenv with Pydantic Settings

**Pattern**:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    better_auth_secret: str
    allowed_origins: str

    class Config:
        env_file = ".env"

settings = Settings()
```

**Rationale**:
- Type-safe configuration
- Automatic .env loading
- Validation of required variables at startup
- No manual os.getenv() scattered in code

---

### 6. Table Creation Strategy

**Decision**: Use SQLModel.metadata.create_all() at startup

**Pattern**:
```python
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
```

**Rationale**:
- Simple for initial deployment
- Auto-creates tables if they don't exist
- Idempotent (safe to run multiple times)

**Future Consideration**: For production with schema changes, migrate to Alembic migrations.

---

## Security Considerations

### JWT Token Verification

**Flow**:
1. Extract `Authorization` header
2. Remove "Bearer " prefix
3. Decode JWT with BETTER_AUTH_SECRET
4. Validate signature and expiration
5. Extract `userId` from payload

**Error Handling**:
- Missing header → 401 Unauthorized
- Invalid signature → 401 Unauthorized
- Expired token → 401 Unauthorized
- Missing userId in payload → 401 Unauthorized

### SQL Injection Prevention

**Approach**: SQLModel parameterized queries (never string concatenation)

**Example**:
```python
# SAFE - parameterized
session.exec(select(Task).where(Task.user_id == user_id))

# UNSAFE - never do this
session.exec(f"SELECT * FROM tasks WHERE user_id = '{user_id}'")
```

**Enforcement**: Constitution mandates no raw SQL, only SQLModel.

### Data Isolation

**Approach**: Add `.where(Task.user_id == user_id)` to ALL queries

**Critical**: Never trust task ID alone - always verify ownership:
```python
task = session.get(Task, task_id)
if not task or task.user_id != user_id:
    raise HTTPException(status_code=404, detail="Task not found")
```

**Rationale**: Return 404 (not 403) to prevent user enumeration attacks.

---

## Dependency Versions

**Reasoning for Pinned Versions**:
- FastAPI 0.109.0: Stable release, well-tested
- SQLModel 0.0.14: Latest, compatible with SQLAlchemy 2.0
- psycopg2-binary 2.9.9: Latest PostgreSQL driver
- python-jose 3.3.0: Stable, production-ready JWT library
- python-dotenv 1.0.0: Latest, simple .env loader
- uvicorn 0.27.0: Latest ASGI server with standard extras

**Update Strategy**: Pin to these versions initially, update after testing.

---

## File Structure Rationale

```
backend/
├── main.py          # Entry point, app initialization, CORS
├── models.py        # Task model (single entity, single file)
├── database.py      # Engine, session, settings (separation of concerns)
├── auth.py          # JWT verification logic (security isolation)
├── routes/
│   └── tasks.py     # All 6 task endpoints (cohesive module)
├── .env             # Secrets (git-ignored)
├── .env.example     # Template (committed)
├── requirements.txt # Dependencies
└── README.md        # Setup instructions
```

**Rationale**:
- Flat structure (no deep nesting for small API)
- Single routes/tasks.py (all endpoints related to same resource)
- Separate auth.py (security logic isolated, easy to audit)
- Separate database.py (DB concerns separate from models)

**Alternative Rejected**: Separating each endpoint into separate files adds unnecessary indirection for 6 simple endpoints.

---

## Performance Considerations

### Database Indexes

**Required Index**: `user_id` on tasks table

**Rationale**: Every query filters by user_id. Without index, queries become table scans as data grows.

**Implementation**: SQLModel Field with `index=True`

### Connection Pooling

**Approach**: SQLAlchemy's built-in connection pool (default)

**Configuration**: Not needed initially; default pool size (5) sufficient for startup.

**Future**: If load increases, configure pool_size and max_overflow in engine creation.

### Query Optimization

**Approach**: Use SQLModel select() statements (not query API)

**Rationale**: Select API is SQLAlchemy 2.0 style, better performance than legacy query API.

---

## Testing Strategy

**Approach**: Manual testing initially, automated tests in future iteration

**Test Flow**:
1. Start server with uvicorn
2. Use curl or Postman to test endpoints
3. Generate JWT token manually for testing
4. Verify responses match specification

**Future**: Add pytest with TestClient for automated endpoint tests.

---

## Open Questions (Resolved)

**Q1: Should we use async/await?**
**A**: No, synchronous for simplicity. Revisit if performance issues arise.

**Q2: How to handle database migrations?**
**A**: Use create_all() for initial version. Add Alembic later for schema changes.

**Q3: Should health check endpoint be implemented?**
**A**: Yes, add GET /api/health (no auth required) for deployment monitoring.

**Q4: How to validate JWT token format (userId vs user_id)?**
**A**: Better Auth uses "userId" in JWT payload (camelCase). Backend will handle both for robustness.

**Q5: Foreign key constraint to users table?**
**A**: Yes, but backend won't manage users table. Better Auth creates it. Backend only references via FK.

---

## Risk Assessment

### High Risk

**None identified**: Greenfield implementation with well-understood technologies.

### Medium Risk

1. **JWT token format mismatch with Better Auth**
   - Mitigation: Document expected JWT payload format, test with real Better Auth tokens
   - Impact: 401 errors if payload structure differs

2. **Database connection string format**
   - Mitigation: Test connection string with Neon console
   - Impact: Startup failure if connection string malformed

### Low Risk

1. **CORS misconfiguration**
   - Mitigation: Test with frontend once available
   - Impact: Browser blocks requests (easy to fix)

2. **Environment variable loading**
   - Mitigation: Use .env.example as template
   - Impact: Startup error with clear message

---

## Constitution Compliance Check

✅ **I. Full-Stack Architecture**: Backend is pure API server, no HTML rendering
✅ **II. API-First Design**: All endpoints under /api/, RESTful conventions, JSON responses
✅ **III. Multi-User Support**: JWT authentication, user_id filtering on all queries
✅ **IV. Persistent Storage**: Neon PostgreSQL, SQLModel ORM, no in-memory storage
✅ **V. Security by Default**: JWT verification, input validation, CORS, environment variables
✅ **VI. Production-Ready**: Independently deployable, environment-based config
✅ **VII. Spec-Driven Development**: All design decisions traced to specification requirements

**No violations identified.**

---

## Next Steps

1. Create data-model.md with detailed Task model schema
2. Create contracts/ directory with request/response examples for all 6 endpoints
3. Create quickstart.md with step-by-step setup instructions
4. Write plan.md with implementation phases and task breakdown
5. Proceed to /sp.tasks for detailed task list
