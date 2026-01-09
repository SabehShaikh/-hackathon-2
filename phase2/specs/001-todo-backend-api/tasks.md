# Tasks: Todo Backend API

**Input**: Design documents from `specs/001-todo-backend-api/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/api-endpoints.md

**Tests**: Tests are NOT included in this task list (manual testing with curl/Postman only)

**Organization**: Tasks are grouped by implementation phase (Foundation → MVP → Features → Polish) to enable incremental delivery.

## Format: `[ID] [P?] [Phase] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Phase]**: Which implementation phase (Foundation, US1, US2, etc.)
- Include exact file paths in descriptions

## Path Conventions

- **Backend service**: `backend/` at repository root
- All Python modules in `backend/` directory
- Routes in `backend/routes/` subdirectory

---

## Phase 0: Foundation (Shared Infrastructure)

**Purpose**: Project initialization and core infrastructure that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Setup Tasks

- [X] T001 [P] [Foundation] Create backend/ directory structure in D:\Q4-Gemini_CLI\Hackathon_2\phase2\backend\
- [X] T002 [P] [Foundation] Create routes/ subdirectory in backend/routes/
- [X] T003 [P] [Foundation] Create __init__.py in backend/routes/ (empty file for Python package)

**Acceptance**: Directory structure exists: backend/, backend/routes/

---

### Dependencies and Configuration

- [X] T004 [Foundation] Create requirements.txt in backend/ with pinned dependencies:
  ```
  fastapi==0.109.0
  sqlmodel==0.0.14
  psycopg2-binary==2.9.9
  python-jose[cryptography]==3.3.0
  python-dotenv==1.0.0
  uvicorn[standard]==0.27.0
  ```

**Acceptance**: requirements.txt file created with 6 dependencies

- [X] T005 [Foundation] Create .gitignore in backend/ with entries:
  ```
  .env
  venv/
  __pycache__/
  *.pyc
  *.pyo
  .DS_Store
  ```

**Acceptance**: .gitignore file prevents committing secrets and build artifacts

- [X] T006 [Foundation] Create .env.example in backend/ with template:
  ```
  # Neon PostgreSQL connection string
  DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require

  # Shared secret for JWT verification (must match Better Auth)
  BETTER_AUTH_SECRET=your-secret-key-min-32-characters

  # CORS allowed origins (comma-separated)
  ALLOWED_ORIGINS=http://localhost:3000
  ```

**Acceptance**: .env.example provides clear template for environment variables

**Dependencies**: T004 must complete before T006 (requirements drive environment needs)

---

### Database Layer

- [X] T007 [Foundation] Create models.py in backend/ with Task SQLModel:
  - Import: `from sqlmodel import Field, SQLModel; from datetime import datetime; from typing import Optional`
  - Define class Task(SQLModel, table=True) with __tablename__ = "tasks"
  - Fields: id (Optional[int], primary key), user_id (str, foreign_key="users.id", index=True, max_length=255)
  - Fields: title (str, min_length=1, max_length=200), description (Optional[str], max_length=1000, default=None)
  - Fields: completed (bool, default=False), created_at (datetime, default_factory=datetime.utcnow)
  - Fields: updated_at (datetime, default_factory=datetime.utcnow)

**Acceptance**: Task model defined with 7 fields, validation constraints, and indexes

- [X] T008 [Foundation] Create database.py in backend/ with engine and settings:
  - Import: `from sqlmodel import create_engine, Session; from pydantic_settings import BaseSettings; from typing import Generator`
  - Define class Settings(BaseSettings) with fields: database_url (str), better_auth_secret (str), allowed_origins (str)
  - Add Config inner class with env_file = ".env"
  - Instantiate settings = Settings()
  - Create engine with: `create_engine(settings.database_url, echo=True)`
  - Define get_session() function yielding Session(engine)

**Acceptance**: Database connection configured, settings loaded from .env, session dependency available

**Dependencies**: T007 must complete before T008 (models imported by database for table creation)

---

### Authentication Layer

