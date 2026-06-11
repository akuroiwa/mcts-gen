# Contract Update: MOPAC Integration

## Modified Tool: reinitialize_mcts
No interface change, but internal behavior for `ligand_mcts` is updated.

## Simulation Stats Update
The `get_simulation_stats` and `get_principal_variation` tools will now include quantum chemical data.

**New fields in result**:
- `mopac_energy`: (float) Heat of Formation in kcal/mol.
- `mopac_status`: (string) 'success', 'failed', or 'skipped'.

## Internal Evaluator Contract
New internal method `total_score` logic:
1. `shape_score` (USR/Gaussian)
2. `chemical_score` (logP/QED)
3. `size_score` (Target size)
4. `mopac_score` (Heat of Formation - only if terminal and shape > threshold)
