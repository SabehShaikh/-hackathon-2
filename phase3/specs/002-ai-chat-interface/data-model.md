# Data Model: Todo AI Chatbot with Natural Language Interface

**Feature**: 002-ai-chat-interface
**Date**: 2026-01-15
**Purpose**: Define database schema, models, relationships, and migration strategy

## Entity-Relationship Overview

```text
┌──────────────┐
│    User      │ (Phase 2 - existing)
│ ───────────  │
│ id (PK)      │───┐
│ email        │   │
│ password_hash│   │
│ created_at   │   │
└──────────────┘   │
                   │ (1:N)
        ┌──────────┴────────────┐
        │                       │
        ▼                       ▼
┌──────────────┐        ┌──────────────┐
│ Conversation │        │     Task     │ (Phase 2 - existing)
│ ──────────── │        │ ──────────── │
│ id (PK)      │───┐    │ id (PK)      │
│ user_id (FK) │   │    │ user_id (FK) │
│ created_at   │   │    │ title        │
│ updated_at   │   │    │ description  │
└──────────────┘   │    │ completed    │
                   │    │ created_at   │
                   │    │ updated_at   │
        (1:N)      │    └──────────────┘
                   │
                   ▼
           ┌──────────────┐
           │   Message    │
           │ ──────────── │
           │ id (PK)      │
           │ conversation_id (FK)
           │ user_id (FK) │
           │ role         │
           │ content      │
           │ created_at   │
           └──────────────┘
```

## Models (SQLModel)

### Existing Models (Phase 2 - No Changes)

