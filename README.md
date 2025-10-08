# Generic MCTS Framework with AI-driven Policy/Value

This project implements a generic Monte Carlo Tree Search (MCTS) framework inspired by AlphaZero, designed for versatility and extensibility. It can be used as a standalone Python library, a local REPL, a standard Web API (FastAPI), or a specialized MCP server for AI agent integration.

## Features

-   **AlphaZero-like MCTS**: Utilizes the PUCT algorithm for efficient, AI-guided search.
-   **Multiple Interfaces**: Accessible as a local library, a CLI, a FastAPI web server, and a FastMCP server.
-   **AI-Powered Code Generation**: Includes an `AGENTS.md` file to guide AI agents in generating new game logic modules.
-   **Configurable Authentication**: The Web API supports optional API key authentication.
-   **Self-Play Mode**: Capable of running self-play sessions to generate training data.

## Architecture

The framework is built around a core library (`mcts_gen`) that provides the main MCTS logic. This core can be accessed in several ways:

1.  **Local REPL**: For direct, interactive use.
2.  **FastAPI Server**: For standard web clients.
3.  **FastMCP Server**: Wraps the FastAPI server to provide a native tool-based interface for AI agents.

## Quickstart

### Installation

**For Users:**
```bash
pip install mcts-gen
```

**For Developers:**
```bash
# Clone the repository
git clone https://github.com/akuroiwa/mcts-gen.git
cd mcts-gen

# Install in editable mode with dev dependencies
python -m venv venv
source venv/bin/activate
pip install -e .[dev]
```

### Running the Servers

**1. FastAPI Server (for web clients):**
```bash
uvicorn mcts_gen.api.main:app --reload --port 8000
```

**2. FastMCP Server (for AI agents):**
```bash
python -m mcts_gen.fastmcp_server
```

### Local Execution (REPL)

1.  Create a `config.json` file in the project root:
    ```json
    {
      "state_module": "mcts_gen.games.dummy_game",
      "state_class": "TicTacToeDummy"
    }
    ```
2.  Run the interactive REPL:
    ```bash
    python -m mcts_gen.cli.repl
    ```

## AI Agent Integration (gemini-cli)

This framework is designed to be used with AI agents like `gemini-cli`. The agent can interact with the MCTS engine through a set of tools exposed by the FastMCP server.

### Setup with `gemini-cli`

`gemini-cli` can automatically manage the MCTS server process for you. Here’s how to set it up:

1.  **Create/Update Settings**: Create or update your `gemini-cli` settings file at `~/.gemini/settings.json`. Add a `mcpServers` entry to tell the CLI how to run the `mcts-gen` server.

    ```json
    {
      "mcpServers": {
        "mcts-gen": {
          "command": "python",
          "args": ["-m", "mcts_gen.fastmcp_server"],
          "context": "/path/to/your/mcts-gen/AGENTS.md"
        }
      }
    }
    ```
    - **Important**: Replace `/path/to/your/mcts-gen/AGENTS.md` with the absolute path to the `AGENTS.md` file in this project.
    - The `"command"` and `"args"` tell `gemini-cli` how to start the server. It will handle starting and stopping it automatically.

2.  **Start `gemini-cli`**: Launch `gemini-cli` in your project directory. It will automatically detect the configuration and make the `mcts-gen` tools available.

3.  **Interact**: You can now instruct the agent with natural language. `gemini-cli` will manage the server in the background.

    -   `mcts-genのinitツールを、ゲームmcts_gen.games.dummy_gameのTicTacToeDummyクラスで呼び出して。` (Initialize the TicTacToeDummy game.)
    -   `stepツールを100回実行して。` (Run the step tool 100 times.)
    -   `bestツールを呼び出して最善手を確認して。` (Call the best tool to see the best move.)

## Development

This project was developed using `spec-kit` for specification-driven development and `gemini-cli` for AI-assisted coding.

### Testing

To run all tests:
```bash
python -m pytest
```

## License

[Specify your license here, e.g., MIT License]