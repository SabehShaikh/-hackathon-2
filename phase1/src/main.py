"""Todo UI layer - menu display, user input handling, and output formatting."""

import todo
from typing import Any
import sys
import io

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def display_banner() -> None:
    """Display application banner."""
    try:
        banner = """
┌─────────────────────────────────────────────────┐
│                                                 │
│        📝  TODO LIST MANAGER  📝                │
│                                                 │
│     Organize your tasks with simplicity         │
│                                                 │
└─────────────────────────────────────────────────┘
"""
        print(banner)
    except UnicodeEncodeError:
        # ASCII fallback
        banner = """
+-------------------------------------------------+
|                                                 |
|          TODO LIST MANAGER                      |
|                                                 |
|     Organize your tasks with simplicity         |
|                                                 |
+-------------------------------------------------+
"""
        print(banner)


def display_menu() -> None:
    """Display the main menu with 6 numbered options."""
    try:
        print("┌─────────────────────────────────────────────────┐")
        print("│                   MAIN MENU                     │")
        print("├─────────────────────────────────────────────────┤")
        print("│  1. ➕ Add Task                                 │")
        print("│  2. 📋 View All Tasks                           │")
        print("│  3. ✏️  Update Task                              │")
        print("│  4. 🗑️  Delete Task                              │")
        print("│  5. ✅ Mark Complete/Incomplete                  │")
        print("│  6. 🚪 Exit                                      │")
        print("└─────────────────────────────────────────────────┘")
    except UnicodeEncodeError:
        # ASCII fallback
        print("+-------------------------------------------------+")
        print("|                   MAIN MENU                     |")
        print("+-------------------------------------------------+")
        print("|  1. Add Task                                    |")
        print("|  2. View All Tasks                              |")
        print("|  3. Update Task                                 |")
        print("|  4. Delete Task                                 |")
        print("|  5. Mark Complete/Incomplete                    |")
        print("|  6. Exit                                        |")
        print("+-------------------------------------------------+")
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
    try:
        if not tasks:
            print("┌─────────────────────────────────────────────────┐")
            print("│             No tasks found                      │")
            print("└─────────────────────────────────────────────────┘")
            return

        print("┌─────────────────────────────────────────────────┐")
        print("│                  YOUR TASKS                     │")
        print("└─────────────────────────────────────────────────┘")
        print()

        for i, task in enumerate(tasks):
            # UTF-8 symbols
            status_symbol = "✓" if task["completed"] else "☐"

            # Task header with border
            print(f"┌─ Task #{task['id']} ─────────────────────────────────────")
            print(f"│ {status_symbol} {task['title']}")
            if task["description"]:
                print(f"│   └─ {task['description']}")
            print(f"│   📅 Created: {task['created_at']}")
            print(f"└─────────────────────────────────────────────────")

            # Add spacing between tasks, but not after the last one
            if i < len(tasks) - 1:
                print()
    except UnicodeEncodeError:
        # ASCII fallback for entire display
        if not tasks:
            print("+-------------------------------------------------+")
            print("|             No tasks found                      |")
            print("+-------------------------------------------------+")
            return

        print("+-------------------------------------------------+")
        print("|                  YOUR TASKS                     |")
        print("+-------------------------------------------------+")
        print()

        for i, task in enumerate(tasks):
            status_symbol = "[X]" if task["completed"] else "[ ]"
            print(f"+-- Task #{task['id']} ---------------------------------")
            print(f"| {status_symbol} {task['title']}")
            if task["description"]:
                print(f"|   +- {task['description']}")
            print(f"|   Created: {task['created_at']}")
            print(f"+-----------------------------------------------")

            if i < len(tasks) - 1:
                print()


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
    try:
        print("\n┌─────────────────────────────────────────────────┐")
        print("│              ➕ ADD NEW TASK                     │")
        print("└─────────────────────────────────────────────────┘\n")
    except UnicodeEncodeError:
        print("\n+-------------------------------------------------+")
        print("|              ADD NEW TASK                       |")
        print("+-------------------------------------------------+\n")

    title = get_title_input()
    description = get_description_input()
    success, task_id, message = todo.add_task(title, description)

    try:
        print("\n" + "─" * 50)
        print(f"✨ {message}")
        print("─" * 50 + "\n")
    except UnicodeEncodeError:
        print("\n" + "-" * 50)
        print(f"* {message}")
        print("-" * 50 + "\n")


