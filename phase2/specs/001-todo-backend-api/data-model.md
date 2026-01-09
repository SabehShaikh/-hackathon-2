# Data Model: Todo Backend API

**Feature**: 001-todo-backend-api
**Date**: 2026-01-08
**Phase**: Phase 1 - Design

## Entity Relationship Diagram

```
┌─────────────────┐
│     users       │  (Managed by Better Auth)
├─────────────────┤
│ id (PK)         │  VARCHAR(255) - UUID
│ email           │  VARCHAR(255) - UNIQUE
│ name            │  VARCHAR(255)
│ created_at      │  TIMESTAMP
└─────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────┐
│     tasks       │  (Managed by Backend API)
├─────────────────┤
│ id (PK)         │  INTEGER - AUTO INCREMENT
│ user_id (FK)    │  VARCHAR(255) → users.id [INDEXED]
│ title           │  VARCHAR(200) - NOT NULL
│ description     │  TEXT - NULLABLE
│ completed       │  BOOLEAN - DEFAULT FALSE
│ created_at      │  TIMESTAMP - DEFAULT NOW()
│ updated_at      │  TIMESTAMP - DEFAULT NOW()
└─────────────────┘
```

**Relationship**: One User has Many Tasks (1:N)

---

## Table: `tasks`

### Schema Definition

| Column       | Type         | Constraints                | Description                           |
|--------------|--------------|----------------------------|---------------------------------------|
| id           | INTEGER      | PRIMARY KEY, AUTO_INCREMENT| Unique task identifier                |
| user_id      | VARCHAR(255) | NOT NULL, FOREIGN KEY, INDEX| Owner of the task (references users.id) |
| title        | VARCHAR(200) | NOT NULL                   | Task title (1-200 characters)         |
| description  | TEXT         | NULLABLE                   | Optional task description (max 1000)  |
| completed    | BOOLEAN      | NOT NULL, DEFAULT FALSE    | Task completion status                |
| created_at   | TIMESTAMP    | NOT NULL, DEFAULT NOW()    | Task creation timestamp               |
| updated_at   | TIMESTAMP    | NOT NULL, DEFAULT NOW()    | Last modification timestamp           |

### Constraints

**Primary Key**:
- `id` - Auto-incrementing integer

**Foreign Key**:
- `user_id` REFERENCES `users(id)`
- Action on DELETE: CASCADE (if user deleted, delete their tasks)
- Action on UPDATE: CASCADE (if user ID changes, update task references)

**Unique Constraints**: None (users can have duplicate task titles)

**Check Constraints** (enforced at application level via SQLModel):
- `title` length between 1 and 200 characters
- `description` length max 1000 characters (if provided)

**Indexes**:
- PRIMARY INDEX on `id` (automatic)
- INDEX on `user_id` (explicit, for query performance)

**Rationale for user_id index**: Every query filters by user_id for data isolation. Without index, queries become O(n) table scans.

---

## SQLModel Implementation

### Task Model (models.py)

```python
from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    """
    Task entity representing a todo item.

    Attributes:
        id: Auto-generated primary key
        user_id: Owner's user ID from JWT token (FK to users.id)
        title: Task title, 1-200 characters, required
        description: Optional task description, max 1000 characters
        completed: Completion status, defaults to False
        created_at: Creation timestamp, auto-set
        updated_at: Last modification timestamp, auto-updated
    """
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        max_length=255,
        nullable=False
    )
    title: str = Field(
        min_length=1,
        max_length=200,
        nullable=False
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        nullable=True
    )
    completed: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )
```

**Notes**:
- `Optional[int]` for id: None before insertion, int after
- `default_factory=datetime.utcnow`: Generates timestamp at creation
- `index=True` on user_id: Creates database index for fast filtering
- `foreign_key="users.id"`: Enforces referential integrity

---

## Pydantic Schemas (Request/Response Models)

### TaskCreate (Request Body for POST)

