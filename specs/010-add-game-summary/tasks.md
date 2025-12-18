---
description: "Task list for feature: Implement Rich Game State Summary for Chess and Shogi"
---

# Tasks: Implement Rich Game State Summary for Chess and Shogi

**Input**: Design documents from `/specs/010-add-game-summary/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

---
## Phase 1: Setup

**Purpose**: Ensure project dependencies are installed.

- [X] T001 Ensure `python-chess` and `python-shogi` are installed (`uv pip install python-chess python-shogi`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No foundational tasks are required for this feature as it builds upon the existing structure.

---

## Phase 3: User Story 1 - Chess Game Analysis (Priority: P1) 🎯 MVP

**Goal**: Implement `get_state_summary` in `ChessGameState` to return the full game PGN.

**Independent Test**: Run a Chess MCTS simulation, call `get_principal_variation`, and verify the `final_state_summary` contains a valid PGN string.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T002 [US1] Create a unit test `test_get_state_summary_pgn` in `tests/unit/test_games/test_chess_mcts.py`. This test should create a `ChessGameState`, push several moves, and assert that the `get_state_summary()` method returns a dictionary with a valid `pgn` key.

### Implementation for User Story 1

- [ ] T003 [P] [US1] Add `import chess.pgn` to `src/mcts_gen/games/chess_mcts.py`.
- [ ] T004 [US1] Implement the `get_state_summary(self) -> dict` method in the `ChessGameState` class in `src/mcts_gen/games/chess_mcts.py`. Use `chess.pgn.Game.from_board(self.board)` to generate the PGN string.
- [ ] T005 [US1] Run the test `test_get_state_summary_pgn` and ensure it passes.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 - Shogi Game Analysis (Priority: P1)

**Goal**: Implement `get_state_summary` in `ShogiGameState` to return the full game KIF.

**Independent Test**: Run a Shogi MCTS simulation, call `get_principal_variation`, and verify the `final_state_summary` contains a valid KIF string.

### Tests for User Story 2 ⚠️

- [ ] T006 [US2] Create a unit test `test_get_state_summary_kif` in `tests/unit/test_games/test_shogi_mcts.py`. This test should create a `ShogiGameState`, push several moves, and assert that the `get_state_summary()` method returns a dictionary with a valid `kif` key.

### Implementation for User Story 2

- [ ] T007 [P] [US2] Add `import shogi.KIF` to `src/mcts_gen/games/shogi_mcts.py`.
- [ ] T008 [US2] Implement the `get_state_summary(self) -> dict` method in the `ShogiGameState` class in `src/mcts_gen/games/shogi_mcts.py`. Use `shogi.KIF.Exporter(self.board)` to generate the KIF string.
- [ ] T009 [US2] Run the test `test_get_state_summary_kif` and ensure it passes.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently.

---

## Phase 5: Polish & Cross-Cutting Concerns

- [ ] T010 [P] Review and add docstrings for the new `get_state_summary` methods in `src/mcts_gen/games/chess_mcts.py` and `src/mcts_gen/games/shogi_mcts.py`.
- [ ] T011 Manually validate the feature by following the steps in `specs/010-add-game-summary/quickstart.md`.
- [ ] T012 Final check of `GEMINI.md` to ensure context is accurate.

---

## Dependencies & Execution Order

### Phase Dependencies
- **Setup (Phase 1)**: Must be completed first.
- **User Stories (Phase 3 & 4)**: Can begin after Setup.
- **Polish (Phase 5)**: Depends on all user stories being complete.

### User Story Dependencies
- **User Story 1 (Chess)**: No dependencies on other stories.
- **User Story 2 (Shogi)**: No dependencies on other stories.

### Parallel Opportunities
- After Phase 1, **User Story 1** and **User Story 2** can be implemented in parallel.
  - Task `T003` and `T007` can be done in parallel.
- The polish task `T010` can be done in parallel for both files.

---

## Implementation Strategy

### Incremental Delivery
1.  Complete Phase 1 (Setup).
2.  Implement and test User Story 1 (Chess). The feature is now functional for Chess.
3.  Implement and test User Story 2 (Shogi). The feature is now functional for both games.
4.  Complete Phase 5 (Polish).
