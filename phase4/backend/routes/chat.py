"""
Chat routes for AI-powered task management.

Phase 3 - Provides the POST /api/chat endpoint for
natural language interaction with the task management agent.

Features:
- Conversation persistence
- Error handling with specific messages
- Logging for debugging
"""

import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from datetime import datetime
from typing import List

from models import (
    ChatRequest, ChatResponse, ToolCallResult,
    Conversation, Message, Task
)
from database import get_session
from auth import get_current_user

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def send_chat_message(
    request: ChatRequest,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Send a chat message to the AI agent.

    The agent interprets natural language and manages tasks
    using MCP tools (add, list, complete, delete, update).

    Conversation history persists in database for multi-session continuity.

    Args:
        request: ChatRequest with message and optional conversation_id
        user_id: Authenticated user ID (from JWT)
        session: Database session

    Returns:
        ChatResponse with conversation_id, response text, and tool_calls

    Raises:
        HTTPException: 404 if conversation not found
        HTTPException: 500 on processing errors (with specific messages)
    """
    conversation = None

    try:
        # Get or create conversation
        if request.conversation_id:
            # Load existing conversation
            conversation = session.get(Conversation, request.conversation_id)
            if not conversation or conversation.user_id != user_id:
                raise HTTPException(
                    status_code=404,
                    detail="Conversation not found or does not belong to user"
                )
        else:
            # Create new conversation
            conversation = Conversation(user_id=user_id)
            session.add(conversation)
            session.commit()
            session.refresh(conversation)

        # Validate message
        if not request.message or not request.message.strip():
            return ChatResponse(
                conversation_id=conversation.id,
                response="Please enter a message. I can help you add, list, complete, update, or delete tasks.",
                tool_calls=[]
            )

        # Store user message
        user_message = Message(
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content=request.message.strip()
        )
        session.add(user_message)
        session.commit()

        # Load conversation history for context
        messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at)
        ).all()

        # Process with agent
        from agent import process_message
        response_text, tool_calls = await process_message(
            user_id=user_id,
            message=request.message.strip(),
            history=messages,
            session=session
        )

        # Ensure we have a response
        if not response_text:
            response_text = "I processed your request but have no additional response."

        # Store assistant response
        assistant_message = Message(
            conversation_id=conversation.id,
            user_id=user_id,
            role="assistant",
            content=response_text
        )
        session.add(assistant_message)

        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()

        logger.info(f"Chat processed for user {user_id}: {len(tool_calls)} tool calls")

        return ChatResponse(
            conversation_id=conversation.id,
            response=response_text,
            tool_calls=tool_calls
        )

    except HTTPException:
        # Re-raise HTTP exceptions (like 404)
        raise
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Chat error for user {user_id}: {error_msg}")

        # Provide specific error messages based on error type
        error_lower = error_msg.lower()

        if "rate" in error_lower or "429" in error_msg or "quota" in error_lower:
            detail = "I'm currently experiencing high demand. Please wait a moment and try again."
        elif "timeout" in error_lower or "timed out" in error_lower:
            detail = "The request took too long. Please try a simpler request or try again."
        elif "connection" in error_lower or "network" in error_lower:
            detail = "Having trouble connecting to the AI service. Please try again."
        elif "database" in error_lower or "sql" in error_lower:
            detail = "A database error occurred. Please try again."
        else:
            # Generic but still informative
            detail = "Something went wrong processing your request. Please try again."

        raise HTTPException(
            status_code=500,
            detail=detail
        )


@router.get("/conversations", response_model=List[dict])
def get_conversations(
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all conversations for the current user.

    Returns conversations ordered by most recent first.
    """
    try:
        conversations = session.exec(
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
        ).all()

        return [
            {
                "id": conv.id,
                "createdAt": conv.created_at.isoformat(),
                "updatedAt": conv.updated_at.isoformat()
            }
            for conv in conversations
        ]
    except Exception as e:
        logger.error(f"Get conversations error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch conversations")


@router.get("/conversations/{conversation_id}/messages", response_model=List[dict])
def get_conversation_messages(
    conversation_id: int,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all messages for a specific conversation.

    Returns messages ordered chronologically.
    """
    try:
        # Verify conversation belongs to user
        conversation = session.get(Conversation, conversation_id)
        if not conversation or conversation.user_id != user_id:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found"
            )

        messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        ).all()

        return [
            {
                "id": msg.id,
                "role": msg.role,
                "content": msg.content,
                "createdAt": msg.created_at.isoformat()
            }
            for msg in messages
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get messages error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch messages")
