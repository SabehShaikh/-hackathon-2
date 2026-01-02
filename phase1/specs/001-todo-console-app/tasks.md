# Tasks: Todo Console App - Phase 1

**Input**: Design documents from `/specs/001-todo-console-app/`
**Prerequisites**: plan.md, spec.md, constitution.md
**Branch**: `001-todo-console-app`

**Tests**: Manual testing only for Phase 1 (automated tests not requested in spec)

**Organization**: Tasks are grouped by user story (US1-US5) to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- All file paths are at repository root using single project structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project structure initialization

- [X] T001 Verify Python 3.13+ installed (`python --version`) and UV package manager available
- [X] T002 Create `src/` directory at repository root if not exists
- [X] T003 [P] Create empty `src/todo.py` file for business logic layer
- [X] T004 [P] Create empty `src/main.py` file for UI layer

**Checkpoint**: Project structure ready

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data structures and validation that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 [US1] Add module-level storage to `src/todo.py`: `tasks: list[dict[str, Any]] = []` and `next_id: int = 1`
- [X] T006 [US1] Add necessary imports to `src/todo.py`: `from datetime import datetime` and `from typing import Any`
- [X] T007 [P] [US1] Implement `validate_title(title: str) -> tuple[bool, str]` in `src/todo.py`
  - Check title.strip() is not empty → error: "Title cannot be empty. Please enter a title."
  - Check len(title) <= 200 → error: "Title too long (max 200 characters). Please shorten."
  - Return (True, "") if valid, (False, error_msg) otherwise
- [X] T008 [P] [US1] Implement `validate_description(description: str) -> tuple[bool, str]` in `src/todo.py`
  - Check len(description) <= 1000 → error: "Description too long (max 1000 characters). Please shorten."
  - Return (True, "") if valid, (False, error_msg) otherwise

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add tasks with title/description and view all tasks in a formatted list

**Independent Test**: Launch app → add 3 tasks with various titles/descriptions → view task list → confirm all appear with IDs, status symbols, timestamps → exit

**Acceptance**:
- FR-002: Add tasks with title (1-200 chars) and optional description (max 1000 chars)
- FR-003: Auto-generate unique sequential IDs starting from 1
- FR-004: Auto-timestamp with ISO 8601 format
- FR-005: Initialize completed=False
- FR-007: Display tasks with ID, title, status symbol (☐), timestamp
- FR-009: Display "No tasks found" for empty list

### Implementation for User Story 1

**Business Logic (src/todo.py)**:

- [X] T009 [US1] Implement `add_task(title: str, description: str = "") -> tuple[bool, int | None, str]` in `src/todo.py`
  - Validate title using validate_title() → return (False, None, error_msg) if invalid
  - Validate description using validate_description() → return (False, None, error_msg) if invalid
  - Create task dict: `{"id": next_id, "title": title, "description": description, "completed": False, "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}`
  - Append task to tasks list
  - Store current next_id in task_id variable
  - Increment global next_id
  - Return (True, task_id, f"Task #{task_id} created successfully!")

- [X] T010 [US1] Implement `get_all_tasks() -> list[dict[str, Any]]` in `src/todo.py`
  - Return copy of tasks list using `tasks.copy()`

- [X] T011 [US1] Implement `get_task_by_id(task_id: int) -> dict[str, Any] | None` in `src/todo.py`
  - Loop through tasks list
  - Return task dict if task["id"] == task_id
  - Return None if not found

**UI Layer (src/main.py)**:

- [X] T012 [P] [US1] Add imports to `src/main.py`: `import todo` and `from typing import Any`

- [X] T013 [P] [US1] Implement `display_menu() -> None` in `src/main.py`
  - Print "=== Todo List Manager ==="
  - Print "1. Add Task"
  - Print "2. View All Tasks"
  - Print "3. Update Task"
  - Print "4. Delete Task"
  - Print "5. Mark Complete/Incomplete"
  - Print "6. Exit"
  - Print empty line