- [X] T009 [Foundation] Create auth.py in backend/ with JWT verification:
  - Import: `from fastapi import Header, HTTPException; from jose import JWTError, jwt; from database import settings`
  - Define get_current_user(authorization: str = Header(...)) -> str function
  - Extract token by removing "Bearer " prefix from authorization header
  - Decode JWT with: `jwt.decode(token, settings.better_auth_secret, algorithms=["HS256"])`
  - Extract user_id from payload.get("userId") (note: camelCase from Better Auth)
  - Raise HTTPException(status_code=401, detail="Invalid authentication credentials") on JWTError or missing userId
  - Return user_id string

**Acceptance**: JWT verification dependency extracts user_id from token, returns 401 on invalid token

**Dependencies**: T008 must complete before T009 (settings required for secret key)

---

### FastAPI Application

- [X] T010 [Foundation] Create main.py in backend/ with FastAPI app:
  - Import: `from fastapi import FastAPI; from fastapi.middleware.cors import CORSMiddleware; from sqlmodel import SQLModel`
  - Import: `from database import engine, settings`
  - Create app = FastAPI(title="Todo Backend API", version="1.0.0")
  - Add CORSMiddleware with: allow_origins=settings.allowed_origins.split(","), allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
  - Define @app.on_event("startup") function calling SQLModel.metadata.create_all(engine)
  - Define @app.get("/api/health") function returning {"status": "healthy"}

**Acceptance**: FastAPI app with CORS, startup event for table creation, health check endpoint

**Dependencies**: T008 must complete before T010 (engine and settings required)

**Checkpoint**: Foundation ready - FastAPI app runnable with `uvicorn main:app --reload`, health check accessible at http://localhost:8000/api/health

---

## Phase 1: User Story 1 - Task Listing (Priority: P1) 🎯 MVP

**Goal**: Users can retrieve all their tasks (foundation for UI display)

**Independent Test**: Authenticate, call GET /api/tasks, verify empty array returned initially

### Implementation for User Story 1 - Task Listing

- [X] T011 [US1] Create routes/tasks.py in backend/routes/ with router and list endpoint:
  - Import: `from fastapi import APIRouter, Depends, HTTPException, status; from sqlmodel import Session, select; from typing import List`
  - Import: `from models import Task; from database import get_session; from auth import get_current_user`
  - Create router = APIRouter(prefix="/api/tasks", tags=["tasks"])
  - Define @router.get("/", response_model=List[Task]) function
  - Parameters: user_id: str = Depends(get_current_user), session: Session = Depends(get_session)
  - Query: statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
  - Execute: tasks = session.exec(statement).all()
  - Return: tasks (list of Task objects)

**Acceptance**: GET /api/tasks returns empty array initially, requires authentication

**Dependencies**: T007 (models), T008 (database), T009 (auth) must complete before T011

- [X] T012 [US1] Update main.py to include tasks router:
  - Import: `from routes import tasks`
  - Add line: `app.include_router(tasks.router)`

**Acceptance**: Tasks router registered, GET /api/tasks accessible via FastAPI app

**Dependencies**: T010 (main.py), T011 (tasks router) must complete before T012

**Checkpoint**: GET /api/tasks works, returns empty array with valid JWT, returns 401 without JWT

---

## Phase 2: User Story 2 - Task Creation (Priority: P1) 🎯 MVP

**Goal**: Users can create new tasks (essential write operation)

**Independent Test**: Authenticate, POST /api/tasks with title, verify task created with ID and timestamps

### Pydantic Schemas

- [X] T013 [US2] Add Pydantic schemas to models.py for request/response:
  - Import: `from pydantic import BaseModel`
  - Define class TaskCreate(BaseModel) with fields: title (str, min_length=1, max_length=200), description (Optional[str], max_length=1000, default=None)
  - Define class TaskUpdate(BaseModel) with fields: title (Optional[str], min_length=1, max_length=200, default=None), description (Optional[str], max_length=1000, default=None)
  - Add Config class to both with json_schema_extra examples

**Acceptance**: Request validation schemas defined for create and update operations

**Dependencies**: T007 (models.py exists) must complete before T013

### Implementation for User Story 2 - Task Creation

