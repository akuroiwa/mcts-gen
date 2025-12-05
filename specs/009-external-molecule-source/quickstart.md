# Quickstart

**Feature**: The list of molecules that are the raw materials for chemical fragments is stored as an external file, increasing the extensibility of the module.

This feature enhances the `ligand_mcts` module by allowing you to provide a file containing source molecules, from which chemical fragments will be dynamically generated for the MCTS simulation.

## How to Use the New `source_molecule_path`

1.  **Prepare your Source Molecule File**: Create a text file containing a list of complete molecules. Supported formats are:
    *   **SMILES**: Files with `.smi` or `.smiles` extension (one SMILES string per line).
    *   **SDF**: Files with `.sdf` extension (standard SDF format).
    *   **CSV**: Files with `.csv` extension, containing a column named `smiles` (case-insensitive) for molecular structures.

    *Example `molecules.smi` content:*
    ```
    CCO
    c1ccccc1
    CNC(=O)c1ccc(C)cc1
    ```

2.  **Initialize the MCTS Simulation**: When calling `reinitialize_mcts` for the `ligand_mcts` game, provide the `source_molecule_path` argument in the `state_kwargs` dictionary, in addition to the `pocket_path`.

    *Example `state_kwargs` dictionary:*
    ```python
    {
        "pocket_path": "/path/to/your/pocketX_atm.pdb",
        "source_molecule_path": "/path/to/your/molecules.smi"
    }
    ```

3.  **Run the Simulation**: The MCTS will then automatically:
    *   Read your `source_molecule_path` file.
    *   Dynamically fragment the molecules using the BRICS algorithm.
    *   Use these generated fragments as `legal_actions` during the MCTS search.

This approach eliminates the need for hard-coded fragment lists, making it easier to experiment with different sets of starting materials for ligand design.
