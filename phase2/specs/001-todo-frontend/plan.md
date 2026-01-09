# Implementation Plan: Todo Frontend Web Application

**Branch**: `001-todo-frontend` | **Date**: 2026-01-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-frontend/spec.md`

## Summary

Build a modern Next.js web application that provides a beautiful, responsive user interface for managing todo tasks. The frontend consumes the existing backend API (Phase 1) to enable user authentication, task CRUD operations, and theme customization. Key features include Better Auth integration with JWT tokens, optimistic UI updates, comprehensive error handling, dark mode support, and mobile-first responsive design using Shadcn/ui components.

## Technical Context

**Language/Version**: TypeScript 5.x with Next.js 16+ (App Router)
**Primary Dependencies**: Next.js, React 19+, Better Auth (JWT plugin), Shadcn/ui, Tailwind CSS, next-themes
**Storage**: Browser localStorage (theme preference), HTTP-only cookies (session tokens)
**Testing**: React Testing Library, Playwright (E2E), Jest
**Target Platform**: Modern web browsers (last 2 versions of Chrome, Firefox, Safari, Edge)
**Project Type**: Web frontend (single-page application with Next.js App Router)
**Performance Goals**:
- Initial page load < 2 seconds
- Task operations complete < 3 seconds
- UI updates (theme toggle, optimistic updates) < 300ms
- Support up to 1000 tasks without performance degradation

**Constraints**:
- Must integrate with existing backend at http://localhost:8000
- Better Auth with JWT tokens (BETTER_AUTH_SECRET: 63734b1ce73e64801b32de3f9dd0d807)
- Session expiration fixed at 7 days
- Cannot modify backend API contracts
- Must handle error codes: 401 (unauthorized), 404 (not found), 422 (validation)

**Scale/Scope**:
- ~15-20 React components
- 4 main routes (/, /login, /signup, /dashboard)
- 8 Shadcn/ui components to install and configure
- ~5-7 API client functions
- Responsive design supporting 320px - 2560px viewports

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Full-Stack Architecture ✅ PASS

**Check**: Frontend is clearly separated from backend; consumes API exclusively via HTTP

**Status**: PASS - This is a pure frontend application that communicates with the existing Phase 1 backend API at http://localhost:8000. No HTML rendering on backend. All communication through documented API contracts.

**Evidence**:
- Frontend lives in `frontend/` directory structure
- All data operations via centralized API client (`lib/api.ts`)
- Backend endpoints under `/api/` namespace
- Clear separation of concerns

### Principle II: API-First Design ✅ PASS

**Check**: Frontend consumes RESTful API through centralized client; no direct database access

**Status**: PASS - All backend communication flows through `lib/api.ts` with documented contracts. Frontend has zero database access.

**Evidence**:
- Centralized API client in `lib/api.ts`
- RESTful endpoints: GET/POST/PUT/PATCH/DELETE `/api/tasks`
- JSON request/response format
- Authorization Bearer tokens in headers
- No database dependencies in frontend

### Principle III: Multi-User Support ✅ PASS

**Check**: Application supports multiple users with authentication and data isolation

**Status**: PASS - Better Auth handles user authentication, JWT tokens enforce identity, backend enforces data isolation by user_id.

**Evidence**:
- Better Auth with JWT plugin for authentication
- User signup/login flows
- Protected routes via middleware
- JWT token sent in Authorization header
- Backend enforces user_id filtering (not frontend responsibility)

### Principle IV: Persistent Storage ✅ PASS

**Check**: Application data persists in backend database; frontend uses localStorage only for preferences

**Status**: PASS - All task data persists in backend PostgreSQL via API. Frontend only stores theme preference and session cookies locally.

**Evidence**:
- Task data persisted via backend API calls
- PostgreSQL database managed by backend (Phase 1)
- Frontend localStorage limited to theme preference
- Session tokens in HTTP-only cookies

### Principle V: Security by Default ✅ PASS

**Check**: JWT authentication enforced; input validation; secrets in environment variables

**Status**: PASS - JWT tokens required for all protected routes. Better Auth handles secure session management. Input validation mirrors backend rules. Secrets in `.env.local`.

**Evidence**:
- Better Auth JWT plugin configured
- Middleware protects `/dashboard` route
- Authorization header on all API requests
- Client-side validation (title 1-200 chars, description max 1000 chars)
- BETTER_AUTH_SECRET in environment variable
- API URL in NEXT_PUBLIC_API_URL

### Principle VI: Production-Ready Deployment ✅ PASS

**Check**: Frontend independently deployable; environment-based configuration; CORS handled

**Status**: PASS - Next.js app deployable to Vercel/Netlify/any hosting. Environment variables for configuration. CORS handled by backend.

**Evidence**:
- Standard Next.js project structure
- Environment variables for API URL and auth secret
- Static/SSR build options available
- Independent of backend deployment

### Principle VII: Spec-Driven Development Only ✅ PASS

**Check**: Feature has specification; plan created before tasks; PHR to be created

**Status**: PASS - Following SDD workflow: spec.md → plan.md → tasks.md. PHR will be created upon plan completion.

**Evidence**:
- spec.md exists with complete requirements
- This plan.md generated via `/sp.plan`
- tasks.md to follow via `/sp.tasks`
- PHR creation planned

**GATE RESULT**: ✅ ALL CHECKS PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-frontend/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (technology decisions)
├── data-model.md        # Phase 1 output (frontend state model)
├── quickstart.md        # Phase 1 output (setup instructions)
├── contracts/           # Phase 1 output (API contracts)
│   └── api-contracts.md # RESTful API contract documentation
├── checklists/
│   └── requirements.md  # Quality validation checklist
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── app/
│   ├── layout.tsx                 # Root layout with ThemeProvider, Navbar
│   ├── page.tsx                   # Home page (auth-based redirect)
│   ├── globals.css                # Tailwind base styles, CSS variables
│   ├── dashboard/
│   │   └── page.tsx               # Protected dashboard with TaskList
│   ├── login/
│   │   └── page.tsx               # Login form page
│   └── signup/
│       └── page.tsx               # Signup form page
├── components/
│   ├── ui/                        # Shadcn components (auto-generated)
│   │   ├── button.tsx
│   │   ├── input.tsx
│   │   ├── textarea.tsx
│   │   ├── dialog.tsx
│   │   ├── card.tsx
│   │   ├── checkbox.tsx
│   │   ├── form.tsx
│   │   ├── toast.tsx
│   │   └── switch.tsx
│   ├── tasks/
│   │   ├── TaskList.tsx           # Server component fetching tasks
│   │   ├── TaskItem.tsx           # Client component for single task
│   │   ├── CreateTaskDialog.tsx   # Client component for create dialog
│   │   ├── EditTaskDialog.tsx     # Client component for edit dialog
│   │   └── DeleteConfirmDialog.tsx # Client component for delete confirm
│   ├── Navbar.tsx                 # Navigation with logout, theme toggle
│   └── ThemeToggle.tsx            # Client component for theme switch
├── lib/
│   ├── api.ts                     # Centralized API client with auth
│   ├── auth.ts                    # Better Auth configuration
│   ├── utils.ts                   # Utility functions (cn, etc.)
│   └── types.ts                   # TypeScript types for API models
├── providers/
│   └── ThemeProvider.tsx          # next-themes provider wrapper
├── middleware.ts                  # Route protection (auth check)
├── .env.local                     # Environment variables (gitignored)
├── .env.example                   # Example env file (committed)
├── next.config.ts                 # Next.js configuration
├── tailwind.config.ts             # Tailwind configuration with dark mode
├── components.json                # Shadcn CLI configuration
├── package.json                   # Dependencies and scripts
├── tsconfig.json                  # TypeScript configuration (strict mode)
└── README.md                      # Project documentation
```

