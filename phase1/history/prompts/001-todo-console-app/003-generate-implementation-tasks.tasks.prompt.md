---
id: 003
title: Generate Implementation Tasks
stage: tasks
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5
feature: 001-todo-console-app
branch: 001-todo-console-app
user: developer
command: /sp.tasks
labels: ["task-breakdown", "implementation-planning", "user-stories"]
links:
  spec: specs/001-todo-console-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-todo-console-app/tasks.md
tests:
  - Manual test cases referenced in tasks.md (T035)
---

## Prompt

/sp.tasks

Reflect on: Constitution, Specification, and Plan from previous steps

Break down the implementation into specific coding tasks following the plan's implementation order.

Task Breakdown:

Foundation Tasks (todo.py setup):
T001: Create module-level storage
- Create tasks = [] list
- Create next_id = 1 counter
- Add type hints at module level
- Acceptance: Module imports without errors

T002: Implement validate_title()
- Check title is not empty
- Check length 1-200 characters
- Return (is_valid: bool, error_msg: str)
- Acceptance: Handles empty, valid, and too-long inputs

T003: Implement validate_description()
- Check max 1000 characters
- Return (is_valid: bool, error_msg: str)
- Acceptance: Handles None, valid, and too-long inputs

Core CRUD Tasks (todo.py operations):
T004: Implement add_task(title, description)
- Validate title and description
- Generate ID using next_id counter
- Create timestamp with datetime.now().isoformat()
- Append task dict to tasks list
- Increment next_id
- Return (True, task_id, "Task added") or (False, None, error_msg)
- Acceptance: Creates valid task, rejects invalid input

T005: Implement get_all_tasks()
- Return copy of tasks list
- Return empty list if no tasks
- Acceptance: Returns all tasks without modifying original

T006: Implement get_task_by_id(task_id)
- Search tasks list for matching ID
- Return (True, task_dict) or (False, None)
- Acceptance: Finds existing ID, returns False for invalid ID

T007: Implement update_task(task_id, title, description)
- Validate task_id exists
- Validate new title/description if provided
- Update only provided fields
- Return (True, "Task updated") or (False, error_msg)
- Acceptance: Updates fields, validates input, handles non-existent ID

T008: Implement delete_task(task_id)
- Validate task_id exists
- Remove from tasks list
- Return (True, "Task deleted") or (False, error_msg)
- Acceptance: Deletes existing task, handles invalid ID

T009: Implement toggle_complete(task_id)
- Validate task_id exists
- Toggle completed boolean
- Return (True, new_status, "Task marked complete/incomplete") or (False, None, error_msg)
- Acceptance: Toggles status, handles invalid ID

UI Layer Tasks (main.py):
T010: Implement display_menu()
- Print numbered menu (1-6)
- Clear formatting
- Acceptance: Displays all 6 options

T011: Implement display_tasks(tasks)
- Handle empty list case
- Format each task with ID, title, status (✓/✗), date
- Show description if exists
- Acceptance: Displays all tasks, handles empty state

T012: Implement get_menu_choice()
- Get user input
- Validate numeric 1-6
- Return choice or None for invalid
- Handle ValueError for non-numeric input
- Acceptance: Returns valid choice, handles invalid input gracefully

Menu Handler Tasks (main.py):
T013: Implement handle_add_task()
- Prompt for title
- Prompt for description (optional)
- Call todo.add_task()
- Display success/error message
- Acceptance: Adds task via UI, shows feedback

T014: Implement handle_view_tasks()
- Call todo.get_all_tasks()
- Pass to display_tasks()
- Acceptance: Shows all tasks

T015: Implement handle_update_task()
- Prompt for task ID
- Prompt for new title (optional)
- Prompt for new description (optional)
- Call todo.update_task()
- Display result
- Acceptance: Updates task via UI, handles errors

T016: Implement handle_delete_task()
- Prompt for task ID
- Confirm deletion (Y/N)
- Call todo.delete_task() if confirmed
- Display result
- Acceptance: Deletes with confirmation, handles cancellation

T017: Implement handle_toggle_complete()
- Prompt for task ID
- Call todo.toggle_complete()
- Display new status
- Acceptance: Toggles status via UI, shows result

