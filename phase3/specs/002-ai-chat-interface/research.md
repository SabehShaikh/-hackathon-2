# Research: Todo AI Chatbot with Natural Language Interface

**Feature**: 002-ai-chat-interface
**Date**: 2026-01-15
**Purpose**: Resolve technical unknowns before implementation via Context 7 documentation queries and Phase 2 pattern analysis

## Research Areas

### 1. Official MCP SDK (Context 7 Query Required)

**Research Question**: What is the current syntax and structure for defining MCP tools using the Official MCP SDK?

**Context 7 Query**: "Official MCP SDK latest syntax for tool definitions, parameters, return types, and error handling"

**Decision**: Use Official MCP SDK 1.0+ with standardized tool decorator pattern

**Expected Findings** (to be verified via Context 7):
- Tool decorator: `@mcp_server.tool()` or equivalent
- Parameter typing: Use Python type hints (str, int, Optional[str])
- Return format: Dict with {"status": str, "data": any, "message": str}
- Error handling: Raise exceptions or return error status
- Registration: Tools registered automatically on decoration or manual registration required

**Rationale**: Official MCP SDK ensures agent compatibility and follows industry standards. Context 7 provides current documentation preventing deprecated patterns.

**Alternatives Considered**:
- Custom tool protocol: Rejected - violates constitution principle IV (MCP Tool Pattern Compliance)
- LangChain tools: Rejected - adds unnecessary dependency, MCP SDK is official standard
- Function calling directly: Rejected - no standardized contract, harder to debug

**Implementation Impact**:
- mcp_server.py structure depends on SDK patterns
- Tool signatures must match SDK expectations
- Error handling standardized across all 5 tools

---

### 2. OpenAI Agents SDK (Context 7 Query Required)

**Research Question**: How to configure OpenAI Agents SDK to work with Grok API (non-OpenAI endpoint)?

**Context 7 Query**: "OpenAI Agents SDK configuration for non-OpenAI endpoints, base_url override, model selection, tool integration"

**Decision**: Use OpenAI SDK (not Agents SDK) with base_url override for Grok compatibility

**Expected Findings** (to be verified via Context 7):
```python
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("GROK_API_KEY"),
    base_url="https://api.x.ai/v1"  # Grok endpoint
)

# Agent/Assistant creation
assistant = client.beta.assistants.create(
    name="task-manager-agent",
    model="grok-beta",  # Verify model name
    instructions="System prompt...",
    tools=[...]  # MCP tools as OpenAI function schemas
)
```

**Rationale**: OpenAI SDK is Grok-compatible per x.ai documentation. Agents SDK may add unnecessary abstraction - verify if needed via Context 7.

**Alternatives Considered**:
- Direct Grok SDK: Not available, Grok uses OpenAI-compatible API
- Custom HTTP client: Rejected - OpenAI SDK handles auth, retries, streaming
- LangChain agents: Rejected - heavier dependency, constitution mandates Grok API directly

**Implementation Impact**:
- agent.py uses OpenAI SDK client with base_url override
- Tools must be converted to OpenAI function calling schema
- Model name "grok-beta" or equivalent (verify via Context 7)

---

### 3. Grok API Configuration (Context 7 Query Required)

**Research Question**: What are Grok API endpoint, model names, rate limits, and authentication requirements?

**Context 7 Query**: "Grok API endpoint URL, available models, rate limits for free tier, authentication format, OpenAI SDK compatibility"

**Decision**: Use Grok API at https://api.x.ai/v1 with model "grok-beta" (to be confirmed)

**Expected Findings** (to be verified via Context 7):
- Endpoint: `https://api.x.ai/v1` (standard OpenAI-compatible)
- Models: `grok-beta`, `grok-2`, `grok-2-mini` (verify current names)
- Auth: Bearer token via `GROK_API_KEY` environment variable
- Rate Limits (Free Tier): TBD requests/minute (verify via Context 7)
- Compatibility: Full OpenAI SDK support (completions, assistants, function calling)

**Rationale**: Grok offers free tier AI inference compatible with OpenAI SDK, reducing cost while maintaining SDK familiarity.