**Structure Decision**: Web application structure (Option 2 from template). This is a pure frontend project consuming an existing backend API. The `frontend/` directory contains all Next.js application code. Backend code exists in separate `backend/` directory from Phase 1 and is not modified in this phase.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All constitution principles are satisfied.

---

## Phase 0: Research & Technology Decisions

### Research Questions

Based on the technical context and constitution requirements, the following areas require research to ensure best practices:

1. **Better Auth + Next.js 16 App Router Integration**
   - How to configure Better Auth with JWT plugin in App Router
   - Session cookie storage and retrieval patterns
   - Server vs. client component considerations for auth state

2. **API Client Architecture**
   - Best practices for centralized fetch wrapper with auth headers
   - Error handling and retry logic
   - Type-safe request/response patterns

3. **Optimistic UI Updates**
   - React patterns for optimistic updates with rollback
   - State management for task completion toggle
   - Error recovery UX patterns

4. **Shadcn/ui + Next.js App Router**
   - Shadcn component installation and configuration
   - Server vs. client component usage with Shadcn
   - Form validation with React Hook Form (if needed)

5. **Dark Mode Implementation**
   - next-themes integration with App Router
   - CSS variable strategy for theme switching
   - Preventing flash of unstyled content (FOUC)

6. **Middleware for Route Protection**
   - Next.js 16 middleware patterns for auth checking
   - JWT token verification in middleware
   - Redirect logic for protected routes

