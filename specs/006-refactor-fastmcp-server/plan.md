# Implementation Plan: Refactor fastmcp_server to use @mcp.prompt

**Branch**: `006-refactor-fastmcp-server` | **Date**: 2025-10-18 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/006-refactor-fastmcp-server/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → If not found: ERROR "No feature spec at {path}"
2. Fill Technical Context (scan for NEEDS CLARIFICATION)
   → Detect Project Type from context (web=frontend+backend, mobile=app+api)
   → Set Structure Decision based on project type
3. Evaluate Constitution Check section below
   → If violations exist: Document in Complexity Tracking
   → If no justification possible: ERROR "Simplify approach first"
   → Update Progress Tracking: Initial Constitution Check
4. Execute Phase 0 → research.md
   → If NEEDS CLARIFICATION remain: ERROR "Resolve unknowns"
5. Execute Phase 1 → contracts, data-model.md, quickstart.md, agent-specific template file (e.g., `CLAUDE.md` for Claude Code, `.github/copilot-instructions.md` for GitHub Copilot, or `GEMINI.md` for Gemini CLI).
6. Re-evaluate Constitution Check section
   → If new violations: Refactor design, return to Phase 1
   → Update Progress Tracking: Post-Design Constitution Check
7. Plan Phase 2 → Describe task generation approach (DO NOT create tasks.md)
8. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS at step 7. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary
This feature refactors the `mcts-gen` package to embed agent instructions directly into `fastmcp_server.py` using the `@mcp.prompt` decorator. This removes the dependency on the external `AGENTS.md` file, simplifying package distribution and user setup. The documentation will be updated to reflect this change, and the package version will be bumped to `0.0.2`.

## Technical Context
**Language/Version**: Python >=3.8
**Primary Dependencies**: fastmcp, mcts, mcts-solver
**Storage**: N/A
**Testing**: pytest
**Target Platform**: Linux server
**Project Type**: Single project (library)
**Performance Goals**: N/A
**Constraints**: N/A
**Scale/Scope**: N/A

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Simplicity**:
- Projects: 1 (mcts-gen library)
- Using framework directly? Yes (fastmcp)
- Single data model? Yes
- Avoiding patterns? Yes

**Architecture**:
- EVERY feature as library? Yes
- Libraries listed: `mcts-gen` (A generic MCTS framework)
- CLI per library: The package provides a runnable module `mcts_gen.fastmcp_server`.
- Library docs: N/A

**Testing (NON-NEGOTIABLE)**:
- RED-GREEN-Refactor cycle enforced? Yes, will be followed.
- Git commits show tests before implementation? Yes, will be followed.
- Order: Contract→Integration→E2E→Unit strictly followed? Yes.
- Real dependencies used? Yes.
- Integration tests for: new libraries, contract changes, shared schemas? Yes, contract tests will validate the MCP prompt.

**Observability**:
- Structured logging included? To be confirmed during implementation.
- Frontend logs → backend? N/A
- Error context sufficient? To be confirmed during implementation.

**Versioning**:
- Version number assigned? Yes, `0.0.2`.
- BUILD increments on every change? N/A
- Breaking changes handled? Yes, this is a breaking change for users relying on `AGENTS.md`, and it's handled by a minor version bump and clear documentation.

## Project Structure

### Documentation (this feature)
```
specs/006-refactor-fastmcp-server/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
# Option 1: Single project (DEFAULT)
src/
└── mcts_gen/
    ├── __init__.py
    ├── fastmcp_server.py
    ├── games/
    ├── models/
    └── services/

tests/
├── contract/
├── integration/
└── unit/
```

**Structure Decision**: Option 1: Single project

## Phase 0: Outline & Research
1. **Extract unknowns from Technical Context**: All clear.
2. **Generate and dispatch research agents**: N/A.
3. **Consolidate findings** in `research.md`: Done.

**Output**: `research.md` with all NEEDS CLARIFICATION resolved.

## Phase 1: Design & Contracts
*Prerequisites: research.md complete*

1. **Extract entities from feature spec** → `data-model.md`: Done. No new entities.
2. **Generate API contracts**: Done. No new contracts.
3. **Generate contract tests**: Will be done in the implementation phase.
4. **Extract test scenarios** from user stories → `quickstart.md`: Done.
5. **Update agent file incrementally**: N/A for this project setup.

**Output**: `data-model.md`, `/contracts/`, `quickstart.md`.

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `/templates/tasks-template.md` as base.
- Generate tasks based on the Functional Requirements in `spec.md`.
- **FR-001 & FR-002**: Create a task to refactor `fastmcp_server.py` and delete `AGENTS.md`.
- **FR-003 & FR-004**: Create a task to update `pyproject.toml`.
- **FR-005**: Create a task to update `docs/conf.py`.
- **FR-006**: Create a task to update `README.md`.
- **FR-007**: Create a task to update `docs/quickstart.rst`.
- Create tasks for writing contract and integration tests to verify the new prompt mechanism.

**Ordering Strategy**:
1.  Update `pyproject.toml` and `docs/conf.py` (versioning).
2.  Write a failing contract test that checks for the new `@mcp.prompt`.
3.  Refactor `fastmcp_server.py` to use `@mcp.prompt` and make the test pass.
4.  Delete `src/mcts_gen/AGENTS.md`.
5.  Update `README.md` and `docs/quickstart.rst`.
6.  Run all tests to ensure no regressions.

**Estimated Output**: ~7-10 numbered, ordered tasks in `tasks.md`.

## Complexity Tracking
No violations identified.

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

---
*Based on Constitution v2.1.1 - See `/memory/constitution.md`*