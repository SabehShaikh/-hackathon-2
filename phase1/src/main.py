"""Todo UI layer - menu display, user input handling, and output formatting."""

import todo
from typing import Any


def display_menu() -> None:
    """Display the main menu with 6 numbered options."""
    print("=== Todo List Manager ===")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Complete/Incomplete")
    print("6. Exit")
    print()


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
    if not tasks:
        print("No tasks found")
        return

    for task in tasks:
        # Try UTF-8 symbols, fallback to ASCII if encoding fails
        status_symbol = "✓" if task["completed"] else "☐"

        try:
            print(f"[{task['id']}] {status_symbol} {task['title']} (Created: {task['created_at']})")
            if task["description"]:
                print(f"    {task['description']}")
        except UnicodeEncodeError:
            # Fallback to ASCII symbols if UTF-8 not supported
            status_symbol = "[X]" if task["completed"] else "[ ]"
            print(f"[{task['id']}] {status_symbol} {task['title']} (Created: {task['created_at']})")
            if task["description"]:
                print(f"    {task['description']}")


def get_title_input(prompt: str = "Enter task title: ") -> str:
    """Prompt for task title with validation.

    Args:
        prompt: Custom prompt message

    Returns:
        Valid title (1-200 characters)

    Loops until valid input received.
    """
    while True:
        title_input = input(prompt)
        is_valid, error_msg = todo.validate_title(title_input)
        if is_valid:
            return title_input
        print(error_msg)


def get_description_input() -> str:
    """Prompt for task description (optional).

    Returns:
        Description string (may be empty, max 1000 chars)

    Loops until valid input received.
    """
    while True:
        desc_input = input("Enter task description (optional, press Enter to skip): ")
        if not desc_input:
            return ""
        is_valid, error_msg = todo.validate_description(desc_input)
        if is_valid:
            return desc_input
        print(error_msg)


def handle_add_task() -> None:
    """Handle Add Task menu option (Option 1)."""
    title = get_title_input()
    description = get_description_input()
    success, task_id, message = todo.add_task(title, description)
    print(message)
    print()


def handle_view_tasks() -> None:
    """Handle View All Tasks menu option (Option 2)."""
    all_tasks = todo.get_all_tasks()
    display_tasks(all_tasks)
    print()


def get_task_id() -> int:
    """Prompt user for task ID with validation.

    Returns:
        Task ID (positive integer)

    Handles:
        - Non-numeric input
        - Negative numbers
        - Empty input
    """
    while True:
        try:
            task_id_input = input("Enter task ID: ")
            task_id = int(task_id_input)
            if task_id > 0:
                return task_id
            print("Invalid task ID. Please enter a positive number.")
        except ValueError:
            print("Invalid task ID. Please enter a positive number.")


def handle_update_task() -> None:
    """Handle Update Task menu option (Option 3)."""
    task_id = get_task_id()
    print("Leave blank to keep existing value")

    # Get new title
    new_title_input = input("Enter new title (or press Enter to skip): ")
    title_arg = None
    if new_title_input:
        # Validate title
        while True:
            is_valid, error_msg = todo.validate_title(new_title_input)
            if is_valid:
                title_arg = new_title_input
                break
            print(error_msg)
            new_title_input = input("Enter new title (or press Enter to skip): ")
            if not new_title_input:
                break

    # Get new description
    new_desc_input = input("Enter new description (or press Enter to skip): ")
    desc_arg = None
    if new_desc_input:
        # Validate description
        while True:
            is_valid, error_msg = todo.validate_description(new_desc_input)
            if is_valid:
                desc_arg = new_desc_input
                break
            print(error_msg)
            new_desc_input = input("Enter new description (or press Enter to skip): ")
            if not new_desc_input:
                break

    success, message = todo.update_task(task_id, title_arg, desc_arg)
    print(message)
    print()


def get_yes_no_confirmation(prompt: str) -> bool:
    """Prompt for Y/N confirmation.

    Args:
        prompt: Question to ask user

    Returns:
        True if 'Y' or 'y', False if 'N' or 'n'

    Loops until valid input (Y/N) received.
    """
    while True:
        response = input(f"{prompt} (Y/N): ")
        if response.upper() == "Y":
            return True
        elif response.upper() == "N":
            return False
        else:
            print("Invalid input. Please enter Y or N.")


def handle_delete_task() -> None:
    """Handle Delete Task menu option (Option 4)."""
    task_id = get_task_id()
    confirmed = get_yes_no_confirmation("Are you sure you want to delete this task?")
    if not confirmed:
        print("Deletion cancelled")
        print()
        return

    success, message = todo.delete_task(task_id)
    print(message)
    print()


def handle_mark_complete() -> None:
    """Handle Mark Complete/Incomplete menu option (Option 5)."""
    task_id = get_task_id()
    success, new_status, message = todo.toggle_complete(task_id)
    print(message)
    print()


def get_menu_choice() -> int:
    """Prompt user for menu choice (1-6) with validation.

    Returns:
        Valid menu choice (1-6)

    Handles:
        - Non-numeric input
        - Out-of-range numbers
        - Empty input
    """
    while True:
        try:
            choice_input = input("Enter choice (1-6): ")
            choice = int(choice_input)
            if 1 <= choice <= 6:
                return choice
            print("Invalid choice. Please enter a number between 1-6.")
        except ValueError:
            print("Invalid choice. Please enter a number between 1-6.")


def main_loop() -> None:
    """Main application loop - displays menu and handles user choices.

    Runs until user selects Exit (Option 6).
    """
    print("=== Todo List Manager ===")
    print()

    try:
        while True:
            display_menu()
            choice = get_menu_choice()

            if choice == 1:
                handle_add_task()
            elif choice == 2:
                handle_view_tasks()
            elif choice == 3:
                handle_update_task()
            elif choice == 4:
                handle_delete_task()
            elif choice == 5:
                handle_mark_complete()
            elif choice == 6:
                print("Goodbye! Note: All tasks will be lost (in-memory mode).")
                break
    except KeyboardInterrupt:
        print("\n\nGoodbye! Note: All tasks will be lost (in-memory mode).")


if __name__ == "__main__":
    main_loop()
