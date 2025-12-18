# Quickstart for Rich Game Summaries (PGN/KIF)

This guide explains how to use the `get_principal_variation` tool to retrieve a full game history in PGN (for Chess) or KIF (for Shogi) format.

## Prerequisites
- The `mcts-gen` environment is set up.
- The simulation server is running.

## Usage

The `get_state_summary()` method is called automatically by the existing `get_principal_variation` tool. The summary is included in the tool's output.

### 1. Run a Chess Simulation and Get PGN

To get a PGN summary for a chess game:

1.  **Initialize a Chess MCTS simulation.**
    ```json
    {
      "tool": "reinitialize_mcts",
      "state_module": "mcts_gen.games.chess_mcts",
      "state_class": "ChessGameState"
    }
    ```

2.  **Run one or more MCTS rounds.**
    ```json
    {
      "tool": "run_mcts_round",
      "exploration_constant": 1.41
    }
    ```

3.  **Call `get_principal_variation`**.
    ```json
    {
      "tool": "get_principal_variation"
    }
    ```

4.  **Inspect the output.** The result will contain the principal variation path and a `final_state_summary` with the PGN.

    **Example Output:**
    ```json
    {
      "principal_variation": [
        "e2e4",
        "e7e5",
        "g1f3"
      ],
      "final_state_summary": {
        "pgn": "[Event \"?\"]\n[Site \"?\"]\n[Date \"????.??.??\"]\n[Round \"?\"]\n[White \"?\"]\n[Black \"?\"]\n[Result \"*"]\n\n1. e4 e5 2. Nf3 *"
      }
    }
    ```

### 2. Run a Shogi Simulation and Get KIF

To get a KIF summary for a shogi game:

1.  **Initialize a Shogi MCTS simulation.**
    ```json
    {
      "tool": "reinitialize_mcts",
      "state_module": "mcts_gen.games.shogi_mcts",
      "state_class": "ShogiGameState"
    }
    ```

2.  **Run MCTS rounds** as needed.

3.  **Call `get_principal_variation`**.

4.  **Inspect the output.** The result will contain the `final_state_summary` with the KIF record.

    **Example Output:**
    ```json
    {
      "principal_variation": [
        "7g7f",
        "3c3d"
      ],
      "final_state_summary": {
        "kif": "手合割：平手\n先手：\n後手：\n\n1 ７六歩(77)\n2 ３四歩(33)\nまで2手で中断"
      }
    }
    ```

