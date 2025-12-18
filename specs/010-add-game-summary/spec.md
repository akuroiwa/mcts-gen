# Feature Specification: Implement Rich Game State Summary for Chess and Shogi

**Feature Branch**: `010-add-game-summary`  
**Created**: 2025-12-16  
**Status**: Draft  
**Input**: User description: "In chess_mcts.py and shogi_mcts.py, implement the get_state_summary method. This method will be called by the existing get_principal_variation tool. For chess, the summary should include the full PGN of the game. For shogi, it should include the full KIF record."

## User Scenarios & Testing (mandatory)

### User Story 1 - Chess Game Analysis (Priority: P1)

A user runs a Chess MCTS simulation to explore optimal game lines. When they retrieve the principal variation using `get_principal_variation`, the `final_state_summary` in the output includes a standard PGN string, allowing them to easily review the entire game sequence in external chess software.

**Why this priority**: This directly addresses the user's need for a comprehensive, standardized output for Chess simulations, improving the interpretability of results.

**Independent Test**: Can be fully tested by running a Chess MCTS simulation, calling `get_principal_variation`, and verifying the PGN output with a chess PGN parser.

**Acceptance Scenarios**:

1.  **Given** a Chess MCTS simulation has run and found a principal variation, **When** `get_principal_variation` is called, **Then** the `final_state_summary` in the response contains a `pgn` key whose value is a valid PGN string representing the game history.
2.  **Given** the PGN string from `final_state_summary`, **When** it is loaded into standard chess software, **Then** the game history is correctly displayed.

---

### User Story 2 - Shogi Game Analysis (Priority: P1)

A user runs a Shogi MCTS simulation to explore optimal game lines. When they retrieve the principal variation using `get_principal_variation`, the `final_state_summary` in the output contains a standard KIF string, enabling them to analyze the game flow using shogi analysis tools.

**Why this priority**: This directly addresses the user's need for a comprehensive, standardized output for Shogi simulations, improving the interpretability of results.

**Independent Test**: Can be fully tested by running a Shogi MCTS simulation, calling `get_principal_variation`, and verifying the KIF output with a shogi KIF parser.

**Acceptance Scenarios**:

1.  **Given** a Shogi MCTS simulation has run and found a principal variation, **When** `get_principal_variation` is called, **Then** the `final_state_summary` in the response contains a `kif` key whose value is a valid KIF string representing the game history.
2.  **Given** the KIF string from `final_state_summary`, **When** it is loaded into standard shogi software, **Then** the game history is correctly displayed.

---

### Edge Cases
-   What happens when a game ends in a draw (Chess, Shogi)? The PGN/KIF should accurately reflect the draw outcome.
-   How does the system handle very long game histories? The PGN/KIF generation should scale efficiently.

## Requirements (mandatory)

### Functional Requirements
-   **FR1: Chess `get_state_summary` Implementation:** The `ChessGameState` class in `src/mcts_gen/games/chess_mcts.py` shall implement a `get_state_summary()` method.
-   **FR2: Chess PGN Output:** The `get_state_summary()` method in `ChessGameState` shall return a dictionary that includes a key, `pgn`, containing the full PGN string of the game history up to the final state.
-   **FR3: Shogi `get_state_summary` Implementation:** The `ShogiGameState` class in `src/mcts_gen/games/shogi_mcts.py` shall implement a `get_state_summary()` method.
-   **FR4: Shogi KIF Output:** The `get_state_summary()` method in `ShogiGameState` shall return a dictionary that includes a key, `kif`, containing the full KIF string of the game history up to the final state.

### Key Entities
-   **ChessGameState**: Represents the state of a Chess game, including its history of moves.
-   **ShogiGameState**: Represents the state of a Shogi game, including its history of moves.

## Success Criteria (mandatory)

### Measurable Outcomes
-   **SC1: Chess PGN Verifiability:** After a Chess MCTS simulation that finds a principal variation, the `final_state_summary` output from `get_principal_variation` shall contain a `pgn` key whose value is a syntactically valid PGN string that can be parsed by standard chess software.
-   **SC2: Shogi KIF Verifiability:** After a Shogi MCTS simulation that finds a principal variation, the `final_state_summary` output from `get_principal_variation` shall contain a `kif` key whose value is a syntactically valid KIF string that can be parsed by standard shogi software.
-   **SC3: Completeness:** The generated PGN/KIF strings accurately reflect the complete sequence of moves leading to the final state of the principal variation.
-   **SC4: Performance:** The `get_state_summary` method for both Chess and Shogi shall execute within 100ms on typical hardware for games up to 100 moves.

## Assumptions
*   The `python-chess` library provides sufficient functionality to generate a full PGN string from a `chess.Board` object that has a history of moves.
*   The `python-shogi` library provides sufficient functionality to generate a full KIF string from a `shogi.Board` object that has a history of moves.
*   The `get_principal_variation` tool in `ai_gp_simulator.py` will correctly call the `get_state_summary` method on the `final_state` object.

## Out of Scope
*   Support for other game state summary formats beyond PGN (Chess) and KIF (Shogi).
*   Advanced analysis or visualization of PGN/KIF within the `mcts-gen` framework.

## Dependencies
*   `chess_mcts.py` depends on the `python-chess` library.
*   `shogi_mcts.py` depends on the `python-shogi` library.