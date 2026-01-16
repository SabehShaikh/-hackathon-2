---
id: 001
title: Initial constitution for Phase 3
stage: constitution
date: 2026-01-15
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: SABEH
command: /sp.constitution
labels: ["constitution", "phase3", "setup", "governance"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (documentation only)
---

## Prompt

/sp.constitution

Project: Todo AI Chatbot - Phase 3

Context:
Builds on Phase 2 (../phase2/) full-stack todo app. Phase 2 remains unchanged. Phase 3 adds conversational AI interface while reusing Phase 2 backend patterns.

Development Tools:
- SpecifyPlus: Spec-driven development workflow
- Claude Code: Code generation agent
- Context 7 MCP Server: Access current documentation for:
  * Official MCP SDK (latest syntax and patterns)
  * OpenAI Agents SDK (tool calling, agent setup)
  * Grok API (Grok-compatible OpenAI SDK usage)
  * FastAPI (endpoint patterns)
  * SQLModel (ORM queries)

Core Objective:
Enable users to manage tasks through natural language conversation instead of UI buttons.

Tech Stack:

Frontend:
- OpenAI ChatKit (pre-built chat UI)
- Replaces Phase 2's Next.js interface

Backend (Extends Phase 2 patterns):
- FastAPI (same as Phase 2)
- SQLModel ORM (same as Phase 2)
- Neon PostgreSQL (same database as Phase 2)
- Better Auth + JWT (same auth as Phase 2)
- NEW: Official MCP SDK (for tool definitions)
- NEW: OpenAI Agents SDK (compatible with Grok API)
- NEW: Grok API (free tier for AI responses)

Code Reuse from Phase 2:
Reference (read-only) from ../phase2/backend/:
- Database models: Task, User (copy pattern)
- Database connection: Neon PostgreSQL setup (copy pattern)
- Auth system: JWT verification (copy pattern)
- CRUD operations: Task operations (copy pattern)

Phase 2 folder remains untouched. Phase 3 creates new files based on Phase 2 patterns.

Architecture:

Phase 3 Backend Structure:
phase3/backend/
├── models.py          # Task, User (from Phase 2) + Conversation, Message (new)
├── database.py        # Neon connection (from Phase 2)
├── auth.py            # JWT verification (from Phase 2)
├── mcp_server.py      # NEW: MCP tools using Official MCP SDK
├── agent.py           # NEW: Agent setup with Grok API
├── routes/
│   ├── auth.py        # Auth endpoints (from Phase 2)
│   ├── tasks.py       # Task CRUD endpoints (from Phase 2)
│   └── chat.py        # NEW: Chat endpoint
└── main.py            # FastAPI app

MCP Tools (5 Required):
Use Context 7 to access latest MCP SDK documentation.
Follow mcp-tool-pattern skill for all tools:

1. add_task(user_id, title, description)
2. list_tasks(user_id, status)
3. complete_task(user_id, task_id)
4. delete_task(user_id, task_id)
5. update_task(user_id, task_id, title, description)

Agent Configuration:
- Name: task-manager-agent
- AI: Grok API (via OpenAI-compatible SDK)
- Tools: 5 MCP tools
- Behavior: Interpret natural language, call appropriate tools, confirm actions

Stateless Architecture:
Server holds NO state. All conversation history in database.

Database Models:
From Phase 2 (copy pattern):
- User: id, email, password_hash, created_at
- Task: id, user_id, title, description, completed, created_at, updated_at

New for Phase 3:
- Conversation: id, user_id, created_at, updated_at
- Message: id, conversation_id, user_id, role, content, created_at

API Endpoints:
Keep from Phase 2 pattern:
- POST /api/auth/signup
- POST /api/auth/login
- GET /api/tasks/
- POST /api/tasks/
- PUT /api/tasks/{id}
- PATCH /api/tasks/{id}/complete
- DELETE /api/tasks/{id}

New for Phase 3:
- POST /api/chat
  Request: {conversation_id (optional), message}
  Response: {conversation_id, response, tool_calls}

Frontend:
- OpenAI ChatKit component
- Calls POST /api/chat endpoint
- Displays conversation history

Deployment:
- Backend: HuggingFace Spaces (new Space for Phase 3)
- Frontend: Vercel (new deployment for Phase 3)
- Database: Same Neon PostgreSQL (add new tables)

Success Criteria:
- Natural language task management works
- Conversation persists across sessions
- AI interprets commands correctly
- Graceful error handling
- All CRUD operations via chat

Constraints:
- Phase 2 folder untouched
- Use Context 7 for current documentation
- Use Grok API (free) not OpenAI (paid)
- Follow mcp-tool-pattern skill
- Stateless server architecture
- Spec-driven development (no manual coding)

## Response snapshot

Created comprehensive constitution v1.0.0 for Todo AI Chatbot - Phase 3 with 8 core principles:

1. **Phase 2 Immutability**: Read-only reference to Phase 2 codebase, no modifications allowed
2. **Pattern Reuse Over Invention**: Copy proven Phase 2 patterns (database, auth, CRUD)
3. **Documentation-First Development**: Query Context 7 MCP Server before all implementation
4. **MCP Tool Pattern Compliance**: Follow mcp-tool-pattern skill for all 5 agent tools
5. **Stateless Server Architecture**: Zero in-memory state, all conversation history in database
6. **Agent-Centric Design**: Natural language only, no UI controls
7. **Grok API Integration**: Use Grok free tier via OpenAI-compatible SDK
8. **Database Migration Safety**: Extend Phase 2 schema without breaking changes

Added sections:
- Development Workflow (SDD process: specify → plan → tasks → implement)
- PHR Enforcement (routing, template filling, verbatim prompt capture)
- ADR Workflow (three-part significance test, user consent required)
- Technical Constraints (locked vs flexible tech stack choices)
- Performance/Security Requirements
- Quality Gates (pre-implementation, implementation, deployment)
- Governance (amendment process, compliance rules)

All templates verified for alignment:
✅ plan-template.md - Constitution Check section compatible
✅ spec-template.md - User story prioritization aligns
✅ tasks-template.md - Phase organization matches workflow

No unresolved placeholders. Constitution ready for use.

## Outcome

- ✅ Impact: Established governance framework for Phase 3 development, ensuring consistency with Phase 2 patterns and documentation-first approach
- 🧪 Tests: N/A (documentation artifact)
- 📁 Files: Created .specify/memory/constitution.md (v1.0.0)
- 🔁 Next prompts: Run `/sp.specify` to create feature specification, then `/sp.plan` for architecture design
- 🧠 Reflection: Constitution successfully bridges Phase 2 patterns with Phase 3 AI capabilities while maintaining strict separation and documentation discipline

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution template filled completely on first pass
- Graders run and results (PASS/FAIL): Manual validation PASS (no unresolved tokens, all principles testable, templates aligned)
- Prompt variant (if applicable): N/A (standard constitution creation flow)
- Next experiment (smallest change to try): Test constitution compliance during `/sp.specify` execution to verify principles are enforceable
