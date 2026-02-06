"""
MCP Tools for Task Management Agent.

This module implements the 5 MCP tools following the mcp-tool-pattern:
- add_task: Create a new task
- list_tasks: Retrieve user's tasks with optional filtering
- complete_task: Mark a task as completed
- delete_task: Delete a task permanently
- update_task: Update task title and/or description

All tools return a standardized response format:
{
    "status": "success" | "error",
    "data": {...},
    "message": "User-friendly message"
}
"""

from sqlmodel import Session, select
from datetime import datetime
from typing import Optional, List, Dict, Any, Literal

from models import Task


def add_task(
    user_id: str,
    title: str,
    description: Optional[str] = None,
    session: Session = None
) -> Dict[str, Any]:
    """
    Create a new task for the user.

    Call this when user wants to add, create, or remember something.

    Args:
        user_id: User identifier from JWT token
        title: Task title (required, 1-500 chars)
        description: Optional task description

    Returns:
        Dict with status, data (task_id, title), and message
    """
    try:
        # Validate title
        if not title or not title.strip():
            return {
                "status": "error",
                "data": {},
                "message": "Task title cannot be empty"
            }

        # Create new task
        task = Task(
            user_id=user_id,
            title=title.strip(),
            description=description.strip() if description else None,
            completed=False
        )

        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "status": "success",
            "data": {
                "task_id": task.id,
                "title": task.title
            },
            "message": f"Task created: {task.title}"
        }

    except Exception as e:
        return {
            "status": "error",
            "data": {},
            "message": f"Failed to create task: {str(e)}"
        }


def list_tasks(
    user_id: str,
    status: Literal["all", "pending", "completed"] = "all",
    session: Session = None
) -> Dict[str, Any]:
    """
    Retrieve user's tasks with optional filtering.

    Call this when user wants to see, list, or check their tasks.

    Args:
        user_id: User identifier from JWT token
        status: Filter by completion status ("all", "pending", "completed")

    Returns:
        Dict with status, data (array of tasks), and message
    """
    try:
        # Build query
        query = select(Task).where(Task.user_id == user_id)

        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)

        query = query.order_by(Task.created_at.desc())

        # Execute query
        tasks = session.exec(query).all()

        # Format response
        task_list = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description or "",
                "completed": task.completed
            }
            for task in tasks
        ]

        # Generate message
        if not task_list:
            message = "You don't have any tasks yet. Want to add one?"
        elif status == "pending":
            message = f"You have {len(task_list)} pending task{'s' if len(task_list) != 1 else ''}"
        elif status == "completed":
            message = f"You have {len(task_list)} completed task{'s' if len(task_list) != 1 else ''}"
        else:
            message = f"You have {len(task_list)} task{'s' if len(task_list) != 1 else ''}"

        return {
            "status": "success",
            "data": task_list,
            "message": message
        }

    except Exception as e:
        return {
            "status": "error",
            "data": [],
            "message": f"Failed to retrieve tasks: {str(e)}"
        }


def complete_task(
    user_id: str,
    task_id: int,
    session: Session = None
) -> Dict[str, Any]:
    """
    Mark a task as completed.

    Call this when user says they finished, completed, or are done with a task.

    Args:
        user_id: User identifier for authorization
        task_id: Task ID to mark as completed

    Returns:
        Dict with status, data (task_id, title), and message
    """
    try:
        # Find task
        task = session.get(Task, task_id)

        if not task:
            return {
                "status": "error",
                "data": {},
                "message": f"Task {task_id} not found"
            }

        # Authorization check
        if task.user_id != user_id:
            return {
                "status": "error",
                "data": {},
                "message": f"Task {task_id} not found"
            }

        # Already completed?
        if task.completed:
            return {
                "status": "success",
                "data": {
                    "task_id": task.id,
                    "title": task.title
                },
                "message": f"Task '{task.title}' was already completed"
            }

        # Mark as completed
        task.completed = True
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()

        return {
            "status": "success",
            "data": {
                "task_id": task.id,
                "title": task.title
            },
            "message": f"Completed task: {task.title}"
        }

    except Exception as e:
        return {
            "status": "error",
            "data": {},
            "message": f"Failed to complete task: {str(e)}"
        }


def delete_task(
    user_id: str,
    task_id: int,
    session: Session = None
) -> Dict[str, Any]:
    """
    Delete a task permanently.

    Call this when user wants to remove, delete, or cancel a task.

    Args:
        user_id: User identifier for authorization
        task_id: Task ID to delete

    Returns:
        Dict with status, data (task_id, title), and message
    """
    try:
        # Find task
        task = session.get(Task, task_id)

        if not task:
            return {
                "status": "error",
                "data": {},
                "message": f"Task {task_id} not found"
            }

        # Authorization check
        if task.user_id != user_id:
            return {
                "status": "error",
                "data": {},
                "message": f"Task {task_id} not found"
            }

        # Delete task
        title = task.title
        session.delete(task)
        session.commit()

        return {
            "status": "success",
            "data": {
                "task_id": task_id,
                "title": title
            },
            "message": f"Deleted task: {title}"
        }

    except Exception as e:
        return {
            "status": "error",
            "data": {},
            "message": f"Failed to delete task: {str(e)}"
        }


def update_task(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    session: Session = None
) -> Dict[str, Any]:
    """
    Update task title and/or description.

    Call this when user wants to change, modify, or rename a task.

    Args:
        user_id: User identifier for authorization
        task_id: Task ID to update
        title: New task title (optional)
        description: New task description (optional)

    Returns:
        Dict with status, data (task_id, title, description), and message
    """
    try:
        # Validate at least one field provided
        if not title and description is None:
            return {
                "status": "error",
                "data": {},
                "message": "At least one field (title or description) must be provided"
            }

        # Find task
        task = session.get(Task, task_id)

        if not task:
            return {
                "status": "error",
                "data": {},
                "message": f"Task {task_id} not found"
            }

        # Authorization check
        if task.user_id != user_id:
            return {
                "status": "error",
                "data": {},
                "message": f"Task {task_id} not found"
            }

        # Update fields
        if title:
            task.title = title.strip()
        if description is not None:
            task.description = description.strip() if description else None

        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)

        # Generate appropriate message
        if title and description is not None:
            message = f"Updated task {task_id}: {task.title}"
        elif title:
            message = f"Updated task {task_id}: {task.title}"
        else:
            message = f"Updated task {task_id} description"

        return {
            "status": "success",
            "data": {
                "task_id": task.id,
                "title": task.title,
                "description": task.description or ""
            },
            "message": message
        }

    except Exception as e:
        return {
            "status": "error",
            "data": {},
            "message": f"Failed to update task: {str(e)}"
        }


# Tool definitions for agent integration
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new task for the user. Call this when user wants to add, create, or remember something.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Task title (required). Extract from natural language input."
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional task description with additional details"
                    }
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "Retrieve user's tasks with optional filtering. Call this when user wants to see, list, or check their tasks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "description": "Filter tasks by completion status. 'pending' = incomplete tasks only, 'completed' = done tasks only."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed. Call this when user says they finished, completed, or are done with a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "Task ID to mark as completed"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task permanently. Call this when user wants to remove, delete, or cancel a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "Task ID to delete"
                    }
                },
                "required": ["task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update task title and/or description. Call this when user wants to change, modify, or rename a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "Task ID to update"
                    },
                    "title": {
                        "type": "string",
                        "description": "New task title (optional if updating description only)"
                    },
                    "description": {
                        "type": "string",
                        "description": "New task description (optional if updating title only)"
                    }
                },
                "required": ["task_id"]
            }
        }
    }
]