7. **Responsive Design Patterns**
   - Mobile-first Tailwind breakpoint strategy
   - Dialog/modal responsive behavior
   - Touch-friendly UI for mobile devices

### Research Outputs

The research phase will produce `research.md` documenting:

- **Decision**: Chosen approach for each question
- **Rationale**: Why this approach was selected
- **Alternatives Considered**: Other options evaluated
- **Implementation Notes**: Key patterns and gotchas
- **Code Examples**: Reference implementations

---

## Phase 1: Design & Contracts

### Data Model (Frontend State)

The frontend manages the following state models (see `data-model.md`):

**User**
- id: string (from JWT token)
- email: string
- name: string | null

**Task**
- id: number
- user_id: string (not displayed, for API correlation)
- title: string (1-200 chars)
- description: string | null (max 1000 chars)
- completed: boolean
- created_at: string (ISO 8601)
- updated_at: string (ISO 8601)

**Session** (managed by Better Auth)
- token: string (JWT in HTTP-only cookie)
- expiresAt: Date (7 days from creation)

**Theme Preference** (localStorage)
- theme: "light" | "dark" | "system"

### API Contracts

The frontend consumes the following backend API endpoints (see `contracts/api-contracts.md`):

**Authentication**
- POST `/api/auth/signup` - Create new user account
- POST `/api/auth/login` - Authenticate and receive JWT
- POST `/api/auth/logout` - Invalidate session

**Tasks**
- GET `/api/tasks` - Fetch all tasks for authenticated user
- POST `/api/tasks` - Create new task
- GET `/api/tasks/{id}` - Fetch single task (optional, may use list)
- PUT `/api/tasks/{id}` - Update task
- PATCH `/api/tasks/{id}/complete` - Toggle completion status
- DELETE `/api/tasks/{id}` - Delete task

**Request/Response Formats** (JSON):
- Authorization header: `Bearer {JWT_TOKEN}`
- Error response: `{ detail: string }`
- Task response: Task object (see data model)
- Task list response: `Task[]`

### Quickstart Documentation

Phase 1 will generate `quickstart.md` with:

1. **Prerequisites**: Node.js 20+, npm/yarn/pnpm, backend running at localhost:8000
2. **Installation Steps**: Clone, install dependencies, configure environment
3. **Environment Variables**: NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET
4. **Development Server**: `npm run dev`
5. **Shadcn Component Installation**: Commands for all 8 components
6. **First Run**: Create account, login, add tasks
7. **Testing**: Run test suite, E2E tests
8. **Build for Production**: `npm run build`, deployment options

### Agent Context Update

After Phase 1, the agent context will be updated with:
- Next.js 16 App Router patterns
- Better Auth configuration details
- Shadcn/ui component usage
- API client patterns
- TypeScript strict mode conventions

---

## Phase 2: Task Breakdown

Phase 2 will be executed by the `/sp.tasks` command and will generate `tasks.md` with implementation tasks based on this plan and the data models/contracts created in Phase 1.

Expected task categories:
1. **Project Setup**: Initialize Next.js, TypeScript, Tailwind, Shadcn
2. **Authentication**: Better Auth config, login/signup pages, middleware
3. **API Client**: Centralized fetch wrapper, type definitions
4. **Task Components**: TaskList, TaskItem, dialogs (create/edit/delete)
5. **Dashboard**: Layout, protected route, task operations
6. **Theme System**: Dark mode provider, toggle component
7. **Testing**: Unit tests, integration tests, E2E tests
8. **Polish**: Error handling, loading states, animations, accessibility

---

## Implementation Phases

### Phase 0: Research ✅ (Next Step)
- **Goal**: Document all technology decisions and patterns
- **Output**: `research.md`
- **Duration**: Research complete before proceeding to Phase 1

### Phase 1: Design & Contracts ✅ (After Phase 0)
- **Goal**: Define frontend state model and API contracts
- **Outputs**: `data-model.md`, `contracts/api-contracts.md`, `quickstart.md`
- **Duration**: Design complete before generating tasks

### Phase 2: Task Generation ⏳ (After Phase 1)
- **Goal**: Generate detailed implementation tasks
- **Command**: `/sp.tasks`
- **Output**: `tasks.md`
- **Note**: This phase is NOT part of `/sp.plan` - it's a separate command

