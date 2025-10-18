# Tasks for Feature: Add full support for chess

**Feature**: Add full support for chess
**Branch**: `005-add-full-support`

This plan is based on the Test-Driven Development (TDD) methodology. Tests are created before the implementation to ensure correctness.

---

## Task List

### Phase 1: Setup & Dependencies

*   **T001: Configure `pyproject.toml` for chess dependency**
    *   **File**: `pyproject.toml`
    *   **Action**: Add a new optional dependency group `[project.optional-dependencies.chess]` and include the `python-chess` library in it.
    *   **Example**:
        ```toml
        [project.optional-dependencies]
        dev = [...]
        shogi = [...]
        chess = [
            "python-chess"
        ]
        ```

### Phase 2: Contract Testing (TDD)

*   **T002: Create contract test for `ChessGameState`**
    *   **File**: `tests/contract/test_chess_mcts.py`
    *   **Action**: Create a new test file and add `pytest` tests for the `ChessGameState` class. These tests MUST fail initially.
    *   **Requirements**:
        *   Import `ChessGameState` (it won't exist yet).
        *   Test initialization with a FEN string (e.g., from `quickstart.md`) and without (default board).
        *   Test `getCurrentPlayer()` for both white's and black's turn.
        *   Test `getPossibleActions()` to ensure it returns a list of valid UCI move strings.
        *   Test `takeAction()` to verify the board state changes correctly after a move.
        *   Test `isTerminal()` on a non-terminal position and a checkmate/stalemate position.
        *   Test `getReward()` for a win, loss, and draw.
        *   Test `to_dict()` to ensure it returns the correct FEN string.

### Phase 3: Implementation

*   **T003: Implement `ChessGameState`**
    *   **File**: `src/mcts_gen/games/chess_mcts.py`
    *   **Action**: Create the `ChessGameState` class as defined in `research.md` and `data-model.md`.
    *   **Goal**: Make all the tests in `tests/contract/test_chess_mcts.py` pass.
    *   **Dependencies**: T002 must be complete.

### Phase 4: Documentation & Localization

*   **T004: Update `README.md` with installation instructions [P]**
    *   **File**: `README.md`
    *   **Action**: Add a section under "Installation" titled "Installation with Game-Specific Dependencies" explaining how to install extras like `mcts-gen[shogi]` and `mcts-gen[chess]`.
    *   **Dependencies**: T001 must be complete.

*   **T005: Update `docs/quickstart.rst` with installation instructions [P]**
    *   **File**: `docs/quickstart.rst`
    *   **Action**: Add the same installation instructions to the quickstart documentation, ensuring it's clear for new users.
    *   **Dependencies**: T001 must be complete.

*   **T006: Update Japanese translations**
    *   **Directory**: `docs/`
    *   **Action**: Run the following commands in sequence from the `docs` directory to update and build the Japanese localization files.
        1.  `make gettext`
        2.  `sphinx-intl update --language=ja`
    *   **Note**: The user will review the generated `.po` files. We are not responsible for the translation itself, only for updating the files.
    *   **Dependencies**: T005 must be complete.

---

## Parallel Execution Guide

Tasks marked with `[P]` can be executed in parallel after their dependencies are met.

**Example**: Once T001 is done, T004 and T005 can be run concurrently.

```bash
# (After T001 is complete)

# Terminal 1: Execute Task T004
/execute T004

# Terminal 2: Execute Task T005
/execute T005
```
