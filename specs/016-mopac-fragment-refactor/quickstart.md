# Task 016 Quickstart: Quantum Chemical Search

## Prerequisites
Ensure MOPAC2022 is installed and available in your PATH.

```bash
# Verify mopac
mopac --version
```

## Running a MOPAC-enhanced Simulation
1. Initialize as usual.
2. The AI agent will automatically include MOPAC energy in its evaluation once a molecule reaches the target size.

```json
{
  "name": "reinitialize_mcts",
  "args": {
    "state_module": "mcts_gen.games.ligand_mcts",
    "state_class": "LigandMCTSGameState",
    "state_kwargs": {
      "pocket_path": "pocket1_atm.pdb",
      "target_size": 30
    }
  }
}
```

## Reviewing Results
Call `get_principal_variation` to see the Heat of Formation.
```json
{
  "principal_variation": [...],
  "final_score": 2.45,
  "final_state_summary": {
    "smiles": "...",
    "mopac_energy": -120.5,
    "mopac_status": "success"
  }
}
```