def handle_view_tasks() -> None:
    """Handle View All Tasks menu option (Option 2)."""
    print()
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
    try:
        print("\n┌─────────────────────────────────────────────────┐")
        print("│              ✏️  UPDATE TASK                     │")
        print("└─────────────────────────────────────────────────┘\n")
    except UnicodeEncodeError:
        print("\n+-------------------------------------------------+")
        print("|              UPDATE TASK                        |")
        print("+-------------------------------------------------+\n")

    task_id = get_task_id()
    try:
        print("\n💡 Tip: Leave blank to keep existing value\n")
    except UnicodeEncodeError:
        print("\nTip: Leave blank to keep existing value\n")

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

    try:
        print("\n" + "─" * 50)
        print(f"✨ {message}")
        print("─" * 50 + "\n")
    except UnicodeEncodeError:
        print("\n" + "-" * 50)
        print(f"* {message}")
        print("-" * 50 + "\n")


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
    try:
        print("\n┌─────────────────────────────────────────────────┐")
        print("│              🗑️  DELETE TASK                     │")
        print("└─────────────────────────────────────────────────┘\n")
    except UnicodeEncodeError:
        print("\n+-------------------------------------------------+")
        print("|              DELETE TASK                        |")
        print("+-------------------------------------------------+\n")

    task_id = get_task_id()

    try:
        confirmed = get_yes_no_confirmation("\n⚠️  Are you sure you want to delete this task?")
        if not confirmed:
            print("\n❌ Deletion cancelled")
            print()
            return
    except UnicodeEncodeError:
        confirmed = get_yes_no_confirmation("\nAre you sure you want to delete this task?")
        if not confirmed:
            print("\nDeletion cancelled")
            print()
            return

    success, message = todo.delete_task(task_id)

    try:
        print("\n" + "─" * 50)
        print(f"✨ {message}")
        print("─" * 50 + "\n")
    except UnicodeEncodeError:
        print("\n" + "-" * 50)
        print(f"* {message}")
        print("-" * 50 + "\n")


def handle_mark_complete() -> None:
    """Handle Mark Complete/Incomplete menu option (Option 5)."""
    try:
        print("\n┌─────────────────────────────────────────────────┐")
        print("│         ✅ TOGGLE TASK COMPLETION               │")
        print("└─────────────────────────────────────────────────┘\n")
    except UnicodeEncodeError:
        print("\n+-------------------------------------------------+")
        print("|         TOGGLE TASK COMPLETION                  |")
        print("+-------------------------------------------------+\n")

    task_id = get_task_id()
    success, new_status, message = todo.toggle_complete(task_id)

    try:
        print("\n" + "─" * 50)
        print(f"✨ {message}")
        print("─" * 50 + "\n")
    except UnicodeEncodeError:
        print("\n" + "-" * 50)
        print(f"* {message}")
        print("-" * 50 + "\n")


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
    display_banner()

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
                try:
                    print("\n┌─────────────────────────────────────────────────┐")
                    print("│                  GOODBYE! 👋                     │")
                    print("│                                                 │")
                    print("│   ⚠️  Note: All tasks will be lost              │")
                    print("│       (in-memory mode)                          │")
                    print("│                                                 │")
                    print("└─────────────────────────────────────────────────┘\n")
                except UnicodeEncodeError:
                    print("\n+-------------------------------------------------+")
                    print("|                  GOODBYE!                       |")
                    print("|                                                 |")
                    print("|   Note: All tasks will be lost                  |")
                    print("|       (in-memory mode)                          |")
                    print("|                                                 |")
                    print("+-------------------------------------------------+\n")
                break
    except KeyboardInterrupt:
        try:
            print("\n\n┌─────────────────────────────────────────────────┐")
            print("│                  GOODBYE! 👋                     │")
            print("│                                                 │")
            print("│   ⚠️  Note: All tasks will be lost              │")
            print("│       (in-memory mode)                          │")
            print("│                                                 │")
            print("└─────────────────────────────────────────────────┘\n")
        except UnicodeEncodeError:
            print("\n\n+-------------------------------------------------+")
            print("|                  GOODBYE!                       |")
            print("|                                                 |")
            print("|   Note: All tasks will be lost                  |")
            print("|       (in-memory mode)                          |")
            print("|                                                 |")
            print("+-------------------------------------------------+\n")


if __name__ == "__main__":
    main_loop()
