# Contract Update: Simulator Tools

## Modified Tool: reinitialize_mcts
Adds support for named slots and spatial filtering.

**Arguments**:
- `state_module`, `state_class`, `state_kwargs`: (Existing)
- `slot_id`: (Optional, default="main") Identifier for the search context.
- `spatial_filter`: (Optional) Dictionary with `x_min`, `x_max`, `y_min`, `y_max`, `z_min`, `z_max` for ligand games.

## New Tool: activate_mcts_slot
Promotes a stashed/predicted search to the main active context.

**Arguments**:
- `slot_id`: The ID of the slot to activate.

## New Tool: list_mcts_slots
Returns all currently stashed search contexts.

**Returns**:
- `slots`: List of strings.