### Phase 3: Implementation ⏳ (After Phase 2)
- **Goal**: Execute tasks from tasks.md
- **Command**: `/sp.implement` (or manual task execution)
- **Output**: Working frontend application

---

## Architecture Decision Record (ADR) Recommendations

The following architectural decisions should be documented in ADRs:

1. **Better Auth with JWT for Frontend Authentication**
   - **Decision**: Use Better Auth library with JWT plugin for authentication
   - **Context**: Need secure, production-ready auth that integrates with existing backend
   - **Alternatives**: NextAuth.js, custom JWT handling, Auth0
   - **Rationale**: Better Auth provides JWT support, integrates with backend token verification, minimal configuration

2. **Optimistic UI Updates for Task Toggle**
   - **Decision**: Implement optimistic updates for completion toggle with rollback on error
   - **Context**: Users expect instant feedback when marking tasks complete
   - **Alternatives**: Wait for backend response, show loading spinner
   - **Rationale**: Better UX with instant feedback, graceful degradation on error

3. **Shadcn/ui for Component Library**
   - **Decision**: Use Shadcn/ui components instead of building custom or using MUI/Chakra
   - **Context**: Need consistent, accessible, customizable UI components
   - **Alternatives**: Material-UI, Chakra UI, Headless UI, custom components
   - **Rationale**: Shadcn provides copy-paste components (no package lock-in), Tailwind-based, full customization

4. **Next.js App Router (not Pages Router)**
   - **Decision**: Build with Next.js 16 App Router architecture
   - **Context**: Starting new project, need modern React patterns
   - **Alternatives**: Pages Router, Create React App, Vite
   - **Rationale**: App Router is the future of Next.js, better performance with Server Components, built-in layouts

5. **Centralized API Client Pattern**
   - **Decision**: All API calls go through `lib/api.ts` with automatic auth header injection
   - **Context**: Need consistent error handling, auth token management, type safety
   - **Alternatives**: Per-component fetch calls, React Query, SWR
   - **Rationale**: Single source of truth for API communication, easier to maintain, enforces auth pattern

**Note**: These ADRs should be created using `/sp.adr <title>` command when implementing the relevant features.

---

## Success Metrics

### Functional Completeness
- [ ] All 7 user stories from spec.md are implemented and tested
- [ ] All 30 functional requirements (FR-001 to FR-030) are satisfied
- [ ] All edge cases from spec.md are handled

### Performance Targets (from spec Success Criteria)
- [ ] SC-001: Account signup completes in < 1 minute
- [ ] SC-002: Login to dashboard in < 5 seconds
- [ ] SC-003: Task list displays in < 2 seconds
- [ ] SC-004: Create task and see in list in < 3 seconds
- [ ] SC-005: Task toggle feedback in < 100ms
- [ ] SC-008: Theme toggle in < 300ms
- [ ] SC-012: Initial page load in < 2 seconds

### Quality Metrics
- [ ] SC-006: 95% of form submissions succeed or show clear errors
- [ ] SC-007: Responsive on 320px - 2560px viewports
- [ ] SC-010: 90% task flow completion rate on first attempt
- [ ] SC-011: 85% error resolution without external help

### Code Quality
- [ ] TypeScript strict mode with zero errors
- [ ] All components follow Next.js App Router best practices
- [ ] Centralized API client handles all backend communication
- [ ] Dark mode works across all components
- [ ] Accessibility standards met (keyboard navigation, ARIA labels)

### Constitution Compliance
- [ ] Frontend completely separated from backend
- [ ] All data via RESTful API (no direct database access)
- [ ] Multi-user support with JWT authentication
- [ ] Security by default (auth required, input validation, secrets in env)
- [ ] Production-ready (deployable, configured via environment)
- [ ] Spec-driven (tasks reference requirements, ADRs for key decisions)

---

## Next Steps

1. **Immediately**: Generate `research.md` to document technology decisions (Phase 0)
2. **After Research**: Generate `data-model.md`, `contracts/api-contracts.md`, and `quickstart.md` (Phase 1)
3. **After Design**: Run `/sp.tasks` to generate detailed implementation tasks (Phase 2)
4. **After Tasks**: Begin implementation using `/sp.implement` or manual task execution (Phase 3)
5. **During Implementation**: Create ADRs for architectural decisions using `/sp.adr`
6. **Throughout**: Create PHRs for all interactions to maintain traceability

---

**Plan Status**: ✅ Complete - Ready for Phase 0 (Research)
**Constitution Compliance**: ✅ All gates passed
**Next Command**: Generate research.md (internal to this plan command)
