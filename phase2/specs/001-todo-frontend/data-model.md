# Data Model: Todo Frontend State Management

**Feature**: Todo Frontend Web Application
**Date**: 2026-01-09
**Phase**: Phase 1 - Design & Contracts

## Overview

This document defines the frontend data models, state management strategy, and data flow patterns for the Todo Frontend Web Application. The frontend maintains minimal local state and relies primarily on the backend as the source of truth.

---

## State Management Strategy

### Architecture Decision
**Approach**: Server-first with selective client state

**Rationale**:
- Next.js App Router encourages Server Components by default
- Backend is already the source of truth (PostgreSQL database)
- Minimize client-side state complexity
- Leverage React Server Components for automatic data fetching

**State Categories**:

1. **Server State** (fetched from backend, displayed in Server Components)
   - Task list
   - User profile data
   - Initial page loads

2. **Client State** (managed in Client Components)
   - Form inputs (create/edit dialogs)
   - Optimistic UI updates (task toggle)
   - UI state (dialog open/closed, loading indicators)

3. **Persistent Client State** (localStorage/cookies)
   - Theme preference (light/dark/system)
   - Session token (HTTP-only cookie, managed by Better Auth)

4. **Transient State** (temporary, not persisted)
   - Loading indicators
   - Error messages
   - Toast notifications

---

## Core Data Models

### 1. User Model

Represents an authenticated user in the application.

```typescript
interface User {
  id: string               // UUID from backend
  email: string            // User's email address (unique)
  name: string | null      // Optional display name
  created_at: string       // ISO 8601 timestamp
}
```

**Source**: Backend API (via Better Auth integration)

**Frontend Usage**:
- Displayed in navbar/profile section
- Used for greeting messages
- Not editable in Phase 2 (out of scope)

**Validation**:
- Email format validated by backend during signup
- Name optional, max 100 characters (backend enforced)

---

### 2. Task Model

Represents a single todo task item.

```typescript
interface Task {
  id: number                // Auto-increment ID from backend
  user_id: string           // Owner's user ID (not displayed to user)
  title: string             // Task title (1-200 chars)
  description: string | null // Optional description (max 1000 chars)
  completed: boolean        // Completion status
  created_at: string        // ISO 8601 timestamp (when task was created)
  updated_at: string        // ISO 8601 timestamp (last modification)
}
```

**Source**: Backend API (`/api/tasks`)

**Frontend Usage**:
- Displayed in TaskList component
- Editable via EditTaskDialog
- Toggleable via checkbox (optimistic update)
- Deletable via DeleteConfirmDialog

**Validation Rules** (enforced both client and server):
- `title`: Required, 1-200 characters, trimmed
- `description`: Optional, max 1000 characters, nullable
- `completed`: Boolean, defaults to false on creation
- `user_id`: Automatically set by backend from JWT token
- `id`, `created_at`, `updated_at`: Set by backend, read-only

**Frontend-Specific Fields**:
```typescript
interface TaskUIState extends Task {
  isOptimisticallyCompleted?: boolean  // For optimistic updates
  isPending?: boolean                   // For loading states
  error?: string | null                 // For error states
}
```

---

### 3. Session Model

Represents an authenticated user session.

```typescript
interface Session {
  user: User               // Authenticated user object
  token: string            // JWT token (stored in HTTP-only cookie)
  expiresAt: Date          // Session expiration (7 days from creation)
}
```

**Source**: Better Auth library

**Frontend Usage**:
- Checked in middleware for route protection
- Used in API client for Authorization headers
- Displayed in navbar (user email/name)

**Lifecycle**:
- Created on successful login/signup
- Stored in HTTP-only cookie (managed by Better Auth)
- Expires after 7 days or manual logout
- Automatically validated on each request via middleware

---

### 4. Theme Preference Model

Represents user's theme preference.

```typescript
type ThemeMode = "light" | "dark" | "system"

interface ThemePreference {
  mode: ThemeMode          // Current theme selection
  systemPreference: "light" | "dark"  // OS-level preference
}
```

**Source**: Browser localStorage (managed by next-themes)

**Frontend Usage**:
- Controls CSS class on <html> element
- Displayed in ThemeToggle component
- Persists across sessions

**Default**: "system" (respects OS preference)

---

## Request/Response Models

### 5. Create Task Request

```typescript
interface CreateTaskRequest {
  title: string            // Required, 1-200 chars
  description?: string     // Optional, max 1000 chars
}
```

**API Endpoint**: `POST /api/tasks`

**Response**: `Task` object (with id, timestamps, user_id populated by backend)

**Frontend Validation**:
- Title: Required, trimmed, 1-200 characters
- Description: Optional, trimmed, max 1000 characters

---

### 6. Update Task Request

```typescript
interface UpdateTaskRequest {
  title?: string           // Optional, 1-200 chars if provided
  description?: string     // Optional, max 1000 chars if provided, null to clear
  completed?: boolean      // Optional, update completion status
}
```

**API Endpoint**: `PUT /api/tasks/{id}`

**Response**: Updated `Task` object

**Frontend Validation**:
- At least one field must be provided
- If title provided: 1-200 characters
- If description provided: max 1000 characters

---

### 7. API Error Response

```typescript
interface APIError {
  detail: string           // Human-readable error message
  status?: number          // HTTP status code (optional)
}
```

**Common Error Responses**:
- `401 Unauthorized`: "Authentication required" or "Invalid token"
- `404 Not Found`: "Task not found"
- `422 Validation Error`: "Title must be between 1 and 200 characters"
- `500 Internal Server Error`: "An unexpected error occurred"

**Frontend Handling**:
- Parse error.detail and display in toast notification
- 401 errors trigger redirect to login page
- 404 errors remove task from local state (if optimistic update)
- Validation errors display inline on form fields

