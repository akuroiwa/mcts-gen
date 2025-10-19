# Tasks: Refactor fastmcp_server to use @mcp.prompt

**Input**: Design documents from `/specs/006-refactor-fastmcp-server/`
**Prerequisites**: plan.md, research.md, data-model.md, quickstart.md

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- Paths shown below assume a single project structure as defined in `plan.md`.

## Phase 3.1: Setup & Versioning
- [ ] T001: In `pyproject.toml`, update the `version` from "0.0.1" to "0.0.2".
- [ ] T002: In `pyproject.toml`, comment out the `[tool.setuptools.package-data]` section to remove `AGENTS.md` from the build.
- [ ] T003: In `docs/conf.py`, update the `version` and `release` variables to "0.0.2".

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: This test MUST be written and MUST FAIL before ANY implementation**
- [ ] T004: Create a new contract test file `tests/contract/test_mcp_prompts.py`. This test should start the `fastmcp_server`, connect to it, and verify that the `mcts_autonomous_search` prompt is available and contains the expected workflow instructions. The test MUST fail before the server is modified.

## Phase 3.3: Core Implementation (ONLY after T004 is failing)
- [ ] T005: Modify `src/mcts_gen/fastmcp_server.py` to embed the agent instructions using the `@mcp.prompt` decorator for the `mcts_autonomous_search` prompt. This will make T004 pass.
- [ ] T006: Delete the now-redundant file `src/mcts_gen/AGENTS.md`.

## Phase 3.4: Documentation
- [ ] T007 [P]: Update `README.md` to remove references to `AGENTS.md` and explain that prompts are now built-in. Add a section explaining how users can provide *additional* context via their client configuration.
- [ ] T008 [P]: Update `docs/quickstart.rst` with the same information provided in the `README.md` update.

## Phase 3.5: Polish & Verification
- [ ] T009: Run the full test suite using `pytest` to confirm that all tests, including the new contract test and existing tests, pass without regression.

## Dependencies
- **T001, T002, T003** can be done first or in parallel.
- **T004** (Test) must be completed and failing before **T005** (Implementation).
- **T005** blocks **T006** (file deletion).
- **T007, T008** (Docs) can be done in parallel after the core implementation is understood.
- **T009** (Verification) must be the final step.

## Parallel Example
```
# The documentation tasks can be run in parallel:
Task: "Update README.md to explain the new built-in prompt mechanism..."
Task: "Update docs/quickstart.rst with the same information..."
```
