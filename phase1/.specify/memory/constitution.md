# Todo Console App Constitution
<!-- Phase 1: Basic In-Memory Todo Manager -->

## Core Principles

### I. Simplicity First
Every design decision favors simplicity over complexity. This is a console-based todo app using only Python's standard library. No external dependencies, no frameworks, no persistence layer. The entire application fits in a single file and can be understood by reading from top to bottom.

**Rationale**: Hackathon constraints demand rapid development with zero setup friction. Pure Python means no dependency conflicts, instant portability, and focus on core logic rather than infrastructure.

### II. In-Memory Only
All data lives in memory during program execution. No file I/O, no databases, no caching layers. Data is lost when the program exits.

**Rationale**: Phase 1 focuses on CRUD operations and user interface flow. Persistence is explicitly out of scope. This constraint forces clean data modeling and prepares the architecture for future persistence layers without coupling to storage implementation details.

### III. User-Friendly Console Interface
Every interaction provides clear feedback. All menu options are numbered. All inputs are validated with helpful error messages. No cryptic failures, no silent errors, no ambiguous states.

**Rationale**: Console apps must compensate for lack of visual UI with exceptional clarity. Users should never be confused about what to do next or what went wrong.

### IV. Clean Architecture
Separation of concerns enforced at function level:
- **Data layer**: Task data structure and in-memory storage
- **Business logic**: CRUD operations (add, view, update, delete, mark complete)
- **UI layer**: Menu display, input handling, user feedback

**Rationale**: Even simple apps benefit from separation of concerns. This structure makes testing easier, supports future refactoring (e.g., adding persistence), and keeps each function focused on one responsibility.

### V. Robust Input Handling
Never crash on invalid input. Validate all user input before processing. Provide specific error messages that guide users toward valid input.

**Validation rules**:
- Task IDs must be positive integers that exist in the task list
- Titles required (1-200 characters)
- Descriptions optional (max 1000 characters)
- Menu choices must be valid numbered options

**Rationale**: Console apps are fragile by nature. Defensive input handling transforms potential crashes into opportunities for helpful guidance.

### VI. Type Safety and Documentation
- Type hints required on all function signatures
- Docstrings required for all functions using Google style
- Meaningful variable and function names (no abbreviations unless universally understood)

**Rationale**: Python 3.13+ with type hints enables static analysis and IDE support. Documentation serves future developers (including yourself tomorrow). Good naming is the best documentation.

## Code Quality Standards

### Python Standards
- **Version**: Python 3.13+ (verified via `python --version`)
- **Package Manager**: UV (no pip packages beyond UV defaults)
- **Style Guide**: PEP 8 compliance mandatory
- **Line Length**: 88 characters (Black default)
- **Imports**: Standard library only, grouped and sorted (stdlib, third-party, local)

### Naming Conventions
- **Functions/Variables**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Classes**: `PascalCase` (if needed in future phases)
- **Private helpers**: `_leading_underscore`

### Documentation Requirements
```python
def example_function(param1: str, param2: int) -> bool:
    """Short one-line summary.

    Longer description if needed (what it does, why it exists).

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When and why this is raised
    """
```

## Technical Constraints

### Storage Mechanism
Task data structure (in-memory list of dictionaries):
```python
{
    "id": int,              # Auto-incrementing, starts at 1
    "title": str,           # Required, 1-200 chars
    "description": str,     # Optional, max 1000 chars, empty string if not provided
    "completed": bool,      # Default False
    "created_at": str       # ISO 8601 timestamp (YYYY-MM-DD HH:MM:SS)
}
```

**Storage invariants**:
- Task IDs are unique and never reused (even after deletion)
- IDs increment sequentially starting from 1
- No gaps allowed during initial creation (gaps OK after deletion)
- Task list stored as module-level list variable

### Forbidden Operations
- ❌ File I/O (`open()`, `with`, `pathlib` writes)
- ❌ Database connections (SQLite, PostgreSQL, etc.)
- ❌ Web frameworks (Flask, FastAPI, Django)
- ❌ External dependencies beyond Python stdlib
- ❌ GUI libraries (tkinter, PyQt, etc.)
- ❌ Network operations
- ❌ Multithreading/multiprocessing

