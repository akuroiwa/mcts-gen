# MCTS-Gen Project StoryBoard

## Project Overview
A generic MCTS framework driven by an external AI agent, supporting games like Chess, Shogi, and Ligand Generation.

## Current Status
- **Phase**: Implementing fragment-based growth and enhancing conformational diversity.
- **Last Milestone**: Successfully implemented `run_mcts_analysis` and resolved `LigandAction` duck typing issues. Verified 8c7y simulation.
- **Active Context**: Transitioning to fragment-based ligand growth and updating documentation.

## Active Specs & Tasks
- [x] **Spec-011: High-Level Analysis Tool**
    - Status: Completed
    - Goal: Implemented `run_mcts_analysis` to encapsulate MCTS loops.
- [x] **Spec-012: Ligand MCTS Docstring Enhancement**
    - Status: Completed
    - Goal: Documented `source_molecule_path` and duck typing improvements.
- [ ] **Spec-013: Fragment-based Growth and Size Control**
    - Status: Planned
    - Goal: Enable adding fragments (from materials) in addition to single atoms. Handle conformation diversity and size estimation.
- [ ] **Spec-014: Documentation and Translation Update**
    - Status: Planned
    - Goal: Update manuals and translate to Japanese to reflect the new features.

## Specification Index
- [[Specifications/011-HighLevelAnalysis|011: High-Level Analysis Tool (run_mcts_analysis)]]
- [[Specifications/012-LigandMCTS_Robustness|012: Ligand MCTS Robustness & Duck Typing]]
- [[Specifications/013-FragmentGrowth|013: Fragment-based Growth & Size Control]]
...
## Session Logs
- [[Session_Summary_20251210|Latest Session: 2025-12-10 (Transition to Obsidian)]]
