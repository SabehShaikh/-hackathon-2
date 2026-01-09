# Quickstart: Todo Frontend Web Application

**Feature**: Todo Frontend Web Application
**Date**: 2026-01-09
**Phase**: Phase 1 - Setup & Getting Started

## Overview

This guide will help you set up and run the Todo Frontend application in under 10 minutes. The frontend is a Next.js 16 application that connects to the existing backend API from Phase 1.

---

## Prerequisites

Before you begin, ensure you have the following installed:

- ✅ **Node.js** 20.x or higher ([Download](https://nodejs.org/))
- ✅ **npm** 10.x or higher (comes with Node.js)
- ✅ **Git** (for cloning the repository)
- ✅ **Backend API** running at `http://localhost:8000` (from Phase 1)
- ✅ **Modern Web Browser** (Chrome, Firefox, Safari, or Edge - last 2 versions)

### Verify Prerequisites

```bash
node --version  # Should show v20.x.x or higher
npm --version   # Should show 10.x.x or higher
git --version   # Should show git version 2.x or higher
```

### Backend API Verification

Ensure the backend is running and accessible:

```bash
curl http://localhost:8000/api/tasks
# Should return: {"detail":"Authentication required"} (401 error is expected)
```

If you get a connection error, start the backend first (see Phase 1 documentation).

---

## Quick Start (5 Steps)

### Step 1: Clone the Repository (if not already cloned)

```bash
git clone <repository-url>
cd <repository-name>
```

### Step 2: Navigate to Frontend Directory

```bash
cd frontend
```

### Step 3: Install Dependencies

```bash
npm install
```

This will install all required dependencies:
- Next.js 16+
- React 19+
- TypeScript
- Tailwind CSS
- Better Auth
- Shadcn/ui components
- next-themes (dark mode)
- Sonner (toast notifications)
- Lucide React (icons)

**Expected time**: 1-2 minutes

### Step 4: Configure Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```bash
cp .env.example .env.local
```

Edit `.env.local` and set the following variables:

```env
# Backend API URL (development)
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Secret (must match backend or be unique for frontend)
# IMPORTANT: Use the value below for Phase 2 development
BETTER_AUTH_SECRET=63734b1ce73e64801b32de3f9dd0d807

# Next.js Configuration
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

**⚠️ Important**: Never commit `.env.local` to version control. It's already in `.gitignore`.

### Step 5: Start Development Server

```bash
npm run dev
```

The application will start at **http://localhost:3000**

You should see:
```
✓ Ready in 2.3s
○ Local: http://localhost:3000
```

---

## First Time Setup

### 1. Open the Application

Navigate to http://localhost:3000 in your web browser.

You should be redirected to the login page.

### 2. Create Your First Account

1. Click "Sign Up" (or go to http://localhost:3000/signup)
2. Enter your email address
3. Choose a password (min 8 characters)
4. Click "Create Account"

You'll be automatically logged in and redirected to the dashboard.

### 3. Create Your First Task

1. On the dashboard, click "+ New Task" button
2. Enter a task title (e.g., "Buy groceries")
3. Optionally add a description
4. Click "Create"

The task appears in your list instantly!

### 4. Test Core Features

Try the following to verify everything works:

- ✅ **Toggle Complete**: Click the checkbox next to a task
- ✅ **Edit Task**: Click the edit icon, modify the title/description, save
- ✅ **Delete Task**: Click the delete icon, confirm deletion
- ✅ **Dark Mode**: Click the theme toggle in the navbar
- ✅ **Logout**: Click logout button, verify you're redirected to login

### 5. Test Responsive Design

1. Open browser DevTools (F12)
2. Toggle device toolbar (Ctrl/Cmd + Shift + M)
3. Test on mobile (375px), tablet (768px), and desktop (1920px) sizes

All UI elements should adapt to screen size.

---

## Project Structure

Once set up, your frontend directory will look like this:

```
frontend/
├── app/                      # Next.js App Router pages
│   ├── layout.tsx            # Root layout with providers
│   ├── page.tsx              # Home page (redirects based on auth)
│   ├── globals.css           # Global styles and Tailwind
│   ├── dashboard/
│   │   └── page.tsx          # Task dashboard (protected)
│   ├── login/
│   │   └── page.tsx          # Login page
│   └── signup/
│       └── page.tsx          # Signup page
│
├── components/               # React components
│   ├── ui/                   # Shadcn components (generated)
│   ├── tasks/                # Task-related components
│   ├── Navbar.tsx            # Navigation bar
│   └── ThemeToggle.tsx       # Theme switcher
│
├── lib/                      # Utility libraries
│   ├── api.ts                # API client with auth
│   ├── auth.ts               # Better Auth configuration
│   ├── types.ts              # TypeScript type definitions
│   └── utils.ts              # Helper functions
│
├── providers/                # React context providers
│   └── ThemeProvider.tsx     # Dark mode provider
│
├── middleware.ts             # Route protection logic
├── .env.local                # Environment variables (gitignored)
├── .env.example              # Example env file (committed)
├── next.config.ts            # Next.js configuration
├── tailwind.config.ts        # Tailwind CSS configuration
├── components.json           # Shadcn CLI configuration
├── tsconfig.json             # TypeScript configuration
├── package.json              # Dependencies and scripts
└── README.md                 # Project documentation
```

---

## Shadcn/ui Components Installation

The following Shadcn components are used in this project. They should already be installed if you ran `npm install`, but you can reinstall them individually if needed.

### Initial Shadcn Setup (one-time)

```bash
npx shadcn@latest init
```

Answer the prompts:
- TypeScript: **Yes**
- Style: **Default**
- Base color: **Slate**
- Global CSS: **app/globals.css**
- CSS variables: **Yes**
- Tailwind config: **tailwind.config.ts**
- Components: **components**
- Utils: **lib/utils.ts**
- React Server Components: **Yes**

### Install Individual Components

```bash
# Core UI Components
npx shadcn@latest add button
npx shadcn@latest add input
npx shadcn@latest add textarea
npx shadcn@latest add checkbox
npx shadcn@latest add card

# Dialog Components
npx shadcn@latest add dialog

# Form Components
npx shadcn@latest add form

# Feedback Components
npx shadcn@latest add toast

# Theme Toggle
npx shadcn@latest add switch
```

**Note**: These components are copied into your `components/ui/` directory, giving you full control to customize them.

---

## Available Scripts

Run these commands from the `frontend/` directory:

### Development

```bash
npm run dev
```
Starts the development server at http://localhost:3000 with:
- Hot module replacement (HMR)
- TypeScript type checking
- Fast Refresh for React components

### Build for Production

```bash
npm run build
```
Creates an optimized production build:
- Minified JavaScript and CSS
- Optimized images
- Static page generation where possible

### Start Production Server

```bash
npm run start
```
Runs the production build (must run `npm run build` first)

### Type Checking

```bash
npm run type-check
```
Runs TypeScript compiler to check for type errors without emitting files

### Linting

```bash
npm run lint
```
Runs ESLint to check code quality and enforce standards

### Format Code

```bash
npm run format
```
Runs Prettier to format code consistently (if configured)

---

## Common Development Tasks

### Adding a New Shadcn Component

```bash
npx shadcn@latest add <component-name>
```

Example:
```bash
npx shadcn@latest add alert
```

### Viewing Toast Notifications

Toast notifications use Sonner. To see them in action:

1. Ensure `Toaster` component is added to root layout
2. Import and use in components:

```typescript
import { toast } from "sonner"

toast.success("Task created!")
toast.error("Failed to delete task")
toast.info("Session expires in 5 minutes")
```

### Testing Different Screen Sizes

Use Next.js built-in responsive testing:

1. Open http://localhost:3000
2. Press F12 to open DevTools
3. Click device toolbar icon (or Ctrl/Cmd + Shift + M)
4. Select preset devices or enter custom dimensions

Test these breakpoints:
- **Mobile**: 375px (iPhone SE)
- **Tablet**: 768px (iPad)
- **Laptop**: 1024px (small laptop)
- **Desktop**: 1920px (full HD)

### Debugging Authentication Issues

If you have authentication problems:

1. **Check Backend**: Ensure backend is running at http://localhost:8000
2. **Check Environment Variables**: Verify `.env.local` has correct values
3. **Check Browser Console**: Look for CORS errors or 401 responses
4. **Check Network Tab**: Inspect API requests and responses
5. **Clear Cookies**: Some auth issues are caused by stale cookies

```bash
# Clear Better Auth cookies in browser DevTools:
# Application > Cookies > http://localhost:3000 > Delete all
```

### Debugging CORS Issues

If you see CORS errors in the console:

1. **Backend CORS Configuration**: Ensure backend allows `http://localhost:3000`
2. **Credentials**: Ensure `credentials: "include"` is set in fetch options
3. **Headers**: Ensure backend allows `Authorization` and `Content-Type` headers

Expected backend CORS headers:
```
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Credentials: true
Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

---

## Troubleshooting

### Issue: "Cannot GET /api/tasks"

**Cause**: Backend API is not running

**Solution**:
```bash
cd backend  # Navigate to backend directory
# Start backend server (see Phase 1 docs)
python -m uvicorn main:app --reload
```

### Issue: "Network Error" on all requests

**Cause**: Backend URL is incorrect or backend is not running

**Solution**:
1. Check `.env.local` has `NEXT_PUBLIC_API_URL=http://localhost:8000`
2. Verify backend is running: `curl http://localhost:8000/health`
3. Restart dev server: `npm run dev`

### Issue: "Module not found" errors

**Cause**: Dependencies not installed or corrupted node_modules

**Solution**:
```bash
rm -rf node_modules package-lock.json
npm install
```

### Issue: "Port 3000 already in use"

**Cause**: Another process is using port 3000

**Solution**:
```bash
# Option 1: Kill the process using port 3000
# Windows:
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:3000 | xargs kill

# Option 2: Use a different port
npm run dev -- -p 3001
# Update .env.local: NEXT_PUBLIC_APP_URL=http://localhost:3001
```

### Issue: TypeScript errors in IDE

**Cause**: IDE not recognizing TypeScript configuration

**Solution**:
```bash
# VS Code: Reload window
Cmd/Ctrl + Shift + P > "TypeScript: Restart TS Server"

# Or restart type checking
npm run type-check
```

### Issue: Tailwind styles not applying

**Cause**: Tailwind configuration not loaded

**Solution**:
1. Check `tailwind.config.ts` includes all content paths
2. Ensure `globals.css` imports Tailwind directives
3. Restart dev server
4. Clear browser cache (Ctrl/Cmd + Shift + R)

### Issue: Dark mode not working

**Cause**: ThemeProvider not properly configured

**Solution**:
1. Ensure `ThemeProvider` wraps app in `app/layout.tsx`
2. Check `<html>` tag has `suppressHydrationWarning` attribute
3. Verify `tailwind.config.ts` has `darkMode: ["class"]`
4. Clear localStorage and refresh

---

## Testing Your Setup

Run through this checklist to verify everything is working:

### Functional Tests
- [ ] Can access http://localhost:3000 (redirects to /login)
- [ ] Can create a new account via /signup
- [ ] Can log in with created account
- [ ] Can view dashboard with tasks
- [ ] Can create a new task
- [ ] Can toggle task completion status
- [ ] Can edit a task
- [ ] Can delete a task (with confirmation)
- [ ] Can log out (redirects to /login)
- [ ] Can toggle dark mode (persists after refresh)

### Responsive Tests
- [ ] UI works on mobile (375px width)
- [ ] UI works on tablet (768px width)
- [ ] UI works on desktop (1920px width)
- [ ] Dialogs are full-screen on mobile
- [ ] Touch targets are at least 44x44px

### Error Handling Tests
- [ ] Invalid login shows error message
- [ ] Empty task title shows validation error
- [ ] Task title > 200 chars shows validation error
- [ ] Network error shows retry option
- [ ] Session expiry redirects to login

---

## Next Steps

Once you have the application running:

1. **Read the Specification**: Review `specs/001-todo-frontend/spec.md`
2. **Review the Plan**: Read `specs/001-todo-frontend/plan.md`
3. **Explore the Code**: Start with `app/dashboard/page.tsx` and follow the imports
4. **Run Tests**: Execute test suite (once implemented)
5. **Start Development**: Begin implementing tasks from `tasks.md` (after `/sp.tasks` command)

---

## Production Deployment

### Environment Variables for Production

Create a `.env.production.local` file:

```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
BETTER_AUTH_SECRET=<generate-secure-secret>
NEXT_PUBLIC_APP_URL=https://yourdomain.com
```

**Generate secure secret**:
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

### Build and Deploy

```bash
# Build production bundle
npm run build

# Test production build locally
npm run start

# Deploy to Vercel (recommended for Next.js)
npx vercel --prod

# Or deploy to other platforms:
# - Netlify: Use `npm run build` and deploy `out/` directory
# - AWS Amplify: Connect GitHub repo and use build settings
# - Docker: Create Dockerfile and deploy to any container platform
```

### Production Checklist

- [ ] Environment variables configured for production API
- [ ] BETTER_AUTH_SECRET is a secure random string (not the dev secret)
- [ ] CORS enabled on production backend for frontend domain
- [ ] HTTPS enabled on both frontend and backend
- [ ] Error tracking configured (e.g., Sentry)
- [ ] Analytics configured (e.g., Google Analytics, Vercel Analytics)
- [ ] Performance monitoring enabled
- [ ] Security headers configured in `next.config.ts`

---

## Support and Resources

### Documentation
- **Next.js 16 Docs**: https://nextjs.org/docs
- **Better Auth Docs**: https://better-auth.com
- **Shadcn/ui Docs**: https://ui.shadcn.com
- **Tailwind CSS Docs**: https://tailwindcss.com/docs

### Internal Resources
- **Specification**: `specs/001-todo-frontend/spec.md`
- **Implementation Plan**: `specs/001-todo-frontend/plan.md`
- **Research Notes**: `specs/001-todo-frontend/research.md`
- **Data Models**: `specs/001-todo-frontend/data-model.md`
- **API Contracts**: `specs/001-todo-frontend/contracts/api-contracts.md`

### Getting Help
- Check the troubleshooting section above
- Review error messages in browser console
- Check Network tab in DevTools for failed requests
- Verify backend is running and accessible
- Consult project documentation in `specs/` directory

---

**Setup Time**: ~5-10 minutes
**First Task Creation**: ~1 minute
**Ready for Development**: ✅

Happy coding! 🚀
