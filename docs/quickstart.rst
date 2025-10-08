.. _quickstart:

Quickstart
==========

Installation
------------

**For Users:**

.. code-block:: bash

   pip install mcts-gen

**For Developers:**

.. code-block:: bash

   # Clone the repository
   git clone https://github.com/akuroiwa/mcts-gen.git
   cd mcts-gen

   # Install in editable mode with dev dependencies
   python -m venv venv
   source venv/bin/activate
   pip install -e .[dev]

Running the Servers
-------------------

**1. FastAPI Server (for web clients):**

.. code-block:: bash

   uvicorn mcts_gen.api.main:app --reload --port 8000

**2. FastMCP Server (for AI agents):**

.. code-block:: bash

   python -m mcts_gen.fastmcp_server

Local Execution (REPL)
----------------------

1.  Create a ``config.json`` file in the project root:

    .. code-block:: json

       {
         "state_module": "mcts_gen.games.dummy_game",
         "state_class": "TicTacToeDummy"
       }

2.  Run the interactive REPL:

    .. code-block:: bash

       python -m mcts_gen.cli.repl

AI Agent Integration (Gemini CLI)
---------------------------------

To enable an AI agent like Gemini CLI to effectively use this framework, you need to provide it with the agent instructions.

1.  **Locate ``AGENTS.md``**: This file is in the root of the project.
2.  **Configure Gemini CLI**: Set the ``contextFileName`` in your ``~/.gemini/settings.json`` to point to the absolute path of the ``AGENTS.md`` file in this project.

    .. code-block:: json

       { "contextFileName": "/path/to/your/mcts-gen/AGENTS.md" }

3.  **Register the Tools**: Start the FastMCP server and register it with your agent:

    .. code-block:: bash

       # In one terminal, start the server
       python -m mcts_gen.fastmcp_server

       # In your Gemini CLI session, register the server
       /tool register http://127.0.0.1:8000

4.  **Interact**: You can now instruct the agent with natural language. For example:

    -   "Create a game of Tic-Tac-Toe for me."
    -   "Run a search on the current Tic-Tac-Toe game for 100 steps."
