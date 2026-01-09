# API Contracts: Todo Frontend ↔ Backend Integration

**Feature**: Todo Frontend Web Application
**Date**: 2026-01-09
**Phase**: Phase 1 - Design & Contracts
**Backend Base URL**: `http://localhost:8000` (development)

## Overview

This document defines the complete API contract between the Todo Frontend and the existing Backend API (Phase 1). The frontend consumes these RESTful endpoints exclusively - no direct database access.

**Contract Principles**:
- Backend is the source of truth for all data
- Frontend never modifies backend contracts (Phase 1 is immutable)
- All communication via HTTP/JSON
- JWT tokens for authentication (Better Auth compatible)
- Standard REST conventions (GET, POST, PUT, PATCH, DELETE)

---

## Authentication Headers

All protected endpoints require a JWT token in the Authorization header.

### Header Format

```
Authorization: Bearer <JWT_TOKEN>
```

### Token Acquisition

Tokens are obtained via:
1. **POST /api/auth/login** - Returns JWT on successful login
2. **POST /api/auth/signup** - Returns JWT on successful signup

### Token Storage

- Frontend stores token in HTTP-only cookie (managed by Better Auth)
- Cookie name: `better-auth.session_token` (configurable)
- Expires: 7 days from issue
- Secure flag: true in production
- SameSite: Lax

### Token Verification

- Backend verifies token signature and expiration on every request
- Invalid/expired tokens return `401 Unauthorized`
- Frontend handles 401 by clearing session and redirecting to login

---

## Authentication Endpoints

### 1. User Signup

Create a new user account.

**Endpoint**: `POST /api/auth/signup`

**Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"  // optional
}
```

**Success Response** (201 Created):
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2026-01-09T12:00:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiresAt": "2026-01-16T12:00:00Z"
}
```

**Error Responses**:

| Status | Condition | Response Body |
|--------|-----------|---------------|
| 400 Bad Request | Invalid email format | `{ "detail": "Invalid email format" }` |
| 400 Bad Request | Password too short | `{ "detail": "Password must be at least 8 characters" }` |
| 409 Conflict | Email already exists | `{ "detail": "Email already registered" }` |
| 422 Validation Error | Missing required fields | `{ "detail": "Email and password are required" }` |

**Frontend Handling**:
- Validate email format before sending
- Validate password length (min 8 chars) before sending
- Store returned token in Better Auth session
- Redirect to /dashboard on success
- Show validation errors inline on form

---

### 2. User Login

Authenticate existing user.

**Endpoint**: `POST /api/auth/login`

**Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Success Response** (200 OK):
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2026-01-09T12:00:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiresAt": "2026-01-16T12:00:00Z"
}
```

**Error Responses**:

| Status | Condition | Response Body |
|--------|-----------|---------------|
| 401 Unauthorized | Invalid credentials | `{ "detail": "Invalid email or password" }` |
| 422 Validation Error | Missing fields | `{ "detail": "Email and password are required" }` |

**Frontend Handling**:
- Show generic error message ("Invalid email or password") for security
- Store returned token in Better Auth session
- Redirect to ?from parameter or /dashboard on success
- Clear form on error

---

### 3. User Logout

Invalidate current session.

**Endpoint**: `POST /api/auth/logout`

**Headers**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Request Body**: None

**Success Response** (200 OK):
```json
{
  "message": "Logged out successfully"
}
```

**Error Responses**:

| Status | Condition | Response Body |
|--------|-----------|---------------|
| 401 Unauthorized | Invalid/missing token | `{ "detail": "Authentication required" }` |

**Frontend Handling**:
- Clear Better Auth session locally (even if backend fails)
- Redirect to /login
- Show success toast

---

## Task Management Endpoints

All task endpoints require authentication (Authorization header with Bearer token).

### 4. List All Tasks

Fetch all tasks for the authenticated user.

**Endpoint**: `GET /api/tasks`

**Headers**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Query Parameters**: None (Phase 2 has no filtering/sorting/pagination)

**Success Response** (200 OK):
```json
[
  {
    "id": 1,
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2026-01-09T10:00:00Z",
    "updated_at": "2026-01-09T10:00:00Z"
  },
  {
    "id": 2,
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Finish project",
    "description": null,
    "completed": true,
    "created_at": "2026-01-08T15:30:00Z",
    "updated_at": "2026-01-09T09:00:00Z"
  }
]
```

**Empty State** (200 OK):
```json
[]
```

**Error Responses**:

| Status | Condition | Response Body |
|--------|-----------|---------------|
| 401 Unauthorized | Invalid/missing token | `{ "detail": "Authentication required" }` |
| 500 Internal Server Error | Database error | `{ "detail": "An unexpected error occurred" }` |

**Frontend Handling**:
- Fetch on server in dashboard page (Server Component)
- Show empty state component if array is empty
- Show loading skeleton during fetch
- Show error message with retry button on failure

---

### 5. Create Task

Create a new task for the authenticated user.

**Endpoint**: `POST /api/tasks`

**Headers**:
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"  // optional
}
```

