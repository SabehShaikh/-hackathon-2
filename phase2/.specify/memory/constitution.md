<!--
Sync Impact Report:
- Version change: TEMPLATE (1.0.0) → 1.0.0 (initial ratification)
- Modified principles: All principles populated from template
- Added sections: All sections fully defined
- Removed sections: None
- Templates requiring updates: ✅ All templates aligned (plan, spec, tasks)
- Follow-up TODOs: None
-->

# Todo Full-Stack Web Application Constitution

## Core Principles

### I. Full-Stack Architecture
Every feature is built with clear separation between frontend and backend services. Backend is a pure API server exposing RESTful endpoints under `/api/`. Frontend is a Next.js application that consumes the backend API via HTTP. No HTML rendering on backend. Services communicate exclusively through documented API contracts.

**Rationale**: Clear separation enables independent scaling, deployment, and technology evolution. API-first design ensures contract clarity and enables future client diversity.

### II. API-First Design
Backend exposes RESTful API with versioned endpoints. All data operations flow through documented API contracts. Frontend consumes API through centralized client (`lib/api.ts`). No direct database access from frontend.

**Requirements**:
- RESTful conventions (GET, POST, PUT, PATCH, DELETE)
- JSON request/response format
- Consistent error responses with HTTPException
- All routes namespaced under `/api/`
- OpenAPI/Swagger documentation

**Rationale**: API-first ensures frontend-backend decoupling, enables API versioning, and provides clear integration contracts.

### III. Multi-User Support
Application MUST support multiple users with authentication and data isolation. Each user accesses only their own tasks. User ID is extracted from JWT token and enforced at the backend layer.

**Requirements**:
- User authentication (Better Auth on frontend, JWT verification on backend)
- User ID extraction from JWT token
- Data filtering by user_id on all queries
- Foreign key relationships enforcing user ownership
- No shared task access between users

**Rationale**: Multi-user support is a core requirement for production applications and requires proper isolation to prevent data leakage.

### IV. Persistent Storage
PostgreSQL (Neon Serverless) is the single source of truth for all data. SQLModel ORM handles all database operations. No in-memory or file-based storage for production data.

**Data Model**:
- Users: managed by Better Auth (id, email, name, created_at)
- Tasks: user_id (FK), title (1-200 chars), description (max 1000 chars), completed (boolean), timestamps

**Requirements**:
- All database access through SQLModel
- Proper foreign key constraints
- Timestamps (created_at, updated_at) on all entities
- Environment variables for connection strings

**Rationale**: Single source of truth prevents data inconsistency. PostgreSQL provides ACID guarantees and relational integrity.

### V. Security by Default
All endpoints require valid JWT authentication. User data is isolated by user_id. Input validation on all API endpoints. SQL injection prevention through ORM. CORS configured to allow only frontend origin. Secrets stored in environment variables.

**Security Requirements**:
- JWT token verification on all API endpoints
- User ID extraction and enforcement
- Input validation (title 1-200 chars, description max 1000 chars)
- SQLModel parameterized queries (no raw SQL)
- CORS whitelist for frontend origin only
- `.env` files for secrets (never committed)
- HTTPS in production

**Rationale**: Security cannot be added later. Default-secure design prevents vulnerabilities from shipping to production.

### VI. Production-Ready Deployment
Both frontend and backend are independently deployable services. Services are configured via environment variables. Health checks and monitoring endpoints provided. Deployment automation through spec-driven development.

**Requirements**:
- Backend: FastAPI with Uvicorn ASGI server
- Frontend: Next.js with App Router
- Environment-based configuration
- Deployment readiness checklist in spec
- CORS and origins properly configured

**Rationale**: Production readiness from day one prevents architectural debt and ensures smooth deployment.

### VII. Spec-Driven Development Only
All development follows the Spec-Driven Development (SDD) workflow: Specify → Plan → Tasks → Implement. No code written without specification. Changes traced to requirements. PHR (Prompt History Record) created for all interactions. ADR (Architecture Decision Record) for significant architectural decisions.

**Requirements**:
- Feature spec created before planning
- Plan approved before tasks
- Tasks reference spec and plan
- PHRs created automatically
- ADRs for architectural decisions (auth strategy, database choice, deployment architecture)

**Rationale**: Spec-driven development ensures requirements traceability, reduces rework, and maintains architectural coherence.

## Technology Stack

