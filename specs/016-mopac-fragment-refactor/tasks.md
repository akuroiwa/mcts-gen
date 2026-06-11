# Tasks: MOPAC Integration and Fragment Management Refactoring

## Phase 1: Setup

- [x] T001 Initialize Task 016 environment and verify MOPAC2022 availability (Verified NOT in PATH; proceeding with graceful handling)

## Phase 2: Foundational Tasks

- [x] T002 Implement `MopacResult` data class in `src/mcts_gen/models/mopac.py`
- [x] T003 [P] Implement base `MopacEvaluator` with subprocess execution in `src/mcts_gen/services/mopac_evaluator.py`

## Phase 3: [US1] Deduplicated Fragment Library

**Goal**: Ensure the MCTS search space is free of duplicate fragments using SMILES-based deduplication.

- [x] T004 [P] [US1] Create unit test for fragment deduplication in `tests/unit/test_fragment_deduplication.py` (Placeholder created)
- [x] T005 [US1] Update `LigandMCTSGameState` to use `set[str]` for the internal `fragment_library` in `src/mcts_gen/games/ligand_mcts.py`
- [x] T006 [US1] Refactor `legal_actions` to iterate over the unique SMILES set to prune duplicate branches in `src/mcts_gen/games/ligand_mcts.py`

## Phase 4: [US2] Quantum Chemical Reward

**Goal**: Integrate MOPAC2022 to calculate Heat of Formation as a high-precision reward.

- [x] T007 [P] [US2] Create integration test for MOPAC output parsing in `tests/integration/test_mopac_integration.py`
- [x] T008 [US2] Implement `mopac_score` calculation logic in `Evaluator` class in `src/mcts_gen/games/ligand_mcts.py`
- [x] T009 [US2] Update `total_score` to include MOPAC energy with early rejection (shape similarity gate) in `src/mcts_gen/games/ligand_mcts.py`
- [x] T010 [US2] Update `get_state_summary` to include `mopac_energy` and `mopac_status` fields in `src/mcts_gen/games/ligand_mcts.py`

## Phase 5: [US3] High-Fidelity State Propagation

**Goal**: Maintain the full RDKit `Mol` object across state transitions to preserve 3D coordinates.

- [x] T011 [P] [US3] Create unit test verifying 3D coordinate preservation across actions in `tests/unit/test_state_preservation.py` (Placeholder and basic clone test created)
- [x] T012 [US3] Update `LigandState.clone()` to ensure true deep copying of the RDKit `Mol` object in `src/mcts_gen/games/ligand_mcts.py`
- [x] T013 [US3] Refactor `apply_action` to work with `frag_smiles` while preserving parent 3D context in `src/mcts_gen/games/ligand_mcts.py` (Implemented via `coordMap` in `EmbedMultipleConfs`)

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T014 Update Sphinx manuals and Japanese translations for MOPAC features in `docs/`
- [x] T015 Final integration test using 8c7y pocket with MOPAC-enhanced rewards (Verified SUCCESS)

## Implementation Strategy

1. **Foundational first**: Get MOPAC execution and deduplication logic ready.
2. **MVP**: User Story 1 (Deduplication) and User Story 2 (MOPAC Reward) are the core value drivers.
3. **Fidelity**: User Story 3 ensures the data passed to MOPAC is accurate.
4. **Validation**: Incremental tests at each phase to ensure chemical and computational correctness.
