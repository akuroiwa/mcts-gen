---
description: "Task list for implementing the external molecule source feature"
---

# Tasks: The list of molecules that are the raw materials for chemical fragments is stored as an external file, increasing the extensibility of the module.

**Input**: Design documents from `/specs/009-external-molecule-source/`
**Prerequisites**: plan.md, spec.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1)
- Include exact file paths in descriptions

## Path Conventions

- Paths shown below assume a single project structure (`src/`, `tests/`) as defined in `plan.md`.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Configure project dependencies.

- [x] T001 Add `rdkit` as a dependency in `pyproject.toml`.

---

## Phase 2: User Story 1 - Support ligand generation from an external source molecule file (Priority: P1) 🎯 MVP

**Goal**: Allow `LigandMCTSGameState` to initialize its fragment library from a user-provided file of molecules instead of a hard-coded list.

**Independent Test**: Initialize a `ligand_mcts` simulation using the `source_molecule_path` argument pointing to a test `.smi` file. Verify that the simulation starts and that `getPossibleActions` returns actions derived from the molecules in the file.

### Tests for User Story 1 ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T002 [US1] Create a test data directory `tests/unit/test_data/` and a test SMILES file `tests/unit/test_data/molecules.smi`.
- [x] T003 [P] [US1] Add a unit test to `tests/unit/test_ligand_mcts.py` to verify successful initialization when a valid `source_molecule_path` is provided.
- [x] T004 [P] [US1] Add unit tests to `tests/unit/test_ligand_mcts.py` to verify correct molecule parsing from different file formats (.smi, .sdf, .csv).
- [x] T005 [P] [US1] Add a unit test to `tests/unit/test_ligand_mcts.py` for error handling when the provided `source_molecule_path` is invalid or the file is malformed.
- [x] T006 [P] [US1] Add a unit test to `tests/unit/test_ligand_mcts.py` to confirm that the BRICS fragmentation logic produces a non-empty set of fragments from valid source molecules.

### Implementation for User Story 1

- [x] T007 [US1] Modify `LigandMCTSGameState.__init__` in `src/mcts_gen/games/ligand_mcts.py` to accept an optional `source_molecule_path` argument.
- [x] T008 [P] [US1] Implement a private helper function `_load_molecules_from_file` in `src/mcts_gen/games/ligand_mcts.py` to handle file reading and format detection for `.smi`, `.sdf`, and `.csv` files.
- [x] T009 [P] [US1] Implement a private helper function `_generate_fragments_from_molecules` in `src/mcts_gen/games/ligand_mcts.py` that uses RDKit's BRICS algorithm to fragment molecules.
- [x] T010 [US1] In `LigandMCTSGameState.__init__`, call the new helper functions to load molecules and generate fragments when `source_molecule_path` is provided in `src/mcts_gen/games/ligand_mcts.py`.
- [x] T011 [US1] Modify the logic in `LigandMCTSGameState` to use the dynamically generated fragment library instead of any hard-coded list in `src/mcts_gen/games/ligand_mcts.py`.
- [x] T012 [US1] Remove the old hard-coded fragment list and associated logic from `src/mcts_gen/games/ligand_mcts.py`.
- [x] T013 [US1] Implement clear error handling (e.g., raising `ValueError` or `FileNotFoundError`) within the initialization process in `src/mcts_gen/games/ligand_mcts.py`.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 3: Polish & Cross-Cutting Concerns

**Purpose**: Final documentation and validation.

- [x] T014 [P] Update documentation (e.g., `README.md` or `docs/quickstart.rst`) with instructions on how to use the new `source_molecule_path` feature.
- [x] T015 Validate the feature by following the steps outlined in `specs/009-external-molecule-source/quickstart.md`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **User Story 1 (Phase 2)**: Depends on Setup completion.
- **Polish (Phase 3)**: Depends on User Story 1 completion.

### Within User Story 1

- Tests (T002-T006) should be implemented first.
- The `__init__` method modification (T007) is the entry point for the new logic.
- Helper function implementation (T008, T009) can be done in parallel.
- Integration (T010) and using the new library (T011) follow the implementation of helper functions.
- Cleanup (T012) should happen after the new mechanism is confirmed to work.

### Parallel Opportunities

- Within US1, test creation tasks (T003-T006) can be developed in parallel.
- The two helper function implementations (T008, T009) can be done in parallel.
- The documentation update (T014) can be worked on in parallel with implementation once the API is stable.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1.  Complete Phase 1: Setup (T001).
2.  Complete Phase 2: User Story 1 (T002-T013).
3.  **STOP and VALIDATE**: Run all tests for User Story 1 and confirm they pass. Manually test the scenario described in `quickstart.md`.
4.  Complete Phase 3: Polish (T014-T015).
5.  Deploy/demo the feature.

---
