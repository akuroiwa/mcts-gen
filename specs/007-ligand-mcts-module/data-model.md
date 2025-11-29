# Data Model: Ligand MCTS Module

This document defines the primary data structures (Python classes) used in the `ligand_mcts.py` game module.

## 1. LigandMCTSGameState
Represents the complete state of the game at any point, designed to be compatible with the `mcts-gen` engine.

- **Description:** This is the main class that implements the `GameStateBase` interface. It acts as a wrapper around the internal `LigandState` and the `Evaluator`.
- **Fields:**
    - `state (LigandState)`: The core state of the molecule being generated.
    - `evaluator (Evaluator)`: An instance of the evaluator used to score states.
- **Relationships:**
    - Inherits from `GameStateBase`.
    - Composes a `LigandState` object.
    - Composes an `Evaluator` object.

## 2. LigandState
A simple data class representing the molecule being built.

- **Description:** Holds the current molecule's structure and the history of actions taken to create it. This class is internal to the `ligand_mcts` module.
- **Fields:**
    - `mol (rdkit.Chem.Mol)`: The RDKit molecule object representing the current structure. Can be `None` for the initial empty state.
    - `history (List[LigandAction])`: A list of actions that have been applied to reach the current state.
- **State Transitions:**
    - A `LigandState` transitions to a new `LigandState` by applying a `LigandAction` via its `apply_action` method.

## 3. LigandAction
A serializable data class representing a single action that can be taken to modify a `LigandState`.

- **Description:** Defines a modification to the molecule, typically the addition of a chemical fragment.
- **Fields:**
    - `frag_smiles (str)`: The SMILES string of the fragment to be added (e.g., `"c1ccccc1"` for a benzene ring).
    - `attach_idx (Optional[int])`: The index of the atom on the existing molecule to which the new fragment should be attached. (Note: The initial implementation may simplify this connection logic).

## 4. Evaluator
A utility class that calculates the reward for a given molecular state.

- **Description:** This class is responsible for scoring a molecule based on various criteria. It is initialized with the target protein pocket.
- **Fields:**
    - `pocket_points (np.ndarray)`: A NumPy array of 3D coordinates representing the target protein pocket, loaded from a `pocketX_atm.pdb` file.
- **Key Methods:**
    - `total_score(mol)`: Calculates a final weighted score for a given RDKit molecule. This score is a combination of:
        - **Shape Score:** Similarity to the `pocket_points`.
        - **Gaussian Score:** Gaussian overlap with the `pocket_points`.
        - **MolLogP Score:** A measure of hydrophobicity.
        - **QED Score:** A measure of druglikeness.
        - **Penalty Score:** Penalties for invalid or undesirable structures.
- **Relationships:**
    - Instantiated and used by `LigandMCTSGameState`.
