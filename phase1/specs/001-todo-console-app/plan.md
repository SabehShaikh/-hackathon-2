# Implementation Plan: Todo Console App - Phase 1

**Branch**: `001-todo-console-app` | **Date**: 2026-01-02 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-todo-console-app/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a console-based todo list manager enabling developers to manage daily tasks through a simple menu interface. The application provides 5 core CRUD operations (Add, View, Update, Delete, Mark Complete/Incomplete) with robust input validation and clear user feedback. Implementation uses Python 3.13+ standard library only, storing tasks in-memory (no persistence). Architecture follows clean 3-layer separation: Data (in-memory storage), Business Logic (CRUD operations with validation), and UI (console menu and display).

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python standard library only (`datetime`, `typing` for type hints)
**Storage**: In-memory list of dictionaries (no file I/O, no database)
**Testing**: Manual testing only for Phase 1 (automated testing out of scope)
**Target Platform**: Cross-platform console/terminal (Windows, macOS, Linux) with UTF-8 support
**Project Type**: Single console application with 2 Python files
**Performance Goals**: Interactive response (<100ms for all operations), supports 5-50 tasks per session
**Constraints**:
- Maximum 500 lines of code total
- No external dependencies beyond Python stdlib
- No file I/O or persistence
- PEP 8 compliance mandatory
- Type hints and docstrings required for all functions
**Scale/Scope**: Single-user console application, ~450 lines across 2 files, 5 CRUD features

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Simplicity First ✅ PASS
- **Requirement**: Python stdlib only, no frameworks, single-file-capable application
- **Plan Status**: Compliant - Using only `datetime` and `typing` from stdlib, 2-file structure (main.py + todo.py), no external dependencies
- **Justification**: N/A - No violations

### Principle II: In-Memory Only ✅ PASS
- **Requirement**: No file I/O, no databases, data lost on exit
- **Plan Status**: Compliant - In-memory list storage, no persistence layer planned
- **Justification**: N/A - No violations

### Principle III: User-Friendly Console Interface ✅ PASS
- **Requirement**: Clear feedback, numbered menus, helpful error messages
- **Plan Status**: Compliant - Plan includes specific error messages, numbered menu (1-6), confirmation messages for all operations
- **Justification**: N/A - No violations

### Principle IV: Clean Architecture ✅ PASS
- **Requirement**: Separation of concerns at function level (Data, Business Logic, UI)
- **Plan Status**: Compliant - 3-layer design: `todo.py` (data + business logic), `main.py` (UI layer), clear boundaries
- **Justification**: N/A - No violations

### Principle V: Robust Input Handling ✅ PASS
- **Requirement**: Never crash, validate all input, specific error messages
- **Plan Status**: Compliant - Plan includes try/except blocks, validation functions, specific error messages per spec (FR-013)
- **Justification**: N/A - No violations

### Principle VI: Type Safety and Documentation ✅ PASS
- **Requirement**: Type hints on all functions, Google-style docstrings, meaningful names
- **Plan Status**: Compliant - Plan mandates type hints, docstrings specified in function signatures below
- **Justification**: N/A - No violations

### Code Quality Standards ✅ PASS
- **PEP 8**: Plan follows PEP 8 (88-char lines, snake_case, imports grouped)
- **Line Length**: 88 characters (Black default)
- **Naming**: snake_case functions, UPPER_SNAKE_CASE constants
- **Documentation**: Google-style docstrings required

**GATE STATUS**: ✅ ALL CHECKS PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-console-app/
├── spec.md              # Feature specification (created by /sp.specify)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (below)
├── data-model.md        # Phase 1 output (below)
├── quickstart.md        # Phase 1 output (below)
├── checklists/
│   └── requirements.md  # Spec quality checklist (created by /sp.specify)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── main.py              # UI layer: menu loop, display functions, input handling (~200 lines)
└── todo.py              # Data + Business logic: storage, CRUD operations, validation (~250 lines)