```python
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    """Request body for creating a new task."""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread"
            }
        }
```

**Validation**:
- Title required, 1-200 chars
- Description optional, max 1000 chars

---

### TaskUpdate (Request Body for PUT)

```python
class TaskUpdate(BaseModel):
    """Request body for updating a task."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries and cook dinner",
                "description": "Milk, eggs, bread, chicken"
            }
        }
```

**Validation**:
- Both fields optional (update only provided fields)
- If title provided, must be 1-200 chars
- If description provided, must be max 1000 chars

---

### TaskResponse (Response Body for GET/POST/PUT/PATCH)

```python
class TaskResponse(BaseModel):
    """Response body for task operations."""
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allow creation from SQLModel
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "user-uuid-123",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "created_at": "2026-01-08T10:00:00Z",
                "updated_at": "2026-01-08T10:00:00Z"
            }
        }
```

**Notes**:
- `from_attributes=True`: Enables `.model_validate(task)` from SQLModel instance
- Includes all fields for complete task representation
- Timestamps serialized as ISO 8601 strings

---

## Table: `users` (Reference Only)

**Note**: This table is NOT created or managed by the backend API. It is created and managed by Better Auth on the frontend.

### Schema (For Reference)

| Column      | Type         | Constraints       | Description              |
|-------------|--------------|-------------------|--------------------------|
| id          | VARCHAR(255) | PRIMARY KEY       | User UUID                |
| email       | VARCHAR(255) | UNIQUE, NOT NULL  | User email address       |
| name        | VARCHAR(255) | NULLABLE          | User display name        |
| created_at  | TIMESTAMP    | NOT NULL          | User registration time   |

### Backend Relationship to Users Table

**How Backend Interacts**:
1. Backend does NOT create users table (Better Auth does)
2. Backend sets `user_id` foreign key constraint pointing to `users.id`
3. Backend trusts JWT token's `userId` claim (verified with shared secret)
4. Backend assumes user exists if JWT is valid (no user lookup needed)

**Implication**: If users table doesn't exist when tasks table is created, foreign key creation may fail. Solution: Ensure Better Auth initializes database first, or make FK optional in initial deployment.

---

## Database Initialization

### Table Creation (database.py)

```python
from sqlmodel import create_engine, SQLModel, Session
from models import Task  # Import to register table

engine = create_engine(
    settings.database_url,
    echo=True,  # Log SQL statements (disable in production)
)

def create_db_and_tables():
    """Create all tables defined in SQLModel."""
    SQLModel.metadata.create_all(engine)
```

**Called at Startup (main.py)**:

```python
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
```

**Behavior**:
- Idempotent: Safe to run multiple times
- Only creates tables that don't exist
- Does NOT alter existing tables (use Alembic for migrations)

---

## Migration Strategy

### Initial Deployment (Phase 2)

**Approach**: Use `SQLModel.metadata.create_all()`

**Pros**:
- Simple, no migration tool needed
- Fast initial deployment

**Cons**:
- Cannot handle schema changes after deployment

### Future Schema Changes (Post-Phase 2)

**Approach**: Migrate to Alembic

**Example Migration** (adding a `priority` field):

```bash
alembic revision --autogenerate -m "Add priority field"
alembic upgrade head
```

**Rationale**: Once in production with data, cannot drop/recreate tables. Alembic provides incremental migrations.

---

## Data Validation Summary

### At Database Level

- Primary key constraint on `id`
- Foreign key constraint on `user_id`
- NOT NULL constraints on `title`, `user_id`, `completed`, timestamps
- DEFAULT values on `completed` (false) and timestamps

### At Application Level (SQLModel/Pydantic)

- Title length: 1-200 characters
- Description length: max 1000 characters
- Description optional (can be None)
- completed defaults to False
- user_id extracted from JWT (always present)
- Timestamps auto-generated (not user-provided)

### Validation Flow

