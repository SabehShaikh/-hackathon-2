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
    SQLModel.metadata.create_all(engine)


@app.get("/api/health")
def health_check():
    """
    Health check endpoint (no authentication required).

    Returns:
        dict: Health status and timestamp

    Example:
        GET /api/health
        Response: {"status": "healthy"}
    """
    return {"status": "healthy"}