# Testing (manual for Phase 1)
# - No automated test files
# - Manual test checklist in specs/001-todo-console-app/checklists/
```

**Structure Decision**: Single project structure chosen. Console application requires only 2 Python files with clear separation: `todo.py` handles data and business logic (task storage, CRUD operations, validation), while `main.py` handles UI concerns (menu display, user input, output formatting). This aligns with Constitution Principle IV (Clean Architecture) while maintaining Constitution Principle I (Simplicity First) by avoiding unnecessary file/directory proliferation.

## Complexity Tracking

**No violations of constitution principles.** All requirements satisfied within constitutional constraints.

---

## Phase 0: Research & Technology Selection

### Research Questions

Based on Technical Context, the following items require research or decision-making:

1. **Input Validation Strategy**: How to validate string length (1-200 chars for title, max 1000 for description) and handle edge cases (unicode, special characters)?

2. **Timestamp Format**: How to generate ISO 8601 timestamps (YYYY-MM-DD HH:MM:SS) using `datetime` module?

3. **Console Symbol Compatibility**: How to ensure UTF-8 symbols (✓, ☐) display correctly across Windows/macOS/Linux terminals? Fallback strategy?

4. **ID Generation**: How to implement auto-incrementing IDs that never reuse (even after deletion) using only in-memory state?

5. **Error Handling Pattern**: Best practice for returning errors from business logic to UI layer (exceptions vs. return tuples)?

### Research Outcomes

See [research.md](research.md) for detailed findings. Key decisions:

1. **Input Validation**: Use `len()` built-in for character count, `str.strip()` for empty check, accept all unicode (Python 3.13 handles unicode natively)

2. **Timestamp Format**: `datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")` produces ISO 8601 format

3. **Console Symbols**: Use UTF-8 symbols (✓ = `\u2713`, ☐ = `\u2610`) with try/except fallback to ASCII ([X], [ ]) if encoding error occurs

4. **ID Generation**: Module-level counter variable `next_id` incremented after each task creation, never decremented (survives deletions)

5. **Error Handling**: Return tuples `(success: bool, data: Any, message: str)` from business logic to avoid exception handling complexity in UI layer

---

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](data-model.md) for complete entity definitions. Summary:

**Task Entity**:
```python
{
    "id": int,              # Unique identifier (auto-increment, starts at 1)
    "title": str,           # Task title (1-200 chars, required)
    "description": str,     # Task description (max 1000 chars, optional, "" if empty)
    "completed": bool,      # Completion status (default False)
    "created_at": str       # ISO 8601 timestamp "YYYY-MM-DD HH:MM:SS"
}
```

**Storage**:
- Module-level list: `tasks: list[dict[str, Any]] = []`
- Module-level counter: `next_id: int = 1`

**State Transitions**:
- Created → Incomplete (completed=False)
- Incomplete ↔ Complete (toggle via Mark Complete/Incomplete)
- Any State → Deleted (removed from list)

### Function Contracts

#### todo.py - Data & Business Logic Layer

```python
from datetime import datetime
from typing import Any

# Module-level storage
tasks: list[dict[str, Any]] = []
next_id: int = 1

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

    Validation:
        - Title must not be empty (after strip)
        - Title must be 1-200 characters
        - Description must be max 1000 characters
    """

def get_all_tasks() -> list[dict[str, Any]]:
    """Retrieve all tasks ordered by ID.

    Returns:
        List of task dictionaries (may be empty)
    """

def get_task_by_id(task_id: int) -> dict[str, Any] | None:
    """Find a task by its ID.

    Args:
        task_id: Task ID to search for

    Returns:
        Task dictionary if found, None otherwise
    """

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

    Validation:
        - Task ID must exist
        - If title provided, must not be empty and must be 1-200 characters
        - If description provided, must be max 1000 characters
    """

def delete_task(task_id: int) -> tuple[bool, str]:
    """Delete a task by ID.

    Args:
        task_id: ID of task to delete

    Returns:
        Tuple of (success, message):
        - success (bool): True if deleted, False if task not found
        - message (str): Confirmation or error message
    """

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

def validate_title(title: str) -> tuple[bool, str]:
    """Validate a task title.

    Args:
        title: Title string to validate

    Returns:
        Tuple of (valid, error_message):
        - valid (bool): True if valid, False otherwise
        - error_message (str): Empty if valid, error description if invalid
    """

def validate_description(description: str) -> tuple[bool, str]:
    """Validate a task description.

    Args:
        description: Description string to validate

    Returns:
        Tuple of (valid, error_message):
        - valid (bool): True if valid, False otherwise
        - error_message (str): Empty if valid, error description if invalid
    """
```

#### main.py - UI Layer

