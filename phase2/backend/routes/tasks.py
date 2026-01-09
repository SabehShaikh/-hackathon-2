"""
Task management routes for the Todo Backend API.

This module provides RESTful endpoints for CRUD operations on tasks,
with JWT authentication and user data isolation.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from datetime import datetime

from models import Task, TaskCreate, TaskUpdate
from database import get_session
from auth import get_current_user


# Create router with /api/tasks prefix
router = APIRouter(
    prefix="/api/tasks",
    tags=["tasks"]
)


@router.get("/", response_model=List[Task])
def list_tasks(
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Retrieve all tasks belonging to the authenticated user.

    Args:
        user_id: User ID extracted from JWT token (dependency)
        session: Database session (dependency)

    Returns:
        List[Task]: List of tasks owned by the user, ordered by created_at descending

    Raises:
        HTTPException: 401 Unauthorized if JWT token is invalid

    Example:
        GET /api/tasks
        Response: [{"id": 1, "title": "Buy groceries", ...}, ...]
    """
    # Query tasks for the authenticated user, ordered by newest first
    statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
    tasks = session.exec(statement).all()
    return tasks


@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.

    Args:
        task_data: Task creation data (title and optional description)
        user_id: User ID extracted from JWT token (dependency)
        session: Database session (dependency)

    Returns:
        Task: The created task with auto-generated ID and timestamps

    Raises:
        HTTPException: 401 Unauthorized if JWT token is invalid
        HTTPException: 422 Unprocessable Entity if validation fails

    Example:
        POST /api/tasks
        Body: {"title": "Buy groceries", "description": "Milk, eggs, bread"}
        Response: {"id": 1, "user_id": "user-123", "title": "Buy groceries", ...}
    """
    # Create new task with user_id from JWT token
    new_task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description
    )

    # Persist to database
    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    return new_task


@router.get("/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Retrieve a specific task by ID.

    Only returns the task if it belongs to the authenticated user.
    Returns 404 for both non-existent tasks and tasks owned by other users
    (prevents user enumeration).

    Args:
        task_id: Task ID to retrieve
        user_id: User ID extracted from JWT token (dependency)
        session: Database session (dependency)

    Returns:
        Task: The requested task

    Raises:
        HTTPException: 401 Unauthorized if JWT token is invalid
        HTTPException: 404 Not Found if task doesn't exist or wrong owner
        HTTPException: 422 Unprocessable Entity if task_id is not an integer

    Example:
        GET /api/tasks/1
        Response: {"id": 1, "user_id": "user-123", "title": "Buy groceries", ...}
    """
    # Retrieve task by ID
    task = session.get(Task, task_id)

    # Verify task exists and belongs to authenticated user
    if not task or task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a task's title and/or description.

    Only updates fields that are provided in the request body (partial update).
    The updated_at timestamp is automatically updated to the current time.

    Args:
        task_id: Task ID to update
        task_data: Task update data (optional title and description)
        user_id: User ID extracted from JWT token (dependency)
        session: Database session (dependency)

    Returns:
        Task: The updated task

    Raises:
        HTTPException: 401 Unauthorized if JWT token is invalid
        HTTPException: 404 Not Found if task doesn't exist or wrong owner
        HTTPException: 422 Unprocessable Entity if validation fails

    Example:
        PUT /api/tasks/1
        Body: {"title": "Updated title", "description": "Updated description"}
        Response: {"id": 1, "title": "Updated title", "updated_at": "2026-01-08T15:30:00Z", ...}
    """
    # Retrieve task by ID
    task = session.get(Task, task_id)

    # Verify task exists and belongs to authenticated user
    if not task or task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update only provided fields (partial update)
    if task_data.title is not None:
        task.title = task_data.title

    if task_data.description is not None:
        task.description = task_data.description

    # Update timestamp
    task.updated_at = datetime.utcnow()

    # Persist changes
    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.patch("/{task_id}/complete", response_model=Task)
def toggle_task_completion(
    task_id: int,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a task.

    Switches the completed field from false to true or true to false.
    The updated_at timestamp is automatically updated to the current time.

    Args:
        task_id: Task ID to toggle
        user_id: User ID extracted from JWT token (dependency)
        session: Database session (dependency)

    Returns:
        Task: The updated task with toggled completion status

    Raises:
        HTTPException: 401 Unauthorized if JWT token is invalid
        HTTPException: 404 Not Found if task doesn't exist or wrong owner

    Example:
        PATCH /api/tasks/1/complete
        Response: {"id": 1, "completed": true, "updated_at": "2026-01-08T16:00:00Z", ...}
    """
    # Retrieve task by ID
    task = session.get(Task, task_id)

    # Verify task exists and belongs to authenticated user
    if not task or task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle completion status
    task.completed = not task.completed

    # Update timestamp
    task.updated_at = datetime.utcnow()

    # Persist changes
    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Permanently delete a task.

    Only the task owner can delete it. Returns 204 No Content on success
    with no response body. The operation is idempotent - attempting to
    delete an already-deleted task returns 404.

    Args:
        task_id: Task ID to delete
        user_id: User ID extracted from JWT token (dependency)
        session: Database session (dependency)

    Returns:
        None: No response body (204 status indicates success)

    Raises:
        HTTPException: 401 Unauthorized if JWT token is invalid
        HTTPException: 404 Not Found if task doesn't exist or wrong owner

    Example:
        DELETE /api/tasks/1
        Response: 204 No Content (no body)
    """
    # Retrieve task by ID
    task = session.get(Task, task_id)

    # Verify task exists and belongs to authenticated user
    if not task or task.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Permanently delete task
    session.delete(task)
    session.commit()

    # FastAPI automatically returns 204 No Content
    return None
