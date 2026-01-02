"""Automated tests for todo.py business logic."""

import sys
sys.path.insert(0, 'src')

import todo

def reset_state():
    """Reset module state between tests."""
    todo.tasks.clear()
    todo.next_id = 1

def test_validate_title():
    """Test title validation."""
    print("Testing validate_title()...")

    # Valid title
    valid, msg = todo.validate_title("Valid title")
    assert valid == True, "Should accept valid title"
    assert msg == "", "Should have empty error message"

    # Empty title
    valid, msg = todo.validate_title("")
    assert valid == False, "Should reject empty title"
    assert "cannot be empty" in msg, f"Wrong error message: {msg}"

    # Title too long
    valid, msg = todo.validate_title("x" * 201)
    assert valid == False, "Should reject title > 200 chars"
    assert "too long" in msg, f"Wrong error message: {msg}"

    # Exactly 200 chars (boundary)
    valid, msg = todo.validate_title("x" * 200)
    assert valid == True, "Should accept exactly 200 chars"

    print("[PASS] validate_title()")

def test_validate_description():
    """Test description validation."""
    print("Testing validate_description()...")

    # Valid description
    valid, msg = todo.validate_description("Valid description")
    assert valid == True, "Should accept valid description"

    # Empty description (allowed)
    valid, msg = todo.validate_description("")
    assert valid == True, "Should accept empty description"

    # Description too long
    valid, msg = todo.validate_description("x" * 1001)
    assert valid == False, "Should reject description > 1000 chars"
    assert "too long" in msg, f"Wrong error message: {msg}"

    # Exactly 1000 chars (boundary)
    valid, msg = todo.validate_description("x" * 1000)
    assert valid == True, "Should accept exactly 1000 chars"

    print("[PASS] validate_description()")

def test_add_task():
    """Test adding tasks."""
    print("Testing add_task()...")
    reset_state()

    # Add first task
    success, task_id, msg = todo.add_task("Task 1", "Description 1")
    assert success == True, "Should successfully add task"
    assert task_id == 1, f"First task should have ID 1, got {task_id}"
    assert "Task #1 created successfully!" in msg, f"Wrong message: {msg}"

    # Add second task
    success, task_id, msg = todo.add_task("Task 2", "Description 2")
    assert success == True, "Should successfully add second task"
    assert task_id == 2, f"Second task should have ID 2, got {task_id}"

    # Verify tasks list
    assert len(todo.tasks) == 2, f"Should have 2 tasks, got {len(todo.tasks)}"
    assert todo.next_id == 3, f"next_id should be 3, got {todo.next_id}"

    # Add task with invalid title
    success, task_id, msg = todo.add_task("", "Description")
    assert success == False, "Should reject empty title"
    assert task_id is None, "task_id should be None on failure"
    assert "cannot be empty" in msg, f"Wrong error message: {msg}"

    # Add task with invalid description
    success, task_id, msg = todo.add_task("Valid", "x" * 1001)
    assert success == False, "Should reject long description"
    assert task_id is None, "task_id should be None on failure"

    print("[PASS] add_task()")

def test_get_all_tasks():
    """Test retrieving all tasks."""
    print("Testing get_all_tasks()...")
    reset_state()

    # Empty list
    all_tasks = todo.get_all_tasks()
    assert len(all_tasks) == 0, "Should return empty list"

    # Add tasks
    todo.add_task("Task 1", "Desc 1")
    todo.add_task("Task 2", "Desc 2")

    all_tasks = todo.get_all_tasks()
    assert len(all_tasks) == 2, f"Should return 2 tasks, got {len(all_tasks)}"
    assert all_tasks[0]["id"] == 1, "First task should have ID 1"
    assert all_tasks[1]["id"] == 2, "Second task should have ID 2"

    # Verify it's a copy
    all_tasks.append({"id": 999})
    assert len(todo.tasks) == 2, "Original list should not be modified"

    print("[PASS] get_all_tasks()")

def test_get_task_by_id():
    """Test finding task by ID."""
    print("Testing get_task_by_id()...")
    reset_state()

    # Non-existent ID
    task = todo.get_task_by_id(1)
    assert task is None, "Should return None for non-existent ID"

    # Add tasks
    todo.add_task("Task 1", "Desc 1")
    todo.add_task("Task 2", "Desc 2")

    # Find existing task
    task = todo.get_task_by_id(1)
    assert task is not None, "Should find existing task"
    assert task["id"] == 1, "Should return correct task"
    assert task["title"] == "Task 1", "Should have correct title"

    # Find second task
    task = todo.get_task_by_id(2)
    assert task["id"] == 2, "Should find second task"

    # Non-existent ID with existing tasks
    task = todo.get_task_by_id(999)
    assert task is None, "Should return None for non-existent ID"

    print("[PASS] get_task_by_id()")