- [X] T014 [P] [US1] Implement `display_tasks(tasks: list[dict[str, Any]]) -> None` in `src/main.py`
  - If tasks is empty: print "No tasks found" and return
  - For each task in tasks:
    - status_symbol = "✓" if task["completed"] else "☐" (use try/except for encoding, fallback to "[X]"/"[ ]")
    - Print f"[{task['id']}] {status_symbol} {task['title']} (Created: {task['created_at']})"
    - If task["description"]: print f"    {task['description']}" (indented)

- [X] T015 [US1] Implement `get_title_input(prompt: str = "Enter task title: ") -> str` in `src/main.py`
  - Loop until valid:
    - Get input using input(prompt)
    - Call todo.validate_title(title_input)
    - If valid: return title_input
    - If invalid: print error message and continue loop

- [X] T016 [US1] Implement `get_description_input() -> str` in `src/main.py`
  - Get input using input("Enter task description (optional, press Enter to skip): ")
  - If empty: return ""
  - Call todo.validate_description(desc_input)
  - If valid: return desc_input
  - If invalid: print error message, loop until valid or empty

- [X] T017 [US1] Implement `handle_add_task() -> None` in `src/main.py`
  - Call get_title_input() to get title
  - Call get_description_input() to get description
  - Call todo.add_task(title, description)
  - Print success/error message from returned tuple
  - Print empty line

- [X] T018 [US1] Implement `handle_view_tasks() -> None` in `src/main.py`
  - Call todo.get_all_tasks() to get tasks list
  - Call display_tasks(tasks)
  - Print empty line

**Checkpoint**: At this point, adding and viewing tasks should work (partial app with Options 1 and 2 functional)

---

## Phase 4: User Story 5 - Navigate Menu and Exit (Priority: P1) 🎯 MVP

**Goal**: Provide numbered menu navigation and clean exit

**Independent Test**: Launch app → verify menu shows 6 options → select each option 1-5 → test invalid inputs (7, abc, empty) → select option 6 to exit cleanly

**Acceptance**:
- FR-001: Console menu with 6 numbered options
- FR-013: Validate menu choice with error "Invalid choice. Please enter a number between 1-6."
- FR-014: Return to main menu after each operation
- FR-015: Clean exit on option 6

### Implementation for User Story 5

- [X] T019 [US5] Implement `get_menu_choice() -> int` in `src/main.py`
  - Print "Enter choice (1-6): "
  - Loop until valid:
    - Get input using input()
    - Try to convert to int
    - If ValueError or out of range [1,6]: print "Invalid choice. Please enter a number between 1-6." and continue
    - If valid: return int choice

- [X] T020 [US5] Implement `main_loop() -> None` in `src/main.py`
  - Print welcome message "=== Todo List Manager ===" with empty line
  - While True:
    - Call display_menu()
    - Call get_menu_choice() to get choice
    - If choice == 1: call handle_add_task()
    - Elif choice == 2: call handle_view_tasks()
    - Elif choice == 3: call handle_update_task() (stub for now, implemented in US3)
    - Elif choice == 4: call handle_delete_task() (stub for now, implemented in US4)
    - Elif choice == 5: call handle_mark_complete() (stub for now, implemented in US2)
    - Elif choice == 6: print "Goodbye! Note: All tasks will be lost (in-memory mode)." and break
  - Add try/except KeyboardInterrupt around while loop to handle Ctrl+C gracefully

- [X] T021 [US5] Add `if __name__ == "__main__": main_loop()` entry point at end of `src/main.py`

**Checkpoint**: At this point, full menu navigation works with Options 1, 2, and 6 functional (MVP core ready)

---

## Phase 5: User Story 2 - Mark Tasks Complete (Priority: P2)

**Goal**: Toggle task completion status to track progress

