# Feature Specification: Allowing AI agents to autonomously learn how to initialize new games.

**Feature Branch**: `008-ai-learn-init`  
**Created**: 2025年12月3日水曜日  
**Status**: Draft  
**Input**: User description: "Allowing AI agents to autonomously learn how to initialize new games."

## User Scenarios & Testing (mandatory)

### User Story 1 - Initializing a New, Unknown Game (Priority: P1)

An AI agent (like myself) is tasked with running a simulation for a new game it has never seen before. The agent should be able to figure out how to start the simulation without needing explicit, hard-coded instructions for that specific game.

**Why this priority**: This is the core functionality of the feature, enabling the AI agent to adapt to new games autonomously, reducing the need for manual configuration or explicit instructions for every new game.

**Independent Test**: Can be fully tested by adding a new game module (e.g., `checkers_mcts.py` with a simple `GameState` constructor) and tasking the AI agent to initialize a simulation for it. Success is measured by the agent correctly calling `reinitialize_mcts` without needing prior knowledge or manual intervention.

**Acceptance Scenarios**:

1.  **Given** a new game module (e.g., `checkers_mcts.py`) has been added to the `src/mcts_gen/games/` directory.
2.  **And** the AI agent has been tasked to run a simulation for "checkers".
3.  **When** the agent processes this request.
4.  **Then** the agent should automatically inspect the `src/mcts_gen/games/checkers_mcts.py` file.
5.  **And** the agent should identify the `GameState` implementation class (e.g., `CheckersGameState`).
6.  **And** the agent should determine from its `__init__` method that no special arguments are needed (or identify what is needed if the constructor has arguments).
7.  **And** the agent should successfully call the `reinitialize_mcts` tool with the correct `state_module` and `state_class` without errors.

---

### User Story 2 - Initializing a Game with Complex Arguments (Priority: P1)

An AI agent is tasked with running a simulation for a game (like `ligand_mcts`) that requires specific arguments for initialization. The agent should be able to identify these arguments by inspecting the game module and then prompt the user to provide them.

**Why this priority**: This covers the more complex but common scenario where games require specific data or configurations for initialization, ensuring the agent can handle diverse game setups while maintaining autonomy.

**Independent Test**: Can be fully tested by tasking the AI agent to initialize a simulation for the `ligand` game. Success is measured by the agent correctly identifying the `pocket_path` argument, prompting the user for it, and then successfully calling `reinitialize_mcts` once the path is provided.

**Acceptance Scenarios**:

1.  **Given** the existing `ligand_mcts.py` module, which requires a `pocket_path` argument.
2.  **And** the AI agent is tasked to run a simulation for "ligand".
3.  **When** the agent processes this request.
4.  **Then** the agent should automatically inspect `src/mcts_gen/games/ligand_mcts.py`.
5.  **And** it should identify from the `LigandMCTSGameState.__init__` docstring and signature that a `pocket_path` string argument is required.
6.  **And** the agent should then ask the user to provide the path to the required `pocket_path` file before calling `reinitialize_mcts`.

---

### Edge Cases

-   What happens when the requested game module (`*_mcts.py`) does not exist? The agent should report an error to the user.
-   How does the system handle a `GameState` class that does not have type hints or a docstring for its `__init__` method? The agent should attempt to make a best guess based on parameter names or report to the user that it needs clarification.
-   What happens if multiple classes inherit from `GameStateBase` in a single game module? The agent should select the primary one (e.g., the one defined last or with a specific naming convention) or ask for clarification.

## Requirements (mandatory)

### Functional Requirements

-   **FR-001**: The `mcts_autonomous_search` prompt, defined in `src/mcts_gen/fastmcp_server.py`, MUST be updated to include instructions for the AI agent to perform an investigation phase before attempting to initialize a simulation.
-   **FR-002**: The investigation instructions MUST direct the agent to locate and read the relevant `*_mcts.py` file within the `src/mcts_gen/games/` directory based on the requested game.
-   **FR-003**: The instructions MUST guide the agent to identify the class that inherits from `GameStateBase` within the located game module.
-   **FR-004**: The instructions MUST require the agent to analyze the `__init__` method signature and docstring of the identified `GameState` class to determine the required constructor arguments (name, type, and description).
-   **FR-005**: If required arguments are discovered, the prompt should guide the agent to request these from the user before proceeding with initialization.
-   **FR-006**: The final step in the prompt's workflow MUST be to call the `reinitialize_mcts` tool with the discovered `state_module`, `state_class`, and any necessary `state_kwargs`.

### Key Entities

-   **AI Agent**: The language model interacting with the `mcts-gen` framework.
-   **`mcts_autonomous_search` prompt**: The set of system instructions defining the agent's behavior.
-   **Game Module (`*_mcts.py`)**: A Python file defining the rules and state for a specific game.
-   **`GameStateBase` subclass**: The specific class within a game module that implements the game's logic.
-   **`__init__` method**: The constructor for the `GameState` class, whose signature and docstring are the target of the agent's investigation.

## Success Criteria (mandatory)

### Measurable Outcomes

-   **SC-001**: When tasked with starting a new game (e.g., "checkers") that requires no special `__init__` arguments, the AI agent successfully calls `reinitialize_mcts` without asking the user for any input.
-   **SC-002**: When tasked with starting the `ligand` game, the AI agent correctly identifies the need for the `pocket_path` argument and prompts the user for it before calling `reinitialize_mcts`.
-   **SC-003**: The agent's reliability in correctly identifying initialization arguments for any new, properly-formatted game module is >95%.
-   **SC-004**: The overall time-to-initialization for a new game is reduced, as the user no longer needs to manually instruct the agent on game-specific requirements.