**Success Response** (201 Created):
```json
{
  "id": 3,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-09T12:30:00Z",
  "updated_at": "2026-01-09T12:30:00Z"
}
```

**Error Responses**:

| Status | Condition | Response Body |
|--------|-----------|---------------|
| 401 Unauthorized | Invalid/missing token | `{ "detail": "Authentication required" }` |
| 422 Validation Error | Title too short | `{ "detail": "Title must be at least 1 character" }` |
| 422 Validation Error | Title too long | `{ "detail": "Title must be less than 200 characters" }` |
| 422 Validation Error | Description too long | `{ "detail": "Description must be less than 1000 characters" }` |
| 422 Validation Error | Missing title | `{ "detail": "Title is required" }` |

**Frontend Handling**:
- Validate title (1-200 chars) before sending
- Validate description (max 1000 chars) before sending
- Show inline validation errors on form
- Add returned task to local task list on success
- Close dialog on success
- Show success toast

---

### 6. Get Single Task

Fetch a specific task by ID (user ownership verified).

**Endpoint**: `GET /api/tasks/{id}`

**Headers**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Path Parameters**:
- `id` (integer): Task ID

**Success Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-09T10:00:00Z",
  "updated_at": "2026-01-09T10:00:00Z"
}
```

**Error Responses**:

| Status | Condition | Response Body |
|--------|-----------|---------------|
| 401 Unauthorized | Invalid/missing token | `{ "detail": "Authentication required" }` |
| 404 Not Found | Task doesn't exist | `{ "detail": "Task not found" }` |
| 404 Not Found | Task belongs to different user | `{ "detail": "Task not found" }` |

**Frontend Usage**:
- **Optional**: May be used to fetch task details for edit dialog
- **Alternative**: Can use task data from list endpoint (recommended)
- Not required for Phase 2 MVP

---

### 7. Update Task

Update an existing task (partial update supported).

**Endpoint**: `PUT /api/tasks/{id}`

**Headers**:
```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

**Path Parameters**:
- `id` (integer): Task ID

**Request Body** (all fields optional):
```json
{
  "title": "Buy groceries and supplies",
  "description": "Milk, eggs, bread, cleaning supplies",
  "completed": false
}
```

