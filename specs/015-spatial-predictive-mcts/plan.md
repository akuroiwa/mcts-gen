# Implementation Plan: Spatial Partitioning and Predictive Search

**Branch**: `015-spatial-predictive-mcts` | **Date**: 2025-12-31 | **Spec**: [specs/015-spatial-predictive-mcts/spec.md](spec.md)

**Input**: Feature specification from `specs/015-spatial-predictive-mcts/spec.md`

## Technical Context

- **Ligand MCTS**: Current implementation builds molecules atom-by-atom or fragment-by-fragment. Points are derived from `pocket1_atm.pdb`.
- **Game Engine**: Shogi/Chess modules use `python-shogi` and `python-chess`.
- **Search Logic**: MCTS engine is generic; AI drives the loop.

### Unknowns & Research
- **Spatial Filtering**: How to efficiently restrict fragment placement to a specific coordinate box in `LigandState.legal_actions`?
- **State Forking**: How to initialize a "Parallel Reality" MCTS state for predictive search without corrupting the main game tree?
- **Result Consolidation**: Format for presenting partial results to the AI for merging.

## Constitution Check

| Principle | Status | Justification |
|-----------|--------|---------------|
| AI-Augmented UCT | PASS | Maintains the decoupled architecture. |
| Policy Pruning | PASS | Predictive search uses policy to select branches to pre-calculate. |
| Stateful Interaction | PASS | Server will manage multiple search contexts (predicted branches). |
| Spec-Driven Development | PASS | Following the Spec-Kit workflow. |

## Phases

### Phase 0: Research & Feasibility

1. **Research Task: Coordinate-based Action Pruning**
   - Goal: Determine how to filter `attach_idx` and `frag_smiles` placement based on pocket coordinates.
   - Outcome: `research.md` entry.
2. **Research Task: Predictive Branch Management**
   - Goal: Design the tool protocol for forking MCTS sessions (e.g., `predict_mcts_branch`).
   - Outcome: `research.md` entry.

### Phase 1: Design & Contracts

1. **Data Model (`data-model.md`)**:
   - `SpatialZone` definition (X/Y/Z min/max).
   - `PredictionContext` (predicted move, sub-tree reference).
2. **Contract Update (`contracts/`)**:
   - Update `reinitialize_mcts` to accept `spatial_filter`.
   - New tool: `start_predictive_search(move)`.
3. **Quickstart update**:
   - Document how to use spatial zones.

### Phase 2: Implementation

1. **Spatial Implementation**:
   - Update `Evaluator` to load coordinate data for filtering.
   - Update `LigandState.legal_actions` to prune moves outside the zone.
2. **Predictive Search Implementation**:
   - Update `AiGpSimulator` to support "Stashed" or "Named" MCTS instances.
   - Implement tool to switch context to a predicted state.

## Validation Plan

1. **Unit Test**: Initialize `LigandMCTS` with a tiny spatial zone and verify only 1-2 atoms are accessible.
2. **Integration Test**: Run predictive search on a Shogi board; simulate the opponent making the predicted move and verify the search tree is instantly available.
