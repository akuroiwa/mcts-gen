# Feature Specification: The list of molecules that are the raw materials for chemical fragments is stored as an external file, increasing the extensibility of the module.

**Feature Branch**: `009-external-molecule-source`  
**Created**: 2025年12月3日水曜日  
**Status**: Draft  
**Input**: User description: "The list of molecules that are the raw materials for chemical fragments is stored as an external file, increasing the extensibility of the module."

## Feature Description
This feature enhances the `ligand_mcts` module within the `mcts-gen` framework by allowing users to provide a list of complete molecules as raw materials for generating chemical fragments. Instead of relying on a hard-coded or pre-fragmented list, the system will dynamically generate fragments from user-supplied molecules (e.g., existing drugs or candidate compounds). This significantly increases the module's extensibility and user-friendliness, as users can work with readily available molecular data.

## User Scenarios & Testing

### Scenario 1: Initializing Ligand Generation with Source Molecules (Priority: P1)
**Given** the user has a file (e.g., `molecules.smi`) containing a list of complete molecules (e.g., in SMILES format).
**When** the user provides this `source_molecule_path` along with the `pocket_path` to initialize a `ligand_mcts` simulation.
**Then** the system should read the `molecules.smi` file.
**And** the system should process these molecules to generate a library of chemical fragments (e.g., using a fragmentation algorithm like BRICS).
**And** the MCTS simulation should successfully start, using these dynamically generated fragments as `legal_actions`.

### Scenario 2: MCTS Exploration using Generated Fragments (Priority: P1)
**Given** a `ligand_mcts` simulation has been initialized with a `source_molecule_path`.
**When** the MCTS system executes rounds to explore new ligand structures.
**Then** the `getPossibleActions` method should return `LigandAction` objects derived from the dynamically generated fragment library.
**And** the `takeAction` method should correctly apply these actions to build new molecular states.

## Functional Requirements
*   **FR1**: The `LigandMCTSGameState` class in `src/mcts_gen/games/ligand_mcts.py` MUST be modified to accept an optional `source_molecule_path` argument in its constructor.
*   **FR2**: If `source_molecule_path` is provided, the `LigandMCTSGameState` constructor MUST read and parse the file (e.g., expecting SMILES strings).
*   **FR3**: A new internal mechanism (e.g., a dedicated function or class) MUST be implemented within `ligand_mcts.py` to perform chemical fragmentation on the loaded source molecules, generating a library of usable fragments.
*   **FR4**: The `getPossibleActions` method in `LigandMCTSGameState` MUST be updated to generate `LigandAction` objects using the dynamically created fragment library when `source_molecule_path` is specified.
*   **FR5**: The system MUST provide clear error handling if the `source_molecule_path` is invalid or the molecules within it cannot be processed.
*   **FR6**: The existing hard-coded fragment list in `ligand_mcts.py` SHOULD be removed or replaced by this new dynamic mechanism.
*   **FR7**: The system MUST detect the input file format based on its extension (`.smi`, `.smiles`, `.sdf`, `.csv`) and use the correct parser (e.g., from RDKit) to read the source molecules.

## Success Criteria
*   The `ligand_mcts` module successfully initializes an MCTS simulation when provided with a valid `source_molecule_path` to a file containing complete molecules.
*   The MCTS simulation for ligand generation proceeds using fragments derived from the source molecules, leading to chemically plausible ligand candidates.
*   The system can process a SMILES file containing at least 100 source molecules and generate fragments from them within 5 seconds during initialization.
*   The generated fragments are diverse enough to allow the MCTS to explore a broad chemical space for ligand generation.
*   The new `source_molecule_path` mechanism replaces the hard-coded fragment list, simplifying future updates to the fragment library.

## Key Entities
*   **`LigandMCTSGameState`**: The state object for ligand generation.
*   **Source Molecule File**: An external file (e.g., SMILES file) containing complete molecules.
*   **Fragmenter**: A new internal component responsible for breaking down source molecules into fragments.
*   **Fragment Library**: A collection of chemical fragments generated from source molecules.
*   **`LigandAction`**: An action representing the addition of a chemical fragment.

## Assumptions
*   Source molecule files will primarily be in SMILES format, requiring an RDKit-compatible parser.
*   The fragmentation algorithm (e.g., BRICS, retrosynthesis-based) will be chosen based on its suitability for MCTS exploration and computational efficiency.
*   The AI agent will be responsible for obtaining or guiding the user to provide a valid `source_molecule_path`.

## Dependencies
*   **Internal**: `ligand_mcts.py` module.
*   **External Python Libraries**: RDKit (for molecular parsing and fragmentation).

## Design Decisions

*   **Fragmentation Algorithm**: The initial implementation will use the **BRICS** algorithm. It offers a good balance of simplicity and effectiveness for generating a diverse fragment library. More advanced algorithms can be considered in future iterations.
*   **Supported File Formats**: The system will support multiple common file formats for user convenience. It will automatically detect the format based on the file extension and use the appropriate parser:
    *   `.smi` or `.smiles`: SMILES format.
    *   `.sdf`: Structure-Data File format.
    *   `.csv`: Comma-Separated Values, assuming a column named 'smiles' contains the molecular structures.