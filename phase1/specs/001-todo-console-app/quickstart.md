# Quickstart Guide: Todo Console App - Phase 1

**Feature**: Todo Console App - Phase 1
**Date**: 2026-01-02
**Purpose**: Developer setup and testing instructions for implementing the todo list manager

## Prerequisites

- **Python 3.13+** installed and available in PATH
- **UV package manager** installed
- **Git** (for version control)
- **UTF-8 capable terminal** (Windows Terminal, macOS Terminal, or Linux terminal)

### Verify Prerequisites

```bash
# Check Python version (should be 3.13 or higher)
python --version

# Check UV installation
uv --version

# Check Git installation
git --version
```

---

## Project Setup

### 1. Clone Repository and Checkout Feature Branch

```bash
# Navigate to project directory
cd D:\Q4-Gemini_CLI\Hackathon_2\phase1

# Verify you're on the feature branch
git branch --show-current
# Should show: 001-todo-console-app
```

### 2. Create Source Directory

```bash
# Create src directory if it doesn't exist
mkdir -p src

# Verify structure
ls -la src/
```

---

## Implementation Steps

### Step 1: Create `todo.py` (Data & Business Logic)

**File**: `src/todo.py` (~250 lines)

**Contents**:
1. Module-level storage (`tasks`, `next_id`)
2. Validation functions (`validate_title`, `validate_description`)
3. Data access helpers (`get_task_by_id`, `get_all_tasks`)
4. CRUD operations (`add_task`, `update_task`, `delete_task`, `toggle_complete`)

**Imports needed**:
```python
from datetime import datetime
from typing import Any
```

**Entry point**: No entry point (imported by main.py)

**Testing**: Can be tested independently via Python REPL:
```python
python
>>> import src.todo as todo
>>> success, task_id, msg = todo.add_task("Test task", "Description")
>>> print(task_id, msg)
1 Task #1 created successfully!
>>> tasks = todo.get_all_tasks()
>>> print(tasks)
[{'id': 1, 'title': 'Test task', ...}]
```

---

### Step 2: Create `main.py` (UI Layer)

**File**: `src/main.py` (~200 lines)

**Contents**:
1. Display functions (`display_menu`, `display_tasks`)
2. Input helpers (`get_menu_choice`, `get_task_id`, `get_title_input`, `get_description_input`, `get_yes_no_confirmation`)
3. Menu handlers (`handle_add_task`, `handle_view_tasks`, `handle_update_task`, `handle_delete_task`, `handle_mark_complete`)
4. Main loop (`main_loop`)

**Imports needed**:
```python
from typing import Any, NoReturn
import sys
sys.path.insert(0, '.')  # Allow importing from current directory
import src.todo as todo
```

**Entry point**: `if __name__ == "__main__": main_loop()`

---

## Running the Application

### Method 1: UV Run (Recommended)

```bash
# From project root
uv run python src/main.py
```

### Method 2: Direct Python

```bash
# From project root
python src/main.py
```

### Expected Output

```
=== Todo List Manager ===
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete
6. Exit

Enter choice (1-6):
```

---

## Manual Testing Checklist

### Test Suite 1: Basic CRUD Operations

| Test | Steps | Expected Result |
|------|-------|----------------|
| **T1.1: Add task** | Select option 1 → Enter title "Review PR" → Enter description "Check team PRs" | Display "Task #1 created successfully!" |
| **T1.2: View empty list** | Delete all tasks → Select option 2 | Display "No tasks found" |
| **T1.3: View task list** | Add 3 tasks → Select option 2 | Display 3 tasks with IDs, titles, ☐ status, timestamps |
| **T1.4: Update task** | Select option 3 → Enter ID 1 → New title "Review code" → New description "" | Display "Task #1 updated successfully!" |
| **T1.5: Delete task** | Select option 4 → Enter ID 2 → Confirm "Y" | Display "Task #2 deleted successfully!" |
| **T1.6: Mark complete** | Select option 5 → Enter ID 1 | Display "Task #1 marked as complete!" → View shows ✓ |
| **T1.7: Mark incomplete** | Select option 5 → Enter ID 1 (already complete) | Display "Task #1 marked as incomplete!" → View shows ☐ |