---

## State Flow Diagrams

### Task Creation Flow

```
User clicks "Create Task"
    ↓
Open CreateTaskDialog (local state: open=true)
    ↓
User enters title/description (local state: form values)
    ↓
User clicks "Submit"
    ↓
Set loading state (local state: isLoading=true)
    ↓
Call API: POST /api/tasks
    ↓
    ├─ Success:
    │    ↓
    │  Add task to local list (server state updated)
    │    ↓
    │  Show success toast
    │    ↓
    │  Close dialog
    │
    └─ Error:
         ↓
       Show error toast
         ↓
       Keep dialog open with user input
         ↓
       Set loading state (isLoading=false)
```

### Task Toggle Flow (Optimistic Update)

```
User clicks checkbox
    ↓
Update local state immediately (optimistic update)
    ↓
Show new state in UI (<100ms)
    ↓
Call API: PATCH /api/tasks/{id}/complete
    ↓
    ├─ Success:
    │    ↓
    │  Verify server state matches optimistic state
    │    ↓
    │  Show success toast
    │
    └─ Error:
         ↓
       Rollback to previous state
         ↓
       Show error toast
         ↓
       User can retry
```

### Session Expiry Flow

```
User makes API request
    ↓
API returns 401 Unauthorized
    ↓
Clear session from Better Auth
    ↓
Redirect to /login with ?from={current_path}
    ↓
Show message: "Your session has expired. Please log in again."
    ↓
User logs in
    ↓
Redirect to original page ({from} parameter)
```

---

## Data Fetching Patterns

### Server Component Pattern (Initial Load)

```typescript
// app/dashboard/page.tsx (Server Component)
import { auth } from "@/lib/auth"
import { tasksAPI } from "@/lib/api"
import { TaskList } from "@/components/tasks/TaskList"
import { headers } from "next/headers"

export default async function DashboardPage() {
  // Check authentication
  const session = await auth.api.getSession({
    headers: await headers()
  })

  if (!session) {
    redirect("/login")
  }

  // Fetch tasks on server
  const tasks = await tasksAPI.list()

  // Pass to client component
  return <TaskList initialTasks={tasks} />
}
```

### Client Component Pattern (Mutations)

```typescript
// components/tasks/CreateTaskDialog.tsx (Client Component)
"use client"
import { useState } from "react"
import { tasksAPI } from "@/lib/api"
import { toast } from "sonner"

export function CreateTaskDialog({ onTaskCreated }: Props) {
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      const newTask = await tasksAPI.create({ title, description })
      toast.success("Task created!")
      onTaskCreated(newTask)
    } catch (error) {
      toast.error(error.message || "Failed to create task")
    } finally {
      setIsLoading(false)
    }
  }

  return (/* form JSX */)
}
```

---

## Type Definitions File Structure

**File**: `lib/types.ts`

```typescript
// ===== Core Domain Models =====

export interface User {
  id: string
  email: string
  name: string | null
  created_at: string
}

export interface Task {
  id: number
  user_id: string
  title: string
  description: string | null
  completed: boolean
  created_at: string
  updated_at: string
}

export interface Session {
  user: User
  token: string
  expiresAt: Date
}

// ===== Request Models =====

export interface CreateTaskRequest {
  title: string
  description?: string
}

export interface UpdateTaskRequest {
  title?: string
  description?: string
  completed?: boolean
}

export interface LoginRequest {
  email: string
  password: string
}

export interface SignupRequest {
  email: string
  password: string
  name?: string
}

// ===== Response Models =====

export interface APIError {
  detail: string
  status?: number
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  pageSize: number
}
// Note: Not used in Phase 2, but prepared for future pagination

// ===== UI-Specific Models =====

export interface TaskUIState extends Task {
  isOptimisticallyCompleted?: boolean
  isPending?: boolean
  error?: string | null
}

export type ThemeMode = "light" | "dark" | "system"

export interface ThemePreference {
  mode: ThemeMode
  systemPreference: "light" | "dark"
}

// ===== Form Models =====

export interface TaskFormData {
  title: string
  description: string
}

export interface LoginFormData {
  email: string
  password: string
}

export interface SignupFormData {
  email: string
  password: string
  confirmPassword: string
}

// ===== Component Props Types =====

export interface TaskItemProps {
  task: Task
  onToggle: (id: number) => Promise<void>
  onEdit: (task: Task) => void
  onDelete: (id: number) => Promise<void>
}

export interface TaskListProps {
  initialTasks: Task[]
}

export interface DialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}
```

---

## Validation Rules Reference

### Client-Side Validation (Mirrors Backend)

| Field | Rule | Error Message |
|-------|------|---------------|
| task.title | Required | "Title is required" |
| task.title | Min 1 char | "Title must be at least 1 character" |
| task.title | Max 200 chars | "Title must be less than 200 characters" |
| task.description | Max 1000 chars | "Description must be less than 1000 characters" |
| user.email | Valid email format | "Please enter a valid email address" |
| user.password | Min 8 chars | "Password must be at least 8 characters" |
| signup.confirmPassword | Matches password | "Passwords do not match" |

**Note**: Backend is the authoritative source for validation. Client-side validation provides immediate feedback but backend errors take precedence.

---

## Summary

**Frontend State Strategy**: Server-first with minimal client state
**Primary Data Models**: User, Task, Session, ThemePreference
**State Management**: React Server Components + useState for client interactions
**Data Flow**: Fetch on server → Pass to client → Mutate with optimistic updates
**Type Safety**: Full TypeScript coverage in `lib/types.ts`

**Next Steps**: Define API contracts in `contracts/api-contracts.md`
