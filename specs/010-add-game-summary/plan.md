# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the implementation of a `get_state_summary` method in the `ChessGameState` and `ShogiGameState` classes. This method will provide a rich, human-readable summary of the final game state when requested by the `get_principal_variation` tool. For Chess, the summary will be a full PGN string. For Shogi, it will be a full KIF string. This enhances the utility of the MCTS simulation results by providing a standard, portable format for game analysis.

## Technical Context

**Language/Version**: Python 3.12
**Primary Dependencies**: `python-chess`, `python-shogi`
**Storage**: N/A
**Testing**: `pytest`
**Target Platform**: Linux server
**Project Type**: Single Project
**Performance Goals**: `<100ms` for `get_state_summary` on games up to 100 moves.
**Constraints**: None
**Scale/Scope**: The feature is self-contained within the `chess_mcts.py` and `shogi_mcts.py` modules.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

The project constitution file at `.specify/memory/constitution.md` is currently a template with placeholder values. As such, a compliance check cannot be performed. The implementation will proceed based on the existing code conventions.

## Project Structure

### Documentation (this feature)

```text
specs/010-add-game-summary/
├── plan.md              # This file
├── research.md          # Research on KIF/PGN generation
├── data-model.md        # Description of class modifications
├── quickstart.md        # To be created
└── contracts/           # Not applicable for this feature
```

### Source Code (repository root)

This feature modifies existing files within the established single-project structure.

```text
src/
└── mcts_gen/
    └── games/
        ├── chess_mcts.py  # MODIFIED
        └── shogi_mcts.py  # MODIFIED
tests/
└── unit/
    └── test_games/
        ├── test_chess_mcts.py # CREATE/MODIFY (for verification)
        └── test_shogi_mcts.py # CREATE/MODIFY (for verification)
```

**Structure Decision**: The implementation will adhere to the existing `src/` and `tests/` single-project structure. New methods will be added to existing classes, and new unit tests will be added to verify the functionality.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
