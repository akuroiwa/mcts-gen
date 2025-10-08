# Data Models

This document defines the key data structures and entities for the Generic MCTS Framework.

## 1. GameState (Abstract)

Represents the state of a game. This is an abstract concept that will be implemented for each specific game by inheriting from `GameStateBase`.

- **Type**: Abstract Base Class (`abc.ABC`)
- **Key Methods**:
  - `getCurrentPlayer() -> int`: Returns the current player (e.g., +1 or -1).
  - `getPossibleActions() -> List[Any]`: Returns a list of legal moves from the current state.
  - `takeAction(action: Any) -> GameState`: Returns the new state after taking an action.
  - `isTerminal() -> bool`: Returns true if the game is over.
  - `getReward() -> float`: Returns the final reward for the terminal state (+1 for win, -1 for loss, 0 for draw).

## 2. MCTS Node

A node within the Monte Carlo Search Tree.

- **Type**: Class
- **Attributes**:
  - `state: GameState`: The game state this node represents.
  - `parent: MCTSNode | None`: The parent node in the tree.
  - `children: Dict[Any, MCTSNode]`: A dictionary mapping actions to child nodes.
  - `visit_count: int`: The number of times this node has been visited during search.
  - `total_reward: float`: The sum of rewards backpropagated through this node.
  - `prior_probability: float`: The prior probability of selecting this node, as determined by the policy network.

## 3. Policy

A probability distribution over possible moves from a state, as predicted by the AI.

- **Type**: `Dict[str, float]`
- **Description**: A dictionary where keys are the string representation of legal moves and values are their corresponding probabilities. The server is responsible for ensuring the probabilities for legal moves sum to 1.
- **Example**: `{"e2e4": 0.6, "d2d4": 0.4}`

## 4. Value

A scalar value representing the predicted outcome of the game from a given state.

- **Type**: `float`
- **Description**: A single floating-point number in the range [-1.0, 1.0], where +1.0 represents a certain win for the current player and -1.0 represents a certain loss.

## 5. Training Log Entry

A single data point generated from one step of a self-play game, used for training the AI model.

- **Type**: JSON Object
- **Format**: Stored as a single line in a `.jsonl` file.
- **Attributes**:
  - `state: str`: A string representation of the game state (e.g., a JSON array of the board).
  - `policy: Dict[str, float]`: The target policy distribution, derived from the MCTS visit counts for each action at this state.
  - `reward: float`: The final outcome of the game (+1, -1, or 0), applied to every entry for that game.
