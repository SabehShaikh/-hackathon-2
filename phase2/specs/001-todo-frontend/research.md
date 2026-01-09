# Research: Todo Frontend Technology Decisions

**Feature**: Todo Frontend Web Application
**Date**: 2026-01-09
**Phase**: Phase 0 - Research & Technology Selection

## Overview

This document captures all technology decisions, research findings, and implementation patterns for the Todo Frontend Web Application. Each decision includes rationale, alternatives considered, and implementation guidance.

---

## 1. Better Auth + Next.js 16 App Router Integration

### Decision
Use Better Auth library with JWT plugin for authentication, integrated with Next.js 16 App Router using Server Actions and middleware.

### Rationale
- **JWT Support**: Better Auth provides built-in JWT token generation and verification
- **App Router Compatible**: Designed to work with Next.js 13+ App Router patterns
- **Minimal Configuration**: Simple setup compared to alternatives
- **Backend Integration**: Works seamlessly with backend JWT verification
- **Session Management**: Handles secure cookie-based sessions out of the box
- **Type-Safe**: Full TypeScript support

### Alternatives Considered

**NextAuth.js (Auth.js)**
- ❌ More complex configuration for simple JWT use case
- ❌ Heavier dependency with more features than needed
- ✅ More mature ecosystem and documentation
- **Rejected**: Overkill for our JWT-only requirement

**Custom JWT Implementation**
- ✅ Full control over implementation
- ❌ Must implement security features manually
- ❌ Higher risk of security vulnerabilities
- ❌ More time to implement and test
- **Rejected**: Reinventing the wheel, security risk

**Auth0 / Clerk**
- ✅ Fully managed auth service
- ❌ External dependency and cost
- ❌ Overkill for simple email/password auth
- **Rejected**: Unnecessary complexity for self-hosted backend

### Implementation Pattern

**Configuration** (`lib/auth.ts`):
```typescript
import { betterAuth } from "better-auth"
import { jwt } from "better-auth/plugins"

export const auth = betterAuth({
  database: {
    // Connect to backend for user data
    provider: "custom",
    url: process.env.NEXT_PUBLIC_API_URL
  },
  plugins: [
    jwt({
      secret: process.env.BETTER_AUTH_SECRET!,
      expiresIn: "7d"
    })
  ],
  session: {
    cookieCache: {
      enabled: true,
      maxAge: 7 * 24 * 60 * 60 // 7 days
    }
  }
})
```

**Server Component Usage**:
```typescript
import { auth } from "@/lib/auth"

export default async function DashboardPage() {
  const session = await auth.api.getSession({
    headers: await headers()
  })

  if (!session) {
    redirect("/login")
  }

  return <TaskList userId={session.user.id} />
}
```

**Client Component Usage**:
```typescript
"use client"
import { useSession } from "@/lib/auth/client"

export function UserProfile() {
  const { data: session, isLoading } = useSession()

  if (isLoading) return <Spinner />
  if (!session) return <LoginButton />

  return <div>Welcome, {session.user.email}</div>
}
```

### Key Gotchas
- Must configure BETTER_AUTH_SECRET environment variable
- HTTP-only cookies require proper CORS setup with backend
- Server components can access session directly, client components need hooks
- Middleware runs on every request - keep it lightweight

---

## 2. API Client Architecture

### Decision
Centralized fetch wrapper in `lib/api.ts` with automatic JWT injection, type-safe request/response handling, and comprehensive error management.

### Rationale
- **Single Source of Truth**: All API calls go through one place
- **Auth Token Management**: Automatic Bearer token injection
- **Type Safety**: TypeScript interfaces for all endpoints
- **Error Handling**: Consistent error parsing and user-friendly messages
- **Retry Logic**: Optional retry for transient failures
- **Testability**: Easy to mock for testing

### Alternatives Considered

**TanStack Query (React Query)**
- ✅ Built-in caching, refetching, optimistic updates
- ✅ Great DevTools experience
- ❌ Additional dependency and learning curve
- ❌ Overkill for simple CRUD operations
- **Partially Adopted**: May use for complex data fetching later, but start with simple fetch wrapper

