# Tasks: Todo Frontend Web Application

**Input**: Design documents from `/specs/001-todo-frontend/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api-contracts.md

**Tests**: Tests are NOT explicitly requested in the specification, so test tasks are excluded. Focus is on implementation and manual validation per acceptance scenarios.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5, US6, US7)
- Include exact file paths in descriptions

## Path Conventions

- **Frontend**: `frontend/` directory at repository root
- All paths shown are relative to `frontend/` directory
- Absolute paths when needed: `D:\Q4-Gemini_CLI\Hackathon_2\phase2\frontend\`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create frontend project structure: Initialize Next.js 16 with TypeScript in frontend/ directory
- [X] T002 [P] Install core dependencies: next@16+, react@19+, typescript, tailwindcss per package.json
- [X] T003 [P] Configure Tailwind CSS: Setup tailwind.config.ts with dark mode and Shadcn color variables
- [X] T004 [P] Setup TypeScript configuration: Create tsconfig.json with strict mode enabled
- [X] T005 [P] Create global styles in frontend/app/globals.css with Tailwind directives and CSS variables
- [X] T006 [P] Initialize Shadcn CLI: Run npx shadcn@latest init with default configuration
- [X] T007 [P] Install Shadcn button component in frontend/components/ui/button.tsx
- [X] T008 [P] Install Shadcn input component in frontend/components/ui/input.tsx
- [X] T009 [P] Install Shadcn textarea component in frontend/components/ui/textarea.tsx
- [X] T010 [P] Install Shadcn dialog component in frontend/components/ui/dialog.tsx
- [X] T011 [P] Install Shadcn card component in frontend/components/ui/card.tsx
- [X] T012 [P] Install Shadcn checkbox component in frontend/components/ui/checkbox.tsx
- [X] T013 [P] Install Shadcn form component in frontend/components/ui/form.tsx (requires react-hook-form)
- [X] T014 [P] Install Shadcn toast component in frontend/components/ui/toast.tsx and sonner
- [X] T015 [P] Install Shadcn switch component in frontend/components/ui/switch.tsx
- [X] T016 [P] Create environment file template: Copy .env.example with NEXT_PUBLIC_API_URL and BETTER_AUTH_SECRET placeholders
- [X] T017 Configure Next.js in frontend/next.config.ts for API proxy and image optimization

**Checkpoint**: Basic Next.js project with Tailwind and all Shadcn components installed

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T018 Create TypeScript type definitions in frontend/lib/types.ts for User, Task, Session, APIError, and all request/response models
- [X] T019 Setup Better Auth configuration in frontend/lib/auth.ts with JWT plugin and 7-day session
- [X] T020 Create API client base in frontend/lib/api.ts with fetchAPI wrapper, auth token injection, and error handling
- [X] T021 Implement tasksAPI object in frontend/lib/api.ts with all 6 task endpoint functions (list, create, update, toggleComplete, delete)
- [X] T022 Create utility functions in frontend/lib/utils.ts including cn() for className merging
- [X] T023 Create ThemeProvider component in frontend/providers/ThemeProvider.tsx wrapping next-themes
- [X] T024 Create middleware.ts in frontend/ root for route protection checking JWT session
- [X] T025 Create root layout in frontend/app/layout.tsx with ThemeProvider, Toaster, and metadata
- [X] T026 Create home page in frontend/app/page.tsx with auth-based redirect logic (authenticated→dashboard, unauthenticated→login)

**Checkpoint**: Foundation ready - authentication, API client, middleware, and basic layouts configured. User story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - New User Registration and First Login (Priority: P1) 🎯 MVP

**Goal**: Enable new users to create accounts, log in, log out, and access a protected dashboard

**Independent Test**: Complete signup flow with valid credentials → redirected to empty dashboard → logout → login again with same credentials → see dashboard again

### Implementation for User Story 1

- [X] T027 [P] [US1] Create signup page in frontend/app/signup/page.tsx with email, password, confirmPassword form
- [X] T028 [P] [US1] Create login page in frontend/app/login/page.tsx with email and password form
- [X] T029 [P] [US1] Create Navbar component in frontend/components/Navbar.tsx with logout button and user email display
- [X] T030 [US1] Add signup form validation: Email format, password min 8 chars, passwords match in frontend/app/signup/page.tsx
- [X] T031 [US1] Add login form validation: Required fields, email format in frontend/app/login/page.tsx
- [X] T032 [US1] Implement signup handler: Call Better Auth signup API, store token, redirect to /dashboard in frontend/app/signup/page.tsx
- [X] T033 [US1] Implement login handler: Call Better Auth login API, store token, redirect to /dashboard or ?from param in frontend/app/login/page.tsx
- [X] T034 [US1] Implement logout handler in Navbar: Call Better Auth signOut, clear session, redirect to /login in frontend/components/Navbar.tsx
- [X] T035 [US1] Add error handling for signup: Display 409 (email exists), 400 (validation), 422 errors as toast notifications in frontend/app/signup/page.tsx
- [X] T036 [US1] Add error handling for login: Display 401 (invalid credentials) as generic error message in frontend/app/login/page.tsx
- [X] T037 [US1] Create basic dashboard page in frontend/app/dashboard/page.tsx with server-side auth check and welcome message
- [X] T038 [US1] Add Navbar to dashboard layout showing logged-in user's email in frontend/app/dashboard/page.tsx

**Checkpoint**: Users can sign up, log in, see protected dashboard with navbar, and log out. MVP complete!

---

## Phase 4: User Story 2 - View and Browse Todo List (Priority: P2)

**Goal**: Authenticated users can view their complete task list with all details, see empty state, and handle loading/error states

**Independent Test**: Pre-populate tasks via backend API → login → dashboard displays all tasks with title, description, status, date → verify empty state when no tasks → verify loading spinner during fetch → verify error message with retry on API failure

### Implementation for User Story 2

- [X] T039 [P] [US2] Create TaskList component in frontend/components/tasks/TaskList.tsx as Server Component fetching tasks
- [X] T040 [P] [US2] Create TaskItem component in frontend/components/tasks/TaskItem.tsx displaying single task with all fields
- [X] T041 [P] [US2] Create EmptyState component in frontend/components/tasks/EmptyState.tsx with encouraging message
- [X] T042 [US2] Implement task fetching in TaskList: Call tasksAPI.list() on server, handle errors in frontend/components/tasks/TaskList.tsx
- [X] T043 [US2] Add empty state logic: Show EmptyState component when tasks array is empty in frontend/components/tasks/TaskList.tsx
- [X] T044 [US2] Add loading skeleton: Show loading spinner while tasks are being fetched in frontend/components/tasks/TaskList.tsx
- [X] T045 [US2] Add error state: Display friendly error message with retry button on fetch failure in frontend/components/tasks/TaskList.tsx
- [X] T046 [US2] Style TaskItem: Show title, description, completion status (checkbox), and formatted created_at date in frontend/components/tasks/TaskItem.tsx
- [X] T047 [US2] Add visual distinction: Style completed tasks with strikethrough and reduced opacity in frontend/components/tasks/TaskItem.tsx
- [X] T048 [US2] Integrate TaskList into dashboard: Replace welcome message with TaskList component in frontend/app/dashboard/page.tsx
- [X] T049 [US2] Add responsive layout: Grid/list view that adapts to mobile (single column) and desktop (multi-column) in frontend/components/tasks/TaskList.tsx

**Checkpoint**: Dashboard displays task list with all details, handles empty/loading/error states, and is responsive

---

## Phase 5: User Story 3 - Create New Todo Task (Priority: P3)

**Goal**: Users can create new tasks via a dialog form with validation and see them appear in the list immediately

**Independent Test**: Click "New Task" button → dialog opens → enter valid title and description → submit → dialog closes → new task appears in list → refresh page → task persists

### Implementation for User Story 3

- [ ] T050 [P] [US3] Create CreateTaskDialog component in frontend/components/tasks/CreateTaskDialog.tsx with form fields
- [ ] T051 [P] [US3] Add "New Task" button to dashboard in frontend/app/dashboard/page.tsx that opens CreateTaskDialog
- [ ] T052 [US3] Implement form state management: useState for title, description, isOpen in frontend/components/tasks/CreateTaskDialog.tsx
- [ ] T053 [US3] Add form validation: Title required (1-200 chars), description optional (max 1000 chars) in frontend/components/tasks/CreateTaskDialog.tsx
- [ ] T054 [US3] Implement create handler: Call tasksAPI.create(), close dialog on success, show error on failure in frontend/components/tasks/CreateTaskDialog.tsx
- [ ] T055 [US3] Add validation error display: Show inline error messages for title and description length in frontend/components/tasks/CreateTaskDialog.tsx
- [ ] T056 [US3] Add character counter: Display remaining characters for title (200) and description (1000) in frontend/components/tasks/CreateTaskDialog.tsx
- [ ] T057 [US3] Add loading state: Disable submit button and show spinner while creating in frontend/components/tasks/CreateTaskDialog.tsx
- [ ] T058 [US3] Add success feedback: Show toast notification "Task created!" on successful creation in frontend/components/tasks/CreateTaskDialog.tsx
- [ ] T059 [US3] Add error preservation: Keep form values if API fails so user doesn't lose input in frontend/components/tasks/CreateTaskDialog.tsx
- [ ] T060 [US3] Implement dialog close handler: Clear form on cancel/close in frontend/components/tasks/CreateTaskDialog.tsx
- [ ] T061 [US3] Update TaskList to refetch: Use router.refresh() or revalidatePath to show new task in frontend/components/tasks/CreateTaskDialog.tsx

**Checkpoint**: Users can create tasks via dialog, see validation errors, and new tasks appear in list

---

## Phase 6: User Story 4 - Toggle Task Completion Status (Priority: P4)

**Goal**: Users can mark tasks complete/incomplete by clicking checkbox with instant visual feedback and automatic rollback on errors

**Independent Test**: Click checkbox on incomplete task → task immediately shows as complete → refresh page → task remains complete → click checkbox again → task shows as incomplete → simulate backend error → task reverts to previous state with error toast

### Implementation for User Story 4

- [ ] T062 [P] [US4] Create useOptimisticToggle custom hook in frontend/hooks/useOptimisticToggle.ts with optimistic state and rollback logic
- [ ] T063 [US4] Add checkbox to TaskItem: Use Shadcn Checkbox component bound to task.completed in frontend/components/tasks/TaskItem.tsx
- [ ] T064 [US4] Implement optimistic update: Update local state immediately on checkbox click in frontend/components/tasks/TaskItem.tsx using useOptimisticToggle
- [ ] T065 [US4] Implement backend call: Call tasksAPI.toggleComplete() after optimistic update in frontend/components/tasks/TaskItem.tsx
- [ ] T066 [US4] Add rollback logic: Revert to original state if API call fails in frontend/components/tasks/TaskItem.tsx
- [ ] T067 [US4] Add visual feedback: Show pending state (disabled checkbox) during API call in frontend/components/tasks/TaskItem.tsx
- [ ] T068 [US4] Add error handling: Show toast error "Failed to update task" on API failure in frontend/components/tasks/TaskItem.tsx
- [ ] T069 [US4] Add success indication: Briefly show success state (optional) or rely on instant UI update in frontend/components/tasks/TaskItem.tsx
- [ ] T070 [US4] Verify state persistence: Ensure completed status persists after page refresh in frontend/components/tasks/TaskItem.tsx

**Checkpoint**: Task completion toggle works instantly with optimistic updates and handles errors gracefully

---

## Phase 7: User Story 5 - Edit Existing Task (Priority: P5)

**Goal**: Users can edit task title and description via a pre-filled dialog form with validation

**Independent Test**: Click edit button on task → dialog opens with current values → modify title and/or description → save → dialog closes → changes reflected in list → refresh page → changes persist

### Implementation for User Story 5

- [ ] T071 [P] [US5] Create EditTaskDialog component in frontend/components/tasks/EditTaskDialog.tsx with pre-filled form
- [ ] T072 [P] [US5] Add edit button to TaskItem in frontend/components/tasks/TaskItem.tsx that opens EditTaskDialog with task data
- [ ] T073 [US5] Implement form pre-filling: Initialize title and description from task prop in frontend/components/tasks/EditTaskDialog.tsx
- [ ] T074 [US5] Add form validation: Same as create (title 1-200 chars, description max 1000 chars) in frontend/components/tasks/EditTaskDialog.tsx
- [ ] T075 [US5] Implement update handler: Call tasksAPI.update() with modified fields only in frontend/components/tasks/EditTaskDialog.tsx
- [ ] T076 [US5] Add validation error display: Show inline errors for invalid input in frontend/components/tasks/EditTaskDialog.tsx
- [ ] T077 [US5] Add character counter: Display remaining characters same as create dialog in frontend/components/tasks/EditTaskDialog.tsx
- [ ] T078 [US5] Add loading state: Disable submit and show spinner during update in frontend/components/tasks/EditTaskDialog.tsx
- [ ] T079 [US5] Add success feedback: Show toast "Task updated!" on success in frontend/components/tasks/EditTaskDialog.tsx
- [ ] T080 [US5] Add error preservation: Keep edited values if API fails in frontend/components/tasks/EditTaskDialog.tsx
- [ ] T081 [US5] Implement cancel handler: Close dialog without saving if user cancels in frontend/components/tasks/EditTaskDialog.tsx
- [ ] T082 [US5] Update TaskList: Use router.refresh() to show updated task in frontend/components/tasks/EditTaskDialog.tsx

**Checkpoint**: Users can edit existing tasks with validation and see changes reflected immediately

---

## Phase 8: User Story 6 - Delete Todo Task (Priority: P6)

**Goal**: Users can permanently delete tasks with confirmation dialog to prevent accidental deletion

**Independent Test**: Click delete button → confirmation dialog appears → click confirm → task removed from list → verify task deleted from backend → test cancel button → task remains in list

### Implementation for User Story 6

- [ ] T083 [P] [US6] Create DeleteConfirmDialog component in frontend/components/tasks/DeleteConfirmDialog.tsx with confirmation message
- [ ] T084 [P] [US6] Add delete button to TaskItem in frontend/components/tasks/TaskItem.tsx that opens DeleteConfirmDialog
- [ ] T085 [US6] Implement confirmation dialog: Show task title in confirmation message "Delete [title]?" in frontend/components/tasks/DeleteConfirmDialog.tsx
- [ ] T086 [US6] Implement delete handler: Call tasksAPI.delete() only after confirmation in frontend/components/tasks/DeleteConfirmDialog.tsx
- [ ] T087 [US6] Add loading state: Disable confirm button and show spinner during deletion in frontend/components/tasks/DeleteConfirmDialog.tsx
- [ ] T088 [US6] Add success feedback: Show toast "Task deleted" and remove from UI on success in frontend/components/tasks/DeleteConfirmDialog.tsx
- [ ] T089 [US6] Add error handling: Show toast error and keep task in list if deletion fails in frontend/components/tasks/DeleteConfirmDialog.tsx
- [ ] T090 [US6] Implement cancel handler: Close dialog without deleting on cancel/close in frontend/components/tasks/DeleteConfirmDialog.tsx
- [ ] T091 [US6] Update TaskList: Use router.refresh() or optimistic removal to update list in frontend/components/tasks/DeleteConfirmDialog.tsx
- [ ] T092 [US6] Add keyboard shortcut: Support Escape to cancel deletion dialog in frontend/components/tasks/DeleteConfirmDialog.tsx

**Checkpoint**: Users can delete tasks with confirmation and proper error handling

---

## Phase 9: User Story 7 - Toggle Between Light and Dark Mode (Priority: P7)

**Goal**: Users can switch between light/dark themes with a toggle, with preference persisted across sessions

**Independent Test**: Click theme toggle → UI switches to dark mode → all components readable → refresh page → dark mode persists → click toggle again → switches to light mode → test all pages and dialogs in both modes

### Implementation for User Story 7

- [ ] T093 [P] [US7] Create ThemeToggle component in frontend/components/ThemeToggle.tsx using next-themes useTheme hook
- [ ] T094 [P] [US7] Add sun/moon icons from lucide-react to ThemeToggle in frontend/components/ThemeToggle.tsx
- [ ] T095 [US7] Add theme toggle to Navbar in frontend/components/Navbar.tsx positioned in header
- [ ] T096 [US7] Implement theme switch: Toggle between light/dark on click in frontend/components/ThemeToggle.tsx
- [ ] T097 [US7] Add smooth transition: Configure CSS transitions for theme changes in frontend/app/globals.css
- [ ] T098 [US7] Add icon animation: Rotate sun/moon icons on theme switch in frontend/components/ThemeToggle.tsx
- [ ] T099 [US7] Test dark mode colors: Verify all Shadcn components have proper dark mode styles in all pages
- [ ] T100 [US7] Test dark mode readability: Ensure text contrast meets accessibility standards in both modes in all components
- [ ] T101 [US7] Add system preference detection: Default to system theme on first visit in frontend/providers/ThemeProvider.tsx
- [ ] T102 [US7] Verify persistence: Test theme preference saves to localStorage and persists across sessions in frontend/components/ThemeToggle.tsx
- [ ] T103 [US7] Add mounted check: Prevent hydration mismatch by checking mounted state in frontend/components/ThemeToggle.tsx

**Checkpoint**: Theme toggle works smoothly, persists across sessions, all components look good in both modes

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final touches

- [ ] T104 [P] Add responsive navbar: Mobile hamburger menu for smaller screens in frontend/components/Navbar.tsx
- [ ] T105 [P] Add loading indicators: Global loading bar for page transitions in frontend/app/layout.tsx
- [ ] T106 [P] Optimize images: Configure Next.js Image component for logos/avatars in frontend/next.config.ts
- [ ] T107 [P] Add meta tags: SEO metadata for all pages (title, description) in each page.tsx
- [ ] T108 [P] Add favicon: Create and link favicon.ico in frontend/app/ directory
- [ ] T109 [P] Add 404 page: Create custom not-found.tsx with helpful message in frontend/app/not-found.tsx
- [ ] T110 [P] Add error boundary: Create error.tsx for global error handling in frontend/app/error.tsx
- [ ] T111 [P] Improve form accessibility: Add ARIA labels and keyboard navigation to all forms across components
- [ ] T112 [P] Add focus states: Ensure all interactive elements have visible focus indicators in frontend/app/globals.css
- [ ] T113 Add rate limiting feedback: Handle 429 (too many requests) errors gracefully in frontend/lib/api.ts
- [ ] T114 Add session expiry warning: Show warning toast 5 minutes before session expires in frontend/components/Navbar.tsx
- [ ] T115 Add network status indicator: Show offline banner when network is unavailable in frontend/app/layout.tsx
- [ ] T116 Code cleanup: Remove console.logs, unused imports, commented code across all files
- [ ] T117 Format code: Run Prettier/ESLint on all files in frontend/ directory
- [ ] T118 Update README: Document setup, environment variables, and development workflow in frontend/README.md
- [ ] T119 Create .env.example: Document all required environment variables in frontend/.env.example
- [ ] T120 Run quickstart validation: Follow quickstart.md to verify all setup steps work correctly

**Checkpoint**: Application is polished, accessible, performant, and production-ready

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-9)**: All depend on Foundational phase completion
  - US1 (P1) - Authentication: Can start after Foundational
  - US2 (P2) - View Tasks: Depends on US1 (needs login to see dashboard)
  - US3 (P3) - Create Task: Depends on US2 (needs task list component)
  - US4 (P4) - Toggle Complete: Depends on US2 (needs TaskItem component)
  - US5 (P5) - Edit Task: Depends on US2 (needs TaskItem component)
  - US6 (P6) - Delete Task: Depends on US2 (needs TaskItem component)
  - US7 (P7) - Dark Mode: Can start after Setup (independent of other stories)
- **Polish (Phase 10)**: Depends on all desired user stories being complete

### User Story Dependencies

- **US1 (P1) - Authentication**: Can start after Foundational - No dependencies on other stories
- **US2 (P2) - View Tasks**: Depends on US1 completion (needs authenticated dashboard)
- **US3 (P3) - Create Task**: Depends on US2 completion (needs TaskList to display new tasks)
- **US4 (P4) - Toggle**: Depends on US2 completion (modifies TaskItem component)
- **US5 (P5) - Edit**: Depends on US2 completion (modifies TaskItem component)
- **US6 (P6) - Delete**: Depends on US2 completion (modifies TaskItem component)
- **US7 (P7) - Dark Mode**: Can run in parallel after Setup (independent feature)

### Within Each User Story

- Component files can be created in parallel if they don't depend on each other
- Implementation tasks that modify the same file must run sequentially
- Logic/handlers within a component should be implemented after the component structure is created

### Parallel Opportunities

- **Phase 1 (Setup)**: T002-T017 can all run in parallel (different files, no dependencies)
- **Phase 2 (Foundational)**: T018-T023 can run in parallel; T024-T026 depend on T018-T023
- **User Story Components**: Initial component files (CreateTaskDialog, EditTaskDialog, etc.) can be created in parallel within their phase
- **Phase 10 (Polish)**: T104-T112 can run in parallel (different files/concerns)
- **US7 (Dark Mode)**: Can run in parallel with US3-US6 if team capacity allows (independent feature)

---

## Parallel Example: Phase 1 (Setup)

All Shadcn component installations can run simultaneously:

```bash
# Launch all these tasks in parallel:
Task: "Install Shadcn button component in frontend/components/ui/button.tsx"
Task: "Install Shadcn input component in frontend/components/ui/input.tsx"
Task: "Install Shadcn textarea component in frontend/components/ui/textarea.tsx"
Task: "Install Shadcn dialog component in frontend/components/ui/dialog.tsx"
Task: "Install Shadcn card component in frontend/components/ui/card.tsx"
Task: "Install Shadcn checkbox component in frontend/components/ui/checkbox.tsx"
Task: "Install Shadcn form component in frontend/components/ui/form.tsx"
Task: "Install Shadcn toast component in frontend/components/ui/toast.tsx"
Task: "Install Shadcn switch component in frontend/components/ui/switch.tsx"
```

## Parallel Example: User Story 2

Initial component creation can be parallel:

```bash
# Launch these tasks together:
Task: "Create TaskList component in frontend/components/tasks/TaskList.tsx"
Task: "Create TaskItem component in frontend/components/tasks/TaskItem.tsx"
Task: "Create EmptyState component in frontend/components/tasks/EmptyState.tsx"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup (T001-T017)
2. Complete Phase 2: Foundational (T018-T026) - CRITICAL
3. Complete Phase 3: User Story 1 - Authentication (T027-T038)
4. Complete Phase 4: User Story 2 - View Tasks (T039-T049)
5. **STOP and VALIDATE**: Test signup → login → view tasks → logout flow
6. Deploy/demo if ready - MVP delivers value!