```python
from typing import NoReturn
import todo

def display_menu() -> None:
    """Display the main menu with 6 numbered options."""

def display_tasks(tasks: list[dict[str, Any]]) -> None:
    """Display all tasks in a formatted list.

    Args:
        tasks: List of task dictionaries from get_all_tasks()

    Format:
        ID | Status | Title | Created
        - Status: ✓ for complete, ☐ for incomplete (fallback to [X] and [ ])
        - Description indented below title if present
        - "No tasks found" if list is empty
    """

def get_menu_choice() -> int:
    """Prompt user for menu choice (1-6) with validation.

    Returns:
        Valid menu choice (1-6)

    Handles:
        - Non-numeric input
        - Out-of-range numbers
        - Empty input
    """

def get_task_id() -> int:
    """Prompt user for task ID with validation.

    Returns:
        Task ID (positive integer)

    Handles:
        - Non-numeric input
        - Negative numbers
        - Empty input
    """

def get_title_input(prompt: str = "Enter task title: ") -> str:
    """Prompt for task title with validation.

    Args:
        prompt: Custom prompt message

    Returns:
        Valid title (1-200 characters)

    Loops until valid input received.
    """

def get_description_input() -> str:
    """Prompt for task description (optional).

    Returns:
        Description string (may be empty, max 1000 chars)

    Loops until valid input received.
    """

def get_yes_no_confirmation(prompt: str) -> bool:
    """Prompt for Y/N confirmation.

    Args:
        prompt: Question to ask user

    Returns:
        True if 'Y' or 'y', False if 'N' or 'n'

    Loops until valid input (Y/N) received.
    """

def handle_add_task() -> None:
    """Handle Add Task menu option (Option 1)."""

def handle_view_tasks() -> None:
    """Handle View All Tasks menu option (Option 2)."""

def handle_update_task() -> None:
    """Handle Update Task menu option (Option 3)."""

def handle_delete_task() -> None:
    """Handle Delete Task menu option (Option 4)."""

def handle_mark_complete() -> None:
    """Handle Mark Complete/Incomplete menu option (Option 5)."""

def main_loop() -> NoReturn:
    """Main application loop - displays menu and handles user choices.

    Runs until user selects Exit (Option 6).
    """

if __name__ == "__main__":
    main_loop()
```

### API Contracts

N/A - This is a console application with no external API. Function contracts above serve as internal API.

### Quickstart Guide

See [quickstart.md](quickstart.md) for developer setup and testing instructions.

---

## Implementation Order

### Phase 2: Task Generation (via `/sp.tasks`)

This plan document stops here. The next step is to run `/sp.tasks` to generate `tasks.md` with specific implementation tasks derived from this plan.

**Recommended task order** (for `/sp.tasks` to consider):

1. **Foundation** (P1):
   - Create `src/todo.py` with module-level storage variables
   - Implement validation functions (`validate_title`, `validate_description`)

2. **Core CRUD** (P1):
   - Implement `add_task()` function with ID generation and timestamp
   - Implement `get_all_tasks()` function
   - Implement `get_task_by_id()` helper

3. **UI Foundation** (P1):
   - Create `src/main.py` with menu display
   - Implement input helper functions (get_menu_choice, get_task_id, etc.)
   - Implement `display_tasks()` with UTF-8 symbol handling

4. **Menu Handlers** (P1):
   - Implement `handle_add_task()` wiring UI to business logic
   - Implement `handle_view_tasks()`
   - Implement main_loop with menu dispatch

5. **Additional CRUD** (P2):
   - Implement `toggle_complete()` function
   - Implement `handle_mark_complete()` UI handler

6. **Update & Delete** (P3-P4):
   - Implement `update_task()` function
   - Implement `delete_task()` function
   - Implement `handle_update_task()` and `handle_delete_task()` UI handlers

7. **Polish** (Final):
   - Add all docstrings
   - Add all type hints
   - PEP 8 compliance check
   - Manual testing against spec acceptance scenarios

---

## Post-Design Constitution Re-Check

*Required after Phase 1 design completion.*

### Principle I: Simplicity First ✅ PASS
- **Design Status**: 2 files (main.py ~200 lines, todo.py ~250 lines), only stdlib imports, no frameworks
- **Changes from initial check**: None - design maintains simplicity

### Principle II: In-Memory Only ✅ PASS
- **Design Status**: Module-level list storage, no file operations in any function
- **Changes from initial check**: None - no persistence added

### Principle III: User-Friendly Console Interface ✅ PASS
- **Design Status**: Specific error messages in validation functions, helper functions for all input, numbered menu
- **Changes from initial check**: None - UI design follows principle

### Principle IV: Clean Architecture ✅ PASS
- **Design Status**: Clear separation - todo.py (data + logic), main.py (UI), no mixing of concerns
- **Changes from initial check**: None - 3-layer separation maintained

### Principle V: Robust Input Handling ✅ PASS
- **Design Status**: Validation functions in business logic, input helpers in UI, tuple returns for errors
- **Changes from initial check**: None - error handling strategy compliant

