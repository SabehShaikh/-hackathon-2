# Quickstart: Todo AI Chatbot with Natural Language Interface

**Feature**: 002-ai-chat-interface
**Date**: 2026-01-15
**Purpose**: Setup, development, testing, and deployment guide

## Prerequisites

### Required Accounts
- [ ] GitHub account (for code hosting)
- [ ] Neon PostgreSQL account (existing from Phase 2)
- [ ] HuggingFace account (backend deployment)
- [ ] Vercel account (frontend deployment)
- [ ] x.ai account (Grok API key)
- [ ] OpenAI account (for ChatKit domain allowlist)

### Required Software
- [ ] Python 3.11+ (`python --version`)
- [ ] Node.js 18+ (`node --version`)
- [ ] Git (`git --version`)
- [ ] PostgreSQL client (`psql --version`) - optional, for local testing

### Phase 2 Dependencies
- [ ] Phase 2 deployed and operational
- [ ] Neon PostgreSQL database accessible
- [ ] DATABASE_URL from Phase 2
- [ ] BETTER_AUTH_SECRET from Phase 2

---

## Part 1: Environment Setup

### 1.1 Get API Keys

#### Grok API Key (x.ai)
1. Visit https://x.ai/api
2. Sign up or log in
3. Navigate to API Keys section
4. Create new API key
5. Copy key (starts with `xai-...`)
6. Save as `GROK_API_KEY`

#### Database URL (Neon)
1. Use existing Phase 2 Neon PostgreSQL instance
2. Get connection string from Neon dashboard
3. Format: `postgresql://user:password@host/dbname?sslmode=require`
4. Save as `DATABASE_URL`

#### Better Auth Secret (Phase 2)
1. Reuse existing Phase 2 JWT secret
2. Copy from Phase 2 deployment environment variables
3. Save as `BETTER_AUTH_SECRET`

### 1.2 Clone Repository

```bash
cd phase3/
git checkout 002-ai-chat-interface
```

---

## Part 2: Backend Setup

### 2.1 Install Python Dependencies

```bash
cd backend/
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**requirements.txt**:
```
fastapi==0.115.0
uvicorn[standard]==0.32.0
sqlmodel==0.0.22
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
openai==1.58.1
mcp==1.0.0
python-dotenv==1.0.0
passlib[bcrypt]==1.7.4
alembic==1.13.1
```

### 2.2 Configure Environment Variables

Create `.env` file in `backend/`:

```env
# Database (Phase 2 - same instance)
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require

# Authentication (Phase 2 - same secret)
BETTER_AUTH_SECRET=your-phase-2-secret-here

# Grok API (Phase 3 - new)
GROK_API_KEY=xai-your-key-here

# CORS (Phase 3 - update after frontend deployment)
ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend.vercel.app
```

### 2.3 Run Database Migrations

```bash
cd backend/
alembic upgrade head
```

**Expected Output**:
```
INFO  [alembic.runtime.migration] Running upgrade  -> 001, Add conversations and messages tables
```

**Verify Tables Created**:
```bash
psql $DATABASE_URL -c "\dt"
```

Expected tables:
- users (Phase 2)
- tasks (Phase 2)
- conversations (Phase 3 - new)
- messages (Phase 3 - new)

### 2.4 Start Backend Server (Local)

```bash
cd backend/
uvicorn main:app --reload --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**Test Endpoint**:
```bash
curl http://localhost:8000/docs
```

Should show FastAPI Swagger UI with `/api/chat` endpoint.

---

## Part 3: Frontend Setup

### 3.1 Install Node Dependencies

```bash
cd frontend/
npm install
```

**package.json** (key dependencies):
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@openai/chatkit": "^1.0.0",
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0"
  }
}
```

### 3.2 Configure Environment Variables

Create `.env` file in `frontend/`:

```env
# Backend API
VITE_API_URL=http://localhost:8000

# OpenAI ChatKit (update after domain allowlisting)
VITE_OPENAI_DOMAIN_KEY=your-domain-key-here
```

### 3.3 Start Frontend (Local)

```bash
cd frontend/
npm run dev
```

**Expected Output**:
```
  VITE v5.0.0  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

**Test UI**: Open http://localhost:3000 in browser

---

## Part 4: Local Testing

### 4.1 End-to-End Test Flow

1. **Backend Running**: http://localhost:8000
2. **Frontend Running**: http://localhost:3000

**Test Scenario 1: Add Task**
1. Open frontend: http://localhost:3000
2. Log in with Phase 2 credentials
3. Type: "Add buy groceries"
4. Expect: "✅ Added task: Buy groceries"
5. Verify: Task appears in Phase 2 UI (if still deployed)

**Test Scenario 2: List Tasks**
1. Type: "What's on my list?"
2. Expect: List of tasks with IDs
3. Verify: Matches Phase 2 database