**SWR (Vercel)**
- ✅ Lightweight, built for Next.js
- ✅ Automatic revalidation
- ❌ Still requires custom fetcher function
- **Deferred**: Can migrate to SWR later if needed

**Axios**
- ✅ Feature-rich HTTP client
- ✅ Request/response interceptors
- ❌ Additional dependency when fetch API is sufficient
- **Rejected**: Native fetch is sufficient for our needs

### Implementation Pattern

**Type Definitions** (`lib/types.ts`):
```typescript
export interface Task {
  id: number
  user_id: string
  title: string
  description: string | null
  completed: boolean
  created_at: string
  updated_at: string
}

export interface CreateTaskRequest {
  title: string
  description?: string
}

export interface UpdateTaskRequest {
  title?: string
  description?: string
  completed?: boolean
}

export interface APIError {
  detail: string
}
```

**API Client** (`lib/api.ts`):
```typescript
import { auth } from "./auth"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

class APIError extends Error {
  constructor(public status: number, message: string) {
    super(message)
    this.name = "APIError"
  }
}

async function getAuthToken(): Promise<string | null> {
  const session = await auth.api.getSession({
    headers: await headers()
  })
  return session?.token || null
}

async function fetchAPI<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
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
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Unknown error" }))
    throw new APIError(response.status, error.detail)
  }

  return response.json()
}

// Task API Functions
export const tasksAPI = {
  list: () => fetchAPI<Task[]>("/api/tasks"),

  create: (data: CreateTaskRequest) =>
    fetchAPI<Task>("/api/tasks", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  update: (id: number, data: UpdateTaskRequest) =>
    fetchAPI<Task>(`/api/tasks/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  toggleComplete: (id: number) =>
    fetchAPI<Task>(`/api/tasks/${id}/complete`, {
      method: "PATCH",
    }),

  delete: (id: number) =>
    fetchAPI<void>(`/api/tasks/${id}`, {
      method: "DELETE",
    }),
}
```

### Error Handling Strategy
- **401 Unauthorized**: Redirect to login page, clear session
- **404 Not Found**: Show "Task not found" message, remove from UI
- **422 Validation Error**: Show field-specific error messages
- **500 Server Error**: Show generic error, offer retry
- **Network Error**: Show "offline" message, offer retry

### Key Gotchas
- getAuthToken() must run on server in Server Components
- Client components need to pass token from server or use client-side auth hooks
- Always handle JSON parsing errors in error responses
- TypeScript types must match backend API contracts exactly

---

## 3. Optimistic UI Updates

### Decision
Implement optimistic updates for task completion toggle with automatic rollback on backend failure.

### Rationale
- **Instant Feedback**: Users see immediate response to actions
- **Better UX**: No waiting for server round-trip on every toggle
- **Graceful Degradation**: Automatically reverts on error
- **Meets SC-005**: Task toggle feedback < 100ms requirement

### Alternatives Considered

**Wait for Backend Response**
- ✅ Simpler implementation
- ✅ Always shows correct state
- ❌ Poor UX with noticeable delay (200-500ms)
- ❌ Fails SC-005 performance requirement
- **Rejected**: Doesn't meet performance targets

**Optimistic with No Rollback**
- ❌ Can show incorrect state indefinitely
- ❌ Confusing if backend fails silently
- **Rejected**: Poor error handling

### Implementation Pattern

**React Hook for Optimistic Toggle**:
```typescript
"use client"
import { useState, useTransition } from "react"
import { tasksAPI } from "@/lib/api"
import { toast } from "sonner"

export function useOptimisticToggle(task: Task) {
  const [optimisticCompleted, setOptimisticCompleted] = useState(task.completed)
  const [isPending, startTransition] = useTransition()

  const toggleComplete = async () => {
    // Immediately update UI
    setOptimisticCompleted(!optimisticCompleted)

    try {
      // Send backend request
      const updated = await tasksAPI.toggleComplete(task.id)

      // Verify backend state matches optimistic state
      if (updated.completed !== !optimisticCompleted) {
        setOptimisticCompleted(updated.completed)
      }

      toast.success(
        updated.completed ? "Task completed!" : "Task reopened"
      )
    } catch (error) {
      // Rollback on error
      setOptimisticCompleted(task.completed)
      toast.error("Failed to update task. Please try again.")
    }
  }

  return { optimisticCompleted, toggleComplete, isPending }
}
```

**TaskItem Component**:
```typescript
"use client"
import { useOptimisticToggle } from "@/hooks/useOptimisticToggle"

