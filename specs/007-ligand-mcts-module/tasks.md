# Tasks for: Develop ligand_mcts.py

This document outlines the development tasks required to implement the `ligand_mcts.py` game module. The tasks are organized into logical phases to ensure a smooth, dependency-ordered implementation.

## Phase 1: Setup

- [x] T001 Create the new Python module file `src/mcts_gen/games/ligand_mcts.py` and add the necessary initial imports (`dataclasses`, `typing`, `numpy`, `rdkit`, etc.) and placeholder class definitions.

## Phase 2: Foundational Logic

This phase implements the core components for representing and evaluating molecules, independent of the `mcts-gen` game state interface. All tasks in this phase pertain to `src/mcts_gen/games/ligand_mcts.py`.

- [x] T002 [P] Implement the `LigandAction` data class for representing molecular modification actions.
- [x] T003 [P] Implement the `LigandState` data class to hold the current molecule and its history.
- [x] T004 Implement the molecule-to-point-cloud conversion utility (`mol_to_points`) and pocket loading utility (`load_pocket_atm_pdb`).
- [x] T005 Implement the `Evaluator` class skeleton and its `__init__` method.
- [x] T006 Implement the shape-scoring methods (`usr_descriptor`, `gaussian_overlap`) within the `Evaluator` class.
- [x] T007 Implement the chemical property scoring methods (`total_score`) in the `Evaluator` class to calculate a weighted score including MolLogP, QED, and penalties.
- [x] T008 Implement the core logic for the `LigandState` class methods: `clone`, `apply_action`, `legal_actions`, and `is_terminal`.

## Phase 3: GameState Integration

This phase connects the foundational logic to the `mcts-gen` framework by implementing the `GameStateBase` interface. All tasks in this phase pertain to `src/mcts_gen/games/ligand_mcts.py`.

- [x] T009 Implement the `LigandMCTSGameState` class, ensuring it inherits from `mcts_gen.models.game_state.GameStateBase`.
- [x] T010 Implement the `__init__` method for `LigandMCTSGameState`, correctly initializing the `Evaluator` and the initial `LigandState`.
- [x] T011 Implement the `getCurrentPlayer` and `isTerminal` methods for `LigandMCTSGameState`, delegating logic to the internal `LigandState` where appropriate.
- [x] T012 Implement the `getPossibleActions` method for `LigandMCTSGameState`.
- [x] T013 Implement the `takeAction` method for `LigandMCTSGameState`, ensuring it returns a new instance of `LigandMCTSGameState`.
- [x] T014 Implement the `getReward` method for `LigandMCTSGameState`, which uses the `Evaluator` to return a score for a terminal state.

## Phase 4: Testing

- [x] T015 Create the unit test file `tests/unit/test_ligand_mcts.py`.
- [x] T016 [P] In `tests/unit/test_ligand_mcts.py`, write unit tests for the `Evaluator` class to verify that MolLogP, QED, and penalty calculations are correct for known molecules.
- [x] T017 [P] In `tests/unit/test_ligand_mcts.py`, write unit tests for the `LigandState` and `LigandAction` classes.
- [x] T018 In `tests/unit/test_ligand_mcts.py`, write unit tests for `LigandMCTSGameState` to confirm its methods (`takeAction`, `isTerminal`, etc.) behave as expected and correctly implement the `GameStateBase` contract.
- [x] T019 Create the integration test file `tests/integration/test_ligand_mcts_integration.py`.
- [x] T020 In `tests/integration/test_ligand_mcts_integration.py`, write an integration test that dynamically loads the `ligand_mcts` module via `importlib` and runs a small MCTS simulation to ensure it integrates with the engine correctly.

## Phase 5: Polish & Documentation

- [x] T021 Add comprehensive docstrings, comments, and type hints to all new classes and methods in `src/mcts_gen/games/ligand_mcts.py`.
- [x] T022 Investigate the `docs/` directory to find the appropriate file to update with information about the new ligand generation feature, and add a section that introduces the feature and links to the `quickstart.md` guide.

## Dependencies
- **Phase 2** depends on **Phase 1**.
- **Phase 3** depends on **Phase 2**.
- **Phase 4** depends on **Phase 3**.
- **Phase 5** depends on **Phase 3** and can be done in parallel with **Phase 4**.

## Parallel Execution
- Within Phase 2, `LigandAction` (T002) and `LigandState` (T003) can be developed in parallel.
- Within Phase 4, unit tests for different components (T016, T017) can be written in parallel.

## Implementation Strategy
The implementation will follow the phases outlined above. Each phase builds upon the previous one, starting with the core data structures and logic, followed by integration with the framework, and finally testing and documentation. This ensures a solid foundation before connecting the module to the rest of the system. The MVP is the completion of Phase 3, which delivers a functional, loadable game module.
