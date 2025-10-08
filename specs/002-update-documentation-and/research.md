# Research for Documentation and Release Automation

**Status**: Complete

This document outlines the research and decisions made for the documentation and release automation feature. As the requirements were well-defined, this research phase primarily confirms the use of standard, best-practice technologies for each requirement.

---

### Topic 1: Optional Dependencies in `pyproject.toml`

- **Decision**: Use the `[project.optional-dependencies]` table in `pyproject.toml` to define game-specific extras (e.g., `shogi`).
- **Rationale**: This is the standard, PEP 621 compliant method for declaring optional dependencies. It allows users to install extra functionality on demand (e.g., `pip install mcts-gen[shogi]`) without bloating the core installation. This is the universally accepted best practice.
- **Alternatives Considered**: None. Including all dependencies in the core installation is not desirable.

---

### Topic 2: Documentation Tooling

- **Decision**: Continue to use the existing project setup of reStructuredText (`.rst`) with the Sphinx documentation generator.
- **Rationale**: The project is already configured with Sphinx (`docs/conf.py`, etc.). Maintaining a consistent toolchain is efficient. Sphinx is the de-facto standard for Python project documentation and is highly capable.
- **Alternatives Considered**: Migrating to a different tool (e.g., MkDocs) would introduce unnecessary work and provides no significant benefit over the existing setup.

---

### Topic 3: CI/CD for PyPI Publishing

- **Decision**: Implement the release workflow using GitHub Actions.
- **Rationale**: GitHub Actions is tightly integrated with the source code repository, provides a generous free tier for public projects, and has robust, community-vetted actions for building and publishing Python packages to PyPI (e.g., `actions/setup-python`, `pypa/gh-action-pypi-publish`).
- **Alternatives Considered**: External CI/CD services (like CircleCI or Travis CI) would require additional configuration and integration effort.

---
