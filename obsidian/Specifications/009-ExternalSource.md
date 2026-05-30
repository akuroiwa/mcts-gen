# Spec-009: External Molecule Source for Ligand MCTS

## Feature Description
Allows providing a file of complete molecules (SMILES, SDF, CSV) as raw materials for fragment generation using BRICS algorithm.

## User Scenarios
- **Custom Library**: User provides `source_molecule_path`.
- **Dynamic Fragmentation**: System breaks down source molecules during initialization to build the action space.

## Requirements
- `LigandMCTSGameState` accepts optional `source_molecule_path`.
- Support for `.smi`, `.sdf`, `.csv`.
- Integration of BRICS fragmentation logic.

## Status
- **Needs Attention**: Docstring in `ligand_mcts.py` must be enhanced to properly inform the AI agent about this feature. (See Spec-012 in StoryBoard).
