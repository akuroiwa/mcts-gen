# Implementation Plan: The list of molecules that are the raw materials for chemical fragments is stored as an external file, increasing the extensibility of the module.

**Branch**: `009-external-molecule-source` | **Date**: 2025年12月3日水曜日 | **Spec**: ./spec.md
**Input**: Feature specification from `specs/009-external-molecule-source/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Enhance the `ligand_mcts` module to dynamically generate chemical fragments from user-provided external files containing complete molecules (SMILES, SDF, CSV formats). This replaces hard-coded fragment lists and improves extensibility.

## Technical Context

**Language/Version**: Python 3.12
**Primary Dependencies**: RDKit (for molecular parsing and BRICS fragmentation).
**Storage**: Filesystem (for `source_molecule_path` input).
**Testing**: pytest
**Target Platform**: Linux server
**Project Type**: Single project
**Performance Goals**: Process a SMILES file containing at least 100 source molecules and generate fragments from them within 5 seconds during initialization.
**Constraints**: N/A
**Scale/Scope**: Modifies `src/mcts_gen/games/ligand_mcts.py` to support dynamic fragment generation and multiple input file formats for source molecules.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The `constitution.md` file is currently a template and does not contain defined principles. The plan adheres to general best practices for modularity and extensibility in software development.

## Project Structure

### Documentation (this feature)

```text
specs/009-external-molecule-source/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/
└── mcts_gen/
    └── games/
        └── ligand_mcts.py # Main file to be modified.
                           # May add internal helper functions/classes here for fragmentation.
tests/
└── unit/
    └── test_ligand_mcts.py # Existing unit tests to be updated/new ones added.
```

**Structure Decision**: The project is a single Python package. The primary change will be within `src/mcts_gen/games/ligand_mcts.py`. New utility functions or classes for fragmentation and file parsing will be added either directly within `ligand_mcts.py` or a new dedicated utility module if its scope warrants.

## Complexity Tracking
Not applicable, as no constitutional violations are required.