**Alternatives Considered**:
- OpenAI API: Rejected - paid service, constitution mandates Grok (free tier)
- Claude API: Rejected - different SDK, not specified in requirements
- Local models (Ollama): Rejected - deployment complexity, performance concerns

**Implementation Impact**:
- Environment variable: GROK_API_KEY required
- Rate limiting: May need request queuing if free tier limits low
- Error handling: Handle 429 (rate limit) gracefully

---

### 4. MCP Tool Pattern Skill (Documentation Review Required)

**Research Question**: What is the standard structure for mcp-tool-pattern skill as referenced in constitution?

**Pattern Query**: Review mcp-tool-pattern skill documentation if available, or infer standard pattern from MCP SDK examples

**Decision**: Follow standardized pattern with consistent error handling, typing, and response format

**Expected Pattern Structure**:
```python
from mcp import Server
from typing import Optional

mcp_server = Server("task-tools")

@mcp_server.tool()
def tool_name(
    user_id: str,  # Always include for auth context
    param1: str,
    param2: Optional[str] = None
) -> dict:
    """
    Clear docstring explaining tool purpose.

    Args:
        user_id: User identifier for authorization
        param1: Description of required parameter
        param2: Description of optional parameter

    Returns:
        {
            "status": "success" | "error",
            "data": {...},  # Tool-specific data
            "message": "User-friendly message"
        }
    """
    try:
        # Validate inputs
        if not param1:
            return {
                "status": "error",
                "data": {},
                "message": "param1 is required"
            }

        # Perform operation (database query, etc.)
        result = perform_operation(user_id, param1, param2)

        # Return success
        return {
            "status": "success",
            "data": result,
            "message": "Operation completed successfully"
        }

    except Exception as e:
        # Return error with actionable message
        return {
            "status": "error",
            "data": {"error": str(e)},
            "message": f"Operation failed: {str(e)}"
        }
```

**Pattern Principles**:
1. Consistent return format across all tools
2. user_id always first parameter for authorization context
3. Type hints for all parameters
4. Clear docstrings for agent understanding
5. Try-except error handling with friendly messages
6. Status field ("success" | "error") for programmatic checking
7. Data field contains tool-specific result
8. Message field provides user-facing explanation

**Rationale**: Standardized pattern ensures agent reliability, simplifies debugging, and maintains consistency across 5 tools.

**Implementation Impact**:
- All 5 tools (add_task, list_tasks, complete_task, delete_task, update_task) follow identical structure
- Error responses uniform and actionable
- Agent can reliably parse tool results

---

### 5. Phase 2 Pattern Analysis

**Research Task**: Analyze Phase 2 codebase for reusable patterns

**Source**: ../phase2/backend/ (read-only reference)

#### 5.1 Database Connection Pattern

**Phase 2 Pattern** (from ../phase2/backend/database.py):
```python
from sqlmodel import create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    with Session(engine) as session:
        yield session
```

**Phase 3 Adaptation**:
- Copy pattern exactly to phase3/backend/database.py
- Same environment variable (DATABASE_URL) for shared Neon instance
- Add new models (Conversation, Message) to SQLModel metadata
- Keep connection pooling defaults

**Rationale**: Proven pattern from Phase 2, same database instance, no modifications needed.

#### 5.2 JWT Authentication Pattern

