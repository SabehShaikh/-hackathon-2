# Data Model: Todo Console App - Phase 1

**Feature**: Todo Console App - Phase 1
**Date**: 2026-01-02
**Purpose**: Define data structures, validation rules, and state transitions for in-memory task management

## Entities

### Task

Represents a single todo item with lifecycle management (create, update, complete, delete).

**Attributes**:

| Attribute | Type | Required | Constraints | Default | Description |
|-----------|------|----------|-------------|---------|-------------|
| `id` | `int` | Yes (auto) | Unique, positive, auto-increment, never reused | Next available ID | Unique task identifier |
| `title` | `str` | Yes | 1-200 characters (after strip), non-empty | N/A | Task title/summary |
| `description` | `str` | No | Max 1000 characters | `""` (empty string) | Detailed task description |
| `completed` | `bool` | Yes (auto) | True or False | `False` | Completion status flag |
| `created_at` | `str` | Yes (auto) | ISO 8601 format "YYYY-MM-DD HH:MM:SS" | Current timestamp | Creation timestamp |

**Python Representation**:
```python
task: dict[str, Any] = {
    "id": 1,
    "title": "Review pull requests",
    "description": "Check PRs from team members",
    "completed": False,
    "created_at": "2026-01-02 14:35:22"
}
```

**Type Alias**:
```python
from typing import Any
TaskDict = dict[str, Any]
```

---

### Task List (Collection)

In-memory collection storing all tasks during program execution.

**Storage**:
- **Type**: `list[dict[str, Any]]`
- **Scope**: Module-level variable in `todo.py`
- **Name**: `tasks`
- **Initial Value**: `[]` (empty list)
- **Lifetime**: Program execution only (lost on exit)

**Invariants**:
1. All task IDs are unique within the list
2. Tasks ordered by insertion (implicitly by ID due to auto-increment)
3. No null/None tasks in list
4. List may be empty (valid state)

**Python Representation**:
```python
tasks: list[dict[str, Any]] = []
```

---

### ID Counter

Auto-incrementing counter for generating unique task IDs.

**Storage**:
- **Type**: `int`
- **Scope**: Module-level variable in `todo.py`
- **Name**: `next_id`
- **Initial Value**: `1`
- **Behavior**: Increments after each task creation, never decrements

**Invariants**:
1. Always positive (≥ 1)
2. Monotonically increasing (never decreases)
3. Never reused (even after task deletion)

**Python Representation**:
```python
next_id: int = 1
```

---

## Validation Rules

### Title Validation

**Function**: `validate_title(title: str) -> tuple[bool, str]`

**Rules**:
1. Must not be empty after `strip()` (remove leading/trailing whitespace)
2. Must be 1-200 characters (inclusive)
3. All Unicode characters accepted (no character restrictions)

**Error Messages**:
- Empty: `"Title cannot be empty. Please enter a title."`
- Too long: `"Title too long (max 200 characters). Please shorten."`

**Examples**:
```python
validate_title("")                    → (False, "Title cannot be empty. Please enter a title.")
validate_title("   ")                 → (False, "Title cannot be empty. Please enter a title.")
validate_title("Review PR")           → (True, "")
validate_title("A" * 200)             → (True, "")
validate_title("A" * 201)             → (False, "Title too long (max 200 characters). Please shorten.")
validate_title("🎯 Complete project") → (True, "")  # Unicode accepted
```

---

### Description Validation

**Function**: `validate_description(description: str) -> tuple[bool, str]`

**Rules**:
1. Empty allowed (optional field)
2. Must be max 1000 characters (inclusive)
3. All Unicode characters accepted (no character restrictions)

**Error Messages**:
- Too long: `"Description too long (max 1000 characters). Please shorten."`

**Examples**:
```python
validate_description("")           → (True, "")
validate_description("Details")    → (True, "")
validate_description("A" * 1000)   → (True, "")
validate_description("A" * 1001)   → (False, "Description too long (max 1000 characters). Please shorten.")
```

---

### ID Validation

**Function**: `get_task_by_id(task_id: int) -> dict[str, Any] | None`

**Rules**:
1. Task ID must exist in the tasks list
2. Returns task dictionary if found, None if not found

**Usage** (implicit validation):
```python
task = get_task_by_id(5)
if task is None:
    return (False, "Task ID 5 not found. Please try again.")
```

---

## State Transitions

### Task Lifecycle

```
[Start] → Created (completed=False)
           ↓
      Incomplete ↔ Complete (toggle via toggle_complete())
           ↓
       Deleted (removed from list)
```

**Allowed Transitions**:

| From State | Action | To State | Method |
|------------|--------|----------|--------|
| N/A | Create task | Incomplete | `add_task()` |
| Incomplete | Mark complete | Complete | `toggle_complete()` |
| Complete | Mark incomplete | Incomplete | `toggle_complete()` |
| Incomplete | Update task | Incomplete | `update_task()` |
| Complete | Update task | Complete | `update_task()` |
| Incomplete | Delete task | Deleted | `delete_task()` |
| Complete | Delete task | Deleted | `delete_task()` |

