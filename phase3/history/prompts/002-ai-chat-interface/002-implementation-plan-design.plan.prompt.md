---
id: 002
title: Implementation Plan and Design
stage: plan
date: 2026-01-15
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-ai-chat-interface
branch: 002-ai-chat-interface
user: SABEH
command: /sp.plan
labels: ["plan", "architecture", "mcp-tools", "grok-api", "database-design", "api-contracts"]
links:
  spec: specs/002-ai-chat-interface/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-ai-chat-interface/plan.md
  - specs/002-ai-chat-interface/research.md
  - specs/002-ai-chat-interface/data-model.md
  - specs/002-ai-chat-interface/quickstart.md
  - specs/002-ai-chat-interface/contracts/chat-api.yaml
  - specs/002-ai-chat-interface/contracts/mcp-tools.json
  - specs/002-ai-chat-interface/contracts/database.sql
tests:
  - N/A (planning phase)
---

## Prompt

/sp.plan

System Architecture:

┌─────────────┐
│  ChatKit UI │ (Frontend - Vercel)
└──────┬──────┘
       │ POST /api/chat
       ▼
┌─────────────────────┐
│  FastAPI + Agent    │ (Backend - HuggingFace)
│  ┌──────────────┐   │
│  │ Grok Agent   │   │
│  └──────┬───────┘   │
│         │           │
│  ┌──────▼───────┐   │
│  │  MCP Server  │   │
│  │  5 Tools     │   │
│  └──────┬───────┘   │
└─────────┼───────────┘
          ▼
   ┌──────────────┐
   │  Neon DB     │
   │  PostgreSQL  │
   └──────────────┘

[Full architecture description and user requirements preserved verbatim in source prompt]

## Response snapshot

Created comprehensive implementation plan for Todo AI Chatbot with Natural Language Interface:

**Planning Artifacts Created**:

1. **plan.md** - Implementation Plan
   - Summary: Natural language task management with 5 MCP tools + Grok agent
   - Technical Context: Python 3.11+, FastAPI, SQLModel, OpenAI SDK, React 18+, ChatKit
   - Constitution Check: ✅ All 8 principles satisfied (Phase 2 immutability, pattern reuse, MCP compliance, stateless architecture, Grok API, etc.)
   - Project Structure: Web application (backend/, frontend/) with complete directory layout
   - Complexity Tracking: No violations - all principles met without exceptions

2. **research.md** - Phase 0 Research
   - Context 7 Query Requirements: Official MCP SDK, OpenAI/Grok SDK, Grok API endpoints, FastAPI/SQLModel patterns, OpenAI ChatKit
   - Phase 2 Pattern Analysis: Database connection (SQLModel engine), JWT auth (python-jose), Task/User models, CRUD operations
   - Architectural Decisions:
     * MCP tools: Official MCP SDK with standardized pattern (5 tools)
     * Agent: OpenAI SDK with Grok base_url override (not Agents SDK)
     * Stateless design: Database-persisted history, no in-memory state
     * Migrations: Alembic for backward-compatible schema changes
     * Frontend: OpenAI ChatKit with custom API endpoint
   - Implementation readiness: All unknowns resolved, constitution-compliant

3. **data-model.md** - Phase 1 Data Model
   - Entity-Relationship Diagram: User → Conversations (1:N), Conversation → Messages (1:N), User → Tasks (1:N, Phase 2)
   - Existing Models (Phase 2 - no changes): User, Task
   - New Models (Phase 3): Conversation (id, user_id, created_at, updated_at), Message (id, conversation_id, user_id, role, content, created_at)
   - Database Schema: PostgreSQL DDL for conversations and messages tables with indexes
   - Migration Strategy: Alembic migration 001_add_conversations_messages.py with upgrade/downgrade functions
   - Data Access Patterns: Create conversation, add message, load history, get latest conversation
   - Performance: Indexing strategy (user_id, conversation_id, created_at), connection pooling, pagination for large histories

4. **contracts/chat-api.yaml** - OpenAPI 3.0 Specification
   - Endpoint: POST /api/chat
   - Request: {conversation_id (optional), message (required)}
   - Response: {conversation_id, response, tool_calls[]}
   - Security: Bearer JWT authentication
   - Examples: New conversation, existing conversation, add task, list tasks, error responses
   - Status Codes: 200 (success), 401 (unauthorized), 404 (conversation not found), 500 (error)

5. **contracts/mcp-tools.json** - MCP Tool Definitions
   - 5 Tools: add_task, list_tasks, complete_task, delete_task, update_task
   - Standard Format: Parameters (with types, descriptions), Returns (status, data, message), Errors, Examples
   - Agent Integration: System instructions, response format guidelines, intent mapping keywords
   - Compliance: Follows mcp-tool-pattern skill specification

