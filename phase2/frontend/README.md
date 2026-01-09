# Todo Frontend Application

A modern, responsive todo application built with Next.js 16, React 19, TypeScript, and Tailwind CSS.

## Features

- ✅ User authentication (signup, login, logout)
- ✅ Create, read, update, delete tasks
- ✅ Toggle task completion with optimistic updates
- ✅ Dark mode support
- ✅ Responsive design (mobile & desktop)
- ✅ Real-time form validation
- ✅ Toast notifications for user feedback
- ✅ Loading states and error handling

## Tech Stack

- **Framework**: Next.js 16 with App Router
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS v4
- **UI Components**: Shadcn/ui
- **Authentication**: JWT tokens
- **State Management**: React hooks
- **Date Formatting**: date-fns
- **Icons**: Lucide React
- **Notifications**: Sonner (toast)

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Backend API running at http://localhost:8000

### Installation

1. Install dependencies:

```bash
npm install
```

2. Create `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=63734b1ce73e64801b32de3f9dd0d807
BETTER_AUTH_URL=http://localhost:3000
```

3. Start the development server:

```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── dashboard/         # Dashboard page
│   ├── login/             # Login page
│   ├── signup/            # Signup page
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page (redirects)
│   ├── error.tsx          # Error boundary
│   └── not-found.tsx      # 404 page
├── components/            # React components
│   ├── tasks/            # Task-related components
│   ├── ui/               # Shadcn UI components
│   ├── Navbar.tsx        # Navigation bar
│   └── ThemeToggle.tsx   # Dark mode toggle
├── hooks/                # Custom React hooks
├── lib/                  # Utilities and helpers
│   ├── api.ts           # API client
│   ├── auth.ts          # Auth configuration
│   ├── types.ts         # TypeScript types
│   └── utils.ts         # Helper functions
├── providers/           # Context providers
└── middleware.ts        # Route protection
```

## API Integration

The frontend communicates with the backend API at `http://localhost:8000`:

- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User authentication
- `GET /api/tasks` - List all tasks
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/{id}` - Update task
- `PATCH /api/tasks/{id}/complete` - Toggle completion
- `DELETE /api/tasks/{id}` - Delete task

All task endpoints require JWT authentication.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | http://localhost:8000 |
| `BETTER_AUTH_SECRET` | JWT secret (must match backend) | - |
| `BETTER_AUTH_URL` | Frontend URL for auth callbacks | http://localhost:3000 |

## License

MIT
