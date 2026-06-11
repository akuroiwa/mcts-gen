# Feature Specification: MOPAC Integration and Fragment Management Refactoring

**Feature Branch**: `016-mopac-fragment-refactor`

**Created**: 2025年12月31日

**Status**: Draft

**Input**: User description: "Integrate MOPAC2022 for quantum chemical evaluation and refactor fragment management in ligand_mcts.py using a hybrid SMILES-Mol approach to resolve duplication and accumulation issues."

## User Scenarios & Testing

### User Story 1 - Deduplicated Fragment Library (Priority: P1)

As a researcher, I want the MCTS search space to be free of duplicate fragments so that the agent does not waste computational resources exploring identical branches.

**Why this priority**: Duplication currently wastes >30% of search depth.

**Independent Test**: Initialize the system with a material file containing redundant SMILES. Verify that `get_possible_actions` returns a unique set of fragments.

**Acceptance Scenarios**:

1. **Given** a material file with duplicate SMILES, **When** fragments are generated, **Then** the internal library uses a `set` to store only unique SMILES.
2. **Given** the search is running, **When** actions are proposed, **Then** no two actions share the same SMILES and attachment point.

---

### User Story 2 - Quantum Chemical Reward (Priority: P1)

As a medicinal chemist, I want the final reward of a generated ligand to reflect its thermodynamic stability (Heat of Formation) calculated via MOPAC2022.

**Why this priority**: Shape complementarity alone produces chemically unstable molecules.

**Independent Test**: Complete a simulation and verify that the `simulation_stats` include a "mopac_energy" or similar score.

**Acceptance Scenarios**:

1. **Given** a terminal ligand state, **When** `getReward()` is called, **Then** a MOPAC (PM7) calculation is triggered in the background.
2. **Given** a MOPAC calculation fails (e.g., valid but extremely strained molecule), **When** calculating reward, **Then** a severe energy penalty is applied.

---

### User Story 3 - High-Fidelity State Propagation (Priority: P2)

As a developer, I want the MCTS state to maintain the full RDKit `Mol` object (including 3D coordinates and conformers) so that electronic properties are preserved across transitions.

**Why this priority**: Converting to SMILES and back to Mol loses the 3D context needed for MOPAC.

**Independent Test**: Verify that the 3D coordinates of a parent molecule are preserved after a fragment attachment.

**Acceptance Scenarios**:

1. **Given** a state with an optimized 3D conformer, **When** an action is applied, **Then** the new state inherits the coordinates and builds upon them without re-initializing from 2D.

---

## Edge Cases

- **MOPAC Not Installed**: System should gracefully fallback to a standard penalty or inform the user without crashing.
- **Disconnected Fragments**: If MOPAC calculation is requested for a molecule that RDKit failed to bond properly, it should return a high penalty.
- **Calculation Timeout**: Long quantum calculations should be capped to prevent blocking the agent.

## Requirements

### Functional Requirements

- **FR-001**: System MUST use SMILES strings as the primary identifier for fragments in the `fragment_library` to ensure uniqueness.
- **FR-002**: `LigandAction` MUST be defined by its SMILES string, allowing `set`-based deduplication of search branches.
- **FR-003**: `LigandState` MUST maintain the `rdkit.Chem.Mol` object as its internal representation.
- **FR-004**: System MUST support executing MOPAC2022 via subprocess for molecules reaching the `target_size`.
- **FR-005**: System MUST parse Heat of Formation (HOF) and potentially ESP charges from MOPAC output files.
- **FR-006**: System MUST implement an "Early Rejection" gate where MOPAC is only called if shape complementarity exceeds a minimum threshold.

### Key Entities

- **LigandLibrary**: A `set` of unique SMILES strings acting as the building block pool.
- **MopacEvaluator**: A component responsible for XYZ generation, `.mop` file creation, execution, and output parsing.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Zero duplicate SMILES actions per attachment point in `get_possible_actions`.
- **SC-002**: Generated molecules show a correlation between MOPAC HOF and chemical stability.
- **SC-003**: 100% preservation of RDKit Conformer data across state transitions.
- **SC-004**: Average MOPAC calculation overhead remains under 3 seconds per terminal node.

## Assumptions

- We assume MOPAC2022 is accessible in the system path as `mopac`.
- We assume that the user provides a valid 3D environment (protein pocket) for docking.
- We assume PM7 is the appropriate Hamiltonian for the majority of ligand-like molecules.
