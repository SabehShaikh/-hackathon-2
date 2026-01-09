---
id: 002
title: Backend API Specification
stage: spec
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5
feature: 001-todo-backend-api
branch: main
user: SabehShaikh
command: /sp.specify
labels: ["spec", "backend", "api", "fastapi", "todo"]
links:
  spec: specs/001-todo-backend-api/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-todo-backend-api/spec.md
tests:
  - none
---

## Prompt

/sp.specify

Project: Todo App Backend API - Phase 2

Target: RESTful API for todo task management with authentication

Core Features (Backend Only):

1. Database Connection
   - Connect to Neon Serverless PostgreSQL
   - Use SQLModel for ORM
   - Connection string from DATABASE_URL environment variable
   - Auto-create tables on startup

2. Authentication Middleware
   - Verify JWT tokens from Authorization header
   - Extract user_id from token payload
   - Use shared BETTER_AUTH_SECRET for verification
   - Return 401 Unauthorized for missing/invalid tokens
   - Health check endpoint doesn't require auth

3. Task CRUD Operations (All require authentication)

   GET /api/tasks - List all tasks for authenticated user
   POST /api/tasks - Create new task (title required, description optional)
   GET /api/tasks/{id} - Get single task by ID
   PUT /api/tasks/{id} - Update task title and/or description
   DELETE /api/tasks/{id} - Delete task by ID
   PATCH /api/tasks/{id}/complete - Toggle completed status

4. CORS Configuration
   - Allow requests from frontend origin (localhost:3000 in dev)
   - Set in ALLOWED_ORIGINS environment variable

5. Error Handling
   - Validation errors: 422 Unprocessable Entity
   - Authentication errors: 401 Unauthorized
   - Not found: 404 Not Found
   - Server errors: 500 Internal Server Error

Database Schema:
- Tasks table: id, user_id (FK), title (1-200 chars), description (max 1000), completed (default false), timestamps
- Users table: managed by Better Auth (not by backend)

Tech Stack: FastAPI, SQLModel, Neon PostgreSQL, PyJWT, Uvicorn, python-dotenv

Environment Variables: DATABASE_URL, BETTER_AUTH_SECRET, ALLOWED_ORIGINS

Success Criteria:
- All 6 endpoints work correctly
- Authentication required and verified
- Users see only their own tasks
- Database operations use SQLModel
- CORS configured correctly
- No hardcoded secrets

Out of Scope: User registration/login, password hashing, session management, frontend UI, task priorities/tags/due dates, search/filter

## Response snapshot

Created comprehensive feature specification for Todo Backend API with 6 prioritized user stories:

**P1 (MVP):**
- User Story 1: Task Listing - GET /api/tasks (foundation for UI)
- User Story 2: Task Creation - POST /api/tasks (essential write operation)

**P2 (Important):**
- User Story 3: Task Retrieval by ID - GET /api/tasks/{id}
- User Story 4: Task Update - PUT /api/tasks/{id}
- User Story 5: Task Completion Toggle - PATCH /api/tasks/{id}/complete

**P3 (Nice to have):**
- User Story 6: Task Deletion - DELETE /api/tasks/{id}

Each user story includes:
- Clear priority justification
- Independent test description
- Detailed acceptance scenarios (Given/When/Then format)
- Edge cases and error handling

Specification includes:
- 18 functional requirements (FR-001 to FR-018)
- 10 success criteria with measurable outcomes
- Complete API contracts with request/response examples for all 6 endpoints
- 8 security requirements (SEC-001 to SEC-008)
- Data model with Tasks and Users tables (including indexes and constraints)
- Technology constraints and dependencies
- Project structure (backend/ with main.py, models.py, database.py, auth.py, routes/tasks.py)
- Environment variables template
- Acceptance criteria checklist (17 items)
- Explicit out-of-scope items

Specification follows constitution principles:
- API-first design (RESTful endpoints under /api/)
- Multi-user support (JWT authentication, user_id filtering)
- Security by default (environment variables, input validation, CORS)
- Persistent storage (Neon PostgreSQL, SQLModel ORM)
- Spec-driven development (detailed requirements before implementation)

## Outcome

- ✅ Impact: Complete backend API specification with 6 independently testable user stories ready for planning phase
- 🧪 Tests: Acceptance scenarios defined for all user stories (30+ test cases)
- 📁 Files: specs/001-todo-backend-api/spec.md (created)
- 🔁 Next prompts: /sp.plan to create implementation plan with technical design decisions
- 🧠 Reflection: Well-structured spec with clear priorities enables incremental delivery (MVP with P1 stories, then P2/P3)

## Evaluation notes (flywheel)

- Failure modes observed: None - user input was comprehensive with clear requirements
- Graders run and results (PASS/FAIL): PASS - All user stories independently testable, requirements measurable, API contracts complete
- Prompt variant (if applicable): Standard /sp.specify workflow
- Next experiment (smallest change to try): Proceed with /sp.plan to design implementation (database layer, auth middleware, endpoint handlers)
