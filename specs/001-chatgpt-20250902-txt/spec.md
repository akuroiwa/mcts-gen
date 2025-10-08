# Feature Specification: AI-Augmented UCT Framework

## 1. Overview
This document specifies an MCTS framework that uses a standard UCT algorithm augmented by an external AI agent. The AI enhances the search in three ways: providing value estimations, dynamically tuning the exploration constant, and pruning the action space using policy predictions. The architecture is designed for stability, performance, and maximum AI-driven flexibility.

## 2. Architecture

- **`AiGpSimulator` Class:** A stateful class that holds the MCTS engine and exposes its methods as MCP tools.
- **`McpMcts` Engine:** A UCT-based MCTS engine inheriting from `AntLionMcts`. It includes hooks for the AI to inject predictions.
- **AI Agent Roles:**
    1.  **Value Prediction:** The AI provides a value for a given state, which is used by the engine's `dl_method`, replacing random rollouts.
    2.  **Policy Pruning:** The AI receives the list of all possible actions from a node and returns a filtered, smaller list of promising actions. The engine only expands nodes from this filtered list.
    3.  **Exploration Strategy:** The AI generates and refines a strategy (e.g., a Python function) to determine the optimal `explorationConstant` for each search round.

## 3. Functional Requirements

- **FR-001 (Stateful Simulator):** The system MUST provide a single, long-lived `AiGpSimulator` instance whose methods are exposed as stateful MCP tools.
- **FR-002 (AI-driven Action Pruning):** The MCTS engine MUST accept a pre-filtered list of actions from the AI agent (via the `run_mcts_round` tool) to use for node expansion.
- **FR-003 (Action List Provider):** The system MUST provide a tool (`get_possible_actions`) for the AI to retrieve the full list of legal moves for the current state before it performs pruning.
- **FR-004 (AI-driven Value Prediction):** The engine's `dl_method` MUST be overridden to use the value provided by the AI agent.
- **FR-005 (AI-driven Exploration):** The AI agent MUST be responsible for determining the `explorationConstant` for each search round.
- **FR-006 (Serializable Actions):** The `getPossibleActions` method of any `GameStateBase` implementation MUST return a list of serializable, human-readable strings (e.g., USI) to enable processing by the AI agent.