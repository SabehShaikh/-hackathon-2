# Manual Testing Guide - Todo Console App

## Automated Test Results

✅ **All automated business logic tests passed!**

Tested functions:
- [PASS] validate_title() - empty, too long, boundary values
- [PASS] validate_description() - empty (allowed), too long, boundary values
- [PASS] add_task() - valid tasks, invalid inputs, ID generation
- [PASS] get_all_tasks() - empty list, multiple tasks, copy behavior
- [PASS] get_task_by_id() - existing/non-existing IDs
- [PASS] toggle_complete() - status toggling, error handling
- [PASS] update_task() - partial updates, validation, error handling
- [PASS] delete_task() - deletion, error handling
- [PASS] ID sequence - sequential generation, no reuse after deletion

## Manual Testing Checklist (T035)

### Prerequisites
```bash
cd src
python main.py
```

---

### User Story 1: Add and View Tasks (4 tests)

**Test 1.1: Add task with title and description**
- [ ] Select option 1 (Add Task)
- [ ] Enter title: "Review pull requests"
- [ ] Enter description: "Check PRs from team members"
- [ ] Verify: "Task #1 created successfully!" displayed
- [ ] Select option 2 (View All Tasks)
- [ ] Verify: Task appears with [1] ☐ "Review pull requests" (Created: timestamp)
- [ ] Verify: Description "Check PRs from team members" appears indented

**Test 1.2: View multiple tasks**
- [ ] Add 2 more tasks with different titles/descriptions
- [ ] Select option 2
- [ ] Verify: All 3 tasks displayed with IDs 1, 2, 3
- [ ] Verify: All have ☐ symbol (incomplete)
- [ ] Verify: All have timestamps

**Test 1.3: View empty list**
- [ ] Exit app (option 6)
- [ ] Restart app
- [ ] Select option 2
- [ ] Verify: "No tasks found" message displayed

**Test 1.4: Add task with long title/description**
- [ ] Add task with 190-character title and 900-character description
- [ ] Verify: Task created successfully
- [ ] View tasks
- [ ] Verify: Full title and description displayed without truncation

---

### User Story 2: Mark Complete/Incomplete (4 tests)

**Test 2.1: Mark task complete**
- [ ] Add 2 tasks
- [ ] Select option 5 (Mark Complete/Incomplete)
- [ ] Enter task ID: 1
- [ ] Verify: "Task #1 marked as complete!" displayed
- [ ] View tasks (option 2)
- [ ] Verify: Task #1 shows ✓ symbol (complete)
- [ ] Verify: Task #2 still shows ☐ symbol (incomplete)

**Test 2.2: Mark complete task incomplete**
- [ ] Select option 5
- [ ] Enter task ID: 1 (the complete task)
- [ ] Verify: "Task #1 marked as incomplete!" displayed
- [ ] View tasks
- [ ] Verify: Task #1 shows ☐ symbol again

**Test 2.3: Mark non-existent task**
- [ ] Select option 5
- [ ] Enter task ID: 999
- [ ] Verify: "Task ID 999 not found. Please try again." displayed
- [ ] Verify: Returns to main menu without crashing

**Test 2.4: Mixed complete/incomplete display**
- [ ] Mark task #1 as complete
- [ ] Leave task #2 as incomplete
- [ ] View tasks
- [ ] Verify: Task #1 has ✓, task #2 has ☐

---

### User Story 3: Update Task (4 tests)

**Test 3.1: Update both title and description**
- [ ] Add task: "Reveiw code" (typo), description: "Old desc"
- [ ] Select option 3 (Update Task)
- [ ] Enter task ID: 1
- [ ] Enter new title: "Review code" (fixed typo)
- [ ] Enter new description: "Focus on security issues"
- [ ] Verify: "Task #1 updated successfully!" displayed
- [ ] View tasks
- [ ] Verify: Title updated to "Review code"
- [ ] Verify: Description updated to "Focus on security issues"

**Test 3.2: Update only title**
- [ ] Select option 3
- [ ] Enter task ID: 1
- [ ] Enter new title: "Review security code"
- [ ] Press Enter (skip description)
- [ ] Verify: Title updated
- [ ] View tasks
- [ ] Verify: Description unchanged from previous value

**Test 3.3: Update with empty title (should fail)**
- [ ] Select option 3
- [ ] Enter task ID: 1
- [ ] Enter empty title (just press Enter)
- [ ] Enter valid description
- [ ] Verify: "No changes specified." displayed (since empty title skips)

**Test 3.4: Update non-existent task**
- [ ] Select option 3
- [ ] Enter task ID: 999
- [ ] Verify: "Task ID 999 not found. Please try again." displayed

---

### User Story 4: Delete Task (4 tests)

**Test 4.1: Delete with confirmation (Y)**
- [ ] Add 3 tasks (IDs 1, 2, 3)
- [ ] Select option 4 (Delete Task)
- [ ] Enter task ID: 2
- [ ] Enter: Y
- [ ] Verify: "Task #2 deleted successfully!" displayed
- [ ] View tasks
- [ ] Verify: Only tasks #1 and #3 displayed
- [ ] Verify: Task #2 no longer appears

**Test 4.2: Delete with cancellation (N)**
- [ ] Select option 4
- [ ] Enter task ID: 3
- [ ] Enter: N
- [ ] Verify: "Deletion cancelled" displayed
- [ ] View tasks
- [ ] Verify: Task #3 still exists