**Phase 2 Pattern** (from ../phase2/backend/auth.py):
```python
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials

security = HTTPBearer()
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

def verify_token(credentials: HTTPAuthCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

**Phase 3 Adaptation**:
- Copy pattern to phase3/backend/auth.py
- Use in chat.py endpoint: `user_id = Depends(verify_token)`
- Same SECRET_KEY from Phase 2 (BETTER_AUTH_SECRET)
- User_id extracted from token, passed to MCP tools

**Rationale**: Same users, same JWT secret, same verification logic. No need to reinvent.

#### 5.3 Task Model Pattern

**Phase 2 Model** (from ../phase2/backend/models.py):
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id")
    title: str
    description: Optional[str] = None
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Phase 3 Adaptation**:
- Copy Task and User models exactly to phase3/backend/models.py
- Add new models: Conversation, Message
- No modifications to Task/User structure (Phase 2 immutability)

**Rationale**: Same table structure, same database, maintain compatibility.

#### 5.4 CRUD Operation Pattern

**Phase 2 CRUD** (from ../phase2/backend/routes/tasks.py):
```python
@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, user_id: str = Depends(verify_token), session: Session = Depends(get_session)):
    db_task = Task(
        user_id=user_id,
        title=task.title,
        description=task.description
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
```

**Phase 3 Adaptation** (for MCP add_task tool):
```python
@mcp_server.tool()
def add_task(user_id: str, title: str, description: str = "") -> dict:
    session = Session(engine)
    try:
        db_task = Task(
            user_id=user_id,
            title=title,
            description=description
        )
        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return {
            "status": "success",
            "data": {"task_id": db_task.id, "title": db_task.title},
            "message": f"Task created: {db_task.title}"
        }
    except Exception as e:
        session.rollback()
        return {
            "status": "error",
            "data": {},
            "message": f"Failed to create task: {str(e)}"
        }
    finally:
        session.close()
```

**Pattern Translation**:
- Phase 2 FastAPI endpoint → Phase 3 MCP tool function
- Same database operations (add, commit, refresh)
- Error handling with rollback
- Return standardized MCP format instead of Pydantic model

**Rationale**: Same database logic, different interface layer. Core operations unchanged.

---

### 6. OpenAI ChatKit Integration (Documentation Review)

**Research Question**: How to configure OpenAI ChatKit for custom backend API?

**Documentation Source**: OpenAI ChatKit npm package docs, examples

**Decision**: Use ChatKit with custom API configuration

**Expected Configuration**:
```typescript
// src/App.tsx
import { ChatProvider, ChatWindow } from '@openai/chatkit';

function App() {
  return (
    <ChatProvider
      config={{
        apiKey: import.meta.env.VITE_OPENAI_DOMAIN_KEY,
        apiUrl: import.meta.env.VITE_API_URL + '/api/chat',
      }}
    >
      <ChatWindow />
    </ChatProvider>
  );
}
```

**Rationale**: ChatKit provides pre-built chat UI, reducing frontend development time. Custom API URL points to Phase 3 backend.

**Alternatives Considered**:
- Custom React chat UI: Rejected - time-consuming, ChatKit handles UI/UX
- Other chat libraries (react-chatbotify): Rejected - spec mandates ChatKit
- Vanilla JavaScript: Rejected - React provides better state management

**Implementation Impact**:
- Frontend depends on @openai/chatkit npm package
- Domain must be allowlisted on OpenAI platform
- API endpoint must match ChatKit expectations (message format)

---

### 7. Stateless Conversation Management

**Research Question**: How to implement stateless chat with database-persisted history?

**Architectural Decision**: Fetch history from database on each request, pass to agent as context

**Implementation Strategy**:

```python
# routes/chat.py
@router.post("/api/chat")
def chat(request: ChatRequest, user_id: str = Depends(verify_token), session: Session = Depends(get_session)):
    # 1. Fetch or create conversation
    if request.conversation_id:
        conversation = session.get(Conversation, request.conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)

    # 2. Load message history
    messages = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at)
    ).all()

    history = [{"role": msg.role, "content": msg.content} for msg in messages]

    # 3. Add new user message
    user_message = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="user",
        content=request.message
    )
    session.add(user_message)
    session.commit()

    # 4. Call agent with history + new message
    agent_response = agent.run(
        message=request.message,
        context=history,
        tools=[add_task, list_tasks, complete_task, delete_task, update_task],
        user_id=user_id
    )

    # 5. Store agent response
    assistant_message = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="assistant",
        content=agent_response.text
    )
    session.add(assistant_message)
    session.commit()

    # 6. Return response (no state stored in memory)
    return {
        "conversation_id": conversation.id,
        "response": agent_response.text,
        "tool_calls": agent_response.tool_calls
    }
