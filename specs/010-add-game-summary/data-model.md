# Data Model for 010-add-game-summary

This feature does not introduce any new data models.

It involves modifications to the following existing classes, which act as data models for their respective game states:

-   **`ChessGameState`** (`src/mcts_gen/games/chess_mcts.py`)
    -   This class will be modified to add the `get_state_summary()` method. This method will read the game history stored within the `self.board` object to produce a PGN string.

-   **`ShogiGameState`** (`src/mcts_gen/games/shogi_mcts.py`)
    -   This class will be modified to add the `get_state_summary()` method. This method will read the game history stored within the `self.board` object to produce a KIF string.

No new persistent entities or database schema changes are required.
