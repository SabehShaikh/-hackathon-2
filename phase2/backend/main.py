"""
Todo Backend API - Main Application

FastAPI application providing RESTful API for todo task management
with JWT authentication and PostgreSQL persistence.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from database import engine, settings
from routes import tasks, auth


# Create FastAPI application
app = FastAPI(
    title="Todo Backend API",
    version="1.0.0",
    description="RESTful API for todo task management with JWT authentication"
)

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins.split(","),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)



@app.on_event("startup")
def on_startup():
    """
    Application startup event.

    Creates database tables if they don't exist. This is idempotent -
    safe to run multiple times.
    """
    try:
        SQLModel.metadata.create_all(engine)
        print("✓ Database tables created successfully")
    except Exception as e:
        print(f"⚠ Warning: Could not create database tables: {e}")
        print("The app will start but database operations may fail")


@app.get("/api/health")
def health_check():
    """
    Health check endpoint (no authentication required).

    Returns:
        dict: Health status and database connectivity

    Example:
        GET /api/health
        Response: {"status": "healthy", "database": "connected"}
    """
    db_status = "unknown"
    try:
        # Test database connection
        from sqlmodel import text, Session
        with Session(engine) as session:
            session.exec(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)[:100]}"

    return {
        "status": "healthy",
        "database": db_status,
        "message": "Backend API is running"
    }