### Principle VI: Type Safety and Documentation ✅ PASS
- **Design Status**: All function signatures include type hints, docstrings with Args/Returns sections
- **Changes from initial check**: None - documentation complete in contracts

**FINAL GATE STATUS**: ✅ ALL CHECKS PASS - Design approved, ready for `/sp.tasks`

---

## Design Decisions & Rationale

### 1. Return Tuples vs. Exceptions

**Decision**: Business logic functions return `(success: bool, data: Any, message: str)` tuples instead of raising exceptions.

**Rationale**:
- Simplifies UI layer (no try/except needed for business logic calls)
- Makes success/failure explicit in function signature
- Allows returning both data and user-friendly message
- Aligns with Constitution Principle I (Simplicity First)

**Alternatives Considered**:
- Raise ValueError for validation errors → Rejected: Adds complexity to UI layer
- Return None for failures → Rejected: Loses error message information

### 2. Single vs. Separate Validation Functions

**Decision**: Separate `validate_title()` and `validate_description()` functions instead of inline validation.

**Rationale**:
- Reusable across `add_task()` and `update_task()`
- Testable in isolation
- Single responsibility (validation only)
- Aligns with Constitution Principle IV (Clean Architecture)

**Alternatives Considered**:
- Inline validation in CRUD functions → Rejected: Code duplication
- Single validate_task() function → Rejected: Less flexible for partial updates

### 3. Module-Level vs. Class-Based Storage

**Decision**: Module-level variables (`tasks`, `next_id`) instead of a TodoManager class.

**Rationale**:
- Constitution Principle I: Simplicity First (no need for class structure)
- Single-user, single-session app (no concurrency concerns)
- Fewer lines of code (no __init__, no self references)
- Easier to reason about for learning developers (target user)

**Alternatives Considered**:
- TodoManager class → Rejected: Adds complexity without benefit
- Functional approach with explicit state passing → Rejected: More verbose

### 4. UTF-8 Symbols with ASCII Fallback

**Decision**: Attempt UTF-8 symbols (✓, ☐) first, fallback to ASCII ([X], [ ]) on encoding error.

**Rationale**:
- Better UX on modern terminals (majority of users)
- Graceful degradation for older/limited consoles
- Aligns with Constitution Principle III (User-Friendly)
- Spec requirement (FR-007 specifies symbols)

**Alternatives Considered**:
- ASCII only → Rejected: Less visually appealing
- UTF-8 only → Rejected: May crash on some Windows terminals

### 5. Two-File vs. Single-File Structure

**Decision**: Split into `main.py` (UI) and `todo.py` (data/logic) instead of single file.

**Rationale**:
- Constitution Principle IV mandates separation of concerns
- Easier to locate functions by layer
- Prepares for future refactoring (e.g., swapping UI for web interface)
- Still simple enough to understand (<500 lines total)

**Alternatives Considered**:
- Single file with sections → Rejected: Violates Clean Architecture principle
- Three files (data, logic, UI) → Rejected: Over-engineered for this scale

---

## Risk Analysis & Mitigation

### Risk 1: UTF-8 Encoding Issues on Windows

**Likelihood**: Medium | **Impact**: Low

**Description**: Some Windows terminals (cmd.exe without UTF-8 mode) may not display ✓/☐ symbols correctly, showing garbage characters or question marks.

**Mitigation**:
- Implement try/except around symbol printing
- Fallback to ASCII `[X]` and `[ ]` if encoding error detected
- Document terminal requirements in quickstart.md
- Test on Windows cmd.exe, PowerShell, and Windows Terminal

### Risk 2: Title/Description Length Validation Edge Cases

**Likelihood**: Low | **Impact**: Low

**Description**: Unicode characters may have unexpected length behavior (multi-byte chars, combining characters, emoji).

**Mitigation**:
- Python's `len()` counts characters, not bytes (handles unicode correctly)
- Accept all unicode input (no character restrictions)
- Document assumption: character count includes emoji/special chars as 1 char each
- Edge case testing: emoji titles, Chinese characters, accented characters

### Risk 3: ID Counter Overflow

**Likelihood**: Very Low | **Impact**: Very Low

**Description**: If user creates >2^63 tasks in a session, integer overflow could occur.

**Mitigation**:
- Python 3 integers have unlimited precision (no overflow)
- Practical limit: memory exhaustion before ID overflow
- Out of scope for Phase 1 (5-50 tasks expected per session)

### Risk 4: Input Prompt Infinite Loop

**Likelihood**: Low | **Impact**: Medium

