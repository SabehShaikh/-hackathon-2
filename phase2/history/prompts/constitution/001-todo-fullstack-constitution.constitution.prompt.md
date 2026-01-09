---
id: 001
title: Todo Full-Stack Constitution
stage: constitution
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5
feature: none
branch: main
user: SabehShaikh
command: /sp.constitution
labels: ["constitution", "full-stack", "todo-app", "initial-ratification"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

/sp.constitution

Project: Todo Full-Stack Web Application - Phase 2

Core Principles:
- Full-stack architecture: Separate frontend and backend services
- API-first design: Backend exposes RESTful API, frontend consumes it
- Multi-user support: User authentication and data isolation
- Persistent storage: PostgreSQL database for all data
- Secure by default: JWT authentication, input validation, CORS
- Production-ready: Deployable services

Tech Stack:
Backend:
- Python 3.13+ with FastAPI
- SQLModel ORM
- Neon Serverless PostgreSQL
- JWT token verification
- Uvicorn ASGI server

Frontend:
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- Better Auth with JWT
- Server and Client Components

Architecture Constraints:
- Backend: Pure API server (no HTML)
- Frontend: Consumes backend API via HTTP
- Authentication: Better Auth (frontend) + JWT verification (backend)
- Database: Single source of truth in Neon PostgreSQL
- CORS: Backend allows frontend origin

Backend Standards:
- FastAPI best practices
- SQLModel for database operations
- Environment variables for secrets
- RESTful conventions
- Error handling with HTTPException
- All routes under /api/
- User ID extracted from JWT token

Frontend Standards:
- Next.js App Router
- TypeScript strict mode
- Server Components by default
- Centralized API client in lib/api.ts
- Better Auth for authentication
- Tailwind CSS utility classes
- Responsive design

Data Model:
Users (managed by Better Auth):
- id: string (UUID)
- email: string (unique)
- name: string
- created_at: timestamp

Tasks:
- id: integer (auto-increment)
- user_id: string (foreign key)
- title: string (1-200 chars, required)
- description: text (optional, max 1000 chars)
- completed: boolean (default false)
- created_at: timestamp
- updated_at: timestamp

API Endpoints:
- GET /api/tasks - List user's tasks
- POST /api/tasks - Create task
- GET /api/tasks/{id} - Get task
- PUT /api/tasks/{id} - Update task
- DELETE /api/tasks/{id} - Delete task
- PATCH /api/tasks/{id}/complete - Toggle completion

Security:
- All endpoints require valid JWT
- Users access only their own tasks
- Input validation on all endpoints
- SQL injection prevention
- CORS configured properly
- Secrets in environment variables

Success Criteria:
- All 5 CRUD operations work through UI
- User authentication (signup/login)
- Each user sees only their tasks
- Data persists in database
- RESTful API
- Responsive frontend
- Both services deployed
- Spec-driven development only

## Response snapshot

Constitution v1.0.0 successfully created with seven core principles:

1. Full-Stack Architecture - Clear separation of frontend (Next.js) and backend (FastAPI) services
2. API-First Design - RESTful API with documented contracts
3. Multi-User Support - Authentication and data isolation with JWT
4. Persistent Storage - Neon PostgreSQL as single source of truth
5. Security by Default - JWT authentication, input validation, CORS
6. Production-Ready Deployment - Independently deployable services
7. Spec-Driven Development Only - SDD workflow with PHRs and ADRs

Document includes:
- Technology stack (Python 3.13+/FastAPI backend, Next.js 16+/TypeScript frontend)
- Development standards (backend and frontend conventions)
- Code quality requirements (type safety, error handling, validation)
- Testing standards (unit, integration, e2e)
- API endpoint specifications (6 RESTful endpoints under /api/)
- Success criteria (functional, non-functional, deployment readiness)
- Governance (amendment process, compliance requirements)

Sync Impact Report confirms all templates aligned and no follow-up TODOs.

## Outcome

- ✅ Impact: Initial constitution ratified with comprehensive governance for full-stack Todo application
- 🧪 Tests: N/A (constitution document - no tests)
- 📁 Files: .specify/memory/constitution.md (created)
- 🔁 Next prompts: /sp.specify to create feature specification based on constitution
- 🧠 Reflection: Constitution establishes clear principles for API-first, multi-user, secure full-stack architecture with spec-driven workflow

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution template fully populated with user-provided details
- Graders run and results (PASS/FAIL): PASS - All placeholders replaced, governance section complete, version 1.0.0 established
- Prompt variant (if applicable): Standard /sp.constitution workflow
- Next experiment (smallest change to try): Proceed with feature specification (/sp.specify) to define first user story
