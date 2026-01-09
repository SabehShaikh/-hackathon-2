# Feature Specification: Todo Backend API

**Feature Branch**: `001-todo-backend-api`
**Created**: 2026-01-08
**Status**: Draft
**Input**: RESTful API for todo task management with authentication, database integration, and CRUD operations

## User Scenarios & Testing

### User Story 1 - Task Listing (Priority: P1)

As an authenticated user, I want to retrieve all my tasks so I can see what I need to do.

**Why this priority**: Core read operation - must work before any other feature. Forms the foundation for UI display.

**Independent Test**: Can be fully tested by authenticating a user, creating tasks via database seeding, calling GET /api/tasks, and verifying only that user's tasks are returned.

**Acceptance Scenarios**:

1. **Given** I am authenticated with a valid JWT token, **When** I request GET /api/tasks, **Then** I receive a 200 OK with an array of all my tasks
2. **Given** I am authenticated and have no tasks, **When** I request GET /api/tasks, **Then** I receive a 200 OK with an empty array
3. **Given** I am not authenticated (no token), **When** I request GET /api/tasks, **Then** I receive a 401 Unauthorized
4. **Given** I am authenticated, **When** I request GET /api/tasks, **Then** I do not see tasks belonging to other users

---

### User Story 2 - Task Creation (Priority: P1)

As an authenticated user, I want to create new tasks so I can track what I need to do.

**Why this priority**: Essential write operation - required for MVP. Users cannot use the app without being able to add tasks.

**Independent Test**: Can be fully tested by authenticating, sending POST /api/tasks with valid data, and verifying the task is created with correct attributes and ownership.

**Acceptance Scenarios**:

1. **Given** I am authenticated, **When** I POST /api/tasks with valid title, **Then** I receive a 201 Created with the created task object including auto-generated ID and timestamps
2. **Given** I am authenticated, **When** I POST /api/tasks with title and description, **Then** both fields are saved correctly
3. **Given** I am authenticated, **When** I POST /api/tasks without a title, **Then** I receive a 422 Unprocessable Entity with validation error
4. **Given** I am authenticated, **When** I POST /api/tasks with title exceeding 200 chars, **Then** I receive a 422 Unprocessable Entity
5. **Given** I am not authenticated, **When** I POST /api/tasks, **Then** I receive a 401 Unauthorized
6. **Given** I create a task, **When** I retrieve it, **Then** completed defaults to false and user_id is set to my user ID

---

### User Story 3 - Task Retrieval by ID (Priority: P2)

As an authenticated user, I want to retrieve a specific task by ID so I can view its details.

**Why this priority**: Important for viewing single task details but can work independently after P1 stories are complete.

**Independent Test**: Can be fully tested by creating a task, then calling GET /api/tasks/{id} and verifying the correct task is returned with ownership validation.

**Acceptance Scenarios**:

1. **Given** I am authenticated and a task with ID exists and belongs to me, **When** I GET /api/tasks/{id}, **Then** I receive a 200 OK with the task object
2. **Given** I am authenticated, **When** I GET /api/tasks/{id} for a non-existent task, **Then** I receive a 404 Not Found
3. **Given** I am authenticated, **When** I GET /api/tasks/{id} for a task belonging to another user, **Then** I receive a 404 Not Found (not 403, to prevent user enumeration)
4. **Given** I am not authenticated, **When** I GET /api/tasks/{id}, **Then** I receive a 401 Unauthorized

---

### User Story 4 - Task Update (Priority: P2)

As an authenticated user, I want to update my task's title and description so I can keep my tasks accurate.

**Why this priority**: Editing is important but users can work around it temporarily by deleting and recreating tasks.

**Independent Test**: Can be fully tested by creating a task, then calling PUT /api/tasks/{id} with updated data and verifying the changes are persisted with updated timestamp.

**Acceptance Scenarios**:

1. **Given** I am authenticated and own a task, **When** I PUT /api/tasks/{id} with updated title, **Then** I receive a 200 OK with the updated task and updated_at timestamp changes
2. **Given** I am authenticated and own a task, **When** I PUT /api/tasks/{id} with updated description, **Then** the description is updated
3. **Given** I am authenticated, **When** I PUT /api/tasks/{id} with invalid data (e.g., title too long), **Then** I receive a 422 Unprocessable Entity
4. **Given** I am authenticated, **When** I PUT /api/tasks/{id} for a task I don't own, **Then** I receive a 404 Not Found
5. **Given** I am not authenticated, **When** I PUT /api/tasks/{id}, **Then** I receive a 401 Unauthorized

