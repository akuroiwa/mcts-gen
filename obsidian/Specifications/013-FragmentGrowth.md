# Spec-013: Fragment-based Growth and Size Control

## Objective
Enhance `ligand_mcts.py` to support adding multi-atom fragments (generated from external materials) in addition to single atoms. Improve conformational diversity and provide mechanisms for AI-guided ligand size control.

## Key Features
1. **Fragment-based Actions**:
   - Extend `LigandAction` and `LigandState` to allow adding fragments from the `fragment_library` created via BRICS.
   - Maintain compatibility with existing single-atom growth.
2. **Conformational Diversity**:
   - Utilize RDKit's conformer generation to explore different orientations of fragments when they are attached.
   - Ensure the MCTS nodes can represent and distinguish between these different orientations (leveraging the duck typing fix).
3. **Size Control**:
   - Allow the AI to estimate or set a target number of atoms (or physical length) for the ligand based on the binding pocket size.
   - Implement rewards or constraints that encourage the search to reach this target size.

## User Scenarios
- **Scenario 1: Fragment Growth**: User provides a `smiles.csv`. AI generates fragments and builds the ligand using these fragments as building blocks, speeding up the search and ensuring chemical relevance.
- **Scenario 2: Orientation Search**: AI explores different attachment angles for a benzene ring to maximize pocket complementarity.
- **Scenario 3: Size Estimation**: AI analyzes the 8c7y pocket, estimates a 30-atom target size, and guides the MCTS to fill the pocket space effectively.

## Implementation Plan
1. **Research RDKit Conformer Logic**: Find the specific arguments to reflect orientation diversity.
2. **Modify `LigandState.legal_actions`**: Generate actions for multi-atom fragments.
3. **Update `Evaluator`**: Incorporate size-based rewards.
4. **Update AI Prompt**: Guide the agent on size estimation.