export function TaskItem({ task }: { task: Task }) {
  const { optimisticCompleted, toggleComplete, isPending } = useOptimisticToggle(task)

  return (
    <div className={optimisticCompleted ? "line-through opacity-60" : ""}>
      <Checkbox
        checked={optimisticCompleted}
        onCheckedChange={toggleComplete}
        disabled={isPending}
      />
      <span>{task.title}</span>
    </div>
  )
}
```

### Key Gotchas
- Must use useState for local optimistic state
- useTransition helps with pending states
- Always revert to server state on error
- Show visual loading indicator during transition
- Consider debouncing rapid clicks

---

## 4. Shadcn/ui + Next.js App Router

### Decision
Use Shadcn/ui components installed via CLI, with Server Components by default and Client Components ("use client") only when needed.

### Rationale
- **Copy-Paste Components**: No package lock-in, full ownership of code
- **Tailwind-Based**: Customizable via Tailwind config
- **Accessible**: Built on Radix UI primitives (ARIA compliant)
- **Type-Safe**: Full TypeScript support
- **Tree-Shakeable**: Only bundle what you use

### Alternatives Considered

**Material-UI (MUI)**
- ✅ Mature, comprehensive component library
- ❌ Larger bundle size
- ❌ CSS-in-JS adds runtime cost
- ❌ Harder to customize for specific design
- **Rejected**: Too opinionated, bundle size concerns

**Chakra UI**
- ✅ Great developer experience
- ✅ Built-in dark mode
- ❌ CSS-in-JS runtime cost
- ❌ Another abstraction over styling
- **Rejected**: Prefer Tailwind for styling control

**Headless UI**
- ✅ Unstyled primitives, full control
- ❌ Must build all styles from scratch
- ❌ More work than Shadcn copy-paste
- **Rejected**: Too low-level for timeline

### Components to Install

```bash
npx shadcn@latest init
npx shadcn@latest add button
npx shadcn@latest add input
npx shadcn@latest add textarea
npx shadcn@latest add dialog
npx shadcn@latest add card
npx shadcn@latest add checkbox
npx shadcn@latest add form
npx shadcn@latest add toast
npx shadcn@latest add switch
```

### Server vs. Client Component Strategy

**Server Components (default)**:
- Layout wrappers
- Static content
- Data fetching components (TaskList initial load)

**Client Components ("use client")**:
- Interactive forms (CreateTaskDialog, EditTaskDialog)
- Stateful components (TaskItem with checkbox)
- Components using hooks (useTheme, useState, etc.)
- Event handlers (onClick, onChange, etc.)

### Implementation Pattern

**Form Example** (Client Component):
```typescript
"use client"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"

export function CreateTaskDialog({ onClose }: { onClose: () => void }) {
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    await tasksAPI.create({ title, description })
    onClose()
  }

  return (
    <Dialog open onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create New Task</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <Input
            placeholder="Task title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            maxLength={200}
            required
          />
          <Textarea
            placeholder="Description (optional)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            maxLength={1000}
          />
          <Button type="submit">Create Task</Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}
