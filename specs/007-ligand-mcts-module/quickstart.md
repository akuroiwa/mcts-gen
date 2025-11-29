# Quickstart: Ligand Generation with MCTS

This guide explains how to use the `ligand_mcts` module to generate novel molecules that fit a specific protein binding pocket.

## 1. Prerequisites
Before you begin, you must install several external dependencies.

### Python Packages
Install the required Python libraries using pip. `RDKit` is used for chemistry calculations, while `SciPy` and `NumPy` are used for numerical operations.

```bash
pip install rdkit-pypi scipy numpy
```

### fpocket
The `fpocket` software is used to identify binding pockets in protein structures. It can be installed as a snap package.

```bash
sudo snap install fpocket
```

## 2. Generating a Pocket File
The MCTS simulation requires a file that describes the 3D coordinates of the target binding pocket.

1.  **Obtain a protein structure:** Start with a PDB file for your protein of interest (e.g., `my_protein.pdb`).
2.  **Run fpocket:** Execute `fpocket` on your PDB file.
    ```bash
    fpocket -f my_protein.pdb
    ```
3.  **Locate the pocket file:** `fpocket` will create an output directory (e.g., `my_protein_out/pockets/`). Inside, you will find PDB files for each identified pocket. For the largest pocket (pocket 1), the file you need is typically `pocket1_atm.pdb`. This is the file you will provide to the MCTS simulation.

## 3. Running the Simulation
You can initiate a ligand generation simulation through an AI agent interacting with the `mcts-gen` server. The agent needs to call the `reinitialize_mcts` tool with the correct parameters for the ligand generation game.

### Example AI Agent Call
Here is an example of how the AI agent would formulate the call to start the simulation.

- **Goal:** "Generate a ligand for the pocket defined in `/path/to/my_protein_out/pockets/pocket1_atm.pdb`."

The AI agent would translate this into the following tool call:

```python
# This is an illustrative example of the tool call the AI agent would make.
reinitialize_mcts(
    state_module="mcts_gen.games.ligand_mcts",
    state_class="LigandMCTSGameState",
    state_kwargs={
        "pocket_path": "/path/to/my_protein_out/pockets/pocket1_atm.pdb"
    },
    iteration_limit=5000
)
```

### Workflow
1.  The agent calls `reinitialize_mcts` as shown above.
2.  The agent then enters a loop, calling `run_mcts_round` to perform the search.
3.  After the search is complete, the agent calls `get_best_move` to retrieve the SMILES string of the highest-scoring molecule found.
