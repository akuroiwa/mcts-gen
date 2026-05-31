# Implementation Plan: Documentation and Translation Update

## Technical Context

- **Documentation Engine**: Sphinx (reStructuredText).
- **Translation System**: gettext (`.po` files).
- **Current Manuals**:
    - `docs/quickstart.rst`: Basic setup and usage.
    - `docs/paper.rst`: Technical background and architecture.
- **New Features to Document**:
    - `run_mcts_analysis` tool (Search Limit).
    - Fragment-based growth (covalent bonds).
    - Conformation/orientation diversity.
    - `target_size` parameter for AI guidance.

## Proposed Changes

### Phase 1: Update English Documentation

1. **`docs/quickstart.rst`**:
    - Add "Advanced Search with Search Limit" section.
    - Update "Ligand Generation" section with fragment growth and `target_size`.
    - Mention duck typing fix for stability.
2. **`docs/paper.rst`**:
    - Update Section 1 & 6 to reflect the batch execution model.
    - Explain the "Search Limit" as a strategic budget management tool.

### Phase 2: Japanese Translation

1. **Update POT/PO files**:
    - Run `make gettext` (or equivalent) if needed, but normally we update `.po` files manually or via a script.
    - Update `docs/locales/ja/LC_MESSAGES/quickstart.po` and `paper.po`.
2. **Translation**:
    - Provide high-quality Japanese translation for all new/modified paragraphs.

## Verification Plan

1. **Build Test**:
    - Run `make html` in the `docs/` directory.
    - Check for warnings/errors in Sphinx output.
2. **Visual Inspection**:
    - Open `_build/html/index.html` and verify the new sections are rendered correctly in both English and Japanese.