```

### Key Gotchas
- Shadcn components are client components by default - wrap in Server Components where possible
- Form component requires react-hook-form dependency
- Toast requires Toaster component in root layout
- Dialog must be controlled with open/onOpenChange props

---

## 5. Dark Mode Implementation

### Decision
Use next-themes library with CSS variables for theme switching, preventing FOUC (Flash of Unstyled Content).

### Rationale
- **Zero Flash**: Prevents white flash on dark mode load
- **Persistent**: Saves preference to localStorage
- **System Aware**: Respects OS theme preference
- **Tailwind Integration**: Works seamlessly with Tailwind dark: classes
- **Lightweight**: < 2KB gzipped

### Alternatives Considered

**Manual localStorage + CSS Classes**
- ✅ Full control over implementation
- ❌ Must handle FOUC manually
- ❌ Must implement system preference detection
- **Rejected**: next-themes solves these problems

**CSS prefers-color-scheme Only**
- ✅ No JavaScript required
- ❌ No user override option
- ❌ No persistence across devices
- **Rejected**: Users need manual control

### Implementation Pattern

**ThemeProvider Setup** (`providers/ThemeProvider.tsx`):
```typescript
"use client"
import { ThemeProvider as NextThemesProvider } from "next-themes"

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  return (
    <NextThemesProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
    >
      {children}
    </NextThemesProvider>
  )
}
```

**Root Layout** (`app/layout.tsx`):
```typescript
import { ThemeProvider } from "@/providers/ThemeProvider"

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <ThemeProvider>
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
```

**Theme Toggle Component** (`components/ThemeToggle.tsx`):
```typescript
"use client"
import { Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"
import { Button } from "@/components/ui/button"
import { useEffect, useState } from "react"

export function ThemeToggle() {
  const [mounted, setMounted] = useState(false)
  const { theme, setTheme } = useTheme()

  useEffect(() => setMounted(true), [])

  if (!mounted) return null

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
    >
      <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <span className="sr-only">Toggle theme</span>
    </Button>
  )
}
```

**Tailwind Configuration** (`tailwind.config.ts`):
```typescript
import type { Config } from "tailwindcss"

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./app/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        // ... other Shadcn color variables
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}

export default config
```

**CSS Variables** (`app/globals.css`):
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    /* ... other light theme variables */
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    /* ... other dark theme variables */
  }
}
```

### Key Gotchas
- Must use suppressHydrationWarning on <html> to prevent hydration mismatch
- Theme toggle must check mounted state to prevent hydration errors
- Use class-based dark mode (not media query) for manual control
- CSS variables enable smooth theme transitions
- disableTransitionOnChange prevents theme animation jank

---

## 6. Middleware for Route Protection

### Decision
Use Next.js 16 middleware to check JWT authentication for protected routes and redirect unauthenticated users to login.

### Rationale
- **Centralized Auth Logic**: One place to check authentication
- **Edge Runtime**: Runs before page render, prevents flash of content
- **Redirects**: Automatic redirect to login for protected routes
- **Performance**: Lightweight check, no page render if not authorized

### Alternatives Considered

**Per-Page Auth Checks**
- ❌ Duplicate code across protected pages
- ❌ Flash of protected content before redirect
- ❌ Harder to maintain
- **Rejected**: Middleware is more efficient

**Server Component Checks Only**
- ✅ Works with Server Components
- ❌ Still renders page before redirect
- ❌ No protection for API routes
- **Rejected**: Middleware runs earlier in request lifecycle

### Implementation Pattern

**Middleware** (`middleware.ts`):
```typescript
import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"
import { auth } from "@/lib/auth"

// Define protected routes
const protectedRoutes = ["/dashboard"]
const authRoutes = ["/login", "/signup"]

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl

  // Get session from Better Auth
  const session = await auth.api.getSession({
    headers: request.headers
  })

  const isAuthenticated = !!session
  const isProtectedRoute = protectedRoutes.some(route =>
    pathname.startsWith(route)
  )
  const isAuthRoute = authRoutes.some(route =>
    pathname.startsWith(route)
  )

  // Redirect unauthenticated users from protected routes to login
  if (isProtectedRoute && !isAuthenticated) {
    const loginUrl = new URL("/login", request.url)
    loginUrl.searchParams.set("from", pathname)
    return NextResponse.redirect(loginUrl)
  }

  // Redirect authenticated users from auth routes to dashboard
  if (isAuthRoute && isAuthenticated) {
    return NextResponse.redirect(new URL("/dashboard", request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for the ones starting with:
     * - api (API routes)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    "/((?!api|_next/static|_next/image|favicon.ico).*)",
  ],
}
```

**Home Page Redirect** (`app/page.tsx`):
```typescript
import { redirect } from "next/navigation"
import { auth } from "@/lib/auth"
import { headers } from "next/headers"

export default async function HomePage() {
  const session = await auth.api.getSession({
    headers: await headers()
  })

  if (session) {
    redirect("/dashboard")
  } else {
    redirect("/login")
  }
}
```