- [X] T014 [US2] Add create endpoint to routes/tasks.py:
  - Import: `from models import TaskCreate; from datetime import datetime`
  - Define @router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED) function
  - Parameters: task_data: TaskCreate, user_id: str = Depends(get_current_user), session: Session = Depends(get_session)
  - Create: new_task = Task(user_id=user_id, title=task_data.title, description=task_data.description)
  - Add to session: session.add(new_task), session.commit(), session.refresh(new_task)
  - Return: new_task

**Acceptance**: POST /api/tasks creates task with auto-generated ID, timestamps, user_id from JWT, completed=false

**Dependencies**: T011 (router exists), T013 (TaskCreate schema) must complete before T014

**Checkpoint**: MVP functional - users can create and list tasks, authentication enforced

---

## Phase 3: User Story 3 - Task Retrieval by ID (Priority: P2)

**Goal**: Users can view individual task details

**Independent Test**: Create task, then GET /api/tasks/{id}, verify task returned with ownership check

### Implementation for User Story 3 - Task Retrieval by ID

- [X] T015 [US3] Add get-by-id endpoint to routes/tasks.py:
  - Define @router.get("/{task_id}", response_model=Task) function
  - Parameters: task_id: int, user_id: str = Depends(get_current_user), session: Session = Depends(get_session)
  - Query: task = session.get(Task, task_id)
  - Ownership check: if not task or task.user_id != user_id: raise HTTPException(status_code=404, detail="Task not found")
  - Return: task

**Acceptance**: GET /api/tasks/{id} returns task if owned by user, 404 if not found or wrong owner, 401 without auth

**Dependencies**: T011 (router exists) must complete before T015

**Checkpoint**: Task detail retrieval functional with ownership enforcement

---

## Phase 4: User Story 4 - Task Update (Priority: P2)

**Goal**: Users can edit task title and description

**Independent Test**: Create task, PUT /api/tasks/{id} with updated data, verify changes persisted

### Implementation for User Story 4 - Task Update

- [X] T016 [US4] Add update endpoint to routes/tasks.py:
  - Import: `from models import TaskUpdate`
  - Define @router.put("/{task_id}", response_model=Task) function
  - Parameters: task_id: int, task_data: TaskUpdate, user_id: str = Depends(get_current_user), session: Session = Depends(get_session)
  - Query: task = session.get(Task, task_id)
  - Ownership check: if not task or task.user_id != user_id: raise HTTPException(status_code=404, detail="Task not found")
  - Update fields: if task_data.title is not None: task.title = task_data.title
  - Update fields: if task_data.description is not None: task.description = task_data.description
  - Update timestamp: task.updated_at = datetime.utcnow()
  - Commit: session.add(task), session.commit(), session.refresh(task)
  - Return: task

**Acceptance**: PUT /api/tasks/{id} updates provided fields, updates timestamp, enforces ownership, validates input (422 on error)

**Dependencies**: T011 (router exists), T013 (TaskUpdate schema) must complete before T016

**Checkpoint**: Task editing functional

---

## Phase 5: User Story 5 - Task Completion Toggle (Priority: P2)

**Goal**: Users can mark tasks complete or incomplete

**Independent Test**: Create task (completed=false), PATCH /api/tasks/{id}/complete, verify completed=true and timestamp updated

### Implementation for User Story 5 - Task Completion Toggle

- [X] T017 [US5] Add complete-toggle endpoint to routes/tasks.py:
  - Define @router.patch("/{task_id}/complete", response_model=Task) function
  - Parameters: task_id: int, user_id: str = Depends(get_current_user), session: Session = Depends(get_session)
  - Query: task = session.get(Task, task_id)
  - Ownership check: if not task or task.user_id != user_id: raise HTTPException(status_code=404, detail="Task not found")
  - Toggle: task.completed = not task.completed
  - Update timestamp: task.updated_at = datetime.utcnow()
  - Commit: session.add(task), session.commit(), session.refresh(task)
  - Return: task

**Acceptance**: PATCH /api/tasks/{id}/complete toggles completed status, updates timestamp, enforces ownership

**Dependencies**: T011 (router exists) must complete before T017

**Checkpoint**: Task completion toggle functional

---

## Phase 6: User Story 6 - Task Deletion (Priority: P3)

