# Feature Specification: Spatial Partitioning and Predictive Search

**Feature Branch**: `015-spatial-predictive-mcts`

**Created**: 2025年12月31日

**Status**: Draft

**Input**: User description: "Implement spatial pocket partitioning for ligand generation and extend the concept to predictive branch searching for games like Shogi/Chess."

## User Scenarios & Testing

### User Story 1 - Focused Pocket Exploration (Priority: P1)

As a researcher, I want to divide a large binding pocket into several spatial zones so that I can run independent, focused ligand generation simulations for each zone.

**Why this priority**: Large pockets cause search explosion; partitioning is the primary solution for scaling.

**Independent Test**: Verify that a simulation can be initialized with coordinate-based spatial filters that restrict fragment placement to a specific sub-region of the pocket.

**Acceptance Scenarios**:

1. **Given** a large protein pocket, **When** I specify a spatial zone (min/max X, Y, Z), **Then** the MCTS search only considers fragment attachments within that zone.
2. **Given** multiple defined zones, **When** I run simulations for each, **Then** I receive a set of optimized ligand candidates for every individual sub-region.

---

### User Story 2 - Predictive Game Advantage (Priority: P1)

As a Shogi/Chess player (or developer), I want the system to predict my opponent's most likely responses and begin pre-calculating the MCTS tree for those specific board states in advance.

**Why this priority**: Reduces perceived latency and allows deeper search on expected branches without increasing turn-by-turn computation time.

**Independent Test**: Verify that the system can initialize a new MCTS session based on a predicted game state (current state + predicted move) and return the best response for that future state.

**Acceptance Scenarios**:

1. **Given** the current board state and a determined best move, **When** I request a predictive search, **Then** the system identifies the most probable counter-moves and initiates background MCTS rounds for them.
2. **Given** a predicted user move actually occurs, **When** the turn switches, **Then** the system immediately provides the pre-calculated best move for that branch.

---

### User Story 3 - Results Consolidation (Priority: P2)

As an AI agent, I want to merge the partial results from partitioned pocket simulations into a single, comprehensive ligand strategy.

**Why this priority**: Completes the "Divide and Conquer" workflow.

**Independent Test**: Verify that the system can output a summary of best fragments for each zone and suggest possible linkage points.

**Acceptance Scenarios**:

1. **Given** results from multiple pocket zones, **When** requested to consolidate, **Then** the system identifies overlapping or adjacent fragments that could be linked.

## Requirements

### Functional Requirements

- **FR-001**: System MUST support spatial partitioning of protein binding pockets using coordinate ranges or clustering.
- **FR-002**: System MUST allow the AI to set a "Search Focus" region during `reinitialize_mcts` for ligand generation.
- **FR-003**: System MUST provide a mechanism to identify candidate opponent moves in games (e.g., top $N$ moves from a policy model).
- **FR-004**: System MUST support "Predictive State Initialization" where MCTS begins on a board state that hasn't yet occurred in the main game loop. The AI agent will dynamically determine the number of candidate moves to pre-calculate based on the branching complexity and evaluation variance of the current state.
- **FR-005**: System MUST reduce the total computational overhead by breaking massive searches into independent batches.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Perceived latency for the "next-best-move" in games is reduced by 50% when the predicted move occurs.
- **SC-002**: Ligand generation for a large pocket (> 500 atoms) completes 3x faster using 4 spatial zones compared to a single global search.
- **SC-003**: 100% of spatial partitioning boundaries are strictly enforced during the search phase.

## Key Entities

- **SpatialZone**: Represents a 3D bounding box within the protein pocket.
- **PredictedState**: Represents a future board state derived from a current state and a set of probable actions.

## Edge Cases

- **Overlapping Zones**: What happens if spatial zones overlap? The system should treat them as independent but the AI should handle result deduplication.
- **Unexpected User Move**: If the opponent makes a move that was not predicted, the system must gracefully discard the background MCTS results and start a fresh search without delay.
- **Empty Zone**: If a spatial zone contains no valid attachment points, the system should inform the agent early to avoid wasted computation.

## Dependencies

- **Protein Structure Loader**: Relies on `load_pocket_atm_pdb` and USR descriptor logic.
- **Game Engine**: Relies on `python-shogi` or `python-chess` for state validation during prediction.
- **External AI Policy**: Relies on an external model (or the LLM's own policy) to supply candidate moves for predictive search.

## Assumptions

- We assume the AI agent has access to a policy model or historical data to make "informed guesses" about opponent responses in games.
- We assume that "merging" ligands from different zones is a high-level reasoning task for the AI rather than an automatic chemical link optimization at this stage.