**Test Scenario 3: Complete Task**
1. Type: "Mark task 1 as done"
2. Expect: "✅ Completed task: [title]"
3. Verify: Task marked complete in database

**Test Scenario 4: Error Handling**
1. Type: "Complete task 999"
2. Expect: "I couldn't find task 999. Here's what you have: ..."
3. Verify: Friendly error, suggests listing tasks

**Test Scenario 5: Conversation Persistence**
1. Add 2 tasks
2. Close browser tab
3. Reopen http://localhost:3000
4. Expect: Previous conversation visible
5. Type new message
6. Expect: Conversation continues

### 4.2 Manual API Testing

**Test Chat Endpoint** (requires valid JWT):

```bash
# Get JWT token (use Phase 2 login endpoint)
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Copy token from response

# Test chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"message":"Add buy groceries"}'
```

**Expected Response**:
```json
{
  "conversation_id": 1,
  "response": "✅ Added task: Buy groceries",
  "tool_calls": [
    {
      "tool": "add_task",
      "parameters": {
        "user_id": "user123",
        "title": "Buy groceries"
      },
      "result": {
        "status": "success",
        "data": {
          "task_id": 45,
          "title": "Buy groceries"
        }
      }
    }
  ]
}
```

### 4.3 Database Verification

```bash
# Check conversations
psql $DATABASE_URL -c "SELECT * FROM conversations;"

# Check messages
psql $DATABASE_URL -c "SELECT conversation_id, role, content FROM messages ORDER BY created_at;"

# Check tasks created via chat
psql $DATABASE_URL -c "SELECT id, title, completed FROM tasks ORDER BY created_at DESC LIMIT 5;"
```

---

## Part 5: Deployment

### 5.1 Backend Deployment (HuggingFace Spaces)

#### Step 1: Create Dockerfile

**backend/Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run migrations on startup
CMD alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 7860
```

#### Step 2: Create HuggingFace Space

1. Visit https://huggingface.co/spaces
2. Click "Create new Space"
3. Select "Docker" SDK
4. Name: `your-username/todo-ai-chatbot-backend`
5. Visibility: Public or Private

#### Step 3: Configure Secrets

In Space settings → Variables and secrets:
- `DATABASE_URL`: Neon PostgreSQL connection string
- `BETTER_AUTH_SECRET`: Phase 2 JWT secret
- `GROK_API_KEY`: x.ai API key
- `ALLOWED_ORIGINS`: `https://your-frontend.vercel.app` (update after frontend deploy)

#### Step 4: Push Code

```bash
cd backend/
git remote add hf https://huggingface.co/spaces/your-username/todo-ai-chatbot-backend
git push hf main
```

#### Step 5: Verify Deployment

Wait for build to complete (~5 minutes).

Test endpoint:
```bash
curl https://your-username-todo-ai-chatbot-backend.hf.space/docs
```

Should show FastAPI Swagger UI.

**Copy Backend URL**: `https://your-username-todo-ai-chatbot-backend.hf.space`

---

### 5.2 Frontend Deployment (Vercel)

#### Step 1: Push Frontend to GitHub

```bash
cd frontend/
git add .
git commit -m "Phase 3: Frontend ready for deployment"
git push origin 002-ai-chat-interface
```

#### Step 2: Import Project to Vercel

1. Visit https://vercel.com/new
2. Import Git Repository
3. Select `phase3` repository
4. Root Directory: `frontend/`
5. Framework Preset: Vite (or Next.js if using Next)

#### Step 3: Configure Environment Variables

In Vercel project settings → Environment Variables:
- `VITE_API_URL`: `https://your-username-todo-ai-chatbot-backend.hf.space/api`
- `VITE_OPENAI_DOMAIN_KEY`: (leave empty for now)

#### Step 4: Deploy

Click "Deploy" button.

Wait for deployment (~2 minutes).

**Copy Frontend URL**: `https://your-app-name.vercel.app`

---

### 5.3 OpenAI ChatKit Domain Allowlisting

#### Step 1: Add Domain to Allowlist

