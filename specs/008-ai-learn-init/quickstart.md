# Quickstart

**Feature**: Allowing AI agents to autonomously learn how to initialize new games.

This feature simplifies the process of running simulations for new games.

## New Agent Behavior

When an AI agent is tasked with running a simulation for a game (e.g., "start a checkers simulation"), it will now perform the following steps autonomously:

1.  **Investigate**: The agent will locate the corresponding game module file (e.g., `src/mcts_gen/games/checkers_mcts.py`).
2.  **Analyze**: It will read the file to find the `GameState` class and analyze its `__init__` constructor to identify any required arguments.
3.  **Request Information (if needed)**: If the game requires specific arguments for initialization (like a file path), the agent will prompt the user to provide them.
4.  **Initialize**: The agent will then automatically call the MCTS simulation with the correct parameters.

There are no new commands for the user. The AI agent's underlying process has simply become more intelligent and autonomous, requiring less explicit guidance.
