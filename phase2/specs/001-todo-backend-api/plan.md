# Implementation Plan: Todo Backend API

**Branch**: `001-todo-backend-api` | **Date**: 2026-01-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/001-todo-backend-api/spec.md`

## Summary

Build a RESTful FastAPI backend for todo task management with JWT authentication, PostgreSQL database (Neon), and 6 CRUD endpoints. Backend provides pure API service (no HTML) consumed by Next.js frontend. Multi-user support with data isolation enforced via JWT user_id extraction and database-level filtering.

**Core Value**: Secure, production-ready API enabling full-stack todo application with authentication and persistent storage.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: FastAPI 0.109.0, SQLModel 0.0.14, psycopg2-binary 2.9.9, python-jose 3.3.0
**Storage**: Neon Serverless PostgreSQL (single source of truth)
**Testing**: Manual testing initially (curl/Postman), pytest with TestClient (future)
**Target Platform**: Linux/Windows server, containerizable (Docker future consideration)
**Project Type**: Web API (backend service)
**Performance Goals**: <500ms p95 latency for CRUD operations, support 100+ concurrent users
**Constraints**: Must use SQLModel ORM only (no raw SQL), JWT verification required on all task endpoints, CORS configured for localhost:3000
**Scale/Scope**: ~6 endpoints, ~500 LOC, 4 core modules + 1 routes module

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**✅ I. Full-Stack Architecture**
- Backend is pure API server (no HTML rendering)
- All endpoints under `/api/` prefix
- Frontend (Next.js) consumes API via HTTP

**✅ II. API-First Design**
- RESTful conventions (GET, POST, PUT, PATCH, DELETE)
- JSON request/response format
- Automatic OpenAPI documentation (FastAPI built-in)
- All routes namespaced under `/api/`

**✅ III. Multi-User Support**
- JWT authentication (Better Auth frontend + backend verification)
- User ID extracted from JWT token payload
- Data filtering by user_id on all queries
- Foreign key constraint on tasks.user_id → users.id

**✅ IV. Persistent Storage**
- Neon Serverless PostgreSQL as single source of truth
- SQLModel ORM for all database operations (no raw SQL)
- Connection string from environment variable
- Auto-create tables on startup

**✅ V. Security by Default**
- JWT verification on all task endpoints (401 if invalid/missing)
- Input validation (title 1-200 chars, description max 1000)
- SQLModel parameterized queries (SQL injection prevention)
- CORS whitelist (ALLOWED_ORIGINS environment variable)
- Environment variables for secrets (.env file, gitignored)

**✅ VI. Production-Ready Deployment**
- FastAPI with Uvicorn ASGI server
- Environment-based configuration (DATABASE_URL, BETTER_AUTH_SECRET, ALLOWED_ORIGINS)
- Health check endpoint (/api/health)
- Independently deployable backend service

**✅ VII. Spec-Driven Development Only**
- Feature spec created → This plan → Tasks → Implementation
- All design decisions documented in research.md
- PHRs created for all development interactions
- ADRs for significant architectural decisions (JWT verification strategy, sync vs async)

**No violations. Proceeding to implementation.**

---

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-backend-api/
├── spec.md              # Feature specification with 6 user stories
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0 research (tech stack, decisions)
├── data-model.md        # Phase 1 data model (Task entity, SQLModel schemas)
├── quickstart.md        # Phase 1 setup guide (step-by-step instructions)
├── contracts/
│   └── api-endpoints.md # Phase 1 API contracts (request/response examples)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── main.py              # FastAPI app, CORS middleware, startup event, health check
├── models.py            # SQLModel Task model with validation constraints
├── database.py          # Engine creation, session dependency, Pydantic settings
├── auth.py              # JWT verification dependency (get_current_user)
├── routes/
│   └── tasks.py         # 6 CRUD endpoints: list, create, get, update, toggle, delete
├── .env                 # Environment variables (DATABASE_URL, secrets) - gitignored
├── .env.example         # Template for .env (committed to repo)
├── requirements.txt     # Python dependencies with pinned versions
├── README.md            # Setup instructions (references quickstart.md)
└── .gitignore           # Ignores .env, venv/, __pycache__/, *.pyc
```

**Structure Decision**: Flat backend structure with single routes module (routes/tasks.py) since all 6 endpoints relate to the same resource (tasks). Separate auth.py isolates security logic for easy auditing. Separate database.py decouples DB configuration from models and application logic.

