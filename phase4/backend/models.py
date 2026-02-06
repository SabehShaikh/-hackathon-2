"""
Data models for Phase 3 Todo AI Chatbot.

This module defines SQLModel entities for:
- User (Phase 2 - unchanged)
- Task (Phase 2 - unchanged)
- Conversation (Phase 3 - new)
- Message (Phase 3 - new)

And Pydantic schemas for request/response validation.
"""

from sqlmodel import Field, SQLModel, Column
from sqlalchemy import Enum as SAEnum
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from enum import Enum


# ============================================================================
# Phase 2 Models (DO NOT MODIFY - copied for compatibility)
# ============================================================================

class User(SQLModel, table=True):
    """
    User entity for authentication.
    Phase 2 model - DO NOT MODIFY.
    """
    __tablename__ = "users"

    id: str = Field(primary_key=True, max_length=255)
    email: str = Field(unique=True, index=True, max_length=255, nullable=False)
    hashed_password: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class Task(SQLModel, table=True):
    """
    Task entity representing a todo item.
    Phase 2 model - DO NOT MODIFY.
    """
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        max_length=255,
        nullable=False
    )
    title: str = Field(min_length=1, max_length=200, nullable=False)
    description: Optional[str] = Field(default=None, max_length=1000, nullable=True)
    completed: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


# ============================================================================
# Phase 3 Models (NEW)
# ============================================================================

class Conversation(SQLModel, table=True):
    """
    Chat conversation between user and AI agent.
    Persists conversation context for multi-session continuity.
    """
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class MessageRole(str, Enum):
    """Message sender role"""
    USER = "user"
    ASSISTANT = "assistant"


class Message(SQLModel, table=True):
    """
    Individual message in a conversation.
    Stores both user inputs and AI responses.
    """
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(foreign_key="users.id", index=True, max_length=255)
    role: str = Field(max_length=20)  # "user" or "assistant"
    content: str = Field(max_length=10000)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# Phase 2 Request/Response Schemas (for auth compatibility)
# ============================================================================

class TaskCreate(BaseModel):
    """Request body for creating a new task."""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)


class TaskUpdate(BaseModel):
    """Request body for updating a task."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)


class UserSignup(BaseModel):
    """Request body for user signup."""
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=8, max_length=100)


class UserLogin(BaseModel):
    """Request body for user login."""
    email: str = Field(min_length=3, max_length=255)
    password: str = Field(min_length=1, max_length=100)


class AuthResponse(BaseModel):
    """Response body for successful authentication."""
    token: str
    user: dict


# ============================================================================
# Phase 3 Request/Response Schemas (NEW)
# ============================================================================

class ChatRequest(BaseModel):
    """Request body for chat messages."""
    conversation_id: Optional[int] = None
    message: str = Field(min_length=1, max_length=1000)

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": 123,
                "message": "Add buy groceries"
            }
        }


class ToolCallResult(BaseModel):
    """Result from an MCP tool call."""
    tool: str
    parameters: dict
    result: dict


class ChatResponse(BaseModel):
    """Response body for chat messages."""
    conversation_id: int
    response: str
    tool_calls: List[ToolCallResult] = []

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": 123,
                "response": "✅ Added task: Buy groceries",
                "tool_calls": [
                    {
                        "tool": "add_task",
                        "parameters": {"user_id": "user123", "title": "Buy groceries"},
                        "result": {"status": "success", "data": {"task_id": 45}}
                    }
                ]
            }
        }
