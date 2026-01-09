"""
Database configuration and connection management.

This module handles database engine creation, session management,
and environment configuration using Pydantic Settings.
"""

from sqlmodel import create_engine, Session
from pydantic_settings import BaseSettings
from typing import Generator
import os


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes:
        database_url: PostgreSQL connection string (from DATABASE_URL)
        better_auth_secret: JWT signing secret shared with Better Auth
        allowed_origins: Comma-separated list of CORS allowed origins
    """
    database_url: str
    better_auth_secret: str
    allowed_origins: str = "*"  # Default to allow all origins (can be restricted via env var)

    class Config:
        # Use .env file if it exists (local dev), otherwise use system env vars (HF Spaces)
        env_file = ".env" if os.path.exists(".env") else None
        env_file_encoding = "utf-8"
        extra = "ignore"  # Ignore extra environment variables


# Instantiate settings (loaded from .env file or environment variables)
try:
    settings = Settings()
    print(f"✓ Settings loaded successfully")
    print(f"  - DATABASE_URL: {'set' if settings.database_url else 'missing'}")
    print(f"  - BETTER_AUTH_SECRET: {'set' if settings.better_auth_secret else 'missing'}")
    print(f"  - ALLOWED_ORIGINS: {settings.allowed_origins}")
except Exception as e:
    print(f"⚠ ERROR loading settings: {e}")
    print("Please ensure DATABASE_URL and BETTER_AUTH_SECRET environment variables are set")
    raise

# Create database engine
engine = create_engine(
    settings.database_url,
    echo=True,  # Log SQL statements (disable in production)
    pool_pre_ping=True,  # Verify connections before using them
)


def get_session() -> Generator[Session, None, None]:
    """
    Database session dependency for FastAPI.

    Yields a SQLModel session that automatically commits or rolls back
    on completion. Use with FastAPI Depends() for dependency injection.

    Yields:
        Session: SQLModel database session

    Example:
        @app.get("/tasks")
        def get_tasks(session: Session = Depends(get_session)):
            return session.exec(select(Task)).all()
    """
    with Session(engine) as session:
        yield session
