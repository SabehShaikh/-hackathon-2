<!--
SYNC IMPACT REPORT:
Version: 0.0.0 → 1.0.0
Change Type: MAJOR (Initial constitution creation)
Modified Principles: All principles newly created
Added Sections: All sections new
Removed Sections: None

Templates Requiring Updates:
✅ plan-template.md - Constitution Check section aligns with principles
✅ spec-template.md - User story prioritization and acceptance criteria align
✅ tasks-template.md - Phase organization and testing principles align

Follow-up TODOs: None - all placeholders filled
-->

# Todo AI Chatbot - Phase 3 Constitution

## Core Principles

### I. Phase 2 Immutability

Phase 2 (../phase2/) is a read-only reference. All Phase 2 code remains untouched and operational.

**Rules:**
- MUST NOT modify any files in ../phase2/ directory
- MAY read Phase 2 code patterns for reference
- MUST copy and adapt patterns into Phase 3, never link or import directly
- Phase 2 and Phase 3 exist as independent deployments

**Rationale:** Phase 2 is production code serving existing users. Phase 3 is additive functionality with separate deployment paths. Keeping them isolated prevents regression and allows independent scaling.

### II. Pattern Reuse Over Invention

Replicate proven Phase 2 patterns before creating new solutions.

**Rules:**
- Database connection: Copy Neon PostgreSQL setup from Phase 2
- Authentication: Copy JWT verification logic from Phase 2
- Data models: Extend Task/User models from Phase 2
- CRUD operations: Adapt Phase 2 task operations for agent tools
- Error handling: Match Phase 2 error response formats

**Rationale:** Phase 2 patterns are battle-tested and align with existing infrastructure. Consistency reduces cognitive load and simplifies debugging across phases.

### III. Documentation-First Development

Use Context 7 MCP Server for all external API/SDK documentation before implementation.

**Rules:**
- MUST query Context 7 for latest MCP SDK syntax before defining tools
- MUST query Context 7 for OpenAI Agents SDK patterns before agent setup
- MUST query Context 7 for Grok API compatibility before AI integration
- MUST query Context 7 for FastAPI patterns before endpoint creation
- MUST query Context 7 for SQLModel queries before database operations
- NEVER assume SDK usage from internal knowledge
- NEVER proceed with implementation without verified documentation

**Rationale:** APIs and SDKs evolve. Context 7 provides current documentation, preventing deprecated patterns and ensuring compatibility with latest versions.

### IV. MCP Tool Pattern Compliance

All agent tools MUST follow mcp-tool-pattern skill specification.

**Rules:**
- Tool definitions use Official MCP SDK syntax
- Each tool has clear purpose, inputs, outputs, error cases
- Tools map 1:1 to Phase 2 CRUD operations where applicable
- Tool responses are JSON-serializable and self-documenting
- Error responses include actionable messages for agent interpretation

**Rationale:** Standardized tool patterns ensure agent reliability and simplify debugging. The mcp-tool-pattern skill codifies best practices for tool design.

### V. Stateless Server Architecture (NON-NEGOTIABLE)

Backend holds ZERO conversation state in memory. All state persists to database.

**Rules:**
- NO in-memory conversation storage
- NO server-side session caching
- ALL conversation history stored in Conversation/Message models
- Agent reconstructs context by querying database on each request
- Server MUST be restartable without losing conversation state

**Rationale:** Stateless design enables horizontal scaling, simplifies deployment to serverless platforms (HuggingFace Spaces), and prevents state corruption during crashes or redeployments.

### VI. Agent-Centric Design

Natural language understanding drives all task operations. UI is conversation-only.

**Rules:**
- NO task management UI controls (buttons, forms, checkboxes)
- ALL task operations triggered through chat messages
- Agent interprets intent and selects appropriate MCP tool
- Agent confirms actions explicitly before execution when ambiguous
- Agent provides natural language summaries of operations

**Rationale:** The product value is conversational task management. Traditional UI would dilute the AI-first experience and create maintenance overhead for dual interfaces.

### VII. Grok API Integration

Use Grok API (free tier) via OpenAI-compatible SDK. Never OpenAI API directly.

**Rules:**
- MUST use Grok API endpoints
- MUST use OpenAI SDK with Grok base URL override
- MUST verify Grok-compatible model names via Context 7
- MUST handle Grok-specific rate limits and errors
- Cost monitoring: Track token usage, alert on free tier approach

**Rationale:** Grok provides free tier AI capabilities compatible with OpenAI SDK. Using Grok reduces operational cost while maintaining SDK familiarity. Direct OpenAI usage would incur unnecessary expenses.

### VIII. Database Migration Safety

Extend Phase 2 database schema without breaking existing tables.

**Rules:**
- ADD new tables (Conversation, Message) without altering Phase 2 tables
- PRESERVE foreign key integrity to Phase 2 User table
- USE migrations for schema changes (Alembic or SQLModel equivalent)
- INCLUDE rollback scripts for every migration
- TEST migrations on development database before production

**Rationale:** Phase 2 continues using the same database. Backward-compatible migrations prevent service disruption and enable safe rollback if Phase 3 deployment fails.

## Development Workflow

