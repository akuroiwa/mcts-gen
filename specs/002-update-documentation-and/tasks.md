# Tasks: Documentation and Release Automation

**Input**: Design documents from `/specs/002-update-documentation-and/`

## Execution Flow
This task list is generated based on the requirements in `spec.md` and the design in `plan.md`. The tasks are ordered to respect dependencies.

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Paths are relative to the repository root.

---

## Phase 1: Configuration Setup

- [ ] **T001**: **Update `pyproject.toml`**. Add the `[project.optional-dependencies]` table with a `shogi` key, defining `python-shogi` as a dependency. This corresponds to **FR-004**.

- [ ] **T002**: **Verify `MANIFEST.in`**. Ensure the file contains `include LICENSE.txt`. This corresponds to **FR-010**.

- [ ] **T003**: **Verify optional dependency installation**. After T001, run a shell command to create a temporary virtual environment and test `pip install .[shogi]` to confirm it works as expected.

## Phase 2: Documentation Update

- [ ] **T004** [P]: **Update `README.md`**. Replace outdated content regarding the FastAPI server with the new FastMCP-based architecture, setup, and installation instructions, as detailed in `quickstart.md`. This corresponds to **FR-001, FR-002, FR-003**.

- [ ] **T005** [P]: **Update `docs/quickstart.rst`**. Update the content to match the new installation and setup procedures from `quickstart.md`. This corresponds to **FR-001, FR-002, FR-003**.

- [ ] **T006** [P]: **Update `docs/paper.rst`**. Add the specified reference links to the document without altering the existing prose. This corresponds to **FR-005**.

- [ ] **T007**: **Update `docs/modules.rst`**. Update the API reference to reflect the current source code structure. This may involve running `sphinx-apidoc` or manually editing the file. This corresponds to **FR-006**.

## Phase 3: CI/CD Workflow Creation

- [ ] **T008**: **Create workflow directory**. Create the `.github/workflows` directory if it does not already exist.

- [ ] **T009**: **Create `release.yml` workflow file**. Inside `.github/workflows/`, create a new file named `release.yml`. This workflow should trigger on pushes to tags matching `v*.*.*`. It must define two jobs: one for publishing to TestPyPI (if the tag includes a `-test` suffix) and one for publishing to the official PyPI. Use the `pypa/gh-action-pypi-publish` action and reference a `PYPI_API_TOKEN` secret. This corresponds to **FR-007, FR-008, FR-009**.

## Dependencies

- `T003` depends on `T001`.
- All other tasks in Phase 1, 2, and 3 can technically be run in parallel, but are grouped logically.

## Parallel Execution Example

The documentation tasks can be run in parallel:
```
Task: "Update `README.md`..."
Task: "Update `docs/quickstart.rst`..."
Task: "Update `docs/paper.rst`..."
```