### Backend
- Python 3.13+ with type hints
- FastAPI framework for API server
- SQLModel ORM for database operations
- Neon Serverless PostgreSQL for data persistence
- JWT token verification (integration with Better Auth)
- Uvicorn ASGI server for production deployment
- Pydantic models for request/response validation

### Frontend
- Next.js 16+ with App Router
- TypeScript with strict mode enabled
- Tailwind CSS for styling
- Better Auth for authentication with JWT tokens
- Server Components by default (Client Components only when needed)
- Centralized API client (`lib/api.ts`)
- Responsive design patterns

## Development Standards

### Backend Standards
- FastAPI best practices and conventions
- SQLModel for all database operations (no raw SQL)
- Environment variables for all secrets and configuration
- RESTful API conventions (proper HTTP verbs and status codes)
- Error handling with FastAPI HTTPException
- All routes namespaced under `/api/`
- User ID extraction from JWT token on every request
- Type hints on all functions and endpoints
- Docstrings on public APIs

### Frontend Standards
- Next.js App Router (not Pages Router)
- TypeScript strict mode enabled
- Server Components by default (use 'use client' only when required)
- Centralized API client in `lib/api.ts` with token injection
- Better Auth for authentication flow
- Tailwind CSS utility classes (no custom CSS unless justified)
- Responsive design (mobile-first approach)
- Client-side validation mirroring backend validation
- Error handling with user-friendly messages

### Code Quality
- Type safety: TypeScript strict mode, Python type hints
- Error handling: All errors caught and logged with user-friendly messages
- Input validation: Backend validates all inputs; frontend mirrors validation
- No hardcoded secrets or configuration (use environment variables)
- Smallest viable change: No refactoring unrelated code
- Comments only where logic is non-obvious
- Code references in specs and tasks (file:line format)

### Testing Standards
- Backend: Unit tests for business logic, integration tests for API endpoints
- Frontend: Component tests for UI, integration tests for user flows
- Test all CRUD operations end-to-end
- Test authentication and authorization flows
- Test data isolation between users
- Test error handling and edge cases

## API Endpoints

### Required Endpoints
All endpoints require Authorization header with Bearer token.

- `GET /api/tasks` - List all tasks for authenticated user
- `POST /api/tasks` - Create new task (body: {title, description?})
- `GET /api/tasks/{id}` - Get single task by ID (user ownership verified)
- `PUT /api/tasks/{id}` - Update task (body: {title?, description?, completed?})
- `DELETE /api/tasks/{id}` - Delete task (user ownership verified)
- `PATCH /api/tasks/{id}/complete` - Toggle task completion status

### API Conventions
- JSON request/response format
- ISO 8601 timestamps
- Consistent error response format: `{detail: string}`
- HTTP status codes: 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 404 Not Found, 500 Internal Server Error
- User ID extracted from JWT, never from request body or query params

## Success Criteria

### Functional Requirements
- All 5 CRUD operations work through UI (Create, Read, Update, Delete, Toggle Complete)
- User authentication flow complete (signup, login, logout)
- Each user sees only their own tasks
- Data persists in Neon PostgreSQL database
- RESTful API with proper HTTP verbs and status codes
- Responsive frontend (mobile and desktop)
- Both services independently deployable

### Non-Functional Requirements
- Security: JWT authentication enforced on all endpoints
- Performance: API response time < 500ms for typical operations
- Reliability: Proper error handling and user feedback
- Maintainability: Code follows all standards and is documented
- Compliance: Follows Spec-Driven Development workflow

### Deployment Readiness
- Environment variables documented
- Services configured for production deployment
- CORS properly configured
- Database migrations (if applicable) documented
- Health check endpoints available

## Governance

### Amendment Process
Constitution amendments follow semantic versioning:
- **MAJOR**: Backward-incompatible governance/principle removals or redefinitions
- **MINOR**: New principle/section added or materially expanded guidance
- **PATCH**: Clarifications, wording improvements, typo fixes

All amendments require:
1. ADR documenting rationale for change
2. Update of all dependent templates and docs
3. Version increment in constitution
4. Sync Impact Report prepended to constitution file

### Compliance Requirements
- All PRs/reviews must verify compliance with constitution principles
- Spec-driven workflow mandatory (no code without spec)
- PHRs created for all development interactions
- ADRs required for architecturally significant decisions
- Complexity must be justified against constitution principles

### Runtime Guidance
During development, the agent uses CLAUDE.md for runtime development guidance. Constitution remains the authoritative source for project principles and standards.

**Version**: 1.0.0 | **Ratified**: 2026-01-08 | **Last Amended**: 2026-01-08
