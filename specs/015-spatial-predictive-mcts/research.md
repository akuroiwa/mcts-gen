# Research: Spatial Partitioning and Predictive Search

## Decision 1: Spatial Filtering via Attachment Pruning

### Rationale
Restricting the search space by binding pocket coordinates is most effectively done during the **Expansion** phase. By filtering out atoms (attachment points) that fall outside the specified `SpatialZone`, we prevent the MCTS from even considering moves in unauthorized regions.

### Implementation Detail
- `Evaluator` will store a `bounding_box` (optional).
- `LigandState.legal_actions` will retrieve atom positions from the current RDKit `Conformer`.
- Atoms outside the `bounding_box` will be excluded as `attach_idx` candidates.

### Alternatives Considered
- **Post-hoc Filtering (Scoring)**: Allow placement but give zero reward. *Rejected*: This wastes MCTS rounds exploring invalid space.
- **Voxel-based Partitioning**: Use a grid. *Rejected*: Too complex for initial implementation; simple XYZ box is sufficient.

## Decision 2: Predictive "Search Slots" in Simulator

### Rationale
To support predictive search, the `AiGpSimulator` needs to handle multiple search contexts without losing the current game tree.

### Implementation Detail
- Introduce "Stashed Engines".
- `reinitialize_mcts` will accept an optional `slot_id` (defaults to "main").
- The AI can initialize a predicted state in a slot like "predicted_user_move_1".
- When the user actually makes that move, the AI calls `activate_mcts_slot("predicted_user_move_1")` to swap the engines.

### Alternatives Considered
- **Tree Grafting**: Find the sub-node in the current tree. *Rejected*: Hard to do if the AI needs to change parameters or use different pruning for the prediction. Forking a fresh engine is cleaner.

## Decision 3: Size Estimation Logic

### Rationale
AI agents need to know how big a pocket is to set `target_size`.

### Implementation Detail
- Add a helper method (or document the logic) to calculate the volume of the `SpatialZone`.
- Heuristic: 1 heavy atom per 15-20 Å³.