### Incremental Delivery (Recommended)

1. Complete Setup + Foundational → Foundation ready
2. Add US1 (Authentication) → Test independently → Deploy/Demo
3. Add US2 (View Tasks) → Test independently → Deploy/Demo (MVP!)
4. Add US3 (Create Task) → Test independently → Deploy/Demo
5. Add US4 (Toggle Complete) → Test independently → Deploy/Demo
6. Add US5 (Edit Task) → Test independently → Deploy/Demo
7. Add US6 (Delete Task) → Test independently → Deploy/Demo
8. Add US7 (Dark Mode) → Test independently → Deploy/Demo
9. Add Polish → Final production release

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: US1 (Authentication) - blocks others
   - After US1 complete:
     - Developer A: US2 (View Tasks) - blocks US3-US6
     - Developer B: US7 (Dark Mode) - can run in parallel
   - After US2 complete:
     - Developer A: US3 (Create Task)
     - Developer B: US4 (Toggle Complete)
     - Developer C: US5 (Edit Task)
     - Developer D: US6 (Delete Task)
3. Stories complete and integrate independently

---

## Notes

- **[P] tasks**: Different files, no dependencies, safe to parallelize
- **[Story] label**: Maps task to specific user story for traceability
- **No tests included**: Specification doesn't require automated tests; rely on manual validation per acceptance scenarios in spec.md
- **File paths**: All paths relative to `frontend/` directory
- **Commit strategy**: Commit after each task or logical group (e.g., after each US phase)
- **Validation points**: Stop at each checkpoint to validate story independently before proceeding
- **Dependencies**: Follow the dependency graph - don't start a user story before its prerequisites are complete
- **Dark Mode (US7)**: Can be worked on in parallel with US3-US6 after US2 is complete

