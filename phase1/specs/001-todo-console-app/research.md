# Research: Todo Console App - Phase 1

**Feature**: Todo Console App - Phase 1
**Date**: 2026-01-02
**Purpose**: Resolve technical questions and establish implementation patterns for console-based task manager

## Research Questions

### 1. Input Validation Strategy

**Question**: How to validate string length (1-200 chars for title, max 1000 for description) and handle edge cases (unicode, special characters)?

**Research Findings**:
- Python 3.13+ handles Unicode natively via UTF-8
- `len()` built-in counts characters (not bytes), correctly handles:
  - Multi-byte UTF-8 characters (Chinese, Arabic, etc.)
  - Emoji (counted as 1 character each)
  - Combining characters (may appear as multiple chars but count as separate)
- `str.strip()` removes leading/trailing whitespace for empty check
- No need for special character escaping in Python strings

**Decision**: Use `len()` for character count, `str.strip()` for empty check, accept all unicode

**Rationale**: Python 3.13 Unicode support is robust. Spec requires "no crashes" (FR-018), accepting all unicode aligns with this. Character count (not byte count) matches user expectations.

**Alternatives Considered**:
- Regex validation → Rejected: Unnecessary complexity, doesn't handle Unicode edge cases better
- Byte-length validation → Rejected: Confusing for users (emoji = 4 bytes but appears as 1 char)
- ASCII-only restriction → Rejected: Excludes international users unnecessarily

**Implementation Pattern**:
```python
def validate_title(title: str) -> tuple[bool, str]:
    title = title.strip()
    if not title:
        return (False, "Title cannot be empty. Please enter a title.")
    if len(title) > 200:
        return (False, "Title too long (max 200 characters). Please shorten.")
    return (True, "")
```

---

### 2. Timestamp Format

**Question**: How to generate ISO 8601 timestamps (YYYY-MM-DD HH:MM:SS) using `datetime` module?

**Research Findings**:
- `datetime.datetime.now()` returns current local time
- `.strftime("%Y-%m-%d %H:%M:%S")` formats to ISO 8601 (year-month-day hour:minute:second)
- Spec specifies "YYYY-MM-DD HH:MM:SS" format explicitly (FR-004)
- No timezone needed (local time sufficient for single-user app)

**Decision**: `datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")`

**Rationale**: Direct standard library support, matches spec requirements exactly, no external dependencies

**Alternatives Considered**:
- `datetime.datetime.now().isoformat()` → Rejected: Produces "YYYY-MM-DDTHH:MM:SS.microseconds" (different format)
- UTC time via `.utcnow()` → Rejected: Confusing for single-user local app
- Manual string formatting → Rejected: Error-prone, stdlib handles it

**Implementation Pattern**:
```python
from datetime import datetime

created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# Example output: "2026-01-02 14:35:22"
```

---

### 3. Console Symbol Compatibility

**Question**: How to ensure UTF-8 symbols (✓, ☐) display correctly across Windows/macOS/Linux terminals? Fallback strategy?

**Research Findings**:
- UTF-8 check mark: `\u2713` (✓)
- UTF-8 empty checkbox: `\u2610` (☐)
- Modern terminals (Windows Terminal, macOS Terminal, Linux GNOME/KDE) support UTF-8 by default
- Older Windows cmd.exe may show `?` or garbage characters
- Python `print()` raises UnicodeEncodeError if terminal encoding unsupported

**Decision**: Use UTF-8 symbols (`\u2713`, `\u2610`) with try/except fallback to ASCII (`[X]`, `[ ]`) if encoding error occurs

**Rationale**: Provides better UX for majority of users (modern terminals) while gracefully degrading for older systems. Aligns with Constitution Principle III (User-Friendly) and spec requirement FR-007.

**Alternatives Considered**:
- ASCII only (`[X]`, `[ ]`) → Rejected: Less visually appealing, all modern terminals support UTF-8
- UTF-8 only (no fallback) → Rejected: May crash on older Windows systems
- Detect terminal encoding preemptively → Rejected: Over-engineered for this use case

**Implementation Pattern**:
```python
def get_status_symbol(completed: bool) -> str:
    """Get status symbol with UTF-8/ASCII fallback."""
    try:
        return "\u2713" if completed else "\u2610"  # ✓ or ☐
    except UnicodeEncodeError:
        return "[X]" if completed else "[ ]"  # ASCII fallback
```

---

### 4. ID Generation

**Question**: How to implement auto-incrementing IDs that never reuse (even after deletion) using only in-memory state?

**Research Findings**:
- Module-level variables persist for program lifetime
- Counter pattern: increment after each creation, never decrement
- Deletion creates gaps in ID sequence (expected behavior per spec edge cases)
- Python integers have unlimited precision (no overflow risk)

**Decision**: Module-level counter variable `next_id` incremented after each task creation, never decremented

**Rationale**: Simplest implementation meeting spec requirement (FR-003: "never reusing IDs even after task deletion"). No database needed, aligns with Constitution Principle II (In-Memory Only).

**Alternatives Considered**:
- UUID generation → Rejected: Overly complex, non-sequential IDs confusing for users
- Reuse deleted IDs → Rejected: Violates spec requirement FR-003
- Track deleted IDs to avoid reuse → Rejected: Unnecessary complexity given unlimited integer range