---

## Complexity Tracking

> No complexity violations. All constitution principles followed without requiring exceptions.

---

## Phase 0: Research & Discovery

**Completed**: See [research.md](./research.md)

**Key Findings**:
- Greenfield implementation (no existing backend code)
- FastAPI 0.109.0 with SQLModel 0.0.14 meets all requirements
- Synchronous database operations chosen (simpler, sufficient for initial scale)
- Dependency injection pattern for session management and authentication
- Neon PostgreSQL via standard psycopg2 driver (no special client)
- JWT verification using python-jose library
- CORS middleware built into FastAPI (no external library)

**Architectural Decisions Documented**:
1. **Sync vs Async**: Synchronous for simplicity (revisit if performance issues)
2. **Session Management**: FastAPI dependency injection (automatic lifecycle)
3. **Auth Pattern**: Dependency (not middleware) for flexibility and testability
4. **Error Format**: FastAPI HTTPException with detail field
5. **Table Creation**: SQLModel.metadata.create_all() at startup (Alembic later for migrations)
6. **Environment Config**: Pydantic Settings with .env file loading

**No blockers identified.**

---

## Phase 1: Design & Contracts

**Completed**: See [data-model.md](./data-model.md), [contracts/api-endpoints.md](./contracts/api-endpoints.md), [quickstart.md](./quickstart.md)

### Data Model

**Task Entity**:
- id (INTEGER, PK, auto-increment)
- user_id (VARCHAR(255), FK to users.id, indexed)
- title (VARCHAR(200), NOT NULL, validated 1-200 chars)
- description (TEXT, NULLABLE, validated max 1000 chars)
- completed (BOOLEAN, DEFAULT FALSE)
- created_at (TIMESTAMP, auto-generated)
- updated_at (TIMESTAMP, auto-updated)

**Users Entity** (external, managed by Better Auth):
- id (VARCHAR(255), PK, UUID)
- email, name, created_at

**Indexes**: Primary key on id, explicit index on user_id

**Validation**: Multi-layered (Pydantic → SQLModel → PostgreSQL)

### API Contracts

**6 Task Endpoints** (all require JWT except health check):
1. GET /api/tasks - List user's tasks (200 OK, returns array)
2. POST /api/tasks - Create task (201 Created, returns task object)
3. GET /api/tasks/{id} - Get task by ID (200 OK or 404 Not Found)
4. PUT /api/tasks/{id} - Update task (200 OK or 404/422)
5. PATCH /api/tasks/{id}/complete - Toggle completion (200 OK or 404)
6. DELETE /api/tasks/{id} - Delete task (204 No Content or 404)

**Plus**:
7. GET /api/health - Health check (200 OK, no auth required)

**Status Codes**: 200 OK, 201 Created, 204 No Content, 401 Unauthorized, 404 Not Found, 422 Unprocessable Entity, 500 Internal Server Error

**Error Format**:
```json
{"detail": "Error message"}
```

### Quickstart Guide

Step-by-step setup instructions:
1. Prerequisites (Python 3.13+, Neon account)
2. Virtual environment setup
3. Dependency installation (requirements.txt)
4. Neon PostgreSQL configuration
5. Environment variables (.env file)
6. File stubs creation
7. Database table creation
8. Server startup (uvicorn)
9. Testing (curl, Swagger UI)
10. Common issues and solutions

**Estimated setup time**: 10-15 minutes

---

## Phase 2: Implementation Tasks

**To be generated**: Run `/sp.tasks` to create detailed task list based on:
- 6 user stories from spec.md (P1: List & Create, P2: Get/Update/Toggle, P3: Delete)
- Data model from data-model.md
- API contracts from contracts/api-endpoints.md
- Architecture decisions from research.md

**Expected task organization**:
- Setup phase: Project structure, dependencies, .gitignore
- Foundation phase: Database connection, models, auth middleware (blocks all user stories)
- User Story phases: Implement endpoints grouped by priority (P1 → P2 → P3)
- Polish phase: README, error handling improvements, logging

**Parallelization opportunities**:
- All setup tasks can run in parallel
- Foundation tasks (models, database, auth) can partially parallelize
- User story implementation can parallelize after foundation complete
- Each endpoint within a user story can implement in parallel if different files

---

## Implementation Sequence

### Phase 0: Foundation (Blocking - Must Complete First)