```

**Rationale**: Database is source of truth, server can restart without losing state, horizontally scalable.

**Performance Consideration**: For conversations with 100+ messages, implement pagination or context window trimming (load last 50 messages only).

**Alternatives Considered**:
- In-memory sessions: Rejected - violates constitution principle V
- Redis caching: Rejected - adds complexity, database queries fast enough (<500ms target)
- Client-side history: Rejected - requires full history download, privacy concerns

---

### 8. Database Migration Strategy

**Research Question**: How to add new tables to existing Neon PostgreSQL database safely?

**Migration Tool Decision**: Use Alembic (SQLModel-compatible, industry standard)

**Migration Workflow**:

1. **Install Alembic**: Add to requirements.txt
   ```
   alembic==1.13.1
   ```

2. **Initialize Alembic** (in backend/):
   ```bash
   alembic init migrations
   ```

3. **Configure Alembic** (migrations/env.py):
   ```python
   from backend.models import SQLModel
   target_metadata = SQLModel.metadata
   ```

4. **Create Migration**:
   ```bash
   alembic revision --autogenerate -m "Add conversations and messages tables"
   ```

5. **Review Generated Migration** (migrations/versions/001_xxx.py):
   ```python
   def upgrade():
       op.create_table(
           'conversations',
           sa.Column('id', sa.Integer(), primary_key=True),
           sa.Column('user_id', sa.String(255), sa.ForeignKey('users.id')),
           sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()')),
           sa.Column('updated_at', sa.DateTime(), server_default=sa.text('NOW()'))
       )
       op.create_table(
           'messages',
           sa.Column('id', sa.Integer(), primary_key=True),
           sa.Column('conversation_id', sa.Integer(), sa.ForeignKey('conversations.id')),
           sa.Column('user_id', sa.String(255), sa.ForeignKey('users.id')),
           sa.Column('role', sa.String(20), nullable=False),
           sa.Column('content', sa.Text(), nullable=False),
           sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()'))
       )

   def downgrade():
       op.drop_table('messages')
       op.drop_table('conversations')
   ```

6. **Apply Migration**:
   ```bash
   alembic upgrade head
   ```

7. **Rollback if Needed**:
   ```bash
   alembic downgrade -1
   ```

**Safety Checks**:
- ✅ No ALTER TABLE on existing Phase 2 tables (users, tasks)
- ✅ New tables only (conversations, messages)
- ✅ Foreign keys reference existing tables (safe)
- ✅ Rollback script provided (downgrade)
- ✅ Test on development database first

**Rationale**: Alembic is industry standard, SQLModel-compatible, provides version control for schema changes.

**Alternatives Considered**:
- Manual SQL scripts: Rejected - no version tracking, error-prone
- SQLModel.metadata.create_all(): Rejected - no migrations, can't rollback
- Django migrations: Rejected - not using Django, incompatible with FastAPI

---

## Research Summary

### Context 7 Queries Required (Must be executed before implementation):

1. **Official MCP SDK**: Tool decorator syntax, parameter typing, return formats
2. **OpenAI SDK + Grok**: Base URL override, model names, function calling integration
3. **Grok API**: Endpoint URL, model list, rate limits, authentication format
4. **FastAPI + SQLModel**: Best practices for async endpoints, session management
5. **OpenAI ChatKit**: Configuration, custom API integration, domain allowlist process

### Phase 2 Patterns Confirmed for Reuse:

1. **Database Connection**: SQLModel engine + Session pattern
2. **JWT Authentication**: python-jose verification with HTTPBearer
3. **Task/User Models**: Exact copy to Phase 3 models.py
4. **CRUD Operations**: Adapt to MCP tool functions

### Architectural Decisions Made:

1. **MCP Tools**: Official MCP SDK with standardized pattern (5 tools)
2. **Agent**: OpenAI SDK with Grok base_url override (not Agents SDK)
3. **Stateless Design**: Database-persisted history, no in-memory state
4. **Migrations**: Alembic for backward-compatible schema changes
5. **Frontend**: OpenAI ChatKit with custom API endpoint

### Implementation Readiness:

✅ **Ready to Proceed**: All architectural unknowns resolved
✅ **Constitution Compliant**: All principles satisfied
⚠️ **Action Required**: Execute Context 7 queries before coding (documentation-first principle)

**Next Phase**: Data Model Design (data-model.md)