def test_toggle_complete():
    """Test toggling completion status."""
    print("Testing toggle_complete()...")
    reset_state()

    # Non-existent task
    success, status, msg = todo.toggle_complete(1)
    assert success == False, "Should fail for non-existent task"
    assert status is None, "Status should be None on failure"
    assert "not found" in msg, f"Wrong error message: {msg}"

    # Add task
    todo.add_task("Task 1", "Desc 1")
    task = todo.get_task_by_id(1)
    assert task["completed"] == False, "New task should be incomplete"

    # Mark complete
    success, status, msg = todo.toggle_complete(1)
    assert success == True, "Should successfully toggle"
    assert status == True, f"Should be complete, got {status}"
    assert "marked as complete" in msg, f"Wrong message: {msg}"
    assert task["completed"] == True, "Task should be marked complete"

    # Mark incomplete
    success, status, msg = todo.toggle_complete(1)
    assert success == True, "Should successfully toggle back"
    assert status == False, f"Should be incomplete, got {status}"
    assert "marked as incomplete" in msg, f"Wrong message: {msg}"
    assert task["completed"] == False, "Task should be marked incomplete"

    print("[PASS] toggle_complete()")

def test_update_task():
    """Test updating task."""
    print("Testing update_task()...")
    reset_state()

    # Non-existent task
    success, msg = todo.update_task(1, "New title")
    assert success == False, "Should fail for non-existent task"
    assert "not found" in msg, f"Wrong error message: {msg}"

    # Add task
    todo.add_task("Original Title", "Original Description")

    # Update title only
    success, msg = todo.update_task(1, title="New Title")
    assert success == True, "Should successfully update"
    assert "updated successfully" in msg, f"Wrong message: {msg}"
    task = todo.get_task_by_id(1)
    assert task["title"] == "New Title", "Title should be updated"
    assert task["description"] == "Original Description", "Description should be unchanged"

    # Update description only
    success, msg = todo.update_task(1, description="New Description")
    assert success == True, "Should successfully update"
    task = todo.get_task_by_id(1)
    assert task["title"] == "New Title", "Title should be unchanged"
    assert task["description"] == "New Description", "Description should be updated"

    # Update both
    success, msg = todo.update_task(1, "Both Updated", "Both Updated Desc")
    assert success == True, "Should successfully update both"
    task = todo.get_task_by_id(1)
    assert task["title"] == "Both Updated", "Title should be updated"
    assert task["description"] == "Both Updated Desc", "Description should be updated"

    # Update with invalid title
    success, msg = todo.update_task(1, title="")
    assert success == False, "Should reject empty title"
    assert "cannot be empty" in msg, f"Wrong error message: {msg}"

    # No changes specified
    success, msg = todo.update_task(1)
    assert success == False, "Should fail with no changes"
    assert "No changes" in msg, f"Wrong error message: {msg}"

    print("[PASS] update_task()")

def test_delete_task():
    """Test deleting task."""
    print("Testing delete_task()...")
    reset_state()

    # Non-existent task
    success, msg = todo.delete_task(1)
    assert success == False, "Should fail for non-existent task"
    assert "not found" in msg, f"Wrong error message: {msg}"

    # Add tasks
    todo.add_task("Task 1", "Desc 1")
    todo.add_task("Task 2", "Desc 2")
    todo.add_task("Task 3", "Desc 3")

    # Delete middle task
    success, msg = todo.delete_task(2)
    assert success == True, "Should successfully delete"
    assert "deleted successfully" in msg, f"Wrong message: {msg}"
    assert len(todo.tasks) == 2, f"Should have 2 tasks, got {len(todo.tasks)}"

    # Verify correct task deleted
    task = todo.get_task_by_id(2)
    assert task is None, "Task 2 should be deleted"
    task1 = todo.get_task_by_id(1)
    task3 = todo.get_task_by_id(3)
    assert task1 is not None, "Task 1 should still exist"
    assert task3 is not None, "Task 3 should still exist"

    # Try to delete already deleted task
    success, msg = todo.delete_task(2)
    assert success == False, "Should fail for already deleted task"
    assert "not found" in msg, f"Wrong error message: {msg}"

    print("[PASS] delete_task()")

def test_id_sequence():
    """Test ID sequence behavior."""
    print("Testing ID sequence...")
    reset_state()

    # Add 3 tasks
    _, id1, _ = todo.add_task("Task 1", "")
    _, id2, _ = todo.add_task("Task 2", "")
    _, id3, _ = todo.add_task("Task 3", "")

    assert id1 == 1, "First ID should be 1"
    assert id2 == 2, "Second ID should be 2"
    assert id3 == 3, "Third ID should be 3"

    # Delete middle task
    todo.delete_task(2)

    # Add new task - should NOT reuse ID 2
    _, id4, _ = todo.add_task("Task 4", "")
    assert id4 == 4, f"Next ID should be 4 (not reusing 2), got {id4}"
    assert todo.next_id == 5, f"next_id should be 5, got {todo.next_id}"

    print("[PASS] ID sequence")

def run_all_tests():
    """Run all tests."""
    print("=" * 50)
    print("Running Automated Tests for todo.py")
    print("=" * 50)
    print()

    try:
        test_validate_title()
        test_validate_description()
        test_add_task()
        test_get_all_tasks()
        test_get_task_by_id()
        test_toggle_complete()
        test_update_task()
        test_delete_task()
        test_id_sequence()

        print()
        print("=" * 50)
        print("[SUCCESS] ALL TESTS PASSED!")
        print("=" * 50)
        return True
    except AssertionError as e:
        print()
        print("=" * 50)
        print(f"[FAIL] TEST FAILED: {e}")
        print("=" * 50)
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
