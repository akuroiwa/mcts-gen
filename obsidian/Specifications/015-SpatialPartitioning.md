# Spec-015: Spatial Pocket Partitioning

## Objective
Enable efficient exploration of large protein pockets by dividing them into spatial zones and allowing the MCTS search to be restricted to specific regions.

## Scope
- `src/mcts_gen/models/spatial.py`: New model to define 3D `SpatialZone` logic (bounding boxes).
- `src/mcts_gen/games/ligand_mcts.py`: Added support for filtering fragment attachment points based on `SpatialZone`.
- `src/mcts_gen/services/ai_gp_simulator.py`: Updated `reinitialize_mcts` to accept `spatial_filter` arguments.

## Key Changes
1. **SpatialZone Class**: Implemented axis-aligned bounding box (AABB) checks for 3D coordinates.
2. **Filtering Logic**: The `legal_actions` method in `LigandMCTSGameState` now filters atoms based on the active `SpatialZone` if provided.
3. **API Integration**: Exposed `spatial_filter` through the MCP tool interface to allow AI-guided partitioning.

## Verification
- Verified that fragment growth only occurs within the specified bounding box.
- Integration tests confirm `reinitialize_mcts` correctly parses and applies the filter.
