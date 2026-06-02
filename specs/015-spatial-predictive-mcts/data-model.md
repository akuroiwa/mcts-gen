# Data Model: Spatial Partitioning and Predictive Search

## Entities

### SpatialZone
Defines a 3D volume within the protein binding pocket to restrict fragment placement.
- **x_min, x_max**: Float range.
- **y_min, y_max**: Float range.
- **z_min, z_max**: Float range.

### MctsSlot
Represents a stashed search context for predictive execution.
- **slot_id**: Unique identifier (e.g., "main", "predict_p_e4").
- **engine**: The `McpMcts` instance associated with this slot.
- **created_at**: Timestamp for cleanup.

## Relationships
- `AiGpSimulator` manages a dictionary of `MctsSlot` entities.
- `LigandMCTSGameState` optionally references a `SpatialZone` via its `Evaluator`.

## Validation Rules
- `SpatialZone` ranges must be valid (min < max).
- `slot_id` must be alphanumeric.
