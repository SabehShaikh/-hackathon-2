"""
Phase 3: Todo AI Chatbot Backend - Main Application

FastAPI application providing:
- RESTful API for todo task management (Phase 2 compatibility)
- Chat endpoint for AI-powered task management (Phase 3 new)
- JWT authentication
- PostgreSQL persistence
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from database import engine, settings
from routes import auth, chat, tasks

# Create FastAPI application
app = FastAPI(
    title="Todo AI Chatbot API",
    version="1.0.0",
    description="AI-powered todo task management with natural language interface"
)

# Configure CORS middleware FIRST (must be before routers)
# Include both localhost for development and production URLs
base_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "http://127.0.0.1:3002",
    # Production URLs
    "https://todo-vxwd.vercel.app",
    "https://sabehshaikh-hackathon2-phase3.hf.space",
]

# Add any extra origins from ALLOWED_ORIGINS env var
extra_origins = [o.strip() for o in settings.allowed_origins.split(",") if o.strip() and o.strip() != "*"]
origins = list(set(base_origins + extra_origins))  # Deduplicate
print(f"[CORS] Allowed origins: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers AFTER middleware
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(tasks.router)


@app.on_event("startup")
def on_startup():
    """
    Application startup event.
    Creates database tables if they don't exist.
    """
    try:
        SQLModel.metadata.create_all(engine)
        print("[OK] Database tables created/verified successfully")
    except Exception as e:
        print(f"[WARNING] Could not create database tables: {e}")
        print("The app will start but database operations may fail")


@app.get("/api/health")
def health_check():
    """
    Health check endpoint (no authentication required).
    """
    db_status = "unknown"
    try:
        from sqlmodel import text, Session
        with Session(engine) as session:
            session.exec(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)[:100]}"

    return {
        "status": "healthy",
        "database": db_status,
        "message": "Phase 3 Todo AI Chatbot API is running"
    }


@app.get("/")
def root():
    """Root endpoint - redirect to docs."""
    return {
        "message": "Todo AI Chatbot API",
        "docs": "/docs",
        "health": "/api/health"
    }
