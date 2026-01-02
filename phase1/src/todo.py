"""Todo business logic layer - data structures, CRUD operations, and validation."""

from datetime import datetime
from typing import Any

# Module-level storage
tasks: list[dict[str, Any]] = []
next_id: int = 1


def validate_title(title: str) -> tuple[bool, str]:
    """Validate a task title.

    Args:
        title: Title string to validate

    Returns:
        Tuple of (valid, error_message):
        - valid (bool): True if valid, False otherwise
        - error_message (str): Empty if valid, error description if invalid
    """
    if not title.strip():
        return (False, "Title cannot be empty. Please enter a title.")
    if len(title) > 200:
        return (False, "Title too long (max 200 characters). Please shorten.")
    return (True, "")


def validate_description(description: str) -> tuple[bool, str]:
    """Validate a task description.

    Args:
        description: Description string to validate

    Returns:
        Tuple of (valid, error_message):
        - valid (bool): True if valid, False otherwise
        - error_message (str): Empty if valid, error description if invalid
    """
    if len(description) > 1000:
        return (False, "Description too long (max 1000 characters). Please shorten.")
    return (True, "")


def add_task(title: str, description: str = "") -> tuple[bool, int | None, str]:
    """Add a new task to the task list.

    Args:
        title: Task title (1-200 characters, required)
        description: Task description (max 1000 characters, optional)

    Returns:
        Tuple of (success, task_id, message):
        - success (bool): True if task created, False if validation failed
        - task_id (int | None): ID of created task, or None if failed
        - message (str): Confirmation or error message
    """
    global next_id

    # Validate title
    is_valid, error_msg = validate_title(title)
    if not is_valid:
        return (False, None, error_msg)

    # Validate description
    is_valid, error_msg = validate_description(description)
    if not is_valid:
        return (False, None, error_msg)

    # Create task
    task_id = next_id
    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    tasks.append(task)
    next_id += 1

    return (True, task_id, f"Task #{task_id} created successfully!")


def get_all_tasks() -> list[dict[str, Any]]:
    """Retrieve all tasks ordered by ID.

    Returns:
        List of task dictionaries (may be empty)
    """
    return tasks.copy()


def get_task_by_id(task_id: int) -> dict[str, Any] | None:
    """Find a task by its ID.

    Args:
        task_id: Task ID to search for

    Returns:
        Task dictionary if found, None otherwise
    """
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def toggle_complete(task_id: int) -> tuple[bool, bool | None, str]:
    """Toggle the completion status of a task.

    Args:
        task_id: ID of task to toggle

    Returns:
        Tuple of (success, new_status, message):
        - success (bool): True if toggled, False if task not found
        - new_status (bool | None): New completed value, or None if failed
        - message (str): Confirmation or error message
    """
    task = get_task_by_id(task_id)
    if task is None:
        return (False, None, f"Task ID {task_id} not found. Please try again.")

    task["completed"] = not task["completed"]
    new_status = task["completed"]

    if new_status:
        message = f"Task #{task_id} marked as complete!"
    else:
        message = f"Task #{task_id} marked as incomplete!"

    return (True, new_status, message)


def update_task(task_id: int, title: str | None = None, description: str | None = None) -> tuple[bool, str]:
    """Update an existing task's title and/or description.

    Args:
        task_id: ID of task to update
        title: New title (1-200 chars), or None to keep existing
        description: New description (max 1000 chars), or None to keep existing

    Returns:
        Tuple of (success, message):
        - success (bool): True if updated, False if validation failed or task not found
        - message (str): Confirmation or error message
    """
    task = get_task_by_id(task_id)
    if task is None:
        return (False, f"Task ID {task_id} not found. Please try again.")

    if title is None and description is None:
        return (False, "No changes specified.")

    if title is not None:
        is_valid, error_msg = validate_title(title)
        if not is_valid:
            return (False, error_msg)
        task["title"] = title

    if description is not None:
        is_valid, error_msg = validate_description(description)
        if not is_valid:
            return (False, error_msg)
        task["description"] = description

    return (True, f"Task #{task_id} updated successfully!")


def delete_task(task_id: int) -> tuple[bool, str]:
    """Delete a task by ID.

    Args:
        task_id: ID of task to delete

    Returns:
        Tuple of (success, message):
        - success (bool): True if deleted, False if task not found
        - message (str): Confirmation or error message
    """
    task = get_task_by_id(task_id)
    if task is None:
        return (False, f"Task ID {task_id} not found. Please try again.")

    tasks.remove(task)
    return (True, f"Task #{task_id} deleted successfully!")