**Success Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries and supplies",
  "description": "Milk, eggs, bread, cleaning supplies",
  "completed": false,
  "created_at": "2026-01-09T10:00:00Z",
  "updated_at": "2026-01-09T12:45:00Z"
}
```

**Error Responses**:

| Status | Condition | Response Body |
|--------|-----------|---------------|
| 401 Unauthorized | Invalid/missing token | `{ "detail": "Authentication required" }` |
| 404 Not Found | Task doesn't exist or wrong user | `{ "detail": "Task not found" }` |
| 422 Validation Error | Title validation failed | `{ "detail": "Title must be between 1 and 200 characters" }` |
| 422 Validation Error | Description validation failed | `{ "detail": "Description must be less than 1000 characters" }` |
| 422 Validation Error | No fields provided | `{ "detail": "At least one field must be provided" }` |

**Frontend Handling**:
- Used by EditTaskDialog component
- Validate fields before sending
- Update task in local list on success
- Show validation errors inline
- Close dialog on success
- Show success toast

---

### 8. Toggle Task Completion

Toggle the completion status of a task (PATCH endpoint for partial update).

**Endpoint**: `PATCH /api/tasks/{id}/complete`

**Headers**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Path Parameters**:
- `id` (integer): Task ID

**Request Body**: None (endpoint toggles current state)

**Success Response** (200 OK):
```json
{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2026-01-09T10:00:00Z",
  "updated_at": "2026-01-09T13:00:00Z"
}
```

**Error Responses**:

| Status | Condition | Response Body |
|--------|-----------|---------------|
| 401 Unauthorized | Invalid/missing token | `{ "detail": "Authentication required" }` |
| 404 Not Found | Task doesn't exist or wrong user | `{ "detail": "Task not found" }` |

**Frontend Handling**:
- **Optimistic Update**: Update UI immediately before API call
- Used by TaskItem checkbox component
- Rollback on error and show error toast
- No success toast (instant feedback is sufficient)
- Verify returned state matches optimistic state

---

### 9. Delete Task

Permanently delete a task.

**Endpoint**: `DELETE /api/tasks/{id}`

**Headers**:
```
Authorization: Bearer <JWT_TOKEN>
```

**Path Parameters**:
- `id` (integer): Task ID

**Success Response** (204 No Content):
```
(Empty response body)
```

**Error Responses**:

| Status | Condition | Response Body |
|--------|-----------|---------------|
| 401 Unauthorized | Invalid/missing token | `{ "detail": "Authentication required" }` |
| 404 Not Found | Task doesn't exist or wrong user | `{ "detail": "Task not found" }` |

**Frontend Handling**:
- Used by DeleteConfirmDialog component
- Show confirmation dialog before calling
- Remove task from local list only after success
- Show success toast
- On error, keep task in list and show error toast
- Close dialog on success or error

---

## Error Handling Strategy

### Error Response Format

All errors follow the same JSON structure:

```json
{
  "detail": "Human-readable error message"
}
```

### HTTP Status Code Mapping

| Status Code | Frontend Action |
|-------------|----------------|
| 200 OK | Success - process response |
| 201 Created | Success - add to local state |
| 204 No Content | Success - remove from local state |
| 400 Bad Request | Show error message to user |
| 401 Unauthorized | Clear session, redirect to /login |
| 404 Not Found | Remove from local state if optimistic, show error |
| 409 Conflict | Show error message (e.g., "Email already exists") |
| 422 Validation Error | Show inline validation errors on form |
| 500 Internal Server Error | Show generic error, offer retry |
| Network Error | Show "offline" message, offer retry |

### Frontend Error Handling Implementation

```typescript
async function handleAPIError(error: unknown): Promise<void> {
  if (error instanceof APIError) {
    switch (error.status) {
      case 401:
        // Clear session and redirect
        await auth.api.signOut()
        router.push("/login?message=Session expired")
        break

      case 404:
        toast.error("Resource not found")
        break

      case 422:
        toast.error(error.message) // Show validation error
        break

      case 500:
        toast.error("Something went wrong. Please try again.")
        break

      default:
        toast.error(error.message || "An error occurred")
    }
  } else {
    // Network error or unknown error
    toast.error("Network error. Please check your connection.")
  }
}
```

---

## CORS Configuration

The backend must be configured to allow requests from the frontend origin.

### Required CORS Headers

```
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Allow-Credentials: true
```

### Frontend Implications

- Cookies (JWT tokens) are sent with credentials: "include"
- Preflight OPTIONS requests handled by backend
- Frontend runs on localhost:3000 (development)
- Backend runs on localhost:8000 (development)

---

## API Client Implementation

Frontend implements API client in `lib/api.ts`:

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

async function fetchAPI<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const token = await getAuthToken()

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...options.headers,
  }

  if (token) {
    headers["Authorization"] = `Bearer ${token}`
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
    credentials: "include", // Send cookies
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Unknown error" }))
    throw new APIError(response.status, error.detail)
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return undefined as T
  }

  return response.json()
}
```

---

## Rate Limiting & Performance

### Expected Response Times

| Endpoint | Expected Response Time |
|----------|----------------------|
| GET /api/tasks | < 500ms |
| POST /api/tasks | < 300ms |
| PUT /api/tasks/{id} | < 300ms |
| PATCH /api/tasks/{id}/complete | < 200ms |
| DELETE /api/tasks/{id} | < 200ms |
| POST /api/auth/login | < 500ms |
| POST /api/auth/signup | < 800ms (includes password hashing) |

### Frontend Timeout Strategy

- Default timeout: 10 seconds (network errors likely after this)
- Show loading indicator after 200ms (prevent flash for fast responses)
- Allow user to cancel long-running requests

### Rate Limiting

- Backend may implement rate limiting (not specified in Phase 1)
- Frontend should handle 429 Too Many Requests gracefully
- Show "Too many requests. Please wait and try again." message

---

## Contract Validation

### Frontend Responsibilities

- ✅ Send requests in correct format (JSON, headers, auth token)
- ✅ Validate input before sending (client-side validation)
- ✅ Handle all documented error responses
- ✅ Respect backend data types and constraints
- ❌ **NEVER** modify backend API contracts

### Backend Responsibilities (Phase 1)

- ✅ Implement all documented endpoints
- ✅ Validate all inputs on server side
- ✅ Enforce user ownership (user_id from JWT)
- ✅ Return consistent error format
- ✅ Include CORS headers for frontend origin

### Contract Testing

Frontend should test:
1. **Happy Paths**: All endpoints work with valid data
2. **Error Paths**: All error codes are handled correctly
3. **Authentication**: 401 errors trigger logout
4. **Validation**: 422 errors show inline messages
5. **Network Errors**: Offline scenarios handled gracefully

---

## Summary

**Total Endpoints**: 9 (3 auth + 6 tasks)
**Authentication**: JWT token in Authorization header
**Data Format**: JSON request/response
**Error Format**: `{ "detail": string }`
**Frontend Base URL**: http://localhost:3000
**Backend Base URL**: http://localhost:8000

**Next Steps**:
1. Generate quickstart.md with setup instructions
2. Update agent context with API patterns
3. Generate tasks.md for implementation (Phase 2)
