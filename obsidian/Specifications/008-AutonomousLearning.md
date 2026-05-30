# Spec-008: Autonomous Initialization Learning

## Goal
Allow AI agents to autonomously discover how to initialize any game by inspecting its source code and docstrings.

## User Scenarios
- **Unknown Game**: AI identifies `GameState` class and its `__init__` arguments (name, type, description) automatically.
- **Complex Arguments**: AI prompts user for required inputs (like `pocket_path`) before calling `reinitialize_mcts`.

## Requirements
- Updated `mcts_autonomous_search` prompt to include an **Investigation Phase**.
- Agent MUST read `*_mcts.py` files to identify initialization logic.
- Agent MUST use `reinitialize_mcts` with discovered `state_module`, `state_class`, and `state_kwargs`.

## Current Status
- Prompt refined to ensure sequential tool calls.
- Successfully verified with `ligand_mcts.py` initialization.