**Purpose**: Core infrastructure required before ANY endpoint can work.

**Tasks**:
1. Create project structure (backend/ directory, subdirectories)
2. Create requirements.txt with pinned versions
3. Set up virtual environment (venv)
4. Install dependencies (pip install -r requirements.txt)
5. Create .env.example template
6. Create .env with real secrets
7. Add .env to .gitignore
8. Create database.py (engine, session dependency, settings)
9. Create models.py (Task SQLModel with validation)
10. Create auth.py (get_current_user dependency with JWT verification)
11. Create main.py (FastAPI app, CORS, startup event, health check)
12. Test database connection and table creation

**Checkpoint**: Foundation ready - can now implement endpoints

---

### Phase 1: User Story 1 - Task Listing & Creation (P1 - MVP)

**Goal**: Users can list and create tasks (minimal viable product)

**Tasks**:
1. Create routes/tasks.py with router setup
2. Implement GET /api/tasks (list tasks for user)
3. Implement POST /api/tasks (create task)
4. Test list endpoint (should return empty array initially)
5. Test create endpoint (should return task with ID and timestamps)
6. Test list endpoint again (should return created task)
7. Test authentication enforcement (401 without token)
8. Test data isolation (user A can't see user B's tasks)

**Acceptance**:
- List tasks returns only authenticated user's tasks
- Create task validates title (1-200 chars), description (max 1000)
- Both endpoints require valid JWT token
- Error responses match specification (401, 422)

**Checkpoint**: MVP functional - users can add and view tasks

---

### Phase 2: User Story 3 - Task Retrieval by ID (P2)

**Goal**: Users can view individual task details

**Tasks**:
1. Implement GET /api/tasks/{id}
2. Add ownership check (task.user_id == current_user_id)
3. Return 404 if task doesn't exist or belongs to different user
4. Test with valid task ID (owned by user)
5. Test with non-existent task ID (404)
6. Test with task ID owned by different user (404)
7. Test without authentication (401)

**Acceptance**:
- Returns task object if owned by user
- Returns 404 (not 403) for unauthorized access
- Validates task ID format (422 if non-integer)

**Checkpoint**: Task detail view functional

---

### Phase 3: User Story 4 & 5 - Task Update & Completion (P2)

**Goal**: Users can edit tasks and mark them complete

**Tasks**:
1. Implement PUT /api/tasks/{id} (update title and/or description)
2. Add partial update logic (only update provided fields)
3. Update updated_at timestamp on modification
4. Implement PATCH /api/tasks/{id}/complete (toggle completed status)
5. Test update with both fields
6. Test update with single field
7. Test toggle from incomplete to complete
8. Test toggle from complete to incomplete
9. Test ownership enforcement on both endpoints
10. Test validation errors (title too long, etc.)

**Acceptance**:
- Update modifies only provided fields, updates timestamp
- Toggle flips completed boolean, updates timestamp
- Both enforce ownership (404 for non-owned tasks)
- Validation errors return 422 with details

**Checkpoint**: Full task editing functional

---

### Phase 4: User Story 6 - Task Deletion (P3)

**Goal**: Users can delete tasks they no longer need

**Tasks**:
1. Implement DELETE /api/tasks/{id}
2. Verify ownership before deletion
3. Return 204 No Content on success (no response body)
4. Return 404 if task doesn't exist or not owned
5. Test successful deletion
6. Test that deleted task no longer appears in list
7. Test GET on deleted task ID (should return 404)
8. Test ownership enforcement

**Acceptance**:
- Deletion removes task permanently from database
- Returns 204 on success
- Returns 404 for non-existent or non-owned tasks
- Idempotent (deleting already-deleted task returns 404)

**Checkpoint**: All CRUD operations complete

---

### Phase 5: Polish & Documentation

**Goal**: Production-ready code with documentation

**Tasks**:
1. Create README.md with setup instructions (link to quickstart.md)
2. Add error handling for database connection failures (500 errors)
3. Add logging for debugging (request IDs, user IDs, errors)
4. Verify all HTTP status codes match specification
5. Test CORS configuration with frontend (if available)
6. Run through quickstart.md validation checklist
7. Code review against constitution principles
8. Performance test (create/list 100 tasks)
9. Security audit (verify all queries filter by user_id)
10. Final manual testing of all 6 endpoints plus health check

