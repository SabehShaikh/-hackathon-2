# Quickstart Guide: Todo Backend API

**Feature**: 001-todo-backend-api
**Date**: 2026-01-08
**Estimated Setup Time**: 10-15 minutes

## Prerequisites

### Required

- **Python 3.13+** installed ([python.org](https://www.python.org/downloads/))
  - Verify: `python --version` or `python3 --version`
- **pip** (Python package manager, included with Python)
  - Verify: `pip --version` or `pip3 --version`
- **Git** (for version control)
  - Verify: `git --version`

### Required Accounts/Services

- **Neon PostgreSQL Account** ([neon.tech](https://neon.tech))
  - Free tier available
  - Provides: Connection string (DATABASE_URL)
- **Better Auth Secret**
  - Shared secret key for JWT verification
  - Provided by frontend team or generated

### Optional but Recommended

- **Virtual Environment Tool** (venv, virtualenv, or conda)
- **Code Editor** (VS Code, PyCharm, Sublime)
- **API Testing Tool** (cURL, Postman, HTTPie)

---

## Step 1: Clone Repository

```bash
# If repository exists
git clone <repository-url>
cd phase2

# If starting fresh
mkdir -p backend
cd backend
```

---

## Step 2: Set Up Python Virtual Environment

**Why**: Isolates project dependencies from system Python.

### Using venv (built-in)

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Verify activation (prompt should show (venv))
which python  # Should point to venv/bin/python
```

**Note**: Keep virtual environment activated for all subsequent commands.

---

## Step 3: Create Project Structure

```bash
# Ensure you're in backend/ directory
mkdir -p routes
touch main.py models.py database.py auth.py routes/tasks.py
touch requirements.txt .env.example README.md
```

**Expected Structure**:
```
backend/
├── main.py
├── models.py
├── database.py
├── auth.py
├── routes/
│   └── tasks.py
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

---

## Step 4: Install Dependencies

### Create requirements.txt

```bash
cat > requirements.txt << 'EOF'
fastapi==0.109.0
sqlmodel==0.0.14
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
python-dotenv==1.0.0
uvicorn[standard]==0.27.0
EOF
```

### Install Dependencies

```bash
pip install -r requirements.txt

# Verify installation
pip list | grep fastapi
# Should show: fastapi 0.109.0
```

**Note**: This may take 2-3 minutes to download and install all packages.

---

## Step 5: Set Up Neon PostgreSQL Database

### 5.1 Create Neon Project

1. Go to [neon.tech](https://neon.tech) and sign in
2. Click **"New Project"**
3. Choose:
   - **Project Name**: todo-backend
   - **Region**: Select closest to you
   - **PostgreSQL Version**: 16 (default)
4. Click **"Create Project"**

### 5.2 Get Connection String

1. In Neon dashboard, go to **"Connection Details"**
2. Select **"Connection String"** format
3. Copy the connection string (looks like):
   ```
   postgresql://user:password@ep-xxx-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```

### 5.3 Test Connection (Optional)

```bash
# Install psql client if available
psql "postgresql://user:password@ep-xxx-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require"

# If connected successfully, you'll see:
# neondb=>

# Exit with \q
```

---

## Step 6: Configure Environment Variables

### 6.1 Create .env.example (Template)

```bash
cat > .env.example << 'EOF'
# Neon PostgreSQL connection string
DATABASE_URL=postgresql://user:password@host/dbname?sslmode=require

# Shared secret for JWT verification (must match Better Auth)
BETTER_AUTH_SECRET=your-secret-key-min-32-characters

# CORS allowed origins (comma-separated)
ALLOWED_ORIGINS=http://localhost:3000
EOF
```

### 6.2 Create .env (Actual Secrets)

```bash
# Copy template
cp .env.example .env

# Edit .env with real values
# Use your favorite editor (nano, vim, code, etc.)
nano .env
```

**Fill in**:
```
DATABASE_URL=postgresql://YOUR_USER:YOUR_PASSWORD@YOUR_HOST/neondb?sslmode=require
BETTER_AUTH_SECRET=your-actual-secret-key-here-must-be-at-least-32-chars
ALLOWED_ORIGINS=http://localhost:3000
```

**Important**:
- `DATABASE_URL`: Paste your Neon connection string from Step 5.2
- `BETTER_AUTH_SECRET`: Use the SAME secret as your frontend Better Auth
- `ALLOWED_ORIGINS`: Frontend URL (localhost:3000 for development)

### 6.3 Secure .env File

```bash
# Add to .gitignore (prevent committing secrets)
echo ".env" >> .gitignore
echo "venv/" >> .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
```

---

## Step 7: Implement Core Files

**Note**: Follow implementation plan for detailed code. Placeholder stubs below:

### 7.1 models.py (Task Model)

```python
from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True, max_length=255)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### 7.2 database.py (DB Connection)

```python
from sqlmodel import create_engine, Session
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    better_auth_secret: str
    allowed_origins: str

    class Config:
        env_file = ".env"

settings = Settings()
engine = create_engine(settings.database_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
```

### 7.3 auth.py (JWT Verification)

```python
from fastapi import Header, HTTPException
from jose import JWTError, jwt
from database import settings

def get_current_user(authorization: str = Header(...)) -> str:
    try:
        token = authorization.replace("Bearer ", "")
        payload = jwt.decode(
            token,
            settings.better_auth_secret,
            algorithms=["HS256"]
        )
        user_id = payload.get("userId")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### 7.4 routes/tasks.py (Endpoints - Stub)

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from models import Task
from database import get_session
from auth import get_current_user

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.get("/")
def list_tasks(
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
    return tasks

# TODO: Implement other endpoints (POST, GET /{id}, PUT, PATCH, DELETE)
```

### 7.5 main.py (FastAPI App)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from database import engine, settings
from routes import tasks

app = FastAPI(title="Todo Backend API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks.router)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}
```

---

## Step 8: Create Database Tables

```bash
# Start Python interpreter
python

# Run table creation
>>> from main import app
>>> from database import engine
>>> from sqlmodel import SQLModel
>>> SQLModel.metadata.create_all(engine)
# Should see SQL CREATE TABLE statements
>>> exit()
```

**Alternative**: Tables auto-create on first server startup (main.py on_event("startup")).

---

## Step 9: Start Development Server

```bash
# Start server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Expected output:
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process
# INFO:     Started server process
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
```

**Flags**:
- `--reload`: Auto-restart on code changes (development only)
- `--host 0.0.0.0`: Accept connections from any IP
- `--port 8000`: Listen on port 8000

**Note**: Keep terminal open (server running).

---

## Step 10: Test API

### 10.1 Test Health Check (No Auth)

```bash
curl http://localhost:8000/api/health

# Expected:
# {"status":"healthy"}
```

### 10.2 View API Documentation

Open browser:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 10.3 Generate Test JWT Token

**For Testing Only** (generate a test token):

```python
# In Python REPL
from jose import jwt
from datetime import datetime, timedelta

SECRET = "your-secret-key-min-32-characters"  # Same as .env
payload = {
    "userId": "test-user-123",
    "exp": datetime.utcnow() + timedelta(days=1)
}
token = jwt.encode(payload, SECRET, algorithm="HS256")
print(token)
# Copy this token for testing
```

### 10.4 Test List Tasks (With Auth)

```bash
TOKEN="your-generated-token-here"

curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/api/tasks

# Expected (empty list first time):
# []
```

### 10.5 Test Create Task

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "description": "Testing API"}'

# Expected:
# {"id":1,"user_id":"test-user-123","title":"Test task",...}
```

### 10.6 Test List Tasks Again

```bash
curl -H "Authorization: Bearer $TOKEN" \
     http://localhost:8000/api/tasks

# Expected (with created task):
# [{"id":1,"user_id":"test-user-123","title":"Test task",...}]
```

---

## Common Issues & Solutions

### Issue 1: ModuleNotFoundError

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

---

### Issue 2: Database Connection Error

**Error**: `sqlalchemy.exc.OperationalError: could not connect to server`

**Solution**:
- Verify `DATABASE_URL` in `.env` is correct
- Check Neon project is not paused (free tier auto-pauses after inactivity)
- Test connection: `psql "YOUR_DATABASE_URL"`

---

### Issue 3: JWT Verification Fails

**Error**: `401 Unauthorized: Invalid token`

**Solution**:
- Ensure `BETTER_AUTH_SECRET` in `.env` matches frontend
- Check JWT token is not expired
- Verify `Authorization` header format: `Bearer <token>` (note the space)

---

### Issue 4: CORS Error in Browser

**Error**: `Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy`

**Solution**:
- Verify `ALLOWED_ORIGINS` in `.env` includes `http://localhost:3000`
- Restart server after changing `.env` file
- Check CORSMiddleware configuration in `main.py`

---

### Issue 5: Port Already in Use

**Error**: `OSError: [Errno 48] Address already in use`

**Solution**:
```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or use different port
uvicorn main:app --reload --port 8001
```

---

## Development Workflow

### Making Code Changes

1. **Edit code** in your editor
2. **Server auto-reloads** (if `--reload` flag used)
3. **Test changes** via curl or browser
4. **Check logs** in terminal running uvicorn

### Stopping Server

```bash
# In terminal running uvicorn
Ctrl+C

# Server will gracefully shutdown
```

### Restarting Server

```bash
# If --reload flag used: Just save files, auto-reloads
# If no --reload: Stop (Ctrl+C) and restart (uvicorn main:app ...)
```

### Database Changes

**If model changes** (e.g., add field to Task):
1. Update `models.py`
2. For now: Drop and recreate tables (loses data)
   ```python
   from sqlmodel import SQLModel
   from database import engine
   SQLModel.metadata.drop_all(engine)
   SQLModel.metadata.create_all(engine)
   ```
3. Future: Use Alembic migrations (preserve data)

---

## Next Steps

After quickstart setup:

1. **Implement remaining endpoints** (POST, PUT, PATCH, DELETE) - See implementation plan
2. **Add error handling** for edge cases
3. **Test with real Better Auth JWT tokens** (from frontend)
4. **Add logging** for debugging
5. **Write tests** (pytest with TestClient)
6. **Deploy to production** (see deployment guide)

---

## Quickstart Checklist

Setup Verification:

- [ ] Python 3.13+ installed (`python --version`)
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip list | grep fastapi`)
- [ ] Neon PostgreSQL project created
- [ ] Database connection string obtained
- [ ] `.env` file created with all 3 variables
- [ ] `.env` added to `.gitignore`
- [ ] Project structure created (main.py, models.py, etc.)
- [ ] Database tables created (auto or manual)
- [ ] Server starts successfully (`uvicorn main:app --reload`)
- [ ] Health check works (`curl http://localhost:8000/api/health`)
- [ ] Swagger docs accessible (`http://localhost:8000/docs`)
- [ ] Test JWT token generated
- [ ] List tasks endpoint works (returns empty array)
- [ ] Create task endpoint works (returns task object)

All checked? You're ready to implement full CRUD operations!

---

## Support & Resources

**Documentation**:
- FastAPI: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- SQLModel: [sqlmodel.tiangolo.com](https://sqlmodel.tiangolo.com)
- Neon: [neon.tech/docs](https://neon.tech/docs)

**Troubleshooting**:
- Check server logs in terminal running uvicorn
- Use Swagger UI for interactive testing: `http://localhost:8000/docs`
- Validate JWT tokens: [jwt.io](https://jwt.io)

**Constitution Compliance**:
- All setup steps follow constitution principles
- Environment variables for secrets ✅
- SQLModel for database operations ✅
- JWT authentication configured ✅
- API-first design (RESTful endpoints) ✅
