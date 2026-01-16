# Phase 3: Todo AI Chatbot

AI-powered todo task management with natural language interface. Built on top of Phase 2 infrastructure with dual interface support.

## Features

- **Dual Interface**: Manage tasks via traditional UI buttons OR conversational AI chat
- **Natural Language**: Add, list, complete, delete, and update tasks with natural commands
- **Conversation Persistence**: Chat history saved in database for multi-session continuity
- **AI Agent**: Powered by Grok API with intelligent intent recognition
- **Full CRUD**: All 5 MCP tools (add, list, complete, delete, update)

## Architecture

```
phase3/
├── backend/          # FastAPI + Grok Agent + MCP Tools
│   ├── main.py       # FastAPI app
│   ├── agent.py      # Grok AI agent
│   ├── mcp_server.py # 5 MCP tools for task management
│   ├── routes/
│   │   ├── auth.py   # Phase 2 auth endpoints
│   │   └── chat.py   # POST /api/chat endpoint
│   └── models.py     # User, Task, Conversation, Message
│
└── frontend/         # Next.js + ChatKit (Phase 2 + additions)
    ├── app/
    │   ├── dashboard/   # Phase 2 task UI
    │   └── chat/        # NEW: AI chat interface
    └── components/
        ├── tasks/       # Phase 2 task components
        └── chat/        # NEW: ChatInterface
```

## Quick Start

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your values:
# - DATABASE_URL (Neon PostgreSQL)
# - BETTER_AUTH_SECRET (same as Phase 2)
# - GROK_API_KEY (from x.ai)

# Run server
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Set environment variables
# Edit .env.local:
# - NEXT_PUBLIC_API_URL=http://localhost:8000

# Run dev server
npm run dev
```

## API Endpoints

### Authentication (Phase 2)
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login and get JWT token

### Chat (Phase 3)
- `POST /api/chat` - Send message to AI agent

### Health
- `GET /api/health` - Check API status

## Chat Examples

```
"Add buy groceries"           → Creates task: Buy groceries
"Show my tasks"               → Lists all tasks with IDs
"Complete task 1"             → Marks task 1 as done
"Delete task 2"               → Removes task 2
"Change task 3 to Call mom"   → Updates task 3 title
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:pass@host:5432/dbname
BETTER_AUTH_SECRET=your-jwt-secret
GROK_API_KEY=xai-your-api-key
ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-jwt-secret
```

## Deployment

### Backend → HuggingFace Spaces
1. Push backend/ to HuggingFace Spaces repo
2. Set environment variables in Space settings
3. Wait for Docker build

### Frontend → Vercel
1. Push repo to GitHub
2. Import to Vercel (root: phase3/frontend)
3. Set NEXT_PUBLIC_API_URL to HuggingFace URL
4. Update ALLOWED_ORIGINS in HuggingFace

## Tech Stack

- **Backend**: Python 3.11, FastAPI, SQLModel, Grok API (OpenAI SDK)
- **Frontend**: Next.js 15, React 18, TypeScript, Tailwind CSS, shadcn/ui
- **Database**: Neon PostgreSQL (shared with Phase 2)
- **AI**: Grok API via OpenAI SDK compatibility layer

## User Stories

| Priority | Story | Status |
|----------|-------|--------|
| P1 | Add task via chat | ✅ |
| P1 | List tasks via chat | ✅ |
| P1 | AI friendly confirmations | ✅ |
| P2 | Conversation persistence | ✅ |
| P2 | Complete task via chat | ✅ |
| P2 | Graceful error handling | ✅ |
| P3 | Delete task via chat | ✅ |
| P3 | Update task via chat | ✅ |

## License

MIT