**State Invariants**:
- New tasks always start as Incomplete (`completed=False`)
- Toggle always flips current state (True ↔ False)
- Update preserves completion status (doesn't change `completed` field)
- Delete is irreversible (task removed from memory)

---

## Data Access Patterns

### Create (Add Task)

```python
# Input: title (required), description (optional)
# Output: (success, task_id, message)
success, task_id, message = add_task("Review code", "Check for bugs")
if success:
    # Task created with auto-generated ID and timestamp
    # tasks list contains new task
    # next_id incremented
```

**Complexity**: O(1) - append to list

---

### Read (Get All Tasks)

```python
# Input: None
# Output: List of all tasks (may be empty)
all_tasks = get_all_tasks()
# Returns tasks in insertion order (effectively ID order)
```

**Complexity**: O(1) - return reference to list

---

### Read (Get Task by ID)

```python
# Input: task_id
# Output: Task dict or None
task = get_task_by_id(5)
if task is not None:
    # Task found, can access task['title'], task['completed'], etc.
```

**Complexity**: O(n) - linear search through list (acceptable for 5-50 tasks)

---

### Update (Modify Task)

```python
# Input: task_id, new title (optional), new description (optional)
# Output: (success, message)
success, message = update_task(3, title="New title", description=None)
if success:
    # Task updated in-place
    # Unchanged fields preserved
    # completed and created_at unchanged
```

**Complexity**: O(n) - find by ID + update

---

### Delete (Remove Task)

```python
# Input: task_id
# Output: (success, message)
success, message = delete_task(4)
if success:
    # Task removed from tasks list
    # ID 4 never reused (next_id not decremented)
```

**Complexity**: O(n) - find by ID + remove from list

---

### Toggle Complete (Change Status)

```python
# Input: task_id
# Output: (success, new_status, message)
success, new_status, message = toggle_complete(2)
if success:
    # Task completed field toggled (True ↔ False)
    # new_status contains new value
```

**Complexity**: O(n) - find by ID + toggle boolean

---

## Data Integrity

### Constraints

1. **ID Uniqueness**: Enforced by auto-increment counter (no manual ID assignment)
2. **ID Immutability**: Tasks never change ID after creation
3. **Required Fields**: `id`, `title`, `completed`, `created_at` always present
4. **Type Safety**: Python type hints enforce expected types
5. **String Lengths**: Validated before task creation/update

### Error Conditions

| Condition | Check | Response |
|-----------|-------|----------|
| Empty title | `validate_title()` | Return error tuple, don't create/update task |
| Title too long | `validate_title()` | Return error tuple, don't create/update task |
| Description too long | `validate_description()` | Return error tuple, don't create/update task |
| Task ID not found | `get_task_by_id()` returns None | Return error tuple with "Task ID X not found" |

---

## Storage Implementation

### Module Structure (todo.py)

```python
"""
Task data storage and business logic for Todo Console App.

This module manages in-memory task storage and provides CRUD operations
with validation. All data is lost when the program exits.
"""

from datetime import datetime
from typing import Any

# ============================================================================
# Module-Level Storage
# ============================================================================

tasks: list[dict[str, Any]] = []
"""List of all tasks. Each task is a dictionary with keys: id, title, description, completed, created_at."""

next_id: int = 1
"""Auto-incrementing counter for task IDs. Starts at 1, never decrements."""

# ============================================================================
# Validation Functions
# ============================================================================

def validate_title(title: str) -> tuple[bool, str]:
    """Validate task title (1-200 chars, required)."""
    # Implementation...

def validate_description(description: str) -> tuple[bool, str]:
    """Validate task description (max 1000 chars, optional)."""
    # Implementation...

# ============================================================================
# Data Access Functions
# ============================================================================

def get_task_by_id(task_id: int) -> dict[str, Any] | None:
    """Find task by ID, return None if not found."""
    # Implementation...

def get_all_tasks() -> list[dict[str, Any]]:
    """Return all tasks in order."""
    # Implementation...

# ============================================================================
# CRUD Operations
# ============================================================================

def add_task(title: str, description: str = "") -> tuple[bool, int | None, str]:
    """Create new task with validation."""
    # Implementation...

def update_task(task_id: int, title: str | None = None, description: str | None = None) -> tuple[bool, str]:
    """Update existing task with validation."""
    # Implementation...

def delete_task(task_id: int) -> tuple[bool, str]:
    """Delete task by ID."""
    # Implementation...

def toggle_complete(task_id: int) -> tuple[bool, bool | None, str]:
    """Toggle task completion status."""
    # Implementation...
```

---

## Example Data Flows

### Example 1: Create 3 Tasks

```python
# Initial state
tasks = []
next_id = 1

# Add first task
add_task("Review PR", "Check team PRs")
# tasks = [{"id": 1, "title": "Review PR", "description": "Check team PRs", "completed": False, "created_at": "2026-01-02 14:35:22"}]
# next_id = 2

# Add second task
add_task("Write tests", "")
# tasks = [...task1..., {"id": 2, "title": "Write tests", "description": "", "completed": False, "created_at": "2026-01-02 14:36:15"}]
# next_id = 3

# Add third task
add_task("Deploy app", "Deploy to production")
# tasks = [...task1..., ...task2..., {"id": 3, "title": "Deploy app", "description": "Deploy to production", "completed": False, "created_at": "2026-01-02 14:37:08"}]
# next_id = 4
```

---

### Example 2: Update and Delete with ID Gaps

```python
# Starting state: tasks with IDs 1, 2, 3 (from Example 1)
# next_id = 4

# Delete task 2
delete_task(2)
# tasks = [task1, task3]  # ID 2 removed
# next_id = 4  # Unchanged (never decrements)

# Add new task
add_task("Fix bugs", "")
# tasks = [task1, task3, {"id": 4, ...}]  # New task gets ID 4, not 2
# next_id = 5

# Result: IDs are 1, 3, 4 (gap at 2)
```

---

### Example 3: Toggle Completion

```python
# Starting state: task with id=1, completed=False

# Mark complete
toggle_complete(1)
# task['completed'] = True

# Mark incomplete
toggle_complete(1)
# task['completed'] = False
```

---

**Data Model Status**: ✅ COMPLETE - All entities, validations, and transitions defined