---

### User Story 5 - Task Completion Toggle (Priority: P2)

As an authenticated user, I want to mark tasks as complete or incomplete so I can track my progress.

**Why this priority**: Core functionality for a todo app but can be implemented after basic CRUD. Provides clear value increment.

**Independent Test**: Can be fully tested by creating a task (completed=false), calling PATCH /api/tasks/{id}/complete, and verifying the completed status toggles with updated timestamp.

**Acceptance Scenarios**:

1. **Given** I am authenticated and own an incomplete task, **When** I PATCH /api/tasks/{id}/complete, **Then** completed becomes true and updated_at changes
2. **Given** I am authenticated and own a completed task, **When** I PATCH /api/tasks/{id}/complete, **Then** completed becomes false and updated_at changes
3. **Given** I am authenticated, **When** I PATCH /api/tasks/{id}/complete for a task I don't own, **Then** I receive a 404 Not Found
4. **Given** I am not authenticated, **When** I PATCH /api/tasks/{id}/complete, **Then** I receive a 401 Unauthorized

---

### User Story 6 - Task Deletion (Priority: P3)

As an authenticated user, I want to delete tasks I no longer need so I can keep my task list clean.

**Why this priority**: Nice to have but least critical - users can work around by marking tasks complete. Provides cleanup functionality.

**Independent Test**: Can be fully tested by creating a task, calling DELETE /api/tasks/{id}, and verifying the task no longer exists and 204 No Content is returned.

**Acceptance Scenarios**:

1. **Given** I am authenticated and own a task, **When** I DELETE /api/tasks/{id}, **Then** I receive a 204 No Content and the task is removed
2. **Given** I am authenticated and deleted a task, **When** I try to GET /api/tasks/{id}, **Then** I receive a 404 Not Found
3. **Given** I am authenticated, **When** I DELETE /api/tasks/{id} for a task I don't own, **Then** I receive a 404 Not Found
4. **Given** I am not authenticated, **When** I DELETE /api/tasks/{id}, **Then** I receive a 401 Unauthorized
5. **Given** I DELETE /api/tasks/{id} for a non-existent task, **When** I am authenticated, **Then** I receive a 404 Not Found

---

### Edge Cases