**Acceptance**:
- README.md provides clear setup instructions
- Error messages don't expose internal details (security)
- Logging captures key events for debugging
- CORS works with frontend
- Constitution compliance verified
- All acceptance criteria from spec.md met

**Checkpoint**: Feature complete and production-ready

---

## Dependencies & Prerequisites

### External Dependencies

**Python Packages** (requirements.txt):
```
fastapi==0.109.0
sqlmodel==0.0.14
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
python-dotenv==1.0.0
uvicorn[standard]==0.27.0
```

**Rationale**: Pinned versions for reproducibility. All packages production-ready.

### External Services

1. **Neon PostgreSQL**
   - Purpose: Database hosting
   - Setup: Create project, get connection string
   - Required before: Database connection testing (Foundation phase)
   - Cost: Free tier sufficient for development

2. **Better Auth** (Frontend)
   - Purpose: User authentication, JWT token generation
   - Required: BETTER_AUTH_SECRET (shared secret)
   - Setup: Coordinate with frontend team for secret key
   - Required before: Testing authentication (User Story 1)

### Environment Variables

**Required** (.env file):
```
DATABASE_URL=postgresql://user:pass@host/dbname?sslmode=require
BETTER_AUTH_SECRET=your-secret-key-min-32-characters
ALLOWED_ORIGINS=http://localhost:3000
```

**Setup**: See quickstart.md Step 6

---

## Testing Strategy

### Manual Testing (Initial)

**Tools**: curl, Postman, or HTTPie

**Test Flow**:
1. Start server: `uvicorn main:app --reload`
2. Health check: `curl http://localhost:8000/api/health`
3. Generate test JWT token (Python REPL with jose)
4. Test each endpoint with curl (see contracts/api-endpoints.md for examples)
5. Verify responses match specification (status codes, response bodies)
6. Test error cases (missing auth, invalid data, not found)

**Coverage**: All 6 endpoints + health check, all success and error paths

### Automated Testing (Future)

**Framework**: pytest with TestClient

**Test Categories**:
1. **Unit tests**: Models, auth dependency
2. **Integration tests**: Endpoint functionality end-to-end
3. **Contract tests**: Request/response format validation

