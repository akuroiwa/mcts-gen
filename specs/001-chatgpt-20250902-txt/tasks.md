# Tasks: AI-Augmented UCT Framework

**Input**: Design documents from `/specs/001-chatgpt-20250902-txt/`

## Phase 1: Core Engine & Tooling for Policy Pruning (TDD)

- [X] T001: Implement `get_possible_actions` tool in `AiGpSimulator` and its corresponding test.
- [ ] T002: Modify the `run_mcts_round` tool in `AiGpSimulator` to accept a new argument: `actions_to_expand: List[str] | None`.
- [ ] T003: Write a test in `test_simulator_tools.py` to verify that `run_mcts_round`, when given `actions_to_expand`, correctly passes this list to the engine.
- [ ] T004: Modify `McpMcts.expand` to use the `actions_to_expand` list for pruning if it is provided.
- [ ] T005: Run all tests until the new Policy Pruning mechanism is stable and functional.

## Phase 2: Simulator State & Finalization

- [ ] T006: Correctly implement the logic inside `run_mcts_round` to update `improvement` and other metrics.
- [ ] T007: Write tests to verify the correctness of the metrics returned by `run_mcts_round`.

## Phase 3: Documentation

- [ ] T008: Update `AGENTS.md` to detail the final workflow: get actions -> filter list -> run rounds with filtered list.
- [ ] T009: Write the research paper as outlined in `plan.md`.
- [ ] T010: (User Task) Provide a list of any remaining obsolete files for the user to delete.
