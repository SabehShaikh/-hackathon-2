# Implementation Plan: Todo AI Chatbot with Natural Language Interface

**Branch**: `002-ai-chat-interface` | **Date**: 2026-01-15 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-ai-chat-interface/spec.md`

## Summary

Enable users to manage tasks through natural language conversation instead of UI buttons. Phase 3 adds conversational AI interface while reusing Phase 2 backend patterns. Core functionality includes 5 MCP tools (add, list, complete, delete, update tasks) integrated with Grok AI agent, stateless chat API, and OpenAI ChatKit frontend. All conversation history persists in database for multi-session continuity.

**Technical Approach**:
- Backend: FastAPI with Grok agent + Official MCP SDK tools
- Frontend: Phase 2 Next.js app + ChatKit as additional /chat route
- Database: Extend Phase 2 Neon PostgreSQL (add conversations, messages tables)
- Deployment: HuggingFace Spaces (backend), Vercel (frontend)
- Architecture: Stateless server, all state in database
- UI Strategy: **Dual interface** - traditional UI buttons (Phase 2) + conversational AI (Phase 3)

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript/Next.js 15+ (frontend)
**Primary Dependencies**:
- Backend: FastAPI 0.115+, SQLModel 0.0.22, OpenAI SDK 1.58+ (Grok-compatible), Official MCP SDK 1.0+, python-jose 3.3+ (JWT), psycopg2-binary 2.9+ (PostgreSQL)
- Frontend: Next.js 15+ (copied from Phase 2), @openai/chat-kit (chat UI), React 18+, shadcn/ui (existing Phase 2 components)

**Storage**: Neon PostgreSQL (shared with Phase 2, extend schema)
**Testing**: pytest (backend), Jest + React Testing Library (frontend)
**Target Platform**:
- Backend: HuggingFace Spaces (Docker, Python runtime, port 7860)
- Frontend: Vercel (static/serverless deployment)
- Database: Neon PostgreSQL cloud (existing Phase 2 instance)

**Project Type**: Web application (backend + frontend)
**Performance Goals**:
- Chat response < 3s p95 (includes AI inference)
- Database queries < 500ms p95
- Support 100 concurrent users
- Frontend initial load < 2s on broadband

**Constraints**:
- Phase 2 immutability: No modifications to ../phase2/
- Stateless architecture: Zero in-memory conversation state
- Grok API free tier: Must operate within rate limits
- OpenAI domain allowlist: Frontend URL must be allowlisted
- Database migration safety: Backward-compatible schema changes only

**Scale/Scope**:
- MVP with 5 MCP tools covering full CRUD lifecycle
- Single AI agent (task-manager-agent)
- 100+ concurrent users supported
- Conversation history unlimited (pagination for large histories)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Phase 2 Immutability
- ✅ **PASS**: Plan specifies Phase 2 as read-only reference
- ✅ **PASS**: New Phase 3 directory structure (backend/, frontend/)
- ✅ **PASS**: Copy patterns, don't import/link Phase 2 code
- **Verification**: No ../phase2/ modifications in plan or tasks

### II. Pattern Reuse Over Invention
- ✅ **PASS**: Database connection pattern from Phase 2
- ✅ **PASS**: JWT verification from Phase 2 auth.py
- ✅ **PASS**: Task/User models extended from Phase 2
- ✅ **PASS**: CRUD operations adapted for MCP tools
- **Verification**: Phase 2 patterns documented in research.md

### III. Documentation-First Development
- ✅ **PASS**: Context 7 MCP Server usage mandated in spec
- ⚠️ **PENDING**: Must query Context 7 before implementation
- **Action Required**: Document Context 7 queries in research.md
- **Verification**: Research phase must include Context 7 documentation queries

### IV. MCP Tool Pattern Compliance
- ✅ **PASS**: Spec requires mcp-tool-pattern skill compliance
- ⚠️ **PENDING**: Tools must follow Official MCP SDK syntax
- **Action Required**: Research mcp-tool-pattern skill structure
- **Verification**: Tools implementation must match pattern in contracts/

### V. Stateless Server Architecture
- ✅ **PASS**: Spec explicitly requires stateless design
- ✅ **PASS**: All conversation state in database (conversations, messages tables)
- ✅ **PASS**: No server-side session caching planned
- **Verification**: Architecture diagrams and data flow must show database persistence

### VI. Dual Interface Design
- ✅ **PASS**: Phase 2 task UI preserved (dashboard buttons)
- ✅ **PASS**: NEW chat interface added as additional route (/chat)
- ✅ **PASS**: Agent interprets intent and selects tools for chat operations
- ✅ **PASS**: Users choose interface: traditional buttons OR conversational AI
- **Verification**: Frontend includes BOTH dashboard (Phase 2) AND chat page (Phase 3 addition)

### VII. Grok API Integration
- ✅ **PASS**: Spec mandates Grok API (not OpenAI)
- ✅ **PASS**: OpenAI SDK with base_url override for Grok
- ⚠️ **PENDING**: Verify Grok model names and rate limits
- **Action Required**: Research Grok API endpoint and models via Context 7
- **Verification**: agent.py configuration must use x.ai endpoints

### VIII. Database Migration Safety
- ✅ **PASS**: New tables only (conversations, messages)
- ✅ **PASS**: Foreign keys to existing users table
- ✅ **PASS**: Spec requires migration scripts with rollback
- **Verification**: data-model.md must include migration strategy

**Constitution Check Status**: ✅ **PASS** with pending research items
- All principles satisfied at planning stage
- Pending items (Context 7 queries, MCP pattern research, Grok API verification) resolved in Phase 0
- No complexity violations requiring justification

## Project Structure

### Documentation (this feature)

```text
specs/002-ai-chat-interface/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (Context 7 queries, pattern research)
├── data-model.md        # Phase 1 output (database schema, migrations)
├── quickstart.md        # Phase 1 output (setup, deployment, testing)
├── contracts/           # Phase 1 output (API contracts, MCP tool specs)
│   ├── chat-api.yaml    # OpenAPI spec for POST /api/chat
│   ├── mcp-tools.json   # MCP tool definitions (5 tools)
│   └── database.sql     # Schema DDL with migrations
├── checklists/          # Quality validation
│   └── requirements.md  # Spec quality checklist (completed)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
phase3/
├── backend/
│   ├── main.py                 # FastAPI app initialization, CORS setup
│   ├── database.py             # Neon PostgreSQL connection (Phase 2 pattern)
│   ├── models.py               # SQLModel models (Task, User, Conversation, Message)
│   ├── auth.py                 # JWT verification middleware (Phase 2 pattern)
│   ├── agent.py                # Grok agent setup with OpenAI SDK
│   ├── mcp_server.py           # MCP tools implementation (5 tools)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py             # Phase 2 auth endpoints (signup, login)
│   │   ├── tasks.py            # Phase 2 CRUD endpoints (reference only)
│   │   └── chat.py             # NEW: POST /api/chat endpoint
│   ├── migrations/
│   │   ├── env.py              # Alembic environment
│   │   ├── script.py.mako      # Migration template
│   │   └── versions/
│   │       └── 001_add_conversations.py  # Add conversations + messages tables
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile              # HuggingFace Spaces deployment
│   └── .env.example            # Environment variables template
│
├── frontend/                   # Copied from Phase 2 + ChatKit additions
│   ├── app/
│   │   ├── layout.tsx          # (Phase 2) Root layout with providers
│   │   ├── page.tsx            # (Phase 2) Landing page
│   │   ├── login/page.tsx      # (Phase 2) Login form
│   │   ├── signup/page.tsx     # (Phase 2) Signup form
│   │   ├── dashboard/          # (Phase 2) Task management UI
│   │   │   ├── page.tsx
│   │   │   └── DashboardClient.tsx
│   │   └── chat/page.tsx       # NEW: ChatKit interface for AI conversations
│   ├── components/
│   │   ├── Navbar.tsx          # (Phase 2) Updated with "AI Chat" link
│   │   ├── tasks/              # (Phase 2) Task UI components
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskItem.tsx
│   │   │   ├── CreateTaskDialog.tsx
│   │   │   ├── EditTaskDialog.tsx
│   │   │   ├── DeleteConfirmDialog.tsx
│   │   │   └── EmptyState.tsx
│   │   ├── chat/               # NEW: Chat components
│   │   │   └── ChatInterface.tsx  # ChatKit wrapper component
│   │   ├── ThemeToggle.tsx     # (Phase 2)
│   │   └── ui/                 # (Phase 2) shadcn/ui components
│   ├── lib/
│   │   ├── api.ts              # (Phase 2) Task API client, add chat methods
│   │   ├── auth.ts             # (Phase 2) Authentication helpers
│   │   ├── types.ts            # (Phase 2) TypeScript types, add chat types
│   │   └── utils.ts            # (Phase 2) Utility functions
│   ├── hooks/                  # (Phase 2) Custom React hooks
│   ├── providers/              # (Phase 2) React context providers
│   ├── middleware.ts           # (Phase 2) Auth middleware
│   ├── next.config.ts          # (Phase 2) Next.js configuration
│   ├── package.json            # (Phase 2) + @openai/chat-kit dependency
│   ├── tsconfig.json           # (Phase 2) TypeScript config
│   └── .env.local              # Update API_URL to Phase 3 backend
│
└── .gitignore
```

**Structure Decision**: Extended Phase 2 architecture with AI addition:
- Separate backend API (FastAPI on HuggingFace Spaces)
- Extended frontend UI (Phase 2 Next.js + ChatKit route on Vercel)
- Shared database (Neon PostgreSQL from Phase 2)
- Independent deployment and scaling per service

**Phase 3 Frontend Strategy**: Copy Phase 2 frontend entirely, then ADD:
1. Install @openai/chat-kit dependency
2. Create new `/chat` route with ChatKit component
3. Update Navbar with "AI Chat" navigation link
4. Users get TWO ways to manage tasks: traditional buttons + AI conversation

Phase 3 creates new backend directory but COPIES Phase 2 frontend (with additions) to maintain pattern reuse.

## Complexity Tracking

> **No violations - table empty**

All constitution principles satisfied without exceptions:
- ✅ Phase 2 isolation maintained via copy approach (not modify-in-place)
- ✅ Pattern reuse through copying Phase 2 frontend structure
- ✅ Documentation-first via Context 7 (research phase)
- ✅ Standard MCP tool pattern (no custom framework)
- ✅ Stateless architecture (no in-memory complexity)
- ✅ Dual interface design (preserves Phase 2 UI, adds chat as option)
- ✅ Standard Grok API integration (OpenAI SDK compatibility)
- ✅ Safe migrations (additive only)

**Simplicity Wins**:
- Copying Phase 2 frontend instead of rebuilding from scratch
- Adding ChatKit as ONE additional route, not replacing entire UI
- Using pre-built ChatKit instead of custom chat UI
- Reusing Phase 2 auth/database patterns instead of reinventing
- Standard MCP tools instead of custom agent protocols
- Stateless design eliminates session management complexity
- Users choose their preferred interface (buttons or chat)