**Test 4.3: View after deletion (gap in IDs)**
- [ ] With tasks 1 and 3 remaining (2 deleted)
- [ ] View tasks
- [ ] Verify: Only IDs 1 and 3 shown
- [ ] Verify: ID 3 not shown (confirms deletion)

**Test 4.4: Delete non-existent task**
- [ ] Select option 4
- [ ] Enter task ID: 2 (already deleted)
- [ ] Verify: "Task ID 2 not found. Please try again." displayed

---

### User Story 5: Menu Navigation and Exit (5 tests)

**Test 5.1: Display menu**
- [ ] Launch app
- [ ] Verify: "=== Todo List Manager ===" header
- [ ] Verify: Options 1-6 clearly numbered
- [ ] Verify: "Enter choice (1-6):" prompt

**Test 5.2: Navigate all options**
- [ ] Enter 1 → Verify: Add Task screen appears
- [ ] Return to menu
- [ ] Enter 2 → Verify: View All Tasks screen appears
- [ ] Enter 3 → Verify: Update Task screen appears
- [ ] Enter 4 → Verify: Delete Task screen appears
- [ ] Enter 5 → Verify: Mark Complete screen appears

**Test 5.3: Invalid choice (out of range)**
- [ ] Enter: 7
- [ ] Verify: "Invalid choice. Please enter a number between 1-6." displayed
- [ ] Verify: Menu re-displays

**Test 5.4: Invalid choice (non-numeric)**
- [ ] Enter: abc
- [ ] Verify: "Invalid choice. Please enter a number between 1-6." displayed
- [ ] Verify: Menu re-displays

**Test 5.5: Clean exit**
- [ ] Select option 6
- [ ] Verify: "Goodbye! Note: All tasks will be lost (in-memory mode)." displayed
- [ ] Verify: App exits cleanly without errors

---

### Edge Cases (9 tests)

**Edge 1: Empty title on add**
- [ ] Select option 1
- [ ] Press Enter without typing title
- [ ] Verify: "Title cannot be empty. Please enter a title." displayed
- [ ] Verify: Re-prompts for title

**Edge 2: Exactly 200-character title**
- [ ] Add task with exactly 200 characters in title
- [ ] Verify: Task created successfully

**Edge 3: 201-character title**
- [ ] Try to add task with 201 characters
- [ ] Verify: "Title too long (max 200 characters). Please shorten." displayed

**Edge 4: Exactly 1000-character description**
- [ ] Add task with exactly 1000 characters in description
- [ ] Verify: Task created successfully

**Edge 5: 1001-character description**
- [ ] Try to add task with 1001 characters
- [ ] Verify: "Description too long (max 1000 characters). Please shorten." displayed

**Edge 6: Non-existent ID operations**
- [ ] Try to view/update/delete/mark complete task ID 999
- [ ] Verify: "Task ID 999 not found. Please try again." for each

**Edge 7: ID sequence after deletion**
- [ ] Add tasks 1, 2, 3
- [ ] Delete task 2
- [ ] Add new task
- [ ] Verify: New task has ID 4 (not reusing 2)

**Edge 8: Special characters in input**
- [ ] Add task with title: `Task with "quotes" and 'apostrophes'`
- [ ] Add task with description containing: \\ / | < >
- [ ] Verify: Characters stored and displayed correctly

**Edge 9: Rapid operations**
- [ ] Quickly add 10 tasks
- [ ] Delete 5 tasks
- [ ] Update 3 tasks
- [ ] Mark 4 complete
- [ ] View all
- [ ] Verify: All operations completed correctly

---

### Additional Validation (6 tests)

**Valid 1: UTF-8 symbols display (or ASCII fallback)**
- [ ] Mark a task complete
- [ ] View tasks
- [ ] Verify: Either ✓/☐ symbols OR [X]/[ ] displayed consistently

**Valid 2: Timestamps in ISO 8601 format**
- [ ] Add task
- [ ] View tasks
- [ ] Verify: Timestamp shows "YYYY-MM-DD HH:MM:SS" format

**Valid 3: IDs auto-increment correctly**
- [ ] Add 5 tasks without deletions
- [ ] Verify: IDs are 1, 2, 3, 4, 5 in sequence

**Valid 4: Ctrl+C graceful exit**
- [ ] Launch app
- [ ] Press Ctrl+C
- [ ] Verify: "Goodbye! Note: All tasks will be lost (in-memory mode)." displayed
- [ ] Verify: App exits without errors

**Valid 5: Menu returns after each operation**
- [ ] Perform any operation (add/view/update/delete/mark)
- [ ] Verify: Returns to main menu after completion

**Valid 6: All error messages match spec**
- [ ] Test each error condition
- [ ] Verify: Error messages exactly match spec FR-013

---

## Test Summary

**Total Tests**: 36

- User Story 1 (Add/View): 4 tests
- User Story 2 (Mark Complete): 4 tests
- User Story 3 (Update): 4 tests
- User Story 4 (Delete): 4 tests
- User Story 5 (Menu/Exit): 5 tests
- Edge Cases: 9 tests
- Additional Validation: 6 tests

## Bugs Found

Document any bugs discovered during testing in T036:

```
BUG #: [Description]
Severity: [High/Medium/Low]
Steps to Reproduce:
1. ...
2. ...
Expected: ...
Actual: ...
```

## Sign-off

- [ ] All 36 tests completed
- [ ] All tests passed
- [ ] No bugs found (or all bugs fixed)
- [ ] Ready for production use

Tester: ___________________
Date: ___________________
