# Data Model: Chess Game State

## Entity: ChessGameState

Represents the complete state of a single chess game at a specific point in time.

### Description
This entity encapsulates the `python-chess` library's `Board` object, providing a standardized interface for the MCTS engine. It is an in-memory object and is not intended for persistent storage, though it can be serialized to and from a FEN string.

### Attributes

- **board**: `chess.Board`
  - The underlying board object from the `python-chess` library.
  - It manages all game logic, including piece positions, turn, castling rights, en passant square, and move counters.

### State Representation

The canonical representation for serialization and initialization is the **Forsyth-Edwards Notation (FEN)** string.

- **Example (Starting Position)**: `rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1`

### Relationships

- **Inherits from**: `mcts_gen.models.game_state.GameStateBase`
  - It implements the abstract methods defined in the base class, conforming to the interface required by the MCTS engine.

### State Transitions

- **Creation**: A `ChessGameState` is created either with a default starting position or from a valid FEN string.
- **Update**: The state is immutable. The `takeAction` method does not modify the current state but instead returns a *new* `ChessGameState` instance representing the board after the move.
