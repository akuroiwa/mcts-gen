# Spec-016: MOPAC Integration & Fragment Refactor

## Objective
Enhance the chemical realism of generated ligands by integrating quantum chemical stability evaluation (MOPAC2022) and optimize the search space through fragment library deduplication.

## Scope
- `src/mcts_gen/services/mopac_evaluator.py`: New service for external MOPAC2022 execution.
- `src/mcts_gen/games/ligand_mcts.py`: Refactored to use hybrid SMILES-Mol fragment management and integrated MOPAC reward.
- `src/mcts_gen/models/mopac.py`: Data class for MOPAC results.

## Key Changes
1. **MOPAC Reward Integration**: Implemented Heat of Formation (HOF) calculation using MOPAC (PM7/1SCF) as a high-precision reward component.
2. **Early Rejection Gate**: Optimzed performance by only triggering MOPAC evaluation for molecules with sufficient shape complementarity (>0.3).
3. **Hybrid Management**: Switched `fragment_library` to a `set[str]` (SMILES) for deduplication, while maintaining high-fidelity 3D `Mol` objects for state propagation.
4. **Coordinate Preservation**: Improved `apply_action` to fix parent atom coordinates during fragment addition, ensuring consistent 3D context for quantum calculations.

## Verification
- Verified MOPAC output parsing and HOF extraction.
- Unit tests confirm that duplicate fragments are no longer present in the search branches.
- Integration tests with real MOPAC2022 installation confirmed successful reward feedback.
