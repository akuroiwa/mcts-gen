# Research & Analysis

**Feature**: The list of molecules that are the raw materials for chemical fragments is stored as an external file, increasing the extensibility of the module.

## Decisions Made During Specification Clarification:

1.  **Fragmentation Algorithm**: The initial implementation will use the **BRICS** algorithm. This decision was made to balance simplicity and effectiveness for generating a diverse fragment library, allowing for future enhancements with more complex algorithms if needed.
2.  **Supported File Formats**: The system will support multiple common file formats for source molecules: **SMILES** (`.smi`, `.smiles`), **SDF** (`.sdf`), and **CSV** (`.csv` with a 'smiles' column). The system will automatically detect the format based on the file extension.

No further external research is required beyond these confirmed decisions, as RDKit provides the necessary functionalities for parsing these formats and performing BRICS fragmentation.
