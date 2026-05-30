# Spec-007: Ligand MCTS Module

## Feature Description
Introduces `ligand_mcts.py` for de novo ligand generation optimized for protein pockets using MCTS and scoring functions (shape, MolLogP, QED).

## User Scenarios
- **Initialization**: User provides PDB and `fpocket` output. AI guides installation of `rdkit`, `scipy`, `numpy`, and `fpocket`.
- **Search**: MCTS builds molecules iteratively, evaluating shape complementarity and drug-likeness.
- **Results**: Returns best scoring ligand as SMILES.

## Key Requirements
- `LigandMCTSGameState` inherits from `GameStateBase`.
- Constructor accepts `pocket_path`.
- Reward includes shape overlap, MolLogP, and QED.
- Dynamic module loading support.
