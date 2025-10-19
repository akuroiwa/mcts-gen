# Quickstart: Using the mcts-gen Server

This guide explains how to run the `mcts-gen` server and interact with it.

## Installation

First, install the package from PyPI:

```bash
pip install mcts-gen
```

## Running the Server

The core agent instructions are now built directly into the server using the `@mcp.prompt` decorator. You no longer need to manage a separate `AGENTS.md` file.

To start the server, run the following command:

```bash
python -m mcts_gen.fastmcp_server
```

The server will start and be ready to accept connections from an MCP-compatible client.

## Supplying Additional Context

The built-in prompts cover the primary workflow for the MCTS agent. If you need to provide *additional* instructions or context to the agent for a specific session, you can still do so through your client's context configuration (e.g., `.gemini/settings.json` for the Gemini CLI).

This additional context will be supplied to the agent alongside the built-in prompts, but it will not override them. This is useful for providing temporary or experimental instructions without modifying the core package.
