# Tasks: Todo AI Chatbot with Natural Language Interface

**Input**: Design documents from `/specs/002-ai-chat-interface/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/, research.md, quickstart.md

**Tests**: Not explicitly requested in specification - no test tasks generated

**Organization**: Tasks grouped by user story to enable independent implementation and testing of each story

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, etc.)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/`, `frontend/` at phase3/ root
- All paths relative to phase3/ directory

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create phase3/backend/ directory structure (main.py, routes/, migrations/)
- [x] T002 Copy entire Phase 2 frontend to phase3/frontend/ (cp -r ../phase2/frontend/* frontend/, exclude node_modules and .next)
- [x] T003 [P] Create backend/requirements.txt with dependencies: fastapi==0.115.0, uvicorn[standard]==0.32.0, sqlmodel==0.0.22, psycopg2-binary==2.9.9, python-jose[cryptography]==3.3.0, openai==1.58.1, mcp==1.0.0, python-dotenv==1.0.0, passlib[bcrypt]==1.7.4, alembic==1.13.1
- [x] T004 [P] Create backend/.env.example with DATABASE_URL, BETTER_AUTH_SECRET, GROK_API_KEY, ALLOWED_ORIGINS
- [x] T005 [P] Add @ai-sdk/react to frontend/package.json dependencies (chat UI)
- [x] T006 [P] Update frontend/.env.local with NEXT_PUBLIC_API_URL pointing to Phase 3 backend
- [x] T007 [P] Create backend/Dockerfile for HuggingFace Spaces (Python 3.11-slim, port 7860)
- [x] T008 [P] Create phase3/.gitignore (*.env, venv/, node_modules/, __pycache__/, dist/, .next/)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T009 Copy Phase 2 database.py pattern to backend/database.py (SQLModel engine, get_session function)
- [x] T010 [P] Copy Phase 2 auth.py pattern to backend/auth.py (JWT verification, verify_token dependency)
- [x] T011 Copy Phase 2 User model from ../phase2/backend/models.py to backend/models.py
- [x] T012 [P] Copy Phase 2 Task model from ../phase2/backend/models.py to backend/models.py
- [x] T013 Add Conversation model to backend/models.py (id, user_id, created_at, updated_at)
- [x] T014 [P] Add Message model to backend/models.py (id, conversation_id, user_id, role, content, created_at)
- [ ] T015 Initialize Alembic in backend/migrations/ (alembic init migrations)
- [ ] T016 Configure Alembic env.py to use SQLModel metadata from backend/models.py
- [ ] T017 Generate Alembic migration for conversations and messages tables (alembic revision --autogenerate -m "Add conversations and messages")
- [ ] T018 Review generated migration in backend/migrations/versions/001_*.py and verify Phase 2 tables untouched
- [ ] T019 Apply database migration to Neon PostgreSQL (alembic upgrade head)
- [ ] T020 Verify Phase 2 tables (users, tasks) exist and unchanged via psql
- [x] T021 [P] Create backend/main.py with FastAPI app initialization and CORS configuration
- [x] T022 [P] Create backend/routes/__init__.py
- [x] T023 [P] Copy Phase 2 auth routes to backend/routes/auth.py (signup, login endpoints)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Task via Natural Language (Priority: P1) 🎯 MVP

**Goal**: Enable users to create tasks by typing natural commands (e.g., "Add buy groceries")

**Independent Test**: User types "Add buy groceries", receives "✅ Added task: Buy groceries", task appears in database with correct user_id

### Implementation for User Story 1

- [x] T024 [P] [US1] Query Context 7 MCP Server for Official MCP SDK tool definition syntax and document in implementation notes
- [x] T025 [US1] Create backend/mcp_server.py with MCP Server initialization following mcp-tool-pattern skill
- [x] T026 [US1] Implement add_task tool in backend/mcp_server.py (user_id, title, description parameters, returns {"status", "data", "message"})
- [x] T027 [US1] Add database session handling in add_task tool (create Task record, commit, return task_id and title)
- [x] T028 [US1] Add error handling in add_task tool (empty title validation, database errors, return error status)
- [ ] T029 [US1] Test add_task tool independently with direct function call (verify task created in database)

**Checkpoint**: At this point, User Story 1 add_task tool should be fully functional and testable independently

---

## Phase 4: User Story 2 - View Tasks via Natural Language (Priority: P1)

**Goal**: Enable users to see their task list by asking "What's on my list?"

**Independent Test**: User types "What's on my list?", receives formatted list of all tasks with IDs and completion status

### Implementation for User Story 2

- [x] T030 [P] [US2] Implement list_tasks tool in backend/mcp_server.py (user_id, status="all"|"pending"|"completed" parameters)
- [x] T031 [US2] Add database query in list_tasks tool (filter by user_id and optionally by completed status)
- [x] T032 [US2] Format list_tasks response (return array of {id, title, description, completed}, include message with count)
- [x] T033 [US2] Add error handling in list_tasks tool (database errors, empty list handling with friendly message)
- [ ] T034 [US2] Test list_tasks tool independently (verify filtered results, empty list message)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently (add + list)

---

## Phase 5: User Story 6 - AI Confirmation and Friendly Communication (Priority: P1)

**Goal**: Ensure AI provides clear confirmations and helpful responses for all operations

**Independent Test**: User performs any task operation and receives conversational confirmation with relevant details

### Implementation for User Story 6

- [x] T035 [P] [US6] Query Context 7 for OpenAI SDK + Grok API configuration patterns and document in implementation notes
- [x] T036 [US6] Create backend/agent.py with OpenAI client configured for Grok API (base_url="https://api.x.ai/v1")
- [x] T037 [US6] Configure agent system instructions in backend/agent.py ("You are a helpful task management assistant...always confirm actions with friendly messages")
- [x] T038 [US6] Register add_task and list_tasks tools with agent in backend/agent.py
- [ ] T039 [US6] Test agent intent recognition for add commands ("add task", "remind me", "I need to") mapping to add_task tool
- [ ] T040 [US6] Test agent intent recognition for list commands ("show tasks", "what's on my list", "list") mapping to list_tasks tool
- [ ] T041 [US6] Test agent response formatting (includes ✅ emoji for success, friendly confirmations)

**Checkpoint**: Agent understands P1 commands (add, list) and responds with friendly confirmations

---

## Phase 6: User Story 7 - Conversation History Persistence (Priority: P2)

**Goal**: Enable conversation persistence across sessions so users can resume where they left off

**Independent Test**: User adds tasks in conversation, closes app, reopens app, previous conversation visible

### Implementation for User Story 7

- [x] T042 [P] [US7] Create backend/routes/chat.py with POST /api/chat endpoint
- [x] T043 [US7] Add JWT authentication to chat endpoint (user_id = Depends(verify_token))
- [x] T044 [US7] Implement conversation creation logic (if no conversation_id, create new Conversation record)
- [x] T045 [US7] Implement conversation retrieval logic (if conversation_id provided, fetch from database and verify user_id matches)
- [x] T046 [US7] Load message history from database (query Message table by conversation_id, order by created_at)
- [x] T047 [US7] Store user message in messages table (role="user", content=request.message)
- [x] T048 [US7] Call agent with message history + new message (pass conversation context to agent.run())
- [x] T049 [US7] Store agent response in messages table (role="assistant", content=agent response)
- [x] T050 [US7] Update conversation.updated_at timestamp after new messages
- [x] T051 [US7] Return response JSON (conversation_id, response text, tool_calls array)
- [ ] T052 [US7] Test chat endpoint with curl (verify conversation persists across multiple requests)

**Checkpoint**: Conversation history persists in database, stateless server can restart without data loss

---

## Phase 7: User Story 3 - Complete Task via Natural Language (Priority: P2)

**Goal**: Enable users to mark tasks as done by typing "Mark task 1 as done"

**Independent Test**: User types "Mark task 1 as done", receives confirmation, task 1 marked completed in database

### Implementation for User Story 3

- [x] T053 [P] [US3] Implement complete_task tool in backend/mcp_server.py (user_id, task_id parameters)
- [x] T054 [US3] Add database update in complete_task tool (set completed=True, updated_at=now())
- [x] T055 [US3] Add authorization check in complete_task tool (verify task.user_id == user_id before updating)
- [x] T056 [US3] Add error handling in complete_task tool (task not found, task belongs to different user)
- [x] T057 [US3] Register complete_task tool with agent in backend/agent.py
- [ ] T058 [US3] Test agent intent recognition for complete commands ("mark done", "completed", "finished")
- [ ] T059 [US3] Test complete_task tool (verify task updated, authorization enforced, error cases handled)

**Checkpoint**: Users can complete tasks via natural language, user data isolation enforced

---

## Phase 8: User Story 8 - Graceful Error Handling (Priority: P2)

**Goal**: Provide clear, non-technical error messages for all failure scenarios

**Independent Test**: Trigger error conditions (invalid task ID, database timeout, malformed input), each produces user-friendly message

### Implementation for User Story 8

- [x] T060 [P] [US8] Add try-except wrapper in all MCP tools (catch database errors, return error status)
- [ ] T061 [US8] Test agent error handling for non-existent task ("Complete task 999" → "I couldn't find task 999. Here's what you have...")
- [ ] T062 [US8] Test agent error handling for empty task list ("What's on my list?" with 0 tasks → "You don't have any tasks yet. Want to add one?")
- [x] T063 [US8] Add error handling in chat endpoint (try-except for database errors, agent errors, return 500 with friendly message)
- [ ] T064 [US8] Test authentication errors (expired JWT → 401 response with "Please log in again")
- [ ] T065 [US8] Test database connection errors (simulate timeout → "I'm having trouble connecting. Please try again in a moment.")

**Checkpoint**: All error scenarios produce user-friendly, actionable messages

---

## Phase 9: User Story 4 - Delete Task via Natural Language (Priority: P3)

**Goal**: Enable users to remove tasks by typing "Delete task 5"

**Independent Test**: User types "Delete task 5", receives confirmation, task 5 removed from database

### Implementation for User Story 4

- [x] T066 [P] [US4] Implement delete_task tool in backend/mcp_server.py (user_id, task_id parameters)
- [x] T067 [US4] Add database delete in delete_task tool (remove Task record by id and user_id)
- [x] T068 [US4] Add authorization check in delete_task tool (verify task belongs to user before deleting)
- [x] T069 [US4] Add error handling in delete_task tool (task not found, task belongs to different user)
- [x] T070 [US4] Register delete_task tool with agent in backend/agent.py
- [ ] T071 [US4] Test agent intent recognition for delete commands ("delete", "remove", "cancel")
- [ ] T072 [US4] Test delete_task tool (verify task removed, authorization enforced, error cases)

**Checkpoint**: Users can delete tasks via natural language with proper authorization

---

## Phase 10: User Story 5 - Update Task via Natural Language (Priority: P3)

**Goal**: Enable users to modify task details by typing "Change task 2 to 'Call mom tonight'"

**Independent Test**: User types "Change task 2 to 'Call mom tonight'", receives confirmation, task 2 title updated in database

### Implementation for User Story 5

- [x] T073 [P] [US5] Implement update_task tool in backend/mcp_server.py (user_id, task_id, title, description parameters)
- [x] T074 [US5] Add database update in update_task tool (update title and/or description, set updated_at=now())
- [x] T075 [US5] Add validation in update_task tool (at least one field must be provided)
- [x] T076 [US5] Add authorization check in update_task tool (verify task belongs to user)
- [x] T077 [US5] Add error handling in update_task tool (task not found, no fields provided, task belongs to different user)
- [x] T078 [US5] Register update_task tool with agent in backend/agent.py
- [ ] T079 [US5] Test agent intent recognition for update commands ("change", "update", "modify", "rename")
- [ ] T080 [US5] Test update_task tool (verify task updated, validation works, authorization enforced)

**Checkpoint**: All 5 MCP tools complete, agent handles full CRUD lifecycle

---

## Phase 11: Frontend Implementation (Add Chat to Phase 2 Next.js App)

**Purpose**: Add ChatKit as new /chat route while preserving all Phase 2 functionality

**Note**: Phase 2 frontend was copied in T002. These tasks ADD to it, not replace it.

### 11.1 Chat Types and API Client

- [x] T081 [P] Query Context 7 for OpenAI ChatKit configuration with Next.js and integration patterns
- [x] T082 [P] Add chat types to frontend/lib/types.ts (ChatMessage, Conversation, ChatRequest, ChatResponse)
- [x] T083 Add sendChatMessage function to frontend/lib/api.ts (POST /api/chat with JWT token, conversation_id)

### 11.2 Chat Component

- [x] T084 Create frontend/components/chat/ChatInterface.tsx wrapper component for ChatKit
- [x] T085 Configure ChatInterface to use custom API endpoint (lib/api.ts sendChatMessage)
- [x] T086 Add conversation_id state management in ChatInterface (localStorage for persistence)
- [x] T087 Add "New Conversation" button in ChatInterface (clears conversation_id)
- [x] T088 Add loading indicator in ChatInterface during API calls
- [x] T089 Add error handling in ChatInterface (display user-friendly error messages)

### 11.3 Chat Page Route

- [x] T090 Create frontend/app/chat/page.tsx that renders ChatInterface component
- [x] T091 Add auth protection to chat page (redirect to login if not authenticated)
- [x] T092 Style chat page to match Phase 2 design (consistent with dashboard)

### 11.4 Navigation Update

- [x] T093 Update frontend/components/Navbar.tsx to add "AI Chat" link to /chat route
- [x] T094 Add active state styling for AI Chat nav link (highlight when on /chat page)

### 11.5 Integration Testing

- [ ] T095 Test Phase 2 login/signup still works (no regressions)
- [ ] T096 Test Phase 2 dashboard task UI still works (add, edit, delete, complete via buttons)
- [ ] T097 Test new /chat page loads and ChatKit renders
- [ ] T098 Test chat message flow (type message → API call → response displayed)
- [ ] T099 Test conversation persistence (refresh page, history restored)
- [ ] T100 Test navigation between dashboard and chat (both accessible, state preserved)

**Checkpoint**: Both Phase 2 UI and Phase 3 Chat UI functional, users can manage tasks both ways

---

## Phase 12: Deployment Preparation

**Purpose**: Prepare applications for production deployment

- [ ] T101 [P] Test backend locally (uvicorn main:app --reload, verify all endpoints work)
- [ ] T102 [P] Test end-to-end flow locally (frontend → backend → database → agent → response)
- [ ] T103 [P] Verify Phase 2 tables and functionality unchanged (connect to database, check tasks table)
- [ ] T104 Verify backend Dockerfile has migration step in CMD (alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 7860)
- [ ] T105 Test Docker build locally (docker build -t todo-ai-backend ., docker run -p 7860:7860)
- [ ] T106 [P] Create deployment documentation in specs/002-ai-chat-interface/DEPLOY.md (HuggingFace + Vercel steps)
- [ ] T107 [P] Update specs/002-ai-chat-interface/quickstart.md with any implementation-specific notes

---

## Phase 13: Production Deployment

**Purpose**: Deploy backend and frontend to production environments

- [ ] T108 Push backend/ to HuggingFace Spaces repository
- [ ] T109 Configure HuggingFace Space environment variables (DATABASE_URL, BETTER_AUTH_SECRET, GROK_API_KEY, ALLOWED_ORIGINS)
- [ ] T110 Wait for HuggingFace Space build and verify deployment (check logs, test /docs endpoint)
- [ ] T111 [P] Push frontend/ to GitHub for Vercel deployment
- [ ] T112 Import GitHub repository to Vercel (set root directory to phase3/frontend/)
- [ ] T113 Configure Vercel environment variables (NEXT_PUBLIC_API_URL=HuggingFace URL)
- [ ] T114 Deploy frontend to Vercel and copy production URL
- [ ] T115 Update ALLOWED_ORIGINS in HuggingFace Space to include Vercel production URL
- [ ] T116 Restart HuggingFace Space to apply CORS changes

**Checkpoint**: Backend and frontend deployed to production, CORS configured

---

## Phase 14: Production Validation

**Purpose**: Verify all functionality works in production environment

### 14.1 Phase 2 UI Validation (No Regressions)

- [ ] T117 Test login/signup in production (Phase 2 auth flow works)
- [ ] T118 Test dashboard task UI in production (add task via button, verify in database)
- [ ] T119 Test dashboard edit/delete/complete buttons (Phase 2 CRUD fully operational)

### 14.2 Phase 3 Chat UI Validation

- [ ] T120 Test User Story 1 in production (add task via chat, verify in database)
- [ ] T121 Test User Story 2 in production (list tasks via chat)
- [ ] T122 Test User Story 3 in production (complete task via chat)
- [ ] T123 Test User Story 4 in production (delete task via chat)
- [ ] T124 Test User Story 5 in production (update task via chat)
- [ ] T125 Test User Story 6 in production (verify friendly AI confirmations)
- [ ] T126 Test User Story 7 in production (conversation persistence: close/reopen browser)
- [ ] T127 Test User Story 8 in production (trigger error: "Complete task 999", verify friendly error)

### 14.3 Cross-UI Validation

- [ ] T128 Add task via dashboard button, verify appears in chat list command
- [ ] T129 Add task via chat, verify appears in dashboard UI
- [ ] T130 Test navigation between /dashboard and /chat (smooth transitions)

### 14.4 Monitoring

- [ ] T131 [P] Monitor HuggingFace logs for errors or warnings
- [ ] T132 [P] Monitor Vercel logs for frontend errors
- [ ] T133 Test performance (verify < 3s chat response time)

**Checkpoint**: All user stories validated, both UIs work together, Phase 2 functionality preserved

---

## Phase 15: Documentation & Polish

**Purpose**: Complete documentation and final cleanup

- [ ] T134 [P] Update phase3/README.md with project overview, setup instructions, environment variables
- [ ] T135 [P] Document all 5 MCP tools in backend/mcp_server.py with docstrings
- [ ] T136 [P] Add code comments in backend/agent.py explaining Grok API configuration
- [ ] T137 [P] Add code comments in backend/routes/chat.py explaining stateless conversation flow
- [ ] T138 [P] Create specs/002-ai-chat-interface/TESTING.md with manual test scenarios for all 8 user stories
- [ ] T139 Verify all design documents are up-to-date (spec.md, plan.md, data-model.md, quickstart.md)
- [ ] T140 [P] Create specs/002-ai-chat-interface/ARCHITECTURE.md with system diagrams and data flow
- [ ] T141 Run code linting/formatting on backend (black, flake8)
- [ ] T142 [P] Run code linting/formatting on frontend (eslint, prettier)
- [ ] T143 Final git commit with clean commit message

**Checkpoint**: All documentation complete, code clean, ready for demo

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
  - T002 (Copy Phase 2 frontend) must complete before any frontend tasks
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-10)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed) OR sequentially in priority order
  - Priority order: US1 (P1) → US2 (P1) → US6 (P1) → US7 (P2) → US3 (P2) → US8 (P2) → US4 (P3) → US5 (P3)
- **Frontend (Phase 11)**: Depends on T002 (Phase 2 frontend copied) + US1, US2, US6, US7 complete (chat functionality ready)
- **Deployment (Phases 12-14)**: Depends on all user stories complete + Phase 11 complete
- **Documentation (Phase 15)**: Depends on production validation complete

### User Story Dependencies

- **US1 (Add Task) - P1**: Can start after Foundational - No dependencies on other stories
- **US2 (List Tasks) - P1**: Can start after Foundational - Independent of US1 (parallel)
- **US6 (AI Confirmations) - P1**: Depends on US1, US2 (agent needs tools to confirm)
- **US7 (Conversation Persistence) - P2**: Depends on US1, US2, US6 (basic chat working)
- **US3 (Complete Task) - P2**: Can start after Foundational - Independent (parallel with US1, US2)
- **US8 (Error Handling) - P2**: Depends on US1, US2, US3 (tools exist to test errors)
- **US4 (Delete Task) - P3**: Can start after Foundational - Independent (parallel with other tools)
- **US5 (Update Task) - P3**: Can start after Foundational - Independent (parallel with other tools)

### Within Each User Story

- MCP tool implementation before agent registration
- Agent registration before end-to-end testing
- Database operations before error handling
- Independent tool testing before integration

### Parallel Opportunities

**Phase 1 (Setup)**: T003, T004, T005, T006, T007, T008 can all run in parallel (after T002)
**Phase 2 (Foundational)**: T010, T012, T014, T021, T022, T023 can run in parallel within phase
**Phase 3 (US1)**: T024 (Context 7 query) can run parallel with setup
**Phase 4 (US2)**: T030 can start immediately if US1 complete (different tool)
**Phase 7 (US3)**: T053 can run parallel with US2 (different tool, different file)
**Phase 9 (US4)**: T066 can run parallel with US3, US5 (different tools)
**Phase 10 (US5)**: T073 can run parallel with US3, US4 (different tools)
**Phase 11 (Frontend)**: T081, T082 can run in parallel; T090-T094 navigation tasks can run in parallel
**Phase 12 (Deployment Prep)**: T101, T102, T103, T106, T107 can run in parallel
**Phase 14 (Validation)**: T117-T119 (Phase 2 UI) can run parallel with T120-T127 (Chat UI)
**Phase 15 (Documentation)**: T134, T135, T136, T137, T138, T140, T142 can run in parallel

---

## Parallel Example: Multiple User Stories

```bash
# After Foundational phase complete, launch 3 developers in parallel:

# Developer A: User Story 1 (Add Task)
Task: "Implement add_task tool in backend/mcp_server.py"

# Developer B: User Story 2 (List Tasks)
Task: "Implement list_tasks tool in backend/mcp_server.py"

# Developer C: User Story 3 (Complete Task)
Task: "Implement complete_task tool in backend/mcp_server.py"
```

---

## Implementation Strategy

### MVP First (P1 User Stories Only)

1. Complete Phase 1: Setup (T001-T008, including copying Phase 2 frontend)
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Add Task)
4. Complete Phase 4: User Story 2 (List Tasks)
5. Complete Phase 5: User Story 6 (AI Confirmations)
6. Complete Phase 6: User Story 7 (Conversation Persistence)
7. Complete Phase 11: Frontend (T081-T100 - add chat to Phase 2 frontend)
8. **STOP and VALIDATE**: Test BOTH UIs work (dashboard buttons + chat)
9. Deploy MVP (T108-T116)
10. Validate in production (T117-T133)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready, Phase 2 frontend copied
2. Add User Story 1 + 2 + 6 → Test independently → Basic chat working (MVP!)
3. Add User Story 7 → Test independently → Conversation persists
4. Add Phase 11 Frontend → Chat page added to Phase 2 UI
5. **Verify**: Both dashboard buttons AND chat work
6. Add User Story 3 → Test independently → Can complete tasks
7. Add User Story 8 → Test independently → Errors handled gracefully
8. Add User Story 4 + 5 → Test independently → Full CRUD complete
9. Each story adds value without breaking Phase 2 UI or previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (includes copying Phase 2 frontend)
2. Once Foundational done:
   - Developer A: US1 (Add Task) → US6 (Agent setup)
   - Developer B: US2 (List Tasks) → US7 (Chat endpoint)
   - Developer C: US3 (Complete) → US4 (Delete) → US5 (Update)
   - Developer D: Frontend Phase 11 (add chat page, update navbar)
3. Stories complete and integrate independently
4. Cross-UI testing: verify tasks created via chat appear in dashboard and vice versa
5. Final integration testing before deployment

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Context 7 queries (T024, T035, T081) MUST be executed before implementation per constitution
- **Phase 2 frontend reuse**: Copy ../phase2/frontend/ to phase3/frontend/, then ADD chat functionality
- Phase 2 immutability enforced: No modifications to ../phase2/ directory (copy, don't modify)
- Stateless architecture enforced: No in-memory conversation storage (T042-T051)
- MCP tool pattern compliance: All tools follow standardized return format (T026-T080)
- **Dual interface validation**: Test both dashboard buttons AND chat commands work for same tasks
- **Cross-UI sync**: Tasks created via one interface must appear in the other