#### User Model

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    """
    User authentication and identity.
    Phase 2 model - DO NOT MODIFY.
    """
    __tablename__ = "users"

    id: str = Field(primary_key=True)  # UUID from Better Auth
    email: str = Field(unique=True, index=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Relationships**:
- Has many Tasks (1:N)
- Has many Conversations (1:N) - NEW in Phase 3
- Has many Messages (1:N) - NEW in Phase 3

**Business Rules**:
- Email must be unique
- Password stored as bcrypt hash
- Cannot be deleted if tasks or conversations exist (foreign key constraint)

---

#### Task Model

```python
class Task(SQLModel, table=True):
    """
    Todo item belonging to a user.
    Phase 2 model - DO NOT MODIFY.
    """
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=2000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Relationships**:
- Belongs to User (N:1)

**Business Rules**:
- Title required (1-500 chars)
- Description optional (max 2000 chars)
- Default completed=False
- updated_at should be updated on modification (app layer responsibility)

**Indexes**:
- user_id (for querying user's tasks)
- completed (optional, for filtering)

---

### New Models (Phase 3)

#### Conversation Model

```python
class Conversation(SQLModel, table=True):
    """
    Chat conversation between user and AI agent.
    Persists conversation context for multi-session continuity.
    """
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Relationships**:
- Belongs to User (N:1)
- Has many Messages (1:N)

**Business Rules**:
- One user can have multiple conversations (sequential or archived)
- Conversations never deleted (history preservation)
- updated_at reflects last message timestamp

**Indexes**:
- user_id (for fetching user's conversations)
- created_at DESC (for sorting recent conversations)

**Queries**:
```python
# Get user's latest conversation
latest = session.exec(
    select(Conversation)
    .where(Conversation.user_id == user_id)
    .order_by(Conversation.updated_at.desc())
    .limit(1)
).first()

# Get all user conversations (for history UI)
conversations = session.exec(
    select(Conversation)
    .where(Conversation.user_id == user_id)
    .order_by(Conversation.created_at.desc())
).all()
```

---

#### Message Model

```python
from enum import Enum

class MessageRole(str, Enum):
    """Message sender role"""
    USER = "user"
    ASSISTANT = "assistant"

class Message(SQLModel, table=True):
    """
    Individual message in a conversation.
    Stores both user inputs and AI responses.
    """
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    role: MessageRole = Field(sa_column=Column(Enum(MessageRole)))
    content: str = Field(max_length=10000)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Relationships**:
- Belongs to Conversation (N:1)
- Belongs to User (N:1)

**Business Rules**:
- Role must be "user" or "assistant"
- Content max 10,000 chars (long conversations supported)
- Messages immutable after creation (no updates/deletes)
- Ordered by created_at for display

**Validation**:
- Role: Enum enforces valid values only
- Content: Non-empty (min_length=1 validation in app layer)
- user_id: Must match conversation.user_id (app layer check)

**Indexes**:
- conversation_id (for loading conversation history)
- created_at (for ordering messages chronologically)

**Queries**:
```python
# Load conversation history
messages = session.exec(
    select(Message)
    .where(Message.conversation_id == conversation_id)
    .order_by(Message.created_at)
).all()

# Load recent messages (pagination for long conversations)
recent_messages = session.exec(
    select(Message)
    .where(Message.conversation_id == conversation_id)
    .order_by(Message.created_at.desc())
    .limit(50)
).all()
recent_messages.reverse()  # Chronological order

# Count messages in conversation
message_count = session.exec(
    select(func.count(Message.id))
    .where(Message.conversation_id == conversation_id)
).one()
```

---

## Database Schema (DDL)

### Phase 2 Tables (Existing - No Changes)

```sql
-- Users table (Phase 2 - existing)
CREATE TABLE users (
    id VARCHAR(255) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- Tasks table (Phase 2 - existing)
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

### Phase 3 Tables (New)

```sql
-- Conversations table (Phase 3 - new)
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_created_at ON conversations(created_at DESC);

-- Messages table (Phase 3 - new)
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    user_id VARCHAR(255) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```

**Foreign Key Behavior**:
- `ON DELETE CASCADE`: If user deleted, all conversations and messages deleted
- `ON DELETE CASCADE`: If conversation deleted, all messages deleted
- Phase 2 compatibility: No foreign keys reference Phase 3 tables

---

## Migration Strategy

### Migration Tool: Alembic

**Installation**:
```bash
pip install alembic==1.13.1
```

**Initialization** (if not already initialized):
```bash
cd backend/
alembic init migrations
```

### Migration 001: Add Conversations and Messages

**File**: `backend/migrations/versions/001_add_conversations_messages.py`

```python
"""Add conversations and messages tables

Revision ID: 001
Revises: None
Create Date: 2026-01-15

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001'
down_revision = None  # First Phase 3 migration
branch_labels = None
depends_on = None

def upgrade():
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    )
    op.create_index('idx_conversations_user_id', 'conversations', ['user_id'])
    op.create_index('idx_conversations_created_at', 'conversations', ['created_at'], postgresql_ops={'created_at': 'DESC'})

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.String(255), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('NOW()'), nullable=False),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.CheckConstraint("role IN ('user', 'assistant')", name='check_message_role'),
    )
    op.create_index('idx_messages_conversation_id', 'messages', ['conversation_id'])
    op.create_index('idx_messages_created_at', 'messages', ['created_at'])

def downgrade():
    # Drop in reverse order (messages first due to foreign key)
    op.drop_index('idx_messages_created_at', 'messages')
    op.drop_index('idx_messages_conversation_id', 'messages')
    op.drop_table('messages')

    op.drop_index('idx_conversations_created_at', 'conversations')
    op.drop_index('idx_conversations_user_id', 'conversations')
    op.drop_table('conversations')
```

### Migration Execution

**Apply Migration** (Production):
```bash
cd backend/
alembic upgrade head
```

**Rollback** (if needed):
```bash
alembic downgrade -1
```

**Check Current Version**:
```bash
alembic current
```

**Generate Migration from Models** (alternative):
```bash
alembic revision --autogenerate -m "Add conversations and messages"
# Review generated file, then apply
alembic upgrade head
```

### Safety Checks

✅ **Phase 2 Immutability**:
- No ALTER TABLE on users or tasks
- No DROP statements for Phase 2 tables
- Phase 3 tables reference Phase 2 tables via foreign keys only

✅ **Backward Compatibility**:
- Phase 2 backend can run without Phase 3 tables (no dependencies)
- Phase 3 backend requires Phase 3 tables (fails fast if missing)

✅ **Rollback Safety**:
- downgrade() provided for all migrations
- No data loss for Phase 2 (users, tasks untouched)
- Phase 3 data lost on rollback (acceptable - new feature)

✅ **Testing**:
- Test migrations on development database first
- Verify foreign keys work (create conversation → create message)
- Verify cascade deletes (delete user → conversations/messages deleted)

---

## Data Access Patterns

### Create Conversation

```python
def create_conversation(user_id: str, session: Session) -> Conversation:
    conversation = Conversation(user_id=user_id)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation
```

### Add Message

```python
def add_message(
    conversation_id: int,
    user_id: str,
    role: MessageRole,
    content: str,
    session: Session
) -> Message:
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content
    )
    session.add(message)
    session.commit()
    session.refresh(message)

    # Update conversation timestamp
    conversation = session.get(Conversation, conversation_id)
    conversation.updated_at = datetime.utcnow()
    session.add(conversation)
    session.commit()

    return message
```

### Load Conversation History

```python
def get_conversation_history(conversation_id: int, session: Session) -> List[Message]:
    messages = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    ).all()
    return messages
```

### Get User's Latest Conversation

```python
def get_latest_conversation(user_id: str, session: Session) -> Optional[Conversation]:
    conversation = session.exec(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .limit(1)
    ).first()
    return conversation
```

---

## Performance Considerations

### Indexing Strategy

**High Priority Indexes** (already included):
- `conversations.user_id`: Fetch user's conversations
- `messages.conversation_id`: Load conversation history
- `messages.created_at`: Chronological ordering

**Optional Indexes** (add if performance issues):
- `messages.user_id`: If querying all user messages across conversations
- `conversations.updated_at DESC`: For sorting recent conversations

### Query Optimization

**Conversation History Pagination**:
```python
# Load last 50 messages only (for large conversations)
recent_messages = session.exec(
    select(Message)
    .where(Message.conversation_id == conversation_id)
    .order_by(Message.created_at.desc())
    .limit(50)
).all()
recent_messages.reverse()  # Chronological order
```

**Conversation List with Message Count**:
```python
# Get conversations with message counts (if needed for UI)
from sqlalchemy import func, select

conversations_with_counts = session.exec(
    select(
        Conversation,
        func.count(Message.id).label('message_count')
    )
    .join(Message, Conversation.id == Message.conversation_id, isouter=True)
    .where(Conversation.user_id == user_id)
    .group_by(Conversation.id)
    .order_by(Conversation.updated_at.desc())
).all()
```

### Database Connection Pooling

**SQLModel Engine Configuration**:
```python
from sqlmodel import create_engine

engine = create_engine(
    DATABASE_URL,
    echo=False,  # Disable SQL logging in production
    pool_size=10,  # Max 10 connections
    max_overflow=20,  # Allow 20 overflow connections
    pool_timeout=30,  # Wait 30s for connection
    pool_recycle=3600  # Recycle connections every hour
)
```

---

## Data Model Summary

### Phase 2 (Existing - No Changes)
- ✅ Users: Authentication and identity
- ✅ Tasks: Todo items with CRUD operations

### Phase 3 (New)
- ✅ Conversations: Chat session containers
- ✅ Messages: Individual chat messages (user + assistant)

### Relationships
- User → Conversations (1:N)
- User → Messages (1:N)
- Conversation → Messages (1:N)
- User → Tasks (1:N) - Phase 2 relationship preserved

### Migration Status
- ✅ Migration script prepared (001_add_conversations_messages.py)
- ✅ Rollback supported (downgrade function)
- ✅ Phase 2 immutability maintained (no ALTER/DROP on existing tables)
- ⚠️ Ready to apply: Execute `alembic upgrade head` after deployment

**Next Phase**: API Contracts Design (contracts/)