**Independent Test**: Add 2-3 tasks → mark one complete by ID → view list to see ✓ symbol → mark same task incomplete → verify ☐ symbol

**Acceptance**:
- FR-012: Toggle completion status by task ID
- FR-013: Validate task ID exists with error "Task ID X not found. Please try again."
- FR-006: Display "Task #X marked as complete!" or "Task #X marked as incomplete!"

### Implementation for User Story 2

- [X] T022 [US2] Implement `toggle_complete(task_id: int) -> tuple[bool, bool | None, str]` in `src/todo.py`
  - Call get_task_by_id(task_id)
  - If None: return (False, None, f"Task ID {task_id} not found. Please try again.")
  - Toggle task["completed"] = not task["completed"]
  - Store new_status = task["completed"]
  - If new_status is True: message = f"Task #{task_id} marked as complete!"
  - Else: message = f"Task #{task_id} marked as incomplete!"
  - Return (True, new_status, message)

- [X] T023 [US2] Implement `get_task_id() -> int` in `src/main.py`
  - Loop until valid:
    - Get input using input("Enter task ID: ")
    - Try to convert to int
    - If ValueError or negative: print "Invalid task ID. Please enter a positive number." and continue
    - If valid: return int task_id

- [X] T024 [US2] Implement `handle_mark_complete() -> None` in `src/main.py`
  - Call get_task_id() to get task_id
  - Call todo.toggle_complete(task_id)
  - Print message from returned tuple
  - If success: print new status (complete/incomplete)
  - Print empty line

**Checkpoint**: At this point, User Stories 1, 2, and 5 are fully functional (add, view, mark complete, menu navigation)

---

## Phase 6: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Edit task titles and descriptions to correct errors or clarify requirements

**Independent Test**: Add task with title "Reveiw code" (typo) → update to "Review code" with description "Focus on security" → view to confirm changes

**Acceptance**:
- FR-010: Update title and/or description by task ID
- FR-013: Validate empty title with error "Title cannot be empty. Please enter a title."
- FR-013: Validate task ID exists
- FR-006: Display "Task #X updated successfully!"

### Implementation for User Story 3

- [X] T025 [US3] Implement `update_task(task_id: int, title: str | None = None, description: str | None = None) -> tuple[bool, str]` in `src/todo.py`
  - Call get_task_by_id(task_id)
  - If None: return (False, f"Task ID {task_id} not found. Please try again.")
  - If title is not None:
    - Call validate_title(title)
    - If invalid: return (False, error_msg)
    - Update task["title"] = title
  - If description is not None:
    - Call validate_description(description)
    - If invalid: return (False, error_msg)
    - Update task["description"] = description
  - If both title and description are None: return (False, "No changes specified.")
  - Return (True, f"Task #{task_id} updated successfully!")

- [X] T026 [US3] Implement `handle_update_task() -> None` in `src/main.py`
  - Call get_task_id() to get task_id
  - Print "Leave blank to keep existing value"
  - Get new_title using input("Enter new title (or press Enter to skip): ")
  - Get new_desc using input("Enter new description (or press Enter to skip): ")
  - Convert empty strings to None: `title_arg = new_title if new_title else None`
  - Convert empty strings to None: `desc_arg = new_desc if new_desc else None`
  - If title_arg is not None: validate with todo.validate_title(), loop until valid or user provides empty
  - If desc_arg is not None: validate with todo.validate_description(), loop until valid or user provides empty
  - Call todo.update_task(task_id, title_arg, desc_arg)
  - Print message from returned tuple
  - Print empty line

**Checkpoint**: At this point, User Stories 1, 2, 3, and 5 are fully functional

---

## Phase 7: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Remove tasks that are no longer relevant or created by mistake

**Independent Test**: Add 3 tasks → delete task #2 by ID with confirmation → view list to see only #1 and #3 → attempt to delete #2 again to verify error

**Acceptance**:
- FR-011: Delete tasks by ID with Y/N confirmation
- FR-013: Validate task ID exists
- FR-006: Display "Task #X deleted successfully!" or "Deletion cancelled"

