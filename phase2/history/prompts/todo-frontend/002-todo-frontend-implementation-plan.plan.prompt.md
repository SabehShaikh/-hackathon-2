---
id: 002
title: Todo Frontend Implementation Plan
stage: plan
date: 2026-01-09
surface: agent
model: claude-sonnet-4-5
feature: todo-frontend
branch: 001-todo-frontend
user: SabehShaikh
command: /sp.plan
labels: ["planning", "architecture", "frontend", "nextjs", "todo-app"]
links:
  spec: specs/001-todo-frontend/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-todo-frontend/plan.md
  - specs/001-todo-frontend/research.md
  - specs/001-todo-frontend/data-model.md
  - specs/001-todo-frontend/contracts/api-contracts.md
  - specs/001-todo-frontend/quickstart.md
  - history/prompts/todo-frontend/002-todo-frontend-implementation-plan.plan.prompt.md
tests:
  - Constitution Check validation (all gates passed)
  - Technology decision documentation
  - API contract specification
---

## Prompt

/sp.plan

Reflect on: Constitution and Specification

Architecture:
- Next.js 16+ App Router
- TypeScript for type safety
- Shadcn/ui component library
- Better Auth for authentication
- Dark mode with next-themes
- API client for backend communication

File Structure:
frontend/
├── app/
│   ├── layout.tsx          # Root layout with theme provider
│   ├── page.tsx            # Home/redirect page
│   ├── dashboard/
│   │   └── page.tsx        # Main task dashboard (protected)
│   ├── login/
│   │   └── page.tsx        # Login page
│   └── signup/
│       └── page.tsx        # Signup page
├── components/
│   ├── ui/                 # Shadcn components
│   ├── tasks/
│   │   ├── TaskList.tsx
│   │   ├── TaskItem.tsx
│   │   ├── CreateTaskDialog.tsx
│   │   ├── EditTaskDialog.tsx
│   │   └── DeleteConfirm.tsx
│   ├── Navbar.tsx
│   └── ThemeToggle.tsx
├── lib/
│   ├── api.ts              # API client with auth
│   ├── auth.ts             # Better Auth config
│   └── utils.ts            # Helpers
├── providers/
│   └── theme-provider.tsx  # Dark mode provider
├── middleware.ts           # Route protection
├── .env.local
├── tailwind.config.ts
├── components.json         # Shadcn config
└── package.json

Key Components:

1. Authentication (Better Auth + JWT)
   - Better Auth configuration
   - JWT token storage in cookies
   - API client includes token in headers
   - Middleware protects dashboard route

2. API Client (lib/api.ts)
   - Fetch wrapper with auth headers
   - Error handling (401, 404, 422)
   - TypeScript types for requests/responses
   - Base URL from environment variable

3. Shadcn Components to Install:
   - button, input, textarea, form
   - dialog, card, checkbox
   - toast (for notifications)
   - switch (for theme toggle)

4. Task Components:
   - TaskList: Server component fetching tasks
   - TaskItem: Display single task with actions
   - CreateTaskDialog: Form in dialog
   - EditTaskDialog: Pre-filled edit form
   - DeleteConfirm: Confirmation dialog

5. Theme System:
   - next-themes for dark mode
   - ThemeProvider wrapper
   - ThemeToggle component in navbar
   - Tailwind dark: classes

Implementation Order:
1. Project setup (Next.js, TypeScript, Tailwind)
2. Install Shadcn CLI and components
3. Setup Better Auth
4. Create API client
5. Build authentication pages
6. Create task components
7. Build dashboard page
8. Add middleware protection
9. Implement dark mode
10. Test and polish

Dependencies:
- next@16+
- react@19+
- typescript
- tailwindcss
- better-auth
- next-themes
- lucide-react (icons)
- sonner (toast notifications)
- Shadcn components

Environment Variables:
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=63734b1ce73e64801b32de3f9dd0d807

Ready for /sp.tasks breakdown.

## Response snapshot

Created comprehensive implementation plan for Todo Frontend Web Application with complete architecture, research, and contracts documentation.

**Artifacts Generated**:

1. **plan.md** - Master implementation plan with:
   - Technical context (Next.js 16, TypeScript, Better Auth, Shadcn/ui)
   - Constitution compliance validation (all 7 principles passed)
   - Complete project structure (documentation and source code)
   - Performance goals and constraints
   - Phase 0-2 execution strategy
   - ADR recommendations for key decisions

