# Implementation Plan: Add full support for chess

**Branch**: `005-add-full-support` | **Date**: 2025-10-17 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/home/akihiro/文書/develop/git/akuroiwa/mcts-gen/specs/005-add-full-support/spec.md`

## Summary
The feature will be implemented by creating a new `ChessGameState` class in `src/mcts_gen/games/chess_mcts.py`. This class will wrap the `python-chess` library to provide a consistent interface for the MCTS engine, mirroring the existing `ShogiGameState`. The project will be updated to include `python-chess` as an optional dependency, and documentation will be revised to guide users on its installation and use.

## Technical Context
**Language/Version**: Python >=3.8
**Primary Dependencies**: `python-chess`
**Storage**: N/A (in-memory state)
**Testing**: `pytest`
**Target Platform**: Linux server
**Project Type**: single
**Performance Goals**: Fast enough for interactive use in finding the best move.
**Constraints**: Must follow the `GameStateBase` interface contract.
**Scale/Scope**: Standard chess rules.

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Simplicity**:
- Projects: 1 (The main `mcts-gen` library)
- Using framework directly? Yes, `python-chess` is used directly without unnecessary wrappers.
- Single data model? Yes, `ChessGameState` is the single model.
- Avoiding patterns? Yes, no complex patterns like Repository are needed.

**Architecture**:
- EVERY feature as library? Yes, `chess_mcts.py` acts as a game-specific library module.
- Libraries listed: `chess_mcts` - provides chess game state management.
- CLI per library: N/A for this game module.
- Library docs: The interface is documented in the contract.

**Testing (NON-NEGOTIABLE)**:
- RED-GREEN-Refactor cycle enforced? Yes, tests will be written first.
- Git commits show tests before implementation? This will be followed.
- Order: Contract (interface) is defined. Integration tests will be the primary form of testing for this module.
- Real dependencies used? Yes, `python-chess` will be used directly.
- Integration tests for: The new `chess_mcts` library.

**Observability**:
- Structured logging included? The `to_dict` method will be used for logging game states.

**Versioning**:
- N/A for this feature plan.

## Project Structure

### Documentation (this feature)
```
specs/005-add-full-support/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/
│   └── game_module_interface.md
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
# Option 1: Single project (DEFAULT)
src/
└── mcts_gen/
    ├── games/
    │   ├── shogi_mcts.py
    │   └── chess_mcts.py  # <-- NEW
    ├── models/
    └── services/

tests/
└── contract/
    └── test_chess_mcts.py # <-- NEW
```

**Structure Decision**: Option 1: Single project.

## Phase 0: Outline & Research
Research has been completed and documented in `research.md`. The plan is to model `chess_mcts.py` closely on the existing `shogi_mcts.py`, using `python-chess` as the backend.

**Output**: [research.md](./research.md)

## Phase 1: Design & Contracts
Design artifacts have been created based on the research.

**Output**:
- [data-model.md](./data-model.md)
- [contracts/game_module_interface.md](./contracts/game_module_interface.md)
- [quickstart.md](./quickstart.md)

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- A `tasks.md` file will be generated based on the requirements in `spec.md` and the design in `plan.md`.
- Tasks will be created for:
    1.  Updating `pyproject.toml` with the `chess` optional dependency.
    2.  Creating the contract test file `tests/contract/test_chess_mcts.py` with failing tests for the main scenarios (initialization, move generation, terminal states).
    3.  Implementing the `src/mcts_gen/games/chess_mcts.py` file to make the tests pass.
    4.  Updating `README.md` with installation instructions.
    5.  Updating `docs/quickstart.rst` with installation instructions.
    6.  Updating the Japanese localization files (`.po` files).

**Ordering Strategy**:
- TDD order: `pyproject.toml` update -> Test creation -> Implementation -> Documentation.

**Estimated Output**: ~6-8 ordered tasks in `tasks.md`.

## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved
- [ ] Complexity deviations documented