### Spec-Driven Development (SDD)

ALL feature work follows this sequence:

1. **Specification** (`/sp.specify`): User stories, requirements, success criteria
2. **Planning** (`/sp.plan`): Architecture, technical decisions, ADR suggestions
3. **Task Generation** (`/sp.tasks`): Dependency-ordered, testable implementation tasks
4. **Implementation** (`/sp.implement`): Execute tasks with checkpoint validation
5. **Prompt History Records (PHR)**: Created automatically after EVERY user interaction

### PHR Enforcement

PHRs capture development decisions and context for auditability.

**Rules:**
- Create PHR after completing ANY user request (implementation, debugging, planning, spec creation)
- Route PHRs correctly:
  - Constitution work → `history/prompts/constitution/`
  - Feature work → `history/prompts/<feature-name>/`
  - General work → `history/prompts/general/`
- Fill ALL template placeholders (no `[PLACEHOLDER]` or `{{TOKEN}}` left behind)
- Embed full user PROMPT_TEXT (verbatim, not truncated)
- Include concise RESPONSE_TEXT summarizing assistant output
- Skip PHR ONLY for `/sp.phr` command itself

### ADR Workflow

Architectural Decision Records document significant technical choices.

**ADR Trigger Test (ALL must be true):**
1. **Impact**: Long-term consequences (framework choice, data model, API design, security, platform)
2. **Alternatives**: Multiple viable options considered
3. **Scope**: Cross-cutting, influences system design

**When triggered:**
- Suggest: "📋 Architectural decision detected: [brief description]. Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`"
- Wait for user consent
- NEVER auto-create ADRs

**Rationale:** ADRs preserve context for future developers. Over-documentation creates noise; under-documentation loses critical decisions. The three-part test balances thoroughness with efficiency.

## Technical Constraints

### Technology Stack

**Locked Choices (non-negotiable):**
- Backend Framework: FastAPI
- Database: Neon PostgreSQL (shared with Phase 2)
- ORM: SQLModel
- Authentication: Better Auth + JWT (Phase 2 pattern)
- AI Provider: Grok API (not OpenAI)
- Frontend: OpenAI ChatKit (pre-built chat UI)
- Deployment: HuggingFace Spaces (backend), Vercel (frontend)

**Flexible Choices (document in ADR if changed):**
- MCP SDK version (verify latest with Context 7)
- Agent SDK version (verify latest with Context 7)
- Migration tool (Alembic recommended, alternatives require justification)

### Performance Requirements

- Chat endpoint latency: <3s p95 (AI response time dominates)
- Database queries: <100ms p95 (local queries, Neon connection pooling)
- Concurrent users: 50+ supported (stateless architecture enables scaling)

### Security Requirements

- JWT token validation: Reuse Phase 2 auth middleware
- SQL injection prevention: Parameterized queries (SQLModel ORM default)
- API key storage: Environment variables only (.env files, never hardcoded)
- Rate limiting: Per-user limits on chat endpoint (prevent abuse)
- CORS: Frontend domain whitelisting (Vercel domain + localhost for dev)

## Quality Gates

### Pre-Implementation Gates

- [ ] Specification approved (user stories, requirements, success criteria defined)
- [ ] Planning complete (architecture, Phase 2 pattern mapping, ADRs created if needed)
- [ ] Tasks generated (dependency-ordered, testable, file paths specified)
- [ ] Context 7 queries completed (MCP SDK, OpenAI Agents SDK, Grok API docs verified)

### Implementation Gates

- [ ] Phase 2 patterns copied correctly (database, auth, CRUD operations)
- [ ] MCP tools follow mcp-tool-pattern skill
- [ ] Agent configured with Grok API (not OpenAI)
- [ ] Stateless architecture verified (no in-memory state)
- [ ] Database migrations tested (forward + rollback)

### Deployment Gates

- [ ] Environment variables configured (.env for local, secrets for production)
- [ ] Database migrations applied to Neon PostgreSQL
- [ ] Backend deployed to HuggingFace Spaces
- [ ] Frontend deployed to Vercel
- [ ] End-to-end conversation flow tested (authentication → chat → task operations)

## Governance

### Amendment Process

1. Propose change with rationale (why current principle insufficient)
2. Document impact (which templates/workflows affected)
3. Update constitution with version bump:
   - **MAJOR**: Backward-incompatible changes (principle removal/redefinition)
   - **MINOR**: New principle added or materially expanded guidance
   - **PATCH**: Clarifications, wording fixes, typo corrections
4. Sync dependent templates (plan, spec, tasks templates)
5. Create ADR if change meets significance criteria
6. Commit with message: `docs: amend constitution to vX.Y.Z (change summary)`

### Compliance

- ALL PRs/reviews MUST verify adherence to principles
- Complexity violations MUST be justified in plan.md Complexity Tracking table
- Phase 2 immutability violations MUST be rejected immediately
- Documentation-first violations MUST query Context 7 before approval

### Runtime Guidance

During development, refer to `CLAUDE.md` for agent-specific execution guidance. Constitution principles supersede default behaviors.

**Version**: 1.0.0 | **Ratified**: 2026-01-15 | **Last Amended**: 2026-01-15
