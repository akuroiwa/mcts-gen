# Research: Implementing `chess_mcts.py`

## Objective
Define the implementation strategy for `src/mcts_gen/games/chess_mcts.py` by analyzing existing game modules and the `python-chess` library.

## Analysis of `src/mcts_gen/games/shogi_mcts.py`
The existing `shogi_mcts.py` provides a clear blueprint for integrating a new game.

- **Base Class**: Inherits from `mcts_gen.models.game_state.GameStateBase`.
- **Core Logic**: Wraps the `python-shogi` library's `Board` object.
- **State Initialization**: Accepts an SFEN string in the constructor.
- **Actions**: Returns a list of legal moves as USI strings (`move.usi()`).
- **State Transition**: `takeAction` method accepts a USI string, deep-copies the state, and applies the move using `board.push_usi()`.
- **Game Termination**: `isTerminal()` checks for game-over conditions.
- **Reward**: `getReward()` returns -1.0 for a loss, 1.0 for a win (from the perspective of the player who just moved), and 0.0 for draws or non-terminal states.

## Analysis of `python-chess` Library
The `python-chess` library provides analogous functionality to `python-shogi`.

- **Board**: `chess.Board(fen=...)` can be used to represent the game state.
- **Moves**: `board.legal_moves` provides an iterator of legal moves. Moves have a `uci()` method to get the standard string representation.
- **State Changes**: `board.push_uci(uci_string)` applies a move.
- **Game State**:
    - `board.turn` returns `chess.WHITE` or `chess.BLACK`.
    - `board.is_game_over()` checks for termination.
    - `board.result()` gives the outcome (e.g., "1-0", "0-1", "1/2-1/2").
    - Specific outcome checks exist: `is_checkmate()`, `is_stalemate()`, `is_insufficient_material()`, etc.

## Implementation Decision

The new `ChessGameState` class will mirror the structure of `ShogiGameState`.

1.  **Class Definition**: `class ChessGameState(GameStateBase):`
2.  **Constructor**: `__init__(self, fen: str = None)` will create a `chess.Board`. If `fen` is `None`, it will use the default starting position.
3.  **`getCurrentPlayer()`**: Return `1` for `chess.WHITE` and `-1` for `chess.BLACK`.
4.  **`getPossibleActions()`**: Return `[move.uci() for move in self.board.legal_moves]`.
5.  **`takeAction(action: str)`**: Deep-copy the state and use `self.board.push_uci(action)`.
6.  **`isTerminal()`**: Return `self.board.is_game_over()`.
7.  **`getReward()`**:
    - If not terminal, return `0.0`.
    - If `is_checkmate()`, the player whose turn it *is* has been checkmated, so the *other* player won. The reward should be `1.0` for the winner and `-1.0` for the loser. The MCTS framework typically evaluates the state for the *next* player. When a game ends, the reward is for the player who just moved. If `board.is_checkmate()`, the player who just moved delivered the checkmate and won, so the reward is `1.0`.
    - For all other draw conditions (`is_stalemate`, `is_insufficient_material`, etc.), return `0.0`.
8.  **Serialization**:
    - `to_dict()`: Return `{'fen': self.board.fen()}`.
    - `__str__()`: Return `str(self.board)` for a simple text representation.