**Implementation Pattern**:
```python
# Module-level storage
tasks: list[dict[str, Any]] = []
next_id: int = 1

def add_task(title: str, description: str = "") -> tuple[bool, int | None, str]:
    global next_id
    # ... validation ...

    task_id = next_id
    next_id += 1  # Increment for next task (never decrement)

    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "completed": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    tasks.append(task)
    return (True, task_id, f"Task #{task_id} created successfully!")
```

---

### 5. Error Handling Pattern

**Question**: Best practice for returning errors from business logic to UI layer (exceptions vs. return tuples)?

**Research Findings**:
- **Exceptions**:
  - Pros: Pythonic, clear error types, forces handling
  - Cons: Requires try/except in UI layer, adds complexity
- **Return tuples**:
  - Pros: Explicit success/failure, easier to test, no exception handling needed
  - Cons: Less Pythonic, requires tuple unpacking

For console app with simple validation errors (not exceptional conditions):
- Validation failures are expected user behavior (not exceptional)
- UI needs both success/failure status AND user-friendly message
- Constitution Principle I (Simplicity First) favors fewer control structures

**Decision**: Return tuples `(success: bool, data: Any, message: str)` from business logic to avoid exception handling complexity in UI layer

**Rationale**: Validation failures are expected user behavior (not exceptional conditions). Tuple pattern makes success/failure explicit in function signature and simplifies UI layer (no try/except needed). Aligns with Constitution Principle I (Simplicity First).

**Alternatives Considered**:
- Raise ValueError for validation errors → Rejected: Adds try/except complexity to every UI handler
- Return None for failures → Rejected: Loses error message, requires separate error handling
- Use Result/Either monad pattern → Rejected: Over-engineered for Python, requires external library or custom implementation

**Implementation Pattern**:
```python
# Business logic (todo.py)
def add_task(title: str, description: str = "") -> tuple[bool, int | None, str]:
    """Returns (success, task_id, message)."""
    valid, error_msg = validate_title(title)
    if not valid:
        return (False, None, error_msg)

    # ... create task ...
    return (True, task_id, f"Task #{task_id} created successfully!")

# UI layer (main.py)
def handle_add_task() -> None:
    title = get_title_input()
    description = get_description_input()

    success, task_id, message = todo.add_task(title, description)
    print(message)  # No try/except needed
```

---

## Technology Selection Summary

| Technology | Purpose | Decision | Rationale |
|------------|---------|----------|-----------|
| Python 3.13+ | Language/Runtime | Standard library only | Constitution requirement, zero setup friction |
| `datetime` module | Timestamp generation | `strftime("%Y-%m-%d %H:%M:%S")` | Matches spec format exactly |
| `typing` module | Type hints | `tuple`, `list`, `dict`, `Any`, `NoReturn` | Constitution requirement for type safety |
| Module-level vars | State management | `tasks = []`, `next_id = 1` | Simplest pattern for single-user in-memory app |
| Return tuples | Error handling | `(success, data, message)` | Explicit, simple, no exceptions for validation |
| UTF-8 symbols | UI display | `\u2713`/`\u2610` with ASCII fallback | Better UX with graceful degradation |

---

## Best Practices Applied

### 1. Input Validation
- Validate at business logic layer (not UI)
- Return specific error messages (not generic "invalid input")
- Accept all Unicode (no artificial restrictions)

### 2. Error Messages
- User-friendly language ("Title too long" not "ValidationError")
- Actionable guidance ("Please shorten" not just "invalid")
- Consistent format (all errors end with period)

### 3. State Management
- Module-level for simplicity (no class needed)
- Global keyword only where necessary (increment counter)
- Immutable IDs (never change after creation)

### 4. Code Organization
- Separation: todo.py (data/logic), main.py (UI)
- Single responsibility: one function = one purpose
- Type hints on all signatures for clarity

### 5. Terminal Compatibility
- Try UTF-8 first (better UX for 95% of users)
- Fallback to ASCII (compatibility for 5% edge cases)
- No manual encoding detection (let Python handle it)

---

## Open Questions & Assumptions

### Resolved
All technical questions from plan.md Phase 0 have been resolved with decisions above.

### Assumptions Made
1. **Terminal encoding**: Python 3.13+ handles UTF-8 by default on modern systems
2. **Character counting**: `len()` character count (not byte count) matches user expectations
3. **Timestamp timezone**: Local time sufficient for single-user app (no UTC needed)
4. **ID range**: Python unlimited integers mean no overflow concerns for this use case
5. **Error handling**: Validation failures are expected user behavior (not exceptions)

### Future Considerations (Out of Scope for Phase 1)
- Persistence (Phase 2): File I/O patterns, JSON serialization
- Testing (Phase 2): pytest patterns for validation functions
- Multi-user (Phase 3): Session management, concurrent access
- Advanced UI (Phase 3): Colors via `colorama`, progress bars, table formatting

---

## References

- Python 3.13 datetime documentation: https://docs.python.org/3/library/datetime.html
- Python 3.13 Unicode HOWTO: https://docs.python.org/3/howto/unicode.html
- PEP 8 Style Guide: https://peps.python.org/pep-0008/
- ISO 8601 timestamp format: https://en.wikipedia.org/wiki/ISO_8601

---

**Research Status**: ✅ COMPLETE - All technical questions resolved, ready for Phase 1 design