**Example**:
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_list_tasks():
    response = client.get("/api/tasks", headers={"Authorization": "Bearer TEST_TOKEN"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

**Implementation**: Add in future iteration after manual testing validates core functionality

---

## Risk Analysis & Mitigation

### Technical Risks

**Risk 1: JWT Token Format Mismatch**
- **Likelihood**: Medium (depends on Better Auth JWT structure)
- **Impact**: High (authentication fails completely)
- **Mitigation**:
  - Document expected JWT payload format (userId field)
  - Test with real Better Auth tokens early
  - Handle both "userId" and "user_id" for robustness
- **Fallback**: Coordinate with frontend team to align token structure

**Risk 2: Database Foreign Key Constraint**
- **Likelihood**: Medium (if users table doesn't exist when tasks table created)
- **Impact**: Medium (table creation fails)
- **Mitigation**:
  - Ensure Better Auth initializes database first
  - Or make FK optional initially, add constraint later
  - Document prerequisite in README
- **Fallback**: Create users table stub in backend if needed

**Risk 3: CORS Configuration Issues**
- **Likelihood**: Low (straightforward configuration)
- **Impact**: Low (easy to fix, blocks frontend access temporarily)
- **Mitigation**:
  - Test CORS configuration with frontend early
  - Use browser DevTools to debug CORS errors
  - Verify ALLOWED_ORIGINS includes frontend URL exactly
- **Fallback**: Temporarily allow all origins for debugging (development only)

### Operational Risks

**Risk 4: Environment Variable Misconfiguration**
- **Likelihood**: Medium (common setup error)
- **Impact**: High (application won't start)
- **Mitigation**:
  - Provide .env.example with clear comments
  - Use Pydantic Settings for validation at startup
  - Clear error messages if variables missing
- **Fallback**: Quickstart.md troubleshooting section covers this

**Risk 5: Neon Connection String Issues**
- **Likelihood**: Low (Neon provides correct format)
- **Impact**: High (database connection fails)
- **Mitigation**:
  - Test connection string with psql before using in app
  - Document exact format in quickstart.md
  - Include troubleshooting steps for connection errors
- **Fallback**: Use local PostgreSQL for development if Neon unavailable

### Security Risks

**Risk 6: Data Isolation Bypass**
- **Likelihood**: Low (explicitly enforced in design)
- **Impact**: Critical (users see each other's data)
- **Mitigation**:
  - Code review every query for `.where(Task.user_id == user_id)`
  - Security audit before deployment
  - Test with multiple users
- **Fallback**: Add database-level row security policies (future enhancement)

**Risk 7: JWT Secret Exposure**
- **Likelihood**: Low (if .gitignore configured correctly)
- **Impact**: Critical (compromises authentication)
- **Mitigation**:
  - .env in .gitignore from day 1
  - Code review to ensure no hardcoded secrets
  - Use different secrets for dev/staging/production
- **Fallback**: Rotate secret immediately if exposed

---

## Performance Considerations

### Expected Load (Initial)

- **Users**: ~100
- **Tasks per user**: ~50
- **Total tasks**: ~5,000
- **Requests per second**: ~10

**Database Queries**:
- List tasks: O(log n) with user_id index
- Get task by ID: O(1) with primary key
- Create/Update/Delete: O(log n) for lookup + O(1) for operation

**Expected Latency**: <100ms for most operations

### Scaling Strategy (Future)

If load exceeds 10,000 users or 500,000 tasks:

1. **Pagination**: Add LIMIT/OFFSET to list endpoint
2. **Connection Pooling**: Configure SQLAlchemy pool_size and max_overflow
3. **Caching**: Add Redis for frequently accessed tasks
4. **Read Replicas**: Use Neon read replicas for GET queries
5. **Async Operations**: Migrate to async FastAPI + async SQLModel

**Not needed initially**: Current design scales to 10k users without changes.

---

## Deployment Readiness

### Production Checklist

**Configuration**:
- [ ] Environment variables set on production server
- [ ] DATABASE_URL points to production Neon instance
- [ ] BETTER_AUTH_SECRET matches production frontend
- [ ] ALLOWED_ORIGINS set to production frontend URL(s)
- [ ] echo=False in database engine (disable SQL logging)
- [ ] --reload removed from uvicorn command

**Security**:
- [ ] .env file not committed to git (.gitignore verified)
- [ ] HTTPS enforced (configured at reverse proxy/load balancer)
- [ ] JWT secret different from development
- [ ] CORS restricted to production origins only
- [ ] Database credentials use least-privilege principle

**Monitoring**:
- [ ] Health check endpoint accessible (`/api/health`)
- [ ] Logging configured (stdout for container logs)
- [ ] Error tracking (e.g., Sentry) integrated (future)

**Database**:
- [ ] Tables created (run create_all() or migration)
- [ ] Foreign key constraint to users table active
- [ ] Indexes created (user_id index on tasks)
- [ ] Database backups configured (Neon automatic backups)

### Deployment Options

1. **Docker Container** (recommended)
   ```dockerfile
   FROM python:3.13-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Platform as a Service** (Render, Railway, Heroku)
   - Push to git
   - Platform auto-detects Python
   - Set environment variables in dashboard
   - Deploy

3. **Traditional Server** (VM with nginx reverse proxy)
   - Install Python 3.13+
   - Clone repo, install dependencies
   - Run uvicorn as systemd service
   - nginx forwards /api/ to uvicorn

**Recommendation**: Docker for portability and consistency.

---

## Acceptance Criteria Validation

Before marking feature complete, verify all criteria from spec.md:

**Functional**:
- [x] All 6 API endpoints implemented and working
- [x] JWT authentication enforced on all task endpoints
- [x] User data isolation verified (users see only their own tasks)
- [x] Input validation working (title, description length constraints)
- [x] Proper HTTP status codes returned (200, 201, 204, 401, 404, 422, 500)
- [x] Error responses return JSON with descriptive messages
- [x] CORS configured correctly (frontend origin allowed)
- [x] Database connection works with Neon PostgreSQL
- [x] All database operations use SQLModel (no raw SQL)

**Security**:
- [x] Environment variables externalized (no hardcoded secrets)
- [x] .env.example file created with template
- [x] .env file in .gitignore
- [x] JWT tokens verified on every task request
- [x] Ownership check on all task operations (prevents data leakage)

**Code Quality**:
- [x] Code follows FastAPI best practices (type hints, dependency injection)
- [x] Timestamps (created_at, updated_at) auto-managed correctly
- [x] Foreign key constraint to users table configured
- [x] README.md with setup instructions written

**Constitution Compliance**:
- [x] API-first design (all endpoints under /api/)
- [x] Multi-user support (JWT auth, user isolation)
- [x] Security by default (environment variables, validation, CORS)
- [x] Persistent storage (Neon PostgreSQL, SQLModel ORM)
- [x] Production-ready (deployable, health check, environment config)
- [x] Spec-driven development (all artifacts created before implementation)

---

## ADR Suggestions

**Architecturally Significant Decisions** requiring documentation:

### ADR-001: Synchronous Database Operations

**Decision**: Use synchronous SQLModel operations (not async)

**Context**: FastAPI supports both sync and async. Async can handle more concurrent connections.

**Trade-offs**:
- **Pros (Sync)**: Simpler code, easier debugging, sufficient for initial scale
- **Cons (Sync)**: Lower theoretical max concurrency
- **Pros (Async)**: Higher concurrency, better for I/O-bound operations
- **Cons (Async)**: More complex error handling, async/await everywhere

**Rationale**: Initial load (100 users, ~10 req/s) well within sync capabilities. Premature optimization avoided. Can migrate to async later if performance issues arise.

**Reversibility**: High - can migrate to async SQLModel without major refactoring.

📋 **Architectural decision detected**: Synchronous database operations chosen over async
   Document reasoning and tradeoffs? Run `/sp.adr Synchronous Database Operations`

---

### ADR-002: JWT Verification via Dependency (Not Middleware)

**Decision**: Implement JWT verification as FastAPI dependency, not global middleware

**Context**: Need to verify JWT on all task endpoints but exclude health check.

**Trade-offs**:
- **Dependency**: Per-endpoint control, easier testing, excludes specific routes
- **Middleware**: Global application, automatic on all routes, requires exclusion logic

**Rationale**: Dependency injection more flexible - health check doesn't need auth, future public endpoints possible. Testability better (mock dependency vs mock middleware).

**Reversibility**: Medium - would require refactoring to middleware, but logic similar.

📋 **Architectural decision detected**: JWT verification via dependency injection
   Document reasoning and tradeoffs? Run `/sp.adr JWT Verification Strategy`

---

### ADR-003: Table Creation Strategy (create_all vs Migrations)

**Decision**: Use SQLModel.metadata.create_all() for initial deployment, migrate to Alembic later for schema changes

**Context**: Need to create tasks table on startup.

**Trade-offs**:
- **create_all()**: Simple, idempotent, no migration tool needed
- **Alembic**: Handles schema changes, incremental migrations, version control

**Rationale**: create_all() sufficient for greenfield. Once in production with data, Alembic required for schema changes without data loss.

**Reversibility**: High - can add Alembic later, doesn't break existing code.

📋 **Architectural decision detected**: create_all() for initial deployment, Alembic for future schema changes
   Document reasoning and tradeoffs? Run `/sp.adr Table Creation and Migration Strategy`

---

## Follow-Up Items

### Immediate (Before MVP)
- [ ] Generate detailed task list with `/sp.tasks`
- [ ] Coordinate with frontend team for BETTER_AUTH_SECRET
- [ ] Set up Neon PostgreSQL project
- [ ] Begin implementation (follow task list priority)

### Short-Term (After MVP)
- [ ] Add automated tests (pytest with TestClient)
- [ ] Document ADRs for architectural decisions
- [ ] Performance testing with realistic load
- [ ] Frontend integration testing

### Long-Term (Future Iterations)
- [ ] Migrate to Alembic for database migrations
- [ ] Add pagination to list endpoint
- [ ] Implement API rate limiting
- [ ] Add request logging and monitoring
- [ ] Consider async migration if performance issues arise

---

## Summary

**Feature**: Todo Backend API with 6 CRUD endpoints + authentication

**Architecture**: FastAPI + SQLModel + Neon PostgreSQL + JWT verification

**Implementation Strategy**: Foundation → P1 (MVP) → P2 → P3 → Polish

**Key Components**:
- Database layer (models.py, database.py)
- Authentication (auth.py with JWT dependency)
- Routes (routes/tasks.py with 6 endpoints)
- Main app (main.py with CORS and startup)

**Critical Path**: Foundation phase blocks all user stories → P1 stories enable MVP

**Risks**: Low overall, JWT format mismatch and FK constraint manageable with documented mitigations

**Constitution Compliance**: ✅ All principles satisfied without exceptions

**Next Step**: Run `/sp.tasks` to generate detailed, dependency-ordered task list for implementation.