```
User Request
    ↓
Pydantic Model (TaskCreate/TaskUpdate)
    → Validates field types, lengths, required fields
    ↓
SQLModel (Task)
    → Enforces DB constraints, generates defaults
    ↓
PostgreSQL
    → Enforces FK, NOT NULL, data types
```

---

## Query Patterns

### List Tasks for User

```python
from sqlmodel import select

statement = select(Task).where(Task.user_id == user_id)
tasks = session.exec(statement).all()
```

**Index Used**: user_id index (fast lookup)

### Get Task by ID with Ownership Check

```python
task = session.get(Task, task_id)
if not task or task.user_id != user_id:
    raise HTTPException(status_code=404, detail="Task not found")
```

**Index Used**: Primary key index on id (O(1) lookup)

### Create Task

```python
task = Task(
    user_id=user_id,
    title=task_data.title,
    description=task_data.description,
    # completed, timestamps auto-set by defaults
)
session.add(task)
session.commit()
session.refresh(task)  # Load generated id and timestamps
return task
```

### Update Task

```python
task = session.get(Task, task_id)
if not task or task.user_id != user_id:
    raise HTTPException(status_code=404, detail="Task not found")

if task_data.title is not None:
    task.title = task_data.title
if task_data.description is not None:
    task.description = task_data.description

task.updated_at = datetime.utcnow()  # Manual timestamp update
session.add(task)
session.commit()
session.refresh(task)
return task
```

### Delete Task

```python
task = session.get(Task, task_id)
if not task or task.user_id != user_id:
    raise HTTPException(status_code=404, detail="Task not found")

session.delete(task)
session.commit()
```

**Note**: All queries include ownership check to enforce data isolation.

---

## Performance Considerations

### Expected Load (Initial)

- Users: ~100
- Tasks per user: ~50
- Total tasks: ~5,000

**Query Performance**: All queries O(log n) with indexes, acceptable performance.

### Scaling Considerations (Future)

If load increases to 10,000+ users, 500,000+ tasks:

1. **Pagination**: Add LIMIT/OFFSET to list queries
2. **Connection Pooling**: Configure pool_size in engine
3. **Read Replicas**: Use Neon read replicas for GET queries
4. **Caching**: Add Redis for frequently accessed tasks

**Not Needed Initially**: Premature optimization. Current design scales to 10k users without changes.

---

## Security: Data Isolation

### Enforcement Mechanism

**Every query MUST include**:
```python
.where(Task.user_id == user_id)
```

**Example - What NOT to do**:
```python
# INSECURE - returns task regardless of owner
task = session.get(Task, task_id)
return task
```

**Correct Pattern**:
```python
# SECURE - verifies ownership
task = session.get(Task, task_id)
if not task or task.user_id != user_id:
    raise HTTPException(status_code=404, detail="Task not found")
return task
```

**Why 404 instead of 403**: Prevents user enumeration (attacker can't discover valid task IDs).

---

## Data Model Validation Checklist

- [x] Primary key defined and auto-incrementing
- [x] Foreign key to users table with CASCADE
- [x] Index on user_id for query performance
- [x] Title validation (1-200 chars) at application level
- [x] Description validation (max 1000 chars) at application level
- [x] Default values for completed and timestamps
- [x] NOT NULL constraints on required fields
- [x] Pydantic schemas for request/response validation
- [x] Ownership check pattern documented for all queries
- [x] Security: Data isolation enforced via user_id filtering

---

## Summary

**Core Model**: Task entity with 7 fields (id, user_id, title, description, completed, created_at, updated_at)

**Validation**: Multi-layered (Pydantic → SQLModel → PostgreSQL)

**Performance**: Indexed user_id for fast filtering, primary key for direct lookups

**Security**: Ownership enforced on every query, 404 responses to prevent enumeration

**Migration**: create_all() for initial deployment, Alembic for future changes

**Constitution Compliance**: ✅ All requirements met (persistent storage, SQLModel ORM, data isolation)
