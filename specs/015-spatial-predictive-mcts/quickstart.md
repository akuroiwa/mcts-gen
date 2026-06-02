# Task 015 Quickstart: Predictive Search and Spatial Zones

## Spatial Partitioning (Ligands)
To run a simulation restricted to a specific part of a protein pocket:

1. Identify the coordinate box (e.g., using PyMOL or pocket info).
2. Initialize with `spatial_filter`:
```json
{
  "name": "reinitialize_mcts",
  "args": {
    "state_module": "mcts_gen.games.ligand_mcts",
    "state_class": "LigandMCTSGameState",
    "state_kwargs": { "pocket_path": "pocket1_atm.pdb" },
    "spatial_filter": {
      "x_min": 10.5, "x_max": 20.0,
      "y_min": -5.0, "y_max": 5.0,
      "z_min": 100.2, "z_max": 110.5
    }
  }
}
```

## Predictive Search (Games)
To calculate the next move while the user is thinking:

1. Assume your best move was `e2e4`.
2. Predict the user's response (e.g., `e7e5`).
3. Start a background search in a new slot:
```json
{
  "name": "reinitialize_mcts",
  "args": {
    "state_module": "mcts_gen.games.chess_mcts",
    "state_class": "ChessGameState",
    "state_kwargs": { "fen": "... [fen after e2e4 e7e5] ..." },
    "slot_id": "predict_e7e5"
  }
}
```
4. Run analysis on that slot.
5. If the user plays `e7e5`, call `activate_mcts_slot("predict_e7e5")`.
