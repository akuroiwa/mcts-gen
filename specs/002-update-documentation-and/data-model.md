# Data Model for Documentation and Release Automation

**Status**: Complete

This feature does not introduce new data entities within the application code. Instead, the "data model" for this feature consists of the configuration and documentation artifacts that will be created or modified.

---

### Artifacts

1.  **`pyproject.toml`**
    -   **Description**: The primary project definition file.
    -   **Change**: It will be modified to include an `[project.optional-dependencies]` table to allow for installation of game-specific extras like `shogi`.

2.  **`README.md`**
    -   **Description**: The main entry-point documentation for the project.
    -   **Change**: Content will be updated to reflect the current FastMCP-based architecture and remove outdated information about the FastAPI server.

3.  **`docs/` directory files**
    -   **Description**: The Sphinx-based project documentation.
    -   **Change**: `quickstart.rst`, `paper.rst`, and `modules.rst` will be updated with new content, links, and generated API references.

4.  **`.github/workflows/release.yml`** (New File)
    -   **Description**: A new GitHub Actions workflow file.
    -   **Change**: This file will define a CI/CD pipeline that automatically builds and publishes the package to PyPI and TestPyPI when a new version tag is pushed.

5.  **`MANIFEST.in`**
    -   **Description**: Specifies which files to include in the source distribution.
    -   **Change**: Will be updated to ensure `LICENSE.txt` is included in the package.

---