- What happens when JWT token is expired? System returns 401 Unauthorized with appropriate error message
- What happens when JWT token is malformed or has invalid signature? System returns 401 Unauthorized
- What happens when database connection fails? System returns 500 Internal Server Error with generic error message (don't expose DB details)
- What happens when user_id from JWT doesn't exist in users table? Request proceeds normally (users table managed by Better Auth, backend trusts JWT)
- What happens when task ID is invalid format (e.g., string instead of integer)? FastAPI returns 422 Unprocessable Entity
- What happens when description exceeds 1000 characters? System returns 422 Unprocessable Entity with validation error
- What happens when request is missing Authorization header? System returns 401 Unauthorized
- What happens when CORS preflight OPTIONS request is made? System returns 200 OK with appropriate CORS headers

## Requirements

### Functional Requirements

- **FR-001**: System MUST connect to Neon Serverless PostgreSQL using DATABASE_URL environment variable
- **FR-002**: System MUST use SQLModel ORM for all database operations (no raw SQL)
- **FR-003**: System MUST auto-create tasks table on startup if it doesn't exist
- **FR-004**: System MUST verify JWT tokens from Authorization header using BETTER_AUTH_SECRET
- **FR-005**: System MUST extract user_id from JWT token payload for all authenticated requests
- **FR-006**: System MUST return 401 Unauthorized for missing, invalid, or expired JWT tokens
- **FR-007**: System MUST filter all task queries by authenticated user's user_id
- **FR-008**: System MUST validate task title length (1-200 characters)
- **FR-009**: System MUST validate task description length (max 1000 characters)
- **FR-010**: System MUST set completed=false by default for new tasks
- **FR-011**: System MUST auto-generate created_at and updated_at timestamps
- **FR-012**: System MUST update updated_at timestamp on task modifications
- **FR-013**: System MUST return 404 Not Found when task doesn't exist or belongs to different user
- **FR-014**: System MUST return 422 Unprocessable Entity for validation errors with error details
- **FR-015**: System MUST configure CORS to allow requests from ALLOWED_ORIGINS
- **FR-016**: System MUST allow credentials in CORS configuration
- **FR-017**: System MUST return JSON responses for all endpoints
- **FR-018**: System MUST NOT require authentication for health check endpoint (if implemented)

### Key Entities

- **Task**: Represents a todo item with title, optional description, completion status, ownership, and timestamps. Relationships: belongs to one User (via user_id foreign key). Auto-generated ID, auto-managed timestamps.

- **User**: Represents an authenticated user. Managed by Better Auth (external to backend). Backend references User via user_id string extracted from JWT token. No direct user management in backend.

## Success Criteria

### Measurable Outcomes

- **SC-001**: All 6 API endpoints (GET list, POST create, GET by ID, PUT update, PATCH complete, DELETE) return correct status codes and data
- **SC-002**: Users can only access and modify their own tasks (data isolation verified)
- **SC-003**: Invalid or missing JWT tokens result in 401 Unauthorized (authentication enforced)
- **SC-004**: Input validation rejects invalid data with 422 status and descriptive error messages
- **SC-005**: Database operations use SQLModel exclusively (no raw SQL in codebase)
- **SC-006**: CORS configured correctly (frontend origin allowed, credentials permitted)
- **SC-007**: All environment variables externalized (no hardcoded secrets in code)
- **SC-008**: Code follows FastAPI best practices (type hints, Pydantic models, dependency injection)
- **SC-009**: API response time < 500ms for typical operations (P95 latency)
- **SC-010**: Errors return appropriate HTTP status codes with JSON error messages

## API Contracts

### Authentication

All endpoints except health check require:
- Header: `Authorization: Bearer <jwt_token>`
- JWT must be valid and signed with BETTER_AUTH_SECRET
- JWT payload must contain `userId` field

### Endpoints

#### GET /api/tasks

**Request**:
```
GET /api/tasks
Authorization: Bearer <jwt_token>
```

**Response 200**:
```json
[
  {
    "id": 1,
    "user_id": "user-uuid-123",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-01-08T10:00:00Z",
    "updated_at": "2026-01-08T10:00:00Z"
  }
]
```

**Response 401**: `{"detail": "Unauthorized"}`

---

#### POST /api/tasks

**Request**:
```json
POST /api/tasks
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"  // optional
}
```

**Response 201**:
```json
{
  "id": 1,
  "user_id": "user-uuid-123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-08T10:00:00Z",
  "updated_at": "2026-01-08T10:00:00Z"
}
```

**Response 422**: `{"detail": [{"loc": ["body", "title"], "msg": "field required"}]}`

---

#### GET /api/tasks/{id}

**Request**:
```
GET /api/tasks/1
Authorization: Bearer <jwt_token>
```

**Response 200**:
```json
{
  "id": 1,
  "user_id": "user-uuid-123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-08T10:00:00Z",
  "updated_at": "2026-01-08T10:00:00Z"
}
```

**Response 404**: `{"detail": "Task not found"}`

---

#### PUT /api/tasks/{id}

**Request**:
```json
PUT /api/tasks/1
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "title": "Buy groceries and cook",
  "description": "Milk, eggs, bread, chicken"
}
```

**Response 200**: Returns updated task object (same structure as GET)

**Response 404**: `{"detail": "Task not found"}`

**Response 422**: `{"detail": [{"loc": ["body", "title"], "msg": "ensure this value has at most 200 characters"}]}`

---

#### PATCH /api/tasks/{id}/complete

**Request**:
```
PATCH /api/tasks/1/complete
Authorization: Bearer <jwt_token>
```

**Response 200**: Returns task object with toggled `completed` status

**Response 404**: `{"detail": "Task not found"}`

---

#### DELETE /api/tasks/{id}

**Request**:
```
DELETE /api/tasks/1
Authorization: Bearer <jwt_token>
```

**Response 204**: No content (successful deletion)

**Response 404**: `{"detail": "Task not found"}`

---

## Technology Constraints

- **Language**: Python 3.13+
- **Framework**: FastAPI
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **JWT Library**: python-jose[cryptography]
- **Server**: Uvicorn (ASGI)
- **Environment**: python-dotenv for environment variables

## Security Requirements

- **SEC-001**: All secrets MUST be stored in environment variables (DATABASE_URL, BETTER_AUTH_SECRET, ALLOWED_ORIGINS)
- **SEC-002**: JWT tokens MUST be verified on every authenticated request
- **SEC-003**: Database queries MUST use SQLModel parameterization (prevent SQL injection)
- **SEC-004**: Error messages MUST NOT expose internal implementation details or database structure
- **SEC-005**: User data MUST be isolated (users cannot access other users' tasks)
- **SEC-006**: CORS MUST be restrictive (only allow specified origins)
- **SEC-007**: .env file MUST be in .gitignore (never committed to version control)
- **SEC-008**: HTTPS MUST be enforced in production (configured at deployment level)

## Out of Scope

The following are explicitly NOT part of this feature:

- User registration and login endpoints (handled by Better Auth on frontend)
- Password hashing and user authentication logic (Better Auth responsibility)
- Session management (JWT is stateless)
- Frontend UI components
- Task priorities, tags, categories, or due dates (future Phase 5)
- Task search, filtering, or sorting (future Phase 5)
- Task sharing between users
- Real-time updates or WebSockets
- File attachments
- Email notifications
- Rate limiting or API throttling
- API versioning (future consideration)
- Pagination for task lists (future optimization)

## Data Model

### Tasks Table

Managed by backend using SQLModel:

```
tasks
├── id: INTEGER PRIMARY KEY AUTOINCREMENT
├── user_id: VARCHAR(255) NOT NULL FOREIGN KEY → users.id
├── title: VARCHAR(200) NOT NULL
├── description: TEXT NULL
├── completed: BOOLEAN DEFAULT FALSE NOT NULL
├── created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
└── updated_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL
```

**Indexes**:
- PRIMARY KEY on id
- INDEX on user_id (for efficient filtering)

**Constraints**:
- user_id references users.id (managed by Better Auth)
- title NOT NULL, length 1-200
- description NULL, max length 1000
- completed defaults to false

### Users Table

Managed by Better Auth (external to backend):

```
users
├── id: VARCHAR(255) PRIMARY KEY (UUID)
├── email: VARCHAR(255) UNIQUE NOT NULL
├── name: VARCHAR(255)
└── created_at: TIMESTAMP
```

Backend does not create or manage this table, but references users.id via foreign key.

## Environment Variables

Required in `.env` file:

```
DATABASE_URL=postgresql://user:pass@host/dbname
BETTER_AUTH_SECRET=your-shared-secret-key
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend.com
```

## Dependencies

From `requirements.txt`:

```
fastapi==0.109.0
sqlmodel==0.0.14
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
python-dotenv==1.0.0
uvicorn[standard]==0.27.0
```

## Project Structure

```
backend/
├── main.py              # FastAPI app, CORS, startup, health check
├── models.py            # SQLModel Task model definition
├── database.py          # Database connection, engine, session management
├── auth.py              # JWT verification middleware/dependency
├── routes/
│   └── tasks.py         # Task CRUD endpoint implementations
├── .env                 # Environment variables (git-ignored)
├── .env.example         # Template for .env (committed)
├── requirements.txt     # Python dependencies
└── README.md            # Setup and running instructions
```

## Acceptance Criteria Checklist

Before marking this feature complete, verify:

- [ ] All 6 API endpoints implemented and working
- [ ] JWT authentication enforced on all task endpoints
- [ ] User data isolation verified (users see only their own tasks)
- [ ] Input validation working (title, description length constraints)
- [ ] Proper HTTP status codes returned (200, 201, 204, 401, 404, 422, 500)
- [ ] Error responses return JSON with descriptive messages
- [ ] CORS configured correctly (frontend origin allowed)
- [ ] Database connection works with Neon PostgreSQL
- [ ] All database operations use SQLModel (no raw SQL)
- [ ] Environment variables externalized (no hardcoded secrets)
- [ ] .env.example file created with template
- [ ] .env file in .gitignore
- [ ] README.md with setup instructions written
- [ ] Code follows FastAPI best practices (type hints, dependency injection)
- [ ] Timestamps (created_at, updated_at) auto-managed correctly
- [ ] Foreign key constraint to users table configured
- [ ] Constitution principles followed (API-first, security by default, SDD)

## Notes

- Backend is stateless - no session storage required
- Frontend will handle user registration/login via Better Auth
- Backend trusts JWT tokens verified with shared secret
- Task ownership is enforced at the database query level
- Users table is not directly accessed by backend (managed by Better Auth)
- Health check endpoint (if added) should be at GET /api/health and not require auth