### Implementation for User Story 4

- [X] T027 [US4] Implement `delete_task(task_id: int) -> tuple[bool, str]` in `src/todo.py`
  - Call get_task_by_id(task_id)
  - If None: return (False, f"Task ID {task_id} not found. Please try again.")
  - Find index in tasks list where task["id"] == task_id
  - Remove task using tasks.pop(index) or tasks.remove(task)
  - Return (True, f"Task #{task_id} deleted successfully!")

- [X] T028 [US4] Implement `get_yes_no_confirmation(prompt: str) -> bool` in `src/main.py`
  - Loop until valid:
    - Get input using input(f"{prompt} (Y/N): ")
    - Convert to uppercase using .upper()
    - If input is "Y": return True
    - If input is "N": return False
    - Else: print "Invalid input. Please enter Y or N." and continue

- [X] T029 [US4] Implement `handle_delete_task() -> None` in `src/main.py`
  - Call get_task_id() to get task_id
  - Call get_yes_no_confirmation("Are you sure you want to delete this task?")
  - If False: print "Deletion cancelled" and return
  - Call todo.delete_task(task_id)
  - Print message from returned tuple
  - Print empty line

**Checkpoint**: All user stories (1-5) are fully functional - core features complete

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Code quality, documentation, and validation

- [X] T030 [P] Add type hints to all functions in `src/todo.py` (verify using signature annotations)
- [X] T031 [P] Add type hints to all functions in `src/main.py` (import `NoReturn` from typing for main_loop)
- [X] T032 [P] Add Google-style docstrings to all functions in `src/todo.py`
  - Include: Short description, Args section, Returns section
  - Example: validate_title, validate_description, add_task, etc.
- [X] T033 [P] Add Google-style docstrings to all functions in `src/main.py`
  - Include: Short description, Args section (if applicable), Returns section
  - Example: display_menu, display_tasks, get_menu_choice, etc.
- [X] T034 Run PEP 8 style check: verify 88-char line length, snake_case naming, proper imports
- [X] T035 Manual testing: Execute all 36 test cases from quickstart.md (create quickstart.md first if needed)
  - Test all 5 user stories independently
  - Test all edge cases from spec.md
  - Test all error messages from spec FR-013
  - NOTE: Automated tests created and passed; manual testing guide provided in TESTING.md
- [ ] T036 Fix any bugs discovered during manual testing
- [X] T037 Verify total line count < 500 lines using `wc -l src/*.py` or manual count

**Checkpoint**: Code complete, tested, and validated - ready for production use

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (T001-T004) - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (T005-T008)
- **User Story 5 (Phase 4)**: Depends on User Story 1 (T009-T018) for menu handlers
- **User Story 2 (Phase 5)**: Depends on Foundational (T005-T008)
- **User Story 3 (Phase 6)**: Depends on Foundational (T005-T008)
- **User Story 4 (Phase 7)**: Depends on Foundational (T005-T008)
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: CRITICAL - Required for User Story 5 (menu handlers)
- **User Story 5 (P1)**: CRITICAL - Required for full application (menu loop)
- **User Story 2 (P2)**: Independent of other stories (only depends on Foundational)
- **User Story 3 (P3)**: Independent of other stories (only depends on Foundational)
- **User Story 4 (P4)**: Independent of other stories (only depends on Foundational)

### Within Each User Story

- Business logic (todo.py) before UI layer (main.py) when calling business logic functions
- Validation functions (T007-T008) before CRUD operations
- Helper functions (get_title_input, get_task_id) before menu handlers
- Menu handlers before main_loop integration

### Parallel Opportunities