### Required Operations
- ✅ Console input/output (`input()`, `print()`)
- ✅ String formatting and validation
- ✅ List/dictionary manipulation
- ✅ Datetime handling (`datetime.datetime.now()`)
- ✅ Exception handling for user errors

## Feature Requirements

### Required Features (Phase 1)
All five CRUD operations must be implemented and fully functional:

1. **Add Task**
   - Prompt for title (required)
   - Prompt for description (optional, allow empty)
   - Auto-generate ID and timestamp
   - Default completed=False
   - Confirm task created with ID

2. **View Task List**
   - Display all tasks in readable format
   - Show: ID, Title, Status (✓/☐), Created Date
   - Handle empty list gracefully ("No tasks yet")
   - Consider truncating long titles for list view

3. **Update Task**
   - Prompt for task ID
   - Allow editing title and/or description
   - Validate task exists
   - Confirm update success

4. **Delete Task**
   - Prompt for task ID
   - Validate task exists
   - Remove from list
   - Confirm deletion

5. **Mark Complete/Incomplete**
   - Prompt for task ID
   - Toggle completed status
   - Validate task exists
   - Show new status

### User Interface Contract
**Main Menu** (infinite loop until exit):
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

**Input Validation**:
- Menu choice: Must be 1-6
- Task ID: Must be positive integer existing in list
- Title: Must be 1-200 characters
- Description: Max 1000 characters (empty allowed)

**Error Messages** (user-friendly examples):
- "Invalid choice. Please enter a number between 1-6."
- "Task ID 5 not found. Please try again."
- "Title cannot be empty. Please enter a title."
- "Title too long (max 200 characters). Please shorten."

**Success Messages**:
- "Task #3 created successfully!"
- "Task #3 updated successfully!"
- "Task #3 deleted successfully!"
- "Task #3 marked as complete!"

### Success Criteria
Phase 1 is considered complete when:
- ✅ All 5 CRUD features implemented and working
- ✅ No crashes on any invalid input
- ✅ Clear user feedback for every operation
- ✅ Code follows all standards above (PEP 8, type hints, docstrings)
- ✅ Task IDs are unique and auto-increment correctly
- ✅ Menu loop runs continuously until user chooses exit
- ✅ Code generated via spec-driven development workflow
- ✅ Manual testing confirms all features work as expected

## Development Workflow

### Spec-Driven Development Process
1. **Specification** (`/sp.specify`): Define feature requirements in `specs/<feature>/spec.md`
2. **Planning** (`/sp.plan`): Create architecture plan in `specs/<feature>/plan.md`
3. **Task Breakdown** (`/sp.tasks`): Generate testable tasks in `specs/<feature>/tasks.md`
4. **Implementation** (`/sp.implement`): Execute tasks following TDD where applicable
5. **Documentation**: PHR created automatically for each step

### Quality Gates
- All code must pass PEP 8 style checks
- All functions must have type hints and docstrings
- All features must be manually tested
- No crashes on invalid input
- All edge cases handled gracefully

### Testing Strategy (Phase 1)
- **Manual testing required** for all features
- Test cases must cover:
  - Valid inputs (happy path)
  - Invalid inputs (error handling)
  - Edge cases (empty list, nonexistent IDs, boundary values)
- Automated testing out of scope for Phase 1

## Governance

### Constitution Authority
This constitution supersedes all other development practices for the Todo Console App project. All code, design decisions, and features must comply with these principles and constraints.

### Amendment Process
Constitution changes require:
1. Clear rationale for the change
2. Impact analysis on existing code
3. Migration plan if existing code affected
4. Documentation in ADR if architecturally significant

### Compliance Verification
Every commit must verify:
- No external dependencies added
- No file I/O operations introduced
- PEP 8 compliance maintained
- All functions have type hints and docstrings
- Input validation present for all user inputs

### Phase Transition Rules
When moving to Phase 2 (persistence, advanced features):
- Core principles (Simplicity, Clean Architecture) remain
- Technical constraints will be relaxed (file I/O allowed)
- New ADRs required for storage mechanism, data migration
- Backward compatibility not required (Phase 1 is throwaway prototype)

**Version**: 1.0.0 | **Ratified**: 2026-01-02 | **Last Amended**: 2026-01-02
