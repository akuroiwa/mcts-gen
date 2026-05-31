# Feature Specification: Documentation and Translation Update

**Feature Branch**: `014-update-docs`

**Created**: 2025年12月31日

**Status**: Draft

**Input**: User description: "Update documentation and translate to Japanese for recent MCTS enhancements and fragment growth features."

## User Scenarios & Testing

### User Story 1 - Understand Search Limit (Priority: P1)

As a user/developer, I want to understand how to use the new `run_mcts_analysis` tool to avoid API limits and improve search precision.

**Why this priority**: This is a core functionality added to stabilize the AI-MCTS interaction.

**Independent Test**: Verify that `docs/quickstart.rst` and `docs/paper.rst` contain clear explanations of the "Search Limit" concept and usage examples.

**Acceptance Scenarios**:

1. **Given** a user reading the documentation, **When** they look for "Search Limit", **Then** they find a description of `run_mcts_analysis`.
2. **Given** an AI agent reading `AGENTS.md` (or the prompt), **When** it encounters the execution phase, **Then** it knows to use the analysis tool.

---

### User Story 2 - Fragment-based Ligand Growth (Priority: P2)

As a medicinal chemist, I want to know how to provide my own fragments and set a target ligand size for the simulation.

**Why this priority**: Critical for the new ligand generation capabilities.

**Independent Test**: Verify that the documentation explains `source_molecule_path` and `target_size` parameters.

**Acceptance Scenarios**:

1. **Given** the ligand generation section, **When** a user provides a CSV of molecules, **Then** the documentation guides them on the required format.

---

### User Story 3 - Japanese Documentation (Priority: P1)

As a Japanese developer, I want to read the latest manual in my native language.

**Why this priority**: Essential for the user's primary working environment.

**Independent Test**: Verify that `docs/locales/ja/LC_MESSAGES/*.po` files are updated with the new content.

## Requirements

### Functional Requirements

- **FR-001**: Update `docs/quickstart.rst` with `run_mcts_analysis` and ligand growth features.
- **FR-002**: Update `docs/paper.rst` to reflect the transition from individual rounds to batched analysis (GP-like).
- **FR-003**: Regenerate or update gettext `.po` files for Japanese translation.
- **FR-004**: Translate all new content to Japanese.

## Success Criteria

- **SC-001**: Documentation reflects version 0.0.4+ features accurately.
- **SC-002**: `make html` in the `docs/` directory succeeds without errors.
- **SC-003**: Japanese translation is complete and matches the English version.