1. Visit https://platform.openai.com/settings/organization/security/domain-allowlist
2. Click "Add Domain"
3. Enter: `your-app-name.vercel.app` (without https://)
4. Click "Add"
5. Wait for approval (~instant)

#### Step 2: Get Domain Key

1. After domain approved, OpenAI provides a domain key
2. Copy the key (starts with `dk_...`)

#### Step 3: Update Vercel Environment Variable

1. Go to Vercel project settings → Environment Variables
2. Update `VITE_OPENAI_DOMAIN_KEY`: `dk_your-key-here`
3. Click "Save"
4. Redeploy: Vercel → Deployments → Redeploy

---

### 5.4 Update Backend CORS

1. Go to HuggingFace Space settings → Variables
2. Update `ALLOWED_ORIGINS`: `https://your-app-name.vercel.app`
3. Restart Space

---

### 5.5 Final Verification

**Test Production Deployment**:

1. Open `https://your-app-name.vercel.app`
2. Log in with Phase 2 credentials
3. Type: "Add buy groceries"
4. Expect: "✅ Added task: Buy groceries"
5. Verify: Task persists in Phase 2 database
6. Close browser, reopen
7. Expect: Conversation history restored

**Check All Endpoints**:
- ✅ Frontend loads: https://your-app-name.vercel.app
- ✅ Backend API docs: https://your-backend.hf.space/docs
- ✅ Chat endpoint responds: POST /api/chat
- ✅ Phase 2 still operational (untouched)

---

## Part 6: Troubleshooting

### Issue: "GROK_API_KEY not found"

**Solution**:
- Check HuggingFace Space secrets
- Verify key starts with `xai-`
- Restart Space after adding secret

### Issue: "Conversation not found"

**Solution**:
- Check localStorage in browser DevTools
- Verify conversation_id is valid
- Clear localStorage and start new conversation

### Issue: "Task 999 not found" (expected behavior)

**Solution**:
- This is correct error handling
- Agent should suggest listing tasks
- Verify agent response includes helpful message

### Issue: ChatKit not loading

**Solution**:
- Verify domain allowlisted on OpenAI
- Check VITE_OPENAI_DOMAIN_KEY in Vercel
- Verify frontend URL matches allowlisted domain
- Redeploy after environment variable changes

### Issue: Database migration failed

**Solution**:
```bash
# Check current migration version
alembic current

# Rollback to previous version
alembic downgrade -1

# Re-apply migration
alembic upgrade head

# Verify tables exist
psql $DATABASE_URL -c "\dt"
```

### Issue: CORS error in browser console

**Solution**:
- Check ALLOWED_ORIGINS in HuggingFace Space
- Must include frontend Vercel URL
- Format: `https://your-app.vercel.app` (no trailing slash)
- Restart Space after changing

### Issue: Phase 2 tasks not visible in chat

**Solution**:
- Verify same DATABASE_URL in Phase 2 and Phase 3
- Check user_id in JWT token matches Phase 2
- Test Phase 2 UI to confirm tasks exist
- Call list_tasks tool directly to debug

---

## Part 7: Monitoring & Maintenance

### Check Logs

**HuggingFace Backend Logs**:
1. Go to Space → Logs tab
2. Monitor for errors, API calls
3. Check Grok API rate limits

**Vercel Frontend Logs**:
1. Go to Project → Deployments → [Latest] → Logs
2. Monitor for frontend errors
3. Check API request failures

### Database Monitoring

```bash
# Count conversations
psql $DATABASE_URL -c "SELECT COUNT(*) FROM conversations;"

# Count messages
psql $DATABASE_URL -c "SELECT COUNT(*) FROM messages;"

# Recent conversations
psql $DATABASE_URL -c "SELECT id, user_id, created_at FROM conversations ORDER BY created_at DESC LIMIT 10;"
```

### Performance Metrics

**Target Metrics**:
- Chat response: < 3s p95
- Database queries: < 500ms p95
- Frontend load: < 2s initial

**Monitor**:
- HuggingFace Space response times
- Grok API latency
- Neon PostgreSQL query performance

---

## Part 8: Rollback Plan

### If Phase 3 Causes Issues

**Option 1: Disable Phase 3 (keep deployed)**
- Redirect users to Phase 2 URL
- Keep Phase 3 backend/frontend running (no traffic)
- Debug issues without time pressure

**Option 2: Database Rollback**
```bash
cd backend/
alembic downgrade -1
```
- Removes conversations and messages tables
- Phase 2 untouched (users, tasks intact)
- Lose Phase 3 conversation history (acceptable)

**Option 3: Full Rollback**
1. Pause HuggingFace Space
2. Disable Vercel deployment
3. Run database rollback
4. Announce Phase 2 remains operational

---

## Success Checklist

- [ ] Backend deployed to HuggingFace Spaces
- [ ] Frontend deployed to Vercel
- [ ] Domain allowlisted on OpenAI
- [ ] All environment variables configured
- [ ] Database migrations applied
- [ ] End-to-end test passed (add task, list, complete, delete, update)
- [ ] Conversation persistence verified
- [ ] Error handling tested (task 999)
- [ ] Phase 2 still operational (verified)
- [ ] Logs monitored (no errors)
- [ ] Public URLs accessible

**Production URLs**:
- Backend: `https://________.hf.space`
- Frontend: `https://________.vercel.app`
- Database: Neon PostgreSQL (shared with Phase 2)

**Next Steps**: Run `/sp.tasks` to generate implementation tasks
