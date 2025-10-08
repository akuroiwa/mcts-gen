# Implementation Plan: AI-Augmented UCT Framework

**Branch**: `007-policy-pruning` | **Date**: 2025-09-29 | **Spec**: [spec.md](./spec.md)

## Summary
This plan details the implementation of the "AI-Augmented UCT" architecture. Instead of implementing the complex PUCT formula, this approach enhances the standard UCT search by using the AI's policy prediction to prune the action space *before* expansion. This provides a stable, performant, and highly flexible framework for AI-driven search.

## Technical Approach

- **`McpMcts` Engine:** The engine will inherit from `AntLionMcts`. Its `expand` method will be modified to accept and use a pre-filtered list of actions provided by the AI.
- **`AiGpSimulator` Class:** This stateful class will wrap the `McpMcts` engine. Its `run_mcts_round` tool will be the primary interface for the AI, accepting the `explorationConstant` and the pruned `actions_to_expand` list.
- **`fastmcp_server.py`:** A minimal server script will instantiate the `AiGpSimulator` and register its methods as tools.
- **AI Workflow (`AGENTS.md`):** The agent's instructions will define the three-step process for each move: 1) Call `get_possible_actions`. 2) Use its policy model to filter this list down to promising candidates. 3) Call `run_mcts_round` with the filtered list to execute the search.

## Phase 4: Post-Implementation Documentation
- A research paper will be written to document the project's findings, focusing on the novel "Policy Pruning" approach as an alternative to PUCT.