**Goal**: Users can delete tasks they no longer need

**Independent Test**: Create task, DELETE /api/tasks/{id}, verify 204 returned and task no longer exists

### Implementation for User Story 6 - Task Deletion

- [X] T018 [US6] Add delete endpoint to routes/tasks.py:
  - Define @router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT) function
  - Parameters: task_id: int, user_id: str = Depends(get_current_user), session: Session = Depends(get_session)
  - Query: task = session.get(Task, task_id)
  - Ownership check: if not task or task.user_id != user_id: raise HTTPException(status_code=404, detail="Task not found")
  - Delete: session.delete(task), session.commit()
  - Return: None (FastAPI returns 204 No Content automatically)

**Acceptance**: DELETE /api/tasks/{id} removes task permanently, returns 204 on success, 404 if not found/wrong owner

**Dependencies**: T011 (router exists) must complete before T018

**Checkpoint**: All CRUD operations complete

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Production-ready documentation, error handling, and final validation

### Documentation

- [X] T019 [P] [Polish] Create README.md in backend/ with setup instructions:
  - Prerequisites section (Python 3.13+, Neon account)
  - Quick Start section referencing specs/001-todo-backend-api/quickstart.md
  - Running the Server section (uvicorn command)
  - Testing section (curl examples or Swagger UI link)
  - Environment Variables section (reference .env.example)
  - Project Structure section (list of files and their purpose)

**Acceptance**: README.md provides clear setup and usage instructions

- [X] T020 [P] [Polish] Add docstrings to all functions in models.py, database.py, auth.py:
  - Add module-level docstring describing purpose
  - Add function/class docstrings with parameters and return values
  - Use Google-style or NumPy-style docstring format

**Acceptance**: All public functions and classes have descriptive docstrings

**Dependencies**: T007, T008, T009 must complete before T020 (files exist)

---

### Error Handling Improvements

- [ ] T021 [Polish] Add database connection error handling to database.py:
  - Wrap engine creation in try/except for OperationalError
  - Add helpful error message if DATABASE_URL is invalid or connection fails
  - Log error details (without exposing credentials)

**Acceptance**: Clear error message if database connection fails at startup

**Dependencies**: T008 must complete before T021 (database.py exists)

- [ ] T022 [Polish] Add validation for environment variables in database.py Settings:
  - Add validators to ensure DATABASE_URL starts with "postgresql://"
  - Add validator to ensure BETTER_AUTH_SECRET is at least 32 characters
  - Add validator to ensure ALLOWED_ORIGINS is not empty

**Acceptance**: Application fails fast at startup with clear error if environment variables invalid

**Dependencies**: T008 must complete before T022 (Settings class exists)

---

### Testing and Validation

- [ ] T023 [Polish] Manual testing checklist - Test all endpoints with curl or Postman:
  - Generate test JWT token (Python REPL: jose.jwt.encode with test user_id)
  - Test GET /api/health (expect 200, no auth required)
  - Test GET /api/tasks with valid token (expect 200, empty array initially)
  - Test GET /api/tasks without token (expect 401)
  - Test POST /api/tasks with valid data (expect 201, task returned with ID)
  - Test POST /api/tasks without title (expect 422, validation error)
  - Test GET /api/tasks again (expect 200, array with created task)
  - Test GET /api/tasks/{id} with valid ID (expect 200, task returned)
  - Test GET /api/tasks/{id} with non-existent ID (expect 404)
  - Test PUT /api/tasks/{id} with updated data (expect 200, changes reflected)
  - Test PATCH /api/tasks/{id}/complete (expect 200, completed toggled)
  - Test DELETE /api/tasks/{id} (expect 204, no content)
  - Test GET /api/tasks/{id} for deleted task (expect 404)

**Acceptance**: All endpoints return correct status codes and responses per specification

**Dependencies**: T012, T014, T015, T016, T017, T018 must complete before T023 (all endpoints implemented)

- [ ] T024 [Polish] Security audit - Verify data isolation and security requirements:
  - Code review: Every query in routes/tasks.py filters by user_id or checks ownership
  - Verify: HTTPException returns 404 (not 403) for unauthorized access (prevents enumeration)
  - Verify: No raw SQL queries (only SQLModel operations)
  - Verify: .env in .gitignore (secrets not committed)
  - Verify: JWT verification happens on all task endpoints (not health check)
  - Test with two different user_ids: User A cannot access User B's tasks