---

### Test Suite 2: Input Validation

| Test | Steps | Expected Result |
|------|-------|----------------|
| **T2.1: Empty title** | Add task → Press Enter without typing title | Display "Title cannot be empty. Please enter a title." → Re-prompt |
| **T2.2: Title too long** | Add task → Enter 201-character title | Display "Title too long (max 200 characters). Please shorten." → Re-prompt |
| **T2.3: Title exactly 200 chars** | Add task → Enter 200-character title | Task created successfully |
| **T2.4: Description too long** | Add task → Enter valid title → Enter 1001-character description | Display "Description too long (max 1000 characters). Please shorten." → Re-prompt |
| **T2.5: Description exactly 1000 chars** | Add task → Enter valid title → Enter 1000-character description | Task created successfully |
| **T2.6: Invalid menu choice (out of range)** | Enter "7" at menu | Display "Invalid choice. Please enter a number between 1-6." → Re-prompt |
| **T2.7: Invalid menu choice (non-numeric)** | Enter "abc" at menu | Display "Invalid choice. Please enter a number between 1-6." → Re-prompt |
| **T2.8: Task ID not found** | Delete task → Enter ID 999 | Display "Task ID 999 not found. Please try again." → Return to menu |

---

### Test Suite 3: Edge Cases

| Test | Steps | Expected Result |
|------|-------|----------------|
| **T3.1: Unicode title** | Add task → Title "🎯 Complete project" | Task created, displays correctly in list |
| **T3.2: Unicode description** | Add task → Description with Chinese/emoji characters | Task created, displays correctly |
| **T3.3: Special characters** | Add task → Title with quotes "Review \"API\" code" | Task created, no corruption |
| **T3.4: Long task title display** | Add task → 200-char title → View list | Title displays without crashing (may truncate with ...) |
| **T3.5: ID reuse prevention** | Add 3 tasks (IDs 1,2,3) → Delete task 2 → Add new task | New task gets ID 4 (not 2) |
| **T3.6: Delete confirmation cancel** | Delete task → Enter valid ID → Confirm "N" | Display "Deletion cancelled" → Task still exists |
| **T3.7: Whitespace title** | Add task → Title "   " (spaces only) | Display "Title cannot be empty. Please enter a title." |
| **T3.8: Update partial** | Update task → New title → Leave description blank | Only title updated, description preserved |

---

### Test Suite 4: Menu Navigation

| Test | Steps | Expected Result |
|------|-------|----------------|
| **T4.1: Menu loop** | Complete any operation → Check menu redisplays | Menu displayed again after operation |
| **T4.2: Exit cleanly** | Select option 6 | Application exits without errors or hanging |
| **T4.3: Exit via Ctrl+C** | Press Ctrl+C at any prompt | Application exits (KeyboardInterrupt) |
| **T4.4: Multiple operations** | Add → View → Update → View → Delete → View | All operations work in sequence |

---

### Test Suite 5: Success Criteria Validation

| Criterion | Test | Validation |
|-----------|------|------------|
| SC-001: All CRUD work | T1.1-T1.7 | All 5 operations functional |
| SC-002: Graceful errors | T2.1-T2.8 | No crashes, specific error messages |
| SC-003: Workflow <60s | Timed test: Add → View → Mark → View → Delete | Complete in <60 seconds |
| SC-004: Unique IDs | T3.5 | IDs never reused after deletion |
| SC-005: Intuitive navigation | T4.1, T4.4 | Returns to menu after each operation |
| SC-006: Clear feedback | T1.1-T1.7 | Confirmation/error message for every action |
| SC-007: Clean exit | T4.2 | Exits without errors |
| SC-008: <500 lines | `wc -l src/*.py` | Total ≤ 500 lines |
| SC-009: Self-documenting UI | Manual review of menu text | Options clear without external docs |
| SC-010: Edge cases | T3.1-T3.8 | All edge cases handled |

---

## Code Quality Checks

### PEP 8 Compliance

```bash
# Install flake8 (if available)
pip install flake8

# Run PEP 8 check
flake8 src/main.py src/todo.py --max-line-length=88
```

**Expected**: No errors or warnings

