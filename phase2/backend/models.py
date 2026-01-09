"""
Data models for the Todo Backend API.

This module defines the SQLModel Task entity and Pydantic schemas
for request/response validation.
"""

from sqlmodel import Field, SQLModel
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class User(SQLModel, table=True):
    """
    User entity for authentication.

    Attributes:
        id: Auto-generated unique user ID (UUID format)
        email: User's email address (unique, used for login)
        hashed_password: Bcrypt hashed password
        created_at: Account creation timestamp
    """
    __tablename__ = "users"

    id: str = Field(primary_key=True, max_length=255)
    email: str = Field(unique=True, index=True, max_length=255, nullable=False)
    hashed_password: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class Task(SQLModel, table=True):
    """
    Task entity representing a todo item.

    Attributes:
        id: Auto-generated primary key
        user_id: Owner's user ID from JWT token (FK to users.id)
        title: Task title, 1-200 characters, required
        description: Optional task description, max 1000 characters
        completed: Completion status, defaults to False
        created_at: Creation timestamp, auto-set
        updated_at: Last modification timestamp, auto-updated
    """
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        max_length=255,
        nullable=False
    )
    title: str = Field(
        min_length=1,
        max_length=200,
        nullable=False
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        nullable=True
    )
    completed: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )


class TaskCreate(BaseModel):
    """Request body for creating a new task."""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread"
            }
        }


class TaskUpdate(BaseModel):
    """Request body for updating a task."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries and cook dinner",
                "description": "Milk, eggs, bread, chicken"
            }
        }


class UserSignup(BaseModel):
    """Request body for user signup."""
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=100)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }


class UserLogin(BaseModel):
    """Request body for user login."""
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=1, max_length=100)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }


class AuthResponse(BaseModel):
    """Response body for successful authentication."""
    token: str
    user: dict

    class Config:
        json_schema_extra = {
            "example": {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "user": {
                    "id": "user-123",
                    "email": "user@example.com"
                }
            }
        }