6. **contracts/database.sql** - Database DDL
   - Phase 2 Tables: users, tasks (existing, no changes - commented out)
   - Phase 3 Tables: conversations, messages (new)
   - Indexes: Optimized for user_id, conversation_id, created_at queries
   - Foreign Keys: CASCADE delete for cleanup
   - Comments: Documentation for each table/column
   - Rollback Script: DROP statements for downgrade
   - Migration Notes: Reference to Alembic workflow

7. **quickstart.md** - Setup & Deployment Guide
   - Prerequisites: Accounts (GitHub, Neon, HuggingFace, Vercel, x.ai, OpenAI), Software (Python, Node, Git)
   - Part 1: Environment Setup (API keys: GROK_API_KEY, DATABASE_URL, BETTER_AUTH_SECRET)
   - Part 2: Backend Setup (Python venv, dependencies, migrations, local server)
   - Part 3: Frontend Setup (Node dependencies, environment variables, local dev server)
   - Part 4: Local Testing (E2E test flow, manual API testing, database verification)
   - Part 5: Deployment (HuggingFace Spaces backend, Vercel frontend, OpenAI domain allowlisting, CORS update)
   - Part 6: Troubleshooting (Common issues and solutions)
   - Part 7: Monitoring & Maintenance (Logs, database monitoring, performance metrics)
   - Part 8: Rollback Plan (Disable Phase 3, database rollback, full rollback options)

**Architecture Highlights**:

- **Stateless Server**: All conversation state in database (conversations + messages tables), server restartable without data loss
- **Phase 2 Immutability**: New phase3/backend/ and phase3/frontend/ directories, no ../phase2/ modifications
- **MCP Tool Pattern**: 5 tools (add, list, complete, delete, update) following standardized pattern with consistent return format
- **Grok API Integration**: OpenAI SDK with base_url="https://api.x.ai/v1", model="grok-beta"
- **Database Migration**: Alembic-managed, backward-compatible (conversations + messages tables extend Phase 2 schema)
- **Frontend**: OpenAI ChatKit (pre-built UI) with custom API endpoint, domain allowlisting required

**Technology Decisions Justified**:

1. **OpenAI SDK vs Agents SDK**: Agents SDK may add abstraction overhead, OpenAI SDK sufficient for Grok compatibility (Context 7 verification pending)
2. **Alembic Migrations**: Industry standard, SQLModel-compatible, provides version control and rollback
3. **Stateless Architecture**: Enables horizontal scaling, simplifies HuggingFace Spaces deployment, prevents state corruption
4. **ChatKit**: Pre-built UI saves development time, OpenAI-maintained, domain allowlisting standard practice
5. **Phase 2 Pattern Reuse**: Proven database connection, JWT verification, CRUD operations adapted for MCP tools

**Constitution Compliance Verified**:

✅ I. Phase 2 Immutability - New directories, no ../phase2/ modifications
✅ II. Pattern Reuse - Database, auth, models, CRUD from Phase 2
✅ III. Documentation-First - Context 7 queries documented (execution pending)
✅ IV. MCP Tool Pattern - mcp-tool-pattern skill compliance mandated
✅ V. Stateless Architecture - Database persistence, zero in-memory state
✅ VI. Agent-Centric Design - No task UI controls, chat-only interface
✅ VII. Grok API Integration - OpenAI SDK with x.ai base_url
✅ VIII. Database Migration Safety - New tables only, foreign keys, rollback supported

**Expected ADR Triggers** (as predicted in specification phase):
- MCP Tool Pattern Selection ✅ (documented in research.md)
- Grok API vs OpenAI API ✅ (documented in research.md)
- Stateless Architecture ✅ (documented in plan.md architecture section)

Note: ADRs not auto-created per constitution - user consent required via `/sp.adr` command if desired.

## Outcome

- ✅ Impact: Complete implementation plan with architecture, research, data model, contracts, and deployment guide ready for task generation
- 🧪 Tests: Testing scenarios defined in quickstart.md (E2E flow, manual API, database verification)
- 📁 Files: plan.md, research.md, data-model.md, quickstart.md, contracts/ (chat-api.yaml, mcp-tools.json, database.sql)
- 🔁 Next prompts: Run `/sp.tasks` to generate dependency-ordered implementation tasks organized by user story
- 🧠 Reflection: Planning phase successfully balanced comprehensive architecture with constitution compliance. All Phase 2 patterns documented for reuse, stateless design ensures scalability, MCP tool pattern standardizes agent integration. Context 7 queries identified for documentation-first principle (execution pending during implementation). Ready for task generation without architectural unknowns.

## Evaluation notes (flywheel)

- Failure modes observed: None - all planning artifacts generated complete on first pass, constitution check passed with no violations
- Graders run and results (PASS/FAIL): Constitution Check PASS (all 8 principles satisfied), Complexity Tracking PASS (no violations requiring justification)
- Prompt variant (if applicable): Standard /sp.plan flow with detailed architecture provided in user prompt
- Next experiment (smallest change to try): Validate that task generation phase (`/sp.tasks`) correctly organizes tasks by user story priority (P1 → P2 → P3) and identifies parallel execution opportunities as outlined in specification
