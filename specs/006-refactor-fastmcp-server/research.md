# Research: Prompt Handling Strategy

## Decision
The project will adopt the `@mcp.prompt` decorator within `fastmcp_server.py` as the sole method for defining the core agent instructions. The external `AGENTS.md` file will be removed.

## Rationale
1.  **Simplification of Distribution:** Embedding prompts in the code eliminates the need for users to manage or correctly place a separate `AGENTS.md` file. This makes the PyPI package truly self-contained and improves the out-of-the-box experience.
2.  **Single Source of Truth:** It ensures that the agent's instructions are always in sync with the code version. This prevents potential mismatches between the server logic and an outdated external context file.
3.  **Reduced Maintenance:** It simplifies the build and packaging process by removing the `package-data` dependency in `pyproject.toml`.

## Alternatives Considered
1.  **Hybrid Approach:** A solution was considered where `@mcp.prompt` would be the default, but an `AGENTS.md` file could be used as an override. This was rejected due to increased complexity in the server's startup logic and potential user confusion.
2.  **File-Only Approach:** The previous method of relying solely on `AGENTS.md`. This was rejected as it complicates the user setup process.
