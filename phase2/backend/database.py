"""
Database configuration and connection management.

This module handles database engine creation, session management,
and environment configuration using Pydantic Settings.
"""

from sqlmodel import create_engine, Session
from pydantic_settings import BaseSettings
from typing import Generator


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
    allowed_origins: str

    class Config:
        env_file = ".env"


# Instantiate settings (loaded from .env file)
settings = Settings()

# Create database engine
engine = create_engine(
    settings.database_url,
    echo=True,  # Log SQL statements (disable in production)
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
