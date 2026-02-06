"""
Task REST API routes for dashboard.

Phase 2 compatible - Provides traditional CRUD endpoints
for the dashboard UI to manage tasks without AI chat.
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from datetime import datetime
from typing import List

from models import Task, TaskCreate, TaskUpdate
from database import get_session
from auth import get_current_user

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("", response_model=List[dict])
def get_tasks(
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the current user.
    """
    try:
        statement = select(Task).where(Task.user_id == user_id).order_by(Task.created_at.desc())
        tasks = session.exec(statement).all()

        return [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "createdAt": task.created_at.isoformat(),
                "updatedAt": task.updated_at.isoformat()
            }
            for task in tasks
        ]
    except Exception as e:
        print(f"Get tasks error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch tasks")


@router.post("", response_model=dict, status_code=201)
def create_task(
    task_data: TaskCreate,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task.
    """
    try:
        new_task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description
        )

        session.add(new_task)
        session.commit()
        session.refresh(new_task)

        return {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "completed": new_task.completed,
            "createdAt": new_task.created_at.isoformat(),
            "updatedAt": new_task.updated_at.isoformat()
        }
    except Exception as e:
        print(f"Create task error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create task")


@router.patch("/{task_id}", response_model=dict)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update an existing task.
    """
    try:
        task = session.get(Task, task_id)

        if not task or task.user_id != user_id:
            raise HTTPException(status_code=404, detail="Task not found")

        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description

        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "createdAt": task.created_at.isoformat(),
            "updatedAt": task.updated_at.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Update task error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update task")


@router.patch("/{task_id}/complete", response_model=dict)
def toggle_task_complete(
    task_id: int,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle task completion status.
    """
    try:
        task = session.get(Task, task_id)

        if not task or task.user_id != user_id:
            raise HTTPException(status_code=404, detail="Task not found")

        task.completed = not task.completed
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)

        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "completed": task.completed,
            "createdAt": task.created_at.isoformat(),
            "updatedAt": task.updated_at.isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Toggle complete error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to toggle task completion")


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: int,
    user_id: str = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a task.
    """
    try:
        task = session.get(Task, task_id)

        if not task or task.user_id != user_id:
            raise HTTPException(status_code=404, detail="Task not found")

        session.delete(task)
        session.commit()

        return None
    except HTTPException:
        raise
    except Exception as e:
        print(f"Delete task error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete task")
