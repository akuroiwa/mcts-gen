# Implementation Plan: MOPAC Integration and Fragment Management

**Branch**: `016-mopac-fragment-refactor` | **Date**: 2025-12-31 | **Spec**: [specs/016-mopac-fragment-refactor/spec.md](spec.md)

**Input**: Feature specification from `specs/016-mopac-fragment-refactor/spec.md`

## Summary
Integrate MOPAC2022 for high-precision reward calculation (Heat of Formation) and refactor `ligand_mcts.py` to use a hybrid SMILES-Mol management system. This ensures a deduplicated search space and high-fidelity 3D state propagation.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: RDKit (2023.x+), MOPAC2022 (external), pandas, fastmcp

**Storage**: Local filesystem for temporary MOPAC input/output files.

**Testing**: pytest (unit and integration tests)

## Constitution Check

| Principle | Status | Justification |
|-----------|--------|---------------|
| AI-Augmented UCT | PASS | AI continues to drive the simulation loop. |
| Policy Pruning | PASS | Deduplication ensures the agent works on unique branches. |
| Stateful Interaction | PASS | RDKit Mol objects preserved within the state. |
| Spec-Driven Development | PASS | Following the Spec-Kit workflow. |

## Phases

### Phase 0: Research & Feasibility (COMPLETED)
- Decisions documented in [research.md](research.md).
- Confirmed MOPAC execution via `1SCF` PM7.
- Confirmed SMILES-based deduplication strategy.

### Phase 1: Design & Contracts (COMPLETED)
- Data model in [data-model.md](data-model.md).
- Contract updates in [contracts/tools.md](contracts/tools.md).

### Phase 2: Implementation

1. **Refactor `LigandAction` and Library**:
   - Change `fragment_library` from `List[str]` to `set[str]` in `LigandMCTSGameState`.
   - Update `legal_actions` to iterate over the unique SMILES set.
2. **State Propagation Refactor**:
   - Ensure `LigandState.clone()` creates a true deep copy of the RDKit `Mol` object.
   - Update `apply_action` to work with `frag_smiles`.
3. **MOPAC Integration**:
   - Implement `MopacEvaluator` class in `src/mcts_gen/services/mopac_evaluator.py`.
   - Integrate `MopacEvaluator` into `Evaluator.total_score()`.
   - Implement early rejection logic (shape similarity threshold).

## Validation Plan

1. **Unit Test**: Initialize with redundant materials and verify `possible_actions` count.
2. **Integration Test**: Run a terminal evaluation and verify MOPAC output parsing.
3. **Regression**: Ensure Shogi/Chess modules are unaffected.
