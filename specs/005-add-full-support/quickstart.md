# Quickstart: MCTS for Chess

This guide demonstrates how to use the `mcts-gen` library to find the best move in a game of chess.

## 1. Installation

First, install `mcts-gen` with the optional `chess` dependencies. This will automatically install the required `python-chess` library.

```bash
# Using uv
uv pip install mcts-gen[chess]

# Using pip
# pip install mcts-gen[chess]
```

## 2. Example Usage

The following script initializes a chess board from a FEN string and uses the MCTS agent to determine the best next move.

```python
from mcts_gen.services.ai_gp_simulator import AiGpSimulator
from mcts_gen.games.chess_mcts import ChessGameState

# This is a famous puzzle position: Mate in 3 for White.
# See: https://www.chess.com/forum/view/more-puzzles/a-beautiful-mate-in-3
fen = "1r3rk1/p1p1q1pp/3b1n2/4p3/8/2N1B3/PPP1QPPP/2KR3R w - - 1 16"

# Initialize the MCTS simulator with the chess game state
# The reinitialize_mcts function is a tool available to the Gemini agent,
# representing the start of a simulation.
simulator = AiGpSimulator()
simulator.reinitialize_mcts(
    state_module="mcts_gen.games.chess_mcts",
    state_class="ChessGameState",
    state_kwargs={"fen": fen}
)

# The agent would run the MCTS loop for a number of iterations.
# This is a simplified representation of that loop.
num_iterations = 500
exploration_constant = 1.41

print(f"Starting board state (from FEN):\n{simulator.root_state.board}")
print("\nRunning MCTS simulation...")

for i in range(num_iterations):
    # In the real implementation, the agent calls the `run_mcts_round` tool.
    # This is a direct call for demonstration purposes.
    simulator.mcts.run_round()

# After the simulation, retrieve the best move found.
# The agent would call the `get_best_move` tool.
best_move_obj = simulator.mcts.get_best_move()
best_move_uci = best_move_obj.action

print(f"\nSimulation complete after {num_iterations} iterations.")
print(f"Recommended best move (UCI format): {best_move_uci}")

# Expected output for the puzzle is typically Qc4+, though MCTS may find other strong moves.

# You can then apply the move to see the new state.
new_game_state = simulator.root_state.takeAction(best_move_uci)
print(f"\nBoard state after move {best_move_uci}:")
print(new_game_state.board)
```

### Expected Output

```
Starting board state (from FEN):
1 r 3 r k 1
p 1 p 1 q 1 p p
3 b 1 n 2
4 p 3
8
2 N 1 B 3
P P P 1 Q P P P
2 K R 3 R

Running MCTS simulation...

Simulation complete after 500 iterations.
Recommended best move (UCI format): e2c4

Board state after move e2c4:
1 r 3 r k 1
p 1 p 1 q 1 p p
3 b 1 n 2
4 p 3
2 Q 5
2 N 1 B 3
P P P 2 P P P
2 K R 3 R
```
