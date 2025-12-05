---

description: "Task list for Allowing AI agents to autonomously learn how to initialize new games."
---

# Tasks: Allowing AI agents to autonomously learn how to initialize new games.

**Input**: Design documents from `/specs/008-ai-learn-init/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The feature specification implicitly requires testing the agent's behavior for new games and complex arguments. Therefore, a test task is included in the polish phase.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

No specific setup tasks are required for this feature, as it involves modifying an existing system prompt within an already set up project.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

No foundational tasks are required for this feature. The core modifications are directly within the AI agent's prompt logic and do not necessitate new underlying infrastructure.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Initializing a New, Unknown Game (Priority: P1) 🎯 MVP

**Goal**: AI agent autonomously learns to initialize new games without specific instructions.

**Independent Test**: Add a new game module (e.g., `checkers_mcts.py` with a simple `GameState` constructor) and task the AI agent to initialize a simulation for it. Success is measured by the agent correctly calling `reinitialize_mcts` without needing prior knowledge or manual intervention.

### Implementation for User Story 1

- [ ] T001 [US1] Update `mcts_autonomous_search` prompt with investigation instructions in `src/mcts_gen/fastmcp_server.py`
- [ ] T002 [US1] Implement logic to locate and read `*_mcts.py` in `src/mcts_gen/fastmcp_server.py`
- [ ] T003 [US1] Implement logic to identify `GameStateBase` subclass in `src/mcts_gen/fastmcp_server.py`
- [ ] T004 [US1] Implement logic to analyze `__init__` signature and docstring for arguments in `src/mcts_gen/fastmcp_server.py`
- [ ] T005 [US1] Implement logic to call `reinitialize_mcts` with discovered parameters in `src/mcts_gen/fastmcp_server.py`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Initializing a Game with Complex Arguments (Priority: P1)

**Goal**: AI agent handles games with complex initialization arguments by prompting the user.

**Independent Test**: Task agent with `ligand` game and verify argument request.

### Implementation for User Story 2

- [ ] T006 [US2] Implement logic to request arguments from the user if needed in `src/mcts_gen/fastmcp_server.py`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T007 Add a test to `tests/contract/test_mcp_prompts.py` to verify the new prompt behavior

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately (N/A for this feature)
- **Foundational (Phase 2)**: No dependencies (N/A for this feature)
- **User Stories (Phase 3+)**: User Story 1 can proceed directly. User Story 2 builds on the logic of User Story 1 but is implemented as a distinct task.
- **Polish (Final Phase)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies on other stories.
- **User Story 2 (P1)**: Builds on the investigation logic established in User Story 1 but is independently testable for its specific prompting behavior.

### Within Each User Story

- Core logic implementation tasks for a user story should precede the test task (if test is added in polish phase).
- Ensure that the agent's logic for analyzing `__init__` arguments (T004) is robust before implementing the call to `reinitialize_mcts` (T005) and argument prompting (T006).

### Parallel Opportunities

- No significant parallelization opportunities are identified for implementation tasks within this single feature, as most changes are within the same file (`src/mcts_gen/fastmcp_server.py`).
- The test task (T007) can be developed in parallel with the implementation if following a TDD approach.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1.  Complete Phase 3: User Story 1 tasks (T001-T005).
2.  **STOP and VALIDATE**: Test User Story 1 independently.

### Incremental Delivery

1.  Complete User Story 1 (T001-T005).
2.  Add User Story 2 (T006).
3.  Add Polish tasks (T007).

### Parallel Team Strategy

Not applicable for this feature due to the limited scope and single-file modifications.

---

## Notes

-   [P] tasks = different files, no dependencies
-   [Story] label maps task to specific user story for traceability
-   Each user story should be independently completable and testable
-   Verify tests fail before implementing
-   Commit after each task or logical group
-   Stop at any checkpoint to validate story independently
-   Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