**Description**: If input validation loops (e.g., `get_title_input()`) have no escape, user could be stuck.

**Mitigation**:
- All input loops re-prompt until valid input
- User can always exit via Ctrl+C (KeyboardInterrupt)
- Document Ctrl+C escape in user guidance
- Consider adding "back to menu" option in future phases

### Risk 5: Code Size Exceeds 500 Line Limit

**Likelihood**: Low | **Impact**: Medium

**Description**: With docstrings, type hints, and error handling, code may exceed 500 lines.

**Mitigation**:
- Current design: ~200 lines (main.py) + ~250 lines (todo.py) = 450 lines (50 line buffer)
- Minimize comments (docstrings count, inline comments avoided)
- Prefer concise variable names (within PEP 8 guidelines)
- If exceeded: remove optional features (delete confirmation, description display)

---

## Metrics & Success Criteria

Aligns with spec Success Criteria (SC-001 to SC-010):

| Spec Criterion | Implementation Metric | Validation Method |
|----------------|----------------------|-------------------|
| SC-001: All CRUD operations work | 5 functions implemented (add, view, update, delete, toggle) | Manual test each function |
| SC-002: Graceful error handling | No unhandled exceptions, specific error messages | Manual test invalid inputs |
| SC-003: Workflow <60 seconds | Add → view → mark → view → delete flow | Manual timing test |
| SC-004: Unique IDs | `next_id` counter never decrements | Manual test with deletions |
| SC-005: Intuitive navigation | Menu loop returns after each operation | Manual UX test |
| SC-006: Clear feedback | All operations return message string | Manual test all paths |
| SC-007: Clean exit | Option 6 exits without errors | Manual test exit |
| SC-008: <500 lines code | Line count check | `wc -l src/*.py` |
| SC-009: Self-documenting UI | Menu text explains all options | Manual review |
| SC-010: Edge cases handled | 9 edge cases from spec tested | Manual test checklist |

---

## Appendices

### Appendix A: Function Call Flow Examples

**Example 1: Add Task (Happy Path)**
```
User selects Option 1
→ main.handle_add_task()
  → main.get_title_input() → "Review PR"
  → main.get_description_input() → "Check team PRs"
  → todo.add_task("Review PR", "Check team PRs")
    → todo.validate_title("Review PR") → (True, "")
    → todo.validate_description("Check team PRs") → (True, "")
    → Create task dict with id=1, timestamp
    → Append to tasks list
    → Increment next_id to 2
    → Return (True, 1, "Task #1 created successfully!")
  → Display success message
  → Return to main menu
```

**Example 2: Update Task (Invalid ID)**
```
User selects Option 3
→ main.handle_update_task()
  → main.get_task_id() → 99
  → main.get_title_input() → "New title"
  → todo.update_task(99, "New title", None)
    → todo.get_task_by_id(99) → None
    → Return (False, "Task ID 99 not found. Please try again.")
  → Display error message
  → Return to main menu
```

### Appendix B: Error Message Reference

All error messages from spec FR-013:

| Scenario | Error Message |
|----------|---------------|
| Invalid menu choice (out of range) | "Invalid choice. Please enter a number between 1-6." |
| Invalid menu choice (non-numeric) | "Invalid choice. Please enter a number between 1-6." |
| Task ID not found | "Task ID {id} not found. Please try again." |
| Empty title | "Title cannot be empty. Please enter a title." |
| Title too long (>200 chars) | "Title too long (max 200 characters). Please shorten." |
| Description too long (>1000 chars) | "Description too long (max 1000 characters). Please shorten." |

Success messages:

| Operation | Success Message |
|-----------|----------------|
| Add task | "Task #{id} created successfully!" |
| Update task | "Task #{id} updated successfully!" |
| Delete task | "Task #{id} deleted successfully!" |
| Mark complete | "Task #{id} marked as complete!" |
| Mark incomplete | "Task #{id} marked as incomplete!" |
| Cancel delete | "Deletion cancelled" |

### Appendix C: Type Hint Reference

All custom types used:

```python
from typing import Any, NoReturn

TaskDict = dict[str, Any]  # {'id': int, 'title': str, 'description': str, 'completed': bool, 'created_at': str}
SuccessResult = tuple[bool, str]  # (success, message)
AddResult = tuple[bool, int | None, str]  # (success, task_id, message)
ToggleResult = tuple[bool, bool | None, str]  # (success, new_status, message)
ValidationResult = tuple[bool, str]  # (valid, error_message)
```

---

**Plan Status**: ✅ COMPLETE - Ready for `/sp.tasks` to generate implementation tasks
