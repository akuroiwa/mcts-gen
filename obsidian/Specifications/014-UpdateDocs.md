# Spec-014: Documentation and Translation Update

## Objective
Update the official project manuals to reflect the enhancements in v0.0.4+, including the Search Limit mechanism and fragment-based ligand growth, and provide a full Japanese translation.

## Scope
- `docs/quickstart.rst`: Added section on `run_mcts_analysis` and updated ligand generation details.
- `docs/paper.rst`: Updated sections to discuss strategic budget management (Search Limit) and conformational diversity.
- `docs/locales/ja/LC_MESSAGES/`: Full Japanese translation of new content.

## Key Changes
1. **Search Limit Documentation**: Explained how `run_mcts_analysis` allows batching MCTS rounds to avoid API limits and improve precision.
2. **Fragment Growth details**: Documented support for multi-atom fragments, covalent bond formation, and orientation (conformation) diversity.
3. **Japanese Translation**: Standardized RST syntax for Japanese (spaces around markers) to ensure clean Sphinx builds.

## Verification
- Built HTML docs in English and Japanese.
- Verified build logs are free of warnings/errors.