2. **research.md** - Technology decisions covering:
   - Better Auth + Next.js App Router integration (JWT authentication)
   - API client architecture (centralized fetch wrapper)
   - Optimistic UI updates (React state with rollback)
   - Shadcn/ui component strategy (copy-paste, Tailwind-based)
   - Dark mode implementation (next-themes, zero FOUC)
   - Middleware for route protection (edge runtime)
   - Responsive design patterns (mobile-first, touch-friendly)

3. **data-model.md** - Frontend state management:
   - Core models: User, Task, Session, ThemePreference
   - Request/Response models for API communication
   - State management strategy (server-first with client state)
   - Data flow diagrams (creation, toggle, session expiry)
   - TypeScript type definitions file structure

4. **contracts/api-contracts.md** - Complete API specification:
   - 9 RESTful endpoints (3 auth + 6 tasks)
   - Request/response formats with examples
   - Error handling strategy (401, 404, 422, 500)
   - CORS configuration requirements
   - Authentication headers (JWT Bearer tokens)
   - API client implementation patterns

5. **quickstart.md** - Developer setup guide:
   - Prerequisites and verification steps
   - 5-step quick start process
   - First-time setup walkthrough
   - Shadcn component installation
   - Troubleshooting common issues
   - Production deployment checklist

**Constitution Compliance**: ✅ All 7 principles validated
- Full-stack architecture with clear separation
- API-first design (RESTful, centralized client)
- Multi-user support (Better Auth + JWT)
- Persistent storage (backend PostgreSQL)
- Security by default (JWT auth, validation, env vars)
- Production-ready deployment (independent, configurable)
- Spec-driven development (following SDD workflow)

**Architecture Decisions**:
- Next.js 16 App Router (Server Components by default)
- TypeScript strict mode (type safety)
- Better Auth with JWT plugin (backend integration)
- Shadcn/ui components (Tailwind-based, accessible)
- Centralized API client in lib/api.ts
- Optimistic updates for task completion toggle
- next-themes for dark mode (persistent, system-aware)
- Middleware for route protection (edge runtime)
- Mobile-first responsive design (320px-2560px)

**Performance Targets**:
- Initial page load < 2 seconds
- Task operations complete < 3 seconds
- UI updates (theme toggle, optimistic) < 300ms
- Support up to 1000 tasks without degradation

**Key Technologies**:
- Frontend: Next.js 16+, React 19+, TypeScript 5.x
- Styling: Tailwind CSS, Shadcn/ui components
- Auth: Better Auth (JWT plugin), HTTP-only cookies
- State: Server Components + useState (minimal client state)
- Theme: next-themes (light/dark/system)
- Notifications: Sonner (toast)
- Icons: Lucide React

**Next Steps**: Run `/sp.tasks` to generate detailed implementation tasks based on this plan.

## Outcome

- ✅ Impact: Complete implementation plan with architecture, research, data models, API contracts, and quickstart guide generated for Todo Frontend
- 🧪 Tests: Constitution Check passed all 7 principles - frontend architecture complies with project standards
- 📁 Files: Created plan.md, research.md, data-model.md, api-contracts.md, quickstart.md
- 🔁 Next prompts: Run `/sp.tasks` to generate implementation tasks, create ADRs for key decisions using `/sp.adr`, begin implementation with `/sp.implement`
- 🧠 Reflection: Successfully designed a comprehensive Next.js frontend architecture that integrates with existing Phase 1 backend, prioritizes performance (optimistic updates, Server Components), security (JWT auth, middleware protection), and developer experience (Shadcn/ui, TypeScript, comprehensive docs)

## Evaluation notes (flywheel)

- Failure modes observed: Agent context update script unavailable (template missing) - skipped without blocking progress
- Graders run and results (PASS/FAIL): Constitution Check - PASS (all 7 principles validated and satisfied)
- Prompt variant (if applicable): Standard /sp.plan workflow with Phase 0 (research) and Phase 1 (design/contracts) completion
- Next experiment (smallest change to try): Consider TanStack Query for more complex data fetching patterns if optimistic updates become difficult to manage at scale