**Acceptance**: All security requirements from constitution and spec verified

**Dependencies**: T011, T014, T015, T016, T017, T018 must complete before T024 (all endpoints implemented)

- [ ] T025 [Polish] Verify OpenAPI documentation at http://localhost:8000/docs:
  - Check all 7 endpoints listed (6 task + 1 health)
  - Verify request/response schemas shown correctly
  - Verify authorization header documented
  - Test "Try it out" functionality with JWT token

**Acceptance**: Swagger UI provides complete, accurate API documentation

**Dependencies**: T012 must complete before T025 (app with all routes running)

---

### Final Validation

- [ ] T026 [Polish] Run through quickstart.md validation checklist:
  - Verify all setup steps work as documented
  - Verify .env.example matches actual required variables
  - Verify requirements.txt installs without errors
  - Verify server starts with: uvicorn main:app --reload --host 0.0.0.0 --port 8000
  - Verify health check accessible: curl http://localhost:8000/api/health

**Acceptance**: quickstart.md steps execute successfully from clean environment

**Dependencies**: All implementation tasks (T001-T018) and documentation (T019) must complete before T026

---

## Dependencies & Execution Order

### Phase Dependencies

- **Foundation (Phase 0)**: No dependencies - MUST complete first before ANY user story
- **User Story 1 (Phase 1)**: Depends on Foundation completion - MVP milestone
- **User Story 2 (Phase 2)**: Depends on Foundation completion - MVP milestone (can parallelize with US1 route implementation)
- **User Story 3 (Phase 3)**: Depends on Foundation completion - can start after Foundation
- **User Story 4 (Phase 4)**: Depends on Foundation completion - can start after Foundation
- **User Story 5 (Phase 5)**: Depends on Foundation completion - can start after Foundation
- **User Story 6 (Phase 6)**: Depends on Foundation completion - can start after Foundation
- **Polish (Phase 7)**: Depends on all user story implementations complete

### Critical Path

```
T001-T006 (Setup)
    ↓
T007 (models.py)
    ↓
T008 (database.py)
    ↓
T009 (auth.py)
    ↓
T010 (main.py with health check)
    ↓
[Foundation Complete - Checkpoint]
    ↓
T011 (tasks router + list endpoint)
    ↓
T012 (register router)
    ↓
[MVP Phase 1 Complete - Can list tasks]
    ↓
T013 (Pydantic schemas)
    ↓
T014 (create endpoint)
    ↓
[MVP Phase 2 Complete - Can create and list tasks]
    ↓
T015, T016, T017, T018 (remaining endpoints - can parallelize)
    ↓
[All CRUD Complete - Checkpoint]
    ↓
T019-T026 (Polish, documentation, validation)
    ↓
[Feature Complete]
```

### Parallel Opportunities

**Foundation Phase**:
- T001, T002, T003 (directory setup) can run in parallel
- T004, T005, T006 (config files) can run in parallel after directory setup
- T007 (models) independent of config files (can parallelize with T004-T006)

**User Story Phases**:
- After Foundation complete, routes for US3, US4, US5, US6 can implement in parallel (all modify same file routes/tasks.py - coordinate to avoid conflicts)
- T013 (schemas) can run in parallel with T011 (list endpoint) since they modify different parts of code

**Polish Phase**:
- T019, T020 (documentation) can run in parallel
- T021, T022 (error handling) can run in parallel
- T023, T024, T025 (testing) must run after all implementations complete

---

## Implementation Strategy

### MVP First (Foundation + User Stories 1 & 2)

1. Complete Phase 0: Foundation (T001-T010)
   - **Checkpoint**: Server starts, health check works
2. Complete Phase 1: Task Listing (T011-T012)
   - **Checkpoint**: GET /api/tasks returns empty array with auth
3. Complete Phase 2: Task Creation (T013-T014)
   - **Checkpoint**: POST /api/tasks creates tasks, GET returns created tasks