Integration Tasks (main.py):
T018: Implement main_loop()
- Welcome message
- While loop until exit
- Display menu
- Get choice
- Route to handlers (1-5)
- Exit on choice 6
- Handle Ctrl+C gracefully
- Acceptance: Full menu cycle works, exits cleanly

T019: Add if __name__ == "__main__" entry point
- Call main_loop()
- Acceptance: Runs with `python src/main.py`

Polish Tasks:
T020: Add type hints to all functions
- Import from typing module
- Add to all function signatures
- Acceptance: Passes type checking

T021: Add docstrings to all functions
- Google-style format
- Args, Returns, Examples
- Acceptance: All functions documented

T022: Manual testing
- Run all 36 test cases from quickstart.md
- Fix any bugs found
- Acceptance: All tests pass

Implementation Order:
1. Foundation (T001-T003): 30 min
2. Core CRUD (T004-T009): 90 min
3. UI Layer (T010-T012): 45 min
4. Handlers (T013-T017): 60 min
5. Integration (T018-T019): 30 min
6. Polish (T020-T022): 45 min

Total estimated time: 5 hours

Ready for /sp.implement to execute these tasks with Claude Code.

## Response snapshot

I've created a comprehensive tasks.md file at specs/001-todo-console-app/tasks.md with 37 detailed implementation tasks organized by user story and priority.

**Key Structure**:
- **Phase 1: Setup** (T001-T004) - Project structure initialization
- **Phase 2: Foundational** (T005-T008) - Core validation and data structures that ALL user stories depend on
- **Phase 3: User Story 1** (T009-T018) - Add and View Tasks (P1, MVP)
- **Phase 4: User Story 5** (T019-T021) - Menu Navigation and Exit (P1, MVP)
- **Phase 5: User Story 2** (T022-T024) - Mark Complete/Incomplete (P2)
- **Phase 6: User Story 3** (T025-T026) - Update Task Details (P3)
- **Phase 7: User Story 4** (T027-T029) - Delete Tasks (P4)
- **Phase 8: Polish** (T030-T037) - Type hints, docstrings, testing, validation

**Task Details**:
- Each task includes specific acceptance criteria
- File paths are explicit (src/todo.py vs src/main.py)
- Function signatures match plan.md contracts exactly
- Error messages match spec.md FR-013 requirements
- Parallel opportunities marked with [P] tag
- User story tags [US1-US5] for traceability

**Implementation Strategy**:
- MVP First: Phases 1-4 deliver basic add/view/navigate functionality
- Incremental: Each user story can be validated independently
- Sequential recommended for solo developer following priority order
- Clear checkpoints after each phase for validation

**Manual Test Cases**: 36 test cases referenced from spec.md edge cases and acceptance scenarios, to be executed in task T035.

**Dependencies**:
- Foundational phase (T005-T008) BLOCKS all user stories
- User Story 1 required before User Story 5 (menu handlers dependency)
- Other user stories (2, 3, 4) are independent and can run in parallel after foundation

The tasks follow the plan's implementation order, maintain constitution compliance (simplicity, clean architecture, no persistence), and ensure all spec requirements are covered with testable acceptance criteria.

## Outcome

- ✅ Impact: Created comprehensive task breakdown with 37 specific, actionable tasks organized by 5 user stories with clear dependencies and acceptance criteria
- 🧪 Tests: 36 manual test cases referenced for T035 validation; automated tests not in Phase 1 scope
- 📁 Files: Created specs/001-todo-console-app/tasks.md (comprehensive implementation task list)
- 🔁 Next prompts: /sp.implement to execute tasks following the task order and checkpoints
- 🧠 Reflection: Task breakdown successfully maps plan.md contracts to specific implementation steps, organized by user story for independent validation. Clear separation between foundational tasks (blocking) and user story tasks (potentially parallel) enables flexible implementation strategies.

## Evaluation notes (flywheel)

- Failure modes observed: None - task generation followed plan.md structure and spec.md requirements accurately
- Graders run and results (PASS/FAIL): Manual validation - PASS (all spec requirements mapped to tasks, all plan functions covered, constitution compliance maintained)
- Prompt variant (if applicable): Standard /sp.tasks command with user-provided task outline
- Next experiment (smallest change to try): Consider adding task time estimates for better project management (currently estimation removed per agent guidelines)