---

## Task Count Summary

- **Phase 1 (Setup)**: 17 tasks
- **Phase 2 (Foundational)**: 9 tasks
- **Phase 3 (US1 - Auth)**: 12 tasks
- **Phase 4 (US2 - View)**: 11 tasks
- **Phase 5 (US3 - Create)**: 12 tasks
- **Phase 6 (US4 - Toggle)**: 9 tasks
- **Phase 7 (US5 - Edit)**: 12 tasks
- **Phase 8 (US6 - Delete)**: 10 tasks
- **Phase 9 (US7 - Dark Mode)**: 11 tasks
- **Phase 10 (Polish)**: 17 tasks

**Total**: 120 tasks

**MVP Scope** (US1 + US2): 38 tasks (Setup + Foundational + US1 + US2)
**Full Feature Set**: 120 tasks

**Parallel Opportunities**: 35+ tasks can run in parallel during setup and within user story phases

---

## Suggested MVP Scope

For fastest time to value, implement in this order:

1. **Weeks 1**: Phase 1 (Setup) + Phase 2 (Foundational) → 26 tasks
2. **Week 2**: Phase 3 (US1 - Authentication) → 12 tasks
3. **Week 2-3**: Phase 4 (US2 - View Tasks) → 11 tasks

**MVP Delivered**: Users can sign up, log in, and view their task list (49 tasks total)

Then incrementally add US3 (Create), US4 (Toggle), US5 (Edit), US6 (Delete), US7 (Dark Mode), and Polish as separate deployable increments.