### Type Hints Check

```bash
# Install mypy (if available)
pip install mypy

# Run type check
mypy src/main.py src/todo.py
```

**Expected**: No type errors

### Line Count Check

```bash
# Count lines in both files
wc -l src/*.py

# Should show:
# ~200 main.py
# ~250 todo.py
# ~450 total (within 500 limit)
```

---

## Troubleshooting

### Issue: UTF-8 Symbols Don't Display (Windows cmd.exe)

**Symptom**: Menu shows `?` or garbage characters instead of ✓/☐

**Solution**:
1. Use Windows Terminal instead of cmd.exe, OR
2. Enable UTF-8 in cmd.exe:
   ```cmd
   chcp 65001
   ```
3. Fallback: Modify `display_tasks()` to use ASCII `[X]` and `[ ]` instead

---

### Issue: ModuleNotFoundError: No module named 'src'

**Symptom**: `python src/main.py` fails with import error

**Solution**:
Add path fix to top of `main.py`:
```python
import sys
sys.path.insert(0, '.')
```

---

### Issue: Tasks Lost Between Runs

**Symptom**: Data disappears after exiting application

**Expected Behavior**: This is correct! Phase 1 is in-memory only (no persistence). Data intentionally lost on exit per Constitution Principle II.

---

### Issue: KeyboardInterrupt Not Caught

**Symptom**: Ctrl+C shows stack trace

**Expected Behavior**: This is acceptable for Phase 1. Stack trace exit is valid way to terminate console apps.

**Optional Enhancement** (if time permits):
```python
try:
    main_loop()
except KeyboardInterrupt:
    print("\nExiting application. Goodbye!")
    sys.exit(0)
```

---

## Performance Testing

### Expected Performance

| Operation | Expected Time | Acceptable Range |
|-----------|--------------|------------------|
| Add task | <50ms | <100ms |
| View all tasks (10 tasks) | <50ms | <100ms |
| Update task | <50ms | <100ms |
| Delete task | <50ms | <100ms |
| Toggle complete | <50ms | <100ms |

**Note**: All operations are O(n) or better with n=5-50 tasks, so performance should be instant.

---

## Known Limitations (By Design)

1. **No Persistence**: Data lost on exit (Phase 1 constraint)
2. **No Undo**: Operations are irreversible (Phase 1 out of scope)
3. **Linear Search**: O(n) ID lookup acceptable for small task lists
4. **No Multi-User**: Single user only (Phase 1 constraint)
5. **Manual Testing Only**: No automated tests (Phase 1 constraint)

---

## Next Steps After Implementation

1. ✅ **Complete Implementation**: Ensure both files functional
2. ✅ **Run Test Suite**: Execute all tests in checklists above
3. ✅ **Verify Success Criteria**: Check all SC-001 through SC-010 pass
4. ✅ **Code Quality**: PEP 8, type hints, docstrings complete
5. ✅ **Line Count**: Verify <500 lines total
6. 📋 **Commit Changes**: `git add src/` → `git commit -m "Implement todo console app"`
7. 🚀 **Next Phase**: Run `/sp.tasks` to generate detailed implementation tasks

---

## Reference: Complete Test Session Example

```bash
# 1. Start application
uv run python src/main.py

# 2. Add first task
Enter choice (1-6): 1
Enter task title: Review pull requests
Enter task description (press Enter to skip): Check PRs from team members
Task #1 created successfully!

# 3. View tasks
Enter choice (1-6): 2
ID | Status | Title                  | Created
---+--------+------------------------+---------------------
1  | ☐      | Review pull requests   | 2026-01-02 14:35:22
    Description: Check PRs from team members

# 4. Mark complete
Enter choice (1-6): 5
Enter task ID: 1
Task #1 marked as complete!

# 5. View updated list
Enter choice (1-6): 2
ID | Status | Title                  | Created
---+--------+------------------------+---------------------
1  | ✓      | Review pull requests   | 2026-01-02 14:35:22
    Description: Check PRs from team members

# 6. Exit
Enter choice (1-6): 6
Thank you for using Todo List Manager. Goodbye!
```

---

**Quickstart Status**: ✅ COMPLETE - Ready for implementation and testing
