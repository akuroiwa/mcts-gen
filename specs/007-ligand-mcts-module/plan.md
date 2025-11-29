# Implementation Plan: Develop ligand_mcts.py

## 1. Technical Context
This feature will be implemented by creating a new, self-contained Python module at `src/mcts_gen/games/ligand_mcts.py`. This module will define a `LigandMCTSGameState` class that conforms to the `GameStateBase` abstract base class, allowing it to be dynamically loaded by the existing `AiGpSimulator` service without any modifications to the core `mcts-gen` framework.

The module will encapsulate all logic for de novo ligand generation, including state representation (the molecule being built), action definition (adding fragments), and reward calculation. The reward calculation will be handled by an internal `Evaluator` class that scores molecules based on shape complementarity to a user-provided protein pocket, hydrophobicity (MolLogP), and druglikeness (QED).

Dependencies on `rdkit-pypi`, `scipy`, and `numpy` are required for cheminformatics calculations and are expected to be installed by the end-user, as per the project's pattern for optional game-specific dependencies.

## 2. Constitution Check
- **Modularity**: The plan adheres to this principle by creating a new, decoupled game module. The module is self-contained and does not require changes to the core application logic.
- **Testability**: The `LigandMCTSGameState` class will be a pure class that can be instantiated and tested independently. Its inputs (actions) and outputs (new states, rewards) are well-defined, facilitating unit testing.
- **Clarity**: The implementation will be clearly separated into `GameState` logic, `Action` definitions, and the `Evaluator`, making the code easy to understand and maintain.
- **Extensibility**: The `Evaluator` class is designed to be easily extensible with new scoring functions in the future.

*Note: The constitution file at `.specify/memory/constitution.md` was not accessible. The check was performed against standard software engineering best practices, which the plan fully adheres to.*

## 3. Implementation Phases

### Phase 0: Research
No significant research is required as the technical path is clear. The `research.md` file will document the decisions to use `rdkit-pypi` for chemical property calculations and to rely on the existing `importlib`-based dynamic loading mechanism.

### Phase 1: Design and Contracts
- **Data Model (`data-model.md`):** Define the structure and attributes of the key Python classes: `LigandMCTSGameState`, `LigandAction`, `LigandState` (internal representation of the molecule), and `Evaluator`.
- **Contracts (`contracts/game_module_interface.md`):** Document how `LigandMCTSGameState` fulfills the public contract defined by the `GameStateBase` abstract class. No API (e.g., OpenAPI) contract is needed as this is a Python library module.
- **Quickstart (`quickstart.md`):** Provide a user guide that explains:
    1.  How to install the required dependencies (`rdkit-pypi`, `scipy`, `numpy`, `fpocket`).
    2.  How to use `fpocket` to generate the necessary input file.
    3.  A code example demonstrating how to invoke the simulation via the AI agent, specifying the correct `state_module`, `state_class`, and `state_kwargs`.

### Phase 2: Implementation (Task Breakdown)
The detailed task breakdown will be generated in the next step (`/speckit.tasks`). High-level tasks will include:
1.  Implement the `Evaluator` class with shape, MolLogP, and QED scoring.
2.  Implement the `LigandAction` and `LigandState` data classes.
3.  Implement the `LigandMCTSGameState` class, ensuring it correctly implements the `GameStateBase` interface.
4.  Write unit tests for the `Evaluator` and `LigandMCTSGameState`.
5.  Write an integration test to ensure the module can be loaded and run by the `mcts-gen` engine.

## 4. Testing Strategy
- **Unit Tests:**
    - Test the `Evaluator` class with known molecules to ensure scoring functions (MolLogP, QED, penalties) return expected values.
    - Test the `LigandMCTSGameState` methods:
        - `takeAction`: Ensure it correctly applies an action and returns a new state.
        - `isTerminal`: Verify terminal conditions (e.g., molecule size).
        - `getReward`: Ensure it returns a float value from the evaluator.
- **Integration Tests:**
    - Create a test that mimics `AiGpSimulator`, dynamically loading the `ligand_mcts` module and running a few MCTS rounds to ensure it integrates with the MCTS engine without errors.
- **Contract Tests:**
    - The unit tests for `LigandMCTSGameState` effectively serve as contract tests, ensuring the `GameStateBase` interface is correctly implemented.