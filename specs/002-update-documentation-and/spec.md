# Feature Specification: Documentation and Release Automation

**Feature Branch**: `002-update-documentation-and`  
**Created**: 2025-10-08  
**Status**: Draft  
**Input**: User description: "Update documentation and automate release workflow"

---

## User Scenarios & Testing *(mandatory)*

### Primary User Story
As a project maintainer, I want to update the project's documentation to reflect the latest code changes and automate the package release process to PyPI, so that users have accurate information and new versions can be published efficiently and reliably.

### Acceptance Scenarios
1. **Given** the outdated `README.md`, **When** the documentation is updated, **Then** it should accurately describe the current FastMCP-based architecture and setup.
2. **Given** the outdated `docs/` directory, **When** the documentation is updated, **Then** `quickstart.rst`, `paper.rst`, and `modules.rst` should be current.
3. **Given** the `pyproject.toml` without optional dependencies, **When** it is updated, **Then** users should be able to install game-specific dependencies using `pip install mcts-gen[shogi]`.
4. **Given** no release workflow exists, **When** a new git tag matching `v*` is pushed, **Then** a GitHub Actions workflow should automatically build and publish the package to PyPI.

### Edge Cases
- What happens when the PyPI token is invalid? The release workflow should fail with a clear error.
- How does the system handle missing game dependencies if not installed via optional dependencies? The program should raise an `ImportError` with a helpful message.

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: System MUST provide updated `README.md` and `docs/quickstart.rst` detailing the removal of the FastAPI server and the new FastMCP-based usage.
- **FR-002**: Documentation MUST include instructions for setting up the FastMCP server via `.gemini/settings.json`, explaining the difference between the project-local (`./.gemini/`) and global (`~/.gemini/`) locations.
- **FR-003**: Documentation MUST link to the official `gofastmcp.com` guide for alternative setup methods (e.g., using `uv`).
- **FR-004**: `pyproject.toml` MUST be updated to define optional dependencies for game-specific packages (e.g., `shogi = ["python-shogi"]`).
- **FR-005**: `docs/paper.rst` MUST be updated to include the following reference links without altering the main content:
    - OpenSpiel (`https://github.com/google-deepmind/open_spiel`) as a source for the AlphaZero algorithm.
    - MCTS-Solver paper (`https://www.researchgate.net/publication/220962507_Monte-Carlo_Tree_Search_Solver`).
    - Links to: `https://github.com/pbsinclair42/MCTS`, `https://github.com/akuroiwa/mcts-solver`, `https://github.com/akuroiwa/chess-ant`, `https://chess-ant.readthedocs.io/`, and `https://github.com/gunyarakun/python-shogi`.
- **FR-006**: `docs/modules.rst` API reference MUST be regenerated or updated to reflect the current `src/mcts_gen` codebase.
- **FR-007**: A GitHub Actions workflow file MUST be created in `.github/workflows/` that triggers on new tags (e.g., `v*.*.*`).
- **FR-008**: The workflow MUST support publishing to both the official PyPI repository and the TestPyPI repository for trial runs.
- **FR-009**: The workflow MUST build the Python package and publish it using a secret token (`PYPI_API_TOKEN`).
- **FR-010**: The `MANIFEST.in` file MUST include `LICENSE.txt` to ensure it is part of the source distribution.

---

## Review & Acceptance Checklist

### Content Quality
- [ ] No implementation details (languages, frameworks, APIs)
- [ ] Focused on user value and business needs
- [ ] Written for non-technical stakeholders
- [ ] All mandatory sections completed

### Requirement Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous  
- [ ] Success criteria are measurable
- [ ] Scope is clearly bounded
- [ ] Dependencies and assumptions identified

---