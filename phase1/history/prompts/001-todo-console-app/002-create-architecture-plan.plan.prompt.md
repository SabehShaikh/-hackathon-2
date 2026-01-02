---
id: 002
title: Create Architecture Plan
stage: plan
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-todo-console-app
branch: 001-todo-console-app
user: developer
command: /sp.plan
labels: ["planning", "architecture", "design", "3-layer", "console-app"]
links:
  spec: specs/001-todo-console-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-todo-console-app/plan.md
 - specs/001-todo-console-app/research.md
 - specs/001-todo-console-app/data-model.md
 - specs/001-todo-console-app/quickstart.md
tests:
 - Constitution Check validation (all 6 principles PASS pre and post design)
---

## Prompt

/sp.plan

Reflect on: Constitution and Specification from previous steps

Architecture: 3-layer design
1. Data Layer - In-memory task storage (list of dicts)
2. Business Logic - CRUD operations with validation
3. UI Layer - Console menu and display

File Structure:
src/
├── main.py      # UI layer, menu loop (~200 lines)
└── todo.py      # Data + business logic (~250 lines)

Key Components:

todo.py:
- tasks = [] (global list storing task dicts)
- next_id = 1 (counter for auto-increment IDs)
- add_task(title, desc) → returns (success, task_id, message)
- get_all_tasks() → returns tasks list
- update_task(id, title, desc) → returns (success, message)
- delete_task(id) → returns (success, message)
- toggle_complete(id) → returns (success, new_status, message)
- validate_id(id) → checks if task exists

main.py:
- display_menu() → prints 6 numbered options
- display_tasks(tasks) → formats task list with ✓/✗ status
- main_loop() → menu cycle until exit
- Handle all user input with try/except
- Call todo.py functions, display results

Design Decisions:
1. List of dicts (not classes) - stdlib only per Constitution
2. Auto-increment IDs starting at 1 - simple for console
3. Return tuples (success, data, message) - explicit errors
4. Validate in business logic, display in UI - clean separation

Testing Strategy (Manual):
- Test each CRUD operation with valid/invalid inputs
- Verify error messages (no stack traces)
- Check edge cases: empty title, invalid ID, long input
- Confirm menu navigation (1-6, invalid choices)

Quality Checks:
- Under 500 lines total
- Type hints on all functions
- No external dependencies
- PEP 8 compliant

Implementation Order:
1. Build todo.py data layer first
2. Add business logic functions
3. Create main.py UI layer
4. Wire menu loop
5. Test manually

Risk Mitigation:
- Invalid input → try/except blocks
- Long task lists → acceptable for Phase 1
- ID conflicts → counter resets each run (expected)

## Response snapshot

Created comprehensive architecture plan for Todo Console App Phase 1 with complete design artifacts:

**Plan Document** (`specs/001-todo-console-app/plan.md` - 702 lines):

1. **Summary & Technical Context**:
   - 3-layer architecture (Data, Business Logic, UI)
   - Python 3.13+ stdlib only, 2-file structure
   - In-memory storage, manual testing, <500 lines

2. **Constitution Check** (Pre-Design): ✅ ALL 6 PRINCIPLES PASS
   - Simplicity First, In-Memory Only, User-Friendly Interface
   - Clean Architecture, Robust Input Handling, Type Safety

3. **Project Structure**:
   - Documentation: plan.md, research.md, data-model.md, quickstart.md
   - Source: src/main.py (UI), src/todo.py (data/logic)
   - Decision: 2-file split for clean separation, <500 lines total

4. **Phase 0: Research** (5 questions resolved):
   - Input validation strategy (len(), strip(), unicode support)
   - Timestamp format (strftime ISO 8601)
   - Console symbols (UTF-8 with ASCII fallback)
   - ID generation (module-level counter, never reuse)
   - Error handling (return tuples vs exceptions)

5. **Phase 1: Design & Contracts**:
   - **Data Model**: Task entity (5 attributes), Task List (in-memory), ID Counter
   - **Function Contracts**:
     - todo.py: 9 functions (add_task, get_all_tasks, get_task_by_id, update_task, delete_task, toggle_complete, validate_title, validate_description)
     - main.py: 11 functions (display_menu, display_tasks, 5 handlers, 4 input helpers, main_loop)
   - **Validation Rules**: Title (1-200 chars), Description (max 1000 chars), ID existence
   - **State Transitions**: Created → Incomplete ↔ Complete → Deleted

6. **Constitution Re-Check** (Post-Design): ✅ ALL 6 PRINCIPLES PASS
   - No changes from initial check, design maintains compliance

7. **Design Decisions & Rationale** (5 key decisions):
   - Return tuples (not exceptions) - simpler UI layer
   - Separate validation functions - reusable, testable
   - Module-level storage (not class) - simplicity first
   - UTF-8 with ASCII fallback - better UX, graceful degradation
   - Two-file structure (not one) - clean architecture

8. **Risk Analysis** (5 risks with mitigations):
   - UTF-8 encoding on Windows, validation edge cases, ID overflow, input loops, code size

9. **Metrics & Success Criteria**: Maps all 10 spec criteria to implementation metrics

10. **Appendices**: Function call flows, error messages, type hints

**Research Document** (`specs/001-todo-console-app/research.md`):
- 5 research questions with findings, decisions, rationale, alternatives
- Technology selection summary table
- Best practices for validation, errors, state, organization, compatibility
- Implementation patterns with code examples

**Data Model Document** (`specs/001-todo-console-app/data-model.md`):
- Task entity definition with 5 attributes, constraints, validation
- Task List collection (in-memory list)
- ID Counter (auto-increment, never reuse)
- Validation rules (title, description, ID) with error messages
- State transitions diagram and lifecycle
- Data access patterns (CRUD with complexity analysis)
- Storage implementation structure
- Example data flows

**Quickstart Guide** (`specs/001-todo-console-app/quickstart.md`):
- Prerequisites and verification steps
- Implementation steps (todo.py, main.py)
- Running instructions (UV, direct Python)
- 5 test suites (36 total tests):
  - Basic CRUD (7 tests)
  - Input validation (8 tests)
  - Edge cases (8 tests)
  - Menu navigation (4 tests)
  - Success criteria validation (10 tests)
- Code quality checks (PEP 8, type hints, line count)
- Troubleshooting guide
- Complete test session example

**Agent Context Updated**:
- Added Python 3.13+ language
- Added Python stdlib framework (`datetime`, `typing`)
- Added in-memory storage database

## Outcome

- ✅ Impact: Complete architecture plan with 4 detailed design documents (plan, research, data-model, quickstart) totaling ~1500 lines of design documentation, 20 function contracts, 5 design decisions, 36 test cases
- 🧪 Tests: Constitution Check PASS (all 6 principles pre and post design), no violations
- 📁 Files: Created plan.md (702 lines), research.md, data-model.md, quickstart.md; updated CLAUDE.md
- 🔁 Next prompts: /sp.tasks to generate implementation tasks from this plan
- 🧠 Reflection: Architecture design complete and constitutionally compliant. 3-layer separation (data/logic/UI) clear, return tuple pattern simplifies error handling, module-level storage aligns with simplicity principle. Ready for task generation.

## Evaluation notes (flywheel)

- Failure modes observed: None - planning workflow completed successfully with full compliance
- Graders run and results (PASS/FAIL): Constitution Check PASS (pre-design 6/6, post-design 6/6), no violations justified
- Prompt variant (if applicable): Standard architecture planning with research, data modeling, and quickstart generation
- Next experiment (smallest change to try): Proceed to /sp.tasks for implementation task breakdown, prioritize P1 stories (Add/View, Menu) for MVP
