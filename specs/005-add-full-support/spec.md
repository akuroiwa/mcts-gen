# Feature Specification: Add full support for chess

**Feature Branch**: `005-add-full-support`
**Status**: Draft
**Input**: User description: "Add full support for chess, including a new chess_mcts.py implementation, python-chess dependency, updated documentation, and i18n."

---

## User Scenarios & Testing *(mandatory)*

### Primary User Story
As a user of the `mcts-gen` library, I want to apply the MCTS algorithm to chess games to find the optimal move, and I want to be able to install the necessary chess-specific dependencies easily.

### Acceptance Scenarios
1.  **Given** a fresh environment, **When** I run `uv pip install mcts-gen[chess]`, **Then** `python-chess` is installed as a dependency.
2.  **Given** a chess game state represented by a FEN string, **When** I initialize the `chess_mcts` module with it, **Then** the game state is correctly set up.
3.  **Given** an initialized `chess_mcts` game, **When** I run the MCTS simulation, **Then** it correctly identifies and returns the best move.
4.  **Given** I have made several moves, **When** I request the game history, **Then** a valid PGN string is returned.
5.  **Given** the project documentation, **When** I look for installation instructions, **Then** I find a clear explanation for installing game-specific extras like `[chess]`.
6.  **Given** I am a Japanese user, **When** I build the documentation, **Then** the new instructions are correctly translated into Japanese.

### Edge Cases
- What happens when an invalid FEN string is provided? The system should raise a specific error.
- How does the system handle a game state that is a checkmate or stalemate? The MCTS should correctly identify that there are no further legal moves.

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: The system MUST provide a new game module, `src/mcts_gen/games/chess_mcts.py`, for handling chess games.
- **FR-002**: The system MUST use the `python-chess` library for all chess-related logic (game state, move generation, validation).
- **FR-003**: The system MUST allow initializing a chess game from a FEN (Forsyth-Edwards Notation) string.
- **FR-004**: The system MUST be able to print a user-friendly representation of the current board state to the console.
- **FR-005**: The system MUST provide a mechanism to export the game history in PGN (Portable Game Notation) format.
- **FR-006**: The project's packaging configuration (`pyproject.toml`) MUST be updated to define an optional dependency group `chess` that includes `python-chess`.
- **FR-007**: The user documentation (`README.md` and `docs/quickstart.rst`) MUST be updated to include instructions on how to install game-specific dependencies like `mcts-gen[chess]`.
- **FR-008**: The Japanese localization files (`.po`) MUST be updated to reflect the changes in the documentation.
- **FR-009**: The system MUST include tests for the `chess_mcts.py` module, using FEN strings from `chess-ant/pgn/` for test cases.

---

## Review & Acceptance Checklist

### Content Quality
- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] All mandatory sections completed

### Requirement Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable
- [ ] Scope is clearly bounded
- [ ] Dependencies and assumptions identified