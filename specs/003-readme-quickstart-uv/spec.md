# Feature Specification: READMEとquickstartにuvによる環境管理とfastmcpコマンドの設定方法を追加する

**Feature Branch**: `003-readme-quickstart-uv`
**Status**: Draft

---

## User Scenarios & Testing

### Primary User Story
As a new user of `mcts-gen`, I want to find clear instructions on how to set up my Python environment using `uv` and configure the project to work with `gemini-cli` via the `fastmcp` command, so that I can quickly get started with the project.

### Acceptance Scenarios
1. **Given** a user has cloned the `mcts-gen` repository, **When** they read `README.md`, **Then** they find a section explaining how to install and use `uv` for environment setup and how to run the `fastmcp install gemini-cli` command.
2. **Given** a user is reading the documentation, **When** they navigate to `docs/quickstart.rst`, **Then** they find the same detailed setup instructions for `uv` and `fastmcp`.

---

## Requirements

### Functional Requirements
- **FR-001**: The `README.md` file MUST be updated to include a new section detailing the setup process using `uv`.
- **FR-002**: The `docs/quickstart.rst` file MUST be updated to include the same setup instructions.
- **FR-003**: The instructions MUST include the following steps:
    - How to install `pipx` (`sudo apt install pipx`).
    - How to install `uv` (`pipx install uv`).
    - How to create and activate a virtual environment (`uv venv` and `source .venv/bin/activate`).
    - How to install the project dependencies (`uv pip install mcts-gen[shogi]`).
    - The exact `fastmcp install gemini-cli` command to run, including the path to `fastmcp_server.py:mcp`.
- **FR-004**: The documentation MUST mention that running the `fastmcp` command generates the `.gemini/settings.json` file.
- **FR-005**: The documentation MUST explain why the `:mcp` suffix is necessary for the `fastmcp_server.py` script.