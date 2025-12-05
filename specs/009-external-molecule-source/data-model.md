# Data Model

**Feature**: The list of molecules that are the raw materials for chemical fragments is stored as an external file, increasing the extensibility of the module.

This feature does not introduce new top-level persistent data models. However, it involves internal modifications to how the `LigandState` is constructed and managed:

*   **`LigandState`**:
    *   **Internal Fragment Library**: A new internal attribute will store the dynamically generated fragment library, which will be a list of `LigandAction` objects or similar structures. This library is derived from the `source_molecule_path`.
    *   **Relationship**: This fragment library will be used by the `LigandState`'s `legal_actions` method.

*   **Source Molecule File**:
    *   **Description**: An external file provided by the user containing a list of complete molecules (e.g., in SMILES, SDF, or CSV format).
    *   **Usage**: Read at initialization time to generate the internal fragment library.
