# Tasks: Spatial Partitioning and Predictive Search

## Phase 1: Setup

- [x] T001 Initialize Task 015 environment and verify Spec-Kit configuration

## Phase 2: Foundational Tasks

- [x] T002 Implement `SpatialZone` data structure in `src/mcts_gen/models/spatial.py`
- [x] T003 Implement `MctsSlot` management logic in `src/mcts_gen/services/slot_manager.py`
- [x] T004 Update `Evaluator` to support optional coordinate loading in `src/mcts_gen/games/ligand_mcts.py`

## Phase 3: [US1] Focused Pocket Exploration

**Goal**: Restrict ligand growth to a specific coordinate box within the binding pocket.

- [x] T005 [P] [US1] Implement `bounding_box` filtering logic in `src/mcts_gen/games/ligand_mcts.py`
- [x] T006 [US1] Update `LigandState.legal_actions` to prune attachment points outside the `SpatialZone` in `src/mcts_gen/games/ligand_mcts.py`
- [x] T007 [US1] Update `reinitialize_mcts` to accept and apply `spatial_filter` in `src/mcts_gen/services/ai_gp_simulator.py`

## Phase 4: [US2] Predictive Game Advantage

**Goal**: Pre-calculate MCTS trees for likely future board states using slots.

- [x] T008 [P] [US2] Extend `AiGpSimulator` to support multiple named MCTS engines (slots) in `src/mcts_gen/services/ai_gp_simulator.py`
- [x] T009 [US2] Implement `activate_mcts_slot` tool to swap active search context in `src/mcts_gen/services/ai_gp_simulator.py`
- [x] T010 [US2] Implement `list_mcts_slots` tool in `src/mcts_gen/services/ai_gp_simulator.py`

## Phase 5: [US3] Results Consolidation

**Goal**: Provide a mechanism for the AI to view and merge results from different zones.

- [x] T011 [US3] Enhance `get_principal_variation` to include spatial zone metadata in `src/mcts_gen/services/ai_gp_simulator.py`
- [x] T012 [US3] Implement a summary tool for multi-slot results in `src/mcts_gen/services/ai_gp_simulator.py`

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T013 Update AI prompt in `src/mcts_gen/fastmcp_server.py` to guide the use of slots and spatial zones
- [x] T014 [P] Update Sphinx documentation in `docs/quickstart.rst` and translate to Japanese
- [ ] T015 Final integration test using 8c7y pocket partitioning and predictive Chess branches

## Implementation Strategy

1. **MVP**: Implement User Story 1 (Spatial Partitioning) first, as it directly solves the search space explosion issue in ligand generation.
2. **Incremental**: Add Slot management and User Story 2 (Predictive Search).
3. **Refine**: Implement consolidation tools and finalize documentation.
