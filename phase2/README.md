# TodoApp - Full-Stack Task Management Application

A modern, full-stack todo application with a beautiful UI, built with Next.js 15, FastAPI, and PostgreSQL. Features JWT authentication, real-time updates, dark mode support, and a responsive design.

![TodoApp](https://img.shields.io/badge/Next.js-15-black?logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-336791?logo=postgresql)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript)

## Features

### Frontend
- **Modern UI/UX**: Beautiful gradient backgrounds, smooth animations, and polished design
- **Dark Mode**: Full dark mode support with seamless theme switching
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Real-time Updates**: Optimistic UI updates for instant feedback
- **Authentication**: Secure JWT-based authentication with login and signup
- **Task Management**:
  - Create, read, update, and delete tasks
  - Toggle task completion with visual feedback
  - Edit tasks inline with modal dialogs
  - View task timestamps with relative time formatting

### Backend
- **RESTful API**: 6 CRUD endpoints for comprehensive task management
- **JWT Authentication**: Secure user authentication with Better Auth integration
- **Multi-user Support**: Complete data isolation between users
- **PostgreSQL Database**: Reliable Neon serverless PostgreSQL storage
- **Auto Documentation**: Interactive Swagger/ReDoc API documentation
- **CORS Configuration**: Properly configured for frontend integration

## Tech Stack

### Frontend
- **Framework**: Next.js 15 (React 19)
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS 3 with custom gradient designs
- **UI Components**: Radix UI primitives with shadcn/ui
- **Icons**: Lucide React
- **Forms**: React Hook Form
- **Date Formatting**: date-fns
- **Notifications**: Sonner (toast notifications)

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (Neon Serverless)
- **ORM**: SQLModel (Pydantic + SQLAlchemy)
- **Authentication**: JWT with python-jose
- **Environment**: python-dotenv
- **Server**: Uvicorn (ASGI)

## Project Structure

```
phase2/
├── frontend/                 # Next.js frontend application
│   ├── app/                  # App router pages
│   │   ├── page.tsx          # Landing page
│   │   ├── login/            # Login page
│   │   ├── signup/           # Signup page
│   │   └── dashboard/        # Dashboard (protected)
│   ├── components/           # React components
│   │   ├── ui/               # shadcn/ui components
│   │   ├── tasks/            # Task-related components
│   │   ├── Navbar.tsx        # Navigation bar
│   │   └── ThemeToggle.tsx   # Dark mode toggle
│   ├── lib/                  # Utilities and API client
│   │   ├── api.ts            # API client with auth
│   │   └── types.ts          # TypeScript types
│   ├── hooks/                # Custom React hooks
│   └── providers/            # React context providers
│
├── backend/                  # FastAPI backend application
│   ├── main.py               # FastAPI app entry point
│   ├── models.py             # Database models and schemas
│   ├── database.py           # Database connection and config
│   ├── auth.py               # JWT authentication
│   └── routes/               # API route handlers
│       ├── auth.py           # Auth endpoints
│       └── tasks.py          # Task CRUD endpoints
│
└── README.md                 # This file
```

## Prerequisites

- **Node.js**: 18+ (for frontend)
- **Python**: 3.13+ (for backend)
- **PostgreSQL**: Neon account ([neon.tech](https://neon.tech))
- **Package Managers**: npm/yarn/pnpm (frontend), pip (backend)

## Setup Instructions

### 1. Clone the Repository

```bash
cd phase2
```

### 2. Backend Setup

#### Install Dependencies

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Configure Environment

Create `.env` file in the `backend/` directory:

```bash
cp .env.example .env
```

Edit `.env` with your actual values:

```env
# Neon PostgreSQL connection string
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require

# Shared secret for JWT verification (must match frontend)
BETTER_AUTH_SECRET=your-secret-key-min-32-characters

# CORS allowed origins
ALLOWED_ORIGINS=http://localhost:3000
```

**Get your Neon PostgreSQL URL:**
1. Sign up at [neon.tech](https://neon.tech)
2. Create a new project
3. Copy the connection string from the dashboard

#### Run the Backend Server

```bash
# Development mode (with auto-reload)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Server will start at: `http://localhost:8000`

**API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 3. Frontend Setup

#### Install Dependencies

```bash
cd frontend

# Install dependencies
npm install
# or
yarn install
# or
pnpm install
```

#### Configure Environment

Create `.env.local` file in the `frontend/` directory:

```bash
cp .env.example .env.local
```

Edit `.env.local`:

```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Secret (must match backend)
BETTER_AUTH_SECRET=your-secret-key-min-32-characters

# Better Auth URL (for authentication callbacks)
BETTER_AUTH_URL=http://localhost:3000
```

**Important:** Make sure `BETTER_AUTH_SECRET` matches the one in your backend `.env` file.

#### Run the Frontend Server

```bash
# Development mode
npm run dev
# or
yarn dev
# or
pnpm dev
```

Frontend will start at: `http://localhost:3000`

## Environment Variables

### Backend (.env)

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string from Neon | `postgresql://user:pass@host/db?sslmode=require` |
| `BETTER_AUTH_SECRET` | JWT signing secret (min 32 chars) | `your-secret-key-min-32-characters` |
| `ALLOWED_ORIGINS` | Comma-separated CORS allowed origins | `http://localhost:3000` |

### Frontend (.env.local)

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | `http://localhost:8000` |
| `BETTER_AUTH_SECRET` | JWT secret (must match backend) | `your-secret-key-min-32-characters` |
| `BETTER_AUTH_URL` | Frontend base URL | `http://localhost:3000` |

## API Endpoints

All task endpoints require JWT authentication via `Authorization: Bearer <token>` header.

### Authentication

- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/login` - Login and receive JWT token

### Tasks

- `GET /api/tasks` - List all tasks for authenticated user
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get specific task by ID
- `PUT /api/tasks/{id}` - Update task title/description
- `PATCH /api/tasks/{id}/complete` - Toggle task completion status
- `DELETE /api/tasks/{id}` - Delete task permanently

### Health Check

- `GET /api/health` - Health check (no auth required)

For detailed API documentation, visit the Swagger UI at http://localhost:8000/docs when the backend is running.

## Development Workflow

1. **Start Backend**: Open terminal in `backend/`, activate venv, run `uvicorn main:app --reload`
2. **Start Frontend**: Open terminal in `frontend/`, run `npm run dev`
3. **Access App**: Open http://localhost:3000 in your browser
4. **Create Account**: Click "Sign Up" and create a new account
5. **Start Managing Tasks**: Login and start creating tasks!

## Deployment Instructions

### Backend Deployment (Render/Railway/Fly.io)

1. Create account on your preferred platform
2. Connect your Git repository
3. Set environment variables from `.env` file
4. Deploy command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Update frontend `NEXT_PUBLIC_API_URL` with deployed backend URL

### Frontend Deployment (Vercel/Netlify)

1. Create account on Vercel or Netlify
2. Connect your Git repository
3. Set framework to "Next.js"
4. Add environment variables from `.env.local`
5. Deploy!

**Important:** After deployment, update:
- Backend `ALLOWED_ORIGINS` to include frontend production URL
- Frontend `NEXT_PUBLIC_API_URL` to backend production URL

## Troubleshooting

### Backend Issues

**Database Connection Error:**
- Verify `DATABASE_URL` is correct
- Check Neon project is not paused (free tier auto-pauses after inactivity)
- Test connection: `psql "YOUR_DATABASE_URL"`

**JWT Verification Fails:**
- Ensure `BETTER_AUTH_SECRET` matches frontend
- Check token is not expired
- Verify `Authorization` header format: `Bearer <token>` (with space)

**CORS Errors:**
- Verify `ALLOWED_ORIGINS` includes frontend URL
- Restart server after changing `.env`
- Check browser DevTools Network tab for preflight requests

### Frontend Issues

**API Connection Fails:**
- Ensure backend is running on the correct port (8000)
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check browser console for error messages

**Authentication Not Working:**
- Clear browser localStorage and cookies
- Verify `BETTER_AUTH_SECRET` matches backend
- Check token is being sent in Authorization header

**Tasks Not Updating:**
- Check browser console for API errors
- Verify JWT token is valid and not expired
- Restart both frontend and backend servers

## Features in Detail

### User Authentication
- Secure JWT-based authentication
- Password validation (min 8 characters)
- Email format validation
- Persistent login sessions
- Automatic token refresh

### Task Management
- Create tasks with title and optional description
- Edit tasks inline with modal dialogs
- Mark tasks as complete with visual feedback
- Delete tasks with confirmation dialog
- View creation timestamps with relative time ("2 hours ago")
- Real-time UI updates with optimistic rendering

### UI/UX Features
- Beautiful gradient backgrounds (purple to blue)
- Smooth animations and transitions
- Dark mode with system preference detection
- Responsive design for all screen sizes
- Toast notifications for user feedback
- Loading states and error handling
- Empty state illustrations
- Hover effects and visual polish

## Credits

**Made by Sabeh Shaikh**

- GitHub: [@SabehShaikh](https://github.com/SabehShaikh)
- LinkedIn: [sabeh-shaikh](https://www.linkedin.com/in/sabeh-shaikh/)

## License

This project is part of the Q4-Gemini CLI Hackathon Phase 2.

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

---

**Happy Task Managing! 🚀**
