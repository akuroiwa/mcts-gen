# Plan: Spec-013 Fragment-based Growth and Size Control

## Objective
Implement multi-atom fragment support, conformational diversity, and AI-guided size control in `ligand_mcts.py`.

## Technical Strategy

### 1. Fragment Growth & Flexible Loading
- **Flexible CSV Parsing**: Update `_load_molecules_from_file` to handle CSVs without a 'smiles' header by checking columns for valid SMILES strings.
- **Fragment Actions**: Ensure `legal_actions` generates choices for all fragments in the library.

### 2. Conformational Diversity (Orientation)
- **Problem**: Duck typing allows objects as nodes, enabling orientation to be a state property.
- **Mechanism**:
    - Add `orientation_idx: int = 0` to `LigandAction`.
    - In `apply_action`:
        1. Create the combined molecule.
        2. Call `AllChem.EmbedMultipleConfs(mol, numConfs=10, randomSeed=...)`.
        3. Use the `orientation_idx` to select the specific conformer.
    - In `legal_actions`: Generate multiple actions per (fragment, attach_idx) pair with different `orientation_idx`.

### 3. Size Control
- **Parameter**: `target_size: int` (default 30) passed to `LigandMCTSGameState`.
- **Reward**:
    - `Evaluator` calculates `size_score = 1.0 - abs(current_size - target_size) / target_size`.
    - Penalty for exceeding `target_size` by more than 20%.

## Implementation Tasks (Specs)
1. **Robust Loading**: Fix CSV parsing in `ligand_mcts.py`.
2. **Conformer Integration**: Implement `orientation_idx` logic in `LigandAction` and `apply_action`.
3. **Size Reward**: Implement `target_size` scoring in `Evaluator`.
4. **AI Guidance**: Update prompt to encourage volume-based size estimation.

## Workspace Synchronization
- Sync this plan to `obsidian/Specifications/013-FragmentGrowth.md`.
- Create `specs/013-fragment-growth/` documents using Spec-Kit.
