# Game State Module Interface Contract

This document defines the Python interface that all game state modules MUST implement to be compatible with the `mcts-gen` MCTS engine.

## Base Class

All game state modules must inherit from `mcts_gen.models.game_state.GameStateBase`.

```python
from abc import ABC, abstractmethod
from typing import List, Any, Dict

class GameStateBase(ABC):
    @abstractmethod
    def getCurrentPlayer(self) -> int:
        """Returns the player whose turn it is (1 for player 1, -1 for player 2)."""
        pass

    @abstractmethod
    def getPossibleActions(self) -> List[Any]:
        """Returns a list of all legal actions from the current state."""
        pass

    @abstractmethod
    def takeAction(self, action: Any) -> 'GameStateBase':
        """Returns a new GameState object that results from taking the given action."""
        pass

    @abstractmethod
    def isTerminal(self) -> bool:
        """Returns True if the game is over, False otherwise."""
        pass

    @abstractmethod
    def getReward(self) -> float:
        """Returns the reward for the current state. Only meaningful for terminal states.
           - 1.0: Win for the player who just moved.
           - -1.0: Loss for the player who just moved (win for the current player).
           - 0.0: Draw or non-terminal state.
        """
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Serializes the game state to a dictionary for logging or transport."""
        pass
```

## Implementation Requirements for `chess_mcts.py`

- **Class**: `ChessGameState(GameStateBase)`
- **`__init__(self, fen: str = None)`**: Constructor.
- **`getCurrentPlayer()`**: Returns `int` (`1` or `-1`).
- **`getPossibleActions()`**: Returns `List[str]`, where each string is a UCI move.
- **`takeAction(action: str)`**: Takes a UCI move string and returns a new `ChessGameState`.
- **`isTerminal()`**: Returns `bool`.
- **`getReward()`**: Returns `float`.
- **`to_dict()`**: Returns `Dict[str, str]` (e.g., `{'fen': '...'}`).