4. **STOP and VALIDATE**: Test MVP with curl/Postman
5. MVP deployed if validated

### Full Implementation

1. Foundation (T001-T010) → Foundation ready
2. MVP (T011-T014) → Test independently → MVP ready
3. Remaining endpoints (T015-T018) → Can implement in any order
4. Polish (T019-T026) → Production ready

### Team Parallelization

With multiple developers:
1. Developer A: Foundation (T001-T010)
2. Once Foundation done:
   - Developer A: US1 & US2 (T011-T014) - MVP
   - Developer B: US3 (T015)
   - Developer C: US4 & US5 (T016-T017)
   - Developer D: US6 (T018)
3. All developers: Polish tasks (T019-T026) - can divide

**Coordination**: All route implementations modify routes/tasks.py - use git branches or coordinate timing to avoid merge conflicts.

---

## Notes

- [P] tasks = different files or independent code sections, safe to parallelize
- Routes tasks (T011, T014, T015, T016, T017, T018) all modify routes/tasks.py - coordinate to avoid conflicts
- Foundation phase (T001-T010) is CRITICAL PATH - blocks all user stories
- MVP achieved after T014 (list + create tasks working)
- All task endpoints require auth dependency - automatically enforced by Depends(get_current_user)
- Commit after each completed task or logical group (e.g., after each endpoint)
- Verify tests pass at checkpoints before proceeding to next phase

---

## Acceptance Criteria (Final Validation)

Before marking feature complete, verify (aligned with spec.md):

**Functional Requirements**:
- [ ] All 6 task endpoints implemented and returning correct status codes
- [ ] Health check endpoint works without authentication
- [ ] JWT authentication enforced on all task endpoints
- [ ] User data isolation verified (users see only their own tasks)
- [ ] Input validation working (title 1-200 chars, description max 1000 chars)
- [ ] Timestamps auto-generated and auto-updated correctly

**API Contracts**:
- [ ] GET /api/tasks returns 200 with array
- [ ] POST /api/tasks returns 201 with created task
- [ ] GET /api/tasks/{id} returns 200 or 404
- [ ] PUT /api/tasks/{id} returns 200 or 404/422
- [ ] PATCH /api/tasks/{id}/complete returns 200 or 404
- [ ] DELETE /api/tasks/{id} returns 204 or 404
- [ ] All error responses include detail field
- [ ] Validation errors return 422 with field details

**Security**:
- [ ] No hardcoded secrets (all in .env)
- [ ] .env file in .gitignore
- [ ] JWT verification on every task request
- [ ] Ownership check on all task operations
- [ ] Database queries use SQLModel (no raw SQL)
- [ ] CORS configured correctly

**Code Quality**:
- [ ] Type hints on all functions
- [ ] Docstrings on public APIs
- [ ] README.md with setup instructions
- [ ] Code follows FastAPI best practices

**Constitution Compliance**:
- [ ] API-first design (all endpoints under /api/)
- [ ] Multi-user support (JWT auth, user_id filtering)
- [ ] Security by default (environment variables, validation, CORS)
- [ ] Persistent storage (Neon PostgreSQL, SQLModel ORM)
- [ ] Production-ready (deployable, health check)

---

## Summary

**Total Tasks**: 26 tasks (10 foundation + 8 implementation + 8 polish)

**Critical Path**: Foundation (T001-T010) → MVP routes (T011-T014) → Remaining routes (T015-T018) → Polish (T019-T026)

**MVP Milestone**: After T014 (users can create and list tasks)

**Estimated Effort**:
- Foundation: ~2-3 hours (first-time setup)
- MVP endpoints: ~1-2 hours (list + create)
- Remaining endpoints: ~2-3 hours (4 endpoints)
- Polish: ~1-2 hours (docs, testing, validation)
- **Total**: ~6-10 hours for experienced Python/FastAPI developer

**Parallel Opportunities**: Config files (T004-T006), documentation (T019-T020), endpoint implementations after foundation (coordinate on routes/tasks.py)

**Testing Strategy**: Manual testing with curl/Postman throughout (T023), security audit (T024), OpenAPI validation (T025)

**Next Step**: Begin implementation with T001 (create directory structure)