### Key Gotchas
- Middleware runs on every request - keep it lightweight
- Use matcher config to exclude static files and API routes
- Store "from" parameter in login redirect to return user after auth
- Better Auth session check must work in Edge Runtime
- Middleware runs before Server Components

---

## 7. Responsive Design Patterns

### Decision
Mobile-first approach with Tailwind breakpoints, touch-friendly UI elements (minimum 44x44px), and responsive dialogs that become full-screen on mobile.

### Rationale
- **Mobile-First**: Majority of users may be on mobile
- **Progressive Enhancement**: Add desktop features on larger screens
- **Touch-Friendly**: Meets accessibility guidelines for touch targets
- **Responsive Dialogs**: Better UX on small screens

### Breakpoint Strategy

**Tailwind Breakpoints**:
- `sm`: 640px - Small tablets
- `md`: 768px - Tablets
- `lg`: 1024px - Laptops
- `xl`: 1280px - Desktops
- `2xl`: 1536px - Large desktops

**Design Decisions**:
- Mobile (default): Single column, full-width cards, stacked layout
- Tablet (md): Two columns, condensed spacing
- Desktop (lg): Three columns, sidebar navigation, hover states

### Implementation Pattern

**Responsive Task List**:
```typescript
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {tasks.map(task => (
    <TaskCard key={task.id} task={task} />
  ))}
</div>
```

**Responsive Dialog**:
```typescript
<Dialog>
  <DialogContent className="w-full max-w-md sm:max-w-lg md:max-w-xl">
    <DialogHeader>
      <DialogTitle className="text-lg sm:text-xl">
        Create Task
      </DialogTitle>
    </DialogHeader>
    {/* Form content */}
  </DialogContent>
</Dialog>
```

**Touch-Friendly Buttons**:
```typescript
<Button
  size="lg"
  className="min-h-[44px] min-w-[44px] touch-manipulation"
>
  Delete
</Button>
```

**Responsive Navbar**:
```typescript
<nav className="flex items-center justify-between p-4 md:px-8">
  <h1 className="text-xl md:text-2xl font-bold">Todo App</h1>
  <div className="flex items-center gap-2 md:gap-4">
    <ThemeToggle />
    <Button className="hidden sm:inline-flex">Logout</Button>
    <Button className="sm:hidden" size="icon">
      <LogOut className="h-5 w-5" />
    </Button>
  </div>
</nav>
```

### Key Gotchas
- Always test on real devices, not just browser DevTools
- Touch targets must be minimum 44x44px (Apple HIG, WCAG 2.1)
- Use `touch-manipulation` CSS to disable zoom on double-tap
- Dialogs should have max-width constraints on desktop
- Consider thumb-reach zones on mobile (bottom navigation better than top)
- Test with slow 3G network throttling

---

## Summary of Key Decisions

| Area | Decision | Primary Rationale |
|------|----------|------------------|
| **Authentication** | Better Auth + JWT | Simple JWT integration with backend |
| **API Client** | Centralized fetch wrapper | Single source of truth, type safety |
| **Optimistic UI** | React state + rollback | Instant feedback, meets performance target |
| **Components** | Shadcn/ui | Copy-paste, Tailwind-based, accessible |
| **Dark Mode** | next-themes | Zero FOUC, system-aware, persistent |
| **Route Protection** | Next.js middleware | Centralized, edge runtime, efficient |
| **Responsive** | Mobile-first Tailwind | Progressive enhancement, touch-friendly |

---

## Implementation Checklist

- [ ] Initialize Next.js 16 with TypeScript and Tailwind
- [ ] Install and configure Shadcn/ui CLI
- [ ] Set up Better Auth with JWT plugin
- [ ] Create centralized API client with type definitions
- [ ] Implement middleware for route protection
- [ ] Add next-themes provider and theme toggle
- [ ] Build responsive layouts with mobile-first approach
- [ ] Implement optimistic updates for task toggle
- [ ] Add comprehensive error handling and user feedback
- [ ] Test on mobile devices and various screen sizes

---

**Research Complete**: ✅ All technology decisions documented
**Next Phase**: Generate data-model.md and API contracts (Phase 1)
