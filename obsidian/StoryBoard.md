# MCTS-Gen Project StoryBoard

## Project Overview
A generic MCTS framework driven by an external AI agent, supporting games like Chess, Shogi, and Ligand Generation.

## Current Status
- **Phase**: Transitioning to `antigravity-cli` and Obsidian-based specification management.
- **Last Milestone**: Successfully verified `ligand_mcts.py` with `8c7y` protein pocket.
- **Active Context**: Moving from manual tool calls to high-level analysis tools to avoid loop detection issues.

## Active Specs & Tasks
- [ ] **Spec-011: High-Level Analysis Tool**
    - Status: Planned
    - Goal: Implement `run_mcts_analysis` to encapsulate MCTS loops and stop conditions.
- [ ] **Spec-012: Ligand MCTS Docstring Enhancement**
    - Status: Planned
    - Goal: Document `source_molecule_path` and external dependency usage to guide AI agents.

## Specification Index
- [[Specifications/007-LigandMCTS|007: Ligand MCTS Module]]
- [[Specifications/008-AutonomousLearning|008: Autonomous Initialization Learning]]
- [[Specifications/009-ExternalSource|009: External Molecule Source for Ligand MCTS]]
- [[Specifications/010-GameSummary|010: PGN/KIF Summary for Chess/Shogi]]

## Session Logs
- [[Session_Summary_20251210|Latest Session: 2025-12-10 (Transition to Obsidian)]]