- **Phase 1 Setup**: T003 and T004 can run in parallel (different files)
- **Phase 2 Foundational**: T007 and T008 can run in parallel (validation functions independent)
- **Phase 3 User Story 1**: T012, T013, T014 can run in parallel after T009-T011 complete
- **Phase 8 Polish**: T030-T033 can run in parallel (different concerns)
- **After Foundational**: User Stories 2, 3, 4 can theoretically run in parallel (different CRUD operations)

---

## Implementation Strategy

### MVP First (User Stories 1 and 5 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T008) - CRITICAL
3. Complete Phase 3: User Story 1 (T009-T018) - Add and View
4. Complete Phase 4: User Story 5 (T019-T021) - Menu Navigation
5. **STOP and VALIDATE**: Test basic workflow (add → view → exit)
6. Result: Functional MVP with add, view, and exit features

### Incremental Delivery

1. MVP (US1 + US5) → Test independently → Demo basic todo list
2. Add User Story 2 (T022-T024) → Test independently → Demo completion tracking
3. Add User Story 3 (T025-T026) → Test independently → Demo editing
4. Add User Story 4 (T027-T029) → Test independently → Demo deletion
5. Complete Polish (T030-T037) → Full validation → Production ready

### Sequential Implementation (Recommended for Solo Developer)

Follow phases in order (Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 → Phase 7 → Phase 8):
- Ensures each user story is complete before moving to next
- Allows for early validation at checkpoints
- Aligns with priority order (P1 → P2 → P3 → P4)

---

## Notes

- **[P] tasks**: Different files or independent functions, can run in parallel
- **[Story] label**: Maps task to specific user story (US1-US5) for traceability
- **Type hints**: Required on all functions per Constitution Principle VI
- **Docstrings**: Google-style required per Constitution Principle VI
- **Error messages**: Must match spec FR-013 exactly
- **Line limit**: Total code must be < 500 lines per Constitution
- **Manual testing**: Automated tests NOT included (Phase 1 scope)
- **Commit strategy**: Commit after each phase or logical task group
- **Checkpoints**: Stop and validate at each checkpoint before proceeding

---

## Manual Test Cases Reference

The following test cases from spec.md should be validated in T035:

**User Story 1 (Add/View)**:
1. Add task with title and description → verify confirmation with ID
2. View 3 tasks → verify all display with ID, status, timestamp
3. View empty list → verify "No tasks found" message
4. Add task with very long title/description → verify no crash

**User Story 2 (Mark Complete)**:
5. Mark incomplete task → verify "marked as complete" message
6. Mark complete task → verify "marked as incomplete" message
7. Mark non-existent task → verify "not found" error
8. View mixed complete/incomplete → verify ✓ and ☐ symbols

**User Story 3 (Update)**:
9. Update both title and description → verify success
10. Update only title → verify description unchanged
11. Update with empty title → verify error message
12. Update non-existent task → verify "not found" error

**User Story 4 (Delete)**:
13. Delete with Y confirmation → verify success
14. Delete with N confirmation → verify cancellation
15. View after deletion → verify task removed
16. Delete non-existent task → verify "not found" error

**User Story 5 (Menu/Navigation)**:
17. Display menu → verify 6 options numbered
18. Select valid options 1-5 → verify navigation works
19. Select invalid option 7 → verify error message
20. Enter non-numeric "abc" → verify error message
21. Select option 6 → verify clean exit

**Edge Cases**:
22. Empty title on add → verify error
23. Exactly 200 char title → verify accepts
24. 201 char title → verify error
25. Exactly 1000 char description → verify accepts
26. 1001 char description → verify error
27. Non-existent ID operations → verify errors
28. ID sequence after deletion → verify never reuse
29. Special characters in input → verify no crash
30. Rapid operations → verify state consistency

**Additional Validation**:
31. UTF-8 symbols display correctly (or fallback to ASCII)
32. Timestamps in ISO 8601 format (YYYY-MM-DD HH:MM:SS)
33. IDs auto-increment correctly
34. Ctrl+C exits gracefully
35. Menu returns after each operation
36. All success/error messages match spec
